from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


class Scaling(VoiceoverScene):
    def construct(self):
        self.card()
        self.vecchia()
        self.picture()
        self.accuracy()
        self.profile()
        self.big()
        self.others()

    def card(self):
        card = chapter_card(7, r"Scaling up", r"A hundred thousand locations", lit=(1988, 2016), part=PART)
        with self.voiceover("Chapter seven. Scaling up."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def vecchia(self):
        rows = [
            cmath(r"p(z_1, \dots, z_n)", r"=", r"\textstyle\prod_i p(z_i \mid z_1, \dots, z_{i-1})", font_size=32),
            cmath(r"\text{Vecchia (1988)}", r":", r"p(z_i \mid z_{1:i-1}) \approx p(z_i \mid z_{N(i)}), \ \ |N(i)| \le m", font_size=30),
            cmath(r"\text{cost}", r":", r"O(n m^3) \text{ instead of } O(n^3)", font_size=32),
            cmath(r"\text{why it works}", r":", r"\text{nearby observations can approximately screen distant ones}", font_size=30),
        ]
        rows[1][-1].set_color(FIELDC)
        whys = [why(r"exact: \ the chain rule"), why(r"keep only the $m$ nearest earlier points"), why(r"linear in $n$"),
                why(r"the screening effect \ (Stein 2002)")]
        with self.voiceover(
            "<bookmark mark='a'/> Any joint density factors exactly, by the chain rule, into a product of "
            "conditionals: each value given all the earlier ones. <bookmark mark='b'/> Aldo Vecchia's idea of 1988: "
            "condition each value only on its m nearest earlier neighbours. <bookmark mark='c'/> Each factor then "
            "needs only an m by m matrix, so the cost grows linearly in n. <bookmark mark='d'/> It can work well "
            "through approximate screening under suitable covariance and observation conditions: once you know values"
            " close to a point, distant ones add almost nothing, This is not exact conditional independence for a "
            "general Matérn field. Our fast implementation searches among four m nearest overall candidates and may "
            "retain fewer than m earlier points."
        ) as vo:
            intro=label('Vecchia approximates a joint density with smaller conditionals',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        g = np.random.Generator(np.random.PCG64(3911))
        n = 60
        xy = g.random((n, 2))
        P = lambda a: np.array([(a[0] - 0.5) * 6.0 - 1.6, (a[1] - 0.5) * 5.0 + 0.1, 0])
        frame = Rectangle(width=6.0, height=5.0, stroke_color=GREY_B, stroke_width=1.5).move_to([-1.6, 0.1, 0])
        dots = VGroup(*[Dot(P(p), radius=0.06, color=GREY_B) for p in xy])
        i = 45
        prev = np.arange(i)
        dd = np.sqrt(((xy[prev] - xy[i]) ** 2).sum(1))
        nb = prev[np.argsort(dd)[:5]]
        earlier = VGroup(*[dots[j].copy().set_color(FIELDC) for j in prev])
        lines = VGroup(*[Line(P(xy[i]), P(xy[j]), color=TAUC, stroke_width=2.5) for j in nb])
        me = Dot(P(xy[i]), radius=0.11, color=TAUC)
        side = fit_rows(VGroup(
            label(r"points in some order", font_size=22, color=GREY_B),
            label(r"blue: \ the 45 earlier points", font_size=22, color=FIELDC),
            label(r"gold: \ point 46 and its $m = 5$ nearest earlier neighbours", font_size=22, color=TAUC),
            label(r"its conditional uses a $5 \times 5$ matrix, \ not $45 \times 45$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In a picture. Put the locations in some order. <bookmark mark='b'/> When we reach point "
            "forty-six, the exact conditional would involve all forty-five earlier points. <bookmark mark='c'/> Vecchia keeps "
            "only its five nearest earlier neighbours. <bookmark mark='d'/> Each factor is a small regression on a few "
            "neighbours, and they can all be computed in parallel."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(frame), FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(earlier), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(me), Create(lines), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def accuracy(self):
        d = load("scale")
        ms = [1, 3, 5, 10, 20, 30]
        err = [d["exact"] - d["vecchia"][str(m)] for m in ms]
        top = float(np.ceil(max(err) / 100) * 100)
        A = axes([0, 30], [0, top], x_length=7.0, y_length=4.2, xlabel=r"neighbours $m$", ylabel=r"exact $-$ Vecchia log-likelihood",
                 xticks=[0, 10, 20, 30], yticks=list(np.linspace(0, top, 5)), xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-2.6, 0.1, 0])
        ax = A.ax
        c = polyline(ax, ms, err, FIELDC, 3)
        dots = VGroup(*[Dot(ax.c2p(m, e), radius=0.07, color=FIELDC) for m, e in zip(ms, err)])
        side = fit_rows(VGroup(
            label(r"2,000 points, \ $\nu = 3/2$, \ a nugget", font_size=24),
            label(rf"$m = 1$: \ off by {err[0]:.0f}", font_size=24, color=FIELDC),
            label(rf"$m = 10$: \ {err[3]:.0f}; \ \ $m = 30$: \ {err[5]:.1f}", font_size=24, color=FIELDC),
            label(r"a nugget slows convergence", font_size=24, color=MISSC),
            label(r"fix: \ condition on the latent field", font_size=24, color=GREY_A),
            label(r"(Katzfuss \& Guinness 2021)", font_size=24, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How good is it? Two thousand points from a smooth Matérn field with a nugget. <bookmark "
            "mark='b'/> With one neighbour, the log-likelihood is off by " + f"{err[0]:.0f}" + " units; with ten, by "
            + f"{err[3]:.0f}" + "; with thirty, by " + say(err[5], 1) + ". <bookmark mark='c'/> The nugget slows the "
            "convergence: neighbours measured with noise screen off the rest less well. <bookmark mark='d'/> Modern "
            "versions condition on the noise-free field instead, and get much closer with few neighbours."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(dots), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.clear_scene()

    def profile(self):
        d = load("scale")
        grid = np.asarray(d["grid"], float)
        ex, vc = np.asarray(d["prof_ex"], float), np.asarray(d["prof_vc"], float)
        ex, vc = ex - ex.max(), vc - vc.max()
        lo = float(np.floor(min(ex.min(), vc.min()) / 20) * 20)
        A = axes([0.1, 0.35], [lo, 0], x_length=7.0, y_length=4.2, xlabel=r"range $\rho$", ylabel=r"log-likelihood $-$ its maximum",
                 xticks=[0.1, 0.2, 0.3], yticks=list(np.linspace(lo, 0, 5)), xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-2.6, 0.1, 0])
        ax = A.ax
        c1 = polyline(ax, grid, ex, TRUEC, 3)
        c2 = polyline(ax, grid, vc, FIELDC, 3)
        b1, b2 = float(grid[np.argmax(ex)]), float(grid[np.argmax(vc)])
        side = fit_rows(VGroup(
            label(r"gold: \ the exact likelihood in $\rho$", font_size=22, color=TRUEC),
            label(r"blue: \ Vecchia with $m = 10$", font_size=22, color=FIELDC),
            label(rf"grid maxima: exact {b1:.3g}, approximate {b2:.3g}; generating range 0.2", font_size=22, color=BANDC),
            label(r"Vecchia's curve is flatter:", font_size=22, color=GREY_A),
            label(r"curvature-based intervals require separate calibration", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For estimation, what matters is the shape. The exact log-likelihood as a function "
            "of the range, <bookmark mark='b'/> and Vecchia's with ten neighbours, each shifted to peak at zero. "
            "<bookmark mark='c'/> Here their maxima on the displayed grid are close to the generating range. This is "
            "one realization, not a guarantee that the estimates coincide. <bookmark mark='d'/> In this example "
            "Vecchia's curve is flatter, so intervals read off this curve would be wider. Curvature and uncertainty "
            "calibration can be distorted in either direction, and the approximation can move an estimate; it needs "
            "validation."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def big(self):
        d = load("scale")
        rows = fit_rows(VGroup(
            label(r"100,000 locations on the World's island", font_size=28, color=FIELDC),
            label(rf"exact likelihood: \ about {d['cubic_extrap_hours']:,.0f} hours, \ and 80 GB of memory", font_size=28, color=MISSC),
            label(rf"Vecchia, \ $m = 10$: \ {d['big_time']:.1f} seconds, \ on one core", font_size=28, color=BANDC),
            label(r"nearest-neighbour GPs \ (Datta et al.\ 2016): \ Vecchia as a prior, \ for MCMC on millions", font_size=28, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now a timing benchmark with a hundred thousand jittered land-node locations on the "
            "World's island. The field values are reused from the nearest selected grid nodes, so this is a speed "
            "illustration rather than an exact covariance-model simulation at the jittered sites. <bookmark "
            "mark='b'/> The exact likelihood would need about " + f"{d['cubic_extrap_hours']:,.0f}" + " hours and eighty gigabytes of memory for "
            "the matrix alone. <bookmark mark='c'/> Vecchia with ten neighbours takes " + say(d["big_time"], 1) + " seconds "
            "on one core. <bookmark mark='d'/> Abhirup Datta and colleagues turned the idea into a prior, the "
            "nearest-neighbour Gaussian process of 2016, so that Bayesian spatial models with millions of locations can be "
            "fitted by MCMC."
        ) as vo:
            self.add(seeded_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def others(self):
        rows = [[r"approach", r"idea", r"cost"],
                [r"covariance tapering", r"multiply $C$ by a compact taper: \ sparse $K$", r"sparse Cholesky"],
                [r"low rank \ (predictive process)", r"the field through $r$ knots", r"$O(n r^2)$"],
                [r"Vecchia, \ NNGP", r"sparse inverse Cholesky", r"$O(n m^3)$"],
                [r"GMRF, \ SPDE", r"sparse precision", r"chapter 8"]]
        tab = table_rows(rows, font_size=26, col_buff=0.8, row_buff=0.34, colors=[GREY_A, PTC, AREAC, FIELDC, BANDC]).move_to([0, 0.5, 0])
        foot = label(r"Heaton et al.\ (2019): \ a competition of all of them on one data set; \ Vecchia and SPDE did best", font_size=22, color=GREY_A).move_to([0, -2.2, 0])
        if foot.width > 12.4:
            foot.width = 12.4
        with self.voiceover(
            "<bookmark mark='a'/> Other ways to scale. <bookmark mark='b'/> Tapering multiplies the covariance by a "
            "function that is exactly zero beyond some distance, so the matrix becomes sparse. <bookmark mark='c'/> Low-rank "
            "methods represent the field through a few hundred knots, but they smooth away the short-range detail. "
            "<bookmark mark='d'/> Vecchia makes the inverse Cholesky factor sparse. <bookmark mark='e'/> And Markov random "
            "fields make the precision matrix sparse, the subject of chapter eight. <bookmark mark='f'/> A 2019 "
            "competition led by Matthew Heaton put all of them on the same large data set; the Vecchia-type and SPDE "
            "methods did best."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
