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

  // ---- Part 29: the map of feelings.  Same or different for 45 pairs of faces, scaled into a map of yours -------
  W.faces = function (el) {
    var w = null, FACE = "#ff9f43", YOURS = "#5bd18b", TRUE = "#9aa4b2", LINK = "#b39ddb";
    // the same ten faces, on the same valence-arousal plane, as emotion.FACES
    var NAMES = ["excited", "happy", "content", "calm", "tired", "sad", "afraid", "angry", "surprised", "neutral"];
    var VA = [[0.7, 0.75], [0.9, 0.3], [0.75, -0.45], [0.2, -0.8], [-0.35, -0.8], [-0.8, -0.4], [-0.6, 0.85],
              [-0.85, 0.5], [0.05, 0.95], [0, 0]];
    var N = NAMES.length;
    var st = { phase: "idle", pairs: [], k: 0, D: null, map: null };
    function start(seed) {
      var r = QB.rng(seed * 7919 + 29), i, j, t;
      st.pairs = [];
      for (i = 0; i < N; i++) for (j = i + 1; j < N; j++) st.pairs.push(r() < 0.5 ? [i, j] : [j, i]);
      for (i = st.pairs.length - 1; i > 0; i--) { j = Math.floor(r() * (i + 1)); t = st.pairs[i]; st.pairs[i] = st.pairs[j]; st.pairs[j] = t; }
      st.D = []; for (i = 0; i < N; i++) { st.D.push([]); for (j = 0; j < N; j++) st.D[i].push(0); }
      st.k = 0; st.map = null; st.phase = "go";
    }
    // classical scaling: B = -1/2 J D^2 J, its top two eigenvectors by power iteration with deflation
    function mds(D) {
      var n = D.length, i, j, k, B = [], rm = [], all = 0;
      for (i = 0; i < n; i++) { B.push([]); for (j = 0; j < n; j++) B[i].push(D[i][j] * D[i][j]); }
      for (i = 0; i < n; i++) { rm.push(0); for (j = 0; j < n; j++) rm[i] += B[i][j] / n; all += rm[i] / n; }
      for (i = 0; i < n; i++) for (j = 0; j < n; j++) B[i][j] = -0.5 * (B[i][j] - rm[i] - rm[j] + all);
      var X = [], vals = [];
      for (i = 0; i < n; i++) X.push([0, 0]);
      for (k = 0; k < 2; k++) {
        var v = [], it, lam = 0, nv;
        for (i = 0; i < n; i++) v.push(Math.sin(1.7 * i + 0.3 + k));
        for (it = 0; it < 300; it++) {
          var u = [];
          for (i = 0; i < n; i++) { u.push(0); for (j = 0; j < n; j++) u[i] += B[i][j] * v[j]; }
          nv = Math.sqrt(u.reduce(function (s, x) { return s + x * x; }, 0)) || 1;
          lam = 0; for (i = 0; i < n; i++) lam += v[i] * u[i];
          v = u.map(function (x) { return x / nv; });
        }
        lam = 0;
        for (i = 0; i < n; i++) { var bv = 0; for (j = 0; j < n; j++) bv += B[i][j] * v[j]; lam += v[i] * bv; }
        vals.push(lam);
        for (i = 0; i < n; i++) X[i][k] = v[i] * Math.sqrt(Math.max(lam, 0));
        for (i = 0; i < n; i++) for (j = 0; j < n; j++) B[i][j] -= lam * v[i] * v[j];
      }
      return { X: X, vals: vals };
    }
    // the rotation or reflection and scale that best map X onto Y (both centred), and the correlation
    function procrustes(X, Y) {
      function centre(P) {
        var m = [0, 0]; P.forEach(function (p) { m[0] += p[0] / P.length; m[1] += p[1] / P.length; });
        return { P: P.map(function (p) { return [p[0] - m[0], p[1] - m[1]]; }), m: m };
      }
      var xc = centre(X), yc = centre(Y), best = null;
      [1, -1].forEach(function (flip) {
        var P = xc.P.map(function (p) { return [p[0], flip * p[1]]; }), M = [[0, 0], [0, 0]], ss = 0;
        P.forEach(function (p, i) {
          var q = yc.P[i]; M[0][0] += p[0] * q[0]; M[0][1] += p[0] * q[1]; M[1][0] += p[1] * q[0]; M[1][1] += p[1] * q[1];
          ss += p[0] * p[0] + p[1] * p[1];
        });
        var th = Math.atan2(M[0][1] - M[1][0], M[0][0] + M[1][1]), c = Math.cos(th), s = Math.sin(th);
        var fit = c * (M[0][0] + M[1][1]) + s * (M[0][1] - M[1][0]);
        if (!best || fit > best.fit) best = { fit: fit, P: P, c: c, s: s, sc: ss > 0 ? fit / ss : 0 };
      });
      var Z = best.P.map(function (p) {
        return [best.sc * (best.c * p[0] - best.s * p[1]) + yc.m[0], best.sc * (best.s * p[0] + best.c * p[1]) + yc.m[1]];
      });
      var a = [], b = [];
      Z.forEach(function (z, i) { a.push(z[0], z[1]); b.push(Y[i][0], Y[i][1]); });
      var ma = a.reduce(function (s, x) { return s + x; }, 0) / a.length, mb = b.reduce(function (s, x) { return s + x; }, 0) / b.length;
      var sab = 0, saa = 0, sbb = 0, i;
      for (i = 0; i < a.length; i++) { sab += (a[i] - ma) * (b[i] - mb); saa += (a[i] - ma) * (a[i] - ma); sbb += (b[i] - mb) * (b[i] - mb); }
      return { Z: Z, r: saa > 0 && sbb > 0 ? sab / Math.sqrt(saa * sbb) : 0 };
    }
    function finish() {
      var m = mds(st.D), pr = procrustes(m.X, VA), tot = 0, i, j;
      for (i = 0; i < N; i++) for (j = i + 1; j < N; j++) tot += st.D[i][j];
      st.map = { Z: pr.Z, r: pr.r, vals: m.vals, different: tot };
    }
    // a face from valence and arousal, by the rule the film's faces use
    function drawFace(ctx, cx, cy, r, v, a, col) {
      ctx.save();
      ctx.strokeStyle = col; ctx.fillStyle = "rgba(0,0,0,0.6)"; ctx.lineWidth = Math.max(2, r / 16);
      ctx.beginPath(); ctx.arc(cx, cy, r, 0, 2 * Math.PI); ctx.fill(); ctx.stroke();
      var eh = (0.06 + 0.07 * (a + 1) / 2) * r / 0.5, ew = 0.12 * r / 0.5;
      ctx.fillStyle = col;
      [-0.35, 0.35].forEach(function (dx) {
        ctx.beginPath(); ctx.ellipse(cx + dx * r, cy - 0.18 * r, ew / 2, eh / 2, 0, 0, 2 * Math.PI); ctx.fill();
      });
      var lift = 0.38 * r + 0.08 * r * a, tilt = 0;
      if (v < -0.2 && a > 0.2) tilt = v < -0.75 ? 0.12 * r : -0.12 * r;
      ctx.beginPath();
      ctx.moveTo(cx - 0.5 * r, cy - lift); ctx.lineTo(cx - 0.18 * r, cy - (lift - tilt));
      ctx.moveTo(cx + 0.18 * r, cy - (lift - tilt)); ctx.lineTo(cx + 0.5 * r, cy - lift);
      ctx.stroke();
      var mw = 0.5 * r, c = -0.28 * r * v, y0 = 0.38 * r, open = Math.max(a, 0) * 0.16 * r;
      ctx.beginPath(); ctx.moveTo(cx - mw, cy + y0); ctx.quadraticCurveTo(cx, cy + y0 - 2 * c, cx + mw, cy + y0); ctx.stroke();
      if (open > 0.01) {
        ctx.beginPath(); ctx.moveTo(cx - 0.8 * mw, cy + y0 + 0.02 * r);
        ctx.quadraticCurveTo(cx, cy + y0 - 2 * c + 2 * open, cx + 0.8 * mw, cy + y0 + 0.02 * r); ctx.stroke();
      }
      ctx.restore();
    }
    var task = T.create(el, {
      keys: { f: 0, j: 1 },
      accepting: function () { return st.phase === "go"; },
      respond: function (side) {
        var p = st.pairs[st.k];
        st.D[p[0]][p[1]] = st.D[p[1]][p[0]] = side;   // 0: the same feeling; 1: different
        task.count++;
        st.k++;
        st.phase = "pause";
        if (st.k >= st.pairs.length) finish();
        if (w) w.render();
        task.later(function () { st.phase = st.k >= st.pairs.length ? "done" : "go"; if (w) w.render(); }, 250);
      },
    });
    w = QB.widget(el, {
      title: "The map of feelings: same or different?",
      sub: "Forty-five pairs of schematic faces, every pair of ten. F (or tap left) if the two show the same feeling, J (or tap right) if they show different feelings. Then classical scaling turns your answers into a map, rotated onto the plane the faces were drawn from.",
      panels: 2, height: 340, weights: [1.1, 1],
      controls: [],
      buttons: [
        { label: "Start", act: function (state) { start(state.seed); } },
        { label: "Clear", act: function (state) { state.seed++; task.clear(); st.phase = "idle"; st.pairs = []; st.map = null; } },
      ],
      draw: function (g) {
        var ctx = g.ctx, b = T.stage(g, 0, task);
        if (st.phase === "go") {
          var p = st.pairs[st.k], r = Math.min(70, b.h / 3.6, b.w / 6);
          ctx.save(); ctx.textAlign = "center"; ctx.fillStyle = C.muted; ctx.font = "12px system-ui, sans-serif";
          ctx.fillText("The same feeling (F), or different (J)?", b.cx, b.y + 28);
          ctx.fillText("pair " + (st.k + 1) + " of " + st.pairs.length, b.cx, b.y + b.h - 16);
          ctx.restore();
          drawFace(ctx, b.cx - b.w / 4, b.cy + 4, r, VA[p[0]][0], VA[p[0]][1], FACE);
          drawFace(ctx, b.cx + b.w / 4, b.cy + 4, r, VA[p[1]][0], VA[p[1]][1], FACE);
        } else if (st.phase === "pause") {
          T.message(ctx, b, "...");
        } else if (st.phase === "done") {
          T.message(ctx, b, "Your map", "On the right: where your answers put each face (green), joined to where it was drawn from (grey).");
        } else {
          T.message(ctx, b, "On you", "Press Start, then answer quickly: same feeling, or different? There are no right answers.");
        }
        var a = g[1].axes({ x: [-1.3, 1.3], y: [-1.3, 1.3], xticks: [-1, 0, 1], yticks: [-1, 0, 1],
          title: st.map ? "Your map, rotated onto the plane" : "The plane the faces were drawn from",
          xlabel: "unpleasant to pleasant", ylabel: "calm to aroused" });
        a.dots(VA.map(function (q) { return q[0]; }), VA.map(function (q) { return q[1]; }), { color: TRUE, r: 4 });
        if (st.map) {
          st.map.Z.forEach(function (z, i) { a.line([VA[i][0], z[0]], [VA[i][1], z[1]], { color: LINK, width: 1 }); });
          a.dots(st.map.Z.map(function (z) { return z[0]; }), st.map.Z.map(function (z) { return z[1]; }), { color: YOURS, r: 5 });
          st.map.Z.forEach(function (z, i) { a.text(z[0], z[1], NAMES[i], { color: C.ink, dx: 6, size: 10 }); });
        } else {
          VA.forEach(function (q, i) { a.text(q[0], q[1], NAMES[i], { color: C.muted, dx: 6, size: 10 }); });
        }
      },
      readout: function () {
        var out = [["pairs answered", String(task.count)]];
        if (st.map) {
          out.push(["pairs you called different", st.map.different + " of 45"]);
          out.push(["your map against the true plane", "r = " + st.map.r.toFixed(2)]);
          var tot = st.map.vals[0] + st.map.vals[1];
          if (tot > 0) out.push(["share of the map on the first dimension", (100 * st.map.vals[0] / tot).toFixed(0) + "%"]);
          out.push(["Psyche, answering each pair once", "r = 0.68 (ten times: 0.98)"]);
        }
        return out;
      },
      note: "Nothing you answer is stored or sent. Each answer is one bit, so a map from 45 bits is coarse; that it recovers the plane at all is the point of classical scaling (Torgerson 1952), which needs no theory of what the dimensions are. The faces vary only in valence and arousal, so the plane is known; with real faces, Abelson and Sermat (1962) found the same two dimensions in people's judgments. Procrustes rotation (or reflection) and scaling are allowed because a map from distances has no fixed orientation.",
    });
  };
})();
