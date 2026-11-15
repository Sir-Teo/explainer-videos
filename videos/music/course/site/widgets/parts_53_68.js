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

  // ---- Part 55: a room's reverberation and modes -----------------------------------------------------------------
  function roomModes(L, fmax) {
    var out = [], c = 343, n = [0, 1, 2].map(function (i) { return Math.floor(2 * fmax * L[i] / c) + 1; });
    for (var a = 0; a <= n[0]; a++) for (var b = 0; b <= n[1]; b++) for (var d = 0; d <= n[2]; d++) {
      if (a + b + d === 0) continue;
      var f = c / 2 * Math.sqrt(Math.pow(a / L[0], 2) + Math.pow(b / L[1], 2) + Math.pow(d / L[2], 2));
      if (f <= fmax) out.push([f, (a > 0) + (b > 0) + (d > 0)]);
    }
    return out.sort(function (p, q) { return p[0] - q[0]; });
  }
  function roomNumbers(v) {
    var V = v.Lx * v.Ly * v.Lz, S = 2 * (v.Lx * v.Ly + v.Ly * v.Lz + v.Lx * v.Lz);
    var sab = 0.161 * V / (v.alpha * S), eyr = 0.161 * V / (-S * Math.log(1 - v.alpha));
    return { V: V, S: S, sab: sab, eyr: eyr, fs: 2000 * Math.sqrt(eyr / V) };
  }

  W.room = function (el) {
    QB.widget(el, {
      title: "A room's reverberation and modes",
      sub: "Set a rectangular room's size and the absorption of its walls. The plot is every mode below 200 Hz (tallest: axial, then tangential, then oblique) and the Schroeder frequency above which they overlap. Play a clap in the room, decaying at Eyring's rate.",
      panels: 1, height: 240,
      controls: [{ k: "Lx", label: "Length", min: 2, max: 40, step: 0.1, value: 5, fmt: function (x) { return x.toFixed(1) + " m"; } },
                 { k: "Ly", label: "Width", min: 2, max: 30, step: 0.1, value: 4, fmt: function (x) { return x.toFixed(1) + " m"; } },
                 { k: "Lz", label: "Height", min: 2, max: 20, step: 0.1, value: 2.7, fmt: function (x) { return x.toFixed(1) + " m"; } },
                 { k: "alpha", label: "Average absorption", min: 0.02, max: 0.9, step: 0.01, value: 0.15, fmt: function (x) { return x.toFixed(2); } }],
      buttons: [{ label: "Play a clap in this room", act: function (s) {
        var rate = 44100, T = Math.min(8, roomNumbers(s.v).eyr), n = Math.floor((T + 0.6) * rate), out = new Float32Array(n), lp = 0, peak = 0;
        for (var i = 0; i < n; i++) {
          var t = i / rate, w = Math.random() * 2 - 1;
          lp += 0.25 * (w - lp);
          var mixw = Math.min(1, t / T);
          out[i] = ((1 - mixw) * w + mixw * lp) * Math.exp(-6.91 * t / T) * Math.min(1, t / 0.002);
          peak = Math.max(peak, Math.abs(out[i]));
        }
        for (i = 0; i < n; i++) out[i] *= 0.4 / peak;
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (gr, v, s) {
        s.v = v;
        var m = roomModes([v.Lx, v.Ly, v.Lz], 200), r = roomNumbers(v);
        var a = gr[0].axes({ x: [0, 200], y: [0, 1.1], title: "Modes below 200 Hz", xlabel: "Hz" });
        var hs = { 1: 1.0, 2: 0.7, 3: 0.45 }, cols = { 1: C.idea, 2: C.implied, 3: C.loss };
        for (var i = 0; i < m.length && i < 600; i++) a.line([m[i][0], m[i][0]], [0, hs[m[i][1]]], { color: cols[m[i][1]], width: 1.5 });
        if (r.fs < 200) a.line([r.fs, r.fs], [0, 1.1], { color: C.muted, width: 2 });
      },
      readout: function (v, s) {
        var r = roomNumbers(v), m = roomModes([v.Lx, v.Ly, v.Lz], 200);
        return [["T60, Sabine / Eyring", r.sab.toFixed(2) + " s / " + r.eyr.toFixed(2) + " s"],
                ["Schroeder frequency", r.fs.toFixed(0) + " Hz"],
                ["modes below 200 Hz", String(m.length) + (m.length ? " (first at " + m[0][0].toFixed(1) + " Hz)" : "")],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "A living room is modal through the whole bass; a hall's Schroeder frequency is near 20 Hz. Make the walls deader and Sabine's time parts from Eyring's: Sabine never reaches zero, even when every wall is an open window."
    });
  };

  // ---- Part 56: two microphones on one source ---------------------------------------------------------------------
  function combDb(f, v) {
    var tau = Math.max(v.far - v.near, 0) / 343, g = (v.near / v.far) * (v.flip ? -1 : 1);
    var re = 1 + g * Math.cos(2 * Math.PI * f * tau), im = -g * Math.sin(2 * Math.PI * f * tau);
    return 20 * Math.log10(Math.sqrt(re * re + im * im) + 1e-9);
  }

  W.comb = function (el) {
    QB.widget(el, {
      title: "Two microphones on one source",
      sub: "A close microphone and a farther one hear the same guitar; summed, they make a comb filter. Set the distances, flip the far microphone's polarity, and hear a strummed noise burst through the sum.",
      panels: 1, height: 240,
      controls: [{ k: "near", label: "Close microphone", min: 0.1, max: 2, step: 0.05, value: 0.5, fmt: function (x) { return x.toFixed(2) + " m"; } },
                 { k: "far", label: "Far microphone", min: 0.2, max: 8, step: 0.05, value: 1.5, fmt: function (x) { return x.toFixed(2) + " m"; } },
                 { k: "flip", label: "Far microphone's polarity (0 as is, 1 flipped)", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x ? "flipped" : "as is"; } }],
      buttons: [{ label: "Play bursts through the sum", act: function (s) {
        var rate = 44100, n = 3 * rate, out = new Float32Array(n), v = s.v;
        var d = Math.round(Math.max(v.far - v.near, 0) / 343 * rate), g = (v.near / v.far) * (v.flip ? -1 : 1), src = new Float32Array(n), lp = 0;
        for (var i = 0; i < n; i++) {
          var t = (i / rate) % 0.5;
          lp += 0.3 * ((Math.random() * 2 - 1) - lp);
          src[i] = lp * Math.exp(-t * 9);
        }
        var peak = 0;
        for (i = 0; i < n; i++) { out[i] = src[i] + (i >= d ? g * src[i - d] : 0); peak = Math.max(peak, Math.abs(out[i])); }
        for (i = 0; i < n; i++) out[i] *= 0.4 / peak;
        s.sound = play(out, rate);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (gr, v, s) {
        s.v = v;
        var xs = [], ys = [];
        for (var e = Math.log10(20); e <= Math.log10(20000); e += 0.002) { xs.push(e); ys.push(Math.max(-30, combDb(Math.pow(10, e), v))); }
        var a = gr[0].axes({ x: [Math.log10(20), Math.log10(20000)], y: [-30, 8], title: "The sum's response (dB) against log10 of frequency (Hz)", xlabel: "log10 Hz" });
        a.line([Math.log10(20), Math.log10(20000)], [0, 0], { color: "#3A4250", width: 1.5 });
        a.line(xs, ys, { color: C.idea, width: 2 });
      },
      readout: function (v, s) {
        var tau = Math.max(v.far - v.near, 0) / 343, g = v.near / v.far;
        return [["delay", (1000 * tau).toFixed(2) + " ms"],
                ["first notch", tau > 0 ? (v.flip ? "0 Hz (and every " + (1 / tau).toFixed(0) + " Hz)" : (1 / (2 * tau)).toFixed(0) + " Hz") : "none"],
                ["peaks and dips", "+" + (20 * Math.log10(1 + g)).toFixed(1) + " / " + (20 * Math.log10(Math.max(1 - g, 1e-6))).toFixed(1) + " dB"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "The 3 : 1 rule: with the far microphone three times as far away, it hears the source 9.5 dB quieter and the comb stays within +2.5 and -3.5 dB. Flip the polarity and the notches move to where the peaks were, starting with the bass."
    });
  };

  // ---- Part 57: a limiter and a streaming service ------------------------------------------------------------------
  var LOOP = null;
  function loopGroove() {
    if (LOOP) return LOOP;
    var rate = 48000, n = 4 * rate, y = new Float32Array(n), seed = 7;
    function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647 * 2 - 1; }
    for (var k = 0; k < 16; k++) {
      var i0 = Math.floor(k * 0.25 * rate), L = Math.floor(0.2 * rate);
      for (var j = 0; j < L && i0 + j < n; j++) {
        var t = j / rate;
        y[i0 + j] += (k % 2 === 0) ? Math.sin(2 * Math.PI * (60 + 80 * Math.exp(-t * 30)) * t) * Math.exp(-t * 12) : 0.6 * rnd() * Math.exp(-t * 25);
      }
    }
    for (var i = 0; i < n; i++) { var tt = i / rate; y[i] = 0.1 * (y[i] + 0.15 * Math.sin(2 * Math.PI * 110 * tt) * (1 + 0.5 * Math.sin(Math.PI * tt))); }
    LOOP = y;
    return y;
  }
  function kLoudness(y) {
    var b1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], a1 = [1, -1.69065929318241, 0.73248077421585];
    var b2 = [1, -2, 1], a2 = [1, -1.99004745483398, 0.99007225036621];
    function filt(x, b, a) { var o = new Float32Array(x.length), x1 = 0, x2 = 0, y1 = 0, y2 = 0;
      for (var i = 0; i < x.length; i++) { var v = b[0] * x[i] + b[1] * x1 + b[2] * x2 - a[1] * y1 - a[2] * y2; x2 = x1; x1 = x[i]; y2 = y1; y1 = v; o[i] = v; } return o; }
    var z = filt(filt(y, b1, a1), b2, a2), ms = 0;
    for (var i = 0; i < z.length; i++) ms += z[i] * z[i];
    return -0.691 + 10 * Math.log10(2 * ms / z.length + 1e-20);      // the same signal in two channels
  }
  function limitTo(y, driveDb) {
    var g = Math.pow(10, driveDb / 20), c = Math.pow(10, -1 / 20), n = y.length, L = 72, need = new Float32Array(n), out = new Float32Array(n);
    for (var i = 0; i < n; i++) need[i] = Math.min(1, c / Math.max(Math.abs(y[i] * g), 1e-9));
    var e = 1, rel = Math.exp(-1 / (0.08 * 48000)), peak = 0;
    for (i = 0; i < n; i++) {
      var m = 1;
      for (var j = i; j < Math.min(n, i + L); j++) if (need[j] < m) m = need[j];
      e = m < e ? m : rel * e + (1 - rel) * m;
      out[i] = Math.max(-c, Math.min(c, y[i] * g * e));
      peak = Math.max(peak, Math.abs(out[i]));
    }
    return { y: out, peak: 20 * Math.log10(peak + 1e-12) };
  }

  W.loud = function (el) {
    QB.widget(el, {
      title: "A limiter and a streaming service",
      sub: "Drive a short groove into a look-ahead limiter with its ceiling at -1 dBFS. The plot is the master's waveform; the readout its loudness, its peak-to-loudness ratio, and the gain a streaming service at its target would give it. Hear it as mastered, then as the service plays it.",
      panels: 1, height: 220,
      controls: [{ k: "drive", label: "Drive into the limiter", min: 0, max: 36, step: 0.5, value: 16, fmt: function (x) { return "+" + x.toFixed(1) + " dB"; } },
                 { k: "svc", label: "The service's target", min: -24, max: -10, step: 1, value: -14, fmt: function (x) { return x.toFixed(0) + " LUFS"; } }],
      buttons: [{ label: "Play as mastered", act: function (s) { s.sound = play(s.m.y, 48000); } },
                { label: "Play as the service plays it", act: function (s) {
                  var g = Math.pow(10, Math.min(0, s.v.svc - s.L) / 20), y = new Float32Array(s.m.y.length);
                  for (var i = 0; i < y.length; i++) y[i] = s.m.y[i] * g;
                  s.sound = play(y, 48000);
                } }],
      init: function (s) { s.sound = null; },
      draw: function (gr, v, s) {
        s.v = v;
        s.m = limitTo(loopGroove(), v.drive);
        s.L = kLoudness(s.m.y);
        var a = gr[0].axes({ x: [0, 4], y: [-1, 1], title: "The master's waveform (ceiling at -1 dBFS)", xlabel: "seconds" });
        var xs = [], hi = [], lo = [], step = 480;
        for (var i = 0; i < s.m.y.length; i += step) { var mx = 0; for (var j = i; j < i + step; j++) mx = Math.max(mx, Math.abs(s.m.y[j])); xs.push(i / 48000); hi.push(mx); lo.push(-mx); }
        a.line([0, 4], [0.891, 0.891], { color: "#C0504D", width: 1 });
        a.line([0, 4], [-0.891, -0.891], { color: "#C0504D", width: 1 });
        a.line(xs, hi, { color: C.idea, width: 1.5 });
        a.line(xs, lo, { color: C.idea, width: 1.5 });
      },
      readout: function (v, s) {
        var g = Math.min(0, v.svc - s.L);
        return [["loudness (K-weighted, ungated)", s.L.toFixed(1) + " LUFS"], ["peak-to-loudness ratio", (s.m.peak - s.L).toFixed(1) + " dB"],
                ["the service's gain", g.toFixed(1) + " dB (it never turns this one up)"], ["peaks as played", (s.m.peak + g).toFixed(1) + " dBFS"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Past the point where the limiter starts working, every decibel of drive adds less than a decibel of loudness and takes almost a decibel of peak-to-loudness ratio. The service hands the loudness back; the flattened peaks stay flattened."
    });
  };

  // ---- Part 58: an ABX test ------------------------------------------------------------------------------------------
  function binomPmf(n, p) {
    var out = [], lc = 0;
    for (var k = 0; k <= n; k++) {
      if (k > 0) lc += Math.log(n - k + 1) - Math.log(k);
      out.push(Math.exp(lc + k * Math.log(Math.max(p, 1e-12)) + (n - k) * Math.log(Math.max(1 - p, 1e-12))));
    }
    return out;
  }
  function abxThreshold(n, alpha) {
    var pm = binomPmf(n, 0.5), tail = 0;
    for (var c = n; c >= 0; c--) { tail += pm[c]; if (tail >= alpha) return c + 1; }
    return 0;
  }
  function abxSound(noiseDb, which) {
    var rate = 44100, n = Math.floor(1.6 * rate), y = new Float32Array(n), seed = 11;
    function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647 * 2 - 1; }
    var g = Math.pow(10, noiseDb / 20);
    for (var i = 0; i < n; i++) {
      var t = i / rate, env = Math.min(1, t / 0.02) * Math.min(1, (1.6 - t) / 0.1), v = 0;
      [220, 330, 440, 550, 660].forEach(function (f, j) { v += Math.sin(2 * Math.PI * f * t) / (j + 1); });
      y[i] = 0.12 * env * (v + (which === "B" ? g * 4 * rnd() : 0));
    }
    return y;
  }

  W.abx = function (el) {
    QB.widget(el, {
      title: "An ABX test",
      sub: "A is a chord; B is the same chord with a little noise added. Play A, B and X (one of the two, chosen at random), then reveal. The plot is how many right answers a guesser gets in a test of that many trials (grey) against a listener who is right with the probability you set (gold); the line is the score needed to pass at 5 per cent.",
      panels: 1, height: 220,
      controls: [{ k: "n", label: "Trials", min: 4, max: 100, step: 1, value: 16, fmt: function (x) { return x.toFixed(0); } },
                 { k: "p", label: "The listener is right", min: 0.5, max: 1, step: 0.01, value: 0.7, fmt: function (x) { return (100 * x).toFixed(0) + " %"; } },
                 { k: "noise", label: "B's noise", min: -50, max: -10, step: 1, value: -30, fmt: function (x) { return x.toFixed(0) + " dB"; } }],
      buttons: [{ label: "Play A", act: function (s) { s.sound = play(abxSound(s.v.noise, "A"), 44100); } },
                { label: "Play B", act: function (s) { s.sound = play(abxSound(s.v.noise, "B"), 44100); } },
                { label: "Play X", act: function (s) { if (!s.x) s.x = Math.random() < 0.5 ? "A" : "B"; s.revealed = false; s.sound = play(abxSound(s.v.noise, s.x), 44100); } },
                { label: "Reveal X (and draw a new one)", act: function (s) { s.revealed = s.x || "play X first"; s.x = null; } }],
      init: function (s) { s.sound = null; s.x = null; s.revealed = false; },
      draw: function (gr, v, s) {
        s.v = v;
        var n = Math.round(v.n), g = binomPmf(n, 0.5), l = binomPmf(n, v.p), c = abxThreshold(n, 0.05), ks = [], top = 0;
        for (var k = 0; k <= n; k++) { ks.push(k); top = Math.max(top, g[k], l[k]); }
        var a = gr[0].axes({ x: [0, n], y: [0, top * 1.1], title: "Right answers out of " + n, xlabel: "right answers" });
        a.line(ks, g, { color: "#8A93A0", width: 2 });
        a.line(ks, l, { color: C.idea, width: 2.5 });
        a.line([c - 0.5, c - 0.5], [0, top * 1.1], { color: "#C0504D", width: 1.5 });
      },
      readout: function (v, s) {
        var n = Math.round(v.n), c = abxThreshold(n, 0.05), l = binomPmf(n, v.p), pw = 0;
        for (var k = c; k <= n; k++) pw += l[k];
        return [["right answers needed to pass", c + " of " + n], ["chance this listener passes (power)", (100 * pw).toFixed(0) + " %"],
                ["X was", s.revealed ? s.revealed : "play A, B and X, then reveal"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "A failed short test does not show that a difference is inaudible: a listener right 70 % of the time passes a 16-trial test less than half the time. Make B's noise quieter until you cannot tell, then count how often you were right."
    });
  };

  // ---- Part 59: why a microphone howls ----------------------------------------------------------------------------
  function loopH(f, v) {
    // the acoustic path from loudspeaker to microphone: the direct sound and one reflection, through a one-pole
    // roll-off (the loudspeaker and microphone); returns [re, im] of H(f) before the amplifier's gain
    var c = 343, d1 = v.dist, d2 = v.dist + v.extra, w = 2 * Math.PI * f;
    var a1 = 1 / d1, a2 = v.refl / d2, t1 = d1 / c, t2 = d2 / c;
    var re = a1 * Math.cos(w * t1) + a2 * Math.cos(w * t2), im = -a1 * Math.sin(w * t1) - a2 * Math.sin(w * t2);
    var x = f / 3000, lr = 1 / (1 + x * x), li = -x / (1 + x * x);              // 1 / (1 + i f/fc)
    var hp = f / 120, hr = hp * hp / (1 + hp * hp), hi = hp / (1 + hp * hp);    // i (f/fh) / (1 + i f/fh)
    var r1 = re * lr - im * li, i1 = re * li + im * lr;
    return [r1 * hr - i1 * hi, r1 * hi + i1 * hr];
  }
  function edge(v) {
    var best = -1e9, at = 0;
    for (var e = 2; e <= Math.log10(8000); e += 0.0005) {
      var f = Math.pow(10, e), h = loopH(f, v);
      if (h[0] > best) { best = h[0]; at = f; }
    }
    return { gain: -20 * Math.log10(best), f: at };
  }
  function howlSound(v, g_db) {
    var sr = 44100, n = Math.round(2.2 * sr), y = new Float32Array(n), c = 343;
    var d1 = Math.round(v.dist / c * sr), d2 = Math.round((v.dist + v.extra) / c * sr);
    var g = Math.pow(10, g_db / 20), a1 = g / v.dist, a2 = g * v.refl / (v.dist + v.extra);
    var al = 1 - Math.exp(-2 * Math.PI * 3000 / sr), ah = Math.exp(-2 * Math.PI * 120 / sr), lp = 0, hpY = 0, hpX = 0, burst = Math.round(0.06 * sr);
    for (var i = 0; i < n; i++) {
      var x = i < burst ? (Math.random() * 2 - 1) * 0.3 * Math.sin(Math.PI * i / burst) : 0;
      var u = (i >= d1 ? a1 * y[i - d1] : 0) + (i >= d2 ? a2 * y[i - d2] : 0);
      lp += al * (u - lp);
      hpY = ah * (hpY + lp - hpX); hpX = lp;
      y[i] = Math.tanh(x + hpY);                                    // the amplifier clips instead of exploding
    }
    for (var j = 0; j < n; j++) y[j] *= 0.5 * Math.min(1, (n - j) / 2000);
    return y;
  }

  W.howl = function (el) {
    QB.widget(el, {
      title: "Why a microphone howls",
      sub: "A microphone hears its loudspeaker twice: directly and by one reflection. The plot is the real part of the loop's response (the loudspeaker-to-microphone path) on a log frequency axis, with the amplifier's gain added; where a peak reaches the line at 0 dB, the loop howls at that frequency (Nyquist's criterion). Play a clap into the loop at the gain you set.",
      panels: 1, height: 240,
      controls: [{ k: "dist", label: "Microphone to loudspeaker", min: 1, max: 15, step: 0.1, value: 4, fmt: function (x) { return x.toFixed(1) + " m"; } },
                 { k: "extra", label: "Reflection's extra path", min: 0.5, max: 20, step: 0.1, value: 6, fmt: function (x) { return x.toFixed(1) + " m"; } },
                 { k: "refl", label: "Reflection's strength", min: 0, max: 0.95, step: 0.01, value: 0.6, fmt: function (x) { return x.toFixed(2); } },
                 { k: "margin", label: "Gain against the edge", min: -12, max: 2, step: 0.1, value: -3, fmt: function (x) { return (x > 0 ? "+" : "") + x.toFixed(1) + " dB"; } }],
      buttons: [{ label: "Play a clap", act: function (s) { var e = edge(s.v); s.sound = play(howlSound(s.v, e.gain + s.v.margin), 44100); } }],
      init: function (s) { s.sound = null; },
      draw: function (gr, v, s) {
        s.v = v;
        var e = edge(v), g = e.gain + v.margin, xs = [], ys = [];
        for (var q = 2; q <= Math.log10(8000); q += 0.001) {
          var h = loopH(Math.pow(10, q), v);
          xs.push(q); ys.push(h[0] > 0 ? Math.max(-40, 20 * Math.log10(h[0]) + g) : -40);
        }
        var a = gr[0].axes({ x: [2, Math.log10(8000)], y: [-40, 6], title: "Re of the loop (dB, gain included) against log10 of frequency (Hz)", xlabel: "log10 Hz" });
        a.line([2, Math.log10(8000)], [0, 0], { color: "#C0504D", width: 1.5 });
        a.line(xs, ys, { color: C.idea, width: 2 });
        a.line([Math.log10(e.f), Math.log10(e.f)], [-40, 6], { color: "#3A4250", width: 1.5 });
      },
      readout: function (v, s) {
        var e = edge(v);
        return [["it will howl at", e.f.toFixed(0) + " Hz"], ["the largest stable gain", e.gain.toFixed(1) + " dB"],
                ["now", v.margin < 0 ? (-v.margin).toFixed(1) + " dB under the edge: it rings, then stops" : "past the edge: it howls"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Move the microphone further from the loudspeaker and the edge rises by 6 dB per doubling of distance, while the howl note jumps between the peaks of the comb that the direct sound and the reflection make. Set the gain 0.5 dB under the edge and the clap rings on at the howl note; set it 6 dB under and it simply stops."
    });
  };

  // ---- Part 60: dividing the pool ---------------------------------------------------------------------------------
  function pools(v) {
    // 1,000 paying users at the same fee; light users play few streams, mostly niche artists; heavy users play many,
    // mostly the charts; bot accounts pay the fee and stream one fake artist all month
    var fee = 11.99 * 0.7, n = 1000, nl = Math.round(n * v.light), nh = n - nl, bots = Math.round(v.bots);
    var sl = v.lightStreams, sh = v.heavyStreams, sb = 14000;
    var nicheL = 0.85, nicheH = 0.15;
    var streams = { chart: nl * sl * (1 - nicheL) + nh * sh * (1 - nicheH), niche: nl * sl * nicheL + nh * sh * nicheH, fraud: bots * sb };
    var total = streams.chart + streams.niche + streams.fraud, pool = (n + bots) * fee;
    var pr = { chart: pool * streams.chart / total, niche: pool * streams.niche / total, fraud: pool * streams.fraud / total };
    var uc = { chart: nl * fee * (1 - nicheL) + nh * fee * (1 - nicheH), niche: nl * fee * nicheL + nh * fee * nicheH, fraud: bots * fee };
    return { pr: pr, uc: uc, pool: pool, rate: pool / total, botFees: bots * fee };
  }
  function poolChord(shares) {
    var sr = 44100, n = Math.round(1.6 * sr), y = new Float32Array(n), f = [261.63, 329.63, 392.0], k = ["chart", "niche", "fraud"];
    var tot = shares.chart + shares.niche + shares.fraud;
    for (var j = 0; j < 3; j++) {
      var a = 0.5 * shares[k[j]] / tot;
      for (var i = 0; i < n; i++) {
        var env = Math.min(1, i / 400) * Math.min(1, (n - i) / 4000);
        y[i] += a * env * (Math.sin(2 * Math.PI * f[j] * i / sr) + 0.3 * Math.sin(4 * Math.PI * f[j] * i / sr));
      }
    }
    return y;
  }

  W.pool = function (el) {
    QB.widget(el, {
      title: "Dividing a streaming pool",
      sub: "A thousand subscribers each pay the same fee. Light listeners play few streams, mostly niche artists; heavy listeners play many, mostly the charts; bot accounts pay the fee and stream one fake artist all month. Bars: what each kind of artist is paid pro rata (one pool, by share of all streams; pale) and user by user (each fee divided by that user's own listening; solid). Play the two divisions as chords: C for the charts, E for the niche, G for the fake artist, each as loud as its share.",
      panels: 1, height: 230,
      controls: [{ k: "light", label: "Light listeners", min: 0, max: 1, step: 0.01, value: 0.45, fmt: function (x) { return (100 * x).toFixed(0) + " %"; } },
                 { k: "lightStreams", label: "Their streams a month", min: 20, max: 800, step: 10, value: 300, fmt: function (x) { return x.toFixed(0); } },
                 { k: "heavyStreams", label: "Heavy listeners' streams", min: 200, max: 4000, step: 50, value: 1800, fmt: function (x) { return x.toFixed(0); } },
                 { k: "bots", label: "Bot accounts", min: 0, max: 50, step: 1, value: 20, fmt: function (x) { return x.toFixed(0); } }],
      buttons: [{ label: "Play pro rata", act: function (s) { s.sound = play(poolChord(pools(s.v).pr), 44100); } },
                { label: "Play user by user", act: function (s) { s.sound = play(poolChord(pools(s.v).uc), 44100); } }],
      init: function (s) { s.sound = null; },
      draw: function (gr, v, s) {
        s.v = v;
        var r = pools(v), k = ["chart", "niche", "fraud"], top = 0;
        for (var j = 0; j < 3; j++) top = Math.max(top, r.pr[k[j]], r.uc[k[j]]);
        var a = gr[0].axes({ x: [0, 9], y: [0, top * 1.1], title: "Paid to the chart stars, the niche artists and the fake artist (dollars a month)", xlabel: "charts | niche | fake" });
        var cols = [C.idea || "#E8B04B", "#6FA8DC", "#C0504D"];
        for (var j2 = 0; j2 < 3; j2++) {
          var x0 = 3 * j2 + 0.5;
          a.line([x0 + 0.5, x0 + 0.5], [0, r.pr[k[j2]]], { color: "#8A93A0", width: 14 });
          a.line([x0 + 1.5, x0 + 1.5], [0, r.uc[k[j2]]], { color: cols[j2], width: 14 });
        }
      },
      readout: function (v, s) {
        var r = pools(v);
        function pc(a, b) { return (b === 0 ? 0 : 100 * (a / b - 1)).toFixed(0) + " %"; }
        return [["pool, and the average per stream", "$" + r.pool.toFixed(0) + ", " + (100 * r.rate).toFixed(3) + " cents"],
                ["niche artists, user by user against pro rata", pc(r.uc.niche, r.pr.niche)],
                ["the bots pay in, and take out pro rata", "$" + r.botFees.toFixed(0) + ", $" + r.pr.fraud.toFixed(0)],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Set the light and heavy listeners to the same number of streams and the two divisions agree: the difference comes only from how much the kinds of listener play. Add bots, and pro rata pays them a share of everyone's fees; user by user they get back only their own."
    });
  };

  // ---- Part 61: YIN -------------------------------------------------------------------------------------------------
  function yinTone(v, n, seed) {
    var sr = 44100, y = new Float32Array(n), s = seed || 1;
    function rnd() { s = (s * 16807) % 2147483647; return s / 2147483647; }
    for (var i = 0; i < n; i++) {
      var t = i / sr, x = 0;
      for (var k = (v.missing > 0.5 ? 2 : 1); k <= v.partials; k++) x += Math.sin(2 * Math.PI * v.f0 * k * t + k) / k;
      y[i] = x;
    }
    var p = 0;
    for (var j = 0; j < n; j++) p += y[j] * y[j];
    var sd = Math.sqrt(p / n) * Math.pow(10, -v.snr / 20);
    for (var q = 0; q < n; q += 2) {                       // Gaussian noise by Box-Muller
      var u1 = Math.max(rnd(), 1e-9), u2 = rnd(), r = Math.sqrt(-2 * Math.log(u1));
      y[q] += sd * r * Math.cos(2 * Math.PI * u2);
      if (q + 1 < n) y[q + 1] += sd * r * Math.sin(2 * Math.PI * u2);
    }
    return y;
  }
  function yinCurve(x, W, L) {
    var d = new Float64Array(L), dn = new Float64Array(L), run = 0;
    for (var tau = 1; tau < L; tau++) {
      var s = 0;
      for (var j = 0; j < W; j++) { var e = x[j] - x[j + tau]; s += e * e; }
      d[tau] = s; run += s; dn[tau] = s * tau / Math.max(run, 1e-12);
    }
    dn[0] = 1;
    return dn;
  }
  function yinPick(dn, tmin, thr) {
    var L = dn.length, t = -1;
    for (var k = tmin; k < L - 1; k++) if (dn[k] < thr) { t = k; while (t + 1 < L - 1 && dn[t + 1] < dn[t]) t++; break; }
    if (t < 0) { var g = 1e9; for (var k2 = tmin; k2 < L - 1; k2++) if (dn[k2] < g) { g = dn[k2]; t = k2; } }
    var a = dn[t - 1], b = dn[t], c = dn[t + 1], den = a - 2 * b + c;
    return t + (Math.abs(den) > 1e-12 ? 0.5 * (a - c) / den : 0);
  }

  W.yin = function (el) {
    QB.widget(el, {
      title: "YIN: one voice's pitch",
      sub: "A tone of a few partials, perhaps without its fundamental, in white noise. The plot is YIN's normalized difference function d'(τ) against the lag τ (in milliseconds): how badly the wave matches itself shifted by τ. The first dip under the threshold (red) is taken as the period. Play the tone to hear what the estimate should be.",
      panels: 1, height: 230,
      controls: [{ k: "f0", label: "Fundamental", min: 80, max: 600, step: 1, value: 220, fmt: function (x) { return x.toFixed(0) + " Hz"; } },
                 { k: "partials", label: "Partials", min: 1, max: 12, step: 1, value: 5, fmt: function (x) { return x.toFixed(0); } },
                 { k: "missing", label: "Remove the fundamental", min: 0, max: 1, step: 1, value: 0, fmt: function (x) { return x > 0.5 ? "yes" : "no"; } },
                 { k: "snr", label: "Signal to noise", min: -10, max: 40, step: 1, value: 20, fmt: function (x) { return x.toFixed(0) + " dB"; } },
                 { k: "thr", label: "Threshold", min: 0.02, max: 0.5, step: 0.01, value: 0.1, fmt: function (x) { return x.toFixed(2); } }],
      buttons: [{ label: "Play the tone", act: function (s) {
        var y = yinTone(s.v, 44100 * 1.5, 7), pk = 0;
        for (var i = 0; i < y.length; i++) pk = Math.max(pk, Math.abs(y[i]));
        for (var j = 0; j < y.length; j++) y[j] *= 0.4 / pk * Math.min(1, j / 500, (y.length - j) / 2000);
        s.sound = play(y, 44100);
      } }],
      init: function (s) { s.sound = null; },
      draw: function (gr, v, s) {
        s.v = v;
        var sr = 44100, L = Math.ceil(sr / 60) + 2, W = 2 * L, x = yinTone(v, W + L + 4, 3);
        var dn = yinCurve(x, W, L), xs = [], ys = [];
        for (var k = 1; k < L; k++) { xs.push(1000 * k / sr); ys.push(Math.min(dn[k], 2)); }
        var t = yinPick(dn, Math.floor(sr / 1000), v.thr);
        s.est = sr / t;
        var a = gr[0].axes({ x: [0, 1000 * L / sr], y: [0, 2], title: "d'(τ), the normalized difference", xlabel: "lag τ (ms)" });
        a.line([0, 1000 * L / sr], [v.thr, v.thr], { color: "#C0504D", width: 1.5 });
        a.line(xs, ys, { color: C.idea, width: 2 });
        a.line([1000 * t / sr, 1000 * t / sr], [0, 2], { color: "#6FA8DC", width: 1.5 });
        a.line([1000 / v.f0, 1000 / v.f0], [0, 0.15], { color: "#8A93A0", width: 4 });
      },
      readout: function (v, s) {
        var e = s.est || 0, err = 1200 * Math.log(e / v.f0) / Math.log(2);
        return [["YIN's estimate", e.toFixed(1) + " Hz"], ["against the true fundamental", (err >= 0 ? "+" : "") + err.toFixed(0) + " cents" + (Math.abs(err) > 300 ? " (a gross error)" : "")],
                ["the period (grey tick)", (1000 / v.f0).toFixed(2) + " ms"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Remove the fundamental: the dip stays where it was, because the wave still repeats at the same period, and you still hear the same pitch. Lower the signal to noise below about 0 dB and the dips fill in; when none falls under the threshold, YIN takes the deepest one, often at twice the period: an octave error."
    });
  };

  // ---- Part 62: tempo and its octave --------------------------------------------------------------------------------
  function tempoPattern(v) {
    // onsets (seconds, strength) of a drum pattern: beats, and off-beats of adjustable strength and swing
    var beat = 60 / v.bpm, out = [];
    for (var k = 0; k * beat < 8; k++) {
      out.push([k * beat, k % 2 === 0 ? 1.0 : 0.8]);
      if (v.off > 0.01) out.push([(k + v.swing) * beat, v.off]);
    }
    return out;
  }
  function tempoCurve(v) {
    // the autocorrelation of an impulse train with those strengths, at lags from 0.2 to 2 s, times a log-Gaussian prior
    var ons = tempoPattern(v), lags = [], ac = [], w = [], best = 0, bestBpm = 0, top = 0;
    for (var bpm = 30; bpm <= 300; bpm += 1) {
      var lag = 60 / bpm, a = 0;
      for (var i = 0; i < ons.length; i++) for (var j = 0; j < ons.length; j++) {
        var d = ons[j][0] - ons[i][0] - lag;
        a += ons[i][1] * ons[j][1] * Math.exp(-0.5 * (d / 0.012) * (d / 0.012));
      }
      var pr = Math.exp(-0.5 * Math.pow(Math.log(bpm / v.prior) / Math.LN2 / v.width, 2));
      lags.push(Math.log(bpm) / Math.LN2); ac.push(a); w.push(a * pr);
      top = Math.max(top, a);
      if (a * pr > best) { best = a * pr; bestBpm = bpm; }
    }
    return { x: lags, ac: ac, w: w, top: top, bpm: bestBpm };
  }
  function tempoSound(v, found) {
    var sr = 44100, n = Math.round(8 * sr), y = new Float32Array(n), s = 3;
    function rnd() { s = (s * 16807) % 2147483647; return s / 2147483647 * 2 - 1; }
    tempoPattern(v).forEach(function (o) {
      var i0 = Math.round(o[0] * sr), len = Math.round(0.05 * sr);
      for (var i = 0; i < len && i0 + i < n; i++) y[i0 + i] += 0.45 * o[1] * rnd() * Math.exp(-i / (0.012 * sr));
    });
    for (var t = 0; t < 8; t += 60 / found) {
      var k0 = Math.round(t * sr), m = Math.round(0.02 * sr);
      for (var q = 0; q < m && k0 + q < n; q++) y[k0 + q] += 0.3 * Math.sin(2 * Math.PI * 2000 * q / sr) * Math.exp(-q / (0.004 * sr));
    }
    return y;
  }

  W.tempo = function (el) {
    QB.widget(el, {
      title: "Tempo, and its octave",
      sub: "A drum pattern: a hit on every beat and, if you like, off-beats between them. The grey curve is how strongly the pattern repeats at each tempo (its autocorrelation); the gold curve is that times a prior, centred where you choose, which is how a tracker picks one tempo out of the hierarchy. Play the pattern with clicks at the tempo found.",
      panels: 1, height: 230,
      controls: [{ k: "bpm", label: "The beat", min: 50, max: 180, step: 1, value: 96, fmt: function (x) { return x.toFixed(0) + " a minute"; } },
                 { k: "off", label: "Off-beats", min: 0, max: 1, step: 0.05, value: 0.4, fmt: function (x) { return x.toFixed(2); } },
                 { k: "swing", label: "Where the off-beat falls", min: 0.5, max: 0.75, step: 0.01, value: 0.5, fmt: function (x) { return (100 * x).toFixed(0) + " % of the beat"; } },
                 { k: "prior", label: "The prior's centre", min: 60, max: 200, step: 1, value: 120, fmt: function (x) { return x.toFixed(0); } },
                 { k: "width", label: "The prior's width", min: 0.2, max: 3, step: 0.05, value: 1, fmt: function (x) { return x.toFixed(2) + " octaves"; } }],
      buttons: [{ label: "Play with the tracker's clicks", act: function (s) { s.sound = play(tempoSound(s.v, tempoCurve(s.v).bpm), 44100); } }],
      init: function (s) { s.sound = null; },
      draw: function (gr, v, s) {
        s.v = v;
        var r = tempoCurve(v), wtop = 0;
        for (var i = 0; i < r.w.length; i++) wtop = Math.max(wtop, r.w[i]);
        var a = gr[0].axes({ x: [Math.log(30) / Math.LN2, Math.log(300) / Math.LN2], y: [0, 1.05], title: "Repetition at each tempo (grey), weighted by the prior (gold)", xlabel: "log2 of beats a minute" });
        a.line(r.x, r.ac.map(function (z) { return z / r.top; }), { color: "#8A93A0", width: 1.5 });
        a.line(r.x, r.w.map(function (z) { return z / wtop; }), { color: C.idea, width: 2.5 });
        var xb = Math.log(r.bpm) / Math.LN2;
        a.line([xb, xb], [0, 1.05], { color: "#6FA8DC", width: 1.5 });
      },
      readout: function (v, s) {
        var r = tempoCurve(v), ratio = r.bpm / v.bpm;
        var what = Math.abs(ratio - 1) < 0.04 ? "the beat" : (Math.abs(ratio - 2) < 0.08 ? "double time" : (Math.abs(ratio - 0.5) < 0.04 ? "half time" : "another level"));
        return [["tempo found", r.bpm.toFixed(0) + " a minute"], ["relative to the beat", what],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Strengthen the off-beats and the pattern repeats as strongly at twice the tempo; then the prior decides, and near 120 it often chooses double time for a slow beat. Move the off-beat late (swing) and double time stops fitting, because the off-beats are no longer halfway."
    });
  };

  // ---- Part 63: popularity feeding on itself ------------------------------------------------------------------------
  function loopSim(v) {
    // listeners with tastes (two latent factors) and songs; each round every listener is shown the five most played
    // songs, each replaced with probability explore by a random song, and plays those that suit them
    var nu = 150, ni = 60, s = 11;
    function rnd() { s = (s * 16807) % 2147483647; return s / 2147483647; }
    function gauss() { var a = Math.max(rnd(), 1e-9), b = rnd(); return Math.sqrt(-2 * Math.log(a)) * Math.cos(2 * Math.PI * b); }
    var U = [], V = [], i, j;
    for (i = 0; i < nu; i++) U.push([gauss(), gauss()]);
    for (j = 0; j < ni; j++) V.push([gauss(), gauss()]);
    var like = [];
    for (i = 0; i < nu; i++) { like.push([]); for (j = 0; j < ni; j++) like[i].push(1 / (1 + Math.exp(-(U[i][0] * V[j][0] + U[i][1] * V[j][1])))); }
    var plays = [], own = [], g = [], go = [];
    for (j = 0; j < ni; j++) { plays.push(1); own.push(1); }
    function gini(x) {
      var a = x.slice().sort(function (p, q) { return p - q; }), n = a.length, num = 0, tot = 0;
      for (var k = 0; k < n; k++) { num += (2 * (k + 1) - n - 1) * a[k]; tot += a[k]; }
      return num / (n * tot);
    }
    for (var r = 0; r < v.rounds; r++) {
      var order = plays.map(function (p, k) { return [p, k]; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 5).map(function (z) { return z[1]; });
      for (i = 0; i < nu; i++) {
        for (var q = 0; q < 5; q++) {
          var item = rnd() < v.explore ? Math.floor(rnd() * ni) : order[q];
          if (rnd() < like[i][item]) plays[item] += 1;
        }
        var b = Math.floor(rnd() * ni);
        if (rnd() < like[i][b]) own[b] += 1;
      }
      g.push(gini(plays)); go.push(gini(own));
    }
    return { gini: g, own: go, plays: plays };
  }
  function loopChord(plays) {
    var sr = 44100, n = Math.round(2.0 * sr), y = new Float32Array(n);
    var top = plays.map(function (p, k) { return [p, k]; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 8);
    var tot = 0; top.forEach(function (z) { tot += z[0]; });
    var scale = [0, 2, 4, 7, 9, 12, 14, 16];
    top.forEach(function (z, k) {
      var f = 261.63 * Math.pow(2, scale[k] / 12), a = 0.6 * z[0] / tot;
      for (var i = 0; i < n; i++) y[i] += a * Math.sin(2 * Math.PI * f * i / sr) * Math.min(1, i / 400, (n - i) / 4000);
    });
    return y;
  }

  W.loop = function (el) {
    QB.widget(el, {
      title: "Popularity feeding on itself",
      sub: "150 simulated listeners with tastes, 60 songs. Each round a recommender shows every listener the five most played songs, each replaced, with the probability you set, by a random song; listeners play what suits them. Gold: the inequality of plays (Gini) round by round; grey: a world without a recommender, where listeners browse at random. Play the eight most played songs as a chord, each note as loud as its share.",
      panels: 1, height: 220,
      controls: [{ k: "explore", label: "Exploration", min: 0, max: 1, step: 0.05, value: 0, fmt: function (x) { return (100 * x).toFixed(0) + " %"; } },
                 { k: "rounds", label: "Rounds", min: 5, max: 60, step: 1, value: 30, fmt: function (x) { return x.toFixed(0); } }],
      buttons: [{ label: "Play the top eight", act: function (s) { s.sound = play(loopChord(loopSim(s.v).plays), 44100); } }],
      init: function (s) { s.sound = null; },
      draw: function (gr, v, s) {
        s.v = v;
        var r = loopSim(v), xs = [];
        for (var k = 0; k < r.gini.length; k++) xs.push(k + 1);
        var a = gr[0].axes({ x: [1, Math.max(2, r.gini.length)], y: [0, 1], title: "Gini of plays, round by round", xlabel: "round" });
        a.line(xs, r.own, { color: "#8A93A0", width: 2 });
        a.line(xs, r.gini, { color: C.idea, width: 2.5 });
      },
      readout: function (v, s) {
        var r = loopSim(v), sorted = r.plays.slice().sort(function (a, b) { return b - a; }), tot = 0;
        sorted.forEach(function (p) { tot += p; });
        return [["Gini after the last round", r.gini[r.gini.length - 1].toFixed(2) + " (without a recommender " + r.own[r.own.length - 1].toFixed(2) + ")"],
                ["the most played song's share", (100 * sorted[0] / tot).toFixed(0) + " %"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "With no exploration the first songs to be played are shown to everyone, played more, and shown again: a few songs take almost everything, whatever listeners' tastes. Explore a little and other songs get the chance to be found."
    });
  };

  // Part 64: masks on a spectrogram -------------------------------------------------------------------------------
  function maskWorld(v) {
    // a voice (a comb of harmonics gliding over a few notes) and drums (broadband hits), as magnitudes on a
    // 48-frame by 40-bin grid, each bin with its own random phase; the mixture is their complex sum
    var T = 48, F = 40, seed = 7, rnd = function () { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
    var notes = [6, 6, 8, 9, 8, 6, 5, 6], A = [], B = [], X = [];
    for (var t = 0; t < T; t++) {
      var f0 = notes[Math.floor(t / 6)], hit = (t % 6 === 0) ? 1 : (t % 6 === 1 ? 0.45 : 0.06);
      for (var f = 0; f < F; f++) {
        var a = 0;
        for (var h = 1; h * f0 < F + 2; h++) a += Math.exp(-Math.pow(f - h * f0, 2) / 0.5) * Math.pow(0.8, h - 1);
        var b = v.drums * hit * (0.6 + 0.4 * rnd()) * Math.exp(-f / 30);
        var pa = 2 * Math.PI * rnd(), pb = 2 * Math.PI * rnd();
        A.push([a * Math.cos(pa), a * Math.sin(pa)]); B.push([b * Math.cos(pb), b * Math.sin(pb)]);
        X.push([A[A.length - 1][0] + B[B.length - 1][0], A[A.length - 1][1] + B[B.length - 1][1]]);
      }
    }
    var mag = function (z) { return Math.sqrt(z[0] * z[0] + z[1] * z[1]); };
    var M = [], num = 0, den = 0, den0 = 0;
    for (var i = 0; i < X.length; i++) {
      var ma = Math.pow(mag(A[i]), v.power), mb = Math.pow(mag(B[i]), v.power);
      var m = ma / (ma + mb + 1e-12);
      m = Math.min(1, Math.max(0, m + v.noise * (rnd() - 0.5) * 2));
      M.push(m);
      var e = [A[i][0] - m * X[i][0], A[i][1] - m * X[i][1]];
      num += mag(A[i]) * mag(A[i]); den += e[0] * e[0] + e[1] * e[1];
      var e0 = [A[i][0] - X[i][0], A[i][1] - X[i][1]]; den0 += e0[0] * e0[0] + e0[1] * e0[1];
    }
    return { T: T, F: F, X: X.map(mag), M: M, sdr: 10 * Math.log10(num / den), sdr0: 10 * Math.log10(num / den0) };
  }
  function heat(a, vals, T, F, lo, hi, gold) {
    a.clip(function (c) {
      var w = a.w / T, h = a.h / F;
      for (var t = 0; t < T; t++) for (var f = 0; f < F; f++) {
        var z = Math.max(0, Math.min(1, (vals[t * F + f] - lo) / (hi - lo)));
        c.fillStyle = gold ? "rgba(214,170,60," + z.toFixed(3) + ")" : "rgba(235,235,240," + z.toFixed(3) + ")";
        c.fillRect(a.x0 + t * w, a.y0 + a.h - (f + 1) * h, w + 0.5, h + 0.5);
      }
    });
  }
  W.mask = function (el) {
    QB.widget(el, {
      title: "Masks on a spectrogram",
      sub: "A voice (a comb of harmonics over eight notes) and drum hits, as magnitudes in time-frequency bins, each bin with its own phase. The mask shares every bin of the mixture between them: power 1 shares in proportion to the true magnitudes, higher powers decide more sharply, and very high powers give the ideal binary mask. Add mask error to see what an imperfect separator does. The score is the voice's SDR, computed bin by bin.",
      panels: 2, height: 230,
      controls: [{ k: "power", label: "Mask power", min: 0.5, max: 12, step: 0.5, value: 1, fmt: function (x) { return x.toFixed(1); } },
                 { k: "noise", label: "Mask error", min: 0, max: 0.6, step: 0.02, value: 0, fmt: function (x) { return "± " + x.toFixed(2); } },
                 { k: "drums", label: "Drums level", min: 0.2, max: 3, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1) + "×"; } }],
      draw: function (gr, v) {
        var r = maskWorld(v), mx = 0;
        r.X.forEach(function (x) { mx = Math.max(mx, x); });
        var lg = r.X.map(function (x) { return Math.log10(x + 1e-3); });
        var a = gr[0].axes({ x: [0, r.T], y: [0, r.F], title: "the mixture's magnitudes", xlabel: "frame" });
        heat(a, lg, r.T, r.F, Math.log10(mx) - 2.5, Math.log10(mx), false);
        var b = gr[1].axes({ x: [0, r.T], y: [0, r.F], title: "the voice's mask (gold = 1)", xlabel: "frame" });
        heat(b, r.M, r.T, r.F, 0, 1, true);
      },
      readout: function (v) {
        var r = maskWorld(v);
        return [["the voice's SDR with this mask", r.sdr.toFixed(1) + " dB"],
                ["doing nothing (the mixture itself)", r.sdr0.toFixed(1) + " dB"]];
      },
      note: "Even a perfect mask cannot reach infinity: where voice and drums share a bin, the mixture's phase is neither's, and scaling it cannot undo that. Here power 2, which shares each bin by energy (the Wiener mask), scores best; power 1 is close behind, and very sharp masks, near the binary mask, lose a decibel or more. Which wins depends on the music: when one source dominates its bins, as drum hits do, sharp masks lose little."
    });
  };
  // Part 65: a Markov chain on Bach's chorale tunes -------------------------------------------------------------
  var CHORALE_TUNES = [[[60,2,0],[62,2,0],[64,4,0],[65,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[64,4,1],[64,4,0],[64,4,0],[62,2,0],[64,2,0],[65,2,0],[64,2,0],[62,4,0],[60,4,0],[62,4,0],[60,4,1],[60,4,0],[62,4,0],[64,4,0],[65,4,0],[64,4,0],[62,4,0],[64,4,0],[62,4,1],[62,4,0],[64,4,0],[65,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[64,4,1],[64,4,0],[64,4,0],[62,2,0],[64,2,0],[65,2,0],[64,2,0],[62,4,0],[60,2,0],[57,2,0],[59,4,0],[60,4,1]],[[64,4,0],[65,4,0],[67,4,0],[67,4,0],[60,4,0],[62,4,0],[64,8,1],[69,4,0],[71,4,0],[72,4,0],[64,4,0],[62,8,0],[60,8,1],[67,4,0],[62,4,0],[64,8,1],[69,6,0],[67,2,0],[66,8,1],[67,4,0],[62,4,0],[64,2,0],[66,2,0],[67,4,0],[67,4,0],[66,4,0],[67,8,1],[69,4,0],[71,4,0],[72,4,0],[64,4,0],[62,8,0],[60,8,1]],[[67,4,0],[67,4,0],[67,4,0],[67,2,0],[69,2,0],[70,4,0],[69,4,0],[67,4,0],[65,4,1],[67,4,0],[64,2,0],[62,2,0],[60,2,0],[62,2,0],[64,4,0],[66,4,0],[67,4,0],[69,4,0],[67,4,1],[67,4,0],[72,4,0],[71,4,0],[69,4,0],[71,4,0],[72,2,0],[71,2,0],[69,4,0],[67,4,1],[67,4,0],[72,4,0],[67,4,0],[69,4,0],[64,2,0],[65,2,0],[67,4,0],[65,4,0],[64,4,1],[64,4,0],[62,2,0],[64,2,0],[65,4,0],[64,4,0],[62,4,0],[57,4,0],[59,4,0],[60,4,1]],[[67,8,0],[69,8,0],[72,8,0],[71,8,0],[69,8,0],[72,8,0],[69,8,0],[67,8,1],[74,8,0],[74,8,0],[74,8,0],[76,12,0],[72,4,0],[74,8,0],[72,8,0],[71,8,1],[72,8,0],[72,8,0],[72,8,0],[71,8,0],[69,8,0],[72,8,0],[69,6,0],[67,2,0],[67,8,1],[74,8,0],[74,8,0],[74,8,0],[76,12,0],[72,4,0],[74,8,0],[72,6,0],[71,2,0],[71,16,1],[76,6,0],[74,2,0],[72,6,0],[71,2,0],[69,8,0],[71,8,0],[72,16,1]],[[72,4,0],[72,4,0],[72,4,0],[71,4,0],[67,4,0],[69,4,0],[71,4,0],[72,4,1],[72,4,0],[71,4,0],[69,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[64,4,1],[64,4,0],[62,4,0],[64,2,0],[66,2,0],[67,4,0],[69,4,0],[67,4,0],[66,4,0],[67,4,1],[67,4,0],[69,4,0],[71,4,0],[72,4,0],[71,4,0],[69,4,0],[69,4,0],[67,4,1],[67,4,0],[65,4,0],[64,4,0],[69,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,1],[62,4,0],[64,4,0],[66,4,0],[67,4,0],[69,4,0],[67,4,0],[66,4,0],[67,4,1]],[[64,4,0],[60,4,0],[62,4,0],[64,2,0],[65,2,0],[67,4,0],[65,8,0],[64,4,1],[64,2,0],[65,2,0],[67,4,0],[67,4,0],[62,4,0],[64,4,0],[60,8,0],[59,4,1],[55,4,0],[60,4,0],[62,4,0],[64,4,0],[64,2,0],[65,2,0],[62,12,1],[64,4,0],[60,4,0],[62,4,0],[64,2,0],[65,2,0],[67,4,0],[65,8,0],[64,4,1],[64,2,0],[65,2,0],[67,4,0],[67,4,0],[62,4,0],[64,4,0],[60,8,0],[59,4,1],[55,4,0],[60,4,0],[62,4,0],[64,4,0],[65,4,0],[64,4,0],[62,4,0],[60,4,1]],[[64,2,0],[65,2,0],[67,4,0],[69,4,0],[67,4,0],[65,2,0],[64,2,0],[64,8,1],[67,4,0],[69,4,0],[71,4,0],[72,4,0],[72,2,0],[71,2,0],[71,8,0],[69,4,1],[74,2,0],[72,2,0],[71,4,0],[72,2,0],[71,2,0],[69,6,0],[67,2,0],[67,12,1],[67,4,0],[69,4,0],[71,4,0],[72,6,0],[72,2,0],[71,12,1],[67,4,0],[67,4,0],[69,4,0],[67,4,0],[65,2,0],[64,2,0],[64,8,1],[67,4,0],[69,2,0],[71,2,0],[72,4,0],[72,4,0],[71,4,0],[72,12,1]],[[60,2,0],[62,2,0],[64,4,0],[65,4,0],[67,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,1],[67,4,0],[69,4,0],[71,4,0],[72,4,0],[71,2,0],[69,2,0],[69,8,0],[67,4,1],[60,2,0],[62,2,0],[64,4,0],[65,4,0],[67,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,1],[67,4,0],[69,4,0],[71,4,0],[72,4,0],[71,2,0],[69,2,0],[69,8,0],[67,4,1],[67,4,0],[72,4,0],[71,4,0],[69,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,1],[67,4,0],[65,4,0],[64,4,0],[62,2,0],[64,2,0],[65,4,0],[64,4,0],[62,4,0],[60,4,1]],[[60,4,0],[64,4,0],[67,6,0],[67,2,0],[67,4,0],[67,4,0],[69,8,0],[67,8,1],[67,4,0],[72,4,0],[67,4,0],[72,2,0],[74,2,0],[76,4,0],[74,4,0],[72,4,0],[71,4,0],[69,4,0],[67,8,1],[67,4,0],[72,4,0],[67,4,0],[69,4,0],[64,4,0],[65,2,0],[64,2,0],[62,4,0],[60,4,1],[67,4,0],[67,6,0],[65,2,0],[64,4,0],[62,4,0],[60,8,1],[67,4,0],[67,6,0],[65,2,0],[64,4,0],[62,4,0],[60,8,1],[62,4,0],[64,4,0],[65,4,0],[64,4,1],[67,4,0],[69,4,0],[71,4,0],[72,4,1],[72,2,0],[74,2,0],[76,4,0],[74,4,0],[72,4,1],[67,4,0],[72,4,0],[67,4,0],[69,4,0],[64,4,0],[65,2,0],[64,2,0],[62,4,0],[60,8,1]],[[55,4,0],[60,4,0],[62,4,0],[64,4,0],[69,4,0],[67,6,0],[65,2,0],[64,4,1],[69,4,0],[67,4,0],[65,4,0],[64,4,0],[65,2,0],[67,2,0],[62,8,0],[60,4,1],[67,4,0],[69,4,0],[69,4,0],[62,4,1],[62,4,0],[67,4,0],[67,4,0],[60,4,1],[64,4,0],[62,4,0],[60,4,0],[59,4,0],[60,2,0],[59,2,0],[57,8,0],[55,4,1],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[64,2,0],[65,2,0],[62,8,0],[60,4,1]],[[67,4,0],[65,2,0],[64,2,0],[69,4,0],[71,4,0],[72,4,0],[72,4,0],[71,8,1],[69,2,0],[71,2,0],[72,4,0],[67,2,0],[65,2,0],[64,4,0],[65,4,0],[64,4,0],[62,4,0],[60,4,1],[67,4,0],[65,2,0],[64,2,0],[69,4,0],[71,4,0],[72,4,0],[72,4,0],[71,8,1],[69,2,0],[71,2,0],[72,4,0],[67,2,0],[65,2,0],[64,4,0],[65,4,0],[64,4,0],[62,4,0],[60,4,1],[64,4,0],[66,4,0],[68,4,0],[69,2,0],[71,2,0],[72,4,0],[71,4,0],[69,8,1],[71,4,0],[72,4,0],[74,4,0],[76,4,0],[74,4,0],[74,4,0],[72,8,1]],[[64,4,0],[65,4,0],[67,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[62,4,1],[64,4,0],[65,4,0],[67,2,0],[65,2,0],[64,4,0],[62,2,0],[64,1,0],[65,1,0],[62,4,0],[60,8,1],[64,4,0],[65,4,0],[67,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[62,4,1],[64,4,0],[65,4,0],[67,2,0],[65,2,0],[64,4,0],[62,2,0],[64,1,0],[65,1,0],[62,4,0],[60,8,1],[62,4,0],[64,4,0],[65,4,0],[65,4,0],[64,6,0],[62,2,0],[62,8,1],[65,4,0],[67,4,0],[69,4,0],[69,4,0],[67,2,0],[69,1,0],[70,1,0],[67,4,0],[65,8,1],[64,4,0],[65,4,0],[67,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[62,4,1],[64,4,0],[65,4,0],[67,4,0],[60,2,0],[62,2,0],[64,4,0],[62,4,0],[60,8,1]],[[60,4,0],[67,4,0],[67,4,0],[67,4,0],[67,4,0],[69,4,0],[67,2,0],[65,2,0],[64,4,1],[62,4,0],[64,2,0],[66,2,0],[67,4,0],[69,4,0],[69,4,0],[67,8,1],[67,4,0],[67,4,0],[67,4,0],[67,4,0],[64,2,0],[65,2,0],[67,4,0],[65,2,0],[64,2,0],[62,4,1],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[62,4,0],[60,2,0],[62,2,0],[64,2,0],[65,2,0],[67,4,1],[67,4,0],[65,4,0],[64,2,0],[62,2,0],[64,4,0],[62,4,0],[60,12,1]],[[67,4,0],[67,4,0],[69,4,0],[69,4,0],[71,4,0],[71,4,0],[72,8,1],[74,4,0],[74,4,0],[72,4,0],[72,4,0],[71,4,0],[69,2,0],[71,1,0],[72,1,0],[69,8,0],[67,8,1],[67,4,0],[67,4,0],[69,4,0],[69,4,0],[67,4,0],[65,4,0],[64,8,1],[67,4,0],[67,4,0],[65,4,0],[65,4,0],[64,4,0],[62,2,0],[64,1,0],[65,1,0],[62,8,0],[60,8,1],[72,4,0],[72,4,0],[71,4,0],[71,4,0],[69,4,0],[69,4,0],[67,8,1],[67,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[62,4,0],[60,8,1]],[[72,4,0],[71,4,0],[72,4,0],[74,4,0],[74,4,0],[72,4,0],[74,4,0],[76,4,1],[77,4,0],[76,4,0],[74,4,0],[72,4,0],[71,2,0],[69,2,0],[71,4,0],[72,4,0],[74,8,0],[72,12,1],[72,4,0],[74,2,0],[76,2,0],[77,4,0],[76,2,0],[74,2,0],[72,4,0],[74,2,0],[72,2,0],[71,4,0],[69,4,1],[71,4,0],[67,4,0],[67,4,0],[74,4,0],[76,4,0],[77,2,0],[76,2,0],[74,4,0],[72,4,1],[79,4,0],[76,4,0],[77,2,0],[76,2,0],[74,6,0],[72,2,0],[71,4,0],[72,4,0],[74,8,0],[72,12,1]],[[64,4,0],[62,4,0],[60,4,0],[62,4,0],[64,4,0],[65,4,0],[67,8,1],[69,4,0],[67,4,0],[65,4,0],[64,2,0],[62,2,0],[62,8,0],[60,8,1],[64,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[60,4,0],[59,8,1],[60,4,0],[62,4,0],[64,4,0],[64,4,0],[65,8,0],[64,8,1],[64,4,0],[65,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[64,8,1],[62,4,0],[62,4,0],[64,2,0],[66,2,0],[67,4,0],[67,4,0],[66,4,0],[67,8,1],[67,4,0],[64,4,0],[69,4,0],[67,4,0],[65,4,0],[64,4,0],[62,8,1],[64,2,0],[65,2,0],[67,4,0],[65,4,0],[64,2,0],[62,2,0],[62,8,0],[60,8,1]],[[72,4,0],[72,2,0],[74,2,0],[76,4,0],[74,4,0],[72,4,0],[71,8,0],[69,4,1],[76,4,0],[77,4,0],[74,4,0],[76,4,0],[74,4,0],[72,12,1],[72,2,0],[74,2,0],[76,4,0],[76,4,0],[77,4,0],[77,4,0],[79,4,0],[77,2,0],[76,2,0],[74,4,1],[79,4,0],[76,4,0],[76,4,0],[74,4,0],[72,4,0],[71,8,0],[69,4,1],[76,4,0],[77,4,0],[74,4,0],[76,4,0],[74,4,0],[72,12,1]],[[72,4,0],[74,4,0],[74,4,0],[72,6,0],[71,2,0],[69,4,0],[67,4,0],[69,4,0],[71,4,0],[72,12,1],[76,2,0],[77,2,0],[79,4,0],[81,4,0],[79,6,0],[77,2,0],[76,2,0],[74,2,0],[72,2,0],[71,2,0],[69,4,0],[71,4,0],[72,8,1],[76,4,0],[76,4,0],[76,4,0],[74,4,0],[76,8,0],[72,4,1],[72,4,0],[74,2,0],[76,2,0],[77,4,0],[76,2,0],[74,2,0],[76,4,0],[72,8,1],[74,2,0],[76,2,0],[77,4,0],[76,2,0],[74,2,0],[72,2,0],[71,2,0],[69,4,0],[67,4,0],[72,2,0],[74,2,0],[76,4,0],[74,6,0],[72,2,0],[71,4,0],[69,4,0],[67,8,1],[69,4,0],[71,4,0],[72,8,0],[74,8,0],[72,12,1]],[[72,4,0],[71,4,0],[69,4,0],[67,4,0],[65,2,0],[64,2,0],[69,4,0],[69,4,0],[67,4,1],[72,4,0],[71,4,0],[69,4,0],[67,4,0],[65,2,0],[64,2,0],[69,4,0],[69,4,0],[67,4,1],[67,4,0],[69,4,0],[71,4,0],[72,2,0],[74,2,0],[76,4,0],[74,2,0],[72,2,0],[74,4,0],[72,4,1],[72,4,0],[72,4,0],[74,4,0],[72,4,0],[69,2,0],[71,2,0],[72,4,0],[72,4,0],[71,4,1],[71,4,0],[72,4,0],[74,4,0],[72,4,0],[69,2,0],[71,2,0],[72,4,0],[72,4,0],[71,4,1],[76,4,0],[77,2,0],[76,2,0],[74,4,0],[76,2,0],[74,2,0],[72,4,0],[72,4,0],[71,4,0],[72,4,1],[71,4,0],[72,4,0],[71,4,0],[69,4,0],[67,4,0],[67,4,0],[66,4,0],[67,4,1],[76,4,0],[74,4,0],[72,4,0],[71,4,1],[76,4,0],[77,2,0],[76,2,0],[74,4,0],[76,2,0],[74,2,0],[72,4,0],[72,4,0],[71,4,0],[72,4,1],[72,4,0],[72,4,0],[72,4,0],[74,4,0],[72,4,0],[72,4,0],[71,4,0],[72,4,1]],[[64,4,0],[62,4,0],[60,4,0],[62,4,0],[64,2,0],[65,2,0],[67,4,0],[65,8,0],[64,8,1],[67,4,0],[64,4,0],[65,4,0],[64,2,0],[62,2,0],[60,2,0],[62,2,0],[64,4,0],[62,8,0],[60,8,1],[67,4,0],[69,2,0],[71,2,0],[72,4,0],[72,4,0],[71,2,0],[69,2,0],[67,2,0],[69,2,0],[69,8,0],[67,8,1],[67,4,0],[69,2,0],[71,2,0],[72,4,0],[72,4,0],[71,2,0],[69,2,0],[67,2,0],[69,2,0],[69,8,0],[67,8,1],[62,4,0],[64,4,0],[65,4,0],[65,4,0],[64,2,0],[67,2,0],[65,2,0],[64,2,0],[62,4,0],[62,4,1],[67,4,0],[64,4,0],[65,4,0],[64,2,0],[62,2,0],[60,2,0],[62,2,0],[64,4,0],[62,8,0],[60,16,1]],[[72,4,0],[72,4,0],[71,4,0],[69,4,0],[67,4,0],[72,4,0],[74,4,0],[76,4,1],[74,4,0],[76,2,0],[77,1,0],[79,1,0],[77,4,0],[76,4,0],[74,2,0],[76,2,0],[77,4,0],[76,4,0],[74,8,0],[72,12,1],[72,4,0],[74,4,0],[76,4,0],[72,4,1],[72,4,0],[74,4,0],[76,4,0],[72,4,1],[69,4,0],[74,6,0],[72,2,0],[71,4,0],[72,2,0],[71,2,0],[69,8,0],[67,4,1],[67,4,0],[72,4,0],[71,4,0],[69,4,0],[67,4,0],[72,4,0],[74,4,0],[76,4,1],[74,4,0],[79,6,0],[77,2,0],[76,4,0],[74,2,0],[76,2,0],[77,4,0],[76,4,0],[74,8,0],[72,12,1]],[[76,4,0],[76,4,0],[72,4,0],[74,4,0],[76,4,0],[77,8,0],[74,4,1],[74,4,0],[74,4,0],[72,4,0],[72,4,0],[71,4,0],[72,12,1],[74,4,0],[74,4,0],[74,4,0],[74,4,0],[76,4,0],[72,8,0],[72,4,1],[72,4,0],[71,4,0],[72,4,0],[74,4,0],[74,4,0],[72,12,1],[76,4,0],[76,4,0],[72,4,0],[74,4,0],[76,4,0],[77,8,0],[74,4,1],[74,4,0],[74,4,0],[72,4,0],[72,4,0],[71,4,0],[72,12,1],[74,4,0],[74,4,0],[74,4,0],[74,4,0],[76,4,0],[72,8,0],[72,4,1],[72,4,0],[71,4,0],[72,4,0],[74,4,0],[74,4,0],[72,12,1],[71,4,0],[71,4,0],[71,4,0],[71,4,0],[71,4,0],[72,8,0],[72,4,1],[71,4,0],[71,4,0],[71,4,0],[71,4,0],[71,4,0],[72,8,0],[72,4,1],[76,4,0],[76,4,0],[72,4,0],[74,4,0],[76,4,0],[77,8,0],[76,4,0],[76,4,0],[74,4,0],[76,4,0],[73,4,0],[73,4,0],[74,12,1],[76,4,0],[76,4,0],[72,4,0],[74,4,0],[76,4,0],[77,8,0],[76,4,0],[76,4,0],[74,4,0],[76,4,0],[73,4,0],[73,4,0],[74,12,1],[76,4,0],[76,4,0],[72,4,0],[74,4,0],[76,4,0],[77,8,0],[74,4,0],[74,4,0],[74,4,0],[72,4,0],[72,4,0],[71,4,0],[72,12,1]],[[67,4,0],[64,4,0],[60,4,0],[67,4,0],[67,4,0],[69,8,1],[69,4,0],[62,4,0],[62,4,0],[67,4,0],[65,4,0],[64,4,0],[62,4,0],[60,4,1],[67,4,0],[69,4,0],[69,4,0],[67,4,0],[65,4,0],[64,8,1],[62,4,0],[64,4,0],[66,4,0],[67,4,0],[69,2,0],[71,1,0],[72,1,0],[71,4,0],[69,4,0],[67,4,1],[67,4,0],[67,4,0],[67,4,0],[72,4,0],[70,2,0],[69,2,0],[69,8,1],[69,4,0],[69,4,0],[69,4,0],[74,4,0],[72,2,0],[71,2,0],[71,8,1],[67,4,0],[69,4,0],[67,4,0],[69,4,0],[71,4,0],[72,8,1],[67,4,0],[69,2,0],[67,2,0],[65,2,0],[64,2,0],[62,4,0],[62,4,0],[60,12,1]],[[67,4,0],[69,4,0],[67,2,0],[65,2,0],[64,2,0],[65,2,0],[67,4,0],[62,8,1],[64,4,0],[66,4,0],[67,8,1],[67,4,0],[69,4,0],[67,4,0],[62,2,0],[64,2,0],[65,4,0],[64,4,0],[62,4,0],[60,4,1],[60,4,0],[62,2,0],[64,2,0],[65,4,0],[64,2,0],[65,2,0],[67,8,0],[62,4,0],[60,2,0],[59,2,0],[57,4,0],[55,8,1],[55,4,0],[60,4,0],[62,4,0],[64,2,0],[65,2,0],[67,8,0],[65,4,0],[64,4,0],[62,4,0],[64,8,1],[64,2,0],[65,2,0],[67,4,0],[69,4,0],[67,4,0],[62,4,0],[64,4,0],[66,4,0],[67,4,1],[67,4,0],[69,4,0],[67,4,0],[62,2,0],[64,2,0],[65,4,0],[64,4,0],[62,4,0],[60,4,1],[60,4,0],[62,2,0],[64,2,0],[65,4,0],[64,2,0],[65,2,0],[67,8,0],[62,4,0],[60,2,0],[59,2,0],[57,4,0],[55,8,1],[55,4,0],[60,4,0],[62,4,0],[64,2,0],[65,2,0],[67,8,0],[65,4,0],[64,4,0],[62,4,0],[57,4,0],[59,4,0],[60,4,1],[62,4,0],[64,4,0],[60,4,0],[57,8,0],[55,4,1],[62,2,0],[64,1,0],[65,1,0],[64,8,0],[62,8,0],[60,4,1]],[[64,4,0],[64,4,0],[65,2,0],[67,1,0],[69,1,0],[67,4,0],[65,1,0],[64,1,0],[65,2,0],[64,4,1],[64,2,0],[65,2,0],[67,4,0],[60,4,0],[62,4,0],[64,4,0],[62,8,0],[60,4,1],[64,4,0],[64,4,0],[65,2,0],[67,1,0],[69,1,0],[67,4,0],[65,4,0],[64,4,1],[64,2,0],[65,2,0],[67,4,0],[60,4,0],[62,4,0],[64,3,0],[65,1,0],[62,8,0],[60,4,1],[62,4,0],[62,4,0],[64,4,0],[65,4,0],[65,3,0],[67,1,0],[64,4,1],[64,4,0],[62,4,0],[67,2,0],[69,1,0],[70,1,0],[69,4,0],[67,2,0],[66,2,0],[67,4,1],[67,4,0],[67,2,0],[65,2,0],[64,4,0],[65,4,0],[67,2,0],[69,1,0],[70,1,0],[69,4,1],[62,4,0],[64,4,0],[64,4,0],[62,4,0],[62,4,0],[60,4,1]],[[62,4,0],[67,4,0],[65,4,0],[63,4,0],[62,4,0],[60,8,0],[62,4,1],[69,4,0],[70,4,0],[70,4,0],[69,2,0],[67,2,0],[69,4,0],[67,12,1],[70,4,0],[69,2,0],[67,2,0],[65,4,0],[67,4,0],[69,4,0],[70,8,0],[70,4,1],[65,4,0],[67,4,0],[65,4,0],[63,4,0],[63,4,0],[62,12,1],[70,4,0],[69,2,0],[70,2,0],[72,4,0],[70,4,0],[69,4,0],[67,8,0],[69,4,1],[62,4,0],[63,4,0],[62,4,0],[60,4,0],[65,4,0],[62,12,1]],[[64,4,0],[69,4,0],[67,4,0],[65,4,0],[64,4,0],[62,8,0],[64,4,1],[71,4,0],[72,4,0],[72,4,0],[71,2,0],[69,2,0],[71,4,0],[69,12,1],[64,4,0],[69,4,0],[67,4,0],[65,4,0],[64,4,0],[62,8,0],[64,4,1],[71,4,0],[72,4,0],[72,4,0],[71,2,0],[69,2,0],[71,4,0],[69,12,1],[72,4,0],[71,2,0],[69,2,0],[67,4,0],[69,4,0],[71,4,0],[72,8,0],[72,4,1],[67,4,0],[69,4,0],[67,4,0],[65,4,0],[65,4,0],[64,12,1],[72,4,0],[71,2,0],[72,2,0],[74,4,0],[72,4,0],[71,4,0],[69,8,0],[71,4,1],[64,4,0],[65,4,0],[64,4,0],[62,4,0],[67,4,0],[64,12,1]],[[69,4,0],[69,4,0],[69,4,0],[68,4,0],[64,4,0],[69,4,0],[71,4,0],[72,4,0],[72,4,0],[74,4,0],[72,4,0],[71,4,1],[71,4,0],[72,4,0],[74,4,0],[76,2,0],[74,2,0],[72,4,0],[77,4,0],[77,4,0],[76,4,0],[75,2,0],[74,2,0],[74,8,0],[72,4,1],[72,4,0],[71,4,0],[69,4,0],[67,4,0],[64,2,0],[65,2,0],[67,4,0],[67,4,0],[69,4,0],[67,4,0],[65,8,0],[64,4,1],[76,4,0],[74,4,0],[72,2,0],[71,2,0],[71,8,0],[69,12,1]],[[67,4,0],[67,4,0],[67,4,0],[69,4,0],[67,4,0],[72,4,0],[74,4,0],[72,8,1],[71,2,0],[72,2,0],[74,4,0],[76,4,0],[74,2,0],[72,2,0],[71,4,0],[69,4,0],[67,4,1],[67,4,0],[72,4,0],[71,2,0],[72,2,0],[74,4,0],[69,4,0],[67,2,0],[66,2,0],[64,4,0],[62,4,1],[62,4,0],[69,4,0],[69,4,0],[69,4,0],[71,4,0],[72,2,0],[71,2,0],[69,4,0],[67,2,0],[69,2,0],[71,4,0],[69,8,0],[67,4,0],[67,4,0],[67,12,1]],[[76,4,0],[76,2,0],[77,2,0],[79,4,0],[76,4,0],[72,4,0],[74,4,0],[76,4,0],[77,4,1],[76,4,0],[74,4,0],[72,4,0],[72,6,0],[74,2,0],[76,4,0],[76,4,0],[74,2,0],[72,2,0],[74,4,0],[72,12,1],[76,4,0],[74,4,0],[76,4,0],[72,4,0],[69,4,0],[74,4,0],[72,4,0],[74,4,1],[76,4,0],[72,4,0],[72,4,0],[72,6,0],[74,2,0],[76,4,0],[76,4,0],[74,2,0],[72,2,0],[74,4,0],[72,12,1]]];   // thirty of Bach's chorale soprano lines in C: [key, sixteenths, fermata]
  function chainSample(v) {
    var k = Math.round(v.order), seed = Math.round(v.seed) * 7919 + 13, rnd = function () { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
    var key = function (n) { return n[0] + ":" + n[1] + ":" + n[2]; };
    var counts = {}, starts = [];
    CHORALE_TUNES.forEach(function (t) {
      starts.push(t.slice(0, k));
      for (var i = k; i < t.length; i++) {
        var ctx = t.slice(i - k, i).map(key).join("|");
        counts[ctx] = counts[ctx] || {};
        counts[ctx][key(t[i])] = (counts[ctx][key(t[i])] || 0) + 1;
      }
    });
    var out = starts[Math.floor(rnd() * starts.length)].slice(), phrases = 0;
    while (out.length < 64) {
      var ctx = out.slice(out.length - k).map(key).join("|"), c = counts[ctx];
      if (!c) break;
      var ks = Object.keys(c), w = ks.map(function (s) { return Math.pow(c[s], 1 / v.temp); }), tot = 0;
      w.forEach(function (x) { tot += x; });
      var r = rnd() * tot, j = 0;
      while (r > w[j] && j < ks.length - 1) { r -= w[j]; j++; }
      var n = ks[j].split(":").map(Number);
      out.push(n);
      if (n[2]) { phrases++; if (phrases >= 4 && n[0] % 12 === 0) break; }
    }
    // the longest run of notes copied from one tune, and the notes inside a copied run of 8 or more
    var seqs = CHORALE_TUNES.map(function (t) { return "," + t.map(key).join(",") + ","; }), best = [0, 0], cover = out.map(function () { return false; });
    for (var i = 0; i < out.length; i++) {
      var L = 1, last = 0;
      while (i + L <= out.length) {
        var s = "," + out.slice(i, i + L).map(key).join(",") + ",";
        if (!seqs.some(function (q) { return q.indexOf(s) >= 0; })) break;
        last = L; L++;
      }
      if (last > best[0]) best = [last, i];
      if (last >= 8) for (var m = i; m < i + last; m++) cover[m] = true;
    }
    var share = 0; cover.forEach(function (x) { if (x) share++; });
    return { notes: out, longest: best[0], cover: cover, share: out.length ? share / out.length : 0 };
  }
  function chainSound(notes) {
    var sr = 22050, six = 0.14, n = 0;
    notes.forEach(function (x) { n += x[1] * six + (x[2] ? 0.25 : 0); });
    var y = new Float32Array(Math.ceil((n + 0.5) * sr)), t = 0;
    notes.forEach(function (x) {
      var f = 440 * Math.pow(2, (x[0] - 69) / 12), d = x[1] * six * (x[2] ? 1.6 : 0.95), i0 = Math.floor(t * sr);
      for (var i = 0; i < d * sr && i0 + i < y.length; i++) {
        var s = i / sr, e = Math.min(1, s / 0.02) * Math.min(1, (d - s) / 0.05);
        y[i0 + i] += 0.18 * e * (Math.sin(2 * Math.PI * f * s) + 0.5 * Math.sin(4 * Math.PI * f * s) + 0.25 * Math.sin(6 * Math.PI * f * s));
      }
      t += x[1] * six + (x[2] ? 0.25 : 0);
    });
    return y;
  }
  W.chain = function (el) {
    QB.widget(el, {
      title: "A Markov chain on Bach's tunes",
      sub: "Thirty of Bach's chorale melodies, transposed to C. The chain remembers the last few notes (the order) and draws the next from what followed them in the tunes; the temperature flattens or sharpens its odds. Gold notes are new; red notes lie inside a run of eight or more copied note for note from one tune.",
      panels: 1, height: 220,
      controls: [{ k: "order", label: "Order", min: 0, max: 6, step: 1, value: 2, fmt: function (x) { return x.toFixed(0); } },
                 { k: "temp", label: "Temperature", min: 0.3, max: 2, step: 0.1, value: 1, fmt: function (x) { return x.toFixed(1); } },
                 { k: "seed", label: "Draw", min: 1, max: 30, step: 1, value: 1, fmt: function (x) { return x.toFixed(0); } }],
      buttons: [{ label: "Play the tune", act: function (s) { s.sound = play(chainSound(chainSample(s.v).notes), 22050); } }],
      init: function (s) { s.sound = null; },
      draw: function (gr, v, s) {
        s.v = v;
        var r = chainSample(v), t = 0, lo = 100, hi = 0, xs = [];
        r.notes.forEach(function (n) { lo = Math.min(lo, n[0]); hi = Math.max(hi, n[0]); xs.push(t); t += n[1]; });
        var a = gr[0].axes({ x: [0, Math.max(t, 16)], y: [lo - 2, hi + 2], title: "the tune drawn (sixteenths across, pitch up)", xlabel: "sixteenths" });
        r.notes.forEach(function (n, i) { a.line([xs[i], xs[i] + n[1] * 0.92], [n[0], n[0]], { color: r.cover[i] ? "#E5484D" : C.idea, width: 5 }); });
      },
      readout: function (v, s) {
        var r = chainSample(v);
        return [["notes drawn", String(r.notes.length)], ["longest run copied from one tune", r.longest + " notes"],
                ["share inside a copied run of 8", (100 * r.share).toFixed(0) + " %"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Orders 0 and 1 wander and copy little; by order 4 or 5 most of the tune is a stretch of one of Bach's, because with so few tunes most long contexts were seen only once. The temperature trades safety for surprise, but cannot make a long-memory chain original."
    });
  };
  // Part 66: diffusion, exactly, on points in a plane -------------------------------------------------------------
  function diffuseRun(v) {
    var seed = Math.round(v.seed) * 104729 + 7, rnd = function () { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
    var gauss = function () { var u = Math.max(rnd(), 1e-12), w = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * w); };
    // the data: points on two rings, as a stand-in for the sounds a model learnt from
    var data = [];
    for (var i = 0; i < 120; i++) {
      var r = i < 60 ? 1.0 : 2.0, a = 2 * Math.PI * i / 60;
      data.push([r * Math.cos(a), r * Math.sin(a)]);
    }
    var T = Math.round(v.steps), beta = [], abar = [], acc = 1;
    for (var t = 0; t < T; t++) { var b = 1e-4 + (v.bmax - 1e-4) * t / Math.max(T - 1, 1); beta.push(b); acc *= (1 - b); abar.push(acc); }
    // the best possible denoiser for this data: the posterior mean of x0 given x_t, over the data points
    function eps(x, t) {
      var ab = abar[t], w = [], tot = 0, m = [0, 0];
      for (var j = 0; j < data.length; j++) {
        var dx = x[0] - Math.sqrt(ab) * data[j][0], dy = x[1] - Math.sqrt(ab) * data[j][1];
        w.push(-(dx * dx + dy * dy) / (2 * (1 - ab)));
      }
      var mx = Math.max.apply(null, w);
      for (j = 0; j < data.length; j++) { w[j] = Math.exp(w[j] - mx); tot += w[j]; }
      for (j = 0; j < data.length; j++) { m[0] += w[j] * data[j][0] / tot; m[1] += w[j] * data[j][1] / tot; }
      return [(x[0] - Math.sqrt(ab) * m[0]) / Math.sqrt(1 - ab), (x[1] - Math.sqrt(ab) * m[1]) / Math.sqrt(1 - ab)];
    }
    var pts = [];
    for (i = 0; i < Math.round(v.n); i++) pts.push([gauss() * 2, gauss() * 2]);
    var stopAt = Math.round((1 - v.shown) * T);
    for (t = T - 1; t >= stopAt; t--) {
      pts = pts.map(function (x) {
        var e = eps(x, t), b = beta[t], ab = abar[t];
        var y = [(x[0] - b / Math.sqrt(1 - ab) * e[0]) / Math.sqrt(1 - b), (x[1] - b / Math.sqrt(1 - ab) * e[1]) / Math.sqrt(1 - b)];
        if (t > 0) { y[0] += Math.sqrt(b) * gauss(); y[1] += Math.sqrt(b) * gauss(); }
        return y;
      });
    }
    // how many samples sit within 0.15 of a data point, and how many are within 0.02 of one (copies)
    var near = 0, copies = 0;
    pts.forEach(function (x) {
      var dmin = 1e9;
      data.forEach(function (p) { dmin = Math.min(dmin, Math.hypot(x[0] - p[0], x[1] - p[1])); });
      if (dmin < 0.15) near++;
      if (dmin < 0.02) copies++;
    });
    return { data: data, pts: pts, near: near, copies: copies, final_abar: abar[T - 1] };
  }
  W.diffuse = function (el) {
    QB.widget(el, {
      title: "Drawing by removing noise",
      sub: "Grey: the training data, points on two rings. Gold: samples, which start as pure noise and are denoised step by step by the best possible denoiser for this data. Slide 'Shown' to watch the reverse process from noise (0) to the end (1); change the number of steps and how much noise the forward process adds.",
      panels: 1, height: 300,
      controls: [{ k: "shown", label: "Shown", min: 0, max: 1, step: 0.05, value: 1, fmt: function (x) { return (100 * x).toFixed(0) + " % of the steps"; } },
                 { k: "steps", label: "Steps", min: 5, max: 200, step: 5, value: 100, fmt: function (x) { return x.toFixed(0); } },
                 { k: "bmax", label: "Noise at the last step", min: 0.01, max: 0.2, step: 0.01, value: 0.05, fmt: function (x) { return x.toFixed(2); } },
                 { k: "n", label: "Samples", min: 20, max: 300, step: 10, value: 150, fmt: function (x) { return x.toFixed(0); } },
                 { k: "seed", label: "Draw", min: 1, max: 20, step: 1, value: 1, fmt: function (x) { return x.toFixed(0); } }],
      draw: function (gr, v) {
        var r = diffuseRun(v);
        var a = gr[0].axes({ x: [-4, 4], y: [-3, 3], title: "data (grey) and samples (gold)" });
        a.dots(r.data.map(function (p) { return p[0]; }), r.data.map(function (p) { return p[1]; }), { r: 2, color: "#8A93A0" });
        a.dots(r.pts.map(function (p) { return p[0]; }), r.pts.map(function (p) { return p[1]; }), { r: 3, color: C.idea });
      },
      readout: function (v) {
        var r = diffuseRun(v);
        return [["samples near the data (within 0.15)", r.near + " of " + r.pts.length],
                ["samples that are copies of a data point (within 0.02)", String(r.copies)],
                ["signal left after all the forward noise", (100 * Math.sqrt(r.final_abar)).toFixed(1) + " %"]];
      },
      note: "With enough steps and enough noise, every sample ends on the rings. But this denoiser is perfect for the training points, and a perfect denoiser reproduces them: nearly every sample lands on a training point. A real network, which cannot memorize every example, generalizes between them; that gap is the copying question of Parts 65 and 66."
    });
  };
  // Part 67: a literature with selective publication -------------------------------------------------------------
  function funnelSim(v) {
    var seed = Math.round(v.seed) * 7907 + 3, rnd = function () { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
    var gauss = function () { var u = Math.max(rnd(), 1e-12), w = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * w); };
    var studies = [];
    for (var i = 0; i < Math.round(v.k); i++) {
      var n = Math.round(10 + rnd() * (v.nmax - 10)), se = Math.sqrt(2 / n), est = v.effect + se * gauss();
      var sig = est / se > 1.96;
      studies.push({ n: n, se: se, est: est, pub: sig || rnd() < v.pnull });
    }
    var pool = function (list) { var a = 0, b = 0; list.forEach(function (s) { a += s.est / (s.se * s.se); b += 1 / (s.se * s.se); }); return b ? a / b : NaN; };
    var pub = studies.filter(function (s) { return s.pub; });
    var first = studies.filter(function (s) { return s.est / s.se > 1.96; })[0];
    return { studies: studies, all: pool(studies), pub: pool(pub), npub: pub.length, first: first };
  }
  W.funnel = function (el) {
    QB.widget(el, {
      title: "A literature with selective publication",
      sub: "Each dot is a study of a two-group difference, its estimate across and its precision up (big studies at the top). Significant studies are always published; others only with the chance you set. Gold: published. Grey: in the file drawer. The vertical line is the true effect.",
      panels: 1, height: 300,
      controls: [{ k: "effect", label: "True effect", min: 0, max: 0.6, step: 0.02, value: 0.1, fmt: function (x) { return x.toFixed(2) + " sd"; } },
                 { k: "pnull", label: "Non-significant studies published", min: 0, max: 1, step: 0.05, value: 0.15, fmt: function (x) { return (100 * x).toFixed(0) + " %"; } },
                 { k: "k", label: "Studies run", min: 20, max: 400, step: 10, value: 120, fmt: function (x) { return x.toFixed(0); } },
                 { k: "nmax", label: "Largest study (a group)", min: 20, max: 1000, step: 10, value: 120, fmt: function (x) { return x.toFixed(0); } },
                 { k: "seed", label: "Draw", min: 1, max: 20, step: 1, value: 1, fmt: function (x) { return x.toFixed(0); } }],
      draw: function (gr, v) {
        var r = funnelSim(v), prec = r.studies.map(function (s) { return 1 / s.se; }), top = Math.max.apply(null, prec) * 1.05;
        var a = gr[0].axes({ x: [-1, 1.6], y: [0, top], title: "the funnel", xlabel: "estimated effect (sd)" });
        var un = r.studies.filter(function (s) { return !s.pub; }), pb = r.studies.filter(function (s) { return s.pub; });
        a.dots(un.map(function (s) { return s.est; }), un.map(function (s) { return 1 / s.se; }), { r: 2.5, color: "#5A6270" });
        a.dots(pb.map(function (s) { return s.est; }), pb.map(function (s) { return 1 / s.se; }), { r: 3, color: C.idea });
        a.vline(v.effect, { color: "#FFFFFF", width: 1.5, dash: [] });
        var ys = [], xs = [];
        for (var y = 0.6; y <= top; y += top / 40) { ys.push(y); xs.push(1.96 / y); }
        a.line(xs, ys, { color: "#E5484D", width: 1.5 });
      },
      readout: function (v) {
        var r = funnelSim(v);
        return [["published", r.npub + " of " + r.studies.length],
                ["pooled, all studies", r.all.toFixed(2)], ["pooled, the published", r.pub.toFixed(2)],
                ["the first significant study", r.first ? r.first.est.toFixed(2) + " (" + r.first.n + " a group)" : "none"]];
      },
      note: "With small studies and a file drawer, the published literature overstates a small effect, and its first significant result most of all. Publish the non-significant studies too, or run bigger ones, and the published estimate comes back to the truth. Set the true effect to zero: a literature can find an effect that is not there."
    });
  };
})();
