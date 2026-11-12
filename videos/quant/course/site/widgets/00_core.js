// Quant, Built: the course site's interactives.  One widget per part, drawn on a canvas with no dependencies.
// tools/course_site.py concatenates this folder into assets/widgets.js; a page mounts a widget on every
// <div class="widget" data-widget="name">.  Everything simulated here is labelled as such on screen.
var QB = (function () {
  "use strict";
  var C = {
    bg: "#0e1117", panel: "#151b26", line: "#263041", ink: "#e6edf3", muted: "#8b98a9", q: "#a78bfa", p: "#fbbf24",
    spot: "#58a6ff", option: "#e879f9", gain: "#4ade80", loss: "#f87171", house: "#e2c08d", realized: "#2dd4bf",
    implied: "#fb923c", idea: "#f7d154", cash: "#94a3b8",
  };

  // ---- numbers -----------------------------------------------------------------------------------------------
  function rng(seed) { // mulberry32: a seeded uniform generator, so a widget redraws the same paths
    var a = (seed >>> 0) || 1;
    var u = function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
    u.normal = function () { // Box-Muller
      var x = 0; while (x === 0) x = u();
      return Math.sqrt(-2 * Math.log(x)) * Math.cos(2 * Math.PI * u());
    };
    u.student = function (nu) { // t with nu degrees of freedom, scaled to unit variance (nu > 2)
      var z = u.normal(), s = 0;
      for (var i = 0; i < nu; i++) { var e = u.normal(); s += e * e; }
      return z / Math.sqrt(s / nu) * Math.sqrt((nu - 2) / nu);
    };
    return u;
  }
  function pdf(x) { return Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI); }
  function cdf(x) { // Abramowitz-Stegun 7.1.26 on erf; absolute error below 1.5e-7
    var t = 1 / (1 + 0.3275911 * Math.abs(x) / Math.SQRT2);
    var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t *
      Math.exp(-x * x / 2);
    return x >= 0 ? 0.5 * (1 + y) : 0.5 * (1 - y);
  }
  function inv(p) { // Acklam's inverse normal
    var a = [-39.69683028665376, 220.9460984245205, -275.9285104469687, 138.357751867269, -30.66479806614716, 2.506628277459239];
    var b = [-54.47609879822406, 161.5858368580409, -155.6989798598866, 66.80131188771972, -13.28068155288572];
    var c = [-0.007784894002430293, -0.3223964580411365, -2.400758277161838, -2.549732539343734, 4.374664141464968, 2.938163982698783];
    var d = [0.007784695709041462, 0.3224671290700398, 2.445134137142996, 3.754408661907416];
    var q, r;
    if (p < 0.02425) { q = Math.sqrt(-2 * Math.log(p)); return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
    if (p > 1 - 0.02425) { q = Math.sqrt(-2 * Math.log(1 - p)); return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
    q = p - 0.5; r = q * q;
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
  }
  function bs(S, K, T, sig, r, cp) { // Black-Scholes price, delta, gamma, vega, theta (per year); cp = +1 call, -1 put
    r = r || 0; cp = cp || 1;
    if (T <= 0 || sig <= 0) { var iv = Math.max(cp * (S - K), 0); return { price: iv, delta: cp * (S - K) > 0 ? cp : 0, gamma: 0, vega: 0, theta: 0 }; }
    var st = sig * Math.sqrt(T), d1 = (Math.log(S / K) + (r + 0.5 * sig * sig) * T) / st, d2 = d1 - st, df = Math.exp(-r * T);
    return {
      price: cp * (S * cdf(cp * d1) - K * df * cdf(cp * d2)), delta: cp * cdf(cp * d1), gamma: pdf(d1) / (S * st),
      vega: S * pdf(d1) * Math.sqrt(T), theta: -S * pdf(d1) * sig / (2 * Math.sqrt(T)) - cp * r * K * df * cdf(cp * d2),
    };
  }
  function linspace(a, b, n) { var o = new Array(n); for (var i = 0; i < n; i++) o[i] = a + (b - a) * i / (n - 1); return o; }
  function mean(x) { var s = 0; for (var i = 0; i < x.length; i++) s += x[i]; return s / x.length; }
  function sd(x) { var m = mean(x), s = 0; for (var i = 0; i < x.length; i++) s += (x[i] - m) * (x[i] - m); return Math.sqrt(s / (x.length - 1)); }
  function quantile(x, q) { var s = Array.prototype.slice.call(x).sort(function (a, b) { return a - b; }); var i = (s.length - 1) * q, lo = Math.floor(i); return s[lo] + (s[Math.min(lo + 1, s.length - 1)] - s[lo]) * (i - lo); }
  function hist(x, lo, hi, n) { var h = new Array(n).fill(0), w = (hi - lo) / n; for (var i = 0; i < x.length; i++) { var k = Math.floor((x[i] - lo) / w); if (k >= 0 && k < n) h[k]++; } return h; }
  function fmt(v, d) { return (v < 0 ? "−" : "") + Math.abs(v).toFixed(d === undefined ? 2 : d); }
  function pct(v, d) { return fmt(100 * v, d === undefined ? 1 : d) + "%"; }

  // ---- a plot panel ------------------------------------------------------------------------------------------
  function Axes(ctx, box, o) {
    this.ctx = ctx; this.o = o || {};
    var padL = this.o.noY ? 10 : 46, padB = this.o.noX ? 8 : 32, padT = this.o.title ? 24 : 10;
    this.x0 = box.x + padL; this.y0 = box.y + padT; this.w = box.w - padL - 12; this.h = box.h - padT - padB;
    this.xr = this.o.x || [0, 1]; this.yr = this.o.y || [0, 1];
    this.frame();
  }
  Axes.prototype.px = function (x) { var r = this.xr; return this.x0 + this.w * (this.o.logx ? Math.log(x / r[0]) / Math.log(r[1] / r[0]) : (x - r[0]) / (r[1] - r[0])); };
  Axes.prototype.py = function (y) { var r = this.yr; return this.y0 + this.h * (1 - (this.o.logy ? Math.log(y / r[0]) / Math.log(r[1] / r[0]) : (y - r[0]) / (r[1] - r[0]))); };
  function ticks(r, log, n) {
    var out = [], i;
    if (log) { for (i = Math.ceil(Math.log10(r[0]) - 1e-9); i <= Math.floor(Math.log10(r[1]) + 1e-9); i++) out.push(Math.pow(10, i)); return out; }
    var span = r[1] - r[0], step = Math.pow(10, Math.floor(Math.log10(span / (n || 5)))), m = span / (n || 5) / step;
    step *= m > 5 ? 10 : m > 2 ? 5 : m > 1 ? 2 : 1;
    for (i = Math.ceil(r[0] / step - 1e-9); i * step <= r[1] + 1e-9; i++) out.push(+(i * step).toPrecision(12));
    return out;
  }
  function tickLabel(v, log) {
    if (log) { var e = Math.round(Math.log10(v)); return e >= -2 && e <= 4 ? String(+v.toPrecision(3)) : "1e" + e; }
    var a = Math.abs(v); if (a >= 10000) return (v / 1000).toFixed(0) + "k";
    return String(+v.toPrecision(4)).replace("-", "−");
  }
  Axes.prototype.frame = function () {
    var c = this.ctx, o = this.o, i, t, p;
    c.save(); c.font = "11px system-ui, sans-serif"; c.lineWidth = 1;
    var xt = o.xticks || ticks(this.xr, o.logx, o.nx), yt = o.yticks || ticks(this.yr, o.logy, o.ny);
    c.strokeStyle = C.line; c.fillStyle = C.muted;
    if (!o.noX) { c.textAlign = "center"; c.textBaseline = "top"; for (i = 0; i < xt.length; i++) { p = this.px(xt[i]); c.beginPath(); c.moveTo(p, this.y0); c.lineTo(p, this.y0 + this.h); c.stroke(); c.fillText(o.xfmt ? o.xfmt(xt[i]) : tickLabel(xt[i], o.logx), p, this.y0 + this.h + 5); } }
    if (!o.noY) { c.textAlign = "right"; c.textBaseline = "middle"; for (i = 0; i < yt.length; i++) { p = this.py(yt[i]); c.beginPath(); c.moveTo(this.x0, p); c.lineTo(this.x0 + this.w, p); c.stroke(); c.fillText(o.yfmt ? o.yfmt(yt[i]) : tickLabel(yt[i], o.logy), this.x0 - 6, p); } }
    if (!o.noFrame) { c.strokeStyle = "#3a475c"; c.strokeRect(this.x0 + 0.5, this.y0 + 0.5, this.w, this.h); }
    if (o.xlabel) { c.textAlign = "center"; c.textBaseline = "bottom"; c.fillText(o.xlabel, this.x0 + this.w / 2, this.y0 + this.h + 31); }
    if (o.title) { c.fillStyle = C.ink; c.font = "600 12.5px system-ui, sans-serif"; c.textAlign = "left"; c.textBaseline = "top"; c.fillText(o.title, this.x0, this.y0 - 20); }
    c.restore();
    t = 0;
  };
  Axes.prototype.clip = function (fn) { var c = this.ctx; c.save(); c.beginPath(); c.rect(this.x0, this.y0, this.w, this.h); c.clip(); fn(c); c.restore(); };
  Axes.prototype.line = function (xs, ys, s) {
    s = s || {}; var self = this;
    this.clip(function (c) {
      c.strokeStyle = s.color || C.spot; c.lineWidth = s.width || 1.8; c.globalAlpha = s.alpha === undefined ? 1 : s.alpha;
      if (s.dash) c.setLineDash(s.dash); c.lineJoin = "round"; c.beginPath();
      var pen = false;
      for (var i = 0; i < xs.length; i++) {
        var y = ys[i]; if (y === null || y !== y || !isFinite(y)) { pen = false; continue; }
        var X = self.px(xs[i]), Y = Math.max(-1e4, Math.min(1e4, self.py(y)));
        if (pen) c.lineTo(X, Y); else { c.moveTo(X, Y); pen = true; }
      }
      c.stroke();
    });
    return this;
  };
  Axes.prototype.area = function (xs, ys, base, s) {
    s = s || {}; var self = this;
    this.clip(function (c) {
      c.fillStyle = s.color || C.spot; c.globalAlpha = s.alpha === undefined ? 0.25 : s.alpha; c.beginPath();
      var i, b = function (k) { return typeof base === "number" ? base : base[k]; };
      c.moveTo(self.px(xs[0]), self.py(b(0)));
      for (i = 0; i < xs.length; i++) c.lineTo(self.px(xs[i]), self.py(ys[i]));
      for (i = xs.length - 1; i >= 0; i--) c.lineTo(self.px(xs[i]), self.py(b(i)));
      c.closePath(); c.fill();
    });
    return this;
  };
  Axes.prototype.bars = function (xs, hs, w, s) {
    s = s || {}; var self = this;
    this.clip(function (c) {
      c.globalAlpha = s.alpha === undefined ? 0.85 : s.alpha;
      var base = self.py(s.base || (self.o.logy ? self.yr[0] : 0));
      for (var i = 0; i < xs.length; i++) {
        c.fillStyle = typeof s.color === "function" ? s.color(i) : (s.color || C.spot);
        var x1 = self.px(xs[i] - w / 2), x2 = self.px(xs[i] + w / 2), y = self.py(hs[i]);
        c.fillRect(x1, Math.min(y, base), Math.max(1, x2 - x1 - (s.gap === undefined ? 1 : s.gap)), Math.abs(base - y));
      }
    });
    return this;
  };
  Axes.prototype.dots = function (xs, ys, s) {
    s = s || {}; var self = this;
    this.clip(function (c) {
      c.globalAlpha = s.alpha === undefined ? 1 : s.alpha;
      for (var i = 0; i < xs.length; i++) {
        c.fillStyle = typeof s.color === "function" ? s.color(i) : (s.color || C.spot);
        c.beginPath(); c.arc(self.px(xs[i]), self.py(ys[i]), s.r || 3, 0, 6.2832); c.fill();
      }
    });
    return this;
  };
  Axes.prototype.hline = function (y, s) { return this.line([this.xr[0], this.xr[1]], [y, y], Object.assign({ color: C.muted, width: 1, dash: [4, 4] }, s || {})); };
  Axes.prototype.vline = function (x, s) { return this.line([x, x], [this.yr[0], this.yr[1]], Object.assign({ color: C.muted, width: 1, dash: [4, 4] }, s || {})); };
  Axes.prototype.text = function (x, y, str, s) {
    s = s || {}; var c = this.ctx; c.save(); c.font = (s.bold ? "600 " : "") + (s.size || 11.5) + "px system-ui, sans-serif";
    c.textAlign = s.align || "left"; c.textBaseline = s.base || "middle";
    var X = this.px(x) + (s.dx || 0), Y = this.py(y) + (s.dy || 0);
    if (s.bg) { // a plate behind the label, so it stays readable over lines
      var tw = c.measureText(str).width, x0 = c.textAlign === "center" ? X - tw / 2 : c.textAlign === "right" ? X - tw : X;
      c.fillStyle = "rgba(21,27,38,0.88)"; c.fillRect(x0 - 4, Y - 9, tw + 8, 18);
    }
    c.fillStyle = s.color || C.ink; c.fillText(str, X, Y); c.restore(); return this;
  };
  Axes.prototype.legend = function (items, s) { // [[label, color], ...] in a corner: "tl" (default), "tr", "bl", "br"
    s = s || {}; var c = this.ctx, pos = s.pos || "tl", lh = 15; c.save(); c.font = "11.5px system-ui, sans-serif"; c.textBaseline = "middle";
    var wmax = 0, i; for (i = 0; i < items.length; i++) wmax = Math.max(wmax, c.measureText(items[i][0]).width);
    var x = pos[1] === "l" ? this.x0 + 8 : this.x0 + this.w - wmax - 26, y = pos[0] === "t" ? this.y0 + 11 : this.y0 + this.h - lh * items.length + 4;
    c.fillStyle = "rgba(14,17,23,0.72)"; c.fillRect(x - 5, y - 9, wmax + 28, lh * items.length + 4);
    for (i = 0; i < items.length; i++) {
      c.strokeStyle = items[i][1]; c.lineWidth = 2.5; c.beginPath(); c.moveTo(x, y + i * lh); c.lineTo(x + 14, y + i * lh); c.stroke();
      c.fillStyle = C.ink; c.textAlign = "left"; c.fillText(items[i][0], x + 19, y + i * lh);
    }
    c.restore(); return this;
  };

  // ---- a widget: title, canvas, sliders, buttons, readout ------------------------------------------------------
  function widget(el, spec) {
    el.innerHTML = "";
    var add = function (tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text) n.textContent = text; return n; };
    if (spec.title) el.appendChild(add("p", "w-title", spec.title));
    if (spec.sub) el.appendChild(add("p", "w-sub", spec.sub));
    var canvas = add("canvas"); canvas.setAttribute("role", "img"); canvas.setAttribute("aria-label", spec.title || "interactive figure"); el.appendChild(canvas);
    var v = {}, state = { seed: 1 }, outs = {}, raf = 0, running = false, last = 0;
    var controls = add("div", "controls");
    (spec.controls || []).forEach(function (cdef) {
      v[cdef.k] = cdef.value;
      var lab = add("label"); lab.appendChild(add("span", "", cdef.label));
      var out = add("output"); lab.appendChild(out); outs[cdef.k] = [out, cdef.fmt || function (x) { return String(x); }];
      var inp = add("input"); inp.type = "range"; inp.min = cdef.min; inp.max = cdef.max; inp.step = cdef.step; inp.value = cdef.value;
      inp.setAttribute("aria-label", cdef.label);
      inp.addEventListener("input", function () { v[cdef.k] = +inp.value; if (spec.onChange) spec.onChange(v, state, cdef.k); render(); kick(); });
      lab.appendChild(inp); controls.appendChild(lab);
    });
    if ((spec.controls || []).length) el.appendChild(controls);
    var bar = add("div", "w-buttons");
    (spec.buttons || []).forEach(function (b) {
      var btn = add("button", "", b.label); btn.type = "button";
      btn.addEventListener("click", function () { b.act(state, v); render(); kick(); });
      bar.appendChild(btn);
    });
    if ((spec.buttons || []).length) el.appendChild(bar);
    var read = add("div", "readout"); el.appendChild(read);
    if (spec.note) el.appendChild(add("p", "w-note", spec.note));
    if (spec.init) spec.init(state, v);

    function render() {
      var cssW = Math.max(280, Math.floor(el.clientWidth - (el.classList.contains("hero-widget") ? 0 : 32)));
      var n = spec.panels || 1, stack = n > 1 && cssW < 620;
      var cssH = (spec.height || 300) * (stack ? n * 0.82 : 1), dpr = Math.min(window.devicePixelRatio || 1, 2);
      if (canvas.width !== Math.round(cssW * dpr) || canvas.height !== Math.round(cssH * dpr)) {
        canvas.width = Math.round(cssW * dpr); canvas.height = Math.round(cssH * dpr); canvas.style.height = cssH + "px";
      }
      var ctx = canvas.getContext("2d"); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = spec.bg || C.panel; ctx.fillRect(0, 0, cssW, cssH);
      var weights = spec.weights || new Array(n).fill(1), tot = weights.reduce(function (a, b) { return a + b; }, 0), acc = 0;
      var boxes = weights.map(function (wt) {
        var b = stack ? { x: 0, y: cssH * acc / tot, w: cssW, h: cssH * wt / tot } : { x: cssW * acc / tot, y: 0, w: cssW * wt / tot, h: cssH };
        acc += wt; return b;
      });
      var g = boxes.map(function (b) { return { box: b, ctx: ctx, axes: function (o) { return new Axes(ctx, b, o); } }; });
      g.ctx = ctx; g.w = cssW; g.h = cssH;
      spec.draw(g, v, state);
      Object.keys(outs).forEach(function (k) { outs[k][0].textContent = outs[k][1](v[k]); });
      if (spec.readout) {
        read.innerHTML = "";
        spec.readout(v, state).forEach(function (r) { var s = add("span", "", r[0] + " "); s.appendChild(add("b", "", r[1])); read.appendChild(s); });
      }
    }
    function frame(t) {
      var dt = Math.min(0.05, (t - last) / 1000 || 0.016); last = t;
      running = !!spec.animate(v, state, dt); render();
      if (running) raf = requestAnimationFrame(frame);
    }
    function kick() { if (spec.animate && !running && !reduced()) { running = true; last = performance.now(); raf = requestAnimationFrame(frame); } }
    function reduced() { return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches; }
    if (spec.animate && reduced()) { for (var warm = 0; warm < 300; warm++) spec.animate(v, state, 0.016); } // a settled still frame
    var ro = window.ResizeObserver ? new ResizeObserver(function () { render(); }) : null;
    if (ro) ro.observe(el); else window.addEventListener("resize", render);
    render();
    if (spec.animate) {
      if (window.IntersectionObserver) new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) kick(); else { running = false; cancelAnimationFrame(raf); } }); }).observe(el);
      else kick();
    }
    return { render: render, v: v, state: state };
  }

  var registry = {};
  function mount() {
    document.querySelectorAll(".widget[data-widget]").forEach(function (el) {
      var f = registry[el.dataset.widget];
      if (!f) { el.textContent = "Interactive '" + el.dataset.widget + "' is not available."; return; }
      try { f(el); } catch (err) { el.textContent = "This interactive failed to start: " + err.message; if (window.console) console.error(err); }
    });
  }

  return { mount: mount, C: C, rng: rng, pdf: pdf, cdf: cdf, inv: inv, bs: bs, linspace: linspace, mean: mean, sd: sd, quantile: quantile,
    hist: hist, fmt: fmt, pct: pct, widget: widget, W: registry };
})();
