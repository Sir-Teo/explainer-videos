from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        o = load("orders")
        self.card()
        self.library(env, o)

    def card(self):
        c = chapter_card(8, r"The simulation library", r"Which numbers can a simulation be trusted with?", part=PART)
        with self.voiceover("Chapter eight. The simulation library."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def library(self, env, o):
        chart = house_chart(PART, lit=("data",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{euler\_maruyama}, \texttt{milstein}", rf"strong orders {o['slope_strong_euler']:.2f} and "
                                                            rf"{o['slope_strong_milstein']:.2f}, measured on GBM"),
            (r"\texttt{ou\_exact}, \texttt{cir\_exact}", r"exact transitions: stationary moments checked"),
            (r"\texttt{merton\_jumps}", r"compensated drift: $\mathbb{E}[S_T] = S_0 e^{\mu T}$ checked"),
            (r"\texttt{hawkes\_thinning}, \texttt{hawkes\_fit}", r"rate $\mu/(1 - \alpha/\beta)$ and the MLE recovered"),
            (r"\texttt{fbm}, \texttt{hurst\_from\_increments}", r"$H$ recovered at 0.1, 0.5 and 0.8"),
            (r"\texttt{signature2}", r"Chen's identity; the unit square's L\'evy area is 1"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=21, color=QC.HOUSE), label(b, font_size=20, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 5.4)
        tab.next_to(chart, DOWN, buff=0.35)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 6: every simulator is tested against a case with a known answer before any desk "
                             rf"prices with it.  The trial counter reads {env['trials']}.", 12.4, 23,
                             QC.HOUSE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The House's simulation library is now built, and every routine in it is tested against a case where the "
            "answer is known. <bookmark mark='a'/> The two schemes, with their measured orders. Exact transitions "
            "for mean-reverting rates. A jump-diffusion whose drift is compensated. Hawkes processes, simulated by "
            "thinning and fitted by maximum likelihood. Fractional Brownian motion, with the Hurst estimator checked "
            "on it. And path signatures. <bookmark mark='b'/> Which gives the House its sixth rule: no desk prices "
            "with a simulator that hasn't first reproduced a known answer."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
