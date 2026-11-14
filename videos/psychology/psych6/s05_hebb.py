from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403

LIM = 2.3  # half-width of the weight plane


class Hebb(VoiceoverScene):
    def construct(self):
        self.card()
        self.postulate()
        self.diverges()
        self.repair()
        self.settles()

    def card(self):
        card = chapter_card(4, r"Hebb's rule", r"What rule should change a synapse?", lit={1949: r"Hebb's postulate"},
                            part=PART, scale=("neuron", "circuit"), marr=("how",))
        with self.voiceover(
            "Chapter four. Hebb's rule."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def postulate(self):
        head = heading(r"1949: \ a guess about learning")
        q = quote_card(r"``When an axon of cell A is near enough to excite a cell B and repeatedly or persistently "
                       r"takes part in firing it, some growth process or metabolic change takes place in one or "
                       r"both cells such that A's efficiency, as one of the cells firing B, is increased.''",
                       r"D. O. Hebb, \emph{The Organization of Behavior} (1949)", width=12.0, font_size=28)
        q.move_to([0, 1.55, 0])
        a, b = unit("A", 0.5, EXC, 30).move_to([-5.2, -1.5, 0]), unit("B", 0.5, VOLT, 30).move_to([-2.2, -1.5, 0])
        w = ValueTracker(3.0)
        conn = always_redraw(lambda: Arrow(a.get_right(), b.get_left(), color=RULE, stroke_width=w.get_value(),
                                           buff=0.08, max_tip_length_to_length_ratio=0.14))
        rule = MathTex(r"\Delta w \;=\; \eta\, x\, y", font_size=54, color=RULE).move_to([-3.7, -2.75, 0])
        needs = VGroup(
            label(r"what the synapse has to know", font_size=28, color=GREY_A),
            label(r"$x$: \ was my input active?", font_size=30, color=EXC),
            label(r"$y$: \ did my cell fire?", font_size=30, color=VOLT),
            label(r"and nothing else: \ the rule is local", font_size=30, color=P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.2, -1.9, 0])
        src = historical_tag(archive.HEBB_1949.cite)
        with self.voiceover(
            "In 1949 the Canadian psychologist Donald Hebb published a book, The Organization of Behavior, and "
            "in it he made a guess. <bookmark mark='a'/> When an axon of cell A is near enough to excite a cell "
            "B, and repeatedly or persistently takes part in firing it, some growth process or metabolic change "
            "takes place in one or both cells, such that A's efficiency, as one of the cells firing B, is "
            "increased. <bookmark mark='b'/> In short: if A keeps helping to fire B, the synapse from A to B "
            "gets stronger. Nobody had seen a synapse do this. Hebb needed it, because he wanted to explain how "
            "experience could leave a lasting trace in a brain, and this was the simplest rule that would. "
            "<bookmark mark='c'/> As an equation: the change in the weight is the input, times the output, "
            "times a small learning rate. <bookmark mark='d'/> Look at what kind of rule that is. The synapse "
            "needs to know two things. Was my input active? Did my cell fire? Both are available right there, "
            "at the synapse. No supervisor. No error signal from somewhere else. A rule like that is called "
            "local, and locality is the constraint that any theory of learning in a brain has to respect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(q[0]), FadeIn(q[1]), FadeIn(q.src), Write(q.body), run_time=10.0)
            vo.wait_until("b")
            self.play(FadeIn(a), FadeIn(b), FadeIn(conn))
            for _ in range(3):
                self.play(Indicate(a, color=WHITE, scale_factor=1.15), run_time=0.45)
                self.play(Indicate(b, color=WHITE, scale_factor=1.15), w.animate.increment_value(3.0), run_time=0.6)
            vo.wait_until("c")
            self.play(Write(rule))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in needs], lag_ratio=0.7), run_time=7.0)
        self.clear_scene()

    # ------------------------------------------------------------------------------------------------------------
    def _stage(self, h):
        """The cloud of inputs on the left and the plane of weights on the right."""
        A = axes([-7, 7], [-3.5, 3.5], x_length=6.4, y_length=3.2, xticks=[-6, -3, 0, 3, 6], yticks=[-3, 0, 3],
                 xlabel=r"input 1", ylabel=r"input 2", center=[-3.6, -0.55, 0])
        ax = A.ax
        cloud = VGroup(*[Dot(ax.c2p(x, y), radius=0.028, color=GREY_B, fill_opacity=0.75) for x, y in h["cloud"]])
        B = axes([-LIM, LIM], [-LIM, LIM], x_length=3.7, y_length=3.7, xticks=[-2, -1, 0, 1, 2],
                 yticks=[-2, -1, 0, 1, 2], xlabel=r"weight 1", ylabel=r"weight 2", center=[3.9, -0.6, 0])
        bx = B.ax
        circle = Circle(radius=np.linalg.norm(bx.c2p(1, 0) - bx.c2p(0, 0)), color=GREY_C, stroke_width=2)
        circle.move_to(bx.c2p(0, 0))
        circle_l = label(r"length 1", font_size=20, color=GREY_B).next_to(circle, UP, buff=0.05).shift(LEFT * 0.9)
        return A, ax, cloud, B, bx, VGroup(circle, circle_l)

    def _run(self, ax, bx, path, color, k):
        """The current weight direction as a line through the cloud, and the path so far in the weight plane."""
        def w_now():
            return path[min(int(k.get_value()), len(path) - 1)]

        def direction():
            w = w_now()
            u = w / max(np.linalg.norm(w), 1e-9)
            r = min(6.6 / max(abs(u[0]), 1e-9), 3.3 / max(abs(u[1]), 1e-9))
            return Line(ax.c2p(*(-r * u)), ax.c2p(*(r * u)), color=color, stroke_width=4)

        def trail():
            n = min(int(k.get_value()), len(path) - 1) + 1
            pts = [bx.c2p(*w) for w in path[:n] if abs(w[0]) < LIM and abs(w[1]) < LIM]
            m = VMobject(color=color, stroke_width=3.5)
            if len(pts) > 1:
                m.set_points_as_corners(pts)
            return m

        def tip():
            w = w_now()
            r = max(abs(w[0]), abs(w[1]))
            if r > LIM:
                w = w * (LIM / r)
            return Dot(bx.c2p(*w), radius=0.09, color=color)

        return always_redraw(direction), always_redraw(trail), always_redraw(tip), w_now

    def diverges(self):
        h = load("hebb")
        sgn = float(np.sign(h["oja_w"][0]))
        path = h["hebb_path"] * sgn
        head = heading(r"Run Hebb's rule on a unit with two inputs")
        eq = MathTex(r"y = w_1 x_1 + w_2 x_2", r"\qquad\quad", r"\Delta w_i = \eta\, x_i\, y", font_size=38)
        eq[0].set_color(VOLT)
        eq[2].set_color(RULE)
        eq.move_to([-3.4, 2.3, 0])
        A, ax, cloud, B, bx, ring = self._stage(h)
        k = ValueTracker(0)
        line, trail, tip, w_now = self._run(ax, bx, path, BAD, k)
        size = DecimalNumber(0.0, num_decimal_places=1, font_size=40, color=BAD)
        size.add_updater(lambda m: m.set_value(float(np.linalg.norm(w_now()))))
        size_g = VGroup(label(r"length of the weights:", font_size=26, color=GREY_A), size).arrange(RIGHT, buff=0.2)
        size_g.move_to([3.9, 2.3, 0])
        end = wrapped_label(rf"After {h['hebb_steps_to_50']} steps the weights are fifty times their natural size, "
                            r"and still accelerating. \ Hebb's rule has no way to stop.", 8.8, 27, P.ACCENT)
        end.next_to(A, DOWN, buff=0.2).to_edge(LEFT, buff=0.4)
        tag = psyche_tag()
        with self.voiceover(
            "Let's run it. Give a model cell two inputs. <bookmark mark='a'/> Each dot on the left is one "
            "moment: the activity of input one across, and of input two upwards. The two are correlated. When "
            "one is high the other tends to be. <bookmark mark='b'/> On the right is the cell's pair of "
            "weights, starting small. The circle marks a total length of one. Now apply Hebb's rule at every "
            "moment. <bookmark mark='c'/> The weights turn toward the long axis of the cloud, the direction "
            "in which the inputs vary most. That part is good, and I'll say why in a minute. "
            "<bookmark mark='d'/> But watch their length. Stronger weights give a bigger output. A bigger "
            "output gives a bigger change in the weights. That's a positive feedback, and it runs away. "
            f"After {h['hebb_steps_to_50']} steps the weights are fifty times their natural size and still "
            "accelerating. <bookmark mark='e'/> Hebb's rule, as he stated it, has no way to stop. Every "
            "synapse grows until it hits whatever ceiling biology imposes. And a brain with every synapse at "
            "its ceiling has learned nothing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(cloud, lag_ratio=0.002), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(ring), FadeIn(tip), FadeIn(size_g))
            self.add(line, trail)
            vo.wait_until("c")
            self.play(k.animate.set_value(70), run_time=6.0, rate_func=linear)
            vo.wait_until("d")
            self.play(k.animate.set_value(len(path) - 1), run_time=9.0, rate_func=linear)
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def repair(self):
        head = heading(r"The repair: \ keep the total length fixed")
        l1 = VGroup(label(r"one step of Hebb, then shrink back to length 1", font_size=28, color=GREY_A),
                    MathTex(r"w \;\leftarrow\; \frac{w + \eta\, y\, x}{\lVert w + \eta\, y\, x \rVert}",
                            font_size=44)).arrange(DOWN, buff=0.2)
        l2 = VGroup(label(r"for a small learning rate, \ using $\lVert w \rVert = 1$ and $w \cdot x = y$",
                          font_size=28, color=GREY_A),
                    MathTex(r"\frac{1}{\lVert w + \eta\, y\, x \rVert} \;\approx\; 1 - \eta\, y^2",
                            font_size=44)).arrange(DOWN, buff=0.2)
        l3 = MathTex(r"\Delta w \;=\;", r"\eta\, y\, x", r"\;-\;", r"\eta\, y^2\, w", font_size=56)
        l3[1].set_color(RULE)
        l3[3].set_color(INH)
        col = VGroup(l1, l2, l3).arrange(DOWN, buff=0.5).move_to([0, 0.1, 0])
        b1 = VGroup(Brace(l3[1], DOWN, color=RULE, buff=0.1))
        b1.add(label(r"Hebb", font_size=26, color=RULE).next_to(b1[0], DOWN, buff=0.08))
        b2 = VGroup(Brace(l3[3], DOWN, color=INH, buff=0.1))
        b2.add(label(r"forgetting, \ faster when the cell is active", font_size=26, color=INH).next_to(
            b2[0], DOWN, buff=0.08).shift(RIGHT * 1.6))
        name = label(r"Oja's rule (1982): \ still local", font_size=30, color=P.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The repair is simple to state. After each step of Hebb's rule, shrink all the weights back to a "
            "fixed total length. <bookmark mark='a'/> Written out, that's a division by the new length. "
            "<bookmark mark='b'/> For a small learning rate you can expand it, and the division becomes a "
            "factor of one minus the learning rate times the output squared. <bookmark mark='c'/> Multiply "
            "through, keep the terms of first order, and here's what's left. The change in a weight is still "
            "input times output: Hebb's term. <bookmark mark='d'/> But now there's a second term, which takes "
            "away a little of every weight, in proportion to the square of the output. The more active the "
            "cell, the faster all of its synapses decay. <bookmark mark='e'/> This is Oja's rule, from 1982. "
            "And it's still local. The synapse needs its input, its cell's output, and its own strength."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(l1[0]), Write(l1[1]))
            vo.wait_until("b")
            self.play(FadeIn(l2[0]), Write(l2[1]))
            vo.wait_until("c")
            self.play(Write(l3[:2]), FadeIn(b1))
            vo.wait_until("d")
            self.play(Write(l3[2:]), FadeIn(b2))
            vo.wait_until("e")
            self.play(FadeIn(name, shift=UP * 0.1))
        self.clear_scene()

    def settles(self):
        h = load("hebb")
        sgn = float(np.sign(h["oja_w"][0]))
        path, pc = h["oja_path"] * sgn, h["pc"] * sgn
        head = heading(r"Oja's rule on the same inputs")
        A, ax, cloud, B, bx, ring = self._stage(h)
        k = ValueTracker(0)
        line, trail, tip, w_now = self._run(ax, bx, path, MODEL, k)
        target = Circle(radius=0.17, color=THRESH, stroke_width=3).move_to(bx.c2p(*pc))
        target_l = label(r"first principal component", font_size=22, color=THRESH).next_to(target, UR, buff=0.05)
        keep_in_frame(target_l)
        size = DecimalNumber(0.0, num_decimal_places=2, font_size=40, color=MODEL)
        size.add_updater(lambda m: m.set_value(float(np.linalg.norm(w_now()))))
        size_g = VGroup(label(r"length of the weights:", font_size=26, color=GREY_A), size).arrange(RIGHT, buff=0.2)
        size_g.move_to([3.9, 2.3, 0])
        facts = VGroup(
            label(rf"the direction that carries {pct(h['share'])} of the inputs' variance", font_size=27,
                  color=THRESH),
            label(r"found by one cell adjusting its own synapses", font_size=27, color=MODEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(A, DOWN, buff=0.2).to_edge(LEFT, buff=0.4)
        end = label(r"correlation in, \ structure out", font_size=38, color=P.ACCENT).move_to([-3.4, 2.3, 0])
        tag = psyche_tag()
        with self.voiceover(
            "Run it on the same inputs. <bookmark mark='a'/> The weights turn toward the long axis, as before. "
            "And this time they stop, on the circle, at a length of "
            f"{h['oja_final_norm']:.2f}. <bookmark mark='b'/> Where they stop has a name. It's the first "
            "principal component of the inputs. Of all the ways to combine these inputs into one number, it's "
            "the combination that varies the most, and so the one that tells you the most about them. Here it "
            f"carries {100 * h['share']:.0f} percent of the variance. <bookmark mark='c'/> Statisticians find "
            "this direction with matrix algebra. One model neuron found it by adjusting its own synapses, with "
            "nobody telling it what to look for. <bookmark mark='d'/> That's the general lesson. Correlation "
            "in, structure out. A cell that strengthens the inputs that are active together ends up as a "
            "detector for whatever tends to occur together in its world. That is a kind of learning that "
            "needs no teacher, and it's the kind Hebb was after."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(cloud), FadeIn(B), FadeIn(ring), FadeIn(tip),
                      FadeIn(size_g))
            self.add(line, trail)
            vo.wait_until("a")
            self.play(k.animate.set_value(40), run_time=6.0, rate_func=linear)
            self.play(k.animate.set_value(len(path) - 1), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(target, scale=2.0), FadeIn(target_l), FadeIn(facts[0]))
            vo.wait_until("c")
            self.play(FadeIn(facts[1]))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
