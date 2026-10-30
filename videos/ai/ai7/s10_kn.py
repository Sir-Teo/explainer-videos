from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import MONO, PART, card_in, load

KN = C.COUNTING
ADD = GREY_B
GT = C.BITS  # Good-Turing's estimate
HELD = C.TRUE_P  # the truth on held-out text


class KneserNey(VoiceoverScene):
    def construct(self):
        card_in(self, 9, r"Kneser--Ney, from Good--Turing", r"How do you count what you've never seen?",
                "Chapter nine. Kneser-Ney, from Good-Turing.")
        self.goodturing()
        self.discount()
        self.orders()
        self.idea()
        self.board()

    # ------------------------------------------------------------------
    def goodturing(self):
        d = load("goodturing")
        rows = d["rows"]
        h = history_card(1953, r"I.~J.~Good, \ after Alan Turing", r"at Bletchley Park: \\ the chance of what has "
                         r"never yet been seen, \\ for breaking German codes", width=7.0).move_to([0, 1.3, 0])
        colors = {r"r^*": GT, r"N_{r+1}": C.MODEL_Q, r"N_r": C.MODEL_Q, r"N_1": C.MODEL_Q}
        f1 = cmath(r"r^*", r"=", r"(r + 1)\,", r"\frac{N_{r+1}}{N_r}", colors=colors, font_size=44)
        f2 = cmath(r"p(\text{unseen})", r"=", r"\frac{N_1}{N}", colors=colors, font_size=40)
        fs = VGroup(f1, f2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([-3.6, 2.1, 0])
        nr = label(r"$N_r$: \ how many different word pairs were seen exactly $r$ times", font_size=22, color=C.MODEL_Q)
        nr.next_to(fs, DOWN, buff=0.25).align_to(fs, LEFT)
        hdr = VGroup(MathTex(r"r", font_size=28), MathTex(r"N_r", font_size=28, color=C.MODEL_Q),
                     label(r"Good--Turing $r^*$", font_size=22, color=GT), label(r"held out", font_size=22, color=HELD))
        tab = VGroup(hdr)
        for r_ in rows:
            nrv = sci(r_["Nr"], 2) if r_["Nr"] >= 1e6 else fmt_int(int(r_["Nr"]))
            dg = 6 if r_["r"] == 0 else 2
            tab.add(VGroup(MathTex(str(r_["r"]), font_size=26), MathTex(nrv, font_size=26, color=C.MODEL_Q),
                           MathTex(f"{r_['gt']:.{dg}f}", font_size=26, color=GT),
                           MathTex(f"{r_['held']:.{dg}f}", font_size=26, color=HELD)))
        for j, x_ in enumerate((-5.6, -3.9, -1.4, 1.2)):
            for r_ in tab:
                r_[j].set_x(x_)
        for i, r_ in enumerate(tab):
            for m in r_:
                m.set_y(0.2 - 0.38 * i)
        tab.shift(RIGHT * 0.6)
        foot = label(rf"word pairs in the novels: \ ${d['tokens']:,}$ words, \ two halves; \ ``held out'': the average count "
                     r"in the other half".replace(",", "{,}"), font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        nr_ = np.array([r_["Nr"] for r_ in rows[1:]])
        gnr = axes([0.5, len(nr_) + 0.5, 1], [0, 6, 1], x_length=5.2, y_length=2.2, xlabel=r"seen $r$ times",
                   ylabel=r"how many different word pairs", xticks=list(range(1, len(nr_) + 1)), yticks=[0, 2, 4, 6],
                   yfmt=lambda v: f"10^{{{int(v)}}}", center=[0, -2.0, 0])
        nrb = VGroup(*[Rectangle(width=0.4, height=max(gnr.ax.c2p(0, np.log10(v))[1] - gnr.ax.c2p(0, 0)[1], 0.02),
                                 stroke_width=0, fill_color=C.MODEL_Q, fill_opacity=0.85).move_to(gnr.ax.c2p(k + 1, np.log10(v) / 2))
                       for k, v in enumerate(nr_)])
        r1 = rows[1]
        close = abs(r1["gt"] - r1["held"]) < 0.1 and abs(rows[0]["gt"] - rows[0]["held"]) / rows[0]["held"] < 0.2
        verdict = (f"It works. A pair seen once in one half of the novels turns up on average {r1['held']:.2f} times in "
                   f"the other half; Good–Turing predicted {r1['gt']:.2f}, from counts alone."
                   if close else
                   f"A pair seen once in one half of the novels turns up on average {r1['held']:.2f} times in the "
                   f"other half; Good–Turing predicted {r1['gt']:.2f}.")
        with self.voiceover(
            "Counting fails on what it has never seen, and most things are never seen. The fix came from code "
            "breaking. At Bletchley Park, Alan Turing and his assistant Jack Good needed the chance of things they had "
            "never yet seen. Good published the method in 1953, crediting Turing. <bookmark mark='a'/> "
            "Let N r be the number of different things seen exactly r times. Something seen r times is really worth "
            "r star: r plus one, times N r plus one over N r. And the total chance of everything unseen is N one over "
            "N, the share of things seen exactly once. <bookmark mark='b'/> Let's test it on pairs of words in the "
            "novels: count them in one half, then check the counts in the other half. <bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(FadeIn(h, shift=UP * 0.2), FadeIn(gnr), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in nrb], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(h.animate.scale(0.75).move_to([3.7, 2.3, 0]), FadeOut(gnr), FadeOut(nrb))
            self.play(Write(f1), FadeIn(nr))
            self.play(Write(f2))
            vo.wait_until("b")
            self.play(FadeOut(h), FadeIn(tab[0]), LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[2])) for r_ in tab[1:]],
                                                              lag_ratio=0.1), FadeIn(foot), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_[3]) for r_ in tab[1:]], lag_ratio=0.1), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def discount(self):
        d = load("goodturing")
        rows = d["rows"][1:]
        disc = np.array([r_["r"] - r_["held"] for r_ in rows])
        g = axes([0.5, len(rows) + 0.5, 1], [0, 1.2, 0.25], x_length=7.0, y_length=3.8, xlabel=r"count $r$ in one half",
                 ylabel=r"$r$ minus the average count in the other half", xticks=list(range(1, len(rows) + 1)),
                 yticks=[0, 0.5, 1.0], center=[-2.4, -0.4, 0])
        ax = g.ax
        bars_ = VGroup(*[Rectangle(width=0.45, height=max(ax.c2p(0.5, v)[1] - ax.c2p(0.5, 0)[1], 0.01), stroke_width=0,
                                   fill_color=HELD, fill_opacity=0.85).move_to(ax.c2p(i + 1, v / 2))
                         for i, v in enumerate(disc)])
        vals = VGroup(*[MathTex(f"{v:.2f}", font_size=22, color=HELD).next_to(b, UP, buff=0.06) for v, b in zip(disc, bars_)])
        mid = float(np.mean(disc[1:]))
        flat = disc[1:].max() - disc[1:].min() < 0.3
        colors = {r"D": C.SURPRISE}
        f = cmath(r"p(w \mid h)", r"=", r"\frac{\max(N(h w) -", r"D", r",\; 0)}{N(h)}", r"+", r"\text{(the rest, shared out)}",
                  colors=colors, font_size=34).move_to([3.0, 2.6, 0])
        if f.width > 7.0:
            f.width = 7.0
        nm = label(r"absolute discounting \\ (Ney, Essen \& Kneser, 1994)", font_size=24, color=C.SURPRISE)
        nm.move_to([4.6, 0.6, 0])
        verdict = (f"From two times on, the loss is nearly the same for every count, between {disc[1:].min():.2f} and "
                   f"{disc[1:].max():.2f}. Kenneth Church and William Gale saw the same thing in newswire in 1991."
                   if flat else
                   f"The loss ranges from {disc.min():.2f} to {disc.max():.2f}.")
        with self.voiceover(
            "Look at what a count loses between the two halves: r, minus what the same pairs average in the other "
            f"half. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> So instead of a formula for every r, "
            "subtract one fixed discount, D, from every count you've seen, and share the savings among what you "
            "haven't. That's absolute discounting, and it's the first half of Kneser–Ney."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_], lag_ratio=0.1), FadeIn(vals), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(f), FadeIn(nm))
        del mid
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def orders(self):
        k = load("kn")
        p1 = np.asarray(k["part1_rows"])
        kn = np.array([r["test"] for r in k["rows"]])
        M = len(kn) - 1
        ax = Axes(x_range=[0, M, 1], y_range=[1.8, 4.8, 0.5], x_length=8.0, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.4, 0])
        xl = VGroup(*[MathTex(str(i), font_size=24, color=GREY_B).next_to(ax.c2p(i, 1.8), DOWN, buff=0.12) for i in range(M + 1)])
        yl = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for v in (2.0, 3.0, 4.0)])
        xn = label(r"characters of context", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.55)
        yn = label(r"bits per character on the passage", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        c1 = VMobject(color=ADD, stroke_width=4).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(p1[:M + 1])])
        d1 = VGroup(*[Dot(ax.c2p(i, v), radius=0.06, color=ADD) for i, v in enumerate(p1[:M + 1])])
        c2 = VMobject(color=KN, stroke_width=4).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(kn)])
        d2 = VGroup(*[Dot(ax.c2p(i, v), radius=0.06, color=KN) for i, v in enumerate(kn)])
        l1 = label(r"Part 1: \ add a little to every count", font_size=26, color=ADD).move_to([4.4, 1.2, 0])
        l2 = label(rf"Kneser--Ney: \ ${kn[-1]:.2f}$ at ${M}$ characters", font_size=26, color=KN).next_to(l1, DOWN, buff=0.4)
        l2.align_to(l1, LEFT)
        best1 = int(np.argmin(p1))
        with self.voiceover(
            "Back to part one's scoreboard. The best counting model there used four characters of context and reached "
            f"{p1[best1]:.2f} bits per character on the passage. <bookmark mark='a'/> Longer contexts should help, but "
            "they're rare: most long contexts in the passage appeared only a handful of times in thirty novels, if at "
            "all. With part one's simple smoothing, the score gets worse beyond four characters. "
            "<bookmark mark='b'/> Better smoothing keeps improving."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xn), FadeIn(yn))
            self.play(Create(c1), LaggedStart(*[FadeIn(d) for d in d1], lag_ratio=0.1), FadeIn(l1), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(d1[best1], scale_factor=1.8, color=WHITE))
            vo.wait_until("b")
            self.play(Create(c2), LaggedStart(*[FadeIn(d) for d in d2], lag_ratio=0.1), FadeIn(l2), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def idea(self):
        d = load("goodturing")
        colors = {r"D": C.SURPRISE, r"P_{\mathrm{KN}}(c \mid h')": KN, r"\lambda(h)": C.SURPRISE}
        f = cmath(r"P_{\mathrm{KN}}(c \mid h)", "=", r"\frac{\max\big(N(h c) -", r"D", r",\, 0\big)}{N(h)}", "+",
                  r"\lambda(h)", r"\,", r"P_{\mathrm{KN}}(c \mid h')", colors=colors, font_size=40).to_edge(UP, buff=0.6)
        n1 = label(r"$h$: \ the context; \ $h'$: \ the context with its oldest character dropped", font_size=24,
                   color=GREY_A).next_to(f, DOWN, buff=0.25)
        idea1 = label(r"1. \ take a fixed discount $D$ off every count seen, \\ and hand it to the shorter context",
                      font_size=28, color=C.SURPRISE)
        cont = cmath(r"N(h c)", r"\;\longrightarrow\;", r"N_{1+}(\,\bullet\, h c)", font_size=40)
        idea2 = label(r"2. \ below the top, count how many \emph{different} contexts \\ a character follows, \ not how "
                      r"often it appears", font_size=28, color=KN)
        VGroup(idea1, idea2).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([-1.6, -1.2, 0])
        cont.next_to(idea2, DOWN, buff=0.3).align_to(idea2, LEFT).shift(RIGHT * 0.5)
        ex = VGroup(VGroup(data_text(d["word"], font=MONO, font_size=26, color=WHITE),
                           label(rf"${d['word_count']:,}$ times, \ after ${d['word_prev']}$ different word"
                                 rf"{'s' if d['word_prev'] != 1 else ''}".replace(",", "{,}"), font_size=22, color=GREY_A)
                           ).arrange(RIGHT, buff=0.2),
                    VGroup(data_text(d["other"], font=MONO, font_size=26, color=WHITE),
                           label(rf"${d['other_count']:,}$ times, \ after ${d['other_prev']}$ different words".replace(",", "{,}"),
                                 font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.2))
        ex.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, -2.9, 0])
        exl = label(r"in the novels:", font_size=20, color=GREY_B).next_to(ex, UP, buff=0.12).align_to(ex, LEFT)
        cite_ = cite(r"R.~Kneser \& H.~Ney (1995); \ S.~Chen \& J.~Goodman (1998)", corner=UR)
        U, dh = 0.32, 0.32
        counts = [6, 4, 3, 2]
        cbars = VGroup(*[Rectangle(width=0.45, height=c * U - dh, stroke_width=0, fill_color=KN, fill_opacity=0.85)
                         .move_to([2.6 + 0.65 * i, -1.3 + (c * U - dh) / 2, 0]) for i, c in enumerate(counts)])
        slices = VGroup(*[Rectangle(width=0.45, height=dh, stroke_width=0, fill_color=C.SURPRISE, fill_opacity=0.9)
                          .next_to(b, UP, buff=0) for b in cbars])
        base = Line([2.25, -1.3, 0], [6.9, -1.3, 0], color=GREY_C, stroke_width=2)
        pile = Rectangle(width=0.55, height=dh * len(counts), stroke_color=C.SURPRISE, stroke_width=2)
        pile.move_to([6.2, -1.3 + dh * len(counts) / 2, 0])
        dl = MathTex(r"D", font_size=30, color=C.SURPRISE).next_to(slices[0], LEFT, buff=0.12)
        cl = label(r"counts after $h$ \ (schematic)", font_size=20, color=KN).next_to(cbars, DOWN, buff=0.1)
        pl = label(r"to $h'$", font_size=22, color=C.SURPRISE).next_to(pile, DOWN, buff=0.12)
        moved = VGroup(*[s.copy().move_to([6.2, -1.3 + dh * (j + 0.5), 0]).set(width=0.55)
                         for j, s in enumerate(slices)])
        with self.voiceover(
            "Reinhard Kneser and Hermann Ney's smoothing, from 1995, has two ideas. <bookmark mark='a'/> First, "
            "absolute discounting: shave the fixed discount off every count you've seen, <bookmark mark='c'/> and use "
            "the savings to back off to a shorter context, one character fewer: blend the two. "
            "<bookmark mark='b'/> Second, judge the shorter contexts by their variety. In the novels, "
            f"'{d['word']}' appears {d['word_count']:,} times, but only ever after "
            f"{d['word_prev']} different word{'s' if d['word_prev'] != 1 else ''}, '{d['word_top_prev']}'. "
            f"'{d['other']}' is about as common, and follows {d['other_prev']:,} different words. "
            f"<bookmark mark='d'/> After an unfamiliar word, '{d['other']}' is the far better guess. So the shorter "
            "contexts count how many different contexts something follows, not how often it appears."
        ) as vo:
            self.play(Write(f), FadeIn(n1), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(idea1), Indicate(term(f, r"D"), color=C.SURPRISE), Create(base), FadeIn(cbars),
                      FadeIn(slices), FadeIn(cl))
            self.play(FadeIn(dl))
            vo.wait_until("c")
            self.play(Create(pile), FadeIn(pl), *[ReplacementTransform(s, m) for s, m in zip(slices, moved)],
                      run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(idea2), FadeIn(exl), FadeIn(ex[0]))
            self.play(FadeIn(ex[1]))
            vo.wait_until("d")
            self.play(FadeIn(cont))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        k = load("kn")
        sb = load("scoreboard")
        rows = [dict(r) for r in sb["rows"]]
        i, j = int(sb["new"][0]), int(sb["new"][1])
        rows[j] = {key: v for key, v in rows[j].items() if key != "bits"}  # chapter ten's row, still to come
        board = scoreboard(rows, highlight=(i,), max_bits=8.0)
        board.scale_to_fit_height(min(board.height, 6.6)).move_to(DOWN * 0.1)
        row = board.rows[i]
        glow = SurroundingRectangle(row, color=KN, buff=0.08, corner_radius=0.08)
        with self.voiceover(
            f"With seven characters of context, Kneser–Ney reaches {k['best_bits']:.2f} bits per character on the "
            "passage. <bookmark mark='a'/> For two decades, from speech recognition to machine translation, a "
            "Kneser–Ney model was the language model in the noisy channel. Stanley Chen and Joshua Goodman's careful "
            "comparison in 1998 found it the best of all the counting methods. But why stop at seven characters?"
        ) as vo:
            self.play(FadeIn(board))
            vo.wait_until("a")
            self.play(Create(glow), Indicate(row, color=KN, scale_factor=1.05))
        self.wait(0.5)
        self.clear_scene()
