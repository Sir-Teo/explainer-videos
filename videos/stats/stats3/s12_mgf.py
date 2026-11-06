from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403


class MGF(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.normal()
        self.sums()
        self.gamma_sum()
        self.cf()

    def card(self):
        card = chapter_card(11, r"Generating functions", r"Part 2's polynomials, \ grown up", lit=(1810,), part=PART)
        with self.voiceover("Chapter eleven. Generating functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"M_X(t)", r"=", r"E\, e^{tX}", font_size=40),
            cmath(r"M_X(t)", r"=", r"1 + t\, E X + \frac{t^2}{2!} E X^2 + \frac{t^3}{3!} E X^3 + \cdots", font_size=36),
            cmath(r"M_X^{(k)}(0)", r"=", r"E X^k", font_size=40),
        ]
        rows[0][0].set_color(EXACT)
        rows[2][2].set_color(EXACT)
        whys = [why(r"assume $M_X(t)$ is finite in a neighborhood of $0$"), why(r"expand $e^{tX}$; \ linearity"),
                why(r"differentiate $k$ times at $0$")]
        back = label(r"Part 2's pgf was $E\, s^X$; \ put $s = e^t$", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.5)
        intro = label('Moments in a generating function', font_size=36)
        with self.voiceover(
            "Part 2 represented finite counting distributions as polynomials. For distributions whose moment generating function is finite around zero, the idea extends to a power series. <bookmark mark='a'/> The moment generating function of X is the expectation of e to the "
            "t X, a function of t. <bookmark mark='b'/> Expand the exponential, and by linearity every moment of X "
            "appears as a coefficient, with t to the k over k factorial. <bookmark mark='c'/> So the k-th "
            "derivative at zero is the k-th moment, which is where the name comes from. <bookmark mark='d'/> It's "
            "Part 2's probability generating function, with s replaced by e to the t."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=0.6)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=k > 0)
            vo.wait_until("d")
            self.play(FadeIn(back))
        self.clear_scene()

    def normal(self):
        rows = [
            cmath(r"M(t)", r"=", r"\int \frac{1}{\sqrt{2\pi}} e^{tz - z^2/2}\, dz", font_size=34),
            cmath(r"M(t)", r"=", r"e^{t^2/2} \int \frac{1}{\sqrt{2\pi}} e^{-(z - t)^2/2}\, dz", font_size=34),
            cmath(r"M(t)", r"=", r"e^{t^2/2}", font_size=40),
            cmath(r"M_{\mu + \sigma Z}(t)", r"=", r"e^{\mu t}\, M(\sigma t)", r"=", r"e^{\mu t + \sigma^2 t^2 / 2}",
                  font_size=36),
        ]
        rows[3][4].set_color(EXACT)
        whys = [why(r"$Z$ standard normal"), why(r"complete the square"), why(r"a shifted normal integrates to $1$"),
                why(r"location and scale")]
        mom = MathTex(r"M'(0) = \mu, \quad M''(0) = \mu^2 + \sigma^2", font_size=30, color=GREY_A).to_edge(DOWN, buff=0.5)
        intro = label('Complete the square', font_size=36)
        with self.voiceover(
            "For the standard normal the moment generating function takes one trick. <bookmark mark='a'/> Write "
            "out the integral. <bookmark mark='b'/> Complete the square in the exponent: t z minus z squared over "
            "two is t squared over two minus z minus t, squared, over two. <bookmark mark='c'/> What's left is a "
            "normal density shifted by t, which integrates to one, so M of t is e to the t squared over two. "
            "<bookmark mark='d'/> For a normal with mean mu and variance sigma squared, shift and scale: e to the mu "
            "t plus sigma squared t squared over two. Differentiate at zero and out come the mean and the second "
            "moment."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.4, buff=0.5)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=k in (1, 2))
            self.play(FadeIn(mom))
        self.clear_scene()

    def sums(self):
        d = load("mgf")
        rows = [
            cmath(r"M_{X+Y}(t)", r"=", r"E\, e^{tX} e^{tY}", r"=", r"M_X(t)\, M_Y(t)", font_size=34),
            cmath(r"\text{Poisson: } M(t)", r"=", r"e^{\lambda (e^t - 1)}", font_size=34),
            cmath(r"M_{X+Y}(t)", r"=", r"e^{(a + b)(e^t - 1)}", font_size=34),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"independence"), why(r"$\sum_k e^{tk} e^{-\lambda} \lambda^k / k!$"),
                why(r"Poisson$(a) +$ Poisson$(b) =$ Poisson$(a + b)$")]
        A = axes([-0.6, 13.6], [0, 0.22], x_length=5.8, y_length=3.0, xlabel=rf"Poisson$({d['a']}) +$ Poisson$({d['b']})$",
                 xticks=[0, 4, 8, 12], yticks=[0, 0.1, 0.2], center=[-3.4, -2.0, 0])
        bars = pmf_bars(A.ax, d["kk"], d["emp"], SIM, width=0.65)
        dots = pmf_dots(A.ax, d["kk"], d["pois"], EXACT, radius=0.06)
        leg = legend([(SIM, r"50,000 simulated sums"), (EXACT, r"Poisson$(4)$")], font_size=20).next_to(A, UP, buff=0.1)
        uniq = label(r"if $M$ is finite near $0$, \ it determines the distribution", font_size=24, color=S.ACCENT)
        uniq.move_to([3.4, -1.6, 0])
        why2 = label(r"(proved in Part 43)", font_size=20, color=GREY_B).next_to(uniq, DOWN, buff=0.12)
        intro = label('Independent sums become products', font_size=36)
        with self.voiceover(
            "Like Part 2's polynomials, moment generating functions turn sums into products. "
            "<bookmark mark='a'/> For independent X and Y, the generating function of the sum is the product of "
            "theirs. <bookmark mark='b'/> A Poisson with mean lambda has generating function e to the lambda times "
            "e to the t minus one. <bookmark mark='c'/> Multiply two of them and the exponents add: the sum of "
            "independent Poissons is Poisson, with the means added. <bookmark mark='d'/> Fifty thousand simulated "
            "sums agree. That last step needs one more fact: a moment generating function that's finite near zero "
            "determines its distribution uniquely. It's true, and Part 43 proves it."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.9, x=0.4, buff=0.45, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(A), FadeIn(bars), FadeIn(dots), FadeIn(leg), FadeIn(uniq), FadeIn(why2))
        self.clear_scene()

    def gamma_sum(self):
        rows = [
            cmath(r"M_{\text{exp}}(t)", r"=", r"\int_0^\infty e^{tx} \lambda e^{-\lambda x}\, dx", r"=",
                  r"\frac{\lambda}{\lambda - t}", font_size=34),
            cmath(r"M_{G_1 + \cdots + G_k}(t)", r"=", r"\left(\frac{\lambda}{\lambda - t}\right)^{k}", font_size=36),
            cmath(r"M_{\text{gamma}(k, \text{rate }\lambda)}(t)", r"=", r"\int_0^\infty e^{tx} \frac{\lambda^k x^{k-1} e^{-\lambda x}}"
                  r"{(k-1)!}\, dx", r"=", r"\left(\frac{\lambda}{\lambda - t}\right)^{k}", font_size=32),
        ]
        rows[2][4].set_color(EXACT)
        whys = [why(r"for $t < \lambda$"), why(r"independent gaps: \ multiply"),
                why(r"substitute $u = (\lambda - t)x$: \ the same function")]
        take = label(r"chapter 5's buses, \ now proved: \ the $k$-th arrival is gamma", font_size=26, color=S.ACCENT)
        take.to_edge(DOWN, buff=0.6)
        intro = label('The wait for the k-th arrival', font_size=36)
        with self.voiceover(
            "Uniqueness turns generating functions into a proof machine. Chapter five claimed that the wait for the "
            "third bus is gamma; here's the proof. <bookmark mark='a'/> The exponential's moment generating function "
            "is lambda over lambda minus t. <bookmark mark='b'/> The wait for the k-th bus is a sum of k independent "
            "exponential gaps, so its generating function is that, to the k. <bookmark mark='c'/> And the gamma "
            "density, integrated against e to the t x with one substitution, gives exactly the same function. Same "
            "generating function, same distribution: the k-th arrival of a Poisson process is gamma."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.5, x=0.2, buff=0.6, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            self.play(FadeIn(take))
        self.clear_scene()

    def cf(self):
        dfn = definition_card(r"Characteristic function", r"$\varphi_X(t) = E\, e^{itX}$: \ always finite, since "
                              r"$|e^{itX}| = 1$", color=EXACT, width=6.4, font_size=25).move_to([0, 1.8, 0])
        ex = VGroup(MathTex(r"\text{normal: } \varphi(t) = e^{-t^2/2}", font_size=32),
                    MathTex(r"\text{Cauchy: } \varphi(t) = e^{-|t|}", r"\quad \text{(no mgf at all)}", font_size=32))
        ex.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.3, 0])
        ex[1][1].set_color(GREY_B)
        take = label(r"Part 6 proves the central limit theorem with it", font_size=28, color=S.ACCENT).to_edge(DOWN, buff=0.7)
        intro = label('A transform that always exists', font_size=36)
        with self.voiceover(
            "Some distributions, like the Cauchy, have no moment generating function: e to the t X has infinite "
            "expectation for every t except zero. <bookmark mark='a'/> The cure is to use an imaginary t. The "
            "characteristic function, the expectation of e to the i t X, always exists, because e to the i t X has "
            "size one. <bookmark mark='b'/> For the normal it's e to the minus t squared over two; even the Cauchy "
            "has one, e to the minus the absolute value of t. <bookmark mark='c'/> Characteristic functions are how "
            "Laplace first glimpsed the central limit theorem, and how Part 6 will prove it."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(dfn))
            vo.wait_until("b")
            self.play(FadeIn(ex, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(take))
        self.clear_scene()
