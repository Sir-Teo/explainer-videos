from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, KIND_COLOR, NO, PART, YES, load

N = 16


def network(levels, x0=4.6, dx=0.6, y0=2.15, dy=0.6, color=HEAD):
    """A prefix network drawn as dots: column i is bit position i (bit 0 on the right); row k is level k.  Each
    combine is a dot at (i, k) fed by the value at (j, k - 1).  Returns (wires, combines per level, xs, ys)."""
    X = lambda i: x0 - dx * i  # noqa: E731
    L = len(levels)
    dy = min(dy, 4.4 / L)
    Y = lambda k: y0 - dy * k  # noqa: E731
    rails = VGroup(*[Line([X(i), Y(0) + 0.3, 0], [X(i), Y(L) - 0.15, 0], color=GREY_D, stroke_width=2) for i in range(N)])
    tops = VGroup(*[MathTex(rf"{i}", font_size=18, color=GREY_B).move_to([X(i), Y(0) + 0.5, 0]) for i in range(N)])
    per_level = []
    for k, level in enumerate(levels, start=1):
        g = VGroup()
        for i, j in level:
            g.add(Line([X(j), Y(k - 1), 0], [X(i), Y(k), 0], color=color, stroke_width=2.2),
                  Dot([X(i), Y(k), 0], radius=0.075, color=color))
        per_level.append(g)
    outs = VGroup(*[MathTex(rf"c_{{{i + 1}}}", font_size=18, color=YES).move_to([X(i), Y(L) - 0.4, 0]) for i in range(N)])
    return rails, tops, per_level, outs


class Prefix(VoiceoverScene):
    def construct(self):
        self.card()
        self.gpk()
        self.lookahead()
        self.operator()
        self.networks()
        self.compare()

    def card(self):
        card = chapter_card(4, r"Carries in parallel", r"Can every carry be known at once?", lit=(1960, 1973),
                            part=PART)
        with self.voiceover("Chapter four. Carries in parallel."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def gpk(self):
        head = label(r"Each position generates, \ propagates \ or kills", font_size=36).to_edge(UP, buff=0.35)
        a, b = "10110110", "01100011"
        tags = []
        for x, y in zip(a, b):
            tags.append("G" if x == y == "1" else ("K" if x == y == "0" else "P"))
        col = {"G": YES, "P": HEAD, "K": NO}
        xs = [-3.5 + 0.8 * i for i in range(8)]
        ra = VGroup(*[MathTex(ch, font_size=40, color=DATA).move_to([xs[i], 1.6, 0]) for i, ch in enumerate(a)])
        rb = VGroup(*[MathTex(ch, font_size=40, color=DATA).move_to([xs[i], 0.9, 0]) for i, ch in enumerate(b)])
        rt = VGroup(*[MathTex(t, font_size=40, color=col[t]).move_to([xs[i], -0.1, 0]) for i, t in enumerate(tags)])
        names = VGroup(MathTex("a", font_size=34, color=GREY_B).move_to([xs[0] - 1.0, 1.6, 0]),
                       MathTex("b", font_size=34, color=GREY_B).move_to([xs[0] - 1.0, 0.9, 0]))
        defs = VGroup(
            MathTex(r"g_i = a_i\, b_i", r"\quad \text{generate: a carry leaves, whatever comes in}", font_size=30),
            MathTex(r"p_i = a_i \oplus b_i", r"\quad \text{propagate: the carry passes through}", font_size=30),
            MathTex(r"\text{neither}", r"\quad \text{kill: no carry leaves}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(DOWN * 1.6)
        for m, c in zip(defs, (YES, HEAD, NO)):
            m[0].set_color(c)
            m[1].set_color(GREY_A)
        rec = MathTex(r"c_{i+1} = g_i + p_i\, c_i, \qquad s_i = p_i \oplus c_i", font_size=38, color=CODE).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "To break the chain, look at what one column does with a carry, before knowing what the carry is. "
            "<bookmark mark='a'/> If both of its bits are one, it sends a carry out no matter what comes in: it "
            "generates. If exactly one bit is one, a carry that comes in goes straight out: it propagates. If both are "
            "zero, no carry leaves: it kills. <bookmark mark='b'/> These three cases depend only on the column's own "
            "two bits, so every column knows its letter after one gate delay, all at once. "
            "<bookmark mark='c'/> In symbols: g is a and b, p is a exclusive-or b, the carry out is g, or p and the "
            "carry in, and the sum bit is p exclusive-or the carry in. The whole problem of fast addition is now "
            "computing every carry from these letters quickly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ra), FadeIn(rb), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(defs[i]) for i in range(3)], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in rt], lag_ratio=0.08))
            vo.wait_until("c")
            self.play(FadeIn(rec))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lookahead(self):
        head = label(r"Unroll the recurrence: \ carry lookahead", font_size=36).to_edge(UP, buff=0.35)
        lines = VGroup(
            MathTex(r"c_1 = g_0 + p_0 c_0", font_size=34),
            MathTex(r"c_2 = g_1 + p_1 g_0 + p_1 p_0 c_0", font_size=34),
            MathTex(r"c_3 = g_2 + p_2 g_1 + p_2 p_1 g_0 + p_2 p_1 p_0 c_0", font_size=34),
            MathTex(r"c_4 = g_3 + p_3 g_2 + p_3 p_2 g_1 + p_3 p_2 p_1 g_0 + p_3 p_2 p_1 p_0 c_0", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.7)
        for l in lines:
            l.set_color(CODE)
        read = label(r"``a carry reaches position 4 if some position generated one, \\ and every position after it "
                     r"propagated''", font_size=26, color=GREY_A).next_to(lines, DOWN, buff=0.45)
        cost = label(r"two levels of gates for every carry, \ but the terms grow like $n^2$, \ and the gates need "
                     r"$n$ inputs", font_size=26, color=NO).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "One idea is to unroll the recurrence. <bookmark mark='a'/> The carry into position one is g zero, or p "
            "zero and the carry in. Substitute that into the next one, and the next. <bookmark mark='b'/> The carry "
            "into position four reads like a sentence: a carry arrives if some position generated one and every "
            "position after it propagated it. <bookmark mark='c'/> In principle every carry is now two levels of gates, "
            "an and of p's and a g, then an or. In practice the formula for carry n has n terms with up to n inputs "
            "each, and gates with dozens of inputs are slow. Real carry-lookahead adders use this for groups of four "
            "bits, then treat each group as one big position and do it again. That repetition is the real idea, and "
            "it has a beautiful algebra."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            self.play(FadeIn(lines[1]), FadeIn(lines[2]))
            vo.wait_until("b")
            self.play(FadeIn(lines[3]), FadeIn(read))
            vo.wait_until("c")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def operator(self):
        head = label(r"A block is a function of its carry-in", font_size=36).to_edge(UP, buff=0.35)
        fns = VGroup()
        for name, mapping, col in (("K", (0, 0), NO), ("P", (0, 1), HEAD), ("G", (1, 1), YES)):
            pts_in = [np.array([0, 0.35 - 0.7 * v, 0]) for v in (0, 1)]
            g = VGroup(MathTex(name, font_size=40, color=col))
            box = VGroup(*[MathTex(str(v), font_size=28, color=GREY_A).move_to(np.array([-0.6, 0.35 - 0.7 * v, 0]))
                           for v in (0, 1)],
                         *[MathTex(str(v), font_size=28, color=GREY_A).move_to(np.array([0.6, 0.35 - 0.7 * v, 0]))
                           for v in (0, 1)])
            arrows = VGroup(*[Arrow(np.array([-0.45, 0.35 - 0.7 * v, 0]), np.array([0.45, 0.35 - 0.7 * m, 0]), buff=0.05,
                                    stroke_width=3, color=col, max_tip_length_to_length_ratio=0.25)
                              for v, m in zip((0, 1), mapping)])
            g.add(VGroup(box, arrows))
            g.arrange(DOWN, buff=0.25)
            fns.add(g)
        fns.arrange(RIGHT, buff=1.2).move_to(LEFT * 3.2 + UP * 1.0)
        cap = label(r"carry-in $\mapsto$ carry-out: \ $c \mapsto g + p\,c$", font_size=26, color=GREY_A).next_to(
            fns, DOWN, buff=0.35)
        op = MathTex(r"(g, p) \circ (g', p') = (g + p\,g',\ \ p\,p')", font_size=40, color=CODE).move_to(
            RIGHT * 3.2 + UP * 1.6)
        opl = label(r"the high block after the low one: \ function composition", font_size=24, color=GREY_A).next_to(
            op, DOWN, buff=0.25)
        assoc = MathTex(r"\big((g,p) \circ (g',p')\big) \circ (g'',p'') = (g,p) \circ \big((g',p') \circ (g'',p'')\big)",
                        font_size=30, color=YES).move_to(DOWN * 1.2)
        both = MathTex(r"= (g + p\,g' + p\,p'\,g'',\ \ p\,p'\,p'')", font_size=30, color=YES).next_to(assoc, DOWN,
                                                                                                    buff=0.25)
        so = label(r"associative: \ group the positions any way you like", font_size=28, color=HEAD).to_edge(DOWN,
                                                                                                     buff=0.45)
        with self.voiceover(
            "Here is the algebra. <bookmark mark='a'/> Think of a column, or any block of columns, as a function from "
            "the carry that comes in to the carry that goes out. There are only three such functions: kill sends "
            "everything to zero, propagate is the identity, and generate sends everything to one. Every block is one of "
            "them, and is described by its pair, g and p. <bookmark mark='b'/> Putting a high block after a low one is "
            "composing their functions, and the pair of the combination is g plus p g prime, and p p prime. "
            "<bookmark mark='c'/> Composition of functions is always associative, so this operator is too: combine "
            "three blocks either way and you get the same pair. <bookmark mark='d'/> That one fact is the key. It "
            "means the carries are prefix combinations, like running totals, and running totals of an associative "
            "operation can be computed by a tree instead of a chain, in logarithmic depth."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in fns], lag_ratio=0.3), FadeIn(cap), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(op), FadeIn(opl))
            vo.wait_until("c")
            self.play(FadeIn(assoc), FadeIn(both))
            vo.wait_until("d")
            self.play(FadeIn(so))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def show_network(self, kind, title_tex, narration, marks):
        d = load("prefix")[kind]
        head = label(title_tex, font_size=34).to_edge(UP, buff=0.3)
        rails, tops, per_level, outs = network(d["levels"], color=KIND_COLOR[kind])
        stats = label(rf"{d['nodes']} combines, \ depth {d['depth']}, \ fan-out {d['fanout']}", font_size=26,
                      color=KIND_COLOR[kind]).to_edge(DOWN, buff=0.25)
        with self.voiceover(narration) as vo:
            self.play(FadeIn(head), FadeIn(rails), FadeIn(tops))
            vo.wait_until(marks[0])
            for g in per_level:
                self.play(LaggedStart(*[Create(m) for m in g], lag_ratio=0.02), run_time=0.6)
            self.play(FadeIn(outs))
            vo.wait_until(marks[1])
            self.play(FadeIn(stats))
        self.wait(0.3)
        self.clear_scene()

    def networks(self):
        self.show_network(
            "ripple", r"The ripple adder, \ as a prefix network: \ a chain",
            "Draw the sixteen positions as columns, bit zero on the right, and draw a dot wherever two blocks are "
            "combined. <bookmark mark='a'/> The ripple adder is a chain: position one absorbs position zero, then two "
            "absorbs that, and so on, one combine per level, fifteen levels deep. <bookmark mark='b'/> Fifteen "
            "combines, the fewest possible, and the slowest.", ("a", "b"))
        self.show_network(
            "kogge-stone", r"Kogge--Stone (1973): \ double the reach every level",
            "In 1973 Peter Kogge and Harold Stone published the fastest arrangement. <bookmark mark='a'/> At the first "
            "level every position combines with its neighbour one to the right; at the second, with the position two "
            "to the right; then four, then eight. After four levels every position holds the combination of everything "
            "below it: all sixteen carries, in log two of n levels. <bookmark mark='b'/> The price is size, forty-nine "
            "combines, and wiring: the long diagonal wires are what make real Kogge-Stone adders hard to lay out.",
            ("a", "b"))
        self.show_network(
            "brent-kung", r"Brent--Kung (1982): \ a tree up, \ and a tree down",
            "Richard Brent and H. T. Kung found the frugal arrangement in 1982. <bookmark mark='a'/> Build a binary "
            "tree upwards, combining pairs, then pairs of pairs, until the top position holds the whole sum; then send "
            "the partial results back down the tree to fill in the positions between. <bookmark mark='b'/> Twenty-six "
            "combines, fewer than twice the ripple's, in seven levels: about two log n. The same up-and-down sweep is "
            "the parallel scan of Part 10, which sums, sorts and allocates on graphics processors.", ("a", "b"))
        self.show_network(
            "sklansky", r"Sklansky (1960): \ divide and conquer",
            "The oldest is Jack Sklansky's, from 1960, and it is divide and conquer. <bookmark mark='a'/> Solve the low "
            "half and the high half separately, then let the top result of the low half fan out to every position in "
            "the high half, and do the same inside each half. Four levels, as fast as Kogge-Stone, with thirty-two "
            "combines. <bookmark mark='b'/> But one value must drive eight gates at once, and Part 3 showed that "
            "fan-out costs time. Every real adder is a compromise between these three.", ("a", "b"))

    # ------------------------------------------------------------------
    def compare(self):
        d = load("prefix")
        head = label(r"Three ways to compute every carry", font_size=36).to_edge(UP, buff=0.4)
        rows = VGroup()
        hdr = VGroup(*[label(t, font_size=24, color=GREY_B) for t in (r"network", r"combines", r"depth", r"fan-out",
                                                                      r"wiring")])
        rows.add(hdr)
        info = {"ripple": r"short", "kogge-stone": r"long, \ many", "brent-kung": r"few", "sklansky": r"long"}
        for kind in ("ripple", "brent-kung", "sklansky", "kogge-stone"):
            r = d[kind]
            rows.add(VGroup(label(kind.replace("-", "--").title().replace("Kogge--Stone", r"Kogge--Stone"),
                                  font_size=26, color=KIND_COLOR[kind]),
                            MathTex(str(r["nodes"]), font_size=30, color=GREY_A),
                            MathTex(str(r["depth"]), font_size=30, color=GREY_A),
                            MathTex(str(r["fanout"]), font_size=30, color=GREY_A),
                            label(info[kind], font_size=24, color=GREY_A)))
        for i, r in enumerate(rows):
            for j, m in enumerate(r):
                m.move_to([-4.6 + [0, 2.8, 4.4, 6.0, 7.8][j], 1.6 - 0.6 * i, 0])
        n16 = note(r"for $n = 16$; \ in general: \ ripple $n - 1$ and $n - 1$; \ Kogge--Stone about $n \log_2 n$ and "
                   r"$\log_2 n$; \ Brent--Kung $2n$ and $2 \log_2 n$", font_size=22).next_to(rows, DOWN, buff=0.5)
        bound = label(r"no prefix network is both as small as ripple and as shallow as Kogge--Stone: \\ size $+$ depth "
                      r"$\ge 2n - 2$ \ (Snir, 1986)", font_size=26, color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Side by side, for sixteen positions. <bookmark mark='a'/> The ripple chain is smallest and deepest. "
            "Kogge-Stone is shallowest and biggest, with fan-out two but a forest of long wires. Brent-Kung is nearly "
            "as small as the ripple at twice Kogge-Stone's depth. Sklansky is shallow and small, but with a fan-out of "
            "nine. <bookmark mark='b'/> And there is a theorem saying you cannot have everything: Marc Snir proved in "
            "1986 that for any prefix network, the size plus the depth is at least two n minus two. Designers of real "
            "chips use hybrids, Han-Carlson, Ladner-Fischer and others, tuned to the wires and gates of each process."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[1:]], lag_ratio=0.3), FadeIn(n16),
                      run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(bound))
        self.wait(0.3)
        self.clear_scene()
