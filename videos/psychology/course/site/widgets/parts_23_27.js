// Interactives for Act V continued, Thinking (Parts 23-27).  Each is an experiment the reader takes part in, built on
// the task kit (00_tasks.js); nothing a reader does is stored or sent anywhere.
(function () {
  "use strict";
  var C = QB.C, W = QB.W, T = QB.task;

  // ---- Part 23: a made-up language.  Watch a stream of syllables, then find its words ---------------------------
  W.stream = function (el) {
    var w = null, GOLD = "#f2c14e", BLUE = "#7ec8f5", GREEN = "#5bd18b", RED = "#ef6f6c", GREY = "#9aa4b2";
    var CONS = "bdgklmnprt", VOW = "aiou";
    var KEYS = { f: 0, j: 1 };
    var S = { phase: "idle", seed: 0, words: [], stream: [], k: 0, flagged: [], hits: 0, cover: 0, test: [], t: 0,
              answers: [], tp: [] };
    function build() {
      var u = QB.rng(48611 * S.seed + 7), pool = [], i, j;
      for (i = 0; i < CONS.length; i++) for (j = 0; j < VOW.length; j++) pool.push(CONS[i] + VOW[j]);
      for (i = pool.length - 1; i > 0; i--) { j = Math.floor(u() * (i + 1)); var t = pool[i]; pool[i] = pool[j]; pool[j] = t; }
      S.words = [pool.slice(0, 3), pool.slice(3, 6), pool.slice(6, 9), pool.slice(9, 12)];
      // 48 words in random order, no word twice running: 144 syllables
      S.stream = []; S.flagged = [];
      var prev = -1;
      for (i = 0; i < 48; i++) {
        var k = prev;
        while (k === prev) k = Math.floor(u() * 4);
        prev = k;
        S.words[k].forEach(function (s) { S.stream.push(s); S.flagged.push(u() < 0.06); });
      }
      // transitional probabilities, as Psyche computes them
      var pair = {}, first = {};
      for (i = 0; i + 1 < S.stream.length; i++) {
        var key = S.stream[i] + "|" + S.stream[i + 1];
        pair[key] = (pair[key] || 0) + 1; first[S.stream[i]] = (first[S.stream[i]] || 0) + 1;
      }
      S.tp = [];
      for (i = 0; i + 1 < S.stream.length; i++) S.tp.push(pair[S.stream[i] + "|" + S.stream[i + 1]] / first[S.stream[i]]);
      // the test: each word against a part-word made of the end of one word and the start of another
      var tests = [];
      for (i = 0; i < 4; i++) {
        var other = S.words[(i + 1) % 4];
        var part = [S.words[i][2], other[0], other[1]];
        tests.push({ word: S.words[i].join(""), part: part.join(""), wordLeft: u() < 0.5 });
        var part2 = [S.words[i][1], S.words[i][2], other[0]];
        tests.push({ word: S.words[(i + 2) % 4].join(""), part: part2.join(""), wordLeft: u() < 0.5 });
      }
      S.test = tests;
    }
    function scoreTP(item) {  // mean transitional probability inside a candidate, from the stream
      var syl = [item.slice(0, 2), item.slice(2, 4), item.slice(4, 6)], pair = {}, first = {}, i;
      for (i = 0; i + 1 < S.stream.length; i++) {
        var key = S.stream[i] + "|" + S.stream[i + 1];
        pair[key] = (pair[key] || 0) + 1; first[S.stream[i]] = (first[S.stream[i]] || 0) + 1;
      }
      var a = (pair[syl[0] + "|" + syl[1]] || 0) / (first[syl[0]] || 1), b = (pair[syl[1] + "|" + syl[2]] || 0) / (first[syl[1]] || 1);
      return (a + b) / 2;
    }
    function next() {
      if (S.k >= S.stream.length) { S.phase = "test"; S.t = 0; w.render(); return; }
      S.phase = "listen"; w.render();
      task.later(function () { S.k++; next(); }, Math.round(1000 * (S.secs || 0.25)));
    }
    function start() {
      task.clear(); S.seed++; build(); S.k = 0; S.hits = 0; S.cover = 0; S.answers = [];
      S.phase = "listen"; w.render(); task.later(next, 300);
    }
    var task = T.create(el, { keys: KEYS, accepting: function () { return S.phase === "listen" || S.phase === "test"; },
                              respond: answer });
    function answer(side) {
      if (S.phase === "listen") {  // the cover task: press J (or tap right) for a blue syllable
        task.count++;
        if (side === 1) { S.cover++; if (S.flagged[Math.min(S.k, S.flagged.length - 1)]) S.hits++; }
        return;
      }
      if (S.phase !== "test") return;
      task.count++;
      var item = S.test[S.t], choseLeft = side === 0;
      S.answers.push({ correct: choseLeft === item.wordLeft });
      S.t++;
      if (S.t >= S.test.length) S.phase = "done";
      w.render();
    }

    w = QB.widget(el, {
      title: "A language in two minutes: find its words",
      sub: "A stream of syllables from a made-up language, with no spaces, one syllable at a time (about 40 seconds). To keep your eyes on it, press J (or tap right) when a syllable turns blue. Then eight pairs: which of the two was a word of the language? F (or tap left) for the left one, J (or tap right) for the right one.",
      panels: 2, height: 330, weights: [1.2, 1],
      controls: [{ k: "secs", label: "Seconds per syllable", min: 0.2, max: 0.5, step: 0.01, value: 0.25,
                   fmt: function (x) { return x.toFixed(2) + " s"; } }],
      onChange: function (v) { S.secs = v.secs; },
      buttons: [
        { label: "Start", act: start },
        { label: "Clear", act: function () { task.clear(); S.phase = "idle"; S.answers = []; } },
      ],
      draw: function (g, v) {
        if (v && v.secs) S.secs = v.secs;
        var c = g.ctx, b = T.stage(g, 0, task);
        c.save(); c.textAlign = "center"; c.textBaseline = "middle";
        if (S.phase === "idle") {
          T.message(c, b, "On you", "Press Start. Syllables from a language you have never heard will appear one at a time, with no gaps between words. Just watch, and press J when one turns blue. Then you will be asked to pick out its words.");
        } else if (S.phase === "listen") {
          var s = S.stream[Math.min(S.k, S.stream.length - 1)] || "";
          c.fillStyle = S.flagged[S.k] ? BLUE : C.ink; c.font = "600 40px system-ui, sans-serif";
          c.fillText(s, b.cx, b.cy);
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("syllable " + (S.k + 1) + " of " + S.stream.length, b.cx, b.y + b.h - 18);
        } else if (S.phase === "test") {
          var item = S.test[S.t], L = item.wordLeft ? item.word : item.part, R = item.wordLeft ? item.part : item.word;
          c.fillStyle = C.muted; c.font = "12px system-ui, sans-serif";
          c.fillText("pair " + (S.t + 1) + " of " + S.test.length + ": which was a word of the language?", b.cx, b.y + 20);
          c.fillStyle = GOLD; c.font = "600 32px system-ui, sans-serif";
          c.fillText(L, b.x + b.w * 0.27, b.cy); c.fillText(R, b.x + b.w * 0.73, b.cy);
          c.fillStyle = GREY; c.font = "13px system-ui, sans-serif";
          c.fillText("F: left", b.x + b.w * 0.27, b.y + b.h - 22); c.fillText("J: right", b.x + b.w * 0.73, b.y + b.h - 22);
        } else if (S.phase === "done") {
          T.message(c, b, "Finished.", "The words were " + S.words.map(function (x) { return x.join(""); }).join(", ") + ". On the right: your score, chance, and Psyche's, which only counts which syllable follows which.");
        }
        c.restore();

        var n = S.answers.length, mine = n ? S.answers.filter(function (a) { return a.correct; }).length / n : NaN;
        var psyche = S.test.length ? S.test.filter(function (t) { return scoreTP(t.word) > scoreTP(t.part); }).length / S.test.length : NaN;
        if (S.phase === "listen" && S.tp.length) {
          var a = g[1].axes({ x: [0, 30], y: [0, 1.05], xticks: [], yticks: [0, 0.5, 1],
            title: "Transitional probability, last 30 syllables", xlabel: "", ylabel: "P(next | this)" });
          var lo = Math.max(0, Math.min(S.k, S.tp.length) - 30), xs = [], ys = [];
          for (var i = lo; i < Math.min(S.k, S.tp.length); i++) { xs.push(i - lo); ys.push(S.tp[i]); }
          if (xs.length) { a.line(xs, ys, { color: GREEN, width: 2 }); a.dots(xs, ys, { color: GREEN, r: 3 }); }
        } else {
          var a2 = g[1].axes({ x: [0, 3], y: [0, 1], xticks: [], yticks: [0, 0.5, 1],
            title: "Words chosen over part-words", xlabel: "you        chance        Psyche", ylabel: "share right" });
          if (!isNaN(mine)) a2.bars([0.5], [mine], 0.55, { color: GOLD });
          a2.bars([1.5], [0.5], 0.55, { color: GREY, alpha: 0.5 });
          if (!isNaN(psyche) && S.phase === "done") a2.bars([2.5], [psyche], 0.55, { color: GREEN });
        }
      },
      readout: function () {
        var n = S.answers.length, f = function (x) { return isNaN(x) ? "–" : Math.round(100 * x) + "%"; };
        var mine = n ? S.answers.filter(function (a) { return a.correct; }).length / n : NaN;
        return [["pairs answered", n + " of 8"], ["you chose the word", f(mine)], ["chance", "50%"],
                ["blue syllables spotted", S.hits + ""]];
      },
      note: "Nothing you do is stored or sent. Each run makes a new language of four three-syllable words, as in Saffran, Aslin and Newport (1996), whose eight-month-olds heard two minutes of such a stream. Inside a word the next syllable is certain; across a boundary it is one of three. Psyche's learner (language.transitional_probabilities) uses nothing else. With eight pairs your own score is rough: 6 or more right is better than chance would usually give.",
    });
  };
})();
