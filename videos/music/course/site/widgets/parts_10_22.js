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
  // ---- Part 15: a key finder you can watch ---------------------------------------------------------------------
  var TUNES15 = [{"name": "the Tune", "mode": "major", "p": [0, 0, 7, 7, 9, 9, 7, 5, 5, 4, 4, 2, 2, 0, 7, 7, 5, 5, 4, 4, 2, 7, 7, 5], "b": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0]}, {"name": "Frère Jacques", "mode": "major", "p": [0, 2, 4, 0, 0, 2, 4, 0, 4, 5, 7, 4, 5, 7, 7, 9, 7, 5, 4, 0, 7, 9, 7, 5], "b": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5]}, {"name": "Ode to Joy", "mode": "major", "p": [4, 4, 5, 7, 7, 5, 4, 2, 0, 0, 2, 4, 4, 2, 2, 4, 4, 5, 7, 7, 5, 4, 2, 0], "b": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]}, {"name": "Greensleeves", "mode": "minor", "p": [0, 3, 5, 7, 9, 7, 5, 2, -2, 0, 2, 3, 0, 0, -1, 0, 2, -1, -5, 0, 3, 5, 7, 9], "b": [1.0, 2.0, 1.0, 1.5, 0.5, 1.0, 2.0, 1.0, 1.5, 0.5, 1.0, 2.0, 1.0, 1.5, 0.5, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.5, 0.5]}, {"name": "Happy Birthday to You", "mode": "major", "p": [-5, -5, -3, -5, 0, -1, -5, -5, -3, -5, 2, 0, -5, -5, 7, 4, 0, -1, -3, 5, 5, 4, 0, 2], "b": [0.75, 0.25, 1.0, 1.0, 1.0, 2.0, 0.75, 0.25, 1.0, 1.0, 1.0, 2.0, 0.75, 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75, 0.25, 1.0, 1.0, 1.0]}, {"name": "Amazing Grace", "mode": "major", "p": [-5, 0, 4, 0, 4, 2, 0, -3, -5, -5, 0, 4, 0, 4, 2, 4, 7, 4, 7, 7, 4, 0, 4, 2], "b": [1.0, 2.0, 0.5, 0.5, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 0.5, 0.5, 2.0, 0.5, 0.5, 3.0, 0.5, 0.5, 2.0, 0.5, 0.5, 2.0, 1.0]}, {"name": "Drunken Sailor", "mode": "minor", "p": [7, 7, 7, 7, 7, 7, 7, 0, 3, 7, 5, 5, 5, 5, 5, 5, 5, -2, 2, 5, 7, 7, 7, 7], "b": [1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0]}];
  var KK15 = [[6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88], [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]];
  var TP15 = [[0.748, 0.060, 0.488, 0.082, 0.670, 0.460, 0.096, 0.715, 0.104, 0.366, 0.057, 0.400], [0.712, 0.084, 0.474, 0.618, 0.049, 0.460, 0.105, 0.747, 0.404, 0.067, 0.133, 0.330]];
  var NAMES15 = ["C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"];
  function corr15(a, b) {
    var n = a.length, ma = 0, mb = 0, i, sab = 0, saa = 0, sbb = 0;
    for (i = 0; i < n; i++) { ma += a[i] / n; mb += b[i] / n; }
    for (i = 0; i < n; i++) { sab += (a[i] - ma) * (b[i] - mb); saa += (a[i] - ma) * (a[i] - ma); sbb += (b[i] - mb) * (b[i] - mb); }
    return saa > 0 && sbb > 0 ? sab / Math.sqrt(saa * sbb) : 0;
  }
  // the share of time on each of the twelve notes in the first n notes of a tune, moved up by `shift` semitones
  function dist15(tune, n, shift) {
    var d = [], i, total = 0;
    for (i = 0; i < 12; i++) d.push(0);
    for (i = 0; i < Math.min(n, tune.p.length); i++) { d[(((tune.p[i] + shift) % 12) + 12) % 12] += tune.b[i]; total += tune.b[i]; }
    for (i = 0; i < 12; i++) d[i] /= Math.max(total, 1e-9);
    return d;
  }
  // the correlation of the notes with each of the 24 keys' profiles: 12 major, then 12 minor
  function scores15(d, prof) {
    var out = [], mode, t, k;
    for (mode = 0; mode < 2; mode++) for (t = 0; t < 12; t++) {
      var p = [];
      for (k = 0; k < 12; k++) p.push(prof[mode][(k - t + 12) % 12]);
      out.push(corr15(d, p));
    }
    return out;
  }
  function tuneSound15(tune, n, shift) {
    var rate = 44100, beat = 0.34, total = 0, i, k, h;
    for (i = 0; i < Math.min(n, tune.p.length); i++) total += tune.b[i];
    var out = new Float32Array(Math.floor((total * beat + 0.9) * rate)), t0 = 0;
    for (i = 0; i < Math.min(n, tune.p.length); i++) {
      var hz = 261.63 * Math.pow(2, (tune.p[i] + shift) / 12), start = Math.floor(t0 * rate), len = Math.floor((tune.b[i] * beat + 0.5) * rate);
      for (k = 0; k < len && start + k < out.length; k++) {
        var t = k / rate, y = 0;
        for (h = 1; h <= 6; h++) y += Math.sin(2 * Math.PI * hz * h * t) / (h * h) * Math.exp(-t * (2.5 + 0.9 * h));
        out[start + k] += 0.3 * y * Math.min(1, t / 0.004);
      }
      t0 += tune.b[i] * beat;
    }
    return play(out, rate);
  }

  W.key = function (el) {
    QB.widget(el, {
      title: "A key finder you can watch",
      sub: "Choose a tune, move it to any key, and let the key finder hear its first few notes. Left: how much of the time each of the twelve notes has sounded. Right: how well that matches each of the 24 keys (twelve major, then twelve minor); the tallest bar is the key finder's answer. Add notes one at a time and watch it change its mind.",
      panels: 2, height: 300,
      controls: [
        { k: "tune", label: "The tune (0 the Tune, 1 Frère Jacques, 2 Ode to Joy, 3 Greensleeves, 4 Happy Birthday, 5 Amazing Grace, 6 Drunken Sailor)", min: 0, max: 6, step: 1, value: 0 },
        { k: "n", label: "Notes heard so far", min: 1, max: 24, step: 1, value: 7 },
        { k: "shift", label: "Moved up by so many semitones (0 puts the home note on C)", min: 0, max: 11, step: 1, value: 0 },
        { k: "prof", label: "Profiles (0: listeners' ratings, 1982; 1: counts from music, 2007)", min: 0, max: 1, step: 1, value: 1 },
      ],
      buttons: [
        { label: "Play the notes heard", act: function (s, v) { s.sound = tuneSound15(TUNES15[s.tune], s.n, s.shift); } },
      ],
      init: function (s) { s.sound = null; s.tune = 0; s.n = 7; s.shift = 0; },
      draw: function (g, v, s) {
        var tune = TUNES15[v.tune], d = dist15(tune, v.n, v.shift), sc = scores15(d, v.prof ? TP15 : KK15), idx = [], i, best = 0;
        s.tune = v.tune; s.n = v.n; s.shift = v.shift; s.scores = sc;
        for (i = 0; i < 24; i++) if (sc[i] > sc[best]) best = i;
        s.best = best;
        var second = best === 0 ? 1 : 0;
        for (i = 0; i < 24; i++) if (i !== best && sc[i] > sc[second]) second = i;
        s.second = second;
        var twelve = [];
        for (i = 0; i < 12; i++) twelve.push(i + 1);
        var a = g[0].axes({ x: [0.3, 12.7], y: [0, Math.max.apply(null, d) * 1.15 + 0.01], title: "Time on each note so far", xlabel: "C  D♭  D  E♭  E  F  F♯  G  A♭  A  B♭  B", xticks: [], ylabel: "share" });
        a.bars(twelve, d, 0.7, { color: C.idea });
        for (i = 0; i < 24; i++) idx.push(i + 1);
        var b = g[1].axes({ x: [0.3, 24.7], y: [-1, 1], title: "Match with each key: 12 major, then 12 minor", xlabel: "C major ... B major   |   C minor ... B minor", xticks: [], ylabel: "correlation" });
        b.bars(idx, sc, 0.7, { color: function (k) { return k === best ? C.loss : (k < 12 ? C.idea : C.implied); } });
      },
      readout: function (v, s) {
        var name = function (k) { return NAMES15[k % 12] + (k < 12 ? " major" : " minor"); };
        var tune = TUNES15[v.tune], truth = NAMES15[v.shift % 12] + " " + tune.mode;
        return [["tune", tune.name + ", home note on " + NAMES15[v.shift % 12]],
                ["the key finder says", name(s.best) + "  (r = " + fmt(s.scores[s.best], 2) + ")"],
                ["its second choice", name(s.second) + "  (r = " + fmt(s.scores[s.second], 2) + ")"],
                ["is it right?", name(s.best) === truth ? "yes" : "no: the tune is in " + truth + (v.tune === 6 ? " (Dorian: a mode the key finder does not know)" : "")],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "With the listeners' ratings the key finder often names the key a fifth too high; with profiles counted from music it is right on nearly every whole tune. Watch the Tune: after its first phrase the answer is C major, at the start of the second phrase (two long Fs) it wavers toward F major, and it settles again by the end, because the Tune has no seventh degree to decide between the two. Drunken Sailor has D as its home and the notes of C major, and neither profile was built for that."
    });
  };
  // ---- Part 16: first species by hand, against Fux's cantus ------------------------------------------------------
  // Every one of the 152 lines that obey the twelve rules over Fux's cantus (counted and listed by Monochord), best
  // first by Fux's preferences, and for each note of each line which rules break if it moves one or two steps.
  var CP16 = {"cf":[62,65,64,62,67,65,69,67,65,64,62],"lines":[[74,69,71,74,71,74,72,76,77,73,74],[74,69,71,74,71,74,72,74,77,73,74],[74,72,76,77,76,74,72,71,72,73,74],[74,69,71,74,76,77,76,71,72,73,74],[74,69,71,74,71,74,72,76,74,73,74],[74,69,71,74,76,74,72,71,72,73,74],[74,72,67,69,71,74,72,76,77,73,74],[69,74,72,74,71,74,72,76,77,73,74],[74,72,79,77,76,77,76,71,72,73,74],[74,72,76,77,76,74,72,71,69,73,74],[74,69,71,74,76,74,72,76,77,73,74],[62,74,72,74,71,74,72,76,77,73,74],[74,72,79,77,76,74,72,71,72,73,74],[74,72,76,77,76,74,72,71,74,73,74],[74,72,67,69,71,74,72,74,77,73,74],[69,74,72,74,71,74,72,74,77,73,74],[69,74,72,77,76,74,72,71,72,73,74],[74,69,71,74,76,74,72,74,77,73,74],[62,69,67,69,71,74,72,76,77,73,74],[74,72,76,77,76,74,72,76,74,73,74],[74,72,67,69,71,74,72,76,74,73,74],[69,74,72,74,76,77,76,71,72,73,74],[69,74,72,74,71,74,72,76,74,73,74],[74,69,71,74,71,69,72,76,77,73,74],[62,74,72,74,71,74,72,74,77,73,74],[74,69,71,74,76,74,72,71,74,73,74],[74,69,71,74,76,74,72,71,69,73,74],[74,72,79,77,76,77,72,74,77,73,74],[62,74,72,77,76,74,72,71,72,73,74],[74,72,67,69,76,74,72,71,72,73,74],[69,74,72,74,76,74,72,71,72,73,74],[74,72,79,77,76,74,72,76,77,73,74],[62,74,72,74,76,77,76,71,72,73,74],[74,72,79,77,74,77,76,71,72,73,74],[62,74,72,74,71,74,72,76,74,73,74],[62,69,67,69,71,74,72,74,77,73,74],[74,72,79,77,76,74,72,71,69,73,74],[74,69,71,74,71,69,72,74,77,73,74],[74,72,79,77,76,74,72,71,74,73,74],[62,74,72,74,76,74,72,71,72,73,74],[74,69,71,74,71,72,77,76,74,73,74],[69,81,79,77,76,77,76,71,72,73,74],[74,72,79,77,76,74,72,74,77,73,74],[74,69,71,74,71,74,77,76,74,73,74],[62,69,67,69,71,74,72,76,74,73,74],[74,72,67,69,76,74,72,76,77,73,74],[62,69,67,71,76,74,72,71,72,73,74],[69,81,79,77,76,74,72,71,72,73,74],[74,81,79,77,76,77,76,71,72,73,74],[69,74,72,74,76,74,72,76,77,73,74],[69,74,72,77,76,74,72,71,74,73,74],[69,74,72,77,76,74,72,71,69,73,74],[74,69,71,74,71,69,72,76,74,73,74],[74,81,79,77,76,74,72,71,72,73,74],[74,72,79,77,76,74,72,76,74,73,74],[62,69,67,69,76,74,72,71,72,73,74],[62,74,72,77,76,74,72,71,69,73,74],[74,72,67,69,76,74,72,74,77,73,74],[62,69,67,71,76,74,72,76,77,73,74],[62,74,72,74,76,74,72,76,77,73,74],[69,74,72,74,76,74,72,74,77,73,74],[74,72,67,69,71,69,72,76,77,73,74],[74,72,79,77,74,77,72,74,77,73,74],[62,74,72,77,76,74,72,71,74,73,74],[69,74,72,77,76,74,72,76,74,73,74],[69,74,72,74,71,69,72,76,77,73,74],[74,72,67,69,76,74,72,71,69,73,74],[74,72,67,69,76,74,72,71,74,73,74],[69,74,72,71,76,74,72,71,72,73,74],[69,74,72,74,76,74,72,71,69,73,74],[69,74,72,74,76,74,72,71,74,73,74],[69,81,79,77,76,77,72,74,77,73,74],[62,74,72,74,71,69,72,76,77,73,74],[74,81,79,77,76,77,72,74,77,73,74],[69,81,79,77,76,74,72,76,77,73,74],[62,74,72,74,76,74,72,71,69,73,74],[62,74,72,74,76,74,72,74,77,73,74],[69,81,79,77,74,77,76,71,72,73,74],[62,69,67,69,76,74,72,76,77,73,74],[62,69,67,71,76,74,72,74,77,73,74],[62,74,72,77,76,74,72,76,74,73,74],[74,81,79,77,76,74,72,76,77,73,74],[62,74,72,74,76,74,72,71,74,73,74],[74,72,67,69,71,69,72,74,77,73,74],[74,72,67,69,71,74,77,76,74,73,74],[74,81,79,77,74,77,76,71,72,73,74],[62,74,72,71,76,74,72,71,72,73,74],[69,74,72,74,71,69,72,74,77,73,74],[69,74,72,74,71,74,77,76,74,73,74],[69,74,72,71,76,74,72,76,77,73,74],[74,72,67,69,71,72,77,76,74,73,74],[69,74,72,74,71,72,77,76,74,73,74],[69,81,79,77,76,74,72,71,69,73,74],[69,81,79,77,76,74,72,71,74,73,74],[74,81,79,77,76,74,72,71,69,73,74],[62,69,67,71,76,74,72,71,69,73,74],[62,69,67,71,76,74,72,71,74,73,74],[69,81,79,77,76,74,72,74,77,73,74],[74,69,71,74,71,69,77,76,74,73,74],[62,69,67,69,76,74,72,74,77,73,74],[62,74,72,74,71,69,72,74,77,73,74],[74,81,79,77,76,74,72,71,74,73,74],[74,81,79,77,76,74,72,74,77,73,74],[62,69,67,69,71,69,72,76,77,73,74],[74,72,67,69,71,69,72,76,74,73,74],[62,69,67,69,76,74,72,71,69,73,74],[62,69,67,69,76,74,72,71,74,73,74],[62,74,72,74,71,74,77,76,74,73,74],[69,74,72,74,71,69,72,76,74,73,74],[62,74,72,71,76,74,72,76,77,73,74],[69,74,72,71,76,74,72,74,77,73,74],[74,72,79,77,76,74,77,76,77,73,74],[62,69,67,71,83,81,77,76,77,73,74],[62,74,72,74,71,72,77,76,74,73,74],[69,81,79,77,76,74,72,76,74,73,74],[74,69,71,74,76,74,77,76,74,73,74],[62,74,72,74,71,69,72,76,74,73,74],[74,81,79,77,76,74,72,76,74,73,74],[62,69,67,69,71,69,72,71,72,73,74],[69,81,79,77,74,77,72,74,77,73,74],[69,74,72,71,76,74,72,71,69,73,74],[69,74,72,71,76,74,72,71,74,73,74],[62,74,72,71,76,74,72,74,77,73,74],[62,69,67,69,71,69,72,74,77,73,74],[74,81,79,77,74,77,72,74,77,73,74],[69,74,72,71,83,81,77,76,77,73,74],[62,69,67,69,71,72,77,76,74,73,74],[62,74,72,71,76,74,72,71,69,73,74],[62,69,67,69,71,74,77,76,74,73,74],[62,74,72,71,76,74,72,71,74,73,74],[74,72,79,77,76,74,77,76,74,73,74],[62,69,67,69,71,69,72,76,74,73,74],[62,69,67,71,83,81,77,76,74,73,74],[62,74,72,71,83,81,77,76,77,73,74],[74,72,67,69,71,69,77,76,74,73,74],[69,74,72,74,71,69,77,76,74,73,74],[62,74,72,74,71,69,77,76,74,73,74],[69,74,72,71,83,81,77,76,74,73,74],[74,72,67,69,76,74,77,76,74,73,74],[69,74,72,74,76,74,77,76,74,73,74],[62,69,67,69,71,69,72,71,69,73,74],[69,81,79,77,76,74,77,76,77,73,74],[74,81,79,77,76,74,77,76,77,73,74],[62,74,72,71,83,81,77,76,74,73,74],[62,74,72,74,76,74,77,76,74,73,74],[62,69,67,69,71,69,77,76,74,73,74],[62,69,67,71,76,74,77,76,74,73,74],[69,81,79,77,76,74,77,76,74,73,74],[62,69,67,69,76,74,77,76,74,73,74],[74,81,79,77,76,74,77,76,74,73,74],[69,74,72,71,76,74,77,76,74,73,74],[62,74,72,71,76,74,77,76,74,73,74]],"scores":[28.8,27.7,27.5,27.0,26.9,26.4,26.3,26.2,25.6,25.5,25.5,25.4,25.3,25.2,25.2,25.1,24.8,24.7,24.6,24.4,24.4,24.4,24.3,24.3,24.3,24.1,24.1,24.1,24.0,23.9,23.8,23.8,23.6,23.6,23.5,23.5,23.3,23.2,23.0,23.0,23.0,23.0,23.0,22.9,22.7,22.7,22.7,22.7,22.7,22.6,22.5,22.5,22.4,22.4,22.2,22.2,22.0,21.9,21.8,21.8,21.8,21.8,21.8,21.7,21.7,21.7,21.6,21.6,21.5,21.5,21.5,21.5,21.2,21.2,21.2,21.0,21.0,21.0,21.0,21.0,20.9,20.9,20.7,20.7,20.7,20.7,20.7,20.6,20.6,20.6,20.5,20.4,20.4,20.4,20.4,20.4,20.4,20.4,20.2,20.2,20.1,20.1,20.1,20.1,19.9,19.9,19.9,19.8,19.8,19.8,19.8,19.8,19.8,19.6,19.6,19.6,19.3,19.3,19.2,19.2,19.2,19.2,19.0,19.0,18.9,18.9,18.8,18.7,18.7,18.4,18.2,18.2,18.2,18.1,18.0,17.9,17.4,17.3,17.1,17.0,16.9,16.9,16.6,16.5,16.2,16.0,15.9,15.3,15.1,15.0,15.0,14.2],"masks":["2.3.3.842.148.101.81.30.100.181.100.181.80.1.101.940.108.101.1.80.81.80.101.940.108.101.81.a0.181.0.981.30.0.881.41.140.164.4.85.25.4.5.5.804","2.3.3.842.148.101.81.30.100.181.100.181.80.1.101.940.108.101.1.80.81.80.101.940.108.1.81.30.140.181.0.981.880.1.141.140.164.4.85.25.4.5.5.804","22.83.3.902.100.101.80.81.80.1.981.0.830.881.401.500.1.80.881.120.1.a0.81.900.8.81.81.20.128.1.81.30.0.81.0.101.34.84.85.25.4.5.5.804","2.3.3.842.148.101.81.30.100.181.100.181.180.1.181.840.1.80.881.30.820.881.1.100.100.1.8c0.41.168.101.81.30.100.181.100.101.34.84.85.25.4.5.5.804","2.3.803.42.148.101.81.30.100.181.100.181.80.1.901.140.108.101.1.80.81.80.901.140.108.1.81.8a0.881.880.101.100.1.20.881.0.24.4.85.25.204.5.805.4","2.3.803.42.148.101.81.30.100.181.100.181.80.1.981.40.801.880.1.130.1.a0.881.100.8.81.81.820.128.1.81.30.0.81.0.901.34.84.85.25.4.5.805.4","22.83.3.902.100.1.80.41.168.101.81.30.140.181.180.101.8.81.1.1b0.81.80.101.940.108.101.81.a0.181.0.981.30.0.881.41.140.164.4.85.25.4.5.5.804","42.3.2.3.1.b0.101.920.101.120.181.130.80.81.101.940.108.101.1.80.81.80.101.940.108.101.81.a0.181.0.981.30.0.881.41.140.164.4.85.25.4.5.5.804","22.83.3.102.140.1.80.1.800.981.541.540.120.181.d81.500.101.0.81.830.20.81.801.100.100.1.c0.841.168.101.81.30.100.181.100.101.34.84.85.25.4.5.5.4","22.83.3.902.100.101.80.81.80.1.981.0.830.881.401.500.1.80.881.120.1.a0.81.900.8.81.81.120.28.81.81.100.168.141.81.0.4.4.185.65.4.5.5.804","2.3.3.842.148.101.81.30.100.181.100.181.80.1.181.840.1.80.801.130.1.a0.81.900.108.101.81.a0.181.0.981.30.800.881.41.140.164.4.85.25.4.5.5.804","442.443.43.42.141.1e0.141.970.101.120.181.130.80.81.101.940.108.101.1.80.81.80.101.940.108.101.81.a0.181.0.981.30.0.881.41.140.164.4.85.25.4.5.5.804","22.83.3.102.140.1.80.1.0.981.541.540.120.181.d81.500.1.80.81.920.1.a0.81.100.8.81.81.20.128.1.81.30.0.81.0.101.34.84.85.25.4.5.5.4","22.83.3.902.100.101.80.81.80.1.981.0.830.881.401.500.1.80.881.120.1.a0.81.900.8.81.81.120.128.1.81.80.81.0.101.940.24.4.85.25.4.5.5.804","22.83.3.902.100.1.80.41.168.101.81.30.140.181.180.101.8.81.1.1b0.81.80.101.940.108.1.81.30.140.181.0.981.880.1.141.140.164.4.85.25.4.5.5.804","42.3.2.3.1.b0.101.920.101.120.181.130.80.81.101.940.108.101.1.80.81.80.101.940.108.1.81.30.140.181.0.981.880.1.141.140.164.4.85.25.4.5.5.804","42.3.2.3.1.b0.101.920.101.160.181.100.0.881.501.540.101.180.981.120.1.a0.81.900.8.81.81.20.128.1.81.30.0.81.0.101.34.84.85.25.4.5.5.804","2.3.3.842.148.101.81.30.100.181.100.181.80.1.181.840.1.80.801.130.1.a0.81.800.108.1.81.30.140.181.0.981.80.801.141.140.164.4.85.25.4.5.5.804","442.443.3.2.38.181.141.160.128.101.181.130.140.81.80.1.8.81.1.1b0.81.80.101.940.108.101.81.a0.181.0.981.30.0.881.41.140.164.4.85.25.4.5.5.804","22.83.3.902.100.101.80.81.80.1.981.0.830.881.401.500.1.80.881.120.1.a0.81.900.108.1.81.a0.81.80.901.100.1.20.81.800.24.4.85.25.204.5.5.804","22.83.803.102.100.1.80.841.168.101.81.30.140.181.180.101.8.81.1.1b0.81.80.901.140.108.1.81.8a0.881.880.101.100.1.20.881.0.24.4.85.25.204.5.805.4","42.3.2.3.1.b0.101.920.101.120.181.130.100.81.81.800.1.80.881.30.820.881.1.100.100.1.8c0.41.168.101.81.30.100.181.100.101.34.84.85.25.4.5.5.804","42.3.2.3.1.b0.901.120.101.120.181.930.80.81.901.140.108.101.1.80.81.80.901.140.108.1.81.8a0.881.880.101.100.1.20.881.0.24.4.85.25.204.5.805.4","2.3.3.842.148.101.81.30.100.181.100.181.80.1.101.940.8.181.1.180.168.101.81.80.188.101.101.1a0.181.0.981.30.0.881.41.140.164.4.85.25.4.5.5.804","442.443.43.42.141.1e0.141.970.101.120.181.130.80.81.101.940.108.101.1.80.81.80.101.940.108.1.81.30.140.181.0.981.880.1.141.140.164.4.85.25.4.5.5.804","2.3.803.42.148.101.81.30.100.181.100.181.80.1.981.40.801.880.1.130.1.a0.881.100.8.81.81.920.128.1.81.80.81.0.901.140.24.4.85.25.4.5.805.4","2.3.803.42.148.101.81.30.100.181.100.181.80.1.981.40.801.880.1.130.1.a0.881.100.8.81.81.920.28.81.81.100.168.141.81.0.4.4.185.65.4.5.805.4","22.83.3.102.140.1.80.1.800.981.541.540.120.181.d81.500.101.0.81.830.0.81.801.140.148.141.81.30.140.181.100.181.80.1.941.140.164.4.85.25.4.5.5.4","442.443.43.42.141.1e0.141.970.101.160.181.100.0.881.501.540.101.180.981.120.1.a0.81.900.8.81.81.20.128.1.81.30.0.81.0.101.34.84.85.25.4.5.5.804","22.83.803.102.100.1.80.841.168.101.81.30.140.1c1.100.101.801.9b0.101.160.101.1a0.981.100.8.81.81.820.128.1.81.30.0.81.0.901.34.84.85.25.4.5.805.4","42.3.2.3.1.b0.901.120.101.120.181.930.0.81.881.0.801.880.1.130.1.a0.881.100.8.81.81.820.128.1.81.30.0.81.0.901.34.84.85.25.4.5.805.4","22.83.3.102.140.1.80.1.800.981.541.540.120.181.d81.500.1.80.81.920.1.a0.81.100.108.101.81.a0.181.0.181.830.0.81.841.140.164.4.85.25.4.5.5.4","442.443.43.42.141.1e0.141.970.101.120.181.130.100.81.81.800.1.80.881.30.820.881.1.100.100.1.8c0.41.168.101.81.30.100.181.100.101.34.84.85.25.4.5.5.804","22.83.3.102.140.1.80.1.800.981.541.540.1a0.101.d81.500.140.101.0.81.a0.81.901.100.100.1.c0.841.168.101.81.30.100.181.100.101.34.84.85.25.4.5.5.4","442.443.43.42.141.1e0.941.170.101.120.181.930.80.81.901.140.108.101.1.80.81.80.901.140.108.1.81.8a0.881.880.101.100.1.20.881.0.24.4.85.25.204.5.805.4","442.443.3.2.38.181.141.160.128.101.181.130.140.81.80.1.8.81.1.1b0.81.80.101.940.108.1.81.30.140.181.0.981.880.1.141.140.164.4.85.25.4.5.5.804","22.83.3.102.140.1.80.1.0.981.541.540.120.181.d81.500.1.80.81.920.1.a0.81.100.8.81.81.120.28.81.81.100.168.141.81.0.4.4.185.65.4.5.5.4","2.3.3.842.148.101.81.30.100.181.100.181.80.1.101.940.8.181.1.180.168.101.81.80.188.1.181.30.140.181.0.981.880.1.141.140.164.4.85.25.4.5.5.804","22.83.3.102.140.1.80.1.0.981.541.540.120.181.d81.500.1.80.81.920.1.a0.81.100.8.81.81.120.128.1.81.80.81.0.101.140.24.4.85.25.4.5.5.4","442.443.43.42.141.1e0.941.170.101.120.181.930.0.81.881.0.801.880.1.130.1.a0.881.100.8.81.81.820.128.1.81.30.0.81.0.901.34.84.85.25.4.5.805.4","2.3.3.842.148.101.81.30.100.181.100.181.80.1.101.940.108.101.81.b0.0.c1.0.101.1.8b0.101.160.101.1a0.981.100.1.20.81.800.24.4.85.25.204.5.5.804","42.43.42.43.120.9c1.541.570.120.181.d81.540.20.81.481.c00.101.0.81.30.20.81.1.900.100.1.c0.41.168.101.81.30.100.181.100.101.34.84.85.25.4.5.5.4","22.83.3.102.140.1.80.1.800.981.541.540.120.181.d81.500.1.80.81.920.1.a0.81.0.108.1.81.30.140.181.0.181.80.1.941.140.164.4.85.25.4.5.5.4","2.3.3.842.148.101.81.30.100.181.100.181.80.1.101.940.108.101.1.80.c1.0.101.9c0.81.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","442.443.3.2.38.181.141.160.128.101.181.130.140.81.80.1.8.81.1.1b0.81.80.901.140.108.1.81.8a0.881.880.101.100.1.20.881.0.24.4.85.25.204.5.805.4","22.83.3.902.100.1.80.41.168.101.81.30.140.1c1.100.101.1.1b0.901.160.101.1a0.181.900.108.101.81.a0.181.0.981.30.800.881.41.140.164.4.85.25.4.5.5.804","442.443.3.2.38.181.141.160.128.141.181.180.c1.0.101.100.801.8a0.141.120.101.1a0.981.100.8.81.81.820.128.1.81.30.0.81.0.901.34.84.85.25.4.5.805.4","42.43.42.43.120.9c1.541.570.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.100.8.81.81.20.128.1.81.30.0.81.0.101.34.84.85.25.4.5.5.4","42.43.3.2.30.981.541.560.120.181.d81.540.20.81.481.c00.101.0.81.30.20.81.1.900.100.1.c0.41.168.101.81.30.100.181.100.101.34.84.85.25.4.5.5.4","42.3.2.3.1.b0.101.920.101.120.181.130.0.81.81.800.1.80.801.130.1.a0.81.900.108.101.81.a0.181.0.981.30.800.881.41.140.164.4.85.25.4.5.5.804","42.3.2.3.1.b0.101.920.101.160.181.100.0.881.501.540.101.180.981.120.1.a0.81.900.8.81.81.120.128.1.81.80.81.0.101.940.24.4.85.25.4.5.5.804","42.3.2.3.1.b0.101.920.101.160.181.100.0.881.501.540.101.180.981.120.1.a0.81.900.8.81.81.120.28.81.81.100.168.141.81.0.4.4.185.65.4.5.5.804","2.3.803.42.148.101.81.30.100.181.100.181.80.1.901.140.8.181.1.180.168.101.81.80.88.1.101.9a0.881.880.101.100.1.20.881.0.24.4.85.25.204.5.805.4","42.43.3.2.30.981.541.560.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.100.8.81.81.20.128.1.81.30.0.81.0.101.34.84.85.25.4.5.5.4","22.83.3.102.140.1.80.1.0.981.541.540.120.181.d81.500.1.80.81.920.1.a0.81.100.108.1.81.a0.81.80.101.900.1.20.81.0.24.4.85.25.204.5.5.4","442.443.3.2.38.181.141.160.128.101.181.130.40.c1.0.101.801.9b0.101.160.101.1a0.981.100.8.81.81.820.128.1.81.30.0.81.0.901.34.84.85.25.4.5.805.4","442.443.43.42.141.1e0.141.970.101.160.181.100.0.881.501.540.101.180.981.120.1.a0.81.900.8.81.81.120.28.81.81.100.168.141.81.0.4.4.185.65.4.5.5.804","22.83.3.902.100.1.80.41.168.101.81.30.140.1c1.100.101.1.1b0.901.160.101.1a0.181.900.108.1.81.30.140.181.0.981.80.801.141.140.164.4.85.25.4.5.5.804","442.443.3.2.38.181.141.160.128.141.181.180.c1.0.101.100.1.a0.941.120.101.1a0.181.900.108.101.81.a0.181.0.981.30.800.881.41.140.164.4.85.25.4.5.5.804","442.443.43.42.141.1e0.141.970.101.120.181.130.0.81.81.800.1.80.801.130.1.a0.81.900.108.101.81.a0.181.0.981.30.800.881.41.140.164.4.85.25.4.5.5.804","42.3.2.3.1.b0.101.920.101.120.181.130.0.81.81.800.1.80.801.130.1.a0.81.800.108.1.81.30.140.181.0.981.80.801.141.140.164.4.85.25.4.5.5.804","22.83.3.902.100.1.80.41.168.101.81.30.140.181.180.101.8.81.1.130.168.101.81.80.188.101.101.1a0.181.0.981.30.0.881.41.140.164.4.85.25.4.5.5.804","22.83.3.102.140.1.80.1.800.981.541.540.1a0.101.d81.500.140.101.0.81.80.1.901.140.148.141.81.30.140.181.100.181.80.1.941.140.164.4.85.25.4.5.5.4","442.443.43.42.141.1e0.141.970.101.160.181.100.0.881.501.540.101.180.981.120.1.a0.81.900.8.81.81.120.128.1.81.80.81.0.101.940.24.4.85.25.4.5.5.804","42.3.2.3.1.b0.101.920.101.160.181.100.800.881.501.540.101.180.981.120.1.a0.81.900.108.1.81.a0.81.80.901.100.1.20.81.800.24.4.85.25.204.5.5.804","42.3.2.3.1.b0.101.920.101.120.181.130.80.81.101.940.8.181.1.180.168.101.81.80.188.101.101.1a0.181.0.981.30.0.881.41.140.164.4.85.25.4.5.5.804","22.83.803.102.100.1.80.841.168.101.81.30.140.1c1.100.101.801.9b0.101.160.101.1a0.981.100.8.81.81.920.28.81.81.100.168.141.81.0.4.4.185.65.4.5.805.4","22.83.803.102.100.1.80.841.168.101.81.30.140.1c1.100.101.801.9b0.101.160.101.1a0.981.100.8.81.81.920.128.1.81.80.81.0.901.140.24.4.85.25.4.5.805.4","42.3.2.3.1.b0.901.120.101.1a0.181.900.141.20.81.0.801.8a0.141.120.101.1a0.981.100.8.81.81.820.128.1.81.30.0.81.0.901.34.84.85.25.4.5.805.4","42.3.2.3.1.b0.901.120.101.120.181.930.0.81.881.0.801.880.1.130.1.a0.881.100.8.81.81.920.28.81.81.100.168.141.81.0.4.4.185.65.4.5.805.4","42.3.2.3.1.b0.901.120.101.120.181.930.0.81.881.0.801.880.1.130.1.a0.881.100.8.81.81.920.128.1.81.80.81.0.901.140.24.4.85.25.4.5.805.4","42.43.42.43.120.9c1.541.570.120.181.d81.540.20.81.481.c00.101.0.81.30.0.81.1.940.148.141.81.30.140.181.100.181.80.1.141.940.164.4.85.25.4.5.5.4","442.443.43.42.141.1e0.141.970.101.120.181.130.80.81.101.940.8.181.1.180.168.101.81.80.188.101.101.1a0.181.0.981.30.0.881.41.140.164.4.85.25.4.5.5.804","42.43.3.2.30.981.541.560.120.181.d81.540.20.81.481.c00.101.0.81.30.0.81.1.940.148.141.81.30.140.181.100.181.80.1.141.940.164.4.85.25.4.5.5.4","42.43.42.43.120.9c1.541.570.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.100.108.101.81.a0.181.0.181.30.0.81.41.940.164.4.85.25.4.5.5.4","442.443.43.42.141.1e0.941.170.101.120.181.930.0.81.881.0.801.880.1.130.1.a0.881.100.8.81.81.920.28.81.81.100.168.141.81.0.4.4.185.65.4.5.805.4","442.443.43.42.141.1e0.141.970.101.120.181.130.0.81.81.800.1.80.801.130.1.a0.81.800.108.1.81.30.140.181.0.981.80.801.141.140.164.4.85.25.4.5.5.804","42.43.42.43.120.9c1.541.570.120.181.d81.540.1a0.1.581.d00.140.101.0.81.a0.81.101.900.100.1.c0.41.168.101.81.30.100.181.100.101.34.84.85.25.4.5.5.4","442.443.3.2.38.181.141.160.128.101.181.130.40.c1.0.101.1.1b0.901.160.101.1a0.181.900.108.101.81.a0.181.0.981.30.800.881.41.140.164.4.85.25.4.5.5.804","442.443.3.2.38.181.141.160.128.141.181.180.c1.0.101.100.1.a0.941.120.101.1a0.181.900.108.1.81.30.140.181.0.981.80.801.141.140.164.4.85.25.4.5.5.804","442.443.43.42.141.1e0.141.970.101.160.181.100.800.881.501.540.101.180.981.120.1.a0.81.900.108.1.81.a0.81.80.901.100.1.20.81.800.24.4.85.25.204.5.5.804","42.43.3.2.30.981.541.560.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.100.108.101.81.a0.181.0.181.30.0.81.41.940.164.4.85.25.4.5.5.4","442.443.43.42.141.1e0.941.170.101.120.181.930.0.81.881.0.801.880.1.130.1.a0.881.100.8.81.81.920.128.1.81.80.81.0.901.140.24.4.85.25.4.5.805.4","22.83.3.902.100.1.80.41.168.101.81.30.140.181.180.101.8.81.1.130.168.101.81.80.188.1.181.30.140.181.0.981.880.1.141.140.164.4.85.25.4.5.5.804","22.83.3.902.100.1.80.41.168.101.81.30.140.181.180.101.108.181.1.1b0.c1.0.101.9c0.81.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","42.43.3.2.30.981.541.560.120.181.d81.540.1a0.1.581.d00.140.101.0.81.a0.81.101.900.100.1.c0.41.168.101.81.30.100.181.100.101.34.84.85.25.4.5.5.4","442.443.43.42.141.1e0.941.170.101.1a0.181.900.141.20.81.0.801.8a0.141.120.101.1a0.981.100.8.81.81.820.128.1.81.30.0.81.0.901.34.84.85.25.4.5.805.4","42.3.2.3.1.b0.101.920.101.120.181.130.80.81.101.940.8.181.1.180.168.101.81.80.188.1.181.30.140.181.0.981.880.1.141.140.164.4.85.25.4.5.5.804","42.3.2.3.1.b0.101.920.101.120.181.130.80.81.101.940.108.101.1.80.c1.0.101.9c0.81.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","42.3.2.3.1.b0.101.920.101.1a0.181.100.141.20.81.0.1.a0.941.120.101.1a0.181.900.108.101.81.a0.181.0.981.30.800.881.41.140.164.4.85.25.4.5.5.804","22.83.3.902.100.1.80.41.168.101.81.30.140.181.180.101.108.81.81.30.0.c1.0.101.1.8b0.101.160.101.1a0.981.100.1.20.81.800.24.4.85.25.204.5.5.804","42.3.2.3.1.b0.101.920.101.120.181.130.80.81.1.940.108.101.81.b0.0.c1.0.101.1.8b0.101.160.101.1a0.981.100.1.20.81.800.24.4.85.25.204.5.5.804","42.43.42.43.120.9c1.541.570.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.100.8.81.81.120.28.81.81.100.168.141.81.0.4.4.185.65.4.5.5.4","42.43.42.43.120.9c1.541.570.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.100.8.81.81.120.128.1.81.80.81.0.101.140.24.4.85.25.4.5.5.4","42.43.3.2.30.981.541.560.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.100.8.81.81.120.28.81.81.100.168.141.81.0.4.4.185.65.4.5.5.4","442.443.3.2.38.181.141.160.128.141.181.180.c1.0.101.100.801.8a0.141.120.101.1a0.981.100.8.81.81.920.28.81.81.100.168.141.81.0.4.4.185.65.4.5.805.4","442.443.3.2.38.181.141.160.128.141.181.180.c1.0.101.100.801.8a0.141.120.101.1a0.981.100.8.81.81.920.128.1.81.80.81.0.901.140.24.4.85.25.4.5.805.4","42.43.42.43.120.9c1.541.570.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.0.108.1.81.30.140.181.0.181.80.1.141.940.164.4.85.25.4.5.5.4","2.3.3.842.148.101.81.30.100.181.100.181.80.1.101.940.8.181.1.180.168.41.c1.0.101.9a0.141.120.101.1a0.981.100.1.20.81.800.24.4.85.25.204.5.5.804","442.443.3.2.38.181.141.160.128.101.181.130.40.c1.0.101.1.1b0.901.160.101.1a0.181.900.108.1.81.30.140.181.0.981.80.801.141.140.164.4.85.25.4.5.5.804","442.443.43.42.141.1e0.141.970.101.120.181.130.80.81.101.940.8.181.1.180.168.101.81.80.188.1.181.30.140.181.0.981.880.1.141.140.164.4.85.25.4.5.5.804","42.43.3.2.30.981.541.560.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.100.8.81.81.120.128.1.81.80.81.0.101.140.24.4.85.25.4.5.5.4","42.43.3.2.30.981.541.560.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.0.108.1.81.30.140.181.0.181.80.1.141.940.164.4.85.25.4.5.5.4","442.443.3.2.38.181.141.160.128.101.181.130.40.81.80.1.8.81.1.130.168.101.81.80.188.101.101.1a0.181.0.981.30.0.881.41.140.164.4.85.25.4.5.5.804","22.83.803.102.100.1.80.841.168.101.81.30.140.181.180.101.8.81.1.130.168.101.81.80.88.1.101.9a0.881.880.101.100.1.20.881.0.24.4.85.25.204.5.805.4","442.443.3.2.38.181.141.160.128.101.181.130.40.c1.0.101.801.9b0.101.160.101.1a0.981.100.8.81.81.920.28.81.81.100.168.141.81.0.4.4.185.65.4.5.805.4","442.443.3.2.38.181.141.160.128.101.181.130.40.c1.0.101.801.9b0.101.160.101.1a0.981.100.8.81.81.920.128.1.81.80.81.0.901.140.24.4.85.25.4.5.805.4","442.443.43.42.141.1e0.141.970.101.120.181.130.80.81.101.940.108.101.1.80.c1.0.101.9c0.81.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","42.3.2.3.1.b0.901.120.101.120.181.930.80.81.901.140.8.181.1.180.168.101.81.80.88.1.101.9a0.881.880.101.100.1.20.881.0.24.4.85.25.204.5.805.4","442.443.43.42.141.1e0.141.970.101.1a0.181.100.141.20.81.0.1.a0.941.120.101.1a0.181.900.108.101.81.a0.181.0.981.30.800.881.41.140.164.4.85.25.4.5.5.804","42.3.2.3.1.b0.101.920.101.1a0.181.100.141.20.81.0.1.a0.941.120.101.1a0.181.900.108.1.81.30.140.181.0.981.80.801.141.140.164.4.85.25.4.5.5.804","22.83.3.102.140.1.80.1.800.981.541.540.120.181.d81.500.1.80.81.920.141.20.81.80.81.a0.901.120.101.20.81.830.0.81.841.140.164.4.85.25.4.5.5.4","442.443.3.2.38.181.141.160.128.141.181.180.c1.40.141.140.120.9c1.541.560.1e0.101.dc1.500.1.180.1.80.101.20.81.30.0.81.41.140.164.4.85.25.4.5.5.4","442.443.43.42.141.1e0.141.970.101.120.181.130.80.81.1.940.108.101.81.b0.0.c1.0.101.1.8b0.101.160.101.1a0.981.100.1.20.81.800.24.4.85.25.204.5.5.804","42.43.42.43.120.9c1.541.570.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.100.108.1.81.a0.81.80.101.100.1.20.81.0.24.4.85.25.204.5.5.4","2.3.3.842.148.101.81.30.100.181.100.181.80.1.181.840.1.80.801.130.141.20.81.880.881.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","442.443.43.42.141.1e0.941.170.101.120.181.930.80.81.901.140.8.181.1.180.168.101.81.80.88.1.101.9a0.881.880.101.100.1.20.881.0.24.4.85.25.204.5.805.4","42.43.3.2.30.981.541.560.120.181.d81.540.20.81.481.d00.1.80.81.120.1.a0.81.100.108.1.81.a0.81.80.101.100.1.20.81.0.24.4.85.25.204.5.5.4","442.443.3.2.38.181.141.160.128.101.181.130.40.81.80.1.8.81.1.930.168.1.81.80.88.81.901.120.128.1.81.830.0.81.800.101.34.84.885.25.4.5.5.4","42.43.42.43.120.9c1.541.570.120.181.d81.540.1a0.1.581.d00.140.101.0.81.80.1.101.940.148.141.81.30.140.181.100.181.80.1.141.940.164.4.85.25.4.5.5.4","42.3.2.3.1.b0.901.120.101.1a0.181.900.141.20.81.0.801.8a0.141.120.101.1a0.981.100.8.81.81.920.28.81.81.100.168.141.81.0.4.4.185.65.4.5.805.4","42.3.2.3.1.b0.901.120.101.1a0.181.900.141.20.81.0.801.8a0.141.120.101.1a0.981.100.8.81.81.920.128.1.81.80.81.0.901.140.24.4.85.25.4.5.805.4","442.443.43.42.141.1e0.141.970.101.1a0.181.100.141.20.81.0.1.a0.941.120.101.1a0.181.900.108.1.81.30.140.181.0.981.80.801.141.140.164.4.85.25.4.5.5.804","442.443.3.2.38.181.141.160.128.101.181.130.40.81.80.1.8.81.1.130.168.101.81.80.188.1.181.30.140.181.0.981.880.1.141.140.164.4.85.25.4.5.5.804","42.43.3.2.30.981.541.560.120.181.d81.540.1a0.1.581.d00.140.101.0.81.80.1.101.940.148.141.81.30.140.181.100.181.80.1.141.940.164.4.85.25.4.5.5.4","42.3.2.3.1.b0.101.120.101.1a0.181.100.141.60.c1.40.120.9c1.541.560.1e0.101.dc1.500.1.180.1.80.101.20.81.30.0.81.41.140.164.4.85.25.4.5.5.4","442.443.3.2.38.181.141.160.128.101.181.130.140.81.80.1.108.81.81.30.0.c1.0.101.1.8b0.101.160.101.1a0.981.100.1.20.81.800.24.4.85.25.204.5.5.804","442.443.43.42.141.1e0.941.170.101.1a0.181.900.141.20.81.0.801.8a0.141.120.101.1a0.981.100.8.81.81.920.28.81.81.100.168.141.81.0.4.4.185.65.4.5.805.4","442.443.3.2.38.181.141.160.128.101.181.130.140.81.80.1.108.181.1.1b0.c1.0.101.9c0.81.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","442.443.43.42.141.1e0.941.170.101.1a0.181.900.141.20.81.0.801.8a0.141.120.101.1a0.981.100.8.81.81.920.128.1.81.80.81.0.901.140.24.4.85.25.4.5.805.4","22.83.3.102.140.1.80.1.800.981.541.540.120.181.d81.500.1.80.81.920.141.20.81.80.81.a0.901.120.1.a0.81.900.1.20.81.0.24.4.85.25.204.5.5.4","442.443.3.2.38.181.141.160.128.101.181.130.40.81.80.1.8.81.1.130.168.101.81.80.88.1.101.9a0.881.880.101.100.1.20.881.0.24.4.85.25.204.5.805.4","442.443.3.2.38.181.141.160.128.141.181.180.c1.40.141.140.120.9c1.541.560.1e0.101.dc1.500.1.180.1.180.1.a0.81.100.1.20.81.0.24.4.85.25.204.5.5.4","442.443.43.42.141.1e0.141.170.101.1a0.181.100.141.60.c1.40.120.9c1.541.560.1e0.101.dc1.500.1.180.1.80.101.20.81.30.0.81.41.140.164.4.85.25.4.5.5.4","22.83.3.902.100.1.80.41.168.101.81.30.140.181.180.101.8.81.1.130.168.41.c1.0.101.9a0.141.120.101.1a0.981.100.1.20.81.800.24.4.85.25.204.5.5.804","42.3.2.3.1.b0.101.920.101.120.181.130.80.81.101.940.8.181.1.180.168.41.c1.0.101.9a0.141.120.101.1a0.981.100.1.20.81.800.24.4.85.25.204.5.5.804","442.443.43.42.141.1e0.141.970.101.120.181.130.80.81.101.940.8.181.1.180.168.41.c1.0.101.9a0.141.120.101.1a0.981.100.1.20.81.800.24.4.85.25.204.5.5.804","42.3.2.3.1.b0.101.120.101.1a0.181.100.141.60.c1.40.120.9c1.541.560.1e0.101.dc1.500.1.180.1.180.1.a0.81.100.1.20.81.0.24.4.85.25.204.5.5.4","22.83.3.902.100.1.80.41.168.101.81.30.140.1c1.100.101.1.1b0.901.160.141.120.181.980.881.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","42.3.2.3.1.b0.101.920.101.120.181.130.0.81.81.800.1.80.801.130.141.20.81.880.881.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","442.443.3.2.38.181.141.160.128.101.181.130.40.81.80.1.8.81.1.930.168.1.81.80.88.81.901.120.28.81.81.900.168.141.81.0.4.4.985.65.4.5.5.4","42.43.42.43.120.9c1.541.570.120.181.d81.540.20.81.481.d00.1.80.81.120.141.20.81.80.81.a0.101.920.101.20.81.30.0.81.41.940.164.4.85.25.4.5.5.4","42.43.3.2.30.981.541.560.120.181.d81.540.20.81.481.d00.1.80.81.120.141.20.81.80.81.a0.101.920.101.20.81.30.0.81.41.940.164.4.85.25.4.5.5.4","442.443.43.42.141.1e0.141.170.101.1a0.181.100.141.60.c1.40.120.9c1.541.560.1e0.101.dc1.500.1.180.1.180.1.a0.81.100.1.20.81.0.24.4.85.25.204.5.5.4","442.443.43.42.141.1e0.141.970.101.120.181.130.0.81.81.800.1.80.801.130.141.20.81.880.881.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","442.443.3.2.38.181.141.160.128.101.181.130.40.81.80.1.8.81.1.130.168.41.c1.0.101.9a0.141.120.101.1a0.981.100.1.20.81.800.24.4.85.25.204.5.5.804","442.443.3.2.38.181.141.160.128.141.181.180.c1.0.101.100.1.a0.941.120.141.120.181.980.881.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","42.43.42.43.120.9c1.541.570.120.181.d81.540.20.81.481.d00.1.80.81.120.141.20.81.80.81.a0.101.920.1.a0.81.100.1.20.81.0.24.4.85.25.204.5.5.4","442.443.3.2.38.181.141.160.128.101.181.130.40.c1.0.101.1.1b0.901.160.141.120.181.980.881.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","42.43.3.2.30.981.541.560.120.181.d81.540.20.81.481.d00.1.80.81.120.141.20.81.80.81.a0.101.920.1.a0.81.100.1.20.81.0.24.4.85.25.204.5.5.4","42.3.2.3.1.b0.101.920.101.1a0.181.100.141.20.81.0.1.a0.941.120.141.120.181.980.881.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804","442.443.43.42.141.1e0.141.970.101.1a0.181.100.141.20.81.0.1.a0.941.120.141.120.181.980.881.8a0.101.120.1.a0.881.100.1.20.81.800.24.4.85.25.204.5.5.804"],"rules":["only consonances against the cantus","begin on a perfect consonance","end on the octave or unison, by step, through the sixth or third","no unison except at the ends","no parallel fifths or octaves","no perfect consonance reached by similar motion","no tritones, sevenths or leaps larger than an octave","no repeated notes","after a leap larger than a third, a step back","no more than three parallel thirds or sixths in a row","no crossing, and no more than a tenth apart","a single highest note"]};
  var SHIFT16 = [-2, -1, 1, 2], LET16 = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"];
  function name16(p) { return LET16[p % 12] + (Math.floor(p / 12) - 1); }
  function step16(p, d) {
    var white = [0, 2, 4, 5, 7, 9, 11], q = p, k;
    if (white.indexOf(p % 12) < 0) return p + d;
    for (k = 0; k < Math.abs(d); k++) { q += d > 0 ? 1 : -1; while (white.indexOf(q % 12) < 0) q += d > 0 ? 1 : -1; }
    return q;
  }
  function motion16(a0, a1, b0, b1) {
    var da = a1 - a0, db = b1 - b0;
    if (da === 0 && db === 0) return "static";
    if (da === 0 || db === 0) return "oblique";
    if ((da > 0) !== (db > 0)) return "contrary";
    return da === db ? "parallel" : "similar";
  }
  function sound16(up, cf) {
    var rate = 44100, bar = 0.85, out = new Float32Array(Math.floor((cf.length * bar + 1.2) * rate)), i, k, h, v;
    for (i = 0; i < cf.length; i++) for (v = 0; v < 2; v++) {
      var hz = 440 * Math.pow(2, ((v ? cf[i] : up[i]) - 69) / 12), start = Math.floor(i * bar * rate), len = Math.floor((bar + 0.6) * rate);
      for (k = 0; k < len && start + k < out.length; k++) {
        var t = k / rate, y = 0;
        for (h = 1; h <= 6; h++) y += Math.sin(2 * Math.PI * hz * h * t) / (h * h) * Math.exp(-t * (1.6 + 0.8 * h));
        out[start + k] += 0.22 * y * Math.min(1, t / 0.004);
      }
    }
    return play(out, rate);
  }

  W.counterpoint = function (el) {
    QB.widget(el, {
      title: "One of 152 lines, and what breaks it",
      sub: "Fux's cantus firmus (blue) with a first-species line above it (gold). Pick any of the 152 lines that obey all twelve rules, ranked by Fux's preferences (1 is the line in the film). Then move one of its notes a step or two and see which rules the new line breaks: a red note is wrong. Right: the motion between the two voices at each move.",
      panels: 2, height: 300,
      controls: [
        { k: "line", label: "Which good line (1 is the best by Fux's preferences, 152 the worst)", min: 1, max: 152, step: 1, value: 1 },
        { k: "bar", label: "The note to move (0: none; 1 to 11 are the bars)", min: 0, max: 11, step: 1, value: 0 },
        { k: "shift", label: "Move it by so many steps of the scale (0: leave it)", min: -2, max: 2, step: 1, value: 1 },
      ],
      buttons: [
        { label: "Play the two voices", act: function (s) { s.sound = sound16(s.up, CP16.cf); } },
      ],
      init: function (s) { s.sound = null; s.up = CP16.lines[0].slice(); },
      draw: function (g, v, s) {
        var base = CP16.lines[v.line - 1], up = base.slice(), i, broken = [], bad = -1;
        if (v.bar > 0 && v.shift !== 0) {
          bad = v.bar - 1;
          up[bad] = step16(up[bad], v.shift);
          var mask = parseInt(CP16.masks[v.line - 1].split(".")[bad * 4 + SHIFT16.indexOf(v.shift)], 16);
          for (i = 0; i < CP16.rules.length; i++) if (mask & (1 << i)) broken.push(CP16.rules[i]);
        }
        s.up = up; s.broken = broken; s.bad = bad;
        var xs = [], cf = CP16.cf;
        for (i = 0; i < cf.length; i++) xs.push(i + 1);
        var a = g[0].axes({ x: [0.3, 11.7], y: [58, 82], title: "Two voices, one note to a bar", xlabel: "bar", ylabel: "key (60 is middle C)", xticks: [1, 3, 5, 7, 9, 11] });
        for (i = 0; i < cf.length; i++) a.line([xs[i], xs[i]], [cf[i], up[i]], { color: C.line, width: 1 });
        a.line(xs, cf, { color: C.spot, width: 1.2, alpha: 0.6 });
        a.dots(xs, cf, { color: C.spot, r: 5 });
        a.line(xs, up, { color: C.idea, width: 1.2, alpha: 0.6 });
        a.dots(xs, up, { color: function (k) { return k === bad ? (broken.length ? C.loss : C.gain) : C.idea; }, r: 5 });
        for (i = 0; i < cf.length; i++) {
          var iv = up[i] - cf[i], label = { 0: "1", 3: "3", 4: "3", 7: "5", 8: "6", 9: "6", 12: "8", 15: "10", 16: "10", 19: "12", 20: "13", 21: "13", 24: "15" }[iv];
          a.text(xs[i], 59.3, label || "×", { align: "center", size: 10.5, color: label ? C.muted : C.loss });
        }
        var kinds = ["parallel", "similar", "contrary", "oblique"], counts = [0, 0, 0, 0];
        for (i = 1; i < cf.length; i++) { var m = kinds.indexOf(motion16(up[i - 1], up[i], cf[i - 1], cf[i])); if (m >= 0) counts[m]++; }
        s.counts = counts;
        var b = g[1].axes({ x: [0.3, 4.7], y: [0, 10], title: "Motion at the ten moves", xticks: [], ylabel: "moves" });
        b.bars([1, 2, 3, 4], counts, 0.6, { color: function (k) { return k === 2 ? C.gain : (k < 2 ? C.implied : C.idea); } });
        for (i = 0; i < 4; i++) b.text(i + 1, 0, kinds[i], { align: "center", base: "top", dy: 7, color: C.muted });
      },
      readout: function (v, s) {
        var base = CP16.lines[v.line - 1];
        return [["the line", s.up.map(name16).join(" ")],
                ["rank by Fux's preferences", v.line + " of 152 (score " + fmt(CP16.scores[v.line - 1], 1) + ")"],
                ["contrary moves", s.counts[2] + " of 10"],
                ["the moved note", s.bad < 0 ? "none" : name16(base[s.bad]) + " to " + name16(s.up[s.bad]) + " in bar " + (s.bad + 1)],
                ["rules broken", s.bad < 0 ? "none" : (s.broken.length ? s.broken.join("; ") : "none: this is another of the 152")],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Of the 6,688 ways to move one note of a good line by one or two steps, 97 in a hundred break a rule, and three in four break two or more at once: a note moved off a consonance often also reaches a perfect interval by similar motion or spoils a leap's recovery. Every change to the cadence (bars 10 and 11) breaks it. The top lines move in contrary motion seven to nine times in ten; the bottom ones only once or twice, and obey every rule while sounding aimless, which is the Frontier's open question: the rules say what to avoid, not what makes a line good."
    });
  };

  // ---- Part 17: a harmonizer you can steer ---------------------------------------------------------------------
  // The chord model (learned from 280 of Bach's chorales, split by tune) and the search of the film, run in the page:
  // chords and voicings chosen together by the Viterbi algorithm, with the penalties on sliders.
  var HZ17 = {"models":{"major":{"names":["I","V","vi","IV","ii","V7","ii7","II","iii","vi7","III","II7","VI","vii°","IVmaj7","VI7","iii7","I7","viiø7","♭VII","III7","v","♯iv°","vii7","iiiø7","iii°","Imaj7","♭ii°"],"members":[[0,4,7],[7,11,2],[9,0,4],[5,9,0],[2,5,9],[7,11,2,5],[2,5,9,0],[2,6,9],[4,7,11],[9,0,4,7],[4,8,11],[2,6,9,0],[9,1,4],[11,2,5],[5,9,0,4],[9,1,4,7],[4,7,11,2],[0,4,7,10],[11,2,5,9],[10,2,5],[4,8,11,2],[7,10,2],[6,9,0],[11,2,6,9],[4,7,10,2],[4,7,10],[0,4,7,11],[1,4,7]],"T":[[-0.94,-1.65,-2.81,-2.03,-3.68,-4.08,-2.98,-4.11,-4.56,-3.98,-5.31,-4.11,-5.42,-4.14,-4.46,-5.11,-5.88,-4.67,-9.82,-5.88,-7.42,-6.77,-5.31,-6.77,-9.82,-7.42,-5.11,-9.82],[-0.88,-1.35,-2.96,-3.36,-3.36,-3.67,-7.07,-3.36,-3.31,-3.27,-3.55,-5.54,-6.03,-6.42,-6.42,-5.76,-5.54,-5.07,-7.07,-7.07,-5.07,-9.47,-7.07,-9.47,-9.47,-7.07,-5.76,-5.21],[-2.22,-1.93,-1.58,-2.87,-2.87,-4.21,-2.56,-3.41,-2.54,-3.81,-3.25,-2.9,-5.17,-3.99,-5.17,-6.21,-4.49,-4.89,-3.59,-8.6,-6.21,-4.89,-6.21,-4.67,-8.6,-5.56,-6.21,-6.21],[-1.24,-2.08,-3.18,-1.87,-2.59,-2.79,-3.45,-3.82,-3.58,-4.82,-5.1,-4.14,-6.13,-2.89,-4.42,-5.1,-4.6,-5.1,-3.82,-4.6,-8.53,-5.49,-8.53,-4.82,-6.13,-8.53,-8.53,-5.49],[-1.66,-2.47,-2.41,-3.45,-1.54,-2.57,-4.53,-5.2,-3.53,-5.84,-3.53,-4.53,-2.72,-4.31,-4.13,-4.53,-4.31,-5.2,-5.2,-4.13,-4.31,-4.81,-5.84,-8.24,-3.85,-3.85,-8.24,-4.53],[-0.31,-3.71,-2.93,-3.93,-3.53,-3.71,-4.59,-7.64,-3.93,-4.59,-5.24,-7.64,-7.64,-7.64,-3.71,-4.21,-7.64,-7.64,-7.64,-7.64,-7.64,-7.64,-7.64,-7.64,-7.64,-7.64,-7.64,-3.93],[-1.39,-0.8,-5.19,-3.48,-5.19,-2.29,-4.16,-5.19,-4.16,-7.59,-3.48,-7.59,-7.59,-3.88,-5.19,-7.59,-3.88,-7.59,-4.16,-5.19,-7.59,-7.59,-7.59,-7.59,-5.19,-5.19,-5.19,-7.59],[-3.81,-0.28,-4.48,-7.52,-7.52,-4.09,-7.52,-2.57,-4.09,-7.52,-5.12,-3.26,-7.52,-7.52,-7.52,-7.52,-7.52,-7.52,-7.52,-7.52,-7.52,-4.09,-4.48,-4.48,-7.52,-5.12,-5.12,-7.52],[-2.0,-2.58,-1.67,-1.89,-3.13,-4.09,-4.48,-4.48,-2.65,-1.67,-4.48,-4.48,-5.13,-7.53,-3.81,-3.42,-7.53,-7.53,-7.53,-7.53,-7.53,-7.53,-7.53,-4.48,-7.53,-7.53,-5.13,-7.53],[-3.09,-1.52,-7.35,-2.74,-3.09,-3.24,-2.74,-1.18,-4.95,-4.95,-7.35,-2.27,-7.35,-4.95,-7.35,-7.35,-4.95,-4.95,-7.35,-4.31,-7.35,-7.35,-3.09,-7.35,-7.35,-4.95,-7.35,-7.35],[-4.23,-7.27,-0.5,-2.48,-7.27,-7.27,-7.27,-7.27,-3.34,-7.27,-1.79,-7.27,-3.16,-7.27,-4.87,-7.27,-7.27,-7.27,-7.27,-7.27,-3.56,-7.27,-7.27,-7.27,-7.27,-7.27,-7.27,-7.27],[-3.65,-0.39,-3.65,-7.09,-7.09,-4.69,-7.09,-4.69,-3.16,-4.04,-3.37,-2.98,-7.09,-7.09,-7.09,-7.09,-7.09,-7.09,-7.09,-7.09,-4.04,-2.98,-4.69,-7.09,-7.09,-4.69,-4.69,-7.09],[-2.26,-4.48,-2.08,-4.48,-1.01,-6.88,-6.88,-3.44,-3.44,-6.88,-6.88,-6.88,-1.43,-6.88,-6.88,-3.83,-6.88,-6.88,-4.48,-4.48,-6.88,-6.88,-6.88,-6.88,-4.48,-6.88,-6.88,-4.48],[-0.58,-3.09,-6.8,-3.37,-4.4,-2.54,-3.76,-6.8,-2.69,-6.8,-3.09,-6.8,-4.4,-3.76,-6.8,-6.8,-3.37,-6.8,-6.8,-6.8,-3.76,-6.8,-6.8,-6.8,-3.76,-6.8,-6.8,-6.8],[-1.33,-1.86,-3.73,-6.13,-3.08,-1.86,-3.08,-6.13,-3.73,-6.13,-3.73,-6.13,-6.13,-2.02,-3.08,-6.13,-6.13,-3.73,-3.73,-6.13,-6.13,-6.13,-6.13,-6.13,-6.13,-6.13,-6.13,-6.13],[-5.88,-5.88,-5.88,-5.88,-0.36,-3.48,-5.88,-2.45,-3.48,-5.88,-5.88,-5.88,-5.88,-5.88,-5.88,-5.88,-3.48,-5.88,-5.88,-2.84,-5.88,-5.88,-5.88,-5.88,-5.88,-5.88,-5.88,-5.88],[-1.11,-1.88,-2.55,-2.27,-2.94,-3.59,-2.94,-5.99,-5.99,-2.05,-5.99,-5.99,-5.99,-5.99,-5.99,-5.99,-5.99,-5.99,-5.99,-5.99,-5.99,-5.99,-3.59,-5.99,-5.99,-5.99,-5.99,-5.99],[-3.61,-6.01,-3.61,-0.71,-1.62,-6.01,-2.3,-6.01,-6.01,-3.61,-6.01,-6.01,-6.01,-6.01,-6.01,-6.01,-6.01,-3.61,-6.01,-6.01,-6.01,-6.01,-2.97,-6.01,-6.01,-6.01,-6.01,-6.01],[-1.54,-5.93,-1.82,-3.54,-5.93,-5.93,-5.93,-5.93,-2.5,-3.54,-1.32,-5.93,-3.54,-3.54,-5.93,-2.89,-3.54,-5.93,-5.93,-5.93,-5.93,-5.93,-5.93,-3.54,-5.93,-5.93,-5.93,-5.93],[-2.65,-3.3,-3.3,-1.98,-2.26,-3.3,-5.7,-5.7,-5.7,-5.7,-5.7,-5.7,-5.7,-5.7,-5.7,-3.3,-5.7,-2.65,-5.7,-2.26,-5.7,-5.7,-5.7,-5.7,-1.59,-2.26,-5.7,-5.7],[-5.66,-5.66,-0.26,-2.62,-5.66,-5.66,-5.66,-5.66,-5.66,-5.66,-3.27,-5.66,-5.66,-5.66,-5.66,-5.66,-5.66,-5.66,-5.66,-5.66,-3.27,-5.66,-5.66,-5.66,-5.66,-5.66,-5.66,-5.66],[-3.03,-5.43,-3.03,-2.38,-2.0,-3.03,-5.43,-3.03,-3.03,-5.43,-5.43,-3.03,-5.43,-5.43,-5.43,-5.43,-5.43,-2.38,-5.43,-2.38,-5.43,-1.5,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43],[-5.79,-0.31,-3.4,-5.79,-5.79,-5.79,-5.79,-3.4,-5.79,-3.4,-5.79,-3.4,-5.79,-5.79,-5.79,-5.79,-5.79,-5.79,-5.79,-5.79,-5.79,-5.79,-3.4,-3.4,-5.79,-5.79,-5.79,-5.79],[-0.78,-1.85,-2.24,-5.29,-5.29,-5.29,-5.29,-5.29,-5.29,-2.89,-5.29,-5.29,-5.29,-5.29,-5.29,-5.29,-2.89,-5.29,-5.29,-5.29,-2.89,-5.29,-5.29,-5.29,-5.29,-5.29,-5.29,-5.29],[-5.38,-5.38,-5.38,-5.38,-0.99,-5.38,-5.38,-5.38,-5.38,-2.99,-5.38,-5.38,-0.77,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38],[-5.38,-5.38,-5.38,-0.87,-5.38,-2.99,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38,-1.67,-5.38,-5.38,-2.99,-5.38,-2.99,-5.38,-2.99,-5.38,-2.34,-5.38,-5.38,-5.38,-5.38,-5.38,-5.38],[-5.34,-2.29,-2.29,-0.94,-5.34,-5.34,-5.34,-1.9,-5.34,-5.34,-5.34,-2.94,-5.34,-5.34,-5.34,-5.34,-5.34,-5.34,-5.34,-5.34,-5.34,-5.34,-2.29,-5.34,-5.34,-5.34,-5.34,-5.34],[-5.43,-5.43,-5.43,-5.43,-0.29,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43,-2.38,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43,-5.43,-3.03]],"E":[[-0.82,-9.98,-9.98,-9.98,-0.99,-9.98,-9.98,-1.69,-9.98,-9.98,-9.98,-9.98],[-9.56,-9.56,-0.77,-9.56,-9.56,-9.56,-9.56,-1.02,-9.56,-9.56,-9.56,-1.74],[-0.51,-8.72,-8.72,-8.72,-1.32,-8.72,-8.72,-8.72,-8.72,-2.04,-8.72,-8.72],[-1.59,-8.64,-8.64,-8.64,-8.64,-0.94,-8.64,-8.64,-8.64,-0.91,-8.64,-8.64],[-8.35,-8.35,-1.0,-8.35,-8.35,-0.81,-8.35,-8.35,-8.35,-1.68,-8.35,-8.35],[-7.73,-7.73,-1.15,-7.73,-7.73,-1.35,-7.73,-1.31,-7.73,-7.73,-7.73,-1.9],[-3.16,-7.67,-0.48,-7.67,-7.67,-1.15,-7.67,-7.67,-7.67,-3.96,-7.67,-7.67],[-7.65,-7.65,-1.3,-7.65,-7.65,-7.65,-2.13,-7.65,-7.65,-0.5,-7.65,-7.65],[-7.65,-7.65,-7.65,-7.65,-1.97,-7.65,-7.65,-0.58,-7.65,-7.65,-7.65,-1.21],[-1.13,-7.42,-7.42,-7.42,-2.47,-7.42,-7.42,-1.56,-7.42,-0.97,-7.42,-7.42],[-7.37,-7.37,-7.37,-7.37,-0.49,-7.37,-7.37,-7.37,-2.58,-7.37,-7.37,-1.18],[-1.06,-7.17,-0.98,-7.17,-7.17,-7.17,-2.22,-7.17,-7.17,-1.82,-7.17,-7.17],[-7.0,-2.29,-7.0,-7.0,-0.36,-7.0,-7.0,-7.0,-7.0,-1.64,-7.0,-7.0],[-6.85,-6.85,-1.17,-6.85,-6.85,-1.28,-6.85,-6.85,-6.85,-6.85,-6.85,-0.91],[-2.92,-6.35,-6.35,-6.35,-1.84,-0.61,-6.35,-6.35,-6.35,-1.47,-6.35,-6.35],[-6.22,-3.17,-6.22,-6.22,-1.27,-6.22,-6.22,-0.87,-6.22,-1.42,-6.22,-6.22],[-6.2,-6.2,-0.9,-6.2,-1.58,-6.2,-6.2,-1.32,-6.2,-6.2,-6.2,-2.27],[-1.5,-6.11,-6.11,-6.11,-1.03,-6.11,-6.11,-1.1,-6.11,-6.11,-2.68,-6.11],[-6.0,-6.0,-1.73,-6.0,-6.0,-2.06,-6.0,-6.0,-6.0,-1.6,-6.0,-0.74],[-5.89,-5.89,-0.64,-5.89,-5.89,-1.02,-5.89,-5.89,-5.89,-5.89,-2.46,-5.89],[-5.81,-5.81,-0.79,-5.81,-0.93,-5.81,-5.81,-5.81,-2.37,-5.81,-5.81,-3.41],[-5.77,-5.77,-1.38,-5.77,-5.77,-5.77,-5.77,-0.83,-5.77,-5.77,-1.26,-5.77],[-0.83,-5.77,-5.77,-5.77,-5.77,-5.77,-0.76,-5.77,-5.77,-2.73,-5.77,-5.77],[-5.53,-5.53,-0.33,-5.53,-5.53,-5.53,-5.53,-5.53,-5.53,-1.82,-5.53,-2.48],[-5.49,-5.49,-3.09,-5.49,-0.35,-5.49,-5.49,-1.56,-5.49,-5.49,-5.49,-5.49],[-5.4,-5.4,-5.4,-5.4,-0.45,-5.4,-5.4,-1.14,-5.4,-5.4,-5.4,-5.4],[-0.89,-5.4,-5.4,-5.4,-1.01,-5.4,-5.4,-3.0,-5.4,-5.4,-5.4,-1.97],[-5.4,-1.97,-5.4,-5.4,-0.45,-5.4,-5.4,-1.69,-5.4,-5.4,-5.4,-5.4]],"F":[-0.9,-1.13,-2.67,-3.06,-3.23,-5.71,-9.15,-4.44,-4.35,-9.15,-3.38,-9.15,-3.32,-9.15,-9.15,-9.15,-9.15,-6.1,-9.15,-5.22,-6.75,-5.43,-6.75,-9.15,-9.15,-9.15,-9.15,-9.15],"S":[-0.99,-1.77,-2.62,-2.92,-2.85,-3.03,-3.21,-3.43,-4.12,-3.84,-4.3,-3.97,-4.12,-4.99,-4.99,-4.99,-4.41,-8.92,-4.99,-5.48,-5.48,-6.52,-5.87,-4.65,-5.87,-6.52,-6.52,-8.92]},"minor":{"names":["i","III","iv","V","VII","I","VI","IV","v","iiø7","vii","iv7","♭II","V7","VII7","IV7","ii°","VImaj7","vø7","I7","II","vii°","v7","vii7","i7","ii7","ii","II7","vi°","viø7","vii°7","v°","♯iv°7","♭IImaj7"],"members":[[0,3,7],[3,7,10],[5,8,0],[7,11,2],[10,2,5],[0,4,7],[8,0,3],[5,9,0],[7,10,2],[2,5,8,0],[10,1,5],[5,8,0,3],[1,5,8],[7,11,2,5],[10,2,5,8],[5,9,0,3],[2,5,8],[8,0,3,7],[7,10,1,5],[0,4,7,10],[2,6,9],[11,2,5],[7,10,2,5],[10,1,5,8],[0,3,7,10],[2,5,9,0],[2,5,9],[2,6,9,0],[9,0,3],[9,0,3,7],[11,2,5,8],[7,10,1],[6,9,0,3],[1,5,8,0]],"T":[[-1.16,-3.38,-2.59,-1.92,-2.8,-4.67,-3.09,-3.35,-3.32,-2.82,-6.14,-3.66,-6.78,-4.79,-4.67,-3.74,-4.1,-4.57,-9.18,-5.75,-5.47,-4.1,-5.25,-6.78,-5.07,-3.98,-4.79,-4.92,-6.78,-5.25,-5.07,-9.18,-6.14,-9.18],[-2.33,-1.11,-3.09,-4.22,-2.01,-4.32,-1.81,-4.72,-4.44,-4.72,-5.12,-3.23,-5.79,-5.12,-4.12,-3.82,-4.57,-4.72,-8.83,-5.4,-6.44,-5.12,-5.4,-6.44,-4.22,-6.44,-5.4,-8.83,-4.32,-5.4,-6.44,-5.79,-8.83,-8.83],[-2.22,-2.9,-1.28,-3.23,-3.1,-2.16,-3.23,-4.74,-4.41,-3.53,-3.32,-4.41,-3.96,-4.27,-3.36,-5.23,-4.27,-4.95,-3.1,-6.27,-5.23,-8.67,-4.56,-4.16,-6.27,-8.67,-8.67,-8.67,-8.67,-8.67,-5.23,-4.41,-4.16,-4.56],[-0.78,-4.69,-5.58,-1.23,-6.23,-2.06,-2.95,-4.91,-4.91,-8.62,-6.23,-8.62,-8.62,-3.83,-8.62,-8.62,-8.62,-6.23,-8.62,-8.62,-8.62,-6.23,-8.62,-8.62,-8.62,-6.23,-8.62,-6.23,-8.62,-5.19,-8.62,-8.62,-8.62,-8.62],[-2.84,-0.75,-2.97,-3.9,-1.65,-4.3,-4.01,-3.16,-3.7,-8.41,-6.01,-8.41,-8.41,-5.36,-4.69,-5.36,-6.01,-8.41,-8.41,-3.9,-4.97,-6.01,-4.15,-8.41,-4.15,-8.41,-8.41,-8.41,-4.69,-6.01,-4.97,-8.41,-8.41,-8.41],[-3.36,-5.84,-1.09,-5.84,-3.97,-0.81,-3.97,-2.67,-5.84,-8.24,-8.24,-8.24,-3.84,-8.24,-8.24,-5.19,-5.84,-5.84,-8.24,-4.3,-5.84,-8.24,-8.24,-8.24,-8.24,-5.19,-5.84,-5.19,-8.24,-8.24,-8.24,-8.24,-5.84,-8.24],[-3.12,-1.57,-2.24,-3.7,-3.01,-4.1,-1.67,-5.16,-4.77,-2.76,-3.81,-3.5,-2.95,-8.21,-3.5,-5.16,-3.19,-3.94,-5.81,-5.81,-5.16,-5.81,-5.16,-3.41,-5.81,-5.81,-8.21,-8.21,-5.81,-8.21,-5.81,-5.81,-5.16,-4.77],[-2.62,-3.7,-5.01,-3.15,-1.19,-4.37,-5.01,-1.26,-4.37,-5.01,-2.16,-7.41,-7.41,-4.37,-7.41,-4.37,-7.41,-7.41,-7.41,-5.01,-7.41,-3.98,-7.41,-7.41,-7.41,-7.41,-3.15,-7.41,-5.01,-7.41,-7.41,-7.41,-7.41,-7.41],[-2.14,-2.14,-2.25,-7.39,-2.52,-3.68,-3.0,-3.28,-1.69,-7.39,-4.35,-7.39,-4.99,-7.39,-7.39,-4.99,-4.35,-3.28,-4.99,-3.46,-2.68,-7.39,-7.39,-7.39,-7.39,-7.39,-4.35,-3.68,-4.99,-3.13,-7.39,-7.39,-7.39,-7.39],[-1.9,-4.2,-4.85,-0.51,-4.85,-2.98,-3.81,-7.25,-3.53,-4.85,-7.25,-7.25,-7.25,-3.32,-7.25,-7.25,-7.25,-2.98,-7.25,-7.25,-7.25,-7.25,-7.25,-7.25,-7.25,-4.85,-7.25,-7.25,-7.25,-7.25,-7.25,-7.25,-7.25,-7.25],[-6.77,-2.51,-1.76,-6.77,-3.73,-2.51,-2.38,-2.84,-6.77,-6.77,-1.76,-4.38,-3.73,-4.38,-6.77,-4.38,-6.77,-4.38,-2.84,-3.34,-6.77,-6.77,-6.77,-3.06,-6.77,-6.77,-6.77,-6.77,-3.73,-6.77,-4.38,-3.34,-6.77,-4.38],[-4.16,-1.85,-6.56,-3.12,-0.72,-6.56,-4.16,-6.56,-4.16,-2.29,-4.16,-6.56,-3.51,-6.56,-3.51,-6.56,-3.51,-6.56,-6.56,-6.56,-6.56,-6.56,-4.16,-6.56,-6.56,-6.56,-6.56,-6.56,-6.56,-6.56,-6.56,-6.56,-4.16,-6.56],[-6.65,-3.61,-3.22,-6.65,-3.61,-3.22,-1.7,-4.25,-6.65,-6.65,-1.57,-6.65,-1.94,-4.25,-6.65,-4.25,-6.65,-6.65,-2.26,-6.65,-6.65,-6.65,-6.65,-3.61,-6.65,-6.65,-6.65,-6.65,-3.61,-6.65,-4.25,-2.72,-6.65,-3.61],[-0.64,-6.47,-6.47,-2.75,-6.47,-1.85,-2.75,-6.47,-6.47,-4.07,-6.47,-4.07,-6.47,-2.54,-6.47,-4.07,-6.47,-6.47,-6.47,-6.47,-6.47,-6.47,-6.47,-6.47,-6.47,-6.47,-6.47,-6.47,-6.47,-4.07,-6.47,-6.47,-6.47,-6.47],[-2.79,-0.48,-2.79,-3.82,-6.22,-3.18,-3.82,-6.22,-3.82,-6.22,-6.22,-3.82,-6.22,-6.22,-3.18,-6.22,-3.82,-3.82,-6.22,-6.22,-6.22,-6.22,-6.22,-6.22,-6.22,-6.22,-6.22,-6.22,-6.22,-6.22,-6.22,-6.22,-6.22,-6.22],[-1.94,-3.94,-6.34,-2.4,-0.85,-6.34,-6.34,-6.34,-6.34,-6.34,-2.4,-6.34,-6.34,-2.9,-6.34,-3.94,-6.34,-6.34,-6.34,-6.34,-6.34,-2.62,-6.34,-6.34,-6.34,-6.34,-3.94,-6.34,-3.94,-6.34,-6.34,-6.34,-6.34,-6.34],[-3.31,-1.21,-6.35,-1.27,-3.95,-6.35,-2.24,-6.35,-3.31,-6.35,-6.35,-3.95,-6.35,-3.95,-3.95,-3.95,-3.31,-6.35,-6.35,-3.95,-6.35,-6.35,-6.35,-6.35,-6.35,-6.35,-6.35,-6.35,-6.35,-6.35,-6.35,-6.35,-2.92,-6.35],[-3.27,-2.21,-1.92,-2.39,-2.88,-6.32,-3.92,-2.6,-6.32,-2.6,-6.32,-6.32,-3.27,-3.92,-2.88,-6.32,-2.6,-3.27,-3.92,-6.32,-6.32,-2.6,-6.32,-6.32,-6.32,-6.32,-6.32,-6.32,-6.32,-6.32,-6.32,-3.92,-6.32,-3.92],[-6.12,-6.12,-2.01,-6.12,-6.12,-0.55,-6.12,-6.12,-6.12,-6.12,-6.12,-6.12,-3.72,-6.12,-6.12,-6.12,-6.12,-6.12,-6.12,-2.68,-6.12,-6.12,-2.68,-6.12,-6.12,-6.12,-6.12,-6.12,-6.12,-6.12,-3.72,-6.12,-6.12,-3.07],[-6.1,-6.1,-0.79,-6.1,-6.1,-3.05,-3.7,-1.98,-3.05,-3.7,-6.1,-6.1,-2.66,-6.1,-3.7,-6.1,-6.1,-6.1,-6.1,-3.7,-3.7,-6.1,-3.7,-6.1,-6.1,-6.1,-6.1,-3.7,-6.1,-6.1,-6.1,-6.1,-6.1,-3.7],[-6.14,-3.74,-6.14,-1.0,-6.14,-6.14,-6.14,-6.14,-0.94,-6.14,-6.14,-6.14,-6.14,-6.14,-6.14,-6.14,-6.14,-6.14,-6.14,-6.14,-2.21,-6.14,-6.14,-6.14,-6.14,-6.14,-6.14,-3.1,-6.14,-6.14,-6.14,-6.14,-6.14,-6.14],[-0.25,-6.05,-6.05,-3.65,-6.05,-6.05,-6.05,-6.05,-6.05,-3.65,-6.05,-6.05,-6.05,-3.65,-6.05,-6.05,-6.05,-6.05,-6.05,-6.05,-6.05,-6.05,-6.05,-6.05,-6.05,-6.05,-6.05,-6.05,-6.05,-6.05,-2.62,-6.05,-6.05,-6.05],[-5.84,-1.23,-1.91,-5.84,-3.44,-2.41,-1.91,-2.8,-5.84,-5.84,-5.84,-3.44,-5.84,-5.84,-5.84,-5.84,-5.84,-3.44,-5.84,-2.8,-5.84,-5.84,-5.84,-5.84,-5.84,-5.84,-5.84,-5.84,-3.44,-5.84,-5.84,-5.84,-5.84,-5.84],[-5.84,-0.97,-2.8,-5.84,-5.84,-5.84,-1.23,-5.84,-5.84,-5.84,-5.84,-5.84,-5.84,-5.84,-5.84,-5.84,-5.84,-3.44,-3.44,-5.84,-5.84,-5.84,-3.44,-3.44,-3.44,-5.84,-5.84,-5.84,-5.84,-5.84,-5.84,-3.44,-5.84,-5.84],[-3.35,-2.32,-5.75,-5.75,-1.82,-5.75,-1.49,-1.64,-5.75,-5.75,-5.75,-2.7,-5.75,-5.75,-5.75,-2.7,-5.75,-5.75,-5.75,-5.75,-3.35,-5.75,-5.75,-3.35,-5.75,-5.75,-5.75,-5.75,-5.75,-5.75,-5.75,-5.75,-5.75,-5.75],[-0.53,-2.57,-5.61,-2.57,-3.22,-3.22,-5.61,-3.22,-5.61,-3.22,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61,-5.61],[-1.43,-5.37,-5.37,-5.37,-1.65,-2.97,-2.32,-2.97,-2.32,-5.37,-5.37,-5.37,-5.37,-2.97,-5.37,-5.37,-5.37,-5.37,-5.37,-5.37,-5.37,-5.37,-2.97,-5.37,-5.37,-5.37,-5.37,-2.97,-5.37,-5.37,-5.37,-5.37,-5.37,-5.37],[-5.58,-3.18,-5.58,-0.96,-5.58,-5.58,-5.58,-5.58,-0.87,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-3.18,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58,-5.58],[-3.06,-5.46,-5.46,-3.06,-0.75,-5.46,-5.46,-3.06,-3.06,-5.46,-2.02,-5.46,-5.46,-5.46,-5.46,-3.06,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46,-3.06,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46],[-2.41,-5.46,-5.46,-2.41,-3.06,-5.46,-5.46,-3.06,-1.74,-3.06,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46,-1.34,-3.06,-5.46,-5.46,-5.46,-5.46,-5.46,-2.41,-5.46,-5.46,-5.46,-5.46,-5.46,-5.46],[-0.7,-5.41,-2.37,-5.41,-5.41,-1.7,-5.41,-5.41,-5.41,-5.41,-5.41,-5.41,-5.41,-3.01,-5.41,-5.41,-5.41,-5.41,-5.41,-3.01,-5.41,-5.41,-5.41,-5.41,-5.41,-5.41,-5.41,-5.41,-5.41,-5.41,-5.41,-5.41,-5.41,-5.41],[-5.32,-2.92,-2.92,-5.32,-5.32,-1.88,-1.88,-5.32,-5.32,-5.32,-2.92,-5.32,-2.27,-5.32,-5.32,-5.32,-5.32,-2.27,-5.32,-2.92,-5.32,-5.32,-5.32,-5.32,-5.32,-5.32,-5.32,-5.32,-5.32,-5.32,-1.88,-5.32,-5.32,-5.32],[-5.16,-5.16,-5.16,-0.36,-5.16,-5.16,-5.16,-5.16,-2.11,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16,-5.16],[-5.27,-2.87,-2.87,-5.27,-2.87,-1.34,-5.27,-5.27,-5.27,-2.87,-2.87,-5.27,-5.27,-5.27,-5.27,-5.27,-5.27,-5.27,-1.83,-5.27,-5.27,-5.27,-5.27,-2.87,-5.27,-5.27,-5.27,-5.27,-5.27,-5.27,-5.27,-2.87,-5.27,-2.87]],"E":[[-1.03,-9.29,-9.29,-0.89,-9.29,-9.29,-9.29,-1.47,-9.29,-9.29,-9.29,-9.29],[-8.96,-8.96,-8.96,-1.02,-8.96,-8.96,-8.96,-0.82,-8.96,-8.96,-1.63,-8.96],[-1.41,-8.77,-8.77,-8.77,-8.77,-0.79,-8.77,-8.77,-1.21,-8.77,-8.77,-8.77],[-8.71,-8.71,-0.64,-8.71,-8.71,-8.71,-8.71,-1.07,-8.71,-8.71,-8.71,-2.09],[-8.52,-8.52,-1.42,-8.52,-8.52,-0.83,-8.52,-8.52,-8.52,-8.52,-1.14,-8.52],[-0.58,-8.47,-8.47,-8.47,-2.31,-8.47,-8.47,-1.08,-8.47,-8.47,-8.47,-8.47],[-0.59,-8.35,-8.35,-1.62,-8.35,-8.35,-8.35,-8.35,-1.4,-8.35,-8.35,-8.35],[-1.0,-7.62,-7.62,-7.62,-7.62,-0.56,-7.62,-7.62,-7.62,-2.91,-7.62,-7.62],[-7.48,-7.48,-1.77,-7.48,-7.48,-7.48,-7.48,-1.19,-7.48,-7.48,-0.65,-7.48],[-2.59,-7.3,-0.32,-7.3,-7.3,-1.74,-7.3,-7.3,-3.87,-7.3,-7.3,-7.3],[-7.04,-1.52,-7.04,-7.04,-7.04,-1.64,-7.04,-7.04,-7.04,-7.04,-0.55,-7.04],[-2.89,-6.83,-6.83,-2.21,-6.83,-0.44,-6.83,-6.83,-1.68,-6.83,-6.83,-6.83],[-6.71,-2.6,-6.71,-6.71,-6.71,-0.82,-6.71,-6.71,-0.74,-6.71,-6.71,-6.71],[-6.54,-6.54,-1.34,-6.54,-6.54,-1.29,-6.54,-1.14,-6.54,-6.54,-6.54,-2.03],[-6.54,-6.54,-2.28,-6.54,-6.54,-1.01,-6.54,-6.54,-1.4,-6.54,-1.29,-6.54],[-1.55,-6.5,-6.5,-1.55,-6.5,-0.79,-6.5,-6.5,-6.5,-2.23,-6.5,-6.5],[-6.43,-6.43,-0.46,-6.43,-6.43,-1.56,-6.43,-6.43,-1.92,-6.43,-6.43,-6.43],[-0.78,-6.38,-6.38,-2.12,-6.38,-6.38,-6.38,-1.13,-2.45,-6.38,-6.38,-6.38],[-6.3,-6.3,-6.3,-6.3,-6.3,-1.78,-6.3,-0.59,-6.3,-6.3,-1.35,-6.3],[-0.84,-6.24,-6.24,-6.24,-2.8,-6.24,-6.24,-1.36,-6.24,-6.24,-1.44,-6.24],[-6.22,-6.22,-1.02,-6.22,-6.22,-6.22,-1.6,-6.22,-6.22,-0.87,-6.22,-6.22],[-6.07,-6.07,-1.36,-6.07,-6.07,-0.82,-6.07,-6.07,-6.07,-6.07,-6.07,-1.27],[-6.0,-6.0,-2.95,-6.0,-6.0,-1.29,-6.0,-1.29,-6.0,-6.0,-0.98,-6.0],[-5.92,-1.99,-5.92,-5.92,-5.92,-2.87,-5.92,-5.92,-1.81,-5.92,-0.48,-5.92],[-1.25,-5.86,-5.86,-1.6,-5.86,-5.86,-5.86,-1.47,-5.86,-5.86,-1.35,-5.86],[-2.63,-5.68,-1.74,-5.68,-5.68,-0.32,-5.68,-5.68,-5.68,-5.68,-5.68,-5.68],[-5.61,-5.61,-1.09,-5.61,-5.61,-0.66,-5.61,-5.61,-5.61,-2.17,-5.61,-5.61],[-1.06,-5.57,-0.95,-5.57,-5.57,-5.57,-2.13,-5.57,-5.57,-2.13,-5.57,-5.57],[-2.52,-5.57,-5.57,-0.77,-5.57,-5.57,-5.57,-5.57,-5.57,-0.86,-5.57,-5.57],[-1.02,-5.53,-5.53,-2.48,-5.53,-5.53,-5.53,-2.1,-5.53,-0.91,-5.53,-5.53],[-5.49,-5.49,-1.56,-5.49,-5.49,-0.47,-5.49,-5.49,-2.05,-5.49,-5.49,-5.49],[-5.4,-3.0,-5.4,-5.4,-5.4,-5.4,-5.4,-0.89,-5.4,-5.4,-0.69,-5.4],[-1.14,-5.4,-5.4,-0.53,-5.4,-5.4,-5.4,-5.4,-5.4,-3.0,-5.4,-5.4],[-0.96,-5.36,-5.36,-5.36,-5.36,-0.56,-5.36,-5.36,-5.36,-5.36,-5.36,-5.36]],"F":[-1.89,-1.91,-2.55,-1.72,-2.58,-1.62,-2.89,-3.01,-3.67,-8.98,-4.58,-8.98,-4.58,-4.87,-8.98,-6.58,-8.98,-8.98,-8.98,-5.54,-5.54,-8.98,-8.98,-8.98,-8.98,-8.98,-6.58,-8.98,-8.98,-8.98,-8.98,-8.98,-8.98,-8.98],"S":[-1.46,-2.42,-2.17,-2.28,-2.63,-2.59,-2.85,-3.91,-3.77,-3.35,-4.53,-3.84,-4.68,-4.39,-5.35,-4.86,-5.74,-4.53,-4.86,-4.39,-4.68,-4.68,-4.28,-5.35,-4.53,-5.07,-5.74,-5.07,-6.39,-5.35,-8.79,-8.79,-5.35,-5.74]}},"tunes":[{"name":"the Tune (Part 12's melody), in C major","tonic":0,"mode":"major","soprano":[72,72,79,79,81,81,79,77,77,76,76,74,74,72],"fermatas":[6,13],"bach":null},{"name":"the Passion Chorale, first two phrases (Bach, 1727)","tonic":9,"mode":"minor","soprano":[64,69,67,65,64,62,62,64,71,72,71,72,71,69,69,69],"fermatas":[7,13],"bach":[[64,60,57,57],[69,60,57,53],[67,64,60,52],[65,57,62,50],[64,60,55,48],[62,60,57,42],[62,59,55,43],[64,60,55,48],[71,64,59,44],[72,64,57,45],[71,65,57,50],[72,64,57,52],[71,62,56,40],[69,60,52,45],[69,60,52,45],[69,60,52,45]],"bach_names":["i","VI","III","iv","III","IV7","VII","III","V","i","iiø7","i","V7","i","i","i"]}]};
  var RANGES17 = [[60, 81], [55, 74], [48, 69], [40, 62]];
  function voicings17(s, members, tonic, lead) {
    var pcs = members.map(function (m) { return (tonic + m) % 12; }), out = [], a, t, b;
    var need = [pcs[0], pcs[1]].concat(pcs.length === 4 ? [pcs[3]] : []);
    if (pcs.indexOf(s % 12) < 0) return out;
    for (a = RANGES17[1][0]; a <= RANGES17[1][1]; a++) {
      if (pcs.indexOf(a % 12) < 0 || a > s || s - a > 12) continue;
      for (t = RANGES17[2][0]; t <= RANGES17[2][1]; t++) {
        if (pcs.indexOf(t % 12) < 0 || t > a || a - t > 12) continue;
        for (b = RANGES17[3][0]; b <= RANGES17[3][1]; b++) {
          if (pcs.indexOf(b % 12) < 0 || b > t || t - b > 24) continue;
          var ch = [s, a, t, b], have = ch.map(function (p) { return p % 12; }), ok = true, k, nl = 0;
          for (k = 0; k < need.length; k++) if (have.indexOf(need[k]) < 0) ok = false;
          for (k = 0; k < 4; k++) if (have[k] === lead) nl++;
          if (ok && nl <= 1) out.push(ch);
        }
      }
    }
    return out;
  }
  var PAIRS17 = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]];
  function parallels17(p, c) {
    var n = 0, k;
    for (k = 0; k < 6; k++) {
      var i = PAIRS17[k][0], j = PAIRS17[k][1], v0 = ((p[i] - p[j]) % 12 + 12) % 12, v1 = ((c[i] - c[j]) % 12 + 12) % 12;
      if (p[i] !== c[i] && p[j] !== c[j] && v0 === v1 && (v0 === 0 || v0 === 7) && (c[i] > p[i]) === (c[j] > p[j])) n++;
    }
    return n;
  }
  function harmonize17(tune, w) {
    var M = HZ17.models[tune.mode], tonic = tune.tonic, lead = (tonic + 11) % 12, n = tune.soprano.length, layers = [], k, i, j;
    var fer = {}; tune.fermatas.forEach(function (f) { fer[f] = 1; });
    for (k = 0; k < n; k++) {
      var s = tune.soprano[k], deg = ((s - tonic) % 12 + 12) % 12, order = [];
      for (i = 0; i < M.names.length; i++) order.push(i);
      order.sort(function (x, y) { return M.E[y][deg] - M.E[x][deg]; });
      var opts = [];
      order.slice(0, 14).forEach(function (si) {
        if (M.members[si].indexOf(deg) < 0) return;
        voicings17(s, M.members[si], tonic, lead).forEach(function (ch) { opts.push({ s: si, ch: ch }); });
      });
      layers.push(opts);
    }
    function unary(k, o) {
      var u = -M.E[o.s][((o.ch[0] - tonic) % 12 + 12) % 12], root = (tonic + M.members[o.s][0]) % 12;
      if (o.ch[3] % 12 !== root) u += 0.4;
      for (var q = 0; q < 3; q++) if (o.ch[q] === o.ch[q + 1]) u += 1.0;
      var mem = M.members[o.s];
      if (mem.length === 3 && ((mem[1] - mem[0] + 12) % 12) === 4 && ((mem[2] - mem[0] + 12) % 12) === 7) {
        var third = (tonic + mem[1]) % 12, nt = 0;
        for (q = 0; q < 4; q++) if (o.ch[q] % 12 === third) nt++;
        if (nt >= 2) u += 0.6;                                      // a doubled major third
      }
      if (fer[k] || k === n - 1) u -= 2.0 * M.F[o.s];
      if (k === 0) u -= M.S[o.s];
      if (k === n - 1) u += 4.0 * (M.members[o.s][0] !== 0) + 2.0 * (o.ch[3] % 12 !== tonic % 12);
      return u;
    }
    var cost = layers[0].map(function (o) { return unary(0, o); }), back = [];
    for (k = 1; k < n; k++) {
      var prev = layers[k - 1], cur = layers[k], nc = [], bk = [];
      for (j = 0; j < cur.length; j++) {
        var c = cur[j].ch, best = 1e18, arg = 0;
        for (i = 0; i < prev.length; i++) {
          var p = prev[i].ch;
          var x = cost[i] - w.chord * M.T[prev[i].s][cur[j].s] + w.motion * (Math.abs(c[1] - p[1]) + Math.abs(c[2] - p[2])) + 0.02 * Math.abs(c[3] - p[3]);
          if (x >= best) continue;
          x += w.parallel * parallels17(p, c);
          if (Math.abs(c[1] - p[1]) > 4) x += 0.6;
          if (Math.abs(c[2] - p[2]) > 4) x += 0.6;
          for (var q = 0; q < 3; q++) if (c[q + 1] > p[q] || c[q] < p[q + 1]) { x += 1.0; break; }
          var vs = ((c[0] - c[3]) % 12 + 12) % 12, vp = ((p[0] - p[3]) % 12 + 12) % 12;            // hidden fifths and octaves, outer voices
          if (c[0] !== p[0] && c[3] !== p[3] && (c[0] > p[0]) === (c[3] > p[3]) && (vs === 0 || vs === 7) && vs !== vp && Math.abs(c[0] - p[0]) > 2) x += 1.5;
          for (q = 0; q < 4; q += 3) if (p[q] % 12 === lead && c[q] % 12 === tonic % 12 && c[q] - p[q] !== 1) x += 3.0;
          var pm = M.members[prev[i].s];
          if (pm.length === 4) {
            var sev = (tonic + pm[3]) % 12;
            for (q = 0; q < 4; q++) { var dq = c[q] - p[q]; if (p[q] % 12 === sev && !(dq >= -2 && dq < 0) && dq !== 0) x += 3.0; }
          }
          if (prev[i].s === cur[j].s && p[3] === c[3]) x += 1.0;
          if (x < best) { best = x; arg = i; }
        }
        nc.push(best + unary(k, cur[j]));
        bk.push(arg);
      }
      cost = nc; back.push(bk);
    }
    var jbest = 0;
    for (j = 1; j < cost.length; j++) if (cost[j] < cost[jbest]) jbest = j;
    var path = [jbest];
    for (k = back.length - 1; k >= 0; k--) { jbest = back[k][jbest]; path.push(jbest); }
    path.reverse();
    return path.map(function (pj, k) { return layers[k][pj]; });
  }
  function chordsSound17(chords) {
    var rate = 44100, beat = 0.62, out = new Float32Array(Math.floor((chords.length * beat + 1.0) * rate)), k, v, n, h;
    for (k = 0; k < chords.length; k++) for (v = 0; v < 4; v++) {
      var hz = 440 * Math.pow(2, (chords[k][v] - 69) / 12), start = Math.floor(k * beat * rate), len = Math.floor((beat + 0.25) * rate);
      for (n = 0; n < len && start + n < out.length; n++) {
        var t = n / rate, y = 0;
        for (h = 1; h <= 5; h++) y += Math.sin(2 * Math.PI * hz * h * t) * Math.pow(0.7, h - 1);
        out[start + n] += 0.05 * y * Math.min(1, t / 0.03, (len - n) / (0.08 * rate));
      }
    }
    return play(out, rate);
  }
  function roll17(ax, chords, bad) {
    var cols = [C.idea, "#F472B6", "#A3E635", "#7DD3FC"], xs = [], v, k;
    for (k = 0; k < chords.length; k++) xs.push(k + 1);
    for (k = 0; k < bad.length; k++) ax.line([bad[k] + 0.5, bad[k] + 0.5], [38, 84], { color: C.loss, width: 2 });
    for (v = 0; v < 4; v++) {
      var ys = chords.map(function (c) { return c[v]; });
      ax.line(xs, ys, { color: cols[v], width: 1.6 });
      ax.dots(xs, ys, { color: cols[v], r: 3.2 });
    }
  }
  function stats17(chords) {
    var par = [], mot = 0, k;
    for (k = 1; k < chords.length; k++) {
      if (parallels17(chords[k - 1], chords[k])) par.push(k);
      mot += Math.abs(chords[k][1] - chords[k - 1][1]) + Math.abs(chords[k][2] - chords[k - 1][2]);
    }
    return { par: par, motion: mot / Math.max(1, chords.length - 1) };
  }

  W.fourpart = function (el) {
    QB.widget(el, {
      title: "A harmonizer you can steer",
      sub: "The film's harmonizer, running in the page: a tune, one note a beat; for every beat a chord that holds the tune's note and a voicing for alto, tenor and bass, all chosen together by the Viterbi algorithm. The chord model was learned from 280 of Bach's chorales. Move the sliders to change what the search cares about. Left: its harmonization (soprano gold, alto pink, tenor green, bass blue; red lines are parallel fifths or octaves). Right: Bach's own setting where there is one, or the same search with no rules at all.",
      panels: 2, height: 300,
      controls: [
        { k: "tune", label: "The tune (0: the Tune's first two phrases; 1: the Passion Chorale's, which the model never saw)", min: 0, max: 1, step: 1, value: 1 },
        { k: "parallel", label: "Penalty for each parallel fifth or octave", min: 0, max: 8, step: 0.5, value: 6 },
        { k: "motion", label: "Penalty for each semitone the alto and tenor move", min: 0, max: 0.6, step: 0.05, value: 0.05 },
        { k: "chord", label: "Weight on Bach's chord-to-chord habits", min: 0, max: 2, step: 0.1, value: 1 },
      ],
      buttons: [
        { label: "Play the harmonization", act: function (s) { s.sound = chordsSound17(s.ours); } },
        { label: "Play the right-hand one", act: function (s) { s.sound = chordsSound17(s.other); } },
      ],
      init: function (s) { s.sound = null; s.ours = []; s.other = []; },
      draw: function (g, v, s) {
        var tune = HZ17.tunes[v.tune], M = HZ17.models[tune.mode];
        var res = harmonize17(tune, { parallel: v.parallel, motion: v.motion, chord: v.chord });
        s.ours = res.map(function (o) { return o.ch; });
        s.names = res.map(function (o) { return M.names[o.s]; });
        if (tune.bach) { s.other = tune.bach; s.otherNames = tune.bach_names; s.otherTitle = "Bach, 1727"; }
        else {
          var plain = harmonize17(tune, { parallel: 0, motion: v.motion, chord: v.chord });
          s.other = plain.map(function (o) { return o.ch; }); s.otherNames = plain.map(function (o) { return M.names[o.s]; }); s.otherTitle = "the same search, parallels free";
        }
        s.st = stats17(s.ours); s.st2 = stats17(s.other);
        var n = s.ours.length;
        var a = g[0].axes({ x: [0.5, n + 0.5], y: [38, 84], title: "The search", xlabel: "beat", ylabel: "key number", xticks: [1, 4, 8, 12, 16].filter(function (x) { return x <= n; }) });
        roll17(a, s.ours, s.st.par);
        var b = g[1].axes({ x: [0.5, n + 0.5], y: [38, 84], title: s.otherTitle, xlabel: "beat", ylabel: "key number", xticks: [1, 4, 8, 12, 16].filter(function (x) { return x <= n; }) });
        roll17(b, s.other, s.st2.par);
        var same = 0;
        for (var k = 0; k < n; k++) if (tune.bach && s.names[k] === s.otherNames[k]) same++;
        s.same = tune.bach ? same + " of " + n + " beats" : "-";
      },
      readout: function (v, s) {
        return [["the search's chords", s.names.join(" ")],
                ["the right-hand chords", s.otherNames.join(" ")],
                ["parallel fifths and octaves", s.st.par.length + " (right: " + s.st2.par.length + ")"],
                ["alto and tenor motion, semitones a beat", fmt(s.st.motion, 1) + " (right: " + fmt(s.st2.motion, 1) + ")"],
                ["the same chord as Bach", s.same],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Set the parallel penalty to zero and red lines appear: Bach's chords, chosen by habit alone, move in fifths and octaves all the time. Raise the motion penalty and the inner voices freeze; lower it to zero and they wander. On the Passion Chorale the search agrees with Bach on about half the beats and never breaks the rule; what it cannot do, at any setting, is give the alto and tenor lines worth singing. (This page's search is the film's with its smaller penalties fixed.)"
    });
  };
})();
