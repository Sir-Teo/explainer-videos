// Interactives for Act XIII, the frontier (Parts 58-62).  Each is an experiment the reader takes part in, built on
// the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 58: the tilt after-effect, on you, then predicted by an adapting population code. ----
  function tiltShift(test, adapter, loss) {
    var n = 72, width = 20, num = 0, den = 0, i;
    for (i = 0; i < n; i++) {
      var pref = -90 + 180 * i / n;
      var da = ((adapter - pref + 90) % 180 + 180) % 180 - 90;
      var dt = ((test - pref + 90) % 180 + 180) % 180 - 90;
      var gain = 1 - loss * Math.exp(-da * da / (2 * width * width));
      var r = gain * Math.exp(-dt * dt / (2 * width * width));
      var ang = 2 * pref * Math.PI / 180;
      num += r * Math.sin(ang); den += r * Math.cos(ang);
    }
    var est = Math.atan2(num, den) / 2 * 180 / Math.PI;
    return ((est - test + 90) % 180 + 180) % 180 - 90;
  }
  function grating(ctx, cx, cy, R, angle, spacing) {
    var a = angle * Math.PI / 180, dx = Math.sin(a), dy = -Math.cos(a), nx = Math.cos(a), ny = Math.sin(a), t;
    ctx.save(); ctx.strokeStyle = "#e8eef6"; ctx.lineWidth = Math.max(2, spacing * 0.45);
    for (t = -R + spacing / 2; t < R; t += spacing) {
      var h = Math.sqrt(Math.max(R * R - t * t, 0));
      ctx.beginPath(); ctx.moveTo(cx + t * nx - h * dx, cy + t * ny - h * dy);
      ctx.lineTo(cx + t * nx + h * dx, cy + t * ny + h * dy); ctx.stroke();
    }
    ctx.strokeStyle = "#8a93a3"; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(cx, cy, R, 0, 2 * Math.PI); ctx.stroke();
    ctx.restore();
  }
  W.aftereffect = function (el) {
    var w = null, ADAPT = 20000, TOPUP = 4000, NT = 3;
    var S = { phase: "idle", t0: 0, answers: [], trial: 0 };
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return S.phase === "adapt" || S.phase === "test" || S.phase === "done"; },
      respond: function (side) {
        if (S.phase === "done") { S.phase = "adapt"; S.t0 = T.now(); S.trial = 0; S.answers = []; if (w) w.render(); task.later(tick, 500); return; }
        if (S.phase === "adapt") { task.clear(); S.phase = "test"; if (w) w.render(); return; }
        S.answers.push(side); task.count++; S.trial++;
        if (S.trial >= NT) { S.phase = "done"; if (w) w.render(); return; }
        S.phase = "topup"; S.t0 = T.now(); if (w) w.render(); task.later(tick, 500);
      },
    });
    function tick() {
      if (S.phase !== "adapt" && S.phase !== "topup") return;
      if (T.now() - S.t0 >= (S.phase === "adapt" ? ADAPT : TOPUP)) { S.phase = "test"; if (w) w.render(); return; }
      if (w) w.render();
      task.later(tick, 500);
    }
    w = QB.widget(el, {
      title: "Stare, then look",
      sub: "Press Start and keep your eyes on the yellow dot for twenty seconds while the grating leans clockwise. Then a vertical grating appears: does its top look tilted to the left (F) or to the right (J)? Three tests, each after a four-second top-up of the adapter. On the right, Psyche's population code predicts the shift for any adapter; move the sliders.",
      panels: 2, height: 330,
      controls: [
        { k: "adapter", label: "adapter's tilt (degrees, clockwise)", min: 5, max: 45, step: 5, value: 20, fmt: function (x) { return x.toFixed(0); } },
        { k: "loss", label: "gain lost by adapted units", min: 0.1, max: 0.8, step: 0.05, value: 0.5, fmt: function (x) { return Math.round(100 * x) + "%"; } },
      ],
      buttons: [
        { label: "Start", act: function () { S.phase = "adapt"; S.t0 = T.now(); S.trial = 0; S.answers = []; task.later(tick, 500); } },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.answers = []; S.trial = 0; } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, task), R = Math.min(b.w, b.h) * 0.34;
        if (S.phase === "adapt" || S.phase === "topup") {
          grating(ctx, b.cx, b.cy + 6, R, v.adapter, 14);
          ctx.fillStyle = "#f2c14e"; ctx.beginPath(); ctx.arc(b.cx, b.cy + 6, 5, 0, 2 * Math.PI); ctx.fill();
          ctx.fillStyle = "#cfd6e2"; ctx.font = "13px sans-serif"; ctx.textAlign = "center";
          ctx.fillText(Math.max(0, Math.ceil(((S.phase === "adapt" ? ADAPT : TOPUP) - (T.now() - S.t0)) / 1000)) + " s: keep looking at the dot" + (S.phase === "adapt" ? " (F or J: test now)" : ""), b.cx, b.y + 22);
        } else if (S.phase === "test") {
          grating(ctx, b.cx, b.cy + 6, R, 0, 14);
          ctx.fillStyle = "#cfd6e2"; ctx.font = "13px sans-serif"; ctx.textAlign = "center";
          ctx.fillText("test " + (S.trial + 1) + " of " + NT + ".   F: top tilted left     J: top tilted right", b.cx, b.y + 22);
        } else if (S.phase === "done") {
          var lefts = S.answers.filter(function (x) { return x === 0; }).length;
          T.message(ctx, b, "Tilted left in " + lefts + " of " + NT + " tests" + (lefts >= 2 ? ": the after-effect." : "."),
            "The test grating was exactly vertical. Most people see it tilted away from the adapter, here to the left, by a few degrees. Press F or J to try again, with a different adapter if you like.");
        } else {
          T.message(ctx, b, "On you", "Press Start, then keep your eyes on the dot for twenty seconds.");
        }
        var a = g[1].axes({ x: [-45, 45], y: [-8, 8], title: "Psyche's predicted shift (degrees) against test minus adapter" });
        var xs = [], ys = [], t;
        for (t = -45; t <= 45; t += 2.5) { xs.push(t); ys.push(tiltShift(t, 0, v.loss)); }
        a.line([-45, 45], [0, 0], { color: "#59606b", width: 1 });
        a.line(xs, ys, { color: "#f2c14e", width: 2 });
        var s = tiltShift(-v.adapter, 0, v.loss);
        a.text(-v.adapter, s - 1.2, "vertical: " + s.toFixed(1) + " deg", { align: "center", size: 10 });
      },
      readout: function (v) { return [["vertical seen at", tiltShift(-v.adapter, 0, v.loss).toFixed(1) + " deg"]]; },
      note: "Nothing you choose is stored or sent. The model is Part 58's: 72 units tuned to orientation, adaptation lowering the gain of those near the adapter, and a readout that does not know about the adaptation.",
    });
  };
})();
