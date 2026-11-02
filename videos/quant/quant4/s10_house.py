from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import MART, PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.monitor()
        self.desk(env)

    def card(self):
        c = chapter_card(9, r"The e-value monitor", r"When should the House believe a result?", part=PART)
        with self.voiceover("Chapter nine. The e-value monitor."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def monitor(self):
        code = VGroup(*[data_text(t, font_size=20, font="DejaVu Sans Mono") for t in [
            "from explainer.quant.house.martingale import EProcess",
            "e = EProcess()                      # a mixture of bettors, wealth 1",
            "for x in daily_scaled_pnl:          # |x| < 1, mean zero under the null",
            "    e.update(x)                     # wealth *= 1 + lambda * x",
            "    if e.rejected(alpha=0.05):      # wealth ever >= 20",
            "        flag(strategy)",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        code[1:].shift(DOWN * 0.2)
        box = SurroundingRectangle(code, buff=0.3, color=GREY_C, corner_radius=0.1)
        panel = VGroup(box, code).to_edge(UP, buff=0.6)
        uses = VGroup(
            label(r"what it watches", font_size=24, color=GREY_A),
            label(r"a strategy's daily profit: is its edge real, or a fair game with a lucky start?", font_size=22),
            label(r"a market: is it a fair game for a class of bets (chapter 8)?", font_size=22),
            label(r"a model: are its forecasts calibrated, day after day (Part 26)?", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(panel, DOWN, buff=0.5)
        with self.voiceover(
            "The House's monitor is a few lines of code, and it is tested. Feed it a daily number that should have mean "
            "zero if nothing is going on, scaled to lie between minus one and one: a strategy's profit over its "
            "recent volatility, say. It updates the wealth of a mixture of bettors, and raises a flag if that wealth "
            "ever reaches twenty. <bookmark mark='a'/> It can watch a strategy, to tell an edge from a lucky start; a "
            "market, as in the last chapter; or a model's forecasts, which is how Part twenty-six will use it, when "
            "the research desk tests hundreds of ideas and has to know which results to believe."
        ) as vo:
            self.play(Create(box), LaggedStart(*[FadeIn(c) for c in code], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(u) for u in uses], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def desk(self, env):
        chart = house_chart(PART, lit=("data",)).scale(0.72).to_edge(UP, buff=0.25)
        items = VGroup(
            label(r"\texttt{martingale}: doubling, gambler's ruin, Doob's decomposition, likelihood ratios", font_size=22),
            label(r"stable laws (McCulloch), Mantegna--Stanley scaling, and the e-process monitor", font_size=22),
            label(rf"the trial counter now reads {env['trials']}; the Nikkei's hold-out from 2021 is sealed", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(chart, DOWN, buff=0.4)
        if items.width > 13.0:
            items.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 5: a claim that something beats a fair game is tested with an e-process, valid "
                             r"whenever it is checked.", 12.0, 24, QC.HOUSE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The data desk gains the martingale library: the doubling system and the gambler's ruin, Doob's "
            "decomposition, likelihood ratios, stable-law fits and the monitor. <bookmark mark='a'/> The trial "
            f"counter now reads {env['trials']}, and the Nikkei's hold-out years are sealed. <bookmark mark='b'/> And "
            "the House adopts its fifth rule: a claim that anything beats a fair game is tested with an e-process, "
            "valid whenever it is checked."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05), FadeIn(items[:2]))
            vo.wait_until("a")
            self.play(FadeIn(items[2]))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
