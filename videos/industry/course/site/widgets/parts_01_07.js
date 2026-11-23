// Interactives for Act I, Reading an Industry (Parts 1-7).
(function () {
  "use strict";
  var C = QB.C, W = QB.W;

  // ---- Part 1: split the price of one phone ------------------------------------------------------------------
  // The film's model (explainer/industry/works/chain.py): the shop keeps a margin on the 60% of sales that go
  // through carriers and resellers; Apple pays for the parts, assembly ($30) and other costs of sales ($40); its
  // research and selling cost 14.9% of its revenue and its tax is 15.6% of its profit.
  W.splitprice = function (el) {
    var INDIRECT = 0.6, ASSEMBLY = 30, OTHER = 40, OPEX = 0.1493, TAX = 0.156;
    var model = function (price, channel, parts, memory) {
      var ch = price * INDIRECT * channel, rev = price - ch, gross = rev - parts - memory - ASSEMBLY - OTHER;
      var opex = OPEX * rev, pretax = gross - opex, tax = Math.max(0, TAX * pretax);
      return { ch: ch, rev: rev, parts: parts, memory: memory, asm: ASSEMBLY + OTHER, opex: opex, tax: tax,
               profit: pretax - tax, gm: rev > 0 ? gross / rev : 0 };
    };
    var names = ["shop or carrier", "other parts", "memory", "assembly, shipping, warranty", "Apple's research and selling", "tax", "Apple's profit"];
    var cols = [C.implied, C.cash, C.loss, C.house, C.spot, C.muted, C.gain];
    var stack = function (a, x, m) {
      var vals = [m.ch, m.parts, m.memory, m.asm, m.opex, m.tax, Math.max(0, m.profit)], base = 0, i;
      for (i = 0; i < vals.length; i++) {
        a.bars([x], [base + vals[i]], 0.55, { base: base, color: cols[i], alpha: 0.9 });
        base += vals[i];
      }
      return base;
    };
    QB.widget(el, {
      title: "Split the price: where $1,099 goes",
      sub: "The left column is the film's central case for a 256GB iPhone 17 Pro in 2025; the right column is the phone you set with the sliders. Raise the memory cost towards 2026's level (about $244) and watch Apple's profit shrink; then raise the price and see how much it takes to win it back.",
      panels: 2, height: 300,
      controls: [
        { k: "price", label: "Price before tax", min: 999, max: 1599, step: 10, value: 1099, fmt: function (x) { return "$" + x; } },
        { k: "channel", label: "Shop or carrier margin", min: 0, max: 0.2, step: 0.01, value: 0.1, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "parts", label: "Parts other than memory", min: 350, max: 650, step: 5, value: 468, fmt: function (x) { return "$" + x; } },
        { k: "memory", label: "Memory and storage", min: 20, max: 400, step: 2, value: 52, fmt: function (x) { return "$" + x; } },
      ],
      draw: function (g, v, s) {
        var ref = model(1099, 0.1, 468, 52), m = model(v.price, v.channel, v.parts, v.memory), top;
        top = Math.max(1650, ref.ch + ref.parts + ref.memory + ref.asm + ref.opex + ref.tax + Math.max(0, ref.profit),
                       m.ch + m.parts + m.memory + m.asm + m.opex + m.tax + Math.max(0, m.profit));
        var a = g[0].axes({ x: [-0.6, 3.3], y: [0, top], title: "Dollars per phone", xticks: [0, 1],
                            xfmt: function (x) { return x < 0.5 ? "film, 2025" : "your phone"; } });
        stack(a, 0, ref);
        stack(a, 1, m);
        a.hline(v.price, { color: C.idea });
        a.legend(names.map(function (n, i) { return [n, cols[i]]; }).reverse(), { pos: "tr" });
        var xs = [], ys = [], mm;
        for (mm = 20; mm <= 400; mm += 5) { xs.push(mm); ys.push(model(v.price, v.channel, v.parts, mm).profit); }
        var b = g[1].axes({ x: [20, 400], y: [-150, 450], title: "Apple's profit per phone, against the memory cost",
                            xlabel: "memory and storage ($)", yfmt: function (y) { return "$" + Math.round(y); } });
        b.hline(0, { color: C.muted });
        b.hline(ref.profit, { color: C.gain, dash: [4, 4] });
        b.line(xs, ys, { color: C.gain, width: 1.6 });
        b.vline(52, { color: C.muted });
        b.vline(v.memory, { color: C.idea });
        b.legend([["profit at your price", C.gain], ["your memory cost", C.idea], ["2025 memory ($52)", C.muted]], { pos: "tr" });
        s.m = m; s.ref = ref;
      },
      readout: function (v, s) {
        var m = s.m, cents = function (x) { return Math.round(100 * x / v.price) + "¢"; };
        return [["Apple's profit", "$" + Math.round(m.profit) + " (" + cents(m.profit) + " of each $)"],
                ["the parts", "$" + Math.round(m.parts + m.memory) + " (" + cents(m.parts + m.memory) + ")"],
                ["memory's share of the parts", Math.round(100 * m.memory / Math.max(1, m.parts + m.memory)) + "%"],
                ["Apple's gross margin", Math.round(100 * m.gm) + "%"]];
      },
      note: "This is the film's model of one phone, not Apple's accounts: the split of the parts, the shop's margin, assembly and other costs are estimates with ranges (the Register, Part 1). Figures in US dollars, before sales tax.",
    });
  };
  // ---- Part 2: everything a dollar touches ----------------------------------------------------------------------
  // The film's 2023 table (BEA's use table after redefinitions, fifteen sectors): A[i][j] is what sector j buys from
  // sector i per dollar of its output (videos/industry/industry2/compute.py).  One more dollar of a sector's goods
  // bought by final users sets off rounds of buying; their sum is the Leontief inverse's column.
  W.ripple = function (el) {
    var NAMES = ["Farms", "Mining", "Utilities", "Construction", "Manufacturing", "Wholesale", "Retail", "Transport", "Information", "Finance, RE", "Business svcs", "Educ., health", "Leisure", "Other svcs", "Government"];
    var A = [[0.2503, 0.0002, 0.0, 0.001, 0.0479, 0.0, 0.0005, 0.0, 0.0, 0.0, 0.0006, 0.0001, 0.0058, 0.0001, 0.0018], [0.002, 0.0788, 0.037, 0.0089, 0.0624, 0.0, 0.0001, 0.0003, 0.0009, 0.0, 0.0005, 0.0006, 0.0011, 0.0012, 0.0048], [0.017, 0.0217, 0.0563, 0.0058, 0.0114, 0.0068, 0.0191, 0.0083, 0.0071, 0.0058, 0.0034, 0.0072, 0.0185, 0.0082, 0.0111], [0.0034, 0.0068, 0.009, 0.0002, 0.0037, 0.0021, 0.0048, 0.0049, 0.0022, 0.0148, 0.001, 0.0016, 0.0052, 0.0047, 0.0297], [0.1358, 0.1181, 0.0326, 0.2216, 0.3193, 0.0486, 0.0221, 0.0774, 0.0373, 0.0088, 0.0408, 0.0712, 0.068, 0.0514, 0.117], [0.0848, 0.0318, 0.0118, 0.0552, 0.0762, 0.0269, 0.0135, 0.0175, 0.0162, 0.0041, 0.0118, 0.0212, 0.0188, 0.0148, 0.0227], [0.0028, 0.0013, 0.0041, 0.0446, 0.003, 0.0002, 0.0031, 0.0108, 0.0002, 0.0012, 0.0013, 0.0003, 0.0063, 0.007, 0.0001], [0.0293, 0.0233, 0.0424, 0.0183, 0.0285, 0.0507, 0.0426, 0.1239, 0.0097, 0.0071, 0.0121, 0.0114, 0.0107, 0.0056, 0.0212], [0.0008, 0.0013, 0.009, 0.0047, 0.004, 0.0079, 0.016, 0.0062, 0.1224, 0.0097, 0.0234, 0.0114, 0.0216, 0.0154, 0.0367], [0.023, 0.0556, 0.0343, 0.0351, 0.0219, 0.0955, 0.122, 0.112, 0.0651, 0.1995, 0.0785, 0.1036, 0.1263, 0.1142, 0.0262], [0.0065, 0.0981, 0.0504, 0.0519, 0.0346, 0.1564, 0.1068, 0.062, 0.1254, 0.0967, 0.1373, 0.0997, 0.1036, 0.0784, 0.0892], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0007, 0.0016, 0.0001, 0.0, 0.0, 0.0001, 0.011, 0.0027, 0.0032, 0.008], [0.0009, 0.0006, 0.005, 0.001, 0.0013, 0.0084, 0.0053, 0.0077, 0.0234, 0.016, 0.017, 0.027, 0.0358, 0.0045, 0.0096], [0.0006, 0.0006, 0.0018, 0.004, 0.0025, 0.009, 0.0066, 0.0111, 0.0038, 0.007, 0.0089, 0.0077, 0.0093, 0.0072, 0.0165], [0.0, 0.0, 0.0013, 0.0, 0.0008, 0.0082, 0.0037, 0.0048, 0.0012, 0.0018, 0.0017, 0.0025, 0.0063, 0.0015, 0.0032]];
    var ABBR = ["Farm", "Mine", "Util", "Build", "Mfg", "Whol", "Ret", "Trans", "Info", "Fin", "Bus", "EdH", "Leis", "Oth", "Gov"];
    var n = NAMES.length;
    var rounds = function (j, scale, K) { // cumulative output by sector after each round, k = 0..K
      var x = new Array(n).fill(0), tot = new Array(n).fill(0), path = [], i, k, y;
      x[j] = 1;
      for (k = 0; k <= K; k++) {
        for (i = 0; i < n; i++) tot[i] += x[i];
        path.push(tot.reduce(function (a, b) { return a + b; }, 0));
        y = new Array(n).fill(0);
        for (i = 0; i < n; i++) for (var m = 0; m < n; m++) y[i] += scale * A[i][m] * x[m];
        x = y;
      }
      return { tot: tot.slice(), path: path };
    };
    QB.widget(el, {
      title: "Everything a dollar touches: rounds of buying through the 2023 economy",
      sub: "Pick a sector and spend one more dollar on its goods or services. Each round, every sector that has to produce something buys its own inputs from the others. Step through the rounds and watch the total converge to the Leontief inverse; then make every industry buy more from the others and see the multiplier grow.",
      panels: 2, height: 320, weights: [1.35, 1],
      controls: [
        { k: "j", label: "Sector bought from", min: 0, max: n - 1, step: 1, value: 4, fmt: function (x) { return NAMES[x]; } },
        { k: "k", label: "Rounds of buying", min: 0, max: 15, step: 1, value: 1, fmt: function (x) { return String(x); } },
        { k: "scale", label: "Buying from others, against 2023", min: 0.6, max: 1.4, step: 0.05, value: 1, fmt: function (x) { return Math.round(100 * x) + "%"; } },
      ],
      draw: function (g, v, s) {
        var r = rounds(v.j, v.scale, v.k), full = rounds(v.j, v.scale, 200), i, xs = [];
        for (i = 0; i < n; i++) xs.push(i);
        var top = Math.max(1.6, Math.max.apply(null, full.tot) * 1.1);
        var a = g[0].axes({ x: [-0.6, n - 0.4], y: [0, top], title: "Output by sector for $1 of " + NAMES[v.j] + " bought ($)",
                            xticks: xs, xfmt: function (x) { return ABBR[Math.round(x)]; },
                            yfmt: function (y) { return "$" + y.toFixed(2); } });
        a.bars(xs, r.tot, 0.7, { color: function (i) { return i === v.j ? C.idea : C.spot; }, alpha: 0.9 });
        a.dots(xs, full.tot, { color: C.gain, r: 3.5 });
        a.legend([["after " + v.k + " round" + (v.k === 1 ? "" : "s"), C.spot], ["all rounds (Leontief inverse)", C.gain]], { pos: "tr" });
        var ks = [], ps = [];
        for (i = 0; i <= 15; i++) { ks.push(i); ps.push(full.path[i]); }
        var tmax = Math.max(2.6, full.path[full.path.length - 1] * 1.1);
        var b = g[1].axes({ x: [-0.5, 15.5], y: [0, tmax], title: "Total output after k rounds", xlabel: "round",
                            yfmt: function (y) { return "$" + y.toFixed(1); } });
        b.hline(full.path[full.path.length - 1], { color: C.gain });
        b.line(ks, ps, { color: C.idea, width: 1.6 });
        b.dots(ks.slice(0, v.k + 1), ps.slice(0, v.k + 1), { color: C.idea, r: 3.5 });
        s.r = r; s.full = full;
      },
      readout: function (v, s) {
        var got = s.r.path[s.r.path.length - 1], all = s.full.path[s.full.path.length - 1];
        return [["output so far", "$" + got.toFixed(2)], ["all rounds", "$" + all.toFixed(2)],
                ["captured", Math.round(100 * got / all) + "%"],
                ["bought from other sectors, round 1", "$" + (rounds(v.j, v.scale, 1).path[1] - 1).toFixed(2)]];
      },
      note: "Computed from BEA's 2023 input-output use table, fifteen sectors, as in the film. The model assumes each industry keeps its recipe as it grows and that its suppliers can grow with it: a guide to how industries depend on one another, not a forecast of jobs created.",
    });
  };
  // ---- Part 3: grow the bakery --------------------------------------------------------------------------------------
  // The film's model firm (explainer/industry/works/firm.py): 60,000 loaves at a price, flour and fillings $1.30 a
  // loaf, staff and rent $115,000, a $45,000 oven over ten years and then a new shop's oven each year, a $20,000 loan
  // at 7%, tax 21%; it grows by the same rate each year. Profit and cash part when customers pay late.
  W.bakery = function (el) {
    var run = function (v) {
      var cash = 40000, rec = 0, inv = 0, pay = 0, ppe = 0, debt = 0, eq = 40000, vint = [], out = [], k;
      for (k = 0; k < 6; k++) {
        var gk = Math.pow(1 + v.growth, k), capex = k === 0 ? 45000 : 30000 * gk;
        vint.push(capex);
        var dep = 0;
        vint.forEach(function (a, i) { if (vint.length - 1 - i < 10) dep += a / 10; });
        var units = 60000 * gk, rev = units * v.price, cogs = units * 1.3, fixed = 115000 * gk;
        if (k === 0) debt += 20000;
        var ebit = rev - cogs - fixed - dep, interest = 0.07 * debt, pretax = ebit - interest;
        var tax = Math.max(0, 0.21 * pretax), net = pretax - tax;
        var rec1 = rev * v.rdays / 365, inv1 = cogs * 10 / 365, pay1 = cogs * v.pdays / 365;
        var cfo = net + dep - (rec1 - rec) - (inv1 - inv) + (pay1 - pay);
        cash += cfo - capex + (k === 0 ? 20000 : 0);
        rec = rec1; inv = inv1; pay = pay1; ppe += capex - dep; eq += net;
        out.push({ year: k + 1, rev: rev, net: net, cash: cash, cfo: cfo, capex: capex,
                   assets: cash + rec + inv + ppe, rec: rec, inv: inv, ppe: ppe, pay: pay, debt: debt, eq: eq });
      }
      return out;
    };
    QB.widget(el, {
      title: "Grow the bakery: profit against cash",
      sub: "The film's model bakery. Make it grow faster, give its cafe customers longer to pay, or get longer from the miller, and watch the gap between profit and cash. The second panel is the balance sheet at the end of year 6: what it has, and whose money paid for it.",
      panels: 2, height: 320,
      controls: [
        { k: "growth", label: "Growth a year", min: 0, max: 0.8, step: 0.05, value: 0.6, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "rdays", label: "Days the cafes take to pay", min: 0, max: 90, step: 5, value: 60, fmt: function (x) { return x + " days"; } },
        { k: "pdays", label: "Days the miller gives", min: 0, max: 90, step: 5, value: 30, fmt: function (x) { return x + " days"; } },
        { k: "price", label: "Price of a loaf", min: 3.0, max: 4.5, step: 0.05, value: 3.6, fmt: function (x) { return "$" + x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var o = run(v), xs = o.map(function (r) { return r.year; });
        var lo = Math.min(0, Math.min.apply(null, o.map(function (r) { return r.cash; }))) * 1.1;
        var hi = Math.max(50000, Math.max.apply(null, o.map(function (r) { return Math.max(r.cash, r.net); }))) * 1.1;
        var a = g[0].axes({ x: [0.5, 6.5], y: [lo, hi], title: "Profit and cash, years 1-6", xticks: xs,
                            yfmt: function (y) { return "$" + Math.round(y / 1000) + "k"; } });
        a.hline(0, { color: C.muted });
        a.bars(xs.map(function (x) { return x - 0.18; }), o.map(function (r) { return r.net; }), 0.32, { color: C.gain });
        a.line(xs, o.map(function (r) { return r.cash; }), { color: C.loss, width: 2 });
        a.dots(xs, o.map(function (r) { return r.cash; }), { color: C.loss, r: 3.5 });
        a.legend([["profit for the year", C.gain], ["cash in the bank", C.loss]], { pos: "tl" });
        var L = o[o.length - 1], owns = [L.cash > 0 ? L.cash : 0, L.rec, L.inv, L.ppe];
        var owes = [L.pay, L.debt + (L.cash < 0 ? -L.cash : 0), L.eq];
        var top = Math.max(owns.reduce(function (p, q) { return p + q; }, 0), owes.reduce(function (p, q) { return p + q; }, 0)) * 1.15;
        var b = g[1].axes({ x: [-0.6, 1.6], y: [0, top], title: "Balance sheet, end of year 6", xticks: [0, 1],
                            xfmt: function (x) { return x < 0.5 ? "what it has" : "who paid for it"; },
                            yfmt: function (y) { return "$" + Math.round(y / 1000) + "k"; } });
        var cols1 = [C.cash, C.spot, C.house, C.q], cols2 = [C.implied, C.loss, C.gain], base = 0, i;
        for (i = 0; i < owns.length; i++) { b.bars([0], [base + owns[i]], 0.6, { base: base, color: cols1[i] }); base += owns[i]; }
        base = 0;
        for (i = 0; i < owes.length; i++) { b.bars([1], [base + owes[i]], 0.6, { base: base, color: cols2[i] }); base += owes[i]; }
        b.legend([["cash", C.cash], ["owed by cafes", C.spot], ["flour", C.house], ["ovens", C.q], ["owed to the miller", C.implied],
                  ["bank (and overdraft)", C.loss], ["owner", C.gain]], { pos: "tr" });
        s.o = o;
      },
      readout: function (v, s) {
        var o = s.o, neg = o.filter(function (r) { return r.cash < 0; }), L = o[o.length - 1];
        return [["cash runs out", neg.length ? "in year " + neg[0].year : "never"],
                ["profit in year 6", "$" + Math.round(L.net).toLocaleString()],
                ["cash from operations, year 6", "$" + Math.round(L.cfo).toLocaleString()],
                ["return on the owner's money, year 6", Math.round(100 * L.net / L.eq) + "%"]];
      },
      note: "A model bakery, not a real company: the same arithmetic as the film (explainer/industry/works/firm.py). A negative cash balance is money the bakery would have to borrow or raise from its owner.",
    });
  };

  // ---- Part 4: the price war -----------------------------------------------------------------------------------------
  // Two identical plants (100 units a period each, $20 of cost per unit, a fixed cost per period). Buyers each want
  // one unit at up to $80 and buy from the cheaper plant first, then the other; at equal prices they split. The rival
  // cuts 5% below the lowest price whenever it has sold less than 90% of its plant, and edges its price up 5% when
  // it is nearly full. You choose your opening price and how you answer when it undercuts you.
  W.pricewar = function (el) {
    var K = 100, MC = 20, TOP = 80, ROUNDS = 10;
    var RESP = ["hold your price", "match the rival", "undercut by 5%"];
    var play = function (v) {
      var pa = v.open, pb = 70, out = [], cumA = 0, cumB = 0, k;
      for (k = 0; k < ROUNDS; k++) {
        var qa = 0, qb = 0, Q = v.demand;
        if (pa < pb) { qa = Math.min(K, Q); qb = Math.min(K, Q - qa); }
        else if (pb < pa) { qb = Math.min(K, Q); qa = Math.min(K, Q - qb); }
        else { qa = Math.min(K, Q / 2); qb = Math.min(K, Q - qa); qa = Math.min(K, Q - qb); }
        var prA = (pa - MC) * qa - v.fixed, prB = (pb - MC) * qb - v.fixed;
        cumA += prA; cumB += prB;
        out.push({ t: k + 1, pa: pa, pb: pb, qa: qa, qb: qb, prA: prA, prB: prB, cumA: cumA, cumB: cumB });
        var low = Math.min(pa, pb), nb, na = pa;
        nb = qb < 0.9 * K ? Math.max(MC, low * 0.95) : Math.min(TOP, pb * 1.05);
        if (nb < pa) {
          if (v.resp === 1) na = nb;
          else if (v.resp === 2) na = Math.max(MC, nb * 0.95);
        }
        pa = na; pb = nb;
      }
      return out;
    };
    QB.widget(el, {
      title: "The price war: ten rounds against a rival with the same plant",
      sub: "You and a rival each run a plant that can make 100 units a period, at $20 a unit plus a fixed cost. Buyers go to the cheaper plant first. The rival undercuts you whenever its plant is less than 90% full. Set your opening price and your answer to its cuts, then lower demand below what the two plants can make and watch what happens to the price.",
      panels: 2, height: 300,
      controls: [
        { k: "open", label: "Your opening price", min: 30, max: 80, step: 1, value: 70, fmt: function (x) { return "$" + x; } },
        { k: "resp", label: "When the rival undercuts you", min: 0, max: 2, step: 1, value: 1, fmt: function (x) { return RESP[x]; } },
        { k: "demand", label: "Buyers each period (the plants make 200)", min: 100, max: 200, step: 5, value: 150, fmt: function (x) { return x + " units"; } },
        { k: "fixed", label: "Each plant's fixed cost a period", min: 0, max: 4000, step: 100, value: 2500, fmt: function (x) { return "$" + x.toLocaleString(); } },
      ],
      draw: function (g, v, s) {
        var o = play(v), ts = o.map(function (r) { return r.t; });
        var a = g[0].axes({ x: [0.5, 10.5], y: [0, 90], title: "Prices, round by round", xticks: [1, 4, 7, 10],
                            yfmt: function (y) { return "$" + y; } });
        a.hline(MC, { color: C.cash });
        a.hline(MC + v.fixed / K, { color: C.implied });
        a.line(ts, o.map(function (r) { return r.pa; }), { color: C.gain, width: 2.5 });
        a.dots(ts, o.map(function (r) { return r.pa; }), { color: C.gain, r: 3.5 });
        a.line(ts, o.map(function (r) { return r.pb; }), { color: C.loss, width: 2 });
        a.dots(ts, o.map(function (r) { return r.pb; }), { color: C.loss, r: 3 });
        a.legend([["your price", C.gain], ["rival's price", C.loss], ["cost of one more unit", C.cash], ["full cost at a full plant", C.implied]], { pos: "tr" });
        var all = o.map(function (r) { return r.cumA; }).concat(o.map(function (r) { return r.cumB; }));
        var lo = Math.min(0, Math.min.apply(null, all)) * 1.1 - 100, hi = Math.max(1000, Math.max.apply(null, all)) * 1.1;
        var b = g[1].axes({ x: [0.5, 10.5], y: [lo, hi], title: "Profit so far", xticks: [1, 4, 7, 10],
                            yfmt: function (y) { return "$" + Math.round(y / 1000) + "k"; } });
        b.hline(0, { color: C.muted });
        b.line(ts, o.map(function (r) { return r.cumA; }), { color: C.gain, width: 2.5 });
        b.line(ts, o.map(function (r) { return r.cumB; }), { color: C.loss, width: 2 });
        b.legend([["you", C.gain], ["rival", C.loss]], { pos: "tl" });
        s.o = o;
        s.ac = MC + v.fixed / K;
      },
      readout: function (v, s) {
        var o = s.o, L = o[o.length - 1];
        var below = o.filter(function (r) { return r.pa < s.ac; }).length;
        return [["your profit over ten rounds", "$" + Math.round(L.cumA).toLocaleString()],
                ["the rival's", "$" + Math.round(L.cumB).toLocaleString()],
                ["your price in round 10", "$" + L.pa.toFixed(2)],
                ["rounds you sold below full cost", below + " of 10"]];
      },
      note: "A model market, not real firms: the arithmetic of chapters 1, 8 and 10 of the film. With 200 buyers both plants are full and nobody needs to cut; below that, the plant with idle capacity always gains by undercutting while the price is above $20, the cost of one more unit, so the price falls towards it whatever you do. Holding your price keeps your margin and loses your customers.",
    });
  };
})();
