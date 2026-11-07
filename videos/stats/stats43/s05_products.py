from __future__ import annotations

import numpy as np

from videos.stats.stats43.common import *  # noqa: F403


class Products(VoiceoverScene):
    def construct(self):
        self.card()
        self.independence()
        self.fubini()
        self.counter()
        self.extension()
        self.likelihood()

    def card(self):
        card = chapter_card(4, r"Independence and products", r"How do infinitely many coins exist?", part=PART)
        with self.voiceover("Chapter four. Independence, products, and how infinitely many coins can exist at once."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def independence(self):
        rows = [
            cmath(r"\mathcal G \perp \mathcal H", r"\iff", r"P(A \cap B) = P(A) P(B) \ \ \forall A \in \mathcal G, B \in \mathcal H", font_size=32),
            cmath(r"X \perp Y", r"\iff", r"\sigma(X) \perp \sigma(Y)", font_size=34),
            cmath(r"\text{enough}", r":", r"P(X \le x, Y \le y) = F(x) G(y) \ \ \forall x, y \ \ (\pi\text{--}\lambda)", font_size=32),
            cmath(r"\text{so}", r":", r"g(X) \perp h(Y); \ \ E[XY] = E X\, E Y \text{ if integrable}", font_size=32),
        ]
        rows[1][-1].set_color(LAWC)
        whys = [why(r"for $\sigma$-algebras"), why(r"for variables: \ their information"), why(r"a generating class"), why(r"by the next theorem")]
        with self.voiceover(
            "<bookmark mark='a'/> Independence is a property of information. Two sigma-algebras are independent if "
            "every event of one is independent of every event of the other. <bookmark mark='b'/> Two random variables"
            " are independent if the sigma-algebras they generate are. <bookmark mark='c'/> By pi–lambda again, it is"
            " enough that the joint CDF factors into the marginals. <bookmark mark='d'/> Measurable functions of "
            "independent variables are then independent, because their information is contained in the originals', "
            "and the expectation of a product factors, by the theorem that follows."
        ) as vo:
            heading=label('Independence is a property of sigma-algebras',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fubini(self):
        rows = [
            cmath(r"(\mu \times \nu)(A \times B)", r"=", r"\mu(A)\, \nu(B), \ \text{extended uniquely to } \mathcal F \otimes \mathcal G", font_size=30),
            cmath(r"\text{Tonelli}", r":", r"f \ge 0 \Rightarrow \textstyle\iint f \, d(\mu \times \nu) = \int\!\big(\int f \, d\nu\big) d\mu = \int\!\big(\int f \, d\mu\big) d\nu", font_size=28),
            cmath(r"\text{Fubini}", r":", r"\textstyle\iint |f| < \infty \ \Rightarrow \ \text{the same, for signed } f", font_size=32),
            cmath(r"E[XY]", r"=", r"\textstyle\iint xy \, d\mu_X\, d\mu_Y = E X \, E Y \ \ (X \perp Y: \ \text{the joint law is } \mu_X \times \mu_Y)", font_size=28),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"rectangles, \ then Carath\'eodory"), why(r"non-negative measurable; sigma-finite spaces"), why(r"signed: \ if absolutely integrable"), why(r"the product rule")]
        with self.voiceover(
            "<bookmark mark='a'/> For sigma-finite measure spaces, including probability spaces, the product measure "
            "gives a rectangle the product of its sides' measures, and Carathéodory's theorem extends that uniquely. "
            "<bookmark mark='b'/> Tonelli's theorem: for a non-negative function, the double integral equals either "
            "iterated integral, in either order. <bookmark mark='c'/> Fubini's theorem: the same holds for a signed "
            "function, provided its absolute value is integrable. <bookmark mark='d'/> Independence says the joint "
            "law is the product of the marginals, and Fubini then gives the product rule for expectations. The "
            "proviso in Fubini is not a technicality."
        ) as vo:
            heading=label('Product integration requires measurability and sigma-finiteness',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def counter(self):
        m = 6
        s = 0.7
        x0, y0 = -4.6, 2.0
        cells = VGroup()
        for i in range(m):
            for j in range(m):
                v = 1 if i == j else (-1 if j == i + 1 else 0)
                col = GOODC if v == 1 else (BADC if v == -1 else GREY_E)
                sq = Square(side_length=s * 0.92, stroke_width=0, fill_color=col, fill_opacity=0.8 if v else 0.35).move_to([x0 + j * s, y0 - i * s, 0])
                t = label(f"{v:+d}" if v else "0", font_size=20, color=WHITE if v else GREY_C).move_to(sq)
                cells.add(VGroup(sq, t))
        dots_r = label(r"$\cdots$", font_size=30, color=GREY_B).move_to([x0 + m * s, y0 - 2.5 * s, 0])
        dots_d = label(r"$\vdots$", font_size=30, color=GREY_B).move_to([x0 + 2.5 * s, y0 - m * s + 0.1, 0])
        rs = VGroup(*[label(r"$0$", font_size=22, color=S.ACCENT).move_to([x0 + (m + 0.9) * s, y0 - i * s, 0]) for i in range(m)])
        cs = VGroup(*[label(r"$1$" if j == 0 else r"$0$", font_size=22, color=LAWC).move_to([x0 + j * s, y0 - (m + 0.9) * s, 0]) for j in range(m)])
        side = fit_rows(VGroup(
            label(r"$a_{mm} = +1$, \ $a_{m, m+1} = -1$", font_size=24),
            label(r"every row sums to 0: \ $\sum_m \sum_n a_{mn} = 0$", font_size=24, color=S.ACCENT),
            label(r"column 1 sums to 1, \ the rest to 0: \ $\sum_n \sum_m a_{mn} = 1$", font_size=24, color=LAWC),
            label(r"$\sum |a_{mn}| = \infty$: \ Fubini's proviso fails", font_size=24, color=BADC),
        ), 4.6, 0.45, [4.2, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is why. Counting measure on the integers is a measure too, so double series obey "
            "the same rules. Put plus one on the diagonal and minus one just to its right. <bookmark mark='b'/> Every row "
            "sums to zero, so summing rows first gives zero. <bookmark mark='c'/> But the first column sums to one and "
            "every other column to zero, so summing columns first gives one. <bookmark mark='d'/> The absolute values sum "
            "to infinity, and without that proviso the order of integration can change the answer. In probability it "
            "appears whenever an expectation of a product of non-integrable variables is computed by conditioning."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.03), FadeIn(dots_r), FadeIn(dots_d), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rs), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(cs), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def extension(self):
        rows = [
            cmath(r"\mu_{t_1 \ldots t_k}", r":", r"\text{a law on } \mathbb R^k \text{ for each finite set of indices}", font_size=32),
            cmath(r"\text{consistent}", r":", r"\text{marginalizing } \mu_{t_1 \ldots t_k} \text{ over } t_k \text{ gives } \mu_{t_1 \ldots t_{k-1}}", font_size=30),
            cmath(r"\text{Kolmogorov}", r":", r"\exists! \ P \text{ on } (\mathbb R^T, \mathcal B^T) \text{ with these finite-dimensional laws}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{i.i.d.\ sequences, Markov chains, Gaussian processes exist}", font_size=30),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"finite-dimensional laws"), why(r"they agree with each other"), why(r"the extension theorem (1933)"), why(r"Parts 7, 17, 39")]
        with self.voiceover(
            "<bookmark mark='a'/> For infinitely many variables, Kolmogorov proved the theorem the Grundbegriffe is best "
            "remembered for. Suppose we specify a law for every finite collection of the variables, <bookmark mark='b'/> "
            "consistently, so that integrating one variable out of a joint law gives the smaller joint law. <bookmark "
            "mark='c'/> Then there is exactly one probability measure on the space of all paths with those "
            "finite-dimensional laws. <bookmark mark='d'/> That one theorem makes sense of an infinite sequence of coin "
            "tosses, of Part seven's Markov chains, of Part seventeen's time series and of Part thirty-nine's Gaussian "
            "fields. One warning: it builds measures on the product sigma-algebra, which cannot see properties of "
            "uncountably many coordinates at once, such as continuity of a path. Part forty-four's Brownian motion needs "
            "one more step."
        ) as vo:
            heading=label('Consistent finite-dimensional laws define a product-space law',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def likelihood(self):
        rows = fit_rows(VGroup(
            label(r"$n$ i.i.d.\ observations: \ the law of the data is $\mu_\theta^{\otimes n}$", font_size=26),
            label(r"its density with respect to $\lambda^{\otimes n}$: \ $\prod_i f_\theta(x_i)$, \ the likelihood", font_size=26, color=LAWC),
            label(r"a likelihood is a Radon--Nikodym derivative: \ $dP_\theta / d\nu$", font_size=26, color=S.ACCENT),
            label(r"one fixed dominating measure for the parameter family is required", font_size=26, color=GOODC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Statistics lives on these products. A sample of n independent observations has the "
            "n-fold product law. <bookmark mark='b'/> Its density, with respect to the product of Lebesgue measures, "
            "is the product of the individual densities: the likelihood of Part twenty-two. <bookmark mark='c'/> In "
            "general a likelihood is a Radon–Nikodym derivative, the density of the data's law with respect to some "
            "fixed measure. <bookmark mark='d'/> That is why one definition covers counts, measurements, censored "
            "survival times and mixtures of them: when the whole parameter family admits one fixed, "
            "parameter-independent dominating measure. Some statistical families are not dominated in this way."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
