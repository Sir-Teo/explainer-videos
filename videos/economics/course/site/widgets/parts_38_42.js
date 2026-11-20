// Interactives for Act VIII, Work and the State (Parts 38-42).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var W = QB.W;
  var GOLD = "#F6C453", RED = "#F25F5C", TEAL = "#7FD1B9", VIOLET = "#C9A0FF";

  // ---- Part 38: work and wages ---------------------------------------------------------------------------------
  W.minimum = function (el) {
    // A firm facing labour supply L = 200 (w/6)^eta and a marginal product 6 (L/200)^-0.3, so that a competitive
    // market would pay $6 and hire 200 (explainer.economics.agora.labour: monopsony, floor_monopsony).  The firm
    // hires where the marginal cost of labour, w (1 + 1/eta), meets the marginal product; a minimum wage between its
    // own wage and $6 raises employment, above $6 it lowers it.
    var B = 0.3, WC = 6, LC = 200;
    function supplyL(w, eta) { return LC * Math.pow(w / WC, eta); }
    function demandL(w) { return LC * Math.pow(w / WC, -1 / B); }
    function mono(eta) {
      var L = LC * Math.pow(eta / (1 + eta), 1 / (1 / eta + B));
      return { L: L, w: WC * Math.pow(L / LC, 1 / eta) };
    }
    function employ(m, eta) {
      var M = mono(eta);
      if (m <= M.w) return M.L;
      return Math.min(supplyL(m, eta), demandL(m));
    }
    function f2(x) { return x.toFixed(2); }
    QB.widget(el, {
      title: "A minimum wage at a firm that sets wages",
      sub: "Left: the firm's supply of workers (teal), the cost of one more worker (violet), what one more adds (red) " +
           "and your minimum (gold). Right: workers hired against the minimum wage, with yours marked.",
      panels: 2, height: 270,
      controls: [
        { k: "m", label: "Minimum wage, $ an hour", min: 3.5, max: 8, step: 0.05, value: 5.5, fmt: f2 },
        { k: "eta", label: "Supply elasticity facing the firm (large = competitive)", min: 1, max: 20, step: 0.5,
          value: 3, fmt: function (x) { return x.toFixed(1); } },
      ],
      draw: function (g, v, st) {
        var Ls = [], ws = [], mcl = [], mrp = [], k;
        for (k = 0; k <= 60; k++) {
          var L = 40 + 280 * k / 60;
          var w = WC * Math.pow(L / LC, 1 / v.eta);
          Ls.push(L); ws.push(w); mcl.push(w * (1 + 1 / v.eta)); mrp.push(WC * Math.pow(L / LC, -B));
        }
        var a = g[0].axes({ x: [40, 320], y: [3, 9], title: "the firm's labour market", xlabel: "workers" });
        a.line(Ls, ws.map(function (w) { return Math.min(w, 9); }), { color: TEAL, width: 2.5 });
        a.line(Ls, mcl.map(function (w) { return Math.min(w, 9); }), { color: VIOLET, width: 2.5 });
        a.line(Ls, mrp.map(function (w) { return Math.min(w, 9); }), { color: RED, width: 2.5 });
        a.hline(v.m, { color: GOLD });
        var M = mono(v.eta), now = employ(v.m, v.eta);
        a.dots([M.L], [M.w], { color: VIOLET, r: 5 });
        var ms = [], es = [];
        for (k = 0; k <= 80; k++) { var mm = 3.5 + 4.5 * k / 80; ms.push(mm); es.push(employ(mm, v.eta)); }
        var b = g[1].axes({ x: [3.5, 8], y: [0, 260], title: "workers hired", xlabel: "minimum wage, $" });
        b.line(ms, es.map(function (e) { return Math.min(e, 260); }), { color: GOLD, width: 2.5 });
        b.dots([v.m], [Math.min(now, 260)], { color: GOLD, r: 6 });
        st.M = M; st.now = now;
      },
      readout: function (v, st) {
        return [["the firm's own wage and hiring", "$" + st.M.w.toFixed(2) + ", " + st.M.L.toFixed(0) + " workers"],
                ["hiring at your minimum", st.now.toFixed(0) + " (" + (100 * (st.now / st.M.L - 1)).toFixed(0) +
                  "% against no minimum)"],
                ["the markdown below what a worker adds", (100 / (1 + v.eta)).toFixed(0) + "%"]];
      },
      note: "The model of Part 38, chapter 7. A minimum between the firm's wage and the competitive $6 raises " +
            "employment; above $6 it lowers it. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
