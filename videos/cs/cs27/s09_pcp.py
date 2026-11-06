from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono)


class Pcp(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.linearity()
        self.dinur()

    def card(self):
        card = chapter_card(8, r"The PCP theorem", r"How few bits of a proof must you read?", lit=(1992, 2005),
                            extra=((1992, r"Arora--Safra; \ ALMSS"), (2005, r"Dinur")), part=PART)
        with self.voiceover("Chapter eight. The PCP theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def theorem(self):
        head = label(r"Probabilistically checkable proofs", font_size=34).to_edge(UP, buff=0.3)
        bits = VGroup(*[Square(side_length=0.2, stroke_color=GREY_D, stroke_width=0.5,
                               fill_color=DATA if (i * 37 + 11) % 5 < 2 else BG, fill_opacity=0.9)
                        for i in range(320)]).arrange_in_grid(rows=5, cols=64, buff=0.02)
        bits.scale_to_fit_width(12.6).next_to(head, DOWN, buff=0.45)
        picks = [17, 141, 290]
        marks = VGroup(*[SurroundingRectangle(bits[i], color=HEAD, buff=0.03, stroke_width=3) for i in picks])
        bl = label(r"a proof of polynomial length, \ written in a special robust format", font_size=19,
                   color=GREY_A).next_to(bits, DOWN, buff=0.12)
        lines = VGroup(
            label(r"\textbf{PCP}$(O(\log n), O(1))$: \ the verifier uses $O(\log n)$ random bits \ and reads only "
                  r"\textbf{a constant number} of bits of the proof", font_size=22, color=WHITE),
            label(r"a correct proof of a true statement is always accepted", font_size=22, color=YES),
            label(r"for a false statement, \ \textbf{every} purported proof is rejected with probability $\ge "
                  r"\tfrac12$", font_size=22, color=NO),
            label(r"\textbf{the PCP theorem}: \ NP = PCP$(O(\log n), O(1))$ \ (Arora--Safra; \ Arora, \ Lund, \ "
                  r"Motwani, \ Sudan, \ Szegedy, \ 1992)", font_size=22, color=HEAD),
            label(r"H\aa stad \ (2001): \ 3 bits are enough, \ with error just above $\tfrac12$", font_size=22,
                  color=LAM),
        ).arrange(DOWN, buff=0.25).next_to(bl, DOWN, buff=0.4)
        with self.voiceover(
            "Here is the most surprising theorem in this part. <bookmark mark='a'/> Take any statement with an NP "
            "proof, say that a formula is satisfiable. The proof can be rewritten, in polynomial length, in a special "
            "robust format, so that a verifier who flips a logarithmic number of coins and reads just a constant "
            "number of bits of it can check it. <bookmark mark='b'/> A correct proof is always accepted. <bookmark "
            "mark='c'/> If the statement is false, every purported proof is rejected at least half the time. "
            "<bookmark mark='d'/> That is the PCP theorem, proved in 1992 by Sanjeev Arora and Shmuel Safra, and "
            "Arora, Carsten Lund, Rajeev Motwani, Madhu Sudan and Mario Szegedy. <bookmark mark='e'/> Johan Håstad "
            "later showed that three bits suffice. Reading three bits of a proof, chosen at random, is as convincing "
            "as reading all of it, given a proof written the right way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bits), FadeIn(bl))
            vo.wait_until("a")
            self.play(Create(marks), FadeIn(lines[0]))
            for mk, ln in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def linearity(self):
        b = load("blr")
        head = label(r"A 3-bit test you can run: \ linearity", font_size=32).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 0.45, 0.1], y_range=[0, 0.55, 0.1], x_length=5.4, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.6).to_edge(
            LEFT, buff=1.0)
        pts = VGroup(*[Dot(ax.c2p(r["distance"], r["reject"]), radius=0.06, color=HEAD) for r in b["rows"]])
        curve = ax.plot(lambda d: 3 * d - 6 * d * d, x_range=[0, 0.25], color=YES, stroke_width=2.5)
        xl = label(r"distance from the nearest linear function", font_size=17, color=GREY_A).next_to(ax, DOWN,
                                                                                                   buff=0.3)
        yl = label(r"rejection probability", font_size=17, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT, buff=0.3)
        ticks = VGroup(*[label(f"{x:g}", font_size=14, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                         for x in (0.1, 0.2, 0.3, 0.4)],
                       *[label(f"{y:g}", font_size=14, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                         for y in (0.1, 0.3, 0.5)])
        cl = label(r"$3\delta - 6\delta^2$", font_size=20, color=YES).next_to(ax.c2p(0.25, 0.375), DR, buff=0.1)
        notes = VGroup(
            label(r"is $f: \{0,1\}^8 \to \{0,1\}$ a parity of some subset of bits?", font_size=20, color=WHITE),
            label(r"\textbf{BLR test} \ (Blum, \ Luby, \ Rubinfeld, 1990): \\ pick random $x, y$; \ check $f(x) + "
                  r"f(y) = f(x \oplus y)$", font_size=20, color=DATA),
            label(r"three queries; \ linear functions always pass", font_size=20, color=YES),
            label(r"we corrupted a linear function in $t$ places \\ and computed the exact rejection rate", font_size=20,
                  color=GREY_A),
            label(r"small distance $\delta$: \ rejection $\approx 3\delta - 6\delta^2$, \\ the bound of Bellare et al. "
                  r"(1996)", font_size=20, color=HEAD),
            label(r"far from linear $\Rightarrow$ caught often: \\ the kind of robustness PCPs are built from",
                  font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "The full proof is long, but its flavour fits in a small experiment. <bookmark mark='a'/> Is a Boolean "
            "function on eight bits a parity, the exclusive or of some subset of its inputs? <bookmark mark='b'/> "
            "Manuel Blum, Michael Luby and Ronitt Rubinfeld proposed a test: pick two random inputs x and y, and "
            "check that f of x plus f of y equals f of x exclusive-or y. <bookmark mark='c'/> It reads three values, "
            "and parities always pass. <bookmark mark='d'/> We took a parity, corrupted it in more and more places, "
            "and computed the exact probability that the test rejects. <bookmark mark='e'/> For small distances it "
            "follows three delta minus six delta squared, the bound proved by Mihir Bellare and coauthors. <bookmark "
            "mark='f'/> A function far from every parity is caught often. PCP constructions encode proofs so that "
            "every wrong proof is far from every right one, and tests like this one find the difference."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks), FadeIn(notes[0]))
            for mk, n_ in zip("bcd", notes[1:4]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1))
            vo.wait_until("e")
            self.play(Create(curve), FadeIn(cl), FadeIn(notes[4]))
            vo.wait_until("f")
            self.play(FadeIn(notes[5]))
        self.wait(0.3)
        self.clear_scene()

    def dinur(self):
        head = label(r"Dinur's proof \ (2005): \ amplify the gap", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"view the PCP theorem as a statement about constraint graphs: \ some constant fraction of "
                  r"constraints must be violated", font_size=21, color=WHITE),
            label(r"start: \ an NP-hard graph where unsatisfiable means \textbf{at least one} violated constraint",
                  font_size=21, color=DATA),
            label(r"each step: \ make the graph an \textbf{expander} \ (Part 56), \ take walks: \ the violated "
                  r"fraction \textbf{doubles}", font_size=21, color=HEAD),
            label(r"then shrink the alphabet back down \ (composition), \ losing only a constant", font_size=21,
                  color=LAM),
            label(r"after $O(\log n)$ steps: \ a constant fraction violated, \ in polynomial size: \ the PCP theorem",
                  font_size=21, color=YES),
            label(r"a 1992 proof of algebra and coding theory, \ redone combinatorially in about 40 pages",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "In 2005 Irit Dinur gave a new proof, combinatorial and much shorter. <bookmark mark='a'/> Think of a "
            "proof as an assignment to a graph of constraints. <bookmark mark='b'/> Satisfiability already gives a "
            "graph where, if the formula is unsatisfiable, at least one constraint fails: a gap of one constraint. "
            "<bookmark mark='c'/> Each step of Dinur's proof turns the graph into an expander, the kind Part 56 "
            "studies, and replaces constraints by walks on it, doubling the fraction of violated constraints. "
            "<bookmark mark='d'/> A second step shrinks the alphabet back down, losing only a constant factor. "
            "<bookmark mark='e'/> After logarithmically many rounds, a constant fraction of constraints must fail, "
            "and the graph is still polynomial: that is the PCP theorem. <bookmark mark='f'/> A result first proved "
            "with heavy algebra became a forty-page combinatorial argument."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
