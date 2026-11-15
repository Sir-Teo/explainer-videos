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
})();
