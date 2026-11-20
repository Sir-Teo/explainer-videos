from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ forecasting inflation, \ bargaining over wages", r"How do forecasters and "
             r"negotiators use all this?", "Chapter fifteen. In practice: forecasting inflation, bargaining over "
             "wages.", lit={1967: r"Friedman", 2012: r"the Fed's 2\%"}, scale=("firm", "nation"),
             horizon=("a quarter", "a year"))
        self.persist()
        self.called()
        self.desk()

    def persist(self):
        P = load("persistence")
        f = next(x for x in facts.FACTS if x.key == "persistence")
        data_m = label(rf"US CPI, \ annual: \ this year on last, \\ correlation {P['all']:.2f}; \\ 1960--83: \ "
                       rf"{P['1960_1983']:.2f}; \ 1984--2019: \ {P['1984_2019']:.2f}", font_size=18, color=WHITE)
        theory_m = label(r"contracts, \ indexation \\ and expectations \\ carry it forward", font_size=19,
                         color=EXPECT)
        agora_m = label(r"Part 30 builds it: \\ prices set in advance, \\ a few at a time", font_size=19,
                        color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, EXPECT, None)).move_to(UP * 0.3)
        tag = data_tag(r"BLS: \ the CPI, \ via FRED; \ this film's correlations", corner=DR, font_size=12)
        with self.voiceover(
            "A forecaster starts from one of the series' facts: inflation is persistent. <bookmark mark='a'/> In "
            "American data, this year's inflation and last year's have a correlation of "
            f"{P['all']:.2f}. It was {P['1960_1983']:.2f} before 1984, and {P['1984_2019']:.2f} afterwards, once "
            "the anchor took hold. <bookmark mark='b'/> In theory, persistence comes from contracts that last a "
            "while, from pay and prices indexed to past inflation, and from expectations that look back. "
            "<bookmark mark='c'/> Agora's column waits for Part thirty, which builds prices that are set in advance, "
            "a few at a time."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1][2:]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2][2:]))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["friedman_1967"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=19).move_to(UP * 0.1)
        tag = published_tag(r"Friedman, \ AER 58(1) (1968); \ BLS via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "And the forecast this part began with. Called it? <bookmark mark='a'/> In December 1967, Friedman "
            "said there was no permanent trade-off: holding unemployment below its natural rate would take ever "
            "faster inflation. <bookmark mark='b'/> In the decade that followed, inflation and unemployment both "
            "rose, from five and three and a half percent in 1969 to nine and eight and a half in 1975, and the "
            "stable curve of the 1960s vanished. <bookmark mark='c'/> Right. It is one of the few forecasts in "
            "economics that changed the textbooks as well as the policy."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()

    def desk(self):
        rows = VGroup(
            label(r"the forecaster's toolkit", font_size=27, color=E.ACCENT),
            label(r"core inflation as the trend; \ energy and food as shocks that pass", font_size=22, color=WAGE),
            label(r"expectations from surveys and from bond markets", font_size=22, color=EXPECT),
            label(r"slack from unemployment, \ or openings per unemployed person", font_size=22, color=UNEMP),
            label(r"at the bargaining table: \ wage deals that build in expected inflation, \ and cost-of-living "
                  r"clauses that index to past inflation", font_size=21, color=CB),
            label(r"indexation spreads in high inflation, \ and makes it harder to stop", font_size=22, color=INFL),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "The working forecaster's toolkit follows from this part. <bookmark mark='a'/> Core inflation as the "
            "trend, with energy and food treated as shocks that usually pass. <bookmark mark='b'/> Expectations, "
            "from surveys of households and firms and from bond markets. <bookmark mark='c'/> Slack, from "
            "unemployment against its natural rate, or from openings per unemployed person. "
            "<bookmark mark='d'/> And at the bargaining table, wage deals build in the inflation both sides expect, "
            "and some include cost-of-living clauses that raise pay with past inflation. "
            "<bookmark mark='e'/> Those clauses spread when inflation is high, as they did in the 1970s, and make it "
            "harder to bring down."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
