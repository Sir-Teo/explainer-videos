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
  // ---- Part 52: many agents ----------------------------------------------------------------------------------------
  W.households = function (el) {
    // Agora's many agents (explainer.economics.agora.hetero), smaller: a one-asset household block, quarterly, log
    // utility, a three-state Rouwenhorst chain for log income (persistence 0.966, s.d. 0.5), no borrowing, 70 asset
    // points; output 1, the real rate 0.5%, government bonds B (the households' only asset), taxes r B, and the
    // discount factor that makes households hold exactly B.  Jacobians over 80 quarters by the fake-news algorithm.
    var R0 = 0.005, NA = 70, NE = 3, T = 80, RHO = 0.966, SD = 0.5, H = 1e-4;
    var p = (1 + RHO) / 2, q = 1 - p;
    var P = [[p * p, 2 * p * q, q * q], [p * q, p * p + q * q, p * q], [q * q, 2 * p * q, p * p]];
    var psi = Math.sqrt(2) * SD, PI = [0.25, 0.5, 0.25];
    var e = [Math.exp(-psi), 1, Math.exp(psi)];
    var em = PI[0] * e[0] + PI[1] * e[1] + PI[2] * e[2];
    e = e.map(function (x) { return x / em; });
    function grid(B) {
      var amax = Math.max(60, 25 * B), a = new Float64Array(NA);
      for (var i = 0; i < NA; i++) { a[i] = amax * Math.pow(i / (NA - 1), 3); }
      return a;
    }
    function step(a, cN, rN, rNow, Z, beta) {
      // one backward step of the endogenous grid method: tomorrow's rule and return, today's return and income
      var c = new Float64Array(NA * NE), ap = new Float64Array(NA * NE);
      var cE = new Float64Array(NA), aE = new Float64Array(NA);
      for (var s = 0; s < NE; s++) {
        for (var i = 0; i < NA; i++) {
          var emu = 0;
          for (var t = 0; t < NE; t++) { emu += P[s][t] / cN[i * NE + t]; }
          cE[i] = 1 / (beta * (1 + rN) * emu);
          aE[i] = (cE[i] + a[i] - Z * e[s]) / (1 + rNow);
        }
        var k = 0;
        for (var j = 0; j < NA; j++) {
          var x = a[j], cc;
          if (x < aE[0]) { cc = (1 + rNow) * x + Z * e[s]; } else {
            while (k < NA - 2 && aE[k + 1] < x) { k++; }
            cc = cE[k] + (cE[k + 1] - cE[k]) * (x - aE[k]) / (aE[k + 1] - aE[k]);
          }
          c[j * NE + s] = cc;
          ap[j * NE + s] = Math.max((1 + rNow) * x + Z * e[s] - cc, 0);
        }
      }
      return { c: c, ap: ap };
    }
    function lottery(a, ap) {
      var idx = new Int32Array(NA * NE), w = new Float64Array(NA * NE);
      for (var m = 0; m < NA * NE; m++) {
        var x = ap[m], lo = 0, hi = NA - 1;
        if (x >= a[NA - 1]) { idx[m] = NA - 2; w[m] = 1; continue; }
        while (hi - lo > 1) { var mid = (lo + hi) >> 1; if (a[mid] <= x) { lo = mid; } else { hi = mid; } }
        idx[m] = lo; w[m] = Math.min(Math.max((x - a[lo]) / (a[lo + 1] - a[lo]), 0), 1);
      }
      return { idx: idx, w: w };
    }
    function forward(D, L) {
      var Dn = new Float64Array(NA * NE), out = new Float64Array(NA * NE);
      for (var m = 0; m < NA * NE; m++) {
        var s = m % NE, i = L.idx[m];
        Dn[i * NE + s] += D[m] * (1 - L.w[m]);
        Dn[(i + 1) * NE + s] += D[m] * L.w[m];
      }
      for (var j = 0; j < NA; j++) {
        for (var t = 0; t < NE; t++) {
          var v = 0;
          for (var u = 0; u < NE; u++) { v += Dn[j * NE + u] * P[u][t]; }
          out[j * NE + t] = v;
        }
      }
      return out;
    }
    function expect(X, L) {
      var out = new Float64Array(NA * NE);
      for (var m = 0; m < NA * NE; m++) {
        var s = m % NE, i = L.idx[m], v0 = 0, v1 = 0;
        for (var t = 0; t < NE; t++) { v0 += P[s][t] * X[i * NE + t]; v1 += P[s][t] * X[(i + 1) * NE + t]; }
        out[m] = (1 - L.w[m]) * v0 + L.w[m] * v1;
      }
      return out;
    }
    function dot(x, y) { var s = 0; for (var i = 0; i < x.length; i++) { s += x[i] * y[i]; } return s; }
    function steady(B) {
      var a = grid(B), Z = 1 - R0 * B, lo = 0.85, hi = 1 / (1 + R0) - 1e-7, beta, c, ap, D, res;
      c = new Float64Array(NA * NE);
      for (var m = 0; m < NA * NE; m++) { c[m] = 0.1 * a[Math.floor(m / NE)] + Z * e[m % NE]; }
      D = new Float64Array(NA * NE);
      for (m = 0; m < NA * NE; m++) { D[m] = PI[m % NE] / NA; }
      for (var it = 0; it < 30; it++) {
        beta = 0.5 * (lo + hi);
        for (var k = 0; k < 3000; k++) {
          res = step(a, c, R0, R0, Z, beta);
          var d = 0;
          for (m = 0; m < NA * NE; m++) { d = Math.max(d, Math.abs(res.c[m] - c[m])); }
          c = res.c;
          if (d < 1e-9) { break; }
        }
        ap = res.ap;
        var L = lottery(a, ap);
        for (k = 0; k < 6000; k++) {
          var Dn = forward(D, L), dd = 0;
          for (m = 0; m < NA * NE; m++) { dd = Math.max(dd, Math.abs(Dn[m] - D[m])); }
          D = Dn;
          if (dd < 1e-12) { break; }
        }
        if (dot(D, ap) > B) { hi = beta; } else { lo = beta; }
      }
      var mpc = 0, lim = 0;
      for (m = 0; m < NA * NE; m++) {
        var i = Math.floor(m / NE), s = m % NE, x = a[i] + 0.01 / (1 + R0), k2 = 0;
        while (k2 < NA - 2 && a[k2 + 1] < x) { k2++; }
        var cx = c[k2 * NE + s] + (c[(k2 + 1) * NE + s] - c[k2 * NE + s]) * (x - a[k2]) / (a[k2 + 1] - a[k2]);
        mpc += D[m] * (cx - c[m]) / 0.01;
        if (i === 0) { lim += D[m]; }
      }
      return { a: a, Z: Z, B: B, beta: beta, c: c, ap: ap, D: D, mpc: mpc, lim: lim };
    }
    function jacobians(ss) {
      var a = ss.a, L = lottery(a, ss.ap), D1 = forward(ss.D, L), E = { C: [ss.c], A: [ss.ap] }, J = {};
      for (var t = 1; t < T - 1; t++) { E.C.push(expect(E.C[t - 1], L)); E.A.push(expect(E.A[t - 1], L)); }
      ["r", "Z"].forEach(function (inp) {
        var Y = { C: new Float64Array(T), A: new Float64Array(T) }, Dc = [], cp = null;
        for (var u = 0; u < T; u++) {
          var r;
          if (u === 0) { r = inp === "r" ? step(a, ss.c, R0, R0 + H, ss.Z, ss.beta) : step(a, ss.c, R0, R0, ss.Z + H, ss.beta); }
          else if (u === 1 && inp === "r") { r = step(a, cp, R0 + H, R0, ss.Z, ss.beta); }
          else { r = step(a, cp, R0, R0, ss.Z, ss.beta); }
          cp = r.c;
          var yc = 0, ya = 0;
          for (var m = 0; m < NA * NE; m++) { yc += ss.D[m] * (r.c[m] - ss.c[m]); ya += ss.D[m] * (r.ap[m] - ss.ap[m]); }
          Y.C[u] = yc / H; Y.A[u] = ya / H;
          var Dn = forward(ss.D, lottery(a, r.ap));
          for (m = 0; m < NA * NE; m++) { Dn[m] = (Dn[m] - D1[m]) / H; }
          Dc.push(Dn);
        }
        ["C", "A"].forEach(function (o) {
          var M = [];
          for (var t = 0; t < T; t++) {
            var row = new Float64Array(T);
            for (var s = 0; s < T; s++) { row[s] = t === 0 ? Y[o][s] : dot(E[o][t - 1], Dc[s]); }
            if (t > 0) { for (s = 1; s < T; s++) { row[s] += M[t - 1][s - 1]; } }
            M.push(row);
          }
          J[o + inp] = M;
        });
      });
      return J;
    }
    function solve(M, b) { // Gaussian elimination with partial pivoting
      var n = b.length, A = M.map(function (r) { return Array.prototype.slice.call(r); }), x = b.slice();
      for (var k = 0; k < n; k++) {
        var piv = k;
        for (var i = k + 1; i < n; i++) { if (Math.abs(A[i][k]) > Math.abs(A[piv][k])) { piv = i; } }
        var tmp = A[k]; A[k] = A[piv]; A[piv] = tmp; var tb = x[k]; x[k] = x[piv]; x[piv] = tb;
        for (i = k + 1; i < n; i++) {
          var f = A[i][k] / A[k][k];
          if (f === 0) { continue; }
          for (var j = k; j < n; j++) { A[i][j] -= f * A[k][j]; }
          x[i] -= f * x[k];
        }
      }
      for (k = n - 1; k >= 0; k--) {
        var s = x[k];
        for (j = k + 1; j < n; j++) { s -= A[k][j] * x[j]; }
        x[k] = s / A[k][k];
      }
      return x;
    }
    function mv(M, x) { return M.map(function (r) { return dot(r, x); }); }
    function experiment(B) {
      var ss = steady(B), J = jacobians(ss), dr = new Array(T).fill(0), dG = [], dT = [], dBd = [], prev = 0;
      for (var t = 1; t < T; t++) { dr[t] = -0.0025 * Math.pow(0.7, t - 1); }
      var rhs = mv(J.Ar, dr).map(function (x) { return -x; }), dZ = solve(J.AZ, rhs);
      var direct = mv(J.Cr, dr), indirect = mv(J.CZ, dZ);
      for (t = 0; t < T; t++) {
        dG.push(0.01 * Math.pow(0.8, t));
        dT.push(0.1 * prev);
        dBd.push((1 + R0) * prev + dG[t] - dT[t]);
        prev = dBd[t];
      }
      var dZd = solve(J.AZ, dBd), num = 0, den = 0;
      for (t = 0; t < T; t++) { var qd = Math.pow(1 + R0, -t); num += qd * (dZd[t] + dT[t]); den += qd * dG[t]; }
      var ra = 0;
      for (t = 1; t < T; t++) { ra -= dr[t] / (1 + R0); }
      var qs = 0;
      for (t = 0; t < T; t++) { qs += Math.pow(1 + R0, -t) * dr[t]; }
      var raDirect = (R0 * B - 1) / (1 + R0) * qs;
      var impc = [];
      for (t = 0; t < 16; t++) { impc.push(J.CZ[t][0]); }
      return { ss: ss, direct: direct, indirect: indirect, mult: num / den, ra: ra, raShare: raDirect / ra,
               impc: impc };
    }
    QB.widget(el, {
      title: "Households",
      sub: "You choose how much liquid wealth households hold. Left: the central bank cuts the real rate by a quarter " +
           "point, fading over a year; spending (white) split into the direct effect of the rate (blue) and the " +
           "indirect effect through incomes (gold), against one representative household (dashed). Right: how a " +
           "one-off rise in income is spent, quarter by quarter.",
      panels: 2, height: 260,
      controls: [
        { k: "lw", label: "Liquid wealth (quarters of output)", min: 0, max: 4, step: 1, value: 2,
          fmt: function (x) { return Math.pow(2, x).toFixed(0); } },
      ],
      draw: function (g, v, st) {
        var B = Math.pow(2, Math.round(v.lw));
        st.cache = st.cache || {};
        if (!st.cache[B]) { st.cache[B] = experiment(B); }
        var x = st.cache[B], qs = [], tot = [], dr = [], ind = [], ra = [];
        for (var t = 0; t < 16; t++) {
          qs.push(t); dr.push(100 * x.direct[t]); ind.push(100 * x.indirect[t]);
          tot.push(100 * (x.direct[t] + x.indirect[t]));
          ra.push(t === 0 ? 100 * x.ra : 100 * x.ra * Math.pow(0.7, t));
        }
        st.x = x;
        var L = g[0].axes({ x: [0, 15], y: [-0.2, 1.0], title: "spending, % of output", xlabel: "quarters" });
        L.hline(0);
        L.line(qs, ra, { color: "#9CA3AF", dash: [5, 4], width: 1.4 });
        L.line(qs, tot, { color: "#FFFFFF", width: 2.2 });
        L.line(qs, dr, { color: "#7EC8F5", width: 1.8 });
        L.line(qs, ind, { color: "#F2C14E", width: 1.8 });
        var R = g[1].axes({ x: [-0.5, 15.5], y: [0, 0.6], title: "share of a one-off income spent", xlabel: "quarter" });
        R.bars(qs, x.impc, 0.7, { color: "#7FD1B9" });
      },
      readout: function (v, st) {
        var x = st.x;
        var share0 = x.direct[0] / (x.direct[0] + x.indirect[0]);
        var s4 = 0, t4 = 0;
        for (var t = 0; t < 4; t++) { s4 += x.direct[t]; t4 += x.direct[t] + x.indirect[t]; }
        return [["spent of a windfall, first quarter", QB.pct(x.ss.mpc, 0)],
                ["at the borrowing limit", QB.pct(x.ss.lim, 0)],
                ["direct share: first quarter, first year", QB.pct(share0, 0) + ", " + QB.pct(s4 / t4, 0)],
                ["one household's direct share", QB.pct(x.raShare, 0)],
                ["deficit-financed multiplier", x.mult.toFixed(2)]];
      },
      note: "Part 52, chapters 9 to 11. The less liquid wealth, the more of the extra spending comes through incomes " +
            "and the larger the multiplier; the total barely changes. A smaller model than the film's (3 income " +
            "states, 70 points, 80 quarters), so its numbers differ slightly. Computed in your browser; nothing you " +
            "do here is stored or sent.",
    });
  };
  // ---- Part 53: information and persuasion --------------------------------------------------------------------
  W.persuade = function (el) {
    // Agora's information and persuasion (explainer.economics.agora.persuade): Kamenica and Gentzkow's prosecutor.
    // The investigation flags every guilty defendant and a share p of the innocent; the judge, who knows the prior
    // and the design, convicts a flagged defendant when Pr(guilty | flag) >= the threshold, and acquits otherwise.
    QB.widget(el, {
      title: "Persuade",
      sub: "You design the investigation. Left: the judge's belief in guilt after a flag (purple) and the share of " +
           "defendants convicted (gold) as the share of innocent defendants flagged varies; your design is the " +
           "dot. Right: what the prosecutor gets at each belief, its concave closure, and the prior.",
      panels: 2, height: 260,
      controls: [
        { k: "prior", label: "Share guilty (the prior)", min: 0.05, max: 0.95, step: 0.05, value: 0.3,
          fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "thr", label: "Judge's standard of proof", min: 0.2, max: 0.9, step: 0.05, value: 0.5,
          fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "p", label: "Innocent defendants flagged", min: 0, max: 1, step: 0.01, value: 0.2,
          fmt: function (x) { return Math.round(100 * x) + "%"; } },
      ],
      draw: function (g, v, st) {
        var pr = v.prior, t = v.thr;
        function post(p) { return pr / (pr + (1 - pr) * p); }
        function conv(p) {
          if (pr >= t) { return 1; }
          return post(p) >= t - 1e-12 ? pr + (1 - pr) * p : 0;
        }
        var ps = [], cs = [], bs = [];
        for (var i = 0; i <= 200; i++) { var p = i / 200; ps.push(p); cs.push(conv(p)); bs.push(post(p)); }
        var L = g[0].axes({ x: [0, 1], y: [0, 1], title: "after a flag", xlabel: "share of innocent flagged" });
        L.hline(t, { color: "#7EC8F5" });
        L.line(ps, bs, { color: "#C9A0FF", width: 1.6 });
        L.line(ps, cs, { color: "#F2C14E", width: 2.2 });
        L.dots([v.p], [conv(v.p)], { color: "#FFFFFF", r: 4 });
        var mu = [], val = [], cav = [];
        for (var j = 0; j <= 200; j++) {
          var m = j / 200; mu.push(m); val.push(m >= t ? 1 : 0); cav.push(Math.min(1, m / t));
        }
        var R = g[1].axes({ x: [0, 1], y: [0, 1.05], title: "the prosecutor's value", xlabel: "the judge's belief" });
        R.line(mu, val, { color: "#F2C14E", width: 2 });
        R.line(mu, cav, { color: "#C9A0FF", width: 2, dash: [5, 4] });
        R.vline(pr, { color: "#FFFFFF" });
        st.post = post(v.p); st.conv = conv(v.p);
        st.best = pr >= t ? 1 : pr / t;
        st.pbest = pr >= t ? 1 : pr * (1 - t) / (t * (1 - pr));
      },
      readout: function (v, st) {
        return [["judge's belief after a flag", QB.pct(st.post, 0)],
                ["convicted, your design", QB.pct(st.conv, 0)],
                ["the best design flags", QB.pct(st.pbest, 0) + " of the innocent"],
                ["convicted, best design", QB.pct(st.best, 0) + " (prior / standard)"]];
      },
      note: "Part 53, chapters 1 and 5. The best investigation leaves the judge exactly at the standard after a " +
            "flag; one step further and the flag stops working. Computed in your browser; nothing you do here is " +
            "stored or sent.",
    });
  };
})();
