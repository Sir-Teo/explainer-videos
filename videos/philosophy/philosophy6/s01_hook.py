from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.question()
        self.preview()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"No one shall expel us from the paradise that Cantor has created.", r"David Hilbert",
                       r"`On the infinite' (1926)", width=10.0, font_size=28).next_to(t, DOWN, buff=0.7)
        with self.voiceover(
            "Part 6 is about the infinite, and about the theory that tamed it: the theory of sets. "
            "<bookmark mark='a'/>In 1926 David Hilbert declared that no one would expel mathematicians from the "
            "paradise that Georg Cantor had created. <bookmark mark='b'/>The paradise was real. So were the "
            "snakes: paradoxes that brought down the first theory of sets, and questions, like the size of the "
            "continuum, that its axioms can provably never answer."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=GOAL, scale_factor=1.02))
        self.clear_scene()

    def question(self):
        d = load("hotel")
        head = label(r"Are there more natural numbers than squares?", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        top = VGroup(*[MathTex(str(a), font_size=34) for a, _ in d["squares"]]).arrange(RIGHT, buff=0.55)
        bot = VGroup(*[MathTex(str(b), font_size=34, color=GOAL) for _, b in d["squares"]])
        for t, b in zip(top, bot):
            b.next_to(t, DOWN, buff=1.0)
        lines = VGroup(*[Line(t.get_bottom(), b.get_top(), buff=0.1, color=SETC, stroke_width=2) for t, b in
                         zip(top, bot)])
        g = VGroup(top, bot, lines).move_to([0, 0.2, 0])
        yes = label(r"most numbers are not squares: \ \textit{more} numbers", font_size=26, color=GREY_A).to_edge(
            DOWN, buff=1.1)
        no = label(r"but each number has its own square: \ \textit{as many}", font_size=26, color=GOAL).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "Here is the question that started it. <bookmark mark='a'/>Are there more natural numbers than square "
            "numbers? <bookmark mark='b'/>Surely yes: most numbers are not squares, and the squares thin out as "
            "they grow. <bookmark mark='c'/>Surely no: pair each number with its square, one, four, nine, sixteen, "
            "and nothing is left over on either side. Galileo saw this in 1638 and concluded that 'more' and 'as "
            "many' make no sense for infinite collections. Cantor concluded the opposite: they make perfect sense, "
            "and they lead somewhere astonishing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top))
            vo.wait_until("b")
            self.play(FadeIn(yes))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(Create(ln), FadeIn(b)) for ln, b in zip(lines, bot)],
                                  lag_ratio=0.15), FadeIn(no))
        self.clear_scene()

    def preview(self):
        d = load("diagonal")
        tab = bit_table(d["rows"], cell=0.42).move_to([-3.0, 0.2, 0])
        diag = VGroup(*[SurroundingRectangle(tab.cell[i][i], buff=0.0, color=GOAL, stroke_width=3)
                        for i in range(len(d["rows"]))])
        new = bit_table([d["diagonal"]], cell=0.42).next_to(tab, DOWN, buff=0.5)
        nl = label(r"flip the diagonal: \ a row that is not in the list", font_size=24, color=GOAL).next_to(
            new, DOWN, buff=0.25)
        bricks = VGroup(label(r"this part's two bricks in the Wall:", font_size=26, color=P.WALL),
                        label(r"Russell's paradox \ (1902): \ not every condition defines a set", font_size=26),
                        label(r"Cohen \ (1963): \ the axioms cannot settle the continuum", font_size=26)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.3, 0])
        with self.voiceover(
            "Two pictures will carry us through. <bookmark mark='a'/>The first is Cantor's diagonal: a list of "
            "infinite rows of zeros and ones, and a new row built by flipping the diagonal, which differs from every "
            "row in the list. It proves there are different sizes of infinity. <bookmark mark='b'/>The second is a "
            "wall. This part lays two bricks: Russell's paradox, which shows that not every condition defines a set, "
            "and Paul Cohen's theorem of 1963, which shows that the standard axioms cannot decide how many real "
            "numbers there are."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab))
            self.play(LaggedStart(*[Create(r) for r in diag], lag_ratio=0.15))
            self.play(FadeIn(new), FadeIn(nl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in bricks], lag_ratio=0.4))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Galileo's paradox, \ Hilbert's hotel, \ Dedekind's definition of the infinite",
            r"Cantor: \ the rationals are countable, \ the reals are not; \ the diagonal, drawn",
            r"Cantor's absolute and its critics; \ Russell's letter; \ the axioms of Zermelo and Fraenkel",
            r"sets built from nothing; \ the cumulative hierarchy",
            r"ordinals to $\varepsilon_0$, \ Goodstein's sequences and the hydra, \ the alephs",
            r"the axiom of choice and Banach--Tarski; \ the continuum hypothesis and forcing",
            r"large cardinals and determinacy; \ does CH have an answer?",
        ], font_size=25)
        with self.voiceover(
            "So: <bookmark mark='a'/>first the hotel and Galileo's paradox. <bookmark mark='b'/>Then Cantor's "
            "proofs, that the fractions can be counted and the real numbers cannot. <bookmark mark='c'/>Then Cantor's "
            "critics, the paradox that broke Frege's system, and the axioms that replaced it. <bookmark mark='d'/>We build sets "
            "out of nothing, and stack them in a hierarchy. <bookmark mark='e'/>We count past infinity with "
            "ordinals, and meet a sequence of numbers that grows for longer than the universe will last, and then "
            "comes back to zero, and a monster that Hercules always defeats. <bookmark mark='f'/>Then choice, a theorem that doubles a ball, and the continuum "
            "problem. <bookmark mark='g'/>And at the end, a question for philosophers: when the axioms run out, "
            "is there still a fact of the matter?"
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
