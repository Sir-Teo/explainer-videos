// Interactives for Acts IV to VI (Parts 23-37).  As before, each can be heard: the sound is computed in the page and
// played through the browser's Web Audio after a click.  Nothing is downloaded.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;
  var audio = null;

  function play(samples, rate) {
    try {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return false;
      if (!audio) audio = new AC();
      if (audio.state === "suspended" && audio.resume) audio.resume();
      var buf = audio.createBuffer(1, samples.length, rate);
      buf.getChannelData(0).set(samples);
      var src = audio.createBufferSource();
      src.buffer = buf; src.connect(audio.destination); src.start();
      return true;
    } catch (e) { return false; }
  }
  function hz(m) { return 440 * Math.pow(2, (m - 69) / 12); }
  // a soft sung-like tone: a few harmonics with a formant-ish tilt, a slow attack and release
  function notesSound(notes, unit) {
    var rate = 44100, end = 0, i, k;
    notes.forEach(function (n) { end = Math.max(end, n[1] + n[2]); });
    var out = new Float32Array(Math.floor((end * unit + 0.8) * rate));
    notes.forEach(function (n) {
      var f = hz(n[0]), s0 = Math.floor(n[1] * unit * rate), len = Math.floor(n[2] * unit * rate), amps = [1, 0.6, 0.45, 0.3, 0.18, 0.1];
      for (i = 0; i < len && s0 + i < out.length; i++) {
        var t = i / rate, env = Math.min(1, t / 0.04) * Math.min(1, (len - i) / rate / 0.06), v = 0;
        for (k = 0; k < amps.length; k++) v += amps[k] * Math.sin(2 * Math.PI * f * (k + 1) * t * (1 + 0.003 * Math.sin(2 * Math.PI * 5.2 * t)));
        out[s0 + i] += 0.12 * env * v;
      }
    });
    return out;
  }

  // ---- Part 23: an isorhythm engine -----------------------------------------------------------------------------
  var COLORS23 = [
    ["7 pitches", [53, 55, 57, 58, 57, 55, 53]],
    ["9 pitches", [53, 55, 57, 55, 53, 52, 50, 52, 53]],
    ["12 pitches", [50, 53, 55, 57, 55, 53, 52, 50, 48, 50, 52, 50]],
    ["the Tune, 7", [53, 53, 60, 60, 62, 62, 60]],
    ["28 pitches", [53, 55, 57, 55, 53, 52, 50, 52, 53, 55, 57, 58, 57, 55, 53, 55, 57, 60, 58, 57, 55, 53, 52, 50, 52, 53, 52, 50]],
  ];
  var TALEAE23 = [
    ["L L L rest (the fifth mode's ordo)", [3, 3, 3, -3]],
    ["5 notes, 2 rests", [3, 3, 2, 1, -3, 3, -3]],
    ["4 notes, 1 rest", [3, 2, 1, 3, -3]],
    ["8 notes", [2, 1, 2, 1, 3, 3, 2, 1, -3]],
    ["6 notes", [3, 1, 2, 3, -1, 2, 1]],
  ];
  function gcd(a, b) { while (b) { var t = b; b = a % b; a = t; } return a; }
  function iso23(color, talea, dim, statements) {
    var nt = talea.filter(function (d) { return d > 0; }).length, L = color.length * nt / gcd(color.length, nt);
    var total = statements ? statements * color.length : L, out = [], t = 0, k = 0, i = 0;
    while (k < total) {
      var d = talea[i % talea.length] * dim;
      if (d > 0) { out.push([color[k % color.length], t, d, k]); k++; }
      t += Math.abs(d); i++;
    }
    return { notes: out, L: L, colors: L / color.length, taleae: L / nt, nt: nt };
  }
  W.isorhythm = function (el) {
    QB.widget(el, {
      title: "Color against talea",
      sub: "An isorhythmic tenor lays a color (a list of pitches) through a talea (a rhythm of notes and rests) until both run out together. Choose a color and a talea. Left: the tenor, each statement of the color in its own colour, a grey line at the start of every talea. Right: every note as a point (its place in the talea, its place in the color); the two cycles realign only when every reachable pair has been visited, after lcm(color, talea notes) notes.",
      panels: 2, height: 300,
      controls: [
        { k: "c", label: "Color", min: 0, max: COLORS23.length - 1, step: 1, value: 0, fmt: function (i) { return COLORS23[i][0]; } },
        { k: "t", label: "Talea", min: 0, max: TALEAE23.length - 1, step: 1, value: 1, fmt: function (i) { return TALEAE23[i][0]; } },
        { k: "d", label: "Diminution (the talea at 1/d speed)", min: 1, max: 3, step: 1, value: 1, fmt: function (i) { return i === 1 ? "none" : "1/" + i; } },
      ],
      buttons: [{ label: "Play the tenor", act: function (s) { s.sound = play(notesSound(s.notes, 0.18), 44100); } }],
      init: function (s) { s.sound = null; s.notes = []; },
      draw: function (g, v, s) {
        var color = COLORS23[v.c][1], talea = TALEAE23[v.t][1], R = iso23(color, talea, 1 / v.d), n = R.notes, i;
        s.notes = n; s.R = R; s.color = color; s.talea = talea;
        var end = 0, lo = 99, hi = 0;
        n.forEach(function (x) { end = Math.max(end, x[1] + x[2]); lo = Math.min(lo, x[0]); hi = Math.max(hi, x[0]); });
        var a = g[0].axes({ x: [0, end], y: [lo - 1, hi + 1], title: "The tenor (" + n.length + " notes)", xlabel: "time (breves)", ylabel: "key number" });
        var cols = [C.idea, "#7DD3FC", "#F472B6", "#A3E635", "#FDBA74", "#C4B5FD", "#94A3B8", "#FCA5A5", "#86EFAC"];
        var span = talea.reduce(function (p, q) { return p + Math.abs(q); }, 0) / v.d;
        for (var tt = 0; tt <= end + 1e-9; tt += span) a.vline(tt, { color: "#555" });
        n.forEach(function (x) { var st = Math.floor(x[3] / color.length); a.line([x[1], x[1] + x[2] * 0.95], [x[0], x[0]], { color: cols[st % cols.length], width: 5 }); });
        var b = g[1].axes({ x: [-0.5, R.nt - 0.5], y: [-0.5, color.length - 0.5], title: "Pairs visited: (talea note, color pitch)", xlabel: "place in the talea", ylabel: "place in the color" });
        var xs = [], ys = [];
        for (i = 0; i < n.length; i++) { xs.push(i % R.nt); ys.push(i % color.length); }
        b.dots(xs, ys, { color: C.idea, r: Math.max(2, Math.min(6, 120 / Math.max(R.nt, color.length))) });
      },
      readout: function (v, s) {
        var R = s.R, g_ = gcd(s.color.length, R.nt);
        return [["color", s.color.length + " pitches"], ["talea", R.nt + " notes, " + s.talea.filter(function (d) { return d < 0; }).length + " rests"],
                ["they meet again after", R.L + " notes: " + R.colors + " colors, " + R.taleae + " taleae"],
                ["pairs visited", R.L + " of " + (s.color.length * R.nt) + (g_ > 1 ? " (they share a factor " + g_ + ")" : " (no common factor: every pair)")],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "With 7 pitches and 5 notes the two cycles share no factor, so every (talea note, pitch) pair occurs once before they realign after 35 notes: the Chinese remainder theorem, sung. Give them a common factor (12 pitches against 6 notes) and they realign much sooner, visiting only some pairs. Machaut and de Vitry often chose a color that holds a whole number of taleae, so that the two lined up at every statement; diminution replays the same talea faster, as the later sections of many motets do."
    });
  };
  // ---- Part 24: how is this dissonance treated? -------------------------------------------------------------------
  var WHITE24 = [0, 2, 4, 5, 7, 9, 11], NM24 = ["C", "D", "E", "F", "G", "A", "B"];
  function wk24(i) { return 12 * Math.floor(i / 7) + WHITE24[((i % 7) + 7) % 7] + 48; }       // white-key index -> key number
  function wname24(i) { return NM24[((i % 7) + 7) % 7] + (Math.floor(i / 7) + 3); }
  var CONS24 = { 0: 1, 3: 1, 4: 1, 7: 1, 8: 1, 9: 1 };
  var PAL24 = { passing: 55.2, suspension: 30.9, neighbour: 10.1, cambiata: 1.0, anticipation: 0.3, free: 2.6 };
  function classify24(up, tie, b1, b2) {
    // up: four key numbers on beats 0..3; tie: the note of beat 1 held into beat 2 (same pitch); bass b1 on 0-1, b2 on 2-3
    var notes = [], out = [], k;
    for (k = 0; k < 4; k++) {
      if (k === 2 && tie && up[2] === up[1]) { notes[notes.length - 1].end = 3; continue; }
      notes.push({ p: up[k], start: k, end: k + 1 });
    }
    function bassAt(t) { return t < 2 ? b1 : b2; }
    function step(a, b) { var d = Math.abs(a - b); return d >= 1 && d <= 2; }
    for (k = 0; k < notes.length; k++) {
      var n = notes[k], pr = notes[k - 1], nx = notes[k + 1];
      var times = [n.start];
      if (n.start < 2 && n.end > 2 && b2 !== b1) times.push(2);          // the bass moves under a held note
      times.forEach(function (t) {
        var ic = ((n.p - bassAt(t)) % 12 + 12) % 12;
        if (CONS24[ic]) { out.push({ k: k, t: t, kind: "consonant" }); return; }
        var kind = "free";
        if (t > n.start) {
          var prepared = CONS24[((n.p - bassAt(n.start)) % 12 + 12) % 12];
          kind = (prepared && nx && n.p - nx.p >= 1 && n.p - nx.p <= 2) ? "suspension" : "free";
        } else if (pr && nx && step(n.p, pr.p) && step(nx.p, n.p)) {
          kind = (Math.sign(n.p - pr.p) === Math.sign(nx.p - n.p)) ? "passing" : "neighbour";
        } else if (pr && nx && pr.p - n.p >= 1 && pr.p - n.p <= 2 && n.p - nx.p >= 3 && n.p - nx.p <= 4) {
          kind = "cambiata";
        }
        out.push({ k: k, t: t, kind: kind });
      });
    }
    return { notes: notes, marks: out };
  }
  var KC24 = { consonant: "#8A93A0", passing: C.idea, suspension: "#F472B6", neighbour: "#7DD3FC", cambiata: "#A3E635", anticipation: "#94A3B8", free: C.loss };
  W.treatment = function (el) {
    var ctl = [];
    for (var q = 1; q <= 4; q++) ctl.push({ k: "u" + q, label: "Upper voice, beat " + q, min: 7, max: 18, step: 1, value: [14, 14, 14, 13][q - 1], fmt: wname24 });
    ctl.push({ k: "tie", label: "Hold beat 2 into beat 3 (if the same note)", min: 0, max: 1, step: 1, value: 1, fmt: function (i) { return i ? "held" : "struck again"; } });
    ctl.push({ k: "b1", label: "Bass, beats 1-2", min: 0, max: 11, step: 1, value: 5, fmt: wname24 });
    ctl.push({ k: "b2", label: "Bass, beats 3-4", min: 0, max: 11, step: 1, value: 8, fmt: wname24 });
    QB.widget(el, {
      title: "How is this dissonance treated?",
      sub: "Two voices over four beats. Set the upper voice's four notes and the two bass notes; hold the second note into the third to make a suspension. Each moment where the upper voice clashes with the bass (a second, fourth, tritone or seventh) is classified by Jeppesen's rules, as the film's program does on Palestrina's 102,279 dissonances: passing, neighbour, suspension, cambiata, or free. Right: how Palestrina's dissonances divide.",
      panels: 2, height: 290,
      controls: ctl,
      buttons: [{ label: "Play", act: function (s) { s.sound = play(notesSound(s.play, 0.42), 44100); } }],
      init: function (s) { s.sound = null; s.play = []; },
      draw: function (g, v, s) {
        var up = [wk24(v.u1), wk24(v.u2), wk24(v.u3), wk24(v.u4)], b1 = wk24(v.b1), b2 = wk24(v.b2);
        var R = classify24(up, v.tie, b1, b2);
        s.R = R;
        s.play = R.notes.map(function (n) { return [n.p, n.start, n.end - n.start]; }).concat([[b1, 0, 2], [b2, 2, 2]]);
        var lo = Math.min(b1, b2, Math.min.apply(null, up)) - 2, hi = Math.max(b1, b2, Math.max.apply(null, up)) + 3;
        var a = g[0].axes({ x: [0, 4], y: [lo, hi], title: "The two voices", xlabel: "beat", ylabel: "key number", xticks: [0, 1, 2, 3, 4] });
        a.line([0, 2], [b1, b1], { color: "#8A93A0", width: 7 });
        a.line([2, 4], [b2, b2], { color: "#8A93A0", width: 7 });
        R.notes.forEach(function (n) { a.line([n.start + 0.04, n.end - 0.04], [n.p, n.p], { color: C.ink, width: 7 }); });
        R.marks.forEach(function (m) {
          if (m.kind === "consonant") return;
          var n = R.notes[m.k];
          a.dots([m.t + 0.12], [n.p + 1.2], { color: KC24[m.kind], r: 6 });
          a.text(m.t + 0.12, n.p + 2.0, m.kind, { align: "left", size: 11, color: KC24[m.kind] });
        });
        var ks = ["passing", "suspension", "neighbour", "cambiata", "free"];
        var b = g[1].axes({ x: [-0.6, 4.6], y: [0, 60], title: "Palestrina's dissonances, in 100", xticks: [], ylabel: "share" });
        b.bars([0, 1, 2, 3, 4], ks.map(function (k) { return PAL24[k]; }), 0.6, { color: function (i) { return KC24[ks[i]]; } });
        ks.forEach(function (k, i) { b.text(i, 0, k, { align: "center", base: "top", dy: 7, size: 10, color: C.muted }); });
      },
      readout: function (v, s) {
        var ds = s.R.marks.filter(function (m) { return m.kind !== "consonant"; });
        return [["dissonances", ds.length ? ds.map(function (m) { return "beat " + (m.t + 1) + ": " + m.kind; }).join("; ") : "none: every beat consonant"],
                ["in Palestrina", ds.length ? ds.map(function (m) { return m.kind + " " + PAL24[m.kind] + " in 100"; }).join("; ") : "-"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "The opening setting is a 7-6 suspension: C over A is a third, the bass moves to D under the held C (a seventh), and C falls to B. Strike the C again instead of holding it and the same seventh becomes free, as in Monteverdi's madrigals. Try C B A over a held A for a passing note, C D C for a neighbour, and C B G A over A then G for a cambiata."
    });
  };
  // ---- Part 25: a figured-bass realizer ---------------------------------------------------------------------------
  var FIGS25 = [["", [3, 5]], ["6", [3, 6]], ["6/4", [4, 6]], ["7", [3, 5, 7]], ["6/5", [3, 5, 6]], ["4/3", [3, 4, 6]], ["4/2", [2, 4, 6]]];
  var CMAJ25 = [0, 2, 4, 5, 7, 9, 11];
  function wkey25(i) { return 12 * Math.floor(i / 7) + CMAJ25[((i % 7) + 7) % 7] + 36; }   // white-key index from C2
  function above25(bi, step) { return wkey25(bi + step - 1) % 12; }
  function options25(bi, fig) {
    var need = FIGS25[fig][1].map(function (st) { return above25(bi, st); }), bass = wkey25(bi), out = [];
    var allowed = need.concat([bass % 12]);
    var keys = [];
    for (var m = Math.max(55, bass + 1); m <= 79; m++) if (allowed.indexOf(m % 12) >= 0) keys.push(m);
    for (var a = 0; a < keys.length; a++) for (var b = a + 1; b < keys.length; b++) for (var c = b + 1; c < keys.length; c++) {
      var ch = [keys[a], keys[b], keys[c]];
      if (ch[2] - ch[0] > 12) continue;
      var pcs = ch.map(function (x) { return x % 12; });
      if (need.every(function (n) { return pcs.indexOf(n) >= 0; })) out.push(ch);
    }
    return out;
  }
  function cost25(a, b, ba, bb) {
    var c = 0, i, j, va = [ba].concat(a), vb = [bb].concat(b);
    for (i = 0; i < 3; i++) c += Math.abs(a[i] - b[i]);
    for (i = 0; i < 4; i++) for (j = i + 1; j < 4; j++) {
      var ia = ((va[j] - va[i]) % 12 + 12) % 12, ib = ((vb[j] - vb[i]) % 12 + 12) % 12;
      if (ia === ib && (ia === 0 || ia === 7) && va[i] !== vb[i]) c += 50;
    }
    return c;
  }
  function realize25(bis, figs, top) {
    var opts = bis.map(function (b, k) { return options25(b, figs[k]); });
    if (opts.some(function (o) { return !o.length; })) return null;
    var best = [opts[0].map(function (o) { return 4 * Math.abs(o[2] - top); })], back = [];
    for (var k = 1; k < opts.length; k++) {
      var row = [], bk = [];
      opts[k].forEach(function (b) {
        var m = 1e18, arg = 0;
        opts[k - 1].forEach(function (a, i) { var c = best[k - 1][i] + cost25(a, b, wkey25(bis[k - 1]), wkey25(bis[k])); if (c < m) { m = c; arg = i; } });
        row.push(m); bk.push(arg);
      });
      best.push(row); back.push(bk);
    }
    var last = best[best.length - 1], j = last.indexOf(Math.min.apply(null, last)), path = [j];
    for (k = back.length - 1; k >= 0; k--) { j = back[k][j]; path.unshift(j); }
    return { chords: path.map(function (j2, k2) { return opts[k2][j2]; }), cost: Math.min.apply(null, last), counts: opts.map(function (o) { return o.length; }) };
  }
  W.figuredbass = function (el) {
    var ctl = [];
    var defB = [7, 10, 12, 11, 7], defF = [0, 1, 0, 3, 0];
    for (var q = 0; q < 5; q++) {
      ctl.push({ k: "b" + q, label: "Bass " + (q + 1), min: 3, max: 13, step: 1, value: defB[q], fmt: function (i) { return ["C", "D", "E", "F", "G", "A", "B"][((i % 7) + 7) % 7] + (Math.floor(i / 7) + 2); } });
      ctl.push({ k: "f" + q, label: "Figure " + (q + 1), min: 0, max: FIGS25.length - 1, step: 1, value: defF[q], fmt: function (i) { return FIGS25[i][0] || "5/3"; } });
    }
    ctl.push({ k: "top", label: "Start the top voice near", min: 67, max: 79, step: 1, value: 72, fmt: function (m) { return ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"][m % 12] + (Math.floor(m / 12) - 1); } });
    QB.widget(el, {
      title: "Realize a figured bass",
      sub: "Five bass notes in C major and a figure under each (5/3 means a plain triad; 6, a third and a sixth; 7, add the seventh...). The page finds every three-voice chord the figure allows above each bass note, then the path through them whose upper voices move least, with no parallel fifths or octaves, as the film's realizer did for Corelli's bass. Move the starting top note to get another, equally correct, realization.",
      panels: 2, height: 280,
      controls: ctl,
      buttons: [{ label: "Play", act: function (s) { s.sound = s.notes.length ? play(notesSound(s.notes, 0.6), 44100) : false; } }],
      init: function (s) { s.sound = null; s.notes = []; },
      draw: function (g, v, s) {
        var bis = [], figs = [], q;
        for (q = 0; q < 5; q++) { bis.push(v["b" + q]); figs.push(v["f" + q]); }
        var R = realize25(bis, figs, v.top);
        s.R = R; s.notes = [];
        var a = g[0].axes({ x: [0, 5], y: [34, 82], title: R ? "The realization" : "No chord fits a figure in this range", xlabel: "chord", ylabel: "key number", xticks: [0, 1, 2, 3, 4, 5] });
        bis.forEach(function (b, k) {
          a.line([k + 0.05, k + 0.95], [wkey25(b), wkey25(b)], { color: "#8A93A0", width: 6 });
          a.text(k + 0.5, wkey25(b) - 3.2, FIGS25[figs[k]][0] || "5/3", { align: "center", size: 11, color: C.muted });
          s.notes.push([wkey25(b), k, 1]);
        });
        if (R) R.chords.forEach(function (ch, k) { ch.forEach(function (m, i) { a.line([k + 0.05, k + 0.95], [m, m], { color: i === 2 ? C.idea : "#7DD3FC", width: 6 }); s.notes.push([m, k, 1]); }); });
        var b2 = g[1].axes({ x: [-0.5, 4.5], y: [0, 40], title: "Chords the figure allows, per bass note", xticks: [], ylabel: "count" });
        if (R) {
          b2.bars([0, 1, 2, 3, 4], R.counts, 0.6, { color: C.idea });
          R.counts.forEach(function (c, i) { b2.text(i, c, String(c), { align: "center", base: "bottom", dy: -4, size: 10, color: C.muted }); });
        }
      },
      readout: function (v, s) {
        var R = s.R, total = R ? R.counts.reduce(function (p, c) { return p * c; }, 1) : 0;
        return [["realizations possible", R ? total.toLocaleString() : "none"], ["chosen path's motion (semitones, upper voices)", R ? String(R.cost) : "-"],
                ["top voice", R ? R.chords.map(function (ch) { return ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"][ch[2] % 12]; }).join(" ") : "-"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Even five chords allow thousands of correct realizations; the smoothest path is only one of them, and a continuo player would choose by the music above, which the bass alone does not know. That is why the film's realization of Corelli's bass held most of his notes but almost none of his melody."
    });
  };

  // ---- Part 26: a Classical phrase: chords, an accompaniment figure, and the cadence it ends on --------------------
  var CH26 = [["I", [0, 4, 7]], ["ii", [2, 5, 9]], ["IV", [5, 9, 0]], ["V", [7, 11, 2]], ["V7", [7, 11, 2, 5]], ["vi", [9, 0, 4]]];
  var FIG26 = ["block chords", "Alberti bass", "repeated chords", "broken octaves"];
  var TUNE26 = [[72, 0, 1], [72, 1, 1], [79, 2, 1], [79, 3, 1], [81, 4, 1], [81, 5, 1], [79, 6, 2], [77, 8, 1], [77, 9, 1], [76, 10, 1], [76, 11, 1]];
  function voice26(pcs, lo) {   // the chord's tones placed from ``lo`` upward, root lowest
    var out = [], base = lo + ((pcs[0] - lo) % 12 + 12) % 12;
    pcs.forEach(function (pc, i) { var m = base + ((pc - pcs[0]) % 12 + 12) % 12; out.push(m); });
    return out.sort(function (a, b) { return a - b; });
  }
  function cadence26(a, b) {
    var x = CH26[a][0], y = CH26[b][0];
    if ((x === "V" || x === "V7") && y === "I") return ["authentic cadence", "an answer: the phrase is finished"];
    if (y === "V" || y === "V7") return ["half cadence", "a question: it asks for another phrase"];
    if ((x === "V" || x === "V7") && y === "vi") return ["deceptive cadence", "the expected I swerves to vi: go on"];
    if (x === "IV" && y === "I") return ["plagal cadence", "the 'amen': a softer close"];
    return ["no cadence", "the phrase stops without a formula"];
  }
  W.galantphrase = function (el) {
    var defs = [0, 2, 0, 3, 4, 0, 4, 3];
    var ctl = [];
    for (var q = 0; q < 8; q++) ctl.push({ k: "c" + q, label: "Bar " + (Math.floor(q / 2) + 1) + ", half " + (q % 2 + 1), min: 0, max: CH26.length - 1, step: 1, value: defs[q], fmt: function (i) { return CH26[i][0]; } });
    ctl.push({ k: "fig", label: "Accompaniment", min: 0, max: FIG26.length - 1, step: 1, value: 1, fmt: function (i) { return FIG26[i]; } });
    QB.widget(el, {
      title: "Build a four-bar Classical phrase",
      sub: "The Tune's opening over eight half-bar chords that you choose, with an accompaniment figure. The page names the cadence the last two chords make (V to I authentic, ending on V a half cadence, V to vi deceptive, IV to I plagal) and counts the harmonic rhythm: how often the chord changes. The film's quartets change their sounding pitch classes on about 85 beats in 100; the galant harmony underneath changes far more slowly.",
      panels: 2, height: 290,
      controls: ctl,
      buttons: [{ label: "Play", act: function (s) { s.sound = play(notesSound(s.notes, 0.36), 44100); } }],
      init: function (s) { s.sound = null; s.notes = []; },
      draw: function (g, v, s) {
        var cs = [], q, notes = TUNE26.map(function (n) { return n.slice(); });
        for (q = 0; q < 8; q++) cs.push(v["c" + q]);
        var last = cs[7], prev = cs[6];
        notes.push([CH26[last][0] === "I" ? 72 : (CH26[last][0] === "vi" ? 72 : 74), 12, 4]);
        var acc = [];
        cs.forEach(function (c, h) {
          var t0 = 2 * h, pcs = CH26[c][1], ch = voice26(pcs, 48), bass = ch[0];
          if (v.fig === 0) ch.forEach(function (m) { acc.push([m, t0, 2]); });
          else if (v.fig === 1) [bass, ch[2] || ch[1], ch[1], ch[2] || ch[1]].forEach(function (m, i) { acc.push([m, t0 + 0.5 * i, 0.5]); });
          else if (v.fig === 2) { acc.push([bass - 12, t0, 2]); for (var r = 0; r < 4; r++) ch.slice(1).forEach(function (m) { acc.push([m, t0 + 0.5 * r, 0.45]); }); }
          else for (var r2 = 0; r2 < 4; r2++) acc.push([bass + (r2 % 2 ? 12 : 0) - 12, t0 + 0.5 * r2, 0.5]);
        });
        s.notes = notes.concat(acc);
        var changes = 0;
        for (q = 1; q < 8; q++) if (cs[q] !== cs[q - 1]) changes++;
        s.changes = changes; s.cad = cadence26(prev, last); s.cs = cs;
        var a = g[0].axes({ x: [0, 16], y: [30, 86], title: "The phrase", xlabel: "beats", ylabel: "key number", xticks: [0, 4, 8, 12, 16] });
        acc.forEach(function (n) { a.line([n[1] + 0.03, n[1] + n[2] - 0.03], [n[0], n[0]], { color: "#8A93A0", width: 5 }); });
        notes.forEach(function (n) { a.line([n[1] + 0.04, n[1] + n[2] - 0.04], [n[0], n[0]], { color: C.idea, width: 7 }); });
        cs.forEach(function (c, h) { a.text(2 * h + 1, 33, CH26[c][0], { align: "center", size: 11, color: C.muted }); });
        var b = g[1].axes({ x: [-0.6, 1.6], y: [0, 100], title: "Chord changes per 100 half-bars", xticks: [], ylabel: "in 100" });
        b.bars([0, 1], [100 * changes / 7, 85], 0.5, { color: function (i) { return i ? "#8A93A0" : C.idea; } });
        b.text(0, 0, "your phrase", { align: "center", base: "top", dy: 7, size: 10, color: C.muted });
        b.text(1, 0, "quartets: pitch classes per beat", { align: "center", base: "top", dy: 7, size: 10, color: C.muted });
      },
      readout: function (v, s) {
        return [["cadence", s.cad[0] + ": " + s.cad[1]], ["chord changes", s.changes + " of 7 half-bar boundaries"],
                ["chords", s.cs.map(function (c) { return CH26[c][0]; }).join(" ")],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "End on V and the phrase asks a question; follow it with the same opening ending V to I and you have a period, the film's basic unit. Change the figure and the energy changes while the harmony stays: the accompaniment is the style's motor."
    });
  };

  // ---- Part 27: rubato, two ways ----------------------------------------------------------------------------------
  var TUNE27 = [[72, 0, 1], [72, 1, 1], [79, 2, 1], [79, 3, 1], [81, 4, 1], [81, 5, 1], [79, 6, 2], [77, 8, 1], [77, 9, 1], [76, 10, 1], [76, 11, 1], [74, 12, 1], [74, 13, 1], [72, 14, 2]];
  var BASS27 = [[48, 0, 2], [48, 2, 2], [53, 4, 2], [48, 6, 2], [43, 8, 2], [48, 10, 2], [43, 12, 2], [48, 14, 2]];
  function arch27(b, depth, power) {   // performance time of score beat b under Todd's phrase arch, phrases of 8 beats
    var n = Math.max(1, Math.round(b * 48)), t = 0, i;
    for (i = 0; i < n; i++) {
      var x = (i + 0.5) / 48, u = (x % 8) / 8;
      var tempo = 1 + depth * (1 - Math.pow(Math.abs(2 * u - 1), power)) - depth * (1 - 1 / (power + 1));
      t += (1 / 48) / tempo;
    }
    return t * b * 48 / n;
  }
  function stolen27(b, amount) { var bar = Math.floor(b / 2) * 2, u = (b - bar) / 2; return bar + 2 * (u + amount * Math.sin(Math.PI * u)); }
  W.rubato = function (el) {
    QB.widget(el, {
      title: "Bend the time",
      sub: "The Tune's first two phrases over a bass. Arch the tempo of the whole texture, as Todd's model does (slower at a phrase's ends, faster in its middle), or steal time in the melody alone while the bass keeps strict time, as Mozart described in 1777. Left: when each melody note sounds, against strict time. Right: the tempo the listener hears.",
      panels: 2, height: 280,
      controls: [
        { k: "depth", label: "Phrase arch depth", min: 0, max: 0.5, step: 0.02, value: 0.24, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "power", label: "Arch shape (2 = parabola)", min: 1, max: 4, step: 0.5, value: 2, fmt: function (x) { return x.toFixed(1); } },
        { k: "steal", label: "Stolen time in the melody", min: 0, max: 0.3, step: 0.02, value: 0, fmt: function (x) { return Math.round(100 * x) + "% of a bar"; } }
      ],
      buttons: [{ label: "Play", act: function (s) { s.sound = play(notesSound(s.notes, 0.45), 44100); } }],
      init: function (s) { s.sound = null; s.notes = []; },
      draw: function (g, v, s) {
        var tm = function (b) { return stolen27(arch27(b, v.depth, v.power), v.steal); };
        var tb = function (b) { return arch27(b, v.depth, v.power); };
        s.notes = TUNE27.map(function (n) { var a = tm(n[1]); return [n[0], a, Math.max(0.2, tm(n[1] + n[2]) - a)]; })
          .concat(BASS27.map(function (n) { var a = tb(n[1]); return [n[0], a, tb(n[1] + n[2]) - a]; }));
        var a = g[0].axes({ x: [0, 16], y: [-0.8, 0.8], title: "Melody: performed minus written (beats)", xlabel: "written beat", ylabel: "early - / late +", xticks: [0, 4, 8, 12, 16] });
        a.line([0, 16], [0, 0], { color: "#8A93A0", width: 2 });
        var xs = TUNE27.map(function (n) { return n[1]; }), dev = xs.map(function (x) { return tm(x) - x; });
        a.line(xs, dev, { color: C.idea, width: 2 });
        a.dots(xs, dev, { color: C.idea, r: 4 });
        var bx = BASS27.map(function (n) { return n[1]; });
        a.dots(bx, bx.map(function (x) { return tb(x) - x; }), { color: "#8A93A0", r: 4 });
        var grid = [], tempo = [], i;
        for (i = 0; i <= 160; i++) { var x = i / 10; grid.push(x); tempo.push(0.1 / Math.max(1e-6, arch27(x + 0.05, v.depth, v.power) - arch27(Math.max(0, x - 0.05), v.depth, v.power)) * (x > 0.05 ? 1 : 0.5)); }
        var b = g[1].axes({ x: [0, 16], y: [0.5, 1.5], title: "Tempo of the texture (1 = strict)", xlabel: "written beat", xticks: [0, 4, 8, 12, 16] });
        b.line([0, 16], [1, 1], { color: "#8A93A0", width: 2 });
        b.line(grid.slice(1), tempo.slice(1), { color: C.idea, width: 3 });
        s.total = tm(16);
      },
      readout: function (v, s) {
        return [["length of the two phrases", s.total.toFixed(2) + " beats (strict: 16)"],
                ["kind of rubato", v.steal > 0 && v.depth > 0 ? "both: an arch, and stolen time on top" : v.steal > 0 ? "stolen: the bass keeps time" : v.depth > 0 ? "an arch: everything bends" : "none: strict"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "A phrase arch keeps each phrase about its written length while moving time from its ends to its middle; stolen time keeps the bar lines exactly where they were. Recorded pianists do both, in proportions that changed over the twentieth century."
    });
  };
})();
