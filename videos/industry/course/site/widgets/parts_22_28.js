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

  // ---- Part 23: buy the season (the Works' Season in explainer/industry/works/fashion.py) -----------------------------
  // Demand is lognormal with a mean of 100,000; its forecast error is cv months ahead and 20% once the first weeks of the
  // season have shown how the style sells.  A shirt sells for $40; made far away and ordered early it costs $12, made
  // nearby and ordered late it costs the "late" price; leftovers go in the sale.  The buyer orders a base early and, after
  // the first weeks, tops up to the best late order for what they showed.  Expectations over what the first weeks reveal
  // are taken on a grid of 161 points.
  W.seasonbuy = function (el) {
    var P = 40, MEAN = 100000, CVN = 0.2, CF = 12, Z = [], WZ = [], i;
    for (i = 0; i <= 160; i++) { var z = -8 + 0.1 * i; Z.push(z); WZ.push(Math.exp(-z * z / 2)); }
    var wsum = WZ.reduce(function (a, b) { return a + b; }, 0);
    WZ = WZ.map(function (w) { return w / wsum; });
    function ncdf(x) {
      var t = 1 / (1 + 0.2316419 * Math.abs(x)), d = 0.3989422804 * Math.exp(-x * x / 2);
      var p = d * t * (0.31938153 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))));
      return x >= 0 ? 1 - p : p;
    }
    function nppf(p) {  // Acklam's rational approximation
      var a = [-39.69683028665376, 220.9460984245205, -275.9285104469687, 138.357751867269, -30.66479806614716, 2.506628277459239];
      var b = [-54.47609879822406, 161.5858368580409, -155.6989798598866, 66.80131188771972, -13.28068155288572];
      var c = [-0.007784894002430293, -0.3223964580411365, -2.400758277161838, -2.549732539343734, 4.374664141464968, 2.938163982698783];
      var d = [0.007784695709041462, 0.3224671290700398, 2.445134137142996, 3.754408661907416];
      var q, r;
      if (p < 0.02425) { q = Math.sqrt(-2 * Math.log(p)); return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
      if (p > 0.97575) { q = Math.sqrt(-2 * Math.log(1 - p)); return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
      q = p - 0.5; r = q * q;
      return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
    }
    function sold(q, mu, s) {
      var lq = Math.log(Math.max(q, 1e-9)), m = Math.exp(mu + s * s / 2);
      return m * ncdf((lq - mu - s * s) / s) + q * (1 - ncdf((lq - mu) / s));
    }
    function sig(cvf) {
      var sf = Math.sqrt(Math.log(1 + cvf * cvf)), sn = Math.sqrt(Math.log(1 + CVN * CVN));
      return { sf: sf, sn: sn, s1: Math.sqrt(Math.max(sf * sf - sn * sn, 1e-9)), mu0: Math.log(MEAN) - sf * sf / 2 };
    }
    function summary(q, sd, cost, cl) {
      var left = q - sd, rev = P * sd + cl * left;
      return { ordered: q, sold: sd, cleared: left, lost: MEAN - sd, profit: rev - cost, gm: (rev - cost) / rev };
    }
    function far(cvf, cl) {
      var g = sig(cvf), q = Math.exp(g.mu0 + g.sf * nppf((P - CF) / (P - cl)));
      return summary(q, sold(q, g.mu0, g.sf), CF * q, cl);
    }
    function chase(base, cvf, cn, cl) {
      var g = sig(cvf), z = nppf((P - cn) / (P - cl)), q = 0, sd = 0, top = 0, k;
      for (k = 0; k < Z.length; k++) {
        var mu = g.mu0 + g.s1 * Z[k], tgt = Math.exp(mu + g.sn * z), qq = Math.max(base, tgt);
        q += WZ[k] * qq; sd += WZ[k] * sold(qq, mu, g.sn); top += WZ[k] * (qq - base);
      }
      return summary(q, sd, CF * base + cn * top, cl);
    }
    QB.widget(el, {
      title: "Buy the season",
      sub: "A new T-shirt sells for $40, and on average 100,000 people will want one, but months ahead nobody knows how many. Order a base early from a factory far away at $12 a shirt; after the first weeks of the season, top up from a factory nearby at the late price. Whatever is left at the end goes in the sale. Choose the early base, how good the forecast is months ahead, the late price and the sale price.",
      panels: 2, height: 300, weights: [1, 1],
      controls: [
        { k: "base", label: "Early base order, thousand shirts", min: 0, max: 200, step: 5, value: 110, fmt: function (x) { return x + "k"; } },
        { k: "cv", label: "Forecast error months ahead (share of average demand)", min: 0.25, max: 1.0, step: 0.05, value: 0.6, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "cn", label: "Late price a shirt, from nearby, $", min: 12, max: 30, step: 1, value: 16, fmt: function (x) { return "$" + x; } },
        { k: "cl", label: "Sale price for leftovers, $", min: 0, max: 11, step: 1, value: 8, fmt: function (x) { return "$" + x; } },
      ],
      draw: function (g, v, s) {
        var bases = [], prof = [], b, best = { b: 0, p: -1e18 };
        for (b = 0; b <= 200; b += 5) {
          var r = chase(b * 1000, v.cv, v.cn, v.cl);
          bases.push(b); prof.push(r.profit / 1e6);
          if (r.profit > best.p) best = { b: b, p: r.profit };
        }
        var f = far(v.cv, v.cl), mine = chase(v.base * 1000, v.cv, v.cn, v.cl);
        var lo = Math.min.apply(null, prof.concat([f.profit / 1e6])), hi = Math.max.apply(null, prof.concat([f.profit / 1e6]));
        var pad = Math.max(0.05, (hi - lo) * 0.15);
        var ax = g[0].axes({ x: [0, 200], y: [lo - pad, hi + pad], title: "Expected profit of the season, $m",
                             xticks: [0, 50, 100, 150, 200], xfmt: function (x) { return x + "k"; }, yfmt: function (y) { return y.toFixed(2); } });
        ax.line(bases, prof, { color: C.p, width: 2.4 });
        ax.hline(f.profit / 1e6, { color: C.muted, dash: [4, 4] });
        ax.vline(v.base, { color: C.spot, dash: [5, 4], width: 1.4 });
        ax.legend([["a base early, the hits chased late", C.p], ["everything early, the best amount", C.muted]], { pos: "bl" });
        var keys = ["sold at full price", "left for the sale", "customers who found none"];
        var mv = [mine.sold / 1000, mine.cleared / 1000, mine.lost / 1000], fv = [f.sold / 1000, f.cleared / 1000, f.lost / 1000];
        var top = Math.max.apply(null, mv.concat(fv)) * 1.15;
        var bx = g[1].axes({ x: [-0.5, 2.5], y: [0, top], title: "Shirts, thousand: your buy (colour) and everything early (grey)",
                             xticks: [0, 1, 2], xfmt: function (x) { return keys[Math.round(x)] || ""; }, yfmt: function (y) { return Math.round(y); } });
        bx.bars([-0.18, 0.82, 1.82], fv, 0.32, { color: C.muted, alpha: 0.9 });
        bx.bars([0.18, 1.18, 2.18], mv, 0.32, { color: C.spot, alpha: 0.9 });
        s.r = { mine: mine, far: f, best: best };
      },
      readout: function (v, s) {
        var m = s.r.mine, f = s.r.far, b = s.r.best;
        return [["your expected profit / everything early", "$" + (m.profit / 1e6).toFixed(2) + "m / $" + (f.profit / 1e6).toFixed(2) + "m"],
                ["the best early base here", b.b + "k shirts, $" + (b.p / 1e6).toFixed(2) + "m"],
                ["your gross margin / everything early", (100 * m.gm).toFixed(1) + "% / " + (100 * f.gm).toFixed(1) + "%"],
                ["shirts ordered in all, on average", Math.round(m.ordered / 1000) + "k"]];
      },
      note: "The Works' season, as in the film: everything ordered early (162,000 shirts) earns $2.32m and leaves 70,000 for the sale; everything ordered late earns $2.19m; a base of about 111,000 early with the hits chased late earns $2.49m at a 59.4% gross margin. Inditex's gross margin in the year to January 2026 was 58.3%. The numbers here are illustrations.",
    });
  };

  // ---- Part 24: bid for five tenders (the Works' Tender in explainer/industry/works/contractor.py) --------------------
  // A job really costs $100m.  Each bidder's estimate is off by a normal error (sd as a share of the cost); the rivals add
  // their markup to their estimates; the lowest bid wins and is paid its bid.  Your chance of winning at your estimate is
  // the chance every rival bids higher; expectations integrate over your own error on a grid of 801 points.
  W.sealedbid = function (el) {
    var COST = 100;
    function ncdf(x) {
      var t = 1 / (1 + 0.2316419 * Math.abs(x)), d = 0.3989422804 * Math.exp(-x * x / 2);
      var p = d * t * (0.31938153 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))));
      return x >= 0 ? 1 - p : p;
    }
    function bid(m, sd, mr, n) {
      var N = 801, i, win = 0, prof = 0, rev = 0, est = 0, wsum = 0;
      for (i = 0; i < N; i++) {
        var e = -7 * sd + 14 * sd * i / (N - 1), w = Math.exp(-0.5 * (e / sd) * (e / sd));
        var b = (1 + m) * (1 + e) * COST, re = b / (COST * (1 + mr)) - 1;
        var pw = Math.pow(1 - ncdf(re / sd), n);
        wsum += w; win += w * pw; prof += w * pw * (b - COST); rev += w * pw * b; est += w * pw * e;
      }
      return { win: win / wsum, profit: prof / wsum, margin: rev > 0 ? prof / rev : 0, est: win > 0 ? est / win : 0 };
    }
    QB.widget(el, {
      title: "Bid for five tenders",
      sub: "A job really costs $100m, but every bidder's estimate is off a little, sometimes high and sometimes low. You and your rivals each add a markup to your own estimate and hand in a sealed price; the lowest price wins and is paid what it bid. Choose your markup, how far off estimates are, what the rivals add and how many of them there are.",
      panels: 2, height: 300, weights: [1, 1],
      controls: [
        { k: "m", label: "Your markup on your estimate", min: 0, max: 0.25, step: 0.01, value: 0.08, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "sd", label: "How far off estimates are (standard deviation)", min: 0.01, max: 0.12, step: 0.01, value: 0.05, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "mr", label: "What the rivals add", min: 0, max: 0.2, step: 0.01, value: 0.08, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "n", label: "Number of rivals", min: 1, max: 9, step: 1, value: 4, fmt: function (x) { return x; } },
      ],
      draw: function (g, v, s) {
        var ms = [], prof = [], win = [], k, best = { m: 0, p: -1e18 };
        for (k = 0; k <= 25; k++) {
          var r = bid(k / 100, v.sd, v.mr, v.n);
          ms.push(k); prof.push(5 * r.profit); win.push(100 * r.win);
          if (r.profit > best.p) best = { m: k, p: r.profit };
        }
        var lo = Math.min.apply(null, prof), hi = Math.max.apply(null, prof), pad = Math.max(0.3, (hi - lo) * 0.12);
        var ax = g[0].axes({ x: [0, 25], y: [lo - pad, hi + pad], title: "Expected profit over five tenders, $m",
                             xticks: [0, 5, 10, 15, 20, 25], xfmt: function (x) { return x + "%"; }, yfmt: function (y) { return y.toFixed(1); } });
        ax.hline(0, { color: C.muted });
        ax.line(ms, prof, { color: C.p, width: 2.4 });
        ax.vline(100 * v.m, { color: C.spot, dash: [5, 4], width: 1.4 });
        var bx = g[1].axes({ x: [0, 25], y: [0, 100], title: "Your chance of winning each tender, %",
                             xticks: [0, 5, 10, 15, 20, 25], xfmt: function (x) { return x + "%"; }, yfmt: function (y) { return Math.round(y) + "%"; } });
        bx.line(ms, win, { color: C.q, width: 2.4 });
        bx.vline(100 * v.m, { color: C.spot, dash: [5, 4], width: 1.4 });
        s.r = { mine: bid(v.m, v.sd, v.mr, v.n), best: best };
      },
      readout: function (v, s) {
        var r = s.r.mine, b = s.r.best;
        return [["jobs won of five, on average", (5 * r.win).toFixed(2)],
                ["margin on the work you win (you added " + Math.round(100 * v.m) + "%)", (100 * r.margin).toFixed(1) + "%"],
                ["your estimate when you win, against the true cost", (100 * r.est).toFixed(1) + "%"],
                ["best markup here; its profit over five tenders", b.m + "%; $" + (5 * b.p).toFixed(2) + "m"]];
      },
      note: "The Works' tender, as in the film: with estimates 5% off and four rivals adding 8%, adding 8% yourself wins one tender in five and keeps a 1.7% margin on the work won; adding 2% wins 2.7 of five and loses $2.8m; the best markup is about 8%. Real American general contractors have kept about 3 cents of each dollar of revenue. The numbers here are illustrations.",
    });
  };

})();
