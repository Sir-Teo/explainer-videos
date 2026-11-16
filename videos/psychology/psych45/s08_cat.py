from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Cat(VoiceoverScene):
    def construct(self):
        self.card()
        self.algorithm()
        self.compare()
        self.exposure()

    def card(self):
        card = chapter_card(7, r"Adaptive testing", r"Why ask everyone the same questions?",
                            lit={1982: r"Weiss", 2000: r"Wainer"}, part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter seven. Adaptive testing."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def algorithm(self):
        head = heading(r"Four steps, \ repeated")
        data = (
            (r"estimate", r"start at the population mean; \ after each answer, \ the posterior mean and SD (chapter 6)",
             MODEL),
            (r"choose", r"the unused item with the most information at the current estimate (chapter 5)", PERSON),
            (r"ask", r"one answer, \ right or wrong", WHITE),
            (r"stop", r"when the standard error is small enough, \ or the test is long enough", GOOD),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=19, width=2.4), wrapped_label(how, 9.4, 22, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.5, 0])
        foot = wrapped_label(r"each person gets their own test, \ but every score is on one scale, \ because the "
                             r"items were calibrated first: \ the payoff of chapter 3", 12.0, 22, YOU).move_to([0, -2.4, 0])
        with self.voiceover(
            "An adaptive test is four steps, repeated. <bookmark mark='a'/> Estimate: start at the population mean, "
            "and after each answer, update the posterior. <bookmark mark='b'/> Choose: the unused item with the most "
            "information at the current estimate. <bookmark mark='c'/> Ask it. <bookmark mark='d'/> And stop when the "
            "standard error is small enough, or the test is long enough. <bookmark mark='e'/> Each person gets their "
            "own test, but every score is on one scale, because the items were calibrated first. It's the payoff of "
            "Rasch's idea."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def compare(self):
        d = load("cat")
        head = heading(r"The same precision, \ half the items")
        A = axes([0, 62], [0, 0.75], x_length=5.6, y_length=3.4, xticks=[0, 10, 20, 30, 40, 50, 60], yticks=[0, 0.25, 0.5, 0.75],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"items given",
                 ylabel=r"error (RMSE)", center=[-3.3, 0.3, 0], font_size=13)
        best = VGroup(*[Dot(A.ax.c2p(k, e), radius=0.06, color=SYMP) for k, e in zip(d["lengths"], d["fixed_best"])])
        rand = VGroup(*[Dot(A.ax.c2p(k, e), radius=0.06, color=GREY_B) for k, e in zip(d["lengths"], d["fixed_rand"])])
        cat_ = Dot(A.ax.c2p(d["mean_items"], d["cat_rmse"]), radius=0.11, color=GOOD)
        cat_l = label(r"adaptive", font_size=15, color=GOOD).next_to(cat_, DOWN, buff=0.1)
        line = DashedLine(A.ax.c2p(0, d["cat_rmse"]), A.ax.c2p(62, d["cat_rmse"]), color=GOOD, stroke_width=1.5)
        key = VGroup(label(r"best fixed form", font_size=14, color=SYMP), label(r"random fixed form", font_size=14,
                                                                                 color=GREY_B)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.05)
        k_match = int(d["lengths"][np.argmax(d["fixed_best"] <= d["cat_rmse"] + 0.002)])
        rows = rows_of([
            (r"Psyche: \ 1{,}000 simulated people, \ a calibrated bank of 300 items", WHITE),
            (rf"the adaptive test stops at SE 0.3 after {d['mean_items']:.0f} items on average, \ with error "
             rf"{d['cat_rmse']:.2f}", GOOD),
            (rf"the best fixed form, \ built for the average person, \ needs about {k_match} items for the same error; "
             rf"\ a random one, \ even more", SYMP),
            (r"the saving is largest for people far from average, \ whom a fixed form measures worst", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.cat}, \ \texttt{irt.eap}; \ simulated bank and people")
        with self.voiceover(
            "How much does it save? <bookmark mark='a'/> Psyche gives a thousand simulated people a calibrated bank of "
            "three hundred items. <bookmark mark='b'/> The adaptive test stops after about seventeen items on average. "
            "<bookmark mark='c'/> The best fixed form, built for the average person, needs about thirty-five items for "
            "the same accuracy. A random fixed form needs even more. <bookmark mark='d'/> The saving is largest for "
            "people far from average, whom a fixed form measures worst."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(best), FadeIn(rand))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(cat_), FadeIn(cat_l), FadeIn(line))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def exposure(self):
        d = load("cat")
        head = heading(r"The costs")
        data = (
            (r"exposure", rf"the first item is the most informative at the mean, \ so everyone gets it: \ here "
                          rf"{100 * d['max_exposure']:.0f}\% of test-takers; \ shared online, \ it is no longer a "
                          rf"test item", AUTH),
            (r"control", r"choose at random among the few best items, \ or cap each item's rate (Sympson and "
                         r"Hetter's method)", MODEL),
            (r"content", r"a test must also cover its topics: \ the choice is constrained, \ not just most informative",
             SYMP),
            (r"calibration", r"a bank of hundreds of items, \ each pre-tested on enough people to know its curve", PERSON),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=18, width=2.6), wrapped_label(how, 9.4, 21, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "The costs. <bookmark mark='a'/> Exposure. The first item is the most informative at the mean, so "
            "everyone gets it. Here, every single test-taker. Shared online, it's no longer a test item. "
            "<bookmark mark='b'/> So real tests choose at random among the few best items, or cap each item's rate. "
            "<bookmark mark='c'/> A test must also cover its topics, so the choice is constrained. "
            "<bookmark mark='d'/> And it needs a bank of hundreds of items, each pre-tested on enough people to know "
            "its curve."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
