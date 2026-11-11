from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bar_chart, grid_table,
                                   load, mono, words)


class Chaining(VoiceoverScene):
    def construct(self):
        self.card()
        self.chains()
        self.lengths()
        self.universal()
        self.flooding()

    def card(self):
        card = chapter_card(2, r"Chaining and universal hashing", r"What if an adversary picks the keys?",
                            lit=(1979,), extra=((1979, r"Carter and Wegman: \ universal hashing"),), part=PART)
        with self.voiceover("Chapter two. Chaining, and universal hashing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def chains(self):
        head = label(r"Chaining: \ each slot holds a list", font_size=34).to_edge(UP, buff=0.3)
        m = 7
        buckets = [["sea"], [], ["the", "ship", "whale"], [], ["ahab"], ["white", "boat"], []]
        rows = VGroup()
        for i, b in enumerate(buckets):
            cell = Rectangle(width=0.7, height=0.5, stroke_color=GREY_B, stroke_width=1.4, fill_color=BG,
                             fill_opacity=1)
            idx = mono(str(i), 16, GREY_B).next_to(cell, LEFT, buff=0.15)
            items = VGroup()
            prev = cell
            for w in b:
                box_ = VGroup(RoundedRectangle(width=1.25, height=0.42, corner_radius=0.08, stroke_color=DATA,
                                               stroke_width=1.5, fill_color=BG, fill_opacity=1), mono(w, 18, CODE))
                box_[1].move_to(box_[0])
                box_.next_to(prev, RIGHT, buff=0.45)
                items.add(Arrow(prev.get_right(), box_.get_left(), buff=0.05, stroke_width=2, color=GREY_B,
                                max_tip_length_to_length_ratio=0.25), box_)
                prev = box_
            rows.add(VGroup(idx, cell, items))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=1.5)
        pts = VGroup(
            label(r"load factor \ $\alpha = n / m$", font_size=24, color=HEAD),
            MathTex(r"\mathbb{E}[\text{fixed-slot length}] = \alpha", font_size=32),
            label(r"find: \ hash, \ then walk one chain: \ $O(1 + \alpha)$", font_size=22, color=YES),
            label(r"keep $\alpha$ below a constant \ (grow the table, \ Part 16's doubling)", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "The simplest answer is to keep a chain of keys at each slot. <bookmark mark='a'/> A "
            "collision adds another entry to that slot's list. <bookmark mark='b'/> The load factor is n "
            "over m. With suitable random hashing, a fixed slot has expected chain length alpha. A "
            "successful search for a resident key also accounts for that key itself. <bookmark mark='c'/>"
            " Expected lookup work is order one plus alpha, excluding the cost to hash and compare long "
            "keys. <bookmark mark='d'/> Keeping alpha bounded by geometric resizing gives amortized "
            "expected constant table work. The randomness assumption and the amortized resizing statement"
            " are separate."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=2.5)
            for mk, p in zip("bcd", (pts[:2], pts[2], pts[3])):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def lengths(self):
        d = load("chaining")
        head = label(rf"{words(d['n'])} keys in {words(d['m'])} chains", font_size=34).to_edge(UP, buff=0.3)
        ks = [str(k) for k in range(9)]
        meas = [d["hist"][k] for k in ks]
        pois = [d["poisson"][k] for k in ks]
        ch = bar_chart(meas, ks, [DATA] * 9, height=3.4, bar_w=0.55, gap=0.45, fmt_=lambda v: f"{v:,.0f}",
                       font_size=17).move_to(LEFT * 1.6 + DOWN * 0.4)
        dots = VGroup()
        vmax = max(meas)
        for b, p in zip(ch.bars, pois):
            y = ch.bars[0].get_bottom()[1] + 3.4 * p / vmax
            dots.add(Dot([b.get_center()[0], y, 0], radius=0.07, color=HEAD))
        xl = label(r"chain length", font_size=18, color=GREY_B).next_to(ch, DOWN, buff=0.2)
        side = VGroup(
            label(r"bars: \ measured, \ with a random universal hash", font_size=20, color=DATA),
            label(r"dots: \ Poisson with mean 1, \ $m\,e^{-1}/k!$", font_size=20, color=HEAD),
            label(rf"longest chain: \ {d['max_chain']}", font_size=22, color=GREY_A),
            label(r"longest-chain theorem needs independent-binning assumptions beyond universality", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Here is one seeded experiment with ten thousand and seven keys and as many slots. <bookmark "
            "mark='a'/> Each bar counts the slots with a given chain length. <bookmark mark='b'/> The "
            "dots are a Poisson reference from independent balls into bins. This universal family "
            "guarantees pairwise collision control, not full independence, so agreement with that curve "
            "is an observation rather than its theorem. <bookmark mark='c'/> The displayed maximum is "
            "measured in this table. The familiar logarithm over log-log maximum-load scale needs "
            "stronger random-binning assumptions; universality alone does not establish it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(ch.names), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch.bars], lag_ratio=0.1), FadeIn(ch.vals),
                      FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2:]))
        self.wait(0.3)
        self.clear_scene()

    def universal(self):
        d = load("chaining")
        head = label(r"Universal hashing: \ a random family, \ fixed keys", font_size=33).to_edge(UP, buff=0.3)
        p, m = 7, 3
        pairs = {((a + b) % p, (4 * a + b) % p) for a in range(1, p) for b in range(p)}
        assert pairs == {(r, s) for r in range(p) for s in range(p) if r != s}
        collisions = sum(r % m == s % m for r, s in pairs)
        assert collisions == 10
        cells = VGroup()
        for s in range(p):
            for r in range(p):
                col = BG if r == s else NO if r % m == s % m else DATA
                cells.add(Square(side_length=0.39, stroke_color=GREY_D, stroke_width=0.8,
                                 fill_color=col, fill_opacity=0.9).move_to([-5.7 + 0.43 * r, 1.75 - 0.43 * s, 0]))
        axes = VGroup(*[mono(str(i), 15, GREY_B).move_to([-5.7 + 0.43 * i, 2.18, 0]) for i in range(p)],
                      *[mono(str(i), 15, GREY_B).move_to([-6.12, 1.75 - 0.43 * i, 0]) for i in range(p)])
        axes.add(mono('r', 18, DATA).move_to([-4.4, 2.55, 0]), mono('s', 18, DATA).move_to([-6.45, 0.46, 0]))
        witness = VGroup(
            label(r"$p=7,\ m=3,\ x=1,\ y=4$: \ all 42 ordered pairs $r\ne s$", font_size=18, color=GREY_A),
            label(r"red: \ same residue mod 3; \ diagonal excluded", font_size=18, color=NO),
            MathTex(r"\Pr[\text{collision}]=\frac{10}{42}\le\frac13", font_size=29, color=HEAD),
        ).arrange(DOWN, buff=0.16).move_to([-4.5, -1.9, 0])
        if witness.width > 5.4: witness.scale_to_fit_width(5.4)
        theory = VGroup(
            label(r"fix the keys before choosing the random function", font_size=23, color=GREY_A),
            MathTex(r"\Pr_{h\in H}[h(x)=h(y)]\le\frac1m\quad(x\ne y)", font_size=31, color=YES),
            MathTex(r"h_{a,b}(x)=((ax+b)\bmod p)\bmod m", font_size=31, color=DATA),
            label(r"prime $p$; \ $0\le x<p$; \ uniform $1\le a<p$, \ $0\le b<p$", font_size=20, color=GREY_B),
            MathTex(r"\mathbb E[\text{other colliders}]\le\frac{n-1}{m}", font_size=30, color=YES),
            label(r"successful chain search also counts the resident key", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to([2.85, 0.45, 0])
        if theory.width > 7.4: theory.scale_to_fit_width(7.4)
        note = label(rf"separate finite check: \ 20,000 random functions, \ observed {100*d['pair_rate']:.2f}\% "
                     r"against bound 1\%; \ not a defense against arbitrary adaptive key selection",
                     font_size=19, color=GREY_B).to_edge(DOWN, buff=0.28)
        with self.voiceover("A fixed public hash can expose a large colliding key set. <bookmark mark='a'/> Carter and "
            "Wegman's remedy chooses a random function from a family after the key set is fixed. "
            "<bookmark mark='b'/> Universality bounds the collision probability for every distinct pair "
            "by one over m. For a resident key, the expected number of other colliders is at most n minus"
            " one over m; include the key itself for a successful-chain bound. <bookmark mark='c'/> This "
            "affine family works on distinct residues from zero through p minus one, with prime p, "
            "nonzero a, and uniformly chosen b. <bookmark mark='d'/> Before the final reduction, two "
            "distinct inputs produce a uniformly chosen ordered pair of different residues. Counting "
            "pairs in the same output bucket gives the bound. <bookmark mark='e'/> Two fixed keys across "
            "twenty thousand random functions illustrate that rate; this finite check is not the proof, "
            "and adaptive attackers that learn the chosen function fall outside the fixed-key guarantee.") as vo:
            self.play(FadeIn(head), FadeIn(theory[0]))
            vo.wait_until("a"); self.play(FadeIn(theory[1]))
            vo.wait_until("b"); self.play(FadeIn(theory[4:]))
            vo.wait_until("c"); self.play(FadeIn(theory[2:4]))
            vo.wait_until("d"); self.play(FadeIn(cells), FadeIn(axes), FadeIn(witness))
            vo.wait_until("e"); self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def flooding(self):
        d = load("chaining")
        head = label(r"Hash flooding", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([rf"{words(d['attack_n'])} keys, \ all multiples of $m$", r"longest chain",
                          r"probes to find them all"], [
            [r"fixed hash \ $x \bmod m$", words(d["attack_fixed_max"]), words(d["attack_fixed_cost"])],
            [r"random universal hash", words(d["attack_uni_max"]), words(d["attack_uni_cost"])],
        ], widths=[5.4, 2.6, 3.6], row_h=0.6, font_size=22, mono_cols=(),
            colors=[[NO, NO, NO], [YES, YES, YES]]).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"2011: \ web servers in PHP, \ Java, \ Python and Ruby hashed request parameters with fixed "
                  r"functions", font_size=21, color=GREY_A),
            label(r"one crafted request of colliding names kept a core busy for minutes \ (Klink and W\"alde)",
                  font_size=21, color=NO),
            label(r"the fix: \ a keyed hash, \ SipHash \ (Aumasson and Bernstein, \ 2012), \ Python's default "
                  r"since 3.4", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.55)
        with self.voiceover(
            "This is not a theoretical worry. <bookmark mark='a'/> Take the fixed hash x mod m and feed "
            "it two thousand multiples of m. Every key lands in slot zero: one chain of two thousand, and"
            " finding them all takes two million probes. The same keys under a random universal hash "
            "scatter into chains of one or two. <bookmark mark='b'/> In 2011, Alexander Klink and Julian "
            "Wälde showed that web servers in PHP, Java, Python and Ruby stored request parameters in "
            "hash tables with fixed functions. <bookmark mark='c'/> One request full of colliding names "
            "could keep a server's core busy for minutes. <bookmark mark='d'/> The fix was a hash with a "
            "secret random key. SipHash, designed by Jean-Philippe Aumasson and Daniel Bernstein, has "
            "been Python's string hash since version 3.4."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(Indicate(tab, color=HEAD, scale_factor=1.02), run_time=0.7)
            for mk, p in zip("bcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
