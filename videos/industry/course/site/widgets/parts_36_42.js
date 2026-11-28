// Interactives for Parts 36-42.
(function () {
  "use strict";
  var C = QB.C, W = QB.W;

  // ---- Part 36: run a software company (the Works' Saas in explainer/industry/works/saas.py) ---------------------------
  // ARR moves each quarter by new business from ramped salespeople (crowded as the team grows), expansion and churn;
  // extra budget buys salespeople (hired at the start of each year) or engineering, which builds a decaying product stock
  // that lowers churn and lifts expansion and sales; an optional price rise in the third quarter.
  W.saasrun = function (el) {
    var ARR0 = 200e6, REPS0 = 100, PROD = 0.45e6, RAMP = 2, REPCOST = 0.7e6, MARKET = 300, RND0 = 40e6, GA = 0.10;
    var SCALE = 150e6, DECAY = 0.20, CUT = 0.5, LIFT = 0.6, SLIFT = 0.3, BILL = 0.5, BUMP = 0.03, ELAST = 1.5, Q = 20;
    function run(v, extra, share) {
      var gm = v.gm / 100, churn0 = v.churn / 100, exp0 = v.exp / 100, rise = v.rise / 100, raiseAt = rise > 0 ? 2 : -99;
      var arr = ARR0, hires = [], stock = 0, out = { arr: [], margin: [], cash: 0 };
      for (var t = 0; t < Q; t++) {
        if (t % 4 === 0 && extra > 0) hires.push([t, extra * share / REPCOST]);
        var rndx = extra * (1 - share);
        stock = stock * Math.pow(1 - DECAY, 0.25) + rndx / 4;
        var q = stock / SCALE, ramped = REPS0, hired = 0;
        for (var i = 0; i < hires.length; i++) { hired += hires[i][1]; if (t - hires[i][0] >= RAMP) ramped += hires[i][1]; }
        var reps = REPS0 + hired, churn = churn0 * (1 - CUT * q), pq = 0;
        if (t >= raiseAt && t < raiseAt + 4) { pq = rise / 4; churn += BUMP; }
        var unit = t >= raiseAt ? Math.pow(1 + rise, 1 - ELAST) : 1;
        var crowd = (1 + REPS0 / MARKET) / (1 + reps / MARKET);
        var nw = ramped * PROD * (1 + SLIFT * q) * crowd * unit / 4;
        var start = arr;
        arr = arr + nw + arr * exp0 * (1 + LIFT * q) / 4 + arr * pq - arr * churn / 4;
        var rev = (start + arr) / 8, op = gm * rev - reps * REPCOST / 4 - (RND0 + rndx) / 4 - GA * rev;
        out.arr.push(arr); out.margin.push(op / rev); out.cash += op + BILL * (arr - start);
      }
      return out;
    }
    QB.widget(el, {
      title: "Run a software company",
      sub: "Your company rents its software by the year: $200m of annual recurring revenue (ARR), 100 salespeople and $40m of engineering. Set how many customers leave and how much the rest add, the gross margin, an extra budget and how it is split between salespeople and engineers, and a price rise in the third quarter. Five years, quarter by quarter.",
      panels: 2, height: 300, weights: [1, 1],
      controls: [
        { k: "churn", label: "ARR lost each year to customers leaving or cutting back, %", min: 2, max: 20, step: 0.5, value: 8, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "exp", label: "ARR added each year by customers who stay, %", min: 0, max: 30, step: 0.5, value: 10, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "gm", label: "Gross margin, %", min: 50, max: 90, step: 1, value: 78, fmt: function (x) { return x + "%"; } },
        { k: "extra", label: "Extra budget a year, $m", min: 0, max: 80, step: 5, value: 30, fmt: function (x) { return "$" + x + "m"; } },
        { k: "share", label: "Share of it spent on salespeople (the rest on engineers), %", min: 0, max: 100, step: 5, value: 50, fmt: function (x) { return x + "%"; } },
        { k: "rise", label: "Price rise in the third quarter, %", min: 0, max: 25, step: 1, value: 0, fmt: function (x) { return x + "%"; } },
      ],
      draw: function (g, v, s) {
        var r = run(v, v.extra * 1e6, v.share / 100), base = run({ churn: v.churn, exp: v.exp, gm: v.gm, rise: 0 }, 0, 0.5);
        var xs = []; for (var t = 1; t <= Q; t++) xs.push(t / 4);
        var top = Math.max(Math.max.apply(null, r.arr), Math.max.apply(null, base.arr)) / 1e6;
        var a = g[0].axes({ x: [0, 5], y: [0, top * 1.1], title: "ARR, $m", xfmt: function (x) { return "yr " + x.toFixed(0); },
                            yfmt: function (y) { return y.toFixed(0); } });
        a.line(xs, base.arr.map(function (x) { return x / 1e6; }), { color: C.muted, width: 1.6, dash: [5, 4] });
        a.line(xs, r.arr.map(function (x) { return x / 1e6; }), { color: C.spot, width: 2.6 });
        var shares = [], arr5 = [], cash5 = [];
        for (var sh = 0; sh <= 100; sh += 10) { var rr = run(v, v.extra * 1e6, sh / 100); shares.push(sh); arr5.push(rr.arr[Q - 1] / 1e6); cash5.push(rr.cash / 1e6); }
        var lo = Math.min(Math.min.apply(null, arr5), Math.min.apply(null, cash5)), hi = Math.max(Math.max.apply(null, arr5), Math.max.apply(null, cash5));
        var b = g[1].axes({ x: [0, 100], y: [Math.min(0, lo), hi * 1.1], title: "After five years by share to salespeople: ARR (gold), cash (green), $m",
                            xfmt: function (x) { return x.toFixed(0) + "%"; }, yfmt: function (y) { return y.toFixed(0); } });
        b.line(shares, arr5, { color: C.spot, width: 2.2 });
        b.line(shares, cash5, { color: C.gain, width: 2.2 });
        b.vline(v.share, { color: C.p, dash: [5, 4], width: 1.4 });
        s.r = r; s.base = base;
      },
      readout: function (v, s) {
        var r = s.r, g5 = r.arr[Q - 1] / r.arr[Q - 5] - 1;
        return [["ARR after five years; without the extra budget", "$" + (r.arr[Q - 1] / 1e6).toFixed(0) + "m; $" + (s.base.arr[Q - 1] / 1e6).toFixed(0) + "m"],
                ["growth in year five; operating margin in year five", (100 * g5).toFixed(1) + "%; " + (100 * r.margin[Q - 1]).toFixed(1) + "%"],
                ["cash generated over five years", (r.cash < 0 ? "-" : "") + "$" + Math.abs(r.cash / 1e6).toFixed(0) + "m"],
                ["net revenue retention at the start", (100 * (1 - v.churn / 100 + v.exp / 100)).toFixed(0) + "%"]];
      },
      note: "As in the film: with churn of 8% and expansion of 10%, an extra $30m a year split half and half ends five years with about $588m of ARR; all on engineers, about $561m but the most cash ($706m) and the highest margin; all on salespeople, about $581m and the least cash ($440m). A 10% price rise in the third quarter, with no extra budget, adds about $9m of ARR. Every input is an assumption, not any company's figures.",
    });
  };
})();
