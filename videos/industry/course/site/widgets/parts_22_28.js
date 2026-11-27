// Interactives for Parts 22-28.
(function () {
  "use strict";
  var C = QB.C, W = QB.W;

  // ---- Part 22: run a brand against a store label (the Works' Brand in explainer/industry/works/brand.py) ----------
  // Shoppers choose by a logit: the brand's utility is 0.05 sqrt(advertising stock) - 0.45 price + c, the store label's
  // -0.45 x its price, with c set so the brand has 45% at the steady stock of $100m a year over a 20% decay (500) and a
  // $10 price against $5.  500 million units a year; the brand costs $4 a unit; eight years at 8%.
  W.brandrun = function (el) {
    var UNITS = 500e6, COST = 4, BETA = 0.45, K = 0.05, RATE = 0.08, YEARS = 8, STOCK0 = 500;
    var CONST = Math.log(0.45 / 0.55) - (K * Math.sqrt(STOCK0) - BETA * (10 - 5));
    function share(stock, p, sp) {
      var ub = K * Math.sqrt(Math.max(stock, 0)) - BETA * p + CONST, us = -BETA * sp;
      return 1 / (1 + Math.exp(us - ub));
    }
    function run(ads, p, sp, decay) {
      var stock = STOCK0, prof = [], sh = [], npv = 0, t;
      for (t = 0; t < YEARS; t++) {
        stock = (1 - decay) * stock + ads;
        var s = share(stock, p, sp), pr = s * UNITS * (p - COST) / 1e6 - ads;
        prof.push(pr); sh.push(100 * s); npv += pr / Math.pow(1 + RATE, t + 1);
      }
      return { prof: prof, sh: sh, npv: npv };
    }
    QB.widget(el, {
      title: "Run a brand",
      sub: "Your detergent sits on the shelf beside the store's own label. Shoppers choose by price and by how well they remember your brand, which advertising builds up and which wears off each year. You start where the film starts: $100m of advertising a year, a $10 price against the store label's $5, and 45% of the 500 million bottles sold. Change the advertising, your price, the store label's price and how fast advertising wears off.",
      panels: 2, height: 300, weights: [1, 1],
      controls: [
        { k: "ads", label: "Advertising a year, $m", min: 0, max: 300, step: 10, value: 100, fmt: function (x) { return "$" + x + "m"; } },
        { k: "price", label: "Your price, $", min: 6, max: 12, step: 0.5, value: 10, fmt: function (x) { return "$" + x.toFixed(2); } },
        { k: "store", label: "The store label's price, $", min: 3, max: 7, step: 0.5, value: 5, fmt: function (x) { return "$" + x.toFixed(2); } },
        { k: "decay", label: "Share of the advertising's effect that wears off each year", min: 0.05, max: 0.5, step: 0.05, value: 0.2, fmt: function (x) { return Math.round(100 * x) + "%"; } },
      ],
      draw: function (g, v, s) {
        var r = run(v.ads, v.price, v.store, v.decay), base = run(100, 10, 5, 0.2), xs = [], i;
        for (i = 1; i <= YEARS; i++) xs.push(i);
        var all = r.prof.concat(base.prof), lo = Math.min.apply(null, all), hi = Math.max.apply(null, all);
        var pad = Math.max(50, (hi - lo) * 0.15);
        var ax = g[0].axes({ x: [0.5, YEARS + 0.5], y: [lo - pad, hi + pad], title: "Profit after advertising, $m a year",
                             xticks: [1, 2, 3, 4, 5, 6, 7, 8], yfmt: function (y) { return Math.round(y).toLocaleString(); } });
        ax.line(xs, base.prof, { color: C.muted, width: 1.6, dash: [4, 4] });
        ax.line(xs, r.prof, { color: C.p, width: 2.4 });
        var bx = g[1].axes({ x: [0.5, YEARS + 0.5], y: [0, 100], title: "Your share of the bottles sold, %",
                             xticks: [1, 2, 3, 4, 5, 6, 7, 8], yfmt: function (y) { return Math.round(y) + "%"; } });
        bx.line(xs, base.sh, { color: C.muted, width: 1.6, dash: [4, 4] });
        bx.line(xs, r.sh, { color: C.spot, width: 2.4 });
        s.r = { r: r, base: base };
      },
      readout: function (v, s) {
        var r = s.r.r, b = s.r.base;
        return [["eight years, discounted: yours / the film's hold", "$" + (r.npv / 1e3).toFixed(2) + "bn / $" + (b.npv / 1e3).toFixed(2) + "bn"],
                ["profit in year one / year eight", "$" + Math.round(r.prof[0]).toLocaleString() + "m / $" + Math.round(r.prof[YEARS - 1]).toLocaleString() + "m"],
                ["your share in year eight", Math.round(r.sh[YEARS - 1]) + "%"],
                ["the store label's share in year eight", Math.round(100 - r.sh[YEARS - 1]) + "%"]];
      },
      note: "The Works' brand, as in the film: holding earns $1,250m a year and $7.18bn over eight years; cutting the advertising to nothing earns $1,263m in year one, then falls to $892m as share slides from 45% to 30%, $6.17bn in all; cutting the price to $8 wins 67% of the shelf but earns $1,236m a year, $7.10bn. The dashed lines are the film's hold. P&G spent $10.2bn, 11.7% of its sales, on advertising in fiscal 2026; the numbers here are illustrations.",
    });
  };

})();
