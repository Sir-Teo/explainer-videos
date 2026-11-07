from __future__ import annotations

import numpy as np

from videos.stats.stats43.common import *  # noqa: F403


class CharacteristicFunctions(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.inversion()
        self.mgf()
        self.heyde()
        self.continuity()
        self.wold()

    def card(self):
        card = chapter_card(8, r"Characteristic functions", r"A transform that always exists", lit=(1925,), part=PART)
        with self.voiceover("Chapter eight. Characteristic functions: a transform that always exists."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\varphi_X(t)", r"=", r"E\, e^{itX} = E \cos tX + i\, E \sin tX, \ \ |\varphi_X(t)| \le 1", font_size=32),
            cmath(r"\varphi_{X + Y}", r"=", r"\varphi_X \varphi_Y \ \ (X \perp Y); \ \ \varphi_{aX + b}(t) = e^{ibt} \varphi_X(at)", font_size=32),
            cmath(r"N(0, 1)", r":", r"e^{-t^2/2}; \ \ \text{Cauchy}: \ e^{-|t|}; \ \ \text{Uniform}(-1, 1): \ \sin t / t", font_size=32),
            cmath(r"E|X|^k < \infty", r"\Rightarrow", r"\varphi \in C^k, \ \ \varphi^{(k)}(0) = i^k E X^k", font_size=32),
        ]
        rows[0][-1].set_color(LAWC)
        whys = [why(r"bounded: \ always exists"), why(r"sums become products"), why(r"the standard ones"), why(r"moments, \ when they exist")]
        with self.voiceover(
            "<bookmark mark='a'/> Part three's moment generating function, the expectation of e to the t X, can be "
            "infinite for every nonzero t, as for the Cauchy law. For positive lognormal and Pareto variables it "
            "diverges to the right of zero, while remaining finite for nonpositive t. Put an i in the exponent and "
            "the problem vanishes. The characteristic function is the expectation of e to the i t X, a cosine and a "
            "sine, bounded by one, so it exists for every law and every t. <bookmark mark='b'/> It keeps the MGF's "
            "virtues: the characteristic function of a sum of independent variables is the product, and affine maps "
            "act simply. <bookmark mark='c'/> The normal's is e to the minus t squared over two; the Cauchy's, e to "
            "the minus absolute t, with a corner at zero because it has no mean; a uniform's, sine t over t. "
            "<bookmark mark='d'/> When k moments exist, it is k times differentiable, and its derivatives at zero "
            "give the moments."
        ) as vo:
            heading=label('Characteristic functions exist for every real probability law',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def inversion(self):
        d = load("cf")
        t = np.asarray(d["t"])
        A = axes([-10, 10], [-0.2, 1], x_length=5.4, y_length=3.4, xlabel=r"$t$", ylabel=r"$\varphi(t)$", xticks=[-10, -5, 0, 5, 10],
                 yticks=[0, 0.5, 1], center=[-3.5, 0.8, 0])
        B = axes([-2.5, 2.5], [0, 0.6], x_length=5.4, y_length=3.4, xlabel=r"$x$", ylabel=r"density", xticks=[-2, -1, 0, 1, 2],
                 yticks=[0, 0.25, 0.5], center=[3.3, 0.8, 0])
        phi = curve(A.ax, t, d["phi"], LIMC, 3.5)
        emp = curve(A.ax, t, d["emp_re"], LAWC, 2)
        x = np.asarray(d["x"])
        tri = curve(B.ax, x, d["tri"], LIMC, 4)
        inv = VGroup(*[Dot(B.ax.c2p(a, b), radius=0.04, color=LAWC) for a, b in zip(x[::3], np.asarray(d["f"])[::3])])
        side = fit_rows(VGroup(
            label(r"$X = U_1 + U_2$, \ uniforms on $(-1, 1)$: \ $\varphi(t) = (\sin t / t)^2$", font_size=24),
            label(r"blue: \ the empirical $\varphi$ of 4,000 draws", font_size=22, color=LAWC),
            label(r"inversion: \ $f(x) = \frac{1}{2\pi} \int e^{-itx} \varphi(t) \, dt$ \ when $\int |\varphi| < \infty$", font_size=24, color=S.ACCENT),
            label(rf"recovered: \ the triangle, \ to within {max(abs(a - b) for a, b in zip(d['f'], d['tri'])):.4f}", font_size=22, color=GOODC),
        ), 12.4, 0.28, [0, -2.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A characteristic function determines its law, and the law can be read back off it. The sum of two uniforms on minus one to one has characteristic function sine t over t, squared: the square, because the variables are independent. <bookmark mark='b'/> In blue, the empirical version from four thousand simulated sums, which converges to it. <bookmark mark='c'/> When the characteristic function is integrable, the inversion formula gives the density directly: one over two pi times the integral of e to the minus i t x times phi. <bookmark mark='d'/> Computed numerically, its maximum error on the displayed grid is about eight ten-thousandths; truncation and quadrature error remain. For any law, a slightly more careful version recovers the probability of every interval whose endpoints carry no atoms, so by pi–lambda, the characteristic function determines the law."       ) as vo:
            self.play(FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(Create(phi), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(emp), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(tri), FadeIn(inv), FadeIn(side[3]))
        self.clear_scene()

    def mgf(self):
        rows = [
            cmath(r"M(s) = E e^{sX} < \infty", r"\text{ on }", r"|s| < \delta", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"M(z)=E e^{zX}\text{ analytic; }\varphi(t)=M(it),\quad |\text{Re}\, z| < \delta", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"\text{equal MGFs near 0} \Rightarrow \text{equal } \varphi \text{ everywhere (identity theorem)}", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"\text{equal laws: \ Part 3's promise, kept}", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"an MGF near zero"), why(r"analytic continuation"), why(r"analytic functions agreeing on a line"), why(r"by inversion")]
        with self.voiceover(
            "<bookmark mark='a'/> Now Part three's promise. Suppose the moment generating function is finite on an interval "
            "around zero. <bookmark mark='b'/> Then the expectation of e to the z X is an analytic function of a complex z on "
            "the strip where the real part is within delta of zero, and on the imaginary axis it is the characteristic "
            "function. <bookmark mark='c'/> Two such functions that agree on a real interval agree on the whole strip, by the "
            "identity theorem of complex analysis, so they agree on the imaginary axis too. <bookmark mark='d'/> Equal "
            "characteristic functions mean equal laws. So a moment generating function finite near zero does determine its "
            "law. Without that condition, the claim can fail, and so can a stronger-sounding one."
        ) as vo:
            heading=label('An MGF finite near zero determines the law',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def heyde(self):
        d = load("cf")
        xs = np.asarray(d["xs"])
        A = axes([0, 6], [0, 1.2], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"density", xticks=[0, 1, 2, 3, 4, 5, 6],
                 yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        ln = curve(ax, xs, d["ln"], LIMC, 4)
        alt = curve(ax, xs, d["alt"], LAWC, 3)
        tab = table_rows([[r"$r$", r"$E X^r$, \ lognormal", r"$E X^r$, \ wiggled"]] +
                         [[f"{m[0]}", f"{m[1]:.4f}", f"{m[2]:.4f}"] for m in d["moments"]], font_size=22, col_buff=0.35, row_buff=0.14)
        tab.move_to([4.45, 1.0, 0])
        side = fit_rows(VGroup(
            label(r"$f(x)\,[1 + 0.8 \sin(2\pi \log x)]$", font_size=22, color=LAWC),
            label(r"every moment the same: \ $e^{r^2/2}$", font_size=22, color=S.ACCENT),
            label(r"moments do not determine the lognormal", font_size=22, color=BADC),
            label(r"(its MGF is infinite for every $s > 0$)", font_size=20, color=GREY_B),
        ), 4.6, 0.36, [4.45, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lognormal has every moment, but no moment generating function to the right of zero. "
            "<bookmark mark='b'/> In 1963 Christopher Heyde wiggled its density by one plus a constant times the sine of two "
            "pi log x. The result is a different law, <bookmark mark='c'/> with exactly the same moments: the integral of x to "
            "the r times the wiggle vanishes for every whole number r, because after substituting the log, the sine "
            "integrates to zero against a shifted normal. The table checks the first four numerically. <bookmark mark='d'/> "
            "So moments alone need not determine a law. A moment generating function finite near zero is enough, and so is "
            "Carleman's condition on the growth of the moments; the lognormal's grow too fast."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ln))
            vo.wait_until("b")
            self.play(Create(alt), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def continuity(self):
        d = load("cf")
        tb = d["tail"]
        rows = [
            cmath(r"\text{L\'evy}", r":", r"\varphi_n \to \varphi \text{ pointwise}, \ \varphi \text{ continuous at } 0 \ \Rightarrow \ X_n \Rightarrow X, \ \varphi_X = \varphi", font_size=28),
            cmath(r"\text{tail}", r":", r"P(|X| > 2/u) \le \frac1u \int_{-u}^{u} \big(1 - \operatorname{Re}\varphi(t)\big) dt", font_size=32),
            cmath(r"\text{so}", r":", r"\varphi \text{ continuous at } 0 \Rightarrow \text{the right side is small for small } u \Rightarrow \text{tight}", font_size=28),
            cmath(r"\text{then}", r":", r"\text{Helly} + \text{uniqueness} \Rightarrow \text{every limit has } \varphi", font_size=32),
        ]
        rows[1][-1].set_color(S.ACCENT)
        whys = [why(r"the continuity theorem"), why(rf"Cauchy, $u = 1$: \ {tb['1.0'][0]:.3f} $\ge$ {tb['1.0'][1]:.3f}"), why(r"no mass escapes"), why(r"chapter 7's tools")]
        with self.voiceover(
            f"<bookmark mark='a'/> Lévy's continuity theorem turns convergence of characteristic functions into weak convergence: if they converge pointwise to a function continuous at zero, the laws converge to the law with that characteristic function. <bookmark mark='b'/> The key is a tail bound: the chance that absolute X exceeds two over u is at most one over u times the integral of one minus the real part of phi from minus u to u. For the Cauchy law with u equal to one, the bound is {say(tb['1.0'][0], 3)} against a true value of {say(tb['1.0'][1], 3)}. <bookmark mark='c'/> If the limit is continuous at zero, that integral is small for small u, uniformly in n eventually, so the sequence is tight. <bookmark mark='d'/> Helly's theorem then supplies a convergent subsequence, its limit must have characteristic function phi, and by uniqueness every subsequence has the same limit. The proof uses every tool of the last two chapters."
        ) as vo:
            heading=label('Continuity at zero prevents mass from escaping',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def wold(self):
        rows = fit_rows(VGroup(
            label(r"Cram\'er--Wold (1936): \ $X_n \Rightarrow X$ in $\mathbb R^k$ \ $\iff$ \ $t^\top X_n \Rightarrow t^\top X$ \ for every $t$", font_size=26, color=LAWC),
            label(r"proof: \ $\varphi_{X_n}(t) = E e^{i t^\top X_n} = \varphi_{t^\top X_n}(1)$", font_size=26, color=GREY_A),
            label(r"so the multivariate CLT is the univariate one, \ in every direction", font_size=26, color=S.ACCENT),
            label(r"used in every multi-parameter asymptotic of Parts 22--41", font_size=24, color=GOODC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One more consequence, by Harald Cramér and Herman Wold in 1936: random vectors converge in "
            "law exactly when every linear combination of their coordinates does. <bookmark mark='b'/> The proof is a single "
            "line: the vector's characteristic function at t is the characteristic function of the projection onto t, "
            "evaluated at one. <bookmark mark='c'/> So the multivariate central limit theorem is the univariate one applied "
            "in every direction at once. <bookmark mark='d'/> Every asymptotic statement about several parameters in the "
            "master's, from Wald tests to the sandwich, rests on it."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
