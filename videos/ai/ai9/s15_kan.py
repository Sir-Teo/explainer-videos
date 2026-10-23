from __future__ import annotations


import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import HIST, KANC, NEURON, PART, WEIGHT, load, log_axes


def mini_plot(xs, ys, width=0.9, height=0.55, color=KANC, lo=None, hi=None) -> VGroup:
    """A tiny graph of one learned edge function, in a box."""
    ys = np.asarray(ys, float)
    lo = ys.min() if lo is None else lo
    hi = ys.max() if hi is None else hi
    span = max(hi - lo, 1e-9)
    box = RoundedRectangle(width=width, height=height, corner_radius=0.06, stroke_color=GREY_D, stroke_width=1,
                           fill_color="#121722", fill_opacity=1)
    pts = [box.get_corner(DL) + np.array([0.06 + (width - 0.12) * (x - xs[0]) / (xs[-1] - xs[0]),
                                           0.06 + (height - 0.12) * (y - lo) / span, 0]) for x, y in zip(xs, ys)]
    return VGroup(box, VMobject(color=color, stroke_width=2.2).set_points_as_corners(pts))


class KAN(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.kan()
        self.replay()
        self.debate()

    def card(self):
        card = chapter_card(14, r"Kolmogorov--Arnold networks", r"What if the edges learned whole functions?", part=PART)
        with self.voiceover("Chapter fourteen. Kolmogorov–Arnold networks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def theorem(self):
        h13 = history_card(1900, r"David Hilbert's thirteenth problem", r"can the roots of a degree-$7$ equation be "
                           r"written using only functions of two variables?", width=6.0, color=HIST).move_to([-3.5, 2.3, 0])
        ka = history_card(1957, r"Andrey Kolmogorov, \ and his student Vladimir Arnold, \ aged $19$",
                          r"yes, \ and far more: \ every continuous function of $n$ variables is built from functions "
                          r"of one variable, \ and addition", width=6.0, color=HIST).move_to([3.5, 2.3, 0])
        colors = {r"\Phi_q": KANC, r"\varphi_{q,p}": NEURON}
        th = cmath(r"f(x_1, \dots, x_n)", r"=", r"\sum_{q=0}^{2n}", r"\Phi_q", r"\Big(\sum_{p=1}^{n}",
                   r"\varphi_{q,p}", r"(x_p)\Big)", font_size=40, colors=colors).move_to([0, 0.05, 0])
        # the picture for n = 2: two inputs, five inner sums, one outer sum
        ins = VGroup(*[Circle(radius=0.18, color=GREY_B, stroke_width=2.5).move_to([-3.6, -1.6 - 1.0 * k, 0]) for k in range(2)])
        mids = VGroup(*[Circle(radius=0.15, color=NEURON, stroke_width=2.5).move_to([-0.6, -1.0 - 0.5 * q, 0]) for q in range(5)])
        out = Circle(radius=0.2, color=KANC, stroke_width=3).move_to([2.4, -2.0, 0])
        e1 = VGroup(*[Line(a.get_right(), b.get_left(), color=NEURON, stroke_width=1.8) for a in ins for b in mids])
        e2 = VGroup(*[Line(b.get_right(), out.get_left(), color=KANC, stroke_width=1.8) for b in mids])
        pic_l = label(r"$n = 2$: \ $2 \times 5$ inner functions, \ $5$ outer", font_size=22, color=GREY_A)
        pic_l.next_to(out, RIGHT, buff=0.4)
        irr = VGroup(label(r"1989, \ Girosi \& Poggio: \ ``irrelevant''", font_size=22, color=C.SURPRISE),
                     label(r"the inner functions can be wild, \\ nothing a network could learn", font_size=20, color=GREY_A),
                     label(r"1991, \ K{\r u}rkov\'a: \ ``relevant''", font_size=22, color=KANC),
                     label(r"smooth approximate versions \\ come with error bounds", font_size=20, color=GREY_A))
        irr.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, -2.0, 0])
        with self.voiceover(
            "There's another way to build any function, and it's older than the perceptron. <bookmark mark='a'/> In "
            "1900 David Hilbert asked, as the thirteenth of his famous problems, whether the solutions of a "
            "seventh-degree equation could be written using only functions of two variables. <bookmark mark='b'/> In "
            "1957 Andrey Kolmogorov and his nineteen-year-old student Vladimir Arnold answered with something far "
            "stronger. <bookmark mark='c'/> Every continuous function of n variables on a cube is a sum of 2n plus "
            "one functions of one variable, each applied to a sum of n more functions of one variable. "
            "<bookmark mark='d'/> The only function of several variables you ever need is addition. "
            "<bookmark mark='e'/> Network researchers noticed it in the eighties, and argued: in 1989 Federico Girosi and "
            "Tomaso Poggio called it irrelevant, because the inner functions can be wildly irregular; in 1991 Vera "
            "Kurkova answered that smooth approximate versions work, with error bounds."
        ) as vo:
            self.play(FadeIn(h13, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(h13, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(ka, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(Write(th))
            self.play(FadeIn(ins), FadeIn(mids), FadeIn(out), Create(e1), Create(e2), FadeIn(pic_l), run_time=1.6)
            vo.wait_until("d")
            self.play(Indicate(mids, color=NEURON), Indicate(out, color=KANC), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeOut(pic_l), LaggedStart(*[FadeIn(m) for m in irr], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kan(self):
        d = load("kan")
        # an MLP: weights on edges, a fixed bend at each node; a KAN: a learned function on each edge, sums at nodes
        def diagram(x0, edge_pic):
            ins = VGroup(*[Circle(radius=0.16, color=GREY_B, stroke_width=2.5).move_to([x0 - 1.6, 0.6 - 1.2 * k, 0])
                           for k in range(2)])
            hid = VGroup(*[Circle(radius=0.16, color=NEURON, stroke_width=2.5).move_to([x0, 1.2 - 0.6 * q, 0])
                           for q in range(5)])
            out = Circle(radius=0.18, color=KANC, stroke_width=3).move_to([x0 + 1.6, 0, 0])
            e = VGroup(*[Line(a.get_center(), b.get_center(), buff=0.17, color=GREY_C, stroke_width=1.5)
                         for a in ins for b in hid], *[Line(b.get_center(), out.get_center(), buff=0.17, color=GREY_C,
                                                            stroke_width=1.5) for b in hid])
            return VGroup(e, ins, hid, out)

        mlp, kan = diagram(-3.6, False), diagram(3.0, True)
        ml = VGroup(label(r"MLP", font_size=30, color=NEURON),
                    label(r"a number on each edge, \\ a fixed bend at each node", font_size=22, color=GREY_A))
        kl = VGroup(label(r"KAN", font_size=30, color=KANC),
                    label(r"a learned curve on each edge, \\ just a sum at each node", font_size=22, color=GREY_A))
        for g_, l_ in ((mlp, ml), (kan, kl)):
            l_.arrange(DOWN, buff=0.1).next_to(g_, UP, buff=0.35)
        wdots = VGroup(*[Dot(e.get_center(), radius=0.05, color=WEIGHT) for e in mlp[0]])
        bends = VGroup(*[MathTex(r"\sigma", font_size=18, color=NEURON).move_to(c) for c in mlp[2]])
        xs = np.asarray(d["xs"])
        E = np.asarray(d["kan_edges"])[-1]
        order = [2 * (i % 5) + i // 5 for i in range(10)] + list(range(10, 15))  # edge i -> its learned curve
        curves_ = VGroup(*[mini_plot(xs, E[order[i]], width=0.55, height=0.34).move_to(kan[0][i].get_center())
                           for i in range(len(kan[0]))])
        spline = label(r"each curve: \ a cubic B-spline \\ on a grid, \ plus a SiLU", font_size=22, color=KANC)
        spline.next_to(kan, DOWN, buff=0.3)
        hc = history_card(r"April 2024", r"Ziming Liu, Max Tegmark et al.: \ KAN", r"Kolmogorov--Arnold networks: "
                          r"more accurate with fewer parameters on scientific formulas, \ and readable", width=6.0,
                          color=KANC).to_edge(DOWN, buff=0.25).shift(LEFT * 3.4)
        with self.voiceover(
            "In April 2024 Ziming Liu, Max Tegmark and colleagues turned the theorem into an architecture. "
            "<bookmark mark='a'/> An ordinary network puts a number on every edge and a fixed bend at every node. "
            "<bookmark mark='b'/> A Kolmogorov–Arnold network puts a learnable curve on every edge, a smooth spline "
            "on a grid of points, and only adds at the nodes. Unlike the theorem's version, the layers can be stacked "
            "as deep as you like. <bookmark mark='c'/> They reported that small KANs fit scientific formulas more "
            "accurately than much larger MLPs, that their error falls faster as they grow, and that you can read "
            "the learned curves and recover the formula."
        ) as vo:
            self.play(FadeIn(mlp), FadeIn(kan), FadeIn(ml), FadeIn(kl))
            vo.wait_until("a")
            self.play(FadeIn(wdots), FadeIn(bends))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_, scale=0.6) for c_ in curves_], lag_ratio=0.06), FadeIn(spline), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d = load("kan")
        xs = np.asarray(d["xs"])
        snaps = [int(s) for s in d["kan_snaps"]]
        E = np.asarray(d["kan_edges"])  # snapshot, edge, x
        cv = np.asarray(d["kan_curve"])  # step, train rmse, test rmse
        mc = np.asarray(d["mlp_curve"])
        f = cmath(r"f(x, y)", r"=", r"\exp\big(\sin(\pi x) + y^2\big)", font_size=34).to_corner(UL, buff=0.35)
        fl = label(r"the KAN paper's own example", font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.1).align_to(f, LEFT)
        # the [2, 5, 1] KAN laid out: 10 first-layer curves (5 hidden x 2 inputs), 5 second-layer curves
        pos1 = [np.array([-5.2 + 1.15 * (i % 5), 0.6 - 0.75 * (i // 5), 0]) for i in range(10)]
        pos2 = [np.array([-5.2 + 1.15 * i, -1.6, 0]) for i in range(5)]
        lo, hi = float(E.min()), float(E.max())

        def edges(k):
            g = VGroup()
            for i in range(10):
                g.add(mini_plot(xs, E[k, 2 * (i % 5) + i // 5], color=KANC).move_to(pos1[i]))
            for i in range(5):
                g.add(mini_plot(xs, E[k, 10 + i], color=C.BITS).move_to(pos2[i]))
            return g

        l1 = label(r"layer 1: \ each hidden unit's curve of $x$ \ (top) \ and of $y$ \ (below)", font_size=20,
                   color=KANC).next_to(pos1[0], UP, buff=0.45).align_to([-5.7, 0, 0], LEFT)
        l2 = label(r"layer 2: \ one curve per hidden unit", font_size=20, color=C.BITS).next_to(pos2[0], DOWN, buff=0.4)
        l2.align_to([-5.7, 0, 0], LEFT)
        steps = int(cv[-1, 0])
        g = axes([0, steps], [-4, 1], x_length=4.6, y_length=3.0, xlabel=r"step", ylabel=r"test error \ (log scale)",
                 xticks=[0, steps], yticks=[-4, -2, 0], yfmt=lambda v: rf"10^{{{int(v)}}}", center=[4.2, -0.4, 0],
                 font_size=18)
        t = ValueTracker(0)

        def upto(arr, col):
            def make():
                n_ = max(2, int(np.searchsorted(arr[:, 0], t.get_value(), side="right")))
                return VMobject(color=col, stroke_width=3).set_points_as_corners(
                    [g.ax.c2p(a, float(np.clip(np.log10(max(b, 1e-6)), -4, 1))) for a, b in arr[:n_, [0, 2]]])
            return make

        lk, lm = always_redraw(upto(cv, KANC)), always_redraw(upto(mc, NEURON))
        lg = legend([(KANC, rf"KAN $[2, 5, 1]$: \ ${int(d['kan_params'])}$ parameters"),
                     (NEURON, rf"MLP, \ two layers of $10$: \ ${int(d['mlp_params'])}$")], font_size=18)
        lg.next_to(g, UP, buff=0.2).align_to(g, LEFT)
        sv = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=26)
                           .move_to([4.2, -2.9, 0]))
        tag = note(r"computed: \ trained on $1{,}000$ points, \ tested on $1{,}000$ more").to_corner(DR, buff=0.15)
        kt, mt = float(d["kan_test"]), float(d["mlp_test"])
        ratio = mt / kt
        verdict = (f"The KAN ends with a test error of {kt:.4f}, {ratio:.0f} times smaller than the MLP's {mt:.4f}, "
                   "with about the same number of parameters." if ratio > 1.5 else
                   (f"The KAN ends at {kt:.4f} and the MLP at {mt:.4f}: about even, at the same size." if ratio > 0.67
                    else f"Here the MLP ends lower, {mt:.4f} against the KAN's {kt:.4f}."))
        cs, cq = float(np.max(d["corr_sin"])), float(np.max(d["corr_sq"]))
        shapes = (f"Some of the curves on x take the shape of a sine wave, and some on y of a parabola: the closest "
                  f"match a sine and a square with correlations of {cs:.2f} and {cq:.2f}. Pieces of the formula, drawn "
                  "as pictures."
                  if min(cs, cq) > 0.9 else
                  f"The curves change shape as it learns, but they don't spell out the formula on their own: the closest "
                  f"any comes to a sine is a correlation of {cs:.2f}, and to a square, {cq:.2f}. Reading a formula off a "
                  "KAN takes pruning and simplifying, as the paper describes.")
        cur = edges(0)
        with self.voiceover(
            "Let's try it, on the example from their paper: e to the sine of pi x, plus y squared. Here is a KAN "
            "with two inputs, five hidden nodes and one output: fifteen curves, all of them learned. "
            "<bookmark mark='a'/> Watch them as it trains. <bookmark mark='b'/> " + shapes + " <bookmark mark='c'/> " +
            verdict
        ) as vo:
            self.play(Write(f), FadeIn(fl), FadeIn(cur), FadeIn(l1), FadeIn(l2), FadeIn(g), FadeIn(lg), FadeIn(tag))
            self.add(lk, lm, sv)
            vo.wait_until("a")
            for k in range(1, len(snaps)):
                nxt = edges(k)
                self.play(Transform(cur, nxt), t.animate.set_value(snaps[k]), run_time=1.6)
            vo.wait_until("c")
            for m_ in (lk, lm, sv):
                m_.clear_updaters()
            self.play(Indicate(cur, color=WHITE, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def debate(self):
        d = load("kan")
        tab = d["table"]
        kans = np.array([(p, e) for kind, _, p, e in tab if kind == "kan"], float)
        mlps = np.array([(p, e) for kind, _, p, e in tab if kind == "mlp"], float)
        g = log_axes([1, 4], [-5, 0], 5.4, 3.8, center=[-3.0, -0.6, 0], xlabel=r"parameters",
                     ylabel=r"test error \ (log scale)", xticks=range(1, 5), yticks=range(-5, 1))
        ax = g.ax
        pk = VGroup(*[Dot(ax.c2p(np.log10(p), np.log10(e)), radius=0.07, color=KANC) for p, e in kans])
        pm = VGroup(*[Dot(ax.c2p(np.log10(p), np.log10(e)), radius=0.07, color=NEURON) for p, e in mlps])
        ck = curve(g.ax, np.log10(kans[:, 0]), np.log10(kans[:, 1]), KANC, 2.5)
        cm = curve(g.ax, np.log10(mlps[:, 0]), np.log10(mlps[:, 1]), NEURON, 2.5)
        lg = legend([(KANC, r"KANs, \ finer and finer grids"), (NEURON, r"MLPs, \ wider and wider")], font_size=20)
        lg.next_to(g, UP, buff=0.2).align_to(g, LEFT)
        cards = VGroup(
            history_card(r"July 2024", r"Runpeng Yu, Weihao Yu \& Xinchao Wang: \ \textit{KAN or MLP: A Fairer "
                         r"Comparison}", r"at equal parameters and operations, \ MLPs win on vision, language, audio "
                         r"and tabular tasks; \ KANs win on symbolic formulas, \ and forget more", width=6.0,
                         color=C.SURPRISE),
            history_card(r"August 2024", r"KAN 2.0", r"KANs as tools for science: \ finding formulas and "
                         r"conserved quantities", width=6.0, color=KANC),
            history_card(r"2026", r"inside frontier language models", r"still gated MLPs \ (the published "
                         r"configurations of Llama, Qwen, DeepSeek, gpt-oss)", width=6.0, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, -0.3, 0])
        tag = note(r"computed").next_to(g, DOWN, buff=0.1).align_to(g, RIGHT)
        bk = float(kans[:, 1].min())
        bm = float(mlps[:, 1].min())
        res = (f"On this function, a smooth formula, KANs reach lower errors per parameter: the best KAN, at "
               f"{bk:.5f}, beats the best MLP, at {bm:.5f}." if bk < bm else
               f"On this function our best MLP, at {bm:.5f}, actually beats our best KAN, at {bk:.5f}.")
        with self.voiceover(
            "Then came the debate. <bookmark mark='a'/> " + res + " That's the kind of task the paper chose. "
            "<bookmark mark='b'/> In July 2024 Runpeng Yu, Weihao Yu and Xinchao Wang compared the two fairly, at "
            "equal numbers of parameters and operations, on images, text, audio and tables. MLPs generally won. "
            "KANs won on symbolic formulas, and forgot more of an old task when taught a new one. "
            "<bookmark mark='c'/> The KAN authors' sequel that August leaned into science: finding formulas and "
            "conserved quantities. <bookmark mark='d'/> And inside today's language models, the published "
            "configurations still show gated MLPs. A theorem from 1957 found a niche, not a revolution."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pk], lag_ratio=0.15), Create(ck),
                      LaggedStart(*[FadeIn(p) for p in pm], lag_ratio=0.15), Create(cm), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(cards[2], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
