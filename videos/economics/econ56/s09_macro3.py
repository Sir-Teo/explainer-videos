from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

LINES = [
    r"A central bank minimizes $\mathbb{E}\sum_t \beta^t \big[\pi_t^2 + 0.25\,(x_t - 0.5)^2\big]$ subject to "
    r"$\pi_t = \beta\,\mathbb{E}_t \pi_{t+1} + 0.1\, x_t + u_t$, \ with $\beta = 0.99$ and a cost shock $u_t = "
    r"0.5\, u_{t-1} + \varepsilon_t$. \ It cannot commit to future policy.",
    r"(a) \ Find average inflation and the average output gap. \quad (9 marks)",
    r"(b) \ Find the responses of inflation and the gap to a cost shock. \quad (9 marks)",
    r"(c) \ How would the ability to commit change (b)? \quad (7 marks)",
]


class Macro3(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Macro: \ the three-equation model under discretion", r"What does a central bank lose by "
             r"deciding one period at a time?", "Question seven. Macroeconomics: the three-equation model under "
             "discretion.", lit={1977: r"Kydland and Prescott", 1983: r"Barro and Gordon",
                                 1999: r"Clarida, \ Gal\'i and Gertler"},
             scale=("nation",), horizon=("a year", "a decade"))
        self.statement()
        self.bias()
        self.shock()
        self.picture()
        self.marks()

    def statement(self):
        paper = exam_paper(7, "macro", r"discretion", LINES).move_to(UP * 0.5)
        with self.voiceover(
            "Question seven. A central bank cares about inflation and about the output gap, which it would like "
            "to be half a point above its natural level. The economy follows Part thirty's Phillips curve, with a "
            "cost shock that halves each quarter. The bank cannot commit. <bookmark mark='a'/> Part a: average "
            "inflation and the average gap. <bookmark mark='b'/> Part b: the response to a cost shock. <bookmark "
            "mark='c'/> Part c: what commitment would change. Pause, and write the bank's first-order condition."
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("abc", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 7.0)
        self.clear_scene()

    def bias(self):
        M = load("macro3")
        tag = part_tag(7, "a", "macro")
        rows = steps([
            (r"\min\ \pi_t^2 + \lambda (x_t - x^*)^2 \ \ \text{s.t.}\ \ \pi_t = \kappa x_t + "
             r"\underbrace{\beta\,\mathbb{E}_t \pi_{t+1} + u_t}_{\text{taken as given}}",
             r"discretion: \ today's bank cannot move expectations of tomorrow"),
            (r"\kappa\,\pi_t + \lambda\,(x_t - x^*) = 0", r"first-order condition"),
            (rf"\bar\pi = \frac{{\lambda \kappa x^*}}{{\lambda(1 - \beta) + \kappa^2}} = "
             rf"\frac{{0.25 \times 0.1 \times 0.5}}{{0.0025 + 0.01}} = {M['pi_bar']:.2f}",
             r"the Phillips curve and the condition, \ in a steady state", GAIN),
            (rf"\bar x = \frac{{(1 - \beta)\,\bar\pi}}{{\kappa}} = {M['x_bar']:.2f} \qquad (\text{{target }} 0.5)",
             r"the inflation bias buys almost no output"),
        ])
        rows.move_to(DOWN * 0.1)
        box = answer_box(rows[2][0])
        with self.voiceover(
            "Part a. <bookmark mark='a'/> Under discretion the bank re-optimizes every period and takes "
            "tomorrow's expected inflation as given, because it cannot promise anything about tomorrow. <bookmark "
            "mark='b'/> The first-order condition trades inflation against the gap: kappa pi plus lambda times the "
            "gap's shortfall equals zero. <bookmark mark='c'/> In a steady state the Phillips curve and this "
            f"condition together give average inflation of {M['pi_bar']:.2f} point: the inflation bias. <bookmark "
            f"mark='d'/> And what does it buy? An average gap of only {M['x_bar']:.2f}, against the 0.5 the bank "
            "wanted. Everyone expects the bank to try, so inflation rises until trying no longer pays; Kydland and "
            "Prescott's argument, in Part twenty-eight's language."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if mk == "c":
                    self.play(Create(box))
        self.clear_scene()

    def shock(self):
        M = load("macro3")
        tag = part_tag(7, "b, c", "macro")
        rows = steps([
            (r"\pi_t = a_\pi u_t, \quad x_t = a_x u_t, \quad \mathbb{E}_t \pi_{t+1} = \rho\, a_\pi u_t",
             r"guess and verify"),
            (rf"a_\pi = \frac{{\lambda}}{{\kappa^2 + \lambda(1 - \beta\rho)}} = {M['a_pi']:.2f}, \qquad "
             rf"a_x = -\frac{{\kappa}}{{\kappa^2 + \lambda(1 - \beta\rho)}} = {say_tex(M['a_x'])}",
             r"from the first-order condition and the Phillips curve", GAIN),
            (r"\text{commitment: } \pi_t = \tfrac{\lambda}{\kappa}\,(x_{t-1} - x_t)",
             r"the bank promises to keep the gap low after the shock fades"),
            (rf"x_t = {M['a_commit']:.2f}\, x_{{t-1}} + c\, u_t", r"history dependence: \ the gap returns slowly"),
            (rf"\text{{loss from one shock: }} {M['loss_d']:.2f} \ \to\ {M['loss_c']:.2f}",
             r"expected future policy does part of the work today"),
        ])
        rows.move_to(DOWN * 0.1)
        box = answer_box(rows[1][0])
        with self.voiceover(
            "Part b. <bookmark mark='a'/> Guess that inflation and the gap are proportional to the shock; then "
            "expected inflation is rho times today's. <bookmark mark='b'/> Substituting into the first-order "
            f"condition and the Phillips curve gives inflation {M['a_pi']:.2f} times the shock and the gap "
            f"{say_num(M['a_x'], 2)} times: the bank lets inflation rise and squeezes output, and both fade as the "
            "shock does. <bookmark mark='c'/> Part c. A bank that could commit would promise to keep the gap low "
            "even after the shock has gone. <bookmark mark='d'/> Its gap returns slowly, with a coefficient of "
            f"{M['a_commit']:.2f} on its own past. <bookmark mark='e'/> Because people expect that, inflation "
            f"rises less today, and the loss from one shock falls from {M['loss_d']:.2f} to {M['loss_c']:.2f}. "
            "The gain from commitment comes through expectations, which is the whole case for forward guidance."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if mk == "b":
                    self.play(Create(box))
        self.clear_scene()

    def picture(self):
        M = load("macro3")
        h = np.arange(len(M["pi_d"]))
        axs = []
        for k, (name, yr, yt) in enumerate(((r"inflation", (-0.4, 2.0), [0, 1, 2]),
                                             (r"output gap", (-0.9, 0.2), [-0.8, -0.4, 0]))):
            axs.append(plane([0, 12], list(yr), center=(LEFT * 3.3 if k == 0 else RIGHT * 2.4) + DOWN * 0.3,
                             x_length=5.2, y_length=4.4, xticks=[0, 4, 8, 12], yticks=yt,
                             xlabel=r"quarters after a unit cost shock", ylabel=name, xfmt=lambda x: f"{x:.0f}",
                             yfmt=lambda y: f"{y:+.1f}".replace("-", "{-}") if y else "0", font_size=14))
        zs = VGroup(*[DashedLine(a.ax.c2p(0, 0), a.ax.c2p(12, 0), color=GREY_D, stroke_width=1) for a in axs])
        dsc = VGroup(path(axs[0], h, M["pi_d"], MACRO, 3.0), path(axs[1], h, M["x_d"], MACRO, 3.0))
        com = VGroup(path(axs[0], h, M["pi_c"], GAIN, 3.0), path(axs[1], h, M["x_c"], GAIN, 3.0))
        key = VGroup(label(r"orange: \ discretion", font_size=19, color=MACRO),
                     label(r"green: \ commitment", font_size=19, color=GAIN)).arrange(RIGHT, buff=0.8).to_edge(
            UP, buff=0.45)
        with self.voiceover(
            "The picture. <bookmark mark='a'/> Under discretion, inflation jumps and the gap falls, and both die "
            "away with the shock. <bookmark mark='b'/> Under commitment, inflation rises by less, and later even "
            "dips below zero; the gap falls by less at first but stays negative longer, after the shock is nearly "
            "gone. That promise, kept, is what holds today's inflation down."
        ) as vo:
            self.play(*[FadeIn(a) for a in axs], FadeIn(zs), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(dsc), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(com), run_time=1.5)
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"letting the discretionary bank choose expectations: \ that is commitment",
            r"believing the bias buys output: \ the average gap is $(1 - \beta)\bar\pi / \kappa$, \ nearly zero",
            r"the wrong sign on the gap's response to a cost shock",
            r"forgetting that $\mathbb{E}_t \pi_{t+1} = \rho\,\pi_t$ when solving by undetermined coefficients",
        ]).move_to(UP * 0.2)
        take = label(r"what a bank cannot promise, \ it pays for in average inflation and in every shock",
                     font_size=23, color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> Letting the discretionary bank choose expectations. "
            "<bookmark mark='b'/> Believing the bias buys output. <bookmark mark='c'/> The wrong sign on the gap. "
            "<bookmark mark='d'/> And forgetting what expected inflation is when the shock persists. <bookmark "
            "mark='e'/> The idea to keep, from Parts twenty-eight and thirty: what a central bank cannot promise, "
            "it pays for, in average inflation and again in every shock."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()

