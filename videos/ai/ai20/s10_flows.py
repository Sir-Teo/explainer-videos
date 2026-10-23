from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (AR, DATA, FLOW, NOISE, PART, Plane, digit_sheet, load)


def warp_lines(plane: Plane, L, color=FLOW, stroke_width=1.6, clip=2.95) -> VGroup:
    """Grid lines (k, n, 2) of the plane as polylines (points outside the panel clamped to its edge)."""
    g = VGroup()
    for line in np.asarray(L):
        g.add(VMobject(stroke_color=color, stroke_width=stroke_width).set_points_smoothly(
            plane.pts(np.clip(line, -clip, clip))))
    return g


class Flows(VoiceoverScene):
    def construct(self):
        self.card()
        self.one_d()
        self.coupling()
        self.warp()
        self.replay()
        self.digits()

    def card(self):
        card = chapter_card(9, r"Normalizing flows", r"Can noise be bent into data, invertibly?", lit=(), part=PART)
        with self.voiceover("Chapter nine. Normalizing flows."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def one_d(self):
        g = axes([-3, 3], [0, 0.55], x_length=4.6, y_length=2.0, xlabel=r"$z$", xticks=[-2, 0, 2], center=[-4.0, 1.6, 0])
        zs = np.linspace(-3, 3, 300)
        pz = np.exp(-zs ** 2 / 2) / math.sqrt(2 * math.pi)
        cz = curve(g.ax, zs, pz, NOISE, 3)
        gx = lambda z: z + 0.8 * np.tanh(2 * z) + 0.25 * z ** 2 * np.sign(z) * 0.3
        xs = gx(zs)
        dx = np.gradient(xs, zs)
        px = pz / dx
        h = axes([float(xs.min()), float(xs.max())], [0, float(px.max() * 1.1)], x_length=4.6, y_length=2.0,
                 xlabel=r"$x = g(z)$", xticks=[], center=[-4.0, -1.8, 0])
        cx = curve(h.ax, xs, px, FLOW, 3)
        a, b = 0.35, 0.65
        ia = (zs >= a) & (zs <= b)
        sz = Polygon(*[g.ax.c2p(z, 0) for z in (a, b)], *[g.ax.c2p(z, p) for z, p in zip(zs[ia][::-1], pz[ia][::-1])],
                     stroke_width=0, fill_color=NOISE, fill_opacity=0.5)
        sx = Polygon(*[h.ax.c2p(x, 0) for x in (gx(a), gx(b))], *[h.ax.c2p(x, p) for x, p in zip(xs[ia][::-1],
                                                                                                 px[ia][::-1])],
                     stroke_width=0, fill_color=FLOW, fill_opacity=0.5)
        arr = Arrow(g.get_bottom() + DOWN * 0.05, h.get_top() + UP * 0.05, buff=0.1, color=GREY_B, stroke_width=2.5)
        al = label(r"stretch here, \ thin out here", font_size=20, color=GREY_A).next_to(arr, RIGHT, buff=0.15)
        rows = [
            cmath(r"p_x(x)\, |dx|", r"=", r"p_z(z)\, |dz|", font_size=36),
            cmath(r"p_x(x)", r"=", r"p_z\big(g^{-1}(x)\big)\, \Big|\frac{d g^{-1}}{dx}\Big|", font_size=36),
            cmath(r"\log p_x(x)", r"=", r"\log p_z(f(x))", r"+", r"\log \big|\det J_f(x)\big|", font_size=36),
        ]
        rows[2][4].set_color(FLOW)
        whys = [why(r"probability is conserved"), why(r"in one dimension"),
                why(r"in $d$: \ $f = g^{-1}$, \ its Jacobian's determinant")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=2.9, buff=0.7, edge=6.9)
        tg = note(r"illustrative").to_corner(DR, buff=0.25)
        with self.voiceover(
            "The fourth answer keeps the likelihood exact, and the sampling a single pass. Start from simple noise "
            "z, and push it through an invertible function g. <bookmark mark='a'/> Where g stretches the line, the "
            "probability spreads thin; where it squeezes, it piles up. <bookmark mark='b'/> Probability is "
            "conserved: the mass in a small interval of z equals the mass in its image. <bookmark mark='c'/> So "
            "the density of x is the density of the z that made it, times how much the inverse map shrinks a "
            "small interval. <bookmark mark='d'/> In many dimensions, the factor is the absolute determinant of "
            "the inverse map's Jacobian. The log-likelihood is exact; we can train by maximum likelihood, as for "
            "the autoregressive models. Esteban Tabak and Eric Vanden-Eijnden described flows like this in 2010; "
            "Danilo Rezende and Shakir Mohamed brought them to deep learning in 2015."
        ) as vo:
            self.play(FadeIn(g), Create(cz), FadeIn(tg))
            vo.wait_until("a")
            self.play(GrowArrow(arr), FadeIn(h), Create(cx), FadeIn(al))
            vo.wait_until("b")
            self.play(FadeIn(sz), FadeIn(sx))
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def coupling(self):
        f2 = load("flow2d")
        eqs = VGroup(
            cmath(r"y_{1:k}", r"=", r"x_{1:k}", font_size=34),
            cmath(r"y_{k+1:d}", r"=", r"x_{k+1:d} \odot \exp\big(s(x_{1:k})\big) + t(x_{1:k})", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.0, 2.2, 0])
        n = 6
        cell = 0.5
        mat = VGroup()
        for i in range(n):
            for j in range(n):
                if i < 3 and j < 3:
                    col, txt = (FLOW, "1") if i == j else (None, "0")
                elif i >= 3 and j >= 3:
                    col, txt = (C.BITS, r"e^{s}") if i == j else (None, "0")
                elif i >= 3 and j < 3:
                    col, txt = (GREY_B, r"\ast")
                else:
                    col, txt = (None, "0")
                sq = Square(cell, stroke_color=GREY_D, stroke_width=1, fill_color=col or "#0B0F17",
                            fill_opacity=0.35 if col else 1)
                sq.move_to([j * cell, -i * cell, 0])
                mat.add(VGroup(sq, MathTex(txt, font_size=20, color=WHITE if col else GREY_C).move_to(sq)))
        mat.move_to([-3.0, -1.0, 0])
        ml = label(r"the Jacobian: \ triangular", font_size=22, color=GREY_A).next_to(mat, UP, buff=0.15)
        ld = cmath(r"\log |\det J|", r"=", r"\sum_i s_i(x_{1:k})", font_size=36).move_to([3.2, 1.6, 0])
        ld[2].set_color(C.BITS)
        inv = cmath(r"x_{k+1:d}", r"=", r"\big(y_{k+1:d} - t(y_{1:k})\big) \odot \exp\big(-s(y_{1:k})\big)",
                    font_size=30).move_to([3.2, 0.3, 0])
        il = label(r"and the inverse is just as cheap", font_size=20, color=GREY_A).next_to(inv, DOWN, buff=0.12)
        gap = max(float(f2[f"{n_}_logdet_gap"]) for n_ in ("moons", "ring", "checker"))
        chk = label(rf"checked: \ the sum of the $s$'s against autograd's determinant: \ largest gap "
                    rf"${sci(gap, 1)}$ nats", font_size=20, color=FLOW).move_to([3.0, -1.4, 0])
        if chk.width > 7.4:
            chk.width = 7.4
        hist = label(r"NICE: \ Dinh, Krueger \& Bengio (2014); \ RealNVP: \ Dinh, Sohl-Dickstein \& Bengio (2017)",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The catch is the determinant: for a general d by d Jacobian it costs d cubed operations, and for an "
            "image d is in the thousands. Laurent Dinh, with Yoshua Bengio, found a way around it. Split the "
            "variables in two. <bookmark mark='a'/> Copy the first half unchanged; <bookmark mark='b'/> scale "
            "and shift the second half, by amounts s and t that any network computes from the first half. "
            "<bookmark mark='c'/> The Jacobian is then triangular: the first half doesn't depend on the second. A "
            "triangular matrix's determinant is the product of its diagonal, so the log-determinant is just the "
            "sum of the s's, free. <bookmark mark='d'/> The inverse is as cheap: subtract t, divide by e to the s. "
            "The networks inside never need to be inverted. <bookmark mark='e'/> We checked ours against "
            f"autograd's full determinant: they agree to {sci(gap, 1)} nats. Stack such layers, alternating which "
            "half is copied, and the flow can bend anything."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(mat), FadeIn(ml))
            self.play(Write(ld))
            vo.wait_until("d")
            self.play(Write(inv), FadeIn(il))
            vo.wait_until("e")
            self.play(FadeIn(chk), FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def warp(self):
        f2 = load("flow2d")
        pl = Plane(5.6, center=[-2.6, -0.2, 0])
        W = np.asarray(f2["moons_warp"])  # layers+1, 22 lines, 121, 2
        Pts = np.asarray(f2["moons_warp_pts"])  # layers+1, 800, 2
        n = int(f2["n_layers"])
        lines = [warp_lines(pl, W[k]) for k in range(n + 1)]
        dots = [pl.dots(np.clip(Pts[k][:400], -2.95, 2.95), DATA, radius=0.022) for k in range(n + 1)]
        cnt = [label(rf"after layer ${k}$ of ${n}$" if k else r"the base: \ Gaussian noise", font_size=24,
                     color=FLOW).move_to([3.9, 2.3, 0]) for k in range(n + 1)]
        expl = VGroup(label(r"lines: \ a square grid of the base plane", font_size=20, color=FLOW),
                      label(r"dots: \ samples of the base noise", font_size=20, color=DATA),
                      label(r"each layer moves one coordinate, \\ as a function of the other", font_size=20,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.1, 0.6, 0])
        C2 = np.asarray(f2["checker_warp"])
        CP = np.asarray(f2["checker_warp_pts"])
        cl = warp_lines(pl, C2[-1])
        cd = pl.dots(np.clip(CP[-1][:400], -2.95, 2.95), DATA, radius=0.022)
        cp = label(r"the same flow, \ trained on the checkerboard", font_size=22, color=FLOW).move_to([4.0, -1.6, 0])
        with self.voiceover(
            "Here is that bending, for our flow on the two moons: eight coupling layers. The lines are a square "
            "grid of the noise plane, the dots are samples of the noise. <bookmark mark='a'/> Layer by layer: each "
            "one slides points along one axis, by an amount that depends on where they are along the other. "
            "<bookmark mark='b'/> The grid shears, stretches and folds, without ever tearing or crossing itself, "
            "because every layer is invertible. <bookmark mark='c'/> After the eighth, the noise has become the "
            "moons: one pass from noise to sample, and the same map read backwards gives each point its exact "
            "probability. <bookmark mark='d'/> Trained on the checkerboard instead, the same layers have to cut "
            "the plane into squares, with smooth maps."
        ) as vo:
            self.play(FadeIn(pl), Create(lines[0]), FadeIn(dots[0]), FadeIn(cnt[0]), FadeIn(expl))
            vo.wait_until("a")
            per = max(0.6, vo.until("c") / n)
            cur_l, cur_d, cur_c = lines[0], dots[0], cnt[0]
            for k in range(1, n + 1):
                self.play(Transform(cur_l, lines[k]), Transform(cur_d, dots[k]), ReplacementTransform(cur_c, cnt[k]),
                          run_time=0.75 * per)
                cur_c = cnt[k]
                self.wait(0.25 * per)
            vo.wait_until("d")
            self.play(Transform(cur_l, cl), Transform(cur_d, cd), FadeIn(cp), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        f2, t = load("flow2d"), load("toys")
        pl = Plane(4.0, center=[-3.6, 0.2, 0])
        frames = np.asarray(f2["checker_frames"])
        steps = list(f2["checker_frame_steps"])
        imgs = [pl.image(fr, FLOW) for fr in frames]
        truth = pl.image(t["checker_density"], DATA).scale(0.5).next_to(pl, DOWN, buff=0.15).align_to(pl, LEFT)
        tl = label(r"the truth", font_size=18, color=DATA).next_to(truth, RIGHT, buff=0.1)
        cap = [label(rf"step ${s:,}$".replace(",", "{,}"), font_size=22, color=FLOW).next_to(pl, UP, buff=0.12)
               for s in steps]
        rows = VGroup()
        names = {"moons": r"two moons", "ring": r"ring of eight", "checker": r"checkerboard"}
        gaps = {}
        for n_ in ("moons", "ring", "checker"):
            nll = float(np.asarray(f2[f"{n_}_curve"])[-1, 1])
            h = float(t[f"{n_}_entropy"])
            gaps[n_] = nll - h
            rows.add(VGroup(label(names[n_], font_size=24, color=DATA),
                            MathTex(rf"{nll:.2f}", font_size=30, color=FLOW),
                            MathTex(rf"{h:.2f}", font_size=30, color=DATA),
                            MathTex(rf"{nll - h:+.2f}", font_size=30, color=C.SURPRISE)))
        head = VGroup(label(r"", font_size=20), label(r"held-out NLL", font_size=20, color=FLOW),
                      label(r"the floor $h(p)$", font_size=20, color=DATA), label(r"gap", font_size=20,
                                                                                  color=C.SURPRISE))
        tab = VGroup(head, *rows)
        for r in tab:
            for j, m in enumerate(r):
                m.move_to([1.3 + [0, 2.2, 4.0, 5.6][j], 0, 0])
        for i, r in enumerate(tab):
            r.shift(UP * (1.2 - 0.62 * i))
        for r in rows:
            r[0].align_to(rows[0][0], RIGHT)
        worst = max(gaps, key=gaps.get)
        if worst == "ring":
            why_hard = ("The ring is the hardest: an invertible map can't tear one blob of noise into eight separate "
                        "islands, so it stretches thin bridges of probability between them.")
        elif worst == "checker":
            why_hard = ("The checkerboard is the hardest: a stack of smooth invertible maps can only approximate its "
                        "cliffs.")
        else:
            why_hard = "The moons are the hardest of the three for it."
        with self.voiceover(
            "Training, replayed on the checkerboard: the flow's density at each checkpoint. <bookmark mark='a'/> "
            "Mass flows out of the empty squares and into the filled ones, and the edges slowly sharpen. "
            "<bookmark mark='b'/> On held-out points, against each density's floor, the flow's surprise ends "
            f"{gaps['moons']:.2f} nats above it on the moons, {gaps['ring']:.2f} on the ring, and "
            f"{gaps['checker']:.2f} on the checkerboard. " + why_hard
        ) as vo:
            self.play(FadeIn(pl), FadeIn(imgs[0]), FadeIn(cap[0]), FadeIn(truth), FadeIn(tl))
            cur, cc = imgs[0], cap[0]
            per = max(0.4, vo.until("b") / max(1, len(imgs) - 1))
            for k in range(1, len(imgs)):
                self.play(FadeTransform(cur, imgs[k]), ReplacementTransform(cc, cap[k]), run_time=0.7 * per)
                cur, cc = imgs[k], cap[k]
                self.wait(0.3 * per)
            vo.wait_until("b")
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def digits(self):
        fl, pc = load("flow"), load("pixelcnn")
        s1 = digit_sheet(np.asarray(fl["s0_show"])[:24], 3, 8, size=0.48, gap=0.04).move_to([-3.3, 1.4, 0])
        s2 = digit_sheet(np.asarray(fl["s0_show_cold"])[:24], 3, 8, size=0.48, gap=0.04).move_to([-3.3, -1.4, 0])
        l1 = label(r"our RealNVP on digits: \ noise at temperature $1$", font_size=20, color=FLOW).next_to(s1, UP,
                                                                                                         buff=0.1)
        l2 = label(r"temperature $0.7$: \ the noise scaled down", font_size=20, color=FLOW).next_to(s2, UP, buff=0.1)
        b_f = [float(fl[f"s{s}_bpp"]) for s in (0, 1, 2)]
        b_p = [float(pc[f"s{s}_bpp"]) for s in (0, 1, 2)]
        cmp_ = VGroup(
            label(rf"RealNVP: \ ${np.mean(b_f):.2f}$ bits per pixel \ (${min(b_f):.2f}$--${max(b_f):.2f}$)",
                  font_size=22, color=FLOW),
            label(rf"PixelCNN: \ ${np.mean(b_p):.2f}$ \ (${min(b_p):.2f}$--${max(b_p):.2f}$)", font_size=22,
                  color=AR),
            label(r"three seeds each, \ the same budget", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, 1.9, 0])
        hist = VGroup(
            history_card(2018, r"Kingma \& Dhariwal: \ Glow", r"invertible $1 \times 1$ convolutions; \ faces at "
                         r"$256^2$", width=4.6, font_size=18),
            history_card(2024, r"Zhai et al.: \ TarFlow", r"Transformer autoregressive flows on image patches: \ "
                         r"samples comparable to diffusion", width=4.6, font_size=18),
        ).arrange(DOWN, buff=0.2).move_to([3.5, -1.3, 0])
        better = np.mean(b_p) < np.mean(b_f)
        verdict = (f"In bits per pixel the flow gets {np.mean(b_f):.2f} on held-out digits, against "
                   f"{np.mean(b_p):.2f} for the PixelCNN on the same budget: "
                   + ("an exact likelihood, but a worse one; coupling layers spend capacity on staying invertible."
                      if better else "a better likelihood than the autoregressive model."))
        with self.voiceover(
            "On digits, our flow is eight coupling layers on the logits of the pixels, and here is what it draws. "
            "<bookmark mark='a'/> Strokes, but noisy ones. Turning the noise down, a trick from OpenAI's Glow, "
            "makes them cleaner and more alike: the flows' version of truncation. <bookmark mark='b'/> "
            f"{verdict} <bookmark mark='c'/> Glow, in 2018, made flows that drew faces; then, for years, flows "
            "trailed the other families. In 2024 Shuangfei Zhai and colleagues at Apple built one from transformer "
            "blocks over image patches, and reported samples comparable to diffusion models: the first time for "
            "a flow on its own. And the continuous version of a flow, next chapter, is what flow matching trains "
            "in Part 21."
        ) as vo:
            self.play(FadeIn(s1), FadeIn(l1))
            vo.wait_until("a")
            self.play(FadeIn(s2), FadeIn(l2))
            vo.wait_until("b")
            self.play(FadeIn(cmp_, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(h_, shift=UP * 0.1) for h_ in hist], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()
