from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403


class Plastic(VoiceoverScene):
    def construct(self):
        self.card()
        self.critical()
        self.remap()
        self.taxi()

    def card(self):
        card = chapter_card(10, r"A brain that rewires", r"Are the maps fixed?", lit=(), part=PART,
                            scale=("circuit", "brain"), marr=("how", "tissue"))
        with self.voiceover(
            "Chapter ten. A brain that rewires."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _columns(self, center, share_left, title, col=VOLT):
        """Cells of the visual cortex, each answering to the left eye (pink) or the right (blue)."""
        c = np.asarray(center, float)
        n = 14
        k = int(round(n * share_left))
        cells = VGroup(*[Rectangle(width=0.4, height=0.95, stroke_width=1, stroke_color=BACKGROUND,
                                   fill_color=FRONTAL if (i * 5) % n < k else PARIETAL, fill_opacity=0.85)
                         for i in range(n)]).arrange(RIGHT, buff=0.02).move_to(c)
        return VGroup(cells, label(title, font_size=27, color=col).next_to(cells, UP, buff=0.12))

    def critical(self):
        head = heading(r"The 1960s: \ a window that closes")
        normal = self._columns([-3.7, 1.35, 0], 0.5, r"both eyes open: \ cells shared between the eyes")
        kitten = self._columns([-3.7, -0.5, 0], 0.07, r"one eye closed in a kitten's first months", LESION)
        adult = self._columns([-3.7, -2.35, 0], 0.5, r"the same eye closed in an adult cat", SPARED)
        key = VGroup(VGroup(Square(side_length=0.25, stroke_width=0, fill_color=FRONTAL, fill_opacity=0.85),
                            label(r"answers to the eye that was closed", font_size=25, color=FRONTAL)).arrange(
            RIGHT, buff=0.15),
            VGroup(Square(side_length=0.25, stroke_width=0, fill_color=PARIETAL, fill_opacity=0.85),
                   label(r"answers to the other eye", font_size=25, color=PARIETAL)).arrange(RIGHT, buff=0.15)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, 2.1, 0])
        rows = VGroup(
            wrapped_label(r"the closed eye is healthy; \ it has lost its place in the cortex", 5.8, 31, WHITE),
            wrapped_label(r"closing an adult's eye, even for a year, does not do this", 5.8, 31, SPARED),
            wrapped_label(r"a critical period: \ early on, the wiring is settled by use, \ by Part 6's rule", 5.8,
                          31, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.7, -0.7, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.WIESEL_HUBEL_1963.cite)
        tag = note(r"schematic: not the papers' counts").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Everything so far makes the brain sound like a fixed piece of wiring. It isn't, and the first "
            "proof came from kittens. <bookmark mark='a'/> In a normal cat, the cells of the visual cortex "
            "are shared out between the two eyes. In the nineteen-sixties Torsten Wiesel and David Hubel "
            "closed one eye of newborn kittens for the first months of life, then opened it. "
            "<bookmark mark='b'/> The eye itself was healthy. But almost no cells in the cortex answered to "
            "it any more. They'd been taken over by the other eye. The kitten was blind in a perfectly good "
            "eye. <bookmark mark='c'/> Then they did the same to adult cats, for much longer. Nothing of the "
            "kind happened. <bookmark mark='d'/> So there's a window early in life, a critical period, when "
            "the wiring is settled by use. Inputs that are active together keep their connections. An input "
            "that's silent loses them. That's Part 6's learning rule, building a brain. It's also why a "
            "child's lazy eye has to be treated early."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(normal), FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(kitten), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(adult), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def remap(self):
        d = archive.MERZENICH_1984.data
        head = heading(r"1984: \ a map redrawn in an adult")
        names = [r"finger 1", r"finger 2", r"finger 3", r"finger 4", r"finger 5"]
        cols = [GREY_B, PARIETAL, LESION, TEMPORAL, GREY_B]

        def strip(y, widths, title, gone=False):
            x, g = -6.7, VGroup()
            for i, (w, name) in enumerate(zip(widths, names)):
                if w <= 0:
                    continue
                r = Rectangle(width=w, height=1.0, color=BACKGROUND, stroke_width=3, fill_color=cols[i],
                              fill_opacity=0.75).move_to([x + w / 2, y, 0])
                g.add(VGroup(r, label(name, font_size=26, color=BLACK).move_to(r)))
                x += w
            g.add(label(title, font_size=27, color=GREY_A).next_to(g, UP, buff=0.12).align_to(g, LEFT))
            return g

        before = strip(0.9, [1.3, 1.3, 1.3, 1.3, 1.3], r"the hand's map on the cortex, before")
        after = strip(-1.5, [1.3, 1.95, 0.0, 1.95, 1.3], r"months after finger 3 is lost")
        rows = VGroup(
            wrapped_label(rf"{d['animals']}, \ mapped {d['months']} months after the loss", 5.6, 29, WHITE),
            wrapped_label(r"the cortex that served the lost finger does not fall silent: \ it answers to the "
                          r"neighbours", 5.6, 30, P.ACCENT),
            wrapped_label(r"in people who have lost an arm, \ a touch on the face can be felt in the missing "
                          r"hand: \ on Penfield's map, the face lies next to the hand", 5.6, 29, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.75, -0.3, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.MERZENICH_1984.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "For twenty years after that, the rule was thought to be: plastic in infancy, fixed in "
            "adulthood. Then Michael Merzenich and his colleagues looked at Penfield's map in adult monkeys. "
            "<bookmark mark='a'/> Each finger has its own stretch of cortex. They mapped it, and then one "
            "finger was lost. <bookmark mark='b'/> Months later they mapped the cortex again. The stretch "
            "that had served the missing finger hadn't fallen silent. It now answered to the fingers on "
            "either side. The map had been redrawn, in an adult. <bookmark mark='c'/> The same thing "
            "happens in people. After an arm is lost, some patients find that a touch on the cheek is felt, "
            "at the same moment, in the missing hand. Look back at Penfield's strip. The face lies next to "
            "the hand. The face's input has moved in next door. So a map on the cortex isn't a fixed "
            "allotment. It's the current state of a competition, and what keeps a territory is use."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(before), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(after), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def taxi(self):
        d = archive.MAGUIRE_2000.data
        head = heading(r"London: \ does learning a city change a brain?")
        b = brain_medial(4.0, [-4.7, 1.2, 0])
        back = Dot(b.at(0.3, -0.17), radius=0.16, color=THRESH)
        back_l = label(r"the back of the hippocampus", font_size=25, color=THRESH).next_to(b.shell, DOWN, buff=0.1)
        left = VGroup(
            wrapped_label(rf"2000: \ {d['drivers']} licensed taxi drivers, \ {d['years_driving']:.0f} years at "
                          r"the wheel on average", 6.6, 30, WHITE),
            wrapped_label(r"more grey matter there than in other men, \ and more, the longer they had driven",
                          6.6, 30, WHITE),
            wrapped_label(r"But which came first? \ Perhaps people with that kind of hippocampus become taxi "
                          r"drivers.", 6.6, 30, LESION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([2.9, 1.3, 0])
        keep_in_frame(left)
        counts = [(d["qualified"], rf"{d['qualified']} qualified", SPARED, r"it grew"),
                  (d["failed"], rf"{d['failed']} did not qualify", GREY_B, r"no change"),
                  (d["controls"], rf"{d['controls']} never trained", GREY_B, r"no change")]
        people = VGroup()
        x = -6.4
        for n, name, col, what in counts:
            dots = VGroup(*[Dot(radius=0.08, color=col) for _ in range(n)]).arrange_in_grid(cols=10, buff=0.07)
            cap = VGroup(label(name, font_size=27, color=col), label(what, font_size=29, color=col)).arrange(
                DOWN, buff=0.05)
            grp = VGroup(dots, cap).arrange(DOWN, buff=0.15)
            grp.move_to([x + 1.6, -2.45, 0], aligned_edge=UP).shift(UP * 1.0)
            people.add(grp)
            x += 3.5
        follow = wrapped_label(rf"2011: \ {d['trainees']} trainees scanned before and after years of learning "
                               r"the streets", 3.4, 28, P.ACCENT).move_to([5.2, -2.3, 0])
        keep_in_frame(follow)
        src = published_tag(archive.MAGUIRE_2000.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "And does ordinary learning change a human brain enough to see? The famous test is in London. To "
            "get a taxi licence there you must learn the layout of some twenty-five thousand streets, and "
            f"it takes years. <bookmark mark='a'/> In 2000 Eleanor Maguire scanned {d['drivers']} licensed "
            "drivers. They had more grey matter at the back of the hippocampus than other men of their age, "
            "and the longer they'd driven, the more they had. <bookmark mark='b'/> You know the objection, "
            "from Part 2. That's a comparison of two groups who weren't assigned at random. Maybe people "
            "born with that kind of hippocampus are the ones who become taxi drivers. <bookmark mark='c'/> "
            f"So in 2011 she did the harder study. {d['trainees']} trainees were scanned before they began, "
            f"and again years later. In the {d['qualified']} who qualified, that part of the hippocampus "
            f"had grown. In the {d['failed']} who trained and didn't qualify, it hadn't, and nor had it in "
            "people who never trained. <bookmark mark='d'/> That's as close to an experiment as the question "
            "allows, and it goes on the Ledger as replicated. It's one laboratory and one extraordinary "
            "skill. It doesn't follow that a puzzle on your phone will do the same."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(b.shell), FadeIn(b.hippocampus))
            vo.wait_until("a")
            self.play(FadeIn(back, scale=2.0), FadeIn(back_l), FadeIn(left[0]), FadeIn(left[1]))
            vo.wait_until("b")
            self.play(FadeIn(left[2]))
            vo.wait_until("c")
            self.play(FadeIn(follow), LaggedStart(*[FadeIn(p_) for p_ in people], lag_ratio=0.6), run_time=6.0)
            vo.wait_until("d")
        self.clear_scene()
