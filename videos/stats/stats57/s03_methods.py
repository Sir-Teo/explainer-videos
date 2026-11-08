from __future__ import annotations

from videos.stats.stats57.common import *  # noqa: F403


class Methods(VoiceoverScene):
    def construct(self):
        self.card()
        self.full()
        self.compare()
        self.homotopy()
        self.jackknife()
        self.proof()
        self.stable()
        self.cvplus()
        self.cost()

    def card(self):
        card = chapter_card(2, r"Full, \ split and jackknife$+$", r"Using every observation twice, \ honestly", lit=(2021,), part=PART)
        with self.voiceover("Chapter two. Full, split and jackknife plus conformal: using every observation twice, honestly."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def full(self):
        rows = [
            cmath(r"\text{for each candidate } y", r":", r"\text{refit on all } n + 1 \text{ points, \ with } (x_{n+1}, y) \text{ added}", font_size=34),
            cmath(r"S_i^y", r"=", r"|Y_i - \hat\mu^y(X_i)|, \ \ i \le n + 1", font_size=36),
            cmath(r"C(x)", r"=", r"\{y: \ S_{n+1}^y \text{ is not among the } \lfloor (n+1)\alpha \rfloor \text{ largest}\}", font_size=34),
            cmath(r"\text{cost}", r":", r"\text{a refit per candidate: \ cheap for ridge, \ lasso}", font_size=34),
        ]
        rows[2][-1].set_color(COVC)
        rows[3][-1].set_color(MISSC)
        whys = [why(r"Vovk, \ Gammerman \& Shafer (2005)"), why(r"exchangeable when $y = Y_{n+1}$"), why(r"the lemma, \ inverted"), why(r"why split conformal exists")]
        head = label('Full', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Full conformal prediction, the original form by Vladimir Vovk, Alexander Gammerman and Glenn "
            "Shafer, uses all the data for both jobs. For each candidate value y of the new outcome, refit the model on all n "
            "plus one points, with the test point labelled y. <bookmark mark='b'/> Compute every point's residual under that "
            "fit. When y is the true value, the model treats the test point exactly like the others, so the residuals are "
            "exchangeable. <bookmark mark='c'/> Keep every y whose residual is not among the largest alpha fraction: the lemma, "
            "inverted. <bookmark mark='d'/> The cost is a refit for every candidate y, affordable only for models like ridge "
            "regression or the lasso, whose fits move simply with y."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def compare(self):
        d = load("full")
        rows = fit_rows(VGroup(
            VGroup(
                label(r"Full versus split conformal: a ridge-regression experiment", font_size=36, color=WHITE),
                label(rf"ridge regression, \ $n = {d['n']}$, \ $p = {d['p']}$, \ {d['reps']} repetitions, \ $\alpha = 0.1$", font_size=26, color=GREY_A),
            ).arrange(DOWN, buff=0.2),
            label(rf"full conformal: \ coverage {100 * d['full']['coverage']:.1f}\%, \ median length {d['full']['len']:.2f}", font_size=28, color=COVC),
            label(rf"split conformal \ (20 to fit, \ 20 to calibrate): \ {100 * d['split']['coverage']:.1f}\%, \ {d['split']['len']:.2f}", font_size=28, color=CALC),
            label(rf"in this simulation, \ full is {100 * (1 - d['full']['len'] / d['split']['len']):.0f}\% shorter, \ because no data are set aside", font_size=28, color=TESTPT),
        ), 12.4, 0.6, [0, 0, 0])
        self.add(rows[0])
        with self.voiceover(
            f"<bookmark mark='a'/> A comparison: ridge regression with forty observations and five features, two hundred "
            f"repetitions. <bookmark mark='b'/> Full conformal covers {100 * d['full']['coverage']:.1f} percent, with median "
            f"length {say(d['full']['len'], 2)}. <bookmark mark='c'/> Split conformal, fitting on twenty and calibrating on "
            f"twenty, covers {100 * d['split']['coverage']:.1f} percent, with median length {say(d['split']['len'], 2)}. "
            f"<bookmark mark='d'/> Both are valid; full conformal is about {100 * (1 - d['full']['len'] / d['split']['len']):.0f} "
            f"percent shorter, because it sets no data aside."
        ) as vo:
            self.play(FadeIn(simulated_tag(r"simulated")))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def homotopy(self):
        rows = [
            cmath(r"\text{full conformal for the lasso}", r":", r"\hat\beta(y) \text{ is piecewise linear in the candidate } y", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\text{residuals are piecewise linear: \ find all breakpoints, \ exactly}", font_size=32),
            cmath(r"\text{ridge}", r":", r"\text{residuals are linear in } y: \ \text{the set is a union of intervals}", font_size=34),
            cmath(r"\text{general models}", r":", r"\text{approximate by a grid, \ or by influence functions}", font_size=34),
        ]
        rows[1][-1].set_color(COVC)
        whys = [why(r"Lei (2019)"), why(r"a homotopy, \ as in LARS"), why(r"Burnaev \& Vovk"), why(r"Part 49's tool")]
        head = label('Homotopy', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Full conformal is affordable when the fit moves simply with the candidate label. For the lasso, Jing Lei showed that the coefficients are piecewise linear in y, <bookmark mark='b'/> so the residuals are too, and the prediction set can be found exactly by tracing the breakpoints, as LARS traces the lasso path. <bookmark mark='c'/> For ridge regression, every residual is linear in y, and the set is a union of intervals found in one pass. <bookmark mark='d'/> For general models, approximate: a grid of candidates or a first-order influence-function expansion. A bare finite grid can omit tails and holes and has no exact continuum guarantee. Our ridge calculation instead solves all absolute-residual crossings analytically and retains the union of intervals."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def jackknife(self):
        rows = [
            cmath(r"R_i", r"=", r"|Y_i - \hat\mu_{-i}(X_i)|: \ \text{leave-one-out residuals}", font_size=36),
            cmath(r"\text{jackknife}", r":", r"\hat\mu(x) \pm \hat q_{1-\alpha}(R): \ \text{no guarantee}", font_size=34),
            cmath(r"\text{jackknife}+", r":", r"\big[\hat q_\alpha\{\hat\mu_{-i}(x) - R_i\}, \ \hat q_{1-\alpha}\{\hat\mu_{-i}(x) + R_i\}\big]", font_size=34),
            cmath(r"\text{guarantee}", r":", r"P(Y_{n+1} \in C) \ge 1 - 2\alpha, \ \text{for any permutation-symmetric fitting algorithm}", font_size=36),
        ]
        rows[1][-1].set_color(MISSC)
        rows[3][-1].set_color(COVC)
        whys = [why(r"$n$ fits, \ not one per candidate"), why(r"Part 34: \ fails for unstable fits"), why(r"Barber, \ Cand\`es, \ Ramdas \& Tibshirani (2021)"), why(r"and $1 - \alpha$ for stable ones")]
        head = label('Jackknife', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Between the two extremes is the jackknife: fit n models, each leaving one point out, and record each point's leave-one-out residual. <bookmark mark='b'/> The naive jackknife puts the full fit's prediction plus or minus the quantile of those residuals. It has no guarantee, and Part thirty-four showed it failing for an interpolating fit. <bookmark mark='c'/> Barber, Candès, Ramdas and Tibshirani's jackknife plus uses the leave-one-out predictions at the test point instead of the full fit, shifted by each residual. <bookmark mark='d'/> Its coverage is at least one minus two alpha for any permutation-symmetric fitting algorithm under exchangeability, using the prescribed finite-sample order statistics. Stability refinements require their additional conditions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\text{imagine}", r":", r"\text{fit on every } n - 1 \text{ of all } n + 1 \text{ points: \ } \tilde\mu_{-(i,j)}", font_size=34),
            cmath(r"A_{ij}", r"=", r"1\big\{R_{i, (-i,j)} > R_{j, (-i,j)}\big\}: \ \text{a tournament among the } n + 1", font_size=32),
            cmath(r"\text{at most}", r":", r"2\alpha(n + 1) \text{ points can lose to } (1 - \alpha)(n+1) \text{ others}", font_size=34),
            cmath(r"\text{exchangeability}", r"\Rightarrow", r"P(\text{the test point is one of them}) \le 2\alpha \qquad \blacksquare", font_size=34),
        ]
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"leave two out"), why(r"who has the larger residual"), why(r"a counting lemma"), why(r"its rank is symmetric")]
        head = label('The guarantee and its assumptions', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The proof is a tournament. Imagine fitting the algorithm on every subset of n minus one of "
            "all n plus one points, including the test point. <bookmark mark='b'/> For each pair of points, record which one "
            "has the larger residual under the fit that left both out. <bookmark mark='c'/> A counting argument shows that at "
            "most two alpha times n plus one points can each lose to one minus alpha times n plus one others. <bookmark "
            "mark='d'/> The jackknife plus interval fails only if the test point is one of these, and by exchangeability that "
            "has probability at most two alpha."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def stable(self):
        rows = [
            cmath(r"\text{stable algorithms}", r":", r"|\hat\mu(x) - \hat\mu_{-i}(x)| \le \varepsilon \text{ with high probability}", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\text{jackknife}+ \text{ covers } \ge 1 - \alpha - O(\varepsilon\text{-terms})", font_size=34),
            cmath(r"\text{and the naive jackknife}", r":", r"\text{stability refinements need inflation or continuity conditions}", font_size=34),
            cmath(r"\text{unstable}", r":", r"\text{only jackknife}+ \text{ keeps a guarantee \ (} 1 - 2\alpha \text{)}", font_size=34),
        ]
        rows[1][-1].set_color(COVC)
        rows[3][-1].set_color(MISSC)
        whys = [why(r"Part 54's stability"), why(r"Barber et al., \ Section 5"), why(r"the old method rescued"), why(r"interpolators")]
        head = label('Stable', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> For stable algorithms, those whose predictions change little when one point is left out, in Part fifty-four's sense, <bookmark mark='b'/> jackknife plus covers at least one minus alpha, minus terms that vanish with the stability parameter. <bookmark mark='c'/> Stability can justify appropriately inflated jackknife intervals or asymptotic validity under continuity conditions. A small prediction perturbation alone does not prove uninflated finite-sample coverage. <bookmark mark='d'/> Only for unstable algorithms, such as the interpolating fits of Part fifty-four, does the distinction matter, and then only jackknife plus keeps a guarantee, the weaker one minus two alpha."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cost(self):
        rows = [
            cmath(r"\text{split}", r":", r"\text{one fit; \ half the data calibrates}", font_size=36),
            cmath(r"\text{jackknife}+", r":", r"n \text{ fits; \ every point both trains and calibrates}", font_size=36),
            cmath(r"\text{CV}+, \ K \text{ folds}", r":", r"K \text{ fits; \ between the two}", font_size=36),
            cmath(r"\text{full}", r":", r"\text{one fit per candidate label, \ per test point}", font_size=36),
        ]
        rows[0][-1].set_color(CALC)
        rows[3][-1].set_color(MISSC)
        whys = [why(r"cheap, \ noisier"), why(r"n = 1{,}000: \ 1{,}000 fits"), why(r"K = 10: \ ten fits"), why(r"unless a homotopy exists")]
        head = label('Cost', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The ledger of costs. Split conformal fits once, but only half the data trains the model and the rest calibrates it, which can increase width and variability; there is no pointwise ordering against full conformal. <bookmark mark='b'/> Jackknife plus fits n times, once per left-out point, and every point both trains and calibrates: with a thousand points, a thousand fits. <bookmark mark='c'/> CV plus with K folds fits K times, ten for ten folds, and sits between them. <bookmark mark='d'/> And full conformal fits once for every candidate label at every test point, which is affordable only when a homotopy, like the lasso's, traces all the refits at once."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cvplus(self):
        rows = fit_rows(VGroup(
            label(r"Conformal methods: guarantees and computation", font_size=36, color=WHITE),
            label(r"split: \ one fit; \ $\ge 1 - \alpha$; \ wastes the calibration half", font_size=26, color=CALC),
            label(r"CV$+$: \ $K$ fits; \ $\ge 1 - 2\alpha$, \ less a small term in $K$ and $n$", font_size=26, color=CALC),
            label(r"jackknife$+$: \ $n$ fits; \ $\ge 1 - 2\alpha$", font_size=26, color=COVC),
            label(r"full: \ a fit per candidate; \ $\ge 1 - \alpha$; \ no universal length ordering", font_size=26, color=COVC),
            label(r"the trade is computation against data, \ never validity", font_size=26, color=TESTPT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The menu, then. <bookmark mark='b'/> Split conformal: one fit, coverage at least one minus alpha, but half the data wasted. <bookmark mark='c'/> Cross-validation plus: K fits, and a guarantee slightly below one minus two alpha. <bookmark mark='d'/> Jackknife plus: n fits, at least one minus two alpha. <bookmark mark='e'/> Full conformal: a fit for every candidate, at least one minus alpha, with no universal ordering of interval length. <bookmark mark='f'/> The trade is always computation against data; validity is never the price."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
