from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import exotics as X
from videos.quant.quant15.common import BAD, BARRIER, DELTA, GOOD, OPT, PART, SPOT, illustration, load


class Barriers(VoiceoverScene):
    def construct(self):
        b = load("barrier")
        self.card()
        self.reflection()
        self.monitoring(b)
        self.delta(b)

    def card(self):
        c = chapter_card(2, r"Barriers", r"What is an option worth if it can die on the way?", part=PART)
        with self.voiceover("Chapter two. Barriers."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def reflection(self):
        g = np.random.default_rng(4)
        n = 300
        t = np.linspace(0, 1, n + 1)
        x = np.concatenate([[0], np.cumsum(g.standard_normal(n) * np.sqrt(1 / n) * 0.9)])
        # force a crossing for the picture
        x = x - 0.6 * np.sin(np.pi * t) * 1.2
        hb = -0.45
        i = int(np.argmax(x < hb))
        refl = x.copy()
        refl[i:] = 2 * hb - x[i:]
        ax = axes([0, 1], [-1.6, 0.9], x_length=8.0, y_length=4.4, xlabel=r"time", ylabel=r"log price", xticks=[],
                  yticks=[], font_size=16).to_edge(LEFT, buff=0.7)
        a = ax.ax
        bar = DashedLine(a.c2p(0, hb), a.c2p(1, hb), stroke_color=BARRIER, stroke_width=3)
        bl = label(r"barrier $H$", font_size=20, color=BARRIER).next_to(a.c2p(1, hb), RIGHT, buff=0.1)
        p1 = curve(a, t, x, SPOT, stroke_width=2.5)
        p2 = curve(a, t[i:], refl[i:], OPT, stroke_width=2.5)
        dot = Dot(a.c2p(t[i], hb), radius=0.07, color=WHITE)
        rows = [cmath(r"C_{\text{down-out}}", r"=", r"C(S) - \Big(\frac{H}{S}\Big)^{2\lambda - 2} C\Big(\frac{H^2}{S}\Big)",
                      font_size=34, colors={r"C_{\text{down-out}}": OPT})]
        side = VGroup(rows[0], wrapped_label(r"the reflection principle: every path that touches the barrier and ends "
                                             r"above the strike has a mirror image that ends below; so the value of the "
                                             r"paths that died is a vanilla priced from the mirrored spot $H^2/S$ "
                                             r"(Merton 1973; Reiner and Rubinstein 1991), with $\lambda = (r - q)/\sigma^2"
                                             r" + \tfrac12$", 4.4, 19, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        side.to_edge(RIGHT, buff=0.35)
        src = illustration(r"one Brownian path and its reflection after the first touch")
        with self.voiceover(
            "A barrier option is a vanilla that can die, or be born, on the way. A down-and-out call is a call that "
            "vanishes the moment the price touches a barrier below. How do you price the paths that died? "
            "<bookmark mark='a'/> Reflect them. From the first touch, every path has a mirror image across the "
            "barrier, equally likely under Brownian motion. So the value of the paths that touched and finished "
            "above the strike equals the value of mirrored paths finishing below. <bookmark mark='b'/> The result "
            "is a closed form: the vanilla, minus a vanilla priced from the mirrored spot, H squared over S. Robert "
            "Merton wrote it down in 1973; Eric Reiner and Mark Rubinstein catalogued the whole family in 1991."
        ) as vo:
            self.play(FadeIn(ax), Create(bar), FadeIn(bl), Create(p1), FadeIn(src), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(dot), Create(p2), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def monitoring(self, b):
        rows = b["rows"]
        tab = VGroup(VGroup(label(r"barrier watched", font_size=22, color=GREY_A),
                            label(r"Monte Carlo", font_size=22, color=GREY_A),
                            label(r"closed form, shifted barrier", font_size=22, color=GREY_A)))
        for r in rows:
            tab.add(VGroup(label(r["name"], font_size=24), MathTex(rf"{r['mc']:.2f} \pm {2 * r['se']:.2f}", font_size=28),
                           MathTex(f"{r['bgk']:.2f}", font_size=28, color=GOOD)))
        tab.add(VGroup(label(r"the textbook formula", font_size=24, color=GREY_A),
                       VectorizedPoint(), MathTex(f"{b['continuous']:.2f}", font_size=28, color=BAD)))
        xs = [-3.8, 0.6, 4.2]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.2 - 0.62 * i, 0])
        rows_tex = cmath(r"H_{\text{eff}}", r"=", r"H\,e^{-\beta\sigma\sqrt{\Delta t}},\quad \beta = "
                         r"-\frac{\zeta(\frac12)}{\sqrt{2\pi}} \approx 0.5826", font_size=32,
                         colors={r"H_{\text{eff}}": BARRIER}).to_edge(DOWN, buff=1.1)
        note_ = wrapped_label(r"Broadie, Glasserman and Kou (1997): a barrier checked every $\Delta t$ behaves like a "
                              r"continuous one moved away by this factor; term sheets watch at the close, not continuously",
                              11.0, 20, GREY_A).next_to(rows_tex, DOWN, buff=0.2)
        p = b["params"]
        src = illustration(rf"down-and-out call: $S = K = {p['S']:.0f}$, $H = {p['H']:.0f}$, six months, $\sigma = "
                           rf"{100 * p['sigma']:.0f}\%$; 100{{,}}000 paths, 20 steps a day", corner=UR)
        with self.voiceover(
            "There is a catch. The formula assumes the barrier is watched continuously. Real term sheets check it "
            "once a day, at the close, or once a month. A barrier watched less often is harder to hit, so the "
            f"knock-out is worth more: {rows[0]['mc']:.2f} watched monthly, against {b['continuous']:.2f} for the "
            "textbook formula. <bookmark mark='a'/> Mark Broadie, Paul Glasserman and Steven Kou found the fix in "
            "1997: move the barrier away by a factor of e to the beta sigma root delta t, with beta about 0.58, a "
            "constant from the Riemann zeta function. Then the continuous formula matches every frequency to the "
            "second decimal."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(src), LaggedStart(*[FadeIn(r_[:2]) for r_ in tab[1:-1]], lag_ratio=0.2),
                      FadeIn(tab[-1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in tab[1:-1]], lag_ratio=0.2), FadeIn(rows_tex), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def delta(self, b):
        S = np.asarray(b["S"])
        g1 = axes([80, 130], [0, 30], x_length=5.6, y_length=3.4, xlabel=r"spot", ylabel=r"value",
                  xticks=[85, 100, 115, 130], yticks=[0, 10, 20, 30], font_size=15)
        g2 = axes([80, 130], [0, 1.2], x_length=5.6, y_length=3.4, xlabel=r"spot", ylabel=r"delta",
                  xticks=[85, 100, 115, 130], yticks=[0, 0.5, 1.0], font_size=15)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).to_edge(UP, buff=1.0)
        p = b["params"]
        van = X.bs.price(S, p["K"], p["T"], p["sigma"], p["r"])
        lv = curve(g1.ax, S, np.clip(van, 0, 30), GREY_B, stroke_width=2)
        lb = curve(g1.ax, S, np.clip(np.asarray(b["value"]), 0, 30), OPT, stroke_width=3)
        ld = curve(g2.ax, S, np.clip(np.asarray(b["delta"]), 0, 1.2), DELTA, stroke_width=3)
        bars = VGroup(*[DashedLine(g.ax.c2p(p["H"], lo), g.ax.c2p(p["H"], hi), stroke_color=BARRIER, stroke_width=2)
                        for g, lo, hi in ((g1, 0, 30), (g2, 0, 1.2))])
        leg = legend([(GREY_B, r"vanilla call"), (OPT, r"down-and-out call")], font_size=17).next_to(g1, DOWN, buff=0.2)
        Sd = np.asarray(b["delta"])
        near = float(Sd[np.argmax(S > p["H"] + 0.2)])
        foot = wrapped_label(rf"just above the barrier the option is worth almost nothing, yet the hedge still holds "
                             rf"{near:.2f} units per option; on the touch, delta falls to zero and the whole hedge must be "
                             r"sold at once. Dealers watching the same barrier sell together: popular barrier levels are "
                             r"where markets gap", 11.5, 20, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The hedging is where barriers bite. Just above the barrier, the down-and-out call is worth almost "
            f"nothing, but the dealer's hedge still holds {near:.2f} units of the underlying per option. "
            "<bookmark mark='a'/> On the touch the option dies, its delta drops to zero, and the whole hedge must be "
            "sold at once. Every dealer watching the same level must sell at the same moment. That is why barrier "
            "levels on popular products are where markets gap."
        ) as vo:
            self.play(FadeIn(g1), Create(lv), Create(lb), FadeIn(leg), Create(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(ld), Create(bars[1]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
