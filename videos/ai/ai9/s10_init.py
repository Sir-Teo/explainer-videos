from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import BWD, NEURON, PART, WEIGHT, load

SMALL, HE, BIG = "#7FD3FF", C.BITS, C.SURPRISE
RIDGE_A, RIDGE_B = "#3FB8AF", "#F28C5B"  # first layer, last layer


def spoken(v: float) -> str:
    """A large factor, as it would be said: 'thirty million', 'two billion'."""
    if v >= 1e9:
        return f"{round(v / 1e9)} billion"
    if v >= 1e6:
        return f"{round(v / 1e6, -1 if v >= 1e7 else 0):.0f} million"
    return f"{v:,.0f}"


class Init(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.layers()
        self.glorot()
        self.he()
        self.ridge()

    def card(self):
        card = chapter_card(9, r"Initialization, derived", r"How big should the starting weights be?", lit=(2010, 2015),
                            part=PART)
        with self.voiceover("Chapter nine. Initialization, derived."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def layers(self):
        g = load("signal")
        L = int(g["L"])
        lo, hi = -9, 9
        ax = Axes(x_range=[0, L, 10], y_range=[0, hi - lo, 3], x_length=7.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.0, -0.5, 0])
        yl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v - lo), LEFT, buff=0.1)
                      for v in range(lo, hi + 1, 3)])
        xl = label(r"layer", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"typical size of the signal", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        ls = np.arange(1, L + 1)

        def line(key, col, sw=4):
            v = np.clip(np.log10(np.maximum(np.asarray(g[key]), 1e-30)), lo, hi) - lo
            return curve(ax, ls, v, col, sw)

        c_small, c_he, c_big = line("sd_small", SMALL), line("sd_he", HE), line("sd_big", BIG)

        def ride(key, col):
            """A pulse travelling through the layers along the curve, as big as the signal it carries."""
            vals = np.asarray(g[key])
            pulse = glow_dot(ax.c2p(1, np.clip(np.log10(vals[0]), lo, hi) - lo), color=col, radius=0.1)

            def upd(m, alpha):
                k = alpha * (L - 1)
                v = float(vals[min(int(k), L - 1)])
                r = float(np.clip(0.1 * v ** 0.12, 0.012, 0.55))
                m.become(glow_dot(ax.c2p(k + 1, float(np.clip(np.log10(max(v, 1e-30)), lo, hi)) - lo), color=col, radius=r))

            return Succession(UpdateFromAlphaFunc(pulse, upd), FadeOut(pulse, run_time=0.01))
        names = VGroup(label(r"weights $0.7\times$ too small: \ vanishes", font_size=24, color=SMALL),
                       label(r"weights just right", font_size=24, color=HE),
                       label(r"weights $1.4\times$ too big: \ explodes", font_size=24, color=BIG))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.4, 0.6, 0])
        grad = label(r"gradients flowing back do the same, \\ so the first layers can't learn", font_size=24,
                     color=GREY_A).next_to(names, DOWN, buff=0.5).align_to(names, LEFT)
        head = label(r"$50$ layers of $256$ ReLU units, \ random weights", font_size=30).to_edge(UP, buff=0.35)
        bells = VGroup()
        for k, (f, col) in enumerate(((0.7, SMALL), (1.0, HE), (1.4, BIG))):
            x0 = 3.0 + 1.35 * k
            base = Line([x0 - 0.6, 1.55, 0], [x0 + 0.6, 1.55, 0], color=GREY_C, stroke_width=1.5)
            bell = FunctionGraph(lambda t, f=f: 0.5 / f * np.exp(-0.5 * (t / (0.22 * f)) ** 2), x_range=[-0.6, 0.6],
                                 color=col, stroke_width=3).shift([x0, 1.55, 0])
            bells.add(VGroup(base, bell))
        bells = VGroup(bells[0], bells[2], bells[1])  # in the order the narration shows them
        grey_bells = VGroup(*[b_.copy().set_color(GREY_D) for b_ in bells])
        spread = label(r"the spread of the random starting weights", font_size=22, color=GREY_A)
        spread.next_to(VGroup(*bells), UP, buff=0.2)
        shrink = float(g["sd_small"][0] / g["sd_small"][-1])
        grow = float(g["sd_big"][-1])
        tag = note(r"computed").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Before training, the weights are random. But random how? What matters is their spread: how far the "
            "random starting weights stray from zero. Send a signal through fifty layers and track "
            "its size. <bookmark mark='a'/> Draw the weights a little too small, and each layer shrinks the signal "
            f"by a fixed factor. After fifty layers, it's about {spoken(shrink)} times smaller: gone. "
            f"<bookmark mark='b'/> A little too big, and it explodes, to about {spoken(grow)}. <bookmark mark='c'/> "
            "Only one size keeps it steady, layer after layer. And gradients, flowing backwards, vanish or explode "
            "the same way."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn), FadeIn(spread), FadeIn(tag),
                      Create(grey_bells))
            vo.wait_until("a")
            self.play(Create(c_small), ride("sd_small", SMALL), FadeIn(names[0]), Create(bells[0]), run_time=3.0,
                      rate_func=linear)
            vo.wait_until("b")
            self.play(Create(c_big), ride("sd_big", BIG), FadeIn(names[2]), Create(bells[1]), run_time=3.0,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(Create(c_he), ride("sd_he", HE), FadeIn(names[1]), Create(bells[2]), run_time=3.0,
                      rate_func=linear)
            self.play(FadeIn(grad))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def glorot(self):
        colors = {r"\operatorname{Var}(W)": WEIGHT, r"n_{\text{in}}": NEURON, r"n_{\text{out}}": BWD}
        rows = [
            cmath(r"z_i", r"=", r"\textstyle\sum_{j=1}^{n_{\text{in}}} W_{ij}\, a_j", font_size=34, colors=colors),
            cmath(r"\operatorname{Var}(z)", r"=", r"n_{\text{in}}", r"\,", r"\operatorname{Var}(W)", r"\,\mathbb{E}[a^2]",
                  font_size=34, colors=colors),
            cmath(r"\operatorname{Var}(W)", r"=", r"1 / ", r"n_{\text{in}}", font_size=34, colors=colors),
            cmath(r"\operatorname{Var}(W)", r"=", r"1 / ", r"n_{\text{out}}", font_size=34, colors=colors),
            cmath(r"\operatorname{Var}(W)", r"=", r"2 / (", r"n_{\text{in}}", r"+", r"n_{\text{out}}", r")",
                  font_size=34, colors=colors),
        ]
        whys = [why(r"a unit adds up its $n_{\text{in}}$ inputs"),
                why(r"independent terms, \ weights of mean $0$"),
                why(r"tanh near $0$: \ $\mathbb{E}[a^2] \approx \operatorname{Var}(z)$; \ keep it the same"),
                why(r"backwards: \ the same sum, \ through $W^{\top}$"),
                why(r"a compromise between the two")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-1.6, buff=0.42, edge=6.9)
        # one unit, its n_in inputs and the n_out units it feeds
        uin = VGroup(*[Dot([-3.6, -1.0 - 0.45 * k, 0], radius=0.09, color=NEURON) for k in range(5)])
        uout = VGroup(*[Dot([3.6, -1.2 - 0.5 * k, 0], radius=0.09, color=BWD) for k in range(4)])
        unit = Circle(radius=0.32, color=WEIGHT, stroke_width=3).move_to([0, -1.9, 0])
        fan_in = VGroup(*[Arrow(d_.get_center(), unit.get_center(), buff=0.34, color=NEURON, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.06) for d_ in uin])
        fan_out = VGroup(*[Arrow(d_.get_center(), unit.get_center(), buff=0.34, color=BWD, stroke_width=2.5,
                                 max_tip_length_to_length_ratio=0.06) for d_ in uout])
        out_lines = VGroup(*[Line(unit.get_center(), d_.get_center(), buff=0.34, color=GREY_D, stroke_width=2)
                             for d_ in uout])
        lin = label(r"$n_{\text{in}}$ inputs", font_size=28, color=NEURON).next_to(uin, LEFT, buff=0.3)
        lout = label(r"$n_{\text{out}}$ units it feeds", font_size=28, color=BWD).next_to(uout, RIGHT, buff=0.3)
        lout.shift(LEFT * max(0.0, lout.get_right()[0] - 6.9))
        fwd_l = label(r"forward: \ the signal", font_size=24, color=NEURON).next_to(unit, UP, buff=0.15)
        bwd_l = label(r"backward: \ the gradient", font_size=24, color=BWD).next_to(unit, DOWN, buff=0.15)
        diagram = VGroup(uin, unit, out_lines, lin)
        cite_ = cite(r"X.~Glorot \& Y.~Bengio, \textit{Understanding the difficulty of training deep feedforward "
                     r"neural networks} (2010); \ Y.~LeCun et al., \textit{Efficient BackProp} (1998)", corner=DL)
        box = None
        with self.voiceover(
            "The right size follows from one line of probability. <bookmark mark='a'/> A unit adds up its n inputs, "
            "each times a weight. <bookmark mark='b'/> If the weights are independent with mean zero, the variances "
            "of the terms add: the sum's variance is n times the weights' variance times the inputs' typical square. "
            "<bookmark mark='c'/> For tanh units near zero, the output is about the input, so to keep the variance "
            "the same from layer to layer, the weights' variance should be one over n in. <bookmark mark='d'/> Going "
            "backwards, the gradient is summed over the units it feeds, through the transposed matrix: that asks for "
            "one over n out. <bookmark mark='e'/> Xavier Glorot and Yoshua Bengio, in 2010, took the compromise: two "
            "over the sum. Yann LeCun had recommended one over n in, for the forward pass, back in 1998."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(diagram), FadeIn(uout), FadeIn(lout))
            vo.wait_until("a")
            step(0)
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in fan_in], lag_ratio=0.1), FadeIn(fwd_l))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in fan_out], lag_ratio=0.1), FadeIn(bwd_l))
            vo.wait_until("e")
            step(4)
            box = SurroundingRectangle(rows[4], color=WEIGHT, buff=0.12, corner_radius=0.08)
            self.play(Create(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def he(self):
        g = load("signal")
        colors = {r"\tfrac{2}{n}": HE, r"\tfrac{1}{n}": NEURON}
        f1 = cmath(r"\operatorname{Var}(w)", "=", r"\tfrac{1}{n}", colors=colors, font_size=46)
        f2 = cmath(r"\operatorname{Var}(w)", "=", r"\tfrac{2}{n}", colors=colors, font_size=46)
        for f in (f1, f2):
            f.move_to([3.6, 2.4, 0])
        half = cmath(r"\mathbb{E}\big[\max(0, z)^2\big]", r"=", r"\tfrac12 \operatorname{Var}(z)", font_size=34)
        half.move_to([3.6, 1.2, 0])
        hw = label(r"$z$ symmetric about $0$: \ the ReLU keeps \\ exactly half of $\mathbb{E}[z^2]$", font_size=22,
                   color=GREY_A).next_to(half, DOWN, buff=0.2)
        h = np.asarray(g["hist_he"])[24].astype(float)
        h = h / h.max()
        edges = np.linspace(-4, 4, len(h) + 1)
        bw = 5.6 / len(h)
        bars = VGroup(*[Rectangle(width=bw * 0.92, height=max(2.6 * v, 0.01), stroke_width=0, fill_color=HE,
                                  fill_opacity=0.85).move_to([-3.4 + (edges[i] + edges[i + 1]) / 2 * 0.7, -1.6 + 1.3 * v, 0])
                        for i, v in enumerate(h)])
        base = Line([-6.3, -1.6, 0], [-0.5, -1.6, 0], color=GREY_C, stroke_width=2)
        zero = DashedLine([-3.4, -1.65, 0], [-3.4, 1.2, 0], color=GREY_B, stroke_width=2)
        hl = label(r"what a unit receives, before the ReLU \\ (layer $25$ of the steady network, \ computed)",
                   font_size=22, color=GREY_A).next_to(base, DOWN, buff=0.15)
        neg = VGroup(*[b for b, e in zip(bars, edges[1:]) if e <= 0])
        why2 = label(r"only half the variance survives each layer, \\ so double the weights' variance", font_size=26,
                     color=HE).move_to([3.6, -1.0, 0])
        cites = label(r"K.~He, X.~Zhang, S.~Ren \& J.~Sun, \textit{Delving Deep into Rectifiers} (2015): \ $2/n$", font_size=22,
                      color=GREY_B).move_to([3.0, -2.9, 0])
        with self.voiceover(
            "A ReLU changes the bookkeeping. <bookmark mark='a'/> Here is what the units of a middle layer receive, "
            "before the bend, in the steady network: a symmetric bell. <bookmark mark='b'/> The ReLU throws away the "
            "negative half, so the mean square of its output is exactly half the variance of its input. "
            "<bookmark mark='c'/> To make up for it, double the weights' variance: two over n. That's He "
            "initialization, from Kaiming He and colleagues in 2015, and it's the steady line of a minute ago."
        ) as vo:
            self.play(Write(f1))
            vo.wait_until("a")
            self.play(Create(base), FadeIn(hl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03),
                      run_time=1.6)
            vo.wait_until("b")
            self.play(Create(zero), neg.animate.set_fill(GREY_D, opacity=0.5), Write(half), FadeIn(hw), run_time=1.4)
            vo.wait_until("c")
            morph(self, f1, f2)
            self.play(FadeIn(why2), FadeIn(cites))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ridge(self):
        r = load("ridge")
        L = int(r["L"])
        ax = ThreeDAxes(x_range=[-1, 1, 0.5], y_range=[0, L, 10], z_range=[0, 1, 0.5], x_length=6.0, y_length=7.0,
                        z_length=2.2, axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ax.shift(DOWN * 0.3)
        layers = list(range(0, L, 2))

        def ridges(key):
            H = np.asarray(r[f"hist_{key}"])
            nb = H.shape[1]
            xs = np.linspace(-1, 1, nb + 1)
            xc = (xs[1:] + xs[:-1]) / 2
            out = VGroup()
            for l in layers[::-1]:  # back to front
                p = H[l] / max(H[l].max(), 1e-12)
                pts = [ax.c2p(-1, l + 1, 0)] + [ax.c2p(x, l + 1, z) for x, z in zip(xc, p)] + [ax.c2p(1, l + 1, 0)]
                col = interpolate_color(ManimColor(RIDGE_A), ManimColor(RIDGE_B), l / (L - 1))
                out.add(Polygon(*pts, stroke_color=WHITE, stroke_width=1.0, fill_color=col, fill_opacity=0.55))
            return out

        cases = [("tanh_std", r"weights $U[-1/\sqrt{n},\, 1/\sqrt{n}]$: \ variance $\tfrac{1}{3n}$", SMALL),
                 ("tanh_xavier", r"Glorot: \ variance $\tfrac1n$", HE),
                 ("tanh_big", r"variance $\tfrac4n$", BIG)]
        rid = [ridges(k) for k, _, _ in cases]
        head = label(r"$50$ tanh layers: \ each ridge is one layer's outputs, \ front to back", font_size=28)
        head.to_edge(UP, buff=0.3)
        caps = [label(t, font_size=28, color=c).to_corner(UL, buff=0.35).shift(DOWN * 0.6) for _, t, c in cases]
        xlab = VGroup(label(r"output $-1$", font_size=22, color=GREY_B), label(r"$+1$", font_size=22, color=GREY_B))
        scale_note = note(r"computed; \ each layer's histogram scaled to the same height").to_corner(UR, buff=0.2)
        scale_note.shift(DOWN * 0.6)
        first = label(r"layer $1$ \ (front)", font_size=22, color=RIDGE_A)
        last = label(r"layer $50$ \ (back)", font_size=22, color=RIDGE_B)
        for m in (head, *caps, scale_note):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        sd = {k: np.asarray(r[f"sd_{k}"]) for k, _, _ in cases}
        e_std = int(-math.floor(math.log10(max(sd["tanh_std"][-1], 1e-300))))
        gs = {k: np.asarray(r[f"gsd_{k}"]) for k, _, _ in cases}
        with self.voiceover(
            "Here is the inside of a fifty-layer tanh network, as a landscape. Each ridge is the histogram of one "
            "layer's outputs, from the first layer at the front to the fiftieth at the back. <bookmark mark='a'/> "
            "With the old rule of thumb, weights uniform between plus and minus one over root n, the outputs shrink "
            f"layer after layer, from a typical size of {sd['tanh_std'][0]:.2f} to about ten to the minus {e_std}: the "
            "ridges collapse into a spike at zero. <bookmark mark='b'/> With Glorot and Bengio's variance, one over "
            f"n, they stay spread out, narrowing slowly, to {sd['tanh_xavier'][-1]:.2f} by the last layer. "
            "<bookmark mark='c'/> Make the weights too big, and the units saturate: the outputs pile up at minus one "
            "and plus one. Yet the gradient doesn't die: the gradient arriving at the first layer is "
            f"{gs['tanh_big'][0] / gs['tanh_big'][-1]:,.0f} times the size of the one at the top. It explodes, and the "
            "next chapter explains why."
        ) as vo:
            self.set_camera_orientation(phi=62 * DEGREES, theta=-58 * DEGREES, zoom=0.95)
            xlab[0].move_to(ax.c2p(-1, -4, 0))
            xlab[1].move_to(ax.c2p(1, -4, 0))
            first.move_to(ax.c2p(1.45, 1, 0))
            last.move_to(ax.c2p(1.45, L, 0))
            for m in (*xlab, first, last):
                m.rotate(PI / 2, axis=RIGHT)
            self.play(FadeIn(head), FadeIn(scale_note), Create(ax.get_x_axis()), Create(ax.get_y_axis()),
                      FadeIn(xlab), FadeIn(first), FadeIn(last))
            self.play(LaggedStart(*[FadeIn(p_) for p_ in rid[0][::-1]], lag_ratio=0.06), run_time=2.5)
            self.begin_ambient_camera_rotation(rate=0.012)
            vo.wait_until("a")
            self.play(FadeIn(caps[0]))
            vo.wait_until("b")
            self.play(FadeOut(caps[0]), FadeIn(caps[1]), Transform(rid[0], rid[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeOut(caps[1]), FadeIn(caps[2]), Transform(rid[0], rid[2]), run_time=2.0)
            self.stop_ambient_camera_rotation()
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
