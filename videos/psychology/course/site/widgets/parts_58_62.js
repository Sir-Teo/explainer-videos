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

  // ---- Part 59: design a task for groups or for individuals, then buy reliability with trials. ----
  W.taskdesign = function (el) {
    var w = null;
    var S = { phase: "idle", pred: null, q: 0, preds: [] };
    function rel(share, trials) { var sb = share * 60, err = 2 * 120 * 120 / trials; return sb * sb / (sb * sb + err); }
    function groupD(share, trials) { var sb = share * 60; return (1 - share) * 60 / Math.sqrt(sb * sb + 2 * 120 * 120 / trials); }
    var QS = [
      { share: 0.25, trials: 60, head: "A huge group effect: a reliable measure of each person?",
        why: "Everyone shows the effect, so there is little difference between people left to measure: the reliability paradox (Hedge, Powell and Sumner, 2018)." },
      { share: 0.25, trials: 600, head: "Same task, ten times the trials: reliable now?",
        why: "Trial noise averages away; the between-person differences were there all along. Trials cost participants' time." },
      { share: 0.75, trials: 60, head: "Back to 60 trials, but a task whose effect varies more between people: reliable?",
        why: "Reliability rises, and the group effect falls: a task built for individuals is a weaker demonstration in a group." },
    ];
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return S.phase === "ask" || S.phase === "shown"; },
      respond: function (side) {
        if (S.phase === "shown") { S.q++; S.phase = S.q >= QS.length ? "done" : "ask"; if (w) w.render(); return; }
        S.pred = side; S.preds.push(side); S.phase = "shown"; task.count++; if (w) w.render();
      },
    });
    w = QB.widget(el, {
      title: "A task for groups, or for people?",
      sub: "First a prediction: a Stroop-like effect so robust that 400 people show it with t near 50. Will each person's effect correlate well with itself three weeks later? Press F for well (above 0.7), J for poorly (or tap); then two more versions of the task. The sliders: how much of the effect varies between people, and how many trials each person does.",
      panels: 2, height: 320,
      controls: [
        { k: "share", label: "share of the effect that varies between people", min: 0.05, max: 0.95, step: 0.05, value: 0.25, fmt: function (x) { return x.toFixed(2); } },
        { k: "trials", label: "trials per condition", min: 20, max: 2000, step: 20, value: 60, fmt: function (x) { return x.toFixed(0); } },
      ],
      buttons: [
        { label: "Start", act: function () { S.phase = "ask"; S.pred = null; S.q = 0; S.preds = []; } },
        { label: "Clear", act: function () { S.phase = "idle"; S.pred = null; S.q = 0; S.preds = []; } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        var Q = QS[Math.min(S.q, QS.length - 1)];
        if (S.phase === "ask") {
          T.message(ctx, b, (S.q + 1) + " of 3. " + Q.head, Q.share * 100 + "% of the effect varies between people, " + Q.trials + " trials per condition.   F: yes, retest above 0.7.   J: no, much lower.");
        } else if (S.phase === "shown") {
          var rq = rel(Q.share, Q.trials);
          T.message(ctx, b, "In Psyche the retest correlation is " + rq.toFixed(2) + ", the group effect d " + groupD(Q.share, Q.trials).toFixed(1) + ".",
            "You predicted " + (S.pred ? "a poor measure" : "a good one") + (((rq > 0.7) === (S.pred === 0)) ? ": right. " : ": not this time. ") + Q.why + " Any key: next.");
        } else if (S.phase === "done") {
          T.message(ctx, b, "Three tasks, one trade-off.", "Only more trials buy both a group effect and a reliable measure. Try the sliders: they show the whole curve.");
        } else {
          T.message(ctx, b, "On you", "Press Start for the prediction; the sliders work any time.");
        }
        var a = g[1].axes({ x: [0, 1], y: [0, 1], title: "Reliability (gold) against share varying between people" });
        var xs = [], ys = [], s;
        for (s = 0.05; s <= 0.951; s += 0.05) { xs.push(s); ys.push(rel(s, v.trials)); }
        a.line(xs, ys, { color: "#f2c14e", width: 2 });
        a.line([0, 1], [0.8, 0.8], { color: "#5bd18b", width: 1 });
        var r = rel(v.share, v.trials);
        a.text(v.share, Math.min(r + 0.08, 0.95), "reliability " + r.toFixed(2) + ", group d " + groupD(v.share, v.trials).toFixed(1), { align: "center", size: 10 });
      },
      readout: function (v) { return [["reliability", rel(v.share, v.trials).toFixed(2)], ["group effect d", groupD(v.share, v.trials).toFixed(2)]]; },
      note: "Nothing you choose is stored or sent. The task is Part 59's: an effect budget of 60 ms split between a common mean and differences between people, with trial noise of 120 ms. Only more trials buy both a group effect and a reliable measure.",
    });
  };
  // ---- Part 60: human or machine, then how much to rely on an aid. ----
  W.humanormachine = function (el) {
    var w = null;
    var ITEMS = [
      ["Everyone knows what attention is. It is the taking possession by the mind, in clear and vivid form, of one out of what seem several simultaneously possible objects or trains of thought.", 0],
      ["Habit is the groove that a repeated act wears into the nervous system, so that what once cost effort comes at last to cost nothing at all.", 1],
      ["The baby, assailed by eyes, ears, nose, skin, and entrails at once, feels it all as one great blooming, buzzing confusion.", 0],
      ["Memory is not a storehouse but a performance; each time we recall, we rebuild, and the building is never quite the same.", 1],
      ["It is nothing jointed; it flows. A 'river' or a 'stream' are the metaphors by which it is most naturally described.", 0],
      ["We do not first see and then judge; the judging is already in the seeing, and the eye arrives at its object with an opinion.", 1],
    ];
    var S = { phase: "idle", k: 0, answers: [] };
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return S.phase === "run"; },
      respond: function (side) {
        S.answers.push(side); S.k++; task.count++;
        if (S.k >= ITEMS.length) S.phase = "done";
        if (w) w.render();
      },
    });
    function score() { var c = 0, i; for (i = 0; i < S.answers.length; i++) if (S.answers[i] === ITEMS[i][1]) c++; return c; }
    w = QB.widget(el, {
      title: "Human or machine?",
      sub: "Six sentences about the mind. Three are William James's (1890); three were written for Part 60 by a language model in his manner. For each, press F for James or J for the machine (or tap the left or right half). Then, on the right, choose how often to follow an aid that is right 80% of the time when you are right 70%.",
      panels: 2, height: 330,
      controls: [
        { k: "rely", label: "share of decisions where you follow the aid", min: 0, max: 1, step: 0.05, value: 0.5, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "aid", label: "the aid's accuracy", min: 0.5, max: 0.95, step: 0.05, value: 0.8, fmt: function (x) { return Math.round(100 * x) + "%"; } },
      ],
      buttons: [
        { label: "Start", act: function () { S.phase = "run"; S.k = 0; S.answers = []; task.count = 0; } },
        { label: "Clear", act: function () { S.phase = "idle"; S.k = 0; S.answers = []; } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (S.phase === "run") {
          ctx.fillStyle = "#cfd6e2"; ctx.font = "13px sans-serif"; ctx.textAlign = "center";
          ctx.fillText("sentence " + (S.k + 1) + " of " + ITEMS.length + ":   F James   J machine", b.cx, b.y + 22);
          ctx.font = "15px serif"; ctx.fillStyle = "#e8eef6";
          T.wrap(ctx, "\u201c" + ITEMS[S.k][0] + "\u201d", b.cx, b.cy - 30, b.w - 60, 20);
        } else if (S.phase === "done") {
          T.message(ctx, b, "You got " + score() + " of 6.",
            "Sentences 1, 3 and 5 are James's (attention, the baby's blooming, buzzing confusion, the stream of thought); 2, 4 and 6 are the machine's. In larger studies people do little better than chance with short texts: we judge minds by their surface.");
        } else {
          T.message(ctx, b, "On you", "Press Start to judge six sentences; the slider on the right works any time.");
        }
        var a = g[1].axes({ x: [0, 1], y: [0.5, 1], title: "Your accuracy (gold) against how often you follow the aid" });
        var acc = function (s) { return s * v.aid + (1 - s) * 0.7; };
        a.line([0, 1], [acc(0), acc(1)], { color: "#f2c14e", width: 2 });
        a.line([0, 1], [Math.max(v.aid, 0.7), Math.max(v.aid, 0.7)], { color: "#5bd18b", width: 1 });
        a.text(v.rely, Math.min(acc(v.rely) + 0.04, 0.97), Math.round(100 * acc(v.rely)) + "%", { align: "center", size: 11 });
      },
      readout: function (v) { return [["your accuracy", Math.round(100 * (v.rely * v.aid + (1 - v.rely) * 0.7)) + "%"], ["best possible", Math.round(100 * Math.max(v.aid, 0.7)) + "%"]]; },
      note: "Nothing you choose is stored or sent. The line is Part 60's: following an aid at random on a share of decisions mixes its accuracy with yours; when the aid is better, the best policy is to follow it every time, and algorithm aversion costs the difference.",
    });
  };
})();
