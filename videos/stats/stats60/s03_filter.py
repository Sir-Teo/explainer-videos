from __future__ import annotations

import numpy as np

from videos.stats.stats60.common import *  # noqa: F403


class Filter(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter two. Efficient robust estimation in high dimensions: the filter.", 2,
                            r"Efficient high-dimensional robustness", r"Robust and computable", lit=(2016,))
        self.problem()
        self.attack()
        self.idea()
        self.why()
        self.chart()
        self.eps_chart()
        self.sos()

    def problem(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The goal: estimate the mean of a d-dimensional Gaussian from n samples, an epsilon fraction "
            "of them chosen by an adversary. <bookmark mark='b'/> The best possible error is of order epsilon, plus "
            "the sampling error root d over n. <bookmark mark='c'/> The Tukey median achieves it, but "
            "cannot be computed. The coordinatewise and geometric medians can be computed, but their error grows like epsilon "
            "root d. <bookmark mark='d'/> In 2016 two groups, Ilias Diakonikolas, Gautam Kamath, Daniel Kane, Jerry Li, Ankur "
            "Moitra and Alistair Stewart, and independently Kevin Lai, Anup Rao and Santosh Vempala, found polynomial-time "
            "estimators whose error barely depends on the dimension: Lai, Rao and Vempala's grows like root log d, and "
            "Diakonikolas and co-authors' is epsilon times a root-log factor, with no d at all.",
            [(r"\text{goal}", r":", r"\text{the mean of } N(\mu, I_d), \ \varepsilon n \text{ points adversarial}", 38),
             (r"\text{optimal}", r":", r"\varepsilon + \sqrt{d/n}", 40),
             (r"\text{easy medians}", r":", r"\text{error} \propto \varepsilon\sqrt d", 40),
             (r"\text{2016}", r":", r"\text{polynomial time, \ (nearly) dimension-free error}", 40)],
            [r"the strong model", r"up to constants", r"computable, \ not robust", r"Diakonikolas et al.; \ Lai, \ Rao \& Vempala"],
            colors=[(2, NAIVEC), (3, FIXC)])

    def attack(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The adversary's simplest effective move: put every planted point at the same location, with "
            "every coordinate equal to two. <bookmark mark='b'/> Each coordinate's median moves by about one and a quarter "
            "times epsilon, since the median shifts until it has absorbed the extra mass on one side. <bookmark mark='c'/> "
            "Across d coordinates, those shifts add in quadrature: the error is about one and a quarter epsilon root d. "
            "<bookmark mark='d'/> The mean moves by two epsilon root d. Neither notices that the planted points are, as a "
            "cluster, very far from the rest.",
            [(r"\text{the attack}", r":", r"\varepsilon n \text{ points at } (2, 2, \dots, 2)", 40),
             (r"\text{per coordinate}", r":", r"\text{the median moves} \approx 1.25\,\varepsilon", 40),
             (r"\text{coordinatewise median}", r":", r"\text{error} \approx 1.25\,\varepsilon\sqrt d", 40),
             (r"\text{mean}", r":", r"\text{error} = 2\varepsilon\sqrt d", 40)],
            [r"a tight cluster", r"$1/(2\phi(0)) \approx 1.25$", r"adds up", r"worse still"],
            colors=[(2, NAIVEC), (3, NAIVEC)])

    def idea(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Spectral filtering exploits the relation between a displaced mean and inflated variance, together with stability of the clean sample. <bookmark mark='b'/> The displayed implementation uses a Marchenko-Pastur edge plus heuristic slack as its stopping threshold. This threshold alone is not a robust-estimation certificate. <bookmark mark='c'/> It removes the most extreme five percent of top-eigenvector projections each round. <bookmark mark='d'/> Certified filters instead choose thresholds with a proof that contamination decreases relative to retained clean mass. Our deterministic trimming illustrates the idea on this planted attack; it does not implement that theorem.",
            [(r"\text{key fact}", r":", r"\text{a shifted mean} \Rightarrow \text{an inflated variance in that direction}", 36),
             (r"\lambda_{\max}(\hat\Sigma)", r"\le", r"(1 + \sqrt{d/n})^2 + C\varepsilon\log\tfrac1\varepsilon: \ \text{heuristic stop}", 36),
             (r"\text{else}", r":", r"\text{project on the top eigenvector; \ remove the extremes}", 38),
             (r"\text{repeat}", r":", r"\text{certified filters prove progress; \ this trimming is heuristic}", 38)],
            [r"a certificate", r"the clean edge plus slack", r"one direction at a time", r"a potential argument"],
            colors=[(1, FIXC)])

    def why(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Why can spectral information help? One needs both clean-sample stability and control of the contamination budget. <bookmark mark='b'/> Moving the mean by delta using epsilon mass creates a variance contribution with scale delta squared over epsilon. Deletions and changes in the retained clean mean also need bounds. <bookmark mark='c'/> Under appropriate Gaussian stability conditions, certified filters obtain error of order epsilon root log one over epsilon, plus sampling error, in the strong contamination model. <bookmark mark='d'/> An eigenvalue is part of this certificate. A small top eigenvalue, without the other assumptions, does not certify proximity to any particular clean mean.",
            [(r"\text{if}", r":", r"\text{outliers move the mean by } \delta \text{ along } v", 40),
             (r"\text{then}", r":", r"\text{contamination contribution has scale } \delta^2/\varepsilon", 40),
             (r"\text{Gaussian stability + spectral control}", r"\Rightarrow", r"\delta = O\big(\varepsilon\sqrt{\log(1/\varepsilon)}\big)", 40),
             (r"\text{so}", r":", r"\text{an eigenvalue replaces a minimum over directions}", 38)],
            [r"the adversary's dilemma", r"Chebyshev, \ reversed", r"the certificate", r"polynomial time"],
            colors=[(2, FIXC)])

    def chart(self):
        d = load("robust")
        R = d["rows"]
        ds = np.log10([r["d"] for r in R])
        A = axes([0.6, 2.4], [0, 3.0], x_length=7.4, y_length=4.4, xlabel=r"dimension $d$ (log scale)", ylabel=r"error $\|\hat\mu - \mu\|$",
                 xticks=[1, 2], xfmt=lambda v: f"{10 ** v:g}", yticks=[0, 1, 2, 3], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"mean": NAIVEC, "coord_median": BADC, "geo_median": DEPTHC, "filter": FIXC, "oracle": GREY_B}
        lines = {k: VGroup(polyline(ax, ds, [r[k] for r in R], c, 10 if k == "oracle" else 3.5, 0.5 if k == "oracle" else 1.0),
                           *[Dot(ax.c2p(a, r[k]), radius=0.06, color=c) for a, r in zip(ds, R)])
                 for k, c in cols.items()}
        r100 = [r for r in R if r["d"] == 100][0]
        side = side_groups([
            [(rf"$n = {d['n']:,}$, \ $\varepsilon = {d['eps']}$", WHITE), (r"the $(2, \dots, 2)$ attack", GREY_A)],
            [(r"red: \ the mean", NAIVEC), (r"orange: \ coordinatewise median", BADC)],
            [(r"purple: \ geometric median", DEPTHC)],
            [(r"green: \ heuristic spectral trimming", FIXC), (r"grey band: \ mean of the clean points", GREY_B)],
            [(rf"$d = 100$: \ mean {r100['mean']:.2f}", GREY_A), (rf"medians {r100['coord_median']:.2f}, \ {r100['geo_median']:.2f}", GREY_A),
             (rf"filter {r100['filter']:.2f}", FIXC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The four estimators, as the dimension grows, with two thousand points and ten percent "
            f"planted. <bookmark mark='b'/> The mean and the coordinatewise median grow like root d. <bookmark mark='c'/> So does "
            f"the geometric median, more slowly. <bookmark mark='d'/> The filter tracks the grey oracle, the mean of the clean "
            f"points alone: its observed error is close to the clean-sample error in these four seeded repetitions. This is not a worst-case guarantee. <bookmark mark='e'/> At a hundred dimensions, the mean is off "
            f"by {say(r100['mean'], 2)}, the medians by {say(r100['coord_median'], 2)} and {say(r100['geo_median'], 2)}, the "
            f"filter by {say(r100['filter'], 2)}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated, \ four repetitions")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lines["mean"]), Create(lines["coord_median"]), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lines["geo_median"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(lines["oracle"]), Create(lines["filter"]), FadeIn(side[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def eps_chart(self):
        d = load("robust")
        R = d["rows_eps"]
        es = np.array([r["eps"] for r in R])
        A = axes([0, 0.21], [0, 4.2], x_length=7.4, y_length=4.4, xlabel=rf"contaminated fraction $\varepsilon$, \ $d = {d['d_fixed']}$", ylabel=r"error $\|\hat\mu - \mu\|$",
                 xticks=[0, 0.05, 0.1, 0.15, 0.2], yticks=[0, 1, 2, 3, 4], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"mean": NAIVEC, "coord_median": BADC, "geo_median": DEPTHC, "filter": FIXC}
        lines = [VGroup(polyline(ax, es, [r[k] for r in R], c, 3.5), *[Dot(ax.c2p(a, r[k]), radius=0.06, color=c) for a, r in zip(es, R)]) for k, c in cols.items()]
        last = R[-1]
        side = side_groups([
            [(r"the same estimators, \ $\varepsilon$ growing", WHITE)],
            [(r"mean, \ medians: \ linear in $\varepsilon$", NAIVEC), (r"slope $\propto \sqrt d$", NAIVEC)],
            [(r"the filter: \ near the sampling error", FIXC), (rf"{last['filter']:.2f} at $\varepsilon = 0.2$", FIXC)],
            [(rf"removed: \ {100 * last['removed_bad']:.0f}\% of the planted", GREY_A), (rf"and {100 * last['removed_good']:.0f}\% of the clean", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> Fix a hundred dimensions and vary the contamination. <bookmark mark='b'/> The mean and the "
            f"two medians grow linearly in epsilon, with slopes proportional to root d. <bookmark mark='c'/> The filter stays "
            f"near the sampling error throughout, {say(last['filter'], 2)} at twenty percent contamination. <bookmark mark='d'/> "
            f"It removed {100 * last['removed_bad']:.0f} percent of the planted points, and {100 * last['removed_good']:.0f} percent "
            f"of the clean ones: the price of caution is small."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated, \ four repetitions")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[Create(l) for l in lines[:3]], FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lines[3]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def sos(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Convex reweighting offers another route to spectral control. <bookmark mark='b'/> Sum-of-squares methods certify higher moments for more demanding robust-estimation problems. <bookmark mark='c'/> Computational limits depend on the corruption model. Statistical-query lower bounds support an epsilon root log one over epsilon barrier for strong or total-variation corruption of isotropic Gaussians. They do not give that barrier for Huber mixtures. <bookmark mark='d'/> In fact, Diakonikolas, Kane, Pensia and Pittas obtained order-epsilon error with near-optimal samples and almost-linear time for the Huber model in 2023. Their algorithm is more elaborate than this demonstration.",
            [(r"\text{other methods}", r":", r"\text{convex reweighting with a spectral constraint}", 38),
             (r"\text{harder problems}", r":", r"\text{sum-of-squares certificates of moments}", 38),
             (r"\text{lower bound}", r":", r"\text{strong/TV corruption, SQ barrier: } \varepsilon\sqrt{\log(1/\varepsilon)}", 36),
             (r"\text{the book}", r":", r"\text{Huber: \ DKPP (2023) achieve } O(\varepsilon)", 40)],
            [r"many routes", r"higher moments", r"statistical-computational limits", r"\emph{Algorithmic High-Dimensional Robust Statistics}"],
            colors=[(2, NAIVEC)])
