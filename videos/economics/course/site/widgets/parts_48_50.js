// Interactives for Act IX, The Fields (Parts 43-50, second block: 48-50).  Each is a game the reader plays (the kit:
// 00_games.js).
(function () {
  "use strict";
  var W = QB.W;

  // ---- Part 48: environment and climate -------------------------------------------------------------------------
  W.carbonprice = function (el) {
    // Agora's DICE-style model (explainer.economics.agora.climate: Dice.scc): the consumption lost each year,
    // 2025-2300, per tonne of CO2 emitted in 2025 (D, dollars of 2019), and the growth of consumption per head (G).
    // The social cost of carbon discounts D by the Ramsey factor (1 + rho)^-t (c_t / c_0)^-eta.
    var D = [0.000, 0.349, 0.595, 0.773, 0.907, 1.011, 1.095, 1.167, 1.229, 1.286, 1.338, 1.388, 1.436, 1.483, 1.529,
      1.575, 1.620, 1.665, 1.710, 1.755, 1.800, 1.846, 1.891, 1.937, 1.983, 2.030, 2.076, 2.123, 2.171, 2.219, 2.267,
      2.315, 2.364, 2.413, 2.463, 2.513, 2.564, 2.615, 2.666, 2.718, 2.770, 2.823, 2.876, 2.930, 2.984, 3.038, 3.094,
      3.149, 3.205, 3.261, 3.318, 3.376, 3.434, 3.492, 3.551, 3.610, 3.670, 3.730, 3.791, 3.852, 3.913, 3.975, 4.038,
      4.101, 4.164, 4.228, 4.292, 4.356, 4.422, 4.487, 4.553, 4.620, 4.686, 4.753, 4.821, 4.889, 4.958, 5.027, 5.096,
      5.165, 5.236, 5.306, 5.377, 5.448, 5.520, 5.592, 5.665, 5.737, 5.811, 5.884, 5.958, 6.032, 6.107, 6.182, 6.258,
      6.333, 6.410, 6.486, 6.563, 6.640, 6.717, 6.795, 6.873, 6.952, 7.030, 7.109, 7.189, 7.268, 7.348, 7.428, 7.509,
      7.590, 7.670, 7.752, 7.833, 7.915, 7.997, 8.079, 8.162, 8.245, 8.328, 8.411, 8.495, 8.578, 8.662, 8.746, 8.831,
      8.915, 9.000, 9.085, 9.170, 9.256, 9.341, 9.427, 9.513, 9.599, 9.685, 9.771, 9.858, 9.944, 10.031, 10.118,
      10.205, 10.293, 10.380, 10.467, 10.555, 10.643, 10.731, 10.819, 10.907, 10.995, 11.083, 11.171, 11.260, 11.348,
      11.437, 11.526, 11.614, 11.703, 11.792, 11.881, 11.970, 12.059, 12.148, 12.237, 12.326, 12.415, 12.505, 12.594,
      12.683, 12.773, 12.862, 12.951, 13.040, 13.130, 13.219, 13.308, 13.398, 13.487, 13.576, 13.665, 13.755, 13.844,
      13.933, 14.022, 14.111, 14.200, 14.289, 14.378, 14.467, 14.556, 14.645, 14.734, 14.822, 14.911, 15.000, 15.088,
      15.177, 15.265, 15.353, 15.441, 15.529, 15.617, 15.705, 15.793, 15.880, 15.968, 16.055, 16.143, 16.230, 16.317,
      16.404, 16.491, 16.578, 16.665, 16.751, 16.837, 16.924, 17.010, 17.096, 17.181, 17.267, 17.353, 17.438, 17.523,
      17.608, 17.693, 17.778, 17.863, 17.947, 18.031, 18.115, 18.199, 18.283, 18.367, 18.450, 18.533, 18.616, 18.699,
      18.782, 18.864, 18.947, 19.029, 19.111, 19.192, 19.274, 19.355, 19.436, 19.517, 19.598, 19.678, 19.759, 19.839,
      19.919, 19.998, 20.078, 20.157, 20.236, 20.315, 20.394, 20.472, 20.550, 20.628, 20.706, 20.784, 20.861, 20.938,
      21.015, 21.091, 21.168, 21.244, 21.320, 21.395, 21.471, 21.546];
    var G = [0.01835, 0.01834, 0.01831, 0.01827, 0.01822, 0.01816, 0.01809, 0.01801, 0.01793, 0.01784, 0.01775,
      0.01765, 0.01755, 0.01744, 0.01734, 0.01723, 0.01712, 0.01700, 0.01689, 0.01677, 0.01666, 0.01654, 0.01643,
      0.01631, 0.01619, 0.01608, 0.01596, 0.01584, 0.01573, 0.01561, 0.01550, 0.01538, 0.01527, 0.01516, 0.01505,
      0.01494, 0.01482, 0.01472, 0.01461, 0.01450, 0.01439, 0.01429, 0.01418, 0.01408, 0.01398, 0.01387, 0.01377,
      0.01367, 0.01357, 0.01347, 0.01338, 0.01328, 0.01319, 0.01309, 0.01300, 0.01291, 0.01281, 0.01272, 0.01263,
      0.01254, 0.01246, 0.01237, 0.01228, 0.01220, 0.01211, 0.01203, 0.01195, 0.01186, 0.01178, 0.01170, 0.01162,
      0.01154, 0.01146, 0.01139, 0.01131, 0.01124, 0.01117, 0.01109, 0.01102, 0.01094, 0.01087, 0.01079, 0.01072,
      0.01065, 0.01058, 0.01051, 0.01044, 0.01037, 0.01030, 0.01023, 0.01016, 0.01009, 0.01003, 0.00996, 0.00989,
      0.00983, 0.00976, 0.00970, 0.00964, 0.00957, 0.00951, 0.00945, 0.00939, 0.00933, 0.00927, 0.00921, 0.00915,
      0.00909, 0.00903, 0.00897, 0.00891, 0.00886, 0.00880, 0.00874, 0.00869, 0.00863, 0.00858, 0.00852, 0.00847,
      0.00842, 0.00836, 0.00831, 0.00826, 0.00820, 0.00815, 0.00810, 0.00805, 0.00800, 0.00795, 0.00790, 0.00785,
      0.00780, 0.00775, 0.00771, 0.00766, 0.00761, 0.00756, 0.00752, 0.00747, 0.00742, 0.00738, 0.00733, 0.00729,
      0.00724, 0.00720, 0.00715, 0.00711, 0.00706, 0.00702, 0.00698, 0.00694, 0.00689, 0.00685, 0.00681, 0.00677,
      0.00673, 0.00669, 0.00664, 0.00660, 0.00656, 0.00652, 0.00648, 0.00645, 0.00641, 0.00637, 0.00633, 0.00629,
      0.00625, 0.00621, 0.00618, 0.00614, 0.00610, 0.00607, 0.00603, 0.00599, 0.00596, 0.00592, 0.00589, 0.00585,
      0.00582, 0.00578, 0.00575, 0.00571, 0.00568, 0.00564, 0.00561, 0.00558, 0.00554, 0.00551, 0.00548, 0.00544,
      0.00541, 0.00538, 0.00535, 0.00532, 0.00528, 0.00525, 0.00522, 0.00519, 0.00516, 0.00513, 0.00510, 0.00507,
      0.00504, 0.00501, 0.00498, 0.00495, 0.00492, 0.00489, 0.00486, 0.00483, 0.00480, 0.00478, 0.00475, 0.00472,
      0.00469, 0.00466, 0.00464, 0.00461, 0.00458, 0.00456, 0.00453, 0.00450, 0.00448, 0.00445, 0.00442, 0.00440,
      0.00437, 0.00435, 0.00432, 0.00430, 0.00427, 0.00424, 0.00422, 0.00420, 0.00417, 0.00415, 0.00412, 0.00410,
      0.00407, 0.00405, 0.00403, 0.00400, 0.00398, 0.00396, 0.00393, 0.00391, 0.00389, 0.00387, 0.00384, 0.00382,
      0.00380, 0.00378, 0.00375, 0.00373, 0.00371, 0.00369, 0.00367, 0.00365, 0.00362, 0.00360, 0.00358, 0.00356,
      0.00354, 0.00352, 0.00350, 0.00348, 0.00346, 0.00344, 0.00342, 0.00340, 0.00338, 0.00336, 0.00334, 0.00332];
    function factors(rho, eta) {
      var f = [1], lc = 0;
      for (var t = 1; t < D.length; t++) { lc += G[t - 1]; f.push(Math.pow(1 + rho, -t) * Math.exp(-eta * lc)); }
      return f;
    }
    function scc(rho, eta) {
      var f = factors(rho, eta), s = 0, late = 0;
      for (var t = 0; t < D.length; t++) { s += D[t] * f[t]; if (t > 75) late += D[t] * f[t]; }
      return { scc: s, late: late / s, f: f };
    }
    QB.widget(el, {
      title: "Price a tonne",
      sub: "Left: the damage one tonne emitted in 2025 does each year (grey) and what it is worth today at your " +
           "discounting (red). Right: the social cost of carbon as pure time preference varies, at your eta.",
      panels: 2, height: 270,
      controls: [
        { k: "rho", label: "Pure time preference, rho", min: 0, max: 0.03, step: 0.001, value: 0.015,
          fmt: function (x) { return (100 * x).toFixed(1) + "% a year"; } },
        { k: "eta", label: "How fast a dollar matters less as people grow richer, eta", min: 0, max: 2.5, step: 0.05,
          value: 1.45, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, st) {
        var r = scc(v.rho, v.eta), yrs = [], disc = [];
        for (var t = 0; t < D.length; t++) { yrs.push(2025 + t); disc.push(D[t] * r.f[t]); }
        var A = g[0].axes({ x: [2025, 2300], y: [0, 24], title: "dollars a year, per tonne", xlabel: "year" });
        A.line(yrs, D, { color: "#9AA3B2", width: 2 });
        A.line(yrs, disc, { color: "#F25F5C", width: 2.5 });
        A.vline(2100, { color: "#6B7280", dash: [3, 3] });
        var rs = [], ss = [];
        for (var k = 0; k <= 30; k++) { var rr = k * 0.001; rs.push(100 * rr); ss.push(scc(rr, v.eta).scc); }
        var top = Math.min(Math.max.apply(null, ss) * 1.1, 3000);
        var B = g[1].axes({ x: [0, 3], y: [0, top], title: "social cost of carbon, $ a tonne",
                            xlabel: "pure time preference, %" });
        B.line(rs, ss.map(function (y) { return Math.min(y, top); }), { color: "#7FD1B9", width: 2.5 });
        B.dots([100 * v.rho], [Math.min(r.scc, top)], { color: "#F2C14E", r: 5 });
        st.r = r; st.g0 = G.slice(0, 25).reduce(function (a, b) { return a + b; }, 0) / 25;
      },
      readout: function (v, st) {
        return [["social cost of carbon", "$" + st.r.scc.toFixed(0) + " a tonne"],
                ["from damage after 2100", (100 * st.r.late).toFixed(0) + "%"],
                ["implied discount rate, first 25 years", (100 * (v.rho + v.eta * st.g0)).toFixed(2) + "% a year"],
                ["for comparison", "DICE-2023: $66 (base), $87 at 3%, $176 at 2%"]];
      },
      note: "Part 48, chapters 6 and 7. The damage stream is the film's model's, for a pulse in 2025 on today's " +
            "policies; at rho 1.5% and eta 1.45 it gives about $63, at rho 0.1% and eta 1 about $408. Computed in " +
            "your browser; nothing you do here is stored or sent.",
    });
  };

  // ---- Part 49: the economic approach ---------------------------------------------------------------------------
  W.deter = function (el) {
    // Agora's economic approach (explainer.economics.agora.family: offend_share): potential offenders with gains
    // log-normal around one year of prison (log-sd 0.8), here 400 evenly spaced quantiles; an offender with CARA
    // coefficient a, who counts each later year of a sentence beta times the one before, offends when
    // (1 - p) u(g) + p u(g - F) > 0, with F the felt sentence.
    function qnorm(p) {                       // Acklam's approximation to the normal quantile
      var a = [-39.69683028665376, 220.9460984245205, -275.9285104469687, 138.3577518672690, -30.66479806614716,
               2.506628277459239];
      var b = [-54.47609879822406, 161.5858368580409, -155.6989798598866, 66.80131188771972, -13.28068155288572];
      var c = [-0.007784894002430293, -0.3223964580411365, -2.400758277161838, -2.549732539343734,
               4.374664141464968, 2.938163982698783];
      var d = [0.007784695709041462, 0.3224671290700398, 2.445134137142996, 3.754408661907416];
      var q, r;
      if (p < 0.02425) {
        q = Math.sqrt(-2 * Math.log(p));
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
      }
      if (p > 1 - 0.02425) { return -qnorm(1 - p); }
      q = p - 0.5; r = q * q;
      return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q /
             (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
    }
    var N = 400, gains = [];
    for (var i = 0; i < N; i++) { gains.push(Math.exp(0.8 * qnorm((i + 0.5) / N))); }
    function u(x, a) { return Math.abs(a) < 1e-9 ? x : (1 - Math.exp(-a * x)) / a; }
    function felt(S, beta) { return Math.abs(beta - 1) < 1e-9 ? S : (1 - Math.pow(beta, S)) / (1 - beta); }
    function share(p, S, a, beta) {
      var F = felt(S, beta), n = 0;
      for (var i = 0; i < N; i++) { if ((1 - p) * u(gains[i], a) + p * u(gains[i] - F, a) > 0) n++; }
      return n / N;
    }
    QB.widget(el, {
      title: "Deter",
      sub: "You run the Island's justice system. Left: the share who offend as the chance of being caught varies " +
           "(purple) and as the sentence varies (gold), scaled so both start at your settings. Right: what doubling " +
           "each would do.",
      panels: 2, height: 260,
      controls: [
        { k: "p", label: "Chance of being caught", min: 0.02, max: 0.5, step: 0.01, value: 0.2,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
        { k: "S", label: "Sentence, years", min: 0.5, max: 10, step: 0.5, value: 3,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "a", label: "Dislike of risk (CARA)", min: -0.3, max: 1.0, step: 0.05, value: 0,
          fmt: function (x) { return x.toFixed(2) + (x < 0 ? " (likes risk)" : x > 0 ? "" : " (indifferent)"); } },
        { k: "beta", label: "Weight on each later year of prison", min: 0.6, max: 1.0, step: 0.01, value: 1.0,
          fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, st) {
        var ks = [], sp = [], ss = [];
        for (var k = 0; k <= 30; k++) {
          var m = 0.25 + k * 0.125;                  // a multiple of today's setting, 0.25 to 4
          ks.push(m);
          sp.push(share(Math.min(v.p * m, 1), v.S, v.a, v.beta));
          ss.push(share(v.p, v.S * m, v.a, v.beta));
        }
        var A = g[0].axes({ x: [0, 4], y: [0, 1], title: "share who offend", xlabel: "multiple of today's setting" });
        A.line(ks, sp, { color: "#C9A0FF", width: 2.5 });
        A.line(ks, ss, { color: "#F2C14E", width: 2.5 });
        A.vline(1, { color: "#6B7280", dash: [3, 3] });
        A.vline(2, { color: "#6B7280", dash: [2, 4] });
        st.now = share(v.p, v.S, v.a, v.beta);
        st.dp = share(Math.min(2 * v.p, 1), v.S, v.a, v.beta);
        st.ds = share(v.p, 2 * v.S, v.a, v.beta);
        var B = g[1].axes({ x: [0, 3], y: [0, 1], title: "share who offend", xlabel: "now, chance x2, sentence x2" });
        B.bars([0.5, 1.5, 2.5], [st.now, st.dp, st.ds], 0.6,
               { color: function (i) { return ["#9AA3B2", "#C9A0FF", "#F2C14E"][i]; } });
      },
      readout: function (v, st) {
        var best = Math.abs(st.dp - st.ds) < 0.005 ? "no difference" : (st.dp < st.ds ? "the chance" : "the sentence");
        return [["offend now", (100 * st.now).toFixed(0) + "%"],
                ["with the chance doubled", (100 * st.dp).toFixed(0) + "%"],
                ["with the sentence doubled", (100 * st.ds).toFixed(0) + "%"],
                ["deters more", best],
                ["expected sentence, p x S", (v.p * v.S).toFixed(2) + " years"]];
      },
      note: "Part 49, chapters 1 and 2. Risk-neutral offenders who count every year respond only to p x S; those " +
            "who dislike risk fear the long sentence more; those who count later years for less are deterred more by " +
            "the chance, as most evidence finds. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
