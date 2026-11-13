// Interactives for Acts II and III: the limits of proof, the liar, mathematics, the moderns, knowledge (Parts 7-12).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  function heading(ctx, b, str) { // a panel title in the style of Axes
    ctx.save(); ctx.fillStyle = C.ink; ctx.font = "600 12.5px system-ui, sans-serif"; ctx.textAlign = "left"; ctx.textBaseline = "top";
    ctx.fillText(str, b.x + 12, b.y + 6); ctx.restore();
  }
  function label(ctx, str, x, y, o) { // small text; o: color, align, base, size, bold
    o = o || {}; ctx.save(); ctx.fillStyle = o.color || C.muted; ctx.font = (o.bold ? "600 " : "") + (o.size || 11.5) + "px system-ui, sans-serif";
    ctx.textAlign = o.align || "left"; ctx.textBaseline = o.base || "middle"; ctx.fillText(str, x, y); ctx.restore();
  }

  // ---- Part 7: Turing machines and the busy beaver game ------------------------------------------------------
  W.beaverrun = function (el) {
    var NAMES = ["a random two-state machine", "two-state champion", "three-state champion", "four-state champion"];
    var CHAMPS = [null, "1RB1LB_1LA1RZ", "1RB1RZ_1LB0RC_1LC1LA", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA"];
    var parse = function (code) { // standard notation -> rules[2 * state + symbol] = [write, move, next] (next -1 halts)
      var rules = [], blocks = code.split("_"), i, k, t;
      for (i = 0; i < blocks.length; i++) for (k = 0; k < 2; k++) {
        t = blocks[i].substr(3 * k, 3);
        rules.push([+t[0], t[1] === "R" ? 1 : -1, t[2] === "Z" ? -1 : "ABCD".indexOf(t[2])]);
      }
      return rules;
    };
    var text = function (rules) {
      var out = [], i;
      for (i = 0; i < rules.length; i++) out.push((i % 2 ? "" : (i ? " " : "")) + rules[i][0] + (rules[i][1] > 0 ? "R" : "L") + (rules[i][2] < 0 ? "Z" : "ABCD"[rules[i][2]]));
      return out.join("");
    };
    var run = function (rules, cap, each) { // from a blank tape in state A; each(step, tape, head, state) before every step
      var tape = new Uint8Array(260), head = 130, state = 0, steps = 0, lo = 130, hi = 130, r, ones = 0, i;
      while (state >= 0 && steps < cap) {
        if (each) each(steps, tape, head, state);
        r = rules[2 * state + tape[head]]; tape[head] = r[0]; head += r[1]; state = r[2]; steps++;
        if (head < lo) lo = head; if (head > hi) hi = head;
      }
      if (each) each(steps, tape, head, state);
      for (i = 0; i < 260; i++) ones += tape[i];
      return { steps: steps, halted: state < 0, lo: lo, hi: hi, ones: ones };
    };
    QB.widget(el, {
      title: "Run a machine, then try to referee the busy beaver game",
      sub: "Left: a Turing machine started on a blank tape, one row per step (gold cells hold a 1, the blue cell is under the head). Right: all 20,736 two-state machines, by the step at which they halt. Set your patience: machines that halt by then are settled, the rest are still running, and no amount of patience tells you which of those would stop later.",
      panels: 2, height: 320,
      controls: [
        { k: "m", label: "Machine", min: 0, max: 3, step: 1, value: 3, fmt: function (x) { return NAMES[x]; } },
        { k: "t", label: "Steps shown", min: 0, max: 107, step: 1, value: 107, fmt: function (x) { return String(x); } },
        { k: "cap", label: "Patience (steps before you stop watching)", min: 1, max: 12, step: 1, value: 3, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New random machine", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var i, k, ctx = g.ctx;
        if (!s.halt) { // every two-state machine once: how many halt at exactly step k
          s.halt = new Array(61).fill(0); s.total = 0;
          var ch = [], w, mv, nx, a, b, c, d;
          for (w = 0; w < 2; w++) for (mv = -1; mv <= 1; mv += 2) for (nx = -1; nx < 2; nx++) ch.push([w, mv, nx]);
          for (a = 0; a < 12; a++) for (b = 0; b < 12; b++) for (c = 0; c < 12; c++) for (d = 0; d < 12; d++) {
            var res = run([ch[a], ch[b], ch[c], ch[d]], 60); s.total++;
            if (res.halted) s.halt[res.steps]++;
          }
        }
        var rules;
        if (v.m === 0) {
          var r = QB.rng(s.seed + 70); rules = [];
          for (i = 0; i < 4; i++) rules.push([r() < 0.5 ? 0 : 1, r() < 0.5 ? -1 : 1, Math.floor(r() * 3) - 1]);
        } else rules = parse(CHAMPS[v.m]);
        var full = run(rules, 107), shown = Math.min(v.t, full.steps);
        var b0 = g[0].box, x0 = b0.x + 66, y0 = b0.y + 46, aw = b0.w - 78, ah = b0.h - 60;
        var lo = full.lo - 1, hi = full.hi + 1, nc = hi - lo + 1, cw = Math.min(22, aw / nc), rh = Math.min(16, ah / (shown + 1));
        var ox = x0 + (aw - cw * nc) / 2, lastState = 0, lastOnes = 0;
        heading(ctx, b0, "The tape, step by step");
        label(ctx, "rules  " + text(rules), b0.x + 12, b0.y + 31, { color: C.muted });
        run(rules, shown, function (step, tape, head, state) {
          var y = y0 + step * rh, j;
          for (j = lo; j <= hi; j++) {
            ctx.fillStyle = j === head ? C.spot : tape[j] ? C.idea : C.bg;
            ctx.fillRect(ox + (j - lo) * cw, y, Math.max(1, cw - (cw > 5 ? 1 : 0)), Math.max(1, rh - (rh > 5 ? 1 : 0)));
          }
          lastState = state; lastOnes = 0; for (j = lo; j <= hi; j++) lastOnes += tape[j];
        });
        label(ctx, "step 0", x0 - 6, y0 + rh / 2, { align: "right" });
        if (shown > 0) label(ctx, "step " + shown, x0 - 6, Math.max(y0 + rh / 2 + 13, y0 + shown * rh + rh / 2), { align: "right" });
        s.out = { steps: shown, halted: lastState < 0, ones: lastOnes, total: full.steps, fullHalted: full.halted };

        var xs = [], hs = [], done = 0, later = 0, top = 0;
        for (k = 1; k <= 12; k++) { xs.push(k); hs.push(s.halt[k]); top = Math.max(top, s.halt[k]); }
        for (k = 1; k <= 60; k++) { if (k <= v.cap) done += s.halt[k]; else later += s.halt[k]; }
        s.out.done = done; s.out.later = later; s.out.running = s.total - done;
        var ax = g[1].axes({ x: [0.3, 12.7], y: [0, top * 1.3], title: "Two-state machines: when they halt", xlabel: "step", xticks: xs });
        ax.bars(xs, hs, 0.8, { color: function (j) { return xs[j] <= v.cap ? C.gain : C.loss; } });
        ax.vline(v.cap + 0.5, { color: C.ink });
        ax.legend([["halted within your patience", C.gain], ["halt later: you cannot tell yet", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["this machine", o.halted ? "halted after " + o.steps + " steps" : (o.steps < o.total ? "running at step " + o.steps : (o.fullHalted ? "halted" : "still running at step " + o.steps))],
          ["ones on the tape", String(o.ones)], ["two-state machines halted within your patience", String(o.done)],
          ["still running", String(o.running)], ["of those, halt later", String(o.later)]];
      },
      note: "Exact, not simulated: every two-state machine is run for 60 steps in your browser. 9,784 halt, none later than step 6, so BB(2) = 6; but that the other 10,952 never halt takes a proof for each, and for larger machines no program can supply those proofs.",
    });
  };

  // ---- Part 8: three sentences about each other's truth, by Kripke and by revision ------------------------
  W.liarstages = function (el) {
    var NAME = ["A", "B", "C"];
    var says = function (i, k) {
      var x = "'" + NAME[(i + 1) % 3] + "'";
      return ["snow is white", "grass is red", x + " is true", x + " is not true", "this sentence is true", "this sentence is not true", x + " is true or not true"][k];
    };
    var not = function (a) { return a === 0 ? 0 : 3 - a; }; // values: 0 neither, 1 false, 2 true
    var or = function (a, b) { return a === 2 || b === 2 ? 2 : (a === 1 && b === 1 ? 1 : 0); };
    var val = function (k, i, I) {
      var x = I[(i + 1) % 3];
      return k === 0 ? 2 : k === 1 ? 1 : k === 2 ? x : k === 3 ? not(x) : k === 4 ? I[i] : k === 5 ? not(I[i]) : or(x, not(x));
    };
    var jump = function (w, I) { return [val(w[0], 0, I), val(w[1], 1, I), val(w[2], 2, I)]; };
    var same = function (a, b) { return a[0] === b[0] && a[1] === b[1] && a[2] === b[2]; };
    var COL = [C.line, C.loss, C.gain], LET = ["n", "f", "t"];
    var cell = function (ctx, x, y, w, h, v) {
      ctx.fillStyle = COL[v]; ctx.fillRect(x, y, w - 2, h);
      label(ctx, LET[v], x + (w - 2) / 2, y + h / 2 + 1, { align: "center", color: v ? C.bg : C.muted, bold: true });
    };
    QB.widget(el, {
      title: "Three sentences that talk about each other's truth",
      sub: "Choose what A, B and C say. Left: Kripke's construction starts with no values and adds only what is forced (green true, red false, grey neither). Right: revision theory starts from a guess and revises it for ever. The chain shown is grounded. Now make a liar, a truth-teller and a cycle, and find a sentence the two theories judge differently (try 'is true or not true' about a liar).",
      panels: 2, height: 300,
      controls: [
        { k: "a", label: "A says", min: 0, max: 6, step: 1, value: 2, fmt: function (x) { return says(0, x); } },
        { k: "b", label: "B says", min: 0, max: 6, step: 1, value: 3, fmt: function (x) { return says(1, x); } },
        { k: "c", label: "C says", min: 0, max: 6, step: 1, value: 1, fmt: function (x) { return says(2, x); } },
        { k: "h", label: "First guess", min: 0, max: 7, step: 1, value: 0, fmt: function (x) { return "A " + (x & 4 ? "true" : "false") + ", B " + (x & 2 ? "true" : "false") + ", C " + (x & 1 ? "true" : "false"); } },
      ],
      draw: function (g, v, s) {
        var w = [v.a, v.b, v.c], ctx = g.ctx, i, j, k, n;
        var stages = [[0, 0, 0]];
        for (k = 0; k < 6; k++) { var nx = jump(w, stages[stages.length - 1]); if (same(nx, stages[stages.length - 1])) break; stages.push(nx); }
        var fps = [], I;
        for (n = 0; n < 27; n++) { I = [n % 3, Math.floor(n / 3) % 3, Math.floor(n / 9)]; if (same(jump(w, I), I)) fps.push(I); }
        var lfp = stages[stages.length - 1], kind = [], grounded = 0, paradox = 0;
        for (i = 0; i < 3; i++) {
          var any = false; for (j = 0; j < fps.length; j++) if (fps[j][i] !== 0) any = true;
          kind.push(lfp[i] !== 0 ? "grounded" : any ? "ungrounded" : "paradoxical");
          grounded += lfp[i] !== 0 ? 1 : 0; paradox += kind[i] === "paradoxical" ? 1 : 0;
        }
        var rev = function (h, steps) { // classical revision: h is [1 or 2] x 3
          var out = [h], t; for (t = 0; t < steps; t++) out.push(jump(w, out[out.length - 1])); return out;
        };
        var verdict = [], fin = [[], [], []], unst = [false, false, false];
        for (n = 0; n < 8; n++) {
          var seq = rev([n & 4 ? 2 : 1, n & 2 ? 2 : 1, n & 1 ? 2 : 1], 12);
          for (i = 0; i < 3; i++) { for (j = 7; j <= 12; j++) if (seq[j][i] !== seq[6][i]) unst[i] = true; fin[i][seq[12][i]] = true; }
        }
        for (i = 0; i < 3; i++) verdict.push(unst[i] ? "unstable" : fin[i][1] && fin[i][2] ? "depends on guess" : fin[i][2] ? "stably true" : "stably false");
        var differ = [];
        for (i = 0; i < 3; i++) if (kind[i] === "paradoxical" && verdict[i].indexOf("stably") === 0) differ.push(NAME[i]);
        s.out = { fps: fps.length, grounded: grounded, paradox: paradox, differ: differ.length ? differ.join(", ") : "none", stages: stages.length - 1 };

        var draw = function (b, title, rows, right, ncol) {
          heading(ctx, b, title);
          var rh = (b.h - 34) / 3, cw = Math.min(34, (b.w - 24 - 112) / ncol), r, q;
          for (r = 0; r < 3; r++) {
            var y = b.y + 30 + r * rh;
            label(ctx, NAME[r] + ":  " + says(r, w[r]), b.x + 12, y + 9, { color: C.ink });
            for (q = 0; q < rows.length; q++) cell(ctx, b.x + 12 + q * cw, y + 22, cw, Math.min(26, rh - 34), rows[q][r]);
            label(ctx, right[r], b.x + 12 + ncol * cw + 6, y + 22 + Math.min(26, rh - 34) / 2, { color: C.idea });
          }
          for (q = 0; q < rows.length; q++) label(ctx, String(q), b.x + 12 + q * cw + (cw - 2) / 2, b.y + b.h - 8, { align: "center" });
        };
        draw(g[0].box, "Kripke: add only what is forced, stage by stage", stages.concat([lfp]).slice(0, Math.max(2, stages.length)), kind, 4);
        draw(g[1].box, "Revision: guess, then revise, stage by stage", rev([v.h & 4 ? 2 : 1, v.h & 2 ? 2 : 1, v.h & 1 ? 2 : 1], 8), verdict, 9);
      },
      readout: function (v, s) {
        return [["Kripke stages until nothing changes", String(s.out.stages)], ["fixed points", String(s.out.fps)], ["grounded sentences", String(s.out.grounded)],
          ["paradoxical", String(s.out.paradox)], ["paradoxical for Kripke but stable under revision", s.out.differ]];
      },
      note: "Exact. Kripke's values are strong Kleene (t, f, n); a sentence is grounded if the least fixed point gives it a value, paradoxical if none of the fixed points does, ungrounded otherwise. Revision's verdict is taken over all eight starting guesses.",
    });
  };

  // ---- Part 9: a two-world Kripke model against ten propositions ------------------------------------------
  W.kripkeforce = function (el) {
    var A = ["v", 0], B = ["v", 1], Cc = ["v", 2], BOT = ["bot"];
    var imp = function (a, b) { return ["imp", a, b]; }, and = function (a, b) { return ["and", a, b]; }, or = function (a, b) { return ["or", a, b]; };
    var neg = function (a) { return imp(a, BOT); };
    var F = [
      ["A → (B → A)", imp(A, imp(B, A)), "λx. λy. x"],
      ["(A → B → C) → (A → B) → A → C", imp(imp(A, imp(B, Cc)), imp(imp(A, B), imp(A, Cc))), "λx. λy. λz. x z (y z)"],
      ["A ∧ B → B ∧ A", imp(and(A, B), and(B, A)), "λp. ⟨snd p, fst p⟩"],
      ["(A ∧ B → C) → A → B → C", imp(imp(and(A, B), Cc), imp(A, imp(B, Cc))), "λf. λx. λy. f ⟨x, y⟩"],
      ["(A → C) → (B → C) → A ∨ B → C", imp(imp(A, Cc), imp(imp(B, Cc), imp(or(A, B), Cc))), "case analysis"],
      ["A → ¬¬A", imp(A, neg(neg(A))), "λx. λk. k x"],
      ["¬¬(A ∨ ¬A)", neg(neg(or(A, neg(A)))), "λk. k (inr (λa. k (inl a)))"],
      ["A ∨ ¬A", or(A, neg(A)), ""],
      ["((A → B) → A) → A", imp(imp(imp(A, B), A), A), ""],
      ["¬¬A → A", imp(neg(neg(A)), A), ""],
    ];
    var WHEN = ["never proved", "proved only later", "proved from the start"];
    var forces = function (w, t, at) { // worlds 0 <= 1; at[i] is the first world where atom i holds (2: never)
      if (t[0] === "v") return at[t[1]] <= w;
      if (t[0] === "bot") return false;
      if (t[0] === "and") return forces(w, t[1], at) && forces(w, t[2], at);
      if (t[0] === "or") return forces(w, t[1], at) || forces(w, t[2], at);
      for (var u = w; u <= 1; u++) if (forces(u, t[1], at) && !forces(u, t[2], at)) return false;
      return true;
    };
    QB.widget(el, {
      title: "Two stages of knowledge against ten propositions",
      sub: "A Kripke model with two worlds: what is proved now, and what is proved later. Choose when A, B and C get proved. The seven propositions that have a program are forced now in every setting; excluded middle, Peirce's law and double negation elimination hold as long as nothing is proved only later, and each fails in some setting where A is.",
      panels: 2, height: 320, weights: [0.9, 1.1],
      controls: [
        { k: "a", label: "A is", min: 0, max: 2, step: 1, value: 1, fmt: function (x) { return WHEN[x]; } },
        { k: "b", label: "B is", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return WHEN[x]; } },
        { k: "c", label: "C is", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return WHEN[x]; } },
        { k: "f", label: "Proposition shown on the left", min: 1, max: 10, step: 1, value: 8, fmt: function (x) { return F[x - 1][0]; } },
      ],
      draw: function (g, v, s) {
        var ctx = g.ctx, at = [2 - v.a, 2 - v.b, 2 - v.c], i, w, b = g[0].box, sel = F[v.f - 1];
        var now = [], bad = 0, n = 0;
        for (i = 0; i < 10; i++) { now.push(forces(0, F[i][1], at)); n += now[i] ? 1 : 0; if (F[i][2] && !now[i]) bad++; }
        s.out = { now: now[v.f - 1], later: forces(1, sel[1], at), n: n, bad: bad };
        heading(ctx, b, "The model: now, and later");
        var cy = b.y + b.h * 0.42, r = Math.min(52, b.w * 0.17), cx = [b.x + b.w * 0.27, b.x + b.w * 0.73];
        ctx.save(); ctx.strokeStyle = C.muted; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(cx[0] + r + 4, cy); ctx.lineTo(cx[1] - r - 8, cy); ctx.stroke();
        ctx.fillStyle = C.muted; ctx.beginPath(); ctx.moveTo(cx[1] - r - 2, cy); ctx.lineTo(cx[1] - r - 11, cy - 5); ctx.lineTo(cx[1] - r - 11, cy + 5); ctx.closePath(); ctx.fill(); ctx.restore();
        for (w = 0; w < 2; w++) {
          var known = []; for (i = 0; i < 3; i++) if (at[i] <= w) known.push("ABC"[i]);
          var ok = forces(w, sel[1], at);
          ctx.save(); ctx.fillStyle = C.bg; ctx.strokeStyle = ok ? C.gain : C.loss; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(cx[w], cy, r, 0, 6.2832); ctx.fill(); ctx.stroke(); ctx.restore();
          label(ctx, w ? "later" : "now", cx[w], cy - r - 12, { align: "center", color: C.ink, bold: true });
          label(ctx, "proved:", cx[w], cy - 11, { align: "center" });
          label(ctx, known.length ? known.join(", ") : "nothing", cx[w], cy + 8, { align: "center", color: C.idea, bold: true, size: 13 });
          label(ctx, ok ? "forced" : "not forced", cx[w], cy + r + 14, { align: "center", color: ok ? C.gain : C.loss, bold: true });
        }
        label(ctx, sel[0], b.x + b.w / 2, b.y + b.h - 34, { align: "center", color: C.ink, size: 12.5 });
        label(ctx, sel[2] ? "its program:  " + sel[2] : "no program proves it", b.x + b.w / 2, b.y + b.h - 15, { align: "center", color: sel[2] ? C.gain : C.loss });

        var t = g[1].box, rh = (t.h - 36) / 10, narrow = t.w < 470;
        heading(ctx, t, "Forced now? (green yes, red no)");
        for (i = 0; i < 10; i++) {
          var y = t.y + 30 + i * rh;
          if (i === v.f - 1) { ctx.fillStyle = "rgba(88,166,255,0.14)"; ctx.fillRect(t.x + 8, y, t.w - 16, rh); }
          ctx.fillStyle = now[i] ? C.gain : C.loss; ctx.beginPath(); ctx.arc(t.x + 20, y + rh / 2, 5, 0, 6.2832); ctx.fill();
          label(ctx, F[i][0], t.x + 32, y + rh / 2, { color: C.ink, size: narrow ? 11 : 11.5 });
          label(ctx, F[i][2] ? (narrow && F[i][2].length > 16 ? "has a program" : F[i][2]) : "no program", t.x + t.w - 12, y + rh / 2, { align: "right", color: F[i][2] ? C.muted : C.loss, size: 11 });
        }
      },
      readout: function (v, s) {
        return [["the proposition is forced now", s.out.now ? "yes" : "no"], ["forced later", s.out.later ? "yes" : "no"], ["of the ten, forced now", s.out.n + " of 10"],
          ["propositions with a program that fail", String(s.out.bad)]];
      },
      note: "Exact. A world forces 'if P then Q' when every world from it onward that forces P forces Q; so 'not A' needs A to stay unproved for ever. When no letter is proved only later the model is an ordinary truth table, and all ten hold.",
    });
  };

  // ---- Part 10: the angle sum of a triangle, measured on a curved surface -------------------------------
  W.triangleexcess = function (el) {
    var ARC = 206264.806; // arcseconds in a radian
    var excess = function (side, R) { // equilateral triangle of the given side on a sphere of radius R, in radians
      var a = Math.min(side / R, 2.09), c = Math.cos(a), A = Math.acos(Math.max(-1, Math.min(1, c / (1 + c))));
      return { A: A, e: Math.max(0, 3 * A - Math.PI), a: a };
    };
    var angle = function (sec) { return sec >= 3600 ? fmt(sec / 3600, 2) + "°" : sec >= 0.1 ? fmt(sec, 1) + "″" : fmt(sec, 3) + "″"; };
    QB.widget(el, {
      title: "Do a triangle's angles sum to two right angles?",
      sub: "An equilateral triangle drawn on a sphere, as a surveyor would measure it. Kant held the 180° sum to be known in advance. Make the triangle the size of Gauss's survey of Hanover and the excess is about 15 seconds of arc, at the edge of what an instrument can see; make it a continent wide, or sharpen the instrument, and the sum is plainly not 180°.",
      panels: 2, height: 300, weights: [0.8, 1.2],
      controls: [
        { k: "ls", label: "Side of the triangle", min: 1, max: 4, step: 0.01, value: 1.91, fmt: function (x) { return Math.round(Math.pow(10, x)) + " km"; } },
        { k: "R", label: "Radius of the sphere (Earth: 6371 km)", min: 5000, max: 20000, step: 1, value: 6371, fmt: function (x) { return x + " km"; } },
        { k: "lp", label: "Smallest angle the instrument can resolve", min: -1, max: 4, step: 0.05, value: 0, fmt: function (x) { return angle(Math.pow(10, x)); } },
      ],
      draw: function (g, v, s) {
        var ctx = g.ctx, side = Math.pow(10, v.ls), prec = Math.pow(10, v.lp), r = excess(side, v.R), i, k;
        s.out = { side: side, A: r.A * 180 / Math.PI, sec: r.e * ARC, seen: r.e * ARC >= prec };
        var b = g[0].box, cx = b.x + b.w / 2, cy = b.y + 28 + (b.h - 58) / 2, rad = Math.max(30, Math.min(b.w / 2 - 20, (b.h - 58) / 2));
        heading(ctx, b, "The triangle on its sphere");
        var grad = ctx.createRadialGradient(cx - rad * 0.3, cy - rad * 0.3, rad * 0.1, cx, cy, rad);
        grad.addColorStop(0, "#22304a"); grad.addColorStop(1, C.bg);
        ctx.save(); ctx.fillStyle = grad; ctx.strokeStyle = "#3a475c"; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(cx, cy, rad, 0, 6.2832); ctx.fill(); ctx.stroke();
        var rho = Math.asin(Math.min(1, Math.sin(r.a / 2) / 0.8660254)), V = [];
        for (i = 0; i < 3; i++) { var az = Math.PI / 2 + i * 2.0943951; V.push([Math.sin(rho) * Math.cos(az), Math.sin(rho) * Math.sin(az), Math.cos(rho)]); }
        if (Math.sin(rho) * rad < 3) {
          ctx.fillStyle = C.idea; ctx.beginPath(); ctx.arc(cx, cy, 2.5, 0, 6.2832); ctx.fill();
          var mx = cx + rad * 0.42, my = cy - rad * 0.38, ms = Math.min(22, rad * 0.3); // the same triangle, magnified
          ctx.strokeStyle = C.muted; ctx.lineWidth = 1; ctx.setLineDash([3, 3]); ctx.beginPath(); ctx.moveTo(cx + 3, cy - 3); ctx.lineTo(mx - ms * 0.7, my + ms * 0.6); ctx.stroke(); ctx.setLineDash([]);
          ctx.strokeStyle = C.idea; ctx.fillStyle = "rgba(247,209,84,0.18)"; ctx.lineWidth = 2; ctx.beginPath();
          ctx.moveTo(mx, my - ms); ctx.lineTo(mx - ms * 0.866, my + ms * 0.5); ctx.lineTo(mx + ms * 0.866, my + ms * 0.5); ctx.closePath(); ctx.fill(); ctx.stroke();
        } else {
          ctx.strokeStyle = C.idea; ctx.fillStyle = "rgba(247,209,84,0.18)"; ctx.lineWidth = 2; ctx.beginPath();
          for (i = 0; i < 3; i++) {
            var p = V[i], q = V[(i + 1) % 3], dot = Math.max(-1, Math.min(1, p[0] * q[0] + p[1] * q[1] + p[2] * q[2])), om = Math.acos(dot), so = Math.sin(om) || 1;
            for (k = 0; k <= 24; k++) {
              var t = k / 24, wa = Math.sin((1 - t) * om) / so, wb = Math.sin(t * om) / so, X = cx + rad * (wa * p[0] + wb * q[0]), Y = cy - rad * (wa * p[1] + wb * q[1]);
              if (i === 0 && k === 0) ctx.moveTo(X, Y); else ctx.lineTo(X, Y);
            }
          }
          ctx.closePath(); ctx.fill(); ctx.stroke();
        }
        ctx.restore();
        label(ctx, Math.sin(rho) * rad < 3 ? "to scale it is the gold dot; each angle " + fmt(s.out.A, 4) + "°" : "each angle " + fmt(s.out.A, 2) + "°", cx, b.y + b.h - 14, { align: "center", color: C.idea });

        var xs = QB.linspace(1, 4, 61).map(function (x) { return Math.pow(10, x); });
        var ys = xs.map(function (x) { return Math.max(1e-3, excess(x, v.R).e * ARC); });
        var ax = g[1].axes({ x: [10, 10000], y: [1e-3, 1e7], logx: true, logy: true, title: "Excess over 180° against the triangle's side", xlabel: "side (km)",
          yticks: [1e-2, 1, 100, 3600, 360000], yfmt: function (y) { return y >= 3600 ? Math.round(y / 3600) + "°" : y + "″"; },
          xticks: [10, 100, 1000, 10000], xfmt: function (x) { return x >= 1000 ? x / 1000 + "k" : String(x); } });
        ax.area([10, 10000], [prec, prec], 1e-3, { color: C.loss, alpha: 0.12 });
        ax.hline(prec, { color: C.loss });
        ax.line(xs, ys, { color: C.spot, width: 2.2 });
        ax.dots([side], [Math.max(1e-3, s.out.sec)], { color: C.idea, r: 6 });
        ax.legend([["excess of the angle sum", C.spot], ["below this the instrument sees 180°", C.loss], ["your triangle", C.idea]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["side", Math.round(s.out.side) + " km"], ["angle sum", fmt(3 * s.out.A, 4) + "°"], ["excess over 180°", angle(s.out.sec)], ["the instrument can tell", s.out.seen ? "yes" : "no"]];
      },
      note: "Exact spherical trigonometry: the excess equals the triangle's area divided by the radius squared. Gauss's triangle (69, 85 and 106 km) had an excess of 14.9″. This is the earth's surface, not space; that physical space is curved was shown by starlight bending at the sun in 1919.",
    });
  };

  // ---- Part 11: Williamson's unmarked clock, with a margin for error --------------------------------------
  W.marginclock = function (el) {
    var N = 31, ROWS = ["p", "Kp", "KKp", "KKKp"];
    QB.widget(el, {
      title: "The unmarked clock: knowing, and knowing that you know",
      sub: "A clock face with 31 unnumbered marks; you can tell where the hand points only to within a margin. Let p be 'the hand is at or below the boundary'. You know p only if p holds at every mark you cannot rule out (gold). Put the hand one mark inside the boundary: you know p but do not know that you know it. Set the margin to zero and the gap closes.",
      panels: 2, height: 300, weights: [0.8, 1.2],
      controls: [
        { k: "h", label: "Where the hand really points", min: 0, max: 30, step: 1, value: 19, fmt: function (x) { return "mark " + x; } },
        { k: "m", label: "Margin for error", min: 0, max: 4, step: 1, value: 1, fmt: function (x) { return x === 0 ? "none" : x + (x === 1 ? " mark" : " marks") + " either way"; } },
        { k: "c", label: "p: the hand is at or below", min: 5, max: 25, step: 1, value: 20, fmt: function (x) { return "mark " + x; } },
      ],
      draw: function (g, v, s) {
        var ctx = g.ctx, i, k, j, lev = [[]];
        for (i = 0; i < N; i++) lev[0].push(i <= v.c);
        for (k = 1; k < 4; k++) {
          lev.push([]);
          for (i = 0; i < N; i++) { var ok = true; for (j = Math.max(0, i - v.m); j <= Math.min(N - 1, i + v.m); j++) if (!lev[k - 1][j]) ok = false; lev[k].push(ok); }
        }
        var gap = 0; for (i = 0; i < N; i++) if (lev[1][i] && !lev[2][i]) gap++;
        s.out = { at: [lev[0][v.h], lev[1][v.h], lev[2][v.h], lev[3][v.h]], gap: gap };

        var b = g[0].box, cx = b.x + b.w / 2, cy = b.y + 26 + (b.h - 62) / 2, R = Math.max(40, Math.min(b.w / 2 - 34, (b.h - 62) / 2 - 22));
        var ang = function (mark) { return -Math.PI / 2 + mark * 2 * Math.PI / N; };
        heading(ctx, b, "The clock");
        ctx.save(); ctx.lineCap = "butt";
        ctx.strokeStyle = C.gain; ctx.globalAlpha = 0.55; ctx.lineWidth = 9; ctx.beginPath(); ctx.arc(cx, cy, R, ang(-0.5), ang(v.c + 0.5)); ctx.stroke();
        ctx.strokeStyle = C.idea; ctx.globalAlpha = 0.9; ctx.lineWidth = 7; ctx.beginPath(); ctx.arc(cx, cy, R - 12, ang(Math.max(0, v.h - v.m) - 0.5), ang(Math.min(N - 1, v.h + v.m) + 0.5)); ctx.stroke();
        ctx.globalAlpha = 1; ctx.strokeStyle = C.muted; ctx.lineWidth = 1.5;
        for (i = 0; i < N; i++) { var a = ang(i); ctx.beginPath(); ctx.moveTo(cx + (R + 7) * Math.cos(a), cy + (R + 7) * Math.sin(a)); ctx.lineTo(cx + (R + 13) * Math.cos(a), cy + (R + 13) * Math.sin(a)); ctx.stroke(); }
        ctx.strokeStyle = C.ink; ctx.lineWidth = 2.5; ctx.lineCap = "round"; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + (R - 20) * Math.cos(ang(v.h)), cy + (R - 20) * Math.sin(ang(v.h))); ctx.stroke();
        ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(cx, cy, 3.5, 0, 6.2832); ctx.fill(); ctx.restore();
        label(ctx, "0", cx + (R + 24) * Math.cos(ang(0)), cy + (R + 24) * Math.sin(ang(0)), { align: "center" });
        label(ctx, String(v.c), cx + (R + 24) * Math.cos(ang(v.c)), cy + (R + 24) * Math.sin(ang(v.c)), { align: "center", color: C.gain });
        label(ctx, "green: p is true", b.x + 12, b.y + b.h - 22, { color: C.gain });
        label(ctx, "gold: cannot be ruled out", b.x + 12, b.y + b.h - 8, { color: C.idea });

        var t = g[1].box, left = t.x + 52, cw = (t.w - 52 - 14) / N, rh = Math.min(38, (t.h - 64) / 4), top = t.y + 34;
        heading(ctx, t, "Where each holds, mark by mark");
        for (k = 0; k < 4; k++) {
          label(ctx, ROWS[k], left - 8, top + k * (rh + 6) + rh / 2, { align: "right", color: C.ink, bold: true });
          for (i = 0; i < N; i++) { ctx.fillStyle = lev[k][i] ? C.gain : C.line; ctx.globalAlpha = lev[k][i] ? 0.85 : 1; ctx.fillRect(left + i * cw, top + k * (rh + 6), Math.max(1, cw - 1), rh); }
          ctx.globalAlpha = 1;
        }
        ctx.save(); ctx.strokeStyle = C.ink; ctx.lineWidth = 1.5; ctx.strokeRect(left + v.h * cw - 1, top - 3, cw + 1, 4 * (rh + 6)); ctx.restore();
        for (i = 0; i <= 30; i += 10) label(ctx, String(i), left + i * cw + cw / 2, top + 4 * (rh + 6) + 8, { align: "center" });
        label(ctx, "the hand", Math.max(left + 24, Math.min(t.x + t.w - 30, left + v.h * cw + cw / 2)), top + 4 * (rh + 6) + 22, { align: "center", color: C.ink });
      },
      readout: function (v, s) {
        var yn = function (x) { return x ? "yes" : "no"; }, a = s.out.at;
        return [["p is true", yn(a[0])], ["you know p", yn(a[1])], ["you know that you know", yn(a[2])], ["and know that again", yn(a[3])],
          ["marks where you know without knowing that you know", String(s.out.gap)]];
      },
      note: "Exact. K holds at a mark when what it is applied to holds at every mark within the margin (the marks do not wrap past 0 or 30). Each K strips one margin from the edge, so the KK principle fails just inside any boundary unless the margin is zero.",
    });
  };

  // ---- Part 12: the muddy children, round by round --------------------------------------------------------
  W.muddyrounds = function (el) {
    var choose = function (n, j) { var c = 1, i; for (i = 1; i <= j; i++) c = c * (n - j + i) / i; return Math.round(c); };
    QB.widget(el, {
      title: "The muddy children, round by round",
      sub: "Each child sees every forehead but its own. Each round the father asks 'do you know whether you are muddy?' and all answer at once. Right: the worlds nobody has ruled out, by how many children are muddy in them. With the father's announcement one layer falls each round until the muddy children know; switch it off and nothing ever changes, though every child could already see mud.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Children", min: 2, max: 8, step: 1, value: 5, fmt: function (x) { return String(x); } },
        { k: "k", label: "Muddy children", min: 1, max: 8, step: 1, value: 3, fmt: function (x) { return String(x); } },
        { k: "r", label: "Round", min: 1, max: 9, step: 1, value: 1, fmt: function (x) { return "round " + x; } },
        { k: "f", label: "Father first says 'someone is muddy'", min: 0, max: 1, step: 1, value: 1, fmt: function (x) { return x ? "yes" : "no"; } },
      ],
      draw: function (g, v, s) {
        var ctx = g.ctx, n = v.n, k = Math.min(v.k, n), r = v.r, j, i;
        // layer j (worlds with j muddy children) is still possible at the start of round r
        var done = v.f === 1 && r > k; // the muddy children answered yes in round k: the world is known to all
        var left = [], total = 0, top = 0;
        for (j = 0; j <= n; j++) {
          var c = choose(n, j), alive = v.f === 0 ? c : (done ? (j === k ? 1 : 0) : (j >= Math.min(r, k) ? c : 0));
          left.push(alive); total += alive; top = Math.max(top, c);
        }
        var muddyKnow = v.f === 1 && r >= k, cleanKnow = v.f === 1 && r >= k + 1;
        s.out = { n: n, k: k, total: total, all: Math.pow(2, n), muddyKnow: muddyKnow, cleanKnow: cleanKnow, clean: n - k };

        var b = g[0].box, per = n <= 4 ? n : Math.ceil(n / 2), rowsN = Math.ceil(n / per), cw = (b.w - 24) / per, chh = (b.h - 40) / rowsN, rad = Math.max(10, Math.min(24, cw / 2 - 8, chh / 2 - 22));
        heading(ctx, b, "Round " + r + ": who can answer?");
        for (i = 0; i < n; i++) {
          var cx = b.x + 12 + (i % per + 0.5) * cw, cy = b.y + 36 + Math.floor(i / per) * chh + rad + 4, muddy = i < k, knows = muddy ? muddyKnow : cleanKnow;
          ctx.save(); ctx.fillStyle = "#e9c9a3"; ctx.beginPath(); ctx.arc(cx, cy, rad, 0, 6.2832); ctx.fill();
          if (muddy) { ctx.fillStyle = "#7a4a21"; ctx.beginPath(); ctx.ellipse(cx, cy - rad * 0.45, rad * 0.55, rad * 0.26, 0, 0, 6.2832); ctx.fill(); }
          ctx.fillStyle = C.bg; ctx.beginPath(); ctx.arc(cx - rad * 0.35, cy + rad * 0.1, 2, 0, 6.2832); ctx.arc(cx + rad * 0.35, cy + rad * 0.1, 2, 0, 6.2832); ctx.fill();
          ctx.strokeStyle = knows ? C.gain : C.muted; ctx.lineWidth = knows ? 3 : 1.5; ctx.beginPath(); ctx.arc(cx, cy, rad + 3, 0, 6.2832); ctx.stroke(); ctx.restore();
          label(ctx, knows ? (muddy ? "I am muddy" : "I am clean") : "I don't know", cx, cy + rad + 15, { align: "center", color: knows ? C.gain : C.muted, size: 11 });
        }

        var xs = [], ghost = [];
        for (j = 0; j <= n; j++) { xs.push(j); ghost.push(choose(n, j)); }
        var ax = g[1].axes({ x: [-0.6, n + 0.6], y: [0, top * 1.75], title: "Worlds not yet ruled out", xlabel: "muddy children in the world", xticks: xs });
        ax.bars(xs, ghost, 0.8, { color: C.line, alpha: 1 });
        ax.bars(xs, left, 0.8, { color: function (q) { return q === k ? C.idea : C.spot; } });
        ax.legend([["still possible", C.spot], ["the layer of the real world", C.idea], ["ruled out", C.line]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["worlds still possible", o.total + " of " + o.all], ["the " + o.k + " muddy " + (o.k === 1 ? "child knows" : "children know"), o.muddyKnow ? "yes" : "no"],
          ["the " + o.clean + " clean " + (o.clean === 1 ? "child knows" : "children know"), o.clean === 0 ? "none to ask" : o.cleanKnow ? "yes" : "no"],
          ["muddy children first know in", v.f ? "round " + o.k : "no round"]];
      },
      note: "Exact. The counts are binomial coefficients: the father's sentence removes the world with no mud, each 'nobody knows' removes the next layer, and once the muddy children answer everyone knows the real world. With two or more muddy children the father says nothing any child did not know; what he adds is common knowledge.",
    });
  };
})();
