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
})();
