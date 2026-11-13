// Interactives for Acts III and IV, Knowledge and Science (Parts 13-18).
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;
  function f2(x) { return x.toFixed(2); }
  function squareBox(b) { // shrink a panel's box so that the plot area inside the axes is square
    var side = Math.max(120, Math.min(b.w - 58, b.h - 56));
    return { x: b.x + (b.w - side - 58) / 2, y: b.y + (b.h - side - 56) / 2, w: side + 58, h: side + 56 };
  }

  // ---- Part 13: a credence in A and in not-A; the Dutch book and the accuracy argument --------------------------
  W.dutchbrier = function (el) {
    QB.widget(el, {
      title: "Off the line: a sure loss and a worse score in every world",
      sub: "The gold point is a credence in A and a credence in not-A. The white line is where they sum to 1. Off the line, the green point (the nearest coherent credence) is closer to both corners of truth, and a bookie has a sure profit. Move the point onto the line and both complaints vanish.",
      panels: 2, height: 310,
      controls: [
        { k: "a", label: "Credence in A", min: 0, max: 1, step: 0.01, value: 0.6, fmt: f2 },
        { k: "b", label: "Credence in not-A", min: 0, max: 1, step: 0.01, value: 0.6, fmt: f2 },
      ],
      draw: function (g, v, s) {
        var t = Math.max(0, Math.min(1, (v.a - v.b + 1) / 2)), p = [t, 1 - t];
        var bA = (v.a - 1) * (v.a - 1) + v.b * v.b, bN = v.a * v.a + (v.b - 1) * (v.b - 1);
        var pA = (p[0] - 1) * (p[0] - 1) + p[1] * p[1], pN = p[0] * p[0] + (p[1] - 1) * (p[1] - 1);
        s.out = { sum: v.a + v.b, loss: Math.abs(v.a + v.b - 1), bA: bA, bN: bN, pA: pA, pN: pN };
        var box = g[0].box, sq = squareBox(box); box.x = sq.x; box.y = sq.y; box.w = sq.w; box.h = sq.h;
        var a = g[0].axes({ x: [0, 1], y: [0, 1], title: "Credence space", xlabel: "credence in A", nx: 4, ny: 4 });
        var th = QB.linspace(0, Math.PI / 2, 40), i, xs = [], ys = [], xs2 = [], ys2 = [];
        var rA = Math.sqrt(bA), rN = Math.sqrt(bN);
        for (i = 0; i < th.length; i++) {
          xs.push(1 - rA * Math.cos(th[i])); ys.push(rA * Math.sin(th[i]));
          xs2.push(rN * Math.sin(th[i])); ys2.push(1 - rN * Math.cos(th[i]));
        }
        a.line(xs, ys, { color: C.spot, width: 1.2, dash: [3, 3] });
        a.line(xs2, ys2, { color: C.q, width: 1.2, dash: [3, 3] });
        a.line([0, 1], [1, 0], { color: C.ink, width: 1.6 });
        a.line([v.a, p[0]], [v.b, p[1]], { color: C.gain, width: 1.5 });
        a.dots([1], [0], { color: C.spot, r: 5 }); a.dots([0], [1], { color: C.q, r: 5 });
        a.dots([p[0]], [p[1]], { color: C.gain, r: 5 }); a.dots([v.a], [v.b], { color: C.idea, r: 6 });
        a.text(1, 0, "A true", { color: C.spot, align: "right", dx: -12, dy: -12 });
        a.text(0, 1, "A false", { color: C.q, dx: 12, dy: 12 });
        var m = Math.max(1.05, Math.max(bA, bN) * 1.1);
        var b = g[1].axes({ x: [0, 8], y: [0, m], title: "Penalty (Brier) and the bookie's profit", xticks: [1.5, 4.5, 7],
          xfmt: function (x) { return x < 2 ? "if A" : x < 5 ? "if not-A" : "sure loss"; } });
        b.bars([1, 4], [bA, bN], 0.9, { color: C.idea });
        b.bars([2, 5], [pA, pN], 0.9, { color: C.gain });
        b.bars([7], [s.out.loss], 0.9, { color: C.loss });
        b.legend([["your credence", C.idea], ["nearest coherent", C.gain], ["bookie's sure profit", C.loss]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["sum of credences", f2(o.sum)], ["sure loss per unit stake", o.loss < 0.005 ? "none: coherent" : f2(o.loss)],
          ["Brier if A: yours, coherent", f2(o.bA) + ", " + f2(o.pA)], ["if not-A", f2(o.bN) + ", " + f2(o.pN)]];
      },
      note: "The dotted arcs pass through your point, centred on each truth corner: any point inside both arcs is more accurate in both worlds. The bookie sells you both bets when the sum exceeds 1 and buys both when it is below 1, at your own prices, with stakes of 1.",
    });
  };

  // ---- Part 14: Grove's spheres over four worlds; expansion against revision -------------------------------------
  W.grovespheres = function (el) {
    var names = ["pq", "p¬q", "¬pq", "¬p¬q"], keys = ["w0", "w1", "w2", "w3"];
    var news = [ // the sentence learned, as the set of worlds where it is true
      ["¬p", [0, 0, 1, 1]], ["¬q", [0, 1, 0, 1]], ["¬p ∨ ¬q", [0, 1, 1, 1]], ["p ↔ ¬q", [0, 1, 1, 0]], ["¬p ∧ ¬q", [0, 0, 0, 1]], ["p", [1, 1, 0, 0]],
    ];
    function rk(label, k, val) { return { k: k, label: "Rank of " + label, min: 0, max: 3, step: 1, value: val }; }
    function setName(inSet) { var o = []; for (var i = 0; i < 4; i++) if (inSet[i]) o.push(names[i]); return o.length ? o.join(", ") : "none"; }
    QB.widget(el, {
      title: "Grove's spheres: learn a sentence that contradicts what you believe",
      sub: "Four worlds sit on spheres by rank: rank 0, the centre, is what you believe. Press the button to change the news A (outlined in blue). Expansion keeps only the believed worlds where A holds, and can leave nothing. Revision moves to the most plausible A-worlds (gold), so it stays consistent. Change the ranks and watch what revision keeps.",
      panels: 2, height: 320,
      controls: [rk("pq", "w0", 0), rk("p¬q", "w1", 1), rk("¬pq", "w2", 2), rk("¬p¬q", "w3", 3)],
      buttons: [{ label: "Next news", act: function (s) { s.k = ((s.k || 0) + 1) % news.length; } }],
      init: function (s) { s.k = 0; },
      draw: function (g, v, s) {
        var i, r = [], m = 9, A = news[s.k || 0][1], c = g.ctx;
        for (i = 0; i < 4; i++) m = Math.min(m, v[keys[i]]);
        for (i = 0; i < 4; i++) r.push(v[keys[i]] - m);
        var K = [], exp = [], rev = [], best = 9;
        for (i = 0; i < 4; i++) if (A[i]) best = Math.min(best, r[i]);
        for (i = 0; i < 4; i++) { K.push(r[i] === 0 ? 1 : 0); exp.push(K[i] && A[i] ? 1 : 0); rev.push(A[i] && r[i] === best ? 1 : 0); }
        s.out = { K: K, exp: exp, rev: rev, ent: best, name: news[s.k || 0][0] };
        // left: the spheres
        var b = g[0].box, cx = b.x + b.w / 2, cy = b.y + b.h / 2 + 8, R = Math.min(b.w, b.h - 24) / 2 - 8;
        var rad = [0.36 * R, 0.58 * R, 0.79 * R, R], ang = [-0.75, -0.25, 0.75, 0.25];
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("Spheres of plausibility", b.x + 12, b.y + 6);
        for (i = 3; i >= 0; i--) {
          c.beginPath(); c.arc(cx, cy, rad[i], 0, 6.2832);
          c.fillStyle = i === 0 ? "rgba(230,237,243,0.10)" : "rgba(88,166,255,0.035)"; c.fill();
          c.strokeStyle = i === 0 ? C.ink : "#3a475c"; c.lineWidth = i === 0 ? 1.4 : 1; c.stroke();
        }
        c.font = "11px system-ui, sans-serif"; c.textAlign = "center"; c.textBaseline = "middle";
        for (i = 0; i < 4; i++) {
          var mid = r[i] === 0 ? 0.6 * rad[0] : (rad[r[i] - 1] + rad[r[i]]) / 2, th = ang[i] * Math.PI;
          var x = cx + mid * Math.cos(th) * (r[i] === 0 ? 1 : 0.92), y = cy + mid * Math.sin(th);
          var tw = c.measureText(names[i]).width + 10;
          if (rev[i]) { c.fillStyle = C.idea; c.fillRect(x - tw / 2, y - 9, tw, 18); }
          if (A[i]) { c.strokeStyle = C.spot; c.lineWidth = 1.6; c.strokeRect(x - tw / 2, y - 9, tw, 18); }
          c.fillStyle = rev[i] ? "#0e1117" : K[i] ? C.ink : C.muted; c.fillText(names[i], x, y);
        }
        // right: the four sets as rows of cells
        var d = g[1].box, rows = [["K: believed now", K, C.ink], ["A: the news", A, C.spot], ["K + A: expansion", exp, C.loss], ["K * A: revision", rev, C.idea]];
        var left = d.x + 118, cw = Math.max(34, Math.min(62, (d.w - 130) / 4)), top = d.y + 54, rh = Math.min(48, (d.h - 70) / 4);
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("The worlds each set leaves open", d.x + 12, d.y + 6);
        c.font = "11px system-ui, sans-serif"; c.textBaseline = "middle";
        for (i = 0; i < 4; i++) { c.fillStyle = C.muted; c.textAlign = "center"; c.fillText(names[i], left + cw * (i + 0.5), top - 14); }
        for (var j = 0; j < 4; j++) {
          var yy = top + rh * j, any = 0;
          c.fillStyle = C.muted; c.textAlign = "left"; c.fillText(rows[j][0], d.x + 12, yy + rh / 2);
          for (i = 0; i < 4; i++) {
            c.strokeStyle = "#3a475c"; c.lineWidth = 1; c.strokeRect(left + cw * i + 3.5, yy + 4.5, cw - 7, rh - 9);
            if (rows[j][1][i]) { any = 1; c.fillStyle = rows[j][2]; c.globalAlpha = 0.85; c.fillRect(left + cw * i + 4, yy + 5, cw - 8, rh - 10); c.globalAlpha = 1; }
          }
          if (!any) {
            var msg = "no world left: inconsistent", mw = c.measureText(msg).width;
            c.fillStyle = C.panel; c.fillRect(left + cw * 2 - mw / 2 - 5, yy + rh / 2 - 9, mw + 10, 18);
            c.fillStyle = C.loss; c.textAlign = "center"; c.fillText(msg, left + cw * 2, yy + rh / 2);
          }
        }
        c.restore();
      },
      readout: function (v, s) {
        var o = s.out;
        return [["news A", o.name], ["believed now", setName(o.K)], ["after expansion", setName(o.exp) === "none" ? "inconsistent" : setName(o.exp)],
          ["after revision", setName(o.rev)], ["rank of the best A-world", String(o.ent)]];
      },
      note: "Ranks are Spohn's: 0 is believed, higher is more surprising; only their order matters for one revision. When A is consistent with what you believe, revision and expansion agree (the vacuity and inclusion postulates). The rank of the best A-world is how firmly not-A was held.",
    });
  };

  // ---- Part 15: merging of opinions, and a prior that rules the truth out ----------------------------------------
  W.mergingpriors = function (el) {
    QB.widget(el, {
      title: "Opposite priors, the same tosses",
      sub: "Ann thinks heads is rare, Bo thinks it is common; each prior is worth ten imaginary tosses. Cy gives probability zero to every chance above one half. All three watch the same simulated coin and conditionalize. Ann and Bo merge whatever they started with. Move the true chance above one half and Cy stops at one half for good.",
      panels: 2, height: 300,
      controls: [
        { k: "truth", label: "The coin's true chance of heads", min: 0.05, max: 0.95, step: 0.01, value: 0.7, fmt: f2 },
        { k: "ann", label: "Ann's prior expectation", min: 0.05, max: 0.95, step: 0.05, value: 0.1, fmt: f2 },
        { k: "bo", label: "Bo's prior expectation", min: 0.05, max: 0.95, step: 0.05, value: 0.9, fmt: f2 },
        { k: "n", label: "Tosses watched", min: 0, max: 400, step: 1, value: 400 },
      ],
      buttons: [{ label: "New tosses", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var r = QB.rng(s.seed + 1962), N = 400, G = 100, i, k, h = 0;
        var ks = [], pa = [], pb = [], pc = [], lw = new Array(G).fill(0), grid = [];
        for (i = 0; i < G; i++) grid.push(0.5 * (i + 0.5) / G); // Cy's support: chances up to one half
        var cy = function () { var mx = -1e300, a = 0, b = 0, j; for (j = 0; j < G; j++) mx = Math.max(mx, lw[j]); for (j = 0; j < G; j++) { var w = Math.exp(lw[j] - mx); a += w * grid[j]; b += w; } return a / b; };
        var hAt = 0;
        for (k = 0; k <= N; k++) {
          ks.push(k); pa.push((h + 10 * v.ann) / (k + 10)); pb.push((h + 10 * v.bo) / (k + 10)); pc.push(cy());
          if (k === v.n) hAt = h;
          var f = r() < v.truth ? 1 : 0; h += f;
          for (i = 0; i < G; i++) lw[i] += Math.log(f ? grid[i] : 1 - grid[i]);
        }
        var n = v.n;
        s.out = { gap0: Math.abs(pa[0] - pb[0]), gap: Math.abs(pa[n] - pb[n]), cy: pc[n], h: hAt };
        var a = g[0].axes({ x: [0, N], y: [0, 1], title: "Each one's probability that the next toss is heads", xlabel: "tosses watched" });
        a.hline(v.truth, { color: C.ink });
        a.line(ks, pa, { color: C.spot, alpha: 0.3 }); a.line(ks, pb, { color: C.idea, alpha: 0.3 }); a.line(ks, pc, { color: C.loss, alpha: 0.3 });
        a.line(ks.slice(0, n + 1), pa.slice(0, n + 1), { color: C.spot }); a.line(ks.slice(0, n + 1), pb.slice(0, n + 1), { color: C.idea });
        a.line(ks.slice(0, n + 1), pc.slice(0, n + 1), { color: C.loss });
        a.vline(n, { color: C.muted });
        a.legend([["Ann", C.spot], ["Bo", C.idea], ["Cy", C.loss], ["true chance", C.ink]], { pos: v.truth > 0.55 ? "br" : "tr" });
        // posterior densities over the chance, after n tosses, on a grid and normalised numerically
        var xs = QB.linspace(0.005, 0.995, 199), dens = function (al, be, cut) {
          var o = [], mx = -1e300, j, tot = 0;
          for (j = 0; j < xs.length; j++) { var l = (cut && xs[j] > 0.5) ? -1e300 : (al - 1) * Math.log(xs[j]) + (be - 1) * Math.log(1 - xs[j]); o.push(l); mx = Math.max(mx, l); }
          for (j = 0; j < o.length; j++) { o[j] = Math.exp(o[j] - mx); tot += o[j]; }
          for (j = 0; j < o.length; j++) o[j] = o[j] / (tot * (xs[1] - xs[0]));
          return o;
        };
        var da = dens(hAt + 10 * v.ann, n - hAt + 10 * (1 - v.ann)), db = dens(hAt + 10 * v.bo, n - hAt + 10 * (1 - v.bo)), dc = dens(hAt + 1, n - hAt + 1, true);
        var top = 2.2; for (i = 0; i < xs.length; i++) top = Math.max(top, da[i], db[i]); // Cy's spike at one half is clipped
        var b = g[1].axes({ x: [0, 1], y: [0, top * 1.08], title: "What each believes about the chance now", xlabel: "chance of heads", noY: true });
        b.area(xs, da, 0, { color: C.spot, alpha: 0.2 }).line(xs, da, { color: C.spot });
        b.area(xs, db, 0, { color: C.idea, alpha: 0.2 }).line(xs, db, { color: C.idea });
        b.line(xs, dc, { color: C.loss });
        b.vline(v.truth, { color: C.ink });
      },
      readout: function (v, s) {
        var o = s.out;
        return [["heads so far", o.h + " of " + v.n], ["Ann and Bo differ by", f2(o.gap0) + " at the start, " + f2(o.gap) + " now"],
          ["Cy's prediction", f2(o.cy)], ["true chance", f2(v.truth)]];
      },
      note: "Simulated tosses. Ann and Bo have Beta priors with the stated means; Cy's prior is uniform on chances up to one half and zero above (red; its peak is cut off by the frame). Blackwell and Dubins: priors that agree on what is possible merge with probability one; the data cannot revive what a prior has given probability zero (Cromwell's rule).",
    });
  };

  // ---- Part 16: peeking at a p-value against betting on the data -------------------------------------------------
  W.peekbet = function (el) {
    var RUNS = 300, L = 100, STEP = 5; // 300 simulated studies of 500 observations, a possible look every 5
    function noise(s) { // cumulative sums of standard normal noise at every possible look, cached by seed
      if (s.cache && s.cacheSeed === s.seed) return s.cache;
      var r = QB.rng(s.seed + 1939), out = [], i, j, k;
      for (i = 0; i < RUNS; i++) { var row = new Float64Array(L), c = 0; for (j = 0; j < L; j++) { for (k = 0; k < STEP; k++) c += r.normal(); row[j] = c; } out.push(row); }
      s.cache = out; s.cacheSeed = s.seed; return out;
    }
    QB.widget(el, {
      title: "Peek as often as you like: the p-value breaks, the bet does not",
      sub: "Three hundred simulated studies of up to 500 observations each. One analyst stops the first time p < 0.05; another bets on the data and stops when her wealth reaches 20. With no real effect, add looks: the first analyst's false alarms climb far above 5% while the bettor's stay below it. Then add a real effect and compare their power.",
      panels: 2, height: 300,
      controls: [
        { k: "looks", label: "Number of looks at the data", min: 1, max: 100, step: 1, value: 20 },
        { k: "mu", label: "True effect (in standard deviations)", min: 0, max: 0.4, step: 0.02, value: 0, fmt: f2 },
        { k: "alt", label: "Effect the bettor bets on", min: 0.1, max: 0.5, step: 0.02, value: 0.2, fmt: f2 },
      ],
      buttons: [{ label: "New studies", act: function (s) { s.seed++; } }],
      draw: function (g, v, s) {
        var cs = noise(s), i, j, k, ks = [], rp = [], rb = [];
        // first look (on the grid of 100) at which each analyst would stop, for every possible number of looks
        var hitP = new Uint8Array(RUNS * L), hitB = new Uint8Array(RUNS * L), lw = [];
        for (i = 0; i < RUNS; i++) {
          var row = [];
          for (j = 0; j < L; j++) {
            var m = (j + 1) * STEP, S = cs[i][j] + v.mu * m, z = S / Math.sqrt(m), w = v.alt * S - m * v.alt * v.alt / 2;
            hitP[i * L + j] = Math.abs(z) > 1.96 ? 1 : 0; hitB[i * L + j] = w >= Math.log(20) ? 1 : 0; row.push(w / Math.LN10);
          }
          lw.push(row);
        }
        var crossed = [];
        for (k = 1; k <= L; k++) {
          var np = 0, nb = 0;
          for (i = 0; i < RUNS; i++) {
            var a = 0, b = 0;
            for (j = 1; j <= k; j++) { var idx = Math.max(0, Math.round(j * L / k) - 1); if (hitP[i * L + idx]) a = 1; if (hitB[i * L + idx]) b = 1; }
            np += a; nb += b; if (k === v.looks) crossed.push(b);
          }
          ks.push(k); rp.push(np / RUNS); rb.push(nb / RUNS);
        }
        s.out = [rp[v.looks - 1], rb[v.looks - 1], rp[0]];
        var A = g[0].axes({ x: [1, L], y: [0, 1], title: "Studies that ever declare an effect", xlabel: "number of looks", yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        A.hline(0.05, { color: C.muted });
        A.line(ks, rp, { color: C.loss }); A.line(ks, rb, { color: C.gain });
        A.vline(v.looks, { color: C.ink });
        A.legend([["stop at the first p < 0.05", C.loss], ["stop when wealth reaches 20", C.gain], ["5%", C.muted]], { pos: "tr" });
        var B = g[1].axes({ x: [0, L * STEP], y: [-3, 3], title: "The bettor's wealth in 40 of the studies", xlabel: "observations", yticks: [-3, -2, -1, 0, 1, 2, 3], yfmt: function (y) { return y === 0 ? "1" : y > 0 ? String(Math.pow(10, y)) : "1/" + Math.pow(10, -y); } });
        var xs = []; for (j = 0; j < L; j++) xs.push((j + 1) * STEP);
        for (i = 0; i < 40; i++) B.line(xs, lw[i], { color: crossed[i] ? C.gain : C.spot, width: 1, alpha: crossed[i] ? 0.8 : 0.35 });
        B.hline(Math.log(20) / Math.LN10, { color: C.idea });
        B.text(L * STEP, Math.log(20) / Math.LN10, "wealth 20", { color: C.idea, align: "right", dx: -6, dy: -9, bg: true });
      },
      readout: function (v, s) {
        return [[v.mu > 0 ? "detects the effect: p-peeker" : "false alarms: p-peeker", QB.pct(s.out[0], 0)], ["bettor", QB.pct(s.out[1], 0)],
          ["p-value with one look only", QB.pct(s.out[2], 0)]];
      },
      note: "Simulated data: normal observations with standard deviation 1. The bettor's wealth is the likelihood ratio of her chosen effect against no effect, a test martingale when there is no effect, so by Ville's inequality it ever reaches 20 in at most 5% of studies, however many looks. Green paths reached 20 at one of the looks taken.",
    });
  };

  // ---- Part 17: seeing against doing in a confounded model --------------------------------------------------------
  W.seeingdoing = function (el) {
    function arrow(c, x1, y1, x2, y2, w, color, dash) {
      var a = Math.atan2(y2 - y1, x2 - x1), h = 9 + w;
      c.save(); c.strokeStyle = color; c.fillStyle = color; c.lineWidth = w; if (dash) c.setLineDash(dash);
      c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2 - h * Math.cos(a), y2 - h * Math.sin(a)); c.stroke(); c.setLineDash([]);
      c.beginPath(); c.moveTo(x2, y2); c.lineTo(x2 - h * Math.cos(a - 0.4), y2 - h * Math.sin(a - 0.4)); c.lineTo(x2 - h * Math.cos(a + 0.4), y2 - h * Math.sin(a + 0.4)); c.closePath(); c.fill();
      c.restore();
    }
    QB.widget(el, {
      title: "Seeing is not doing: a drug, recovery, and age behind both",
      sub: "Age affects who takes the drug and who recovers. The bars compare recovery with and without the drug: within each age group, among everyone as observed, and among everyone if the drug were assigned (do). Strengthen the two arrows out of age and the observed comparison drifts from the truth, even to the opposite sign. Set either arrow to zero and seeing equals doing.",
      panels: 2, height: 310, weights: [0.8, 1.2],
      controls: [
        { k: "e", label: "The drug's true effect on recovery", min: -0.2, max: 0.3, step: 0.01, value: 0.2, fmt: function (x) { return fmt(x, 2); } },
        { k: "c", label: "Age → drug: extra uptake among the old", min: -0.45, max: 0.45, step: 0.01, value: 0.35, fmt: function (x) { return fmt(2 * x, 2); } },
        { k: "a", label: "Age → recovery: effect of being old", min: -0.4, max: 0, step: 0.01, value: -0.35, fmt: function (x) { return fmt(x, 2); } },
      ],
      draw: function (g, v, s) {
        var base = 0.6, pd = [0.5 - v.c, 0.5 + v.c]; // P(drug | young), P(drug | old); half are old
        var pr = function (d, a) { return base + v.e * d + v.a * a; };
        var seen1 = (pr(1, 0) * pd[0] + pr(1, 1) * pd[1]) / (pd[0] + pd[1]);
        var seen0 = (pr(0, 0) * (1 - pd[0]) + pr(0, 1) * (1 - pd[1])) / (2 - pd[0] - pd[1]);
        var do1 = 0.5 * pr(1, 0) + 0.5 * pr(1, 1), do0 = 0.5 * pr(0, 0) + 0.5 * pr(0, 1);
        s.out = { naive: seen1 - seen0, truth: do1 - do0 };
        // left: the graph
        var b = g[0].box, c = g.ctx, top = { x: b.x + b.w / 2, y: b.y + 70 }, L = { x: b.x + Math.max(48, b.w * 0.2), y: b.y + b.h - 78 }, R = { x: b.x + b.w - Math.max(56, b.w * 0.2), y: b.y + b.h - 78 };
        var col = function (x) { return Math.abs(x) < 0.005 ? "#3a475c" : x > 0 ? C.gain : C.loss; }, wd = function (x, k) { return 1.2 + 5 * Math.min(1, Math.abs(x) / k); };
        c.save();
        c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("The causal graph", b.x + 12, b.y + 6);
        arrow(c, top.x - 14, top.y + 18, L.x + 10, L.y - 20, wd(v.c, 0.45), col(v.c), [5, 4]);
        arrow(c, top.x + 14, top.y + 18, R.x - 10, R.y - 20, wd(v.a, 0.4), col(v.a));
        arrow(c, L.x + 30, L.y, R.x - 44, R.y, wd(v.e, 0.3), col(v.e));
        c.font = "600 12px system-ui, sans-serif"; c.textAlign = "center"; c.textBaseline = "middle";
        [[top, "age"], [L, "drug"], [R, "recovery"]].forEach(function (n) {
          var tw = c.measureText(n[1]).width + 18;
          c.fillStyle = C.bg; c.strokeStyle = C.ink; c.lineWidth = 1.2; c.fillRect(n[0].x - tw / 2, n[0].y - 14, tw, 28); c.strokeRect(n[0].x - tw / 2, n[0].y - 14, tw, 28);
          c.fillStyle = C.ink; c.fillText(n[1], n[0].x, n[0].y);
        });
        c.font = "11px system-ui, sans-serif"; c.fillStyle = C.muted;
        c.fillText("do(drug) cuts the dashed arrow", b.x + b.w / 2, b.y + b.h - 34);
        c.fillText("green raises, red lowers", b.x + b.w / 2, b.y + b.h - 17);
        c.restore();
        // right: recovery rates
        var A = g[1].axes({ x: [0, 12], y: [0, 1], title: "Recovery rate without and with the drug", xticks: [1.5, 4.5, 7.5, 10.5],
          xfmt: function (x) { return x < 2 ? "young" : x < 5 ? "old" : x < 8 ? "as seen" : "do(drug)"; }, yfmt: function (y) { return Math.round(100 * y) + "%"; } });
        A.bars([1, 4, 7, 10], [pr(0, 0), pr(0, 1), seen0, do0], 0.9, { color: C.cash });
        A.bars([2, 5, 8, 11], [pr(1, 0), pr(1, 1), seen1, do1], 0.9, { color: C.idea });
        A.vline(6, { color: C.line, dash: [2, 3] });
        A.legend([["no drug", C.cash], ["drug", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        var o = s.out, rev = o.naive * o.truth < 0 && Math.abs(o.naive) > 0.005 && Math.abs(o.truth) > 0.005;
        return [["seen: drug minus no drug", fmt(o.naive, 3)], ["adjusted for age = do(drug)", fmt(o.truth, 3)], ["confounding bias", fmt(o.naive - o.truth, 3)],
          ["sign reversed (Simpson)", rev ? "yes" : "no"]];
      },
      note: "Exact probabilities from a structural model, no sampling: half the population is old; uptake is 50% plus or minus half the stated gap; recovery is 60% plus the drug's effect plus age's effect. The back-door formula averages the within-age comparisons with the population's age weights, which is what an intervention would produce.",
    });
  };

  // ---- Part 18: an Ising lattice, coarse-grained by block spins while it runs -------------------------------------
  W.blockspins = function (el) {
    var L = 81, TC = 2 / Math.log(1 + Math.SQRT2);
    function reset(s, ordered) {
      var r = QB.rng(s.seed + 1966); s.rnd = r; s.spin = new Int8Array(L * L);
      for (var i = 0; i < L * L; i++) s.spin[i] = ordered || r() < 0.5 ? 1 : -1;
    }
    function sweep(s, T, n) { // heat-bath updates at random sites: n sweeps of the lattice
      var p = [], h, sp = s.spin, r = s.rnd;
      for (h = -4; h <= 4; h += 2) p.push(1 / (1 + Math.exp(-2 * h / T)));
      for (var k = 0; k < n * L * L; k++) {
        var i = Math.floor(r() * L), j = Math.floor(r() * L);
        h = sp[((i + 1) % L) * L + j] + sp[((i + L - 1) % L) * L + j] + sp[i * L + (j + 1) % L] + sp[i * L + (j + L - 1) % L];
        sp[i * L + j] = r() < p[(h + 4) / 2] ? 1 : -1;
      }
    }
    function block(a, n) { // majority of each 3 x 3 block of an n x n lattice
      var m = n / 3, o = new Int8Array(m * m);
      for (var i = 0; i < m; i++) for (var j = 0; j < m; j++) {
        var t = 0; for (var x = 0; x < 3; x++) for (var y = 0; y < 3; y++) t += a[(3 * i + x) * n + 3 * j + y];
        o[i * m + j] = t > 0 ? 1 : -1;
      }
      return o;
    }
    function corr(a, n) { var t = 0; for (var i = 0; i < n; i++) for (var j = 0; j < n; j++) t += a[i * n + j] * (a[((i + 1) % n) * n + j] + a[i * n + (j + 1) % n]); return t / (2 * n * n); }
    function paint(c, a, n, x0, y0, cell) {
      c.fillStyle = "#1d2b4a"; c.fillRect(x0, y0, n * cell, n * cell);
      c.fillStyle = C.idea; c.beginPath();
      for (var i = 0; i < n; i++) for (var j = 0; j < n; j++) if (a[i * n + j] > 0) c.rect(x0 + j * cell, y0 + i * cell, cell, cell);
      c.fill();
    }
    QB.widget(el, {
      title: "Block spins: watch detail wash out",
      sub: "A running Ising lattice of 81 by 81 spins (gold up, blue down), and the same lattice with each 3 by 3 block replaced by its majority, once and twice. Below the critical temperature the blocked pictures are more ordered than the original; above it they are more random; at 2.27 they look like the original at every scale. Slide the temperature across.",
      panels: 2, height: 300,
      controls: [
        { k: "T", label: "Temperature", min: 1.5, max: 3.5, step: 0.01, value: 2.27, fmt: f2 },
        { k: "speed", label: "Sweeps per frame", min: 1, max: 12, step: 1, value: 6 },
      ],
      buttons: [{ label: "Start from order", act: function (s) { s.seed++; reset(s, true); } }, { label: "Start from disorder", act: function (s) { s.seed++; reset(s, false); } }],
      init: function (s) { reset(s, false); sweep(s, 2.27, 60); },
      animate: function (v, s) { sweep(s, v.T, v.speed); return true; },
      draw: function (g, v, s) {
        var c = g.ctx, b1 = block(s.spin, L), b2 = block(b1, 27), m = 0, i;
        for (i = 0; i < L * L; i++) m += s.spin[i];
        s.out = { c: [corr(s.spin, L), corr(b1, 27), corr(b2, 9)], m: Math.abs(m) / (L * L), exact: v.T < TC ? Math.pow(1 - Math.pow(Math.sinh(2 / v.T), -4), 0.125) : 0 };
        var a = g[0].box, cell = Math.max(1, Math.floor(Math.min(a.w - 24, a.h - 40) / L)), side = cell * L;
        c.save(); c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top";
        c.fillText("The lattice: 81 × 81", a.x + (a.w - side) / 2, a.y + 8);
        paint(c, s.spin, L, a.x + (a.w - side) / 2, a.y + 30, cell);
        var d = g[1].box, half = (d.w - 36) / 2, c1 = Math.max(1, Math.floor(Math.min(half, d.h - 40) / 27)), s1 = c1 * 27, c2 = c1 * 3;
        var gap = (d.w - 2 * s1) / 3;
        c.fillStyle = C.ink; c.fillText("Blocked once: 27 × 27", d.x + gap, d.y + 8);
        paint(c, b1, 27, d.x + gap, d.y + 30, c1);
        c.fillStyle = C.ink; c.fillText("Twice: 9 × 9", d.x + 2 * gap + s1, d.y + 8);
        paint(c, b2, 9, d.x + 2 * gap + s1, d.y + 30, c2);
        c.restore();
      },
      readout: function (v, s) {
        var o = s.out;
        return [["neighbour correlation at 81, 27, 9", f2(o.c[0]) + ", " + f2(o.c[1]) + ", " + f2(o.c[2])], ["|m| now", f2(o.m)],
          ["Onsager's exact |m|", f2(o.exact)], ["critical temperature", "2.269"]];
      },
      note: "Simulated: heat-bath dynamics with periodic edges, J = 1. Near the critical temperature, and after a start from disorder below it, a lattice this size takes many sweeps to settle, so |m| lags Onsager's infinite-lattice value. The blocking rule is Kadanoff's majority vote.",
    });
  };
})();
