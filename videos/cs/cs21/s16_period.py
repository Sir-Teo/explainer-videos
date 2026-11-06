from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import strings as St
from videos.cs.cs21.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Period(VoiceoverScene):
    def construct(self):
        self.card()
        self.fine_wilf()
        self.palindromes()
        self.lyndon()

    def card(self):
        card = chapter_card(15, r"Periods, \ palindromes and Lyndon words", r"What structure hides inside one string?",
                            lit=(1965, 1975), extra=((1965, r"Fine--Wilf"), (1975, r"Manacher")), part=PART)
        with self.voiceover("Chapter fifteen. Periods, palindromes and Lyndon words."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def fine_wilf(self):
        head = label(r"Periods", font_size=36).to_edge(UP, buff=0.35)
        w = "abaababaaba"
        per = St.periods(w.encode())
        cells = VGroup(*[VGroup(Square(side_length=0.62, stroke_color=DATA, stroke_width=1.5), mono(c, 26, WHITE))
                         for c in w]).arrange(RIGHT, buff=0)
        for c in cells:
            c[1].move_to(c[0])
        cells.move_to(UP * 1.15)
        arcs5 = VGroup(*[ArcBetweenPoints(cells[i].get_top(), cells[i + 5].get_top(), angle=-0.8, color=YES,
                                          stroke_width=1.6) for i in range(len(w) - 5)])
        arcs8 = VGroup(*[ArcBetweenPoints(cells[i].get_bottom(), cells[i + 8].get_bottom(), angle=0.6, color=HEAD,
                                          stroke_width=1.6) for i in range(len(w) - 8)])
        t5 = mono("p = 5", 18, YES).next_to(arcs5, UP, buff=0.08)
        t8 = mono("p = 8", 18, HEAD).next_to(arcs8, DOWN, buff=0.08)
        lines = VGroup(
            label(rf"$p$ is a period if $s_i = s_{{i+p}}$ wherever both exist: \ \texttt{{{w}}} has periods "
                  rf"{', '.join(str(p) for p in per)}", font_size=21, color=WHITE),
            label(r"the periods are $n$ minus the borders: \ KMP's failure function lists them all", font_size=21,
                  color=GREY_A),
            MathTex(r"\text{periods } p, q \text{ and } n \ge p + q - \gcd(p, q) \;\Longrightarrow\; \gcd(p, q) "
                    r"\text{ is a period}", font_size=32, color=LAM),
            label(r"Fine and Wilf (1965): \ and this string, \ one character shorter than the bound, \ shows it is "
                  r"tight", font_size=21, color=HEAD),
            label(r"used by every linear-time matcher that skips ahead safely \ (Galil's rule; \ Crochemore and "
                  r"Perrin's two-way algorithm, \ inside glibc's \texttt{memmem})", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Some structure lives inside a single string. <bookmark mark='a'/> A string has period p if every "
            "character equals the one p places later. This one has periods five and eight. <bookmark mark='b'/> "
            "The periods are exactly n minus the borders of chapter three, so the failure function lists them "
            "all. <bookmark mark='c'/> Nathan Fine and Herbert Wilf proved in 1965 that if a string has periods p "
            "and q and is at least p plus q minus their greatest common divisor long, it also has that divisor as "
            "a period. <bookmark mark='d'/> Five and eight have divisor one, so a string of twelve characters "
            "with both periods would be a single repeated letter; ours, of eleven, escapes, which shows the bound is "
            "tight. <bookmark mark='e'/> This lemma is what lets fast matchers skip ahead without missing "
            "anything; Crochemore and Perrin's two-way algorithm, inside the C library's memmem, depends on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells))
            vo.wait_until("a")
            self.play(Create(arcs5), FadeIn(t5), FadeIn(lines[0]))
            self.play(Create(arcs8), FadeIn(t8))
            for mk, ln in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def palindromes(self):
        d = load("period")
        head = label(r"The longest palindrome in thirty novels", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"expanding around each of $2n$ centres is quadratic in the worst case \ (\texttt{aaaa}\dots)",
                  font_size=22, color=WHITE),
            label(r"Manacher (1975): \ inside a known palindrome, \ a centre's radius starts from its \textbf{mirror}'s",
                  font_size=22, color=LAM),
            label(r"the right edge of the known palindrome only moves right: \ $O(n)$", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.45)
        pal = d["palindrome"]
        big_ = label(r"\textit{Able was I ere I saw Elba.}", font_size=44, color=HEAD).next_to(lines, DOWN, buff=0.6)
        src = label(r"Lenehan, \ in \textit{Ulysses} \ (1922)", font_size=22, color=GREY_A).next_to(big_, DOWN,
                                                                                                buff=0.2)
        stats = label(rf"letters only: \ {words(d['scanned'])} of them, \ {d['t_manacher']:.0f} s in Python; \ "
                      rf"{d['pal_len']} letters, \ \texttt{{{pal}}} \ (runs of one letter excluded)", font_size=20,
                      color=WHITE).to_edge(DOWN, buff=0.6)
        if stats.width > 13:
            stats.width = 13
        with self.voiceover(
            "What is the longest palindrome in the novels? <bookmark mark='a'/> Expanding around each possible "
            "centre is quadratic for a text like a run of a's. <bookmark mark='b'/> Glenn Manacher's 1975 algorithm "
            "notices that inside a palindrome already found, each centre mirrors one on the other side, so its "
            "radius can start from the mirror's instead of from zero. <bookmark mark='c'/> The right edge of the "
            "furthest palindrome only ever moves right, which makes the whole scan linear. <bookmark mark='d'/> We "
            "ran it over the letters of all thirty novels, nineteen million of them, ignoring runs of a single "
            "letter. The winner, at nineteen letters, is Lenehan in Ulysses: able was I ere I saw Elba."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(stats))
            self.play(Write(big_), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()

    def lyndon(self):
        d = load("period")
        head = label(r"Lyndon words", font_size=36).to_edge(UP, buff=0.35)
        ex = d["lyndon"]
        rows = VGroup(*[label(rf"\texttt{{{w}}} $=$ " + r" $\cdot$ ".join(rf"\texttt{{{f}}}" for f in fs), font_size=26,
                              color=c) for (w, fs), c in zip(ex.items(), (DATA, LAM, YES))]).arrange(DOWN, buff=0.3)
        lines = VGroup(
            label(r"a \textbf{Lyndon word} is strictly smaller than all of its rotations: \ \texttt{an}, \ \texttt{iss}, "
                  r"\ \texttt{abracad}", font_size=22, color=WHITE),
            label(r"Chen, Fox and Lyndon (1958): \ every string factors \textbf{uniquely} into non-increasing Lyndon words",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.45)
        rows.next_to(lines, DOWN, buff=0.45)
        uses = VGroup(
            label(r"Duval (1983): \ the factorization in linear time, \ with constant extra space", font_size=21,
                  color=GREY_A),
            label(r"the bijective BWT needs no end marker; \ Lyndon arrays underlie recent linear-time suffix sorting and "
                  r"the proof of the runs theorem \ (Bannai et al., 2017)", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "One more piece of structure. <bookmark mark='a'/> A Lyndon word is strictly smaller, in dictionary "
            "order, than every one of its rotations. <bookmark mark='b'/> Kuo-Tsai Chen, Ralph Fox and Roger Lyndon "
            "proved that every string splits in exactly one way into Lyndon words that never increase. <bookmark "
            "mark='c'/> Banana is b, an, an, a. Mississippi is m, iss, iss, ipp, i. <bookmark mark='d'/> Jean-Pierre "
            "Duval found the factorization in linear time with constant extra memory. <bookmark mark='e'/> It sounds "
            "like a curiosity, but it gives a Burrows–Wheeler transform without an end marker, and Lyndon words "
            "were the key to the 2017 proof that a string of length n has fewer than n maximal repetitions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(uses[0]))
            vo.wait_until("e")
            self.play(FadeIn(uses[1]))
        self.wait(0.3)
        self.clear_scene()
