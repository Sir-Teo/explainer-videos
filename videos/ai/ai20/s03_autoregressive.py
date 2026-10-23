from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (crossfade, AR, DATA, GAN_C, PART, Plane, digit_rgb, digit_sheet, load, rgb_of, to_image)


def pixel_grid(side=0.3, gap=0.03, color=GREY_D) -> VGroup:
    g = VGroup(*[Square(side, stroke_color=color, stroke_width=1, fill_color="#0B0F17", fill_opacity=1)
                 for _ in range(196)])
    g.arrange_in_grid(14, 14, buff=gap)
    return g


def level_color(v: float) -> ManimColor:
    a = float(v) / 15.0
    c = rgb_of("#0B0F17") * (1 - a) + np.ones(3) * a
    return ManimColor(c)


class Autoregressive(VoiceoverScene):
    def construct(self):
        self.card()
        self.chain()
        self.plane()
        self.images()
        self.blind()
        self.replay()
        self.drawing()

    def card(self):
        card = chapter_card(2, r"One pixel at a time", r"Can a model write an image the way it writes a sentence?",
                            lit=(1948,), part=PART)
        with self.voiceover("Chapter two. One pixel at a time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def chain(self):
        f = cmath(r"p(x_1, \dots, x_n)", r"=", r"p(x_1)", r"\,", r"p(x_2 \mid x_1)", r"\,",
                  r"p(x_3 \mid x_1, x_2)", r"\cdots", r"p(x_n \mid x_{<n})", font_size=40).move_to(UP * 2.2)
        for i in (2, 4, 6, 8):
            f[i].set_color(AR)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=0.9, height=0.7, corner_radius=0.1, stroke_color=AR,
                                                 stroke_width=2), MathTex(rf"x_{{{k}}}", font_size=32))
                         for k in range(1, 7)])
        for b in boxes:
            b[1].move_to(b[0])
        boxes.arrange(RIGHT, buff=0.5).move_to(DOWN * 0.1)
        arcs = VGroup()
        for j in range(1, 6):
            for i in range(j):
                if j - i <= 2:
                    arcs.add(CurvedArrow(boxes[i].get_top() + UP * 0.05, boxes[j].get_top() + UP * 0.05,
                                         angle=-0.9 if j - i == 1 else -1.1, color=AR, stroke_width=2,
                                         tip_length=0.14).set_opacity(0.8))
        ex = VGroup(label(r"Shannon (1948): \ English, letter by letter", font_size=24, color=GREY_A),
                    label(r"Part 1's language models: \ token by token", font_size=24, color=GREY_A),
                    label(r"here: \ a digit, \ pixel by pixel", font_size=24, color=AR))
        ex.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(DOWN * 2.3)
        with self.voiceover(
            "The first answer needs no new mathematics. Any distribution factors by the chain rule: <bookmark "
            "mark='a'/> the first variable, times the second given the first, times the third given the first two, "
            "and so on. <bookmark mark='b'/> Each factor is one prediction: the next variable, given everything "
            "before it. Learn every factor and you have the distribution exactly; sample them in order and you "
            "have a sample. <bookmark mark='c'/> Shannon's English, every language model in this series, and now a "
            "digit."
        ) as vo:
            self.play(Write(f[:2]))
            vo.wait_until("a")
            self.play(Write(f[2:]), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.12),
                      LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.1), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.1) for e in ex], lag_ratio=0.5), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plane(self):
        a, t = load("ar2d"), load("toys")
        xs = np.asarray(a["xs"])
        pl = Plane(4.2, center=[-3.4, 0.35, 0])
        truth = pl.image(t["moons_density"], DATA)
        truth.set_opacity(0.35)
        # p(x1) along the bottom edge, p(x2 | x1) as vertical slices
        m1 = np.asarray(a["moons_x1"])
        base_y = pl.frame.get_bottom()[1] - 0.12
        sc = 0.9 / m1.max()
        marg = VMobject(stroke_color=AR, stroke_width=3).set_points_smoothly(
            [[pl.p(x, 0)[0], base_y - v * sc, 0] for x, v in zip(xs[::3], m1[::3])])
        ml = MathTex(r"p(x_1)", font_size=30, color=AR).next_to(marg, LEFT, buff=0.15).shift(DOWN * 0.2)
        cuts = list(a["moons_cuts"])
        slices, lines_ = VGroup(), VGroup()
        cond = np.asarray(a["moons_cond"])
        for c, cd in zip(cuts, cond):
            x0 = pl.p(c, 0)[0]
            s2 = 0.75 / cd.max()
            keep = np.abs(xs) <= 3.0
            slices.add(VMobject(stroke_color=C.MODEL_Q, stroke_width=3).set_points_smoothly(
                [[x0 + v * s2, pl.p(0, y)[1], 0] for y, v in zip(xs[keep][::2], cd[keep][::2])]))
            lines_.add(DashedLine(pl.p(c, -3), pl.p(c, 3), color=GREY_B, stroke_width=1.5, dash_length=0.08))
        cl = MathTex(r"p(x_2 \mid x_1)", font_size=30, color=C.MODEL_Q).next_to(pl, UP, buff=0.12).shift(RIGHT * 0.8)
        frames = np.asarray(a["moons_frames"])
        steps = list(a["moons_frame_steps"])
        curve_ = np.asarray(a["moons_curve"])
        h = float(t["moons_entropy"])
        top = math.ceil(curve_[:, 1].max() * 2) / 2
        g = axes([0, steps[-1]], [h - 0.3, top], x_length=4.6, y_length=3.0, xlabel=r"training step",
                 ylabel=r"held-out NLL (nats)", xticks=[0, steps[-1]], yticks=[round(h, 2), top],
                 center=[3.6, 0.2, 0])
        floor_ = DashedLine(g.ax.c2p(0, h), g.ax.c2p(steps[-1], h), color=DATA, stroke_width=2)
        fl = label(r"the floor, \ $h(p)$", font_size=20, color=DATA).next_to(floor_, UP, buff=0.06).align_to(floor_,
                                                                                                         RIGHT)
        dots_ = VGroup(*[Dot(g.ax.c2p(s, v), radius=0.05, color=AR) for s, v in curve_])
        line_ = curve(g.ax, curve_[:, 0], curve_[:, 1], AR, 3)
        imgs = [pl.image(fr, AR) for fr in frames]
        mlp = note(r"each factor: \ a mixture of $10$ Gaussians, \ set by a small network").next_to(pl, DOWN, buff=1.2)
        final = float(curve_[-1, 1])
        gap = final - h
        verdict = (f"It ends {gap:.2f} nats above the floor: close to the best any model could do."
                   if gap < 0.1 else f"It ends {gap:.2f} nats above the floor: the shape is right, the edges still "
                   "a little soft.")
        tg = note(rf"computed: \ ${a['params']:,}$ parameters".replace(",", "{,}")).to_corner(DR, buff=0.25)
        with self.voiceover(
            "In the plane, the first factor, p of x one, is a curve along the bottom. <bookmark mark='a'/> The "
            "second, p of x two given x one, is a different curve for every slice: a mixture of ten Gaussians set "
            "by a small network fed x one. <bookmark mark='b'/> Multiply the two: the density the model learns, "
            f"replayed through training, beside its held-out surprise. <bookmark mark='c'/> {verdict}"
        ) as vo:
            self.play(FadeIn(pl), FadeIn(truth), Create(marg), FadeIn(ml), FadeIn(mlp), FadeIn(tg))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Create(l_), Create(s_)) for l_, s_ in zip(lines_, slices)],
                                  lag_ratio=0.4), FadeIn(cl), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeOut(truth), FadeOut(lines_), FadeOut(slices), FadeOut(cl), FadeOut(marg), FadeOut(ml),
                      FadeIn(imgs[0]), FadeIn(g), Create(floor_), FadeIn(fl), FadeIn(dots_[0]))
            cur = imgs[0]
            per = max(0.35, (vo.until("c") - 1.0) / max(1, len(imgs) - 1))
            for k in range(1, len(imgs)):
                self.play(crossfade(cur, imgs[k]), FadeIn(dots_[k]), run_time=per)
                cur = imgs[k]
            self.play(Create(line_), run_time=0.8)
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def images(self):
        grid = pixel_grid(0.28, 0.03).move_to([-3.6, -0.1, 0])
        k0 = 6 * 14 + 8
        ctx = VGroup(*[grid[i].copy().set_fill(AR, opacity=0.35) for i in range(k0)])
        cur = grid[k0].copy().set_fill(C.MODEL_Q, opacity=0.9)
        order = VGroup(*[Arrow(grid[r * 14].get_left() + LEFT * 0.25, grid[r * 14 + 13].get_right() + RIGHT * 0.05,
                               buff=0, color=GREY_C, stroke_width=1.2, max_tip_length_to_length_ratio=0.03)
                         for r in range(0, 14, 3)])
        kern = VGroup()
        for r in range(3):
            for c in range(3):
                on = r < 1 or (r == 1 and c < 1)
                sq = Square(0.55, stroke_color=GREY_B, stroke_width=1.5, fill_color=AR if on else "#0B0F17",
                            fill_opacity=0.6 if on else 1)
                kern.add(sq)
        kern.arrange_in_grid(3, 3, buff=0.05).move_to([2.4, 1.6, 0])
        kern[4].set_fill(C.MODEL_Q, opacity=0.9)
        kz = VGroup(*[MathTex(r"0", font_size=26, color=GREY_B).move_to(kern[i]) for i in (5, 6, 7, 8)])
        kl = label(r"a masked $3 \times 3$ filter: \\ the future is zeroed", font_size=22, color=GREY_A)
        kl.next_to(kern, RIGHT, buff=0.35)
        hist = VGroup(
            label(r"NADE \ (Larochelle \& Murray, 2011)", font_size=22, color=GREY_A),
            label(r"MADE: \ masked networks \ (Germain et al., 2015)", font_size=22, color=GREY_A),
            label(r"PixelRNN and PixelCNN \ (van den Oord et al., 2016)", font_size=22, color=AR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.3, -1.3, 0])
        soft = label(r"each pixel: \ $16$ probabilities, \ one per grey level", font_size=22, color=C.MODEL_Q)
        soft.next_to(grid, DOWN, buff=0.25)
        with self.voiceover(
            "An image is the same story with more variables: the 196 pixels of a digit in reading order. <bookmark "
            "mark='a'/> To predict this pixel the model may look at every pixel before it, and nothing after; it "
            "outputs sixteen probabilities, one per grey level, like a language model's next token. <bookmark "
            "mark='b'/> The trick that makes training fast is a mask: every filter has its future half set to zero, "
            "so one pass predicts all 196 pixels at once, each from its own past. <bookmark mark='c'/> From NADE and "
            "MADE came PixelRNN and PixelCNN, by Aaron van den Oord and colleagues at DeepMind in 2016, and WaveNet "
            "for speech."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(order))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in ctx], lag_ratio=0.01), run_time=1.5)
            self.play(FadeIn(cur, scale=1.3), FadeIn(soft))
            vo.wait_until("b")
            self.play(FadeIn(kern), FadeIn(kz), FadeIn(kl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(h_, shift=UP * 0.1) for h_ in hist], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blind(self):
        p = load("pixelcnn")
        maps = [(np.asarray(p["rf_plain"]), r"masked convolutions, stacked", C.SURPRISE),
                (np.asarray(p["rf_two"]), r"two stacks: \ vertical and horizontal", AR)]
        i0, j0 = 7, 7
        panels = VGroup()
        blind_sq = []
        for rf, name, col in maps:
            grid = pixel_grid(0.27, 0.025)
            bl_ = VGroup()
            for i in range(14):
                for j in range(14):
                    sq = grid[i * 14 + j]
                    mirror = 2 * j0 - j
                    # a full cone of view is symmetric about the pixel's column: an earlier pixel is in the blind
                    # spot if it is unseen while its mirror image across that column is seen
                    blind_ = i < i0 and not rf[i, j] and 0 <= mirror < 14 and rf[i, mirror]
                    if (i, j) == (i0, j0):
                        sq.set_fill(C.MODEL_Q, opacity=0.95)
                    elif rf[i, j]:
                        sq.set_fill(AR, opacity=0.55)
                    elif blind_:
                        sq.set_fill(C.SURPRISE, opacity=0.6)
                        bl_.add(sq)
            blind_sq.append(bl_)
            panels.add(VGroup(grid, label(name, font_size=22, color=col).next_to(grid, UP, buff=0.15)))
        panels.arrange(RIGHT, buff=1.2).move_to(UP * 0.2)
        key = VGroup(
            VGroup(Square(0.22, fill_color=AR, fill_opacity=0.55, stroke_width=0),
                   label(r"pixels the prediction can see", font_size=20)).arrange(RIGHT, buff=0.12),
            VGroup(Square(0.22, fill_color=C.SURPRISE, fill_opacity=0.6, stroke_width=0),
                   label(r"earlier pixels it never sees: \ the blind spot", font_size=20)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.7)
        src = note(r"computed: \ the gradient of the orange pixel's prediction with respect to every input "
                   r"pixel").to_edge(DOWN, buff=0.25)
        cite_ = cite(r"van den Oord et al., \textit{Conditional Image Generation with PixelCNN Decoders} (2016)",
                     corner=UL)
        with self.voiceover(
            "There's a catch. Ask the network which inputs its prediction depends on: the gradient of one pixel's "
            "prediction with respect to every input. <bookmark mark='a'/> With masked filters stacked naively, a "
            "wedge above and to the right is never seen, though it comes earlier. <bookmark mark='b'/> The second "
            "PixelCNN paper splits the network in two: a vertical stack that sees the rows above, feeding a "
            "horizontal stack that sees the row so far. No blind spot. That is the layout we train."
        ) as vo:
            self.play(FadeIn(panels[0][1]), FadeIn(panels[0][0]), FadeIn(src), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(key[0]), FadeIn(key[1]))
            if len(blind_sq[0]):
                self.play(Indicate(blind_sq[0], color=C.SURPRISE, scale_factor=1.15))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        p = load("pixelcnn")
        cv = np.asarray(p["s0_curve"])
        snaps = np.asarray(p["s0_snaps"])
        ex = cv[:, 1]
        g = axes([0, ex[-1]], [0.8, 4.2], x_length=5.6, y_length=3.6, xlabel=r"training digits seen",
                 ylabel=r"held-out bits per pixel", xticks=[0, ex[-1]], yticks=[1, 2, 3, 4],
                 xfmt=lambda v: f"{v / 1000:.0f}" + (r"\text{k}" if v else ""), center=[-3.0, -0.2, 0])
        uni = DashedLine(g.ax.c2p(0, 4), g.ax.c2p(ex[-1], 4), color=GREY_C, stroke_width=1.5)
        ul = label(r"uniform guessing: \ $4$ bits", font_size=18, color=GREY_B).next_to(uni, DOWN, buff=0.06)
        ul.align_to(uni, RIGHT)
        pts = VGroup(*[Dot(g.ax.c2p(e, b), radius=0.055, color=AR) for e, b in zip(ex, cv[:, 2])])
        ln = curve(g.ax, ex, cv[:, 2], AR, 3)
        finals = [float(p[f"s{s}_bpp"]) for s in (0, 1, 2)]
        seeds_ = VGroup(*[Dot(g.ax.c2p(ex[-1], b), radius=0.06, color=WHITE).set_opacity(0.8) for b in finals])
        sheets = [digit_sheet(s_, 4, 4, size=0.55, gap=0.05).move_to([3.6, 0.3, 0]) for s_ in snaps]
        steps_ = [label(rf"after ${e / 1000:.1f}$k digits: \ ${b:.2f}$ bits per pixel", font_size=22, color=AR)
                  .next_to(sheets[0], DOWN, buff=0.25) for e, b in zip(ex, cv[:, 2])]
        head = label(r"our PixelCNN, \ seed $0$ \ (the same random numbers at every checkpoint)", font_size=22,
                     color=GREY_A).to_edge(UP, buff=0.35)
        lo, hi = min(finals), max(finals)
        c0, f0 = float(cv[0, 2]), finals[0]
        tg = note(rf"computed: \ ${p['s0_params']:,}$ parameters, \ $3$ seeds".replace(",", "{,}")).to_corner(DR,
                                                                                                          buff=0.2)
        with self.voiceover(
            "Here is ours learning: on the left, its held-out surprise in bits per pixel; on the right, what it "
            f"draws at each checkpoint. <bookmark mark='a'/> Untrained, it pays {c0:.2f} bits per pixel, about "
            "uniform guessing, and draws static. <bookmark mark='b'/> Then it learns that most pixels are black, "
            f"that ink comes in strokes, and their shapes. <bookmark mark='c'/> It ends at {f0:.2f} bits per pixel; "
            f"three seeds end between {lo:.2f} and {hi:.2f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(head), Create(uni), FadeIn(ul), FadeIn(tg), FadeIn(pts[0]), FadeIn(sheets[0]),
                      FadeIn(steps_[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            cur_s, cur_l = sheets[0], steps_[0]
            per = max(0.5, vo.until("c") / max(1, len(sheets) - 1))
            for k in range(1, len(sheets)):
                self.play(FadeIn(pts[k], scale=1.4), crossfade(cur_s, sheets[k]),
                          ReplacementTransform(cur_l, steps_[k]), run_time=0.55 * per)
                cur_s, cur_l = sheets[k], steps_[k]
                self.wait(0.45 * per)
            vo.wait_until("c")
            self.play(Create(ln), FadeIn(seeds_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drawing(self):
        p, gn = load("pixelcnn"), load("gan")
        probs = np.asarray(p["s0_trace_probs"])
        img = np.asarray(p["s0_trace_image"])
        grid = pixel_grid(0.34, 0.03).move_to([-3.4, 0.0, 0])
        k = ValueTracker(0)
        bars = LiveBars(probs[0], max_value=1.0, height=2.6, bar_width=0.22, gap=0.07, colors=[C.MODEL_Q] * 16,
                        labels=None)
        bars.place(-0.9, x=3.4)
        ramp = VGroup(*[Square(0.2, stroke_width=0, fill_color=level_color(v), fill_opacity=1) for v in range(16)])
        for i, sq in enumerate(ramp):
            sq.move_to([bars._cx(i) + bars.base.get_start()[0] + 0.15 - bars.x0, -1.12, 0])
        bl = label(r"the next pixel: \ $p(x_i \mid x_{<i})$ over $16$ grey levels", font_size=22, color=C.MODEL_Q)
        bl.next_to(bars, UP, buff=0.35).set_x(3.4)
        cnt = DecimalNumber(0, num_decimal_places=0, font_size=30, color=AR).move_to([3.0, -2.0, 0])
        cl = label(r"pixels drawn, \ of $196$", font_size=22, color=GREY_A).next_to(cnt, RIGHT, buff=0.2)
        cur = SurroundingRectangle(grid[0], color=C.MODEL_Q, buff=0.02, stroke_width=3)

        def upd(_):
            n = int(min(196, k.get_value()))
            for i in range(196):
                grid[i].set_fill(level_color(img.flat[i]) if i < n else "#0B0F17", opacity=1)
            j = min(n, 195)
            for t_, v in zip(bars.trackers, probs[j]):
                t_.set_value(float(v))
            cur.move_to(grid[j])
            cnt.set_value(n)

        holder = VGroup(grid, cur, cnt)
        holder.add_updater(upd)
        ms_ar = float(p["s0_sample_secs"]) * 1000
        ms_gan = float(gn["s0_sample_secs"]) * 1000
        ratio = ms_ar / max(ms_gan, 1e-9)
        cost = label(rf"$196$ passes per digit: \ ${ms_ar:.1f}$ ms here, \ against ${ms_gan:.3f}$ ms for the GAN",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And here is one digit being drawn, with the model's sixteen probabilities for the next pixel. "
            "<bookmark mark='a'/> In the margin it is sure: black. <bookmark mark='b'/> At a stroke's edge it "
            "hesitates, and the coin it tosses shapes the digit. <bookmark mark='c'/> The price is the order: 196 "
            f"passes for one digit, each waiting for the last, {ms_ar:.1f} milliseconds here, about {ratio:,.0f} "
            "times the GAN's single pass."
        ) as vo:
            self.add(holder)
            self.play(FadeIn(grid), FadeIn(bars), FadeIn(ramp), FadeIn(bl), FadeIn(cl), FadeIn(cur), FadeIn(cnt))
            vo.wait_until("a")
            first = int(np.argmax(img.ravel() > 3))
            self.play(k.animate.set_value(max(8, first - 2)), run_time=vo.until("b") * 0.9, rate_func=linear)
            vo.wait_until("b")
            self.play(k.animate.set_value(min(196, first + 30)), run_time=max(3.0, vo.until("c") * 0.9),
                      rate_func=linear)
            vo.wait_until("c")
            self.play(k.animate.set_value(196), FadeIn(cost), run_time=max(2.0, vo.remaining() - 0.5),
                      rate_func=linear)
        holder.clear_updaters()
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()
