from __future__ import annotations

import numpy as np

from videos.stats.stats51.common import *  # noqa: F403


class Comparison(VoiceoverScene):
    def construct(self):
        self.card()
        self.slepian()
        self.chart()
        self.fernique()
        self.gordon()
        self.singular()
        self.cgmt()

    def cgmt(self):
        rows = [
            cmath(r"\text{compact sets, continuous }\psi\text{ convex--concave}", r":", r"\text{CGMT: tail bounds, probability factors }2", font_size=34),
            cmath(r"\Phi=\min_w \max_u \ u^\top G w + \psi(w, u)", r"\ \text{compared with}\ ", r"\min_w \max_u \ \|w\|g^\top u + \|u\|h^\top w + \psi", font_size=30),
            cmath(r"\text{the lasso, \ } p/n \to \delta", r":", r"\text{its exact risk, \ from a two-dimensional problem}", font_size=32),
            cmath(r"\text{the moral}", r":", r"\text{comparison gives not just bounds, \ but limits}", font_size=32),
        ]
        rows[1][-1].set_color(GAUSSC)
        rows[2][-1].set_color(MATC)
        whys = [why(r"Stojnic (2013)"), why(r"Thrampoulidis, \ Oymak \& Hassibi (2015)"), why(r"Part 59"), why(r"proportional asymptotics")]
        heading = label('Compact convex--concave problems admit Gaussian tail comparison', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A modern sharpening. Mihailo Stojnic noticed in 2013 that under compactness, continuity and convex-concave structure, Gaussian min-max comparison controls both tails, with probability factors of two. It is not equality of the two random problems. <bookmark mark='b'/> Christos Thrampoulidis, Samet Oymak and Babak Hassibi turned this into the convex Gaussian min-max theorem of 2015: a min-max involving a Gaussian matrix behaves like the much simpler one built from two Gaussian vectors. <bookmark mark='c'/> Since the lasso and many other estimators are such min-max problems, their exact risk, when p and n grow in proportion, can be read off from a problem in two scalar variables. <bookmark mark='d'/> Comparison inequalities give not just bounds but exact limits, which is the subject of Part fifty-nine."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def card(self):
        card = chapter_card(7, r"Gaussian comparison", r"Less correlated means a larger maximum", lit=(1962, 1985), part=PART)
        with self.voiceover("Chapter seven. Gaussian comparison: less correlated means a larger maximum."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def slepian(self):
        rows = [
            cmath(r"X, Y \text{ centred Gaussian in } \mathbb R^N", r":", r"E X_i^2 = E Y_i^2 \text{ for every } i", font_size=32),
            cmath(r"E X_i X_j \le E Y_i Y_j \text{ for all } i \ne j", r"\Rightarrow", r"P(\max X \ge t) \ge P(\max Y \ge t)", font_size=32),
            cmath(r"\text{so}", r":", r"E\max_i X_i \ge E\max_i Y_i", font_size=34),
            cmath(r"\text{proof}", r":", r"\text{interpolate } \sqrt{u}\,X + \sqrt{1-u}\,Y; \ \text{differentiate in } u", font_size=32),
        ]
        rows[1][-1].set_color(GAUSSC)
        rows[2][-1].set_color(GAUSSC)
        whys = [why(r"equal variances"), why(r"Slepian's lemma (1962)"), why(r"integrate the tails"), why(r"Gaussian integration by parts")]
        heading = label('Equal Gaussian variances and covariance order compare maximum tails', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> David Slepian, at Bell Labs in 1962, asked how the correlations of Gaussian variables affect "
            "their maximum. Take two centred Gaussian vectors with the same variances. <bookmark mark='b'/> If every pairwise "
            "correlation of X is at most the corresponding correlation of Y, then X's maximum is stochastically larger: it "
            "exceeds every threshold with at least as much probability. <bookmark mark='c'/> In particular its expected maximum "
            "is at least as large. <bookmark mark='d'/> The proof interpolates between the two vectors and differentiates; "
            "Gaussian integration by parts turns the derivative into a sum of covariance differences, each with a known sign."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("compare")
        rho = np.asarray(d["rhos"])
        A = axes([0, 1.02], [0, 3.6], x_length=7.4, y_length=4.4, xlabel=r"common correlation $\rho$", ylabel=r"$E\max$ of 1,000 standard normals",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 1, 2, 3], center=[-2.5, 0.2, 0])
        ax = A.ax
        u = np.linspace(0, 1, 120)
        th = polyline(ax, u, np.sqrt(1 - u) * d["emax"], EXACTC, 3)
        sim = VGroup(*[Dot(ax.c2p(a, b), radius=0.1, color=GAUSSC) for a, b in zip(rho, d["sim"])])
        sud = DashedLine(ax.c2p(0, d["sudakov"]), ax.c2p(1.02, d["sudakov"]), color=BNDC, stroke_width=2.5)
        i5 = list(d["rhos"]).index(0.5)
        side = fit_rows(VGroup(
            label(r"$X_i = \sqrt{1-\rho}\, Z_i + \sqrt\rho\, W$, \ $i \le 1{,}000$", font_size=22),
            label(rf"$\rho = 0$: \ independent, \ $E\max = {d['emax']:.3f}$", font_size=22, color=GAUSSC),
            label(r"white: \ $\sqrt{1-\rho}\; E\max$, \ exact; \ blue: \ simulated", font_size=22, color=EXACTC),
            label(rf"$\rho = 1/2$: \ {d['sim'][i5]:.2f}, \ \ Sudakov's bound (purple)", font_size=22, color=BNDC),
            label(r"more correlation, \ smaller maximum: \ Slepian", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A thousand standard normals sharing a common correlation rho, built from independent ones "
            f"plus a shared component. <bookmark mark='b'/> Independent, their expected maximum is {say(d['emax'], 2)}. "
            f"<bookmark mark='c'/> The shared component adds nothing to the maximum on average, so the expected maximum is the "
            f"root of one minus rho times the independent value: the white curve, matched by simulation. <bookmark mark='d'/> "
            f"At correlation one half, two variables are exactly one unit apart in the canonical metric, so this is the case "
            f"of Sudakov's bound, which the purple line shows is attained: {say(d['sim'][i5], 2)}. <bookmark mark='e'/> "
            f"Slepian's lemma in one picture: as the correlation rises, the maximum falls, all the way to a single normal's "
            f"mean of zero."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ curve exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(sim[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(th), FadeIn(VGroup(*sim[1:])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(sud), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def fernique(self):
        rows = [
            cmath(r"E(X_i - X_j)^2", r"\ge", r"E(Y_i - Y_j)^2 \ \text{ for all } i, j", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"E\max_i X_i \ge E\max_i Y_i: \ \text{no equal variances needed}", font_size=34),
            cmath(r"\text{Sudakov's minoration}", r":", r"\varepsilon\text{-separated } \Rightarrow \text{ compare with i.i.d. } N(0, \varepsilon^2/2)", font_size=30),
            cmath(r"\text{contraction}", r":", r"E\sup_t \langle g, \varphi(t)\rangle \le E\sup_t \langle g, t\rangle \text{ for 1-Lipschitz } \varphi", font_size=30),
        ]
        rows[1][-1].set_color(GAUSSC)
        whys = [why(r"larger increments"), why(r"Sudakov--Fernique (1971, 1975)"), why(r"chapter 6's lower bound"), why(r"a corollary")]
        heading = label('Increment order alone compares expected Gaussian maxima', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Sudakov and Fernique removed the condition of equal variances. If every increment of X is at least as large as the corresponding increment of Y, <bookmark mark='b'/> then X's expected maximum is at least Y's. Only distances matter, which is why the supremum is a property of the canonical metric. <bookmark mark='c'/> Sudakov's minoration follows at once: on an epsilon-separated set, the increments are at least those of independent normals with variance epsilon squared over two. <bookmark mark='d'/> So does a contraction principle: a one-Lipschitz map between Euclidean index sets can only shrink the Gaussian expected supremum. Rademacher contraction is a separate theorem with its own conditions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gordon(self):
        rows = [
            cmath(r"u\in S^{p-1},\ v\in S^{n-1},\ G_{ij}\stackrel{\rm iid}{\sim}N(0,1)", r":", r"\min_{u} \max_{v} X_{uv} \ \ \text{for doubly indexed processes}", font_size=34),
            cmath(r"X_{uv} = \langle Gu, v\rangle", r",", r"\ Y_{uv} = \langle g, u\rangle + \langle h, v\rangle", font_size=34),
            cmath(r"E\min_u\max_v X_{uv}", r"\ge", r"E\min_u\max_v Y_{uv}: \ \text{Gordon (1985)}", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"E\, s_{\min}(G) \ge \sqrt n - \sqrt p, \ \ E\, s_{\max}(G) \le \sqrt n + \sqrt p", font_size=34),
        ]
        rows[2][-1].set_color(GAUSSC)
        rows[3][-1].set_color(MATC)
        whys = [why(r"the smallest singular value is one"), why(r"a matrix vs \ two vectors"), why(r"increments compared"), why(r"chapter 4's white curves")]
        heading = label('Unit-sphere min--max comparison bounds expected singular values', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Yehoram Gordon extended the comparison in 1985 to min-max quantities, minimum over one index of a maximum over another. The smallest singular value of a matrix is such a quantity. <bookmark mark='b'/> Compare u transpose G v, for an n by p standard Gaussian matrix G, u on the p-dimensional unit sphere and v on the n-dimensional unit sphere, with the much simpler process built from two independent Gaussian vectors. <bookmark mark='c'/> Their increments satisfy Gordon's conditions, so the min-max of the first is at least that of the second. <bookmark mark='d'/> Evaluating the simple one gives the expected smallest singular value at least root n minus root p, and Slepian gives the largest at most root n plus root p: chapter four's white curves, exact bounds at every n and p."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def singular(self):
        d = load("matrices")
        rows = [[r"$p$ \ ($n = 400$)"] + [str(r["p"]) for r in d["rows"]],
                [r"$\sqrt n + \sqrt p$"] + [f"{r['gordon_max']:.2f}" for r in d["rows"]],
                [r"$E\, s_{\max}$, \ simulated"] + [f"{r['max']:.2f}" for r in d["rows"]],
                [r"$E\, s_{\min}$, \ simulated"] + [f"{r['min']:.2f}" for r in d["rows"]],
                [r"$\sqrt n - \sqrt p$"] + [f"{r['gordon_min']:.2f}" for r in d["rows"]]]
        tab = table_rows(rows, font_size=26, col_buff=0.5, row_buff=0.36, colors=[GREY_B, EXACTC, MATC, SPHC, EXACTC])
        if tab.width > 12.8:
            tab.width = 12.8
        tab.move_to([0, 0.9, 0])
        foot = label(r"every simulated largest value under Gordon's ceiling, \ every smallest above his floor", font_size=24, color=GOODC).move_to([0, -1.5, 0])
        foot2 = label(r"and with Gaussian concentration (chapter 3), \ each is within $O(1)$ of its mean", font_size=24, color=GREY_A).move_to([0, -2.3, 0])
        r = d["rows"]
        with self.voiceover(
            f"<bookmark mark='a'/> The numbers behind chapter four's picture. For every number of columns, the simulated "
            f"largest singular value lies below root n plus root p, and the smallest above root n minus root p: at four hundred "
            f"columns, the floor is zero, and the simulated smallest is {say(r[-1]['min'], 1)}. <bookmark mark='b'/> Gordon's "
            f"bounds hold for the expectation. <bookmark mark='c'/> The singular values are one-Lipschitz functions of the "
            f"matrix's entries, so chapter three's concentration puts each within a constant of its mean, with Gaussian tails."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated; \ bounds exact")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()
