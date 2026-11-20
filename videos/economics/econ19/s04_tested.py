from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403

ERA = ((1270, 1639, WAGE, r"1270--1639"), (1640, 1799, GREY_B, r"1640--1799"), (1800, 1859, GDP, r"1800--1859"))


class Tested(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Malthus tested", r"Did more people really mean lower wages, \ and did better technology buy "
             r"people rather than income?", "Chapter three. Malthus tested.",
             lit={2007: r"Clark", 2011: r"Ashraf and Galor"}, scale=("nation", "world"), horizon=("a century",))
        self.curve()
        self.errors()
        self.across()

    def curve(self):
        e = load("elasticity")
        pts = e["points"]
        lx = [np.log10(q["pop"]) for q in pts]
        ly = [np.log10(q["wage"]) for q in pts]
        ax = plane([3.2, 4.3], [1.2, 1.9], center=LEFT * 2.2 + DOWN * 0.45, x_length=7.2, y_length=5.0,
                   xticks=[np.log10(v) for v in (2000, 3000, 5000, 10000, 15000)],
                   yticks=[np.log10(v) for v in (20, 30, 50, 70)],
                   xlabel=r"England's population, \ thousands \ (log scale)", ylabel=r"real wages \ (log scale)",
                   xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{10 ** v:.0f}",
                   font_size=16)
        dots = VGroup()
        for q, x, y in zip(pts, lx, ly):
            c = next(col for a, b, col, _ in ERA if a <= q["decade"] <= b)
            dots.add(Dot(ax.ax.c2p(x, y), radius=0.06, color=c))
        b = e["before"]
        xs = np.array([np.log10(1800), np.log10(5600)])
        fit = Line(ax.ax.c2p(xs[0], (b["intercept"] + b["slope"] * np.log(10 ** xs[0])) / np.log(10)),
                   ax.ax.c2p(xs[1], (b["intercept"] + b["slope"] * np.log(10 ** xs[1])) / np.log(10)),
                   color=WAGE, stroke_width=3)
        leg = VGroup(*[VGroup(Dot(radius=0.07, color=c), label(t, font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.1)
                       for _, _, c, t in ERA]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(
            ax.ax.c2p(4.1, 1.83))
        a_ = e["after"]
        rows = VGroup(
            label(r"each dot: \ one decade's average", font_size=20, color=GREY_A),
            label(rf"1270--1640: \ slope {b['slope']:.2f} \ (s.e. {b['se_nw']:.2f}), \ $R^2$ {b['r2']:.2f}",
                  font_size=21, color=WAGE),
            label(r"1\% more people, \ about 0.9\% lower wages", font_size=21, color=WAGE),
            label(rf"1600--1800: \ slope ${a_['slope']:+.2f}$: \ the curve stops binding", font_size=21, color=GDP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3).shift(UP * 0.6)
        tag = agora_tag(corner=DR, font_size=14)
        src = data_tag(data.cite("millennium"), corner=DL, font_size=12)
        with self.voiceover(
            "The first prediction: more people, lower wages. <bookmark mark='a'/> Here is every decade of England "
            "from 1270 to 1860, its population across and its real wage up, both on log scales. "
            "<bookmark mark='b'/> Until about 1640 the decades lie along a falling line. Agora fits it: a slope of "
            f"{say_num(b['slope'], 2)}, with a standard error, allowing for decades that follow one another, of "
            f"{b['se_nw']:.2f}. <bookmark mark='c'/> One percent more people meant about nine tenths of a percent lower "
            "wages. That is Malthus's labour demand curve, and population explains four fifths of the swings in "
            "wages. <bookmark mark='d'/> After 1600 the dots climb to the right: more people and higher wages at "
            "once. The curve has stopped binding. That is what an escape looks like in the data."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(leg), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), FadeIn(rows[0]), run_time=4)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), *[Indicate(d, color=GDP, scale_factor=1.6) for q, d in zip(pts, dots)
                                         if q["decade"] >= 1800])
        self.clear_scene()

    def errors(self):
        e = load("elasticity")["before"]
        yrs = np.array(e["years"], float)
        u = np.array(e["residuals"])
        top = plane([1265, 1645], [-0.6, 0.4], center=UP * 1.45 + LEFT * 1.6, x_length=8.8, y_length=2.7,
                    xticks=[1300, 1400, 1500, 1600], yticks=[-0.5, 0, 0.3], xfmt=lambda v: f"{v:.0f}",
                    ylabel=r"residual, \ log wage", yfmt=lambda v: f"{v:.1f}", font_size=14)
        zero = DashedLine(top.ax.c2p(1265, 0), top.ax.c2p(1645, 0), color=GREY_B, stroke_width=1.5)
        res = path(top, yrs, u, color=WAGE, width=2.5, smooth=False)
        lags = ["0", "5", "10", "20", "40"]
        se = [e["se_by_lag"][k] for k in lags]
        bot = plane([-0.5, 4.5], [0, 0.08], center=DOWN * 1.85 + LEFT * 1.6, x_length=8.8, y_length=2.5,
                    xticks=[], yticks=[0, 0.04, 0.08], ylabel=r"standard error \\ of the slope",
                    yfmt=lambda v: f"{v:.2f}", font_size=14)
        bars = VGroup()
        for i, (k, v) in enumerate(zip(lags, se)):
            h = bot.ax.c2p(0, v)[1] - bot.ax.c2p(0, 0)[1]
            r = Rectangle(width=1.0, height=h, stroke_width=0, fill_color=WAGE if k != "10" else E.ACCENT,
                          fill_opacity=0.85).move_to(bot.ax.c2p(i, 0), aligned_edge=DOWN)
            lab = VGroup(label(r"no lags \\ (HC1)" if k == "0" else rf"{k} years", font_size=14, color=GREY_A),
                         label(f"{v:.3f}", font_size=14, color=WHITE))
            lab[0].next_to(r, DOWN, buff=0.08)
            lab[1].next_to(r, UP, buff=0.05)
            bars.add(VGroup(r, lab))
        side = VGroup(
            label(rf"neighbouring years' errors: \\ correlation {e['rho1']:.2f}", font_size=20, color=WAGE),
            MathTex(r"\hat S = \sum_{\ell=-L}^{L}\Big(1-\tfrac{|\ell|}{L+1}\Big)\hat\Gamma_\ell", font_size=30),
            label(r"Newey and West, \ 1987: \\ add the covariances, \ down-weighted", font_size=18, color=GREY_A),
            label(rf"even at 40 years: \\ the slope is {abs(e['slope']) / se[-1]:.0f} \\ standard errors from zero",
                  font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Newey and West, Econometrica 55(3) (1987)", corner=DR, font_size=12)
        with self.voiceover(
            "A word on that standard error, because time series need care. <bookmark mark='a'/> Here are the "
            "regression's residuals, year by year: what wages did that population does not explain. They wander in "
            f"long swings. A year's error is correlated with the next year's, at {e['rho1']:.2f}. "
            "<bookmark mark='b'/> So the {n} years are not {n} independent pieces of evidence. The usual formula, "
            f"even the one robust to unequal variances, treats them as if they were, and gives {e['se_hc1']:.3f}. "
            "<bookmark mark='c'/> Whitney Newey and Kenneth West's estimator adds the covariances between nearby "
            "years, each down-weighted the further apart they are. With ten years of lags, the standard error more "
            f"than doubles, to {e['se_by_lag']['10']:.3f}. <bookmark mark='d'/> How many lags is a judgment, so "
            "check it: with forty years, the error is larger still, and the slope is still about "
            f"{abs(e['slope']) / se[-1]:.0f} standard errors from zero. The conclusion does not depend on the choice."
            .replace("{n}", str(e["n"]))
        ) as vo:
            self.play(FadeIn(top), Create(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(res), run_time=3, rate_func=linear)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bot), FadeIn(bars[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(bars[1]), FadeIn(bars[2]))
            vo.wait_until("d")
            self.play(FadeIn(bars[3]), FadeIn(bars[4]), FadeIn(side[3]))
        self.clear_scene()

    def across(self):
        rows = VGroup(
            label(r"the second prediction: \ better technology buys people, \ not income", font_size=25),
            label(r"Quamrul Ashraf and Oded Galor, \ 2011: \ countries in the years 1 to 1500", font_size=23,
                  color=TECH),
            label(r"an earlier start to farming, \ or better land: \ far denser populations", font_size=23,
                  color=POP),
            label(r"but no measurable gain in income per head", font_size=23, color=WAGE),
            label(r"Gregory Clark: \ the average person in 1800 lived no better than the average hunter-gatherer",
                  font_size=21, color=GREY_A),
            label(r"a bold claim, \ much disputed in its detail, \ but the broad pattern is not", font_size=21,
                  color=HOLD),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Ashraf and Galor, AER 101(5) (2011); \ Clark, \emph{A Farewell to Alms} (2007)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The second prediction is bolder. <bookmark mark='a'/> Better technology should buy people, not income. "
            "<bookmark mark='b'/> Quamrul Ashraf and Oded Galor tested it across countries in the years 1 to 1500. "
            "<bookmark mark='c'/> Places where farming began earlier, or whose land was better, had far denser "
            "populations, <bookmark mark='d'/> but no measurable advantage in income per head. "
            "<bookmark mark='e'/> Gregory Clark went further: the average person in 1800, he argued, lived no better "
            "than the average hunter-gatherer. <bookmark mark='f'/> That claim is much disputed in its detail. The "
            "broad pattern, technology turning into people, is not."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
