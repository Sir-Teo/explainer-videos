from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

# One token from a big model, at batch size one: every weight is read once.  Published figures, not measured here.
BW = 3.35e12  # bytes a second: an H100 (SXM)'s HBM3 memory, NVIDIA's datasheet
PEAK = 989e12  # dense 16-bit operations a second, the same chip
PARAMS = 70.6e9  # Llama 3.1 70B
BYTES = 2 * PARAMS  # 16 bits each
TOKENS_S = BW / BYTES
USE = 2 * PARAMS * TOKENS_S / PEAK  # the share of the chip's arithmetic a lone conversation uses


class Hook(VoiceoverScene):
    def construct(self):
        self.stream()
        self.bound()
        self.plan()

    # ------------------------------------------------------------------
    def stream(self):
        cols, rows = 18, 10
        g = np.random.default_rng(19)
        shade = g.uniform(0.15, 0.65, (rows, cols))
        cell = 0.36
        wall = VGroup(*[Square(cell * 0.86, stroke_width=0, fill_color=C.NEURAL, fill_opacity=shade[r, c])
                        for r in range(rows) for c in range(cols)]).arrange_in_grid(rows=rows, cols=cols, buff=cell * 0.14)
        wall.move_to([-2.6, 0.5, 0])
        for i, sq in enumerate(wall):
            sq.base = shade[i // cols, i % cols]
        wl = label(r"memory: \ the weights, \\ $70$ billion numbers, \ $141$ GB", font_size=24, color=C.NEURAL).to_edge(UP, buff=0.35)
        wl.set_x(wall.get_x())
        lay = VGroup(label(r"layer $1$", font_size=18, color=GREY_C), label(r"layer $80$", font_size=18, color=GREY_C))
        lay[0].next_to(wall, DOWN, buff=0.12).align_to(wall, LEFT)
        lay[1].next_to(wall, DOWN, buff=0.12).align_to(wall, RIGHT)
        lay_a = Arrow(lay[0].get_right(), lay[1].get_left(), buff=0.15, stroke_width=1.5, color=GREY_D, max_tip_length_to_length_ratio=0.03)
        chip_ = VGroup(*[Square(0.22, stroke_width=0.8, stroke_color=C.BITS, fill_color=C.BITS, fill_opacity=0.15) for _ in range(36)])
        chip_.arrange_in_grid(rows=6, cols=6, buff=0.04).move_to([4.9, 0.5, 0])
        chip_box = SurroundingRectangle(chip_, color=C.BITS, buff=0.12, stroke_width=2.5, corner_radius=0.08)
        cl_ = label(r"the chip's \\ arithmetic", font_size=22, color=C.BITS).next_to(chip_box, UP, buff=0.2)
        p0, p1 = wall.get_right() + RIGHT * 0.2, chip_box.get_left() + LEFT * 0.1
        pipe = VGroup(Line(p0 + UP * 0.12, p1 + UP * 0.12, color=GREY_C, stroke_width=1.5),
                      Line(p0 + DOWN * 0.12, p1 + DOWN * 0.12, color=GREY_C, stroke_width=1.5))
        pl = label(r"$3.35$ TB/s", font_size=22, color=GREY_A).next_to(pipe, DOWN, buff=0.15)
        x0, x1 = wall.get_left()[0], wall.get_right()[0]
        sweep = ValueTracker(x0 - 1.0)

        def light(m):
            x = sweep.get_value()
            for sq in m:
                hot = np.exp(-((sq.get_x() - x) / 0.35) ** 2)
                sq.set_fill(interpolate_color(ManimColor(C.NEURAL), ManimColor(WHITE), 0.85 * hot), opacity=min(1.0, sq.base + hot))

        n_dots = 6

        def flow(m):
            u = (sweep.get_value() - x0) / (x1 - x0)
            on = 1.0 if -0.05 < u < 1.05 else 0.0
            for i, d in enumerate(m):
                f = (u * 4 + i / n_dots) % 1.0
                d.move_to(p0 + (p1 - p0) * f).set_opacity(on)

        dots = VGroup(*[Dot(radius=0.05, color=WHITE).set_opacity(0) for _ in range(n_dots)])
        text = "the girl"
        chips = VGroup(*[Text(ch if ch != " " else "·", font="DejaVu Sans Mono", font_size=34, color=WHITE) for ch in text])
        chips.arrange(RIGHT, buff=0.12).next_to(chip_box, DOWN, buff=0.9)
        out_l = label(r"written so far:", font_size=22, color=GREY_A).next_to(chips, UP, buff=0.2)
        n_tok = ValueTracker(0)
        cl = label(r"GB read from memory", font_size=24, color=C.BITS).move_to([-1.6, -2.75, 0])
        count = Integer(0, font_size=34, color=C.BITS).next_to(cl, LEFT, buff=0.18)
        count.add_updater(lambda m: m.set_value(int(round(141 * n_tok.get_value()))).next_to(cl, LEFT, buff=0.18))
        tag = note(r"schematic: \ one square stands for $400$ million weights").to_corner(DR, buff=0.25)
        bytes_l = label(r"each weight: \ $16$ bits $=$ $2$ bytes", font_size=20, color=C.NEURAL).next_to(wl, DOWN, buff=0.1)
        pl2 = label(r"memory bandwidth: \\ $3.35$ TB a second", font_size=20, color=GREY_A).next_to(pipe, DOWN, buff=0.15)
        with self.voiceover(
            "When a big model writes, it writes one token at a time. And to write each one, it has to read every "
            "single one of its weights. <bookmark mark='a'/> For a seventy-billion-parameter model, stored as "
            "sixteen-bit numbers, two bytes each, that's a hundred and forty-one gigabytes, streamed from memory "
            "through to the chip, <bookmark mark='b'/> for one token. Then all of it again for the next one, and the "
            "next. <bookmark mark='c'/> How many bytes a second can flow from memory to the chip is the memory "
            "bandwidth: here, three point three five terabytes a second."
        ) as vo:
            self.play(FadeIn(wall, lag_ratio=0.01), FadeIn(wl), FadeIn(lay), GrowArrow(lay_a), FadeIn(tag), run_time=1.5)
            self.play(FadeIn(chip_), Create(chip_box), FadeIn(cl_), Create(pipe), FadeIn(pl))
            vo.wait_until("a")
            wall.add_updater(light)
            dots.add_updater(flow)
            self.add(dots)
            self.play(FadeIn(out_l), FadeIn(cl), FadeIn(count), FadeIn(bytes_l))
            self.play(sweep.animate.set_value(x1 + 0.6), n_tok.animate.set_value(1), run_time=2.6, rate_func=linear)
            self.play(FadeIn(chips[0], shift=DOWN * 0.2), chip_.animate.set_fill(opacity=0.5), run_time=0.4)
            self.play(chip_.animate.set_fill(opacity=0.15), run_time=0.3)
            vo.wait_until("b")
            for k in range(1, len(chips)):
                sweep.set_value(x0 - 0.6)
                rt = max(0.35, 1.2 * 0.75 ** k)
                self.play(sweep.animate.set_value(x1 + 0.6), n_tok.animate.set_value(k + 1), run_time=rt, rate_func=linear)
                self.add(chips[k])
            wall.remove_updater(light)
            dots.clear_updaters()
            count.clear_updaters()
            self.remove(dots)
            vo.wait_until("c")
            self.play(FadeTransform(pl, pl2), Indicate(pipe, color=WHITE, scale_factor=1.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bound(self):
        colors = {r"\text{bandwidth}": C.BITS, r"\text{bytes}": C.NEURAL}
        f1 = cmath(r"\frac{\text{tokens}}{\text{second}}", r"\;\le\;", r"\frac{", r"\text{bandwidth}", r"}{", r"\text{bytes}", r"}",
                   colors=colors, font_size=44).move_to(UP * 2.5 + LEFT * 2.6)
        f2 = cmath(r"=\;\frac{3.35\ \text{TB/s}}{141\ \text{GB}}\;\approx\;", rf"{TOKENS_S:.0f}", font_size=44,
                   colors={rf"{TOKENS_S:.0f}": C.BITS}).next_to(f1, RIGHT, buff=0.3)
        VGroup(f1, f2).move_to(UP * 2.5)
        src = label(r"an H100 chip; \ Llama 3.1 70B in 16-bit numbers", font_size=22, color=GREY_A).next_to(VGroup(f1, f2), DOWN, buff=0.3)
        # the chip's arithmetic, as a bar; the sliver one conversation uses; and its first percent, magnified
        W = 11.0
        full = Rectangle(width=W, height=0.5, stroke_color=GREY_C, stroke_width=1.5, fill_opacity=0).move_to(UP * 0.1)
        used = Rectangle(width=max(W * USE, 0.03), height=0.5, stroke_width=0, fill_color=C.SURPRISE, fill_opacity=1)
        used.align_to(full, LEFT).set_y(full.get_y())
        fl = label(rf"the chip's arithmetic: \ ${PEAK / 1e12:.0f}$ trillion operations a second", font_size=22,
                   color=GREY_A).next_to(full, UP, buff=0.15).align_to(full, LEFT)
        mag = 50
        zw = W * 0.01
        zoom_src = Rectangle(width=zw, height=0.7, stroke_color=WHITE, stroke_width=1.5).align_to(full, LEFT).set_y(full.get_y())
        inset = Rectangle(width=zw * mag, height=0.9, stroke_color=GREY_B, stroke_width=1.5).move_to([-2.4, -1.7, 0])
        inset.align_to(full, LEFT)
        big = Rectangle(width=W * USE * mag, height=0.9, stroke_width=0, fill_color=C.SURPRISE, fill_opacity=1)
        big.align_to(inset, LEFT).set_y(inset.get_y())
        rays = VGroup(Line(zoom_src.get_corner(DL), inset.get_corner(UL), color=GREY_C, stroke_width=1),
                      Line(zoom_src.get_corner(DR), inset.get_corner(UR), color=GREY_C, stroke_width=1))
        il = label(rf"the first $1\%$, \ magnified ${mag}\times$", font_size=20, color=GREY_B).next_to(inset, RIGHT, buff=0.25)
        ul = label(rf"used, \ writing ${TOKENS_S:.0f}$ tokens a second: \ ${100 * USE:.2f}\%$", font_size=28,
                   color=C.SURPRISE).next_to(inset, DOWN, buff=0.3).align_to(inset, LEFT)
        cite_ = cite(r"NVIDIA, \textit{H100 Tensor Core GPU} datasheet; \ Meta, \textit{Llama 3.1} (2024)", corner=DR)
        # training vs inference: the same weights, changing in one, frozen in the other
        g = np.random.default_rng(7)
        panels = VGroup()
        for k, (head, col) in enumerate(((r"training: \ the weights change", C.SURPRISE),
                                         (r"inference: \ the weights frozen, \ tokens out", C.BITS))):
            box = RoundedRectangle(width=5.8, height=2.5, corner_radius=0.15, stroke_color=col, stroke_width=2).move_to([-3.2 + 6.4 * k, -1.3, 0])
            grid = VGroup(*[Square(0.3, stroke_width=0, fill_color=C.NEURAL, fill_opacity=float(o)) for o in g.uniform(0.2, 0.8, 18)])
            grid.arrange_in_grid(rows=3, cols=6, buff=0.05).move_to(box.get_center() + LEFT * 1.2 + DOWN * 0.2)
            hl_ = label(head, font_size=22, color=col).next_to(box.get_top(), DOWN, buff=0.2)
            panels.add(VGroup(box, grid, hl_))
        upd = CurvedArrow(panels[0][1].get_right() + RIGHT * 0.2 + DOWN * 0.3, panels[0][1].get_right() + RIGHT * 0.2 + UP * 0.3,
                          angle=PI * 0.9, color=C.SURPRISE, stroke_width=2.5, tip_length=0.15)
        upl = label(r"learn from \\ each example", font_size=18, color=C.SURPRISE).next_to(upd, RIGHT, buff=0.2)
        out_a = Arrow(panels[1][1].get_right(), panels[1][1].get_right() + RIGHT * 1.0, buff=0.15, color=GREY_B, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.25)
        out_t = VGroup(*[data_text(w_, font="DejaVu Sans Mono", font_size=24, color=WHITE) for w_ in ("the", "girl", "ran")])
        out_t.arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(out_a, RIGHT, buff=0.15)
        with self.voiceover(
            "So memory sets a speed limit. Tokens per second can't beat the memory bandwidth divided by the bytes of "
            f"weights: on one of today's best chips, about {TOKENS_S:.0f} tokens a second. <bookmark mark='a'/> And "
            "meanwhile the chip's arithmetic sits almost idle. <bookmark mark='b'/> One conversation uses "
            f"{'a third of one percent' if 0.25 < 100 * USE < 0.42 else f'{100 * USE:.2f} percent'} of it. "
            "<bookmark mark='c'/> Running a trained model to get answers, with no learning, just using it, is called "
            "inference; it's not part six's variational inference. And inference is a problem "
            "of moving numbers, not multiplying them."
        ) as vo:
            self.play(Write(f1), FadeIn(cite_))
            self.play(FadeIn(f2, shift=LEFT * 0.1), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(full), FadeIn(fl))
            self.play(GrowFromEdge(used, LEFT))
            vo.wait_until("b")
            self.play(Create(zoom_src), Create(rays), Create(inset), FadeIn(il))
            self.play(GrowFromEdge(big, LEFT), FadeIn(ul), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeOut(VGroup(full, used, fl, zoom_src, rays, inset, big, il, ul)), run_time=0.5)
            self.play(FadeIn(panels), Create(upd), FadeIn(upl))
            for _ in range(2):
                self.play(*[sq.animate.set_fill(opacity=float(o)) for sq, o in zip(panels[0][1], g.uniform(0.2, 0.8, 18))],
                          GrowArrow(out_a) if _ == 0 else Wait(0), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(w_, shift=RIGHT * 0.15) for w_ in out_t], lag_ratio=0.4),
                      *[sq.animate.set_fill(opacity=float(o)) for sq, o in zip(panels[0][1], g.uniform(0.2, 0.8, 18))], run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 19: \ Inference", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"guess ahead, \ fewer bits, \ fewer bytes moved", font_size=30, color=C.BITS).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=19, done=18).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part is about running models fast: guessing ahead and checking at once, storing numbers in fewer "
            "bits, <bookmark mark='a'/> and moving fewer bytes."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
