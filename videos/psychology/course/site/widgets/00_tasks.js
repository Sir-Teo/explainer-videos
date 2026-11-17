// The task kit of Psychology, Built: what every experiment on the course site shares.  It is concatenated before
// the parts' interactives (the files are joined in name order) and defines QB.task:
//
//   QB.task.create(el, spec)   one experiment: its keys and taps, its timer, and what a scripted participant needs
//   QB.task.timed(el, o)       a timed-trial loop on top of it: foreperiod, stimulus, one response, feedback
//   QB.task.stage(g, i, task)  the dark panel an experiment runs in;  QB.task.message(...)  a heading and a line
//   QB.task.now(), QB.task.wrap(...)
//
// An experiment's data live in the page's memory and are gone when the page is closed.  Nothing in this file or in
// the interactives reads or writes storage, cookies or the network (tests/psychology/test_task_kit.py checks it).
//
// tools/check_widgets.js plays a scripted participant against QB.task.live: it starts the experiment with the
// widget's first button, answers when a task says it is ready, and fails the page if the answers are not recorded.
// So the first button of an experiment starts it, and a task counts each response it records (task.count).
(function () {
  "use strict";
  var C = QB.C;
  var T = { live: [] };

  T.now = function () { return window.performance && performance.now ? performance.now() : Date.now(); };

  // Centred lines of text, broken at spaces to fit maxW; returns the y of the next line.
  T.wrap = function (ctx, text, x, y, maxW, lh) {
    var words = text.split(" "), line = "", i;
    for (i = 0; i < words.length; i++) {
      var t = line ? line + " " + words[i] : words[i];
      if (ctx.measureText(t).width > maxW && line) { ctx.fillText(line, x, y); y += lh; line = words[i]; } else line = t;
    }
    if (line) { ctx.fillText(line, x, y); y += lh; }
    return y;
  };

  // Draw the stage in panel g[i] and return its box with the centre added.  Given a task, the box is also where
  // its taps are read: the left half answers 0 and the right half 1.
  T.stage = function (g, i, task) {
    var ctx = g.ctx, b = g[i].box;
    ctx.save();
    ctx.fillStyle = "#05070b"; ctx.fillRect(b.x + 6, b.y + 6, b.w - 12, b.h - 12);
    ctx.strokeStyle = C.idea; ctx.lineWidth = 2; ctx.strokeRect(b.x + 6, b.y + 6, b.w - 12, b.h - 12);
    ctx.restore();
    var box = { x: b.x, y: b.y, w: b.w, h: b.h, cx: b.x + b.w / 2, cy: b.y + b.h / 2 };
    if (task) task.box = box;
    return box;
  };

  // A heading at height y and a wrapped line under it, centred in the stage: the idle, feedback and finished
  // screens of an experiment.
  T.message = function (ctx, b, head, sub, y) {
    y = y === undefined ? b.cy - 26 : y;
    ctx.save();
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillStyle = C.ink; ctx.font = "600 15px system-ui, sans-serif";
    ctx.fillText(head, b.cx, y);
    if (sub) {
      ctx.fillStyle = C.muted; ctx.font = "12.5px system-ui, sans-serif";
      T.wrap(ctx, sub, b.cx, y + 30, b.w - 44, 17);
    }
    ctx.restore();
  };

  // One experiment in the widget element el.  Call it before QB.widget(el, ...): the listeners sit on el and on
  // the document, so they outlive the widget's own markup.
  //   spec.keys       {key: side}, lower case; " " is the space bar
  //   spec.accepting  function () -> is the experiment running, so that a press means something (even "too early")?
  //   spec.ready      function () -> would a press now be recorded as a response?  (default: accepting)
  //   spec.respond    function (side, how): how is "key" or "tap"; a tap gives side 0 (left half) or 1 (right half)
  // Returns the task: {keys, box, count, accepting, ready, later(fn, ms), clear()}.  later() keeps one timer, so
  // scheduling a new step cancels the pending one.
  T.create = function (el, spec) {
    var timer = 0;
    var task = {
      el: el, keys: spec.keys || {}, box: null, count: 0,
      accepting: spec.accepting, ready: spec.ready || spec.accepting,
      clear: function () { if (timer) { clearTimeout(timer); timer = 0; } },
      later: function (fn, ms) { task.clear(); timer = setTimeout(function () { timer = 0; fn(); }, ms); },
    };
    el.addEventListener("pointerdown", function (e) {
      var canvas = e.target, b = task.box;
      if (!canvas || canvas.tagName !== "CANVAS" || !b || !task.accepting()) return;
      var rect = canvas.getBoundingClientRect(), x = e.clientX - rect.left, y = e.clientY - rect.top;
      if (x < b.x || x > b.x + b.w || y < b.y || y > b.y + b.h) return;
      e.preventDefault();
      spec.respond(x < b.cx ? 0 : 1, "tap");
    });
    document.addEventListener("keydown", function (e) {
      if (e.repeat || e.ctrlKey || e.metaKey || e.altKey || !task.accepting()) return;
      var key = (e.key || "").toLowerCase();
      if (key === "spacebar") key = " ";
      if (!Object.prototype.hasOwnProperty.call(task.keys, key)) return;
      if (key === " ") e.preventDefault(); // or the page scrolls
      spec.respond(task.keys[key], "key");
    });
    T.live.push(task);
    return task;
  };

  function salt(text) { var h = 0, i; for (i = 0; i < text.length; i++) h = (h * 31 + text.charCodeAt(i)) % 9973; return h; }

  // A timed-trial loop: a blank foreperiod of random length, the stimulus, one response or a timeout, a moment of
  // feedback, the next trial.  A press during the foreperiod is "too early": the trial is run again.
  //   o.keys                       {key: side}, as for create()
  //   o.trials()                   trials in a block
  //   o.seed()                     a number: the stimuli and foreperiods of a block come from QB.rng
  //   o.stimulus(rand, cond)       the stimulus of the next trial (any value); rand() is uniform on [0, 1)
  //   o.correct(stim, side, cond)  is this response right?  (default: every response is)
  //   o.render()                   redraw the widget
  //   o.foreperiod [min, max], o.timeout, o.pause {scored, early, timeout}: milliseconds
  //   o.words {early, timeout, wrong(side)}: feedback lines
  // Returns the run: phase ("idle", "wait", "go", "feedback", "done"), cond, trial, stim, msg, early, wrong;
  // log, one row {condition, trial, rt, correct} per trial that ended in a response or a timeout (rt NaN), in the
  // Battery's trial format; rts(cond), the times of the correct responses; start(cond), which empties that
  // condition's rows and runs a block; reset(); running(); and task, the create() object.
  T.timed = function (el, o) {
    var fore = o.foreperiod || [900, 2600], limit = o.timeout || 2000;
    var pause = { scored: 700, early: 900, timeout: 900 }, words = o.words || {}, k, t0 = 0;
    for (k in o.pause || {}) pause[k] = o.pause[k];
    var run = { phase: "idle", cond: "", trial: 0, stim: null, msg: "", early: 0, wrong: 0, log: [] };
    run.running = function () { return run.phase === "wait" || run.phase === "go" || run.phase === "feedback"; };
    run.rts = function (cond) {
      var out = [], i;
      for (i = 0; i < run.log.length; i++) if (run.log[i].condition === cond && run.log[i].correct) out.push(run.log[i].rt);
      return out;
    };
    function feedback(msg, ms) { run.msg = msg; run.phase = "feedback"; o.render(); task.later(next, ms); }
    function next() {
      if (run.trial >= o.trials()) { task.clear(); run.phase = "done"; o.render(); return; }
      run.trial++; run.phase = "wait"; run.msg = "";
      var rand = QB.rng(o.seed() * 977 + run.trial * 131 + run.early * 17 + salt(run.cond));
      run.stim = o.stimulus(rand, run.cond);
      o.render();
      task.later(function () {
        run.phase = "go"; o.render(); t0 = T.now();
        task.later(function () {
          run.log.push({ condition: run.cond, trial: run.trial, rt: NaN, correct: false });
          feedback(words.timeout || "No response in time.", pause.timeout);
        }, limit);
      }, fore[0] + (fore[1] - fore[0]) * rand());
    }
    function respond(side) {
      if (run.phase === "wait") {
        run.early++; run.trial--;
        feedback(words.early || "Too early.", pause.early);
      } else if (run.phase === "go") {
        var rt = T.now() - t0, ok = o.correct ? !!o.correct(run.stim, side, run.cond) : true;
        run.log.push({ condition: run.cond, trial: run.trial, rt: rt, correct: ok });
        task.count++;
        if (!ok) run.wrong++;
        feedback(ok ? Math.round(rt) + " ms" : (words.wrong ? words.wrong(side) : "Wrong (not counted)."), pause.scored);
      }
    }
    var task = T.create(el, { keys: o.keys, accepting: run.running, ready: function () { return run.phase === "go"; },
      respond: respond });
    run.task = task;
    run.start = function (cond) {
      task.clear();
      run.cond = cond; run.trial = 0; run.msg = "";
      run.log = run.log.filter(function (r) { return r.condition !== cond; });
      next();
    };
    run.reset = function () {
      task.clear();
      run.phase = "idle"; run.trial = 0; run.early = 0; run.wrong = 0; run.msg = ""; run.log = [];
    };
    return run;
  };

  QB.task = T;
})();
