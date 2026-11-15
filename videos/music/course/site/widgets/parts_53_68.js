// Interactives for Acts IX (end) to XII (Parts 53-68).  As before, each can be heard: the sound is computed in the page
// and played through the browser's Web Audio after a click.  Nothing is downloaded.
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

  // ---- Part 53: MIDI on the wire ----------------------------------------------------------------------------------
  function hex2(b) { return (b < 16 ? "0" : "") + b.toString(16).toUpperCase(); }
  function chordBytes(n, running, vel) {
    var out = [];
    for (var j = 0; j < n; j++) {
      if (j === 0 || !running) out.push(0x90);
      out.push(48 + 3 * j, vel);
    }
    return out;
  }
  function arrivals(n, running) {
    var t = [], bytes = 0;
    for (var j = 0; j < n; j++) { bytes += (j === 0 || !running) ? 3 : 2; t.push(bytes * 0.32); }
    return t;
  }
  W.midi = function (el) {
    QB.widget(el, {
      title: "A chord down a MIDI cable",
      sub: "Choose how many notes the chord has, whether running status is used, and the velocity. The plot shows when each note-on has fully arrived, at 320 microseconds a byte; the readout shows the bytes themselves. Play the chord as it arrives over the cable, then all at once.",
      panels: 1, height: 240,
      controls: [{ k: "n", label: "Notes in the chord", min: 1, max: 16, step: 1, value: 12, fmt: function (x) { return x.toFixed(0); } },
                 { k: "run", label: "Running status (0 off, 1 on)", min: 0, max: 1, step: 1, value: 1, fmt: function (x) { return x ? "on" : "off"; } },
                 { k: "vel", label: "Velocity", min: 1, max: 127, step: 1, value: 100, fmt: function (x) { return x.toFixed(0); } }],
      buttons: [{ label: "Play, over the cable", act: function (s) { s.sound = play(render(s.v, true), 44100); } },
                { label: "Play, all at once", act: function (s) { s.sound = play(render(s.v, false), 44100); } }],
      init: function (s) { s.sound = null; },
      draw: function (gr, v, s) {
        s.v = v;
        var t = arrivals(v.n, v.run > 0), xs = [], ys = [];
        for (var j = 0; j < t.length; j++) { xs.push(t[j]); ys.push(j + 1); }
        var a = gr[0].axes({ x: [0, 16], y: [0, 17], title: "Note-on j fully arrived (ms)", xlabel: "ms" });
        a.dots(xs, ys, { r: 4, color: C.idea });
      },
      readout: function (v, s) {
        var b = chordBytes(v.n, v.run > 0, v.vel), t = arrivals(v.n, v.run > 0);
        return [["bytes", b.length + ": " + b.slice(0, 14).map(hex2).join(" ") + (b.length > 14 ? " ..." : "")],
                ["last note arrives", t[t.length - 1].toFixed(2) + " ms after the first byte starts"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Running status saves the repeated status byte, so a chord's notes after the first cost two bytes, not three. Sixteen notes then take about 10.6 ms instead of 15.4: heard, if at all, as a slightly softer attack."
    });
    function render(v, serial) {
      var rate = 44100, n = Math.floor(1.6 * rate), out = new Float32Array(n), t = arrivals(v.n, v.run > 0), amp = 0.5 * v.vel / 127 / Math.sqrt(v.n);
      for (var j = 0; j < v.n; j++) {
        var f = hz(48 + 3 * j), start = serial ? Math.floor(t[j] / 1000 * rate) : 0;
        for (var i = start; i < n; i++) {
          var tt = (i - start) / rate;
          out[i] += amp * Math.exp(-tt / 0.5) * (Math.sin(2 * Math.PI * f * tt) + 0.3 * Math.sin(4 * Math.PI * f * tt)) * Math.min(1, tt / 0.001);
        }
      }
      return out;
    }
  };
  // ---- Part 54: a loudspeaker in a box ----------------------------------------------------------------------------
  function boxResponse(f, v) {
    // the closed forms: sealed, a second-order high-pass at fc = fs sqrt(1 + a) with Q = Qts sqrt(1 + a);
    // vented, the fourth-order polynomial of Thiele (lossless), with h = fb / fs
    var a = v.Vas / v.Vb, s = f / v.fs;
    if (v.vent < 0.5) {
      var fc = v.fs * Math.sqrt(1 + a), Q = v.Qts * Math.sqrt(1 + a), x = f / fc;
      var re = 1 - x * x, im = x / Q;
      return 20 * Math.log10(x * x / Math.sqrt(re * re + im * im));
    }
    var h = v.fb / v.fs, Q = v.Qts;
    // H(s) = s^4 / (s^4 + a1 s^3 + a2 s^2 + a3 s + a4) in units of fs (Thiele, lossless)
    var a1 = 1 / Q, a2 = (a + 1 + h * h), a3 = h * h / Q, a4 = h * h;
    var w = s, r = Math.pow(w, 4) - a2 * w * w + a4, i = -a1 * Math.pow(w, 3) + a3 * w;
    return 20 * Math.log10(Math.pow(w, 4) / Math.sqrt(r * r + i * i));
  }
  W.box = function (el) {
    QB.widget(el, {
      title: "A loudspeaker in a box",
      sub: "Set the driver's Thiele-Small parameters and the box. The plot is the bass response (dB) from the closed forms of Small (sealed) and Thiele (vented). Play a slow bass sweep through it.",
      panels: 1, height: 260,
      controls: [{ k: "fs", label: "Driver resonance fs", min: 20, max: 120, step: 1, value: 40, fmt: function (x) { return x.toFixed(0) + " Hz"; } },
                 { k: "Qts", label: "Qts", min: 0.2, max: 1.0, step: 0.01, value: 0.38, fmt: function (x) { return x.toFixed(2); } },
                 { k: "Vas", label: "Vas", min: 5, max: 200, step: 1, value: 50, fmt: function (x) { return x.toFixed(0) + " L"; } },
                 { k: "Vb", label: "Box volume", min: 5, max: 200, step: 1, value: 35, fmt: function (x) { return x.toFixed(0) + " L"; } },
                 { k: "vent", label: "Vented (0 no, 1 yes)", min: 0, max: 1, step: 1, value: 1, fmt: function (x) { return x ? "vented" : "sealed"; } },
                 { k: "fb", label: "Port tuning fb", min: 15, max: 100, step: 1, value: 40, fmt: function (x) { return x.toFixed(0) + " Hz"; } }],
      buttons: [{ label: "Play a bass sweep through it", act: function (s) {
        var rate = 44100, n = 5 * rate, out = new Float32Array(n), ph = 0;
        for (var i = 0; i < n; i++) {
          var t = i / rate, f = 25 * Math.pow(8, t / 5);
          ph += f / rate;
          var g = Math.pow(10, Math.min(6, boxResponse(f, s.v)) / 20);
          out[i] = 0.4 * g * Math.sin(2 * Math.PI * ph) * Math.min(1, t / 0.05) * Math.min(1, (5 - t) / 0.1);
        }
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (gr, v, s) {
        s.v = v;
        var xs = [], ys = [];
        for (var e = Math.log10(10); e <= Math.log10(1000); e += 0.01) { xs.push(e); ys.push(Math.max(-40, Math.min(10, boxResponse(Math.pow(10, e), v)))); }
        var a = gr[0].axes({ x: [1, 3], y: [-40, 10], title: "Response (dB) against log10 of frequency (Hz)", xlabel: "log10 Hz" });
        a.line([1, 3], [0, 0], { color: "#3A4250", width: 1.5 });
        a.line([1, 3], [-3, -3], { color: "#3A4250", width: 1 });
        a.line(xs, ys, { color: C.idea, width: 2.5 });
      },
      readout: function (v, s) {
        var f3 = null;
        for (var e = 1; e <= 3; e += 0.001) { if (boxResponse(Math.pow(10, e), v) >= -3) { f3 = Math.pow(10, e); break; } }
        var a = v.Vas / v.Vb;
        return [["-3 dB point", f3 ? f3.toFixed(1) + " Hz" : "below 10 Hz"],
                ["sealed: fc and Qtc", (v.fs * Math.sqrt(1 + a)).toFixed(1) + " Hz, " + (v.Qts * Math.sqrt(1 + a)).toFixed(2)],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Thiele's B4 alignment: Qts = 0.383, Vb = Vas / 1.414, fb = fs, gives a maximally flat response down to fs. Shrink the box and the bass bulges, or rolls off sooner; the iron law trades box size, bass and efficiency."
    });
  };
})();
