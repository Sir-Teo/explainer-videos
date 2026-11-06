from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono,
                                   words)


class Communication(VoiceoverScene):
    def construct(self):
        self.card()
        self.equality()
        self.lower()
        self.streaming()

    def card(self):
        card = chapter_card(4, r"Communication complexity", r"How many bits must two people exchange?",
                            lit=(1979,), extra=((1979, r"Yao"),), part=PART)
        with self.voiceover("Chapter four. Communication complexity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def equality(self):
        e = load("equality")
        head = label(r"Are our strings equal?", font_size=34).to_edge(UP, buff=0.3)
        alice = VGroup(RoundedRectangle(width=2.4, height=1.0, corner_radius=0.1, color=DATA).set_fill(DATA, 0.12),
                       label(r"Alice: \ $x \in \{0,1\}^n$", font_size=20, color=DATA))
        bob = VGroup(RoundedRectangle(width=2.4, height=1.0, corner_radius=0.1, color=HEAD).set_fill(HEAD, 0.12),
                     label(r"Bob: \ $y \in \{0,1\}^n$", font_size=20, color=HEAD))
        for g in (alice, bob):
            g[1].move_to(g[0])
        VGroup(alice, bob).arrange(RIGHT, buff=4.0).next_to(head, DOWN, buff=0.5)
        msg = Arrow(alice.get_right(), bob.get_left(), buff=0.1, color=YES)
        ml = label(r"$r$, \ $x(r) \bmod q$", font_size=20, color=YES).next_to(msg, UP, buff=0.08)
        rows = [[words(r["n"]), words(r["det_bits"]), str(r["rand_bits"])] for r in e["rows"]]
        tab = grid_table([r"$n$ bits each", r"deterministic", r"randomized"], rows, widths=[2.8, 3.0, 2.4],
                         row_h=0.42, font_size=20, mono_cols=(), colors=[[WHITE, NO, YES]] * len(rows))
        tab.next_to(VGroup(alice, bob), DOWN, buff=0.5).to_edge(LEFT, buff=0.9)
        notes = VGroup(
            label(r"read each string as a polynomial; \\ send one random point and its value \\ (Part 20's "
                  r"fingerprints, \ as a protocol)", font_size=20, color=WHITE),
            label(rf"strings of {words(e['n'])} bits differing in one place, \\ $q$ = {words(e['q'])}: \ "
                  rf"{e['wrong']} wrong in {words(e['trials'])} trials \\ (bound $n/q$ = 0.001)", font_size=20,
                  color=YES),
            label(r"deterministically, \ $n$ bits are \textbf{necessary}: \\ next slide", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, RIGHT, buff=0.6).align_to(tab, UP)
        fit_right(notes)
        with self.voiceover(
            "In 1979 Andrew Yao asked a clean question: if Alice holds one input and Bob another, how many bits must "
            "they exchange to compute something about both? <bookmark mark='a'/> Take equality. Are two n-bit "
            "strings the same? <bookmark mark='b'/> With randomness it is cheap. Alice treats her string as a "
            "polynomial, picks a random point, and sends the point and the value: Part 20's fingerprint as a "
            "protocol. Different strings agree at a random point with probability at most n over q. <bookmark "
            "mark='c'/> On strings of a thousand bits differing in a single place, with a field of a million, our "
            "twenty thousand trials never erred. For strings of a trillion bits, a hundred and sixty-two bits are enough. <bookmark "
            "mark='d'/> Without randomness, Alice must send all n bits, and that can be proved."
        ) as vo:
            self.play(FadeIn(head), FadeIn(alice), FadeIn(bob))
            vo.wait_until("b")
            self.play(GrowArrow(msg), FadeIn(ml), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def lower(self):
        head = label(r"Lower bounds: \ fooling sets and rank", font_size=34).to_edge(UP, buff=0.3)
        n = 3
        N = 1 << n
        cells = VGroup()
        for i in range(N):
            for j in range(N):
                sq = Square(side_length=0.42, stroke_color=GREY_B, stroke_width=1,
                            fill_color=YES if i == j else BG, fill_opacity=0.7)
                sq.move_to(LEFT * 4.8 + RIGHT * j * 0.42 + UP * 1.4 + DOWN * i * 0.42)
                cells.add(VGroup(sq, mono("1" if i == j else "0", 14, WHITE).move_to(sq)))
        cl = label(r"the matrix $M_{xy} = [x = y]$ \ for $n = 3$", font_size=19, color=GREY_A).next_to(cells, DOWN,
                                                                                                    buff=0.15)
        lines = VGroup(
            label(r"a protocol exchanging $c$ bits splits the matrix into $\le 2^c$ \textbf{rectangles}, \\ each "
                  r"all-0 or all-1", font_size=21, color=WHITE),
            label(r"no rectangle can hold two diagonal 1s: \ $(x, x)$ and $(y, y)$ would force $(x, y)$ to be 1 too",
                  font_size=21, color=DATA),
            label(r"so $2^n$ rectangles are needed: \ $c \ge n$ \ (a \textbf{fooling set})", font_size=21, color=NO),
            label(r"the same from linear algebra: \ $c \ge \log_2 \operatorname{rank} M$ \ (Mehlhorn and Schmidt, "
                  r"1982)", font_size=21, color=HEAD),
            label(r"\textbf{disjointness}: \ do our sets intersect? \ $\Omega(n)$ bits even \textbf{with} "
                  r"randomness \\ (Kalyanasundaram and Schnitger; \ Razborov)", font_size=21, color=LAM),
            label(r"the \textbf{log-rank conjecture} \ (Lov\'asz and Saks, 1988): \ is $\log \operatorname{rank}$ "
                  r"always close to the truth? \ Open", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(cells, RIGHT, buff=0.6).align_to(cells, UP)
        fit_right(lines)
        with self.voiceover(
            "How do you prove that a protocol needs many bits? <bookmark mark='a'/> Write the function as a matrix, "
            "Alice's input for the row, Bob's for the column. A protocol that exchanges c bits cuts this matrix into "
            "at most two to the c rectangles, each constant. <bookmark mark='b'/> For equality the matrix is the "
            "identity. No rectangle can contain two diagonal ones, because a rectangle containing x, x and y, y also "
            "contains x, y, which is zero. <bookmark mark='c'/> So two to the n rectangles are needed, and n bits. "
            "<bookmark mark='d'/> Linear algebra gives the same bound through the rank of the matrix. <bookmark "
            "mark='e'/> Some functions resist even randomness. Deciding whether two sets intersect needs a linear "
            "number of bits, randomized or not. <bookmark mark='f'/> And whether the logarithm of the rank always "
            "predicts the true cost, up to a polynomial, is the log-rank conjecture, open since 1988."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cl))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def streaming(self):
        head = label(r"Why streaming algorithms must approximate", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"a streaming algorithm with $s$ bits of memory is a one-way protocol: \\ Alice runs it on her half "
                  r"of the stream \ and sends the $s$ bits to Bob", font_size=22, color=WHITE),
            label(r"so a stream question that would solve disjointness needs $s = \Omega(n)$", font_size=22,
                  color=DATA),
            label(r"exact distinct counts, \ exact frequency moments, \ the most frequent item: \ all linear space",
                  font_size=22, color=NO),
            label(r"Alon, \ Matias and Szegedy \ (1996): \ the lower bounds behind Part 20's sketches", font_size=22,
                  color=HEAD),
            label(r"so HyperLogLog and Count-Min approximate \textbf{because they must}", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.38).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "This explains a design choice from Part 20. <bookmark mark='a'/> A streaming algorithm with s bits of "
            "memory is a one-way protocol: Alice runs it on the first half of the stream and hands its memory to "
            "Bob. <bookmark mark='b'/> So any stream question that would answer disjointness needs linear memory. "
            "<bookmark mark='c'/> Exact distinct counts, exact frequency moments and the exact most frequent item "
            "all fall this way. <bookmark mark='d'/> Noga Alon, Yossi Matias and Mario Szegedy proved these bounds "
            "in 1996, alongside the sketches. <bookmark mark='e'/> HyperLogLog and Count-Min approximate because they "
            "must."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
