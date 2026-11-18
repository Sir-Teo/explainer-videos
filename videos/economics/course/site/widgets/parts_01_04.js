// Interactives for Act I, The Question (Parts 1-4).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;
  var BLUE = "#5DADEC", AMBER = "#F2B84B", ORANGE = "#FF9F5A", GOLD = "#F6C453";

  // ---- Part 1: the pit -------------------------------------------------------------------------------------------
  W.pit = function (el) {
    var VALUES = [3.40, 3.10, 2.90, 2.70, 2.50, 2.30, 2.10, 1.90, 1.70, 1.50];
    var COSTS = [1.20, 1.40, 1.60, 1.80, 2.00, 2.20, 2.40, 2.60, 2.80, 3.00];
    var YOU = 3; // the buyer whose card says $2.70
    var mkt = QB.econ.market(VALUES, COSTS);
    QB.widget(el, {
      title: "The pit: you are the buyer with the $2.70 card",
      sub: "Nineteen other traders hold private cards. Pick the price you will call out: you bid it, and you take any " +
           "offer at or below it. The market opens six times with the same cards. Watch where the deals go, and what " +
           "you keep (your card minus your price). Then switch the others to zero intelligence and see what changes.",
      panels: 2, height: 310,
      controls: [
        { k: "bid", label: "Your price", min: 1.0, max: 2.7, step: 0.05, value: 2.3, fmt: function (x) { return "$" + x.toFixed(2); } },
        { k: "kind", label: "The other traders (0 learn, 1 random)", min: 0, max: 1, step: 1, value: 0,
          fmt: function (x) { return x ? "zero intelligence" : "learning"; } },
        { k: "periods", label: "Periods", min: 1, max: 10, step: 1, value: 6 },
      ],
      buttons: [{ label: "New market (reshuffle who calls when)", act: function (s) { s.seed = (s.seed * 7919 + 13) % 100003 || 1; } }],
      draw: function (g, v, s) {
        var res = QB.econ.auction(mkt, { kind: v.kind ? "zi" : "zip", periods: v.periods, seed: s.seed, human: YOU, bid: v.bid });
        var xs = [], ys = [], mineX = [], mineY = [], seps = [], x = 0.5, i, k;
        for (k = 0; k < res.length; k++) {
          if (k) seps.push(x - 0.75);
          for (i = 0; i < res[k].prices.length; i++) {
            xs.push(x); ys.push(res[k].prices[i]);
            if (res[k].trades[i].human) { mineX.push(x); mineY.push(res[k].prices[i]); }
            x += 1;
          }
          x += 1.5;
        }
        var xmax = Math.max(x - 1, 2);
        var a = g[0].axes({ x: [0, xmax], y: [1, 3.5], title: "Every deal, in order (periods divided by dashes)", xlabel: "deal number", noX: false });
        a.area([0, xmax], [mkt.hi, mkt.hi], mkt.lo, { color: GOLD, alpha: 0.18 });
        for (i = 0; i < seps.length; i++) a.vline(seps[i], { color: "#3a475c" });
        a.dots(xs, ys, { color: C.ink, r: 3 });
        a.dots(mineX, mineY, { color: GOLD, r: 5 });
        a.hline(v.bid, { color: GOLD, dash: [2, 3] });
        a.legend([["a deal", C.ink], ["your deal", GOLD], ["the band $2.20 to $2.30", GOLD]], { pos: "tr" });
        // the cards as staircases
        var b = g[1].axes({ x: [0, 10], y: [1, 3.5], title: "The cards: demand (blue) and supply (amber)", xlabel: "how many units" });
        var dx = [], dy = [], sx = [], sy = [];
        for (i = 0; i < 10; i++) { dx.push(i, i + 1); dy.push(mkt.v[i], mkt.v[i]); sx.push(i, i + 1); sy.push(mkt.c[i], mkt.c[i]); }
        b.area([0, mkt.q], [mkt.hi, mkt.hi], mkt.lo, { color: GOLD, alpha: 0.25 });
        b.line(dx, dy, { color: BLUE, width: 2.4 }).line(sx, sy, { color: AMBER, width: 2.4 });
        b.hline(v.bid, { color: GOLD, dash: [2, 3] });
        b.text(9.8, v.bid + 0.08, "your price", { color: GOLD, align: "right", size: 11 });
        var last = res[res.length - 1], earned = 0, n = 0;
        for (k = 0; k < res.length; k++) if (res[k].mine !== null) { earned += VALUES[YOU] - res[k].mine; n++; }
        s.out = { alpha: last.alpha, eff: last.efficiency, n: n, periods: res.length, earned: earned,
                  mean: last.prices.length ? QB.mean(last.prices) : 0 };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["you traded in", o.n + " of " + o.periods + " periods"], ["you kept", "$" + fmt(o.earned, 2)],
                ["last period: mean price", o.mean ? "$" + fmt(o.mean, 2) : "no deals"], ["Smith's alpha", fmt(o.alpha, 1) + "%"],
                ["share of the possible gain", QB.pct(o.eff, 0)]];
      },
      note: "Simulated traders: a port of Agora's market (explainer/economics/agora/market.py), Cliff's margin-adjusting " +
            "traders or Gode and Sunder's zero-intelligence ones, as in the film. The competitive band is computed from " +
            "the twenty cards. Nothing you do here is stored or sent.",
    });
  };
})();
