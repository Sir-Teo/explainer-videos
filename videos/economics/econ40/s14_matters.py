from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class Matters(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Does inequality matter?", r"For growth, \ for health, \ for politics: \ what can be known?",
             "Chapter twelve. Does inequality matter?", lit={2016: r"Chetty et al., \ JAMA"},
             scale=("household", "nation"), horizon=("a decade",))
        self.health()
        self.identify()

    def health(self):
        M = tables.MATTERS.data
        rows = [(r"men", M["men"], PARENT), (r"women", M["women"], CHILD)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(rows):
            y = 0.6 - 1.4 * k
            r = Rectangle(width=v * 0.5, height=0.7, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-2.0 + v * 0.25, y, 0]))
            bars.add(VGroup(label(nm, font_size=24, color=col).next_to(np.array([-2.15, y, 0]), LEFT, buff=0.15),
                            r, label(f"{v} years", font_size=24, color=WHITE).next_to(r, RIGHT, buff=0.2)))
        head = label(r"life expectancy at 40: \ the richest 1\% against the poorest 1\%", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        sub = label(r"tax records linked to death records, \ 2001--2014; \ the gap widened over the period",
                    font_size=19, color=GREY_A).next_to(head, DOWN, buff=0.2)
        foot = label(r"income buys health, \ and health earns income: \ the gradient is not, \ by itself, \ an effect "
                     r"of inequality", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.MATTERS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Does any of this matter, beyond the numbers? Start with the starkest. Linking tax records to death "
            "records, Chetty and coauthors measured life expectancy by income. <bookmark mark='a'/> At forty, the "
            f"richest one percent of American men can expect to live {M['men']} years longer than the poorest one "
            f"percent; <bookmark mark='b'/> for women, {M['women']} years. Between 2001 and 2014 the gap widened. "
            "<bookmark mark='c'/> But a gradient is not an effect of inequality. Income buys health, and health "
            "earns income: illness lowers earnings as surely as poverty raises illness. Whether a more unequal "
            "society is less healthy, holding each person's own income fixed, is a different and much harder "
            "question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(tag), *[FadeIn(b_[0]) for b_ in bars])
            for mk, b_ in zip("ab", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b_[1], LEFT), FadeIn(b_[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def identify(self):
        cards = point_cards([
            (r"growth", r"regressions across \\ countries find positive, \\ negative and no effects, \\ by sample and "
                        r"method", TOP),
            (r"health", r"own income matters; \\ others' income is \\ hard to separate from \\ everything else",
             CHILD),
            (r"politics", r"the rich vote, \ give \\ and lobby more; \\ whether policy follows \\ is debated", WEALTH),
            (r"what can be learned", r"natural experiments: \\ lotteries, \ reforms, \\ local shocks, \ moves", GAIN),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.1)
        head = label(r"what can be identified", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        sub = label(r"the same difficulty everywhere: \ a correlation across places \ or countries is not an effect",
                    font_size=20, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The same difficulty runs through every claim about inequality's consequences. <bookmark mark='a'/> For "
            "growth: regressions of growth on inequality across countries have found positive, negative and no "
            "effects, depending on the period, the sample and the method; countries differ in too many other ways. "
            "<bookmark mark='b'/> For health: a person's own income clearly matters; the effect of other people's "
            "incomes is very hard to separate from everything else that differs between places. "
            "<bookmark mark='c'/> For politics: the rich vote, give and lobby more, and whether policy follows "
            "their preferences more closely is a live debate. <bookmark mark='d'/> What has worked is the toolkit of "
            "Part four: lotteries, reforms, local shocks and moves, like the movers of chapter ten. Inequality "
            "matters most clearly where it shapes opportunity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub, shift=UP * 0.1))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
