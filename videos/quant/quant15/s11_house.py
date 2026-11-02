from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)

    def card(self):
        c = chapter_card(10, r"The exotics pricer", r"What must the desk know before it sells a note?", part=PART)
        with self.voiceover("Chapter ten. The exotics pricer."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("vol",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{down\_out\_call}, \texttt{down\_in\_put}, \texttt{bgk\_barrier}", r"barriers, watched as the term sheet says"),
            (r"\texttt{digital\_call}, \texttt{call\_spread\_digital}", r"the digital, and the hedge the desk can run"),
            (r"\texttt{geometric\_asian\_call}, \texttt{lookback\_floating\_call}", r"closed forms, and control variates"),
            (r"\texttt{snowball\_price}, \texttt{fair\_coupon}", r"the snowball by Monte Carlo"),
            (r"\texttt{worst\_of\_put}", r"correlation risk"),
            (r"\texttt{uvm\_price}", r"the price of not knowing the volatility"),
            (r"the snowball surrogate", r"the whole book in microseconds"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=19, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.0)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 15: before a note is sold, the desk prices it under at least two models, holds a reserve "
                             r"for the gap, and simulates its hedge through the worst path on record for the underlying, "
                             r"including what the hedge must trade on the barrier day.  "
                             rf"The trial counter still reads {env['trials']}.", 12.4, 22, QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The volatility desk now has its exotics pricer. <bookmark mark='a'/> Barriers watched the way the term "
            "sheet watches them. Digitals, and the call spreads that hedge them. Closed forms and control variates for "
            "averages and lookbacks. The snowball, its fair coupon, and the network that reprices a book of them. "
            "Correlation, and the price of not knowing the volatility. <bookmark mark='b'/> The fifteenth rule: before "
            "a note is sold, the desk prices it under at least two models, holds a reserve for the gap, and simulates "
            "its hedge through the worst path on record, including what the hedge must trade on the day a barrier "
            f"breaks. No strategy was tested, and the counter still reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
