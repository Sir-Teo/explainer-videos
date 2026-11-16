from __future__ import annotations

from videos.music.music65.common import *  # noqa: F403


class Recombine(SoundScene):
    def construct(self):
        chapter(self, 5, r"Recombination", r"What if the machine copies on purpose, \ a phrase at a time?")
        self.cope()
        self.heard()
        self.questions()

    # ------------------------------------------------------------------
    def cope(self):
        items = [
            (r"Cope's EMI \ (Experiments in Musical Intelligence, \ from 1981): \ cut a composer's works into pieces, \ and put them back together differently", WHITE),
            (r"the pieces join where they connect: \ the last note of one leads by step to the first of the next", WHITE),
            (r"`signatures': \ patterns a composer repeats, \ kept whole", WHITE),
            (r"an analysis of each piece's role \ (opening, \ middle, \ cadence) \ decides where it may go", WHITE),
            (r"everything is copied; \ nothing is in that order anywhere", TUNE),
        ]
        rows_scene(self, r"recombinancy", items,
                   "David Cope's EMI took the opposite road. <bookmark mark='b'/> Cut a composer's works into pieces and put them back together differently. <bookmark mark='c'/> The pieces join where they connect: the last note of one leads by step to the first of the next. <bookmark mark='d'/> Patterns the composer repeats, which Cope called signatures, are kept whole. <bookmark mark='e'/> And an analysis of each piece's role, opening, middle or cadence, decides where it may go. <bookmark mark='f'/> The approach recombines learned material; the extent of literal copying and novelty depends on the implementation and source corpus.", marks="bcdef")

    # ------------------------------------------------------------------
    def heard(self):
        d = load("recombine")
        c = clip("recombined.one")
        roll = tune_roll(d["notes"], width=11.0, height=1.6).move_to(DOWN * 0.2)
        # colour each phrase by its source
        cols = [TUNE, BLUE, EAR, GREY_B]
        k, pi = 0, 0
        for b, (p, dd, f) in zip(roll.notes, d["notes"]):
            b.set_fill(cols[pi % 4])
            if f:
                pi += 1
        srcs = VGroup(*[label(rf"phrase {k + 1} of {bwv(n)}", font_size=16, color=cols[i]) for i, (n, k) in enumerate(d["sources"])]).arrange(RIGHT, buff=0.5).next_to(roll, DOWN, buff=0.45)
        head = label(r"four chorales, \ one tune", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        box = choice_boxes([r"a recombined chorale"], width=4.2, height=0.8, size=18).move_to(UP * 2.0)
        with self.voiceover("Monochord's recombiner takes an opening phrase from one chorale, two middle phrases from two others, and a closing phrase from a fourth, each joined to the next by a step, and Part 17 harmonizes the result."):
            self.play(FadeIn(head), FadeIn(box), FadeIn(roll), FadeIn(srcs))
        with self.listen(c) as snd:
            window(snd, r"recombined", kind="synthesized", detail=r"four chorales; \ Part 17's harmony", corner=DL, tag_corner=DR)
            pulse(snd, box, 0.0, c.duration, buff=0.06)
        res = label(rf"{100 * d['share8']:.0f}\% of its notes lie inside a run of 8 copied from one chorale; \ its longest run: \ {d['copy']['length']} notes, \ one whole phrase", font_size=17, color=EAR).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"It sounds like a chorale because every phrase is one: {say(round(100 * d['share8']))} per cent of its notes lie "
            f"inside a run of eight copied from a single chorale, and its longest copied run, {say(d['copy']['length'])} notes, "
            "is a whole phrase. Only the joins are new."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def questions(self):
        items = [
            (r"Cope's Bach-style chorales and inventions convinced listeners; \ his critics said the convincing parts were Bach's", WHITE),
            (r"Cope's answer: \ all composers recombine what they have heard; \ EMI only does it openly", WHITE),
            (r"both are partly right: \ style is largely recombination of shared patterns \ (Part 25, \ Part 26), \ and the order matters", WHITE),
            (r"for the law, \ the size of what is copied matters: \ a phrase of a living composer's song is not a cadence of Bach's", TUNE),
        ]
        rows_scene(self, r"is it composing?", items,
                   "Is it composing? <bookmark mark='b'/> Cope's chorales and inventions in Bach's style convinced listeners, and his critics said the convincing parts were Bach's. <bookmark mark='c'/> Cope answered that every composer recombines what they have heard, and that EMI only does it openly. <bookmark mark='d'/> Both are partly right: style is largely the recombination of shared patterns, as Parts 25 and 26 found for the Baroque and the Classical style, and the order is where the art is. <bookmark mark='e'/> For the law, protectable expression, substantial similarity and jurisdiction matter, alongside what and how much is copied: a phrase of a living songwriter's melody is not a stock cadence of Bach's.", marks="bcde")
