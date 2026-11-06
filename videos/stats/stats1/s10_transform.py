from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats1.common import *  # noqa: F403


def boxcox(y, lam):
    return np.log(y) if abs(lam) < 1e-9 else (y ** lam - 1) / lam


class Transform(VoiceoverScene):
    def construct(self):
        self.card()
        self.family()
        self.live()
        self.likelihood()
        self.stabilize()

    def card(self):
        card = chapter_card(9, r"Transformations", r"Change the ruler, and the shape changes with it", lit=(),
                            part=PART)
        with self.voiceover("Chapter nine. Transformations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def family(self):
        A = axes([0, 3], [-2.5, 3], x_length=6.0, y_length=4.8, xlabel=r"$y$", ylabel=r"$y^{(\lambda)}$",
                 xticks=[0, 1, 2, 3], yticks=[-2, 0, 2], center=[-3.4, -0.4, 0])
        ax = A.ax
        lam = ValueTracker(1.0)
        ys = np.linspace(0.08, 3, 200)

        def fam():
            v = boxcox(ys, lam.get_value())
            ok = (v > -2.5) & (v < 3)
            return curve(ax, ys[ok], v[ok], S.ACCENT, 4)

        cur = always_redraw(fam)
        ghosts = VGroup(*[curve(ax, ys[(boxcox(ys, l) > -2.5) & (boxcox(ys, l) < 3)],
                                boxcox(ys, l)[(boxcox(ys, l) > -2.5) & (boxcox(ys, l) < 3)], GREY_D, 2)
                          for l in (1.5, 1.0, 0.5, 0.0, -0.5, -1.0)])
        read = always_redraw(lambda: MathTex(rf"\lambda = {lam.get_value():.2f}", font_size=38, color=S.ACCENT)
                             .next_to(A, UP, buff=0.1))
        rows = [
            cmath(r"y^{(\lambda)}", r"=", r"\frac{y^\lambda - 1}{\lambda}", font_size=38),
            cmath(r"y^{(\lambda)}", r"=", r"\frac{e^{\lambda \log y} - 1}{\lambda}", font_size=38),
            cmath(r"y^{(\lambda)}", r"=", r"\log y + \tfrac{\lambda}{2}(\log y)^2 + \cdots", font_size=38),
            cmath(r"y^{(0)}", r"=", r"\log y", font_size=38),
        ]
        whys = [why(r"Box \& Cox (1964)"), why(r"$y^\lambda = e^{\lambda \log y}$"), why(r"Taylor in $\lambda$"),
                why(r"let $\lambda \to 0$")]
        with self.voiceover(
            "If a logarithm can turn a lopsided distribution into a symmetric one, what about other transformations? "
            "<bookmark mark='a'/> In 1964 George Box and David Cox proposed a family with one dial, lambda: y to the "
            "lambda, minus one, divided by lambda. <bookmark mark='b'/> At lambda equal to one it's just y minus one: "
            "nothing changes but the origin. At a half it's essentially a square root; at minus one, essentially "
            "one over y. <bookmark mark='c'/> The subtraction and division are there to make the family continuous. "
            "Write y to the lambda as e to the lambda log y, expand in lambda, and as lambda goes to zero the curve "
            "becomes the logarithm. So the log isn't a special case bolted on; it's the middle of the family. "
            "<bookmark mark='d'/> Turning the dial bends the ruler: lambdas below one compress large values and "
            "stretch small ones, pulling in a right tail."
        ) as vo:
            self.play(FadeIn(A), FadeIn(ghosts))
            self.add(cur, read)
            vo.wait_until("a")
            step = ladder(self, rows, whys, keep=4, top=2.6, x=2.7, buff=0.45)
            step(0)
            vo.wait_until("b")
            self.play(lam.animate.set_value(0.5), run_time=1.5)
            self.play(lam.animate.set_value(-1.0), run_time=1.5)
            vo.wait_until("c")
            step(1)
            step(2)
            self.play(lam.animate.set_value(0.0), run_time=1.5)
            step(3)
            vo.wait_until("d")
            self.play(lam.animate.set_value(1.5), run_time=2.0)
            self.play(lam.animate.set_value(0.0), run_time=2.0)
        cur.clear_updaters()
        read.clear_updaters()
        self.clear_scene()

    def live(self):
        b = load("boxcox")
        y = np.asarray(b["y"])
        A = axes([-3.5, 5.5], [0, 0.75], x_length=8.6, y_length=4.2, xlabel=r"transformed income, standardized",
                 xticks=[-3, -1, 1, 3, 5], center=[-1.8, -0.6, 0])
        ax = A.ax
        lam = ValueTracker(1.0)
        edges = np.linspace(-3.5, 5.5, 46)

        def hist():
            t = boxcox(y, lam.get_value())
            z = (t - t.mean()) / t.std()
            # Omit off-scale tails; preserve their mass in the denominator rather
            # than moving them into the end bins or renormalizing the visible data.
            counts = np.histogram(z, edges)[0]
            return hist_bars(ax, edges, counts / (len(z) * np.diff(edges)), color=S.EST, stroke_width=0.5)

        h = always_redraw(hist)
        readout = always_redraw(lambda: VGroup(
            MathTex(rf"\lambda = {lam.get_value():.2f}", font_size=38, color=S.ACCENT),
            MathTex(rf"\text{{skewness}} = {stats.skew(boxcox(y, lam.get_value())):.2f}", font_size=34,
                    color=S.EST)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 1.2, 0]))
        zz = np.linspace(-3.5, 5.5, 200)
        bell = curve(ax, zz, stats.norm.pdf(zz), S.TRUTH, 3, smooth=True)
        bl = label(r"a bell, for reference", font_size=22, color=S.TRUTH).move_to([4.6, -0.2, 0])
        tag = simulated_tag(r"simulated: 300 World incomes")
        tails = note(r"tails outside the axis are omitted; \ density uses all 300 incomes").to_edge(UP, buff=0.3)
        with self.voiceover(
            "Watch what the dial does to real data. <bookmark mark='a'/> Three hundred World incomes, transformed, "
            "then standardized so the pictures are comparable. At lambda equal to one the histogram is the raw "
            f"income: skewness {b['skew']['1.0']:.1f}. <bookmark mark='b'/> Turn lambda down to a half, a square root: "
            f"the skew drops to {b['skew']['0.5']:.1f}. <bookmark mark='c'/> At zero, the logarithm: "
            f"{b['skew']['0.0']:.2f}, nearly symmetric. <bookmark mark='d'/> Go further, to minus a half, and you "
            f"overshoot: the skew turns negative, {b['skew']['-0.5']:.1f}, and the long tail is now on the left. "
            "There's a best setting, and it's near zero."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag), FadeIn(tails), Create(bell), FadeIn(bl))
            self.add(h, readout)
            vo.wait_until("b")
            self.play(lam.animate.set_value(0.5), run_time=2.5)
            vo.wait_until("c")
            self.play(lam.animate.set_value(0.0), run_time=2.5)
            vo.wait_until("d")
            self.play(lam.animate.set_value(-0.5), run_time=2.5)
            self.play(lam.animate.set_value(b["lam_hat"]), run_time=2.0)
        h.clear_updaters()
        readout.clear_updaters()
        self.clear_scene()

    def likelihood(self):
        b = load("boxcox")
        lams, ll = np.asarray(b["lams"]), np.asarray(b["ll"])
        top = ll.max()
        A = axes([-1.0, 1.5], [top - 60, top + 8], x_length=8.0, y_length=4.4, xlabel=r"$\lambda$",
                 ylabel=r"log-likelihood $\ell(\lambda)$", xticks=[-1, -0.5, 0, 0.5, 1, 1.5],
                 center=[-1.8, -0.4, 0])
        ax = A.ax
        keep = ll > top - 60
        c = curve(ax, lams[keep], ll[keep], S.LIK, 4)
        lh = b["lam_hat"]
        mark = Line(ax.c2p(lh, top - 60), ax.c2p(lh, top), color=S.EST, stroke_width=3)
        ml = MathTex(rf"\hat\lambda = {lh:.2f}", font_size=34, color=S.EST).next_to(ax.c2p(lh, top), UP, buff=0.12)
        lo, hi = b["lam_lo"], b["lam_hi"]
        if lo <= 0 <= hi:
            near = min(abs(lo), abs(hi)) < 0.15 * (hi - lo)
            zero_says = ("and zero, the logarithm, is inside it" + (", though near its edge" if near else "") +
                         ". So for these incomes, the log is not just convenient. It's consistent with what the data "
                         "choose.")
        else:
            zero_says = ("and zero, the logarithm, is just outside it. The log is a fine round-number choice, but the "
                         "data would prefer a slightly different power.")
        ci = Line(ax.c2p(lo, top - 1.92), ax.c2p(hi, top - 1.92), color=S.EST, stroke_width=6)
        cil = label(rf"plausible: \ ${lo:.2f}$ to ${hi:.2f}$", font_size=26, color=S.EST).next_to(ci, RIGHT, buff=0.3)
        eq = cmath(r"\ell(\lambda)", r"=", r"-\tfrac n2 \log \hat\sigma^2(\lambda)", r"+",
                   r"(\lambda - 1)\sum_i \log y_i", r"+ C", font_size=32, colors={r"(\lambda - 1)\sum_i \log y_i": S.ACCENT})
        eq.scale_to_fit_width(7.0)
        eq.move_to([3.4, 2.4, 0])
        jac = label(r"the Jacobian: \ changing the ruler changes the density", font_size=22,
                    color=S.ACCENT).next_to(eq, DOWN, buff=0.15)
        with self.voiceover(
            "Box and Cox didn't choose lambda by eye. <bookmark mark='a'/> They asked: if some transformation makes "
            "the data exactly normal, which lambda makes these data most probable? That's maximum likelihood, the "
            "workhorse of Parts 9 and 22. <bookmark mark='b'/> The formula has a term you might not expect: lambda "
            "minus one times the sum of the log y's. It's a Jacobian. Stretching the ruler stretches the density, "
            "and a fair comparison between lambdas has to account for it. <bookmark mark='c'/> Here's the "
            f"log-likelihood across lambda. Its peak is at lambda hat equals {lh:.2f}. <bookmark mark='d'/> And the "
            f"curve says how sure to be: every lambda from {lo:.2f} to {hi:.2f} is within the usual margin of the "
            f"peak, {zero_says}"
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(jac))
            vo.wait_until("c")
            self.play(Create(mark), FadeIn(ml))
            vo.wait_until("d")
            self.play(Create(ci), FadeIn(cil))
        self.clear_scene()

    def stabilize(self):
        b = load("boxcox")
        pois, means = np.asarray(b["pois"]), b["pois_means"]
        g = np.random.Generator(np.random.PCG64(9))

        def strip(vals, center, width, height, tf, top, color, title):
            A = axes([-0.5, 3.5], [0, top], x_length=width, y_length=height, center=center)
            A.ax.x_axis.set_opacity(0.3)
            ax = A.ax
            dots = VGroup()
            sds = VGroup()
            for k, v in enumerate(vals):
                tv = tf(v)
                xs = k + 0.35 * (g.random(len(v)) - 0.5)
                dots.add(VGroup(*[Dot(ax.c2p(a, c), radius=0.025, color=color, fill_opacity=0.6)
                                  for a, c in zip(xs[:150], tv[:150])]))
                m, s_ = tv.mean(), tv.std()
                sds.add(VGroup(Line(ax.c2p(k + 0.3, m - s_), ax.c2p(k + 0.3, m + s_), color=S.ACCENT, stroke_width=4),
                               MathTex(f"{s_:.2f}", font_size=24, color=S.ACCENT).next_to(ax.c2p(k + 0.3, m + s_),
                                                                                         UP, buff=0.08)))
            names = VGroup(*[MathTex(rf"\mu = {m}", font_size=22, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                             for k, m in enumerate(means)])
            t = label(title, font_size=26, color=color).next_to(A, UP, buff=0.15)
            return VGroup(A, dots, sds, names, t)

        left = strip(pois, [-3.6, -0.6, 0], 5.6, 4.6, lambda v: v, 175, S.EST, r"Poisson counts")
        right = strip(pois, [3.6, -0.6, 0], 5.4, 4.6, np.sqrt, 14, MEDIAN, r"their square roots")
        rows = [
            cmath(r"\mathrm{Var}\, g(X)", r"\approx", r"g'(\mu)^2\, \mathrm{Var}\, X", font_size=32),
            cmath(r"\mathrm{Var}\, \sqrt X", r"\approx", r"\Big(\frac{1}{2\sqrt\mu}\Big)^2 \mu", r"=", r"\frac14",
                  font_size=32),
        ]
        whys = [why(r"the delta method: \ Part 6"), why(r"Poisson: \ $\mathrm{Var}\, X = \mu$")]
        tag = note(r"computed: 400 draws at each mean").to_corner(DR, buff=0.3)
        with self.voiceover(
            "One more use of a transformation: to make spreads equal. <bookmark mark='a'/> Counts of rare events, "
            "like the deaths by horse kick of Part 3, follow a Poisson distribution, whose variance equals its "
            "mean. So groups with bigger counts are more spread out. Here are four groups, with means two, eight, "
            f"thirty-two and a hundred and twenty-eight. Their standard deviations grow: {b['pois_sd'][0]:.2f}, "
            f"{b['pois_sd'][1]:.2f}, {b['pois_sd'][2]:.2f}, {b['pois_sd'][3]:.2f}. That breaks methods which assume "
            "every group is equally noisy. <bookmark mark='b'/> Take square roots, and the spreads become "
            f"{b['pois_sd_sqrt'][0]:.2f}, {b['pois_sd_sqrt'][1]:.2f}, {b['pois_sd_sqrt'][2]:.2f}, "
            f"{b['pois_sd_sqrt'][3]:.2f}: all close to a half. <bookmark mark='c'/> Why a half? A transformation g "
            "of a variable near its mean changes its variance by the square of g's slope. The slope of the square "
            "root at mu is one over two root mu; square it, multiply by the Poisson variance mu, and the mu "
            "cancels, leaving one quarter. That's the delta method, and Part 6 proves it."
        ) as vo:
            self.play(FadeIn(left[0]), FadeIn(left[1]), FadeIn(left[3]), FadeIn(left[4]), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in left[2]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(right[0]), *[TransformFromCopy(a, c) for a, c in zip(left[1], right[1])],
                      FadeIn(right[3]), FadeIn(right[4]), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(s_) for s_ in right[2]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeOut(left))
            step = ladder(self, rows, whys, keep=2, top=2.4, x=-4.4, buff=0.6)
            step(0)
            step(1)
        self.clear_scene()
