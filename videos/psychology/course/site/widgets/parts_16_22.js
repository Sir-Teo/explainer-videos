// Interactives for Act IV, Learning and Memory (Parts 16-22).  Each is an experiment the reader takes part in, built on
// the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 16: the gardener's game.  Predict each plant; your predictions reveal the contingency you learned ------
  W.contingency = function (el) {
    var w = null, PER = 20, LATE = 10, YOU = "#f2c14e", OK = "#5bd18b", CS = "#7ec8f5", BAD = "#ef6f6c", US = "#f2a65a";
    // four blocks: P(bloom | fertilizer), P(bloom | none)
    var BLOCKS = [[0.75, 0.75], [0.75, 0.25], [0.25, 0.25], [0.25, 0.75]];
    var S = { phase: "idle", seed: 0, block: 0, trial: 0, order: [], plan: [], cur: null, said: null, res: [] };
    function deck(u, p1, p0) {
      // exactly PER trials: half fertilized; within each half the share that bloom is fixed, so each block's
      // contingency is exact; the order is shuffled
      var half = PER / 2, out = [], i, j, t, k1 = Math.round(p1 * half), k0 = Math.round(p0 * half);
      for (i = 0; i < half; i++) out.push({ f: true, bloom: i < k1 });
      for (i = 0; i < half; i++) out.push({ f: false, bloom: i < k0 });
      for (i = out.length - 1; i > 0; i--) { j = Math.floor(u() * (i + 1)); t = out[i]; out[i] = out[j]; out[j] = t; }
      return out;
    }
    function start() {
      task.clear(); S.seed++; S.block = 0; S.res = []; S.said = null;
      var u = QB.rng(104729 * S.seed + 17), order = [0, 1, 2, 3], i, j, t;
      for (i = 3; i > 0; i--) { j = Math.floor(u() * (i + 1)); t = order[i]; order[i] = order[j]; order[j] = t; }
      S.order = order; begin();
    }
    function begin() {
      var b = BLOCKS[S.order[S.block]], u = QB.rng(7919 * S.seed + 131 * S.block + 3);
      S.plan = deck(u, b[0], b[1]); S.trial = 0; S.res.push([]);
      S.phase = "intro"; w.render();
      task.later(next, 1600);
    }
    function next() {
      S.cur = S.plan[S.trial]; S.trial++; S.said = null;
      S.phase = "show"; w.render();
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "show"; }, respond: answer });
    function answer(side) {  // 0: will not bloom, 1: will bloom
      if (S.phase !== "show" || !w) return;
      task.count++;
      S.said = side === 1;
      S.res[S.block].push({ f: S.cur.f, bloom: S.cur.bloom, said: S.said });
      S.phase = "feedback"; w.render();
      task.later(function () {
        if (S.trial < PER) { next(); return; }
        S.block++;
        if (S.block >= BLOCKS.length) { S.phase = "done"; w.render(); } else begin();
      }, 700);
    }
    // your contingency in a block: P(you predict bloom | fertilizer) - P(you predict bloom | none), late trials only
    function yours(k) {
      var r = S.res[k];
      if (!r || r.length < PER) return NaN;
      var late = r.slice(PER - LATE), a = 0, na = 0, b = 0, nb = 0;
      late.forEach(function (x) { if (x.f) { na++; if (x.said) a++; } else { nb++; if (x.said) b++; } });
      if (!na || !nb) return NaN;
      return a / na - b / nb;
    }
    function bloomRate(k) {
      var r = S.res[k]; if (!r || r.length < PER) return NaN;
      var late = r.slice(PER - LATE), n = 0;
      late.forEach(function (x) { if (x.said) n++; });
      return n / late.length;
    }
    function plant(c, x, y, s, fert, bloom, show) {
      c.save();
      c.fillStyle = "#3a2a20"; c.strokeStyle = "#9aa3ad"; c.lineWidth = 1.5;
      c.beginPath(); c.moveTo(x - 0.3 * s, y + 0.5 * s); c.lineTo(x + 0.3 * s, y + 0.5 * s);
      c.lineTo(x + 0.38 * s, y + 0.1 * s); c.lineTo(x - 0.38 * s, y + 0.1 * s); c.closePath(); c.fill(); c.stroke();
      c.strokeStyle = OK; c.lineWidth = 4;
      c.beginPath(); c.moveTo(x, y + 0.1 * s); c.lineTo(x, y - 0.45 * s); c.stroke();
      if (show) {
        if (bloom) {
          c.fillStyle = US;
          for (var i = 0; i < 5; i++) {
            var a = i * 2 * Math.PI / 5;
            c.beginPath(); c.arc(x + 0.16 * s * Math.cos(a), y - 0.55 * s + 0.16 * s * Math.sin(a), 0.13 * s, 0, 2 * Math.PI); c.fill();
          }
          c.fillStyle = YOU; c.beginPath(); c.arc(x, y - 0.55 * s, 0.08 * s, 0, 2 * Math.PI); c.fill();
        } else {
          c.strokeStyle = "#7c858f"; c.lineWidth = 4;
          c.beginPath(); c.moveTo(x, y - 0.45 * s); c.lineTo(x + 0.18 * s, y - 0.35 * s); c.stroke();
        }
      }
      if (fert) {
        c.fillStyle = CS; c.fillRect(x - 0.72 * s, y - 0.05 * s, 0.32 * s, 0.4 * s);
        c.fillStyle = "#05070b"; c.font = "600 " + Math.round(0.2 * s) + "px system-ui, sans-serif";
        c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("F", x - 0.56 * s, y + 0.15 * s);
      }
      c.restore();
    }

    w = QB.widget(el, {
      title: "The gardener's game: does the fertilizer work?",
      sub: "Four batches of twenty plants. Some get fertilizer (a blue F bag), some do not. Before each plant is revealed, predict whether it will bloom: F, or tap the left half, for no; J, or tap the right half, for yes. In some batches the fertilizer helps, in some it harms, and in some it does nothing while most plants bloom anyway. Your predictions in the last ten plants of each batch show the contingency you learned.",
      panels: 2, height: 320, weights: [1.1, 1],
      controls: [],
      buttons: [
        { label: "Start", act: start },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.block = 0; S.trial = 0; S.res = []; S.cur = null; } },
      ],
      draw: function (g) {
        var c = g.ctx, b = T.stage(g, 0, task);
        c.save(); c.textAlign = "center"; c.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(c, b, "On you", "Press Start. Eighty plants in four batches, about three minutes. Predict each one, then see it.");
        } else if (S.phase === "intro") {
          T.message(c, b, "Batch " + (S.block + 1) + " of 4", "A new fertilizer, a new set of plants.");
        } else if (S.phase === "done") {
          T.message(c, b, "Finished.", "On the right: your learned contingency in each batch (late predictions) against the true one. The two batches where the fertilizer did nothing differ only in how often plants bloomed. If your point for the blooming batch sits above zero, you showed the outcome-density effect of chapter four.");
        } else {
          var s = Math.min(b.h * 0.42, 90);
          plant(c, b.cx, b.cy + 0.05 * s, s, S.cur.f, S.cur.bloom, S.phase === "feedback");
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("batch " + (S.block + 1) + " of 4, plant " + S.trial + " of " + PER, b.cx, b.y + 16);
          c.font = "600 18px system-ui, sans-serif";
          if (S.phase === "feedback") {
            var right = S.said === S.cur.bloom;
            c.fillStyle = S.cur.bloom ? US : C.muted;
            c.fillText(S.cur.bloom ? "Bloomed" : "Did not bloom", b.cx, b.y + 40);
            c.font = "12.5px system-ui, sans-serif"; c.fillStyle = right ? OK : BAD;
            c.fillText(right ? "as you predicted" : "not as you predicted", b.cx, b.y + b.h - 16);
          } else {
            c.fillStyle = C.ink; c.fillText("Will it bloom?", b.cx, b.y + 40);
            c.font = "12.5px system-ui, sans-serif"; c.fillStyle = C.muted;
            c.fillText(b.w < 420 ? "F / no        J / yes" : "F, or tap the left half: no        J, or tap the right half: yes", b.cx, b.y + b.h - 16);
          }
        }
        c.restore();

        var a = g[1].axes({ x: [-0.75, 0.75], y: [-1, 1], xticks: [-0.5, 0, 0.5], yticks: [-1, -0.5, 0, 0.5, 1],
          title: "Your contingency against the true one", xlabel: "true ΔP", ylabel: "yours" });
        a.line([-0.75, 0.75], [-0.75, 0.75], { color: C.muted, width: 1 });
        a.line([-0.75, 0.75], [0, 0], { color: C.muted, width: 0.5 });
        for (var k = 0; k < S.res.length; k++) {
          var v = yours(k), blk = BLOCKS[S.order[k]];
          if (isNaN(v)) continue;
          var dp = (Math.round(blk[0] * PER / 2) - Math.round(blk[1] * PER / 2)) / (PER / 2), col = dp !== 0 ? OK : (blk[0] > 0.5 ? US : CS);
          var x = dp + (dp === 0 ? (blk[0] > 0.5 ? 0.06 : -0.06) : 0);
          a.dots([x], [v], { color: col, r: 6 });
        }
      },
      readout: function () {
        var f = function (v) { return isNaN(v) ? "–" : (v >= 0 ? "+" : "") + v.toFixed(2); }, rows = [["plants", String(S.res.reduce(function (n, r) { return n + r.length; }, 0))]];
        for (var k = 0; k < S.res.length; k++) {
          var blk = BLOCKS[S.order[k]];
          if (S.res[k].length < PER) { rows.push(["batch " + (k + 1), "in progress"]); continue; }
          rows.push(["batch " + (k + 1) + " (true ΔP " + (blk[0] >= blk[1] ? "+" : "") + ((Math.round(blk[0] * PER / 2) - Math.round(blk[1] * PER / 2)) / (PER / 2)).toFixed(2) + ", bloom " + Math.round(100 * (Math.round(blk[0] * PER / 2) + Math.round(blk[1] * PER / 2)) / PER) + "%)", f(yours(k))]);
        }
        return rows;
      },
      note: "Nothing you answer is stored or sent. Each batch has exactly ten fertilized and ten unfertilized plants, and the number of each that bloom is fixed (eight of ten, or three of ten), so the true contingency ΔP = P(bloom | fertilizer) − P(bloom | none) is exact; only the order is random. Your learned contingency is the same difference computed from your predictions in the last ten plants of the batch, after you have had time to learn. Rescorla and Wagner's rule, with the garden as a cue present on every trial, predicts that this difference settles at the true ΔP, and that early on, when blooms are common, it runs high: the outcome-density effect.",
    });
  };
})();
