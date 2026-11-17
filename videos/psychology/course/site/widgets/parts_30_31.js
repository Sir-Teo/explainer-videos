// Interactives for Act VII, Growing (Parts 30-31).  Each is an experiment the reader takes part in, built on the
// task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 30: predict the infant.  Six published looking-time results; where did infants look longer? --------
  W.infant = function (el) {
    var w = null, LEFT = "#7ec8f5", RIGHT = "#ffb3c7", OK = "#5bd18b", NO = "#ef6f6c", AMBER = "#f2c14e";
    var ITEMS = [
      { q: "A screen rotates back toward a box hidden behind it.", a: "it stops where it meets the box",
        b: "it rotates on, through the box's space", ans: 1, who: "5-month-olds (Baillargeon, Spelke & Wasserman 1985)",
        status: "contested", note: "the looking pattern repeats; whether it shows knowledge of the box is argued" },
      { q: "One doll, then a second added behind a screen. The screen drops.", a: "two dolls", b: "one doll", ans: 1,
        who: "5-month-olds (Wynn 1992)", status: "contested", note: "pooled d = 0.34 over 12 studies; arithmetic or familiarity?" },
      { q: "From a box of mostly white balls, five are drawn.", a: "four white, one red", b: "four red, one white", ans: 1,
        who: "8-month-olds (Xu & Garcia 2008)", status: "not entered", note: "infants as intuitive statisticians" },
      { q: "A voice talks to the infant.", a: "adult-directed speech", b: "infant-directed speech", ans: 1,
        who: "3 to 15 months (ManyBabies 2020)", status: "replicated", note: "d = 0.35 in 65 laboratories, larger with age" },
      { q: "A woman's toy is moved while she cannot see. She searches.", a: "where she left it", b: "where it is now",
        ans: 1, who: "15-month-olds (Onishi & Baillargeon 2005)", status: "contested",
        note: "preregistered replications of such tasks have mostly failed" },
      { q: "After many displays of 8 dots, a new display.", a: "16 dots", b: "12 dots", ans: 0,
        who: "6-month-olds (Xu & Spelke 2000)", status: "not entered", note: "Weber's law: the ratio, 2 : 1, is what matters; found again in later infant studies" }
    ];
    var st = { phase: "idle", k: 0, order: [], picks: [], last: null };
    function start(seed) {
      var r = QB.rng(seed * 4099 + 30), i, j, t;
      st.order = [0, 1, 2, 3, 4, 5];
      for (i = st.order.length - 1; i > 0; i--) { j = Math.floor(r() * (i + 1)); t = st.order[i]; st.order[i] = st.order[j]; st.order[j] = t; }
      st.k = 0; st.picks = []; st.last = null; st.phase = "go";
    }
    function card(ctx, x, y, wd, ht, lines, col) {
      ctx.save();
      ctx.fillStyle = "#0b0f16"; ctx.fillRect(x, y, wd, ht);
      ctx.strokeStyle = col; ctx.lineWidth = 2; ctx.strokeRect(x, y, wd, ht);
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      var i, y0 = y + ht / 2 - (lines.length - 1) * 10;
      for (i = 0; i < lines.length; i++) {
        ctx.fillStyle = i === 0 ? col : C.ink; ctx.font = (i === 0 ? "600 15px" : "13px") + " system-ui, sans-serif";
        ctx.fillText(lines[i], x + wd / 2, y0 + 20 * i);
      }
      ctx.restore();
    }
    function wrap(text, n) {
      var words = text.split(" "), out = [], cur = "";
      words.forEach(function (wd) { if ((cur + " " + wd).trim().length > n) { out.push(cur.trim()); cur = wd; } else { cur += " " + wd; } });
      if (cur.trim()) out.push(cur.trim());
      return out;
    }
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return st.phase === "go"; },
      respond: function (side) {
        var it = ITEMS[st.order[st.k]];
        st.picks.push({ item: st.order[st.k], side: side, right: side === it.ans });
        st.last = st.picks[st.picks.length - 1];
        task.count++;
        st.k++;
        st.phase = "feedback";
        if (w) w.render();
        task.later(function () { st.phase = st.k >= ITEMS.length ? "done" : "go"; if (w) w.render(); }, 1800);
      },
    });
    w = QB.widget(el, {
      title: "Predict the infant",
      sub: "Six published infant experiments, each with two outcomes. Which one did the infants look at longer? F (or tap left) for the left outcome, J (or tap right) for the right. After each, the reported result and what happened when it was checked.",
      panels: 2, height: 330, weights: [1.25, 1],
      controls: [],
      buttons: [
        { label: "Start", act: function (state) { start(state.seed); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); st.phase = "idle"; st.picks = []; st.k = 0; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (st.phase === "go") {
          var it = ITEMS[st.order[st.k]], cw = (b.w - 60) / 2, ch = Math.min(110, b.h - 150);
          ctx.save(); ctx.textAlign = "center"; ctx.fillStyle = C.ink; ctx.font = "14px system-ui, sans-serif";
          wrap(it.q, 48).forEach(function (ln, i) { ctx.fillText(ln, b.cx, b.y + 30 + 18 * i); });
          ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("Where did infants look longer?   (" + (st.k + 1) + " of " + ITEMS.length + ")", b.cx, b.y + b.h - 16);
          ctx.restore();
          card(ctx, b.x + 20, b.cy - ch / 2 + 18, cw, ch, ["F"].concat(wrap(it.a, 22)), LEFT);
          card(ctx, b.x + 40 + cw, b.cy - ch / 2 + 18, cw, ch, ["J"].concat(wrap(it.b, 22)), RIGHT);
        } else if (st.phase === "feedback" && st.last) {
          var jt = ITEMS[st.last.item];
          T.message(ctx, b, st.last.right ? "That is what was reported." : "The study reported the other one.",
            "Longer looks at: " + (jt.ans === 0 ? jt.a : jt.b) + ". " + jt.who + ".");
        } else if (st.phase === "done") {
          var n = st.picks.filter(function (p) { return p.right; }).length;
          T.message(ctx, b, n + " of 6 match the published results.", "On the right: what happened to each when it was checked.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Guess before you know: most people's guesses are better than chance, which is part of the lesson.");
        }
        var c2 = g[1].box, ctx2 = g.ctx, x0 = c2.x + 8, y0 = c2.y + 22, nch = Math.max(24, Math.floor((c2.w - 30) / 6.4));
        ctx2.save(); ctx2.textAlign = "left"; ctx2.font = "600 13px system-ui, sans-serif"; ctx2.fillStyle = C.ink;
        ctx2.fillText("What the Ledger says", x0, y0);
        st.picks.forEach(function (p, i) {
          var it = ITEMS[p.item], y = y0 + 24 + 50 * i;
          var col = it.status === "replicated" ? OK : (it.status === "contested" ? AMBER : C.muted);
          ctx2.fillStyle = p.right ? OK : NO; ctx2.font = "13px system-ui, sans-serif";
          ctx2.fillText((p.right ? "✓ " : "✗ ") + it.who, x0, y);
          ctx2.fillStyle = col; ctx2.font = "12px system-ui, sans-serif";
          wrap(it.status + ": " + it.note, nch).slice(0, 2).forEach(function (ln, j) { ctx2.fillText(ln, x0 + 16, y + 16 + 14 * j); });
        });
        ctx2.restore();
      },
      readout: function () {
        var n = st.picks.filter(function (p) { return p.right; }).length;
        return [["predictions", String(task.count)], ["matching the published result", n + " of " + st.picks.length]];
      },
      note: "Nothing you choose is stored or sent. Each item is a real, published looking-time result, with its status in the series' Replication Ledger ('not entered' means the part describes it without a row). A longer look is evidence about attention; what it shows about knowledge is an inference, and the inferences are where infant findings have failed.",
    });
  };
  // Part 31: three clocks.  Mystery worlds drawn as cross-sections in three years; the reader names the clock.
  W.clocks = function (el) {
    var w = null, AGE = "#7ec8f5", PER = "#f2c14e", COH = "#b39ddb", OK = "#5bd18b", NO = "#ef6f6c";
    var YEARS = [[1960, "#9aa3ad"], [1990, AGE], [2020, PER]], NAMES = ["age", "period", "cohort"], KCOL = [AGE, PER, COH];
    var S = { phase: "idle", k: 0, trials: [], log: [], last: null, a: -0.3, p: 0.2, c: 0.3, tapX: -1 };
    function world(kind, r) {
      // a function score(age, year) for one clock only, with random size and shape
      var sgn = r() < 0.8 ? 1 : -1, size = 0.6 + 0.6 * r();
      if (kind === 0) {
        var onset = 35 + 25 * r(), early = r() < 0.4;
        return function (a) { return early ? size * (Math.min(a, 40) - 20) / 20 - size * Math.max(a - onset, 0) / 25 : -sgn * size * Math.max(a - onset, 0) / 25; };
      }
      if (kind === 1) {
        var step = 1970 + 40 * r(), trend = r() < 0.5;
        return function (a, y) { return trend ? sgn * size * (y - 1990) / 30 : sgn * size * (y > step ? 1 : 0); };
      }
      return function (a, y) { return sgn * size * ((y - a) - 1940) / 50; };
    }
    function start(seed) {
      var r = QB.rng(seed * 3121 + 31), i, j, t, kinds = [0, 0, 0, 1, 1, 1, 2, 2, 2];
      for (i = kinds.length - 1; i > 0; i--) { j = Math.floor(r() * (i + 1)); t = kinds[i]; kinds[i] = kinds[j]; kinds[j] = t; }
      S.trials = kinds.map(function (kd) { return { kind: kd, f: world(kd, r), noise: r() * 1000 }; });
      S.k = 0; S.log = []; S.last = null; S.phase = "go";
    }
    function answer(choice) {
      var tr = S.trials[S.k];
      S.log.push({ kind: tr.kind, choice: choice, right: choice === tr.kind });
      S.last = S.log[S.log.length - 1];
      task.count++;
      S.k++;
      S.phase = "feedback";
      if (w) w.render();
      task.later(function () { S.phase = S.k >= S.trials.length ? "done" : "go"; if (w) w.render(); }, 2200);
    }
    el.addEventListener("pointerdown", function (e) {
      var c = e.target;
      if (!c || c.tagName !== "CANVAS") return;
      S.tapX = e.clientX - c.getBoundingClientRect().left;
    });
    var task = T.create(el, {
      keys: { a: 0, p: 1, c: 2 },
      accepting: function () { return S.phase === "go"; },
      respond: function (side, how) {
        if (how === "tap") {
          var b = task.box, third = b ? Math.floor(3 * (S.tapX - b.x) / b.w) : side * 2;
          side = Math.max(0, Math.min(2, third));
        }
        answer(side);
      },
    });
    function plot(ctx, b, f, title) {
      var x0 = b.x + 44, x1 = b.x + b.w - 16, y0 = b.y + 40, y1 = b.y + b.h - 78, lo = -2.2, hi = 2.2, i, k;
      function X(a) { return x0 + (x1 - x0) * (a - 20) / 60; }
      function Y(v) { return y1 - (y1 - y0) * (Math.max(lo, Math.min(hi, v)) - lo) / (hi - lo); }
      ctx.save();
      ctx.strokeStyle = C.muted; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x0, y1); ctx.lineTo(x1, y1); ctx.stroke();
      ctx.fillStyle = C.muted; ctx.font = "11px system-ui, sans-serif"; ctx.textAlign = "center";
      [20, 50, 80].forEach(function (a) { ctx.fillText(String(a), X(a), y1 + 14); });
      ctx.fillText("age", (x0 + x1) / 2, y1 + 28);
      ctx.save(); ctx.translate(x0 - 22, (y0 + y1) / 2); ctx.rotate(-Math.PI / 2); ctx.fillText("score", 0, 0); ctx.restore();
      if (title) { ctx.fillStyle = C.ink; ctx.font = "13px system-ui, sans-serif"; ctx.fillText(title, (x0 + x1) / 2, b.y + 24); }
      YEARS.forEach(function (yc, j) {
        ctx.strokeStyle = yc[1]; ctx.lineWidth = 3; ctx.beginPath();
        for (i = 0; i <= 30; i++) {
          var a = 20 + 2 * i, v = f(a, yc[0]);
          if (i === 0) ctx.moveTo(X(a), Y(v)); else ctx.lineTo(X(a), Y(v));
        }
        ctx.stroke();
        ctx.fillStyle = yc[1]; ctx.textAlign = "left"; ctx.font = "11px system-ui, sans-serif";
        ctx.fillText("tested " + yc[0], x0 + 8 + 78 * j, y0 - 4);
      });
      ctx.restore();
    }
    w = QB.widget(el, {
      title: "Age, period or cohort?",
      sub: "Each mystery world is drawn as three cross-sections: average score by age, in 1960, 1990 and 2020. Only one clock is at work. Press A (age), P (period) or C (cohort), or tap the left, middle or right third. On the right, set the three effects yourself and see what each design would report.",
      panels: 2, height: 360, weights: [1.15, 1],
      controls: [
        { k: "a", label: "Age effect (per decade)", min: -1, max: 1, step: 0.05, value: -0.3, fmt: function (x) { return x.toFixed(2); } },
        { k: "p", label: "Period effect (per decade)", min: -1, max: 1, step: 0.05, value: 0.2, fmt: function (x) { return x.toFixed(2); } },
        { k: "c", label: "Cohort effect (per decade)", min: -1, max: 1, step: 0.05, value: 0.3, fmt: function (x) { return x.toFixed(2); } },
      ],
      onChange: function (v) { S.a = v.a; S.p = v.p; S.c = v.c; },
      buttons: [
        { label: "Start", act: function (state) { start(state.seed); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); S.phase = "idle"; S.log = []; S.k = 0; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (S.phase === "go") {
          var tr = S.trials[S.k];
          plot(ctx, b, function (a, y) { return tr.f(a, y) + 0.05 * Math.sin(a * 0.23 + y * 0.31 + tr.noise); },
               "World " + (S.k + 1) + " of " + S.trials.length + ": which clock?");
          ctx.save(); ctx.textAlign = "center"; ctx.font = "600 14px system-ui, sans-serif";
          ["A: age", "P: period", "C: cohort"].forEach(function (t, i) {
            ctx.fillStyle = KCOL[i]; ctx.fillText(t, b.x + b.w * (i + 0.5) / 3, b.y + b.h - 22);
          });
          ctx.restore();
        } else if (S.phase === "feedback" && S.last) {
          var why = ["Every year shows the same curve: only age matters.",
                     "Within a year, age makes no difference; the years differ: a period effect.",
                     "Each year slopes with age, and the lines shift between years: generations keep their level for life."];
          T.message(ctx, b, S.last.right ? "Right: " + NAMES[S.last.kind] + "." : "It was " + NAMES[S.last.kind] + ".", why[S.last.kind]);
        } else if (S.phase === "done") {
          var n = S.log.filter(function (l) { return l.right; }).length, coh = S.log.filter(function (l) { return l.kind === 2 && l.choice === 0; }).length;
          T.message(ctx, b, n + " of " + S.log.length + " right.", coh ? "You read a cohort world as ageing " + coh + " time" + (coh > 1 ? "s" : "") + ": the cross-section's trap." : "No cohort world fooled you into seeing ageing.");
        } else {
          T.message(ctx, b, "On you", "Press Start: nine mystery worlds, three of each clock, in a random order.");
        }
        // the explorer: a Lexis map of the reader's world and what three designs would see
        var c2 = g[1].box, cx = g.ctx, gx = c2.x + 40, gy = c2.y + 30, gw = c2.w - 60, gh = Math.min(c2.h * 0.5, 170), i, j;
        function score(age, yr) { return S.a * (age - 50) / 10 + S.p * (yr - 1990) / 10 + S.c * ((yr - age) - 1940) / 10; }
        cx.save();
        for (i = 0; i < 12; i++) for (j = 0; j < 12; j++) {
          var yr = 1960 + 5 * i + 2.5, age = 20 + 5 * j + 2.5, v = Math.max(-1, Math.min(1, score(age, yr) / 4));
          var lo = [120, 90, 200], mid = [34, 38, 46], hi = [91, 209, 139], tgt = v < 0 ? lo : hi, u = Math.abs(v);
          cx.fillStyle = "rgb(" + Math.round(mid[0] + (tgt[0] - mid[0]) * u) + "," + Math.round(mid[1] + (tgt[1] - mid[1]) * u) + "," + Math.round(mid[2] + (tgt[2] - mid[2]) * u) + ")";
          cx.fillRect(gx + gw * i / 12, gy + gh - gh * (j + 1) / 12, gw / 12 + 0.5, gh / 12 + 0.5);
        }
        cx.strokeStyle = COH; cx.lineWidth = 2; cx.beginPath(); cx.moveTo(gx, gy + gh); cx.lineTo(gx + gw, gy); cx.stroke();
        cx.fillStyle = C.muted; cx.font = "11px system-ui, sans-serif"; cx.textAlign = "center";
        cx.fillText("year of test, 1960 to 2020", gx + gw / 2, gy + gh + 14);
        cx.save(); cx.translate(gx - 14, gy + gh / 2); cx.rotate(-Math.PI / 2); cx.fillText("age 20 to 80", 0, 0); cx.restore();
        cx.textAlign = "left"; cx.fillStyle = C.ink; cx.font = "600 12px system-ui, sans-serif";
        cx.fillText("Your world: green higher, purple lower; the diagonal is one life", c2.x + 10, c2.y + 16);
        var rows = [["a cross-section (many ages, one year), per decade of age", S.a - S.c, AGE],
                    ["one cohort followed (one life), per decade", S.a + S.p, COH],
                    ["the same age in later years, per decade", S.p + S.c, PER]];
        cx.font = "12px system-ui, sans-serif";
        rows.forEach(function (rw, k) {
          cx.fillStyle = rw[2]; cx.fillText(rw[0] + ": " + (rw[1] >= 0 ? "+" : "") + rw[1].toFixed(2), c2.x + 10, gy + gh + 36 + 18 * k);
        });
        cx.fillStyle = C.muted;
        var nch = Math.max(30, Math.floor((c2.w - 20) / 6.2)), msg = "Add the same k to age and cohort and take it from period: all three readings stay the same.";
        var words = msg.split(" "), lines = [], cur = "";
        words.forEach(function (wd) { if ((cur + " " + wd).trim().length > nch) { lines.push(cur.trim()); cur = wd; } else { cur += " " + wd; } });
        lines.push(cur.trim());
        lines.forEach(function (ln, k) { cx.fillText(ln, c2.x + 10, gy + gh + 36 + 18 * 3 + 4 + 15 * k); });
        cx.restore();
      },
      readout: function () {
        var n = S.log.filter(function (l) { return l.right; }).length;
        return [["answers", String(task.count)], ["right", n + " of " + S.log.length],
                ["cross-section slope", (S.a - S.c).toFixed(2)]];
      },
      note: "Nothing you choose is stored or sent. The worlds are simulated, one clock at a time. Real data mix all three, and because age = year of test - year of birth, no design can separate them without an assumption: the three readings on the right are all any data can show.",
    });
  };
})();
