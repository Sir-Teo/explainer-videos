from __future__ import annotations

import numpy as np

from videos.stats.stats21.common import *  # noqa: F403


class MM(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.median()
        self.family()
        self.engel()
        self.bradley_terry()
        self.verdict()

    def card(self):
        card = chapter_card(6, r"MM algorithms", r"Minimize a simpler function, \ again and again", part=PART)
        with self.voiceover("Chapter six. MM algorithms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"g(\theta \mid \theta_k)", r"\ge", r"f(\theta) \ \ \text{for all } \theta", font_size=30),
            cmath(r"g(\theta_k \mid \theta_k)", r"=", r"f(\theta_k)", font_size=30),
            cmath(r"\theta_{k+1}", r"=", r"\arg\min_\theta g(\theta \mid \theta_k)", font_size=30),
            cmath(r"f(\theta_{k+1})", r"\le", r"g(\theta_{k+1} \mid \theta_k) \le g(\theta_k \mid \theta_k) = f(\theta_k)", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"a majorizer: \ above $f$ everywhere"), why(r"touching it at the current point"),
                why(r"minimize the easy surrogate instead"), why(r"so $f$ never goes up: \ the descent property")]
        with self.voiceover(
            "MM stands for majorize, then minimize, a principle Kenneth Lange and others built into a general method. "
            "<bookmark mark='a'/> At the current point, build a surrogate function g that lies above f everywhere, "
            "<bookmark mark='b'/> and touches it at the current point. <bookmark mark='c'/> Minimize the surrogate, which is "
            "chosen to be easy, often a quadratic. <bookmark mark='d'/> Then f at the new point is at most the surrogate there, "
            "which is at most the surrogate at the old point, which equals f there. The objective can never increase. No line "
            "search, no tuning."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def median(self):
        d = load("mm")
        x = np.asarray(d["x"])
        grid = np.asarray(d["grid"])
        f = np.asarray(d["f"])
        A = axes([-1, 13], [0, 50], x_length=8.4, y_length=4.4, xlabel=r"$\theta$", ylabel=r"$\sum_i |x_i - \theta|$",
                 xticks=[0, 2, 4, 6, 8, 10, 12], yticks=[0, 25, 50], center=[-1.4, 0.3, 0])
        ax = A.ax
        fc = curve(ax, grid, f, FIT, 3.5)
        ticks = VGroup(*[Line(ax.c2p(v, 0), ax.c2p(v, 2.5), color=GREY_B, stroke_width=2) for v in x])
        maj, mins = VGroup(), VGroup()
        for k, th in enumerate(d["thetas"][:4]):
            w = 1 / (1e-9 + np.abs(x - th))
            g = np.array([np.sum(w * (x - t) ** 2 / 2 + np.abs(x - th) / 2) for t in grid])
            m = g < 50
            maj.add(curve(ax, grid[m], g[m], PATH, 2.5))
            mins.add(Dot(ax.c2p(th, float(np.sum(np.abs(x - th)))), radius=0.08, color=PATH))
        rows = fit_rows(VGroup(
            label(r"seven numbers; \ the median minimizes the blue curve", font_size=22),
            label(r"$|r| \le \dfrac{r^2}{2|r_k|} + \dfrac{|r_k|}{2}$: \ a parabola above each kink", font_size=22, color=PATH),
            label(r"minimize the parabola: \ a weighted mean, \ weights $1/|x_i - \theta_k|$", font_size=22, color=PATH),
            label(rf"$\theta$: \ {d['thetas'][0]:.1f} $\to$ {d['thetas'][1]:.2f} $\to$ {d['thetas'][2]:.2f} $\to$ {d['thetas'][3]:.2f} $\to \cdots \to$ 4", font_size=22),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The simplest example: the median of seven numbers, which minimizes the sum of absolute "
            "deviations, the blue curve with a kink at every data point. <bookmark mark='b'/> Each absolute value lies below a "
            "parabola that touches it at the current residual. Add them up and you have a smooth majorizer, in gold, touching "
            "the blue curve at the current guess, nine. <bookmark mark='c'/> Its minimum is a weighted mean, with weight one "
            "over each point's current distance, and that is the next guess. <bookmark mark='d'/> Nine, then seven point oh "
            "nine, then six point eight six, then six point seven six: each step downhill, on its way to the median, four."
        ) as vo:
            self.play(FadeIn(A), Create(fc), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(mins[0], scale=1.5), Create(maj[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(mins[1], scale=1.5))
            vo.wait_until("d")
            for k in (1, 2, 3):
                self.play(FadeOut(maj[k - 1]), Create(maj[k]), FadeIn(mins[k], scale=1.5), run_time=1.2)
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def family(self):
        rows = [
            cmath(r"\text{EM}", r":", r"\text{the expected complete-data log likelihood minorizes}", font_size=28),
            cmath(r"\text{IRLS for LAD, \ quantiles}", r":", r"\text{the parabola above } |r| \text{ (Hunter \& Lange 2000)}", font_size=28),
            cmath(r"\text{Weiszfeld (1937)}", r":", r"\text{the spatial median}", font_size=28),
            cmath(r"\text{multidimensional scaling}", r":", r"\text{SMACOF (de Leeuw 1977)}", font_size=28),
        ]
        rows[0][2].set_color(PATH)
        whys = [why(r"Dempster, \ Laird \& Rubin (1977): \ Part 22"), why(r"the median example, \ in regression"),
                why(r"the same weights, \ in the plane"), why(r"Part 31")]
        with self.voiceover(
            "Many famous algorithms turn out to be MM in disguise. <bookmark mark='a'/> The EM algorithm, the next part's main "
            "tool, is MM for maximization: the expected log likelihood of the complete data lies below the real one and "
            "touches it. <bookmark mark='b'/> Hunter and Lange's algorithm for quantile regression uses the parabola trick we "
            "just saw. <bookmark mark='c'/> Weiszfeld's 1937 algorithm for the spatial median is the same weighted mean in two "
            "dimensions. <bookmark mark='d'/> And so is de Leeuw's SMACOF for multidimensional scaling, in Part 31."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def engel(self):
        d = load("mm")
        obj = np.asarray(d["engel_mm"])
        gap = np.maximum(obj - d["engel_lp"], 1e-4)
        ks = np.arange(len(gap))
        A = axes([0, len(gap)], [-4, 3], x_length=8.0, y_length=4.2, xlabel=r"MM iteration", ylabel=r"gap to the LP optimum (log$_{10}$)",
                 xticks=[0, 20, 40, 60], yticks=[-4, -2, 0, 2], center=[-1.6, 0.3, 0])
        ax = A.ax
        ln = polyline(ax, ks, np.log10(gap), PATH, 3.5)
        rows = fit_rows(VGroup(
            label(r"median regression of Engel's food spending", font_size=22),
            label(rf"the LP optimum: \ {d['engel_lp']:,.1f}", font_size=22, color=NEWT),
            label(r"MM: \ weighted least squares, \ again and again", font_size=22, color=PATH),
            label(r"always downhill; \ steadily, \ not quadratically", font_size=22, color=HIT),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's MM doing median regression on Engel's households, each step a weighted least squares "
            "fit. <bookmark mark='b'/> The linear program gives the exact optimum. <bookmark mark='c'/> MM's objective falls "
            "toward it, <bookmark mark='d'/> never rising, a little closer at every step, but linearly, not with Newton's "
            "doubling digits. That's the usual bargain: reliable, simple, and sometimes slow."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ln), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def bradley_terry(self):
        d = load("bt")
        teams = d["teams"]
        wins = np.asarray(d["wins"], int)
        hdr = [r"\textbf{wins over}"] + [rf"\textbf{{{t}}}" for t in teams] + [r"\textbf{strength}"]
        body = [[teams[i]] + [("--" if i == j else str(wins[i, j])) for j in range(4)] + [f"{d['g'][i]:.2f}"] for i in range(4)]
        t = table_rows([hdr] + body, font_size=24, col_buff=0.55, row_buff=0.26, colors=[GREY_A] + [None] * 4)
        for r in t[1:]:
            r[-1].set_color(PATH)
        t.move_to([0, 1.3, 0])
        rows = fit_rows(VGroup(
            label(r"Bradley--Terry: \ $P(i \text{ beats } j) = g_i / (g_i + g_j)$", font_size=24),
            label(r"MM update: \ $g_i \leftarrow W_i \big/ \sum_j n_{ij} / (g_i + g_j)$", font_size=24, color=PATH),
            label(rf"log likelihood: \ {d['loglik'][0]:.1f} $\to$ {d['loglik'][1]:.1f} $\to$ {d['loglik'][2]:.1f} $\to \cdots \to$ {d['loglik'][-1]:.1f}", font_size=22, color=HIT),
            label(rf"$P$(Harbour beats Quarry) $= {d['P'][0][3]:.2f}$", font_size=22, color=TRUE),
            label(r"Zermelo (1929), \ for chess; \ Hunter (2004): \ it is MM", font_size=20, color=GREY_A),
        ), 12.0, 0.25, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Another MM classic ranks competitors from their head-to-head results. Here's a toy season "
            "among four of the World's town teams, each pair meeting ten times. The Bradley–Terry model gives each team a "
            "strength g, and says team i beats team j with probability g i over g i plus g j. <bookmark mark='b'/> The update "
            "has a lovely form: a team's new strength is its total wins divided by a sum over its opponents. "
            "<bookmark mark='c'/> The log likelihood rises at every step. <bookmark mark='d'/> At the end, Harbour is the "
            "strongest, and would beat Quarry eighty-seven percent of the time. <bookmark mark='e'/> Ernst Zermelo proposed "
            "exactly this iteration for chess tournaments in 1929; David Hunter showed in 2004 that it's an MM algorithm, which "
            "is why it always works."
        ) as vo:
            self.add(simulated_tag(r"a toy season"))
            vo.wait_until("a")
            self.play(FadeIn(t), FadeIn(rows[0]), run_time=2.0)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def verdict(self):
        rows = fit_rows(VGroup(
            label(r"MM: \ stable, \ monotone, \ no step sizes to tune", font_size=24, color=HIT),
            label(r"each step easy: \ a weighted mean, \ a least-squares fit, \ a closed form", font_size=24, color=PATH),
            label(r"convergence: \ linear, \ sometimes painfully slow", font_size=24, color=RES),
            label(r"remedies: \ acceleration (SQUAREM), \ or switch to Newton near the end", font_size=22, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So MM algorithms are stable and monotone, with no step size to choose. <bookmark mark='b'/> Each "
            "step is something simple, a weighted mean or a least-squares fit. <bookmark mark='c'/> The cost is speed: "
            "convergence is linear, and can be painfully slow when the surrogate is much more curved than the function. "
            "<bookmark mark='d'/> The standard fixes are extrapolation schemes like SQUAREM, or switching to Newton once close."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
