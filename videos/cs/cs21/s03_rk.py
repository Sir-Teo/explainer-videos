from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class RabinKarp(VoiceoverScene):
    def construct(self):
        self.card()
        self.rolling()
        self.measured()

    def card(self):
        card = chapter_card(2, r"Rolling hashes", r"Can one number stand for a whole window?", lit=(1987,),
                            extra=((1987, r"Karp--Rabin"),), part=PART)
        with self.voiceover("Chapter two. Rolling hashes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rolling(self):
        head = label(r"Compare fingerprints, \ not characters", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"read a window of $m$ characters as a number in base $b$, \ modulo a prime $p$", font_size=22,
                  color=WHITE),
            MathTex(r"h(t_i \dots t_{i+m-1}) = \Big(\sum_{k=0}^{m-1} t_{i+k}\, b^{\,m-1-k}\Big) \bmod p", font_size=34,
                    color=LAM),
            label(r"slide by one: \ drop the first character, \ shift, \ add the next", font_size=22, color=WHITE),
            MathTex(r"h_{i+1} = \big( (h_i - t_i\, b^{\,m-1})\, b + t_{i+m} \big) \bmod p", font_size=36, color=YES),
            label(r"$O(1)$ per position; \ compare characters only when the fingerprints agree", font_size=22,
                  color=HEAD),
            label('fixed unequal byte windows, \\ prime $p>255$, \\ uniform $b\\in\\mathbb F_p$: \\ collision $\\le(m-1)/p$', font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.26).next_to(head, DOWN, buff=0.35)
        digits, m, p = "2359023141526739921", 5, 13
        strip = VGroup(*[VGroup(Square(side_length=0.48, stroke_color=GREY_B, stroke_width=1.5), mono(c, 22, WHITE))
                         for c in digits]).arrange(RIGHT, buff=0)
        for c in strip:
            c[1].move_to(c[0])
        strip.to_edge(DOWN, buff=1.05)
        win = SurroundingRectangle(VGroup(*strip[0:m]), color=YES, buff=0.03, stroke_width=3)

        def tag(i):
            v = int(digits[i:i + m])
            return label(rf"${v} \bmod {p} = {v % p}$", font_size=22, color=YES if v % p == 31415 % p else LAM
                         ).next_to(VGroup(*strip[i:i + m]), DOWN, buff=0.15)
        pt = label(rf"looking for $31415$: \ $31415 \bmod {p} = {31415 % p}$ \ (base $b = 10$, \ $m = {m}$)",
                   font_size=19, color=GREY_A).next_to(strip, UP, buff=0.2)
        with self.voiceover(
            "Richard Karp and Michael Rabin, in 1987, used Part 20's fingerprints. <bookmark mark='a'/> Read each window of m characters as a number in base b, modulo a prime p, and compare it with the pattern's number. <bookmark mark='b'/> Sliding the window by one place doesn't need a fresh sum: <bookmark mark='c'/> subtract the character that leaves, multiply by the base, and add the one that arrives. <bookmark mark='d'/> That is a constant amount of work per position, and characters are compared only when the two numbers agree. <bookmark mark='e'/> For two fixed unequal byte windows, choose a prime larger than 255 and a base uniformly in its field. They give the same number only if a nonzero polynomial of degree m minus one vanishes at that base, which Schwartz–Zippel says happens with probability at most m minus one over p."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            t = tag(0)
            self.play(FadeIn(strip), FadeIn(pt), Create(win), FadeIn(t))
            vo.wait_until("b")
            self.play(FadeIn(lines[2], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(lines[3], shift=UP * 0.1))
            for i in range(1, 8):
                nt = tag(i)
                self.play(win.animate.move_to(VGroup(*strip[i:i + m])), Transform(t, nt), run_time=0.45)
                if digits[i:i + m] == "31415":
                    self.play(Indicate(win, color=YES), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(lines[4], shift=UP * 0.1))
            for i in range(8, len(digits) - m + 1):
                nt = tag(i)
                self.play(win.animate.move_to(VGroup(*strip[i:i + m])), Transform(t, nt), run_time=0.3)
                if digits[i:i + m] != "31415" and int(digits[i:i + m]) % p == 31415 % p:
                    self.play(Indicate(win, color=NO), run_time=0.5)
                if digits[i:i + m] == "31415":
                    self.play(Indicate(win, color=YES), run_time=0.6)
            vo.wait_until("e")
            self.play(FadeIn(lines[5], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("rk")
        head = label(rf"\texttt{{{d['pattern']}}} \ in \textit{{Moby-Dick}}, \ by fingerprint", font_size=32
                     ).to_edge(UP, buff=0.35)
        rows = [[words(r["mod"]), words(r["spurious"]), f"{r['expected']:,.1f}", words(r["cmp"]), words(r["hits"])]
                for r in d["rows"]]
        tab = grid_table([r"modulus $p$", r"false alarms", 'heuristic windows/$p$', r"character comparisons",
                          r"found"], rows, widths=[2.4, 2.2, 2.8, 3.4, 1.4], row_h=0.44, font_size=20, mono_cols=(),
                         colors=[[LAM, NO, HEAD, GREY_A, YES]] * len(rows)).next_to(head, DOWN, buff=0.45)
        tab.set_x(0)
        notes = VGroup(
            label('fixed base 256 here; \\ every fingerprint match is checked exactly', font_size=21,
                  color=WHITE),
            label(r"its strength: \ many patterns of one length at once \ (a hash set of fingerprints), \ and "
                  r"the 2D version for images", font_size=21, color=GREY_A),
            label(r"its descendants: \ rsync, \ deduplication, \ plagiarism detection \ (chapter 14)", font_size=21,
                  color=CTRL),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            f"Here is Queequeg in Moby-Dick, {words(d['n'])} bytes. This experiment fixes the base at 256. <bookmark mark='a'/> The windows-over-modulus column is a heuristic reference, not a randomized expectation for this fixed text and base. The small modulus produces many false alarms; every one is rejected by exact byte comparisons. <bookmark mark='b'/> Larger moduli have fewer false alarms in these observations. Randomizing the base would give the polynomial bound from the previous screen, with a prime larger than the byte alphabet. <bookmark mark='c'/> Fingerprints can also screen many equal-length patterns at once, before exact verification, and extend to two-dimensional matching. <bookmark mark='d'/> Rolling updates return in rsync and deduplicating backups."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[3:]], lag_ratio=0.3), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
