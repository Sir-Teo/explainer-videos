// Interactives for Computer Science, Built, Parts 48-53: system design, reliability, graphics, numerics, quantum computation.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  function heading(c, box, str) { // a panel title in the place Axes puts one
    c.save(); c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
    c.fillText(str, box.x + 12, box.y + 6); c.restore();
  }

  // ---- Part 48: Che's approximation against a simulated LRU cache ----------------------------------------------
  W.chezipf = function (el) {
    var N = 1000, REQ = 12000, WARM = 3000, SIZES = [10, 20, 40, 80, 160, 320, 500];
    var popularity = function (s) { var p = [], t = 0, i; for (i = 1; i <= N; i++) { p.push(Math.pow(i, -s)); t += p[i - 1]; } for (i = 0; i < N; i++) p[i] /= t; return p; };
    var cheT = function (p, c) { // the characteristic time: sum_i (1 - exp(-p_i T)) = c, by bisection
      var lo = 0, hi = 1, k, i, sum, mid;
      var filled = function (T) { sum = 0; for (i = 0; i < N; i++) sum += 1 - Math.exp(-p[i] * T); return sum; };
      for (k = 0; k < 60 && filled(hi) < c; k++) hi *= 2;
      for (k = 0; k < 30; k++) { mid = (lo + hi) / 2; if (filled(mid) < c) lo = mid; else hi = mid; }
      return (lo + hi) / 2;
    };
    var cheHit = function (p, T) { var h = 0, i; for (i = 0; i < N; i++) h += p[i] * (1 - Math.exp(-p[i] * T)); return h; };
    var lru = function (trace, c, occ) { // hit rate after the warm-up; occ[i] counts the samples that found item i cached
      var prev = new Int32Array(N + 2), next = new Int32Array(N + 2), inside = new Uint8Array(N), size = 0, hits = 0, t, x, v, i;
      var HEAD = N, TAIL = N + 1; next[HEAD] = TAIL; prev[TAIL] = HEAD;
      for (t = 0; t < trace.length; t++) {
        x = trace[t];
        if (inside[x]) { if (t >= WARM) hits++; next[prev[x]] = next[x]; prev[next[x]] = prev[x]; }
        else { inside[x] = 1; size++; if (size > c) { v = prev[TAIL]; prev[TAIL] = prev[v]; next[prev[v]] = TAIL; inside[v] = 0; size--; } }
        next[x] = next[HEAD]; prev[x] = HEAD; prev[next[HEAD]] = x; next[HEAD] = x;
        if (occ && t >= WARM && t % 30 === 0) for (i = 0; i < N; i++) occ[i] += inside[i];
      }
      return hits / (trace.length - WARM);
    };
    QB.widget(el, {
      title: "One number predicts a cache: Che's approximation against LRU",
      sub: "A thousand items with Zipf popularity are requested 12,000 times. Gold is Che's formula, blue dots are a simulated LRU cache, grey is the best fixed set. Change the size and the skew: the formula follows. Then make requests repeat recent ones, which breaks the independence it assumes, and watch LRU pull above it.",
      panels: 2, height: 300,
      controls: [
        { k: "c", label: "Cache size C (entries)", min: 10, max: 500, step: 10, value: 100 },
        { k: "s", label: "Zipf exponent s", min: 0.4, max: 1.4, step: 0.05, value: 0.9, fmt: function (x) { return x.toFixed(2); } },
        { k: "rep", label: "Requests that repeat one of the last 50", min: 0, max: 60, step: 5, value: 0, fmt: function (x) { return x + "%"; } },
      ],
      buttons: [{ label: "New trace", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var p = popularity(v.s), r = QB.rng(s.seed + 480), cum = [], acc = 0, i, k, trace = [];
        for (i = 0; i < N; i++) { acc += p[i]; cum.push(acc); }
        for (k = 0; k < REQ; k++) {
          if (k >= 50 && r() < v.rep / 100) { trace.push(trace[k - 1 - Math.floor(r() * 50)]); continue; }
          var u = r(), lo = 0, hi = N - 1;
          while (lo < hi) { var m = (lo + hi) >> 1; if (cum[m] < u) lo = m + 1; else hi = m; }
          trace.push(lo);
        }
        var cs = [], che = [], stat = [], sim = [];
        for (k = 0; k <= 16; k++) { var c = Math.round(10 * Math.pow(50, k / 16)); cs.push(c); che.push(cheHit(p, cheT(p, c))); stat.push(cum[c - 1]); }
        for (k = 0; k < SIZES.length; k++) sim.push(lru(trace, SIZES[k], null));
        var occ = new Float64Array(N), T = cheT(p, v.c), here = lru(trace, v.c, occ), samples = Math.floor((REQ - WARM) / 30);
        s.out = [cheHit(p, T), here, cum[v.c - 1], T];
        var pc = function (y) { return Math.round(100 * y) + "%"; };
        var a = g[0].axes({ x: [10, 500], y: [0, 1], logx: true, xticks: [10, 30, 100, 300, 500], title: "Hit rate against cache size", xlabel: "cache size (entries)", yfmt: pc });
        a.line(cs, stat, { color: C.cash, dash: [4, 4], width: 1.3 }).line(cs, che, { color: C.idea, width: 2 });
        a.dots(SIZES, sim, { color: C.spot, r: 3.2 }).dots([v.c], [here], { color: C.spot, r: 5.5 });
        a.vline(v.c, { color: C.muted });
        a.legend([["Che's formula", C.idea], ["simulated LRU", C.spot], ["best fixed set", C.cash]], { pos: "tl" });
        var ranks = [], pin = [], bx = [], by = [], e;
        for (i = 1; i <= N; i = Math.max(i + 1, Math.round(i * 1.12))) { ranks.push(i); pin.push(1 - Math.exp(-p[i - 1] * T)); }
        for (e = 0; e < 12; e++) { // simulated occupancy, averaged over ranks in a logarithmic bin
          var a0 = Math.round(Math.pow(N, e / 12)), a1 = Math.max(a0 + 1, Math.round(Math.pow(N, (e + 1) / 12))), sum = 0;
          for (i = a0; i < a1; i++) sum += occ[i - 1];
          bx.push(Math.sqrt(a0 * (a1 - 1))); by.push(sum / (a1 - a0) / Math.max(1, samples));
        }
        var b = g[1].axes({ x: [1, N], y: [0, 1], logx: true, title: "Chance that the item of each rank is cached", xlabel: "popularity rank", yfmt: pc });
        b.line([1, v.c, v.c, N], [1, 1, 0, 0], { color: C.cash, dash: [4, 4], width: 1.3 });
        b.line(ranks, pin, { color: C.idea, width: 2 }).dots(bx, by, { color: C.spot, r: 3.2 });
        b.text(N, 0.92, "1 − exp(−pT)", { color: C.idea, align: "right", dx: -8, bg: true });
      },
      readout: function (v, s) {
        return [["Che predicts", QB.pct(s.out[0])], ["simulated LRU", QB.pct(s.out[1])], ["best fixed set", QB.pct(s.out[2])], ["characteristic time T", fmt(s.out[3], 0) + " requests"]];
      },
      note: "Simulated data. The first 3,000 requests warm the cache and are not counted. Che's approximation assumes independent references: each request is drawn from the popularities whatever came before. A repeated request keeps the same popularities but not the independence, and recency then helps LRU.",
    });
  };

  // ---- Part 49: a news feed's hybrid fan-out over a power-law follower graph ---------------------------------
  W.fanoutcut = function (el) {
    var U = 100000, FM = 20, M = U - 1, P = 0.5; // users, least followers, the cap, posts per user a day
    var tail = function (al, tau) { // E[F; F >= tau] for P(F > x) = (FM/x)^(al-1), capped at M
      var a2 = Math.abs(al - 2) < 1e-6 ? 2.0001 : al, t = Math.min(Math.max(tau, FM), M);
      return Math.pow(FM, a2 - 1) * ((a2 - 1) * Math.pow(t, 2 - a2) - Math.pow(M, 2 - a2)) / (a2 - 2);
    };
    var big = function (y) { return y >= 1e9 ? (y / 1e9).toFixed(1) + " bn" : y >= 1e6 ? (y / 1e6).toFixed(1) + " M" : Math.round(y / 1e3) + " k"; };
    QB.widget(el, {
      title: "Push, pull, and where to cut: a feed's fan-out",
      sub: "100,000 users post half a time a day; follower counts follow a power law from 20 upwards. Accounts below the threshold are pushed into their followers' timelines (blue), the rest are pulled at read time (orange). Slide the threshold: with many reads per post the total only falls as more is pushed. Then make reads rarer than posts and the slope turns over.",
      panels: 2, height: 300,
      controls: [
        { k: "lt", label: "Pull accounts with at least", min: 1.3, max: 5, step: 0.05, value: 4, fmt: function (x) { return Math.round(Math.pow(10, x)).toLocaleString("en") + " followers"; } },
        { k: "lr", label: "Timeline reads per post", min: -1, max: 2, step: 0.05, value: 1.6, fmt: function (x) { var r = Math.pow(10, x); return r < 10 ? r.toFixed(1) : r.toFixed(0); } },
        { k: "al", label: "Power-law exponent α", min: 1.65, max: 2.95, step: 0.05, value: 2.1, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var r = P * Math.pow(10, v.lr), tau = Math.pow(10, v.lt), EF = tail(v.al, FM), i, ts = [], push = [], pull = [], tot = [], share = [], acc = [];
        for (i = 0; i <= 74; i++) {
          var t = Math.pow(10, 1.3 + 3.7 * i / 74), hi = tail(v.al, t);
          ts.push(t); push.push(U * P * (EF - hi)); pull.push(U * r * hi); tot.push(push[i] + pull[i]);
          share.push(hi / EF); acc.push(Math.pow(FM / t, v.al - 1));
        }
        var h = tail(v.al, tau), now = U * (P * (EF - h) + r * h), pushAll = U * P * EF, pullAll = U * r * EF;
        s.out = [now, pushAll, pullAll, Math.round(U * Math.pow(FM / Math.max(tau, FM), v.al - 1)), h / EF, Math.min(tau, M)];
        var lo = Math.min(pushAll, pullAll) / 30, top = Math.max(pushAll, pullAll) * 3;
        lo = Math.pow(10, Math.floor(Math.log10(lo))); top = Math.pow(10, Math.ceil(Math.log10(top)));
        var clampv = function (arr) { return arr.map(function (y) { return Math.max(y, lo); }); };
        var a = g[0].axes({ x: [20, 100000], y: [lo, top], logx: true, logy: true, xticks: [100, 1000, 10000, 100000], xfmt: function (x) { return x >= 1000 ? x / 1000 + "k" : String(x); }, title: "Operations a day against the threshold", xlabel: "pull accounts with at least this many followers",
          yfmt: function (y) { return y >= 1e9 ? y / 1e9 + "bn" : y >= 1e6 ? y / 1e6 + "M" : y / 1e3 + "k"; } });
        a.line(ts, clampv(push), { color: C.spot, width: 1.5 }).line(ts, clampv(pull), { color: C.implied, width: 1.5 }).line(ts, tot, { color: C.idea, width: 2.4 });
        a.vline(tau, { color: C.muted }).dots([tau], [now], { color: C.idea, r: 5 });
        a.legend([["total", C.idea], ["pushed writes", C.spot], ["pulled fetches", C.implied]], { pos: "bl" });
        var b = g[1].axes({ x: [20, 100000], y: [0, 1], logx: true, xticks: [100, 1000, 10000, 100000], xfmt: function (x) { return x >= 1000 ? x / 1000 + "k" : String(x); }, title: "Who is above the threshold", xlabel: "threshold (followers)", yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.line(ts, share, { color: C.implied, width: 2 }).line(ts, acc, { color: C.q, width: 2 });
        b.vline(tau, { color: C.muted });
        b.legend([["share of all follows", C.implied], ["share of accounts", C.q]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["hybrid", big(s.out[0]) + " a day"], ["push all", big(s.out[1])], ["pull all", big(s.out[2])], ["accounts pulled", s.out[3].toLocaleString("en")],
          ["their share of follows", QB.pct(s.out[4])], ["worst post", Math.round(s.out[5]).toLocaleString("en") + " writes"]];
      },
      note: "Closed form for a Pareto law capped at 99,999 followers; every operation costs the same. The total is U[p·E(F; F < τ) + r·E(F; F ≥ τ)]: it falls with τ whenever r > p, so the count alone never picks an interior threshold. What the hybrid buys is the last readout, the bound on one post's fan-out.",
    });
  };

  // ---- Part 50: a retry storm that outlasts its trigger ------------------------------------------------------
  W.retrystorm = function (el) {
    var CAP = 100, T = 100, T0 = 20, TIMEOUT = 1;
    var storm = function (base, depth, len, R, dt) { // per-second load sent and requests answered in time
      var ta = [], cnt = [], att = [], dead = [], h = 0, tp = 0, steps = Math.round(T / dt), i, good = [], sent = [];
      for (i = 0; i < T; i++) { good.push(0); sent.push(0); }
      for (i = 0; i < steps; i++) {
        var t = i * dt, sec = Math.min(T - 1, Math.floor(t + 1e-9));
        while (tp < ta.length && ta[tp] + TIMEOUT <= t + 1e-9) { // the client gives up, and may send again
          if (cnt[tp] > 1e-9) { dead[tp] = 1; if (att[tp] < R) { ta.push(t); cnt.push(cnt[tp]); att.push(att[tp] + 1); dead.push(0); sent[sec] += cnt[tp]; } }
          tp++;
        }
        ta.push(t); cnt.push(base * dt); att.push(0); dead.push(0); sent[sec] += base * dt;
        var budget = CAP * dt * (t >= T0 - 1e-9 && t < T0 + len - 1e-9 ? depth : 1);
        while (budget > 1e-12 && h < ta.length) { // first come first served; late answers still cost the work
          var take = Math.min(budget, cnt[h]);
          if (!dead[h]) good[sec] += take;
          cnt[h] -= take; budget -= take;
          if (cnt[h] <= 1e-12) h++;
        }
      }
      var left = 0, tail = 0;
      for (i = h; i < cnt.length; i++) left += cnt[i];
      for (i = T - 10; i < T; i++) tail += good[i] / 10;
      var rec = -1;
      for (i = Math.ceil(T0 + len); i < T; i++) if (good[i] >= 0.9 * base) { rec = i - (T0 + len); break; }
      return { good: good, sent: sent, stuck: tail < 0.5 * base, queue: left, rec: rec };
    };
    QB.widget(el, {
      title: "A retry storm: the overload that outlasts its cause",
      sub: "A server answers 100 requests a second, first come first served; clients give up after one second. At 20 s it loses part of its capacity for a while. With no retries it catches up. Add retries: every request that times out is sent again, the queue is full of requests nobody is waiting for, and the server never answers in time again. The map on the right shows which triggers tip it over.",
      panels: 2, height: 300,
      controls: [
        { k: "ret", label: "Retries after a timeout", min: 0, max: 5, step: 1, value: 3 },
        { k: "load", label: "What users send", min: 40, max: 95, step: 5, value: 80, fmt: function (x) { return x + " a second"; } },
        { k: "depth", label: "Capacity left during the trigger", min: 30, max: 100, step: 5, value: 50, fmt: function (x) { return x + "%"; } },
        { k: "len", label: "Length of the trigger", min: 0, max: 30, step: 1, value: 10, fmt: function (x) { return x + " s"; } },
      ],
      draw: function (g, v, s) {
        var r = storm(v.load, v.depth / 100, v.len, v.ret, 0.05), i, ts = [], total = 0, peak = 0;
        for (i = 0; i < T; i++) { ts.push(i + 0.5); total += r.good[i]; peak = Math.max(peak, r.sent[i]); }
        s.out = [total / (v.load * T), peak, r.rec, r.stuck, r.queue];
        var top = Math.max(200, Math.ceil(peak / 50) * 50 + 100);
        var a = g[0].axes({ x: [0, T], y: [0, top], title: "Each second: load sent and requests answered in time", xlabel: "seconds" });
        a.area([T0, T0 + v.len], [top, top], 0, { color: C.loss, alpha: 0.13 });
        a.line([0, T0, T0, T0 + v.len, T0 + v.len, T], [CAP, CAP, CAP * v.depth / 100, CAP * v.depth / 100, CAP, CAP], { color: C.muted, dash: [4, 4], width: 1.2 });
        a.line(ts, r.sent, { color: C.implied, width: 1.6 }).line(ts, r.good, { color: C.gain, width: 2.2 });
        a.legend([["load sent", C.implied], ["answered in time", C.gain], ["capacity", C.muted]], { pos: "tr" });
        var depths = [35, 45, 55, 65, 75, 85, 95], lens = [2.5, 7.5, 12.5, 17.5, 22.5, 27.5], j;
        var b = g[1].axes({ x: [0, 30], y: [30, 100], title: "Triggers: recovers (green), stays collapsed (red)", xlabel: "length of the trigger (s)", yfmt: function (y) { return y + "%"; } });
        b.clip(function (c) {
          for (i = 0; i < depths.length; i++) for (j = 0; j < lens.length; j++) {
            var st = storm(v.load, depths[i] / 100, lens[j], v.ret, 0.1).stuck;
            c.fillStyle = st ? C.loss : C.gain; c.globalAlpha = 0.45;
            c.fillRect(b.px(lens[j] - 2.5) + 1, b.py(depths[i] + 5) + 1, b.px(5) - b.px(0) - 2, b.py(0) - b.py(10) - 2);
          }
        });
        b.dots([v.len], [v.depth], { color: C.idea, r: 6 });
      },
      readout: function (v, s) {
        return [["answered in time", QB.pct(s.out[0], 0) + " of what users sent"], ["peak load sent", Math.round(s.out[1]) + " a second"],
          ["after the trigger", s.out[3] ? "never recovers" : s.out[2] < 0 ? "recovering" : "normal again in " + s.out[2].toFixed(0) + " s"], ["queue at 100 s", Math.round(s.out[4]) + " requests"]];
      },
      note: "A fluid model, with no randomness: requests are counted in fractions. The y axis of the map is the capacity left during the trigger, each cell is one run of 100 s, and the gold dot is the trigger chosen by the sliders. The collapsed state is stable because the server spends all its work on requests whose clients have already given up; a retry budget, shedding old requests or a circuit breaker breaks the loop.",
    });
  };

  // ---- Part 51: where a depth buffer's precision goes ---------------------------------------------------------
  W.depthcrowd = function (el) {
    var FAR = 1000;
    var stored = function (d, n) { return FAR * (d - n) / (d * (FAR - n)); }; // window depth in [0, 1], affine in 1/d
    var gapAt = function (d, n, bits) { var k = (FAR - n) / (FAR * n * (Math.pow(2, bits) - 1)); return d * d * k / (1 + d * k); };
    var len = function (x) { return x >= 100 ? x.toFixed(0) : x >= 10 ? x.toFixed(1) : x >= 1 ? x.toFixed(2) : x >= 0.01 ? x.toFixed(3) : x.toExponential(1); };
    QB.widget(el, {
      title: "Where the depth buffer's precision goes",
      sub: "Perspective stores a depth that is affine in 1/d, so most of the buffer's steps lie just behind the near plane (left). The right panel is the smallest gap the buffer can tell apart at each distance: two surfaces closer than that z-fight. With the near plane at 1 and 24 bits the scene is safe; pull the near plane in to 0.01, or drop to 16 bits, and the red region reaches the camera.",
      panels: 2, height: 300,
      controls: [
        { k: "ln", label: "Near plane", min: -2, max: 1, step: 0.05, value: 0, fmt: function (x) { return len(Math.pow(10, x)); } },
        { k: "bits", label: "Depth buffer bits", min: 16, max: 32, step: 8, value: 24 },
        { k: "lg", label: "Gap between two surfaces", min: -3, max: 0, step: 0.05, value: -2, fmt: function (x) { return len(Math.pow(10, x)); } },
      ],
      draw: function (g, v, s) {
        var n = Math.pow(10, v.ln), gap = Math.pow(10, v.lg), i, ds = [], st = [], res = [];
        for (i = 0; i <= 120; i++) { var d = n * Math.pow(FAR / n, i / 120); ds.push(d); st.push(stored(d, n)); res.push(gapAt(d, n, v.bits)); }
        var k = (FAR - n) / (FAR * n * (Math.pow(2, v.bits) - 1)), disc = gap * gap * k * k + 4 * gap * k;
        var fight = (gap * k + Math.sqrt(disc)) / (2 * k); // the distance where the resolvable gap equals the surfaces' gap
        var safe = fight >= FAR;
        s.out = [2 * FAR * n / (FAR + n), gapAt(100, n, v.bits), gapAt(FAR, n, v.bits), safe ? -1 : Math.max(fight, n)];
        var a = g[0].axes({ x: [0.01, FAR], y: [0, 1], logx: true, title: "Stored depth against distance", xlabel: "distance from the eye", yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        a.line(ds, st, { color: C.spot, width: 2.2 });
        a.vline(n, { color: C.muted }).hline(0.5, { color: C.muted }).vline(s.out[0], { color: C.idea });
        a.text(s.out[0], 0.12, "half the range used by " + len(s.out[0]), { color: C.idea, dx: 6, bg: true });
        a.text(n, 0.93, "near", { color: C.muted, dx: n < 0.03 ? 6 : -6, align: n < 0.03 ? "left" : "right" });
        var b = g[1].axes({ x: [0.01, FAR], y: [1e-9, 1e3], logx: true, logy: true, yticks: [1e-9, 1e-6, 1e-3, 1, 1e3], title: "Smallest gap the buffer resolves", xlabel: "distance from the eye",
          yfmt: function (y) { return y >= 1 ? String(y) : y >= 1e-3 ? "0.001" : y >= 1e-6 ? "1e−6" : "1e−9"; } });
        if (!safe) b.area([Math.max(fight, n), FAR], [1e3, 1e3], 1e-9, { color: C.loss, alpha: 0.16 });
        b.line(ds, res.map(function (y) { return Math.max(y, 1e-9); }), { color: C.spot, width: 2.2 });
        b.hline(gap, { color: C.idea, dash: [], width: 1.6 });
        b.legend([["resolvable gap", C.spot], ["the two surfaces' gap", C.idea], ["they z-fight here", C.loss]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["half the depth range is used by distance", len(s.out[0])], ["resolvable gap at distance 100", len(s.out[1])], ["at the far plane (1000)", len(s.out[2])],
          ["the two surfaces z-fight", s.out[3] < 0 ? "nowhere before the far plane" : "beyond distance " + len(s.out[3])]];
      },
      note: "Exact arithmetic for an integer depth buffer with the far plane at 1000: stored depth f(d − n)/(d(f − n)), one step 1/(2^b − 1), so the gap is about d²(f − n)/(f n (2^b − 1)). It grows with the square of the distance and shrinks in proportion to the near plane's distance, which is why moving the near plane out is worth more than extra bits.",
    });
  };

  // ---- Part 52: Runge's phenomenon, and Chebyshev points -----------------------------------------------------
  W.rungenodes = function (el) {
    var XS = QB.linspace(-1, 1, 401), names = ["equally spaced", "Chebyshev"];
    var nodes = function (n, cheb) { // n + 1 points and their barycentric weights
      var x = [], w = [], j, c = 1;
      for (j = 0; j <= n; j++) {
        if (cheb) { x.push(-Math.cos(j * Math.PI / n)); w.push((j % 2 ? -1 : 1) * (j === 0 || j === n ? 0.5 : 1)); }
        else { x.push(-1 + 2 * j / n); w.push((j % 2 ? -1 : 1) * c); c = c * (n - j) / (j + 1); }
      }
      return { x: x, w: w };
    };
    var interp = function (nd, f, t) { // the barycentric formula
      var num = 0, den = 0, j, d, q;
      for (j = 0; j < nd.x.length; j++) { d = t - nd.x[j]; if (Math.abs(d) < 1e-13) return f[j]; q = nd.w[j] / d; num += q * f[j]; den += q; }
      return num / den;
    };
    var maxErr = function (n, cheb, a) {
      var nd = nodes(n, cheb), f = nd.x.map(function (x) { return 1 / (1 + a * a * x * x); }), e = 0, i;
      for (i = 0; i < XS.length; i += 2) e = Math.max(e, Math.abs(interp(nd, f, XS[i]) - 1 / (1 + a * a * XS[i] * XS[i])));
      return e;
    };
    var sci = function (x) { return x >= 0.01 && x < 1000 ? x.toPrecision(3) : x.toExponential(1).replace("e-", "e−").replace("e+", "e"); };
    QB.widget(el, {
      title: "Runge's phenomenon: more points, worse answer",
      sub: "The grey curve is 1/(1 + a²x²). The gold curve is the one polynomial through the marked points. With equally spaced points, add more and the ends swing wider; switch to Chebyshev points, crowded towards the ends, and the same degree converges. The right panel shows the largest error at every degree for both.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Degree (points − 1)", min: 2, max: 40, step: 1, value: 10 },
        { k: "cheb", label: "Points", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return names[x]; } },
        { k: "a", label: "Sharpness a (poles at ±i/a)", min: 1, max: 10, step: 0.5, value: 5, fmt: function (x) { return x.toFixed(1); } },
      ],
      draw: function (g, v, s) {
        var a2 = v.a * v.a, nd = nodes(v.n, v.cheb), fn = nd.x.map(function (x) { return 1 / (1 + a2 * x * x); }), i, n;
        var truth = XS.map(function (x) { return 1 / (1 + a2 * x * x); }), p = XS.map(function (x) { return interp(nd, fn, x); });
        var ns = [], eE = [], eC = [], pred = [], rho = (1 + Math.sqrt(1 + a2)) / v.a, floor = 1e-16;
        for (n = 2; n <= 40; n++) { ns.push(n); eE.push(Math.max(maxErr(n, 0, v.a), floor)); eC.push(Math.max(maxErr(n, 1, v.a), floor)); pred.push(Math.max(Math.pow(rho, -n), floor)); }
        s.out = [eE[v.n - 2], eC[v.n - 2], rho];
        var ax = g[0].axes({ x: [-1, 1], y: [-0.8, 2.2], title: "Degree " + v.n + " through " + names[v.cheb] + " points", xlabel: "x" });
        ax.line(XS, truth, { color: C.cash, width: 2 }).line(XS, p, { color: C.idea, width: 2 });
        ax.dots(nd.x, fn, { color: C.spot, r: 3 });
        ax.legend([["the function", C.cash], ["the interpolant", C.idea]], { pos: "bl" });
        var b = g[1].axes({ x: [2, 40], y: [1e-16, 1e8], logy: true, yticks: [1e-16, 1e-12, 1e-8, 1e-4, 1, 1e4, 1e8], title: "Largest error against degree", xlabel: "degree",
          yfmt: function (y) { var e = Math.round(Math.log10(y)); return e === 0 ? "1" : "1e" + (e < 0 ? "−" + (-e) : e); } });
        b.line(ns, pred, { color: C.muted, dash: [4, 4], width: 1.2 }).line(ns, eE, { color: C.loss, width: 2 }).line(ns, eC, { color: C.gain, width: 2 });
        b.vline(v.n, { color: C.idea });
        b.legend([["equally spaced", C.loss], ["Chebyshev", C.gain], ["ρ^(−n)", C.muted]], { pos: "bl" });
      },
      readout: function (v, s) {
        return [["largest error, equally spaced", sci(s.out[0])], ["Chebyshev", sci(s.out[1])], ["predicted rate ρ = (1 + √(1 + a²))/a", fmt(s.out[2], 3)]];
      },
      note: "Exact function values, evaluated by the barycentric formula on 201 test points. The Chebyshev error falls like ρ^(−n), where ρ is set by the function's poles at ±i/a: the nearer they are to the interval, the slower. With equally spaced points the error grows whenever the poles lie inside a fixed region around the interval; at a = 1 they are outside it and both converge.",
    });
  };

  // ---- Part 53: Grover's search as a rotation ----------------------------------------------------------------
  W.groverturn = function (el) {
    var classical = function (N, M, k) { // the chance that k distinct looks find one of M marked items
      var miss = 1, i;
      for (i = 0; i < k; i++) { if (N - M - i <= 0) return 1; miss *= (N - M - i) / (N - i); }
      return 1 - miss;
    };
    QB.widget(el, {
      title: "Grover's search is a rotation",
      sub: "The state lives in a plane: one axis is the marked items, the other everything else. It starts almost flat, at angle θ with sin θ = √(M/N), and each round (the oracle's reflection, then the diffusion's) turns it by 2θ. Add rounds until the arrow points at the marked axis, then keep going and watch the chance fall again. More items make θ smaller and the climb slower, by a square root.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Qubits (N = 2ⁿ items)", min: 3, max: 12, step: 1, value: 6, fmt: function (x) { return x + " (N = " + Math.pow(2, x).toLocaleString("en") + ")"; } },
        { k: "k", label: "Rounds k", min: 0, max: 100, step: 1, value: 3 },
        { k: "m", label: "Marked items M", min: 1, max: 4, step: 1, value: 1 },
      ],
      draw: function (g, v, s) {
        var N = Math.pow(2, v.n), th = Math.asin(Math.sqrt(v.m / N)), ang = (2 * v.k + 1) * th, p = Math.pow(Math.sin(ang), 2);
        var best = Math.max(0, Math.round(Math.PI / (4 * th) - 0.5));
        s.out = [th * 180 / Math.PI, p, best, Math.pow(Math.sin((2 * best + 1) * th), 2), classical(N, v.m, v.k), (N + 1) / (v.m + 1)];
        // the plane of the state
        var c = g.ctx, bx = g[0].box, R = Math.min(bx.w - 110, bx.h - 96) / 2, cx = bx.x + bx.w / 2, cy = bx.y + bx.h / 2 + 8, i;
        heading(c, bx, "The state after " + v.k + " round" + (v.k === 1 ? "" : "s"));
        c.save();
        c.strokeStyle = C.line; c.lineWidth = 1; c.beginPath(); c.arc(cx, cy, R, 0, 6.2832); c.stroke();
        c.strokeStyle = "#3a475c"; c.beginPath(); c.moveTo(cx - R - 8, cy); c.lineTo(cx + R + 8, cy); c.moveTo(cx, cy + R + 8); c.lineTo(cx, cy - R - 8); c.stroke();
        c.font = "11.5px system-ui, sans-serif"; c.fillStyle = C.gain; c.textAlign = "center"; c.textBaseline = "bottom"; c.fillText("marked", cx, cy - R - 10);
        c.fillStyle = C.muted; c.textAlign = "left"; c.textBaseline = "middle"; c.fillText("the rest", cx + R + 12, cy);
        var from = Math.max(0, v.k - 12);
        for (i = from; i < v.k; i++) { // earlier rounds, fading
          var a0 = (2 * i + 1) * th; c.globalAlpha = 0.12 + 0.5 * (i - from + 1) / (v.k - from + 1); c.strokeStyle = C.spot; c.lineWidth = 1.2;
          c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx + R * Math.cos(a0), cy - R * Math.sin(a0)); c.stroke();
        }
        c.globalAlpha = 1; c.strokeStyle = C.muted; c.setLineDash([4, 4]); c.lineWidth = 1.2;
        c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx + R * Math.cos(th), cy - R * Math.sin(th)); c.stroke(); c.setLineDash([]);
        var ex = cx + R * Math.cos(ang), ey = cy - R * Math.sin(ang);
        c.strokeStyle = C.idea; c.lineWidth = 2.6; c.beginPath(); c.moveTo(cx, cy); c.lineTo(ex, ey); c.stroke();
        c.fillStyle = C.idea; c.beginPath(); c.arc(ex, ey, 4.5, 0, 6.2832); c.fill();
        c.strokeStyle = C.gain; c.lineWidth = 3; c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx, cy - R * Math.sin(ang)); c.stroke(); // its height: the marked amplitude
        c.fillStyle = C.ink; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("gold: the state   green: amplitude on the marked items", bx.x + 12, bx.y + bx.h - 20);
        c.restore();
        // success against rounds
        var ks = [], pq = [], pc = [];
        for (i = 0; i <= 400; i++) { var kk = i / 4; ks.push(kk); pq.push(Math.pow(Math.sin((2 * kk + 1) * th), 2)); }
        var kc = [];
        for (i = 0; i <= 100; i++) { kc.push(i); pc.push(classical(N, v.m, i)); }
        var b = g[1].axes({ x: [0, 100], y: [0, 1], title: "Chance of finding a marked item", xlabel: "rounds (quantum) or looks (classical)", yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.line(kc, pc, { color: C.cash, dash: [4, 4], width: 1.4 }).line(ks, pq, { color: C.idea, width: 1.8 });
        b.vline(best, { color: C.gain }).dots([v.k], [p], { color: C.idea, r: 5.5 });
        b.legend([["Grover: sin²((2k+1)θ)", C.idea], ["classical looks", C.cash], ["best round", C.gain]], { pos: "br" });
      },
      readout: function (v, s) {
        return [["θ", fmt(s.out[0], 2) + "°"], ["chance after " + v.k + " rounds", QB.pct(s.out[1])], ["best round", s.out[2] + " (" + QB.pct(s.out[3]) + ")"],
          ["classical, after " + v.k + " looks", QB.pct(s.out[4])], ["classical looks expected", fmt(s.out[5], 1)]];
      },
      note: "Exact: the formula is the simulator's result to rounding. The arrow's earlier positions are drawn in blue. The best round is the integer nearest π/(4θ) − ½, about (π/4)√(N/M); no quantum algorithm can search an unstructured list in fewer than a constant times √N queries.",
    });
  };
})();
