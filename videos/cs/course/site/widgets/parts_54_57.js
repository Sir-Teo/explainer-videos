// Interactives for Computer Science, Built, Parts 54-57: proofs of programs, trusting trust, spectral graphs, learning theory.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 54: four binary-search midpoints on 6-bit machine integers -------------------------------------------
  W.midpointwrap = function (el) {
    var B = 6, HALF = 32, MASK = 63;
    var names = ["(lo + hi) >> 1", "lo + ((hi − lo) >> 1)", "(lo + hi) >>> 1", "lo + ((hi − lo) >>> 1)"];
    var wrap = function (x) { return ((x + HALF) & MASK) - HALF; };
    var steps = function (f, lo, hi) { // the true inner value, what the machine holds, and the midpoint it computes
      var sum = f === 0 || f === 2, t = sum ? lo + hi : hi - lo, w = wrap(t);
      var half = f >= 2 ? (w & MASK) >> 1 : w >> 1;
      return { t: t, w: w, mid: sum ? wrap(half) : wrap(lo + half) };
    };
    var good = function (f, lo, hi) { var m = steps(f, lo, hi).mid; return lo <= m && m < hi; };
    var counts = []; // per formula: failing pairs with 0 <= lo < hi, and with any lo < hi
    (function () {
      for (var f = 0; f < 4; f++) {
        var a = 0, b = 0;
        for (var lo = -HALF; lo < HALF; lo++) for (var hi = lo + 1; hi < HALF; hi++) if (!good(f, lo, hi)) { b++; if (lo >= 0) a++; }
        counts.push([a, b]);
      }
    })();
    QB.widget(el, {
      title: "Bloch's bug on a 6-bit machine",
      sub: "Integers here have 6 bits: −32 to 31. The left panel tests one midpoint formula on every pair lo < hi (the upper triangle): blue where lo ≤ mid < hi, red where it fails. Move lo and hi into the red, then change the formula: the first repair is safe only right of the dashed line (lo ≥ 0), the last one everywhere.",
      panels: 2, height: 310,
      controls: [
        { k: "lo", label: "lo", min: -32, max: 31, step: 1, value: 12, fmt: function (x) { return fmt(x, 0); } },
        { k: "hi", label: "hi", min: -32, max: 31, step: 1, value: 27, fmt: function (x) { return fmt(x, 0); } },
        { k: "f", label: "Midpoint formula", min: 0, max: 3, step: 1, value: 0, fmt: function (x) { return names[x]; } },
      ],
      draw: function (g, v, s) {
        var f = v.f, lo, hi;
        var a = g[0].axes({ x: [-32, 32], y: [-32, 32], title: "Every pair lo < hi", xlabel: "lo   (hi on the vertical axis)", xticks: [-32, -16, 0, 16, 32], yticks: [-32, -16, 0, 16, 32] });
        a.clip(function (c) {
          var cw = a.px(1) - a.px(0), ch = a.py(0) - a.py(1);
          for (lo = -HALF; lo < HALF; lo++) for (hi = lo + 1; hi < HALF; hi++) {
            c.fillStyle = good(f, lo, hi) ? C.spot : C.loss; c.globalAlpha = good(f, lo, hi) ? 0.55 : 0.9;
            c.fillRect(a.px(lo), a.py(hi + 1), cw + 0.5, ch + 0.5);
          }
        });
        a.vline(0, { color: C.ink, width: 1.2 });
        if (v.lo < v.hi) a.dots([v.lo + 0.5], [v.hi + 0.5], { color: C.idea, r: 5.5 });
        a.legend([["lo ≤ mid < hi", C.spot], ["fails", C.loss], ["your pair", C.idea]], { pos: "br" });
        var r = steps(f, v.lo, v.hi), ok = v.lo < v.hi && good(f, v.lo, v.hi), sum = f === 0 || f === 2;
        s.out = { r: r, ok: ok, valid: v.lo < v.hi };
        var b = g[1].axes({ x: [-34, 33], y: [0, 1], noY: true, title: "The 6-bit number line", xticks: [-32, -16, 0, 16, 31], xlabel: "value" });
        b.line([-32, 31], [0.3, 0.3], { color: C.muted, width: 1.5 });
        if (v.lo < v.hi) b.line([v.lo, v.hi], [0.3, 0.3], { color: C.spot, width: 6, alpha: 0.6 });
        b.dots([v.lo, v.hi], [0.3, 0.3], { color: C.spot, r: 5 });
        b.text(v.lo, 0.3, "lo", { color: C.spot, align: "center", dy: 16 });
        b.text(v.hi, 0.3, "hi", { color: C.spot, align: "center", dy: 16 });
        b.dots([r.mid], [0.3], { color: ok ? C.idea : C.loss, r: 6 });
        b.text(r.mid, 0.3, "mid", { color: ok ? C.idea : C.loss, align: "center", dy: -17, bold: true });
        var what = sum ? "lo + hi" : "hi − lo";
        b.text(-33, 0.92, what + " = " + fmt(r.t, 0) + (r.t !== r.w ? ",  held as " + fmt(r.w, 0) : ",  fits in 6 bits"), { color: r.t !== r.w ? C.loss : C.ink });
        b.text(-33, 0.8, (f >= 2 ? "read as unsigned: " + ((r.w & MASK)) + ",  halved: " + ((r.w & MASK) >> 1) : "halved (signed): " + fmt(r.w >> 1, 0)), { color: C.ink });
        b.text(-33, 0.68, "mid = " + fmt(r.mid, 0) + (v.lo < v.hi ? (ok ? ",  inside [lo, hi)" : ",  outside [lo, hi)") : ",  but lo < hi is required"), { color: ok ? C.idea : C.loss });
      },
      readout: function (v, s) {
        var o = s.out, k = counts[v.f];
        return [["mid", fmt(o.r.mid, 0)], ["lo ≤ mid < hi", o.valid ? (o.ok ? "holds" : "fails") : "needs lo < hi"],
          ["failing pairs with 0 ≤ lo", k[0] + " of 496"], ["failing pairs with any lo", k[1] + " of 2016"]];
      },
      note: "Exact two's-complement arithmetic on 6-bit words, every pair enumerated. >> is the arithmetic shift, >>> the logical one. The film asks the same question of 16-bit words, where a SAT solver stands in for the enumeration.",
    });
  };

  // ---- Part 55: a password's entropy against the guesses people's choices need ----------------------------------
  W.passwordzipf = function (el) {
    var alpha = [[10, "digits"], [26, "lowercase"], [36, "lowercase + digits"], [62, "letters + digits"], [95, "with symbols"]];
    var VOCAB = 1e7, YEAR = 3.156e7;
    var harmonic = function (n, s) { // sum of r^-s for r = 1..n: exact to 1,000, then Euler-Maclaurin
      var h = 0, m = Math.min(n, 1000), r;
      for (r = 1; r <= m; r++) h += Math.pow(r, -s);
      if (n > m) h += (Math.abs(s - 1) < 1e-9 ? Math.log(n / m) : (Math.pow(n, 1 - s) - Math.pow(m, 1 - s)) / (1 - s)) + 0.5 * (Math.pow(n, -s) - Math.pow(m, -s));
      return h;
    };
    var span = function (sec) { // a duration in words; never NaN
      if (sec < 1e-3) return "under a millisecond";
      if (sec < 1) return (sec * 1000).toFixed(0) + " ms";
      if (sec < 120) return sec.toFixed(1) + " s";
      if (sec < 7200) return (sec / 60).toFixed(0) + " minutes";
      if (sec < 172800) return (sec / 3600).toFixed(0) + " hours";
      if (sec < 2 * YEAR) return (sec / 86400).toFixed(0) + " days";
      var y = sec / YEAR;
      if (y < 1e6) return Math.round(y).toLocaleString("en-US") + " years";
      return "10^" + Math.log10(y).toFixed(0) + " years";
    };
    QB.widget(el, {
      title: "Bits of entropy, and the passwords people choose",
      sub: "Left: the expected time to guess a uniformly random password, 2^H / 2R with H = L log₂ N, at the attacker's rate and against a slow salted hash at 10 guesses a second. Right: a Zipf model of human choice, where an attacker tries the most popular passwords first. Lengthen the password and the left panel climbs out of reach; the right panel does not move.",
      panels: 2, height: 310,
      controls: [
        { k: "L", label: "Length L", min: 4, max: 20, step: 1, value: 8, fmt: function (x) { return x + " characters"; } },
        { k: "a", label: "Alphabet N", min: 0, max: 4, step: 1, value: 1, fmt: function (x) { return alpha[x][0] + " (" + alpha[x][1] + ")"; } },
        { k: "r", label: "Guesses a second, R", min: 1, max: 12, step: 1, value: 10, fmt: function (x) { return "10^" + x; } },
        { k: "z", label: "Zipf exponent of human choice", min: 0.6, max: 1.4, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var N = alpha[v.a][0], R = Math.pow(10, v.r), H = v.L * Math.log(N) / Math.LN2, L, i;
        var Ls = [], fast = [], slow = [];
        for (L = 4; L <= 20; L++) { var half = Math.pow(N, L) / 2; Ls.push(L); fast.push(Math.max(1e-9, half / R)); slow.push(Math.max(1e-9, half / 10)); }
        var a = g[0].axes({ x: [4, 20], y: [1e-6, 1e30], logy: true, title: "Random password: expected time to guess", xlabel: "length L", yticks: [1e-6, 1, 1e6, 1e12, 1e18, 1e24, 1e30], yfmt: function (y) { return "1e" + Math.round(Math.log10(y)); } });
        a.hline(86400, { color: C.muted }); a.text(20, 86400, "a day", { color: C.muted, align: "right", dx: -4, dy: -8 });
        a.hline(YEAR * 100, { color: C.muted }); a.text(20, YEAR * 100, "a century", { color: C.muted, align: "right", dx: -4, dy: -8 });
        a.hline(4.35e17, { color: C.muted }); a.text(20, 4.35e17, "age of the universe", { color: C.muted, align: "right", dx: -4, dy: -8 });
        a.line(Ls, slow, { color: C.idea, width: 2 }); a.line(Ls, fast, { color: C.spot, width: 2 });
        a.vline(v.L, { color: C.ink });
        a.dots([v.L, v.L], [Math.min(1e30, Math.max(1e-6, fast[v.L - 4])), Math.min(1e30, Math.max(1e-6, slow[v.L - 4]))], { color: function (k) { return k ? C.idea : C.spot; }, r: 4.5 });
        a.legend([["at R guesses a second", C.spot], ["slow salted hash, 10 a second", C.idea]], { pos: "tl" });
        var Hn = harmonic(VOCAB, v.z), gs = [], share = [], rnd = [];
        for (i = 0; i <= 70; i++) { var q = Math.pow(10, i / 10); gs.push(q); share.push(harmonic(Math.round(q), v.z) / Hn); rnd.push(Math.min(1, q / Math.pow(N, v.L))); }
        var b = g[1].axes({ x: [1, 1e7], y: [0, 1], logx: true, title: "Share of accounts cracked", xlabel: "guesses per account, most popular first", yfmt: function (y) { return Math.round(100 * y) + "%"; }, xfmt: function (x) { var e = Math.round(Math.log10(x)); return e % 2 ? "" : "1e" + e; } });
        b.line(gs, rnd, { color: C.gain, width: 2 }); b.line(gs, share, { color: C.loss, width: 2.2 });
        b.vline(1e6, { color: C.muted });
        b.legend([["people's choices (Zipf)", C.loss], ["random, this L and N", C.gain]], { pos: "tl" });
        s.out = { H: H, fast: Math.pow(N, v.L) / 2 / R, slow: Math.pow(N, v.L) / 20, ten: harmonic(10, v.z) / Hn, mil: harmonic(1e6, v.z) / Hn };
      },
      readout: function (v, s) {
        var o = s.out;
        return [["entropy H", fmt(o.H, 1) + " bits"], ["expected time at R", span(o.fast)], ["against the slow hash", span(o.slow)],
          ["people's choices: 10 guesses crack", QB.pct(o.ten, 0)], ["a million crack", QB.pct(o.mil, 0)]];
      },
      note: "The left panel is exact arithmetic for a uniformly random password. The right panel is an illustrative model, not data: the r-th most popular of ten million passwords is chosen with probability proportional to 1/r^s. With s = 1 it gives the film's figures, 18% after ten guesses and 86% after a million.",
    });
  };

  // ---- Part 56: two communities, the Fiedler vector's sweep cut, and the walk the bottleneck slows ----------------
  function jacobiEig(M) { // eigenvalues (ascending) and eigenvectors of a small symmetric matrix, by cyclic Jacobi rotations
    var n = M.length, A = M.map(function (r) { return r.slice(); }), V = [], i, j, p, q, k, sweep;
    for (i = 0; i < n; i++) { V.push(new Array(n).fill(0)); V[i][i] = 1; }
    for (sweep = 0; sweep < 14; sweep++) {
      var off = 0;
      for (p = 0; p < n; p++) for (q = p + 1; q < n; q++) off += A[p][q] * A[p][q];
      if (off < 1e-18) break;
      for (p = 0; p < n; p++) for (q = p + 1; q < n; q++) {
        if (Math.abs(A[p][q]) < 1e-14) continue;
        var th = (A[q][q] - A[p][p]) / (2 * A[p][q]), t = (th >= 0 ? 1 : -1) / (Math.abs(th) + Math.sqrt(th * th + 1));
        var c = 1 / Math.sqrt(t * t + 1), sn = t * c;
        for (k = 0; k < n; k++) { var akp = A[k][p], akq = A[k][q]; A[k][p] = c * akp - sn * akq; A[k][q] = sn * akp + c * akq; }
        for (k = 0; k < n; k++) { var apk = A[p][k], aqk = A[q][k]; A[p][k] = c * apk - sn * aqk; A[q][k] = sn * apk + c * aqk; }
        for (k = 0; k < n; k++) { var vkp = V[k][p], vkq = V[k][q]; V[k][p] = c * vkp - sn * vkq; V[k][q] = sn * vkp + c * vkq; }
      }
    }
    var idx = []; for (i = 0; i < n; i++) idx.push(i);
    idx.sort(function (a, b) { return A[a][a] - A[b][b]; });
    return { values: idx.map(function (a) { return A[a][a]; }), vector: function (m) { var out = []; for (var r = 0; r < n; r++) out.push(V[r][idx[m]]); return out; } };
  }

  W.fiedlersweep = function (el) {
    var STEPS = 300;
    QB.widget(el, {
      title: "A bottleneck, seen by the second eigenvalue",
      sub: "Two communities joined by a few edges, coloured by the sweep cut over the Fiedler vector; the edges it severs are red. On the right a lazy random walk starts in the left community: the thinner the bridge, the smaller λ₂ and the longer the walk takes to forget its start. Add edges between the communities until the cut stops being the planted one.",
      panels: 2, height: 320,
      controls: [
        { k: "k", label: "Vertices in each community", min: 6, max: 14, step: 1, value: 10, fmt: function (x) { return String(x); } },
        { k: "pin", label: "Edge probability inside", min: 0.2, max: 0.9, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "pout", label: "Edge probability between", min: 0, max: 0.6, step: 0.02, value: 0.02, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New graph", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var k = v.k, n = 2 * k, r = QB.rng(s.seed * 7 + 560), A = [], d = new Array(n).fill(0), i, j, t;
        for (i = 0; i < n; i++) A.push(new Array(n).fill(0));
        var U = []; // one uniform per pair, drawn for the largest graph so that sliders add and remove edges monotonically
        for (i = 0; i < 28; i++) { U.push([]); for (j = 0; j < 28; j++) U[i].push(j > i ? r() : 0); }
        var side = function (a) { return a < k ? 0 : 1; }, slot = function (a) { return a < k ? a : 14 + (a - k); };
        for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) {
          var same = side(i) === side(j), ring = same && (j === i + 1 || (j - i === k - 1 && (i === 0 || i === k)));
          var on = ring || (i === k - 1 && j === k) || U[slot(i)][slot(j)] < (same ? v.pin : v.pout); // a ring in each community and one bridge keep it connected
          if (on) { A[i][j] = A[j][i] = 1; d[i]++; d[j]++; }
        }
        var vol = 0; for (i = 0; i < n; i++) vol += d[i];
        var Nm = []; for (i = 0; i < n; i++) { Nm.push([]); for (j = 0; j < n; j++) Nm[i].push((i === j ? 1 : 0) - A[i][j] / Math.sqrt(d[i] * d[j])); }
        var eig = jacobiEig(Nm), lam2 = Math.max(0, eig.values[1]), f = eig.vector(1).map(function (x, a) { return x / Math.sqrt(d[a]); });
        if (f[0] > 0) f = f.map(function (x) { return -x; });
        var order = []; for (i = 0; i < n; i++) order.push(i);
        order.sort(function (a, b) { return f[a] - f[b]; });
        var S = new Array(n).fill(false), cut = 0, vs = 0, best = 9, bestK = 1, curve = [];
        for (t = 0; t < n - 1; t++) {
          var u = order[t], inS = 0; for (j = 0; j < n; j++) if (S[j] && A[u][j]) inS++;
          cut += d[u] - 2 * inS; S[u] = true; vs += d[u];
          var phi = cut / Math.max(1, Math.min(vs, vol - vs)); curve.push(phi);
          if (phi < best) { best = phi; bestK = t + 1; }
        }
        var inCut = new Array(n).fill(false); for (t = 0; t < bestK; t++) inCut[order[t]] = true;
        var pc = 0, pv = 0, wrong = 0; for (i = 0; i < k; i++) { pv += d[i]; for (j = k; j < n; j++) pc += A[i][j]; }
        for (i = 0; i < n; i++) if (inCut[i] !== (i < k)) wrong++;
        wrong = Math.min(wrong, n - wrong);
        // the lazy walk from vertex 0
        var p = new Array(n).fill(0), tv = [], bound = [], ts = [], tmix = -1, pimin = 1; p[0] = 1;
        for (i = 0; i < n; i++) pimin = Math.min(pimin, d[i] / vol);
        for (t = 0; t <= STEPS; t++) {
          var dist = 0; for (i = 0; i < n; i++) dist += Math.abs(p[i] - d[i] / vol);
          dist /= 2; if (tmix < 0 && dist < 0.25) tmix = t;
          ts.push(t); tv.push(Math.max(dist, 1e-6)); bound.push(Math.max(1e-6, Math.min(1, 0.5 * Math.sqrt(1 / pimin) * Math.pow(1 - lam2 / 2, t))));
          var nx = new Array(n).fill(0);
          for (i = 0; i < n; i++) { nx[i] += 0.5 * p[i]; var share = 0.5 * p[i] / d[i]; for (j = 0; j < n; j++) if (A[i][j]) nx[j] += share; }
          p = nx;
        }
        s.out = { lam2: lam2, phi: best, planted: pc / Math.max(1, Math.min(pv, vol - pv)), tmix: tmix, wrong: wrong };
        // left: the graph
        var c = g.ctx, b = g[0].box, R = Math.min(b.w * 0.2, b.h * 0.3), cy = b.y + b.h * 0.54, pos = [];
        for (i = 0; i < n; i++) { var ang = 2 * Math.PI * (i % k) / k + (i < k ? 0 : Math.PI), cx = b.x + b.w * (i < k ? 0.27 : 0.73); pos.push([cx + R * Math.cos(ang), cy + R * Math.sin(ang)]); }
        c.save(); c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("The sweep cut of the Fiedler vector", b.x + 12, b.y + 6);
        for (var pass = 0; pass < 2; pass++) for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) if (A[i][j] && (inCut[i] !== inCut[j]) === (pass === 1)) {
          c.strokeStyle = pass ? C.loss : "#3a475c"; c.lineWidth = pass ? 1.6 : 1; c.globalAlpha = pass ? 0.95 : 0.8;
          c.beginPath(); c.moveTo(pos[i][0], pos[i][1]); c.lineTo(pos[j][0], pos[j][1]); c.stroke();
        }
        c.globalAlpha = 1;
        for (i = 0; i < n; i++) { c.fillStyle = inCut[i] ? C.spot : C.idea; c.beginPath(); c.arc(pos[i][0], pos[i][1], 5.5, 0, 6.2832); c.fill(); }
        c.font = "11.5px system-ui, sans-serif"; c.textBaseline = "middle";
        var ly = b.y + b.h - 14, lx = b.x + 12;
        [["one side", C.spot], ["other side", C.idea], ["cut edges", C.loss]].forEach(function (it) {
          c.fillStyle = it[1]; c.beginPath(); c.arc(lx + 4, ly, 4, 0, 6.2832); c.fill(); c.fillStyle = C.ink; c.fillText(it[0], lx + 13, ly); lx += c.measureText(it[0]).width + 30;
        });
        c.restore();
        // right: the walk
        var a = g[1].axes({ x: [0, STEPS], y: [1e-3, 1], logy: true, title: "Lazy walk: distance to stationarity", xlabel: "steps" });
        a.hline(0.25, { color: C.muted }); a.text(STEPS, 0.25, "1/4: mixed", { color: C.muted, align: "right", dx: -4, dy: 10 });
        a.line(ts, bound, { color: C.loss, width: 1.5, dash: [5, 4] }); a.line(ts, tv, { color: C.gain, width: 2.2 });
        a.legend([["total variation", C.gain], ["bound from λ₂", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["λ₂", fmt(o.lam2, 3)], ["λ₂/2 ≤ sweep φ ≤ √(2λ₂)", fmt(o.lam2 / 2, 3) + " ≤ " + fmt(o.phi, 3) + " ≤ " + fmt(Math.sqrt(2 * o.lam2), 3)],
          ["φ of the planted cut", fmt(o.planted, 3)], ["vertices on the other side of it", String(o.wrong)], ["steps to mix", o.tmix < 0 ? "more than 300" : String(o.tmix)]];
      },
      note: "Simulated graphs: each community is a ring plus random chords, and one bridge always joins the two. λ₂ is the second eigenvalue of the normalized Laplacian I − D^(−1/2) A D^(−1/2), found by Jacobi rotations; the bound is ½ √(1/π_min) (1 − λ₂/2)^t.",
    });
  };

  // ---- Part 57: Hedge and follow the leader, on random losses and against an adversary --------------------------
  W.hedgeleader = function (el) {
    var worlds = ["random losses", "alternating adversary"];
    QB.widget(el, {
      title: "Regret: Hedge against follow the leader",
      sub: "Regret is the learner's total loss minus the best expert's. Hedge weights each expert by exp(−η × its loss so far) and has regret at most ln N / η + ηT/8 whatever the losses. Switch to the adversary, where follow the leader loses almost every round, then raise η and watch Hedge turn into it.",
      panels: 2, height: 300,
      controls: [
        { k: "world", label: "Losses", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return worlds[x]; } },
        { k: "N", label: "Experts N", min: 2, max: 50, step: 1, value: 20, fmt: function (x) { return String(x); } },
        { k: "T", label: "Rounds T", min: 100, max: 2000, step: 100, value: 1000, fmt: function (x) { return String(x); } },
        { k: "mult", label: "η as a multiple of √(8 ln N / T)", min: -4, max: 6, step: 1, value: 0, fmt: function (x) { return "× " + (x >= 0 ? Math.pow(2, x).toFixed(0) : "1/" + Math.pow(2, -x).toFixed(0)); } },
      ],
      buttons: [{ label: "New losses", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var N = v.N, T = v.T, r = QB.rng(s.seed * 13 + 570), eta0 = Math.sqrt(8 * Math.log(N) / T), eta = eta0 * Math.pow(2, v.mult);
        var means = [], i, t; for (i = 0; i < N; i++) means.push(0.4 + 0.2 * r()); means[N > 3 ? 3 : 0] = 0.35;
        var cum = new Array(N).fill(0), ch = 0, cf = 0, ts = [], rh = [], rf = [], gb = [], stride = Math.max(1, T / 200), loss = new Array(N);
        var wts = new Array(N).fill(1 / N);
        for (t = 0; t < T; t++) {
          if (v.world === 0) for (i = 0; i < N; i++) loss[i] = r() < means[i] ? 1 : 0;
          else for (i = 0; i < N; i++) loss[i] = i === 0 ? (t === 0 ? 0.5 : (t % 2 === 0 ? 1 : 0)) : i === 1 ? (t % 2 === 1 ? 1 : 0) : 1; // experts 0 and 1 alternate; the rest always lose
          var lead = 0, mn = cum[0], sw = 0, hl = 0;
          for (i = 1; i < N; i++) if (cum[i] < mn) { mn = cum[i]; lead = i; }
          for (i = 0; i < N; i++) { wts[i] = Math.exp(-eta * (cum[i] - mn)); sw += wts[i]; } // weights relative to the leader: no underflow
          for (i = 0; i < N; i++) hl += wts[i] / sw * loss[i];
          ch += hl; cf += loss[lead];
          for (i = 0; i < N; i++) cum[i] += loss[i];
          mn = cum[0]; for (i = 1; i < N; i++) if (cum[i] < mn) mn = cum[i];
          if ((t + 1) % stride === 0 || t === T - 1) { ts.push(t + 1); rh.push(ch - mn); rf.push(cf - mn); gb.push(Math.log(N) / eta + eta * (t + 1) / 8); }
        }
        var k = ts.length - 1, best = Math.sqrt(T * Math.log(N) / 2);
        s.out = { hedge: rh[k], ftl: rf[k], bound: gb[k], best: best, eta: eta };
        var top = Math.max(gb[k], rf[k], rh[k], 10) * 1.12, lo = Math.min(0, Math.min.apply(null, rf), Math.min.apply(null, rh));
        var a = g[0].axes({ x: [0, T], y: [lo, top], title: "Regret so far", xlabel: "round t" });
        a.line(ts, gb, { color: C.loss, width: 1.6, dash: [5, 4] });
        a.line(ts, rf, { color: C.idea, width: 2 }); a.line(ts, rh, { color: C.gain, width: 2.2 });
        a.legend([["Hedge", C.gain], ["follow the leader", C.idea], ["ln N/η + ηt/8", C.loss]], { pos: "tl" });
        // right: the guarantee as a function of eta, with the chosen eta marked
        var es = [], bs = []; for (i = -40; i <= 60; i++) { var e = eta0 * Math.pow(2, i / 10); es.push(Math.pow(2, i / 10)); bs.push(Math.log(N) / e + e * T / 8); }
        var b = g[1].axes({ x: [1 / 16, 64], y: [1, Math.max(10 * best, 100)], logx: true, logy: true, title: "The guarantee ln N/η + ηT/8", xlabel: "η / √(8 ln N / T)", xticks: [1 / 16, 1 / 4, 1, 4, 16, 64], xfmt: function (x) { return x >= 1 ? String(x) : "1/" + Math.round(1 / x); } });
        b.line(es, bs, { color: C.loss, width: 2 });
        b.hline(best, { color: C.muted }); b.text(64, best, "√(T ln N / 2)", { color: C.muted, align: "right", dx: -4, dy: 10 });
        b.dots([Math.pow(2, v.mult)], [Math.max(1, gb[k])], { color: C.loss, r: 5 });
        b.dots([Math.pow(2, v.mult)], [Math.max(1, Math.min(Math.max(10 * best, 100), rh[k]))], { color: C.gain, r: 5 });
        b.legend([["guarantee", C.loss], ["Hedge's regret at T", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["Hedge's regret", fmt(o.hedge, 1)], ["its guarantee", fmt(o.bound, 1)], ["best guarantee √(T ln N / 2)", fmt(o.best, 1)], ["follow the leader's regret", fmt(o.ftl, 1)]];
      },
      note: "Simulated losses. Random world: each expert loses 1 with its own probability between 0.4 and 0.6, one of them 0.35. Adversary: two experts alternate losing 1 after a first half-loss, the others always lose. Hedge's loss is its expected loss, the weighted average over experts.",
    });
  };
})();
