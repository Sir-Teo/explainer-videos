from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403

LAM_C = {"0": BAD, "2": PAST, "10": FUT, "100": BLUEC}


class Laplace(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The rule of succession", r"How likely is the next success?", lit=(1763, 1937),
                            part=PART)
        with self.voiceover("Chapter two. The rule of succession."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rule()
        self.sunrise()
        self.definetti()
        self.carnap()

    def rule(self):
        head = label(r"Laplace's rule \ (1814)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        setup = stack([(r"an unknown chance $\theta$ of success, \ every value equally likely in advance", WHITE),
                       (r"$s$ successes in $n$ trials", PAST)], font_size=24).next_to(head, DOWN, buff=0.4)
        eq = MathTex(r"P(\text{next success} \mid s \text{ of } n) = \frac{\int_0^1 \theta^{s+1}(1-\theta)^{n-s}\,"
                     r"d\theta}{\int_0^1 \theta^{s}(1-\theta)^{n-s}\, d\theta} = \frac{s + 1}{n + 2}", font_size=36,
                     color=FUT).next_to(setup, DOWN, buff=0.5)
        ex = stack([(r"no data: \ $\tfrac12$; \ \ one success: \ $\tfrac23$; \ \ nine of ten: \ $\tfrac{10}{12}$", WHITE),
                    (r"Bayes's essay \ (1763) \ had the integral; \ Laplace the formula and its uses", GREY_A)],
                   font_size=23).next_to(eq, DOWN, buff=0.5)
        with self.voiceover(
            "The first mathematical answer to Hume came from Thomas Bayes and Pierre-Simon Laplace. "
            "<bookmark mark='a'/>Suppose an event has an unknown chance theta of happening on each trial, and that "
            "beforehand every value of theta is equally likely. You have seen s successes in n trials. "
            "<bookmark mark='b'/>Then the probability that the next trial succeeds is a ratio of two integrals, and "
            "it comes out beautifully: s plus one, over n plus two. <bookmark mark='c'/>With no data, a half. After one "
            "success, two thirds. After nine of ten, ten twelfths. Bayes's essay of 1763 contained the integral; "
            "Laplace gave the formula, and applied it everywhere."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(setup))
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.5))
        self.clear_scene()

    def sunrise(self):
        d = load("laplace")["sunrise"]
        head = label(r"Will the sun rise tomorrow?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        sun = VGroup(Circle(radius=0.6, color=PAST, fill_color=PAST, fill_opacity=0.7),
                     *[Line(0.75 * np.array([np.cos(a), np.sin(a), 0]), 1.05 * np.array([np.cos(a), np.sin(a), 0]),
                            color=PAST, stroke_width=3) for a in np.linspace(0, TAU, 12, endpoint=False)]).move_to(
            [-4.6, 0.6, 0])
        horizon = Line([-6.4, -0.1, 0], [-2.8, -0.1, 0], color=GREY_B, stroke_width=3)
        rows = stack([
            (r"Laplace: \ recorded history, \ about 5{,}000 years: \ " + f"{d['days']:,}".replace(",", "{,}")
             + r" days", WHITE),
            (r"$P(\text{sunrise tomorrow}) = 1 - \dfrac{1}{" + f"{d['days'] + 2:,}".replace(",", "{,}") + r"}$", FUT),
            (r"odds of " + f"{d['odds_against']:,}".replace(",", "{,}") + r" to 1", FUT),
            (r"sunrise every day for another 5{,}000 years: \ " + f"{d['p_all_next_n'][str(365 * 5000)]:.2f}"
             if str(365 * 5000) in d["p_all_next_n"] else r"", GREY_A),
            (r"Laplace added: \ for one who knows the laws that regulate the days, \ far greater", GREY_A),
            (r"the answer is only as good as the uniform prior: \ why should it be uniform?", BAD),
        ], font_size=22, aligned_edge=LEFT, width=7.2).move_to([2.6, -0.2, 0])
        with self.voiceover(
            "Laplace's famous example. <bookmark mark='a'/>Recorded history, he said, covers about five thousand "
            "years: over a million and eight hundred thousand sunrises. <bookmark mark='b'/>So the probability of "
            "another tomorrow is one minus one over that number plus two: <bookmark mark='c'/>odds of about one "
            "million eight hundred thousand to one. <bookmark mark='d'/>The same rule gives only about even odds that "
            "the sun rises every day for the next five thousand years. <bookmark mark='e'/>Laplace himself added that "
            "someone who knows the laws regulating the days would put the probability far higher. "
            "<bookmark mark='f'/>And there is the catch: the answer is only as good as the uniform prior over "
            "theta. Why should ignorance look like that? Part 13's Bertrand already showed it need not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(horizon), FadeIn(sun))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def definetti(self):
        hc = history_card(1937, r"Bruno de Finetti", r"`La prévision: \ ses lois logiques, \ ses sources "
                          r"subjectives'", width=7.0, color=HIST).to_corner(UL, buff=0.35)
        ex = label(r"\textit{exchangeable}: \ the probability of a sequence depends only on how many 1s, \ not "
                   r"their order", font_size=22, color=WHITE).next_to(hc, DOWN, buff=0.35).set_x(0)
        seqs = ["0011", "0101", "0110", "1001", "1010", "1100"]
        bars = VGroup()
        for i, sq in enumerate(seqs):
            b = Rectangle(width=0.7, height=1.4, stroke_width=0, fill_color=PAST, fill_opacity=0.8)
            t = MathTex(sq, font_size=24).next_to(b, DOWN, buff=0.12)
            bars.add(VGroup(b, t))
        bars.arrange(RIGHT, buff=0.3, aligned_edge=DOWN).next_to(ex, DOWN, buff=0.65).set_x(-3.0)
        bl = label(r"Laplace's prior: \ each $\tfrac{1}{30}$", font_size=20, color=PAST).next_to(bars, UP, buff=0.1)
        thm = MathTex(r"P(x_1, \dots, x_n) = \int_0^1 \theta^{s}(1-\theta)^{n-s}\, d\mu(\theta)", font_size=34,
                      color=FUT).move_to([3.4, -0.6, 0])
        tl = label(r"the representation theorem", font_size=20, color=FUT).next_to(thm, UP, buff=0.15)
        foot = stack([(r"an `unknown chance' is not a metaphysical posit: \ it is what exchangeable beliefs look like",
                       GOAL),
                      (r"but exchangeable over \textit{which} description? \ green, \ or grue? \ (Ch.\ 6)", BAD)],
                     font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Laplace assumed an unknown chance. Bruno de Finetti, a subjectivist who doubted that chances exist "
            "at all, showed in 1937 that you do not need to assume it. <bookmark mark='a'/>Call your beliefs about a "
            "sequence exchangeable if the probability of any sequence depends only on how many ones it has, not on "
            "their order. <bookmark mark='b'/>With Laplace's prior, for example, each of these six orderings of two "
            "ones in four gets exactly one thirtieth. <bookmark mark='c'/>De Finetti's representation theorem: "
            "any exchangeable beliefs about an unending sequence are exactly as if you believed in an unknown "
            "chance theta, with some prior mu over it, and tosses independent given theta. "
            "<bookmark mark='d'/>So the unknown chance is not a metaphysical posit. It is simply what exchangeable "
            "beliefs look like, and learning from frequencies follows. <bookmark mark='e'/>But exchangeable with "
            "respect to which description of the outcomes? Green and blue, or grue and bleen? We will see in chapter "
            "six that this is the whole question."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(ex))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.15),
                      *[FadeIn(b[1]) for b in bars], FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(tl), Write(thm))
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def carnap(self):
        d = load("laplace")
        head = label(r"Carnap's continuum of inductive methods \ (1952)", font_size=30, color=CONN).to_edge(UP,
                                                                                                           buff=0.3)
        eq = MathTex(r"P(\text{next success}) = \frac{s + \lambda/2}{n + \lambda}", font_size=36,
                     color=FUT).next_to(head, DOWN, buff=0.35)
        ax = Axes(x_range=[0, 50, 10], y_range=[0.4, 0.9, 0.1], x_length=7.2, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 18}).move_to([-2.0, -1.3, 0])
        xl = label(r"trials, \ 80\% successes", font_size=19, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.35)
        curves = VGroup()
        legend = VGroup()
        names = {"0": r"$\lambda = 0$: \ the straight rule", "2": r"$\lambda = 2$: \ Laplace",
                 "10": r"$\lambda = 10$", "100": r"$\lambda = 100$: \ near indifference"}
        for L, col in LAM_C.items():
            pts = [(n, y) for n, y in d["lambda"][L] if n > 0 or L != "0"]
            curves.add(series_plot(ax, [y for _, y in pts], col, xs=[n for n, _ in pts]))
            legend.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=col, stroke_width=4),
                              label(names[L], font_size=19, color=col)).arrange(RIGHT, buff=0.12))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.5, -0.6, 0])
        note = stack([(r"$\lambda$: \ the prior's weight, \ in imaginary trials", GREY_A),
                      (r"every $\lambda$ converges; \ none is fixed by logic", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=4.6).next_to(legend, DOWN, buff=0.4).align_to(legend, LEFT)
        with self.voiceover(
            "Rudolf Carnap tried to make inductive logic a branch of logic. <bookmark mark='a'/>He found not one rule "
            "but a continuum: s plus lambda over two, over n plus lambda. The parameter lambda says how many imaginary "
            "trials the prior is worth. <bookmark mark='b'/>Lambda zero is the straight rule: predict the observed "
            "frequency. Lambda two is Laplace. Large lambda clings to one half, near indifference. "
            "<bookmark mark='c'/>With eighty percent successes, every method converges to point eight, at different "
            "speeds. <bookmark mark='d'/>Carnap could not find a logical reason to prefer one lambda. The choice is "
            "a choice of prior, and Hume's problem reappears as a parameter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(legend))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.clear_scene()
