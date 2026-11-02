from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import PART, load


class Hardware(VoiceoverScene):
    def construct(self):
        self.card()
        self.cards(load("race"))

    def card(self):
        c = chapter_card(9, r"Hardware: grids, GPUs and quantum", r"What does a faster machine actually buy?", part=PART)
        with self.voiceover("Chapter nine. Hardware: grids, GPUs, and quantum computers."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def cards(self, race):
        pts = race["points"]
        mc = min((q for q in pts if q["method"].startswith("Monte Carlo")), key=lambda q: q["err"])
        cos = min((q for q in pts if q["method"] == "COS" and q["err"] < mc["err"]), key=lambda q: q["time"])
        speed = f"{round(mc['time'] / cos['time'], -3):,.0f}".replace(",", "{,}")
        a = history_card(r"overnight", r"the bank risk run", r"Every night a bank reprices its whole book under thousands of "
                         r"scenarios for risk limits, capital and valuation adjustments (Part 21), on grids of thousands of "
                         r"machines. Monte Carlo is embarrassingly parallel, so GPUs took over much of it.",
                         color=QC.FIRM, width=6.2, font_size=20)
        b = history_card(2011, r"JPMorgan and Maxeler", r"The bank reported moving the core of its credit-derivative risk "
                         r"model onto FPGA chips: a full run that had taken eight hours or more fell to about four minutes, "
                         r"so scenarios could be rerun during the day.", color=QC.FIRM, width=6.2, font_size=20)
        c = history_card(2021, r"Chakrabarti et al., \textit{Quantum}", r"Quantum amplitude estimation needs $1/\varepsilon$ "
                         r"samples instead of Monte Carlo's $1/\varepsilon^2$. But to beat a classical computer on a "
                         r"benchmark derivative they estimated about 8{,}000 error-corrected logical qubits and a T-depth "
                         r"of 54 million, run in about a second: far beyond any machine built so far.", color=QC.IDEA,
                         width=6.2, font_size=20)
        d = history_card(r"the lesson", r"algorithms first", rf"In the race of chapter 8, on one core, COS beat Monte Carlo's best "
                         rf"accuracy about {speed} times faster. Variance reduction, a better grid or the right transform "
                         r"usually buys more "
                         r"than new hardware, and AAD turns a thousand Greeks into a handful of prices.",
                         color=QC.HOUSE, width=6.2, font_size=20)
        grid = VGroup(VGroup(a, b).arrange(RIGHT, buff=0.35, aligned_edge=UP),
                      VGroup(c, d).arrange(RIGHT, buff=0.35, aligned_edge=UP)).arrange(DOWN, buff=0.3)
        if grid.height > 7.2:
            grid.scale_to_fit_height(7.2)
        grid.move_to(ORIGIN)
        with self.voiceover(
            "Where does the computing happen? Every night, a bank reprices its whole book under thousands of "
            "scenarios, for risk limits, capital and the valuation adjustments of Part twenty-one, on grids of "
            "thousands of machines. Monte Carlo splits perfectly across processors, so graphics chips took over much of "
            "the work. <bookmark mark='a'/> In 2011 JPMorgan reported moving the core of its credit-derivative risk "
            "model onto programmable chips, cutting a run of eight hours or more to about four minutes. "
            "<bookmark mark='b'/> And quantum computers? Amplitude estimation needs one over epsilon samples instead "
            "of one over epsilon squared, a genuine quadratic speedup. But a 2021 study estimated that beating a "
            "classical machine on a benchmark derivative would take about eight thousand error-corrected qubits running "
            "a circuit fifty-four million layers deep in about a second, far beyond any machine yet built. "
            "<bookmark mark='c'/> The lesson of this part: the gaps between algorithms on one core are larger than "
            "the gaps between machines."
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(b, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(d, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
