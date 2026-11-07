from __future__ import annotations

import numpy as np

from videos.stats.stats30.common import *  # noqa: F403


class HodgesLehmann(VoiceoverScene):
    def construct(self):
        self.card()
        self.walsh()
        self.picture()
        self.interval()
        self.newcomb()
        self.darwin()
        self.properties()

    def card(self):
        card = chapter_card(2, r"Hodges--Lehmann", r"An estimate from a test", lit=(1963,), part=PART)
        with self.voiceover("Chapter two. The Hodges–Lehmann estimator."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def walsh(self):
        rows = [
            cmath(r"W^+(\theta)", r"=", r"\#\{i \le j : (x_i + x_j)/2 > \theta\}", font_size=30),
            cmath(r"E_\theta W^+", r"=", r"\tfrac12 \cdot \tfrac{n(n+1)}{2}", font_size=32),
            cmath(r"\hat\theta_{\mathrm{HL}}", r"=", r"\mathrm{median}_{i \le j} \tfrac{x_i + x_j}{2}", font_size=32),
            cmath(r"\text{efficiency}", r"=", r"\text{the Wilcoxon test's: \ } 0.955 \text{ at the normal}, \ \ge 0.864", font_size=28),
        ]
        rows[2][2].set_color(HLC)
        whys = [why(r"the signed-rank statistic, \ as a count"), why(r"at the true centre: \ half of them"),
                why(r"solve $W^+ = $ its expectation"), why(r"Hodges \& Lehmann (1963)")]
        with self.voiceover(
            "<bookmark mark='a'/> Hodges and Lehmann turned the test into an estimate. The signed-rank statistic, "
            "testing centre theta, counts the Walsh averages, the averages of all pairs of observations including "
            "each with itself, that exceed theta. <bookmark mark='b'/> At the true centre of a symmetric "
            "distribution, half of them should. <bookmark mark='c'/> So estimate the centre by the value that splits "
            "them in half: the median of the Walsh averages. <bookmark mark='d'/> It inherits the test's efficiency: "
            "ninety-five and a half percent at the normal, under the regular continuous symmetric finite-variance "
            "location assumptions, never below eighty-six point four, and sometimes far above one."
        ) as vo:
            intro=label('The median of pairwise averages estimates a symmetry center',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        x = np.array([2.1, 3.4, 3.9, 4.4, 5.2, 5.6, 6.3, 14.0])
        i, j = np.triu_indices(len(x))
        w = (x[i] + x[j]) / 2
        A = axes([1, 15], [-0.5, 1.5], x_length=10.0, y_length=3.4, xlabel=r"value", ylabel=r"", xticks=[2, 4, 6, 8, 10, 12, 14],
                 yticks=[], center=[0, 0.8, 0])
        ax = A.ax
        data = VGroup(*[Dot(ax.c2p(v, 1.1), radius=0.09, color=WHITE) for v in x])
        rng = np.random.default_rng(4)
        wd = VGroup(*[Dot(ax.c2p(v, rng.uniform(-0.2, 0.5)), radius=0.05, color=HLC, fill_opacity=0.8) for v in w])
        mline = DashedLine(ax.c2p(np.mean(x), -0.4), ax.c2p(np.mean(x), 1.4), color=MEANC, stroke_width=2.5)
        hline = DashedLine(ax.c2p(np.median(w), -0.4), ax.c2p(np.median(w), 1.4), color=HLC, stroke_width=2.5)
        dline = DashedLine(ax.c2p(np.median(x), -0.4), ax.c2p(np.median(x), 1.4), color=MEDC, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(r"8 observations, \ one far out at 14", font_size=22),
            label(rf"blue: \ the {len(w)} Walsh averages", font_size=22, color=HLC),
            label(rf"their median: \ {np.median(w):.2f}", font_size=22, color=HLC),
            label(rf"red: \ the mean, \ {np.mean(x):.2f}; \ green: \ the median, \ {np.median(x):.2f}", font_size=22, color=GREY_A),
        ), 12.0, 0.22, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Eight observations, one far out at fourteen. <bookmark mark='b'/> Their thirty-six Walsh "
            "averages: each pair's midpoint. The far point creates eight averages of its own, spread towards the right, but "
            "the other twenty-eight crowd the middle. <bookmark mark='c'/> Their median is four point eight three. "
            "<bookmark mark='d'/> The mean, five point six, is dragged right; the median, four point eight, is not. "
            "Hodges–Lehmann sits with the median here, while using the data far more efficiently."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in data], lag_ratio=0.1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in wd], lag_ratio=0.03), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(hline), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(mline), Create(dline), FadeIn(rows[3]))
        self.clear_scene()

    def interval(self):
        rows = [
            cmath(r"\{\theta : \text{signed-rank test accepts}\}", r"=", r"[w_{(k)}, w_{(N - k + 1)}]", font_size=28),
            cmath(r"k", r":", r"P(W^+ \le k - 1) \le \alpha/2 \ \text{ under } H_0", font_size=30),
            cmath(r"\text{exact}", r":", r"\text{for any continuous symmetric distribution}", font_size=30),
            cmath(r"n = 8", r":", r"k = 4: \ \ [w_{(4)}, w_{(33)}], \ \ 96.1\%", font_size=30),
        ]
        rows[0][2].set_color(HLC)
        whys = [why(r"invert the test, \ Part 11's duality"), why(r"from the exact null, \ $2^n$ sign patterns"),
                why(r"distribution-free"), why(r"the ordered Walsh averages")]
        with self.voiceover(
            "<bookmark mark='a'/> An interval comes the same way, by inverting the test, Part 11's duality: the centres the "
            "signed-rank test would accept form an interval between two ordered Walsh averages. <bookmark mark='b'/> Which "
            "two is read from the exact null distribution of the statistic, two to the n equally likely sign patterns. "
            "<bookmark mark='c'/> The coverage is exact for any continuous symmetric distribution. <bookmark mark='d'/> With "
            "eight observations it runs from the fourth smallest Walsh average to the thirty-third, with coverage ninety-six "
            "point one percent: the discreteness of the null means exact levels jump."
        ) as vo:
            intro=label('Inverting a continuous signed-rank reference gives ordered-pair bounds',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def newcomb(self):
        d = load("newcomb")
        a, c = d["all"], d["clean"]
        A = axes([22, 30], [-0.5, 5.5], x_length=6.4, y_length=4.2, xlabel=r"passage time $-$ 24,800 ns", ylabel=r"",
                 xticks=[22, 24, 26, 28, 30], yticks=[], center=[-3.0, 0.3, 0])
        ax = A.ax
        spec = (("mean", r"mean, \ all 66", a, MEANC), ("mean", r"mean, \ strays removed", c, MEANC), ("median", r"median, \ all 66", a, MEDC),
                ("hl", r"Hodges--Lehmann, \ all 66", a, HLC), ("hl", r"Hodges--Lehmann, \ removed", c, HLC))
        bars, labs = VGroup(), VGroup()
        for k, (key, t, src, col) in enumerate(spec):
            y = 4.6 - k
            v = src[key]
            bars.add(VGroup(Line(ax.c2p(v["lo"], y), ax.c2p(v["hi"], y), color=col, stroke_width=5),
                            Dot(ax.c2p(v["est"], y), radius=0.08, color=WHITE)))
            labs.add(label(rf"{t}: \ {v['est']:.2f} \ [{v['lo']:.2f}, {v['hi']:.2f}]", font_size=19, color=col).next_to(ax.c2p(30, y), RIGHT, buff=0.25))
        with self.voiceover(
            "<bookmark mark='a'/> On Newcomb's data. The t interval for the mean of all sixty-six runs from "
            "twenty-three point six to twenty-eight point nine, widened by the two strays. <bookmark mark='b'/> "
            "Remove them by hand and it jumps and shrinks. <bookmark mark='c'/> The median's distribution-free "
            "interval: twenty-six to twenty-nine. <bookmark mark='d'/> Hodges–Lehmann's: twenty-six to twenty-eight "
            "and a half, almost the same whether the strays are in or out. The robust and hand-trimmed intervals are "
            "close in this example. The rounded historical data have ties, so the continuous signed-rank reference is"
            " not an exact tie-adjusted guarantee."
        ) as vo:
            self.add(newcomb_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[2]), FadeIn(labs[2]))
            vo.wait_until("d")
            self.play(FadeIn(bars[3:]), FadeIn(labs[3:]))
        self.clear_scene()

    def properties(self):
        rows = fit_rows(VGroup(
            label(r"breakdown $1 - 1/\sqrt2 \approx 29\%$: \ chapter four", font_size=24, color=HLC),
            label(r"targets the centre of symmetry; \ for skewed data, \ the pseudo-median", font_size=24, color=RES),
            label(r"two samples: \ the median of all $x_i - y_j$; \ the Mann--Whitney interval", font_size=24),
            label(r"regression: \ rank-based slopes \ (Theil 1950; \ Sen 1968)", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Its breakdown point, chapter four's measure, is one minus one over root two, about "
            "twenty-nine percent. <bookmark mark='b'/> It estimates the centre of symmetry; for skewed data it estimates "
            "something called the pseudo-median, neither mean nor median. <bookmark mark='c'/> For two samples, the same "
            "idea gives the median of all pairwise differences and an interval inverting the Mann–Whitney test. "
            "<bookmark mark='d'/> And for a regression slope, the median of pairwise slopes, Henri Theil's and Pranab Kumar "
            "Sen's estimator."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def darwin(self):
        from explainer.stats.kit import robust as RR
        from scipy import stats as st
        x = np.asarray(museum.DARWIN_ZEA, float)
        n = len(x)
        t = st.t.ppf(0.975, n - 1)
        m, s = x.mean(), x.std(ddof=1) / np.sqrt(n)
        hl = RR.hodges_lehmann(x)
        lo, hi = RR.hodges_lehmann_ci(x)
        A = axes([-80, 80], [-0.5, 1.5], x_length=10.0, y_length=2.6, xlabel=r"cross- minus self-fertilized height (eighths of an inch)",
                 ylabel=r"", xticks=[-60, -30, 0, 30, 60], yticks=[], center=[0, 1.1, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(v, 0.9), radius=0.08, color=WHITE) for v in x])
        tb = VGroup(Line(ax.c2p(m - t * s, 0.35), ax.c2p(m + t * s, 0.35), color=MEANC, stroke_width=5), Dot(ax.c2p(m, 0.35), radius=0.08))
        hb = VGroup(Line(ax.c2p(lo, 0.0), ax.c2p(hi, 0.0), color=HLC, stroke_width=5), Dot(ax.c2p(hl, 0.0), radius=0.08))
        rows = fit_rows(VGroup(
            label(r"Darwin's 15 pairs of maize plants \ (Part 16)", font_size=22),
            label(rf"mean {m:.1f}, \ $t$ interval [{m - t * s:.1f}, {m + t * s:.1f}]", font_size=22, color=MEANC),
            label(rf"Hodges--Lehmann {hl:.1f}, \ signed-rank reference [{lo:.1f}, {hi:.1f}]", font_size=22, color=HLC),
            label(r"two negative pairs pull the mean down; \ HL is higher and its interval tighter", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Darwin's maize, from Part 16: fifteen pairs, cross-fertilized minus self-fertilized"
            " height. <bookmark mark='b'/> The mean difference is twenty-one, with a t interval from just above zero "
            "to forty-two. <bookmark mark='c'/> Hodges–Lehmann's estimate is twenty-five, with a continuous "
            "signed-rank reference interval from four to forty-one and a half; the rounded differences contain ties. "
            "<bookmark mark='d'/> Two negative pairs pull the mean down and widen its interval; the robust estimate "
            "sits with the bulk of the pairs, and its interval excludes zero by a wider margin."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(hb), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
