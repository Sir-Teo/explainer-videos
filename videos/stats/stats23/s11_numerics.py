from __future__ import annotations

import numpy as np

from explainer.stats.kit import ols as O
from videos.stats.stats23.common import *  # noqa: F403


class Numerics(VoiceoverScene):
    def construct(self):
        self.card()
        self.mirror()
        self.columns()
        self.routes()
        self.updating()
        self.accuracy()
        self.kappa_plot()
        self.advice()

    def card(self):
        card = chapter_card(10, r"Numerics", r"How the computer solves least squares", part=PART)
        with self.voiceover("Chapter ten. The numerics of least squares."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def mirror(self):
        u = 0.55
        c = np.array([-2.2, -0.6, 0])
        P = lambda v: c + u * np.array([v[0], v[1], 0])  # noqa: E731
        axes_ = VGroup(Line(P((-6, 0)), P((6, 0)), color=GREY_C, stroke_width=1.5), Line(P((0, -4)), P((0, 6)), color=GREY_C, stroke_width=1.5))
        a = np.array([3.0, 4.0])
        r = np.array([-5.0, 0.0])
        v = a - r
        n = np.array([-v[1], v[0]]) / np.linalg.norm(v)
        mirror = DashedLine(P(-6 * n), P(6 * n), color=PATH, stroke_width=3)
        va = Arrow(P((0, 0)), P(a), buff=0, color=OLS_C, stroke_width=5, tip_length=0.2)
        vr = Arrow(P((0, 0)), P(r), buff=0, color=GLS_C, stroke_width=5, tip_length=0.2)
        vv = DashedLine(P(a), P(r), color=GREY_B, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"blue: \ a column, \ $a = (3, 4)$", font_size=22, color=OLS_C),
            label(r"gold: \ a mirror, \ perpendicular to $v = a + \|a\| e_1$", font_size=22, color=PATH),
            label(r"teal: \ its reflection, \ $(-5, 0)$", font_size=22, color=GLS_C),
            label(r"$H = I - 2vv^\top/v^\top v$: \ orthogonal", font_size=22),
            label(r"lengths kept, \ so no error is amplified", font_size=22, color=HIT),
        ), 4.6, 0.42, [4.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The method behind QR, from Alston Householder in 1958, is a mirror. Take a column "
            "of the data, here the vector three, four. <bookmark mark='b'/> There is a mirror that reflects it onto "
            "the first axis. <bookmark mark='c'/> Its image is minus five, zero: the same length, with every "
            "component but the first zeroed. <bookmark mark='d'/> The reflection is an orthogonal matrix, the "
            "identity minus twice the projection onto v. <bookmark mark='e'/> In exact arithmetic orthogonal "
            "transformations preserve the norm of an existing error. Floating-point steps add roundoff too, but "
            "Householder QR controls it through backward stability."
        ) as vo:
            self.play(FadeIn(axes_), GrowArrow(va))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(mirror), Create(vv), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(TransformFromCopy(va, vr), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def grid(self, A, center, size=0.42):
        g = VGroup()
        n, p = A.shape
        for i in range(n):
            for j in range(p):
                zero = abs(A[i, j]) < 1e-10
                g.add(Square(side_length=size * 0.9, stroke_width=1, stroke_color=GREY_C, fill_opacity=0.9 if not zero else 0.05,
                             fill_color=OLS_C if not zero else GREY_E).move_to([j * size, -i * size, 0]))
        return g.move_to(center)

    def columns(self):
        X = np.random.Generator(np.random.PCG64(10)).normal(size=(7, 3))
        h = O.householder(X)
        grids = [self.grid(S_, [-3.0, 0.3, 0]) for S_ in h["steps"]]
        cap = VGroup(*[label(t, font_size=24, color=GREY_A).next_to(grids[0], DOWN, buff=0.35)
                       for t in (r"$X$: \ 7 $\times$ 3", r"after $H_1$", r"after $H_2 H_1$", r"$R = H_3 H_2 H_1 X$")])
        rows = fit_rows(VGroup(
            label(r"$H_1$ zeroes column 1 below the top", font_size=22),
            label(r"$H_2$ works on the rest, \ leaving row 1 alone", font_size=22),
            label(r"after $p$ reflections: \ upper triangular $R$", font_size=22, color=OLS_C),
            label(r"$Q^\top y$ comes along for free", font_size=22),
            label(r"then solve $R b = Q^\top y$ by back-substitution", font_size=22, color=HIT),
        ), 4.6, 0.42, [3.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Apply it to a whole design matrix, seven rows and three columns. The first reflection "
            "zeroes the first column below its top entry. <bookmark mark='b'/> The second works on the remaining rows and "
            "zeroes the second column below the diagonal, without disturbing the first row. <bookmark mark='c'/> After three "
            "reflections the matrix is upper triangular: R. <bookmark mark='d'/> Applying the same reflections to y gives Q "
            "transpose y. <bookmark mark='e'/> Then R b equals Q transpose y is solved from the bottom up. The normal "
            "equations never appear."
        ) as vo:
            self.play(FadeIn(grids[0]), FadeIn(cap[0]))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(Transform(grids[0], grids[k + 1]), Transform(cap[0], cap[k + 1]), FadeIn(rows[k]))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def routes(self):
        rows = [
            cmath(r"\text{Cholesky of } X^\top X", r":", r"np^2 + p^3/3 \ \text{flops}; \ \kappa^2", font_size=30),
            cmath(r"\text{Householder QR}", r":", r"2np^2 - \tfrac23 p^3; \ \kappa", font_size=30),
            cmath(r"\text{SVD}", r":", r"\text{a few times more; \ } \kappa, \ \text{and handles rank deficiency}", font_size=28),
            cmath(r"\text{rank-deficient}", r":", r"X^+ y, \ \text{the minimum-norm solution}", font_size=30),
        ]
        rows[1][2].set_color(OLS_C)
        whys = [why(r"fastest; \ squares the condition number"), why(r"twice the work, \ what \texttt{lm} does"),
                why(r"the singular values show the near-collinearity"), why(r"Part 4's pseudoinverse; \ Part 59's interpolation")]
        intro = label('Working matrix conditioning differs across numerical routes', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Three routes, at three prices. Forming X transpose X and taking its Cholesky factor is the "
            "fastest, but squares the condition number, Longley's disaster. <bookmark mark='b'/> Householder QR costs about "
            "twice as much and works with the condition number itself; it is what R's lm and most statistical software do. "
            "<bookmark mark='c'/> The singular value decomposition costs a few times more again, and shows directly which "
            "combinations of predictors are nearly missing. <bookmark mark='d'/> When the columns are exactly dependent, it "
            "gives the minimum-norm least squares solution through the pseudoinverse, which Part 59 will meet again when "
            "there are more parameters than data."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def updating(self):
        rows = [
            cmath(r"\text{a new row}", r":", r"\begin{pmatrix} R \\ x^\top \end{pmatrix} \to R' \ \text{by } p \text{ Givens rotations}", font_size=28),
            cmath(r"\text{cost}", r":", r"O(p^2) \ \text{per row, \ not } O(np^2)", font_size=30),
            cmath(r"\text{big data}", r":", r"\text{QR each chunk, \ stack the } R\text{s, \ QR again}", font_size=30),
            cmath(r"\text{deleting a row}", r":", r"\text{downdating: \ less stable}", font_size=30),
        ]
        rows[0][2].set_color(OLS_C)
        whys = [why(r"rotate the new row into $R$"), why(r"streaming least squares"), why(r"tall-skinny QR: \ one pass, \ in parallel"),
                why(r"the deletion formula's numerical twin")]
        intro = label('QR updates must carry the transformed response too', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> QR also updates well. When a new observation arrives, stack it under R, carry the "
            "transformed response alongside it, and rotate with p small Givens rotations, each mixing two rows. "
            "<bookmark mark='b'/> That costs order p squared per row, so least squares can be updated as data stream "
            "in. <bookmark mark='c'/> For data too big for one machine, factor each chunk separately, stack the small"
            " R factors together with each chunk's transformed response, and factor once more. In exact arithmetic "
            "this gives the same least-squares fit as one huge QR. <bookmark mark='d'/> Removing a row, downdating, "
            "is possible but less stable, the numerical cousin of chapter eleven's deletion formula."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def accuracy(self):
        d = load("longley")
        rows = [
            cmath(r"\text{backward stable}", r":", r"\text{the exact answer to a slightly perturbed problem}", font_size=28),
            cmath(r"\dfrac{\|\hat b - b\|}{\|b\|}", r"\lesssim", r"\kappa\,\varepsilon + \kappa^2 \varepsilon \dfrac{\|e\|}{\|X b\|}", font_size=30),
            cmath(r"\varepsilon", r"=", rf"{d['eps32']:.1e} \ \text{{(single)}}, \ {d['eps64']:.1e} \ \text{{(double)}}".replace("e-07", r"\times 10^{-7}").replace("e-16", r"\times 10^{-16}"), font_size=30),
            cmath(r"\text{Longley}", r":", r"\text{worst-case bounds can be very pessimistic}", font_size=28),
        ]
        rows[1][2].set_color(OLS_C)
        whys = [why(r"Wilkinson; \ Golub (1965)"), why(r"QR's error bound: \ Golub \& Van Loan"),
                why(r"machine epsilon"), why(r"$R^2 = 0.995$")]
        intro = label('Backward stability and forward sensitivity are different properties', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The theory is James Wilkinson's backward error analysis. Householder QR is backward"
            " stable: what it computes is the exact least squares solution for data perturbed by a few units of "
            "rounding error. <bookmark mark='b'/> The forward error is then bounded by the condition number times "
            "machine epsilon, plus a second term with the condition number squared, multiplied by how large the "
            "residuals are compared with the fit. <bookmark mark='c'/> Machine epsilon is about ten to the minus "
            "seven in single precision and two times ten to the minus sixteen in double. <bookmark mark='d'/> A good "
            "fit alone does not make the squared-condition term small: Longley's enormous condition number makes this"
            " worst-case bound very pessimistic. Observed accuracy depends on directional sensitivity and the actual "
            "rounding errors, and must be measured against the certified answer."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def kappa_plot(self):
        d = load("kappa")
        lk = np.asarray(d["logk"])
        A = axes([1, 12], [0, 16], x_length=8.0, y_length=4.4, xlabel=r"$\log_{10} \kappa(X)$", ylabel=r"correct digits",
                 xticks=[2, 4, 6, 8, 10, 12], yticks=[0, 4, 8, 12, 16], center=[-1.6, 0.3, 0])
        ax = A.ax
        ne = polyline(ax, lk, d["ne"], RES, 3.5)
        qr = polyline(ax, lk, d["qr"], OLS_C, 3.5)
        qrr = polyline(ax, lk, d["qr_resid"], PATH, 3.5)
        g1 = DashedLine(ax.c2p(1, 15), ax.c2p(12, 4), color=GREY_C, stroke_width=1.5)
        g2 = DashedLine(ax.c2p(1, 14), ax.c2p(7.5, 1), color=GREY_C, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"designs with a chosen condition number", font_size=22),
            label(r"blue: QR, near-exact fit; \ 90-digit reference", font_size=22, color=OLS_C),
            label(r"red: normal equations; \ failed solves score zero", font_size=22, color=RES),
            label(r"amber: QR with residuals; \ stronger sensitivity possible", font_size=22, color=PATH),
            label(r"dashed: \ slopes $-1$ and $-2$", font_size=22, color=GREY_C),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Sensitivity guides, compared with a seeded experiment. Build designs with condition"
            " numbers from ten to a trillion. Score each floating-point answer against a ninety-digit least-squares "
            "solution of the exact rounded inputs, not the original generating coefficients. <bookmark mark='b'/> For"
            " near-exact fits the QR results roughly follow the one-digit-per-power guide, with variation across "
            "designs. <bookmark mark='c'/> The normal equations degrade faster and can fail to factor or solve. "
            "Failed solves receive zero digits and are recorded separately. <bookmark mark='d'/> With nonzero "
            "residuals, sensitivity can include a squared-condition term, so even backward-stable QR can lose "
            "accuracy much faster. Badly conditioned problems with poor fits are hard for every method. <bookmark "
            "mark='e'/> The dashed guides have slopes minus one and minus two."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(qr), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ne), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(qrr), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(g1), Create(g2), FadeIn(rows[4]))
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"never invert $X^\top X$; \ never form it if you can avoid it", font_size=24, color=RES),
            label(r"centre and scale: \ Longley's $\kappa$ falls from $5 \times 10^9$ to 111", font_size=24, color=OLS_C),
            label(r"check $\kappa$ and the VIFs before believing the digits", font_size=24),
            label(r"single precision is back, \ on GPUs: \ Longley's lesson again", font_size=24, color=PATH),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The practical rules. Never invert X transpose X, and don't form it at all if you can avoid "
            "it. <bookmark mark='b'/> Centre and scale the predictors: Longley's condition number falls from five billion to "
            "a hundred and eleven, and even the single-precision normal equations recover three or four digits. "
            "<bookmark mark='c'/> Check the condition number and the variance inflation factors before trusting printed "
            "digits. <bookmark mark='d'/> And remember that single and even half precision are back, on the graphics "
            "processors used for machine learning: Longley's lesson is current."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
