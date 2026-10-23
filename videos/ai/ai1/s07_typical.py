from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import PART, load

TYP = C.BITS  # the typical set
ALL = "#3A4558"  # sequences outside it


def coin_classes(n: int, q: float):
    """Per number of spaces k in n tosses: log2 of how many sequences, and log2 of each one's probability."""
    k = np.arange(n + 1)
    logC = np.array([(math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1)) / math.log(2) for j in k])
    return k, logC, k * math.log2(q) + (n - k) * math.log2(1 - q)


def pow2(e: float) -> str:
    """2^e as TeX: a plain percentage while it is readable, a power of two after."""
    v = 2.0 ** e
    return rf"{100 * v:.1f}\%" if v >= 0.001 else rf"2^{{{e:.0f}}}"


class Typical(VoiceoverScene):
    def construct(self):
        self.card()
        self.concentrate()
        self.definition()
        self.shrink()
        self.theorem()
        self.meaning()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Typical sequences and the source coding theorem",
                            r"Why do long messages compress so well?", lit=(1948,), part=PART)
        with self.voiceover("Chapter six. Why long messages compress so well."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def concentrate(self):
        t = load("typical")
        H = float(t["H"])
        ns = [int(n) for n in t["ns"]]
        edges = np.asarray(t["edges"])
        width = 2 * (edges[1] - edges[0])
        hist = {n: np.asarray(t["hist"][str(n)], float) for n in ns}
        hist = {n: (h[0::2] + h[1::2]) / h.sum() for n, h in hist.items()}  # 0.1-bit bins, as shares
        centers = (edges[:-1:2] + width / 2)
        a = axes([0, 11], [0, 1], x_length=10.0, y_length=3.6, xlabel=r"surprise per letter: \ "
                 r"$-\frac{1}{n} \log_2 p(x_1 \dots x_n)$, \ bits", ylabel=r"share of $4{,}000$ sampled texts",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.5, 1], center=[0, -0.75, 0], font_size=20)
        ax = a.ax

        def bars(n):
            g = VGroup()
            for c, h in zip(centers, hist[n]):
                if h <= 0 or c > 11:
                    continue
                b0, b1 = ax.c2p(c - width / 2, 0), ax.c2p(c + width / 2, h)
                g.add(Rectangle(width=b1[0] - b0[0], height=max(b1[1] - b0[1], 0.01), stroke_width=0,
                                fill_color=C.SURPRISE, fill_opacity=0.85).move_to((b0 + b1) / 2))
            return g

        hl = DashedLine(ax.c2p(H, 0), ax.c2p(H, 1), color=C.ENTROPY, stroke_width=2.5)
        hlab = label(rf"$H = {H:.2f}$", font_size=26, color=C.ENTROPY).next_to(ax.c2p(H, 1), UP, buff=0.1)
        cur = bars(ns[0])
        nlab = MathTex(rf"n = {ns[0]}", font_size=38, color=WHITE).to_corner(UR, buff=0.5).shift(DOWN * 0.6)

        def inside_lab(n):
            return label(rf"within $0.1$ bits of $H$: \ ${100 * t['inside'][str(n)]:.0f}\%$", font_size=26,
                         color=C.BITS).next_to(nlab, DOWN, buff=0.2).align_to(nlab, RIGHT)

        ins = inside_lab(ns[0])
        head = label(r"Long texts are all about equally surprising", font_size=36).to_edge(UP, buff=0.3)
        sub = label(r"letters drawn independently, \ at the books' frequencies", font_size=24, color=GREY_B)
        sub.next_to(head, DOWN, buff=0.15)
        tag = computed_tag()
        sd = {n: float(t["sd"][str(n)]) for n in ns}
        with self.voiceover(
            "In chapter four we saw that whole bits waste up to one per symbol, and that coding long blocks fixes "
            "it. Here is why. <bookmark mark='a'/> Make up a text by drawing letters one at a time, independently, "
            "with the books' frequencies: a crude model of English, but one we can reason about exactly. Measure its "
            "surprise per letter. <bookmark mark='b'/> For a single letter, it's all over the place, from a couple of "
            "bits to almost eleven. <bookmark mark='c'/> Ten letters: the spread narrows. <bookmark mark='d'/> A "
            "hundred, a thousand, ten thousand: the surprise per letter piles up at one value, "
            f"{H:.2f} bits, the entropy. Its spread shrinks from {sd[ns[0]]:.1f} bits to {sd[ns[-1]]:.2f}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(cur), FadeIn(nlab), FadeIn(ins), Create(hl), FadeIn(hlab))
            vo.wait_until("c")
            for j, n in enumerate(ns[1:]):
                if j == 1:
                    vo.wait_until("d")
                new = bars(n)
                self.play(ReplacementTransform(cur, new),
                          Transform(nlab, MathTex(rf"n = {n:,}".replace(",", "{,}"), font_size=38).move_to(nlab, RIGHT)),
                          Transform(ins, inside_lab(n)), run_time=1.3)
                cur = new
        th = theorem_card(r"asymptotic equipartition", r"$-\frac{1}{n} \log_2 p(X_1 \dots X_n) \to H$ \ with "
                          r"probability $1$, \ for independent symbols (the law of large numbers) and for any stationary "
                          r"ergodic source", who=r"Shannon (1948); \ McMillan (1953); \ Breiman (1957)", width=8.4,
                          color=C.ENTROPY).to_corner(UL, buff=0.35).shift(DOWN * 0.9)
        with self.voiceover(
            "It's the law of large numbers. The surprise of a text is a sum of the surprises of its letters, and an "
            "average of many independent surprises settles at their mean, which is the entropy. "
            "<bookmark mark='a'/> Shannon proved it in 1948, and McMillan and Breiman extended it to sources with "
            "memory, like real text. It has a mouthful of a name: the asymptotic equipartition property."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(sub), FadeIn(th, shift=DOWN * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def definition(self):
        df = definition_card(r"the typical set $A_\varepsilon^{(n)}$",
                             r"the sequences $x_1 \dots x_n$ whose surprise per symbol is within $\varepsilon$ of $H$: "
                             r"\ $\big|{-\frac1n} \log_2 p(x_1 \dots x_n) - H\big| \le \varepsilon$", width=11.0,
                             color=TYP).to_edge(UP, buff=0.35)
        rows = [
            cmath(r"2^{-n(H+\varepsilon)}", r"\le", r"p(x)", r"\le", r"2^{-n(H-\varepsilon)}", font_size=38),
            cmath(r"P(A)", r"\to", r"1", font_size=38),
            cmath(r"1", r"\ge", r"P(A) \ge |A|\, 2^{-n(H+\varepsilon)}", font_size=38),
            cmath(r"|A|", r"\le", r"2^{n(H+\varepsilon)}", font_size=38),
            cmath(r"|A|", r"\ge", r"(1-\delta)\, 2^{n(H-\varepsilon)}", font_size=38),
        ]
        whys = [why(r"each member: \ the definition"), why(r"the AEP"), why(r"each of the $|A|$ members has at least "
                r"$2^{-n(H+\varepsilon)}$"), why(r"so there are at most this many"),
                why(r"and $P(A) \ge 1 - \delta$ forces at least this many")]
        step = ladder(self, rows, whys, keep=4, top=1.0, x=-2.4, buff=0.38, edge=6.9)
        with self.voiceover(
            "Call a sequence typical if its surprise per symbol is within a small epsilon of the entropy. "
            "<bookmark mark='a'/> Then each typical sequence has probability close to two to the minus n H. "
            "<bookmark mark='b'/> By the equipartition property, the typical set holds nearly all the probability. "
            "<bookmark mark='c'/> Count them: all their probabilities together can't exceed one, <bookmark mark='d'/> "
            "so there are at most two to the n H plus epsilon of them; <bookmark mark='e'/> and since they hold "
            "nearly everything, at least about two to the n H. Nearly every sequence you will ever see is one of "
            "about two to the n H, all about equally likely."
        ) as vo:
            self.play(FadeIn(df, shift=DOWN * 0.2))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shrink(self):
        t = load("typical")
        q, h, eps = float(t["q"]), float(t["h"]), float(t["eps"])
        rows = {int(r["n"]): r for r in t["rows"]}
        show = [n for n in (4, 8, 16, 33, 68, 138, 280, 568, 1000) if n in rows]
        W, xL = 11.6, -5.4
        y_top, y_bot, bh = 1.15, -1.75, 0.5

        def picture(n):
            k, logC, logp = coin_classes(n, q)
            share = np.exp2(logC - n)  # each class's share of all 2^n sequences
            mass = np.exp2(logC + logp)  # and of the probability
            typ = np.abs(-logp / n - h) <= eps
            g = VGroup()
            xa = xb = xL
            for j in range(n + 1):
                wa, wb = W * share[j], W * mass[j]
                if wa < 1e-4 and wb < 1e-4:
                    xa, xb = xa + wa, xb + wb
                    continue
                col = TYP if typ[j] else (ALL if j % 2 == 0 else "#4A5670")
                ra = Rectangle(width=max(wa, 1e-3), height=bh, stroke_width=0, fill_color=col,
                               fill_opacity=1).move_to([xa + wa / 2, y_top, 0])
                rb = Rectangle(width=max(wb, 1e-3), height=bh, stroke_width=0, fill_color=col,
                               fill_opacity=1).move_to([xb + wb / 2, y_bot, 0])
                band = Polygon([xa, y_top - bh / 2, 0], [xa + wa, y_top - bh / 2, 0], [xb + wb, y_bot + bh / 2, 0],
                               [xb, y_bot + bh / 2, 0], stroke_width=0, fill_color=col,
                               fill_opacity=0.35 if typ[j] else 0.08)
                g.add(band, ra, rb)
                xa, xb = xa + wa, xb + wb
            top_seq = Line([xL, y_bot - bh / 2 - 0.12, 0], [xL, y_bot + bh / 2 + 0.12, 0], color=WHITE, stroke_width=3)
            g.add(top_seq)
            return g

        frames = VGroup(Rectangle(width=W, height=bh, stroke_color=GREY_B, stroke_width=1.5).move_to([xL + W / 2, y_top, 0]),
                        Rectangle(width=W, height=bh, stroke_color=GREY_B, stroke_width=1.5).move_to([xL + W / 2, y_bot, 0]))
        lt = label(r"all $2^n$ sequences, \ each the same width", font_size=24, color=GREY_A)
        lt.next_to(frames[0], UP, buff=0.12).align_to(frames[0], LEFT)
        lb = label(r"the same sequences, \ each as wide as its probability", font_size=24, color=GREY_A)
        lb.next_to(frames[1], DOWN, buff=0.12).align_to(frames[1], LEFT)
        head = label(rf"A source that writes a space with probability ${q:.3f}$: \ $n$ symbols", font_size=30)
        head.to_edge(UP, buff=0.3)
        key = VGroup(Square(0.22, stroke_width=0, fill_color=TYP, fill_opacity=1),
                     label(rf"typical: \ within ${eps}$ bits of $H = {h:.3f}$", font_size=22, color=TYP)).arrange(RIGHT, buff=0.15)
        key.next_to(head, DOWN, buff=0.18)
        top_l = label(r"the most likely sequence: \ no spaces at all", font_size=20, color=WHITE)
        top_l.next_to([xL, y_bot - bh / 2, 0], DOWN, buff=0.55).align_to(frames[1], LEFT)

        def readout(n):
            r = rows[n]
            return VGroup(
                MathTex(rf"n = {n}", font_size=34),
                label(rf"share of sequences: \ ${pow2(r['log2_frac'])}$", font_size=24, color=TYP),
                label(rf"share of probability: \ ${100 * r['P']:.1f}\%$" if r["P"] < 0.9995 else
                      rf"share of probability: \ $1 - 10^{{{math.log10(1 - r['P']):.0f}}}$", font_size=24, color=TYP),
                label(rf"most likely sequence: \ ${pow2(math.log2(r['p_top']))}$", font_size=22, color=GREY_A),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.2, -0.3, 0])

        pic = picture(show[0])
        ro = readout(show[0])
        r0, r1 = rows[show[0]], rows[show[-1]]
        with self.voiceover(
            "Here is the typical set, drawn. Take a simpler source: a coin that writes a space with the books' "
            f"frequency of spaces, {q:.3f}. <bookmark mark='a'/> Lay out all two to the n sequences in a row, each "
            "the same width, from the most likely, with no spaces at all, to the least. <bookmark mark='b'/> Below, "
            "the same sequences, each as wide as its probability. The typical ones are in gold. "
            f"<bookmark mark='c'/> With {show[0]} symbols, they are {100 * 2 ** r0['log2_frac']:.0f} percent of the "
            f"sequences, holding {100 * r0['P']:.0f} percent of the probability. <bookmark mark='d'/> Now make the "
            "sequences longer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(frames[0]), FadeIn(lt))
            vo.wait_until("b")
            self.play(Create(frames[1]), FadeIn(lb), FadeIn(pic), FadeIn(top_l))
            vo.wait_until("c")
            self.play(FadeIn(ro))
            vo.wait_until("d")
        with self.voiceover(
            "In the top row, the gold shrinks to a sliver, and then to nothing you can see. In the bottom row it "
            f"spreads until it fills almost everything. <bookmark mark='a'/> By {show[-1]} symbols, the typical "
            f"sequences are two to the minus {-r1['log2_frac']:.0f} of all sequences, and they carry all but "
            f"{100 * (1 - r1['P']):.6f} percent of the probability. <bookmark mark='b'/> And the single most likely "
            "sequence, all non-spaces, isn't typical at all: you will essentially never see it."
        ) as vo:
            for n in show[1:]:
                new_pic, new_ro = picture(n), readout(n)
                self.play(ReplacementTransform(pic, new_pic), ReplacementTransform(ro, new_ro), run_time=1.2)
                pic, ro = new_pic, new_ro
            vo.wait_until("a")
            self.play(Indicate(ro[1], color=TYP), Indicate(ro[2], color=TYP))
            vo.wait_until("b")
            self.play(Indicate(top_l, color=WHITE), Indicate(ro[3], color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        t = load("typical")
        h = float(t["h"])
        rows = t["rows"]
        ns = np.array([r["n"] for r in rows], float)
        rate = np.array([r["shannon_rate"] for r in rows])
        th = theorem_card(r"Shannon's source coding theorem", r"a source of entropy $H$ bits per symbol can be coded "
                          r"in $H + \varepsilon$ bits per symbol, for any $\varepsilon > 0$, by coding long enough "
                          r"blocks; \ and no code does better than $H$ on average", who=r"C.~E.~Shannon (1948)",
                          width=9.6, color=C.ENTROPY).to_edge(UP, buff=0.3)
        code = VGroup(
            label(r"typical? \ send $0$, then its index: \ $\lceil n(H + \varepsilon) \rceil$ bits", font_size=24,
                  color=TYP),
            label(r"not typical? \ send $1$, then the sequence as it is: \ $n \log_2 K$ bits", font_size=24,
                  color=GREY_A),
            label(r"average: \ $\le n(H + \varepsilon) + 2 + P(\text{not typical})\, n \log_2 K$", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_corner(DL, buff=0.4).shift(UP * 0.35)
        a = axes([0.5, 3.0], [h - 0.02, 0.9], x_length=5.0, y_length=2.6, xlabel=r"block length $n$",
                 ylabel=r"bits per symbol", xticks=[1, 2, 3], yticks=[0.7, 0.8, 0.9],
                 xfmt=lambda v: f"10^{{{int(v)}}}", center=[3.7, -1.9, 0], font_size=18)
        ax = a.ax
        cur = curve(ax, np.log10(ns), np.minimum(rate, 0.9), C.BITS, 3.5)
        hline = DashedLine(ax.c2p(0.5, h), ax.c2p(3.0, h), color=C.ENTROPY, stroke_width=2.5)
        hl = label(rf"$H = {h:.3f}$", font_size=22, color=C.ENTROPY).next_to(ax.c2p(3.0, h), UP, buff=0.08)
        hl.align_to(hline, RIGHT)
        cap = label(r"Shannon's code on whole blocks of $n$ symbols", font_size=20, color=C.BITS)
        cap.next_to(a, UP, buff=0.05)
        tag = note(r"computed: \ exact, \ for the coin above").next_to(a, DOWN, buff=0.1)
        with self.voiceover(
            "That gives the source coding theorem. <bookmark mark='a'/> To compress n symbols: if the sequence is "
            "typical, send a zero, then its number in a list of the typical set: about n H bits. If it isn't, send a "
            "one and the sequence as it is. That rarely happens, so on average you pay about H bits per symbol. "
            "<bookmark mark='b'/> And no code does better: any list short enough to save more would miss most of "
            "the typical sequences, and with them almost all the probability. <bookmark mark='c'/> Even the simple "
            "rounded code of the last chapter, used on whole blocks, closes in on the entropy: from "
            f"{rate[0]:.3f} bits per symbol with blocks of {int(ns[0])}, to {rate[-1]:.4f} with blocks of "
            f"{int(ns[-1])}, against an entropy of {h:.4f}."
        ) as vo:
            self.play(FadeIn(th, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in code], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(th.body, color=C.ENTROPY, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(a), FadeIn(cap), FadeIn(tag), Create(hline), FadeIn(hl))
            self.play(Create(cur), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        t = load("typical")
        gap = float(t["gap27"])
        H = float(t["H"])
        page = 2000
        head = label(r"Real text is a vanishing corner of all possible strings", font_size=34).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(rf"strings of $n$ letters: \ $27^n = 2^{{{math.log2(27):.2f} n}}$", font_size=30),
            label(rf"typical under the letter frequencies: \ $2^{{{H:.2f} n}}$, \ a share of $2^{{-{gap:.2f} n}}$",
                  font_size=30, color=TYP),
            label(rf"a page of ${page:,}$ letters: \ a share of $2^{{-{gap * page:,.0f}}}$".replace(",", "{,}"),
                  font_size=30, color=TYP),
            label(r"at about $1$ bit per letter (Shannon's estimate): \ $2^{n}$ of them", font_size=30, color=C.HUMAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.55)
        # nested squares: all strings, the letter-typical ones, the English-typical ones (areas schematic)
        sq = VGroup(Square(2.6, stroke_color=GREY_B, stroke_width=2, fill_color=ALL, fill_opacity=0.4),
                    Square(1.1, stroke_width=0, fill_color=TYP, fill_opacity=0.6),
                    Square(0.32, stroke_width=0, fill_color=C.HUMAN, fill_opacity=0.9))
        sq[1].move_to(sq[0].get_corner(DL) + np.array([0.75, 0.75, 0]))
        sq[2].move_to(sq[1].get_center() + np.array([-0.2, -0.15, 0]))
        sq.to_corner(DR, buff=0.5)
        sch = note(r"areas not to scale").next_to(sq, UP, buff=0.1)
        take = label(r"a language model's job: \ find that corner; \ to write, \ draw from it", font_size=30,
                     color=C.BITS).to_edge(DOWN, buff=0.5).shift(LEFT * 1.6)
        with self.voiceover(
            "Now think about English. There are twenty-seven to the n strings of n letters. "
            f"<bookmark mark='a'/> Even under the letter frequencies alone, the typical ones are a fraction two to "
            f"the minus {gap:.2f} n of them: for a page of {page:,} letters, two to the minus {gap * page:,.0f}. "
            "<bookmark mark='b'/> At Shannon's one bit per letter, real text is a far smaller corner still. "
            "<bookmark mark='c'/> A language model's whole job is to find that corner, and to write, it draws from "
            "it. How it should draw comes back in Part 5."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(sq[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]), FadeIn(sq[1]), FadeIn(sch))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]), FadeIn(sq[2]))
            vo.wait_until("c")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
