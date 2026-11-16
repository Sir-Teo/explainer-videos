from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Crossed(VoiceoverScene):
    def construct(self):
        self.card()
        self.items()
        self.maximal()
        self.slopes()

    def card(self):
        card = chapter_card(4, r"Participants and items, \ crossed", r"What varies, \ and what should the test know?",
                            lit={1973: r"Clark", 2013: r"Barr et al."}, part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter four. Participants and items, crossed."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def items(self):
        d = load("example")
        head = heading(r"Why the by-participant test fails")
        A = axes([0, 21], [-1, 1], x_length=6.0, y_length=3.0, xticks=[1, 10, 11, 20], yticks=[-0.5, 0, 0.5],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"word", ylabel=r"word's mean",
                 center=[-3.0, 0.3, 0], font_size=13)
        dots = VGroup(*[Dot(A.ax.c2p(j + 1, m), radius=0.08, color=GOOD if c else SYMP)
                        for j, (m, c) in enumerate(zip(d["item_means"], d["item_cond"]))])
        key = VGroup(label(r"related primes", font_size=13, color=GOOD), label(r"unrelated primes", font_size=13,
                                                                                color=SYMP)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"words differ: \ some are easy, \ some hard; \ ten words are in each condition", WHITE),
            (r"every participant sees the same twenty words, \ so the words' quirks are shared by every person's "
             r"average", AUTH),
            (r"the by-participant test sees thirty agreeing people, \ and mistakes the words' quirks for an effect", AUTH),
            (r"a model with random effects for participants and items knows there are only ten words a side: \ the "
             r"test that matters has about 18 degrees of freedom, \ not 29", GOOD),
        ], 5.6, 19, 0.38).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.priming\_study}, \ one simulated study")
        with self.voiceover(
            "Why does the by-participant test fail? <bookmark mark='a'/> Words differ: some are easy, some hard, and "
            "there are only ten in each condition. <bookmark mark='b'/> Every participant sees the same twenty words, "
            "so the words' quirks are in every person's average. <bookmark mark='c'/> The by-participant test sees "
            "thirty people who agree, and mistakes the words' quirks for an effect. <bookmark mark='d'/> A model with "
            "random effects for both participants and items knows there are only ten words a side. The test that "
            "matters has about eighteen degrees of freedom, not twenty-nine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key), FadeIn(dots))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def maximal(self):
        head = heading(r"How much structure?")
        data = (
            (r"min F$'$", r"Clark's 1973 remedy: \ combine the by-participant and by-item tests; \ slightly "
                          r"conservative, \ and still useful", SYMP),
            (r"crossed model", r"random intercepts for participants and items, \ fitted together (Baayen, \ Davidson "
                               r"and Bates, \ 2008)", MODEL),
            (r"keep it maximal", r"Barr and colleagues, \ 2013: \ include every random slope the design allows, \ or "
                                 r"error rates rise again", PERSON),
            (r"or parsimonious", r"Matuschek and colleagues, \ 2017: \ maximal models lose power and often fail to "
                                 r"converge; \ simplify by evidence, \ not by habit", GOOD),
            (r"convergence", r"a model that will not converge is saying the data cannot estimate what was asked", AUTH),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=17, width=3.0), wrapped_label(how, 9.2, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.3, 0])
        tag = published_tag(r"Baayen, Davidson \& Bates (2008); \ Barr et al. (2013); \ Matuschek et al. (2017)")
        with self.voiceover(
            "How much structure should the model have? <bookmark mark='a'/> Clark's own remedy combined the "
            "by-participant and by-item tests into one, slightly conservative. <bookmark mark='b'/> Crossed mixed "
            "models fit random effects for participants and items together, as Harald Baayen, Douglas Davidson and "
            "Douglas Bates showed in 2008. <bookmark mark='c'/> Dale Barr and colleagues argued in 2013: keep it "
            "maximal. Include every random slope the design allows, or error rates rise again. "
            "<bookmark mark='d'/> Hannes Matuschek and colleagues replied in 2017 that maximal models lose power and "
            "often fail to converge. Simplify by evidence, not habit. <bookmark mark='e'/> And a model that won't "
            "converge is saying the data can't estimate what was asked."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def slopes(self):
        d = load("slopefpr")
        head = heading(r"When people differ in the effect")
        A = axes([0.3, 3.7], [0, 0.2], x_length=4.6, y_length=3.0, xticks=None, yticks=[0, 0.05, 0.1, 0.15],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"false positives", center=[-3.6, 0.3, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3], [d["F1"], d["F2"], d["minF"]], [AUTH, AUTH, GOOD], width=0.6)
        five = DashedLine(A.ax.c2p(0.3, 0.05), A.ax.c2p(3.7, 0.05), color=GREY_B, stroke_width=1.5)
        names = VGroup(*[wrapped_label(t, 1.4, 12, c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, (t, c) in
                         enumerate(((r"by participants", AUTH), (r"by items", AUTH), (r"both random", GOOD)))])
        rows = rows_of([
            (r"now the words barely differ, \ but participants differ in the effect itself: \ for some it is "
             r"positive, \ for others negative, \ on average zero", WHITE),
            (rf"the by-item test now fails: \ {100 * d['F2']:.0f}\% false positives; \ and the by-participant test "
             rf"is not safe either: \ {100 * d['F1']:.0f}\%", AUTH),
            (rf"treating both as random holds the line: \ {100 * d['minF']:.0f}\%", GOOD),
            (r"the argument for keeping random slopes: \ every source of variation the design allows must be in "
             r"the test", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.false\_positive\_rates}, \ 200 simulated studies")
        with self.voiceover(
            "The danger runs both ways. <bookmark mark='a'/> Now the words barely differ, but participants differ in "
            "the effect itself: positive for some, negative for others, zero on average. <bookmark mark='b'/> The "
            "by-item test now fails, at about twelve percent false positives, and the by-participant test isn't safe "
            "either. <bookmark mark='c'/> Treating both as random holds the line. <bookmark mark='d'/> That's the "
            "argument for keeping random slopes: every source of variation the design allows must be in the test."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(five))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]), FadeIn(b[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
