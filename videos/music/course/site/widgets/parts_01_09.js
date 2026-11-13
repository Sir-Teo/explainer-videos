// Interactives for Act I, Sound (Parts 1-9).  Each one can be heard: the sound is computed in the page, from the
// same numbers the picture is drawn from, and played through the browser's Web Audio (after a click, as browsers
// require).  Nothing is downloaded.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, fmt = QB.fmt;
  var audio = null;

  // Play an array of samples in [-1, 1].  Returns false where the browser has no audio (the picture still works).
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

  // ---- Part 1: the plucked string ---------------------------------------------------------------------------
  var F1 = 130.81, SHOWN = 16;
  function amount(n, beta) { return 2 * Math.sin(n * Math.PI * beta) / (n * n * Math.PI * Math.PI * beta * (1 - beta)); }
  function triangle(z, beta) { // the plucked shape on [0, 1], continued as an odd function of period 2
    z = z - 2 * Math.floor(z / 2);
    var sign = 1; if (z > 1) { z = 2 - z; sign = -1; }
    return sign * (z <= beta ? z / beta : (1 - z) / (1 - beta));
  }
  function exact(x, tau, beta) { return 0.5 * (triangle(x - 2 * tau, beta) + triangle(x + 2 * tau, beta)); }
  function summed(x, tau, beta, modes) {
    var u = 0;
    for (var n = 1; n <= modes; n++) u += amount(n, beta) * Math.sin(n * Math.PI * x) * Math.cos(2 * Math.PI * n * tau);
    return u;
  }
  function pluckSound(beta, modes) { // the force on the bridge: partial n at sin(n pi beta)/n, the high ones dying first
    var rate = 44100, len = Math.floor(1.6 * rate), y = new Float32Array(len), n, i, peak = 0;
    for (n = 1; n <= modes; n++) {
      var a = Math.sin(n * Math.PI * beta) / n;
      if (Math.abs(a) < 1e-9 || n * F1 > 0.45 * rate) continue;
      var w = 2 * Math.PI * n * F1 / rate, dec = (0.9 + 0.003 * n * n * 9.87) / rate;
      for (i = 0; i < len; i++) y[i] += a * Math.exp(-dec * i) * Math.cos(w * i);
    }
    for (i = 0; i < len; i++) peak = Math.max(peak, Math.abs(y[i]));
    var gain = peak > 0 ? 0.3 / peak : 0, fade = Math.floor(0.004 * rate), tail = Math.floor(0.1 * rate);
    for (i = 0; i < len; i++) y[i] *= gain * Math.min(1, i / fade) * Math.min(1, (len - i) / tail);
    return play(y, rate);
  }
  W.pluckedstring = function (el) {
    QB.widget(el, {
      title: "Pluck a string: its shape, its modes, its sound",
      sub: "Left: an ideal string let go from a pluck. The dashed line is the true motion, two corners running round; the solid line is the sum of the modes you allow. Right: how much of each partial the bridge feels. Move the plucking point and watch partials vanish; cut the modes down and hear the tone go dull. Press Pluck to hear it.",
      panels: 2, height: 300,
      controls: [
        { k: "beta", label: "Where you pluck (fraction of the length)", min: 0.05, max: 0.5, step: 0.01, value: 0.2, fmt: function (x) { return fmt(x, 2); } },
        { k: "modes", label: "Modes in the sum", min: 1, max: 40, step: 1, value: 12 },
        { k: "tau", label: "Time (fraction of a period)", min: 0, max: 1, step: 0.01, value: 0, fmt: function (x) { return fmt(x, 2); } },
      ],
      buttons: [
        { label: "Pluck", act: function (s, v) { s.t = 0; s.run = true; s.sound = pluckSound(v.beta, v.modes); } },
      ],
      init: function (s) { s.t = 0; s.run = false; s.sound = null; },
      animate: function (v, s, dt) { // one pluck: three periods in slow motion
        if (!s.run) return false;
        s.t += dt / 2.2;
        if (s.t >= 3) { s.t = 0; s.run = false; }
        return s.run;
      },
      draw: function (g, v, s) {
        var tau = v.tau + (s.run ? s.t : 0), i, xs = [], ex = [], su = [], gap = 0;
        for (i = 0; i <= 200; i++) {
          var x = i / 200, e = exact(x, tau, v.beta), m = summed(x, tau, v.beta, v.modes);
          xs.push(x); ex.push(e); su.push(m);
        }
        for (i = 0; i <= 200; i++) gap = Math.max(gap, Math.abs(summed(i / 200, 0, v.beta, v.modes) - exact(i / 200, 0, v.beta)));
        s.gap = gap;
        var a = g[0].axes({ x: [0, 1], y: [-1.15, 1.15], title: "The string", xlabel: "position along the string", yticks: [-1, 0, 1] });
        a.hline(0, { dash: [2, 3] });
        a.line(xs, ex, { color: C.muted, width: 1.4, dash: [5, 4] });
        a.line(xs, su, { color: C.idea, width: 2.2 });
        a.dots([v.beta], [exact(v.beta, 0, v.beta)], { color: C.implied, r: 4, alpha: tau === 0 ? 1 : 0.35 });
        a.legend([["sum of " + v.modes + (v.modes === 1 ? " mode" : " modes"), C.idea], ["the true motion", C.muted]], { pos: "tr" });
        var ns = [], hs = [], top = 0, n;
        for (n = 1; n <= SHOWN; n++) { ns.push(n); hs.push(Math.abs(Math.sin(n * Math.PI * v.beta)) / n); top = Math.max(top, hs[n - 1]); }
        for (n = 0; n < SHOWN; n++) hs[n] /= top;
        var b = g[1].axes({ x: [0.3, SHOWN + 0.7], y: [0, 1.08], title: "What the bridge feels, partial by partial", xlabel: "partial", xticks: [1, 4, 8, 12, 16], yticks: [0, 0.5, 1] });
        b.bars(ns, hs, 0.7, { color: function (k) { return k < v.modes ? C.spot : C.line; } });
        var miss = [], cen = 0, tot = 0;
        for (n = 1; n <= SHOWN; n++) if (Math.abs(Math.sin(n * Math.PI * v.beta)) < 1e-6) miss.push(n);
        for (n = 1; n <= v.modes; n++) { var p = Math.pow(Math.sin(n * Math.PI * v.beta) / n, 2); cen += n * p; tot += p; }
        s.miss = miss; s.cen = tot > 0 ? cen / tot : 1;
      },
      readout: function (v, s) {
        return [["partials missing", s.miss && s.miss.length ? s.miss.join(", ") : "none"],
                ["brightness (mean partial number)", fmt(s.cen || 1, 2)],
                ["largest gap between the sum and the pluck", QB.pct(s.gap || 0, 1)],
                ["sound", s.sound === null ? "press Pluck" : (s.sound ? "playing C3, 130.8 Hz" : "not available in this browser")]];
      },
      note: "An ideal string fixed at both ends, released from rest. Mode n is present in the shape in the amount sin(nπβ)/n² and in the force on the bridge as sin(nπβ)/n, where β is the plucking point; a mode with a node there is missing. The sound is computed in your browser from the modes you allow, each dying away faster the higher it is, as on the film's string. Simulated.",
    });
  };

  // ---- Part 2: a bottle ---------------------------------------------------------------------------------------
  var CAIR = 343.2;
  function helm(An, Ln, V) { return CAIR / (2 * Math.PI) * Math.sqrt(An / (V * Ln)); }
  function twoTube(An, Ln, Ab, Lb) { // the smallest root of tan(k Ln) tan(k Lb) = An / Ab, by bisection
    var lo = 1e-6, hi = 0.999 * (Math.PI / 2) / Math.max(Ln, Lb), r = An / Ab, i, k;
    for (i = 0; i < 60; i++) { k = 0.5 * (lo + hi); if (Math.tan(k * Ln) * Math.tan(k * Lb) < r) lo = k; else hi = k; }
    return CAIR * 0.5 * (lo + hi) / (2 * Math.PI);
  }
  var NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  function noteOf(hz) {
    var m = 69 + 12 * Math.log(hz / 440) / Math.LN2, r = Math.round(m);
    return NOTE_NAMES[((r % 12) + 12) % 12] + (Math.floor(r / 12) - 1) + (m - r >= 0 ? " +" : " −") + fmt(Math.abs(100 * (m - r)), 0) + " cents";
  }
  function bottleSound(hz, blown) { // a slap: the resonance ringing down; a breath: noise through the same resonance
    var rate = 44100, len = Math.floor((blown ? 1.8 : 0.9) * rate), y = new Float32Array(len), i, peak = 0;
    var Q = 33, w = 2 * Math.PI * hz / rate, r = Math.exp(-w / (2 * Q)), a1 = 2 * r * Math.cos(w), a2 = -r * r, y1 = 0, y2 = 0, x;
    for (i = 0; i < len; i++) {
      x = blown ? (Math.random() * 2 - 1) * Math.min(1, i / (0.08 * rate)) * Math.min(1, (len - i) / (0.2 * rate)) : (i < 40 ? 0.5 * (1 - Math.cos(2 * Math.PI * i / 40)) : 0);
      y[i] = x + a1 * y1 + a2 * y2; y2 = y1; y1 = y[i];
    }
    for (i = 0; i < len; i++) peak = Math.max(peak, Math.abs(y[i]));
    for (i = 0; i < len; i++) y[i] *= 0.3 / (peak || 1);
    return play(y, rate);
  }
  W.bottle = function (el) {
    QB.widget(el, {
      title: "Tune a bottle: a mass of air on a spring of air",
      sub: "Left: a bottle of 330 ml and its note as you pour water in. Right: the note against how full it is, by Helmholtz's formula (dashed) and with the neck and body treated as two tubes (solid). Change the neck and watch both move. Slap it or blow across it to hear the note.",
      panels: 2, height: 300,
      controls: [
        { k: "fill", label: "How full the body is", min: 0, max: 0.8, step: 0.01, value: 0.2, fmt: function (x) { return QB.pct(x, 0); } },
        { k: "neck", label: "Neck length (cm)", min: 2, max: 12, step: 0.5, value: 6, fmt: function (x) { return fmt(x, 1); } },
        { k: "bore", label: "Neck width (mm)", min: 10, max: 30, step: 1, value: 18 },
      ],
      buttons: [
        { label: "Slap", act: function (s, v) { s.sound = bottleSound(s.hz, false); } },
        { label: "Blow", act: function (s, v) { s.sound = bottleSound(s.hz, true); } },
      ],
      init: function (s) { s.sound = null; s.hz = 172; },
      draw: function (g, v, s) {
        var rn = v.bore / 2000, An = Math.PI * rn * rn, Ln = v.neck / 100 + 1.46 * rn, Ab = Math.PI * 0.03 * 0.03, V = 330e-6, Lb = V / Ab;
        var fs = [], ex = [], lu = [], i, f;
        for (i = 0; i <= 40; i++) { f = 0.8 * i / 40; fs.push(f); ex.push(twoTube(An, Ln, Ab, Lb * (1 - f))); lu.push(helm(An, Ln, V * (1 - f))); }
        s.hz = twoTube(An, Ln, Ab, Lb * (1 - v.fill)); s.lumped = helm(An, Ln, V * (1 - v.fill));
        var a = g[0].axes({ x: [-1.2, 1.2], y: [0, 1.1], title: "The bottle", xticks: [], yticks: [] });
        var nh = Math.min(0.42, 0.035 * v.neck + 0.08), bh = 1.0 - nh, bw = 0.5, nw = Math.max(0.06, v.bore / 150);
        a.line([-bw, bw, bw, nw, nw, -nw, -nw, -bw, -bw], [0.02, 0.02, bh - 0.08, bh, 1.0, 1.0, bh, bh - 0.08, 0.02], { color: C.muted, width: 2 });
        var wy = 0.02 + v.fill * (bh - 0.1);
        a.line([-bw + 0.02, bw - 0.02], [wy, wy], { color: C.idea, width: 3 });
        a.line([-bw + 0.02, -bw + 0.02, bw - 0.02, bw - 0.02], [wy, 0.04, 0.04, wy], { color: C.idea, width: 1.2 });
        var b = g[1].axes({ x: [0, 0.8], y: [0, Math.max(400, 1.05 * lu[40])], title: "Its note as it fills", xlabel: "how full the body is", xticks: [0, 0.2, 0.4, 0.6, 0.8] });
        b.line(fs, lu, { color: C.muted, width: 1.4, dash: [5, 4] });
        b.line(fs, ex, { color: C.idea, width: 2.2 });
        b.dots([v.fill], [s.hz], { color: C.implied, r: 5 });
        b.legend([["two tubes, exact", C.idea], ["Helmholtz's formula", C.muted]], { pos: "tl" });
      },
      readout: function (v, s) {
        return [["its note", fmt(s.hz, 1) + " Hz  (" + noteOf(s.hz) + ")"],
                ["Helmholtz's formula says", fmt(s.lumped, 1) + " Hz, " + fmt(1200 * Math.log(s.lumped / s.hz) / Math.LN2, 0) + " cents sharp"],
                ["sound", s.sound === null ? "press Slap or Blow" : (s.sound ? "playing " + fmt(s.hz, 0) + " Hz" : "not available in this browser")]];
      },
      note: "A bottle of 330 ml with a body 6 cm wide; the neck's length includes 1.46 radii for the air that moves at its two ends. The solid curve is the lowest root of tan(kL_neck) tan(kL_body) = A_neck / A_body; Helmholtz's formula is its long-wavelength limit and runs sharp. The sound is one resonance with a quality factor of 33, struck or fed with noise, computed in your browser. Simulated.",
    });
  };
})();
