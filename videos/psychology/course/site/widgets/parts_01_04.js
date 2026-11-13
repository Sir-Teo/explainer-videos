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
})();
