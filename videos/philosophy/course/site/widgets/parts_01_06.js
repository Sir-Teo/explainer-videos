// Interactives for the prologue and Act I, The Machinery of Reason (Parts 1-6).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;
  function font(c, size, bold) { c.font = (bold ? "600 " : "") + size + "px system-ui, sans-serif"; }

  // ---- Part 1: a syllogistic mood against the 256 arrangements of the Venn regions ---------------------------
  var KIND = "AEIO", FIG = [[[1, 2], [0, 1]], [[2, 1], [0, 1]], [[1, 2], [1, 0]], [[2, 1], [1, 0]]]; // terms S=0, M=1, P=2
  var MOODNAMES = {
    "1AAA": "Barbara", "1EAE": "Celarent", "1AII": "Darii", "1EIO": "Ferio", "1AAI": "Barbari", "1EAO": "Celaront",
    "2EAE": "Cesare", "2AEE": "Camestres", "2EIO": "Festino", "2AOO": "Baroco", "2EAO": "Cesaro", "2AEO": "Camestros",
    "3AAI": "Darapti", "3IAI": "Disamis", "3AII": "Datisi", "3EAO": "Felapton", "3OAO": "Bocardo", "3EIO": "Ferison",
    "4AAI": "Bramantip", "4AEE": "Camenes", "4IAI": "Dimaris", "4EAO": "Fesapo", "4EIO": "Fresison", "4AEO": "Camenos",
  };
  // region r (0..7): bit 0 = in S, bit 1 = in M, bit 2 = in P; a model is a bitmask of inhabited regions
  function sentence(kind, x, y, model) {
    var xy = false, xnoty = false;
    for (var r = 0; r < 8; r++) if (model >> r & 1) { if (r >> x & 1) { if (r >> y & 1) xy = true; else xnoty = true; } }
    return kind === 0 ? !xnoty : kind === 1 ? !xy : kind === 2 ? xy : xnoty;
  }
  function inhabited(model) {
    var t = 0; for (var r = 0; r < 8; r++) if (model >> r & 1) t |= r;
    return t === 7;
  }
  function bits(m) { var n = 0; while (m) { n += m & 1; m >>= 1; } return n; }
  function checkMood(f, a, b, c, imp) { // -> {prem: models where both premises hold, counter: [models], best: smallest countermodel or -1}
    var t = FIG[f], prem = 0, counter = 0, best = -1;
    for (var m = 0; m < 256; m++) {
      if (imp && !inhabited(m)) continue;
      if (sentence(a, t[0][0], t[0][1], m) && sentence(b, t[1][0], t[1][1], m)) {
        prem++;
        if (!sentence(c, 0, 2, m)) { counter++; if (best < 0 || bits(m) < bits(best)) best = m; }
      }
    }
    return { prem: prem, counter: counter, best: best };
  }
  var moodGrid = null;
  function allMoods() { // status of each of the 256 moods: 2 valid, 1 valid with inhabited terms, 0 invalid
    if (moodGrid) return moodGrid;
    moodGrid = [];
    for (var f = 0; f < 4; f++) for (var k = 0; k < 64; k++) {
      var a = k >> 4, b = k >> 2 & 3, c = k & 3;
      moodGrid.push(checkMood(f, a, b, c, false).counter === 0 ? 2 : checkMood(f, a, b, c, true).counter === 0 ? 1 : 0);
    }
    return moodGrid;
  }
  var WORDS = [["All ", " are "], ["No ", " are "], ["Some ", " are "], ["Some ", " are not "]], TERM = ["S", "M", "P"];
  function say(kind, x, y) { return WORDS[kind][0] + TERM[x] + WORDS[kind][1] + TERM[y]; }

  W.vennmoods = function (el) {
    QB.widget(el, {
      title: "One mood against every arrangement of the regions",
      sub: "Choose a figure and the three sentences. The machine tries all 256 ways the eight Venn regions can be inhabited or empty and, if the mood is invalid, shows the smallest arrangement that refutes it. Set figure 3, A, A, I (Darapti, the unicorn argument) and switch the last slider: the empty world refutes it until every term must be inhabited.",
      panels: 2, height: 310,
      controls: [
        { k: "fig", label: "Figure", min: 1, max: 4, step: 1, value: 3, fmt: function (x) { return String(x); } },
        { k: "a", label: "Major premise", min: 0, max: 3, step: 1, value: 0, fmt: function (x) { return KIND[x]; } },
        { k: "b", label: "Minor premise", min: 0, max: 3, step: 1, value: 0, fmt: function (x) { return KIND[x]; } },
        { k: "c", label: "Conclusion", min: 0, max: 3, step: 1, value: 2, fmt: function (x) { return KIND[x]; } },
        { k: "imp", label: "Every term inhabited", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "yes" : "no"; } },
      ],
      draw: function (g, v, s) {
        var f = v.fig - 1, t = FIG[f], res = checkMood(f, v.a, v.b, v.c, v.imp === 1), c = g.ctx, bx = g[0].box, i;
        s.res = res; s.name = MOODNAMES[v.fig + KIND[v.a] + KIND[v.b] + KIND[v.c]] || "";
        // left: the argument and the Venn diagram
        c.save();
        font(c, 12.5, true); c.fillStyle = C.ink; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText(res.counter ? "Invalid: a refuting arrangement" : "Valid: no arrangement refutes it", bx.x + 12, bx.y + 6);
        font(c, 12); c.fillStyle = C.muted;
        c.fillText(say(v.a, t[0][0], t[0][1]) + ".  " + say(v.b, t[1][0], t[1][1]) + ".", bx.x + 12, bx.y + 26);
        c.fillStyle = res.counter ? C.loss : C.gain; c.fillText("So: " + say(v.c, 0, 2) + ".", bx.x + 12, bx.y + 43);
        var R = Math.min(bx.w / 4.3, (bx.h - 78) / 3.5), cx = bx.x + bx.w / 2, cy = bx.y + 66 + 1.62 * R;
        var cen = [[-0.5, -0.3], [0, 0.55], [0.5, -0.3]], col = [C.spot, C.q, C.implied];
        for (i = 0; i < 3; i++) {
          c.strokeStyle = col[i]; c.lineWidth = 2; c.beginPath(); c.arc(cx + cen[i][0] * R, cy + cen[i][1] * R, R, 0, 6.2832); c.stroke();
        }
        font(c, 13, true); c.textAlign = "center"; c.textBaseline = "middle";
        c.fillStyle = col[0]; c.fillText("S", cx - 1.55 * R, cy - 1.0 * R);
        c.fillStyle = col[2]; c.fillText("P", cx + 1.55 * R, cy - 1.0 * R);
        c.fillStyle = col[1]; c.fillText("M", cx + 0.95 * R, cy + 1.4 * R);
        // a mark at each region: index = bit0 S, bit1 M, bit2 P
        var at = [[-1.75, 1.2], [-0.95, -0.55], [0, 1.05], [-0.62, 0.35], [0.95, -0.55], [0, -0.75], [0.62, 0.35], [0, -0.05]];
        var show = res.counter ? res.best : -1;
        for (i = 0; i < 8; i++) {
          var X = cx + at[i][0] * R, Y = cy + at[i][1] * R;
          if (show >= 0 && (show >> i & 1)) { c.fillStyle = C.idea; c.beginPath(); c.arc(X, Y, 6, 0, 6.2832); c.fill(); }
          else if (show >= 0) { c.strokeStyle = C.muted; c.lineWidth = 1.2; c.beginPath(); c.arc(X, Y, 4, 0, 6.2832); c.stroke(); }
        }
        if (show >= 0) {
          font(c, 11); c.fillStyle = C.muted; c.textAlign = "left";
          c.fillText("outside", cx - 1.75 * R + 9, cy + 1.2 * R);
        }
        c.restore();
        // right: all 256 moods
        var grid = allMoods(), b2 = g[1].box, x0 = b2.x + 30, y0 = b2.y + 30, cw = (b2.w - 44) / 16, ch = Math.min(13, (b2.h - 96) / 16);
        c.save();
        font(c, 12.5, true); c.fillStyle = C.ink; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("All 256 moods (a row of 16 per major and minor)", b2.x + 12, b2.y + 6);
        for (var ff = 0; ff < 4; ff++) for (var k = 0; k < 64; k++) {
          var st = grid[ff * 64 + k], gx = x0 + (k & 15) * cw, gy = y0 + (ff * 4 + (k >> 4)) * ch + ff * 5;
          c.fillStyle = st === 2 ? C.idea : st === 1 ? C.spot : C.line;
          c.fillRect(gx, gy, cw - 1.5, ch - 1.5);
          if (ff === f && k === (v.a << 4 | v.b << 2 | v.c)) { c.strokeStyle = C.ink; c.lineWidth = 2; c.strokeRect(gx - 1.5, gy - 1.5, cw + 1.5, ch + 1.5); }
        }
        font(c, 11); c.fillStyle = C.muted; c.textAlign = "right"; c.textBaseline = "middle";
        for (ff = 0; ff < 4; ff++) c.fillText("fig " + (ff + 1), x0 - 4, y0 + ff * (4 * ch + 5) + 2 * ch);
        var ly = y0 + 16 * ch + 26; c.textAlign = "left";
        [[C.idea, "valid in every arrangement (15)"], [C.spot, "valid only if every term is inhabited (9)"], [C.line, "invalid (232); the white frame is your mood"]].forEach(function (it, j) {
          c.fillStyle = it[0]; c.fillRect(b2.x + 12, ly + j * 15 - 5, 10, 10); c.fillStyle = C.muted; c.fillText(it[1], b2.x + 28, ly + j * 15);
        });
        c.restore();
      },
      readout: function (v, s) {
        return [["mood", "figure " + v.fig + " " + KIND[v.a] + KIND[v.b] + KIND[v.c] + (s.name ? " (" + s.name + ")" : "")],
          ["arrangements where both premises hold", String(s.res.prem)], ["of which refute the conclusion", String(s.res.counter)],
          ["verdict", s.res.counter ? "invalid" : "valid"]];
      },
      note: "S is the subject of the conclusion, P its predicate, M the middle term. Gold dots are inhabited regions of the refuting arrangement, hollow circles are empty ones. 'All S are P' is read as 'no S is outside P', so it is true when there are no S at all.",
    });
  };

  // ---- Part 2: random 3-SAT, one dial: clauses per atom -------------------------------------------------------
  function ksat(r, n, m) { // m clauses of three distinct atoms, random signs; literals are +-(1..n)
    var out = [];
    for (var i = 0; i < m; i++) {
      var a = 1 + Math.floor(r() * n), b = a, c = a;
      while (b === a) b = 1 + Math.floor(r() * n);
      while (c === a || c === b) c = 1 + Math.floor(r() * n);
      out.push([r() < 0.5 ? a : -a, r() < 0.5 ? b : -b, r() < 0.5 ? c : -c]);
    }
    return out;
  }
  function dpllRun(clauses, cap) { // propagate, branch on the lowest open atom (true first), back up; counts decisions
    var decisions = 0, conflicts = 0;
    function simp(cl, lit) {
      var out = [];
      for (var i = 0; i < cl.length; i++) {
        var c = cl[i], keep = true, d = null, j;
        for (j = 0; j < c.length; j++) { if (c[j] === lit) { keep = false; break; } }
        if (!keep) continue;
        for (j = 0; j < c.length; j++) if (c[j] === -lit) { d = c.filter(function (x) { return x !== -lit; }); break; }
        out.push(d || c);
      }
      return out;
    }
    function go(cl) {
      for (;;) {
        var unit = 0, i;
        for (i = 0; i < cl.length; i++) { if (cl[i].length === 0) { conflicts++; return false; } if (!unit && cl[i].length === 1) unit = cl[i][0]; }
        if (!unit) break;
        cl = simp(cl, unit);
      }
      if (!cl.length) return true;
      if (decisions > cap) return false;
      var v = 1e9;
      for (i = 0; i < cl.length; i++) for (var j = 0; j < cl[i].length; j++) v = Math.min(v, Math.abs(cl[i][j]));
      decisions++; if (go(simp(cl, v))) return true;
      decisions++; return go(simp(cl, -v));
    }
    var sat = go(clauses);
    return { sat: sat, decisions: decisions, conflicts: conflicts };
  }
  function median(xs) { var s = xs.slice().sort(function (a, b) { return a - b; }), k = s.length >> 1; return s.length % 2 ? s[k] : (s[k - 1] + s[k]) / 2; }

  W.satdial = function (el) {
    var RATIOS = QB.linspace(1, 8, 29), PER = 24;
    QB.widget(el, {
      title: "The dial: clauses per atom in random 3-SAT",
      sub: "Each point is 24 random formulas of three-literal clauses, solved in your browser by DPLL (propagate, branch, back up). Turn the dial from few clauses per atom to many: the share of satisfiable formulas falls from one to zero, and the search works hardest in between. Add atoms and the fall gets steeper.",
      panels: 2, height: 300,
      controls: [
        { k: "ratio", label: "Clauses per atom", min: 1, max: 8, step: 0.25, value: 4.25, fmt: function (x) { return x.toFixed(2); } },
        { k: "n", label: "Atoms n", min: 8, max: 28, step: 4, value: 20, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New formulas", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var key = v.n + ":" + s.seed, i, k;
        if (s.key !== key) { // the two curves depend only on n and the seed
          s.key = key; s.share = []; s.work = [];
          var r = QB.rng(977 * s.seed + v.n);
          for (i = 0; i < RATIOS.length; i++) {
            var nsat = 0, dec = [];
            for (k = 0; k < PER; k++) { var out = dpllRun(ksat(r, v.n, Math.round(RATIOS[i] * v.n)), 20000); nsat += out.sat ? 1 : 0; dec.push(out.decisions); }
            s.share.push(nsat / PER); s.work.push(median(dec));
          }
        }
        var idx = Math.round((v.ratio - 1) / 0.25), top = Math.max(4, 1.15 * Math.max.apply(null, s.work));
        s.at = [s.share[idx], s.work[idx], RATIOS[s.work.indexOf(Math.max.apply(null, s.work))]];
        var a = g[0].axes({ x: [1, 8], y: [0, 1.05], title: "Share of formulas that are satisfiable", xlabel: "clauses per atom" });
        a.vline(4.27, { color: C.muted }); a.text(4.27, 0.97, "4.27", { color: C.muted, dx: 5 });
        a.line(RATIOS, s.share, { color: C.idea, width: 2.2 });
        a.vline(v.ratio, { color: C.ink, dash: [], width: 1.2 }); a.dots([v.ratio], [s.at[0]], { color: C.idea, r: 5 });
        var b = g[1].axes({ x: [1, 8], y: [0, top], title: "DPLL's work: median decisions", xlabel: "clauses per atom" });
        b.vline(4.27, { color: C.muted });
        b.line(RATIOS, s.work, { color: C.spot, width: 2.2 });
        b.vline(v.ratio, { color: C.ink, dash: [], width: 1.2 }); b.dots([v.ratio], [s.at[1]], { color: C.spot, r: 5 });
        b.legend([["median decisions of 24 runs", C.spot], ["the threshold for large n", C.muted]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["satisfiable at this ratio", QB.pct(s.at[0], 0)], ["median decisions", fmt(s.at[1], 0)], ["work peaks at ratio", fmt(s.at[2], 2)],
          ["truth-table rows", String(Math.pow(2, v.n))]];
      },
      note: "Simulated formulas. The dashed line marks 4.27 clauses per atom, where the fall happens for large n; for formulas this small the fall is gradual and the peak of the work sits a little to its right, as in the film.",
    });
  };

  // ---- Part 3: the order of two quantifiers, on a random relation --------------------------------------------
  W.quantorder = function (el) {
    QB.widget(el, {
      title: "Everyone loves someone, or someone is loved by everyone?",
      sub: "A relation L on n people: a gold cell in row x, column y means x loves y. 'For all x there is y' needs a gold cell in every row; 'there is y for all x' needs one full column. Lower the density until a row goes empty, raise it until a column fills: the second sentence never holds without the first.",
      panels: 2, height: 310,
      controls: [
        { k: "n", label: "People n", min: 2, max: 8, step: 1, value: 5, fmt: function (x) { return String(x); } },
        { k: "p", label: "Density of L", min: 0.05, max: 0.95, step: 0.01, value: 0.45, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New relation", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var n = v.n, r = QB.rng(131 * s.seed + 7), u = [], i, j, c = g.ctx, bx = g[0].box;
        for (i = 0; i < 64; i++) u.push(r()); // one uniform per cell, so raising the density only adds cells
        var L = function (x, y) { return u[8 * x + y] < v.p; };
        var rowOk = [], colFull = [], ae = true, ea = false;
        for (i = 0; i < n; i++) { rowOk[i] = false; for (j = 0; j < n; j++) if (L(i, j)) rowOk[i] = true; if (!rowOk[i]) ae = false; }
        for (j = 0; j < n; j++) { colFull[j] = true; for (i = 0; i < n; i++) if (!L(i, j)) colFull[j] = false; if (colFull[j]) ea = true; }
        var pa = Math.pow(1 - Math.pow(1 - v.p, n), n), pe = 1 - Math.pow(1 - Math.pow(v.p, n), n);
        s.out = [ae, ea, pa, pe];
        // left: the relation as a grid
        c.save();
        font(c, 12.5, true); c.fillStyle = C.ink; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("The relation L(x, y): row x loves column y", bx.x + 12, bx.y + 6);
        var size = Math.min(bx.w - 150, bx.h - 62), cell = size / n, x0 = bx.x + 40, y0 = bx.y + 46;
        font(c, 11); c.textAlign = "center"; c.textBaseline = "middle";
        for (i = 0; i < n; i++) {
          c.fillStyle = colFull[i] ? C.gain : C.muted; c.fillText("y" + (i + 1), x0 + (i + 0.5) * cell, y0 - 9);
          c.fillStyle = rowOk[i] ? C.muted : C.loss; c.fillText("x" + (i + 1), x0 - 14, y0 + (i + 0.5) * cell);
          for (j = 0; j < n; j++) {
            c.fillStyle = L(i, j) ? (colFull[j] ? C.gain : C.idea) : (rowOk[i] ? C.line : "rgba(248,113,113,0.28)");
            c.fillRect(x0 + j * cell + 1, y0 + i * cell + 1, cell - 2, cell - 2);
          }
        }
        var lx = x0 + size + 12, ly = y0 + 8; c.textAlign = "left";
        [[C.idea, "x loves y"], [C.gain, "a full column"], ["rgba(248,113,113,0.5)", "an empty row"]].forEach(function (it, k) {
          c.fillStyle = it[0]; c.fillRect(lx, ly + 17 * k - 5, 10, 10); c.fillStyle = C.muted; c.fillText(it[1], lx + 15, ly + 17 * k);
        });
        font(c, 12, true);
        c.fillStyle = ae ? C.gain : C.loss; c.fillText("∀x ∃y L: " + (ae ? "true" : "false"), lx, ly + 66);
        c.fillStyle = ea ? C.gain : C.loss; c.fillText("∃y ∀x L: " + (ea ? "true" : "false"), lx, ly + 84);
        c.restore();
        // right: how likely each sentence is at this density
        var ps = QB.linspace(0.01, 0.99, 99);
        var a = g[1].axes({ x: [0, 1], y: [0, 1.05], title: "Chance each sentence holds, n = " + n, xlabel: "density of L" });
        a.line(ps, ps.map(function (q) { return Math.pow(1 - Math.pow(1 - q, n), n); }), { color: C.spot, width: 2.2 });
        a.line(ps, ps.map(function (q) { return 1 - Math.pow(1 - Math.pow(q, n), n); }), { color: C.implied, width: 2.2 });
        a.vline(v.p, { color: C.ink, dash: [], width: 1.2 });
        a.dots([v.p, v.p], [pa, pe], { color: function (k) { return k ? C.implied : C.spot; }, r: 5 });
        a.legend([["∀x ∃y L(x, y)", C.spot], ["∃y ∀x L(x, y)", C.implied]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["everyone loves someone", s.out[0] ? "true" : "false"], ["someone is loved by everyone", s.out[1] ? "true" : "false"],
          ["chance of the first", QB.pct(s.out[2], 1)], ["chance of the second", QB.pct(s.out[3], 1)]];
      },
      note: "Simulated relation: each pair is in L independently with the chosen density. The curves are exact: (1 − (1 − p)ⁿ)ⁿ and 1 − (1 − pⁿ)ⁿ. The orange curve lies below the blue one everywhere, because a full column puts a gold cell in every row.",
    });
  };

  // ---- Part 4: a frame decides which modal axioms are valid on it --------------------------------------------
  // sets of worlds are bitmasks; succ[w] is the mask of worlds that w sees
  function mBox(X, succ, n) { var o = 0; for (var w = 0; w < n; w++) if ((succ[w] & ~X) === 0) o |= 1 << w; return o; }
  function mDia(X, succ, n) { var o = 0; for (var w = 0; w < n; w++) if (succ[w] & X) o |= 1 << w; return o; }
  var MODAL = [
    { name: "T", f: "□p → p", cond: "reflexive", ev: function (p, s, n, all) { return (all & ~mBox(p, s, n)) | p; },
      ok: function (s, n) { for (var w = 0; w < n; w++) if (!(s[w] >> w & 1)) return false; return true; } },
    { name: "D", f: "□p → ◇p", cond: "serial", ev: function (p, s, n, all) { return (all & ~mBox(p, s, n)) | mDia(p, s, n); },
      ok: function (s, n) { for (var w = 0; w < n; w++) if (!s[w]) return false; return true; } },
    { name: "B", f: "p → □◇p", cond: "symmetric", ev: function (p, s, n, all) { return (all & ~p) | mBox(mDia(p, s, n), s, n); },
      ok: function (s, n) { for (var w = 0; w < n; w++) for (var v = 0; v < n; v++) if ((s[w] >> v & 1) && !(s[v] >> w & 1)) return false; return true; } },
    { name: "4", f: "□p → □□p", cond: "transitive", ev: function (p, s, n, all) { var b = mBox(p, s, n); return (all & ~b) | mBox(b, s, n); },
      ok: function (s, n) { for (var w = 0; w < n; w++) for (var v = 0; v < n; v++) if ((s[w] >> v & 1) && (s[v] & ~s[w])) return false; return true; } },
    { name: "5", f: "◇p → □◇p", cond: "euclidean", ev: function (p, s, n, all) { var d = mDia(p, s, n); return (all & ~d) | mBox(d, s, n); },
      ok: function (s, n) { for (var w = 0; w < n; w++) for (var v = 0; v < n; v++) if ((s[w] >> v & 1) && (s[w] & ~s[v])) return false; return true; } },
    { name: "Löb", f: "□(□p → p) → □p", cond: "transitive, no cycle",
      ev: function (p, s, n, all) { var b = mBox(p, s, n); return (all & ~mBox((all & ~b) | p, s, n)) | b; },
      ok: function (s, n) {
        var w, v;
        for (w = 0; w < n; w++) for (v = 0; v < n; v++) if ((s[w] >> v & 1) && (s[v] & ~s[w])) return false; // transitive
        for (w = 0; w < n; w++) if (s[w] >> w & 1) return false; // transitive and irreflexive: no cycle
        return true;
      } },
  ];
  function refute(ax, succ, n) { // the first valuation of p and world where the axiom fails, or null
    var all = (1 << n) - 1;
    for (var p = 0; p <= all; p++) { var t = ax.ev(p, succ, n, all) & all; if (t !== all) { for (var w = 0; w < n; w++) if (!(t >> w & 1)) return { p: p, w: w }; } }
    return null;
  }

  W.frameaxioms = function (el) {
    QB.widget(el, {
      title: "The shape of the arrows decides the axiom",
      sub: "A frame: worlds, and arrows saying which world sees which. The table tests six axioms on it under every valuation of p. Press the buttons to add every loop, every reverse arrow or every shortcut, and watch T, B and 4 turn valid. For the axiom you select, the picture shows a valuation that refutes it: p is true at the gold worlds, and the axiom fails at the ringed one.",
      panels: 2, height: 320,
      controls: [
        { k: "n", label: "Worlds", min: 2, max: 5, step: 1, value: 4, fmt: function (x) { return String(x); } },
        { k: "d", label: "Density of arrows", min: 0, max: 1, step: 0.05, value: 0.4, fmt: function (x) { return x.toFixed(2); } },
        { k: "ax", label: "Axiom to refute", min: 0, max: 5, step: 1, value: 0, fmt: function (x) { return MODAL[x].name; } },
      ],
      buttons: [
        { label: "New frame", act: function (s) { s.seed++; } },
        { label: "Loops on/off", act: function (s) { s.refl = !s.refl; } },
        { label: "Reverse arrows on/off", act: function (s) { s.sym = !s.sym; } },
        { label: "Shortcuts on/off", act: function (s) { s.trans = !s.trans; } },
      ],
      draw: function (g, v, s) {
        var n = v.n, r = QB.rng(53 * s.seed + 11), succ = [], w, u, k, c = g.ctx, bx = g[0].box;
        var un = []; for (k = 0; k < 25; k++) un.push(r());
        for (w = 0; w < n; w++) { succ[w] = 0; for (u = 0; u < n; u++) if (un[5 * w + u] < v.d) succ[w] |= 1 << u; }
        if (s.refl) for (w = 0; w < n; w++) succ[w] |= 1 << w;
        if (s.sym) for (w = 0; w < n; w++) for (u = 0; u < n; u++) if (succ[w] >> u & 1) succ[u] |= 1 << w;
        if (s.trans) for (k = 0; k < n; k++) for (w = 0; w < n; w++) if (succ[w] >> k & 1) succ[w] |= succ[k]; // Warshall
        s.res = MODAL.map(function (ax) { return { cex: refute(ax, succ, n), ok: ax.ok(succ, n) }; });
        var arrows = 0; for (w = 0; w < n; w++) for (u = 0; u < n; u++) if (succ[w] >> u & 1) arrows++;
        s.arrows = arrows;
        var cex = s.res[v.ax].cex;
        // left: the frame
        c.save();
        font(c, 12.5, true); c.fillStyle = C.ink; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText(cex ? "A valuation refuting " + MODAL[v.ax].name + " at the ringed world" : MODAL[v.ax].name + " is valid on this frame", bx.x + 12, bx.y + 6);
        var cx = bx.x + bx.w / 2, cy = bx.y + bx.h / 2 + 10, rad = Math.min(bx.w, bx.h - 40) * 0.33, nr = 15, pos = [];
        for (w = 0; w < n; w++) { var ang = -Math.PI / 2 + 2 * Math.PI * w / n; pos.push([cx + rad * Math.cos(ang), cy + rad * Math.sin(ang)]); }
        c.strokeStyle = C.spot; c.fillStyle = C.spot; c.lineWidth = 1.6;
        for (w = 0; w < n; w++) for (u = 0; u < n; u++) if (succ[w] >> u & 1) {
          if (w === u) { // a loop, drawn outside the circle of worlds
            var ox = pos[w][0] - cx, oy = pos[w][1] - cy, ol = Math.sqrt(ox * ox + oy * oy) || 1;
            c.beginPath(); c.arc(pos[w][0] + ox / ol * (nr + 7), pos[w][1] + oy / ol * (nr + 7), 10, 0, 6.2832); c.stroke();
            continue;
          }
          var dx = pos[u][0] - pos[w][0], dy = pos[u][1] - pos[w][1], len = Math.sqrt(dx * dx + dy * dy), ux = dx / len, uy = dy / len;
          var both = succ[u] >> w & 1, off = both ? 4 : 0, sx = pos[w][0] + ux * nr - uy * off, sy = pos[w][1] + uy * nr + ux * off;
          var ex = pos[u][0] - ux * (nr + 2) - uy * off, ey = pos[u][1] - uy * (nr + 2) + ux * off;
          c.beginPath(); c.moveTo(sx, sy); c.lineTo(ex, ey); c.stroke();
          c.beginPath(); c.moveTo(ex, ey); c.lineTo(ex - ux * 9 - uy * 4, ey - uy * 9 + ux * 4); c.lineTo(ex - ux * 9 + uy * 4, ey - uy * 9 - ux * 4); c.closePath(); c.fill();
        }
        for (w = 0; w < n; w++) {
          var isP = cex && (cex.p >> w & 1);
          c.fillStyle = isP ? C.idea : C.panel; c.beginPath(); c.arc(pos[w][0], pos[w][1], nr, 0, 6.2832); c.fill();
          c.strokeStyle = cex && cex.w === w ? C.loss : C.ink; c.lineWidth = cex && cex.w === w ? 3.5 : 1.5; c.stroke();
          font(c, 12, true); c.fillStyle = isP ? C.bg : C.ink; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("w" + w, pos[w][0], pos[w][1]);
        }
        c.restore();
        // right: the six axioms
        var b2 = g[1].box, small = b2.w < 420, x0 = b2.x + 12, rowH = Math.min(34, (b2.h - 62) / 6), y0 = b2.y + 52;
        var cols = small ? [0, 138, 288] : [0, 150, 320];
        c.save();
        font(c, 12.5, true); c.fillStyle = C.ink; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("Valid on this frame, under every valuation?", x0, b2.y + 6);
        font(c, 11); c.fillStyle = C.muted; c.textBaseline = "middle";
        c.fillText("axiom", x0 + cols[0], b2.y + 34); c.fillText("the arrows are", x0 + cols[1], b2.y + 34); c.fillText("valid", x0 + cols[2], b2.y + 34);
        MODAL.forEach(function (ax, i) {
          var y = y0 + i * rowH + rowH / 2, res = s.res[i];
          if (i === v.ax) { c.fillStyle = "rgba(88,166,255,0.12)"; c.fillRect(b2.x + 6, y - rowH / 2 + 1, b2.w - 12, rowH - 2); }
          font(c, 12, true); c.fillStyle = C.ink; c.fillText(ax.name, x0 + cols[0], y);
          font(c, small ? 11 : 12); c.fillStyle = C.ink; c.fillText(ax.f, x0 + cols[0] + 28, y);
          c.fillStyle = res.ok ? C.gain : C.muted; c.fillText((res.ok ? "" : "not ") + ax.cond, x0 + cols[1], y);
          font(c, 12, true); c.fillStyle = res.cex ? C.loss : C.gain; c.fillText(res.cex ? "no" : "yes", x0 + cols[2], y);
        });
        c.restore();
      },
      readout: function (v, s) {
        var valid = MODAL.filter(function (ax, i) { return !s.res[i].cex; }).map(function (ax) { return ax.name; });
        return [["arrows", String(s.arrows)], ["closures on", [s.refl ? "loops" : "", s.sym ? "reverses" : "", s.trans ? "shortcuts" : ""].filter(Boolean).join(", ") || "none"],
          ["valid here", valid.join(", ") || "none"], ["axiom and shape agree on", MODAL.filter(function (ax, i) { return !s.res[i].cex === s.res[i].ok; }).length + " of 6"]];
      },
      note: "Simulated frame: each arrow is present independently with the chosen density, then the closures you switched on are applied. Validity is checked by brute force over all 2ⁿ valuations of p. 'No cycle' includes loops: on a finite frame it is what 'no infinite chain' comes to.",
    });
  };

  // ---- Part 5: the heap, by sharpenings and by degrees --------------------------------------------------------
  W.heapdegrees = function (el) {
    var N = 100;
    QB.widget(el, {
      title: "The heap: 101 men, a penumbra, and what modus ponens loses",
      sub: "Man 0 has no hair and man 100 a full head. Choose where the borderline cases begin and how wide the penumbra is. Left: the degree to which each man is bald, and the supervaluationist's verdict over all sharpenings. Right: each conditional 'if man i is bald, so is man i + 1' is almost true, but the guarantee of chained modus ponens leaks at every step. Narrow the penumbra to one man and the classical sharp cutoff returns.",
      panels: 2, height: 300,
      controls: [
        { k: "lo", label: "Last clearly bald man", min: 0, max: 60, step: 1, value: 30, fmt: function (x) { return String(x); } },
        { k: "w", label: "Width of the penumbra", min: 1, max: 40, step: 1, value: 40, fmt: function (x) { return String(x); } },
        { k: "i", label: "Inspect man", min: 0, max: 100, step: 1, value: 50, fmt: function (x) { return String(x); } },
      ],
      draw: function (g, v, s) {
        var lo = v.lo, hi = v.lo + v.w, men = [], deg = [], cond = [], bound = [1], i, out = -1;
        for (i = 0; i <= N; i++) { men.push(i); deg.push(i <= lo ? 1 : i >= hi ? 0 : (hi - i) / (hi - lo)); }
        for (i = 0; i < N; i++) {
          cond.push(Math.min(1, 1 - deg[i] + deg[i + 1]));
          var b = bound[i] + cond[i] - 1; bound.push(b < 1e-9 ? 0 : b);
          if (out < 0 && bound[i + 1] === 0) out = i + 1;
        }
        var m = v.i, status = m <= lo ? "super-true" : m >= hi ? "super-false" : "neither";
        s.out = { min: 1 - 1 / (hi - lo), out: out, status: status, deg: deg[m], bound: bound[m], sharp: hi - lo };
        var a = g[0].axes({ x: [0, N], y: [0, 1.25], title: "'Man i is bald'", xlabel: "man i", yticks: [0, 0.5, 1] });
        a.area([0, lo], [1.25, 1.25], 0, { color: C.gain, alpha: 0.10 });
        a.area([lo, hi], [1.25, 1.25], 0, { color: C.idea, alpha: 0.12 });
        a.area([hi, N], [1.25, 1.25], 0, { color: C.loss, alpha: 0.10 });
        a.line(men, deg, { color: C.spot, width: 2.2 });
        a.vline(m, { color: C.ink, dash: [], width: 1.2 }); a.dots([m], [deg[m]], { color: C.spot, r: 5 });
        a.legend([["degree of 'bald'", C.spot], ["super-true", C.gain], ["neither (penumbra)", C.idea], ["super-false", C.loss]], { pos: "tr" });
        var b2 = g[1].axes({ x: [0, N], y: [0, 1.25], title: "The argument, step by step", xlabel: "man i", yticks: [0, 0.5, 1] });
        b2.line(men.slice(0, N), cond, { color: C.idea, width: 2 });
        b2.line(men, bound, { color: C.loss, width: 2.2 });
        b2.vline(m, { color: C.ink, dash: [], width: 1.2 }); b2.dots([m], [bound[m]], { color: C.loss, r: 5 });
        b2.legend([["degree of 'if i is bald, so is i + 1'", C.idea], ["what modus ponens still guarantees", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["man " + v.i + " is bald", s.out.status + ", degree " + fmt(s.out.deg, 2)], ["sharpenings", String(s.out.sharp)],
          ["lowest conditional", fmt(s.out.min, 3)], ["guarantee at man " + v.i, fmt(s.out.bound, 2)], ["guarantee gone at man", String(s.out.out)]];
      },
      note: "A sharpening is a cutoff inside the penumbra; a sentence is super-true if true on every sharpening. Degrees fall linearly across the penumbra, the conditional has Łukasiewicz degree min(1, 1 − a + b), and modus ponens guarantees only a + (a → b) − 1. The conditionals inside the penumbra are each false on exactly one sharpening, so none is super-true.",
    });
  };

  // ---- Part 6: Cantor's diagonal, and the row that keeps escaping --------------------------------------------
  W.diagonalescape = function (el) {
    var MAXN = 16;
    QB.widget(el, {
      title: "The row that is not on the list",
      sub: "A list of rows of zeros and ones (gold is 1). Flip each cell on the diagonal and you get a new row that differs from row i at place i, so it is nowhere on the list. Press 'Add the new row to the list': the list grows, and its diagonal produces another row that escapes. Read row x as the set f(x) and the new row is Cantor's set of all x not in f(x).",
      panels: 2, height: 320,
      controls: [
        { k: "n", label: "Rows on the list", min: 3, max: 10, step: 1, value: 6, fmt: function (x) { return String(x); } },
        { k: "p", label: "Share of ones", min: 0, max: 1, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [
        { label: "Add the new row to the list", act: function (s) { s.added = (s.added || 0) + 1; } },
        { label: "New list", act: function (s) { s.seed++; s.added = 0; } },
      ],
      draw: function (g, v, s) {
        var added = Math.min(s.added || 0, MAXN - v.n), m = v.n + added, T = [], i, j, c = g.ctx, bx = g[0].box;
        s.added = added;
        var base = function (a, b) { return QB.rng(4099 * s.seed + 67 * a + b + 1)() < v.p ? 1 : 0; };
        for (i = 0; i < m; i++) {
          T.push([]);
          for (j = 0; j < m; j++) T[i].push(i >= v.n && j < i ? 1 - T[j][j] : base(i, j)); // an added row starts as the flipped diagonal it came from
        }
        var d = [], dist = [], least = m;
        for (i = 0; i < m; i++) d.push(1 - T[i][i]);
        for (i = 0; i < m; i++) { var k = 0; for (j = 0; j < m; j++) if (T[i][j] !== d[j]) k++; dist.push(k); least = Math.min(least, k); }
        s.out = { m: m, least: least, added: added };
        // left: the table and the flipped diagonal
        c.save();
        font(c, 12.5, true); c.fillStyle = C.ink; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("The list, its diagonal, and the flipped row", bx.x + 12, bx.y + 6);
        var cell = Math.min((bx.w - 70) / m, (bx.h - 78) / (m + 1.6)), x0 = bx.x + 46, y0 = bx.y + 32;
        font(c, 11); c.textBaseline = "middle";
        for (i = 0; i < m; i++) {
          if (cell >= 13) { c.fillStyle = i >= v.n ? C.realized : C.muted; c.textAlign = "right"; c.fillText("row " + (i + 1), x0 - 6, y0 + (i + 0.5) * cell); }
          for (j = 0; j < m; j++) {
            c.fillStyle = T[i][j] ? C.idea : C.line; c.globalAlpha = i === j ? 1 : 0.55;
            c.fillRect(x0 + j * cell + 1, y0 + i * cell + 1, cell - 2, cell - 2);
          }
          c.globalAlpha = 1; c.strokeStyle = C.spot; c.lineWidth = 2; c.strokeRect(x0 + i * cell + 1, y0 + i * cell + 1, cell - 2, cell - 2);
        }
        var yd = y0 + m * cell + 0.6 * cell;
        c.fillStyle = C.loss; c.textAlign = "right"; c.fillText("new", x0 - 6, yd + cell / 2);
        for (j = 0; j < m; j++) {
          c.fillStyle = d[j] ? C.idea : C.line; c.fillRect(x0 + j * cell + 1, yd + 1, cell - 2, cell - 2);
          c.strokeStyle = C.loss; c.lineWidth = 2; c.strokeRect(x0 + j * cell + 1, yd + 1, cell - 2, cell - 2);
        }
        c.restore();
        // right: how far the new row is from each row
        var xs = []; for (i = 0; i < m; i++) xs.push(i + 1);
        var a = g[1].axes({ x: [0.4, m + 0.6], y: [0, m + 0.5], title: "Places where the new row differs from row i", xlabel: "row i", xticks: xs, ny: 4 });
        a.bars(xs, dist, 0.7, { color: function (q) { return q >= v.n ? C.realized : C.spot; } });
        a.hline(1, { color: C.loss });
        a.legend([["rows of the first list", C.spot], ["rows you added", C.realized], ["at least 1: place i", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["rows on the list", String(s.out.m)], ["rows added", String(s.out.added)], ["closest row differs in", s.out.least + (s.out.least === 1 ? " place" : " places")],
          ["the new row is on the list", s.out.least === 0 ? "yes" : "no"]];
      },
      note: "Simulated list: each cell is 1 independently with the chosen share. An added row is the flipped diagonal of the list as it then stood, so it differs from the next new row at its own diagonal cell at least. The list stops growing at 16 rows here; the argument does not.",
    });
  };
})();
