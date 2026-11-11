from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, GOOD, HML, MKT, PART, ask, fit_right, illustration


class Firms(VoiceoverScene):
    def construct(self):
        self.card()
        self.dfa()
        self.aqr()
        self.etfs()
        self.longonly()
        self.costs()

    def card(self):
        c = chapter_card(12, r"The factor industry", r"What happens when research becomes a product?", lit=(1981, 1998),
                         part=PART)
        with self.voiceover("Chapter twelve. The firms that turned the factors into funds, described from the public "
                            "record."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def dfa(self):
        card = firm_card(r"Dimensional Fund Advisors",
                         r"founded in 1981 by David Booth and Rex Sinquefield to give institutions systematic access to "
                         r"small company stocks, at a time when pension portfolios held mostly large ones. It later added "
                         r"value and profitability tilts, working closely with academics including Eugene Fama and Kenneth "
                         r"French. Not an index fund in the usual sense: rules-based, but trading patiently around its "
                         r"targets", numbers=[(r"1981", r"founded"), (r"\text{small, value, profitability}", r"its tilts")],
                         source=r"the firm's public descriptions; press coverage", width=9.0, font_size=21)
        with self.voiceover(
            "The first firm built on the factors was Dimensional Fund Advisors, founded in 1981 by David Booth and Rex "
            "Sinquefield, the year Banz published the size effect. Its first purpose was to give pension funds "
            "systematic access to small companies, which institutional portfolios had mostly ignored. It later added "
            "value and profitability, working closely with Eugene Fama and Kenneth French. Its funds are rules-based "
            "but not index funds in the usual sense: they trade patiently around their targets, to keep costs down. "
            "Dimensional is the factors as a long-only, low-turnover product."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
            self.wait(1.0)
        self.clear_scene()

    def aqr(self):
        card = firm_card(r"AQR Capital Management",
                         r"founded in 1998 by Cliff Asness and colleagues from Goldman Sachs's quantitative research group. "
                         r"Runs long--short and long-only factor strategies across asset classes (value, momentum, carry, "
                         r"defensive), and publishes the data sets used in this part. Its assets were reported at about "
                         r"\$226 billion in 2018; they fell sharply through value's slump of 2018--2020, as clients withdrew",
                         numbers=[(r"1998", r"founded"), (r"\approx \$226\ \text{bn}", r"assets reported, 2018")],
                         source=r"press reports (Institutional Investor, Bloomberg); AQR's published data sets",
                         width=9.0, font_size=21)
        with self.voiceover(
            "The second is AQR Capital Management, founded in 1998 by Cliff Asness and colleagues from Goldman Sachs's "
            "quantitative group. It runs the styles of chapter seven, value, momentum, carry and defensive, across "
            "asset classes, long-short as well as long-only, and it publishes the data sets this part has used. Its "
            "assets were reported at about two hundred and twenty-six billion dollars in 2018. Then value's worst years "
            "arrived, and clients withdrew a large part of that, as Shleifer and Vishny's model of Part twenty-three "
            "predicts for any arbitrageur whose investors judge it on recent returns."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
            self.wait(1.0)
        self.clear_scene()

    def etfs(self):
        cards = VGroup(
            desk_question(r"factor indices", r"index providers publish rules for value, momentum, quality, low-volatility "
                          r"and size indices; exchange-traded funds track them, cheaply and transparently ('smart beta')",
                          width=12.0, font_size=20),
            desk_question(r"what they hold", r"long only, and usually broad: a tilt toward the factor, not the long--short "
                          r"portfolio of the papers", width=12.0, font_size=20),
            desk_question(r"what that costs", r"a published rule is a predictable trade: others can trade ahead of index "
                          r"rebalancing, a cost the fund's holders bear", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "The third is the factor exchange-traded fund. <bookmark mark='a'/> Index providers publish rules for value, "
            "momentum, quality, low volatility and size indices, and funds track them cheaply and in the open. "
            "<bookmark mark='b'/> They are long only and usually broad: a tilt toward the factor, not the long-short "
            "portfolio of the papers. <bookmark mark='c'/> And a published rule is a predictable trade. Other traders "
            "can buy before an index adds a stock and sell before it drops one, and the fund's holders pay for it."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def longonly(self):
        rows = [cmath(r"R^{\text{tilt}}", r"\approx", r"R^{m} + h\,HML,\quad h \approx 0.2\text{--}0.4", font_size=42,
                      colors={r"R^{\text{tilt}}": HML}),
                cmath(r"\text{tracking error}", r"=", r"h\,\sigma_{HML} \approx 0.3 \times 10\% = 3\%", font_size=38)]
        whys = [why(r"a long-only value fund is the market plus a fraction of the long--short factor: most of its risk is "
                    r"the market's, and the factor's premium arrives diluted. Illustrative loading"),
                why(r"so a long-only investor experiences the factor as a few percent of tracking error against the index: "
                    r"value's lost decade, for such a fund, was a decade of losing to the benchmark by a point or two a "
                    r"year")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "What does a long-only factor fund actually hold? Approximately the market, plus a fraction of the "
            "long-short factor, a fifth to two fifths for a typical value fund. <bookmark mark='a'/> Most of its risk "
            "is the market's. The factor appears as tracking error against the index, a few percent a year. Value's "
            "lost decade, for such a fund, was ten years of trailing the benchmark by a point or two a year: not a "
            "crash, but enough to lose most of its clients."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def costs(self):
        cards = VGroup(
            desk_question(r"turnover", r"value and profitability rebalance yearly; momentum monthly, turning over its "
                          r"whole portfolio several times a year. Its costs are the largest of the classic factors",
                          width=12.0, font_size=20),
            desk_question(r"measured costs", r"Frazzini, Israel and Moskowitz (2018), on AQR's own trades: real "
                          r"implementation costs were well below the academic estimates, so the factors survive costs at "
                          r"their scale. Novy-Marx and Velikov (2016): many anomalies do not", width=12.0, font_size=20),
            desk_question(r"capacity", r"the more money follows a factor, the more its trades move prices against it "
                          r"(Part 23's inelastic markets; Part 37's market impact)", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "And costs. <bookmark mark='a'/> Value and profitability rebalance once a year. Momentum rebalances every "
            "month and turns its portfolio over several times a year, so its costs are the largest. "
            "<bookmark mark='b'/> Andrea Frazzini, Ronen Israel and Tobias Moskowitz measured them on AQR's own trades "
            "and found them well below the academic estimates: the classic factors survive costs at that firm's scale. "
            "Robert Novy-Marx and Mihail Velikov found that many smaller anomalies do not. <bookmark mark='c'/> And "
            "capacity: the more money follows a factor, the more its own trades move prices against it. Part "
            "twenty-six puts costs into every backtest; Part thirty-seven measures impact."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a long-only value fund trailed its index by 1.5\% a year for ten years. Was the fund broken, the factor "
                r"broken, or neither? What would you ask the manager?")
        with self.voiceover("A long-only value fund trailed its index by one and a half percent a year for ten years. Was "
                            "the fund broken, the factor broken, or neither? What would you ask the manager?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
