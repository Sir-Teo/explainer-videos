from __future__ import annotations

from videos.stats.stats57.common import *  # noqa: F403


class FunctionClasses(VoiceoverScene):
    def construct(self):
        self.card()
        self.shift_view()
        self.method()
        self.compute_note()
        self.why_exact()
        self.compare()
        self.infinite()

    def card(self):
        card = chapter_card(4, r"Conditional guarantees over function classes", r"Exact coverage for every group in a family", lit=(2023,), part=PART)
        with self.voiceover("Chapter four. Conditional guarantees over function classes: exact coverage for every group in a family."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def shift_view(self):
        rows = [
            cmath(r"\text{conditional coverage}", r"\iff", r"E\big[f(X)\big(1\{Y \in C(X)\} - (1 - \alpha)\big)\big] = 0 \ \ \forall f", font_size=32),
            cmath(r"f \text{ a density ratio}", r":", r"\text{coverage under the covariate shift } dQ = f\,dP", font_size=34),
            cmath(r"f \in \mathcal F, \text{ a chosen class}", r":", r"\text{coverage under every shift in } \mathcal F", font_size=34),
            cmath(r"\mathcal F = \text{group indicators}", r":", r"\text{coverage within every group, \ overlapping allowed}", font_size=34),
        ]
        rows[2][-1].set_color(COVC)
        rows[3][-1].set_color(COVC)
        whys = [why(r"for every bounded $f$"), why(r"reweighting the test law"), why(r"Gibbs, \ Cherian \& Cand\`es"), why(r"the useful special case")]
        head = label('Shift view', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Gibbs, Cherian and Candès start from a reformulation. Conditional coverage is equivalent to the miscoverage being uncorrelated with every function of x. <bookmark mark='b'/> Each such function, if it is a density ratio, describes a covariate shift: coverage under the reweighted test distribution. <bookmark mark='c'/> Asking for all functions is impossible, as chapter three showed. Asking for a chosen class is not: coverage under every shift in that class. <bookmark mark='d'/> When the class is spanned by group indicators, that means at least nominal coverage within every prespecified group under IID sampling, even with overlap. The randomized dual version can make the moment equations exact."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def method(self):
        rows = [
            cmath(r"\hat g_S", r"=", r"\arg\min_{g \in \mathcal F} \tfrac{1}{n+1}\Big(\textstyle\sum_{i \le n}\ell_{1-\alpha}(S_i - g(X_i)) + \ell_{1-\alpha}(S - g(x))\Big)", font_size=30),
            cmath(r"C(x)", r"=", r"\{y: \ S(x, y) \le \hat g_{S(x, y)}(x)\}", font_size=36),
            cmath(r"\text{finite-dimensional } \mathcal F", r":", r"\text{an LP; \ the test dual variable is monotone in }S", font_size=34),
            cmath(r"\mathcal F = \text{constants}", r":", r"\text{split conformal, \ exactly}", font_size=36),
        ]
        rows[1][-1].set_color(COVC)
        whys = [why(r"quantile regression, \ with the test point added"), why(r"include $y$ if its score is below its own fit"), why(r"bisection on $S$"), why(r"the special case")]
        head = label('Method', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The method is quantile regression with a twist. Fit the one minus alpha quantile of the scores over the class F by minimizing the pinball loss, with the test point included at an imagined score S. <bookmark mark='b'/> The prediction set keeps every y whose score is below the fitted quantile at x, computed with that very score included. <bookmark mark='c'/> For a finite-dimensional class each fit is a linear programme, and its test-point dual variable is monotone in S. We invert that dual variable with verified brackets, which avoids treating a primal interpolation plateau as the acceptance criterion. <bookmark mark='d'/> For constants the conservative dual construction recovers the inflated empirical-quantile threshold up to numerical tolerance."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def compute_note(self):
        rows = [
            cmath(r"\text{each threshold}", r":", r"\text{one dual quantile-regression LP per candidate }S", font_size=34),
            cmath(r"\text{monotone in } S", r":", r"\text{verified brackets and dual-score bisection}", font_size=34),
            cmath(r"\text{group classes}", r":", r"\text{one threshold per pattern of group memberships}", font_size=34),
            cmath(r"\text{randomize}", r":", r"\text{to make the coverage exact rather than conservative}", font_size=34),
        ]
        rows[2][-1].set_color(COVC)
        whys = [why(r"the pinball loss"), why(r"as in our NHANES run"), why(r"few patterns, \ cheap"), why(r"as with ties")]
        head = label('Compute note', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Computing it takes one quantile regression, a linear programme, for each candidate score. <bookmark mark='b'/> Because the dual variable is monotone in the score, bracketed bisection finds the boundary. A separate geometry LP detects when every score must be accepted. <bookmark mark='c'/> For a class of group indicators, test points with the same pattern of memberships share a threshold, so the work is one bisection per pattern; that is how our NHANES calculation runs. <bookmark mark='d'/> And a small randomization makes the coverage exact instead of conservative, as with ties in chapter one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def why_exact(self):
        rows = [
            cmath(r"\text{subgradient condition}", r":", r"\textstyle\sum_{i \le n+1} f(X_i)\big(1\{S_i \le \hat g(X_i)\} - (1 - \alpha)\big) \approx 0 \ \ \forall f \in \mathcal F", font_size=30),
            cmath(r"\text{the test point}", r":", r"\text{is one of the } n + 1, \ \text{exchangeable with the rest}", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"E\big[f(X_{n+1})(1\{Y_{n+1} \in C\} - (1 - \alpha))\big] \ge 0 \ \ \forall f \ge 0 \in \mathcal F", font_size=30),
            cmath(r"\text{groups}", r":", r"P(Y \in C \mid X \in G) \ge 1 - \alpha \ \text{ for every } G", font_size=34),
        ]
        rows[3][-1].set_color(COVC)
        whys = [why(r"the subgradient of the pinball loss"), why(r"symmetry"), why(r"group slack includes its prevalence in the denominator"), why(r"exact, \ finite-sample")]
        head = label('Subgradients, symmetry and coverage', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Why is it exact? The quantile-regression first-order conditions make its subgradient residual orthogonal to the class. Points on the fitted boundary require subgradients, not an unqualified equality for binary indicators. We choose solutions symmetrically in all observations. <bookmark mark='b'/> The test point is one of those n plus one, exchangeable with the rest. <bookmark mark='c'/> So in expectation its miscoverage is orthogonal to every nonnegative function in the class, with a weighted moment error bounded by dimension over n plus one times the expected maximum weight, under conditional score continuity. Dividing by a group's probability introduces that probability in the denominator. <bookmark mark='d'/> For group indicators, that is coverage of at least one minus alpha within every group, in finite samples."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def compare(self):
        rows = [
            cmath(r"\text{Mondrian}", r":", r"\text{disjoint groups; \ simple; \ exact}", font_size=36),
            cmath(r"\text{conditional calibration}", r":", r"\text{overlapping groups, \ shifts, \ smooth functions}", font_size=34),
            cmath(r"\text{slack}", r":", r"\text{group upper slack }\frac{\dim\mathcal F}{(n+1)P(X\in G)}", font_size=36),
            cmath(r"\text{so}", r":", r"\text{a large class needs a large calibration set}", font_size=36),
        ]
        rows[1][-1].set_color(COVC)
        rows[3][-1].set_color(WEIGHTC)
        whys = [why(r"Vovk et al."), why(r"Gibbs, \ Cherian \& Cand\`es"), why(r"the price of richness"), why(r"choose $\mathcal F$ accordingly")]
        head = label('Compare', font_size=32, color=TESTPT).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Against Mondrian: Mondrian handles disjoint groups, simply and exactly. <bookmark mark='b'/> Conditional calibration handles overlapping groups, covariate shifts, and smooth classes of functions. <bookmark mark='c'/> For marginal coverage, a continuity-based upper slack is dimension over n plus one. For a group of prevalence pi it is dimension divided by n plus one times pi, capped at one. Small groups can have much larger slack. <bookmark mark='d'/> So a large class needs a large calibration set, and the class should be chosen with that budget in mind."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def infinite(self):
        rows = fit_rows(VGroup(
            label(r"for infinite classes \ (an RKHS, \ all Lipschitz shifts):", font_size=28, color=GREY_A),
            label(r"add a penalty to the quantile regression", font_size=26, color=WEIGHTC),
            label(r"coverage under each shift $f$, \ up to an error they can estimate from the data", font_size=26, color=COVC),
            label(r"a dial between marginal (constants) and the impossible (everything)", font_size=26, color=TESTPT),
            label(r"published in \emph{JRSS B} (2025)", font_size=22, color=GREY_B),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For infinite classes, such as a reproducing-kernel Hilbert space or all Lipschitz shifts, "
            "<bookmark mark='b'/> they add a penalty to the quantile regression. <bookmark mark='c'/> Coverage under each shift "
            "then holds up to an error that can be estimated from the data. <bookmark mark='d'/> The class is a dial, between "
            "marginal coverage, with only the constants, and the impossible, with every function. <bookmark mark='e'/> The paper "
            "appeared in the Journal of the Royal Statistical Society in 2025."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
