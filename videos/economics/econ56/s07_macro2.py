from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

LINES = [
    r"An unemployed worker draws one wage offer each period from the uniform distribution on $[0, 1]$. \ Accepting "
    r"gives that wage for ever; \ the worker discounts by $\beta = 0.95$. \ While unemployed the worker receives "
    r"$b = 0.5$ for 8 periods, \ and $z = 0.1$ thereafter.",
    r"(a) \ Write the Bellman equations. \quad (8 marks)",
    r"(b) \ Show that the reservation wage falls as benefits run out, \ and compute it after exhaustion. "
    r"\quad (10 marks)",
    r"(c) \ How does the chance of leaving unemployment change over a spell? \quad (7 marks)",
]


class Macro2(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Macro: \ a McCall worker whose benefits expire", r"Does a job seeker search differently "
             r"as benefits run out?", "Question six. Macroeconomics: a McCall worker whose benefits expire.",
             lit={1970: r"McCall", 1979: r"Shavell and Weiss", 1990: r"Katz and Meyer"},
             scale=("person",), horizon=("a year",))
        self.statement()
        self.bellman()
        self.picture()
        self.evidence()
        self.marks()

    def statement(self):
        paper = exam_paper(6, "macro", r"benefits that expire", LINES).move_to(UP * 0.5)
        with self.voiceover(
            "Question six. An unemployed worker gets one wage offer a period, uniform between zero and one, and a "
            "job, once taken, lasts for ever. The discount factor is 0.95. Unemployment benefits pay one half for "
            "eight periods, then only 0.1. <bookmark mark='a'/> Part a: the Bellman equations. <bookmark "
            "mark='b'/> Part b: show the reservation wage falls as benefits run out, and compute it once they "
            "have. <bookmark mark='c'/> Part c: what happens to the chance of leaving unemployment. Pause: which "
            "state should you solve first?"
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("abc", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 7.0)
        self.clear_scene()

    def bellman(self):
        M = load("macro2")
        res = M["res"]
        tag = part_tag(6, "a, b", "macro")
        rows = steps([
            (r"W(w) = \frac{w}{1 - \beta}", r"a job pays $w$ for ever"),
            (r"U_0 = z + \beta\,\mathbb{E}\max\big\{W(w'),\ U_0\big\}",
             r"benefits gone: \ the same problem every period, \ so solve it first"),
            (rf"w^*_0 = z + \frac{{\beta}}{{2(1 - \beta)}}\,(1 - w^*_0)^2 \ \Rightarrow\ w^*_0 = {res[0]:.3f}",
             r"$w^* = (1 - \beta)U$, \ and with uniform offers \ $\mathbb{E}\max$ has a closed form", GAIN),
            (r"U_d = b + \beta\,\mathbb{E}\max\big\{W(w'),\ U_{d-1}\big\}, \qquad d = 1, \dots, 8",
             r"$d$ periods of benefit left: \ work backwards from exhaustion"),
            (rf"w^*_d = (1 - \beta)\,U_d: \quad {res[0]:.3f} < {res[1]:.3f} < \dots < {res[-1]:.3f}",
             r"$U_{d-1} < U_d$ because $z < b$, \ and the operator is monotone: \ induction", GAIN),
            (rf"\text{{benefits for ever: }} w^* = {M['res_inf']:.3f}", r"the bound the sequence approaches"),
        ], math_size=28, buff=0.28)
        rows.move_to(DOWN * 0.1)
        boxes = [answer_box(rows[2][0]), answer_box(rows[4][0])]
        with self.voiceover(
            "Parts a and b. <bookmark mark='a'/> A job at wage w is worth w over one minus beta. <bookmark "
            "mark='b'/> Once benefits are gone, every period looks the same, so the value of searching satisfies "
            "an ordinary McCall equation. Solve that state first: it is where backward induction starts. <bookmark "
            "mark='c'/> With uniform offers the expectation of the maximum has a closed form, and the reservation "
            f"wage solves a quadratic: {res[0]:.3f}. <bookmark mark='d'/> With d periods of benefit left, the "
            "worker gets b today and moves to state d minus one tomorrow. <bookmark mark='e'/> Each extra period of "
            "benefit raises the value of searching, because b exceeds z and the Bellman operator is monotone; so "
            f"the reservation wage rises with benefits left, from {res[0]:.3f} after exhaustion to {res[-1]:.3f} "
            f"at the start of a spell. <bookmark mark='f'/> With benefits for ever it would be {M['res_inf']:.3f}."
        ) as vo:
            self.play(FadeIn(tag))
            for k, (mk, r_) in enumerate(zip("abcdef", rows)):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if k == 2:
                    self.play(Create(boxes[0]))
                if k == 4:
                    self.play(Create(boxes[1]))
        self.clear_scene()

    def picture(self):
        M = load("macro2")
        res, haz = M["res"], M["hazard"]
        D = M["D"]
        # left to right: the spell as it passes, d = D, D-1, ..., 0
        xs = np.arange(D + 1)
        r_by_time = [res[D - k] for k in xs]
        h_by_time = [haz[D - k] for k in xs]
        ax = plane([-0.6, D + 0.6], [0.7, 0.84], center=LEFT * 2.6 + UP * 0.6, x_length=7.2, y_length=3.0,
                   xticks=list(range(0, D + 1, 2)), yticks=[0.72, 0.76, 0.80], xlabel=r"",
                   ylabel=r"reservation wage", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.2f}", font_size=14)
        bars = VGroup()
        for x, r in zip(xs, r_by_time):
            p0, p1 = ax.ax.c2p(x - 0.32, 0.7), ax.ax.c2p(x + 0.32, r)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=MACRO if x < D else ERR,
                               fill_opacity=0.8, stroke_width=0).move_to((p0 + p1) / 2))
        forever = DashedLine(ax.ax.c2p(-0.6, M["res_inf"]), ax.ax.c2p(D + 0.6, M["res_inf"]), color=GREY_B,
                             stroke_width=1.8)
        fl = label(r"benefits for ever", font_size=15, color=GREY_B).next_to(ax.ax.c2p(D + 0.6, M["res_inf"]),
                                                                              RIGHT, buff=0.1)
        axh = plane([-0.6, D + 0.6], [0.15, 0.3], center=LEFT * 2.6 + DOWN * 2.35, x_length=7.2, y_length=1.9,
                    xticks=list(range(0, D + 1, 2)), yticks=[0.2, 0.25], xlabel=r"periods since the spell began",
                    ylabel=r"chance of leaving", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.2f}",
                    font_size=14)
        hl = path(axh, xs, h_by_time, GAIN, 2.6, smooth=False)
        hd = VGroup(*[dot(axh, x, h, GAIN, 0.05) for x, h in zip(xs, h_by_time)])
        side = VGroup(
            label(r"orange: \ benefits still paid", font_size=19, color=MACRO),
            label(r"red: \ benefits exhausted", font_size=19, color=ERR),
            label(rf"leaving rises from \\ {h_by_time[0]:.2f} to {h_by_time[-1]:.2f} a period", font_size=19,
                  color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Part c. <bookmark mark='a'/> Follow a spell from the start: the reservation wage falls period by "
            "period as exhaustion approaches, <bookmark mark='b'/> and drops to its lowest once benefits have run "
            "out. <bookmark mark='c'/> The chance of accepting an offer is one minus the reservation wage, so it "
            f"rises over the spell, from {h_by_time[0]:.2f} to {h_by_time[-1]:.2f} a period: job seekers become "
            "less choosy as the money runs out."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(forever), FadeIn(fl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[:-1]], lag_ratio=0.2), FadeIn(side[0]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[-1], DOWN), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(axh), Create(hl), FadeIn(hd), FadeIn(side[2]), run_time=1.5)
        self.clear_scene()

    def evidence(self):
        cards = VGroup(
            history_card(1990, r"Lawrence Katz and Bruce Meyer", r"American spells: \ the rate of leaving "
                         r"unemployment rises sharply in the weeks around benefit exhaustion", color=MACRO,
                         width=11.0, font_size=22),
            history_card(2007, r"David Card, \ Raj Chetty and Andrea Weber", r"Austrian records: \ the spike in "
                         r"leaving the unemployment register is far larger than the spike in starting new jobs",
                         color=GAIN, width=11.0, font_size=22),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"and in the data?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(r"Katz and Meyer, \ J. Public Econ. 41 (1990); \ Card, \ Chetty and Weber, \ AER P\&P "
                            r"97(2) (2007)", corner=DR, font_size=12)
        with self.voiceover(
            "And in the data? <bookmark mark='a'/> Lawrence Katz and Bruce Meyer found that American job seekers "
            "leave unemployment much faster in the weeks around exhaustion. <bookmark mark='b'/> David Card, Raj "
            "Chetty and Andrea Weber, with Austrian records, found that the spike in leaving the unemployment "
            "register is far larger than the spike in starting a job: many people simply stop being counted. An "
            "exam answer that predicts a rising exit rate is right; one that adds that the data distinguish "
            "finding a job from leaving the register earns the extra mark."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("ab", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"one reservation wage for the whole spell: \ the problem is not stationary until benefits end",
            r"starting the recursion at the first period: \ backward induction starts at exhaustion",
            r"valuing a job at $w$ rather than $w/(1 - \beta)$",
            r"proving monotonicity by intuition alone: \ the operator is monotone and $b > z$; \ say so",
        ]).move_to(UP * 0.2)
        take = label(r"a deadline makes a stationary problem a sequence: \ solve the end first", font_size=23,
                     color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> One reservation wage for the whole spell. <bookmark "
            "mark='b'/> Starting the recursion at the wrong end. <bookmark mark='c'/> Valuing a job at one "
            "period's wage. <bookmark mark='d'/> And asserting that the reservation wage falls without the "
            "two-line proof. <bookmark mark='e'/> The idea to keep, from Parts twenty-four and forty-two: a "
            "deadline turns a stationary problem into a sequence, and you solve the end first."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()
