from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Bargaining(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Bargaining inside the household", r"Does it matter whose pocket the money goes into?",
             "Chapter seven. Bargaining inside the household.", lit={1997: r"Lundberg, Pollak and Wales"},
             scale=("household",), horizon=("a year",))
        self.models()
        self.island()
        self.benefit()

    def models(self):
        left = VGroup(
            label(r"the unitary household", font_size=26, color=GREY_A),
            label(r"one budget, \ one set of tastes", font_size=20, color=WHITE),
            label(r"income is pooled: \\ who brings it home \\ cannot matter", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.3)
        right = VGroup(
            label(r"the collective household", font_size=26, color=E.ACCENT),
            label(r"two people, \ two sets of tastes", font_size=20, color=WHITE),
            label(r"they bargain; \ each one's say \\ grows with what they \\ would have alone", font_size=20,
                  color=WHITE),
        ).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=2.0).move_to(UP * 0.6)
        eq = MathTex(r"\max\; \lambda\, u_{\text{mother}} + (1-\lambda)\, u_{\text{father}}, \quad "
                     r"\lambda = \lambda(\text{her share of income})", font_size=34, color=THEORY).to_edge(DOWN,
                                                                                                buff=1.0)
        tag = published_tag(r"Becker (1981); \ Chiappori (1988); \ Lundberg and Pollak (1993)", corner=DR,
                            font_size=11)
        with self.voiceover(
            "Becker's household made decisions as if it were one person, with one budget and one set of tastes. "
            "<bookmark mark='a'/> In this unitary household income is pooled: a pound earned by the father and a "
            "pound earned by the mother buy the same things. <bookmark mark='b'/> The alternative, developed by "
            "Pierre-André Chiappori, Shelly Lundberg, Robert Pollak and others, is a household of two people with "
            "their own tastes, who bargain. <bookmark mark='c'/> Each one's weight in the bargain rises with what "
            "they would have on their own, and so with the share of the income they control. <bookmark mark='d'/> "
            "Then who receives the money matters. That is testable."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(left[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(left[1:]))
            vo.wait_until("b")
            self.play(FadeIn(right[0]), FadeIn(right[1]))
            vo.wait_until("c")
            self.play(FadeIn(right[2]))
            vo.wait_until("d")
            self.play(Write(eq), run_time=1.5)
        self.clear_scene()

    def island(self):
        B = load("bargain")
        s = np.array(B["share"])
        ax = plane([0, 1], [0.1, 0.45], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.4,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0.1, 0.2, 0.3, 0.4],
                   xlabel=r"the mother's share of the household's income",
                   ylabel=r"share of the budget spent on the child", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        uni = path(ax, s, B["child_uni"], GREY_B, 3.0)
        col = path(ax, s, B["child_col"], E.ACCENT, 3.4)
        bf, af = B["before"], B["after"]
        arrow = Arrow(ax.ax.c2p(0.3, bf["child"]), ax.ax.c2p(0.4, af["child"]), buff=0.0, color=GAIN,
                      stroke_width=4, max_tip_length_to_length_ratio=0.3)
        side = VGroup(
            label(rf"the mother cares more \\ for the child good \\ ({B['child_taste'][1]:.2f} against "
                  rf"{B['child_taste'][0]:.2f})", font_size=17, color=WOMEN),
            label(r"grey: \ unitary, \ flat", font_size=17, color=GREY_B),
            label(r"gold: \ collective, \\ rising with her share", font_size=17, color=E.ACCENT),
            label(rf"move a tenth of income \\ to her purse: \ child \\ spending {100 * B['rise']:+.0f}\%",
                  font_size=17, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "On the Island, a household where the mother cares more than the father about spending on their "
            "child. <bookmark mark='a'/> In the unitary household, the share of the budget spent on the child is "
            "the same however the income is split. <bookmark mark='b'/> In the collective household it rises with "
            "the mother's share of the income, because her weight in the household's decisions rises with it. "
            "<bookmark mark='c'/> Now move a tenth of the household's income from the father's pay packet to the "
            f"mother's purse, with total income unchanged. Spending on the child rises {100 * B['rise']:.0f} "
            "percent. In the unitary model it would not change at all."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(uni), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(col), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("c")
            self.play(GrowArrow(arrow), FadeIn(side[3]), run_time=1.5)
        self.clear_scene()

    def benefit(self):
        chain = flow_chain([(r"before: \ a tax \\ allowance for \\ children", MEN), (r"the late 1970s: \\ a cash "
                                                                                   r"benefit", GREY_B),
                            (r"paid to \\ the mother", WOMEN), (r"spending on \\ children's and \\ women's clothes",
                                                                GAIN)],
                           notes=[r"in the father's \\ pay packet", r"the same money, \\ roughly", r"a different purse",
                                  r"rose relative \\ to men's"], box_w=2.9, font_size=19,
                           note_size=17).move_to(UP * 0.9)
        foot = VGroup(
            label(r"income is not pooled", font_size=26, color=E.ACCENT),
            label(r"later: \ pensions to grandmothers, \ transfers to mothers: \ mostly similar patterns",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.BARGAIN_49.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Britain ran the experiment. <bookmark mark='a'/> Until the late 1970s, most support for children came "
            "as a tax allowance, which raised the father's take-home pay. <bookmark mark='b'/> Then it was turned "
            "into a cash benefit, <bookmark mark='c'/> paid to the mother. <bookmark mark='d'/> Shelly Lundberg, "
            "Robert Pollak and Terence Wales found that spending on children's and women's clothing rose relative "
            "to spending on men's clothing. <bookmark mark='e'/> Income is not pooled. Studies since, of pensions "
            "paid to grandmothers in South Africa and of cash paid to mothers elsewhere, have mostly found similar "
            "patterns, one reason many transfer programmes now pay the mother."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]), Indicate(chain.boxes[0], color=WHITE, scale_factor=1.04))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(foot[0], shift=UP * 0.1))
            self.play(FadeIn(foot[1]))
        self.clear_scene()
