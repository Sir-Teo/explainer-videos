from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import ALPHA27, MONO, PART, letter_row, load

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
        pl = np.asarray(load("letters")["p"], float)
        s_lo, s_hi = float(-np.log2(pl.max())), float(-np.log2(pl.min()))
        rng = np.random.default_rng(6)  # one sample of the source, for the picture
        draw = "".join(ALPHA27[i] for i in rng.choice(27, size=96, p=pl / pl.sum()))
        sample = VGroup(*[letter_row(draw[k:k + 48], font_size=22) for k in (0, 48)]).arrange(DOWN, buff=0.2)
        sample_c = label(r"a text drawn this way", font_size=24, color=GREY_B)
        sample_g = VGroup(sample, sample_c).arrange(DOWN, buff=0.3).move_to(ax.c2p(5.8, 0.55))
        if sample_g.get_left()[0] < ax.c2p(0.4, 0)[0]:
            sample_g.shift(RIGHT * (ax.c2p(0.4, 0)[0] - sample_g.get_left()[0]))
        with self.voiceover(
            "Last chapter, whole bits wasted up to one per symbol, and long blocks were the cure. Here is why. "
            "<bookmark mark='a'/> Draw letters independently, with the books' frequencies, crude but exact to reason "
            "about, and measure the surprise per letter. <bookmark mark='b'/> For one letter, it's all over the "
            f"place, from {s_lo:.1f} bits to {s_hi:.1f}. <bookmark mark='c'/> Ten letters: the spread narrows. "
            f"<bookmark mark='d'/> A hundred, a thousand, ten thousand: it piles up at {H:.2f} bits, the entropy, its "
            f"spread shrinking from {sd[ns[0]]:.1f} bits to {sd[ns[-1]]:.2f}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(a))
            vo.wait_until("a")
            self.play(FadeIn(sample_c), AddTextLetterByLetter(sample[0], time_per_char=0.02),
                      AddTextLetterByLetter(sample[1], time_per_char=0.02))
            self.play(FadeIn(tag), Indicate(a.xlabel, color=WHITE, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeOut(sample_g), FadeIn(cur), FadeIn(nlab), FadeIn(ins), Create(hl), FadeIn(hlab))
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
                          color=C.ENTROPY).to_corner(UR, buff=0.35).shift(DOWN * 0.8)
        with self.voiceover(
            "It's the law of large numbers: a text's surprise is a sum over its letters, and the average of many "
            "independent surprises settles at their mean, the entropy. <bookmark mark='a'/> Shannon proved it in "
            "1948; McMillan and Breiman extended it to sources with memory, like real text. Its name: the "
            "asymptotic equipartition property."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(sub), FadeOut(nlab), FadeOut(ins), VGroup(a, cur, hl, hlab).animate.scale(0.62).to_corner(DL, buff=0.4))
            self.play(FadeIn(th, shift=DOWN * 0.2))
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
        whys = [why(r"each member: \ the definition"), why(r"the AEP"), why(r"each member has at least $2^{-n(H+\varepsilon)}$"), why(r"so there are at most this many"),
                why(r"and $P(A) \ge 1 - \delta$ forces at least this many")]
        step = ladder(self, rows, whys, keep=4, top=1.0, x=-2.4, buff=0.38, edge=6.9)
        with self.voiceover(
            "Call a sequence typical if its surprise per symbol is within a small epsilon of the entropy. "
            "<bookmark mark='a'/> Then each has probability close to two to the minus n H. "
            "<bookmark mark='b'/> By equipartition, together they hold nearly all the probability. "
            "<bookmark mark='c'/> Count them: their probabilities can't add past one, <bookmark mark='d'/> so there "
            "are at most two to the n H plus epsilon; <bookmark mark='e'/> and since they hold nearly everything, "
            "at least about two to the n H. Almost every sequence you'll see is one of these, all about equally "
            "likely."
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
        top_l = label(r"$\uparrow$ \ the most likely sequence: \ no spaces at all", font_size=20, color=WHITE)
        top_l.next_to(lb, RIGHT, buff=0.6)

        def readout(n):
            r = rows[n]
            return VGroup(
                MathTex(rf"n = {n}", font_size=34),
                label(rf"typical: \ ${pow2(r['log2_frac'])}$ of the sequences,", font_size=24, color=TYP),
                label(rf"${100 * r['P']:.1f}\%$ of the probability" if r["P"] < 0.9995 else
                      rf"$1 - 10^{{{math.log10(1 - r['P']):.0f}}}$ of the probability", font_size=24, color=TYP),
                label(rf"\quad the likeliest sequence: \ ${pow2(math.log2(r['p_top']))}$", font_size=22, color=GREY_A),
            ).arrange(RIGHT, buff=0.22).move_to([0, -3.45, 0])

        pic = picture(show[0])
        ro = readout(show[0])
        rng = np.random.default_rng(11)  # one run of the coin, for the picture
        coin = "".join(" " if rng.random() < q else "x" for _ in range(44))
        coin_g = VGroup(letter_row(coin, font_size=30, space_opacity=0.9),
                        label(r"a sample: \ \texttt{x} is a letter, \ \textvisiblespace\ a space", font_size=22, color=GREY_B))
        coin_g.arrange(DOWN, buff=0.2).move_to([0, (y_top + y_bot) / 2, 0])
        r0, r1 = rows[show[0]], rows[show[-1]]
        miss = 1 - r1["P"]
        missed = (f"all but one part in {1 / miss / 1e6:,.0f} million of the probability" if miss < 1e-6 else
                  f"{100 * r1['P']:.4f} percent of the probability")
        with self.voiceover(
            "Here is the typical set, drawn. Take a simpler source: a coin that writes a space with the books' "
            f"frequency, {q:.3f}. <bookmark mark='a'/> Lay out all two to the n sequences in a row, equally wide, "
            "from the most likely, with no spaces, to the least. <bookmark mark='b'/> Below, the same sequences, "
            "each as wide as its probability; the typical ones in gold. "
            f"<bookmark mark='c'/> With {show[0]} symbols, they are {100 * 2 ** r0['log2_frac']:.0f} percent of the "
            f"sequences, holding {100 * r0['P']:.0f} percent of the probability. <bookmark mark='d'/> Now make the "
            "sequences longer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), Create(frames[0]), Create(frames[1]), FadeIn(coin_g))
            vo.wait_until("a")
            self.play(FadeIn(lt), FadeIn(VGroup(*[m for k, m in enumerate(pic) if k % 3 == 1])))
            vo.wait_until("b")
            self.play(FadeOut(coin_g))
            self.play(FadeIn(lb), FadeIn(VGroup(*[m for k, m in enumerate(pic) if k % 3 != 1])), FadeIn(top_l))
            vo.wait_until("c")
            self.play(FadeIn(ro))
            vo.wait_until("d")
        with self.voiceover(
            "In the top row, the gold shrinks to a sliver, then to nothing you can see; in the bottom row it spreads "
            f"until it fills almost everything. <bookmark mark='a'/> By {show[-1]} symbols, the typical sequences "
            f"are two to the minus {-r1['log2_frac']:.0f} of all sequences, and carry {missed}. "
            "<bookmark mark='b'/> And the most likely sequence, all non-spaces, isn't typical at all: you'll "
            "essentially never see it."
        ) as vo:
            for n in show[1:]:
                new_pic, new_ro = picture(n), readout(n)
                self.play(FadeOut(pic), FadeIn(new_pic), FadeOut(ro), FadeIn(new_ro), run_time=1.0)
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
            label(r"typical? \ send $0$, then its index: \\ $\lceil n(H + \varepsilon) \rceil$ bits", font_size=26,
                  color=TYP),
            label(r"not typical? \ send $1$, then the sequence \\ as it is: \ $n \log_2 K$ bits", font_size=26,
                  color=GREY_A),
            label(r"average: \\ $\le n(H + \varepsilon) + 2 + P(\text{not typical})\, n \log_2 K$", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-3.3, -0.6, 0])
        a = axes([0.5, 3.0], [h - 0.02, 0.9], x_length=5.0, y_length=2.6, xlabel=r"block length $n$",
                 ylabel=r"bits per symbol", xticks=[1, 2, 3], yticks=[0.7, 0.8, 0.9],
                 xfmt=lambda v: f"10^{{{int(v)}}}", center=[3.6, -1.0, 0], font_size=18)
        ax = a.ax
        cur = curve(ax, np.log10(ns), np.minimum(rate, 0.9), C.BITS, 3.5)
        hline = DashedLine(ax.c2p(0.5, h), ax.c2p(3.0, h), color=C.ENTROPY, stroke_width=2.5)
        hl = label(rf"$H = {h:.3f}$", font_size=22, color=C.ENTROPY).next_to(ax.c2p(3.0, h), UP, buff=0.08)
        hl.align_to(hline, RIGHT)
        cap = label(r"Shannon's code on whole blocks of $n$ symbols", font_size=20, color=C.BITS)
        cap.next_to(a, UP, buff=0.05)
        tag = note(r"computed: \ exact, \ for the coin above").next_to(a, DOWN, buff=0.1)
        rng = np.random.default_rng(12)  # made-up members of the list, for the picture

        def member(k):
            return VGroup(Text(format(k, "06b"), font=MONO, font_size=22, color=TYP),
                          letter_row("".join(" " if rng.random() < 0.19 else "x" for _ in range(16)), font_size=22,
                                     space_opacity=0.9)).arrange(RIGHT, buff=0.35)

        listing = VGroup(*[member(k) for k in range(4)], MathTex(r"\vdots", font_size=28, color=GREY_B),
                         member(63)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        listing[4].set_x(listing[0][0].get_x())
        lst_t = label(r"the typical set, numbered", font_size=24, color=TYP).next_to(listing, UP, buff=0.2)
        lst_b = Brace(VGroup(*[m[0] for m in listing[:4]], listing[5][0]), LEFT, color=TYP)
        lst_l = label(r"$\approx nH$ \\ bits", font_size=22, color=TYP).next_to(lst_b, LEFT, buff=0.1)
        lst = VGroup(listing, lst_t, lst_b, lst_l, note(r"schematic").next_to(listing, DOWN, buff=0.2))
        lst.move_to([3.7, -1.0, 0])
        with self.voiceover(
            "That gives the source coding theorem. <bookmark mark='a'/> To compress n symbols: if the sequence is "
            "typical, send a zero, then its number in a list of the typical set: about n H bits. If not, send a one "
            "and the sequence itself. That's rare, so on average you pay about H bits per symbol. "
            "<bookmark mark='b'/> And no code does better: a shorter list would miss most typical sequences, and "
            "almost all the probability. <bookmark mark='c'/> Even last chapter's rounded "
            f"code, used on whole blocks, closes in on the entropy: {rate[0]:.3f} bits per symbol with blocks of "
            f"{int(ns[0])}, {rate[-1]:.4f} with blocks of {int(ns[-1])}, against {h:.4f}."
        ) as vo:
            self.play(FadeIn(th, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in code], lag_ratio=0.5), FadeIn(lst), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(th.body, color=C.ENTROPY, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeOut(lst))
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
        sq = VGroup(Square(2.9, stroke_color=GREY_B, stroke_width=2, fill_color=ALL, fill_opacity=0.4),
                    Square(1.25, stroke_width=0, fill_color=TYP, fill_opacity=0.6),
                    Square(0.36, stroke_width=0, fill_color=C.HUMAN, fill_opacity=0.9))
        sq[1].move_to(sq[0].get_corner(DL) + np.array([0.85, 0.85, 0]))
        sq[2].move_to(sq[1].get_center() + np.array([-0.22, -0.17, 0]))
        sq.to_corner(DR, buff=0.4)
        sch = note(r"areas not to scale").next_to(sq, UP, buff=0.1)
        names = VGroup(label(r"all strings", font_size=24, color=GREY_A),
                       label(r"typical under the letter frequencies", font_size=24, color=TYP),
                       label(r"typical English", font_size=24, color=C.HUMAN))
        for nm, y_ in zip(names, (sq[0].get_top()[1] - 0.3, sq[1].get_top()[1] - 0.1, sq[2].get_y())):
            nm.move_to([sq.get_left()[0] - 0.3, y_, 0], aligned_edge=RIGHT)
        take = label(r"a language model's job: \ find that corner; \ to write, \ draw from it", font_size=30,
                     color=C.BITS).to_edge(DOWN, buff=0.5).shift(LEFT * 1.6)
        with self.voiceover(
            "Now English: twenty-seven to the n strings of n letters. <bookmark mark='a'/> Under letter frequencies "
            f"alone, the typical ones are a fraction two to the minus {gap:.2f} n: for a page of {page:,} letters, "
            f"two to the minus {gap * page:,.0f}. <bookmark mark='b'/> At one bit per letter, real text is a far "
            "smaller corner. <bookmark mark='c'/> A language model's job is to find that corner, and to write, it "
            "draws from it: how, in Part 5."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(sq[0]), FadeIn(names[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]), FadeIn(sq[1]), FadeIn(sch), FadeIn(names[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]), FadeIn(sq[2]), FadeIn(names[2]))
            vo.wait_until("c")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
