from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403


def car(color, facing=1) -> VGroup:
    body = RoundedRectangle(corner_radius=0.12, width=1.6, height=0.45, fill_color=color, fill_opacity=0.9,
                            stroke_width=0)
    cab = RoundedRectangle(corner_radius=0.1, width=0.8, height=0.35, fill_color=color, fill_opacity=0.7,
                           stroke_width=0).next_to(body, UP, buff=0).shift(LEFT * 0.15 * facing)
    wheels = VGroup(*[Circle(radius=0.15, fill_color=GREY_D, fill_opacity=1, stroke_color=GREY_B,
                             stroke_width=2).move_to(body.get_bottom() + RIGHT * dx) for dx in (-0.5, 0.5)])
    return VGroup(body, cab, wheels)


class Hook(VoiceoverScene):
    def construct(self):
        self.crash()
        self.glass()
        self.your_list()
        self.your_test()
        self.question()
        self.objectives()

    def crash(self):
        lp = archive.LOFTUS_PALMER_1974.data
        road = Line([-6.2, 1.2, 0], [6.2, 1.2, 0], color=GREY_C, stroke_width=3)
        a, b = car(CTX, 1).move_to([-5.0, 1.65, 0]), car(TRACE, -1).move_to([5.0, 1.65, 0])
        q = MathTex(r"\text{About how fast were the cars going when they}", r"\;\underline{\text{\ \ \ \ \ \ \ \ \ \ }}\;",
                    r"\text{each other?}", font_size=34).move_to([0, 0.1, 0])
        ax = axes([0, 5], [0, 45], x_length=7.6, y_length=2.2, xticks=[], yticks=[0, 20, 40],
                  xlabel=r"", ylabel=r"estimated speed (mph)", center=[0, -1.5, 0], font_size=18)
        bar = bars(ax.ax, np.arange(5) + 0.5, lp["mph"], FALSE, width=0.6)
        names = VGroup(*[label(v, font_size=22, color=FALSE).next_to(ax.ax.c2p(i + 0.5, 0), DOWN, buff=0.15)
                         for i, v in enumerate(lp["verbs"])])
        vals = VGroup(*[label(f"{m:.1f}", font_size=20, color=GREY_A).next_to(r, UP, buff=0.08)
                        for r, m in zip(bar, lp["mph"])])
        tag = historical_tag(archive.LOFTUS_PALMER_1974.cite)
        with self.voiceover(
            "In 1974, at the University of Washington, Elizabeth Loftus and John Palmer showed students short films "
            "of traffic accidents. <bookmark mark='a'/> Afterwards came a questionnaire, and one question mattered: "
            "about how fast were the cars going when they hit each other? <bookmark mark='b'/> Except that not "
            "everyone read hit. Some read smashed into, some collided with, bumped, or contacted. One word, and "
            "nothing else, differed. <bookmark mark='c'/> The estimates followed the word. Smashed gave about "
            f"{lp['mph'][0]:.0f} miles an hour; contacted, about {lp['mph'][-1]:.0f}. The same films, seen by the "
            "same kind of people, and a single verb moved the speed by nine miles an hour."
        ) as vo:
            self.play(FadeIn(tag), Create(road), FadeIn(a), FadeIn(b))
            self.play(a.animate.move_to([-0.82, 1.65, 0]), b.animate.move_to([0.82, 1.65, 0]), run_time=1.6,
                      rate_func=rate_functions.ease_in_quad)
            flash = Star(n=8, outer_radius=0.55, inner_radius=0.25, color=LOST, fill_opacity=0.8).move_to([0, 1.7, 0])
            self.play(FadeIn(flash, scale=0.4), run_time=0.3)
            self.play(FadeOut(flash), run_time=0.5)
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            words = VGroup(*[label(v, font_size=30, color=FALSE) for v in lp["verbs"]])
            for w in words:
                w.move_to(q[1])
            self.play(FadeIn(words[3]))
            prev = 3
            for i in (0, 1, 2, 4):
                self.play(FadeOut(words[prev]), FadeIn(words[i]), run_time=0.45)
                prev = i
            vo.wait_until("c")
            self.play(FadeOut(words[prev]), FadeIn(ax), FadeIn(names))
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in bar], lag_ratio=0.2), FadeIn(vals))
        self.clear_scene()

    def glass(self):
        lp = archive.LOFTUS_PALMER_1974.data
        g = lp["glass_yes"]
        n = lp["per_group"]
        head = heading(r"One week later: \ ``Did you see any broken glass?''")
        groups = ((r"smashed", g["smashed"], FALSE), (r"hit", g["hit"], CUE), (r"no speed question", g["control"],
                                                                                GREY_B))
        cols = VGroup()
        for name, k, col in groups:
            dots = VGroup(*[Dot(radius=0.09, color=col if i < k else GREY_D) for i in range(n)])
            dots.arrange_in_grid(rows=5, cols=10, buff=0.1)
            cols.add(VGroup(label(name, font_size=26, color=col), dots,
                            label(rf"{k} of {n} said yes", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.25))
        cols.arrange(RIGHT, buff=0.8).move_to([0, 0.3, 0])
        note = rows_of([
            (r"there was no broken glass in the film", LOST),
            (r"the word did not only colour a judgement: \ a week later it had become part of what people "
             r"remembered seeing", WHITE),
        ], 12.4, 27, 0.25).to_edge(DOWN, buff=0.6)
        tag = historical_tag(archive.LOFTUS_PALMER_1974.cite)
        with self.voiceover(
            "That alone might be a bias in judging speed. So in a second experiment, a hundred and fifty students "
            "saw a film of a multiple-car crash, fifty heard smashed, fifty heard hit, and fifty were not asked about "
            "speed at all. <bookmark mark='a'/> A week later they came back and answered one more question: did "
            f"you see any broken glass? <bookmark mark='b'/> Of those who had heard smashed, {g['smashed']} of fifty "
            f"said yes. Of those who had heard hit, {g['hit']}. Of those not asked, {g['control']}. "
            "<bookmark mark='c'/> There was no broken glass in the film. <bookmark mark='d'/> A word in a question "
            "had become, a week later, a memory of something seen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[FadeIn(c[0]) for c in cols], *[FadeIn(c[1]) for c in cols])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c[2]) for c in cols], lag_ratio=0.6))
            vo.wait_until("c")
            self.play(FadeIn(note[0]))
            vo.wait_until("d")
            self.play(FadeIn(note[1]))
        self.clear_scene()

    def your_list(self):
        stage = demo_stage(8.8, 4.2, center=[0, 0.6, 0])
        note = label(r"fifteen words, \ one every second and a half: \ just watch", font_size=26,
                     color=GREY_A).next_to(stage, DOWN, buff=0.3)
        with self.voiceover(
            "Before we go on, an experiment on you, as in the last part. <bookmark mark='a'/> Fifteen words will "
            "appear, one every second and a half. Just watch them, and try to remember them. Here they come."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(note))
        spot = stage.box.get_center() + UP * 0.2
        for w in SLEEP_LIST:
            t_ = label(w, font_size=72, color=WHITE).move_to(spot)
            self.add(t_)
            self.wait(1.2)
            self.remove(t_)
            self.wait(0.3)
        self.clear_scene()

    def your_test(self):
        head = heading(r"Was it in the list?")
        chips = VGroup(*[word_chip(w, color=WHITE, font_size=34, width=2.6) for w, _ in TEST_WORDS])
        chips.arrange_in_grid(rows=2, cols=3, buff=(0.7, 0.6)).move_to([0, 0.6, 0])
        rows = rows_of([
            (r"for each word: \ yes or no", WHITE),
            (r"and for each yes: \ do you \emph{remember} seeing it, \ or do you just \emph{know} it was there?",
             CUE),
        ], 12.4, 28, 0.25).to_edge(DOWN, buff=0.8)
        pause = VGroup(Rectangle(width=0.2, height=0.7, fill_color=YOU, fill_opacity=1, stroke_width=0),
                       Rectangle(width=0.2, height=0.7, fill_color=YOU, fill_opacity=1, stroke_width=0)
                       ).arrange(RIGHT, buff=0.2).next_to(chips, RIGHT, buff=0.5)
        with self.voiceover(
            "Now six words. For each one, decide: was it in the list or not? <bookmark mark='a'/> And for every "
            "word you say yes to, decide one more thing. Do you remember it, can you bring back the moment it was "
            "on the screen? Or do you just know it was there? <bookmark mark='b'/> Pause the video and write down "
            "your answers. We'll come back to them in chapter eight."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3),
                      FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(pause))
        self.wait(1.5)
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ how memory loses what it had, \ and how it gains what it never had")
        rows = rows_of([
            (r"the shape of forgetting, \ and the two great reasons for it", LOST),
            (r"how memories settle into the brain, \ and why two learning systems are better than one", CTX),
            (r"spacing and testing: \ the two best-established ways to remember more", CUE),
            (r"remembering as rebuilding: \ schemas, \ words that were never there, \ suggestion", FALSE),
            (r"when to trust a memory: \ confidence, \ line-ups, \ and the people who forget nothing", TRACE),
        ], 11.8, 30, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "Last time, memory was a search, and a remarkably good one. This part is about its two failures, and "
            "they are not the same failure. <bookmark mark='a'/> Memory loses what it had: we'll fit the laws of "
            "forgetting, and ask why it happens at all. <bookmark mark='b'/> We'll see how memories settle into the "
            "brain over time, and why a brain might need two ways of learning. <bookmark mark='c'/> Then the two "
            "best-established ways of remembering more: spacing and testing, each with a model you can fit. "
            "<bookmark mark='d'/> And memory gains what it never had: the schema, the word that was never on the "
            "list, the suggestion that becomes a memory. <bookmark mark='e'/> Which leaves the practical question: "
            "when should anyone trust a memory, in a courtroom, a clinic, or a classroom?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 21", font_size=34, color=GREY_B), label(r"Memory II: \ Forgetting and Inventing",
                                                                           font_size=60))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"four laws of forgetting fitted to Ebbinghaus and three replications; \ Jost's law and the averaging "
            r"artefact",
            r"interference in an associator; \ consolidation in two stores; \ a network that learns a penguin",
            r"spacing by Pavlik and Anderson's model; \ testing by the bifurcation model, \ fitted",
            r"reconstruction: \ Bartlett, \ the category adjustment model, \ the DRM illusion by global matching",
            r"suggestion: \ misinformation, \ implanted memories, \ and 53 replications of verbal overshadowing",
            r"confidence and accuracy by signal detection; \ half-life regression, \ as language apps use it",
        ], color=P.ACCENT, font_size=30, width=13.2)
        with self.voiceover(
            "This is Part 21 of Psychology, Built, the fourth part of Act Five, on thinking: memory, forgetting and "
            "inventing. <bookmark mark='a'/> We'll fit four laws of forgetting to Ebbinghaus's curve and to three "
            "people who repeated his experiment, one of them in 2015. We'll watch interference happen in a network, "
            "consolidation in two stores, and a network that learns about penguins and forgets about robins. We'll "
            "fit models of the spacing and the testing effects. Then reconstruction: Bartlett's schemas, a model in "
            "which memory leans toward the typical, and the illusion you just took part in, explained by one "
            "equation. Then suggestion, implanted memories, and the open data from fifty-three replications of one "
            "experiment. And finally confidence: when it predicts accuracy and when it doesn't, and the model a "
            "language app uses to decide when you'll forget a word."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=26.0)
        self.clear_scene()
