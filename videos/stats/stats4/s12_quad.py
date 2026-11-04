from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


class Quad(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.simulate()
        self.cochran()
        self.noncentral()
        self.independence()
        self.student()

    def card(self):
        card = chapter_card(11, r"Quadratic forms in normal vectors", r"When is $\mathbf z^\top A \mathbf z$ chi-squared?",
                            lit=(1876,), part=PART)
        with self.voiceover("Chapter eleven. Quadratic forms in normal vectors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\mathbf z^\top P\mathbf z", r"=", r"\mathbf z^\top Q\Lambda Q^\top \mathbf z", r"=", r"\mathbf w^\top \Lambda \mathbf w",
                  font_size=34),
            cmath(r"\mathbf w", r"=", r"Q^\top \mathbf z \sim N(\mathbf 0, I)", font_size=34),
            cmath(r"\mathbf z^\top P\mathbf z", r"=", r"\sum_{k : \lambda_k = 1} w_k^2", r"\sim", r"\chi^2_{\operatorname{rank} P}",
                  font_size=36),
        ]
        rows[2][4].set_color(EXACT)
        whys = [why(r"spectral theorem"), why(r"rotating a standard normal leaves it standard normal"),
                why(r"eigenvalues $0$ and $1$")]
        th = theorem_card(r"$\chi^2$ quadratic forms", r"for $\mathbf z \sim N(\mathbf 0, I)$ and symmetric $A$: \ "
                          r"$\mathbf z^\top A\mathbf z \sim \chi^2_r$ \ iff $A$ is a projection of rank $r$", color=EXACT,
                          width=7.4, font_size=24).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here the hook's eigenvalues pay off completely. <bookmark mark='a'/> Take a standard normal vector z "
            "and a projection P, and diagonalize P. <bookmark mark='b'/> Rotating a standard normal vector gives "
            "another standard normal vector: Herschel's rotation invariance from Part 3. <bookmark mark='c'/> So z "
            "transpose P z is a sum of squared independent standard normals, one for each eigenvalue equal to one: "
            "chi-squared, with degrees of freedom equal to the rank. <bookmark mark='d'/> And the converse holds: "
            "a quadratic form in a standard normal vector is chi-squared only if its matrix is a projection."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.55, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(th, shift=UP * 0.2))
        self.clear_scene()

    def simulate(self):
        d = load("quad")
        xs = np.asarray(d["xs"])
        q1, q2 = np.asarray(d["q1"]), np.asarray(d["q2"])
        n, p = d["n"], d["p"]
        A = axes([0, 25], [0, 0.27], x_length=8.4, y_length=4.2, xlabel=r"value of the quadratic form",
                 xticks=[0, 5, 10, 15, 20, 25], yticks=[0, 0.1, 0.2], center=[-1.6, -0.6, 0])
        ax = A.ax
        ed = np.linspace(0, 25, 51)
        h1 = hist_bars(ax, ed, np.histogram(q1, ed)[0] / (len(q1) * np.diff(ed)), color=FIT, opacity=0.5)
        h2 = hist_bars(ax, ed, np.histogram(q2, ed)[0] / (len(q2) * np.diff(ed)), color=RES, opacity=0.5)
        c1 = curve(ax, xs, np.clip(np.asarray(d["chi_p"]), 0, 0.27), EXACT, 3)
        c2 = curve(ax, xs, np.clip(np.asarray(d["chi_np"]), 0, 0.27), EXACT, 3)
        info = VGroup(MathTex(rf"\mathbf z^\top H\mathbf z:\ \ \text{{mean }} {d['q1_mean']:.2f} \ \ (\chi^2_{p})", font_size=28,
                              color=FIT),
                      MathTex(rf"\mathbf z^\top (I - H)\mathbf z:\ \ \text{{mean }} {d['q2_mean']:.2f} \ \ (\chi^2_{{{n - p}}})",
                              font_size=28, color=RES),
                      MathTex(rf"\text{{correlation between them: }} {d['corr']:.3f}", font_size=26, color=GREY_A))
        info.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, 2.3, 0])
        tag = note(rf"simulated: 20,000 standard normal vectors, \ $n = {n}$, \ $p = {p}$").to_corner(DR, buff=0.3)
        with self.voiceover(
            f"Check it. <bookmark mark='a'/> Take a hat matrix for n equal to {n} and p equal to {p}, and twenty "
            "thousand standard normal vectors. <bookmark mark='b'/> z transpose H z, blue, falls on the chi-squared "
            f"with {p} degrees of freedom, <bookmark mark='c'/> and z transpose I minus H z, red, on the chi-squared "
            f"with {n - p}. <bookmark mark='d'/> And the two are uncorrelated, in fact independent, because they're "
            "built from different coordinates of the rotated vector: the fitted part and the residual part never "
            "share a direction."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(h1), Create(c1), FadeIn(info[0]))
            vo.wait_until("c")
            self.play(FadeIn(h2), Create(c2), FadeIn(info[1]))
            vo.wait_until("d")
            self.play(FadeIn(info[2]))
        self.clear_scene()

    def cochran(self):
        th = theorem_card(r"Cochran's theorem (1934), \ first look", r"if $I = P_1 + \cdots + P_k$ with projections of ranks "
                          r"$r_1 + \cdots + r_k = n$, \ then the $\mathbf z^\top P_j \mathbf z$ are independent $\chi^2_{r_j}$",
                          color=EXACT, width=8.4, font_size=24).move_to([0, 1.2, 0])
        uses = VGroup(label(r"Part 8: \ $\bar x$ and $s^2$ are independent; \ $(n-1)s^2/\sigma^2 \sim \chi^2_{n-1}$", font_size=26),
                      label(r"Part 12: \ the $t$ and $F$ tests of regression", font_size=26),
                      label(r"Part 13: \ the analysis of variance", font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        uses.next_to(th, DOWN, buff=0.5)
        with self.voiceover(
            "That observation generalizes into one of the central theorems of classical statistics. "
            "<bookmark mark='a'/> If the identity splits into projections onto mutually perpendicular subspaces, "
            "the corresponding pieces of the squared length of a standard normal vector are independent "
            "chi-squareds, with the ranks as degrees of freedom. It's William Cochran's theorem, from 1934. "
            "<bookmark mark='b'/> In Part 8 it gives the independence of the sample mean and variance and the "
            "chi-squared law of the variance; in Part 12, the t and F tests of regression; in Part 13, the whole "
            "analysis of variance."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(u, shift=RIGHT * 0.2) for u in uses], lag_ratio=0.4))
        self.clear_scene()

    def noncentral(self):
        e = load("extras")
        nc = e["ncx2"]
        xs = np.asarray(e["ncx2_xs"])
        A = axes([0, 40], [0, 0.13], x_length=8.2, y_length=4.0, xlabel=r"$\|(I - H)(\mathbf z + \boldsymbol\mu)\|^2$",
                 xticks=[0, 10, 20, 30, 40], yticks=[0, 0.05, 0.1], center=[-1.8, -0.8, 0])
        ax = A.ax
        cols = {"0.0": GREY_A, "2.0": S.ACCENT, "4.0": RES}
        cvs = VGroup(*[curve(ax, xs, np.clip(np.asarray(e["ncx2_pdf"][k]), 0, 0.13), c, 3) for k, c in cols.items()])
        crit = DashedLine(ax.c2p(14.07, 0), ax.c2p(14.07, 0.13), color=EXACT, stroke_width=2)
        cl = label(r"95\% point of $\chi^2_7$", font_size=20, color=EXACT).next_to(crit, UP, buff=0.05)
        f = MathTex(r"E\,\|P(\mathbf z + \boldsymbol\mu)\|^2 = r + \|P\boldsymbol\mu\|^2", font_size=30).to_edge(UP, buff=0.35)
        rows = VGroup(*[MathTex(rf"\|P\boldsymbol\mu\| = {float(k):.0f}:\ \ \text{{mean }} {v['mean']:.2f}\ ({v['theory']:.0f}),\ \ "
                                rf"\text{{beyond the line }} {100 * v['power']:.1f}\%", font_size=24, color=cols[k])
                        for k, v in nc.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.0, 1.6, 0])
        for r in rows:
            if r.width > 6.4:
                r.width = 6.4
        take = label(r"the noncentral $\chi^2$: \ how often a test notices a real effect \ (its power, \ Part 10)", font_size=24,
                     color=S.ACCENT).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "What if the normal vector isn't centred at zero? <bookmark mark='a'/> Shift it by mu. The quadratic "
            "form now averages its rank plus the squared length of the projected shift, and its distribution is the "
            "noncentral chi-squared. <bookmark mark='b'/> With no shift, grey, it's the ordinary chi-squared with "
            "seven degrees of freedom. <bookmark mark='c'/> A shift of length two, yellow, moves it right; a shift of "
            "length four, red, moves it far right. <bookmark mark='d'/> Draw the line that an ordinary chi-squared "
            f"exceeds only five percent of the time. The shifted versions exceed it {100 * nc['2.0']['power']:.0f} "
            f"and {100 * nc['4.0']['power']:.0f} percent of the time, in twenty thousand simulations each, matching "
            "the theory. That fraction is a test's power, the probability that it notices a real effect, and it's "
            "the subject of Part 10."
        ) as vo:
            self.play(FadeIn(A), Write(f))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(cvs[0]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(cvs[1]), Create(cvs[2]), FadeIn(rows[1:]))
            vo.wait_until("d")
            self.play(Create(crit), FadeIn(cl), FadeIn(take))
        self.clear_scene()

    def independence(self):
        e = load("extras2")["indep"]
        panels = VGroup()
        for k, (mk, vk, ttl, col, cc) in enumerate((("n_mean", "n_var", r"normal samples of 10", FIT, e["n_corr"]),
                                                     ("e_mean", "e_var", r"exponential samples of 10", RES, e["e_corr"]))):
            m_, v_ = np.asarray(e[mk]), np.asarray(e[vk])
            if k == 0:
                A = axes([-1.2, 1.2], [0, 3.0], x_length=4.6, y_length=3.6, xlabel=r"$\bar x$", ylabel=r"$s^2$",
                         xticks=[-1, 0, 1], yticks=[0, 1, 2, 3], center=[-3.4, -0.8, 0])
            else:
                A = axes([0, 2.5], [0, 5.0], x_length=4.6, y_length=3.6, xlabel=r"$\bar x$", ylabel=r"$s^2$",
                         xticks=[0, 1, 2], yticks=[0, 2, 4], center=[3.4, -0.8, 0])
            ax = A.ax
            lo, hi, ylo, yhi = bounds(ax)
            pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.018, color=col, fill_opacity=0.6) for a, b in zip(m_[:1500], v_[:1500])
                           if lo < a < hi and ylo < b < yhi])
            t = label(ttl, font_size=24, color=col).next_to(A, UP, buff=0.15)
            c = MathTex(rf"\operatorname{{corr}} = {cc:.3f}", font_size=26, color=col).next_to(t, DOWN, buff=0.08)
            panels.add(VGroup(A, pts, t, c))
        head = label(r"$\bar x$ lives in $P_{\mathbf 1}$, \ $s^2$ in $I - P_{\mathbf 1}$: \ independent \emph{only} for normal data",
                     font_size=26, color=S.ACCENT).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The perpendicular split has a striking consequence, and a striking limitation. <bookmark mark='a'/> The "
            "sample mean depends only on the projection onto the ones vector; the sample variance only on the "
            "perpendicular part. For normal data those parts are independent, so the mean and the variance are "
            "independent too. <bookmark mark='b'/> Twenty thousand normal samples of ten: the cloud of means and "
            "variances shows no relation at all. <bookmark mark='c'/> But the argument used rotation invariance, "
            "which only the normal has. For exponential data, the same plot shows a strong relation: samples with "
            "larger means have larger variances, a correlation of about point seven. The normal is the only "
            "distribution with this property, a theorem of Geary from 1936."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][2]), FadeIn(panels[0][1], lag_ratio=0.001), FadeIn(panels[0][3]))
            vo.wait_until("c")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][2]), FadeIn(panels[1][1], lag_ratio=0.001), FadeIn(panels[1][3]))
        self.clear_scene()

    def student(self):
        rows = [
            cmath(r"\sqrt n\,\frac{\bar x - \mu}{\sigma}", r"\sim", r"N(0, 1)", font_size=34),
            cmath(r"\frac{(n-1)s^2}{\sigma^2}", r"=", r"\frac{\|(I - P_{\mathbf 1})\mathbf x\|^2}{\sigma^2}", r"\sim", r"\chi^2_{n-1}",
                  font_size=32),
            cmath(r"T = \sqrt n\,\frac{\bar x - \mu}{s}", r"=", r"\frac{N(0, 1)}{\sqrt{\chi^2_{n-1}/(n-1)}}", r"\sim", r"t_{n-1}",
                  font_size=32),
        ]
        rows[2][4].set_color(EXACT)
        whys = [why(r"the projection onto $\mathbf 1$"), why(r"the projection off $\mathbf 1$: \ rank $n - 1$"),
                why(r"independent numerator and denominator: \ Part 3's $t$")]
        take = label(r"Student's 1908 result, \ in three lines of projections: \ Part 8 proves every step", font_size=26,
                     color=S.ACCENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Put the pieces together and Student's t falls out. <bookmark mark='a'/> For normal data, the sample "
            "mean, standardized with the true sigma, is standard normal: it lives in the projection onto the ones "
            "vector. <bookmark mark='b'/> The sample variance lives in the perpendicular projection, of rank n minus "
            "one, so scaled by sigma squared it's chi-squared with n minus one degrees of freedom. <bookmark mark='c'/> "
            "And the two are independent. So the mean standardized with the estimated s is a standard normal over "
            "the root of an independent chi-squared over its degrees of freedom: exactly Part 3's definition of t "
            "with n minus one degrees of freedom. Gosset's 1908 result, in three lines of projections."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.6, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            self.play(FadeIn(take))
        self.clear_scene()
