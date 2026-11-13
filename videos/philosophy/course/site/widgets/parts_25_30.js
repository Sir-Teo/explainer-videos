// Interactives for Philosophy, Built, Parts 25-30: space and time, the quantum puzzle, language, phenomenology, mind.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 25: the tilting slice of simultaneity and the Rietdijk-Putnam boost -------------------------------
  W.simulslice = function (el) {
    QB.widget(el, {
      title: "Whose present? The tilting slice of simultaneity",
      sub: "A Minkowski diagram with c = 1: I am at the origin, the dashed lines are my light cone, and E is a distant event. Slide the observer's speed and the gold slice of events simultaneous with here-now tilts. Put E outside the light cone and find the speed that carries the slice through it; then move E inside the cone and see that no speed does.",
      panels: 2, height: 310,
      controls: [
        { k: "v", label: "Observer's speed v (fraction of c)", min: -0.95, max: 0.95, step: 0.01, value: 0.3, fmt: function (x) { return fmt(x, 2); } },
        { k: "et", label: "Event E: my time t", min: -2, max: 2, step: 0.05, value: 0.6, fmt: function (x) { return fmt(x, 2); } },
        { k: "ex", label: "Event E: my position x", min: -2, max: 2, step: 0.05, value: 1, fmt: function (x) { return fmt(x, 2); } },
      ],
      draw: function (g, v, s) {
        var gam = 1 / Math.sqrt(1 - v.v * v.v), tp = gam * (v.et - v.v * v.ex), xp = gam * (v.ex - v.v * v.et);
        var I = v.et * v.et - v.ex * v.ex, space = Math.abs(v.et) < Math.abs(v.ex) - 1e-9, need = space ? v.et / v.ex : 0;
        s.out = { tp: tp, xp: xp, I: I, space: space, need: need, light: Math.abs(Math.abs(v.et) - Math.abs(v.ex)) <= 1e-9 };
        var a = g[0].axes({ x: [-2.2, 2.2], y: [-2.2, 2.2], title: "Spacetime, drawn in my frame", xlabel: "my position x" });
        a.area([-2.2, 0, 2.2], [2.2, 0, 2.2], 2.2, { color: C.spot, alpha: 0.1 });
        a.area([-2.2, 0, 2.2], [-2.2, 0, -2.2], -2.2, { color: C.spot, alpha: 0.1 });
        a.line([-2.2, 2.2], [-2.2, 2.2], { color: C.muted, dash: [4, 4], width: 1 }).line([-2.2, 2.2], [2.2, -2.2], { color: C.muted, dash: [4, 4], width: 1 });
        a.line([-2.2, 2.2], [0, 0], { color: C.spot, width: 1.4 });
        a.line([-2.2, 2.2], [-2.2 * v.v, 2.2 * v.v], { color: C.idea, width: 2.4 });
        a.line([-2.2 * v.v, 2.2 * v.v], [-2.2, 2.2], { color: C.idea, width: 1.2, alpha: 0.7 });
        a.dots([0], [0], { color: C.ink, r: 4 });
        a.dots([v.ex], [v.et], { color: space ? C.gain : C.loss, r: 6 });
        a.text(v.ex, v.et, "E", { bold: true, dx: v.ex > 1.7 ? -16 : 9, dy: v.et > 1.8 ? 10 : -9 });
        a.text(0, 1.95, "my time t", { color: C.muted, dx: 8, bg: true });
        a.legend([["the observer's present", C.idea], ["my present", C.spot], ["light cone", C.muted]], { pos: "br" });
        var vs = QB.linspace(-0.95, 0.95, 191), ts = vs.map(function (u) { return (v.et - u * v.ex) / Math.sqrt(1 - u * u); });
        var b = g[1].axes({ x: [-1, 1], y: [-4, 4], title: "E's time for an observer at speed v", xlabel: "observer's speed v" });
        b.hline(0, { color: C.idea });
        b.line(vs, ts, { color: space ? C.gain : C.loss, width: 2 });
        b.vline(v.v, { color: C.muted });
        b.dots([v.v], [Math.max(-4, Math.min(4, tp))], { color: C.ink, r: 4 });
        if (space) { b.dots([need], [0], { color: C.idea, r: 5 }); b.text(need, 0, "v = t/x", { color: C.idea, dx: need > 0.5 ? -52 : 8, dy: -11, bg: true }); }
        b.text(-0.95, 3.5, space ? "spacelike: the curve crosses zero" : "not spacelike: E's sign never changes", { color: space ? C.gain : C.loss, bg: true });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["E's time for the observer", fmt(o.tp, 2)], ["interval t² − x²", fmt(o.I, 2)],
          ["E is", o.light ? "on the light cone" : o.space ? "spacelike from here-now" : (v.et > 0 ? "in my absolute future" : "in my absolute past")],
          ["speed that makes E present", o.space ? fmt(o.need, 2) : "none below c"]];
      },
      note: "Exact Lorentz transformation, t′ = γ(t − vx), in units with c = 1; nothing is simulated. E is green when it lies outside the light cone and red when inside or on it. The interval t² − x² in the readout does not change with v: it is what every observer agrees on.",
    });
  };

  // ---- Part 26: the CHSH quantity as the four measurement angles move -----------------------------------------
  W.chshangles = function (el) {
    var rad = Math.PI / 180, fold = function (d) { d = Math.abs(d) % 360; return d > 180 ? 360 - d : d; };
    var Eq = function (x, y) { return -Math.cos((x - y) * rad); }, El = function (x, y) { return -1 + 2 * fold(x - y) / 180; };
    var S = function (E, a, a2, b, b2) { return E(a, b) + E(a, b2) + E(a2, b) - E(a2, b2); };
    QB.widget(el, {
      title: "Four angles and the number S",
      sub: "Alice measures spin along a (fixed, pointing up) or a′, Bob along b or b′, on the two halves of a singlet. S adds three of the four correlations and subtracts the fourth. Any account with local, predetermined answers keeps S between −2 and 2. Turn the angles: the quantum S (blue) leaves that band and stops at 2√2; the local model (dashed) never leaves.",
      panels: 2, height: 310, weights: [0.8, 1.2],
      controls: [
        { k: "a2", label: "Alice's second angle a′", min: 0, max: 180, step: 1, value: 90, fmt: function (x) { return x + "°"; } },
        { k: "b", label: "Bob's first angle b", min: -180, max: 180, step: 1, value: 45, fmt: function (x) { return fmt(x, 0) + "°"; } },
        { k: "b2", label: "Bob's second angle b′", min: -180, max: 180, step: 1, value: -45, fmt: function (x) { return fmt(x, 0) + "°"; } },
      ],
      draw: function (g, v, s) {
        var sq = S(Eq, 0, v.a2, v.b, v.b2), sl = S(El, 0, v.a2, v.b, v.b2);
        s.out = { sq: sq, sl: sl, e: [Eq(0, v.b), Eq(0, v.b2), Eq(v.a2, v.b), Eq(v.a2, v.b2)] };
        // the dial of settings
        var c = g.ctx, bx = g[0].box, cx = bx.x + bx.w / 2, cy = bx.y + bx.h / 2 + 8, R = Math.max(40, Math.min(bx.w, bx.h - 50) / 2 - 22);
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("The settings", bx.x + 12, bx.y + 6);
        c.strokeStyle = C.line; c.lineWidth = 1; c.beginPath(); c.arc(cx, cy, R, 0, 6.2832); c.stroke();
        var ray = function (deg, col, name, wide) {
          var x = cx + R * Math.sin(deg * rad), y = cy - R * Math.cos(deg * rad);
          c.strokeStyle = col; c.lineWidth = wide; c.beginPath(); c.moveTo(cx, cy); c.lineTo(x, y); c.stroke();
          c.fillStyle = col; c.beginPath(); c.arc(x, y, 4, 0, 6.2832); c.fill();
          c.font = "600 12px system-ui, sans-serif"; c.textAlign = "center"; c.textBaseline = "middle";
          c.fillText(name, cx + (R + 13) * Math.sin(deg * rad), cy - (R + 13) * Math.cos(deg * rad));
        };
        ray(0, C.spot, "a", 2.4); ray(v.a2, C.spot, "a′", 2.4); ray(v.b, C.idea, "b", 1.6); ray(v.b2, C.idea, "b′", 1.6);
        c.font = "11px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "alphabetic";
        c.fillStyle = C.spot; c.fillText("Alice", bx.x + 12, bx.y + bx.h - 8);
        c.fillStyle = C.idea; c.fillText("Bob", bx.x + 52, bx.y + bx.h - 8);
        c.restore();
        // S as Bob's first angle sweeps
        var bs = QB.linspace(-180, 180, 181), q = [], l = [], T = 2 * Math.SQRT2;
        for (var i = 0; i < bs.length; i++) { q.push(S(Eq, 0, v.a2, bs[i], v.b2)); l.push(S(El, 0, v.a2, bs[i], v.b2)); }
        var a = g[1].axes({ x: [-180, 180], y: [-3.2, 4.4], title: "S as Bob's first angle b turns", xlabel: "b (degrees)", xticks: [-180, -90, 0, 90, 180], yticks: [-2.83, -2, 0, 2, 2.83] });
        a.area([-180, 180], [2, 2], -2, { color: C.gain, alpha: 0.1 });
        a.hline(2, { color: C.gain }).hline(-2, { color: C.gain }).hline(T, { color: C.loss }).hline(-T, { color: C.loss });
        a.line(bs, l, { color: C.muted, dash: [5, 4], width: 1.4 });
        a.line(bs, q, { color: C.spot, width: 2.2 });
        a.vline(v.b, { color: C.idea });
        a.dots([v.b], [sq], { color: C.spot, r: 5 });
        a.legend([["quantum S", C.spot], ["a local model", C.muted]], { pos: "tl" });
        a.text(178, 2, "local bound", { color: C.gain, align: "right", dy: -9 });
        a.text(178, T, "Tsirelson", { color: C.loss, align: "right", dy: -9 });
      },
      readout: function (v, s) {
        var o = s.out, big = Math.abs(o.sq) > 2 + 1e-9;
        return [["E(a,b), E(a,b′), E(a′,b), E(a′,b′)", o.e.map(function (x) { return fmt(x, 2); }).join(", ")], ["quantum S", fmt(o.sq, 3)], ["local model S", fmt(o.sl, 3)],
          ["verdict", big ? "outside the local band" : "a local model could do this"], ["CHSH game win rate", QB.pct(0.5 + Math.abs(o.sq) / 8)]];
      },
      note: "Exact values, nothing simulated. The singlet's correlation is E = −cos(angle between the settings); the dashed local model answers by a hidden direction, which gives a correlation that is a straight line in the angle. The win rate is the best the CHSH game allows with these settings, 1/2 + |S|/8: 75% at |S| = 2, about 85.4% at 2√2.",
    });
  };

  // ---- Part 27: determiners as relations between two sets, and the conservativity test ------------------------
  W.detvenn = function (el) {
    var DETS = [
      ["every", function (x, y, z) { return x === 0; }],
      ["some", function (x, y, z) { return y > 0; }],
      ["no", function (x, y, z) { return y === 0; }],
      ["most", function (x, y, z) { return y > x; }],
      ["exactly two", function (x, y, z) { return y === 2; }],
      ["at least half", function (x, y, z) { return 2 * y >= x + y; }],
      ["only", function (x, y, z) { return z === 0; }],
    ]; // x = students who do not smoke, y = students who smoke, z = smokers who are not students
    var cap = function (w) { return w.charAt(0).toUpperCase() + w.slice(1); };
    QB.widget(el, {
      title: "Does a determiner look outside the noun?",
      sub: "A determiner relates the noun's set A (students) to the verb phrase's set B (smokers). Fill the three regions and read each row: is 'Q students smoke' true, and is 'Q students are students who smoke' true? A conservative determiner gives the same answer to both. Add a smoker who is not a student and see which row breaks.",
      panels: 2, height: 310,
      controls: [
        { k: "x", label: "Students who do not smoke", min: 0, max: 6, step: 1, value: 2 },
        { k: "y", label: "Students who smoke", min: 0, max: 6, step: 1, value: 3 },
        { k: "z", label: "Smokers who are not students", min: 0, max: 6, step: 1, value: 1 },
        { k: "d", label: "Determiner read out below", min: 0, max: 6, step: 1, value: 3, fmt: function (i) { return DETS[i][0]; } },
      ],
      draw: function (g, v, s) {
        var c = g.ctx, bx = g[0].box, i, k;
        var rows = DETS.map(function (d) { var full = d[1](v.x, v.y, v.z), cut = d[1](v.x, v.y, 0); return [d[0], full, cut, full === cut]; });
        s.out = rows;
        c.save();
        // the Venn diagram
        var cy = bx.y + bx.h / 2 + 6, R = Math.max(40, Math.min(bx.w / 3.6, (bx.h - 70) / 2)), ax = bx.x + bx.w / 2 - R * 0.55, bxx = bx.x + bx.w / 2 + R * 0.55;
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("The two sets", bx.x + 12, bx.y + 6);
        c.globalAlpha = 0.16; c.fillStyle = C.spot; c.beginPath(); c.arc(ax, cy, R, 0, 6.2832); c.fill();
        c.fillStyle = C.idea; c.beginPath(); c.arc(bxx, cy, R, 0, 6.2832); c.fill(); c.globalAlpha = 1;
        c.lineWidth = 1.6; c.strokeStyle = C.spot; c.beginPath(); c.arc(ax, cy, R, 0, 6.2832); c.stroke();
        c.strokeStyle = C.idea; c.beginPath(); c.arc(bxx, cy, R, 0, 6.2832); c.stroke();
        c.font = "600 12px system-ui, sans-serif"; c.textBaseline = "middle"; c.textAlign = "center";
        c.fillStyle = C.spot; c.fillText("A: students", ax - R * 0.3, cy - R - 10);
        c.fillStyle = C.idea; c.fillText("B: smokers", bxx + R * 0.3, cy - R - 10);
        var dots = function (n, x0, col) { // n people in a column pattern centred at x0
          for (k = 0; k < n; k++) {
            var colm = k % 2, row = Math.floor(k / 2), xx = x0 + (colm - 0.5) * 16, yy = cy + (row - 1) * 18;
            c.fillStyle = col; c.beginPath(); c.arc(xx, yy, 5.5, 0, 6.2832); c.fill();
          }
        };
        dots(v.x, ax - R * 0.5, C.spot); dots(v.y, (ax + bxx) / 2, C.gain); dots(v.z, bxx + R * 0.5, C.idea);
        c.fillStyle = C.muted; c.font = "11px system-ui, sans-serif"; c.textBaseline = "alphabetic";
        c.fillText(v.x + " + " + v.y + " + " + v.z + " people", bx.x + bx.w / 2, bx.y + bx.h - 8);
        // the table
        var tb = g[1].box, x0 = tb.x + 12, w = tb.w - 24, top = tb.y + 30, rh = Math.min(30, (tb.h - 44) / 7.6);
        var cols = [x0, x0 + w * 0.42, x0 + w * 0.66, x0 + w * 0.9];
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("Seven candidates, two sentences", x0, tb.y + 6);
        c.font = "11px system-ui, sans-serif"; c.fillStyle = C.muted; c.textBaseline = "middle";
        c.fillText("Q", cols[0], top + rh * 0.3); c.textAlign = "center";
        c.fillText("Q(A, B)", cols[1], top + rh * 0.3); c.fillText("Q(A, A∩B)", cols[2], top + rh * 0.3); c.fillText("same", cols[3], top + rh * 0.3);
        for (i = 0; i < 7; i++) {
          var y = top + rh * (i + 1.1), r = rows[i];
          if (i === v.d) { c.fillStyle = "rgba(247,209,84,0.13)"; c.fillRect(x0 - 6, y - rh / 2, w + 12, rh); }
          c.textAlign = "left"; c.fillStyle = i === v.d ? C.idea : C.ink; c.font = (i === v.d ? "600 " : "") + "12px system-ui, sans-serif";
          c.fillText(r[0], cols[0], y);
          c.textAlign = "center"; c.font = "12px system-ui, sans-serif";
          c.fillStyle = r[1] ? C.gain : C.muted; c.fillText(r[1] ? "true" : "false", cols[1], y);
          c.fillStyle = r[2] ? C.gain : C.muted; c.fillText(r[2] ? "true" : "false", cols[2], y);
          c.fillStyle = r[3] ? C.gain : C.loss; c.font = "600 12px system-ui, sans-serif"; c.fillText(r[3] ? "yes" : "NO", cols[3], y);
        }
        c.restore();
      },
      readout: function (v, s) {
        var r = s.out[v.d], broken = s.out.filter(function (q) { return !q[3]; }).map(function (q) { return q[0]; });
        return [[cap(r[0]) + " students smoke:", r[1] ? "true" : "false"], [cap(r[0]) + " students are students who smoke:", r[2] ? "true" : "false"],
          ["conservativity fails here for", broken.length ? broken.join(", ") : "none"]];
      },
      note: "Exact truth conditions, as in the Reasoner: every, A ⊆ B; some, A ∩ B is not empty; no, A ∩ B is empty; most, more students smoke than do not; at least half, |A ∩ B| ≥ |A|/2; only, B ⊆ A. Blue dots are students who do not smoke, green are students who smoke, gold are smokers who are not students. 'Only' is the one that looks outside A, and it is not a determiner.",
    });
  };

  // ---- Part 28: the Rational Speech Acts listener hearing 'some' ----------------------------------------------
  W.rsacookies = function (el) {
    var listen = function (n, alpha, depth, pAll) { // the level-`depth` listener's belief over 0..n cookies after 'some'
      var P = [], s, u, k, M = [[], [], []];
      for (s = 0; s <= n; s++) { P.push(s === n ? pAll : (1 - pAll) / n); M[0].push(s === 0 ? 1 : 0); M[1].push(s >= 1 ? 1 : 0); M[2].push(s === n ? 1 : 0); }
      var norm = function (row) { var t = 0, i; for (i = 0; i < row.length; i++) t += row[i]; return row.map(function (x) { return t > 0 ? x / t : 0; }); };
      var L = M.map(function (row) { return norm(row.map(function (m, i) { return m * P[i]; })); }), said = 1;
      for (k = 0; k < depth; k++) {
        var S = []; // S[s][u]
        for (s = 0; s <= n; s++) { var r = []; for (u = 0; u < 3; u++) r.push(L[u][s] > 0 ? Math.pow(L[u][s], alpha) : 0); S.push(norm(r)); }
        L = [0, 1, 2].map(function (uu) { return norm(P.map(function (p, i) { return S[i][uu] * p; })); });
        said = S[n][1];
      }
      return { L: L[1], said: depth > 0 ? said : (pAll > 0 ? 0.5 : 1) };
    };
    QB.widget(el, {
      title: "What 'some' conveys: a listener who reasons about the speaker",
      sub: "Someone ate some of the cookies. Literally that is true whether one was eaten or all of them. The grey bars are a literal listener's beliefs after hearing 'some'; the blue bars belong to a listener who asks why the speaker did not say 'all'. Raise the speaker's rationality or the depth of reasoning and 'all' drains away; raise the prior that all were eaten and the inference weakens.",
      panels: 2, height: 300,
      controls: [
        { k: "alpha", label: "Speaker's rationality α", min: 0.5, max: 8, step: 0.1, value: 4, fmt: function (x) { return x.toFixed(1); } },
        { k: "depth", label: "Levels of reasoning", min: 0, max: 6, step: 1, value: 1 },
        { k: "n", label: "Cookies", min: 2, max: 6, step: 1, value: 3 },
        { k: "pall", label: "Prior that all were eaten", min: 0.05, max: 0.9, step: 0.01, value: 0.25, fmt: function (x) { return QB.pct(x, 0); } },
      ],
      draw: function (g, v, s) {
        var lit = listen(v.n, v.alpha, 0, v.pall), prag = listen(v.n, v.alpha, v.depth, v.pall), xs = [], i;
        for (i = 1; i <= v.n; i++) xs.push(i);
        s.out = [lit.L[v.n], prag.L[v.n], prag.said];
        var a = g[0].axes({ x: [0.4, v.n + 0.6], y: [0, 1], title: "Belief after hearing 'some'", xlabel: "cookies eaten", xticks: xs,
          xfmt: function (t) { return t === v.n ? t + " (all)" : String(t); } });
        a.bars(xs.map(function (x) { return x - 0.19; }), lit.L.slice(1), 0.36, { color: C.muted, alpha: 0.75 });
        a.bars(xs.map(function (x) { return x + 0.19; }), prag.L.slice(1), 0.36, { color: C.spot });
        a.legend([["literal listener", C.muted], ["pragmatic listener", C.spot]], { pos: "tl" });
        var al = QB.linspace(0.5, 8, 60), d, cols = [C.muted, C.spot, C.q, C.realized], lo = 1;
        var curves = [0, 1, 2, 4].map(function (dd) { return al.map(function (x) { var y = listen(v.n, x, dd, v.pall).L[v.n]; if (y < 1e-6) return null; if (y < lo) lo = y; return y; }); });
        var b = g[1].axes({ x: [0.5, 8], y: [Math.pow(10, Math.floor(Math.log10(lo))), 1], logy: true, title: "P(all | 'some') against rationality", xlabel: "speaker's rationality α" });
        for (d = 0; d < 4; d++) b.line(al, curves[d], { color: cols[d], width: d === 1 ? 2.2 : 1.4, dash: d === 0 ? [4, 4] : null });
        b.vline(v.alpha, { color: C.idea });
        b.dots([v.alpha], [Math.max(1e-6, prag.L[v.n])], { color: C.idea, r: 5 });
        b.legend([["literal (level 0)", C.muted], ["level 1", C.spot], ["level 2", C.q], ["level 4", C.realized]], { pos: "br" });
      },
      readout: function (v, s) {
        return [["literal P(all | 'some')", QB.pct(s.out[0])], ["pragmatic P(all | 'some')", s.out[1] < 0.001 ? "below 0.1%" : QB.pct(s.out[1])],
          ["a speaker who saw all says 'some'", v.depth === 0 ? "not modelled at level 0" : (s.out[2] < 0.001 ? "below 0.1%" : QB.pct(s.out[2]))]];
      },
      note: "The Rational Speech Acts model (Frank and Goodman), computed exactly: three utterances ('none', 'some', 'all'), no utterance costs, the other states share the remaining prior equally. With 3 cookies, a uniform prior (25%), α = 4 and one level, the pragmatic listener gives 'all' about 6 in 1000. The gold dot is the current setting.",
    });
  };

  // ---- Part 29: Husserl's diagram and a present with a fading tail --------------------------------------------
  W.retentionfade = function (el) {
    var NAMES = ["C", "D", "E", "F", "G", "A", "B"];
    var perms = function (n) { // all orderings of 0..n-1
      var out = [], a = [], used = [];
      var go = function () { if (a.length === n) { out.push(a.slice()); return; } for (var i = 0; i < n; i++) if (!used[i]) { used[i] = 1; a.push(i); go(); a.pop(); used[i] = 0; } };
      go(); return out;
    };
    var cache = {};
    var trace = function (m, lam) { var w = [], i; for (i = 0; i < m.length; i++) w.push(0); for (i = 0; i < m.length; i++) w[m[i]] += Math.pow(lam, m.length - 1 - i); return w; };
    QB.widget(el, {
      title: "The living present: how much of the melody is in the now?",
      sub: "Left, Husserl's diagram for one melody: each note sounds on the top line and then sinks along its diagonal, fainter by the chosen factor at each step; the gold vertical is what the present holds at the last note. Right, that present for two melodies with the same notes and the same last note. Slide the fading to 0 (a knife-edge) and to 1 (nothing fades): at both ends the two presents become the same.",
      panels: 2, height: 300,
      controls: [
        { k: "lam", label: "What a note keeps at each step into the past", min: 0, max: 1, step: 0.01, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "n", label: "Notes in the melody", min: 3, max: 6, step: 1, value: 5 },
      ],
      buttons: [{ label: "New melody", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = v.n, lam = v.lam, r = QB.rng(s.seed + 29), A = [], i, j, k;
        for (i = 0; i < n; i++) A.push(i);
        for (i = n - 1; i > 0; i--) { j = Math.floor(r() * (i + 1)); k = A[i]; A[i] = A[j]; A[j] = k; }
        var B = A.slice(0, n - 1).reverse().concat([A[n - 1]]), wA = trace(A, lam), wB = trace(B, lam);
        var all = cache[n] || (cache[n] = perms(n)), seen = {}, distinct = 0, diff = 0;
        for (i = 0; i < all.length; i++) { var key = trace(all[i], lam).map(function (x) { return x.toFixed(7); }).join(","); if (!seen[key]) { seen[key] = 1; distinct++; } }
        for (i = 0; i < n; i++) diff += Math.abs(wA[i] - wB[i]);
        var readable = lam > 0 && lam < 1;
        s.out = { distinct: distinct, total: all.length, diff: diff, readable: readable, A: A, B: B };
        var slope = 0.6, a = g[0].axes({ x: [-0.6, n - 0.3], y: [-(n - 1) * slope - 0.7, 0.9], title: "Melody 1 in Husserl's diagram", noY: true, xlabel: "time: the notes as they sound",
          xticks: A.map(function (q, t) { return t; }), xfmt: function (t) { return NAMES[A[t]]; } });
        a.line([-0.6, n - 0.3], [0, 0], { color: C.muted, width: 1.2 });
        for (k = 0; k < n; k++) a.line([k, n - 1], [0, -slope * (n - 1 - k)], { color: C.spot, width: 1.2, alpha: 0.55 });
        a.line([n - 1, n - 1], [0.35, -slope * (n - 1) - 0.35], { color: C.idea, width: 2 });
        for (k = 0; k < n; k++) {
          var age = n - 1 - k, wt = Math.pow(lam, age);
          a.dots([k], [0], { color: C.ink, r: 3.5 });
          a.dots([n - 1], [-slope * age], { color: C.spot, r: 3 + 7 * wt, alpha: 0.25 + 0.75 * wt });
          a.text(n - 1, -slope * age, NAMES[A[k]] + (age === 0 ? " now" : ""), { align: "right", dx: -15, color: wt > 0.02 ? C.ink : C.muted, bg: true });
        }
        a.text(-0.5, 0.55, "now-points", { color: C.muted });
        var xs = [], top = 0; for (i = 0; i < n; i++) { xs.push(i); top = Math.max(top, wA[i], wB[i]); }
        var b = g[1].axes({ x: [-0.6, n - 0.4], y: [0, Math.max(1.05, top * 1.2)], title: "What the present holds at the last note", xlabel: "note", xticks: xs, xfmt: function (t) { return NAMES[t]; } });
        b.bars(xs.map(function (x) { return x - 0.19; }), wA, 0.36, { color: C.spot });
        b.bars(xs.map(function (x) { return x + 0.19; }), wB, 0.36, { color: C.idea });
        b.legend([["melody 1", C.spot], ["melody 2", C.idea]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out, nm = function (m) { return m.map(function (q) { return NAMES[q]; }).join(" "); };
        return [["melody 1", nm(o.A)], ["melody 2", nm(o.B)], ["the two presents differ by", fmt(o.diff, 2)],
          ["orderings told apart", o.distinct + " of " + o.total], ["order readable from the present", o.readable ? "yes: faintest first" : "no"]];
      },
      note: "A model in the spirit of Husserl's retention, as in the film, not his analysis: every past note is held with weight (fading factor) raised to its age. Melody 2 is melody 1 with the earlier notes in reverse order. With factor 0 only the sounding note is held, and the orderings fall into as many groups as there are notes; with factor 1 every note is held equally and the order is lost.",
    });
  };

  // ---- Part 30: Yablo's pigeon and the proportional cause -----------------------------------------------------
  W.pigeonred = function (el) {
    var SH = [["scarlet", "#ff4d2e"], ["crimson", "#e0315a"], ["maroon", "#a8323e"], ["teal", "#2aa198"], ["navy", "#4c6ef5"], ["olive", "#9a9a3a"]];
    var lg = function (x) { return Math.log(x) / Math.LN2; };
    var info = function (groups, peck) { // bits the cause carries about pecking when each of its values is set with equal chance
      var py = 0, I = 0, q = 1 / groups.length, pgs = groups.map(function (gr) { var t = 0; gr.forEach(function (k) { t += peck[k] / gr.length; }); return t; });
      pgs.forEach(function (pg) { py += q * pg; }); // the pecking rate under the intervention itself
      pgs.forEach(function (pg) {
        if (pg > 0 && py > 0) I += q * pg * lg(pg / py);
        if (pg < 1 && py < 1) I += q * (1 - pg) * lg((1 - pg) / (1 - py));
      });
      return Math.max(0, I);
    };
    var CANDS = [["red", [[0, 1, 2], [3, 4, 5]], 1], ["scarlet", [[0], [1, 2, 3, 4, 5]], 1], ["the exact shade", [[0], [1], [2], [3], [4], [5]], Math.log(6) / Math.LN2]];
    QB.widget(el, {
      title: "Sophie the pigeon: which cause is the right size?",
      sub: "Six shades, three of them red. Sophie pecks at the shades she was trained on. Each candidate cause is set by intervention and scored by the bits it carries about pecking (blue) against the bits it takes to state (grey). Trained on all three reds, 'red' carries everything the exact shade does for 1 bit instead of 2.58. Train her on scarlet alone, or on two reds, and see the proportional cause change.",
      panels: 2, height: 300,
      controls: [
        { k: "k", label: "Shades she pecks at", min: 1, max: 6, step: 1, value: 3, fmt: function (k) { return k === 1 ? "scarlet only" : k === 3 ? "the three reds" : k === 6 ? "all six" : "the first " + k; } },
        { k: "hit", label: "Chance of pecking at a trained shade", min: 0.5, max: 0.99, step: 0.01, value: 0.95, fmt: function (x) { return QB.pct(x, 0); } },
        { k: "fa", label: "Chance of pecking at any other shade", min: 0.01, max: 0.5, step: 0.01, value: 0.05, fmt: function (x) { return QB.pct(x, 0); } },
      ],
      draw: function (g, v, s) {
        var peck = [], i;
        for (i = 0; i < 6; i++) peck.push(i < v.k ? v.hit : v.fa);
        var res = CANDS.map(function (c) { return [c[0], info(c[1], peck), c[2]]; }), best = 0;
        for (i = 1; i < 3; i++) if (res[i][1] > res[best][1] + 1e-9 || (Math.abs(res[i][1] - res[best][1]) <= 1e-9 && res[i][2] < res[best][2])) best = i;
        s.out = { res: res, best: res[best][1] > 1e-6 ? res[best][0] : "none: nothing here makes a difference" };
        var a = g[0].axes({ x: [0.4, 6.6], y: [0, 1.2], yticks: [0, 0.2, 0.4, 0.6, 0.8, 1], title: "How often she pecks at each shade", xticks: [1, 2, 3, 4, 5, 6], xfmt: function (t) { return SH[t - 1][0]; },
          yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        a.bars([1, 2, 3, 4, 5, 6], peck, 0.62, { color: function (q) { return SH[q][1]; } });
        a.line([0.6, 3.4], [1.05, 1.05], { color: C.ink, width: 2 });
        a.text(2, 1.125, "the reds", { align: "center" });
        var b = g[1].axes({ x: [0.4, 3.6], y: [0, 2.8], title: "Three candidate causes of a peck", xticks: [1, 2, 3], xfmt: function (t) { return res[t - 1][0]; } });
        b.bars([0.82, 1.82, 2.82], res.map(function (r) { return r[1]; }), 0.32, { color: C.spot });
        b.bars([1.18, 2.18, 3.18], res.map(function (r) { return r[2]; }), 0.32, { color: C.cash, alpha: 0.6 });
        for (i = 0; i < 3; i++) b.text(i + 0.82, res[i][1], fmt(res[i][1], 2), { align: "center", dy: -9, size: 11 });
        b.legend([["bits about pecking", C.spot], ["bits to state the cause", C.cash]], { pos: "tl" });
      },
      readout: function (v, s) {
        var r = s.out.res;
        return [["'red' carries", fmt(r[0][1], 3) + " bits"], ["'scarlet' carries", fmt(r[1][1], 3) + " bits"], ["the exact shade carries", fmt(r[2][1], 3) + " bits"],
          ["most difference for the fewest bits", s.out.best]];
      },
      note: "Exact mutual information between the candidate cause and pecking, when each value of the cause is set by intervention with equal chance and the shade is then drawn evenly within that value (after Yablo 1992, Woodward 2003, List and Menzies 2009). At the film's setting (three reds, 95% and 5%) 'red' and the exact shade both carry 0.714 bits. For 'scarlet' this page gives 0.273 where the film shows 0.369: the film's figure is measured against the pecking rate over all six shades, this one against the rate under the intervention.",
    });
  };
})();
