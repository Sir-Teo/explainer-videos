// Interactives for Act VI, Feeling and Wanting (Parts 28-29).  Each is an experiment the reader takes part in, built
// on the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 28: sooner or later.  The adjusting-amount procedure at six delays, and your discount curve ---------
  W.discount = function (el) {
    var w = null, NOW = "#ff9f43", LATER = "#5bd18b", FIT = "#f2c14e", REF = "#9aa4b2";
    var DELAYS = [1, 7, 30, 90, 180, 365], NAMES = ["1 day", "1 week", 1 + " month", "3 months", "6 months", "1 year"];
    var AMOUNT = 100, STEPS = 6;
    var st = { phase: "idle", items: [], k: 0, cells: [], repeat: null };
    function start(seed) {
      var r = QB.rng(seed * 6007 + 28), order = [0, 1, 2, 3, 4, 5], i, j, t;
      for (i = order.length - 1; i > 0; i--) { j = Math.floor(r() * (i + 1)); t = order[i]; order[i] = order[j]; order[j] = t; }
      st.cells = DELAYS.map(function (d) { return { d: d, now: AMOUNT / 2, step: AMOUNT / 4, done: 0 }; });
      st.repeat = { d: DELAYS[2], now: AMOUNT / 2, step: AMOUNT / 4, done: 0 };   // one month, measured twice
      st.items = [];
      // interleave the delays: each round asks every delay once, in a shuffled order
      for (j = 0; j < STEPS; j++) {
        for (i = 0; i < order.length; i++) st.items.push({ c: order[i] });
        st.items.push({ c: -1 });
      }
      st.k = 0; st.phase = "go";
    }
    function cell(it) { return it.c < 0 ? st.repeat : st.cells[it.c]; }
    function indiff(c) { return c.done ? c.now : null; }
    function fitK() {   // least squares of indifference points on A / (1 + kD), by a grid in log k
      var pts = st.cells.filter(function (c) { return c.done === STEPS; });
      if (pts.length < 3) return null;
      var best = null, bestE = Infinity, e, i, k;
      for (i = 0; i <= 400; i++) {
        k = Math.pow(10, -5 + 5 * i / 400);
        e = 0;
        pts.forEach(function (c) { var m = AMOUNT / (1 + k * c.d); e += (c.now - m) * (c.now - m); });
        if (e < bestE) { bestE = e; best = k; }
      }
      return best;
    }
    function auc() {
      var pts = st.cells.filter(function (c) { return c.done === STEPS; });
      if (pts.length < DELAYS.length) return null;
      var x = [0].concat(DELAYS.map(function (d) { return d / 365; })), y = [1].concat(st.cells.map(function (c) { return c.now / AMOUNT; }));
      var a = 0, i;
      for (i = 1; i < x.length; i++) a += (x[i] - x[i - 1]) * (y[i] + y[i - 1]) / 2;
      return a;
    }
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return st.phase === "go"; },
      respond: function (side) {
        var c = cell(st.items[st.k]);
        // side 0: the amount now; side 1: 100 later.  Taking it now means the offer was above your indifference
        // point, so the next offer falls; waiting means it was below, so it rises
        c.now = side === 0 ? c.now - c.step : c.now + c.step;
        c.step /= 2;
        c.done++;
        task.count++;
        st.k++;
        st.phase = "pause";
        if (w) w.render();
        task.later(function () { st.phase = st.k >= st.items.length ? "done" : "go"; if (w) w.render(); }, 300);
      },
    });
    function card(ctx, x, y, wd, ht, lines, col) {
      ctx.save();
      ctx.fillStyle = "#0b0f16"; ctx.fillRect(x, y, wd, ht);
      ctx.strokeStyle = col; ctx.lineWidth = 2; ctx.strokeRect(x, y, wd, ht);
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      var i, y0 = y + ht / 2 - (lines.length - 1) * 11;
      for (i = 0; i < lines.length; i++) {
        ctx.fillStyle = i === 0 ? col : C.ink; ctx.font = (i === 0 ? "600 18px" : "13px") + " system-ui, sans-serif";
        ctx.fillText(lines[i], x + wd / 2, y0 + 22 * i);
      }
      ctx.restore();
    }
    w = QB.widget(el, {
      title: "Sooner or later: your discount curve",
      sub: "Forty-two choices between some money now and 100 later. F (or tap left) for the money now, J (or tap right) for 100 later. Each answer moves that delay's next offer halfway toward the point where you would switch. One delay is measured twice, to see how consistent you are.",
      panels: 2, height: 330, weights: [1.1, 1],
      controls: [],
      buttons: [
        { label: "Start", act: function (state) { start(state.seed); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); st.phase = "idle"; st.cells = []; st.repeat = null; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (st.phase === "go") {
          var it = st.items[st.k], c = cell(it), cw = (b.w - 60) / 2, ch = Math.min(120, b.h - 120);
          var name = NAMES[DELAYS.indexOf(c.d)];
          ctx.save(); ctx.textAlign = "center"; ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("Which would you rather have?", b.cx, b.y + 30);
          ctx.fillText("choice " + (st.k + 1) + " of " + st.items.length, b.cx, b.y + b.h - 18);
          ctx.restore();
          card(ctx, b.x + 20, b.cy - ch / 2 + 6, cw, ch, ["$" + c.now.toFixed(2), "now"], NOW);
          card(ctx, b.x + 40 + cw, b.cy - ch / 2 + 6, cw, ch, ["$" + AMOUNT, "in " + name], LATER);
        } else if (st.phase === "pause") {
          T.message(ctx, b, "...");
        } else if (st.phase === "done") {
          T.message(ctx, b, "Done.", "On the right: what 100 later is worth to you now, at each delay, with the hyperbola that fits best.");
        } else {
          T.message(ctx, b, "On you", "Press Start. Answer as if the money were real. There are no right answers, only yours.");
        }
        var a = g[1].axes({ x: [0, 365], y: [0, 105], xticks: [0, 90, 180, 365], yticks: [0, 50, 100],
          title: "Worth now of 100 later", xlabel: "delay (days)", ylabel: "dollars now" });
        a.line([0, 365], [100, 100], { color: REF, width: 1, dash: [5, 4] });
        var k = fitK(), xs = QB.linspace(0, 365, 80);
        if (k !== null) a.line(xs, xs.map(function (d) { return AMOUNT / (1 + k * d); }), { color: FIT, width: 2 });
        st.cells.forEach(function (c) {
          var v = indiff(c);
          if (v !== null) a.dots([c.d], [v], { color: c.done === STEPS ? LATER : REF, r: 5 });
        });
        if (st.repeat && st.repeat.done) a.dots([st.repeat.d + 6], [st.repeat.now], { color: NOW, r: 5 });
        a.legend([["your points", LATER], ["one month, again", NOW], ["best hyperbola", FIT]], { pos: "tr" });
      },
      readout: function () {
        var out = [["choices", String(task.count)]];
        st.cells.forEach(function (c, i) {
          if (c.done === STEPS) out.push([NAMES[i] + ": worth now", "$" + c.now.toFixed(1)]);
        });
        if (st.repeat && st.repeat.done === STEPS) {
          out.push(["one month, measured again", "$" + st.repeat.now.toFixed(1) + " (difference " + Math.abs(st.repeat.now - st.cells[2].now).toFixed(1) + ")"]);
        }
        var k = fitK(), A = auc();
        if (k !== null) out.push(["your hyperbolic k", k.toPrecision(2) + " a day; 100 in a year is worth $" + (AMOUNT / (1 + 365 * k)).toFixed(0)]);
        if (A !== null) out.push(["area under your points", A.toFixed(2) + " (1 = no discounting)"]);
        return out;
      },
      note: "Nothing you choose is stored or sent. Each delay gets six questions, starting at $50 and moving by $25, $12.50 and so on, so each point is good to within about $1.60. The curve is the hyperbola V = 100 / (1 + kD) that fits your six points best (Mazur 1987); the area under the points (Myerson, Green and Warusawitharana 2001) needs no model. Hypothetical money gives much the same curves as real money in studies that compared them, but your answer is about this moment and this money, not a fixed trait.",
    });
  };
})();
