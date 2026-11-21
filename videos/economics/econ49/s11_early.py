from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Early(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Early childhood", r"Is the best investment the earliest one?",
             "Chapter nine. Early childhood.", lit={1962: r"Perry Preschool", 2006: r"Heckman",
                                                    2022: r"Durkin et al."}, scale=("person",),
             horizon=("a lifetime",))
        self.perry()
        self.curve()
        self.replicate()

    def perry(self):
        T = tables.EARLY_49.data
        chain = flow_chain([(rf"Ypsilanti, \ Michigan, \\ {T['perry_year']}", CHILD),
                            (rf"{T['perry_n']} children, \\ aged 3 and 4", WOMEN), (r"half get two years \\ of "
                                                                                   r"preschool", SCHOOL),
                            (r"followed \\ to age 40", GAIN)],
                           notes=[r"poor, \ black families", r"chosen by lottery, \\ roughly", r"and home visits",
                                  r"earnings, \ crime, \\ welfare"], box_w=2.9, font_size=19,
                           note_size=17).move_to(UP * 1.2)
        res = VGroup(
            label(r"the test-score gains faded within a few years", font_size=22, color=HOLD),
            label(r"but as adults: \ more earnings, \ less crime, \ less welfare", font_size=22, color=GAIN),
            label(rf"Heckman and colleagues: \ a return of {T['perry_lo']}--{T['perry_hi']}\% a year to society",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 1.7)
        tag = published_tag(r"Heckman et al., \ J. Public Econ. (2010)", corner=DR, font_size=11)
        with self.voiceover(
            "If schools matter, perhaps what comes before school matters more. <bookmark mark='a'/> In 1962, in "
            "Ypsilanti, Michigan, the Perry Preschool project took "
            f"{T['perry_n']} three- and four-year-olds from poor black families, <bookmark mark='b'/> and gave about "
            "half of them, chosen roughly by lottery, two years of preschool and weekly home visits. <bookmark "
            "mark='c'/> They have been followed to the age of forty. <bookmark mark='d'/> The gains in test scores "
            "faded within a few years. <bookmark mark='e'/> But as adults the children who went earned more, were "
            "arrested less and depended less on welfare. <bookmark mark='f'/> James Heckman and colleagues "
            f"estimated a return to society of {T['perry_lo']} to {T['perry_hi']} percent a year, better than the "
            "stock market's."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]), FadeIn(chain.notes[1]))
            vo.wait_until("b")
            self.play(GrowArrow(chain.arrows[1]), FadeIn(chain.boxes[2]), FadeIn(chain.notes[2]))
            vo.wait_until("c")
            self.play(GrowArrow(chain.arrows[2]), FadeIn(chain.boxes[3]), FadeIn(chain.notes[3]))
            for mk, r_ in zip("def", res):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def curve(self):
        ax = plane([0, 30], [0, 1], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.4,
                   xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[], xlabel=r"age at which the investment is made",
                   ylabel=r"return \ (schematic)", xfmt=lambda v: f"{v:.0f}", font_size=14)
        a = np.linspace(0, 30, 120)
        h = 0.12 + 0.8 * np.exp(-a / 5.5)
        heck = path(ax, a, h, CHILD, 3.4)
        flat = path(ax, a, 0.35 + 0.0 * a, HOLD, 3.0)
        side = VGroup(
            label(r"Heckman's argument: \\ skills beget skills, \\ so early returns \\ are highest", font_size=17,
                  color=CHILD),
            label(r"a shape argued from \\ theory and a few \\ programmes, \ not \\ a fitted curve", font_size=17,
                  color=GREY_A),
            label(r"Rea and Burton, \\ hundreds of \\ programmes: \ no \\ fall with age", font_size=17, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Heckman, \ Science (2006); \ Rea and Burton, \ J. Econ. Surveys (2020)", corner=DR,
                            font_size=11)
        with self.voiceover(
            "From Perry and a few similar programmes came an influential picture. <bookmark mark='a'/> James "
            "Heckman argued that skills beget skills: what a child learns early makes later learning cheaper, so "
            "the return to investing in people falls with the age at which it is made. <bookmark mark='b'/> The "
            "picture is drawn from theory and a handful of programmes; it is not a curve fitted to many. <bookmark "
            "mark='c'/> David Rea and Tony Burton took the benefit-cost ratios of hundreds of programmes evaluated "
            "for Washington State and found no sign that returns fall with the age of the people served: good and "
            "bad programmes at every age. Heckman replied that his curve was about what is possible, not about the "
            "average programme. Both can be true."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(heck), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(flat), FadeIn(side[2]), run_time=2.0)
        self.clear_scene()

    def replicate(self):
        T = tables.EARLY_49.data
        cards = point_cards([
            (r"Perry, \ 1962", r"small, \ intensive, \\ followed for 40 \\ years: \ large \\ adult gains", GAIN),
            (r"Head Start's trial", r"national, \ random: \\ gains largely gone \\ by first grade, \\ few by third",
             HOLD),
            (r"Tennessee's pre-K", rf"{T['tn_n']:,} children, \\ random: \ lower \\ scores in grades \\ 3 to 6"
             .replace(",", "{,}"), LOSS),
            (r"the lesson", r"a programme is not \\ a category: \ what \\ works at small scale \\ may not at large",
             E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"what replicates?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.EARLY_49.tag, corner=DR, font_size=11)
        with self.voiceover(
            "And when programmes like Perry are scaled up? <bookmark mark='a'/> Perry was small and intensive, run "
            "by enthusiasts and followed for decades. <bookmark mark='b'/> America's national Head Start programme "
            "was put to a randomized trial: the gains at the end of the programme had largely faded by the end of "
            "first grade, with few differences left by third. <bookmark mark='b2'/> Its defenders point to long-run "
            "studies of Head Start "
            "that find gains in adulthood, as at Perry. <bookmark mark='c'/> Tennessee's statewide pre-kindergarten "
            f"programme was also tested by lottery, with {T['tn_n']:,} children. By sixth grade, the children "
            "offered a place were doing worse than the others, with lower scores and more trouble at school. "
            "<bookmark mark='d'/> The lesson is not that early childhood does not matter. It is that a programme "
            "is not a category: what works at small scale with the best staff may not survive being scaled up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(cards.cards[0], color=WHITE, scale_factor=1.04))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
                if mk == "b":
                    vo.wait_until("b2")
                    self.play(Indicate(cards.cards[0], color=WHITE, scale_factor=1.04))
        self.clear_scene()
