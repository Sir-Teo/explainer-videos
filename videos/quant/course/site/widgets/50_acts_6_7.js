// Interactives for Acts VI-VII and the finale (Parts 35-43).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, pct = QB.pct;

  // ---- Part 35: Glosten and Milgrom -------------------------------------------------------------------------------------
  W.gm = function (el) {
    QB.widget(el, {
      title: "The spread is insurance against people who know more",
      sub: "The asset is worth 0 or 1. A share μ of traders know which and trade on it; the rest buy or sell at random. The dealer cannot tell them apart, so the ask is the expected value given that someone bought, the bid given that someone sold, and every trade moves the dealer's belief.",
      panels: 2, weights: [1.4, 1], height: 300,
      controls: [
        { k: "mu", label: "Share of informed traders μ", min: 0, max: 0.9, step: 0.02, value: 0.3, fmt: function (x) { return pct(x, 0); } },
        { k: "p", label: "Dealer's starting belief that the value is 1", min: 0.05, max: 0.95, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New tape", act: function (s) { s.seed++; } }, { label: "Flip the true value", act: function (s) { s.high = !s.high; } }],
      init: function (s) { s.high = true; },
      draw: function (g, v, s) {
        var quotes = function (p) { var pb1 = v.mu + (1 - v.mu) / 2, pb0 = (1 - v.mu) / 2; return [p * pb1 / (p * pb1 + (1 - p) * pb0), p * pb0 / (p * pb0 + (1 - p) * pb1)]; };
        var r = QB.rng(s.seed + 1700), n = 60, p = v.p, P = [p], A = [], B = [], buys = [], i;
        for (i = 0; i < n; i++) { var q = quotes(p); A.push(q[0]); B.push(q[1]); var buy = r() < v.mu ? s.high : r() < 0.5; buys.push(buy); p = buy ? q[0] : q[1]; P.push(p); }
        var q0 = quotes(v.p), xs = QB.linspace(0, n - 1, n), a = g[0].axes({ x: [0, n], y: [0, 1], title: "Sixty trades: quotes and the dealer's belief (true value " + (s.high ? "1" : "0") + ")", xlabel: "trade" });
        a.area(xs, A, B, { color: C.spot, alpha: 0.22 }); a.line(xs, A, { color: C.loss, width: 1.2 }); a.line(xs, B, { color: C.gain, width: 1.2 });
        a.line(QB.linspace(0, n, n + 1), P, { color: C.ink, width: 2 });
        a.dots(xs.filter(function (_, j) { return buys[j]; }), A.filter(function (_, j) { return buys[j]; }), { color: C.loss, r: 2.5 });
        a.dots(xs.filter(function (_, j) { return !buys[j]; }), B.filter(function (_, j) { return !buys[j]; }), { color: C.gain, r: 2.5 });
        a.legend([["ask", C.loss], ["bid", C.gain], ["belief", C.ink]], { pos: s.high ? "br" : "tr" });
        var mus = QB.linspace(0, 0.9, 60), keep = v.mu, b = g[1].axes({ x: [0, 0.9], y: [0, 1], title: "Spread at the first trade against μ", xlabel: "share of informed traders", xfmt: function (x) { return (100 * x).toFixed(0) + "%"; } });
        b.line(mus, mus.map(function (m) { v.mu = m; var z = quotes(v.p); return z[0] - z[1]; }), { color: C.p, width: 2.2 }); v.mu = keep;
        b.dots([v.mu], [q0[0] - q0[1]], { color: C.ink, r: 5 });
        s.out = [q0[1], q0[0], P[n], buys.filter(Boolean).length];
      },
      readout: function (v, s) { return [["first bid", fmt(s.out[0], 3)], ["first ask", fmt(s.out[1], 3)], ["spread", fmt(s.out[1] - s.out[0], 3)], ["belief after 60 trades", fmt(s.out[2], 3)], ["buys", s.out[3] + " of 60"]]; },
      note: "At a belief of one half the spread equals μ exactly. The price converges on the truth because the informed keep trading in one direction: order flow carries information.",
    });
  };

  // ---- Part 36: an order book made of nothing but arrivals ---------------------------------------------------------------
  W.lob = function (el) {
    var L = 60;
    QB.widget(el, {
      title: "An order book with no intelligence in it",
      sub: "Limit orders arrive at random prices, market orders eat the best quotes, resting orders are cancelled at random. Nobody here has a view, and still there is a spread, a depth profile and a price that wanders. Thin the queue on one side and watch which way it breaks.",
      panels: 2, weights: [1.25, 1], height: 310,
      controls: [
        { k: "lim", label: "Limit-order arrivals", min: 0.5, max: 6, step: 0.1, value: 2.5, fmt: function (x) { return x.toFixed(1); } },
        { k: "mkt", label: "Market-order arrivals", min: 0.2, max: 6, step: 0.1, value: 1.5, fmt: function (x) { return x.toFixed(1); } },
        { k: "can", label: "Cancellation rate", min: 0.02, max: 1, step: 0.02, value: 0.2, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "Reset", act: function (s) { s.book = null; } }],
      init: function (s) { s.r = QB.rng(5); },
      animate: function (v, s, dt) {
        var i, k, r = s.r;
        if (!s.book) { s.book = new Array(L).fill(0); for (i = 0; i < L; i++) s.book[i] = i < L / 2 - 1 ? 4 : i > L / 2 ? -4 : 0; s.mid = []; s.t = 0; }
        var B = s.book, steps = 6;
        for (k = 0; k < steps; k++) {
          var bid = -1, ask = L; for (i = L - 1; i >= 0; i--) if (B[i] > 0) { bid = i; break; } for (i = 0; i < L; i++) if (B[i] < 0) { ask = i; break; }
          if (r() < v.lim * 0.5) { var side = r() < 0.5; var px = side ? Math.min(ask - 1, (ask < L ? ask : L - 1) - 1 - Math.floor(r() * 12)) : Math.max(bid + 1, (bid >= 0 ? bid : 0) + 1 + Math.floor(r() * 12)); if (px >= 0 && px < L) B[px] += side ? 1 : -1; }
          if (r() < v.mkt * 0.12) { if (r() < 0.5) { if (ask < L) B[ask] += 1; } else if (bid >= 0) B[bid] -= 1; }
          for (i = 0; i < L; i++) if (B[i] !== 0 && r() < v.can * 0.02 * Math.abs(B[i])) B[i] -= Math.sign(B[i]);
          if (bid >= 0 && ask < L) { s.mid.push((bid + ask) / 2); if (s.mid.length > 600) s.mid.shift(); s.bid = bid; s.ask = ask; }
        }
        return true;
      },
      draw: function (g, v, s) {
        if (!s.book) return;
        var B = s.book, xs = QB.linspace(0, L - 1, L), top = Math.max(12, Math.max.apply(null, B.map(Math.abs)) + 2);
        var a = g[0].axes({ x: [-1, L], y: [0, top], title: "The book: resting buy orders (green) and sell orders (red)", xlabel: "price, in ticks" });
        a.bars(xs, B.map(Math.abs), 1, { color: function (i) { return B[i] > 0 ? C.gain : C.loss; } });
        var qb = B[s.bid] || 0, qa = -(B[s.ask] || 0), up = qb > 0 && qa > 0 ? 1 - 2 / Math.PI * Math.atan(qa / qb) : 0.5;
        a.vline((s.bid + s.ask) / 2, { color: C.ink });
        var m = s.mid, lo = Math.min.apply(null, m) - 2, hi = Math.max.apply(null, m) + 2, b = g[1].axes({ x: [0, 600], y: [lo, hi], title: "The mid price", xlabel: "events (most recent at the right)", xticks: [] });
        b.line(m.map(function (_, i) { return 600 - m.length + i; }), m, { color: C.spot, width: 1.5 });
        s.out = [s.ask - s.bid, qb, qa, up];
      },
      readout: function (v, s) { return s.out ? [["spread", s.out[0] + " ticks"], ["best bid size", String(s.out[1])], ["best ask size", String(s.out[2])], ["imbalance", fmt(s.out[1] / Math.max(1, s.out[1] + s.out[2]), 2)], ["P(next move up), queue model", pct(s.out[3], 0)]] : []; },
      note: "A zero-intelligence book in the spirit of Smith, Farmer, Gillemot and Krishnamurthy (2003). The last number is 1 − (2/π)·atan(ask size / bid size), the diffusive-queue formula of Part 36.",
    });
  };

  // ---- Part 37: Almgren and Chriss -------------------------------------------------------------------------------------------
  W.ac = function (el) {
    QB.widget(el, {
      title: "How fast to sell",
      sub: "Selling quickly moves the price against you; selling slowly leaves you exposed to the market for longer. Almgren and Chriss trade the two off with one number, the trader's risk aversion, and the answer is a family of schedules and a frontier.",
      panels: 2, height: 300,
      controls: [
        { k: "lam", label: "Risk aversion (urgency)", min: -2, max: 2.5, step: 0.05, value: 0.5, fmt: function (x) { return Math.pow(10, x).toPrecision(2); } },
        { k: "eta", label: "Temporary impact of trading fast", min: 0.02, max: 0.5, step: 0.01, value: 0.1, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var sig = 0.3, T = 1, ts = QB.linspace(0, 1, 101);
        var plan = function (lam) { var k = Math.sqrt(lam * sig * sig / v.eta), sh = Math.sinh(k * T);
          if (k < 1e-4) return { x: ts.map(function (t) { return 1 - t; }), cost: v.eta / T, sd: sig * Math.sqrt(T / 3) };
          return { x: ts.map(function (t) { return Math.sinh(k * (T - t)) / sh; }), cost: v.eta * k * k / (sh * sh) * (T / 2 + Math.sinh(2 * k * T) / (4 * k)), sd: sig / sh * Math.sqrt(Math.max(0, Math.sinh(2 * k * T) / (4 * k) - T / 2)) }; };
        var me = plan(Math.pow(10, v.lam)), a = g[0].axes({ x: [0, 1], y: [0, 1], title: "Share of the order still to sell", xlabel: "time (one day)" });
        [-2, -0.5, 0.5, 1.5, 2.5].forEach(function (l) { a.line(ts, plan(Math.pow(10, l)).x, { color: C.cash, width: 1, alpha: 0.5 }); });
        a.line(ts, ts.map(function (t) { return 1 - t; }), { color: C.muted, width: 1.2, dash: [4, 4] }); a.line(ts, me.x, { color: C.p, width: 2.6 });
        a.legend([["your schedule", C.p], ["even pace (TWAP)", C.muted]], { pos: "tr" });
        var ls = QB.linspace(-2.5, 3, 80).map(function (l) { return plan(Math.pow(10, l)); }), b = g[1].axes({ x: [0, 0.19], y: [0, Math.min(3, ls[79].cost * 1.05)], title: "Expected cost against risk: the frontier", xlabel: "standard deviation of the cost" });
        b.line(ls.map(function (p) { return p.sd; }), ls.map(function (p) { return p.cost; }), { color: C.spot, width: 2 }); b.dots([me.sd], [me.cost], { color: C.p, r: 6 });
        var half = 0; for (var i = 0; i <= 100; i++) if (me.x[i] <= 0.5) { half = ts[i]; break; }
        s.out = [half, me.cost, me.sd, plan(1e-6).cost];
      },
      readout: function (v, s) { return [["half the order is sold by", pct(s.out[0], 0) + " of the day"], ["expected cost", fmt(s.out[1], 3)], ["sd of the cost", fmt(s.out[2], 3)], ["cost at an even pace", fmt(s.out[3], 3)]]; },
      note: "x(t) = X·sinh κ(T − t) / sinh κT with κ = √(λσ²/η). Costs are in units of the order's value squared; σ = 30% over the horizon.",
    });
  };

  // ---- Part 38: a market maker who leans against inventory -------------------------------------------------------------------
  W.mm = function (el) {
    QB.widget(el, {
      title: "A market maker who leans against inventory",
      sub: "The maker quotes around a reservation price that is the mid shifted against its inventory: long, it lowers both quotes to sell; short, it raises them to buy. Orders hit a quote more often the closer it sits to the mid. Set the risk aversion to zero and it quotes symmetrically and lets inventory wander.",
      panels: 2, height: 310,
      controls: [
        { k: "gam", label: "Inventory aversion γ", min: 0, max: 2, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "sig", label: "Volatility of the mid", min: 0.5, max: 4, step: 0.1, value: 2, fmt: function (x) { return x.toFixed(1); } },
        { k: "k", label: "How fast fills fall with distance k", min: 0.5, max: 4, step: 0.1, value: 1.5, fmt: function (x) { return x.toFixed(1); } },
      ],
      buttons: [{ label: "New session", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = 400, dt = 1 / n, r = QB.rng(s.seed + 1800), mid = 100, q = 0, cash = 0, M = [], RP = [], BQ = [], AQ = [], Q = [], PL = [], i, gam = Math.max(v.gam, 1e-6), A = 140;
        var run = function (gm, seed) { var rr = QB.rng(seed), m = 100, qq = 0, c = 0, g2 = Math.max(gm, 1e-6), j; for (j = 0; j < n; j++) { var tl = 1 - j * dt, rp = m - qq * g2 * v.sig * v.sig * tl, hs = (g2 * v.sig * v.sig * tl + 2 / g2 * Math.log(1 + g2 / v.k)) / 2, db = m - (rp - hs), da = (rp + hs) - m; if (rr() < A * Math.exp(-v.k * Math.max(db, 0)) * dt) { qq++; c -= rp - hs; } if (rr() < A * Math.exp(-v.k * Math.max(da, 0)) * dt) { qq--; c += rp + hs; } m += v.sig * Math.sqrt(dt) * rr.normal(); } return c + qq * m; };
        for (i = 0; i < n; i++) {
          var tl = 1 - i * dt, rp = mid - q * gam * v.sig * v.sig * tl, hs = (gam * v.sig * v.sig * tl + 2 / gam * Math.log(1 + gam / v.k)) / 2;
          M.push(mid); RP.push(rp); BQ.push(rp - hs); AQ.push(rp + hs); Q.push(q); PL.push(cash + q * mid);
          if (r() < A * Math.exp(-v.k * Math.max(mid - (rp - hs), 0)) * dt) { q++; cash -= rp - hs; }
          if (r() < A * Math.exp(-v.k * Math.max(rp + hs - mid, 0)) * dt) { q--; cash += rp + hs; }
          mid += v.sig * Math.sqrt(dt) * r.normal();
        }
        var pn = [], pz = []; for (i = 0; i < 150; i++) { pn.push(run(v.gam, 9000 + i)); pz.push(run(0, 9000 + i)); }
        s.out = [PL[n - 1], Math.max.apply(null, Q.map(Math.abs)), QB.mean(pn), QB.sd(pn), QB.mean(pz), QB.sd(pz)];
        var xs = QB.linspace(0, 1, n), lo = Math.min.apply(null, BQ) - 0.3, hi = Math.max.apply(null, AQ) + 0.3, a = g[0].axes({ x: [0, 1], y: [lo, hi], title: "One session: the mid and the maker's two quotes", xlabel: "time" });
        a.area(xs, AQ, BQ, { color: C.spot, alpha: 0.14 }); a.line(xs, AQ, { color: C.loss, width: 1 }); a.line(xs, BQ, { color: C.gain, width: 1 }); a.line(xs, M, { color: C.ink, width: 1.8 });
        a.legend([["mid", C.ink], ["ask", C.loss], ["bid", C.gain]], { pos: "tl" });
        var qm = Math.max(4, s.out[1] + 1), b = g[1].axes({ x: [0, 1], y: [-qm, qm], title: "Inventory (bars) and P&L (line, rescaled)", xlabel: "time" });
        b.bars(xs, Q, 1 / n, { color: function (j) { return Q[j] >= 0 ? C.gain : C.loss; }, gap: 0, alpha: 0.55 }); b.hline(0, { dash: null });
        var pm = Math.max.apply(null, PL.map(Math.abs)) || 1; b.line(xs, PL.map(function (p) { return p / pm * qm * 0.9; }), { color: C.p, width: 2 });
      },
      readout: function (v, s) { return [["this session's P&L", fmt(s.out[0], 1)], ["largest inventory", String(s.out[1])], ["150 sessions: mean ± sd", fmt(s.out[2], 1) + " ± " + fmt(s.out[3], 1)], ["with γ = 0", fmt(s.out[4], 1) + " ± " + fmt(s.out[5], 1)]]; },
      note: "Avellaneda and Stoikov (2008): reservation price r = s − qγσ²(T − t), total spread γσ²(T − t) + (2/γ)·ln(1 + γ/k). Leaning gives up some expected profit and removes more than half of its variability.",
    });
  };

  // ---- Part 39: a constant-product pool ------------------------------------------------------------------------------------------
  W.amm = function (el) {
    QB.widget(el, {
      title: "What a liquidity provider holds, and loses",
      sub: "A pool holds x tokens and y dollars with x·y fixed; its price is y/x. As the market price moves, arbitrageurs trade the pool along the curve, always buying the token from it cheap and selling it dear. The provider ends with more of whatever fell.",
      panels: 2, height: 300,
      controls: [
        { k: "r", label: "Market price, relative to the start", min: -1.6, max: 1.6, step: 0.02, value: 0.69, fmt: function (x) { return "×" + Math.exp(x).toFixed(2); } },
        { k: "sig", label: "Volatility (for the loss per year)", min: 10, max: 150, step: 5, value: 80, fmt: function (x) { return x + "%"; } },
      ],
      draw: function (g, v, s) {
        var r = Math.exp(v.r), x = 1 / Math.sqrt(r), y = Math.sqrt(r), xs = QB.linspace(0.3, 3.3, 200), a = g[0].axes({ x: [0, 3.3], y: [0, 3.3], title: "The pool's reserves slide along x·y = k", xlabel: "tokens held by the pool" });
        a.line(xs, xs.map(function (q) { return 1 / q; }), { color: C.q, width: 2.2 });
        a.area([0, x], [y, y], 0, { color: C.q, alpha: 0.12 }); a.dots([1], [1], { color: C.cash, r: 4 }); a.dots([x], [y], { color: C.p, r: 6 });
        a.line([x - 0.5, x + 0.5], [y + 0.5 * r, y - 0.5 * r], { color: C.p, width: 1.4 });
        a.text(1, 1, " start", { color: C.cash, dx: 6 }); a.text(x, y, " now: price = y/x", { color: C.p, dx: 8, dy: -10, bg: true });
        a.text(3.25, 3.1, "vertical: dollars held by the pool", { color: C.muted, align: "right" });
        var rs = QB.linspace(-1.6, 1.6, 120).map(Math.exp), b = g[1].axes({ x: [0.2, 5], y: [0, 3.2], logx: true, title: "Value: in the pool against simply holding", xlabel: "price relative to the start", xticks: [0.2, 0.5, 1, 2, 5] });
        b.line(rs, rs.map(function (q) { return (1 + q) / 2; }), { color: C.cash, width: 2 }); b.line(rs, rs.map(Math.sqrt), { color: C.q, width: 2.2 });
        b.vline(r, { color: C.p }); b.dots([r, r], [(1 + r) / 2, Math.sqrt(r)], { color: function (i) { return i ? C.q : C.cash; }, r: 5 });
        b.legend([["hold 50/50", C.cash], ["in the pool (before fees)", C.q]], { pos: "tl" });
        s.out = [2 * Math.sqrt(r) / (1 + r) - 1, x, y, v.sig * v.sig / 8e4];
      },
      readout: function (v, s) { return [["impermanent loss", pct(s.out[0], 2)], ["pool now holds", fmt(s.out[1], 2) + " tokens, " + fmt(s.out[2], 2) + " dollars"], ["loss versus rebalancing, σ²/8", pct(s.out[3], 1) + " of the pool a year"]]; },
      note: "Impermanent loss depends only on where the price ends: 2√r/(1 + r) − 1. Loss versus rebalancing accrues every block at σ²/8 whether or not the price comes back; fees have to cover it.",
    });
  };

  // ---- Part 40: VaR and expected shortfall under fat tails --------------------------------------------------------------------------
  W.var = function (el) {
    var lgam = function (x) { var c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.001208650973866179, -0.000005395239384953], y = x, t = x + 5.5, s = 1.000000000190015; t -= (x + 0.5) * Math.log(t); for (var j = 0; j < 6; j++) s += c[j] / ++y; return -t + Math.log(2.5066282746310005 * s / x); };
    var tpdf = function (x, nu) { return Math.exp(lgam((nu + 1) / 2) - lgam(nu / 2)) / Math.sqrt(nu * Math.PI) * Math.pow(1 + x * x / nu, -(nu + 1) / 2); };
    QB.widget(el, {
      title: "The same volatility, two tails",
      sub: "A normal distribution and a Student t with the same standard deviation of 1%. At 95% the two value-at-risk numbers nearly agree. Go further into the tail, or ask how bad the bad days are (expected shortfall), and they part company.",
      panels: 2, height: 300,
      controls: [
        { k: "nu", label: "Tail weight: degrees of freedom", min: 2.5, max: 30, step: 0.5, value: 4, fmt: function (x) { return x.toFixed(1); } },
        { k: "a", label: "Confidence level", min: 90, max: 99.9, step: 0.1, value: 99, fmt: function (x) { return x.toFixed(1) + "%"; } },
      ],
      draw: function (g, v, s) {
        var nu = v.nu, sc = Math.sqrt((nu - 2) / nu), al = v.a / 100, N = 4000, xs = QB.linspace(0, 40, N + 1), cdfT = [0.5], i, h = 40 / N;
        for (i = 1; i <= N; i++) cdfT.push(cdfT[i - 1] + h * 0.5 * (tpdf(xs[i - 1], nu) + tpdf(xs[i], nu)));
        var qT = function (p) { for (var j = 1; j <= N; j++) if (cdfT[j] >= p) return xs[j - 1] + h * (p - cdfT[j - 1]) / (cdfT[j] - cdfT[j - 1]); return 40; };
        var esT = function (p) { var q = qT(p); return (nu + q * q) / (nu - 1) * tpdf(q, nu) / (1 - p); };
        var varT = sc * qT(al), ES_T = sc * esT(al), varN = QB.inv(al), ES_N = QB.pdf(varN) / (1 - al);
        s.out = [varN, varT, ES_N, ES_T];
        var ls = QB.linspace(-8, 0, 200), a = g[0].axes({ x: [-8, 0], y: [0.0001, 0.6], logy: true, title: "The loss tail of each distribution (log scale)", xlabel: "daily return, %" });
        a.line(ls, ls.map(QB.pdf), { color: C.cash, width: 2 }); a.line(ls, ls.map(function (x) { return tpdf(x / sc, nu) / sc; }), { color: C.loss, width: 2.2 });
        a.vline(-varN, { color: C.cash }); a.vline(-varT, { color: C.loss }); a.vline(-ES_T, { color: C.p });
        a.legend([["normal", C.cash], ["Student t, same sd", C.loss], ["t: expected shortfall", C.p]], { pos: "tl" });
        var cs = QB.linspace(0.9, 0.999, 60), b = g[1].axes({ x: [0.9, 0.999], y: [1, 12], title: "Risk measures against the confidence level, %", xlabel: "confidence", xticks: [0.9, 0.95, 0.99], xfmt: function (x) { return (100 * x).toFixed(0) + "%"; } });
        b.line(cs, cs.map(QB.inv), { color: C.cash, width: 1.6 }); b.line(cs, cs.map(function (c) { return QB.pdf(QB.inv(c)) / (1 - c); }), { color: C.cash, width: 1.6, dash: [5, 4] });
        b.line(cs, cs.map(function (c) { return sc * qT(c); }), { color: C.loss, width: 2 }); b.line(cs, cs.map(function (c) { return Math.min(40, sc * esT(c)); }), { color: C.loss, width: 2, dash: [5, 4] });
        b.vline(al); b.legend([["normal: VaR, and ES dashed", C.cash], ["Student t: VaR, and ES dashed", C.loss]], { pos: "tl" });
      },
      readout: function (v, s) { return [["VaR: normal / t", fmt(s.out[0], 2) + "% / " + fmt(s.out[1], 2) + "%"], ["expected shortfall: normal / t", fmt(s.out[2], 2) + "% / " + fmt(s.out[3], 2) + "%"], ["ES ÷ VaR for the t", fmt(s.out[3] / s.out[1], 2)]]; },
      note: "For a normal, expected shortfall at 97.5% is close to VaR at 99%: that is why Basel moved between them. With four degrees of freedom the average bad day is half again as bad as the VaR.",
    });
  };

  // ---- Part 41: the spirals --------------------------------------------------------------------------------------------------------
  W.firesale = function (el) {
    var spiral = function (shock, L, depth, kappa) { // a levered holder must cut the position to what its equity can carry
      var q = 1, p = 1 - shock, D = 1 - 1 / L, path = [1, p], i;
      for (i = 0; i < 60; i++) { var e = q * p - D; if (e <= 0) { path.push(Math.max(0, p - q / depth)); return { path: path, wiped: true, fall: 1 - path[path.length - 1] }; }
        var m = Math.min(0.9, 1 / L + kappa * (1 - p)), target = Math.min(q, e / (m * p)), sell = q - target; if (sell < 1e-7) break; D -= sell * p; q = target; p = Math.max(0.01, p - sell / depth); path.push(p); }
      return { path: path, wiped: false, fall: 1 - p };
    };
    QB.widget(el, {
      title: "What a levered holder must sell",
      sub: "A fund holds an asset with borrowed money. A shock cuts its equity; to get back within its margin it sells; the sale pushes the price down, which cuts its equity again. If lenders also raise margins as prices fall, the two spirals feed each other.",
      panels: 2, height: 300,
      controls: [
        { k: "L", label: "Leverage", min: 1.5, max: 25, step: 0.5, value: 6, fmt: function (x) { return x + "×"; } },
        { k: "shock", label: "The first shock to the price", min: 0.5, max: 15, step: 0.5, value: 4, fmt: function (x) { return "−" + x + "%"; } },
        { k: "depth", label: "Market depth", min: 1, max: 20, step: 0.5, value: 5, fmt: function (x) { return x.toFixed(1) + "× the position"; } },
        { k: "kap", label: "Margin tightening as prices fall", min: 0, max: 4, step: 0.1, value: 1.5, fmt: function (x) { return x.toFixed(1); } },
      ],
      draw: function (g, v, s) {
        var a1 = spiral(v.shock / 100, v.L, v.depth, 0), a2 = spiral(v.shock / 100, v.L, v.depth, v.kap), n = Math.max(a1.path.length, a2.path.length, 8);
        var a = g[0].axes({ x: [0, n], y: [0, 1.02], title: "The price, round by round of forced selling", xlabel: "round" });
        a.hline(1 - v.shock / 100, { color: C.muted }); a.text(n, 1 - v.shock / 100, "the shock alone", { color: C.muted, align: "right", dy: -8 });
        a.line(a1.path.map(function (_, i) { return i; }), a1.path, { color: C.p, width: 2 }); a.dots(a1.path.map(function (_, i) { return i; }), a1.path, { color: C.p, r: 2.5 });
        a.line(a2.path.map(function (_, i) { return i; }), a2.path, { color: C.loss, width: 2.2 }); a.dots(a2.path.map(function (_, i) { return i; }), a2.path, { color: C.loss, r: 2.5 });
        a.legend([["loss spiral (fixed margin)", C.p], ["with rising margins", C.loss]], { pos: "bl" });
        var sh = QB.linspace(0.005, 0.15, 60), b = g[1].axes({ x: [0, 15], y: [0, 100], title: "Total fall against the size of the first shock, %", xlabel: "first shock, %" });
        b.line([0, 15], [0, 15], { color: C.muted, width: 1.2, dash: [4, 4] });
        b.line(sh.map(function (x) { return 100 * x; }), sh.map(function (x) { return 100 * spiral(x, v.L, v.depth, 0).fall; }), { color: C.p, width: 2 });
        b.line(sh.map(function (x) { return 100 * x; }), sh.map(function (x) { return 100 * spiral(x, v.L, v.depth, v.kap).fall; }), { color: C.loss, width: 2.2 });
        b.vline(v.shock);
        s.out = [a1, a2];
      },
      readout: function (v, s) { var o = function (a) { return pct(a.fall, 1) + (a.wiped ? " (equity wiped out)" : "") + ", ×" + fmt(a.fall / (v.shock / 100), 1); }; return [["total fall, loss spiral", o(s.out[0])], ["with rising margins", o(s.out[1])], ["equity cushion 1/L", pct(1 / v.L, 1)]]; },
      note: "A minimal fixed point in the spirit of Brunnermeier and Pedersen (2009). Depth is how many times the fund's position must be sold to move the price to zero. Raise the leverage or thin the market and a threshold appears, beyond which selling can no longer restore the margin.",
    });
  };

  // ---- Part 42: Kirman's ants ----------------------------------------------------------------------------------------------------------
  W.kirman = function (el) {
    var N = 100;
    QB.widget(el, {
      title: "Herding without news",
      sub: "A hundred traders each hold one of two views. At every meeting one of them either changes its mind on its own (with probability ε) or copies whoever it meets. When ε is small the crowd spends its time at the extremes and flips between them for no reason at all.",
      panels: 2, weights: [1.5, 1], height: 290,
      controls: [{ k: "eps", label: "Chance of changing one's mind independently ε", min: -3.7, max: -1, step: 0.05, value: -2.7, fmt: function (x) { return Math.pow(10, x).toPrecision(2); } }],
      buttons: [{ label: "Restart", act: function (s) { s.k = 50; s.path = []; s.hist = new Array(N + 1).fill(0); } }],
      init: function (s) { s.r = QB.rng(3); s.k = 50; s.path = []; s.hist = new Array(N + 1).fill(0); },
      onChange: function (v, s) { s.hist = new Array(N + 1).fill(0); },
      animate: function (v, s) {
        var eps = Math.pow(10, v.eps), i, r = s.r;
        for (i = 0; i < 4000; i++) { var k = s.k, up = (N - k) / N * (eps + (1 - eps) * k / (N - 1)), dn = k / N * (eps + (1 - eps) * (N - k) / (N - 1)), u = r(); if (u < up) s.k++; else if (u < up + dn) s.k--; s.hist[s.k]++; if (i % 80 === 0) { s.path.push(s.k); if (s.path.length > 900) s.path.shift(); } }
        return true;
      },
      draw: function (g, v, s) {
        var eps = Math.pow(10, v.eps), al = eps * (N - 1) / (1 - eps), a = g[0].axes({ x: [0, 900], y: [0, N], title: "Traders holding view A", xlabel: "time (most recent at the right)", xticks: [] });
        a.hline(50); a.line(s.path.map(function (_, i) { return 900 - s.path.length + i; }), s.path, { color: C.spot, width: 1.4 });
        var tot = s.hist.reduce(function (x, y) { return x + y; }, 0) || 1, hh = s.hist.map(function (c) { return c / tot; }), xs = QB.linspace(0, N, N + 1), logp = [0], k, mx = -1e9, st;
        for (k = 0; k < N; k++) logp.push(logp[k] + Math.log((N - k) * (eps + (1 - eps) * k / (N - 1))) - Math.log((k + 1) * (eps + (1 - eps) * (N - k - 1) / (N - 1))));
        logp.forEach(function (l) { mx = Math.max(mx, l); }); st = logp.map(function (l) { return Math.exp(l - mx); }); var ssum = st.reduce(function (x, y) { return x + y; }, 0); st = st.map(function (x) { return x / ssum; });
        var top = Math.max(0.03, Math.max.apply(null, st) * 1.2, Math.max.apply(null, hh) * 1.1), b = g[1].axes({ x: [-1, N + 1], y: [0, Math.min(top, 0.25)], title: "Time spent at each split", xlabel: "traders holding view A" });
        b.bars(xs, hh, 1, { color: C.spot, gap: 0 }); b.line(xs, st, { color: C.p, width: 2 });
        b.legend([["this run", C.spot], ["exact stationary law", C.p]], { pos: "tr" });
        s.out = [al, s.k, hh.slice(0, 11).concat(hh.slice(90)).reduce(function (x, y) { return x + y; }, 0)];
      },
      readout: function (v, s) { return [["ε(N − 1)/(1 − ε)", fmt(s.out[0], 2) + (s.out[0] < 1 ? " (< 1: two humps)" : " (> 1: one hump)")], ["now", s.out[1] + " of 100 hold A"], ["time with over 90% on one side", pct(s.out[2], 0)]]; },
      note: "Kirman (1993). The stationary law is close to a Beta(α, α) with α = ε(N − 1)/(1 − ε): below one, the middle is the least likely place to find the crowd.",
    });
  };

  // ---- Part 43: skill or luck -------------------------------------------------------------------------------------------------------------
  W.skill = function (el) {
    QB.widget(el, {
      title: "Of the funds that look skilled, how many are?",
      sub: "Two thousand funds. A few have real alpha before costs; the rest have none. After T years each has a t-statistic, and the ones above 2 are called skilled. Count how many of them really are.",
      panels: 2, height: 300,
      controls: [
        { k: "pi", label: "Funds with real skill", min: 0, max: 30, step: 0.5, value: 3, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "al", label: "Their alpha, a year", min: 0.5, max: 8, step: 0.25, value: 3, fmt: function (x) { return x.toFixed(2) + "%"; } },
        { k: "T", label: "Years of track record", min: 1, max: 40, step: 1, value: 10, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New funds", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var M = 2000, te = 5, r = QB.rng(s.seed + 1900), nS = Math.round(M * v.pi / 100), mu = v.al / te * Math.sqrt(v.T), t = [], i;
        for (i = 0; i < M; i++) t.push((i < nS ? mu : 0) + r.normal());
        var win = 0, winS = 0, big = 0; for (i = 0; i < M; i++) { if (t[i] > 2) { win++; if (i < nS) winS++; } }
        var ps = t.map(function (x) { return 2 * (1 - QB.cdf(Math.abs(x))); }); ps.forEach(function (p) { if (p > 0.5) big++; });
        var pi0 = Math.min(1, big / (M * 0.5)), power = 1 - QB.cdf(2 - mu), ppv = v.pi / 100 * power / (v.pi / 100 * power + (1 - v.pi / 100) * 0.0228 + 1e-12);
        s.out = [win, winS, pi0, ppv, power];
        var hn = QB.hist(t.slice(nS), -4, 8, 48), hs = QB.hist(t.slice(0, nS), -4, 8, 48), xs = QB.linspace(-3.875, 7.875, 48), top = Math.max.apply(null, hn) * 1.15;
        var a = g[0].axes({ x: [-4, 8], y: [0, top], title: "t-statistics of the funds' alphas", xlabel: "t-statistic" });
        a.bars(xs, hn.map(function (c, j) { return c + hs[j]; }), 0.25, { color: C.gain }); a.bars(xs, hn, 0.25, { color: C.cash, alpha: 1 });
        a.vline(2, { color: C.p }); a.text(2, top * 0.92, " called skilled", { color: C.p }); a.legend([["no skill", C.cash], ["skilled", C.gain]], { pos: "tl" });
        var Ts = QB.linspace(1, 40, 60), b = g[1].axes({ x: [0, 40], y: [0, 1], title: "Share of the 'skilled' who really are", xlabel: "years of track record", yfmt: function (y) { return (100 * y).toFixed(0) + "%"; } });
        b.line(Ts, Ts.map(function (T) { var pw = 1 - QB.cdf(2 - v.al / te * Math.sqrt(T)); return v.pi / 100 * pw / (v.pi / 100 * pw + (1 - v.pi / 100) * 0.0228 + 1e-12); }), { color: C.gain, width: 2.2 });
        b.line(Ts, Ts.map(function (T) { return 1 - QB.cdf(2 - v.al / te * Math.sqrt(T)); }), { color: C.spot, width: 1.6, dash: [5, 4] });
        b.vline(v.T); b.legend([["of those above t = 2, truly skilled", C.gain], ["of the skilled, found", C.spot]], { pos: "br" });
      },
      readout: function (v, s) { return [["funds above t = 2", String(s.out[0])], ["of which truly skilled", s.out[1] + (s.out[0] ? " (" + pct(s.out[1] / s.out[0], 0) + ")" : "")], ["expected share", pct(s.out[3], 0)], ["Storey's estimate of the no-skill share", pct(s.out[2], 0)]]; },
      note: "Tracking error 5% a year, so the t-statistic of a skilled fund is centred on α√T / 5. With 3% of funds skilled it takes decades before a good record means a good manager.",
    });
  };
})();
