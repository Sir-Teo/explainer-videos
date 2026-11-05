from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C, load)


class Open(VoiceoverScene):
    def construct(self):
        self.card()
        self.page1()
        self.page2()
        self.page3()
        self.settled()
        self.limits()
        self.method()
        self.question()

    def card(self):
        c = chapter_card(7, r"What we still do not know", r"Which questions has the series left open?", part=PART)
        with self.voiceover(
            "Chapter seven, and the answer to the pause, or eight of them. Each part ended with open problems; these "
            "are the ones that kept returning, across the whole series, in markets, in models, and in the tools used "
            "to study them."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def page1(self):
        cards = VGroup(
            desk_question(r"1. the equity premium (Part 23)", r"why stocks have paid so much more than bonds, for so long, with consumption so smooth; no model fits it without strong assumptions", width=12.4, font_size=19),
            desk_question(r"2. rough volatility (Part 14)", r"whether volatility is truly rough, or rough-looking at the scales we measure; what that means for hedging", width=12.4, font_size=19),
            desk_question(r"3. the factor zoo's dimension (Parts 24--25)", r"how many independent sources of expected return there are: five, twenty, or a few hundred weak ones", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "In markets. <bookmark mark='a'/> The equity premium: why stocks have paid so much more than bonds, for so "
            "long, with consumption so smooth, a puzzle no model resolves without strong assumptions. "
            "<bookmark mark='b'/> Rough volatility: whether volatility is truly rough, or only looks so at the scales we "
            "can measure, and what that means for hedging. <bookmark mark='c'/> And the dimension of the factor zoo: "
            "how many independent sources of expected return there really are, five, twenty, or hundreds of weak ones."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def page2(self):
        cards = VGroup(
            desk_question(r"4. learning at low signal-to-noise (Parts 27, 29)", r"when flexible models beat linear ones on returns whose predictable part is one percent of their variance, and how to know before the hold-out", width=12.4, font_size=19),
            desk_question(r"5. language models and look-ahead (Parts 28, 42)", r"honest tests of models that have read the future; chronologically consistent training at scale", width=12.4, font_size=19),
            desk_question(r"6. machines and stability (Parts 41--42)", r"herding, collusion and correlated errors when many traders share models; how to measure model monoculture", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "In models. <bookmark mark='a'/> Learning when the signal is tiny: when flexible models beat linear ones on "
            "returns whose predictable part is one percent of their variance, and how to know before the hold-out. "
            "<bookmark mark='b'/> Honest tests of language models that have read the future, and models trained, at "
            "scale, only on what was known at each date. <bookmark mark='c'/> And what machines that share models do "
            "to the stability of the market they trade in, and how to measure it."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def page3(self):
        cards = VGroup(
            desk_question(r"7. Treasury market plumbing (Parts 18, 41)", r"how the world's safe asset can be made liquid in a panic: dealer balance sheets, central clearing, the basis trade", width=12.4, font_size=19),
            desk_question(r"8. climate risk", r"how physical and transition risks are priced, when the data are short and the horizon is long; this series did not cover it, which is itself an open problem", width=12.4, font_size=19),
            desk_question(r"and the method itself", r"how to do research when every test spends a little of the data's honesty: the envelope and the counter are one answer, not the last", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "In the system, and in the method. <bookmark mark='a'/> How the safest asset can be made liquid in a panic: "
            "dealer balance sheets, central clearing and the basis trade. <bookmark mark='b'/> Climate risk, priced on "
            "short data over long horizons, which this series did not cover, and that is an open problem in itself. "
            "<bookmark mark='c'/> And research itself: every test spends a little of the data's honesty, and the "
            "House's envelope and counter are one answer, not the last."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def settled(self):
        cards = VGroup(
            desk_question(r"settled: normal VaR fails", r"Part 40: a normal VaR on ninety years of the US market was "
                          r"exceeded on 2.24\% of days, in clusters; a GARCH-filtered one passed", width=12.4, font_size=19),
            desk_question(r"settled: learners can collude", r"Part 42 reproduced Calvano and coauthors: Q-learners reach "
                          r"81\% of the way to monopoly profits, and punish", width=12.4, font_size=19),
            desk_question(r"settled: a backtest is not a forecast", r"the Track Record: research Sharpe ratios shrink, "
                          r"by about half above the average, when the envelope opens", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And three things the series did settle, at least for its own data. <bookmark mark='a'/> A normal VaR fails: "
            "on ninety years of the American market it was exceeded far more often than promised, in clusters. "
            "<bookmark mark='b'/> Learning algorithms can collude without speaking. <bookmark mark='c'/> And a backtest "
            "is not a forecast: research Sharpe ratios shrink when the envelope opens."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        cards = VGroup(
            desk_question(r"not tested: real fund records", r"Chapters 2 and 3 used a simulated population, where the "
                          r"truth is known; fund-level databases are licensed", width=12.4, font_size=19),
            desk_question(r"not tested: other surfaces", r"one Bitcoin options surface, on one day, with the next day "
                          r"kept for checks; equity and rates surfaces may rank models differently", width=12.4,
                          font_size=19),
            desk_question(r"not tested: a long hold-out", r"five sealed years, so most rows cannot be told apart from "
                          r"their research values or from zero", width=12.4, font_size=19),
            desk_question(r"not tested: language models as traders", r"no downloaded model was run; Part 42 explains "
                          r"what an honest test would need", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "And, just as honestly, what the series could not test. <bookmark mark='a'/> Real fund records: the "
            "databases of fund returns are licensed, so the counting of skill was checked on a simulated population, "
            "where the truth is known, and not on real funds. <bookmark mark='b'/> Other surfaces: one Bitcoin options "
            "surface on one day ranks models for that market, not for every market. <bookmark mark='c'/> A long "
            "hold-out: five sealed years cannot separate most strategies from their research values, or from zero. "
            "<bookmark mark='d'/> And language models as traders, which the series discussed but did not run. Each "
            "is a place where the next version of this course should start."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def method(self):
        rows = [cmath(r"\text{question}", r"\to", r"\text{model} \to \text{proof} \to \text{data}", font_size=40,
                      colors={r"\text{question}": QC.IDEA}),
                cmath(r"\text{data}", r":", r"\text{point in time, research window, sealed hold-out}", font_size=36),
                cmath(r"\text{every trial}", r":", r"\text{counted, and the count reported}", font_size=38,
                      colors={r"\text{every trial}": REC_C})]
        whys = [why(r"the shape of every part: a question, a model, a theorem proved, then checked by simulation or "
                    r"data"),
                why(r"Rule 1, kept for forty-three parts: nothing is known before it was known"),
                why(r"and the result shown whatever it says: the Track Record's one virtue")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And the method the series used on all of them. <bookmark mark='a'/> A question, a model, a theorem proved, "
            "and then a check, by simulation or by data. <bookmark mark='b'/> Data used as of the date it was known, "
            "with a research window and a sealed hold-out. <bookmark mark='c'/> And every trial counted, and the "
            "result shown, whatever it said."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"in 1900 Louis Bachelier modelled prices as a random walk that could go negative. When did a "
                       r"major exchange switch to his model, and why?")
        with self.voiceover(
            "Pause and predict. In nineteen hundred Louis Bachelier modelled prices as a random walk that could go "
            "below zero. When did a major exchange switch to his model, and why?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
