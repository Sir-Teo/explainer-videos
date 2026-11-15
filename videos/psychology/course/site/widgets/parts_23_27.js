// Interactives for Act V continued, Thinking (Parts 23-27).  Each is an experiment the reader takes part in, built on
// the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 23: a made-up language.  Watch a stream of syllables, then find its words ---------------------------
  W.stream = function (el) {
    var w = null, GOLD = "#f2c14e", BLUE = "#7ec8f5", GREEN = "#5bd18b", RED = "#ef6f6c", GREY = "#9aa4b2";
    var CONS = "bdgklmnprt", VOW = "aiou";
    var KEYS = { f: 0, j: 1 };
    var S = { phase: "idle", seed: 0, words: [], stream: [], k: 0, flagged: [], hits: 0, cover: 0, test: [], t: 0,
              answers: [], tp: [] };
    function build() {
      var u = QB.rng(48611 * S.seed + 7), pool = [], i, j;
      for (i = 0; i < CONS.length; i++) for (j = 0; j < VOW.length; j++) pool.push(CONS[i] + VOW[j]);
      for (i = pool.length - 1; i > 0; i--) { j = Math.floor(u() * (i + 1)); var t = pool[i]; pool[i] = pool[j]; pool[j] = t; }
      S.words = [pool.slice(0, 3), pool.slice(3, 6), pool.slice(6, 9), pool.slice(9, 12)];
      // 48 words in random order, no word twice running: 144 syllables
      S.stream = []; S.flagged = [];
      var prev = -1;
      for (i = 0; i < 48; i++) {
        var k = prev;
        while (k === prev) k = Math.floor(u() * 4);
        prev = k;
        S.words[k].forEach(function (s) { S.stream.push(s); S.flagged.push(u() < 0.06); });
      }
      // transitional probabilities, as Psyche computes them
      var pair = {}, first = {};
      for (i = 0; i + 1 < S.stream.length; i++) {
        var key = S.stream[i] + "|" + S.stream[i + 1];
        pair[key] = (pair[key] || 0) + 1; first[S.stream[i]] = (first[S.stream[i]] || 0) + 1;
      }
      S.tp = [];
      for (i = 0; i + 1 < S.stream.length; i++) S.tp.push(pair[S.stream[i] + "|" + S.stream[i + 1]] / first[S.stream[i]]);
      // the test: each word against a part-word made of the end of one word and the start of another
      var tests = [];
      for (i = 0; i < 4; i++) {
        var other = S.words[(i + 1) % 4];
        var part = [S.words[i][2], other[0], other[1]];
        tests.push({ word: S.words[i].join(""), part: part.join(""), wordLeft: u() < 0.5 });
        var part2 = [S.words[i][1], S.words[i][2], other[0]];
        tests.push({ word: S.words[(i + 2) % 4].join(""), part: part2.join(""), wordLeft: u() < 0.5 });
      }
      S.test = tests;
    }
    function scoreTP(item) {  // mean transitional probability inside a candidate, from the stream
      var syl = [item.slice(0, 2), item.slice(2, 4), item.slice(4, 6)], pair = {}, first = {}, i;
      for (i = 0; i + 1 < S.stream.length; i++) {
        var key = S.stream[i] + "|" + S.stream[i + 1];
        pair[key] = (pair[key] || 0) + 1; first[S.stream[i]] = (first[S.stream[i]] || 0) + 1;
      }
      var a = (pair[syl[0] + "|" + syl[1]] || 0) / (first[syl[0]] || 1), b = (pair[syl[1] + "|" + syl[2]] || 0) / (first[syl[1]] || 1);
      return (a + b) / 2;
    }
    function next() {
      if (S.k >= S.stream.length) { S.phase = "test"; S.t = 0; w.render(); return; }
      S.phase = "listen"; w.render();
      task.later(function () { S.k++; next(); }, Math.round(1000 * (S.secs || 0.25)));
    }
    function start() {
      task.clear(); S.seed++; build(); S.k = 0; S.hits = 0; S.cover = 0; S.answers = [];
      S.phase = "listen"; w.render(); task.later(next, 300);
    }
    var task = T.create(el, { keys: KEYS, accepting: function () { return S.phase === "listen" || S.phase === "test"; },
                              respond: answer });
    function answer(side) {
      if (S.phase === "listen") {  // the cover task: press J (or tap right) for a blue syllable
        task.count++;
        if (side === 1) { S.cover++; if (S.flagged[Math.min(S.k, S.flagged.length - 1)]) S.hits++; }
        return;
      }
      if (S.phase !== "test") return;
      task.count++;
      var item = S.test[S.t], choseLeft = side === 0;
      S.answers.push({ correct: choseLeft === item.wordLeft });
      S.t++;
      if (S.t >= S.test.length) S.phase = "done";
      w.render();
    }

    w = QB.widget(el, {
      title: "A language in two minutes: find its words",
      sub: "A stream of syllables from a made-up language, with no spaces, one syllable at a time (about 40 seconds). To keep your eyes on it, press J (or tap right) when a syllable turns blue. Then eight pairs: which of the two was a word of the language? F (or tap left) for the left one, J (or tap right) for the right one.",
      panels: 2, height: 330, weights: [1.2, 1],
      controls: [{ k: "secs", label: "Seconds per syllable", min: 0.2, max: 0.5, step: 0.01, value: 0.25,
                   fmt: function (x) { return x.toFixed(2) + " s"; } }],
      onChange: function (v) { S.secs = v.secs; },
      buttons: [
        { label: "Start", act: start },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.answers = []; } },
      ],
      draw: function (g, v) {
        if (v && v.secs) S.secs = v.secs;
        var c = g.ctx, b = T.stage(g, 0, task);
        c.save(); c.textAlign = "center"; c.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(c, b, "On you", "Press Start. Syllables from a language you have never heard will appear one at a time, with no gaps between words. Just watch, and press J when one turns blue. Then you will be asked to pick out its words.");
        } else if (S.phase === "listen") {
          var s = S.stream[Math.min(S.k, S.stream.length - 1)] || "";
          c.fillStyle = S.flagged[S.k] ? BLUE : C.ink; c.font = "600 40px system-ui, sans-serif";
          c.fillText(s, b.cx, b.cy);
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("syllable " + (S.k + 1) + " of " + S.stream.length, b.cx, b.y + b.h - 18);
        } else if (S.phase === "test") {
          var item = S.test[S.t], L = item.wordLeft ? item.word : item.part, R = item.wordLeft ? item.part : item.word;
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("pair " + (S.t + 1) + " of " + S.test.length + ": which was a word of the language?", b.cx, b.y + 20);
          c.fillStyle = GOLD; c.font = "600 32px system-ui, sans-serif";
          c.fillText(L, b.x + b.w * 0.27, b.cy); c.fillText(R, b.x + b.w * 0.73, b.cy);
          c.fillStyle = GREY; c.font = "13px system-ui, sans-serif";
          c.fillText("F: left", b.x + b.w * 0.27, b.y + b.h - 22); c.fillText("J: right", b.x + b.w * 0.73, b.y + b.h - 22);
        } else if (S.phase === "done") {
          T.message(c, b, "Finished.", "The words were " + S.words.map(function (x) { return x.join(""); }).join(", ") + ". On the right: your score, chance, and Psyche's, which only counts which syllable follows which.");
        }
        c.restore();

        var n = S.answers.length, mine = n ? S.answers.filter(function (a) { return a.correct; }).length / n : NaN;
        var psyche = S.test.length ? S.test.filter(function (t) { return scoreTP(t.word) > scoreTP(t.part); }).length / S.test.length : NaN;
        if (S.phase === "listen" && S.tp.length) {
          var a = g[1].axes({ x: [0, 30], y: [0, 1.05], xticks: [], yticks: [0, 0.5, 1],
            title: "Transitional probability, last 30 syllables", xlabel: "", ylabel: "P(next | this)" });
          var lo = Math.max(0, Math.min(S.k, S.tp.length) - 30), xs = [], ys = [];
          for (var i = lo; i < Math.min(S.k, S.tp.length); i++) { xs.push(i - lo); ys.push(S.tp[i]); }
          if (xs.length) { a.line(xs, ys, { color: GREEN, width: 2 }); a.dots(xs, ys, { color: GREEN, r: 3 }); }
        } else {
          var a2 = g[1].axes({ x: [0, 3], y: [0, 1], xticks: [], yticks: [0, 0.5, 1],
            title: "Words chosen over part-words", xlabel: "you        chance        Psyche", ylabel: "share right" });
          if (!isNaN(mine)) a2.bars([0.5], [mine], 0.55, { color: GOLD });
          a2.bars([1.5], [0.5], 0.55, { color: GREY, alpha: 0.5 });
          if (!isNaN(psyche) && S.phase === "done") a2.bars([2.5], [psyche], 0.55, { color: GREEN });
        }
      },
      readout: function () {
        var n = S.answers.length, f = function (x) { return isNaN(x) ? "–" : Math.round(100 * x) + "%"; };
        var mine = n ? S.answers.filter(function (a) { return a.correct; }).length / n : NaN;
        return [["pairs answered", n + " of 8"], ["you chose the word", f(mine)], ["chance", "50%"],
                ["blue syllables spotted", S.hits + ""]];
      },
      note: "Nothing you do is stored or sent. Each run makes a new language of four three-syllable words, as in Saffran, Aslin and Newport (1996), whose eight-month-olds heard two minutes of such a stream. Inside a word the next syllable is certain; across a boundary it is one of three. Psyche's learner (language.transitional_probabilities) uses nothing else. With eight pairs your own score is rough: 6 or more right is better than chance would usually give.",
    });
  };

  // ---- Part 24: mental rotation on you.  Same shape, or its mirror image? --------------------------------------
  W.rotation = function (el) {
    var w = null, SAME = "#5bd18b", MIRROR = "#ef6f6c", SHAPE = "#7ec8f5", REF = "#9aa4b2";
    var ANGLES = [0, 60, 120, 180];
    // the F-pentomino: it has no mirror symmetry, so a turned copy and a mirrored copy can always be told apart
    var CELLS = [[1, 0], [2, 0], [0, 1], [1, 1], [1, 2]];
    // Ganis and Kievit (2015): mean of 54 people's times on correct "same" trials, at 0, 50, 100 and 150 degrees
    var GK = { x: [0, 50, 100, 150], y: [1563, 2461, 3053, 3341] };
    var run = T.timed(el, {
      keys: { f: 0, j: 1 },
      trials: function () { return w.v.n; },
      seed: function () { return w.state.seed; },
      stimulus: function (rand) {
        return { angle: ANGLES[Math.floor(rand() * 4)], mirror: rand() < 0.5, spin: rand() * 360 };
      },
      correct: function (stim, side) { return (side === 1) === stim.mirror; },
      render: function () {  // keep each trial's stimulus with its row, so the fit can tell same from mirror trials
        var L = run ? run.log : [];
        if (L.length && !L[L.length - 1].stim) L[L.length - 1].stim = run.stim;
        if (w) w.render();
      },
      foreperiod: [600, 1200], timeout: 7000, pause: { scored: 600, early: 800, timeout: 800 },
      words: { early: "Too early: wait for the shapes.", timeout: "No answer in seven seconds.",
        wrong: function () { return "Wrong (not counted)."; } },
    });

    function drawShape(ctx, cx, cy, size, angle, mirror, color) {
      var mx = 0, my = 0, i;
      for (i = 0; i < CELLS.length; i++) { mx += CELLS[i][0] + 0.5; my += CELLS[i][1] + 0.5; }
      mx /= CELLS.length; my /= CELLS.length;
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(angle * Math.PI / 180);
      if (mirror) ctx.scale(-1, 1);
      ctx.fillStyle = color; ctx.strokeStyle = "#e8edf3"; ctx.lineWidth = 1.5;
      for (i = 0; i < CELLS.length; i++) {
        var x = (CELLS[i][0] - mx) * size, y = (CELLS[i][1] - my) * size;
        ctx.fillRect(x, y, size, size); ctx.strokeRect(x, y, size, size);
      }
      ctx.restore();
    }

    function fit() {  // least squares of time on angle, over the correct "same" trials
      var xs = [], ys = [], i, r;
      for (i = 0; i < run.log.length; i++) {
        r = run.log[i];
        if (r.correct && r.stim && !r.stim.mirror) { xs.push(r.stim.angle); ys.push(r.rt); }
      }
      if (xs.length < 3) return null;
      var mx = QB.mean(xs), my = QB.mean(ys), sxy = 0, sxx = 0;
      for (i = 0; i < xs.length; i++) { sxy += (xs[i] - mx) * (ys[i] - my); sxx += (xs[i] - mx) * (xs[i] - mx); }
      if (sxx === 0) return null;
      var b = sxy / sxx;
      return { slope: b, icpt: my - b * mx, xs: xs, ys: ys };
    }

    w = QB.widget(el, {
      title: "Mental rotation, on you",
      sub: "Two shapes: is the right one the left one turned, or its mirror image? F (or tap left) for the same shape, J (or tap right) for a mirror image. Answer as fast as you can while staying right. Then see how your time grows with the angle, and how fast you turn.",
      panels: 2, height: 320, weights: [1.1, 1],
      controls: [{ k: "n", label: "Trials", min: 12, max: 48, step: 4, value: 24, fmt: function (x) { return x.toFixed(0); } }],
      buttons: [
        { label: "Start", act: function () { run.reset(); run.start("rotation"); } },
        { label: "Clear", act: function () { run.reset(); } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, run.task), size = Math.min(b.w, b.h) * 0.085;
        if (run.phase === "go") {
          drawShape(ctx, b.x + b.w * 0.3, b.cy, size, run.stim.spin, false, SHAPE);
          drawShape(ctx, b.x + b.w * 0.7, b.cy, size, run.stim.spin + run.stim.angle, run.stim.mirror, SHAPE);
          ctx.save(); ctx.textAlign = "center"; ctx.font = "12px system-ui, sans-serif";
          ctx.fillStyle = SAME; ctx.fillText("same: F", b.x + b.w * 0.25, b.y + b.h - 20);
          ctx.fillStyle = MIRROR; ctx.fillText("mirror: J", b.x + b.w * 0.75, b.y + b.h - 20);
          ctx.fillStyle = C.muted; ctx.fillText("trial " + run.trial + " of " + v.n, b.cx, b.y + 22);
          ctx.restore();
        } else if (run.phase === "wait") {
          ctx.save(); ctx.strokeStyle = C.muted; ctx.lineWidth = 3; ctx.beginPath();
          ctx.moveTo(b.cx - 12, b.cy); ctx.lineTo(b.cx + 12, b.cy); ctx.moveTo(b.cx, b.cy - 12); ctx.lineTo(b.cx, b.cy + 12);
          ctx.stroke(); ctx.restore();
        } else if (run.phase === "feedback") {
          T.message(ctx, b, run.msg);
        } else if (run.phase === "done") {
          T.message(ctx, b, "Finished.", "On the right: your time to say 'same' at each angle, the line through it, and the 54 people of Ganis and Kievit (2015).");
        } else {
          T.message(ctx, b, "On you", "Press Start. Each trial shows two shapes, the right one turned by 0, 60, 120 or 180 degrees, and mirrored half the time.");
        }
        var f = fit(), top = 4000, i;
        if (f) for (i = 0; i < f.ys.length; i++) top = Math.max(top, f.ys[i] + 300);
        top = Math.min(9000, Math.ceil(top / 1000) * 1000);
        var a = g[1].axes({ x: [-10, 190], y: [0, top], xticks: [0, 60, 120, 180], yticks: [0, top / 2, top],
          title: "Time to say 'same', by angle", xlabel: "angle (degrees)", ylabel: "ms" });
        a.line(GK.x, GK.y, { color: REF, width: 2, dash: [5, 4] });
        a.dots(GK.x, GK.y, { color: REF, r: 3 });
        a.text(150, GK.y[3] + 0.06 * top, "54 people (2015)", { color: REF, align: "center", size: 11 });
        if (f) {
          a.dots(f.xs, f.ys, { color: SHAPE, r: 3, alpha: 0.75 });
          a.line([0, 180], [f.icpt, f.icpt + 180 * f.slope], { color: SAME, width: 2.5 });
        }
      },
      readout: function () {
        var f = fit(), n = run.log.length, right = 0, i;
        for (i = 0; i < n; i++) if (run.log[i].correct) right++;
        var rate = f && f.slope > 0 ? Math.round(1000 / f.slope) + " degrees a second" : "–";
        return [["answers", String(task().count)], ["right", n ? Math.round(100 * right / n) + "%" : "–"],
          ["your slope", f ? f.slope.toFixed(1) + " ms per degree" : "–"], ["your rotation speed", rate],
          ["54 people, median", "about 93 degrees a second"]];
      },
      note: "Nothing you do is stored or sent. Shepard and Metzler (1971) found the time to say 'same' grows in a straight line with the angle, as if a picture were turned at a steady speed; Ganis and Kievit's open data, fitted in the film, put the median person at about 93 degrees a second for 3-D figures. Flat shapes like these are usually turned faster. A browser adds its own delay to every time, which moves your whole line up but leaves its slope alone.",
    });
    function task() { return run.task; }
  };

  // ---- Part 25: moving dots, careful and then fast.  Your accuracy, your times, and your two bounds by EZ --------
  W.dots = function (el) {
    var w = null, raf = 0, CAREFUL = "#4dd0e1", FAST = "#ff9f43", REF = "#9aa4b2", DOT = "#e8edf3";
    var COH = [0.1, 0.2, 0.4], N = 70, SPEED = 0.35;   // dots, and their step in aperture radii per second
    // Wagenmakers et al. (2008), 17 people: median accuracy and mean time in each kind of block (the film's data)
    var REF17 = { careful: [0.77, 0.95], fast: [0.54, 0.85] };
    var dots = [], last = 0;
    var run = T.timed(el, {
      keys: { f: 0, j: 1 },
      trials: function () { return w.v.n; },
      seed: function () { return w.state.seed; },
      stimulus: function (rand) { return { dir: rand() < 0.5 ? 0 : 1, coh: COH[Math.floor(rand() * 3)] }; },
      correct: function (stim, side) { return side === stim.dir; },
      render: function () {
        if (w) w.render();
        if (run && run.phase === "go") { seedDots(); if (!raf) raf = requestAnimationFrame(tick); }
      },
      foreperiod: [500, 1000], timeout: 3000, pause: { scored: 500, early: 800, timeout: 800 },
      words: { early: "Too early: wait for the dots.", timeout: "No answer in three seconds.",
        wrong: function () { return "Wrong."; } },
    });
    function seedDots() {
      if (dots.length) return;
      var r = QB.rng(run.trial * 7919 + 13), i;
      for (i = 0; i < N; i++) {
        var a = 2 * Math.PI * r(), d = Math.sqrt(r());
        dots.push({ x: d * Math.cos(a), y: d * Math.sin(a) });
      }
      last = T.now();
    }
    function step(dt) {
      var i, st = run.stim, dir = st.dir === 1 ? 1 : -1;
      for (i = 0; i < dots.length; i++) {
        var p = dots[i], ang = Math.random() < st.coh ? (dir > 0 ? 0 : Math.PI) : 2 * Math.PI * Math.random();
        p.x += SPEED * dt * Math.cos(ang); p.y += SPEED * dt * Math.sin(ang);
        if (p.x * p.x + p.y * p.y > 1) { var a = 2 * Math.PI * Math.random(), d = Math.sqrt(Math.random()); p.x = d * Math.cos(a); p.y = d * Math.sin(a); }
      }
    }
    function tick() {
      raf = 0;
      if (!w || run.phase !== "go") { dots = []; return; }
      var t = T.now(); step(Math.min(0.05, (t - last) / 1000)); last = t;
      w.render();
      raf = requestAnimationFrame(tick);
    }

    // EZ diffusion (Wagenmakers, van der Maas and Grasman 2007), noise scale 1, times in seconds
    function ez(pc, vrt, mrt, n) {
      pc = Math.min(Math.max(pc, 0.5 + 0.5 / n), 1 - 0.5 / n);
      if (!(vrt > 0)) return null;
      var L = Math.log(pc / (1 - pc));
      var x = L * (L * pc * pc - L * pc + pc - 0.5) / vrt;
      if (!(x > 0)) return null;
      var v = Math.pow(x, 0.25), a = L / v, y = -v * a;
      var mdt = (a / (2 * v)) * (1 - Math.exp(y)) / (1 + Math.exp(y));
      return { v: v, a: a, t0: mrt - mdt };
    }
    function block(cond) {
      var L = run.log.filter(function (r) { return r.condition === cond && !isNaN(r.rt); }), i, c = [];
      if (L.length < 4) return null;
      var right = 0;
      for (i = 0; i < L.length; i++) if (L[i].correct) { right++; c.push(L[i].rt / 1000); }
      var all = L.map(function (r) { return r.rt / 1000; });
      var out = { n: L.length, pc: right / L.length, mrt: QB.mean(all), fit: null };
      if (c.length >= 3) {
        var m = QB.mean(c), v = 0;
        for (i = 0; i < c.length; i++) v += (c[i] - m) * (c[i] - m);
        out.fit = ez(out.pc, v / (c.length - 1), m, L.length);
      }
      return out;
    }

    w = QB.widget(el, {
      title: "Moving dots, careful and then fast",
      sub: "Most dots move at random; some drift left or right. F (or tap left) for left, J (or tap right) for right. Run a careful block first: be sure before you answer. Then a fast block: answer the moment you have a guess. Your two blocks become two points, and two bounds.",
      panels: 2, height: 320, weights: [1.1, 1],
      controls: [{ k: "n", label: "Trials per block", min: 12, max: 48, step: 4, value: 20, fmt: function (x) { return x.toFixed(0); } }],
      buttons: [
        { label: "Careful block", act: function () { dots = []; run.start("careful"); } },
        { label: "Fast block", act: function () { dots = []; run.start("fast"); } },
        { label: "Clear", act: function () { dots = []; run.reset(); } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, run.task), R = Math.min(b.w, b.h) * 0.33, i;
        var col = run.cond === "fast" ? FAST : CAREFUL;
        if (run.phase === "go") {
          ctx.save();
          ctx.strokeStyle = "#2a3140"; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(b.cx, b.cy, R + 6, 0, 2 * Math.PI); ctx.stroke();
          ctx.fillStyle = DOT;
          for (i = 0; i < dots.length; i++) { ctx.beginPath(); ctx.arc(b.cx + dots[i].x * R, b.cy + dots[i].y * R, 2.2, 0, 2 * Math.PI); ctx.fill(); }
          ctx.textAlign = "center"; ctx.font = "12px system-ui, sans-serif"; ctx.fillStyle = col;
          ctx.fillText((run.cond === "fast" ? "FAST: " : "CAREFUL: ") + "trial " + run.trial + " of " + v.n, b.cx, b.y + 22);
          ctx.fillStyle = C.muted; ctx.fillText("left: F        right: J", b.cx, b.y + b.h - 18);
          ctx.restore();
        } else if (run.phase === "wait") {
          ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = 3; ctx.beginPath();
          ctx.moveTo(b.cx - 10, b.cy); ctx.lineTo(b.cx + 10, b.cy); ctx.moveTo(b.cx, b.cy - 10); ctx.lineTo(b.cx, b.cy + 10);
          ctx.stroke(); ctx.restore();
        } else if (run.phase === "feedback") {
          T.message(ctx, b, run.msg);
        } else if (run.phase === "done") {
          T.message(ctx, b, run.cond === "fast" ? "Fast block finished." : "Careful block finished.",
            run.cond === "fast" ? "On the right: your two blocks beside the 17 people of the film." : "Now press Fast block: answer the moment you have a guess.");
        } else {
          T.message(ctx, b, "On you", "Press Careful block. Each trial: a cross, then a cloud of dots for up to three seconds. Which way are some of them drifting?");
        }
        var a = g[1].axes({ x: [0.2, 1.6], y: [0.5, 1.0], xticks: [0.4, 0.8, 1.2, 1.6], yticks: [0.5, 0.75, 1.0],
          title: "Accuracy against time", xlabel: "mean time (s)", ylabel: "proportion right" });
        a.line([REF17.fast[0], REF17.careful[0]], [REF17.fast[1], REF17.careful[1]], { color: REF, width: 2, dash: [5, 4] });
        a.dots([REF17.fast[0]], [REF17.fast[1]], { color: FAST, r: 3, alpha: 0.6 });
        a.dots([REF17.careful[0]], [REF17.careful[1]], { color: CAREFUL, r: 3, alpha: 0.6 });
        a.text(REF17.careful[0], REF17.careful[1] - 0.05, "17 people (2008)", { color: REF, align: "center", size: 11 });
        var bf = block("fast"), bc = block("careful");
        if (bf && bc) a.line([Math.min(1.6, bf.mrt), Math.min(1.6, bc.mrt)], [bf.pc, bc.pc], { color: C.ink, width: 2 });
        if (bf) a.dots([Math.min(1.6, bf.mrt)], [Math.max(0.5, bf.pc)], { color: FAST, r: 6 });
        if (bc) a.dots([Math.min(1.6, bc.mrt)], [Math.max(0.5, bc.pc)], { color: CAREFUL, r: 6 });
      },
      readout: function () {
        var bc = block("careful"), bf = block("fast");
        function show(bl) { return bl ? Math.round(100 * bl.pc) + "% in " + bl.mrt.toFixed(2) + " s" : "–"; }
        function bound(bl) { return bl && bl.fit ? bl.fit.a.toFixed(2) : "–"; }
        var ratio = bc && bf && bc.fit && bf.fit ? (bf.fit.a / bc.fit.a).toFixed(2) : "–";
        return [["answers", String(run.task.count)], ["careful", show(bc)], ["fast", show(bf)],
          ["your bounds (EZ), careful / fast", bound(bc) + " / " + bound(bf)], ["fast over careful", ratio],
          ["17 people (EZ), median", "0.59"]];
      },
      note: "Nothing you do is stored or sent. EZ diffusion (Wagenmakers, van der Maas and Grasman, 2007) turns a block's accuracy, and the mean and variance of its correct times, into a drift, a bound and a non-decision time. Asked to hurry, the 17 people of the film lowered their EZ bound to a median 59% of their careful one. With twenty trials a block your numbers are rough, and a browser adds its own delay to every time; the ratio of your two bounds is the steadiest thing here.",
    });
  };
  // ---- Part 26: the disease problem, then a ladder of sure amounts against gambles: your own fourfold pattern ----
  W.gambles = function (el) {
    var w = null, GAIN = "#5bd18b", LOSS = "#ef6f6c", SURE = "#7ec8f5", RISKY = "#f2c14e", REF = "#9aa4b2";
    // Tversky and Kahneman (1981): share choosing the sure programme; (1992): alpha 0.88, gamma 0.61, delta 0.69
    var TK81 = { saved: 72, die: 22 }, ALPHA = 0.88, GAM = 0.61, DEL = 0.69;
    var CELLS = [{ p: 0.05, s: 1, name: "+100 at 5%" }, { p: 0.95, s: 1, name: "+100 at 95%" },
      { p: 0.05, s: -1, name: "-100 at 5%" }, { p: 0.95, s: -1, name: "-100 at 95%" }];
    var STEPS = 4;
    var st = { phase: "idle", items: [], k: 0, frame: "", frameChoice: -1, cells: [], delay: [] };
    function wtk(p, g) { var a = Math.pow(p, g); return a / Math.pow(a + Math.pow(1 - p, g), 1 / g); }
    function modelCE(p, s) { return s * 100 * Math.pow(wtk(p, s > 0 ? GAM : DEL), 1 / ALPHA); }
    function start(seed) {
      var r = QB.rng(seed * 7919 + 26), i, j;
      st.frame = r() < 0.5 ? "saved" : "die"; st.frameChoice = -1;
      st.cells = CELLS.map(function (c) { return { p: c.p, s: c.s, name: c.name, lo: 0, hi: 100, done: 0 }; });
      st.delay = [-1, -1];
      st.items = [{ kind: "frame" }];
      for (j = 0; j < STEPS; j++) for (i = 0; i < CELLS.length; i++) st.items.push({ kind: "cell", c: i });
      st.items.push({ kind: "delay", d: 0 }, { kind: "delay", d: 1 });
      st.k = 0; st.phase = "go";
    }
    function item() { return st.items[st.k]; }
    function offer(it) {   // [left: the sure option, right: the gamble], as lines of text
      if (it.kind === "frame") {
        return st.frame === "saved"
          ? [["Programme A", "200 people will be saved."], ["Programme B", "1/3 chance all 600 saved,", "2/3 chance no one saved."]]
          : [["Programme C", "400 people will die."], ["Programme D", "1/3 chance nobody dies,", "2/3 chance all 600 die."]];
      }
      if (it.kind === "delay") {
        return it.d === 0 ? [["$100 today"], ["$110 in 4 weeks"]] : [["$100 in 26 weeks"], ["$110 in 30 weeks"]];
      }
      var c = st.cells[it.c], s = (c.lo + c.hi) / 2, sign = c.s > 0 ? "+" : "-";
      return [["Sure: " + sign + "$" + s.toFixed(1)], ["Gamble: " + sign + "$100", "with chance " + Math.round(100 * c.p) + "%", "else $0"]];
    }
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return st.phase === "go"; },
      respond: function (side) {
        var it = item();
        if (it.kind === "frame") st.frameChoice = side;
        else if (it.kind === "delay") st.delay[it.d] = side;
        else {
          var c = st.cells[it.c], s = (c.lo + c.hi) / 2;
          // gains: choosing the sure s means s is above your certainty equivalent; losses (in sizes): choosing the
          // sure loss s means s is below the size of your certainty equivalent
          if (c.s > 0) { if (side === 0) c.hi = s; else c.lo = s; } else { if (side === 0) c.lo = s; else c.hi = s; }
          c.done++;
        }
        task.count++;
        st.k++;
        st.phase = "pause";
        if (w) w.render();
        task.later(function () { st.phase = st.k >= st.items.length ? "done" : "go"; if (w) w.render(); }, 350);
      },
    });
    function ce(c) { return c.done ? c.s * (c.lo + c.hi) / 2 : null; }
    function card(ctx, x, y, wd, ht, lines, col) {
      ctx.save();
      ctx.fillStyle = "#0b0f16"; ctx.fillRect(x, y, wd, ht);
      ctx.strokeStyle = col; ctx.lineWidth = 2; ctx.strokeRect(x, y, wd, ht);
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      var i, y0 = y + ht / 2 - (lines.length - 1) * 10;
      for (i = 0; i < lines.length; i++) {
        ctx.fillStyle = i === 0 ? col : C.ink; ctx.font = (i === 0 ? "600 14px" : "13px") + " system-ui, sans-serif";
        ctx.fillText(lines[i], x + wd / 2, y0 + 20 * i);
      }
      ctx.restore();
    }
    w = QB.widget(el, {
      title: "Six hundred lives, and your own fourfold pattern",
      sub: "Nineteen choices, each between two cards. F (or tap left) for the left card, J (or tap right) for the right. First the disease problem, in one of its two frames; then sure amounts against gambles, narrowing in on the sure amount you find just as good; then two choices over time.",
      panels: 2, height: 330, weights: [1.1, 1],
      controls: [],
      buttons: [
        { label: "Start", act: function (state) { start(state.seed); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); st.phase = "idle"; st.cells = []; st.frameChoice = -1; st.delay = [-1, -1]; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (st.phase === "go") {
          var it = item(), o = offer(it), cw = (b.w - 60) / 2, ch = Math.min(130, b.h - 120);
          ctx.save(); ctx.textAlign = "center"; ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          var head = it.kind === "frame" ? "A disease is expected to kill 600 people. Which do you favour?"
            : it.kind === "delay" ? "Which would you rather have?" : "Which would you rather have?";
          T.wrap(ctx, head, b.cx, b.y + 30, b.w - 40, 16);
          ctx.fillText("choice " + (st.k + 1) + " of " + st.items.length, b.cx, b.y + b.h - 18);
          ctx.restore();
          card(ctx, b.x + 20, b.cy - ch / 2 + 6, cw, ch, o[0], SURE);
          card(ctx, b.x + 40 + cw, b.cy - ch / 2 + 6, cw, ch, o[1], RISKY);
        } else if (st.phase === "pause") {
          T.message(ctx, b, "...");
        } else if (st.phase === "done") {
          T.message(ctx, b, "Done.", "On the right: your certainty equivalents beside prospect theory's. Below: your choices and the published ones.");
        } else {
          T.message(ctx, b, "On you", "Press Start. There are no right answers, only yours.");
        }
        var a = g[1].axes({ x: [0, 1], y: [0, 100], xticks: [0, 0.5, 1], yticks: [0, 50, 100],
          title: "Sure amount as good as the gamble", xlabel: "chance of the 100", ylabel: "size of sure amount" });
        a.line([0, 1], [0, 100], { color: REF, width: 1, dash: [5, 4] });
        var ps = QB.linspace(0.01, 0.99, 50);
        a.line(ps, ps.map(function (p) { return modelCE(p, 1); }), { color: GAIN, width: 2 });
        a.line(ps, ps.map(function (p) { return -modelCE(p, -1); }), { color: LOSS, width: 2, dash: [6, 4] });
        st.cells.forEach(function (c) {
          var v = ce(c);
          if (v !== null) a.dots([c.p], [Math.abs(v)], { color: c.s > 0 ? GAIN : LOSS, r: 6 });
        });
        a.text(0.3, 92, "above the dashed line: seeks risk for gains, avoids it for losses", { color: C.muted, align: "center", size: 10 });
        a.legend([["theory, gains", GAIN], ["theory, losses", LOSS], ["dots: yours", C.ink]], { pos: "br" });
      },
      readout: function () {
        var out = [["choices", String(task.count)]];
        if (st.frameChoice >= 0) {
          var sure = st.frameChoice === 0;
          out.push(["disease problem (" + (st.frame === "saved" ? "lives saved" : "deaths") + ")", sure ? "sure programme" : "gamble"]);
          out.push(["1981: chose the sure programme", st.frame === "saved" ? TK81.saved + "% of 152" : TK81.die + "% of 155"]);
        }
        st.cells.forEach(function (c) {
          var v = ce(c);
          if (v !== null) out.push([c.name + ": yours / theory", v.toFixed(0) + " / " + modelCE(c.p, c.s).toFixed(0)]);
        });
        if (st.delay[0] >= 0 && st.delay[1] >= 0) {
          var rev = st.delay[0] === 0 && st.delay[1] === 1;
          out.push(["over time", rev ? "now you take $100, later you would wait: a reversal" : (st.delay[0] === st.delay[1] ? "consistent" : "the other way round")]);
        }
        return out;
      },
      note: "Nothing you choose is stored or sent. The ladder halves the range four times for each gamble, so your sure amounts are good to within about 3 dollars. Prospect theory's curves use Tversky and Kahneman's 1992 values: for gains (green), a 5% chance of 100 is worth about 10, more than its expected 5; for losses (red, by size), the pattern flips. Seeking risk for unlikely gains and likely losses, avoiding it for likely gains and unlikely losses, is the fourfold pattern.",
    });
  };
})();
