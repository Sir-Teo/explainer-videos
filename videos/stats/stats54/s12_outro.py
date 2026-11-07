from __future__ import annotations

from videos.stats.stats54.common import *  # noqa: F403

PROBLEMS = [
    r"Show that intervals on $\mathbb R$ have VC dimension 2, \ and half-planes in $\mathbb R^2$ have VC dimension 3.",
    r"Prove the finite-class bound $\sup_h|R_n - R| \le \sqrt{\log(2K/\delta)/(2n)}$ \ from Hoeffding and a union bound.",
    r"Show $\hat{\mathfrak R}_n\{x \mapsto \langle w, x\rangle: \|w\| \le B\} \le B\sqrt{\sum\|x_i\|^2}/n$.",
    r"For realizable thresholds, \ show ERM's risk exceeds $\varepsilon$ with probability at most $2(1 - \varepsilon)^n$.",
    r"Prove Hedge's regret bound $\log K/\eta + \eta T/8$ \ with the potential $\Phi_t = \log\sum_k e^{-\eta L_{t,k}}$.",
    r"Find $\psi$ for the hinge loss: \ show conditional excess hinge risk dominates conditional 0--1 excess.",
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
            (r"Vapnik--Chervonenkis: \ shattering", CLASSC), (r"ERM and uniform convergence", TRAINC),
            (r"VC bounds; \ selection on the Board", BOUNDC), (r"Rademacher complexity, \ contraction", BOUNDC),
            (r"localization: \ fast rates", GOODC), (r"margins: \ boosting, \ SVMs", CLASSC),
            (r"PAC-Bayes and Gibbs posteriors", BOUNDC), (r"stability: \ ridge, \ SGD", TESTC),
            (r"online learning: \ Hedge, \ regret", CLASSC), (r"calibrated surrogates", TESTC),
            (r"double descent, \ benign overfitting", GOODC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 54, \ in eleven lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-four in eleven lines. Vapnik and Chervonenkis's shattering. Empirical risk "
            "minimization and uniform convergence. VC bounds, and selection on the Board. Rademacher complexity and "
            "contraction. Localization and fast rates. Margins for boosting and support vector machines. <bookmark "
            "mark='b'/> PAC-Bayes and Gibbs posteriors. Stability, for ridge regression and stochastic gradient descent. "
            "Online learning and regret. Calibrated surrogate losses. And double descent with benign overfitting."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.3), run_time=5.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(54, r"why learning generalizes, \ and where the theory runs out", r"four years of PhD courses, \ taken one at a time",
                            r"Part 55: \ the qualifying exam: \ twelve problems, \ the whole core at once")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This one explained why learning generalizes, and where the "
            "classical theory runs out. <bookmark mark='b'/> It and the eleven parts before it were taken one at a time. "
            "<bookmark mark='c'/> Part fifty-five is the qualifying exam: twelve classic problems that draw on the whole PhD "
            "core at once, each posed, paused and proved on screen."
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
            (r"the qualifying exam's learning-theory problem", [55]), (r"conformal guarantees, \ distribution-free", [57]),
            (r"online learning becomes betting: \ e-values", [58]), (r"exact risks of interpolators, \ proportional asymptotics", [59]),
            (r"generalization of foundation models", [64]),
        ], font_size=22)
        self.play(FadeIn(card.head))
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part fifty-five sets a learning-theory problem in the qualifying exam. "
            "Part fifty-seven returns to distribution-free guarantees with conformal methods. Part fifty-eight turns online "
            "learning into betting and e-values. Part fifty-nine computes the exact risks of interpolators when p and n grow "
            "together. And Part sixty-four asks what any of this says about foundation models."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Two VC dimensions; the finite-class bound; "
            "the linear class's Rademacher complexity; the realizable threshold's fast rate; Hedge's regret; and the hinge "
            "loss's psi-transform. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. Shalev-Shwartz \& S. Ben-David, \emph{Understanding Machine Learning} (2014); \ F. Bach, \emph{Learning Theory from First Principles} (2024)",
             r"M. Mohri, \ A. Rostamizadeh \& A. Talwalkar, \emph{Foundations of Machine Learning} (2018); \ M. Wainwright (2019), ch. 4, 14",
             r"V. Vapnik, \emph{Statistical Learning Theory} (1998); \ N. Cesa-Bianchi \& G. Lugosi, \emph{Prediction, Learning, and Games} (2006)"],
            [r"V. Vapnik \& A. Chervonenkis (1971); \ N. Sauer (1972); \ P. Bartlett \& S. Mendelson (2002); \ M. Ledoux \& M. Talagrand (1991)",
             r"P. Bartlett, \ O. Bousquet \& S. Mendelson (2005); \ V. Koltchinskii (2006); \ R. Schapire et al. (1998); \ D. McAllester (1999)",
             r"O. Catoni (2007); \ O. Bousquet \& A. Elisseeff (2002); \ M. Hardt, \ B. Recht \& Y. Singer (2016); \ P. Bartlett, \ M. Jordan \& J. McAuliffe (2006)",
             r"C. Zhang et al. (2017); \ M. Belkin et al. (2019); \ P. Bartlett, \ P. Long, \ G. Lugosi \& A. Tsigler (2020); \ V. Nagarajan \& Z. Kolter (2019)"])
        with self.voiceover(
            "The books this part follows: Shalev-Shwartz and Ben-David, Bach's Learning Theory from First Principles, Mohri, "
            "Rostamizadeh and Talwalkar, Wainwright, Vapnik's own book, and Cesa-Bianchi and Lugosi on prediction and games; "
            "with the papers from Vapnik and Chervonenkis to Bartlett, Long, Lugosi and Tsigler."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=54, current=None)
        nxt = VGroup(label(r"Part 55", font_size=30, color=GREY_B), label(r"The Qualifying Exam", font_size=48),
                     label(r"are you ready to do research?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Fifty-four parts of sixty-five, and the courses of the PhD core are complete. <bookmark mark='a'/> Generalization depends on the learning rule, the data distribution and the capacity it effectively uses. Uniform bounds are one route; margins, stability, PAC-Bayes and the geometry of interpolation give others. Independent evaluation remains essential when choosing among models. <bookmark mark='b'/> Next, Part fifty-five: the qualifying exam."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(54)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
