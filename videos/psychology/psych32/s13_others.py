from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403


class Others(VoiceoverScene):
    def construct(self):
        self.card()
        self.multiple()
        self.emotional()
        self.mozart()

    def card(self):
        card = chapter_card(12, r"Other intelligences", r"Are there kinds of intelligence the tests miss?",
                            lit={1983: r"Gardner", 1993: r"Rauscher et al.", 2006: r"Visser et al."}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter twelve. Other intelligences."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def multiple(self):
        head = heading(r"Multiple intelligences")
        names = [r"linguistic", r"logical-mathematical", r"spatial", r"musical", r"bodily-kinesthetic",
                 r"interpersonal", r"intrapersonal", r"naturalist \ (1999)"]
        chips = VGroup(*[word_chip(n, color=VERB if i < 7 else GREY_B, font_size=19, width=3.4)
                         for i, n in enumerate(names)])
        chips.arrange_in_grid(rows=4, cols=2, buff=(0.25, 0.22)).move_to([-3.4, -0.2, 0])
        rows = rows_of([
            (r"Howard Gardner, \ 1983, \ \emph{Frames of Mind}: \ seven separate intelligences, \ an eighth added in "
             r"1999; \ widely taught in schools", WHITE),
            (r"Part 3's test: \ do measures of them form separate factors, \ with their own validity?", MODEL),
            (r"Beth Visser, \ Michael Ashton and Philip Vernon, \ 2006: \ tests of the eight domains showed a "
             r"positive manifold and a large general factor; \ the purely cognitive ones loaded on it most, \ the "
             r"bodily and musical ones least", G),
            (r"as a list of talents worth teaching, \ useful; \ as a claim of independent intelligences, \ not "
             r"supported", LOST),
        ], 5.8, 21, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Visser, \ Ashton \& Vernon (2006)")
        with self.voiceover(
            "Is there more to intelligence than g? <bookmark mark='a'/> In 1983, in Frames of Mind, Howard Gardner "
            "proposed seven separate intelligences, and added an eighth, the naturalist, in 1999. The idea is widely "
            "taught in schools. <bookmark mark='b'/> Part 3's question applies: do measures of them form separate "
            "factors, each with its own validity? <bookmark mark='c'/> In 2006 Beth Visser, Michael Ashton and "
            "Philip Vernon gave tests of all eight domains to the same people. They found a positive manifold and a "
            "large general factor. The purely cognitive tests loaded on it most, the bodily and musical ones least. "
            "<bookmark mark='d'/> As a list of talents worth teaching, the theory is useful. As a claim of "
            "independent intelligences, it isn't supported."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in chips], lag_ratio=0.15), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def emotional(self):
        head = heading(r"Emotional intelligence")
        rows = rows_of([
            (r"two kinds of measure share one name: \ ability tests, \ which score answers to emotional problems "
             r"against a key, \ and self-reports, \ which ask people to rate themselves", WHITE),
            (r"the self-report versions overlap heavily with the personality traits of Part 33; \ the ability "
             r"versions overlap with ordinary cognitive ability", VERB),
            (r"Part 3's standards: \ a new construct needs reliability, \ discriminant validity from what we "
             r"already measure, \ and incremental validity in prediction", MODEL),
            (r"emotion understanding is real and learnable; \ whether it is a separate intelligence is still argued",
             YOU),
        ], 12.4, 22, 0.32).move_to([0, -1.75, 0])
        pairs = VGroup()
        for x, a, b_, col in ((-3.4, r"ability tests of EI", r"cognitive ability", G),
                              (3.4, r"self-reports of EI", r"personality traits \ (Part 33)", VERB)):
            ca = word_chip(a, color=col, font_size=22, width=3.6).move_to([x, 2.0, 0])
            cb = word_chip(b_, color=GREY_B, font_size=22, width=3.6).move_to([x, 0.6, 0])
            ar = Arrow(ca.get_bottom(), cb.get_top(), buff=0.08, color=col, stroke_width=4)
            pairs.add(VGroup(ca, ar, cb, label(r"overlaps with", font_size=16, color=GREY_A).next_to(ar, RIGHT,
                                                                                                    buff=0.1)))
        with self.voiceover(
            "Emotional intelligence is the most popular candidate. <bookmark mark='a'/> Two kinds of measure share "
            "the name. Ability tests score people's answers to emotional problems against a key; self-reports ask "
            "people to rate themselves. <bookmark mark='b'/> The self-report versions overlap heavily with the "
            "personality traits of Part 33, and the ability versions with ordinary cognitive ability. "
            "<bookmark mark='c'/> Part 3's standards apply. A new construct needs reliability, discriminant validity "
            "from what we already measure, and incremental validity in prediction. <bookmark mark='d'/> "
            "Understanding emotions is real, and learnable. Whether it's a separate intelligence is still argued."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), *[FadeIn(p_[0]) for p_ in pairs])
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[FadeIn(p_[1:]) for p_ in pairs])
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def mozart(self):
        head = heading(r"The Mozart effect")
        rows = rows_of([
            (r"Frances Rauscher, \ Gordon Shaw and Katherine Ky, \ 1993, \ in \emph{Nature}: \ students who listened "
             r"to a Mozart sonata did better on a spatial reasoning task for a short time afterwards", WHITE),
            (r"within a few years: \ CDs for babies, \ and a US state that proposed giving every newborn classical "
             r"music", G),
            (r"Rauscher said from the start that the effect was brief and spatial, \ not a rise in general "
             r"intelligence", VERB),
            (r"Jakob Pietschnig, \ Martin Voracek and Anton Formann, \ 2010: \ about 40 studies, \ more than 3{,}000 "
             r"people: \ a small effect against silence or no stimulus, \ varying by laboratory, \ and little evidence "
             r"of anything specific to Mozart", LOST),
        ], 12.4, 22, 0.3).move_to([0, -1.6, 0])
        A = axes([-0.2, 0.8], [0, 1], x_length=7.0, y_length=1.2, xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"effect on spatial tasks, \ $d$", center=[0, 1.75, 0], font_size=14)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, 1), color=GREY_B, stroke_width=2)
        ci = VGroup(Line(A.ax.c2p(0.23, 0.5), A.ax.c2p(0.52, 0.5), color=LOST, stroke_width=6),
                    Dot(A.ax.c2p(0.37, 0.5), radius=0.09, color=LOST),
                    label(r"Mozart against no stimulus: \ $d = 0.37$ \ [0.23, \ 0.52]", font_size=17, color=LOST)
                    .next_to(A.ax.c2p(0.52, 0.5), RIGHT, buff=0.2))
        tag = published_tag(r"Rauscher et al.\ (1993); \ Pietschnig et al.\ (2010)")
        with self.voiceover(
            "And then there's the shortest-lived intelligence of all. <bookmark mark='a'/> In 1993, in Nature, "
            "Frances Rauscher, Gordon Shaw and Katherine Ky reported that students who listened to a Mozart sonata "
            "did better on a spatial reasoning task for a short time afterwards. <bookmark mark='b'/> Within a few "
            "years there were CDs for babies, and an American state proposed giving every newborn a recording of "
            "classical music. <bookmark mark='c'/> Rauscher said from the start that the effect was brief and "
            "spatial, not a rise in general intelligence. <bookmark mark='d'/> In 2010 Jakob Pietschnig, Martin "
            "Voracek and Anton Formann pooled about forty studies with more than three thousand people. They found "
            "a small effect compared with silence or no stimulus, varying by laboratory, and little evidence of "
            "anything specific to Mozart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(A), Create(zero), FadeIn(ci), FadeIn(rows[3], shift=RIGHT * 0.15))
        self.clear_scene()
