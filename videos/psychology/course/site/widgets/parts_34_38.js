// Interactives for Act IX, Other people (Parts 34-38).  Each is an experiment the reader takes part in, built on
// the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 34: Asch's lines, alone and after five recorded answers.  The five answers are scripted. ----
  W.lines = function (el) {
    var w = null, N = 12, CRIT = [2, 3, 5, 6, 8, 9, 11, 12], NAMES = ["A", "B", "C"];
    var S = { phase: "idle", block: "", k: 0, trial: null, shown: 0, msg: "", seed: 1,
              log: { alone: [], group: [] } };
    var lastX = 0.5;
    // read where a tap landed (thirds of the stage: A, B, C); registered before the task kit's own listener
    el.addEventListener("pointerdown", function (e) {
      var b = task && task.box, c = e.target;
      if (!b || !c || c.tagName !== "CANVAS") return;
      var r = c.getBoundingClientRect();
      lastX = (e.clientX - r.left - b.x) / b.w;
    });
    function makeTrial(k) {
      var rand = QB.rng(S.seed * 7919 + k * 104729 + (S.block === "group" ? 31 : 0));
      var std = 70 + Math.round(70 * rand()), right = Math.floor(3 * rand()), lens = [], i;
      var d1 = 0.22 + 0.2 * rand(), d2 = 0.22 + 0.2 * rand();
      var others = [std * (1 - d1), std * (1 + d2)];
      if (rand() < 0.5) others.reverse();
      for (i = 0; i < 3; i++) lens.push(i === right ? std : others.shift());
      var crit = S.block === "group" && CRIT.indexOf(k) >= 0, wrong = right;
      if (crit) { wrong = (right + 1 + Math.floor(2 * rand())) % 3; }
      return { std: std, lens: lens, right: right, crit: crit, said: wrong };
    }
    function next() {
      if (S.k >= N) { S.phase = "done"; task.clear(); if (w) w.render(); return; }
      S.k++; S.trial = makeTrial(S.k); S.shown = 0; S.msg = "";
      if (S.block === "group") {
        S.phase = "reveal";
        (function step() {
          S.shown++; if (w) w.render();
          if (S.shown < 5) task.later(step, 450); else task.later(function () { S.phase = "go"; if (w) w.render(); }, 450);
        })();
      } else { S.phase = "go"; if (w) w.render(); }
    }
    function answer(i) {
      var t = S.trial;
      S.log[S.block].push({ trial: S.k, crit: t.crit, right: i === t.right, withGroup: t.crit && i === t.said });
      task.count++;
      S.phase = "feedback"; S.msg = "You said " + NAMES[i] + ".";
      if (w) w.render();
      task.later(next, 650);
    }
    var task = T.create(el, {
      keys: { "1": 0, "2": 1, "3": 2, "a": 0, "b": 1, "c": 2 },
      accepting: function () { return S.phase === "go"; },
      respond: function (side, how) { answer(how === "tap" ? Math.max(0, Math.min(2, Math.floor(lastX * 3))) : side); },
    });
    function start(block) { task.clear(); S.block = block; S.log[block] = []; S.k = 0; S.seed++; next(); }
    function tally(block) {
      var L = S.log[block], crit = 0, conf = 0, err = 0, errNon = 0, i;
      for (i = 0; i < L.length; i++) {
        if (!L[i].right) { err++; if (!L[i].crit) errNon++; }
        if (L[i].crit) { crit++; if (L[i].withGroup) conf++; }
      }
      return { n: L.length, err: err, crit: crit, conf: conf, errNon: errNon };
    }
    w = QB.widget(el, {
      title: "Which line matches?",
      sub: "A standard line on the left, three comparison lines on the right. Say which matches it: press 1, 2 or 3 (or A, B, C), or tap the third of the stage under your answer. Run it alone first, then with five earlier answers shown before yours.",
      panels: 2, height: 380, weights: [1.35, 1],
      buttons: [
        { label: "Alone", act: function () { start("alone"); } },
        { label: "With five others", act: function () { start("group"); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = { alone: [], group: [] }; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task), i, t = S.trial;
        if ((S.phase === "go" || S.phase === "reveal" || S.phase === "feedback") && t) {
          var sc = Math.min(1, (b.h - 150) / 160), base = b.y + b.h - 70;
          ctx.save(); ctx.textAlign = "center"; ctx.font = "12px system-ui, sans-serif"; ctx.fillStyle = C.muted;
          ctx.fillText((S.block === "group" ? "With five others" : "Alone") + ": trial " + S.k + " of " + N, b.cx, b.y + 26);
          ctx.lineWidth = 6; ctx.lineCap = "butt"; ctx.strokeStyle = C.ink;
          var xs = b.x + b.w * 0.16;
          ctx.beginPath(); ctx.moveTo(xs, base); ctx.lineTo(xs, base - t.std * sc); ctx.stroke();
          ctx.fillStyle = C.muted; ctx.fillText("standard", xs, base + 18);
          for (i = 0; i < 3; i++) {
            var x = b.x + b.w * (0.44 + 0.2 * i);
            ctx.strokeStyle = "#cfd6de";
            ctx.beginPath(); ctx.moveTo(x, base); ctx.lineTo(x, base - t.lens[i] * sc); ctx.stroke();
            ctx.fillStyle = C.ink; ctx.font = "600 14px system-ui, sans-serif"; ctx.fillText(NAMES[i] + "  (" + (i + 1) + ")", x, base + 20);
          }
          if (S.block === "group") {
            ctx.font = "12px system-ui, sans-serif";
            for (i = 0; i < 5; i++) {
              var px = b.x + 40 + i * 52, py = b.y + 54;
              ctx.fillStyle = "#2a3039"; ctx.beginPath(); ctx.arc(px, py, 15, 0, 2 * Math.PI); ctx.fill();
              if (i < S.shown) { ctx.fillStyle = C.ink; ctx.font = "600 14px system-ui, sans-serif"; ctx.fillText(NAMES[t.said], px, py + 5); }
            }
            ctx.font = "12px system-ui, sans-serif"; ctx.fillStyle = C.muted; ctx.textAlign = "left";
            ctx.fillText(S.shown < 5 ? "earlier answers..." : "your turn", b.x + 40 + 5 * 52 - 18, b.y + 58);
          }
          if (S.phase === "feedback") { ctx.textAlign = "center"; ctx.fillStyle = C.muted; ctx.fillText(S.msg, b.cx, b.y + b.h - 24); }
          ctx.restore();
        } else if (S.phase === "done") {
          var r = tally(S.block);
          T.message(ctx, b, S.block === "group" ? "Done: " + r.conf + " of " + r.crit + " answers went with a wrong majority." : "Done: " + r.err + " errors in " + r.n + " trials.",
                    S.block === "group" ? "On " + r.crit + " of the twelve trials the five recorded answers were unanimous and wrong. The film shows what Asch's participants did with real people in the room." : "Now run it with five others. The lines are just as easy.");
        } else {
          T.message(ctx, b, "On you", "Press Alone for twelve trials with no one else, then With five others. Answer what you see.");
        }
        // the record
        var c2 = g[1].box, cx = g.ctx, a = tally("alone"), gr = tally("group"), y0 = c2.y + c2.h - 40, hmax = c2.h - 110;
        cx.save(); cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("Your errors, alone and with the group", c2.x + 10, c2.y + 18);
        var bars = [["alone", a.n ? a.err / a.n : NaN, "#7ec8f5"], ["with five, wrong majority", gr.crit ? gr.conf / gr.crit : NaN, "#f2c14e"],
                    ["with five, right majority", gr.n - gr.crit > 0 ? gr.errNon / (gr.n - gr.crit) : NaN, "#9aa3ad"]];
        cx.font = "11px system-ui, sans-serif";
        bars.forEach(function (bb, j) {
          var bx = c2.x + 30 + j * (c2.w - 50) / 3, bw = (c2.w - 50) / 3 - 18;
          cx.strokeStyle = "#2a3039"; cx.strokeRect(bx, y0 - hmax, bw, hmax);
          if (!isNaN(bb[1])) {
            cx.fillStyle = bb[2]; cx.fillRect(bx, y0 - hmax * bb[1], bw, hmax * bb[1]);
            cx.fillStyle = C.ink; cx.textAlign = "center"; cx.fillText(Math.round(100 * bb[1]) + "%", bx + bw / 2, y0 - hmax * bb[1] - 6);
          }
          cx.fillStyle = C.muted; cx.textAlign = "center"; T.wrap(cx, bb[0], bx + bw / 2, y0 + 14, bw + 10, 13);
        });
        cx.restore();
      },
      readout: function () {
        var a = tally("alone"), gr = tally("group");
        return [["answers", String(task.count)], ["alone, errors", a.n ? a.err + " / " + a.n : "-"],
                ["with a wrong majority", gr.crit ? gr.conf + " / " + gr.crit : "-"]];
      },
      note: "Nothing you answer is stored or sent. The five earlier answers are scripted: there is no one else, and you know it, which is the main difference from Asch's room, where the others were present, spoke aloud and were in on it. Eight of the twelve trials are critical: the majority is unanimous and chooses a line that is clearly wrong.",
    });
  };
})();
