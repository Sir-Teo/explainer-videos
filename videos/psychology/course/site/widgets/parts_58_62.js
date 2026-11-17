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

  // ---- Part 61: one cell of a design space, then the whole space; and incentives for a research community. ----
  W.designspace = function (el) {
    var w = null;
    var rand = function (seed) { var a = seed >>> 0; return function () { a = (a + 0x6d2b79f5) >>> 0; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
    var r = rand(61), K = 10, mains = [], pairs = [], i, j;
    function gauss() { var u = Math.max(r(), 1e-9), v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
    for (i = 0; i < K; i++) mains.push(0.1 * gauss());
    for (i = 0; i < K; i++) { pairs.push([]); for (j = 0; j < K; j++) pairs[i].push(j > i ? 0.05 * gauss() : 0); }
    function effect(cell) {
      var e = 0.3, a, b;
      for (a = 0; a < K; a++) { var xa = (cell >> a) & 1 ? 1 : -1; e += mains[a] * xa; for (b = a + 1; b < K; b++) e += pairs[a][b] * xa * ((cell >> b) & 1 ? 1 : -1); }
      return e;
    }
    var all = []; for (i = 0; i < (1 << K); i++) all.push(effect(i));
    var S = { phase: "idle", cell: 0, k: 0 };
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return S.phase === "pick"; },
      respond: function (side) { S.cell |= side << S.k; S.k++; task.count++; if (S.k >= K) S.phase = "shown"; if (w) w.render(); },
    });
    var NAMES = ["text (F) or call (J)", "one reminder (F) or three (J)", "named sender (F) or not (J)", "deadline (F) or none (J)", "gain (F) or loss (J) framing", "morning (F) or evening (J)", "short (F) or long (J)", "online (F) or in person (J)", "students (F) or adults (J)", "country A (F) or B (J)"];
    function fdr(base, power, alpha) { var tp = base * power, fp = (1 - base) * alpha; return fp / (tp + fp); }
    w = QB.widget(el, {
      title: "One experiment, or the space of them?",
      sub: "You are testing whether a reminder raises attendance. Make ten design choices with F and J (or tap left and right); that picks one of 1,024 experiments, as a single study does. Then see the true effect in your cell against all of them. On the right: the share of published positive results that are false, for a field's base rate of true hypotheses, its power and its false-positive rate.",
      panels: 2, height: 330,
      controls: [
        { k: "base", label: "share of tested hypotheses that are true", min: 0.05, max: 0.5, step: 0.05, value: 0.1, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "power", label: "power", min: 0.2, max: 0.95, step: 0.05, value: 0.8, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [
        { label: "Start", act: function () { S.phase = "pick"; S.cell = 0; S.k = 0; task.count = 0; } },
        { label: "Clear", act: function () { S.phase = "idle"; S.cell = 0; S.k = 0; } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (S.phase === "pick") {
          T.message(ctx, b, "Choice " + (S.k + 1) + " of 10", NAMES[S.k]);
        } else if (S.phase === "shown") {
          var e = all[S.cell], below = 0; for (i = 0; i < all.length; i++) if (all[i] < e) below++;
          T.message(ctx, b, "Your experiment's true effect: " + e.toFixed(2) + " SD",
            "That is above " + Math.round(100 * below / all.length) + "% of the 1,024 possible experiments. Across the space the effect runs from " + Math.min.apply(null, all).toFixed(2) + " to " + Math.max.apply(null, all).toFixed(2) + ", and about a quarter of cells go the other way. A single study reports one cell; an integrative design maps them all.");
        } else {
          T.message(ctx, b, "On you", "Press Start, then make ten design choices.");
        }
        var a = g[1].axes({ x: [0, 0.2], y: [0, 1], title: "False share of positives (gold) against the false-positive rate" });
        var xs = [], ys = [], al;
        for (al = 0.005; al <= 0.2; al += 0.005) { xs.push(al); ys.push(fdr(v.base, v.power, al)); }
        a.line(xs, ys, { color: "#f2c14e", width: 2 });
        var f5 = fdr(v.base, v.power, 0.05);
        a.text(0.05, Math.min(f5 + 0.08, 0.95), "at 0.05: " + Math.round(100 * f5) + "%", { align: "center", size: 11 });
      },
      readout: function (v) { return [["false share at 0.05", Math.round(100 * fdr(v.base, v.power, 0.05)) + "%"]]; },
      note: "Nothing you choose is stored or sent. The space is Part 61's: ten binary choices with main effects and pairwise interactions, drawn once. The right panel is the arithmetic behind Smaldino and McElreath's model: when few tested hypotheses are true, even honest labs publish many false positives.",
    });
  };

  // ---- Part 62: the last experiment: mental rotation on you, your slope, and its split-half reliability. ----
  W.lastrotation = function (el) {
    var w = null, ANG = [0, 60, 120, 180], N = 32;
    var S = { phase: "idle", k: 0, trials: [], t0: 0, res: [] };
    function plan(seed) {
      var r = (function (a) { return function () { a = (a + 0x6d2b79f5) >>> 0; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; })(seed >>> 0);
      var out = [], i;
      for (i = 0; i < N; i++) out.push({ angle: ANG[i % 4], mirror: (Math.floor(i / 4) % 2) === 1 });
      for (i = out.length - 1; i > 0; i--) { var j = Math.floor(r() * (i + 1)), tmp = out[i]; out[i] = out[j]; out[j] = tmp; }
      return out;
    }
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return S.phase === "run"; },
      respond: function (side) {
        var tr = S.trials[S.k];
        S.res.push({ angle: tr.angle, rt: T.now() - S.t0, correct: (side === 1) === tr.mirror, odd: S.k % 2 === 0 });
        S.k++; task.count++;
        if (S.k >= N) { S.phase = "done"; } else { S.t0 = T.now(); }
        if (w) w.render();
      },
    });
    function slope(rows) {
      var n = rows.length, mx = 0, my = 0, i, sxx = 0, sxy = 0;
      if (n < 3) return NaN;
      for (i = 0; i < n; i++) { mx += rows[i].angle; my += rows[i].rt; }
      mx /= n; my /= n;
      for (i = 0; i < n; i++) { sxx += (rows[i].angle - mx) * (rows[i].angle - mx); sxy += (rows[i].angle - mx) * (rows[i].rt - my); }
      return sxx > 0 ? sxy / sxx : NaN;
    }
    function drawR(ctx, x, y, angle, mirror, size) {
      ctx.save(); ctx.translate(x, y); ctx.rotate(angle * Math.PI / 180); if (mirror) ctx.scale(-1, 1);
      ctx.fillStyle = "#e8eef6"; ctx.font = "bold " + size + "px serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.fillText("R", 0, 0); ctx.restore();
    }
    w = QB.widget(el, {
      title: "The last experiment",
      sub: "Press Start. Each trial shows an R on the left and, on the right, the same R turned (press F) or its mirror image turned (press J), or tap the left or right half. Thirty-two trials; answer as fast as you can without errors. Then see your time against the angle, your slope, and how well your odd and even trials agree.",
      panels: 2, height: 330,
      buttons: [
        { label: "Start", act: function (state) { S.trials = plan(62 + (state ? state.seed : 0)); S.k = 0; S.res = []; task.count = 0; S.phase = "run"; S.t0 = T.now(); } },
        { label: "Clear", act: function (state) { if (state) state.seed++; S.phase = "idle"; S.k = 0; S.res = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (S.phase === "run") {
          var tr = S.trials[S.k];
          ctx.fillStyle = "#cfd6e2"; ctx.font = "13px sans-serif"; ctx.textAlign = "center";
          ctx.fillText("trial " + (S.k + 1) + " of " + N + ":   F same   J mirror", b.cx, b.y + 22);
          drawR(ctx, b.x + b.w * 0.3, b.cy + 10, 0, false, 72);
          drawR(ctx, b.x + b.w * 0.7, b.cy + 10, tr.angle, tr.mirror, 72);
        } else if (S.phase === "done") {
          var all = S.res.filter(function (r) { return r.correct; });
          var so = slope(all.filter(function (r) { return r.odd; })), se = slope(all.filter(function (r) { return !r.odd; }));
          var sl = slope(all);
          T.message(ctx, b, "Your slope: " + (isFinite(sl) ? (sl).toFixed(1) + " ms per degree" : "too few correct trials"),
            "Odd trials: " + (isFinite(so) ? so.toFixed(1) : "?") + "; even trials: " + (isFinite(se) ? se.toFixed(1) : "?") + " ms per degree. With only 16 trials in each half, the two halves of one person often disagree: that is why Part 62 needed 40 people, and found a reliability of 0.74 with an interval from 0.51 to 0.87.");
        } else {
          T.message(ctx, b, "On you", "Press Start for 32 trials of mental rotation.");
        }
        var a = g[1].axes({ x: [-10, 190], y: [0, 3000], title: "Your correct trials: time (ms) against angle (degrees)" });
        var means = [];
        ANG.forEach(function (ang) {
          var rs = S.res.filter(function (r) { return r.correct && r.angle === ang; }).map(function (r) { return r.rt; });
          if (rs.length) { var m = rs.reduce(function (p, q) { return p + q; }, 0) / rs.length; means.push([ang, Math.min(m, 2950)]); }
        });
        if (means.length > 1) a.line(means.map(function (p) { return p[0]; }), means.map(function (p) { return p[1]; }), { color: "#f2c14e", width: 2 });
        means.forEach(function (p) { a.text(p[0], p[1] + 120, Math.round(p[1]) + "", { align: "center", size: 10 }); });
      },
      readout: function () { var all = S.res.filter(function (r) { return r.correct; }); var sl = slope(all); return [["trials done", S.res.length + " of " + N], ["your slope", isFinite(sl) ? sl.toFixed(1) + " ms/deg" : "n/a"]]; },
      note: "Nothing you do is stored or sent. The task is a two-dimensional version of Part 24's; the slope is the least-squares slope of your correct trials' times on the angle, computed in your browser.",
    });
  };
})();
