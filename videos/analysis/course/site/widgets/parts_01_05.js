// Interactives for Analysis, Built, Parts 1-5: Principles of Mathematical Analysis, and the Lebesgue integral.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 1: the cover game on (0, 1] ----------------------------------------------------------------------
  W.covergame = function (el) {
    var need = function (a, rho) { return Math.floor(Math.log(a) / Math.log(rho) + 1e-9) + 1; };
    QB.widget(el, {
      title: "The cover game on (0, 1]: how many intervals reach down to a?",
      sub: "Every point x of (0, 1] is given the open interval from x(1 − r) to x(1 + r): an open cover of (0, 1]. The gold intervals are the fewest that cover [a, 1]; neighbours overlap by a hair. Slide a toward 0: the closed set [a, 1] always gets a finite subcover, but the count grows without bound, so (0, 1] gets none.",
      panels: 2, height: 300,
      controls: [
        { k: "la", label: "Left end a of the set [a, 1]", min: -6, max: -0.3, step: 0.1, value: -1, fmt: function (x) { var a = Math.pow(10, x); return a >= 0.01 ? a.toFixed(3) : a.toExponential(1); } },
        { k: "r", label: "Radius of each interval, as a share of its centre x", min: 0.1, max: 0.9, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var a = Math.pow(10, v.la), rho = (1 - v.r) / (1 + v.r), N = need(a, rho), j;
        s.out = [a, N, Math.log(1 / a) / Math.log(1 / rho)];
        var p = g[0].axes({ x: [1e-6, 3], y: [0, 1], logx: true, noY: true, title: "The fewest intervals covering [a, 1]", xlabel: "x (log scale)" });
        p.area([1e-6, a], [1, 1], 0, { color: C.loss, alpha: 0.13 });
        p.line([a, 1], [0.08, 0.08], { color: C.ink, width: 3 });
        for (j = 1; j <= N; j++) {
          var y = 0.22 + 0.14 * ((j - 1) % 4);
          p.line([Math.max(1e-6, Math.pow(rho, j)), Math.pow(rho, j - 1) * 1.02], [y, y], { color: C.idea, width: 4 });
        }
        p.vline(a, { color: C.loss });
        p.legend([["[a, 1]", C.ink], ["chosen intervals", C.idea], ["not yet reached", C.loss]], { pos: "tl" });
        p.text(3, 0.92, N + (N === 1 ? " interval" : " intervals"), { color: C.idea, bold: true, dx: -8, align: "right", bg: true });
        var top = need(1e-6, rho) + 2, as = [], ns = [];
        for (j = 0; j <= 240; j++) { var aa = Math.pow(10, -6 + 6 * j / 240); as.push(aa); ns.push(need(Math.min(aa, 0.999), rho)); }
        var q = g[1].axes({ x: [1e-6, 1], y: [0, top], logx: true, title: "Intervals needed, against a", xlabel: "a (log scale)" });
        q.line(as, ns, { color: C.spot, width: 2 });
        q.vline(a, { color: C.loss });
        q.dots([a], [N], { color: C.idea, r: 5 });
        q.text(1e-6, 0, "a → 0: no finite number is enough", { color: C.muted, dx: 8, dy: -12 });
      },
      readout: function (v, s) {
        return [["a", s.out[0] >= 0.01 ? s.out[0].toFixed(3) : s.out[0].toExponential(1)], ["intervals needed for [a, 1]", String(s.out[1])],
          ["ln(1/a) / ln((1 + r)/(1 − r))", fmt(s.out[2], 2)], ["for (0, 1] itself", "no finite subcover"]];
      },
      note: "Exact count, not a simulation: N intervals of this family reach down only to left ends above ((1 − r)/(1 + r))ᴺ, so [a, 1] needs the least N greater than ln(1/a) / ln((1 + r)/(1 − r)). Heine-Borel's bisection fails on (0, 1] at exactly the missing point 0.",
    });
  };

  // ---- Part 2: Riemann's rearrangement, by the greedy rule ---------------------------------------------------
  W.greedyrearrange = function (el) {
    QB.widget(el, {
      title: "One series, any sum you like: the greedy rearrangement",
      sub: "The terms are +1, +1/3ᵖ, +1/5ᵖ, … and −1/2ᵖ, −1/4ᵖ, … Below the target, take the next unused positive term; above it, the next negative one. With p = 1 the series converges only conditionally and every target is reached. Raise p above 1: the series converges absolutely, the positive pile is finite, and the walk stalls.",
      panels: 2, height: 300,
      controls: [
        { k: "T", label: "Target sum", min: -2, max: 4, step: 0.01, value: 3.14, fmt: function (x) { return fmt(x, 2); } },
        { k: "n", label: "Terms used", min: 20, max: 3000, step: 20, value: 400, fmt: function (x) { return String(x); } },
        { k: "p", label: "Exponent p of the terms ±1/kᵖ", min: 1, max: 2, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var p = v.p, T = v.T, n = v.n, i, sum = 0, ip = 0, im = 0, up = 0, down = 0, xs = [], ys = [], rat = [];
        for (i = 1; i <= n; i++) {
          if (sum <= T) { ip++; up = Math.pow(2 * ip - 1, -p); sum += up; } else { im++; down = Math.pow(2 * im, -p); sum -= down; }
          xs.push(i); ys.push(sum); rat.push((ip + 0.5) / (im + 0.5));
        }
        if (s.natp !== p) { // the sum in the natural order, by averaging two consecutive partial sums
          var a = 0, b = 0; for (i = 1; i <= 2000; i++) { b = a; a += (i % 2 ? 1 : -1) * Math.pow(i, -p); }
          s.nat = (a + b) / 2; s.natp = p;
        }
        var cond = Math.abs(p - 1) < 1e-9, pred = Math.exp(2 * (T - Math.LN2));
        s.out = [sum, Math.abs(sum - T), ip, im, cond ? pred : null, ip > 0 && im > 0 && Math.abs(sum - T) <= Math.max(up, down)];
        var lo = Math.min(T, s.nat, 0) - 0.5, hi = Math.max(T, s.nat, 1) + 0.6;
        var A = g[0].axes({ x: [0, n], y: [lo, hi], title: "Partial sums of the rearranged series", xlabel: "terms used" });
        A.hline(s.nat, { color: C.muted });
        A.hline(T, { color: C.idea, dash: [6, 4], width: 1.5 });
        A.line(xs, ys, { color: C.spot, width: 1.6 });
        A.legend([["partial sums", C.spot], ["target", C.idea], ["sum in the natural order", C.muted]], { pos: T > (lo + hi) / 2 ? "br" : "tr" });
        var B = g[1].axes({ x: [0, n], y: [1e-3, 1e4], logy: true, title: "Positive terms used per negative term", xlabel: "terms used" });
        B.line(xs, rat, { color: C.spot, width: 1.6 });
        if (cond) { B.hline(pred, { color: C.idea, dash: [6, 4], width: 1.5 }); B.legend([["running ratio", C.spot], ["e^(2(T − ln 2))", C.idea]], { pos: "br" }); }
        else B.legend([["running ratio", C.spot]], { pos: "br" });
      },
      readout: function (v, s) {
        return [["sum after " + v.n + " terms", fmt(s.out[0], 4)], ["distance from the target", fmt(s.out[1], 4)],
          ["positive : negative terms used", s.out[2] + " : " + s.out[3]],
          ["Pringsheim's ratio e^(2(T − ln 2))", s.out[4] === null ? "p = 1 only" : (s.out[4] >= 10 ? fmt(s.out[4], 1) : fmt(s.out[4], 3))],
          ["within the last term taken from either pile", s.out[5] ? "yes" : "no"]];
      },
      note: "Exact arithmetic in floating point, no simulation. For p = 1, once the target has been crossed the distance to it is at most the last term taken from one of the piles, which tends to 0 (Riemann's theorem, Rudin 3.54). For p > 1 a walk that stalls is not a rearrangement at all: it stops using one pile, and every true rearrangement has the natural sum (Rudin 3.55).",
    });
  };

  // ---- Part 3: Fourier partial sums and Fejér means under two lenses -----------------------------------------
  W.gibbsfejer = function (el) {
    var PI = Math.PI;
    var shapes = [
      { name: "sawtooth", c0: 0, jump: PI, y: [-2.2, 2.2],
        f: function (x) { return x > 0 ? (PI - x) / 2 : x < 0 ? (-PI - x) / 2 : 0; }, term: function (k, x) { return Math.sin(k * x) / k; } },
      { name: "square wave", c0: 0, jump: PI / 2, y: [-1.3, 1.3],
        f: function (x) { return x > 0 ? PI / 4 : x < 0 ? -PI / 4 : 0; }, term: function (k, x) { return k % 2 ? Math.sin(k * x) / k : 0; } },
      { name: "triangle wave", c0: PI / 2, jump: 0, y: [-0.4, 3.9],
        f: function (x) { return Math.abs(x); }, term: function (k, x) { return k % 2 ? -4 / PI * Math.cos(k * x) / (k * k) : 0; } },
    ];
    QB.widget(el, {
      title: "A Fourier series under two lenses: the sup error and the mean-square error",
      sub: "The magenta curve is the partial sum s_N, the green one the Fejér mean (the average of s_0, …, s_N). At a jump the partial sum overshoots by about 9% of the jump however large N is, so its sup error never shrinks, while its mean-square error goes to 0. Switch to the triangle wave, which is continuous: now both go to 0. Narrow the window to look at the jump.",
      panels: 2, height: 310,
      controls: [
        { k: "shape", label: "Function", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return shapes[x].name; } },
        { k: "N", label: "Terms N", min: 1, max: 150, step: 1, value: 20, fmt: function (x) { return String(x); } },
        { k: "z", label: "Half-width of the window around 0", min: 0.2, max: 3.14, step: 0.02, value: 3.14, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var sh = shapes[v.shape], N = v.N, i, k, t;
        var at = function (x) { var a = sh.c0, b = sh.c0; for (var m = 1; m <= N; m++) { var u = sh.term(m, x); a += u; b += (1 - m / (N + 1)) * u; } return [a, b]; };
        var n1 = 320, xs = [], fs = [], ss = [], fe = [];
        for (i = 0; i < n1; i++) {
          var x = -v.z + 2 * v.z * (i + 0.5) / n1; t = at(x);
          xs.push(x); fs.push(sh.f(x)); ss.push(t[0]); fe.push(t[1]);
        }
        var A = g[0].axes({ x: [-v.z, v.z], y: sh.y, title: "The " + sh.name + ", s_N and the Fejér mean", xlabel: "x" });
        if (sh.jump) { A.line(xs.slice(0, n1 / 2), fs.slice(0, n1 / 2), { color: C.cash, width: 2.4 }); A.line(xs.slice(n1 / 2), fs.slice(n1 / 2), { color: C.cash, width: 2.4 }); }
        else A.line(xs, fs, { color: C.cash, width: 2.4 });
        A.line(xs, fe, { color: C.gain, width: 1.6 });
        A.line(xs, ss, { color: C.option, width: 1.6 });
        A.legend([["f", C.cash], ["partial sum s_N", C.option], ["Fejér mean", C.gain]], { pos: sh.jump ? "tr" : "tl" });
        // errors of s_n and of the Fejér mean for n = 1 .. N, on a grid of (−π, π)
        var M = 240, gx = [], gf = [], cur = [], cum = [], ns = [], esup = [], erms = [], fsup = [];
        for (i = 0; i < M; i++) gx.push(-PI + 2 * PI * (i + 0.5) / M);
        for (i = 1; i <= 12; i++) { gx.push(PI * Math.pow(2, -i)); gx.push(-PI * Math.pow(2, -i)); } // closing in on 0, for the sup only
        for (i = 0; i < gx.length; i++) { gf.push(sh.f(gx[i])); cur.push(sh.c0); cum.push(sh.c0); }
        for (k = 1; k <= N; k++) {
          var a = 0, b = 0, c = 0;
          for (i = 0; i < gx.length; i++) {
            cur[i] += sh.term(k, gx[i]); cum[i] += cur[i];
            var d = Math.abs(cur[i] - gf[i]), e = Math.abs(cum[i] / (k + 1) - gf[i]);
            if (d > a) a = d; if (i < M) b += d * d; if (e > c) c = e;
          }
          ns.push(k); esup.push(Math.max(a, 1e-4)); erms.push(Math.max(Math.sqrt(b / M), 1e-4)); fsup.push(Math.max(c, 1e-4));
        }
        var B = g[1].axes({ x: [0, Math.max(N, 4)], y: [1e-4, 10], logy: true, title: "Errors against the number of terms", xlabel: "n" });
        B.line(ns, esup, { color: C.option, width: 1.8 });
        B.line(ns, fsup, { color: C.gain, width: 1.8 });
        B.line(ns, erms, { color: C.spot, width: 1.8 });
        if (N < 3) B.dots([N, N, N], [esup[N - 1], fsup[N - 1], erms[N - 1]], { color: function (j) { return [C.option, C.gain, C.spot][j]; }, r: 3.5 });
        B.legend([["sup |s_n − f|", C.option], ["sup |Fejér − f|", C.gain], ["root-mean-square of s_n − f", C.spot]], { pos: "bl" });
        var over = null;
        if (sh.jump) { // the first peak to the right of the jump
          var mx = -1e9, xp; for (i = 1; i <= 160; i++) { xp = Math.min(PI, 3 * PI / (N + 1)) * i / 160; t = at(xp)[0] - sh.f(xp); if (t > mx) mx = t; }
          over = mx / sh.jump;
        }
        s.out = [over, esup[N - 1], erms[N - 1], fsup[N - 1]];
      },
      readout: function (v, s) {
        return [["largest s_N − f beside the jump, as a share of the jump", s.out[0] === null ? "no jump" : QB.pct(s.out[0], 2)],
          ["sup error of s_N", fmt(s.out[1], 3)], ["root-mean-square error of s_N", fmt(s.out[2], 4)], ["sup error of the Fejér mean", fmt(s.out[3], 3)]];
      },
      note: "Computed from the series, no simulation. The sup errors are taken on a grid of 240 points plus points closing in on 0 from both sides, none of them at the jump itself. The overshoot tends to Si(π)/π − 1/2 = 8.95% of the jump (Gibbs); Fejér's kernel is nonnegative, so the green curve never overshoots, but no sequence of continuous functions converges uniformly to a jump.",
    });
  };

  // ---- Part 4: the contraction principle on a cobweb ---------------------------------------------------------
  W.cobwebcontract = function (el) {
    var S1 = Math.sin(1);
    QB.widget(el, {
      title: "Iterating g(x) = a cos x: a contraction, and what happens when it stops being one",
      sub: "The gold path bounces between the curve and the diagonal; the green dot is the fixed point. For a ≤ 1 the map sends [0, 1] into itself and shrinks distances by c = a sin 1 < 1, so the theorem promises one fixed point and the bound cⁿ/(1 − c)·|x₁ − x₀| on the error. Raise a: past 1 the theorem is silent though the iteration still converges, and once the slope at the fixed point exceeds 1 it settles on a two-point cycle instead.",
      panels: 2, height: 310,
      controls: [
        { k: "a", label: "Factor a in g(x) = a cos x", min: 0.2, max: 2.5, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "x0", label: "Starting point x₀", min: 0, max: 1, step: 0.01, value: 0.1, fmt: function (x) { return x.toFixed(2); } },
        { k: "n", label: "Steps", min: 1, max: 40, step: 1, value: 12, fmt: function (x) { return String(x); } },
      ],
      draw: function (g, v, s) {
        var a = v.a, n = v.n, i, lo = 0, hi = Math.PI / 2;
        for (i = 0; i < 60; i++) { var m = (lo + hi) / 2; if (m - a * Math.cos(m) < 0) lo = m; else hi = m; }
        var xstar = (lo + hi) / 2, orb = [v.x0];
        for (i = 0; i < n; i++) orb.push(a * Math.cos(orb[i]));
        var mn = Math.min.apply(null, orb.concat([0])) - 0.15, mxv = Math.max.apply(null, orb.concat([1, xstar])) + 0.15;
        var A = g[0].axes({ x: [mn, mxv], y: [mn, mxv], title: "The cobweb", xlabel: "x" });
        var gx = QB.linspace(mn, mxv, 160), gy = gx.map(function (x) { return a * Math.cos(x); });
        A.line([mn, mxv], [mn, mxv], { color: C.muted, width: 1.2 });
        A.line(gx, gy, { color: C.spot, width: 2 });
        var px = [orb[0]], py = [mn];
        for (i = 0; i < n; i++) { px.push(orb[i]); py.push(orb[i + 1]); px.push(orb[i + 1]); py.push(orb[i + 1]); }
        A.line(px, py, { color: C.idea, width: 1.3, alpha: 0.9 });
        A.dots([xstar], [xstar], { color: C.gain, r: 5 });
        A.legend([["y = a cos x", C.spot], ["the iteration", C.idea]], { pos: "br" });
        var c = a * S1, has = a <= 1 + 1e-9, ks = [], er = [], bd = [], d0 = Math.abs(orb[1] - orb[0]);
        for (i = 0; i <= n; i++) {
          ks.push(i); er.push(Math.max(Math.abs(orb[i] - xstar), 1e-16));
          if (has) bd.push(Math.max(Math.pow(c, i) / (1 - c) * d0, 1e-16));
        }
        var B = g[1].axes({ x: [0, Math.max(n, 4)], y: [1e-16, 100], logy: true, yticks: [1e-16, 1e-12, 1e-8, 1e-4, 1], title: "Distance to the fixed point", xlabel: "step k",
          yfmt: function (y) { return y === 1 ? "1" : "1e" + Math.round(Math.log(y) / Math.LN10); } });
        if (has) B.line(ks, bd, { color: C.idea, width: 1.6, dash: [6, 4] });
        B.line(ks, er, { color: C.spot, width: 2 });
        B.dots(ks, er, { color: C.spot, r: 2.4 });
        B.legend(has ? [["|x_k − x*|", C.spot], ["the theorem's bound", C.idea]] : [["|x_k − x*|", C.spot]], { pos: "bl" });
        var slope = a * Math.sin(xstar);
        s.out = [xstar, slope, er[n], has ? bd[n] : null, has ? "a contraction of [0, 1]" : slope < 1 ? "no contraction of [0, 1], but still attracting" : "repelling: a two-point cycle"];
      },
      readout: function (v, s) {
        var e = function (x) { return x < 1e-3 ? x.toExponential(1) : fmt(x, 4); };
        return [["fixed point x*", fmt(s.out[0], 6)], ["slope there, |g′(x*)|", fmt(s.out[1], 3)], ["error after " + v.n + " steps", e(s.out[2])],
          ["bound from the theorem", s.out[3] === null ? "none (a > 1)" : e(s.out[3])], ["verdict", s.out[4]]];
      },
      note: "Exact iteration in floating point; errors are floored at 1e−16. At a = 1 this is the film's cos x = x, with x* = 0.7390851332 and c = sin 1 ≈ 0.84. The contraction principle is sufficient, not necessary: between a = 1 and about 1.32 the iteration converges without the theorem's help.",
    });
  };

  // ---- Part 5: escaping mass, and the lid that stops it ------------------------------------------------------
  W.masslid = function (el) {
    var names = ["tall spike n·1(0, 1/n]", "sliding block 1[n, n+1]", "spreading slab (1/n)·1[0, n]", "(1 − x/n)ⁿ on [0, n]"];
    var H = function (k) { var h = 0; for (var j = 1; j <= k; j++) h += 1 / j; return h; };
    QB.widget(el, {
      title: "Escaping mass, and the lid that stops it",
      sub: "Blue is f_n; gold is the smallest lid so far, the largest of f_1, …, f_n at each point. The first three sequences have integral 1 and tend to 0 at every point: the mass escapes, and the lid's integral grows without bound. The fourth lies under the integrable lid e^(−x) (green), and its integrals converge to the integral of its limit.",
      panels: 2, height: 300,
      controls: [
        { k: "q", label: "Sequence", min: 0, max: 3, step: 1, value: 0, fmt: function (x) { return names[x]; } },
        { k: "n", label: "Index n", min: 1, max: 60, step: 1, value: 6, fmt: function (x) { return String(x); } },
      ],
      draw: function (g, v, s) {
        var n = v.n, q = v.q, k, A, fx = [], fy = [], ex = [], ey = [], ks = [], I = [], E = [];
        if (q === 0) {
          A = g[0].axes({ x: [0, 1], y: [0, Math.max(4, 1.12 * n)], title: "f_n and the smallest lid", xlabel: "x" });
          fx = [0, 1 / n, 1 / n, 1]; fy = [n, n, 0, 0];
          ex.push(0); ey.push(n);
          for (k = n; k >= 1; k--) { ex.push(1 / k); ey.push(k); ex.push(1 / k); ey.push(k - 1); }
        } else if (q === 1) {
          A = g[0].axes({ x: [0, Math.max(6, n + 2)], y: [0, 1.5], title: "f_n and the smallest lid", xlabel: "x" });
          fx = [n, n, n + 1, n + 1]; fy = [0, 1, 1, 0];
          ex = [1, 1, n + 1, n + 1]; ey = [0, 1, 1, 0];
        } else if (q === 2) {
          A = g[0].axes({ x: [0, Math.max(6, n + 1)], y: [0, 1.25], title: "f_n and the smallest lid", xlabel: "x" });
          fx = [0, n, n, n + 1]; fy = [1 / n, 1 / n, 0, 0];
          for (k = 1; k <= n; k++) { ex.push(k - 1); ey.push(1 / k); ex.push(k); ey.push(1 / k); }
          ex.push(n); ey.push(0);
        } else {
          A = g[0].axes({ x: [0, 8], y: [0, 1.25], title: "f_n under the lid e^(−x)", xlabel: "x" });
          var xs = QB.linspace(0, 8, 200);
          fx = xs; fy = xs.map(function (x) { return x < n ? Math.pow(1 - x / n, n) : 0; });
          ex = xs; ey = xs.map(function (x) { return Math.exp(-x); });
        }
        A.area(fx, fy, 0, { color: C.spot, alpha: 0.28 });
        A.line(ex, ey, { color: q === 3 ? C.gain : C.idea, width: 2 });
        A.line(fx, fy, { color: C.spot, width: 2 });
        A.legend(q === 3 ? [["f_n", C.spot], ["the lid e^(−x)", C.gain]] : [["f_n", C.spot], ["smallest lid for f_1 … f_n", C.idea]], { pos: "tr" });
        for (k = 1; k <= n; k++) {
          ks.push(k); I.push(q === 3 ? k / (k + 1) : 1);
          E.push(q === 0 || q === 2 ? H(k) : q === 1 ? k : k / (k + 1));
        }
        var top = Math.max(2.4, 1.6 * E[n - 1]);
        var B = g[1].axes({ x: [0, Math.max(n, 4)], y: [0, top], title: "Integrals against the index", xlabel: "k" });
        B.hline(q === 3 ? 1 : 0, { color: C.muted });
        if (q !== 3) B.line(ks, E, { color: C.idea, width: 2 });
        B.line(ks, I, { color: C.spot, width: 2 });
        B.dots([n, n], [E[n - 1], I[n - 1]], { color: function (j) { return j || q === 3 ? C.spot : C.idea; }, r: 4 });
        B.legend(q === 3 ? [["∫ f_k = k/(k + 1), below ∫ e^(−x) = 1", C.spot], ["∫ of the limit", C.muted]]
          : [["∫ f_k", C.spot], ["∫ of the smallest lid for f_1 … f_k", C.idea], ["∫ of the limit", C.muted]], { pos: "tl" });
        s.out = [I[n - 1], q === 3 ? 1 : 0, E[n - 1], q === 3 ? "yes: e^(−x), with integral 1" : q === 1 ? "no: the smallest lid has integral n" : "no: the smallest lid has integral 1 + 1/2 + … + 1/n"];
      },
      readout: function (v, s) {
        return [["∫ f_n", fmt(s.out[0], 3)], ["∫ of the pointwise limit", fmt(s.out[1], 0)], ["∫ of the smallest lid so far", fmt(s.out[2], 3)], ["an integrable lid", s.out[3]]];
      },
      note: "Exact values, no simulation. Fatou's lemma allows the integral of the limit to be smaller than the limit of the integrals, never larger; dominated convergence says that under one integrable lid the two are equal. For (1 − x/n)ⁿ the integrals are n/(n + 1).",
    });
  };
})();
