from __future__ import annotations

import numpy as np

from videos.stats.stats12.common import *  # noqa: F403


class Bands(VoiceoverScene):
    def construct(self):
        self.card()
        self.formulas()
        self.picture()
        self.one_family()
        self.lesson()

    def card(self):
        card = chapter_card(7, r"Bands", r"How sure are we of the line, \ and of the next point?", part=PART)
        with self.voiceover("Chapter seven. Confidence and prediction bands."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def formulas(self):
        rows = [
            cmath(r"\mathrm{Var}\big(x_0^\top\hat\beta\big)", r"=", r"\sigma^2\,x_0^\top(X^\top X)^{-1}x_0 = \sigma^2\Big(\frac1n + \frac{(x_0 - \bar x)^2}{\sum (x_i - \bar x)^2}\Big)",
                  font_size=30),
            cmath(r"\text{the mean at } x_0", r":", r"x_0^\top\hat\beta \pm t\,s\,\sqrt{x_0^\top(X^\top X)^{-1}x_0}", font_size=30),
            cmath(r"\text{a new } y \text{ at } x_0", r":", r"x_0^\top\hat\beta \pm t\,s\,\sqrt{1 + x_0^\top(X^\top X)^{-1}x_0}", font_size=30),
            cmath(r"\text{the whole line}", r":", r"x_0^\top\hat\beta \pm \sqrt{p\,F_{p,\,n-p}}\ s\,\sqrt{x_0^\top(X^\top X)^{-1}x_0}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"smallest at $\bar x$, \ growing as $x_0$ moves away"), why(r"pointwise confidence (Part 11)"),
                why(r"Part 11's prediction interval: \ the noise of one more point"), why(r"Working \& Hotelling (1929): \ every $x_0$ at once")]
        with self.voiceover(
            "How uncertain is the fitted line itself? <bookmark mark='a'/> The variance of the fitted value at a point x-nought "
            "is smallest at the mean of the x's and grows quadratically as x-nought moves away, because a small error in the "
            "slope matters more far from the centre. <bookmark mark='b'/> That gives a pointwise confidence interval for the "
            "mean of y at x-nought. <bookmark mark='c'/> For a new observation, add the noise of one more point: Part 11's "
            "prediction interval, now along a line. <bookmark mark='d'/> And for the whole line at once, Holbrook Working and "
            "Harold Hotelling replaced the t multiplier by the square root of p times an F quantile in 1929: Part 11's Scheffé "
            "idea, for regression."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.7, x=-0.6, buff=0.55, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("bands")
        dl = load("line")
        x, y = np.asarray(dl["x"]), np.asarray(dl["y"])
        grid = np.asarray(d["grid"])
        A = axes([-2.2, 2.2], [-3.2, 3.2], x_length=7.4, y_length=5.4, xlabel=r"mid-parent ($z$)", ylabel=r"child ($z$)",
                 xticks=[-2, -1, 0, 1, 2], yticks=[-3, 0, 3], center=[-2.0, -0.3, 0])
        ax = A.ax
        pts = scatter(ax, x, y)
        fitl = polyline(ax, grid, d["fit"], FIT, 3.5)
        cb = band(ax, grid, np.asarray(d["lo"]), np.asarray(d["hi"]), FIT, 0.35)
        wh = VGroup(polyline(ax, grid, d["wlo"], S.POST, 2), polyline(ax, grid, d["whi"], S.POST, 2))
        pb = VGroup(DashedVMobject(polyline(ax, grid, np.clip(d["plo"], -3.2, 3.2), S.PRIOR, 2.5), num_dashes=40),
                    DashedVMobject(polyline(ax, grid, np.clip(d["phi"], -3.2, 3.2), S.PRIOR, 2.5), num_dashes=40))
        leg = legend([(FIT, rf"95\% for the mean, \ pointwise \ ($t = {d['t']:.2f}$)"), (S.POST, rf"Working--Hotelling \ ($\sqrt{{2F}} = {d['wh']:.2f}$)"),
                      (S.PRIOR, r"95\% prediction, \ for a new family")], font_size=20).move_to([4.5, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"the confidence band is a bow tie: \ narrow at $\bar x$", font_size=22),
            label(r"the prediction band holds most of the points; \ the confidence band does not, \ and should not", font_size=22, color=GREY_A),
            label(r"more data shrinks the confidence band to the line; \ never the prediction band", font_size=22, color=OBS),
        ), 4.6, 0.3, [4.5, -1.2, 0])
        tag = simulated_tag(r"the World: \ 30 families", corner=DR)
        with self.voiceover(
            "Here are all three on the thirty families. <bookmark mark='a'/> The fitted line, and its pointwise ninety-five "
            "percent confidence band: a bow tie, narrowest at the average parent and widening toward the ends. "
            "<bookmark mark='b'/> The Working–Hotelling band, which covers the whole true line at once, is a little wider. "
            "<bookmark mark='c'/> And the prediction band, for a new family's child, is much wider: it has to contain the "
            "scatter of individuals, not just the uncertainty about the average. <bookmark mark='d'/> Most of the points lie "
            "inside the prediction band, and most lie outside the confidence band, as they should. With more data, the "
            "confidence band shrinks onto the line; the prediction band never shrinks below the noise."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag), FadeIn(pts))
            vo.wait_until("a")
            self.play(Create(fitl), FadeIn(cb), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(wh), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(Create(pb), FadeIn(leg[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"which band answers your question?", font_size=30, color=OBS),
            label(r"``how tall are children of 180 cm parents, \ on average?'': \ the confidence band", font_size=24),
            label(r"``how tall will \emph{this} child be?'': \ the prediction band", font_size=24),
            label(r"``where is the whole regression line?'': \ Working--Hotelling", font_size=24),
            label(r"software draws the first by default; \ the question usually wants the second", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So which band answers your question? <bookmark mark='b'/> How tall are the children of tall "
            "parents, on average? The confidence band. <bookmark mark='c'/> How tall will this particular child be? The "
            "prediction band. <bookmark mark='d'/> Where does the whole regression line lie? Working–Hotelling. "
            "<bookmark mark='e'/> Plotting software usually draws the first by default, while the question people are asking "
            "is usually the second."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def one_family(self):
        d = load("dummies")
        m2 = d["m2"]
        from explainer.stats.kit import ols as O
        X = O.design(np.asarray(d["mid"]), np.asarray(d["son"]))
        r = O.fit(X, np.asarray(d["y"]))
        X0 = np.array([[1.0, 175.0, 1.0]])
        lo, hi = r.band(X0)
        plo, phi = r.band(X0, prediction=True)
        rows = fit_rows(VGroup(
            label(r"a couple whose average height is 175 cm \ expect a son", font_size=28),
            MathTex(rf"\hat y = {m2[0]:.1f} + {m2[1]:.3f}\times 175 + {m2[2]:.1f} = {r.predict(X0)[0]:.1f}\ \text{{cm}}", font_size=32, color=FIT),
            MathTex(rf"\text{{mean of such sons: }} [{lo[0]:.1f},\ {hi[0]:.1f}]", font_size=30, color=FIT),
            MathTex(rf"\text{{this son: }} [{plo[0]:.1f},\ {phi[0]:.1f}]", font_size=30, color=S.PRIOR),
            label(r"400 families pin down the average to within a centimetre; \ one son's height stays uncertain by $\pm 11$ cm", font_size=24,
                  color=OBS),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "A concrete prediction. <bookmark mark='a'/> A couple whose average height is a hundred and seventy-five "
            "centimetres are expecting a son. <bookmark mark='b'/> The dummy-variable model predicts a hundred and seventy-nine "
            "centimetres. <bookmark mark='c'/> The ninety-five percent confidence interval for the average height of all such "
            "sons is barely two centimetres wide: four hundred families pin it down well. <bookmark mark='d'/> But the "
            "prediction interval for this particular son runs from about a hundred and sixty-eight to a hundred and "
            "ninety. <bookmark mark='e'/> Parents' heights tell you a lot about sons on average, and much less about any "
            "one of them."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
