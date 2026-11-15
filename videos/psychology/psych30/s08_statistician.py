from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Statistician(VoiceoverScene):
    def construct(self):
        self.card()
        self.balls()
        self.debate()

    def card(self):
        card = chapter_card(7, r"Born knowing, \ or built?", r"Is the infant a statistician?",
                            lit={1990: r"Spelke", 2008: r"Xu \& Garcia", 2012: r"Xu \& Kushnir"},
                            part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter seven. Born knowing, or built?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def balls(self):
        d = load("statistics")
        head = heading(r"Eight months, \ and a box of balls")
        rng = np.random.default_rng(3)
        box = Rectangle(width=3.2, height=2.4, color=GREY_B, stroke_width=3).move_to([-3.8, 1.0, 0])
        pts = rng.uniform([-5.2, 0.0], [-2.4, 2.0], size=(60, 2))
        balls = VGroup(*[Dot([x, y, 0], radius=0.09, color=(LOST if i < 6 else WHITE)) for i, (x, y) in
                         enumerate(pts)])
        def sample(nr, y):
            g = VGroup(*[Dot([0, 0, 0], radius=0.12, color=(LOST if j < nr else WHITE)) for j in range(5)])
            return g.arrange(RIGHT, buff=0.15).move_to([-3.8, y, 0])
        s1 = sample(4, -1.0)
        s2 = sample(1, -2.0)
        l1 = label(rf"$p = {d['mostly_red_p']:.4f}$", font_size=18, color=LOST).next_to(s1, RIGHT, buff=0.3)
        l2 = label(rf"$p = {d['mostly_white_p']:.2f}$", font_size=18, color=WHITE).next_to(s2, RIGHT, buff=0.3)
        rows = rows_of([
            (r"Fei Xu and Vashti Garcia, \ 2008: \ a box is shown to be mostly white balls; \ an experimenter, "
             r"\ eyes closed, \ draws five", WHITE),
            (r"8-month-olds looked longer when the sample was four red and one white than four white and one red",
             LOST),
            (rf"with nine in ten white \ (illustrative), \ the first sample is {d['ratio']:.0f} times less "
             rf"probable: \ {d['mostly_red_bits']:.1f} bits of surprise against {d['mostly_white_bits']:.1f}", MODEL),
            (r"infants seem to reason from a population to a sample, \ and back: \ intuitive statistics", GOOD),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Xu \& Garcia (2008)")
        with self.voiceover(
            "A third view says infants are neither born with the answers nor blank. They are learners with good "
            "statistical tools. <bookmark mark='a'/> In 2008 Fei Xu and Vashti Garcia showed eight-month-olds a box "
            "of mostly white balls. An experimenter, eyes closed, drew five. <bookmark mark='b'/> Infants looked "
            "longer when the sample was four red and one white than when it was four white and one red. "
            "<bookmark mark='c'/> With nine white balls in ten, which is an illustrative share, the first sample is "
            f"about {d['ratio']:.0f} times less probable than the second: {d['mostly_red_bits']:.1f} bits of surprise "
            f"against {d['mostly_white_bits']:.1f}. <bookmark mark='d'/> Infants seem to reason from a population to "
            "a sample, and, in other experiments in the same paper, from a sample back to the population: intuitive "
            "statistics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(box), FadeIn(balls))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(s1), FadeIn(s2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(l1), FadeIn(l2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def debate(self):
        head = heading(r"Three views, \ at their best")
        cols = VGroup()
        for name, col, pts in (
                (r"core knowledge", OBJ, [r"a few innate systems: \ objects, \ number, \ agents, \ places",
                                          r"shown early, \ across cultures, \ and in other animals",
                                          r"best evidence: \ newborn chicks and young infants share expectations "
                                          r"about objects"]),
                (r"constructivism", LOOK, [r"Piaget, \ and its modern forms: \ knowledge built from action and "
                                           r"experience", r"looking studies read too much into a long look",
                                           r"best evidence: \ lean explanations for many looking results; \ "
                                           r"knowledge that grows gradually"]),
                (r"rational constructivism", NUM, [r"Xu, \ Gopnik and others: \ innate learning mechanisms, \ "
                                                   r"Bayesian in spirit, \ and some starting concepts",
                                                   r"infants as scientists: \ sampling, \ testing, \ revising",
                                                   r"best evidence: \ infants use probabilities, \ and learn "
                                                   r"from data in the laboratory"])):
            box = VGroup(label(name, font_size=24, color=col),
                         *[wrapped_label(p, 3.7, 18, WHITE) for p in pts]).arrange(DOWN, buff=0.25)
            cols.add(box)
        cols.arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to([0, 0.2, 0])
        foot = wrapped_label(r"each view predicts something the others do not: \ which is the test", 12.0, 22,
                             GREY_A).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Spelke \& Kinzler (2007); \ Xu \& Kushnir (2012)")
        with self.voiceover(
            "So there are three views. <bookmark mark='a'/> Core knowledge: a few innate systems, for objects, "
            "number, agents and places, shown early, across cultures, and in other animals. "
            "<bookmark mark='b'/> Constructivism, Piaget's view and its modern forms: knowledge is built from action "
            "and experience, and looking studies read too much into a long look. <bookmark mark='c'/> And rational "
            "constructivism, from Fei Xu, Alison Gopnik and others: infants come with powerful learning mechanisms, "
            "Bayesian in spirit, and a few starting concepts, and they behave like small scientists. "
            "<bookmark mark='d'/> Each view predicts something the others don't, and that's where the tests are."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
