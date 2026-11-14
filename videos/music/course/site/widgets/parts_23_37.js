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
})();
