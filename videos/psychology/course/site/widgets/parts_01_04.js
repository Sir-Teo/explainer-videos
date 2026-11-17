// Interactives for Act I, Asking a Mind a Question (Parts 1-4).  In this series each interactive is an experiment
// the reader takes part in.  Nothing a reader does is stored or sent anywhere: the data live in the page's memory
// and are gone when the page is closed.  The keys, taps, timing and trial loop are the task kit's (00_tasks.js).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt, T = QB.task;
  var SIMPLE = "#9fd8f0", CHOICE = "#f28fb8", GO = "#3ddc84", LEFT = "#5dadec";

  // ---- Part 1: your own reaction time, simple and choice -------------------------------------------------------
  W.reactiontime = function (el) {
    var w = null, mean = {};
    var run = T.timed(el, {
      keys: { " ": -1, f: 0, j: 1 }, // the space bar answers either way; F is left and J is right
      trials: function () { return w.v.n; },
      seed: function () { return w.state.seed; },
      stimulus: function (rand, cond) { return cond === "choice" ? (rand() < 0.5 ? 0 : 1) : 1; }, // 0: blue square, left; 1: green circle, right
      correct: function (stim, side, cond) { return cond === "simple" || side === stim; },
      render: function () { if (w) w.render(); },
      words: { early: "Too early: wait for the shape.", timeout: "No response in two seconds.",
        wrong: function (side) { return side < 0 ? "Use F or J, or tap a side." : "Wrong side (not counted)."; } },
    });

    w = QB.widget(el, {
      title: "Your reaction time: simple, then choice",
      sub: "Simple: press the space bar, or tap the dark panel, the moment the grey circle turns green. Choice: a blue square means left (the F key, or tap the left half), a green circle means right (J, or the right half). Then compare your two averages, and move the delay slider to see what a slower device would have recorded.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Trials in a block", min: 5, max: 20, step: 1, value: 8, fmt: function (x) { return x.toFixed(0); } },
        { k: "lag", label: "Pretend your device adds this delay", min: 0, max: 120, step: 5, value: 0, fmt: function (x) { return x.toFixed(0) + " ms"; } },
      ],
      buttons: [
        { label: "Start the simple task", act: function () { run.start("simple"); } },
        { label: "Start the choice task", act: function () { run.start("choice"); } },
        { label: "Clear my data", act: function () { run.reset(); } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, run.task), cx = b.cx, cy = b.cy, r = Math.min(b.w, b.h) * 0.16;
        if (run.phase === "wait" || run.phase === "go") {
          ctx.save();
          ctx.textAlign = "center"; ctx.textBaseline = "middle";
          ctx.font = "12px system-ui, sans-serif"; ctx.fillStyle = C.muted;
          ctx.fillText("trial " + run.trial + " of " + v.n, cx, b.y + 24);
          if (run.cond === "choice" && run.phase === "wait") { // a fixation cross
            ctx.strokeStyle = C.muted; ctx.lineWidth = 3; ctx.beginPath();
            ctx.moveTo(cx - 12, cy); ctx.lineTo(cx + 12, cy); ctx.moveTo(cx, cy - 12); ctx.lineTo(cx, cy + 12); ctx.stroke();
          } else if (run.phase === "go" && run.stim === 0) {
            ctx.fillStyle = LEFT; ctx.fillRect(cx - r, cy - r, 2 * r, 2 * r);
          } else {
            ctx.fillStyle = run.phase === "go" ? GO : "#3a4150"; ctx.beginPath(); ctx.arc(cx, cy, r, 0, 2 * Math.PI); ctx.fill();
          }
          if (run.cond === "choice") {
            ctx.font = "12px system-ui, sans-serif";
            ctx.fillStyle = LEFT; ctx.fillText("square: left (F)", b.x + b.w * 0.25, b.y + b.h - 22);
            ctx.fillStyle = GO; ctx.fillText("circle: right (J)", b.x + b.w * 0.75, b.y + b.h - 22);
          }
          ctx.restore();
        } else if (run.phase === "feedback") {
          T.message(ctx, b, run.msg);
        } else if (run.phase === "done") {
          T.message(ctx, b, "Block finished.", run.cond === "simple" ? "Now start the choice task." : "Compare the two rows on the other panel.");
        } else {
          T.message(ctx, b, "On you", "Press a Start button. Respond with the space bar, F and J, or by tapping this panel.");
        }

        var rows = [["simple", SIMPLE, 2], ["choice", CHOICE, 1]], data = [run.rts("simple"), run.rts("choice")], top = 500, i, k;
        for (k = 0; k < 2; k++) for (i = 0; i < data[k].length; i++) top = Math.max(top, data[k][i] + v.lag + 60);
        top = Math.min(2200, Math.ceil(top / 100) * 100);
        var a = g[1].axes({ x: [100, top], y: [0, 3], title: "Each response, and the average of each task", xlabel: "reaction time as recorded (ms)", noY: true });
        a.vline(213, { color: C.muted });
        a.text(213, 2.82, "1,469 adults, calibrated lab: 213", { color: C.muted, dx: 5, size: 11 });
        mean = {};
        for (k = 0; k < 2; k++) {
          var xs = data[k], shown = [], ys = [], jr = QB.rng(11 + k);
          for (i = 0; i < xs.length; i++) { shown.push(xs[i] + v.lag); ys.push(rows[k][2] + 0.3 * (jr() - 0.5)); }
          a.text(a.xr[0], rows[k][2] + 0.42, rows[k][0], { color: rows[k][1], dx: 6, bold: true });
          if (xs.length) {
            var m = QB.mean(shown); mean[rows[k][0]] = m;
            a.dots(shown, ys, { color: rows[k][1], r: 3.2, alpha: 0.85 });
            a.line([m, m], [rows[k][2] - 0.36, rows[k][2] + 0.36], { color: rows[k][1], width: 2.5 });
          }
        }
        if (mean.simple !== undefined && mean.choice !== undefined) {
          a.line([mean.simple, mean.choice], [0.38, 0.38], { color: C.idea, width: 2.5 });
          a.text((mean.simple + mean.choice) / 2, 0.16, "choice − simple", { color: C.idea, align: "center" });
        }
      },
      readout: function () {
        var ms = function (x) { return x === undefined ? "–" : fmt(x, 0) + " ms"; };
        var d = mean.simple !== undefined && mean.choice !== undefined ? mean.choice - mean.simple : undefined;
        return [["simple, average", ms(mean.simple)], ["choice, average", ms(mean.choice)], ["choice − simple", ms(d)],
          ["responses", String(run.rts("simple").length + run.rts("choice").length)], ["too early", String(run.early)]];
      },
      note: "Your data stay in this page and are gone when you close it. A browser adds a delay of its own to every time, different on every device, so the absolute times here cannot be compared with a laboratory's or with another person's. The difference between your two tasks can: a constant delay moves both averages and leaves the difference alone, which the slider shows. Reference line: Woods et al. (2015), simple visual reactions measured with calibrated hardware.",
    });
  };

  // ---- Part 2: try to be random, against a program that guesses your next press --------------------------------
  W.berandom = function (el) {
    var w = null;
    var S = { phase: "idle", who: "you", seq: [], runCache: {} };
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "run"; }, respond: press });
    var YOU = "#f2f2f2", COIN = "#4fd1c5", GUESS = "#ff9f5a";

    // The predictor of the film: for each press, find the longest recent context (up to `depth` presses) after
    // which one key has led the other by at least two, and bet on that key; with nothing to go on, bet on a switch.
    // Returns one guess per press, plus the guess for the press that has not been made yet.
    function predict(seq, depth) {
      var counts = {}, guesses = [], i, k, key, c, g;
      for (i = 0; i <= seq.length; i++) {
        g = -1;
        for (k = Math.min(depth, i); k >= 1 && g < 0; k--) {
          c = counts[seq.slice(i - k, i).join("")];
          if (c && Math.abs(c[0] - c[1]) >= 2) g = c[1] > c[0] ? 1 : 0;
        }
        if (g < 0) g = i ? 1 - seq[i - 1] : 0;
        guesses.push(g);
        if (i === seq.length) break;
        for (k = 1; k <= Math.min(depth, i); k++) {
          key = seq.slice(i - k, i).join("");
          if (!counts[key]) counts[key] = [0, 0];
          counts[key][seq[i]]++;
        }
      }
      return guesses;
    }
    function longestRun(seq) {
      var best = seq.length ? 1 : 0, run = 1, i;
      for (i = 1; i < seq.length; i++) { run = seq[i] === seq[i - 1] ? run + 1 : 1; if (run > best) best = run; }
      return best;
    }
    function switches(seq) {
      var s = 0, i;
      for (i = 1; i < seq.length; i++) if (seq[i] !== seq[i - 1]) s++;
      return seq.length > 1 ? s / (seq.length - 1) : NaN;
    }
    function coinSeq(n, seed) { var r = QB.rng(seed), o = [], i; for (i = 0; i < n; i++) o.push(r() < 0.5 ? 0 : 1); return o; }
    function coinRun(n) { // the mean longest run of a fair coin in n tosses, by simulation (cached)
      if (!S.runCache[n]) {
        var tot = 0, k;
        for (k = 0; k < 400; k++) tot += longestRun(coinSeq(n, 7000 + 31 * k + n));
        S.runCache[n] = tot / 400;
      }
      return S.runCache[n];
    }
    function press(side) {
      if (S.phase !== "run" || !w) return;
      S.seq.push(side); task.count++;
      if (S.seq.length >= w.v.n) S.phase = "done";
      w.render();
    }

    w = QB.widget(el, {
      title: "Be random, if you can",
      sub: "Press F and J (or tap the left and right halves of the dark panel) in as random an order as you can. Before every press, a small program has already guessed it from what you did earlier. A fair coin beats it half the time. Do you?",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Presses in a run", min: 30, max: 150, step: 10, value: 60, fmt: function (x) { return x.toFixed(0); } },
        { k: "depth", label: "How many presses back the program looks", min: 1, max: 5, step: 1, value: 3, fmt: function (x) { return x.toFixed(0); } },
      ],
      buttons: [
        { label: "Start", act: function () { S.seq = []; S.who = "you"; S.phase = "run"; } },
        { label: "Let a coin play instead", act: function (state, v) { S.who = "coin"; S.seq = coinSeq(v.n, 100 + (state.seed || 1) * 13 + (S.coins = (S.coins || 0) + 1)); S.phase = "done"; } },
        { label: "Clear", act: function () { S.seq = []; S.phase = "idle"; S.who = "you"; } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, task), cx = b.cx, cy = b.cy, i;
        var seq = S.seq, n = seq.length, guesses = predict(seq, v.depth), hits = 0, col = S.who === "coin" ? COIN : YOU;
        var run = [], k;
        for (i = 0; i < n; i++) { if (guesses[i] === seq[i]) hits++; run.push(hits / (i + 1)); }
        S.hits = hits;
        ctx.save();
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        if (S.phase === "run") { // a faint divider, and the two keys
          ctx.strokeStyle = "#1b2230"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(cx, b.y + 40); ctx.lineTo(cx, b.y + b.h - 70); ctx.stroke();
          ctx.font = "600 34px system-ui, sans-serif"; ctx.fillStyle = C.muted;
          ctx.fillText("F", b.x + b.w * 0.25, cy - 28); ctx.fillText("J", b.x + b.w * 0.75, cy - 28);
          ctx.font = "12px system-ui, sans-serif";
          ctx.fillText((v.n - n) + " presses to go", cx, b.y + 24);
          if (n) {
            var ok = guesses[n - 1] === seq[n - 1];
            ctx.fillStyle = ok ? GUESS : C.muted;
            ctx.fillText("it guessed " + (guesses[n - 1] ? "J" : "F") + (ok ? ": right" : ": wrong"), cx, cy + 14);
          } else { ctx.fillText("its first guess is made", cx, cy + 14); }
        } else if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start, then F and J (or tap a side) in as random an order as you can.", cy - 40);
        } else {
          T.message(ctx, b, S.who === "coin" ? "A coin played." : "Run finished.",
            "The program guessed " + hits + " of " + n + " presses. Now compare with a coin, or try again.", cy - 40);
        }
        // the most recent presses, as squares: filled for J, hollow for F
        var show = Math.min(n, Math.floor((b.w - 40) / 11)), x0 = cx - show * 5.5, y0 = b.y + b.h - 44;
        for (i = 0; i < show; i++) {
          k = n - show + i;
          ctx.fillStyle = seq[k] ? col : "#2a3242";
          ctx.fillRect(x0 + i * 11, y0, 9, 9);
          ctx.fillStyle = guesses[k] === seq[k] ? GUESS : "transparent";
          ctx.fillRect(x0 + i * 11, y0 + 12, 9, 3);
        }
        if (show) { ctx.fillStyle = C.muted; ctx.font = "11px system-ui, sans-serif"; ctx.fillText("your presses (bright: J); orange underline: guessed", cx, y0 + 26); }
        ctx.restore();

        var a = g[1].axes({ x: [1, Math.max(v.n, 2)], y: [0, 1], title: "Share of presses the program has guessed so far", xlabel: "press number", ylabel: "guessed" });
        var xs = [], up = [], lo = [];
        for (i = 4; i <= v.n; i++) { xs.push(i); up.push(Math.min(1, 0.5 + 1 / Math.sqrt(i))); lo.push(Math.max(0, 0.5 - 1 / Math.sqrt(i))); }
        a.line(xs, up, { color: C.muted, width: 1, dash: [4, 4] });
        a.line(xs, lo, { color: C.muted, width: 1, dash: [4, 4] });
        a.hline(0.5, { color: C.muted });
        a.text(1, 0.5, "a coin: 50%", { color: C.muted, dx: 8, dy: 12, size: 11 });
        a.text(v.n, Math.min(0.97, 0.5 + 1 / Math.sqrt(v.n) + 0.06), "within chance", { color: C.muted, align: "right", size: 11 });
        if (n > 1) {
          var px = []; for (i = 0; i < n; i++) px.push(i + 1);
          a.line(px, run, { color: col, width: 2.5 });
          a.dots([n], [run[n - 1]], { color: col, r: 4 });
        }
      },
      readout: function (v) {
        var n = S.seq.length, sw = switches(S.seq);
        return [
          [S.who === "coin" ? "the coin, guessed" : "you, guessed", n ? QB.pct(S.hits / n, 0) : "–"],
          ["switched keys", n > 1 ? QB.pct(sw, 0) + " (a coin: 50%)" : "–"],
          ["longest run", n ? longestRun(S.seq) + " (a coin: about " + fmt(coinRun(Math.max(n, 2)), 1) + ")" : "–"],
          ["presses", String(n)],
        ];
      },
      note: "Nothing you press is stored or sent: the sequence lives in this page and is gone when you close it. The program does nothing clever. It remembers what you pressed the last few times the same keys had just come up, and once you have leaned one way it bets on that; with nothing to go on, it bets that you will switch. People asked to be random switch too often and avoid long runs, which is exactly what it feeds on. One run proves little: with 60 presses anything between about 37% and 63% is within a coin's own luck (the dashed band), so try several runs, and then let a coin play. This is why, in an experiment, the order of conditions and the assignment to groups are left to a shuffled deck and never to the experimenter.",
    });
  };

  // ---- Part 3: a reading of your character, and what your rating of it is worth ------------------------------
  W.forer = function (el) {
    var w = null;
    var PAIRS = [["mountains", "the sea"], ["morning", "evening"], ["a plan", "seeing what happens"],
      ["a book", "a party"], ["the city", "the countryside"], ["numbers", "words"]];
    // six of the thirteen statements of Forer (1949)
    var READING = ["You have a great need for other people to like and admire you.",
      "You have a tendency to be critical of yourself.",
      "You have a great deal of unused capacity which you have not turned to your advantage.",
      "Disciplined and self-controlled outside, you tend to be worrisome and insecure inside.",
      "At times you have serious doubts as to whether you have made the right decision or done the right thing.",
      "At times you are extroverted, affable, sociable, while at other times you are introverted, wary, reserved."];
    var FORER = 4.26, YOU = "#f2c14e", CLASS = "#9fd8f0";
    var S = { phase: "idle", answers: [], ratings: [], patterns: [] };
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "test"; }, respond: answer });
    function answer(side) {
      if (S.phase !== "test" || !w) return;
      S.answers.push(side); task.count++;
      if (S.answers.length >= PAIRS.length) S.phase = "reading";
      w.render();
    }
    function pattern() { var o = "", i; for (i = 0; i < S.answers.length; i++) o += S.answers[i] ? "J" : "F"; return o; }

    w = QB.widget(el, {
      title: "A reading of your character",
      sub: "An experiment on how accurate a description of you feels. Answer six quick questions (F for the left word, J for the right, or tap a side), read the short description that follows, and rate how well it fits you. One thing about the experiment is kept back until you have given your rating, and it is explained straight afterwards.",
      panels: 2, height: 340, weights: [1.3, 1],
      controls: [
        { k: "rating", label: "How well does the description fit you?", min: 0, max: 5, step: 1, value: 3, fmt: function (x) { return x.toFixed(0) + (x === 0 ? " (poorly)" : x === 5 ? " (perfectly)" : ""); } },
      ],
      buttons: [
        { label: "Start", act: function () { S.answers = []; S.phase = "test"; } },
        { label: "Give my rating", act: function (state, v) { if (S.phase === "reading") { S.ratings.push(v.rating); S.patterns.push(pattern()); S.phase = "reveal"; } } },
        { label: "Clear", act: function () { S.phase = "idle"; S.answers = []; S.ratings = []; S.patterns = []; } },
      ],
      draw: function (g, v) {
        var ctx = g.ctx, b = T.stage(g, 0, task), i, y;
        ctx.save();
        ctx.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start. Six quick questions come first, then a description of your character to rate.");
        } else if (S.phase === "test") {
          var n = S.answers.length, pair = PAIRS[n];
          ctx.textAlign = "center";
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("question " + (n + 1) + " of " + PAIRS.length + ": which do you prefer?", b.cx, b.y + 26);
          ctx.strokeStyle = "#1b2230"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(b.cx, b.y + 50); ctx.lineTo(b.cx, b.y + b.h - 50); ctx.stroke();
          ctx.fillStyle = C.ink; ctx.font = "600 " + (b.w < 380 ? 17 : 22) + "px system-ui, sans-serif";
          T.wrap(ctx, pair[0], b.x + b.w * 0.25, b.cy - 8, b.w * 0.42, 24);
          T.wrap(ctx, pair[1], b.x + b.w * 0.75, b.cy - 8, b.w * 0.42, 24);
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("F, or tap here", b.x + b.w * 0.25, b.y + b.h - 28);
          ctx.fillText("J, or tap here", b.x + b.w * 0.75, b.y + b.h - 28);
        } else {
          var small = b.w < 420, lh = small ? 14 : 16;
          ctx.textAlign = "left";
          ctx.fillStyle = S.phase === "reveal" ? C.muted : YOU; ctx.font = "600 12.5px system-ui, sans-serif";
          ctx.fillText(S.phase === "reveal" ? "The description you rated" : "Your reading", b.x + 20, b.y + 24);
          ctx.fillStyle = S.phase === "reveal" ? C.muted : C.ink; ctx.font = (small ? 11.5 : 12.5) + "px system-ui, sans-serif";
          y = b.y + 46;
          for (i = 0; i < READING.length; i++) y = T.wrap(ctx, READING[i], b.x + 20, y, b.w - 40, lh) + 3;
          if (S.phase === "reading") {
            ctx.fillStyle = YOU; ctx.font = "600 12.5px system-ui, sans-serif";
            T.wrap(ctx, "Set the slider to your rating, then press Give my rating.", b.x + 20, Math.min(y + 12, b.y + b.h - 22), b.w - 40, lh);
          }
        }
        ctx.restore();

        var a = g[1].axes({ x: [0, 5], y: [0, 3], title: S.phase === "reveal" ? "Everyone gets the same description" : "How well it fits, from 0 to 5", xlabel: "rating (0 poorly, 5 perfectly)", noY: true });
        if (S.phase === "reveal") {
          a.vline(FORER, { color: CLASS });
          a.text(FORER, 2.72, "Forer's 39 students, 1949: 4.26", { color: CLASS, align: "right", dx: -6, size: 11 });
          a.text(0, 1.95, "34 of the 39 gave it 4 or 5.", { color: C.muted, dx: 8, size: 11.5 });
          a.text(0, 1.55, "It did not depend on your six answers:", { color: C.muted, dx: 8, size: 11.5 });
          a.text(0, 1.2, "press Start and answer differently.", { color: C.muted, dx: 8, size: 11.5 });
          var xs = [], ys = [], jr = QB.rng(5);
          for (i = 0; i < S.ratings.length; i++) { xs.push(S.ratings[i]); ys.push(0.45 + 0.3 * (jr() - 0.5)); }
          a.dots(xs, ys, { color: YOU, r: 5, alpha: 0.9 });
          a.text(0, 0.82, "your rating" + (S.ratings.length > 1 ? "s" : ""), { color: YOU, dx: 8, size: 11.5, bold: true });
        } else {
          a.vline(v.rating, { color: YOU });
          a.text(v.rating, 2.72, "the slider: " + v.rating.toFixed(0), { color: YOU, align: v.rating > 2.5 ? "right" : "left", dx: v.rating > 2.5 ? -6 : 6, size: 11 });
          a.text(0, 1.6, S.phase === "reading" ? "Rate the whole description." : "The description appears after the six questions.", { color: C.muted, dx: 8, size: 11.5 });
        }
      },
      readout: function () {
        var n = S.ratings.length;
        return [
          ["your rating", n ? String(S.ratings[n - 1]) + " of 5" : "–"],
          ["Forer's class, 1949", S.phase === "reveal" ? "4.26 of 5" : "after your rating"],
          ["your six answers", S.answers.length ? pattern() : "–"],
          ["descriptions rated", String(n)],
        ];
      },
      note: "Nothing you answer is stored or sent: it lives in this page and is gone when you close it. What was kept back: the six questions do nothing, and every reader is shown the same description, whatever they answer. It is made of six of the thirteen statements that Bertram Forer handed to each of his 39 students in 1949 as the result of a personality test; they rated it 4.26 out of 5 on average. If your rating was high, that is the usual result. The statements are true of nearly everyone, so a description that fits you this well has told you nothing about yourself, and your agreement is no evidence that a test behind it measured anything. A measurement has to tell people apart.",
    });
  };

  // ---- Part 4: one dataset in which nothing is going on, and four defensible choices about how to analyse it ----
  W.forkingpaths = function (el) {
    var w = null;
    var FORKS = [["Which outcome?", "reaction time", "error rate"],
      ["Outliers?", "keep everyone", "drop beyond 2.5 SD"],
      ["Adjust for age?", "no", "yes"],
      ["More people?", "stop at 20 a group", "add 10 a group"]];
    var HIT = "#f2c14e", MISS = "#8fa3bf";
    var S = { phase: "idle", seed: 0, data: null, choice: [0, 0, 0, 0], row: 0, tried: {}, all: null, many: null };

    // Two groups of 30 drawn from one population: age, a mean reaction time, and an error rate that goes with it.
    function makeData(seed) {
      var u = QB.rng(7919 * seed + 13), d = { age: [[], []], rt: [[], []], err: [[], []] }, g, i, k;
      for (g = 0; g < 2; g++) for (i = 0; i < 30; i++) {
        var age = 18 + Math.floor(48 * u()), z = u.normal(), s = 0;
        for (k = 0; k < 24; k++) s += -30 * Math.log(1 - u());
        d.age[g].push(age);
        d.rt[g].push(300 + 0.6 * (age - 40) + 24 * z + s / 12 - 60);
        d.err[g].push(6 + 2 * (0.55 * z + Math.sqrt(1 - 0.55 * 0.55) * u.normal()));
      }
      return d;
    }
    function solve(A, b) {
      var n = b.length, i, j, k, M = A.map(function (r, q) { return r.concat([b[q]]); });
      for (i = 0; i < n; i++) {
        var piv = i;
        for (j = i + 1; j < n; j++) if (Math.abs(M[j][i]) > Math.abs(M[piv][i])) piv = j;
        var t = M[i]; M[i] = M[piv]; M[piv] = t;
        for (j = i + 1; j < n; j++) { var f = M[j][i] / M[i][i]; for (k = i; k <= n; k++) M[j][k] -= f * M[i][k]; }
      }
      var x = new Array(n);
      for (i = n - 1; i >= 0; i--) { var s = M[i][n]; for (j = i + 1; j < n; j++) s -= M[i][j] * x[j]; x[i] = s / M[i][i]; }
      return x;
    }
    // The p-value of the group difference by least squares, for one setting of the four switches.
    function pvalue(d, c) {
      var k = c[3] ? 30 : 20, score = c[0] ? d.err : d.rt, y = [], X = [], g, i, a, r, m = 0, n = 0, s2 = 0;
      var lo = -Infinity, hi = Infinity;
      if (c[1]) {
        for (g = 0; g < 2; g++) for (i = 0; i < k; i++) { m += score[g][i]; n++; }
        m /= n;
        for (g = 0; g < 2; g++) for (i = 0; i < k; i++) s2 += (score[g][i] - m) * (score[g][i] - m);
        var sd = Math.sqrt(s2 / (n - 1)); lo = m - 2.5 * sd; hi = m + 2.5 * sd;
      }
      for (g = 0; g < 2; g++) for (i = 0; i < k; i++) {
        var v = score[g][i];
        if (v <= lo || v >= hi) continue;
        y.push(v); X.push(c[2] ? [1, 1 - g, d.age[g][i]] : [1, 1 - g]);
      }
      var p = X[0].length, A = [], b = [];
      for (a = 0; a < p; a++) { A.push(new Array(p).fill(0)); b.push(0); }
      for (i = 0; i < y.length; i++) for (a = 0; a < p; a++) { b[a] += X[i][a] * y[i]; for (r = 0; r < p; r++) A[a][r] += X[i][a] * X[i][r]; }
      var beta = solve(A, b), e1 = new Array(p).fill(0), rss = 0;
      e1[1] = 1;
      var inv11 = solve(A, e1)[1];
      for (i = 0; i < y.length; i++) { var fit = 0; for (a = 0; a < p; a++) fit += X[i][a] * beta[a]; rss += (y[i] - fit) * (y[i] - fit); }
      var df = y.length - p, t = beta[1] / Math.sqrt(rss / df * inv11);
      var z = Math.sqrt(df * Math.log(1 + t * t / df)) * (8 * df + 1) / (8 * df + 3); // Wallace's normal approximation to t
      return 2 * (1 - QB.cdf(z));
    }
    function sixteen(d) {
      var o = [], i;
      for (i = 0; i < 16; i++) { var c = [(i >> 3) & 1, (i >> 2) & 1, (i >> 1) & 1, i & 1]; o.push({ c: c, p: pvalue(d, c) }); }
      return o;
    }
    function pText(p) { return p < 0.001 ? "< .001" : p.toFixed(3).replace(/^0/, ""); }
    function current() { return S.tried[S.choice.join("")]; }
    function smallest() { var m = 1, k; for (k in S.tried) m = Math.min(m, S.tried[k]); return m; }
    function record() { S.tried[S.choice.join("")] = pvalue(S.data, S.choice); }
    function begin(seed) {
      S.seed = seed; S.data = makeData(seed); S.choice = [0, 0, 0, 0]; S.row = 0; S.tried = {}; S.all = null; S.phase = "test";
      record();
    }
    var task = T.create(el, { keys: { f: 0, j: 1 }, accepting: function () { return S.phase === "test"; }, respond: answer });
    function answer(side) {
      if (S.phase !== "test" || !w) return;
      S.choice[S.row] = side; S.row = (S.row + 1) % FORKS.length; task.count++;
      record(); w.render();
    }

    w = QB.widget(el, {
      title: "Four choices and a study of nothing",
      sub: "A game was tested on two groups, and in this page the game does nothing: both groups are drawn from the same population. The planned analysis is the left-hand option of every row. Go through the rows and choose (F for the left option, J for the right, or tap a side); each choice reruns the analysis. Can you get p below .05 without doing anything you could not defend? The page opens on dataset 3, the first in which the plan fails and another analysis succeeds; move the slider and press Start for the others, most of which give nothing whatever you choose.",
      panels: 2, height: 360, weights: [1.25, 1],
      controls: [
        { k: "seed", label: "Dataset", min: 1, max: 300, step: 1, value: 3, fmt: function (x) { return "number " + x.toFixed(0); } },
      ],
      buttons: [
        { label: "Start", act: function (state, v) { begin(v.seed); } },
        { label: "Show all sixteen", act: function () { if (S.data) { S.all = sixteen(S.data); S.phase = "reveal"; } } },
        { label: "Run 1,000 datasets", act: function () {
          var plan = 0, any = 0, i;
          for (i = 0; i < 1000; i++) {
            var all = sixteen(makeData(1000 + i)), hit = false;
            if (all[0].p < 0.05) plan++;
            all.forEach(function (r) { if (r.p < 0.05) hit = true; });
            if (hit) any++;
          }
          S.many = { plan: plan / 1000, any: any / 1000 };
        } },
        { label: "Clear", act: function () { S.phase = "idle"; S.data = null; S.tried = {}; S.all = null; S.many = null; S.choice = [0, 0, 0, 0]; S.row = 0; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), i, j;
        ctx.save();
        ctx.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(ctx, b, "On you", "Press Start. One study of a game that does nothing, and four choices about how to analyse it.");
        } else {
          var small = b.w < 420, top = b.y + 42, rh = (b.h - 42 - 58) / FORKS.length, cur = current();
          ctx.textAlign = "left"; ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("dataset " + S.seed + ": a game that does nothing", b.x + 18, b.y + 24);
          for (i = 0; i < FORKS.length; i++) {
            var y0 = top + i * rh, active = S.phase === "test" && i === S.row;
            ctx.textAlign = "left"; ctx.fillStyle = active ? C.ink : C.muted;
            ctx.font = (active ? "600 " : "") + "12px system-ui, sans-serif";
            ctx.fillText((active ? "▸ " : "") + FORKS[i][0], b.x + 18, y0 + 8);
            for (j = 0; j < 2; j++) {
              var bw = (b.w - 44) / 2, bx = b.x + 18 + j * (bw + 8), on = S.choice[i] === j;
              ctx.strokeStyle = on ? HIT : "#2a3242"; ctx.lineWidth = on ? 2 : 1;
              ctx.strokeRect(bx, y0 + 19, bw, rh - 27);
              ctx.fillStyle = on ? C.ink : C.muted; ctx.textAlign = "center";
              ctx.font = (small ? 11 : 12.5) + "px system-ui, sans-serif";
              ctx.fillText(FORKS[i][j + 1], bx + bw / 2, y0 + 19 + (rh - 27) / 2);
            }
          }
          ctx.textAlign = "center";
          ctx.fillStyle = cur < 0.05 ? HIT : MISS; ctx.font = "600 15px system-ui, sans-serif";
          ctx.fillText("this analysis: p = " + pText(cur) + (cur < 0.05 ? ", significant" : ""), b.cx, b.y + b.h - 40);
          ctx.fillStyle = C.muted; ctx.font = "11.5px system-ui, sans-serif";
          ctx.fillText(S.phase === "test" ? (small ? "F or tap left.  J or tap right." : "F or tap the left half: left option.  J or the right half: right option.")
            : (small ? "Press Start for another dataset." : "All sixteen are on the other panel. Press Start for another dataset."), b.cx, b.y + b.h - 19);
        }
        ctx.restore();

        var a = g[1].axes({ x: [0, 1], y: [0, 3], title: S.phase === "reveal" ? "All sixteen analyses of this dataset" : "The analyses you have run", xlabel: "p-value", noY: true });
        a.vline(0.05, { color: HIT });
        a.text(0.05, 2.78, ".05", { color: HIT, dx: 5, size: 11 });
        var xs = [], ys = [], hx = [], hy = [], jr = QB.rng(11), hits = 0, list = [], k;
        if (S.phase === "reveal") S.all.forEach(function (r) { list.push(r.p); });
        else for (k in S.tried) list.push(S.tried[k]);
        list.forEach(function (p) {
          var yy = 0.35 + 0.6 * jr();
          if (p < 0.05) { hx.push(p); hy.push(yy); hits++; } else { xs.push(p); ys.push(yy); }
        });
        if (xs.length) a.dots(xs, ys, { color: MISS, r: 5, alpha: 0.9 });
        if (hx.length) a.dots(hx, hy, { color: HIT, r: 6, alpha: 1 });
        if (S.phase === "idle") {
          a.text(0.12, 2.2, "Every analysis you run is a dot here.", { color: C.muted, dx: 4, size: 11.5 });
        } else if (S.phase === "test") {
          a.text(0.12, 2.3, "analyses run: " + list.length + " of 16", { color: C.muted, dx: 4, size: 11.5 });
          a.text(0.12, 1.95, "smallest p so far: " + pText(smallest()), { color: smallest() < 0.05 ? HIT : C.muted, dx: 4, size: 11.5, bold: smallest() < 0.05 });
          a.text(0.12, 1.6, "the plan gave " + pText(S.tried["0000"]), { color: C.muted, dx: 4, size: 11.5 });
        } else {
          a.text(0.12, 2.3, hits + " of the 16 give p below .05", { color: hits ? HIT : C.muted, dx: 4, size: 11.5, bold: true });
          a.text(0.12, 1.95, "the plan gave " + pText(S.tried["0000"]), { color: C.muted, dx: 4, size: 11.5 });
          a.text(0.12, 1.6, "The game does nothing in every dataset.", { color: C.muted, dx: 4, size: 11.5 });
        }
        if (S.many) a.text(0.12, 1.2, "1,000 datasets: the plan " + QB.pct(S.many.plan, 0) + ", any of sixteen " + QB.pct(S.many.any, 0), { color: C.ink, dx: 4, size: 11.5 });
      },
      readout: function () {
        var n = Object.keys(S.tried).length;
        return [
          ["this analysis", S.data ? "p = " + pText(current()) : "–"],
          ["analyses run", S.data ? n + " of 16" : "–"],
          ["smallest p so far", S.data ? pText(smallest()) : "–"],
          ["1,000 datasets: plan, any of 16", S.many ? QB.pct(S.many.plan, 0) + ", " + QB.pct(S.many.any, 0) : "press Run 1,000 datasets"],
        ];
      },
      note: "Nothing you choose is stored or sent: it lives in this page and is gone when you close it. Every dataset here is generated in the page with no effect of the game, so every p-value below .05 is a false alarm. Each right-hand option is one a careful researcher could defend: errors are a fair measure of performance, dropping extreme scores is standard, age does slow reaction times, and twenty a group is small. Run on its own, the planned analysis is wrong about one time in twenty. If the data are allowed to pick among the sixteen, at least one succeeds in close to one dataset in five (press Run 1,000 datasets), and with the stronger choices studied by Simmons, Nelson and Simonsohn (2011) the figure reached 61%. No single choice here is the error. The error is choosing after seeing which way each one points, and the remedy is to write the analysis down before the data arrive.",
    });
  };
})();
