from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import DCOL, HIST, NCOL, PART, SP, load


class Kaplan(VoiceoverScene):
    def construct(self):
        self.card()
        self.gopher()
        self.counting()
        self.replication()

    def card(self):
        card = chapter_card(9, r"What Kaplan missed", r"Why did two careful studies disagree?", lit=(2020, 2022),
                            part=PART)
        with self.voiceover("Chapter nine. What Kaplan missed."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def gopher(self):
        # one budget, two shapes: Gopher (280 billion parameters, 300 billion tokens), Chinchilla (70 billion, 1.4 trillion)
        u = 0.0105  # screen units per billion parameters (width) ...
        v = 0.0021  # ... and per billion tokens (height)
        gw, gh = 280 * u, 300 * v
        cw, chh = 70 * u, 1400 * v
        base = np.array([-5.6, -2.4, 0])
        gop = Rectangle(width=gw, height=gh, stroke_color=SP, stroke_width=2.5, fill_color=SP, fill_opacity=0.25)
        gop.move_to(base, aligned_edge=DL)
        chi = Rectangle(width=cw, height=chh, stroke_color=C.TRUE_P, stroke_width=2.5, fill_color=C.TRUE_P, fill_opacity=0.25)
        chi.move_to(base + np.array([gw + 0.9, 0, 0]), aligned_edge=DL)
        gl = VGroup(label(r"Gopher \ (2021)", font_size=24, color=SP),
                    label(r"$280$ billion parameters \\ $300$ billion tokens", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.08)
        gl.next_to(gop, UP, buff=0.15)
        cl = VGroup(label(r"Chinchilla \ (2022)", font_size=24, color=C.TRUE_P),
                    label(r"$70$ billion parameters \\ $1.4$ trillion tokens", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.08)
        cl.next_to(chi, RIGHT, buff=0.2).align_to(chi, UP)
        ax_n = label(r"parameters $\rightarrow$", font_size=20, color=NCOL).next_to(gop, DOWN, buff=0.12).align_to(gop, LEFT)
        ax_d = label(r"tokens $\rightarrow$", font_size=20, color=DCOL).rotate(PI / 2).next_to(gop, LEFT, buff=0.12).align_to(gop, DOWN)
        same = label(r"the same compute: \ about $5.8 \times 10^{23}$ operations \ (area $\propto ND$)", font_size=22,
                     color=GREY_A).to_edge(UP, buff=0.35)
        res = VGroup(label(r"Chinchilla won on almost every test:", font_size=24, color=WHITE),
                     label(r"MMLU $67.5\%$, \ more than $7$ points above Gopher", font_size=24, color=C.TRUE_P),
                     label(r"smaller, \ so cheaper to run", font_size=24, color=C.TRUE_P))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, 1.2, 0])
        link = note(r"GPT-3, \ Gopher \ and Chinchilla in the lineage: \ Part 14").next_to(res, DOWN, buff=0.4).align_to(res, LEFT)
        cite_ = cite(r"J.~Hoffmann et al.\ (2022), \ Table 1 and abstract", corner=DR)
        with self.voiceover(
            "Kaplan's laws said: as the budget grows, put most of it into the model. GPT-3 read under two tokens per "
            "parameter, and DeepMind's Gopher, two hundred and eighty billion parameters, read three hundred billion "
            "tokens. <bookmark mark='a'/> Chinchilla used the same compute on a model a quarter the size, trained on "
            "four times the data. <bookmark mark='b'/> It beat Gopher on almost everything: on the MMLU exam, by more "
            "than seven points. And it was four times cheaper to run. So who was wrong, and why?"
        ) as vo:
            self.play(FadeIn(same), DrawBorderThenFill(gop), FadeIn(gl), FadeIn(ax_n), FadeIn(ax_d), FadeIn(cite_))
            vo.wait_until("a")
            self.play(TransformFromCopy(gop, chi), FadeIn(cl), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.4), FadeIn(link))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counting(self):
        ch = load("chinchilla")
        budgets = np.asarray(ch["budgets"], float)
        n_all, n_ne = np.asarray(ch["nopt2"], float), np.asarray(ch["nopt_kaplan"], float)
        a_all, a_ne = float(ch["a2"]), float(ch["a_kaplan_count"])
        share = np.asarray(ch["emb_share"], float)
        ok = np.isfinite(n_all) & np.isfinite(n_ne)
        lc = np.log10(budgets[ok])
        ly = np.log10(np.concatenate([n_all[ok], n_ne[ok]]))
        x0, x1 = lc.min() - 0.3, lc.max() + 0.3
        y0, y1 = math.floor(ly.min() * 2) / 2 - 0.2, math.ceil(ly.max() * 2) / 2 + 0.2
        ax = CornerAxes(x_range=[x0, x1, 1], y_range=[y0, y1, 0.5], x_length=5.8, y_length=4.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.4, -0.5, 0])
        xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, y0), DOWN, buff=0.08)
                      for v in range(math.ceil(x0), math.floor(x1) + 1)])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.08)
                      for v in range(math.ceil(y0), math.floor(y1) + 1)])
        xn = label(r"compute budget \ (operations)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"the best size, \ counted two ways", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)

        def line(n, col):
            b = np.polyfit(lc, np.log10(n[ok]), 1)
            xs = np.array([x0 + 0.1, x1 - 0.1])
            return VGroup(Line(ax.c2p(xs[0], np.polyval(b, xs[0])), ax.c2p(xs[1], np.polyval(b, xs[1])), color=col, stroke_width=3),
                          *[Dot(ax.c2p(a, math.log10(v)), radius=0.07, color=col) for a, v in zip(lc, n[ok])])

        l_all, l_ne = line(n_all, NCOL), line(n_ne, SP)
        lg = VGroup(label(rf"all the parameters: \ slope ${a_all:.2f}$", font_size=22, color=NCOL),
                    label(rf"leaving out the input and output layers: \ ${a_ne:.2f}$", font_size=22, color=SP))
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, 2.0, 0])
        sh = label(rf"the left-out share: \ ${100 * share[0]:.0f}\%$ of the smallest model, \ ${100 * share[-1]:.0f}\%$ of the "
                   r"largest", font_size=20, color=GREY_A).next_to(lg, DOWN, buff=0.25).align_to(lg, LEFT)
        cards = VGroup(
            history_card(2024, r"Pearce \& Song", r"Kaplan counted parameters without the embeddings, at small scale: "
                         r"that alone turns $0.5$ into nearly $0.73$", width=5.6, color=HIST),
            history_card(2024, r"Porian et al.", r"and three details: \ the last layer's cost, \ the warmup's length, \ "
                         r"and an optimizer setting ($\beta_2$) untuned at small batches", width=5.6, color=HIST))
        cards.arrange(DOWN, buff=0.15).move_to([3.4, -1.55, 0])
        bigger = a_ne > a_all + 0.03
        with self.voiceover(
            "Part of the answer is how you count. Kaplan counted parameters without the embeddings, and at small "
            "scale those are a large share of a model. <bookmark mark='a'/> Our own runs show the effect. The same "
            f"budgets, the same best models: counting all their parameters, the best size grows with slope "
            f"{a_all:.2f}. <bookmark mark='b'/> Counting only the hidden layers, "
            + (f"it grows with slope {a_ne:.2f}: the small models look smaller than they are, so the law looks "
               "steeper. In 2024 Tim Pearce and Jinyeop Song showed that counting this way, at Kaplan's small scale, "
               "turns Chinchilla's one half into something close to Kaplan's 0.73. " if bigger else
               f"the slope is {a_ne:.2f}: in our models the left-out share is too small to bend it much. In 2024 Tim "
               "Pearce and Jinyeop Song showed that at Kaplan's small scale, counting this way turns one half into "
               "something close to 0.73. ")
            + "<bookmark mark='c'/> The same year, Tomer Porian and colleagues found the rest: the cost of the last "
            "layer, the length of the warmup, and an optimizer setting left untuned at small batches. Fix all three, "
            "and Kaplan's own setup gives Chinchilla's answer."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(Create(l_all[0]), FadeIn(l_all[1:]), FadeIn(lg[0]))
            vo.wait_until("b")
            self.play(Create(l_ne[0]), FadeIn(l_ne[1:]), FadeIn(lg[1]), FadeIn(sh))
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replication(self):
        hd = label(r"Chinchilla's third method, \ refitted", font_size=36).to_edge(UP, buff=0.35)
        colors = {r"\alpha": NCOL, r"\beta": DCOL}
        pub = VGroup(label(r"published, \ 2022", font_size=26, color=SP),
                     MathTex(r"E = 1.69,\ A = 406.4,\ B = 410.7", font_size=30),
                     MathTex(r"\alpha = 0.34,\ \ \beta = 0.28", font_size=30),
                     MathTex(r"a = 0.46", font_size=30, color=SP),
                     label(r"about $70$ tokens per parameter \\ at the optimum", font_size=20, color=GREY_A))
        rep = VGroup(label(r"Besiroglu et al.\ (Epoch AI), \ 2024", font_size=26, color=C.TRUE_P),
                     MathTex(r"E = 1.82,\ A = 482,\ B = 2085", font_size=30),
                     MathTex(r"\alpha = 0.35,\ \ \beta = 0.37", font_size=30),
                     MathTex(r"a = 0.51 \pm 0.02", font_size=30, color=C.TRUE_P),
                     label(r"about $20$ tokens per parameter: \\ the same as methods 1 and 2", font_size=20, color=GREY_A))
        for g in (pub, rep):
            g.arrange(DOWN, buff=0.18)
        boxes = VGroup(*[SurroundingRectangle(g, buff=0.3, corner_radius=0.12, stroke_color=c, stroke_width=1.8)
                         for g, c in ((pub, SP), (rep, C.TRUE_P))])
        pair = VGroup(VGroup(boxes[0], pub), VGroup(boxes[1], rep)).arrange(RIGHT, buff=0.8).move_to(UP * 0.25)
        how = label(r"the data read back from the paper's Figure 4: \ $240$ runs, \ each point's colour decoded into a loss",
                    font_size=22, color=GREY_A).next_to(pair, DOWN, buff=0.35)
        ci = label(r"the published uncertainty, $0.454$ to $0.455$, \ would take over $600{,}000$ runs; \ they ran fewer "
                   r"than $500$", font_size=22, color=C.BITS).next_to(how, DOWN, buff=0.2)
        ours = load("chinchilla")
        lesson = label(rf"an exponent is a measurement, with an error bar: \ ours, ${float(ours['a3_lo']):.2f}$ to "
                       rf"${float(ours['a3_hi']):.2f}$", font_size=24, color=WHITE).to_edge(DOWN, buff=0.35)
        cite_ = cite(r"T.~Besiroglu, E.~Erdil, M.~Barnett \& J.~You, \textit{Chinchilla Scaling: A Replication Attempt} "
                     r"(2024)", corner=UR).shift(DOWN * 0.55)
        with self.voiceover(
            "Chinchilla itself was checked two years later. Its three methods had disagreed slightly: the fitted "
            "formula said 0.46, the other two about a half. <bookmark mark='a'/> In 2024, Tamay Besiroglu and "
            "colleagues at Epoch AI rebuilt the data from the paper's own figure, two hundred and forty runs, "
            "reading each point's loss from its colour, and refitted the formula. <bookmark mark='b'/> They got "
            "0.51, plus or minus 0.02: about twenty tokens per parameter, in agreement with the other two methods. "
            "The published fit had been off. <bookmark mark='c'/> And its stated uncertainty was implausibly "
            "small: an interval that narrow would take over six hundred thousand runs, and they had run fewer than "
            "five hundred. <bookmark mark='d'/> The lesson for us: an exponent is a measurement, and it has an "
            "error bar."
        ) as vo:
            self.play(FadeIn(hd), FadeIn(pair[0]))
            vo.wait_until("a")
            self.play(FadeIn(how), FadeIn(cite_))
            vo.wait_until("b")
            self.play(FadeIn(pair[1], shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(ci))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.wait(0.3)
        self.clear_scene()
