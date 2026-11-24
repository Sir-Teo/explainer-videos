// Interactives for Act II, Out of the Ground (Parts 8-14).
(function () {
  "use strict";
  var C = QB.C, W = QB.W;

  // ---- Part 8: an oil shock --------------------------------------------------------------------------------------
  // The film's model (explainer/industry/works/oil.py, clearing_multiple): demand q = p^(-ed) and supply
  // q = (1 - loss) p^(es) around a starting point, so the price multiple that clears a lost share of supply is
  // (1 - loss)^(1 / (-ed - es)).  In 2026 EIA put the peak shut-in at 10.9m b/d of about 106m (10%).
  W.oilshock = function (el) {
    function mult(loss, ed, es) { return Math.pow(1 - loss, 1 / (-ed - es)); }
    QB.widget(el, {
      title: "An oil shock: how far must the price rise?",
      sub: "Take a share of the world's oil off the market. In the short run few buyers can use less and few sellers can produce more, so the price has to rise until enough buyers give up enough oil. Set how much of the supply is lost and how strongly each side responds to price, and see the price that clears the market.",
      panels: 2, height: 300,
      controls: [
        { k: "loss", label: "Share of the world's supply lost", min: 0, max: 0.15, step: 0.005, value: 0.05, fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
        { k: "ed", label: "How strongly buyers cut back (% use per 1% price)", min: 0.02, max: 0.5, step: 0.01, value: 0.05, fmt: function (x) { return x.toFixed(2); } },
        { k: "es", label: "How strongly sellers add oil (% supply per 1% price)", min: 0.0, max: 0.5, step: 0.01, value: 0.05, fmt: function (x) { return x.toFixed(2); } },
        { k: "p0", label: "Price before the shock, $ a barrel", min: 40, max: 120, step: 1, value: 70, fmt: function (x) { return "$" + x.toFixed(0); } },
      ],
      draw: function (g, v, s) {
        var m = mult(v.loss, v.ed, v.es), p1 = v.p0 * m, q1 = Math.pow(m, -v.ed);
        var ps = [], dq = [], sq0 = [], sq1 = [], i;
        var top = Math.max(v.p0 * 3.2, p1 * 1.2);
        for (i = 0; i <= 60; i++) {
          var p = v.p0 * 0.3 + (top - v.p0 * 0.3) * i / 60;
          ps.push(p);
          dq.push(100 * Math.pow(p / v.p0, -v.ed));
          sq0.push(100 * Math.pow(p / v.p0, v.es));
          sq1.push(100 * (1 - v.loss) * Math.pow(p / v.p0, v.es));
        }
        var a = g[0].axes({ x: [80, 110], y: [0, top], title: "Supply and demand (oil, before the shock = 100)",
                            xticks: [85, 90, 95, 100, 105], yfmt: function (y) { return "$" + Math.round(y); } });
        a.line(dq, ps, { color: C.p, width: 2.2 });
        a.line(sq0, ps, { color: C.muted, width: 1.4, dash: [4, 4] });
        a.line(sq1, ps, { color: C.loss, width: 2.2 });
        a.dots([100], [v.p0], { color: C.muted, r: 4 });
        a.dots([100 * q1], [p1], { color: C.spot, r: 5 });
        a.legend([["demand", C.p], ["supply before", C.muted], ["supply after", C.loss]], { pos: "tr" });
        var ls = [], ms = [];
        for (i = 0; i <= 60; i++) { var l = 0.15 * i / 60; ls.push(100 * l); ms.push(mult(l, v.ed, v.es)); }
        var b = g[1].axes({ x: [0, 15], y: [1, Math.max(3, m * 1.1)], title: "Price multiple against the share of supply lost",
                            xticks: [0, 5, 10, 15], xfmt: function (x) { return x + "%"; }, yfmt: function (y) { return "x" + y.toFixed(1); } });
        b.line(ls, ms, { color: C.spot, width: 2.2 });
        b.vline(10.3, { color: C.loss });
        b.text(10.5, Math.max(3, m * 1.1) * 0.92, "2026 peak shut-in", { size: 10.5, color: C.loss });
        b.dots([100 * v.loss], [m], { color: C.spot, r: 5 });
        s.r = { m: m, p1: p1, use: 100 * (q1 - 1), rev: m * (1 - v.loss) * Math.pow(m, v.es) - 1 };
      },
      readout: function (v, s) {
        var r = s.r;
        return [["price after the shock", "$" + r.p1.toFixed(0) + " a barrel"],
                ["price multiple", "x" + r.m.toFixed(2)],
                ["oil used, change", r.use.toFixed(1) + "%"],
                ["sellers' revenue, change", (r.rev >= 0 ? "+" : "") + Math.round(100 * r.rev) + "%"]];
      },
      note: "This is the film's chapter 9 model, with constant elasticities. Over 2026 as a whole, EIA's figures imply buyers cut use by about 0.05% for each 1% rise in price; stocks, rerouted pipelines and ships, and lower demand in China cushioned the shock, which is why the price rose less than this model says for a 10% loss.",
    });
  };
})();
