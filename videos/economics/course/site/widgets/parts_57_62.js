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
})();
