from __future__ import annotations

import numpy as np

from videos.stats.stats12.common import *  # noqa: F403


class Diagnostics(VoiceoverScene):
    def construct(self):
        self.card()
        self.quartet()
        self.leverage()
        self.probe()
        self.cooks()
        self.honesty()
        self.residual_plots()
        self.qq()

    def card(self):
        card = chapter_card(9, r"Diagnostics", r"Look at the data, \ not just the fit", lit=(1973,), part=PART)
        with self.voiceover("Chapter nine. Diagnostics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def quartet(self):
        d = load("anscombe")
        panels = VGroup()
        for j, k in enumerate(("1", "2", "3", "4")):
            c = d[k]
            r_, col = divmod(j, 2)
            A = axes([3, 20], [2, 14], x_length=4.0, y_length=2.4, xticks=[5, 10, 15, 20], yticks=[5, 10], center=[-3.0 + 6.0 * col, 1.4 - 3.2 * r_, 0],
                     font_size=16)
            ax = A.ax
            pts = scatter(ax, c["x"], c["y"], radius=0.05)
            ln = fit_line(ax, c["coef"][0], c["coef"][1], 3, 20, FIT, 2.5)
            t = MathTex(rf"{k}:\ \ \hat y = {c['coef'][0]:.2f} + {c['coef'][1]:.3f}x,\ \ R^2 = {c['r2']:.2f}", font_size=20, color=GREY_A).next_to(A, DOWN, buff=0.08)
            panels.add(VGroup(A, pts, ln, t))
        src = historical_tag(r"Anscombe (1973)", corner=UR)
        with self.voiceover(
            "In 1973 Francis Anscombe published four small datasets to make a point. <bookmark mark='a'/> All four have the "
            "same means, the same variances, the same correlation, and the same fitted line: three plus a half x, with R "
            "squared of point six seven. <bookmark mark='b'/> The first is an ordinary noisy line. The second is a smooth curve, "
            "for which a straight line is the wrong model. The third is nearly a line with one outlier. The fourth has no "
            "relationship at all, except for a single point far to the right that decides the entire slope. "
            "<bookmark mark='c'/> Identical numbers, four different stories. Diagnostics are how you tell them apart without "
            "having to look at every plot."
        ) as vo:
            self.play(FadeIn(src), *[FadeIn(p[0]) for p in panels])
            vo.wait_until("a")
            self.play(*[Create(p[2]) for p in panels], *[FadeIn(p[3]) for p in panels])
            vo.wait_until("b")
            for p in panels:
                self.play(FadeIn(p[1], lag_ratio=0.05), run_time=0.9)
        self.clear_scene()

    def leverage(self):
        rows = [
            cmath(r"h_{ii}", r"=", r"[H]_{ii} = \frac1n + \frac{(x_i - \bar x)^2}{\sum_j (x_j - \bar x)^2}", font_size=34),
            cmath(r"\textstyle\sum_i h_{ii}", r"=", r"p", r"\quad\text{average leverage } p/n", font_size=34),
            cmath(r"\mathrm{Var}(e_i)", r"=", r"\sigma^2(1 - h_{ii})", font_size=34),
            cmath(r"r_i", r"=", r"\frac{e_i}{s\sqrt{1 - h_{ii}}}", r"\quad\text{studentized residuals}", font_size=34),
        ]
        rows[0][2].set_color(OBS)
        whys = [why(r"leverage: \ how far $x_i$ is from the others"), why(r"the trace of the hat matrix (ch.~2)"),
                why(r"high-leverage points pull the line to themselves: \ small residuals"), why(r"put residuals on a common scale")]
        intro = label('Separate unusual predictors from unusual residuals', font_size=36)
        with self.voiceover(
            "Two quantities do most of the work. <bookmark mark='a'/> The leverage of a point is its diagonal entry in the hat "
            "matrix, and for one predictor it measures how far its x is from the others. <bookmark mark='b'/> Leverages add up "
            "to p, so the average is p over n. <bookmark mark='c'/> A residual's variance is sigma squared times one minus the "
            "leverage: high-leverage points drag the line toward themselves, so their residuals look deceptively small. "
            "<bookmark mark='d'/> Dividing by that standard deviation gives the studentized residuals, which are comparable "
            "across points."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def probe(self):
        g = np.random.Generator(np.random.PCG64(1977))
        x = np.r_[g.uniform(1, 9, 19), 5.0]
        y = 1 + 0.8 * x + g.normal(0, 0.8, 20)
        y[-1] = 1 + 0.8 * 5.0
        A = axes([0, 20], [-4, 18], x_length=7.4, y_length=5.0, xlabel=r"$x$", ylabel=r"$y$", xticks=[0, 5, 10, 15, 20], yticks=[0, 5, 10, 15],
                 center=[-2.2, -0.3, 0])
        ax = A.ax
        pr = InfluenceProbe(ax, x, y, index=-1, x_span=(0, 20))
        pr.readout_pos = np.array([4.6, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"Built: \ the influence probe", font_size=26, color=OBS),
            label(r"drag one point; \ the line refits live", font_size=22, color=GREY_A),
            label(r"far in $y$ at central $x$: \ big residual, \ limited slope effect", font_size=22),
            label(r"far in $x$ only: \ high leverage, \ on the line", font_size=22),
            label(r"far in both: \ it moves the line", font_size=22, color=S.ACCENT),
        ), 4.6, 0.3, [4.6, -1.6, 0])
        with self.voiceover(
            "Here's the instrument built for this part, the influence probe. <bookmark mark='a'/> Twenty points and their "
            "fitted line. One point, in orange, can be dragged, and the line refits as it moves. The readout shows the slope, "
            "the point's leverage, and its Cook's distance, which measures how much the whole fit depends on it. "
            "<bookmark mark='b'/> Move it straight up, in the middle of the data. It gets a big residual, but the slope barely "
            "changes: at the centre, a point has little leverage. <bookmark mark='c'/> Now bring it back and slide it far to "
            "the right, along the line. Its leverage soars, but it agrees with the others, so nothing changes. "
            "<bookmark mark='d'/> Finally, far to the right and far off the line. Now the slope swings, and Cook's distance "
            "explodes. Influence needs both: leverage, from an unusual x, and a residual, from an unusual y."
        ) as vo:
            self.play(FadeIn(A))
            self.add(pr, pr.readout)
            self.play(FadeIn(pr), FadeIn(pr.readout), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(pr.move_to_point(5.0, 15.0, run_time=3.0))
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(pr.move_to_point(5.0, 5.0, run_time=1.5))
            self.play(pr.move_to_point(19.0, 1 + 0.8 * 19, run_time=3.0))
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(pr.move_to_point(19.0, -2.0, run_time=3.0))
            self.play(FadeIn(rows[4]))
        pr.stop()
        self.clear_scene()

    def cooks(self):
        d = load("anscombe")
        rows = [
            cmath(r"D_i", r"=", r"\frac{\|\hat y - \hat y_{(i)}\|^2}{p\,s^2} = \frac{r_i^2}{p}\cdot\frac{h_{ii}}{1 - h_{ii}}", font_size=34),
            cmath(r"\text{Anscombe 3}", r":", rf"\max D_i = {max(d['3']['cooks']):.2f}", r"\quad\text{the outlier}", font_size=32),
            cmath(r"\text{Anscombe 4}", r":", rf"h_{{ii}} = {max(d['4']['lev']):.2f}", r"\quad D_i \text{ undefined: the fit passes through it}", font_size=30),
        ]
        rows[0][2].set_color(S.ACCENT)
        whys = [why(r"Cook (1977): \ how far the fits move when point $i$ is deleted"), why(r"$D > 1$: \ look hard"),
                why(r"leverage 1: \ the slope is that one point")]
        with self.voiceover(
            "<bookmark mark='a'/> Dennis Cook's distance, from 1977, summarizes influence in one number: how far all the fitted "
            "values move when a point is deleted, scaled by the noise. It's a residual squared times a function of leverage, "
            "so it needs both. <bookmark mark='b'/> In Anscombe's third dataset, the outlier has a Cook's distance of one point "
            "four. A common rule of thumb says anything above one deserves a hard look. <bookmark mark='c'/> In the fourth, the "
            "lone point on the right has leverage exactly one: the slope is determined by that single point, the fit passes "
            "through it, and its residual is zero. Deleting it leaves no slope at all."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.4, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def residual_plots(self):
        d = load("anscombe")["2"]
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        fitted = d["coef"][0] + d["coef"][1] * x
        res = y - fitted
        A = axes([4, 11], [-2.5, 1.5], x_length=6.0, y_length=4.0, xlabel=r"fitted value", ylabel=r"residual", xticks=[5, 7, 9, 11],
                 yticks=[-2, 0, 1], center=[-2.8, -0.3, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(4, 0), ax.c2p(11, 0), color=GREY_B, stroke_width=1.5)
        pts = scatter(ax, fitted, res)
        rows = fit_rows(VGroup(
            label(r"Anscombe 2: \ residuals against fitted values", font_size=24),
            label(r"a curve: \ the model is missing a term", font_size=24, color=RES),
            label(r"a funnel: \ uneven noise (ch.~10)", font_size=24, color=GREY_A),
            label(r"a few far points: \ outliers or influence", font_size=24, color=GREY_A),
            label(r"a shapeless cloud: \ what you hope to see", font_size=24, color=FIT),
        ), 5.2, 0.34, [4.0, -0.3, 0])
        with self.voiceover(
            "The single most useful diagnostic is a plot. <bookmark mark='a'/> Plot the residuals against the fitted values. "
            "For Anscombe's second dataset, the residuals form an arch. <bookmark mark='b'/> A curve means the model is missing "
            "a term: here, a square. <bookmark mark='c'/> A funnel means the noise grows with the fitted value, the subject of "
            "the next chapter. <bookmark mark='d'/> A few far points mean outliers or influence. <bookmark mark='e'/> A shapeless "
            "cloud is what you hope to see: whatever's left is noise."
        ) as vo:
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(pts, lag_ratio=0.1), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def honesty(self):
        rows = fit_rows(VGroup(
            label(r"what to do with an influential point", font_size=30, color=OBS),
            label(r"check it: \ a typing error, \ a different population, \ a broken instrument?", font_size=24),
            label(r"report the fit with and without it; \ if conclusions change, \ say so", font_size=24),
            label(r"never delete points just because they are inconvenient: \ that is a forking path (Part 10)", font_size=24, color=MISS),
            label(r"if outliers are expected, \ use a method built for them: \ robust regression (Part 30)", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What should you do with an influential point? <bookmark mark='b'/> First, check it. Is it a "
            "typing error, a member of a different population, a broken instrument? <bookmark mark='c'/> Then report the fit "
            "with and without it, and if the conclusions change, say so. <bookmark mark='d'/> Never delete points simply because "
            "they're inconvenient: that's one of Part 10's forking paths. <bookmark mark='e'/> And if outliers are part of the "
            "process, use a method designed for them, the robust regression of Part 30."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def qq(self):
        from scipy import stats as st
        from explainer.stats.kit import ols as O
        d = load("hetsim")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        r = O.fit(O.design(x), y)
        rs = np.sort(r.student)
        q = st.norm.ppf((np.arange(1, len(rs) + 1) - 0.5) / len(rs))
        A = axes([-3, 3], [-6, 6], x_length=5.4, y_length=4.6, xlabel=r"normal quantiles", ylabel=r"studentized residuals", xticks=[-2, 0, 2],
                 yticks=[-5, 0, 5], center=[-3.0, -0.3, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(-3, -3), ax.c2p(3, 3), color=GREY_B, stroke_width=1.5)
        keep = np.abs(rs) < 6
        pts = scatter(ax, q[keep], rs[keep], radius=0.04)
        rows = fit_rows(VGroup(
            label(r"the normal quantile plot (Part 1) of the residuals", font_size=24),
            label(r"near the line: \ compatible with IID homoskedastic normal errors", font_size=22, color=GREY_A),
            label(r"tails bending away: \ heavy tails or outliers", font_size=22, color=RES),
            label(r"here: \ chapter 10's funnel data, \ with tails far heavier than normal", font_size=22, color=OBS),
        ), 5.2, 0.34, [3.9, -0.3, 0])
        with self.voiceover(
            "One more plot belongs in every regression. <bookmark mark='a'/> Part 1's normal quantile plot, applied to the "
            "studentized residuals. Under IID homoskedastic normal errors, these dependent internally studentized residuals should lie approximately near the diagonal; this is a diagnostic, not a proof. <bookmark mark='b'/> Here they "
            "don't: both tails bend away, far heavier than normal. These are the funnel-shaped data of the next chapter, where "
            "the noisiest points are also the most influential. The plot can't tell you why the tails are heavy, but it tells "
            "you to find out."
        ) as vo:
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(pts, lag_ratio=0.01), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()
