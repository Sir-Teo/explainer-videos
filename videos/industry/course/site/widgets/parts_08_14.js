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
  // ---- Part 9: a mine's grade --------------------------------------------------------------------------------------
  // The film's model mine (explainer/industry/works/mine.py): it mills 40 Mt of ore a year for 15 years, the grade
  // falling 2% a year; $2.20 a tonne of rock moved, $7.00 a tonne milled, 55 cents a pound for smelting, freight and
  // overheads; $3bn to build over three years, $300m to close; a 4% royalty and 27% income tax; discounted at 8%.
  W.minegrade = function (el) {
    var LB = 2204.62;
    function cash(grade, strip, rec, price) {
      var ore = 40e6, life = 15, build = 3, capex = 3000, n = build + life + 1, cf = [], k, t;
      for (t = 0; t < n; t++) cf.push(0);
      for (t = 0; t < build; t++) cf[t] -= capex / build;
      var site = ore * (1 + strip) * 2.2 + ore * 7.0, first = null;
      for (k = 0; k < life; k++) {
        var g = grade * Math.pow(0.98, k), cu = ore * g / 100 * rec, lbs = cu * LB / 1e6;
        var unit = site / (cu * LB) + 0.55, rev = price * lbs, cost = unit * lbs, roy = 0.04 * rev;
        var tax = 0.27 * Math.max(rev - cost - roy - capex / life, 0);
        cf[build + k] += rev - cost - roy - tax;
        if (k === 0) first = { cu: cu / 1e3, unit: unit };
      }
      cf[n - 1] -= 300;
      var npv = 0;
      for (t = 0; t < n; t++) npv += cf[t] / Math.pow(1.08, t);
      return { npv: npv, first: first };
    }
    function breakeven(grade, strip, rec) {
      var lo = 0.05, hi = 30, i;
      for (i = 0; i < 60; i++) { var m = (lo + hi) / 2; if (cash(grade, strip, rec, m).npv > 0) hi = m; else lo = m; }
      return (lo + hi) / 2;
    }
    QB.widget(el, {
      title: "A copper mine: how much does grade matter?",
      sub: "Set the share of copper in the ore, the waste rock stripped for each tonne of ore, the share of the copper the mill recovers, and the price of copper. See how much rock a tonne of copper takes, what a pound costs, and what the mine is worth today.",
      panels: 2, height: 300,
      controls: [
        { k: "grade", label: "Copper in the ore (grade)", min: 0.2, max: 2.0, step: 0.01, value: 0.5, fmt: function (x) { return x.toFixed(2) + "%"; } },
        { k: "strip", label: "Waste rock per tonne of ore (strip ratio)", min: 0, max: 4, step: 0.1, value: 2, fmt: function (x) { return x.toFixed(1) + " : 1"; } },
        { k: "rec", label: "Share of the copper recovered", min: 0.6, max: 0.95, step: 0.01, value: 0.87, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "price", label: "Copper price, $ a pound", min: 1.5, max: 8, step: 0.05, value: 4.5, fmt: function (x) { return "$" + x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var gs = [], rock = [], i;
        for (i = 0; i <= 60; i++) { var gg = 0.2 + 1.8 * i / 60; gs.push(gg); rock.push((1 + v.strip) / (gg / 100 * v.rec)); }
        var here = (1 + v.strip) / (v.grade / 100 * v.rec);
        var a = g[0].axes({ x: [0.2, 2.0], y: [10, 3000], logy: true, title: "Tonnes of rock moved for a tonne of copper",
                            xticks: [0.25, 0.5, 1, 1.5, 2], xfmt: function (x) { return x + "%"; },
                            yticks: [10, 30, 100, 300, 1000, 3000], yfmt: function (y) { return Math.round(y).toLocaleString(); } });
        a.line(gs, rock, { color: C.house, width: 2.2 });
        a.dots([v.grade], [here], { color: C.spot, r: 5 });
        a.vline(1.02, { color: C.muted });
        a.text(1.05, 2000, "Escondida 2025", { size: 10.5, color: C.muted });
        var be = breakeven(v.grade, v.strip, v.rec), ps = [], vs = [], top = 8, j;
        for (j = 0; j <= 50; j++) { var p = 1.5 + (top - 1.5) * j / 50; ps.push(p); vs.push(cash(v.grade, v.strip, v.rec, p).npv / 1000); }
        var now = cash(v.grade, v.strip, v.rec, v.price);
        var lo = Math.min(-4, vs[0] * 1.05), hi = Math.max(4, vs[vs.length - 1] * 1.05);
        var b = g[1].axes({ x: [1.5, top], y: [lo, hi], title: "What the mine is worth today, $bn, against the copper price",
                            xticks: [2, 3, 4, 5, 6, 7, 8], xfmt: function (x) { return "$" + x; }, yfmt: function (y) { return y.toFixed(0); } });
        b.hline(0, { color: C.muted });
        b.line(ps, vs, { color: C.p, width: 2.2 });
        if (be < top) { b.vline(be, { color: C.loss }); b.text(be + 0.08, hi * 0.85, "break-even", { size: 10.5, color: C.loss }); }
        b.dots([v.price], [now.npv / 1000], { color: C.spot, r: 5 });
        s.r = { rock: here, cu: now.first.cu, unit: now.first.unit, be: be, npv: now.npv };
      },
      readout: function (v, s) {
        var r = s.r;
        return [["rock for a tonne of copper", Math.round(r.rock).toLocaleString() + " t"],
                ["copper in year one", Math.round(r.cu) + " kt"],
                ["cash cost a pound, year one", "$" + r.unit.toFixed(2)],
                ["break-even price", r.be < 29 ? "$" + r.be.toFixed(2) : "none below $30"],
                ["worth today", (r.npv >= 0 ? "$" : "-$") + Math.abs(r.npv / 1000).toFixed(2) + "bn"]];
      },
      note: "This is the film's model mine. At its default grade of 0.5% it needs $3.61 a pound to pay its way; Escondida milled ore at 1.02% in 2025 and expects about 0.85% in 2026. Real mines differ in size, depth, power, water and by-products, and gold or molybdenum in the ore can pay much of the cost.",
    });
  };
  // ---- Part 10: Cochrane's treadmill ------------------------------------------------------------------------------
  // The film's model (explainer/industry/works/farm.py, treadmill): a method that grows `gain` more on the same costs
  // spreads along a logistic curve; demand has constant elasticity, so the price is output^(1/elasticity), starting
  // 15% above the cost of a unit.  An adopter's margin is price x (1 + gain) - cost; a laggard's, price - cost.
  W.treadmill = function (el) {
    QB.widget(el, {
      title: "Cochrane's treadmill: who keeps the gain from a better seed?",
      sub: "A new method lets farmers grow more on the same costs. The first to adopt it profit; as everyone copies them, output rises and the price falls. Set how big the gain is, how much more people buy when food gets cheaper, and how fast farmers adopt, and see who ends up with the gain.",
      panels: 2, height: 300,
      controls: [
        { k: "gain", label: "Extra output from the new method", min: 0.02, max: 0.4, step: 0.01, value: 0.12, fmt: function (x) { return "+" + Math.round(100 * x) + "%"; } },
        { k: "el", label: "Demand elasticity (% more bought for 1% lower price)", min: 0.1, max: 2.0, step: 0.05, value: 0.4, fmt: function (x) { return "-" + x.toFixed(2); } },
        { k: "speed", label: "How fast farmers adopt", min: 0.15, max: 1.2, step: 0.05, value: 0.45, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var n = 30, t, share = [], price = [], ad = [], lag = [], yrs = [];
        for (t = 0; t < n; t++) {
          var sh = 1 / (1 + Math.exp(-v.speed * (t - 10))), q = 1 + v.gain * sh, p = Math.pow(q, -1 / v.el) * 1.15;
          yrs.push(t); share.push(sh); price.push(p); ad.push(p * (1 + v.gain) - 1); lag.push(p - 1);
        }
        var a = g[0].axes({ x: [0, n - 1], y: [0, 1.25], title: "Price (1 = the cost of a unit) and share adopted",
                            xticks: [0, 10, 20, 29], xfmt: function (x) { return "yr " + x; }, yfmt: function (y) { return y.toFixed(1); } });
        a.line(yrs, price, { color: C.p, width: 2.2 });
        a.line(yrs, share, { color: C.muted, width: 1.4, dash: [4, 4] });
        a.hline(1, { color: C.loss });
        a.legend([["price", C.p], ["share adopted", C.muted], ["cost", C.loss]], { pos: "bl" });
        var lo = Math.min(-0.3, Math.min.apply(null, lag) * 1.1), hi = Math.max(0.4, Math.max.apply(null, ad) * 1.1);
        var b = g[1].axes({ x: [0, n - 1], y: [lo, hi], title: "Margin over cost: early adopter and laggard",
                            xticks: [0, 10, 20, 29], xfmt: function (x) { return "yr " + x; }, yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.hline(0, { color: C.muted });
        b.line(yrs, ad, { color: C.gain, width: 2.2 });
        b.line(yrs, lag, { color: C.loss, width: 2.2 });
        b.legend([["adopter", C.gain], ["laggard", C.loss]], { pos: "tr" });
        s.r = { p: price[n - 1] / price[0], a0: ad[0], a1: ad[n - 1], l1: lag[n - 1] };
      },
      readout: function (v, s) {
        var r = s.r;
        return [["price at the end", (r.p >= 1 ? "+" : "") + Math.round(100 * (r.p - 1)) + "%"],
                ["early adopter's margin, year 0", "+" + Math.round(100 * r.a0) + "%"],
                ["adopter's margin at the end", (r.a1 >= 0 ? "+" : "") + Math.round(100 * r.a1) + "%"],
                ["laggard's margin at the end", (r.l1 >= 0 ? "+" : "") + Math.round(100 * r.l1) + "%"]];
      },
      note: "This is the film's chapter 4 model. Food has inelastic demand (people do not eat much more when it is cheap), so a better seed lowers the price a long way and the gain passes to the people who eat. Try a high elasticity, like a product people buy more of when it is cheaper: the price falls less and the adopters keep more.",
    });
  };
})();
