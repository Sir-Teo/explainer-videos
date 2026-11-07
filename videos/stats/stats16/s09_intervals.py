from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.stats.board import coverage_board, load_all
from explainer.stats.kit import bootstrap as Bt
from explainer.stats.world import World
from videos.stats.stats16.common import *  # noqa: F403


def law_hist(d, center=(-1.6, 0.6, 0), x_length=8.0, y_length=3.6):
    reps = np.asarray(d["reps"])
    e = np.linspace(0, 1.2, 49)
    A = axes([0, 1.2], [0, 180], x_length=x_length, y_length=y_length, xlabel=r"$r^*$", ylabel=r"resamples",
             xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 80, 160], center=list(center), font_size=18)
    ax = A.ax
    bars = hist_bars(ax, e, np.histogram(reps, e)[0], color=BOOT, opacity=0.75)
    one = DashedLine(ax.c2p(1, 0), ax.c2p(1, 170), color=GREY_C, stroke_width=2)
    obs = DashedLine(ax.c2p(d["r"], 0), ax.c2p(d["r"], 170), color=OBS, stroke_width=3)
    return A, ax, bars, one, obs


class BootIntervals(VoiceoverScene):
    def construct(self):
        self.card()
        self.percentile()
        self.basic()
        self.boot_t()
        self.bca()
        self.compare()
        self.board()
        self.lessons()

    def card(self):
        card = chapter_card(8, r"Bootstrap intervals", r"From a histogram of replicates to a 95\% interval", part=PART)
        with self.voiceover("Chapter eight. Bootstrap intervals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def percentile(self):
        d = load("law")
        A, ax, bars, one, obs = law_hist(d)
        lo, hi = d["percentile"]
        br = Line(ax.c2p(lo, -12), ax.c2p(hi, -12), color=BOOT, stroke_width=8)
        q1 = DashedLine(ax.c2p(lo, 0), ax.c2p(lo, 150), color=BOOT, stroke_width=2)
        q2 = DashedLine(ax.c2p(hi, 0), ax.c2p(hi, 150), color=BOOT, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"the percentile interval", font_size=26, color=BOOT),
            label(r"the 2.5th and 97.5th percentiles of $r^*$", font_size=22),
            MathTex(rf"[{lo:.3f},\ {hi:.3f}]", font_size=32, color=BOOT),
            label(r"respects $r \le 1$; \ transformation-invariant", font_size=22, color=HIT),
            label(r"regularity is needed; \ finite-sample coverage can be poor", font_size=22, color=RES),
        ), 4.6, 0.36, [4.6, 0.5, 0])
        with self.voiceover(
            "We have two thousand bootstrap correlations. How do we make an interval? <bookmark mark='a'/> The simplest answer, "
            "Efron's first: <bookmark mark='b'/> take the middle ninety-five percent of the replicates, from the two and a "
            "half to the ninety-seven and a half percentile. <bookmark mark='c'/> Point four four seven to point nine six two. "
            "<bookmark mark='d'/> It has nice properties. It can't leave the range of possible values, and if you transform "
            "the statistic, say by Fisher's z, ideal percentile endpoints transform with it. Finite Monte Carlo interpolation introduces small discrepancies. <bookmark mark='e'/> One useful sufficient motivation is that "
            "a transformation makes the estimate approximately unbiased and normal with constant variance. This is not a necessary condition. When the "
            "estimate is biased or its spread changes with the parameter, the percentile interval is off."
        ) as vo:
            self.play(FadeIn(A), FadeIn(bars), Create(one), Create(obs))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(q1), Create(q2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(br), FadeIn(rows[2]))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def basic(self):
        d = load("law")
        lo, hi = d["percentile"]
        rows = [
            cmath(r"\hat\theta^* - \hat\theta", r"\ \approx\ ", r"\hat\theta - \theta\ \ \text{in law}", font_size=32),
            cmath(r"q^*_{.025} - \hat\theta \le \hat\theta - \theta", r"\le", r"q^*_{.975} - \hat\theta\ \ \text{w.p. } 0.95", font_size=30),
            cmath(r"\theta", r"\in", r"[\,2\hat\theta - q^*_{.975},\ \ 2\hat\theta - q^*_{.025}\,]", font_size=32),
            cmath(r"\text{law schools}", r":", rf"[{d['basic'][0]:.3f},\ {d['basic'][1]:.3f}]", font_size=32),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"the bootstrap principle, \ for the error"), why(r"read the error's quantiles off the replicates"),
                why(r"the ``basic'' interval: \ the percentiles reflected"), why(r"its upper end is above 1: \ impossible")]
        with self.voiceover(
            "The bootstrap principle suggests something different. <bookmark mark='a'/> It says the error of a replicate about "
            "the estimate mimics the error of the estimate about the truth. <bookmark mark='b'/> So the error lies between the "
            "replicates' quantiles minus the estimate, with probability ninety-five percent. <bookmark mark='c'/> Solve for theta: "
            "the interval is twice the estimate minus the upper quantile, to twice the estimate minus the lower one. It's the "
            "percentile interval reflected about the estimate: where the replicates have a long left tail, this interval has "
            "a long right one. <bookmark mark='d'/> For the law schools: point five nine one to one point one oh six. Its upper "
            "end is a correlation above one, which is impossible. The basic interval is right in logic, and here the "
            "reflection takes it out of bounds: it's only as good as the approximation that the error's distribution doesn't "
            "depend on theta."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def boot_t(self):
        W = World()
        x = W.income[W.sample(15, among=W.adult, seed=166)] / 1000
        mu = float((W.income[W.adult] / 1000).mean())
        g = np.random.Generator(np.random.PCG64(9))
        reps = Bt.bootstrap(x, np.mean, 4000, g)
        pl, ph = np.quantile(reps, [0.025, 0.975])
        bl, bh = Bt.bootstrap_t_ci(x, 4000, g)
        tl, th = stats.t.interval(0.95, 14, loc=x.mean(), scale=x.std(ddof=1) / np.sqrt(15))
        rows = [
            cmath(r"t^*", r"=", r"\frac{\bar x^* - \bar x}{s^*/\sqrt n}", font_size=32),
            cmath(r"\text{CI}", r"=", r"[\,\bar x - t^*_{.975}\, s/\sqrt n,\ \ \bar x - t^*_{.025}\, s/\sqrt n\,]", font_size=30),
        ]
        g2 = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.0, 2.0, 0])
        for r_ in g2:
            if r_.width > 6.0:
                r_.width = 6.0
        note_ = label(r"each resample studentized by its own $s^*$: \ Part 8's pivot, \ its table from the data", font_size=22,
                      color=GREY_A).move_to([3.4, 2.0, 0])
        if note_.width > 6.0:
            note_.width = 6.0
        A = axes([20, 70], [0, 4], x_length=9.0, y_length=2.4, xlabel=r"mean income, \ thousands", xticks=[20, 30, 40, 50, 60, 70],
                 center=[-0.4, -1.1, 0])
        ax = A.ax
        tr = DashedLine(ax.c2p(mu, 0), ax.c2p(mu, 3.9), color=S.TRUTH, stroke_width=3)
        trl = label(r"truth", font_size=20, color=S.TRUTH).next_to(ax.c2p(mu, 3.9), UP, buff=0.05)

        def seg(a, b, y, col, name):
            ln = Line(ax.c2p(a, y), ax.c2p(b, y), color=col, stroke_width=7)
            nm = label(name, font_size=20, color=col).next_to(ax.c2p(20, y), LEFT, buff=0.2)
            return VGroup(ln, nm)

        s1 = seg(tl, th, 3.0, S.ALT, r"Student's $t$")
        s2 = seg(pl, ph, 2.0, BOOT, r"percentile")
        s3 = seg(bl, bh, 1.0, OBS, r"bootstrap-$t$")
        cap = fit_rows(VGroup(
            label(rf"one sample of 15 incomes from the World: \ mean {x.mean():.1f}; \ the World's mean {mu:.1f}", font_size=20),
        ), 12.0, 0.2, [0, -3.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A third idea goes back to Part 8's pivot. Studentize each replicate: subtract the sample mean "
            "and divide by the replicate's own standard error. <bookmark mark='b'/> The quantiles of these t-star values replace "
            "Student's table. Gosset's table assumed normal data; this one is built from the data themselves, and so it can be "
            "asymmetric. <bookmark mark='c'/> Try it on fifteen incomes from the World, which are very skewed. The mean is "
            "forty-two point four; the World's true mean is forty-nine point five. <bookmark mark='d'/> Student's t-interval "
            "is symmetric: twenty-eight to fifty-seven. <bookmark mark='e'/> The percentile interval is narrower: "
            "thirty-one to fifty-five. Both catch the truth this time, but both sit nearly symmetrically around a mean that's too low. <bookmark mark='f'/> The bootstrap-t interval "
            "stretches to the right, thirty to sixty-two, because with a right-skewed population a low sample mean usually "
            "comes with a low standard deviation too. Peter Hall showed in 1988 that this interval is accurate to second order under suitable smoothness and moment conditions: "
            "its coverage error shrinks like one over n rather than one over root n."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(g2[0]), FadeIn(note_))
            vo.wait_until("b")
            self.play(FadeIn(g2[1]))
            vo.wait_until("c")
            self.play(FadeIn(A), Create(tr), FadeIn(trl), FadeIn(cap))
            for m_, s_ in zip("def", [s1, s2, s3]):
                vo.wait_until(m_)
                self.play(Create(s_[0]), FadeIn(s_[1]))
        self.clear_scene()

    def bca(self):
        d = load("law")
        low, high = d["bca_levels"]
        rows = [
            cmath(r"z_0", r"=", rf"\Phi^{{-1}}\big((\#\{{r^* < r\}}+\tfrac12\#\{{r^*=r\}})/B\big) = {d['z0']:.3f}", font_size=30),
            cmath(r"a", r"=", rf"\frac{{\sum (\bar r_{{(\cdot)}} - r_{{(i)}})^3}}{{6 \big[\sum (\bar r_{{(\cdot)}} - r_{{(i)}})^2\big]^{{3/2}}}} = {d['a']:.3f}", font_size=28),
            cmath(r"\alpha_{1,2}", r"=", rf"\Phi\Big(z_0 + \frac{{z_0 + z_\alpha}}{{1 - a(z_0 + z_\alpha)}}\Big) = {low:.3f},\ {high:.3f}", font_size=28),
            cmath(r"\text{BCa}", r"=", rf"[q^*_{{{low:.3f}}},\ q^*_{{{high:.3f}}}] = [{d['bca'][0]:.3f},\ {d['bca'][1]:.3f}]", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"bias: \ only 45\% of replicates fall below $r$"), why(r"acceleration: \ the jackknife's skewness"),
                why(r"shifted percentile levels"), why(r"Efron (1987): \ stated here, \ proved in Part 30")]
        with self.voiceover(
            "Efron's answer to the percentile interval's flaws, in 1987, was BCa: bias-corrected and accelerated. It's "
            "stated here, not derived. <bookmark mark='a'/> The bias correction z-nought measures how far the replicates are "
            "off-centre: only forty-four and a half percent fall below the observed correlation, so z-nought is minus point "
            "one three seven. <bookmark mark='b'/> The acceleration a measures how fast the standard error changes with the "
            "parameter, estimated from the skewness of the jackknife values of chapter six: minus point oh seven six. "
            "<bookmark mark='c'/> Together they move the percentile levels: instead of two and a half and ninety-seven and a "
            "half, BCa uses the point four and the ninety-two point nine percentiles. <bookmark mark='d'/> For the law schools, "
            "point two eight seven to point nine four three: shifted down, and much longer on the left. BCa keeps the percentile "
            "interval's good properties, staying in range and transforming correctly, and it's second-order accurate like "
            "the bootstrap-t."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def compare(self):
        d = load("law")
        A = axes([0.2, 1.15], [0, 6], x_length=9.4, y_length=4.4, xlabel=r"the law-school correlation", xticks=[0.25, 0.5, 0.75, 1.0],
                 center=[0.8, 0.3, 0])
        ax = A.ax
        one = DashedLine(ax.c2p(1, 0), ax.c2p(1, 5.8), color=GREY_C, stroke_width=2)
        obs = DashedLine(ax.c2p(d["r"], 0), ax.c2p(d["r"], 5.8), color=OBS, stroke_width=2.5)
        items = [("normal-theory, \\ Fisher's $z$", d["fisher_z"], S.ALT), ("$r \\pm 1.96\\,\\widehat{\\mathrm{SE}}_{\\text{boot}}$", d["normal"], GREY_B),
                 ("percentile", d["percentile"], BOOT), ("basic", d["basic"], RES), ("BCa", d["bca"], OBS)]
        segs = VGroup()
        for k, (nm, (lo, hi), col) in enumerate(items):
            y = 5.0 - k
            ln = Line(ax.c2p(lo, y), ax.c2p(hi, y), color=col, stroke_width=7)
            t = label(nm, font_size=20, color=col).next_to(ax.c2p(0.2, y), LEFT, buff=0.2)
            v = MathTex(rf"[{lo:.2f}, {hi:.2f}]", font_size=20, color=col).next_to(ln, UP, buff=0.06)
            segs.add(VGroup(ln, t, v))
        with self.voiceover(
            "<bookmark mark='a'/> Side by side, for the fifteen law schools. The normal-theory interval, through Fisher's z: "
            "point four four to point nine two. <bookmark mark='b'/> The estimate plus or minus one point nine six bootstrap "
            "standard errors: it crosses one. <bookmark mark='c'/> The percentile interval. <bookmark mark='d'/> The basic "
            "interval, crossing one. <bookmark mark='e'/> And BCa, reaching down to point two nine. Five reasonable recipes, "
            "five different answers, from fifteen points. The disagreement is itself informative: with a sample this small and "
            "a bounded, skewed statistic, the data can't pin down the interval's shape. Which recipe can we trust? That's a "
            "question for the Board."
        ) as vo:
            self.play(FadeIn(A), Create(one), Create(obs))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(Create(segs[k][0]), FadeIn(segs[k][1]), FadeIn(segs[k][2]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=16) if r.part == 16 and r.setting.startswith("the World")]
        b = coverage_board(rows, lit_part=16, placeholders=0, font_size=20, row_h=0.6)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "The Board's test: the mean of fifteen incomes from the World, whose distribution is extremely skewed, ten thousand "
            "samples, nine hundred and ninety-nine resamples each. <bookmark mark='a'/> The percentile interval covers eighty-"
            "five and a half percent: broken. <bookmark mark='b'/> BCa, eighty-six point seven: broken too, barely better. "
            "<bookmark mark='c'/> The bootstrap-t, ninety-one point six: still broken, but the best by far. "
            "<bookmark mark='d'/> And Student's t, the method that assumes normality: eighty-eight point four. Between the "
            "percentile and the bootstrap-t. With fifteen observations from a population this skewed, none of these four recipes reaches "
            "ninety-five percent. The bootstrap is not magic: it can't conjure the incomes in the long right tail that the "
            "sample didn't happen to contain."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        self.wait(1.0)
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"percentile: \ in range; \ usually first-order under regularity", font_size=24, color=BOOT),
            label(r"basic: \ the right logic, \ but it can leave the parameter space", font_size=24, color=RES),
            label(r"bootstrap-$t$: \ second-order, \ needs a standard error for every resample", font_size=24, color=OBS),
            label(r"BCa: \ second-order under regularity; \ a common option", font_size=24, color=OBS),
            label(r"none can see the tail the sample missed", font_size=26, color=GREY_A),
        ), 12.4, 0.46, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The percentile interval is simple and stays in range, but its coverage error shrinks slowly "
            "and small-sample coverage can be poor in either direction. <bookmark mark='b'/> The basic interval has the right logic but can leave the "
            "parameter space. <bookmark mark='c'/> Under stronger smoothness and moment conditions, the bootstrap-t is second-order accurate but needs a standard error for every "
            "resample, which for complicated statistics means a bootstrap inside the bootstrap. <bookmark mark='d'/> BCa is "
            "second-order accurate under suitable regularity, stays in range, and is a common software option. Its finite-sample fitted acceleration need not transform exactly. <bookmark mark='e'/> And none of "
            "them can see what the sample didn't contain."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
