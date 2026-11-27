// Interactives for Act III, Making (Parts 15-21).
(function () {
  "use strict";
  var C = QB.C, W = QB.W;

  // ---- Part 15: build a fab or book a foundry --------------------------------------------------------------------
  // The film's model (explainer/industry/works/fab.py): gross dies on a 300 mm wafer, Poisson yield exp(-A D), a fab
  // that costs capex/life + fixed a year plus a variable cost per wafer, and a new process whose defect density falls
  // from 0.5 towards 0.1 per cm2, halving the gap every 150,000 wafers.  The foundry charges a price per wafer on its
  // mature process.  Run it: at 5,000 wafers a month the foundry earns $1.07bn a year against -$3.46bn for the fab;
  // owning first pays at about 32,000.
  W.fab = function (el) {
    function dpw(a) { return Math.PI * 150 * 150 / a - Math.PI * 300 / Math.sqrt(2 * a); }
    function good(a, d) { return dpw(a) * Math.exp(-a / 100 * d); }
    function learning(d0, d1, w, half) { return d1 + (d0 - d1) * Math.pow(0.5, w / half); }
    function plan(vol, own, p) {
      var g, costWafer;
      if (own) {
        var wafers = vol * 12 * 5, steps = 60, sum = 0;
        for (var k = 0; k < steps; k++) sum += good(p.die, learning(0.5, 0.1, wafers * (k + 0.5) / steps, 150000));
        g = sum / steps;
        var yearCost = p.capex / 5 + 1.0 + 2500 * vol * 12 / 1e9;
        costWafer = yearCost * 1e9 / (vol * 12);
      } else {
        g = good(p.die, 0.1);
        costWafer = p.price;
      }
      var costDie = costWafer / g;
      return { good: g, costWafer: costWafer, costDie: costDie, profit: (p.chipPrice - costDie) * g * vol * 12 / 1e9 };
    }
    QB.widget(el, {
      title: "Build a fab, or book a foundry?",
      sub: "The Works' chip designer from the film's Run it chapter. It needs a number of 12-inch wafers a month for five years. It can build its own fab, which costs the same whether it is full or empty and starts on a new process with many defects, or it can pay a foundry by the wafer and use the foundry's mature process. Set the volume, the fab's cost, the foundry's price and the size of the chip.",
      panels: 2, height: 300, weights: [3, 2],
      controls: [
        { k: "vol", label: "Wafers a month the designer needs", min: 2000, max: 50000, step: 1000, value: 20000, fmt: function (x) { return (x / 1000).toFixed(0) + "k"; } },
        { k: "capex", label: "Cost of building the fab, $ billion", min: 5, max: 40, step: 1, value: 20, fmt: function (x) { return "$" + x + "bn"; } },
        { k: "price", label: "Foundry's price per wafer", min: 8000, max: 30000, step: 500, value: 17000, fmt: function (x) { return "$" + (x / 1000).toFixed(1) + "k"; } },
        { k: "die", label: "Size of the chip, mm²", min: 50, max: 600, step: 10, value: 100, fmt: function (x) { return x + " mm²"; } },
      ],
      draw: function (g, v, s) {
        var p = { capex: v.capex, price: v.price, die: v.die, chipPrice: 60 * v.die / 100 };
        var vols = [], fo = [], ow = [], even = null;
        for (var x = 2000; x <= 50000; x += 1000) {
          var a = plan(x, false, p).profit, b = plan(x, true, p).profit;
          vols.push(x / 1000); fo.push(a); ow.push(b);
          if (even === null && b > a) even = x;
        }
        var lo = Math.min(0, Math.min.apply(null, ow)), hi = Math.max(Math.max.apply(null, fo), Math.max.apply(null, ow));
        var ax = g[0].axes({ x: [2, 50], y: [Math.max(lo, -15), hi * 1.1 + 0.5], title: "Profit a year, $bn, by wafers a month",
                             xticks: [10, 20, 30, 40, 50], xfmt: function (x) { return x + "k"; }, yfmt: function (y) { return "$" + y.toFixed(0) + "bn"; } });
        ax.line(vols, fo, { color: C.q, width: 2.4 });
        ax.line(vols, ow, { color: C.p, width: 2.4 });
        ax.line([2, 50], [0, 0], { color: C.muted, width: 1, dash: [3, 3] });
        ax.vline(v.vol / 1000, { color: C.spot, dash: [5, 4], width: 1.4 });
        if (even !== null) ax.text(even / 1000, hi * 1.05, "owning pays from " + (even / 1000).toFixed(0) + "k", { align: "left", dx: 5, color: C.p, bg: true });
        ax.legend([["book the foundry", C.q], ["build the fab", C.p]], { pos: "tl" });
        var f = plan(v.vol, false, p), o = plan(v.vol, true, p);
        var top = Math.max(f.costDie, Math.min(o.costDie, f.costDie * 6)) * 1.25;
        var b2 = g[1].axes({ x: [0, 3], y: [0, top], title: "Cost of one good chip", xticks: [], yfmt: function (y) { return "$" + Math.round(y); } });
        b2.bars([1], [f.costDie], 0.7, { color: C.q });
        b2.bars([2], [Math.min(o.costDie, top)], 0.7, { color: C.p });
        b2.text(1, f.costDie, "$" + f.costDie.toFixed(0), { dy: -9, align: "center", size: 10.5 });
        b2.text(2, Math.min(o.costDie, top), "$" + o.costDie.toFixed(0), { dy: -9, align: "center", size: 10.5 });
        b2.text(1, 0, "foundry", { dy: 12, align: "center", size: 10 });
        b2.text(2, 0, "own fab", { dy: 12, align: "center", size: 10 });
        s.r = { f: f, o: o, even: even, util: v.vol / 50000 };
      },
      readout: function (v, s) {
        var r = s.r, better = r.o.profit > r.f.profit ? "build the fab" : "book the foundry";
        return [["better choice", better + " (" + (Math.max(r.o.profit, r.f.profit) >= 0 ? "$" : "-$") + Math.abs(Math.max(r.o.profit, r.f.profit)).toFixed(2) + "bn a year)"],
                ["the fab would be", Math.round(100 * r.util) + "% full"],
                ["owning first pays at", r.even === null ? "never, up to 50k a month" : (r.even / 1000).toFixed(0) + "k wafers a month"]];
      },
      note: "The Works' numbers, as in the film: the fab holds 50,000 wafers a month, its tools are written off over five years, it costs $1bn a year to staff and maintain and $2,500 a wafer in materials and power; chips sell for $60 per 100 mm² of silicon. A small designer cannot fill a fab, so every wafer carries a large share of a factory that sits idle, and a new process yields badly at first. The foundry fills its fabs with hundreds of customers and has already climbed the learning curve. Make the fab dearer and the break-even moves out of reach for all but the biggest buyers: that is why most designers no longer own fabs.",
    });
  };


  // ---- Part 16: the order that needs a plant -----------------------------------------------------------------------
  // The film's model (explainer/industry/works/device.py): a brand offers 20 million devices a year for three years at a
  // fee per device, if a new plant ($800m) is ready in a year.  Each device costs $9 of labour and $3 of other costs; the
  // plant costs $60m a year.  The first year runs at half speed.  After three years the brand renews for three more with
  // probability p.  A plant in a new country has half the labour cost, costs 10% more and ramps 30%, 70%, 100%.
  // Run it: building is worth -$194m if not renewed and +$420m if renewed (break-even p about 32%).
  W.assembler = function (el) {
    function flows(plan, v) {
      var labour = 9, other = 3, fixed = 60, plant = v.plant, ramp = [0.5, 1, 1];
      if (plan === "abroad") { labour = 4.5; plant = v.plant * 1.1; ramp = [0.3, 0.7, 1]; }
      var out = [-plant];
      for (var t = 0; t < 6; t++) out.push((t < 3 ? ramp[t] : 1) * v.units * (v.fee - labour - other) - fixed);
      return out;
    }
    function parts(plan, v) {
      var f = flows(plan, v), first = 0, rest = 0;
      for (var t = 0; t < f.length; t++) { var d = f[t] / Math.pow(1.08, t); if (t <= 3) first += d; else rest += d; }
      return [first, rest];
    }
    function value(plan, v, p) {
      if (plan === "decline") return 0;
      var fr = parts(plan, v);
      return fr[0] + p * fr[1];
    }
    QB.widget(el, {
      title: "The order that needs a plant",
      sub: "You run an assembler. A brand offers you millions of devices a year for three years at a fee per device, if you build a new plant within a year. After three years it may renew, or move the work elsewhere. Set the fee, the size of the order, the plant's cost and your guess of the chance it renews.",
      panels: 2, height: 300, weights: [3, 2],
      controls: [
        { k: "p", label: "Chance the brand renews", min: 0, max: 1, step: 0.05, value: 0.5, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "fee", label: "Fee per device, $", min: 15, max: 45, step: 1, value: 30, fmt: function (x) { return "$" + x; } },
        { k: "units", label: "Devices a year, million", min: 5, max: 40, step: 1, value: 20, fmt: function (x) { return x + "m"; } },
        { k: "plant", label: "Cost of the plant, $m", min: 200, max: 1600, step: 50, value: 800, fmt: function (x) { return "$" + x + "m"; } },
      ],
      draw: function (g, v, s) {
        var ps = [], b = [], a = [], d = [], i, even = null;
        for (i = 0; i <= 20; i++) {
          var p = i / 20; ps.push(100 * p);
          b.push(value("build", v, p)); a.push(value("abroad", v, p)); d.push(0);
        }
        var fr = parts("build", v);
        even = fr[0] >= 0 ? 0 : (fr[1] > 0 && -fr[0] / fr[1] <= 1 ? -fr[0] / fr[1] : null);
        var lo = Math.min(Math.min.apply(null, b), Math.min.apply(null, a), 0), hi = Math.max(Math.max.apply(null, b), Math.max.apply(null, a), 50);
        var ax = g[0].axes({ x: [0, 100], y: [lo * 1.1, hi * 1.15], title: "Value of the plan today, $m, by chance of renewal",
                             xticks: [0, 25, 50, 75, 100], xfmt: function (x) { return x + "%"; }, yfmt: function (y) { return "$" + Math.round(y); } });
        ax.line(ps, d, { color: C.muted, width: 1.4, dash: [4, 4] });
        ax.line(ps, b, { color: C.p, width: 2.4 });
        ax.line(ps, a, { color: "#b58cff", width: 2.4 });
        ax.vline(100 * v.p, { color: C.spot, dash: [5, 4], width: 1.4 });
        ax.legend([["build here", C.p], ["build in a new country", "#b58cff"], ["decline", C.muted]], { pos: "tl" });
        var f = flows("build", v);
        var top = Math.max.apply(null, f.map(Math.abs)) * 1.2;
        var bx = g[1].axes({ x: [-0.7, 6.7], y: [-top, top], title: "Building here: cash each year, $m", xticks: [0, 1, 2, 3, 4, 5, 6],
                             xfmt: function (x) { return "yr " + x; }, yfmt: function (y) { return "$" + Math.round(y); } });
        for (i = 0; i < f.length; i++) bx.bars([i], [f[i]], 0.6, { color: f[i] < 0 ? C.loss : (i > 3 ? "#7a5a30" : C.p) });
        s.r = { build: value("build", v, v.p), abroad: value("abroad", v, v.p), even: even, margin: (v.fee - 12 - 60 / v.units) / (450 + v.fee) };
      },
      readout: function (v, s) {
        var r = s.r, best = r.build >= Math.max(r.abroad, 0) ? "build here" : (r.abroad > 0 ? "build in a new country" : "decline");
        return [["best plan", best + " ($" + Math.round(Math.max(r.build, r.abroad, 0)) + "m)"],
                ["building pays above", r.even === null ? "never" : Math.round(100 * r.even) + "% chance of renewal"],
                ["margin on turnkey revenue", (100 * r.margin).toFixed(1) + "%"]];
      },
      note: "The Works' numbers, as in the film: $9 of labour and $3 of other costs a device, $60m a year to run the plant, 8% a year to discount, and a first year at half speed. The margin shown counts revenue as the assembler books it when it buys the $450 of parts and resells them: that is why a business earning good money on its own work reports a margin of a few per cent. Lower the chance of renewal and the plant becomes a bet the assembler loses; that is the brand's power, and why assemblers ask brands to pay for tooling.",
    });
  };

  W.carmaker = function (el) {
    var LIST = 45000, VAR = 36000, CAP = 125000, SHIFT = 288e6, FIXED = 900e6, PLAN = 220000;
    function demand(v, mine, theirs) {
      return PLAN * v.state * Math.pow(mine / LIST, -v.own) * Math.pow(theirs / LIST, v.cross);
    }
    function profit(v, me, them, shifts) {
      var pm = LIST - (me === "discount" ? v.disc : 0), pt = LIST - (them === "discount" ? v.disc : 0);
      var cars = Math.min(demand(v, pm, pt), (shifts || 2) * CAP);
      return (cars * (pm - VAR) - (shifts || 2) * SHIFT - FIXED) / 1e6;
    }
    function table(v) {
      var t = {};
      ["hold", "discount"].forEach(function (a) { ["hold", "discount"].forEach(function (b) { t[a + "|" + b] = profit(v, a, b); }); });
      return t;
    }
    QB.widget(el, {
      title: "The showroom duel",
      sub: "Your plant and a rival's are identical: two shifts, 250,000 cars a year, a $45,000 list price and $36,000 of parts and materials in each car. The orders have come in below plan. Each of you either holds the price or pays a discount. Set the discount, how willing buyers are to switch between the two models, and how weak demand is.",
      panels: 2, height: 300, weights: [3, 2],
      controls: [
        { k: "disc", label: "Discount per car, $", min: 500, max: 6000, step: 250, value: 3000, fmt: function (x) { return "$" + x.toLocaleString(); } },
        { k: "own", label: "Own-price elasticity (how much a price cut wins)", min: 3, max: 10, step: 0.5, value: 7, fmt: function (x) { return x.toFixed(1); } },
        { k: "cross", label: "Cross-price elasticity (how much comes from the rival)", min: 1, max: 9, step: 0.5, value: 6, fmt: function (x) { return x.toFixed(1); } },
        { k: "state", label: "Demand against plan", min: 0.5, max: 1.3, step: 0.05, value: 0.7, fmt: function (x) { return Math.round(100 * x) + "%"; } },
      ],
      draw: function (g, v, s) {
        if (v.cross >= v.own) v.cross = v.own - 0.5;
        var xs = [], hold = [], disc = [], i;
        for (i = 0; i <= 24; i++) {
          var d = 250 * i; xs.push(d);
          var w = { disc: d, own: v.own, cross: v.cross, state: v.state };
          hold.push(profit(w, "discount", "hold") - profit(w, "hold", "hold"));
          disc.push(profit(w, "discount", "discount") - profit(w, "hold", "discount"));
        }
        var lo = Math.min(Math.min.apply(null, hold), Math.min.apply(null, disc), 0), hi = Math.max(Math.max.apply(null, hold), Math.max.apply(null, disc), 10);
        var ax = g[0].axes({ x: [0, 6000], y: [lo * 1.1, hi * 1.15], title: "What discounting adds to your profit, $m, by size of discount",
                             xticks: [0, 2000, 4000, 6000], xfmt: function (x) { return "$" + x / 1000 + "k"; }, yfmt: function (y) { return Math.round(y); } });
        ax.line([0, 6000], [0, 0], { color: C.muted, width: 1.2, dash: [4, 4] });
        ax.line(xs, hold, { color: C.p, width: 2.4 });
        ax.line(xs, disc, { color: "#f2a65a", width: 2.4 });
        ax.vline(v.disc, { color: C.spot, dash: [5, 4], width: 1.4 });
        ax.legend([["if the rival holds", C.p], ["if the rival discounts", "#f2a65a"]], { pos: "tl" });
        var t = table(v);
        var keys = ["hold|hold", "discount|hold", "hold|discount", "discount|discount"], vals = keys.map(function (k) { return t[k]; });
        var top = Math.max.apply(null, vals.map(Math.abs)) * 1.2;
        var bx = g[1].axes({ x: [-0.7, 3.7], y: [-top, top], title: "Your profit, $m: you / rival",
                             xticks: [0, 1, 2, 3], xfmt: function (x) { return ["H/H", "D/H", "H/D", "D/D"][x]; }, yfmt: function (y) { return Math.round(y); } });
        for (i = 0; i < 4; i++) bx.bars([i], [vals[i]], 0.6, { color: vals[i] < 0 ? C.loss : C.p });
        var eq = [];
        ["hold", "discount"].forEach(function (a) { ["hold", "discount"].forEach(function (b) {
          var other = a === "hold" ? "discount" : "hold", otherb = b === "hold" ? "discount" : "hold";
          if (t[a + "|" + b] >= t[other + "|" + b] && t[b + "|" + a] >= t[otherb + "|" + a]) eq.push(a + "/" + b);
        }); });
        s.r = { t: t, eq: eq, cut: (Math.min(PLAN * v.state, CAP) * (LIST - VAR) - SHIFT - FIXED) / 1e6 };
      },
      readout: function (v, s) {
        var r = s.r, t = r.t;
        var pd = t["discount|hold"] > t["hold|hold"] && t["discount|discount"] > t["hold|discount"] && t["hold|hold"] > t["discount|discount"];
        return [["equilibrium (you/rival)", r.eq.length ? r.eq.join(", ") : "none in pure moves"],
                ["both hold / both discount", "$" + Math.round(t["hold|hold"]) + "m / $" + Math.round(t["discount|discount"]) + "m each"],
                ["a prisoner's dilemma?", pd ? "yes: each discounts, both lose" : "no"],
                ["both cut a shift and hold", "$" + Math.round(r.cut) + "m each"]];
      },
      note: "The Works' plant, as in the film: each shift costs $288m a year whether busy or not, and tooling, engineering and overhead another $900m. A car's demand is the plan times the demand you set, times (your price / $45,000) to the minus own elasticity, times (the rival's price / $45,000) to the cross elasticity: when own is much bigger than cross, a discount mostly takes buyers from the rival. With the film's numbers, discounting is the better reply whatever the rival does, and both end far worse off than if both had held. Make buyers less willing to switch, or the discount bigger, and the dilemma goes away.",
    });
  };

  // Part 19: the tender (the Works' Tender in explainer/industry/works/machine.py)
  W.tender = function (el) {
    var FLEET = 100, COST = 1.0;
    function value(v, price) { return price - COST + v.service * v.attach; }
    function payoff(v, me, them) {
      var p = { hold: v.hold, cut: v.cut };
      var share = p[me] < p[them] ? 1 : (p[me] > p[them] ? 0 : 0.5);
      return share * FLEET * value(v, p[me]);
    }
    function table(v) {
      var t = {};
      ["hold", "cut"].forEach(function (a) { ["hold", "cut"].forEach(function (b) { t[a + "|" + b] = payoff(v, a, b); }); });
      return t;
    }
    QB.widget(el, {
      title: "The tender",
      sub: "You and a rival bid for a customer's fleet of 100 machines that cost $1.0m each to build. Each of you bids high or cuts; the lower bid wins the whole fleet and a tie splits it. Whoever sells the machines also sells their parts and service, on the share of owners who stay with the maker: the attach rate. Set the bids, the value of the servicing and the attach rate.",
      panels: 2, height: 300, weights: [3, 2],
      controls: [
        { k: "hold", label: "The high bid, $m a machine", min: 1.0, max: 2.0, step: 0.05, value: 1.3, fmt: function (x) { return "$" + x.toFixed(2) + "m"; } },
        { k: "cut", label: "The low bid, $m a machine", min: 0.5, max: 1.2, step: 0.05, value: 0.9, fmt: function (x) { return "$" + x.toFixed(2) + "m"; } },
        { k: "service", label: "Value of a machine's servicing today, $m", min: 0, max: 1.5, step: 0.05, value: 0.6, fmt: function (x) { return "$" + x.toFixed(2) + "m"; } },
        { k: "attach", label: "Attach rate (owners who buy service from the maker)", min: 0, max: 1, step: 0.05, value: 1.0, fmt: function (x) { return Math.round(100 * x) + "%"; } },
      ],
      draw: function (g, v, s) {
        if (v.cut >= v.hold) v.cut = v.hold - 0.05;
        var xs = [], gain = [], i;
        for (i = 0; i <= 20; i++) {
          var a = i / 20; xs.push(a);
          var w = { hold: v.hold, cut: v.cut, service: v.service, attach: a };
          gain.push(payoff(w, "cut", "hold") - payoff(w, "hold", "hold"));
        }
        var lo = Math.min(Math.min.apply(null, gain), -5), hi = Math.max(Math.max.apply(null, gain), 5);
        var ax = g[0].axes({ x: [0, 1], y: [lo * 1.1, hi * 1.15], title: "What cutting adds against a rival who holds, $m, by attach rate",
                             xticks: [0, 0.25, 0.5, 0.75, 1], xfmt: function (x) { return Math.round(100 * x) + "%"; }, yfmt: function (y) { return Math.round(y); } });
        ax.hline(0, { color: C.muted });
        ax.line(xs, gain, { color: C.p, width: 2.4 });
        ax.vline(v.attach, { color: C.spot, dash: [5, 4], width: 1.4 });
        var t = table(v);
        var keys = ["hold|hold", "cut|hold", "hold|cut", "cut|cut"], vals = keys.map(function (k) { return t[k]; });
        var top = Math.max.apply(null, vals.map(Math.abs).concat([1])) * 1.2;
        var bx = g[1].axes({ x: [-0.7, 3.7], y: [-top, top], title: "Your value, $m: you / rival",
                             xticks: [0, 1, 2, 3], xfmt: function (x) { return ["H/H", "C/H", "H/C", "C/C"][x]; }, yfmt: function (y) { return Math.round(y); } });
        for (i = 0; i < 4; i++) bx.bars([i], [vals[i]], 0.6, { color: vals[i] < 0 ? C.loss : C.p });
        var eq = [];
        ["hold", "cut"].forEach(function (a) { ["hold", "cut"].forEach(function (b) {
          var oa = a === "hold" ? "cut" : "hold", ob = b === "hold" ? "cut" : "hold";
          if (t[a + "|" + b] >= t[oa + "|" + b] && t[b + "|" + a] >= t[ob + "|" + a]) eq.push(a + "/" + b);
        }); });
        var thr = ((v.hold - COST) / 2 - (v.cut - COST)) / (v.service / 2 || 1e-9);
        s.r = { t: t, eq: eq, thr: thr };
      },
      readout: function (v, s) {
        var r = s.r, t = r.t;
        return [["equilibrium (you/rival)", r.eq.length ? r.eq.join(", ") : "none in pure moves"],
                ["both hold / both cut", "$" + Math.round(t["hold|hold"]) + "m / $" + Math.round(t["cut|cut"]) + "m each"],
                ["cutting beats holding against a holder above", v.service > 0 ? (r.thr > 1 ? "never (above 100%)" : Math.max(0, Math.round(100 * r.thr)) + "% attach") : "never"],
                ["the floor price (cost less servicing)", "$" + (COST - v.service * v.attach).toFixed(2) + "m"]];
      },
      note: "The Works' tender, as in the film: with bids of $1.3m and $0.9m, servicing worth $0.6m a machine and every owner staying with the maker, cutting is the better reply whatever the rival does, so both cut and each is worth $25m instead of $45m. Lower the attach rate, as when independent workshops take the servicing, and holding the price starts to pay. Otis, which keeps most of the maintenance of the lifts it installs, earned 4.8 cents on a dollar of new equipment and 25.1 on a dollar of service in 2025.",
    });
  };

  // Part 18: build an airliner programme (the Works' Programme in explainer/industry/works/aircraft.py)
  W.airframer = function (el) {
    var FIRST = 450, DEV_YEARS = 6, RAMP = [0.15, 0.4, 0.7, 1.0], YEARS = 25, R = 0.08;
    function unit(n, learn) { return FIRST * Math.pow(n, Math.log(learn) / Math.LN2); }
    function run(v) {
      var cum = 0, built = 0, npv = 0, out = [], be = null, trough = 0, t, k;
      for (t = 0; t < DEV_YEARS; t++) {
        cum -= v.dev / DEV_YEARS; npv -= v.dev / DEV_YEARS / Math.pow(1 + R, t);
        out.push(cum); trough = Math.min(trough, cum);
      }
      for (k = 0; k < YEARS; k++) {
        var n = Math.round(v.rate * (k < RAMP.length ? RAMP[k] : 1)), cost = 0, i;
        for (i = 1; i <= n; i++) cost += unit(built + i, v.learn);
        built += n;
        var cash = (n * v.price - cost) / 1000;
        cum += cash; npv += cash / Math.pow(1 + R, DEV_YEARS + k);
        out.push(cum); trough = Math.min(trough, cum);
        if (be === null && cum >= 0) be = { year: DEV_YEARS + k, units: built };
      }
      var cross = Math.pow(FIRST / v.price, 1 / (-Math.log(v.learn) / Math.LN2));
      return { cum: out, npv: npv, be: be, trough: trough, cross: cross, built: built };
    }
    QB.widget(el, {
      title: "Build an airliner programme",
      sub: "The first aircraft off your new line costs $450m to build. Each time the number built doubles, the next one costs a fixed share of what it did: the learning rate. You spend the development cost over six years before the first delivery, then ramp up to your production rate and sell for 25 years. Set the price, the learning rate, the development cost and the rate.",
      panels: 2, height: 300, weights: [1, 1],
      controls: [
        { k: "price", label: "Price per aircraft, $m", min: 60, max: 160, step: 5, value: 110, fmt: function (x) { return "$" + x + "m"; } },
        { k: "learn", label: "Learning rate (cost after each doubling)", min: 0.75, max: 0.95, step: 0.01, value: 0.82, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "dev", label: "Development cost, $bn", min: 5, max: 40, step: 1, value: 20, fmt: function (x) { return "$" + x + "bn"; } },
        { k: "rate", label: "Production rate, aircraft a year", min: 40, max: 400, step: 10, value: 120, fmt: function (x) { return x + " a year"; } },
      ],
      draw: function (g, v, s) {
        var r = run(v), xs = [], ys = [], i;
        for (i = 0; i <= 60; i++) { var lx = i * 3.5 / 60; xs.push(lx); ys.push(unit(Math.pow(10, lx), v.learn)); }
        var ax = g[0].axes({ x: [0, 3.5], y: [0, 480], title: "Cost to build the n-th aircraft, $m (log scale of n)",
                             xticks: [0, 1, 2, 3], xfmt: function (x) { return Math.round(Math.pow(10, x)).toLocaleString(); },
                             yfmt: function (y) { return "$" + Math.round(y); } });
        ax.line(xs, ys, { color: "#b58cff", width: 2.4 });
        ax.hline(v.price, { color: "#f6c453", width: 1.6 });
        if (r.cross <= 3000) ax.dots([Math.log(r.cross) / Math.LN10], [v.price], { color: C.p, r: 5 });
        ax.legend([["cost of the n-th", "#b58cff"], ["price", "#f6c453"]], { pos: "tr" });
        var yr = [], lo = Math.min.apply(null, r.cum), hi = Math.max.apply(null, r.cum);
        for (i = 0; i < r.cum.length; i++) yr.push(i);
        var bx = g[1].axes({ x: [0, r.cum.length - 1], y: [Math.min(lo * 1.1, -5), Math.max(hi * 1.1, 5)],
                             title: "Cumulative cash, $bn, by year", xticks: [0, 6, 15, 30], xfmt: function (x) { return "yr " + x; },
                             yfmt: function (y) { return Math.round(y); } });
        bx.hline(0, { color: C.muted });
        bx.line(yr, r.cum, { color: r.npv >= 0 ? C.p : C.loss, width: 2.4 });
        if (r.be) bx.dots([r.be.year], [r.cum[r.be.year]], { color: C.p, r: 5 });
        s.r = r;
      },
      readout: function (v, s) {
        var r = s.r;
        return [["each aircraft costs less than its price", r.cross <= 1e6 ? "from the " + Math.round(r.cross).toLocaleString() + "th" : "never"],
                ["the deepest point of the valley", "$" + r.trough.toFixed(1) + "bn"],
                ["cash back to zero", r.be ? "year " + r.be.year + ", after " + r.be.units.toLocaleString() + " aircraft" : "not within 31 years"],
                ["value today at 8%", "$" + r.npv.toFixed(1) + "bn"]];
      },
      note: "The Works' programme, as in the film: with a $110m price, 82% learning, $20bn of development and 120 aircraft a year, the 137th aircraft is the first to cost less than its price, the cash bottoms out near -$26bn, comes back to zero in year 15 after 990 aircraft, and the programme is worth about $9bn today. Slow the learning to 90% and it never pays back. Cut the price by a quarter, as an incumbent far down its own curve could, and see what is left for a newcomer.",
    });
  };

})();
