from __future__ import annotations

import numpy as np

from videos.stats.stats48.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.paths()
        self.kolmogorov()
        self.question()
        self.upgrades()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1933, 1949, 1952)).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"1933: \ Kolmogorov: \ the law of $\sqrt n \sup_x |F_n(x) - F(x)|$, \ by hard analysis", font_size=26),
            label(r"1949: \ Doob: \ $\sqrt n(F_n - F)$ looks like a Brownian bridge, \ so its sup should too", font_size=26, color=EMPC),
            label(r"1952: \ Donsker proves the guess: \ a central limit theorem for a whole random function", font_size=26, color=GOODC),
            label(r"1956--1978: \ Skorokhod, \ Dudley: \ the measure theory it needed, \ and a far wider reach", font_size=26, color=CLASSC),
        ), 12.4, 0.55, [0, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1933 Andrei Kolmogorov found the limiting law of the largest gap between an empirical "
            "distribution function and the true one, scaled by root n, by a long and difficult calculation. <bookmark "
            "mark='b'/> In 1949 Joseph Doob made a guess. Root n times the gap, as a function of x, behaves like a Brownian "
            "bridge, a Brownian motion pinned to zero at both ends. So its largest value should behave like the largest "
            "value of the bridge, and Kolmogorov's law should simply be the law of that maximum. <bookmark mark='c'/> Three "
            "years later Monroe Donsker proved it: a central limit theorem, not for a number, but for an entire random "
            "function. <bookmark mark='d'/> Making the proof airtight took Skorokhod and Dudley, and what they built became "
            "the theory of empirical processes, which now sits underneath most of modern statistics and machine learning."
        ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def paths(self):
        d = load("hook")
        g = np.asarray(d["grid"])
        A = axes([0, 1], [-1.6, 1.6], x_length=7.4, y_length=4.4, xlabel=r"$u = F(x)$", ylabel=r"$\sqrt n\,(F_n - F)$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[-1, 0, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"20": S.PRIOR, "200": S.ALT, "5000": EMPC}
        cs = {n: clip_curve(ax, g, d["paths"][n], c, 3, ymin=-1.6, ymax=1.6) for n, c in cols.items()}
        br = clip_curve(ax, np.linspace(0, 1, 401), d["bridge"], BRIDGEC, 3, ymin=-1.6, ymax=1.6)
        side = fit_rows(VGroup(
            label(r"uniform data: \ $F(x) = x$", font_size=22),
            label(r"purple: \ $n = 20$: \ a staircase", font_size=22, color=S.PRIOR),
            label(r"teal: \ $n = 200$", font_size=22, color=S.ALT),
            label(r"blue: \ $n = 5000$: \ rough, \ like Brownian motion", font_size=22, color=EMPC),
            label(r"white: \ a Brownian bridge, \ pinned at 0 and 1", font_size=22, color=BRIDGEC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Take uniform data, so that the true distribution function is the diagonal, and draw root n "
            "times the gap between the empirical and the true distribution functions. <bookmark mark='b'/> With twenty "
            "points it is a staircase: it jumps up by one over root n at each data point and slides down in between. "
            "<bookmark mark='c'/> With two hundred the steps are finer, <bookmark mark='d'/> and with five thousand the "
            "path is as rough as a Brownian motion. <bookmark mark='e'/> Beside it, a Brownian bridge: the same roughness, "
            "the same pinning at zero and one, and the same variance, u times one minus u, at each point."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["20"]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(cs["200"]), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(cs["5000"]), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(br), FadeIn(side[4]), run_time=1.5)
        self.clear_scene()

    def kolmogorov(self):
        d = load("hook")
        e = np.asarray(d["edges"])
        A = axes([0, 2.4], [0, 1.9], x_length=7.4, y_length=4.4, xlabel=r"$\sqrt n\, D_n = \sqrt n \sup |F_n - F|$", ylabel=r"density",
                 xticks=[0, 0.5, 1, 1.5, 2], yticks=[0, 0.5, 1, 1.5], center=[-2.5, 0.2, 0])
        ax = A.ax
        h5 = hist_bars(ax, e, d["5"]["hist"], color=S.PRIOR, opacity=0.35)
        h100 = hist_bars(ax, e, d["100"]["hist"], color=EMPC, opacity=0.55)
        kc = polyline(ax, d["u"], d["dens"], BRIDGEC, 4)
        side = fit_rows(VGroup(
            label(r"20,000 samples of each size", font_size=22),
            label(rf"purple: \ $n = 5$: \ 95th percentile {d['5']['q95']:.3f}", font_size=22, color=S.PRIOR),
            label(rf"blue: \ $n = 100$: \ {d['100']['q95']:.3f}", font_size=22, color=EMPC),
            label(rf"white: \ $\sup |B|$: \ Kolmogorov's law, \ {d['k95']:.3f}", font_size=22, color=BRIDGEC),
            label(r"the same law for every continuous $F$", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Now the largest gap itself, simulated twenty thousand times. <bookmark mark='b'/> With "
            f"five observations its ninety-fifth percentile is {say(d['5']['q95'], 2)}; <bookmark mark='c'/> with a hundred, "
            f"{say(d['100']['q95'], 2)}. <bookmark mark='d'/> The white curve is the density of the largest absolute value "
            f"of a Brownian bridge, Kolmogorov's distribution, with ninety-fifth percentile {say(d['k95'], 3)}. Doob's guess "
            f"is right. <bookmark mark='e'/> And because the probability integral transform turns any continuous "
            f"distribution into the uniform, the same law holds whatever F is: the test is distribution-free."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated: \ 20,000 samples per $n$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(h5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(h100), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(kc), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"$F_n(x)$ is an average: \ $P_n f = \tfrac1n \sum_i f(X_i)$ \ with $f = \mathbf 1\{\cdot \le x\}$", font_size=28),
            label(r"the empirical process: \ $\mathbb G_n f = \sqrt n\,(P_n f - P f)$, \ indexed by a class $\mathcal F$", font_size=28, color=EMPC),
            label(r"the question: \ for which classes $\mathcal F$ do the LLN and the CLT hold \emph{uniformly}, \ and how fast?", font_size=28, color=CLASSC),
            label(r"why it matters: \ M-estimators, \ bootstraps, \ bands, \ classifiers \ all take a sup over a class", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The general idea is a change of viewpoint. The empirical distribution function at x is an "
            "average: the average of an indicator function over the sample. <bookmark mark='b'/> So instead of one "
            "average, consider many at once: the empirical process, root n times the gap between the sample average and "
            "the true mean, as a function of f running over a whole class of functions. Distribution functions are the "
            "class of indicators of half-lines. <bookmark mark='c'/> The question of this part is: for which classes do the "
            "law of large numbers and the central limit theorem hold uniformly over the class, and at what rate? <bookmark "
            "mark='d'/> It matters because so much of statistics takes a supremum over a class: the consistency of "
            "M-estimators, the bootstrap, confidence bands, and the theory of classifiers."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(8, r"the plug-in principle: \ $F_n \to F$", r"uniformly, \ on trust",
                         r"chapters 1--2: \ Glivenko--Cantelli, \ symmetrization, \ VC classes"),
            upgrade_card(44, r"Donsker's invariance principle", r"stated, \ for partial sums",
                         r"chapters 4--5: \ entropy, \ chaining, \ Donsker classes, \ proved"),
            upgrade_card(47, r"a uniform LLN; \ the bootstrap empirical process", r"both, \ on trust",
                         r"chapters 7, \ 11, \ 12: \ the functional delta method, \ bootstraps, \ estimated parameters"),
        ]
        for c in cards:
            c.scale(0.86)
        VGroup(*cards).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Three promises are due. Part eight used the plug-in principle, that the empirical "
            "distribution converges to the true one uniformly; chapters one and two prove it, and much more. <bookmark "
            "mark='b'/> Part forty-four stated Donsker's invariance principle for random walks; chapters four and five "
            "prove the empirical-process version with entropy and chaining. <bookmark mark='c'/> And Part forty-seven twice "
            "pointed here: for the uniform law of large numbers behind consistency, and for the bootstrap empirical process. "
            "Those arrive in chapters seven, eleven and twelve."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 48", font_size=34, color=GREY_B), label(r"Empirical Processes", font_size=48)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Glivenko--Cantelli classes; \ symmetrization; \ Rademacher averages; \ VC dimension",
            r"covering and bracketing numbers; \ Dudley's chaining; \ Donsker classes",
            r"Talagrand's concentration; \ the functional delta method; \ Z-estimators with nuisance parameters",
            r"rates and cube-root asymptotics; \ the bootstrap empirical process; \ KS with estimated parameters",
        ], color=CLASSC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 43, \ 44, \ 47").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.empirical}, \ the chaining net").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-eight: empirical processes. <bookmark mark='b'/> We'll prove uniform laws of "
            "large numbers by symmetrization and Rademacher averages, and measure the size of a class by its VC dimension; "
            "measure it more finely by covering and bracketing numbers, and use Dudley's chaining, drawn as refining nets, "
            "to prove uniform central limit theorems; meet Talagrand's concentration inequality; differentiate along the "
            "empirical process, with quantiles, Kaplan–Meier and estimators with nuisance parameters; find the cube-root "
            "rate of the Grenander estimator; and finish with the bootstrap and the Kolmogorov–Smirnov test done right."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
