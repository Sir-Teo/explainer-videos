from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import LOSS, P_C, PART, load, real_data


class Barings(VoiceoverScene):
    def construct(self):
        n = load("nikkei")
        self.card()
        self.file()
        self.chart(n)

    def card(self):
        c = chapter_card(4, r"Doubling down: Barings, 1995", r"What happens when the bankroll is someone else's?",
                         lit=(1995,), part=PART)
        with self.voiceover("Chapter four. Doubling down: Barings, 1995."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def file(self):
        card = crisis_card(r"26 February 1995", r"Barings",
                           r"Britain's oldest merchant bank, founded in 1762, failed after its Singapore derivatives "
                           r"trader, Nick Leeson, lost about \pounds 830 million on Nikkei futures and options. The losses "
                           r"had been hidden since 1992 in error account 88888. ING bought the bank for one pound.",
                           stats=[(r"\approx \pounds 830\text{m}", r"the loss, more than the bank's capital"),
                                  (r"88888", r"the error account that hid it"), (r"233", r"years old")],
                           width=10.6, font_size=27)
        card.move_to(ORIGIN)
        with self.voiceover(
            "In February 1995 the doubling system broke a bank. Barings, Britain's oldest merchant bank, founded in "
            "1762, failed after a single trader in Singapore, Nick Leeson, lost about eight hundred and thirty "
            "million pounds, more than the bank's entire capital. Since 1992 he had hidden his losses in an error "
            "account numbered eight eight eight eight eight. The Dutch bank ING bought what was left for one pound. "
            "Leeson was arrested in Frankfurt and sentenced in Singapore to six and a half years in prison."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def chart(self, n):
        t, v = np.asarray(n["t"]), np.asarray(n["value"])
        g = axes([1994.5, 1995.25], [15000, 21500], x_length=8.2, y_length=4.6, ylabel=r"Nikkei 225",
                 xticks=[1994.5, 1994.75, 1995.0, 1995.25], xfmt=lambda x: {1994.5: "Jul 94", 1994.75: "Oct 94",
                                                                             1995.0: "Jan 95", 1995.25: "Apr 95"}[x],
                 yticks=[15000, 17000, 19000, 21000], yfmt=lambda u: f"{int(u):,}".replace(",", "{,}"), font_size=18)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, v, P_C, stroke_width=3)
        kobe_t = 1995 + 16 / 365
        kobe = DashedLine(ax.c2p(kobe_t, 15000), ax.c2p(kobe_t, 21500), color=LOSS, stroke_width=2)
        kl = label(r"Kobe earthquake, 17 Jan.", font_size=19, color=LOSS).next_to(ax.c2p(kobe_t, 21300), LEFT, buff=0.1)
        bar_t = 1995 + 56 / 365
        fall = DashedLine(ax.c2p(bar_t, 15000), ax.c2p(bar_t, 21500), color=QC.CRISIS, stroke_width=2)
        fl = label(r"Barings fails, 26 Feb.", font_size=19, color=QC.CRISIS).next_to(ax.c2p(bar_t, 15300), LEFT, buff=0.1)
        p = n["pick"]
        side = VGroup(
            MathTex(rf"\text{{13 Jan.: }} {p['19950113']:,.0f}".replace(",", "{,}"), font_size=28),
            MathTex(rf"\text{{23 Jan.: }} {p['19950123']:,.0f}\ ({100 * (p['19950123'] / p['19950113'] - 1):.0f}\%)".replace(",", "{,}"),
                    font_size=28, color=LOSS),
            MathTex(rf"\text{{27 Feb.: }} {p['19950227']:,.0f}\ ({100 * (p['19950227'] / p['19950113'] - 1):.0f}\%)".replace(",", "{,}"),
                    font_size=28, color=LOSS),
            wrapped_label(r"long Nikkei futures and short options that paid if the index stayed calm near 19,000; as it "
                          r"fell he bought more, doubling down to win it back", 4.4, 21, GREY_A),
            wrapped_label(r"a doubling system needs an endless bankroll; a hidden account let him borrow the bank's", 4.4,
                          21, LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        src = real_data(r"FRED: Nikkei 225 daily close (NIKKEI225); facts from the public record")
        with self.voiceover(
            "Here is the Nikkei through those months. Leeson was long Nikkei futures, and had sold options that paid "
            "him as long as the index stayed calm, near nineteen thousand. <bookmark mark='a'/> On the seventeenth "
            "of January an earthquake struck Kobe. Within a week the index had fallen eight percent. "
            "<bookmark mark='b'/> He did what the doubling system prescribes: as the market fell, he bought more, "
            "to win everything back on the rebound. The rebound did not come. <bookmark mark='c'/> A doubling system "
            "needs an endless bankroll and no limit on its bets. The hidden account gave Leeson both, until the "
            "bankroll he was really using, the bank's capital, ran out. On the twenty-sixth of February Barings "
            "failed, and the next day the Nikkei fell again. Optional stopping was not repealed; the bank's risk "
            "controls had simply allowed the one strategy the theorem excludes."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(line), run_time=2.5)
            self.play(FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(kobe), FadeIn(kl), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(fall), FadeIn(fl), FadeIn(side[2]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()
