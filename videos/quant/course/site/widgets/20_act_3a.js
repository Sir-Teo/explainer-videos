// Interactives for Act III, first half (Parts 9-15).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, pct = QB.pct;

  // ---- Part 9: replication on a tree, and when it becomes an arbitrage ----------------------------------------------
  W.tree = function (el) {
    QB.widget(el, {
      title: "Price by replication on a tree",
      sub: "A call struck at 100 on a four-step tree. Each node's value is the cost of the stock-and-cash portfolio that matches the two nodes after it. Push the interest rate outside the range of the two moves and the tree offers free money.",
      panels: 2, weights: [1.6, 1], height: 320,
      controls: [
        { k: "u", label: "Up move per step", min: 2, max: 30, step: 1, value: 12, fmt: function (x) { return "+" + x + "%"; } },
        { k: "d", label: "Down move per step", min: 2, max: 30, step: 1, value: 10, fmt: function (x) { return "−" + x + "%"; } },
        { k: "r", label: "Interest per step", min: -8, max: 20, step: 0.5, value: 1, fmt: function (x) { return x.toFixed(1) + "%"; } },
      ],
      draw: function (g, v, s) {
        var u = 1 + v.u / 100, d = 1 - v.d / 100, R = 1 + v.r / 100, q = (R - d) / (u - d), n = 4, K = 100, i, j, S = [], V = [];
        for (i = 0; i <= n; i++) { S.push([]); V.push([]); for (j = 0; j <= i; j++) S[i].push(100 * Math.pow(u, j) * Math.pow(d, i - j)); }
        for (j = 0; j <= n; j++) V[n][j] = Math.max(S[n][j] - K, 0);
        for (i = n - 1; i >= 0; i--) for (j = 0; j <= i; j++) V[i][j] = (q * V[i + 1][j + 1] + (1 - q) * V[i + 1][j]) / R;
        var delta = (V[1][1] - V[1][0]) / (S[1][1] - S[1][0]), bond = V[0][0] - delta * 100, ok = q > 0 && q < 1;
        s.out = [q, V[0][0], delta, bond, ok];
        var lo = S[n][0] * 0.9, hi = S[n][n] * 1.1, a = g[0].axes({ x: [-0.3, n + 0.5], y: [lo, hi], logy: true, title: "Stock price (grey) and option value (colour) at each node", xlabel: "step", yticks: [], noY: true });
        for (i = 0; i < n; i++) for (j = 0; j <= i; j++) { a.line([i, i + 1], [S[i][j], S[i + 1][j + 1]], { color: C.line, width: 1.2 }); a.line([i, i + 1], [S[i][j], S[i + 1][j]], { color: C.line, width: 1.2 }); }
        for (i = 0; i <= n; i++) for (j = 0; j <= i; j++) {
          a.dots([i], [S[i][j]], { color: V[i][j] > 1e-9 ? C.option : C.cash, r: 4 });
          a.text(i, S[i][j], fmt(S[i][j], 0), { color: C.muted, size: 10.5, dx: 7, dy: -8 });
          a.text(i, S[i][j], fmt(V[i][j], 2), { color: ok ? C.option : C.loss, size: 11.5, bold: true, dx: 7, dy: 6 });
        }
        var b = g[1].axes({ x: [0.6, 1.4], y: [0, 1], title: "One step: where growth at the riskless rate falls", noY: true, yticks: [], xfmt: function (x) { return (x >= 1 ? "+" : "−") + Math.abs(100 * (x - 1)).toFixed(0) + "%"; } });
        b.area([d, u], [0.62, 0.62], 0.38, { color: ok ? C.gain : C.loss, alpha: 0.25 });
        b.vline(d, { color: C.loss, dash: null }); b.vline(u, { color: C.gain, dash: null }); b.vline(R, { color: C.p, dash: null, width: 2.5 });
        b.text(d, 0.7, "down", { color: C.loss, align: "center", bg: true }); b.text(u, 0.7, "up", { color: C.gain, align: "center", bg: true }); b.text(R, 0.3, "cash", { color: C.p, align: "center", bg: true });
        b.text(1, 0.9, ok ? "no arbitrage: q = " + fmt(q, 3) : (R >= u ? "ARBITRAGE: cash beats the stock in every state" : "ARBITRAGE: the stock beats cash in every state"), { color: ok ? C.ink : C.loss, align: "center", bold: true, size: 12, bg: true });
        b.text(1, 0.12, "q = (1 + r − d) / (u − d)", { color: C.muted, align: "center", bg: true });
      },
      readout: function (v, s) {
        return s.out[4] ? [["risk-neutral q", fmt(s.out[0], 3)], ["call price", fmt(s.out[1], 2)], ["replicating portfolio", fmt(s.out[2], 3) + " shares, " + fmt(s.out[3], 2) + " cash"]]
          : [["risk-neutral q", fmt(s.out[0], 3) + " (not a probability)"], ["price", "undefined: an arbitrage exists"]];
      },
      note: "Nothing here uses the probability that the stock rises. The price is the cost of the hedge.",
    });
  };

  // ---- Part 10: the delta hedger's P&L ---------------------------------------------------------------------------------
  W.hedge = function (el) {
    QB.widget(el, {
      title: "Sell a call, hedge it, see what you earned",
      sub: "A three-month at-the-money call sold at the implied volatility and delta-hedged on 1,200 simulated paths whose true volatility is the realized one. The seller keeps about vega × (implied − realized); the spread around that is the cost of hedging in steps.",
      panels: 2, height: 300,
      controls: [
        { k: "iv", label: "Implied volatility (the price you sold at)", min: 10, max: 40, step: 1, value: 20, fmt: function (x) { return x + "%"; } },
        { k: "rv", label: "Realized volatility (what the stock does)", min: 10, max: 40, step: 1, value: 20, fmt: function (x) { return x + "%"; } },
        { k: "n", label: "Rebalances in three months", min: 1, max: 8, step: 1, value: 6, fmt: function (x) { return String(Math.pow(2, x)); } },
      ],
      buttons: [{ label: "New paths", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var N = Math.pow(2, v.n), T = 0.25, dt = T / N, iv = v.iv / 100, rv = v.rv / 100, paths = 1200, r = QB.rng(s.seed + 200), pnl = [], k, i, show = null;
        var prem = QB.bs(100, 100, T, iv).price;
        for (k = 0; k < paths; k++) {
          var S = 100, del = QB.bs(S, 100, T, iv).delta, cash = prem - del * S, rec = k === 0 ? [[0, S, del]] : null;
          for (i = 1; i <= N; i++) {
            S *= Math.exp(-0.5 * rv * rv * dt + rv * Math.sqrt(dt) * r.normal());
            if (i < N) { var nd = QB.bs(S, 100, T - i * dt, iv).delta; cash -= (nd - del) * S; del = nd; }
            if (rec) rec.push([i * dt, S, del]);
          }
          pnl.push(cash + del * S - Math.max(S - 100, 0)); if (rec) show = rec;
        }
        var m = QB.mean(pnl), sdv = QB.sd(pnl), vega = QB.bs(100, 100, T, iv).vega;
        s.out = [prem, m, sdv, vega * (iv - rv)];
        var a = g[0].axes({ x: [0, T], y: [0, 1], title: "One path: the hedge ratio the seller holds", xlabel: "years", yfmt: function (y) { return y.toFixed(1); } });
        a.line(show.map(function (p) { return p[0]; }), show.map(function (p) { return p[2]; }), { color: C.idea, width: 2 });
        var lo = Math.min.apply(null, show.map(function (p) { return p[1]; })), hi = Math.max.apply(null, show.map(function (p) { return p[1]; }));
        a.line(show.map(function (p) { return p[0]; }), show.map(function (p) { return 0.08 + 0.84 * (p[1] - lo) / Math.max(1e-9, hi - lo); }), { color: C.spot, width: 1, alpha: 0.7 });
        a.legend([["delta (shares held)", C.idea], ["stock price (rescaled)", C.spot]], { pos: "tl" });
        var w = Math.max(1.5, Math.abs(m) + 3.5 * sdv), b = g[1].axes({ x: [-w, w], y: [0, paths * 0.2], title: "Seller's P&L per 100 of stock, 1,200 paths", xlabel: "P&L (premium " + fmt(prem, 2) + ")" });
        var H = QB.hist(pnl, -w, w, 50);
        b.bars(QB.linspace(-w + w / 50, w - w / 50, 50), H, w / 25, { color: function (j) { return -w + (j + 0.5) * w / 25 < 0 ? C.loss : C.gain; } });
        b.vline(0, { color: C.ink, dash: null }); b.vline(m, { color: C.p });
      },
      readout: function (v, s) { return [["mean P&L", fmt(s.out[1], 2)], ["vega × (implied − realized)", fmt(s.out[3], 2)], ["sd of P&L", fmt(s.out[2], 2)], ["premium", fmt(s.out[0], 2)]]; },
      note: "Zero rates, no costs. Halving the rebalancing interval cuts the spread by about √2; nothing but the volatility gap moves the mean.",
    });
  };

  // ---- Part 11: gamma against theta ---------------------------------------------------------------------------------------
  W.gamma = function (el) {
    QB.widget(el, {
      title: "Gamma against theta",
      sub: "A delta-hedged straddle struck at 100, held for one day. It earns ½Γ(move)² and pays one day of time decay; a change in implied volatility adds vega on top.",
      panels: 2, height: 300,
      controls: [
        { k: "T", label: "Days to expiry", min: 2, max: 120, step: 1, value: 30, fmt: function (x) { return x + " days"; } },
        { k: "iv", label: "Implied volatility", min: 10, max: 60, step: 1, value: 20, fmt: function (x) { return x + "%"; } },
        { k: "dv", label: "Change in implied volatility today", min: -5, max: 5, step: 0.5, value: 0, fmt: function (x) { return (x > 0 ? "+" : "") + x.toFixed(1) + " pts"; } },
      ],
      draw: function (g, v, s) {
        var T = v.T / 252, iv = v.iv / 100, dt = 1 / 252, val = function (S, t, sg) { return QB.bs(S, 100, t, sg, 0, 1).price + QB.bs(S, 100, t, sg, 0, -1).price; };
        var v0 = val(100, T, iv), del0 = QB.bs(100, 100, T, iv, 0, 1).delta + QB.bs(100, 100, T, iv, 0, -1).delta, gam = 2 * QB.bs(100, 100, T, iv).gamma;
        var theta = 2 * QB.bs(100, 100, T, iv).theta * dt, vega = 2 * QB.bs(100, 100, T, iv).vega * v.dv / 100, be = 100 * iv * Math.sqrt(dt), span = Math.max(3, 4 * be);
        var xs = QB.linspace(-span, span, 121), tot = xs.map(function (m) { return val(100 + m, T - dt, iv + v.dv / 100) - v0 - del0 * m; });
        var lo = Math.min(Math.min.apply(null, tot), theta) * 1.3 - 0.02, hi = Math.max.apply(null, tot) * 1.15 + 0.02;
        var a = g[0].axes({ x: [-span, span], y: [lo, hi], title: "One day's P&L against the stock's move", xlabel: "move in the stock" });
        a.hline(0, { dash: null }); a.line(xs, xs.map(function (m) { return 0.5 * gam * m * m; }), { color: C.gain, width: 1.4 });
        a.hline(theta, { color: C.loss, width: 1.4, dash: null }); a.line(xs, tot, { color: C.ink, width: 2.4 });
        a.vline(be, { color: C.p }); a.vline(-be, { color: C.p });
        a.legend([["gamma: ½Γ(move)²", C.gain], ["theta: a day's decay", C.loss], ["total, hedged", C.ink]], { pos: "tl" });
        var Ss = QB.linspace(70, 130, 121), b = g[1].axes({ x: [70, 130], y: [0, 32], title: "The straddle's value: today and at expiry", xlabel: "stock price" });
        b.line(Ss, Ss.map(function (S) { return Math.abs(S - 100); }), { color: C.muted, width: 1.4 });
        b.line(Ss, Ss.map(function (S) { return val(S, T, iv); }), { color: C.option, width: 2.2 });
        b.legend([["today", C.option], ["at expiry", C.muted]], { pos: "tl" });
        s.out = [gam, theta, be, vega];
      },
      readout: function (v, s) { return [["gamma", fmt(s.out[0], 3)], ["theta, one day", fmt(s.out[1], 3)], ["breakeven move S·σ·√Δt", "±" + fmt(s.out[2], 2)], ["vega P&L today", fmt(s.out[3], 2)]]; },
      note: "The curve between 'today' and 'at expiry' is what theta takes away; its curvature is the gamma that pays for it.",
    });
  };

  // ---- Part 12: SVI, the density, and the arbitrage ------------------------------------------------------------------------
  W.svi = function (el) {
    QB.widget(el, {
      title: "A smile in five numbers, and the density inside it",
      sub: "Raw SVI gives the total variance w(k) = a + b(ρ(k − m) + √((k − m)² + s²)) at log-moneyness k. The implied density is the second strike-derivative of the call price. Steepen the wings or sharpen the kink until the density goes negative: that smile cannot exist.",
      panels: 2, height: 300,
      controls: [
        { k: "a", label: "Level a", min: 0, max: 0.02, step: 0.0005, value: 0.002, fmt: function (x) { return x.toFixed(4); } },
        { k: "b", label: "Wings b", min: 0.002, max: 0.2, step: 0.002, value: 0.014, fmt: function (x) { return x.toFixed(3); } },
        { k: "rho", label: "Tilt ρ", min: -0.95, max: 0.95, step: 0.05, value: -0.6, fmt: function (x) { return x.toFixed(2); } },
        { k: "m", label: "Shift m", min: -0.15, max: 0.15, step: 0.01, value: 0, fmt: function (x) { return x.toFixed(2); } },
        { k: "s", label: "Smoothness s", min: 0.004, max: 0.3, step: 0.002, value: 0.08, fmt: function (x) { return x.toFixed(3); } },
      ],
      draw: function (g, v, s) {
        var T = 1 / 12, w = function (k) { return v.a + v.b * (v.rho * (k - v.m) + Math.sqrt((k - v.m) * (k - v.m) + v.s * v.s)); };
        var ks = QB.linspace(-0.4, 0.4, 161), ivs = ks.map(function (k) { return 100 * Math.sqrt(Math.max(w(k), 1e-10) / T); });
        var K = QB.linspace(62, 148, 431), h = K[1] - K[0], call = K.map(function (x) { var k = Math.log(x / 100), sg = Math.sqrt(Math.max(w(k), 1e-10) / T); return QB.bs(100, x, T, sg).price; });
        var dens = K.map(function (_, i) { return i === 0 || i === K.length - 1 ? 0 : (call[i - 1] - 2 * call[i] + call[i + 1]) / (h * h); });
        var minD = Math.min.apply(null, dens.slice(2, -2)), maxD = Math.max.apply(null, dens), ok = minD > -1e-5;
        s.out = [ivs[80], (ivs[84] - ivs[76]) / (ks[84] - ks[76]) / 100, ok];
        var a = g[0].axes({ x: [-0.4, 0.4], y: [0, Math.min(150, Math.max(40, Math.max.apply(null, ivs) * 1.1))], title: "Implied volatility, one-month options, %", xlabel: "log-moneyness k = ln(K/F)" });
        a.line(ks, ivs, { color: C.q, width: 2.2 }); a.vline(0);
        var b = g[1].axes({ x: [62, 148], y: [Math.min(-0.004, minD * 1.2), maxD * 1.15], title: ok ? "Implied density of the price in one month" : "Negative density: a butterfly arbitrage", xlabel: "strike" });
        b.area(K, dens.map(function (d) { return Math.max(d, 0); }), 0, { color: C.q, alpha: 0.3 });
        b.area(K, dens.map(function (d) { return Math.min(d, 0); }), 0, { color: C.loss, alpha: 0.8 });
        b.line(K, dens, { color: ok ? C.q : C.loss, width: 1.8 }); b.hline(0, { dash: null });
        var ln = K.map(function (x) { var sg = ivs[80] / 100 * Math.sqrt(T); return QB.pdf((Math.log(x / 100) + 0.5 * sg * sg) / sg) / (x * sg); });
        b.line(K, ln, { color: C.muted, width: 1.2, dash: [4, 4] });
        b.legend([["implied by the smile", C.q], ["lognormal at ATM vol", C.muted]], { pos: "tr" });
      },
      readout: function (v, s) { return [["at-the-money vol", fmt(s.out[0], 1) + "%"], ["skew ∂σ/∂k", fmt(s.out[1], 2)], ["butterfly arbitrage", s.out[2] ? "none" : "yes: negative density"]]; },
      note: "Lee's bound: the wings cannot be steeper than b(1 + |ρ|) ≤ 2. Long before that, a sharp kink (small s) breaks the density at the money.",
    });
  };

  // ---- Part 13: SABR ----------------------------------------------------------------------------------------------------------
  function sabr(F, K, T, al, be, rho, nu) { // Hagan et al. (2002), lognormal implied volatility
    var fk = Math.pow(F * K, (1 - be) / 2), lg = Math.log(F / K), b1 = 1 - be;
    var corr = 1 + (b1 * b1 / 24 * al * al / (fk * fk) + rho * be * nu * al / (4 * fk) + (2 - 3 * rho * rho) / 24 * nu * nu) * T;
    var den = fk * (1 + b1 * b1 / 24 * lg * lg + Math.pow(b1, 4) / 1920 * Math.pow(lg, 4));
    if (Math.abs(lg) < 1e-7) return al / den * corr;
    var z = nu / al * fk * lg, x = Math.log((Math.sqrt(1 - 2 * rho * z + z * z) + z - rho) / (1 - rho));
    return al / den * (z / x) * corr;
  }
  W.sabr = function (el) {
    QB.widget(el, {
      title: "Stochastic volatility makes the smile; correlation tilts it",
      sub: "Hagan's SABR formula for one-year options. ν is the volatility of volatility (curvature), ρ its correlation with the price (skew), β how the smile travels when the forward moves.",
      panels: 2, height: 300,
      controls: [
        { k: "atm", label: "At-the-money volatility", min: 8, max: 50, step: 1, value: 20, fmt: function (x) { return x + "%"; } },
        { k: "nu", label: "Vol of vol ν", min: 0, max: 1.5, step: 0.05, value: 0.6, fmt: function (x) { return x.toFixed(2); } },
        { k: "rho", label: "Correlation ρ", min: -0.95, max: 0.95, step: 0.05, value: -0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "be", label: "Backbone β", min: 0, max: 1, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var T = 1, nu = Math.max(v.nu, 1e-4), al = v.atm / 100 * Math.pow(100, 1 - v.be), i;
        for (i = 0; i < 20; i++) al *= (v.atm / 100) / sabr(100, 100, T, al, v.be, v.rho, nu); // match the at-the-money vol
        var Ks = QB.linspace(60, 150, 91), sm = function (F) { return Ks.map(function (K) { return 100 * sabr(F, K, T, al, v.be, v.rho, nu); }); };
        var base = sm(100), top = Math.max(40, Math.min(120, Math.max.apply(null, base) * 1.15));
        var a = g[0].axes({ x: [60, 150], y: [0, top], title: "The smile, forward at 100", xlabel: "strike" });
        a.line(Ks, base, { color: C.q, width: 2.4 }); a.hline(v.atm, { color: C.muted }); a.vline(100);
        var b = g[1].axes({ x: [60, 150], y: [0, top], title: "The smile when the forward moves", xlabel: "strike" });
        [[90, C.loss], [100, C.q], [110, C.gain]].forEach(function (f) { b.line(Ks, sm(f[0]), { color: f[1], width: 1.8 }); b.dots([f[0]], [100 * sabr(f[0], f[0], T, al, v.be, v.rho, nu)], { color: f[1], r: 4 }); });
        b.legend([["forward 90", C.loss], ["forward 100", C.q], ["forward 110", C.gain]], { pos: "tr" });
        s.out = [(base[45] - base[35]) / Math.log(105 / 95) / 100, base[10] - base[40], al];
      },
      readout: function (v, s) { return [["skew ∂σ/∂ln K at the money", fmt(s.out[0], 3)], ["70-strike vol minus ATM", fmt(s.out[1], 1) + " pts"], ["α", fmt(s.out[2], 3)]]; },
      note: "The dots are the at-the-money volatility at each forward: the backbone. With β = 1 it is flat (lognormal); with β = 0 it rises as the forward falls (normal).",
    });
  };

  // ---- Part 14: rough paths and the skew's power law ----------------------------------------------------------------------------
  W.rough = function (el) {
    QB.widget(el, {
      title: "How rough is volatility?",
      sub: "A log-volatility path that is a fractional Brownian motion with Hurst exponent H. H = ½ is Brownian; the market looks like H ≈ 0.1. The same exponent sets how fast the at-the-money skew grows as maturity shrinks.",
      panels: 2, height: 300,
      controls: [{ k: "H", label: "Hurst exponent H", min: 0.03, max: 0.5, step: 0.01, value: 0.1, fmt: function (x) { return x.toFixed(2); } }],
      buttons: [{ label: "New path", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = 256, r = QB.rng(s.seed + 300), i, j, k, H = v.H, t = [], L = [], y = [0];
        // exact fractional Brownian motion on the grid: Cholesky factor of cov(s, t) = (s^2H + t^2H - |t - s|^2H) / 2
        for (i = 1; i <= n; i++) t.push(i / n);
        for (i = 0; i < n; i++) { L.push(new Float64Array(i + 1)); for (j = 0; j <= i; j++) {
          var c = 0.5 * (Math.pow(t[i], 2 * H) + Math.pow(t[j], 2 * H) - Math.pow(Math.abs(t[i] - t[j]), 2 * H));
          for (k = 0; k < j; k++) c -= L[i][k] * L[j][k];
          L[i][j] = i === j ? Math.sqrt(Math.max(c, 1e-14)) : c / L[j][j]; } }
        var z = []; for (i = 0; i < n; i++) z.push(r.normal());
        for (i = 0; i < n; i++) { var acc = 0; for (k = 0; k <= i; k++) acc += L[i][k] * z[k]; y.push(acc); }
        var lags = [1, 2, 4, 8, 16, 32], lx = [], ly = [];
        lags.forEach(function (L) { var m = 0, c = 0; for (i = L; i <= n; i++) { m += Math.pow(y[i] - y[i - L], 2); c++; } lx.push(Math.log(L)); ly.push(Math.log(m / c)); });
        var mx = QB.mean(lx), my = QB.mean(ly), num = 0, den = 0; for (i = 0; i < lx.length; i++) { num += (lx[i] - mx) * (ly[i] - my); den += (lx[i] - mx) * (lx[i] - mx); }
        s.out = [num / den / 2, H - 0.5];
        var ymax = Math.max(0.6, Math.max.apply(null, y.map(Math.abs)) * 1.1), a = g[0].axes({ x: [0, 1], y: [-ymax, ymax], title: "A log-volatility path", xlabel: "time" });
        a.line(QB.linspace(0, 1, n + 1), y, { color: C.q, width: 1.1 });
        var Ts = QB.linspace(Math.log(1 / 252), Math.log(2), 60).map(Math.exp), b = g[1].axes({ x: [1 / 252, 2], y: [0.05, 30], logx: true, logy: true, title: "At-the-money skew against maturity (log-log)", xlabel: "maturity, years", xticks: [1 / 252, 1 / 52, 1 / 12, 0.25, 1, 2], xfmt: function (x) { return x < 0.01 ? "1d" : x < 0.03 ? "1w" : x < 0.1 ? "1m" : x < 0.3 ? "3m" : x + "y"; } });
        b.line(Ts, Ts.map(function (t) { return 0.6 * Math.pow(t, H - 0.5); }), { color: C.q, width: 2.4 });
        b.line(Ts, Ts.map(function () { return 0.6; }), { color: C.cash, width: 1.4, dash: [5, 4] });
        b.line(Ts, Ts.map(function (t) { return 0.6 * Math.pow(t, -0.4); }), { color: C.implied, width: 1.2, dash: [2, 3] });
        b.legend([["this H: skew ∝ T^(H−½)", C.q], ["a diffusion (H = ½): flat", C.cash], ["equity index data: about T^−0.4", C.implied]], { pos: "bl" });
      },
      readout: function (v, s) { return [["H estimated from the path", fmt(s.out[0], 2)], ["skew exponent H − ½", fmt(s.out[1], 2)]]; },
      note: "The estimate is the slope of log E|increment|² against log lag, divided by two (Gatheral, Jaisson and Rosenbaum's regression), on this one path.",
    });
  };

  // ---- Part 15: a snowball note ---------------------------------------------------------------------------------------------------
  W.snowball = function (el) {
    QB.widget(el, {
      title: "What the buyer of a snowball has sold",
      sub: "A two-year note on an index starting at 100. It is called away with its coupon at the first monthly date (after month 3) the index is above 103. If it is never called and the index ever closed below the knock-in level, the buyer takes the index's loss.",
      panels: 2, weights: [1.4, 1], height: 310,
      controls: [
        { k: "sig", label: "Index volatility", min: 8, max: 45, step: 1, value: 20, fmt: function (x) { return x + "%"; } },
        { k: "ki", label: "Knock-in level", min: 55, max: 95, step: 1, value: 75, fmt: function (x) { return x + "% of start"; } },
        { k: "c", label: "Coupon, a year", min: 2, max: 30, step: 1, value: 15, fmt: function (x) { return x + "%"; } },
      ],
      buttons: [{ label: "New paths", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var paths = 1500, months = 24, dpm = 21, n = months * dpm, sg = v.sig / 100, dt = 1 / 252, r = QB.rng(s.seed + 400), rate = 0.02, k, i;
        var cnt = [0, 0, 0], pv = 0, a = g[0].axes({ x: [0, months], y: [40, 160], title: "Forty of 1,500 paths, by how they end", xlabel: "month" });
        a.hline(103, { color: C.gain }); a.hline(v.ki, { color: C.loss }); a.text(months, 103, "knock-out 103", { color: C.gain, align: "right", dy: -8 }); a.text(months, v.ki, "knock-in " + v.ki, { color: C.loss, align: "right", dy: 9 });
        for (k = 0; k < paths; k++) {
          var S = 100, kin = false, out = -1, xs = k < 40 ? [0] : null, ys = k < 40 ? [100] : null;
          for (i = 1; i <= n; i++) {
            S *= Math.exp((rate - 0.5 * sg * sg) * dt + sg * Math.sqrt(dt) * r.normal());
            if (S < v.ki) kin = true;
            if (xs && i % 3 === 0) { xs.push(i / dpm); ys.push(S); }
            if (i % dpm === 0 && i / dpm >= 3 && S >= 103) { out = i; break; }
          }
          var typ, pay, t;
          if (out > 0) { typ = 0; t = out / 252; pay = 1 + v.c / 100 * t; } else if (!kin) { typ = 1; t = 2; pay = 1 + v.c / 100 * 2; } else { typ = 2; t = 2; pay = Math.min(S / 100, 1); }
          cnt[typ]++; pv += pay * Math.exp(-rate * t);
          if (xs) a.line(xs, ys, { color: [C.gain, C.idea, C.loss][typ], width: 1, alpha: 0.55 });
        }
        s.out = [cnt[0] / paths, cnt[1] / paths, cnt[2] / paths, pv / paths];
        var b = g[1].axes({ x: [-0.6, 2.6], y: [0, 1], title: "How the note ends", xticks: [0, 1, 2], xfmt: function (x) { return ["called early", "runs to the end", "knocked in"][x]; }, yfmt: function (y) { return (100 * y).toFixed(0) + "%"; } });
        b.bars([0, 1, 2], s.out.slice(0, 3), 0.7, { color: function (j) { return [C.gain, C.idea, C.loss][j]; } });
        [0, 1, 2].forEach(function (j) { b.text(j, s.out[j], pct(s.out[j], 0), { align: "center", dy: -9, bold: true }); });
      },
      readout: function (v, s) { return [["value per 100 of notional", fmt(100 * s.out[3], 1)], ["called early with coupon", pct(s.out[0], 0)], ["loses with the index", pct(s.out[2], 0)]]; },
      note: "Simulated under the pricing measure with a 2% rate. Raise the volatility and the value falls: the buyer is short a down-and-in put and is paid the coupon for it.",
    });
  };
})();
