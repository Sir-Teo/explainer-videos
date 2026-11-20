// Interactives for Act VIII, Work and the State (Parts 38-42).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var W = QB.W;
  var GOLD = "#F6C453", RED = "#F25F5C", TEAL = "#7FD1B9", VIOLET = "#C9A0FF";

  // ---- Part 38: work and wages ---------------------------------------------------------------------------------
  W.minimum = function (el) {
    // A firm facing labour supply L = 200 (w/6)^eta and a marginal product 6 (L/200)^-0.3, so that a competitive
    // market would pay $6 and hire 200 (explainer.economics.agora.labour: monopsony, floor_monopsony).  The firm
    // hires where the marginal cost of labour, w (1 + 1/eta), meets the marginal product; a minimum wage between its
    // own wage and $6 raises employment, above $6 it lowers it.
    var B = 0.3, WC = 6, LC = 200;
    function supplyL(w, eta) { return LC * Math.pow(w / WC, eta); }
    function demandL(w) { return LC * Math.pow(w / WC, -1 / B); }
    function mono(eta) {
      var L = LC * Math.pow(eta / (1 + eta), 1 / (1 / eta + B));
      return { L: L, w: WC * Math.pow(L / LC, 1 / eta) };
    }
    function employ(m, eta) {
      var M = mono(eta);
      if (m <= M.w) return M.L;
      return Math.min(supplyL(m, eta), demandL(m));
    }
    function f2(x) { return x.toFixed(2); }
    QB.widget(el, {
      title: "A minimum wage at a firm that sets wages",
      sub: "Left: the firm's supply of workers (teal), the cost of one more worker (violet), what one more " +
           "adds (red) and your minimum (gold). Right: workers hired against the minimum wage, with yours marked.",
      panels: 2, height: 270,
      controls: [
        { k: "m", label: "Minimum wage, $ an hour", min: 3.5, max: 8, step: 0.05, value: 5.5, fmt: f2 },
        { k: "eta", label: "Supply elasticity facing the firm (large = competitive)", min: 1, max: 20, step: 0.5,
          value: 3, fmt: function (x) { return x.toFixed(1); } },
      ],
      draw: function (g, v, st) {
        var Ls = [], ws = [], mcl = [], mrp = [], k;
        for (k = 0; k <= 60; k++) {
          var L = 40 + 280 * k / 60;
          var w = WC * Math.pow(L / LC, 1 / v.eta);
          Ls.push(L); ws.push(w); mcl.push(w * (1 + 1 / v.eta)); mrp.push(WC * Math.pow(L / LC, -B));
        }
        var a = g[0].axes({ x: [40, 320], y: [3, 9], title: "the firm's labour market", xlabel: "workers" });
        a.line(Ls, ws.map(function (w) { return Math.min(w, 9); }), { color: TEAL, width: 2.5 });
        a.line(Ls, mcl.map(function (w) { return Math.min(w, 9); }), { color: VIOLET, width: 2.5 });
        a.line(Ls, mrp.map(function (w) { return Math.min(w, 9); }), { color: RED, width: 2.5 });
        a.hline(v.m, { color: GOLD });
        var M = mono(v.eta), now = employ(v.m, v.eta);
        a.dots([M.L], [M.w], { color: VIOLET, r: 5 });
        var ms = [], es = [];
        for (k = 0; k <= 80; k++) { var mm = 3.5 + 4.5 * k / 80; ms.push(mm); es.push(employ(mm, v.eta)); }
        var b = g[1].axes({ x: [3.5, 8], y: [0, 260], title: "workers hired", xlabel: "minimum wage, $" });
        b.line(ms, es.map(function (e) { return Math.min(e, 260); }), { color: GOLD, width: 2.5 });
        b.dots([v.m], [Math.min(now, 260)], { color: GOLD, r: 6 });
        st.M = M; st.now = now;
      },
      readout: function (v, st) {
        return [["the firm's own wage and hiring", "$" + st.M.w.toFixed(2) + ", " + st.M.L.toFixed(0) + " workers"],
                ["hiring at your minimum", st.now.toFixed(0) + " (" + (100 * (st.now / st.M.L - 1)).toFixed(0) +
                  "% against no minimum)"],
                ["the markdown below what a worker adds", (100 / (1 + v.eta)).toFixed(0) + "%"]];
      },
      note: "The model of Part 38, chapter 7. A minimum between the firm's wage and the competitive $6 raises " +
            "employment; above $6 it lowers it. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 39: the wage structure -----------------------------------------------------------------------------
  W.race = function (el) {
    // The canonical model (explainer.economics.agora.labour: skill_premium, implied_demand): ln(premium) =
    // D - S / sigma, with relative demand D and relative supply S growing at the reader's rates, against the
    // college premium the BLS measured, 1979-2025 (median weekly earnings, bachelor's and higher over high school).
    var BLS = [1.382, 1.414, 1.423, 1.45, 1.482, 1.505, 1.52, 1.526, 1.584, 1.59, 1.624, 1.653, 1.678, 1.727, 1.723,
               1.741, 1.729, 1.711, 1.69, 1.714, 1.755, 1.764, 1.771, 1.759, 1.74, 1.718, 1.738, 1.746, 1.775, 1.804,
               1.816, 1.827, 1.803, 1.787, 1.834, 1.786, 1.814, 1.819, 1.796, 1.814, 1.832, 1.819, 1.795, 1.81, 1.79,
               1.819, 1.801];
    var Y0 = 1979;
    function pct(x) { return x.toFixed(1) + "%"; }
    QB.widget(el, {
      title: "The race between education and technology",
      sub: "Left: the college premium your settings produce (gold) against the one measured (dots). Right: this " +
           "year's market for skill: supply (teal) and demand (red), moving at your rates.",
      panels: 2, height: 270,
      controls: [
        { k: "sigma", label: "Elasticity of substitution, sigma", min: 1, max: 4, step: 0.05, value: 1.41,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "d1", label: "Demand growth before 1992, % a year", min: 0, max: 6, step: 0.1, value: 3.5, fmt: pct },
        { k: "d2", label: "Demand growth after 1992, % a year", min: 0, max: 6, step: 0.1, value: 2.0, fmt: pct },
        { k: "s", label: "Supply growth, % a year", min: 0, max: 6, step: 0.1, value: 2.7, fmt: pct },
        { k: "yr", label: "Year shown on the right", min: 1979, max: 2025, step: 1, value: 2000,
          fmt: function (x) { return x.toFixed(0); } },
      ],
      draw: function (g, v, st) {
        var ys = [], pm = [], k;
        var p0 = Math.log(BLS[0]);
        for (k = 0; k <= 46; k++) {
          var t = Y0 + k;
          var D = (Math.min(t, 1992) - Y0) * v.d1 / 100 + Math.max(t - 1992, 0) * v.d2 / 100;
          var S = k * v.s / 100;
          ys.push(t); pm.push(Math.exp(p0 + D - S / v.sigma));
        }
        var a = g[0].axes({ x: [1978, 2026], y: [1.0, 2.6], title: "college premium", xlabel: "year" });
        a.dots(ys, BLS, { color: "#9AA3B2", r: 2.5 });
        a.line(ys, pm, { color: "#F2C14E", width: 2.5 });
        var j = v.yr - Y0;
        a.vline(v.yr, {});
        var Dj = (Math.min(v.yr, 1992) - Y0) * v.d1 / 100 + Math.max(v.yr - 1992, 0) * v.d2 / 100;
        var Sj = j * v.s / 100;
        var b = g[1].axes({ x: [-0.2, 1.6], y: [0, 1.2], title: "log premium against log relative supply",
                            xlabel: "relative supply (log, from 1979)" });
        var xs = [], dl = [];
        for (k = 0; k <= 40; k++) { var x = -0.2 + 1.8 * k / 40; xs.push(x); dl.push(p0 + Dj - x / v.sigma); }
        b.line(xs, dl, { color: "#F25F5C", width: 2.5 });
        b.vline(Sj, { color: "#7FD1B9", width: 2.5, dash: [] });
        b.dots([Sj], [p0 + Dj - Sj / v.sigma], { color: "#F2C14E", r: 5 });
        var err = 0;
        for (k = 0; k <= 46; k++) { err += Math.pow(Math.log(pm[k]) - Math.log(BLS[k]), 2); }
        st.rmse = Math.sqrt(err / 47); st.p2025 = pm[46]; st.pyr = pm[j];
      },
      readout: function (v, st) {
        return [["premium in " + v.yr + ", your model", st.pyr.toFixed(2)],
                ["premium in 2025: your model, measured", st.p2025.toFixed(2) + ", 1.80"],
                ["fit to 1979-2025 (root mean square error in logs)", st.rmse.toFixed(3)]];
      },
      note: "Part 39, chapter 2. Supply pulls the premium down by its growth over sigma; demand pushes it up. " +
            "Measured supply grew about 2.7% a year after 1992. Computed in your browser; nothing you do here is " +
            "stored or sent.",
    });
  };
  W.tail = function (el) {
    // Random growth (explainer.economics.agora.distribution: simulate_growth, zeta): log income takes a random
    // step each year (drift nu, volatility sigma), never falls below a floor at a third of the starting income,
    // and careers end at rate delta and restart at 1. The tail of the stationary distribution is Pareto with
    // exponent zeta = (-nu + sqrt(nu^2 + 2 sigma^2 delta)) / sigma^2.
    var N = 4000, YEARS = 300, FLOOR = Math.log(1 / 3);
    function zeta(nu, s, d) { return (-nu + Math.sqrt(nu * nu + 2 * s * s * d)) / (s * s); }
    QB.widget(el, {
      title: "Where long tails come from",
      sub: "Left: the share of careers above each income (log scales), simulated (dots) and the theory's slope " +
           "(gold). Right: the Lorenz curve of the same incomes.",
      panels: 2, height: 270,
      controls: [
        { k: "sigma", label: "Volatility of yearly income growth, %", min: 4, max: 25, step: 0.5, value: 14.4,
          fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "life", label: "Average career length, years (1 / delta)", min: 10, max: 80, step: 1, value: 40,
          fmt: function (x) { return x.toFixed(0); } },
        { k: "nu", label: "Average growth of log income, % a year", min: -3, max: 3, step: 0.1, value: 0,
          fmt: function (x) { return x.toFixed(1) + "%"; } },
      ],
      draw: function (g, v, st) {
        var s = v.sigma / 100, d = 1 / v.life, nu = v.nu / 100, r = QB.rng(40), y = [], i, t;
        for (i = 0; i < N; i++) y.push(0);
        for (t = 0; t < YEARS; t++) {
          for (i = 0; i < N; i++) {
            if (r() < d) { y[i] = 0; continue; }
            y[i] = Math.max(y[i] + nu + s * r.normal(), FLOOR);
          }
        }
        var x = y.map(Math.exp).sort(function (a, b) { return a - b; });
        var tot = 0; for (i = 0; i < N; i++) tot += x[i];
        var gx = [], gs = [], k;
        for (k = 0; k < 40; k++) {
          var q = 1 - Math.pow(10, -3 * k / 39);   // from the median-ish to the top 0.1%
          var j = Math.min(N - 2, Math.floor(q * N));
          if (x[j] >= 1) { gx.push(x[j]); gs.push(1 - (j + 1) / N); }
        }
        var z = zeta(nu, s, d);
        var a = g[0].axes({ x: [1, 1000], y: [0.0005, 1], logx: true, logy: true, title: "share above",
                            xlabel: "income (start = 1)" });
        a.dots(gx, gs, { color: "#7EC8F5", r: 2.5 });
        if (gx.length > 1 && z > 0) {
          var x0 = gx[0], s0 = gs[0], tx = [], ty = [];
          for (k = 0; k <= 20; k++) { var xx = x0 * Math.pow(1000 / x0, k / 20); tx.push(xx); ty.push(s0 * Math.pow(xx / x0, -z)); }
          a.line(tx, ty, { color: "#F2C14E", width: 2.5 });
        }
        var px = [0], py = [0], cum = 0;
        for (i = 0; i < N; i++) { cum += x[i]; if (i % 40 === 39 || i === N - 1) { px.push((i + 1) / N); py.push(cum / tot); } }
        var b = g[1].axes({ x: [0, 1], y: [0, 1], title: "share of income", xlabel: "share of people, poorest first" });
        b.line([0, 1], [0, 1], { color: "#9AA3B2", width: 1, dash: [4, 4] });
        b.line(px, py, { color: "#F2C14E", width: 2.5 });
        var area = 0;
        for (k = 1; k < px.length; k++) area += (px[k] - px[k - 1]) * (py[k] + py[k - 1]) / 2;
        var top = 0; for (i = Math.floor(0.99 * N); i < N; i++) top += x[i];
        st.z = z; st.gini = 1 - 2 * area; st.top1 = top / tot;
      },
      readout: function (v, st) {
        return [["Pareto exponent of the tail (theory)", st.z.toFixed(2) + (st.z <= 1 ? ": no finite mean" : "")],
                ["top 1% share, simulated", (100 * st.top1).toFixed(1) + "%"],
                ["Gini, simulated", st.gini.toFixed(3)]];
      },
      note: "Part 40, chapter 4. More volatile incomes, faster growth or longer careers fatten the tail (a lower " +
            "exponent, a larger top share). 4,000 careers, 300 years, computed in your browser; nothing you do " +
            "here is stored or sent.",
    });
  };
})();
