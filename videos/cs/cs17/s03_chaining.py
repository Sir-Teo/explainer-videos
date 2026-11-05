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
            MathTex(r"\mathbb{E}[\text{chain length}] = \alpha", font_size=32),
            label(r"find: \ hash, \ then walk one chain: \ $O(1 + \alpha)$", font_size=22, color=YES),
            label(r"keep $\alpha$ below a constant \ (grow the table, \ Part 16's doubling)", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "The simplest answer to collisions is to let a slot hold more than one key. <bookmark mark='a'/> Each "
            "slot points to a short linked list, a chain, of the keys that hashed there. <bookmark mark='b'/> With "
            "n keys in m slots, the load factor alpha is n over m, and if the hash spreads keys evenly, the "
            "expected length of a chain is alpha. <bookmark mark='c'/> So a find hashes, then walks one chain: "
            "constant time plus alpha. <bookmark mark='d'/> Keep alpha below a constant by doubling the table "
            "when it fills, and the amortized analysis of Part 16 says the cost stays constant per operation."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=2.5)
            for mk, p in zip("abcd", pts):
                if mk != "a":
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
            label(r"the longest is $\Theta(\log n / \log \log n)$ \ (Gonnet, \ 1981)", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Here are ten thousand keys in ten thousand chains, alpha equal to one. <bookmark mark='a'/> The bars "
            "count chains of each length. A third are empty, a third hold one key, and the counts fall off fast. "
            "<bookmark mark='b'/> The dots are the Poisson distribution with mean one, which is what throwing "
            "balls into bins at random predicts, and they sit on the bars. <bookmark mark='c'/> The longest chain "
            "has a handful of keys: it grows like log n over log log n, which in practice means it barely grows."
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
        head = label(r"Universal hashing \ (Carter and Wegman, \ 1979)", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"no single hash function is good for every set of keys: \ an adversary can pick keys that "
                  r"collide", font_size=22, color=NO),
            label(r"so choose the function \textbf{at random}, \ from a family $H$, \ when the table is made",
                  font_size=22, color=GREY_A),
            MathTex(r"H \text{ is universal if } \Pr_{h \in H}[h(x) = h(y)] \le \frac1m \text{ for all } x \ne y",
                    font_size=32, color=YES),
            MathTex(r"h_{a,b}(x) = \bigl((a x + b) \bmod p\bigr) \bmod m, \qquad 1 \le a < p,\ 0 \le b < p",
                    font_size=32, color=DATA),
            label(r"why: \ for $x \ne y$, \ the map $(a, b) \mapsto (ax + b,\ ay + b) \bmod p$ is a bijection, "
                  r"\ so the pair is uniform over distinct pairs", font_size=20, color=GREY_B),
            label(rf"checked: \ two fixed keys, \ 20,000 random $h$, \ $m = 100$: \ collide {100 * d['pair_rate']:.2f}\% "
                  r"of the time, \ bound 1\%", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "A fixed hash function has a weakness: for any one function, there are sets of keys that all collide. "
            "<bookmark mark='a'/> Larry Carter and Mark Wegman's answer, in 1979, was to pick the function at "
            "random, from a family, when the table is built. <bookmark mark='b'/> A family is universal if two "
            "different keys collide with probability at most one over m, over the random choice. Then the expected "
            "chain length is at most alpha for every set of keys, not just random ones. <bookmark mark='c'/> One "
            "such family: multiply by a random a, add a random b, reduce modulo a prime, then modulo m. <bookmark "
            "mark='d'/> The proof is short: for two different keys, the pair of values before the last reduction "
            "is uniformly distributed over distinct pairs, and at most a one-in-m fraction of those pairs agree "
            "modulo m. <bookmark mark='e'/> We checked it with two fixed keys and twenty thousand random "
            "functions: they collided about one percent of the time, as promised."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(steps[0]))
            for mk, s in zip("abcde", steps[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(s))
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
            "This is not a theoretical worry. <bookmark mark='a'/> Take the fixed hash x mod m and feed it two "
            "thousand multiples of m. Every key lands in slot zero: one chain of two thousand, and finding them "
            "all takes two million probes. The same keys under a random universal hash scatter into chains of "
            "one or two. <bookmark mark='b'/> In 2011, Alexander Klink and Julian Wälde showed that web servers "
            "in PHP, Java, Python and Ruby stored request parameters in hash tables with fixed functions. "
            "<bookmark mark='c'/> One request full of colliding names could keep a server's core busy for minutes. "
            "<bookmark mark='d'/> The fix was a hash with a secret random key. SipHash, designed by Jean-Philippe "
            "Aumasson and Daniel Bernstein, has been Python's string hash since version 3.4."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            for mk, p in zip("bcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
