// Interactives for Act V, The Long Run (Parts 19-24).  Each is a game the reader plays (the kit: 00_games.js).
(function () {
  "use strict";
  var W = QB.W;
  var GOLD = "#F6C453", RED = "#F25F5C", GREEN = "#7BD88F", GREY_HINT = "#8B93A1", BLUE = "#9FB8F2";

  // ---- Part 19: the great escape ---------------------------------------------------------------------------------
  W.malthus = function (el) {
    // the Malthusian island of Part 19 (explainer.economics.agora.malthus: simulate): income per head A (X / L)^beta on
    // fixed land, population growing at lambda ln(y / ybar) a year, here capped at a maximum rate (the reader's
    // demographic transition); a plague in year 100, a better plough in year 250, and technology that may also grow
    // steadily every year.  Can the reader find a setting in which income per head keeps rising?
    var T = 400;
    function run(v) {
      var L = 1, A = 1, ys = [], Ls = [], ts = [];
      for (var t = 0; t <= T; t++) {
        if (t === 100) L *= 1 - v.plague;
        if (t === 250) A *= 1 + v.plough;
        var y = A * Math.pow(1 / L, v.beta);
        ts.push(t); ys.push(y); Ls.push(L);
        var grow = Math.min(v.lam * Math.log(y), v.cap);
        L *= Math.exp(grow);
        A *= 1 + v.g;
      }
      return { t: ts, y: ys, L: Ls };
    }
    QB.widget(el, {
      title: "Can the island escape?",
      sub: "Income per head is technology times land per person to the power beta, and the population grows when " +
           "income is above subsistence (1 on the left chart). A plague strikes in year 100 and a better plough " +
           "arrives in year 250. Then add steady technological progress, and cap how fast the population can grow, " +
           "as a demographic transition would. Which settings let income per head keep rising?",
      panels: 2, height: 300,
      controls: [
        { k: "beta", label: "Diminishing returns, beta", min: 0.2, max: 1.0, step: 0.05, value: 0.6 },
        { k: "lam", label: "How fast population follows income, lambda", min: 0.005, max: 0.05, step: 0.005,
          value: 0.02 },
        { k: "plague", label: "Share killed by the plague in year 100", min: 0, max: 0.6, step: 0.05, value: 0.45,
          fmt: function (x) { return (100 * x).toFixed(0) + "%"; } },
        { k: "plough", label: "Gain from the better plough in year 250", min: 0, max: 1.0, step: 0.1, value: 0.5,
          fmt: function (x) { return "+" + (100 * x).toFixed(0) + "%"; } },
        { k: "g", label: "Steady technological progress, a year", min: 0, max: 0.02, step: 0.001, value: 0,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
        { k: "cap", label: "Fastest the population can grow, a year", min: 0, max: 0.03, step: 0.001, value: 0.03,
          fmt: function (x) { return (100 * x).toFixed(1) + "%"; } },
      ],
      draw: function (g, v, s) {
        var r = run(v);
        s.r = r;
        var ymax = Math.max(2, Math.max.apply(null, r.y) * 1.1);
        var a = g[0].axes({ x: [0, T], y: [0, ymax], title: "Income per head (subsistence = 1)", xlabel: "year" });
        a.line(r.t, r.y, { color: GOLD, width: 2.5 });
        a.hline(1, { color: GREY_HINT });
        var Lmax = Math.max(2, Math.max.apply(null, r.L) * 1.1);
        var b = g[1].axes({ x: [0, T], y: [0, Lmax], title: "Population (year 0 = 1)", xlabel: "year" });
        b.line(r.t, r.L, { color: RED, width: 2.5 });
      },
      readout: function (v, s) {
        var r = s.r;
        if (!r) return [];
        var yEnd = r.y[r.y.length - 1], y300 = r.y[300], hl = Math.log(2) / (v.lam * v.beta);
        var rising = yEnd > y300 * 1.05;
        return [["income per head in year 400", yEnd.toFixed(2) + " (subsistence 1)"],
                ["population in year 400", r.L[r.L.length - 1].toFixed(2)],
                ["half-life of a shock, without progress", hl.toFixed(0) + " years"],
                ["still rising at the end?", rising ? "yes: the island is escaping" :
                  (yEnd > 1.2 ? "no: a higher plateau, but not rising" : "no: back in the trap")]];
      },
      note: "With no steady progress the island always returns to subsistence: technology buys people, not income " +
            "(Part 19, chapter 2). Steady progress alone lifts income only to a higher plateau. Income keeps rising " +
            "only when progress outruns the fastest the population can grow. Computed in your browser; nothing you do " +
            "here is stored or sent.",
    });
  };
})();
