from __future__ import annotations

import numpy as np

from videos.stats.stats23.common import *  # noqa: F403

SHORT = [r"intercept", r"GNP deflator", r"GNP", r"unemployed", r"armed forces", r"population", r"year"]


class Hook(VoiceoverScene):
    def construct(self):
        self.longley()
        self.data()
        self.digits()
        self.why_digits()
        self.objectives()

    def longley(self):
        tl = timeline(lit=(1967,)).to_edge(UP, buff=0.35)
        hc = history_card(1967, r"James W. Longley, \ US Bureau of Labor Statistics",
                          r"``An appraisal of least squares programs for the electronic computer from the point of view of "
                          r"the user'': \ sixteen years of employment data, \ seven coefficients, \ run through the "
                          r"regression programs of the day. \ Many printed answers with hardly a digit right",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"the programs did nothing wrong in algebra", font_size=24),
            label(r"they solved the right equations the wrong way", font_size=24, color=RES),
        ), 12.0, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1967 James Longley, an economist at the US Bureau of Labor Statistics, published a "
            "warning in the Journal of the American Statistical Association. He had taken sixteen years of American "
            "economic data, a regression with seven coefficients, and run it through the least squares programs of the day. "
            "Many printed answers with hardly a correct digit. <bookmark mark='b'/> The programs did nothing wrong in "
            "algebra. <bookmark mark='c'/> They solved the right equations the wrong way."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def data(self):
        d = load("longley")
        X, y = np.asarray(d["X"]), np.asarray(d["y"])
        hdr = [r"\textbf{year}", r"\textbf{employed}", r"\textbf{GNP defl.}", r"\textbf{GNP}", r"\textbf{unemployed}",
               r"\textbf{armed}", r"\textbf{population}"]
        body = []
        for i in (0, 1, 2, 7, 14, 15):
            body.append([f"{X[i, 6]:.0f}", f"{y[i]:,.0f}", f"{X[i, 1]:.1f}", f"{X[i, 2]:,.0f}", f"{X[i, 3]:,.0f}",
                         f"{X[i, 4]:,.0f}", f"{X[i, 5]:,.0f}"])
        body.insert(3, [r"$\vdots$"] * 7)
        t = table_rows([hdr] + body, font_size=22, col_buff=0.5, row_buff=0.22, colors=[GREY_A] + [None] * 7)
        t.move_to([0, 1.3, 0])
        C = np.asarray(d["corr"])
        vif = d["vif"]
        foot = fit_rows(VGroup(
            label(rf"corr(GNP, year) $= {C[1, 5]:.3f}$; \ corr(GNP, population) $= {C[1, 4]:.3f}$", font_size=24),
            label(rf"variance inflation factors up to {max(vif):,.0f}", font_size=24, color=RES),
            label(r"NIST later certified the answer to 15 digits", font_size=24, color=HIT),
        ), 12.0, 0.32, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are Longley's data: total employment from 1947 to 1962, with six predictors, the "
            "price deflator, gross national product, unemployment, the size of the armed forces, the population, and the "
            "year itself. <bookmark mark='b'/> They are almost the same variable six times over: GNP and the year are "
            "correlated point nine nine five, GNP and population point nine nine one. <bookmark mark='c'/> One variance "
            "inflation factor, Part 12's measure of collinearity, is nearly eighteen hundred. <bookmark mark='d'/> Decades "
            "later the US National Institute of Standards and Technology certified the right answer to fifteen digits, so "
            "we can grade any method against it."
        ) as vo:
            self.add(longley_tag())
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in t], lag_ratio=0.15), run_time=2.0)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k]))
        self.clear_scene()

    def digits(self):
        d = load("longley")
        methods = [r"normal eq., \ single", r"QR, \ single", r"normal eq., \ double", r"QR, \ double"]
        dig = [d["ne32_digits"], d["qr32_digits"], d["ne64_digits"], d["qr64_digits"]]
        b = DigitsBoard(SHORT, methods, dig, cell_w=2.35, row_h=0.56, font_size=21, center=[0, 0.55, 0])
        b.scale_to_fit_width(min(b.width, 13.0))
        head = label(r"correct significant digits, \ against NIST's certified values", font_size=26).to_edge(UP, buff=0.35)
        foot = fit_rows(VGroup(
            label(r"single precision: \ about 7 digits to work with; \ double: \ about 16", font_size=22, color=GREY_A),
            label(r"the normal equations in single precision: \ not one digit, \ several signs wrong", font_size=22, color=RES),
        ), 12.0, 0.25, [0, -2.75, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Let's repeat Longley's test. Each bar counts the correct significant digits of a "
            "coefficient, out of fifteen. <bookmark mark='b'/> First the textbook formula, solving the normal equations X "
            "transpose X b equals X transpose y, in single precision, about seven digits, roughly what many machines of the "
            "sixties used. The matrix isn't even recognizably positive definite any more, the Cholesky factorization fails, "
            "and plain elimination returns numbers with no correct digits at all; several have the wrong sign. "
            "<bookmark mark='c'/> The same precision with a QR decomposition, Part 4's method, gets five or six digits right. "
            "<bookmark mark='d'/> In double precision the normal equations manage seven or eight, <bookmark mark='e'/> and "
            "QR eleven to thirteen. The arithmetic was the same; the route through it decided the answer."
        ) as vo:
            self.add(longley_tag())
            self.play(FadeIn(head), FadeIn(b.names))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(b.column(0)), FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
            for j, m_ in zip((1, 2, 3), "cde"):
                vo.wait_until(m_)
                self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in b.column(j)], lag_ratio=0.05))
        self.clear_scene()

    def why_digits(self):
        d = load("longley")
        rows = [
            cmath(r"\kappa(X)", r"=", rf"\sigma_{{\max}}/\sigma_{{\min}} \approx {d['cond_X'] / 1e9:.1f} \times 10^9", font_size=30),
            cmath(r"\kappa(X^\top X)", r"=", r"\kappa(X)^2 \approx 2.4 \times 10^{19}", font_size=30),
            cmath(r"\text{digits lost}", r"\approx", r"\log_{10} \kappa: \ \ \text{QR loses } 10, \ \text{the normal equations } 19", font_size=28),
            cmath(r"\text{centre and scale}", r":", rf"\kappa = {d['cond_scaled']:.0f}", font_size=30),
        ]
        rows[1][2].set_color(RES)
        whys = [why(r"the condition number: \ Part 4"), why(r"forming $X^\top X$ squares it"),
                why(r"single precision has 7; \ double has 16"), why(r"chapter ten: \ numerics")]
        with self.voiceover(
            "<bookmark mark='a'/> Why? The condition number of the design matrix, the ratio of its largest to smallest "
            "singular value, is about five billion: some direction in the data is almost not there. <bookmark mark='b'/> "
            "Forming X transpose X squares it, to about two times ten to the nineteen. <bookmark mark='c'/> A rule of thumb "
            "says you lose about the log of the condition number in digits. QR works with X itself and loses about ten; the "
            "normal equations work with its square and lose nineteen, more than double precision even has. "
            "<bookmark mark='d'/> Centring and scaling the predictors brings the condition number down to about one hundred "
            "and ten. Chapter ten returns to the numerics."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 23", font_size=34, color=GREY_B), label(r"The Linear Model in Depth", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the general linear hypothesis and its $F$-test, \ derived",
            r"GLS; \ standard errors that survive heteroskedasticity and clustering",
            r"what a wrong linear model estimates; \ noisy regressors",
            r"quantile regression and splines",
            r"the numerics of least squares; \ influence",
        ], color=OLS_C, font_size=26)
        prereq = note(r"prerequisites: \ Parts 12, \ 21 and 22").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.ols} II; \ the digits board").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part twenty-three: the linear model in depth. <bookmark mark='b'/> We'll derive the general "
            "linear hypothesis and its F-test; meet generalized least squares; build standard errors that survive uneven "
            "noise and clustered data, with a wild bootstrap for when the clusters are few; ask what a linear model estimates "
            "when the truth isn't linear, and what noisy regressors do; fit quantiles and splines; and finish with the "
            "numerics of least squares and the influence of single points."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
