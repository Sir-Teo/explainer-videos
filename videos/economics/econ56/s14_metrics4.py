from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403


def mat(M, digits: int = 2) -> str:
    rows = [" & ".join(f"{v:.{digits}f}" for v in r) for r in M]
    return r"\begin{pmatrix} " + r" \\ ".join(rows) + r" \end{pmatrix}"


class Metrics4(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Econometrics: \ a VAR with a long-run restriction", r"Can what lasts for ever identify "
             r"what happens now?", "Question twelve. Econometrics: a VAR with a long-run restriction.",
             lit={1989: r"Blanchard and Quah", 1997: r"Faust and Leeper", 1999: r"Gal\'i"},
             scale=("nation",), horizon=("a decade",))
        self.statement()
        self.solve()
        self.picture()
        self.marks()

    def statement(self):
        M = load("metrics4")
        S = np.array(M["Sigma"])
        lines = [
            rf"Output growth and unemployment follow $y_t = A\,y_{{t-1}} + u_t$, \ with $A = {mat(M['A'])}$ and "
            rf"$\mathbb{{E}}[u_t u_t'] = \Sigma = {mat(S)}$. \ There are two orthogonal shocks of unit variance, \ "
            r"$u_t = B\,\varepsilon_t$: \ supply, \ which may move output's level for ever, \ and demand, \ which "
            r"cannot.",
            r"(a) \ Count the unknowns and the restrictions. \quad (6 marks)",
            r"(b) \ Show how the long-run restriction identifies $B$. \quad (10 marks)",
            r"(c) \ Compute $B$, \ and say how well it is estimated from 400 quarters. \quad (9 marks)",
        ]
        paper = exam_paper(12, "metrics", r"a long-run restriction", lines).move_to(UP * 0.4)
        with self.voiceover(
            "The last question. Output growth and unemployment follow a first-order vector autoregression, with "
            "the matrix A and the covariance of the surprises given. Two shocks drive it: supply, which may move "
            "the level of output for ever, and demand, which cannot. <bookmark mark='a'/> Part a: count the "
            "unknowns. <bookmark mark='b'/> Part b: show how the long-run restriction identifies the impact "
            "matrix. <bookmark mark='c'/> Part c: compute it, and say how well it can be estimated. Pause: where "
            "does the zero go?"
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("abc", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 7.0)
        self.clear_scene()

    def solve(self):
        M = load("metrics4")
        tag = part_tag(12, "a--c", "metrics")
        bm, bs = np.array(M["B_est_mean"]), np.array(M["B_est_sd"])
        rows = steps([
            (r"B:\ 4 \text{ unknowns}; \qquad \Sigma = BB':\ 3 \text{ equations}", r"one restriction short"),
            (r"\textstyle\sum_{h \ge 0} \partial \Delta y_{t+h} / \partial \varepsilon_t = \big[C(1)\,B\big]_{1\cdot},"
             r" \qquad C(1) = (I - A)^{-1}", r"the effect on output's level is the sum of the effects on its growth"),
            (r"\big[C(1)\,B\big]_{12} = 0", r"demand cannot move output's level for ever", GAIN),
            (r"C(1)\,\Sigma\,C(1)' = \big(C(1)B\big)\big(C(1)B\big)' \ \Rightarrow\ C(1)B = \operatorname{chol}"
             r"\big(C(1)\Sigma C(1)'\big)", r"a lower-triangular square root is unique, \ up to signs"),
            (rf"B = C(1)^{{-1}} \operatorname{{chol}}(\cdot) = {mat(M['B'])}", r"signs: \ supply raises output; \ "
             r"demand lowers unemployment", GAIN),
            (rf"{M['reps']} \text{{ samples of }} {M['T']}: \ \hat b_{{11}} = {bm[0, 0]:.2f}\ ({bs[0, 0]:.2f}), \ \ "
             rf"\hat b_{{12}} = {bm[0, 1]:.2f}\ ({bs[0, 1]:.2f})", r"the long run is read from the VAR's "
             r"persistence: \ imprecise"),
        ], math_size=27, buff=0.27)
        rows.move_to(DOWN * 0.1)
        boxes = [answer_box(rows[2][0]), answer_box(rows[4][0])]
        with self.voiceover(
            "Part a. <bookmark mark='a'/> The impact matrix B has four entries; the covariance of the surprises "
            "gives three equations. One short, as in Part fifty-five. <bookmark mark='b'/> Part b. A shock's effect "
            "on the level of output is the sum of its effects on output growth, which is the first row of C of "
            "one times B, with C of one the inverse of I minus A. <bookmark mark='c'/> The restriction: demand's "
            "entry there is zero. <bookmark mark='d'/> Then C of one times Sigma times its transpose equals C of "
            "one B times its own transpose, and C of one B is lower triangular: it is the Cholesky factor, unique "
            "up to the signs of its columns. <bookmark mark='e'/> Multiply back by the inverse of C of one, "
            "choose the signs so that supply raises output and demand lowers unemployment, and B is recovered "
            f"exactly. <bookmark mark='f'/> Part c. In {M['reps']} simulated samples of {M['T']} quarters, the "
            "estimates are centred on the truth, but with standard deviations of a tenth to a fifth of their size: "
            "the long run is read from how persistent the autoregression is, and persistence is hard to estimate. "
            "Jon Faust and Eric Leeper warned that long-run restrictions can be unreliable for exactly this "
            "reason."
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
        M = load("metrics4")
        h = np.arange(len(M["level_supply"]))
        axl = plane([0, 20], [-0.2, 1.4], center=LEFT * 3.3 + DOWN * 0.3, x_length=5.2, y_length=4.6,
                    xticks=[0, 5, 10, 15, 20], yticks=[0, 0.5, 1.0], xlabel=r"quarters",
                    ylabel=r"output's level", xfmt=lambda x: f"{x:.0f}",
                    yfmt=lambda y: f"{y:.1f}" if y else "0", font_size=14)
        axr = plane([0, 20], [-0.4, 0.2], center=RIGHT * 2.6 + DOWN * 0.3, x_length=5.2, y_length=4.6,
                    xticks=[0, 5, 10, 15, 20], yticks=[-0.4, -0.2, 0, 0.2], xlabel=r"quarters",
                    ylabel=r"unemployment", xfmt=lambda x: f"{x:.0f}",
                    yfmt=lambda y: f"{y:+.1f}".replace("-", "{-}") if y else "0", font_size=14)
        zs = VGroup(*[DashedLine(a.ax.c2p(0, 0), a.ax.c2p(20, 0), color=GREY_D, stroke_width=1) for a in (axl, axr)])
        sup = VGroup(path(axl, h, M["level_supply"], SUPPLY, 3.0), path(axr, h, M["u_supply"], SUPPLY, 3.0))
        dem = VGroup(path(axl, h, M["level_demand"], DEMAND, 3.0), path(axr, h, M["u_demand"], DEMAND, 3.0))
        key = VGroup(label(r"green: \ supply", font_size=19, color=SUPPLY),
                     label(r"gold: \ demand", font_size=19, color=DEMAND)).arrange(RIGHT, buff=0.8).to_edge(
            UP, buff=0.45)
        lr = label(rf"for ever: \ ${np.array(M['L'])[0, 0]:.2f}$", font_size=17, color=SUPPLY).next_to(
            axl.ax.c2p(20, M["level_supply"][-1]), UP, buff=0.12).shift(LEFT * 0.6)
        with self.voiceover(
            "The picture. <bookmark mark='a'/> A supply shock raises output's level for good, to "
            f"{np.array(M['L'])[0, 0]:.2f}, and nudges unemployment down for a while. <bookmark mark='b'/> A "
            "demand shock raises output at first, and the level returns to where it started, by construction; "
            "unemployment falls and recovers. The zero was imposed at infinity, and it shapes every quarter "
            "before it."
        ) as vo:
            self.play(FadeIn(axl), FadeIn(axr), FadeIn(zs), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(sup), FadeIn(lr), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(dem), run_time=1.5)
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"putting the zero in $B$, \ the impact, \ instead of in $C(1)B$, \ the long run",
            r"taking the Cholesky factor of $\Sigma$: \ that is a timing restriction",
            r"output in levels in the VAR: \ the restriction is on the cumulated response of growth",
            r"no sign normalization: \ $B$ is identified only up to the sign of each column",
        ]).move_to(UP * 0.2)
        take = label(r"one zero at infinity buys the whole impact matrix, \ at the price of precision", font_size=23,
                     color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> Putting the zero in the impact matrix. <bookmark "
            "mark='b'/> Taking the Cholesky factor of Sigma, which is a different assumption, about timing. "
            "<bookmark mark='c'/> Putting output in levels. <bookmark mark='d'/> And forgetting the signs. "
            "<bookmark mark='e'/> The idea to keep, from Part fifty-five: one zero at infinity buys the whole "
            "impact matrix, at the price of precision."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()
