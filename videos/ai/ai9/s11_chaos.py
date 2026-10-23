from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import CHAOS, CRIT, ORDER, PART, WEIGHT, load, rgb_of

SETS = (("ordered", ORDER), ("critical", CRIT), ("chaotic", CHAOS))


def cobweb(ax, xs, fx, x0, n, color, stroke_width=2.5):
    """The iteration x -> f(x) drawn as a staircase between the curve and the diagonal."""
    pts = [ax.c2p(x0, 0)]
    x = x0
    for _ in range(n):
        y = float(np.interp(x, xs, fx))
        pts += [ax.c2p(x, y), ax.c2p(y, y)]
        x = y
    return VMobject(color=color, stroke_width=stroke_width).set_points_as_corners(pts)


def chi_image(chi, width, height) -> ImageMobject:
    """chi_1 as colour: blue below 1 (ordered), pink above (chaotic), dark at the edge."""
    t = np.clip((np.asarray(chi) - 1.0) / 0.6, -1, 1)
    mid, a, b = rgb_of("#141A24"), rgb_of(ORDER), rgb_of(CHAOS)
    rgb = np.where(t[..., None] >= 0, mid + (b - mid) * t[..., None], mid + (a - mid) * (-t[..., None]))
    img = ImageMobject((np.concatenate([rgb, np.ones(t.shape + (1,))], -1)[::-1] * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


class Chaos(VoiceoverScene):
    def construct(self):
        self.card()
        self.lengths()
        self.correlations()
        self.phase()
        self.trainable()

    def card(self):
        card = chapter_card(10, r"The edge of chaos", r"Why is there one right size?", part=PART)
        with self.voiceover("Chapter ten. The edge of chaos."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lengths(self):
        m = load("meanfield")
        qs = np.asarray(m["qs"])
        sb2 = float(m["sb2"])
        g = axes([0, 3], [0, 3], x_length=5.0, y_length=4.4, xlabel=r"$q_{l-1}$", ylabel=r"$q_l$",
                 xticks=[0, 1, 2, 3], yticks=[1, 2, 3], center=[-3.2, -0.6, 0])
        ax = g.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(3, 3), color=GREY_B, stroke_width=2, dash_length=0.08)
        qm = np.asarray(m["qmap_critical"])
        cq = curve(ax, qs, np.minimum(qm, 3), CRIT, 4)
        web = cobweb(ax, qs, qm, 2.8, 8, WHITE, 2)
        qstar = float(m["qstar_critical"])
        star = glow_dot(ax.c2p(qstar, qstar), color=CRIT, radius=0.08)
        sl = MathTex(rf"q^* = {qstar:.2f}", font_size=30, color=CRIT).next_to(star, DR, buff=0.15)
        colors = {r"\sigma_w^2": WEIGHT, r"\sigma_b^2": GREY_A}
        eq = cmath(r"q_l", r"=", r"\sigma_w^2", r"\, \mathbb{E}_{z \sim N(0,1)}\big[\tanh(\sqrt{q_{l-1}}\, z)^2\big] + ",
                   r"\sigma_b^2", font_size=32, colors=colors).move_to([3.3, 2.4, 0])
        defs = label(r"$q_l$: \ the variance of layer $l$'s sums; \\ $\sigma_w^2/n$, \ $\sigma_b^2$: \ the variances of "
                     r"the random weights and biases", font_size=22, color=GREY_A).next_to(eq, DOWN, buff=0.25)
        idea = label(r"very wide: \ each sum is a Gaussian, \\ and one number per layer describes it", font_size=24,
                     color=GREY_A).move_to([3.3, -0.4, 0])
        sets = label(rf"here \ $\sigma_w^2 = {m['sets']['critical']:.2f}$, \ $\sigma_b^2 = {sb2:g}$", font_size=24,
                     color=CRIT).move_to([3.3, -1.5, 0])
        cite_ = cite(r"B.~Poole et al.\ (2016); \ S.~S.~Schoenholz, J.~Gilmer, S.~Ganguli \& J.~Sohl-Dickstein (2017)",
                     corner=DR)
        # a very wide layer feeding the next: every sum adds up many random terms, so it is Gaussian
        gw = np.random.default_rng(17)  # the drawing's random wiring (schematic)
        lo_row = VGroup(*[Dot([-5.9 + 0.19 * i, -1.6, 0], radius=0.05, color=GREY_B) for i in range(32)])
        hi_row = VGroup(*[Dot([-5.9 + 0.19 * i, 0.9, 0], radius=0.05, color=CRIT) for i in range(32)])
        wires = VGroup(*[Line(lo_row[int(i)].get_center(), hi_row[int(j)].get_center(), stroke_width=0.6, color=GREY_D,
                              stroke_opacity=0.6) for i, j in gw.integers(0, 32, (220, 2))])
        bell = FunctionGraph(lambda t_: 1.1 * np.exp(-0.5 * (t_ / 0.42) ** 2), x_range=[-1.4, 1.4], color=CRIT,
                             stroke_width=4).shift([-2.95, 1.2, 0])
        bell_base = Line([-4.45, 1.2, 0], [-1.45, 1.2, 0], color=GREY_C, stroke_width=1.5)
        bl = label(r"each sum: \ a Gaussian, \ variance $q_l$", font_size=26, color=CRIT).next_to(bell, UP, buff=0.1)
        wide_tag = note(r"schematic").next_to(lo_row, DOWN, buff=0.15).align_to(lo_row, LEFT)
        wide = VGroup(lo_row, hi_row, wires, bell, bell_base, bl, wide_tag)
        with self.voiceover(
            "Why is there one right size? In 2016 and 2017 Ben Poole, Sam Schoenholz, Surya Ganguli, Jascha "
            "Sohl-Dickstein and colleagues answered with physics: mean-field theory. <bookmark mark='a'/> Make the "
            "network very wide. Then each unit's weighted sum, over random weights, is a Gaussian, and a single "
            "number describes a whole layer: the variance of its sums, q. <bookmark mark='b'/> One layer maps q to "
            "the next: square the tanh, average over the Gaussian, scale by the weight variance, add the bias "
            "variance. <bookmark mark='c'/> Plot that map against the diagonal, and iterate it: the staircase "
            f"converges to a fixed point, here q star equals {qstar:.2f}. Lengths settle down within a few layers, "
            "whatever the input. The interesting question is what happens to two inputs."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(lo_row), FadeIn(hi_row), Create(wires), FadeIn(wide_tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(idea), Create(bell_base), Create(bell), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeOut(wide), Write(eq), FadeIn(defs))
            self.play(FadeIn(g), Create(diag), Create(cq), FadeIn(sets))
            vo.wait_until("c")
            self.play(Create(web), run_time=3.0)
            self.play(FadeIn(star), FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def correlations(self):
        m = load("meanfield")
        cs = np.asarray(m["cs"])
        g = axes([0, 1], [0, 1], x_length=4.2, y_length=4.2, xlabel=r"correlation, \ layer $l - 1$",
                 ylabel=r"layer $l$", xticks=[0, 1], yticks=[1], center=[-4.4, -0.5, 0], font_size=18)
        ax = g.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_B, stroke_width=2, dash_length=0.06)
        maps = {k: curve(ax, cs, np.asarray(m[f"cmap_{k}"]), c, 3.5) for k, c in SETS}
        L = len(np.asarray(m["csim_ordered"])) - 1
        g2 = axes([0, L], [0, 1], x_length=5.4, y_length=4.2, xlabel=r"layer",
                  ylabel=r"correlation of two inputs", xticks=[0, 20, 40, 60], yticks=[0, 0.5, 1], center=[2.6, -0.5, 0],
                  font_size=18)
        ax2 = g2.ax
        mf = {k: curve(ax2, np.arange(len(m[f"ctraj_{k}"])), np.asarray(m[f"ctraj_{k}"]), c, 3) for k, c in SETS}
        sim = {k: VGroup(*[Dot(ax2.c2p(i, v), radius=0.035, color=c) for i, v in enumerate(np.asarray(m[f"csim_{k}"]))
                           if i % 2 == 0]) for k, c in SETS}
        chi = {k: float(m[f"chi_{k}"]) for k, _ in SETS}
        sw = {k: float(v) for k, v in m["sets"].items()}
        lg = legend([(c, rf"\textrm{{{k}}}: \ $\sigma_w^2 = {sw[k]:.2f}$, \ $\chi_1 = {chi[k]:.2f}$") for k, c in SETS],
                    font_size=20).next_to(g2, UP, buff=0.25).align_to(g2, LEFT)
        key = label(r"lines: \ mean-field theory; \ dots: \ a real network of width $1{,}000$", font_size=20,
                    color=GREY_A).to_edge(DOWN, buff=0.25)
        chi_eq = cmath(r"\chi_1", r"=", r"\sigma_w^2\, \mathbb{E}\big[\tanh'(\sqrt{q^*} z)^2\big]", font_size=30,
                       colors={r"\chi_1": CRIT}).to_edge(UP, buff=0.3).shift(LEFT * 3.0)
        chi_l = label(r"the slope of the map at $c = 1$", font_size=22, color=GREY_A).next_to(chi_eq, RIGHT, buff=0.3)
        ends = {k: float(np.asarray(m[f"ctraj_{k}"])[-1]) for k, _ in SETS}
        survive = (f"After {L} layers, their correlation is only {ends['critical']:.2f}: the two inputs are still told "
                   "apart. " if ends["critical"] < 0.99 else f"Even here, after {L} layers, they have nearly merged. ")
        with self.voiceover(
            "Send two different inputs through, and follow their correlation, c, layer by layer. Identical inputs "
            "stay identical, so c equals one is always a fixed point. Whether it attracts or repels depends on the "
            "map's slope there, called chi one. <bookmark mark='a'/> With small weights, chi one is "
            f"{chi['ordered']:.2f}, less than one: the ordered phase. Every pair of inputs is pulled together, "
            "until the network gives every input the same output. <bookmark mark='b'/> With big weights, chi one is "
            f"{chi['chaotic']:.2f}: the chaotic phase. Nearby inputs are pushed apart, to a correlation of "
            f"{ends['chaotic']:.2f}, and the network scrambles everything it sees. <bookmark mark='c'/> In between, "
            "chi one equals one exactly: the edge of chaos, where correlations change slowly and information about "
            "the input survives the trip. " + survive + 
            "<bookmark mark='d'/> The dots are a real network of width a thousand, and the theory tracks it. And chi "
            "one is also the factor that scales the gradient, layer by layer, on the way back: below one it "
            "vanishes, above one it explodes, as you just saw."
        ) as vo:
            self.play(Write(chi_eq), FadeIn(chi_l), FadeIn(g), Create(diag), FadeIn(g2))
            for mk, (k, c) in zip("abc", (SETS[0], SETS[2], SETS[1])):
                vo.wait_until(mk)
                self.play(Create(maps[k]), Create(mf[k]), FadeIn(lg[[s for s, _ in SETS].index(k)]), run_time=1.6)
            vo.wait_until("d")
            self.play(*[LaggedStart(*[FadeIn(dt) for dt in sim[k]], lag_ratio=0.03) for k, _ in SETS], FadeIn(key),
                      run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def phase(self):
        m = load("meanfield")
        sw, sb, chi = np.asarray(m["phase_sw"]), np.asarray(m["phase_sb"]), np.asarray(m["phase_chi"])
        g = axes([sw[0], sw[-1]], [sb[0], sb[-1]], x_length=7.0, y_length=4.6, xlabel=r"$\sigma_w^2$ \ (weights)",
                 ylabel=r"$\sigma_b^2$ \ (biases)", xticks=[1, 2, 3, 4], yticks=[0, 0.25, 0.5], center=[-1.6, -0.4, 0])
        ax = g.ax
        img = chi_image(chi, ax.x_length if hasattr(ax, "x_length") else 7.0, 4.6)
        img.stretch_to_fit_width(abs(ax.c2p(sw[-1], 0)[0] - ax.c2p(sw[0], 0)[0]))
        img.stretch_to_fit_height(abs(ax.c2p(0, sb[-1])[1] - ax.c2p(0, sb[0])[1]))
        img.move_to(ax.c2p((sw[0] + sw[-1]) / 2, (sb[0] + sb[-1]) / 2))
        crit = curve(ax, np.asarray(m["crit_sw"]), sb, CRIT, 4)
        lab = VGroup(label(r"ordered", font_size=30, color=ORDER).move_to(ax.c2p(1.1, 0.38)),
                     label(r"chaotic", font_size=30, color=CHAOS).move_to(ax.c2p(3.5, 0.1)),
                     label(r"$\chi_1 = 1$", font_size=26, color=CRIT).next_to(ax.c2p(2.84, 0.5), DR, buff=0.08))
        sb2 = float(m["sb2"])
        marks = VGroup(*[Dot(ax.c2p(float(m["sets"][k]), sb2), radius=0.08, color=c, stroke_color=WHITE, stroke_width=1.5)
                         for k, c in SETS])
        x0 = float(np.asarray(m["crit_sw"])[0])
        glo = Dot(ax.c2p(x0, 0), radius=0.11, color=WHITE)
        gl = label(rf"$\sigma_b = 0$: \ the edge is at $\sigma_w^2 = {x0:.2f}$, \\ Glorot's $\operatorname{{Var}}(W) = 1/n$",
                   font_size=24, color=WHITE).move_to([4.6, 1.4, 0])
        relu = label(r"ReLU: \ $\chi_1 = \sigma_w^2 / 2$, \\ so the edge is at $\sigma_w^2 = 2$: \ He's $2/n$", font_size=24,
                     color=C.BITS).move_to([4.6, -0.3, 0])
        tag = note(r"computed: \ $\chi_1$ for tanh, \ mean-field theory").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here is the whole picture for tanh networks: chi one, for every spread of the weights and of the biases. "
            "Blue is order, pink is chaos, <bookmark mark='a'/> and the yellow line between them is the edge. "
            "<bookmark mark='b'/> Now look where it meets the bottom, where the biases are zero: at a weight "
            f"variance of {x0:.2f} over n. That's exactly Glorot's rule from the last chapter. "
            "<bookmark mark='c'/> For ReLU units the same calculation gives chi one equals sigma w squared over two, "
            "so the edge sits at two over n: He's rule. The initialization rules weren't just tidy bookkeeping. "
            "They put the network on the edge of chaos."
        ) as vo:
            self.play(FadeIn(g), FadeIn(img), FadeIn(tag), FadeIn(lab[:2]))
            self.bring_to_front(g)
            vo.wait_until("a")
            self.play(Create(crit), FadeIn(lab[2]), FadeIn(marks))
            vo.wait_until("b")
            self.play(FadeIn(glo, scale=2), FadeIn(gl))
            vo.wait_until("c")
            self.play(FadeIn(relu))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trainable(self):
        m = load("meanfield")
        t = load("trainable")
        sws, depths, acc = np.asarray(t["sws"]), np.asarray(t["depths"]), np.asarray(t["acc"])
        xi = np.asarray(t["xi"])
        K = int(t["classes"])
        W, H = 6.4, 4.4
        g = axes([0, len(sws)], [0, len(depths)], x_length=W, y_length=H, ylabel=r"depth", center=[-2.0, -0.5, 0])
        ax = g.ax
        cells = VGroup()
        for i, L in enumerate(depths):
            for j, a in enumerate(sws):
                v = float(acc[i, j])
                col = interpolate_color(ManimColor("#141A24"), ManimColor(C.BITS), float(np.clip((v - 1 / K) / (1 - 1 / K), 0, 1)))
                cells.add(Rectangle(width=W / len(sws), height=H / len(depths), stroke_width=0.5, stroke_color=BACKGROUND,
                                    fill_color=col, fill_opacity=1).move_to(ax.c2p(j + 0.5, i + 0.5)))
        xt = VGroup(*[MathTex(f"{a:.1f}", font_size=18, color=GREY_B).next_to(ax.c2p(j + 0.5, 0), DOWN, buff=0.1)
                      for j, a in enumerate(sws) if j % 2 == 0])
        yt = VGroup(*[MathTex(str(L), font_size=18, color=GREY_B).next_to(ax.c2p(0, i + 0.5), LEFT, buff=0.1)
                      for i, L in enumerate(depths)])
        xt.add(label(r"$\sigma_w^2$", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.42))

        def depth_index(Lval):  # depth -> the heatmap's row coordinate (piecewise linear between rows)
            return float(np.interp(Lval, depths, np.arange(len(depths)) + 0.5))

        six = []
        for j, a in enumerate(sws):
            y = 6 * xi[j]
            six.append(ax.c2p(j + 0.5, depth_index(min(y, depths[-1] * 1.5)) if y <= depths[-1] else len(depths)))
        six_line = VMobject(color=WHITE, stroke_width=3).set_points_as_corners(six)
        six_l = label(r"$6\,\xi_c$", font_size=26, color=WHITE).next_to(six[0], UR, buff=0.1)
        key = label(rf"training accuracy after ${t['steps']}$ steps \\ (dark: \ chance, $1/{K}$; \ bright: \ $100\%$)",
                    font_size=22, color=GREY_A).move_to([4.5, 1.8, 0])
        xi_eq = cmath(r"\xi_c", r"=", r"-1 / \ln \chi_c", font_size=32).move_to([4.5, 0.4, 0])
        xi_l = label(r"how many layers a correlation survives; \\ infinite at the edge", font_size=22, color=GREY_A)
        xi_l.next_to(xi_eq, DOWN, buff=0.15)
        tag = note(rf"computed: \ tanh nets of width ${t['width']}$, \ ${K}$ classes in ${t['dim']}$ dimensions").to_corner(DR, buff=0.2)
        inside = np.array([[L <= 6 * x for x in xi] for L in depths])
        ok = acc > 0.5
        agree = float((inside == ok).mean())
        rows_ok = [i for i in range(len(depths)) if ok[i].any()]
        i_deep = rows_ok[-1] if rows_ok else 0
        L_deep = int(depths[i_deep])
        deep_ok = [float(sws[j]) for j in range(len(sws)) if ok[i_deep, j]]
        verdict = (f"The bright region hugs the line: on {100 * agree:.0f} percent of the grid, the rule 'trainable "
                   "exactly when the depth is below six depth scales' predicts our result."
                   if agree >= 0.75 else
                   f"The rule of thumb agrees with our result on {100 * agree:.0f} percent of the grid: our runs are "
                   "shorter and smaller than theirs, so the boundary is rougher.")
        deep_list = ", ".join(f"{v:.1f}" for v in deep_ok)
        if i_deep == len(depths) - 1:
            deepest = f"At {L_deep} layers, only weight variances near the edge train: {deep_list}."
        else:
            deepest = (f"At {L_deep} layers, only weight variances near the edge still train: {deep_list}; at "
                       f"{depths[-1]}, none does in {t['steps']} steps.")
        xs_m, xi_m = np.asarray(m["xi_sw"]), np.asarray(m["xi"])
        g0 = axes([0.6, 4.0], [0, 100], x_length=6.4, y_length=4.2, xlabel=r"$\sigma_w^2$",
                  ylabel=r"depth scale $\xi_c$ \ (layers)", xticks=[1, 2, 3, 4], yticks=[0, 50, 100], center=[-2.0, -0.4, 0])
        xi_curve = curve(g0.ax, xs_m, np.minimum(xi_m, 100), CRIT, 4)
        edge_l = label(r"the edge: \ $\xi_c \to \infty$", font_size=26, color=CRIT).next_to(
            g0.ax.c2p(float(m["sw_crit"]), 100), RIGHT, buff=0.15)
        xi_tag = note(r"computed: \ mean-field theory, \ $\sigma_b^2 = " + f"{float(m['sb2']):g}" + r"$").next_to(
            g0, DOWN, buff=0.1).align_to(g0, RIGHT)
        with self.voiceover(
            "How deep can a network be and still train? The theory gives a depth scale, xi c: how many layers a "
            "correlation survives before it's forgotten. It's infinite exactly at the edge. "
            "<bookmark mark='a'/> Schoenholz and colleagues found that networks train when they're shallower than "
            "about six depth scales. We tried it: tanh networks from five to a hundred layers deep, at twelve weight "
            "variances, each trained the same way on the same small task. <bookmark mark='b'/> Bright means it "
            "learned; dark means it stayed at chance. <bookmark mark='c'/> " + verdict + " <bookmark mark='c2'/> " + deepest +
            " <bookmark mark='d'/> Pushed further, the idea trained convolutional networks ten thousand layers deep "
            "in 2018, with nothing but a careful initialization. Part 12 returns to it, for transformers."
        ) as vo:
            self.play(FadeIn(xi_eq), FadeIn(xi_l), FadeIn(g0), FadeIn(xi_tag))
            self.play(Create(xi_curve), FadeIn(edge_l), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeOut(g0), FadeOut(xi_curve), FadeOut(edge_l), FadeOut(xi_tag))
            self.play(FadeIn(g), FadeIn(xt), FadeIn(yt), FadeIn(tag))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.005), FadeIn(key), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(six_line), FadeIn(six_l), run_time=1.5)
            vo.wait_until("d")
            self.play(Indicate(six_line, color=CRIT))
        self.wait(0.3)
        self.clear_scene()
