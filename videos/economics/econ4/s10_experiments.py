from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403

LOTTO = "#7BD88F"
STAYED = "#9AA5B8"


def step_area(ax, edges, h, color, opacity=0.35):
    """A histogram drawn as one filled step outline."""
    a = ax.ax
    pts = [a.c2p(edges[0], 0)]
    for x0, x1, v in zip(edges[:-1], edges[1:], h):
        pts += [a.c2p(x0, v), a.c2p(x1, v)]
    pts.append(a.c2p(edges[-1], 0))
    return Polygon(*pts, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=opacity)


class Experiments(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Experiments", r"What if you run the lottery on purpose?",
             "Chapter eight. Experiments.", lit=("households", "government"), scale=("person", "household"),
             horizon=("a year", "a decade"))
        self.island()
        self.nit()
        self.progresa()
        self.field()

    def _panel(self, ex, way, x, title, in_name, out_name, in_color):
        p = ex[way]
        ax = axes([-3, 3], [0, 0.55], x_length=5.0, y_length=2.4, xticks=[-2, 0, 2], yticks=None,
                  xlabel=r"ability \ (planted; nobody sees it)", font_size=18, center=[x, 0.15, 0])
        head = label(title, font_size=27, color=in_color).next_to(ax, UP, buff=0.35)
        outs = step_area(ax, ex["edges"], p["out"], STAYED, 0.25)
        ins = step_area(ax, ex["edges"], p["in"], in_color, 0.35)
        key = VGroup(Square(0.18, stroke_width=0, fill_color=in_color, fill_opacity=0.8),
                     label(in_name, font_size=19, color=in_color),
                     Square(0.18, stroke_width=0, fill_color=STAYED, fill_opacity=0.8),
                     label(out_name, font_size=19, color=STAYED)).arrange(RIGHT, buff=0.12)
        key[2].shift(RIGHT * 0.25)
        key[3].shift(RIGHT * 0.25)
        key.next_to(head, DOWN, buff=0.12)
        n1, n0 = p["n1"], p["n0"]
        res = VGroup(
            label(rf"{n1} in, \ {n0} out", font_size=20, color=GREY_B),
            label(rf"earnings gap: \ ${p['diff']:+.3f}$ \ (s.e.\ {p['se']:.3f})", font_size=25, color=in_color),
        ).arrange(DOWN, buff=0.14).next_to(ax, DOWN, buff=0.25)
        return VGroup(ax, head, key, outs, ins, res), ax, head, key, outs, ins, res

    def island(self):
        ex = load("experiment")
        left, *L = self._panel(ex, "chose", -3.5, r"they chose", r"signed up", r"stayed out", NONEXP)
        right, *R = self._panel(ex, "lottery", 3.5, r"a lottery chose", r"won a place", r"did not", LOTTO)
        truth = label(rf"planted effect of the apprenticeship: \ $+{ex['effect']:.2f}$", font_size=26,
                      color=E.TRUTH).to_edge(DOWN, buff=0.45)
        tag = island_tag(rf"simulated: the Island, {ex['n']:,} young islanders".replace(",", "{,}"), corner=DR,
                         font_size=14).shift(UP * 0.45)
        with self.voiceover(
            "Why does a lottery work when careful regressions fail? Watch it on the Island. "
            "<bookmark mark='a'/> The boatwrights offer a year's apprenticeship, and we've planted its effect: it "
            "raises a young islander's earnings by ten percent. <bookmark mark='b'/> First, let the islanders "
            "choose. Those with the poorest prospects are keenest to sign up. Here is their ability, which we "
            "planted and nobody can see: the ones who signed up sit to the left of the ones who stayed out. "
            f"<bookmark mark='c'/> Compare their earnings, and the apprenticeship seems to cut them, by "
            f"{abs(ex['chose']['diff']) * 100:.0f} percent. Wrong in sign, like the survey comparisons in "
            "LaLonde's test. <bookmark mark='d'/> Now give the places by lottery. The winners and the losers are "
            "alike in ability, not because anyone measured it, but because a coin can't tell who is able. "
            f"<bookmark mark='e'/> And the gap in earnings is {ex['lottery']['diff'] * 100:.0f} percent, within "
            "its margin of the truth. That is what randomization buys: balance on everything, including what no "
            "one can see."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(L[0]), FadeIn(L[1]), FadeIn(R[0]), FadeIn(R[1]))
            vo.wait_until("a")
            self.play(FadeIn(truth))
            vo.wait_until("b")
            self.play(FadeIn(L[2]), FadeIn(L[3]), FadeIn(L[4]))
            vo.wait_until("c")
            self.play(FadeIn(L[5]))
            self.play(Indicate(L[5][1], color=NONEXP))
            vo.wait_until("d")
            self.play(FadeIn(R[2]), FadeIn(R[3]), FadeIn(R[4]))
            vo.wait_until("e")
            self.play(FadeIn(R[5]))
            self.play(Indicate(R[5][1], color=LOTTO), Indicate(truth, color=E.TRUTH))
        self.clear_scene()

    def nit(self):
        n = load("nit")
        G, t = n["shown"]["G"], n["shown"]["t"]
        ax = axes([0, 2.6], [0, 2.6], x_length=5.0, y_length=4.4, xticks=[0, 1, 2], yticks=[0, 1, 2],
                  xlabel=r"earnings \ (in poverty lines)", ylabel=r"income after the plan", font_size=19,
                  center=LEFT * 3.2 + DOWN * 0.3)
        a = ax.ax
        diag = DashedLine(a.c2p(0, 0), a.c2p(2.5, 2.5), color=GREY_B, stroke_width=2.5)
        dl = label(r"no plan", font_size=19, color=GREY_B).next_to(a.c2p(2.5, 2.5), DOWN + RIGHT, buff=0.05)
        be = G / t
        plan = VGroup(Line(a.c2p(0, G), a.c2p(be, be), color=E.ACCENT, stroke_width=5),
                      Line(a.c2p(be, be), a.c2p(2.5, 2.5), color=E.ACCENT, stroke_width=5))
        gdot = Dot(a.c2p(0, G), radius=0.08, color=E.ACCENT)
        gl = label(r"the guarantee", font_size=20, color=E.ACCENT).move_to(gdot.get_center() + UP * 0.62 + RIGHT * 0.8)
        bdot = Dot(a.c2p(be, be), radius=0.08, color=E.ACCENT)
        bl = label(r"break-even", font_size=20, color=E.ACCENT).next_to(bdot, DOWN + RIGHT, buff=0.08)
        slope = label(rf"each dollar earned \\ keeps {100 * (1 - t):.0f} cents", font_size=19, color=E.ACCENT)
        slope.move_to(a.c2p(0.75, 2.05))
        others = VGroup(*[DashedLine(a.c2p(0, G), a.c2p(min(G / r, 2.5), G + (1 - r) * min(G / r, 2.5)),
                                     color=E.ACCENT, stroke_width=2, stroke_opacity=0.5) for r in (0.3, 0.7)])
        rows = VGroup(
            label(r"the negative income tax: \ Milton Friedman, 1962", font_size=24, color=E.ACCENT),
            label(r"New Jersey and Pennsylvania, 1968--72: \\ about 1,350 families, \ randomly assigned"
                  .replace("1,350", "1{,}350"), font_size=23),
            label(r"guarantees of 50 to 125\% of the poverty line, \\ tax rates of 30, 50 or 70\%: \ eight plans",
                  font_size=23),
            label(r"then Gary, Seattle--Denver, \ rural areas, \\ and Manitoba's Mincome", font_size=23, color=GREY_A),
            label(r"found: \ people worked somewhat less; \\ wives and single mothers more so than husbands",
                  font_size=23, color=EXP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.45).shift(UP * 0.2)
        tag = published_tag(r"Friedman (1962); Kershaw and Fair (1976); Munnell, ed., \emph{Lessons from the Income "
                            r"Maintenance Experiments} (1986)", corner=DL, font_size=13)
        with self.voiceover(
            "Economists began running such lotteries on purpose in the late 1960s, on the biggest question in "
            "welfare policy. <bookmark mark='a'/> Milton Friedman had proposed a negative income tax: give every "
            "family a guaranteed income, <bookmark mark='b'/> and as the family earns more, take back part of "
            "each dollar, until at the break-even point the payment runs out. <bookmark mark='c'/> The worry was "
            "obvious. If each dollar you earn keeps only fifty cents, will you work less? Nobody's regressions "
            "could settle it. <bookmark mark='d'/> So from 1968 about thirteen hundred and fifty low-income "
            "families in New Jersey and Pennsylvania were assigned at random to eight different plans, or to "
            "none, <bookmark mark='e'/> with guarantees from half the poverty line to one and a quarter times it, "
            "and tax rates of thirty, fifty or seventy percent. <bookmark mark='f'/> Larger trials followed, the "
            "biggest in Seattle and Denver. <bookmark mark='g'/> Their answer: people did work somewhat less, "
            "husbands a little, wives and single mothers more. Some of the fall turned out to be earnings that "
            "families simply didn't report, which is its own lesson in measurement."
        ) as vo:
            self.play(FadeIn(ax), Create(diag), FadeIn(dl), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(gdot, scale=1.5), FadeIn(gl))
            vo.wait_until("b")
            self.play(Create(plan[0]), FadeIn(bdot), FadeIn(bl))
            self.play(Create(plan[1]))
            vo.wait_until("c")
            self.play(FadeIn(slope))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]), Create(others))
            vo.wait_until("f")
            self.play(FadeIn(rows[3]))
            vo.wait_until("g")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def progresa(self):
        # 506 villages: 320 drawn to start in 1998, 186 to wait until the end of 1999
        rng = np.random.default_rng(1997)
        order = rng.permutation(506)
        first = set(order[:320].tolist())
        cols, size, gap = 30, 0.16, 0.05
        grid = VGroup()
        for k in range(506):
            r_, c_ = divmod(k, cols)
            sq = Square(size, stroke_width=0, fill_color=GREY_C, fill_opacity=0.9)
            sq.move_to([c_ * (size + gap), -r_ * (size + gap), 0])
            grid.add(sq)
        grid.move_to(LEFT * 3.3 + DOWN * 0.15)
        colored = [sq.animate.set_fill(LOTTO if k in first else STAYED, opacity=0.95) for k, sq in enumerate(grid)]
        key = VGroup(Square(0.2, stroke_width=0, fill_color=LOTTO, fill_opacity=0.95),
                     label(r"320 villages: \ payments from 1998", font_size=20, color=LOTTO),
                     Square(0.2, stroke_width=0, fill_color=STAYED, fill_opacity=0.95),
                     label(r"186 villages: \ about two years later", font_size=20, color=STAYED))
        key.arrange_in_grid(rows=2, cols=2, buff=(0.15, 0.15), col_alignments="cl").next_to(grid, DOWN, buff=0.3)
        head = label(r"PROGRESA, \ rural Mexico, \ 1997", font_size=30, color=E.ACCENT).next_to(grid, UP, buff=0.35)
        rows = VGroup(
            label(r"cash to mothers, \ if the children go to school \\ and the family keeps its clinic visits",
                  font_size=24),
            label(r"designed by Santiago Levy, \ deputy finance minister", font_size=23, color=GREY_A),
            label(r"the order of the villages: \ a lottery", font_size=24, color=LOTTO),
            label(r"enrolment rose, \ most at the step into \\ secondary school, \ and most for girls", font_size=24,
                  color=EXP),
            label(r"the evidence helped it survive a change of government \\ (2002: Oportunidades)", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45).shift(UP * 0.2)
        tag = published_tag(r"Skoufias (2005), IFPRI; Schultz, J.\ Dev.\ Econ.\ 74 (2004); Levy, \emph{Progress "
                            r"against Poverty} (2006)", corner=DL, font_size=13)
        with self.voiceover(
            "The idea travelled. <bookmark mark='a'/> In 1997 Mexico launched PROGRESA, which paid mothers in poor "
            "rural villages if their children went to school and the family kept its visits to the clinic. "
            "<bookmark mark='b'/> Its designer, the economist Santiago Levy, then deputy finance minister, wanted "
            "proof that would outlast the government. <bookmark mark='c'/> Five hundred and six villages were "
            "chosen for the evaluation. <bookmark mark='d'/> There wasn't money to start everywhere at once, so a "
            "lottery decided the order: three hundred and twenty villages began first, and the other one hundred "
            "and eighty-six about two years later. <bookmark mark='e'/> The comparison was clean. Enrolment rose, "
            "most at the step from primary into secondary school, and most for girls. <bookmark mark='f'/> When a "
            "new government took office, the programme survived under a new name, and versions of it now run in "
            "dozens of countries."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(sq, scale=0.5) for sq in grid], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("d")
            self.play(*colored, FadeIn(key), FadeIn(rows[2]), run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
            vo.wait_until("f")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def field(self):
        kinds = point_cards([
            (r"the laboratory", r"markets and games with real money, \\ students as traders: \ Vernon Smith, "
                                r"Nobel 2002 \ (Part 2)", "#9AA5B8"),
            (r"field experiments", r"real markets, \ real traders: \\ John List at sports-card shows, \ Part 45",
             "#F2B84B"),
            (r"policy trials", r"textbooks, deworming, microcredit: \\ Kremer, Banerjee and Duflo, \ Nobel 2019",
             LOTTO),
            (r"A/B tests", r"thousands a day, \ inside online firms: \\ chapter 12", E.ACCENT),
        ], width=12.6, cols=2, font_size=22).move_to(UP * 0.35)
        warn = label(r"an experiment answers the question it asked, \ where and when it asked it", font_size=27,
                     color=E.MISS).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"the Nobel prize in economic sciences, 2002 and 2019", corner=DR, font_size=13)
        with self.voiceover(
            "Experiments in economics now come in four kinds. <bookmark mark='a'/> In the laboratory, people trade "
            "and bargain for real money: Vernon Smith's double auctions, which you saw in Part 2, won him a Nobel "
            "prize in 2002. <bookmark mark='b'/> In the field, experiments run in real markets, with the people who "
            "trade there, sometimes without their knowing they are in one. <bookmark mark='c'/> Policy trials test "
            "programmes before they are scaled up: textbooks and deworming pills in Kenyan schools, microcredit in "
            "Indian cities. Michael Kremer, Abhijit Banerjee and Esther Duflo shared the 2019 prize for this "
            "approach. <bookmark mark='d'/> And inside online firms, thousands of small experiments run every day; "
            "chapter twelve meets the people who run them. <bookmark mark='e'/> But an experiment has a limit "
            "built in. It answers the question it asked, in the place and time it asked it. Whether the answer "
            "travels is a different question, and the next two chapters are about it."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c_ in zip("abcd", kinds.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(warn))
        self.clear_scene()
