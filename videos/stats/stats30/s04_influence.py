from __future__ import annotations

import numpy as np

from explainer.stats.kit import robust as R
from videos.stats.stats30.common import *  # noqa: F403


class Influence(VoiceoverScene):
    def construct(self):
        self.card()
        self.gross()
        self.rail()
        self.rail_middle()
        self.sensitivity()
        self.definition()
        self.sd_if()
        self.theory()
        self.properties()
        self.hampel_opt()

    def card(self):
        card = chapter_card(3, r"Gross errors and influence", r"What one bad point can do", lit=(1974,), part=PART)
        with self.voiceover("Chapter three. Gross errors and influence functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def gross(self):
        rows = [
            cmath(r"F_\varepsilon", r"=", r"(1 - \varepsilon) F + \varepsilon\, \delta_z", font_size=32),
            cmath(r"T(F_\varepsilon)", r"\approx", r"T(F) + \varepsilon\, \mathrm{IF}(z; T, F)", font_size=32),
            cmath(r"\mathrm{IF}(z)", r"=", r"\lim_{\varepsilon \to 0} \dfrac{T(F_\varepsilon) - T(F)}{\varepsilon}", font_size=30),
            cmath(r"\text{sample}", r":", r"\mathrm{SC}(z) = (n + 1)\bigl(T(x_1, \dots, x_n, z) - T(x_1, \dots, x_n)\bigr)", font_size=26),
        ]
        rows[2][2].set_color(HLC)
        whys = [why(r"a gross-error model: \ a little mass at $z$"), why(r"a functional's derivative"),
                why(r"Hampel (1968, 1974)"), why(r"Tukey's sensitivity curve")]
        with self.voiceover(
            "<bookmark mark='a'/> Frank Hampel's framework. Think of an estimator as a functional T of the distribution. "
            "Contaminate the distribution by moving a small mass epsilon to a single point z. <bookmark mark='b'/> To first "
            "order, the estimate moves by epsilon times a function of z: <bookmark mark='c'/> the influence function, the "
            "derivative of the functional in the direction of a point mass at z. <bookmark mark='d'/> Its sample version is "
            "Tukey's sensitivity curve: add one observation at z, and record n plus one times the change in the estimate."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rail(self):
        d = load("influence")
        x = np.asarray(d["clean"])[:24]
        est = [(r"mean", np.mean, MEANC), (r"median", np.median, MEDC), (r"Hodges--Lehmann", R.hodges_lehmann, HLC),
               (r"Huber", lambda z: R.m_location(z, "huber")["mu"], HUBC), (r"biweight", lambda z: R.m_location(z, "biweight")["mu"], BIWC)]
        rail = EstimatorRail(x, est, (10, 90), index=int(np.argmax(x)), width=9.6, center=[0.6, 0.3, 0], font_size=20)
        rows = fit_rows(VGroup(
            label(r"24 of Newcomb's clean measurements; \ drag the largest one out", font_size=22),
            label(r"the mean follows it all the way", font_size=22, color=MEANC),
            label(r"median, \ Hodges--Lehmann, \ Huber: \ move a little, \ then stop", font_size=22, color=HLC),
            label(r"the biweight comes back: \ it rejects the point", font_size=22, color=BIWC),
        ), 12.0, 0.2, [0, -2.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The estimator rail, this part's instrument: two dozen of Newcomb's measurements on a line, "
            "and below, five estimates of their centre. Take the largest observation and drag it to the right. "
            "<bookmark mark='b'/> The mean follows it, without limit. <bookmark mark='c'/> The median, Hodges–Lehmann and "
            "Huber's estimate move a little at first and then stop: beyond some point, how far out the observation is no "
            "longer matters. <bookmark mark='d'/> The biweight moves and then comes back: once the point is far enough out, "
            "it is given weight zero, as if rejected."
        ) as vo:
            self.add(newcomb_tag())
            self.play(FadeIn(rail))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(rail.drag(60.0, run_time=4.0), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(rail.drag(80.0, run_time=2.0), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(rail.drag(89.0, run_time=2.0), FadeIn(rows[3]))
        rail.stop()
        self.clear_scene()

    def sensitivity(self):
        d = load("influence")
        g = np.asarray(d["grid"])
        A = axes([-60, 90], [-30, 50], x_length=7.4, y_length=4.4, xlabel=r"position of the added point $z$",
                 ylabel=r"sensitivity curve", xticks=[-50, 0, 50], yticks=[-20, 0, 20, 40], center=[-2.0, 0.3, 0])
        ax = A.ax
        spec = (("mean", MEANC), ("median", MEDC), ("hl", HLC), ("huber", HUBC), ("biweight", BIWC))
        cs = {k: clip_curve(ax, g, np.asarray(d["sc"][k]), c, 3, ymin=-30, ymax=50) for k, c in spec}
        rows = fit_rows(VGroup(
            label(r"Newcomb's 64 clean measurements, \ plus one at $z$", font_size=22),
            label(r"mean: \ a straight line, \ unbounded", font_size=22, color=MEANC),
            label(r"median: \ a step", font_size=22, color=MEDC),
            label(r"Hodges--Lehmann, \ Huber: \ bounded", font_size=22, color=HLC),
            label(r"biweight: \ bounded, \ and back to zero", font_size=22, color=BIWC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The sensitivity curves, on all sixty-four clean measurements. <bookmark mark='b'/> The "
            "mean's is a straight line: one observation can move it anywhere. <bookmark mark='c'/> The median's is a step: "
            "it only cares which side of the centre the point is on. <bookmark mark='d'/> Hodges–Lehmann's and Huber's rise "
            "and level off. <bookmark mark='e'/> The biweight's rises, then falls back to zero: a far enough point has no "
            "influence at all. Estimators with this shape are called redescending."
        ) as vo:
            self.add(newcomb_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, ((key, _), m_) in enumerate(zip(spec[:2], "bc")):
                vo.wait_until(m_)
                self.play(Create(cs[key]), FadeIn(rows[k + 1]))
            vo.wait_until("d")
            self.play(Create(cs["hl"]), Create(cs["huber"]), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(cs["biweight"]), FadeIn(rows[4]))
        self.clear_scene()

    def definition(self):
        rows = [
            cmath(r"\gamma^*", r"=", r"\sup_z |\mathrm{IF}(z)|", font_size=32),
            cmath(r"\text{mean}", r":", r"\mathrm{IF} = z - \mu: \ \ \gamma^* = \infty", font_size=30),
            cmath(r"\text{median}", r":", r"\mathrm{IF} = \dfrac{\mathrm{sign}(z - m)}{2 f(m)}: \ \ \gamma^* = \sqrt{\pi/2} = 1.25", font_size=28),
            cmath(r"\text{M-estimator}", r":", r"\mathrm{IF} = \psi(z) / E\,\psi'(X)", font_size=30),
        ]
        rows[3][2].set_color(HUBC)
        whys = [why(r"the gross-error sensitivity"), why(r"one point can move it anywhere"), why(r"at the standard normal"),
                why(r"the influence function is the $\psi$")]
        with self.voiceover(
            "<bookmark mark='a'/> The worst influence, the supremum of its absolute value, is the gross-error sensitivity. "
            "<bookmark mark='b'/> For the mean the influence function is z minus mu: unbounded. <bookmark mark='c'/> For the "
            "median it is plus or minus one over twice the density at the median, at the standard normal one point two five, "
            "the smallest of any consistent estimator. <bookmark mark='d'/> For an M-estimator, the solution of a sum of psi "
            "functions equal to zero, it is psi itself, scaled: so you design the influence function by choosing psi."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def theory(self):
        d = load("influence")
        z = np.asarray(d["z"])
        A = axes([-5, 5], [-3, 3], x_length=7.4, y_length=4.4, xlabel=r"$z$ (standard units)", ylabel=r"IF$(z)$ at $N(0, 1)$",
                 xticks=[-4, -2, 0, 2, 4], yticks=[-2, 0, 2], center=[-2.0, 0.3, 0])
        ax = A.ax
        spec = (("mean", MEANC), ("median", MEDC), ("trim10", TRIMC), ("huber", HUBC), ("biweight", BIWC))
        cs = {k: clip_curve(ax, z, np.asarray(d["theo"][k]), c, 3, ymin=-3, ymax=3) for k, c in spec}
        gr = d["gross"]
        rows = fit_rows(VGroup(
            label(r"the influence functions at the standard normal", font_size=22),
            label(r"mean: \ unbounded", font_size=22, color=MEANC),
            label(rf"median: \ $\pm {gr['median']:.2f}$", font_size=22, color=MEDC),
            label(rf"10\% trimmed: \ $\pm {gr['trim10']:.2f}$; \ Huber: \ $\pm {gr['huber']:.2f}$", font_size=22, color=HUBC),
            label(rf"biweight: \ peak {gr['biweight']:.2f}, \ zero beyond 4.69", font_size=22, color=BIWC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The theoretical influence functions at the standard normal. <bookmark mark='b'/> The "
            "mean's line. <bookmark mark='c'/> The median's step, at one point two five. <bookmark mark='d'/> The trimmed "
            "mean and Huber's estimate are linear in the middle, like the mean, and clipped at about one point six: almost "
            "the mean's efficiency, with bounded influence. <bookmark mark='e'/> The biweight is linear near zero, peaks at "
            "one point seven seven, and returns to zero beyond four point six nine standard units."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cs["mean"]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cs["median"]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(cs["trim10"]), Create(cs["huber"]), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(cs["biweight"]), FadeIn(rows[4]))
        self.clear_scene()

    def properties(self):
        rows = [
            cmath(r"\textstyle\int \mathrm{IF}\, dF", r"=", r"0", font_size=32),
            cmath(r"\textstyle\int \mathrm{IF}^2\, dF", r"=", r"\text{the asymptotic variance}", font_size=30),
            cmath(r"\sqrt n\,(T(F_n) - T(F))", r"\approx", r"\tfrac{1}{\sqrt n} \textstyle\sum_i \mathrm{IF}(X_i)", font_size=30),
            cmath(r"\text{trade-off}", r":", r"\text{bounded } \gamma^* \ \text{vs \ small variance}", font_size=30),
        ]
        rows[2][2].set_color(HLC)
        whys = [why(r"it averages to zero"), why(r"Part 22's sandwich, \ in disguise"), why(r"the von Mises expansion"),
                why(r"Hampel's optimality problem: \ chapter five")]
        with self.voiceover(
            "<bookmark mark='a'/> Two facts make the influence function central. It averages to zero over the distribution. "
            "<bookmark mark='b'/> Its mean square is the estimator's asymptotic variance, Part 22's sandwich in another form. "
            "<bookmark mark='c'/> Because the estimator, to first order, is the average of the influence of each observation, "
            "the von Mises expansion. <bookmark mark='d'/> So bounded influence and small variance pull against each other, "
            "and the best compromise is chapter five's problem."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hampel_opt(self):
        rows = [
            cmath(r"\min_\psi", r"\ ", r"V(\psi, \Phi) \ \text{ subject to } \ \gamma^*(\psi) \le c", font_size=30),
            cmath(r"\text{solution}", r":", r"\psi(z) = \max(-k, \min(k, z)), \ \ k = k(c)", font_size=30),
            cmath(r"\text{so}", r":", r"\text{Huber's } \psi \text{ again, \ from a different question}", font_size=30),
            cmath(r"c \to \sqrt{\pi/2}", r":", r"\text{the median: \ the most robust}", font_size=30),
        ]
        rows[2][2].set_color(HUBC)
        whys = [why(r"Hampel's optimality problem"), why(r"bounded, \ linear in the middle"),
                why(r"Hampel (1968): \ the same answer as Huber's minimax"), why(r"the smallest possible sensitivity")]
        with self.voiceover(
            "<bookmark mark='a'/> Hampel posed the trade-off as an optimization: minimize the variance at the normal, subject "
            "to a bound c on the gross-error sensitivity. <bookmark mark='b'/> The solution is the identity, clipped at plus "
            "and minus k: <bookmark mark='c'/> Huber's psi again, reached from a different question, which is part of why it "
            "is so widely used. <bookmark mark='d'/> As c falls to its smallest possible value, root pi over two, k shrinks "
            "to zero and the solution becomes the median, the most robust estimator of all."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rail_middle(self):
        from explainer.stats.kit import robust as RR
        d = load("influence")
        x = np.asarray(d["clean"])[:24]
        est = [(r"mean", np.mean, MEANC), (r"median", np.median, MEDC), (r"Hodges--Lehmann", RR.hodges_lehmann, HLC),
               (r"Huber", lambda z: RR.m_location(z, "huber")["mu"], HUBC)]
        rail = EstimatorRail(x, est, (10, 50), index=int(np.argmin(x)), width=9.6, center=[0.6, 0.4, 0], font_size=20)
        rows = fit_rows(VGroup(
            label(r"now slide the smallest point slowly across the middle", font_size=22),
            label(r"the median jumps as the point crosses it: \ influence is a step", font_size=22, color=MEDC),
            label(r"the others glide: \ smooth influence, \ like the mean's near the centre", font_size=22, color=HLC),
        ), 12.0, 0.2, [0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The rail shows the shape near the centre too. Slide the smallest point slowly from the left "
            "across the middle of the data. <bookmark mark='b'/> The median doesn't move at all until the point crosses it, "
            "then jumps: its influence is a step, which also makes it inefficient. <bookmark mark='c'/> Hodges–Lehmann and "
            "Huber glide smoothly, like the mean does, for points near the centre. They behave like the mean where the mean "
            "is good, and like the median where the mean fails."
        ) as vo:
            self.add(newcomb_tag())
            self.play(FadeIn(rail))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(rail.drag(30.0, run_time=5.0), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(rail.drag(40.0, run_time=3.0), FadeIn(rows[2]))
        rail.stop()
        self.clear_scene()

    def sd_if(self):
        rows = [
            cmath(r"T(F)", r"=", r"\sigma(F) = \sqrt{\mathrm{Var}_F X}", font_size=30),
            cmath(r"\mathrm{IF}(z; \sigma, \Phi)", r"=", r"\tfrac12 (z^2 - 1)", font_size=32),
            cmath(r"\mathrm{IF}(z; d, \Phi)", r"=", r"|z| - \sqrt{2/\pi}", font_size=32),
            cmath(r"\text{Tukey's duel}", r":", r"\text{quadratic against linear influence}", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"the standard deviation as a functional"), why(r"quadratic: \ far points dominate"),
                why(r"the mean deviation: \ linear"), why(r"both unbounded, \ one far worse")]
        with self.voiceover(
            "<bookmark mark='a'/> The hook's duel, seen through influence functions. Treat the standard deviation as a "
            "functional of the distribution. <bookmark mark='b'/> At the normal its influence function is half of z squared "
            "minus one: quadratic, so a point at ten standard units counts fifty times as much as a typical one. "
            "<bookmark mark='c'/> The mean deviation's is the absolute value of z minus a constant: only linear. "
            "<bookmark mark='d'/> Both are unbounded, but one grows far faster, which is exactly why Tukey's rare wide errors "
            "hurt the standard deviation so much more."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
