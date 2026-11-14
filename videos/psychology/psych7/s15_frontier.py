from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403


def sheet(arr, height, center, tint, hi):
    """One model cortex as an image, in a thin frame."""
    img = picture(arr, height=height, lo=0.0, hi=hi, tint=tint).move_to(center)
    frame = Square(side_length=height, color=GREY_D, stroke_width=2).move_to(center)
    return Group(img, frame)


def on_sheet(frame, x, y, size=40):
    """The scene point of voxel (x, y) on a sheet drawn in ``frame``."""
    h = frame.height
    return frame.get_corner(DL) + np.array([(x + 0.5) / size * h, (y + 0.5) / size * h, 0.0])


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.method()
        self.bias()
        self.open()

    def card(self):
        card = chapter_card(14, r"Frontier: mapping damage in thousands",
                            r"Can a statistical map of lesions be trusted?", lit=(), part=PART, scale=("brain",),
                            marr=("tissue",))
        with self.voiceover(
            "Chapter fourteen. Frontier: mapping damage in thousands."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def method(self):
        d = load("lesionmap")
        head = heading(r"From one famous patient to hundreds of scans")
        ex = d["artery_example"]
        small = Group(*[sheet(ex[k].astype(float), 1.45, ORIGIN, LESION, 1.0) for k in range(6)])
        small.arrange_in_grid(2, 3, buff=0.18).move_to([-4.0, 0.55, 0])
        small_l = label(r"six of 400 simulated patients: \ what each stroke destroyed", font_size=22, color=GREY_A)
        small_l.next_to(small, DOWN, buff=0.15)
        over = sheet(d["artery_overlap"], 3.3, [3.9, 0.55, 0], DATA, float(d["artery_overlap"].max()))
        over_l = label(r"overlap: \ how many patients are damaged at each point", font_size=22, color=DATA)
        over_l.next_to(over, DOWN, buff=0.15)
        arrow = Arrow([-1.3, 0.55, 0], [1.9, 0.55, 0], color=GREY_B, stroke_width=4, buff=0.1)
        steps = VGroup(
            wrapped_label(r"at each point: \ split the patients into damaged there and spared there, \ and "
                          r"compare the two groups' scores", 12.6, 28, WHITE),
            wrapped_label(r"the map of that statistic says where damage goes with the deficit", 12.6, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.45)
        tag = psyche_tag(r"simulated patients: Psyche")
        # then and now
        one = brain_side(2.6, fill=0.3).move_to([-4.2, 0.3, 0])
        one_l = label(r"1861: \ one brain, after death", font_size=28, color=GREY_A).next_to(one, DOWN, buff=0.3)
        many = VGroup(*[RoundedRectangle(width=0.42, height=0.42, corner_radius=0.06, color=GREY_B, stroke_width=1.5,
                                         fill_color=DATA, fill_opacity=0.12 + 0.5 * ((7 * k) % 10) / 10)
                        for k in range(96)]).arrange_in_grid(rows=8, buff=0.1).move_to([3.3, 0.3, 0])
        many_l = label(r"today: \ a scan and a score for every patient", font_size=28, color=DATA).next_to(
            many, DOWN, buff=0.3)
        then_now = VGroup(one, one_l, many, many_l)
        with self.voiceover(
            "Broca had one brain on a table. Today a stroke unit has a scan of every patient and a score "
            "on every test, for hundreds or thousands of people, and that has changed the method. "
            "<bookmark mark='a'/> Each patient is a picture of what was destroyed. Here are six, from a "
            "simulation we'll come back to. <bookmark mark='b'/> Lay them on top of one another and you "
            "have a map of where damage tends to fall. <bookmark mark='c'/> Then, at each point of the "
            "brain, split the patients in two: those damaged there, and those spared there. Compare the "
            "two groups' scores on, say, a speech test. <bookmark mark='d'/> Do that at every point and "
            "you have a map of where damage goes with the deficit. No famous patient is needed, and nobody "
            "decides in advance where to look. It's called lesion-symptom mapping, and since the early "
            "two-thousands it's been the standard way to do what Broca did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(FadeIn(one), FadeIn(one_l))
            self.play(FadeIn(many, lag_ratio=0.02), FadeIn(many_l), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeOut(then_now), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(s) for s in small], lag_ratio=0.3), FadeIn(small_l), run_time=3.0)
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(over), FadeIn(over_l))
            vo.wait_until("c")
            self.play(FadeIn(steps[0], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(steps[1], shift=UP * 0.1))
        self.clear_scene()

    def bias(self):
        d = load("lesionmap")
        m = archive.MAH_2014.data
        head = heading(r"The map is pulled toward the artery")
        cx, cy = d["critical_centre"]
        groups = []
        for name, x0, title in (("artery", -4.65, r"strokes follow one artery"),
                                ("anywhere", 0.05, r"lesions fall anywhere")):
            t = np.clip(d[f"{name}_tmap"], 0, None)
            s = sheet(t, 4.3, [x0, -0.1, 0], THRESH, float(t.max()))
            fr = s[1]
            unit = fr.height / 40
            ring = Circle(radius=3.0 * unit, color=WHITE, stroke_width=3).move_to(on_sheet(fr, cx, cy))
            c = d[f"{name}_centre"]
            cross = VGroup(Line(LEFT * 0.12, RIGHT * 0.12, color=LESION, stroke_width=5),
                           Line(DOWN * 0.12, UP * 0.12, color=LESION, stroke_width=5)).move_to(
                on_sheet(fr, c[0], c[1]))
            ttl = label(title, font_size=28, color=WHITE).next_to(s, UP, buff=0.12)
            res = label(rf"off by {d[f'{name}_mean_displacement']:.1f} voxels, \ over 30 studies", font_size=27,
                        color=LESION if name == "artery" else GREY_A).next_to(s, DOWN, buff=0.12)
            extra = VGroup()
            if name == "artery":
                y = on_sheet(fr, 0, d["trunk_row"])[1]
                extra.add(DashedLine([fr.get_left()[0], y, 0], [fr.get_right()[0], y, 0], color=GREY_A,
                                     stroke_width=2),
                          label(r"the trunk", font_size=22, color=WHITE).next_to([fr.get_left()[0], y, 0], UR,
                                                                                 buff=0.04))
            groups.append((s, ring, cross, ttl, res, extra))
        key = VGroup(
            VGroup(Circle(radius=0.13, color=WHITE, stroke_width=3), label(r"the region that matters", font_size=26)
                   ).arrange(RIGHT, buff=0.15),
            VGroup(label(r"$+$", font_size=32, color=LESION), label(r"where the map points", font_size=26,
                                                                   color=LESION)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rows = VGroup(
            key,
            wrapped_label(r"damage near the trunk always takes the region beyond it, \ so the trunk looks like "
                          r"the best predictor", 4.1, 27, WHITE),
            wrapped_label(rf"{fmt_int(m['patients'])} real strokes: \ the same error, \ along the arteries' "
                          r"territories", 4.1, 27, DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.85, -0.1, 0])
        keep_in_frame(rows)
        src = published_tag(archive.MAH_2014.cite)
        tag = psyche_tag(r"maps: simulated patients (Psyche)")
        toward = int((d["artery_shift"][:, 1] < 0).sum())  # studies whose map moved toward the trunk
        with self.voiceover(
            "Can the map be trusted? We can ask, because in a simulation we know the answer. "
            "<bookmark mark='a'/> Here's a sheet of model cortex, and four hundred simulated patients. The "
            "deficit depends on one small region, the white ring. Nothing else matters. And the strokes "
            "aren't scattered at random. They follow an artery: a trunk along the middle, with branches "
            "leaving it. Block the artery anywhere, and everything fed from beyond that point is lost. "
            "<bookmark mark='b'/> The map lights up, and its centre, the red cross, isn't on the ring. "
            f"It's pulled toward the trunk. Over thirty repeats of the study the error averages "
            f"{d['artery_mean_displacement']:.1f} voxels, and in {toward} of the thirty it's in that direction. "
            "<bookmark mark='c'/> The reason is simple. A blockage near the trunk always takes the critical "
            "region with it. So damage near the trunk predicts the deficit better than partial damage to the "
            "region itself. <bookmark mark='d'/> Run the same study with lesions that can fall anywhere, and "
            f"the error drops to {d['anywhere_mean_displacement']:.1f} voxels, with no preferred direction. "
            f"<bookmark mark='e'/> This isn't only a toy. In 2014 a London group took the scans of "
            f"{fmt_int(m['patients'])} stroke patients and showed that the standard method mislocalizes in "
            "just this way, along the territories of the brain's arteries. Chapter four said one damaged "
            "system can fake two. This is the same lesson at scale: damage isn't assigned at random, so a "
            "lesion study is an observational study, with Part 2's problems."
        ) as vo:
            s, ring, cross, ttl, res, extra = groups[0]
            self.play(FadeIn(head), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(s[1]), FadeIn(ttl), FadeIn(ring), FadeIn(extra), FadeIn(rows[0][0]))
            vo.wait_until("b")
            self.play(FadeIn(s[0]), FadeIn(cross, scale=2.0), FadeIn(res), FadeIn(rows[0][1]))
            self.bring_to_front(ring, cross, extra)
            vo.wait_until("c")
            self.play(FadeIn(rows[1], shift=UP * 0.1))
            vo.wait_until("d")
            s2, ring2, cross2, ttl2, res2, _ = groups[1]
            self.play(FadeIn(s2), FadeIn(ttl2), FadeIn(ring2), FadeIn(cross2), FadeIn(res2))
            vo.wait_until("e")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def open(self):
        head = heading(r"What is not settled")
        items = [
            (r"Can a map be corrected for where strokes fall?",
             r"Methods that weigh all points together help. \ None removes the problem.", THRESH),
            (r"Is the damage the lesion, \ or what the lesion disconnects?",
             r"A small hole in a cable can silence regions far away that look intact on the scan.", PARIETAL),
            (r"What does the cerebellum do for thought?",
             r"Most of the brain's neurons are there, \ and this part gave it one line.", CEREBELLUM),
            (r"Are ``areas'' the right unit at all?",
             r"Or are they our drawing of something that is graded, overlapping, and different in each "
             r"person?", TEMPORAL),
        ]
        rows = VGroup()
        for q, a, col in items:
            rows.add(VGroup(wrapped_label(q, 12.6, 34, col), wrapped_label(a, 12.6, 29, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([0, 0.0, 0])
        keep_in_frame(rows)
        star = wrapped_label(r"$\star$ \ Problem 7: \ design the lesion study that tells a damaged region from a "
                             r"damaged connection.", 12.6, 29, P.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So here's what isn't settled. <bookmark mark='a'/> Can a map be corrected for where strokes "
            "tend to fall? Methods that weigh all the points together, instead of one at a time, do better. "
            "None of them makes the problem go away, because the patients who'd separate two neighbouring "
            "regions mostly don't exist. <bookmark mark='b'/> Is the damage the lesion, or what the lesion "
            "disconnects? Wernicke's third aphasia was a cut cable. A small hole in the white matter can "
            "silence regions far away that look intact on the scan. <bookmark mark='c'/> What does the "
            "cerebellum do for thought? Most of the brain's neurons are in it, and this part gave it one "
            "line, about movement. People with damage there have problems that aren't about movement, and "
            "nobody has a settled account of why. <bookmark mark='d'/> And are areas the right unit at "
            "all? Or are they our drawing of something graded, overlapping, and a little different in each "
            "person? <bookmark mark='e'/> The starred problem asks you to design the study that would "
            "tell a damaged region from a damaged connection."
        ) as vo:
            self.play(FadeIn(head))
            for k, mark_ in enumerate("abcd"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(star, shift=UP * 0.1))
        self.clear_scene()
