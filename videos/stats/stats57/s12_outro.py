from __future__ import annotations

from videos.stats.stats57.common import *  # noqa: F403

PROBLEMS = [
    r"Show that with $n+1$ exchangeable almost surely distinct scores, \ $P(S_{n+1} \le S_{(k)}) = k/(n+1)$ \ exactly.",
    r"Show that the coverage of split conformal for IID continuous scores, \ given calibration, \ is Beta$(k, n + 1 - k)$.",
    r"For the Bahadur--Savage family, \ show the $t$-interval's coverage is at most $1-(1-\varepsilon)^n+(1-\varepsilon)^n c_n$, \ where $c_n$ is the no-atom coverage.",
    r"Show that ACI's average miss rate satisfies $|\bar e_T - \alpha| \le (\max(\alpha_1, 1 - \alpha_1) + \gamma)/(\gamma T)$.",
    r"Show that Mondrian conformal gives coverage $\ge 1 - \alpha$ within every group of a partition.",
    r"Prove conformal risk control: \ $E L_{n+1}(\hat\lambda) \le \alpha$ for losses in $[0, B]$, \ nonincreasing in $\lambda$.",
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
            (r"Bahadur--Savage: \ no free mean", MISSC), (r"the quantile lemma, \ exact to $1/n$", COVC),
            (r"coverage given the calibration set: \ Beta", CALC), (r"full, \ split, \ jackknife$+$, \ CV$+$", CALC),
            (r"no conditional coverage without infinite length", MISSC), (r"functional-specific limits; \ quantiles remain possible", MISSC),
            (r"coverage over a function class", COVC), (r"weighted and nonexchangeable conformal", WEIGHTC),
            (r"online: \ ACI for every sequence", WEIGHTC), (r"outliers and risk control", COVC),
            (r"groups on NHANES; \ six open problems", S.ACCENT),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 57, \ in eleven lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-seven in eleven lines. No informative finite-width uniformly honest mean interval exists over all finite-mean distributions. The quantile lemma makes prediction exact to within one over n. For IID continuous scores, coverage conditional on the calibration set has a Beta law. Full, split, jackknife plus and cross-validation plus trade computation for data. Conditional coverage needs infinite intervals, while the possibility of parameter confidence intervals depends on the functional; marginal quantiles are possible. <bookmark mark='b'/> Coverage over a chosen function class is possible, and exact. Weights carry the guarantee beyond exchangeability. Online, ACI controls the miss rate for every sequence. The same lemma tests for outliers and controls risks. And on NHANES, every named group can be covered at once."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.5), run_time=12.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.5), run_time=10.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(57, r"guarantees for a sample of fixed size", r"you look at the data once, \ at the end",
                            r"Part 58: \ inference that stays valid whenever you look")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. The rank-based interval guarantees concern a fixed sample; the ACI chapter separately controls a long-run error frequency. <bookmark mark='b'/> Those confidence statements do not yet provide simultaneous validity over every stopping time. <bookmark mark='c'/> Part fifty-eight builds inference that stays valid however often you look, and lets you stop when you like."
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
            (r"e-values and test martingales", [58]), (r"conformal under proportional asymptotics", [59]),
            (r"prediction for causal effects", [62]), (r"uncertainty for foundation models", [64]),
            (r"the dissertation's predictive claims", [65]),
        ], font_size=22)
        self.play(FadeIn(card.head))
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part fifty-eight's e-values and test martingales. Part fifty-nine's "
            "conformal inference when p and n grow together. Part sixty-two's prediction intervals for individual causal "
            "effects. Part sixty-four's uncertainty for foundation models. And the predictive claims of the dissertation."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The lemma's exact coverage; the Beta law; the "
            "Bahadur–Savage bound; ACI's guarantee; Mondrian coverage; and conformal risk control. Pause here if you want to try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"A. Angelopoulos, \ R. Foygel Barber \& S. Bates, \ \emph{Theoretical Foundations of Conformal Prediction} (2024)",
             r"V. Vovk, \ A. Gammerman \& G. Shafer, \emph{Algorithmic Learning in a Random World} (2005; 2nd ed. 2022)",
             r"A. Angelopoulos \& S. Bates, \ \emph{A Gentle Introduction to Conformal Prediction} (2021)"],
            [r"R. R. Bahadur \& L. J. Savage, \ \emph{Ann. Math. Stat.} (1956); \ J. Lei \& L. Wasserman, \ \emph{JRSS B} (2014); \ V. Vovk (2012)",
             r"R. Foygel Barber, \ E. Cand\`es, \ A. Ramdas \& R. Tibshirani, \ \emph{Ann. Stat.} (2021, \ 2023), \ \emph{IMA} (2021); \ R. Barber (2020)",
             r"I. Gibbs, \ J. Cherian \& E. Cand\`es, \ \emph{JRSS B} (2025); \ I. Gibbs \& E. Cand\`es, \ NeurIPS (2021); \ R. Tibshirani et al. (2019)",
             r"S. Bates et al., \ \emph{Ann. Stat.} (2023); \ A. Angelopoulos et al., \ ICLR (2024); \ CDC/NCHS, \ NHANES 2017--18"])
        with self.voiceover(
            "The books behind this part: Angelopoulos, Barber and Bates's theoretical foundations; Vovk, Gammerman and "
            "Shafer's original book; and Angelopoulos and Bates's gentle introduction; with the papers from Bahadur and Savage "
            "to Gibbs, Cherian and Candès."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=57, current=None)
        nxt = VGroup(label(r"Part 58", font_size=30, color=GREY_B), label(r"Anytime-Valid Inference", font_size=48),
                     label(r"what if you look at the data every day, \ and choose what to collect as you go?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Fifty-seven parts of sixty-five. <bookmark mark='a'/> In 1943 a Navy captain complained to the Statistical "
            "Research Group at Columbia that ordnance tests ran long after the answer was obvious, and Abraham Wald invented the "
            "sequential probability ratio test. <bookmark mark='b'/> Next, Part fifty-eight: anytime-valid inference and "
            "adaptive experiments."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(57)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
