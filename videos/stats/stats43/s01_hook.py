from __future__ import annotations

from videos.stats.stats43.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.hilbert()
        self.kolmogorov()
        self.upgrades()
        self.objectives()

    def hilbert(self):
        tl = timeline(lit=(1900, 1933)).to_edge(UP, buff=0.35)
        hc = history_card(1900, r"David Hilbert, \ \emph{Mathematical Problems}, \ Paris",
                          r"twenty-three problems for the new century, \ ten of them read aloud to the International "
                          r"Congress of Mathematicians; \ the sixth asks for axioms for physics",
                          color=LAWC, width=11.0, font_size=23).move_to([0, 0.9, 0])
        q = VGroup(
            label(r"``To treat in the same manner, \ by means of axioms, \ those physical sciences", font_size=26),
            label(r"in which already today mathematics plays an important part;", font_size=26),
            label(r"in the first rank are the theory of probabilities and mechanics.''", font_size=26),
        ).arrange(DOWN, buff=0.18).move_to([0, -1.6, 0])
        q[2].set_color(S.ACCENT)
        with self.voiceover(
            "<bookmark mark='a'/> In August 1900, in Paris, David Hilbert set the International Congress of Mathematicians "
            "twenty-three problems, the ones he thought the new century should solve; there was time to read ten of "
            "them aloud. <bookmark mark='b'/> The "
            "sixth asked for axioms for physics: to treat in the same manner, by means of axioms, those physical sciences "
            "in which already today mathematics plays an important part. <bookmark mark='c'/> And it named the first two: "
            "the theory of probabilities, and mechanics. Probability, in 1900, had results, from Bernoulli's law to "
            "Laplace's central limit theorem, but no agreed definition of what a probability is, or of what a random "
            "variable is."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(q[0]), FadeIn(q[1]))
            vo.wait_until("c")
            self.play(FadeIn(q[2]))
        self.clear_scene()

    def kolmogorov(self):
        hc = history_card(1933, r"A. N. Kolmogorov, \ \emph{Grundbegriffe der Wahrscheinlichkeitsrechnung}",
                          r"sixty-two pages in a German monograph series; \ built on Lebesgue's measure (1902) and on "
                          r"Borel's and Fr\'echet's work: \ probability becomes a branch of measure theory",
                          color=LAWC, width=11.0, font_size=23).move_to([0, 1.7, 0])
        rows = fit_rows(VGroup(
            label(r"a probability space: \ $(\Omega, \mathcal F, P)$, \ $P$ a measure with $P(\Omega) = 1$", font_size=26),
            label(r"an event: \ a set in the $\sigma$-algebra $\mathcal F$", font_size=26, color=GREY_A),
            label(r"a random variable: \ a measurable function $X : \Omega \to \mathbb R$", font_size=26, color=LAWC),
            label(r"an expectation: \ a Lebesgue integral $\int X \, dP$", font_size=26, color=GREY_A),
            label(r"a conditional expectation: \ a Radon--Nikodym derivative", font_size=26, color=GREY_A),
        ), 12.4, 0.36, [0, -1.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The answer came in 1933, in sixty-two pages by Andrey Kolmogorov, the Grundbegriffe, "
            "the foundations of the theory of probability. Its move was to make probability a branch of measure theory, "
            "the theory of length, area and volume that Henri Lebesgue had built thirty years earlier. <bookmark "
            "mark='b'/> A probability space is a set of outcomes, a collection of events, and a measure of total mass "
            "one. <bookmark mark='c'/> An event is a set in that collection. <bookmark mark='d'/> A random variable is a "
            "measurable function on the outcomes. <bookmark mark='e'/> An expectation is a Lebesgue integral. <bookmark "
            "mark='f'/> And a conditional expectation, the hardest idea of the old theory, became a Radon–Nikodym "
            "derivative. Every limit theorem in this course rests on these definitions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(2, r"probability is a function on events, \ additive over disjoint ones",
                         r"that every set of outcomes is an event", r"chapter 1: \ $\sigma$-algebras, \ and a set that "
                         r"cannot be measured"),
            upgrade_card(3, r"the moment generating function determines the law", r"that this was true, \ on trust",
                         r"chapter 8: \ characteristic functions, \ inversion, \ uniqueness"),
            upgrade_card(6, r"the strong law; \ the CLT by MGFs; \ Berry--Esseen's $1/\sqrt n$",
                         r"an MGF; \ the strong law and the rate without proof",
                         r"chapters 6, \ 9 and 10: \ Etemadi, \ Lindeberg, \ Stein"),
        ]
        for c in cards:
            c.scale(0.86)
        VGroup(*cards).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Three promises from the first stage are now due. Part two defined probability as an"
            " additive function on events, and quietly assumed that every set of outcomes is an event. Chapter one "
            "shows why that is impossible for rotation-invariant length on every subset of the interval, assuming the"
            " axiom of choice. An atomic probability such as a point mass can be defined on all subsets. <bookmark "
            "mark='b'/> Part three said the moment generating function determines a law, and asked you to trust it. "
            "Chapter eight proves it, with characteristic functions. <bookmark mark='c'/> And Part six stated the "
            "strong law, proved the central limit theorem only for laws with a moment generating function, and quoted"
            " Berry and Esseen's rate. Chapters six and nine explain the strong law and central limit theorem proofs."
            " Chapter ten develops Stein's method and states a published Berry–Esseen constant; it does not derive "
            "that sharp constant."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 43", font_size=34, color=GREY_B), label(r"Measure-Theoretic Probability", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"$\sigma$-algebras, \ measures, \ random variables as measurable maps, \ integration",
            r"independence and products; \ Borel--Cantelli, \ the 0--1 laws, \ the strong law",
            r"weak convergence, \ characteristic functions, \ Lindeberg--Feller, \ Stein's method",
            r"stable laws, \ large deviations, \ extremes: \ what the limit theorems say beyond the CLT",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Part 6; \ \emph{Analysis, Built} Parts 1--5").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.limits}, \ the weak-convergence lab").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-three: measure-theoretic probability, the first part of the PhD core. "
            "<bookmark mark='b'/> We'll build sigma-algebras and measures, random variables and their integrals; "
            "independence, the Borel–Cantelli lemmas and the zero–one laws, and a full proof of the strong law; weak "
            "convergence, characteristic functions, Lindeberg's theorem and Stein's method, with exact probability "
            "formulas and numerical distance calculations in a weak-convergence lab; and then what lies beyond the "
            "normal: stable laws, large deviations and extremes. Each condition that matters gets its counterexample."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
