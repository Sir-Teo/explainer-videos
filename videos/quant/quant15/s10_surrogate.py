from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, illustration, load


class Surrogate(VoiceoverScene):
    def construct(self):
        s = load("surrogate")
        self.card()
        self.net(s)

    def card(self):
        c = chapter_card(9, r"A neural pricer for the book", r"How do you reprice ten thousand notes every second?",
                         part=PART)
        with self.voiceover("Chapter nine. A neural pricer for the book."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def net(self, s):
        mc = np.asarray(s["test_mc"])
        nn = np.asarray(s["test_net"])
        g = axes([0.55, 1.25], [0.55, 1.25], x_length=4.6, y_length=4.6, xlabel=r"Monte Carlo, 40{,}000 paths",
                 ylabel=r"the network", xticks=[0.6, 0.8, 1.0, 1.2], yticks=[0.6, 0.8, 1.0, 1.2], font_size=15)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        diag = DashedLine(ax.c2p(0.55, 0.55), ax.c2p(1.25, 1.25), stroke_color=GREY_C, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(np.clip(a, 0.55, 1.25), np.clip(b, 0.55, 1.25)), radius=0.045, color=OPT)
                        for a, b in zip(mc, nn)])
        speed = s["t_mc"] / s["t_net"]
        side = VGroup(
            wrapped_label(rf"a small network (three inputs: the index against the start, the months elapsed, whether "
                          rf"knocked in) trained on {s['n_train']:,} Monte Carlo prices of {s['train_paths']:,} paths "
                          r"each".replace(",", "{,}"), 4.6, 19, GREY_A),
            MathTex(rf"\text{{error}}\ {s['rmse']:.3f}\ \text{{per 1 of notional}}", font_size=30, color=OPT),
            MathTex(rf"{s['t_mc']:.1f}\ \text{{s}} \to {1e6 * s['t_net']:.1f}\ \mu\text{{s per price}}", font_size=30, color=GOOD),
            wrapped_label(rf"about {speed / 1e6:.0f} million times faster, with an error close to the Monte Carlo noise of "
                          r"its own training data. The largest errors sit at the knock-in cliff, where the price jumps; "
                          r"a desk checks the network against fresh simulation every night", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        src = illustration(rf"{len(mc)} random test notes, never seen in training; CPU, one thread")
        with self.voiceover(
            "A desk with thousands of snowballs must reprice and re-hedge all of them through the day, and one "
            f"Monte Carlo price takes about {s['t_mc']:.0f} seconds. So train a network to do it. Three inputs, the "
            "index against the note's start, the months elapsed, and whether it has knocked in; one output, the "
            f"price. It learns from {s['n_train']:,} noisy Monte Carlo prices. <bookmark mark='a'/> On a hundred and "
            "fifty notes it never saw, priced by Monte Carlo with forty thousand paths, it agrees to "
            f"{s['rmse']:.3f} per unit of notional. <bookmark mark='b'/> And it answers in about "
            f"{1e6 * s['t_net']:.1f} microseconds: millions of times faster. This is what Part seventeen does at "
            "scale, and what made chapter five's daily hedge possible."
        ) as vo:
            self.play(FadeIn(side[0]), FadeIn(g), Create(diag), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.01, run_time=2), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
