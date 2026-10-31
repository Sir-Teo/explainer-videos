from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import DCOL, FIT, HIST, PART, SP, lag, load, predict_card, takeaway_card, visible_values

EPOCH_COLORS = ["#7FD3FF", C.INTERVAL, C.BITS, C.MODEL_Q, C.SURPRISE]


class Data(VoiceoverScene):
    def construct(self):
        self.card()
        self.predict()
        self.repeat()
        self.effective()
        self.stock()
        self.takeaway()

    def card(self):
        card = chapter_card(11, r"When the data runs out", r"Is reading the same text twice as good as new text?", part=PART)
        with self.voiceover("Chapter eleven. When the data runs out."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def repeat(self):
        r = load("repeat")
        U = [int(u) for u in r["unique"]]
        ep = [int(e) for e in r["epochs"]]
        fin = np.asarray(r["final"], float)
        total = int(r["total"])
        logs = [int(round(math.log2(u))) for u in U]
        allc = np.concatenate([np.asarray(r[f"curve{k}"])[:, 1] for k in logs])
        lo = float(np.floor(fin.min() * 10) / 10 - 0.05)
        hi = float(min(np.ceil(np.percentile(allc, 90) * 10) / 10, lo + 1.5))
        ax = CornerAxes(x_range=[14, math.log2(total), 1], y_range=[lo, hi, 0.2], x_length=6.4, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.0, -0.5, 0])
        xt = VGroup(*[MathTex(rf"2^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.08)
                      for v in range(14, int(math.log2(total)) + 1, 2)])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(14, v), LEFT, buff=0.08)
                      for v in np.arange(math.ceil(lo * 5) / 5, hi + 1e-9, 0.2)])
        xn = label(r"characters read so far", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"held-out bits per character", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        lines = VGroup()
        B = 256
        for k, col in zip(logs, EPOCH_COLORS):
            c = np.asarray(r[f"curve{k}"])
            xs = np.log2(c[:, 0] * B)
            keep = xs >= 14
            lines.add(curve(ax, xs[keep], visible_values(c[keep, 1], lo, hi), col, 3))
        lg = VGroup(*[label(rf"${u:,}$ distinct, \ ${e}$ epoch{'s' if e > 1 else ''}".replace(",", "{,}"), font_size=20, color=c)
                      for u, e, c in zip(U, ep, EPOCH_COLORS)]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lg.move_to([3.9, 1.6, 0])
        means = fin.mean(1)
        rows = VGroup(*[label(rf"${e}$: \ ${m:.3f}$ \ (${f.min():.3f}$--${f.max():.3f}$)", font_size=20, color=c)
                        for e, m, f, c in zip(ep, means, fin, EPOCH_COLORS)]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        rh = label(r"epochs: \ final bits, \ three seeds", font_size=20, color=GREY_A)
        tab = VGroup(rh, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.9, -1.5, 0])
        tag = note(rf"computed: \ width ${int(r['width'])}$, \ ${total:,}$ characters of training in every run".replace(",", "{,}"))
        tag.to_corner(DL, buff=0.2)
        d4 = means[1] - means[0]
        d16 = means[2] - means[0]
        worst = means[-1] - means[0]
        rises = np.asarray(r[f"curve{logs[-1]}"])[:, 1]
        overfit = rises[-1] > rises.min() + 0.02
        said1 = (
            f"Four epochs cost only {d4:.3f} bits: nearly as good as new text. " if d4 < 0.03 else
            f"Four epochs cost {d4:.3f} bits. "
        )
        said2 = (
            f"At two hundred and fifty-six, the model memorizes its sample: the held-out loss falls, then climbs, "
            f"and ends {worst:.2f} bits worse than fresh text." if overfit else
            f"At two hundred and fifty-six, it ends {worst:.2f} bits worse than fresh text."
        )
        with self.voiceover(
            "Good text is finite. What happens when a model has read it all and must read it again? Train our "
            f"character model on {total / 1e6:.1f} million characters every time, but drawn from fewer and fewer "
            "distinct ones, from one pass over fresh text down to two hundred and fifty-six passes over a small "
            "sample. <bookmark mark='a'/> "
            + said1
            + f"Sixteen cost {d16:.3f}. <bookmark mark='b'/> "
            + said2
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(tag), FadeIn(lg))
            self.play(LaggedStart(*[Create(l_) for l_ in lines[:2]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(lines[2]), FadeIn(tab[0]), FadeIn(rows[:3]))
            vo.wait_until("b")
            self.play(lag([Create(l_) for l_ in lines[3:]], lag_ratio=0.3), FadeIn(rows[3:]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def effective(self):
        r = load("repeat")
        U = np.asarray(r["unique"], float)
        ep = np.asarray(r["epochs"], float)
        eff = np.asarray(r["effective"], float)
        Rs, Rp = float(r["Rstar"]), float(r["Rstar_paper"])
        colors = {r"R^*": C.BITS, r"U": DCOL}
        rows = [
            cmath(r"\text{the } k\text{-th repeat is worth}", r"\ \ ", r"e^{-k/R^*}", r"\ \text{of new text}",
                  font_size=32, colors=colors),
            cmath(r"D'", r"=", r"U + U \textstyle\sum_{k=1}^{R} e^{-k/R^*}", font_size=32, colors=colors),
            cmath(r"D'", r"\approx", r"U + U R^* \big(1 - e^{-R/R^*}\big)", font_size=32, colors=colors),
        ]
        whys = [why(r"each pass a fixed fraction less useful"), why(r"$U$ distinct, \ read $1 + R$ times"),
                why(r"the sum as an integral \ (Muennighoff et al.)")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-1.8, buff=0.32, edge=6.9)
        lx = np.log2(ep)
        ax = CornerAxes(x_range=[0, lx.max() + 0.3, 2], y_range=[0, math.log2(max(np.nanmax(eff / U), 40)) + 0.3, 1],
                        x_length=5.8, y_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.6, -1.7, 0])
        xt = VGroup(*[MathTex(str(int(2 ** v)), font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for v in range(0, int(lx.max()) + 1, 2)])
        ymax = ax.y_range[1]
        yt = VGroup(*[MathTex(str(int(2 ** v)), font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                      for v in range(0, int(ymax) + 1, 2)])
        xn = label(r"epochs", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"worth, \ in passes of new text \ ($D'/U$)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(min(lx.max(), ymax), min(lx.max(), ymax)), color=GREY_D, stroke_width=1.5)
        dl = label(r"as good as new", font_size=18, color=GREY_B).next_to(ax.c2p(3.2, 3.2), UL, buff=0.05)
        es = np.geomspace(1, ep.max(), 80)

        def worth(R_):
            return np.log2(1 + R_ * (1 - np.exp(-(es - 1) / R_)))

        fit = curve(ax, np.log2(es), worth(Rs), C.BITS, 3.5, smooth=True)
        paper = DashedVMobject(curve(ax, np.log2(es), np.minimum(worth(Rp), ymax), GREY_A, 2.5, smooth=True), num_dashes=40)
        pts = VGroup(*[Dot(ax.c2p(a, math.log2(e / u)), radius=0.08, color=WHITE) for a, e, u in zip(lx, eff, U)
                       if np.isfinite(e)])
        off = [int(e_) for e_, v in zip(ep, eff) if not np.isfinite(v)]
        offl = label(r"off the curve: \ " + ", ".join(str(v) for v in off) + r" epochs, \ worse than any fresh run", font_size=18,
                     color=GREY_A).next_to(ax.c2p(lx.max(), 0), UL, buff=0.15) if off else VGroup()
        lg = VGroup(label(r"white: \ our runs, \ read off the fresh-data curve", font_size=20, color=WHITE),
                    label(rf"ours: \ $R^* = {Rs:.1f}$", font_size=22, color=C.BITS),
                    label(rf"Muennighoff et al.: \ $R^* = {Rp:.1f}$ \ (up to $9$ billion parameters)", font_size=20, color=GREY_A))
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.7, -1.4, 0])
        cap = (1 + Rs)
        said3 = (
            f"Muennighoff's team, with models of up to nine billion parameters, found {Rp:.1f}. Our small "
            "model gets less from repeating, " if Rs < Rp / 2 else
            f"Muennighoff's team found {Rp:.1f}, "
        )
        with self.voiceover(
            "How much is a repeat worth? In 2023, Niklas Muennighoff and colleagues proposed a simple answer. "
            "<bookmark mark='a'/> Suppose each pass over the same text is worth a fixed fraction less than the one "
            "before. <bookmark mark='b'/> Then U distinct characters read R more times are worth U plus a sum of "
            "shrinking terms, <bookmark mark='c'/> which saturates: however often you repeat, you never get more "
            "than U times one plus R-star. <bookmark mark='d'/> Read each of our runs off the fresh-data curve, to "
            f"find how much new text it was worth, and fit R-star: {Rs:.1f} passes. "
            + said3
            + f"and the ceiling is about {cap:.0f} times the distinct text."
        ) as vo:
            q = VGroup(label(r"How much is a repeat worth?", font_size=40, color=WHITE),
                       label(r"N.~Muennighoff et al., \textit{Scaling Data-Constrained Language Models} (2023)",
                             font_size=24, color=GREY_A)).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
            self.play(FadeIn(q[0], shift=UP * 0.2))
            self.play(FadeIn(q[1]))
            vo.wait_until("a")
            self.play(FadeOut(q), run_time=0.6)
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(diag), FadeIn(dl))
            self.play(lag([FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.2), FadeIn(lg[0]), FadeIn(offl))
            self.play(Create(fit), FadeIn(lg[1]), Create(paper), FadeIn(lg[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stock(self):
        hd = label(r"how much text is there?", font_size=36).to_edge(UP, buff=0.35)
        cards = VGroup(
            history_card(2024, r"Villalobos et al.\ (Epoch AI)",
                         r"projected usable public text at the $2028$ crossing: \ about $4 \times 10^{14}$ tokens, \ quality "
                         r"and repetition adjusted; \ their $2024$ forecast: training sets reach it between $2026$ and "
                         r"$2032$, "
                         r"most likely $2028$", width=6.2, color=HIST),
            history_card(2023, r"Muennighoff et al.", r"up to about $4$ epochs: \ almost as good as new data; \ beyond "
                         r"$16$: \ little left", width=6.2, color=HIST),
            history_card(2025, r"Alibaba, \ Qwen3", r"about $36$ trillion training tokens, \ including synthetic data; \ $119$ languages and dialects",
                         width=6.2, color=HIST),
        ).arrange(DOWN, buff=0.22).move_to([-3.0, -0.4, 0])
        # a bar: the stock against one frontier run (log scale), schematic positions from the cited numbers
        ax = NumberLine(x_range=[12, 15, 1], length=5.4, include_ticks=True, color=GREY_C).move_to([3.6, 0.6, 0])
        ticks = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=22, color=GREY_B).next_to(ax.n2p(v), DOWN, buff=0.12)
                         for v in (12, 13, 14, 15)])
        l4 = Dot(ax.n2p(math.log10(36e12)), radius=0.1, color=C.TRUE_P)
        l4l = label(r"Qwen3: \ $3.6\times10^{13}$", font_size=20, color=C.TRUE_P).next_to(l4, UP, buff=0.15)
        st = Dot(ax.n2p(math.log10(4e14)), radius=0.1, color=SP)
        stl = label(r"$2028$ projected stock: \ $4\times10^{14}$", font_size=20, color=SP).next_to(st, UP, buff=0.15)
        unit = label(r"tokens", font_size=20, color=GREY_A).next_to(ticks, DOWN, buff=0.1)
        ways = label(r"ways around it: \ repeating, \ rephrasing, \\ synthetic text, \ other kinds of data \ (Part 18)",
                     font_size=22, color=GREY_A).move_to([3.6, -1.8, 0])
        with self.voiceover(
            "How close are we? In 2024, Pablo Villalobos and colleagues at Epoch AI projected usable "
            "public text at the 2028 crossing at about four times ten to the fourteen tokens, after allowing for quality and repetition, "
            "and projected that training sets would reach it between 2026 and 2032, most likely in 2028. "
            "<bookmark mark='a'/> Repeating stretches it: Muennighoff's four epochs are nearly free. "
            "<bookmark mark='b'/> Alibaba's Qwen3, in 2025, was pretrained on about thirty-six trillion tokens: "
            "including synthetic data. Training tokens are not a count of distinct human text. <bookmark mark='c'/> So the field is looking for more: "
            "rephrased text, synthetic text and other kinds of data, the subject of part eighteen."
        ) as vo:
            self.play(FadeIn(hd), FadeIn(cards[0], shift=RIGHT * 0.1), Create(ax), FadeIn(ticks), FadeIn(unit))
            self.play(FadeIn(st), FadeIn(stl))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=RIGHT * 0.1), FadeIn(l4), FadeIn(l4l))
            vo.wait_until("c")
            self.play(FadeIn(ways))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        pc = predict_card(r"Train for the same number of characters, \ but on a quarter of the text, \ read four "
                          r"times. \ How much worse than a model that read fresh text all the way?")
        with self.voiceover(
            "Pause and predict. Train for the same number of characters, but on a quarter of the text, read four "
            "times over. How much worse will it be than a model that read fresh text all the way?"
        ):
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(pc))

    def takeaway(self):
        tk = takeaway_card(r"Repeats are worth less, \ then nothing",
                           r"A few passes over the same data are almost as good as new data; \ each repeat is worth "
                           r"less, \ and the total saturates at about $U(1 + R^*)$.",
                           r"next: \ two other budgets, \ experts and bits")
        with self.voiceover(
            "The takeaway: a few passes over the same data are almost as good as new data, but each repeat is worth "
            "less, and the total saturates. Next, two other budgets: experts, and bits."
        ) as vo:
            self.play(FadeIn(tk[0], shift=UP * 0.2))
            self.wait(max(0.0, vo.duration * 0.5 - 1.0))
            self.play(FadeIn(tk[1]))
        self.wait(0.4)
        self.play(FadeOut(tk))
