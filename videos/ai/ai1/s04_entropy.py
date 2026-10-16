from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import ALPHA27, area_slivers, letter, load, plain_axes, polyline


class Entropy(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.average()
        self.uniform()
        self.coin()
        self.jensen()
        self.conditional()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Entropy: the average surprise", r"How surprised should you expect to be?",
                            lit=(1948,), part=1)
        with self.voiceover("Chapter three. Entropy.") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def average(self):
        lt = load("letters")
        p = lt["p"]
        H = float(lt["H"])
        assert abs(H - 4.084) < 0.001
        defn = mtex([r"H(p)", r"=", r"\sum_x p(x)\, \log_2 \frac{1}{p(x)}", r"=", r"\mathbb{E}\big[\, s(X) \,\big]"],
                    font_size=42).to_edge(UP, buff=0.4)
        defn[0].set_color(C.ENTROPY)
        sub = label(r"the surprise you should \textit{expect}: \ each surprise weighted by how often it happens",
                    font_size=26, color=GREY_A).next_to(defn, DOWN, buff=0.25)
        W, scale, y0 = 11.0, 0.32, -2.5
        order = list(lt["order"])  # common to rare
        flat, cum = {}, 0.0
        for i in order:
            pi = p[i]
            flat[i] = Rectangle(width=W * pi, height=0.05, stroke_width=0.8, stroke_color=BACKGROUND,
                                fill_color=C.TRUE_P, fill_opacity=0.9).move_to([-W / 2 + (cum + pi / 2) * W, y0 + 0.025, 0])
            cum += pi
        flat = VGroup(*[flat[i] for i in range(27)])
        sl = area_slivers(p, W=W, y0=y0, scale=scale, order=order)
        self.order = order
        base = Line([-W / 2, y0, 0], [W / 2, y0, 0], color=GREY_C, stroke_width=1.5)
        wl = label(r"width: \ $p(x)$", font_size=24, color=C.TRUE_P).next_to(base, DOWN, buff=0.45)
        tall = [ALPHA27.index(c) for c in " ezq"]
        labs = VGroup()
        for i in tall:
            t = letter(ALPHA27[i], font_size=20, color=WHITE).next_to(sl[i], UP, buff=0.08)
            labs.add(t)
        hl = label(r"height: \ $\log_2 \frac{1}{p(x)}$", font_size=24, color=C.SURPRISE)
        hl.move_to([3.0, y0 + scale * 11.0, 0])
        area = label(rf"area $= H = {H:.2f}$ bits", font_size=34, color=C.ENTROPY).move_to([-3.2, y0 + scale * 5.6, 0])
        with self.voiceover(
            "Surprise is about one event. Before the event, we can ask a different question: on average, how "
            "surprised should we expect to be? <bookmark mark='a'/> Weight each surprise by how often it happens, "
            "and add up. That average surprise is the entropy, written H of p."
        ) as vo:
            self.play(FadeIn(defn[:3]))
            vo.wait_until("a")
            self.play(FadeIn(defn[3:]), FadeIn(sub))
        with self.voiceover(
            "There's a nice picture of it. Take the unit bar from chapter one, <bookmark mark='a'/> each symbol a "
            "sliver as wide as its probability, sorted from common to rare. <bookmark mark='b'/> Now raise each sliver to the height of its "
            "surprise. Common symbols are wide and low; rare ones are thin and tall. <bookmark mark='c'/> The entropy "
            "is the total area: for English letters, 4.08 bits."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(base), FadeIn(flat), FadeIn(wl))
            vo.wait_until("b")
            self.play(ReplacementTransform(flat, sl), FadeIn(hl), run_time=2.0)
            self.play(FadeIn(labs))
            vo.wait_until("c")
            self.play(FadeIn(area))
        self.sl, self.base, self.area, self.labs, self.W, self.scale, self.y0 = sl, base, area, labs, W, scale, y0
        self.defn, self.sub, self.wl, self.hl = defn, sub, wl, hl

    # ------------------------------------------------------------------
    def uniform(self):
        W, scale, y0 = self.W, self.scale, self.y0
        u = np.full(27, 1 / 27)
        uni = area_slivers(u, W=W, y0=y0, scale=scale, color=GREY_B, opacity=0.5)
        Hu = math.log2(27)
        lab_u = label(rf"all $27$ equally likely: \ area $= \log_2 27 = {Hu:.2f}$ bits", font_size=28, color=GREY_A)
        lab_u.move_to([-2.0, 1.25, 0])
        red = label(r"English letters: \ $4.08$ bits. \ The rest is \textit{redundancy}.", font_size=28, color=C.ENTROPY)
        red.next_to(lab_u, DOWN, buff=0.2).align_to(lab_u, LEFT)
        with self.voiceover(
            "Compare a source where all twenty-seven symbols are equally likely. <bookmark mark='a'/> Every sliver "
            "is the same width, and the same height: log two of twenty-seven, 4.75 bits. That's the most you can "
            "be surprised, on average, by one symbol from twenty-seven. <bookmark mark='b'/> English, even counted "
            "one letter at a time, sits below it. The gap is what Shannon called redundancy: structure a good "
            "guesser can exploit."
        ) as vo:
            self.play(FadeOut(self.area), FadeOut(self.labs), FadeOut(self.hl))
            vo.wait_until("a")
            self.play(FadeIn(uni), self.sl.animate.set_fill(opacity=0.35), run_time=1.5)
            self.play(FadeIn(lab_u))
            vo.wait_until("b")
            self.play(self.sl.animate.set_fill(opacity=0.85), FadeIn(red))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def coin(self):
        ax = plain_axes([0, 1, 0.25], [0, 1, 0.5], 6.4, 4.0).shift(RIGHT * 2.8 + DOWN * 0.4)
        xl = VGroup(*[MathTex(t, font_size=24, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.15)
                      for t, v in (("0", 0), ("\\tfrac12", 0.5), ("1", 1))])
        yl = VGroup(*[MathTex(t, font_size=24, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15)
                      for t, v in (("0", 0), ("1", 1))])
        axl = VGroup(label(r"$P(\text{heads})$", font_size=24, color=GREY_A).next_to(ax.c2p(1, 0), DOWN, buff=0.45),
                     label(r"$H$, bits", font_size=24, color=GREY_A).next_to(ax.c2p(0, 1), UP, buff=0.15))
        xs = np.linspace(0.0005, 0.9995, 400)
        hb = -(xs * np.log2(xs) + (1 - xs) * np.log2(1 - xs))
        curve = polyline(ax, xs, hb, color=C.ENTROPY, stroke_width=4)
        f = mtex(r"H = p \log_2 \tfrac1p + (1 - p) \log_2 \tfrac{1}{1-p}", font_size=34).to_edge(UP, buff=0.5)
        t = ValueTracker(0.5)

        def hbin(v):
            return float(-(v * math.log2(v) + (1 - v) * math.log2(1 - v)))

        def inset():
            v = t.get_value()
            g = area_slivers([v, 1 - v], W=4.6, x=-4.1, y0=-2.2, scale=0.62, color=C.SURPRISE)
            g[0].set_fill(C.TRUE_P, 0.8)
            heads = MathTex("H", font_size=24, color=C.TRUE_P).next_to(g[0], UP, buff=0.06)
            tails = MathTex("T", font_size=24, color=C.SURPRISE).next_to(g[1], UP, buff=0.06)
            val = MathTex(rf"p = {v:.2f}, \quad H = {hbin(v):.2f}", font_size=30).move_to([-4.1, 1.5, 0])
            return VGroup(g, heads, tails, val)

        ins = always_redraw(inset)
        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), hbin(t.get_value())), radius=0.08, color=WHITE))
        with self.voiceover(
            "The simplest case is a coin. <bookmark mark='a'/> If it's fair, the entropy is one bit. "
            "<bookmark mark='b'/> Bias it, and the outcome gets easier to guess. Heads ninety percent of the time, "
            "and the entropy falls to 0.47 bits. <bookmark mark='c'/> A coin that always lands heads has no "
            "entropy at all. The entropy is largest when the outcomes are equally likely."
        ) as vo:
            self.play(Write(f), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(axl))
            self.play(Create(curve))
            vo.wait_until("a")
            self.add(ins, dot)
            self.wait(0.5)
            vo.wait_until("b")
            self.play(t.animate.set_value(0.9), run_time=2.0)
            assert abs(hbin(0.9) - 0.469) < 0.001
            vo.wait_until("c")
            self.play(t.animate.set_value(0.999), run_time=1.5)
            self.play(t.animate.set_value(0.5), run_time=1.5)
        ins.clear_updaters()
        dot.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def jensen(self):
        # every distribution on three outcomes is a point of a triangle; its entropy, a height: a dome
        zb = -1.2  # the triangle sits low, so the dome is centred once the camera tilts
        T = [np.array([-2.7, -2.1, zb]), np.array([2.7, -2.1, zb]), np.array([0.0, 2.55, zb])]
        mid = sum(T) / 3
        zs = 1.55  # height per bit

        def H3(a, b, c):
            return -sum(x * math.log2(x) for x in (a, b, c) if x > 1e-12)

        def at(a, b, c, lift=0.0):
            return a * T[0] + b * T[1] + c * T[2] + np.array([0, 0, zs * H3(a, b, c) + lift])

        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[0, 3, 1], x_length=8, y_length=8, z_length=3)
        dome = Surface(lambda u, v: at(u, (1 - u) * v, (1 - u) * (1 - v)), u_range=[0, 1], v_range=[0, 1],
                       resolution=(32, 32), fill_opacity=0.9, stroke_width=0.3, stroke_color=BACKGROUND,
                       checkerboard_colors=False)
        dome.set_fill_by_value(axes=axes, colorscale=list(zip(SURFACE_COLORS, np.linspace(zb, zb + zs * math.log2(3), 5))),
                               axis=2)
        tri = Polygon(*T, color=GREY_B, stroke_width=2)
        edges = VGroup(*[ParametricFunction(lambda t, i=i: at(*np.roll([t, 1 - t, 0.0], i), lift=0.02),
                                            t_range=[0.001, 0.999], color=C.ENTROPY, stroke_width=4)
                         for i in range(3)])
        peak = Dot3D(at(1 / 3, 1 / 3, 1 / 3, lift=0.08), radius=0.12, color=WHITE)
        stem = DashedLine(mid, at(1 / 3, 1 / 3, 1 / 3), color=WHITE,
                          stroke_width=2)
        corners = VGroup(*[MathTex(t, font_size=36, color=GREY_A).move_to(T[i] + 0.4 * normalize(T[i] - mid))
                           for i, t in enumerate((r"A", r"B", r"C"))])
        head = label(r"No distribution on $K$ outcomes beats the uniform one", font_size=34).to_edge(UP, buff=0.35)
        top = label(r"uniform: \ $\log_2 3 = 1.58$ bits", font_size=30, color=WHITE).to_corner(UR, buff=0.5).shift(DOWN * 0.6)
        edge_l = label(r"each edge: \ a coin", font_size=28, color=C.ENTROPY).next_to(top, DOWN, buff=0.25).align_to(top, LEFT)
        for m in (head, top, edge_l):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        with self.voiceover(
            "That's true in general. With K possible outcomes, the entropy is at most log two of K. "
            "<bookmark mark='a'/> The proof is one inequality. The logarithm bends downward, so the average of logs "
            "is at most the log of the average. That's Jensen's inequality. <bookmark mark='b'/> Entropy is an "
            "average of logs. <bookmark mark='c'/> Swap in the log of the average, <bookmark mark='d'/> and the "
            "average of one over p is just the number of outcomes. <bookmark mark='e'/> So H is at most log K, with "
            "equality only when every outcome is equally likely."
        ) as vo:
            self.play(FadeIn(head), Create(tri), FadeIn(corners), FadeIn(dome), run_time=1.2)
            self.move_camera(phi=62 * DEGREES, theta=-62 * DEGREES, added_anims=[FadeOut(corners)], run_time=2.2)
            self.play(Create(edges), FadeIn(peak), Create(stem), FadeIn(top), FadeIn(edge_l), run_time=1.2)
            self.begin_ambient_camera_rotation(rate=0.35)
            vo.wait_until("a")
            self.stop_ambient_camera_rotation()
            self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(dome, tri, edges, peak, stem)),
                                                                    FadeOut(top), FadeOut(edge_l)], run_time=1.6)
            self.jensen_2d(vo)
        self.wait(0.3)
        self.clear_scene()

    def jensen_2d(self, vo):
        ax = plain_axes([0, 8, 2], [-1, 3.2, 1], 6.0, 3.9).shift(LEFT * 3.0 + DOWN * 0.8)
        xs = np.linspace(0.5, 8, 300)
        curve = polyline(ax, xs, np.log2(xs), color=C.ENTROPY, stroke_width=5)
        a_, b_ = 1.0, 7.0
        m = 0.5 * (a_ + b_)
        pa = glow_dot(ax.c2p(a_, math.log2(a_)), color=C.BITS, radius=0.07, layers=3)
        pb = glow_dot(ax.c2p(b_, math.log2(b_)), color=C.BITS, radius=0.07, layers=3)
        chord = Line(ax.c2p(a_, math.log2(a_)), ax.c2p(b_, math.log2(b_)), color=C.BITS, stroke_width=3)
        pm = glow_dot(ax.c2p(m, math.log2(m)), color=C.ENTROPY, radius=0.08, layers=4)
        pc = glow_dot(ax.c2p(m, 0.5 * (math.log2(a_) + math.log2(b_))), color=C.BITS, radius=0.08, layers=4)
        gap = Line(pc.get_center(), pm.get_center(), color=WHITE, stroke_width=2.5)
        lab1 = MathTex(r"\log_2 \mathbb{E}[Y]", font_size=32, color=C.ENTROPY).next_to(pm, UP, buff=0.15)
        lab2 = MathTex(r"\mathbb{E}[\log_2 Y]", font_size=32, color=C.BITS).next_to(pc, DOWN, buff=0.18)
        cap = label(r"$\log_2$ bends down: \ the average of logs $\le$ the log of the average", font_size=26,
                    color=GREY_A).next_to(ax, DOWN, buff=0.35)
        colors = {r"H(p)": C.ENTROPY, r"\log_2 K": C.ENTROPY}
        steps = [
            [r"H(p)", "=", r"\mathbb{E}\Big[\log_2 \tfrac{1}{p(X)}\Big]"],
            [r"H(p)", r"\le", r"\log_2 \mathbb{E}\Big[\tfrac{1}{p(X)}\Big]"],
            [r"H(p)", r"\le", r"\log_2 \sum_x p(x)\,\tfrac{1}{p(x)}"],
            [r"H(p)", r"\le", r"\log_2 K"],
        ]
        eqs = [cmath(*st, colors=colors, font_size=48).move_to([3.6, 0.9, 0]) for st in steps]
        whys = [why(r"definition"), why(r"Jensen: $\log_2$ is concave"), why(r"write out $\mathbb{E}$"),
                why(r"$K$ terms, each $1$")]
        for w in whys:
            w.scale(1.2).move_to([3.6, -0.4, 0])
        eq = label(r"equality exactly when $p$ is uniform", font_size=30, color=C.BITS).move_to([3.6, -1.6, 0])
        self.play(Create(ax), Create(curve), run_time=1.2)
        self.play(FadeIn(pa), FadeIn(pb), Create(chord))
        self.play(FadeIn(pm), FadeIn(pc), Create(gap), FadeIn(lab1), FadeIn(lab2), FadeIn(cap))
        vo.wait_until("b")
        self.play(Write(eqs[0]), FadeIn(whys[0]))
        prev = eqs[0]
        for k, mark in enumerate("cde"):
            vo.wait_until(mark)
            self.play(FadeOut(whys[k]), FadeIn(whys[k + 1]), run_time=0.5)
            morph(self, prev, eqs[k + 1], run_time=1.1)
            prev = eqs[k + 1]
        box = SurroundingRectangle(prev, color=C.ENTROPY, buff=0.2, corner_radius=0.1)
        self.play(Create(box), FadeIn(eq))

    # ------------------------------------------------------------------
    def conditional(self):
        b = load("bigram")
        lt = load("letters")
        p1 = b["joint"].sum(1)
        rowH = np.asarray(b["row_H"])
        Hc = float(b["H_cond"])
        assert abs(Hc - 3.33) < 0.005 and rowH[ALPHA27.index("q")] < 0.05 and rowH[0] > 4.0
        W, y0, scale = 11.6, -2.7, 0.8
        cols, cum = VGroup(), 0.0
        for i in range(27):
            h = scale * rowH[i]
            r = Rectangle(width=max(W * p1[i], 0.003), height=max(h, 0.003), stroke_width=0.8,
                          stroke_color=BACKGROUND, fill_color=C.CONTEXT, fill_opacity=0.85)
            r.move_to([-W / 2 + (cum + p1[i] / 2) * W, y0 + h / 2, 0])
            cols.add(r)
            cum += p1[i]
        labs = VGroup(*[letter(ALPHA27[i], font_size=18, color=GREY_A).next_to(cols[i], DOWN, buff=0.1)
                        for i in range(27) if W * p1[i] > 0.25])
        base = Line([-W / 2, y0, 0], [W / 2, y0, 0], color=GREY_C, stroke_width=1.5)
        H1 = Line([-W / 2, y0 + scale * float(lt["H"]), 0], [W / 2, y0 + scale * float(lt["H"]), 0], color=C.ENTROPY,
                  stroke_width=2.5)
        H1l = label(r"$H(\text{next}) = 4.08$: \ no context", font_size=24, color=C.ENTROPY).next_to(H1, UP, buff=0.1)
        H1l.align_to(H1, RIGHT)
        defn = mtex(r"H(Y \mid X) = \sum_x p(x)\, H(Y \mid X = x)", font_size=38).to_edge(UP, buff=0.4)
        q_i = ALPHA27.index("q")
        q_lab = label(r"after \texttt{q}: \ $0.02$ bits", font_size=22, color=C.BITS)
        q_lab.move_to([cols[q_i].get_x() - 1.2, y0 + scale * 5.1, 0])
        q_arrow = Arrow(q_lab.get_bottom(), cols[q_i].get_top(), buff=0.05, color=C.BITS, stroke_width=2,
                        max_tip_length_to_length_ratio=0.2)
        sp_lab = label(r"after a space: \ $4.11$", font_size=22, color=C.BITS).next_to(cols[0], UP, buff=0.12)
        assert abs(rowH[q_i] - 0.02) < 0.006 and abs(rowH[0] - 4.11) < 0.006
        area = label(rf"area $= H(\text{{next}} \mid \text{{previous}}) = {Hc:.2f}$ bits", font_size=30,
                     color=C.CONTEXT).next_to(defn, DOWN, buff=0.3)
        rule = label(r"on average, knowing more never hurts: \ $H(Y \mid X) \le H(Y)$ \quad (proof: Chapter 5)",
                     font_size=24, color=GREY_A).next_to(area, DOWN, buff=0.2)
        with self.voiceover(
            "Entropy also works when we know something. For each previous letter, the next letter has its own "
            "distribution, and its own entropy. <bookmark mark='a'/> Draw a column for each previous letter, as wide "
            "as that letter is common, and as tall as the entropy of what follows it. <bookmark mark='b'/> After q, "
            "almost nothing: two hundredths of a bit. <bookmark mark='c'/> After a space, a new word begins, and the "
            "entropy is 4.11 bits."
        ) as vo:
            self.play(Write(defn))
            vo.wait_until("a")
            self.play(Create(base), LaggedStart(*[GrowFromEdge(c, DOWN) for c in cols], lag_ratio=0.04), FadeIn(labs),
                      run_time=2.2)
            vo.wait_until("b")
            self.play(FadeIn(q_lab), GrowArrow(q_arrow))
            vo.wait_until("c")
            self.play(FadeIn(sp_lab))
        with self.voiceover(
            "The total area is the conditional entropy: 3.33 bits, given the previous letter, <bookmark mark='a'/> "
            "down from 4.08 bits with no context at all. <bookmark mark='b'/> On average, knowing more never makes "
            "you more uncertain. We'll prove that in chapter five."
        ) as vo:
            self.play(FadeIn(area))
            vo.wait_until("a")
            self.play(Create(H1), FadeIn(H1l))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.5)
        self.clear_scene()
