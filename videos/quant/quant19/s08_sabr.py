from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import NORMAL, PART, ask, fit_right, illustration, load


class SABR(VoiceoverScene):
    def construct(self):
        s = load("sabr")
        self.card()
        self.model()
        self.dials(s)

    def card(self):
        c = chapter_card(7, r"SABR for rates", r"Why does every expiry have its own smile?", lit=(2002,), part=PART)
        with self.voiceover("Chapter seven. SABR: the model every rates desk uses for the smile."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"dF_t", r"=", r"\alpha_t\,F_t^{\beta}\,dW_t", font_size=44, colors={r"dF_t": NORMAL}),
                cmath(r"d\alpha_t", r"=", r"\nu\,\alpha_t\,dZ_t,\qquad d\langle W, Z\rangle = \rho\,dt", font_size=42,
                      colors={r"d\alpha_t": QC.VEGA}),
                cmath(r"\sigma_N(K)", r"\approx", r"\alpha\,\frac{z}{x(z)}\Big(1 + \tfrac{2 - 3\rho^2}{24}\,\nu^2 T\Big),"
                      r"\quad z = \tfrac{\nu}{\alpha}(F - K)", font_size=36, colors={r"\sigma_N(K)": NORMAL})]
        whys = [why(r"Hagan, Kumar, Lesniewski and Woodward (2002): one forward rate (a swap rate, or a caplet's rate), "
                    r"with no drift under its own measure"),
                why(r"its volatility is itself random, and correlated with it: Part 13's stochastic volatility, one "
                    r"expiry at a time"),
                why(r"$\beta = 0$, the normal SABR used where rates can be negative: a closed-form smile, "
                    r"$x(z) = \ln\frac{\sqrt{1 - 2\rho z + z^2} + z - \rho}{1 - \rho}$ (the House's \texttt{sabr\_normal\_iv})")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.4, buff=0.7, edge=6.9)
        with self.voiceover(
            "Market swaptions and caps are not flat in strike; they smile. In 2002 Patrick Hagan and his coauthors "
            "wrote the model that the market adopted for it, SABR. Take one forward rate, with no drift under its own "
            "measure. <bookmark mark='a'/> Make its volatility random too, and correlated with the rate: Part "
            "thirteen's stochastic volatility, applied one expiry at a time. <bookmark mark='b'/> With beta equal to "
            "zero, the normal version used since rates went negative, the implied normal volatility has a closed form."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def dials(self, s):
        K = (np.asarray(s["K"]) - s["F"]) * 1e4
        base = np.asarray(s["base"]) * 1e4
        panels = VGroup()
        titles = {"alpha": r"$\alpha$: the level", "rho": r"$\rho$: the skew", "nu": r"$\nu$: the curvature"}
        for name in ("alpha", "rho", "nu"):
            g = axes([K.min(), K.max()], [40, 200], x_length=3.8, y_length=3.0, xlabel=r"strike $-$ forward, bp",
                     ylabel=titles[name], xticks=[-300, 0, 300], yticks=[50, 100, 150], font_size=12)
            ax = g.ax
            lines = VGroup(curve(ax, K, np.clip(base, 40, 200), WHITE, stroke_width=2.5))
            for v_, c_ in zip(s[name], (QC.SPOT, QC.OPTION)):
                lines.add(curve(ax, K, np.clip(np.asarray(v_) * 1e4, 40, 200), c_, stroke_width=2.5))
            vals = s[name + "_vals"]
            lab = MathTex(rf"{vals[0]:g}\ \ /\ \ {s['params'][name]:g}\ \ /\ \ {vals[1]:g}", font_size=20).next_to(
                g, DOWN, buff=0.1)
            panels.add(VGroup(g, lines, lab))
        panels.arrange(RIGHT, buff=0.45).shift(DOWN * 0.3)
        leg = legend([(QC.SPOT, r"lower"), (WHITE, r"base"), (QC.OPTION, r"higher")], font_size=17).arrange(
            RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"normal vol in bp a year against strike, a 2-year option on a 3.5\% forward; illustrative "
                             r"parameters. A desk fits $\alpha$, $\rho$ and $\nu$ to each expiry's quotes every day, and "
                             r"uses the fitted model to price strikes nobody quotes", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Each parameter has one job. <bookmark mark='a'/> Alpha sets the level of the smile, up and down. "
            "<bookmark mark='b'/> Rho tilts it: when volatility tends to rise as the rate falls, a negative rho, low "
            "strikes become dearer. <bookmark mark='c'/> And nu, the volatility of volatility, bends the wings up. A desk fits "
            "the three to each expiry's quotes every morning, and uses the fitted curve to price every strike in "
            "between, and every strike beyond."
        ) as vo:
            self.play(FadeIn(leg), FadeIn(foot))
            for i, m in enumerate(("a", "b", "c")):
                vo.wait_until(m)
                self.play(FadeIn(panels[i]))
        q = ask(r"SABR fits each expiry separately. What can go wrong when you price a product that depends on two "
                r"expiries at once?")
        with self.voiceover("SABR fits each expiry on its own. What can go wrong when a product depends on two expiries "
                            "at once?"):
            self.play(FadeOut(foot), FadeIn(q))
        self.add(illustration(r"Hagan, Kumar, Lesniewski and Woodward (2002), normal SABR; illustrative parameters"))
        self.wait(0.5)
        self.clear_scene()
