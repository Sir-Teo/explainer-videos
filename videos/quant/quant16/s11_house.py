from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)

    def card(self):
        c = chapter_card(10, r"The pricing engine", r"How does the desk choose a method, and know it is right?", part=PART)
        with self.voiceover("Chapter ten. The pricing engine."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("data", "vol")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{mc\_call}, \texttt{normals}, \texttt{brownian\_bridge}", r"Monte Carlo, variance reduction, Sobol"),
            (r"\texttt{mlmc}", r"multilevel Monte Carlo"),
            (r"\texttt{lsm\_put}, \texttt{andersen\_broadie\_put}", r"American options with both bounds"),
            (r"\texttt{greeks\_three\_ways}, \texttt{aad\_greeks}", r"bumps, pathwise, likelihood ratio, adjoints"),
            (r"\texttt{fd\_european}, \texttt{fd\_american\_put}", r"theta schemes, Rannacher, PSOR"),
            (r"\texttt{heston\_adi}", r"Douglas and Craig--Sneyd on non-uniform grids"),
            (r"\texttt{carr\_madan}, \texttt{cos\_price}", r"Fourier pricing"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=19, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.6)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 16: every price leaves the engine with its error estimate (a standard error, a duality "
                             r"gap or a grid-refinement difference), and every method is checked nightly against a second, "
                             r"independent one on the same product.  "
                             rf"The trial counter still reads {env['trials']}.", 12.4, 22, QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The House now has a pricing engine, shared by every desk. <bookmark mark='a'/> Monte Carlo with its "
            "variance reduction and Sobol points. Multilevel simulation. American options with both bounds. Greeks "
            "three ways, and by adjoints. Finite differences with Rannacher's start, the American problem, and ADI "
            "for two dimensions. And Fourier pricing. <bookmark mark='b'/> The sixteenth rule: no price leaves the "
            "engine without its error, a standard error, a duality gap, or the change under grid refinement, and every "
            "method is checked each night against an independent one on the same product. No strategy was tested, and "
            f"the counter still reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
