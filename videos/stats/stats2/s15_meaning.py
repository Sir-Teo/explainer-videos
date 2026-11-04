from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403

FREQ, LOGIC, BELIEF = S.EST, S.LIK, S.PRIOR


class Meaning(VoiceoverScene):
    def construct(self):
        self.card()
        self.frequency()
        self.logic_belief()
        self.dutch_book()
        self.cox()
        self.synthesis()

    def card(self):
        card = chapter_card(14, r"What probability means", r"A frequency, a logic, or a degree of belief?",
                            lit=(1933,), part=PART)
        with self.voiceover("Chapter fourteen. What probability means."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def frequency(self):
        g = np.random.Generator(np.random.PCG64(1866))
        flips = g.integers(0, 2, 5000)
        run = np.cumsum(flips) / np.arange(1, 5001)
        A = axes([0, 5000], [0.3, 0.7], x_length=7.4, y_length=3.8, xlabel=r"tosses", ylabel=r"fraction of heads",
                 xticks=[0, 2500, 5000], yticks=[0.3, 0.5, 0.7], xfmt=lambda v: fmt_int(v), center=[-2.6, -0.5, 0])
        ax = A.ax
        idx = np.unique(np.geomspace(3, 5000, 300).astype(int)) - 1
        cv = curve(ax, idx + 1, np.clip(run[idx], 0.3, 0.7), FREQ, 2.5)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(5000, 0.5), color=EXACT, stroke_width=2)
        hc = history_card(1928, r"Richard von Mises; \ John Venn (1866)", r"probability is the limiting relative "
                          r"frequency in an endless sequence of trials", color=FREQ, width=5.4, font_size=22)
        hc.move_to([4.0, 1.9, 0])
        probs = VGroup(label(r"but: \ the long run is never observed", font_size=24, color=GREY_A),
                       label(r"and: \ what is the frequency of \emph{rain tomorrow}?", font_size=24, color=GREY_A),
                       label(r"or of \emph{this} defendant's guilt?", font_size=24, color=GREY_A))
        probs.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.0, -1.0, 0])
        tag = note(r"simulated: fair tosses").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Kolmogorov's axioms tell us how probabilities must fit together. They don't say what a probability "
            "is, and for three centuries people have disagreed. <bookmark mark='a'/> The first answer is frequency. "
            "Toss a coin again and again, and the fraction of heads settles down. On this view, championed by John "
            "Venn and then by Richard von Mises, the probability of heads simply is that limiting fraction. "
            "<bookmark mark='b'/> It's concrete and testable, and it's the meaning the Coverage Board uses. But it "
            "has problems. Nobody ever observes an infinite sequence. <bookmark mark='c'/> And many probabilities "
            "we care about are about single events: rain tomorrow, a candidate winning an election, whether this "
            "defendant committed this crime. There's no sequence of identical tomorrows."
        ) as vo:
            self.play(FadeIn(A), Create(half), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cv), run_time=3.5)
            self.play(FadeIn(hc, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(probs[0]))
            vo.wait_until("c")
            self.play(FadeIn(probs[1]), FadeIn(probs[2]))
        self.clear_scene()

    def logic_belief(self):
        c1 = history_card(1921, r"John Maynard Keynes, \ \emph{A Treatise on Probability}", r"probability is a "
                          r"logical relation: \ how far evidence supports a conclusion; \ later Jeffreys, Carnap",
                          color=LOGIC, width=6.0, font_size=22)
        c2 = history_card(1926, r"Frank Ramsey; \ Bruno de Finetti (1931, 1937)", r"probability is a degree of "
                          r"belief, \ measured by the bets you would accept: \ ``probability does not exist'' "
                          r"(de Finetti), \ outside our minds", color=BELIEF, width=6.0, font_size=22)
        VGroup(c1, c2).arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to([0, 1.3, 0])
        price = definition_card(r"A probability as a price", r"your probability for $A$ is the price $p$ at which you "
                                r"would buy \emph{or} sell a ticket paying $1$ if $A$ happens", color=BELIEF,
                                width=7.4, font_size=24).move_to([0, -1.9, 0])
        with self.voiceover(
            "Two other answers make probability about knowledge rather than about the world. <bookmark mark='a'/> "
            "The logical view, John Maynard Keynes's in 1921, is that a probability measures how strongly a body of "
            "evidence supports a conclusion, the way logic measures whether it proves it. <bookmark mark='b'/> The "
            "subjective view, Frank Ramsey's in 1926 and Bruno de Finetti's a few years later, is that a probability "
            "is a degree of belief: yours, about this. De Finetti put it provocatively: probability does not exist, "
            "outside our minds. <bookmark mark='c'/> To make belief measurable, measure it by betting. Your "
            "probability for an event is the price at which you'd be equally willing to buy or to sell a ticket that "
            "pays one if the event happens."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(price, shift=UP * 0.2))
        self.clear_scene()

    def dutch_book(self):
        prices = VGroup(MathTex(r"\text{your price for ``rain''}", r"=", r"0.6", font_size=32),
                        MathTex(r"\text{your price for ``no rain''}", r"=", r"0.6", font_size=32))
        prices.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.5)
        for p in prices:
            p[2].set_color(BELIEF)
        warn = MathTex(r"0.6 + 0.6 = 1.2 > 1", font_size=30, color=S.RESID).next_to(prices, RIGHT, buff=0.8)
        head = VGroup(*[label(t, font_size=24, color=GREY_A) for t in (r"tomorrow", r"you pay", r"you collect", r"net")])
        rows_data = [(r"it rains", r"1.20", r"1.00", r"-0.20"), (r"it doesn't", r"1.20", r"1.00", r"-0.20")]
        table = VGroup(head)
        for r in rows_data:
            table.add(VGroup(label(r[0], font_size=26), MathTex(r[1], font_size=30), MathTex(r[2], font_size=30),
                             MathTex(r[3], font_size=30, color=S.RESID)))
        for row in table:
            for k, m in enumerate(row):
                m.move_to([-3.6 + 2.6 * k, 0, 0])
        table.arrange(DOWN, buff=0.35).move_to([0, -0.6, 0])
        for row in table:
            for k, m in enumerate(row):
                m.set_x(-3.6 + 2.6 * k)
        th = theorem_card(r"the Dutch book", r"if your prices break the axioms, \ someone can trade with you so that you "
                          r"lose whatever happens. \ Prices that obey them are \emph{coherent}.", who=r"Ramsey 1926; \ "
                          r"de Finetti 1937", color=BELIEF, width=9.0, font_size=23).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Betting prices bring a surprise: they must obey Kolmogorov's axioms, or you can be exploited. "
            "<bookmark mark='a'/> Suppose you price a ticket on rain tomorrow at sixty cents, and a ticket on no "
            "rain also at sixty cents. Your probabilities add up to more than one. <bookmark mark='b'/> A bookmaker "
            "sells you both tickets. You pay a dollar twenty. <bookmark mark='c'/> Tomorrow, exactly one ticket "
            "pays: a dollar. Rain or shine, you've lost twenty cents. <bookmark mark='d'/> That's called a Dutch "
            "book, and the theorem of Ramsey and de Finetti says it's avoidable exactly when your prices satisfy the "
            "rules of probability. Coherence, the requirement that nobody can make you a sure loser, forces "
            "nonnegativity, normalization and additivity. A subjectivist ends up with the same mathematics as a "
            "frequentist, for a different reason."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(prices))
            self.play(Write(warn))
            vo.wait_until("b")
            self.play(FadeIn(table[0]), FadeIn(VGroup(*[r[:2] for r in table[1:]])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*[r[2:] for r in table[1:]])))
            vo.wait_until("d")
            self.play(FadeIn(th, shift=UP * 0.2))
        self.clear_scene()

    def cox(self):
        th = theorem_card(r"Cox's theorem", r"any way of grading the plausibility of statements by real numbers, \ "
                          r"consistent with logic and with a few requirements of common sense, \ is equivalent to "
                          r"probability", who=r"R. T. Cox, 1946; \ E. T. Jaynes; \ exact conditions: Halpern (1999)",
                          color=LOGIC, width=9.6, font_size=24).move_to([0, 1.0, 0])
        tri = VGroup(label(r"frequency", font_size=30, color=FREQ), label(r"logic", font_size=30, color=LOGIC),
                     label(r"belief", font_size=30, color=BELIEF))
        tri.arrange(RIGHT, buff=2.0).move_to([0, -1.6, 0])
        ax_l = label(r"the same axioms", font_size=28, color=EXACT).move_to([0, -2.6, 0])
        arrows = VGroup(*[Arrow(t.get_bottom(), ax_l.get_top(), buff=0.1, color=GREY_B, stroke_width=2) for t in tri])
        with self.voiceover(
            "The logical view has its own theorem. <bookmark mark='a'/> In 1946 the physicist Richard Cox showed "
            "that any system for grading the plausibility of statements with real numbers, consistent with ordinary "
            "logic and a few common-sense requirements, has to be equivalent to probability. The exact conditions "
            "turned out to need care, as Joseph Halpern showed in 1999, but the message stands. "
            "<bookmark mark='b'/> Three meanings, three arguments, and they all arrive at the same three axioms."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in tri], lag_ratio=0.3))
            self.play(*[GrowArrow(a) for a in arrows], FadeIn(ax_l))
        self.clear_scene()

    def synthesis(self):
        left = VGroup(label(r"frequentist", font_size=32, color=FREQ),
                      label(r"$P$ describes repeatable experiments", font_size=24),
                      label(r"methods graded by how often they err", font_size=24),
                      label(r"the Coverage Board: \ Parts 8, 11, \dots", font_size=22, color=GREY_B))
        right = VGroup(label(r"Bayesian", font_size=32, color=BELIEF),
                       label(r"$P$ describes what is known", font_size=24),
                       label(r"beliefs updated by Bayes' theorem", font_size=24),
                       label(r"Part 15, \ and Parts 26--27", font_size=22, color=GREY_B))
        for g in (left, right):
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to([0, 0.6, 0])
        bridge = label(r"this series uses both, \ and checks each against the World", font_size=30,
                       color=S.ACCENT).to_edge(DOWN, buff=1.0)
        later = label(r"the argument between them: \ Part 26", font_size=22, color=GREY_B).next_to(bridge, DOWN, buff=0.2)
        with self.voiceover(
            "In practice, statistics divides along this line. <bookmark mark='a'/> Frequentist statistics treats "
            "probability as a property of repeatable experiments, and grades methods by how often they're wrong: "
            "that's the promise the Coverage Board checks. <bookmark mark='b'/> Bayesian statistics treats "
            "probability as a description of what's known, and updates it with Bayes' theorem, as we did with the "
            "screening test. <bookmark mark='c'/> This series uses both, because both work, and because in the "
            "World we can check either kind of claim against the truth. The argument between them is old and "
            "sometimes bitter, and Part 26 tells it properly."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(bridge, shift=UP * 0.2), FadeIn(later))
        self.clear_scene()
