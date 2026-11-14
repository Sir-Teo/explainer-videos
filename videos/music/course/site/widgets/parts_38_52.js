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
})();
