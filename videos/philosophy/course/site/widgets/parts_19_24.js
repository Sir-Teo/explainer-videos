// Interactives for Life and Act V, The World (Parts 19-24).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  // ---- Part 19: Hamilton's rule ------------------------------------------------------------------------------
  W.hamiltonkin = function (el) {
    QB.widget(el, {
      title: "Hamilton's rule: when does helping a relative spread?",
      sub: "Pairs of relatives meet; an altruist pays c offspring and gives its partner b. With probability r the partner carries the same gene by descent. Move r, b and c across the curve rb = c and watch the share of altruists turn around.",
      panels: 2, height: 300,
      controls: [
        { k: "r", label: "Relatedness r", min: 0, max: 1, step: 0.005, value: 0.5, fmt: function (x) { return x.toFixed(3); } },
        { k: "b", label: "Benefit to the partner b", min: 0, max: 1, step: 0.01, value: 0.3, fmt: function (x) { return x.toFixed(2); } },
        { k: "c", label: "Cost to the helper c", min: 0.02, max: 0.5, step: 0.01, value: 0.1, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New population", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var rnd = QB.rng(s.seed + 19), gens = 60, n = 1000, p = 0.2, q = 0.2, sim = [p], det = [q], ts = [0], t, i;
        for (t = 1; t <= gens; t++) {
          var num = 0, den = 0;
          for (i = 0; i < n; i++) {
            var f = rnd() < p ? 1 : 0, o = rnd() < v.r ? f : (rnd() < p ? 1 : 0);
            var wf = 1 - v.c * f + v.b * o, wo = 1 - v.c * o + v.b * f;
            num += f * wf + o * wo; den += wf + wo;
          }
          p = den > 0 ? Math.min(1, Math.max(0, num / den)) : p;
          q = q * (1 - v.c + v.b * (v.r + (1 - v.r) * q)) / (1 + (v.b - v.c) * q);
          sim.push(p); det.push(q); ts.push(t);
        }
        s.out = [v.r * v.b - v.c, sim[gens], det[gens]];
        var up = s.out[0] > 0, col = up ? C.gain : C.loss;
        var a = g[0].axes({ x: [0, gens], y: [0, 1], title: "Share of altruists", xlabel: "generation" });
        a.hline(0.2, { color: C.muted });
        a.line(ts, sim, { color: C.spot, width: 1.4, alpha: 0.9 });
        a.line(ts, det, { color: col, width: 2.2 });
        a.legend([["expected (no drift)", col], ["1,000 simulated pairs", C.spot]], { pos: up ? "br" : "tr" });
        var b = g[1].axes({ x: [0, 1], y: [0, 10], title: "The rule: b/c above 1/r", xlabel: "relatedness r" });
        var rs = QB.linspace(0.1, 1, 60), hy = rs.map(function (x) { return 1 / x; });
        b.area(rs, hy.map(function () { return 10; }), hy, { color: C.gain, alpha: 0.13 });
        b.line(rs, hy, { color: C.idea, width: 2 });
        b.text(0.56, 6.4, "altruism spreads", { color: C.gain });
        b.text(0.05, 1.1, "dies out", { color: C.loss });
        b.text(0.2, 5.6, "rb = c", { color: C.idea, dx: 6 });
        b.dots([v.r], [Math.min(10, v.b / v.c)], { color: col, r: 6 });
      },
      readout: function (v, s) {
        return [["rb − c", fmt(s.out[0], 3)], ["b/c", fmt(v.b / v.c, 1)], ["needed 1/r", v.r > 0 ? fmt(1 / v.r, 1) : "no benefit is enough"],
          ["altruists after 60 generations", QB.pct(s.out[1], 0) + " (expected " + QB.pct(s.out[2], 0) + ")"]];
      },
      note: "Simulated data. The model is the film's: baseline fitness 1, a fifth of the population altruistic at the start. Siblings have r = 1/2, half-siblings 1/4, cousins 1/8. The dot is drawn at b/c = 10 when the ratio is larger.",
    });
  };

  // ---- Part 20: the special composition question, counted ----------------------------------------------------
  W.blockfusions = function (el) {
    QB.widget(el, {
      title: "How many things are there? Blocks, contact and fusion",
      sub: "Blocks are scattered on a table. Nihilism counts only the blocks; universalism counts every group of them; the contact answer counts the groups that hang together. Widen what counts as touching and the contact count climbs from one extreme to the other.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Blocks", min: 2, max: 10, step: 1, value: 6, fmt: function (x) { return String(x); } },
        { k: "reach", label: "How close counts as touching", min: 0, max: 1.5, step: 0.01, value: 0.3, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "Scatter again", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var rnd = QB.rng(s.seed + 2020), n = v.n, xs = [], ys = [], i, j, m;
        for (i = 0; i < 10; i++) { xs.push(0.08 + 0.84 * rnd()); ys.push(0.1 + 0.8 * rnd()); }
        var adj = [];
        for (i = 0; i < n; i++) {
          adj.push(0);
          for (j = 0; j < n; j++) if (i !== j && Math.sqrt((xs[i] - xs[j]) * (xs[i] - xs[j]) + (ys[i] - ys[j]) * (ys[i] - ys[j])) <= v.reach) adj[i] |= 1 << j;
        }
        var contact = 0, bySize = [], biggest = 0;
        for (i = 0; i <= n; i++) bySize.push(0);
        for (m = 1; m < (1 << n); m++) {
          var seen = m & -m, grew = true;
          while (grew) { grew = false; for (i = 0; i < n; i++) if ((seen >> i) & 1) { var add = adj[i] & m & ~seen; if (add) { seen |= add; grew = true; } } }
          if (seen === m) { contact++; var k = 0; for (i = 0; i < n; i++) k += (m >> i) & 1; bySize[k]++; if (k > biggest) biggest = k; }
        }
        s.out = [n, contact, Math.pow(2, n) - 1, biggest];
        var a = g[0].axes({ x: [0, 1], y: [0, 1], title: "The table", noX: true, noY: true });
        for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) if ((adj[i] >> j) & 1) a.line([xs[i], xs[j]], [ys[i], ys[j]], { color: C.idea, width: 2, alpha: 0.8 });
        a.dots(xs.slice(0, n), ys.slice(0, n), { color: C.spot, r: 8 });
        a.legend([["a block (a simple)", C.spot], ["two blocks touching", C.idea]], { pos: "bl" });
        var top = Math.pow(2, n);
        var b = g[1].axes({ x: [0.4, 3.6], y: [1, Math.max(10, 4 * top)], logy: true, title: "Objects, on three answers", xticks: [1, 2, 3],
          xfmt: function (t) { return ["nihilism", "contact", "universalism"][t - 1]; } });
        b.bars([1, 2, 3], [n, contact, top - 1], 0.6, { color: function (q) { return [C.spot, C.idea, C.q][q]; }, base: 1 });
        b.text(1, n, String(n), { align: "center", dy: -9, bg: true });
        b.text(2, contact, String(contact), { align: "center", dy: -9, bg: true });
        b.text(3, top - 1, String(top - 1), { align: "center", dy: -9, bg: true });
      },
      readout: function (v, s) {
        return [["nihilism", String(s.out[0])], ["contact", String(s.out[1])], ["universalism", String(s.out[2])], ["largest object by contact", s.out[3] + " of " + s.out[0] + " blocks"]];
      },
      note: "Simulated positions. A group counts as one object on the contact answer when its blocks are linked by a chain of touching pairs. The count jumps at exact distances: the argument from vagueness asks what could make one of those cut-offs the right one.",
    });
  };

  // ---- Part 21: connectedness and continuity over a life -----------------------------------------------------
  W.parfitfade = function (el) {
    QB.widget(el, {
      title: "One life: direct memory links fade, the chain holds",
      sub: "Each year lays down memories, and each memory survives a year with the chosen probability. Left: how much of one earlier self every later self still holds. Right: selves a decade apart, joined by an arc when the later one holds enough of the earlier one's memories. Lower the retention or raise the bar until the chain itself breaks.",
      panels: 2, height: 300,
      controls: [
        { k: "keep", label: "Yearly retention of a memory", min: 0.8, max: 0.99, step: 0.005, value: 0.95, fmt: function (x) { return x.toFixed(3); } },
        { k: "bar", label: "Share needed for a direct link", min: 0.05, max: 0.95, step: 0.01, value: 0.5, fmt: function (x) { return QB.pct(x, 0); } },
        { k: "ref", label: "Age of the earlier self", min: 5, max: 40, step: 1, value: 10, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New life", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var rnd = QB.rng(s.seed + 21), years = 81, per = 60, born = [], death = [], y, i, j, k;
        for (y = 0; y < years; y++) for (i = 0; i < per; i++) {
          var u = rnd(); if (u < 1e-12) u = 1e-12;
          born.push(y); death.push(y + 1 + Math.max(1, Math.ceil(Math.log(u) / Math.log(v.keep))));
        }
        var conn = function (a, b) { // share of the memories held at age a that are still held at age b >= a
          var held = 0, still = 0;
          for (k = 0; k < born.length; k++) if (born[k] <= a && death[k] > a) { held++; if (death[k] > b) still++; }
          return held > 0 ? still / held : 0;
        };
        var ages = [], sim = [], th = [], half = -1;
        for (y = v.ref; y < years; y++) {
          ages.push(y); sim.push(conn(v.ref, y)); th.push(Math.pow(v.keep, y - v.ref));
          if (half < 0 && sim[sim.length - 1] < 0.5) half = y;
        }
        var a = g[0].axes({ x: [0, 80], y: [0, 1], title: "Memories of the earlier self still held", xlabel: "age" });
        a.hline(v.bar, { color: C.idea });
        a.text(79, v.bar, "direct link", { color: C.idea, align: "right", dy: v.bar > 0.85 ? 10 : -9 });
        a.line(ages, th, { color: C.muted, dash: [4, 4], width: 1.2 });
        a.line(ages, sim, { color: C.spot, width: 2 });
        a.vline(v.ref, { color: C.muted });
        a.legend([["simulated life", C.spot], ["retention^years", C.muted]], { pos: "tr" });
        var nodes = [0, 10, 20, 30, 40, 50, 60, 70, 80], link = [], direct = 0, chain = true;
        var b = g[1].axes({ x: [-6, 86], y: [0, 1], title: "Selves a decade apart", xlabel: "age", noY: true, xticks: nodes });
        for (i = 0; i < nodes.length; i++) for (j = i + 1; j < nodes.length; j++) {
          var c = conn(nodes[i], nodes[j]);
          if (j === i + 1) { link.push(c); if (c < v.bar) chain = false; }
          if (c >= v.bar) {
            direct++;
            var xs = QB.linspace(nodes[i], nodes[j], 24), hgt = 0.1 + 0.82 * (j - i) / 8;
            b.line(xs, xs.map(function (x) { var t = (x - nodes[i]) / (nodes[j] - nodes[i]); return 0.08 + 4 * (hgt - 0.08) * t * (1 - t); }),
              { color: j === i + 1 ? C.gain : C.idea, width: j === i + 1 ? 2.4 : 1.4, alpha: 0.9 });
          }
        }
        b.dots(nodes, nodes.map(function () { return 0.08; }), { color: C.spot, r: 5 });
        b.legend([["neighbours linked", C.gain], ["a longer direct link", C.idea]], { pos: "tl" });
        if (!chain) b.text(40, 0.6, "the chain is broken", { color: C.loss, align: "center", bold: true, bg: true });
        s.out = [half, QB.mean(link), direct, chain, conn(0, 80) >= v.bar];
      },
      readout: function (v, s) {
        return [["under half of the earlier self at age", s.out[0] < 0 ? "never, by 80" : String(s.out[0])],
          ["decade-to-decade overlap", QB.pct(s.out[1], 0)], ["direct links among 36 pairs", String(s.out[2])],
          ["the child linked to the 80-year-old", s.out[4] ? "directly" : (s.out[3] ? "only through the chain" : "not at all")]];
      },
      note: "Simulated data: 60 memories a year for 80 years. Connectedness is the share of an earlier self's memories a later self holds; continuity is an unbroken chain of strong links. Reid's officer is the case where the ends of the chain are not linked directly.",
    });
  };

  // ---- Part 22: the two-dimensional matrix -------------------------------------------------------------------
  W.twodmatrix = function (el) {
    var WORLDS = [
      { name: "Earth", watery: "H2O", evening: "Venus", morning: "Venus", stick: "1.00 m" },
      { name: "Twin Earth", watery: "XYZ", evening: "Venus", morning: "Mars", stick: "1.01 m" },
      { name: "Dusk", watery: "H2O", evening: "Mars", morning: "Venus", stick: "1.00 m" },
    ];
    // a term is rigid (fixed by the world considered as actual), a description (looked up where we check), or a constant
    var SENT = [
      ["water = H2O", ["rigid", "watery"], ["const", "H2O"]],
      ["Hesperus = Phosphorus", ["rigid", "evening"], ["rigid", "morning"]],
      ["water = the watery stuff", ["rigid", "watery"], ["desc", "watery"]],
      ["the length of S = one metre", ["desc", "stick"], ["rigid", "stick"]],
      ["the evening star = Venus", ["desc", "evening"], ["const", "Venus"]],
      ["H2O = H2O", ["const", "H2O"], ["const", "H2O"]],
    ];
    function term(t, w, u) { return t[0] === "rigid" ? WORLDS[w][t[1]] : t[0] === "desc" ? WORLDS[u][t[1]] : t[1]; }
    QB.widget(el, {
      title: "One sentence, two worlds: the two-dimensional matrix",
      sub: "Each row takes a world as actual, which fixes what the names pick out; each column is the world where the sentence is then checked. The gold diagonal says whether it is a priori, the blue row whether it is necessary. Pick a sentence, then change which world is actual: the necessity can change, the diagonal cannot.",
      panels: 2, height: 300,
      controls: [
        { k: "sent", label: "Sentence", min: 1, max: 6, step: 1, value: 1, fmt: function (x) { return SENT[x - 1][0]; } },
        { k: "act", label: "World that is actual", min: 1, max: 3, step: 1, value: 1, fmt: function (x) { return WORLDS[x - 1].name; } },
      ],
      draw: function (g, v, s) {
        var S = SENT[v.sent - 1], act = v.act - 1, M = [], i, j, c = g.ctx;
        for (i = 0; i < 3; i++) { M.push([]); for (j = 0; j < 3; j++) M[i].push(term(S[1], i, j) === term(S[2], i, j)); }
        var rowT = M[act][0] && M[act][1] && M[act][2], rowF = !M[act][0] && !M[act][1] && !M[act][2];
        var prio = M[0][0] && M[1][1] && M[2][2];
        s.out = [S[0], rowT ? "necessary" : rowF ? "necessarily false" : "contingent", prio ? "a priori" : "a posteriori", M[act][act]];
        var b = g[0].box, left = b.x + 88, top = b.y + 56, cw = Math.min(120, (b.w - 100) / 3), ch = Math.min(64, (b.h - 84) / 3);
        c.save(); c.textBaseline = "middle";
        c.font = "600 12.5px system-ui, sans-serif"; c.fillStyle = C.ink; c.textAlign = "left"; c.fillText(S[0], b.x + 12, b.y + 14);
        c.font = "11px system-ui, sans-serif"; c.fillStyle = C.muted; c.fillText("columns: the world where it is checked", b.x + 12, b.y + 31);
        for (j = 0; j < 3; j++) { c.textAlign = "center"; c.fillStyle = C.muted; c.fillText(WORLDS[j].name, left + cw * (j + 0.5), top - 9); }
        for (i = 0; i < 3; i++) {
          c.textAlign = "right"; c.fillStyle = i === act ? C.spot : C.muted; c.font = (i === act ? "600 " : "") + "11px system-ui, sans-serif";
          c.fillText(WORLDS[i].name, left - 8, top + ch * (i + 0.5));
          for (j = 0; j < 3; j++) {
            c.fillStyle = M[i][j] ? "rgba(74,222,128,0.30)" : "rgba(248,113,113,0.28)"; c.fillRect(left + cw * j + 2, top + ch * i + 2, cw - 4, ch - 4);
            c.fillStyle = M[i][j] ? C.gain : C.loss; c.textAlign = "center"; c.font = "600 14px system-ui, sans-serif";
            c.fillText(M[i][j] ? "true" : "false", left + cw * (j + 0.5), top + ch * (i + 0.5));
          }
        }
        c.lineWidth = 2.5; c.strokeStyle = C.idea;
        for (i = 0; i < 3; i++) c.strokeRect(left + cw * i + 2, top + ch * i + 2, cw - 4, ch - 4);
        c.strokeStyle = C.spot; c.setLineDash([6, 4]); c.strokeRect(left - 2, top + ch * act - 2, cw * 3 + 4, ch + 4); c.setLineDash([]);
        c.font = "11px system-ui, sans-serif"; c.textAlign = "left";
        c.fillStyle = C.idea; c.fillText("gold: the diagonal", b.x + 12, top + ch * 3 + 16);
        c.fillStyle = C.spot; c.fillText("blue: the actual row", b.x + 12 + Math.min(150, b.w / 2), top + ch * 3 + 16);
        // the four boxes
        var q = g[1].box, qx = q.x + 96, qy = q.y + 56, qw = Math.max(60, (q.w - 112) / 2), qh = Math.min(84, (q.h - 80) / 2);
        c.font = "600 12.5px system-ui, sans-serif"; c.fillStyle = C.ink; c.fillText("Where it lands", q.x + 12, q.y + 14);
        c.font = "11px system-ui, sans-serif"; c.fillStyle = C.muted; c.fillText("with " + WORLDS[act].name + " as the actual world", q.x + 12, q.y + 31);
        var cols = ["a priori", "a posteriori"], rows = ["necessary", "contingent"], col = prio ? 0 : 1, row = rowT ? 0 : rowF ? -1 : 1;
        for (j = 0; j < 2; j++) { c.textAlign = "center"; c.fillStyle = C.muted; c.fillText(cols[j], qx + qw * (j + 0.5), qy - 9); }
        for (i = 0; i < 2; i++) {
          c.textAlign = "right"; c.fillStyle = C.muted; c.fillText(rows[i], qx - 8, qy + qh * (i + 0.5));
          for (j = 0; j < 2; j++) {
            var here = i === row && j === col;
            c.fillStyle = here ? "rgba(247,209,84,0.25)" : "rgba(38,48,65,0.6)"; c.fillRect(qx + qw * j + 2, qy + qh * i + 2, qw - 4, qh - 4);
            if (here) { c.strokeStyle = C.idea; c.lineWidth = 2; c.strokeRect(qx + qw * j + 2, qy + qh * i + 2, qw - 4, qh - 4); c.fillStyle = C.idea; c.beginPath(); c.arc(qx + qw * (j + 0.5), qy + qh * (i + 0.5), 7, 0, 6.2832); c.fill(); }
          }
        }
        c.textAlign = "left"; c.fillStyle = row < 0 ? C.loss : C.muted;
        c.fillText(row < 0 ? "false in every world: necessarily false here" : "the four boxes of necessity and a priority", q.x + 12, qy + qh * 2 + 16);
        c.restore();
      },
      readout: function (v, s) {
        return [["sentence", s.out[0]], ["actual row", s.out[1]], ["diagonal", s.out[2]], ["true in the actual world", s.out[3] ? "yes" : "no"]];
      },
      note: "The three worlds are the film's. Earth: the watery stuff is H2O, and one planet is both evening and morning star. Twin Earth: the watery stuff is XYZ, the morning star is Mars, and stick S is 1.01 m long. Dusk: the evening star is Mars. Names and 'one metre' are rigid; 'the watery stuff', 'the evening star' and 'the length of S' are descriptions.",
    });
  };

  // ---- Part 23: Hume on miracles, by the numbers -------------------------------------------------------------
  W.miraclewitness = function (el) {
    QB.widget(el, {
      title: "Hume's maxim: how many witnesses outweigh a miracle?",
      sub: "A report of an event with a tiny prior. Each witness reports it with one probability if it happened and a smaller one if it did not. Left: the probability it happened after k reports. Right: the same in odds, where each independent witness adds one step. Raise the share of witnesses who merely repeat the first, and the steps shrink to nothing.",
      panels: 2, height: 300,
      controls: [
        { k: "lp", label: "Prior probability of the event", min: -9, max: -1, step: 0.1, value: -6, fmt: function (x) { return "1 in " + Number(Math.pow(10, -x).toPrecision(2)).toLocaleString("en-US"); } },
        { k: "hit", label: "A witness reports it, if it happened", min: 0.5, max: 0.999, step: 0.001, value: 0.99, fmt: function (x) { return QB.pct(x, 1); } },
        { k: "fa", label: "A witness reports it, if it did not", min: 0.001, max: 0.5, step: 0.001, value: 0.01, fmt: function (x) { return QB.pct(x, 1); } },
        { k: "copy", label: "Later witnesses who repeat the first", min: 0, max: 1, step: 0.01, value: 0, fmt: function (x) { return QB.pct(x, 0); } },
      ],
      draw: function (g, v, s) {
        var K = 12, ks = [], dep = [], ind = [], ldep = [], lind = [], k, first = -1;
        var l0 = v.lp - Math.log10(1 - Math.pow(10, v.lp)); // log10 prior odds
        var stepI = Math.log10(v.hit / v.fa), stepD = Math.log10((v.copy + (1 - v.copy) * v.hit) / (v.copy + (1 - v.copy) * v.fa));
        var post = function (lo) { return 1 / (1 + Math.pow(10, -lo)); };
        for (k = 0; k <= K; k++) {
          var li = l0 + k * stepI, ld = k === 0 ? l0 : l0 + stepI + (k - 1) * stepD;
          ks.push(k); lind.push(li); ldep.push(ld); ind.push(post(li)); dep.push(post(ld));
          if (first < 0 && post(ld) > 0.5) first = k;
        }
        s.out = [dep[1], dep[4], first, stepI, stepD];
        var a = g[0].axes({ x: [0, K], y: [0, 1], title: "Probability the event happened", xlabel: "witnesses who report it" });
        a.hline(0.5, { color: C.muted });
        a.line(ks, ind, { color: C.muted, dash: [4, 4], width: 1.4 });
        a.line(ks, dep, { color: C.idea, width: 2.2 });
        a.dots(ks, dep, { color: C.idea, r: 3.2 });
        a.legend([["these witnesses", C.idea], ["if all were independent", C.muted]], { pos: "br" });
        var lo = Math.min(-9.5, l0 - 0.5), hi = Math.max(4, Math.min(30, l0 + K * stepI));
        var b = g[1].axes({ x: [0, K], y: [lo, hi], title: "The same, as log10 odds", xlabel: "witnesses who report it" });
        b.hline(0, { color: C.muted });
        b.text(K, 0, "even odds", { color: C.muted, align: "right", dy: -9 });
        b.line(ks, lind, { color: C.muted, dash: [4, 4], width: 1.4 });
        b.line(ks, ldep, { color: C.idea, width: 2.2 });
        b.dots(ks, ldep, { color: C.idea, r: 3.2 });
      },
      readout: function (v, s) {
        var p = function (x) { return x < 0.001 ? "1 in " + Math.round(1 / Math.max(x, 1e-300)).toLocaleString("en-US") : QB.pct(x, 1); };
        return [["after one witness", p(s.out[0])], ["after four", p(s.out[1])],
          ["first more probable than not at", s.out[2] < 0 ? "more than 12 witnesses" : s.out[2] + (s.out[2] === 1 ? " witness" : " witnesses")],
          ["odds multiplied per later witness", "×" + (Math.pow(10, s.out[4]) >= 100 ? Math.round(Math.pow(10, s.out[4])) : fmt(Math.pow(10, s.out[4]), 2))]];
      },
      note: "The defaults are the film's: a one-in-a-million event and witnesses who are right 99 times in 100 leave it at about 1 in 10,000 after one report and more probable than not after four. A later witness repeats the first with the chosen probability and otherwise reports independently; at 100% the crowd is one witness.",
    });
  };

  // ---- Part 24: the Kac ring ---------------------------------------------------------------------------------
  W.kacring = function (el) {
    QB.widget(el, {
      title: "The Kac ring: reversible, recurrent, and it still decays",
      sub: "Balls sit on a ring, all white at the start. At each step every ball moves one place clockwise and changes colour if it crosses a gold marker. Slide the time forward: the imbalance decays like a dissipative system. Keep sliding to N and to 2N steps, where the rule that predicted the decay fails completely.",
      panels: 2, height: 320,
      controls: [
        { k: "time", label: "Time, in turns of the ring (t / N)", min: 0, max: 2, step: 0.005, value: 0.1, fmt: function (x) { return x.toFixed(3); } },
        { k: "mu", label: "Share of edges with a marker", min: 0, max: 0.5, step: 0.01, value: 0.1, fmt: function (x) { return QB.pct(x, 0); } },
        { k: "n", label: "Balls on the ring N", min: 20, max: 300, step: 10, value: 120, fmt: function (x) { return String(x); } },
      ],
      buttons: [{ label: "New markers", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var rnd = QB.rng(s.seed + 1959), N = v.n, marked = [], m = 0, i, t, T = Math.round(v.time * N);
        for (i = 0; i < 300; i++) marked.push(rnd() < v.mu ? 1 : 0);
        for (i = 0; i < N; i++) m += marked[i];
        // the ball that starts at site j has, after t steps, crossed edges j, j+1, ..., j+t-1 (mod N)
        var pre = [0]; for (i = 0; i < 3 * N; i++) pre.push(pre[i] + marked[i % N]);
        var mu = m / N, ts = [], delta = [], theory = [], now = [];
        for (t = 0; t <= 2 * N; t++) {
          var sum = 0; for (i = 0; i < N; i++) sum += ((pre[i + t] - pre[i]) & 1) ? -1 : 1;
          ts.push(t / N); delta.push(sum / N); theory.push(t === 0 ? 1 : Math.pow(1 - 2 * mu, t));
        }
        for (i = 0; i < N; i++) now.push(((pre[i + T] - pre[i]) & 1) ? 0 : 1);
        var white = (1 + delta[T]) / 2, ent = 0;
        if (white > 0 && white < 1) ent = -(white * Math.log(white) + (1 - white) * Math.log(1 - white)) / Math.LN2;
        s.out = [T, m, delta[T], theory[T], ent];
        var c = g.ctx, b = g[0].box, cx = b.x + b.w / 2, cy = b.y + b.h / 2 + 8, R = Math.min(b.w, b.h - 30) / 2 - 16, rad = Math.max(1.6, Math.min(6, 2.4 * R / N));
        c.save();
        c.font = "600 12.5px system-ui, sans-serif"; c.fillStyle = C.ink; c.textAlign = "left"; c.textBaseline = "top"; c.fillText("The ring at step " + T, b.x + 12, b.y + 6);
        c.strokeStyle = C.line; c.lineWidth = 1; c.beginPath(); c.arc(cx, cy, R, 0, 6.2832); c.stroke();
        for (i = 0; i < N; i++) {
          var ang = -Math.PI / 2 + 6.2832 * ((i + T) % N) / N, x = cx + R * Math.cos(ang), y = cy + R * Math.sin(ang);
          c.fillStyle = now[i] ? C.ink : "#3b4658"; c.beginPath(); c.arc(x, y, rad, 0, 6.2832); c.fill();
        }
        c.strokeStyle = C.idea; c.lineWidth = 2;
        for (i = 0; i < N; i++) if (marked[i]) {
          var am = -Math.PI / 2 + 6.2832 * (i + 0.5) / N;
          c.beginPath(); c.moveTo(cx + (R - 9) * Math.cos(am), cy + (R - 9) * Math.sin(am)); c.lineTo(cx + (R + 9) * Math.cos(am), cy + (R + 9) * Math.sin(am)); c.stroke();
        }
        c.font = "11.5px system-ui, sans-serif"; c.textAlign = "center"; c.textBaseline = "middle";
        c.fillStyle = C.ink; c.fillText(QB.pct(white, 0) + " white", cx, cy - 9);
        c.fillStyle = C.idea; c.fillText(m + (m === 1 ? " marker" : " markers"), cx, cy + 9);
        c.restore();
        var a = g[1].axes({ x: [0, 2], y: [-1.05, 1.05], title: "Imbalance (white − black) / N", xlabel: "time t / N" });
        a.hline(0, { color: C.muted });
        a.line(ts, delta, { color: C.spot, width: 1.6 });
        a.line(ts, theory, { color: C.idea, width: 1.6, dash: [5, 4] });
        a.vline(T / N, { color: C.ink });
        a.dots([T / N], [delta[T]], { color: C.spot, r: 5 });
        a.legend([["the ring", C.spot], ["(1 − 2μ)^t", C.idea]], { pos: "bl" });
      },
      readout: function (v, s) {
        return [["step", String(s.out[0])], ["imbalance", fmt(s.out[2], 2)], ["decay rule predicts", fmt(s.out[3], 2)], ["entropy of the colours", fmt(s.out[4], 2) + " bits"]];
      },
      note: "Simulated markers; the motion itself has no chance in it. After N steps every ball has crossed every marker once, so the ring is all black if the number of markers is odd and all white if it is even; after 2N steps it is all white again, whatever the markers.",
    });
  };
})();
