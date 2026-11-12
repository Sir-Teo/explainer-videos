// Interactives for Act III, second half (Parts 16-22).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, pct = QB.pct;

  function vdc(i, base) { var f = 1, x = 0; while (i > 0) { f /= base; x += f * (i % base); i = Math.floor(i / base); } return x; }

  // ---- Part 16: Monte Carlo, antithetic pairs, low-discrepancy points ---------------------------------------------------
  W.mc = function (el) {
    QB.widget(el, {
      title: "Three ways to average a payoff",
      sub: "A one-year call struck at 110 on a stock at 100, 20% volatility. The same number of terminal prices is drawn at random, in antithetic pairs, and from a low-discrepancy sequence. Watch each estimate close on the Black-Scholes price.",
      panels: 2, weights: [1.35, 1], height: 300,
      controls: [{ k: "n", label: "Paths", min: 4, max: 15, step: 1, value: 10, fmt: function (x) { return Math.pow(2, x).toLocaleString("en-US"); } }],
      buttons: [{ label: "New random numbers", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var N = Math.pow(2, v.n), sig = 0.2, K = 110, exact = QB.bs(100, K, 1, sig).price, r = QB.rng(s.seed + 500), i;
        var pay = function (z) { return Math.max(100 * Math.exp(-0.5 * sig * sig + sig * z) - K, 0); };
        var runP = [], runA = [], runQ = [], xs = [], sp = 0, sa = 0, sq = 0, sp2 = 0, shift = r();
        for (i = 1; i <= N; i++) {
          var z = r.normal(), p = pay(z); sp += p; sp2 += p * p;
          sa += i % 2 ? pay(z) : pay(-s.lastZ); s.lastZ = z;
          var u = (vdc(i, 2) + shift) % 1; sq += pay(QB.inv(Math.min(Math.max(u, 1e-9), 1 - 1e-9)));
          if (i >= 8 && (i & (i - 1)) === 0 || i === N || (i > 16 && i % Math.ceil(N / 200) === 0)) { xs.push(i); runP.push(sp / i); runA.push(sa / i); runQ.push(sq / i); }
        }
        var se = Math.sqrt((sp2 / N - (sp / N) * (sp / N)) / N);
        s.out = [exact, sp / N, sa / N, sq / N, se];
        var a = g[0].axes({ x: [8, Math.max(N, 16)], y: [exact - 2.2, exact + 2.2], logx: true, title: "Running estimate of the price", xlabel: "paths used" });
        a.area(xs, xs.map(function (n) { return exact + 1.96 * se * Math.sqrt(N / n); }), xs.map(function (n) { return exact - 1.96 * se * Math.sqrt(N / n); }), { color: C.cash, alpha: 0.16 });
        a.hline(exact, { color: C.ink, dash: null }); a.line(xs, runP, { color: C.cash, width: 1.6 }); a.line(xs, runA, { color: C.spot, width: 1.6 }); a.line(xs, runQ, { color: C.option, width: 2 });
        a.legend([["random", C.cash], ["antithetic pairs", C.spot], ["low-discrepancy", C.option], ["Black-Scholes", C.ink]], { pos: "tr" });
        var M = Math.min(N, 1024), b = g[1].axes({ x: [0, 1], y: [0, 1], title: "The first " + M + " points in two dimensions", noX: true, noY: true, xticks: [], yticks: [] });
        var px = [], py = [], qx = [], qy = [], r2 = QB.rng(s.seed + 501);
        for (i = 1; i <= M; i++) { px.push(r2() * 0.48); py.push(r2()); qx.push(0.52 + vdc(i, 2) * 0.48); qy.push(vdc(i, 3)); }
        b.dots(px, py, { color: C.cash, r: 1.6 }); b.dots(qx, qy, { color: C.option, r: 1.6 });
        b.text(0.24, 0.04, "random", { color: C.cash, align: "center", bg: true }); b.text(0.76, 0.04, "low-discrepancy", { color: C.option, align: "center", bg: true });
      },
      readout: function (v, s) {
        var e = function (x) { return fmt(x, 3) + " (error " + fmt(x - s.out[0], 3) + ")"; };
        return [["exact", fmt(s.out[0], 3)], ["random", e(s.out[1])], ["antithetic", e(s.out[2])], ["low-discrepancy", e(s.out[3])], ["95% band", "±" + fmt(1.96 * s.out[4], 3)]];
      },
      note: "The grey band is ±1.96 standard errors of the plain estimate: it narrows like 1/√n. Evenly spread points narrow like 1/n.",
    });
  };

  // ---- Part 17: hedging with costs: the no-trade band --------------------------------------------------------------------
  W.band = function (el) {
    QB.widget(el, {
      title: "Where not to trade",
      sub: "A sold three-month call, hedged daily with a proportional cost. Instead of chasing delta every day, hold the position until it leaves a band around delta. A learned hedger finds the same shape: a wider band costs less and risks more.",
      panels: 2, height: 300,
      controls: [
        { k: "cost", label: "Cost per trade", min: 0, max: 100, step: 5, value: 30, fmt: function (x) { return x + " bp of notional"; } },
        { k: "band", label: "Half-width of the band, in delta", min: 0, max: 0.3, step: 0.01, value: 0.08, fmt: function (x) { return "±" + x.toFixed(2); } },
      ],
      buttons: [{ label: "New paths", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var T = 0.25, N = 63, dt = T / N, sig = 0.2, c = v.cost / 1e4, prem = QB.bs(100, 100, T, sig).price, paths = 400;
        var run = function (hw, seed, keep) {
          var r = QB.rng(seed), pnl = [], cs = 0, k, i, rec = null;
          for (k = 0; k < paths; k++) {
            var S = 100, d = QB.bs(S, 100, T, sig).delta, pos = d, cash = prem - pos * S - c * pos * S, cc = c * pos * S;
            if (keep && k === 0) rec = [[0, d, pos]];
            for (i = 1; i < N; i++) {
              S *= Math.exp(-0.5 * sig * sig * dt + sig * Math.sqrt(dt) * r.normal()); d = QB.bs(S, 100, T - i * dt, sig).delta;
              if (Math.abs(d - pos) > hw) { var tgt = d > pos ? d - hw : d + hw, tr = tgt - pos; cash -= tr * S + c * Math.abs(tr) * S; cc += c * Math.abs(tr) * S; pos = tgt; }
              if (rec && k === 0) rec.push([i * dt, d, pos]);
            }
            S *= Math.exp(-0.5 * sig * sig * dt + sig * Math.sqrt(dt) * r.normal());
            pnl.push(cash + pos * S - c * pos * S - Math.max(S - 100, 0)); cs += cc + c * pos * S;
          }
          return { sd: QB.sd(pnl), mean: QB.mean(pnl), cost: cs / paths, rec: rec };
        };
        var key = v.cost + ":" + s.seed;
        if (s.key !== key) { s.key = key; s.sweep = QB.linspace(0, 0.3, 13).map(function (hw) { var o = run(hw, s.seed + 600, false); o.hw = hw; return o; }); }
        var me = run(v.band, s.seed + 600, true); s.out = [me.mean, me.sd, me.cost];
        var a = g[0].axes({ x: [0, T], y: [0, 1], title: "One path: delta, the band, and the position held", xlabel: "years" });
        var ts = me.rec.map(function (p) { return p[0]; }), ds = me.rec.map(function (p) { return p[1]; });
        a.area(ts, ds.map(function (d) { return Math.min(1, d + v.band); }), ds.map(function (d) { return Math.max(0, d - v.band); }), { color: C.idea, alpha: 0.16 });
        a.line(ts, ds, { color: C.idea, width: 1.2 }); a.line(ts, me.rec.map(function (p) { return p[2]; }), { color: C.gain, width: 2.2 });
        a.legend([["Black-Scholes delta", C.idea], ["shares actually held", C.gain]], { pos: "tl" });
        var b = g[1].axes({ x: [0, Math.max(0.6, s.sweep[0].cost * 1.1)], y: [0, Math.max(1.2, s.sweep[12].sd * 1.1)], title: "Every band width: cost paid against risk kept", xlabel: "average cost paid" });
        b.line(s.sweep.map(function (o) { return o.cost; }), s.sweep.map(function (o) { return o.sd; }), { color: C.cash, width: 1.6 });
        b.dots(s.sweep.map(function (o) { return o.cost; }), s.sweep.map(function (o) { return o.sd; }), { color: C.cash, r: 3 });
        b.dots([me.cost], [me.sd], { color: C.gain, r: 6 }); b.text(me.cost, me.sd, "  your band", { color: C.gain });
      },
      readout: function (v, s) { return [["mean P&L", fmt(s.out[0], 2)], ["sd of P&L", fmt(s.out[1], 2)], ["cost paid", fmt(s.out[2], 2)]]; },
      note: "400 simulated paths per band. Whalley and Wilmott's asymptotic band is proportional to (cost × Γ²)^(1/3): widest where gamma is largest.",
    });
  };

  // ---- Part 18: the yield curve in three numbers --------------------------------------------------------------------------
  W.curve = function (el) {
    QB.widget(el, {
      title: "Level, slope, curvature",
      sub: "The Nelson-Siegel curve: y(τ) = β₀ + β₁·(1 − e^(−τ/λ))/(τ/λ) + β₂·((1 − e^(−τ/λ))/(τ/λ) − e^(−τ/λ)). Three numbers move almost every yield curve ever observed.",
      panels: 2, weights: [1.3, 1], height: 300,
      controls: [
        { k: "b0", label: "Level β₀ (the long end)", min: 0, max: 8, step: 0.1, value: 4.5, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "b1", label: "Slope β₁ (short minus long)", min: -5, max: 5, step: 0.1, value: -1.5, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "b2", label: "Curvature β₂ (the hump)", min: -6, max: 6, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "lam", label: "Where the hump sits λ", min: 0.5, max: 5, step: 0.1, value: 1.8, fmt: function (x) { return x.toFixed(1) + " years"; } },
      ],
      draw: function (g, v, s) {
        var l1 = function (t) { var x = t / v.lam; return (1 - Math.exp(-x)) / x; }, l2 = function (t) { return l1(t) - Math.exp(-t / v.lam); };
        var y = function (t) { return v.b0 + v.b1 * l1(t) + v.b2 * l2(t); }, f = function (t) { var e = Math.exp(-t / v.lam); return v.b0 + v.b1 * e + v.b2 * (t / v.lam) * e; };
        var ts = QB.linspace(0.05, 30, 200), ys = ts.map(y), fs = ts.map(f), lo = Math.min(-0.5, Math.min.apply(null, ys.concat(fs)) - 0.4), hi = Math.max(8, Math.max.apply(null, ys.concat(fs)) + 0.4);
        var a = g[0].axes({ x: [0, 30], y: [lo, hi], title: "Zero yields and forward rates, %", xlabel: "maturity, years" });
        a.hline(0, { dash: null }); a.line(ts, fs, { color: C.q, width: 1.4, dash: [5, 4] }); a.line(ts, ys, { color: C.p, width: 2.4 });
        a.dots([2, 10, 30], [y(2), y(10), y(30)], { color: C.ink, r: 3.5 });
        a.legend([["zero yield", C.p], ["instantaneous forward", C.q]], { pos: "br" });
        var b = g[1].axes({ x: [0, 30], y: [0, 1.05], title: "What one unit of each factor does to the curve", xlabel: "maturity, years" });
        b.line(ts, ts.map(function () { return 1; }), { color: C.p, width: 2 }); b.line(ts, ts.map(l1), { color: C.spot, width: 2 }); b.line(ts, ts.map(l2), { color: C.option, width: 2 });
        b.legend([["level", C.p], ["slope", C.spot], ["curvature", C.option]], { pos: "tr" });
        var price = 0, dur = 0, t; for (t = 0.5; t <= 10; t += 0.5) { var cf = (t === 10 ? 102 : 2), df = Math.exp(-y(t) / 100 * t); price += cf * df; dur += t * cf * df; }
        s.out = [y(2), y(10), y(10) - y(2), price, dur / price];
      },
      readout: function (v, s) { return [["2-year", fmt(s.out[0], 2) + "%"], ["10-year", fmt(s.out[1], 2) + "%"], ["2s10s slope", fmt(100 * s.out[2], 0) + " bp" + (s.out[2] < 0 ? " (inverted)" : "")], ["10-year 4% bond", fmt(s.out[3], 1) + ", duration " + fmt(s.out[4], 1) + " y"]]; },
      note: "A parallel rise of one point costs the ten-year bond about its duration in percent: roughly eight.",
    });
  };

  // ---- Part 19: a short-rate model draws the whole curve --------------------------------------------------------------------
  W.vasicek = function (el) {
    QB.widget(el, {
      title: "One short rate, a whole curve",
      sub: "Vasicek's model: dr = a(b − r)dt + σdW. Every bond price is the expected discount factor along these paths, and it has a closed form. Move today's rate above or below its long-run mean and the curve inverts or steepens.",
      panels: 2, height: 300,
      controls: [
        { k: "r0", label: "Today's short rate", min: -1, max: 9, step: 0.1, value: 1.5, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "b", label: "Long-run mean b", min: 0, max: 8, step: 0.1, value: 4, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "a", label: "Mean reversion a", min: 0.05, max: 2, step: 0.05, value: 0.4, fmt: function (x) { return x.toFixed(2); } },
        { k: "sig", label: "Volatility σ", min: 0.1, max: 3, step: 0.1, value: 1.2, fmt: function (x) { return x.toFixed(1) + "% a year"; } },
      ],
      buttons: [{ label: "New paths", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var a_ = v.a, b_ = v.b / 100, sg = v.sig / 100, r0 = v.r0 / 100, n = 240, T = 20, dt = T / n, r = QB.rng(s.seed + 700), k, i, xs = QB.linspace(0, T, n + 1);
        var ax = g[0].axes({ x: [0, T], y: [-4, 12], title: "Thirty short-rate paths, %", xlabel: "years" }), e = Math.exp(-a_ * dt), sdStep = sg * Math.sqrt((1 - e * e) / (2 * a_));
        for (k = 0; k < 30; k++) { var x = r0, ys = [100 * x]; for (i = 1; i <= n; i++) { x = b_ + (x - b_) * e + sdStep * r.normal(); ys.push(100 * x); } ax.line(xs, ys, { color: C.spot, width: 1, alpha: 0.45 }); }
        ax.hline(v.b, { color: C.p }); ax.hline(0, { dash: null });
        var yld = function (t) { var B = (1 - Math.exp(-a_ * t)) / a_, A = (b_ - sg * sg / (2 * a_ * a_)) * (B - t) - sg * sg * B * B / (4 * a_); return -(A - B * r0) / t; };
        var ts = QB.linspace(0.1, 30, 150), ys2 = ts.map(function (t) { return 100 * yld(t); }), bx = g[1].axes({ x: [0, 30], y: [Math.min(-1, Math.min.apply(null, ys2) - 0.5), Math.max(9, Math.max.apply(null, ys2) + 0.5)], title: "The yield curve the model implies, %", xlabel: "maturity, years" });
        var inf = 100 * (b_ - sg * sg / (2 * a_ * a_)); bx.hline(inf, { color: C.muted }); bx.hline(0, { dash: null }); bx.line(ts, ys2, { color: C.p, width: 2.4 });
        bx.text(30, inf, "long-run yield", { color: C.muted, align: "right", dy: -8 });
        var m5 = b_ + (r0 - b_) * Math.exp(-5 * a_), s5 = sg * Math.sqrt((1 - Math.exp(-10 * a_)) / (2 * a_));
        s.out = [100 * yld(2), 100 * yld(10), inf, QB.cdf(-m5 / s5)];
      },
      readout: function (v, s) { return [["2-year yield", fmt(s.out[0], 2) + "%"], ["10-year yield", fmt(s.out[1], 2) + "%"], ["yield as T → ∞", fmt(s.out[2], 2) + "% (b − σ²/2a²)"], ["half-life of a shock", fmt(Math.log(2) / v.a, 1) + " y"], ["P(short rate < 0 in 5 years)", pct(s.out[3], 1)]]; },
      note: "The long yield sits below b by a convexity term. Vasicek's rate can go negative; that used to be called a flaw.",
    });
  };

  // ---- Part 20: correlation decides who loses --------------------------------------------------------------------------------
  W.pool = function (el) {
    QB.widget(el, {
      title: "One number decides whether the senior tranche is safe",
      sub: "A large pool of loans, each with the same default probability, driven by one common factor with correlation ρ (Vasicek's model, the one inside the Basel formula). The pool's expected loss does not depend on ρ. Who bears it does.",
      panels: 2, height: 300,
      controls: [
        { k: "pd", label: "Default probability of each loan", min: 0.5, max: 12, step: 0.5, value: 3, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "rho", label: "Asset correlation ρ", min: 0.01, max: 0.7, step: 0.01, value: 0.15, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var p = v.pd / 100, th = QB.inv(p), tr = [[0, 0.03, C.loss, "equity 0-3%"], [0.03, 0.07, C.p, "mezzanine 3-7%"], [0.07, 1, C.spot, "senior 7-100%"]];
        var dens = function (x, rho) { var q = QB.inv(Math.min(Math.max(x, 1e-9), 1 - 1e-9)), a = (Math.sqrt(1 - rho) * q - th) / Math.sqrt(rho); return Math.sqrt((1 - rho) / rho) * QB.pdf(a) / QB.pdf(q); };
        var el_ = function (rho, lo, hi) { var acc = 0, i, n = 400; for (i = 0; i < n; i++) { var m = -6 + 12 * (i + 0.5) / n, L = QB.cdf((th - Math.sqrt(rho) * m) / Math.sqrt(1 - rho)); acc += QB.pdf(m) * 12 / n * (Math.min(L, hi) - Math.min(L, lo)) / (hi - lo); } return acc; };
        var xs = QB.linspace(0.0005, 0.3, 300), ds = xs.map(function (x) { return dens(x, v.rho); }), top = Math.min(80, Math.max.apply(null, ds) * 1.1);
        var a = g[0].axes({ x: [0, 0.3], y: [0, top], title: "Share of the pool that defaults: its distribution", xlabel: "fraction of loans in default", xfmt: function (x) { return (100 * x).toFixed(0) + "%"; } });
        tr.forEach(function (t) { var sub = xs.filter(function (x) { return x >= t[0] && x <= Math.min(t[1], 0.3); }); if (sub.length > 1) a.area(sub, sub.map(function (x) { return Math.min(top, dens(x, v.rho)); }), 0, { color: t[2], alpha: 0.35 }); });
        a.line(xs, ds, { color: C.ink, width: 1.8 }); a.vline(p, { color: C.muted }); a.text(p, top * 0.93, " expected", { color: C.muted });
        var q999 = QB.cdf((th + Math.sqrt(v.rho) * QB.inv(0.999)) / Math.sqrt(1 - v.rho));
        var rs = QB.linspace(0.01, 0.7, 40), b = g[1].axes({ x: [0, 0.7], y: [0.0001, 1], logy: true, title: "Expected loss of each tranche against ρ", xlabel: "asset correlation ρ", yfmt: function (y) { return y >= 0.01 ? (100 * y).toFixed(0) + "%" : (100 * y) + "%"; } });
        var now = [];
        tr.forEach(function (t) { b.line(rs, rs.map(function (r) { return Math.max(1e-6, el_(r, t[0], t[1])); }), { color: t[2], width: 2 }); var e = el_(v.rho, t[0], t[1]); now.push(e); b.dots([v.rho], [Math.max(1e-4, e)], { color: t[2], r: 4.5 }); });
        b.vline(v.rho); b.legend(tr.map(function (t) { return [t[3], t[2]]; }), { pos: "br" });
        s.out = [now, q999];
      },
      readout: function (v, s) { return [["equity loses", pct(s.out[0][0], 1)], ["mezzanine", pct(s.out[0][1], 2)], ["senior", pct(s.out[0][2], 3)], ["99.9% worst default rate", pct(s.out[1], 1)]]; },
      note: "No recovery, a large homogeneous pool. Raising ρ moves loss from the equity tranche to the senior one: equity is long correlation, senior is short it.",
    });
  };

  // ---- Part 21: exposure, collateral, CVA ----------------------------------------------------------------------------------------
  W.cva = function (el) {
    QB.widget(el, {
      title: "The loan hidden inside a swap",
      sub: "A ten-year payer swap, notional 100. Its value wanders as rates move; whenever it is positive, the counterparty owes you. Collateral removes all but what can build up during the days it takes to close out a defaulter.",
      panels: 2, height: 300,
      controls: [
        { k: "sig", label: "Rate volatility", min: 20, max: 200, step: 5, value: 90, fmt: function (x) { return x + " bp a year"; } },
        { k: "mpor", label: "Days to close out", min: 0, max: 30, step: 1, value: 0, fmt: function (x) { return x === 0 ? "no collateral" : x + " (margined)"; } },
        { k: "haz", label: "Counterparty's credit spread", min: 20, max: 800, step: 10, value: 150, fmt: function (x) { return x + " bp"; } },
      ],
      buttons: [{ label: "New paths", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var T = 10, n = 240, dt = T / n, paths = 800, r = QB.rng(s.seed + 800), sg = v.sig / 1e4, lag = Math.round(v.mpor / 252 / dt * 10) / 10, k, i;
        var ann = function (t) { return (1 - Math.exp(-0.03 * (T - t))) / 0.03; }, V = [], xs = QB.linspace(0, T, n + 1), EE = new Array(n + 1).fill(0), all = [];
        for (i = 0; i <= n; i++) all.push([]);
        var a = g[0].axes({ x: [0, T], y: [-22, 22], title: "Value of the swap to you on 40 paths", xlabel: "years" });
        for (k = 0; k < paths; k++) {
          var x = 0, vv = [0];
          for (i = 1; i <= n; i++) { x += sg * Math.sqrt(dt) * r.normal(); vv.push(100 * x * ann(i * dt)); }
          for (i = 0; i <= n; i++) { var e; if (v.mpor === 0) e = Math.max(vv[i], 0); else { var back = Math.max(0, i - Math.max(1, Math.round(v.mpor / 252 / dt))); e = Math.max(vv[i] - vv[back], 0); } EE[i] += e / paths; all[i].push(e); }
          if (k < 40) a.line(xs, vv, { color: C.spot, width: 1, alpha: 0.4 });
        }
        a.hline(0, { dash: null });
        var PFE = all.map(function (col) { return QB.quantile(col, 0.95); }), lam = v.haz / 1e4 / 0.6, cva = 0;
        for (i = 1; i <= n; i++) cva += 0.6 * EE[i] * Math.exp(-0.03 * i * dt) * (Math.exp(-lam * (i - 1) * dt) - Math.exp(-lam * i * dt));
        var top = Math.max(2, Math.max.apply(null, PFE) * 1.1), b = g[1].axes({ x: [0, T], y: [0, top], title: "Exposure: expected, and the 95% worst case", xlabel: "years" });
        b.area(xs, EE, 0, { color: C.loss, alpha: 0.3 }); b.line(xs, EE, { color: C.loss, width: 2 }); b.line(xs, PFE, { color: C.p, width: 1.6, dash: [5, 4] });
        b.legend([["expected exposure", C.loss], ["95% potential future exposure", C.p]], { pos: "tr" });
        s.out = [Math.max.apply(null, EE), cva, cva / ann(0) * 100, lag];
      },
      readout: function (v, s) { return [["peak expected exposure", fmt(s.out[0], 2)], ["CVA", fmt(s.out[1], 3) + " per 100"], ["as a running spread", fmt(s.out[2], 1) + " bp"]]; },
      note: "Simulated: a driftless normal swap rate, a 3% discount rate, 40% recovery, hazard = spread / 0.6. The hump is the swap's annuity shrinking while rates have had time to move.",
    });
  };

  // ---- Part 22: carry in a forward curve ---------------------------------------------------------------------------------------------
  W.carry = function (el) {
    QB.widget(el, {
      title: "The forward curve, and what the roll pays",
      sub: "A commodity's forward price is the spot plus financing and storage, less the convenience of having the barrel: F = S·e^((r + u − y)T). Hold the front contract and roll it each month and you earn the slope of the curve, whatever the spot does.",
      panels: 2, height: 300,
      controls: [
        { k: "r", label: "Interest rate r", min: 0, max: 10, step: 0.25, value: 4, fmt: function (x) { return x.toFixed(2) + "%"; } },
        { k: "u", label: "Storage cost u", min: 0, max: 40, step: 0.5, value: 3, fmt: function (x) { return x.toFixed(1) + "% a year"; } },
        { k: "y", label: "Convenience yield y", min: 0, max: 40, step: 0.5, value: 12, fmt: function (x) { return x.toFixed(1) + "% a year"; } },
      ],
      buttons: [{ label: "New spot path", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var c = (v.r + v.u - v.y) / 100, ms = QB.linspace(0, 24, 25), F = ms.map(function (m) { return 80 * Math.exp(c * m / 12); });
        var a = g[0].axes({ x: [0, 24], y: [Math.min(50, F[24] - 5), Math.max(110, F[24] + 5)], title: c > 0 ? "Forward curve: contango" : c < 0 ? "Forward curve: backwardation" : "Forward curve: flat", xlabel: "months to delivery" });
        a.hline(80); a.line(ms, F, { color: c > 0 ? C.loss : C.gain, width: 2.4 }); a.dots(ms, F, { color: c > 0 ? C.loss : C.gain, r: 2.5 }); a.text(0.5, 80, "spot 80", { color: C.muted, dy: -9 });
        var r = QB.rng(s.seed + 900), n = 36, spot = [0], roll = [0], i;
        for (i = 1; i <= n; i++) { var ds = 0.3 / Math.sqrt(12) * r.normal(); spot.push(spot[i - 1] + ds); roll.push(roll[i - 1] + ds - c / 12); }
        var lo = Math.min(Math.min.apply(null, spot), Math.min.apply(null, roll)) - 0.1, hi = Math.max(Math.max.apply(null, spot), Math.max.apply(null, roll)) + 0.1;
        var b = g[1].axes({ x: [0, n], y: [lo, hi], title: "Three years: the spot, and the rolled front contract", xlabel: "month", yfmt: function (y) { return (100 * y).toFixed(0) + "%"; } });
        b.hline(0, { dash: null }); b.line(QB.linspace(0, n, n + 1), spot, { color: C.cash, width: 1.8 }); b.line(QB.linspace(0, n, n + 1), roll, { color: c > 0 ? C.loss : C.gain, width: 2.2 });
        b.legend([["spot price (log)", C.cash], ["long the front, rolled", c > 0 ? C.loss : C.gain]], { pos: "tl" });
        s.out = [c, F[12], -c];
      },
      readout: function (v, s) { return [["slope of the curve r + u − y", pct(s.out[0], 1) + " a year"], ["12-month forward", fmt(s.out[1], 2)], ["roll return", pct(s.out[2], 1) + " a year"]]; },
      note: "In April 2020 storage ran out: u spiked, the front contract fell far below the spot of a month later, and on 20 April it settled at −37.63 dollars.",
    });
  };
})();
