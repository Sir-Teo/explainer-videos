from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, module_box,
                                   timeline_bar)

STAGES = [(r"style", LAM), (r"layout", DATA), (r"paint", HEAD), (r"composite", KERN)]


def _stages(lit, w=1.55, h=0.5, font=17, dim=GREY_D):
    """The pipeline as a row of boxes, the stages in `lit` coloured and the others dimmed."""
    g = VGroup(*[module_box(n, c if k in lit else dim, w=w, h=h, font=font) for k, (n, c) in enumerate(STAGES)])
    g.arrange(RIGHT, buff=0.3)
    arrows = VGroup(*[Arrow(g[k].get_right(), g[k + 1].get_left(), buff=0.04, stroke_width=2, color=GREY_B,
                            max_tip_length_to_length_ratio=0.3) for k in range(len(g) - 1)])
    for k, b in enumerate(g):
        if k not in lit:
            b[1].set_color(GREY_C)
    return VGroup(g, arrows)


class Rendering(VoiceoverScene):
    def construct(self):
        self.card()
        self.pipeline()
        self.layers()
        self.budget()
        self.jank()

    def card(self):
        card = chapter_card(5, r"Paint, \ layers and the frame", r"How does a page reach the screen sixty times a "
                            r"second?", lit=(2011, 2011),
                            extra=((2011, r"requestAnimationFrame in Firefox and Chrome"),), part=PART)
        with self.voiceover("Chapter five. Paint, layers and the frame."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the pipeline and the display list
    def pipeline(self):
        head = label(r"From boxes to pixels", font_size=36).to_edge(UP, buff=0.3)
        src = module_box(r"DOM $+$ CSSOM", GREY_A, w=2.1, h=0.6, font=18)
        boxes = VGroup(src, *[module_box(n, c, w=2.0, h=0.6, font=19) for n, c in STAGES]).arrange(RIGHT, buff=0.5)
        boxes.next_to(head, DOWN, buff=0.6)
        arrows = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.05, stroke_width=2.5,
                                color=GREY_B, max_tip_length_to_length_ratio=0.3) for k in range(4)])
        outs = VGroup(*[wrapped_label(t, 2.0, font_size=17, color=c).next_to(boxes[k + 1], DOWN, buff=0.18)
                        for k, (t, c) in enumerate(((r"a computed style for every element", LAM),
                                                    (r"a tree of boxes and line boxes", DATA),
                                                    (r"a display list of drawing commands", HEAD),
                                                    (r"layers rastered and combined into one frame", KERN)))])
        dl = code_block(["fillRect(0, 0, 900, 1392, bg)", "drawText('Computer Science, Built', 36, 52)",
                         "fillRect(36, 70, 828, 2, grey)", "drawText('Sixty-one parts in eleven', 36, 104)",
                         "drawText('acts ...', 36, 124)", "...                 # one layer's list"], size=15,
                        color=HEAD)
        dlt = label(r"a display list \ (illustrative)", font_size=18, color=HEAD)
        dlg = VGroup(dlt, dl).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(outs, DOWN, buff=0.9)
        dlg.align_to([-6.5, 0, 0], LEFT)
        notes = VGroup(
            wrapped_label(r"paint does not make pixels: \ it records what to draw, \ in the order CSS defines \ "
                          r"(backgrounds and borders, \ then content, \ then positioned elements by "
                          r"\texttt{z-index})", 5.4, font_size=19, color=WHITE),
            wrapped_label(r"rasterising the list into pixels, \ in tiles and usually on the GPU, \ is Part 51's "
                          r"subject", 5.4, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(dlg, RIGHT, buff=0.6).align_to(dlg, UP)
        token = Dot(radius=0.12, color=WHITE).move_to(boxes[0].get_top() + UP * 0.25)
        with self.voiceover(
            "With every box placed, the browser still has to make pixels, and it does so in a pipeline. "
            "<bookmark mark='a'/> Style computes the properties of every element. Layout places the boxes. Paint "
            "walks the box tree and records what to draw. Composite combines the results into a frame. "
            "<bookmark mark='b'/> Paint does not set pixels directly. It produces a display list, drawing commands "
            "in the order CSS defines: backgrounds and borders first, then text, then positioned elements by their "
            "stacking order. <bookmark mark='c'/> Turning that list into pixels, in tiles and usually on the "
            "graphics processor, is rasterisation, the subject of Part 51."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(token))
            for k in range(4):
                self.play(GrowArrow(arrows[k]), FadeIn(boxes[k + 1]), FadeIn(outs[k]),
                          token.animate.move_to(boxes[k + 1].get_top() + UP * 0.25), run_time=0.9)
            vo.wait_until("b")
            self.play(FadeIn(dlg), FadeIn(notes[0]), Indicate(boxes[3]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), Indicate(boxes[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ layers and the compositor
    def layers(self):
        head = label(r"Layers and the compositor", font_size=36).to_edge(UP, buff=0.3)
        shear = np.array([[1.0, 0.55, 0.0], [0.0, 0.42, 0.0], [0.0, 0.0, 1.0]])

        def layer(w, h, col, name, op=0.18):
            r = Rectangle(width=w, height=h, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=op)
            r.apply_matrix(shear)
            return VGroup(r, label(name, font_size=17, color=col).next_to(r, LEFT, buff=0.15))
        page = layer(3.6, 2.6, GREY_B, r"page")
        bar = layer(3.6, 0.6, DATA, r"sticky header")
        card = layer(1.4, 0.9, HEAD, r"animated card", op=0.4)
        page.move_to([-3.2, -1.4, 0])
        bar.move_to([-3.2, 0.25, 0]).align_to(page, RIGHT)
        card.move_to([-3.6, 1.6, 0])
        guide = DashedLine(page[0].get_center(), card[0].get_center(), color=GREY_D, stroke_width=1)
        rows = VGroup(
            VGroup(label(r"animate \texttt{width} or \texttt{top}: \ every stage, \ every frame", font_size=19,
                         color=NO), _stages({0, 1, 2, 3})).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            VGroup(label(r"animate \texttt{transform} or \texttt{opacity}: \ composite only", font_size=19,
                         color=YES), _stages({3})).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.3, 1.0, 0])
        notes = VGroup(
            wrapped_label(r"each layer is rastered once into a texture; \ the compositor moves, \ fades and stacks "
                          r"textures on the GPU", 6.4, font_size=19, color=WHITE),
            wrapped_label(r"it runs on its own thread, \ so such an animation keeps going while scripts are busy", 6.4,
                          font_size=19, color=YES),
            wrapped_label(r"layers cost memory: \ \texttt{will-change} asks for one; \ too many and the GPU runs "
                          r"short", 6.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(rows, DOWN, buff=0.45).align_to(rows, LEFT)
        with self.voiceover(
            "Browsers do not repaint the whole page for every change. <bookmark mark='a'/> They split it into "
            "layers: here the page, a header that stays put while the page scrolls, and a card being animated. Each "
            "layer is rastered once into a texture, and the compositor stacks the textures on the graphics "
            "processor. <bookmark mark='b'/> Animate a property such as width, and every frame goes through style, "
            "layout, paint and composite. Animate transform or opacity instead, and nothing about the boxes "
            "changes: the compositor just moves or fades a texture. <bookmark mark='c'/> It runs on its own thread, "
            "so such an animation keeps running even while a script is busy. <bookmark mark='d'/> Layers are not "
            "free, though: each is a texture in memory, and a page that asks for too many runs short."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(page, shift=DOWN * 0.2), FadeIn(bar, shift=DOWN * 0.2), FadeIn(card, shift=DOWN * 0.2),
                      Create(guide))
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
            for d in (RIGHT * 1.4, LEFT * 1.4):
                self.play(card.animate.shift(d), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), card.animate.set_opacity(0.4), run_time=1.0)
            self.play(card.animate.set_opacity(1), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the frame budget and requestAnimationFrame
    def budget(self):
        fr = load("frames")
        frame = fr["budget_ms"]
        r0 = fr["long"]["renders"][0]
        step = r0[1] - r0[0]
        head = label(rf"{frame:.1f} milliseconds", font_size=36).to_edge(UP, buff=0.3)
        x0, s, span = -5.2, 11.2 / 100, 100
        rows = VGroup()
        for k, (hz, per, col) in enumerate(((60, frame, DATA), (120, frame / 2, LAM))):
            y = 2.0 - k * 0.9
            axis = Line([x0, y, 0], [x0 + span * s, y, 0], color=GREY_C, stroke_width=1.2)
            ticks = VGroup(*[Line([x0 + t * s, y - 0.15, 0], [x0 + t * s, y + 0.15, 0], color=col, stroke_width=2.5)
                             for t in [q * per for q in range(int(span / per) + 1)]])
            name = label(rf"{hz} Hz", font_size=19, color=col).next_to(axis, LEFT, buff=0.25)
            gap = label(rf"a frame every {per:.1f} ms", font_size=17, color=col).next_to(
                ticks[1], UP, buff=0.08).align_to(ticks[0], LEFT)
            rows.add(VGroup(axis, ticks, name, gap))
        ms = VGroup(*[label(rf"{t} ms", font_size=16, color=GREY_B).move_to([x0 + t * s, 0.75, 0])
                      for t in range(0, 101, 25)])
        # one frame, as our simulator spends it: the rendering step, and the rest left for tasks
        fy, fs = -0.35, 11.2 / frame / 1.5
        fx0 = -5.2
        rnd = timeline_bar(0, step, fy, YES, h=0.45, scale=fs)
        rest = Rectangle(width=(frame - step) * fs, height=0.45, stroke_color=GREY_C, stroke_width=1,
                         fill_opacity=0).move_to([(step + frame) / 2 * fs, fy, 0])
        one = VGroup(rnd, rest).shift(RIGHT * fx0)
        lab = VGroup(
            label(rf"rendering step: \ {step:.0f} ms in our model", font_size=17, color=YES).next_to(
                rnd, DOWN, buff=0.12).align_to(rnd, LEFT),
            label(rf"{frame - step:.1f} ms left for tasks", font_size=17, color=GREY_A).move_to(rest),
        )
        code = code_block(["function step(t) {", "  card.style.transform =", "      `translateX(${x(t)}px)`;",
                           "  requestAnimationFrame(step);", "}", "requestAnimationFrame(step);"], size=16)
        code.to_corner(DL, buff=0.5)
        notes = VGroup(
            wrapped_label(r"\texttt{requestAnimationFrame} runs a callback once, \ just before the next frame's "
                          r"style and layout, \ with that frame's timestamp", 6.2, font_size=19, color=WHITE),
            wrapped_label(r"a timer set to 16 ms drifts against the display; \ the callback follows it, \ and "
                          r"pauses in background tabs", 6.2, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(code, RIGHT, buff=0.5).align_to(code, UP)
        with self.voiceover(
            "All of this has a deadline. <bookmark mark='a'/> A sixty hertz display shows a new frame every sixteen "
            "point seven milliseconds; on a hundred and twenty hertz screen, every eight point three. "
            "<bookmark mark='b'/> Everything for a frame, scripts, style, layout and paint, has to fit in that "
            "window. In our simulator a frame's rendering step takes four milliseconds, leaving about twelve and a "
            "half for everything else. <bookmark mark='c'/> To animate in step with the display, a page asks for "
            "requestAnimationFrame. Its callback runs once, just before the next frame's style and layout, and "
            "receives that frame's time. A timer set to sixteen milliseconds drifts against the display instead, "
            "and the browser pauses animation frames in background tabs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.5), FadeIn(ms))
            vo.wait_until("b")
            self.play(FadeIn(one), FadeIn(lab))
            vo.wait_until("c")
            self.play(FadeIn(code), FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ jank: one long task against chunks
    def jank(self):
        fr = load("frames")
        frame = fr["budget_ms"]
        lg, ch = fr["long"], fr["chunked"]
        head = label(r"One long task, \ and the frames it drops", font_size=36).to_edge(UP, buff=0.3)
        T = 275.0
        x0, s = -6.2, 12.6 / T

        def X(t):
            return x0 + t * s

        def lane(data, y, long_col):
            ticks = VGroup(*[Line([X(q * frame), y + 0.32, 0], [X(q * frame), y + 0.48, 0], color=GREY_B,
                                  stroke_width=1.5) for q in range(int(T / frame) + 1)])
            base = Line([X(0), y, 0], [X(T), y, 0], color=GREY_D, stroke_width=1)
            bars = VGroup()
            for a, b, kind, _ in data["timeline"]:
                if b - a < 1e-9:
                    continue
                if kind == "render":
                    col = YES
                else:
                    col = long_col if b - a > frame else DATA
                bar = timeline_bar(a, b, y, col, h=0.42, scale=s).shift(RIGHT * x0)
                if kind == "task" and bar.width > 0.1:      # a hairline gap shows where one task ends
                    bar.stretch_to_fit_width(bar.width - 0.04)
                bars.add(bar)
            return VGroup(base, ticks), bars
        ya, yb = 1.25, -0.85
        lane_a, bars_a = lane(lg, ya, NO)
        lane_b, bars_b = lane(ch, yb, DATA)
        ta = label(r"a click at 40 ms runs one 120 ms task", font_size=20, color=NO).move_to(
            [0, ya + 0.8, 0]).align_to([x0, 0, 0], LEFT)
        tb = label(r"the same work in 8 ms chunks, \ each yielding with \texttt{setTimeout(0)}", font_size=20,
                   color=DATA).move_to([0, yb + 0.8, 0]).align_to([x0, 0, 0], LEFT)
        vs = label(r"vsync", font_size=16, color=GREY_B).next_to([X(T), ya + 0.4, 0], RIGHT, buff=0.08)
        ra = lg["renders"]
        k = max(range(len(lg["gaps"])), key=lambda q: lg["gaps"][q])
        a0, a1 = ra[k][0], ra[k + 1][0]
        brace = BraceBetweenPoints([X(a0), ya - 0.3, 0], [X(a1), ya - 0.3, 0], direction=DOWN, color=NO)
        bl = label(rf"{lg['gaps'][k]:.1f} ms between frames: \ {lg['dropped']} frames dropped", font_size=18,
                   color=NO).next_to(brace, DOWN, buff=0.08)
        rb = ch["renders"]
        lo, hi = min(ch["gaps"]), max(ch["gaps"])
        cb = label(rf"{ch['dropped']} frames dropped; \ frames {lo:.0f} to {hi:.1f} ms apart", font_size=18,
                   color=YES).move_to([X((rb[2][0] + rb[10][0]) / 2), yb - 0.55, 0])
        done_long = max(b for a, b, kind, _ in lg["timeline"] if kind == "task")
        done_ch = ch["finish"]
        marks = VGroup(
            DashedLine([X(done_long), ya - 0.25, 0], [X(done_long), yb + 0.3, 0], color=NO, stroke_width=1.5,
                       dash_length=0.06),
            DashedLine([X(done_ch), yb - 0.25, 0], [X(done_ch), yb - 0.95, 0], color=DATA, stroke_width=1.5,
                       dash_length=0.06),
        )
        ml = label(rf"work done at {done_ch:.0f} ms, \ not {done_long:.0f}", font_size=18, color=DATA).next_to(
            marks[1], RIGHT, buff=0.1).shift(DOWN * 0.2)
        axis = VGroup(*[label(rf"{t} ms", font_size=16, color=GREY_B).move_to([X(t), -2.05, 0])
                        for t in range(0, 251, 50)])
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.85),
                                 label(t, font_size=17, color=c)).arrange(RIGHT, buff=0.1)
                          for t, c in ((r"task", DATA), (r"long task", NO),
                                       (r"rendering: \ 3 ms animation callback, \ then style, \ layout, \ paint",
                                        YES))]).arrange(RIGHT, buff=0.45).next_to(axis, DOWN, buff=0.3)
        rule = wrapped_label(r"the browser's own Long Tasks API flags any task over 50 ms; \ input that arrives "
                             r"during one also waits \ (Chapter 10's INP)", 12.4, font_size=19,
                             color=HEAD).to_edge(DOWN, buff=0.2)
        assert lg["dropped"] == 7 and ch["dropped"] == 0
        with self.voiceover(
            "Here is our event-loop simulator running an animation: every frame, a three millisecond "
            "requestAnimationFrame callback, then style, layout and paint. <bookmark mark='a'/> At forty "
            "milliseconds a click arrives, and its handler does a hundred and twenty milliseconds of work in one "
            "task. <bookmark mark='b'/> A task runs to completion, and rendering cannot happen in the middle of "
            "one. So after frames sixteen point seven milliseconds apart comes a gap of a hundred and twenty-six "
            "point seven: seven frames dropped, and the animation visibly stutters. That stutter is jank. "
            "<bookmark mark='c'/> Now split the same work into chunks of eight milliseconds, each scheduling the "
            "next with setTimeout of zero. Between chunks the loop gets a chance to render. "
            "<bookmark mark='d'/> No frame is dropped, though some arrive a few milliseconds late. "
            "<bookmark mark='e'/> The price is throughput: the work finishes at a hundred and ninety-six "
            "milliseconds instead of a hundred and sixty. <bookmark mark='f'/> Browsers flag any task over fifty "
            "milliseconds as a long task, and a click during one waits too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lane_a), FadeIn(vs), FadeIn(axis), FadeIn(legend))
            self.play(LaggedStart(*[FadeIn(bb) for bb in bars_a if bb[0].get_center()[0] < X(40)], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(ta))
            self.play(LaggedStart(*[FadeIn(bb) for bb in bars_a if bb[0].get_center()[0] >= X(40)],
                                  lag_ratio=0.2), run_time=2)
            vo.wait_until("b")
            self.play(GrowFromCenter(brace), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(lane_b), FadeIn(tb))
            self.play(LaggedStart(*[FadeIn(bb) for bb in bars_b], lag_ratio=0.12), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(cb))
            vo.wait_until("e")
            self.play(Create(marks), FadeIn(ml))
            vo.wait_until("f")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM)
