// Interactives for Acts VIII and IX: the browser, services, people, the cloud, data pipelines, search (Parts 42-47).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  function label(c, str, x, y, o) { // one line of text on the canvas
    o = o || {}; c.save(); c.font = (o.bold ? "600 " : "") + (o.size || 11.5) + "px system-ui, sans-serif";
    c.fillStyle = o.color || C.muted; c.textAlign = o.align || "left"; c.textBaseline = o.base || "middle";
    c.fillText(str, x, y); c.restore();
  }
  function heading(c, box, str) { label(c, str, box.x + 12, box.y + 14, { bold: true, size: 12.5, color: C.ink }); }

  // ---- Part 42: greedy against Knuth-Plass line breaking -----------------------------------------------------
  W.raggedlines = function (el) {
    var texts = [
      "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families.",
      "Call me Ishmael. Some years ago, never mind how long precisely, having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen.",
      "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope.",
    ];
    var names = ["Pride and Prejudice", "Moby-Dick", "A Tale of Two Cities"];
    function greedy(wd, sp, L) {
      var lines = [], cur = [], w = 0, i, need;
      for (i = 0; i < wd.length; i++) {
        need = cur.length ? w + sp + wd[i] : wd[i];
        if (cur.length && need > L) { lines.push(cur); cur = [i]; w = wd[i]; } else { cur.push(i); w = need; }
      }
      if (cur.length) lines.push(cur);
      return lines;
    }
    function total(wd, sp, L) { // Knuth-Plass with the film's cost: 100 (shortfall / width)^3 per line, the last line free
      var n = wd.length, best = [0], prev = [0], i, j, w, cost, s;
      for (j = 1; j <= n; j++) {
        best.push(Infinity); prev.push(j - 1); w = -sp;
        for (i = j - 1; i >= 0; i--) {
          w += wd[i] + sp;
          if (w > L && i < j - 1) break;
          s = L - w; cost = j === n ? 0 : s < 0 ? 1e9 : 100 * Math.pow(s / L, 3);
          if (best[i] + cost < best[j]) { best[j] = best[i] + cost; prev[j] = i; }
        }
      }
      var lines = [], ln;
      for (j = n; j > 0; j = prev[j]) { ln = []; for (i = prev[j]; i < j; i++) ln.push(i); lines.unshift(ln); }
      return lines;
    }
    function stats(lines, wd, sp, L) {
      var bad = 0, worst = 0, k, i, w, s;
      for (k = 0; k < lines.length - 1; k++) {
        w = -sp; for (i = 0; i < lines[k].length; i++) w += wd[lines[k][i]] + sp;
        s = Math.max(0, L - w); bad += 100 * Math.pow(s / L, 3); worst = Math.max(worst, s);
      }
      return [lines.length, worst, bad];
    }
    QB.widget(el, {
      title: "Where should a paragraph break?",
      sub: "The same words are broken twice. Greedy fills each line and moves on; Knuth and Plass's dynamic program chooses all the breaks together to minimize the summed cube of each line's shortfall. Red bars show how far each line falls short. Narrow the column and watch greedy leave one bad line that total fit spreads out.",
      panels: 2, height: 300,
      controls: [
        { k: "wd", label: "Column width", min: 45, max: 100, step: 1, value: 62, fmt: function (x) { return x + "%"; } },
        { k: "nw", label: "Words", min: 15, max: 56, step: 1, value: 56 },
        { k: "txt", label: "Paragraph", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return names[x]; } },
      ],
      draw: function (g, v, s) {
        var c = g.ctx, words = texts[v.txt].split(" ").slice(0, v.nw), size = g[0].box.w > 430 ? 14 : 11.5;
        var font = size + "px Georgia, serif", wd = [], i, p, k;
        c.save(); c.font = font;
        for (i = 0; i < words.length; i++) wd.push(c.measureText(words[i]).width);
        var sp = c.measureText(" ").width; c.restore();
        s.out = [];
        for (p = 0; p < 2; p++) {
          var b = g[p].box, L = Math.max(120, (b.w - 28) * v.wd / 100), x0 = b.x + 14, y0 = b.y + 36, lh = size + 4;
          var lines = p ? total(wd, sp, L) : greedy(wd, sp, L), st = stats(lines, wd, sp, L);
          s.out.push(st);
          heading(c, b, p ? "Knuth-Plass: all breaks chosen together" : "Greedy: fill each line, then move on");
          c.save(); c.beginPath(); c.rect(b.x, b.y + 26, b.w, b.h - 28); c.clip();
          c.strokeStyle = C.muted; c.setLineDash([4, 4]); c.lineWidth = 1;
          c.beginPath(); c.moveTo(x0 + L + 0.5, y0 - 8); c.lineTo(x0 + L + 0.5, y0 + lh * lines.length - 4); c.stroke(); c.setLineDash([]);
          c.font = font; c.textBaseline = "middle"; c.textAlign = "left";
          for (k = 0; k < lines.length; k++) {
            var x = x0, y = y0 + lh * k;
            for (i = 0; i < lines[k].length; i++) { c.fillStyle = C.ink; c.fillText(words[lines[k][i]], x, y); x += wd[lines[k][i]] + sp; }
            x -= sp;
            if (k < lines.length - 1 && L - x + x0 > 0.5) {
              var sh = (L - x + x0) / L;
              c.fillStyle = C.loss; c.globalAlpha = Math.min(0.9, 0.2 + 4 * sh); c.fillRect(x + 3, y - lh / 2 + 2, L - (x - x0) - 3, lh - 4); c.globalAlpha = 1;
            }
          }
          c.restore();
        }
      },
      readout: function (v, s) {
        return [["lines, greedy", String(s.out[0][0])], ["lines, Knuth-Plass", String(s.out[1][0])],
          ["worst shortfall", fmt(s.out[0][1], 0) + " px against " + fmt(s.out[1][1], 0) + " px"],
          ["badness", fmt(s.out[0][2], 2) + " against " + fmt(s.out[1][2], 2)]];
      },
      note: "Word widths are measured by your browser's own font, so the breaks differ a little between machines. Badness is the sum over all lines but the last of 100 × (shortfall / column width)³, the cost the film uses; the dashed line is the right edge of the column. Greedy never uses more lines; total fit never has more badness.",
    });
  };
  // ---- Part 43: a counter behind a network that loses and duplicates ------------------------------------------
  W.retrycounter = function (el) {
    var N = 400, names = ["at most once", "at least once", "exactly once"];
    function expect(l, d, A) { // expected count per increment: [at most once, at least once, exactly once] with A sends allowed
      var del = (1 - l) * (1 + d), p = (1 - l) * ((1 - d) * (1 - l) + d * (1 - l * l));
      var sends = p > 1e-9 ? (1 - Math.pow(1 - p, A)) / p : A;
      return [del, del * sends, 1 - Math.pow(l, A)];
    }
    function simulate(l, d, A, seed) { // N increments; a send is lost with probability l, an arriving one is doubled with probability d
      var r = QB.rng(seed), c = [0, 0, 0], sent = 0, i, a, k, copies, acked, first;
      for (i = 0; i < N; i++) {
        acked = false; first = true;
        for (a = 0; a < A && !acked; a++) {
          sent++;
          copies = r() < l ? 0 : (r() < d ? 2 : 1);
          if (a === 0) c[0] += copies;          // at most once: the first send only, every copy counted
          c[1] += copies;                       // at least once: every copy of every send counted
          if (copies && first) { c[2]++; first = false; } // exactly once: the receiver remembers the id
          for (k = 0; k < copies; k++) if (r() >= l) acked = true; // each copy is acknowledged; acks are lost too
        }
      }
      return { c: c, sent: sent };
    }
    QB.widget(el, {
      title: "Three delivery promises, one counter",
      sub: "A sender increments a remote counter 400 times. Each message, and each acknowledgement, is lost with the chosen probability; some arrive twice. Sending once loses counts, retrying until acknowledged adds them, and retrying with an id the receiver remembers is exact. Now cut the resends to zero and watch the exact count break too.",
      panels: 2, height: 300,
      controls: [
        { k: "loss", label: "Messages lost", min: 0, max: 60, step: 1, value: 10, fmt: function (x) { return x + "%"; } },
        { k: "dup", label: "Messages duplicated", min: 0, max: 20, step: 1, value: 2, fmt: function (x) { return x + "%"; } },
        { k: "res", label: "Resends allowed", min: 0, max: 12, step: 1, value: 12 },
      ],
      buttons: [{ label: "New network", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var l = v.loss / 100, d = v.dup / 100, A = v.res + 1, sim = simulate(l, d, A, s.seed * 7919 + 11), i;
        var cols = [C.spot, C.loss, C.gain], share = sim.c.map(function (x) { return x / N; });
        s.out = sim;
        var top = Math.max(1.5, Math.ceil(Math.max(share[1], expect(0.6, d, A)[1]) * 2.2) / 2);
        var a = g[0].axes({ x: [0.4, 3.6], y: [0, top], title: "This network: count / 400 sent", xticks: [1, 2, 3], xfmt: function (t) { return names[t - 1]; } });
        a.bars([1, 2, 3], share, 0.6, { color: function (k) { return cols[k]; } });
        a.hline(1, { color: C.ink });
        for (i = 0; i < 3; i++) a.text(i + 1, share[i], String(sim.c[i]), { align: "center", dy: -9, bold: true });
        var ls = QB.linspace(0, 0.6, 61), e = [[], [], []];
        for (i = 0; i < ls.length; i++) { var q = expect(ls[i], d, A); e[0].push(q[0]); e[1].push(q[1]); e[2].push(q[2]); }
        var b = g[1].axes({ x: [0, 60], y: [0, top], title: "Expected count / sent, against loss", xlabel: "messages lost (%)" });
        var xs = ls.map(function (t) { return 100 * t; });
        b.hline(1, { color: C.ink });
        b.line(xs, e[1], { color: C.loss }).line(xs, e[0], { color: C.spot }).line(xs, e[2], { color: C.gain });
        b.vline(v.loss, { color: C.idea });
        b.dots([v.loss, v.loss, v.loss], share, { color: function (k) { return cols[k]; }, r: 4 });
        b.legend([["at least once", C.loss], ["exactly once (dedup)", C.gain], ["at most once", C.spot]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["at most once", String(s.out.c[0])], ["at least once", String(s.out.c[1])], ["exactly once", String(s.out.c[2])],
          ["truth", String(N)], ["messages sent with retries", String(s.out.sent)]];
      },
      note: "Simulated network. Bars and dots are one run of 400 increments; the curves are expectations: (1 − loss)(1 + dup) for one send, that number times the expected sends until an acknowledgement returns for at-least-once, and 1 − loss^(sends allowed) with deduplication. Deduplication uses the same messages as at-least-once; it needs the receiver to remember ids.",
    });
  };
  // ---- Part 44: an A/A test looked at every k days -----------------------------------------------------------
  W.morninglooks = function (el) {
    var T = 600, SHOW = 24, rules = ["first p < α", "sequential test"];
    QB.widget(el, {
      title: "An A/A test, and how often you look at it",
      sub: "Six hundred experiments in which nothing differs between the arms. Each line is one experiment's z statistic, day by day; it stops, in red, the first time a look finds it outside the boundary. Look once at the end and about α of them declare a winner. Look every morning and watch the share climb; then switch to the sequential test, whose boundary starts high.",
      panels: 2, height: 300,
      controls: [
        { k: "days", label: "Length of the test", min: 5, max: 60, step: 1, value: 30, fmt: function (x) { return x + " days"; } },
        { k: "every", label: "Look every", min: 1, max: 60, step: 1, value: 1, fmt: function (x) { return x === 1 ? "day" : x + " days"; } },
        { k: "alpha", label: "Significance level α", min: 1, max: 10, step: 1, value: 5, fmt: function (x) { return x + "%"; } },
        { k: "rule", label: "Stopping rule", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return rules[x]; } },
      ],
      buttons: [{ label: "New experiments", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed * 104729 + 3), D = v.days, al = v.alpha / 100, zfix = QB.inv(1 - al / 2), t, e, d;
        var bound = [], look = [];
        for (d = 1; d <= D; d++) { // the boundary in z units on day d, and whether day d is a look
          var q = d / 10; // the mixture puts its weight on effects that ten days of traffic can resolve
          bound.push(v.rule ? Math.sqrt(2 * (1 + q) / q * Math.log(Math.sqrt(1 + q) / al)) : zfix);
          look.push(d % v.every === 0 || d === D);
        }
        var stopped = new Array(D).fill(0), paths = [], stops = [], last = 0;
        for (e = 0; e < T; e++) {
          var sum = 0, z = [], hit = -1;
          for (d = 1; d <= D; d++) {
            sum += r.normal(); var zz = sum / Math.sqrt(d);
            if (e < SHOW) z.push(zz);
            if (hit < 0 && look[d - 1] && Math.abs(zz) > bound[d - 1]) hit = d;
          }
          if (hit > 0) stopped[hit - 1]++;
          if (Math.abs(sum / Math.sqrt(D)) > zfix) last++;
          if (e < SHOW) { paths.push(z); stops.push(hit); }
        }
        var cum = [], acc = 0, days = [];
        for (d = 1; d <= D; d++) { acc += stopped[d - 1]; cum.push(100 * acc / T); days.push(d); }
        var looks = 0; for (d = 0; d < D; d++) if (look[d]) looks++;
        s.out = [looks, acc / T, last / T, al];
        var a = g[0].axes({ x: [1, D], y: [-5, 5], title: "z statistic of " + SHOW + " of the experiments", xlabel: "day" });
        for (e = 0; e < SHOW; e++) {
          var end = stops[e] > 0 ? stops[e] : D;
          a.line(days.slice(0, end), paths[e].slice(0, end), { color: stops[e] > 0 ? C.loss : C.spot, width: stops[e] > 0 ? 1.4 : 1, alpha: stops[e] > 0 ? 0.95 : 0.4 });
          if (stops[e] > 0) a.dots([end], [paths[e][end - 1]], { color: C.loss, r: 3.5 });
        }
        var bx = [], bu = [], bl = [];
        for (d = 1; d <= D; d++) if (look[d - 1]) { bx.push(d); bu.push(Math.min(5, bound[d - 1])); bl.push(-Math.min(5, bound[d - 1])); }
        if (bx.length > 1) { a.line(bx, bu, { color: C.idea, width: 1.5 }).line(bx, bl, { color: C.idea, width: 1.5 }); }
        a.dots(bx, bu, { color: C.idea, r: 2 }).dots(bx, bl, { color: C.idea, r: 2 });
        var top = Math.max(12, Math.ceil(Math.max(cum[D - 1], 2 * v.alpha) / 10) * 10);
        var b = g[1].axes({ x: [1, D], y: [0, top], title: "Experiments that declared a winner so far", xlabel: "day", yfmt: function (y) { return y + "%"; } });
        b.hline(v.alpha, { color: C.muted });
        b.line(days, cum, { color: C.loss, width: 2 });
        b.legend([["all " + T + " experiments", C.loss], ["promised: α", C.muted]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["looks", String(s.out[0])], ["false positives", QB.pct(s.out[1])], ["promised", QB.pct(s.out[3], 0)], ["one look on the last day", QB.pct(s.out[2])]];
      },
      note: "Simulated data: with no real effect the z statistic is a random walk divided by √day. Gold marks the boundary at each look: ±z for a fixed level, or the mixture test's boundary √(2(1 + q)/q · ln(√(1 + q)/α)) with q = day/10, which Ville's inequality keeps below α at every look. The price of the sequential test is a later stop when an effect is real.",
    });
  };
  // ---- Part 45: a proportional autoscaler acting on an old measurement ----------------------------------------
  W.autoscalegain = function (el) {
    var STEPS = 80, QUOTA = 200, TARGET = 0.6;
    function limit(d) { return 2 * Math.cos(d * Math.PI / (2 * d + 1)); }
    QB.widget(el, {
      title: "An autoscaler with a delay",
      sub: "Load jumps at step 10. Every step the controller adds gain × (measured utilization / target − 1) × servers, but the measurement is some steps old. Below the gold curve the server count settles at the right size; raise the gain or the delay across it and the loop overshoots, then swings between one server and the quota of 200.",
      panels: 2, height: 300,
      controls: [
        { k: "gain", label: "Gain K", min: 0.05, max: 2.2, step: 0.05, value: 0.3, fmt: function (x) { return x.toFixed(2); } },
        { k: "delay", label: "Measurement delay", min: 0, max: 6, step: 1, value: 1, fmt: function (x) { return x + (x === 1 ? " step" : " steps"); } },
        { k: "spike", label: "Load after the jump", min: 50, max: 300, step: 10, value: 100, fmt: function (x) { return x + " req/s"; } },
      ],
      buttons: [{ label: "New noise", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed * 31 + 5), n = 40 / 10 / TARGET, util = [], ts = [], ns = [], t, load, seen, lo = Infinity, hi = 0, peak = 0;
        for (t = 0; t < STEPS; t++) { // the film's model: each server handles 10 requests a second, the target is 60% busy
          load = (t >= 10 ? v.spike : 40) * (1 + 0.02 * r.normal());
          util.push(load / (10 * n));
          seen = util[Math.max(0, t - v.delay)];
          n = Math.min(QUOTA, Math.max(1, n + v.gain * (seen / TARGET - 1) * n));
          ts.push(t); ns.push(n); peak = Math.max(peak, n);
          if (t >= STEPS - 20) { lo = Math.min(lo, n); hi = Math.max(hi, n); }
        }
        var ideal = v.spike / 10 / TARGET, lim = limit(v.delay), ok = v.gain < lim;
        s.out = [ideal, peak, lo, hi, lim, ok];
        var a = g[0].axes({ x: [0, STEPS - 1], y: [1, 300], logy: true, title: "Servers running", xlabel: "step" });
        a.hline(ideal, { color: C.muted }).hline(QUOTA, { color: C.loss, dash: [2, 4] });
        a.vline(10, { color: C.muted, dash: [2, 4] });
        a.line(ts, ns, { color: ok ? C.gain : C.loss, width: 2 });
        a.text(STEPS - 2, QUOTA, "quota", { color: C.loss, align: "right", dy: -8 });
        a.text(STEPS - 2, ideal, "right size", { color: C.muted, align: "right", dy: 9 });
        var ds = [], ks = [], d;
        for (d = 0; d <= 6; d++) { ds.push(d); ks.push(limit(d)); }
        var b = g[1].axes({ x: [-0.3, 6.3], y: [0, 2.3], title: "Gain against delay: where the loop is stable", xlabel: "delay d (steps)", xticks: [0, 1, 2, 3, 4, 5, 6] });
        b.area(ds, ks, 0, { color: C.gain, alpha: 0.14 });
        b.line(ds, ks, { color: C.idea, width: 2 }).dots(ds, ks, { color: C.idea, r: 3 });
        b.dots([v.delay], [v.gain], { color: ok ? C.gain : C.loss, r: 6 });
        b.text(1.7, 1.95, "K = 2 cos(dπ / (2d + 1))", { color: C.idea });
        b.text(1.7, 1.7, "oscillates above, settles below", { color: C.muted });
      },
      readout: function (v, s) {
        return [["right size", fmt(s.out[0], 1)], ["peak", fmt(s.out[1], 1)], ["last 20 steps", fmt(s.out[2], 1) + " to " + fmt(s.out[3], 1)],
          ["stable gain below", fmt(s.out[4], 2)], ["this loop", s.out[5] ? "settles" : "oscillates"]];
      },
      note: "Simulated load with 2% noise. The limit comes from the linearized error e(t+1) = e(t) − K·e(t−d); the simulated loop is nonlinear and clipped between 1 server and the quota, so just above the limit it swings rather than diverging. K = 1 with no delay is Kubernetes' rule n ← n·u/u*.",
    });
  };
  // ---- Part 46: a watermark's lag, completeness against latency -----------------------------------------------
  W.watermarklag = function (el) {
    var N = 120, RATE = 2, SIZE = 10, SPAN = N / RATE;
    function makeEvents(delay, seed) { // [event time, arrival time], sorted by arrival; 5% are much later
      var r = QB.rng(seed), ev = [], i, d;
      for (i = 0; i < N; i++) {
        d = -delay * Math.log(1 - r()) + (r() < 0.05 ? 8 + 7 * r() : 0);
        ev.push([i / RATE, i / RATE + d]);
      }
      ev.sort(function (a, b) { return a[1] - b[1]; });
      return ev;
    }
    function process(ev, lag, allowed) { // tumbling windows of 10 s; a window fires when the watermark passes its end
      var nw = SPAN / SIZE, counts = new Array(nw).fill(0), truth = new Array(nw).fill(0), fired = new Array(nw).fill(-1);
      var status = [], wmk = [], maxEt = -Infinity, dropped = 0, refine = 0, i, w, k, wm;
      for (i = 0; i < ev.length; i++) {
        w = Math.min(nw - 1, Math.floor(ev[i][0] / SIZE)); truth[w]++;
        maxEt = Math.max(maxEt, ev[i][0]); wm = maxEt - lag; wmk.push([wm, ev[i][1]]);
        if (wm >= (w + 1) * SIZE + allowed) { dropped++; status.push(2); }
        else { counts[w]++; if (fired[w] >= 0) { refine++; status.push(1); } else status.push(0); }
        for (k = 0; k < nw; k++) if (fired[k] < 0 && counts[k] > 0 && wm >= (k + 1) * SIZE) fired[k] = ev[i][1];
      }
      var lat = 0, exact = 0, last = ev[ev.length - 1][1];
      for (k = 0; k < nw; k++) { lat += (fired[k] < 0 ? last : fired[k]) - (k + 1) * SIZE; if (counts[k] === truth[k]) exact++; }
      return { dropped: dropped, refine: refine, exact: exact, nw: nw, lat: lat / nw, status: status, wmk: wmk };
    }
    QB.widget(el, {
      title: "How long should a window wait?",
      sub: "Each dot is an event: across, when it happened; up, when it arrived. Windows are ten seconds of event time. The gold watermark trails the newest event time by the lag, and a window answers when the watermark passes its end; events that arrive after that are dropped (red). Shorten the lag for early answers and lost events, then add allowed lateness and keep both.",
      panels: 2, height: 300,
      controls: [
        { k: "lag", label: "Watermark lag", min: 0, max: 20, step: 0.5, value: 3, fmt: function (x) { return x.toFixed(1) + " s"; } },
        { k: "delay", label: "Mean network delay", min: 0.2, max: 5, step: 0.1, value: 1.5, fmt: function (x) { return x.toFixed(1) + " s"; } },
        { k: "late", label: "Allowed lateness", min: 0, max: 30, step: 1, value: 0, fmt: function (x) { return x + " s"; } },
      ],
      buttons: [{ label: "New stream", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var ev = makeEvents(v.delay, s.seed * 613 + 17), res = process(ev, v.lag, v.late), i, k;
        s.out = res;
        var top = SPAN + 30, cols = [C.spot, C.implied, C.loss];
        var a = g[0].axes({ x: [0, SPAN], y: [0, top], title: "Event time and arrival time", xlabel: "event time (s)", xticks: [0, 10, 20, 30, 40, 50, 60] });
        a.line([0, SPAN], [0, SPAN], { color: C.muted, width: 1, dash: [4, 4] });
        var wx = [], wy = [];
        for (i = 0; i < res.wmk.length; i++) { if (i) { wx.push(res.wmk[i - 1][0]); wy.push(res.wmk[i][1]); } wx.push(res.wmk[i][0]); wy.push(res.wmk[i][1]); }
        a.line(wx, wy, { color: C.idea, width: 1.6 });
        a.dots(ev.map(function (e) { return e[0]; }), ev.map(function (e) { return e[1]; }), { color: function (j) { return cols[res.status[j]]; }, r: 2.6 });
        a.legend([["counted on time", C.spot], ["counted as a refinement", C.implied], ["dropped", C.loss], ["watermark", C.idea]], { pos: "br" });
        var lx = [], ly = [], lag;
        for (lag = 0; lag <= 20; lag += 1) { k = process(ev, lag, v.late); lx.push(k.lat); ly.push(100 * k.dropped / N); }
        var ymax = Math.max(10, Math.ceil(Math.max.apply(null, ly) / 10) * 10 + 5), xmax = Math.max(25, Math.ceil(Math.max.apply(null, lx) / 5) * 5);
        var b = g[1].axes({ x: [0, xmax], y: [0, ymax], title: "Every lag from 0 to 20 s on this stream", xlabel: "mean wait for a window's first answer (s)", yfmt: function (y) { return y + "%"; } });
        b.line(lx, ly, { color: C.loss, width: 1.6 }).dots(lx, ly, { color: C.loss, r: 2 });
        b.dots([res.lat], [100 * res.dropped / N], { color: C.idea, r: 6 });
        b.legend([["events dropped", C.loss], ["the chosen lag", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["dropped", s.out.dropped + " of " + N], ["windows exact", s.out.exact + " of " + s.out.nw],
          ["first answer after", fmt(s.out.lat, 1) + " s"], ["refinements", String(s.out.refine)]];
      },
      note: "Simulated stream: 120 events, two a second, exponential network delays, and one in twenty held back a further 8 to 15 s (a phone offline). The dashed diagonal is an event with no delay; a dot to the left of the gold line arrived behind the watermark. With allowed lateness, a late event reopens its window and the answer is corrected; the price is state kept longer and answers that change.",
    });
  };
  // ---- Part 47: bits per posting under four gap codes --------------------------------------------------------
  W.gapcodes = function (el) {
    function lg2(x) { return Math.log(x) / Math.LN2; }
    function gammaBits(g) { return 2 * Math.floor(lg2(g) + 1e-12) + 1; }
    function deltaBits(g) { var n = Math.floor(lg2(g) + 1e-12) + 1; return n - 1 + gammaBits(n); }
    function vbyteBits(g) { return 8 * Math.max(1, Math.ceil((Math.floor(lg2(g) + 1e-12) + 1) / 7)); }
    function model(mean, c) { // gaps: 1 with probability c (a run), otherwise geometric; the overall mean is kept
      var m2 = Math.max(1, (mean - c) / (1 - c)), p = 1 / m2, q = 1 - p, gmax = Math.min(60000, Math.ceil(40 * m2) + 2);
      var H = 0, v = 0, ga = 0, de = 0, g, P, w = (1 - c) * p;
      for (g = 1; g <= gmax; g++) {
        P = w + (g === 1 ? c : 0); w *= q;
        if (P <= 0) continue;
        H -= P * lg2(P); v += P * vbyteBits(g); ga += P * gammaBits(g); de += P * deltaBits(g);
      }
      var rice = [], k, M, qm;
      for (k = 0; k <= 12; k++) { M = Math.pow(2, k); qm = Math.pow(q, M); rice.push((1 - c) * (qm < 1 ? qm / (1 - qm) : 0) + 1 + k); }
      return { H: H, vbyte: v, gamma: ga, delta: de, rice: rice };
    }
    QB.widget(el, {
      title: "Gaps between document ids, in bits",
      sub: "A postings list is stored as gaps between sorted document ids. A rare word has long gaps, a common one short gaps. Bars show the expected bits per posting under four codes, against the entropy of the gaps (green). Slide the Rice parameter k to find its best value, about log₂(0.69 × mean gap), where it nearly touches the entropy. Then make the gaps clustered: no k comes close any more, and γ and δ, which assume nothing about the mean, win.",
      panels: 2, height: 300,
      controls: [
        { k: "lg", label: "Mean gap N / f", min: 0.5, max: 10, step: 0.25, value: 4.75, fmt: function (x) { return fmt(Math.pow(2, x), x < 4 ? 1 : 0); } },
        { k: "k", label: "Rice parameter k", min: 0, max: 12, step: 1, value: 4 },
        { k: "run", label: "Gaps that are runs of 1", min: 0, max: 80, step: 5, value: 0, fmt: function (x) { return x + "%"; } },
      ],
      draw: function (g, v, s) {
        var mean = Math.pow(2, v.lg), m = model(mean, v.run / 100), kk, best = 0;
        for (kk = 1; kk <= 12; kk++) if (m.rice[kk] < m.rice[best]) best = kk;
        var rule = Math.max(0, Math.floor(lg2(Math.max(1, 0.69 * mean))));
        s.out = [m, best, rule, mean];
        var vals = [m.vbyte, m.gamma, m.delta, m.rice[v.k]], names = ["v-byte", "γ", "δ", "Rice k=" + v.k], cols = [C.cash, C.spot, C.q, C.idea];
        var top = Math.max(12, Math.ceil(Math.min(40, Math.max.apply(null, vals)) / 4) * 4 + 2);
        var a = g[0].axes({ x: [0.4, 4.6], y: [0, top], title: "Expected bits per posting (green: entropy)", xticks: [1, 2, 3, 4], xfmt: function (t) { return names[t - 1]; } });
        a.bars([1, 2, 3, 4], vals.map(function (x) { return Math.min(x, top); }), 0.62, { color: function (i) { return cols[i]; } });
        a.hline(m.H, { color: C.gain, dash: [], width: 1.6 });
        for (kk = 0; kk < 4; kk++) a.text(kk + 1, Math.min(vals[kk], top - 1.2), fmt(vals[kk], 2), { align: "center", dy: -9, bold: true });
        var ks = [], rs = [];
        for (kk = 0; kk <= 12; kk++) { ks.push(kk); rs.push(m.rice[kk]); }
        var ytop = Math.max(14, Math.ceil(Math.max(m.H + 8, m.rice[best] + 6)));
        var b = g[1].axes({ x: [-0.4, 12.4], y: [0, ytop], title: "Rice code against k (green: entropy)", xlabel: "Rice parameter k (remainder bits)", xticks: [0, 2, 4, 6, 8, 10, 12] });
        b.hline(m.H, { color: C.gain, dash: [], width: 1.6 });
        b.vline(rule, { color: C.muted });
        b.line(ks, rs, { color: C.idea, width: 2 }).dots(ks, rs, { color: C.idea, r: 2.5 });
        b.dots([v.k], [Math.min(m.rice[v.k], ytop)], { color: C.ink, r: 5.5 });
        b.text(rule, ytop, "the rule's k", { color: C.muted, dx: 5, dy: 10 });
      },
      readout: function (v, s) {
        var m = s.out[0];
        return [["entropy", fmt(m.H, 2) + " bits"], ["Rice at this k", fmt(m.rice[v.k], 2)], ["best k", String(s.out[1])], ["the rule's k", String(s.out[2])],
          ["γ", fmt(m.gamma, 2)], ["variable byte", fmt(m.vbyte, 2)]];
      },
      note: "Exact expectations, no simulation. With no runs the gaps are geometric with the chosen mean, the model under which Golomb's code is optimal; a Rice code is a Golomb code whose parameter is a power of two: quotient in unary, k remainder bits. With runs, a share of the gaps equals 1 and the rest are longer, as in a list like 'whale', which is dense in one book and absent from the others.",
    });
  };
})();
