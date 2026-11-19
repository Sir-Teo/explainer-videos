from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403


def votes_square(n, color, cell=0.28):
    """n votes cost n^2 credits: an n-by-n square of cells."""
    g = VGroup(*[Square(cell, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=0.35)
                 for _ in range(n * n)])
    g.arrange_in_grid(n, n, buff=0.03)
    return g


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ new votes, \ and choosing for machines", r"Can a vote measure how much people "
             r"care, \ and whose preferences should a machine learn?",
             "Chapter fifteen. Frontier: new votes, and choosing for machines.",
             lit={2009: r"Bernheim and Rangel", 2018: r"Lalley and Weyl", 2024: r"social choice for AI"},
             scale=("person", "nation", "world"), horizon=("a decade",))
        self.behavioural()
        self.quadratic()
        self.machines()

    def behavioural(self):
        rows = VGroup(
            label(r"welfare economics assumed that what people choose shows what is good for them", font_size=23),
            label(r"but choices shift with framing, \ defaults and the moment: \ parts seven and forty-five",
                  font_size=23, color=GREY_A),
            label(r"Bernheim and Rangel, \ 2009: \ count x as better than y only if y is never chosen when x is "
                  r"available", font_size=22, color=WELF),
            label(r"the ranking has gaps where choices conflict: \ welfare stays silent there", font_size=23,
                  color=RULE),
            label(r"which choices to trust, \ the planner's or the doer's, \ is the new form of Robbins's question",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Bernheim and Rangel, QJE 124(1) (2009)", corner=DR, font_size=13)
        with self.voiceover(
            "The first frontier is inside each person. <bookmark mark='a'/> Welfare economics assumed that what "
            "people choose shows what is good for them. <bookmark mark='b'/> But choices shift with framing, with "
            "defaults, with the moment, as parts seven and forty-five show. <bookmark mark='c'/> Douglas Bernheim and "
            "Antonio Rangel proposed in 2009 to count x as better than y only when y is never chosen while x is "
            "available. <bookmark mark='d'/> The result is a ranking with gaps: where a person's choices conflict, "
            "welfare economics stays silent rather than guess. <bookmark mark='e'/> Deciding which choices to trust, "
            "the planner's in January or the doer's in December, is the new form of Robbins's old question."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def quadratic(self):
        sq = VGroup(*[VGroup(votes_square(n, VOTE["E"]), label(rf"{n} vote{'s' if n > 1 else ''}: \ {n * n} "
                                                                  rf"credit{'s' if n > 1 else ''}", font_size=19,
                                                                  color=GREY_A))
                      for n in (1, 2, 3, 4)])
        for g in sq:
            g.arrange(DOWN, buff=0.15)
        sq.arrange(RIGHT, buff=0.6, aligned_edge=DOWN).move_to(UP * 1.2)
        rows = VGroup(
            label(r"the $n$th vote costs $n^2 - (n-1)^2 = 2n - 1$ credits more", font_size=23, color=RULE),
            label(r"so each voter buys votes until the next costs more than the issue is worth to them", font_size=22),
            label(r"votes in proportion to how much you care: \ intensity, \ not only direction", font_size=23,
                  color=WELF),
            label(r"Lalley and Weyl: \ in large electorates, \ close to the efficient decision; \ collusion is its "
                  r"weak point", font_size=21, color=GREY_A),
            label(r"Colorado's House Democrats ranked spending bills this way in 2019; \ a court later required the "
                  r"votes be public", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).next_to(sq, DOWN, buff=0.45)
        tag = published_tag(r"Lalley and Weyl, AEA P\&P 108 (2018); \ Posner and Weyl, \emph{Radical Markets} "
                            r"(2018)", corner=DR, font_size=12)
        with self.voiceover(
            "The second frontier is the ballot. One person, one vote cannot record how much anyone cares: a "
            "majority that mildly prefers one plan beats a minority that badly needs another. Quadratic voting gives "
            "each voter a budget of credits. <bookmark mark='a'/> One vote on an issue costs one credit, two votes cost four, "
            "three cost nine, four cost sixteen. <bookmark mark='b'/> So each extra vote costs more than the last: "
            "the nth costs two n minus one. <bookmark mark='c'/> A voter keeps buying until the next vote costs more "
            "than the issue is worth to them, <bookmark mark='d'/> and so casts votes in proportion to how much they "
            "care. <bookmark mark='e'/> Steven Lalley and Glen Weyl showed that in large electorates the result comes "
            "close to the efficient decision. Its weak point is collusion: two people who agree can split their "
            "votes and pay less. <bookmark mark='f'/> In 2019 the Democrats in Colorado's House used it to rank "
            "competing spending bills; a court later required that the votes be made public."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in sq], lag_ratio=0.5), run_time=3)
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def machines(self):
        rows = VGroup(
            label(r"language models are tuned on many people's comparisons of answers", font_size=23),
            label(r"fit one reward to everyone, \ and the model aggregates them: \ but by which rule?", font_size=23,
                  color=RULE),
            label(r"Siththaranjan, \ Laidlaw and Hadfield-Menell, \ 2024: \ implicitly, \ Borda's count", font_size=23,
                  color=VOTE["D"]),
            label(r"so, \ by Gibbard and Satterthwaite, \ annotators can gain by misreporting", font_size=23,
                  color=CYCLE),
            label(r"Conitzer and colleagues, \ 2024: \ who gives feedback, \ what kind, \ how to aggregate: \ social "
                  r"choice's questions", font_size=21, color=WELF),
            label(r"2023: \ about 1{,}000 Americans proposed and voted on rules for a model \ (Collective "
                  r"Constitutional AI)", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"ICLR 2024 (arXiv 2312.08358); \ ICML 2024, PMLR 235; \ Huang et al., FAccT 2024",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The newest frontier is choosing for machines. <bookmark mark='a'/> Large language models are tuned on "
            "many people's comparisons between pairs of answers. <bookmark mark='b'/> Fitting a single reward to "
            "everyone's comparisons aggregates their preferences, so it is a social choice rule. But which one? "
            "<bookmark mark='c'/> Anand Siththaranjan, Cassidy Laidlaw and Dylan Hadfield-Menell showed in 2024 that, "
            "when annotators differ in ways the data don't record, the standard method implicitly runs Borda's "
            "count. <bookmark mark='d'/> Which means, by Gibbard and Satterthwaite, that annotators can gain by "
            "misreporting. <bookmark mark='e'/> Vincent Conitzer and colleagues argued the same year that the "
            "questions of alignment, who gives feedback, what kind, and how to combine it, are social choice's "
            "questions. <bookmark mark='f'/> And in 2023 Anthropic and the Collective Intelligence Project asked "
            "about a thousand Americans to propose and vote on rules for a model, then trained one on the result. "
            "Condorcet's problem has a new electorate."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
