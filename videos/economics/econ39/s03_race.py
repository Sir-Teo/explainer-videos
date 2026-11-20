from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Race(VoiceoverScene):
    def construct(self):
        card(self, 2, r"The race between education and technology",
             r"Why did the college premium rise, \ and why did it stall?",
             "Chapter two. The race between education and technology.",
             lit={1975: r"Tinbergen", 1992: r"Katz and Murphy", 2008: r"Goldin and Katz"}, scale=("nation",),
             horizon=("a decade",))
        self.model()
        self.regression()
        self.demand()

    def model(self):
        R = load("race")
        ys = R["years"]
        s0, s1 = R["supply"][0], R["supply"][-1]
        w0, w1 = R["premium"][0], R["premium"][-1]
        sig = R["km"]["sigma"]
        ax = plane([-0.4, 0.9], [0.2, 1.0], center=LEFT * 2.0 + DOWN * 0.5, x_length=7.6, y_length=4.8,
                   xticks=[-0.25, 0, 0.25, 0.5, 0.75], yticks=[0.2, 0.4, 0.6, 0.8, 1.0],
                   xlabel=r"relative supply: \ log of college over high-school workers",
                   ylabel=r"log college premium", xfmt=lambda v: f"{v:+.2f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        xs = np.linspace(-0.4, 0.9, 60)
        d0 = path(ax, xs, w0 - (xs - s0) / sig, DEMAND, 3.0, yr=(0.2, 1.0))
        d1 = path(ax, xs, w1 - (xs - s1) / sig, DEMAND, 3.0, yr=(0.2, 1.0))
        v0, v1 = vline(ax, s0, 0.2, 1.0, SUPPLY), vline(ax, s1, 0.2, 1.0, SUPPLY)
        p0, p1 = dot(ax, s0, w0, WHITE, 0.09), dot(ax, s1, w1, WHITE, 0.09)
        l0 = label(f"{ys[0]}", font_size=17, color=WHITE).next_to(p0, LEFT, buff=0.12)
        l1 = label(f"{ys[-1]}", font_size=17, color=WHITE).next_to(p1, RIGHT, buff=0.12)
        eq = MathTex(r"\ln\frac{w_H}{w_L} = \Big(1 - \frac{1}{\sigma}\Big)\ln\frac{A_H}{A_L} - "
                     r"\frac{1}{\sigma}\ln\frac{H}{L}", font_size=30).to_corner(UR, buff=0.4)
        side = VGroup(
            label(r"teal: \ supply, \ set by schooling", font_size=17, color=SUPPLY),
            label(r"red: \ demand, \ slope $-1/\sigma$", font_size=17, color=DEMAND),
            label(rf"supply rose {R['supply'][-1] - R['supply'][0]:.2f} log points; \\ the premium still rose: \\ "
                  r"demand must have moved", font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(eq, DOWN, buff=0.45).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"BLS via FRED; \ the canonical model", corner=DR, font_size=12)
        with self.voiceover(
            "The simplest explanation is a market for skill with two goods: college and high-school labour. "
            "<bookmark mark='a'/> In the 1970s Jan Tinbergen called it a race. Firms combine the two kinds of worker "
            "with "
            "an elasticity of substitution sigma; technology changes how productive each is. The college premium "
            "then depends on two things: relative demand, pushed up by technology, and relative supply, pushed up by "
            "schooling. <bookmark mark='b'/> Supply is set by how many people finish college: here it is, in "
            f"{ys[0]}, <bookmark mark='c'/> and demand slopes down, with slope minus one over sigma. "
            f"<bookmark mark='d'/> By {ys[-1]}, college graduates had become far more plentiful relative to "
            "high-school graduates, <bookmark mark='e'/> and yet the premium rose. With supply moving that far right, "
            "only a rightward shift in demand can explain it: technology must have raised the demand for skill."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Write(eq), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(v0), Create(d0), FadeIn(p0), FadeIn(l0), run_time=1.5)
            vo.wait_until("b")
            self.play(Indicate(v0, color=WHITE), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Indicate(d0, color=WHITE), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Create(v1))
            vo.wait_until("e")
            self.play(Create(d1), FadeIn(p1), FadeIn(l1), FadeIn(side[2]))
        self.clear_scene()

    def regression(self):
        R = load("race")
        N = R["naive"]
        K = R["km"]
        ys = np.array(R["years"])
        t = (ys - ys[0]) / (ys[-1] - ys[0])
        sup = np.array(R["supply"])
        sn = (sup - sup.min()) / (sup.max() - sup.min())
        ax = plane([1991, 2026], [0, 1], center=LEFT * 3.3 + DOWN * 0.5, x_length=5.6, y_length=4.0,
                   xticks=[1995, 2005, 2015, 2025], yticks=[0, 0.5, 1], ylabel=r"scaled from 0 to 1",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=13)
        lt = path(ax, ys, t, GREY_A, 2.4, smooth=False)
        ls = path(ax, ys, sn, SUPPLY, 3.0, smooth=False)
        keys = VGroup(label(r"grey: \ time", font_size=16, color=GREY_A),
                      label(r"teal: \ relative supply", font_size=16, color=SUPPLY)).arrange(RIGHT, buff=0.4).next_to(
            ax, UP, buff=0.2)
        km = VGroup(
            label(rf"Katz and Murphy, \ {K['first']}--{K['last']}:", font_size=21, color=E.ACCENT),
            MathTex(rf"\ln\frac{{w_H}}{{w_L}} = a + b\,t {K['coef']:+.3f}\,\ln\frac{{H}}{{L}}", font_size=28),
            label(rf"$\sigma$ = 1/{-K['coef']:.3f} = {K['sigma']:.2f}", font_size=21, color=WHITE),
            label(rf"the same regression, \ {ys[0]}--{ys[-1]}:", font_size=21, color=LOSS),
            label(rf"time and supply correlate {N['corr_trend_supply']:.3f}; \\ the slope is {N['slope']:+.2f}, \ "
                  rf"so $\sigma$ = {N['sigma']:.1f}: \\ impossible, \ and meaningless", font_size=18, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.4 + DOWN * 0.2)
        tag = published_tag(tables.KM_1992.tag + r"; \ refit on BLS data via FRED", corner=DR, font_size=11)
        with self.voiceover(
            "To measure sigma, Lawrence Katz and Kevin Murphy in 1992 regressed the premium on a time trend, standing "
            "for steady growth in demand, and on relative supply. <bookmark mark='a'/> Over 1963 to 1987 the "
            f"coefficient on supply was about {say_num(K['coef'], 2)}, an elasticity of substitution of "
            f"{K['sigma']:.2f}. <bookmark mark='b'/> Try the same regression on the years since 1992. "
            "<bookmark mark='c'/> Relative supply has grown almost exactly in a straight line, so it is nearly "
            f"identical to the time trend: their correlation is {N['corr_trend_supply']:.3f}. "
            "<bookmark mark='d'/> The regression cannot tell them apart, and returns a negative elasticity, which "
            "makes no sense. Katz and Murphy had an advantage: supply growth slowed sharply in the 1980s, breaking "
            "the link with the trend. A model is identified only by the variation the data happen to contain."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(km[0]), FadeIn(km[1]), FadeIn(keys[0]), Create(lt))
            vo.wait_until("a")
            self.play(FadeIn(km[2]))
            vo.wait_until("b")
            self.play(FadeIn(km[3]), FadeIn(keys[1]))
            vo.wait_until("c")
            self.play(Create(ls), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(km[4]))
        self.clear_scene()

    def demand(self):
        R = load("race")
        S = R["sigmas"]
        r1, r2 = R["d141_rates"], R["d25_rates"]
        periods = list(r1)
        bars = VGroup()
        top = 3.0
        for k, per in enumerate(periods):
            x = -4.6 + 2.6 * k
            for j, (v, col) in enumerate(((r1[per], DEMAND), (r2[per], "#F7A4A3"))):
                h = v * 100 / top * 3.4
                b = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                    np.array([x + 0.9 * j, -2.2 + h / 2, 0]))
                bars.add(VGroup(b, label(f"{100 * v:.1f}", font_size=17, color=WHITE).next_to(b, UP, buff=0.08)))
        names = VGroup(*[label(p.replace("-", "--"), font_size=18, color=GREY_A).move_to(
            np.array([-4.15 + 2.6 * k, -2.55, 0])) for k, p in enumerate(periods)])
        pull = R["supply_rate"] / R["km"]["sigma"]
        sup_h = pull * 100 / top * 3.4
        sline = DashedLine(np.array([-5.2, -2.2 + sup_h, 0]), np.array([2.4, -2.2 + sup_h, 0]), color=SUPPLY,
                           stroke_width=3)
        slab = label(rf"dashed: \ supply's pull on \\ the premium at $\sigma$ = 1.41: \\ {100 * pull:.1f}\% a year",
                     font_size=16, color=SUPPLY)
        head = label(r"how fast relative demand for college workers grew, \ \% a year", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.35)
        deq = MathTex(r"D_t = \ln\frac{w_H}{w_L} + \frac{1}{\sigma}\ln\frac{H}{L}", font_size=32).next_to(head, DOWN,
                                                                                                    buff=0.3)
        keys = VGroup(label(r"dark: \ $\sigma$ = 1.41", font_size=17, color=DEMAND),
                      label(r"light: \ $\sigma$ = 2.5", font_size=17, color="#F7A4A3")).arrange(DOWN, aligned_edge=LEFT,
                                                                                                 buff=0.2)
        side = VGroup(
            keys, slab,
            label(rf"other estimates: \\ Ciccone and Peri, \ states: \ {S['cp']:.1f}; \\ Card and Lemieux, \ "
                  rf"cohorts: \ {S['cl']:.1f}", font_size=16, color=GREY_A),
            label(rf"education explains {S['agk_8000']}\% of the rise \\ in inequality, \ 1980--2000; \\ "
                  rf"{S['agk_0017']}\% in 2000--17", font_size=16, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        tag = published_tag(r"BLS via FRED; \ " + tables.SIGMA_SKILL.tag, corner=DR, font_size=11)
        with self.voiceover(
            "So fix sigma from earlier work and ask the model a different question: how fast must demand have grown "
            "to produce the premium we see, given the supply we see? <bookmark mark='a'/> With sigma at 1.41, "
            f"relative demand for college workers grew {100 * r1[periods[0]]:.1f} percent a year in the 1990s, "
            f"{100 * r1[periods[1]]:.1f} in the 2000s, and {100 * r1[periods[2]]:.1f} since 2010. "
            "<bookmark mark='b'/> With the larger elasticities that other designs find, between one and a half and "
            "two and a half, the numbers are smaller but the shape is the same. <bookmark mark='c'/> Meanwhile supply "
            f"grew {100 * R['supply_rate']:.1f} percent a year, which at sigma 1.41 pulls the premium down by "
            f"{100 * pull:.1f} percent a year. Demand outran it in the 1990s; since 2010 it has fallen just behind, "
            "and the premium has edged down. Claudia Goldin and Lawrence Katz call this the race between education "
            "and technology: in the 1980s technology ran far ahead and the premium soared; lately education has kept "
            "pace. <bookmark mark='d'/> Autor, Goldin and Katz find that "
            "rising returns to education explain three-quarters of the rise in wage inequality from 1980 to 2000 "
            "but well under half since: something else is now at work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names), FadeIn(tag), Write(deq), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(bars[2 * k], shift=UP * 0.2) for k in range(3)], lag_ratio=0.3),
                      FadeIn(keys[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(bars[2 * k + 1], shift=UP * 0.2) for k in range(3)], lag_ratio=0.3),
                      FadeIn(keys[1]), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(sline), FadeIn(slab))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
