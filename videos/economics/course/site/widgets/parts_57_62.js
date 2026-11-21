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
})();
