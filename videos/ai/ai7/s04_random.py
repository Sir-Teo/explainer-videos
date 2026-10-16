from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import AUSTEN, DICKENS, TEST, TRAIN, curve, load


class RandomLabels(VoiceoverScene):
    def construct(self):
        self.card()
        self.experiment()

    def card(self):
        card = chapter_card(3, r"Memorizing nonsense", r"Can a network fit random labels?", part=7)
        with self.voiceover("Chapter three. Memorizing nonsense."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def experiment(self):
        r = load("random")
        T, S = np.asarray(r["true"]), np.asarray(r["shuffled"])
        n, n_params = int(r["n"]), int(r["n_params"])
        # the labels, as a strip of coloured pages, then shuffled
        from videos.ai.ai5 import compute as c5

        pg = c5.load("pages")
        y = np.asarray(pg["y"])[~np.asarray(pg["test"], bool)]
        g = np.random.default_rng(2017)
        perm = g.permutation(len(y))
        cols = 32
        cells = VGroup(*[Square(0.13, stroke_width=0, fill_color=AUSTEN if v == 0 else DICKENS, fill_opacity=0.9)
                         for v in y])
        cells.arrange_in_grid(cols=cols, buff=0.025).move_to([0, 2.25, 0])
        cl = label(rf"the ${n}$ training pages, \\ coloured by author", font_size=24, color=GREY_A).next_to(cells, LEFT, buff=0.4)
        net = label(rf"one network: \ $70 \to 512 \to 512 \to 2$, \ ${n_params:,}$ weights".replace(",", "{,}"),
                    font_size=26, color=WHITE).next_to(cells, DOWN, buff=0.3)
        panels = VGroup()
        for k, (D, title) in enumerate(((T, r"true authors"), (S, r"shuffled authors"))):
            ax = Axes(x_range=[0, 3.2, 1], y_range=[0.4, 1.0, 0.1], x_length=5.4, y_length=2.3, tips=False,
                      axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
            ax.move_to([-3.4 + 6.8 * k, -1.55, 0])
            lx = np.log10(D[:, 0])
            ctr, cte = curve(ax, lx, D[:, 1], TRAIN, 3), curve(ax, lx, D[:, 2], TEST, 4)
            yl = VGroup(*[MathTex(rf"{int(round(100 * v))}\%", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                          for v in (0.5, 0.75, 1.0)])
            xl = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(v, 0.4), DOWN, buff=0.08)
                          for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3))])
            t = label(title, font_size=28, color=WHITE).next_to(ax, UP, buff=0.15)
            yl_ = D[-1, 2] - 0.13 if D[-1, 2] > 0.8 else D[-1, 2] + 0.1
            end = label(rf"new pages: \ ${100 * D[-1, 2]:.0f}\%$", font_size=26, color=TEST).move_to(ax.c2p(2.5, yl_))
            panels.add(VGroup(ax, yl, xl, t, ctr, cte, end))
        key = VGroup(label(r"training pages right", font_size=22, color=TRAIN),
                     label(r"new pages right", font_size=22, color=TEST)).arrange(RIGHT, buff=0.5)
        key.next_to(panels, DOWN, buff=0.2)
        key.add(label(r"(training steps on a log scale)", font_size=20, color=GREY_B)).arrange(RIGHT, buff=0.5)
        key.next_to(panels, DOWN, buff=0.2)
        cite_ = cite(r"C.~Zhang, S.~Bengio, M.~Hardt, B.~Recht \& O.~Vinyals, \textit{Understanding Deep Learning Requires "
                     r"Rethinking Generalization} (2017)", corner=UR)
        with self.voiceover(
            "In 2016, Chiyuan Zhang and colleagues ran an experiment that broke the classical picture. Take a "
            f"network, here with about {round(n_params, -3) // 1000} thousand weights, and train it on the "
            f"{n} training pages with their true authors. <bookmark mark='a'/> It fits all of them, and gets "
            f"{100 * T[-1, 2]:.1f} percent of new pages right. <bookmark mark='b'/> Now shuffle the authors, so "
            "every label is random. Same network, same training."
        ) as vo:
            self.play(FadeIn(cl), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.002), FadeIn(net), FadeIn(cite_),
                      run_time=1.8)
            self.play(*[FadeIn(m) for m in panels[0][:4]], FadeIn(key))
            vo.wait_until("a")
            self.play(Create(panels[0][4]), Create(panels[0][5]), run_time=2.0)
            self.play(FadeIn(panels[0][6]))
            vo.wait_until("b")
            self.play(*[c.animate.set_fill(AUSTEN if y[perm[i]] == 0 else DICKENS) for i, c in enumerate(cells)],
                      run_time=1.5)
        with self.voiceover(
            "It fits these too, every one of them, only a little more slowly. It has memorized nonsense. "
            "<bookmark mark='a'/> And on new pages, it's at chance, as it must be. <bookmark mark='b'/> So the same "
            "network can memorize anything at all. Then counting what a model could fit can't explain why, given "
            "real labels, it finds a rule that works on new pages instead. Something in how it's trained prefers "
            "simple answers. Why, exactly, is still being worked out."
        ) as vo:
            self.play(*[FadeIn(m) for m in panels[1][:4]])
            self.play(Create(panels[1][4]), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(panels[1][5]), run_time=1.5)
            self.play(FadeIn(panels[1][6]))
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()
