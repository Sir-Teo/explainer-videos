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
})();
