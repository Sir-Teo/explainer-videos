from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import HIST, MUP, PART, RICH, SP, load, table_card


class MuP(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.table()
        self.coord()

    def card(self):
        card = chapter_card(3, r"$\mu$P, derived", r"How should each layer scale, so that every layer keeps learning?",
                            part=PART)
        with self.voiceover("Chapter three. Mu-P, derived."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        head = label(r"one layer: \ $h = W x$, \ with $n$ inputs of size about $1$", font_size=30).to_edge(UP, buff=0.35)
        colors = {r"\sqrt{n}": SP, r"n": MUP, r"\eta": C.BITS}
        rows = [
            cmath(r"h_i", r"=", r"\textstyle\sum_{j=1}^{n} W_{ij}\, x_j", font_size=36),
            cmath(r"|h_i|", r"\approx", r"\sigma", r"\sqrt{n}", font_size=36, colors=colors),
            cmath(r"\Delta W", r"=", r"-\eta\; g\, x^{\top}", font_size=36, colors=colors),
            cmath(r"\Delta h_i", r"=", r"-\eta\; g_i\, (x \cdot x)", r"\approx", r"\eta", r"\, n", font_size=36, colors=colors),
            cmath(r"\Delta h = \Theta(1)", r"\Rightarrow", r"\eta \propto 1/n", r",\quad", r"\sigma \propto 1/\sqrt{n}",
                  font_size=36, colors=colors),
        ]
        whys = [why(r"$n$ terms, \ added"), why(r"random signs cancel: \ central limit theorem"),
                why(r"a layer's gradient is an outer product"),
                why(r"$x \cdot x$: \ $n$ terms of one sign, \ law of large numbers"),
                why(r"what we ask: \ every layer changes by about $1$")]
        step = ladder(self, rows, whys, keep=5, top=2.35, x=-2.2, buff=0.38, edge=6.9)
        moral = label(r"the update is \emph{aligned} with the input, \ the starting weights are not: \ they scale "
                      r"differently", font_size=24, color=MUP).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the whole idea, in one layer. Its output is a sum of n weights times n inputs. "
            "<bookmark mark='a'/> At the start the weights are random, so the n terms have random signs and mostly "
            "cancel: by the central limit theorem, the sum grows like the square root of n. Divide the starting "
            "weights by the square root of n, and the output stays the same size at any width. "
            "<bookmark mark='b'/> Training is different. The gradient of a layer is an outer product: the error "
            "signal times the input. <bookmark mark='c'/> So the step, applied to that input, gives a sum of n "
            "terms that all have the same sign: it grows like n, not its square root. "
            "<bookmark mark='d'/> If every layer should keep changing by about the same amount at any width, the "
            "learning rate must shrink like one over n. Greg Yang and Edward Hu worked this out for every layer of "
            "any network in 2021, and called it the maximal update parametrization: mu-P."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            self.play(FadeIn(moral))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        tab = table_card([
            [r"", r"input weights, \ biases", r"hidden weights", r"output weights"],
            [r"starting variance", r"$1/\mathrm{fan\_in}$", r"$1/\mathrm{fan\_in}$", r"$1/\mathrm{fan\_in}^{\,2}$"],
            [r"Adam learning rate", r"$\eta$", r"$\eta\,/\,\mathrm{fan\_in}$", r"$\eta\,/\,\mathrm{fan\_in}$"],
            [r"the usual way (SP)", r"$1/\mathrm{fan\_in}$, \ $\eta$", r"$1/\mathrm{fan\_in}$, \ $\eta$",
             r"$1/\mathrm{fan\_in}$, \ $\eta$"],
        ], col_colors=[GREY_A, MUP, MUP, MUP], font_size=24)
        tab[0][3].set_color(SP)
        tab.move_to(UP * 0.9)
        head = label(r"$\mu$P for Adam", font_size=40, color=MUP).to_edge(UP, buff=0.35)
        ours = label(r"in our code: \ the output multiplied by $64/n$ and started at zero, \ and the $n \times n$ "
                     r"hidden matrix's rate times $64/n$: \\ the same thing, \ written so a width-$64$ model is "
                     r"identical in both", font_size=22, color=GREY_A).next_to(tab, DOWN, buff=0.45)
        why_ = VGroup(label(r"Adam: \ every entry moves by about $\eta$ \ $\Rightarrow$ \ $\Delta W x \sim \eta\, n$",
                            font_size=24, color=C.BITS),
                      label(r"the output layer: \ $n$ aligned inputs too, \ and it must start small", font_size=24,
                            color=C.BITS)).arrange(DOWN, buff=0.15).next_to(ours, DOWN, buff=0.35)
        cite_ = cite(r"G.~Yang \& E.~Hu (2021); \ G.~Yang et al., \textit{Tensor Programs V} (2022), Table 3", corner=DR)
        with self.voiceover(
            "For Adam, the optimizer every language model uses, the recipe is a short table. "
            "<bookmark mark='a'/> Inputs and biases learn at the base rate. Hidden matrices learn at the base rate "
            "divided by their width, because Adam moves every entry by about the learning rate, so the n aligned "
            "terms add up to n times it. The output layer starts much smaller, with variance one over the width "
            "squared, and learns at the rate over the width. <bookmark mark='b'/> The usual way, which we'll call "
            "SP, uses one rate everywhere. <bookmark mark='c'/> Our code writes the same rules slightly differently, "
            "so that a model of width sixty-four is the same in both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(tab[0][0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(FadeIn(tab[0][1]), FadeIn(tab[0][2]), FadeIn(why_))
            vo.wait_until("b")
            self.play(FadeIn(tab[0][3]))
            vo.wait_until("c")
            self.play(FadeIn(ours))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def coord(self):
        z = load("coord")
        W = np.asarray(z["widths"], float)
        sp, mu = np.asarray(z["sp"]), np.asarray(z["mup"])  # widths x steps x layers
        lw = np.log10(W)
        allv = np.log10(np.concatenate([sp.ravel(), mu.ravel()]))
        allv = allv[np.isfinite(allv)]
        y0, y1 = math.floor(allv.min()), math.ceil(allv.max())
        layer_cols = [GREY_B, C.CONTEXT, C.BITS]
        layer_names = [r"first hidden layer", r"second hidden layer", r"output scores"]
        pans = VGroup()
        for k, (M, ttl, col) in enumerate(((sp, r"the usual way (SP)", SP), (mu, r"$\mu$P", MUP))):
            ax = CornerAxes(x_range=[lw.min() - 0.1, lw.max() + 0.1, 1], y_range=[y0, y1, 1], x_length=5.0, y_length=3.6,
                            tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
            ax.move_to([-3.4 + 6.8 * k, -0.7, 0])
            xt = VGroup(*[MathTex(f"{int(w):,}".replace(",", "{,}"), font_size=18, color=GREY_B)
                          .next_to(ax.c2p(math.log10(w), y0), DOWN, buff=0.08) for w in W[::2]])
            yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=18, color=GREY_B).next_to(ax.c2p(lw.min() - 0.1, v), LEFT, buff=0.08)
                          for v in range(y0, y1 + 1)])
            lines = VGroup()
            for t in range(M.shape[1]):
                for j in range(3):
                    op = 0.35 + 0.65 * t / (M.shape[1] - 1)
                    lines.add(curve(ax, lw, np.log10(M[:, t, j]), layer_cols[j], 2.5).set_stroke(opacity=op))
            t_ = label(ttl, font_size=30, color=col).next_to(ax, UP, buff=0.15)
            xl = label(r"width", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
            pans.add(VGroup(ax, xt, yt, t_, xl, lines))
        key = VGroup(*[label(n_, font_size=20, color=c) for n_, c in zip(layer_names, layer_cols)]).arrange(RIGHT, buff=0.5)
        key.to_edge(UP, buff=0.3)
        yl = label(r"how much each layer's activations changed, \ steps $1$ to $4$ (fainter: earlier)", font_size=20,
                   color=GREY_A).next_to(key, DOWN, buff=0.12)
        s_sp, s_mu = float(z["slope_sp"]), float(z["slope_mup"])
        grows = s_sp > 0.2
        flat = abs(s_mu) < 0.15
        tag = note(r"computed: \ Adam, learning rate $0.01$, \ the same four batches at every width").to_corner(DL, buff=0.2)
        said1 = (
            f"the change in the output scores grows with the width, about as the width to the power {s_sp:.2f}: "
            "a learning rate that is right for a small model is too big for a large one, and eventually blows it "
            "up. " if grows else
            f"the output scores' change barely grows with width here, a power of {s_sp:.2f}. "
        )
        said2 = (
            f"the lines are flat, a power of {s_mu:.2f}: every layer changes by the same amount at every width, "
            "which is what the derivation asked for." if flat else
            f"the change grows as the width to the {s_mu:.2f}, much less than the usual way."
        )
        with self.voiceover(
            "Yang's test for whether a parametrization is right is called a coordinate check: train for a few steps "
            "at many widths, with one learning rate, and measure how much each layer's activations change. "
            "<bookmark mark='a'/> In the usual parametrization, "
            + said1
            + "<bookmark mark='b'/> In mu-P, "
            + said2
        ) as vo:
            self.play(FadeIn(key), FadeIn(yl), FadeIn(tag), *[FadeIn(p[:5]) for p in pans])
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in pans[0][5]], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in pans[1][5]], lag_ratio=0.05), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
