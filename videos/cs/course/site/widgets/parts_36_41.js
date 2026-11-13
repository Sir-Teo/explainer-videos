// Interactives for Computer Science, Built, Parts 36-41: networks, agreement, scale, software engineering, version control.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;

  function rect(a, x1, x2, y1, y2, color, alpha) { // a filled rectangle in an Axes' data coordinates
    a.clip(function (c) {
      c.globalAlpha = alpha === undefined ? 1 : alpha; c.fillStyle = color;
      var X1 = a.px(x1), X2 = a.px(x2), Y1 = a.py(y1), Y2 = a.py(y2);
      c.fillRect(Math.min(X1, X2), Math.min(Y1, Y2), Math.max(1, Math.abs(X2 - X1)), Math.max(1, Math.abs(Y2 - Y1)));
    });
  }

  // ---- Part 36: ALOHA, offered load against throughput -------------------------------------------------------
  W.alohaload = function (el) {
    var names = ["pure ALOHA", "slotted ALOHA"];
    var arrivals = function (r, G, n, slotted) { // n frame start times of a Poisson process of rate G per frame time
      var t = 0, out = [], i;
      for (i = 0; i < n; i++) { var u = 0; while (u === 0) u = r(); t += -Math.log(u) / G; out.push(slotted ? Math.ceil(t) : t); }
      return out;
    };
    var verdicts = function (st, slotted) { // true where a frame meets no other frame
      var ok = [], i, gap = slotted ? 0.5 : 1;
      for (i = 0; i < st.length; i++) ok.push((i === 0 || st[i] - st[i - 1] >= gap) && (i === st.length - 1 || st[i + 1] - st[i] >= gap));
      return ok;
    };
    QB.widget(el, {
      title: "ALOHA: offer more, deliver less",
      sub: "Stations send frames of one time unit whenever they like, at a total rate of G attempts per frame time. Green frames met no other frame; red ones collided and are lost. Raise G past 0.5 and the measured throughput falls; switch to slots and the peak doubles.",
      panels: 2, height: 300,
      controls: [
        { k: "G", label: "Offered load G", min: 0.05, max: 3, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
        { k: "slot", label: "Protocol", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return names[x]; } },
      ],
      buttons: [{ label: "New traffic", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var slotted = v.slot === 1, r = QB.rng(s.seed + 360), st = arrivals(r, v.G, 3000, slotted), ok = verdicts(st, slotted);
        var i, good = 0, T = Math.max(1, st[st.length - 1]), rows = 5, ends = [], k;
        for (i = 0; i < ok.length; i++) if (ok[i]) good++;
        var theory = v.G * Math.exp(-(slotted ? 1 : 2) * v.G);
        s.out = [good / T, theory, good / ok.length, Math.exp(-(slotted ? 1 : 2) * v.G)];
        var a = g[0].axes({ x: [0, 24], y: [0, rows], noY: true, title: "The first 24 frame times on the channel", xlabel: "time, in frame times", xticks: [0, 4, 8, 12, 16, 20, 24] });
        if (slotted) for (i = 1; i < 24; i++) a.vline(i, { color: C.line, dash: [2, 3] });
        for (k = 0; k < rows; k++) ends.push(-1);
        for (i = 0; i < st.length && st[i] < 24; i++) {
          var row = -1, best = 0;
          for (k = 0; k < rows; k++) { if (ends[k] <= st[i]) { row = k; break; } if (ends[k] < ends[best]) best = k; }
          if (row < 0) row = best;
          ends[row] = st[i] + 1;
          rect(a, st[i], st[i] + 1, rows - 1 - row + 0.15, rows - row - 0.15, ok[i] ? C.gain : C.loss, 0.85);
        }
        a.legend([["delivered", C.gain], ["collided", C.loss]], { pos: "br" });
        var gs = QB.linspace(0.01, 3, 120), pure = gs.map(function (x) { return x * Math.exp(-2 * x); }), slot = gs.map(function (x) { return x * Math.exp(-x); });
        var b = g[1].axes({ x: [0, 3], y: [0, 0.45], title: "Throughput S against offered load G", xlabel: "offered load G" });
        b.line(gs, pure, { color: C.implied, width: slotted ? 1.2 : 2.4 }).line(gs, slot, { color: C.spot, width: slotted ? 2.4 : 1.2 });
        b.hline(slotted ? 1 / Math.E : 0.5 / Math.E);
        b.text(3, (slotted ? 1 / Math.E : 0.5 / Math.E), slotted ? "1/e" : "1/2e", { align: "right", dx: -4, dy: -9, color: C.muted });
        b.vline(v.G, { color: C.idea });
        b.dots([v.G], [Math.min(0.45, good / T)], { color: C.idea, r: 5 });
        b.legend([["G e^(−2G), pure", C.implied], ["G e^(−G), slotted", C.spot], ["measured here", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["throughput measured", fmt(s.out[0], 3)], ["formula", fmt(s.out[1], 3)], ["frames delivered", QB.pct(s.out[2])], ["formula", QB.pct(s.out[3])]];
      },
      note: "Simulated data: 3,000 attempts drawn as a Poisson process (new frames and retries together), as in Abramson's model. A pure-ALOHA frame survives if no other starts within one frame time either side; a slotted frame if it is alone in its slot.",
    });
  };

  // ---- Part 37: Chiu and Jain's phase plane ------------------------------------------------------------------
  W.aimdzigzag = function (el) {
    var rules = ["AIMD", "AIAD", "MIMD", "MIAD"], A = 0.03, M = 1.15, STEPS = 120;
    var jain = function (x, y) { var q = x * x + y * y; return q > 0 ? (x + y) * (x + y) / (2 * q) : 1; };
    QB.widget(el, {
      title: "Two users, one link, one bit of feedback",
      sub: "Each round both users learn only whether the link was overloaded, and both apply the same rule. The gold path is the pair of rates. Under AIMD it zig-zags to the green fairness line from any start; change the rule and the path keeps its difference, keeps its ratio, or starves a user.",
      panels: 2, height: 320,
      controls: [
        { k: "rule", label: "Rule (increase, decrease)", min: 0, max: 3, step: 1, value: 0, fmt: function (x) { return rules[x]; } },
        { k: "x1", label: "User 1 starts at", min: 0.05, max: 0.9, step: 0.05, value: 0.1, fmt: function (x) { return x.toFixed(2); } },
        { k: "x2", label: "User 2 starts at", min: 0.05, max: 0.9, step: 0.05, value: 0.6, fmt: function (x) { return x.toFixed(2); } },
        { k: "b", label: "Multiplicative decrease b", min: 0.3, max: 0.9, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2); } },
      ],
      draw: function (g, v, s) {
        var x = v.x1, y = v.x2, xs = [x], ys = [y], t = [0], i, addUp = v.rule < 2, mulDown = v.rule === 0 || v.rule === 2;
        for (i = 1; i <= STEPS; i++) {
          if (x + y > 1) { if (mulDown) { x *= v.b; y *= v.b; } else { x = Math.max(0, x - A); y = Math.max(0, y - A); } }
          else if (addUp) { x += A; y += A; } else { x *= M; y *= M; }
          xs.push(x); ys.push(y); t.push(i);
        }
        var f = 0, e = 0;
        for (i = STEPS - 19; i <= STEPS; i++) { f += jain(xs[i], ys[i]) / 20; e += (xs[i] + ys[i]) / 20; }
        s.out = [f, e, Math.abs(xs[STEPS] - ys[STEPS]), jain(v.x1, v.x2)];
        var a = g[0].axes({ x: [0, 1.2], y: [0, 1.2], title: "The plane of rates: " + rules[v.rule], xlabel: "user 1's rate (link capacity = 1)" });
        a.line([0, 1], [1, 0], { color: C.muted, dash: [5, 4], width: 1.3 });
        a.line([0, 1.2], [0, 1.2], { color: C.gain, width: 1.3 });
        a.line(xs, ys, { color: C.idea, width: 1.6 });
        a.dots([v.x1], [v.x2], { color: C.ink, r: 4 });
        a.dots([xs[STEPS]], [ys[STEPS]], { color: C.idea, r: 4.5 });
        a.legend([["path, from the white dot", C.idea], ["fair: equal rates", C.gain], ["full: rates sum to 1", C.muted]], { pos: "br" });
        var b = g[1].axes({ x: [0, STEPS], y: [0, 1.4], title: "The two rates, round by round", xlabel: "round" });
        b.hline(1, { color: C.muted });
        b.line(t, xs, { color: C.spot }).line(t, ys, { color: C.implied });
        b.legend([["user 1", C.spot], ["user 2", C.implied]], { pos: "tr" });
      },
      readout: function (v, s) {
        return [["Jain's index at the start", fmt(s.out[3], 3)], ["over the last 20 rounds", fmt(s.out[0], 3)], ["mean load", QB.pct(s.out[1], 0)], ["gap between the users", fmt(s.out[2], 3)]];
      },
      note: "Chiu and Jain's model, with no randomness: additive steps are 0.03 of the link, multiplicative increase is by 1.15, and a decrease happens whenever the rates sum to more than 1. Jain's index is (x1 + x2)² / 2(x1² + x2²): 1 when shares are equal, 0.5 when one user has everything.",
    });
  };

  // ---- Part 38: Raft's randomized election timeouts ----------------------------------------------------------
  W.raftsplitvote = function (el) {
    var T = 150, CAP = 40, TRIALS = 400;
    var term = function (r, n, spread, d) { // one term: who times out, who becomes a candidate, who wins (or -1)
      var to = [], i, k, first = 0;
      for (i = 0; i < n; i++) { to.push(T * (1 + spread * r())); if (to[i] < to[first]) first = i; }
      var cand = [], votes = [];
      for (i = 0; i < n; i++) { cand.push(to[i] <= to[first] + d); votes.push(cand[i] ? 1 : 0); }
      for (i = 0; i < n; i++) {
        if (cand[i]) continue;
        var best = -1, bt = 0;
        for (k = 0; k < n; k++) if (cand[k]) { var at = to[k] + d * (0.5 + 0.5 * r()); if (best < 0 || at < bt) { best = k; bt = at; } }
        votes[best]++;
      }
      var win = -1;
      for (i = 0; i < n; i++) if (votes[i] > n / 2) win = i;
      return { to: to, cand: cand, votes: votes, win: win, first: first };
    };
    QB.widget(el, {
      title: "Split votes: why Raft randomizes its election timeouts",
      sub: "The leader has crashed. Each server waits a timeout drawn between T and T(1 + spread), then stands as a candidate; a server that times out before a rival's request reaches it stands too, and votes for itself. Shrink the spread to zero, or lengthen the message delay, and elections end with no majority, term after term.",
      panels: 2, height: 300,
      controls: [
        { k: "spread", label: "Spread of the timeout", min: 0, max: 1, step: 0.01, value: 1, fmt: function (x) { return "[T, " + (1 + x).toFixed(2) + " T]"; } },
        { k: "d", label: "Message delay", min: 1, max: 40, step: 1, value: 10, fmt: function (x) { return x + " ms"; } },
        { k: "n", label: "Servers", min: 3, max: 9, step: 2, value: 5 },
      ],
      buttons: [{ label: "New election", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var one = term(QB.rng(s.seed + 380), v.n, v.spread, v.d), r = QB.rng(s.seed + 381), i, k;
        var hist = [0, 0, 0, 0, 0, 0, 0], never = 0, sum = 0, done = 0;
        for (i = 0; i < TRIALS; i++) {
          for (k = 1; k <= CAP; k++) if (term(r, v.n, v.spread, v.d).win >= 0) break;
          if (k > CAP) { never++; hist[6]++; } else { sum += k; done++; hist[Math.min(k, 6) - 1]++; }
        }
        s.out = [hist[0] / TRIALS, done ? sum / done : 0, never / TRIALS, done];
        var a = g[0].axes({ x: [0, 2 * T + 40], y: [0, v.n], noY: true, xlabel: "milliseconds since the leader fell silent (T = 150 ms)",
          title: "One election: " + (one.win >= 0 ? "server " + (one.win + 1) + " wins with " + one.votes[one.win] + " of " + v.n + " votes" : "split vote, no leader this term") });
        rect(a, one.to[one.first], one.to[one.first] + v.d, 0, v.n, C.loss, 0.22);
        for (i = 0; i < v.n; i++) {
          rect(a, 0, one.to[i], v.n - 1 - i + 0.2, v.n - i - 0.2, one.cand[i] ? C.idea : C.spot, i === one.win ? 1 : 0.6);
          a.text(4, v.n - i - 0.5, "S" + (i + 1) + (one.cand[i] ? ": candidate, " + one.votes[i] + (one.votes[i] === 1 ? " vote" : " votes") : ""), { color: C.bg, bold: true, size: 11 });
        }
        var b = g[1].axes({ x: [0.4, 7.6], y: [0, 1], title: "Terms needed to elect a leader, " + TRIALS + " elections", xlabel: "terms",
          xticks: [1, 2, 3, 4, 5, 6, 7], xfmt: function (x) { return x === 6 ? "6+" : x === 7 ? "never" : String(x); }, yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.bars([1, 2, 3, 4, 5, 6, 7], hist.map(function (h) { return h / TRIALS; }), 0.8, { color: function (j) { return j === 6 ? C.loss : j === 0 ? C.gain : C.spot; } });
      },
      readout: function (v, s) {
        return [["elected in the first term", QB.pct(s.out[0])], ["mean terms when elected", s.out[3] ? fmt(s.out[1], 2) : "none elected"], ["no leader in " + CAP + " terms", QB.pct(s.out[2])]];
      },
      note: "Left: gold servers timed out and stood as candidates, blue ones heard a request first, and the red band is the first request in flight. Simulated data, in a simplified model of one election: every server is up, logs are equal, each server votes for the first request it receives (after a delay between half and all of the message delay), and a failed term starts afresh. The series' full Raft, with real logs and faults, is in the lab.",
    });
  };

  // ---- Part 39: quorums and bounded staleness ----------------------------------------------------------------
  W.quorumoverlap = function (el) {
    var TRIALS = 3000, WM = 10, RM = 5; // mean write delay to a replica, mean one-way read delay (ms)
    var trial = function (r, N, R, Wq) { // one write then one read; returns what happened, with times relative to the ack
      var ex = function (m) { var u = 0; while (u === 0) u = r(); return -m * Math.log(u); };
      var arr = [], req = [], rt = [], i, order = [];
      for (i = 0; i < N; i++) { arr.push(ex(WM)); req.push(ex(RM)); rt.push(req[i] + ex(RM)); order.push(i); }
      var sorted = arr.slice().sort(function (a, b) { return a - b; }), ack = sorted[Wq - 1];
      order.sort(function (a, b) { return rt[a] - rt[b]; });
      var need = Infinity; // the read is fresh once t reaches the smallest (arrival - ack - request delay) among the first R
      for (i = 0; i < R; i++) need = Math.min(need, arr[order[i]] - ack - req[order[i]]);
      return { arr: arr, req: req, ack: ack, first: order.slice(0, R), need: need };
    };
    QB.widget(el, {
      title: "R + W > N: when a read must meet the last write",
      sub: "A write goes to all N replicas and is acknowledged when W have it; t milliseconds later a read asks all N and takes the newest of the first R answers. Make R + W exceed N and the stale share is exactly zero. Lower R or W to answer sooner, and reads miss the write until the laggards catch up.",
      panels: 2, height: 300,
      controls: [
        { k: "N", label: "Replicas N", min: 3, max: 7, step: 1, value: 3 },
        { k: "R", label: "Read quorum R (at most N)", min: 1, max: 7, step: 1, value: 1 },
        { k: "W", label: "Write quorum W (at most N)", min: 1, max: 7, step: 1, value: 1 },
        { k: "t", label: "Read follows the ack by t", min: 0, max: 60, step: 1, value: 5, fmt: function (x) { return x + " ms"; } },
      ],
      buttons: [{ label: "New write", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var N = v.N, R = Math.min(v.R, N), Wq = Math.min(v.W, N), i, k;
        var one = trial(QB.rng(s.seed + 390), N, R, Wq), r = QB.rng(s.seed + 391), needs = [];
        for (i = 0; i < TRIALS; i++) needs.push(trial(r, N, R, Wq).need);
        var ts = QB.linspace(0, 60, 61), ps = ts.map(function (t) { var c = 0; for (k = 0; k < TRIALS; k++) if (needs[k] > t) c++; return c / TRIALS; });
        var stale = one.need > v.t;
        s.out = [R, Wq, N, ps[Math.round(v.t)], ps[0], stale];
        var a = g[0].axes({ x: [0, 80], y: [0, N], noY: true, xlabel: "milliseconds since the write was sent", xticks: [0, 20, 40, 60, 80],
          title: "One write, one read: the read is " + (stale ? "STALE" : "fresh") });
        var readAt = one.ack + v.t;
        for (i = 0; i < N; i++) {
          var y1 = N - 1 - i + 0.22, y2 = N - i - 0.22;
          rect(a, 0, Math.min(80, one.arr[i]), y1, y2, C.cash, 0.45);
          if (one.arr[i] < 80) rect(a, one.arr[i], 80, y1, y2, C.gain, 0.45);
          var hit = readAt + one.req[i], isFirst = one.first.indexOf(i) >= 0;
          if (hit <= 80) a.dots([hit], [N - i - 0.5], { color: one.arr[i] <= hit ? C.ink : C.loss, r: isFirst ? 6 : 3 });
        }
        a.vline(Math.min(80, one.ack), { color: C.idea, dash: [], width: 1.6 });
        if (readAt <= 80) a.vline(readAt, { color: C.spot, dash: [], width: 1.6 });
        var b = g[1].axes({ x: [0, 60], y: [0, 1], title: "Stale reads against t, for N = " + N + ", R = " + R + ", W = " + Wq, xlabel: "t, milliseconds after the ack", yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        b.area(ts, ps, 0, { color: C.loss, alpha: 0.2 }).line(ts, ps, { color: C.loss, width: 2 });
        b.vline(v.t, { color: C.spot });
        b.dots([v.t], [ps[Math.round(v.t)]], { color: C.spot, r: 5 });
        b.text(58, 0.9, R + Wq > N ? "R + W > N: never stale" : "R + W ≤ N: quorums can miss each other", { align: "right", color: R + Wq > N ? C.gain : C.loss, bold: true, bg: true });
      },
      readout: function (v, s) {
        return [["R + W", s.out[0] + " + " + s.out[1] + (s.out[0] + s.out[1] > s.out[2] ? " > " : " ≤ ") + s.out[2]], ["stale reads at t", QB.pct(s.out[3])], ["at t = 0", QB.pct(s.out[4])]];
      },
      note: "Simulated data: 3,000 writes, with exponential delays (mean 10 ms for the write to reach a replica, 5 ms each way for the read), the model of probabilistically bounded staleness. Left: each replica is grey while it holds the old value and green once it has the write; the gold line is the acknowledgement and the blue line the read. Dots are the read reaching each replica, large for the first R to answer, red where the replica still holds the old value.",
    });
  };

  // ---- Part 40: Brooks' law, with its condition --------------------------------------------------------------
  W.brookslate = function (el) {
    var WORK = 120, TEAM = 6, MENTOR = 0.5, DT = 0.05, CAP = 80;
    var project = function (addAt, add, ramp, cost, trace) { // the part's model: returns the finishing month
      var t = 0, done = 0, joined = false, n, eff, out, frac;
      while (done < WORK && t < CAP) {
        if (add > 0 && t >= addAt) joined = true;
        n = TEAM + (joined ? add : 0); eff = Math.max(0, 1 - cost * (n - 1)); out = TEAM * eff;
        if (joined) { frac = ramp > 0 ? Math.min(1, (t - addAt) / ramp) : 1; out += add * eff * frac; if (frac < 1) out -= add * MENTOR * eff; }
        done += Math.max(0, out) * DT; t += DT;
        if (trace) { trace[0].push(t); trace[1].push(Math.min(WORK, done)); }
      }
      return t;
    };
    QB.widget(el, {
      title: "Adding people to a late project",
      sub: "A project of 120 person-months has six people. More join in the month you choose: each newcomer needs months to reach full speed, takes half of an experienced person's time meanwhile, and adds a channel to everyone. Add them in month 2 and the project finishes sooner; slide the month to the right and Brooks' law appears.",
      panels: 2, height: 300,
      controls: [
        { k: "at", label: "Month the newcomers join", min: 0, max: 24, step: 1, value: 16 },
        { k: "add", label: "People added", min: 0, max: 12, step: 1, value: 4 },
        { k: "ramp", label: "Months to reach full speed", min: 0, max: 12, step: 1, value: 6 },
        { k: "cost", label: "Time lost per colleague", min: 0, max: 0.04, step: 0.005, value: 0.02, fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
      ],
      draw: function (g, v, s) {
        var tr0 = [[0], [0]], tr1 = [[0], [0]], base = project(0, 0, v.ramp, v.cost, tr0), fin = project(v.at, v.add, v.ramp, v.cost, tr1);
        var ms = [], fs = [], m, best = 0;
        for (m = 0; m <= 24; m++) { ms.push(m); fs.push(project(m, v.add, v.ramp, v.cost, null)); if (fs[m] < fs[best]) best = m; }
        var n = TEAM + v.add;
        s.out = [base, fin, fin - base, n * (n - 1) / 2];
        var xmax = Math.max(30, Math.ceil(Math.max(base, fin) / 5) * 5 + 5);
        var a = g[0].axes({ x: [0, xmax], y: [0, 135], title: "Work done, in person-months", xlabel: "month" });
        a.hline(WORK, { color: C.muted });
        a.text(xmax, WORK, "done: 120", { align: "right", dx: -4, dy: -9, color: C.muted });
        a.line(tr0[0], tr0[1], { color: C.spot, width: 1.6 }).line(tr1[0], tr1[1], { color: C.idea, width: 2.2 });
        if (v.add > 0) a.vline(v.at, { color: C.idea });
        a.legend([["six people throughout", C.spot], ["with " + v.add + " added in month " + v.at, C.idea]], { pos: "br" });
        var lo = Math.min(base, Math.min.apply(null, fs)), hi = Math.max(base, Math.max.apply(null, fs));
        var b = g[1].axes({ x: [0, 24], y: [Math.floor(lo - 1.5), Math.ceil(hi + 1.5)], title: "Finishing month, by when they join", xlabel: "month the newcomers join", xticks: [0, 4, 8, 12, 16, 20, 24] });
        b.area(ms, fs.map(function (f) { return Math.max(f, base); }), base, { color: C.loss, alpha: 0.3 });
        b.hline(base, { color: C.spot });
        b.line(ms, fs, { color: C.idea, width: 2 });
        b.dots([v.at], [fs[v.at]], { color: C.idea, r: 5 });
        b.legend([["with newcomers", C.idea], ["nobody added", C.spot], ["later than doing nothing", C.loss]], { pos: "br" });
      },
      readout: function (v, s) {
        return [["nobody added: month", fmt(s.out[0], 1)], ["with newcomers: month", fmt(s.out[1], 1)], [s.out[2] > 0.05 ? "later by (months)" : "sooner by (months)", fmt(Math.abs(s.out[2]), 1)], ["channels in the team", String(s.out[3])]];
      },
      note: "The film's model, not data: every person produces one person-month a month, less the share lost to each colleague (n(n − 1)/2 channels in all); newcomers ramp up linearly and each occupies half a mentor until then. Brooks' law holds when the ramp is long compared with the time left.",
    });
  };

  // ---- Part 41: a merge queue that tests batches and bisects failures ----------------------------------------
  W.queuebisect = function (el) {
    var SIZES = [1, 2, 4, 8, 16, 32, 64], CHANGES = 6400;
    var resolve = function (bad, lo, hi, depth, log) { // test bad[lo..hi); on red, split in halves; returns test runs
      var red = false, i;
      for (i = lo; i < hi; i++) if (bad[i]) { red = true; break; }
      if (log) log.push([lo, hi, depth, red]);
      if (!red || hi - lo === 1) return 1;
      var mid = lo + Math.floor((hi - lo) / 2);
      return 1 + resolve(bad, lo, mid, depth + 1, log) + resolve(bad, mid, hi, depth + 1, log);
    };
    QB.widget(el, {
      title: "A merge queue: test a batch, bisect when it is red",
      sub: "Changes wait in a queue and are tested a batch at a time on top of main. A green batch lands whole after one test run; a red one is split in halves and each half tested, down to the guilty changes. With few bad changes, big batches cost a fraction of a run per change. Raise the share of bad changes and big batches are nearly always red.",
      panels: 2, height: 300,
      controls: [
        { k: "p", label: "Share of changes that break the tests", min: 0.5, max: 25, step: 0.5, value: 3, fmt: function (x) { return x.toFixed(1) + "%"; } },
        { k: "k", label: "Batch size", min: 0, max: 6, step: 1, value: 4, fmt: function (x) { return String(SIZES[x]); } },
      ],
      buttons: [{ label: "New batch", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var p = v.p / 100, b = SIZES[v.k], r = QB.rng(s.seed + 410), one = [], log = [], i, j;
        for (i = 0; i < b; i++) one.push(r() < p);
        var runsOne = resolve(one, 0, b, 0, log), nBad = 0;
        for (i = 0; i < b; i++) if (one[i]) nBad++;
        var r2 = QB.rng(s.seed + 411), all = [], per = [], best = 0;
        for (i = 0; i < CHANGES; i++) all.push(r2() < p);
        for (j = 0; j < SIZES.length; j++) {
          var runs = 0;
          for (i = 0; i < CHANGES; i += SIZES[j]) runs += resolve(all, i, i + SIZES[j], 0, null);
          per.push(runs / CHANGES); if (per[j] < per[best]) best = j;
        }
        s.out = [Math.pow(1 - p, b), per[v.k], SIZES[best], per[best], runsOne, nBad];
        var rows = 8, a = g[0].axes({ x: [0, b], y: [0, rows], noY: true, noX: true,
          title: "This batch of " + b + ": " + runsOne + (runsOne === 1 ? " test run, " : " test runs, ") + nBad + " rejected" });
        for (i = 0; i < log.length; i++) rect(a, log[i][0] + 0.04 * b / 16, log[i][1] - 0.04 * b / 16, rows - 1 - log[i][2] + 0.14, rows - log[i][2] - 0.14, log[i][3] ? C.loss : C.gain, 0.8);
        for (i = 0; i < b; i++) rect(a, i + 0.1, i + 0.9, 0.1, 0.75, one[i] ? C.loss : C.cash, one[i] ? 1 : 0.55);
        var ymax = Math.max(1.6, Math.ceil(Math.max.apply(null, per) * 5) / 5);
        var c = g[1].axes({ x: [-0.4, 6.4], y: [0, ymax], title: "Test runs per change, by batch size", xlabel: "batch size", xticks: [0, 1, 2, 3, 4, 5, 6], xfmt: function (x) { return String(SIZES[x]); } });
        c.hline(1, { color: C.muted });
        c.text(6.4, 1, "one run per change", { align: "right", dx: -4, dy: -9, color: C.muted });
        c.bars([0, 1, 2, 3, 4, 5, 6], per, 0.7, { color: function (q) { return q === v.k ? C.idea : q === best ? C.gain : C.spot; } });
        c.legend([["this batch size", C.idea], ["cheapest", C.gain]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["a batch is green with probability", QB.pct(s.out[0])], ["test runs per change", fmt(s.out[1], 3)], ["cheapest batch size", String(s.out[2])], ["its runs per change", fmt(s.out[3], 3)]];
      },
      note: "Left: each bar is one test run over the changes beneath it, green if it passed and the group landed, red if it failed and was split; the bottom row is the changes, red for the bad ones. Simulated data: 6,400 changes, each bad independently with the chosen probability; a bad change always fails the tests and changes do not interact. Only tested combinations land, so main stays green at every batch size; what changes is the cost.",
    });
  };
})();
