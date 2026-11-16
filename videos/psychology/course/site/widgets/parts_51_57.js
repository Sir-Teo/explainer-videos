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
})();
