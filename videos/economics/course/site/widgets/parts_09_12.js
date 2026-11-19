// Interactives for Act III, Markets (Parts 9-12).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var C = QB.C, W = QB.W;
  var GOLD = "#F6C453", RED = "#F25F5C", GREEN = "#7BD88F", GREY_HINT = "#8B93A1";
  var ANA = "#F29E8E", BO = "#9FB8F2", LENS = "#C9A0FF";

  // ---- Part 9: the invisible hand, proved ---------------------------------------------------------------------
  W.box = function (el) {
    // the Edgeworth box of Part 9 (explainer.economics.island, Part 9; explainer.economics.agora.ge): ten fish and ten
    // baskets of coconuts; Ana has 8 and 1.5 and spends 40% on fish, Bo has 2 and 8.5 and spends 60%
    var X = 10, Y = 10, aA = 0.4, aB = 0.6, eA = [8, 1.5], eB = [2, 8.5];
    function uA(x, y) { return aA * Math.log(x) + (1 - aA) * Math.log(y); }
    function uB(x, y) { return aB * Math.log(x) + (1 - aB) * Math.log(y); }
    function indA(u, x) { return Math.exp((u - aA * Math.log(x)) / (1 - aA)); }
    function indB(u, x) { return Y - Math.exp((u - aB * Math.log(X - x)) / (1 - aB)); } // in Ana's coordinates
    function cc(x) { var kA = aA / (1 - aA), kB = aB / (1 - aB); return kB * x * Y / (kA * (X - x) + kB * x); }
    var uA0 = uA(eA[0], eA[1]), uB0 = uB(eB[0], eB[1]);
    var pStar = (aA * eA[1] + aB * eB[1]) / ((1 - aA) * eA[0] + (1 - aB) * eB[0]);
    function demand(a, e, p) { var m = p * e[0] + e[1]; return [a * m / p, (1 - a) * m]; }
    function grid(n, lo, hi) { var o = []; for (var i = 0; i < n; i++) o.push(lo + (hi - lo) * i / (n - 1)); return o; }

    QB.widget(el, {
      title: "Trade in the box",
      sub: "Ana has 8 fish and 1.5 baskets of coconuts; Bo has 2 fish and 8.5 baskets. Propose a trade: how many fish " +
           "Ana gives, and how many baskets she gets. Both accept it only if it lands in the purple lens. Keep " +
           "trading until there is nothing left that both would want, or switch to prices and find the one that " +
           "clears both markets.",
      panels: 2, height: 340, weights: [1.1, 1],
      controls: [
        { k: "give", label: "Fish Ana gives", min: 0, max: 7.5, step: 0.1, value: 2,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "get", label: "Baskets Ana gets", min: 0, max: 8, step: 0.1, value: 1,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "p", label: "Price of a fish, in baskets (price mode)", min: 0.3, max: 3, step: 0.01, value: 2,
          fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [
        { label: "Propose a trade", act: function (s) { s.mode = "trade"; } },
        { label: "Set a price", act: function (s) { s.mode = "price"; } },
        { label: "Show the contract curve", act: function (s) { s.cc = !s.cc; } },
      ],
      draw: function (g, v, s) {
        var mode = s.mode || "trade";
        var b = g[0].axes({ x: [0, X], y: [0, Y], title: "Ana's fish across, her coconuts up (Bo's from the top right)",
                            xlabel: "Ana's fish" });
        var xs = grid(200, 0.05, X - 0.05), ia = [], ib = [], lx = [], lA = [], lB = [];
        xs.forEach(function (x) { ia.push(indA(uA0, x)); ib.push(indB(uB0, x)); });
        for (var i = 0; i < xs.length; i++) if (ia[i] < ib[i]) { lx.push(xs[i]); lA.push(ia[i]); lB.push(ib[i]); }
        if (lx.length > 1) b.area(lx, lB, lA, { color: LENS, alpha: 0.25 });
        b.line(xs, ia, { color: ANA, width: 2 });
        b.line(xs, ib, { color: BO, width: 2 });
        if (s.cc) { var cy = xs.map(cc); b.line(xs, cy, { color: GOLD, width: 2.2 }); }
        b.dots([eA[0]], [eA[1]], { r: 5, color: function () { return C.ink; } });
        var out = { mode: mode };
        if (mode === "trade") {
          var x = eA[0] - v.give, y = eA[1] + v.get, ok = x > 0 && y > 0 && x < X && y < Y;
          var dA = ok ? uA(x, y) - uA0 : -Infinity, dB = ok ? uB(X - x, Y - y) - uB0 : -Infinity;
          var onCC = ok && Math.abs(y - cc(x)) < 0.1;
          if (ok) {
            b.line(xs, xs.map(function (z) { return indA(uA(x, y), z); }), { color: ANA, width: 1.2, dash: [3, 3] });
            b.line(xs, xs.map(function (z) { return indB(uB(X - x, Y - y), z); }), { color: BO, width: 1.2, dash: [3, 3] });
          }
          b.dots([x], [y], { r: 6, color: function () { return dA > 0 && dB > 0 ? (onCC ? GREEN : GOLD) : RED; } });
          var c = g[1].axes({ x: [0.5, 2.5], y: [-40, 60], title: "Better off than at the start (%)", xlabel: "Ana, Bo" });
          var gA = ok ? 100 * (Math.exp(dA) - 1) : -40, gB = ok ? 100 * (Math.exp(dB) - 1) : -40;
          c.bars([1, 2], [gA, gB], 0.6, { color: function (j) { return [ANA, BO][j]; }, alpha: 0.85 });
          c.hline(0, { color: GREY_HINT });
          out.ok = ok; out.dA = gA; out.dB = gB; out.both = dA > 0 && dB > 0; out.onCC = onCC; out.x = x; out.y = y;
        } else {
          var p = v.p, dAp = demand(aA, eA, p), dBp = demand(aB, eB, p);
          var lxs = grid(2, 0, X), ly = lxs.map(function (z) { return eA[1] - p * (z - eA[0]); });
          b.line(lxs, ly, { color: C.ink, width: 1.6 });
          b.dots([dAp[0]], [dAp[1]], { r: 5, color: function () { return ANA; } });
          b.dots([X - dBp[0]], [Y - dBp[1]], { r: 5, color: function () { return BO; } });
          var ps = grid(120, 0.3, 3), z = ps.map(function (q) { return demand(aA, eA, q)[0] + demand(aB, eB, q)[0] - X; });
          var d = g[1].axes({ x: [0.3, 3], y: [-6, 6], title: "Excess demand for fish", xlabel: "price of a fish (baskets)" });
          d.line(ps, z, { color: GOLD, width: 2.2 });
          d.hline(0, { color: GREY_HINT });
          d.vline(p, { color: C.ink, dash: [3, 3] });
          var zz = dAp[0] + dBp[0] - X;
          d.dots([p], [zz], { r: 5, color: function () { return Math.abs(zz) < 0.05 ? GREEN : RED; } });
          out.p = p; out.z = zz; out.sell = eA[0] - dAp[0]; out.buy = dBp[0] - eB[0];
        }
        s.out = out;
      },
      readout: function (v, s) {
        var o = s.out;
        if (o.mode === "trade") {
          var verdict = !o.ok ? "impossible: there aren't that many goods" :
                        !o.both ? (o.dA <= 0 ? "Ana refuses" : "Bo refuses") :
                        o.onCC ? "both accept, and there is almost nothing more to gain" : "both accept, but more trade would help both";
          return [["verdict", verdict], ["Ana", (o.dA >= 0 ? "+" : "") + o.dA.toFixed(1) + "%"],
                  ["Bo", (o.dB >= 0 ? "+" : "") + o.dB.toFixed(1) + "%"]];
        }
        return [["Ana would sell", o.sell.toFixed(2) + " fish"], ["Bo would buy", o.buy.toFixed(2) + " fish"],
                ["excess demand for fish", o.z.toFixed(2) + (Math.abs(o.z) < 0.05 ? " (both markets clear)" : "")],
                ["the clearing price", Math.abs(o.z) < 0.05 ? "found: " + pStar.toFixed(3) + " baskets a fish" :
                                       "move the price toward where excess demand is zero"]];
      },
      note: "Percent better off is the proportional change in a bundle the trader likes as much. Computed in your " +
            "browser; nothing you do here is stored or sent.",
    });
  };
})();
