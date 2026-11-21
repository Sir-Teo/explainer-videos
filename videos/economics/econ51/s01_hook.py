from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.name()
        self.today()
        self.question()
        self.title()
        self.objectives()

    def name(self):
        hc = history_card(1950, r"Richard Bellman, \ at RAND", r"needs a name for his mathematics of decisions made "
                          r"in stages, \ one that will not alarm the Air Force's masters", color=E.ACCENT, width=10.6,
                          font_size=24).move_to(UP * 1.6)
        words = VGroup(
            VGroup(label(r"``programming''", font_size=34, color=POLICY),
                   label(r"planning, \ as in a military schedule", font_size=20, color=GREY_A)).arrange(
                DOWN, buff=0.15),
            VGroup(label(r"``dynamic''", font_size=34, color=VALUE),
                   label(r"it changes over time; \\ and, \ he wrote, \ it cannot be used as an insult", font_size=20,
                         color=GREY_A)).arrange(DOWN, buff=0.15),
        ).arrange(RIGHT, buff=1.4).next_to(hc, DOWN, buff=0.6)
        quote = label(r"``something not even a Congressman could object to''", font_size=26, color=WHITE).next_to(
            words, DOWN, buff=0.5)
        caveat = label(r"his memory of the date has been questioned: \ Wilson became Secretary of Defense in 1953",
                       font_size=16, color=GREY_B).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Bellman, \ \emph{Eye of the Hurricane} (1984); \ Dreyfus, \ Operations Research (2002)",
                            corner=DR, font_size=11)
        with self.voiceover(
            "In his autobiography, the mathematician Richard Bellman recalled the autumn of 1950, when he went to "
            "work at the RAND Corporation, which did research for the United States Air Force. <bookmark mark='a'/> "
            "His first task was to find a name for his mathematics of decisions made in stages. The Secretary of "
            "Defense, he wrote, had a pathological fear and hatred of the word research, and the Air Force answered "
            "to him. <bookmark mark='b'/> So Bellman chose programming, in the sense of planning, as in a military "
            "schedule, <bookmark mark='c'/> and dynamic, because the problems change over time and because, he "
            "said, it is impossible to use the word dynamic as an insult. <bookmark mark='d'/> It was, he wrote, "
            "something not even a Congressman could object to. <bookmark mark='e'/> His memory of the date has "
            "been questioned, since the Secretary he named took office only in 1953; the name stuck either way."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(hc, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(words[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(words[1], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(quote, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(caveat))
        self.clear_scene()

    def today(self):
        G = load("growth")
        ax = plane([0.5, 1.5], [-20, 0], center=LEFT * 1.5 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[0.5, 0.75, 1.0, 1.25, 1.5], yticks=[-20, -15, -10, -5, 0],
                   xlabel=r"capital, \ as a share of its steady state", ylabel=r"value", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        g = G["grid"]
        curves = VGroup()
        keys = ["1", "2", "5", "10", "30", "100"]
        for i, k in enumerate(keys):
            col = interpolate_color(ManimColor(GRID), ManimColor(VALUE), i / (len(keys) - 1))
            curves.add(path(ax, g, G["kept"][k], col, 2.2))
        final = path(ax, g, G["V"], WHITE, 3.2)
        side = VGroup(
            label(r"guess a value, \\ apply Bellman's \\ equation, \ repeat", font_size=19, color=WHITE),
            label(rf"{G['vfi_iters']} rounds \\ to settle", font_size=19, color=VALUE),
            label(rf"{1000 * G['vfi_seconds']:.0f} milliseconds \\ on this machine", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = label(r"the growth model of Part 29 \ (computed)", font_size=13, color=GREY_B).to_corner(DL, buff=0.3)
        with self.voiceover(
            "Seventy years on, dynamic programming is how economists solve economies that have no formula. "
            "<bookmark mark='a'/> Guess the value of being in each situation, apply Bellman's equation, and repeat. "
            "Each round the guess improves, <bookmark mark='b'/> and after "
            f"{G['vfi_iters']} rounds the growth model of Part twenty-nine has settled, <bookmark mark='c'/> in a "
            "few hundredths of a second on a laptop. Inside an estimation, a model like this is solved again for "
            "every set of parameters the estimator tries, thousands of times. So speed matters; and so does a "
            "harder question."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("b")
            self.play(Create(final), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why does repeating Bellman's equation converge at all?", font_size=26, color=VALUE),
            label(r"which methods are fast, \ and which are accurate?", font_size=26, color=EGM),
            label(r"how do you know a computed answer is right?", font_size=26, color=ERR),
            label(r"and what breaks when the model grows?", font_size=26, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: how is an economy that has no formula solved, and how do you know the answer is right? "
            "<bookmark mark='a'/> Why does repeating Bellman's equation converge at all? <bookmark mark='b'/> Which "
            "methods are fast, and which are accurate? <bookmark mark='c'/> How do you know a computed answer is "
            "right? <bookmark mark='d'/> And what breaks when the model grows?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1971, 2021], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["log10"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, VALUE, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 51 \ $\cdot$ \ Computing Economies", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fifty-one: computing economies."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act X \ $\cdot$ \ The Graduate Core", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"the Bellman operator, \ its contraction, \ value and policy iteration",
            r"grids, \ interpolation, \ the endogenous grid method",
            r"projection and perturbation; \ when certainty equivalence misleads",
            r"accuracy: \ Euler-equation errors; \ expectations; \ continuous time",
            r"constraints that bind, \ the curse of dimensionality, \ reproducibility",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part opens Act ten, the graduate core: the tools that turn the models of the course into research. "
            "<bookmark mark='a'/> The Bellman operator, why it converges, and value and policy iteration. <bookmark "
            "mark='b'/> Grids, interpolation, and a method with no root finding at all. <bookmark mark='c'/> "
            "Projection and perturbation, and when certainty equivalence misleads. <bookmark mark='d'/> Accuracy, "
            "measured; expectations; and continuous time. <bookmark mark='e'/> Then constraints that bind, the curse "
            "of dimensionality, and how to make a computation that someone else can repeat."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
