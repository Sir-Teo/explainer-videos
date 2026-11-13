// Interactives for Stage III, Master's (Parts 37-42).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 37: the weights two-way fixed effects puts on each treated town-year ------------------------------
  W.forbiddentwfe = function (el) {
    var T = 20, START = [4, 9, 14], NAMES = ["adopt 2004", "adopt 2009", "adopt 2014"], COL = [C.spot, C.idea, C.gain];
    QB.widget(el, {
      title: "Staggered adoption: where two-way fixed effects puts its weight",
      sub: "Three cohorts of towns adopt a programme in 2004, 2009 and 2014. Left: each cohort's true effect by year. Right: the weight the two-way fixed-effects regression gives each treated cohort-year. Weights below zero fall on the early cohort's late years, so let its effect grow and watch the regression leave the truth, then cross zero.",
      panels: 2, height: 300,
      controls: [
        { k: "g1", label: "Effect growth per year, 2004 cohort", min: 0, max: 1, step: 0.05, value: 0.7, fmt: function (x) { return x.toFixed(2); } },
        { k: "g2", label: "Effect growth per year, later cohorts", min: 0, max: 1, step: 0.05, value: 0.2, fmt: function (x) { return x.toFixed(2); } },
        { k: "jump", label: "Effect in the adoption year, all cohorts", min: 0, max: 3, step: 0.1, value: 0.5, fmt: function (x) { return x.toFixed(1); } },
        { k: "never", label: "Never-treated towns (of 200)", min: 0, max: 100, step: 5, value: 20, fmt: function (x) { return String(x); } },
      ],
      draw: function (g, v, s) {
        var share = [76, 56, 48].map(function (c) { return c / 180 * (200 - v.never) / 200; }).concat([v.never / 200]);
        var D = [], tau = [], i, t, years = [];
        for (t = 0; t < T; t++) years.push(2000 + t);
        for (i = 0; i < 4; i++) {
          D.push([]); tau.push([]);
          for (t = 0; t < T; t++) {
            var on = i < 3 && t >= START[i];
            D[i].push(on ? 1 : 0);
            tau[i].push(on ? v.jump + (i === 0 ? v.g1 : v.g2) * (t - START[i]) : 0);
          }
        }
        // two-way demeaning of D with cohort shares as weights
        var rowm = D.map(function (r) { return QB.mean(r); }), colm = [], all = 0;
        for (t = 0; t < T; t++) { var c = 0; for (i = 0; i < 4; i++) c += share[i] * D[i][t]; colm.push(c); all += c / T; }
        var den = 0, num = 0, att = 0, nt = 0, neg = 0, wts = [[], [], []], wmax = 1e-9, tmax = 1;
        for (i = 0; i < 4; i++) for (t = 0; t < T; t++) { var d = D[i][t] - rowm[i] - colm[t] + all; den += share[i] * d * d; }
        den = Math.max(den, 1e-12);
        for (i = 0; i < 3; i++) for (t = 0; t < T; t++) {
          var w = D[i][t] ? share[i] * (D[i][t] - rowm[i] - colm[t] + all) / den : null;
          wts[i].push(w);
          if (D[i][t]) { num += w * tau[i][t]; att += share[i] * tau[i][t]; nt += share[i]; if (w < 0) neg += w; wmax = Math.max(wmax, Math.abs(w)); tmax = Math.max(tmax, tau[i][t]); }
        }
        att = nt > 0 ? att / nt : 0;
        s.out = [att, num, neg];
        var a = g[0].axes({ x: [2000, 2019], y: [Math.min(0, num * 1.25 - 0.3), tmax * 1.12], title: "True effect by cohort and year", xlabel: "year", nx: 4 });
        for (i = 0; i < 3; i++) a.line(years, tau[i].map(function (y, k) { return D[i][k] ? y : null; }), { color: COL[i], width: 2.2 });
        a.hline(att, { color: C.ink }); a.hline(num, { color: C.loss, dash: [2, 3] });
        a.legend([[NAMES[0], COL[0]], [NAMES[1], COL[1]], [NAMES[2], COL[2]], ["true ATT", C.ink], ["TWFE", C.loss]], { pos: "tl" });
        var b = g[1].axes({ x: [2000, 2019], y: [-wmax * 1.15, wmax * 1.15], title: "TWFE's weight on each treated cohort-year", xlabel: "year", nx: 4 });
        b.hline(0, { color: C.muted });
        for (i = 0; i < 3; i++) {
          var xs = [], ys = [];
          for (t = 0; t < T; t++) if (wts[i][t] !== null) { xs.push(years[t]); ys.push(wts[i][t]); }
          b.line(xs, ys, { color: COL[i], width: 1.2, alpha: 0.6 });
          b.dots(xs, ys, { color: function (k) { return ys[k] < 0 ? C.loss : COL[i]; }, r: 3 });
        }
        b.text(2000.5, -wmax * 0.95, "red dots: negative weights", { color: C.loss });
      },
      readout: function (v, s) {
        return [["true ATT", fmt(s.out[0], 2)], ["TWFE coefficient", fmt(s.out[1], 2)], ["sum of the negative weights", fmt(s.out[2], 2)]];
      },
      note: "Computed exactly from cohort means, with no noise: 76, 56 and 48 towns per cohort, rescaled when the never-treated count changes. The weights sum to one. With no growth every cohort-year has the same effect, so the weights do not matter and TWFE equals the ATT.",
    });
  };

  // ---- Part 38: the Kalman filter for a local level, and its gain ---------------------------------------------
  W.kalmangain = function (el) {
    QB.widget(el, {
      title: "Tracking a hidden level: the Kalman gain",
      sub: "A hidden level drifts slowly and drops once, at year 40; each year it is measured with noise of sd 1. The filter is told a ratio q of level variance to measurement variance. Small q trusts the past and is slow to see the drop; large q chases the noise. Hide some years after the drop and the band widens until data return.",
      panels: 2, height: 300, weights: [1.6, 1],
      controls: [
        { k: "lq", label: "Signal-to-noise ratio q the filter assumes", min: -3, max: 1, step: 0.05, value: -1, fmt: function (x) { return Math.pow(10, x).toPrecision(2); } },
        { k: "drop", label: "Size of the drop at year 40", min: 0, max: 5, step: 0.25, value: 3, fmt: function (x) { return x.toFixed(2); } },
        { k: "hide", label: "Years hidden after the drop", min: 0, max: 20, step: 1, value: 0, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New series", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 380), n = 100, q = Math.pow(10, v.lq), t, lev = [], y = [], xs = [], walk = 0;
        for (t = 0; t < n; t++) { walk += 0.15 * r.normal(); lev.push(10 + walk - (t >= 40 ? v.drop : 0)); y.push(lev[t] + r.normal()); xs.push(t); }
        var m = y[0], P = 10, mf = [], lo = [], hi = [], sse = 0, K = 0;
        for (t = 0; t < n; t++) {
          P += q;
          if (!(t >= 40 && t < 40 + v.hide)) { K = P / (P + 1); m += K * (y[t] - m); P *= 1 - K; }
          mf.push(m); lo.push(m - 1.645 * Math.sqrt(P)); hi.push(m + 1.645 * Math.sqrt(P)); sse += (m - lev[t]) * (m - lev[t]);
        }
        var Ks = 0.5 * (Math.sqrt(q * q + 4 * q) - q);
        s.out = [Ks, Math.log(0.5) / Math.log(1 - Ks), Math.sqrt(sse / n)];
        var a = g[0].axes({ x: [0, n - 1], y: [2, 14], title: "Measurements, the hidden level and the filter", xlabel: "year" });
        a.area(xs, hi, lo, { color: C.idea, alpha: 0.2 });
        var seen = [], sy = [];
        for (t = 0; t < n; t++) if (!(t >= 40 && t < 40 + v.hide)) { seen.push(t); sy.push(y[t]); }
        a.dots(seen, sy, { color: C.cash, r: 2, alpha: 0.8 });
        a.line(xs, lev, { color: C.spot, width: 1.6 });
        a.line(xs, mf, { color: C.idea, width: 2.2 });
        a.vline(40, { color: C.muted });
        a.legend([["filtered level, 90% band", C.idea], ["hidden level", C.spot], ["measurements", C.cash]], { pos: "bl" });
        var lags = [], wt = [];
        for (t = 0; t < 30; t++) { lags.push(t); wt.push(Ks * Math.pow(1 - Ks, t)); }
        var b = g[1].axes({ x: [-0.7, 29.7], y: [0, Math.max(0.1, Ks * 1.15)], title: "Weight on each past measurement", xlabel: "years ago" });
        b.bars(lags, wt, 0.8, { color: C.idea });
        b.text(29, Math.max(0.1, Ks * 1.15) * 0.9, "K (1 − K)^j", { align: "right", color: C.muted });
      },
      readout: function (v, s) {
        return [["steady-state gain K", fmt(s.out[0], 3)], ["half-life of a measurement's weight", fmt(s.out[1], 1) + " years"], ["RMSE of the filtered level", fmt(s.out[2], 2)]];
      },
      note: "Simulated data: the level is a random walk with yearly sd 0.15, so the q that matches it is 0.0225 until the drop, which no q expects. In steady state the filter is exponential smoothing with K = (√(q² + 4q) − q)/2.",
    });
  };

  // ---- Part 39: kriging on a line ------------------------------------------------------------------------------
  function matern(d, rho, k) { // unit variance; k = 0, 1, 2 for nu = 1/2, 3/2, 5/2
    var nu = k + 0.5, x = Math.sqrt(2 * nu) * Math.abs(d) / rho;
    return (k === 0 ? 1 : k === 1 ? 1 + x : 1 + x + x * x / 3) * Math.exp(-x);
  }
  function chol(A) { // lower Cholesky factor in place of a copy; tiny pivots are floored
    var n = A.length, L = [], i, j, k, sum;
    for (i = 0; i < n; i++) {
      L.push(new Array(n).fill(0));
      for (j = 0; j <= i; j++) {
        sum = A[i][j]; for (k = 0; k < j; k++) sum -= L[i][k] * L[j][k];
        L[i][j] = i === j ? Math.sqrt(Math.max(sum, 1e-10)) : sum / L[j][j];
      }
    }
    return L;
  }
  function cholSolve(L, b) {
    var n = L.length, y = new Array(n), i, k, sum;
    for (i = 0; i < n; i++) { sum = b[i]; for (k = 0; k < i; k++) sum -= L[i][k] * y[k]; y[i] = sum / L[i][i]; }
    for (i = n - 1; i >= 0; i--) { sum = y[i]; for (k = i + 1; k < n; k++) sum -= L[k][i] * y[k]; y[i] = sum / L[i][i]; }
    return y;
  }
  W.krigeline = function (el) {
    var NS = 10, NG = 101, NUS = ["1/2", "3/2", "5/2"];
    QB.widget(el, {
      title: "Kriging on a line: range, smoothness and nugget",
      sub: "Ten noisy measurements (dots) of a hidden curve, a Matérn field with range 1.5 and smoothness 3/2. The gold line is the simple-kriging prediction under the covariance you choose, with its 90% band. Shorten the range and the band balloons between stations; lengthen it and the band becomes too narrow to hold the curve. The right panel shows the weights behind the prediction at one site.",
      panels: 2, height: 300, weights: [1.6, 1],
      controls: [
        { k: "rho", label: "Range ρ assumed", min: 0.2, max: 5, step: 0.1, value: 1.5, fmt: function (x) { return x.toFixed(1); } },
        { k: "nu", label: "Smoothness ν assumed", min: 0, max: 2, step: 1, value: 1, fmt: function (x) { return NUS[x]; } },
        { k: "nug", label: "Nugget (measurement variance) assumed", min: 0, max: 0.5, step: 0.01, value: 0.04, fmt: function (x) { return x.toFixed(2); } },
        { k: "x0", label: "Prediction site", min: 0, max: 10, step: 0.1, value: 4.6, fmt: function (x) { return x.toFixed(1); } },
      ],
      buttons: [{ label: "New field", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var i, j, k;
        if (!s.cache || s.cache.seed !== s.seed) { // the hidden curve and the data: once per seed
          var r = QB.rng(s.seed + 390), pts = [], site = [];
          for (i = 0; i < NG; i++) pts.push(10 * i / (NG - 1));
          for (i = 0; i < NS; i++) { site.push(0.5 + i + 0.6 * (r() - 0.5)); pts.push(site[i]); }
          var A = pts.map(function (a, p) { return pts.map(function (b, q) { return matern(a - b, 1.5, 1) + (p === q ? 1e-6 : 0); }); });
          var L0 = chol(A), e = pts.map(function () { return r.normal(); }), f = [];
          for (i = 0; i < pts.length; i++) { var acc = 0; for (j = 0; j <= i; j++) acc += L0[i][j] * e[j]; f.push(acc); }
          s.cache = { seed: s.seed, grid: pts.slice(0, NG), truth: f.slice(0, NG), site: site, z: site.map(function (x, q) { return f[NG + q] + 0.2 * r.normal(); }) };
        }
        var c = s.cache, K = c.site.map(function (a, p) { return c.site.map(function (b, q) { return matern(a - b, v.rho, v.nu) + (p === q ? v.nug + 1e-8 : 0); }); });
        var L = chol(K), alpha = cholSolve(L, c.z), pred = [], lo = [], hi = [], inside = 0;
        var at = function (x) {
          var k0 = c.site.map(function (a) { return matern(a - x, v.rho, v.nu); }), w = cholSolve(L, k0), m = 0, q = 0;
          for (k = 0; k < NS; k++) { m += k0[k] * alpha[k]; q += k0[k] * w[k]; }
          return { m: m, sd: Math.sqrt(Math.max(1 - q, 0)), w: w };
        };
        for (i = 0; i < NG; i++) {
          var o = at(c.grid[i]); pred.push(o.m); lo.push(o.m - 1.645 * o.sd); hi.push(o.m + 1.645 * o.sd);
          if (Math.abs(c.truth[i] - o.m) <= 1.645 * o.sd) inside++;
        }
        var t = at(v.x0), sw = 0; for (k = 0; k < NS; k++) sw += t.w[k];
        s.out = [t.m, t.sd, sw, inside / NG];
        var a = g[0].axes({ x: [0, 10], y: [-3.2, 3.2], title: "Hidden curve, data and the kriged prediction", xlabel: "position" });
        a.area(c.grid, hi, lo, { color: C.idea, alpha: 0.2 });
        a.line(c.grid, c.truth, { color: C.spot, width: 1.5 });
        a.line(c.grid, pred, { color: C.idea, width: 2.2 });
        a.dots(c.site, c.z, { color: C.ink, r: 3.2 });
        a.vline(v.x0, { color: C.loss }); a.dots([v.x0], [t.m], { color: C.loss, r: 4 });
        a.legend([["kriged mean, 90% band", C.idea], ["hidden curve", C.spot], ["prediction site", C.loss]], { pos: "bl" });
        var wm = 0.2; for (k = 0; k < NS; k++) wm = Math.max(wm, Math.abs(t.w[k]));
        var b = g[1].axes({ x: [0, 10], y: [-wm * 1.15, wm * 1.15], title: "Kriging weight of each station", xlabel: "station position" });
        b.hline(0, { color: C.muted });
        b.bars(c.site, t.w, 0.45, { color: function (q) { return t.w[q] < 0 ? C.loss : C.idea; } });
        b.vline(v.x0, { color: C.loss });
      },
      readout: function (v, s) {
        return [["prediction at the site", fmt(s.out[0], 2)], ["its kriging sd", fmt(s.out[1], 2)], ["sum of the weights", fmt(s.out[2], 2)], ["curve inside the 90% band", QB.pct(s.out[3], 0)]];
      },
      note: "Simulated data: one draw of a unit-variance Matérn field (ρ = 1.5, ν = 3/2) with measurement sd 0.2. Simple kriging with mean 0 and variance 1 assumed, so the weights need not sum to one: what is left over goes to the mean. Red bars are negative weights, on stations screened by a nearer one. The share of the curve inside the band is for this one field, not an average.",
    });
  };

  // ---- Part 40: Kaplan-Meier, the two shortcuts, and informative censoring ------------------------------------
  W.censorstairs = function (el) {
    QB.widget(el, {
      title: "Censored lifetimes: the staircase and the shortcuts",
      sub: "Lifetimes are exponential with mean 10; each patient is also censored at a random time before the study ends. Gold is Kaplan-Meier, with a tick at each censoring; red drops the censored patients; orange counts them as deaths. Shorten the study and the shortcuts sink while the staircase holds. Then withdraw patients shortly before they die: the censoring is no longer independent, and the staircase rises above the truth.",
      panels: 2, height: 300, weights: [1.6, 1],
      controls: [
        { k: "n", label: "Patients", min: 20, max: 300, step: 10, value: 100, fmt: function (x) { return String(x); } },
        { k: "end", label: "Study length (censoring uniform up to it)", min: 6, max: 60, step: 1, value: 25, fmt: function (x) { return String(x); } },
        { k: "inf", label: "Share withdrawn shortly before death", min: 0, max: 0.6, step: 0.05, value: 0, fmt: function (x) { return QB.pct(x, 0); } },
      ],
      buttons: [{ label: "New patients", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 400), n = v.n, P = [], i, T0 = 8, XM = 24;
        for (i = 0; i < n; i++) {
          var u = 0; while (u === 0) u = r();
          var t = -10 * Math.log(u), c = v.end * r(), pull = r(), frac = 0.5 + 0.4 * r();
          if (pull < v.inf) c = Math.min(c, frac * t);
          P.push({ t: Math.min(t, c), e: t <= c });
        }
        P.sort(function (a, b) { return a.t - b.t || (b.e ? 1 : 0) - (a.e ? 1 : 0); });
        var S = 1, kx = [0], ky = [1], rx = [0], ry = [n], tick = [], ticky = [], ncens = 0, km8 = 1, seen8 = 0, dead = 0, alive8 = 0;
        for (i = 0; i < n; i++) {
          var atRisk = n - i;
          if (P[i].e) { kx.push(P[i].t); ky.push(S); S *= 1 - 1 / atRisk; kx.push(P[i].t); ky.push(S); dead++; if (P[i].t > T0) seen8++; }
          else { ncens++; tick.push(P[i].t); ticky.push(S); }
          if (P[i].t <= T0) km8 = S;
          if (P[i].t > T0) alive8++;
          rx.push(P[i].t); ry.push(atRisk); rx.push(P[i].t); ry.push(atRisk - 1);
        }
        kx.push(XM); ky.push(S);
        var grid = QB.linspace(0, XM, 97), truth = grid.map(function (x) { return Math.exp(-x / 10); });
        var drop = grid.map(function (x) { var k = 0; for (var j = 0; j < n; j++) if (P[j].e && P[j].t > x) k++; return dead > 0 ? k / dead : 0; });
        var asd = grid.map(function (x) { var k = 0; for (var j = 0; j < n; j++) if (P[j].t > x) k++; return k / n; });
        s.out = [Math.exp(-T0 / 10), km8, dead > 0 ? seen8 / dead : 0, alive8 / n, ncens / n];
        var a = g[0].axes({ x: [0, XM], y: [0, 1.02], title: "Estimated survival S(t)", xlabel: "time" });
        a.line(grid, drop, { color: C.loss, width: 1.3 });
        a.line(grid, asd, { color: C.implied, width: 1.3 });
        a.line(grid, truth, { color: C.ink, width: 1.2, dash: [4, 4] });
        a.line(kx, ky, { color: C.idea, width: 2.2 });
        a.clip(function (ctx) {
          ctx.strokeStyle = C.idea; ctx.lineWidth = 1;
          for (var j = 0; j < tick.length; j++) { var X = a.px(tick[j]), Y = a.py(ticky[j]); ctx.beginPath(); ctx.moveTo(X, Y - 4); ctx.lineTo(X, Y + 4); ctx.stroke(); }
        });
        a.vline(T0, { color: C.muted });
        a.legend([["Kaplan-Meier", C.idea], ["truth", C.ink], ["censored dropped", C.loss], ["censored as deaths", C.implied]], { pos: "tr" });
        var b = g[1].axes({ x: [0, XM], y: [0, n * 1.05], title: "Patients still at risk", xlabel: "time" });
        b.line(rx, ry, { color: C.spot, width: 1.8 });
        b.vline(T0, { color: C.muted });
      },
      readout: function (v, s) {
        return [["true S(8)", fmt(s.out[0], 3)], ["Kaplan-Meier", fmt(s.out[1], 3)], ["censored dropped", fmt(s.out[2], 3)], ["censored as deaths", fmt(s.out[3], 3)], ["share censored", QB.pct(s.out[4], 0)]];
      },
      note: "Simulated data. A withdrawn patient leaves at a point between 50% and 90% of the way to their own death, which the analyst cannot see. Kaplan-Meier needs censoring that is independent of the lifetime; no estimator can repair the withdrawn case from these data alone.",
    });
  };

  // ---- Part 41: which missingness a covariate can repair -------------------------------------------------------
  W.maskmean = function (el) {
    QB.widget(el, {
      title: "Missing at random, and not: what a covariate can repair",
      sub: "Each point is a person: x is always seen, y (true mean 0) is hidden for some. Red crosses are the hidden values. Blue is the mean of the complete cases; gold imputes each hidden y from the regression of y on x. Let missingness depend on x and only blue goes wrong. Let it depend on y itself and both do, and nothing in the observed data says so.",
      panels: 2, height: 300, weights: [1.5, 1],
      controls: [
        { k: "rate", label: "Share of y missing", min: 0.1, max: 0.7, step: 0.05, value: 0.4, fmt: function (x) { return QB.pct(x, 0); } },
        { k: "bx", label: "Missingness depends on x (MAR)", min: 0, max: 3, step: 0.1, value: 1.5, fmt: function (x) { return x.toFixed(1); } },
        { k: "by", label: "Missingness depends on y itself (MNAR)", min: 0, max: 3, step: 0.1, value: 0, fmt: function (x) { return x.toFixed(1); } },
      ],
      buttons: [{ label: "New sample", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 410), n = 300, REPS = 60, rep, i, a0 = 0;
        var sample = function () {
          var X = [], Y = [];
          for (var k = 0; k < n; k++) { var x = r.normal(); X.push(x); Y.push(0.6 * x + 0.8 * r.normal()); }
          return [X, Y];
        };
        var first = sample(), lo = -12, hi = 12; // the intercept that gives the chosen share, by bisection on the first sample
        for (i = 0; i < 40; i++) {
          a0 = (lo + hi) / 2; var m = 0;
          for (var k = 0; k < n; k++) m += 1 / (1 + Math.exp(-(a0 + v.bx * first[0][k] + v.by * first[1][k])));
          if (m / n > v.rate) hi = a0; else lo = a0;
        }
        var analyse = function (X, Y) {
          var M = [], no = 0, sx = 0, sy = 0, k;
          for (k = 0; k < n; k++) { var miss = r() < 1 / (1 + Math.exp(-(a0 + v.bx * X[k] + v.by * Y[k]))); M.push(miss); if (!miss) { no++; sx += X[k]; sy += Y[k]; } }
          if (no < 3) return { M: M, cc: 0, adj: 0, miss: 1 };
          var mx = sx / no, my = sy / no, sxx = 0, sxy = 0, xall = QB.mean(X);
          for (k = 0; k < n; k++) if (!M[k]) { sxx += (X[k] - mx) * (X[k] - mx); sxy += (X[k] - mx) * (Y[k] - my); }
          var b = sxx > 1e-9 ? sxy / sxx : 0, adj = 0;
          for (k = 0; k < n; k++) adj += M[k] ? my + b * (X[k] - mx) : Y[k];
          return { M: M, cc: my, adj: adj / n, miss: 1 - no / n, b: b, a: my - b * mx, xall: xall };
        };
        var one = analyse(first[0], first[1]), ccs = [one.cc], adjs = [one.adj];
        for (rep = 1; rep < REPS; rep++) { var d = sample(), o = analyse(d[0], d[1]); ccs.push(o.cc); adjs.push(o.adj); }
        s.out = [one.cc, one.adj, QB.mean(ccs), QB.mean(adjs), one.miss];
        var ax = g[0].axes({ x: [-3, 3], y: [-3.2, 3.2], title: "One sample of 300", xlabel: "x (always seen)" });
        var ox = [], oy = [], hx = [], hy = [];
        for (i = 0; i < n; i++) { if (one.M[i]) { hx.push(first[0][i]); hy.push(first[1][i]); } else { ox.push(first[0][i]); oy.push(first[1][i]); } }
        ax.dots(ox, oy, { color: C.spot, r: 2.2, alpha: 0.8 });
        ax.clip(function (ctx) {
          ctx.strokeStyle = C.loss; ctx.globalAlpha = 0.65; ctx.lineWidth = 1.1;
          for (var k = 0; k < hx.length; k++) { var X = ax.px(hx[k]), Y = ax.py(hy[k]); ctx.beginPath(); ctx.moveTo(X - 2.5, Y - 2.5); ctx.lineTo(X + 2.5, Y + 2.5); ctx.moveTo(X - 2.5, Y + 2.5); ctx.lineTo(X + 2.5, Y - 2.5); ctx.stroke(); }
        });
        ax.hline(0, { color: C.ink }); ax.hline(one.cc, { color: C.spot, dash: null, width: 1.6 }); ax.hline(one.adj, { color: C.idea, dash: null, width: 1.6 });
        ax.legend([["true mean of y", C.ink], ["complete-case mean", C.spot], ["imputed from x", C.idea], ["hidden values", C.loss]], { pos: "tl" });
        var b2 = g[1].axes({ x: [-1.2, 1.2], y: [0, 3], title: "The two estimates in 60 samples", xlabel: "estimate (truth 0)", yticks: [] });
        b2.vline(0, { color: C.ink });
        var jit = QB.rng(7), j1 = [], j2 = [];
        for (i = 0; i < REPS; i++) { j1.push(2.1 + 0.5 * (jit() - 0.5)); j2.push(0.9 + 0.5 * (jit() - 0.5)); }
        b2.dots(ccs, j1, { color: C.spot, r: 2.6, alpha: 0.8 }); b2.dots(adjs, j2, { color: C.idea, r: 2.6, alpha: 0.8 });
        b2.text(-1.15, 2.7, "complete cases", { color: C.spot }); b2.text(-1.15, 0.3, "imputed from x", { color: C.idea });
      },
      readout: function (v, s) {
        return [["complete-case mean", fmt(s.out[0], 2)], ["imputed from x", fmt(s.out[1], 2)], ["average over 60 samples", fmt(s.out[2], 2) + " and " + fmt(s.out[3], 2)], ["missing", QB.pct(s.out[4], 0)]];
      },
      note: "Simulated data: x and y are standard normal with correlation 0.6, and y is hidden with probability logistic in x and y with the two slopes above. The gold estimate is valid when, given x, missingness does not depend on y (MAR). With both slopes at zero the data are missing completely at random and both estimates are unbiased.",
    });
  };

  // ---- Part 42: sizing a cluster-randomized trial --------------------------------------------------------------
  W.clustertowns = function (el) {
    var SIG = 16.5;
    QB.widget(el, {
      title: "How many towns? The design effect at work",
      sub: "A trial randomizes whole towns and measures m adults in each (blood pressure, sd 16.5 mm Hg). Left: power against the number of towns per arm, as it really is (gold) and as it looks if the adults are treated as independent (red). Right: the towns per arm needed for 80% power as m grows. Raise the intraclass correlation from zero and watch the two curves on the left part, and a floor appear on the right that no number of adults per town gets under.",
      panels: 2, height: 300,
      controls: [
        { k: "rho", label: "Intraclass correlation ρ", min: 0, max: 0.2, step: 0.005, value: 0.055, fmt: function (x) { return x.toFixed(3); } },
        { k: "m", label: "Adults measured per town, m", min: 5, max: 500, step: 5, value: 50, fmt: function (x) { return String(x); } },
        { k: "k", label: "Towns per arm", min: 4, max: 60, step: 1, value: 21, fmt: function (x) { return String(x); } },
        { k: "delta", label: "Effect to detect (mm Hg)", min: 1, max: 8, step: 0.25, value: 4, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var de = 1 + (v.m - 1) * v.rho, nInd = 2 * Math.pow(1.96 + 0.8416, 2) * SIG * SIG / (v.delta * v.delta);
        var power = function (k, d) { var se = SIG * Math.sqrt(2 * d / (k * v.m)), z = v.delta / se; return QB.cdf(z - 1.96) + QB.cdf(-z - 1.96); };
        var need = function (m) { return nInd * (1 + (m - 1) * v.rho) / m; };
        var ks = QB.linspace(2, 60, 117), real = ks.map(function (k) { return power(k, de); }), claimed = ks.map(function (k) { return power(k, 1); });
        s.out = [de, v.k * v.m / de, power(v.k, de), power(v.k, 1), 2 * QB.cdf(-1.96 / Math.sqrt(de)), need(v.m), nInd * v.rho];
        var a = g[0].axes({ x: [0, 60], y: [0, 1.02], title: "Power at 5%, by towns per arm", xlabel: "towns per arm", yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        a.hline(0.8, { color: C.muted });
        a.line(ks, claimed, { color: C.loss, width: 1.6, dash: [5, 4] });
        a.line(ks, real, { color: C.idea, width: 2.2 });
        a.vline(v.k, { color: C.muted }); a.dots([v.k], [s.out[2]], { color: C.idea, r: 4.5 }); a.dots([v.k], [s.out[3]], { color: C.loss, r: 3.5 });
        a.legend([["analysed by town (real)", C.idea], ["adults as independent (claimed)", C.loss]], { pos: "br" });
        var ms = [], ys = [], i;
        for (i = 0; i <= 80; i++) { ms.push(5 * Math.pow(100, i / 80)); ys.push(need(ms[i])); }
        var top = Math.min(4000, Math.max(20, 1.15 * need(5)));
        var b = g[1].axes({ x: [5, 500], y: [0, top], logx: true, xticks: [5, 10, 20, 50, 100, 200, 500], title: "Towns per arm for 80% power", xlabel: "adults per town, m (log scale)" });
        b.hline(nInd * v.rho, { color: C.spot });
        b.line(ms, ys, { color: C.idea, width: 2.2 });
        b.dots([v.m], [need(v.m)], { color: C.idea, r: 4.5 });
        b.legend([["towns needed", C.idea], ["floor: the m → ∞ limit", C.spot]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["design effect", fmt(s.out[0], 2)], ["adults per arm are worth", fmt(s.out[1], 0)], ["real power", QB.pct(s.out[2], 0)], ["claimed if independent", QB.pct(s.out[3], 0)],
          ["type I error if analysed by adult", QB.pct(s.out[4], 0)], ["towns per arm for 80%", fmt(s.out[5], 1)], ["floor", fmt(s.out[6], 1)]];
      },
      note: "Formulas, not a simulation: normal approximations with known variances, design effect 1 + (m − 1)ρ, and towns per arm 2(1.96 + 0.84)²σ²/δ² × design effect / m. With few towns the t test has somewhat less power than shown, which is why the film adds a town per arm.",
    });
  };
})();
