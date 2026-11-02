from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, KELLY, OVER, PART, UNDER, VALUE, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)
        self.pipeline(load("merton_us"), load("robust_fraction"), load("davis_norman"), env)

    def card(self):
        c = chapter_card(19, r"The sizing module", r"How big is every position the House takes?", part=PART)
        with self.voiceover("Chapter nineteen. The sizing module."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("data",)).scale(0.55).to_edge(UP, buff=0.15)
        rows = [
            (r"\texttt{crra}, \texttt{certainty\_equivalent}, \texttt{pratt\_premium}", r"utility and the price of risk"),
            (r"\texttt{bellman\_merton}, \texttt{hjb\_fd\_merton}", r"Merton by dynamic programming and by the HJB"),
            (r"\texttt{eikonal\_march}", r"monotone and non-monotone schemes, side by side"),
            (r"\texttt{merton\_consumption\_rate}, \texttt{no\_trade\_band}", r"spending, and the band of trading costs"),
            (r"\texttt{kelly\_binary}, \texttt{realized\_growth}", r"Kelly, and growth measured on history"),
            (r"\texttt{snell\_envelope}, \texttt{concave\_majorant}, \texttt{perpetual\_put}", r"stopping, three ways"),
            (r"\texttt{cpt\_value}, \texttt{robust\_fraction}, \texttt{theta\_for\_detection}",
             r"prospect theory, and doubt"),
            (r"\texttt{bsde\_regression}, \texttt{mfg\_liquidation}", r"nonlinear pricing, and the crowd"),
            (r"\texttt{ppo\_merton}, \texttt{ppo\_rebalance}, \texttt{grossman\_zhou\_fraction}",
             r"learners checked against answers; drawdown floors"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=18, color=QC.HOUSE), label(b, font_size=17, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.4)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.2:
            tab.scale_to_fit_width(13.2)
        with self.voiceover(
            "The House's sizing module collects this part's tools, every one tested against a closed form or a "
            "second method. <bookmark mark='a'/> Utility and certainty equivalents. Merton by dynamic programming and "
            "by finite differences on the HJB equation. The scheme comparison of the viscosity chapter. Consumption "
            "and the no-trade band. Kelly and realized growth. Stopping three ways. Prospect theory and robust "
            "fractions. The backward equation and the crowd. And the learners, which must agree with the answers "
            "before they are trusted with anything harder."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["portfolio"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.35, run_time=6))
        self.wait(0.4)
        self.clear_scene()

    def pipeline(self, m, rf, d, env):
        kel = m["fraction"][0]
        p20 = [r_ for r_ in rf["rows"] if abs(r_["p"] - 0.2) < 1e-9][0]
        rob_kelly = m["excess"] / ((1 + p20["theta"]) * m["sigma"] ** 2)
        steps_ = VGroup(
            MathTex(rf"\text{{1. Kelly on the estimate: }}\frac{{\hat\mu - r}}{{\sigma^2}} = {100 * kel:.0f}\%",
                    font_size=30, color=KELLY),
            MathTex(rf"\text{{2. half of it: }}{50 * kel:.0f}\%", font_size=30, color=UNDER),
            MathTex(rf"\text{{3. doubt (}}\theta = {p20['theta']:.1f}\text{{, 20\% detection error): }}"
                    rf"{100 * rob_kelly:.0f}\%", font_size=30, color=ALT),
            MathTex(r"\text{4. trade only outside the no-trade band}", font_size=30, color=VALUE),
            MathTex(r"\text{5. a drawdown budget as a Grossman--Zhou floor}", font_size=30, color=OVER),
            MathTex(r"\text{6. recompute whenever the volatility forecast moves}", font_size=30, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.6)
        rule = wrapped_label(r"Rule 9: no position above the Kelly fraction of its estimated edge; the default is half, "
                             r"or the robust fraction if smaller; rebalance only outside the no-trade band; a drawdown "
                             rf"budget is a Grossman--Zhou floor. The trial counter reads {env['trials']}.", 12.4, 22,
                             QC.HOUSE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is how the House sizes a position, on the US market's own numbers, with log utility as the "
            f"ceiling. Kelly on the estimated edge: {100 * kel:.0f} percent, more than twice levered. "
            f"<bookmark mark='a'/> Half of it, for the doubt in the estimate: {50 * kel:.0f}. Or, more carefully, the "
            "robust fraction with doubt calibrated to a twenty percent detection error: "
            f"{100 * rob_kelly:.0f} percent. <bookmark mark='b'/> Then trade only when the position leaves its "
            "no-trade band; cap losses with a drawdown floor that ratchets up; and recompute whenever the "
            "volatility forecast moves, so that a calm-market size never meets a storm. <bookmark mark='c'/> That is "
            "rule nine. This part registered three tests on the House's data, the split-sample Kelly fraction, "
            f"myopic loss aversion and volatility targeting, and the trial counter now reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(steps_[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps_[1]), FadeIn(steps_[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in steps_[3:]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
