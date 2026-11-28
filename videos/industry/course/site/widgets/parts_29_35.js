// Interactives for Parts 29-35.
(function () {
  "use strict";
  var C = QB.C, W = QB.W;

  // ---- Part 29: price a lane (the Works' Lane in explainer/industry/works/freight.py) ---------------------------------
  // A truck costs (non-fuel + diesel / mpg) a mile driven, loaded or empty.  Out: the lane's miles at the offered rate.
  // Home: a load at the back rate with some chance (after a day's wait at $450), else empty.  A network instead runs a
  // share of its miles empty, and needs cost / (1 - empty share) a loaded mile.
  W.lanerun = function (el) {
    var MPG = 6.5, DAY = 450;
    function trip(v) {
      var c = v.nonfuel + v.diesel / MPG, out = v.head * v.miles, cost = 2 * v.miles * c;
      var backRev = v.p * v.back * v.miles, wait = v.p > 0 ? DAY : 0;
      return { c: c, out: out, cost: cost, backRev: backRev, wait: wait, empty: out - cost,
               withBack: out + backRev - cost - wait, oneWay: out - v.miles * c,
               beEmpty: 2 * c, beBack: (cost + wait - backRev) / v.miles, network: c / (1 - v.share) };
    }
    QB.widget(el, {
      title: "Price a lane",
      sub: "Your truck lives in Chicago and a shipper offers a load to Atlanta. The truck costs the same a mile whether the trailer is full or empty. Choose the truck's costs, the rate offered, and what the trip home looks like, and compare with a network that keeps only a share of its miles empty.",
      panels: 2, height: 300, weights: [1, 1],
      controls: [
        { k: "nonfuel", label: "Truck's cost a mile before fuel", min: 1.5, max: 2.6, step: 0.05, value: 2.05, fmt: function (x) { return "$" + x.toFixed(2); } },
        { k: "diesel", label: "Diesel, $ a gallon", min: 2.5, max: 6.5, step: 0.05, value: 3.66, fmt: function (x) { return "$" + x.toFixed(2); } },
        { k: "miles", label: "Miles out (and back)", min: 200, max: 2000, step: 20, value: 720, fmt: function (x) { return x.toLocaleString(); } },
        { k: "head", label: "Rate offered out, a loaded mile", min: 1.5, max: 6, step: 0.05, value: 2.84, fmt: function (x) { return "$" + x.toFixed(2); } },
        { k: "back", label: "Rate for a load home, a mile", min: 0, max: 3, step: 0.05, value: 1.6, fmt: function (x) { return "$" + x.toFixed(2); } },
        { k: "p", label: "Chance of finding a load home", min: 0, max: 1, step: 0.05, value: 0.6, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "share", label: "A network's share of miles empty", min: 0.05, max: 0.5, step: 0.01, value: 0.14, fmt: function (x) { return Math.round(100 * x) + "%"; } },
      ],
      draw: function (g, v, s) {
        var r = trip(v);
        var vals = [r.out / 1e3, r.backRev / 1e3, -(r.cost + r.wait) / 1e3, r.withBack / 1e3];
        var lo = Math.min(-0.5, vals[2] * 1.1, vals[3] * 1.1), hi = Math.max(0.5, (r.out + r.backRev) / 1e3 * 1.15);
        var a = g[0].axes({ x: [-0.6, 3.6], y: [lo, hi], title: "One round trip, $ thousand",
                            xticks: [0, 1, 2, 3], xfmt: function (x) { return ["paid out", "paid home", "costs", "result"][Math.round(x)]; },
                            yfmt: function (y) { return "$" + y.toFixed(1) + "k"; } });
        a.hline(0, { color: C.muted, width: 1 });
        a.bars([0, 1, 2, 3], vals, 0.6, { color: function (i) { return i === 2 ? C.loss : (i === 3 ? (vals[3] >= 0 ? C.gain : C.loss) : C.spot); }, alpha: 0.9 });
        var es = [], need = [], k;
        for (k = 0; k <= 45; k++) { var e = 0.05 + 0.01 * k; es.push(100 * e); need.push(r.c / (1 - e)); }
        var b = g[1].axes({ x: [5, 50], y: [0, Math.max(6, r.c / 0.5 * 1.05)], title: "Rate a loaded mile needed, by share of miles empty",
                            xfmt: function (x) { return Math.round(x) + "%"; }, yfmt: function (y) { return "$" + y.toFixed(1); } });
        b.line(es, need, { color: C.p, width: 2.4 });
        b.hline(v.head, { color: C.spot, dash: [5, 4], width: 1.4 });
        b.vline(100 * v.share, { color: C.gain, width: 1.2 });
        b.legend([["needed", C.p], ["the rate offered", C.spot], ["your network", C.gain]], { pos: "tl" });
        s.r = r;
      },
      readout: function (v, s) {
        var r = s.r;
        function usd(x) { return (x < 0 ? "-$" : "+$") + Math.abs(Math.round(x)).toLocaleString(); }
        return [["the truck's cost a mile", "$" + r.c.toFixed(2)],
                ["one way only; home empty", usd(r.oneWay) + "; " + usd(r.empty)],
                ["with the chance of a load home", usd(r.withBack)],
                ["rate out needed: empty home / with loads home / network", "$" + r.beEmpty.toFixed(2) + " / $" + r.beBack.toFixed(2) + " / $" + r.network.toFixed(2)]];
      },
      note: "As in the film: a truck at $2.61 a mile earns $166 one way at J.B. Hunt's $2.84 a loaded mile, loses $1,716 when it drives home empty, and needs $5.23 a loaded mile to pay; Knight-Swift ran 13.9% of its miles empty in 2025, which needs about $3.04. The truck's cost before fuel, the rate home and its chance are this series' assumptions.",
    });
  };

  // ---- Part 30: bid for spectrum (the Works' Auction in explainer/industry/works/telco.py) ----------------------------
  // A uniform-price ascending clock: the price rises by $0.25bn a block while the blocks wanted exceed the supply; each
  // bidder wants the blocks it values at or above the price, up to a cap; everyone pays the final price.
  W.spectrumclock = function (el) {
    var RIVALS = [[6.0, 4.5, 4.5, 2.0], [10.0, 7.0, 4.0, 1.5], [9.0, 7.5, 7.0, 3.5]], STEP = 0.25;
    function run(you, cap, supply) {
      var vals = [you].concat(RIVALS), caps = [cap, 4, 4, 4], p = 0, path = [], d, i;
      while (true) {
        d = [];
        for (i = 0; i < 4; i++) {
          var n = 0, k;
          for (k = 0; k < 4; k++) if (vals[i][k] >= p - 1e-9) n++;
          d.push(Math.min(n, caps[i]));
        }
        var tot = d.reduce(function (a, b) { return a + b; }, 0);
        path.push([p, tot]);
        if (tot <= supply || p > 50) break;
        p = Math.round((p + STEP) * 100) / 100;
      }
      var sur = d.map(function (n, j) { var v = 0, k; for (k = 0; k < n; k++) v += vals[j][k]; return v - n * p; });
      return { p: p, d: d, sur: sur, path: path, rev: p * d.reduce(function (a, b) { return a + b; }, 0) };
    }
    QB.widget(el, {
      title: "Bid for spectrum",
      sub: "Eight blocks of airwaves (or as many as you choose) are sold by a rising clock: each bidder says how many blocks it wants at each price, and when no more are wanted than are on offer, every winner pays that price for each block. Set what the blocks are worth to you and how many you will ask for, and see the price, what you win and what you keep. The three rivals bid honestly, with the film's values.",
      panels: 2, height: 300, weights: [1, 1],
      controls: [
        { k: "cap", label: "Most blocks you ask for", min: 1, max: 4, step: 1, value: 4, fmt: function (x) { return String(x); } },
        { k: "v1", label: "Your 1st block is worth, $bn", min: 1, max: 12, step: 0.5, value: 9.5, fmt: function (x) { return "$" + x.toFixed(1); } },
        { k: "v2", label: "Your 2nd block", min: 0.5, max: 12, step: 0.5, value: 9.0, fmt: function (x) { return "$" + x.toFixed(1); } },
        { k: "v3", label: "Your 3rd block", min: 0.5, max: 12, step: 0.5, value: 7.0, fmt: function (x) { return "$" + x.toFixed(1); } },
        { k: "v4", label: "Your 4th block", min: 0.5, max: 12, step: 0.5, value: 6.5, fmt: function (x) { return "$" + x.toFixed(1); } },
        { k: "supply", label: "Blocks on offer", min: 5, max: 12, step: 1, value: 8, fmt: function (x) { return String(x); } },
      ],
      draw: function (g, v, s) {
        var you = [v.v1, v.v2, v.v3, v.v4].sort(function (a, b) { return b - a; });
        var r = run(you, v.cap, v.supply), xs = [], ys = [], i;
        for (i = 0; i < r.path.length; i++) { xs.push(r.path[i][0]); ys.push(r.path[i][1]); }
        var xmax = Math.max(8, r.p + 1);
        var a = g[0].axes({ x: [0, xmax], y: [0, 17], title: "Blocks wanted as the price rises", xfmt: function (x) { return "$" + x.toFixed(0) + "bn"; },
                            yfmt: function (y) { return Math.round(y); } });
        a.hline(v.supply, { color: C.muted, dash: [4, 4], width: 1.2 });
        a.line(xs, ys, { color: C.p, width: 2.4 });
        a.vline(r.p, { color: C.spot, dash: [5, 4], width: 1.4 });
        a.legend([["blocks wanted", C.p], ["blocks on offer", C.muted], ["final price", C.spot]], { pos: "tr" });
        var caps = [1, 2, 3, 4], sur = caps.map(function (c) { return run(you, c, v.supply).sur[0]; });
        var hi = Math.max(1, Math.max.apply(null, sur) * 1.2), lo = Math.min(0, Math.min.apply(null, sur) * 1.2);
        var b = g[1].axes({ x: [0.4, 4.6], y: [lo, hi], title: "What you keep (value less price), by blocks asked for",
                            xticks: caps, xfmt: function (x) { return Math.round(x) + " max"; }, yfmt: function (y) { return "$" + y.toFixed(1) + "bn"; } });
        b.bars(caps, sur, 0.6, { color: function (i) { return caps[i] === v.cap ? C.gain : C.spot; }, alpha: 0.9 });
        s.r = r; s.best = caps[sur.indexOf(Math.max.apply(null, sur))];
      },
      readout: function (v, s) {
        var r = s.r;
        return [["final price a block", "$" + r.p.toFixed(2) + "bn"],
                ["blocks won: you, A, B, C", r.d.join(", ")],
                ["what you keep; the best number to ask for", "$" + r.sur[0].toFixed(2) + "bn; " + s.best],
                ["what the auction raised", "$" + r.rev.toFixed(1) + "bn"]];
      },
      note: "As in the film: bidding honestly for every block you value, the clock stops at $6.75bn and you keep $5.25bn on three blocks; asking for two, it stops at $4.75bn and you keep $9.00bn, and every rival is better off too, while the auction raises $38bn instead of $54bn. The values are an illustration.",
    });
  };

  // ---- Part 31: run a store for a year (the Works' Store in explainer/industry/works/store.py) ------------------------
  // Volume = p^elasticity x a staffing factor; goods cost (1 - gm) of base sales per unit of volume; labour is a share of
  // base sales times the hours; rent is fixed; other costs are a share of revenue.
  W.storeyear = function (el) {
    var OCC = 0.03, OTHER = 0.07;
    function vol(p, s, e) {
      var v = Math.pow(p, e);
      if (s < 1) v *= 1 - 0.6 * (1 - s) - 1.5 * (1 - s) * (1 - s); else v *= 1 + 0.3 * (s - 1) - (s - 1) * (s - 1);
      return v;
    }
    function year(v, p, s) {
      var sales = v.sales * 1e6, q = vol(p, s, v.e), rev = sales * p * q, goods = sales * (1 - v.gm / 100) * q;
      var lab = sales * v.lab / 100 * s, profit = rev - goods - lab - sales * OCC - rev * OTHER;
      return { rev: rev, profit: profit, margin: profit / rev, q: q };
    }
    QB.widget(el, {
      title: "Run a store for a year",
      sub: "A supermarket with a few rivals nearby. Set its sales, its gross margin, how much its shoppers care about price, its staff costs, and then choose its prices against the rivals' and its staff hours, and see a year's profit.",
      panels: 2, height: 300, weights: [1, 1],
      controls: [
        { k: "p", label: "Prices against rivals", min: 0.94, max: 1.06, step: 0.005, value: 1.0, fmt: function (x) { return (x >= 1 ? "+" : "") + (100 * (x - 1)).toFixed(1) + "%"; } },
        { k: "s", label: "Staff hours against normal", min: 0.75, max: 1.25, step: 0.01, value: 1.0, fmt: function (x) { return (x >= 1 ? "+" : "") + Math.round(100 * (x - 1)) + "%"; } },
        { k: "sales", label: "Sales a year, $ million", min: 20, max: 80, step: 1, value: 50, fmt: function (x) { return "$" + x + "m"; } },
        { k: "gm", label: "Gross margin, %", min: 18, max: 32, step: 0.1, value: 23.3, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "lab", label: "Staff cost, % of sales", min: 8, max: 14, step: 0.1, value: 11, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "e", label: "Shoppers' price sensitivity", min: -9, max: -3, step: 0.1, value: -5.7, fmt: function (x) { return x.toFixed(1); } },
      ],
      draw: function (g, v, s) {
        var ps = [], pp = [], k, best = { p: 1, v: -1e18 };
        for (k = 0; k <= 48; k++) { var p = 0.94 + 0.0025 * k, y = year(v, p, v.s).profit / 1e6; ps.push(100 * (p - 1)); pp.push(y); if (y > best.v) best = { p: p, v: y }; }
        var lo = Math.min.apply(null, pp), hi = Math.max.apply(null, pp);
        var a = g[0].axes({ x: [-6, 6], y: [Math.min(lo, 0) - 0.1, hi + 0.2], title: "Profit, $m a year, by prices against rivals",
                            xfmt: function (x) { return (x > 0 ? "+" : "") + x.toFixed(0) + "%"; }, yfmt: function (y) { return "$" + y.toFixed(1) + "m"; } });
        a.hline(0, { color: C.muted, dash: [4, 4], width: 1 });
        a.line(ps, pp, { color: C.gain, width: 2.4 });
        a.vline(100 * (v.p - 1), { color: C.spot, dash: [5, 4], width: 1.4 });
        var ss = [], sp = [];
        for (k = 0; k <= 50; k++) { var st = 0.75 + 0.01 * k; ss.push(100 * (st - 1)); sp.push(year(v, v.p, st).profit / 1e6); }
        var lo2 = Math.min.apply(null, sp), hi2 = Math.max.apply(null, sp);
        var b = g[1].axes({ x: [-25, 25], y: [Math.min(lo2, 0) - 0.1, hi2 + 0.2], title: "Profit, $m a year, by staff hours",
                            xfmt: function (x) { return (x > 0 ? "+" : "") + x.toFixed(0) + "%"; }, yfmt: function (y) { return "$" + y.toFixed(1) + "m"; } });
        b.hline(0, { color: C.muted, dash: [4, 4], width: 1 });
        b.line(ss, sp, { color: C.p, width: 2.4 });
        b.vline(100 * (v.s - 1), { color: C.spot, dash: [5, 4], width: 1.4 });
        s.r = year(v, v.p, v.s); s.best = best;
      },
      readout: function (v, s) {
        var r = s.r;
        return [["sales this year", "$" + (r.rev / 1e6).toFixed(1) + "m"],
                ["profit; per dollar", "$" + (r.profit / 1e6).toFixed(2) + "m; " + (100 * r.margin).toFixed(1) + "c"],
                ["shoppers against normal", (r.q >= 1 ? "+" : "") + (100 * (r.q - 1)).toFixed(1) + "%"],
                ["the most profitable price here", (s.best.p >= 1 ? "+" : "") + (100 * (s.best.p - 1)).toFixed(1) + "%"]];
      },
      note: "As in the film: on $50m of sales at Kroger's 23.3% gross margin, the store keeps $1.15m, 2.3 cents a dollar; 3% cheaper it keeps $1.04m, 3% dearer $1.07m; a 1% price cut needs 6.1% more sales to stand still; 20% fewer staff hours cut profit to $0.78m. The staff, rent and other costs and the shoppers' sensitivity are this series' assumptions.",
    });
  };

})();
