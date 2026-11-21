from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403

YES = r"$\checkmark$"
NO = r"$\times$"


class Evidence(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The evidence", r"What do the three best designs identify, \ and do they transfer?",
             "Chapter seven. The evidence.", lit={2016: r"Aizer et al.", 2021: r"Corinth et al.",
                                                  2022: r"Ananat et al.", 2023: r"Baker et al."},
             scale=("household", "nation"), horizon=("a year", "a century"))
        self.work()
        self.long_run()
        self.counter()
        self.transfer()

    def work(self):
        T = tables.CTC_2021.data
        A = tables.ALLOWANCE_50.data
        c1 = study_card(r"America's monthly payments, \ 2021", r"Ananat, Glasner, Hamilton and Parolin (2022)",
                        [(r"varied", r"monthly payments to most families with children, \ July to December 2021"),
                         (r"compared", r"parents with and without children, \ before and after"),
                         (r"found", rf"child poverty (SPM) {T['spm_2020']}\% $\to$ {T['spm_2021']}\%; \ work: \ "
                                    r"effects very small, \ of either sign, \ insignificant")],
                        design="DiD", width=6.3, font_size=19)
        c2 = study_card(r"Canada's Child Benefit, \ 2016", r"Baker, Messacar and Stabile (2023)",
                        [(r"varied", r"a larger, \ income-tested, \ permanent benefit"),
                         (r"compared", r"families by how much their benefit rose"),
                         (r"found", rf"poverty about {A['ccb_single']}\% lower for single mothers, \ "
                                    rf"{A['ccb_two']}\% for couples, \ by 2018; \ no sign of less work")],
                        design="DiD", width=6.3, font_size=19)
        VGroup(c1, c2).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.2)
        head = label(r"poverty and work", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.45)
        tag = published_tag(r"Ananat et al., \ NBER WP 29823 (2022); \ Baker, Messacar and Stabile, \ JOLE (2023)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The evidence. A memo should rest on the best few designs, each with what it identifies, and an "
            "honest word on whether it transfers to the case at hand. On poverty and work, two. <bookmark "
            "mark='a'/> First, America's own monthly payments of 2021. Elizabeth Ananat and her co-authors "
            "compared parents, who received them, with adults without children, who did not, before and after "
            "July. <bookmark mark='b'/> They found employment effects very small, of either sign, and "
            "statistically insignificant, including for parents in the range where the old credit had rewarded "
            "work. <bookmark mark='c'/> Second, Canada's Child Benefit of 2016, larger and permanent. Michael Baker, "
            "Derek Messacar and Mark Stabile compared families by how much their benefit rose. <bookmark "
            f"mark='d'/> By 2018 poverty was about {A['ccb_single']} percent lower among single mothers and "
            f"{A['ccb_two']} percent lower among couples, with no sign that parents worked less, on either margin."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(c1.card), FadeIn(c1.head), FadeIn(c1.body[:2]), *[FadeIn(m) for m in c1[2:]])
            vo.wait_until("b")
            self.play(FadeIn(c1.body[2]))
            vo.wait_until("c")
            self.play(FadeIn(c2.card), FadeIn(c2.head), FadeIn(c2.body[:2]), *[FadeIn(m) for m in c2[2:]])
            vo.wait_until("d")
            self.play(FadeIn(c2.body[2]))
        self.clear_scene()

    def long_run(self):
        A = tables.ALLOWANCE_50.data
        c1 = study_card(r"Mothers' Pensions, \ 1911--1935", r"Aizer, Eli, Ferrie and Lleras-Muney (2016)",
                        [(r"varied", r"cash to poor mothers: \ some applicants accepted, \ some turned down"),
                         (r"compared", rf"{A['boys']:,} sons of accepted and rejected mothers".replace(",", "{,}")),
                         (r"found", r"about a year longer life, \ a third of a year more school, \ higher adult "
                                    r"income")],
                        design="regression", width=6.3, font_size=19)
        c2 = study_card(r"Canada's child benefits", r"Milligan and Stabile (2011)",
                        [(r"varied", r"benefits that differed across provinces, \ years and family types"),
                         (r"compared", r"children by the benefit their family could get"),
                         (r"found", r"higher test scores; \ better maternal health and mental health")],
                        design="IV", width=6.3, font_size=19)
        VGroup(c1, c2).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.2)
        head = label(r"the long run", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.45)
        caveat = label(r"the long run is where the value lies, \ and where the evidence is oldest and thinnest",
                       font_size=20, color=HOLD).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Aizer et al., \ AER (2016); \ Milligan and Stabile, \ AEJ: Policy (2011)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "The long run needs a different kind of evidence, because it takes a generation to arrive. <bookmark "
            "mark='a'/> Anna Aizer and her co-authors found the files of America's first welfare programme, the "
            "Mothers' Pensions of 1911 to 1935, and compared the sons of mothers who were accepted with the sons "
            f"of mothers who applied and were turned down, {A['boys']:,} boys in all. <bookmark mark='b'/> The sons "
            "of accepted mothers lived about a year longer, had a third of a year more schooling, and earned more "
            "as adults. <bookmark mark='c'/> Kevin Milligan and Mark Stabile used Canadian benefits that differed "
            "across provinces, years and family types. <bookmark mark='d'/> Children whose families could get more "
            "had higher test scores, and their mothers better health and mental health. <bookmark mark='e'/> This "
            "is where most of an allowance's value may lie, and it is where the evidence is oldest, most "
            "indirect and thinnest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(c1.card), FadeIn(c1.head), FadeIn(c1.body[:2]), *[FadeIn(m) for m in c1[2:]])
            vo.wait_until("b")
            self.play(FadeIn(c1.body[2]))
            vo.wait_until("c")
            self.play(FadeIn(c2.card), FadeIn(c2.head), FadeIn(c2.body[:2]), *[FadeIn(m) for m in c2[2:]])
            vo.wait_until("d")
            self.play(FadeIn(c2.body[2]))
            vo.wait_until("e")
            self.play(FadeIn(caveat, shift=UP * 0.1))
        self.clear_scene()

    def counter(self):
        A = tables.ALLOWANCE_50.data
        c = study_card(r"A permanent American allowance, \ simulated", r"Corinth, Meyer, Stadnicki and Wu (2021)",
                       [(r"assumed", r"participation elasticities from the mainstream of the literature, \ applied "
                                     r"to the end of the phase-in and to the added income"),
                        (r"found", rf"about {A['exits']} million working parents ({A['exit_share']}\%) leave work; "
                                   rf"\ child poverty falls by at most {A['max_cut']}\%")],
                       design="calibration", width=9.4, font_size=20).move_to(UP * 0.6)
        why = VGroup(
            label(r"not a measurement: \ a model with borrowed elasticities", font_size=21, color=GREY_A),
            label(r"but it asks the right question: \ what would a permanent policy do?", font_size=21,
                  color=WHITE),
        ).arrange(DOWN, buff=0.25).next_to(c, DOWN, buff=0.5)
        tag = published_tag(r"Corinth et al., \ NBER WP 29366 (2021)", corner=DR, font_size=12)
        with self.voiceover(
            "And a counterpoint the memo must answer, not ignore. <bookmark mark='a'/> In 2021 Kevin Corinth, "
            "Bruce Meyer, Matthew Stadnicki and Derek Wu simulated a permanent American allowance, with "
            "participation elasticities from the mainstream of the labour literature, applied to the end of the "
            f"phase-in and to the income the allowance adds. <bookmark mark='b'/> About {A['exits']} million "
            f"working parents, {A['exit_share']} percent, would leave work, and child poverty would fall by at most "
            f"{A['max_cut']} percent, not by the half that the static arithmetic suggests. <bookmark mark='c'/> "
            "This is not a measurement: it is a model, with elasticities borrowed from other settings. <bookmark "
            "mark='d'/> But it asks the right question, the one the 2021 experience cannot answer: what would a "
            "permanent policy do, once families had years to adjust?"
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(c.card), FadeIn(c.head), FadeIn(c.body[0]), *[FadeIn(m) for m in c[2:]])
            vo.wait_until("b")
            self.play(FadeIn(c.body[1]))
            vo.wait_until("c")
            self.play(FadeIn(why[0]))
            vo.wait_until("d")
            self.play(FadeIn(why[1]))
        self.clear_scene()

    def transfer(self):
        cols = [r"permanent", r"in America", r"today", r"measured, \\ not assumed"]
        rows = [(r"2021 payments", (0, 1, 1, 1), SPM), (r"Canada, \ 2016", (1, 0, 1, 1), EVIDENCE),
                (r"Mothers' Pensions", (1, 1, 0, 1), CHILD), (r"the simulation", (1, 1, 1, 0), BUDGET)]
        xs = [-2.0, 0.4, 2.6, 4.9]
        hdr = VGroup(*[label(c, font_size=20, color=GREY_A).move_to([x, 2.1, 0]) for c, x in zip(cols, xs)])
        grid = VGroup()
        for i, (name, ticks, col) in enumerate(rows):
            y = 1.0 - 0.95 * i
            nm = label(name, font_size=22, color=col).move_to([-4.6, y, 0])
            cells = VGroup(*[label(YES if t else NO, font_size=30, color=GAIN if t else LOSS).move_to([x, y, 0])
                             for t, x in zip(ticks, xs)])
            grid.add(VGroup(nm, cells))
        foot = label(r"no study ticks every box: \ the memo must combine them, \ and say how", font_size=22,
                     color=E.ACCENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Do these transfer to the Island's permanent allowance? Ask four questions of each. <bookmark "
            "mark='a'/> The 2021 payments were American, recent and measured, but they lasted six months, and "
            "people do not reorganize their working lives around a payment they expect to end. <bookmark "
            "mark='b'/> Canada's benefit is permanent, recent and measured, but Canada's labour market, health "
            "care and other benefits differ. <bookmark mark='c'/> The Mothers' Pensions were permanent and "
            "American and measured a lifetime, but a century ago. <bookmark mark='d'/> And the simulation is "
            "permanent, American and current, but its key numbers are assumed. <bookmark mark='e'/> No study ticks "
            "every box. The memo has to combine them, and say how."
        ) as vo:
            self.play(FadeIn(hdr))
            for mk, g in zip("abcd", grid):
                vo.wait_until(mk)
                self.play(FadeIn(g[0]), LaggedStart(*[FadeIn(c, scale=1.3) for c in g[1]], lag_ratio=0.2),
                          run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
