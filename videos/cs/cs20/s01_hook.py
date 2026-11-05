from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (COST, CTRL, DATA, HEAD, LAM, NO, PART, YES, big, grid_table, load, mono, words)


class Hook(VoiceoverScene):
    def construct(self):
        self.kilobytes()
        self.coins()
        self.plan()

    def kilobytes(self):
        d = load("job")
        head = label(r"The top words of thirty novels, \ twice", font_size=36).to_edge(UP, buff=0.35)
        rep = d["report"][:8]
        rows = [[w, words(c), words(c)] for w, c in rep]
        tab = grid_table([r"word", r"Part 17: \ every word kept", r"this part: \ a sketch"], rows,
                         widths=[1.8, 3.8, 3.8], row_h=0.38, font_size=20, mono_cols=(0,),
                         colors=[[DATA, GREY_A, YES]] * len(rows)).next_to(head, DOWN, buff=0.4)
        tab.set_x(0)
        dots = label(r"\dots \ all twenty words, \ all twenty counts, \ identical", font_size=20, color=GREY_A
                     ).next_to(tab, DOWN, buff=0.2)
        mem = VGroup(
            label(rf"{d['v2_bytes'] / 1e6:.1f} MB", font_size=34, color=NO),
            label(r"against", font_size=22, color=GREY_A),
            label(rf"{d['v3_bytes'] / 1000:.1f} KB", font_size=34, color=YES),
        ).arrange(RIGHT, buff=0.5).next_to(dots, DOWN, buff=0.45)
        how = label(r"the second program never stores the words it counts", font_size=24, color=HEAD
                    ).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here are the most common words in the thirty novels, counted twice. <bookmark mark='a'/> On the left, "
            "Part 17's program, which kept every distinct word in a hash table. On the right, this part's "
            "program. The counts agree, all twenty words and all twenty numbers. <bookmark mark='b'/> But the "
            "first program needed almost two megabytes, and the second needs eighteen and a half kilobytes, a "
            "hundred times less. <bookmark mark='c'/> The second program doesn't store the words it counts at "
            "all, apart from a few dozen candidates. It does it by flipping coins, and it is exactly right only "
            "with high probability. By the end of this part we will know how high."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), FadeIn(dots))
            vo.wait_until("b")
            self.play(FadeIn(mem))
            vo.wait_until("c")
            self.play(FadeIn(how))
        self.wait(0.3)
        self.clear_scene()

    def coins(self):
        k = load("karger")
        p = load("primes")
        head = label(r"A coin flip can stand in for cleverness", font_size=36).to_edge(UP, buff=0.4)
        rows = VGroup(*[VGroup(label(a, font_size=26, color=c), label(b, font_size=21, color=GREY_A)).arrange(
            DOWN, buff=0.12) for a, b, c in (
            (r"check a matrix product \ in $n^2$, \ not $n^3$", rf"a wrong answer survives 20 checks with probability "
                                                            r"$2^{-20}$", DATA),
            (r"find a minimum cut \ by contracting random edges", rf"one run: \ {k['success'] * 100:.0f}\% here; \ "
                                                                  r"enough runs: \ almost surely", LAM),
            (r"test a 300-digit number for primality", rf"one round: \ {p['round_1024'] * 1000:.0f} ms; \ a wrong "
                                                        r"answer at most one time in four", YES),
            (r"estimate millions of counts \ in kilobytes", r"the Job, \ ledger row 9", COST))]).arrange(DOWN, buff=0.4)
        rows.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "That is the theme of this part: a coin flip can stand in for cleverness. <bookmark mark='a'/> With "
            "coins we can check a claimed matrix product in n squared time instead of recomputing it. <bookmark "
            "mark='b'/> We can find the weakest link of a network by contracting random edges. <bookmark "
            "mark='c'/> We can test a three-hundred-digit number for primality in milliseconds, which Part 30's "
            "cryptography depends on. <bookmark mark='d'/> And we can count a stream in a fraction of the memory. "
            "Each time, we pay with a small, provable chance of a wrong answer, or of a long wait."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Randomness as a Resource", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"Las Vegas and Monte Carlo; \ shrinking an error by repetition",
            r"checking: \ Freivalds, \ Schwartz--Zippel, \ perfect matchings, \ fingerprints",
            r"Karger's cuts, \ Miller--Rabin's primes, \ random walks for SAT, \ two choices",
            r"Bloom filters and streams: \ reservoirs, \ Count-Min, \ HyperLogLog, \ AMS, \ MinHash",
            r"the Job in 18.6 KB: \ ledger row 9, \ and how often it is right",
            r"the probabilistic method; \ removing the coins; \ where the coins come from",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 20 of Computer Science, Built: Randomness as a Resource. <bookmark mark='a'/> In this part: the "
            "two kinds of randomized algorithm, and how repetition shrinks their errors; checking products and "
            "polynomials with random points; cuts, primes, random walks and the power of two choices; Bloom "
            "filters and sketches of streams, ending in the Job in eighteen kilobytes; the probabilistic method; "
            "and whether the coins can be removed, and where they come from."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
