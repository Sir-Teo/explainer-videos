from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats22.common import *  # noqa: F403


def crab_axes(center=(-1.6, 0.2, 0), x_length=8.0, y_length=4.4):
    return axes([0.575, 0.70], [0, 110], x_length=x_length, y_length=y_length, xlabel=r"forehead breadth / body length",
                ylabel=r"crabs", xticks=[0.58, 0.60, 0.62, 0.64, 0.66, 0.68, 0.70], yticks=[0, 25, 50, 75, 100],
                center=list(center))


def crab_bars(ax, x, w, color=None):
    g = VGroup()
    wd = ax.c2p(0.0038, 0)[0] - ax.c2p(0, 0)[0]
    for a, c in zip(x, w):
        h = max(0.01, ax.c2p(0, c)[1] - ax.c2p(0, 0)[1])
        g.add(Rectangle(width=wd, height=h, stroke_width=0, fill_color=color or GREY_B, fill_opacity=0.75).move_to(ax.c2p(a, 0), aligned_edge=DOWN))
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.weldon()
        self.histogram()
        self.nonic()
        self.solutions()
        self.likelihood_way()
        self.objectives()

    def weldon(self):
        tl = timeline(lit=(1894, 1922)).to_edge(UP, buff=0.35)
        hc = history_card(1893, r"W. F. R. Weldon, \ Naples",
                          r"measures 1,000 shore crabs from the Bay of Naples: \ among other things, \ the breadth of the "
                          r"``forehead'' as a fraction of body length. \ The histogram is lopsided. \ Two races of crab, \ "
                          r"perhaps, \ one evolving away from the other?",
                          color=CRAB2, width=11.0, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"he asks Karl Pearson: \ is this two normal curves added together?", font_size=24),
            label(r"five unknowns: \ the mix, \ two means, \ two spreads", font_size=24, color=GREY_A),
        ), 12.0, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1893 the zoologist Raphael Weldon measured a thousand shore crabs from the Bay of Naples. "
            "Among other things he recorded the breadth of each crab's forehead as a fraction of its body length. The "
            "histogram came out lopsided, and Weldon wondered whether he was looking at two races of crab mixed together, "
            "perhaps one evolving away from the other. <bookmark mark='b'/> He asked his friend Karl Pearson: is this the sum "
            "of two normal curves? <bookmark mark='c'/> That question has five unknowns: the share of each race, their two "
            "means, and their two spreads."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def histogram(self):
        d = load("crabs")
        x, w = np.asarray(d["x"]), np.asarray(d["w"])
        A = crab_axes()
        ax = A.ax
        bars = crab_bars(ax, x, w)
        mu, sd = d["one"]
        gr = np.asarray(d["grid"])
        one = curve(ax, gr, 1000 * 0.004 * stats.norm.pdf(gr, mu, sd), RES, 3)
        rows = fit_rows(VGroup(
            label(r"1,000 crabs, \ in 29 intervals of 0.004", font_size=22),
            label(rf"mean {mu:.4f}, \ SD {sd:.4f}", font_size=22),
            label(r"red: \ one normal curve with that mean and SD", font_size=22, color=RES),
            VGroup(label(r"too low on the left shoulder,", font_size=22, color=GREY_A),
                   label(r"too high on the right: \ skewed", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
        ), 3.45, 0.42, [5.1, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are Weldon's thousand crabs, in the twenty-nine intervals Pearson printed. "
            "<bookmark mark='b'/> Their mean ratio is point six four four seven. <bookmark mark='c'/> A single normal curve "
            "with the same mean and spread, in red, fits badly: <bookmark mark='d'/> the data have a long left shoulder and a "
            "steep right side. A single normal can't be skewed; a mixture of two can."
        ) as vo:
            self.add(crab_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(one), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def nonic(self):
        hc = history_card(1894, r"Karl Pearson, \ \emph{Phil. Trans.}",
                          r"match the mixture's first five moments to the data's: \ five equations, \ five unknowns. \ "
                          r"Eliminating four of them leaves a polynomial of degree nine \ (a ``nonic''), \ solved by hand",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"the method of moments, \ at its most heroic", font_size=24),
            label(r"the nonic had more than one usable root", font_size=24, color=RES),
            label(r"Pearson's tie-breaker: \ whichever matched the sixth moment better", font_size=24, color=GREY_A),
        ), 12.0, 0.35, [0, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Pearson's answer, published in 1894, was the method of moments at its most heroic. He wrote "
            "the mixture's mean and its second to fifth central moments in terms of the five unknowns, and set them equal to "
            "the data's. Eliminating four unknowns left a single polynomial of the ninth degree, which he solved by hand. "
            "<bookmark mark='b'/> It had more than one root that made sense. <bookmark mark='c'/> To choose, he computed the "
            "sixth moment of each candidate and kept the one closer to the data's."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(rows[0]))
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def solutions(self):
        d = load("crabs")
        sols = d["pearson"]
        hdr = [r"\textbf{solution}", r"$p$", r"$\mu_1$", r"$\sigma_1$", r"$\mu_2$", r"$\sigma_2$", r"\textbf{sixth moment}"]
        body = []
        for k, s_ in enumerate(sols):
            body.append([rf"moments {chr(65 + k)}", f"{s_[0]:.3f}", f"{s_[1]:.4f}", f"{s_[2]:.4f}", f"{s_[3]:.4f}", f"{s_[4]:.4f}",
                         rf"{d['sixth'][k] * 1e10:.2f}"])
        body.append([r"the data", "", "", "", "", "", rf"{d['sixth_data'] * 1e10:.2f}"])
        t = table_rows([hdr] + body, font_size=24, col_buff=0.55, row_buff=0.3, colors=[GREY_A, None, None, TRUE])
        t.move_to([0, 0.6, 0])
        best = int(np.argmin([abs(v - d["sixth_data"]) for v in d["sixth"]]))
        foot = fit_rows(VGroup(
            label(r"sixth moments in units of $10^{-10}$", font_size=20, color=GREY_B),
            label(rf"moments {chr(65 + best)} is closer: \ Pearson's kind of choice", font_size=24, color=PATH),
            label(r"but why moments at all? \ and how sure are these numbers?", font_size=24, color=RES),
        ), 12.0, 0.3, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Solving Pearson's five equations numerically, from hundreds of starting points, finds exactly "
            "two admissible solutions, both with two components close together. <bookmark mark='b'/> Their sixth moments differ, "
            "and solution B is the closer to the data's. <bookmark mark='c'/> But this raises the questions of this part. Why "
            "should matching moments give good estimates at all? Which method is best? And how sure can we be of numbers "
            "like these?"
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(t[0]), FadeIn(t[1]), FadeIn(t[2]), FadeIn(t[3]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(Indicate(t[1 + best], color=PATH), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def likelihood_way(self):
        d = load("crabs")
        x, w = np.asarray(d["x"]), np.asarray(d["w"])
        A = crab_axes()
        ax = A.ax
        bars = crab_bars(ax, x, w)
        gr = np.asarray(d["grid"])
        s = 1000 * 0.004
        c1 = curve(ax, gr, s * np.asarray(d["comp1"]), CRAB1, 2.5)
        c2 = curve(ax, gr, s * np.asarray(d["comp2"]), CRAB2, 2.5)
        tot = curve(ax, gr, s * np.asarray(d["dens"]), PATH, 3.5)
        th = d["theta"]
        rows = fit_rows(VGroup(
            label(r"maximum likelihood, \ by EM (chapter 8)", font_size=22, color=PATH),
            label(rf"blue: \ {100 * th[0]:.0f}\% at {th[1]:.4f}, \ SD {th[2]:.4f}", font_size=22, color=CRAB1),
            label(rf"red: \ {100 * (1 - th[0]):.0f}\% at {th[3]:.4f}, \ SD {th[4]:.4f}", font_size=22, color=CRAB2),
            VGroup(label(rf"log likelihood \ {d['loglik'][-1]:.2f}", font_size=22, color=PATH),
                   label(rf"moments B \ {d['ll_pearson'][1]:.2f}; \ one normal \ {d['ll_one']:.2f}", font_size=20)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            label(r"Fisher (1922): \ why this is the efficient answer", font_size=20, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fisher's alternative, from 1922, is maximum likelihood: choose the five numbers that make the "
            "observed crabs most probable. Here it is, computed by the EM algorithm of chapter eight. <bookmark mark='b'/> "
            "Forty-three percent of the crabs in a broader component centred at point six three two, <bookmark mark='c'/> the "
            "rest in a narrower one at point six five five. <bookmark mark='d'/> Its log likelihood beats both of Pearson's "
            "solutions, and beats a single normal by twenty-seven units. <bookmark mark='e'/> This part explains why maximum "
            "likelihood works, how to measure its uncertainty, how to compute it, and what happens when the model itself is "
            "wrong."
        ) as vo:
            self.add(crab_tag())
            self.play(FadeIn(A), FadeIn(bars))
            vo.wait_until("a")
            self.play(Create(tot), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 22", font_size=34, color=GREY_B), label(r"Likelihood in Depth", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"why the MLE is consistent and asymptotically normal: \ the proofs",
            r"observed vs expected information; \ many parameters and the profile likelihood",
            r"Wald, \ score and likelihood-ratio tests; \ Neyman--Scott",
            r"the EM algorithm, \ and where likelihood misbehaves",
            r"misspecification and the sandwich; \ quasi- and pseudo-likelihood; \ the likelihood principle",
        ], color=LIK, font_size=26)
        prereq = note(r"prerequisites: \ Parts 9, \ 10 and 21").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.mle}; \ the likelihood landscape").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part twenty-two: likelihood in depth. <bookmark mark='b'/> We'll prove the two properties Part "
            "9 promised; separate observed from expected information; handle many parameters with the profile likelihood; "
            "compare the three classical tests; meet a problem where maximum likelihood fails; derive the EM algorithm and "
            "refit the crabs; see where likelihood misbehaves; derive the sandwich for wrong models; meet quasi- and "
            "pseudo-likelihood; argue about the likelihood principle; and glimpse the geometry of information."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
