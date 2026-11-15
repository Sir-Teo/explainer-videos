// Interactives for Act VI's last parts and Act VII (Parts 38-52).  As before, each can be heard: the sound is computed in
// the page and played through the browser's Web Audio after a click.  Nothing is downloaded.
(function () {
  "use strict";
  var C = QB.C, W = QB.W;
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

  // ---- Part 38: the swing model -----------------------------------------------------------------------------------
  function ratio38(bpm) { return Math.min(3.5, Math.max(1, 3 + (1 - 3) * (bpm - 120) / (300 - 120))); }
  function times38(eighths, bpm, r, delay) {
    var beat = 60 / bpm;
    return eighths.map(function (e) {
      var b = Math.floor(e / 2), on = e % 2 === 0;
      return (b + (on ? 0 : r / (1 + r))) * beat + (on ? delay / 1000 : 0);
    });
  }
  function ping38(out, t0, rate, gain, f) {
    var i0 = Math.floor(t0 * rate), fs = [f, f * 2.41, f * 3.97, f * 5.63], dec = [7, 9, 12, 15];
    for (var j = 0; j < 0.5 * rate && i0 + j < out.length; j++) {
      var t = j / rate, v = 0;
      for (var k = 0; k < 4; k++) v += Math.exp(-dec[k] * t) * Math.sin(2 * Math.PI * fs[k] * t) / (k + 1);
      out[i0 + j] += gain * v * Math.min(1, t / 0.001);
    }
  }
  function pluck38(out, t0, rate, m, dur, gain) {
    var f = hz(m), i0 = Math.floor(t0 * rate), n = Math.floor(dur * rate);
    for (var j = 0; j < n && i0 + j < out.length; j++) {
      var t = j / rate, env = Math.exp(-3 * t) * Math.min(1, t / 0.004) * Math.min(1, (n - j) / rate / 0.03);
      out[i0 + j] += gain * env * (Math.sin(2 * Math.PI * f * t) + 0.4 * Math.sin(4 * Math.PI * f * t) + 0.15 * Math.sin(6 * Math.PI * f * t));
    }
  }
  var LINE38 = [[76, 0], [79, 1], [81, 2], [79, 3], [76, 4], [74, 5], [72, 6], [74, 7], [76, 8], [72, 9], [69, 10], [72, 11], [74, 12], [76, 13], [72, 14]];
  var BASS38 = [48, 52, 55, 57, 53, 57, 60, 58, 48, 52, 55, 52, 43, 47, 50, 49];

  W.swing = function (el) {
    QB.widget(el, {
      title: "Swing, modelled: the long-short ratio against tempo",
      sub: "Choose a tempo. The model sets the swung eighths' ratio, 3:1 at 120 beats a minute falling in a straight line to 1:1 at 300, the trend measured on jazz drummers' ride cymbals. Add a delay to the line's on-beat notes, as soloists do, and hear the ride pattern, a walking bass and a line together.",
      panels: 2, height: 230,
      controls: [
        { k: "bpm", label: "Tempo", min: 80, max: 320, step: 5, value: 160, fmt: function (x) { return x + " a minute"; } },
        { k: "delay", label: "Line's downbeats late by", min: 0, max: 60, step: 5, value: 0, fmt: function (x) { return x + " ms"; } },
        { k: "override", label: "Ratio (0 = the model's)", min: 0, max: 4, step: 0.25, value: 0, fmt: function (x) { return x === 0 ? "model" : x.toFixed(2) + " : 1"; } }
      ],
      buttons: [{ label: "Play four bars", act: function (s) {
        var rate = 44100, bpm = s.v.bpm, r = s.r, beat = 60 / bpm, n = Math.floor((16 * beat + 1) * rate), out = new Float32Array(n);
        var ride = [0, 2, 3, 4, 6, 7], b, i, ts;
        for (b = 0; b < 4; b++) {
          ts = times38(ride, bpm, r, 0);
          for (i = 0; i < ts.length; i++) ping38(out, b * 4 * beat + ts[i], rate, 0.05, 3300);
        }
        for (i = 0; i < 16; i++) pluck38(out, i * beat, rate, BASS38[i] - 12, beat * 0.95, 0.22);
        for (var rep = 0; rep < 2; rep++) {
          ts = times38(LINE38.map(function (x) { return x[1]; }), bpm, r, s.v.delay);
          for (i = 0; i < LINE38.length; i++) {
            var nxt = i + 1 < ts.length ? ts[i + 1] : ts[i] + beat;
            pluck38(out, rep * 8 * beat + ts[i], rate, LINE38[i][0], Math.max(0.1, (nxt - ts[i]) * 0.95), 0.16);
          }
        }
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        s.v = v;
        s.r = v.override > 0 ? v.override : ratio38(v.bpm);
        var xs = [], ys = [], ms = [], b;
        for (b = 80; b <= 320; b += 5) { xs.push(b); ys.push(ratio38(b)); ms.push(1000 * 60 / b / (1 + ratio38(b))); }
        var a = g[0].axes({ x: [80, 320], y: [0.8, 3.6], title: "The model's ratio (gold) and the short note in ms / 50 (blue)", xlabel: "beats a minute" });
        a.line(xs, ys, { color: C.idea, width: 2.5 });
        a.line(xs, ms.map(function (x) { return x / 50; }), { color: "#60A5FA", width: 2 });
        a.dots([v.bpm], [s.r], { r: 6, color: "#F472B6" });
        var beat = 60 / v.bpm, ts = times38([0, 1, 2, 3, 4, 5, 6, 7], v.bpm, s.r, v.delay);
        var a2 = g[1].axes({ x: [0, 4], y: [0, 1], title: "One bar: beats (grey) and the line's eighths (pink)", xlabel: "beats" });
        for (b = 0; b <= 4; b++) a2.line([b, b], [0.1, 0.9], { color: "#8A93A0", width: 1 });
        a2.dots(ts.map(function (t) { return t / beat; }), ts.map(function () { return 0.5; }), { r: 6, color: "#F472B6" });
      },
      readout: function (v, s) {
        var r = s.r, beat = 60 / v.bpm;
        return [["long : short", r.toFixed(2) + " : 1" + (v.override > 0 ? " (yours)" : " (the model's)")],
                ["the long and short notes", (1000 * beat * r / (1 + r)).toFixed(0) + " ms and " + (1000 * beat / (1 + r)).toFixed(0) + " ms"],
                ["downbeat delay", v.delay + " ms, " + (100 * v.delay / 1000 / beat).toFixed(0) + "% of a beat"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Past about 160 beats a minute the model's short note hardly changes, near a tenth of a second: as the tempo rises, the long note shrinks instead. Try a fixed 2:1 (the textbook triplet) at 260 and hear it lurch."
    });
  };
  // ---- Part 39: the bebop scale --------------------------------------------------------------------------------------
  var NN39 = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"];
  var Q39 = [["dominant seventh", [0, 4, 7, 10], [0, 2, 4, 5, 7, 9, 10], 11], ["sixth", [0, 4, 7, 9], [0, 2, 4, 5, 7, 9, 11], 8],
             ["minor seventh", [0, 3, 7, 10], [0, 2, 3, 5, 7, 9, 10], 11]];
  function run39(scale, start, dir, n) {
    var out = [start], m = start;
    for (var i = 1; i < n; i++) {
      m += dir;
      while (scale.indexOf(((m % 12) + 12) % 12) < 0) m += dir;
      out.push(m);
    }
    return out;
  }
  W.bebop = function (el) {
    QB.widget(el, {
      title: "The bebop scale: chord tones on every beat",
      sub: "Pick a chord and run its scale in eighth notes from one of its chord tones on a beat. The plain mode has seven notes, and after an octave the beats slip onto non-chord tones; add the bebop scale's chromatic passing tone and the four chord tones alternate with four others for ever. Try the minor seventh to see where the trick needs a different passing tone.",
      panels: 1, height: 230,
      controls: [
        { k: "root", label: "Root", min: 0, max: 11, step: 1, value: 0, fmt: function (x) { return NN39[x]; } },
        { k: "kind", label: "Chord", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return Q39[x][0]; } },
        { k: "from", label: "Start on chord tone", min: 0, max: 3, step: 1, value: 3, fmt: function (x) { return ["root", "third", "fifth", "seventh / sixth"][x]; } },
        { k: "dir", label: "Direction", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "up" : "down"; } },
        { k: "bebop", label: "Scale", min: 0, max: 1, step: 1, value: 1, fmt: function (x) { return x ? "bebop (8 notes)" : "plain (7 notes)"; } }
      ],
      buttons: [{ label: "Play the run", act: function (s) {
        var rate = 44100, e = 0.2, n = Math.floor((s.line.length * e + 1.5) * rate), out = new Float32Array(n), i, j;
        s.chord.forEach(function (p) {
          var f = hz(48 + p), i0 = 0;
          for (j = 0; j < n; j++) { var t = j / rate; out[j] += 0.05 * Math.exp(-0.6 * t) * Math.sin(2 * Math.PI * f * t); }
        });
        s.line.forEach(function (m, k) {
          var f = hz(m), i0 = Math.floor(k * e * rate);
          for (j = 0; j < 0.25 * rate && i0 + j < n; j++) {
            var t = j / rate, env = Math.exp(-6 * t) * Math.min(1, t / 0.004);
            out[i0 + j] += 0.18 * env * (Math.sin(2 * Math.PI * f * t) + 0.3 * Math.sin(4 * Math.PI * f * t));
          }
        });
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        var q = Q39[v.kind], r = v.root;
        var chord = q[1].map(function (i) { return (r + i) % 12; });
        var scale = q[2].map(function (i) { return (r + i) % 12; });
        if (v.bebop) scale = scale.concat([(r + q[3]) % 12]);
        var startPc = chord[v.from], start = 60 + ((startPc - 60) % 12 + 12) % 12 + (v.dir ? 0 : 12);
        var line = run39(scale, start, v.dir ? 1 : -1, 16);
        s.line = line; s.chord = chord;
        var a = g[0].axes({ x: [-0.5, 15.5], y: [Math.min.apply(null, line) - 2, Math.max.apply(null, line) + 2], title: "Sixteen eighth notes: beats are the even positions (big dots); gold = chord tone on a beat, pink = not", xlabel: "eighth note" });
        var bx = [], by = [], gx = [], gy = [], ox = [], oy = [];
        line.forEach(function (m, k) {
          if (k % 2 === 0) { if (chord.indexOf(m % 12) >= 0) { gx.push(k); gy.push(m); } else { bx.push(k); by.push(m); } }
          else { ox.push(k); oy.push(m); }
        });
        a.line(line.map(function (_, k) { return k; }), line, { color: "#3A4250", width: 1.5 });
        a.dots(ox, oy, { r: 3, color: "#8A93A0" });
        a.dots(gx, gy, { r: 7, color: C.idea });
        a.dots(bx, by, { r: 7, color: "#F472B6" });
        s.hits = gx.length;
      },
      readout: function (v, s) {
        return [["notes", s.line.map(function (m) { return NN39[m % 12]; }).join(" ")],
                ["beats on chord tones", s.hits + " of 8"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "With the plain mode the run keeps chord tones on the beats for about an octave and then slips. The bebop scale's extra note makes the cycle eight long, so the alternation never breaks, from any chord tone, in either direction."
    });
  };
  // ---- Part 40: a step sequencer with drum-machine voices --------------------------------------------------------------
  var PAT40 = {
    rock: { kick: [0, 8, 10], snare: [4, 12], hat: [0, 2, 4, 6, 8, 10, 12, 14], open: [] },
    funk: { kick: [0, 3, 10], snare: [4, 7, 12, 15], hat: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], open: [] },
    disco: { kick: [0, 4, 8, 12], snare: [4, 12], hat: [0, 4, 8, 12], open: [2, 6, 10, 14] },
    house: { kick: [0, 4, 8, 12], snare: [4, 12], hat: [], open: [2, 6, 10, 14] },
    trap: { kick: [0, 7, 10], snare: [8], hat: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], open: [] }
  };
  var STYLES40 = ["rock", "funk", "disco", "house", "trap"];
  var HAT40 = [205.3, 304.4, 369.6, 522.7, 540, 800];
  function kick40(out, i0, rate, decay, gain) {
    var ph = 0;
    for (var j = 0; j < 5 * decay * rate && i0 + j < out.length; j++) {
      var t = j / rate, f = 52 * (1 + 0.6 * Math.exp(-t / 0.02));
      ph += 2 * Math.PI * f / rate;
      out[i0 + j] += gain * Math.sin(ph) * Math.exp(-t / decay) * Math.min(1, t / 0.0005);
    }
  }
  function noise40(out, i0, rate, dur, decay, gain, hp) {
    var prev = 0, prevy = 0, a = Math.exp(-2 * Math.PI * hp / rate);
    for (var j = 0; j < dur * rate && i0 + j < out.length; j++) {
      var x = Math.random() * 2 - 1, y = a * (prevy + x - prev);
      prev = x; prevy = y;
      out[i0 + j] += gain * y * Math.exp(-j / rate / decay);
    }
  }
  function hat40(out, i0, rate, open, gain) {
    var dur = open ? 0.5 : 0.08, decay = open ? 0.18 : 0.022, prev = 0, prevy = 0, a = Math.exp(-2 * Math.PI * 7000 / rate);
    for (var j = 0; j < dur * rate && i0 + j < out.length; j++) {
      var t = j / rate, x = 0;
      for (var k = 0; k < 6; k++) x += Math.sin(2 * Math.PI * HAT40[k] * t + 0.7 * k) > 0 ? 1 : -1;
      var y = a * (prevy + x - prev); prev = x; prevy = y;
      out[i0 + j] += gain * 0.25 * y * Math.exp(-t / decay);
    }
  }
  W.steps = function (el) {
    QB.widget(el, {
      title: "A step sequencer with drum-machine voices",
      sub: "Five beats on the sixteen-step grid of a drum machine, played by voices built the way the 808's circuits work: a struck resonator for the kick, noise for the clap, six square waves for the hats. Choose a style, the tempo, the swing and the kick's decay; then play two bars.",
      panels: 1, height: 220,
      controls: [
        { k: "style", label: "Style", min: 0, max: 4, step: 1, value: 0, fmt: function (x) { return STYLES40[x]; } },
        { k: "bpm", label: "Tempo", min: 70, max: 160, step: 2, value: 112, fmt: function (x) { return x + " a minute"; } },
        { k: "swing", label: "Swing", min: 50, max: 70, step: 1, value: 50, fmt: function (x) { return x + "%"; } },
        { k: "decay", label: "Kick decay", min: 0.1, max: 1.5, step: 0.05, value: 0.45, fmt: function (x) { return x.toFixed(2) + " s"; } }
      ],
      buttons: [{ label: "Play two bars", act: function (s) {
        var v = s.v, p = PAT40[STYLES40[v.style]], rate = 44100, step = 60 / v.bpm / 4;
        var n = Math.floor((32 * step + 1.5) * rate), out = new Float32Array(n);
        function at(st, bar) { return Math.floor((bar * 16 * step + (2 * Math.floor(st / 2) + (st % 2 ? 2 * v.swing / 100 : 0)) * step) * rate); }
        for (var bar = 0; bar < 2; bar++) {
          p.kick.forEach(function (st) { kick40(out, at(st, bar), rate, v.decay, 0.5); });
          p.snare.forEach(function (st) { noise40(out, at(st, bar), rate, 0.25, 0.06, 0.35, 900); });
          p.hat.forEach(function (st) { hat40(out, at(st, bar), rate, false, 0.15); });
          p.open.forEach(function (st) { hat40(out, at(st, bar), rate, true, 0.12); });
        }
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        s.v = v;
        var p = PAT40[STYLES40[v.style]];
        var a = g[0].axes({ x: [-0.5, 15.5], y: [-0.5, 3.5], title: STYLES40[v.style] + ": kick, snare / clap, hat, open hat (dots: hits; grey lines: beats)", xlabel: "step" });
        for (var b = 0; b <= 4; b++) a.line([4 * b - 0.5, 4 * b - 0.5], [-0.5, 3.5], { color: "#3A4250", width: 1 });
        var rows = [["kick", 3, C.idea], ["snare", 2, "#F472B6"], ["hat", 1, "#8A93A0"], ["open", 0, "#60A5FA"]];
        rows.forEach(function (r) {
          var xs = p[r[0]].map(function (st) { return st + (st % 2 ? 2 * (v.swing - 50) / 100 : 0); });
          a.dots(xs, xs.map(function () { return r[1]; }), { r: 7, color: r[2] });
        });
      },
      readout: function (v, s) {
        var p = PAT40[STYLES40[v.style]];
        var back = p.snare.filter(function (x) { return x === 4 || x === 12; }).length / p.snare.length;
        return [["backbeat", Math.round(100 * back) + "% of snare hits on beats 2 and 4"],
                ["kick", "52 Hz, falling 60 dB in " + (v.decay * Math.log(1000)).toFixed(2) + " s"],
                ["swing", v.swing + "%: the off sixteenths fall " + (v.swing - 50) * 2 + "% of a sixteenth late"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Disco and house put the kick on every beat; trap moves the snare to beat three, so the beat feels half as fast as its hats. Try funk at 58% swing, and the kick's decay long enough to become a bass note."
    });
  };
  // ---------------------------------------------------------------- Part 41: orchestration as additive synthesis
  var PROF41 = {"flute": [0.0, -20.8, -11.5, -21.5, -17.5, -23.6, -24.5, -26.1, -29.3, -27.5, -35.9, -30.9, -31.9, -32.9, -33.9, -34.9], "clarinet": [0.0, -20.1, -1.9, -18.2, -4.3, -18.4, -7.0, -19.7, -9.9, -21.5, -13.0, -23.7, -28.3, -32.9, -37.5, -42.1], "saxophone": [0.0, -4.5, -11.8, -21.7, -18.0, -22.1, -31.2, -34.2, -36.6, -40.5, -35.4, -32.0, -33.0, -34.0, -35.0, -36.0], "trumpet (soft)": [0.0, -18.9, -33.6, -48.5, -60.3, -65.3, -70.7, -69.0, -66.9, -68.9, -70.1, -65.6, -66.6, -67.6, -68.6, -69.6], "trumpet (loud)": [0.0, -2.0, -5.9, -13.2, -13.6, -15.7, -20.8, -22.5, -25.0, -33.7, -41.2, -43.2, -49.3, -55.3, -61.4, -67.5], "horn": [0.0, -12.9, -27.6, -42.5, -54.3, -59.3, -64.7, -63.0, -60.9, -62.9, -64.1, -59.6, -60.6, -61.6, -62.6, -63.6], "violin": [0.0, -5.5, -10.4, -12.2, -13.4, -13.3, -13.3, -13.9, -14.1, -39.1, -18.4, -22.8, -25.7, -28.6, -31.5, -34.4]};
  var NAMES41 = Object.keys(PROF41);
  var STEPS41 = [0, 12, 19, 24, 28, 31, 34, 36];     // semitones above the melody note to harmonics 1..8 (tempered)
  function parts41(v) {
    var f0 = 261.63, out = [];
    PROF41[NAMES41[v.a]].forEach(function (db, k) { out.push([f0 * (k + 1), Math.pow(10, db / 20), 0]); });
    var f1 = f0 * Math.pow(2, (STEPS41[v.h - 1] + v.off / 100) / 12), g = Math.pow(10, v.g / 20);
    PROF41[NAMES41[v.b]].forEach(function (db, k) { out.push([f1 * (k + 1), g * Math.pow(10, db / 20), 1]); });
    return out;
  }
  W.orchestra = function (el) {
    QB.widget(el, {
      title: "Ravel's trick: one instrument on another's harmonic",
      sub: "A melody instrument on middle C, with its sixteen harmonics measured from the series' physical models, and a second instrument placed on one of its harmonics, quieter. When every partial of the second lands on the first's harmonic series, the two fuse into one new colour, as Boléro's horn, celesta and piccolos do. Detune the second and they come apart.",
      panels: 1, height: 240,
      controls: [
        { k: "a", label: "Melody", min: 0, max: NAMES41.length - 1, step: 1, value: 5, fmt: function (x) { return NAMES41[x]; } },
        { k: "b", label: "Added", min: 0, max: NAMES41.length - 1, step: 1, value: 0, fmt: function (x) { return NAMES41[x]; } },
        { k: "h", label: "On harmonic", min: 1, max: 8, step: 1, value: 3, fmt: function (x) { return x + " (+" + STEPS41[x - 1] + " semitones)"; } },
        { k: "g", label: "Its level", min: -30, max: 0, step: 1, value: -11, fmt: function (x) { return x + " dB"; } },
        { k: "off", label: "Detune", min: -100, max: 100, step: 5, value: 0, fmt: function (x) { return x + " cents"; } }
      ],
      buttons: [{ label: "Play: melody alone, then with the added part", act: function (s) {
        var rate = 44100, d = 1.6, n = Math.floor((2 * d + 0.5) * rate), out = new Float32Array(n), ps = parts41(s.v);
        for (var half = 0; half < 2; half++) {
          var i0 = Math.floor(half * (d + 0.4) * rate);
          ps.forEach(function (p, j) {
            if (p[2] === 1 && half === 0) return;
            if (p[0] > 18000) return;
            var ph = (j * 2.39996) % 6.283;
            for (var i = 0; i < d * rate; i++) {
              var t = i / rate, env = Math.min(1, t / 0.06) * Math.min(1, (d - t) / 0.1);
              out[i0 + i] += 0.08 * p[1] * env * Math.sin(2 * Math.PI * p[0] * t + ph);
            }
          });
        }
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        s.v = v;
        var ps = parts41(v), f0 = 261.63;
        var a = g[0].axes({ x: [0, 17], y: [-60, 3], title: "Partials in harmonics of C4 (gold: melody, blue: added part; grey lines: the series)", xlabel: "frequency / 261.6 Hz" });
        for (var k = 1; k <= 16; k++) a.line([k, k], [-60, 3], { color: "#3A4250", width: 1 });
        [0, 1].forEach(function (w) {
          var q = ps.filter(function (p) { return p[2] === w && p[0] / f0 < 17; });
          a.bars(q.map(function (p) { return p[0] / f0; }), q.map(function (p) { return Math.max(-60, 20 * Math.log10(p[1])); }), 0.18, { color: w ? "#60A5FA" : C.idea, base: -60 });
        });
      },
      readout: function (v, s) {
        var ps = parts41(v), f0 = 261.63, tot = 0, on = 0, num = 0;
        ps.forEach(function (p) {
          var pw = p[1] * p[1], k = Math.max(1, Math.round(p[0] / f0));
          tot += pw; num += pw * p[0];
          if (Math.abs(1200 * Math.log2(p[0] / (k * f0))) <= 20) on += pw;
        });
        var alone = 0, an = 0;
        ps.filter(function (p) { return p[2] === 0; }).forEach(function (p) { alone += p[1] * p[1]; an += p[1] * p[1] * p[0]; });
        return [["fusion", Math.round(100 * on / tot) + "% of the power within 20 cents of C4's harmonic series"],
                ["brightness", "spectral centroid " + Math.round(an / alone) + " Hz alone, " + Math.round(num / tot) + " Hz together"],
                ["harmonic " + v.h, "a tempered note is " + (1200 * (STEPS41[v.h - 1] / 12) - 1200 * Math.log2(v.h)).toFixed(1) + " cents from the true harmonic"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Ravel put a celesta on the 4th harmonic and piccolos on the 3rd and 5th. Try harmonic 5: the tempered major third is 13.7 cents sharp of the true harmonic, and still fuses; now detune by 50 cents and hear two instruments again. Harmonic 7, a flat seventh, lies 31 cents from the nearest tempered note, and does not fuse."
    });
  };
  // ---------------------------------------------------------------- Part 42: operations on a motive
  var MAJ42 = [0, 2, 4, 5, 7, 9, 11];
  function deg42(m) { var pc = ((m % 12) + 12) % 12, o = Math.floor(m / 12), i = 0; for (var k = 0; k < 7; k++) if (MAJ42[k] <= pc) i = k; return 7 * o + i; }
  function key42(d) { var o = Math.floor(d / 7), r = ((d % 7) + 7) % 7; return 12 * o + MAJ42[r]; }
  function step42(m, k) { return key42(deg42(m) + k); }
  var MOT42 = [[64, 0, 0.5], [62, 0.5, 0.5], [60, 1, 1], [67, 2, 2]];
  var OPS42 = {
    "none": function (m) { return m; },
    "invert": function (m) { var ax = deg42(m[0][0]); return m.map(function (n) { return [key42(2 * ax - deg42(n[0])), n[1], n[2]]; }); },
    "retrograde": function (m) { var end = Math.max.apply(null, m.map(function (n) { return n[1] + n[2]; })); return m.map(function (n) { return [n[0], end - n[1] - n[2], n[2]]; }).sort(function (a, b) { return a[1] - b[1]; }); },
    "augment": function (m) { var a0 = m[0][1]; return m.map(function (n) { return [n[0], a0 + 2 * (n[1] - a0), 2 * n[2]]; }); },
    "diminish": function (m) { var a0 = m[0][1]; return m.map(function (n) { return [n[0], a0 + (n[1] - a0) / 2, n[2] / 2]; }); },
    "fragment": function (m) { return m.slice(0, 2); },
    "expand an interval": function (m) {
      var iv = [], i, best = 0; for (i = 1; i < m.length; i++) iv.push(deg42(m[i][0]) - deg42(m[i - 1][0]));
      for (i = 1; i < iv.length; i++) if (Math.abs(iv[i]) > Math.abs(iv[best])) best = i;
      var s = iv[best] >= 0 ? 1 : -1; return m.map(function (n, j) { return [j > best ? step42(n[0], s) : n[0], n[1], n[2]]; }); },
    "new rhythm": function (m) { var a0 = m[0][1], span = Math.max.apply(null, m.map(function (n) { return n[1] + n[2]; })) - a0; return m.map(function (n, j) { return [n[0], a0 + span * j / m.length, span / m.length]; }); },
    "embellish": function (m) {
      var out = []; m.forEach(function (n, j) {
        if (j + 1 < m.length && Math.abs(deg42(m[j + 1][0]) - deg42(n[0])) >= 2) {
          var k = deg42(m[j + 1][0]) - deg42(n[0]), s = k > 0 ? 1 : -1, len = Math.abs(k);
          for (var i = 0; i < len; i++) out.push([step42(n[0], s * i), n[1] + n[2] * i / len, n[2] / len]);
        } else out.push(n);
      }); return out; }
  };
  var ON42 = Object.keys(OPS42);
  var NN42 = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"];
  function apply42(v) {
    var m = OPS42[ON42[v.op2]](OPS42[ON42[v.op1]](MOT42.map(function (n) { return n.slice(); })));
    return m.map(function (n) { return [step42(n[0], v.k), n[1], n[2]]; });
  }
  function tone42(out, i0, rate, f, dur, g) {
    var n = Math.floor((dur + 0.4) * rate);
    for (var i = 0; i < n && i0 + i < out.length; i++) {
      var t = i / rate, e = Math.min(1, t / 0.005) * Math.exp(-t * 2.2) * (t < dur ? 1 : Math.exp(-(t - dur) * 12));
      out[i0 + i] += g * e * (Math.sin(2 * Math.PI * f * t) + 0.35 * Math.sin(4 * Math.PI * f * t) + 0.12 * Math.sin(6 * Math.PI * f * t));
    }
  }
  W.motive = function (el) {
    QB.widget(el, {
      title: "Operations on a motive",
      sub: "Our four-note motive (E D C, then up a fifth to G) under up to two of the classical operations, then moved along the C major scale. Every operation is diatonic: steps are counted on the scale, so the result stays in the key. Play the motive and then the result.",
      panels: 1, height: 230,
      controls: [
        { k: "op1", label: "First operation", min: 0, max: ON42.length - 1, step: 1, value: 1, fmt: function (x) { return ON42[x]; } },
        { k: "op2", label: "Second operation", min: 0, max: ON42.length - 1, step: 1, value: 0, fmt: function (x) { return ON42[x]; } },
        { k: "k", label: "Move along the scale", min: -7, max: 7, step: 1, value: 0, fmt: function (x) { return (x > 0 ? "+" : "") + x + " steps"; } }
      ],
      buttons: [{ label: "Play: motive, then result", act: function (s) {
        var rate = 44100, beat = 0.4, r = apply42(s.v);
        var endR = Math.max.apply(null, r.map(function (n) { return n[1] + n[2]; })), gap = 4 * beat + 0.6;
        var out = new Float32Array(Math.floor((gap + endR * beat + 1.2) * rate));
        MOT42.forEach(function (n) { tone42(out, Math.floor(n[1] * beat * rate), rate, 440 * Math.pow(2, (n[0] - 69) / 12), n[2] * beat, 0.25); });
        r.forEach(function (n) { tone42(out, Math.floor((gap + n[1] * beat) * rate), rate, 440 * Math.pow(2, (n[0] - 69) / 12), n[2] * beat, 0.25); });
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        s.v = v;
        var r = apply42(v), all = MOT42.concat(r).map(function (n) { return n[0]; });
        var lo = Math.min.apply(null, all) - 2, hi = Math.max.apply(null, all) + 2;
        var endR = Math.max.apply(null, r.map(function (n) { return n[1] + n[2]; }));
        var a = g[0].axes({ x: [-0.2, 4.6 + Math.max(4, endR)], y: [lo, hi], title: "The motive (grey) and the result (gold), key numbers against beats", xlabel: "beats" });
        MOT42.forEach(function (n) { a.line([n[1], n[1] + n[2] * 0.92], [n[0], n[0]], { color: "#8A93A0", width: 7 }); });
        a.line([4.3, 4.3], [lo, hi], { color: "#3A4250", width: 1 });
        r.forEach(function (n) { a.line([4.6 + n[1], 4.6 + n[1] + n[2] * 0.92], [n[0], n[0]], { color: C.idea, width: 7 }); });
      },
      readout: function (v, s) {
        var r = apply42(v);
        var names = r.map(function (n) { return NN42[n[0] % 12]; }).join(" ");
        var iv = []; for (var i = 1; i < r.length; i++) iv.push(r[i][0] - r[i - 1][0]);
        return [["result", names],
                ["intervals", iv.map(function (x) { return (x > 0 ? "+" : "") + x; }).join(", ") + " semitones"],
                ["length", Math.max.apply(null, r.map(function (n) { return n[1] + n[2]; })) - r[0][1] + " beats"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Inversion then retrograde gives the motive's retrograde inversion, the fourth form of a twelve-tone row (Part 29). Move the inverted motive along the scale and listen to its intervals change by a semitone here and there while it stays recognisable: that is what diatonic means."
    });
  };
  // ---------------------------------------------------------------- Part 43: two players correcting each other
  function gauss43(rnd) { var u = 0, v = 0; while (u === 0) u = rnd(); v = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
  function rng43(seed) { var s = seed >>> 0; return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
  function duo43(v, n) {
    var r = rng43(v.seed * 7919 + 17), on = [[0, 0]], mprev = [0, 0];
    var P = [0.5, 0.5 * (1 + v.diff / 100)], al = [v.a1, v.a2];
    for (var k = 1; k < n; k++) {
      var m = [gauss43(r) * 0.005, gauss43(r) * 0.005], row = [];
      for (var i = 0; i < 2; i++) {
        var j = 1 - i, T = P[i] + gauss43(r) * v.noise / 1000;
        row.push(on[k - 1][i] + T - al[i] * (on[k - 1][i] - on[k - 1][j]) + m[i] - mprev[i]);
      }
      mprev = m; on.push(row);
    }
    return on;
  }
  W.duo = function (el) {
    QB.widget(el, {
      title: "Two players keeping time",
      sub: "Each player has an inner timekeeper and corrects each note by a fraction (alpha) of the last asynchrony with the other. The asynchrony shrinks by 1 - (alpha 1 + alpha 2) each beat: it holds for totals between 0 and 2, drifts at 0, and shakes apart above 2. Give the players different tempos and some noise, and listen.",
      panels: 1, height: 240,
      controls: [
        { k: "a1", label: "Player 1 corrects", min: 0, max: 1.5, step: 0.05, value: 0.25, fmt: function (x) { return x.toFixed(2); } },
        { k: "a2", label: "Player 2 corrects", min: 0, max: 1.5, step: 0.05, value: 0.25, fmt: function (x) { return x.toFixed(2); } },
        { k: "diff", label: "Player 2's tempo", min: -5, max: 5, step: 0.5, value: 2, fmt: function (x) { return (x > 0 ? x + "% slower" : (x < 0 ? (-x) + "% faster" : "the same")); } },
        { k: "noise", label: "Timekeeper noise", min: 0, max: 30, step: 1, value: 12, fmt: function (x) { return x + " ms"; } },
        { k: "seed", label: "Random seed", min: 1, max: 20, step: 1, value: 1, fmt: function (x) { return "" + x; } }
      ],
      buttons: [{ label: "Play 32 beats", act: function (s) {
        var rate = 44100, on = duo43(s.v, 32), t0 = Math.min(on[0][0], on[0][1]);
        var end = Math.max.apply(null, on.map(function (r) { return Math.max(r[0], r[1]); })) - t0 + 0.8;
        if (!(end < 60)) { s.sound = false; return; }
        var out = new Float32Array(Math.floor(end * rate)), f = [523.25, 329.63];
        on.forEach(function (r) {
          for (var i = 0; i < 2; i++) {
            var i0 = Math.floor((r[i] - t0) * rate);
            for (var q = 0; q < 0.25 * rate && i0 + q < out.length; q++) { if (i0 + q < 0) continue; var tt = q / rate; out[i0 + q] += 0.2 * Math.exp(-tt * 14) * Math.sin(2 * Math.PI * f[i] * tt); }
          }
        });
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        s.v = v;
        var on = duo43(v, 32), asy = on.map(function (r) { return 1000 * (r[1] - r[0]); });
        var lim = Math.min(400, Math.max(60, Math.max.apply(null, asy.map(Math.abs)) * 1.1));
        var a = g[0].axes({ x: [0, 31], y: [-lim, lim], title: "Asynchrony, player 2 minus player 1 (ms), beat by beat", xlabel: "beat" });
        a.hline(0);
        a.line(asy.map(function (_, i) { return i; }), asy.map(function (x) { return Math.max(-lim, Math.min(lim, x)); }), { color: C.idea, width: 2 });
        a.dots(asy.map(function (_, i) { return i; }), asy.map(function (x) { return Math.max(-lim, Math.min(lim, x)); }), { r: 3, color: C.idea });
      },
      readout: function (v, s) {
        var tot = v.a1 + v.a2, b = 1 - tot;
        var state = tot <= 0 ? "no correction: the tempo difference accumulates" : (tot >= 2 ? "over-correction: unstable, it shakes apart" : "stable");
        var sd = (tot > 0 && tot < 2) ? Math.sqrt(2 * Math.pow(v.noise, 2) / (1 - b * b) + 4 * 25 / (1 + b)).toFixed(1) + " ms" : "infinite";
        var lag = (tot > 0 && tot < 2) ? (1000 * 0.5 * v.diff / 100 / tot).toFixed(0) + " ms steady lag from the tempo difference" : "none settles";
        return [["total correction", tot.toFixed(2) + ": " + state],
                ["spread (equal tempos)", sd],
                ["lag", lag],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available (or the duo fell apart)")]];
      },
      note: "With equal corrections of 0.25 and a 2% tempo difference the duo holds, with a steady lag. Set both to zero and the lag grows by 10 ms every beat. Let one player correct by 1.5 and the other by 0.6: the total passes 2 and every correction overshoots."
    });
  };
  // ---------------------------------------------------------------- Part 44: a tempo that hits three actions
  function scan44(v) {
    var hits = [v.h1, v.h2, v.h3], out = [], sols = [], prevOk = false, best = null;
    for (var b = 60; b <= 180.0001; b += 0.05) {
      var per = 60 / b / v.sub, worst = 0;
      hits.forEach(function (h) { var n = (h - v.start) / per; worst = Math.max(worst, Math.abs(n - Math.round(n)) * per * 24); });
      out.push([b, worst]);
      var ok = worst <= v.tol;
      if (ok && (!best || worst < best[1])) best = [b, worst];
      if (!ok && prevOk) { sols.push(best); best = null; }
      prevOk = ok;
    }
    if (prevOk && best) sols.push(best);
    return { curve: out, sols: sols };
  }
  W.hits = function (el) {
    QB.widget(el, {
      title: "Find a tempo that hits three actions",
      sub: "Three hit points in a scene, in seconds, and the cue's first downbeat. For every tempo from 60 to 180 beats a minute, the curve shows how far (in film frames, 1/24 s) the worst hit falls from its nearest beat. Dips below the gold line are tempos that hit all three. Play the best one: a click on every beat and a thump at each hit.",
      panels: 1, height: 240,
      controls: [
        { k: "start", label: "Cue downbeat", min: 0, max: 2, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2) + " s"; } },
        { k: "h1", label: "Hit 1", min: 1, max: 6, step: 0.05, value: 3.2, fmt: function (x) { return x.toFixed(2) + " s (frame " + Math.round(24 * x) + ")"; } },
        { k: "h2", label: "Hit 2", min: 4, max: 10, step: 0.05, value: 7.95, fmt: function (x) { return x.toFixed(2) + " s (frame " + Math.round(24 * x) + ")"; } },
        { k: "h3", label: "Hit 3", min: 8, max: 15, step: 0.05, value: 11.4, fmt: function (x) { return x.toFixed(2) + " s (frame " + Math.round(24 * x) + ")"; } },
        { k: "tol", label: "Tolerance", min: 0.25, max: 3, step: 0.25, value: 1, fmt: function (x) { return x + " frames"; } },
        { k: "sub", label: "Hit on", min: 1, max: 2, step: 1, value: 1, fmt: function (x) { return x === 1 ? "beats" : "beats and half-beats"; } }
      ],
      buttons: [{ label: "Play the best tempo", act: function (s) {
        var r = scan44(s.v); if (!r.sols.length) { s.sound = false; return; }
        var b = r.sols.reduce(function (a, c) { return c[1] < a[1] ? c : a; })[0], rate = 44100, per = 60 / b;
        var end = s.v.h3 + 1.5, out = new Float32Array(Math.floor(end * rate));
        function tick(t, f, g, dec) { var i0 = Math.floor(t * rate); for (var q = 0; q < 0.3 * rate && i0 + q < out.length; q++) { var tt = q / rate; out[i0 + q] += g * Math.exp(-tt * dec) * Math.sin(2 * Math.PI * f * tt); } }
        for (var t = s.v.start; t < end - 0.3; t += per) tick(t, 1760, 0.15, 60);
        [s.v.h1, s.v.h2, s.v.h3].forEach(function (h) { tick(h, 70, 0.6, 8); tick(h, 140, 0.3, 10); });
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        s.v = v;
        var r = scan44(v);
        var a = g[0].axes({ x: [60, 180], y: [0, 12], title: "Worst miss in frames, for every tempo (gold: the tolerance)", xlabel: "beats a minute" });
        a.line(r.curve.map(function (p) { return p[0]; }), r.curve.map(function (p) { return Math.min(p[1], 12); }), { color: "#60A5FA", width: 1 });
        a.line([60, 180], [v.tol, v.tol], { color: C.idea, width: 1.5 });
        a.dots(r.sols.map(function (p) { return p[0]; }), r.sols.map(function (p) { return p[1]; }), { r: 5, color: C.idea });
      },
      readout: function (v, s) {
        var r = scan44(v);
        var list = r.sols.slice(0, 5).map(function (p) { var f = 1440 / p[0]; return p[0].toFixed(2) + " (" + Math.floor(f) + "-" + Math.round((f - Math.floor(f)) * 8) + ")"; }).join(", ");
        return [["tempos that hit all three", r.sols.length ? r.sols.length + ": " + list + (r.sols.length > 5 ? " ..." : "") : "none: loosen the tolerance or allow half-beats"],
                ["one frame", (1000 / 24).toFixed(1) + " ms"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "no tempo to play")]];
      },
      note: "With the default scene only two tempos between 70 and 160 hit within a frame. Allow half-beats and the count jumps. Move one hit by a frame or two (0.05 s) and watch the solutions appear and vanish: that is why editors and composers negotiate over single frames."
    });
  };
  // ---------------------------------------------------------------- Part 45: one stream or two?
  function erb45(f) { return 21.4 * Math.log10(1 + 0.00437 * f); }
  function bound45(trt, k) { var e = erb45(1000) + k * trt, fb = (Math.pow(10, e / 21.4) - 1) / 0.00437; return 12 * Math.log2(fb / 1000); }
  W.stream = function (el) {
    QB.widget(el, {
      title: "One stream or two?",
      sub: "ABA- triplets: a tone A at 1 kHz, a tone B some semitones above, A again, a rest. Choose the interval and the time from one onset to the next. The gold line is our competition model's boundary (two streams above it), fitted to van Noorden's temporal coherence boundary; the blue line is his fission boundary (one stream below it). Play it and judge for yourself.",
      panels: 1, height: 240,
      controls: [
        { k: "st", label: "B above A", min: 0, max: 15, step: 0.5, value: 6, fmt: function (x) { return x + " semitones"; } },
        { k: "trt", label: "Onset to onset", min: 40, max: 200, step: 5, value: 90, fmt: function (x) { return x + " ms"; } },
        { k: "kk", label: "Model constant (w / tau)", min: 10, max: 60, step: 0.5, value: 32.4, fmt: function (x) { return x.toFixed(1) + " ERB-numbers a second"; } }
      ],
      buttons: [{ label: "Play 20 triplets", act: function (s) {
        var rate = 44100, T = s.v.trt / 1000, n = 20, out = new Float32Array(Math.floor((4 * T * n + 0.3) * rate));
        var fa = 1000, fb = 1000 * Math.pow(2, s.v.st / 12), dur = Math.min(0.05, T * 0.8);
        function tone(i0, f) { for (var q = 0; q < dur * rate && i0 + q < out.length; q++) { var t = q / rate; out[i0 + q] += 0.25 * Math.sin(Math.PI * t / dur) * Math.sin(2 * Math.PI * f * t); } }
        for (var c = 0; c < n; c++) { tone(Math.floor(4 * c * T * rate), fa); tone(Math.floor((4 * c + 1) * T * rate), fb); tone(Math.floor((4 * c + 2) * T * rate), fa); }
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        s.v = v;
        var a = g[0].axes({ x: [40, 200], y: [0, 15], title: "Interval against onset-to-onset time (the dot: your setting)", xlabel: "milliseconds" });
        var xs = [], ys = [];
        for (var t = 40; t <= 200; t += 2) { xs.push(t); ys.push(Math.min(bound45(t / 1000, v.kk), 15)); }
        a.line(xs, ys, { color: C.idea, width: 2.5 });
        a.line([40, 200], [1.5, 1.5], { color: "#60A5FA", width: 1.5 });
        a.dots([60, 80, 100, 120, 150], [4, 5.5, 7, 8.5, 11], { r: 4, color: "#F472B6" });
        a.dots([v.trt], [v.st], { r: 7, color: "#FFFFFF" });
      },
      readout: function (v, s) {
        var b = bound45(v.trt / 1000, v.kk);
        var verdict = v.st > b ? "two streams (above the coherence boundary)" : (v.st < 1.5 ? "one stream (below the fission boundary)" : "ambiguous: either can be heard");
        return [["model boundary here", b.toFixed(1) + " semitones"], ["prediction", verdict],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Pink dots: points read from van Noorden's figure, good to about a semitone. Six semitones at 90 ms sits near the line: listen for the gallop splitting after a few seconds. Halve the speed and it holds together; double the interval and it never gallops."
    });
  };
  // ---------------------------------------------------------------- Part 46: what an ending costs
  var IC46 = {"-5": 6.09, "-4": 11.02, "-3": 6.31, "-2": 11.02, "-1": 5.33, "0": 1.23, "1": 11.02, "2": 2.43, "3": 11.02, "4": 2.75, "5": 3.73, "6": 10.91, "7": 3.75, "8": 11.02, "9": 5.54, "10": 11.02, "11": 9.8, "12": 9.43};
  var NAMES46 = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"];
  W.ending = function (el) {
    QB.widget(el, {
      title: "What does an ending cost?",
      sub: "The Tune's last phrase, F F E E D D, and then a last note of your choice. The bars show how surprising each possible last note is to Part 46's listener model, trained on fifty other tunes: minus log2 of the probability it gave that note, in bits. Choose a note and play the phrase with it.",
      panels: 1, height: 230,
      controls: [{ k: "n", label: "Last note", min: -5, max: 12, step: 1, value: 0, fmt: function (x) { return NAMES46[((x % 12) + 12) % 12] + (x < 0 ? " (below)" : (x >= 12 ? " (an octave up)" : "")); } }],
      buttons: [{ label: "Play the phrase", act: function (s) {
        var rate = 44100, beat = 0.42, seq = [5, 5, 4, 4, 2, 2, s.v.n], out = new Float32Array(Math.floor((8 * beat + 1.2) * rate));
        seq.forEach(function (m, i) {
          var f = 261.63 * Math.pow(2, m / 12), i0 = Math.floor(i * beat * rate), dur = (i === 6 ? 2 : 0.95) * beat;
          for (var q = 0; q < (dur + 0.3) * rate && i0 + q < out.length; q++) { var t = q / rate; out[i0 + q] += 0.22 * Math.exp(-t * 2.5) * (t < dur ? 1 : Math.exp(-(t - dur) * 15)) * (Math.sin(2 * Math.PI * f * t) + 0.3 * Math.sin(4 * Math.PI * f * t)); }
        });
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        s.v = v;
        var xs = [], ys = [];
        for (var k = -5; k <= 12; k++) { xs.push(k); ys.push(IC46[String(k)]); }
        var a = g[0].axes({ x: [-5.6, 12.6], y: [0, 12], title: "Surprise of each possible last note, in bits (white: your choice)", xlabel: "semitones above the tonic C" });
        a.bars(xs, ys, 0.7, { color: function (i) { return xs[i] === v.n ? "#FFFFFF" : (ys[i] < 3 ? C.idea : "#F472B6"); } });
      },
      readout: function (v, s) {
        var b = IC46[String(v.n)];
        return [["your ending", NAMES46[((v.n % 12) + 12) % 12] + ": " + b.toFixed(2) + " bits, a probability of about 1 in " + Math.round(Math.pow(2, b))],
                ["the model's uncertainty before it", "2.57 bits"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "C, the real ending, costs about one bit. The notes outside the key cost about eleven: the model had never seen them end such a phrase. D and E cost little because folk tunes often end a phrase on them; they sound unfinished, which is a different thing from surprising."
    });
  };
})();
