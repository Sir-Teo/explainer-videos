// Interactives for Act II, Notes (Parts 10-22).  As in Act I, each can be heard: the sound is computed in the page
// and played through the browser's Web Audio after a click.  Nothing is downloaded.
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

  // ---- Part 10: the same signs, another tune ----------------------------------------------------------------
  var CONTOUR = [0, 1, 0, 1, 0, -1], BEATS = [1, 1, 1, 1, 1, 1, 2], TUNE = [0, 0, 4, 4, 5, 5, 4];
  var MAJOR = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16], LETTERS = ["C", "D", "E", "F", "G", "A", "B"];
  var KEYS = [["C", 60, 0], ["D", 62, 1], ["F", 65, 3], ["G", 67, 4]];       // name, key number of the tonic, its letter

  // ways[k][s]: how many ways to finish the melody from note k standing on step s (the film's dynamic programme)
  function waysTable(span) {
    var n = CONTOUR.length + 1, w = [], k, s, j;
    for (k = 0; k < n; k++) { w.push([]); for (s = 0; s < span; s++) w[k].push(k === n - 1 ? 1 : 0); }
    for (k = n - 2; k >= 0; k--) for (s = 0; s < span; s++) {
      var sum = 0;
      if (CONTOUR[k] > 0) for (j = s + 1; j < span; j++) sum += w[k + 1][j];
      else if (CONTOUR[k] < 0) for (j = 0; j < s; j++) sum += w[k + 1][j];
      else sum = w[k + 1][s];
      w[k][s] = sum;
    }
    return w;
  }
  function countAll(w) { var t = 0, s; for (s = 0; s < w[0].length; s++) t += w[0][s]; return t; }
  // the index-th melody with the contour, in dictionary order
  function melody(w, index) {
    var span = w[0].length, out = [], s, k, options;
    for (s = 0; s < span; s++) { if (index < w[0][s]) break; index -= w[0][s]; }
    out.push(Math.min(s, span - 1));
    for (k = 0; k < CONTOUR.length; k++) {
      var cur = out[out.length - 1];
      options = [];
      if (CONTOUR[k] > 0) for (s = cur + 1; s < span; s++) options.push(s);
      else if (CONTOUR[k] < 0) for (s = 0; s < cur; s++) options.push(s);
      else options.push(cur);
      for (s = 0; s < options.length; s++) { if (index < w[k + 1][options[s]]) break; index -= w[k + 1][options[s]]; }
      out.push(options[Math.min(s, options.length - 1)]);
    }
    return out;
  }
  function tuneSound(keys) {
    var rate = 44100, beat = 0.42, total = 0, i, n, h;
    for (i = 0; i < BEATS.length; i++) total += BEATS[i];
    var out = new Float32Array(Math.floor((total * beat + 0.8) * rate)), t0 = 0;
    for (i = 0; i < keys.length; i++) {
      var hz = 440 * Math.pow(2, (keys[i] - 69) / 12), start = Math.floor(t0 * rate), len = Math.floor((BEATS[i] * beat + 0.7) * rate);
      for (n = 0; n < len && start + n < out.length; n++) {
        var t = n / rate, y = 0;
        for (h = 1; h <= 6; h++) y += Math.sin(2 * Math.PI * hz * h * t) / (h * h) * Math.exp(-t * (2.2 + 0.9 * h));
        out[start + n] += 0.32 * y * Math.min(1, t / 0.004);
      }
      t0 += BEATS[i] * beat;
    }
    return play(out, rate);
  }

  W.notation = function (el) {
    QB.widget(el, {
      title: "The same signs, another tune",
      sub: "The signs over the first phrase of the Tune say: the same, up, the same, up, the same, down. Choose how many notes of the scale a singer may use, and step through every melody that fits. Left: the melody on a staff. Right: the same melody as a piano roll. Then change the key and see which notation has to be redrawn.",
      panels: 2, height: 300,
      controls: [
        { k: "span", label: "Notes of the scale to choose from", min: 3, max: 9, step: 1, value: 6 },
        { k: "which", label: "Which of the melodies that fit", min: 0, max: 1, step: 0.001, value: 0.72, fmt: function (x, v) { return ""; } },
        { k: "key", label: "The key (1 = ...)", min: 0, max: 3, step: 1, value: 0, fmt: function (k) { return KEYS[k][0]; } },
      ],
      buttons: [
        { label: "Play it", act: function (s) { s.sound = tuneSound(s.keys); } },
        { label: "Show the Tune", act: function (s, v) { s.force = true; } },
      ],
      init: function (s) { s.sound = null; s.force = false; s.keys = []; },
      draw: function (g, v, s) {
        var w = waysTable(v.span), total = countAll(w), index = Math.min(total - 1, Math.floor(v.which * total));
        var steps = melody(w, index), i;
        if (s.force && v.span >= 6) steps = TUNE.slice();
        s.force = false;
        var key = KEYS[v.key], keys = [], names = [], xs = [], t = 0, isTune = true;
        for (i = 0; i < steps.length; i++) {
          keys.push(key[1] + MAJOR[steps[i]]);
          names.push(LETTERS[(key[2] + steps[i]) % 7]);
          xs.push(t + BEATS[i] / 2); t += BEATS[i];
          if (steps[i] !== TUNE[i]) isTune = false;
        }
        s.steps = steps; s.keys = keys; s.names = names; s.total = total; s.index = index; s.isTune = isTune;
        // the staff: lines are every second letter; a note's height is its letter, not its key number
        var pos = steps.map(function (st) { return key[2] + st; });            // letters above C
        var a = g[0].axes({ x: [-0.6, 8.4], y: [-3, 13], title: "On a staff (a step of the scale is one line or space)", xticks: [], yticks: [] });
        for (i = 0; i < 5; i++) a.line([-0.6, 8.4], [2 + 2 * i, 2 + 2 * i], { color: C.muted, width: 1 });
        for (i = 0; i < pos.length; i++) {
          if (pos[i] <= 0) a.line([xs[i] - 0.35, xs[i] + 0.35], [0, 0], { color: C.muted, width: 1 });
          if (pos[i] >= 12) a.line([xs[i] - 0.35, xs[i] + 0.35], [12, 12], { color: C.muted, width: 1 });
        }
        a.dots(xs, pos, { color: isTune ? C.idea : C.implied, r: 6 });
        for (i = 0; i < pos.length; i++) a.text(xs[i], -2.2, String(steps[i] % 7 + 1), { color: C.muted, align: "center" });
        var lo = Math.min.apply(null, keys) - 2, hi = Math.max.apply(null, keys) + 2;
        var b = g[1].axes({ x: [0, 8], y: [Math.min(lo, 58), Math.max(hi, 72)], title: "As a piano roll (a key of the piano is one row)", xlabel: "beats", ylabel: "key number" });
        t = 0;
        for (i = 0; i < keys.length; i++) {
          b.line([t + 0.06, t + BEATS[i] - 0.06], [keys[i], keys[i]], { color: isTune ? C.idea : C.implied, width: 7 });
          t += BEATS[i];
        }
      },
      readout: function (v, s) {
        var signs = ["first"].concat(CONTOUR.map(function (c) { return c > 0 ? "up" : c < 0 ? "down" : "same"; })).join(", ");
        var bits = Math.log(Math.pow(v.span, 7)) / Math.LN2, left = Math.log(s.total) / Math.LN2;
        return [["the signs", signs],
                ["melodies that fit, on " + v.span + " notes", s.total + " of " + Math.pow(v.span, 7) + "  (this is number " + (s.index + 1) + ")"],
                ["bits the signs leave open", fmt(left, 1) + " of " + fmt(bits, 1)],
                ["this melody, in letters", s.names.join(" ") + (s.isTune ? "   (the Tune)" : "")],
                ["in numbers (jianpu), 1 = " + KEYS[v.key][0], s.steps.map(function (st) { return st % 7 + 1; }).join(" ") + " -"],
                ["as key numbers (MIDI)", s.keys.join(" ")],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Signs that say only up, down or the same fit many melodies: 85 on six notes, 322 on eight. They remind a singer of a tune already known; they cannot teach one. Change the key: on the staff every note moves, and on the piano roll every key number changes, but the line of numbers stays as it was, because numbered notation writes a note's place in its scale. Each notation keeps something different."
    });
  };
})();
