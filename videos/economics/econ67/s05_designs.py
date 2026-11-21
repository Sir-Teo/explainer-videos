from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403


class Designs(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Specification searching by design", r"Do some research designs leave more room to search "
             r"than others?", "Chapter four. Specification searching by design.",
             lit={1983: "Leamer", 2020: "Brodeur, Cook and Heyes"}, scale=("world",), horizon=("a decade",))
        self.published()
        self.panels()
        self.caveat()

    def published(self):
        D = tables.SELECTION_67.data
        cards = point_cards([
            (r"the data", rf"over {D['bch_tests']:,} tests in {D['bch_journals']} leading journals, \ 2015 and "
             r"2018, \ each tagged by its design", FIRST),
            (r"the finding", r"instruments show the most bunching just past 1.96, \ difference in differences "
             r"some, \ trials and discontinuities the least", FAIL),
            (r"why it fits", r"an instrument, \ a control group or a time window can be chosen after seeing "
             r"results; \ a randomization or a cutoff is fixed before", TRUE),
            (r"Leamer, \ 1983", r"`let's take the con out of econometrics': \ results that depend on unreported "
             r"choices are not evidence", STATE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"methods matter", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Brodeur, \ Cook and Heyes, \ \emph{AER} 110(11) (2020); \ Leamer, \ \emph{AER} "
                            r"73(1) (1983)", corner=DL, font_size=12)
        with self.voiceover(
            "In 2020 Brodeur returned with Nikolai Cook and Anthony Heyes. <bookmark mark='a'/> They collected over "
            "twenty-one thousand tests from twenty-five leading journals, and tagged each by the design that "
            "produced it: randomized trials, regression discontinuities, difference in differences, instrumental "
            "variables. <bookmark mark='b'/> The bunching just past the line was worst for instruments, present "
            "for difference in differences, and least for trials and discontinuities. <bookmark mark='c'/> That "
            "fits how the designs work. Which instrument, which control group, which time window: these can be "
            "chosen after seeing results. A randomization, or a cutoff set by law, is fixed before anyone looks. "
            "<bookmark mark='d'/> Edward Leamer had made the general point in 1983, in a paper called Let's Take the "
            "Con out of Econometrics: a result that depends on choices nobody reports is not yet evidence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def panels(self):
        Dd = load("designs")
        bins = np.array(Dd["bins"], float)
        cells = VGroup()
        for d_ in Dd["order"]:
            r = Dd["designs"][d_]
            ax = plane([0, 5], [0, 1500], x_length=5.0, y_length=2.1, xticks=[0, 1.96, 4],
                       yticks=[0, 1500], xfmt=lambda v: "1.96" if abs(v - 1.96) < 1e-9 else f"{v:.0f}",
                       yfmt=lambda v: f"{v:,.0f}", font_size=12)
            h = histogram(ax, bins[bins <= 5.0001], r["hist"][:50], DESIGN_COL[d_], opacity=0.8)
            ln = vline(ax, 1.96, 0, 1500, FAIL, 1.8)
            t = label(rf"{DESIGN_NAME[d_]}: \ search {100 * r['search']:.0f}\%", font_size=15,
                      color=DESIGN_COL[d_]).next_to(ax.ax, UP, buff=0.05)
            stat = label(rf"caliper {r['caliper']['ratio']:.1f} \ \ missing {100 * (1 - r['beta']):.0f}\%",
                         font_size=14, color=GREY_A).next_to(ax.ax.c2p(5, 1500), DL, buff=0.05)
            cells.add(VGroup(ax, h, ln, t, stat))
        cells.arrange_in_grid(rows=2, cols=2, buff=(0.7, 0.55)).move_to(DOWN * 0.15)
        if cells.width > 12.8:
            cells.scale_to_fit_width(12.8)
        note_ = label(r"caliper: \ results within 0.2 above 1.96 per result within 0.2 below; \ missing: \ the "
                      r"share of insignificant results the selection model finds absent", font_size=14,
                      color=GREY_A).to_edge(DOWN, buff=0.25)
        tag = island_tag(r"the simulated field, \ by design: \ agora.field.DESIGNS", corner=UL, font_size=12)
        order = Dd["order"]
        b = {d_: Dd["designs"][d_]["beta"] for d_ in order}
        cal = {d_: Dd["designs"][d_]["caliper"]["ratio"] for d_ in order}
        with self.voiceover(
            "The simulated field was built with this in mind. <bookmark mark='a'/> Its researchers search more "
            "when the design allows it: one in ten after an insignificant trial, three in twenty after a "
            "discontinuity, three in ten with a difference in differences, nearly half with an instrument. Journals "
            "treat every design alike. <bookmark mark='b'/> In each design's published results, the bump past "
            f"1.96 grows from trials to instruments: the caliper ratio runs from {cal['RCT']:.1f} and "
            f"{cal['RDD']:.1f} to {cal['DiD']:.1f} and {cal['IV']:.1f}. <bookmark mark='c'/> Fit Andrews and Kasy's "
            "selection model, the subject of the next chapter, to each panel. It cannot tell a researcher's search "
            "from an editor's rejection, but it measures their joint effect: the share of insignificant results "
            f"missing from the record rises from {100 * (1 - b['RCT']):.0f} percent for trials to "
            f"{100 * (1 - b['IV']):.0f} percent for instruments. The same journals, different freedom."
        ) as vo:
            self.play(FadeIn(tag), *[FadeIn(c[0]) for c in cells], *[FadeIn(c[2]) for c in cells],
                      *[FadeIn(c[3]) for c in cells])
            vo.wait_until("a")
            self.play(*[Indicate(c[3], color=WHITE) for c in cells])
            self.play(*[LaggedStart(*[GrowFromEdge(x, DOWN) for x in c[1]], lag_ratio=0.01) for c in cells],
                      run_time=2.5)
            vo.wait_until("b")
            self.play(*[FadeIn(c[4]) for c in cells], FadeIn(note_))
            vo.wait_until("c")
            self.play(*[Indicate(c[4], color=WHITE) for c in cells])
        self.clear_scene()

    def caveat(self):
        rows = VGroup(
            label(r"a test statistic of 1.97 rounded from 1.96 looks like bunching", font_size=22, color=GREY_A),
            label(r"Kranz and P\"utz (2022): \ adjusting for rounding, \ the evidence for difference in "
                  r"differences \\ at 5\% fades; \ for instruments it remains", font_size=22, color=PUB),
            label(r"Brodeur, \ Cook and Heyes accept it: \ the shakiest of their findings", font_size=22,
                  color=TRUE),
            label(r"the method of detecting bias is itself open to checking", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.2)
        tag = published_tag(r"Kranz and P\"utz, \ \emph{AER} 112(9) (2022), \ and the authors' reply", corner=DL,
                            font_size=12)
        with self.voiceover(
            "And the evidence on the evidence was itself checked. <bookmark mark='a'/> Many papers report "
            "coefficients and standard errors rounded to two or three digits, and a z computed from rounded numbers "
            "can land just past 1.96 by arithmetic alone. <bookmark mark='b'/> In 2022 Sebastian Kranz and Peter "
            "Pütz corrected for rounding: the bunching for difference in differences at five percent faded, while "
            "for instruments it remained. <bookmark mark='c'/> Brodeur, Cook and Heyes agreed that this had been "
            "their shakiest finding. <bookmark mark='d'/> That exchange is the system working: a claim about bias, "
            "replicated, corrected, and narrowed, in the same journal."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
