from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Labour(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Labour markets", r"Can a merger lower wages \ without raising any price?",
             "Chapter eleven. Labour markets.", lit={2016: r"no-poach clauses", 2021: r"Prager and Schmitt",
                                                     2023: r"Guideline 10"},
             scale=("person", "firm", "city"), horizon=("a year",))
        self.hospitals()
        self.evidence()

    def hospitals(self):
        L = load("labour")
        ax = plane([-0.6, 2.6], [0, 45], center=LEFT * 2.8 + DOWN * 0.5, x_length=6.0, y_length=4.6, xticks=[],
                   yticks=[0, 10, 20, 30, 40], ylabel=r"\$ an hour", yfmt=lambda v: f"{v:.0f}", font_size=15)
        mrp = 40.0
        vals = [mrp, L["before"][0], L["after"][0]]
        cols = (WHITE, WORK, CARTEL)
        names = (r"what a nurse's \\ hour is worth", r"the wage, \\ two employers", r"the wage, \\ one employer")
        bars, labs, vl = VGroup(), VGroup(), VGroup()
        for k, (v, c, n) in enumerate(zip(vals, cols, names)):
            p0, p1 = ax.ax.c2p(k - 0.3, 0), ax.ax.c2p(k + 0.3, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=c,
                               fill_opacity=0.35 if k == 0 else 0.85, stroke_width=0).move_to((p0 + p1) / 2))
            labs.add(label(n, font_size=15, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.15))
            vl.add(label(f"{v:.2f}", font_size=17, color=c).next_to(bars[-1], UP, buff=0.06))
        top = DashedLine(ax.ax.c2p(-0.6, mrp), ax.ax.c2p(2.6, mrp), color=GREY_B, stroke_width=1.4)
        side = VGroup(
            label(r"nurses choose among two hospitals and other work, \\ by logit in the wage", font_size=19,
                  color=GREY_A),
            label(rf"the markdown: \ {L['markdown_before']:.0f}\% of the value of the work", font_size=21,
                  color=WORK),
            label(rf"after the merger: \ {L['markdown_after']:.0f}\%; \ wages {L['fall']:.1f}\%"
                  .replace("-", "{-}"), font_size=21, color=CARTEL),
            label(r"a nurse who leaves one hospital for the other \\ no longer leaves the employer", font_size=19,
                  color=GREY_B),
            label(r"no patient's price need change: \ the harm is in the labour market", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ a town with two hospitals; \ agora.merger.labour\_merger", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Mergers also join employers. Part thirty-eight showed how an employer with few rivals for its workers "
            "pays them less than their work is worth. <bookmark mark='a'/> In an Island town, nurses choose between "
            "two hospitals and other work, by a logit in the wage. <bookmark mark='b'/> Each hospital pays "
            f"{L['before'][0]:.2f} dollars an hour for work worth forty: a markdown of {L['markdown_before']:.0f} "
            "percent, because a hospital that raised its wage would also pay the higher wage to every nurse it "
            f"already has. <bookmark mark='c'/> The hospitals merge. Wages fall to {L['after'][0]:.2f}, by "
            f"{say_num(-L['fall'], 1)} percent, and the markdown widens to {L['markdown_after']:.0f}. <bookmark "
            "mark='d'/> It is the diversion argument again, on the other side of the market: a nurse who quits one "
            "hospital for the other no longer leaves the employer. <bookmark mark='e'/> No patient's price need "
            "change at all. A review that looks only at what buyers pay would miss this harm entirely."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(labs), Create(top))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(vl[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(vl[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(vl[2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def evidence(self):
        cards = VGroup(
            history_card(2021, r"Elena Prager and Matt Schmitt", r"after the quarter of hospital mergers that raised "
                         r"employer concentration most, \ wage growth slowed by about 1.7 points a year for nurses "
                         r"and pharmacy workers, \ 1.1 for other skilled workers; \ not for the unskilled",
                         color=WORK, width=11.6, font_size=19),
            history_card(2016, r"no-poach clauses", r"Alan Krueger and Orley Ashenfelter: \ 58\% of major "
                         r"franchisors' contracts barred one franchisee from hiring another's workers; \ after the "
                         r"paper, \ state attorneys general made many drop them", color=CARTEL, width=11.6,
                         font_size=19),
            history_card(2023, r"the Merger Guidelines, \ Guideline 10", r"mergers that may substantially lessen "
                         r"competition for workers are judged like those that harm buyers", color=GOV, width=11.6,
                         font_size=19),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        tag = published_tag(r"Prager and Schmitt, AER (2021), as summarized by Kellogg Insight; \ Krueger and "
                            r"Ashenfelter, JHR (2022); \ the 2023 Merger Guidelines", corner=DL, font_size=12)
        with self.voiceover(
            "Is it real? <bookmark mark='a'/> Elena Prager and Matt Schmitt studied American hospital mergers. "
            "After the quarter of mergers that raised employer concentration most, wage growth slowed by about "
            "1.7 percentage points a year for nurses and pharmacy workers, and 1.1 for other skilled workers, "
            "whose skills are worth most in hospitals; for unskilled workers, who can work anywhere, they found no "
            "effect. <bookmark mark='b'/> Employers can also simply agree not to compete for workers. Alan Krueger "
            "and Orley Ashenfelter read the 2016 franchise contracts of America's big chains and found that 58 "
            "percent barred one franchisee from hiring another's workers. After their paper circulated, state "
            "attorneys general pressed many chains to drop the clauses, and the federal agencies had already "
            "warned that naked no-poach agreements could be prosecuted as crimes. <bookmark mark='c'/> In 2023 "
            "the merger guidelines gave labour markets a guideline of their own. The tools are the same as for "
            "buyers: a market, shares, diversion, now measured in workers who would switch employers."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
        self.clear_scene()
