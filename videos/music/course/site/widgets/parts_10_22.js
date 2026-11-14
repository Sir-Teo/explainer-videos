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
})();
