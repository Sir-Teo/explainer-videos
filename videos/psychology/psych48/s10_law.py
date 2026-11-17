from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Law(VoiceoverScene):
    def construct(self):
        self.card()
        self.practice()
        self.howmany()

    def card(self):
        card = chapter_card(9, r"A law that was an average", r"Is the power law of practice a law of any mind?",
                            lit={1981: r"Newell \& Rosenbloom", 2000: r"Heathcote et al."}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter nine. A law that was an average."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def practice(self):
        d = load("practice")
        head = heading(r"The power law of practice")
        A = axes([0, 200], [300, 1100], x_length=5.6, y_length=3.4, xticks=[0, 50, 100, 150, 200],
                 yticks=[400, 600, 800, 1000], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"trial", ylabel=r"response time (ms)", center=[-3.3, 0.3, 0], font_size=13)
        cols = [SYMP, PERSON, GOOD, MODEL, CARE, GREY_A]
        some = VGroup(*[curve_in(A.ax, d["t"], np.clip(y, 300, 1100), c, stroke_width=1.5) for y, c in zip(d["some"], cols)])
        avg = curve(A.ax, d["t"], d["mean"], WHITE, stroke_width=4)
        pw = DashedVMobject(curve(A.ax, d["t"], d["avg_pow"], GOOD, stroke_width=3), num_dashes=40)
        ex = DashedVMobject(curve(A.ax, d["t"], d["avg_exp"], AUTH, stroke_width=3), num_dashes=40)
        rows = rows_of([
            (r"Newell and Rosenbloom, \ 1981: \ across many skills, \ practice curves follow a power law: \ a law "
             r"of practice", WHITE),
            (rf"Psyche's 60 learners each speed up exponentially, \ at very different rates; \ an exponential fits "
             rf"{100 * d['exp_wins']:.0f}\% of them better than a power law", PERSON),
            (r"their average is better fitted by a power law (green) than by an exponential (red)", GOOD),
            (r"Heathcote, \ Brown and Mewhort, \ 2000: \ person by person, \ real data favour the exponential: \ the "
             r"law described the average, \ not the learner", AUTH),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.practice\_curves}, \ 60 simulated learners")
        with self.voiceover(
            "Estes's warning has a famous case. <bookmark mark='a'/> In 1981 Allen Newell and Paul Rosenbloom showed "
            "that across many skills, practice curves follow a power law. It became the law of practice. "
            "<bookmark mark='b'/> Psyche's sixty learners each speed up exponentially, at very different rates, and "
            "an exponential fits almost all of them better than a power law. <bookmark mark='c'/> But their average "
            "is better fitted by a power law. <bookmark mark='d'/> Andrew Heathcote, Scott Brown and Douglas Mewhort "
            "fitted real practice data person by person in 2000, and found the exponential favoured. The law "
            "described the average, not the learner."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(some), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(avg), Create(pw), Create(ex))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def howmany(self):
        d = load("powerk")
        head = heading(r"How many learners make a law?")
        A = axes([0.3, 5.7], [0, 1.0], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"averages better fit by a power law",
                 center=[-3.3, 0.3, 0], font_size=12)
        b = bars(A.ax, [1, 2, 3, 4, 5], d["power_wins"], [PERSON, PERSON, MODEL, MODEL, GOOD], width=0.6)
        names = VGroup(*[label(rf"{int(k)}", font_size=14, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, k in enumerate(d["k"])])
        nl = label(r"exponential learners averaged", font_size=13, color=GREY_A).next_to(names, DOWN, buff=0.1)
        rows = rows_of([
            (r"average $k$ of Psyche's exponential learners, \ 60 times for each $k$, \ and ask which curve fits "
             r"the average better", WHITE),
            (rf"one learner: \ the power law wins {100 * d['power_wins'][0]:.0f}\% of the time, \ by noise", PERSON),
            (rf"thirty learners: \ {100 * d['power_wins'][-1]:.0f}\%: \ averaging different rates manufactures "
             rf"the power law", GOOD),
            (r"the lesson for Part 47 and this part: \ fit the person, \ then describe the population, \ never "
             r"the reverse", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.practice\_curves}, \ 60 averages for each size")
        with self.voiceover(
            "How many learners does it take to make a law? <bookmark mark='a'/> Average k of Psyche's exponential "
            "learners, sixty times for each k, and ask which curve fits the average better. <bookmark mark='b'/> "
            "With one learner, the power law wins only about one time in twelve, by noise. <bookmark mark='c'/> With "
            "thirty learners it wins eighty-eight percent of the time. Averaging different rates manufactures the "
            "power law. <bookmark mark='d'/> That's the lesson of Part 47 and of this part: fit the person, then "
            "describe the population, never the reverse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(nl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]), FadeIn(b[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(x) for x in b[2:]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
