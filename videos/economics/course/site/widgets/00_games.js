// Economics, Built: the game kit the parts' interactives share (QB.econ).  Every part's interactive is a game the
// reader plays against Agora's traders; the kit holds the engines.  A game keeps its state in the page's memory: no
// storage, no cookies, no network.
//
//   QB.econ.market(values, costs)          -> {v, c, q, lo, hi, p, surplus}: the competitive prediction
//   QB.econ.auction(mkt, opts)             -> periods of a continuous double auction (zip or zi traders),
//                                             with an optional human buyer who bids a fixed price
//   QB.econ.alpha(prices, p0)              -> Smith's (1962) coefficient of convergence, in percent
// The traders are a port of explainer/economics/agora/market.py (Cliff 1997; Gode and Sunder 1993).
(function () {
  "use strict";

  function market(values, costs) {
    var v = values.slice().sort(function (a, b) { return b - a; });
    var c = costs.slice().sort(function (a, b) { return a - b; });
    var n = Math.min(v.length, c.length), q = 0, k;
    for (k = 0; k < n; k++) if (v[k] >= c[k]) q++;
    var lo = q > 0 ? Math.max(c[q - 1], q < v.length ? v[q] : 0) : 0;
    var hi = q > 0 ? Math.min(v[q - 1], q < c.length ? c[q] : 5) : 0;
    var s = 0;
    for (k = 0; k < q; k++) s += v[k] - c[k];
    return { v: v, c: c, q: q, lo: lo, hi: hi, p: (lo + hi) / 2, surplus: s, values: values, costs: costs };
  }

  function alpha(prices, p0) {
    if (!prices.length || !(p0 > 0)) return 0;
    var s = 0;
    for (var i = 0; i < prices.length; i++) s += (prices[i] - p0) * (prices[i] - p0);
    return 100 * Math.sqrt(s / prices.length) / p0;
  }

  function Trader(kind, side, limit, rnd) {
    this.kind = kind; this.side = side; this.limit = limit; this.rnd = rnd; this.active = true;
    if (kind === "zip") {
      var mu = 0.05 + 0.3 * rnd();
      this.margin = side === "sell" ? mu : -mu;
      this.beta = 0.1 + 0.4 * rnd(); this.gamma = 0.1 * rnd(); this.momentum = 0;
    }
  }
  Trader.prototype.quote = function (floor, ceiling) {
    if (this.kind === "human") return this.limit;
    if (this.kind === "zi") return this.side === "buy" ? floor + (this.limit - floor) * this.rnd() : this.limit + (ceiling - this.limit) * this.rnd();
    return this.limit * (1 + this.margin);
  };
  Trader.prototype.move = function (target) {
    var p = this.limit * (1 + this.margin), d = this.beta * (target - p);
    this.momentum = this.gamma * this.momentum + (1 - this.gamma) * d;
    var m = (p + this.momentum) / this.limit - 1;
    this.margin = this.side === "sell" ? Math.max(0, m) : Math.min(0, Math.max(-1, m));
  };
  Trader.prototype.learn = function (price, side, dealt) {
    if (this.kind !== "zip") return;
    var r = this.rnd, p = this.limit * (1 + this.margin);
    var up = price * (1 + 0.05 * r()) + 0.05 * r(), down = price * (1 - 0.05 * r()) - 0.05 * r();
    if (this.side === "sell") {
      if (dealt) { if (p <= price) this.move(up); else if (side === "buy" && this.active) this.move(down); }
      else if (side === "sell" && p >= price && this.active) this.move(down);
    } else {
      if (dealt) { if (p >= price) this.move(down); else if (side === "sell" && this.active) this.move(up); }
      else if (side === "buy" && p <= price && this.active) this.move(up);
    }
  };

  // opts: {kind: "zip" | "zi", periods, seed, human: index of the buyer the reader plays (or -1), bid: the reader's
  // price (they bid it, and take any offer at or below it), floor, ceiling}
  function auction(mkt, opts) {
    var rnd = QB.rng(opts.seed || 1), floor = opts.floor || 0, ceiling = opts.ceiling || 5;
    var human = opts.human === undefined ? -1 : opts.human;
    var buyers = mkt.values.map(function (v, i) {
      return new Trader(i === human ? "human" : opts.kind, "buy", i === human ? Math.min(opts.bid, v) : v, rnd);
    });
    var sellers = mkt.costs.map(function (c) { return new Trader(opts.kind, "sell", c, rnd); });
    var out = [];
    for (var per = 0; per < (opts.periods || 6); per++) {
      var i, t; for (i = 0; i < buyers.length; i++) buyers[i].active = true; for (i = 0; i < sellers.length; i++) sellers[i].active = true;
      var bb = null, ba = null, trades = [], idle = 0;
      for (var step = 0; step < 600 && idle <= 120; step++) {
        var live = [];
        for (i = 0; i < buyers.length; i++) if (buyers[i].active) live.push(["buy", i]);
        for (i = 0; i < sellers.length; i++) if (sellers[i].active) live.push(["sell", i]);
        if (!live.length) break;
        var pick = live[Math.floor(rnd() * live.length)], side = pick[0], k = pick[1];
        t = side === "buy" ? buyers[k] : sellers[k];
        var q = t.quote(floor, ceiling), dealt = false, price = q;
        if (side === "buy") {
          if (ba && q >= ba[0]) {
            price = ba[0];
            trades.push({ price: price, value: mkt.values[k], cost: mkt.costs[ba[1]], human: k === human });
            buyers[k].active = false; sellers[ba[1]].active = false; bb = ba = null; dealt = true;
          } else if (!bb || q > bb[0]) bb = [q, k];
        } else {
          if (bb && q <= bb[0]) {
            price = bb[0];
            trades.push({ price: price, value: mkt.values[bb[1]], cost: mkt.costs[k], human: bb[1] === human });
            buyers[bb[1]].active = false; sellers[k].active = false; bb = ba = null; dealt = true;
          } else if (!ba || q < ba[0]) ba = [q, k];
        }
        idle = dealt ? 0 : idle + 1;
        for (i = 0; i < buyers.length; i++) buyers[i].learn(price, side, dealt);
        for (i = 0; i < sellers.length; i++) sellers[i].learn(price, side, dealt);
      }
      var prices = trades.map(function (x) { return x.price; }), gain = 0, mine = null;
      for (i = 0; i < trades.length; i++) { gain += trades[i].value - trades[i].cost; if (trades[i].human) mine = trades[i].price; }
      out.push({ trades: trades, prices: prices, alpha: alpha(prices, mkt.p), efficiency: mkt.surplus > 0 ? gain / mkt.surplus : 0, mine: mine });
    }
    return out;
  }

  QB.econ = { market: market, auction: auction, alpha: alpha };
})();
