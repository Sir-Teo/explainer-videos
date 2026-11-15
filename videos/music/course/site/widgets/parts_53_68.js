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
})();
