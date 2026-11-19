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
  // ---- Part 15: spillovers -------------------------------------------------------------------------------------
  W.pot = function (el) {
    // the shared pot of Part 15 (explainer.economics.agora.public.vcm): four islanders hold 20 shells each round; the
    // pot is multiplied by 4 m and shared equally.  The reader plays one seat; the other three are Agora's typed
    // players: a conditional cooperator, a free rider and a waverer who starts generous and copies the average
    var W0 = 20, NAMES = ["you", "cooperator", "free rider", "waverer"], COLS = [GOLD, GREEN, RED, BLUE];
    function others(s) {
      var h = s.hist, k = h.length;
      var lastAvg = k ? (h[k - 1][0] + h[k - 1][1] + h[k - 1][2] + h[k - 1][3]) / 4 : 14;
      var youLast = k ? h[k - 1][0] : 14;
      var cc = Math.min(W0, Math.max(0, (s.punish ? 1.05 : 0.8) * lastAvg));
      var fr = s.punished ? Math.min(W0, lastAvg) : 0;
      var wv = k ? Math.min(W0, Math.max(0, 0.5 * h[k - 1][3] + 0.5 * youLast * (s.punish ? 1.1 : 0.8))) : 16;
      return [cc, fr, wv];
    }
    QB.widget(el, {
      title: "Play the shared pot",
      sub: "Each round you and three islanders each hold 20 shells and choose, in secret, how many to put in a pot. " +
           "The pot is multiplied and shared equally among all four; you keep what you didn't put in. Play ten rounds " +
           "against Agora's typed players: a conditional cooperator, a free rider and a waverer. Then allow punishment " +
           "and play again.",
      panels: 2, height: 320, weights: [1.1, 1],
      controls: [
        { k: "give", label: "Shells you put in this round", min: 0, max: 20, step: 1, value: 10,
          fmt: function (x) { return x.toFixed(0); } },
        { k: "m", label: "Each shell in the pot returns to each player", min: 0.25, max: 0.75, step: 0.05,
          value: 0.4, fmt: function (x) { return x.toFixed(2) + " (the pot grows x" + (4 * x).toFixed(1) + ")"; } },
      ],
      buttons: [
        { label: "Play the round", act: function (s, v) {
            s.hist = s.hist || []; s.pay = s.pay || [0, 0, 0, 0];
            if (s.hist.length >= 10) return;
            var o = others(s), g = [v.give, o[0], o[1], o[2]];
            var pot = g[0] + g[1] + g[2] + g[3], k;
            for (k = 0; k < 4; k++) s.pay[k] += W0 - g[k] + v.m * pot;
            s.punished = false;
            if (s.punish) {
              var avg = pot / 4;
              if (g[2] < 0.6 * avg) { s.pay[2] -= 6; s.pay[1] -= 2; s.punished = true; }
              if (g[0] < 0.6 * avg) { s.pay[0] -= 6; s.pay[1] -= 2; }
            }
            s.hist.push(g);
          } },
        { label: "Start again", act: function (s) { s.hist = []; s.pay = [0, 0, 0, 0]; s.punished = false; } },
        { label: "Allow punishment (and start again)", act: function (s) {
            s.punish = !s.punish; s.hist = []; s.pay = [0, 0, 0, 0]; s.punished = false; } },
      ],
      draw: function (g, v, s) {
        s.hist = s.hist || []; s.pay = s.pay || [0, 0, 0, 0];
        var a = g[0].axes({ x: [0.5, 10.5], y: [0, 21], title: "Shells put in, round by round" +
                            (s.punish ? " (punishment allowed)" : ""), xlabel: "round" });
        var k, j;
        for (j = 0; j < 4; j++) {
          var xs = [], ys = [];
          for (k = 0; k < s.hist.length; k++) { xs.push(k + 1); ys.push(s.hist[k][j]); }
          if (xs.length > 1) a.line(xs, ys, { color: COLS[j], width: j === 0 ? 2.4 : 1.6 });
          if (xs.length) a.dots(xs, ys, { r: j === 0 ? 5 : 3.5, color: function () { return COLS[j]; } });
        }
        var b = g[1].axes({ x: [-0.5, 3.5], y: [0, 340], title: "Shells earned so far", xlabel: NAMES.join(" / ") });
        b.bars([0, 1, 2, 3], s.pay, 0.6, { color: function (i) { return COLS[i]; } });
        b.hline(10 * v.m * 4 * W0, { color: GREY_HINT, dash: [4, 4] });
      },
      readout: function (v, s) {
        var n = (s.hist || []).length, tot = (s.pay || [0, 0, 0, 0]).reduce(function (x, y) { return x + y; }, 0);
        return [["round", n + " of 10"], ["your shells so far", (s.pay ? s.pay[0] : 0).toFixed(1)],
                ["the four together", tot.toFixed(1)],
                ["if all four gave everything, every round", (4 * 10 * v.m * 4 * W0).toFixed(0) + " (dashed line: each)"],
                ["if nobody gave anything", (4 * 10 * W0).toFixed(0)]];
      },
      note: "With each shell returning 0.4 to each player, giving nothing is always best for you, and giving " +
            "everything best for the four (Part 15, chapter 1). Computed in your browser; nothing you do here is " +
            "stored or sent.",
    });
  };
  // ---- Part 16: auctions ---------------------------------------------------------------------------------------
  W.auction = function (el) {
    // the auction house of Part 16 (explainer.economics.agora.auctions): each round the reader draws a value for a
    // canoe, uniform on 0-100, and three rivals draw theirs; the rivals bid as the risk-neutral equilibrium says
    // (three quarters of their values when the winner pays its bid, their values when it pays the second bid); the
    // reader bids, and the page keeps score against the equilibrium bid played on the same draws
    var N = 20, RIV = 3, NAMES = ["you", "rival 1", "rival 2", "rival 3"], COLS = [GOLD, BLUE, GREEN, RED];
    function draw(s, k) {
      var r = rng((s.seed || 1) * 1009 + 7 * k + 3), out = [], i;
      for (i = 0; i <= RIV; i++) out.push(100 * r());
      return out;
    }
    function outcome(vals, bid, second) {
      var rb = [], i, top = -1, who = 0;
      for (i = 1; i <= RIV; i++) rb.push(second ? vals[i] : 0.75 * vals[i]);
      for (i = 0; i < RIV; i++) if (rb[i] > top) top = rb[i];
      var won = bid > top, price = won ? (second ? top : bid) : 0;
      return { won: won, price: price, profit: won ? vals[0] - price : 0, rivals: rb, top: top };
    }
    QB.widget(el, {
      title: "Bid for the canoe, twenty times",
      sub: "Each round you learn what the canoe is worth to you, between 0 and 100 shells; three rivals have values " +
           "of their own and bid as the theory says. Choose your bid and press Bid. The page keeps your score, and " +
           "the score of the theory's bid on the same draws. Switch the rule between paying your own bid and paying " +
           "the second-highest bid.",
      panels: 2, height: 320, weights: [1, 1.1],
      controls: [
        { k: "bid", label: "Your bid this round", min: 0, max: 100, step: 1, value: 50,
          fmt: function (x) { return x.toFixed(0) + " shells"; } },
      ],
      buttons: [
        { label: "Bid", act: function (s, v) {
            s.hist = s.hist || []; s.seed = s.seed || 1;
            if (s.hist.length >= N) return;
            var k = s.hist.length, vals = draw(s, k), second = !!s.second;
            var me = outcome(vals, v.bid, second);
            var eq = outcome(vals, second ? vals[0] : 0.75 * vals[0], second);
            s.hist.push({ vals: vals, bid: v.bid, me: me, eq: eq });
          } },
        { label: "Switch the rule (and start again)", act: function (s) {
            s.second = !s.second; s.hist = []; s.seed = (s.seed || 1) + 1; } },
        { label: "New draws (start again)", act: function (s) { s.hist = []; s.seed = (s.seed || 1) + 1; } },
      ],
      draw: function (g, v, s) {
        s.hist = s.hist || []; s.seed = s.seed || 1;
        var n = s.hist.length, last = n ? s.hist[n - 1] : null;
        var a = g[0].axes({ x: [-0.5, 3.5], y: [0, 100], title: last ? "Last round: values (pale) and bids" :
                            "Your value this round, and the rivals' (hidden until you bid)", xlabel: NAMES.join(" / ") });
        if (last) {
          a.bars([0, 1, 2, 3], last.vals, 0.7, { color: function () { return "rgba(200,200,200,0.25)"; } });
          a.bars([0, 1, 2, 3], [last.bid].concat(last.me.rivals), 0.4, { color: function (i) { return COLS[i]; } });
          if (last.me.won) a.hline(last.me.price, { color: GOLD, dash: [4, 4] });
        } else {
          a.bars([0], [draw(s, 0)[0]], 0.7, { color: function () { return GOLD; } });
        }
        var b = g[1].axes({ x: [0, N], y: [0, 160], title: "Shells earned so far" + (s.second ?
                            " (pay the second bid)" : " (pay your own bid)"), xlabel: "round" });
        var xs = [0], mine = [0], eqs = [0], k, cm = 0, ce = 0;
        for (k = 0; k < n; k++) { cm += s.hist[k].me.profit; ce += s.hist[k].eq.profit; xs.push(k + 1);
                                  mine.push(cm); eqs.push(ce); }
        if (n) { b.line(xs, eqs, { color: GREY_HINT, width: 1.6, dash: [5, 4] }); b.line(xs, mine, { color: GOLD, width: 2.4 }); }
        b.line([0, N], [0, 5 * N], { color: "rgba(139,147,161,0.35)", width: 1 });
      },
      readout: function (v, s) {
        var h = s.hist || [], n = h.length, nxt = n < N ? draw(s, n)[0] : null, cm = 0, ce = 0, k;
        for (k = 0; k < n; k++) { cm += h[k].me.profit; ce += h[k].eq.profit; }
        var eqBid = nxt === null ? null : (s.second ? nxt : 0.75 * nxt);
        var rows = [["rule", s.second ? "the winner pays the second-highest bid" : "the winner pays its own bid"],
                    ["round", Math.min(n + 1, N) + " of " + N],
                    ["your value this round", nxt === null ? "done" : nxt.toFixed(0) + " shells"],
                    ["the theory's bid for it", eqBid === null ? "-" : eqBid.toFixed(1)],
                    ["your shells so far", cm.toFixed(1)], ["the theory's bid, same draws", ce.toFixed(1)]];
        if (n) rows.push(["last round", h[n - 1].me.won ? "you won, paying " + h[n - 1].me.price.toFixed(1) :
                          "you lost (the top rival bid " + h[n - 1].me.top.toFixed(1) + ")"]);
        return rows;
      },
      note: "With four bidders and values uniform on 0-100, the theory's bid earns 5 shells a round on average under " +
            "either rule (the faint line): revenue equivalence for the bidder (Part 16, chapter 5). Computed in your " +
            "browser; nothing you do here is stored or sent.",
    });
  };
  // ---- Part 17: markets by design ------------------------------------------------------------------------------
  W.match = function (el) {
    // the workshops of Part 17 (explainer.economics.agora.matching: boston, deferred_acceptance): nine children,
    // three workshops (2, 3 and 4 places); the reader truly ranks the boatyard, then the kiln, then the net loft;
    // the eight others rank at random, with the boatyard as popular as the slider says; one lottery breaks ties.
    // For each of the six lists the reader could submit, the page plays 400 such markets under the chosen rule and
    // reports how the reader fares, measured by the TRUE ranking (3 points for the boatyard, 2 the kiln, 1 the loft)
    var SCH = ["boatyard", "kiln", "net loft"], CAP = [2, 3, 4], N = 9, M = 400;
    var LISTS = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]];
    var NAMES = LISTS.map(function (l) { return l.map(function (k) { return SCH[k].split(" ").pop(); }).join(" > "); });
    function others(r, pop) {
      // a random ranking with the boatyard first with probability pop, otherwise uniformly random
      var a = [0, 1, 2], i, j, t;
      for (i = 2; i > 0; i--) { j = Math.floor(r() * (i + 1)); t = a[i]; a[i] = a[j]; a[j] = t; }
      if (r() < pop) { a = [0].concat(a.filter(function (x) { return x !== 0; })); }
      return a;
    }
    function boston(pref, rank) {
      var left = CAP.slice(), got = new Array(N).fill(-1), k, s, i;
      for (k = 0; k < 3; k++) {
        for (s = 0; s < 3; s++) {
          var apps = [];
          for (i = 0; i < N; i++) if (got[i] < 0 && pref[i][k] === s) apps.push(i);
          apps.sort(function (x, y) { return rank[x] - rank[y]; });
          for (i = 0; i < apps.length && left[s] > 0; i++) { got[apps[i]] = s; left[s]--; }
        }
      }
      return got;
    }
    function da(pref, rank) {
      var next = new Array(N).fill(0), held = [[], [], []], free = [], i, changed = true;
      for (i = 0; i < N; i++) free.push(i);
      while (free.length) {
        var nf = [];
        free.forEach(function (i) {
          if (next[i] >= 3) return;
          var s = pref[i][next[i]++];
          held[s].push(i);
        });
        for (var s = 0; s < 3; s++) {
          held[s].sort(function (x, y) { return rank[x] - rank[y]; });
          while (held[s].length > CAP[s]) nf.push(held[s].pop());
        }
        free = nf.filter(function (i) { return next[i] < 3; });
      }
      var got = new Array(N).fill(-1);
      for (var t = 0; t < 3; t++) held[t].forEach(function (i) { got[i] = t; });
      return got;
    }
    function play(v, s) {
      var res = LISTS.map(function () { return { pts: 0, dist: [0, 0, 0, 0] }; }), m, li;
      for (m = 0; m < M; m++) {
        var r = rng((s.seed || 1) * 7919 + m * 31 + 7), pref = [null], rank = [], i;
        for (i = 1; i < N; i++) pref.push(others(r, v.pop));
        for (i = 0; i < N; i++) rank.push(r());
        for (li = 0; li < LISTS.length; li++) {
          pref[0] = LISTS[li];
          var got = (s.da ? da : boston)(pref, rank)[0];
          var pts = got < 0 ? 0 : 3 - got;              // the reader's TRUE ranking: boatyard 3, kiln 2, loft 1
          res[li].pts += pts / M;
          res[li].dist[got < 0 ? 3 : got] += 1 / M;
        }
      }
      return res;
    }
    QB.widget(el, {
      title: "Which list should you submit?",
      sub: "You truly prefer the boatyard, then the kiln, then the net loft. Eight other children rank the three " +
           "workshops too, and one lottery breaks ties. For each of the six lists you could submit, the page plays " +
           "400 markets and scores what you get by your true ranking. Change how popular the boatyard is, and " +
           "switch between the Boston rule and deferred acceptance.",
      panels: 2, height: 320, weights: [1.25, 1],
      controls: [
        { k: "pop", label: "Share of the others who put the boatyard first (beyond chance)", min: 0, max: 0.9,
          step: 0.05, value: 0.5, fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
      ],
      buttons: [
        { label: "Switch the rule", act: function (s) { s.da = !s.da; } },
        { label: "New markets", act: function (s) { s.seed = (s.seed || 1) + 1; } },
      ],
      draw: function (g, v, s) {
        var res = play(v, s);
        s.res = res;
        var a = g[0].axes({ x: [-0.6, 5.6], y: [0, 3], title: "Average result by your true ranking (" +
                            (s.da ? "deferred acceptance" : "the Boston rule") + ")", xlabel: NAMES.join("  |  ") });
        a.bars([0, 1, 2, 3, 4, 5], res.map(function (r) { return r.pts; }), 0.6,
               { color: function (i) { return i === 0 ? GREEN : (s.da ? BLUE : GOLD); } });
        var b = g[1].axes({ x: [-0.5, 3.5], y: [0, 1], title: "If you tell the truth: where you end up",
                            xlabel: "boatyard / kiln / net loft / nowhere" });
        b.bars([0, 1, 2, 3], res[0].dist, 0.6, { color: function (i) { return [GOLD, RED, GREEN, GREY_HINT][i]; } });
      },
      readout: function (v, s) {
        var res = s.res || [], best = 0, i;
        for (i = 1; i < res.length; i++) if (res[i].pts > res[best].pts + 1e-9) best = i;
        return [["rule", s.da ? "deferred acceptance (students asking)" : "the Boston rule"],
                ["the truth (green) scores", res.length ? res[0].pts.toFixed(2) : "-"],
                ["the best list scores", res.length ? res[best].pts.toFixed(2) + " (" + NAMES[best] + ")" : "-"],
                ["does a lie ever pay?", res.length ? (best === 0 ? "no: the truth is best" : "yes, here") : "-"]];
      },
      note: "Under deferred acceptance the truthful list always scores best, whatever the others do (Part 17, " +
            "chapter 6); under the Boston rule a safer list beats the truth when the boatyard is popular. Computed in " +
            "your browser; nothing you do here is stored or sent.",
    });
  };
})();
