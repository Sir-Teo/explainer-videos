from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class Gaps(VoiceoverScene):
    def construct(self):
        self.card()
        self.clique()
        self.chart()
        self.spca()
        self.lasso()
        self.practice()
        self.lowdegree()

    def card(self):
        card = chapter_card(9, r"Statistical--computational gaps", r"Possible in principle, \ out of reach in practice?", lit=(2013,), part=PART)
        with self.voiceover("Chapter nine. Statistical–computational gaps: possible in principle, out of reach in practice?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def clique(self):
        d = load("clique")
        rows = [
            cmath(r"G(n, \tfrac12) \ \text{vs.\ } G(n, \tfrac12) + \text{a clique on } k \text{ vertices}", r":", r"\text{planted clique}", font_size=30),
            cmath(r"\text{information-theoretically}", r":", rf"k > 2\log_2 n \approx {d['log_n']:.0f}: \ \text{{search all }} k\text{{-sets}}", font_size=30),
            cmath(r"\text{in polynomial time}", r":", rf"k \gtrsim \sqrt n = {d['sqrt_n']:.0f}: \ \text{{degrees, \ spectra}}", font_size=32),
            cmath(r"2\log_2 n \ll k \ll \sqrt n", r":", r"\text{no efficient method known, \ after 30 years}", font_size=32),
        ]
        rows[1][-1].set_color(UPC)
        rows[2][-1].set_color(ADAPTC)
        rows[3][-1].set_color(LOWC)
        whys = [why(r"Jerrum (1992); \ Kučera (1995)"), why(r"exponential-time search"), why(r"Alon, \ Krivelevich \& Sudakov (1998)"), why(r"the conjectured hard regime")]
        with self.voiceover(
            f"<bookmark mark='a'/> The minimax theory so far asks what is possible with unlimited computation. A random graph "
            f"in which each edge is present with probability one half, against the same graph with a clique of k vertices "
            f"planted in it. <bookmark mark='b'/> Information-theoretically, a clique larger than about twice log base two of "
            f"n can be detected: search every set of k vertices. For n of four hundred that is about {d['log_n']:.0f}. "
            f"<bookmark mark='c'/> But the best polynomial-time methods, counting degrees or using the top eigenvector, need "
            f"k of order root n, here twenty. <bookmark mark='d'/> In between, detection is possible in principle and no "
            f"efficient algorithm is known, after thirty years of trying."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("clique")
        ks = np.asarray([r["k"] for r in d["rows"]], float)
        pw = np.asarray([r["power"] for r in d["rows"]])
        A = axes([0, 85], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"clique size $k$", ylabel=r"power of the edge-count test",
                 xticks=[0, 20, 40, 60, 80], yticks=[0, 0.05, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        c = VGroup(polyline(ax, ks, pw, ADAPTC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=ADAPTC) for a, b in zip(ks, pw)])
        it = DashedLine(ax.c2p(d["log_n"], 0), ax.c2p(d["log_n"], 1.05), color=UPC, stroke_width=2.5)
        sq = DashedLine(ax.c2p(d["sqrt_n"], 0), ax.c2p(d["sqrt_n"], 1.05), color=HYPC, stroke_width=2.5)
        band = Rectangle(width=ax.c2p(d["sqrt_n"], 0)[0] - ax.c2p(d["log_n"], 0)[0], height=ax.c2p(0, 1.05)[1] - ax.c2p(0, 0)[1],
                         fill_color=LOWC, fill_opacity=0.12, stroke_width=0).move_to(ax.c2p((d["log_n"] + d["sqrt_n"]) / 2, 0.525))
        side = fit_rows(VGroup(
            label(rf"$n = {d['n']}$ vertices, \ 150 graphs per $k$", font_size=22),
            label(r"green: \ the total-edge test, \ polynomial time", font_size=22, color=ADAPTC),
            label(rf"blue: \ $2\log_2 n \approx {d['log_n']:.0f}$: \ possible in principle", font_size=22, color=UPC),
            label(rf"gold: \ $\sqrt n = {d['sqrt_n']:.0f}$", font_size=22, color=HYPC),
            label(r"red band: \ detectable, \ but not by any known fast test", font_size=22, color=LOWC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Simulated, with four hundred vertices. <bookmark mark='b'/> The simplest efficient test "
            f"counts edges. Its power is near five percent for small cliques and climbs past a half only when the clique is a "
            f"good deal larger than root n. <bookmark mark='c'/> Exhaustive search would succeed from about {d['log_n']:.0f} "
            f"vertices, <bookmark mark='d'/> but polynomial-time methods need about root n. <bookmark mark='e'/> The red band "
            f"is the gap: problems that are statistically solvable but, as far as anyone knows, computationally out of reach."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(it), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(sq), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(band), FadeIn(side[4]))
        self.clear_scene()

    def spca(self):
        rows = [
            cmath(r"\Sigma = I_p + \lambda\, vv^\top, \ \|v\|_0 = k", r":", r"\text{sparse PCA: \ detect or estimate } v", font_size=32),
            cmath(r"\text{statistically}", r":", r"n \gtrsim k \log p / \lambda^2", font_size=34),
            cmath(r"\text{efficient methods}", r":", r"n \gtrsim k^2 \log p / \lambda^2: \ \text{a factor } k \text{ more data}", font_size=32),
            cmath(r"\text{Berthet \& Rigollet (2013)}", r":", r"\text{a fast method for the gap would detect planted cliques}", font_size=30),
        ]
        rows[1][-1].set_color(UPC)
        rows[2][-1].set_color(ADAPTC)
        rows[3][-1].set_color(LOWC)
        whys = [why(r"a spiked covariance"), why(r"exhaustive search over supports"), why(r"semidefinite relaxations"), why(r"a reduction")]
        with self.voiceover(
            "<bookmark mark='a'/> The gap reaches statistics proper. In sparse principal components, a covariance matrix has "
            "one spike in a direction with only k non-zero coordinates. <bookmark mark='b'/> Statistically, about k log p "
            "over lambda squared observations suffice, by searching over supports. <bookmark mark='c'/> Every known "
            "efficient method, including semidefinite relaxations, needs about k squared log p: a factor of k more data. "
            "<bookmark mark='d'/> Quentin Berthet and Philippe Rigollet showed in 2013 that a fast method working in the gap "
            "would give a fast method for planted clique. The gap is inherited, by reduction, from a problem believed hard."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lasso(self):
        rows = [
            cmath(r"\text{sparse regression}, \ y = X\beta + z", r":", r"\text{minimax: \ } s\log(p/s)/n, \ \text{best subset attains it}", font_size=30),
            cmath(r"\text{best subset}", r":", r"\binom ps \text{ fits: \ exponential time}", font_size=34),
            cmath(r"\text{the lasso}", r":", r"\text{the same rate, \ in polynomial time, \ \emph{if} } X \text{ is well conditioned}", font_size=30),
            cmath(r"\text{badly conditioned } X", r":", r"\text{evidence of a gap: \ Zhang, \ Wainwright \& Jordan (2014)}", font_size=30),
        ]
        rows[2][-1].set_color(ADAPTC)
        rows[3][-1].set_color(LOWC)
        whys = [why(r"Fano's rate, \ chapter 4"), why(r"Part 28's search"), why(r"Part 52's restricted eigenvalues"), why(r"the gap reaches regression")]
        with self.voiceover(
            "<bookmark mark='a'/> Gaps appear even in regression. With a sparse coefficient vector, the minimax prediction "
            "rate is Fano's s log p over s, divided by n, and best-subset selection attains it. <bookmark mark='b'/> But best "
            "subset must search p choose s models, which takes exponential time. <bookmark mark='c'/> The lasso attains the "
            "same rate in polynomial time, provided the design is well conditioned on sparse vectors, a condition Part "
            "fifty-two calls restricted eigenvalues. <bookmark mark='d'/> When the design is badly conditioned, Yuchen Zhang, "
            "Martin Wainwright and Michael Jordan found evidence in 2014 that no polynomial-time method can match best subset. "
            "Computation, not just information, can set the rate."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def practice(self):
        rows = fit_rows(VGroup(
            label(r"for the working statistician:", font_size=28, color=GREY_A),
            label(r"a minimax rate is a promise about the best method, \ not about the one you can run", font_size=26, color=UPC),
            label(r"when the efficient methods need more data, \ the computational rate is the honest planning number", font_size=26, color=ADAPTC),
            label(r"convex relaxations (the lasso, \ SDPs) \ often sit exactly at the computational limit", font_size=26, color=HYPC),
            label(r"a method that claims the statistical limit in the gap is probably wrong, \ or exponential", font_size=26, color=LOWC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What this means in practice. <bookmark mark='b'/> A minimax rate promises what the best "
            "method could do, not what the method you can actually run will do. <bookmark mark='c'/> When the efficient "
            "methods need more data, as in sparse principal components, the computational rate is the honest number for "
            "planning a study. <bookmark mark='d'/> Convex relaxations, like the lasso and semidefinite programs, often sit "
            "exactly at the computational limit, which is one reason they are so widely used. <bookmark mark='e'/> And a fast "
            "method that claims to reach the statistical limit inside a conjectured gap deserves suspicion: it is probably "
            "wrong, or secretly exponential."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lowdegree(self):
        rows = fit_rows(VGroup(
            label(r"evidence for hardness, \ short of a proof:", font_size=28, color=GREY_A),
            label(r"reductions from planted clique \ (Berthet \& Rigollet 2013; \ Brennan \& Bresler 2020)", font_size=26, color=LOWC),
            label(r"low-degree polynomials: \ if no polynomial of degree $\log n$ can tell the two apart, \ assume nothing fast can", font_size=26, color=HYPC),
            label(r"\ (Hopkins 2018); \ sum-of-squares and statistical-query lower bounds", font_size=26, color=HYPC),
            label(r"the new question: \ the best rate \emph{for an efficient estimator}", font_size=26, color=ADAPTC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Proving that no polynomial-time algorithm exists would separate P from NP, so the field "
            "collects evidence instead. <bookmark mark='b'/> Reductions from planted clique, by Berthet and Rigollet and later "
            "by Matthew Brennan and Guy Bresler, transfer its presumed hardness to many problems. <bookmark mark='c'/> The "
            "low-degree method, developed by Samuel Hopkins in 2018, asks whether any polynomial of degree about log n in the "
            "data can tell the hypotheses apart; when none can, it predicts that no efficient test can either. <bookmark "
            "mark='d'/> Sum-of-squares and statistical-query bounds tell the same story. <bookmark mark='e'/> And so minimax "
            "theory has a new question alongside the old one: not only how well can anyone estimate, but how well can anyone "
            "estimate quickly."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
