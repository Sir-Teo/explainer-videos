from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

LINES = [
    r"Three units are observed for 10 periods. \ Unit E adopts a policy in period 3, \ unit L in period 7, \ and "
    r"unit N never. \ The effect grows with exposure: \ 1 in the first period of adoption, \ 2 in the second, \ and "
    r"so on. \ $Y_{it} = \alpha_i + \lambda_t + \tau_{it}$, \ with no noise.",
    r"(a) \ What is the average effect on the treated cells, \ and what does the two-way fixed-effects regression "
    r"of $Y$ on $D$ estimate? \quad (9 marks)",
    r"(b) \ Decompose that estimate into two-by-two comparisons. \quad (9 marks)",
    r"(c) \ Propose an estimator that recovers the average effect. \quad (7 marks)",
]


class Metrics3(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Econometrics: \ staggered difference-in-differences", r"What does two-way fixed effects "
             r"estimate when units adopt at different times?", "Question eleven. Econometrics: staggered "
             "difference-in-differences.", lit={2020: r"de Chaisemartin and D'Haultf{\oe}uille",
                                                2021: r"Goodman-Bacon; \ Callaway and Sant'Anna",
                                                2024: r"Borusyak, \ Jaravel and Spiess"},
             scale=("city", "nation"), horizon=("a decade",))
        self.statement()
        self.solve()
        self.picture()
        self.marks()

    def statement(self):
        paper = exam_paper(11, "metrics", r"staggered timing", LINES).move_to(UP * 0.5)
        with self.voiceover(
            "Question eleven. Three units over ten periods: E adopts a policy in period three, L in period seven, "
            "N never. The effect grows the longer a unit has had the policy: one, then two, then three. There is "
            "no noise at all, so every number is exact. <bookmark mark='a'/> Part a: the average effect on the "
            "treated, and what two-way fixed effects estimates. <bookmark mark='b'/> Part b: decompose it. "
            "<bookmark mark='c'/> Part c: an estimator that gets it right. Pause, and compute the true average "
            "first."
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("abc", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 7.0)
        self.clear_scene()

    def solve(self):
        M = load("metrics3")
        parts = {(b["kind"], b["g"]): b for b in M["bacon"]}
        en, ln = parts[("vs never", 3.0)], parts[("vs never", 7.0)]
        el, le = parts[("early vs later", 3.0)], parts[("later vs earlier", 7.0)]
        tag = part_tag(11, "a--c", "metrics")
        rows = steps([
            (rf"\text{{ATT}} = \frac{{(1 + \dots + 8) + (1 + \dots + 4)}}{{12}} = {M['att']:.2f}",
             r"8 treated periods for E, \ 4 for L", GAIN),
            (rf"\hat\beta_{{\text{{TWFE}}}} = \frac{{\sum \tilde D_{{it}} Y_{{it}}}}{{\sum \tilde D_{{it}}^2}} = "
             rf"{M['twfe']:.2f}", r"the regression with unit and period effects"),
            (rf"E \text{{ vs }} N: \ {en['est']:.1f}\ \ (w = {en['w']:.3f}), \qquad L \text{{ vs }} N: \ "
             rf"{ln['est']:.1f}\ \ (w = {ln['w']:.3f})", r"(b) \ clean comparisons with the never-treated"),
            (rf"E \text{{ vs }} L,\ \text{{before }} L: \ {el['est']:.1f}\ \ (w = {el['w']:.3f})",
             r"clean: \ L has not started"),
            (rf"L \text{{ vs }} E,\ \text{{after }} E: \ {say_tex(le['est'], 1)}\ \ (w = {le['w']:.3f})",
             r"forbidden: \ E's growing effect is used as a control", ERR),
            (rf"\textstyle\sum w \cdot \text{{est}} = {M['twfe']:.2f} \ne {M['att']:.2f}", r"the weights sum to one"),
            (rf"\hat Y_{{it}}(0) = \hat\alpha_i + \hat\lambda_t \text{{ from untreated cells}} \ \Rightarrow\ "
             rf"\text{{mean}}(Y - \hat Y(0)) = {M['imputation']:.2f}", r"(c) \ imputation: \ compare only with "
             r"what is untreated", GAIN),
        ], math_size=27, buff=0.24)
        rows.move_to(DOWN * 0.15)
        boxes = [answer_box(rows[0][0]), answer_box(rows[6][0])]
        with self.voiceover(
            "Part a. <bookmark mark='a'/> E is treated for eight periods, with effects one to eight; L for four, "
            f"with effects one to four. The average over the twelve treated cells is {M['att']:.2f}. <bookmark "
            "mark='b'/> The two-way fixed-effects regression, with a dummy for each unit and each period, gives "
            f"{M['twfe']:.2f}: barely half. <bookmark mark='c'/> Part b. Andrew Goodman-Bacon showed it is a "
            "weighted average of every two-by-two comparison. E against N, and L against N, are clean. <bookmark "
            "mark='d'/> So is E against L before L starts. <bookmark mark='e'/> But L against E after E has "
            "started uses E as a control while E's effect is still growing. L's own effect, two and a half, "
            f"minus E's growth of four, gives {say_num(le['est'], 1)}, and it gets a quarter of the weight. "
            "<bookmark mark='f'/> The weighted sum is exactly two. <bookmark mark='g'/> Part c. Fit the unit and "
            "period effects on untreated cells only, impute what each treated cell would have been without the "
            f"policy, and average the difference: {M['imputation']:.2f}, the truth. Callaway and Sant'Anna's "
            "estimator, which compares each cohort only with clean controls, gets it too."
        ) as vo:
            self.play(FadeIn(tag))
            for k, (mk, r_) in enumerate(zip("abcdefg", rows)):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if k == 0:
                    self.play(Create(boxes[0]))
                if k == 6:
                    self.play(Create(boxes[1]))
        self.clear_scene()

    def picture(self):
        M = load("metrics3")
        Y, W, D = np.array(M["Y"]), np.array(M["weights"]), np.array(M["D"])
        t = np.array(M["times"])
        cols = (METRICS, EST, GREY_B)
        names = ("E", "L", "N")
        ax = plane([1, 10], [0, 12], center=LEFT * 3.4 + DOWN * 0.3, x_length=5.4, y_length=4.8,
                   xticks=[1, 3, 5, 7, 9], yticks=[0, 4, 8, 12], xlabel=r"period", ylabel=r"$Y$",
                   xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}", font_size=14)
        lines = VGroup(*[path(ax, t, Y[i], cols[i], 2.8, smooth=False) for i in range(3)])
        tags = VGroup(*[label(names[i], font_size=20, color=cols[i]).next_to(ax.ax.c2p(10, Y[i, -1]), RIGHT,
                                                                                buff=0.1) for i in range(3)])
        adopt = VGroup(vline(ax, 3, 0, 12, METRICS, 1.5), vline(ax, 7, 0, 12, EST, 1.5))
        # the weight grid: rows E, L, N; columns 1..10
        grid = VGroup()
        cw, chh = 0.56, 0.62
        for i in range(3):
            for j in range(10):
                w = W[i][j]
                if D[i][j] < 0.5:
                    fc, op, txt = GREY_D, 0.25, ""
                elif w < 0:
                    fc, op, txt = ERR, 0.85, f"{w:.2f}".replace("-", "{-}")
                else:
                    fc, op, txt = GAIN, 0.6 + 2 * w, f"{w:.2f}"
                sq = Rectangle(width=cw, height=chh, stroke_color=GREY_D, stroke_width=1, fill_color=fc,
                               fill_opacity=min(op, 0.95))
                sq.move_to(RIGHT * (0.4 + j * cw) + UP * (0.5 - i * chh))
                cell = VGroup(sq)
                if txt:
                    cell.add(label(txt, font_size=13, color=WHITE).move_to(sq))
                grid.add(cell)
        rl = VGroup(*[label(n_, font_size=18, color=c_).next_to(grid[i * 10], LEFT, buff=0.15)
                      for i, (n_, c_) in enumerate(zip(names, cols))])
        cl = VGroup(*[label(str(j + 1), font_size=14, color=GREY_B).next_to(grid[20 + j], DOWN, buff=0.1)
                      for j in range(10)])
        head = label(r"TWFE's weight on each treated cell", font_size=20, color=WHITE).next_to(grid, UP, buff=0.3)
        note_ = label(rf"E's last four periods get negative weight: \\ $\hat\beta = \sum w_{{it}}\tau_{{it}} = "
                      rf"{M['twfe']:.2f}$", font_size=18, color=ERR).next_to(cl, DOWN, buff=0.35)
        worse = label(rf"without unit N: \ $\hat\beta = {say_tex(M['twfe_no_never'])}$, \ against an effect of "
                      rf"{M['att']:.2f}", font_size=18, color=ERR).next_to(note_, DOWN, buff=0.3)
        VGroup(head, grid, rl, cl, note_, worse).shift(RIGHT * 0.3)
        tag = island_tag(r"illustrative: \ exact, \ no noise", corner=DR, font_size=13)
        with self.voiceover(
            "The picture. <bookmark mark='a'/> The three units' outcomes: E bends up from period three, L from "
            "period seven, N never. <bookmark mark='b'/> On the right, the weight the regression puts on each "
            "treated cell. <bookmark mark='c'/> E's last four periods, where its effect is largest, get negative "
            "weight: the regression subtracts the very effects it should be averaging. <bookmark mark='d'/> Drop "
            "the never-treated unit and it gets worse: the coefficient becomes "
            f"{say_num(M['twfe_no_never'], 2)}, the wrong sign, for a policy that helps every unit that adopts it. "
            "That is the whole difficulty in one grid."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines), FadeIn(tags), Create(adopt), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(head), FadeIn(rl), FadeIn(cl), LaggedStart(*[FadeIn(c) for c in grid],
                                                                         lag_ratio=0.03), run_time=2.0)
            vo.wait_until("c")
            neg = VGroup(*[grid[j] for j in range(6, 10)])
            self.play(Indicate(neg, color=ERR, scale_factor=1.05), FadeIn(note_))
            vo.wait_until("d")
            self.play(FadeIn(worse, shift=UP * 0.1))
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"calling the two-way fixed-effects coefficient the average effect on the treated",
            r"using already-treated units as controls when effects change over time",
            r"believing parallel trends is enough: \ TWFE also needs effects that are the same for everyone, \ "
            r"always",
            r"an event study without a reference period, \ or with contaminated leads and lags",
        ]).move_to(UP * 0.2)
        take = label(r"compare the treated only with what is still untreated", font_size=23,
                     color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> Calling the coefficient the average effect. <bookmark "
            "mark='b'/> Using already-treated units as controls. <bookmark mark='c'/> Believing parallel trends "
            "is enough: this regression also needs the effect to be the same for every unit and every period. "
            "<bookmark mark='d'/> And an event study without a reference period. <bookmark mark='e'/> The idea "
            "to keep, from Part four and from Statistics, Built: compare the treated only with what is still "
            "untreated."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()
