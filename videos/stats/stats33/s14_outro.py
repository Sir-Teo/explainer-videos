from __future__ import annotations

from videos.stats.stats33.common import *  # noqa: F403

PROBLEMS = [
    r"Show that Holm's procedure controls the FWER at $\alpha$ under any dependence.",
    r"Prove that BH's FDR equals $\pi_0 q$ for independent, \ continuous, \ uniform null $p$-values.",
    r"Show that BH at level $q/\sum_{i=1}^m 1/i$ controls the FDR under arbitrary dependence \ (bound $\mathbf 1\{p \le qk/m\}/k$).",
    r"Show that Storey's $\hat\pi_0(\lambda)$ has expectation $\ge \pi_0$.",
    r"For a null $j$, \ show $\mathrm{sign}(W_j)$ is a fair coin independent of $|W_j|$ for knockoffs.",
    r"Derive Ioannidis's PPV with bias $u$, \ and find the prior below which $\mathrm{PPV} < 1/2$ for power 0.8.",
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
            (r"a dead salmon `responds'", SIGC), (r"5{,}000 genes: \ half the uncorrected list is noise", FALSEC),
            (r"Bonferroni, \ Holm, \ closed testing, \ Westfall--Young", FWC), (r"BH: \ 184 discoveries, \ 10\% false", BHC),
            (r"Storey's $\pi_0$ and $q$-values", BHC), (r"Efron: \ local fdr, \ the empirical null", BHC),
            (r"FDR is an average: \ dependence spreads the FDP", BYC), (r"knockoffs: \ a coin flip controls the FDR", BHC),
            (r"forking paths: \ 61\% false positives", FALSEC), (r"replication: \ 36\%; \ effects halved", FALSEC),
            (r"publication bias: \ funnels, \ Egger, \ $p$-curves", SIGC), (r"FCR: \ widen the selected intervals", BHC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 33, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part thirty-three in twelve lines. <bookmark mark='a'/> A dead salmon responded to photographs because thousands "
            "of voxels were tested without correction. In the World's five thousand genes, half the uncorrected list was "
            "noise. Bonferroni, Holm, closed testing and Westfall and Young control the chance of any false discovery, and "
            "find a fifth of the real genes. Benjamini and Hochberg control the share of false discoveries instead, and "
            "find three times as many. Storey estimates the share of nulls; Efron estimates the null itself, and the local "
            "false discovery rate of each gene. The false discovery rate is only an average, and dependence spreads the "
            "proportion widely. Knockoffs control it for any selection method by a coin-flip argument. Forking paths turn a "
            "five percent error rate into sixty-one. Replication rates near a third and effects halved are what selection "
            "predicts. Funnels, Egger's test and p-curves detect a filtered literature. And intervals for selected effects "
            "must be widened to keep their promise."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(33, r"control the error rate of a list: \ FWER, \ FDR, \ FCR",
                            r"the hypotheses and the selection rule were fixed before the data",
                            r"Part 56: \ inference when the questions themselves are chosen by looking: \ PoSI, \ selective inference, \ data splitting")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part controlled the error rates of lists: family-wise, false "
            "discovery and false coverage. <bookmark mark='b'/> It assumed that the family of hypotheses and the selection "
            "rule were fixed before the data arrived. <bookmark mark='c'/> Part 56 drops that: inference when the questions "
            "themselves are chosen by looking at the data."
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
            (r"conformal prediction's exchangeability", [34]), (r"many outcomes in one trial", [35]),
            (r"multiple imputation's inflated tests", [41]), (r"Neyman--Pearson for many hypotheses", [46]),
            (r"minimax testing; \ higher criticism", [50]), (r"selective inference and PoSI", [56]),
            (r"e-values: \ FDR at any stopping time", [58]), (r"genomics-scale causal discovery", [62]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 34's conformal prediction rests on the exchangeability that made "
            "knockoffs work. Part 35 handles many outcomes in one trial. Part 41 meets multiplicity in imputation. Part 46 "
            "extends Neyman and Pearson to many hypotheses. Part 50 asks when sparse signals can be detected at all, with "
            "higher criticism. Part 56 develops selective inference. Part 58's e-values control the false discovery rate at "
            "any stopping time. And Part 62 tests thousands of causal hypotheses at once."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Holm under any dependence; BH's exact "
            "false discovery rate; the Benjamini–Yekutieli bound; Storey's conservative estimate; the knockoff coin flip; "
            "and Ioannidis's formula. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"B. Efron, \emph{Large-Scale Inference} (2010)",
             r"P. Westfall \& S. Young, \emph{Resampling-Based Multiple Testing} (1993)",
             r"S. Dudoit \& M. van der Laan, \emph{Multiple Testing Procedures with Applications to Genomics} (2008)",
             r"M. Borenstein, L. Hedges, J. Higgins \& H. Rothstein, \emph{Introduction to Meta-Analysis} (2009)"],
            [r"Y. Benjamini \& Y. Hochberg (1995); \ Y. Benjamini \& D. Yekutieli (2001, 2005); \ S. Holm (1979); \ J. Storey (2002, 2003)",
             r"R. Marcus, E. Peritz \& K. Gabriel (1976); \ R. Simes (1986); \ Y. Hochberg (1988); \ B. Efron (2004, 2007)",
             r"R. Barber \& E. Cand\`es (2015); \ E. Cand\`es, Y. Fan, L. Janson \& J. Lv (2018); \ C. Bennett et al. (2010)",
             r"J. Ioannidis (2005); \ J. Simmons, L. Nelson \& U. Simonsohn (2011); \ Open Science Collaboration (2015); \ M. Egger et al. (1997)"])
        with self.voiceover(
            "The books this part follows: Efron's Large-Scale Inference; Westfall and Young on resampling-based multiple "
            "testing; Dudoit and van der Laan for genomics; and the Introduction to Meta-Analysis; with the papers from "
            "Holm to the Open Science Collaboration."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=33, current=None)
        nxt = VGroup(label(r"Part 34", font_size=30, color=GREY_B), label(r"Prediction with Guarantees", font_size=48),
                     label(r"can a black box give honest uncertainty?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Thirty-three parts of sixty-five. <bookmark mark='a'/> We can ask thousands of questions and still say how many "
            "of our answers are likely wrong. <bookmark mark='b'/> Knockoffs controlled errors without trusting any model "
            "for the outcome, using only exchangeability. Part 34 asks how far that goes: can a black-box predictor, a "
            "forest or a neural network, come with honest uncertainty? Prediction with guarantees."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(33)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
