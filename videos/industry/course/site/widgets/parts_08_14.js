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
  // ---- Part 11: a mill in a glut --------------------------------------------------------------------------------
  // The film's model (explainer/industry/works/mill.py, glut and industry_glut): an integrated mill of 3 Mt a year,
  // $520 a tonne variable, $750m a year fixed, a 75% minimum rate, half the fixed costs while banked, and a restart
  // cost.  Tonnes beyond the order book sell 15% below the market.  If other mills run full, their extra supply
  // pushes the market price down by a third of a per cent for each per cent of extra supply.
  W.millglut = function (el) {
    QB.widget(el, {
      title: "A mill in a glut: run full, cut output, or bank the furnace?",
      sub: "You run a blast furnace. The price falls and orders dry up for a while, then recover. Choose how deep and how long the glut is, how many rival mills keep running full, and what a restart costs, and see what each strategy loses.",
      panels: 2, height: 300,
      controls: [
        { k: "bottom", label: "Lowest market price, $ a tonne", min: 450, max: 800, step: 10, value: 620, fmt: function (x) { return "$" + x; } },
        { k: "len", label: "Quarters at the bottom", min: 1, max: 10, step: 1, value: 2, fmt: function (x) { return x + (x === 1 ? " quarter" : " quarters"); } },
        { k: "push", label: "Share of rival mills that run full", min: 0, max: 1, step: 0.05, value: 0, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "restart", label: "Cost to restart a banked furnace, $m", min: 0, max: 200, step: 5, value: 60, fmt: function (x) { return "$" + x + "m"; } },
      ],
      draw: function (g, v, s) {
        var top = 880, path = [top, 800], i;
        var fall = [top - (top - v.bottom) * 0.45, top - (top - v.bottom) * 0.85];
        path = [top, 800, fall[0], fall[1]];
        for (i = 0; i < v.len; i++) path.push(v.bottom);
        path.push(v.bottom + (860 - v.bottom) * 0.25, v.bottom + (860 - v.bottom) * 0.6, 860);
        var n = path.length, orders = [], prices = [];
        for (i = 0; i < n; i++) {
          var o = Math.min(1, Math.max(0.55, 0.55 + 0.45 * (path[i] - v.bottom) / Math.max(1, top - v.bottom)));
          orders.push(o);
          prices.push(path[i] * Math.max(0.3, 1 - v.push * (1 - o) / o / 3));
        }
        var cap = 3.0 / 4, fixed = 750 / 4, vc = 520, minr = 0.75, idle = 0.5, disc = 0.15;
        function play(strat) {
          var out = [], cum = 0, banked = false;
          for (var q = 0; q < n; q++) {
            var p = prices[q], o = orders[q], rate = strat === "price" ? 1 : Math.max(o, minr), prof;
            if (strat === "bank" && o < minr) { prof = -fixed * idle; banked = true; }
            else {
              var rs = banked ? v.restart : 0; banked = false;
              var full = Math.min(o, rate) * cap, spot = Math.max(rate - o, 0) * cap;
              prof = full * p + spot * p * (1 - disc) - rate * cap * vc - fixed - rs;
            }
            cum += prof; out.push(cum);
          }
          return out;
        }
        var A = play("price"), B = play("output"), Cc = play("bank"), qs = [];
        for (i = 0; i < n; i++) qs.push(i + 1);
        var a = g[0].axes({ x: [1, n], y: [300, 950], title: "Market price, $ a tonne, and orders",
                            xticks: [1, Math.round(n / 2), n], xfmt: function (x) { return "Q" + x; }, yfmt: function (y) { return "$" + y; } });
        a.line(qs, prices, { color: C.p, width: 2.2 });
        a.line(qs, orders.map(function (o) { return 300 + 650 * o; }), { color: C.muted, width: 1.4, dash: [4, 4] });
        a.hline(770, { color: C.loss });
        a.legend([["price", C.p], ["orders (scaled)", C.muted], ["break-even at full output", C.loss]], { pos: "bl" });
        var all = A.concat(B, Cc), lo = Math.min.apply(null, all), hi = Math.max.apply(null, all);
        var b = g[1].axes({ x: [1, n], y: [Math.min(lo * 1.1, -50), Math.max(hi * 1.1, 50)], title: "Running total of profit, $ million",
                            xticks: [1, Math.round(n / 2), n], xfmt: function (x) { return "Q" + x; }, yfmt: function (y) { return Math.round(y); } });
        b.hline(0, { color: C.muted });
        b.line(qs, A, { color: C.gain, width: 2.2 });
        b.line(qs, B, { color: C.p, width: 2.2 });
        b.line(qs, Cc, { color: C.spot, width: 2.2, dash: [6, 3] });
        b.legend([["run full", C.gain], ["cut output", C.p], ["bank", C.spot]], { pos: "bl" });
        s.r = { a: A[n - 1], b: B[n - 1], c: Cc[n - 1], low: Math.min.apply(null, prices) };
      },
      readout: function (v, s) {
        var r = s.r, best = r.a >= r.b && r.a >= r.c ? "run full" : (r.c >= r.b ? "bank the furnace" : "cut output");
        function m(x) { return (x < 0 ? "-$" : "+$") + Math.abs(Math.round(x)) + "m"; }
        return [["lowest price after rivals' tonnes", "$" + Math.round(r.low)], ["run full", m(r.a)], ["cut output", m(r.b)],
                ["bank the furnace", m(r.c)], ["least bad", best]];
      },
      note: "This is the film's chapter 1 game. With a short, shallow glut, running full loses least: every tonne still sells for more than its ore and coke. Make the glut longer, or let your rivals run full so the price sinks further, and banking the furnace starts to win, unless restarting is very expensive. What is best for one mill makes the glut worse for all of them.",
    });
  };

  // Part 12: a steam cracker on ethane in Texas or naphtha in Europe (the Works' cracker.py, EIA's yields)
  W.cracker = function (el) {
    var Y = {
      ethane: { hydrogen: 0.0591, methane: 0.0704, ethylene: 0.8091, other: 0.0194 + 0.0178 + 0.0081 + 0.0081 + 0.0008 + 0.0073 },
      naphtha: { hydrogen: 0.0097, methane: 0.1694, ethylene: 0.3867,
                 other: 0.1547 + 0.0476 + 0.0507 + 0.0437 + 0.0166 + 0.0224 + 0.0735 + 0.0251 },
    };
    var HV = { hydrogen: 141.8 / 1.05506, methane: 55.5 / 1.05506, ethane: 51.9 / 1.05506 };
    var FEE = 60, BBL = 9, RATIO = 0.9, PREM = 1.1, ENERGY = { ethane: 17, naphtha: 25 }, OTHER = 150;
    function parts(feed, gas, brent) {
      var y = Y[feed], naph = brent * BBL * RATIO;
      var fp = feed === "ethane" ? gas * HV.ethane + FEE : naph;
      var cr = y.hydrogen * gas * HV.hydrogen + y.methane * gas * HV.methane + y.other * naph * PREM;
      var f = fp / y.ethylene, c = cr / y.ethylene, fu = ENERGY[feed] * gas;
      return { feed: f, credits: c, fuel: fu, other: OTHER, cost: f - c + fu + OTHER };
    }
    QB.widget(el, {
      title: "Where would you build a cracker?",
      sub: "A cracker turns ethane or naphtha into ethylene. Set the price of gas in America and in Europe, the price of oil, and how full the world's plants are, and see what a tonne of ethylene costs each plant, what the world price is, and who makes money.",
      panels: 2, height: 300,
      controls: [
        { k: "us", label: "American gas (Henry Hub), $ per million Btu", min: 1.5, max: 10, step: 0.1, value: 3.1, fmt: function (x) { return "$" + x.toFixed(1); } },
        { k: "eu", label: "European gas (TTF), $ per million Btu", min: 3, max: 40, step: 0.5, value: 17, fmt: function (x) { return "$" + x.toFixed(1); } },
        { k: "brent", label: "Brent crude, $ a barrel", min: 30, max: 130, step: 1, value: 69, fmt: function (x) { return "$" + x; } },
        { k: "cu", label: "How full the industry's plants are", min: 65, max: 92, step: 1, value: 75, fmt: function (x) { return x + "%"; } },
      ],
      draw: function (g, v, s) {
        var T = parts("ethane", v.us, v.brent), E = parts("naphtha", v.eu, v.brent);
        var markup = Math.max(0, (v.cu - 70) * 25), price = Math.max(T.cost, E.cost) + markup;
        var hi = Math.max(T.feed, E.feed, price) * 1.15;
        var a = g[0].axes({ x: [0, 11], y: [0, hi], title: "A tonne of ethylene, $: feed, less by-products, plus fuel and other costs",
                            xticks: [], yfmt: function (y) { return "$" + Math.round(y); } });
        function fall(x0, P, col) {
          var lvl = 0, steps = [[P.feed, col], [-P.credits, C.gain], [P.fuel, C.p], [P.other, C.q]];
          steps.forEach(function (st, i) {
            var lo = Math.min(lvl, lvl + st[0]), top = Math.max(lvl, lvl + st[0]);
            a.bars([x0 + i], [top], 0.8, { base: lo, color: st[1], alpha: st[0] < 0 ? 0.45 : 0.85 });
            lvl += st[0];
          });
          a.bars([x0 + 4], [P.cost], 0.8, { color: col, alpha: 0.95 });
          a.text(x0 + 4, P.cost, "$" + Math.round(P.cost), { dy: -10, align: "center", bold: true, color: col });
        }
        fall(0.6, T, C.p);
        fall(5.9, E, C.q);
        a.hline(price, { color: C.ink, dash: [6, 4] });
        a.text(10.9, price, "world price $" + Math.round(price), { dy: -10, align: "right", color: C.ink, bg: true });
        a.text(2.6, hi * 0.97, "Texas, ethane", { align: "center", color: C.p, bold: true });
        a.text(7.9, hi * 0.97, "Europe, naphtha", { align: "center", color: C.q, bold: true });
        var cashT = (price - T.cost) * 1.5 - 150, cashE = (price - E.cost) * 1.5 - 150;
        var lo2 = Math.min(cashT, cashE, 0) * 1.2 - 50, hi2 = Math.max(cashT, cashE, 0) * 1.2 + 50;
        var b = g[1].axes({ x: [0, 3], y: [lo2, hi2], title: "Cash a year, 1.5 Mt plant, after $150m of fixed costs, $m", xticks: [],
                            yfmt: function (y) { return Math.round(y); } });
        b.hline(0, { color: C.muted });
        b.bars([1], [cashT], 0.8, { color: cashT >= 0 ? C.p : C.loss });
        b.bars([2], [cashE], 0.8, { color: cashE >= 0 ? C.q : C.loss });
        b.text(1, cashT, Math.round(cashT) + "", { dy: cashT >= 0 ? -10 : 12, align: "center", bold: true });
        b.text(2, cashE, Math.round(cashE) + "", { dy: cashE >= 0 ? -10 : 12, align: "center", bold: true });
        b.text(1, lo2 + (hi2 - lo2) * 0.04, "Texas", { align: "center", color: C.p, base: "bottom" });
        b.text(2, lo2 + (hi2 - lo2) * 0.04, "Europe", { align: "center", color: C.q, base: "bottom" });
        s.r = { t: T.cost, e: E.cost, price: price, ct: cashT, ce: cashE, payback: cashT > 0 ? 6000 / cashT : Infinity };
      },
      readout: function (v, s) {
        var r = s.r;
        return [["Texas a tonne", "$" + Math.round(r.t)], ["Europe a tonne", "$" + Math.round(r.e)], ["world price", "$" + Math.round(r.price)],
                ["Texas pays back a $6bn plant in", isFinite(r.payback) ? r.payback.toFixed(1) + " years" : "never"]];
      },
      note: "This is the Works' cracker from the film (yields from the EIA; prices of ethane and naphtha tied to gas and Brent, and the fuel and other costs, are the series' assumptions). Ethane is priced like gas and naphtha like oil, so the gap between the plants is the gap between gas and oil. Cheap American gas and dear oil make Texas the winner; push American gas up towards $8 and oil down, and the advantage disappears, as it did before shale.",
    });
  };

  // Part 13: the merit order (the Works' power.py: an illustrative fleet; running costs from EIA's heat rates)
  W.meritorder = function (el) {
    QB.widget(el, {
      title: "The merit order: who runs, and who sets the price?",
      sub: "An illustrative Texas-sized fleet, lined up from the cheapest plant to run to the dearest. Set demand, the price of gas and how much wind and sun there is, and see which plant is on the margin, the price everyone is paid, and what each kind of plant earns on each MWh.",
      panels: 2, height: 300, weights: [2, 1],
      controls: [
        { k: "dem", label: "Demand, GW", min: 30, max: 110, step: 1, value: 70, fmt: function (x) { return x + " GW"; } },
        { k: "gas", label: "Natural gas, $ per million Btu", min: 1.5, max: 15, step: 0.25, value: 3.85, fmt: function (x) { return "$" + x.toFixed(2); } },
        { k: "sun", label: "Solar output right now, GW", min: 0, max: 60, step: 1, value: 15, fmt: function (x) { return x + " GW"; } },
        { k: "wind", label: "Wind output right now, GW", min: 0, max: 35, step: 1, value: 12, fmt: function (x) { return x + " GW"; } },
      ],
      draw: function (g, v, s) {
        var fleet = [
          { n: "solar", mw: v.sun, c: 0, col: C.p },
          { n: "wind", mw: v.wind, c: 0, col: C.spot },
          { n: "nuclear", mw: 5, c: 9.3, col: C.q },
          { n: "coal", mw: 12, c: 24, col: C.muted },
          { n: "combined-cycle gas", mw: 30, c: 6.2 * v.gas + 3.6, col: "#f2a65a" },
          { n: "older gas", mw: 9, c: 9.5 * v.gas + 4, col: "#c9732f" },
          { n: "gas peakers", mw: 6, c: 9.1 * v.gas + 4.2 + 20, col: C.loss },
          { n: "oil and others", mw: 2, c: 150, col: "#5d6b82" },
        ];
        fleet.sort(function (a, b) { return a.c - b.c; });
        var total = 0; fleet.forEach(function (u) { total += u.mw; });
        var left = v.dem, price = 0, x = 0, marg = "none";
        fleet.forEach(function (u) { u.x0 = x; x += u.mw; if (left > 0 && u.mw > 0) { price = u.c; marg = u.n; left -= u.mw; } });
        var short = left > 0;
        if (short) { price = 5000; marg = "nobody: demand exceeds supply"; }
        var top = Math.min(Math.max(price, 60) * 1.25, 200);
        var a = g[0].axes({ x: [0, Math.max(total, v.dem) * 1.05], y: [0, top], title: "Plants, cheapest to run first: running cost, $ a MWh",
                            xfmt: function (x) { return Math.round(x) + " GW"; }, yfmt: function (y) { return "$" + Math.round(y); } });
        fleet.forEach(function (u) {
          if (u.mw <= 0) return;
          a.bars([u.x0 + u.mw / 2], [Math.max(Math.min(u.c, top), top * 0.01)], u.mw, { color: u.col, alpha: u.x0 < v.dem ? 0.9 : 0.35, gap: 2 });
        });
        a.vline(v.dem, { color: C.ink, dash: [6, 4], width: 2 });
        a.hline(Math.min(price, top), { color: C.p, dash: [4, 4] });
        a.text(v.dem, top * 0.95, "demand", { align: "left", dx: 6, color: C.ink, bg: true });
        var run = fleet.filter(function (u) { return u.x0 < v.dem && u.mw > 0; });
        var b = g[1].axes({ x: [0, run.length + 1], y: [0, Math.max(price, 60) * 1.1], title: "Earned on each MWh above running cost",
                            xticks: [], yfmt: function (y) { return "$" + Math.round(y); } });
        run.forEach(function (u, i) {
          var rent = Math.max(price - u.c, 0);
          b.bars([i + 1], [Math.max(rent, 0.5)], 0.7, { color: u.col });
          b.text(i + 1, Math.max(rent, 0.5), "$" + Math.round(rent), { dy: -9, align: "center", size: 10.5 });
        });
        s.r = { price: price, marg: marg, short: short, run: run.length };
      },
      readout: function (v, s) {
        var r = s.r;
        return [["price", r.short ? "the cap, $5,000" : "$" + r.price.toFixed(0) + " a MWh"], ["on the margin", r.marg]];
      },
      note: "This is the merit order of the film's chapter 4, with an illustrative fleet. Every plant left of the demand line runs and is paid the running cost of the last one needed; the difference is what pays back its building cost. Raise the price of gas and the price of power follows, because gas is so often on the margin. Add solar and the midday price can fall to nothing. Push demand past the whole fleet and no plant sets the price: it goes to the cap (here $5,000), and some customers go without.",
    });
  };
  W.landfill = function (el) {
    function play(plan, rivalYear, ceiling, airspace) {
      var cost = 25, region = 1.5, nb = 1.0, rivalFee = 45, rate = 0.07, exp = 15, expCost = 15, expYear = 8;
      var left = airspace, pv = plan === "expand" ? -expCost : 0, lefts = [airspace], full = null;
      for (var t = 1; t <= 60; t++) {
        if (plan === "expand" && t === expYear) left += exp;
        var fee, tons;
        if (left <= 1e-9) { lefts.push(0); continue; }
        if (t > rivalYear) { fee = rivalFee; tons = (region + nb) / 2; }
        else if (plan === "fill") { fee = rivalFee; tons = region + nb; }
        else { fee = ceiling; tons = region; }
        tons = Math.min(tons, left); left -= tons;
        pv += (fee - cost) * tons / Math.pow(1 + rate, t);
        lefts.push(left);
        if (left <= 1e-9 && full === null) full = t;
      }
      return { pv: pv, lefts: lefts, full: full, perTon: pv / (airspace + (plan === "expand" ? exp : 0)) };
    }
    var PLANS = [["fill", "Fill it fast", C.q], ["ceiling", "Charge the ceiling", C.p], ["expand", "Ceiling, and expand", "#b58cff"]];
    QB.widget(el, {
      title: "The last landfill in the valley: what is a hole in the ground worth?",
      sub: "The Works' valley landfill from the film's Run it chapter. Charge the rivals' fee and take everyone's rubbish, charge what the valley will bear, or charge that and apply to expand. Set how long a rival needs for its permit, what hauling rubbish out of the valley would cost, and how much room is left.",
      panels: 2, height: 300, weights: [3, 2],
      controls: [
        { k: "rival", label: "Years until the rival's permit", min: 0, max: 25, step: 1, value: 15, fmt: function (x) { return x + " years"; } },
        { k: "ceil", label: "The valley's ceiling: next landfill plus the haul, $ a ton", min: 45, max: 90, step: 1, value: 65, fmt: function (x) { return "$" + x; } },
        { k: "air", label: "Airspace left, million tons", min: 10, max: 60, step: 1, value: 30, fmt: function (x) { return x + "m tons"; } },
      ],
      draw: function (g, v, s) {
        var res = PLANS.map(function (p) { return play(p[0], v.rival, v.ceil, v.air); });
        var yrs = []; for (var t = 0; t <= 45; t++) yrs.push(t);
        var a = g[0].axes({ x: [0, 45], y: [0, v.air + 16], title: "Airspace left, million tons",
                            xticks: [0, 10, 20, 30, 40], xfmt: function (x) { return "yr " + x; }, yfmt: function (y) { return Math.round(y) + "m"; } });
        res.forEach(function (r, i) { a.line(yrs, yrs.map(function (t) { return r.lefts[t]; }), { color: PLANS[i][2], width: 2.4 }); });
        a.vline(v.rival, { color: C.loss, dash: [5, 4], width: 1.6 });
        a.text(v.rival, v.air + 12, "rival opens", { align: "left", dx: 5, color: C.loss, bg: true });
        var top = Math.max.apply(null, res.map(function (r) { return r.pv; })) * 1.2;
        var b = g[1].axes({ x: [0, 4], y: [0, top], title: "Value today, $m (7% a year)", xticks: [], yfmt: function (y) { return "$" + Math.round(y); } });
        res.forEach(function (r, i) {
          b.bars([i + 1], [Math.max(r.pv, 0.5)], 0.7, { color: PLANS[i][2] });
          b.text(i + 1, Math.max(r.pv, 0.5), "$" + Math.round(r.pv) + "m", { dy: -9, align: "center", size: 10.5 });
        });
        var best = 0; res.forEach(function (r, i) { if (r.pv > res[best].pv) best = i; });
        s.r = { res: res, best: best };
      },
      readout: function (v, s) {
        var r = s.r, b = r.res[r.best];
        return [["worth most", PLANS[r.best][1] + ": $" + Math.round(b.pv) + "m"],
                ["a ton of airspace", "$" + b.perTon.toFixed(2)],
                ["full in", b.full === null ? "not within 60 years" : "year " + b.full]];
      },
      note: "This is the film's Run it, with the Works' numbers: $25 a ton to run, 1.5 million tons a year from the valley, 1 million more from the neighbours at the rivals' $45, and an expansion that costs $15m now and adds 15 million tons in year 8. Once the rival opens, both charge $45 and split the rubbish. With a long permit, patience pays: every ton you fill cheaply now is a ton you cannot sell at the ceiling later. Shorten the permit and the ceiling is worth little. The asset is not the hole; it is the time it takes anyone else to get permission to dig one.",
    });
  };

})();
