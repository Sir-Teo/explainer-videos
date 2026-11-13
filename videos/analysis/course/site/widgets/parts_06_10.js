// Interactives for Analysis, Built, Parts 6-10: L^p and Hilbert space, complex analysis, Banach spaces,
// distributions, spectra.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 6: the unit ball of the p-norm, the triangle inequality and the parallelogram law --------------------
  W.pnormball = function (el) {
    var pn = function (x, y, p) { return Math.pow(Math.pow(Math.abs(x), p) + Math.pow(Math.abs(y), p), 1 / p); };
    var unit = function (deg, p) { var c = Math.cos(deg * Math.PI / 180), s = Math.sin(deg * Math.PI / 180), n = pn(c, s, p); return [c / n, s / n]; };
    var stats = function (au, av, p) { // u, v of p-norm 1 in the two directions: the midpoint's norm and the parallelogram ratio
      var u = unit(au, p), v = unit(av, p), a = pn(u[0] + v[0], u[1] + v[1], p), b = pn(u[0] - v[0], u[1] - v[1], p);
      return { u: u, v: v, mid: a / 2, ratio: (a * a + b * b) / 4 };
    };
    QB.widget(el, {
      title: "The p-norm's unit ball: a distance from p = 1 up, angles only at p = 2",
      sub: "Left: the vectors of p-norm one, two of them (u blue, v green) and their midpoint (gold). Right: for the same two directions, the midpoint's norm and the parallelogram ratio as p varies. Slide p below 1 and the ball caves in, so the midpoint leaves it; only at p = 2 does the parallelogram ratio equal 1 for every pair.",
      panels: 2, height: 310,
      controls: [
        { k: "p", label: "Exponent p", min: 0.5, max: 8, step: 0.05, value: 3, fmt: function (x) { return x.toFixed(2); } },
        { k: "au", label: "Direction of u (degrees)", min: 0, max: 180, step: 1, value: 0, fmt: function (x) { return x.toFixed(0) + "°"; } },
        { k: "av", label: "Direction of v (degrees)", min: 0, max: 180, step: 1, value: 90, fmt: function (x) { return x.toFixed(0) + "°"; } },
      ],
      draw: function (g, v, s) {
        var st = stats(v.au, v.av, v.p), i, xs = [], ys = [];
        s.out = st;
        var bw = Math.max(40, g[0].box.w - 58), bh = Math.max(40, g[0].box.h - 56), half = 1.25;
        var a = g[0].axes({ x: [-half * bw / bh, half * bw / bh], y: [-half, half], title: "Unit ball of the " + v.p.toFixed(2) + "-norm", nx: 4, ny: 4 });
        for (i = 0; i <= 360; i++) { var q = unit(i, v.p); xs.push(q[0]); ys.push(q[1]); }
        a.area(xs, ys, 0, { color: C.q, alpha: 0.16 });
        a.line(xs, ys, { color: C.q, width: 2 });
        a.line([st.u[0], st.v[0]], [st.u[1], st.v[1]], { color: C.muted, width: 1, dash: [4, 4] });
        a.line([0, st.u[0]], [0, st.u[1]], { color: C.spot, width: 2 });
        a.line([0, st.v[0]], [0, st.v[1]], { color: C.gain, width: 2 });
        a.dots([st.u[0]], [st.u[1]], { color: C.spot, r: 4.5 });
        a.dots([st.v[0]], [st.v[1]], { color: C.gain, r: 4.5 });
        a.dots([(st.u[0] + st.v[0]) / 2], [(st.u[1] + st.v[1]) / 2], { color: st.mid > 1 + 1e-9 ? C.loss : C.idea, r: 5 });
        a.legend([["u", C.spot], ["v", C.gain], ["midpoint (red if outside)", C.idea]], { pos: "bl" });
        var ps = [], mids = [], ratios = [];
        for (i = 0; i <= 120; i++) { var p = 0.5 * Math.pow(16, i / 120), t = stats(v.au, v.av, p); ps.push(p); mids.push(t.mid); ratios.push(t.ratio); }
        var b = g[1].axes({ x: [0.5, 8], y: [0, 2.5], logx: true, xticks: [0.5, 1, 2, 4, 8], title: "The same two directions, every p", xlabel: "p (log scale)" });
        b.hline(1, { color: C.muted });
        b.vline(1, { color: C.loss, alpha: 0.6 });
        b.vline(2, { color: C.idea, alpha: 0.6 });
        b.line(ps, mids, { color: C.spot, width: 2 });
        b.line(ps, ratios, { color: C.idea, width: 2 });
        b.dots([v.p], [Math.min(2.5, st.mid)], { color: C.spot, r: 4.5 });
        b.dots([v.p], [Math.min(2.5, st.ratio)], { color: C.idea, r: 4.5 });
        b.legend([["norm of the midpoint", C.spot], ["parallelogram ratio", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["norm of the midpoint", fmt(s.out.mid, 3)], ["triangle inequality for u, v", s.out.mid <= 1 + 1e-9 ? "holds" : "fails"],
          ["(diagonals²) / (sides²)", fmt(s.out.ratio, 3)], ["parallelogram law", Math.abs(s.out.ratio - 1) < 5e-4 ? "holds" : "fails"]];
      },
      note: "u and v are scaled to p-norm 1, so the sides' squares add to 4 and the ratio is (‖u+v‖² + ‖u−v‖²)/4. For p ≥ 1 Minkowski keeps every midpoint inside the ball; a single pair can satisfy the parallelogram law at other p (try u = v), but only p = 2 satisfies it for all pairs.",
    });
  };

  // ---- Part 7: the argument principle and Rouche's theorem for z^5 + a z + 1 ----------------------------------
  W.rouchewinding = function (el) {
    var roots = function (a) { // Durand-Kerner for z^5 + a z + 1 (its roots are simple for every a >= 0)
      var re = [], im = [], k, j, it;
      for (k = 0; k < 5; k++) { re.push(1.1 * Math.cos(0.4 + 2 * Math.PI * k / 5)); im.push(1.1 * Math.sin(0.4 + 2 * Math.PI * k / 5)); }
      for (it = 0; it < 80; it++) {
        for (k = 0; k < 5; k++) {
          var x = re[k], y = im[k], x2 = x * x - y * y, y2 = 2 * x * y, x4 = x2 * x2 - y2 * y2, y4 = 2 * x2 * y2;
          var pr = x4 * x - y4 * y + a * x + 1, pi = x4 * y + y4 * x + a * y, dr = 1, di = 0;
          for (j = 0; j < 5; j++) if (j !== k) { var ur = x - re[j], ui = y - im[j], t = dr * ur - di * ui; di = dr * ui + di * ur; dr = t; }
          var den = dr * dr + di * di; if (den < 1e-300) den = 1e-300;
          re[k] = x - (pr * dr + pi * di) / den; im[k] = y - (pi * dr - pr * di) / den;
        }
      }
      return [re, im];
    };
    QB.widget(el, {
      title: "Counting roots by counting turns: p(z) = z⁵ + a·z + 1",
      sub: "Left: the five roots of p (red) and a circle of radius r. Right: the image of that circle under p (gold) and under the single term a·z (blue). The number of times the gold curve winds around 0 is the number of roots inside the circle. Rouché: while |z⁵ + 1| stays below |a·z| on the circle, gold must wind as often as blue, once.",
      panels: 2, height: 320,
      controls: [
        { k: "r", label: "Radius r of the circle", min: 0.1, max: 1.6, step: 0.01, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "a", label: "Coefficient a", min: 0, max: 4, step: 0.05, value: 3, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var rt = roots(v.a), n = 720, zx = [], zy = [], wx = [], wy = [], bx = [], by = [], i, turn = 0, prev = 0, big = 0, minp = 1e9, inside = 0;
        for (i = 0; i <= n; i++) {
          var th = 2 * Math.PI * i / n, x = v.r * Math.cos(th), y = v.r * Math.sin(th), r5 = Math.pow(v.r, 5);
          var pr = r5 * Math.cos(5 * th) + v.a * x + 1, pi = r5 * Math.sin(5 * th) + v.a * y, ang = Math.atan2(pi, pr);
          zx.push(x); zy.push(y); wx.push(pr); wy.push(pi); bx.push(v.a * x); by.push(v.a * y);
          if (i > 0) { var d = ang - prev; if (d > Math.PI) d -= 2 * Math.PI; if (d < -Math.PI) d += 2 * Math.PI; turn += d; }
          prev = ang; big = Math.max(big, Math.sqrt(pr * pr + pi * pi)); minp = Math.min(minp, Math.sqrt(pr * pr + pi * pi));
        }
        for (i = 0; i < 5; i++) if (rt[0][i] * rt[0][i] + rt[1][i] * rt[1][i] < v.r * v.r) inside++;
        s.out = { wind: Math.round(turn / (2 * Math.PI)), inside: inside, minp: minp, rouche: Math.pow(v.r, 5) + 1 < v.a * v.r };
        var bw = Math.max(40, g[0].box.w - 58), bh = Math.max(40, g[0].box.h - 56), h0 = 1.8;
        var a = g[0].axes({ x: [-h0 * bw / bh, h0 * bw / bh], y: [-h0, h0], title: "z-plane: roots and the circle |z| = r", nx: 4, ny: 4 });
        a.line(zx, zy, { color: C.spot, width: 2 });
        a.dots(rt[0], rt[1], { color: C.loss, r: 4.5 });
        a.legend([["circle |z| = r", C.spot], ["roots of p", C.loss]], { pos: "bl" });
        var h1 = Math.max(1.5, big * 1.08);
        var b = g[1].axes({ x: [-h1 * bw / bh, h1 * bw / bh], y: [-h1, h1], title: "w-plane: the circle's image", nx: 4, ny: 4 });
        b.line(bx, by, { color: C.spot, width: 1.5, alpha: 0.8 });
        b.line(wx, wy, { color: C.idea, width: 2 });
        b.dots([0], [0], { color: C.ink, r: 4 });
        b.text(0, 0, "0", { dx: 7, dy: 9, bg: true });
        b.legend([["p(circle)", C.idea], ["a·z on the circle", C.spot]], { pos: "bl" });
      },
      readout: function (v, s) {
        return [["turns of p(circle) around 0", String(s.out.wind)], ["roots inside (computed directly)", String(s.out.inside)],
          ["smallest |p| on the circle", fmt(s.out.minp, 3)], ["Rouché's hypothesis r⁵ + 1 < a·r", s.out.rouche ? "holds: one root" : "does not hold"]];
      },
      note: "The roots are found by Durand-Kerner iteration and the turns by adding up the change of the argument of p along 720 points of the circle. When the circle passes through a root (smallest |p| near 0) the winding number is not defined and the two counts can differ by one. The film's example is a = 3, r = 1.",
    });
  };

  // ---- Part 8: Lebesgue constants: the Dirichlet kernel's norm grows, the Fejer kernel's does not ---------------
  W.lebesgueconstant = function (el) {
    var dir = function (t, n) { var s = Math.sin(t / 2); return Math.abs(s) < 1e-9 ? 2 * n + 1 : Math.sin((n + 0.5) * t) / s; };
    var fej = function (t, n) { var s = Math.sin(t / 2); if (Math.abs(s) < 1e-9) return n + 1; var q = Math.sin((n + 1) * t / 2) / s; return q * q / (n + 1); };
    var follow = function (t, n, w) { // continuous, bounded by 1, follows the sign of D_n with ramps of relative width w
      if (Math.abs(t) < Math.PI / (2 * n + 1)) return 1;
      return Math.max(-1, Math.min(1, Math.sin((n + 0.5) * Math.abs(t)) / w));
    };
    var lebesgue = function (n) { // Fejer's closed sum for (1/2pi) int |D_n|
      var s = 1 / (2 * n + 1), k; for (k = 1; k <= n; k++) s += 2 / Math.PI * Math.tan(Math.PI * k / (2 * n + 1)) / k; return s;
    };
    QB.widget(el, {
      title: "A function bounded by 1 against the Dirichlet kernel",
      sub: "The n-th Fourier partial sum of f at 0 is the average of f against Dirichlet's kernel (blue, divided by its peak). The gold function is continuous, bounded by 1, and follows the kernel's sign; its partial sum at 0 nearly equals the kernel's norm, which grows like log n. Press the button for Fejér's kernel, which is never negative: its norm stays 1, so nothing can blow up.",
      panels: 2, height: 310,
      controls: [
        { k: "n", label: "n: terms in the partial sum", min: 1, max: 60, step: 1, value: 8, fmt: function (x) { return x.toFixed(0); } },
        { k: "w", label: "Width of the gold function's ramps", min: 0.05, max: 1, step: 0.05, value: 0.2, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "Dirichlet / Fejér kernel", act: function (s) { s.fejer = !s.fejer; } }],
      draw: function (g, v, s) {
        var n = v.n, M = 2400, ts = [], ks = [], fs = [], neg = [], i, sum = 0, absum = 0, peak = s.fejer ? n + 1 : 2 * n + 1;
        for (i = 0; i < M; i++) {
          var t = -Math.PI + 2 * Math.PI * (i + 0.5) / M, k = s.fejer ? fej(t, n) : dir(t, n), f = s.fejer ? 1 : follow(t, n, v.w);
          ts.push(t); ks.push(k / peak); fs.push(f); neg.push(Math.min(0, k / peak)); sum += f * k; absum += Math.abs(k);
        }
        s.out = { reach: sum / M, norm: s.fejer ? 1 : lebesgue(n), quad: absum / M, asym: 4 / (Math.PI * Math.PI) * Math.log(n) + 1.27 };
        var a = g[0].axes({ x: [-Math.PI, Math.PI], y: [-1.25, 2.1], title: (s.fejer ? "Fejér" : "Dirichlet") + " kernel, n = " + n, xlabel: "t" });
        a.hline(0, { color: C.muted, dash: [] });
        a.area(ts, neg, 0, { color: C.loss, alpha: 0.55 });
        a.line(ts, fs, { color: C.idea, width: 1.3 });
        a.line(ts, ks, { color: C.spot, width: 2 });
        a.legend([["kernel ÷ its peak", C.spot], ["f, bounded by 1", C.idea], ["negative lobes", C.loss]], { pos: "tr" });
        var ns = [], Ls = [], ones = [];
        for (i = 1; i <= 60; i++) { ns.push(i); Ls.push(lebesgue(i)); ones.push(1); }
        var b = g[1].axes({ x: [1, 60], y: [0, 3.2], logx: true, xticks: [1, 2, 5, 10, 20, 60], title: "Norm of f → (partial sum at 0)", xlabel: "n (log scale)" });
        b.line(ns, Ls, { color: C.spot, width: 2 });
        b.line(ns, ones, { color: C.gain, width: 2 });
        b.dots([n], [s.out.norm], { color: s.fejer ? C.gain : C.spot, r: 5 });
        b.dots([n], [Math.max(0, Math.min(3.2, s.out.reach))], { color: C.idea, r: 4 });
        b.legend([["Dirichlet: (1/2π)∫|Dₙ|", C.spot], ["Fejér: 1 for every n", C.gain], ["reached by the gold f", C.idea]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["kernel", s.fejer ? "Fejér" : "Dirichlet"], ["norm of the functional", fmt(s.out.norm, 4)],
          ["partial sum of the gold f at 0", fmt(s.out.reach, 4)], ["share of the norm reached", QB.pct(s.out.reach / s.out.norm, 1)],
          ["(4/π²) ln n + 1.27", fmt(s.out.asym, 3)]];
      },
      note: "Exact kernels, integrated on 2,400 points. The norms of these functionals are unbounded, so by Banach-Steinhaus some continuous function has unbounded partial sums at 0; for Fejér means the norms are all 1 and the means of a continuous function converge uniformly.",
    });
  };

  // ---- Part 9: a narrowing bump acts like delta (or its derivatives) while its size blows up ---------------------
  W.deltabump = function (el) {
    var NORM = 2.2522836; // 1 / integral of exp(-1/(1-u^2)) over (-1, 1)
    var rho = function (u) { return Math.abs(u) < 1 ? NORM * Math.exp(-1 / (1 - u * u)) : 0; };
    var phi = [ // the smooth function being tested and its first two derivatives
      function (x) { return Math.sin(1.5 * x) + 0.5 * Math.cos(3 * x); },
      function (x) { return 1.5 * Math.cos(1.5 * x) - 1.5 * Math.sin(3 * x); },
      function (x) { return -2.25 * Math.sin(1.5 * x) - 4.5 * Math.cos(3 * x); },
    ];
    var drho = function (u, k) { // k-th derivative of rho by central differences (for drawing and for its sup)
      var h = 1e-3; if (k === 0) return rho(u);
      if (k === 1) return (rho(u + h) - rho(u - h)) / (2 * h);
      return (rho(u + h) - 2 * rho(u) + rho(u - h)) / (h * h);
    };
    var sups = [0, 0, 0];
    (function () { for (var k = 0; k < 3; k++) for (var i = 0; i <= 2000; i++) sups[k] = Math.max(sups[k], Math.abs(drho(-1 + i / 1000, k))); })();
    var pairing = function (k, eps, x0) { // <rho_eps^(k)(. - x0), phi> = (-1)^k int rho(u) phi^(k)(x0 + eps u) du
      var m = 80, s = 0, i; for (i = 0; i < m; i++) { var u = -1 + 2 * (i + 0.5) / m; s += rho(u) * phi[k](x0 + eps * u); }
      return (k === 1 ? -1 : 1) * s * 2 / m;
    };
    var names = ["δ", "δ′", "δ″"];
    QB.widget(el, {
      title: "What delta does: a narrowing bump tested against a smooth function",
      sub: "Left: a smooth function φ (blue) and the k-th derivative of a bump of width ε centred at x₀ (gold, drawn at a fixed height; its true size is in the readout). Right: the number the bump returns when integrated against φ, for every ε. Shrink ε: the bump's size blows up, and the number settles on φ(x₀), −φ′(x₀) or φ″(x₀).",
      panels: 2, height: 300,
      controls: [
        { k: "le", label: "Width ε of the bump", min: -2, max: 0, step: 0.02, value: -0.3, fmt: function (x) { return Math.pow(10, x).toFixed(3); } },
        { k: "x0", label: "Centre x₀", min: -2, max: 2, step: 0.02, value: 0.4, fmt: function (x) { return fmt(x, 2); } },
        { k: "k", label: "Derivatives k of the bump", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return x.toFixed(0) + " (" + names[x] + ")"; } },
      ],
      draw: function (g, v, s) {
        var eps = Math.pow(10, v.le), k = v.k, i, xs = QB.linspace(-3.2, 3.2, 321), ys = [], bx = [], by = [];
        for (i = 0; i < xs.length; i++) ys.push(phi[0](xs[i]));
        for (i = 0; i <= 400; i++) { var u = -1 + i / 200; bx.push(v.x0 + eps * u); by.push(1.6 * drho(u, k) / sups[k]); }
        var limit = (k === 1 ? -1 : 1) * phi[k](v.x0);
        s.out = { pair: pairing(k, eps, v.x0), limit: limit, sup: sups[k] / Math.pow(eps, k + 1) };
        var a = g[0].axes({ x: [-3.2, 3.2], y: [-2.2, 2.2], title: "φ and the bump's " + (k === 0 ? "graph" : k === 1 ? "first derivative" : "second derivative"), xlabel: "x" });
        a.hline(0, { color: C.muted, dash: [] });
        a.line(xs, ys, { color: C.spot, width: 2 });
        a.area(bx, by, 0, { color: C.idea, alpha: 0.25 });
        a.line(bx, by, { color: C.idea, width: 2 });
        a.vline(v.x0, { color: C.muted });
        a.dots([v.x0], [phi[0](v.x0)], { color: C.spot, r: 4.5 });
        a.legend([["φ", C.spot], ["bump (not to scale)", C.idea]], { pos: "bl" });
        var es = [], ps = [], lo = limit, hi = limit;
        for (i = 0; i <= 50; i++) { var e = Math.pow(10, -2 + 2 * i / 50), p = pairing(k, e, v.x0); es.push(e); ps.push(p); lo = Math.min(lo, p); hi = Math.max(hi, p); }
        var pad = Math.max(0.15, 0.15 * (hi - lo));
        var b = g[1].axes({ x: [0.01, 1], y: [lo - pad, hi + pad], logx: true, xticks: [0.01, 0.03, 0.1, 0.3, 1], title: "⟨k-th derivative of the bump, φ⟩", xlabel: "width ε (log scale)" });
        b.hline(limit, { color: C.gain, width: 1.5 });
        b.line(es, ps, { color: C.idea, width: 2 });
        b.dots([eps], [s.out.pair], { color: C.idea, r: 5 });
        b.legend([["the bump's answer", C.idea], ["limit: ⟨" + names[k] + " at x₀, φ⟩", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["the bump's answer", fmt(s.out.pair, 4)], ["limit as ε → 0", fmt(s.out.limit, 4)],
          ["gap", s.out.pair === s.out.limit ? "0" : Math.abs(s.out.pair - s.out.limit).toExponential(1)],
          ["largest value of the bump's k-th derivative", s.out.sup.toExponential(2)]];
      },
      note: "The bump is exp(−1/(1 − u²)) scaled to area 1 and width ε; φ(x) = sin 1.5x + ½ cos 3x. The answer is computed as (−1)ᵏ ∫ bump · φ⁽ᵏ⁾, which is the definition of a distribution's derivative. The gap shrinks like ε² while the bump's k-th derivative grows like ε^−(k+1): no function is the limit, but the functional is.",
    });
  };

  // ---- Part 10: approximate eigenvectors of multiplication by x on L^2[0, 1] -------------------------------------
  W.approxeigen = function (el) {
    var ratio = function (lam, w) { // |(M - lam) psi| / |psi| for a Gaussian of width w centred at the point of [0, 1] nearest lam
      var c = Math.max(0, Math.min(1, lam)), m = 400, num = 0, den = 0, i;
      for (i = 0; i < m; i++) { var x = (i + 0.5) / m, p = Math.exp(-(x - c) * (x - c) / (w * w)); num += (x - lam) * (x - lam) * p; den += p; }
      return den > 0 ? Math.sqrt(num / den) : Math.abs(c - lam);
    };
    QB.widget(el, {
      title: "Multiplication by x: a spectrum with no eigenvectors",
      sub: "M multiplies a function on [0, 1] by x. Left: a bump ψ (blue) centred as near to λ as it can be, and (x − λ)ψ (gold), on the same scale. Right: the ratio ‖(M − λ)ψ‖ / ‖ψ‖ for every width. For λ inside [0, 1], squeeze the bump and the ratio goes to 0: an approximate eigenvector, never an exact one. Move λ outside and the ratio is stuck above the distance to [0, 1].",
      panels: 2, height: 300,
      controls: [
        { k: "lam", label: "λ", min: -0.5, max: 1.5, step: 0.01, value: 0.4, fmt: function (x) { return fmt(x, 2); } },
        { k: "lw", label: "Width of the bump", min: -2.3, max: -0.3, step: 0.02, value: -1, fmt: function (x) { return Math.pow(10, x).toFixed(3); } },
      ],
      draw: function (g, v, s) {
        var w = Math.pow(10, v.lw), c = Math.max(0, Math.min(1, v.lam)), xs = QB.linspace(0, 1, 401), ps = [], qs = [], i, qmax = 1e-12;
        for (i = 0; i < xs.length; i++) { var p = Math.exp(-(xs[i] - c) * (xs[i] - c) / (2 * w * w)); ps.push(p); qs.push((xs[i] - v.lam) * p); qmax = Math.max(qmax, Math.abs(qs[i])); }
        var dist = Math.max(0, -v.lam, v.lam - 1);
        s.out = { ratio: ratio(v.lam, w), dist: dist };
        var a = g[0].axes({ x: [-0.5, 1.5], y: [-1.15, 1.15], title: "ψ and (x − λ)ψ on [0, 1]", xlabel: "x" });
        a.area([0, 1], [1.15, 1.15], -1.15, { color: C.q, alpha: 0.08 });
        a.hline(0, { color: C.muted, dash: [] });
        a.vline(v.lam, { color: C.loss });
        a.text(v.lam, 1.02, "λ", { color: C.loss, dx: v.lam > 1.3 ? -12 : 6 });
        a.line(xs, ps, { color: C.spot, width: 2 });
        a.line(xs, qs, { color: C.idea, width: 2 });
        a.legend([["ψ", C.spot], ["(x − λ)ψ", C.idea], ["spectrum [0, 1]", C.q]], { pos: "bl" });
        var ws = [], rs = [];
        for (i = 0; i <= 40; i++) { var ww = Math.pow(10, -2.3 + 2 * i / 40); ws.push(ww); rs.push(Math.max(0.002, ratio(v.lam, ww))); }
        var b = g[1].axes({ x: [0.005, 0.5], y: [0.002, 2], logx: true, logy: true, xticks: [0.005, 0.02, 0.1, 0.5], title: "‖(M − λ)ψ‖ / ‖ψ‖", xlabel: "width of the bump (log scale)" });
        if (dist > 0.001) { b.hline(dist, { color: C.loss, width: 1.5 }); }
        b.line(ws, rs, { color: C.idea, width: 2 });
        b.dots([w], [Math.max(0.002, Math.min(2, s.out.ratio))], { color: C.idea, r: 5 });
        b.legend(dist > 0.001 ? [["ratio", C.idea], ["distance from λ to [0, 1]", C.loss]] : [["ratio (→ 0 with the width)", C.idea]], { pos: "br" });
      },
      readout: function (v, s) {
        return [["‖(M − λ)ψ‖ / ‖ψ‖", fmt(s.out.ratio, 4)], ["distance from λ to [0, 1]", fmt(s.out.dist, 2)],
          ["norm of (M − λ)⁻¹", s.out.dist > 1e-9 ? fmt(1 / s.out.dist, 2) : "unbounded"], ["λ is", s.out.dist > 1e-9 ? "outside the spectrum" : "in the spectrum"]];
      },
      note: "ψ is a Gaussian cut off to [0, 1]; the norms are L² norms computed on 400 points. (M − λ)⁻¹ is multiplication by 1/(x − λ), bounded exactly when λ is off [0, 1], with norm 1 / distance. No ψ ever makes the ratio exactly 0: (x − λ)ψ = 0 almost everywhere forces ψ = 0.",
    });
  };
})();
