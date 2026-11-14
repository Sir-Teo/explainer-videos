// Interactives for Act II, The Wet Machine (Parts 5-10).  As in Act I, each is an experiment the reader takes part
// in, built on the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 5: you are the cell downstream; which of two spike trains came from the stronger stimulus? ---------
  W.spiketrain = function (el) {
    var w = null, audio = null;
    var LO = 20, HI = 30, BLOCK = 12, YOU = "#f2c14e", IDEAL = "#9fd8f0";
    var S = { phase: "idle", trial: 0, win: 200, left: [], right: [], strong: 0, msg: "", ok: false, log: [], seed: 0 };

    // A Poisson train: waiting times between signals are exponential.  Times in ms, up to `ms`.
    function train(u, rate, ms) {
      var t = 0, out = [];
      for (;;) { t += -Math.log(1 - u()) / rate * 1000; if (t >= ms) break; out.push(t); }
      return out;
    }
    function pmf(k, lam) { var lp = -lam + k * Math.log(lam), i; for (i = 2; i <= k; i++) lp -= Math.log(i); return Math.exp(lp); }
    // How often a reader who simply counts is right: P(more in the stronger train) + half of P(a tie).
    function ideal(ms) {
      var a = LO * ms / 1000, b = HI * ms / 1000, n = Math.ceil(b + 10 * Math.sqrt(b) + 12), win = 0, tie = 0, below = 0, j;
      for (j = 0; j <= n; j++) { var pa = pmf(j, a), pb = pmf(j, b); win += pb * below; tie += pb * pa; below += pa; }
      return win + 0.5 * tie;
    }
    var GRID = [], CURVE = [], q;
    for (q = 50; q <= 1000; q += 25) { GRID.push(q); CURVE.push(ideal(q)); }

    function next() {
      S.trial++;
      var u = QB.rng(7001 * S.seed + 131 * S.trial + Math.round(S.win));
      S.strong = u() < 0.5 ? 0 : 1;
      var weak = train(u, LO, S.win), strong = train(u, HI, S.win);
      S.left = S.strong === 0 ? strong : weak; S.right = S.strong === 0 ? weak : strong;
      S.phase = "show"; S.msg = "";
      w.render();
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "show"; }, respond: answer });
    function answer(side) {
      if (S.phase !== "show" || !w) return;
      S.ok = side === S.strong;
      S.log.push({ win: S.win, correct: S.ok }); task.count++;
      var ns = S.strong ? S.right.length : S.left.length, nw = S.strong ? S.left.length : S.right.length;
      S.msg = (S.ok ? "Right. " : "No. ") + "The " + (S.strong ? "right" : "left") + " one: " + ns + " signals against " + nw + ".";
      S.phase = "feedback"; w.render();
      task.later(function () { if (S.trial >= BLOCK) { S.phase = "done"; w.render(); } else next(); }, 1000);
    }
    function click(when) {
      var o = audio.createOscillator(), g = audio.createGain();
      o.frequency.value = 900;
      g.gain.setValueAtTime(0.22, when); g.gain.exponentialRampToValueAtTime(0.001, when + 0.004);
      o.connect(g); g.connect(audio.destination); o.start(when); o.stop(when + 0.006);
    }
    // Adrian listened to his fibres through a loudspeaker: each signal a click.  Left recording first, then right.
    function hear() {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC || (S.phase !== "show" && S.phase !== "feedback")) return;
      try {
        audio = audio || new AC();
        var t0 = audio.currentTime + 0.05, gap = S.win / 1000 + 0.4;
        [S.left, S.right].forEach(function (tr, k) { tr.forEach(function (ms) { click(t0 + k * gap + ms / 1000); }); });
      } catch (err) { audio = null; }
    }
    function score(win) {
      var n = 0, k = 0, i;
      for (i = 0; i < S.log.length; i++) if (win === undefined || S.log[i].win === win) { n++; if (S.log[i].correct) k++; }
      return { n: n, k: k };
    }

    w = QB.widget(el, {
      title: "Reading a spike train",
      sub: "You are the cell downstream. Two recordings appear, made from one model sensory cell under two stimuli; one stimulus was stronger, and the cell answered it with 30 signals a second instead of 20. Every signal is the same size. Say which recording came from the stronger stimulus: F for the left, J for the right, or tap a side. Then change the length of the recordings and try again.",
      panels: 2, height: 340, weights: [1.35, 1],
      controls: [
        { k: "win", label: "Length of each recording", min: 50, max: 1000, step: 50, value: 200, fmt: function (x) { return x.toFixed(0) + " ms"; } },
      ],
      buttons: [
        { label: "Start", act: function (state, v) { task.clear(); S.win = v.win; S.seed++; S.trial = 0; next(); } },
        { label: "Hear this pair", act: function () { hear(); } },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.trial = 0; S.log = []; S.msg = ""; } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, task), i, k;
        ctx.save();
        ctx.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start. Twelve pairs of recordings; for each, say which came from the stronger stimulus.");
        } else if (S.phase === "done") {
          var all = score(S.win);
          T.message(ctx, b, "Block finished: " + all.k + " of " + all.n + " right at " + S.win + " ms.",
            "Move the slider to a shorter or a longer recording and press Start again. Your dots collect on the other panel, beside the curve for a reader who simply counts.");
        } else {
          ctx.textAlign = "center"; ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText(b.w < 420 ? "pair " + S.trial + " of " + BLOCK + ": which was the stronger stimulus?"
            : "pair " + S.trial + " of " + BLOCK + ", " + S.win + " ms each: which came from the stronger stimulus?", b.cx, b.y + 26);
          ctx.strokeStyle = "#1b2230"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(b.cx, b.y + 48); ctx.lineTo(b.cx, b.y + b.h - 62); ctx.stroke();
          var halves = [S.left, S.right];
          for (k = 0; k < 2; k++) {
            var x0 = (k ? b.cx + 14 : b.x + 22), x1 = (k ? b.x + b.w - 22 : b.cx - 14), y = b.cy - 6, tr = halves[k];
            ctx.strokeStyle = "#2a3242"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x0, y + 26); ctx.lineTo(x1, y + 26); ctx.stroke();
            ctx.strokeStyle = S.phase === "feedback" && k === S.strong ? YOU : C.ink; ctx.lineWidth = 2; ctx.beginPath();
            for (i = 0; i < tr.length; i++) { var x = x0 + (x1 - x0) * tr[i] / S.win; ctx.moveTo(x, y - 26); ctx.lineTo(x, y + 26); }
            ctx.stroke();
            ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
            ctx.fillText(k ? "J, or tap here" : "F, or tap here", (x0 + x1) / 2, b.y + b.h - 46);
          }
          if (S.phase === "feedback") {
            ctx.fillStyle = S.ok ? YOU : C.loss; ctx.font = "600 13px system-ui, sans-serif";
            ctx.fillText(S.msg, b.cx, b.y + b.h - 22);
          }
        }
        ctx.restore();

        var a = g[1].axes({ x: [40, 1200], y: [0.4, 1.03], logx: true, title: "How often right, by length of recording", xlabel: "length of each recording (ms)" });
        a.hline(0.5, { color: C.muted });
        a.text(45, 0.53, "guessing", { color: C.muted, dx: 4, size: 11 });
        a.line(GRID, CURVE, { color: IDEAL });
        a.text(1000, 0.72, "a reader who counts", { color: IDEAL, align: "right", dx: -4, size: 11 });
        var seen = {}, xs = [], ys = [];
        for (i = 0; i < S.log.length; i++) seen[S.log[i].win] = true;
        for (k in seen) { var sc = score(Number(k)); xs.push(Number(k)); ys.push(sc.k / sc.n); }
        if (xs.length) {
          a.dots(xs, ys, { color: YOU, r: 6, alpha: 0.95 });
          a.text(45, 0.97, "you", { color: YOU, dx: 4, size: 11.5, bold: true });
        } else {
          a.text(45, 0.97, "Your answers appear here as dots.", { color: C.muted, dx: 4, size: 11.5 });
        }
        a.vline(v.win, { color: "#2a3242" });
      },
      readout: function (v) {
        var all = score(), here = score(S.win);
        return [
          ["pairs answered", String(all.n)],
          ["right so far", all.n ? QB.pct(all.k / all.n, 0) : "–"],
          ["at " + S.win + " ms", here.n ? here.k + " of " + here.n : "–"],
          ["a reader who counts, at the slider's length", QB.pct(ideal(v ? v.win : S.win), 0)],
        ];
      },
      note: "Nothing you answer is stored or sent: it lives in this page and is gone when you close it. The recordings are simulated: a model cell that fires at random moments, 20 times a second under the weaker stimulus and 30 under the stronger. With a long recording the difference is plain. With a short one it often is not, and nobody could do better: the curve is the best that any reader can manage by counting, about 62% for 50 ms and 92% for a second. A brain has to act within a fraction of a second, so it cannot count one cell for long. It reads many cells at once instead, which is one reason it has so many. Press Hear this pair to listen as Adrian did in 1926, with each signal a click (left recording first).",
    });
  };

  // ---- Part 6: the Hermann grid with straighter or wavier streets; do you see the grey spots? --------------------
  W.gridspots = function (el) {
    var w = null;
    // waviness: the amplitude of each street's sine, as a share of the street's width
    var LEVELS = [0, 0.1, 0.2, 0.3, 0.4, 0.6], BLOCK = 12, YOU = "#f2c14e", MODEL = "#5bd18b";
    // The receptive-field account, computed by Psyche (psyche/circuits.py, hermann_response): how much dimmer a
    // centre-surround filter makes a crossing than a street, relative to the straight grid.
    var PRED = [1.0, 0.95, 0.91, 0.78, 0.63, 0.36];
    var S = { phase: "idle", trial: 0, level: 0, order: [], log: [], seed: 0, img: null, key: "" };

    function grid(wave, px) {
      // five squares of 4 units with streets of 1 unit, as in the film: 26 units across
      var n = Math.max(130, Math.min(390, Math.round(px / 26) * 26)), unit = n / 26, street = unit, period = 5 * unit;
      var c = document.createElement("canvas"); c.width = n; c.height = n;
      var ctx = c.getContext("2d"), im = ctx.createImageData(n, n), d = im.data, x, y, k, on, amp = wave * street, i = 0;
      var sx = new Float32Array(n), cen = [];
      for (k = 0; k <= 5; k++) cen.push(k * period + street / 2);
      for (x = 0; x < n; x++) sx[x] = amp * Math.sin(2 * Math.PI * (x + 0.5 - street / 2) / period);
      for (y = 0; y < n; y++) {
        for (x = 0; x < n; x++) {
          on = false;
          for (k = 0; k <= 5 && !on; k++) {
            if (Math.abs(y + 0.5 - cen[k] - sx[x]) < street / 2 || Math.abs(x + 0.5 - cen[k] - sx[y]) < street / 2) on = true;
          }
          d[i] = d[i + 1] = d[i + 2] = on ? 255 : 0; d[i + 3] = 255; i += 4;
        }
      }
      ctx.putImageData(im, 0, 0);
      return c;
    }
    function next() {
      S.trial++;
      S.level = S.order[(S.trial - 1) % S.order.length];
      S.phase = "show"; S.img = null;
      w.render();
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "show"; }, respond: answer });
    function answer(side) {
      if (S.phase !== "show" || !w) return;
      S.log.push({ level: S.level, spots: side === 0 }); task.count++;
      S.phase = "gap"; w.render();
      task.later(function () { if (S.trial >= BLOCK) { S.phase = "done"; w.render(); } else next(); }, 450);
    }
    function share(level) {
      var n = 0, k = 0, i;
      for (i = 0; i < S.log.length; i++) if (level === undefined || S.log[i].level === level) { n++; if (S.log[i].spots) k++; }
      return { n: n, k: k };
    }

    w = QB.widget(el, {
      title: "A grid of grey spots",
      sub: "Black squares and white streets. Look at the whole grid for a moment, not at any one crossing, and say whether faint grey spots sit on the crossings: F if you see them, J if you do not (or tap the left or the right half). The streets are straight on some trials and wavy on others. Twelve grids make a block.",
      panels: 2, height: 360, weights: [1.25, 1],
      controls: [],
      buttons: [
        { label: "Start", act: function () {
          task.clear(); S.seed++; S.trial = 0;
          var u = QB.rng(6001 * S.seed + 17), pool = LEVELS.concat(LEVELS), i, j, t;
          for (i = pool.length - 1; i > 0; i--) { j = Math.floor(u() * (i + 1)); t = pool[i]; pool[i] = pool[j]; pool[j] = t; }
          S.order = pool; next();
        } },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.trial = 0; S.log = []; S.img = null; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), i;
        ctx.save();
        ctx.textBaseline = "middle"; ctx.textAlign = "center";
        if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start. Twelve grids, some with straight streets and some with wavy ones; for each, say whether you see grey spots at the crossings.");
        } else if (S.phase === "done") {
          var st = share(0), wv = share(0.6);
          T.message(ctx, b, "Block finished.",
            "Straight streets: spots on " + st.k + " of " + st.n + ". The waviest: on " + wv.k + " of " + wv.n + ". Press Start for another block; your answers collect on the other panel, beside what the receptive-field account predicts.");
        } else if (S.phase === "show") {
          var side = Math.max(60, Math.min(b.w - 40, b.h - 86)), key = S.level + ":" + Math.round(side);
          if (!S.img || S.key !== key) { S.img = grid(S.level, side); S.key = key; }
          ctx.imageSmoothingEnabled = false;
          ctx.drawImage(S.img, b.cx - side / 2, b.y + 40, side, side);
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("grid " + S.trial + " of " + BLOCK, b.cx, b.y + 22);
          ctx.fillText(b.w < 420 ? "F / left: spots      J / right: none" : "F, or tap the left half: I see spots        J, or tap the right half: none",
            b.cx, b.y + b.h - 24);
        }
        ctx.restore();

        var a = g[1].axes({ x: [-0.05, 0.68], y: [-0.05, 1.12], title: "Spots seen, by the waviness of the streets", xlabel: "waviness (share of a street's width)" });
        a.hline(0, { color: "#2a3242" });
        a.line(LEVELS, PRED, { color: MODEL });
        a.text(0.66, PRED[5] - 0.16, "the receptive-field account", { color: MODEL, align: "right", size: 11 });
        var xs = [], ys = [];
        for (i = 0; i < LEVELS.length; i++) { var sc = share(LEVELS[i]); if (sc.n) { xs.push(LEVELS[i]); ys.push(sc.k / sc.n); } }
        if (xs.length) {
          a.dots(xs, ys, { color: YOU, r: 6, alpha: 0.95 });
          a.text(-0.04, 1.06, "you: share of grids with spots", { color: YOU, dx: 2, size: 11.5, bold: true });
        } else {
          a.text(-0.04, 1.06, "Your answers appear here as dots.", { color: C.muted, dx: 2, size: 11.5 });
        }
      },
      readout: function () {
        var all = share(), st = share(0), wv = share(0.6);
        return [
          ["grids judged", String(all.n)],
          ["spots on straight streets", st.n ? st.k + " of " + st.n : "–"],
          ["spots on the waviest", wv.n ? wv.k + " of " + wv.n : "–"],
          ["the account's dimming at the waviest", QB.pct(PRED[5], 0) + " of straight"],
        ];
      },
      note: "Nothing you answer is stored or sent: it lives in this page and is gone when you close it. The green line is not data. It is the textbook explanation, computed: a centre-surround filter makes a crossing dimmer than a street because more of its surround is lit, and the line shows how much dimmer, relative to the straight grid. On that account the spots should fade gradually as the streets bend, and should still be there at moderate waviness. Geier and his colleagues reported in 2008 that for most observers a slight curve is enough to abolish them. If your dots fall to zero while the line is still high, you have repeated the observation that put the explanation in doubt. There is no right answer on any trial: the experiment is asking what you see. The effect depends on the size of the grid on your screen and on where you look, so try it at arm's length without fixing on one crossing.",
    });
  };
  // Part 7: find the blind spot of your right eye, and measure it.  A dot crosses the panel while you look at a
  // cross; you press when it vanishes and again when it returns.  Sweeps run outward and inward by turns, so the
  // time you take to react shifts the two edges in opposite directions and cancels in the average.
  W.blindspot = function (el) {
    var w = null, raf = 0;
    var BLOCK = 4, DUR = 9000, X0 = 0.07, FROM = 0.18, TO = 0.95, YOU = "#f2c14e", TYP = "#5bd18b";
    var CENTRE = 15, NEAR = 12.25, FAR = 17.75, RAD = Math.PI / 180;   // a typical eye, in degrees from fixation
    var S = { phase: "idle", sweep: 0, t0: 0, presses: [], log: [], missed: 0 };

    function frac() { return Math.min(1, (T.now() - S.t0) / DUR); }
    function outward() { return S.sweep % 2 === 1; }
    // the dot's distance from the cross, as a share of the panel's width
    function offset() { var f = frac(), u = outward() ? f : 1 - f; return FROM + (TO - FROM) * u - X0; }
    function stop() { if (raf) { cancelAnimationFrame(raf); raf = 0; } }
    function tick() {
      raf = 0;
      if (S.phase !== "sweep" || !w) return;
      if (frac() >= 1) { finish(); return; }
      w.render();
      raf = requestAnimationFrame(tick);
    }
    function begin() {
      S.sweep++; S.presses = []; S.t0 = T.now(); S.phase = "sweep";
      w.render(); stop(); raf = requestAnimationFrame(tick);
    }
    function finish() {
      stop();
      if (S.presses.length === 2) {
        S.log.push({ near: Math.min(S.presses[0], S.presses[1]), far: Math.max(S.presses[0], S.presses[1]), out: outward() });
      } else S.missed++;
      S.phase = "gap"; w.render();
      task.later(function () { if (S.sweep >= BLOCK) { S.phase = "done"; w.render(); } else begin(); }, 700);
    }
    var task = T.create(el, { keys: { " ": 0 }, accepting: function () { return S.phase === "sweep" && S.presses.length < 2; }, respond: press });
    function press() {
      if (S.phase !== "sweep" || S.presses.length >= 2 || !w) return;
      S.presses.push(offset()); task.count++;
      if (S.presses.length === 2) finish(); else w.render();
    }
    function mean() {
      var n = S.log.length, a = 0, b = 0, i;
      for (i = 0; i < n; i++) { a += S.log[i].near; b += S.log[i].far; }
      return n ? { n: n, near: a / n, far: b / n, centre: (a + b) / (2 * n) } : { n: 0 };
    }
    // If the middle of your blind spot is CENTRE degrees out, your eye is centre / tan(CENTRE) from the screen
    // (in panel widths), and an offset x on the screen is atan(x / distance) degrees out.
    function degrees(x, m) { var d = m.centre / Math.tan(CENTRE * RAD); return Math.atan(x / d) / RAD; }

    w = QB.widget(el, {
      title: "Find your blind spot, and measure it",
      sub: "Close your left eye and look at the cross with your right. Sit about one and a half times the black panel's width from the screen. A dot crosses the panel: press the space bar (or tap the panel) the moment it vanishes, and again the moment it comes back. Keep looking at the cross.",
      panels: 2, height: 340, weights: [1.7, 1],
      controls: [],
      buttons: [
        { label: "Start", act: function () { task.clear(); stop(); S.sweep = 0; begin(); } },
        { label: "Clear", act: function () { task.clear(); stop(); S.phase = "idle"; S.sweep = 0; S.presses = []; S.log = []; S.missed = 0; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), m = mean(), i;
        var cx = b.x + X0 * b.w, cy = b.cy - 8;
        ctx.save();
        ctx.textBaseline = "middle"; ctx.textAlign = "center";
        if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start. Four sweeps: the dot goes out, comes back, goes out, comes back. If it never vanishes, move a little closer to the screen or further from it and start again.");
        } else if (S.phase === "done") {
          T.message(ctx, b, "Block finished.", m.n
            ? "Your blind spot begins " + QB.pct(m.near, 0) + " of the panel's width from the cross and ends at " + QB.pct(m.far, 0) + ". Press Start for four more sweeps; they are averaged with these."
            : "No sweep had both presses. If the dot never vanished, change your distance from the screen and press Start.");
        } else {
          ctx.strokeStyle = C.ink; ctx.lineWidth = 2.5; ctx.beginPath();
          ctx.moveTo(cx - 8, cy); ctx.lineTo(cx + 8, cy); ctx.moveTo(cx, cy - 8); ctx.lineTo(cx, cy + 8); ctx.stroke();
          if (S.phase === "sweep") {
            ctx.fillStyle = YOU; ctx.beginPath(); ctx.arc(cx + offset() * b.w, cy, Math.max(4, b.w / 110), 0, 6.2832); ctx.fill();
          }
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("sweep " + S.sweep + " of " + BLOCK + (outward() ? ": outward" : ": inward"), b.cx, b.y + 22);
          ctx.fillText(S.presses.length === 0 ? "space, or tap: it has vanished" : S.presses.length === 1 ? "space, or tap: it is back" : "",
            b.cx, b.y + b.h - 24);
        }
        ctx.restore();

        var a = g[1].axes({ x: [8, 22], y: [0, 6.2], title: "The hole, if its middle is 15 degrees out", xlabel: "degrees from where you are looking" });
        a.line([NEAR, FAR], [5.3, 5.3], { color: TYP, width: 7 });
        a.text(NEAR, 5.85, "a typical eye: 5.5 degrees wide", { color: TYP, size: 11 });
        if (m.n) {
          var shown = S.log.slice(-4);
          for (i = 0; i < shown.length; i++) {
            a.line([degrees(shown[i].near, m), degrees(shown[i].far, m)], [3.6 - 0.75 * i, 3.6 - 0.75 * i], { color: YOU, width: 3 });
            a.text(21.8, 3.6 - 0.75 * i, shown[i].out ? "out" : "in", { color: C.muted, align: "right", size: 10.5 });
          }
          a.line([degrees(m.near, m), degrees(m.far, m)], [4.45, 4.45], { color: YOU, width: 7 });
          a.text(8.2, 4.45, "you", { color: YOU, size: 11.5, bold: true });
        } else {
          a.text(8.2, 3.4, "Your sweeps appear here.", { color: C.muted, size: 11.5 });
        }
      },
      readout: function () {
        var m = mean();
        return [
          ["sweeps with both presses", String(m.n) + (S.missed ? " (" + S.missed + " without)" : "")],
          ["width of the hole, over its distance out", m.n ? ((m.far - m.near) / m.centre).toFixed(2) + " (typical: 0.38)" : "–"],
          ["its width, if centred 15 degrees out", m.n ? (degrees(m.far, m) - degrees(m.near, m)).toFixed(1) + " degrees" : "–"],
          ["your eye's distance from the screen", m.n ? (m.centre / Math.tan(CENTRE * RAD)).toFixed(1) + " panel widths" : "–"],
        ];
      },
      note: "Nothing you press is stored or sent: it lives in this page and is gone when you close it. The page cannot know how far you sit from the screen, so it reports what does not depend on that: the hole's width as a share of its distance from where you look. To turn that into degrees it assumes the middle of your blind spot is 15 degrees out, which is typical, and eyes differ. You react a little late, which moves both edges outward on an outward sweep and inward on an inward one; averaging the two directions cancels it. The green bar is a textbook value, not a measurement of you.",
    });
  };
  // Part 8: a reported correlation between a brain measure and a questionnaire, with the reliability of each.
  // Could it be true?  Two measures cannot correlate more than the square root of the product of their
  // reliabilities, whatever the brain is doing.
  W.impossible = function (el) {
    var w = null;
    var BLOCK = 12, N = 16, YOU = "#f2c14e", OK = "#5bd18b", BAD = "#ef6f6c", DOT = "#f28fb8";
    var RX = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8], RY = [0.6, 0.7, 0.8, 0.9], DELTA = [-0.25, -0.15, -0.07, 0.07, 0.15, 0.25];
    var S = { phase: "idle", trial: 0, seed: 0, cur: null, log: [], last: null };

    function sample(u, r) {
      // N points whose sample correlation is exactly r
      var x = [], y = [], i, mx = 0, my = 0, sx = 0, sy = 0, sxy = 0;
      function g() { var a = 0, k; for (k = 0; k < 6; k++) a += u(); return (a - 3) * 1.414; }
      for (i = 0; i < N; i++) { x.push(g()); y.push(g()); mx += x[i] / N; my += y[i] / N; }
      for (i = 0; i < N; i++) { x[i] -= mx; y[i] -= my; sx += x[i] * x[i]; }
      sx = Math.sqrt(sx / N);
      for (i = 0; i < N; i++) { x[i] /= sx; sxy += x[i] * y[i] / N; }
      for (i = 0; i < N; i++) { y[i] -= sxy * x[i]; sy += y[i] * y[i]; }
      sy = Math.sqrt(sy / N);
      for (i = 0; i < N; i++) y[i] = r * x[i] + Math.sqrt(1 - r * r) * y[i] / sy;
      return { x: x, y: y };
    }
    function next() {
      S.trial++;
      var u = QB.rng(8101 * S.seed + 37 * S.trial + 5);
      var rx = RX[Math.floor(u() * RX.length)], ry = RY[Math.floor(u() * RY.length)];
      var ceil = Math.sqrt(rx * ry), d = DELTA[(S.trial + S.seed) % DELTA.length];
      var r = Math.max(0.1, Math.min(0.97, Math.round((ceil + d) * 100) / 100));
      if (Math.abs(r - ceil) < 0.03) r = Math.round((ceil + (d > 0 ? 0.06 : -0.06)) * 100) / 100;
      S.cur = { rx: rx, ry: ry, ceil: ceil, r: r, pts: sample(u, r), impossible: r > ceil };
      S.phase = "show"; w.render();
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "show"; }, respond: answer });
    function answer(side) {
      if (S.phase !== "show" || !w) return;
      var said = side === 1, right = said === S.cur.impossible;
      S.last = { right: right, ceil: S.cur.ceil, impossible: S.cur.impossible };
      S.log.push({ r: S.cur.r, ceil: S.cur.ceil, said: said, right: right }); task.count++;
      S.phase = "feedback"; w.render();
      task.later(function () { if (S.trial >= BLOCK) { S.phase = "done"; w.render(); } else next(); }, 1400);
    }
    function score() { var k = 0, i; for (i = 0; i < S.log.length; i++) if (S.log[i].right) k++; return { n: S.log.length, k: k }; }

    w = QB.widget(el, {
      title: "Possible, or impossible?",
      sub: "Each plot is a result of the kind brain-imaging papers report: sixteen people, a questionnaire score across and a brain measure up. You are told the correlation and how reliable each measure is. Press F if the result could be true, J if it cannot be.",
      panels: 2, height: 360, weights: [1.35, 1],
      controls: [],
      buttons: [
        { label: "Start", act: function () { task.clear(); S.seed++; S.trial = 0; next(); } },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.trial = 0; S.log = []; S.cur = null; S.last = null; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), i, sc = score();
        ctx.save();
        ctx.textBaseline = "middle"; ctx.textAlign = "center";
        if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start. Twelve results. For each, decide from the two reliabilities whether the reported correlation is possible.");
        } else if (S.phase === "done") {
          T.message(ctx, b, "Block finished.", "You judged " + sc.k + " of " + sc.n + " correctly. The rule: a correlation cannot exceed the square root of the product of the two reliabilities. Press Start for another block.");
        } else {
          var c = S.cur, side = Math.max(70, Math.min(b.h - 110, b.w * 0.42)), x0 = b.x + 28, y0 = b.y + 44;
          ctx.strokeStyle = "#2a3242"; ctx.lineWidth = 1; ctx.strokeRect(x0, y0, side, side);
          ctx.fillStyle = DOT;
          for (i = 0; i < N; i++) {
            ctx.beginPath();
            ctx.arc(x0 + side / 2 + c.pts.x[i] * side / 5.6, y0 + side / 2 - c.pts.y[i] * side / 5.6, 3.5, 0, 6.2832); ctx.fill();
          }
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("result " + S.trial + " of " + BLOCK, b.cx, b.y + 22);
          var tx = x0 + side + 18, ty = y0 + 14; ctx.textAlign = "left";
          ctx.fillStyle = C.ink; ctx.font = "600 17px system-ui, sans-serif"; ctx.fillText("r = " + c.r.toFixed(2), tx, ty);
          ctx.fillStyle = C.muted; ctx.font = "12.5px system-ui, sans-serif";
          ctx.fillText("reliability of the", tx, ty + 34); ctx.fillText("brain measure: " + c.rx.toFixed(1), tx, ty + 51);
          ctx.fillText("reliability of the", tx, ty + 80); ctx.fillText("questionnaire: " + c.ry.toFixed(1), tx, ty + 97);
          ctx.textAlign = "center";
          if (S.phase === "feedback" && S.last) {
            ctx.fillStyle = S.last.right ? OK : BAD; ctx.font = "600 13px system-ui, sans-serif";
            ctx.fillText((S.last.right ? "Right. " : "No. ") + "The ceiling is " + S.last.ceil.toFixed(2) + ": " + (S.last.impossible ? "impossible." : "it could be true."),
              b.cx, b.y + b.h - 24);
          } else {
            ctx.fillText(b.w < 420 ? "F / left: possible      J / right: impossible" : "F, or tap the left half: could be true        J, or tap the right half: impossible",
              b.cx, b.y + b.h - 24);
          }
        }
        ctx.restore();

        var a = g[1].axes({ x: [0.3, 1.0], y: [0, 1.05], title: "Each result against its ceiling", xlabel: "the ceiling: square root of (reliability x reliability)" });
        a.line([0.3, 1.0], [0.3, 1.0], { color: C.muted, width: 1.5 });
        a.text(0.32, 0.88, "above the line: impossible", { color: C.muted, size: 11 });
        if (S.log.length) {
          var xs = [], ys = [], cols = [];
          for (i = 0; i < S.log.length; i++) { xs.push(S.log[i].ceil); ys.push(S.log[i].r); cols.push(S.log[i].right ? OK : BAD); }
          a.dots(xs, ys, { color: function (k) { return cols[k]; }, r: 5, alpha: 0.95 });
          a.text(0.32, 0.98, "green: you were right", { color: OK, size: 11.5, bold: true });
        } else {
          a.text(0.32, 0.98, "Your answers appear here.", { color: C.muted, size: 11.5 });
        }
        a.text(0.32, 0.06, "reported correlation, upward", { color: C.muted, size: 10.5 });
      },
      readout: function () {
        var sc = score();
        return [
          ["results judged", String(sc.n)],
          ["judged correctly", sc.n ? sc.k + " of " + sc.n : "–"],
          ["ceiling for reliabilities 0.5 and 0.8", "0.63"],
          ["ceiling with task fMRI's typical 0.4", "0.57"],
        ];
      },
      note: "Nothing you answer is stored or sent: it lives in this page and is gone when you close it. The plots are generated here, each with exactly the correlation shown. The rule is Part 3's: if two measures have reliabilities Rx and Ry, the correlation between them cannot exceed the square root of Rx times Ry, even when what they measure is perfectly related. A published correlation above that line was selected, or is a lucky small sample.",
    });
  };
})();
