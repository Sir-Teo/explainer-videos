from __future__ import annotations

from videos.stats.stats55.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.hilbert()
        self.letter()
        self.format()
        self.map_demo()
        self.upgrade()
        self.objectives()

    def hilbert(self):
        tl = timeline(lit=(1900, 1933)).to_edge(UP, buff=0.35)
        hc = history_card(1900, r"David Hilbert, \ the International Congress of Mathematicians, \ Paris",
                          r"twenty-three problems to define the century's mathematics; \ the sixth asked for axioms for "
                          r"probability, \ and Kolmogorov answered it in 1933 \ (Part 43)",
                          color=PROBC, width=11.4, font_size=23).move_to([0, 1.1, 0])
        q = VGroup(
            label(r"``As long as a branch of science offers an abundance of problems,", font_size=27),
            label(r"so long is it alive.''", font_size=27, color=S.ACCENT),
            note(r"D. Hilbert, \ \emph{Mathematical Problems} \ (1900)"),
        ).arrange(DOWN, buff=0.2).move_to([0, -1.6, 0])
        with self.voiceover(
            "This part closes the PhD core, and like the comprehensive exam of Part forty-two, it introduces no new method. "
            "<bookmark mark='a'/> In August 1900, at the International Congress of Mathematicians in Paris, David Hilbert "
            "set out twenty-three problems that he hoped would shape the century's mathematics. The sixth asked for axioms "
            "for the theory of probability; Andrey Kolmogorov answered it in 1933, and Part forty-three began there. "
            "<bookmark mark='b'/> Hilbert's address opened with a sentence every doctoral student should know. As long as a "
            "branch of science offers an abundance of problems, <bookmark mark='c'/> so long is it alive."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(q[0]), FadeIn(q[2]))
            vo.wait_until("c")
            self.play(FadeIn(q[1]))
        self.clear_scene()

    def letter(self):
        m = memo([
            (r"Dear candidate,", WHITE),
            (r"your qualifying examination is tomorrow at nine: \ twelve problems, \ six hours.", GREY_A),
            (r"One problem from each part of the core, \ Parts 43 to 54.", GREY_A),
            (r"Show every step. \ A correct answer without its proof earns nothing.", WHITE),
            (r"--- the Graduate Committee", S.ACCENT),
        ], r"Department of Statistics \ \textbullet\ \ qualifying examination").move_to([0, -0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> It is the night before the qualifying exam. The letter on the desk says: your examination "
            "is tomorrow at nine. Twelve problems, six hours, one from each part of the core, Parts forty-three to "
            "fifty-four. <bookmark mark='b'/> And the line that matters: show every step. At this level, a correct answer "
            "without its proof earns nothing. The exam asks whether you can prove things, which is what research will ask "
            "of you every day."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(m[0]), FadeIn(m[1]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in m[2][:3]], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(m[2][3]), FadeIn(m[2][4]))
        self.clear_scene()

    def format(self):
        card = ExamCard(None, r"how the exam works", r"Parts 43--54",
                        [r"Each problem is posed on a card, \ with the part it draws on and its marks.",
                         r"The clock is your time: \ pause, \ prove it on paper, \ then watch the proof."],
                        marks=0, color=GREY_B).move_to([0, 2.0, 0])
        topics = [
            (r"1. \ Borel--Cantelli", 43, PROBC), (r"2. \ optional stopping", 44, PROBC), (r"3. \ a UMVUE, \ and none", 45, ESTC5),
            (r"4. \ Blyth's method", 45, ESTC5), (r"5. \ Neyman structure", 46, TESTC5), (r"6. \ LAN and local power", 47, TESTC5),
            (r"7. \ bracketing", 48, EMPC), (r"8. \ an influence function", 49, EMPC), (r"9. \ Fano", 50, HDC),
            (r"10. \ matrix Bernstein", 51, HDC), (r"11. \ the lasso's oracle", 52, BAYC), (r"12. \ a contraction rate", 53, BAYC),
        ]
        grid = VGroup(*[VGroup(label(t, font_size=24, color=c), label(rf"Part {p}", font_size=18, color=GREY_B)).arrange(DOWN, buff=0.08)
                        for t, p, c in topics])
        grid.arrange_in_grid(rows=3, cols=4, buff=(0.6, 0.35)).move_to([0, -1.3, 0])
        if grid.width > 12.6:
            grid.width = 12.6
        with self.voiceover(
            "<bookmark mark='a'/> Each problem is posed on a card like this one. <bookmark mark='b'/> The clock is your time "
            "to try it: pause the video, prove it on paper, then watch the proof. <bookmark mark='c'/> The twelve problems: "
            "a Borel–Cantelli argument and optional stopping from probability; a UMVUE and Blyth's method from estimation; "
            "Neyman structure and local asymptotic normality from testing and asymptotics; a bracketing bound and an "
            "influence function from empirical processes and efficiency; Fano's inequality and matrix Bernstein from minimax "
            "theory and high-dimensional probability; and the lasso's oracle inequality and a posterior contraction rate. "
            "Statistical learning theory, Part fifty-four, appears inside several of them."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(card.sweep(4.0))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in grid], lag_ratio=0.25), run_time=7.0)
        self.clear_scene()

    def map_demo(self):
        pm = ProofMap([(r"a tail bound \ for one $n$", 43), (r"sum it over $n$", 43), (r"Borel--Cantelli", 43),
                       (r"almost surely, \ eventually", 43)], color=PROBC).move_to([0, 0.4, 0])
        head = label(r"this part's instrument: \ the proof map", font_size=30, color=GREY_A).to_edge(UP, buff=0.6)
        foot = fit_rows(VGroup(
            label(r"each box: \ one move of the proof; \ beneath it, \ the part whose tool it uses", font_size=24, color=GREY_A),
            label(r"a qualifying exam tests whether the tools connect", font_size=24, color=PROOFC),
        ), 12.4, 0.3, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> This part's instrument is the proof map. After each solution, the proof is drawn as a "
            "chain of moves, <bookmark mark='b'/> each box one step of the argument, <bookmark mark='c'/> and beneath it the "
            "part of the course whose tool it uses. <bookmark mark='d'/> Some proofs stay inside one part. Most do not: the "
            "lasso's oracle inequality needs Part fifty-one's Gaussian maxima, and the contraction rate needs Part fifty's "
            "tests. <bookmark mark='e'/> That is what a qualifying exam really tests: whether the tools you learned one at a "
            "time connect."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pm.boxes), FadeIn(pm.texts), FadeIn(pm.arrows))
            vo.wait_until("b")
            self.play(pm.light(0), pm.light(1))
            vo.wait_until("c")
            self.play(FadeIn(pm.tags), FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(pm.light(2), pm.light(3))
            vo.wait_until("e")
            self.play(pm.done(), FadeIn(foot[1]))
        self.wait(0.5)
        self.clear_scene()

    def upgrade(self):
        cards = [
            upgrade_card(42, r"twelve problems: \ compute, \ fit, \ interpret", r"the methods are correct",
                         r"twelve problems: \ prove the methods are correct"),
            upgrade_card(54, r"twelve parts of PhD courses", r"each taken on its own",
                         r"one exam that needs all twelve at once"),
        ]
        VGroup(*cards).arrange(DOWN, buff=0.4).move_to([0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two promises come due. The comprehensive exam of Part forty-two asked you to compute, fit "
            "and interpret, and assumed the methods were correct. This exam asks you to prove that they are. <bookmark "
            "mark='b'/> And the PhD core was taught one part at a time. Tomorrow's exam needs all twelve at once."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 55", font_size=34, color=GREY_B), label(r"The Qualifying Exam", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"probability: \ Borel--Cantelli for maxima; \ optional stopping when it fails",
            r"estimation and testing: \ a UMVUE, \ Blyth's method, \ Snow's Table IX",
            r"asymptotics and efficiency: \ local power, \ brackets, \ Newcomb's median",
            r"high dimensions: \ Fano, \ matrix Bernstein, \ the lasso's oracle, \ a contraction rate",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 43--54").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.qual}, \ the PhD problem bank, \ the proof map").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-five: the qualifying exam. <bookmark mark='b'/> Twelve problems in six sittings: "
            "probability, with Borel–Cantelli for maxima and optional stopping where it fails; estimation and testing, with a "
            "UMVUE, Blyth's method, and Neyman structure applied to John Snow's cholera table; asymptotics and efficiency, "
            "with local power, a bracketing bound and the median's influence function on Newcomb's measurements of the speed "
            "of light; and high dimensions, with Fano's inequality, matrix Bernstein, the lasso's oracle inequality and a "
            "posterior contraction rate."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
