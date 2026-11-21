from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

LINES = [
    r"On 2{,}000 days a market's demand and supply are $q = a - b\,p + u_d$ and $q = c + d\,p + e\,w + u_s$, \ where "
    r"$w = 1$ on stormy days \ (about 30\% of them) \ and $e < 0$. \ The shocks $u_d$, $u_s$ are independent of each "
    r"other and of $w$.",
    r"(a) \ Which equation is identified? \ Use the order and rank conditions. \quad (8 marks)",
    r"(b) \ Show that the least-squares slope of $q$ on $p$ does not estimate $-b$. \quad (8 marks)",
    r"(c) \ Give a consistent estimator of $b$, \ and compute it from the data. \quad (9 marks)",
]


class Metrics1(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Econometrics: \ identifying a demand curve", r"How can prices and quantities alone reveal "
             r"a demand curve?", "Question nine. Econometrics: identifying a demand curve.",
             lit={1928: r"Philip Wright", 1940: r"Wald", 1950: r"the Cowles Commission"},
             scale=("market",), horizon=("a day", "a year"))
        self.statement()
        self.solve()
        self.picture()
        self.marks()

    def statement(self):
        paper = exam_paper(9, "metrics", r"supply and demand", LINES).move_to(UP * 0.5)
        with self.voiceover(
            "Question nine, the first in econometrics. On two thousand days we see a market's price and quantity. "
            "Demand slopes down with slope minus b; supply slopes up, and storms, on about three days in ten, cut "
            "it. <bookmark mark='a'/> Part a: which equation is identified? <bookmark mark='b'/> Part b: show that "
            "least squares fails. <bookmark mark='c'/> Part c: a consistent estimator, computed. Pause: which "
            "curve does a storm move?"
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("abc", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 7.0)
        self.clear_scene()

    def solve(self):
        M = load("metrics1")
        tag = part_tag(9, "a--c", "metrics")
        rows = steps([
            (r"\text{demand excludes } w: \ 1 \text{ excluded instrument} \ge 1 \text{ endogenous regressor}",
             r"order condition: \ exactly identified"),
            (r"e \ne 0", r"rank condition: \ storms must actually move supply"),
            (r"\text{supply excludes nothing} \ \Rightarrow\ \text{not identified}",
             r"no observed variable shifts demand alone"),
            (rf"\operatorname{{plim}}\,\hat\beta_{{\text{{OLS}}}} = -b + \frac{{\sigma_d^2}}{{(b + d)\,"
             rf"\operatorname{{Var}}(p)}} = {say_tex(M['plim_ols'])}, \quad \text{{sample: }} {say_tex(M['ols'])}",
             r"demand shocks move the price too: \ simultaneity"),
            (rf"\hat b_{{\text{{Wald}}}}:\ \ \frac{{\bar q_1 - \bar q_0}}{{\bar p_1 - \bar p_0}} = "
             rf"\frac{{{say_tex(M['dq'])}}}{{{M['dp']:.2f}}} = {say_tex(M['wald'])} \ \ ({M['se_wald']:.2f})",
             r"storm days against calm days: \ supply slides along demand", GAIN),
            (r"\text{truth: } -1", r"(the data are simulated, \ so we can check)"),
        ], math_size=28, buff=0.28)
        rows.move_to(DOWN * 0.1)
        box = answer_box(rows[4][0])
        with self.voiceover(
            "Part a. <bookmark mark='a'/> The demand equation leaves out the storm variable, which appears in "
            "supply: one excluded instrument for one endogenous regressor, the price. That is the order condition, "
            "and demand is exactly identified, <bookmark mark='b'/> provided storms really move supply, the rank "
            "condition. <bookmark mark='c'/> Supply leaves nothing out, so nothing identifies it. <bookmark "
            "mark='d'/> Part b. Least squares regresses quantity on a price that demand shocks also move. In "
            f"the limit it gives {say_num(M['plim_ols'], 2)}, a blend of the two slopes, and in this sample "
            f"{say_num(M['ols'], 2)}. <bookmark mark='e'/> Part c. Compare storm days with calm days. A storm moves "
            "supply only, so price and quantity slide along the demand curve, and the ratio of the change in "
            f"quantity to the change in price is the slope: {say_num(M['wald'], 2)}, with a standard error of "
            f"{M['se_wald']:.2f}. That is Wald's estimator, and two-stage least squares with one binary "
            "instrument. <bookmark mark='f'/> The truth, since these days are simulated, is minus one."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if mk == "e":
                    self.play(Create(box))
        self.clear_scene()

    def picture(self):
        M = load("metrics1")
        p, q, w = np.array(M["p"]), np.array(M["q"]), np.array(M["w"])
        mm = M["means"]
        ax = plane([1.5, 7.5], [2, 9.5], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=5.6,
                   xticks=[2, 4, 6], yticks=[3, 5, 7, 9], xlabel=r"price $p$", ylabel=r"quantity $q$",
                   xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}", font_size=15)
        calm = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.03, color=GREY_B, fill_opacity=0.55)
                        for a, b, s in zip(p, q, w) if s < 0.5 and 1.5 < a < 7.5 and 2 < b < 9.5])
        storm = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.035, color=METRICS, fill_opacity=0.8)
                         for a, b, s in zip(p, q, w) if s > 0.5 and 1.5 < a < 7.5 and 2 < b < 9.5])
        truth = seg(ax, 1.5, 10 - 1.5, 7.5, 10 - 7.5, WHITE, 2.4)
        m0, m1 = dot(ax, mm["p0"], mm["q0"], EST, 0.1), dot(ax, mm["p1"], mm["q1"], EST, 0.1)
        wald = Line(ax.ax.c2p(mm["p0"] - 1.5, mm["q0"] - 1.5 * M["wald"]),
                    ax.ax.c2p(mm["p1"] + 1.5, mm["q1"] + 1.5 * M["wald"]), color=EST, stroke_width=3.2)
        pm, qm = float(np.mean(p)), float(np.mean(q))
        ols = Line(ax.ax.c2p(pm - 2.5, qm - 2.5 * M["ols"]), ax.ax.c2p(pm + 2.5, qm + 2.5 * M["ols"]), color=ERR,
                   stroke_width=2.6)
        side = VGroup(
            label(r"grey: \ calm days; \ purple: \ storms", font_size=18, color=GREY_A),
            label(r"white: \ the true demand curve", font_size=18, color=WHITE),
            label(rf"red: \ least squares, \ ${say_tex(M['ols'])}$", font_size=18, color=ERR),
            label(rf"gold: \ the two means, \ joined: \\ Wald, \ ${say_tex(M['wald'])}$", font_size=18, color=EST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"simulated: \ 2{,}000 days, \ 400 shown", corner=DR, font_size=13)
        with self.voiceover(
            "The picture. <bookmark mark='a'/> Each dot is a day, purple if stormy. The cloud slopes only gently "
            "down, because both curves move. <bookmark mark='b'/> In white, the demand curve we want. <bookmark "
            "mark='c'/> Least squares through the cloud is far too flat. <bookmark mark='d'/> But the average "
            "calm day and the average stormy day both lie on the demand curve, since storms move only supply; the "
            "line through them is the Wald estimate."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(calm), FadeIn(storm), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ols), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(m0), FadeIn(m1), Create(wald), FadeIn(side[3]))
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"using the storm to estimate supply: \ an instrument identifies the equation it is excluded from",
            r"stating the order condition as if it were sufficient: \ rank needs $e \ne 0$",
            r"asserting the exclusion restriction instead of arguing it: \ do storms change what people want?",
            r"reporting the reduced form, \ $\bar q_1 - \bar q_0$, \ as the demand slope",
        ]).move_to(UP * 0.2)
        take = label(r"a variable that moves one curve traces out the other", font_size=23,
                     color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> Using the storm to estimate supply. <bookmark mark='b'/> "
            "Treating the order condition as sufficient. <bookmark mark='c'/> Asserting the exclusion restriction "
            "instead of arguing it: if storms keep shoppers at home, they move demand too, and the estimator "
            "fails. <bookmark mark='d'/> And reporting the change in quantity as if it were the slope. <bookmark "
            "mark='e'/> The idea to keep, from Part four and Philip Wright's tariff study of 1928: a variable that "
            "moves one curve traces out the other."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()

