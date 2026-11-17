from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Rewards(VoiceoverScene):
    def construct(self):
        self.card()
        self.markers()
        self.bayes()
        self.meta()
        self.sdt()
        self.maslow()

    def card(self):
        card = chapter_card(5, r"Intrinsic and extrinsic", r"Can a reward make you like something less?",
                            lit={1971: r"Deci", 1973: r"Lepper, \ Greene \& Nisbett", 1999: r"Deci, \ Koestner \& Ryan",
                                 2014: r"Cerasoli et al."},
                            part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter five. Intrinsic and extrinsic."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def markers(self):
        head = heading(r"The magic markers")
        groups = VGroup()
        for name, col, h in ((r"expected award", EXTR, 0.45), (r"unexpected award", INTR, 1.0),
                             (r"no award", GREY_B, 0.92)):
            bar = Rectangle(width=1.1, height=2.6 * h, stroke_width=0, fill_color=col, fill_opacity=0.85)
            groups.add(VGroup(bar, label(name, font_size=17, color=col).next_to(bar, DOWN, buff=0.15)))
        groups.arrange(RIGHT, buff=0.5, aligned_edge=DOWN).move_to([-3.4, -0.3, 0])
        yl = label(r"free time later spent drawing \ (schematic)", font_size=16, color=GREY_A).next_to(groups, UP,
                                                                                                   buff=0.3)
        rows = rows_of([
            (r"1973: \ preschool children who already liked drawing with markers", WHITE),
            (r"one group is promised a Good Player certificate for drawing; \ one gets the same certificate as a "
             r"surprise; \ one gets none", EXTR),
            (r"one to two weeks later, \ in free play, \ the children who had expected the award drew about half "
             r"as much as the others", LOST),
            (r"the surprise award did no harm: \ what mattered was drawing in order to get it", INTR),
        ], 5.6, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Lepper, \ Greene \& Nisbett (1973)")
        with self.voiceover(
            "If rewards make things worth doing, more reward should mean more doing. In 1973 Mark Lepper, David "
            "Greene and Richard Nisbett showed a case where it means less. <bookmark mark='a'/> They found preschool "
            "children who already liked drawing with felt-tip markers. <bookmark mark='b'/> One group was promised "
            "a Good Player certificate, with a gold seal and a ribbon, for drawing. A second group got the same "
            "certificate as a surprise afterwards. A third got nothing. <bookmark mark='c'/> One to two weeks later, "
            "the markers were put out during free play, and observers behind a one-way mirror timed the children. "
            "Those who had drawn for the expected award spent about half as much time drawing as the other two "
            "groups. <bookmark mark='d'/> The surprise award did no harm. What mattered was having drawn in order to "
            "get it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(g[0], DOWN) for g in groups], lag_ratio=0.3),
                      FadeIn(VGroup(*[g[1] for g in groups])), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def bayes(self):
        d = load("perception")
        head = heading(r"Derivation: \ inferring your own interest")
        eqs = VGroup(
            MathTex(r"P(\text{draw} \mid I, R) = \sigma(\beta_0 + \beta_I I + \beta_R R)", font_size=32),
            MathTex(r"\frac{P(I = 1 \mid \text{drew}, R)}{P(I = 0 \mid \text{drew}, R)} = \frac{\pi}{1 - \pi}"
                    r"\cdot \frac{P(\text{draw} \mid 1, R)}{P(\text{draw} \mid 0, R)}", font_size=28),
        ).arrange(DOWN, buff=0.35)
        A = axes([0, 4], [0.4, 0.8], x_length=5.6, y_length=3.0, xticks=[0, 1, 2, 3, 4], yticks=[0.5, 0.6, 0.7],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"the reward's pull, \ $\beta_R$",
                 ylabel=r"inferred P(I like it)", center=[-3.3, -0.6, 0], font_size=16)
        c = curve(A.ax, d["pull"], d["curve"], EXTR, 4)
        top = DashedLine(A.ax.c2p(0, d["no_reward"]), A.ax.c2p(4, d["no_reward"]), color=INTR, stroke_width=2)
        tl = label(r"no reward", font_size=16, color=INTR).next_to(A.ax.c2p(4, d["no_reward"]), UP, buff=0.05)
        tl.align_to(top, RIGHT)
        rows = rows_of([
            (r"Bem's self-perception: \ we infer our attitudes partly from our behaviour, \ as an observer would",
             WHITE),
            (rf"having drawn with no reward, \ the inference is {d['no_reward']:.2f} that I like drawing "
             r"\ (prior 0.5)", INTR),
            (rf"having drawn for a reward, \ {d['reward']:.2f}: \ the reward explains part of the drawing, \ and "
             r"discounts the interest", EXTR),
            (r"the stronger the reward's pull, \ the less the act says about the person: \ Kelley's discounting",
             WANT),
        ], 5.6, 21, 0.3)
        right = VGroup(eqs, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{drive.self\_perception}: \ $\beta_0 = -1$, \ $\beta_I = \beta_R = 2$")
        with self.voiceover(
            "One explanation is a piece of inference. <bookmark mark='a'/> Daryl Bem proposed in 1972 that people "
            "infer their own attitudes partly from their own behaviour, the way an observer would. "
            "<bookmark mark='b'/> Write it as Bayes's rule. A child either likes drawing or doesn't, with even odds "
            "beforehand. Liking drawing makes drawing likelier, and so does a promised reward. Having drawn with no "
            f"reward, the inference is {d['no_reward']:.2f} that I like it. <bookmark mark='c'/> Having drawn for a "
            f"reward, it's {d['reward']:.2f}. The reward explains part of the drawing, so the drawing says less "
            "about the child. <bookmark mark='d'/> The stronger the reward's pull, the less the act reveals about "
            "the person. Harold Kelley called this the discounting principle, and here it discounts the child's "
            "interest in its own eyes. It's one account among several; the others say the reward feels "
            "controlling, and takes away a sense of choice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eqs[0]), Write(eqs[1]), FadeIn(top), FadeIn(tl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(c), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def meta(self):
        head = heading(r"Thirty years of argument, \ and the meta-analyses")
        rows = rows_of([
            (r"Deci, \ 1971: \ students paid to solve puzzles spent less of a free period on them afterwards than "
             r"students who were never paid", WHITE),
            (r"Cameron and Pierce, \ 1994: \ a meta-analysis finding little overall harm from rewards", EXTR),
            (r"Deci, \ Koestner and Ryan, \ 1999: \ 128 experiments; \ expected, \ tangible rewards that depend on "
             r"doing the task reliably reduce later free-choice interest; \ verbal praise tends to raise it", LOST),
            (r"Cerasoli, \ Nicklin and Ford, \ 2014: \ in schools and workplaces, \ incentives predict the "
             r"quantity of performance, \ intrinsic motivation its quality, \ and both matter", INTR),
            (r"the effect is real; \ its scope, \ how large and where outside the laboratory, \ is still argued",
             MODEL),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Deci (1971); \ Cameron \& Pierce (1994); \ Deci, \ Koestner \& Ryan (1999); \ "
                            r"Cerasoli, \ Nicklin \& Ford (2014)")
        with self.voiceover(
            "This became one of psychology's longest arguments. <bookmark mark='a'/> Edward Deci had found the "
            "same thing with adults in 1971: students paid to solve puzzles spent less of a free period on them "
            "afterwards than students never paid. <bookmark mark='b'/> In 1994 Judy Cameron and David Pierce "
            "published a meta-analysis concluding that rewards do little overall harm. <bookmark mark='c'/> Deci, "
            "Richard Koestner and Richard Ryan answered in 1999 with a meta-analysis of a hundred and twenty-eight "
            "experiments. Expected, tangible rewards that depend on doing the task reliably reduced later free "
            "choice; verbal praise tended to raise it. <bookmark mark='d'/> And in 2014 Christopher Cerasoli, "
            "Jessica Nicklin and Michael Ford pulled together studies from schools and workplaces: incentives "
            "predicted the quantity of performance, intrinsic motivation its quality, and both mattered. "
            "<bookmark mark='e'/> The undermining effect is real. Its scope, how large it is and where it matters "
            "outside the laboratory, is still argued."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def sdt(self):
        head = heading(r"Self-determination theory")
        names = [(r"autonomy", r"acting from choice, \ not control", INTR),
                 (r"competence", r"getting better at something", BODY),
                 (r"relatedness", r"connection to other people", LIKE)]
        circles = VGroup()
        for k, (n, s, c) in enumerate(names):
            ang = PI / 2 + 2 * PI * k / 3
            pos = np.array([-3.4, 0.0, 0]) + 1.25 * np.array([np.cos(ang), np.sin(ang), 0])
            circ = Circle(radius=1.05, color=c, fill_opacity=0.12).move_to(pos)
            circles.add(VGroup(circ, label(n, font_size=20, color=c).move_to(circ)))
        rows = rows_of([
            (r"Deci and Ryan: \ three basic psychological needs; \ when they are met, \ motivation becomes more "
             r"internal, \ from enjoyment or from values made one's own", WHITE),
            (r"a reward that informs \ (you did well) \ supports competence; \ one that controls \ (do this, \ get "
             r"that) \ thwarts autonomy", EXTR),
            (r"a broad framework with much correlational support, \ used in schools, \ clinics and workplaces "
             r"\ (Part 53)", INTR),
        ], 5.6, 22, 0.34).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Ryan \& Deci (2000)")
        with self.voiceover(
            "Deci and Ryan built the results into self-determination theory. <bookmark mark='a'/> It proposes three "
            "basic psychological needs: autonomy, competence and relatedness. When they're met, motivation becomes "
            "more internal, coming from enjoyment, or from values a person has made their own. "
            "<bookmark mark='b'/> On this view a reward that informs, you did well, supports competence, while a "
            "reward that controls, do this and you'll get that, thwarts autonomy. That's their account of the "
            "markers. <bookmark mark='c'/> It's a broad framework with a great deal of correlational support, and "
            "it's used in schools, clinics and workplaces, which we'll meet again in Part 53."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(c) for c in circles], lag_ratio=0.3))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def maslow(self):
        head = heading(r"Maslow's hierarchy, \ and what became of it")
        py = pyramid([(r"physiological", BODY), (r"safety", INTR), (r"love and belonging", LIKE),
                      (r"esteem", EXTR), (r"self-actualization", WANT)], width=6.0, height=4.6, font_size=22)
        py.move_to([-3.3, -0.35, 0])
        stamp = label(r"the pyramid is not in Maslow's paper", font_size=19, color=GREY_B)
        stamp.next_to(py, DOWN, buff=0.2)
        card_ = theory_card(r"A hierarchy of needs", r"Abraham Maslow, \ 1943",
                            r"needs are satisfied in order: \ each level must be largely met before the next one "
                            r"motivates", r"universal needs, \ yes; \ a fixed ladder, \ no", "contested",
                            width=6.2, font_size=21, color=KANT)
        card_.move_to([3.4, 1.05, 0])
        checks = verdict_row([
            (r"Wahba and Bridwell, \ 1976: \ little support for the ranking", "failed"),
            (r"Tay and Diener, \ 2011: \ 123 countries; \ the needs are universal, \ and each is met "
             r"partly independently of the others", "replicated, smaller"),
        ], width=6.2, font_size=19)
        checks.next_to(card_, DOWN, buff=0.35)
        tag = published_tag(r"Maslow (1943); \ Wahba \& Bridwell (1976); \ Tay \& Diener (2011)")
        with self.voiceover(
            "Self-determination theory has a famous ancestor. <bookmark mark='a'/> In 1943 Abraham Maslow proposed "
            "that human needs form a hierarchy: the body first, then safety, then love and belonging, then esteem, "
            "and at the top what he called self-actualization, becoming what one is able to become. A need higher "
            "up would motivate only once the ones below it were largely met. <bookmark mark='b'/> The pyramid that "
            "carries his name is not in his paper. Management writers drew it in the nineteen-sixties, and it "
            "became the best-known diagram in psychology. <bookmark mark='c'/> When the theory was tested, the "
            "ladder did not hold. In 1976 Mahmoud Wahba and Lawrence Bridwell reviewed the studies and found "
            "little support for the ranking. <bookmark mark='d'/> In 2011 Louis Tay and Ed Diener used surveys "
            "from 123 countries. Needs like Maslow's were found everywhere, and meeting them went with "
            "well-being, but people reported meeting the higher needs whether or not the lower ones were met. "
            "<bookmark mark='e'/> So the list survives and the ladder does not: a lesson in how a theory can be "
            "half right, and remembered for the wrong half."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(layer, shift=UP * 0.15) for layer in py.layers], lag_ratio=0.35),
                      FadeIn(card_.box), FadeIn(card_.name), FadeIn(card_.claim), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(stamp, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(checks.rows[0], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(card_.verdict), FadeIn(card_.status),
                      *[layer.shape.animate.set_fill(opacity=0.32) for layer in py.layers[2:]])
        self.clear_scene()
