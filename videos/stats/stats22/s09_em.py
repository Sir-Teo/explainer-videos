from __future__ import annotations

import numpy as np

from videos.stats.stats22.common import *  # noqa: F403
from videos.stats.stats22.s01_hook import crab_axes


class EM(VoiceoverScene):
    def construct(self):
        self.card()
        self.missing()
        self.steps()
        self.split()
        self.jensen()
        self.minorize()
        self.climb()
        self.louis()

    def card(self):
        card = chapter_card(8, r"EM", r"Fill in what you did not see", lit=(1977,), part=PART)
        with self.voiceover("Chapter eight. The EM algorithm."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def missing(self):
        rows = [
            cmath(r"\text{observed}", r":", r"x_1, \dots, x_n, \ \ \text{the crabs' ratios}", font_size=30),
            cmath(r"\text{missing}", r":", r"z_i \in \{1, 2\}, \ \ \text{each crab's race}", font_size=30),
            cmath(r"\ell(\theta)", r"=", r"\textstyle\sum_i \log\{p\,\phi_1(x_i) + (1 - p)\,\phi_2(x_i)\}", font_size=30),
            cmath(r"\ell_c(\theta)", r"=", r"\textstyle\sum_i \{[z_i = 1]\log p\,\phi_1(x_i) + [z_i = 2]\log (1-p)\,\phi_2(x_i)\}", font_size=26),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"what we have"), why(r"what would make it easy"), why(r"a log of a sum: \ no closed form"),
                why(r"a sum of logs: \ two separate normal fits")]
        intro = label('Latent component labels would simplify the likelihood', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "The crabs' fit came from an algorithm built on one idea: pretend you know what you don't. "
            "<bookmark mark='a'/> We observe each crab's ratio. <bookmark mark='b'/> We don't observe which race it belongs to, "
            "if races there are. <bookmark mark='c'/> The likelihood of what we did observe is a log of a sum, one term per "
            "component, and setting its derivatives to zero gives equations nobody can solve by hand. "
            "<bookmark mark='d'/> But if the labels were known, the complete-data log likelihood would be a sum of logs: the "
            "proportion would be the share of race one, and each component's mean and spread would be the ordinary mean and "
            "spread of its own crabs."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def steps(self):
        rows = [
            cmath(r"\text{E-step}", r":", r"r_i = \dfrac{p\,\phi_1(x_i)}{p\,\phi_1(x_i) + (1 - p)\,\phi_2(x_i)}", font_size=30),
            cmath(r"\text{M-step}", r":", r"p = \bar r, \ \ \mu_1 = \dfrac{\sum r_i x_i}{\sum r_i}, \ \ \sigma_1^2 = \dfrac{\sum r_i (x_i - \mu_1)^2}{\sum r_i}", font_size=28),
            cmath(r"\text{repeat}", r":", r"\text{until the log likelihood stops rising}", font_size=30),
            cmath(r"\text{Dempster, Laird, Rubin}", r":", r"\text{1977: \ a framework for incomplete-data estimation}", font_size=28),
        ]
        rows[0][2].set_color(CRAB1)
        whys = [why(r"each crab's chance of race 1, \ given $\theta$"), why(r"weighted fits, \ as if the $r_i$ were labels"),
                why(r"chapter eight's guarantee: \ it never falls"), why(r"McKendrick (1926), \ Hartley (1958), \ Baum (1970)")]
        intro = label('EM alternates conditional expectation and maximization', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> So alternate. In the E-step, for expectation, use the current parameters to compute"
            " each crab's probability of belonging to race one: its responsibility. <bookmark mark='b'/> In the "
            "M-step, for maximization, refit as if the responsibilities were labels: the proportion is the average "
            "responsibility, and each mean and variance is a weighted mean and variance. <bookmark mark='c'/> Monitor"
            " likelihood changes, parameter changes and numerical diagnostics; a tiny likelihood increment alone need"
            " not establish parameter accuracy. <bookmark mark='d'/> Arthur Dempster, Nan Laird and Donald Rubin "
            "named the algorithm in 1977 and gave a general framework for many incomplete-data problems, although "
            "either step may still be difficult; special cases go back to the epidemiologist Anderson McKendrick in "
            "1926 and to the Baum–Welch algorithm for hidden Markov models."       ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def split(self):
        d = load("crabs")
        x, w, r = np.asarray(d["x"]), np.asarray(d["w"]), np.asarray(d["resp"])
        A = crab_axes()
        ax = A.ax
        wd = ax.c2p(0.0038, 0)[0] - ax.c2p(0, 0)[0]
        grey, lower, upper = VGroup(), VGroup(), VGroup()
        for a, c, q in zip(x, w, r):
            h = max(0.01, ax.c2p(0, c)[1] - ax.c2p(0, 0)[1])
            h1 = max(0.005, ax.c2p(0, c * q)[1] - ax.c2p(0, 0)[1])
            h2 = max(0.005, h - h1)
            grey.add(Rectangle(width=wd, height=h, stroke_width=0, fill_color=GREY_B, fill_opacity=0.75).move_to(ax.c2p(a, 0), aligned_edge=DOWN))
            b1 = Rectangle(width=wd, height=h1, stroke_width=0, fill_color=CRAB1, fill_opacity=0.85).move_to(ax.c2p(a, 0), aligned_edge=DOWN)
            b2 = Rectangle(width=wd, height=h2, stroke_width=0, fill_color=CRAB2, fill_opacity=0.85).next_to(b1, UP, buff=0)
            lower.add(b1)
            upper.add(b2)
        k = int(np.argmin(np.abs(x - 0.6535)))
        rows = fit_rows(VGroup(
            label(r"the E-step at the fitted values", font_size=22),
            label(r"blue: \ expected race-1 crabs, \ $\sum r_i$", font_size=22, color=CRAB1),
            label(r"red: \ the rest, \ race 2", font_size=22, color=CRAB2),
            label(rf"at {x[k]:.4f}: \ {100 * r[k]:.0f}\% blue, \ {100 * (1 - r[k]):.0f}\% red", font_size=22),
            label(r"every crab is split, \ not assigned", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the E-step at the final fit, on Weldon's histogram. <bookmark mark='b'/> Each interval's "
            "crabs are split between the races in proportion to their responsibilities: blue is the expected number from race "
            "one, <bookmark mark='c'/> red the expected number from race two. Almost every crab on the far left is blue; "
            "<bookmark mark='d'/> just left of the histogram's peak, at point six five three five, about a fifth are still blue, "
            "and in the far right tail blue creeps back, because race one is the broader. <bookmark mark='e'/> No crab is ever assigned outright; EM splits each one and fits the pieces."
        ) as vo:
            self.add(crab_tag())
            self.play(FadeIn(A), FadeIn(grey))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeOut(grey), LaggedStart(*[GrowFromEdge(b, DOWN) for b in lower], lag_ratio=0.03), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in upper], lag_ratio=0.03), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Indicate(VGroup(lower[k], upper[k]), color=PATH), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def jensen(self):
        rows = [
            cmath(r"\ell(\theta)", r"=", r"\log \textstyle\sum_z q(z)\, \dfrac{f(x, z; \theta)}{q(z)}", font_size=30),
            cmath(r"", r"\ge", r"\textstyle\sum_z q(z) \log \dfrac{f(x, z; \theta)}{q(z)}", font_size=30),
            cmath(r"\text{equality}", r":", r"q(z) = f(z \mid x; \theta_t) \ \text{at } \theta = \theta_t", font_size=30),
            cmath(r"\ell(\theta)", r"\ge", r"\ell(\theta_t) + Q(\theta \mid \theta_t) - Q(\theta_t \mid \theta_t)", font_size=30),
        ]
        rows[3][-1].set_color(PATH)
        whys = [why(r"any distribution $q$ for the missing labels"), why(r"Jensen: \ log of an average $\ge$ average of logs"),
                why(r"the E-step's responsibilities"), why(r"$Q$: \ the expected complete-data log likelihood")]
        intro = label('Jensen builds a touching lower bound for EM', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Why does it work? <bookmark mark='a'/> Write the likelihood as a sum over the unseen labels, and multiply and "
            "divide by any distribution q for those labels. <bookmark mark='b'/> The log is concave, so by Jensen's inequality "
            "the log of an average is at least the average of the logs: a lower bound on the log likelihood. "
            "<bookmark mark='c'/> The bound is tight, equal, when q is the conditional distribution of the labels given the "
            "data at the current parameters, which is exactly what the E-step computes. <bookmark mark='d'/> So the E-step "
            "builds a lower bound that touches the log likelihood at the current point. Q is the expected complete-data log "
            "likelihood, and the M-step maximizes it."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def minorize(self):
        d = load("em_mm")
        p, ll = np.asarray(d["p"]), np.asarray(d["ll"])
        top = float(ll.max())
        lo = 20 * np.floor((min(s_["ll"] for s_ in d["steps"]) - 30) / 20)
        A = axes([0, 1], [lo, top + 8], x_length=8.0, y_length=4.4, xlabel=r"mixing proportion $p$ \ (other four at the local fit)",
                 ylabel=r"log likelihood", xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[], center=[-1.6, 0.3, 0])
        ax = A.ax
        m = ll > lo
        cv = curve(ax, p[m], ll[m], LIK, 3.5)
        steps = d["steps"]
        bounds_, dots, arrows = VGroup(), VGroup(), VGroup()
        for s_ in steps:
            b = np.asarray(s_["bound"])
            k = b > lo
            bounds_.add(curve(ax, p[k], b[k], PATH, 2.5))
            dots.add(Dot(ax.c2p(s_["p"], s_["ll"]), radius=0.07, color=PATH))
            bt = float(np.interp(s_["next"], p, b))
            arrows.add(Arrow(ax.c2p(s_["next"], bt), ax.c2p(s_["next"], float(np.interp(s_["next"], p, ll))), buff=0,
                             color=HIT, stroke_width=3, tip_length=0.12, max_tip_length_to_length_ratio=0.5))
        rows = fit_rows(VGroup(
            label(r"green: \ the log likelihood in $p$", font_size=22, color=LIK),
            label(r"gold: \ the E-step's lower bound, \ touching at $p_t$", font_size=22, color=PATH),
            label(r"M-step: \ jump to the bound's peak", font_size=22, color=HIT),
            label(rf"$p$: \ {steps[0]['p']:.2f} $\to$ {steps[1]['p']:.2f} $\to$ {steps[2]['p']:.2f} $\to$ {steps[3]['p']:.2f} $\to$ {steps[3]['next']:.2f} $\to \cdots$ {d['p_hat']:.2f}", font_size=22),
            label(r"each step climbs: \ the log likelihood never falls", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's that picture along one coordinate, the mixing proportion, with the other four held at "
            "their estimates. The green curve is the log likelihood. <bookmark mark='b'/> Start at p equals point nine. The "
            "E-step builds the gold lower bound, touching the curve there. <bookmark mark='c'/> The M-step jumps to the bound's "
            "peak, and since the bound lies below the curve, the curve there is at least as high. <bookmark mark='d'/> Build a "
            "new bound at the new point, jump again, and again. <bookmark mark='e'/> Every step climbs. This is the "
            "minorize-maximize idea of Part 21, with the bound supplied by the missing data."
        ) as vo:
            self.play(FadeIn(A), Create(cv))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots[0]), Create(bounds_[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[0]), FadeIn(rows[2]))
            vo.wait_until("d")
            for j in (1, 2, 3):
                self.play(FadeOut(bounds_[j - 1]), FadeIn(dots[j]), Create(bounds_[j]), run_time=0.8)
                self.play(GrowArrow(arrows[j]), run_time=0.6)
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def climb(self):
        d = load("crabs")
        ll = np.asarray(d["loglik"])
        gap = ll[-1] - ll[:-1]
        it = np.arange(len(gap))
        k = gap > 1e-12
        A = axes([0, 1700], [-12, 0], x_length=8.0, y_length=4.4, xlabel=r"EM iteration", ylabel=r"$\log_{10}$ gap to the attained local limit",
                 xticks=[0, 400, 800, 1200, 1600], yticks=[-12, -9, -6, -3, 0], center=[-1.6, 0.3, 0])
        ax = A.ax
        pl = polyline(ax, it[k], np.log10(gap[k]), PATH, 3)
        th0, th = np.asarray(d["path"])[0], d["theta"]
        rows = fit_rows(VGroup(
            label(rf"start: \ $p = {th0[0]:.2f}$; \ end: \ $p = {th[0]:.4f}$", font_size=22),
            label(rf"{d['iters']:,} iterations to a change below $10^{{-13}}$", font_size=22, color=PATH),
            label(r"a straight line: \ linear convergence", font_size=22),
            label(rf"each step keeps {100 * d['rate']:.2f}\% of the error", font_size=22, color=RES),
            label(r"Newton: local acceleration; \ both methods need safeguards", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The full five-parameter run on the crabs started from p equals one half and ended "
            "at point four three. <bookmark mark='b'/> It took one thousand six hundred and twenty-two iterations. "
            "<bookmark mark='c'/> On a log scale, the gap between the current log likelihood and the attained local "
            "log-likelihood limit falls approximately along a straight line: linear convergence, the same fraction of"
            " the error gone each step. <bookmark mark='d'/> Here each step keeps ninety-nine point three six percent"
            " of the error in the parameters, so the gap, which is quadratic in the error, shrinks by about one point"
            " three percent per step. <bookmark mark='e'/> Newton's method from Part 21 would finish in a handful of "
            "steps, but unsafeguarded Newton can wander off or propose a negative variance. EM preserves nonnegative "
            "variance updates, yet can still approach a singular collapsed component. Practical software often runs "
            "EM first and finishes with Newton."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(pl), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def louis(self):
        d = load("crabs")
        se = d["se"]
        rows = [
            cmath(r"\text{rate}", r"=", r"\text{largest share of the information that is missing}", font_size=28),
            cmath(r"I_{\text{obs}}", r"=", r"I_{\text{complete}} - I_{\text{missing}}", font_size=30),
            cmath(r"\text{crabs}", r":", rf"\text{{rate }} {d['rate']:.4f}: \ \text{{the races overlap heavily}}", font_size=28),
            cmath(r"\mathrm{SE}(\hat p)", r"=", rf"{se[0]:.3f}: \ \ \hat p = {d['theta'][0]:.2f} \pm {1.96 * se[0]:.2f}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"Dempster, Laird \& Rubin (1977)"), why(r"the missing-information principle (Louis 1982)"),
                why(r"the labels are almost entirely unknown"), why(r"from the observed information: \ the mix is barely pinned down")]
        intro = label('Missing labels reduce the observed information', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Near a regular isolated EM fixed point, the dominant linear convergence rate is an "
            "eigenvalue of the missing-information fraction matrix. Our successive-step estimate illustrates that "
            "local result. <bookmark mark='b'/> Thomas Louis turned this into a formula for standard errors in 1982: "
            "the observed information is the complete information minus the missing information. <bookmark mark='c'/>"
            " For the crabs the rate is point nine nine three six: the two races overlap so much that the labels, "
            "which would make the problem easy, are almost entirely unknown. <bookmark mark='d'/> The observed "
            "information gives a standard error for the proportion of point one five, so the local curvature "
            "approximation is forty-three percent plus or minus twenty-nine points. Weak separation and mixture "
            "irregularity limit the reliability of this Wald approximation. The means are pinned down to a few "
            "thousandths, but how the crabs divide between the races the data barely say."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
