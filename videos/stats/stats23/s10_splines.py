from __future__ import annotations

import numpy as np

from videos.stats.stats23.common import *  # noqa: F403

KCOL = {"1": BLUE, "3": TEAL, "6": PATH, "20": RED}


class Splines(VoiceoverScene):
    def construct(self):
        self.card()
        self.bases()
        self.basis_picture()
        self.fits()
        self.cv()
        self.varying()
        self.natural()

    def card(self):
        card = chapter_card(9, r"Splines and bases", r"Curves are linear models too", part=PART)
        with self.voiceover("Chapter nine. Splines and bases."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bases(self):
        d = load("splines")
        rows = [
            cmath(r"y", r"=", r"\textstyle\sum_j \beta_j b_j(x) + \varepsilon", font_size=30),
            cmath(r"\text{truncated powers}", r":", r"1, x, x^2, x^3, (x - k_1)_+^3, \dots", font_size=30),
            cmath(r"\text{B-splines}", r":", r"\text{the same space; \ local bumps that sum to one}", font_size=30),
            cmath(r"\kappa", r":", rf"{d['cond_tp']:.1e} \ \text{{vs}} \ {d['cond_bs']:.1f}".replace("e+07", r"\times 10^7"), font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"linear in $\beta$, \ whatever the $b_j$"), why(r"a cubic that may bend at each knot"),
                why(r"de Boor (1972)"), why(r"chapter ten: \ the basis matters to the computer")]
        intro = label('A linear model can use nonlinear functions of its predictors', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> A linear model only has to be linear in its coefficients. Replace x by any set of "
            "basis functions of x, and least-squares algebra still applies. Exact F-tests need the Gaussian "
            "homoskedastic model and fixed basis choice; robust inference needs its own sampling and moment "
            "conditions. Selecting bases using y adds selection uncertainty. <bookmark mark='b'/> A cubic spline is a"
            " cubic polynomial allowed to change at chosen knots, staying smooth. The obvious basis adds a truncated "
            "cube at each knot. <bookmark mark='c'/> B-splines, from Carl de Boor's recursion, span exactly the same "
            "functions, but each is a local bump, and together they sum to one. <bookmark mark='d'/> They're far "
            "better for the computer: with three knots on ages, the truncated-power design has condition number "
            "thirty million; the B-spline design, under six."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def basis_picture(self):
        d = load("splines")
        gr = np.asarray(d["grid"])
        B = np.asarray(d["basis"])
        A = axes([18, 85], [0, 1.05], x_length=8.0, y_length=4.0, xlabel=r"age", ylabel=r"$b_j(x)$",
                 xticks=[20, 33, 44, 61, 85], yticks=[0, 0.5, 1], center=[-1.6, 0.4, 0])
        ax = A.ax
        cols = [BLUE, TEAL, PATH, GLS_C, RED, PROG, GREY_A]
        curves = VGroup(*[curve(ax, gr, B[j], cols[j % len(cols)], 3) for j in range(B.shape[0])])
        knots = VGroup(*[DashedLine(ax.c2p(k, 0), ax.c2p(k, 1.0), color=GREY_C, stroke_width=1.5) for k in d["knots3"]])
        total = curve(ax, gr, B.sum(0), WHITE, 2)
        rows = fit_rows(VGroup(
            label(r"7 cubic B-splines, \ knots at 33, 44, 61", font_size=22),
            label(r"each lives on at most four intervals", font_size=22, color=GREY_A),
            label(r"white: \ their sum, \ exactly 1", font_size=22),
            label(r"so $X^\top X$ is banded: \ cheap and stable", font_size=22, color=HIT),
        ), 3.45, 0.42, [5.1, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are the seven cubic B-splines for knots at ages thirty-three, forty-four and "
            "sixty-one, the quartiles of a sample. <bookmark mark='b'/> Each is non-zero over at most four "
            "neighbouring intervals. <bookmark mark='c'/> At every age they add up to exactly one. <bookmark "
            "mark='d'/> Only neighbouring B-spline basis functions overlap in predictor space, so their Gram matrix "
            "is banded. This design is well conditioned, but poorly spaced knots or rank deficiency can still cause "
            "numerical trouble."
        ) as vo:
            self.play(FadeIn(A), Create(knots))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(total), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def fits(self):
        d = load("splines")
        age, inc = np.asarray(d["age"]), np.asarray(d["inc"])
        gr = np.asarray(d["grid"])
        A = axes([18, 85], [9, 12.5], x_length=8.0, y_length=4.4, xlabel=r"age", ylabel=r"log income",
                 xticks=[20, 30, 40, 50, 60, 70, 80], yticks=[9, 10, 11, 12], center=[-1.6, 0.3, 0])
        ax = A.ax
        keep = (inc > 9) & (inc < 12.5)
        dots = VGroup(*[Dot(ax.c2p(a + 0.3 * np.sin(7 * b), b), radius=0.025, color=GREY_C, fill_opacity=0.5)
                        for a, b in zip(age[keep], inc[keep])])
        truth = polyline(ax, d["ages"], d["truth"], TRUE, 3)
        cvs = {k: curve(ax, gr, v["curve"], KCOL[k], 3) for k, v in d["fits"].items()}
        rows = fit_rows(VGroup(
            label(r"800 of the World's adults, \ log income", font_size=22),
            label(r"gold: \ the true mean at each age", font_size=22, color=TRUE),
            label(r"1 knot: \ too stiff for the drop at 67", font_size=22, color=KCOL["1"]),
            label(r"3 and 6 knots: \ close to the truth", font_size=22, color=KCOL["6"]),
            label(r"20 knots: \ chasing noise", font_size=22, color=KCOL["20"]),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fit log income against age for eight hundred of the World's adults. <bookmark mark='b'/> "
            "The World's true mean rises, levels off and steps down at retirement. <bookmark mark='c'/> One knot gives a "
            "smooth curve that can't follow the drop. <bookmark mark='d'/> Three or six knots, placed at sample quantiles, "
            "track the truth closely. <bookmark mark='e'/> Twenty knots wiggle: each piece is fitted to a handful of "
            "people."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cvs["1"]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(cvs["3"]), Create(cvs["6"]), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(cvs["20"]), FadeIn(rows[4]))
        self.clear_scene()

    def cv(self):
        d = load("splines")
        cv = np.asarray(d["cv"])
        K = np.arange(len(cv))
        lo, hi = float(cv.min()) - 0.002, float(cv.max()) + 0.002
        A = axes([0, 25], [lo, hi], x_length=8.0, y_length=4.2, xlabel=r"number of interior knots",
                 ylabel=r"10-fold CV error", xticks=[0, 5, 10, 15, 20, 25], yticks=np.linspace(lo, hi, 4), center=[-1.6, 0.3, 0],
                 yfmt=lambda v: f"{v:.3f}")
        ax = A.ax
        pl = VGroup(polyline(ax, K, cv, PATH, 3), *[Dot(ax.c2p(k, c), radius=0.05, color=PATH) for k, c in zip(K, cv)])
        b = d["best_K"]
        best = Dot(ax.c2p(b, cv[b]), radius=0.1, color=HIT)
        rows = fit_rows(VGroup(
            label(r"choosing the knots by cross-validation", font_size=22),
            label(rf"minimum at {b} knots", font_size=22, color=HIT),
            label(r"nearby errors need not identify a unique best shape", font_size=22, color=GREY_A),
            label(rf"one-SE rule: {d['oneSE_K']} knots (fold-SE heuristic)", font_size=22),
            label(r"Part 29: \ penalize instead of choosing", font_size=22, color=TEAL),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How many knots? Part 19's answer: cross-validate. Ten-fold prediction error for "
            "zero to twenty-five knots. <bookmark mark='b'/> The displayed minimum is the computed value for this "
            "split; every fold learns its knots from training predictors alone. <bookmark mark='c'/> But look at the "
            "scale: many choices have very similar prediction errors. <bookmark mark='d'/> Individual incomes vary so"
            " much around the curve that its fine shape hardly changes the prediction error; we compute the "
            "one-standard-error choice shown here. The standard error across ten correlated fold losses is a "
            "heuristic, not an exact confidence interval. <bookmark mark='e'/> Choosing knots is awkward and "
            "unstable. Part 29 instead uses many knots and penalizes roughness, choosing one smoothing parameter."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(pl), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(best), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def varying(self):
        rows = [
            cmath(r"y", r"=", r"\textstyle\sum_j \beta_j b_j(\text{age}) + \sum_j \gamma_j b_j(\text{age})\cdot \text{female}", font_size=28),
            cmath(r"H_0", r":", r"\gamma_1 = \dots = \gamma_K = 0", font_size=30),
            cmath(r"\text{two curves}", r":", r"b_j(x) b_k(z): \ \text{tensor products}", font_size=30),
            cmath(r"\text{the catch}", r":", r"K \text{ per curve; \ } K^2 \text{ per surface}", font_size=30),
        ]
        rows[1][2].set_color(OLS_C)
        whys = [why(r"a separate age curve for women"), why(r"one $F$-test: \ do the curves differ?"),
                why(r"surfaces in two variables"), why(r"the curse of dimensionality: \ Part 29")]
        intro = label('Interactions between bases build curves and surfaces', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Bases compose. Multiply the age basis by an indicator for women and the model has two "
            "age curves, one for each sex. <bookmark mark='b'/> Whether the curves differ is a single general linear "
            "hypothesis, all the interaction coefficients zero, tested with chapter two's F. <bookmark mark='c'/> Products of "
            "two bases make surfaces in two variables. <bookmark mark='d'/> The catch is the count: K columns for a curve, "
            "K squared for a surface, K cubed for three variables. Part 29 meets this curse of dimensionality."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def natural(self):
        rows = [
            cmath(r"\text{natural cubic spline}", r":", r"\text{linear beyond the boundary knots}", font_size=30),
            cmath(r"\text{degrees of freedom}", r":", r"J\ \text{interior knots}\Rightarrow J+2\ \text{columns incl. intercept}", font_size=30),
            cmath(r"\text{tests}", r":", r"\text{is the curve linear? \ an } F\text{-test, \ chapter two}", font_size=30),
            cmath(r"\text{Part 20}", r":", r"\text{restricted cubic splines for age}", font_size=30),
        ]
        rows[0][2].set_color(PATH)
        whys = [why(r"tames the wild ends of a cubic"), why(r"zero second derivative at each boundary"),
                why(r"nonlinear columns $= 0$"), why(r"the same object, \ Harrell's name")]
        intro = label('Natural cubic splines impose two boundary curvature constraints', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Cubic splines misbehave at the ends, where data are thin. A natural cubic spline is"
            " forced to be a straight line beyond the outer knots. <bookmark mark='b'/> With J distinct interior "
            "knots and two fixed boundary knots, imposing zero second derivative at the boundaries removes two "
            "degrees of freedom from the unrestricted cubic spline. The natural basis has J plus two columns, "
            "including the intercept. <bookmark mark='c'/> Whether the curve is needed at all is then a general "
            "linear hypothesis: test that the nonlinear columns' coefficients are all zero, with chapter two's F. "
            "<bookmark mark='d'/> These are the restricted cubic splines Part 20 used for age in its blood-pressure "
            "model."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
