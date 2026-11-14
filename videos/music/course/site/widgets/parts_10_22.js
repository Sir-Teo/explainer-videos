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

  // ---- Part 11: a rhythm against the grid -------------------------------------------------------------------
  var WEIGHTS = [5, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1];
  var RHYTHMS = [["every beat", "x...x...x...x..."], ["son clave", "x..x..x...x.x..."], ["rumba clave", "x..x...x..x.x..."], ["bossa nova", "x..x..x...x..x.."],
                 ["tresillo, twice", "x..x..x.x..x..x."], ["every off-beat", "..x...x...x...x."]];
  function rotated(p, k) { k = ((k % 16) + 16) % 16; return p.slice(16 - k) + p.slice(0, 16 - k); }   // every note k pulses later
  // Longuet-Higgins and Lee: a note on a weak pulse, then silence on a stronger one before the next note
  function syncopation(p) {
    var notes = [], i, k, total = 0;
    for (i = 0; i < 16; i++) if (p.charAt(i) === "x") notes.push(i);
    for (k = 0; k < notes.length; k++) {
      var a = notes[k], b = notes[(k + 1) % notes.length], span = ((b - a) % 16 + 16) % 16 || 16, strongest = 0;
      for (i = 1; i < span; i++) strongest = Math.max(strongest, WEIGHTS[(a + i) % 16]);
      if (strongest > WEIGHTS[a]) total += strongest - WEIGHTS[a];
    }
    return total;
  }
  function rhythmSound(p, bpm) {
    var rate = 44100, pulse = 60 / bpm / 4, out = new Float32Array(Math.floor((32 * pulse + 0.4) * rate)), bar, i, n;
    function add(t0, hz, decay, gain, drop) {
      var start = Math.floor(t0 * rate), len = Math.floor(0.25 * rate);
      for (n = 0; n < len && start + n < out.length; n++) {
        var t = n / rate, f = hz * (1 + drop * Math.exp(-t / 0.03));
        out[start + n] += gain * Math.sin(2 * Math.PI * f * t) * Math.exp(-t * decay) * Math.min(1, t / 0.001);
      }
    }
    for (bar = 0; bar < 2; bar++) for (i = 0; i < 16; i++) {
      var t0 = (bar * 16 + i) * pulse;
      if (i % 4 === 0) add(t0, 70, 14, 0.5, 0.5);                       // a low drum on the four beats: the grid
      if (p.charAt(i) === "x") add(t0, 2350, 38, 0.4, 0);               // a clave on the rhythm
    }
    return play(out, rate);
  }

  W.rhythm = function (el) {
    QB.widget(el, {
      title: "A rhythm against the grid",
      sub: "Left: one bar of four-four in sixteenths. The grey bars are the metre's weights (how many levels of the metre each pulse belongs to); the dots are the notes of a rhythm. Slide the rhythm later, one pulse at a time, and watch its syncopation index change. Right: the index for all sixteen positions.",
      panels: 2, height: 300,
      controls: [
        { k: "which", label: "The rhythm", min: 0, max: RHYTHMS.length - 1, step: 1, value: 1, fmt: function (k) { return RHYTHMS[k][0]; } },
        { k: "shift", label: "Start it this many sixteenths later", min: 0, max: 15, step: 1, value: 0 },
        { k: "bpm", label: "Tempo (beats to the minute)", min: 70, max: 170, step: 5, value: 120 },
      ],
      buttons: [
        { label: "Play two bars", act: function (s, v) { s.sound = rhythmSound(rotated(RHYTHMS[v.which][1], v.shift), v.bpm); } },
      ],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        var p = rotated(RHYTHMS[v.which][1], v.shift), idx = [], xs = [], ys = [], all = [], i;
        for (i = 0; i < 16; i++) { idx.push(i + 1); if (p.charAt(i) === "x") { xs.push(i + 1); ys.push(WEIGHTS[i] + 0.45); } }
        for (i = 0; i < 16; i++) all.push(syncopation(rotated(RHYTHMS[v.which][1], i)));
        s.p = p; s.index = all[v.shift]; s.all = all;
        var a = g[0].axes({ x: [0.3, 16.7], y: [0, 6.2], title: "The metre's weights, and where the notes fall", xlabel: "sixteenths of the bar", xticks: [1, 5, 9, 13], yticks: [1, 2, 3, 4, 5] });
        a.bars(idx, WEIGHTS, 0.7, { color: C.muted });
        a.dots(xs, ys, { color: C.idea, r: 6 });
        var top = Math.max.apply(null, all) + 1;
        var b = g[1].axes({ x: [-0.7, 15.7], y: [0, top], title: "Syncopation index at every starting point", xlabel: "sixteenths later", xticks: [0, 4, 8, 12], ylabel: "index" });
        b.bars(idx.map(function (k) { return k - 1; }), all, 0.7, { color: function (k) { return k === v.shift ? C.idea : C.muted; } });
      },
      readout: function (v, s) {
        var on = 0, n = 0, i;
        for (i = 0; i < 16; i++) if (s.p.charAt(i) === "x") { n++; if (i % 4 === 0) on++; }
        var least = Math.min.apply(null, s.all), most = Math.max.apply(null, s.all);
        return [["the rhythm, as placed", s.p],
                ["notes that fall on a beat", on + " of " + n],
                ["syncopation index", String(s.index)],
                ["over all sixteen positions", "from " + least + " to " + most],
                ["beat", fmt(60000 / v.bpm, 0) + " ms; a sixteenth " + fmt(15000 / v.bpm, 0) + " ms"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "The index adds up, for every note that is followed by a silent pulse stronger than itself, the difference of the two weights (Longuet-Higgins and Lee, 1984). The same five strokes can confirm the metre or fight it, depending only on where they start: sliding a rhythm is the cheapest way there is to make a new one. Push the tempo up and note the sixteenth's length; near 100 ms the pulses stop being countable."
    });
  };

  // ---- Part 12: stack a generator ----------------------------------------------------------------------------
  function stackNotes(n, cents) {              // n notes a generator apart, folded into one octave, sorted (in cents)
    var out = [], k;
    for (k = 0; k < n; k++) out.push(((k * cents) % 1200 + 1200) % 1200);
    out.sort(function (a, b) { return a - b; });
    return out;
  }
  function stackGaps(notes) {
    var g = [], k;
    for (k = 0; k < notes.length; k++) g.push((k + 1 < notes.length ? notes[k + 1] : notes[0] + 1200) - notes[k]);
    return g;
  }
  function gapKinds(gaps) {                    // the different sizes of step, largest first
    var sorted = gaps.slice().sort(function (a, b) { return b - a; }), kinds = [], k;
    for (k = 0; k < sorted.length; k++) if (!kinds.length || Math.abs(kinds[kinds.length - 1] - sorted[k]) > 0.05) kinds.push(sorted[k]);
    return kinds;
  }
  function scaleSound(notes) {
    var rate = 44100, step = 0.28, out = new Float32Array(Math.floor(((notes.length + 1) * step + 0.9) * rate)), i, n, h;
    var all = notes.concat([1200]);
    for (i = 0; i < all.length; i++) {
      var hz = 261.63 * Math.pow(2, all[i] / 1200), start = Math.floor(i * step * rate), len = Math.floor(0.8 * rate);
      for (n = 0; n < len && start + n < out.length; n++) {
        var t = n / rate, y = 0;
        for (h = 1; h <= 6; h++) y += Math.sin(2 * Math.PI * hz * h * t) / (h * h) * Math.exp(-t * (2.5 + 0.9 * h));
        out[start + n] += 0.3 * y * Math.min(1, t / 0.004);
      }
    }
    return play(out, rate);
  }

  W.scale = function (el) {
    QB.widget(el, {
      title: "Stack a fifth, and watch the steps",
      sub: "Notes one generator apart, folded into an octave. Left: the notes round the octave (once round is 1200 cents). Right: the steps between neighbours, in order round the circle. Count the sizes of step: there are never more than three, and at some numbers of notes only two.",
      panels: 2, height: 300,
      controls: [
        { k: "gen", label: "The generator (cents; a pure fifth is 702)", min: 680, max: 719.5, step: 0.5, value: 702 },
        { k: "n", label: "Notes in the stack", min: 2, max: 24, step: 1, value: 7 },
      ],
      buttons: [
        { label: "Play the scale", act: function (s) { s.sound = scaleSound(s.notes); } },
      ],
      init: function (s) { s.sound = null; s.notes = []; },
      draw: function (g, v, s) {
        var gen = v.gen === 702 ? 701.955 : v.gen, notes = stackNotes(v.n, gen), gaps = stackGaps(notes), kinds = gapKinds(gaps), i;
        s.notes = notes; s.gaps = gaps; s.kinds = kinds;
        var a = g[0].axes({ x: [-1.35, 1.35], y: [-1.35, 1.35], title: "The notes, round the octave", xticks: [], yticks: [] });
        var cx = [], cy = [], px = [], py = [];
        for (i = 0; i <= 96; i++) { cx.push(Math.sin(2 * Math.PI * i / 96)); cy.push(Math.cos(2 * Math.PI * i / 96)); }
        a.line(cx, cy, { color: C.muted, width: 1 });
        for (i = 0; i < notes.length; i++) { px.push(Math.sin(2 * Math.PI * notes[i] / 1200)); py.push(Math.cos(2 * Math.PI * notes[i] / 1200)); }
        a.dots(px, py, { color: kinds.length === 2 ? C.idea : C.implied, r: 5 });
        var idx = [];
        for (i = 0; i < gaps.length; i++) idx.push(i + 1);
        var b = g[1].axes({ x: [0.3, gaps.length + 0.7], y: [0, Math.max.apply(null, gaps) * 1.15], title: "The steps between neighbours (cents)", xlabel: "step", xticks: [], ylabel: "cents" });
        b.bars(idx, gaps, 0.7, { color: function (k) { return Math.abs(gaps[k] - kinds[0]) < 0.05 ? C.idea : (kinds.length > 1 && Math.abs(gaps[k] - kinds[1]) < 0.05 ? C.implied : C.loss); } });
      },
      readout: function (v, s) {
        var words = ["", "one size", "two sizes", "three sizes"];
        return [["notes", String(v.n)],
                ["sizes of step", words[Math.min(s.kinds.length, 3)] + ":  " + s.kinds.map(function (k) { return fmt(k, 1); }).join(", ") + " cents"],
                ["largest over smallest", s.kinds[s.kinds.length - 1] < 0.05 ? "notes coincide" : fmt(s.kinds[0] / s.kinds[s.kinds.length - 1], 2)],
                ["names for this size", v.n === 5 ? "pentatonic" : v.n === 7 ? "diatonic" : v.n === 12 ? "chromatic" : "-"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "With a pure fifth, two sizes of step occur at 2, 3, 5, 7, 12, 17, 29, 41 and 53 notes: the denominators that come out of the continued fraction for the fifth's size. Five, seven and twelve are the pentatonic, diatonic and chromatic scales. Narrow the generator to 697 cents (meantone) and the list becomes 5, 7, 12, 19, 31; widen it and 17 and 22 appear. The three-gap theorem says that no setting will ever show four sizes."
    });
  };
  // ---- Part 13: one chord, moved and spread ----------------------------------------------------------------
  var KINDS13 = [["major", [0, 4, 7]], ["minor", [0, 3, 7]], ["diminished", [0, 3, 6]], ["augmented", [0, 4, 8]], ["dominant seventh", [0, 4, 7, 10]], ["major seventh", [0, 4, 7, 11]], ["minor seventh", [0, 3, 7, 10]]];
  var SPREADS13 = ["close", "open", "as the harmonic series"];
  var NAMES13 = ["C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"];
  var SUPPORT13 = { 0: 10, 7: 5, 4: 3, 10: 2, 2: 1 };
  function hz13(m) { return 440 * Math.pow(2, (m - 69) / 12); }
  function voicing13(bass, offs, spread) {
    var out = [], i;
    if (spread === 0) for (i = 0; i < offs.length; i++) out.push(bass + offs[i]);
    else if (spread === 1) { out = [bass, bass + offs[2], bass + 12 + offs[1]]; if (offs.length > 3) out.push(bass + 12 + offs[3]); }
    else { out = [bass, bass + 12, bass + 12 + offs[2], bass + 24 + offs[1]]; if (offs.length > 3) out.push(bass + 24 + offs[3]); }
    return out;
  }
  // Part 5's roughness (Plomp and Levelt's curve as fitted by Sethares), over every pair of partials of every note
  function rough13(notes) {
    var f = [], a = [], i, j, k, total = 0;
    for (i = 0; i < notes.length; i++) for (k = 1; k <= 7; k++) { f.push(hz13(notes[i]) * k); a.push(Math.pow(0.88, k - 1)); }
    for (i = 0; i < f.length; i++) for (j = i + 1; j < f.length; j++) {
      var lo = Math.min(f[i], f[j]), sc = 0.24 / (0.0207 * lo + 18.96), d = Math.abs(f[i] - f[j]);
      total += Math.min(a[i], a[j]) * (Math.exp(-3.5 * sc * d) - Math.exp(-5.75 * sc * d));
    }
    return total;
  }
  function saliences13(notes) {
    var out = [], r, i, seen = {};
    for (r = 0; r < 12; r++) out.push(0);
    for (i = 0; i < notes.length; i++) {
      var pc = ((notes[i] % 12) + 12) % 12;
      if (seen[pc]) continue;
      seen[pc] = true;
      for (r = 0; r < 12; r++) out[r] += SUPPORT13[(pc - r + 12) % 12] || 0;
    }
    return out;
  }
  function chordSound(notes) {
    var rate = 44100, len = Math.floor(2.2 * rate), out = new Float32Array(len), i, n, h;
    for (i = 0; i < notes.length; i++) {
      var f = hz13(notes[i]), start = Math.floor(0.015 * i * rate);
      for (n = 0; start + n < len; n++) {
        var t = n / rate, y = 0;
        for (h = 1; h <= 7; h++) y += Math.sin(2 * Math.PI * f * h * t) * Math.pow(0.88, h - 1) / h * Math.exp(-t * (0.9 + 0.35 * h));
        out[start + n] += 0.16 * y * Math.min(1, t / 0.004);
      }
    }
    return play(out, rate);
  }

  W.chord = function (el) {
    QB.widget(el, {
      title: "One chord, moved and spread",
      sub: "Choose a kind of chord, how low its bottom note is, and how its notes are spaced. Left: the roughness of that spacing with its bottom note on every key (Part 5's model); the dot is where you are. Right: the root model's votes for each of the twelve notes. Slide the chord down and hear the mud arrive; spread it and hear it clear.",
      panels: 2, height: 300,
      controls: [
        { k: "kind", label: "The kind of chord (0 major, 1 minor, 2 diminished, 3 augmented, 4 dominant seventh, 5 major seventh, 6 minor seventh)", min: 0, max: 6, step: 1, value: 0 },
        { k: "bass", label: "The bottom note (36 is the C two octaves below middle C; 60 is middle C)", min: 24, max: 72, step: 1, value: 48 },
        { k: "spread", label: "The spacing (0 close, 1 open, 2 as the harmonic series)", min: 0, max: 2, step: 1, value: 0 },
      ],
      buttons: [
        { label: "Play the chord", act: function (s) { s.sound = chordSound(s.notes); } },
      ],
      init: function (s) { s.sound = null; s.notes = [48, 52, 55]; },
      draw: function (g, v, s) {
        var offs = KINDS13[v.kind][1], notes = voicing13(v.bass, offs, v.spread), xs = [], ys = [], m, top = 0;
        s.notes = notes; s.rough = rough13(notes); s.sal = saliences13(notes);
        for (m = 24; m <= 72; m++) { xs.push(m); ys.push(rough13(voicing13(m, offs, v.spread))); top = Math.max(top, ys[ys.length - 1]); }
        var a = g[0].axes({ x: [24, 72], y: [0, top * 1.08], title: "Roughness of this spacing, by where it is put", xlabel: "the bottom note (key number)", ylabel: "roughness", xticks: [24, 36, 48, 60, 72] });
        a.line(xs, ys, { color: C.idea, width: 2 });
        a.dots([v.bass], [s.rough], { color: C.loss, r: 6 });
        var idx = [], best = Math.max.apply(null, s.sal), r;
        for (r = 0; r < 12; r++) idx.push(r + 1);
        var b = g[1].axes({ x: [0.3, 12.7], y: [0, Math.max(best, 20) * 1.1], title: "Votes for each note as the root", xlabel: "C  D♭  D  E♭  E  F  F♯  G  A♭  A  B♭  B", xticks: [], ylabel: "votes" });
        b.bars(idx, s.sal, 0.7, { color: function (k) { return s.sal[k] === best ? C.idea : C.muted; } });
      },
      readout: function (v, s) {
        var best = Math.max.apply(null, s.sal), roots = [], sum = 0, r;
        for (r = 0; r < 12; r++) { sum += s.sal[r]; if (s.sal[r] === best) roots.push(NAMES13[r]); }
        return [["chord", NAMES13[((v.bass % 12) + 12) % 12] + " " + KINDS13[v.kind][0] + ", " + SPREADS13[v.spread]],
                ["notes", s.notes.map(function (m) { return NAMES13[((m % 12) + 12) % 12] + (Math.floor(m / 12) - 1); }).join("  ")],
                ["roughness", fmt(s.rough, 2)],
                ["the model's root", roots.length > 2 ? "a tie of " + roots.length : roots.join(" or ")],
                ["root ambiguity", fmt(Math.sqrt(sum / best), 2)],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "A major triad close together on middle C has a roughness of about 1.1; two octaves lower the same three notes score about 3.9, and spread as a fifth and a tenth they come back to about 2.6. The root model gives C eighteen votes for C, E, G and a four-way tie for a diminished triad, one of the four being a note that is not in the chord. Try the minor seventh: the model prefers the note a minor third above the root you chose, because the same four notes are a major chord with an added sixth."
    });
  };
  // ---- Part 14: notes from an urn, and the leap rule ---------------------------------------------------------
  var MAJOR14 = [0, 2, 4, 5, 7, 9, 11];
  function rng14(seed) { var s = seed >>> 0; return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
  // n notes on the steps 0..span of a scale: each drawn with a preference for the middle (crowd) and for the last note (near)
  function draw14(n, span, crowd, near, rnd) {
    var out = [], mid = span / 2, k, i;
    for (i = 0; i < n; i++) {
      var w = [], total = 0;
      for (k = 0; k <= span; k++) {
        var z = (k - mid) / (span / 2), v = Math.exp(-2 * crowd * z * z);
        if (i > 0) v *= Math.exp(-near * Math.abs(k - out[i - 1]));
        w.push(v); total += v;
      }
      var u = rnd() * total;
      for (k = 0; k <= span; k++) { u -= w[k]; if (u <= 0) break; }
      out.push(Math.min(k, span));
    }
    return out;
  }
  // after each leap (two scale steps or more): did the next move turn back?  Sorted by where the leap landed.
  function leaps14(notes, span) {
    var mid = span / 2, r = { away: [0, 0], across: [0, 0], toward: [0, 0], all: [0, 0] }, i;
    for (i = 0; i + 2 < notes.length; i++) {
      var a = notes[i], b = notes[i + 1], c = notes[i + 2];
      if (Math.abs(b - a) < 2 || c === b) continue;
      var kind = (a - mid) * (b - mid) < 0 ? "across" : (Math.abs(b - mid) > Math.abs(a - mid) ? "away" : "toward");
      var back = (c - b) * (b - a) < 0 ? 1 : 0;
      r[kind][0] += back; r[kind][1] += 1; r.all[0] += back; r.all[1] += 1;
    }
    return r;
  }
  function melodySound(steps) {
    var rate = 44100, step = 0.26, out = new Float32Array(Math.floor((steps.length * step + 0.9) * rate)), i, n, h;
    for (i = 0; i < steps.length; i++) {
      var semis = 12 * Math.floor(steps[i] / 7) + MAJOR14[steps[i] % 7], hz = 261.63 * Math.pow(2, semis / 12), start = Math.floor(i * step * rate), len = Math.floor(0.7 * rate);
      for (n = 0; n < len && start + n < out.length; n++) {
        var t = n / rate, y = 0;
        for (h = 1; h <= 6; h++) y += Math.sin(2 * Math.PI * hz * h * t) / (h * h) * Math.exp(-t * (2.5 + 0.9 * h));
        out[start + n] += 0.3 * y * Math.min(1, t / 0.004);
      }
    }
    return play(out, rate);
  }

  W.melody = function (el) {
    QB.widget(el, {
      title: "Notes from an urn, and the leap rule",
      sub: "A melody made by chance on the white keys. Choose how wide its range is, how much its notes crowd the middle, and how much each note likes to stay near the last one. Left: twenty-four of its notes. Right: after a leap, how often the next move turns back, sorted by where the leap landed (counted over six thousand notes). No setting makes a leap toward the middle turn back as often as a leap away from it.",
      panels: 2, height: 300,
      controls: [
        { k: "span", label: "The range, in steps of the scale (7 is an octave)", min: 4, max: 14, step: 1, value: 8 },
        { k: "crowd", label: "How much the notes crowd the middle of the range (0: every note as likely as another)", min: 0, max: 2, step: 0.1, value: 1 },
        { k: "near", label: "How much each note likes to be near the last one (0: no memory at all)", min: 0, max: 1.5, step: 0.1, value: 0 },
        { k: "seed", label: "Another draw", min: 1, max: 40, step: 1, value: 1 },
      ],
      buttons: [
        { label: "Play the melody", act: function (s) { s.sound = melodySound(s.notes); } },
      ],
      init: function (s) { s.sound = null; s.notes = []; },
      draw: function (g, v, s) {
        var notes = draw14(24, v.span, v.crowd, v.near, rng14(v.seed * 7919)), xs = [], i;
        var st = leaps14(draw14(6000, v.span, v.crowd, v.near, rng14(v.seed * 104729 + 1)), v.span);
        s.notes = notes; s.stats = st;
        for (i = 0; i < notes.length; i++) xs.push(i + 1);
        var a = g[0].axes({ x: [0, 25], y: [-0.5, v.span + 0.5], title: "Twenty-four notes", xlabel: "note", ylabel: "step of the scale", xticks: [1, 8, 16, 24] });
        a.line([0, 25], [v.span / 2, v.span / 2], { color: C.muted, width: 1 });
        a.line(xs, notes, { color: C.idea, width: 1.5 });
        a.dots(xs, notes, { color: C.idea, r: 4 });
        var kinds = ["away", "across", "toward"], vals = [];
        for (i = 0; i < 3; i++) vals.push(st[kinds[i]][1] ? 100 * st[kinds[i]][0] / st[kinds[i]][1] : 0);
        s.vals = vals;
        var b = g[1].axes({ x: [0.3, 3.7], y: [0, 100], title: "Leaps that turn back, in a hundred", xlabel: "away from the middle      across it      toward it", xticks: [], ylabel: "in a hundred" });
        b.bars([1, 2, 3], vals, 0.6, { color: function (k) { return k === 2 ? C.implied : C.idea; } });
      },
      readout: function (v, s) {
        var all = s.stats.all;
        return [["all leaps that turn back", all[1] ? fmt(100 * all[0] / all[1], 0) + " in a hundred" : "-"],
                ["leaps away from the middle", fmt(s.vals[0], 0) + " in a hundred"],
                ["leaps across the middle", fmt(s.vals[1], 0) + " in a hundred"],
                ["leaps toward the middle", fmt(s.vals[2], 0) + " in a hundred"],
                ["leaps counted", String(all[1])],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "With no memory and notes that crowd the middle, about eight leaps in ten turn back, though nothing in the urn knows what a leap is. Set the crowding to zero: the notes are now equally likely, and still most leaps turn back, because a leap away from the middle lands near an edge. Give the notes a liking for their neighbours and the melody begins to sound like a tune; the three bars keep their order. In the fifty-four tunes of the film the figures are 75, 78 and 20."
    });
  };
})();
