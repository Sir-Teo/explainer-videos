// Interactives for Act IX, The Fields (Parts 43-50, first block: 43-47).  Each is a game the reader plays (the kit:
// 00_games.js).
(function () {
  "use strict";
  var W = QB.W;
  var GOLD = "#F6C453", RED = "#F25F5C", TEAL = "#7FD1B9", PINK = "#E8A0B4", GREY = "#9AA3B2";

  // ---- Part 43: measuring market power ---------------------------------------------------------------------------
  W.merger = function (el) {
    // The merger game of Part 43 (explainer.economics.agora.io: nested_shares, bertrand, merger): five cereals in three
    // nests (sweet, nutty, bran), each with its own owner, nested logit with price coefficient 1 and nesting
    // parameter sigma; Bertrand-Nash prices by damped iteration on the first-order conditions,
    // p - c = -(Omega o J)^-1 s, with J[j][k] = ds_k/dp_j.
    var NAMES = ["Sun Flakes", "Honey Puffs", "Nut Clusters", "Bran Buds", "Bran Twigs"];
    var NEST = [0, 0, 1, 2, 2], Q = [0.8, 0.0, 1.0, -0.5, -0.5], MC = [1.5, 1.2, 1.6, 1.0, 1.0];
    var COL = [GOLD, GOLD, PINK, TEAL, TEAL];
    var PAIRS = [];
    for (var a = 0; a < 5; a++) for (var b = a + 1; b < 5; b++) PAIRS.push([a, b]);
    function shares(p, sg) {
      var d = [], D = [0, 0, 0], j, s = [], cond = [];
      for (j = 0; j < 5; j++) { d.push(Math.exp((Q[j] - p[j]) / (1 - sg))); D[NEST[j]] += d[j]; }
      var den = 1; for (var g = 0; g < 3; g++) den += Math.pow(D[g], 1 - sg);
      for (j = 0; j < 5; j++) { cond.push(d[j] / D[NEST[j]]); s.push(cond[j] * Math.pow(D[NEST[j]], 1 - sg) / den); }
      return { s: s, cond: cond, cs: Math.log(den) };
    }
    function jac(p, sg) { // J[j][k] = ds_k / dp_j
      var r = shares(p, sg), s = r.s, c = r.cond, J = [], j, k;
      for (j = 0; j < 5; j++) {
        J.push([]);
        for (k = 0; k < 5; k++) {
          var v;
          if (j === k) v = -s[j] * (1 / (1 - sg) - sg / (1 - sg) * c[j] - s[j]);
          else if (NEST[j] === NEST[k]) v = s[k] * (sg / (1 - sg) * c[j] + s[j]);
          else v = s[k] * s[j];
          J[j].push(v);
        }
      }
      return { J: J, s: s, cs: r.cs };
    }
    function solve(A, y) { // Gaussian elimination with partial pivoting
      var n = y.length, M = A.map(function (row, i) { return row.slice().concat([y[i]]); }), i, k, r;
      for (i = 0; i < n; i++) {
        var piv = i; for (r = i + 1; r < n; r++) if (Math.abs(M[r][i]) > Math.abs(M[piv][i])) piv = r;
        var t = M[i]; M[i] = M[piv]; M[piv] = t;
        for (r = i + 1; r < n; r++) { var f = M[r][i] / M[i][i]; for (k = i; k <= n; k++) M[r][k] -= f * M[i][k]; }
      }
      var x = new Array(n).fill(0);
      for (i = n - 1; i >= 0; i--) { var sum = M[i][n]; for (k = i + 1; k < n; k++) sum -= M[i][k] * x[k]; x[i] = sum / M[i][i]; }
      return x;
    }
    function bertrand(mc, owner, sg, p0) {
      var p = (p0 || mc.map(function (c) { return 1.4 * c; })).slice(), it, j, k;
      for (it = 0; it < 400; it++) {
        var r = jac(p, sg), A = [];
        for (j = 0; j < 5; j++) { A.push([]); for (k = 0; k < 5; k++) A[j].push(owner[j] === owner[k] ? r.J[j][k] : 0); }
        var m = solve(A, r.s.map(function (x) { return -x; })), diff = 0;
        for (j = 0; j < 5; j++) { var nw = mc[j] + m[j]; diff = Math.max(diff, Math.abs(nw - p[j])); p[j] = 0.5 * p[j] + 0.5 * nw; }
        if (diff < 1e-10) break;
      }
      return p;
    }
    function simulate(sg, pair, save) {
      var own0 = [0, 1, 2, 3, 4], own1 = own0.slice(); own1[pair[1]] = pair[0];
      var p0 = bertrand(MC, own0, sg), mc1 = MC.slice();
      mc1[pair[0]] *= 1 - save; mc1[pair[1]] *= 1 - save;
      var p1 = bertrand(mc1, own1, sg, p0);
      var r0 = jac(p0, sg), r1 = shares(p1, sg);
      var tot = r0.s.reduce(function (x, y) { return x + y; }, 0);
      var hhi0 = 0, j; for (j = 0; j < 5; j++) hhi0 += Math.pow(100 * r0.s[j] / tot, 2);
      var dhhi = 2 * (100 * r0.s[pair[0]] / tot) * (100 * r0.s[pair[1]] / tot);
      var div = -r0.J[pair[0]][pair[1]] / r0.J[pair[0]][pair[0]];
      return { p0: p0, p1: p1, dp: p1.map(function (x, k) { return x / p0[k] - 1; }), hhi0: hhi0, dhhi: dhhi,
               dcs: r1.cs / r0.cs - 1, div: div,
               upp: div * (p0[pair[1]] - MC[pair[1]]) - save * MC[pair[0]] };
    }
    QB.widget(el, {
      title: "Simulate a merger",
      sub: "Left: each brand's price change after the merger you choose (the merging pair outlined in white). " +
           "Right: the merging brands' average price rise against the nesting parameter, for your pair (green) " +
           "and for the game's two mergers, the bran twins (teal) and the two largest (gold).",
      panels: 2, height: 270,
      controls: [
        { k: "pair", label: "Which two brands merge", min: 0, max: 9, step: 1, value: 9,
          fmt: function (x) { var q = PAIRS[Math.round(x)]; return NAMES[q[0]] + " + " + NAMES[q[1]]; } },
        { k: "sg", label: "Nesting parameter, sigma", min: 0, max: 0.9, step: 0.01, value: 0.6,
          fmt: function (x) { return x.toFixed(2); } },
        { k: "save", label: "Cost savings for the merging brands", min: 0, max: 0.3, step: 0.01, value: 0,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
      ],
      draw: function (g, v, st) {
        var pair = PAIRS[Math.round(v.pair)], r = simulate(v.sg, pair, v.save), k;
        var lo = Math.min(-0.1, Math.min.apply(null, r.dp) * 1.2), hi = Math.max(0.1, Math.max.apply(null, r.dp) * 1.2);
        var A = g[0].axes({ x: [-0.5, 4.5], y: [lo, hi], title: "price change by brand", xlabel: "brand" });
        A.bars([0, 1, 2, 3, 4], r.dp, 0.6, { color: function (i) { return COL[i]; } });
        A.hline(0, { color: GREY });
        for (k = 0; k < 2; k++) A.text(pair[k], r.dp[pair[k]], (100 * r.dp[pair[k]]).toFixed(1) + "%",
                                       { align: "center", dy: r.dp[pair[k]] >= 0 ? -10 : 10, bg: true });
        var sgs = [], mine = [], xs = [], ys = [];
        for (k = 0; k <= 18; k++) {
          var s = k * 0.05; sgs.push(s);
          var a = simulate(s, pair, v.save), x = simulate(s, [3, 4], v.save), y = simulate(s, [0, 2], v.save);
          mine.push((a.dp[pair[0]] + a.dp[pair[1]]) / 2);
          xs.push((x.dp[3] + x.dp[4]) / 2); ys.push((y.dp[0] + y.dp[2]) / 2);
        }
        var top = Math.max(0.05, Math.max.apply(null, mine.concat(xs, ys)) * 1.1);
        var B = g[1].axes({ x: [0, 0.9], y: [Math.min(0, Math.min.apply(null, mine.concat(xs, ys))), top],
                            title: "merging brands' price rise", xlabel: "nesting parameter sigma" });
        B.line(sgs, xs, { color: TEAL, width: 2 });
        B.line(sgs, ys, { color: GOLD, width: 2 });
        B.line(sgs, mine, { color: "#7BD88F", width: 2.5, dash: [5, 3] });
        B.vline(v.sg, { color: GREY });
        st.r = r; st.pair = pair;
      },
      readout: function (v, st) {
        var r = st.r, p = st.pair;
        return [["merging brands' prices", (100 * (r.dp[p[0]] + r.dp[p[1]]) / 2).toFixed(1) + "%"],
                ["Herfindahl index", r.hhi0.toFixed(0) + " + " + r.dhhi.toFixed(0)],
                ["diversion from " + NAMES[p[0]] + " to " + NAMES[p[1]], (100 * r.div).toFixed(0) + "%"],
                ["upward pricing pressure on " + NAMES[p[0]], r.upp.toFixed(3)],
                ["shoppers' surplus", (100 * r.dcs).toFixed(1) + "%"]];
      },
      note: "Part 43, chapters 2, 9 and 14. Costs and qualities are the game's; the Herfindahl index counts shares of " +
            "cereal sales. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
