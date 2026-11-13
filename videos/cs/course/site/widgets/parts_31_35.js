// Interactives for Act VI, One Machine, Many Programs (Parts 31-34), and Part 35, Databases.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  function label(c, str, x, y, color, align, bold) { // custom-drawn text, 11.5px
    c.save(); c.font = (bold ? "600 12.5px" : "11.5px") + " system-ui, sans-serif"; c.fillStyle = color || C.ink;
    c.textAlign = align || "left"; c.textBaseline = "middle"; c.fillText(str, x, y); c.restore();
  }

  // ---- Part 31: one server, a load and a job-size law --------------------------------------------------------
  W.queuehockey = function (el) {
    var PLONG = 0.05, NJOBS = 4000, SPAN = 240;
    QB.widget(el, {
      title: "Why a busy server is slow: load, and the variance of the job size",
      sub: "One server, Poisson arrivals, mean job size 1. One job in twenty is long; the variability slider sets how long. Raise the load and the first-come-first-served curve bends up like a hockey stick; hold the load and raise the variability, and it rises again while processor sharing does not move.",
      panels: 2, height: 300,
      controls: [
        { k: "rho", label: "Load ρ = λ E[S]", min: 0.05, max: 0.95, step: 0.01, value: 0.8, fmt: function (x) { return x.toFixed(2); } },
        { k: "scv", label: "Size variability C² = Var(S) / E[S]²", min: 0, max: 16, step: 0.5, value: 1, fmt: function (x) { return x.toFixed(1); } },
      ],
      buttons: [{ label: "New arrivals", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var d = Math.sqrt(v.scv / (PLONG * (1 - PLONG))), small = 1 - PLONG * d, big = small + d; // two sizes, mean 1
        var pk = function (rho) { return 1 + rho * (1 + v.scv) / (2 * (1 - rho)); };
        var r = QB.rng(s.seed + 310), t = 0, free = 0, arr = [], dep = [], sum = 0, i;
        for (i = 0; i < NJOBS; i++) {
          t += -Math.log(1 - r()) / v.rho;
          free = Math.max(free, t) + (r() < PLONG ? big : small);
          arr.push(t); dep.push(free); sum += free - t;
        }
        s.out = [pk(v.rho), sum / NJOBS, 1 / (1 - v.rho), big];
        var rs = QB.linspace(0.02, 0.97, 96);
        var a = g[0].axes({ x: [0, 1], y: [1, 400], logy: true, title: "Mean response time against load", xlabel: "load ρ", yticks: [1, 3, 10, 30, 100, 400], yfmt: function (y) { return String(y); } });
        a.line(rs, rs.map(pk), { color: C.loss, width: 2.4 });
        a.line(rs, rs.map(function (x) { return 1 / (1 - x); }), { color: C.spot, width: 2, dash: [6, 5] });
        a.vline(v.rho, { color: C.idea });
        a.dots([v.rho], [Math.max(1, s.out[1])], { color: C.idea, r: 4.5 });
        a.legend([["first come, first served", C.loss], ["processor sharing (dashed)", C.spot], ["this run, simulated", C.idea]], { pos: "tl" });
        // the number in the system over the first SPAN time units: arrivals and departures are both in time order
        var xs = [0], ys = [0], ia = 0, id = 0, n = 0, top = 6, tt;
        while (ia < NJOBS && (arr[ia] < SPAN || dep[id] < SPAN)) {
          if (arr[ia] <= dep[id]) { tt = arr[ia]; ia++; xs.push(tt); ys.push(n); n++; } else { tt = dep[id]; id++; xs.push(tt); ys.push(n); n--; }
          if (tt > SPAN) break;
          xs.push(tt); ys.push(n); if (n > top) top = n;
        }
        xs.push(SPAN); ys.push(n);
        var b = g[1].axes({ x: [0, SPAN], y: [0, Math.ceil(top * 1.15)], title: "Jobs in the system, first " + SPAN + " time units", xlabel: "time (mean job sizes)" });
        b.area(xs, ys, 0, { color: C.loss, alpha: 0.22 }).line(xs, ys, { color: C.loss, width: 1.3 });
      },
      readout: function (v, s) {
        return [["FCFS, Pollaczek-Khinchine", fmt(s.out[0], 1)], ["FCFS, simulated", fmt(s.out[1], 1)], ["processor sharing", fmt(s.out[2], 1)], ["a long job", fmt(s.out[3], 1)]];
      },
      note: "Simulated data: 4,000 jobs per run, so near load 0.95 or at high variability one run can sit well off the formula. Response times are in mean job sizes. FCFS: E[T] = 1 + ρ(1 + C²)/(2(1 − ρ)); processor sharing: 1/(1 − ρ), whatever the size law.",
    });
  };
  // ---- Part 32: a reference string through FIFO, LRU and OPT -------------------------------------------------
  W.beladyframes = function (el) {
    var KINDS = ["Belady's string", "random, with locality", "five pages in a loop"], POL = ["FIFO", "LRU", "OPT"];
    var BELADY = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5];
    var replay = function (tr, k, pol) { // slots[i] = page in frame i (0 = empty); returns faults and every column
      var slots = [], load = [], used = [], cols = [], hits = [], f = 0, t, i, j, at, victim, key, best, nxt;
      for (i = 0; i < k; i++) { slots.push(0); load.push(-1); used.push(-1); }
      for (t = 0; t < tr.length; t++) {
        at = slots.indexOf(tr[t]);
        if (at < 0) {
          f++; victim = slots.indexOf(0);
          if (victim < 0) {
            best = null;
            for (i = 0; i < k; i++) {
              if (pol === 0) key = -load[i];
              else if (pol === 1) key = -used[i];
              else { nxt = 1e9; for (j = t + 1; j < tr.length; j++) if (tr[j] === slots[i]) { nxt = j; break; } key = nxt; }
              if (best === null || key > best) { best = key; victim = i; }
            }
          }
          slots[victim] = tr[t]; load[victim] = t; at = victim;
        }
        used[at] = t; hits.push(at >= 0 && load[at] !== t); cols.push({ s: slots.slice(), at: at });
      }
      return { f: f, cols: cols, hits: hits };
    };
    var trace = function (kind, loc, seed) {
      if (kind === 0) return BELADY;
      var out = [], i, r = QB.rng(seed + 320), recent = [];
      for (i = 0; i < 20; i++) {
        var p = kind === 2 ? 1 + i % 5 : (recent.length && r() < loc ? recent[Math.floor(r() * recent.length)] : 1 + Math.floor(r() * 6));
        out.push(p); recent = recent.filter(function (q) { return q !== p; }); recent.push(p); if (recent.length > 3) recent.shift();
      }
      return out;
    };
    QB.widget(el, {
      title: "Which page to evict: FIFO, LRU and OPT on one reference string",
      sub: "Left: page faults against the number of frames. Right: the frames after every reference under the chosen policy. On Belady's string, move the frames from 3 to 4 and FIFO faults more with more memory; LRU and OPT never do. Then try the loop of five pages with four frames.",
      panels: 2, height: 310, weights: [0.8, 1.2],
      controls: [
        { k: "kind", label: "Reference string", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return KINDS[x]; } },
        { k: "k", label: "Frames", min: 1, max: 7, step: 1, value: 3 },
        { k: "pol", label: "Policy shown on the right", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return POL[x]; } },
        { k: "loc", label: "Locality of the random string", min: 0, max: 0.95, step: 0.05, value: 0.7, fmt: function (x) { return x.toFixed(2); } },
      ],
      buttons: [{ label: "New random string", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var tr = trace(v.kind, v.loc, s.seed), ks = [1, 2, 3, 4, 5, 6, 7], cur = [[], [], []], p, i, t;
        var cols = [C.loss, C.spot, C.gain];
        for (p = 0; p < 3; p++) for (i = 0; i < ks.length; i++) cur[p].push(replay(tr, ks[i], p).f);
        var anomaly = false;
        for (i = 0; i + 1 < ks.length; i++) if (cur[0][i + 1] > cur[0][i]) anomaly = true;
        s.out = [cur[0][v.k - 1], cur[1][v.k - 1], cur[2][v.k - 1], anomaly];
        var a = g[0].axes({ x: [0.5, 7.5], y: [0, tr.length + 1], title: "Faults against frames", xlabel: "frames", xticks: ks });
        for (p = 2; p >= 0; p--) { a.line(ks, cur[p], { color: cols[p], width: 2 }); a.dots(ks, cur[p], { color: cols[p], r: 3 }); }
        a.vline(v.k, { color: C.idea });
        a.legend([["FIFO", C.loss], ["LRU", C.spot], ["OPT", C.gain]], { pos: "bl" });
        // the frames, reference by reference
        var run = replay(tr, v.k, v.pol), c = g.ctx, bx = g[1].box, n = tr.length;
        var cw = Math.min(36, (bx.w - 64) / n), ch = Math.min(30, (bx.h - 104) / v.k), x0 = bx.x + 54, y0 = bx.y + 58;
        label(c, POL[v.pol] + " with " + v.k + (v.k === 1 ? " frame: " : " frames: ") + run.f + " faults in " + n + " references", bx.x + 10, bx.y + 13, C.ink, "left", true);
        label(c, "page", bx.x + 10, y0 - 22, C.muted);
        for (i = 0; i < v.k; i++) label(c, "frame " + (i + 1), bx.x + 10, y0 + ch * (i + 0.5), C.muted);
        c.save(); c.font = "11.5px system-ui, sans-serif"; c.textAlign = "center"; c.textBaseline = "middle";
        for (t = 0; t < n; t++) {
          var X = x0 + cw * t;
          c.fillStyle = run.hits[t] ? C.muted : C.loss; c.fillText(String(tr[t]), X + cw / 2, y0 - 22);
          if (!run.hits[t]) { c.beginPath(); c.arc(X + cw / 2, y0 - 8, 2.2, 0, 6.2832); c.fill(); }
          for (i = 0; i < v.k; i++) {
            var pg = run.cols[t].s[i], here = run.cols[t].at === i;
            c.fillStyle = here ? (run.hits[t] ? "rgba(247,209,84,0.30)" : "rgba(248,113,113,0.45)") : "rgba(88,166,255,0.08)";
            c.fillRect(X + 0.5, y0 + ch * i + 0.5, cw - 1, ch - 1);
            if (pg) { c.fillStyle = here ? C.ink : C.muted; c.fillText(String(pg), X + cw / 2, y0 + ch * (i + 0.5)); }
          }
        }
        c.restore();
        var yl = y0 + ch * v.k + 16;
        c.fillStyle = "rgba(248,113,113,0.6)"; c.fillRect(bx.x + 10, yl - 5, 10, 10); label(c, "fault: page loaded", bx.x + 25, yl, C.muted);
        c.fillStyle = "rgba(247,209,84,0.45)"; c.fillRect(bx.x + 150, yl - 5, 10, 10); label(c, "hit", bx.x + 165, yl, C.muted);
      },
      readout: function (v, s) {
        return [["FIFO faults", String(s.out[0])], ["LRU", String(s.out[1])], ["OPT", String(s.out[2])], ["FIFO anomaly on this string", s.out[3] ? "yes" : "no"]];
      },
      note: "Exact replays, no simulation of time. OPT evicts the page whose next use is farthest away, which needs the future; LRU uses the past as its guess. The random string has 20 references to 6 pages; locality is the chance that a reference repeats one of the last three pages. The locality slider acts on the random string only.",
    });
  };
  // ---- Part 33: two threads, one counter ---------------------------------------------------------------------
  W.lostupdate = function (el) {
    var KIND = ["load, add, store", "atomic fetch-and-add"];
    var play = function (k, p, atomic, r, keep) { // one schedule; returns the final count (and the steps, if kept)
      var per = atomic ? 1 : 3, left = [k * per, k * per], pc = [0, 0], reg = [0, 0], c = 0, t = r() < 0.5 ? 0 : 1, steps = [], lost = 0, kind, stale;
      while (left[0] + left[1] > 0) {
        if (left[t] === 0) t = 1 - t;
        stale = false;
        if (atomic) { c++; kind = 3; }
        else {
          kind = pc[t] % 3;
          if (kind === 0) reg[t] = c; else if (kind === 1) reg[t]++; else { stale = reg[t] !== c + 1; if (stale) lost++; c = reg[t]; }
        }
        pc[t]++; left[t]--;
        if (keep) steps.push({ t: t, kind: kind, stale: stale, c: c });
        if (r() < p) t = 1 - t;
      }
      return { c: c, steps: steps, lost: lost };
    };
    QB.widget(el, {
      title: "Two threads, one counter: where the lost updates go",
      sub: "Each thread adds one to a shared counter k times, as load, add, store. The scheduler switches threads after a step with the chance you set. Left: one schedule, step by step. Right: the final count over 1,500 schedules. Lower the switch chance and the bug hides without going away; make the increment atomic and it is gone.",
      panels: 2, height: 300,
      controls: [
        { k: "k", label: "Increments per thread k", min: 1, max: 6, step: 1, value: 3 },
        { k: "p", label: "Chance of a switch after each step", min: 0.01, max: 1, step: 0.01, value: 0.3, fmt: function (x) { return x.toFixed(2); } },
        { k: "atomic", label: "The increment", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return KIND[x]; } },
      ],
      buttons: [{ label: "New schedule", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var one = play(v.k, v.p, v.atomic, QB.rng(s.seed + 330), true), r = QB.rng(s.seed + 331), top = 2 * v.k, h = [], i, ok = 0, sum = 0;
        for (i = 0; i <= top; i++) h.push(0);
        for (i = 0; i < 1500; i++) { var f = play(v.k, v.p, v.atomic, r, false).c; h[f]++; sum += f; if (f === top) ok++; }
        s.out = [one.c, top, one.lost, ok / 1500, sum / 1500];
        // the schedule: a row per thread, a cell per step, then the counter
        var c = g.ctx, bx = g[0].box, n = one.steps.length, cw = Math.min(22, (bx.w - 76) / n), x0 = bx.x + 62, y0 = bx.y + 40, ch = 26;
        var fill = [C.spot, C.cash, C.idea, C.gain];
        label(c, "One schedule: final count " + one.c + " of " + top, bx.x + 10, bx.y + 13, C.ink, "left", true);
        label(c, "thread A", bx.x + 10, y0 + ch / 2, C.muted); label(c, "thread B", bx.x + 10, y0 + ch * 1.5 + 4, C.muted);
        for (i = 0; i < n; i++) {
          var st = one.steps[i];
          c.fillStyle = st.stale ? C.loss : fill[st.kind]; c.globalAlpha = st.kind === 1 ? 0.55 : 0.9;
          c.fillRect(x0 + cw * i + 0.5, y0 + st.t * (ch + 4), Math.max(1, cw - 1), ch); c.globalAlpha = 1;
        }
        var yc = y0 + 2 * ch + 22, hc = Math.max(40, bx.h - (yc - bx.y) - 62);
        label(c, "counter", bx.x + 10, yc + hc / 2, C.muted);
        label(c, String(top), x0 - 6, yc, C.muted, "right"); label(c, "0", x0 - 6, yc + hc, C.muted, "right");
        c.save(); c.strokeStyle = C.line; c.strokeRect(x0 + 0.5, yc + 0.5, cw * n, hc);
        c.strokeStyle = C.ink; c.lineWidth = 1.8; c.beginPath(); c.moveTo(x0, yc + hc);
        var prev = 0;
        for (i = 0; i < n; i++) { c.lineTo(x0 + cw * (i + 1), yc + hc * (1 - prev / top)); prev = one.steps[i].c; c.lineTo(x0 + cw * (i + 1), yc + hc * (1 - prev / top)); }
        c.stroke(); c.restore();
        var yl = yc + hc + 18, items = v.atomic ? [["atomic add", C.gain]] : [["load", C.spot], ["add", C.cash], ["store", C.idea], ["stale store", C.loss]], xl = bx.x + 10;
        for (i = 0; i < items.length; i++) {
          c.fillStyle = items[i][1]; c.fillRect(xl, yl - 5, 10, 10); label(c, items[i][0], xl + 14, yl, C.muted);
          xl += 22 + c.measureText(items[i][0]).width * 1.2 + 12;
        }
        var xs = [], hs = [];
        for (i = 0; i <= top; i++) { xs.push(i); hs.push(h[i] / 1500); }
        var b = g[1].axes({ x: [-0.6, top + 0.6], y: [0, 1], title: "Final count over 1,500 schedules", xlabel: "final count (" + top + " is correct)", xticks: xs, yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.bars(xs, hs, 0.7, { color: function (j) { return j === top ? C.gain : C.loss; } });
        b.vline(one.c, { color: C.idea });
      },
      readout: function (v, s) {
        return [["this schedule ends at", s.out[0] + " of " + s.out[1]], ["stale stores in it", String(s.out[2])], ["schedules that end correct", QB.pct(s.out[3])], ["mean final count", fmt(s.out[4], 2)]];
      },
      note: "Simulated schedules on one processor. A store is stale (red) when the counter changed after that thread's load, so it writes over another update. The gold line on the right marks the schedule on the left. With real threads the switch chance per instruction is tiny, which is why the race passes tests.",
    });
  };
  // ---- Part 34: a flash translation layer and its garbage collector -------------------------------------------
  W.flashspare = function (el) {
    var B = 128, PP = 16, P = B * PP, GRID = [0.08, 0.12, 0.18, 0.25, 0.35, 0.5, 0.7];
    var ftl = function (op, hotW, trim, seed) { // greedy collection; returns write amplification and erase counts
      var L = Math.floor(P / (1 + op)), live = Math.max(64, Math.floor(L * (1 - trim))), hotN = Math.max(1, Math.floor(live * 0.1));
      var l2p = [], p2l = [], valid = [], erases = [], isFree = [], free = [], i, r = QB.rng(seed), active = 0, wp = 0, host = 0, fl = 0;
      for (i = 0; i < live; i++) l2p.push(-1);
      for (i = 0; i < P; i++) p2l.push(-1);
      for (i = 0; i < B; i++) { valid.push(0); erases.push(0); isFree.push(i > 0); if (i > 0) free.push(i); }
      var place = function (lp) {
        if (wp === PP) { if (!free.length) return false; active = free.shift(); isFree[active] = false; wp = 0; }
        var pp = active * PP + wp; wp++; l2p[lp] = pp; p2l[pp] = lp; valid[active]++; fl++; return true;
      };
      var gc = function () { // the block with the fewest valid pages: copy them forward, erase it
        var v = -1, b, k;
        for (b = 0; b < B; b++) if (b !== active && !isFree[b] && (v < 0 || valid[b] < valid[v])) v = b;
        if (v < 0 || valid[v] >= PP) return false;
        for (k = 0; k < PP; k++) { var lp = p2l[v * PP + k]; if (lp >= 0) { p2l[v * PP + k] = -1; valid[v]--; if (!place(lp)) return false; } }
        erases[v]++; isFree[v] = true; free.push(v); return true;
      };
      var write = function (lp) {
        var guard = 0;
        while (free.length < 2 && guard++ < 200) if (!gc()) break;
        if (l2p[lp] >= 0) { p2l[l2p[lp]] = -1; valid[Math.floor(l2p[lp] / PP)]--; }
        host++; return place(lp);
      };
      var pick = function () { return (hotW > 0.1001 && r() < hotW) ? Math.floor(r() * hotN) : Math.floor(r() * live); };
      for (i = 0; i < live; i++) write(i);
      for (i = 0; i < 1.5 * live; i++) write(pick());
      var h0 = host, f0 = fl, e0 = erases.slice();
      for (i = 0; i < 2.5 * live; i++) write(pick());
      var ed = erases.map(function (e, j) { return e - e0[j]; });
      return { wa: (fl - f0) / Math.max(1, host - h0), erases: ed, spare: (P - live) / live };
    };
    QB.widget(el, {
      title: "Flash: what spare capacity and TRIM buy",
      sub: "A simulated flash drive of 128 erase blocks. Every host write goes to a fresh page, and the collector must copy the still-valid pages of a block before erasing it. Lower the spare and the copies multiply; trim some of the data and they fall; send most writes to a tenth of the data and a few blocks take the wear.",
      panels: 2, height: 300,
      controls: [
        { k: "op", label: "Over-provisioning (spare / user capacity)", min: 8, max: 70, step: 1, value: 14, fmt: function (x) { return x + "%"; } },
        { k: "trim", label: "User data trimmed by the file system", min: 0, max: 50, step: 5, value: 0, fmt: function (x) { return x + "%"; } },
        { k: "hot", label: "Writes that go to the hottest 10% of the data", min: 10, max: 95, step: 5, value: 10, fmt: function (x) { return x === 10 ? "10% (uniform)" : x + "%"; } },
      ],
      buttons: [{ label: "New writes", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var one = ftl(v.op / 100, v.hot / 100, v.trim / 100, s.seed + 340), sim = GRID.map(function (p, i) { return ftl(p, v.hot / 100, v.trim / 100, s.seed + 341 + i).wa; });
        var ps = QB.linspace(0.06, 0.72, 80), sorted = one.erases.slice().sort(function (a, b) { return b - a; }), mean = QB.mean(sorted), xs = [], i;
        s.out = [one.wa, (1 + v.op / 100) / (2 * v.op / 100), sorted[0], mean];
        var a = g[0].axes({ x: [0, 0.75], y: [0, 9], title: "Flash writes per host write", xlabel: "over-provisioning p", xfmt: function (x) { return Math.round(100 * x) + "%"; } });
        a.line(ps, ps.map(function (p) { return (1 + p) / (2 * p); }), { color: C.idea, width: 2 });
        a.line(GRID, sim, { color: C.spot, width: 1.2, alpha: 0.6 }); a.dots(GRID, sim, { color: C.spot, r: 3 });
        a.hline(1, { color: C.muted });
        a.vline(v.op / 100, { color: C.muted });
        a.dots([v.op / 100], [Math.min(9, one.wa)], { color: C.loss, r: 5 });
        a.legend([["estimate (1 + p) / 2p", C.idea], ["simulated, these settings", C.spot], ["this drive", C.loss]], { pos: "tr" });
        for (i = 0; i < B; i++) xs.push(i + 1);
        var b = g[1].axes({ x: [0, B + 1], y: [0, Math.max(10, sorted[0] * 1.15)], title: "Erases per block, most worn first", xlabel: "erase blocks, sorted" });
        b.bars(xs, sorted, 1, { color: C.implied });
        b.hline(mean, { color: C.ink });
        b.text(B, mean, "mean " + fmt(mean, 1), { align: "right", dy: -9, bg: true });
      },
      readout: function (v, s) {
        return [["write amplification", fmt(s.out[0], 2)], ["estimate at this spare", fmt(s.out[1], 2)], ["most-erased block", String(s.out[2])], ["mean erases", fmt(s.out[3], 1)]];
      },
      note: "Simulated data: 2,048 pages, a greedy collector, random page writes measured after the drive has reached a steady state. The estimate assumes uniform writes and no TRIM, so the blue dots leave the gold curve when you move the other two sliders. Trimmed data acts as extra spare.",
    });
  };
  // ---- Part 35: three join algorithms and the memory they are given ------------------------------------------
  W.bufferjoins = function (el) {
    var NAMES = ["block nested loops", "sort-merge", "Grace hash"], COL = [C.loss, C.spot, C.gain];
    var sortCost = function (P, B) { var runs = Math.ceil(P / B), passes = 1; while (runs > 1) { runs = Math.ceil(runs / (B - 1)); passes++; } return { io: 2 * P * passes, passes: passes }; };
    var costs = function (M, N, B) {
      return { c: [M + Math.ceil(M / (B - 2)) * N, sortCost(M, B).io + sortCost(N, B).io + M + N, 3 * (M + N)],
        fits: Math.ceil(M / (B - 1)) <= B - 2, passes: Math.max(sortCost(M, B).passes, sortCost(N, B).passes) };
    };
    QB.widget(el, {
      title: "Three ways to join two tables, counted in page reads and writes",
      sub: "The outer table has M pages, the inner N, and the join may use B pages of memory. Left: each algorithm's cost against B. Right: the three costs at your B. Give the join plenty of memory and the simplest algorithm wins; take it away and hashing wins, until its buckets no longer fit.",
      panels: 2, height: 300, weights: [1.2, 0.8],
      controls: [
        { k: "M", label: "Outer table, M pages", min: 50, max: 2000, step: 50, value: 400 },
        { k: "N", label: "Inner table, N pages", min: 50, max: 2000, step: 50, value: 200 },
        { k: "B", label: "Buffer pages B", min: 3, max: 200, step: 1, value: 20 },
      ],
      draw: function (g, v, s) {
        var Bs = [], ys = [[], [], []], b, k, lo = 1e12, hi = 0, now = costs(v.M, v.N, v.B);
        for (b = 3; b <= 200; b++) {
          var c = costs(v.M, v.N, b); Bs.push(b);
          for (k = 0; k < 3; k++) { var val = k === 2 && !c.fits ? null : c.c[k]; ys[k].push(val); if (val !== null) { lo = Math.min(lo, val); hi = Math.max(hi, val); } }
        }
        var best = -1;
        for (k = 0; k < 3; k++) if ((k < 2 || now.fits) && (best < 0 || now.c[k] < now.c[best])) best = k;
        s.out = [now, best];
        var yr = [Math.pow(10, Math.floor(Math.log10(lo * 0.8))), Math.pow(10, Math.ceil(Math.log10(hi)))];
        var a = g[0].axes({ x: [3, 200], y: yr, logx: true, logy: true, title: "Page I/Os against buffer pages", xlabel: "buffer pages B", xticks: [3, 5, 10, 20, 50, 100, 200], xfmt: function (x) { return String(x); } });
        for (k = 0; k < 3; k++) a.line(Bs, ys[k], { color: COL[k], width: 2 });
        a.vline(v.B, { color: C.idea });
        a.legend([[NAMES[0], COL[0]], [NAMES[1], COL[1]], [NAMES[2] + ", where buckets fit", COL[2]]], { pos: "tr" });
        var top = Math.max(now.c[0], now.c[1], now.c[2]) * 1.22;
        var bb = g[1].axes({ x: [0.4, 3.6], y: [0, top], title: "At B = " + v.B, noX: true });
        bb.bars([1, 2, 3], now.c, 0.62, { color: function (j) { return COL[j]; }, alpha: 0.85 });
        var short = ["nested", "sort", "hash"];
        for (k = 0; k < 3; k++) {
          bb.text(k + 1, now.c[k], Math.round(now.c[k]).toLocaleString("en-US"), { align: "center", dy: -9, size: 11, color: k === best ? C.idea : C.ink, bold: k === best });
          bb.text(k + 1, 0, short[k], { align: "center", dy: -10, size: 11.5, color: C.bg, bold: true });
        }
        if (!now.fits) bb.text(3, now.c[2], "does not fit", { align: "center", dy: -24, size: 11, color: C.loss });
      },
      readout: function (v, s) {
        var now = s.out[0];
        return [["cheapest", NAMES[s.out[1]]], ["block nested loops", Math.round(now.c[0]).toLocaleString("en-US")], ["sort-merge", Math.round(now.c[1]).toLocaleString("en-US") + " (" + now.passes + (now.passes === 1 ? " pass)" : " passes)")], ["Grace hash", now.fits ? Math.round(now.c[2]).toLocaleString("en-US") : "buckets do not fit"]];
      },
      note: "Textbook formulas, no data: block nested loops M + ⌈M/(B − 2)⌉N; sort-merge 2M and 2N per sorting pass plus M + N to merge; Grace hash 3(M + N), valid while each of the B − 1 buckets of the outer table fits in B − 2 pages. Below that the hash join must partition again, which the green curve leaves out.",
    });
  };
})();
