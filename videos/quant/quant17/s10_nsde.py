from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, IV, NET, OPT, PART, REF, illustration, load


class NSDE(VoiceoverScene):
    def construct(self):
        n = load("nsde")
        self.card()
        self.model()
        self.bounds(n)

    def card(self):
        c = chapter_card(9, r"Neural SDEs and robust bounds", r"How wrong can an exotic price be, if the vanillas are right?",
                         part=PART)
        with self.voiceover("Chapter nine. Neural SDEs and robust bounds."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"dX_t", r"=", r"-\tfrac12\sigma_\theta^2\,dt + \sigma_\theta(t, X_t, V_t)\,dW^1_t", font_size=36,
                      colors={r"dX_t": NET}),
                cmath(r"dV_t", r"=", r"b_\theta(t, V_t)\,dt + \eta_\theta(t, V_t)\,dW^2_t,\quad d\langle W^1, W^2\rangle = "
                      r"\rho\,dt", font_size=34, colors={r"dV_t": NET}),
                cmath(r"\min_\theta\ /\ \max_\theta", r"\ ", r"\text{exotic}(\theta)\quad \text{subject to every vanilla "
                      r"repriced}", font_size=34, colors={r"\min_\theta\ /\ \max_\theta": GOOD})]
        whys = [why(r"Gierjatowicz, Sabate-Vidales, \v{S}i\v{s}ka, Szpruch and \v{Z}uri\v{c} (2022): a stochastic volatility "
                    r"model whose coefficients are networks, simulated by Euler steps and differentiated end to end"),
                why(r"a hidden factor $V$ drives the volatility; drift, volatility of volatility and correlation are all "
                    r"learned, so the model can produce any smile Heston can, and many it cannot"),
                why(r"calibrate to vanilla prices, then push the price of an exotic as low and as high as it will go while "
                    r"the vanillas stay repriced: a range, not a point. Part 9's robust bounds and Part 15's model reserve, "
                    r"computed with a model rich enough to matter")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "Part fifteen asked what to charge for not knowing the model. Here is a modern answer. Write a stochastic "
            "volatility model whose coefficients are all neural networks, simulate it with Euler steps, and "
            "differentiate through the simulation. <bookmark mark='a'/> A hidden factor drives the volatility, and its "
            "drift, its volatility and its correlation with the price are all learned. <bookmark mark='b'/> Calibrate "
            "it to the vanilla options. Then push the price of an exotic as low as it will go, and as high, while every "
            "vanilla stays repriced. The answer is a range, and its width is the model risk."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def bounds(self, n):
        su = n["setup"]
        lo, hi, cal, hes = n["low"], n["high"], n["calibrated"], n["heston_doc"]
        vals = [lo["doc"], cal["doc"], hes, hi["doc"]]
        span = max(vals) - min(vals)
        a, b = min(vals) - 0.6 * span, max(vals) + 0.6 * span
        g = axes([a, b], [-1, 1], x_length=10.0, y_length=1.6, xlabel=r"price of the down-and-out call (per unit of spot)",
                 xticks=list(np.linspace(a, b, 5)), xfmt=lambda v: f"{v:.4f}", yticks=[], font_size=15)
        g.move_to(UP * 0.2)
        ax = g.ax
        band = Line(ax.c2p(lo["doc"], 0), ax.c2p(hi["doc"], 0), stroke_color=GOOD, stroke_width=14, stroke_opacity=0.6)
        marks = VGroup()
        for v, txt, col, side in ((lo["doc"], r"lowest", GOOD, DOWN), (hi["doc"], r"highest", GOOD, DOWN),
                                  (hes, r"Heston, the model behind the vanillas", REF, UP),
                                  (cal["doc"], r"the first calibration", NET, UP)):
            d = Dot(ax.c2p(v, 0), radius=0.08, color=col)
            lab = VGroup(label(txt, font_size=17, color=col), MathTex(f"{v:.4f}", font_size=24, color=col)).arrange(DOWN, buff=0.06)
            lab.next_to(d, side, buff=0.25 if side is DOWN else 0.35)
            marks.add(VGroup(d, lab))
        if abs(hes - cal["doc"]) < (b - a) * 0.12:
            marks[3][1].shift(UP * 0.75)
        head = label(rf"a down-and-out call: strike 1, barrier {su['barrier']:g}, one year, watched on {su['steps']} dates",
                     font_size=24).to_edge(UP, buff=0.6)
        foot = wrapped_label(rf"all three neural models reprice the same 36 vanilla calls (4 expiries, 9 strikes) to within "
                             rf"{max(lo['iv_rmse'], hi['iv_rmse'], cal['iv_rmse']):.2f} vol points of Heston's; yet the exotic "
                             rf"ranges from {lo['doc']:.4f} to {hi['doc']:.4f}, {100 * (hi['doc'] - lo['doc']) / hes:.0f}\% of "
                             r"Heston's price. Vanillas fix the marginal distributions; a barrier depends on how they are "
                             r"joined through time, which they do not fix. Small networks, trained for minutes: the true "
                             r"range is at least this wide", 11.8, 20, GREY_A).to_edge(DOWN, buff=0.45)
        src = illustration(r"neural SDE with 3 small networks; 16{,}384 paths a step; prices checked on 200{,}000 fresh paths",
                           corner=UR)
        with self.voiceover(
            "Here is the result for a down-and-out call, with the vanilla prices generated by Heston's model. "
            f"<bookmark mark='a'/> The first calibration prices the barrier option at {cal['doc']:.4f}; Heston's own "
            f"price is {hes:.4f}. <bookmark mark='b'/> Pushed down and up while still repricing every vanilla, the "
            f"neural model reaches {lo['doc']:.4f} and {hi['doc']:.4f}: a range of {100 * (hi['doc'] - lo['doc']) / hes:.0f} "
            "percent of the price, from models that all agree on every quoted option. The vanillas fix how far the "
            "price is likely to go by each date; the barrier depends on the path in between, which they do not fix. "
            "And this is only a lower estimate of the true range: every model here is a real, calibrated one, so the "
            "range is at least this wide, and a richer network trained for longer can only widen it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(src))
            self.play(FadeIn(marks[2]))
            vo.wait_until("a")
            self.play(FadeIn(marks[3]))
            vo.wait_until("b")
            self.play(Create(band), FadeIn(marks[0]), FadeIn(marks[1]), FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()
