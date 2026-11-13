// Interactives for Act I, Asking a Mind a Question (Parts 1-4).  In this series each interactive is an experiment
// the reader takes part in.  Nothing a reader does is stored or sent anywhere: the data live in the page's memory
// and are gone when the page is closed.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;
  var SIMPLE = "#9fd8f0", CHOICE = "#f28fb8", GO = "#3ddc84", LEFT = "#5dadec";

  function now() { return window.performance && performance.now ? performance.now() : Date.now(); }
  function wrap(ctx, text, x, y, maxW, lh) { // centred lines, broken at spaces to fit maxW; returns the next y
    var words = text.split(" "), line = "", i;
    for (i = 0; i < words.length; i++) {
      var t = line ? line + " " + words[i] : words[i];
      if (ctx.measureText(t).width > maxW && line) { ctx.fillText(line, x, y); y += lh; line = words[i]; } else line = t;
    }
    if (line) { ctx.fillText(line, x, y); y += lh; }
    return y;
  }

  // ---- Part 1: your own reaction time, simple and choice -------------------------------------------------------
  W.reactiontime = function (el) {
    var timer = 0, t0 = 0, w = null;
    var S = { phase: "idle", task: "simple", trial: 0, stim: 1, msg: "", box: null, early: 0, wrong: 0,
      rts: { simple: [], choice: [] } };
    function clear() { if (timer) { clearTimeout(timer); timer = 0; } }
    function draw() { if (w) w.render(); }
    function later(fn, ms) { clear(); timer = setTimeout(fn, ms); }
    function next() {
      if (!w) return;
      if (S.trial >= w.v.n) { clear(); S.phase = "done"; draw(); return; }
      S.trial++; S.phase = "wait"; S.msg = "";
      var r = QB.rng(w.state.seed * 977 + S.trial * 131 + (S.task === "choice" ? 7 : 0) + S.early * 17);
      S.stim = S.task === "choice" ? (r() < 0.5 ? 0 : 1) : 1; // 0: blue square, answer left; 1: green circle, right
      draw();
      later(function () {
        S.phase = "go"; draw(); t0 = now();
        later(function () { S.msg = "No response in two seconds."; S.phase = "feedback"; draw(); later(next, 900); }, 2000);
      }, 900 + 1700 * r());
    }
    function start(task) { clear(); S.task = task; S.trial = 0; S.rts[task] = []; S.msg = ""; next(); }
    function respond(side) { // side: 0 left, 1 right, -1 either (the space bar)
      if (S.phase === "wait") {
        S.early++; S.trial--; S.msg = "Too early: wait for the shape."; S.phase = "feedback"; draw(); later(next, 900);
      } else if (S.phase === "go") {
        var rt = now() - t0;
        if (S.task === "simple" || side === S.stim) { S.rts[S.task].push(rt); S.msg = Math.round(rt) + " ms"; }
        else { S.wrong++; S.msg = side < 0 ? "Use F or J, or tap a side." : "Wrong side (not counted)."; }
        S.phase = "feedback"; draw(); later(next, 700);
      }
    }
    var running = function () { return S.phase === "wait" || S.phase === "go" || S.phase === "feedback"; };

    w = QB.widget(el, {
      title: "Your reaction time: simple, then choice",
      sub: "Simple: press the space bar, or tap the dark panel, the moment the grey circle turns green. Choice: a blue square means left (the F key, or tap the left half), a green circle means right (J, or the right half). Then compare your two averages, and move the delay slider to see what a slower device would have recorded.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Trials in a block", min: 5, max: 20, step: 1, value: 8, fmt: function (x) { return x.toFixed(0); } },
        { k: "lag", label: "Pretend your device adds this delay", min: 0, max: 120, step: 5, value: 0, fmt: function (x) { return x.toFixed(0) + " ms"; } },
      ],
      buttons: [
        { label: "Start the simple task", act: function () { start("simple"); } },
        { label: "Start the choice task", act: function () { start("choice"); } },
        { label: "Clear my data", act: function () { clear(); S.phase = "idle"; S.trial = 0; S.early = 0; S.wrong = 0; S.msg = ""; S.rts = { simple: [], choice: [] }; } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = g[0].box, cx = b.x + b.w / 2, cy = b.y + b.h / 2, r = Math.min(b.w, b.h) * 0.16;
        S.box = b;
        ctx.save();
        ctx.fillStyle = "#05070b"; ctx.fillRect(b.x + 6, b.y + 6, b.w - 12, b.h - 12);
        ctx.strokeStyle = C.idea; ctx.lineWidth = 2; ctx.strokeRect(b.x + 6, b.y + 6, b.w - 12, b.h - 12);
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        if (S.phase === "wait" || S.phase === "go") {
          ctx.font = "12px system-ui, sans-serif"; ctx.fillStyle = C.muted;
          ctx.fillText("trial " + S.trial + " of " + v.n, cx, b.y + 24);
          if (S.task === "choice" && S.phase === "wait") { // a fixation cross
            ctx.strokeStyle = C.muted; ctx.lineWidth = 3; ctx.beginPath();
            ctx.moveTo(cx - 12, cy); ctx.lineTo(cx + 12, cy); ctx.moveTo(cx, cy - 12); ctx.lineTo(cx, cy + 12); ctx.stroke();
          } else if (S.phase === "go" && S.stim === 0) {
            ctx.fillStyle = LEFT; ctx.fillRect(cx - r, cy - r, 2 * r, 2 * r);
          } else {
            ctx.fillStyle = S.phase === "go" ? GO : "#3a4150"; ctx.beginPath(); ctx.arc(cx, cy, r, 0, 2 * Math.PI); ctx.fill();
          }
          if (S.task === "choice") {
            ctx.font = "12px system-ui, sans-serif";
            ctx.fillStyle = LEFT; ctx.fillText("square: left (F)", b.x + b.w * 0.25, b.y + b.h - 22);
            ctx.fillStyle = GO; ctx.fillText("circle: right (J)", b.x + b.w * 0.75, b.y + b.h - 22);
          }
        } else {
          ctx.fillStyle = C.ink; ctx.font = "600 15px system-ui, sans-serif";
          var head = S.phase === "feedback" ? S.msg : S.phase === "done" ? "Block finished." : "On you";
          ctx.fillText(head, cx, cy - 26);
          ctx.fillStyle = C.muted; ctx.font = "12.5px system-ui, sans-serif";
          if (S.phase === "done") wrap(ctx, S.task === "simple" ? "Now start the choice task." : "Compare the two rows on the other panel.", cx, cy + 4, b.w - 44, 17);
          else if (S.phase === "idle") wrap(ctx, "Press a Start button. Respond with the space bar, F and J, or by tapping this panel.", cx, cy + 4, b.w - 44, 17);
        }
        ctx.restore();

        var rows = [["simple", SIMPLE, 2], ["choice", CHOICE, 1]], top = 500, i, k;
        for (k = 0; k < 2; k++) for (i = 0; i < S.rts[rows[k][0]].length; i++) top = Math.max(top, S.rts[rows[k][0]][i] + v.lag + 60);
        top = Math.min(2200, Math.ceil(top / 100) * 100);
        var a = g[1].axes({ x: [100, top], y: [0, 3], title: "Each response, and the average of each task", xlabel: "reaction time as recorded (ms)", noY: true });
        a.vline(213, { color: C.muted });
        a.text(213, 2.82, "1,469 adults, calibrated lab: 213", { color: C.muted, dx: 5, size: 11 });
        S.mean = {};
        for (k = 0; k < 2; k++) {
          var xs = S.rts[rows[k][0]], shown = [], ys = [], jr = QB.rng(11 + k);
          for (i = 0; i < xs.length; i++) { shown.push(xs[i] + v.lag); ys.push(rows[k][2] + 0.3 * (jr() - 0.5)); }
          a.text(a.xr[0], rows[k][2] + 0.42, rows[k][0], { color: rows[k][1], dx: 6, bold: true });
          if (xs.length) {
            var m = QB.mean(shown); S.mean[rows[k][0]] = m;
            a.dots(shown, ys, { color: rows[k][1], r: 3.2, alpha: 0.85 });
            a.line([m, m], [rows[k][2] - 0.36, rows[k][2] + 0.36], { color: rows[k][1], width: 2.5 });
          }
        }
        if (S.mean.simple !== undefined && S.mean.choice !== undefined) {
          a.line([S.mean.simple, S.mean.choice], [0.38, 0.38], { color: C.idea, width: 2.5 });
          a.text((S.mean.simple + S.mean.choice) / 2, 0.16, "choice − simple", { color: C.idea, align: "center" });
        }
      },
      readout: function (v) {
        var ms = function (x) { return x === undefined ? "–" : fmt(x, 0) + " ms"; };
        var d = S.mean && S.mean.simple !== undefined && S.mean.choice !== undefined ? S.mean.choice - S.mean.simple : undefined;
        return [["simple, average", ms(S.mean && S.mean.simple)], ["choice, average", ms(S.mean && S.mean.choice)],
          ["choice − simple", ms(d)], ["responses", String(S.rts.simple.length + S.rts.choice.length)],
          ["too early", String(S.early)]];
      },
      note: "Your data stay in this page and are gone when you close it. A browser adds a delay of its own to every time, different on every device, so the absolute times here cannot be compared with a laboratory's or with another person's. The difference between your two tasks can: a constant delay moves both averages and leaves the difference alone, which the slider shows. Reference line: Woods et al. (2015), simple visual reactions measured with calibrated hardware.",
    });

    var canvas = el.querySelector("canvas");
    if (canvas) canvas.addEventListener("pointerdown", function (e) {
      if (!running() || !S.box) return;
      var rect = canvas.getBoundingClientRect(), x = e.clientX - rect.left, y = e.clientY - rect.top, b = S.box;
      if (x < b.x || x > b.x + b.w || y < b.y || y > b.y + b.h) return;
      e.preventDefault();
      respond(x < b.x + b.w / 2 ? 0 : 1);
    });
    document.addEventListener("keydown", function (e) {
      if (!running() || e.repeat) return;
      var key = (e.key || "").toLowerCase();
      if (key === " " || key === "spacebar") { e.preventDefault(); respond(-1); }
      else if (key === "f") respond(0);
      else if (key === "j") respond(1);
    });
  };
})();
