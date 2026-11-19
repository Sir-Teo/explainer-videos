// Interactives for Act I, The Question (Parts 1-4).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;
  var BLUE = "#5DADEC", AMBER = "#F2B84B", ORANGE = "#FF9F5A", GOLD = "#F6C453", GREY_HINT = "#8B93A1";

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
        { k: "periods", label: "Periods", min: 1, max: 10, step: 1, value: 6 },
      ],
      buttons: [
        { label: "The others learn (Cliff's traders)", act: function (s) { s.zi = false; } },
        { label: "The others bid at random (zero intelligence)", act: function (s) { s.zi = true; } },
        { label: "New market (reshuffle who calls when)", act: function (s) { s.seed = (s.seed * 7919 + 13) % 100003 || 1; } },
      ],
      draw: function (g, v, s) {
        var res = QB.econ.auction(mkt, { kind: s.zi ? "zi" : "zip", periods: v.periods, seed: s.seed, human: YOU, bid: v.bid });
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
        a.text(xmax - 0.3, mkt.lo - 0.1, "the competitive band, $" + mkt.lo.toFixed(2) + " to $" + mkt.hi.toFixed(2),
               { color: GOLD, align: "right", size: 11, bg: true });
        a.legend([["a deal", C.ink], ["your deal", GOLD]], { pos: "tr" });
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
        s.out = { zi: !!s.zi, alpha: last.alpha, eff: last.efficiency, n: n, periods: res.length, earned: earned,
                  mean: last.prices.length ? QB.mean(last.prices) : 0 };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["the others", o.zi ? "bid at random" : "learn"], ["you traded in", o.n + " of " + o.periods + " periods"], ["you kept, all periods", "$" + fmt(o.earned, 2)],
                ["last period: mean price", o.mean ? "$" + fmt(o.mean, 2) : "no deals"], ["Smith's alpha", fmt(o.alpha, 1) + "%"],
                ["share of the possible gain", QB.pct(o.eff, 0)]];
      },
      note: "Simulated traders: a port of Agora's market (explainer/economics/agora/market.py), Cliff's margin-adjusting " +
            "traders or Gode and Sunder's zero-intelligence ones, as in the film. The competitive band is computed from " +
            "the twenty cards. Nothing you do here is stored or sent.",
    });
  };

  // ---- Part 2: who pays the tax? ----------------------------------------------------------------------------------
  W.scissors = function (el) {
    var V0 = [3.40, 3.10, 2.90, 2.70, 2.50, 2.30, 2.10, 1.90, 1.70, 1.50];
    var C0 = [1.20, 1.40, 1.60, 1.80, 2.00, 2.20, 2.40, 2.60, 2.80, 3.00];
    var PINK = "#E9A3C9", RED = "#F26D6D";
    function cards(kd, ks) {
      return { v: V0.map(function (x) { return 2.25 + kd * (x - 2.25); }),
               c: C0.map(function (x) { return 2.25 + ks * (x - 2.25); }) };
    }
    QB.widget(el, {
      title: "Who pays the tax? Predict, then let the pit trade",
      sub: "Part 1's twenty cards, with a tax on every unit sold. Make the buyers' cards or the sellers' cards more " +
           "alike (a flatter staircase: they respond more to price) or more spread out (steeper). Choose who hands " +
           "the tax to the government, make your prediction with a button, and watch where the learning traders " +
           "settle. A legal maximum price, if you set one below the market, shows what a cap costs.",
      panels: 2, height: 320,
      controls: [
        { k: "tax", label: "Tax per unit", min: 0, max: 0.8, step: 0.05, value: 0.4, fmt: function (x) { return "$" + x.toFixed(2); } },
        { k: "kd", label: "Buyers' cards: alike (left) or spread (right)", min: 0.3, max: 2.0, step: 0.1, value: 1.0,
          fmt: function (x) { return "x" + x.toFixed(1); } },
        { k: "ks", label: "Sellers' cards: alike (left) or spread (right)", min: 0.3, max: 2.0, step: 0.1, value: 1.0,
          fmt: function (x) { return "x" + x.toFixed(1); } },
        { k: "cap", label: "Legal maximum price (off at $3.50)", min: 1.5, max: 3.5, step: 0.05, value: 3.5,
          fmt: function (x) { return x >= 3.5 ? "none" : "$" + x.toFixed(2); } },
      ],
      buttons: [
        { label: "Sellers remit the tax", act: function (s) { s.on = "sell"; } },
        { label: "Buyers remit the tax", act: function (s) { s.on = "buy"; } },
        { label: "I predict: buyers bear more", act: function (s) { s.guess = "buyers"; } },
        { label: "I predict: sellers bear more", act: function (s) { s.guess = "sellers"; } },
      ],
      draw: function (g, v, s) {
        var on = s.on || "sell", cd = cards(v.kd, v.ks), mkt = QB.econ.market(cd.v, cd.c);
        var cap = v.cap >= 3.5 ? null : v.cap, i, k, r;
        var paid = [], rec = [], eff = [], n = [], dots = [];
        for (r = 0; r < 6; r++) {
          var res = QB.econ.auction(mkt, { kind: "zip", periods: 6, seed: 17 + 31 * r + (s.seed || 1), tax: v.tax,
                                           taxOn: on, cap: cap });
          var last = res[res.length - 1];
          if (last.trades.length) {
            paid.push(QB.mean(last.trades.map(function (t) { return t.paid; })));
            rec.push(QB.mean(last.trades.map(function (t) { return t.received; })));
          }
          eff.push(last.efficiency); n.push(last.trades.length);
          if (r === 0) for (k = 0; k < res.length; k++) for (i = 0; i < res[k].trades.length; i++)
            dots.push([k + (i + 0.5) / Math.max(res[k].trades.length, 1), res[k].trades[i].paid, res[k].trades[i].received]);
        }
        var a = g[0].axes({ x: [0, 10], y: [0, 5], title: "The cards, and the tax as a wedge", xlabel: "units" });
        var dx = [], dy = [], sx = [], sy = [], tx = [], ty = [];
        for (i = 0; i < 10; i++) {
          dx.push(i, i + 1); dy.push(mkt.v[i], mkt.v[i]); sx.push(i, i + 1); sy.push(mkt.c[i], mkt.c[i]);
          if (on === "sell") { tx.push(i, i + 1); ty.push(mkt.c[i] + v.tax, mkt.c[i] + v.tax); }
          else { tx.push(i, i + 1); ty.push(mkt.v[i] - v.tax, mkt.v[i] - v.tax); }
        }
        a.area([0, 10], [mkt.hi, mkt.hi], mkt.lo, { color: GOLD, alpha: 0.18 });
        a.line(dx, dy, { color: BLUE, width: 2.4 }).line(sx, sy, { color: AMBER, width: 2.4 });
        if (v.tax > 0) a.line(tx, ty, { color: PINK, width: 2, dash: [5, 4] });
        if (cap) a.hline(cap, { color: RED, width: 2, dash: [] });
        var mp = paid.length ? QB.mean(paid) : NaN, mr = rec.length ? QB.mean(rec) : NaN;
        if (isFinite(mp)) a.hline(mp, { color: BLUE, dash: [2, 3] });
        if (isFinite(mr)) a.hline(mr, { color: AMBER, dash: [2, 3] });
        a.legend([["demand", BLUE], ["supply", AMBER], [on === "sell" ? "supply plus the tax" : "demand less the tax", PINK]],
                 { pos: "tr" });
        var b = g[1].axes({ x: [0, 6], y: [0, 5], title: "Every deal: what buyers paid (blue), sellers kept (amber)",
                            xlabel: "period" });
        b.area([0, 6], [mkt.hi, mkt.hi], mkt.lo, { color: GOLD, alpha: 0.18 });
        b.dots(dots.map(function (d) { return d[0]; }), dots.map(function (d) { return d[1]; }), { color: BLUE, r: 3 });
        b.dots(dots.map(function (d) { return d[0]; }), dots.map(function (d) { return d[2]; }), { color: AMBER, r: 3 });
        var p0 = mkt.p, share = v.tax > 0 && isFinite(mp) ? (mp - p0) / v.tax : NaN;
        s.out = { on: on, paid: mp, rec: mr, p0: p0, share: share, eff: QB.mean(eff), n: QB.mean(n), q0: mkt.q,
                  guess: s.guess, cap: cap, lo: mkt.lo, hi: mkt.hi };
      },
      readout: function (v, s) {
        var o = s.out, rows = [["tax remitted by", o.on === "sell" ? "sellers" : "buyers"],
                               ["before the tax", o.q0 + " units at $" + fmt(o.lo, 2) + " to $" + fmt(o.hi, 2)]];
        if (isFinite(o.paid)) rows.push(["buyers pay", "$" + fmt(o.paid, 2)], ["sellers keep", "$" + fmt(o.rec, 2)]);
        rows.push(["units traded", fmt(o.n, 1)], ["share of the gains made", QB.pct(o.eff, 0)]);
        if (isFinite(o.share)) {
          var even = Math.abs(o.share - 0.5) < 0.07, who = o.share > 0.5 ? "buyers" : "sellers";
          rows.push(["buyers' share of the tax", QB.pct(Math.max(0, Math.min(1, o.share)), 0)]);
          if (o.guess) rows.push(["your prediction", o.guess + (even ? ": about even, so neither side bears much more" :
                                                                o.guess === who ? ": right" : ": not this time")]);
        }
        return rows;
      },
      note: "Simulated traders: Agora's learning traders (Cliff 1997), six markets of six periods each, the last period " +
            "averaged. Switch who remits the tax and the two dashed price lines barely move: the burden does not " +
            "follow the cheque. Nothing you do here is stored or sent.",
    });
  };

  // ---- Part 3: two baskets, and a chain --------------------------------------------------------------------------
  W.measure = function (el) {
    var GREEN = "#7BD88F", PAAS = "#6FC3F2", LASP = "#F28C6F", FISH = "#6FB7E8";
    // a homothetic (CES) consumer: base expenditure shares s0, price relatives r, elasticity of substitution sig
    function indexes(r, s0, sig) {
      var L = 0, i, s1 = [], w = [], tw = 0, P = 0, tr;
      for (i = 0; i < r.length; i++) L += s0[i] * r[i];
      if (Math.abs(sig - 1) < 1e-6) {
        tr = 0;
        for (i = 0; i < r.length; i++) { s1.push(s0[i]); tr += s0[i] * Math.log(r[i]); }
        tr = Math.exp(tr);
      } else {
        for (i = 0; i < r.length; i++) { w.push(s0[i] * Math.pow(r[i], 1 - sig)); tw += w[i]; }
        for (i = 0; i < r.length; i++) s1.push(w[i] / tw);
        tr = Math.pow(tw, 1 / (1 - sig));
      }
      for (i = 0; i < r.length; i++) P += s1[i] / r[i];
      P = 1 / P;
      return { L: L, P: P, F: Math.sqrt(L * P), T: tr, s1: s1 };
    }
    QB.widget(el, {
      title: "Bo's two baskets: how much dearer is living?",
      sub: "Bo spends $100 a week on fish and coconuts. A stormy year multiplies the price of fish; coconuts stay at $1. " +
           "Set how much fish costs, how much of his budget goes on fish, and how easily he switches between the two " +
           "(0: never; 1: he always spends the same share; 2: he switches readily). Guess where the true rise in his " +
           "cost of living lies, then see the named indexes against the truth, and chain them over seasons of storms.",
      panels: 2, height: 320,
      controls: [
        { k: "r", label: "Fish price in the stormy year (calm = $2)", min: 1.0, max: 4.0, step: 0.1, value: 2.0,
          fmt: function (x) { return "x" + x.toFixed(1) + " ($" + (2 * x).toFixed(2) + ")"; } },
        { k: "share", label: "Share of Bo's budget on fish (calm year)", min: 0.1, max: 0.9, step: 0.05, value: 0.5,
          fmt: function (x) { return QB.pct(x, 0); } },
        { k: "sig", label: "How easily Bo switches (elasticity of substitution)", min: 0.0, max: 2.0, step: 0.1, value: 1.0,
          fmt: function (x) { return x.toFixed(1); } },
        { k: "seasons", label: "Seasons in the chain (calm, storm, calm, ...)", min: 2, max: 20, step: 2, value: 12 },
      ],
      buttons: [
        { label: "I guess: as much as the fish price rose", act: function (s) { s.guess = "fish"; } },
        { label: "I guess: Laspeyres is right", act: function (s) { s.guess = "L"; } },
        { label: "I guess: between Paasche and Laspeyres", act: function (s) { s.guess = "between"; } },
        { label: "I guess: Paasche is right", act: function (s) { s.guess = "P"; } },
      ],
      draw: function (g, v, s) {
        var r = [v.r, 1], s0 = [v.share, 1 - v.share], x = indexes(r, s0, v.sig), i;
        var vals = [x.L, x.P, x.F, x.T].map(function (z) { return 100 * (z - 1); });
        var top = Math.max(5, 100 * (v.r - 1) * 1.05);
        var a = g[0].axes({ x: [0, 4], y: [0, top], title: "The rise in Bo's cost of living, %", xlabel: "" });
        a.bars([0.5, 1.5, 2.5, 3.5], vals, 0.6, { color: function (i) { return [LASP, PAAS, GOLD, GREEN][i]; } });
        a.hline(100 * (v.r - 1), { color: FISH, dash: [5, 4] });
        a.text(0.5, vals[0], "Laspeyres " + fmt(vals[0], 1) + "%", { color: LASP, align: "center", dy: -8 });
        a.text(1.5, vals[1], "Paasche " + fmt(vals[1], 1) + "%", { color: PAAS, align: "center", dy: -8 });
        a.text(2.5, vals[2], "Fisher " + fmt(vals[2], 1) + "%", { color: GOLD, align: "center", dy: -8 });
        a.text(3.5, vals[3], "true " + fmt(vals[3], 1) + "%", { color: GREEN, align: "center", dy: -8 });
        a.legend([["the fish price's own rise", FISH]], { pos: "tl" });
        // chain over seasons: storms come and go, prices end where they began
        var n = v.seasons, cl = [1], cp = [1], cf = [1], ct = [1], xs = [0], k;
        for (k = 1; k <= n; k++) {
          var up = k % 2 === 1, rr = up ? [v.r, 1] : [1 / v.r, 1];
          var base = up ? s0 : indexes([v.r, 1], s0, v.sig).s1;
          var y = indexes(rr, base, v.sig);
          cl.push(cl[k - 1] * y.L); cp.push(cp[k - 1] * y.P); cf.push(cf[k - 1] * y.F); ct.push(ct[k - 1] * y.T);
          xs.push(k);
        }
        var ymax = Math.max(1.2, Math.max.apply(null, cl) * 1.08), ymin = Math.min(0.8, Math.min.apply(null, cp) * 0.92);
        var b = g[1].axes({ x: [0, n], y: [Math.max(0.05, ymin), ymax], title: "Chained over " + n + " seasons", xlabel: "season" });
        b.hline(1, { color: GREY_HINT, dash: [3, 3] });
        b.line(xs, cl, { color: LASP, width: 2.2 }).line(xs, cp, { color: PAAS, width: 2.2 })
         .line(xs, cf, { color: GOLD, width: 2.2, dash: [6, 4] }).line(xs, ct, { color: GREEN, width: 2.6 });
        b.legend([["Laspeyres", LASP], ["Paasche", PAAS], ["Fisher", GOLD], ["true", GREEN]], { pos: "tl" });
        s.out = { L: x.L, P: x.P, F: x.F, T: x.T, r: v.r, guess: s.guess, cl: cl[n], cp: cp[n], cf: cf[n], ct: ct[n], n: n };
      },
      readout: function (v, s) {
        var o = s.out, rows = [
          ["Laspeyres (the calm basket)", "+" + fmt(100 * (o.L - 1), 1) + "%"],
          ["Paasche (the stormy basket)", "+" + fmt(100 * (o.P - 1), 1) + "%"],
          ["Fisher (their geometric mean)", "+" + fmt(100 * (o.F - 1), 1) + "%"],
          ["the truth, for Bo's tastes", "+" + fmt(100 * (o.T - 1), 1) + "%"],
          ["after " + o.n + " seasons: Laspeyres / Paasche / Fisher", fmt(o.cl, 3) + " / " + fmt(o.cp, 3) + " / " + fmt(o.cf, 3)],
        ];
        if (o.guess) {
          var ok = { fish: Math.abs(o.T - o.r) < 1e-6, L: Math.abs(o.T - o.L) < 1e-6, P: Math.abs(o.T - o.P) < 1e-6,
                     between: o.T >= o.P - 1e-9 && o.T <= o.L + 1e-9 }[o.guess];
          rows.push(["your guess", ok ? "right" : "not this time: the truth is +" + fmt(100 * (o.T - 1), 1) + "%"]);
        }
        return rows;
      },
      note: "A homothetic consumer: the true index always lies between Paasche and Laspeyres (Konus 1924), and Fisher " +
            "is close to it; with no switching at all the three coincide, and chain drift needs switching. Computed in " +
            "your browser; nothing you do here is stored or sent.",
    });
  };
})();
