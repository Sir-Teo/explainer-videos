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

})();
