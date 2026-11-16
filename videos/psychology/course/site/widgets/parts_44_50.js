// Interactives for Act XI, the graduate toolkit (Parts 44-50).  Each is an experiment the reader takes part in,
// built on the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  function gauss(rand) {
    var u = 1 - rand(), v = rand();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }
  function mulberry(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function corr(a, b) {
    var n = a.length, ma = 0, mb = 0, sab = 0, saa = 0, sbb = 0, i;
    for (i = 0; i < n; i++) { ma += a[i]; mb += b[i]; }
    ma /= n; mb /= n;
    for (i = 0; i < n; i++) { sab += (a[i] - ma) * (b[i] - mb); saa += (a[i] - ma) * (a[i] - ma); sbb += (b[i] - mb) * (b[i] - mb); }
    return sab / Math.sqrt(saa * sbb);
  }
  // upper tail of chi-square on 1 df
  function p1(x) {
    var z = Math.sqrt(Math.max(x, 0) / 2), t = 1 / (1 + 0.5 * z);
    var e = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 +
            t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))));
    return Math.min(1, e);
  }

  // ---- Part 44: draw the arrows; which diagrams can the data tell apart? ----
  W.diagrams = function (el) {
    var w = null;
    var N = 500;
    // the four ways to direct the edges X-M and M-Y
    var DIAG = [
      { name: "X → M → Y", a: [1, 1] },
      { name: "X ← M ← Y", a: [-1, -1] },
      { name: "X ← M → Y", a: [-1, 1] },
      { name: "X → M ← Y", a: [1, -1] },
    ];
    var TRUTHS = [0, 2, 3, 1, 3, 0];  // the hidden generating diagram in each of six rounds
    var S = { phase: "idle", k: -1, log: [], fit: null, data: null };

    function simulate(truth, seed) {
      var rand = mulberry(seed), X = [], M = [], Y = [], i, x, m, y;
      for (i = 0; i < N; i++) {
        if (truth === 0) { x = gauss(rand); m = 0.6 * x + 0.8 * gauss(rand); y = 0.6 * m + 0.8 * gauss(rand); }
        else if (truth === 1) { y = gauss(rand); m = 0.6 * y + 0.8 * gauss(rand); x = 0.6 * m + 0.8 * gauss(rand); }
        else if (truth === 2) { m = gauss(rand); x = 0.6 * m + 0.8 * gauss(rand); y = 0.6 * m + 0.8 * gauss(rand); }
        else { x = gauss(rand); y = gauss(rand); m = 0.5 * x + 0.5 * y + 0.7 * gauss(rand); }
        X.push(x); M.push(m); Y.push(y);
      }
      var rxm = corr(X, M), rmy = corr(M, Y), rxy = corr(X, Y);
      var part = (rxy - rxm * rmy) / Math.sqrt((1 - rxm * rxm) * (1 - rmy * rmy));
      var chain = -N * Math.log(1 - part * part), coll = -N * Math.log(1 - rxy * rxy);
      return { rxm: rxm, rmy: rmy, rxy: rxy, chi: [chain, chain, chain, coll] };
    }
    function next() {
      S.k++;
      if (S.k >= TRUTHS.length) { S.phase = "done"; task.clear(); }
      else { S.phase = "ask"; S.data = simulate(TRUTHS[S.k], 4400 + 97 * S.k + (w ? w.state.seed : 0)); }
      if (w) w.render();
    }
    var task = T.create(el, {
      keys: { "1": 0, "2": 1, "3": 2, "4": 3 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side, how) {
        var choice = how === "tap" ? (side === 0 ? 0 : 3) : side;
        var d = S.data, best = Math.min.apply(null, d.chi), tied = [];
        for (var j = 0; j < 4; j++) if (d.chi[j] - best < 1e-9) tied.push(j);
        S.log.push({ k: S.k, choice: choice, truth: TRUTHS[S.k], tied: tied, fitsBest: tied.indexOf(choice) >= 0 });
        task.count++;
        S.phase = "shown";
        if (w) w.render();
        task.later(next, 4200);
      },
    });
    function start() { task.clear(); S.k = -1; S.log = []; task.count = 0; next(); }

    function drawDiag(ctx, cx, cy, a, col, sc) {
      var xs = [cx - 70 * sc, cx, cx + 70 * sc], names = ["X", "M", "Y"], i;
      ctx.save();
      ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = 2;
      for (i = 0; i < 2; i++) {
        var from = a[i] > 0 ? xs[i] : xs[i + 1], to = a[i] > 0 ? xs[i + 1] : xs[i], dir = to > from ? 1 : -1;
        var x0 = from + dir * 14 * sc, x1 = to - dir * 14 * sc;
        ctx.beginPath(); ctx.moveTo(x0, cy); ctx.lineTo(x1, cy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x1, cy); ctx.lineTo(x1 - dir * 8, cy - 5); ctx.lineTo(x1 - dir * 8, cy + 5);
        ctx.closePath(); ctx.fill();
      }
      ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.font = "600 " + Math.round(14 * sc) + "px system-ui, sans-serif";
      for (i = 0; i < 3; i++) {
        ctx.strokeRect(xs[i] - 12 * sc, cy - 12 * sc, 24 * sc, 24 * sc);
        ctx.fillText(names[i], xs[i], cy);
      }
      ctx.restore();
    }

    w = QB.widget(el, {
      title: "Draw the arrows",
      sub: "Each round, 500 people are simulated from a hidden diagram on X, M and Y. Look at the correlations and pick the diagram you think made them: press 1 to 4 (or tap left for the first, right for the last). Then see how well each diagram fits.",
      panels: 2, height: 380, weights: [1.4, 1],
      buttons: [
        { label: "Start", act: function () { start(); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), j;
        ctx.save(); ctx.textAlign = "center";
        if (S.phase === "ask" || S.phase === "shown") {
          var d = S.data, last = S.log[S.log.length - 1];
          ctx.fillStyle = C.muted; ctx.font = "13px system-ui, sans-serif";
          ctx.fillText("Round " + (S.k + 1) + " of " + TRUTHS.length + ":  r(X,M) = " + d.rxm.toFixed(2) + "   r(M,Y) = " +
                       d.rmy.toFixed(2) + "   r(X,Y) = " + d.rxy.toFixed(2), b.cx, b.y + 26);
          var rowH = (b.h - 70) / 4;
          for (j = 0; j < 4; j++) {
            var y = b.y + 52 + rowH * (j + 0.5), col = C.ink;
            if (S.phase === "shown") col = d.chi[j] - Math.min.apply(null, d.chi) < 1e-9 ? "#5bd18b" : "#ef6f6c";
            ctx.fillStyle = C.muted; ctx.font = "600 14px system-ui, sans-serif"; ctx.textAlign = "left";
            ctx.fillText(String(j + 1), b.x + 22, y + 5);
            drawDiag(ctx, b.x + b.w * 0.36, y, DIAG[j].a, col, 1);
            ctx.textAlign = "left"; ctx.font = "12.5px system-ui, sans-serif";
            if (S.phase === "shown") {
              ctx.fillStyle = col;
              var p = p1(d.chi[j]);
              ctx.fillText("χ² = " + d.chi[j].toFixed(1) + " on 1 df, p " + (p < 0.001 ? "< 0.001" : "= " + p.toFixed(2)) +
                           (j === last.truth ? "   (the hidden diagram)" : "") + (j === last.choice ? "   your pick" : ""),
                           b.x + b.w * 0.6, y + 4);
            }
          }
          ctx.textAlign = "center";
        } else if (S.phase === "done") {
          T.message(ctx, b, "Six rounds.",
                    "The three diagrams without a collider always fit identically: the data cannot say which made them. Only a collider leaves a mark of its own, because it makes X and Y uncorrelated.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Six rounds, each from a hidden diagram.");
        }
        ctx.restore();
        var c2 = g[1].box, cx = g.ctx;
        cx.save(); cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("Each round: the hidden diagram, and how many fit best", c2.x + 10, c2.y + 18);
        var bh = (c2.h - 50) / TRUTHS.length;
        for (j = 0; j < S.log.length; j++) {
          var r = S.log[j], yy = c2.y + 34 + j * bh;
          cx.fillStyle = r.tied.length === 1 ? "#5bd18b" : "#f2c14e";
          cx.fillText((r.k + 1) + ".  " + DIAG[r.truth].name + "   " + (r.tied.length === 1 ? "only it fits best" :
                      r.tied.length + " diagrams tie"), c2.x + 14, yy + bh / 2);
        }
        cx.restore();
      },
      readout: function () {
        var only = S.log.filter(function (r) { return r.tied.length === 1; }).length;
        return [["rounds", String(task.count)], ["identified by the data", S.log.length ? only + " / " + S.log.length : "-"]];
      },
      note: "Nothing you answer is stored or sent. The data are simulated in your browser; the same reasoning holds for any sample size.",
    });
  };
})();
