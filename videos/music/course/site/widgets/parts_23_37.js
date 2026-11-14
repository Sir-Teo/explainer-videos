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

  // ---- Part 28: a scale's symmetry ------------------------------------------------------------------------------
  var NAMES28 = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"];
  var SCALES28 = { "octatonic": [0, 1, 3, 4, 6, 7, 9, 10], "diatonic": [0, 2, 4, 5, 7, 9, 11], "whole-tone": [0, 2, 4, 6, 8, 10], "pentatonic": [0, 2, 4, 7, 9] };
  var MODES28 = [[0, 2, 4, 6, 8, 10], [0, 1, 3, 4, 6, 7, 9, 10], [0, 2, 3, 4, 6, 7, 8, 10, 11], [0, 1, 2, 5, 6, 7, 8, 11], [0, 1, 5, 6, 7, 11], [0, 2, 4, 5, 6, 8, 10, 11], [0, 1, 2, 3, 5, 6, 7, 8, 9, 11]];
  function mask28(pcs) { var m = 0; pcs.forEach(function (p) { m |= 1 << (((p % 12) + 12) % 12); }); return m; }
  function rot28(m, k) { k = ((k % 12) + 12) % 12; return ((m << k) | (m >>> (12 - k))) & 4095; }
  function period28(m) { for (var k = 1; k <= 12; k++) if (rot28(m, k) === m) return k; return 12; }
  function tclass28(m) { var best = m; for (var k = 1; k < 12; k++) best = Math.min(best, rot28(m, k)); return best; }
  function fits28(m, sc) { var s = mask28(sc); for (var k = 0; k < 12; k++) if ((m & ~rot28(s, k)) === 0) return true; return false; }
  function pop28(m) { var c = 0; while (m) { c += m & 1; m >>>= 1; } return c; }
  var CHANCE28 = {};
  function chance28(k, name) {
    var key = name + k; if (CHANCE28[key] !== undefined) return CHANCE28[key];
    var hits = 0, tot = 0;
    for (var m = 0; m < 4096; m++) if (pop28(m) === k) { tot++; if (fits28(m, SCALES28[name])) hits++; }
    return (CHANCE28[key] = tot ? hits / tot : 0);
  }
  W.symmetric = function (el) {
    var ctl = [], init = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0];
    for (var i = 0; i < 12; i++) ctl.push({ k: "p" + i, label: NAMES28[i], min: 0, max: 1, step: 1, value: init[i], fmt: function (x) { return x ? "in" : "out"; } });
    QB.widget(el, {
      title: "Does your scale map onto itself?",
      sub: "Switch pitch classes in and out. The page finds how many different transpositions your set has (12 for most sets; fewer for the fifteen symmetric shapes, Messiaen's seven modes among them), which common scales contain it, and how often a random set of the same size would fit each scale by chance, as the film computed.",
      panels: 2, height: 300,
      controls: ctl,
      buttons: [{ label: "Play", act: function (s) { s.sound = s.notes.length ? play(notesSound(s.notes, 0.32), 44100) : false; } }],
      init: function (s) { s.sound = null; s.notes = []; },
      draw: function (g, v, s) {
        var pcs = []; for (var i = 0; i < 12; i++) if (v["p" + i]) pcs.push(i);
        var m = mask28(pcs);
        s.pcs = pcs; s.m = m; s.per = pcs.length ? period28(m) : 1;
        s.mode = 0; MODES28.forEach(function (md, j) { if (tclass28(mask28(md)) === tclass28(m)) s.mode = j + 1; });
        s.notes = pcs.map(function (p, j) { return [60 + p, j, 1]; }).concat(pcs.length ? [[72 + pcs[0], pcs.length, 1.5]] : []);
        var a = g[0].axes({ x: [-1.5, 1.5], y: [-1.5, 1.5], title: "The twelve pitch classes", xticks: [], yticks: [] });
        var cx = [], cy = [];
        for (i = 0; i <= 60; i++) { cx.push(Math.cos(2 * Math.PI * i / 60)); cy.push(Math.sin(2 * Math.PI * i / 60)); }
        a.line(cx, cy, { color: "#8A93A0", width: 1 });
        var px = pcs.map(function (p) { return Math.sin(2 * Math.PI * p / 12); }), py = pcs.map(function (p) { return Math.cos(2 * Math.PI * p / 12); });
        if (pcs.length > 1) a.line(px.concat([px[0]]), py.concat([py[0]]), { color: C.idea, width: 2 });
        a.dots(px, py, { color: C.idea, r: 6 });
        for (i = 0; i < 12; i++) a.text(1.3 * Math.sin(2 * Math.PI * i / 12), 1.3 * Math.cos(2 * Math.PI * i / 12), NAMES28[i], { align: "center", size: 11, color: v["p" + i] ? C.ink : C.muted });
        var names = ["octatonic", "diatonic", "whole-tone", "pentatonic"], k = pcs.length;
        var b = g[1].axes({ x: [-0.6, 3.6], y: [0, 1], title: "Chance a random " + k + "-note set fits", xticks: [], ylabel: "share" });
        b.bars([0, 1, 2, 3], names.map(function (n) { return k ? chance28(k, n) : 0; }), 0.6, { color: function (j) { return fits28(m, SCALES28[names[j]]) ? C.idea : "#8A93A0"; } });
        names.forEach(function (n, j) { b.text(j, 0, n, { align: "center", base: "top", dy: 7, size: 10, color: C.muted }); });
      },
      readout: function (v, s) {
        var inside = Object.keys(SCALES28).filter(function (n) { return fits28(s.m, SCALES28[n]); });
        return [["notes", s.pcs.map(function (p) { return NAMES28[p]; }).join(" ") || "none"],
                ["different transpositions", String(s.per) + (s.per < 12 && s.pcs.length && s.pcs.length < 12 ? ": limited transposition" : "")],
                ["Messiaen's mode", s.mode ? String(s.mode) : "none"],
                ["scales that contain it (gold)", inside.length ? inside.join(", ") : "none of these"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Every symmetric set repeats a pattern every 1, 2, 3, 4 or 6 semitones. And a set that fits a scale is evidence only when a random set of its size would rarely fit: with four or five notes, it often would."
    });
  };

  // ---- Part 29: a set's class, vector and complement -------------------------------------------------------------
  function iv29(pcs) { var v = [0, 0, 0, 0, 0, 0]; for (var i = 0; i < pcs.length; i++) for (var j = i + 1; j < pcs.length; j++) { var d = ((pcs[j] - pcs[i]) % 12 + 12) % 12; v[Math.min(d, 12 - d) - 1]++; } return v; }
  function prime29(pcs) {
    if (!pcs.length) return [];
    function packed(s) {
      s = s.slice().sort(function (a, b) { return a - b; });
      var best = null;
      for (var r = 0; r < s.length; r++) {
        var rot = s.slice(r).concat(s.slice(0, r).map(function (x) { return x + 12; }));
        var norm = rot.map(function (x) { return x - rot[0]; });
        var key = norm.slice().reverse();
        if (!best || cmp29(key, best.key) < 0) best = { key: key, norm: norm };
      }
      return best;
    }
    var a = packed(pcs), b = packed(pcs.map(function (x) { return (12 - x) % 12; }));
    return (cmp29(a.key, b.key) <= 0 ? a : b).norm;
  }
  function cmp29(x, y) { for (var i = 0; i < x.length; i++) if (x[i] !== y[i]) return x[i] - y[i]; return 0; }
  W.setclass = function (el) {
    var ctl = [], init = [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0];
    for (var i = 0; i < 12; i++) ctl.push({ k: "p" + i, label: NAMES28[i], min: 0, max: 1, step: 1, value: init[i], fmt: function (x) { return x ? "in" : "out"; } });
    QB.widget(el, {
      title: "Name a chord the way set theory does",
      sub: "Switch pitch classes in and out. The page finds the set's prime form (its name up to transposition and inversion) and its interval vector (how many pairs lie 1 to 6 semitones apart), and compares the vector with that of the notes left out. For six notes the two vectors are always equal: Babbitt's hexachord theorem, which the film checked on all 924 hexachords and proved.",
      panels: 2, height: 300,
      controls: ctl,
      buttons: [{ label: "Play", act: function (s) { s.sound = s.notes.length ? play(notesSound(s.notes, 0.5), 44100) : false; } }],
      init: function (s) { s.sound = null; s.notes = []; },
      draw: function (g, v, s) {
        var pcs = [], comp = [], i;
        for (i = 0; i < 12; i++) (v["p" + i] ? pcs : comp).push(i);
        s.pcs = pcs; s.comp = comp; s.pf = prime29(pcs); s.iv = iv29(pcs); s.ivc = iv29(comp);
        s.notes = pcs.map(function (p) { return [60 + p, 0, 2]; }).concat(pcs.map(function (p, j) { return [60 + p, 2.2 + 0.5 * j, 0.5]; }));
        var a = g[0].axes({ x: [-1.5, 1.5], y: [-1.5, 1.5], title: "The set (gold) and its complement (grey)", xticks: [], yticks: [] });
        var cx = [], cy = [];
        for (i = 0; i <= 60; i++) { cx.push(Math.cos(2 * Math.PI * i / 60)); cy.push(Math.sin(2 * Math.PI * i / 60)); }
        a.line(cx, cy, { color: "#8A93A0", width: 1 });
        var px = pcs.map(function (p) { return Math.sin(2 * Math.PI * p / 12); }), py = pcs.map(function (p) { return Math.cos(2 * Math.PI * p / 12); });
        if (pcs.length > 1) a.line(px.concat([px[0]]), py.concat([py[0]]), { color: C.idea, width: 2 });
        a.dots(px, py, { color: C.idea, r: 6 });
        a.dots(comp.map(function (p) { return Math.sin(2 * Math.PI * p / 12); }), comp.map(function (p) { return Math.cos(2 * Math.PI * p / 12); }), { color: "#8A93A0", r: 4 });
        for (i = 0; i < 12; i++) a.text(1.3 * Math.sin(2 * Math.PI * i / 12), 1.3 * Math.cos(2 * Math.PI * i / 12), NAMES28[i], { align: "center", size: 11, color: v["p" + i] ? C.ink : C.muted });
        var top = Math.max(1, Math.max.apply(null, s.iv.concat(s.ivc)));
        var b = g[1].axes({ x: [0.3, 6.7], y: [0, top + 1], title: "Interval vectors: set (gold), complement (grey)", xticks: [1, 2, 3, 4, 5, 6], xlabel: "interval class" });
        b.bars([0.85, 1.85, 2.85, 3.85, 4.85, 5.85], s.iv, 0.3, { color: C.idea });
        b.bars([1.15, 2.15, 3.15, 4.15, 5.15, 6.15], s.ivc, 0.3, { color: "#8A93A0" });
      },
      readout: function (v, s) {
        var diff = s.ivc.map(function (x, i) { return x - s.iv[i]; });
        return [["prime form", "(" + s.pf.join(" ") + ")"], ["interval vector", "[" + s.iv.join("") + "]"],
                ["complement's vector minus the set's", "[" + diff.join(", ") + "]" + (s.pcs.length === 6 ? ": zero, as the theorem says" : " = (12 - 2k) times (1,1,1,1,1,1/2)")],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Try {0, 1, 4, 6} and {0, 1, 3, 7}: different prime forms, the same vector [111111]. Then any six notes: the complement's vector always matches."
    });
  };

  // ---- Part 30: a cloud, random or even ------------------------------------------------------------------------------
  function rng30(seed) { var x = seed * 2654435761 % 4294967296 || 1; return function () { x ^= x << 13; x >>>= 0; x ^= x >>> 17; x ^= x << 5; x >>>= 0; return x / 4294967296; }; }
  function fact30(k) { var f = 1; for (var i = 2; i <= k; i++) f *= i; return f; }
  W.poissoncloud = function (el) {
    QB.widget(el, {
      title: "A cloud of notes: random or even?",
      sub: "Notes at random moments (a Poisson process, as in Xenakis's clouds) or evenly spaced, at the rate you choose. Left: the cloud over ten seconds. Right: how many seconds held 0, 1, 2 ... notes over ten minutes of the same cloud, against Poisson's law. Random moments clump; even ones never do.",
      panels: 2, height: 280,
      controls: [
        { k: "rate", label: "Notes per second", min: 1, max: 20, step: 1, value: 5, fmt: function (x) { return x + " a second"; } },
        { k: "even", label: "Timing", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "evenly spaced" : "random (Poisson)"; } },
        { k: "seed", label: "Seed", min: 1, max: 20, step: 1, value: 1, fmt: function (x) { return String(x); } }
      ],
      buttons: [{ label: "Play", act: function (s) { s.sound = play(notesSound(s.notes, 1.0), 44100); } }],
      init: function (s) { s.sound = null; s.notes = []; },
      draw: function (g, v, s) {
        var r = rng30(v.seed), t = 0, on = [], i;
        if (v.even) { for (i = 0; i < v.rate * 10; i++) on.push(i / v.rate); }
        else { while (true) { t += -Math.log(1 - r()) / v.rate; if (t >= 10) break; on.push(t); } }
        s.notes = on.map(function (x) { return [60 + Math.floor(r() * 24), x, 0.15]; });
        var a = g[0].axes({ x: [0, 10], y: [58, 86], title: "Ten seconds of the cloud", xlabel: "seconds", ylabel: "key number" });
        s.notes.forEach(function (n) { a.line([n[1], n[1] + 0.12], [n[0], n[0]], { color: C.idea, width: 5 }); });
        var counts = [], k, hist = [];
        var r2 = rng30(v.seed + 100);
        for (i = 0; i < 600; i++) {
          var c = 0;
          if (v.even) c = v.rate; else { var tt = -Math.log(1 - r2()) / v.rate; while (tt < 1) { c++; tt += -Math.log(1 - r2()) / v.rate; } }
          counts.push(c);
        }
        var top = Math.max(12, v.rate * 2 + 4);
        for (k = 0; k <= top; k++) hist.push(0);
        counts.forEach(function (c) { if (c <= top) hist[c]++; });
        var mean = counts.reduce(function (p, q) { return p + q; }, 0) / 600;
        s.var = counts.reduce(function (p, q) { return p + (q - mean) * (q - mean); }, 0) / 600; s.mean = mean;
        var ymax = Math.max.apply(null, hist) * 1.15;
        var b = g[1].axes({ x: [-0.6, top + 0.6], y: [0, ymax], title: "Seconds holding k notes (bars) and Poisson's law (dots)", xlabel: "k" });
        b.bars(hist.map(function (_, j) { return j; }), hist, 0.7, { color: C.idea });
        var px = [], py = [];
        for (k = 0; k <= top; k++) { px.push(k); py.push(600 * Math.exp(-v.rate) * Math.pow(v.rate, k) / fact30(k)); }
        b.dots(px, py, { color: "#F472B6", r: 4 });
      },
      readout: function (v, s) {
        return [["per-second counts: mean, variance", s.mean.toFixed(2) + ", " + s.var.toFixed(2)],
                ["Poisson says", "mean = variance = " + v.rate + (v.even ? " (an even cloud has variance 0)" : "")],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Play both versions at the same rate: the random one bursts and pauses, the even one is heard as a pulse. A random process's counts vary as much as their mean; that variance is the clumping you hear."
    });
  };
  // ---------------------------------------------------------------------------------------------- Part 31: the Tonnetz
  var TRI31 = [];
  (function () { for (var r = 0; r < 12; r++) { TRI31.push([r, "M"]); TRI31.push([r, "m"]); } })();
  var PCN31 = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"];
  function name31(t) { return PCN31[t[0]] + (t[1] === "m" ? "m" : ""); }
  function pcs31(t) { var r = t[0]; return t[1] === "M" ? [r, (r + 4) % 12, (r + 7) % 12] : [r, (r + 3) % 12, (r + 7) % 12]; }
  function mv31(k, t) {
    var r = t[0], q = t[1];
    if (k === "P") return [r, q === "M" ? "m" : "M"];
    if (k === "R") return q === "M" ? [(r + 9) % 12, "m"] : [(r + 3) % 12, "M"];
    return q === "M" ? [(r + 4) % 12, "m"] : [(r + 8) % 12, "M"];
  }
  function key31(t) { return t[0] + t[1]; }
  function path31(a, b) {
    var prev = {}, q = [a], seen = {}; seen[key31(a)] = true;
    while (q.length) {
      var t = q.shift();
      if (key31(t) === key31(b)) break;
      ["P", "L", "R"].forEach(function (k) { var u = mv31(k, t); if (!seen[key31(u)]) { seen[key31(u)] = true; prev[key31(u)] = [t, k]; q.push(u); } });
    }
    var out = [b], word = "", cur = b;
    while (key31(cur) !== key31(a)) { var pr = prev[key31(cur)]; word = pr[1] + word; cur = pr[0]; out.unshift(cur); }
    return { chain: out, word: word };
  }
  function vl31(a, b) {
    var A = pcs31(a).slice().sort(function (x, y) { return x - y; }), B = pcs31(b), best = 99;
    [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]].forEach(function (p) {
      var d = 0; for (var i = 0; i < 3; i++) { var x = ((B[p[i]] - A[i]) % 12 + 12) % 12; d += Math.min(x, 12 - x); }
      best = Math.min(best, d);
    });
    return best;
  }
  function voice31(chain) {
    var out = [], prev = null;
    chain.forEach(function (t) {
      var s = pcs31(t), notes = [];
      if (!prev) { notes = s.map(function (pc) { return 55 + ((pc - 55) % 12 + 12) % 12; }).sort(function (x, y) { return x - y; }); }
      else {
        var used = {};
        prev.forEach(function (m) {
          var best = null;
          s.forEach(function (pc) { if (used[pc]) return; var c = m + ((pc - m + 6) % 12 + 12) % 12 - 6; if (best === null || Math.abs(c - m) < Math.abs(best[0] - m)) best = [c, pc]; });
          notes.push(best[0]); used[best[1]] = true;
        });
      }
      out.push(notes); prev = notes;
    });
    return out;
  }
  W.tonnetz = function (el) {
    QB.widget(el, {
      title: "The Tonnetz: the shortest walk between two triads",
      sub: "Every pitch class is a node: a fifth to the right, a major third up and to the right, a minor third up and to the left. Every triangle is a triad, major pointing up and minor pointing down. Choose two triads: the page finds the fewest P, L and R flips between them, by breadth-first search, and draws the walk.",
      panels: 1, height: 340,
      controls: [
        { k: "a", label: "From", min: 0, max: 23, step: 1, value: 0, fmt: function (x) { return name31(TRI31[x]); } },
        { k: "b", label: "To", min: 0, max: 23, step: 1, value: 17, fmt: function (x) { return name31(TRI31[x]); } }
      ],
      buttons: [{ label: "Play the walk", act: function (s) {
        var notes = [];
        voice31(s.chain).forEach(function (ch, i) { ch.forEach(function (m) { notes.push([m, i, 0.95]); }); notes.push([s.chain[i][0] + 36, i, 0.95]); });
        s.sound = play(notesSound(notes, 0.8), 44100);
      } }],
      init: function (s) { s.sound = null; s.chain = []; },
      draw: function (g, v, s) {
        var A = TRI31[v.a], B = TRI31[v.b], res = path31(A, B);
        s.chain = res.chain; s.word = res.word;
        var a = g[0].axes({ x: [-3.2, 7.2], y: [-2.6, 3.4], title: "The Tonnetz, with the walk", noX: true, noY: true });
        var i, j, X = function (i, j) { return i + 0.5 * j; }, Y = function (i, j) { return 0.866 * j; };
        var pc = function (i, j) { return ((7 * i + 4 * j) % 12 + 12) % 12; };
        for (j = -3; j <= 4; j++) for (i = -5; i <= 8; i++) {
          a.line([X(i, j), X(i + 1, j)], [Y(i, j), Y(i + 1, j)], { color: "#3a475c", width: 1 });
          a.line([X(i, j), X(i, j + 1)], [Y(i, j), Y(i, j + 1)], { color: "#3a475c", width: 1 });
          a.line([X(i + 1, j), X(i, j + 1)], [Y(i + 1, j), Y(i, j + 1)], { color: "#3a475c", width: 1 });
        }
        // a triangle for each triad of the walk, each the nearest copy to the last
        var cx = 2, cy = 0.4, tris = [];
        res.chain.forEach(function (t) {
          var best = null;
          for (j = -3; j <= 3; j++) for (i = -5; i <= 7; i++) {
            if (pc(i, j) !== t[0]) continue;
            var pts = t[1] === "M" ? [[i, j], [i + 1, j], [i, j + 1]] : [[i, j], [i + 1, j], [i + 1, j - 1]];
            var mx = 0, my = 0; pts.forEach(function (p) { mx += X(p[0], p[1]) / 3; my += Y(p[0], p[1]) / 3; });
            var d = (mx - cx) * (mx - cx) + (my - cy) * (my - cy);
            if (best === null || d < best[0]) best = [d, pts, mx, my];
          }
          tris.push(best); cx = best[2]; cy = best[3];
        });
        tris.forEach(function (tr, k) {
          var p = tr[1], col = k === 0 ? C.idea : (k === tris.length - 1 ? "#F472B6" : "#60A5FA");
          a.line([X(p[0][0], p[0][1]), X(p[1][0], p[1][1]), X(p[2][0], p[2][1]), X(p[0][0], p[0][1])],
                 [Y(p[0][0], p[0][1]), Y(p[1][0], p[1][1]), Y(p[2][0], p[2][1]), Y(p[0][0], p[0][1])], { color: col, width: 3.5 });
          a.text(tr[2], tr[3], name31(res.chain[k]), { align: "center", color: col, size: 11, bold: true });
        });
        tris.slice(1).forEach(function (tr, k) { a.line([tris[k][2], tr[2]], [tris[k][3], tr[3]], { color: C.muted, width: 1.2, dash: [3, 3] }); });
        for (j = -3; j <= 4; j++) for (i = -5; i <= 8; i++) {
          var x = X(i, j), y = Y(i, j);
          if (x < -3.1 || x > 7.1 || y < -2.5 || y > 3.3) continue;
          a.text(x, y, PCN31[pc(i, j)], { align: "center", size: 10.5, bg: true, color: C.muted });
        }
      },
      readout: function (v, s) {
        var A = TRI31[v.a], B = TRI31[v.b], common = pcs31(A).filter(function (x) { return pcs31(B).indexOf(x) >= 0; }).length;
        return [["walk", s.chain.map(name31).join(" → ")],
                ["shortest word", (s.word || "(the same triad)") + " — " + s.word.length + " step" + (s.word.length === 1 ? "" : "s")],
                ["notes in common; semitones moved directly", common + "; " + vl31(A, B)],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "C major to B flat minor is five steps, the farthest any triad is from C; C major to A flat minor, the hexatonic pole, is three steps yet only three semitones of voice leading. Distance in moves and distance in semitones are two different measures."
    });
  };
  // ------------------------------------------------------------------------------------- Part 32: the triangle of chords
  function sorted32(c) { return c.map(function (x) { return ((x % 12) + 12) % 12; }).sort(function (a, b) { return a - b; }); }
  function vl32(a, b) {
    var best = null, P = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]];
    P.forEach(function (p) {
      var mv = [], tot = 0;
      for (var i = 0; i < 3; i++) { var d = ((b[p[i]] - a[i]) % 12 + 12) % 12; if (d > 6) d -= 12; mv.push(d); tot += Math.abs(d); }
      if (best === null || tot < best[0] - 1e-9) best = [tot, mv];
    });
    return best;
  }
  function even32(c) {
    var x = sorted32(c), best = 1e9;
    for (var r = 0; r < 3; r++) {
      var y = x.slice(r).concat(x.slice(0, r).map(function (v) { return v + 12; }));
      var e = y.map(function (v, i) { return v - 4 * i; }), m = (e[0] + e[1] + e[2]) / 3;
      best = Math.min(best, Math.sqrt(e.reduce(function (s, v) { return s + (v - m) * (v - m); }, 0)));
    }
    return best;
  }
  function shapeXY32(c) {
    var x = sorted32(c), st = [x[1] - x[0], x[2] - x[1], 12 - (x[2] - x[0])];
    var V = [[0, 1], [-0.866, -0.5], [0.866, -0.5]], px = 0, py = 0;
    for (var k = 0; k < 3; k++) { px += st[k] / 12 * V[k][0]; py += st[k] / 12 * V[k][1]; }
    return [px, py];
  }
  function dft32(c, k) {
    var re = 0, im = 0; c.forEach(function (x) { re += Math.cos(2 * Math.PI * k * x / 12); im -= Math.sin(2 * Math.PI * k * x / 12); });
    return Math.sqrt(re * re + im * im);
  }
  var TARGETS32 = [["C major", [0, 4, 7]], ["C minor", [0, 3, 7]], ["F major", [5, 9, 0]], ["E major", [4, 8, 11]], ["A flat major", [8, 0, 3]],
                   ["F sharp major", [6, 10, 1]], ["augmented C", [0, 4, 8]], ["diminished C", [0, 3, 6]], ["cluster C C# D", [0, 1, 2]]];
  W.chordtriangle = function (el) {
    QB.widget(el, {
      title: "Three-note chords: the triangle, and the shortest way between two",
      sub: "Set three notes by sliders, in quarter-semitone steps if you like: the chord is a point in the triangle of shapes, with the perfectly even augmented triad at its centre. Choose a target chord: the page finds the smallest voice leading, the fewest semitones three voices must move, by trying every way to assign notes to voices.",
      panels: 1, height: 330,
      controls: [
        { k: "n1", label: "Note 1", min: 0, max: 11.75, step: 0.25, value: 0, fmt: function (x) { return x.toFixed(2); } },
        { k: "n2", label: "Note 2", min: 0, max: 11.75, step: 0.25, value: 4, fmt: function (x) { return x.toFixed(2); } },
        { k: "n3", label: "Note 3", min: 0, max: 11.75, step: 0.25, value: 7, fmt: function (x) { return x.toFixed(2); } },
        { k: "t", label: "Target", min: 0, max: TARGETS32.length - 1, step: 1, value: 2, fmt: function (x) { return TARGETS32[x][0]; } }
      ],
      buttons: [{ label: "Play: chord, target, chord", act: function (s) {
        var a = s.A.map(function (x) { return 60 + x; }), b = a.map(function (x, i) { return x + s.moves[i]; }), notes = [];
        [a, b, a, b].forEach(function (ch, i) { ch.forEach(function (m) { notes.push([m, i, 0.95]); }); });
        s.sound = play(notesSound(notes, 0.9), 44100);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        s.A = sorted32([v.n1, v.n2, v.n3]);
        var B = TARGETS32[v.t][1], r = vl32(s.A, B);
        s.size = r[0]; s.moves = r[1];
        var a = g[0].axes({ x: [-1.6, 1.6], y: [-0.75, 1.15], title: "The triangle of three-note shapes (transposition forgotten)", noX: true, noY: true });
        a.line([0, -0.866, 0.866, 0], [1, -0.5, -0.5, 1], { color: C.muted, width: 1.5 });
        var xs = [], ys = [], cs = [];
        for (var p = 0; p <= 12; p++) for (var q = 0; q <= 12 - p; q++) {
          var xy = shapeXY32([0, p, p + q]); xs.push(xy[0]); ys.push(xy[1]); cs.push(even32([0, p, p + q]));
        }
        a.dots(xs, ys, { r: 2.5, color: function (i) { return cs[i] < 1 ? C.idea : "#4b5563"; } });
        var pa = shapeXY32(s.A), pb = shapeXY32(B);
        a.line([pa[0], pb[0]], [pa[1], pb[1]], { color: C.muted, width: 1.2, dash: [4, 4] });
        a.dots([pb[0]], [pb[1]], { r: 7, color: "#60A5FA" });
        a.dots([pa[0]], [pa[1]], { r: 7, color: "#F472B6" });
        a.text(pa[0], pa[1] + 0.08, "your chord", { align: "center", color: "#F472B6", size: 11 });
        a.text(pb[0], pb[1] - 0.09, TARGETS32[v.t][0], { align: "center", color: "#60A5FA", size: 11 });
        a.text(0, 0.05, "augmented", { align: "center", color: C.muted, size: 10 });
      },
      readout: function (v, s) {
        return [["your chord (pitch classes)", s.A.map(function (x) { return x.toFixed(2); }).join(", ")],
                ["distance from even; |F3|, |F5|", even32(s.A).toFixed(2) + "; " + dft32(s.A, 3).toFixed(2) + ", " + dft32(s.A, 5).toFixed(2)],
                ["smallest voice leading to " + TARGETS32[v.t][0], s.size.toFixed(2) + " semitones: moves " + s.moves.map(function (m) { return (m >= 0 ? "+" : "") + m.toFixed(2); }).join(", ")],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "C major to F major is three semitones; to F sharp major, six, the most any triad needs. Move one slider by a quarter tone at a time from C major towards C minor: the point slides along the straight line between them, through the neutral triad."
    });
  };
  // ------------------------------------------------------------------------------------------- Part 33: Euclidean rhythms
  function euclid33(k, n) {
    if (k <= 0) { var z = []; for (var i = 0; i < n; i++) z.push(0); return z; }
    if (k >= n) { var o = []; for (var j = 0; j < n; j++) o.push(1); return o; }
    var a = [], b = [], q;
    for (q = 0; q < k; q++) a.push([1]);
    for (q = 0; q < n - k; q++) b.push([0]);
    while (b.length > 1) {
      var m = Math.min(a.length, b.length), na = [];
      for (q = 0; q < m; q++) na.push(a[q].concat(b[q]));
      var rest = a.length > m ? a.slice(m) : b.slice(m);
      a = na; b = rest;
    }
    var out = [];
    a.concat(b).forEach(function (g) { out = out.concat(g); });
    return out;
  }
  function rot33(p, r) { var n = p.length; return p.map(function (_, i) { return p[(i + r) % n]; }); }
  function gaps33(p) {
    var on = []; p.forEach(function (x, i) { if (x) on.push(i); });
    return on.map(function (o, i) { var nx = on[(i + 1) % on.length]; var d = (nx - o + p.length) % p.length; return d === 0 ? p.length : d; });
  }
  function odd33(p) { var n = p.length; if (n % 2) return null; for (var i = 0; i < n / 2; i++) if (p[i] && p[i + n / 2]) return false; return true; }
  var NAMED33 = { "3,8": "tresillo", "5,8": "cinquillo", "2,5": "khafif-e-ramal", "3,7": "ruchenitza", "4,9": "aksak", "5,12": "a Venda timeline",
                  "7,12": "the West African bell", "5,16": "bossa nova", "7,16": "a samba pattern", "3,4": "cumbia", "4,12": "four even beats" };
  W.euclid = function (el) {
    QB.widget(el, {
      title: "Euclidean rhythms: k strokes spread over n pulses",
      sub: "Bjorklund's algorithm, the one that timed a neutron accelerator, run in the page. Choose the strokes and pulses; rotate the necklace to start on a different stroke; and layer a second Euclidean rhythm against it. Read the clock as twelve semitones instead and E(7,12) is the major scale.",
      panels: 2, height: 300,
      controls: [
        { k: "k", label: "Strokes k", min: 1, max: 16, step: 1, value: 5 },
        { k: "n", label: "Pulses n", min: 2, max: 24, step: 1, value: 8 },
        { k: "r", label: "Rotation", min: 0, max: 23, step: 1, value: 0 },
        { k: "k2", label: "Second layer: strokes", min: 0, max: 16, step: 1, value: 3 }
      ],
      buttons: [{ label: "Play (four cycles)", act: function (s) {
        var notes = [], pulse = 0.16, n = s.p.length;
        for (var c = 0; c < 4; c++) {
          s.p.forEach(function (x, i) { if (x) notes.push([84, (c * n + i) * pulse / 0.16, 0.5]); });
          s.p2.forEach(function (x, i) { if (x) notes.push([60, (c * n + i) * pulse / 0.16, 0.5]); });
        }
        s.sound = play(notesSound(notes, 0.16), 44100);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        var k = Math.min(v.k, v.n), k2 = Math.min(v.k2, v.n);
        s.p = rot33(euclid33(k, v.n), v.r % v.n);
        s.p2 = k2 > 0 ? euclid33(k2, v.n) : [];
        var a = g[0].axes({ x: [-1.4, 1.4], y: [-1.3, 1.3], title: "The necklace: E(" + k + ", " + v.n + ") in gold, the second layer in blue", noX: true, noY: true });
        var cx = [], cy = [], i;
        for (i = 0; i <= 100; i++) { cx.push(Math.cos(2 * Math.PI * i / 100)); cy.push(Math.sin(2 * Math.PI * i / 100)); }
        a.line(cx, cy, { color: "#3a475c", width: 1 });
        var px = [], py = [], ox = [], oy = [], bx = [], by = [];
        for (i = 0; i < v.n; i++) {
          var ang = Math.PI / 2 - 2 * Math.PI * i / v.n, x = Math.cos(ang), y = Math.sin(ang);
          px.push(x); py.push(y);
          if (s.p[i]) { ox.push(x); oy.push(y); }
          if (s.p2[i]) { bx.push(0.75 * x); by.push(0.75 * y); }
        }
        a.dots(px, py, { r: 2.5, color: "#6b7280" });
        if (ox.length > 1) a.line(ox.concat([ox[0]]), oy.concat([oy[0]]), { color: C.idea, width: 2 });
        a.dots(ox, oy, { r: 6, color: C.idea });
        if (bx.length > 1) a.line(bx.concat([bx[0]]), by.concat([by[0]]), { color: "#60A5FA", width: 1.5 });
        a.dots(bx, by, { r: 4.5, color: "#60A5FA" });
        var gp = gaps33(s.p);
        var b = g[1].axes({ x: [-0.6, gp.length - 0.4], y: [0, Math.max.apply(null, gp) + 1], title: "Gaps between strokes, in pulses", xlabel: "stroke" });
        b.bars(gp.map(function (_, j) { return j; }), gp, 0.6, { color: C.idea });
      },
      readout: function (v, s) {
        var k = Math.min(v.k, v.n), gp = gaps33(s.p), od = odd33(s.p);
        return [["rhythm", s.p.map(function (x) { return x ? "x" : "."; }).join("")],
                ["gaps (never differing by more than one)", gp.join(" ")],
                ["oddity (no strokes half a cycle apart)", od === null ? "only defined for an even number of pulses" : (od ? "yes" : "no")],
                ["known as", NAMED33[k + "," + v.n] || "—"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Try 3 in 8 (the tresillo), 5 in 8 (the cinquillo), 7 in 12 (the bell pattern, and the major scale), 5 in 16 against 3. More than half the pulses and the oddity property is impossible: two strokes must face each other."
    });
  };
})();
