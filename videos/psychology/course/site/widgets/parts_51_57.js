// Interactives for Act XII, psychology at work (Parts 51-57).  Each is an experiment the reader takes part in,
// built on the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  function mulberry(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function z(p) { // inverse normal cdf (Acklam)
    var a = [-39.6968302866538, 220.946098424521, -275.928510446969, 138.357751867269, -30.6647980661472, 2.50662827745924],
        b = [-54.4760987982241, 161.585836858041, -155.698979859887, 66.8013118877197, -13.2806815528857],
        c = [-0.00778489400243029, -0.322396458041136, -2.40075827716184, -2.54973253934373, 4.37466414146497, 2.93816398269878],
        d = [0.00778469570904146, 0.32246712907004, 2.445134137143, 3.75440866190742], q, r;
    if (p < 0.02425) { q = Math.sqrt(-2 * Math.log(p)); return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
    if (p > 1 - 0.02425) { q = Math.sqrt(-2 * Math.log(1 - p)); return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
    q = p - 0.5; r = q * q;
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
  }

  // ---- Part 51: Mackworth's clock on you.  Ninety seconds; press when the pointer jumps two steps. ----
  W.watchclock = function (el) {
    var w = null, STEP = 750, N = 120, WINDOW = 2 * STEP;
    var S = { phase: "idle", k: 0, pos: 0, jumps: [], presses: [], sig: [], flash: 0, runs: [] };
    function plan(rand, rare) {
      var p = rare ? 1 / 30 : 1 / 10, sig = [], i, last = -9;
      for (i = 0; i < N; i++) { var s = i > 3 && i - last > 3 && rand() < p; sig.push(s); if (s) last = i; }
      return sig;
    }
    function score() {
      var hit = 0, fa = 0, used = {}, nsig = 0, i, half = [[0, 0], [0, 0]];
      S.jumps.forEach(function (j) { if (j.s) { nsig++; half[j.k < N / 2 ? 0 : 1][1]++; } });
      S.presses.forEach(function (p) {
        var got = null;
        for (i = S.jumps.length - 1; i >= 0; i--) {
          var j = S.jumps[i];
          if (p.t - j.t > WINDOW + 50) break;
          if (j.s && p.t >= j.t && !used[j.k]) { used[j.k] = 1; got = j; break; }
        }
        if (got) { hit++; half[got.k < N / 2 ? 0 : 1][0]++; } else fa++;
      });
      var nn = Math.max(S.jumps.length - nsig, 1);
      var h = (hit + 0.5) / (nsig + 1), f = (fa + 0.5) / (nn + 1);
      return { hit: hit, fa: fa, nsig: nsig, nn: nn, h: h, f: f, d: z(h) - z(f), c: -(z(h) + z(f)) / 2, half: half };
    }
    function step() {
      if (S.k >= N) {
        S.phase = "done";
        var s = score(); S.runs.push({ rare: S.rare, s: s });
        if (w) w.render();
        return;
      }
      var s2 = S.sig[S.k];
      S.pos = (S.pos + (s2 ? 2 : 1)) % 100;
      S.jumps.push({ t: T.now(), s: s2, k: S.k }); S.k++;
      if (w) w.render();
      task.later(step, STEP);
    }
    var task = T.create(el, {
      keys: { " ": 0, f: 0, j: 1 },
      accepting: function () { return S.phase === "run"; },
      respond: function () {
        S.presses.push({ t: T.now(), k: S.k }); S.flash = T.now(); task.count++;
        if (w) w.render();
      },
    });
    function start(state, rare) {
      task.clear();
      var rand = mulberry(51 + (state ? state.seed : 0) * 7 + (rare ? 1 : 0));
      S.sig = plan(rand, rare); S.rare = rare; S.k = 0; S.pos = 0; S.jumps = []; S.presses = []; task.count = 0;
      S.phase = "run"; if (w) w.render();
      task.later(step, STEP);
    }
    w = QB.widget(el, {
      title: "Watch the clock",
      sub: "Norman Mackworth's watch, for ninety seconds. The pointer moves one step at a time. Now and then it jumps two steps at once: press the space bar (or F or J), or tap the clock, as soon as you see a double jump. Then try the rare version, where double jumps come about a third as often.",
      panels: 2, height: 340, weights: [1, 1.1],
      buttons: [
        { label: "Start (common signals)", act: function (state) { start(state, false); } },
        { label: "Start (rare signals)", act: function (state) { start(state, true); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.runs = []; S.jumps = []; S.presses = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), i;
        if (S.phase === "run") {
          var R = Math.min(b.w, b.h) * 0.36, cx = b.cx, cy = b.cy + 8;
          ctx.save();
          ctx.strokeStyle = "#4a5568"; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(cx, cy, R, 0, 2 * Math.PI); ctx.stroke();
          for (i = 0; i < 100; i++) {
            var a = -Math.PI / 2 + 2 * Math.PI * i / 100, r0 = i % 10 === 0 ? R * 0.86 : R * 0.92;
            ctx.beginPath(); ctx.moveTo(cx + r0 * Math.cos(a), cy + r0 * Math.sin(a)); ctx.lineTo(cx + R * Math.cos(a), cy + R * Math.sin(a)); ctx.stroke();
          }
          var ap = -Math.PI / 2 + 2 * Math.PI * S.pos / 100;
          ctx.strokeStyle = "#f2c14e"; ctx.lineWidth = 4;
          ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + R * 0.82 * Math.cos(ap), cy + R * 0.82 * Math.sin(ap)); ctx.stroke();
          ctx.fillStyle = T.now() - S.flash < 250 ? "#7ec8f5" : "#f2c14e";
          ctx.beginPath(); ctx.arc(cx, cy, 5, 0, 2 * Math.PI); ctx.fill();
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif"; ctx.textAlign = "center";
          ctx.fillText(Math.max(0, Math.round((N - S.k) * STEP / 1000)) + " s left", b.cx, b.y + 22);
          ctx.restore();
        } else if (S.phase === "done") {
          var s = S.runs[S.runs.length - 1].s;
          T.message(ctx, b, "You caught " + s.hit + " of " + s.nsig + " double jumps, with " + s.fa + " false alarms.",
            "Your d' is " + s.d.toFixed(2) + " and your criterion c is " + s.c.toFixed(2) + ". Ninety seconds is far too short to show the decrement: in Mackworth's two-hour watch it appears within the first half hour.");
        } else {
          T.message(ctx, b, "On you", "Press a Start button and watch the pointer. Respond only to the double jumps.");
        }
        var a2 = g[1].axes({ x: [0, 3.5], y: [-0.14, 1.05], title: "Your watches (hits and false alarms)", noX: true });
        S.runs.forEach(function (r, k) {
          if (k > 2) return;
          var x = k + 0.6, s = r.s, hr = s.nsig ? s.hit / s.nsig : 0, fr = s.fa / s.nn;
          a2.bars([x], [hr], 0.35, { color: r.rare ? "#f28fb8" : "#5bd18b" });
          a2.bars([x + 0.4], [Math.min(1, fr * 5)], 0.35, { color: "#7ec8f5" });
          a2.text(x + 0.2, -0.07, (r.rare ? "rare" : "common") + "  d' " + s.d.toFixed(1) + ", c " + s.c.toFixed(1), { size: 10, color: C.muted, align: "center" });
        });
        a2.text(0.1, 1.0, "green or pink: hits;  blue: false alarms x 5", { size: 10, color: C.muted });
      },
      readout: function () {
        var last = S.runs.length ? S.runs[S.runs.length - 1].s : null;
        return [["presses", String(task.count)], ["d'", last ? last.d.toFixed(2) : "–"], ["c", last ? last.c.toFixed(2) : "–"]];
      },
      note: "Nothing you press is stored or sent. Rare signals usually raise the criterion (fewer presses, more misses): the prevalence effect of chapter seven, in ninety seconds.",
    });
  };

  // ---- Part 52: Fitts's law on you.  Click targets of three sizes at three distances; your line and throughput. ----
  W.pointer = function (el) {
    var w = null, SIZES = [12, 24, 48], DISTS = [70, 140, 210], REPS = 2;
    var S = { phase: "idle", trials: [], k: 0, target: null, t0: 0, log: [], from: null };
    var mouse = { x: null, y: null };
    function track(e) {
      var c = e.target;
      if (!c || c.tagName !== "CANVAS") return;
      var r = c.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
    }
    el.addEventListener("pointermove", track);
    el.addEventListener("pointerdown", track); // registered before the task kit's, so it runs first
    function place(b) {
      var tr = S.trials[S.k], scale = Math.min(1, (Math.min(b.w, b.h * 1.6) - 70) / 260);
      var D = tr.D * scale, Wd = tr.W, from = S.from || { x: b.cx, y: b.cy }, a, x, y, i;
      for (i = 0; i < 24; i++) {
        a = 2 * Math.PI * ((tr.ang + i * 0.37) % 1);
        x = from.x + D * Math.cos(a); y = from.y + D * Math.sin(a);
        if (x > b.x + 20 + Wd && x < b.x + b.w - 20 - Wd && y > b.y + 34 + Wd && y < b.y + b.h - 20 - Wd) break;
      }
      x = Math.max(b.x + 20 + Wd, Math.min(b.x + b.w - 20 - Wd, x)); y = Math.max(b.y + 34 + Wd, Math.min(b.y + b.h - 20 - Wd, y));
      S.target = { x: x, y: y, W: Wd, D: Math.hypot(x - from.x, y - from.y), from: from };
      S.t0 = T.now();
    }
    function fit() {
      var n = S.log.length, i, mx = 0, my = 0, sxy = 0, sxx = 0;
      if (n < 3) return null;
      for (i = 0; i < n; i++) { mx += S.log[i].ID; my += S.log[i].MT; }
      mx /= n; my /= n;
      for (i = 0; i < n; i++) { sxy += (S.log[i].ID - mx) * (S.log[i].MT - my); sxx += (S.log[i].ID - mx) * (S.log[i].ID - mx); }
      var b = sxx > 0 ? sxy / sxx : 0, a = my - b * mx;
      // throughput: per width, the effective width from the spread of endpoints along the movement axis
      var tp = [], hits = 0;
      SIZES.forEach(function (Wd) {
        var r = S.log.filter(function (q) { return q.W === Wd; });
        if (r.length < 2) return;
        var m = 0, v = 0; r.forEach(function (q) { m += q.dx; }); m /= r.length;
        r.forEach(function (q) { v += (q.dx - m) * (q.dx - m); }); v /= (r.length - 1);
        var we = Math.max(4.133 * Math.sqrt(v), 1);
        r.forEach(function (q) { tp.push(Math.log2(q.D / we + 1) / q.MT); });
      });
      S.log.forEach(function (q) { if (q.hit) hits++; });
      var mtp = tp.length ? tp.reduce(function (s, x) { return s + x; }, 0) / tp.length : NaN;
      return { a: a, b: b, tp: mtp, hits: hits };
    }
    var task = T.create(el, {
      keys: { " ": 0 },
      accepting: function () { return S.phase === "run"; },
      respond: function () {
        if (!S.target) return;
        var t = S.target, px = mouse.x === null ? t.x : mouse.x, py = mouse.y === null ? t.y : mouse.y;
        var ux = (t.x - t.from.x) / (t.D || 1), uy = (t.y - t.from.y) / (t.D || 1);
        var dx = (px - t.x) * ux + (py - t.y) * uy, hit = Math.hypot(px - t.x, py - t.y) <= t.W;
        var mt = (T.now() - S.t0) / 1000;
        S.log.push({ W: t.W, D: t.D, ID: Math.log2(t.D / (2 * t.W) + 1), MT: Math.max(mt, 0.05), dx: dx, hit: hit });
        task.count++; S.from = { x: px, y: py }; S.k++; S.target = null;
        if (S.k >= S.trials.length) { S.phase = "done"; S.target = null; }
        if (w) w.render();
      },
    });
    function start(state) {
      var rand = mulberry(52 + (state ? state.seed : 0)), tr = [], r, i, j;
      for (r = 0; r < REPS; r++) SIZES.forEach(function (Wd) { DISTS.forEach(function (D) { tr.push({ W: Wd, D: D, ang: rand() }); }); });
      for (i = tr.length - 1; i > 0; i--) { j = Math.floor(rand() * (i + 1)); var t = tr[i]; tr[i] = tr[j]; tr[j] = t; }
      S.trials = tr; S.k = 0; S.log = []; S.from = null; S.target = null; task.count = 0; S.phase = "run";
      if (w) w.render();
    }
    w = QB.widget(el, {
      title: "Point and click",
      sub: "Eighteen targets of three sizes appear at three distances. Click each one (or put the pointer on it and press the space bar) as fast as you can while staying accurate. The page fits your own Fitts's law line and works out your throughput in bits per second from where your clicks landed.",
      panels: 2, height: 340, weights: [1.15, 1],
      buttons: [
        { label: "Start", act: function (state) { start(state); } },
        { label: "Clear", act: function (state) { state.seed++; S.phase = "idle"; S.log = []; S.target = null; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (S.phase === "run") {
          if (!S.target) place(b);
          ctx.save();
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif"; ctx.textAlign = "center";
          ctx.fillText("target " + (S.k + 1) + " of " + S.trials.length, b.cx, b.y + 20);
          ctx.fillStyle = "rgba(242,193,78,0.85)";
          ctx.beginPath(); ctx.arc(S.target.x, S.target.y, S.target.W, 0, 2 * Math.PI); ctx.fill();
          ctx.restore();
        } else if (S.phase === "done") {
          var f = fit();
          T.message(ctx, b, "Done: " + (f ? f.hits : 0) + " of " + S.log.length + " clicks on target.",
            f ? "Your line: MT = " + f.a.toFixed(2) + " + " + f.b.toFixed(2) + " x ID seconds. Throughput about " + (isFinite(f.tp) ? f.tp.toFixed(1) : "?") + " bits per second (a mouse usually gives about 3.5 to 5)." : "");
        } else {
          T.message(ctx, b, "On you", "Press Start, then click each yellow target as it appears.");
        }
        var a2 = g[1].axes({ x: [0, 4.5], y: [0, 2], title: "Your movements", xlabel: "index of difficulty (bits)", ylabel: "seconds" });
        var xs = S.log.map(function (q) { return q.ID; }), ys = S.log.map(function (q) { return Math.min(q.MT, 1.98); });
        a2.dots(xs, ys, { color: function (i) { return S.log[i].hit ? "#5bd18b" : "#ef6f6c"; }, r: 3.5 });
        var f2 = fit();
        if (f2) a2.line([0.2, 4.3], [f2.a + 0.2 * f2.b, f2.a + 4.3 * f2.b], { color: "#f2c14e", width: 2 });
      },
      readout: function () {
        var f = fit();
        return [["clicks", String(task.count)], ["slope (s/bit)", f ? f.b.toFixed(2) : "–"], ["throughput", f && isFinite(f.tp) ? f.tp.toFixed(1) + " bit/s" : "–"]];
      },
      note: "Nothing you click is stored or sent. Green dots were on target, red ones missed. With eighteen movements the line is rough; the law shows itself better with more.",
    });
  };

  // ---- Part 53: whom would you hire?  Pairs of candidates: a test score and an interview impression. ----
  W.hiring = function (el) {
    var w = null, N = 12;
    function gauss(rand) { var u = 1 - rand(), v = rand(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
    function person(rand) {
      var g = gauss(rand), s = gauss(rand);
      return { perf: 0.31 * g + 0.45 * s + 0.837 * gauss(rand), test: g + 0.4 * gauss(rand), imp: s + 2.2 * gauss(rand) };
    }
    function pct(z) { var t = 1 / (1 + 0.2316419 * Math.abs(z)), d = 0.3989423 * Math.exp(-z * z / 2);
      var p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274)))); return Math.round(100 * (z > 0 ? 1 - p : p)); }
    var S = { phase: "idle", pairs: [], k: 0, log: [] };
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side) {
        var pr = S.pairs[S.k], pick = pr[side], other = pr[1 - side];
        var testPick = pr[0].test > pr[1].test ? pr[0] : pr[1];
        S.log.push({ right: pick.perf > other.perf, testRight: testPick.perf > (testPick === pr[0] ? pr[1] : pr[0]).perf,
                     choseTest: pick === testPick });
        task.count++; S.k++;
        S.phase = S.k >= N ? "done" : "ask";
        if (w) w.render();
      },
    });
    function start(state) {
      var rand = mulberry(53 + (state ? state.seed : 0)), i;
      S.pairs = [];
      while (S.pairs.length < N) {
        var a = person(rand), b = person(rand);
        if (Math.abs(a.test - b.test) > 0.8 && Math.abs(a.imp - b.imp) > 0.8 && (a.test - b.test) * (a.imp - b.imp) < 0) S.pairs.push(rand() < 0.5 ? [a, b] : [b, a]);
      }
      S.k = 0; S.log = []; task.count = 0; S.phase = "ask";
      if (w) w.render();
    }
    function stars(z) { var n = Math.max(1, Math.min(5, Math.round(3 + z / 1.2))); return "★★★★★".slice(0, n) + "☆☆☆☆☆".slice(0, 5 - n); }
    var WORDS = ["flat, hesitant", "polite, a little stiff", "pleasant, ordinary", "warm, articulate", "confident, memorable"];
    w = QB.widget(el, {
      title: "Whom would you hire?",
      sub: "Twelve pairs of candidates for the same job. Each has a test score (as a percentile) and the interviewer's impression from an unstructured interview. Press F for the left candidate, J for the right (or tap a side). At the end, see how often your choices were the better performer, against simply taking the higher test score.",
      panels: 2, height: 330, weights: [1.25, 1],
      buttons: [
        { label: "Start", act: function (state) { start(state); } },
        { label: "Clear", act: function (state) { state.seed++; S.phase = "idle"; S.log = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (S.phase === "ask") {
          var pr = S.pairs[S.k];
          ctx.save(); ctx.textAlign = "center";
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("pair " + (S.k + 1) + " of " + N, b.cx, b.y + 22);
          [0, 1].forEach(function (i) {
            var c = pr[i], x = b.x + b.w * (i ? 0.75 : 0.25), y = b.cy - 30;
            ctx.fillStyle = C.ink; ctx.font = "600 15px system-ui, sans-serif";
            ctx.fillText(i ? "Candidate B (J)" : "Candidate A (F)", x, y);
            ctx.font = "13px system-ui, sans-serif"; ctx.fillStyle = "#b39ddb";
            ctx.fillText("test: " + pct(c.test / 1.077) + "th percentile", x, y + 28);
            ctx.fillStyle = "#f2c14e"; ctx.font = "16px system-ui, sans-serif";
            ctx.fillText(stars(c.imp / 2.42), x, y + 54);
            ctx.font = "12px system-ui, sans-serif"; ctx.fillText(WORDS[Math.max(0, Math.min(4, Math.round(2 + c.imp / 2.42 / 1.2)))], x, y + 74);
          });
          ctx.restore();
        } else if (S.phase === "done") {
          var mine = S.log.filter(function (r) { return r.right; }).length, test = S.log.filter(function (r) { return r.testRight; }).length;
          var chose = S.log.filter(function (r) { return r.choseTest; }).length;
          T.message(ctx, b, "You picked the better performer " + mine + " times in " + N + "; the higher test score would have " + test + ".",
            "You chose the higher test score " + chose + " times. In these simulated candidates the test has validity about 0.3 and the unstructured impression about 0.2, so impressions mislead more often. Twelve pairs is a small sample: run it again.");
        } else {
          T.message(ctx, b, "On you", "Press Start. In each pair, one candidate has the better test score and the other the better interview impression.");
        }
        var a2 = g[1].axes({ x: [0, 3], y: [0, 1], title: "Better performer picked", noX: true });
        if (S.log.length) {
          var m = S.log.filter(function (r) { return r.right; }).length / S.log.length, t = S.log.filter(function (r) { return r.testRight; }).length / S.log.length;
          a2.bars([0.9, 2.1], [m, t], 0.7, { color: function (i) { return i ? "#b39ddb" : "#f2c14e"; } });
          a2.text(0.9, Math.min(m, 0.9) + 0.06, "you " + Math.round(100 * m) + "%", { align: "center", size: 11 });
          a2.text(2.1, Math.min(t, 0.9) + 0.06, "test " + Math.round(100 * t) + "%", { align: "center", size: 11 });
        }
        a2.hline(0.5, { color: C.muted });
      },
      readout: function () { return [["choices", String(task.count)]]; },
      note: "Nothing you choose is stored or sent. The candidates are simulated from Part 53's interview-noise model; real validities vary by job.",
    });
  };

  // ---- Part 54: two lists, one massed and one spaced.  Predict, study, a short distraction, then the test. ----
  W.spacedlists = function (el) {
    var w = null, SHOW = 1300;
    var POOL = [["harbour", "pencil"], ["violin", "garden"], ["granite", "candle"], ["meadow", "rocket"], ["lantern", "tiger"],
                ["orchard", "button"], ["saddle", "mirror"], ["compass", "pillow"], ["thimble", "forest"], ["canyon", "ladder"],
                ["walnut", "engine"], ["glacier", "spoon"]];
    var S = { phase: "idle", seq: [], k: 0, A: [], B: [], test: [], log: [], pred: null, sums: [] };
    function shuffle(a, rand) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rand() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function nextStudy() {
      if (S.k >= S.seq.length) { S.phase = "distract"; S.k = 0; if (w) w.render(); return; }
      if (w) w.render();
      task.later(function () { S.k++; nextStudy(); }, SHOW);
    }
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return S.phase === "predict" || S.phase === "study" || S.phase === "distract" || S.phase === "test"; },
      respond: function (side) {
        if (S.phase === "predict") { S.pred = side; S.phase = "study"; S.k = 0; task.count++; nextStudy(); return; }
        if (S.phase === "study") { task.clear(); task.count++; S.k++; nextStudy(); return; }
        if (S.phase === "distract") {
          task.count++; S.k++;
          if (S.k >= S.sums.length) { S.phase = "test"; S.k = 0; }
          if (w) w.render(); return;
        }
        var it = S.test[S.k];
        S.log.push({ list: it.list, right: side === it.correct });
        task.count++; S.k++;
        if (S.k >= S.test.length) S.phase = "done";
        if (w) w.render();
      },
    });
    function start(state) {
      var rand = mulberry(54 + (state ? state.seed : 0)), pairs = shuffle(POOL.slice(), rand), i;
      S.A = pairs.slice(0, 6); S.B = pairs.slice(6, 12);
      S.seq = [];
      for (i = 0; i < 6; i++) {
        S.seq.push(S.A[i], S.A[i], S.A[i]);
        S.seq.push(S.B[i], S.B[(i + 2) % 6], S.B[(i + 4) % 6]);
      }
      S.sums = [];
      for (i = 0; i < 6; i++) { var a = 3 + Math.floor(rand() * 7), b = 2 + Math.floor(rand() * 8), ok = rand() < 0.5; S.sums.push([a, b, ok ? a + b : a + b + (rand() < 0.5 ? 1 : -1)]); }
      S.test = [];
      [["massed", S.A], ["spaced", S.B]].forEach(function (L) {
        L[1].forEach(function (p, j) {
          var lure = L[1][(j + 1 + Math.floor(rand() * 5)) % 6][1], correct = rand() < 0.5 ? 0 : 1;
          S.test.push({ list: L[0], cue: p[0], opts: correct === 0 ? [p[1], lure] : [lure, p[1]], correct: correct });
        });
      });
      shuffle(S.test, rand);
      S.k = 0; S.log = []; task.count = 0; S.pred = null; S.phase = "predict"; task.clear();
      if (w) w.render();
    }
    w = QB.widget(el, {
      title: "Two lists: massed and spaced",
      sub: "Twelve word pairs. Six are shown three times in a row (massed); six are shown three times spread out (spaced). First predict which you will remember better, then watch the pairs (F or J moves on sooner), do six quick sums, and take the test: for each first word, pick its partner with F (left) or J (right).",
      panels: 2, height: 330, weights: [1.25, 1],
      buttons: [
        { label: "Start", act: function (state) { start(state); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        ctx.save(); ctx.textAlign = "center"; ctx.textBaseline = "middle";
        if (S.phase === "predict") {
          T.message(ctx, b, "Predict first", "Which list will you remember better? F: the massed list. J: the spaced list.");
        } else if (S.phase === "study") {
          var p = S.seq[Math.min(S.k, S.seq.length - 1)];
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("study " + (S.k + 1) + " of " + S.seq.length + " (F or J: next)", b.cx, b.y + 22);
          ctx.fillStyle = C.ink; ctx.font = "600 26px system-ui, sans-serif";
          ctx.fillText(p[0] + "  –  " + p[1], b.cx, b.cy);
        } else if (S.phase === "distract") {
          var q = S.sums[S.k];
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("a short break: is the sum right? F yes, J no (" + (S.k + 1) + " of 6)", b.cx, b.y + 22);
          ctx.fillStyle = C.ink; ctx.font = "600 26px system-ui, sans-serif";
          ctx.fillText(q[0] + " + " + q[1] + " = " + q[2], b.cx, b.cy);
        } else if (S.phase === "test") {
          var it = S.test[S.k];
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("test " + (S.k + 1) + " of " + S.test.length + ": which word went with it?", b.cx, b.y + 22);
          ctx.fillStyle = C.ink; ctx.font = "600 26px system-ui, sans-serif";
          ctx.fillText(it.cue, b.cx, b.cy - 30);
          ctx.font = "18px system-ui, sans-serif"; ctx.fillStyle = "#b39ddb";
          ctx.fillText("F: " + it.opts[0], b.x + b.w * 0.3, b.cy + 30);
          ctx.fillText("J: " + it.opts[1], b.x + b.w * 0.7, b.cy + 30);
        } else if (S.phase === "done") {
          var m = S.log.filter(function (r) { return r.list === "massed" && r.right; }).length;
          var s2 = S.log.filter(function (r) { return r.list === "spaced" && r.right; }).length;
          T.message(ctx, b, "Massed: " + m + " of 6.  Spaced: " + s2 + " of 6.",
            "You predicted the " + (S.pred === 0 ? "massed" : "spaced") + " list. Six pairs each is a tiny test and chance is 3 of 6, so one run proves little; the effect is clearer after a day. Try again tomorrow with new lists.");
        } else {
          T.message(ctx, b, "On you", "Press Start. First you predict, then twelve pairs, six sums and a twelve-item test.");
        }
        ctx.restore();
        var a2 = g[1].axes({ x: [0, 3], y: [0, 6], title: "Your scores (of 6)", noX: true });
        if (S.phase === "done") {
          var m2 = S.log.filter(function (r) { return r.list === "massed" && r.right; }).length;
          var sp = S.log.filter(function (r) { return r.list === "spaced" && r.right; }).length;
          a2.bars([0.9, 2.1], [m2, sp], 0.7, { color: function (i) { return i ? "#5bd18b" : "#ef6f6c"; } });
          a2.text(0.9, Math.min(m2, 5.4) + 0.4, "massed", { align: "center", size: 11 });
          a2.text(2.1, Math.min(sp, 5.4) + 0.4, "spaced", { align: "center", size: 11 });
        }
        a2.hline(3, { color: C.muted });
      },
      readout: function () { return [["responses", String(task.count)]]; },
      note: "Nothing you answer is stored or sent. In a single short session the spacing advantage is small; Part 54's simulations and studies measure it after days and weeks.",
    });
  };

  // ---- Part 55: which nudge works?  Pairwise bets on five gym interventions, then a simulated megastudy. ----
  W.gymrank = function (el) {
    var w = null;
    var ARMS = ["text reminders before planned workouts", "bonus points for returning after a missed workout",
                "a message that most members go more than you", "a signed pledge to go", "a small cash reward per visit"];
    var TRUE = [0.4, 1.6, 0.2, 0.1, 1.0]; // illustrative extra weekly visits (in tenths), simulated, not the study's
    var S = { phase: "idle", pairs: [], k: 0, wins: [0, 0, 0, 0, 0], est: null, shr: null };
    function gauss(rand) { var u = 1 - rand(), v = rand(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return S.phase === "ask"; },
      respond: function (side) {
        var pr = S.pairs[S.k]; S.wins[pr[side]]++; task.count++; S.k++;
        if (S.k >= S.pairs.length) { S.phase = "done"; }
        if (w) w.render();
      },
    });
    function start(state) {
      var rand = mulberry(55 + (state ? state.seed : 0)), i, j;
      S.pairs = [];
      for (i = 0; i < 5; i++) for (j = i + 1; j < 5; j++) S.pairs.push(rand() < 0.5 ? [i, j] : [j, i]);
      for (i = S.pairs.length - 1; i > 0; i--) { j = Math.floor(rand() * (i + 1)); var t = S.pairs[i]; S.pairs[i] = S.pairs[j]; S.pairs[j] = t; }
      S.est = TRUE.map(function (m) { return m + 0.5 * gauss(rand); });
      var mean = S.est.reduce(function (a, b) { return a + b; }, 0) / 5, wgt = 0.5;
      S.shr = S.est.map(function (e) { return mean + wgt * (e - mean); });
      S.wins = [0, 0, 0, 0, 0]; S.k = 0; task.count = 0; S.phase = "ask";
      if (w) w.render();
    }
    function rankOf(v) { var idx = [0, 1, 2, 3, 4].sort(function (a, b) { return v[b] - v[a]; }); var r = []; idx.forEach(function (x, k) { r[x] = k + 1; }); return r; }
    w = QB.widget(el, {
      title: "Which nudge works?",
      sub: "Ten pairs of interventions a gym chain could test for four weeks. For each pair, press F if you think the left one raises attendance more, J for the right one (or tap). Then see a simulated megastudy: noisy estimates, the winner shrunk, and how your ranking compares.",
      panels: 2, height: 340, weights: [1.2, 1],
      buttons: [
        { label: "Start", act: function (state) { start(state); } },
        { label: "Clear", act: function (state) { state.seed++; S.phase = "idle"; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (S.phase === "ask") {
          var pr = S.pairs[S.k];
          ctx.save(); ctx.textAlign = "center";
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("pair " + (S.k + 1) + " of " + S.pairs.length + ": which raises attendance more?", b.cx, b.y + 22);
          ctx.fillStyle = C.ink; ctx.font = "14px system-ui, sans-serif";
          T.wrap(ctx, "F: " + ARMS[pr[0]], b.x + b.w * 0.27, b.cy - 10, b.w * 0.42, 18);
          T.wrap(ctx, "J: " + ARMS[pr[1]], b.x + b.w * 0.73, b.cy - 10, b.w * 0.42, 18);
          ctx.restore();
        } else if (S.phase === "done") {
          var mine = rankOf(S.wins), truth = rankOf(TRUE), agree = 0, i;
          for (i = 0; i < 5; i++) if (mine[i] === truth[i]) agree++;
          var top = rankOf(S.est).indexOf(1);
          T.message(ctx, b, "Your top pick: " + ARMS[mine.indexOf(1)] + ".",
            "In this simulated world the noisy estimates crowned \"" + ARMS[top] + "\" (" + S.est[top].toFixed(2) + " tenths of a visit); shrunk, " + S.shr[top].toFixed(2) + ". Your ranking matched the simulated truth in " + agree + " of 5 places. Forecasters in the real megastudy did little better than chance.");
        } else {
          T.message(ctx, b, "On you", "Press Start: ten pairs of interventions, then a simulated megastudy.");
        }
        var a2 = g[1].axes({ x: [0, 5.5], y: [-0.5, 3], title: "Simulated megastudy (extra visits, tenths)", noX: true });
        if (S.phase === "done") {
          a2.bars([0.8, 1.8, 2.8, 3.8, 4.8], S.est, 0.35, { color: "#7ec8f5" });
          a2.bars([1.15, 2.15, 3.15, 4.15, 5.15], S.shr, 0.3, { color: "#b39ddb" });
          a2.dots([0.97, 1.97, 2.97, 3.97, 4.97], TRUE, { color: "#f2c14e", r: 4 });
          a2.text(0.3, 2.8, "blue: estimate  purple: shrunk  yellow: truth", { size: 10, color: C.muted });
        }
        a2.hline(0, { color: C.muted });
      },
      readout: function () { return [["choices", String(task.count)]]; },
      note: "Nothing you choose is stored or sent. The five arms are simplified descriptions and their effects are simulated for this page, not the published results.",
    });
  };

  // ---- Part 56: a line-up.  A face is shown briefly; after a pause, six faces; pick one or none, then confidence. ----
  W.lineup = function (el) {
    var w = null, SHOW = 2500, PAUSE = 2500;
    var S = { phase: "idle", culprit: null, faces: [], present: true, pick: null, conf: null, runs: [] };
    function face(rand, base) {
      var f = base ? Object.assign({}, base) : { hw: 0.8 + 0.3 * rand(), hh: 1.0 + 0.3 * rand(), eye: 0.25 + 0.15 * rand(),
                                               ey: -0.1 + 0.15 * rand(), nose: 0.15 + 0.2 * rand(), mouth: -0.2 + 0.4 * rand(),
                                               mw: 0.25 + 0.2 * rand(), hair: rand(), brow: -0.1 + 0.2 * rand() };
      if (base) { ["hw", "hh", "eye", "ey", "nose", "mouth", "mw", "hair", "brow"].forEach(function (k) { f[k] = f[k] + (rand() - 0.5) * 0.22 * (k === "hair" ? 2 : 1); }); }
      return f;
    }
    function draw(ctx, f, x, y, r, col) {
      ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.ellipse(x, y, r * f.hw * 0.5, r * f.hh * 0.6, 0, 0, 2 * Math.PI); ctx.stroke();
      ctx.beginPath(); ctx.arc(x, y - r * f.hh * 0.45, r * f.hw * 0.48, Math.PI * (1.05 + 0.1 * f.hair), Math.PI * (1.95 - 0.1 * f.hair)); ctx.stroke();
      [-1, 1].forEach(function (sgn) {
        ctx.beginPath(); ctx.arc(x + sgn * r * f.eye, y + r * f.ey, r * 0.06, 0, 2 * Math.PI); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x + sgn * r * (f.eye - 0.1), y + r * (f.ey - 0.13 - f.brow * 0.3)); ctx.lineTo(x + sgn * r * (f.eye + 0.1), y + r * (f.ey - 0.13 + f.brow * 0.3)); ctx.stroke();
      });
      ctx.beginPath(); ctx.moveTo(x, y + r * f.ey); ctx.lineTo(x, y + r * (f.ey + f.nose)); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x - r * f.mw, y + r * 0.35); ctx.quadraticCurveTo(x, y + r * (0.35 + f.mouth), x + r * f.mw, y + r * 0.35); ctx.stroke();
      ctx.restore();
    }
    var task = T.create(el, {
      keys: { "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "0": 6 },
      accepting: function () { return S.phase === "lineup" || S.phase === "confidence" || S.phase === "done"; },
      respond: function (k) {
        if (S.phase === "done") { start(w ? w.state : null); return; }
        if (S.phase === "lineup") { S.pick = k; S.phase = k === 6 ? "done" : "confidence"; task.count++; if (S.phase === "done") finish(); if (w) w.render(); return; }
        S.conf = Math.min(k + 1, 5); task.count++; S.phase = "done"; finish(); if (w) w.render();
      },
    });
    function finish() {
      var correct = S.present ? (S.pick === S.cpos) : (S.pick === 6);
      S.runs.push({ present: S.present, pick: S.pick, cpos: S.cpos, conf: S.conf, correct: correct });
    }
    function start(state) {
      var rand = mulberry(56 + (state ? state.seed : 0) * 13 + S.runs.length), i;
      S.culprit = face(rand, null);
      S.present = rand() < 0.5;
      S.faces = []; S.cpos = Math.floor(rand() * 6);
      for (i = 0; i < 6; i++) S.faces.push(S.present && i === S.cpos ? S.culprit : face(rand, S.culprit));
      S.pick = null; S.conf = null; S.phase = "show"; task.clear();
      if (w) w.render();
      task.later(function () { S.phase = "pause"; if (w) w.render(); task.later(function () { S.phase = "lineup"; if (w) w.render(); }, PAUSE); }, SHOW);
    }
    w = QB.widget(el, {
      title: "A line-up",
      sub: "A face appears for two and a half seconds. After a pause you see six faces; the person may or may not be among them. Press 1 to 6 for a face, or 0 if he is not there. Then give your confidence from 1 (a guess) to 5 (certain). Run it several times (any of those keys starts the next line-up): the person is present in about half the line-ups.",
      panels: 2, height: 330, weights: [1.3, 1],
      buttons: [
        { label: "Start", act: function (state) { start(state); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.runs = []; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), i;
        ctx.save(); ctx.textAlign = "center";
        if (S.phase === "show") {
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif"; ctx.fillText("remember this face", b.cx, b.y + 22);
          draw(ctx, S.culprit, b.cx, b.cy + 6, Math.min(b.w, b.h) * 0.32, "#f2c14e");
        } else if (S.phase === "pause") {
          T.message(ctx, b, "...", "");
        } else if (S.phase === "lineup" || S.phase === "confidence" || S.phase === "done") {
          var r = Math.min(b.w / 7.5, b.h / 4.2);
          for (i = 0; i < 6; i++) {
            var x = b.x + b.w * (0.18 + 0.32 * (i % 3)), y = b.y + b.h * (i < 3 ? 0.32 : 0.72);
            var col = S.phase === "done" && S.present && i === S.cpos ? "#5bd18b" : (S.pick === i ? "#7ec8f5" : "#cfd6e3");
            draw(ctx, S.faces[i], x, y, r, col);
            ctx.fillStyle = C.muted; ctx.font = "11px system-ui, sans-serif"; ctx.fillText(String(i + 1), x, y + r * 0.95);
          }
          ctx.fillStyle = C.ink; ctx.font = "12px system-ui, sans-serif";
          var msg = S.phase === "lineup" ? "1-6: pick a face; 0: not present" : S.phase === "confidence" ? "confidence: 1 (guess) to 5 (certain)" :
            (S.present ? "He was number " + (S.cpos + 1) + "." : "He was not in this line-up.") + (S.runs.length && S.runs[S.runs.length - 1].correct ? " You were right." : " Not this time.") + " Any key: next line-up.";
          ctx.fillText(msg, b.cx, b.y + 16);
        } else {
          T.message(ctx, b, "On you", "Press Start. Watch the face; then pick from six, or say he is not there.");
        }
        ctx.restore();
        var a2 = g[1].axes({ x: [0, 6], y: [0, 1], title: "Your line-ups", xlabel: "confidence", noY: false });
        var xs = [], ys = [], cols = [];
        S.runs.forEach(function (rr, k) { if (rr.conf) { xs.push(rr.conf + (k % 5) * 0.06); ys.push(rr.correct ? 0.85 : 0.15); cols.push(rr.correct ? "#5bd18b" : "#ef6f6c"); } });
        a2.dots(xs, ys, { color: function (i) { return cols[i]; }, r: 5 });
        a2.text(0.2, 0.95, "top: right   bottom: wrong", { size: 10, color: C.muted });
      },
      readout: function () { var n = S.runs.length, c = S.runs.filter(function (r) { return r.correct; }).length; return [["line-ups", String(n)], ["right", n ? c + " of " + n : "–"]]; },
      note: "Nothing you choose is stored or sent. The faces are simple drawings; real faces are easier and harder in other ways. Part 56's point: judge your high-confidence picks against your low-confidence ones.",
    });
  };
})();
