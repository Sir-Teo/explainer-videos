// Interactives for Acts IV-V (Parts 23-34).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, pct = QB.pct;

  function solve(A, b) { // Gaussian elimination with partial pivoting; A is small
    var n = b.length, M = A.map(function (r, i) { return r.concat([b[i]]); }), i, j, k;
    for (i = 0; i < n; i++) {
      var p = i; for (j = i + 1; j < n; j++) if (Math.abs(M[j][i]) > Math.abs(M[p][i])) p = j;
      var t = M[i]; M[i] = M[p]; M[p] = t;
      for (j = i + 1; j < n; j++) { var f = M[j][i] / M[i][i]; for (k = i; k <= n; k++) M[j][k] -= f * M[i][k]; }
    }
    var x = new Array(n);
    for (i = n - 1; i >= 0; i--) { var sum = M[i][n]; for (j = i + 1; j < n; j++) sum -= M[i][j] * x[j]; x[i] = sum / M[i][i]; }
    return x;
  }
  function quad(w, S) { var s = 0, i, j; for (i = 0; i < w.length; i++) for (j = 0; j < w.length; j++) s += w[i] * S[i][j] * w[j]; return s; }
  function dot(a, b) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i] * b[i]; return s; }
  var MU = [0.04, 0.07, 0.10], SD = [0.10, 0.18, 0.26];
  function cov(rho) { return SD.map(function (a, i) { return SD.map(function (b, j) { return i === j ? a * a : rho * a * b; }); }); }
  function tangency(mu, S, rf) { var w = solve(S, mu.map(function (m) { return m - rf; })), t = w[0] + w[1] + w[2]; return w.map(function (x) { return x / t; }); }
  function frontier(mu, S) { // minimum volatility for each target mean, fully invested
    var one = [1, 1, 1], a = solve(S, mu), b = solve(S, one), A = dot(one, a), B = dot(mu, a), Cc = dot(one, b), D = B * Cc - A * A;
    return function (m) { return Math.sqrt(Math.max(0, (Cc * m * m - 2 * A * m + B) / D)); };
  }

  // ---- Part 23: the frontier and the tangency portfolio -----------------------------------------------------------------
  W.frontier = function (el) {
    QB.widget(el, {
      title: "Diversification, the frontier and the best portfolio",
      sub: "Three assets with expected excess returns of 4%, 7% and 10% and volatilities of 10%, 18% and 26%. Lower their correlation and the frontier bends left: risk that can be diversified away earns nothing. The line from cash touches the frontier at the tangency portfolio.",
      panels: 2, weights: [1.5, 1], height: 310,
      controls: [
        { k: "rho", label: "Correlation between the assets", min: -0.3, max: 0.95, step: 0.05, value: 0.3, fmt: function (x) { return x.toFixed(2); } },
        { k: "rf", label: "Cash rate", min: 0, max: 3.5, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1) + "%"; } },
      ],
      draw: function (g, v, s) {
        var S = cov(v.rho), rf = v.rf / 100, f = frontier(MU, S), ms = QB.linspace(0.0, 0.14, 120), w = tangency(MU, S, rf);
        var tm = dot(w, MU), ts = Math.sqrt(quad(w, S)), sr = (tm - rf) / ts, gm = solve(S, [1, 1, 1]), gt = gm[0] + gm[1] + gm[2]; gm = gm.map(function (x) { return x / gt; });
        var a = g[0].axes({ x: [0, 0.32], y: [0, 0.14], title: "Expected return against volatility", xlabel: "volatility", xfmt: function (x) { return (100 * x).toFixed(0) + "%"; }, yfmt: function (y) { return (100 * y).toFixed(0) + "%"; } });
        a.line(ms.map(f), ms, { color: C.p, width: 2.4 });
        a.line([0, 0.32], [rf, rf + sr * 0.32], { color: C.gain, width: 1.5 });
        a.dots(SD, MU, { color: C.spot, r: 5 }); ["A", "B", "C"].forEach(function (n, i) { a.text(SD[i], MU[i], n, { color: C.spot, dx: 9, bold: true }); });
        a.dots([ts], [tm], { color: C.gain, r: 6 }); a.text(ts, tm, "tangency", { color: C.gain, dx: -8, dy: -12, align: "right", bg: true });
        a.dots([Math.sqrt(quad(gm, S))], [dot(gm, MU)], { color: C.option, r: 5 }); a.text(Math.sqrt(quad(gm, S)), dot(gm, MU), "minimum variance", { color: C.option, dx: -9, dy: 12, align: "right", bg: true });
        a.dots([0], [rf], { color: C.cash, r: 5 });
        var b = g[1].axes({ x: [-0.6, 2.6], y: [Math.min(-0.5, Math.min.apply(null, w) - 0.1), Math.max(1.2, Math.max.apply(null, w) + 0.15)], title: "Weights of the tangency portfolio", xticks: [0, 1, 2], xfmt: function (x) { return "ABC"[x]; }, yfmt: function (y) { return (100 * y).toFixed(0) + "%"; } });
        b.hline(0, { dash: null }); b.bars([0, 1, 2], w, 0.6, { color: function (i) { return w[i] >= 0 ? C.gain : C.loss; } });
        [0, 1, 2].forEach(function (i) { b.text(i, w[i], pct(w[i], 0), { align: "center", dy: w[i] >= 0 ? -9 : 10, bold: true }); });
        s.out = [sr, Math.max.apply(null, MU.map(function (m, i) { return (m - rf) / SD[i]; }))];
      },
      readout: function (v, s) { return [["Sharpe ratio of the tangency portfolio", fmt(s.out[0], 2)], ["best single asset", fmt(s.out[1], 2)]]; },
      note: "These weights assume the expected returns are known. Part 30's interactive estimates them from data instead.",
    });
  };

  // ---- Part 24: a factor is a sort ------------------------------------------------------------------------------------------
  W.sorts = function (el) {
    QB.widget(el, {
      title: "A factor is a sort",
      sub: "Each month stocks are ranked on a characteristic and split into five portfolios; the factor is the top fifth minus the bottom fifth. A tiny correlation between the characteristic and next month's return, spread across many stocks and months, becomes a visible premium, slowly.",
      panels: 2, height: 300,
      controls: [
        { k: "ic", label: "Correlation with next month's return (IC)", min: 0, max: 0.08, step: 0.002, value: 0.02, fmt: function (x) { return x.toFixed(3); } },
        { k: "n", label: "Stocks", min: 50, max: 3000, step: 50, value: 1000, fmt: function (x) { return String(x); } },
        { k: "T", label: "Months of history", min: 24, max: 720, step: 12, value: 240, fmt: function (x) { return x + " (" + (x / 12).toFixed(0) + " years)"; } },
      ],
      buttons: [{ label: "New history", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var zbar = [-1.4, -0.53, 0, 0.53, 1.4], sig = 0.10, r = QB.rng(s.seed + 1000), sums = [0, 0, 0, 0, 0], ls = [], cum = [0], t, k;
        for (t = 0; t < v.T; t++) { var mkt = 0.006 + 0.045 * r.normal(), q = []; for (k = 0; k < 5; k++) { q.push(mkt + v.ic * sig * zbar[k] + sig / Math.sqrt(v.n / 5) * r.normal()); sums[k] += q[k] / v.T; } ls.push(q[4] - q[0]); cum.push(cum[t] + q[4] - q[0]); }
        var m = QB.mean(ls), sdv = QB.sd(ls), tstat = m / sdv * Math.sqrt(v.T), sr = m / sdv * Math.sqrt(12);
        s.out = [12 * m, tstat, sr, sr > 0.01 ? 4 / (sr * sr) : Infinity];
        var a = g[0].axes({ x: [-0.6, 4.6], y: [0, Math.max(0.016, Math.max.apply(null, sums) * 1.2)], title: "Average monthly return of each fifth", xticks: [0, 1, 2, 3, 4], xfmt: function (x) { return ["lowest", "2", "3", "4", "highest"][x]; }, yfmt: function (y) { return (100 * y).toFixed(1) + "%"; } });
        a.bars([0, 1, 2, 3, 4], sums, 0.7, { color: function (i) { return [C.loss, C.cash, C.cash, C.cash, C.gain][i]; } });
        var lo = Math.min(-0.2, Math.min.apply(null, cum)), hi = Math.max(0.4, Math.max.apply(null, cum));
        var b = g[1].axes({ x: [0, v.T / 12], y: [lo, hi], title: "Top fifth minus bottom fifth, cumulative", xlabel: "years", yfmt: function (y) { return (100 * y).toFixed(0) + "%"; } });
        b.hline(0, { dash: null }); b.line(QB.linspace(0, v.T / 12, v.T + 1), cum, { color: tstat > 2 ? C.gain : C.p, width: 1.8 });
      },
      readout: function (v, s) { return [["premium", pct(s.out[0], 1) + " a year"], ["t-statistic", fmt(s.out[1], 2)], ["Sharpe ratio", fmt(s.out[2], 2)], ["years for t = 2 at this Sharpe", isFinite(s.out[3]) ? fmt(s.out[3], 0) : "never"]]; },
      note: "Simulated. Idiosyncratic volatility 10% a month; the market cancels in the long-short spread. Costs, crowding and crashes are what this picture leaves out.",
    });
  };

  // ---- Part 25: hundreds of tests ---------------------------------------------------------------------------------------------
  W.lucky = function (el) {
    QB.widget(el, {
      title: "How many of the discoveries are real?",
      sub: "M candidate factors are tested at once. Most have no premium; the real ones have t-statistics centred on 3. Three hurdles are drawn: the classical 1.96, Benjamini-Hochberg at a 5% false discovery rate, and Bonferroni.",
      panels: 2, weights: [1.5, 1], height: 300,
      controls: [
        { k: "M", label: "Factors tested", min: 20, max: 2000, step: 20, value: 300, fmt: function (x) { return String(x); } },
        { k: "pi", label: "Share with a real premium", min: 0, max: 40, step: 1, value: 10, fmt: function (x) { return x + "%"; } },
      ],
      buttons: [{ label: "New draw", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 1100), M = v.M, nReal = Math.round(M * v.pi / 100), t = [], real = [], i;
        for (i = 0; i < M; i++) { real.push(i < nReal); t.push((i < nReal ? 3 : 0) + r.normal()); }
        var bonf = QB.inv(1 - 0.05 / (2 * M)), ps = t.map(function (x) { return 2 * (1 - QB.cdf(Math.abs(x))); }), order = ps.map(function (p, j) { return j; }).sort(function (a, b) { return ps[a] - ps[b]; }), kmax = 0;
        for (i = 0; i < M; i++) if (ps[order[i]] <= 0.05 * (i + 1) / M) kmax = i + 1;
        var bh = kmax > 0 ? Math.abs(t[order[kmax - 1]]) - 1e-9 : Infinity;
        var rule = function (thr) { var d = 0, f = 0; for (i = 0; i < M; i++) if (Math.abs(t[i]) > thr) { d++; if (!real[i]) f++; } return [d, f]; };
        s.out = [rule(1.96), rule(bh), rule(bonf), nReal, bh, bonf];
        var hn = QB.hist(t.filter(function (_, j) { return !real[j]; }), -4, 8, 48), hr = QB.hist(t.filter(function (_, j) { return real[j]; }), -4, 8, 48), xs = QB.linspace(-3.875, 7.875, 48);
        var top = Math.max.apply(null, hn.map(function (c, j) { return c + hr[j]; })) * 1.15 + 1, a = g[0].axes({ x: [-4, 8], y: [0, top], title: "The t-statistics, by what they really are", xlabel: "t-statistic" });
        a.bars(xs, hn, 0.25, { color: C.cash }); a.bars(xs, hr.map(function (c, j) { return c + hn[j]; }), 0.25, { color: C.gain, base: 0, alpha: 0.9 }); a.bars(xs, hn, 0.25, { color: C.cash, alpha: 1 });
        a.vline(1.96, { color: C.loss }); a.text(1.96, top * 0.93, "1.96", { color: C.loss, dx: 3 });
        if (isFinite(bh)) { a.vline(bh, { color: C.p }); a.text(bh, top * 0.83, "BH", { color: C.p, dx: 3 }); }
        a.vline(bonf, { color: C.q }); a.text(bonf, top * 0.73, "Bonferroni", { color: C.q, dx: 3 });
        a.legend([["no premium", C.cash], ["real", C.gain]], { pos: "tl" });
        var b = g[1].axes({ x: [-0.6, 2.6], y: [0, Math.max(10, s.out[0][0] * 1.2)], title: "Discoveries: real and false", xticks: [0, 1, 2], xfmt: function (x) { return ["1.96", "BH 5%", "Bonferroni"][x]; } });
        var D = [s.out[0], s.out[1], s.out[2]];
        b.bars([0, 1, 2], D.map(function (d) { return d[0]; }), 0.7, { color: C.loss }); b.bars([0, 1, 2], D.map(function (d) { return d[0] - d[1]; }), 0.7, { color: C.gain, alpha: 1 });
        D.forEach(function (d, j) { b.text(j, d[0], d[0] ? pct(d[1] / d[0], 0) + " false" : "none", { align: "center", dy: -9 }); });
      },
      readout: function (v, s) { return [["real factors", String(s.out[3])], ["found at 1.96", (s.out[0][0] - s.out[0][1]) + " real + " + s.out[0][1] + " false"], ["BH hurdle", isFinite(s.out[4]) ? fmt(s.out[4], 2) : "none pass"], ["Bonferroni hurdle", fmt(s.out[5], 2)]]; },
      note: "The red part of each bar is false discoveries. With few real factors among many tests, most of what clears 1.96 is noise.",
    });
  };

  // ---- Part 26: the best of N backtests ----------------------------------------------------------------------------------------
  W.overfit = function (el) {
    QB.widget(el, {
      title: "The best backtest of many",
      sub: "N strategies with the same true Sharpe ratio are backtested and the best is kept. Its backtest flatters it by an amount that depends only on N and the length of the sample; out of sample it is an ordinary strategy again.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Strategies tried", min: 0, max: 14, step: 1, value: 10, fmt: function (x) { return Math.pow(2, x).toLocaleString("en-US"); } },
        { k: "T", label: "Years of backtest", min: 1, max: 30, step: 1, value: 5, fmt: function (x) { return String(x); } },
        { k: "sr", label: "True Sharpe ratio of every strategy", min: 0, max: 1.5, step: 0.05, value: 0, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New backtests", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var N = Math.pow(2, v.n), r = QB.rng(s.seed + 1200), se = Math.sqrt((1 + 0.5 * v.sr * v.sr) / v.T), is = [], oos = [], best = 0, i;
        for (i = 0; i < N; i++) { is.push(v.sr + se * r.normal()); oos.push(v.sr + se * r.normal()); if (is[i] > is[best]) best = i; }
        var emax = N > 1 ? v.sr + se * ((1 - 0.5772) * QB.inv(1 - 1 / N) + 0.5772 * QB.inv(1 - 1 / (N * Math.E))) : v.sr;
        var z0 = N > 1 ? emax - v.sr : 0, dsr = QB.cdf((is[best] - z0) / se);
        s.out = [is[best], oos[best], emax, dsr];
        var lo = v.sr - 4.2 * se, hi = v.sr + 4.8 * se, H = QB.hist(is, lo, hi, 44), a = g[0].axes({ x: [lo, hi], y: [0, Math.max(4, Math.max.apply(null, H) * 1.15)], title: "Backtested Sharpe ratios of all N", xlabel: "annual Sharpe ratio in the backtest" });
        a.bars(QB.linspace(lo + (hi - lo) / 88, hi - (hi - lo) / 88, 44), H, (hi - lo) / 44, { color: C.spot });
        a.vline(v.sr, { color: C.ink, dash: null }); a.vline(emax, { color: C.p }); a.vline(is[best], { color: C.loss, dash: null, width: 2 });
        a.legend([["the truth", C.ink], ["expected best (formula)", C.p], ["the best found", C.loss]], { pos: "tl" });
        var b = g[1].axes({ x: [lo, hi], y: [lo, hi], title: "The same strategies, out of sample", xlabel: "in the backtest" });
        var m = Math.min(N, 1500); b.line([lo, hi], [lo, hi], { color: C.muted, width: 1, dash: [4, 4] });
        b.dots(is.slice(0, m), oos.slice(0, m), { color: C.spot, r: 1.8, alpha: 0.55 }); b.hline(v.sr, { color: C.ink }); b.dots([is[best]], [oos[best]], { color: C.loss, r: 6 });
      },
      readout: function (v, s) { return [["best backtest", fmt(s.out[0], 2)], ["the same strategy out of sample", fmt(s.out[1], 2)], ["expected best of N", fmt(s.out[2], 2)], ["P(better than chance), deflated", pct(s.out[3], 0)]]; },
      note: "A Sharpe estimate from T years has standard error about √((1 + SR²/2)/T). The deflated probability asks whether the best beats the expected best of N skill-less tries.",
    });
  };

  // ---- Part 27: double descent ---------------------------------------------------------------------------------------------------
  W.descent = function (el) {
    var mp = function (lam, gam) { var b = 1 - gam + lam; return (-b + Math.sqrt(b * b + 4 * gam * lam)) / (2 * gam * lam); };
    var risk = function (lam, gam, r2, s2) { // out-of-sample excess risk of ridge, isotropic features, P/N = gam
      var h = lam * 1e-4, f = mp(lam, gam), fp = (mp(lam + h, gam) - mp(lam - h, gam)) / (2 * h);
      return r2 * lam * lam * (-fp) + s2 * gam * (f + lam * fp);
    };
    QB.widget(el, {
      title: "More parameters than observations",
      sub: "A linear model with P parameters is fitted to N observations. With no penalty the out-of-sample error explodes at P = N and comes back down beyond it. How much of this matters depends on how much signal there is: for returns, very little.",
      panels: 2, height: 300,
      controls: [
        { k: "snr", label: "Predictable share of variance", min: 0.5, max: 90, step: 0.5, value: 20, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "lam", label: "Ridge penalty λ", min: -3, max: 1.5, step: 0.05, value: -0.5, fmt: function (x) { return Math.pow(10, x).toPrecision(2); } },
        { k: "gam", label: "Parameters per observation P/N", min: 0.1, max: 5, step: 0.05, value: 2, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var r2 = v.snr / 100, s2 = 1 - r2, lam = Math.pow(10, v.lam), gs = QB.linspace(0.05, 5, 250).filter(function (x) { return Math.abs(x - 1) > 0.012; });
        var a = g[0].axes({ x: [0, 5], y: [Math.min(0.05, r2 / 4), 50], logy: true, title: "Out-of-sample error against model size", xlabel: "parameters per observation, P/N" });
        a.hline(r2, { color: C.muted }); a.text(4.95, r2, "predict nothing", { color: C.muted, align: "right", dy: -8 }); a.vline(1, { color: C.muted });
        a.line(gs, gs.map(function (x) { return risk(1e-5, x, r2, s2); }), { color: C.loss, width: 2 });
        a.line(gs, gs.map(function (x) { return risk(lam, x, r2, s2); }), { color: C.gain, width: 2.2 });
        a.dots([v.gam], [risk(lam, v.gam, r2, s2)], { color: C.gain, r: 5 });
        a.legend([["no penalty (interpolates when P > N)", C.loss], ["ridge with your λ", C.gain]], { pos: "tr" });
        var ls = QB.linspace(-3, 1.5, 120), rs = ls.map(function (x) { return risk(Math.pow(10, x), v.gam, r2, s2); }), opt = s2 * v.gam / r2;
        var b = g[1].axes({ x: [0.001, 31.6], y: [Math.min.apply(null, rs) * 0.8, Math.min(50, Math.max.apply(null, rs) * 1.1)], logx: true, logy: true, title: "Error against the penalty, at your P/N", xlabel: "ridge penalty λ" });
        b.line(ls.map(function (x) { return Math.pow(10, x); }), rs, { color: C.gain, width: 2.2 }); b.hline(r2, { color: C.muted });
        if (opt > 0.001 && opt < 31.6) { b.vline(opt, { color: C.p }); b.text(opt, Math.min.apply(null, rs) * 0.9, "best λ = σ²γ/r²", { color: C.p, align: opt > 1 ? "right" : "left", dx: opt > 1 ? -5 : 5 }); }
        b.dots([lam], [risk(lam, v.gam, r2, s2)], { color: C.gain, r: 5 });
        s.out = [risk(lam, v.gam, r2, s2), risk(1e-5, v.gam, r2, s2), r2, risk(Math.min(Math.max(opt, 1e-5), 1e3), v.gam, r2, s2)];
      },
      readout: function (v, s) { return [["error with your λ", fmt(s.out[0], 3)], ["with no penalty", fmt(s.out[1], 2)], ["predicting nothing", fmt(s.out[2], 3)], ["at the best λ", fmt(s.out[3], 3)]]; },
      note: "Exact large-sample formulas (Marchenko-Pastur; Hastie, Montanari, Rosset and Tibshirani). Monthly stock returns sit near the left end of the signal slider: well under 1%.",
    });
  };

  // ---- Part 28: tone by dictionary ----------------------------------------------------------------------------------------------
  W.words = function (el) {
    var POS = "strong stronger strength improve improved improving improvement gain gains growth expand expanded expansion solid robust favorable progress resilient recovery rebound confident benefit benefited achieve exceeded success stable stability upgrade positive better best opportunity".split(" ");
    var NEG = "weak weaker weakness decline declined declining loss losses fall fell slowdown slowed contraction recession stress strain deteriorate deteriorated downturn default defaults crisis risk risks adverse concern concerns worse worst unemployment shortfall negative volatile tightening impairment litigation restated".split(" ");
    var UNC = "uncertain uncertainty may might could possibly approximately depend depends unclear unpredictable appears likely assume".split(" ");
    el.innerHTML = '<p class="w-title">Tone by dictionary</p><p class="w-sub">Type or paste a sentence from an earnings call or a central-bank statement. Each word is looked up in three short lists (positive, negative, uncertain), as Tetlock and Loughran-McDonald did with far longer ones. Then try a sentence the lists get wrong.</p>' +
      '<textarea rows="3" aria-label="Text to score" style="width:100%;background:#0a0d13;color:#e6edf3;border:1px solid #263041;border-radius:10px;padding:10px 12px;font:15px/1.5 system-ui,sans-serif"></textarea>' +
      '<p class="marked" style="line-height:2;margin:12px 0 0;font-size:1.05rem"></p><div class="readout"></div>' +
      '<div class="w-buttons"><button type="button" data-t="0">A hawkish statement</button><button type="button" data-t="1">A good quarter</button><button type="button" data-t="2">A sentence that fools it</button></div>' +
      '<p class="w-note">An illustrative list of about a hundred words, not the published dictionaries. Counting words ignores negation, context and who is speaking: that is what the later chapters of Part 28 fix.</p>';
    var ta = el.querySelector("textarea"), out = el.querySelector(".marked"), read = el.querySelector(".readout");
    var samples = ["Inflation remains elevated and risks to the outlook are uncertain; the Committee is strongly committed to further tightening if labor market strength persists.",
      "Revenue growth was strong, margins improved for the fifth quarter, and we are confident that demand will remain robust.",
      "Losses were not as severe as feared, the decline in defaults was better than any concern we had, and nothing about the recovery is weak."];
    function esc(t) { return t.replace(/[&<>]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; }); }
    function render() {
      var words = ta.value.split(/(\s+)/), n = 0, p = 0, m = 0, u = 0;
      out.innerHTML = words.map(function (w) {
        var k = w.toLowerCase().replace(/[^a-z]/g, ""); if (!k) return esc(w); n++;
        var col = POS.indexOf(k) >= 0 ? (p++, C.gain) : NEG.indexOf(k) >= 0 ? (m++, C.loss) : UNC.indexOf(k) >= 0 ? (u++, C.p) : null;
        return col ? '<span style="color:' + col + ';font-weight:600;border-bottom:2px solid ' + col + '">' + esc(w) + "</span>" : '<span style="color:#b7c2d0">' + esc(w) + "</span>";
      }).join("");
      read.innerHTML = "<span>words <b>" + n + "</b></span><span>positive <b>" + p + "</b></span><span>negative <b>" + m + "</b></span><span>uncertain <b>" + u + "</b></span><span>tone (pos − neg)/words <b>" + (n ? fmt((p - m) / n, 3) : "0") + "</b></span>";
    }
    ta.addEventListener("input", render);
    el.querySelectorAll("button").forEach(function (b) { b.addEventListener("click", function () { ta.value = samples[+b.dataset.t]; render(); }); });
    ta.value = samples[0]; render();
  };

  // ---- Part 29: the winner of a search ------------------------------------------------------------------------------------------
  W.winner = function (el) {
    QB.widget(el, {
      title: "The winner of a search",
      sub: "K candidate formulas are scored by their information coefficient on T days of history, and the best one is kept. Its score is its true IC plus luck, and searching harder selects for luck. Shrinking the winner toward zero gives back what it will earn.",
      panels: 2, height: 300,
      controls: [
        { k: "k", label: "Formulas searched", min: 0, max: 14, step: 1, value: 10, fmt: function (x) { return Math.pow(2, x).toLocaleString("en-US"); } },
        { k: "T", label: "Days of history", min: 60, max: 2520, step: 60, value: 500, fmt: function (x) { return String(x); } },
        { k: "sd", label: "Spread of true ICs across formulas", min: 0, max: 0.02, step: 0.001, value: 0.004, fmt: function (x) { return x.toFixed(3); } },
      ],
      buttons: [{ label: "New search", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var K = Math.pow(2, v.k), r = QB.rng(s.seed + 1300), noise = 0.1 / Math.sqrt(v.T), tr = [], is = [], oos = [], best = 0, i;
        for (i = 0; i < K; i++) { tr.push(v.sd * r.normal()); is.push(tr[i] + noise * r.normal()); oos.push(tr[i] + noise * r.normal()); if (is[i] > is[best]) best = i; }
        var shrink = v.sd * v.sd / (v.sd * v.sd + noise * noise), w = 4.5 * Math.sqrt(v.sd * v.sd + noise * noise) + 0.002;
        s.out = [is[best], oos[best], tr[best], shrink * is[best], shrink];
        var m = Math.min(K, 1500), a = g[0].axes({ x: [-w, w], y: [-w, w], title: "In sample against out of sample", xlabel: "IC in the search sample" });
        a.line([-w, w], [-w, w], { color: C.muted, width: 1, dash: [4, 4] }); a.line([-w, w], [-w * shrink, w * shrink], { color: C.p, width: 1.6 });
        a.dots(is.slice(0, m), oos.slice(0, m), { color: C.spot, r: 1.8, alpha: 0.55 }); a.dots([is[best]], [oos[best]], { color: C.loss, r: 6 });
        a.legend([["what to expect: shrink by " + fmt(shrink, 2), C.p], ["the winner", C.loss]], { pos: "tl" });
        var Ks = QB.linspace(0, 14, 15), b = g[1].axes({ x: [1, 16384], y: [0, Math.max(0.02, noise * 4.6 + v.sd * 3)], logx: true, title: "The winner's score against the size of the search", xlabel: "formulas searched" });
        var tot = Math.sqrt(v.sd * v.sd + noise * noise), em = function (k) { var n = Math.pow(2, k); return n > 1 ? tot * ((1 - 0.5772) * QB.inv(1 - 1 / n) + 0.5772 * QB.inv(1 - 1 / (n * Math.E))) : 0; };
        b.line(Ks.map(function (k) { return Math.pow(2, k); }), Ks.map(em), { color: C.loss, width: 2 });
        b.line(Ks.map(function (k) { return Math.pow(2, k); }), Ks.map(function (k) { return shrink * em(k); }), { color: C.gain, width: 2 });
        b.vline(K); b.legend([["its score in the search", C.loss], ["what it earns afterwards", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) { return [["winner in sample", fmt(s.out[0], 4)], ["out of sample", fmt(s.out[1], 4)], ["its true IC", fmt(s.out[2], 4)], ["shrunk estimate", fmt(s.out[3], 4)]]; },
      note: "The daily IC is measured with noise of about 0.1 (a hundred stocks), so T days leave a standard error of 0.1/√T. With no spread in true ICs the whole search is luck.",
    });
  };

  // ---- Part 30: the optimizer on estimated inputs --------------------------------------------------------------------------------
  W.shrink = function (el) {
    QB.widget(el, {
      title: "The optimizer is an error maximizer",
      sub: "The same three assets as in Part 23, correlation 0.3. This time the expected returns are estimated from a sample, 400 times over, and each estimate is handed to the optimizer. Shrinking the estimates toward their common mean trades a little bias for much less noise.",
      panels: 2, height: 300,
      controls: [
        { k: "T", label: "Years of data", min: 2, max: 200, step: 1, value: 10, fmt: function (x) { return String(x); } },
        { k: "sh", label: "Shrink the estimated means toward their average", min: 0, max: 1, step: 0.05, value: 0, fmt: function (x) { return pct(x, 0); } },
      ],
      draw: function (g, v, s) {
        var S = cov(0.3), r = QB.rng(77), wTrue = tangency(MU, S, 0), srTrue = dot(wTrue, MU) / Math.sqrt(quad(wTrue, S)), eq = [1 / 3, 1 / 3, 1 / 3], srEq = dot(eq, MU) / Math.sqrt(quad(eq, S));
        // Cholesky of S for correlated sampling noise in the means
        var L = [[Math.sqrt(S[0][0]), 0, 0], [0, 0, 0], [0, 0, 0]]; L[1][0] = S[1][0] / L[0][0]; L[1][1] = Math.sqrt(S[1][1] - L[1][0] * L[1][0]); L[2][0] = S[2][0] / L[0][0]; L[2][1] = (S[2][1] - L[2][0] * L[1][0]) / L[1][1]; L[2][2] = Math.sqrt(S[2][2] - L[2][0] * L[2][0] - L[2][1] * L[2][1]);
        var srs = [], w1 = [], w3 = [], k, i;
        for (k = 0; k < 400; k++) {
          var z = [r.normal(), r.normal(), r.normal()], mh = MU.map(function (m, i2) { return m + (L[i2][0] * z[0] + L[i2][1] * z[1] + L[i2][2] * z[2]) / Math.sqrt(v.T); });
          var avg = (mh[0] + mh[1] + mh[2]) / 3; mh = mh.map(function (m) { return v.sh * avg + (1 - v.sh) * m; });
          var w = solve(S, mh), tot = w[0] + w[1] + w[2]; if (Math.abs(tot) < 1e-6) tot = 1e-6; w = w.map(function (x) { return x / tot; });
          var sr = dot(w, MU) / Math.sqrt(quad(w, S)); srs.push(sr); w1.push(Math.max(-2, Math.min(3, w[0]))); w3.push(Math.max(-2, Math.min(3, w[2])));
        }
        s.out = [QB.quantile(srs, 0.5), srTrue, srEq, srs.filter(function (x) { return x < srEq; }).length / 400];
        var a = g[0].axes({ x: [-2, 3], y: [-2, 3], title: "Optimal weights from 400 samples", xlabel: "weight in A (the safe asset)", xfmt: function (x) { return (100 * x).toFixed(0) + "%"; }, yfmt: function (y) { return (100 * y).toFixed(0) + "%"; } });
        a.hline(0, { dash: null }); a.vline(0, { dash: null }); a.dots(w1, w3, { color: C.spot, r: 2, alpha: 0.5 });
        a.dots([wTrue[0]], [wTrue[2]], { color: C.gain, r: 6 }); a.text(wTrue[0], wTrue[2], "true optimum", { color: C.gain, dx: 10, dy: -14, bg: true });
        a.dots([1 / 3], [1 / 3], { color: C.p, r: 5 }); a.text(1 / 3, 1 / 3, "1/N", { color: C.p, dx: -10, dy: 14, align: "right", bg: true });
        a.text(-1.93, 2.8, "vertical: weight in C (the risky asset)", { color: C.muted });
        var H = QB.hist(srs, -0.4, 0.6, 40), b = g[1].axes({ x: [-0.4, 0.6], y: [0, Math.max(10, Math.max.apply(null, H) * 1.15)], title: "True Sharpe ratio of each estimated portfolio", xlabel: "Sharpe ratio actually earned" });
        b.bars(QB.linspace(-0.3875, 0.5875, 40), H, 0.025, { color: C.spot }); b.vline(srTrue, { color: C.gain, dash: null }); b.vline(srEq, { color: C.p, dash: null });
        b.legend([["true optimum", C.gain], ["1/N", C.p]], { pos: "tl" });
      },
      readout: function (v, s) { return [["median Sharpe earned", fmt(s.out[0], 2)], ["the true optimum", fmt(s.out[1], 2)], ["1/N", fmt(s.out[2], 2)], ["samples in which 1/N wins", pct(s.out[3], 0)]]; },
      note: "The covariance is taken as known here; estimating it as well only makes things worse (the lab measures that). Full shrinkage hands the optimizer equal means, and it returns the minimum-variance portfolio.",
    });
  };

  // ---- Part 31: from IC to capacity ------------------------------------------------------------------------------------------------
  W.law = function (el) {
    QB.widget(el, {
      title: "Skill, breadth, and what size does to both",
      sub: "The fundamental law says the information ratio is IC × √breadth. It overstates things when the IC itself varies from period to period, and it says nothing about costs, which grow like the square root of the money being moved.",
      panels: 2, height: 300,
      controls: [
        { k: "ic", label: "Average IC", min: 0.005, max: 0.1, step: 0.005, value: 0.03, fmt: function (x) { return x.toFixed(3); } },
        { k: "sd", label: "How much the IC varies", min: 0, max: 0.1, step: 0.005, value: 0.03, fmt: function (x) { return x.toFixed(3); } },
        { k: "to", label: "Turnover of the book", min: 2, max: 100, step: 1, value: 20, fmt: function (x) { return x + "× a year"; } },
      ],
      draw: function (g, v, s) {
        var ns = QB.linspace(Math.log(10), Math.log(5000), 80).map(Math.exp), law = function (n) { return v.ic * Math.sqrt(n) * Math.sqrt(12); }, tv = function (n) { return v.ic / Math.sqrt(v.sd * v.sd + (1 - v.ic * v.ic) / n) * Math.sqrt(12); };
        var a = g[0].axes({ x: [10, 5000], y: [0.1, 30], logx: true, logy: true, title: "Information ratio against breadth (monthly bets)", xlabel: "independent bets per month" });
        a.line(ns, ns.map(law), { color: C.p, width: 2 }); a.line(ns, ns.map(tv), { color: C.loss, width: 2.2 });
        if (v.sd > 0) { a.hline(v.ic / v.sd * Math.sqrt(12), { color: C.muted }); a.text(11, v.ic / v.sd * Math.sqrt(12), "ceiling E[IC]/sd(IC)", { color: C.muted, dy: -8 }); }
        a.legend([["fundamental law", C.p], ["with a varying IC", C.loss]], { pos: "br" });
        var gross = 0.06, aum = QB.linspace(Math.log(1e7), Math.log(3e10), 120).map(Math.exp), net = aum.map(function (A) { return gross - v.to * 0.02 * Math.sqrt(A * v.to / 252 / 2e10); });
        var dollars = aum.map(function (A, i) { return Math.max(0, net[i]) * A / 1e6; }), imax = 0; dollars.forEach(function (d, i) { if (d > dollars[imax]) imax = i; });
        var b = g[1].axes({ x: [1e7, 3e10], y: [0, 6.5], logx: true, title: "Net return against assets (gross alpha 6%)", xlabel: "assets under management, $", xfmt: function (x) { return x >= 1e9 ? (x / 1e9) + "bn" : (x / 1e6) + "m"; }, yfmt: function (y) { return y + "%"; } });
        b.line(aum, net.map(function (x) { return 100 * x; }), { color: C.spot, width: 2 });
        b.line(aum, dollars.map(function (d) { return 6.2 * d / dollars[imax]; }), { color: C.gain, width: 2 });
        b.vline(aum[imax], { color: C.p }); b.legend([["net return, %", C.spot], ["dollars earned (rescaled)", C.gain]], { pos: "bl" });
        s.out = [law(500), tv(500), aum[imax], net[imax], dollars[imax]];
      },
      readout: function (v, s) { return [["IR at 500 bets: the law", fmt(s.out[0], 2)], ["with a varying IC", fmt(s.out[1], 2)], ["capacity", "$" + fmt(s.out[2] / 1e9, 2) + "bn"], ["net return there", pct(s.out[3], 1)], ["dollars a year", "$" + fmt(s.out[4], 0) + "m"]]; },
      note: "Costs: Y·σ·√(Q/ADV) with 2% daily volatility and $20bn of daily volume across the book. Dollars peak where costs have taken two thirds of the gross alpha.",
    });
  };

  // ---- Part 32: trend following's smile ----------------------------------------------------------------------------------------------
  W.trend = function (el) {
    QB.widget(el, {
      title: "Why trend following looks like a straddle",
      sub: "The rule: each day hold a position equal to the market's return so far this month. Its monthly profit is exactly ½(month's return² − sum of daily returns²): large moves either way pay, quiet months cost a little. Autocorrelation in returns is what tips the average above zero.",
      panels: 2, height: 300,
      controls: [
        { k: "rho", label: "Autocorrelation of daily returns", min: -0.1, max: 0.2, step: 0.01, value: 0.03, fmt: function (x) { return x.toFixed(2); } },
        { k: "n", label: "Days per block", min: 5, max: 126, step: 1, value: 21, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New history", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 1400), blocks = 3000, n = v.n, S = [], P = [], x = 0, e = Math.sqrt(1 - v.rho * v.rho), k, i;
        for (k = 0; k < blocks; k++) { var cum = 0, pnl = 0; for (i = 0; i < n; i++) { x = v.rho * x + e * r.normal(); pnl += cum * x; cum += x; } S.push(cum / Math.sqrt(n)); P.push(pnl / n); }
        var m = QB.mean(P), sdv = QB.sd(P), sk = QB.mean(P.map(function (p) { return Math.pow((p - m) / sdv, 3); }));
        s.out = [m / sdv * Math.sqrt(252 / n), sk, P.filter(function (p) { return p < 0; }).length / blocks, 2 * Math.SQRT2 * (n - 2) / Math.sqrt(n * (n - 1))];
        var a = g[0].axes({ x: [-4, 4], y: [-1.5, 7], title: "Trend profit against the market's move in the block", xlabel: "market return, in block standard deviations" });
        a.dots(S.slice(0, 1500), P.slice(0, 1500), { color: C.spot, r: 1.8, alpha: 0.5 }); a.hline(0, { dash: null });
        var xs = QB.linspace(-4, 4, 81); a.line(xs, xs.map(function (z) { return 0.5 * (z * z - 1); }), { color: C.p, width: 2 });
        a.legend([["½(z² − 1): a straddle's payoff", C.p]], { pos: "tl" });
        var H = QB.hist(P, -1.5, 5, 52), b = g[1].axes({ x: [-1.5, 5], y: [1, blocks], logy: true, title: "Distribution of the block's profit (log scale)", xlabel: "profit" });
        b.bars(QB.linspace(-1.4375, 4.9375, 52), H.map(function (c) { return Math.max(c, 1); }), 0.125, { color: function (j) { return -1.5 + (j + 0.5) * 0.125 < 0 ? C.loss : C.gain; }, base: 1 }); b.vline(m, { color: C.p });
      },
      readout: function (v, s) { return [["Sharpe ratio", fmt(s.out[0], 2)], ["skewness", fmt(s.out[1], 2) + " (random walk: " + fmt(s.out[3], 2) + ")"], ["blocks that lose", pct(s.out[2], 0)]]; },
      note: "Simulated AR(1) returns with unit variance. With zero autocorrelation the rule has zero mean and positive skew: it is long realized variance at the block's horizon.",
    });
  };

  // ---- Part 33: trading a mean-reverting spread ----------------------------------------------------------------------------------------
  W.ou = function (el) {
    QB.widget(el, {
      title: "How far should the spread stretch before you trade?",
      sub: "An Ornstein-Uhlenbeck spread. The rule: when it reaches the band, bet on its return to the mean and close there; each round trip costs c. A narrow band trades often for little; a wide one waits for moves that rarely come.",
      panels: 2, weights: [1.4, 1], height: 300,
      controls: [
        { k: "hl", label: "Half-life of the spread", min: 2, max: 60, step: 1, value: 12, fmt: function (x) { return x + " days"; } },
        { k: "m", label: "Entry band", min: 0.2, max: 3, step: 0.05, value: 1.2, fmt: function (x) { return "±" + x.toFixed(2) + " sd"; } },
        { k: "c", label: "Round-trip cost", min: 0, max: 1, step: 0.02, value: 0.2, fmt: function (x) { return x.toFixed(2) + " sd"; } },
      ],
      buttons: [{ label: "New path", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = 20000, phi = Math.pow(0.5, 1 / v.hl), r = QB.rng(s.seed + 1500), x = [0], i;
        for (i = 1; i < n; i++) x.push(phi * x[i - 1] + Math.sqrt(1 - phi * phi) * r.normal());
        var run = function (m) { var pos = 0, pnl = 0, trades = 0, marks = []; for (i = 1; i < n; i++) { if (pos === 0 && Math.abs(x[i]) >= m) { pos = x[i] > 0 ? -1 : 1; pnl -= pos * x[i]; trades++; if (i < 750) marks.push([i, x[i], 1]); } else if (pos !== 0 && pos * x[i] >= 0) { pnl += pos * x[i] - v.c; if (i < 750) marks.push([i, x[i], 0]); pos = 0; } } if (pos !== 0) pnl += pos * x[n - 1]; return { rate: pnl / (n / 252), trades: trades, marks: marks }; };
        var me = run(v.m), ms = QB.linspace(0.2, 3, 29), rates = ms.map(function (m) { return run(m).rate; }), ib = 0; rates.forEach(function (q, j) { if (q > rates[ib]) ib = j; });
        s.out = [me.rate, me.trades / (n / 252), ms[ib], rates[ib]];
        var a = g[0].axes({ x: [0, 750], y: [-3.6, 3.6], title: "Three years of the spread, with your trades", xlabel: "day" });
        a.area([0, 750], [v.m, v.m], -v.m, { color: C.p, alpha: 0.07 }); a.hline(v.m, { color: C.p }); a.hline(-v.m, { color: C.p }); a.hline(0, { dash: null });
        a.line(QB.linspace(0, 749, 750), x.slice(0, 750), { color: C.spot, width: 1.1 });
        a.dots(me.marks.filter(function (k) { return k[2]; }).map(function (k) { return k[0]; }), me.marks.filter(function (k) { return k[2]; }).map(function (k) { return k[1]; }), { color: C.loss, r: 3.5 });
        a.dots(me.marks.filter(function (k) { return !k[2]; }).map(function (k) { return k[0]; }), me.marks.filter(function (k) { return !k[2]; }).map(function (k) { return k[1]; }), { color: C.gain, r: 3.5 });
        var b = g[1].axes({ x: [0, 3], y: [Math.min(-1, Math.min.apply(null, rates)), Math.max(2, Math.max.apply(null, rates) * 1.15)], title: "Profit a year against the band", xlabel: "entry band, sd" });
        b.hline(0, { dash: null }); b.line(ms, rates, { color: C.p, width: 2 }); b.vline(ms[ib], { color: C.gain }); b.dots([v.m], [me.rate], { color: C.ink, r: 5 });
      },
      readout: function (v, s) { return [["profit a year", fmt(s.out[0], 2) + " sd"], ["round trips a year", fmt(s.out[1], 1)], ["best band on this path", "±" + fmt(s.out[2], 2) + " sd"], ["and its profit", fmt(s.out[3], 2) + " sd"]]; },
      note: "Eighty simulated years, daily. As the cost shrinks the best band shrinks only like its cube root: halve the cost and the band falls by a fifth.",
    });
  };

  // ---- Part 34: the drawdown stop --------------------------------------------------------------------------------------------------------
  W.pods = function (el) {
    QB.widget(el, {
      title: "How long does a seat last?",
      sub: "A pod is closed when its P&L falls a fixed distance below its own peak. The expected time until that happens has an exact formula, and it grows exponentially with skill: the stop removes the unskilled quickly and the skilled eventually.",
      panels: 2, height: 300,
      controls: [
        { k: "S", label: "The manager's true Sharpe ratio", min: -0.5, max: 2.5, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "d", label: "The stop, in annual volatilities below the peak", min: 0.25, max: 2, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New paths", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var tau = function (S, d) { return Math.abs(S) < 1e-6 ? d * d : (Math.exp(2 * S * d) - 1 - 2 * S * d) / (2 * S * S); };
        var r = QB.rng(s.seed + 1600), yrs = 8, n = yrs * 252, alive3 = 0, k, i, a = g[0].axes({ x: [0, yrs], y: [-2.5, 9], title: "Thirty pods with this Sharpe ratio", xlabel: "years" });
        for (k = 0; k < 30; k++) { var x = 0, pk = 0, xs = [0], ys = [0], stop = -1; for (i = 1; i <= n; i++) { x += v.S / 252 + r.normal() / Math.sqrt(252); pk = Math.max(pk, x); if (i % 5 === 0) { xs.push(i / 252); ys.push(x); } if (pk - x >= v.d) { stop = i; xs.push(i / 252); ys.push(x); break; } }
          if (stop < 0 || stop > 3 * 252) alive3++; a.line(xs, ys, { color: stop < 0 ? C.gain : C.loss, width: 1, alpha: 0.6 }); if (stop >= 0) a.dots([stop / 252], [x], { color: C.loss, r: 2.5 }); }
        a.hline(0, { dash: null });
        var Ss = QB.linspace(-0.5, 2.5, 100), b = g[1].axes({ x: [-0.5, 2.5], y: [0.05, 200], logy: true, title: "Expected years until the stop", xlabel: "true Sharpe ratio" });
        b.line(Ss, Ss.map(function (q) { return tau(q, v.d); }), { color: C.p, width: 2.2 }); b.dots([v.S], [tau(v.S, v.d)], { color: C.ink, r: 5 });
        s.out = [tau(v.S, v.d), tau(0, v.d), alive3 / 30, Math.abs(v.S) < 1e-6 ? v.d : (Math.exp(2 * v.S * v.d) - 1) / (2 * v.S)];
      },
      readout: function (v, s) { return [["expected years to the stop", fmt(s.out[0], 1)], ["for a manager with no skill", fmt(s.out[1], 1)], ["alive after three years", pct(s.out[2], 0) + " of these 30"], ["expected peak when stopped", fmt(s.out[3], 2) + " vols"]]; },
      note: "E[τ] = (e^(2Sδ) − 1 − 2Sδ)/(2S²) years for continuous monitoring (Taylor 1975; Lehoczky 1977). Watched once a day, the stop behaves like a slightly deeper one.",
    });
  };
})();
