// Interactives for Act VIII, How people differ (Parts 32-33).  Each is an experiment the reader takes part in, built
// on the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 32: a matrix test.  Items built from one to four rules; which option completes the matrix? --------
  W.matrices = function (el) {
    var w = null, OK = "#5bd18b", NO = "#ef6f6c", GOLD = "#f2c14e", BLUE = "#7ec8f5";
    var ATTR = ["shape", "number", "shade", "size"], SHADES = ["#f4f4f4", "#8a8f98", "#3a3f48"], SIZES = [0.42, 0.6, 0.8];
    var RULE = ["stays the same", "steps along the row", "cycles through three values"];
    var S = { phase: "idle", k: 0, items: [], log: [], last: null, t0: 0 };

    // One item: rules[a] is 0 (constant), 1 (progression) or 2 (distribution of three) for each attribute.
    function item(nRules, r) {
      var order = [0, 1, 2, 3], i, j, t, rules = [0, 0, 0, 0], base = [];
      for (i = 3; i > 0; i--) { j = Math.floor(r() * (i + 1)); t = order[i]; order[i] = order[j]; order[j] = t; }
      for (i = 0; i < nRules; i++) rules[order[i]] = r() < 0.5 ? 1 : 2;
      for (i = 0; i < 4; i++) base.push(Math.floor(r() * 3));
      function cell(row, col) {
        return rules.map(function (rl, a) {
          if (rl === 0) return base[a];
          if (rl === 1) return col;
          return (col + row + base[a]) % 3;
        });
      }
      var grid = [], row, col;
      for (row = 0; row < 3; row++) for (col = 0; col < 3; col++) grid.push(cell(row, col));
      var answer = grid[8].slice(), foil = answer.slice(), varying = [];
      for (i = 0; i < 4; i++) if (rules[i] !== 0) varying.push(i);
      // the foil breaks exactly one rule: one rule-governed attribute takes another value
      var a = varying[Math.floor(r() * varying.length)];
      foil[a] = (answer[a] + 1 + Math.floor(r() * 2)) % 3;
      var side = r() < 0.5 ? 0 : 1;
      return { n: nRules, rules: rules, grid: grid, options: side === 0 ? [answer, foil] : [foil, answer], correct: side, broken: a };
    }

    function start(seed) {
      var r = QB.rng(seed * 7919 + 32), ns = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4], i, j, t;
      for (i = ns.length - 1; i > 0; i--) { j = Math.floor(r() * (i + 1)); t = ns[i]; ns[i] = ns[j]; ns[j] = t; }
      S.items = ns.map(function (n) { return item(n, r); });
      S.k = 0; S.log = []; S.last = null; S.phase = "go"; S.t0 = T.now();
    }

    function answer(side) {
      var it = S.items[S.k], rt = T.now() - S.t0;
      S.log.push({ n: it.n, right: side === it.correct, rt: rt, item: it });
      S.last = S.log[S.log.length - 1];
      task.count++;
      S.k++;
      S.phase = "feedback";
      if (w) w.render();
      task.later(function () {
        S.phase = S.k >= S.items.length ? "done" : "go";
        S.t0 = T.now();
        if (w) w.render();
      }, 2000);
    }

    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return S.phase === "go"; },
      respond: function (side) { answer(side); },
    });

    function glyph(ctx, v, x, y, s) {
      // v = [shape, number, shade, size]; s is the cell's side
      // sizes are fixed whatever the count, so a size rule reads the same in every cell; three shapes sit two over one
      var count = v[1] + 1, rad = s * SIZES[v[3]] / 4.6, k, gap = rad * 2.3;
      var pos = count === 1 ? [[0, 0]] : count === 2 ? [[-0.5, 0], [0.5, 0]] : [[-0.5, -0.5], [0.5, -0.5], [0, 0.5]];
      ctx.save();
      ctx.fillStyle = SHADES[v[2]]; ctx.strokeStyle = "#c9ced6"; ctx.lineWidth = 1.2;
      for (k = 0; k < count; k++) {
        var cx = x + s / 2 + pos[k][0] * gap, cy = y + s / 2 + pos[k][1] * gap;
        ctx.beginPath();
        if (v[0] === 0) ctx.arc(cx, cy, rad, 0, 2 * Math.PI);
        else if (v[0] === 1) ctx.rect(cx - rad * 0.88, cy - rad * 0.88, rad * 1.76, rad * 1.76);
        else { ctx.moveTo(cx, cy - rad); ctx.lineTo(cx + rad * 0.95, cy + rad * 0.75); ctx.lineTo(cx - rad * 0.95, cy + rad * 0.75); ctx.closePath(); }
        ctx.fill(); ctx.stroke();
      }
      ctx.restore();
    }

    function drawItem(ctx, b, it) {
      var s = Math.min((b.w - 40) / 3.4, (b.h - 70) / 4.6), gx = b.cx - 1.5 * s, gy = b.y + 18, i;
      ctx.save();
      ctx.strokeStyle = "#5a606b"; ctx.lineWidth = 1;
      for (i = 0; i < 9; i++) {
        var x = gx + s * (i % 3), y = gy + s * Math.floor(i / 3);
        ctx.strokeRect(x, y, s, s);
        if (i < 8) glyph(ctx, it.grid[i], x, y, s);
        else { ctx.fillStyle = GOLD; ctx.font = "600 " + Math.round(s * 0.4) + "px system-ui, sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("?", x + s / 2, y + s / 2); }
      }
      var oy = gy + 3 * s + 0.35 * s;
      [0, 1].forEach(function (k) {
        var ox = b.x + b.w * (k === 0 ? 0.25 : 0.75) - s / 2;
        ctx.strokeStyle = k === 0 ? BLUE : GOLD; ctx.lineWidth = 2; ctx.strokeRect(ox, oy, s, s);
        glyph(ctx, it.options[k], ox, oy, s);
        ctx.fillStyle = k === 0 ? BLUE : GOLD; ctx.font = "600 13px system-ui, sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
        ctx.fillText(k === 0 ? "F (or tap left)" : "J (or tap right)", ox + s / 2, oy + s + 16);
      });
      ctx.restore();
    }

    w = QB.widget(el, {
      title: "A matrix test, built from rules",
      sub: "Twelve items, three each with one, two, three and four rules. In every row, each attribute (shape, number, shade, size) stays the same, steps along the row, or cycles through three values. Pick the option that completes the matrix: press F for the left one or J for the right one, or tap that half. The other option breaks exactly one rule.",
      panels: 2, height: 380, weights: [1.25, 1],
      buttons: [
        { label: "Start", act: function (state) { start(state.seed); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; S.k = 0; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (S.phase === "go") {
          drawItem(ctx, b, S.items[S.k]);
          ctx.save(); ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif"; ctx.textAlign = "left";
          ctx.fillText("Item " + (S.k + 1) + " of " + S.items.length, b.x + 14, b.y + b.h - 14); ctx.restore();
        } else if (S.phase === "feedback" && S.last) {
          var it = S.last.item, parts = [];
          it.rules.forEach(function (rl, a) { if (rl) parts.push(ATTR[a] + " " + RULE[rl]); });
          T.message(ctx, b, (S.last.right ? "Right. " : "Not this time. ") + it.n + " rule" + (it.n > 1 ? "s" : "") + ".",
                    "In each row: " + parts.join("; ") + ". The other option broke the rule for " + ATTR[it.broken] + ".");
        } else if (S.phase === "done") {
          var n = S.log.filter(function (l) { return l.right; }).length;
          T.message(ctx, b, n + " of " + S.log.length + " right.", "With two options, guessing gets half. Look at the chart: if your accuracy fell, or your time rose, as rules were added, you met the limit chapter eight's solver has, the number of rules held at once.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Take your time: accuracy matters here, and the time you take is recorded only on this page.");
        }
        // the chart: accuracy and time by number of rules
        var c2 = g[1].box, cx = g.ctx, x0 = c2.x + 44, x1 = c2.x + c2.w - 14, y0 = c2.y + 34, y1 = c2.y + c2.h * 0.6, k;
        cx.save();
        cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif"; cx.textAlign = "left";
        cx.fillText("Your accuracy by number of rules", c2.x + 10, c2.y + 16);
        cx.strokeStyle = C.muted; cx.lineWidth = 1;
        cx.beginPath(); cx.moveTo(x0, y0); cx.lineTo(x0, y1); cx.lineTo(x1, y1); cx.stroke();
        cx.setLineDash([4, 4]); cx.beginPath(); cx.moveTo(x0, (y0 + y1) / 2); cx.lineTo(x1, (y0 + y1) / 2); cx.stroke(); cx.setLineDash([]);
        cx.fillStyle = C.muted; cx.font = "11px system-ui, sans-serif"; cx.textAlign = "right";
        cx.fillText("100%", x0 - 4, y0 + 4); cx.fillText("chance", x0 - 4, (y0 + y1) / 2 + 4); cx.fillText("0", x0 - 4, y1 + 4);
        var times = [];
        for (k = 1; k <= 4; k++) {
          var rows = S.log.filter(function (l) { return l.n === k; }), bw = (x1 - x0) / 4, bx = x0 + bw * (k - 1) + bw * 0.2;
          var acc = rows.length ? rows.filter(function (l) { return l.right; }).length / rows.length : 0;
          if (rows.length) {
            cx.fillStyle = acc >= 0.75 ? OK : acc > 0.5 ? GOLD : NO;
            cx.fillRect(bx, y1 - (y1 - y0) * acc, bw * 0.6, (y1 - y0) * acc);
          }
          cx.fillStyle = C.muted; cx.textAlign = "center";
          cx.fillText(k + " rule" + (k > 1 ? "s" : ""), bx + bw * 0.3, y1 + 14);
          cx.fillText(rows.length ? rows.filter(function (l) { return l.right; }).length + "/" + rows.length : "-", bx + bw * 0.3, y1 + 28);
          var ok = rows.filter(function (l) { return l.right; });
          times.push(ok.length ? (ok.reduce(function (s, l) { return s + l.rt; }, 0) / ok.length / 1000).toFixed(1) + " s" : "-");
        }
        cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "12px system-ui, sans-serif";
        cx.fillText("Mean time on items you got right: " + times.join(", "), c2.x + 10, y1 + 50);
        cx.fillStyle = C.muted; cx.textAlign = "center";
        var msg = "Carpenter, Just and Shell (1990) found the number of rules explained most of how hard Raven's items were. Twelve items are a very unreliable test: your bars carry the error of chapter six.";
        T.wrap(cx, msg, c2.x + c2.w / 2, y1 + 72, c2.w - 20, 15);
        cx.restore();
      },
      readout: function () {
        var n = S.log.filter(function (l) { return l.right; }).length;
        return [["answers", String(task.count)], ["right", n + " of " + S.log.length]];
      },
      note: "Nothing you choose is stored or sent. The items are generated fresh from rules, like Psyche's in the film; they are not a normed test, and no IQ can be read from them. A real test has many more items, is normed on a large sample of your age group, and reports a band of error around every score.",
    });
  };
})();
