from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403


class Maps(VoiceoverScene):
    def construct(self):
        self.card()
        self.penfield()
        self.retina()
        self.share()

    def card(self):
        card = chapter_card(5, r"Maps", r"How is the world laid out on the cortex?", lit={1937: r"Penfield's map"},
                            part=PART, scale=("brain",), marr=("how", "tissue"))
        with self.voiceover(
            "Chapter five. Maps."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def penfield(self):
        p = archive.PENFIELD_BOLDREY_1937.data
        head = heading(r"Montreal, the 1930s: \ a map drawn on patients who were awake")
        brain = brain_side(3.9, fill=0.22).move_to([-4.7, 1.15, 0])
        strip = Line(at(brain, -0.1, 0.72), at(brain, -0.07, 0.12), color=THRESH, stroke_width=9)
        probe = Line(strip.get_start() + np.array([1.3, 0.0, 0]), at(brain, -0.09, 0.45), color=GREY_A,
                     stroke_width=3)
        probe_l = label(r"a weak current", font_size=22, color=GREY_A).next_to(probe.get_start(), RIGHT, buff=0.08)
        parts = [(r"toes", 0.45), (r"leg", 0.45), (r"trunk", 0.55), (r"arm", 0.5), (r"hand", 0.95), (r"fingers", 1.5),
                 (r"face", 0.85), (r"lips", 1.2), (r"tongue", 0.85)]
        total = sum(w for _, w in parts)
        x0, x1, y = -6.6, 6.6, -1.35
        segs, x = VGroup(), x0
        for i, (name, w) in enumerate(parts):
            wd = (x1 - x0) * w / total
            col = THRESH if name in ("hand", "fingers", "lips") else GREY_B
            r = Rectangle(width=wd, height=0.9, color=BACKGROUND, stroke_width=3, fill_color=col, fill_opacity=0.75)
            r.move_to([x + wd / 2, y, 0])
            segs.add(VGroup(r, label(name, font_size=25, color=BLACK).move_to(r)))
            x += wd
        ends = VGroup(label(r"top of the head", font_size=22, color=GREY_B).next_to(segs[0], UP, buff=0.12).align_to(
            segs, LEFT), label(r"down the side", font_size=22, color=GREY_B).next_to(segs[-1], UP, buff=0.12).align_to(
            segs, RIGHT))
        strip_l = label(r"the strip, unrolled: \ touch", font_size=26, color=THRESH).next_to(segs, UP, buff=0.12)
        rows = VGroup(
            wrapped_label(r"Wilder Penfield operates for epilepsy, \ on patients who are awake", 8.2, 30, WHITE),
            wrapped_label(rf"{p['patients']} patients, {p['years']}: \ the surgeon touches the cortex, \ the "
                          r"patient says what they feel", 8.2, 30, WHITE),
            wrapped_label(r"the body is laid out in order along the strip", 8.2, 30, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.4, 1.3, 0])
        keep_in_frame(rows)
        last = wrapped_label(r"and out of proportion: \ the hands and lips get the most cortex, \ because they "
                             r"have the most to report", 12.8, 30, P.ACCENT).move_to([0, -2.75, 0])
        src = historical_tag(archive.PENFIELD_BOLDREY_1937.cite)
        tag = note(r"schematic: the lengths are not measurements").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Damage is one way to ask what a piece of brain does. There's a second, and it was worked out in "
            "an operating theatre in Montreal. The surgeon Wilder Penfield operated on people with severe "
            "epilepsy, and he kept them awake, under local anaesthetic. The brain itself feels no pain. "
            "<bookmark mark='a'/> Before cutting, he touched the exposed cortex with a weak electric "
            "current, one spot after another, and asked the patient what happened. A tingle in the thumb. A "
            f"twitch of the lip. By 1937 he and Edwin Boldrey had done this in {p['patients']} patients. "
            "<bookmark mark='b'/> Put together, the reports made a map. Along one strip of cortex the body "
            "is laid out in order: toes at the top, then the leg, the trunk, the arm, the hand, the face, "
            "and the tongue at the bottom. <bookmark mark='c'/> And the map is wildly out of proportion. "
            "The fingers and the lips get far more cortex than the whole trunk. The cortex isn't dealing in "
            "skin by the square centimetre. It's allotted by how much each part has to report. Your "
            "fingertip can tell two touches apart at a few millimetres. On your back they have to be "
            "centimetres apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(brain))
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15))
            vo.wait_until("a")
            self.play(Create(strip), Create(probe), FadeIn(probe_l), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.1) for s in segs], lag_ratio=0.25), FadeIn(ends),
                      FadeIn(strip_l), FadeIn(rows[2]), run_time=5.0)
            vo.wait_until("c")
            self.play(*[Indicate(segs[i], color=WHITE, scale_factor=1.06) for i in (4, 5, 7)], FadeIn(last))
        self.clear_scene()

    def retina(self):
        m = load("maps")
        head = heading(r"The same in vision: \ a map of the field of view, stretched at the centre")
        A = axes([0, 40], [0, 25], x_length=6.4, y_length=4.0, xticks=[0, 10, 20, 30, 40], yticks=[0, 10, 20],
                 xlabel=r"distance from the centre of gaze (degrees)", ylabel=r"mm of cortex per degree",
                 center=[-3.6, -0.6, 0])
        ax = A.ax
        c = curve(ax, m["ecc"], m["m"], MODEL, stroke_width=4)
        marks = VGroup()
        for e in (0.0, 10.0, 40.0):
            v = float(17.3 / (e + 0.75))
            marks.add(VGroup(Dot(ax.c2p(e, v), radius=0.08, color=THRESH),
                             label(rf"{v:.1f}" if v < 10 else rf"{v:.0f}", font_size=24, color=THRESH).next_to(
                                 ax.c2p(e, v), UR, buff=0.08)))
        side = VGroup(
            MathTex(r"M(E) \;=\; \frac{17.3}{E + 0.75}", font_size=44, color=MODEL),
            wrapped_label(rf"at the centre of gaze: \ {m['m0']:.0f} mm of cortex for one degree", 5.6, 30, WHITE),
            wrapped_label(rf"ten degrees out: \ {float(17.3 / 10.75):.1f} mm", 5.6, 30, WHITE),
            wrapped_label(r"The retina is the same: \ its receptors are packed tightest at the centre.", 5.6, 30,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.9, -0.3, 0])
        keep_in_frame(side)
        src = published_tag(archive.HORTON_HOYT_1991.cite)
        tag = psyche_tag(r"computed from the published formula")
        with self.voiceover(
            "Vision has a map too. The picture on your retina is laid out, point for point, on the cortex at "
            "the very back of your head. It was first charted from soldiers with small wounds there, who had "
            "small blind patches in their field of view. <bookmark mark='a'/> And like the body's map, it's "
            "stretched. Here's the measured stretch: millimetres of cortex given to one degree of your field "
            "of view, against how far that degree is from where you're looking. <bookmark mark='b'/> At the "
            f"centre of your gaze, one degree gets {m['m0']:.0f} millimetres of cortex. Ten degrees out, it "
            f"gets {float(17.3 / 10.75):.1f}. Forty degrees out, less than half a millimetre. "
            "<bookmark mark='c'/> The formula is about as simple as it could be: a constant, divided by the "
            "distance from the centre plus a little. One degree, for scale, is about the width of your "
            "little fingernail held at arm's length."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(A))
            self.play(Create(c), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(k) for k in marks], lag_ratio=0.6), FadeIn(side[1]), FadeIn(side[2]),
                      run_time=4.0)
            vo.wait_until("c")
            self.play(Write(side[0]), FadeIn(side[3]))
        self.clear_scene()

    def share(self):
        m = load("maps")
        head = heading(r"How much of the map goes to the centre?")
        A = axes([0, 40], [0, 1.0], x_length=5.6, y_length=3.0, xticks=[0, 10, 20, 30, 40], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}", xlabel=r"within this many degrees of the centre",
                 ylabel=r"share of the map (\%)", center=[-3.8, 0.45, 0])
        ax = A.ax
        keep = m["ecc"] > 0.05
        c = curve(ax, m["ecc"][keep], m["share"][keep], MODEL, stroke_width=4)
        i10 = int(np.argmin(np.abs(m["marks"] - 10)))
        i1 = int(np.argmin(np.abs(m["marks"] - 1)))
        pt = VGroup(DashedLine(ax.c2p(10, 0), ax.c2p(10, m["share_at"][i10]), color=THRESH, stroke_width=2),
                    DashedLine(ax.c2p(0, m["share_at"][i10]), ax.c2p(10, m["share_at"][i10]), color=THRESH,
                               stroke_width=2), Dot(ax.c2p(10, m["share_at"][i10]), radius=0.08, color=THRESH))
        facts = VGroup(
            wrapped_label(rf"within 10 degrees of the centre: \ {pct(m['share_at'][i10])} of the map", 5.8, 30,
                          THRESH),
            wrapped_label(rf"within 1 degree, \ a patch your thumb covers at arm's length: \ "
                          rf"{pct(m['share_at'][i1])}", 5.8, 30, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 1.3, 0])
        keep_in_frame(facts)
        # letters that each take the same length of cortex
        y0, unit = -2.6, 0.38
        dot = Dot([-6.3, y0, 0], radius=0.07, color=THRESH)
        letters = VGroup()
        for e, s, ch in zip(m["letter_ecc"], m["letter_size"], "KRNSV"):
            letters.add(label(ch, font_size=int(15 * s) + 9, color=WHITE).move_to([-6.3 + unit * e * 1.9, y0, 0]))
        chart_l = wrapped_label(r"Look at the dot. \ Each letter takes the same length of your cortex.", 5.8, 29,
                                P.ACCENT).move_to([3.6, -0.7, 0])
        keep_in_frame(chart_l)
        tag = psyche_tag(r"computed from the published formula")
        with self.voiceover(
            "Add it up over the whole field. <bookmark mark='a'/> Everything within ten degrees of the "
            f"centre, a patch two fists wide at arm's length, takes {100 * m['share_at'][i10]:.0f} percent of "
            "the whole map. <bookmark mark='b'/> Everything within one degree, a patch your thumb covers, takes "
            f"{100 * m['share_at'][i1]:.0f} percent. So a large part of the visual brain is looking at a "
            "very small part of the world, the part you're pointing your eyes at. <bookmark mark='c'/> "
            "That's why you have to move your eyes to read. Here's a row of letters, each one sized so that "
            "it covers the same length of cortex when you look at the dot. To be equally legible, a letter "
            "sixteen degrees out has to be about ten times the size of one a degree out. You don't see the "
            "world sharply. You see a small sharp patch, and you move it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            self.play(Create(c), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(pt), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(dot), LaggedStart(*[FadeIn(k) for k in letters], lag_ratio=0.3), FadeIn(chart_l),
                      run_time=3.0)
        self.clear_scene()
