from __future__ import annotations

from videos.stats.stats39.common import *  # noqa: F403

PROBLEMS = [
    r"Ordinary kriging: \ minimize $\text{Var}(\lambda^\top Z - Z_0)$ subject to $\mathbf 1^\top\lambda = 1$; \ show the variance is $C(0) - \lambda^\top k_0 - m$.",
    r"On a line with $C(h) = e^{-|h|}$, \ show simple kriging at $s_1 < s_0 < s_2$ ignores every point beyond $s_1$ and $s_2$.",
    r"For Brownian motion with $\text{Var}\,W(t) = \sigma^2 t$, \ find $\gamma(h)$, \ and show it has no sill.",
    r"Show that Moran's $I$ has mean $-1/(n-1)$ under random permutation of the values.",
    r"For a homogeneous Poisson process in the plane, \ show $K(r) = \pi r^2$ \ (ignore edges).",
    r"Derive $\text{EI} = (f^* - \mu)\Phi(z) + s\,\phi(z)$ \ for $f \sim N(\mu, s^2)$, \ $z = (f^* - \mu)/s$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Krige: \ weights from covariance, \ 1951", TAUC), (r"Tobler; \ three kinds of spatial data", GREY_A),
            (r"Bochner: \ which functions are covariances", FIELDC), (r"variograms: \ nugget, \ sill, \ range", VARC),
            (r"kriging: \ the BLUP, \ and the GP posterior", FIELDC), (r"Mat\'ern; \ only $\sigma^2/\rho^{2\nu}$ is learnable", TAUC),
            (r"ML and REML; \ the $O(n^3)$ wall", BANDC), (r"Vecchia: \ 100,000 sites in seconds", BANDC),
            (r"GMRFs, \ the SPDE, \ INLA", FIELDC), (r"Moran's $I$; \ BYM disease maps", AREAC),
            (r"Ripley's $K$; \ Snow's pump; \ Cox processes", PTC), (r"confounding; \ space--time; \ BO; \ honest CV", MISSC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 39, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part thirty-nine in twelve lines. <bookmark mark='a'/> Krige weighted his boreholes by how gold grades "
            "covary with distance. Tobler's law says near things are more related, and spatial data come as fields, areas "
            "or points. Bochner's theorem says which functions can be covariances: those with non-negative spectra. The "
            "variogram describes dependence by its nugget, sill and range. Kriging is the best linear unbiased predictor, "
            "and the posterior mean of a Gaussian process. The Matérn family has a smoothness parameter, and under infill "
            "only one combination of variance and range can be learned, the one predictions need. Likelihood and REML fit "
            "the covariance and the trend together, at a cubic cost. Vecchia's conditioning on a few neighbours handles a "
            "hundred thousand locations in seconds. Markov random fields and the SPDE make the precision sparse, and INLA "
            "fits them fast. Moran's I detects clustering in areas, and the BYM model smooths a speckled disease map. "
            "Ripley's K found Snow's cluster, and Cox processes model it. And a spatial random effect does not adjust for a "
            "confounder; separable covariances are a choice; Gaussian processes optimize expensive functions; and coverage "
            "must be checked with a cross-validation that matches the task."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(39, r"dependence in space: \ fields, \ areas, \ points",
                            r"every value observed, \ eventually: \ nothing cut short",
                            r"Part 40: \ lifetimes we have not finished watching: \ Kaplan--Meier, \ Cox, \ censoring")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part handled dependence in space. <bookmark mark='b'/> Every "
            "value we used was observed in full: a concentration, a count, a location. <bookmark mark='c'/> Part forty "
            "turns to time measured until an event, where the study ends before many of the events happen. The survival "
            "curve of Kaplan and Meier, Cox's partial likelihood, and the traps of hazard ratios."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"shared frailties: \ random effects for lifetimes", [40]), (r"kriging as imputation; \ measurement error", [41]),
            (r"Brownian motion, \ a Gaussian process", [44]), (r"GP priors: \ how fast posteriors contract", [53]),
            (r"new regions as distribution shift", [60]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part forty uses shared random effects, frailties, for lifetimes. "
            "Part forty-one treats prediction at unmeasured places as imputation, and measurement error as a nugget. Part "
            "forty-four studies Brownian motion, the first Gaussian process. Part fifty-three asks how fast Gaussian "
            "process posteriors contract around the truth. And Part sixty treats predicting in a new region as a "
            "distribution shift."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The ordinary kriging variance; screening "
            "for the exponential covariance on a line; the variogram of Brownian motion; the mean of Moran's I; Ripley's K "
            "under complete randomness; and the closed form of expected improvement. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"N. Cressie, \emph{Statistics for Spatial Data} (rev. ed. 1993); \ M. Stein, \emph{Interpolation of Spatial Data} (1999)",
             r"S. Banerjee, B. Carlin \& A. Gelfand, \emph{Hierarchical Modeling and Analysis for Spatial Data} (2nd ed. 2014)",
             r"H. Rue \& L. Held, \emph{Gaussian Markov Random Fields} (2005); \ N. Cressie \& C. Wikle, \emph{Spatio-Temporal Data} (2011)",
             r"C. Rasmussen \& C. Williams, \emph{Gaussian Processes for Machine Learning} (2006); \ P. Diggle, \emph{Point Patterns} (3rd ed. 2013)"],
            [r"D. Krige (1951); \ B. Mat\'ern (1960); \ G. Matheron (1963); \ J. Besag (1974); \ B. Ripley (1976); \ N. Cressie \& D. Hawkins (1980)",
             r"A. Vecchia (1988); \ J. Sacks et al. (1989); \ J. Besag, J. York \& A. Molli\'e (1991); \ D. Jones et al. (1998); \ T. Gneiting (2002)",
             r"H. Zhang (2004); \ H. Rue et al. (2009); \ J. Hodges \& B. Reich (2010); \ C. Paciorek (2010); \ F. Lindgren et al. (2011)",
             r"A. Datta et al. (2016); \ D. Roberts et al. (2017); \ M. Heaton et al. (2019); \ M. Katzfuss \& J. Guinness (2021)"])
        with self.voiceover(
            "The books this part follows: Cressie's Statistics for Spatial Data and Stein's Interpolation; Banerjee, Carlin "
            "and Gelfand on hierarchical spatial models; Rue and Held on Markov random fields, and Cressie and Wikle on space "
            "and time; Rasmussen and Williams on Gaussian processes, and Diggle on point patterns; with the papers from "
            "Krige to Katzfuss and Guinness."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=39, current=None)
        nxt = VGroup(label(r"Part 40", font_size=30, color=GREY_B), label(r"Time to Event", font_size=48),
                     label(r"Kaplan--Meier, \ log-rank, \ Cox, \ and the traps of hazard ratios", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Thirty-nine parts of sixty-five. <bookmark mark='a'/> Near things are more related, and that is what makes "
            "prediction at unmeasured places possible, and honest only when we check it. <bookmark mark='b'/> Next, "
            "lifetimes we have not finished watching: Part forty, time to event."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(39)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
