from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Compute(VoiceoverScene):
    def construct(self):
        self.card()
        self.threshold_unit()
        self.coincidence()
        self.dendrites()

    def card(self):
        card = chapter_card(11, r"What one neuron can compute", r"Is a neuron a switch, or something more?", lit=(),
                            part=PART, scale=("neuron", "circuit"), marr=("what",))
        with self.voiceover(
            "Chapter eleven. What one neuron can compute."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _table(self, title, outs, cx, color):
        rows = VGroup(label(title, font_size=28, color=color))
        for (a, b), o in zip(((0, 0), (0, 1), (1, 0), (1, 1)), outs):
            rows.add(label(rf"{a} \ \ {b} \ $\rightarrow$ \ {o}", font_size=32, color=(WHITE if o else GREY_B)))
        return rows.arrange(DOWN, buff=0.16).move_to([cx, -0.35, 0])

    def threshold_unit(self):
        head = heading(r"The simplest reading: \ add, and compare with a threshold")
        body = Circle(radius=1.05, color=VOLT, stroke_width=3, fill_color="#111722", fill_opacity=1).move_to([0, 0.3, 0])
        rule = MathTex(r"\sum w_i x_i \ge \theta", font_size=30).move_to(body)
        ins = VGroup(*[Arrow([-3.0, 0.3 + dy, 0], body.get_left() + np.array([0.02, dy * 0.35, 0]), color=GATE["n"],
                             stroke_width=4, buff=0.05) for dy in (0.8, -0.8)])
        in_l = VGroup(*[label(t, font_size=28, color=GATE["n"]).next_to(a_.get_start(), LEFT, buff=0.1)
                        for t, a_ in zip((r"input 1", r"input 2"), ins)])
        out = Arrow(body.get_right(), body.get_right() + RIGHT * 2.0, color=MODEL, stroke_width=4, buff=0.05)
        out_l = label(r"fire, or not", font_size=28, color=MODEL).next_to(out, RIGHT, buff=0.1)
        unit = VGroup(body, rule, ins, in_l, out, out_l)
        t_and = self._table(r"both \ (threshold 2)", (0, 0, 0, 1), -5.0, MODEL)
        t_or = self._table(r"either \ (threshold 1)", (0, 1, 1, 1), -1.9, MODEL)
        t_xor = self._table(r"one but not both", (0, 1, 1, 0), 1.2, BAD)
        cross = Cross(t_xor, stroke_color=BAD, stroke_width=4).scale(0.85)
        side = VGroup(
            wrapped_label(r"A cell that only adds can draw one straight boundary between ``fire'' and ``don't''.",
                          3.4, 26, WHITE),
            wrapped_label(r"``One but not both'' needs two boundaries. \ No such cell can do it.", 3.4, 26, BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([5.0, -0.35, 0])
        keep_in_frame(side)
        end = wrapped_label(r"Checked here by linear programming: \ no weights and no threshold give the third "
                            r"table.", 12.0, 26, GREY_A).to_edge(DOWN, buff=0.6)
        tag = note(r"computed").to_corner(DR, buff=0.2)
        with self.voiceover(
            "So what is a neuron, as a computing element? The simplest reading comes straight from the "
            "integrate-and-fire model. It adds up its inputs, each with a weight, and fires if the total "
            "reaches a threshold. <bookmark mark='a'/> That's already logic. Give a cell two inputs and a "
            "high threshold, and it fires only when both are active. <bookmark mark='b'/> Lower the "
            "threshold, and it fires when either is. <bookmark mark='c'/> But there are things a cell of "
            "this kind can't do, and the classic one is the third table: fire when one input is active, but "
            "not when both are. <bookmark mark='d'/> The reason is geometric. A cell that only adds divides "
            "its inputs with one straight boundary: fire on this side, stay silent on that. The third table "
            "needs two boundaries. No choice of weights and threshold will do it, and that isn't a hunch; "
            "it can be checked exactly. For a long time this was taken to be the limit of a single neuron. "
            "If you've seen AI, Built, you'll recognise the perceptron, and the argument that sank it in "
            "1969."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(LaggedStart(FadeIn(in_l), *[GrowArrow(a_) for a_ in ins], FadeIn(body), FadeIn(rule), GrowArrow(out),
                                  FadeIn(out_l), lag_ratio=0.5), run_time=7.0)
            vo.wait_until("a")
            self.play(unit.animate.scale(0.62).move_to([0, 2.25, 0]), run_time=1.0)
            self.play(FadeIn(t_and, lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(t_or, lag_ratio=0.2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(t_xor, lag_ratio=0.2), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(cross), FadeIn(side[0]))
            self.play(FadeIn(side[1]), FadeIn(end))
        self.clear_scene()

    def coincidence(self):
        d = load("dendrites")
        head = heading(r"Time is an input too")
        delays, fires = np.asarray(d["delays"]), np.asarray(d["fires"])
        A = axes([0, 12], [0, 1.3], x_length=7.0, y_length=2.1, xticks=[0, 2, 4, 6, 8, 10, 12], yticks=[],
                 xlabel=r"delay between the two inputs (ms)", center=[-2.8, -1.75, 0])
        ax = A.ax
        bars = VGroup(*[Rectangle(width=(ax.c2p(0.25, 0)[0] - ax.c2p(0, 0)[0]) * 0.9, height=(ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1]),
                                  stroke_width=0, fill_color=(MODEL if f_ else "#2A3242"), fill_opacity=0.9).move_to(
                                      ax.c2p(x_ + 0.125, 0.5)) for x_, f_ in zip(delays, fires)])
        yes = label(r"fires", font_size=24, color=MODEL).move_to(ax.c2p(d["window"] / 2, 1.15))
        no = label(r"silent", font_size=24, color=GREY_A).move_to(ax.c2p(8.5, 1.15))
        # two small bumps: together, and apart
        def bumps(x0, gap, color):
            xs = np.linspace(0, 3.2, 120)
            def epsp(t0):
                t_ = np.clip(xs - t0, 0, None)
                return 1.0 * (np.exp(-t_ / 0.9) - np.exp(-t_ / 0.1)) * (xs >= t0)
            y_ = epsp(0.3) + epsp(0.3 + gap)
            pts = [np.array([x0 + x_, 0.75 + 1.0 * v_, 0]) for x_, v_ in zip(xs, y_)]
            line = VMobject(color=color, stroke_width=3.5).set_points_smoothly(pts)
            thr = DashedLine([x0, 0.75 + 1.0 * 1.25, 0], [x0 + 3.2, 0.75 + 1.0 * 1.25, 0], color=THRESH, stroke_width=2)
            return VGroup(line, thr)
        b1, b2 = bumps(-6.2, 0.08, MODEL), bumps(-2.3, 1.4, LEAK)
        b1_l = label(r"together: \ over the threshold", font_size=22, color=MODEL).next_to(b1, UP, buff=0.08)
        b2_l = label(r"apart: \ each falls short", font_size=22, color=LEAK).next_to(b2, UP, buff=0.08)
        side = VGroup(
            wrapped_label(rf"Each input alone lifts the cell {d['epsp_peak']:.0f} mV. \ The threshold is "
                          rf"{d['gap']:.0f} mV away.", 4.5, 26, WHITE),
            wrapped_label(rf"Together within {d['window']:.0f} ms, they fire it.", 4.5, 26, MODEL),
            wrapped_label(r"The membrane's time constant is the window. \ A leaky cell detects coincidences.",
                          4.5, 26, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.8, 0.0, 0])
        keep_in_frame(side)
        tag = psyche_tag()
        with self.voiceover(
            "That reading leaves something out, and it's time. The membrane forgets. So when inputs arrive "
            "matters as much as how many. <bookmark mark='a'/> Take the integrate-and-fire cell and two "
            f"inputs, each of which lifts the voltage by about {d['epsp_peak']:.0f} millivolts. The threshold "
            f"is {d['gap']:.0f} millivolts up. One input can't reach it. <bookmark mark='b'/> If the two "
            "arrive together, their effects stack and the cell fires. If they arrive a few milliseconds "
            "apart, the first has leaked away before the second comes, and nothing happens. "
            f"<bookmark mark='c'/> For this cell the window is about {d['window']:.0f} milliseconds. Inside "
            "it, fire. Outside, silence. <bookmark mark='d'/> So a leaky cell is a detector of things that "
            "happen at the same moment, and how leaky it is sets how strict it is about the moment. That's a "
            "computation no amount of adding without time can do. Your brain uses it to work out where a "
            "sound came from, by detecting which ear heard it first, to within tens of millionths of a "
            "second. That's in Part 15."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(Create(b2), FadeIn(b2_l), run_time=4.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(b1), FadeIn(b1_l), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(bars, lag_ratio=0.02), FadeIn(yes), FadeIn(no), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()

    def dendrites(self):
        d = load("dendrites")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        head = heading(r"A neuron with branches that decide for themselves")
        soma = Circle(radius=0.6, color=VOLT, stroke_width=3, fill_color="#111722", fill_opacity=1).move_to([-3.0, -0.3, 0])
        b1 = Line(soma.get_center() + np.array([-0.42, 0.42, 0]), [-5.6, 1.9, 0], color=GATE["n"], stroke_width=6)
        b2 = Line(soma.get_center() + np.array([-0.42, -0.42, 0]), [-5.6, -2.5, 0], color=GATE["m"], stroke_width=6)
        ins = VGroup(*[VGroup(Dot(b.point_from_proportion(pr), radius=0.11, color=c), label(str(k), font_size=24, color=c).next_to(
            b.point_from_proportion(pr), UL if b is b1 else DL, buff=0.1)) for b, c, prs, ks in (
                (b1, GATE["n"], (0.55, 0.85), (1, 2)), (b2, GATE["m"], (0.55, 0.85), (3, 4))) for pr, k in zip(prs, ks)])
        axon = Arrow(soma.get_right(), soma.get_right() + RIGHT * 1.6, color=VOLT, stroke_width=4, buff=0)
        cap = VGroup(label(r"a branch fires when both of its inputs are active", font_size=22, color=GREY_A),
                     label(r"the cell fires when either branch does", font_size=22, color=GREY_A)).arrange(
                         DOWN, aligned_edge=LEFT, buff=0.06).next_to(VGroup(b1, b2), DOWN, buff=0.25).align_to(b2, LEFT)
        keep_in_frame(VGroup(cap, b1, b2))
        # the sixteen input patterns: rows by inputs (1, 2), columns by inputs (3, 4)
        cell = 0.88
        grid = VGroup()
        for xi, yi in zip(x, y):
            r, c = 2 * xi[0] + xi[1], 2 * xi[2] + xi[3]
            sq = Square(cell, stroke_color=BACKGROUND, stroke_width=3, fill_color=(MODEL if yi else "#1B2333"),
                        fill_opacity=1).move_to([c * cell, -r * cell, 0])
            grid.add(sq)
        grid.move_to([3.6, -0.1, 0])
        gl, gt = grid.get_left()[0], grid.get_top()[1]
        rl = VGroup(*[label(t, font_size=20, color=GATE["n"]).next_to([gl, gt - (i + 0.5) * cell, 0], LEFT, buff=0.12)
                      for i, t in enumerate((r"neither", r"2", r"1", r"1 and 2"))])
        cl = VGroup(*[label(t, font_size=20, color=GATE["m"]).next_to([gl + (j + 0.5) * cell, gt, 0], UP, buff=0.1)
                      for j, t in enumerate((r"neither", r"4", r"3", r"3 and 4"))])
        tab = VGroup(grid, rl, cl)
        res = VGroup(
            label(rf"fires on {d['fires_on']} of the 16 patterns", font_size=26, color=MODEL),
            label(r"no single adding cell can match it", font_size=26, color=BAD),
        ).arrange(DOWN, buff=0.1).next_to(grid, DOWN, buff=0.3)
        end = label(r"One such neuron is a small network of two layers.", font_size=28, color=P.ACCENT).to_edge(
            DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        tag = note(r"computed: separability checked exactly").to_corner(DR, buff=0.2)
        with self.voiceover(
            "And there's a second thing the simple reading leaves out: the shape of the cell. Inputs don't "
            "all land in one place. They land on dendrites, and dendrites aren't passive wires. Many have "
            "their own voltage-dependent channels, <bookmark mark='z'/> and a branch can produce a local event "
            "of its own when enough of its inputs are active together. <bookmark mark='a'/> So picture a cell with two "
            "branches, two inputs on each. A branch fires locally only if both of its inputs are on. And the "
            "cell body fires if either branch has. <bookmark mark='b'/> Here are all sixteen patterns of "
            "input. The green ones fire the cell: inputs one and two together, or three and four together. "
            "Inputs one and three together do nothing, because they're on different branches. "
            "<bookmark mark='c'/> Now ask whether a cell that merely adds its four inputs could produce this "
            "table. It can't; we checked every possibility at once. <bookmark mark='d'/> What you're looking "
            "at is a network of two layers, with the branches as a hidden layer, inside a single cell. "
            "Whether real neurons compute like this, and how much, is this part's frontier. But the old "
            "picture of the neuron as a simple switch is the floor of what a neuron does, not the ceiling."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(FadeIn(soma), Create(b1), Create(b2), GrowArrow(axon), run_time=3.0)
            vo.wait_until("z")
            self.play(Flash(b1.point_from_proportion(0.6), color=THRESH, flash_radius=0.45), Indicate(b1, color=THRESH),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(ins, lag_ratio=0.2), FadeIn(cap), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(tab, lag_ratio=0.03), FadeIn(res[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(res[1], scale=1.1))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
