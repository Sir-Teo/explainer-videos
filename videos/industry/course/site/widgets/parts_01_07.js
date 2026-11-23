// Interactives for Act I, Reading an Industry (Parts 1-7).
(function () {
  "use strict";
  var C = QB.C, W = QB.W;

  // ---- Part 1: split the price of one phone ------------------------------------------------------------------
  // The film's model (explainer/industry/works/chain.py): the shop keeps a margin on the 60% of sales that go
  // through carriers and resellers; Apple pays for the parts, assembly ($30) and other costs of sales ($40); its
  // research and selling cost 14.9% of its revenue and its tax is 15.6% of its profit.
  W.splitprice = function (el) {
    var INDIRECT = 0.6, ASSEMBLY = 30, OTHER = 40, OPEX = 0.1493, TAX = 0.156;
    var model = function (price, channel, parts, memory) {
      var ch = price * INDIRECT * channel, rev = price - ch, gross = rev - parts - memory - ASSEMBLY - OTHER;
      var opex = OPEX * rev, pretax = gross - opex, tax = Math.max(0, TAX * pretax);
      return { ch: ch, rev: rev, parts: parts, memory: memory, asm: ASSEMBLY + OTHER, opex: opex, tax: tax,
               profit: pretax - tax, gm: rev > 0 ? gross / rev : 0 };
    };
    var names = ["shop or carrier", "other parts", "memory", "assembly, shipping, warranty", "Apple's research and selling", "tax", "Apple's profit"];
    var cols = [C.implied, C.cash, C.loss, C.house, C.spot, C.muted, C.gain];
    var stack = function (a, x, m) {
      var vals = [m.ch, m.parts, m.memory, m.asm, m.opex, m.tax, Math.max(0, m.profit)], base = 0, i;
      for (i = 0; i < vals.length; i++) {
        a.bars([x], [base + vals[i]], 0.55, { base: base, color: cols[i], alpha: 0.9 });
        base += vals[i];
      }
      return base;
    };
    QB.widget(el, {
      title: "Split the price: where $1,099 goes",
      sub: "The left column is the film's central case for a 256GB iPhone 17 Pro in 2025; the right column is the phone you set with the sliders. Raise the memory cost towards 2026's level (about $244) and watch Apple's profit shrink; then raise the price and see how much it takes to win it back.",
      panels: 2, height: 300,
      controls: [
        { k: "price", label: "Price before tax", min: 999, max: 1599, step: 10, value: 1099, fmt: function (x) { return "$" + x; } },
        { k: "channel", label: "Shop or carrier margin", min: 0, max: 0.2, step: 0.01, value: 0.1, fmt: function (x) { return Math.round(100 * x) + "%"; } },
        { k: "parts", label: "Parts other than memory", min: 350, max: 650, step: 5, value: 468, fmt: function (x) { return "$" + x; } },
        { k: "memory", label: "Memory and storage", min: 20, max: 400, step: 2, value: 52, fmt: function (x) { return "$" + x; } },
      ],
      draw: function (g, v, s) {
        var ref = model(1099, 0.1, 468, 52), m = model(v.price, v.channel, v.parts, v.memory), top;
        top = Math.max(1650, ref.ch + ref.parts + ref.memory + ref.asm + ref.opex + ref.tax + Math.max(0, ref.profit),
                       m.ch + m.parts + m.memory + m.asm + m.opex + m.tax + Math.max(0, m.profit));
        var a = g[0].axes({ x: [-0.6, 3.3], y: [0, top], title: "Dollars per phone", xticks: [0, 1],
                            xfmt: function (x) { return x < 0.5 ? "film, 2025" : "your phone"; } });
        stack(a, 0, ref);
        stack(a, 1, m);
        a.hline(v.price, { color: C.idea });
        a.legend(names.map(function (n, i) { return [n, cols[i]]; }).reverse(), { pos: "tr" });
        var xs = [], ys = [], mm;
        for (mm = 20; mm <= 400; mm += 5) { xs.push(mm); ys.push(model(v.price, v.channel, v.parts, mm).profit); }
        var b = g[1].axes({ x: [20, 400], y: [-150, 450], title: "Apple's profit per phone, against the memory cost",
                            xlabel: "memory and storage ($)", yfmt: function (y) { return "$" + Math.round(y); } });
        b.hline(0, { color: C.muted });
        b.hline(ref.profit, { color: C.gain, dash: [4, 4] });
        b.line(xs, ys, { color: C.gain, width: 1.6 });
        b.vline(52, { color: C.muted });
        b.vline(v.memory, { color: C.idea });
        b.legend([["profit at your price", C.gain], ["your memory cost", C.idea], ["2025 memory ($52)", C.muted]], { pos: "tr" });
        s.m = m; s.ref = ref;
      },
      readout: function (v, s) {
        var m = s.m, cents = function (x) { return Math.round(100 * x / v.price) + "¢"; };
        return [["Apple's profit", "$" + Math.round(m.profit) + " (" + cents(m.profit) + " of each $)"],
                ["the parts", "$" + Math.round(m.parts + m.memory) + " (" + cents(m.parts + m.memory) + ")"],
                ["memory's share of the parts", Math.round(100 * m.memory / Math.max(1, m.parts + m.memory)) + "%"],
                ["Apple's gross margin", Math.round(100 * m.gm) + "%"]];
      },
      note: "This is the film's model of one phone, not Apple's accounts: the split of the parts, the shop's margin, assembly and other costs are estimates with ranges (the Register, Part 1). Figures in US dollars, before sales tax.",
    });
  };
})();
