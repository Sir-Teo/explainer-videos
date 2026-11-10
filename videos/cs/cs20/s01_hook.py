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
        how = label('a sketch and 32 candidate words; the whole vocabulary is not retained', font_size=24, color=HEAD
                    ).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            (
            "Here are the most common words in the thirty novels, counted twice. <bookmark mark='a'/> On the left, "
            "Part 17's exact hash-table program. On the right, this part's sketch with thirty-two retained word "
            'candidates. For this corpus and fixed hash seed, all twenty words and counts agree. <bookmark '
            "mark='b'/> The modeled data structures shrink from almost two megabytes to about eighteen and a half "
            "decimal kilobytes. These are program data, not total process memory. <bookmark mark='c'/> The sketch "
            'does not keep the whole vocabulary. Hash collisions can change its answer. By the end we will measure '
            'how often the complete answer survives a sweep of twenty hash seeds.'
        )
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
            ('check a matrix product \\ with $O(n^2)$ arithmetic', r"20 independent rounds: \ false acceptance $\le2^{-20}$", DATA),
            (r"find a minimum cut \ by contracting random edges", rf"observed success: \ {k['success'] * 100:.0f}\% here; \ "
                                                                  r"independent repetition amplifies", LAM),
            ('screen a 300-digit probable-prime candidate', rf"one fixed-base round: \ {p['round_1024'] * 1000:.0f} ms; \ fixed-composite acceptance $\le1/4$", YES),
            (r"estimate millions of counts \ in kilobytes", r"the Job, \ ledger row 9", COST))]).arrange(DOWN, buff=0.4)
        rows.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            (
            "That is the theme of this part: a coin flip can stand in for cleverness. <bookmark mark='a'/> With "
            'exact arithmetic we can check a claimed matrix product with a quadratic number of arithmetic '
            "operations. <bookmark mark='b'/> We can find a network's minimum cut by contracting random edges. "
            "<bookmark mark='c'/> We can rapidly reject composite three-hundred-digit numbers and generate probable "
            "primes, useful for the RSA construction in Part 30. <bookmark mark='d'/> And we can estimate stream "
            'statistics using much less storage. The mathematical guarantees depend on the stated randomness model; '
            'the fixed hash implementations also need empirical checks.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(Indicate(r, color=DATA) if mk == "a" else FadeIn(r, shift=UP * 0.1))
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
            (
            "Part 20 of Computer Science, Built: Randomness as a Resource. <bookmark mark='a'/> In this part: the "
            'two kinds of randomized algorithm, and how repetition shrinks their errors; checking products and '
            'polynomials with random points; cuts, primes, random walks and the power of two choices; Bloom filters '
            'and sketches of streams, ending in the Job in eighteen kilobytes; the probabilistic method; and whether'
            ' the coins can be removed, and where they come from.'
        )
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
