from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403


class Tour(VoiceoverScene):
    def construct(self):
        self.card()
        self.numbers()
        self.outside()
        self.inside()

    def card(self):
        card = chapter_card(1, r"A tour of the parts", r"What is in there, and what is each part for?", lit=(),
                            part=PART, scale=("brain",), marr=("tissue",))
        with self.voiceover(
            "Chapter one. A tour of the parts."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def numbers(self):
        t = load("tour")
        head = heading(r"A brain, in four numbers")
        cells = VGroup(
            big_number(rf"{t['neurons'] / 1e9:.0f} billion", r"neurons", THRESH, 60),
            big_number(pct(t["cortex_share"]), r"of them in the cerebral cortex", PARIETAL, 60),
            big_number(pct(t["mass_share"]), r"of the body's weight", VOLT, 60),
            big_number(pct(t["energy_share"]), r"of the body's energy at rest", LESION, 60),
        ).arrange_in_grid(2, 2, buff=(1.6, 0.8)).move_to([0, 0.1, 0])
        end = wrapped_label(rf"About {t['brain_watts']:.0f} watts, \ day and night: \ "
                            rf"{t['times_fair_share']:.0f} times its share by weight.", 12.6, 30, P.ACCENT)
        end.to_edge(DOWN, buff=0.75)
        src = published_tag(archive.AZEVEDO_2009.cite + r"; " + archive.RAICHLE_2002.cite)
        with self.voiceover(
            "Before the tour, four numbers. <bookmark mark='a'/> A human brain has about "
            f"{t['neurons'] / 1e9:.0f} billion neurons. That's a count, made by dissolving brains and "
            "counting the cell nuclei. <bookmark mark='b'/> Fewer than a fifth of those neurons are in the "
            "cerebral cortex, the folded sheet you picture when someone says brain. Most of the rest are "
            "packed into the cerebellum, at the back. <bookmark mark='c'/> The brain is about two percent "
            "of your body's weight. <bookmark mark='d'/> And it uses about twenty percent of your energy at "
            f"rest. Roughly {t['brain_watts']:.0f} watts, day and night, asleep or awake. That's "
            f"{t['times_fair_share']:.0f} times its share by weight. Keep that number. At the end of this "
            "part it disposes of a famous myth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, mark_ in enumerate("abcd"):
                vo.wait_until(mark_)
                self.play(FadeIn(cells[k], shift=UP * 0.1))
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def outside(self):
        head = heading(r"From the side: \ four lobes, and two things underneath")
        brain = brain_side(6.2, fill=0.18).move_to([-3.5, 0.0, 0])
        front = label(r"front", font_size=22, color=GREY_B).next_to(brain, LEFT, buff=0.1).shift(UP * 0.3)
        keep_in_frame(front)
        entries = [
            ("occipital", r"occipital lobe", OCCIPITAL, r"seeing"),
            ("temporal", r"temporal lobe", TEMPORAL, r"hearing, recognizing, and, on its inner side, memory"),
            ("parietal", r"parietal lobe", PARIETAL, r"touch, space, and where to attend"),
            ("frontal", r"frontal lobe", FRONTAL, r"movement, speech, planning, holding back"),
            ("cerebellum", r"cerebellum", CEREBELLUM, r"the timing and smoothness of movement"),
            ("brainstem", r"brainstem", STEM, r"breathing, heartbeat, sleep and waking"),
        ]
        rows = VGroup()
        for _, name, col, what in entries:
            rows.add(VGroup(label(name, font_size=31, color=col), wrapped_label(what, 5.6, 27, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([3.7, -0.1, 0])
        keep_in_frame(rows)
        end = label(r"every line here is too simple", font_size=26, color=P.ACCENT).to_edge(DOWN, buff=0.3)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here's the left half of a brain, seen from the side, with the front to the left. The cortex is "
            "divided, by convention and by a few deep folds, into four lobes. One line on each. "
            "<bookmark mark='a'/> At the back, the occipital lobe: seeing. <bookmark mark='b'/> Along the "
            "side, the temporal lobe: hearing, recognizing what things are, and, tucked into its inner "
            "surface, the machinery for making memories. <bookmark mark='c'/> On top toward the back, the "
            "parietal lobe: touch, the layout of space, and where to attend. <bookmark mark='d'/> And the "
            "frontal lobe, the largest: movement, speech, planning, and holding yourself back. "
            "<bookmark mark='e'/> Under the back sits the cerebellum, which keeps movement smooth and well "
            "timed. <bookmark mark='f'/> And the brainstem, joining it all to the spinal cord: breathing, "
            "heartbeat, sleep and waking. Damage here is the kind that kills. <bookmark mark='g'/> Every "
            "one of those lines is too simple, like the lines on the transmitters in Part 6. They're a map "
            "for the rest of this part, which is about how anyone came to write them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(brain), FadeIn(front))
            for k, mark_ in enumerate("abcdef"):
                vo.wait_until(mark_)
                piece = brain.lobe[entries[k][0]]
                target = piece[0] if isinstance(piece, VGroup) else piece
                self.play(target.animate.set_fill(opacity=0.8), FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("g")
            self.play(FadeIn(end))
        self.clear_scene()

    def inside(self):
        head = heading(r"Cut down the middle: \ what the cortex wraps around")
        k = 3.1
        c0 = np.array([-3.6, 0.1, 0])

        def P_(x, y):
            return c0 + np.array([x * k, y * k, 0])

        outline = [(-1.0, -0.05), (-0.95, 0.25), (-0.75, 0.5), (-0.45, 0.66), (-0.12, 0.72), (0.2, 0.72), (0.5, 0.62),
                   (0.68, 0.45), (0.85, 0.25), (0.92, 0.0), (0.85, -0.2), (0.68, -0.3), (0.45, -0.33), (0.2, -0.42),
                   (-0.1, -0.45), (-0.4, -0.4), (-0.58, -0.28), (-0.8, -0.18)]
        hemi = Polygon(*[P_(x, y) for x, y in outline], color=GREY_B, stroke_width=3, fill_color="#1A2130",
                       fill_opacity=1).round_corners(0.12)
        stem = Polygon(P_(0.1, -0.2), P_(0.2, -0.86), P_(0.36, -0.86), P_(0.3, -0.2), color=STEM, stroke_width=3,
                       fill_color=STEM, fill_opacity=0.45).round_corners(0.08)
        cb = Ellipse(width=0.62 * k, height=0.36 * k, color=CEREBELLUM, stroke_width=3, fill_color=CEREBELLUM,
                     fill_opacity=0.35).move_to(P_(0.6, -0.5))
        callosum = ArcBetweenPoints(P_(-0.45, 0.2), P_(0.4, 0.2), angle=-PI * 0.55, color=VOLT, stroke_width=12)
        thalamus = Ellipse(width=0.34 * k, height=0.2 * k, color=DEEP, stroke_width=3, fill_color=DEEP,
                           fill_opacity=0.6).move_to(P_(0.05, 0.08))
        hypo = Dot(P_(-0.14, -0.06), radius=0.12, color=LESION)
        basal = Ellipse(width=0.42 * k, height=0.26 * k, color=FRONTAL, stroke_width=3).move_to(P_(-0.25, 0.14))
        basal = DashedVMobject(basal, num_dashes=28)
        hippo = ArcBetweenPoints(P_(-0.12, -0.24), P_(0.34, -0.16), angle=PI * 0.35, color=TEMPORAL, stroke_width=11)
        amyg = Dot(P_(-0.22, -0.24), radius=0.13, color=DATA)
        drawing = VGroup(stem, cb, hemi)
        parts = [
            (callosum, r"corpus callosum", VOLT, r"the cable between the two halves"),
            (thalamus, r"thalamus", DEEP, r"the relay: \ nearly every sense passes through it to the cortex"),
            (basal, r"basal ganglia", FRONTAL, r"choosing and starting actions; \ habits"),
            (hippo, r"hippocampus", TEMPORAL, r"laying down new memories"),
            (amyg, r"amygdala", DATA, r"learning what to fear"),
            (hypo, r"hypothalamus", LESION, r"hunger, thirst, temperature, hormones"),
        ]
        rows = VGroup()
        for _, name, col, what in parts:
            rows.add(VGroup(label(name, font_size=30, color=col), wrapped_label(what, 5.4, 26, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([3.8, 0.0, 0])
        keep_in_frame(rows)
        end = wrapped_label(r"Each half of the brain mostly deals with the opposite side of the body and of the "
                            r"world.", 12.6, 28, P.ACCENT).to_edge(DOWN, buff=0.4)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Now cut the brain down the middle, between its two halves, and look at the inner face of one. "
            "<bookmark mark='a'/> The white band is the corpus callosum, a cable of some two hundred million "
            "fibres that joins the two hemispheres. Remember it. Chapter eight is about what happens when "
            "it's cut. <bookmark mark='b'/> Under it, the thalamus, a relay. Nearly every sense passes "
            "through it on the way to the cortex. <bookmark mark='c'/> Beside it, deeper than this slice, "
            "the basal ganglia, which help choose and start actions and run habits. This is where most of "
            "Part 6's dopamine is delivered. <bookmark mark='d'/> Curled inside the temporal lobe, the "
            "hippocampus. Without it, as we'll see, no new memories of events are laid down. "
            "<bookmark mark='e'/> At its tip, the amygdala, which learns what to fear. <bookmark mark='f'/> "
            "And at the base, the hypothalamus, a few grams of tissue that keeps you fed, watered, warm, and "
            "supplied with hormones. <bookmark mark='g'/> One more fact for the map. Each half of the brain "
            "deals mostly with the opposite side of the body, and the opposite side of the world. The left "
            "hemisphere moves your right hand and sees what's to your right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(drawing))
            for i, mark_ in enumerate("abcdef"):
                vo.wait_until(mark_)
                self.play(FadeIn(parts[i][0], scale=1.15), FadeIn(rows[i], shift=RIGHT * 0.15))
            vo.wait_until("g")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
