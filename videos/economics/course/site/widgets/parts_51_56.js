// Interactives for Act X, The Graduate Core (Parts 51-56).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var W = QB.W;

  // ---- Part 51: computing economies -----------------------------------------------------------------------------
  W.solver = function (el) {
    // Agora's solver harness (explainer.economics.agora.solve): the growth model u = c^(1-g)/(1-g), output k^0.36,
    // depreciation 8%.  Value iteration with next year's capital on a grid of n points from half to one and a half
    // times the steady state, against an accurate rule from time iteration on the Euler equation (200 points,
    // bisection, linear interpolation).  Euler errors on 121 points between 0.6 and 1.4 times the steady state.
    var A = 0.36, DEL = 0.08;
    function model(beta, g) {
      var kss = Math.pow((1 / beta - 1 + DEL) / A, 1 / (A - 1));
      return { beta: beta, g: g, kss: kss };
    }
    function res(k) { return Math.pow(k, A) + (1 - DEL) * k; }
    function mpk(k) { return A * Math.pow(k, A - 1) + 1 - DEL; }
    function u(c, g) { return Math.abs(g - 1) < 1e-9 ? Math.log(c) : Math.pow(c, 1 - g) / (1 - g); }
    function interp(xs, ys, x) {
      var n = xs.length;
      if (x <= xs[0]) { return ys[0] + (ys[1] - ys[0]) * (x - xs[0]) / (xs[1] - xs[0]); }
      if (x >= xs[n - 1]) { return ys[n - 2] + (ys[n - 1] - ys[n - 2]) * (x - xs[n - 2]) / (xs[n - 1] - xs[n - 2]); }
      var lo = 0, hi = n - 1;
      while (hi - lo > 1) { var mid = (lo + hi) >> 1; if (xs[mid] <= x) { lo = mid; } else { hi = mid; } }
      return ys[lo] + (ys[hi] - ys[lo]) * (x - xs[lo]) / (xs[hi] - xs[lo]);
    }
    function grid(m, n) {
      var g = [];
      for (var i = 0; i < n; i++) { g.push(m.kss * (0.5 + i / (n - 1))); }
      return g;
    }
    function vfi(m, n) {
      var g = grid(m, n), V = new Array(n).fill(0), j = new Array(n).fill(0), rounds = 0;
      for (var it = 0; it < 4000; it++) {
        var TV = new Array(n), d = 0;
        var start = 0;
        for (var a = 0; a < n; a++) {
          // the policy rises with capital and the objective is concave in k': search upwards from the last choice
          // and stop at the first fall
          var best = -Infinity, bj = start, R = res(g[a]);
          for (var b = start; b < n; b++) {
            var c = R - g[b];
            if (c <= 0) { break; }
            var w = u(c, m.g) + m.beta * V[b];
            if (w > best) { best = w; bj = b; } else { break; }
          }
          TV[a] = best; j[a] = bj; start = bj;
          d = Math.max(d, Math.abs(best - V[a]));
        }
        V = TV; rounds = it + 1;
        if (d < 1e-6) { break; }
      }
      return { g: g, kp: j.map(function (i) { return g[i]; }), rounds: rounds };
    }
    function accurate(m) {
      var n = 200, g = grid(m, n), c = g.map(function (k) { return 0.3 * res(k); });
      for (var it = 0; it < 1500; it++) {
        var cn = new Array(n), d = 0;
        for (var a = 0; a < n; a++) {
          var R = res(g[a]), lo = 1e-6, hi = R - 1e-6;
          for (var s = 0; s < 40; s++) {
            var mid = 0.5 * (lo + hi), kp = R - mid;
            var rhs = m.beta * Math.pow(Math.max(interp(g, c, kp), 1e-8), -m.g) * mpk(kp);
            if (Math.pow(mid, -m.g) > rhs) { lo = mid; } else { hi = mid; }
          }
          cn[a] = 0.5 * (lo + hi);
          d = Math.max(d, Math.abs(cn[a] - c[a]));
        }
        c = cn;
        if (d < 1e-9) { break; }
      }
      return { g: g, c: c };
    }
    function euler(m, cf) {
      var ks = [], es = [], worst = -20;
      for (var i = 0; i <= 120; i++) {
        var k = m.kss * (0.6 + 0.8 * i / 120), c = cf(k), kp = res(k) - c;
        var e = Math.abs(1 - Math.pow(m.beta * Math.pow(cf(kp), -m.g) * mpk(kp), -1 / m.g) / c);
        var le = Math.log10(Math.max(e, 1e-12));
        ks.push(k / m.kss); es.push(le); worst = Math.max(worst, le);
      }
      return { k: ks, e: es, worst: worst };
    }
    QB.widget(el, {
      title: "Solver",
      sub: "You choose the grid. Left: next year's capital against this year's, from value iteration on your grid " +
           "(blue staircase) and from an accurate rule (white). Right: the Euler-equation errors of each, in log10.",
      panels: 2, height: 260,
      controls: [
        { k: "n", label: "Grid points", min: 10, max: 400, step: 10, value: 30,
          fmt: function (x) { return x.toFixed(0); } },
        { k: "beta", label: "Discount factor", min: 0.9, max: 0.99, step: 0.01, value: 0.96,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "g", label: "Curvature of utility (1 / EIS)", min: 1, max: 5, step: 0.5, value: 2,
          fmt: function (x) { return x.toFixed(1); } },
      ],
      draw: function (g, v, st) {
        var m = model(v.beta, v.g);
        var key = v.beta.toFixed(2) + "," + v.g.toFixed(1);
        st.acc = st.acc || {};
        if (!st.acc[key]) { st.acc[key] = accurate(m); }
        var r = vfi(m, Math.round(v.n)), acc = st.acc[key];
        var cg = function (k) { return res(k) - interp(r.g, r.kp, k); };
        var ca = function (k) { return interp(acc.g, acc.c, k); };
        var eg = euler(m, cg), ea = euler(m, ca);
        var best = 0, bd = Infinity;
        for (var i = 0; i < r.g.length; i++) {
          var d = Math.abs(r.kp[i] - r.g[i]);
          if (d < bd) { bd = d; best = i; }
        }
        st.rounds = r.rounds; st.ss = r.g[best] / m.kss; st.worst = eg.worst; st.worstAcc = ea.worst;
        var xs = r.g.map(function (k) { return k / m.kss; }), ys = r.kp.map(function (k) { return k / m.kss; });
        var ax = acc.g.map(function (k) { return k / m.kss; });
        var ay = acc.g.map(function (k, i) { return (res(k) - acc.c[i]) / m.kss; });
        var L = g[0].axes({ x: [0.5, 1.5], y: [0.5, 1.5], title: "next year's capital / steady state",
                            xlabel: "this year's capital / steady state" });
        L.line([0.5, 1.5], [0.5, 1.5], { color: "#6B7280", dash: [4, 4], width: 1 });
        L.line(ax, ay, { color: "#FFFFFF", width: 1.6 });
        var sx = [], sy = [];
        for (var q = 0; q < xs.length; q++) {
          sx.push(xs[q]); sy.push(ys[q]);
          if (q + 1 < xs.length) { sx.push(xs[q + 1]); sy.push(ys[q]); }
        }
        L.line(sx, sy, { color: "#7EC8F5", width: 2.2 });
        var R = g[1].axes({ x: [0.6, 1.4], y: [-8, 0], title: "Euler error, log10", xlabel: "capital / steady state" });
        R.line(ea.k, ea.e, { color: "#FFFFFF", width: 1.4 });
        R.line(eg.k, eg.e, { color: "#7EC8F5", width: 1.8 });
      },
      readout: function (v, st) {
        return [["rounds of value iteration", st.rounds.toFixed(0)],
                ["steady state on your grid", (100 * (st.ss - 1)).toFixed(1) + "% from the true"],
                ["worst Euler error, your grid", "10^" + st.worst.toFixed(1) + " (one dollar in " +
                 Math.round(Math.pow(10, -st.worst)).toLocaleString("en-US") + ")"],
                ["worst Euler error, accurate rule", "10^" + st.worstAcc.toFixed(1)]];
      },
      note: "Part 51, chapters 1 to 3 and 8. Finer grids cost the square of their size in work and buy roughly " +
            "proportional accuracy; patience (a higher discount factor) costs rounds. Computed in your browser; " +
            "nothing you do here is stored or sent.",
    });
  };
})();
