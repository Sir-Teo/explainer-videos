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

  // ---- Part 3: a sum of sines ---------------------------------------------------------------------------------
  var F3 = 196.0;
  function recipe(shape, n) { // amplitude of harmonic n
    if (shape === 0) return (n % 2) ? 4 / (Math.PI * n) : 0;                 // square
    if (shape === 1) return 2 / (Math.PI * n);                               // sawtooth
    return (n % 2) ? 8 / (Math.PI * Math.PI * n * n) * ((n % 4 === 1) ? 1 : -1) : 0;   // triangle
  }
  function targetWave(shape, x) {
    x = x - Math.floor(x);
    if (shape === 0) return x < 0.5 ? 1 : -1;
    if (shape === 1) return 1 - 2 * x;
    return x < 0.25 ? 4 * x : (x < 0.75 ? 2 - 4 * x : 4 * x - 4);
  }
  function phaseOf(n, scramble) { var r = Math.sin(n * 12.9898) * 43758.5453; return scramble * 2 * Math.PI * (r - Math.floor(r)); }
  function sumWave(shape, terms, scramble, x) {
    var y = 0, n;
    for (n = 1; n <= terms; n++) y += recipe(shape, n) * Math.sin(2 * Math.PI * n * x + phaseOf(n, scramble));
    return y;
  }
  function sumSound(shape, terms, scramble) {
    var rate = 44100, len = Math.floor(1.4 * rate), y = new Float32Array(len), n, i, peak = 0;
    for (n = 1; n <= terms; n++) {
      var a = recipe(shape, n); if (a === 0 || n * F3 > 0.45 * rate) continue;
      var w = 2 * Math.PI * n * F3 / rate, ph = phaseOf(n, scramble);
      for (i = 0; i < len; i++) y[i] += a * Math.sin(w * i + ph);
    }
    for (i = 0; i < len; i++) peak = Math.max(peak, Math.abs(y[i]));
    var fade = Math.floor(0.01 * rate), tail = Math.floor(0.08 * rate);
    for (i = 0; i < len; i++) y[i] *= (0.28 / (peak || 1)) * Math.min(1, i / fade) * Math.min(1, (len - i) / tail);
    return play(y, rate);
  }
  var SHAPES = ["square", "sawtooth", "triangle"];
  W.fouriersum = function (el) {
    QB.widget(el, {
      title: "Build a wave from pure tones",
      sub: "Left: the sum of the first few sines of a square, a sawtooth or a triangle wave, against the wave itself. Right: the recipe, the amount of each harmonic. Add terms and watch the corners form (and the overshoot at a jump refuse to shrink). Scramble the phases: the recipe on the right does not change, the wave on the left does. Press Play to hear what does and does not change.",
      panels: 2, height: 300,
      controls: [
        { k: "shape", label: "Wave (0 square, 1 sawtooth, 2 triangle)", min: 0, max: 2, step: 1, value: 0, fmt: function (x) { return SHAPES[x]; } },
        { k: "terms", label: "Harmonics in the sum", min: 1, max: 40, step: 1, value: 5 },
        { k: "scramble", label: "Scramble the phases", min: 0, max: 1, step: 0.05, value: 0, fmt: function (x) { return fmt(x, 2); } },
      ],
      buttons: [
        { label: "Play", act: function (s, v) { s.sound = sumSound(v.shape, v.terms, v.scramble); } },
      ],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        var xs = [], ys = [], ts = [], i, top = 0;
        for (i = 0; i <= 400; i++) { var x = 2 * i / 400; xs.push(x); ys.push(sumWave(v.shape, v.terms, v.scramble, x)); ts.push(targetWave(v.shape, x)); top = Math.max(top, Math.abs(ys[i])); }
        s.over = v.scramble === 0 ? Math.max(0, top - 1) / 2 : null;
        var a = g[0].axes({ x: [0, 2], y: [-1.6, 1.6], title: "The wave", xlabel: "two periods", xticks: [0, 1, 2], yticks: [-1, 0, 1] });
        a.hline(0, { dash: [2, 3] });
        a.line(xs, ts, { color: C.muted, width: 1.4, dash: [5, 4] });
        a.line(xs, ys, { color: C.idea, width: 2.2 });
        a.legend([["sum of " + v.terms + (v.terms === 1 ? " harmonic" : " harmonics"), C.idea], ["the " + SHAPES[v.shape] + " wave", C.muted]], { pos: "tr" });
        var ns = [], hs = [], cen = 0, tot = 0, n, big = Math.abs(recipe(v.shape, 1));
        for (n = 1; n <= 20; n++) { ns.push(n); hs.push(Math.abs(recipe(v.shape, n)) / big); }
        for (n = 1; n <= v.terms; n++) { var p = Math.pow(recipe(v.shape, n), 2); cen += n * p; tot += p; }
        s.cen = tot > 0 ? cen / tot : 1;
        var b = g[1].axes({ x: [0.3, 20.7], y: [0, 1.08], title: "The recipe: how much of each harmonic", xlabel: "harmonic", xticks: [1, 5, 10, 15, 20], yticks: [0, 0.5, 1] });
        b.bars(ns, hs, 0.7, { color: function (k) { return k < v.terms ? C.spot : C.line; } });
      },
      readout: function (v, s) {
        return [["brightness (mean harmonic number)", fmt(s.cen || 1, 2)],
                ["overshoot at the jump", s.over === null ? "phases scrambled" : (v.shape === 2 ? "none: a triangle has no jump" : QB.pct(s.over, 1) + " of the jump")],
                ["phases", v.scramble === 0 ? "as Fourier's recipe gives them" : "scrambled: same recipe, different wave"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing G3, 196 Hz" : "not available in this browser")]];
      },
      note: "Fourier series of three waves: a square (odd harmonics, 1/n), a sawtooth (all harmonics, 1/n) and a triangle (odd harmonics, 1/n²). The overshoot beside a jump settles near 9 percent however many terms are used (Gibbs). Scrambling the phases leaves the amount of every harmonic untouched; on this note the ear hears little difference, and on a much lower note it would hear more. The sound is computed in your browser. Simulated.",
    });
  };

  // ---- Part 4: a pitch that is not in the sound ---------------------------------------------------------------
  // The note's partials, the lowest of them removed or all of them moved; the pitch is read where the wave's
  // autocorrelation first comes back to its height (Licklider's idea, on the wave itself rather than on a model of
  // the nerve).
  function partialsOf(v) {
    var out = [], n;
    for (n = v.lowest; n < v.lowest + v.count; n++) out.push(n * v.f0 + v.shift);
    return out;
  }
  function acfAt(freqs, tau) { var a = 0, i; for (i = 0; i < freqs.length; i++) a += Math.cos(2 * Math.PI * freqs[i] * tau); return a / freqs.length; }
  function pitchOf(freqs, lo, hi) { // the first delay at which the wave nearly repeats (within 3% of the best)
    var n = 4000, best = -2, bestTau = 1 / hi, i, tau, a, vals = [];
    for (i = 0; i <= n; i++) { tau = 1 / hi + (1 / lo - 1 / hi) * i / n; a = acfAt(freqs, tau); vals.push(a); if (a > best) { best = a; bestTau = tau; } }
    for (i = 1; i < n; i++) {
      if (vals[i] > vals[i - 1] && vals[i] >= vals[i + 1] && vals[i] > best - 0.03) { bestTau = 1 / hi + (1 / lo - 1 / hi) * i / n; best = vals[i]; break; }
    }
    return { hz: 1 / bestTau, height: best };
  }
  function toneSound(freqs) {
    var rate = 44100, len = Math.floor(1.3 * rate), y = new Float32Array(len), i, k, peak = 0;
    for (k = 0; k < freqs.length; k++) {
      if (freqs[k] > 0.45 * rate) continue;
      var w = 2 * Math.PI * freqs[k] / rate;
      for (i = 0; i < len; i++) y[i] += Math.sin(w * i);
    }
    for (i = 0; i < len; i++) peak = Math.max(peak, Math.abs(y[i]));
    var fade = Math.floor(0.02 * rate), tail = Math.floor(0.08 * rate);
    for (i = 0; i < len; i++) y[i] *= (0.25 / (peak || 1)) * Math.min(1, i / fade) * Math.min(1, (len - i) / tail);
    return play(y, rate);
  }
  W.missingfund = function (el) {
    QB.widget(el, {
      title: "A note without its fundamental",
      sub: "Left: the partials of a note. Raise the lowest partial and the bottom of the note disappears; the dashed lines are what was removed. Right: how well the wave lines up with a delayed copy of itself. Its first full return marks the period, and so the pitch, although no partial may be there. Then move every partial up by the same number of hertz: the spacing stays, the pitch does not. Press Play to compare the sound with a pure tone at the pitch.",
      panels: 2, height: 300,
      controls: [
        { k: "f0", label: "The note (Hz)", min: 100, max: 400, step: 10, value: 200 },
        { k: "lowest", label: "Lowest partial present", min: 1, max: 8, step: 1, value: 4 },
        { k: "count", label: "Number of partials", min: 1, max: 8, step: 1, value: 5 },
        { k: "shift", label: "Move every partial up (Hz)", min: 0, max: 100, step: 5, value: 0 },
      ],
      buttons: [
        { label: "Play the partials", act: function (s, v) { s.sound = toneSound(partialsOf(v)); } },
        { label: "Play a pure tone at the pitch", act: function (s, v) { s.sound = toneSound([pitchOf(partialsOf(v), v.f0 / 2.2, v.f0 * 2.2).hz]); } },
      ],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        var fs = partialsOf(v), top = Math.max(2000, fs[fs.length - 1] * 1.1), n, i;
        var a = g[0].axes({ x: [0, top], y: [0, 1.15], title: "What is in the sound", xlabel: "frequency (Hz)", yticks: [] });
        for (n = 1; n < v.lowest; n++) a.line([n * v.f0, n * v.f0], [0, 1], { color: C.muted, width: 1.2, dash: [3, 4] });
        for (i = 0; i < fs.length; i++) a.line([fs[i], fs[i]], [0, 1], { color: v.shift === 0 ? C.idea : C.loss, width: 3 });
        var p = pitchOf(fs, v.f0 / 2.2, v.f0 * 2.2);
        s.p = p;
        a.line([p.hz, p.hz], [0, 0.45], { color: C.gain, width: 2, dash: [2, 3] });
        a.legend([["partials present", v.shift === 0 ? C.idea : C.loss], ["removed", C.muted], ["the pitch heard", C.gain]], { pos: "tr" });
        var xs = [], ys = [], tmax = 2.4 / v.f0;
        for (i = 0; i <= 600; i++) { var tau = tmax * i / 600; xs.push(1000 * tau); ys.push(acfAt(fs, tau)); }
        var b = g[1].axes({ x: [0, 1000 * tmax], y: [-1.1, 1.15], title: "The wave against a delayed copy of itself", xlabel: "delay (ms)", yticks: [-1, 0, 1] });
        b.hline(0, { dash: [2, 3] });
        b.line(xs, ys, { color: C.spot, width: 2 });
        b.vline(1000 / p.hz, { color: C.gain, width: 1.6 });
        b.vline(1000 / v.f0, { color: C.muted });
      },
      readout: function (v, s) {
        var fs = partialsOf(v), p = s.p || pitchOf(fs, v.f0 / 2.2, v.f0 * 2.2), cents = 1200 * Math.log(p.hz / v.f0) / Math.log(2);
        return [["partials", fs.map(function (f) { return fmt(f, 0); }).join(", ") + " Hz"],
                ["energy at the note's own frequency", (v.lowest === 1 && v.shift === 0) ? "yes" : "none"],
                ["pitch (first return of the wave)", fmt(p.hz, 1) + " Hz, " + (Math.abs(cents) < 0.5 ? "the note" : fmt(Math.abs(cents), 0) + " cents " + (cents > 0 ? "above" : "below") + " the note")],
                ["spacing of the partials", fmt(v.f0, 0) + " Hz, whatever the shift"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "A note's pitch is the period of its wave, not its lowest partial: remove partials 1, 2 and 3 and the wave still repeats at the same rate (Seebeck 1841; Schouten 1940). Moving every partial up by the same amount keeps their spacing but changes the delay at which the wave best lines up with itself, and listeners hear the pitch rise by about the shift divided by the number of the middle partial (Schouten's shifted residue). With one partial alone the pitch is that partial; with only high partials (lowest 7 or 8) real listeners hear a weaker pitch than this simple calculation suggests, because the ear no longer resolves them. The sound is computed in your browser. Simulated.",
    });
  };

  // ---- Part 5: a dissonance curve you can bend ------------------------------------------------------------------
  // Plomp and Levelt's curve as fitted by Sethares (1993), summed over every pair of partials of two tones.
  function pairRough(f1, f2, a1, a2) {
    var lo = Math.min(f1, f2), s = 0.24 / (0.0207 * lo + 18.96), d = Math.abs(f2 - f1);
    return Math.min(a1, a2) * (Math.exp(-3.5 * s * d) - Math.exp(-5.75 * s * d));
  }
  function tonePartials(f0, n, roll, stretch) {
    var fs = [], as = [], k, p = Math.log(stretch) / Math.log(2);
    for (k = 1; k <= n; k++) { fs.push(f0 * Math.pow(k, p)); as.push(Math.pow(roll, k - 1)); }
    return { f: fs, a: as };
  }
  function dyadRough(ratio, t) {
    var i, j, n = t.f.length, r = 0;
    for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) r += pairRough(t.f[i], t.f[j], t.a[i], t.a[j]) + pairRough(ratio * t.f[i], ratio * t.f[j], t.a[i], t.a[j]);
    for (i = 0; i < n; i++) for (j = 0; j < n; j++) r += pairRough(t.f[i], ratio * t.f[j], t.a[i], t.a[j]);
    return r;
  }
  function dyadSound(ratio, t) {
    var rate = 44100, len = Math.floor(1.8 * rate), y = new Float32Array(len), i, k, peak = 0;
    for (k = 0; k < t.f.length; k++) {
      var w1 = 2 * Math.PI * t.f[k] / rate, w2 = w1 * ratio, a = t.a[k];
      for (i = 0; i < len; i++) y[i] += a * ((t.f[k] < 0.45 * rate ? Math.sin(w1 * i) : 0) + (t.f[k] * ratio < 0.45 * rate ? Math.sin(w2 * i) : 0));
    }
    for (i = 0; i < len; i++) peak = Math.max(peak, Math.abs(y[i]));
    var fade = Math.floor(0.03 * rate), tail = Math.floor(0.12 * rate);
    for (i = 0; i < len; i++) y[i] *= (0.25 / (peak || 1)) * Math.min(1, i / fade) * Math.min(1, (len - i) / tail);
    return play(y, rate);
  }
  var JUSTS = [[1, 1], [6, 5], [5, 4], [4, 3], [3, 2], [5, 3], [2, 1]];
  W.dissonance = function (el) {
    QB.widget(el, {
      title: "Move the valleys",
      sub: "Left: the roughness of two tones against the interval between them, summed over every pair of their partials; the dotted lines are the just ratios. Right: the partials of the two tones at the interval you have chosen. With whole-multiple partials (stretch 2) the valleys sit on the just ratios. Change the stretch and the valleys move; give the tone one partial and they vanish. Press Play to hear the interval in this timbre.",
      panels: 2, height: 300,
      controls: [
        { k: "cents", label: "Interval (cents)", min: 0, max: 1400, step: 5, value: 700 },
        { k: "stretch", label: "Stretch of the partials (2 = harmonic)", min: 1.8, max: 2.3, step: 0.01, value: 2, fmt: function (x) { return fmt(x, 2); } },
        { k: "n", label: "Partials in each tone", min: 1, max: 10, step: 1, value: 7 },
        { k: "f0", label: "Lower note (Hz)", min: 65, max: 520, step: 5, value: 260 },
      ],
      buttons: [
        { label: "Play the two notes", act: function (s, v) { s.sound = dyadSound(Math.pow(2, v.cents / 1200), tonePartials(v.f0, v.n, 0.88, v.stretch)); } },
      ],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        var t = tonePartials(v.f0, v.n, 0.88, v.stretch), xs = [], ys = [], i, top = 0, best = null;
        for (i = 0; i <= 560; i++) { var c = 1400 * i / 560, r = dyadRough(Math.pow(2, c / 1200), t); xs.push(c); ys.push(r); top = Math.max(top, r); }
        var ratio = Math.pow(2, v.cents / 1200), here = dyadRough(ratio, t);
        for (i = 1; i < 560; i++) if (ys[i] < ys[i - 1] && ys[i] <= ys[i + 1] && (best === null || Math.abs(xs[i] - v.cents) < Math.abs(best - v.cents))) best = xs[i];
        s.here = here; s.top = top; s.best = best;
        var a = g[0].axes({ x: [0, 1400], y: [0, top * 1.12 + 1e-6], title: "Roughness against interval", xlabel: "interval (cents)", xticks: [0, 200, 400, 600, 800, 1000, 1200, 1400], yticks: [] });
        for (i = 0; i < JUSTS.length; i++) a.vline(1200 * Math.log(JUSTS[i][0] / JUSTS[i][1]) / Math.log(2), { color: C.muted });
        a.line(xs, ys, { color: C.loss, width: 2 });
        a.vline(v.cents, { color: C.idea, width: 2, dash: [1, 0] });
        var fmax = Math.max(t.f[t.f.length - 1] * ratio * 1.05, 4 * v.f0);
        var b = g[1].axes({ x: [0, fmax], y: [0, 1.15], title: "The partials of the two tones", xlabel: "frequency (Hz)", yticks: [] });
        for (i = 0; i < t.f.length; i++) {
          b.line([t.f[i], t.f[i]], [0, t.a[i]], { color: C.spot, width: 3 });
          b.line([t.f[i] * ratio, t.f[i] * ratio], [0, t.a[i] * 0.92], { color: C.idea, width: 3 });
        }
        b.legend([["lower tone", C.spot], ["upper tone", C.idea]], { pos: "tr" });
      },
      readout: function (v, s) {
        var ratio = Math.pow(2, v.cents / 1200);
        return [["interval", fmt(v.cents, 0) + " cents, a ratio of " + fmt(ratio, 3)],
                ["roughness here", fmt(100 * (s.here || 0) / (s.top || 1), 0) + "% of the worst interval"],
                ["nearest valley", s.best === null ? "none: a pure tone has no valleys beyond the first band" : fmt(s.best, 0) + " cents (" + fmt(Math.pow(2, s.best / 1200), 3) + ")"],
                ["the octave of this timbre", fmt(v.stretch, 2) + " : 1, " + fmt(1200 * Math.log(v.stretch) / Math.log(2), 0) + " cents"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "The roughness of two pure tones follows Plomp and Levelt's curve (1965), in the form fitted by Sethares (1993): none in unison, worst about a quarter of a critical band apart, gone by about one band. For two tones with partials it is added up over every pair. With one partial the curve has a single hump and no special intervals. With whole-multiple partials its valleys are the just ratios (the dotted lines). Stretch the partials and each valley moves to its old ratio raised to the power log2(stretch): a timbre has its own consonances. Lower the bottom note and the valleys fill in, because the ear's bands are wider in the bass. Roughness is one ingredient of consonance; harmonicity and familiarity are the others. The sound is computed in your browser. Simulated.",
    });
  };

  // ---- Part 6: where to hide the comma ----------------------------------------------------------------------------
  // A chain of eleven fifths, E flat to G sharp, each narrowed by a fraction of the syntonic comma; the twelfth
  // fifth (G sharp to E flat) takes whatever is left.
  var CHAIN = ["E♭", "B♭", "F", "C", "G", "D", "A", "E", "B", "F♯", "C♯", "G♯"];
  var PURE5 = 1200 * Math.log(1.5) / Math.LN2, PURE3 = 1200 * Math.log(1.25) / Math.LN2, SYN = 1200 * Math.log(81 / 80) / Math.LN2;
  function temper(x) { // cents above C of each note of the chain, and the sizes of the twelve fifths and thirds
    var size = PURE5 - x * SYN, pos = [], i;
    for (i = 0; i < 12; i++) pos.push((((i - 3) * size) % 1200 + 1200) % 1200);
    var fifths = [], thirds = [];
    for (i = 0; i < 12; i++) {
      fifths.push(((pos[(i + 1) % 12] - pos[i]) % 1200 + 1200) % 1200 - PURE5);
      thirds.push(((pos[(i + 4) % 12] - pos[i]) % 1200 + 1200) % 1200 - PURE3);
    }
    return { size: size, pos: pos, fifths: fifths, thirds: thirds };
  }
  function triadSound(t, k) {
    var c4 = 261.6256, f = [t.pos[k], t.pos[(k + 4) % 12], t.pos[(k + 1) % 12]].map(function (c) { return c4 * Math.pow(2, c / 1200); }), i, j, n;
    for (i = 1; i < 3; i++) while (f[i] < f[i - 1]) f[i] *= 2;
    if (f[0] > c4 * 1.6) f = f.map(function (x) { return x / 2; });
    var rate = 44100, len = Math.floor(2.0 * rate), y = new Float32Array(len), peak = 0;
    for (j = 0; j < 3; j++) for (n = 1; n <= 7; n++) {
      var w = 2 * Math.PI * f[j] * n / rate, a = Math.pow(0.88, n - 1);
      for (i = 0; i < len; i++) y[i] += a * Math.sin(w * i);
    }
    for (i = 0; i < len; i++) peak = Math.max(peak, Math.abs(y[i]));
    var fade = Math.floor(0.03 * rate), tail = Math.floor(0.12 * rate);
    for (i = 0; i < len; i++) y[i] *= (0.25 / (peak || 1)) * Math.min(1, i / fade) * Math.min(1, (len - i) / tail);
    return play(y, rate);
  }
  function nameOf(x) {
    if (x < 0.005) return "Pythagorean tuning: every fifth pure";
    if (Math.abs(x - 1 / 11) < 0.006) return "very nearly twelve equal steps";
    if (Math.abs(x - 1 / 6) < 0.006) return "sixth-comma meantone";
    if (Math.abs(x - 1 / 4) < 0.006) return "quarter-comma meantone: pure major thirds";
    if (Math.abs(x - 1 / 3) < 0.006) return "third-comma meantone: pure minor thirds";
    return "a meantone temperament";
  }
  W.temperament = function (el) {
    QB.widget(el, {
      title: "Where to hide the comma",
      sub: "Eleven fifths in a chain, each narrowed by a fraction of the comma; the twelfth takes what is left. Left: how far each of the twelve fifths is from pure. Right: how far the major third on each note is from pure. At nothing, the fifths are pure and the thirds a comma wide. At a quarter, eight thirds are pure and four are wolves. Near one eleventh, everything is equal. Choose a key and press Play to hear its chord.",
      panels: 2, height: 300,
      controls: [
        { k: "x", label: "Fraction of the comma taken from each fifth", min: 0, max: 0.34, step: 0.005, value: 0.25, fmt: function (x) { return fmt(x, 3); } },
        { k: "key", label: "Key of the chord", min: 0, max: 11, step: 1, value: 3, fmt: function (k) { return CHAIN[k] + " major"; } },
      ],
      buttons: [
        { label: "Play the chord", act: function (s, v) { s.sound = triadSound(temper(v.x), v.key); } },
      ],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        var t = temper(v.x), idx = [], i;
        s.t = t;
        for (i = 0; i < 12; i++) idx.push(i);
        var a = g[0].axes({ x: [-0.7, 11.7], y: [-45, 45], title: "The twelve fifths: cents from pure", xlabel: "the fifth above each note, E♭ to G♯", xticks: [], yticks: [-40, -20, 0, 20, 40] });
        a.hline(0, {});
        a.bars(idx, t.fifths, 0.7, { color: function (k) { return k === 11 ? C.loss : C.spot; } });
        var b = g[1].axes({ x: [-0.7, 11.7], y: [-12, 45], title: "The twelve major thirds: cents from pure", xlabel: "the third above each note, E♭ to G♯", xticks: [], yticks: [0, 20, 40] });
        b.hline(0, {});
        b.bars(idx, t.thirds, 0.7, { color: function (k) { return k === v.key ? C.idea : (Math.abs(t.thirds[k]) > 25 ? C.loss : C.gain); } });
      },
      readout: function (v, s) {
        var t = s.t || temper(v.x);
        return [["this is", nameOf(v.x)],
                ["each fifth", fmt(t.size, 1) + " cents (" + fmt(t.size - PURE5, 1) + " from pure)"],
                ["the twelfth fifth, G♯ to E♭", fmt(t.fifths[11], 1) + " cents from pure" + (Math.abs(t.fifths[11]) > 15 ? ": a wolf" : "")],
                ["the chord on " + CHAIN[v.key], "third " + fmt(t.thirds[v.key], 1) + ", fifth " + fmt(t.fifths[v.key], 1) + " cents from pure"],
                ["sound", s.sound === null ? "press Play" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Four pure fifths overshoot a pure major third by the syntonic comma, 21.5 cents, and twelve pure fifths overshoot seven octaves by the Pythagorean comma, 23.5 cents. Narrowing each of eleven fifths by a fraction x of the syntonic comma improves the eight thirds that lie inside the chain and pushes the error into the twelfth fifth and the four thirds that cross it. x = 0 is Pythagorean tuning; x = 1/4 is quarter-comma meantone (Aron, 1523); x = 1/3 makes the minor thirds pure; x close to 1/11 shares the Pythagorean comma among all twelve fifths, which is equal temperament. Well temperaments such as Werckmeister's narrow only some of the fifths, and are not on this slider. The sound is computed in your browser. Simulated.",
    });
  };

  // ---- Part 7: a bow on a string ------------------------------------------------------------------------------
  // Velocity waves travel both ways from the bow; at the bow the string must satisfy the string (a straight line)
  // and the rosin (a falling curve of friction against sliding speed), keeping its state where both would do.
  var BOW = { z: 0.25, muS: 0.8, muD: 0.3, v0: 0.05, gBridge: 0.97, aBridge: 0.1, gNut: 0.995, hz: 196, half: 225 };
  function schellengLimits(beta, speed) {
    var r = BOW.z * (1 + BOW.gBridge) / (1 - BOW.gBridge);
    return { max: 2 * BOW.z * speed / (beta * (BOW.muS - BOW.muD)), min: BOW.z * BOW.z * speed / (2 * r * beta * beta * (BOW.muS - BOW.muD)) };
  }
  function bowString(beta, force, speed, seconds) {
    var half = BOW.half, rate = 2 * BOW.hz * half, n1 = Math.max(Math.round(beta * half), 1), n2 = half - n1, steps = Math.floor(seconds * rate);
    var toB = new Float64Array(n1), fromB = new Float64Array(n1), toN = new Float64Array(n2), fromN = new Float64Array(n2);
    var v = new Float32Array(steps), bridge = new Float32Array(steps), slip = new Uint8Array(steps);
    var start = Math.max(force, 0.6 * schellengLimits(n1 / half, speed).max), ease = Math.log(force / start), attack = 0.3 * rate;
    var i1 = 0, i2 = 0, lp = 0, stick = true, s, z = BOW.z;
    for (s = 0; s < steps; s++) {
      var fb = start * Math.exp(ease * Math.min(1, s / attack)), k = fb / (2 * z);
      var vib = fromB[i1], vin = fromN[i2], vh = vib + vin, a = speed - vh, f2, sg = a >= 0 ? 1 : -1, aa = a * sg;
      var b = aa - k * BOW.muD - BOW.v0, disc = b * b + 4 * BOW.v0 * (aa - k * BOW.muS);
      if (aa > k * BOW.muS) { f2 = sg * (aa - 0.5 * (b + Math.sqrt(disc))); stick = false; }
      else if (!stick && disc >= 0 && b > 0) f2 = sg * (aa - 0.5 * (b + Math.sqrt(disc)));
      else { f2 = a; stick = true; }
      v[s] = vh + f2; slip[s] = stick ? 0 : 1;
      var arrB = toB[i1], arrN = toN[i2];
      lp = (1 - BOW.aBridge) * arrB + BOW.aBridge * lp;
      fromB[i1] = -BOW.gBridge * lp; fromN[i2] = -BOW.gNut * arrN;
      toB[i1] = vin + f2; toN[i2] = vib + f2;
      bridge[s] = z * (arrB + BOW.gBridge * lp);
      if (++i1 === n1) i1 = 0;
      if (++i2 === n2) i2 = 0;
    }
    // what it settled into: the last thirty periods
    var P = 2 * half, from = steps - 30 * P, slips = 0, i, lag, best = P, top = -1e300, mean = 0;
    for (i = from; i < steps; i++) { slips += slip[i]; mean += bridge[i]; }
    mean /= 30 * P;
    for (lag = Math.round(0.96 * P); lag <= Math.round(1.6 * P); lag++) {
      var acc = 0;
      for (i = from + lag; i < steps; i += 3) acc += (bridge[i] - mean) * (bridge[i - lag] - mean);
      acc /= (steps - from - lag);
      if (acc > top * 1.0005) { top = acc; best = lag; }
    }
    var frac = slips / (30 * P), realBeta = n1 / half, pitch = P / best, kind;
    if (frac < 1e-6) kind = "stuck: the bow never lets go";
    else if (Math.abs(pitch - 1) > 0.01 || frac < 0.75 * realBeta) kind = "too hard: the string cannot let go on time";
    else if (frac > 1.3 * realBeta) kind = "too lightly: the string slips more than once a period";
    else kind = "the Helmholtz motion";
    return { v: v, bridge: bridge, rate: rate, period: P, frac: frac, beta: realBeta, pitch: pitch, kind: kind, ok: kind === "the Helmholtz motion" };
  }
  function bowSound(d) { // the force on the bridge, at half the simulation's rate, through a few resonances standing for a violin's body
    var rate = d.rate / 2, len = Math.floor(d.bridge.length / 2), x = new Float32Array(len), y = new Float32Array(len), i, j, peak = 0, mean = 0;
    for (i = 0; i < len; i++) { x[i] = 0.5 * (d.bridge[2 * i] + d.bridge[2 * i + 1]); mean += x[i]; }
    mean /= len;
    var modes = [[275, 18, 1.0], [460, 22, 1.3], [540, 22, 1.5], [1100, 10, 0.7], [2500, 3, 2.2]];
    for (j = 0; j < modes.length; j++) {
      var w = 2 * Math.PI * modes[j][0] / rate, r = Math.exp(-w / (2 * modes[j][1])), a1 = 2 * r * Math.cos(w), a2 = -r * r, g = modes[j][2] * (1 - r), y1 = 0, y2 = 0, x1 = 0;
      for (i = 0; i < len; i++) { var xi = x[i] - mean, out = g * (xi - x1) + a1 * y1 + a2 * y2; x1 = xi; y2 = y1; y1 = out; y[i] += out; }
    }
    for (i = 0; i < len; i++) peak = Math.max(peak, Math.abs(y[i]));
    var fade = Math.floor(0.05 * rate), tail = Math.floor(0.1 * rate);
    for (i = 0; i < len; i++) y[i] *= (0.3 / (peak || 1)) * Math.min(1, i / fade) * Math.min(1, (len - i) / tail);
    return play(y, rate);
  }
  W.bow = function (el) {
    QB.widget(el, {
      title: "Inside Schelleng's wedge",
      sub: "A string under a bow, simulated as you move the sliders. Left: the speed of the string at the bow through two periods. In the Helmholtz motion it rides with the bow, then flies back once. Right: Schelleng's diagram, with his two limits for the bow speed you have chosen and a dot where you are. Push the force up through the top of the wedge, or let it fall through the bottom, and watch what the string does instead. Press Bow to hear it.",
      panels: 2, height: 300,
      controls: [
        { k: "beta", label: "Where the bow is: fraction of the string from the bridge", min: 0.04, max: 0.3, step: 0.01, value: 0.1, fmt: function (x) { return fmt(x, 2); } },
        { k: "lf", label: "Bow force (N)", min: -2, max: 1.2, step: 0.02, value: -0.04, fmt: function (x) { return fmt(Math.pow(10, x), Math.pow(10, x) < 0.1 ? 3 : 2); } },
        { k: "speed", label: "Bow speed (m/s)", min: 0.05, max: 0.5, step: 0.01, value: 0.2, fmt: function (x) { return fmt(x, 2); } },
      ],
      buttons: [
        { label: "Bow the string", act: function (s, v) { s.sound = bowSound(bowString(v.beta, Math.pow(10, v.lf), v.speed, 1.5)); } },
      ],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        var force = Math.pow(10, v.lf), d = bowString(v.beta, force, v.speed, 0.8), P = d.period, n = d.v.length, xs = [], ys = [], i, lo = 0, hi = v.speed;
        for (i = 0; i < 2 * P; i++) { var y = d.v[n - 2 * P + i]; xs.push(i / P); ys.push(y); lo = Math.min(lo, y); hi = Math.max(hi, y); }
        s.d = d;
        var a = g[0].axes({ x: [0, 2], y: [lo * 1.1 - 0.05, hi * 1.3 + 0.1], title: "The string's speed under the bow (m/s)", xlabel: "time (periods of the open string)", xticks: [0, 0.5, 1, 1.5, 2] });
        a.hline(v.speed, { color: C.gain });
        a.line(xs, ys, { color: d.ok ? C.idea : C.loss, width: 2 });
        var bs = [], mx = [], mn = [];
        for (i = 0; i <= 40; i++) { var be = 0.035 * Math.pow(0.32 / 0.035, i / 40), L = schellengLimits(be, v.speed); bs.push(be); mx.push(L.max); mn.push(L.min); }
        var b = g[1].axes({ x: [0.035, 0.32], y: [0.005, 20], logx: true, logy: true, title: "Bow force (N) against bow position", xlabel: "fraction of the string from the bridge",
                            xticks: [0.04, 0.07, 0.1, 0.2, 0.3], yticks: [0.01, 0.1, 1, 10] });
        b.area(bs, mx, mn, { color: C.gain, alpha: 0.14 });
        b.line(bs, mx, { color: C.loss, width: 1.8 });
        b.line(bs, mn, { color: C.spot, width: 1.8 });
        b.dots([d.beta], [force], { color: d.ok ? C.idea : C.loss, r: 5 });
        b.legend([["Schelleng's largest force", C.loss], ["his smallest", C.spot]], { pos: "tr" });
      },
      readout: function (v, s) {
        var d = s.d || bowString(v.beta, Math.pow(10, v.lf), v.speed, 0.8), L = schellengLimits(d.beta, v.speed);
        return [["the string is in", d.kind],
                ["it slips for", fmt(100 * d.frac, 1) + "% of each period (Helmholtz: " + fmt(100 * d.beta, 1) + "%)"],
                ["its pitch", fmt(196 * d.pitch, 1) + " Hz (the open string: 196.0)"],
                ["Schelleng's limits here", fmt(L.min, 3) + " to " + fmt(L.max, 2) + " N"],
                ["sound", s.sound === null ? "press Bow" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "The model is the one the film uses (McIntyre, Schumacher and Woodhouse, 1983): waves travelling both ways from a bow at one point, a bridge that reflects a little less than everything, and rosin whose friction falls from 0.8 of the bow's force when the string is stuck to 0.3 when it slides fast. Each note is started as a player starts it, with a firmer bow that is eased to the force you chose in the first third of a second. Schelleng's two lines (1973) are formulas, not this model's own limits: the largest force goes as speed over distance and this string follows it closely; the smallest goes as speed over distance squared, and this string needs two or three times as much. A real string also twists, and real rosin warms and softens as it slides, so a violin's wedge is not exactly either. The sound is the force on the bridge through five resonances standing for a violin's body, computed in your browser. Simulated.",
    });
  };

  // ---- Part 8: shape a vowel -------------------------------------------------------------------------------------
  // The throat and mouth as two tubes end to end, closed at the folds and open at the lips.  The formants are the
  // peaks of the tube's input impedance seen from the folds, found from two transfer matrices (complex arithmetic).
  var VOWELS = [["heed", 270, 2290, 3010], ["hid", 390, 1990, 2550], ["head", 530, 1840, 2480], ["had", 660, 1720, 2410], ["hod", 730, 1090, 2440],
                ["hawed", 570, 840, 2410], ["hood", 440, 1020, 2240], ["who'd", 300, 870, 2240], ["hud", 640, 1190, 2390], ["heard", 490, 1350, 1690]];
  function cmul(a, b) { return [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]]; }
  function cadd(a, b) { return [a[0] + b[0], a[1] + b[1]]; }
  function cdiv(a, b) { var d = b[0] * b[0] + b[1] * b[1]; return [(a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d]; }
  function ccos(z) { return [Math.cos(z[0]) * Math.cosh(z[1]), -Math.sin(z[0]) * Math.sinh(z[1])]; }
  function csin(z) { return [Math.sin(z[0]) * Math.cosh(z[1]), Math.cos(z[0]) * Math.sinh(z[1])]; }
  function tractResponse(a1, l1, a2, l2, f) { // |Z_in| of the two tubes (areas in cm^2, lengths in cm), in units of the first tube's own impedance
    var c = 343, rho = 1.2, S1 = a1 * 1e-4, S2 = a2 * 1e-4, r2 = Math.sqrt(S2 / Math.PI), z1 = rho * c / S1, z2 = rho * c / S2;
    var k = 2 * Math.PI * f / c, loss = 0.012 * Math.sqrt(f / 500), kk = [k, -k * loss], ka = Math.min(k * r2, 1.5);
    var zl = [z2 * 0.25 * ka * ka, z2 * 0.6133 * ka];                                // the open mouth
    function through(zc, len, zload) { // the impedance seen through a tube of impedance zc and length len
      var kl = [kk[0] * len, kk[1] * len], cs = ccos(kl), sn = csin(kl);
      var num = cadd(cmul(zload, cs), cmul([0, zc], sn)), den = cadd(cmul(cmul([0, 1 / zc], sn), zload), cs);
      return cdiv(num, den);
    }
    var z = through(z1, l1 / 100, through(z2, l2 / 100, zl));
    return Math.sqrt(z[0] * z[0] + z[1] * z[1]) / z1;
  }
  function tractFormants(a1, l1, a2, l2) {
    var out = [], prev = 0, cur = tractResponse(a1, l1, a2, l2, 100), f, next;
    for (f = 105; f <= 4500 && out.length < 3; f += 5) {
      next = tractResponse(a1, l1, a2, l2, f + 5);
      if (cur > prev && cur >= next) out.push(f);
      prev = cur; cur = next;
    }
    while (out.length < 3) out.push(out.length ? out[out.length - 1] + 1000 : 500 + 1000 * out.length);
    return out;
  }
  function nearestVowel(f1, f2) {
    var best = 0, bd = 1e9, i;
    for (i = 0; i < VOWELS.length; i++) {
      var d = Math.pow(Math.log(f1 / VOWELS[i][1]), 2) + Math.pow(Math.log(f2 / VOWELS[i][2]), 2);
      if (d < bd) { bd = d; best = i; }
    }
    return { word: VOWELS[best][0], cents: 1200 * Math.sqrt(bd) / Math.log(2) };
  }
  function singVowel(hz, formants) { // pulses of the folds through a resonator for each formant, and out of the mouth
    var rate = 44100, len = Math.floor(1.5 * rate), x = new Float32Array(len), i, j, t = 0, peak = 0;
    while (t < len) { // Rosenberg's pulse: the flow rises, falls faster, and stops while the folds are shut
      var period = rate / (hz * (1 + 0.004 * (Math.random() - 0.5))), open = 0.6 * period, rise = open * 2 / 3, fall = open - rise, i0 = Math.floor(t);
      for (i = i0; i < Math.min(len, i0 + Math.ceil(open)); i++) {
        var u = i - t;
        x[i] = u < rise ? 0.5 * (1 - Math.cos(Math.PI * u / rise)) : Math.cos(0.5 * Math.PI * Math.min(1, (u - rise) / fall));
      }
      t += period;
    }
    var all = formants.concat([3500, 4500]);
    for (j = 0; j < all.length; j++) {
      var bw = 50 + all[j] / 20, r = Math.exp(-Math.PI * bw / rate), b = 2 * r * Math.cos(2 * Math.PI * all[j] / rate), c = -r * r, a = 1 - b - c, y1 = 0, y2 = 0;
      for (i = 0; i < len; i++) { var v = a * x[i] + b * y1 + c * y2; y2 = y1; y1 = v; x[i] = v; }
    }
    for (i = len - 1; i > 0; i--) x[i] -= x[i - 1];
    x[0] = 0;
    for (i = 0; i < len; i++) peak = Math.max(peak, Math.abs(x[i]));
    var fade = Math.floor(0.04 * rate), tail = Math.floor(0.12 * rate);
    for (i = 0; i < len; i++) x[i] *= (0.3 / (peak || 1)) * Math.min(1, i / fade) * Math.min(1, (len - i) / tail);
    return play(x, rate);
  }
  W.vowel = function (el) {
    QB.widget(el, {
      title: "Shape a vowel",
      sub: "The throat and mouth as two tubes: a back one, from the folds, and a front one, to the lips. Left: how strongly the tube answers at each frequency, with the harmonics of the sung note as thin lines. Its three lowest peaks are the formants. Right: the first two formants on the map of Peterson and Barney's ten vowels. Make the back tube narrow and the front wide for the vowel of hod; the back wide and the front narrow for heed; both the same for a mouth at rest. Then change the pitch: the dot does not move.",
      panels: 2, height: 300,
      controls: [
        { k: "a1", label: "Back tube: area (cm²)", min: 0.5, max: 10, step: 0.25, value: 1, fmt: function (x) { return fmt(x, 2); } },
        { k: "a2", label: "Front tube: area (cm²)", min: 0.5, max: 10, step: 0.25, value: 9, fmt: function (x) { return fmt(x, 2); } },
        { k: "l1", label: "Back tube: length (cm)", min: 4, max: 12, step: 0.25, value: 9, fmt: function (x) { return fmt(x, 2); } },
        { k: "l2", label: "Front tube: length (cm)", min: 4, max: 12, step: 0.25, value: 9, fmt: function (x) { return fmt(x, 2); } },
        { k: "hz", label: "Pitch of the voice (Hz)", min: 80, max: 400, step: 5, value: 110 },
      ],
      buttons: [
        { label: "Sing it", act: function (s, v) { s.sound = singVowel(v.hz, tractFormants(v.a1, v.l1, v.a2, v.l2)); } },
      ],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        var fs = [], ys = [], f, top = 0, i;
        for (f = 100; f <= 4000; f += 10) { var z = 20 * Math.log(tractResponse(v.a1, v.l1, v.a2, v.l2, f)) / Math.LN10; fs.push(f); ys.push(z); top = Math.max(top, z); }
        var fm = tractFormants(v.a1, v.l1, v.a2, v.l2);
        s.fm = fm;
        var a = g[0].axes({ x: [0, 4000], y: [top - 60, top + 6], title: "How strongly the tube answers (dB)", xlabel: "frequency (Hz)", xticks: [0, 1000, 2000, 3000, 4000], yticks: [] });
        for (i = 1; i * v.hz < 4000; i++) a.vline(i * v.hz, { color: C.muted, dash: [1, 0], width: 0.6 });
        a.line(fs, ys, { color: C.idea, width: 2.2 });
        for (i = 0; i < 3; i++) a.vline(fm[i], { color: C.loss, width: 1.4 });
        var b = g[1].axes({ x: [200, 850], y: [600, 2600], title: "The map of vowels", xlabel: "first formant (Hz)", xticks: [300, 500, 700], yticks: [1000, 1500, 2000, 2500] });
        b.dots(VOWELS.map(function (w) { return w[1]; }), VOWELS.map(function (w) { return w[2]; }), { color: C.muted, r: 4 });
        for (i = 0; i < VOWELS.length; i++) b.text(VOWELS[i][1] + 12, VOWELS[i][2], VOWELS[i][0], { color: C.muted, align: "left" });
        b.dots([fm[0]], [fm[1]], { color: C.loss, r: 6 });
      },
      readout: function (v, s) {
        var fm = s.fm || tractFormants(v.a1, v.l1, v.a2, v.l2), n = nearestVowel(fm[0], fm[1]);
        return [["formants", fm[0] + ", " + fm[1] + ", " + fm[2] + " Hz"],
                ["nearest vowel on the map", "the one in “" + n.word + "”" + (n.cents > 400 ? " (not close)" : "")],
                ["the tube", fmt(v.l1 + v.l2, 1) + " cm from folds to lips; a plain tube that long would give " + fmt(34300 / (4 * (v.l1 + v.l2)), 0) + ", " + fmt(3 * 34300 / (4 * (v.l1 + v.l2)), 0) + ", " + fmt(5 * 34300 / (4 * (v.l1 + v.l2)), 0) + " Hz"],
                ["harmonics of the voice", "every " + fmt(v.hz, 0) + " Hz"],
                ["sound", s.sound === null ? "press Sing" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "Two tubes of two widths are the oldest cartoon of a mouth (Fant, 1960), and they land within a semitone or so of the formants Peterson and Barney measured in 1952 for the vowels of hod (a narrow throat, a wide mouth) and heed (a wide throat, a narrow gap). The curve is the tube's input impedance seen from the vocal folds, with a little damping and an open, radiating mouth; rounded lips, the nose and the true shape of the tongue are not in it, so the back rounded vowels (who'd, hood) cannot be reached with two tubes. The sound is a train of pulses through one resonator for each formant, computed in your browser: the pitch comes from the pulses and the vowel from the resonators, independently. Simulated.",
    });
  };

  // ---- Part 9: strike a drum -------------------------------------------------------------------------------------
  // A round skin's modes (m still diameters, the n-th zero of the Bessel function J_m), bare, loaded by air as in a
  // kettledrum (measured), or loaded at its centre as in a tabla (computed in the film).
  function besselJ(m, x) { // (1/pi) * integral over 0..pi of cos(m t - x sin t) dt
    var n = 160, s = 0, i;
    for (i = 0; i <= n; i++) { var t = Math.PI * i / n; s += (i === 0 || i === n ? 0.5 : 1) * Math.cos(m * t - x * Math.sin(t)); }
    return s / n;
  }
  var SKIN_MODES = [[0, 1, 2.4048], [1, 1, 3.8317], [2, 1, 5.1356], [0, 2, 5.5201], [3, 1, 6.3802], [1, 2, 7.0156], [4, 1, 7.5883], [2, 2, 8.4172], [0, 3, 8.6537], [5, 1, 8.7715]];
  var DRUMS = [
    { name: "a bare skin", unit: "the lowest mode", ratios: SKIN_MODES.map(function (r) { return r[2] / 2.4048; }), modes: SKIN_MODES, series: [1, 2, 3, 4, 5], fastZero: true },
    { name: "a kettledrum (measured)", unit: "the lowest ringing mode", ratios: [0.85, 1.0, 1.5, 1.98, 2.44, 2.91], modes: [[0, 1, 2.4048], [1, 1, 3.8317], [2, 1, 5.1356], [3, 1, 6.3802], [4, 1, 7.5883], [5, 1, 8.7715]], series: [1, 1.5, 2, 2.5, 3], fastZero: true },
    { name: "a tabla (a heavy patch at the centre)", unit: "the lowest mode", ratios: [1.0, 1.94, 2.95, 3.05, 3.97, 4.10, 4.82, 4.96, 5.14], modes: [[0, 1, 2.4048], [1, 1, 3.8317], [2, 1, 5.1356], [0, 2, 5.5201], [3, 1, 6.3802], [1, 2, 7.0156], [0, 3, 8.6537], [4, 1, 7.5883], [2, 2, 8.4172]], series: [1, 2, 3, 4, 5], fastZero: false },
  ];
  function strikeAmounts(drum, at) { return drum.modes.map(function (r) { return Math.abs(besselJ(r[0], r[2] * at)); }); }
  function drumSound(drum, at, hz) {
    var rate = 44100, len = Math.floor(1.6 * rate), y = new Float32Array(len), amps = strikeAmounts(drum, at), i, k, peak = 0;
    for (k = 0; k < drum.ratios.length; k++) {
      var f = hz * drum.ratios[k], w = 2 * Math.PI * f / rate, d = (3 + 2 * drum.ratios[k]) * (drum.fastZero && drum.modes[k][0] === 0 ? 4 : 1) / rate;
      for (i = 0; i < len; i++) y[i] += amps[k] * Math.exp(-d * i) * Math.sin(w * i);
    }
    for (i = 0; i < len; i++) { y[i] *= Math.min(1, i / 60); peak = Math.max(peak, Math.abs(y[i])); }
    for (i = 0; i < len; i++) y[i] *= 0.3 / (peak || 1) * Math.min(1, (len - i) / 4000);
    return play(y, rate);
  }
  function worstMiss(drum) { // how far the nearest mode is from each wanted frequency, in cents: the worst of them
    var worst = 0, i, k;
    for (i = 0; i < drum.series.length; i++) {
      var best = 1e9;
      for (k = 0; k < drum.ratios.length; k++) best = Math.min(best, Math.abs(1200 * Math.log(drum.ratios[k] / drum.series[i]) / Math.LN2));
      worst = Math.max(worst, best);
    }
    return worst;
  }
  W.drum = function (el) {
    QB.widget(el, {
      title: "Strike a drum",
      sub: "Choose a drum and where to strike it. Left: how strongly the blow starts each mode (a mode is started in proportion to how much the skin moves, in that mode, at the point struck). Right: where the modes stand in frequency, with dotted lines where a musician would want them. Strike a bare skin at its centre and only the modes with no still diameter sound, and they die at once. Move outwards and the ringing modes join. Then change the drum.",
      panels: 2, height: 300,
      controls: [
        { k: "kind", label: "The drum", min: 0, max: 2, step: 1, value: 0, fmt: function (k) { return DRUMS[k].name; } },
        { k: "at", label: "Where it is struck (0 centre, 1 rim)", min: 0, max: 0.95, step: 0.01, value: 0.6, fmt: function (x) { return fmt(x, 2); } },
        { k: "hz", label: "Its note (Hz)", min: 60, max: 300, step: 5, value: 110 },
      ],
      buttons: [
        { label: "Strike it", act: function (s, v) { s.sound = drumSound(DRUMS[v.kind], v.at, v.hz); } },
      ],
      init: function (s) { s.sound = null; },
      draw: function (g, v, s) {
        var drum = DRUMS[v.kind], amps = strikeAmounts(drum, v.at), idx = [], i, top = 0;
        for (i = 0; i < amps.length; i++) { idx.push(i + 1); top = Math.max(top, amps[i]); }
        s.amps = amps;
        var a = g[0].axes({ x: [0.3, amps.length + 0.7], y: [0, Math.max(top, 0.05) * 1.15], title: "How strongly each mode is started", xlabel: "modes, lowest first", xticks: idx, yticks: [] });
        a.bars(idx, amps, 0.7, { color: function (k) { return drum.modes[k][0] === 0 ? C.loss : C.idea; } });
        a.legend([["no still diameter (dies fast)", C.loss], ["with diameters (rings)", C.idea]], { pos: "tr" });
        var hi = drum.ratios[drum.ratios.length - 1] + 0.3;
        var b = g[1].axes({ x: [0.5, hi], y: [0, 1], title: "Where the modes stand, in units of " + drum.unit, xlabel: "frequency ratio", yticks: [] });
        for (i = 0; i < drum.series.length; i++) b.vline(drum.series[i], { color: C.muted });
        for (i = 0; i < drum.ratios.length; i++) b.line([drum.ratios[i], drum.ratios[i]], [0, 0.15 + 0.8 * amps[i] / (top || 1)], { color: drum.modes[i][0] === 0 ? C.loss : C.idea, width: 3 });
      },
      readout: function (v, s) {
        var drum = DRUMS[v.kind], amps = s.amps || strikeAmounts(drum, v.at), best = 0, i;
        for (i = 1; i < amps.length; i++) if (amps[i] > amps[best]) best = i;
        return [["the drum", drum.name],
                ["its modes", drum.ratios.map(function (r) { return fmt(r, 2); }).join(", ")],
                ["worst miss from the dotted lines", fmt(worstMiss(drum), 0) + " cents"],
                ["the mode this blow starts most", "number " + (best + 1) + ", at " + fmt(drum.ratios[best], 2) + " (" + drum.modes[best][0] + " still diameters)"],
                ["sound", s.sound === null ? "press Strike" : (s.sound ? "playing" : "not available in this browser")]];
      },
      note: "A bare skin's modes follow the zeros of the Bessel functions, and form no series: the worst of the first five whole numbers is missed by more than a fourth. A kettledrum's ringing modes, measured by Rossing (1982), stand close to 1, 1.5, 2, 2.5, 3 because the air the skin must move slows its low modes most; its lowest mode of all, with no still diameter, sits below the series and dies in a fraction of a second. A tabla's modes are those computed in the film for a skin whose centre, out to four tenths of the radius, is about ten times as heavy: nine modes gathered near 1, 2, 3, 4, 5. For the kettledrum and the tabla the strength of each mode at the point struck is taken from the bare skin's mode shapes, which is an approximation. The sound is a sum of dying partials, computed in your browser. Simulated.",
    });
  };
})();
