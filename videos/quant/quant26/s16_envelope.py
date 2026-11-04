from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, HURDLE, IS_C, MKT, OOS_C, PART, RULE, ask, comma, illustration, load


def _years(ym):
    ym = np.asarray(ym)
    return ym // 100 + (ym % 100 - 0.5) / 12


class Envelope(VoiceoverScene):
    def construct(self):
        e = load("envelope")
        self.card()
        self.register(e)
        self.opened(e)
        self.eras(e, load("rules"))
        self.meaning(e)
        self.question()

    def card(self):
        c = chapter_card(15, r"The best rule, registered and opened", r"What did 2021--2025 say?", lit=(2021,), part=PART)
        with self.voiceover("Chapter fifteen. The best of the ten thousand rules, registered with its trial count, and "
                            "opened once on the sealed years."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def register(self, e):
        card = firm_card(r"stw\_best\_rule\_part26", r"long when the US market closes above its five-day average, short "
                         r"when below; chosen as the best Sharpe ratio of 10{,}000 rules on 1926--1986; returns are the "
                         r"position at the close times the next day's market return over T-bills",
                         numbers=((r"10{,}000", r"configurations tried"), (r"\texttt{sha256}", r"of the rule engine's code")),
                         source=r"videos/quant/data/envelope.json", kind=r"Registered strategy", width=8.6, font_size=22)
        card.to_edge(UP, buff=0.5)
        before, after = e["trials"] - e["n_trials"], e["trials"]
        cnt = DecimalNumber(before, num_decimal_places=0, group_with_commas=True, font_size=56, color=QC.HOUSE)
        lab = label(r"the House's trial counter", font_size=22, color=GREY_A)
        g = VGroup(lab, cnt).arrange(DOWN, buff=0.15).next_to(card, DOWN, buff=0.5)
        with self.voiceover(
            "The rule is registered like every House strategy: the hash of the code that runs it, its parameters, and "
            "the number of configurations tried to find it, ten thousand. <bookmark mark='a'/> The trial counter, which "
            "stood at three hundred and forty-six, jumps to ten thousand three hundred and forty-six. Every later "
            "claim in the series is now judged against that count. It is the price of having looked."
        ) as vo:
            self.play(FadeIn(card), FadeIn(g))
            vo.wait_until("a")
            self.play(ChangeDecimalToValue(cnt, after), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def opened(self, e):
        x = _years(e["ym"])
        ye, ym = np.log10(np.asarray(e["eq"])), np.log10(np.asarray(e["mkt"]))
        lo, hi = float(min(ye.min(), ym.min()) - 0.05), float(max(ye.max(), ym.max()) + 0.05)
        g = axes([2021, 2026], [lo, hi], x_length=7.6, y_length=4.2, xlabel=r"the sealed years",
                 ylabel=r"growth of \$1, $\log_{10}$ (excess of T-bills)", xticks=[2021, 2022, 2023, 2024, 2025, 2026],
                 yticks=[t for t in (-0.2, 0, 0.2, 0.4) if lo <= t <= hi], font_size=14).to_edge(LEFT, buff=0.5)
        g.shift(DOWN * 0.3)
        ax = g.ax
        lr, lm = curve(ax, x, ye, RULE, stroke_width=3), curve(ax, x, ym, MKT, stroke_width=2.5)
        side = VGroup(
            MathTex(rf"\text{{the rule}}:\ {e['sr_hold']:+.2f} \pm {e['se_hold']:.2f}", font_size=28, color=RULE),
            MathTex(rf"\text{{the market}}:\ {e['sr_bh_hold']:.2f}", font_size=28, color=MKT),
            MathTex(rf"\text{{short}}\ {100 * e['short']:.0f}\%\ \text{{of days}}", font_size=22, color=GREY_A),
            wrapped_label(rf"Sharpe ratios, {e['first'] // 10000}--{e['last'] // 10000}, opened once; the rule's "
                          r"standard error is chapter 5's, for five years of daily returns", 3.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "And the envelope is opened. <bookmark mark='a'/> From 2021 to 2025, the rule that was the best of ten "
            "thousand before 1987 lost money: a Sharpe ratio of minus point two seven, give or take point four five. "
            "It was short four days in ten, through a five-year period in which the market itself earned a Sharpe "
            "ratio of point six."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(lm), Create(lr), FadeIn(side), run_time=3)
        self.add(illustration(r"Ken French daily factors, 2021--2025 (sealed); \texttt{pit.open\_envelope}"))
        self.wait(0.4)
        self.clear_scene()

    def eras(self, e, r):
        items = [(r"1926--1986", e["sr_in"], r["eras"]["in"]["sr_bh"], IS_C),
                 (r"1987--2020", e["sr_out"], r["eras"]["out"]["sr_bh"], OOS_C),
                 (r"2021--2025", e["sr_hold"], e["sr_bh_hold"], HURDLE)]
        g = VGroup()
        for i, (nm, v, m, col) in enumerate(items):
            y = 1.4 - 1.1 * i
            b = Rectangle(width=abs(v) * 3.0, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([v * 1.5, y + 0.12, 0])
            bm = Rectangle(width=abs(m) * 3.0, height=0.22, stroke_width=0, fill_color=MKT, fill_opacity=0.6)
            bm.move_to([m * 1.5, y - 0.25, 0])
            g.add(VGroup(label(nm, font_size=22, color=col).move_to([-4.8, y, 0]), b, bm,
                         MathTex(f"{v:+.2f}", font_size=26).next_to(b, RIGHT if v > 0 else LEFT, buff=0.15),
                         MathTex(f"{m:.2f}", font_size=18, color=MKT).next_to(bm, RIGHT, buff=0.12)))
        axis = Line([0, 2.0, 0], [0, -1.5, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"the same rule's Sharpe ratio in three eras; thin: the market's", font_size=26).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"chosen in the first era, flat in the second, negative in the third. The deflated Sharpe "
                             r"ratio and the reality check passed it in 1986, and were right about 1926--1986", 12.0, 19,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "One rule, three eras. <bookmark mark='a'/> One point six seven when it was chosen. Two hundredths for the "
            "next thirty-four years. Minus point two seven in the five sealed years. <bookmark mark='b'/> The "
            "statistical tests passed it in 1986, and they were right: about 1926 to 1986. What they could not know is "
            "whether the world that produced that history would continue. It did not."
        ) as vo:
            self.play(FadeIn(head), Create(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in g], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def meaning(self, e):
        cards = VGroup(
            desk_question(r"five years cannot convict it", rf"$-0.27 \pm {e['se_hold']:.2f}$ is consistent with a "
                          r"Sharpe ratio of zero, or even of a modest positive one: chapter 5's arithmetic applies to "
                          r"failures too", width=12.2, font_size=20),
            desk_question(r"but thirty-nine years can", r"1987--2025 together: a rule chosen for an edge that was in the "
                          r"data, and was not tradable, and then was not there", width=12.2, font_size=20),
            desk_question(r"it stays in the record", r"the House keeps the opened envelope and the count, so that no later "
                          r"part can quietly try the same rules again and call it a first look", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the result does and does not say. <bookmark mark='a'/> Five years cannot convict the rule on their own: "
            "minus point two seven, give or take point four five, is consistent with zero, or even with a small "
            "positive Sharpe ratio. <bookmark mark='b'/> But the thirty-nine years from 1987 can. <bookmark mark='c'/> "
            "And the record stays: the opened envelope and the count are kept, so that no later part can quietly try "
            "the same rules again and call it a first look."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"the same rule, run on S\&P 500 futures instead of the index, from 1982 (when they began trading) to "
                r"1986. Would you expect its Sharpe ratio to be closer to 1.67 or to 0? Why?")
        with self.voiceover(
            "Pause and predict. Run the same rule on S and P five hundred futures instead of the index, from 1982, when "
            "they began trading, to 1986. Would you expect its Sharpe ratio to be closer to one point six seven, or to "
            "zero? Why?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
