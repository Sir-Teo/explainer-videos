from __future__ import annotations

import numpy as np

from videos.stats.stats59.common import *  # noqa: F403


class RandomMatrices(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter two. Random matrix tools: the Stieltjes transform, and free convolution.", 2,
                            r"Random matrix tools", r"Spectra in closed form")
        self.stieltjes()
        self.inversion()
        self.mp_eq()
        self.moments()
        self.free_idea()
        self.free_chart()
        self.subordination()
        self.uses()

    def stieltjes(self):
        heading = label('The Stieltjes transform', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> The workhorse is the Stieltjes transform. For a probability law mu on the real "
            'line, m of z is the expectation of one over lambda minus z, for z off the real axis. <bookmark '
            "mark='b'/> For a matrix, it is the normalized trace of the resolvent, the inverse of the matrix minus "
            "z. <bookmark mark='c'/> Traces of inverses are exactly what statistics needs: the variance of least "
            "squares, the risk of ridge, the degrees of freedom of a smoother. <bookmark mark='d'/> And the "
            'transform determines the law, as the characteristic function does in Part forty-three.'
        ),
            [(r"m_\mu(z)", r"=", r"\int \frac{d\mu(\lambda)}{\lambda - z}, \ \ z \in \mathbb C^+", 40),
             (r"\text{a matrix}", r":", r"m(z) = \tfrac1p\operatorname{tr}(S - zI)^{-1}", 40),
             (r"\text{statistics}", r":", r"\text{variances, \ risks, \ degrees of freedom are traces of inverses}", 34),
             (r"\text{uniqueness}", r":", r"m \text{ determines } \mu", 40)],
            [r"the resolvent's trace", r"one line of linear algebra", r"why it matters", r"like Part 43's c.f."],
            colors=[(0, RMTC)])

    def inversion(self):
        heading = label('Density inversion, smoothing and atoms', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Stieltjes inversion recovers a density at its continuity points from the "
            "imaginary part of the transform as the imaginary argument tends to zero. <bookmark mark='b'/> At a "
            'positive imaginary argument, the result is a Cauchy-smoothed density. Atoms need separate accounting; '
            "this formula is not a finite-height plot of an atom. <bookmark mark='c'/> The Marchenko-Pastur "
            'transform solves a quadratic, with its branch chosen by positive imaginary part and the proper '
            "behavior at infinity. For ratios above one there is also an atom at zero. <bookmark mark='d'/> This "
            'converts limiting spectral laws into computable traces for statistical risk.'
        ),
            [(r"\text{density}", r"=", r"\lim_{\eta \downarrow 0}\tfrac1\pi\operatorname{Im} m(x + i\eta)", 40),
             (r"\text{in practice}", r":", r"\eta \text{ small, \ e.g. } 10^{-3}", 40),
             (r"\text{MP}", r":", r"\kappa z m^2 - (1 - \kappa - z)m + 1 = 0", 40),
             (r"\text{so}", r":", r"\text{the density from the root's imaginary part}", 38)],
            [r"Stieltjes inversion", r"numerically stable", r"a quadratic", r"Part 52"],
            colors=[(2, RMTC)])

    def mp_eq(self):
        heading = label('Leave one independent row contribution out', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Use the p by p covariance S, written as a sum of n independent row outer products "
            'divided by n. Remove one row contribution, a rank-one update, and apply Sherman-Morrison. <bookmark '
            "mark='b'/> At a fixed complex argument above the real axis, the row's quadratic form divided by n "
            "concentrates near kappa times m, not m. <bookmark mark='c'/> The trace identity gives one plus z m "
            'equal to m over one plus kappa m. Rearranging yields the displayed Marchenko-Pastur quadratic. '
            "<bookmark mark='d'/> The independence and normalization in this leave-one-row-out calculation matter. "
            'Similar resolvent and concentration ideas recur in more complicated estimation problems.'
        ),
            [(r"\text{leave one row contribution out}", r":", r"\text{Sherman--Morrison}", 40),
             (r"x_i'(S_{-i} - zI)^{-1}x_i/n", r"\approx", r"(p/n)m(z)=\kappa m(z)", 38),
             (r"\Rightarrow", r"\;", r"m = \frac{1}{1 - \kappa - z - \kappa z m}", 40),
             (r"\text{the method}", r":", r"\text{leave-one-out plus concentration}", 40)],
            [r"a rank-one update", r"Part 51's concentration", r"self-consistency", r"used again in chapter 4"],
            colors=[(2, RMTC)])

    def free_idea(self):
        heading = label('Ordinary convolution versus free convolution', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Free probability, Dan Voiculescu's theory from the 1980s, answers a harder "
            'question: what is the spectrum of a sum of two large matrices, A plus B, when their eigenvectors are '
            "in generic position? <bookmark mark='b'/> Not the convolution of their spectra: eigenvalues do not "
            "add. <bookmark mark='c'/> Instead the free convolution, computed through the R-transform, which adds "
            "the way cumulants add for independent variables. <bookmark mark='d'/> For a semicircle of variance s "
            "squared plus any matrix D, Pastur's equation gives it directly: m of z is the average over D of one "
            'over d minus z minus s squared m of z.'
        ),
            [(r"\text{question}", r":", r"\operatorname{spec}(A + B), \ \text{generic eigenvectors}", 40),
             (r"\text{not}", r":", r"\mu_A * \mu_B \ \ (\text{eigenvalues do not add})", 40),
             (r"\text{answer}", r":", r"\mu_A \boxplus \mu_B: \ \ R_{A+B} = R_A + R_B", 40),
             (r"\text{semicircle} + D", r":", r"m(z) = E_D\Big[\frac{1}{D - z - s^2 m(z)}\Big]", 38)],
            [r"Voiculescu", r"the naive guess", r"free cumulants add", r"Pastur's equation"],
            colors=[(2, RMTC), (3, RMTC)])

    def free_chart(self):
        d = load("free")
        ev = np.asarray(d["ev"])
        edges = np.linspace(-2.2, 2.2, 56)
        A = axes([-2.2, 2.2], [0, 0.6], x_length=7.4, y_length=4.4, xlabel=r"eigenvalue of $W + D$", ylabel=r"density",
                 xticks=[-2, -1, 0, 1, 2], yticks=[0, 0.25, 0.5], center=[-2.5, 0.2, 0])
        ax = A.ax
        h = histogram(ax, ev, edges, density=True, color=SIMC, opacity=0.55)
        fr = polyline(ax, d["xs"], d["dens"], RMTC, 4)
        nv = polyline(ax, d["xs"], d["naive"], CLASSC, 3)
        side = fit_rows(VGroup(
            label(rf"$W$: \ a Wigner matrix, \ $N = {d['N']:,}$, \ semicircle of variance {d['s2']:g}", font_size=22),
            label(r"$D$: \ a diagonal of random $\pm 1$", font_size=22),
            label(r"blue: \ the eigenvalues of $W + D$", font_size=22, color=SIMC),
            label(r"red: \ ordinary convolution: \ $\pm1$ plus a semicircle", font_size=22, color=CLASSC),
            label(r"teal: \ the free convolution, \ from Pastur's equation", font_size=22, color=RMTC),
        ), 4.6, 0.38, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test. W is a Wigner matrix of size {d['N']:,}, whose spectrum is a semicircle of variance a quarter. <bookmark mark='b'/> D is a diagonal of random plus and minus ones. <bookmark mark='c'/> The eigenvalues of their sum, in blue, form two bumps. <bookmark mark='d'/> The naive guess, ordinary convolution of the two spectral laws, shifts of the semicircle by plus and minus one, is wrong: the bumps are flatter, with hard edges. <bookmark mark='e'/> The free convolution, computed from Pastur's equation, matches the limiting shape. A small positive imaginary part smooths the computed density; finite matrices fluctuate."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ theory exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(h, lag_ratio=0.03), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(nv), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(fr), FadeIn(side[4]), run_time=2.0)
        self.clear_scene()

    def subordination(self):
        heading = label("Pastur's fixed-point equation", font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Why does Pastur's equation work? Adding a semicircle of variance s squared shifts "
            "the argument of D's resolvent by s squared times m: the subordination idea. <bookmark mark='b'/> Then "
            'm is the Stieltjes transform of D, evaluated at the shifted point, and it must agree with itself: a '
            "fixed point. <bookmark mark='c'/> Solving it at each x slightly above the axis, by damped iteration, "
            "gives the density. <bookmark mark='d'/> The same structure, a transform evaluated at a "
            "self-consistently shifted point, appears in ridge regression's risk and in the deterministic "
            'equivalents of chapter eight.'
        ),
            [(r"\text{subordination}", r":", r"m_{W+D}(z) = m_D\big(z + s^2 m_{W+D}(z)\big)", 38),
             (r"\text{a fixed point}", r":", r"\text{in } m, \ \text{at each } z", 40),
             (r"\text{compute}", r":", r"\text{damped iteration at } z = x + i\eta", 40),
             (r"\text{again in}", r":", r"\text{ridge risk; \ random features}", 40)],
            [r"Biane; \ Voiculescu", r"self-consistency", r"as in the chart", r"chapters 3 and 8"],
            colors=[(0, RMTC)])

    def uses(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> What these tools buy statistics. <bookmark mark='b'/> The spectrum of a sample "
            "covariance, and so the bias of its eigenvalues, which Part fifty-two's shrinkage corrected. <bookmark "
            "mark='c'/> Traces of inverses, and so the exact variance and risk of linear estimators. <bookmark "
            "mark='d'/> Sums and products of matrices, and so models with structured noise. <bookmark mark='e'/> "
            'But not nonlinear estimators, such as the logistic MLE or the lasso: for those we need the next three '
            'tools.'
        ),
            [(r"what random matrices buy:", GREY_A),
             (r"sample-covariance spectra, \ and their bias", RMTC),
             (r"traces of inverses: \ exact risks of linear estimators", RMTC),
             (r"sums and products of matrices: \ structured noise", RMTC),
             (r"not nonlinear estimators: \ for those, \ AMP, \ Gordon, \ replicas", AMPC)])

    def moments(self):
        heading = label('MP moments under isotropy', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Some moments of the Marchenko–Pastur law, as a check. Its mean is one: on "
            "average, eigenvalues are right. <bookmark mark='b'/> Its variance is kappa: at kappa a half, the "
            "eigenvalues spread with standard deviation 0.71 around one. <bookmark mark='c'/> The mean of the "
            "inverse is one over one minus kappa, two at a half, which is least squares' inflation. <bookmark "
            "mark='d'/> And the largest eigenvalue is near one plus root kappa squared, 2.91 at a half, against the "
            'truth of one: the limiting top eigenvalue exceeds one in this isotropic proportional model, which is '
            'why Part fifty-two shrank it.'
        ),
            [('\\int x\\,d\\mu', '=', '1', 40),
             ('\\mathrm{Var}', '=', '\\kappa: \\ \\text{SD } 0.71 \\text{ at } \\kappa = 0.5', 40),
             ('\\int x^{-1}\\,d\\mu', '=', '1/(1 - \\kappa) = 2', 40),
             ('\\lambda_{\\max}', '\\to', '(1 + \\sqrt\\kappa)^2 = 2.91', 40)],
            ['unbiased on average', 'spread', 'inflation', "Part 52's shrinkage"],
            colors=[(3, CLASSC)])
