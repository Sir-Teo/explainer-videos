// Open built part pages and exercise their interactive (used by tools/check_course.py).
//   node tools/check_widgets.js _site/stats/part12.html [more pages]
// Fails (exit 1) on a script error, a widget that did not start, a blank canvas, or a page wider than the screen.
// Exits 3 if Playwright is not installed.
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) { console.log("playwright not installed: interactives not exercised"); process.exit(3); }

(async () => {
  const browser = await chromium.launch();
  let bad = 0;
  for (const file of process.argv.slice(2)) {
    const problems = [];
    for (const width of [1280, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      page.on("pageerror", (e) => problems.push(`${width}px: script error: ${e.message}`));
      page.on("console", (m) => { if (m.type() === "error" && !/Failed to load resource|ERR_/.test(m.text())) problems.push(`${width}px: console: ${m.text()}`); });
      await page.goto("file://" + require("path").resolve(file), { waitUntil: "load" });
      await page.waitForTimeout(400);
      const w = page.locator("#try .widget");
      if (!(await w.count())) { problems.push("no interactive on the page"); await page.close(); break; }
      await w.scrollIntoViewIfNeeded();
      const text = await w.innerText();
      if (/failed to start|is not available/.test(text)) problems.push(`${width}px: ${text.slice(0, 200)}`);
      const ink = () => page.evaluate(() => {
        const c = document.querySelector("#try .widget canvas"); if (!c) return -1;
        const d = c.getContext("2d").getImageData(0, 0, c.width, c.height).data, seen = new Set();
        for (let i = 0; i < d.length; i += 4 * 97) seen.add((d[i] << 16) | (d[i + 1] << 8) | d[i + 2]);
        return seen.size;
      });
      if ((await ink()) < 6) problems.push(`${width}px: the canvas is blank or missing`);
      const sliders = w.locator('input[type="range"]');
      for (let i = 0; i < (await sliders.count()); i++) {
        for (const end of ["min", "max", "mid"]) {
          await sliders.nth(i).evaluate((el, end) => {
            const lo = +el.min, hi = +el.max, st = +el.step || 1;
            el.value = end === "min" ? lo : end === "max" ? hi : lo + Math.round((hi - lo) / 2 / st) * st;
            el.dispatchEvent(new Event("input", { bubbles: true }));
          }, end);
          await page.waitForTimeout(30);
        }
      }
      const buttons = w.locator("button");
      for (let i = 0; i < (await buttons.count()); i++) { await buttons.nth(i).click(); await page.waitForTimeout(60); }
      // all sliders at their maximum together, then at their minimum: the corners are where NaNs hide
      for (const end of ["max", "min"]) {
        await w.evaluate((el, end) => el.querySelectorAll('input[type="range"]').forEach((s) => { s.value = end === "max" ? s.max : s.min; s.dispatchEvent(new Event("input", { bubbles: true })); }), end);
        await page.waitForTimeout(60);
        if ((await ink()) < 6) problems.push(`${width}px: blank canvas with every slider at its ${end}`);
        const readout = await w.locator(".readout").innerText().catch(() => "");
        if (/NaN|undefined|Infinity/.test(readout)) problems.push(`${width}px: readout shows ${readout.replace(/\s+/g, " ").slice(0, 160)} (sliders at ${end})`);
      }
      const over = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      if (over > 1) problems.push(`${width}px: the page is ${over}px wider than the screen`);
      await page.close();
    }
    const name = file.split("/").slice(-2).join("/");
    if (problems.length) { bad++; console.log(`${name}: FAILED\n  ` + [...new Set(problems)].join("\n  ")); } else console.log(`${name}: interactive ok`);
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
