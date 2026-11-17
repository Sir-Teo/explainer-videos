from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403


class Synapse(VoiceoverScene):
    def construct(self):
        self.card()
        self.steps()
        self.quanta()
        self.kinds()

    def card(self):
        card = chapter_card(1, r"The chemical synapse", r"What happens in the gap?", lit={1921: "Loewi"}, part=PART,
                            scale=("molecule", "neuron"), marr=("tissue",))
        with self.voiceover(
            "Chapter one. The chemical synapse."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def steps(self):
        head = heading(r"One synapse, \ drawn large")
        cx = -3.5
        axon = VGroup(Line([cx - 0.45, 3.0, 0], [cx - 0.45, 1.7, 0], color=VOLT, stroke_width=4),
                      Line([cx + 0.45, 3.0, 0], [cx + 0.45, 1.7, 0], color=VOLT, stroke_width=4))
        bulb = RoundedRectangle(width=3.9, height=1.75, corner_radius=0.5, color=VOLT, stroke_width=4,
                                fill_color="#111722", fill_opacity=1).move_to([cx, 0.9, 0])
        post = RoundedRectangle(width=4.7, height=1.7, corner_radius=0.4, color=VOLT, stroke_width=4,
                                fill_color="#111722", fill_opacity=1).move_to([cx, -1.4, 0])
        names = VGroup(label(r"the axon's ending", font_size=24, color=GREY_A).next_to(axon, RIGHT, buff=0.2).shift(
            UP * 0.2), label(r"the next cell", font_size=24, color=GREY_A).move_to(post).shift(DOWN * 0.5 + LEFT * 1.3))
        cleft = label(r"cleft", font_size=20, color=GREY_B).move_to([cx + 2.6, -0.26, 0])
        spots = [(-1.25, 1.25), (-0.45, 1.35), (0.4, 1.3), (1.2, 1.25), (-0.7, 0.5), (0.7, 0.5)]
        ves = VGroup()
        for dx, y in spots:
            c = Circle(radius=0.24, color=EXC, stroke_width=3).move_to([cx + dx, y, 0])
            dots = VGroup(*[Dot(c.get_center() + 0.1 * np.array([np.cos(a), np.sin(a), 0]), radius=0.045, color=EXC)
                            for a in (0.5, 2.6, 4.7)])
            ves.add(VGroup(c, dots))
        chans = VGroup(*[Rectangle(width=0.16, height=0.42, stroke_width=0, fill_color=DATA, fill_opacity=1).move_to(
            [cx + s * 1.95, 0.55, 0]) for s in (-1, 1)])
        ca = VGroup(*[Dot([cx + s * (2.9 + 0.25 * k), 0.55 + 0.18 * (k - 1), 0], radius=0.06, color=DATA)
                      for s in (-1, 1) for k in range(3)])
        ca_l = label(r"Ca$^{2+}$", font_size=22, color=DATA).move_to([cx - 2.75, 0.05, 0])
        rx = [-1.5, -0.75, 0.0, 0.75, 1.5]
        recs = VGroup(*[Rectangle(width=0.3, height=0.34, color=GREY_B, stroke_width=3, fill_color="#111722",
                                  fill_opacity=1).move_to([cx + x, -0.55, 0]) for x in rx])
        pulse = Dot([cx, 3.0, 0], radius=0.14, color=THRESH)
        tm = VGroup(*[Dot([cx + sx * 0.7 + 0.12 * (k - 1.5), 0.02, 0], radius=0.055, color=EXC)
                      for sx in (-1, 1) for k in range(4)])
        targets = [np.array([cx + rx[i], -0.42, 0]) + np.array([0.07 * (j - 0.5), 0, 0])
                   for i, j in ((0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0))]
        cur = VGroup(*[Arrow([cx + x, -0.8, 0], [cx + x, -1.4, 0], color=EXC, stroke_width=3, buff=0,
                             max_tip_length_to_length_ratio=0.3) for x in rx[1:4]])
        d = load("integration")
        keep = d["t"] <= 40
        tt, vv = d["t"][keep], d["one"][keep] - d["e_l"]
        epsp = VMobject(color=EXC, stroke_width=3).set_points_as_corners(
            [np.array([cx + 0.2 + 1.9 * t / 40, -1.95 + 0.22 * v, 0]) for t, v in zip(tt[::10], vv[::10])])
        steps = [r"a spike arrives", r"calcium channels open, \ and calcium enters",
                 r"vesicles fuse with the membrane and empty into the cleft",
                 r"the transmitter crosses: \ about 20 nm", r"receptors bind it and open; \ current flows in the "
                 r"next cell", r"the transmitter is pumped back or broken up"]
        rows = VGroup()
        for i, s in enumerate(steps, 1):
            n = label(rf"{i}", font_size=28, color=P.ACCENT)
            t = wrapped_label(s, 5.8, 29, WHITE)
            rows.add(VGroup(n, t).arrange(RIGHT, buff=0.3, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([3.5, 0.35, 0])
        end = label(r"start to finish: \ about half a millisecond", font_size=32, color=P.ACCENT)
        end.to_edge(DOWN, buff=0.6)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here's a chemical synapse, drawn large. Above, the ending of an axon. Below, the membrane of the "
            "next cell. Between them a cleft, about twenty millionths of a millimetre wide. "
            "<bookmark mark='a'/> Inside the ending are vesicles: small bags, each packed with thousands of "
            "molecules of transmitter. <bookmark mark='b'/> One. A spike arrives. <bookmark mark='c'/> Two. "
            "The change of voltage opens channels that let calcium in. <bookmark mark='d'/> Three. The "
            "calcium makes vesicles fuse with the membrane and spill their contents into the cleft. "
            "<bookmark mark='e'/> Four. The transmitter drifts across. The gap is so narrow that this takes "
            "far less than a millisecond. <bookmark mark='f'/> Five. On the far side, receptor molecules bind "
            "it, and open. Ions flow, and the voltage of the next cell moves a little. <bookmark mark='g'/> "
            "Six. The transmitter is cleared away: pumped back into the ending, or broken up by an enzyme. "
            "That ends the message. <bookmark mark='h'/> Start to finish, about half a millisecond. That "
            "delay was one of the things that finally sank the sparks. A current jumping a gap wouldn't need "
            "it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(VGroup(axon, bulb, post, names, cleft, chans, recs)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(v, scale=0.6) for v in ves], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(pulse))
            self.play(pulse.animate.move_to([cx, 1.9, 0]), run_time=0.8, rate_func=linear)
            self.play(FadeOut(pulse, scale=2.5), bulb.animate.set_stroke(THRESH), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(ca), FadeIn(ca_l))
            self.play(*[c.animate.move_to([cx + np.sign(c.get_x() - cx) * (1.2 + 0.2 * (i % 3)), 0.5, 0])
                        for i, c in enumerate(ca)], run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), ves[4].animate.shift(DOWN * 0.3), ves[5].animate.shift(DOWN * 0.3))
            self.play(FadeOut(ves[4]), FadeOut(ves[5]), FadeIn(tm), bulb.animate.set_stroke(VOLT), run_time=0.7)
            vo.wait_until("e")
            self.play(FadeIn(rows[3]), *[m.animate.move_to(p) for m, p in zip(tm, targets)], run_time=1.4)
            vo.wait_until("f")
            self.play(FadeIn(rows[4]), recs.animate.set_stroke(EXC), LaggedStart(*[GrowArrow(a) for a in cur],
                                                                                  lag_ratio=0.2))
            self.play(Create(epsp), run_time=1.5)
            vo.wait_until("g")
            self.play(FadeIn(rows[5]), *[m.animate.move_to([cx + 0.25 * (i - 3.5), 0.45, 0]).set_opacity(0.5)
                                         for i, m in enumerate(tm)], recs.animate.set_stroke(GREY_B), FadeOut(cur),
                      run_time=1.5)
            vo.wait_until("h")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def quanta(self):
        q = load("quanta")
        head = heading(r"How much is released? \ It comes in packets")
        ymax = float(q["hist"].max()) * 1.2
        A = axes([-0.3, 2.3], [0, ymax], x_length=7.2, y_length=4.0, xticks=[0, 0.4, 0.8, 1.2, 1.6, 2.0],
                 yticks=[], xfmt=lambda v: f"{v:.1f}", xlabel=r"response to one impulse (mV)",
                 ylabel=r"how often", center=[-3.0, -0.5, 0])
        ax = A.ax
        bars = hist(ax, q["edges"], q["hist"], EXC, opacity=0.7)
        marks = VGroup()
        for k in range(5):
            top = ax.c2p(k * q["q"], ymax * 0.86)
            marks.add(VGroup(DashedLine(ax.c2p(k * q["q"], 0), top, color=GREY_C, stroke_width=1.5),
                             label(rf"{k}", font_size=26, color=THRESH).next_to(top, UP, buff=0.06)))
        packets = label(r"packets", font_size=24, color=THRESH).next_to(marks[-1][1], RIGHT, buff=0.2)
        # the story first: spontaneous blips, then responses to successive impulses
        def bump(x0, base, h, w=0.26):
            u = np.linspace(0, 1, 14)
            return [np.array([x0 + w * a, base + h * (6 * a) * np.exp(1 - 6 * a), 0]) for a in u]

        g = np.random.default_rng(66)
        xl, xr, unit_h = -6.4, 0.6, 1.5 * q["q"]
        at = np.sort(g.uniform(xl + 0.3, xr - 0.5, 6))
        pts = [np.array([xl, 1.9, 0])]
        for x0 in at:
            pts += [np.array([x0, 1.9, 0])] + bump(x0, 1.9, unit_h) + [np.array([x0 + 0.27, 1.9, 0])]
        pts.append(np.array([xr, 1.9, 0]))
        minis = VMobject(color=VOLT, stroke_width=3).set_points_as_corners(pts)
        minis_l = wrapped_label(r"the nerve silent: \ small blips, \ all one size", 5.0, 28, WHITE).move_to(
            [4.0, 2.1, 0])
        base = -1.9
        ex = q["example"][:16]
        guides = VGroup(*[VGroup(DashedLine([xl, base + k * unit_h, 0], [xr, base + k * unit_h, 0], color=GREY_D,
                                            stroke_width=1.5),
                                 label(rf"{k}", font_size=24, color=THRESH).next_to([xr, base + k * unit_h, 0], RIGHT,
                                                                                    buff=0.12)) for k in range(4)])
        evoked = VGroup(*[VMobject(color=EXC, stroke_width=3).set_points_as_corners(
            [np.array([xl + 0.1 + i * (xr - xl - 0.3) / len(ex) - 0.06, base, 0])]
            + bump(xl + 0.1 + i * (xr - xl - 0.3) / len(ex), base, 1.5 * max(float(v), 0.0))
            + [np.array([xl + 0.1 + i * (xr - xl - 0.3) / len(ex) + 0.36, base, 0])]) for i, v in enumerate(ex)])
        evoked_l = wrapped_label(r"calcium lowered, \ one impulse after another: \ nothing, or one blip's worth, "
                                 r"or two, or three", 5.0, 28, WHITE).move_to([4.0, -0.9, 0])
        story = VGroup(minis, minis_l, guides, evoked, evoked_l)
        muscle = RoundedRectangle(width=5.0, height=1.0, corner_radius=0.3, color=DATA, stroke_width=3,
                                  fill_color=DATA, fill_opacity=0.25).move_to([-3.2, -0.9, 0])
        nerve = Line([-6.2, 1.7, 0], [-3.6, -0.3, 0], color=THRESH, stroke_width=6)
        knob = Dot(nerve.get_end(), radius=0.13, color=THRESH)
        probe = Line([-0.9, 1.7, 0], [-2.6, -0.45, 0], color=GREY_A, stroke_width=3)
        sketch = VGroup(muscle, nerve, knob, probe,
                        label(r"nerve", font_size=26, color=THRESH).next_to(nerve.get_start(), RIGHT, buff=0.2),
                        label(r"muscle fibre", font_size=26, color=DATA).next_to(muscle, DOWN, buff=0.15),
                        label(r"recording electrode", font_size=24, color=GREY_A).next_to(probe.get_start(), UP,
                                                                                          buff=0.1),
                        wrapped_label(r"London, the early 1950s: \ Katz and his colleagues record where a frog's "
                                      r"nerve meets its muscle", 4.8, 28, WHITE).move_to([4.0, 0.2, 0]))
        side = VGroup(
            wrapped_label(rf"a model synapse: \ {q['sites']} release sites, each letting go of one packet with "
                          rf"probability {q['p']:.1f}", 5.0, 26, GREY_A),
            label(rf"no packet at all: \ {pct(q['failures'])} of impulses", font_size=27, color=THRESH),
            label(r"mean response $= n\,p\,q$", font_size=34, color=RULE),
            VGroup(label(r"$n$ \ release sites", font_size=27, color=WHITE),
                   label(r"$p$ \ chance that a site releases", font_size=27, color=WHITE),
                   label(r"$q$ \ response to one packet", font_size=27, color=WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12),
            wrapped_label(r"Three numbers: \ three ways to make a synapse stronger.", 5.0, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, -0.3, 0])
        src = historical_tag(archive.DEL_CASTILLO_KATZ_1954.cite)
        tag = psyche_tag(r"computed: a model synapse")
        with self.voiceover(
            "How much transmitter is released? In the early nineteen-fifties Bernard Katz and his colleagues, "
            "in London, were recording from the place where a frog's nerve meets its muscle, and they noticed "
            "something odd. <bookmark mark='m'/> Even with the nerve silent, there were tiny blips of voltage, "
            "all about the same size. <bookmark mark='n'/> So they lowered the calcium, to make the nerve "
            "release very little, and watched the response to one impulse after another. It didn't shrink "
            "smoothly. It came in steps. Nothing, or one blip's worth, or two, or three. Never one and a "
            "half. <bookmark mark='a'/> This histogram is "
            f"a model synapse behaving that way: {q['sites']} release sites, each letting go of one packet "
            "with a probability of three in ten. <bookmark mark='b'/> The peaks sit at whole numbers of "
            f"packets. And look at the peak on the left. {100 * q['failures']:.0f} percent of impulses "
            "release nothing at all. <bookmark mark='c'/> So transmitter comes in packets, and a packet is "
            "the contents of one vesicle. And a synapse is a gamble. Its average effect is a product of "
            "three numbers: how many sites it has, how likely each one is to release, and how big a response "
            "one packet makes. <bookmark mark='d'/> Three numbers, so three ways to make a synapse stronger. "
            "Keep that in mind when we come to learning."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(sketch))
            vo.wait_until("m")
            self.play(FadeOut(sketch), run_time=0.6)
            self.play(Create(minis), FadeIn(minis_l), run_time=3.0, rate_func=linear)
            vo.wait_until("n")
            self.play(FadeIn(guides), FadeIn(evoked_l))
            self.play(LaggedStart(*[Create(b) for b in evoked], lag_ratio=0.5), run_time=9.0)
            vo.wait_until("a")
            self.play(FadeOut(story), FadeIn(A))
            self.play(FadeIn(bars, lag_ratio=0.02), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.3), FadeIn(packets), run_time=2.0)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4], shift=UP * 0.1))
        self.clear_scene()

    def kinds(self):
        head = heading(r"Two kinds of receptor, \ and two directions")
        def sketch(col, channel):
            mem = VGroup(Line([-0.85, 0, 0], [-0.3 if channel else 0.85, 0, 0], color=GREY_C, stroke_width=6))
            if channel:
                mem.add(Line([0.3, 0, 0], [0.85, 0, 0], color=GREY_C, stroke_width=6))
                body = VGroup(*[Rectangle(width=0.22, height=0.7, color=col, stroke_width=3, fill_color="#1A2130",
                                          fill_opacity=1).move_to([sx * 0.2, 0, 0]) for sx in (-1, 1)])
                out = VGroup(Arrow([0, 0.3, 0], [0, -0.75, 0], color=col, stroke_width=4, buff=0,
                                   max_tip_length_to_length_ratio=0.2))
            else:
                body = VGroup(Rectangle(width=0.4, height=0.7, color=col, stroke_width=3, fill_color="#1A2130",
                                        fill_opacity=1))
                out = VGroup(*[Arrow([0, -0.38, 0], [dx, -0.85, 0], color=col, stroke_width=3, buff=0.02,
                                     max_tip_length_to_length_ratio=0.25) for dx in (-0.5, 0.0, 0.5)])
            lig = Dot([0, 0.5, 0], radius=0.11, color=WHITE)
            return VGroup(mem, body, out, lig)

        fast_t = VGroup(label(r"the receptor is a channel", font_size=31, color=EXC),
                        wrapped_label(r"opens within a millisecond, \ closes a few milliseconds later", 4.4, 27,
                                      WHITE),
                        label(r"for carrying signals", font_size=27, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        slow_t = VGroup(label(r"the receptor starts a reaction inside", font_size=31, color=RULE),
                        wrapped_label(r"slower to begin, \ lasts seconds or minutes, \ changes how the cell "
                                      r"behaves", 4.4, 27, WHITE),
                        label(r"for adjusting", font_size=27, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fast = VGroup(sketch(EXC, True).scale(1.5), fast_t).arrange(RIGHT, buff=0.45)
        slow = VGroup(sketch(RULE, False).scale(1.5), slow_t).arrange(RIGHT, buff=0.45)
        left = VGroup(fast, slow).arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to([-3.4, -0.1, 0])
        keep_in_frame(left)
        x0 = 3.0

        def Y(v):
            return -2.4 + (v + 90) * 0.052

        rail = Line([x0, Y(-90), 0], [x0, Y(8), 0], color=GREY_C, stroke_width=3)
        levels = [(0, r"$0$ mV: \ sodium with potassium", EXC), (-50, r"$-50$: \ threshold", THRESH),
                  (-65, r"$-65$: \ rest", VOLT), (-80, r"$-80$: \ chloride, or potassium", INH)]
        ticks = VGroup()
        for v, txt, col in levels:
            ticks.add(VGroup(Line([x0 - 0.15, Y(v), 0], [x0 + 0.15, Y(v), 0], color=col, stroke_width=4),
                             label(txt, font_size=25, color=col).next_to([x0 + 0.2, Y(v), 0], RIGHT, buff=0.1)))
        up = Arrow([x0 - 0.5, Y(-65), 0], [x0 - 0.5, Y(-10), 0], color=EXC, stroke_width=5, buff=0,
                   max_tip_length_to_length_ratio=0.1)
        dn = Arrow([x0 - 0.5, Y(-65), 0], [x0 - 0.5, Y(-80), 0], color=INH, stroke_width=5, buff=0,
                   max_tip_length_to_length_ratio=0.35)
        up_l = label(r"excitation", font_size=26, color=EXC).next_to(up, LEFT, buff=0.15)
        dn_l = label(r"inhibition", font_size=26, color=INH).next_to(dn, LEFT, buff=0.15)
        ladder = VGroup(rail, ticks, up, dn, up_l, dn_l)
        keep_in_frame(ladder)
        end = wrapped_label(r"A channel pulls the voltage toward the battery of the ions it passes \ (Part 5).", 12.4,
                            28, P.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Two more facts, and we can start building. First, receptors come in two kinds. "
            "<bookmark mark='a'/> In one, the receptor is itself a channel. Transmitter binds, the channel "
            "opens within a millisecond, and it closes a few milliseconds later. That's the kind that carries "
            "signals. <bookmark mark='b'/> In the other, the receptor isn't a channel at all. It sets off a "
            "chain of chemical reactions inside the cell. That's slower to begin, it can last for seconds or "
            "minutes, and it changes how the cell behaves: how excitable it is, even which proteins it makes. "
            "That's the kind that adjusts. <bookmark mark='c'/> Second. What a fast synapse does to the next "
            "cell depends on which ions its channels let through, and you know how to work that out from "
            "Part 5. A channel pulls the voltage toward the battery of the ions it passes. "
            "<bookmark mark='d'/> A channel that passes sodium and potassium together pulls toward zero "
            "millivolts, which is well above threshold. That's excitation. <bookmark mark='e'/> A channel "
            "that passes chloride, or potassium alone, pulls the voltage toward rest or below it, away from "
            "threshold. That's inhibition. Notice that it's the receptor that decides, not the transmitter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(fast, shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(slow, shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(Create(rail), FadeIn(ticks[2]), FadeIn(ticks[1]), FadeIn(end))
            vo.wait_until("d")
            self.play(FadeIn(ticks[0]), GrowArrow(up), FadeIn(up_l))
            vo.wait_until("e")
            self.play(FadeIn(ticks[3]), GrowArrow(dn), FadeIn(dn_l))
        self.clear_scene()
