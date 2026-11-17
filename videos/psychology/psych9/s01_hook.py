from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.jims()
        self.strangers()
        self.design()
        self.objectives()

    def jims(self):
        b = archive.BOUCHARD_1990.data
        head = heading(rf"Ohio, {b['reunited']}: \ two men meet")
        left = VGroup(little_person(1.5, MZC), label(r"Jim", font_size=34, color=MZC)).arrange(DOWN, buff=0.15)
        right = VGroup(little_person(1.5, MZC), label(r"Jim", font_size=34, color=MZC)).arrange(DOWN, buff=0.15)
        left.move_to([-5.6, -0.2, 0])
        right.move_to([-2.9, -0.2, 0])
        gap = DashedLine(left.get_right() + RIGHT * 0.15, right.get_left() + LEFT * 0.15, color=GREY_B, stroke_width=3)
        years = label(rf"{b['age']} years apart", font_size=28, color=GREY_A).next_to(gap, UP, buff=0.15)
        rows = rows_of([
            (r"identical twins, \ adopted by different families as babies", WHITE),
            (r"both named James", MZC),
            (r"first wives: \ Linda and Linda. \ \ Second wives: \ Betty and Betty", MZC),
            (r"sons: \ James Alan and James Allan", MZC),
            (r"each had owned a dog called Toy", MZC),
            (r"a psychologist in Minnesota invites them to his laboratory: \ a twenty-year study begins", THRESH),
        ], 7.0, 30, 0.27).move_to([3.0, -0.2, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.BOUCHARD_1990.cite)
        tag = note(r"the coincidences: as the newspapers reported them").to_corner(DR, buff=0.2)
        with self.voiceover(
            f"In February {b['reunited']}, in Ohio, two men met for the first time since they were a few "
            "weeks old. They were identical twins, adopted by different families as babies, and they were "
            f"{b['age']}. <bookmark mark='a'/> Both had been named James by their new parents, so both "
            "were called Jim. <bookmark mark='b'/> As the newspapers told it, each had married a woman "
            "called Linda, divorced her, and then married a woman called Betty. <bookmark mark='c'/> One "
            "had a son called James Alan. The other had a son called James Allan. <bookmark mark='d'/> "
            "Each had owned a dog called Toy. <bookmark mark='e'/> A psychologist at the University of "
            "Minnesota, Thomas Bouchard, read about them and invited them to his laboratory. That was the "
            "beginning of a study of twins raised apart that ran for twenty years."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(left), FadeIn(right), Create(gap), FadeIn(years),
                      FadeIn(rows[0]))
            for mark_, r in zip("abcde", rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def strangers(self):
        c = load("coincide")
        head = heading(r"Two strangers, \ compared on two hundred things")
        g = np.random.default_rng(3)
        n, cols = c["items"], 20
        lit = g.random(n) < c["chance"]
        while lit.sum() != round(c["expected"]):      # the picture shows the expected number, placed at random
            lit = g.random(n) < c["chance"]
        cells = VGroup(*[Square(side_length=0.21, stroke_width=0, fill_color=THRESH if lit[i] else OWN,
                                fill_opacity=1.0 if lit[i] else 0.3) for i in range(n)])
        cells.arrange_in_grid(rows=n // cols, cols=cols, buff=0.05).move_to([-3.9, 0.9, 0])
        cap = label(rf"{n} things compared; \ {int(lit.sum())} match", font_size=28, color=GREY_A).next_to(cells, DOWN, buff=0.15)
        A = axes([0, 25], [0, 0.15], x_length=5.0, y_length=1.7, xticks=[0, 5, 10, 15, 20, 25], yticks=[],
                 xlabel=r"matches between two strangers", ylabel=r"", center=[-3.9, -2.25, 0])
        bars = VGroup(*[Rectangle(width=0.15, height=max(float(h) * 1.7 / 0.15, 0.005), stroke_width=0, fill_color=THRESH,
                                  fill_opacity=0.85).move_to(A.ax.c2p(k, 0), aligned_edge=DOWN)
                        for k, h in enumerate(c["hist"])])
        rows = rows_of([
            (r"nobody wrote down beforehand what would be compared", WHITE),
            (rf"two strangers, \ {n} comparisons, \ a 1 in {round(1 / c['chance'])} chance of a match on each", WHITE),
            (rf"on average {c['expected']:.0f} match; \ {pct(c['at_least_8'])} of pairs share eight or more", THRESH),
            (r"the newspaper prints the ten, \ not the hundred and ninety", BAD),
        ], 5.6, 30, 0.3).move_to([3.9, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated: 20{,}000 pairs of strangers; \ the chances are an illustration")
        with self.voiceover(
            "It's a wonderful story, and as evidence it's worth almost nothing. You know why, from Part 4. "
            "<bookmark mark='a'/> Nobody wrote down beforehand which things would be compared. The two men "
            "were compared on everything anyone could think of: names, wives, cars, cigarettes, hobbies, "
            "dogs. <bookmark mark='b'/> So take two strangers of the same age, from the same state. "
            f"Compare them on {n} things, and suppose each has a one in {round(1 / c['chance'])} chance "
            f"of matching. <bookmark mark='c'/> On average, {c['expected']:.0f} match. Among twenty "
            f"thousand simulated pairs of strangers, {100 * c['at_least_8']:.0f} percent share eight "
            "things or more. <bookmark mark='d'/> And the newspaper prints the ten that matched, not the "
            "hundred and ninety that didn't. This is the garden of forking paths again, with a "
            "human-interest headline. The chances here are an illustration, not an estimate. The point is "
            "the shape of the mistake."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cells, lag_ratio=0.002), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(cap))
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(bars, lag_ratio=0.03), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def design(self):
        b = archive.BOUCHARD_1990.data
        head = heading(r"Behind the anecdote, \ a design")
        lcard = VGroup(
            label(r"the anecdote", font_size=36, color=BAD),
            wrapped_label(r"one pair of twins; \ the things compared are chosen after looking", 5.4, 30, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-3.6, 1.6, 0])
        rcard = VGroup(
            label(r"the design", font_size=36, color=MODEL),
            wrapped_label(r"many pairs; \ one measure, fixed in advance; \ one number: the correlation between twin and "
                          r"twin", 5.6, 30, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, 1.6, 0])
        pairs = VGroup(*[twin_pair(MZC, True, 0.5) for _ in range(12)]).arrange_in_grid(rows=2, cols=6, buff=0.3)
        pairs.move_to([3.4, -0.6, 0])
        one = twin_pair(MZC, True, 0.9).move_to([-3.6, -0.5, 0])
        logic = wrapped_label(r"Identical twins raised in different homes share their genes, \ and not their home.", 12.4,
                              31, MZC).move_to([0, -1.85, 0])
        res = wrapped_label(rf"Minnesota, 1990: \ about {pct(b['iq_variance_genetic'])} of the variation in "
                            r"intelligence-test scores went with the genes", 12.4, 31, DATA).next_to(logic, DOWN, buff=0.22)
        src = published_tag(archive.BOUCHARD_1990.cite)
        with self.voiceover(
            "But behind the anecdote there's a design, and the design is one of the most repeated in "
            "psychology. <bookmark mark='a'/> Identical twins have the same genes. Raise them in different "
            "homes, and what they still share is their genes, and not their home. <bookmark mark='b'/> "
            "So measure many pairs, on one measure fixed in advance, and compute one number: the "
            "correlation between twin and twin. <bookmark mark='c'/> For scores on intelligence tests, the "
            f"Minnesota group reported in 1990 that about {100 * b['iq_variance_genetic']:.0f} percent of "
            "the variation went with the genes. <bookmark mark='d'/> That number has been attacked and "
            "defended ever since. This part is about what a number like it means, when it can be trusted, "
            "and what it can never tell you. The question sounds simple: how much of who you are did you "
            "inherit? The harder one is what that question means."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(lcard), FadeIn(one))
            vo.wait_until("a")
            self.play(FadeIn(logic, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(rcard), FadeIn(pairs, lag_ratio=0.08), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(res, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(Indicate(res, color=WHITE, scale_factor=1.03))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 9", font_size=34, color=GREY_B), label(r"Genes and Evolution", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"why families cannot separate genes from homes, \ and the designs that can",
            r"many small genes make a bell curve; \ the twin formula and its diagram",
            r"the twin design on the Pool: \ where it finds the truth, \ and four ways it fails",
            r"what heritability is not",
            r"the search for the genes: \ a failed decade, \ then a million tests",
            r"what a polygenic score can say about one person, \ and what evolution can say about us all",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part nine: genes and evolution. <bookmark mark='a'/> We'll see why families can't separate "
            "genes from homes, and meet the designs that can. <bookmark mark='b'/> We'll watch many small "
            "genes add up to a bell curve, derive the formula that twin studies use, and draw the first "
            "path diagram of the series. <bookmark mark='c'/> We'll run the twin design on the Pool, where "
            "we know the truth, and then break its assumptions one at a time. <bookmark mark='d'/> We'll "
            "list what heritability is not, which is longer than what it is. <bookmark mark='e'/> We'll "
            "follow the search for the genes themselves, through a decade of findings that weren't there, "
            "to a million tests at once. <bookmark mark='f'/> And we'll ask what a genetic score can say "
            "about one person, and what evolution can say about all of us."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark_, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
