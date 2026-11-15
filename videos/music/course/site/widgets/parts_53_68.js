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
})();
