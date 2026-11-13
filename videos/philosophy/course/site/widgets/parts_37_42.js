// Interactives for Act VII, Value, concluded, and the Finale (Parts 37-42).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  function label(ctx, str, x, y, o) { // a line of text on the bare canvas
    o = o || {};
    ctx.save(); ctx.font = (o.bold ? "600 " : "") + (o.size || 11.5) + "px system-ui, sans-serif";
    ctx.fillStyle = o.color || C.ink; ctx.textAlign = o.align || "left"; ctx.textBaseline = o.base || "middle";
    ctx.fillText(str, x, y); ctx.restore();
  }

  // ---- Part 37: reflective equilibrium as weighted MaxSAT ----------------------------------------------------
  W.maxsatethics = function (el) {
    var names = [["U", "maximize welfare"], ["D", "never kill"], ["DDE", "double effect"], ["S", "may switch"], ["F", "may not push"], ["H", "may not harvest"]];
    var sets = [["welfare", [0, 3]], ["never kill", [1, 4, 5]], ["double effect", [2, 3, 4, 5]]]; // the maximal consistent sets
    QB.widget(el, {
      title: "Reflective equilibrium: which commitments survive?",
      sub: "Three principles and three trolley judgments, each with a weight for how confident we are. The links between them leave three consistent camps, and the equilibrium is the heaviest. Start from the film's weights, then lower 'may not push' to 1 and 'may not harvest' to 2 and raise welfare to 6, as Greene's argument urges: double effect gives way to welfare.",
      panels: 2, height: 300,
      controls: [
        { k: "u", label: "U: maximize total welfare", min: 0, max: 10, step: 1, value: 3 },
        { k: "d", label: "D: never kill an innocent", min: 0, max: 10, step: 1, value: 3 },
        { k: "f", label: "F: pushing the man is forbidden", min: 0, max: 10, step: 1, value: 5 },
        { k: "h", label: "H: the surgeon may not harvest", min: 0, max: 10, step: 1, value: 5 },
      ],
      draw: function (g, v, s) {
        var w = [v.u, v.d, 2, 4, v.f, v.h], tot = [0, 0, 0], best = 0, i, j, all = 0;
        for (i = 0; i < 6; i++) all += w[i];
        for (i = 0; i < 3; i++) { for (j = 0; j < sets[i][1].length; j++) tot[i] += w[sets[i][1][j]]; best = Math.max(best, tot[i]); }
        var win = [], keep = [false, false, false, false, false, false];
        for (i = 0; i < 3; i++) if (tot[i] === best) win.push(i);
        for (j = 0; j < sets[win[0]][1].length; j++) keep[sets[win[0]][1][j]] = true;
        s.out = { tot: tot, best: best, all: all, win: win, keep: keep };
        var c = g.ctx, b = g[0].box, x0 = b.x + 14, top = b.y + 34, rowH = (b.h - 50) / 6, lab = 138, bw = Math.max(40, b.w - lab - 52);
        label(c, "Commitments: kept (green) or given up (red)", x0, b.y + 14, { bold: true, size: 12.5 });
        for (i = 0; i < 6; i++) {
          var y = top + rowH * i + rowH / 2, col = keep[i] ? C.gain : C.loss;
          label(c, names[i][0], x0, y, { bold: true, color: col });
          label(c, names[i][1], x0 + 32, y, { color: keep[i] ? C.ink : C.muted });
          c.fillStyle = C.line; c.fillRect(x0 + lab, y - 7, bw, 14);
          c.globalAlpha = keep[i] ? 0.9 : 0.45; c.fillStyle = col; c.fillRect(x0 + lab, y - 7, bw * w[i] / 10, 14); c.globalAlpha = 1;
          label(c, String(w[i]), x0 + lab + bw + 8, y, { color: C.muted });
          if (i === 2) { c.strokeStyle = C.line; c.beginPath(); c.moveTo(x0, y + rowH / 2); c.lineTo(b.x + b.w - 14, y + rowH / 2); c.stroke(); }
        }
        var a = g[1].axes({ x: [0.4, 3.6], y: [0, 32], title: "Total weight of each consistent camp", xticks: [1, 2, 3], xfmt: function (x) { return sets[x - 1][0]; } });
        a.bars([1, 2, 3], tot, 0.6, { color: function (k) { return tot[k] === best ? C.idea : C.spot; }, alpha: 0.85 });
        for (i = 0; i < 3; i++) a.text(i + 1, tot[i], String(tot[i]), { align: "center", dy: -9, color: tot[i] === best ? C.idea : C.muted, bold: tot[i] === best });
        a.legend([["the equilibrium", C.idea], ["a consistent camp that loses", C.spot]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out, kept = [], i;
        for (i = 0; i < 6; i++) if (o.keep[i]) kept.push(names[i][0]);
        return [["equilibrium", o.win.length > 1 ? "a tie: " + o.win.map(function (k) { return sets[k][0]; }).join(" and ") : sets[o.win[0]][0]],
          ["keeps", kept.join(", ")], ["weight kept", o.best + " of " + o.all], ["weight given up", String(o.all - o.best)]];
      },
      note: "The film's model: links U → S, ¬F, ¬H; D → ¬S, F, H; DDE → S, F, H are hard constraints, the weights of DDE (2) and S (4) are fixed here, and all weights are invented. Every consistent set of commitments lies inside one of the three camps, so the heaviest camp is the weighted MaxSAT answer. On a tie the first camp's commitments are coloured.",
    });
  };

  // ---- Part 38: the choice behind the veil, as risk aversion grows --------------------------------------------
  W.veilchooser = function (el) {
    var K = 5, N = 150;
    var ce = function (w, eta) { // the certainty equivalent of an equal chance of each class, under CRRA utility
      var i, a = 0;
      if (Math.abs(eta - 1) < 1e-9) { for (i = 0; i < K; i++) a += Math.log(w[i]); return Math.exp(a / K); }
      for (i = 0; i < K; i++) a += Math.pow(w[i], 1 - eta);
      return Math.pow(a / K, 1 / (1 - eta));
    };
    QB.widget(el, {
      title: "Behind the veil: which society would you choose?",
      sub: "Each dot is a society of five equal classes; you will land in one class at random. Gold is the choice of an expected-utility maximizer with risk aversion η. At η = 0 it is Harsanyi's average (red ring); raise η and it walks to Rawls's maximin society (green ring). Set the growth that inequality buys to zero and the two nearly agree.",
      panels: 2, height: 300,
      controls: [
        { k: "eta", label: "Risk aversion η", min: 0, max: 20, step: 0.25, value: 0, fmt: function (x) { return x.toFixed(2); } },
        { k: "g", label: "Growth that inequality buys", min: 0, max: 1.5, step: 0.05, value: 0.8, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New societies", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 1971), soc = [], avg = [], mn = [], i, k, iA = 0, iM = 0, iE = 0, best = -1;
        for (i = 0; i < N; i++) {
          var base = 10 + 20 * r(), sp = r(), raw = [], tot = 0;
          for (k = 0; k < K; k++) { raw.push(Math.exp(1.1 * sp * r.normal())); tot += raw[k]; }
          raw.sort(function (a, b) { return a - b; });
          var w = raw.map(function (x) { return 1 + base * K * (1 + v.g * sp) * x / tot; });
          soc.push(w); avg.push(QB.mean(w)); mn.push(w[0]);
          if (avg[i] > avg[iA]) iA = i;
          if (mn[i] > mn[iM]) iM = i;
          var c = ce(w, v.eta); if (c > best) { best = c; iE = i; }
        }
        s.out = { a: [avg[iA], mn[iA]], m: [avg[iM], mn[iM]], e: [avg[iE], mn[iE]], ce: best, same: iE === iA ? "the average chooser's" : iE === iM ? "the maximin chooser's" : "neither" };
        var a = g[0].axes({ x: [10, 75], y: [0, 50], title: "150 societies: average and least income", xlabel: "average income" });
        a.dots(avg, mn, { color: C.cash, r: 2.2, alpha: 0.7 });
        var ring = function (i, col) { var c = a.ctx; c.save(); c.strokeStyle = col; c.lineWidth = 2; c.beginPath(); c.arc(a.px(avg[i]), a.py(mn[i]), 8, 0, 6.2832); c.stroke(); c.restore(); };
        ring(iA, C.loss); ring(iM, C.gain);
        a.dots([avg[iE]], [mn[iE]], { color: C.idea, r: 5 });
        a.legend([["chosen at this η", C.idea], ["highest average", C.loss], ["highest least income", C.gain]], { pos: "tl" });
        var top = 0; for (k = 0; k < K; k++) top = Math.max(top, soc[iA][k], soc[iM][k], soc[iE][k]);
        var b = g[1].axes({ x: [0.4, 5.6], y: [0, Math.ceil(top / 20) * 20], title: "The five classes of the three societies", xlabel: "class, poorest to richest", xticks: [1, 2, 3, 4, 5] });
        var xs = [1, 2, 3, 4, 5];
        b.bars(xs.map(function (x) { return x - 0.27; }), soc[iA], 0.25, { color: C.loss, alpha: 0.75 });
        b.bars(xs, soc[iE], 0.25, { color: C.idea, alpha: 0.95 });
        b.bars(xs.map(function (x) { return x + 0.27; }), soc[iM], 0.25, { color: C.gain, alpha: 0.75 });
        b.hline(best, { color: C.idea });
        b.text(0.5, best, "certain income worth the same", { color: C.idea, dy: -9, bg: true });
      },
      readout: function (v, s) {
        var o = s.out, pr = function (p) { return "(" + fmt(p[0], 1) + ", " + fmt(p[1], 1) + ")"; };
        return [["chosen (average, least)", pr(o.e)], ["it is", o.same], ["average chooser", pr(o.a)], ["maximin chooser", pr(o.m)], ["certainty equivalent", fmt(o.ce, 1)]];
      },
      note: "Simulated data, in the manner of the film's two hundred societies: total income grows with a society's inequality at the rate set by the second slider. Utility is CRRA, u(w) = (w^(1−η) − 1)/(1 − η), log at η = 1; the certainty equivalent is the sure income with the same expected utility, and falls to the least income as η grows.",
    });
  };

  // ---- Part 39: one set of ballots, five rules ----------------------------------------------------------------
  W.fivewinners = function (el) {
    var orders = ["ADECB", "BEDCA", "CBEDA", "DCEBA", "EBDCA", "ECDBA"], cand = "ABCDE";
    var col = { A: C.spot, B: C.idea, C: C.gain, D: C.option, E: C.implied };
    var rules = ["plurality", "two-round runoff", "instant runoff", "Borda count", "Condorcet"];
    var firsts = function (cnt, alive) { // first-place votes among the candidates still standing
      var f = {}, i, k; for (k = 0; k < alive.length; k++) f[alive[k]] = 0;
      for (i = 0; i < 6; i++) for (k = 0; k < 5; k++) if (alive.indexOf(orders[i][k]) >= 0) { f[orders[i][k]] += cnt[i]; break; }
      return f;
    };
    var top = function (f, keys, lowest) { // the best (or worst) candidate; ties go to the earlier letter
      var b = keys[0], k; for (k = 1; k < keys.length; k++) if (lowest ? f[keys[k]] < f[b] : f[keys[k]] > f[b]) b = keys[k];
      return b;
    };
    var count = function (cnt) {
      var all = cand.split(""), n = 0, i, k, j, f = firsts(cnt, all), out = {};
      for (i = 0; i < 6; i++) n += cnt[i];
      out.n = n; out.first = f; out.win = [top(f, all)];
      var a = top(f, all), rest = all.filter(function (x) { return x !== a; }), b = top(f, rest), f2 = firsts(cnt, [a, b].sort());
      out.win.push(f2[a] >= f2[b] ? a : b);
      var alive = all.slice();
      while (alive.length > 1) { var fr = firsts(cnt, alive), lead = top(fr, alive); if (2 * fr[lead] > n) { alive = [lead]; break; } var drop = top(fr, alive.slice().reverse(), true); alive = alive.filter(function (x) { return x !== drop; }); }
      out.win.push(alive[0]);
      var bo = {}; for (k = 0; k < 5; k++) bo[cand[k]] = 0;
      for (i = 0; i < 6; i++) for (k = 0; k < 5; k++) bo[orders[i][k]] += cnt[i] * (4 - k);
      out.borda = bo; out.win.push(top(bo, all));
      var cw = null;
      for (k = 0; k < 5 && !cw; k++) {
        var ok = true;
        for (j = 0; j < 5 && ok; j++) if (j !== k) { var pro = 0; for (i = 0; i < 6; i++) if (orders[i].indexOf(cand[k]) < orders[i].indexOf(cand[j])) pro += cnt[i]; if (2 * pro <= n) ok = false; }
        if (ok) cw = cand[k];
      }
      out.win.push(cw);
      return out;
    };
    QB.widget(el, {
      title: "One election, five rules: who won?",
      sub: "Six blocs of voters rank five candidates; the film's 55 voters give a different winner under each rule. Change the size of the three largest blocs and watch the winners merge or split. The Condorcet row is empty when the majority cycles or ties.",
      panels: 2, height: 310,
      controls: [
        { k: "a", label: "Voters ranking A D E C B", min: 0, max: 30, step: 1, value: 18 },
        { k: "b", label: "Voters ranking B E D C A", min: 0, max: 30, step: 1, value: 12 },
        { k: "c", label: "Voters ranking C B E D A", min: 0, max: 30, step: 1, value: 10 },
      ],
      draw: function (g, v, s) {
        var o = count([v.a, v.b, v.c, 9, 4, 2]), c = g.ctx, b = g[0].box, i, k;
        var seen = {}, distinct = 0; for (i = 0; i < 5; i++) if (o.win[i] && !seen[o.win[i]]) { seen[o.win[i]] = 1; distinct++; }
        s.out = o; s.distinct = distinct;
        var x0 = b.x + 14, top0 = b.y + 36, rowH = (b.h - 52) / 5;
        label(c, "The winner under each rule", x0, b.y + 14, { bold: true, size: 12.5 });
        for (i = 0; i < 5; i++) {
          var y = top0 + rowH * i + rowH / 2, w = o.win[i];
          label(c, rules[i], x0, y, { size: 12 });
          c.beginPath(); c.arc(x0 + 136, y, 13, 0, 6.2832);
          if (w) { c.fillStyle = col[w]; c.fill(); label(c, w, x0 + 136, y + 0.5, { align: "center", bold: true, size: 13, color: C.bg }); }
          else { c.strokeStyle = C.muted; c.setLineDash([3, 3]); c.stroke(); c.setLineDash([]); }
          var detail = i === 0 ? o.first[w] + " first places" : i === 3 ? o.borda[w] + " points" : i === 4 ? (w ? "beats all four" : "no one beats all") : "";
          if (detail && b.w > 300) label(c, detail, x0 + 158, y, { color: C.muted, size: 11 });
        }
        var a = g[1].axes({ x: [0.4, 5.6], y: [0, 100], title: "First places and Borda points (share)", xticks: [1, 2, 3, 4, 5], xfmt: function (x) { return cand[x - 1]; }, yfmt: function (y) { return y + "%"; } });
        var xs = [1, 2, 3, 4, 5], n = Math.max(1, o.n);
        a.bars(xs.map(function (x) { return x - 0.2; }), xs.map(function (x) { return 100 * o.first[cand[x - 1]] / n; }), 0.36, { color: function (k) { return col[cand[k]]; }, alpha: 0.95 });
        a.bars(xs.map(function (x) { return x + 0.2; }), xs.map(function (x) { return 100 * o.borda[cand[x - 1]] / (4 * n); }), 0.36, { color: function (k) { return col[cand[k]]; }, alpha: 0.45 });
        a.hline(50, { color: C.muted });
        a.text(5.55, 92, "solid: first places   pale: Borda", { align: "right", color: C.muted, bg: true });
      },
      readout: function (v, s) {
        return [["voters", String(s.out.n)], ["winners", s.out.win.map(function (w) { return w || "none"; }).join(", ")], ["different winners", String(s.distinct)]];
      },
      note: "The three smaller blocs are fixed: 9 voters rank D C E B A, 4 rank E B D C A and 2 rank E C D B A. Ties are broken alphabetically, as in the film; instant runoff stops as soon as someone holds a majority of the ballots. Each candidate has one colour throughout.",
    });
  };

  // ---- Part 40: the dissonance curve of two complex tones -----------------------------------------------------
  W.roughnessdips = function (el) {
    var BASE = 261.63, just = [[6, 5], [5, 4], [4, 3], [3, 2], [5, 3], [2, 1]];
    var pair = function (f1, f2, a1, a2) { // Plomp and Levelt's roughness of two partials, in Sethares's form
      var lo = Math.min(f1, f2), d = Math.abs(f2 - f1), sc = 0.24 / (0.0207 * lo + 18.96);
      return Math.min(a1, a2) * (Math.exp(-3.5 * sc * d) - Math.exp(-5.75 * sc * d));
    };
    var rough = function (f, a, r) {
      var n = f.length, F = [], A = [], i, j, t = 0;
      for (i = 0; i < n; i++) { F.push(f[i]); A.push(a[i]); }
      for (i = 0; i < n; i++) { F.push(f[i] * r); A.push(a[i]); }
      for (i = 0; i < 2 * n; i++) for (j = i + 1; j < 2 * n; j++) t += pair(F[i], F[j], A[i], A[j]);
      return t;
    };
    QB.widget(el, {
      title: "Why some intervals sound smooth",
      sub: "Two tones, each a stack of partials, sound together; the curve is their total roughness at every interval. With harmonic partials the dips sit on the whole-number ratios (dotted). Reduce the tones to one partial and the dips vanish; stretch the partials and the dips leave the ratios and follow the timbre.",
      panels: 2, height: 300,
      controls: [
        { k: "n", label: "Partials in each tone", min: 1, max: 8, step: 1, value: 6 },
        { k: "st", label: "Second partial at (2 = harmonic)", min: 1.8, max: 2.3, step: 0.01, value: 2, fmt: function (x) { return x.toFixed(2) + " × f"; } },
        { k: "r", label: "Interval sounded", min: 1, max: 2.3, step: 0.005, value: 1.5, fmt: function (x) { return x.toFixed(3); } },
      ],
      draw: function (g, v, s) {
        var e = Math.log(v.st) / Math.LN2, f = [], amp = [], k, i;
        for (k = 1; k <= v.n; k++) { f.push(BASE * Math.pow(k, e)); amp.push(Math.pow(0.88, k - 1)); }
        var rs = QB.linspace(1, 2.3, 391), d = [], mx = 1e-9, imin = 30;
        for (i = 0; i < rs.length; i++) { d.push(rough(f, amp, rs[i])); mx = Math.max(mx, d[i]); }
        for (i = 30; i < rs.length; i++) if (d[i] < d[imin]) imin = i;
        d = d.map(function (y) { return y / mx; });
        var here = rough(f, amp, v.r) / mx, tri = rough(f, amp, Math.SQRT2) / mx;
        s.out = { here: here, tri: tri, best: rs[imin], cents: 1200 * Math.log(v.r) / Math.LN2 };
        var a = g[0].axes({ x: [1, 2.3], y: [0, 1.25], title: "Roughness against the interval", yticks: [0, 0.5, 1], xlabel: "frequency ratio of the two tones", xticks: [1, 1.25, 1.5, 1.75, 2, 2.25] });
        for (i = 0; i < just.length; i++) { var q = just[i][0] / just[i][1]; a.vline(q, { color: C.muted, dash: [2, 4] }); a.text(q, i % 2 ? 1.18 : 1.08, just[i][0] + ":" + just[i][1], { align: "center", color: C.muted, size: 11 }); }
        a.line(rs, d, { color: C.spot, width: 2 });
        a.vline(v.r, { color: C.idea });
        a.dots([v.r], [here], { color: C.idea, r: 5 });
        var hi = f[v.n - 1] * 2.3 / BASE, b = g[1].axes({ x: [0.5, Math.max(3, hi * 1.05)], y: [0, 1.25], title: "Partials of the two tones at this interval", xlabel: "frequency, in units of the lower tone's fundamental", noY: true });
        for (k = 0; k < v.n; k++) {
          b.line([f[k] / BASE, f[k] / BASE], [0, amp[k]], { color: C.spot, width: 3 });
          b.line([f[k] * v.r / BASE, f[k] * v.r / BASE], [0, amp[k] * 0.92], { color: C.implied, width: 3, alpha: 0.9 });
        }
        b.legend([["lower tone", C.spot], ["upper tone", C.implied]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["interval", fmt(o.cents, 0) + " cents"], ["roughness here", fmt(o.here, 2)], ["at the tritone, √2", fmt(o.tri, 2)], ["smoothest interval above 1.1", fmt(o.best, 3)]];
      },
      note: "The film's model: Sethares's form of Plomp and Levelt's curve, partial k at k^log2(S) times the fundamental with amplitude 0.88^(k−1), the lower tone at middle C. Roughness is scaled so the curve's peak is 1. Partials that nearly coincide beat slowly and add little roughness; partials a fraction of a critical band apart add the most.",
    });
  };

  // ---- Part 41: two calibrated groups, two thresholds ---------------------------------------------------------
  W.groupthresholds = function (el) {
    var M = 200;
    var group = function (mean, t) { // true risk ~ Beta(4 mean, 4 (1 - mean)); the score is the risk itself
      var a = 4 * mean, b = 4 * (1 - mean), i, x, f, tot = 0, pos = 0, tp = 0, fp = 0, xs = [], fs = [];
      for (i = 0; i < M; i++) { x = (i + 0.5) / M; f = Math.pow(x, a - 1) * Math.pow(1 - x, b - 1); xs.push(x); fs.push(f); tot += f; pos += f * x; if (x >= t) { tp += f * x; fp += f * (1 - x); } }
      var neg = tot - pos, sel = tp + fp;
      return { xs: xs, dens: fs.map(function (y) { return y * M / tot; }), base: pos / tot, fpr: neg > 0 ? fp / neg : 0, fnr: pos > 0 ? 1 - tp / pos : 0,
        ppv: sel > 1e-12 ? tp / sel : 1, sel: sel / tot };
    };
    QB.widget(el, {
      title: "One score, two groups: which gap will you accept?",
      sub: "Each person's score is their true risk, so it is calibrated in both groups. Group A's base rate is 30%; set group B's. With one threshold for both, B's false-positive rate is higher. Move B's threshold to close that gap and the precision gap opens; close the precision gap and the error rates part. Only equal base rates close both.",
      panels: 2, height: 300,
      controls: [
        { k: "mb", label: "Base rate of group B", min: 0.3, max: 0.7, step: 0.01, value: 0.5, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "ta", label: "Threshold for group A", min: 0.05, max: 0.95, step: 0.005, value: 0.5, fmt: function (x) { return x.toFixed(3); } },
        { k: "tb", label: "Threshold for group B", min: 0.05, max: 0.95, step: 0.005, value: 0.5, fmt: function (x) { return x.toFixed(3); } },
      ],
      draw: function (g, v, s) {
        var A = group(0.3, v.ta), B = group(v.mb, v.tb);
        s.out = [A, B];
        var a = g[0].axes({ x: [0, 1], y: [0, 2.6], title: "Scores in each group, and the two thresholds", xlabel: "score = true risk", noY: true });
        a.area(A.xs, A.dens, 0, { color: C.spot, alpha: 0.22 }).line(A.xs, A.dens, { color: C.spot, width: 1.8 });
        a.area(B.xs, B.dens, 0, { color: C.implied, alpha: 0.22 }).line(B.xs, B.dens, { color: C.implied, width: 1.8 });
        a.vline(v.ta, { color: C.spot, dash: [6, 3], width: 1.6 }); a.vline(v.tb, { color: C.implied, dash: [2, 3], width: 1.6 });
        a.legend([["group A", C.spot], ["group B", C.implied]], { pos: "tr" });
        var keys = ["sel", "fpr", "fnr", "ppv"];
        var b = g[1].axes({ x: [0.4, 4.6], y: [0, 100], title: "The four rates in each group", xticks: [1, 2, 3, 4], xfmt: function (x) { return ["flagged", "FPR", "FNR", "precision"][x - 1]; }, yfmt: function (y) { return y + "%"; } });
        var xs = [1, 2, 3, 4];
        b.bars(xs.map(function (x) { return x - 0.19; }), keys.map(function (k) { return 100 * A[k]; }), 0.34, { color: C.spot });
        b.bars(xs.map(function (x) { return x + 0.19; }), keys.map(function (k) { return 100 * B[k]; }), 0.34, { color: C.implied });
        for (var i = 0; i < 4; i++) { var d = 100 * Math.abs(A[keys[i]] - B[keys[i]]); b.text(i + 1, Math.max(A[keys[i]], B[keys[i]]) * 100, d < 1 ? "equal" : "gap " + d.toFixed(0), { align: "center", dy: -9, color: d < 1 ? C.gain : C.muted, size: 11 }); }
      },
      readout: function (v, s) {
        var A = s.out[0], B = s.out[1], two = function (k) { return QB.pct(A[k], 0) + " / " + QB.pct(B[k], 0); };
        return [["false positives A / B", two("fpr")], ["false negatives A / B", two("fnr")], ["precision A / B", two("ppv")], ["flagged A / B", two("sel")]];
      },
      note: "The film's population in the limit of many people: risks follow a Beta distribution of concentration 4, outcomes are drawn from the risk, and everyone at or above the group's threshold is labelled high risk. Blue is group A and orange is group B throughout. FPR: the share of those who do not reoffend who are flagged; FNR: the share of those who do who are not; precision: the share of the flagged who reoffend.",
    });
  };

  // ---- Part 42: the off-switch game ---------------------------------------------------------------------------
  W.offswitchdefer = function (el) {
    var wait = function (mu, sig, beta) { // E[u P(human allows)] for u ~ N(mu, sig^2); beta = null is a rational human
      if (beta === null) { if (sig < 1e-9) return Math.max(mu, 0); var z = mu / sig; return mu * QB.cdf(z) + sig * QB.pdf(z); }
      if (sig < 1e-9) return mu / (1 + Math.exp(-beta * mu));
      var n = 160, a = 0, i, t, u; // the midpoint rule over six standard deviations
      for (i = 0; i < n; i++) { t = -6 + 12 * (i + 0.5) / n; u = mu + sig * t; a += QB.pdf(t) * u / (1 + Math.exp(-beta * u)); }
      return a * 12 / n;
    };
    QB.widget(el, {
      title: "The off-switch game: should the robot let us decide?",
      sub: "The robot believes its action is worth u to us, with mean μ and uncertainty σ. It can act, switch itself off (worth 0), or wait and let the human decide. A rational human allows the action exactly when u > 0, so waiting never loses. Lower the human's rationality, or make the robot certain, and the reason to defer goes.",
      panels: 2, height: 300,
      controls: [
        { k: "mu", label: "Robot's expected value of acting, μ", min: -2, max: 2, step: 0.05, value: 0.5, fmt: function (x) { return fmt(x, 2); } },
        { k: "sig", label: "Robot's uncertainty, σ", min: 0, max: 3, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2); } },
        { k: "beta", label: "Human's rationality, β", min: 0.1, max: 10, step: 0.1, value: 10, fmt: function (x) { return x >= 10 ? "rational" : x.toFixed(1); } },
      ],
      draw: function (g, v, s) {
        var beta = v.beta >= 10 ? null : v.beta, act = v.mu, w = wait(v.mu, v.sig, beta), alt = Math.max(act, 0), inc = w - alt;
        s.out = { act: act, w: w, inc: inc, best: inc > 1e-9 ? "wait for the human" : inc < -1e-9 ? (act > 0 ? "act" : "switch off") : "indifferent" };
        var vals = [act, 0, w], top = Math.max(vals[0], vals[2], 0), lo = Math.min(-0.5, Math.floor(Math.min(act, w) * 2) / 2), hi = Math.max(1, Math.ceil(top * 2) / 2 + 0.5);
        var a = g[0].axes({ x: [0.4, 3.6], y: [lo, hi], title: "What each choice is worth to the robot", xticks: [1, 2, 3], xfmt: function (x) { return ["act", "switch off", "wait"][x - 1]; } });
        a.hline(0, { color: C.muted, dash: [] });
        a.bars([1, 2, 3], vals, 0.55, { color: function (k) { return vals[k] >= top - 1e-9 ? C.gain : C.cash; }, alpha: 0.9 });
        for (var k = 0; k < 3; k++) a.text(k + 1, Math.max(vals[k], 0), fmt(vals[k], 2), { align: "center", dy: -9, color: vals[k] >= top - 1e-9 ? C.gain : C.muted });
        var sg = QB.linspace(0, 3, 61), rat = [], cur = [], mn = 0, mx = 0.3;
        for (var i = 0; i < sg.length; i++) { rat.push(wait(v.mu, sg[i], null) - alt); cur.push(wait(v.mu, sg[i], beta) - alt); mn = Math.min(mn, cur[i]); mx = Math.max(mx, rat[i], cur[i]); }
        var b = g[1].axes({ x: [0, 3], y: [Math.floor(mn * 5 - 0.5) / 5, Math.ceil(mx * 5 + 0.5) / 5], title: "Incentive to defer, as uncertainty grows", xlabel: "robot's uncertainty σ" });
        b.hline(0, { color: C.muted });
        b.line(sg, rat, { color: C.gain, width: 1.6, dash: [5, 4] });
        b.line(sg, cur, { color: C.idea, width: 2.2 });
        b.vline(v.sig, { color: C.muted });
        b.dots([v.sig], [inc], { color: C.idea, r: 5 });
        b.legend([["this human", C.idea], ["a rational human", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["act", fmt(o.act, 2)], ["switch off", "0.00"], ["wait", fmt(o.w, 2)], ["incentive to defer", fmt(o.inc, 2)], ["the robot should", o.best]];
      },
      note: "The film's game (Hadfield-Menell, Dragan, Abbeel and Russell 2017): with a rational human, waiting is worth E[max(u, 0)] = μΦ(μ/σ) + σφ(μ/σ), 0.70 at μ = 0.5 and σ = 1 against 0.50 for acting. A noisy human allows the action with probability 1/(1 + e^(−βu)). The incentive to defer is the value of waiting minus the better of acting and switching off; the green bar is the best choice.",
    });
  };
})();
