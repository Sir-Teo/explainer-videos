from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.risk()
        self.local()
        self.price()
        self.upgrades()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1951,)).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"Fisher's claim: \ the MLE's asymptotic variance $1/(nI)$ is the smallest possible", font_size=26),
            label(r"1951: \ Joseph Hodges: \ $T_n = \bar x$ if $|\bar x| \ge n^{-1/4}$, \ else $0$", font_size=28, color=HODC),
            label(r"at $\theta = 0$: \ $n\,E\,T_n^2 \to 0$; \ \ elsewhere: \ the same limit as $\bar x$", font_size=26, color=HODC),
            label(r"Le Cam (1953): \ such points form a set of measure zero; \ Hájek (1970, 1972): \ the right theorem", font_size=26, color=S.ACCENT),
        ), 12.4, 0.55, [0, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fisher had claimed that no estimator can have a smaller asymptotic variance than the "
            "maximum likelihood estimate's, one over n times the information. <bookmark mark='b'/> In 1951 Joseph Hodges "
            "produced a counterexample. For normal data, use the sample mean, unless it is within n to the minus one "
            "quarter of zero, in which case report zero. <bookmark mark='c'/> At theta equal to zero this estimator's "
            "scaled risk goes to zero, beating the bound; at every other theta its limit is the same as the mean's. "
            "<bookmark mark='d'/> Lucien Le Cam showed in 1953 that such superefficiency can happen only on a set of measure "
            "zero, and Jaroslav Hájek found the theorem that says exactly in what sense the MLE is best. This part builds "
            "the toolkit for that theorem and then proves it."
        ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def risk(self):
        d = load("hook")
        th = np.asarray(d["theta"])
        A = axes([-0.6, 0.6], [0, 6], x_length=7.4, y_length=4.4, xlabel=r"$\theta$", ylabel=r"$n\, E_\theta (T_n - \theta)^2$",
                 xticks=[-0.5, 0, 0.5], yticks=[0, 1, 2, 4, 6], center=[-2.5, 0.2, 0])
        rb = RiskBump(A.ax)
        bd = rb.bound(1.0, MLEC)
        cols = {25: S.PRIOR, 100: ALTC, 1000: S.ACCENT, 10000: HODC}
        cs = {n: rb.curve(th, d[f"r{n}"], c, 3.5, ymax=6) for n, c in cols.items()}
        side = fit_rows(VGroup(
            label(r"blue dashed: \ $\bar x$, \ scaled risk 1 \ at every $\theta$", font_size=22, color=MLEC),
            label(r"Hodges: \ purple 25, \ teal 100, \ gold $10^3$, \ red $10^4$", font_size=22, color=HODC),
            label(rf"at $\theta = 0$: \ {d['at0']['25']:.2f}, \ {d['at0']['100']:.3f}, \ $\to 0$", font_size=22, color=GOODC),
            label(r"but a bump beside it, \ taller and narrower as $n$ grows", font_size=22, color=HODC),
            label(r"pointwise, \ the bump moves in and vanishes", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here are the exact risks, scaled by n so that the sample mean's is one everywhere. "
            f"<bookmark mark='b'/> Hodges's estimator, for twenty-five, a hundred, a thousand and ten thousand observations. "
            f"<bookmark mark='c'/> At zero its scaled risk is {say(d['at0']['25'], 2)}, then {say(d['at0']['100'], 2)}, and "
            f"heads to zero. <bookmark mark='d'/> But just beside zero there is a bump, where the estimator says zero when "
            f"the truth is not, and the bump grows taller and narrower with n. <bookmark mark='e'/> At any fixed theta the "
            f"bump eventually passes by, which is why the pointwise limit looks so good."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ normal integrals")))
            vo.wait_until("a")
            self.play(Create(bd), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[Create(cs[n]) for n in cols], FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def local(self):
        d = load("hook")
        h = np.asarray(d["h"])
        A = axes([0, 45], [0, 3.1], x_length=7.4, y_length=4.4, xlabel=r"local parameter $h = \sqrt n\, \theta$",
                 ylabel=r"$\log_{10}$ of the scaled risk", xticks=[0, 10, 20, 30, 40], yticks=[0, 1, 2, 3], center=[-2.5, 0.2, 0])
        ax = A.ax
        lg = lambda r: np.log10(np.maximum(np.asarray(r), 1e-3))  # noqa: E731
        cols = {"100": ALTC, "10000": S.ACCENT, "1000000": HODC}
        cs = {n: clip_curve(ax, h, lg(d[f"h{n}"]), c, 3.5, ymin=0, ymax=3.1) for n, c in cols.items()}
        pk = d["peaks"]
        dots = VGroup(*[Dot(ax.c2p(pk[n]["at"], np.log10(pk[n]["max"])), radius=0.09, color=c) for n, c in cols.items()])
        side = fit_rows(VGroup(
            label(r"$\theta = h/\sqrt n$: \ teal $10^2$, \ gold $10^4$, \ red $10^6$", font_size=22),
            label(rf"peaks: \ {pk['100']['max']:.1f}, \ {pk['10000']['max']:.0f}, \ {pk['1000000']['max']:.0f}", font_size=22, color=HODC),
            label(rf"at $h \approx n^{{1/4}}$: \ {pk['100']['at']:.1f}, \ {pk['10000']['at']:.1f}, \ {pk['1000000']['at']:.1f}", font_size=22, color=S.ACCENT),
            label(r"the worst local risk grows like $\sqrt n$", font_size=22, color=HODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Zoom in at the natural scale, theta equal to h over root n, and plot the scaled risk "
            f"on a log scale. <bookmark mark='b'/> For a hundred, ten thousand and a million observations, the peaks are "
            f"{say(pk['100']['max'], 1)}, about {pk['10000']['max']:.0f}, and about {pk['1000000']['max']:.0f}, <bookmark "
            f"mark='c'/> reached near h equal to n to the one quarter, the edge of Hodges's zone. <bookmark mark='d'/> The "
            f"worst local risk grows like root n without bound. Superefficiency at one point is paid for by "
            f"catastrophe nearby."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[Create(cs[n]) for n in cols], FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(dots), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def price(self):
        rows = fit_rows(VGroup(
            label(r"the question: \ in what sense is the MLE best, \ if not pointwise?", font_size=28),
            label(r"answer \ (chapter 9): \ \emph{locally} and \emph{uniformly}: \ over $\theta \in \theta_0 \pm c/\sqrt n$", font_size=26, color=GOODC),
            label(r"the tools: \ $o_P$, \ $O_P$, \ M-estimators, \ influence functions, \ U-statistics, \ LAN, \ contiguity", font_size=26, color=GREY_A),
            label(r"and their uses: \ efficient tests, \ the bootstrap's accuracy, \ saddlepoints, \ non-regular models", font_size=26, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So the question of this part: if not at each point separately, in what sense is the "
            "maximum likelihood estimate best? <bookmark mark='b'/> The answer, in chapter nine, is local and uniform: over "
            "every shrinking neighbourhood of a parameter value, of size a constant over root n, no estimator can beat it in "
            "the worst case. <bookmark mark='c'/> Getting there needs the modern toolkit of large-sample theory, <bookmark "
            "mark='d'/> which also explains why tests have the power they have, why the bootstrap is accurate, and what to "
            "do when the regularity fails."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(22, r"the MLE is asymptotically $N(\theta, I^{-1}/n)$; \ Wilks's theorem", r"regularity, \ and optimality, \ on trust",
                         r"chapters 1--2: \ M-estimators, \ consistency and the sandwich, \ proved"),
            upgrade_card(45, r"Cram\'er--Rao for unbiased estimators; \ Hodges's warning", r"best means best at each $\theta$",
                         r"chapters 7--9: \ LAN, \ contiguity, \ the convolution and LAM theorems"),
            upgrade_card(16, r"the bootstrap works", r"a first-order argument",
                         r"chapter 11: \ Hadamard differentiability, \ Edgeworth expansions, \ second-order accuracy"),
        ]
        for c in cards:
            c.scale(0.86)
        VGroup(*cards).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Three promises are due. Part twenty-two stated that the MLE is asymptotically normal with "
            "the inverse information as its variance; chapters one and two prove it for M-estimators in general. "
            "<bookmark mark='b'/> Part forty-five proved the Cramér–Rao bound for unbiased estimators and warned about "
            "Hodges; chapters seven to nine give the bound that applies to every estimator. <bookmark mark='c'/> And Part "
            "sixteen used the bootstrap on a first-order argument; chapter eleven shows why it is more accurate than the "
            "normal approximation."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 47", font_size=34, color=GREY_B), label(r"Asymptotic Statistics", font_size=48)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"stochastic orders; \ M- and Z-estimators; \ the Bahadur representation",
            r"influence functions and the functional delta method; \ U- and rank statistics",
            r"LAN, \ contiguity, \ Le Cam's lemmas; \ Hájek's convolution and LAM theorems",
            r"efficiency of tests; \ the bootstrap's second-order accuracy; \ saddlepoints; \ non-regular models",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 22, \ 43, \ 45, \ 46").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.asymptotics}, \ the risk-bump explorer").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-seven: asymptotic statistics. <bookmark mark='b'/> We'll set up stochastic "
            "orders and prove the asymptotics of M-estimators and sample quantiles; differentiate statistical functionals "
            "with influence functions; analyse U-statistics and rank statistics by Hájek's projection; build Le Cam's theory "
            "of local asymptotic normality and contiguity, and prove Hájek's convolution and local asymptotic minimax "
            "theorems, with a risk-bump explorer for Hodges's estimator; and then turn the theory on tests, the bootstrap, "
            "saddlepoints and non-regular models."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
