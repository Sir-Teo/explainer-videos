// Interactives for the end of Act VI and Act VII, Value (Parts 31-36).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 31: a global workspace that ignites, and its masking curve ---------------------------------------
  W.maskignite = function (el) {
    var run = function (I, soa, r, noise, rnd) { // activity every 2 ms for 450 ms; the mask cuts the input at soa
      var w = 0, out = [], k, t, z;
      for (k = 0; k < 225; k++) {
        t = 2 * k;
        z = 0.08 * ((t < soa ? I : 0) + r * w - 55);
        w += 2 / 50 * (100 / (1 + Math.exp(-z)) - w);
        if (noise > 0) w = Math.max(0, w + noise * rnd.normal() * Math.SQRT2);
        out.push(w);
      }
      return out;
    };
    QB.widget(el, {
      title: "Ignition: a workspace, a stimulus and a mask",
      sub: "The workspace's activity w follows the film's one equation. A stimulus drives it until the mask arrives. Slide the mask's delay across the threshold and the activity either fades or takes over and holds; the right panel counts, over noisy trials, how often it holds. Then lower the recurrence: without the loop nothing ignites at any delay.",
      panels: 2, height: 300,
      controls: [
        { k: "soa", label: "Delay before the mask (ms)", min: 10, max: 120, step: 2, value: 44, fmt: function (x) { return x + " ms"; } },
        { k: "I", label: "Stimulus strength I", min: 10, max: 60, step: 1, value: 30 },
        { k: "r", label: "Recurrent excitation r", min: 0.6, max: 2, step: 0.02, value: 1.6, fmt: function (x) { return x.toFixed(2); } },
        { k: "noise", label: "Noise", min: 0, max: 1.5, step: 0.05, value: 0.6, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New trials", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var rnd = QB.rng(s.seed + 31), ts = [], k, j, clean = run(v.I, v.soa, v.r, 0, rnd);
        for (k = 0; k < 225; k++) ts.push(2 * k);
        var a = g[0].axes({ x: [0, 450], y: [0, 150], yticks: [0, 50, 100], title: "Activity after the stimulus", xlabel: "time since the stimulus (ms)" });
        a.area([0, v.soa], [150, 150], 0, { color: C.idea, alpha: 0.1 });
        a.hline(50, { color: C.muted });
        for (j = 0; j < 6; j++) { var tr = run(v.I, v.soa, v.r, v.noise, rnd); a.line(ts, tr, { color: tr[200] > 50 ? C.gain : C.loss, width: 1, alpha: 0.55 }); }
        a.line(ts, clean, { color: C.ink, width: 2 });
        a.vline(v.soa, { color: C.idea });
        a.legend([["without noise", C.ink], ["a trial that ignites", C.gain], ["a trial that fades", C.loss], ["stimulus on, until the mask", C.idea]], { pos: "tr" });
        var ds = [], seen = [], n = 24, here = 0, half = null;
        for (k = 10; k <= 120; k += 10) {
          var c = 0;
          for (j = 0; j < n; j++) if (run(v.I, k, v.r, v.noise, rnd)[200] > 50) c++;
          ds.push(k); seen.push(c / n);
          if (half === null && c / n >= 0.5) half = k;
        }
        for (j = 0; j < 60; j++) if (run(v.I, v.soa, v.r, v.noise, rnd)[200] > 50) here++;
        s.out = [here / 60, Math.max.apply(null, clean), clean[200] > 50, half];
        var b = g[1].axes({ x: [0, 130], y: [0, 1], title: "Masking curve: share of trials seen", xlabel: "delay before the mask (ms)", yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.line(ds, seen, { color: C.spot, width: 2 }).dots(ds, seen, { color: C.spot, r: 3 });
        b.vline(v.soa, { color: C.idea });
        b.dots([v.soa], [here / 60], { color: C.idea, r: 5 });
      },
      readout: function (v, s) {
        return [["seen at this delay", QB.pct(s.out[0], 0)], ["without noise", s.out[2] ? "ignites" : "fades"], ["peak activity without noise", fmt(s.out[1], 0)],
          ["first delay seen half the time", s.out[3] === null ? "none up to 120 ms" : s.out[3] + " ms"]];
      },
      note: "Simulated trials of τ dw/dt = −w + 100 σ(g (I + r w − θ)) with τ = 50 ms, g = 0.08, θ = 55, as in the film; a trial counts as seen when w is above 50 at 400 ms. The gold band is the time the stimulus is on. A toy of the global workspace theory, not a model of any brain.",
    });
  };

  // ---- Part 32: a readiness potential built from noise -------------------------------------------------------
  W.noisereadiness = function (el) {
    QB.widget(el, {
      title: "Libet's ramp, from a leaky accumulator and noise",
      sub: "Sixty runs of the film's accumulator: x drifts up, leaks back, and is jostled by noise; a movement happens when x first reaches the threshold. Left: a few runs. Right: all runs averaged backward from their crossings. Lower the noise until nothing crosses, then raise the drift until the resting level I/k passes the threshold and the ramp no longer needs noise at all.",
      panels: 2, height: 300,
      controls: [
        { k: "I", label: "Drift I", min: 0, max: 0.3, step: 0.005, value: 0.1, fmt: function (x) { return x.toFixed(3); } },
        { k: "k", label: "Leak k", min: 0.1, max: 1.5, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "c", label: "Noise c", min: 0, max: 0.25, step: 0.005, value: 0.1, fmt: function (x) { return x.toFixed(3); } },
        { k: "th", label: "Threshold", min: 0.1, max: 0.5, step: 0.002, value: 0.298, fmt: function (x) { return x.toFixed(3); } },
      ],
      buttons: [{ label: "New runs", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var rnd = QB.rng(s.seed + 32), dt = 0.01, n = 2000, win = 200, runs = 60, rest = v.I / v.k, sd = v.c * Math.sqrt(dt);
        var sum = [], cnt = 0, crossed = 0, wait = 0, shown = [], i, j, t;
        for (i = 0; i <= win; i++) sum.push(0);
        for (j = 0; j < runs; j++) {
          var x = 0, hist = [0], at = -1;
          for (i = 1; i <= n; i++) {
            x += (v.I - v.k * x) * dt + sd * rnd.normal();
            hist.push(x);
            if (x >= v.th) { at = i; break; }
          }
          if (shown.length < 5) shown.push([hist, at]);
          if (at < 0) continue;
          crossed++; wait += at * dt;
          if (at >= win) { cnt++; for (i = 0; i <= win; i++) sum[i] += hist[at - win + i]; }
        }
        var ymax = Math.max(0.36, 1.25 * v.th), ymin = -0.12;
        var a = g[0].axes({ x: [0, 20], y: [ymin, ymax], title: "Five runs, each until it crosses", xlabel: "time (s)" });
        var cols = [C.spot, C.q, C.realized, C.implied, C.option];
        for (j = 0; j < shown.length; j++) {
          var hs = shown[j][0], xs = [], ys = [];
          for (i = 0; i < hs.length; i += 4) { xs.push(i * dt); ys.push(hs[i]); }
          a.line(xs, ys, { color: cols[j], width: 1, alpha: 0.85 });
          if (shown[j][1] > 0) a.dots([shown[j][1] * dt], [v.th], { color: cols[j], r: 3.5 });
        }
        a.hline(v.th, { color: C.loss }).hline(rest, { color: C.idea });
        a.text(20, v.th, "threshold", { color: C.loss, align: "right", dx: -6, dy: -9, bg: true });
        a.text(20, rest, "resting level I/k", { color: C.idea, align: "right", dx: -6, dy: 10, bg: true });
        var b = g[1].axes({ x: [-2, 0], y: [ymin, ymax], title: "Averaged backward from the crossing", xlabel: "time before the movement (s)" });
        b.hline(v.th, { color: C.loss }).hline(rest, { color: C.idea });
        b.text(-2, v.th, "threshold", { color: C.loss, dx: 6, dy: -9, bg: true });
        b.text(-2, rest, "resting level I/k", { color: C.idea, dx: 6, dy: 10, bg: true });
        var start = 0, half = 0;
        if (cnt > 0) {
          var bt = [], bm = [];
          for (i = 0; i <= win; i++) { bt.push((i - win) * dt); bm.push(sum[i] / cnt); }
          b.line(bt, bm, { color: C.gain, width: 2.2 });
          start = bm[0];
          for (i = 0; i <= win; i++) if (bm[i] - bm[0] > 0.5 * (bm[win] - bm[0])) { half = -bt[i]; break; }
        } else {
          b.text(-1, (ymin + ymax) / 2, crossed ? "No run lasted 2 s before crossing" : "No run crossed in 20 s", { align: "center", color: C.muted });
        }
        s.out = [crossed, runs, crossed ? wait / crossed : 0, cnt, start, half, rest];
      },
      readout: function (v, s) {
        var o = s.out;
        return [["runs that cross within 20 s", o[0] + " of " + o[1]], ["mean wait", o[0] ? fmt(o[2], 1) + " s" : "none crossed"],
          ["resting level I/k", fmt(o[6], 3) + (o[6] < v.th ? " (below the threshold)" : " (at or above it)")],
          ["average 2 s before", o[3] ? fmt(o[4], 3) : "no runs to average"], ["half of the rise in the last", o[3] ? fmt(o[5], 2) + " s" : "no runs to average"]];
      },
      note: "Simulated data, in steps of 10 ms, with Schurger, Sitt and Dehaene's kind of parameters as the starting values (drift 0.1, leak 0.5, noise 0.1, threshold 0.298). Only runs that last at least 2 s before crossing enter the average. The model contains no decision: the green ramp is what selecting on a threshold crossing does to noise.",
    });
  };

  // ---- Part 33: the Kelly criterion ---------------------------------------------------------------------------
  W.kellyfortunes = function (el) {
    var grow = function (p, f) { return p * Math.log(1 + f) + (1 - p) * Math.log(1 - f); };
    QB.widget(el, {
      title: "Kelly's fraction: forty fortunes on one coin",
      sub: "Each bettor stakes the same fraction f of her wealth, at even odds, on a coin that wins with probability p. Left: the growth rate g(f) of a typical fortune. Right: forty simulated fortunes on a log scale. Every bet has positive expectation when p is above a half, yet slide f past the peak and then past the point where g crosses zero, and the typical bettor is ruined.",
      panels: 2, height: 300,
      controls: [
        { k: "p", label: "Chance the coin wins, p", min: 0.5, max: 0.9, step: 0.01, value: 0.6, fmt: function (x) { return x.toFixed(2); } },
        { k: "f", label: "Fraction of wealth staked, f", min: 0, max: 0.95, step: 0.01, value: 0.2, fmt: function (x) { return x.toFixed(2); } },
        { k: "n", label: "Bets", min: 100, max: 1000, step: 50, value: 500 },
      ],
      buttons: [{ label: "New coin tosses", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var rnd = QB.rng(s.seed + 33), p = v.p, f = v.f, n = v.n, L10 = Math.LN10, fstar = 2 * p - 1, i, j;
        var fs = [], gs = [], zero = 0;
        for (i = 0; i <= 95; i++) { fs.push(i / 100); gs.push(100 * grow(p, i / 100)); if (i > 0 && gs[i] > 0) zero = i / 100; }
        var gtop = Math.max(0.5, 100 * grow(p, fstar) * 1.25), gbot = -2 * gtop;
        var a = g[0].axes({ x: [0, 0.95], y: [gbot, gtop], title: "Growth rate of a typical fortune", xlabel: "fraction staked, f", yfmt: function (y) { return fmt(y, Math.abs(y) < 10 && gtop < 5 ? 1 : 0) + "%"; } });
        a.hline(0, { color: C.muted });
        a.line(fs, gs, { color: C.spot, width: 2 });
        a.vline(fstar, { color: C.gain });
        a.vline(f, { color: C.idea, dash: [], width: 1.5 });
        a.dots([f], [Math.max(gbot, 100 * grow(p, f))], { color: C.idea, r: 5 });
        a.legend([["g(f), % per bet", C.spot], ["Kelly: f* = 2p − 1", C.gain], ["your f", C.idea]], { pos: "bl" });
        var up = Math.log(1 + f) / L10, down = Math.log(1 - f) / L10, finals = [], paths = [], ruined = 0, stride = Math.max(1, Math.round(n / 100));
        for (j = 0; j < 40; j++) {
          var w = 0, xs = [0], ys = [0];
          for (i = 1; i <= n; i++) { w += rnd() < p ? up : down; if (i % stride === 0 || i === n) { xs.push(i); ys.push(w); } }
          finals.push(w); paths.push([xs, ys]); if (w < -2) ruined++;
        }
        var med = QB.quantile(finals, 0.5), theory = n * grow(p, f) / L10, lo = Math.min(-3, QB.quantile(finals, 0.02) * 1.1, theory * 1.2), hi = Math.max(3, QB.quantile(finals, 0.98) * 1.1, theory * 1.2);
        var b = g[1].axes({ x: [0, n], y: [lo, hi], title: "Forty fortunes: wealth as a power of ten", xlabel: "bets placed", yfmt: function (y) { return "10^" + fmt(y, 0); }, ny: 4 });
        for (j = 0; j < 40; j++) b.line(paths[j][0], paths[j][1], { color: finals[j] < -2 ? C.loss : C.spot, width: 1, alpha: 0.45 });
        b.hline(0, { color: C.muted });
        b.line([0, n], [0, theory], { color: C.idea, width: 2.2 });
        b.legend([["typical path: n g(f)", C.idea], ["a fortune", C.spot], ["ends below 1% of the stake", C.loss]], { pos: "tl" });
        s.out = [fstar, 100 * grow(p, f), med, theory, n * Math.log(1 + f * (2 * p - 1)) / L10, ruined, zero];
      },
      readout: function (v, s) {
        var o = s.out, pow = function (x) { return "10^" + fmt(x, 1); };
        return [["Kelly fraction f*", fmt(o[0], 2)], ["g(f) per bet", fmt(o[1], 2) + "%"], ["g stays positive up to f =", fmt(o[6], 2)],
          ["median fortune", pow(o[2]) + " (theory " + pow(o[3]) + ")"], ["expected fortune", pow(o[4])], ["below 1% of the stake", o[5] + " of 40"]];
      },
      note: "Simulated data: independent even-odds bets, wealth starting at 1. g(f) = p ln(1 + f) + (1 − p) ln(1 − f). The expected fortune (1 + f(2p − 1))^n grows with every increase in f; the median follows g, which is why the two come apart.",
    });
  };

  // ---- Part 34: Press and Dyson's extortioner ----------------------------------------------------------------
  W.extortionline = function (el) {
    var T = 5, R = 3, P = 1, S = 0;
    var clip = function (x) { return Math.min(1 - 1e-6, Math.max(1e-6, x)); };
    var scores = function (p, q) { // long-run scores of X (memory-one p) and Y (memory-one q); states CC, CD, DC, DD as X sees them
      var qy = [q[0], q[2], q[1], q[3]], A = [], i, j, k, r;
      for (i = 0; i < 4; i++) A.push([0, 0, 0, 0, 0]);
      for (j = 0; j < 4; j++) {
        var px = clip(p[j]), py = clip(qy[j]), row = [px * py, px * (1 - py), (1 - px) * py, (1 - px) * (1 - py)];
        for (i = 0; i < 3; i++) A[i][j] = row[i] - (i === j ? 1 : 0); // pi M = pi, three equations
        A[3][j] = 1;
      }
      A[3][4] = 1; // and the probabilities sum to 1
      for (k = 0; k < 4; k++) { // Gaussian elimination with pivoting
        var best = k;
        for (i = k + 1; i < 4; i++) if (Math.abs(A[i][k]) > Math.abs(A[best][k])) best = i;
        var tmp = A[k]; A[k] = A[best]; A[best] = tmp;
        if (Math.abs(A[k][k]) < 1e-14) return [P, P];
        for (i = 0; i < 4; i++) if (i !== k) { r = A[i][k] / A[k][k]; for (j = k; j < 5; j++) A[i][j] -= r * A[k][j]; }
      }
      var pi = [A[0][4] / A[0][0], A[1][4] / A[1][1], A[2][4] / A[2][2], A[3][4] / A[3][3]];
      return [pi[0] * R + pi[1] * S + pi[2] * T + pi[3] * P, pi[0] * R + pi[1] * T + pi[2] * S + pi[3] * P];
    };
    QB.widget(el, {
      title: "Extortion: one player fixes a line between the two scores",
      sub: "X plays the zero-determinant strategy with extortion ratio χ; Y is one of 150 random memory-one opponents. Left: each opponent's long-run score against X's. Right: what happens as Y cooperates more. At χ = 1 the strategy is fair, like tit for tat; raise χ and X takes χ times Y's gain over mutual defection. Then let X's hand tremble and watch the line dissolve.",
      panels: 2, height: 300,
      controls: [
        { k: "chi", label: "Extortion ratio χ", min: 1, max: 6, step: 0.1, value: 3, fmt: function (x) { return x.toFixed(1); } },
        { k: "phi", label: "φ, as a share of its largest value", min: 0.1, max: 1, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "tr", label: "Departure from the formula", min: 0, max: 0.3, step: 0.01, value: 0, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New opponents", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var rnd = QB.rng(s.seed + 34), chi = v.chi, phi = v.phi / (4 * chi + 1), i;
        var p = [1 - 2 * phi * (chi - 1), 1 - phi * (4 * chi + 1), phi * (chi + 4), 0], dir = [-1, 1, -1, 1];
        for (i = 0; i < 4; i++) p[i] = Math.min(1, Math.max(0, p[i] + v.tr * dir[i]));
        var sx = [], sy = [], lo = 1e9, hi = -1e9, mx = 0, my = 0, cnt = 0;
        for (i = 0; i < 150; i++) {
          var sc = scores(p, [rnd(), rnd(), rnd(), rnd()]);
          sx.push(sc[0]); sy.push(sc[1]); mx += sc[0] / 150; my += sc[1] / 150;
          if (Math.abs(sc[1] - P) > 0.02) { var ra = (sc[0] - P) / (sc[1] - P); lo = Math.min(lo, ra); hi = Math.max(hi, ra); cnt++; }
        }
        if (!cnt) { lo = chi; hi = chi; }
        var a = g[0].axes({ x: [0, 5], y: [0, 5], title: "150 opponents: Y's score against X's", xlabel: "Y's long-run score per round" });
        a.line([0, 5], [0, 5], { color: C.muted, width: 1, dash: [4, 4] });
        a.line([P, P + 4 / chi], [P, P + 4], { color: C.idea, width: 1.5 });
        a.dots(sy, sx, { color: C.spot, r: 2.6, alpha: 0.85 });
        a.dots([P], [P], { color: C.loss, r: 4 }).dots([R], [R], { color: C.gain, r: 4 });
        a.legend([["sX − P = χ (sY − P)", C.idea], ["equal scores", C.muted], ["mutual defection (P, P)", C.loss], ["mutual cooperation (R, R)", C.gain]], { pos: "br" });
        var cs = [], yx = [], yy = [];
        for (i = 0; i <= 40; i++) { var c = i / 40, o = scores(p, [c, c, c, c]); cs.push(c); yx.push(o[0]); yy.push(o[1]); }
        var b = g[1].axes({ x: [0, 1], y: [0, 5], title: "If Y cooperates with probability c", xlabel: "Y's probability of cooperating, c" });
        b.hline(R, { color: C.muted });
        b.line(cs, yx, { color: C.idea, width: 2 }).line(cs, yy, { color: C.spot, width: 2 });
        b.legend([["X's score", C.idea], ["Y's score", C.spot], ["mutual cooperation, 3", C.muted]], { pos: "tl" });
        var self = scores(p, p);
        s.out = [p, lo, hi, mx, my, self[0], yx[40], yy[40]];
      },
      readout: function (v, s) {
        var o = s.out;
        return [["X's strategy (CC, CD, DC, DD)", o[0].map(function (x) { return x.toFixed(2); }).join(", ")],
          ["(sX − P)/(sY − P) across opponents", fmt(o[1], 2) + " to " + fmt(o[2], 2)], ["mean scores, X and Y", fmt(o[3], 2) + " and " + fmt(o[4], 2)],
          ["if Y always cooperates", "X " + fmt(o[6], 2) + ", Y " + fmt(o[7], 2)], ["X against a copy of itself", fmt(o[5], 2)]];
      },
      note: "Exact long-run averages from each pair's four-state Markov chain, with payoffs (T, R, P, S) = (5, 3, 1, 0); the opponents are random, nothing else is simulated. The formula is p = (1 − 2φ(χ − 1), 1 − φ(4χ + 1), φ(χ + 4), 0); at χ = 3 and half the largest φ it is the film's (11/13, 1/2, 7/26, 0). Y's best reply is to cooperate fully, which pays X more than mutual cooperation would.",
    });
  };

  // ---- Part 35: the utility monster under three views ---------------------------------------------------------
  W.monstershare = function (el) {
    QB.widget(el, {
      title: "Feeding the utility monster: sum, priority, maximin",
      sub: "A fixed stock of 100 units is split between n ordinary people, each with utility √x, and a monster who turns the same units into k times as much. Left: each view's welfare as the monster's portion grows, with its best split marked. Right: the best portion against k. Raise k and the sum hands the monster nearly everything; maximin does the reverse and gives it less the better it is at enjoying things.",
      panels: 2, height: 300,
      controls: [
        { k: "k", label: "The monster's efficiency k", min: 1, max: 30, step: 0.5, value: 10, fmt: function (x) { return x.toFixed(1); } },
        { k: "n", label: "Ordinary people n", min: 1, max: 50, step: 1, value: 10 },
        { k: "a", label: "Priority: welfare is the sum of u^a", min: 0.1, max: 1, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var k = v.k, n = v.n, a = v.a, T = 100, e = a / (1 - a / 2), i;
        var share = function (kk, rule) { // the monster's best portion, from equal marginal welfare on both sides
          if (rule === 0) return kk * kk / (kk * kk + n);
          if (rule === 1) { var z = Math.pow(kk, e); return z / (z + n); }
          return 1 / (1 + n * kk * kk);
        };
        var wel = function (m, rule) {
          var um = k * Math.sqrt(m), uo = Math.sqrt((T - m) / n);
          return rule === 0 ? um + n * uo : rule === 1 ? Math.pow(um, a) + n * Math.pow(uo, a) : Math.min(um, uo);
        };
        var cols = [C.loss, C.idea, C.spot], names = ["sum", "priority", "maximin"], best = [], r;
        var A = g[0].axes({ x: [0, 100], y: [0, 1.45], yticks: [0, 0.5, 1], title: "Welfare, as a share of its best, by view", xlabel: "units given to the monster" });
        for (r = 0; r < 3; r++) {
          var m0 = T * share(k, r), top = wel(m0, r), ms = [], ws = [];
          for (i = 0; i <= 200; i++) { var m = i < 40 ? i / 40 * 2 : 2 + (i - 40) / 160 * 98; ms.push(m); ws.push(top > 0 ? wel(m, r) / top : 0); }
          A.line(ms, ws, { color: cols[r], width: 1.8 });
          A.dots([m0], [1], { color: cols[r], r: 5 });
          best.push(m0);
        }
        A.legend([["sum of utilities", cols[0]], ["sum of u^a (priority)", cols[1]], ["the worst off (maximin)", cols[2]]], { pos: "tr" });
        var B = g[1].axes({ x: [1, 30], y: [0, 100], logx: true, xticks: [1, 2, 5, 10, 20, 30], title: "The monster's best portion against k", xlabel: "the monster's efficiency k" });
        var ks = QB.linspace(0, Math.log(30), 60).map(Math.exp);
        for (r = 0; r < 3; r++) B.line(ks, ks.map(function (kk) { return T * share(kk, r); }), { color: cols[r], width: 2 });
        B.vline(k, { color: C.muted });
        B.hline(T / (n + 1), { color: C.muted });
        B.text(30, T / (n + 1), "an equal split", { align: "right", dx: -6, dy: -9, color: C.muted, bg: true });
        s.out = best.concat([k * Math.sqrt(best[0]), Math.sqrt((T - best[0]) / n), (T - best[0]) / n]);
      },
      readout: function (v, s) {
        var o = s.out;
        return [["monster's units: sum", fmt(o[0], 1)], ["priority", fmt(o[1], 1)], ["maximin", fmt(o[2], 1)],
          ["under the sum, each other person gets", fmt(o[5], 2)], ["utilities under the sum: monster, each other", fmt(o[3], 1) + ", " + fmt(o[4], 2)]];
      },
      note: "Exact optima, no simulation. The sum gives the monster k²/(k² + n) of the stock; the priority view gives z/(z + n) with z = k^(a/(1 − a/2)), which is the sum at a = 1 and the film's k^(2/3) at a = 0.5; maximin equalizes utilities, 1/(1 + n k²). The others always share their part equally, which is best for every view by symmetry and concavity.",
    });
  };

  // ---- Part 36: Parfit's sequence under four views ------------------------------------------------------------
  W.repugnantladder = function (el) {
    var LET = "ABCDEFGHIJZ";
    QB.widget(el, {
      title: "Parfit's sequence: four views, four best worlds",
      sub: "World A holds one unit of people at welfare 100. Each step to the right doubles the population and keeps only a share of the welfare. Left: the worlds. Right: each view's value along the sequence, as a share of its best, with its best world marked. Slide the welfare kept below 50% and the total view stops short of Z; raise the critical level or change where the variable-value view saturates and their best worlds move.",
      panels: 2, height: 300,
      controls: [
        { k: "keep", label: "Welfare kept at each doubling", min: 0.4, max: 0.75, step: 0.01, value: 0.55, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "c", label: "Critical level c", min: 0, max: 20, step: 0.5, value: 2, fmt: function (x) { return x.toFixed(1); } },
        { k: "k", label: "Variable value saturates near N =", min: 5, max: 500, step: 5, value: 50 },
      ],
      draw: function (g, v, s) {
        var ks = [], n = [], w = [], i, r;
        for (i = 0; i <= 10; i++) { ks.push(i); n.push(Math.pow(2, i)); w.push(100 * Math.pow(v.keep, i)); }
        var vals = [n.map(function (x, j) { return x * w[j]; }), w.slice(), n.map(function (x, j) { return x * (w[j] - v.c); }),
          n.map(function (x, j) { return w[j] * v.k * (1 - Math.exp(-x / v.k)); })];
        var cols = [C.loss, C.spot, C.idea, C.gain], names = ["total", "average", "critical level", "variable value"], best = [];
        var lab = function (t) { return LET.charAt(t); };
        var a = g[0].axes({ x: [-0.6, 10.6], y: [0, 110], xticks: ks, xfmt: lab, title: "The worlds: welfare per person", xlabel: "world (population 1, 2, 4, … 1024)" });
        a.bars(ks, w, 0.7, { color: C.house, alpha: 0.8 });
        a.hline(v.c, { color: C.idea });
        a.text(10.6, v.c, "critical level", { align: "right", dx: -6, dy: -9, color: C.idea, bg: true });
        a.text(10.6, 100, "Z: 1024 people at " + fmt(w[10], w[10] < 10 ? 2 : 1), { align: "right", dx: -6, color: C.ink, bg: true });
        var b = g[1].axes({ x: [-0.6, 10.6], y: [-0.5, 1.2], yticks: [-0.5, 0, 0.5, 1], xticks: ks, xfmt: lab, title: "Each view's value, as a share of its best", xlabel: "world" });
        b.hline(0, { color: C.muted });
        for (r = 0; r < 4; r++) {
          var top = -Infinity, at = 0;
          for (i = 0; i <= 10; i++) if (vals[r][i] > top + 1e-9) { top = vals[r][i]; at = i; }
          var den = top > 1e-9 ? top : 1;
          b.line(ks, vals[r].map(function (x) { return Math.max(-0.6, x / den); }), { color: cols[r], width: 1.8 });
          b.dots([at], [top / den], { color: cols[r], r: 5.5 - r });
          best.push(at);
        }
        b.legend(names.map(function (nm, j) { return [nm, cols[j]]; }), { pos: "bl" });
        s.out = [best, 2 * v.keep, n[10] * w[10]];
      },
      readout: function (v, s) {
        var o = s.out, L = function (i) { return LET.charAt(o[0][i]); };
        return [["best world: total", L(0)], ["average", L(1)], ["critical level", L(2)], ["variable value", L(3)],
          ["total welfare changes at each step by", (o[1] >= 1 ? "+" : "−") + fmt(100 * Math.abs(o[1] - 1), 0) + "%"], ["Z's total (A's is 100)", fmt(o[2], 0)]];
      },
      note: "Exact arithmetic on the film's sequence, no simulation: total Σw, average Σw/N, critical level Σ(w − c), variable value w̄ · k(1 − e^(−N/k)). At the film's settings (55%, c = 2, k = 50) the best worlds are Z, A, D and E. A view's line dips below zero where it counts the world as worse than no one existing.",
    });
  };
})();
