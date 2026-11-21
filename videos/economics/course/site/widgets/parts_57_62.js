// Interactives for Act XI, Economics at Work (Parts 57-62).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var W = QB.W;

  // ---- Part 57: reading the economy in real time ----------------------------------------------------------------
  W.nowcaster = function (el) {
    // Agora's nowcast module (explainer.economics.agora.nowcast): the Island's monthly factor f_t = 0.6 f_{t-1} +
    // eta_t, four indicators x_it = lam_i f_t + e_it (payrolls, production, retail, a survey), and quarterly GDP
    // growth y = 2 + 3 * (average f over the quarter) + 0.8 eps.  The model's nowcast is the Kalman filter on the
    // releases so far; the reader sets their own, release by release, and is scored against the truth.
    var PHI = 0.6, LAM = [1.0, 0.8, 0.7, 0.5], SD = [0.6, 0.7, 0.8, 1.0], MU = 2.0, BETA = 3.0, SDQ = 0.8;
    var NAMES = ["payrolls", "production", "retail", "survey"];
    var COLS = ["#7EC8F5", "#F2C14E", "#7FD1B9", "#E8A0B4"];
    var RELEASES = ["before the quarter", "month 1: the survey", "month 1: hard data", "month 2", "month 3"];
    function simulate(seed) {
      var u = QB.rng(1000 + seed), T = 36, f = [], X = [], k, i;
      var x = 0;
      for (k = 0; k < 24; k++) { x = PHI * x + u.normal(); }
      for (k = 0; k < T; k++) {
        x = PHI * x + u.normal();
        f.push(x);
        var row = [];
        for (i = 0; i < 4; i++) { row.push(LAM[i] * x + SD[i] * u.normal()); }
        X.push(row);
      }
      var t0 = T - 3;
      var y = MU + BETA * (f[t0] + f[t0 + 1] + f[t0 + 2]) / 3 + SDQ * u.normal();
      return { f: f, X: X, y: y, t0: t0 };
    }
    function avail(k, t, i, t0) {
      if (t < t0) { return true; }
      if (t === t0) { return (k >= 1 && i === 3) || k >= 2; }
      if (t === t0 + 1) { return k >= 3; }
      return k >= 4;
    }
    function kalman(sim, k) {
      // state (f_t, f_{t-1}, f_{t-2}); observations skipped where not yet released
      var a = [0, 0, 0], P = [[1 / (1 - PHI * PHI), 0, 0], [0, 1 / (1 - PHI * PHI), 0], [0, 0, 1 / (1 - PHI * PHI)]];
      var t, i, r, c;
      for (t = 0; t <= sim.t0 + 2; t++) {
        a = [PHI * a[0], a[0], a[1]];
        var P2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
        // F P F' + Q with F = [[phi,0,0],[1,0,0],[0,1,0]]
        P2[0][0] = PHI * PHI * P[0][0] + 1; P2[0][1] = PHI * P[0][0]; P2[0][2] = PHI * P[0][1];
        P2[1][0] = P2[0][1]; P2[1][1] = P[0][0]; P2[1][2] = P[0][1];
        P2[2][0] = P2[0][2]; P2[2][1] = P2[1][2]; P2[2][2] = P[1][1];
        P = P2;
        for (i = 0; i < 4; i++) {          // sequential updates: the observation errors are independent
          if (!avail(k, t, i, sim.t0)) { continue; }
          var v = sim.X[t][i] - LAM[i] * a[0];
          var S = LAM[i] * LAM[i] * P[0][0] + SD[i] * SD[i];
          var K = [P[0][0] * LAM[i] / S, P[1][0] * LAM[i] / S, P[2][0] * LAM[i] / S];
          for (r = 0; r < 3; r++) { a[r] += K[r] * v; }
          var Pn = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
          for (r = 0; r < 3; r++) { for (c = 0; c < 3; c++) { Pn[r][c] = P[r][c] - K[r] * LAM[i] * P[0][c]; } }
          P = Pn;
        }
      }
      var m = (a[0] + a[1] + a[2]) / 3, vv = 0;
      for (r = 0; r < 3; r++) { for (c = 0; c < 3; c++) { vv += P[r][c] / 9; } }
      return { mean: MU + BETA * m, sd: Math.sqrt(BETA * BETA * vv + SDQ * SDQ) };
    }
    QB.widget(el, {
      title: "Nowcaster",
      sub: "An Island quarter, release by release. Set your nowcast of the quarter's GDP growth after each release, " +
           "then step to the next. At month 3 the truth is revealed, with the model's Kalman-filter nowcast beside " +
           "yours.",
      panels: 2, height: 250,
      controls: [
        { k: "seed", label: "Quarter", min: 1, max: 30, step: 1, value: 7, fmt: function (x) { return "#" + x; } },
        { k: "k", label: "Release", min: 0, max: 4, step: 1, value: 0, fmt: function (x) { return RELEASES[x]; } },
        { k: "you", label: "Your nowcast (% a year)", min: -8, max: 8, step: 0.1, value: 2.0,
          fmt: function (x) { return (x > 0 ? "+" : "") + x.toFixed(1) + "%"; } },
        { k: "show", label: "Show the model's nowcast", min: 0, max: 1, step: 1, value: 0,
          fmt: function (x) { return x ? "yes" : "no"; } },
      ],
      draw: function (g, v, st) {
        var sim = simulate(v.seed), k = v.k;
        var A = g[0].axes({ x: [-6.5, 2.5], y: [-4.5, 4.5], title: "monthly indicators (0 = the quarter's first month)",
                            xlabel: "month" });
        A.hline(0, {});
        A.vline(-0.5, {});
        for (var i = 0; i < 4; i++) {
          var xs = [], ys = [];
          for (var t = sim.t0 - 6; t <= sim.t0 + 2; t++) {
            if (!avail(k, t, i, sim.t0)) { continue; }
            xs.push(t - sim.t0); ys.push(Math.max(-4.4, Math.min(4.4, sim.X[t][i])));
          }
          A.line(xs, ys, { color: COLS[i], width: 2 });
        }
        A.legend(NAMES.map(function (n, j) { return [n, COLS[j]]; }));
        var nc = kalman(sim, k);
        var B = g[1].axes({ x: [-10, 10], y: [0, 1], noY: true, title: "this quarter's GDP growth, % a year",
                            xlabel: "growth" });
        B.vline(0, {});
        B.dots([v.you], [0.6], { color: "#F2C14E", r: 6 });
        B.text(v.you, 0.6, "you", { color: "#F2C14E", align: "center", dy: -14 });
        if (v.show) {
          B.line([nc.mean - nc.sd, nc.mean + nc.sd], [0.4, 0.4], { color: "#E8A0B4", width: 5 });
          B.dots([nc.mean], [0.4], { color: "#E8A0B4", r: 5 });
          B.text(nc.mean, 0.4, "model", { color: "#E8A0B4", align: "center", dy: 16 });
        }
        if (k === 4) {
          B.dots([sim.y], [0.2], { color: "#7BD88F", r: 6 });
          B.text(sim.y, 0.2, "truth", { color: "#7BD88F", align: "center", dy: 16 });
        }
        st.nc = nc; st.y = sim.y; st.k = k; st.you = v.you;
      },
      readout: function (v, st) {
        var rows = [["release", RELEASES[st.k]],
                    ["your nowcast", st.you.toFixed(1) + "%"]];
        if (v.show) { rows.push(["the model's nowcast", st.nc.mean.toFixed(1) + "% (s.d. " + st.nc.sd.toFixed(1) + ")"]); }
        if (st.k === 4) {
          rows.push(["the truth", st.y.toFixed(1) + "%"]);
          rows.push(["your error / the model's", Math.abs(st.you - st.y).toFixed(1) + " / " +
                     Math.abs(st.nc.mean - st.y).toFixed(1)]);
        }
        return rows;
      },
      note: "Part 57, chapters 3 and 4. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 58: scoring the bill ----------------------------------------------------------------------------------
  W.appraiser = function (el) {
    // Agora's appraisal module (explainer.economics.agora.appraisal): the Island's bridge against Bo's ferry.  Crossings
    // = 1.8 - 0.08 x generalized cost (millions a year); the ferry costs a fare of 4 and 40 minutes, the bridge is free
    // and takes 8; travellers gain Dupuit's surplus (the rule of a half on new crossings); Bo loses his profit; 0.24 and
    // 0.05 deaths per million crossings; 300 to build over three years, 1.2 a year to keep, a hundred years of use,
    // traffic growing 1% a year for forty.  The reader sets the assumptions, decides, then draws an outturn from the
    // Island's reference class (costs 28% over on average, s.d. 39 points; traffic 10% under, s.d. 25).
    var P = { a: 1.8, b: 0.08, fare: 4, ferryMin: 40, bridgeMin: 8, wage: 24, unit: 1.5, fixed: 0.6, rf: 0.24,
              rb: 0.05, build: [100, 100, 100], maint: 1.2, life: 100, growth: 0.01, gyears: 40, noise: 2.8 };
    var NAMES = ["time", "fares", "new trips", "safety", "Bo's profit", "noise", "build", "upkeep"];
    var COLS = ["#7EC8F5", "#9FB8F2", "#7FD1B9", "#F2C14E", "#C9A0FF", "#E8A0B4", "#F25F5C", "#F2A65A"];
    function streams(v, costRatio, trafficRatio) {
      var vot = v.vot * P.wage, g0 = P.fare + vot * P.ferryMin / 60, g1 = vot * P.bridgeMin / 60;
      var q0 = Math.max(P.a - P.b * g0, 0), q1 = Math.max(P.a - P.b * g1, 0);
      var y = { time: q0 * vot * (P.ferryMin - P.bridgeMin) / 60, fares: q0 * P.fare,
                newt: 0.5 * (q1 - q0) * (g0 - g1), lives: (P.rf * q0 - P.rb * q1) * v.vsl,
                bo: (P.fare - P.unit) * q0 };
      return { y: y, nb: P.build.length, T: P.build.length + P.life, cost: costRatio, traffic: trafficRatio };
    }
    function pv(v, rate, costRatio, trafficRatio) {
      var s = streams(v, costRatio, trafficRatio), out = [0, 0, 0, 0, 0, 0, 0, 0], t, df, G;
      for (t = 0; t < s.T; t++) {
        df = Math.pow(1 + rate, -t);
        if (t < s.nb) { out[6] -= P.build[t] * costRatio * df; continue; }
        G = Math.pow(1 + P.growth, Math.min(t - s.nb, P.gyears)) * trafficRatio;
        out[0] += G * s.y.time * df; out[1] += G * s.y.fares * df; out[2] += G * s.y.newt * df;
        out[3] += G * s.y.lives * df; out[4] -= (G * s.y.bo - P.fixed) * df; out[7] -= P.maint * df;
        if (t === s.nb) { out[5] -= P.noise * df; }
      }
      return out;
    }
    function sum(a) { var s = 0; for (var i = 0; i < a.length; i++) { s += a[i]; } return s; }
    function npv(v, rate, c, tr) { return sum(pv(v, rate, c, tr)); }
    function irr(v, c, tr) {
      var lo = 0.0001, hi = 0.5, k;
      if (npv(v, lo, c, tr) <= 0) { return NaN; }
      for (k = 0; k < 60; k++) { var m = (lo + hi) / 2; if (npv(v, m, c, tr) > 0) { lo = m; } else { hi = m; } }
      return (lo + hi) / 2;
    }
    function lognormal(u, mean, sd) {
      var s2 = Math.log(1 + (sd / mean) * (sd / mean)), mu = Math.log(mean) - s2 / 2;
      return Math.exp(mu + Math.sqrt(s2) * u.normal());
    }
    QB.widget(el, {
      title: "Appraiser",
      sub: "Appraise the Island's bridge. Set the discount rate and the assumptions, decide whether to build, then " +
           "draw how the costs and the traffic actually turned out, from the record of projects like it.",
      panels: 2, height: 260,
      controls: [
        { k: "rate", label: "Discount rate", min: 0.01, max: 0.08, step: 0.0025, value: 0.035,
          fmt: function (x) { return (100 * x).toFixed(2) + "%"; } },
        { k: "vot", label: "Value of time (share of the wage)", min: 0.35, max: 0.6, step: 0.05, value: 0.5,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
        { k: "vsl", label: "Value of a statistical life (millions)", min: 5, max: 15, step: 0.5, value: 9,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "cost", label: "Cost uplift you allow", min: 0, max: 0.8, step: 0.05, value: 0,
          fmt: function (x) { return "+" + (100 * x).toFixed(0) + "%"; } },
        { k: "build", label: "Your decision", min: 0, max: 1, step: 1, value: 1,
          fmt: function (x) { return x ? "build" : "do not build"; } },
        { k: "draw", label: "Outturn draw (0 = not yet)", min: 0, max: 20, step: 1, value: 0,
          fmt: function (x) { return x ? "#" + x : "not yet"; } },
      ],
      draw: function (g, v, st) {
        var c = 1 + v.cost, rates = [], vals = [], r;
        for (r = 0.005; r <= 0.0801; r += 0.0025) { rates.push(r); vals.push(npv(v, r, c, 1)); }
        var A = g[0].axes({ x: [0, 0.08], y: [-300, 500], title: "the bridge's NPV against the discount rate",
                            xlabel: "discount rate", xfmt: function (x) { return (100 * x).toFixed(0) + "%"; } });
        A.hline(0, {});
        A.line(rates, vals, { color: "#E8A0B4", width: 2.4 });
        var here = npv(v, v.rate, c, 1);
        A.dots([v.rate], [Math.max(-300, Math.min(500, here))], { color: "#F2C14E", r: 6 });
        var comps = pv(v, v.rate, c, 1);
        var B = g[1].axes({ x: [-0.5, 7.5], y: [-450, 250], title: "present values, millions", noX: false,
                            xticks: [0, 1, 2, 3, 4, 5, 6, 7], xfmt: function (i) { return NAMES[i] || ""; } });
        B.hline(0, {});
        B.bars([0, 1, 2, 3, 4, 5, 6, 7], comps.map(function (x) { return Math.max(-450, Math.min(250, x)); }), 0.7,
               { color: function (i) { return COLS[i]; } });
        st.npv = here; st.bcr = sum(comps.filter(function (x) { return x > 0; })) /
          -sum(comps.filter(function (x) { return x < 0; }));
        st.irr = irr(v, c, 1);
        if (v.draw > 0) {
          var u = QB.rng(5800 + v.draw), oc = lognormal(u, 1.28, 0.39), ot = lognormal(u, 0.90, 0.25);
          st.outturn = { cost: oc, traffic: ot, npv: npv(v, v.rate, oc, ot) };
          A.dots([v.rate], [Math.max(-300, Math.min(500, st.outturn.npv))], { color: "#F25F5C", r: 6 });
          A.text(v.rate, Math.max(-300, Math.min(500, st.outturn.npv)), "outturn", { color: "#F25F5C", dx: 8 });
        } else { st.outturn = null; }
      },
      readout: function (v, st) {
        var rows = [["NPV at " + (100 * v.rate).toFixed(2) + "%", st.npv.toFixed(0) + " million"],
                    ["benefit-cost ratio", st.bcr.toFixed(2)],
                    ["internal rate of return", isNaN(st.irr) ? "none" : (100 * st.irr).toFixed(1) + "%"],
                    ["your decision", v.build ? "build" : "do not build"]];
        if (st.outturn) {
          var good = (st.outturn.npv > 0) === (v.build === 1);
          rows.push(["outturn: cost, traffic", (100 * st.outturn.cost).toFixed(0) + "%, " +
                     (100 * st.outturn.traffic).toFixed(0) + "% of forecast"]);
          rows.push(["outturn NPV", st.outturn.npv.toFixed(0) + " million"]);
          rows.push(["the decision, in hindsight", good ? "right" : "wrong"]);
        }
        return rows;
      },
      note: "Part 58, chapters 2, 6 and 10. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 59: the expert witness ---------------------------------------------------------------------------------
  W.expert = function (el) {
    // Agora's merger module (explainer.economics.agora.merger.functional_forms): two symmetric firms at price 1 with
    // margin m (own elasticity 1/m) and diversion D merge; the merged price from the joint first-order condition under
    // linear, logit (outside good), linear-in-log-price and constant-elasticity demand, with the merged firm's
    // marginal cost cut by any saving.  Each case is an Island merger whose true diversion, margin, saving and demand
    // curve are drawn from a seed; the reader sees noisy estimates and the parties' (inflated) claim of savings,
    // chooses a curve and how much of the claim to credit, decides, and then sees the retrospective.
    var FORMS = ["linear", "logit", "log-linear", "const. elasticity"];
    var COLS = ["#7FD1B9", "#7EC8F5", "#F2C14E", "#F25F5C"];
    function rise(form, m, D, saving) {
      var e = 1 / m, c = (1 - m) * (1 - saving), b = e, d = D * e, q, dq;
      if (form === 0) {
        var a = 1 + b - d;
        return 100 * ((a + (b - d) * c) / (2 * (b - d)) - 1);
      }
      if (form === 1) {
        var s = D / (1 + D), al = e / (1 - s), dl = Math.log(s / (1 - 2 * s)) + al;
        q = function (p) { var x = Math.exp(dl - al * p); return x / (1 + 2 * x); };
        dq = function (p) { var y = q(p); return -al * y * (1 - 2 * y); };
      } else if (form === 2) {
        q = function (p) { return 1 - (b - d) * Math.log(p); };
        dq = function (p) { return -(b - d) / p; };
      } else {
        if (e * (1 - D) <= 1.02) { return Infinity; }
        q = function (p) { return Math.pow(p, -e + d); };
        dq = function (p) { return (-e + d) * Math.pow(p, -e + d - 1); };
      }
      var f = function (p) { return q(p) + (p - c) * dq(p); }, lo = c + 1e-6, hi = 20, k;
      if (f(hi) > 0) { return Infinity; }
      for (k = 0; k < 80; k++) { var mid = (lo + hi) / 2; if (f(mid) > 0) { lo = mid; } else { hi = mid; } }
      return 100 * ((lo + hi) / 2 - 1);
    }
    function makeCase(n) {
      var u = QB.rng(5900 + n), D = 0.05 + 0.4 * u(), m = 0.15 + 0.23 * u(), sav = 0.14 * u();
      var claim = sav * (1 + 1.5 * u()), Dh = D * Math.exp(0.15 * u.normal()), mh = m * Math.exp(0.1 * u.normal());
      var r = u(), form = r < 0.15 ? 0 : (r < 0.55 ? 1 : (r < 0.9 ? 2 : 3));
      var truth = rise(form, m, D, sav), noise = 1.2 * u.normal();
      return { D: D, m: m, saving: sav, claim: claim, Dh: Math.min(Dh, 0.6), mh: Math.min(mh, 0.42), form: form,
               truth: truth, measured: truth + noise };
    }
    QB.widget(el, {
      title: "Expert",
      sub: "You are the agency's economist. Each case is an Island merger of two shops: you see estimates of the " +
           "diversion ratio and the margin, and the companies' claim of savings. Screen it, simulate it, decide, " +
           "then open the retrospective.",
      panels: 2, height: 250,
      controls: [
        { k: "case", label: "Case", min: 1, max: 12, step: 1, value: 1, fmt: function (x) { return "#" + x; } },
        { k: "form", label: "Your demand curve", min: 0, max: 3, step: 1, value: 1,
          fmt: function (x) { return FORMS[x]; } },
        { k: "credit", label: "Credit for the claimed savings", min: 0, max: 1, step: 0.25, value: 0.5,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
        { k: "challenge", label: "Your decision", min: 0, max: 1, step: 1, value: 0,
          fmt: function (x) { return x ? "challenge" : "clear"; } },
        { k: "retro", label: "Retrospective", min: 0, max: 1, step: 1, value: 0,
          fmt: function (x) { return x ? "open" : "sealed"; } },
      ],
      draw: function (g, v, st) {
        var C = makeCase(v.case), X = 0.05;
        st.C = C;
        st.crit = X / (X + C.mh);
        st.guppi = 100 * C.Dh * C.mh;
        st.net = st.guppi - 100 * v.credit * C.claim * (1 - C.mh);
        var A = g[0].axes({ x: [-0.5, 2.5], y: [0, 0.7], title: "the screen: diversion against X/(X + M)",
                            xticks: [0, 1, 2], xfmt: function (i) { return ["diversion", "critical", "GUPPI"][i] || ""; },
                            yfmt: function (y) { return (100 * y).toFixed(0) + "%"; } });
        A.bars([0, 1, 2], [C.Dh, st.crit, Math.max(0, st.guppi / 100)], 0.6,
               { color: function (i) { return ["#E8A0B4", "#FFFFFF", "#F2A65A"][i]; } });
        var preds = [0, 1, 2, 3].map(function (f) { return rise(f, C.mh, C.Dh, v.credit * C.claim); });
        st.preds = preds;
        st.pred = preds[v.form];
        var B = g[1].axes({ x: [-0.5, 3.5], y: [-10, 40], title: "simulated price rise, %",
                            xticks: [0, 1, 2, 3], xfmt: function (i) { return FORMS[i] || ""; } });
        B.hline(0, {});
        B.bars([0, 1, 2, 3], preds.map(function (x) { return Math.max(-10, Math.min(40, x)); }), 0.6,
               { color: function (i) { return i === v.form ? COLS[i] : "#555B66"; } });
        if (v.retro) {
          B.hline(Math.max(-10, Math.min(40, C.measured)), { color: "#F25F5C", dash: [5, 4] });
          B.text(3.4, Math.max(-10, Math.min(38, C.measured)), "measured afterwards", { color: "#F25F5C", dx: -120 });
        }
      },
      readout: function (v, st) {
        var C = st.C, fmt = function (x) { return isFinite(x) ? (x > 0 ? "+" : "") + x.toFixed(1) + "%" : "unbounded"; };
        var rows = [["diversion (estimated)", (100 * C.Dh).toFixed(0) + "%"],
                    ["margin (estimated)", (100 * C.mh).toFixed(0) + "%"],
                    ["the companies' claimed saving", (100 * C.claim).toFixed(1) + "% of marginal cost"],
                    ["one market? (diversion > critical)", C.Dh > st.crit ? "yes" : "no"],
                    ["GUPPI, and net of credited savings", st.guppi.toFixed(1) + "%, " + st.net.toFixed(1) + "%"],
                    ["your simulation (" + FORMS[v.form] + ")", fmt(st.pred)],
                    ["your decision", v.challenge ? "challenge" : "clear"]];
        if (v.retro) {
          var harm = C.truth > 0, right = (v.challenge === 1) === harm;
          rows.push(["the retrospective measured", fmt(C.measured)]);
          rows.push(["the truth (" + FORMS[C.form] + ", saving " + (100 * C.saving).toFixed(1) + "%)", fmt(C.truth)]);
          rows.push(["your decision, in hindsight", right ? "right" : "wrong"]);
        }
        return rows;
      },
      note: "Part 59, chapters 2, 5, 6, 7 and 12. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 60: the price ------------------------------------------------------------------------------------------
  W.fares = function (el) {
    // Agora's revenue module (explainer.economics.agora.revenue.flight and dp_prices): a hundred seats over sixty
    // days; each day buyers arrive as a Poisson stream, 5 a day with exponential values of mean $90 for the first 39
    // days and 4 a day with mean $260 in the last 21; at fare p the day's demand is Poisson with mean lambda e^(-p/mu).
    // The reader sets a fare that moves in a straight line from the first week to the last, and may cap the seats
    // sold before the business travellers arrive; the optimal policy comes from the same dynamic programme as the
    // film's, on fares from $40 to $500 in steps of $10.
    var SEATS = 100, DAYS = 60, SWITCH = 21;
    var LAM = [], MU = [];
    for (var d = 0; d < DAYS; d++) { var late = d >= DAYS - SWITCH; LAM.push(late ? 4 : 5); MU.push(late ? 260 : 90); }
    var GRID = []; for (var g = 40; g <= 500; g += 10) { GRID.push(g); }
    function pmfRow(mean, x) {
      // P(sales = k), k = 0..x, demand Poisson(mean), x seats left
      var out = new Array(x + 1), p = Math.exp(-mean), cum = 0;
      for (var k = 0; k < x; k++) { out[k] = p; cum += p; p = p * mean / (k + 1); }
      out[x] = Math.max(0, 1 - cum);
      return out;
    }
    var DP = null;
    function solve() {
      if (DP) { return DP; }
      var V = new Array(SEATS + 1).fill(0), pol = [];
      for (var t = DAYS - 1; t >= 0; t--) {
        var nV = new Array(SEATS + 1).fill(0), row = new Array(SEATS + 1).fill(0);
        for (var x = 1; x <= SEATS; x++) {
          var best = -1, bp = GRID[0];
          for (var i = 0; i < GRID.length; i++) {
            var p = GRID[i], m = LAM[t] * Math.exp(-p / MU[t]), pk = pmfRow(m, x), v = 0;
            for (var k = 0; k <= x; k++) { v += pk[k] * (p * k + V[x - k]); }
            if (v > best) { best = v; bp = p; }
          }
          nV[x] = best; row[x] = bp;
        }
        V = nV; pol[t] = row;
      }
      DP = { V0: V[SEATS], pol: pol };
      return DP;
    }
    function poisson(u, mean) {
      var L = Math.exp(-mean), k = 0, p = 1;
      do { k++; p *= u(); } while (p > L);
      return k - 1;
    }
    function fareOf(v, t) { var w = Math.floor(t / 7); return v.first + (v.last - v.first) * Math.min(w, 8) / 8; }
    function run(v, seed, useOpt) {
      var u = QB.rng(seed), x = SEATS, rev = 0, path = [], fares = [];
      var D = useOpt ? solve() : null;
      for (var t = 0; t < DAYS; t++) {
        var p = useOpt ? D.pol[t][Math.max(x, 1)] : fareOf(v, t);
        var cap = (!useOpt && t < DAYS - SWITCH) ? Math.max(0, x - v.protect) : x;
        var dmd = poisson(u, LAM[t] * Math.exp(-p / MU[t]));
        var s = Math.min(dmd, cap, x);
        x -= s; rev += p * s; path.push(SEATS - x); fares.push(p);
      }
      return { rev: rev, sold: SEATS - x, path: path, fares: fares };
    }
    function expected(v, useOpt) {
      var tot = 0, n = 200;
      for (var r = 0; r < n; r++) { tot += run(v, 6000 + r, useOpt).rev; }
      return tot / n;
    }
    QB.widget(el, {
      title: "Fares",
      sub: "Price the Island's flight: a hundred seats, sixty days. Set the first week's fare and the last week's " +
           "(the fare moves in a straight line between them), and how many seats to hold back for business " +
           "travellers, who arrive in the last three weeks. Then compare with the optimal policy.",
      panels: 2, height: 250,
      controls: [
        { k: "first", label: "First week's fare", min: 40, max: 400, step: 10, value: 150,
          fmt: function (x) { return "$" + x; } },
        { k: "last", label: "Last week's fare", min: 40, max: 500, step: 10, value: 150,
          fmt: function (x) { return "$" + x; } },
        { k: "protect", label: "Seats held back until the last three weeks", min: 0, max: 60, step: 5, value: 0,
          fmt: function (x) { return x + " seats"; } },
        { k: "draw", label: "Which simulated flight", min: 1, max: 20, step: 1, value: 1,
          fmt: function (x) { return "#" + x; } },
      ],
      draw: function (g, v, st) {
        var mine = run(v, 7000 + v.draw, false), opt = run(v, 7000 + v.draw, true);
        st.mine = mine; st.opt = opt;
        st.expMine = expected(v, false); st.expOpt = solve().V0;
        var days = []; for (var d = 0; d < DAYS; d++) { days.push(d + 1); }
        var A = g[0].axes({ x: [0, 60], y: [0, 500], title: "the fare by day", xlabel: "day of the sale" });
        A.vline(DAYS - SWITCH, { color: "#F2C14E", dash: [4, 4] });
        A.line(days, mine.fares, { color: "#7FD1B9", width: 2.4 });
        A.line(days, opt.fares, { color: "#F2A65A", width: 2.0 });
        A.legend([["yours", "#7FD1B9"], ["optimal", "#F2A65A"]]);
        var B = g[1].axes({ x: [0, 60], y: [0, 100], title: "seats sold on this flight", xlabel: "day of the sale" });
        B.line(days, mine.path, { color: "#7FD1B9", width: 2.4 });
        B.line(days, opt.path, { color: "#F2A65A", width: 2.0 });
      },
      readout: function (v, st) {
        return [["this flight: your revenue, seats sold", "$" + st.mine.rev.toFixed(0) + ", " + st.mine.sold],
                ["this flight: the optimal policy", "$" + st.opt.rev.toFixed(0) + ", " + st.opt.sold],
                ["your rule, on average over 200 flights", "$" + st.expMine.toFixed(0)],
                ["the optimal policy, expected", "$" + st.expOpt.toFixed(0)],
                ["your share of the optimum", (100 * st.expMine / st.expOpt).toFixed(1) + "%"]];
      },
      note: "Part 60, chapters 4 to 6. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 61: economics at the platforms --------------------------------------------------------------------
  W.platform = function (el) {
    // Agora's platform module (explainer.economics.agora.platform.commission_market): riders (1,000 an hour who
    // might ride) ride with logit probability in a_r - b_r fare - w_r wait; the wait, in minutes, is
    // w_min + w_k u / (1 - u) with drivers' utilization u = trips / (drivers x cap); drivers (2,000 who might
    // drive) drive with logit probability in (hourly earnings - w0) / s_d, earnings (1 - c) x fare x trips per
    // driver.  For each commission c the equilibrium is found by nested bisection, as in the film's chapter two.
    var P = { a_r: 3.5, b_r: 0.08, w_r: 0.8, riders: 1000, drivers: 2000, s_d: 2.0, cap: 2.0, w_min: 2.0, w_k: 3.0 };
    function lg(x) { x = Math.max(-50, Math.min(50, x)); return 1 / (1 + Math.exp(-x)); }
    function wait(t, D) { var u = t / (D * P.cap); return P.w_min + P.w_k * u / (1 - u); }
    function trips(D, fare) {
      var lo = 0, hi = D * P.cap * (1 - 1e-9);
      for (var i = 0; i < 60; i++) {
        var t = (lo + hi) / 2, f = t - P.riders * lg(P.a_r - P.b_r * fare - P.w_r * wait(t, D));
        if (f > 0) { hi = t; } else { lo = t; }
      }
      return (lo + hi) / 2;
    }
    function market(c, fare, w0) {
      var lo = 1e-3, hi = P.drivers;
      for (var i = 0; i < 60; i++) {
        var D = (lo + hi) / 2, e = (1 - c) * fare * trips(D, fare) / D;
        var g = D - P.drivers * lg((e - w0) / P.s_d);
        if (g > 0) { hi = D; } else { lo = D; }
      }
      var Dm = (lo + hi) / 2, t = trips(Dm, fare), w = wait(t, Dm), e2 = (1 - c) * fare * t / Dm;
      var ur = P.a_r - P.b_r * fare - P.w_r * w;
      return { c: c, trips: t, drivers: Dm, wait: w, earnings: e2, platform: c * fare * t,
               riders: P.riders * Math.log(1 + Math.exp(ur)) / P.b_r,
               driversS: P.drivers * P.s_d * Math.log(1 + Math.exp((e2 - w0) / P.s_d)) };
    }
    QB.widget(el, {
      title: "Set the commission",
      sub: "Run the Island's ride-hailing app. Choose the share of each fare the platform keeps, and the fare itself; " +
           "drivers drive when their hourly pay beats their other work, riders ride when the wait is short. Find " +
           "the commission that earns the platform the most, then look at what riders and drivers lose.",
      panels: 2, height: 250,
      controls: [
        { k: "c", label: "Commission", min: 0, max: 60, step: 1, value: 20, fmt: function (x) { return x + "%"; } },
        { k: "fare", label: "Fare per trip", min: 10, max: 40, step: 1, value: 20,
          fmt: function (x) { return "$" + x; } },
        { k: "w0", label: "Drivers' other work pays (an hour)", min: 10, max: 30, step: 1, value: 20,
          fmt: function (x) { return "$" + x; } },
      ],
      draw: function (g, v, st) {
        var cs = [], pf = [], rd = [], dr = [], tr = [], wt = [];
        for (var k = 0; k <= 60; k += 1) {
          var m = market(k / 100, v.fare, v.w0);
          cs.push(k); pf.push(m.platform); rd.push(m.riders); dr.push(m.driversS); tr.push(m.trips); wt.push(m.wait);
        }
        var best = 0;
        for (var j = 1; j < pf.length; j++) { if (pf[j] > pf[best]) { best = j; } }
        st.m = market(v.c / 100, v.fare, v.w0); st.best = cs[best]; st.bestTake = pf[best];
        var top = Math.max(Math.max.apply(null, rd), Math.max.apply(null, pf), 1) * 1.1;
        var A = g[0].axes({ x: [0, 60], y: [0, top], title: "dollars an hour, by commission (%)",
                            xlabel: "commission, %" });
        A.line(cs, rd, { color: "#7EC8F5", width: 2.2 });
        A.line(cs, dr, { color: "#F2C14E", width: 2.2 });
        A.line(cs, pf, { color: "#C9A0FF", width: 2.6 });
        A.vline(v.c, { color: "#FFFFFF", dash: [4, 4] });
        A.legend([["riders' surplus", "#7EC8F5"], ["drivers' surplus", "#F2C14E"], ["platform's take", "#C9A0FF"]]);
        var tt = Math.max(Math.max.apply(null, tr), 1) * 1.1;
        var B = g[1].axes({ x: [0, 60], y: [0, tt], title: "trips an hour, by commission (%)",
                            xlabel: "commission, %" });
        B.line(cs, tr, { color: "#7FD1B9", width: 2.4 });
        B.vline(v.c, { color: "#FFFFFF", dash: [4, 4] });
      },
      readout: function (v, st) {
        var m = st.m;
        return [["trips an hour, drivers driving", m.trips.toFixed(0) + ", " + m.drivers.toFixed(0)],
                ["the wait, drivers' hourly pay", m.wait.toFixed(1) + " min, $" + m.earnings.toFixed(2)],
                ["the platform's take an hour", "$" + m.platform.toFixed(0)],
                ["riders' and drivers' surplus an hour", "$" + m.riders.toFixed(0) + ", $" + m.driversS.toFixed(0)],
                ["the platform's best commission at this fare", st.best + "% ($" + st.bestTake.toFixed(0) + ")"]];
      },
      note: "Part 61, chapter 2. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
