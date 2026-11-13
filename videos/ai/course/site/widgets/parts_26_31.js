// Interactives for Act V, Agency, and Act VI, Understanding (Parts 26-31).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  function label(c, str, x, y, o) { // a line of text on the canvas
    o = o || {}; c.save(); c.font = (o.bold ? "600 " : "") + (o.size || 11.5) + "px system-ui, sans-serif";
    c.fillStyle = o.color || C.ink; c.textAlign = o.align || "left"; c.textBaseline = o.base || "middle"; c.fillText(str, x, y); c.restore();
  }
  function heat(v) { // a value in [-1, 1] as a colour: red below zero, green above
    var a = Math.max(-1, Math.min(1, v)), t = Math.abs(a), base = [28, 36, 50], to = a >= 0 ? [74, 222, 128] : [248, 113, 113];
    return "rgb(" + Math.round(base[0] + (to[0] - base[0]) * t) + "," + Math.round(base[1] + (to[1] - base[1]) * t) + "," + Math.round(base[2] + (to[2] - base[2]) * t) + ")";
  }

  // ---- Part 26: value iteration on the film's gridworld -----------------------------------------------------
  W.bellmansweep = function (el) {
    var GRID = [".........", "..#####..", "......#.G", ".##...#.P", "......#..", "S........"], MOVES = [[-1, 0], [0, 1], [1, 0], [0, -1]];
    var cells = [], index = {}, r, c, s, a;
    for (r = 0; r < 6; r++) for (c = 0; c < 9; c++) if (GRID[r].charAt(c) !== "#") { index[r + "," + c] = cells.length; cells.push([r, c]); }
    var n = cells.length, next = []; // next[s][b]: where a move in direction b lands
    for (s = 0; s < n; s++) {
      next.push([]);
      for (a = 0; a < 4; a++) { var k = index[(cells[s][0] + MOVES[a][0]) + "," + (cells[s][1] + MOVES[a][1])]; next[s].push(k === undefined ? s : k); }
    }
    var kind = cells.map(function (rc) { return GRID[rc[0]].charAt(rc[1]); });
    var sweep = function (V, gamma, slip, pol) { // one application of the Bellman optimality operator
      var out = new Array(n), i, b, q, best;
      for (i = 0; i < n; i++) {
        if (kind[i] === "G") { out[i] = 1; continue; }
        if (kind[i] === "P") { out[i] = -1; continue; }
        best = -1e9;
        for (b = 0; b < 4; b++) {
          q = gamma * ((1 - 2 * slip) * V[next[i][b]] + slip * V[next[i][(b + 1) % 4]] + slip * V[next[i][(b + 3) % 4]]);
          if (q > best + 1e-12) { best = q; if (pol) pol[i] = b; }
        }
        out[i] = best;
      }
      return out;
    };
    var dist = function (A, B) { var m = 0, i; for (i = 0; i < n; i++) m = Math.max(m, Math.abs(A[i] - B[i])); return m; };
    QB.widget(el, {
      title: "Value iteration: the news spreads one step per sweep",
      sub: "The film's gridworld: a goal (+1), a pit (−1), walls, and moves that slip sideways. Every value starts at zero; each sweep applies Bellman's equation to all 44 cells at once. Step through the sweeps, then lower the discount or raise the slip and see how the values and the arrows change.",
      panels: 2, height: 300,
      controls: [
        { k: "k", label: "Sweeps", min: 0, max: 60, step: 1, value: 6 },
        { k: "gamma", label: "Discount γ", min: 0.5, max: 0.99, step: 0.01, value: 0.95, fmt: function (x) { return x.toFixed(2); } },
        { k: "slip", label: "Chance of slipping to each side", min: 0, max: 0.3, step: 0.01, value: 0.1, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, st) {
        var V = new Array(n).fill(0), Vs = [V], i, j, pol = new Array(n).fill(-1);
        for (i = 0; i < 400; i++) { V = sweep(V, v.gamma, v.slip); if (i < 60) Vs.push(V); }
        var star = V, cur = Vs[v.k], errs = [], ks = [], bound = [], e0 = dist(Vs[0], star);
        sweep(cur, v.gamma, v.slip, pol);
        for (i = 0; i <= 60; i++) { ks.push(i); errs.push(Math.max(1e-9, dist(Vs[i], star))); bound.push(Math.max(1e-9, Math.pow(v.gamma, i) * e0)); }
        st.out = [errs[v.k], bound[v.k], cur[index["5,0"]], star[index["5,0"]]];
        // the grid
        var ctx = g[0].ctx, b = g[0].box, cs = Math.min((b.w - 24) / 9, (b.h - 44) / 6), x0 = b.x + (b.w - 9 * cs) / 2, y0 = b.y + 30;
        label(ctx, "Values after " + v.k + " sweep" + (v.k === 1 ? "" : "s") + ", and the greedy moves", b.x + 12, b.y + 14, { bold: true, size: 12.5 });
        for (i = 0; i < 6; i++) for (j = 0; j < 9; j++) {
          var id = index[i + "," + j], X = x0 + j * cs, Y = y0 + i * cs;
          ctx.fillStyle = id === undefined ? "#0b0e14" : heat(cur[id]); ctx.fillRect(X + 1, Y + 1, cs - 2, cs - 2);
          if (id === undefined) continue;
          if (kind[id] === "G" || kind[id] === "P") { label(ctx, kind[id] === "G" ? "+1" : "−1", X + cs / 2, Y + cs / 2, { align: "center", bold: true, color: "#0b0e14", size: 12 }); continue; }
          if (kind[id] === "S") { ctx.strokeStyle = C.idea; ctx.lineWidth = 2; ctx.strokeRect(X + 2, Y + 2, cs - 4, cs - 4); }
          if (Math.abs(cur[id]) < 1e-9) continue; // no news has reached this cell yet
          var m = MOVES[pol[id]], cx = X + cs / 2, cy = Y + cs / 2, L = cs * 0.28;
          ctx.strokeStyle = C.ink; ctx.fillStyle = C.ink; ctx.lineWidth = 1.4; ctx.beginPath();
          ctx.moveTo(cx - m[1] * L, cy - m[0] * L); ctx.lineTo(cx + m[1] * L, cy + m[0] * L); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(cx + m[1] * L, cy + m[0] * L);
          ctx.lineTo(cx + m[1] * L * 0.2 - m[0] * L * 0.5, cy + m[0] * L * 0.2 - m[1] * L * 0.5);
          ctx.lineTo(cx + m[1] * L * 0.2 + m[0] * L * 0.5, cy + m[0] * L * 0.2 + m[1] * L * 0.5); ctx.closePath(); ctx.fill();
        }
        var ax = g[1].axes({ x: [0, 60], y: [1e-8, 2], logy: true, title: "Distance to V* (largest over cells)", xlabel: "sweep", yticks: [1e-8, 1e-6, 1e-4, 1e-2, 1], yfmt: function (y) { return y >= 1 ? "1" : "1e" + Math.round(Math.log(y) / Math.LN10); } });
        ax.line(ks, bound, { color: C.idea, dash: [5, 4], width: 1.4 }).line(ks, errs, { color: C.spot });
        ax.vline(v.k, { color: C.muted });
        ax.dots([v.k], [errs[v.k]], { color: C.spot, r: 4 });
        ax.legend([["value iteration", C.spot], ["the bound γ^k", C.idea]], { pos: "bl" });
      },
      readout: function (v, st) {
        return [["distance to V*", st.out[0] < 1e-8 ? "below 1e-8" : st.out[0].toExponential(1)], ["bound γ^k", st.out[1].toExponential(1)], ["value at the start now", fmt(st.out[2], 3)], ["V* at the start", fmt(st.out[3], 3)]];
      },
      note: "Exact arithmetic on the model, no simulation. Green cells have positive value, red negative; the gold frame is the start; arrows appear once a cell's value is no longer zero. V* is taken after 400 sweeps. The contraction theorem only promises the dashed line; the game ends at the goal or the pit, so the true distance falls faster.",
    });
  };

  // ---- Part 27: the KL leash and a noisy reward ---------------------------------------------------------------
  W.klleash = function (el) {
    var M = 12;
    var tilt = function (ref, r, beta) { // pi* = pi_ref e^(r/beta) / Z, computed stably
      var mx = -1e9, i, out = [], z = 0;
      for (i = 0; i < M; i++) mx = Math.max(mx, r[i] / beta);
      for (i = 0; i < M; i++) { out.push(ref[i] * Math.exp(r[i] / beta - mx)); z += out[i]; }
      for (i = 0; i < M; i++) out[i] /= z;
      return out;
    };
    var kl = function (p, q) { var s = 0, i; for (i = 0; i < M; i++) if (p[i] > 1e-300) s += p[i] * Math.log(p[i] / q[i]); return Math.max(0, s); };
    var dot = function (p, x) { var s = 0, i; for (i = 0; i < M; i++) s += p[i] * x[i]; return s; };
    QB.widget(el, {
      title: "A leash of length 1/β, and a reward that is only a proxy",
      sub: "Twelve candidate answers, each with a hidden gold score and a reward model's score (gold plus noise). The optimum of E[r] − β·KL is the reference policy reweighted by e^(r/β). Shorten the leash's hold by lowering β: the policy piles onto the reward model's favourite. Then raise the noise and watch gold stop following.",
      panels: 2, height: 300,
      controls: [
        { k: "lb", label: "Leash strength β", min: -1.5, max: 1, step: 0.05, value: 0, fmt: function (x) { return Math.pow(10, x).toFixed(x < -1 ? 3 : 2); } },
        { k: "noise", label: "Reward model's noise (gold has sd 1)", min: 0, max: 2, step: 0.05, value: 0.8, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New answers", act: function (s) { s.seed++; } }],
      draw: function (g, v, st) {
        var r = QB.rng(st.seed + 270), gold = [], proxy = [], ref = [], i, z = 0, order = [];
        for (i = 0; i < M; i++) { gold.push(r.normal()); ref.push(Math.exp(0.6 * r.normal())); z += ref[i]; }
        for (i = 0; i < M; i++) { ref[i] /= z; proxy.push(gold[i] + v.noise * r.normal()); order.push(i); }
        order.sort(function (a, b) { return proxy[b] - proxy[a]; });
        var beta = Math.pow(10, v.lb), pi = tilt(ref, proxy, beta), bestGold = 0;
        for (i = 1; i < M; i++) if (gold[i] > gold[bestGold]) bestGold = i;
        var ks = [], ps = [], gs = [], lo = 1e9, hi = -1e9, kmax = 0;
        for (i = 0; i <= 70; i++) {
          var q = tilt(ref, proxy, Math.pow(10, 1.5 - 3.2 * i / 70));
          ks.push(kl(q, ref)); ps.push(dot(q, proxy)); gs.push(dot(q, gold));
          lo = Math.min(lo, ps[i], gs[i]); hi = Math.max(hi, ps[i], gs[i]); kmax = Math.max(kmax, ks[i]);
        }
        st.out = [pi[order[0]], kl(pi, ref), dot(pi, proxy), dot(pi, gold), dot(ref, gold), order[0] === bestGold];
        var xs = [], a1 = [], a2 = [], pmax = 0.3;
        for (i = 0; i < M; i++) { xs.push(i + 1); a1.push(ref[order[i]]); a2.push(pi[order[i]]); pmax = Math.max(pmax, a2[i]); }
        var a = g[0].axes({ x: [0.3, M + 0.7], y: [0, Math.min(1, pmax * 1.15)], title: "Reference and optimum, by the reward model's ranking", xlabel: "answers, the reward model's favourite first", xticks: [1, 3, 5, 7, 9, 11] });
        a.bars(xs.map(function (x) { return x - 0.2; }), a1, 0.4, { color: C.muted, gap: 0 });
        a.bars(xs.map(function (x) { return x + 0.2; }), a2, 0.4, { color: C.idea, gap: 0 });
        var gi = order.indexOf(bestGold) + 1;
        a.vline(gi, { color: C.gain });
        a.legend([["reference", C.muted], ["optimum at this β", C.idea], ["gold's favourite", C.gain]], { pos: "tr" });
        var pad = 0.1 * (hi - lo) + 0.05;
        var b = g[1].axes({ x: [0, Math.max(0.5, kmax * 1.03)], y: [lo - pad, hi + pad], title: "Expected score as the leash loosens", xlabel: "KL from the reference (nats)" });
        b.line(ks, ps, { color: C.implied }).line(ks, gs, { color: C.gain });
        b.vline(st.out[1], { color: C.muted });
        b.dots([st.out[1]], [st.out[2]], { color: C.implied, r: 4 }).dots([st.out[1]], [st.out[3]], { color: C.gain, r: 4 });
        b.legend([["what the reward model believes", C.implied], ["what gold says", C.gain]], { pos: "tl" });
      },
      readout: function (v, st) {
        return [["on the reward model's favourite", QB.pct(st.out[0], 0)], ["KL from the reference", fmt(st.out[1], 2) + " nats"], ["reward model believes", fmt(st.out[2], 2)], ["gold says", fmt(st.out[3], 2) + " (reference " + fmt(st.out[4], 2) + ")"], ["favourites agree", st.out[5] ? "yes" : "no"]];
      },
      note: "Simulated data: gold scores are standard normal, the reward model adds independent normal noise, and the reference policy is random. The optimum is exact for these twelve answers; a trained policy only approximates it.",
    });
  };

  // ---- Part 28: many chains, one vote, and pass@k ---------------------------------------------------------------
  W.votepassk = function (el) {
    var M = 10, KS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256], TRIALS = 300;
    var law = function (v) { // answer 0 is right, answer 1 is the strongest wrong one, the rest share what is left
      var rival = Math.min(v.rival, 1 - v.p), rest = Math.max(0, 1 - v.p - rival) / (M - 2), cum = [v.p, v.p + rival], i;
      for (i = 2; i < M; i++) cum.push(cum[i - 1] + rest);
      return { cum: cum, rival: rival, rest: rest };
    };
    var draw1 = function (r, cum) { var u = r(), i = 0; while (i < M - 1 && u > cum[i]) i++; return i; };
    var vote = function (r, cum, k, counts) { // 1 if the plurality is the right answer; ties are split evenly
      var i, top = 0, ties = 0;
      for (i = 0; i < M; i++) counts[i] = 0;
      for (i = 0; i < k; i++) counts[draw1(r, cum)]++;
      for (i = 0; i < M; i++) { if (counts[i] > top) { top = counts[i]; ties = 1; } else if (counts[i] === top) ties++; }
      return counts[0] === top ? 1 / ties : 0;
    };
    QB.widget(el, {
      title: "Many chains, one vote: what sampling more can and cannot buy",
      sub: "A model answers a question right with probability p; its most likely wrong answer has the probability you set, and eight other wrong answers share the rest. Draw k chains and take the most common answer. While the right answer leads, the vote climbs towards certainty. Push the wrong answer above it and the vote turns confidently wrong, although some chain is still right.",
      panels: 2, height: 300,
      controls: [
        { k: "p", label: "Chance one chain is right", min: 0.05, max: 0.9, step: 0.01, value: 0.45, fmt: function (x) { return QB.pct(x, 0); } },
        { k: "rival", label: "Chance of the strongest wrong answer", min: 0.02, max: 0.6, step: 0.01, value: 0.2, fmt: function (x) { return QB.pct(x, 0); } },
        { k: "k", label: "Chains k", min: 1, max: 256, step: 1, value: 16 },
      ],
      buttons: [{ label: "New chains", act: function (s) { s.seed++; } }],
      draw: function (g, v, st) {
        var L = law(v), r = QB.rng(st.seed * 7 + 28), counts = new Array(M), i, t, s;
        vote(r, L.cum, v.k, counts);
        var shown = counts.slice(), top = 0;
        for (i = 0; i < M; i++) top = Math.max(top, shown[i]);
        var accs = [], any = [], bound = [], gap = v.p - Math.max(L.rival, L.rest);
        for (i = 0; i < KS.length; i++) {
          for (s = 0, t = 0; t < TRIALS; t++) s += vote(r, L.cum, KS[i], counts);
          accs.push(s / TRIALS); any.push(1 - Math.pow(1 - v.p, KS[i]));
          bound.push(gap > 0 ? Math.max(0, 1 - (M - 1) * Math.exp(-KS[i] * gap * gap / 2)) : null);
        }
        for (s = 0, t = 0; t < TRIALS; t++) s += vote(r, L.cum, v.k, counts);
        st.out = [s / TRIALS, 1 - Math.pow(1 - v.p, v.k), gap, L.rival, gap > 0 ? Math.max(0, 1 - (M - 1) * Math.exp(-v.k * gap * gap / 2)) : -1];
        var xs = []; for (i = 0; i < M; i++) xs.push(i + 1);
        var a = g[0].axes({ x: [0.3, M + 0.7], y: [0, Math.max(4, top * 1.25)], title: "One draw of " + v.k + " chain" + (v.k === 1 ? "" : "s") + ": how many gave each answer", xlabel: "answer", xticks: xs, xfmt: function (x) { return x === 1 ? "right" : x === 2 ? "rival" : String(x); } });
        a.bars(xs, shown, 0.7, { color: function (j) { return j === 0 ? C.gain : j === 1 ? C.loss : C.cash; } });
        a.legend([["the right answer", C.gain], ["the strongest wrong answer", C.loss], ["other wrong answers", C.cash]], { pos: "tr" });
        var b = g[1].axes({ x: [1, 256], y: [0, 1.02], logx: true, title: "Against the number of chains", xlabel: "chains k (log scale)", xticks: [1, 4, 16, 64, 256], xfmt: function (x) { return String(x); }, yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.line(KS, bound, { color: C.muted, dash: [4, 4], width: 1.3 });
        b.line(KS, any, { color: C.idea }).line(KS, accs, { color: C.spot });
        b.vline(v.k, { color: C.muted });
        b.legend([["some chain is right (pass@k)", C.idea], ["the vote is right", C.spot], ["Hoeffding's guarantee for the vote", C.muted]], { pos: gap > 0 ? "bl" : "tr" });
      },
      readout: function (v, st) {
        return [["one chain", QB.pct(v.p, 0)], ["vote of " + v.k, QB.pct(st.out[0], 0)], ["some chain right", QB.pct(st.out[1], 1)], ["lead over the best wrong answer Δ", fmt(st.out[2], 2)], ["guarantee", st.out[4] < 0 ? "none (Δ ≤ 0)" : QB.pct(st.out[4], 0)]];
      },
      note: "Simulated: 300 votes per point, chains drawn independently. The guarantee is 1 − (m − 1)·exp(−kΔ²/2) for m = 10 answers, from Hoeffding's inequality and a union bound; it is loose but it only needs Δ > 0. Pass@k is exact: 1 − (1 − p)^k. It assumes a checker that can recognize the right chain.",
    });
  };

  // ---- Part 29: errors compound over a long task ----------------------------------------------------------------
  W.horizondecay = function (el) {
    var RUNS = 40;
    QB.widget(el, {
      title: "Many steps in a row: how reliability sets the horizon",
      sub: "Forty simulated runs of one task. Every step succeeds with the reliability you set; a slip ends the run unless a check catches it and the step is retried. Lengthen the task and watch the runs die off as pⁿ; then raise the reliability by one point, or let checks catch half the slips, and see how far the half-way horizon moves.",
      panels: 2, height: 300,
      controls: [
        { k: "p", label: "Reliability of one step", min: 0.9, max: 0.999, step: 0.001, value: 0.97, fmt: function (x) { return QB.pct(x, 1); } },
        { k: "n", label: "Steps in the task", min: 5, max: 300, step: 1, value: 30 },
        { k: "c", label: "Share of slips a check catches", min: 0, max: 0.9, step: 0.05, value: 0, fmt: function (x) { return QB.pct(x, 0); } },
      ],
      buttons: [{ label: "New runs", act: function (s) { s.seed++; } }],
      draw: function (g, v, st) {
        var r = QB.rng(st.seed + 290), n = v.n, pe = 1 - (1 - v.p) * (1 - v.c), i, t, alive = 0;
        var ctx = g[0].ctx, b = g[0].box, x0 = b.x + 14, y0 = b.y + 32, w = b.w - 28, h = b.h - 76, rh = h / RUNS;
        label(ctx, "Forty runs of a " + n + "-step task", b.x + 14, b.y + 14, { bold: true, size: 12.5 });
        for (i = 0; i < RUNS; i++) {
          var fail = n, caught = [];
          for (t = 0; t < n; t++) if (r() > v.p) { if (r() < v.c) caught.push(t); else { fail = t; break; } }
          if (fail === n) alive++;
          var Y = y0 + i * rh, xf = x0 + w * fail / n;
          ctx.fillStyle = C.spot; ctx.globalAlpha = 0.85; ctx.fillRect(x0, Y + 0.5, xf - x0, Math.max(1, rh - 1.5));
          if (fail < n) { ctx.fillStyle = C.loss; ctx.globalAlpha = 0.45; ctx.fillRect(xf, Y + 0.5, x0 + w - xf, Math.max(1, rh - 1.5)); }
          ctx.globalAlpha = 1; ctx.fillStyle = C.idea;
          for (t = 0; t < caught.length; t++) ctx.fillRect(x0 + w * caught[t] / n - 0.5, Y + 0.5, 2, Math.max(1, rh - 1.5));
        }
        ctx.globalAlpha = 1;
        label(ctx, "step 1", x0, y0 + h + 12, { color: C.muted, size: 11 });
        label(ctx, "step " + n, x0 + w, y0 + h + 12, { color: C.muted, size: 11, align: "right" });
        label(ctx, "blue: on track   red: went wrong   gold: slip caught", x0 + w / 2, y0 + h + 28, { color: C.muted, size: 11, align: "center" });
        var ns = [], raw = [], chk = [];
        for (i = 0; i <= 120; i++) { var m = Math.pow(1000, i / 120); ns.push(m); raw.push(Math.pow(v.p, m)); chk.push(Math.pow(pe, m)); }
        var half = Math.LN2 / -Math.log(v.p), halfc = Math.LN2 / -Math.log(pe);
        st.out = [Math.pow(v.p, n), Math.pow(pe, n), half, halfc, alive];
        var a = g[1].axes({ x: [1, 1000], y: [0, 1.02], logx: true, title: "Chance the whole task goes right", xlabel: "steps in the task (log scale)", yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        a.hline(0.5, { color: C.muted });
        a.line(ns, raw, { color: C.loss });
        if (v.c > 0) a.line(ns, chk, { color: C.gain });
        a.vline(n, { color: C.idea });
        a.dots([n], [v.c > 0 ? st.out[1] : st.out[0]], { color: v.c > 0 ? C.gain : C.loss, r: 4 });
        a.legend(v.c > 0 ? [["no checks: pⁿ", C.loss], ["with checks", C.gain], ["this task", C.idea]] : [["pⁿ", C.loss], ["this task", C.idea]], { pos: "bl" });
      },
      readout: function (v, st) {
        var out = [["runs that reach the end", st.out[4] + " of " + RUNS], ["pⁿ", QB.pct(st.out[0], 1)], ["half-way horizon ln 2 / (−ln p)", fmt(st.out[2], 1) + " steps"]];
        if (v.c > 0) { out.push(["with checks", QB.pct(st.out[1], 1)]); out.push(["horizon with checks", fmt(st.out[3], 1) + " steps"]); }
        return out;
      },
      note: "Simulated runs; steps fail independently with the same probability, which real tasks need not obey. A check that catches a share c of slips turns p into 1 − (1 − p)(1 − c). The half-way horizon is the task length at which half the runs succeed, about 0.69 / (1 − p).",
    });
  };

  // ---- Part 30: superposition, n features in two dimensions -----------------------------------------------------
  W.superpolygon = function (el) {
    var SAMPLES = 300, DENS = [];
    (function () { for (var i = 0; i <= 24; i++) DENS.push(Math.pow(10, -2 + 2 * i / 24)); })();
    var gram = function (n) { // cosines between n directions spread evenly round the circle
      var G = [], i, j; for (i = 0; i < n; i++) { G.push([]); for (j = 0; j < n; j++) G[i].push(Math.cos(2 * Math.PI * (i - j) / n)); } return G;
    };
    var polyLoss = function (n, G, bias, rho, U, S) { // mean squared error per feature of ReLU(W'Wx + b), by simulation
      var tot = 0, t, i, j, x = new Array(n), y;
      for (t = 0; t < SAMPLES; t++) {
        for (i = 0; i < n; i++) x[i] = S[t * 8 + i] < rho ? U[t * 8 + i] : 0;
        for (j = 0; j < n; j++) { y = bias; for (i = 0; i < n; i++) if (x[i] !== 0) y += G[j][i] * x[i]; y = y > 0 ? y : 0; tot += (y - x[j]) * (y - x[j]); }
      }
      return tot / (SAMPLES * n);
    };
    QB.widget(el, {
      title: "More ideas than dimensions: when sharing two numbers pays",
      sub: "A network must pass n features through two numbers and rebuild them with ReLU(WᵀWx + b). It can give two features their own perpendicular directions and drop the rest, or spread all n round a circle and accept interference. Make the features rare and sharing wins; make them common and it loses. The bias trades a feature's own reading against the leak into its neighbours.",
      panels: 2, height: 310,
      controls: [
        { k: "n", label: "Features n", min: 3, max: 8, step: 1, value: 5 },
        { k: "lr", label: "Chance a feature is on", min: -2, max: 0, step: 0.05, value: -1.3, fmt: function (x) { return QB.pct(Math.pow(10, x), 1); } },
        { k: "bias", label: "Bias b", min: -0.6, max: 0.1, step: 0.01, value: -0.25, fmt: function (x) { return fmt(x, 2); } },
      ],
      draw: function (g, v, st) {
        var n = v.n, G = gram(n), rho = Math.pow(10, v.lr), r = QB.rng(300), U = [], S = [], i, j;
        for (i = 0; i < SAMPLES * 8; i++) { U.push(r()); S.push(r()); }
        var variance = function (q) { return q / 3 - q * q / 4; }; // of a feature that is uniform on [0, 1] when on
        var shared = [], ded = [], lo = 1e9, hi = 0;
        for (i = 0; i < DENS.length; i++) {
          shared.push(Math.max(1e-6, polyLoss(n, G, v.bias, DENS[i], U, S))); ded.push(Math.max(1e-6, (n - 2) / n * variance(DENS[i])));
          lo = Math.min(lo, shared[i], ded[i]); hi = Math.max(hi, shared[i], ded[i]);
        }
        var here = polyLoss(n, G, v.bias, rho, U, S), hereDed = (n - 2) / n * variance(rho), read = [], leak = 0;
        for (j = 0; j < n; j++) { read.push(Math.max(0, G[j][0] + v.bias)); if (j > 0) leak = Math.max(leak, read[j]); }
        st.out = [here, hereDed, read[0], leak];
        // the directions, and what each output reads when feature 1 alone is fully on
        var ctx = g[0].ctx, b = g[0].box, cx = b.x + b.w / 2, cy = b.y + 26 + (b.h - 34) / 2, R = Math.min(b.w / 2 - 58, (b.h - 34) / 2 - 26);
        label(ctx, "Feature 1 on alone: what each output reads", b.x + 12, b.y + 14, { bold: true, size: 12.5 });
        ctx.strokeStyle = C.line; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(cx, cy, R, 0, 6.2832); ctx.stroke();
        for (j = 0; j < n; j++) {
          var ang = -Math.PI / 2 + 2 * Math.PI * j / n, ex = cx + R * Math.cos(ang), ey = cy + R * Math.sin(ang), col = j === 0 ? C.idea : read[j] > 0.005 ? C.loss : C.spot;
          ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = j === 0 ? 2.6 : 1.8; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(ex, ey); ctx.stroke();
          ctx.beginPath(); ctx.arc(ex, ey, 3.5, 0, 6.2832); ctx.fill();
          label(ctx, (j === 0 ? "1: " : "") + read[j].toFixed(2), cx + (R + 24) * Math.cos(ang), cy + (R + 15) * Math.sin(ang), { align: "center", color: col, bold: j === 0 });
        }
        label(ctx, "gold: feature 1 (should read 1)   red: a leak   blue: reads 0", b.x + b.w / 2, b.y + b.h - 8, { align: "center", color: C.muted, size: 11 });
        var ylo = Math.pow(10, Math.floor(Math.log(Math.max(lo, 1e-6)) / Math.LN10)), yhi = Math.pow(10, Math.ceil(Math.log(hi) / Math.LN10));
        if (yhi <= ylo) yhi = ylo * 10;
        var a = g[1].axes({ x: [0.01, 1], y: [ylo, yhi], logx: true, logy: true, title: "Error per feature against density", xlabel: "chance a feature is on (log scale)", xfmt: function (x) { return Math.round(100 * x) + "%"; }, yfmt: function (y) { return y >= 0.01 ? String(+y.toPrecision(1)) : "1e" + Math.round(Math.log(y) / Math.LN10); } });
        a.line(DENS, ded, { color: C.spot }).line(DENS, shared, { color: C.idea });
        a.vline(rho, { color: C.muted });
        a.dots([rho], [Math.max(1e-6, here)], { color: C.idea, r: 4 }).dots([rho], [Math.max(1e-6, hereDed)], { color: C.spot, r: 4 });
        a.legend([["all n share the plane (superposition)", C.idea], ["two kept, the rest dropped", C.spot]], { pos: "br" });
      },
      readout: function (v, st) {
        return [["error when sharing", st.out[0].toFixed(4)], ["error when dropping n − 2", st.out[1].toFixed(4)], ["better here", st.out[0] < st.out[1] ? "sharing" : "dropping"], ["feature 1 reads", fmt(st.out[2], 2)], ["largest leak", fmt(st.out[3], 2)]];
      },
      note: "Simulated data: each feature is on independently and uniform on [0, 1] when on, all equally important; 300 samples per point. The shared layout is fixed to unit directions evenly spaced, with the bias you set; a trained network also tunes the lengths, so it does a little better. Dropped features are answered with their mean.",
    });
  };

  // ---- Part 31: the control game ----------------------------------------------------------------------------
  W.redteamaudit = function (el) {
    var N = 5000, PS = [];
    (function () { for (var i = 0; i <= 100; i++) PS.push(Math.pow(10, -5 + 5 * i / 100)); })();
    QB.widget(el, {
      title: "The control game: a monitor, an audit budget, and a model that may be attacking",
      sub: "An untrusted model solves 5,000 problems and may hide a backdoor in any of them. A trusted monitor scores each solution's suspicion, and people audit the most suspicious share. Red wins if a backdoor gets through and works before any attack is caught. Move the monitor's separation and the audit budget: against auditing only the first problems, red waits; against monitoring, waiting does not help.",
      panels: 2, height: 300,
      controls: [
        { k: "mu", label: "How far backdoored code stands out (sd)", min: 0, max: 4, step: 0.1, value: 2, fmt: function (x) { return x.toFixed(1); } },
        { k: "audit", label: "Share people can audit", min: 0.5, max: 10, step: 0.5, value: 2, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "s", label: "Chance an unnoticed backdoor works", min: 0.05, max: 1, step: 0.05, value: 0.3, fmt: function (x) { return QB.pct(x, 0); } },
      ],
      draw: function (g, v, st) {
        var cut = QB.inv(1 - v.audit / 100), q = Math.min(0.999999, Math.max(1e-6, 1 - QB.cdf(cut - v.mu))), m = Math.round(v.audit / 100 * N), i;
        var up = [], tm = [], bu = 0, bt = 0, pu = PS[0];
        for (i = 0; i < PS.length; i++) {
          var p = PS[i], c = p * q, w = p * (1 - q) * v.s;
          up.push(Math.pow(1 - p, m) * (1 - Math.pow(1 - p * v.s, N - m)));
          tm.push(w / (c + w) * (1 - Math.pow(1 - c - w, N)));
          if (up[i] > bu) { bu = up[i]; pu = p; }
          bt = Math.max(bt, tm[i]);
        }
        st.out = [q, 1 - bu, 1 - bt, pu, cut];
        var xs = QB.linspace(-3.5, 7.5, 140), honest = xs.map(function (x) { return QB.pdf(x); }), bad = xs.map(function (x) { return QB.pdf(x - v.mu); });
        var a = g[0].axes({ x: [-3.5, 7.5], y: [0, 0.48], title: "What the monitor sees", xlabel: "suspicion score", noY: true });
        var tail = xs.filter(function (x) { return x >= cut; });
        if (tail.length > 1) a.area(tail, tail.map(function (x) { return QB.pdf(x - v.mu); }), 0, { color: C.loss, alpha: 0.35 });
        a.line(xs, honest, { color: C.spot }).line(xs, bad, { color: C.loss });
        a.vline(cut, { color: C.idea });
        a.legend([["honest code", C.spot], ["backdoored code", C.loss], ["audit above this line", C.idea]], { pos: "tr" });
        var b = g[1].axes({ x: [1e-5, 1], y: [0, 1.02], logx: true, title: "Red's chance of winning", xlabel: "how often red attacks, per problem (log scale)", xticks: [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1], xfmt: function (x) { return x >= 0.01 ? Math.round(100 * x) + "%" : x >= 1e-3 ? "0.1%" : x >= 1e-4 ? "0.01%" : "0.001%"; }, yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.line(PS, up, { color: C.implied }).line(PS, tm, { color: C.realized });
        b.dots([pu], [bu], { color: C.implied, r: 4 });
        b.hline(bt, { color: C.realized });
        b.legend([["audit the first " + m + " problems only", C.implied], ["monitor every problem", C.realized]], { pos: "tl" });
      },
      readout: function (v, st) {
        return [["an attack is caught, q", QB.pct(st.out[0], 0)], ["safety, upfront auditing", QB.pct(st.out[1], 0)], ["safety, trusted monitoring", QB.pct(st.out[2], 0)], ["red's best rate against upfront auditing", (100 * st.out[3]).toPrecision(2) + "%"]];
      },
      note: "Exact formulas, no simulation: suspicion of honest code is N(0, 1) and of backdoored code N(μ, 1); the cutoff flags the chosen share of honest code. Under monitoring P(red wins) = w/(c + w)·(1 − (1 − c − w)^N) with c = pq and w = p(1 − q)s, which levels off at (1 − q)s / (q + (1 − q)s). Safety is one minus red's best result. As in the film, there is no hard cap on audits.",
    });
  };
})();
