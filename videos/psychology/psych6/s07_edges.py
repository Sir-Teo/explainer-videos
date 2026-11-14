from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403


class Edges(VoiceoverScene):
    def construct(self):
        self.card()
        self.crab()
        self.step()
        self.bands()

    def card(self):
        card = chapter_card(6, r"Lateral inhibition", r"What does a cell gain by silencing its neighbours?",
                            lit={1957: r"Hartline and Ratliff"}, part=PART, scale=("circuit",), marr=("what", "how"))
        with self.voiceover(
            "Chapter six. Lateral inhibition."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def crab(self):
        head = heading(r"The eye of the horseshoe crab")
        xs = [-6.0 + 0.95 * i for i in range(7)]
        y0, yb = 0.9, -2.45
        units = VGroup(*[unit("", 0.3, VOLT).move_to([x, y0, 0]) for x in xs])
        links = VGroup(*[VGroup(Line([a + 0.32, y0, 0], [b - 0.32, y0, 0], color=INH, stroke_width=3),
                                Dot([a + 0.36, y0, 0], radius=0.07, color=INH),
                                Dot([b - 0.36, y0, 0], radius=0.07, color=INH)) for a, b in zip(xs, xs[1:])])
        fibres = VGroup(*[Line([x, y0 - 0.3, 0], [x, yb + 1.35, 0], color=GREY_C, stroke_width=3) for x in xs])
        base = Line([xs[0] - 0.4, yb, 0], [xs[-1] + 0.4, yb, 0], color=GREY_D, stroke_width=2)
        base_l = label(r"impulses per second in each fibre", font_size=22, color=GREY_B).next_to(base, DOWN, buff=0.1)
        ia, ib = 3, 4
        names = VGroup(label(r"A", font_size=26, color=EXC).move_to(units[ia]),
                       label(r"B", font_size=26, color=DATA).move_to(units[ib]))
        ra, rb = ValueTracker(0.0), ValueTracker(0.0)

        def bar(x, tr, col):
            return always_redraw(lambda: Rectangle(width=0.5, height=max(1.2 * tr.get_value(), 0.01), stroke_width=0,
                                                   fill_color=col, fill_opacity=0.9).move_to(
                [x, yb + max(1.2 * tr.get_value(), 0.01) / 2, 0]))

        bar_a, bar_b = bar(xs[ia], ra, EXC), bar(xs[ib], rb, DATA)

        def light(x, n=1):
            return VGroup(*[Arrow([x + 0.12 * (k - (n - 1) / 2), y0 + 1.5, 0], [x + 0.12 * (k - (n - 1) / 2), y0 + 0.4, 0],
                                  color=THRESH, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.2)
                            for k in range(n)])

        la, lb, lb2 = light(xs[ia]), light(xs[ib]), light(xs[ib], 3)
        side = VGroup(
            wrapped_label(r"light on A alone: \ its fibre fires steadily", 5.0, 27, EXC),
            wrapped_label(r"light B as well: \ A slows, though A's light is unchanged", 5.0, 27, DATA),
            wrapped_label(r"brighter on B: \ A slows more, \ in proportion to B's firing", 5.0, 27, DATA),
            MathTex(r"r_i \;=\; e_i \;-\; \sum_{j \neq i} k_{ij}\, r_j", font_size=44, color=INH),
            wrapped_label(r"each unit's response: \ its own excitation, less a weighted sum of its neighbours' "
                          r"responses", 5.0, 26, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.1, -0.3, 0])
        eye = VGroup()
        for row in range(-4, 5):
            for col in range(-6, 7):
                px, py = 0.34 * (col + 0.5 * (row % 2)), 0.3 * row
                if (px / 2.2) ** 2 + (py / 1.25) ** 2 <= 1.0:
                    eye.add(Circle(radius=0.14, color=GREY_B, stroke_width=1.5, fill_color="#1A2130",
                                   fill_opacity=1).move_to([px, py, 0]))
        eye.move_to([4.0, 0.5, 0])
        eye_l = wrapped_label(r"one compound eye: \ about a thousand receptor units, \ each with its own nerve "
                              r"fibre", 5.0, 27, WHITE).next_to(eye, DOWN, buff=0.35)
        intro = VGroup(eye, eye_l)
        src = historical_tag(archive.HARTLINE_RATLIFF_1957.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The first circuit comes from an animal that has hardly changed in hundreds of millions of years. "
            "The horseshoe crab has a compound eye of about a thousand receptor units. Each has its own nerve "
            "fibre, and the fibres are large enough to record from one at a time. Keffer Hartline spent "
            "decades doing exactly that. <bookmark mark='a'/> Shine a spot of light on one unit, A, and its "
            "fibre fires at a steady rate. <bookmark mark='b'/> Now light its neighbour, B, as well. A's rate "
            "drops. Nothing about the light on A has changed. Its neighbour is inhibiting it. "
            "<bookmark mark='c'/> Make B's light brighter, and A drops further. In 1957 Hartline and Floyd "
            "Ratliff showed that the relation is about as simple as it could be. The inhibition on each unit "
            "is proportional to how fast the other one is firing. <bookmark mark='d'/> And it's mutual. A does "
            "the same to B. So each unit's response is its own excitation, less a weighted sum of its "
            "neighbours' responses, with nearer neighbours counting for more. This is lateral inhibition, and "
            "Hartline shared a Nobel Prize for it in 1967. These equations were measured in the animal. So we "
            "can compute with them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(intro))
            self.play(FadeIn(VGroup(fibres, units, links, base, base_l)))
            self.add(bar_a, bar_b)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.6)
            self.play(FadeIn(la), FadeIn(names[0]), ra.animate.set_value(1.0), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(lb), FadeIn(names[1]), rb.animate.set_value(0.75), ra.animate.set_value(0.75),
                      FadeIn(side[1]), run_time=1.5)
            self.play(Indicate(links[ia], color=WHITE, scale_factor=1.3))
            vo.wait_until("c")
            self.play(ReplacementTransform(lb, lb2), rb.animate.set_value(1.25), ra.animate.set_value(0.5),
                      FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Write(side[3]), FadeIn(side[4]))
            self.play(LaggedStart(*[Indicate(k, color=WHITE, scale_factor=1.2) for k in links], lag_ratio=0.15),
                      run_time=2.5)
        self.clear_scene()

    def _row(self, d, key, out, center, width=8.0, yr=(0, 2.3), yticks=(0, 1, 2), y_length=3.4, smooth=False,
             strip_h=0.75):
        """Units 8 to 72 of the row (its two ends, where a unit has neighbours on one side only, are left off):
        the light as a grey strip, and axes with the light (dashed) and the responses."""
        a, b = 8, 72
        A = axes([a, b], list(yr), x_length=width, y_length=y_length, xticks=[20, 40, 60], yticks=list(yticks),
                 yfmt=lambda v: f"{v:g}", xlabel=r"position along the row of units", ylabel=r"", center=center)
        ax = A.ax
        strip = light_strip(d[key][a:b], width=np.linalg.norm(ax.c2p(b, 0) - ax.c2p(a, 0)), height=strip_h,
                            smooth=smooth)
        strip.move_to([(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2, ax.c2p(a, yr[1])[1] + 0.25 + strip_h / 2, 0])
        x = d["x"][a:b] + 0.5
        inp = DashedVMobject(curve(ax, x, d[key][a:b], LEAK, stroke_width=3), num_dashes=60)
        outp = trace(ax, x, d[out][a:b], MODEL)
        return A, ax, strip, inp, outp

    def step(self):
        d = load("lateral")
        head = heading(r"A row of units, \ shown an edge of light")
        A, ax, strip, inp, outp = self._row(d, "step", "r_step", [-2.6, -1.0, 0])
        lg = legend([(LEAK, r"the light"), (MODEL, r"the units' responses")], font_size=24)
        lg.next_to(ax.c2p(8, 2.3), DR, buff=0.15)
        m = len(d["x"]) // 2
        hi_pt, lo_pt = ax.c2p(m + 0.5, d["bright_band"]), ax.c2p(m - 0.5, d["dark_band"])
        marks = VGroup(label(rf"{d['bright_band']:.2f}", font_size=24, color=THRESH).next_to(hi_pt, UR, buff=0.08),
                       label(rf"{d['dark_band']:.2f}", font_size=24, color=THRESH).next_to(lo_pt, DL, buff=0.08))
        side = VGroup(
            wrapped_label(rf"far from the edge: \ {d['low']:.2f} and {d['high']:.2f}, \ still a ratio of "
                          rf"{d['high'] / d['low']:.1f}", 4.6, 27, WHITE),
            wrapped_label(r"just on the bright side: \ dim neighbours, less inhibition, a stronger response", 4.6,
                          27, WHITE),
            wrapped_label(r"just on the dark side: \ bright neighbours, more inhibition, a weaker one", 4.6, 27,
                          WHITE),
            wrapped_label(rf"across the edge: \ a ratio of {d['edge_out']:.1f} in the responses, \ "
                          rf"{d['contrast_in']:.0f} in the light", 4.6, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, -0.4, 0])
        tag = psyche_tag()
        with self.voiceover(
            "Take a row of eighty such units, and show it an edge. <bookmark mark='a'/> Dim light on the left "
            "half, twice as bright on the right. The grey bar at the top is the light itself. "
            "<bookmark mark='b'/> Here's what the units do. Far from the edge, each one is inhibited equally "
            f"from both sides, and the response is just a scaled copy of the light: {d['low']:.2f} on the dim "
            f"side, {d['high']:.2f} on the bright side. Still a ratio of two. <bookmark mark='c'/> At the edge "
            "it's different. The last unit on the bright side has dim neighbours on one side. So it's "
            f"inhibited less than its fellows, and it responds more: {d['bright_band']:.2f}. "
            "<bookmark mark='d'/> The last unit on the dark side has bright neighbours. It's inhibited more, "
            f"and it responds less: {d['dark_band']:.2f}. <bookmark mark='e'/> Across the edge, the ratio in "
            f"the responses is {d['edge_out']:.1f}, where the light's was two. The circuit has exaggerated "
            "the edge. Hartline and Ratliff went on to record just this pattern from the crab's own eye."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(strip), Create(inp), FadeIn(lg[0]))
            vo.wait_until("b")
            self.play(Create(outp), FadeIn(lg[1]), run_time=3.0, rate_func=linear)
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(marks[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(marks[1]), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()

    def bands(self):
        d = load("lateral")
        stage = demo_stage(13.2, 6.5, tag=r"On you: \ Mach's bands (1865)", center=[0, -0.3, 0])
        c = stage.box.get_center()
        A, ax, strip, _, outp = self._row(d, "ramp", "r_ramp", c + np.array([-2.0, -1.55, 0]), width=8.4,
                                          yr=(0.4, 1.3), yticks=(0.6, 0.9, 1.2), y_length=2.3, smooth=True,
                                          strip_h=1.5)
        strip.shift(UP * 0.75)
        foot, top = d["foot"], d["top"]
        # the light's own profile, drawn under the strip: flat, a ramp, flat
        y_lo, y_hi = strip.get_bottom()[1] - 0.6, strip.get_bottom()[1] - 0.2
        prof = VMobject(color=LEAK, stroke_width=3).set_points_as_corners(
            [[ax.c2p(8, 0)[0], y_lo, 0], [ax.c2p(foot, 0)[0], y_lo, 0], [ax.c2p(top, 0)[0], y_hi, 0],
             [ax.c2p(72, 0)[0], y_hi, 0]])
        prof_l = label(r"the light", font_size=22, color=LEAK).next_to(prof.get_start(), UR, buff=0.08)
        out_l = label(r"the model's responses", font_size=22, color=MODEL).move_to(ax.c2p(20, 1.15))
        arrows = VGroup(*[Arrow([ax.c2p(k, 0)[0], strip.get_top()[1] + 0.45, 0], [ax.c2p(k, 0)[0], strip.get_top()[1], 0],
                                color=THRESH, stroke_width=4, buff=0.03, max_tip_length_to_length_ratio=0.4)
                          for k in (foot - 0.5, top + 0.5)])
        dots = VGroup(Dot(ax.c2p(foot - 0.5, d["ramp_dip"]), radius=0.07, color=THRESH),
                      Dot(ax.c2p(top + 0.5, d["ramp_peak"]), radius=0.07, color=THRESH))
        side = VGroup(
            wrapped_label(r"at the foot of the ramp: \ a thin line darker than the dark side", 3.5, 26, WHITE),
            wrapped_label(r"at its top: \ a thin line brighter than the bright side", 3.5, 26, WHITE),
            wrapped_label(r"neither is in the light", 3.5, 26, THRESH),
            wrapped_label(r"the model: \ a dip at the foot, \ a peak at the top", 3.5, 26, MODEL),
            wrapped_label(r"uniform light: \ a small response. \ A change: \ a large one", 3.5, 26, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to(c + np.array([4.55, -0.25, 0]))
        tag = psyche_tag().next_to(stage.box.get_corner(DR), UL, buff=0.12)
        with self.voiceover(
            "You can see this circuit's signature in your own vision. The physicist Ernst Mach described it in "
            "1865. <bookmark mark='a'/> Here's a strip that's dark on the left and light on the right, with a "
            "short ramp between. The line under it is the actual light: flat, then a ramp, then flat. "
            "<bookmark mark='b'/> Look at the foot of the ramp, where it begins. Most people see a thin line "
            "there that's darker than the dark side. And at the top of the ramp, a thin line that's brighter "
            "than the bright side. Neither one is in the light. <bookmark mark='c'/> Now the model: the same "
            "row of units, shown this ramp. A dip at the foot, and a peak at the top. These are Mach bands, "
            "and lateral inhibition predicts them. <bookmark mark='d'/> What is it for? Where the light is "
            "uniform, every unit is held down by its neighbours, and the response is small. The circuit "
            "spends little on what's the same everywhere, and it shouts where something changes. Edges are "
            "where the information is. <bookmark mark='e'/> One caution before we go on. At a perfectly "
            "sharp step, the model predicts bands too, and people mostly don't see any. This is a model of a "
            "crab's eye. Hold that thought for the next chapter."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(strip), Create(prof), FadeIn(prof_l))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(side[0]))
            self.wait(2.0)
            self.play(GrowArrow(arrows[1]), FadeIn(side[1]))
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(out_l))
            self.play(Create(outp), run_time=3.0, rate_func=linear)
            self.play(FadeIn(dots, scale=1.5), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4], shift=UP * 0.1))
            vo.wait_until("e")
        self.clear_scene()
