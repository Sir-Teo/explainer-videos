from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Workspace(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"The global workspace", r"Is consciousness the brain broadcasting to itself?",
                            lit=(1988,), part=PART)
        with self.voiceover("Chapter eight. The global workspace."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theatre()
        self.ignition()
        self.masking()

    def theatre(self):
        hc = history_card(1988, r"Bernard Baars", r"\textit{A Cognitive Theory of Consciousness}", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        hub = VGroup(Circle(radius=0.8, color=FUNC, fill_opacity=0.15), label(r"workspace", font_size=20,
                                                                             color=FUNC)).move_to([-1.8, -0.6, 0])
        mods = [r"vision", r"hearing", r"memory", r"language", r"motor", r"evaluation"]
        nodes, spokes = VGroup(), VGroup()
        for k, m in enumerate(mods):
            ang = PI / 2 + k * TAU / 6
            pos = hub.get_center() + 2.4 * np.array([np.cos(ang), np.sin(ang), 0])
            nodes.add(VGroup(RoundedRectangle(width=1.6, height=0.6, corner_radius=0.15, color=GREY_B),
                             label(m, font_size=17, color=GREY_A)).move_to(pos))
            spokes.add(Line(hub.get_center(), pos, color=GREY_D, stroke_width=2).set_z_index(-1))
        rows = stack([(r"many specialists working unconsciously, \ in parallel", GREY_A),
                      (r"a limited-capacity stage: \ what wins it is broadcast to all", FUNC),
                      (r"conscious \ = \ globally available \ (Dehaene, \ Kerszberg and Changeux, \ 1998)", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=4.2, buff=0.3).move_to([4.6, 0.0, 0])
        with self.voiceover(
            "The leading scientific theory began with a metaphor. <bookmark mark='a'/>Bernard Baars, in 1988, "
            "pictured the mind as a theatre: many specialist processes, vision, hearing, memory, language, working "
            "in parallel and out of sight. <bookmark mark='b'/>And a stage of limited capacity, the global "
            "workspace. Whatever wins a place on it is broadcast to every specialist at once. "
            "<bookmark mark='c'/>Being conscious of something, on this theory, is its being globally available. "
            "Stanislas Dehaene, Michel Kerszberg and Jean-Pierre Changeux turned the metaphor into a neural model "
            "in 1998, with long-range neurons in the prefrontal and parietal cortex as the stage."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.15), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hub), Create(spokes), FadeIn(rows[1]))
            self.play(*[Indicate(n, color=FUNC, scale_factor=1.05) for n in nodes])
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def ignition(self):
        d = load("workspace")
        head = label(r"Ignition, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["strength"] == 30.0 and d["dt_trace"] == 5 and len(d["trace_sub"]) == 120
        eq = MathTex(r"\tau\,\dot w \;=\; -w \;+\; 100\,\sigma\!\big(g\,(I + r\,w - \theta)\big)", font_size=30,
                     color=FUNC).move_to([0, 2.5, 0])
        ax = Axes(x_range=[0, 600, 100], y_range=[0, 110, 50], x_length=8.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 18}).move_to([-1.4, -0.6, 0])
        xl = label(r"time after the stimulus \ (ms)", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"workspace activity", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.12)
        sub = VMobject(color=GREY_B, stroke_width=3).set_points_as_corners(
            [ax.c2p(5 * k, v) for k, v in enumerate(d["trace_sub"])])
        sup = VMobject(color=FUNC, stroke_width=3).set_points_as_corners(
            [ax.c2p(5 * k, v) for k, v in enumerate(d["trace_sup"])])
        m30 = DashedLine(ax.c2p(30, 0), ax.c2p(30, 105), color=GREY_B, stroke_width=1.5)
        m80 = DashedLine(ax.c2p(80, 0), ax.c2p(80, 105), color=FUNC, stroke_width=1.5)
        side = stack([(r"masked at 30 ms: \ activity fades", GREY_B),
                      (r"masked at 80 ms: \ the loop takes over \ and holds", FUNC),
                      (r"recurrent excitation $r\,w$: \ two stable states, \ and a threshold between", SIG)],
                     font_size=19, aligned_edge=LEFT, width=4.0, buff=0.3).move_to([4.7, -0.4, 0])
        with self.voiceover(
            "The Reasoner builds the core of the neural model in one equation. <bookmark mark='a'/>A workspace "
            "population with activity w is driven by the stimulus, I, and by its own recurrent excitation, r times "
            "w, through a steep sigmoid. A stimulus is shown, then a mask cuts it off. "
            "<bookmark mark='b'/>Mask it after thirty milliseconds, and activity rises a little, then fades away. "
            "<bookmark mark='c'/>Mask it after eighty, and before the mask arrives the loop has crossed its "
            "threshold. The recurrent excitation takes over and holds the activity high long after the stimulus is "
            "gone. <bookmark mark='d'/>The loop has two stable states, low and high, with a threshold between. "
            "Crossing it is called ignition, and on this theory it is the moment of conscious access."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(Create(m30), Create(sub), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(m80), Create(sup), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def masking(self):
        d = load("workspace")
        head = label(r"A masking curve, \ and all-or-none access", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["rows"]
        assert [r["soa"] for r in rows] == list(range(10, 121, 10)) and rows[0]["trials"] == 200
        assert [r["seen"] for r in rows] == [0, 0, 0, 24, 81, 141, 169, 195, 198, 200, 200, 200]
        assert d["probe_soa"] == 50 and d["late_low"] == 136 and d["late_high"] == 64
        ax = Axes(x_range=[0, 120, 20], y_range=[0, 1, 0.5], x_length=5.6, y_length=3.4, tips=False,
                  axis_config={"color": GREY_B, "font_size": 18},
                  x_axis_config={"include_numbers": True},
                  y_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 1}}
                  ).move_to([-3.5, -0.3, 0])
        xl = label(r"stimulus--mask delay \ (ms)", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"share of 200 trials seen", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.12).shift(
            RIGHT * 1.1)
        pts = [ax.c2p(r["soa"], r["seen"] / r["trials"]) for r in rows]
        curve = VMobject(color=FUNC, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=FUNC) for p in pts])
        h = d["late_hist"]
        bx = Axes(x_range=[0, 110, 50], y_range=[0, 140, 70], x_length=4.6, y_length=3.0, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 18}).move_to([3.6, -0.2, 0])
        bars = VGroup(*[Rectangle(width=bx.x_axis.unit_size * 10 * 0.9, height=max(bx.y_axis.unit_size * c, 0.001),
                                  fill_color=FUNC if k >= 8 else GREY_B, fill_opacity=0.8, stroke_width=0
                                  ).move_to(bx.c2p(10 * k + 5, 0), aligned_edge=DOWN) for k, c in enumerate(h)])
        bl = label(r"activity at 400 ms, \ masked at 50 ms", font_size=17, color=GREY_A).next_to(bx, UP, buff=0.15)
        bxl = label(r"low: \ 136 \quad high: \ 64 \quad between: \ none", font_size=18, color=SIG).next_to(
            bx.x_axis, DOWN, buff=0.4)
        foot = label(r"like the human curve \ (Del Cul, \ Baillet and Dehaene, \ 2007): \ a threshold near 50 ms, \ "
                     r"and access that is all or none", font_size=19, color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now add a little noise, and run two hundred trials at each delay between stimulus and mask. "
            "<bookmark mark='a'/>Up to thirty milliseconds, the workspace never ignites. At forty, it ignites on "
            "twenty four trials of two hundred; at fifty, eighty one; at sixty, a hundred and forty one; by ninety, "
            "almost always. The curve is a steep sigmoid. <bookmark mark='b'/>Look at the trials at the threshold "
            "delay of fifty milliseconds. Four hundred milliseconds in, the activity is either low, on a hundred "
            "and thirty six trials, or high, on sixty four. Nothing in between. <bookmark mark='c'/>That is the "
            "signature the theory predicts, and that Antoine Del Cul, Sylvain Baillet and Dehaene reported in 2007: "
            "subjective visibility jumps at a threshold near fifty milliseconds, and late brain activity is all or "
            "none. The toy produces the shape from nothing but a loop that can hold itself on. Whether the loop "
            "explains the seeing, or only the reporting, is the question from chapter two."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), LaggedStart(*[GrowFromCenter(x) for x in dots], lag_ratio=0.1), run_time=3)
            vo.wait_until("b")
            self.play(Create(bx), FadeIn(bl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1))
            self.play(FadeIn(bxl))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
