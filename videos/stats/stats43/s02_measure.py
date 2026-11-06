from __future__ import annotations

import numpy as np

from videos.stats.stats43.common import *  # noqa: F403


class Measures(VoiceoverScene):
    def construct(self):
        self.card()
        self.vitali()
        self.circle()
        self.sigma()
        self.pilambda()
        self.caratheodory()
        self.cantor()

    def card(self):
        card = chapter_card(1, r"$\sigma$-algebras and measures", r"Can every set have a size?", lit=(1905,), part=PART)
        with self.voiceover("Chapter one. Can every set of outcomes be given a probability?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def vitali(self):
        rows = [
            cmath(r"\text{want}", r":", r"\lambda(A) \text{ for all } A \subseteq [0, 1), \text{ shift-invariant, countably additive}", font_size=30),
            cmath(r"x \sim y", r"\iff", r"x - y \in \mathbb Q; \ \ V = \text{one point from each class (choice)}", font_size=30),
            cmath(r"[0, 1)", r"=", r"\textstyle\bigsqcup_{q \in \mathbb Q \cap [0, 1)} (V + q \bmod 1) \ \ \text{(disjoint, countable)}", font_size=30),
            cmath(r"1", r"=", r"\textstyle\sum_q \lambda(V + q) = \sum_q \lambda(V) \in \{0, \infty\}: \ \text{impossible}", font_size=30),
        ]
        rows[3][-1].set_color(BADC)
        whys = [why(r"length, \ on everything"), why(r"Vitali (1905)"), why(r"rational shifts tile the interval"), why(r"contradiction")]
        with self.voiceover(
            "<bookmark mark='a'/> Part two quietly assumed that every set of outcomes has a probability. Try it for the "
            "simplest case: a length on every subset of the unit interval, unchanged by shifting a set around the interval, "
            "countably additive, and giving the whole interval length one. <bookmark mark='b'/> In 1905 Giuseppe Vitali "
            "showed there is no such thing. Call two points equivalent if they differ by a rational number, and, using the "
            "axiom of choice, pick one point from every equivalence class. Call that set V. <bookmark mark='c'/> Shifting V "
            "by each rational in the interval, wrapping around at one, gives countably many disjoint copies that together "
            "cover the interval exactly. <bookmark mark='d'/> So one would equal a countable sum of equal lengths: zero if "
            "V's length is zero, infinity if it is anything else. No length can be assigned to V."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def circle(self):
        g = np.random.default_rng(1905)
        R = 2.3
        c0 = np.array([-3.2, -0.1, 0])
        ring = Circle(radius=R, color=GREY_C, stroke_width=2).move_to(c0)
        v = g.random(9) * 0.11
        shifts = [0.0, 1 / 2, 1 / 3, 2 / 3, 1 / 4, 3 / 4, 1 / 5]
        cols = [LAWC, S.ACCENT, S.ALT, S.PRIOR, S.KEPT, S.RESID, S.TREAT]
        groups = VGroup()
        for s_, col in zip(shifts, cols):
            pts = VGroup(*[Dot(c0 + R * np.array([np.cos(2 * np.pi * ((a + s_) % 1)), np.sin(2 * np.pi * ((a + s_) % 1)), 0]),
                               radius=0.07, color=col) for a in v])
            groups.add(pts)
        side = fit_rows(VGroup(
            label(r"$[0, 1)$ bent into a circle: \ shifts are rotations", font_size=24, color=GREY_A),
            label(r"blue: \ a few points of $V$", font_size=24, color=LAWC),
            label(r"each colour: \ $V$ rotated by a rational", font_size=24, color=S.ACCENT),
            label(r"so: \ not every set can be an event", font_size=26, color=BADC),
            label(r"probabilities live on a \emph{$\sigma$-algebra} of sets", font_size=26, color=GOODC),
        ), 5.4, 0.42, [3.6, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Bend the interval into a circle, so that shifting with wrap-around becomes rotation. "
            "<bookmark mark='b'/> Here are a few points of V, in blue. <bookmark mark='c'/> Each colour is V rotated by a "
            "different rational; the infinitely many rotations fill the circle without overlapping. A rotation cannot "
            "change a length, so all the copies would have the same length, and there are too many of them. <bookmark "
            "mark='d'/> The lesson is not that probability is broken, but that it must be more modest. <bookmark "
            "mark='e'/> Probabilities are assigned to a collection of sets rich enough for everything we want to ask, and "
            "no richer: a sigma-algebra."
        ) as vo:
            self.play(Create(ring), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(groups[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(gg) for gg in groups[1:]], lag_ratio=0.4), FadeIn(side[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def sigma(self):
        rows = [
            cmath(r"\mathcal F", r":", r"\Omega \in \mathcal F; \ \ A \in \mathcal F \Rightarrow A^c \in \mathcal F; \ \ A_1, A_2, \ldots \in \mathcal F \Rightarrow \textstyle\bigcup_i A_i \in \mathcal F", font_size=28),
            cmath(r"P", r":", r"\mathcal F \to [0, 1], \ \ P(\Omega) = 1, \ \ P\big(\textstyle\bigsqcup_i A_i\big) = \sum_i P(A_i)", font_size=30),
            cmath(r"\mathcal B(\mathbb R)", r"=", r"\sigma\{(a, b]\}: \ \text{the smallest } \sigma\text{-algebra containing the intervals}", font_size=30),
            cmath(r"\text{in } \mathcal B", r":", r"\text{open and closed sets, countable sets, } \{\omega : \lim X_n(\omega) \text{ exists}\}, \ldots", font_size=28),
        ]
        rows[2][-1].set_color(LAWC)
        whys = [why(r"closed under countable operations"), why(r"countable additivity"), why(r"the Borel sets"), why(r"everything we ask")]
        with self.voiceover(
            "<bookmark mark='a'/> A sigma-algebra contains the whole space, the complement of each of its sets, and the "
            "union of any countable sequence of its sets, so also countable intersections and limits. <bookmark mark='b'/> "
            "A probability measure gives each of its sets a number between zero and one, one to the whole space, and adds "
            "over countably many disjoint sets: Part two's third axiom, now on a sigma-algebra. <bookmark mark='c'/> On the "
            "real line the standard choice is the Borel sigma-algebra, the smallest one containing the intervals. <bookmark "
            "mark='d'/> It holds every set a statistician will ever ask about: open and closed sets, countable sets, and "
            "events like the set of outcomes on which a sequence of random variables converges. Vitali's set is not in "
            "it, and nothing is lost."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pilambda(self):
        rows = [
            cmath(r"\pi\text{-system}", r":", r"\text{closed under finite intersections, e.g. } \{(-\infty, x] : x \in \mathbb R\}", font_size=30),
            cmath(r"\lambda\text{-system}", r":", r"\Omega \in \mathcal L; \ A \subseteq B \Rightarrow B \setminus A \in \mathcal L; \ A_n \uparrow A \Rightarrow A \in \mathcal L", font_size=30),
            cmath(r"\text{Dynkin}", r":", r"\mathcal P \subseteq \mathcal L \ \Rightarrow \ \sigma(\mathcal P) \subseteq \mathcal L", font_size=32),
            cmath(r"\text{so}", r":", r"\text{the same CDF} \Rightarrow \text{the same law on all of } \mathcal B", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"a generating class"), why(r"where two measures agree"), why(r"the $\pi$--$\lambda$ theorem"), why(r"uniqueness")]
        with self.voiceover(
            "<bookmark mark='a'/> How do we know that two measures agreeing on intervals agree everywhere? A pi-system is a "
            "class closed under finite intersections, like the half-lines from minus infinity to x. <bookmark mark='b'/> "
            "The sets on which two probability measures agree always form a lambda-system: it contains the whole space, "
            "differences of nested sets, and increasing limits. <bookmark mark='c'/> Dynkin's pi–lambda theorem says that "
            "a lambda-system containing a pi-system contains the whole sigma-algebra it generates. <bookmark mark='d'/> So "
            "two laws with the same CDF are the same law on every Borel set. Every uniqueness theorem in probability, from "
            "characteristic functions to product measures, is proved this way."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def caratheodory(self):
        rows = [
            cmath(r"\lambda^*(A)", r"=", r"\inf\big\{\textstyle\sum_i (b_i - a_i) : A \subseteq \bigcup_i (a_i, b_i]\big\}", font_size=32),
            cmath(r"A \text{ measurable}", r"\iff", r"\lambda^*(E) = \lambda^*(E \cap A) + \lambda^*(E \cap A^c) \ \ \forall E", font_size=30),
            cmath(r"\text{Carath\'eodory}", r":", r"\text{these } A \text{ form a } \sigma\text{-algebra} \supseteq \mathcal B, \text{ and } \lambda^* \text{ is a measure on it}", font_size=28),
            cmath(r"\text{with } F", r":", r"\text{lengths } F(b) - F(a) \ \to \ \text{the unique law with CDF } F", font_size=30),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"outer measure: \ cover by intervals"), why(r"sets that split everything cleanly"), why(r"the extension theorem"), why(r"Lebesgue--Stieltjes")]
        with self.voiceover(
            "<bookmark mark='a'/> Existence is Carathéodory's extension theorem, proved in Part five of Analysis, Built. "
            "Define the outer measure of any set as the least total length of countably many intervals covering it. "
            "<bookmark mark='b'/> Call a set measurable if it splits every other set cleanly, with the outer measures of "
            "the two pieces adding up. <bookmark mark='c'/> Constantin Carathéodory showed that the measurable sets form a "
            "sigma-algebra containing all the Borel sets, and that the outer measure is countably additive on it. <bookmark "
            "mark='d'/> Measure lengths with F of b minus F of a instead, for any non-decreasing right-continuous F rising "
            "from zero to one, and the same construction gives a unique law with CDF F. Every distribution we have used "
            "exists because of this theorem."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cantor(self):
        d = load("cantor")
        bars = VGroup()
        L = 5.6
        x0 = -6.4
        for k in range(5):
            segs = [(0.0, 1.0)]
            for _ in range(k):
                segs = [s for a, b in segs for s in ((a, a + (b - a) / 3), (b - (b - a) / 3, b))]
            row = VGroup(*[Line([x0 + a * L, 2.4 - 0.5 * k, 0], [x0 + b * L, 2.4 - 0.5 * k, 0], color=LAWC, stroke_width=6) for a, b in segs])
            bars.add(row)
        mtxt = VGroup(*[label(rf"${(2 / 3) ** k:.3f}$", font_size=20, color=GREY_A).next_to(bars[k], RIGHT, buff=0.25).set_x(x0 + L + 0.5) for k in range(5)])
        A = axes([0, 1], [0, 1], x_length=4.6, y_length=3.6, xlabel=r"$x$", ylabel=r"the Cantor function", xticks=[0, 1 / 3, 2 / 3, 1],
                 yticks=[0, 0.5, 1], xfmt=lambda v: {0: "0", 1 / 3: r"\tfrac13", 2 / 3: r"\tfrac23", 1: "1"}[v], center=[3.6, 0.4, 0])
        ax = A.ax
        cf = polyline(ax, d["x"], d["c"], LIMC, 3)
        side = fit_rows(VGroup(
            label(r"remove middle thirds forever: \ length $(2/3)^k \to 0$", font_size=22, color=LAWC),
            label(r"yet uncountable: \ ternary digits 0 or 2, \ like binary sequences", font_size=22, color=GREY_A),
            label(r"its CDF: \ continuous, \ flat off the set, \ no density", font_size=22, color=LIMC),
            label(r"every law $=$ atoms $+$ a density $+$ a singular part \ (Lebesgue)", font_size=22, color=GOODC),
        ), 12.4, 0.3, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Measure theory also allows laws that elementary probability had no name for. Remove the "
            "middle third of the interval, then the middle third of each piece, forever. <bookmark mark='b'/> After k steps "
            "the remaining length is two thirds to the k, which tends to zero, so the Cantor set has length zero. Yet it is "
            "uncountable: its points are the numbers whose ternary digits are all zeros and twos, which match the binary "
            "sequences one for one. <bookmark mark='c'/> Spread one unit of probability evenly over it, and the CDF is "
            "Cantor's function, the devil's staircase: continuous, so there are no atoms, and flat everywhere off the "
            "Cantor set, so there is no density either. <bookmark mark='d'/> Part two promised the general picture: by "
            "Lebesgue's decomposition, every law on the line is a mixture of atoms, a density, and a singular part like "
            "this one."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[:2]], lag_ratio=0.5), FadeIn(mtxt[:2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[2:]], lag_ratio=0.5), FadeIn(mtxt[2:]), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(A), Create(cf), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
