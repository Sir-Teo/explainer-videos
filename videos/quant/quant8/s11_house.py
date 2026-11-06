from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import control as C
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
            ("crra, certainty_equivalent", r"preferences and money values"),
            ("bellman_merton, hjb_fd_merton", r"dynamic programming and HJB"),
            ("no_trade_band, merton_consumption_rate", r"costs and spending"),
            ("kelly_binary, realized_growth", r"Kelly and historical growth"),
            ("snell_envelope, perpetual_put", r"stopping and smooth fit"),
            ("cpt_value, robust_fraction", r"prospect theory and doubt"),
            ("bsde_regression, mfg_liquidation", r"nonlinear pricing and the crowd"),
            ("ppo_merton, ppo_rebalance", r"learners checked against benchmarks"),
        ]
        tab = VGroup(*[VGroup(data_text(a, font="DejaVu Sans Mono", font_size=18, color=QC.HOUSE),
                              label(b, font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.4)
                       for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.0)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.2:
            tab.scale_to_fit_width(13.2)
        with self.voiceover(
            "The House's sizing module collects this part's tools, every one tested against a closed form or a second "
            "method, because a sizing rule that is wrong is wrong on every position at once. <bookmark mark='a'/> Utility and "
            "certainty equivalents. Merton by dynamic programming and by finite differences on the HJB equation. The scheme "
            "comparison of the viscosity chapter. Consumption and the no-trade band. Kelly and realized growth. Stopping three "
            "ways: value iteration, the convex hull, and smooth fit. Prospect theory and robust fractions. The backward "
            "equation and the crowd. And the learners, which must agree with the answers before they are trusted with "
            "anything harder. Everything rebuilds from one command, and a viewer can change any input and rerun it."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["portfolio"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.35, run_time=6))
        self.wait(0.4)
        self.clear_scene()

    def pipeline(self, m, rf, d, env):
        kel = m["fraction"][0]
        th1 = C.theta_for_detection(0.2, m["excess"] + 0.02, 0.02, m["sigma"], 1.0, rf["years"])
        rob_kelly = float(C.robust_fraction(m["excess"] + 0.02, 0.02, m["sigma"], 1.0, th1))
        steps_ = VGroup(
            MathTex(rf"\text{{1. Kelly on the estimate: }}\frac{{\hat\mu - r}}{{\sigma^2}} = {100 * kel:.0f}\%",
                    font_size=30, color=KELLY),
            MathTex(rf"\text{{2. half of it: }}{50 * kel:.0f}\%", font_size=30, color=UNDER),
            MathTex(rf"\text{{3. doubt (}}\theta = {th1:.2f}\text{{, 20\% detection error): }}"
                    rf"{100 * rob_kelly:.0f}\%", font_size=30, color=ALT),
            MathTex(r"\text{4. trade only outside the no-trade band}", font_size=30, color=VALUE),
            MathTex(r"\text{5. a GZ-inspired nominal drawdown cushion}", font_size=30, color=OVER),
            MathTex(r"\text{6. recompute whenever the volatility forecast moves}", font_size=30, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.6)
        rule = wrapped_label(r"Rule 9 (illustrative House governance): estimated Kelly is a reference cap, not a universal optimal bound; default to half, "
                             r"or the robust fraction if smaller; rebalance only outside the no-trade band; a drawdown "
                             rf"budget uses a GZ-inspired nominal cushion; discrete trading and jumps can breach it. The trial counter reads {env['trials']}.", 12.4, 22,
                             QC.HOUSE).to_edge(DOWN, buff=0.35)
        guide = wrapped_label(r"Separate model rules combined in one illustrative pipeline", 12.4, 22, GREY_A).set_y(-1.3)
        with self.voiceover(
            "Here is how the House sizes a position, on the US market's own numbers, with log utility as the ceiling. "
            f"Kelly on the estimated edge: {100 * kel:.0f} percent, more than twice levered. <bookmark mark='a'/> Half of it, "
            f"for the doubt in the estimate: {50 * kel:.0f}. The robust fraction, with doubt calibrated to a twenty percent "
            f"detection error, is {100 * rob_kelly:.0f} percent; the House takes the smaller of the two. "
            "<bookmark mark='b'/> Then trade only when the position leaves its no-trade band; apply a nominal drawdown "
            "floor that ratchets up; and recompute whenever the volatility forecast moves, while recognizing that forecast updates cannot prevent sudden jumps. This is an illustrative governance pipeline, not a jointly optimal control solution or a drawdown guarantee. <bookmark mark='c'/> That is rule nine. This part registered three tests on the House's data, the "
            "split-sample Kelly fraction, myopic loss aversion and volatility targeting, and the trial counter now reads "
            f"{env['trials']}."
        ) as vo:
            self.play(FadeIn(steps_[0]), FadeIn(guide), run_time=0.5)
            vo.wait_until("a")
            self.play(FadeIn(steps_[1]), FadeIn(steps_[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in steps_[3:]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
