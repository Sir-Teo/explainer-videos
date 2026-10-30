from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import MONO, PART, card_in, load

INF = "#4FD1C5"  # the infinity-gram
KN = C.COUNTING


def show(s: str) -> str:
    return s.replace(" ", "␣").replace("\n", "¶")


class Infini(VoiceoverScene):
    def construct(self):
        card_in(self, 10, r"The $\infty$-gram", r"Why stop at seven characters of context?",
                "Chapter ten. The infinity-gram.")
        self.suffixes()
        self.grow()
        self.result()

    # ------------------------------------------------------------------
    def suffixes(self):
        d = load("infini")
        demo, sa = d["demo"], [int(i) for i in d["demo_sa"]]
        n = len(demo)
        rows = VGroup(*[VGroup(MathTex(str(i), font_size=22, color=GREY_B),
                               data_text(show(demo[i:]), font=MONO, font_size=22, color=WHITE)).arrange(RIGHT, buff=0.3)
                        for i in range(n)])
        for r in rows:
            r[0].set_x(-0.4)
            r[1].next_to(r[0], RIGHT, buff=0.3)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-3.6, -0.3, 0])
        ys = [r.get_y() for r in rows]
        title = VGroup(label(r"every suffix of the text \ (start position, \ the rest)", font_size=22, color=GREY_A))
        title.next_to(rows, UP, buff=0.2)
        title2 = label(r"sorted: \ the suffix array", font_size=22, color=INF).move_to(title)
        q = "rose"
        hit = [k for k, i in enumerate(sa) if demo[i:].startswith(q)]
        box = SurroundingRectangle(VGroup(*[rows[sa[k]] for k in hit]), color=INF, buff=0.06)
        ql = label(rf"``{q}'': \ one block of the sorted list, \ found by binary search", font_size=22, color=INF)
        big = VGroup(label(rf"the thirty novels: \ ${d['n']:,}$ suffixes, \ sorted".replace(",", "{,}"), font_size=28),
                     label(r"$4$ bytes each; \ any string's count in about $2 \times 25$ comparisons", font_size=24,
                           color=GREY_A),
                     label(r"no table of $n$-grams, \ no limit on $n$", font_size=26, color=INF))
        big.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.6, 0])
        cites = cite(r"U.~Manber \& G.~Myers, suffix arrays (1990); \ J.~Liu et al., \textit{Infini-gram} (2024)", corner=DR)
        with self.voiceover(
            "Kneser–Ney stops at seven characters because its tables of counts explode: every longer context is "
            "another row. But a count is just a search through the text, and searching can be fast. "
            "<bookmark mark='a'/> Take every suffix of the text: the text from each position to the end. Here's a "
            "tiny one. <bookmark mark='b'/> Sort them alphabetically. That's a suffix array, from Udi Manber and Gene "
            "Myers in 1990. <bookmark mark='c'/> Every occurrence of any string, of any length, is now one "
            "contiguous block of the list, found by binary search, and the block's size is the count. "
            f"<bookmark mark='d'/> For the thirty novels that's {d['n']:,} suffixes, a hundred megabytes of "
            "positions, sorted in about a minute on this machine. In 2024 Jiacheng Liu and colleagues built one over "
            "five trillion tokens of web text, and called the model it gives an infinity-gram."
        ) as vo:
            self.play(FadeIn(cites))
            vo.wait_until("a")
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(*[rows[i].animate.set_y(ys[k]) for k, i in enumerate(sa)], ReplacementTransform(title, title2),
                      run_time=2.0)
            vo.wait_until("c")
            box = SurroundingRectangle(VGroup(*[rows[sa[k]] for k in hit]), color=INF, buff=0.06)
            ql.next_to(box, RIGHT, buff=0.2)
            self.play(Create(box), FadeIn(ql))
            vo.wait_until("d")
            self.play(FadeOut(ql), FadeIn(big, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grow(self):
        d = load("infini")
        ctx, counts = d["grow_context"], [int(c) for c in d["grow_counts"]]
        L = len(counts)
        g = axes([0, L + 1, 5], [0, 7, 1], x_length=6.4, y_length=3.2, xlabel=r"characters of context",
                 ylabel=r"times the context appears in the novels", xticks=[1, 5, 10, 15, 20, 25][: 1 + L // 5],
                 yticks=[0, 2, 4, 6], yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.6, -0.3, 0])
        ax = g.ax
        bars_ = VGroup(*[Rectangle(width=0.16, height=max(ax.c2p(0, np.log10(c))[1] - ax.c2p(0, 0)[1], 0.02), stroke_width=0,
                                   fill_color=INF, fill_opacity=0.9).move_to(ax.c2p(k + 1, np.log10(c) / 2))
                         for k, c in enumerate(counts)])
        txt = VGroup(*[data_text(show(ch), font=MONO, font_size=26, color=GREY_D) for ch in ctx])
        txt.arrange(RIGHT, buff=0.02).to_edge(UP, buff=0.5)
        if txt.width > 12.5:
            txt.width = 12.5
        cur = Integer(0, font_size=30, color=INF)
        curl = VGroup(label(r"count:", font_size=24, color=GREY_A), cur).arrange(RIGHT, buff=0.15)
        curl.next_to(txt, DOWN, buff=0.3)
        hist = np.asarray(d["hist"])
        g2 = axes([0, 41, 10], [0, float(hist.max()) * 1.1, 1000], x_length=4.4, y_length=2.6,
                  xlabel=r"longest match, characters", ylabel=r"positions in the passage", xticks=[0, 10, 20, 30, 40],
                  center=[4.3, -0.6, 0])
        hb = VGroup(*[Rectangle(width=0.09, height=max(g2.ax.c2p(0, v)[1] - g2.ax.c2p(0, 0)[1], 0.005), stroke_width=0,
                                fill_color=INF, fill_opacity=0.85).move_to(g2.ax.c2p(k + 0.5, v / 2)) for k, v in enumerate(hist)])
        stats = label(rf"median ${d['median_L']:.0f}$, \ longest ${d['max_L']}$", font_size=22, color=INF).next_to(g2, DOWN, buff=0.1)
        last = ("this context appears exactly once, and one more makes it vanish." if counts[-1] == 1 else
                f"this context still appears {counts[-1]} times, and one more makes it vanish.")
        with self.voiceover(
            "Now predict the passage. At each character, take the context before it and extend it to the left, one "
            "character at a time, counting as we go. <bookmark mark='a'/> One character occurs millions of times "
            f"in the novels. Every extra character cuts the count, until, at {L} characters, " + last +
            " <bookmark mark='b'/> The infinity-gram predicts from the "
            "longest context the novels contain: whatever followed it there. <bookmark mark='c'/> Over the "
            f"Maltese Falcon passage, the longest match is usually about {d['median_L']:.0f} characters, and at most "
            f"{d['max_L']}: the novels have never seen most of Hammett's sentences, but they've seen their pieces."
        ) as vo:
            self.play(FadeIn(txt), FadeIn(g), FadeIn(curl))
            vo.wait_until("a")
            for k, c in enumerate(counts):
                rt = 0.35 if k < 8 else 0.18
                self.play(txt[len(ctx) - 1 - k].animate.set_color(INF), FadeIn(bars_[k]),
                          ChangeDecimalToValue(cur, c), run_time=rt)
            vo.wait_until("b")
            self.play(Indicate(txt[len(ctx) - L:], color=INF))
            vo.wait_until("c")
            self.play(FadeIn(g2), LaggedStart(*[GrowFromEdge(b, DOWN) for b in hb], lag_ratio=0.02), FadeIn(stats))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        d = load("infini")
        sb = load("scoreboard")
        acc, zero, mix, kn = d["acc"], d["zero"], d["mix_bits"], d["kn_bits"]
        a = VGroup(label(r"the $\infty$-gram alone:", font_size=26, color=INF),
                   label(rf"next character right: \ ${100 * acc:.0f}\%$ of the time", font_size=24),
                   label(rf"probability $0$ for the true character: \ ${100 * zero:.0f}\%$ of the time", font_size=24),
                   label(r"$\Rightarrow$ \ infinitely many bits", font_size=24, color=C.SURPRISE))
        a.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.6, 2.0, 0])
        colors = {r"\lambda_L": INF, r"P_\infty": INF, r"P_{\mathrm{KN}}": KN}
        eq = cmath(r"P", r"=", r"\lambda_L", r"\,", r"P_\infty", r"+", r"(1 - \lambda_L)", r"\,", r"P_{\mathrm{KN}}",
                   colors=colors, font_size=40).move_to([3.4, 2.4, 0])
        en_ = label(r"one weight per length of match, \\ chosen on held-out text from the novels", font_size=22,
                    color=GREY_A).next_to(eq, DOWN, buff=0.2)
        rows = [dict(r) for r in sb["rows"]]
        i, j = int(sb["new"][0]), int(sb["new"][1])
        keep = [r for k, r in enumerate(rows) if k in (i - 1, i, j) or r.get("key") in ("bzip2",)]
        board = scoreboard(keep, highlight=(len(keep) - 1,), max_bits=3.5, bar_width=5.0, row_h=0.55, font_size=24)
        board.scale_to_fit_width(min(board.width, 9.0)).move_to([0.2, -1.6, 0])
        gain = d["gain"]
        if gain > 0.005:
            verdict = (f"Mixed with Kneser–Ney, trusting it more when the match is long, it gives {mix:.3f} bits per "
                       f"character, against Kneser–Ney's {kn:.3f}: a small gain, and the scoreboard's last counting row.")
        elif gain > 0:
            verdict = (f"Mixed with Kneser–Ney, it gives {mix:.3f} bits per character, against Kneser–Ney's {kn:.3f}: "
                       "barely better. The long matches are too rare in a new novel.")
        else:
            verdict = (f"Mixed with Kneser–Ney, it gives {mix:.3f} bits per character, against Kneser–Ney's {kn:.3f}: "
                       "no gain on a novel the books have never seen.")
        with self.voiceover(
            "How good is it? On its own, the infinity-gram's single most likely next character is right "
            f"{100 * acc:.0f} percent of the time. <bookmark mark='a'/> But {100 * zero:.0f} percent of the time "
            "it gives the true character no chance at all, because it never saw it after that context. One zero, "
            "and the bits are infinite. <bookmark mark='b'/> So it's mixed with Kneser–Ney, with a weight for "
            "each length of match. <bookmark mark='c'/> " + verdict + " <bookmark mark='d'/> At web scale, Liu's "
            "infinity-gram predicted the next token correctly 47 percent of the time and helped neural models when "
            "mixed in; and indexes like it now trace a language model's words back to the documents it was trained "
            "on."
        ) as vo:
            self.play(FadeIn(a[0]), FadeIn(a[1]))
            vo.wait_until("a")
            self.play(FadeIn(a[2]))
            self.play(FadeIn(a[3]))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(en_))
            vo.wait_until("c")
            self.play(FadeIn(board))
            self.play(Indicate(board.rows[len(keep) - 1], color=INF, scale_factor=1.04))
            vo.wait_until("d")
            self.play(Circumscribe(board.rows[len(keep) - 1], color=INF))
        self.wait(0.3)
        self.clear_scene()
