from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import CLS_A, CLS_B, NEURON, PART, PLAIN, RES, load, region_image


class Residual(VoiceoverScene):
    def construct(self):
        self.card()
        self.block()
        self.curves()
        self.inside()
        self.paths()

    def card(self):
        card = chapter_card(11, r"The residual stream", r"How do you train forty layers?", part=PART, lit=(2015,))
        with self.voiceover("Chapter eleven. The residual stream."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def block(self):
        # a plain stack against a residual stack, drawn as boxes
        def stack(x, residual):
            g = VGroup()
            ys = [2.2 - 1.05 * k for k in range(4)]
            spine = Line([x, 2.8, 0], [x, -2.0, 0], color=RES if residual else GREY_D, stroke_width=6 if residual else 0)
            g.add(spine)
            for yv in ys:
                box = RoundedRectangle(width=1.6, height=0.6, corner_radius=0.12, stroke_color=NEURON, stroke_width=2.5,
                                       fill_color="#121722", fill_opacity=1).move_to([x + (1.3 if residual else 0), yv - 0.5, 0])
                g.add(box, MathTex(r"f_\ell", font_size=28).move_to(box))
                if residual:
                    g.add(Arrow([x, yv, 0], box.get_top() + LEFT * 0.3, buff=0.05, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.2),
                          Arrow(box.get_bottom() + LEFT * 0.3, [x, yv - 1.0, 0], buff=0.05, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.2),
                          MathTex(r"+", font_size=30, color=RES).move_to([x - 0.25, yv - 1.0, 0]))
                else:
                    g.add(Arrow([x, yv + 0.2, 0], box.get_top(), buff=0.03, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.2))
            return g

        plain = stack(-4.2, False)
        res = stack(0.6, True)
        pt = label(r"plain: \ $h_{\ell+1} = f_\ell(h_\ell)$", font_size=28, color=PLAIN).next_to(plain, DOWN, buff=0.3)
        rt = label(r"residual: \ $h_{\ell+1} = h_\ell + f_\ell(h_\ell)$", font_size=28, color=RES).next_to(res, DOWN, buff=0.3)
        colors = {r"I": RES}
        jac = cmath(r"\frac{\partial h_{\ell+1}}{\partial h_\ell}", "=", r"I", "+", r"\frac{\partial f_\ell}{\partial h_\ell}",
                    colors=colors, font_size=38).move_to([4.8, 1.2, 0])
        jl = label(r"the identity always gets through: \\ gradients reach the first layers", font_size=24, color=GREY_A)
        jl.next_to(jac, DOWN, buff=0.3)
        wl = label(r"the skip path: \ a plain wire \\ for the gradient", font_size=24, color=RES).next_to(jl, DOWN, buff=0.45)
        cite_ = cite(r"K.~He, X.~Zhang, S.~Ren \& J.~Sun, \textit{Deep Residual Learning for Image Recognition} (2015)",
                     corner=DR)
        pulse = glow_dot(res[0].get_end(), color=WHITE, radius=0.1)
        with self.voiceover(
            "Good initialization gets a signal through at the start, but training can still go wrong in a deep "
            "stack. In December 2015, Kaiming He and colleagues published a fix so simple it's now everywhere. "
            "<bookmark mark='a'/> Instead of each layer replacing what came before, let it add to it. The layers "
            "become small corrections to a stream of numbers flowing straight through: the residual stream. "
            "<bookmark mark='b'/> By the chain rule, the derivative of each block is the identity plus a little "
            "extra. <bookmark mark='w'/> The skip path passes the gradient back unchanged, like a plain wire, so "
            "gradients always have a clear path back to the first layer. Every transformer in this "
            "series is built this way."
        ) as vo:
            self.play(FadeIn(plain), FadeIn(pt), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(res), FadeIn(rt))
            vo.wait_until("b")
            self.play(Write(jac), FadeIn(jl))
            vo.wait_until("w")
            self.play(FadeIn(pulse), FadeIn(wl))
            self.play(pulse.animate.move_to(res[0].get_start()), run_time=2.0, rate_func=linear)
            self.play(FadeOut(pulse))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        r = load("residual")
        P, R = (np.asarray(r[k]) for k in ("plain", "residual"))
        ax = Axes(x_range=[0, P[-1, 0], 500], y_range=[0.4, 1.0, 0.1], x_length=8.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.6, -0.5, 0])
        yl = VGroup(*[MathTex(rf"{int(round(100 * v))}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0.5, 0.75, 1.0)])
        xl = label(r"training steps", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"spiral points on the right side", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        cp, cr = (curve(ax, D[:, 0], D[:, 2], col, 4) for D, col in ((P, PLAIN), (R, RES)))
        pf, rf = float(P[-1, 2]), float(R[-1, 2])
        names = VGroup(label(rf"$40$ plain layers: \ ${100 * pf:.0f}\%$", font_size=26, color=PLAIN),
                       label(rf"$40$ residual layers: \ ${100 * rf:.0f}\%$", font_size=26, color=RES))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 0.8, 0])
        same = label(r"same width, \\ same optimizer, \\ same steps", font_size=24, color=GREY_A).next_to(names, DOWN, buff=0.6)
        same.align_to(names, LEFT)
        tag = note(r"computed").to_corner(DR, buff=0.2)
        first = int(R[np.argmax(R[:, 2] > 0.99), 0]) if (R[:, 2] > 0.99).any() else None
        plain_says = ("never learns anything: it's stuck at a coin flip" if pf < 0.6 else
                      f"learns only slowly, to {100 * pf:.0f} percent")
        res_says = (f"learn the spirals completely, within {first:,} steps" if first is not None and rf > 0.99 else
                    f"reach {100 * rf:.0f} percent of the points")
        with self.voiceover(
            "Here it is on the spirals, with forty layers of thirty-two units. <bookmark mark='a'/> The plain stack "
            f"{plain_says}. <bookmark mark='b'/> The same forty layers with residual connections {res_says}. Same "
            "width, same optimizer, same number of steps."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cp), FadeIn(names[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cr), FadeIn(names[1]), run_time=2.0)
            self.play(FadeIn(same))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inside(self):
        """Why: the two forty-layer stacks as they train, their answers everywhere and the gradient reaching each layer."""
        r = load("residual")
        sp = load("spiral")
        X, y = np.asarray(sp["X"]), np.asarray(sp["y"])
        steps = [int(s_) for s_ in r["snap_steps"]]
        xs = np.asarray(r["xs"])
        nets = ("plain", "residual")
        cols = {"plain": PLAIN, "residual": RES}
        probs = {n: np.asarray(r[f"probs_{n}"]) for n in nets}
        gn = {n: np.log10(np.maximum(np.asarray(r[f"gnorm_{n}"]), 1e-30)) for n in nets}
        lo = float(min(g.min() for g in gn.values())) - 0.3
        hi = float(max(g.max() for g in gn.values())) + 0.1
        S, span = 3.4, 6.8
        cx = {"plain": -3.4, "residual": 3.4}
        cy = 1.05
        frames_ = Group()
        dots = VGroup()
        for n in nets:
            c = np.array([cx[n], cy, 0])
            frames_.add(Square(S, stroke_color=GREY_D, stroke_width=1.5).move_to(c))
            dots.add(*[Dot(c + np.array([p[0] * S / span, p[1] * S / span, 0]), radius=0.018,
                           color=CLS_A if v == 0 else CLS_B, fill_opacity=0.8) for p, v in zip(X, y)])

        def maps(k):
            return Group(*[region_image(probs[n][k], np.zeros_like(probs[n][k]), xs, S, S, boundary=False)
                           .move_to([cx[n], cy, 0]) for n in nets])

        BW, BH, by = 5.6, 1.5, -2.95  # the gradient bars: width of the forty, height of the range, baseline

        def bars(k):
            g = VGroup()
            for n in nets:
                for i, v in enumerate(gn[n][k]):
                    h = max(BH * (v - lo) / (hi - lo), 0.01)
                    x = cx[n] - BW / 2 + (i + 0.5) * BW / len(gn[n][k])
                    g.add(Rectangle(width=BW / len(gn[n][k]) * 0.7, height=h, stroke_width=0, fill_color=cols[n],
                                    fill_opacity=0.85).move_to([x, by + h / 2, 0]))
            return g

        base = VGroup(*[Line([cx[n] - BW / 2 - 0.1, by, 0], [cx[n] + BW / 2 + 0.1, by, 0], color=GREY_C, stroke_width=1.5)
                        for n in nets])
        heads = VGroup(*[label(rf"$40$ {'plain' if n == 'plain' else 'residual'} layers", font_size=24, color=cols[n])
                         .next_to(frames_[j], UP, buff=0.12) for j, n in enumerate(nets)])
        bl = VGroup(*[label(r"layer $1$ \ $\longrightarrow$ \ layer $40$", font_size=18, color=GREY_B)
                      .next_to(b_, DOWN, buff=0.1) for b_ in base])
        gl = label(r"how much gradient reaches each layer \ (log scale)", font_size=20, color=GREY_A).move_to([0, by + BH + 0.25, 0])
        t = ValueTracker(0)
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=30,
                                            color=WHITE).move_to([0, cy + 0.6, 0]))
        cur_m, cur_b = maps(0), bars(0)
        e = int(np.floor(gn["plain"][0, -1] - gn["plain"][0, 0]))  # the last layer's gradient over the first's, in powers of 10
        big = {9: "a billion", 10: "ten billion", 11: "a hundred billion", 12: "a trillion", 13: "ten trillion",
               14: "a hundred trillion", 15: "a quadrillion"}.get(e, f"ten to the {e}")
        rr = 10 ** float(gn["residual"][0].max() - gn["residual"][0].min())
        fade = float(gn["residual"][0].mean() - gn["residual"][-1].mean())
        with self.voiceover(
            "Why does the plain stack never learn? Look inside both of them as they train: on top, what each one says "
            "about every point of the plane; below, how much gradient reaches each of its forty layers, on a log "
            f"scale. <bookmark mark='a'/> At the start, the plain stack's gradients shrink layer by layer on the "
            f"way down: the first layer gets more than {big} times less than the last. The residual stack's "
            f"gradients are all about the same size, within a factor of {rr:.0f}, because each block adds to a "
            "stream the gradient flows straight back along. <bookmark mark='b'/> So as training runs, the residual "
            "stack's answer bends to follow the spirals, and its gradients shrink together, by a factor of "
            f"{'ten' if round(fade) == 1 else ['a hundred', 'a thousand', 'ten thousand', 'a hundred thousand', 'a million'][min(round(fade), 6) - 2]}"
            ", as there is less and less left to fix. The plain stack's answer stays one flat colour, the same "
            "everywhere, and its gradients only fade further."
        ) as vo:
            self.play(FadeIn(frames_), FadeIn(cur_m), FadeIn(dots), FadeIn(heads))
            self.add(cnt)
            self.play(Create(base), FadeIn(bl), FadeIn(gl), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in cur_b], lag_ratio=0.01),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(VGroup(*cur_b[:len(cur_b) // 2]), color=PLAIN, scale_factor=1.05), run_time=1.5)
            vo.wait_until("b")
            for k in range(1, len(steps)):
                nm, nb = maps(k), bars(k)
                self.play(FadeOut(cur_m), FadeIn(nm), Transform(cur_b, nb), t.animate.set_value(steps[k]), run_time=1.6)
                cur_m = nm
                self.bring_to_front(dots)
        self.wait(0.4)
        self.remove(cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paths(self):
        colors = {r"I": RES}
        rows = [cmath(r"h_L", r"=", r"h_0 + \textstyle\sum_{l} f_l(h_l)", font_size=36, colors=colors),
                cmath(r"\frac{\partial h_L}{\partial h_0}", r"=", r"(I + J_L) \cdots (I + J_2)(I + J_1)", font_size=36,
                      colors=colors),
                cmath(r"\frac{\partial h_L}{\partial h_0}", r"=", r"I", r"+ \textstyle\sum_l J_l + \sum_{l > k} J_l J_k + \cdots",
                      font_size=36, colors=colors)]
        whys = [why(r"every block adds to the stream"), why(r"chain rule: \ $J_l = \partial f_l / \partial h$"),
                why(r"multiply out: \ $2^L$ paths, \ one of them the identity")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-2.4, buff=0.5, edge=6.9)
        # three blocks unrolled into eight paths
        xs = [-5.2, -3.2, -1.2, 0.8]
        Y = -2.75  # the diagram's baseline, below the derivation
        nodes = VGroup(*[Dot([x, Y, 0], radius=0.08, color=RES) for x in xs])
        paths_ = VGroup()
        for mask in range(8):
            pts = [np.array([xs[0], Y, 0])]
            for k in range(3):
                on = (mask >> k) & 1
                mid = np.array([(xs[k] + xs[k + 1]) / 2, Y + (0.25 + 0.12 * mask if on else -0.0), 0])
                pts += [mid, np.array([xs[k + 1], Y, 0])]
            col = interpolate_color(ManimColor(RES), ManimColor(NEURON), bin(mask).count("1") / 3)
            paths_.add(VMobject(color=col, stroke_width=2.2, stroke_opacity=0.8).set_points_smoothly(pts))
        pl = label(r"$3$ blocks: \ $2^3 = 8$ paths, \ from no block to all three", font_size=24, color=GREY_A)
        pl.next_to(nodes, DOWN, buff=0.25)
        tag = note(r"schematic").next_to(paths_, UP, buff=0.1).align_to(paths_, LEFT)
        def item(lines, color):
            return VGroup(*[label(t_, font_size=26, color=color) for t_ in lines]).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.08)

        hist_ = VGroup(
            item([r"1997: \ the LSTM's constant error carousel"], GREY_A),
            item([r"May 2015: \ highway networks", r"(Srivastava, Greff \& Schmidhuber)"], GREY_A),
            item([r"Dec 2015: \ ResNet, \ $152$ layers, \ wins ImageNet"], RES),
            item([r"2019: \ GPT-2 scales each block's", r"starting weights by $1/\sqrt{N}$"], GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.0, 0])
        cite_ = cite(r"A.~Veit, M.~Wilber \& S.~Belongie, \textit{Residual Networks Behave Like Ensembles of Relatively "
                     r"Shallow Networks} (2016)", corner=DL)
        with self.voiceover(
            "There's another way to see what the stream does. <bookmark mark='a'/> The last layer is the first plus "
            "everything the blocks added. <bookmark mark='b'/> Its derivative is a product of identity-plus-a-little "
            "factors, <bookmark mark='c'/> and multiplying it out gives two to the L terms: one for every path through "
            "the network, from the path that skips every block to the one that goes through all of them. A residual "
            "network is a crowd of networks of every depth, sharing weights, and Andreas Veit and colleagues found "
            "that most of the gradient flows through the short ones. <bookmark mark='d'/> The idea had ancestors: "
            "the LSTM's constant error carousel in 1997, and the highway networks of Rupesh Srivastava, Klaus Greff "
            "and Juergen Schmidhuber, months before ResNet. ResNet won ImageNet with a hundred and fifty-two layers. "
            "And GPT-2 shrank each block's starting weights by one over the square root of the number of blocks, so "
            "the stream doesn't grow with depth."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(nodes), LaggedStart(*[Create(p) for p in paths_], lag_ratio=0.15), FadeIn(pl), FadeIn(tag),
                      run_time=2.5)
            vo.wait_until("d")
            pic = VGroup(nodes, paths_, pl, tag)
            self.play(FadeOut(VGroup(*rows, *whys)), pic.animate.scale(1.1).move_to([-3.3, 0.0, 0]), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(h) for h in hist_], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()
