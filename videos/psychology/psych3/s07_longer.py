from __future__ import annotations

from videos.psychology.psych3.common import *  # noqa: F403


class Longer(VoiceoverScene):
    def construct(self):
        self.card()
        self.spearman_brown()
        self.alpha()
        self.which_error()
        self.built()

    def card(self):
        card = chapter_card(6, r"Longer tests are better tests", r"How many questions does it take?",
                            lit={1910: r"the Spearman--Brown formula", 1951: r"Cronbach's alpha"}, part=PART,
                            scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter six. Longer tests are better tests."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def spearman_brown(self):
        d = load("longer")
        head = heading(r"Why adding questions helps, and by how much")
        steps = VGroup(
            wrapped_label(r"Add up $k$ questions. \ The true parts agree, so they pile up:", 5.6, 27, WHITE),
            label(r"true variance $\times\, k^2$", font_size=34, color=TRUE),
            wrapped_label(r"The errors are unrelated, so they partly cancel:", 5.6, 27, WHITE),
            label(r"error variance $\times\, k$", font_size=34, color=ERRC),
            label(r"$r_k \;=\; \dfrac{k\, r}{1 + (k - 1)\, r}$", font_size=44, color=P.ACCENT),
        ).arrange(DOWN, buff=0.22).move_to([-3.85, -0.35, 0])
        A = axes([0, 41], [0, 1.0], x_length=6.4, y_length=4.2, xticks=[1, 10, 20, 30, 40],
                 yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], xlabel=r"number of questions", ylabel=r"reliability",
                 center=[3.4, -0.45, 0])
        ax = A.ax
        line = curve(ax, d["curve_k"], d["curve"], P.ACCENT, stroke_width=4)
        dots = VGroup(*[Dot(ax.c2p(k, r), radius=0.07, color=WHITE) for k, r in zip(d["lengths"], d["simulated"])])
        i10 = d["lengths"].index(10)
        one = label(rf"1 question: \ {r2(d['one_item'])}", font_size=24, color=GREY_A)
        one.next_to(ax.c2p(1, d["one_item"]), RIGHT, buff=0.2)
        ten = label(rf"10: \ {r2(d['simulated'][i10])}", font_size=24, color=WHITE)
        ten.next_to(ax.c2p(10, d["simulated"][i10]), DOWN, buff=0.25).shift(RIGHT * 0.5)
        k90 = int(-(-d["for_90"] // 1))
        ninety = label(rf"{r2(0.9)} needs {k90}", font_size=24, color=WHITE)
        ninety.next_to(ax.c2p(k90, 0.9), DOWN, buff=0.25).shift(RIGHT * 0.9)
        leg = legend([(P.ACCENT, r"the formula"), (WHITE, r"measured on the Pool")], font_size=22)
        leg.next_to(A, UP, buff=0.05).shift(RIGHT * 0.6)
        tag = simulated_tag()
        with self.voiceover(
            "If a short test is noisy, the remedy is the obvious one: ask more questions. What's worth knowing is "
            "exactly how much that buys, and Spearman worked it out in 1910, at the same time as a psychologist "
            "named William Brown. <bookmark mark='a'/> Add up k questions that all measure the same thing. Their "
            "true parts agree with one another, so they pile up, and the true variance grows as k squared. "
            "<bookmark mark='b'/> Their errors are unrelated, so they partly cancel, and the error variance "
            "grows only as k. <bookmark mark='c'/> Put those into the definition of reliability and you get the "
            "Spearman-Brown formula. <bookmark mark='d'/> Here it is against the Pool. One question, answered on "
            f"a five-point scale, has a reliability of {d['one_item']:.2f}: mostly noise. Ten questions reach "
            f"{d['simulated'][i10]:.2f}. <bookmark mark='e'/> And then it gets expensive. To reach "
            f"point nine you need {k90}. The curve explains why a single question is a poor measure of a person, "
            "why a decent questionnaire has ten or twenty items, and why nobody writes one with two hundred."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            self.play(FadeIn(dots[0], scale=1.5), FadeIn(one))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(steps[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(steps[2]), FadeIn(steps[3], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(steps[4], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(Create(line), FadeIn(leg), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(p_, scale=1.5) for p_ in dots[1:]], lag_ratio=0.2), FadeIn(ten),
                      run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(ninety))
        self.clear_scene()

    def alpha(self):
        d = load("longer")
        a = d["alpha"]
        head = heading(r"Cronbach's alpha: \ reliability from a single sitting")
        formula = label(r"$\alpha \;=\; \dfrac{k}{k - 1}\left(1 - \dfrac{\text{sum of the item variances}}"
                        r"{\text{variance of the total}}\right)$", font_size=36, color=P.ACCENT).move_to([0, 1.95, 0])

        def tile(title, big, small, color, verdict):
            t = wrapped_label(title, 3.6, 26, WHITE)
            b = label(big, font_size=52, color=color)
            s_ = wrapped_label(small, 3.6, 24, GREY_A)
            v = wrapped_label(verdict, 3.6, 25, color)
            body = VGroup(t, b, s_, v).arrange(DOWN, buff=0.2)
            box = panel(4.1, 3.6, color=color)
            body.move_to(box)
            return VGroup(box, body)

        tiles = VGroup(
            tile(r"ten questions, all equally good", rf"$\alpha = {r2(a['equal']['alpha'])}$",
                 rf"true reliability {r2(a['equal']['truth'])}", TRUE, r"it is the reliability"),
            tile(r"ten questions, some better than others", rf"$\alpha = {r2(a['unequal']['alpha'])}$",
                 rf"true reliability {r2(a['unequal']['truth'])}", SCALE["interval"], r"it is a lower bound"),
            tile(r"twenty questions about two unrelated traits", rf"$\alpha = {r2(a['two_traits']['alpha'])}$",
                 rf"the two halves correlate {r2(a['two_traits']['halves_r'])}", ERRC,
                 r"it does not show that one thing is being measured"),
        ).arrange(RIGHT, buff=0.35).move_to([0, -1.2, 0])
        tag = simulated_tag()
        with self.voiceover(
            "In practice you rarely have a second form of the test. You have one questionnaire, filled in once. "
            "In 1951 Lee Cronbach showed how to get a reliability out of that. <bookmark mark='a'/> Treat every "
            "question as a tiny test of its own. If the questions measure the same thing they'll agree, and the "
            "total will vary far more than the separate questions would by themselves. Alpha compares the two. "
            "It's the most reported statistic in psychology, and it's worth knowing three things about it. "
            f"<bookmark mark='b'/> When the questions are equally good, alpha is the reliability: "
            f"{a['equal']['alpha']:.2f} here, and the truth is the same. <bookmark mark='c'/> When some questions "
            "are better than others, alpha comes out a little low. It's a lower bound. <bookmark mark='d'/> And "
            "the third is the one people get wrong. Take ten questions about conscientiousness and ten about "
            f"extraversion, which have almost nothing to do with each other, and call it one test. Alpha is "
            f"{a['two_traits']['alpha']:.2f}. A high alpha doesn't show that a test measures one thing. It "
            "shows that the test is long and that some of its questions agree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.wait(2.0)
            self.play(FadeIn(formula, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(Indicate(formula, color=WHITE, scale_factor=1.05))
            for m, t in zip("bcd", tiles):
                vo.wait_until(m)
                self.play(FadeIn(t, shift=UP * 0.2))
        self.clear_scene()

    def which_error(self):
        d = load("longer")
        m, k = d["mood"], d["kappa"]
        head = heading(r"Reliable against what? \ Error has more than one source")
        left = VGroup(
            label(r"the day", font_size=34, color=GROUP_A),
            wrapped_label(r"a mood colours every answer on the day you fill it in", 5.4, 26, GREY_A),
            label(rf"alpha, from one sitting: \ {r2(m['alpha'])}", font_size=30, color=WHITE),
            label(rf"the same people a month later: \ {r2(m['retest'])}", font_size=30, color=GROUP_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-3.5, 0.75, 0])
        # 100 cases judged by two raters
        both_yes, split = round(100 * k["both_yes"]), round(100 * k["split"])
        cols = [P.ACCENT] * both_yes + [ERRC] * split + ["#3A4150"] * (100 - both_yes - split)
        grid = VGroup(*[Square(0.2, stroke_width=0, fill_color=c, fill_opacity=1) for c in cols])
        grid.arrange_in_grid(rows=5, cols=20, buff=0.05)
        right = VGroup(
            label(r"the judge", font_size=34, color=GROUP_B),
            wrapped_label(r"two clinicians, a diagnosis present in 1 case in 20", 5.6, 26, GREY_A),
            grid,
            label(rf"they agree on {100 * k['agreement']:.0f} cases in 100", font_size=30, color=WHITE),
            label(rf"agreement beyond chance, kappa: \ {r2(k['kappa'])}", font_size=30, color=GROUP_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.5, 0.45, 0])
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=1), label(t, font_size=20, color=GREY_A))
                       .arrange(RIGHT, buff=0.1) for c, t in ((P.ACCENT, r"both say yes"), (ERRC, r"they differ"),
                                                             ("#3A4150", r"both say no"))]).arrange(RIGHT, buff=0.4)
        key.next_to(grid, DOWN, buff=0.1).align_to(grid, LEFT)
        right[3:].shift(DOWN * 0.3)
        end = label(r"A reliability coefficient always answers: \ consistent across what? \ Items, days, or judges.",
                    font_size=28, color=P.ACCENT).to_edge(DOWN, buff=0.6)
        tag = simulated_tag()
        with self.voiceover(
            "Now a complication that the single word reliability hides. Error isn't one thing. "
            "<bookmark mark='a'/> Suppose your mood on the day colours every answer you give. Within that "
            f"sitting the answers agree beautifully, and alpha is {m['alpha']:.2f}. <bookmark mark='b'/> Test "
            f"the same people a month later, in other moods, and the two totals correlate {m['retest']:.2f}. "
            "Alpha counted the mood as true score, because it was shared by every item. A retest doesn't. "
            "<bookmark mark='c'/> Or take scores that come from a judge. Two clinicians each decide whether a "
            f"rare condition is present. They agree on {100 * k['agreement']:.0f} cases in a hundred, which "
            "sounds excellent. <bookmark mark='d'/> But almost all of that agreement is on the cases where both "
            "say no, which they'd mostly do by chance. Cohen's kappa asks how much better than chance they agree, "
            f"and the answer is {k['kappa']:.2f}. <bookmark mark='e'/> So never accept a reliability without "
            "asking: consistent across what? Across questions, across days, or across judges. They're different "
            "numbers, and the one that matters depends on what you're going to do with the score."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left[0]), FadeIn(left[1]), FadeIn(left[2]))
            vo.wait_until("b")
            self.play(FadeIn(left[3], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(right[0]), FadeIn(right[1]), FadeIn(grid, lag_ratio=0.01), FadeIn(key), FadeIn(right[3]))
            vo.wait_until("d")
            self.play(FadeIn(right[4], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.15))
        self.clear_scene()

    def built(self):
        d = load("longer")
        att = load("attenuation")
        i6 = att["lengths"].index(6)
        head = heading(r"What this part builds: \ a test-score laboratory")
        code = code_block([
            r"from explainer.psychology import measure, pool",
            r"P = pool.Pool()\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \# 100,000 simulated people",
            r"x = P.items('conscientious', ids, k=10)\ \ \ \ \ \ \# their answers, 1 to 5",
            rf"measure.cronbach\_alpha(x)\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \# {d['alpha']['equal']['alpha']:.2f}",
            rf"measure.spearman\_brown({d['one_item']:.2f}, 10)\ \ \ \ \ \ \ \ \ \ \ \ \ \# "
            rf"{d['one_item'] * 10 / (1 + 9 * d['one_item']):.2f}",
            rf"measure.disattenuate({att['observed'][i6]:.2f}, {att['reliabilities'][i6]:.2f}, "
            rf"{att['reliabilities'][i6]:.2f})\ \ \ \ \ \ \# {att['corrected'][i6]:.2f}",
        ], font_size=27).move_to([0, 0.35, 0])
        cap = wrapped_label(r"Each simulated person carries their true values, so every estimator in this part can be "
                            r"marked against the truth. \ Real data never allow that; \ it is what the Pool is for.",
                            11.5, 28, GREY_A).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "Everything in the last three chapters runs in a few lines, and it's what this part adds to the "
            "series' library. <bookmark mark='a'/> The Pool now holds traits, and questionnaires that measure "
            "them with error. The measurement module holds the estimators: alpha, Spearman-Brown, the correction "
            "for attenuation, and the rest. <bookmark mark='b'/> Because each simulated person carries their true "
            "values, every one of those estimators can be marked against the truth. Real data never let you do "
            "that. It's the reason the series has a Pool at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in code.rows], lag_ratio=0.3),
                      run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.clear_scene()
