from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


class Lifetimes(VoiceoverScene):
    def construct(self):
        self.card()
        self.definitions()
        self.hazard_meaning()
        self.graunt()
        self.gompertz()
        self.sixty()
        self.shapes()

    def card(self):
        card = chapter_card(1, r"Lifetimes", r"Survival, \ hazard, \ and the link between them", lit=(1662, 1693, 1825), part=PART)
        with self.voiceover("Chapter one. Lifetimes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definitions(self):
        rows = [
            cmath(r"S(t)", r"=", r"P(T > t)", font_size=34),
            cmath(r"h(t)", r"=", r"\lim_{\delta \to 0} P(t \le T < t + \delta \mid T \ge t)/\delta = f(t)/S(t)", font_size=30),
            cmath(r"H(t)", r"=", r"\textstyle\int_0^t h(u)\, du = -\log S(t)", font_size=32),
            cmath(r"S(t)", r"=", r"e^{-H(t)}", font_size=34),
        ]
        rows[3][-1].set_color(HAZC)
        whys = [why(r"the survival function"), why(r"the hazard: \ the risk now, \ given alive"),
                why(r"the cumulative hazard"), why(r"one function, \ three faces")]
        with self.voiceover(
            "<bookmark mark='a'/> A lifetime T is a positive random variable, and its survival function S of t is the "
            "chance it exceeds t. <bookmark mark='b'/> The hazard is the instantaneous rate of the event at time t among "
            "those who have survived to t: the density divided by the survival. <bookmark mark='c'/> Its integral is the "
            "cumulative hazard, which is minus the log of the survival function, <bookmark mark='d'/> so survival is e to "
            "the minus cumulative hazard. Any one of the three determines the other two."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hazard_meaning(self):
        rows = fit_rows(VGroup(
            label(r"the hazard is a rate, \ per unit time, \ among the living", font_size=26, color=HAZC),
            label(r"a hazard of 0.01 a year: \ about 1 in 100 of those alive die over the next year", font_size=26),
            label(r"it can rise \ (ageing), \ fall \ (infant mortality, \ after surgery), \ or be constant", font_size=26, color=TAUC),
            label(r"constant hazard $\lambda$: \ the exponential, \ no memory, \ $S = e^{-\lambda t}$ \ (Part 3)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The hazard is the natural language for lifetimes because it describes risk among those "
            "still at risk. <bookmark mark='b'/> A hazard of point zero one a year means that, of those alive now, about "
            "one in a hundred will die over the coming year. <bookmark mark='c'/> It can rise with age, fall after a "
            "dangerous operation, or stay constant, <bookmark mark='d'/> which gives the exponential distribution of Part "
            "three, the only lifetime without memory."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def graunt(self):
        d = load("life")
        A = axes([0, 90], [0, 100], x_length=7.4, y_length=4.2, xlabel=r"age", ylabel=r"alive, \ of 100 conceived",
                 xticks=[0, 20, 40, 60, 80], yticks=[0, 25, 50, 75, 100], center=[-2.5, 0.2, 0])
        ax = A.ax
        a, n = d["graunt_ages"], d["graunt_alive"]
        c = polyline(ax, a, n, SURVC, 3)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.07, color=SURVC) for x, y in zip(a, n)])
        side = fit_rows(VGroup(
            label(r"John Graunt (1662): \ London's Bills of Mortality", font_size=22),
            label(r"of 100 conceived, \ 64 alive at 6, \ 25 at 26, \ 6 at 56", font_size=22, color=SURVC),
            label(r"a survival function, \ partly guessed", font_size=22, color=GREY_A),
            label(r"Halley (1693): \ Breslau's records, \ and annuity prices", font_size=22, color=TAUC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The oldest survival curve is John Graunt's of 1662, from London's weekly bills of "
            "mortality, which we met at the very start of this course. <bookmark mark='b'/> Of a hundred conceived, he reckoned, sixty-four were "
            "alive at six, twenty-five at twenty-six, and six at fifty-six. <bookmark mark='c'/> It was a survival function, "
            "partly guessed. <bookmark mark='d'/> Edmond Halley built a better one in 1693 from the records of Breslau, and "
            "used it to price annuities: the beginning of actuarial science."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(dots), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def gompertz(self):
        d = load("life")
        ages = np.asarray(d["ages"], float)
        hm, hw = np.log10(np.asarray(d["haz"]["men"])), np.log10(np.asarray(d["haz"]["women"]))
        A = axes([40, 95], [-3, 0], x_length=7.4, y_length=4.2, xlabel=r"age", ylabel=r"hazard of death per year \ (log scale)",
                 xticks=[40, 50, 60, 70, 80, 90], yticks=[-3, -2, -1, 0], yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.5, 0.2, 0])
        ax = A.ax
        c1 = polyline(ax, ages, np.clip(hm, -3, 0), Y1C, 3)
        c2 = polyline(ax, ages, np.clip(hw, -3, 0), Y0C, 3)
        side = fit_rows(VGroup(
            label(r"Benjamin Gompertz (1825): \ $h(a) = \alpha e^{\beta a}$", font_size=22, color=HAZC),
            label(r"a straight line on a log scale", font_size=22, color=GREY_A),
            label(r"the World: \ men \ (red), \ women \ (blue)", font_size=22),
            label(r"doubling about every 8 years", font_size=22, color=TAUC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1825 the actuary Benjamin Gompertz noticed that adult death rates grow "
            "exponentially with age. <bookmark mark='b'/> On a log scale, the hazard is a straight line. <bookmark "
            "mark='c'/> Here are the World's hazards for a man and a woman with average blood pressure: men's higher at "
            "every age, <bookmark mark='d'/> and both doubling roughly every eight years. Gompertz's law still describes "
            "human mortality between about thirty and ninety remarkably well."
        ) as vo:
            self.add(cohort_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c1), Create(c2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def sixty(self):
        d = load("life")
        t, s = np.asarray(d["t60"], float), np.asarray(d["S60"], float)
        A = axes([0, 40], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"years from age 60", ylabel=r"$S(t)$",
                 xticks=[0, 10, 20, 30, 40], yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        c = polyline(ax, t, s, SURVC, 3)
        m = d["median60"]
        guide = VGroup(DashedLine(ax.c2p(0, 0.5), ax.c2p(m, 0.5), color=TAUC, stroke_width=2),
                       DashedLine(ax.c2p(m, 0.5), ax.c2p(m, 0), color=TAUC, stroke_width=2))
        side = fit_rows(VGroup(
            label(r"a 60-year-old man in the World", font_size=22),
            label(r"$S(t) = e^{-H(t)}$, \ $H$ from both causes", font_size=22, color=SURVC),
            label(rf"median remaining life: \ {m:.1f} years", font_size=22, color=TAUC),
            label(r"the mean needs the whole tail, \ the median does not", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Integrating the hazard gives the survival curve. For a sixty-year-old man in the "
            "World, <bookmark mark='b'/> survival from sixty falls slowly at first, then faster, as the hazard climbs. "
            "<bookmark mark='c'/> Half such men live another " + say(m, 1) + " years. <bookmark mark='d'/> The median is "
            "the natural summary for lifetimes, because it needs only the first half of the curve; the mean needs the "
            "whole tail, and the tail is exactly what censoring hides."
        ) as vo:
            self.add(cohort_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(guide), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def shapes(self):
        A = axes([0, 3], [0, 3], x_length=7.4, y_length=4.2, xlabel=r"time", ylabel=r"hazard $h(t)$",
                 xticks=[0, 1, 2, 3], yticks=[0, 1, 2, 3], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        ts = np.linspace(0.02, 3, 150)
        cs = [polyline(ax, ts, np.clip(k * ts ** (k - 1), 0, 3), c, 3) for k, c in ((0.5, Y0C), (1.0, GREY_B), (2.0, HAZC))]
        bath = np.clip(0.4 / np.sqrt(ts) + 0.15 * ts ** 2 + 0.2, 0, 3)
        cb = polyline(ax, ts, bath, AREAC, 3)
        side = fit_rows(VGroup(
            label(r"Weibull, \ shape $k = 1/2$: \ falling", font_size=22, color=Y0C),
            label(r"$k = 1$: \ constant \ (exponential)", font_size=22, color=GREY_B),
            label(r"$k = 2$: \ rising \ (wear-out)", font_size=22, color=HAZC),
            label(r"the bathtub: \ infant deaths, \ then ageing", font_size=22, color=AREAC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Hazards come in shapes. The Weibull family, h of t equals k t to the k minus one, falls "
            "when its shape k is below one, <bookmark mark='b'/> is constant at one, <bookmark mark='c'/> and rises above "
            "one, like machines that wear out. <bookmark mark='d'/> Human mortality over a whole life is a bathtub: high "
            "in infancy, low through youth, then rising by Gompertz's law. Looking at the hazard, not the density, is what "
            "makes these shapes visible."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(Create(cs[k]), FadeIn(side[k]))
            vo.wait_until("d")
            self.play(Create(cb), FadeIn(side[3]))
        self.clear_scene()
