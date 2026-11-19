// Interactives for Act IV, Failure and Design (Parts 13-18).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var W = QB.W;
  var GOLD = "#F6C453", RED = "#F25F5C", GREEN = "#7BD88F", GREY_HINT = "#8B93A1", BLUE = "#9FB8F2";

  function rng(seed) {
    var a = seed >>> 0;
    return function () {
      a += 0x6D2B79F5;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ---- Part 13: lemons and signals -----------------------------------------------------------------------------
  W.lemons = function (el) {
    // the used-boat market of Part 13 (explainer.economics.agora.info, lemons and lemons_offers): a boat's worth to
    // its owner is uniform on [0, 100]; to a buyer it is worth that plus a premium (or times a multiple); the reader
    // makes offers on 40 boats one after another, without seeing them, or with an inspection
    var H = 100, N = 40;
    function value(q, v, mult) { return mult ? v.mult * q : q + v.premium; }
    QB.widget(el, {
      title: "Buy a used boat you cannot inspect",
      sub: "Forty owners each have a boat worth something between $0 and $100 to them, every value equally likely; " +
           "to you each is worth more. You make the same offer to every owner, and an owner sells only if your offer " +
           "beats what the boat is worth to them. Find your best offer; then see where a market of many buyers " +
           "would settle, and what an inspection is worth.",
      panels: 2, height: 330, weights: [1.1, 1],
      controls: [
        { k: "offer", label: "Your offer, $", min: 0, max: 100, step: 1, value: 60,
          fmt: function (x) { return "$" + x.toFixed(0); } },
        { k: "premium", label: "What a boat is worth to you over its owner's value, $", min: 0, max: 60, step: 1,
          value: 30, fmt: function (x) { return "+$" + x.toFixed(0); } },
        { k: "mult", label: "(Akerlof's version) or times its owner's value", min: 1, max: 3, step: 0.1, value: 1.5,
          fmt: function (x) { return "x" + x.toFixed(1); } },
      ],
      buttons: [
        { label: "New boats", act: function (s) { s.seed = (s.seed || 1970) + 1; } },
        { label: "Switch to Akerlof's version (times, not plus)", act: function (s) { s.mult = !s.mult; } },
        { label: "Pay for an inspection", act: function (s) { s.inspect = !s.inspect; } },
      ],
      draw: function (g, v, s) {
        var r = rng(s.seed || 1970), mult = !!s.mult;
        var boats = [], k;
        for (k = 0; k < N; k++) boats.push(r() * H);
        var got = [], gain = 0;
        boats.forEach(function (q) {
          var willing = s.inspect ? value(q, v, mult) > q : true;     // with an inspection you offer only on good buys
          var price = s.inspect ? Math.max(q + 0.01, 0) : v.offer;  // and you pay just above the owner's value
          if (willing && price > q && (!s.inspect || price <= value(q, v, mult))) {
            got.push([q, value(q, v, mult) - price]);
            gain += value(q, v, mult) - price;
          }
        });
        // panel 1: the market: value of the average boat offered against the price
        var ps = [], vals = [];
        for (k = 0; k <= 100; k++) { ps.push(k); vals.push(value(k / 2, v, mult)); }
        var a = g[0].axes({ x: [0, 100], y: [0, 160], title: "A market of many buyers, $ (white: the price)",
                            xlabel: "price (green: what the average boat offered is worth to a buyer)" });
        a.line([0, 100], [0, 100], { color: "#DDDDDD", width: 1.4 });
        a.line(ps, vals, { color: GREEN, width: 2.2 });
        var eq = 0;
        for (k = 100; k >= 0; k--) { if (vals[k] >= ps[k] - 1e-9) { eq = ps[k]; break; } }
        if (eq > 0) a.dots([eq], [eq], { r: 6, color: function () { return GOLD; } });
        a.vline(v.offer, { color: GOLD, dash: [3, 3] });
        // panel 2: the boats you bought
        var b = g[1].axes({ x: [0, 100], y: [-60, 60], title: "Boats you bought: your gain on each, $",
                            xlabel: "the boat's worth to its owner (hidden from you" + (s.inspect ? ", until inspected)" : ")") });
        b.hline(0, { color: GREY_HINT });
        b.dots(got.map(function (x) { return x[0]; }), got.map(function (x) { return x[1]; }),
               { r: 4, color: function (j) { return got[j][1] >= 0 ? GREEN : RED; } });
        s.out = { n: got.length, gain: gain, eq: eq, shareEq: eq / H };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["boats you bought", o.n + " of " + N], ["your total gain", "$" + o.gain.toFixed(0)],
                ["per boat offered", "$" + (o.gain / N).toFixed(2)],
                ["a market of many buyers settles at", o.eq > 0 ? "$" + o.eq.toFixed(0) + " (" +
                   (100 * o.shareEq).toFixed(0) + "% of boats trade)" : "no price: nothing trades"],
                ["mode", (s.mult ? "times its value" : "plus a premium") + (s.inspect ? ", with an inspection" : "")]];
      },
      note: "With a premium of $30 your best blind offer is $30 (Part 13, chapter 1) and a market settles at $60; with " +
            "Akerlof's x1.5 no price works. Computed in your browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 14: incentives -------------------------------------------------------------------------------------
  W.contract = function (el) {
    // Friday's contract of Part 14 (explainer.economics.agora.contracts.linear_agency): a day's harvest is effort plus
    // luck (sd sigma); effort e costs c e^2 / 2 baskets; Friday is risk averse (CARA, r) and takes the job only if the
    // pay is worth at least nothing extra; pay is a fixed amount plus a share of the harvest
    var C = 0.1, DAYS = 40;
    function terms(v, s) {
      var b = v.share, e = b / C, risk = v.r * b * b * v.sigma * v.sigma / 2;
      var fixed = s.fit ? -b * e + C * e * e / 2 + risk : v.fixed;
      var ce = fixed + b * e - C * e * e / 2 - risk;
      var accepts = ce >= -1e-9;
      var bstar = 1 / (1 + v.r * C * v.sigma * v.sigma);
      var best = bstar / (2 * C);
      return { b: b, e: accepts ? e : 0, risk: risk, fixed: fixed, ce: ce, accepts: accepts, bstar: bstar, best: best,
               profit: accepts ? e - fixed - b * e : 0 };
    }
    QB.widget(el, {
      title: "Write Friday's contract",
      sub: "You are Crusoe. Friday works your grove, and a day's harvest is Friday's effort, in baskets, plus luck. " +
           "You can't see the effort, only the harvest. Offer a fixed pay and a share of the harvest: Friday takes " +
           "the job only if it is worth it to them, and then works as hard as the share makes worth while. Find the " +
           "share that earns you the most, and see how it moves with the luck and with Friday's dislike of risk.",
      panels: 2, height: 330, weights: [1.1, 1],
      controls: [
        { k: "share", label: "Friday's share of the harvest", min: 0, max: 1, step: 0.01, value: 0.5,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
        { k: "fixed", label: "Fixed pay, baskets a day (negative: a rent Friday pays you)", min: -15, max: 10,
          step: 0.1, value: 0, fmt: function (x) { return x.toFixed(1); } },
        { k: "sigma", label: "Luck in the harvest, sd in baskets", min: 0, max: 10, step: 0.5, value: 5,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "r", label: "Friday's dislike of risk, r", min: 0, max: 1, step: 0.05, value: 0.2,
          fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [
        { label: "Set the fixed pay so Friday just accepts", act: function (s) { s.fit = !s.fit; } },
        { label: "New seasons", act: function (s) { s.seed = (s.seed || 1978) + 1; } },
      ],
      draw: function (g, v, s) {
        var t = terms(v, s), k;
        // panel 1: your profit against the share, with the fixed pay that just keeps Friday on
        var bs = [], pr = [];
        for (k = 0; k <= 100; k++) {
          var b = k / 100, e = b / C;
          bs.push(b); pr.push(e - C * e * e / 2 - v.r * b * b * v.sigma * v.sigma / 2);
        }
        var a = g[0].axes({ x: [0, 1], y: [-1, 5.5], title: "Your profit, baskets a day, at each share " +
                            "(the fixed pay set so Friday just accepts)", xlabel: "Friday's share" });
        a.hline(5, { color: GREY_HINT, dash: [4, 4] });
        a.line(bs, pr, { color: GREEN, width: 2.2 });
        a.dots([t.bstar], [t.best], { r: 6, color: function () { return GOLD; } });
        a.dots([t.b], [t.profit], { r: 5, color: function () { return t.accepts ? BLUE : RED; } });
        // panel 2: forty days: the harvest and Friday's pay
        var r = rng(s.seed || 1978), days = [], harv = [], pay = [];
        for (k = 0; k < DAYS; k++) {
          var z = Math.sqrt(-2 * Math.log(r() + 1e-12)) * Math.cos(2 * Math.PI * r());
          var y = t.e + v.sigma * z;
          days.push(k + 1); harv.push(y); pay.push(t.accepts ? t.fixed + t.b * y : 0);
        }
        var c2 = g[1].axes({ x: [0, DAYS + 1], y: [-15, 35], title: "Forty days: the harvest (green) and Friday's pay " +
                             "(gold)", xlabel: "day" });
        c2.hline(0, { color: GREY_HINT });
        c2.dots(days, harv, { r: 3, color: function () { return GREEN; } });
        c2.dots(days, pay, { r: 3, color: function () { return GOLD; } });
        s.out = t;
      },
      readout: function (v, s) {
        var t = s.out;
        return [["Friday", t.accepts ? "takes the job" : "turns it down: raise the fixed pay"],
                ["Friday's effort", t.e.toFixed(2) + " baskets a day"],
                ["what the luck costs Friday", t.risk.toFixed(2) + " baskets a day"],
                ["your expected profit", t.profit.toFixed(2) + " baskets a day"],
                ["the best share, 1/(1 + r c sigma^2)", (100 * t.bstar).toFixed(0) + "%, earning " +
                   t.best.toFixed(2) + " (5.00 if you could see effort)"]];
      },
      note: "At the part's numbers (sd 5, r = 0.2) the best share is two-thirds and earns 3.33 baskets a day (Part 14, " +
            "chapter 1). Computed in your browser; nothing you do here is stored or sent.",
    });
  };
})();
