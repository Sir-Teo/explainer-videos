from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403

LEFT_H, RIGHT_H = FRONTAL, PARIETAL


def top_view(center, word=None, side=-1, cut=True, scale=1.0):
    """The two hemispheres from above with a screen in front: a word flashed to one side of the fixation point
    reaches the hemisphere on the other side."""
    c = np.asarray(center, float)
    k = scale
    hl = Ellipse(width=1.5 * k, height=2.3 * k, color=LEFT_H, stroke_width=3, fill_color=LEFT_H, fill_opacity=0.3).move_to(
        c + LEFT * 0.85 * k)
    hr = Ellipse(width=1.5 * k, height=2.3 * k, color=RIGHT_H, stroke_width=3, fill_color=RIGHT_H, fill_opacity=0.3).move_to(
        c + RIGHT * 0.85 * k)
    band = Line(c + LEFT * 0.2 * k, c + RIGHT * 0.2 * k, color=VOLT, stroke_width=14 * k)
    g = VGroup(hl, hr, band)
    g.hl, g.hr = hl, hr
    if cut:
        g.add(VGroup(Line(c + UP * 0.35 * k, c + DOWN * 0.35 * k, color=LESION, stroke_width=5)))
    screen_y = c[1] + 2.45 * k
    screen = Line([c[0] - 2.4 * k, screen_y, 0], [c[0] + 2.4 * k, screen_y, 0], color=GREY_B, stroke_width=4)
    fix = Dot([c[0], screen_y, 0], radius=0.08 * k, color=WHITE)
    g.add(screen, fix)
    if word is not None:
        w = label(word, font_size=int(30 * k), color=THRESH).move_to([c[0] + side * 1.45 * k, screen_y + 0.38 * k, 0])
        target = hr if side < 0 else hl
        ray = Arrow([c[0] + side * 1.45 * k, screen_y - 0.05, 0], target.get_top() + DOWN * 0.1, color=THRESH,
                    stroke_width=3, buff=0.05, max_tip_length_to_length_ratio=0.1)
        g.add(w, ray)
        g.word, g.ray = w, ray
    g.names = VGroup(label(r"left", font_size=int(22 * k), color=LEFT_H).move_to(hl),
                     label(r"right", font_size=int(22 * k), color=RIGHT_H).move_to(hr))
    g.add(g.names)
    return g


class Split(VoiceoverScene):
    def construct(self):
        self.card()
        self.cut()
        self.test()
        self.interpreter()
        self.myth()

    def card(self):
        card = chapter_card(8, r"Two hemispheres", r"What happens when the cable between them is cut?", lit=(),
                            part=PART, scale=("brain", "mind"), marr=("how", "tissue"))
        with self.voiceover(
            "Chapter eight. Two hemispheres."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def cut(self):
        head = heading(r"The 1960s: \ the cable is cut, and nothing seems to change")
        v = top_view([-3.9, -0.75, 0], cut=False, scale=1.3)
        slash = Line(v[2].get_center() + UP * 0.45, v[2].get_center() + DOWN * 0.45, color=LESION, stroke_width=6)
        under = VGroup(wrapped_label(r"speaks; \ moves the right hand; \ sees the right side", 2.9, 25, LEFT_H).next_to(
            v.hl, DOWN, buff=0.2).shift(LEFT * 0.45),
            wrapped_label(r"silent; \ moves the left hand; \ sees the left side", 2.9, 25, RIGHT_H).next_to(
                v.hr, DOWN, buff=0.2).shift(RIGHT * 0.45))
        keep_in_frame(under)
        rows = VGroup(
            wrapped_label(r"to stop seizures spreading, \ surgeons cut the corpus callosum", 5.8, 31, WHITE),
            wrapped_label(r"the patients walk, talk and work as before", 5.8, 31, SPARED),
            wrapped_label(r"Sperry and Gazzaniga's trick: \ flash a word to one side of where the patient is "
                          r"looking. \ It reaches one hemisphere only.", 5.8, 31, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.6, 0.1, 0])
        keep_in_frame(rows)
        tag = note(r"schematic: the brain from above, a screen in front").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The two halves of your brain are joined by the corpus callosum, the white band from the tour. "
            "<bookmark mark='a'/> In the nineteen-sixties surgeons began cutting it, in patients whose "
            "seizures started on one side and spread to the other. It worked. <bookmark mark='b'/> And the "
            "astonishing thing was how little else seemed to change. The patients walked, talked, worked, "
            "and joked as before. You could have dinner with one and notice nothing. <bookmark mark='c'/> "
            "It took an experiment to find what had happened, and it was designed at Caltech by Roger Sperry "
            "and his student Michael Gazzaniga. Remember the crossing. Whatever is to the left of the point "
            "you're looking at goes to your right hemisphere, and the other way round. So have the patient "
            "stare at a dot, and flash a word to one side, too briefly for the eyes to move. With the cable "
            "cut, that word has reached one hemisphere, and it can't be passed to the other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(v), FadeIn(under))
            vo.wait_until("a")
            self.play(Create(slash), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def test(self):
        head = heading(r"One word, two answers")
        a = top_view([-4.0, -1.2, 0], word=r"RING", side=1, scale=1.0)
        b = top_view([3.2, -1.2, 0], word=r"KEY", side=-1, scale=1.0)
        ra = VGroup(label(r"word on the right", font_size=26, color=GREY_A),
                    wrapped_label(r"``What did you see?'' \ ``Ring.''", 3.4, 28, LEFT_H)).arrange(DOWN, buff=0.12)
        ra.next_to(a, DOWN, buff=0.25)
        rb = VGroup(label(r"word on the left", font_size=26, color=GREY_A),
                    wrapped_label(r"``What did you see?'' \ ``Nothing.''", 3.4, 28, LEFT_H),
                    wrapped_label(r"the left hand, out of sight, picks the key from a pile of objects", 3.8, 26,
                                  RIGHT_H)).arrange(DOWN, buff=0.12)
        rb.next_to(b, DOWN, buff=0.25)
        if rb.get_bottom()[1] < -3.75:
            VGroup(a, b, ra, rb).shift(UP * (-3.75 - rb.get_bottom()[1]))
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Flash a word on the right. <bookmark mark='a'/> It goes to the left hemisphere, which has "
            "speech. What did you see? Ring. <bookmark mark='b'/> Now flash a word on the left. It goes to "
            "the right hemisphere. What did you see? Nothing, says the patient. I didn't see anything. "
            "<bookmark mark='c'/> But put the patient's left hand behind a screen, among a pile of objects, "
            "and ask it to find what was shown. The left hand belongs to the right hemisphere. It feels "
            "about, and picks out the key. Ask the patient why they're holding a key, and they don't know. "
            "<bookmark mark='d'/> So there are two streams of knowing in one skull. Each hemisphere "
            "perceives, remembers, and chooses. Only one of them can tell you about it. And the one that "
            "talks has no idea the other is there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(historical_tag(archive.GAZZANIGA_1978.cite)), FadeIn(a))
            vo.wait_until("a")
            self.play(FadeIn(ra))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(rb[0]), FadeIn(rb[1]))
            vo.wait_until("c")
            self.play(FadeIn(rb[2], shift=UP * 0.1))
            vo.wait_until("d")
        self.clear_scene()

    def interpreter(self):
        head = heading(r"The half that talks explains what the other half did")
        v = top_view([-4.3, -1.3, 0], scale=0.95)

        def card_(text, col, w=2.3):
            box = RoundedRectangle(width=w, height=0.8, corner_radius=0.12, color=col, stroke_width=3,
                                   fill_color="#111722", fill_opacity=1)
            return VGroup(box, wrapped_label(text, w - 0.25, 24, col).move_to(box))

        sees_l = card_(r"a chicken's claw", LEFT_H).next_to(v, UP, buff=0.2).shift(RIGHT * 1.5)
        sees_r = card_(r"a house in snow", RIGHT_H).next_to(v, UP, buff=0.2).shift(LEFT * 1.5)
        picks = VGroup(
            VGroup(label(r"the right hand picks", font_size=24, color=LEFT_H), card_(r"a chicken", LEFT_H)).arrange(
                RIGHT, buff=0.25),
            VGroup(label(r"the left hand picks", font_size=24, color=RIGHT_H), card_(r"a shovel", RIGHT_H)).arrange(
                RIGHT, buff=0.25),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.3).move_to([3.2, 1.5, 0])
        q = quote_card(r"``Why the shovel?'' \ ``Oh, that's simple. The chicken claw goes with the chicken, and "
                       r"you need a shovel to clean out the chicken shed.''", r"a split-brain patient, as "
                       r"Gazzaniga reports it", width=7.0, font_size=26)
        q.move_to([3.2, -0.9, 0])
        keep_in_frame(q)
        end = wrapped_label(r"No hesitation, no ``I don't know''. \ Part 3 called this telling more than we can "
                            r"know.", 7.0, 27, P.ACCENT).next_to(q, DOWN, buff=0.3)
        keep_in_frame(end)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Gazzaniga then ran the experiment that turned a curiosity into a discovery about all of us. "
            "<bookmark mark='a'/> Show each hemisphere a different picture at once. The left hemisphere sees "
            "a chicken's claw. The right sees a house in the snow. <bookmark mark='b'/> Then each hand picks "
            "a card that goes with what its hemisphere saw. The right hand picks a chicken. The left hand "
            "picks a snow shovel. <bookmark mark='c'/> Now ask the patient, which means asking the left "
            "hemisphere, why the left hand is pointing at a shovel. The left hemisphere never saw the snow. "
            "It doesn't say, I don't know. It says, without a pause: that's simple. The chicken claw goes "
            "with the chicken, and you need a shovel to clean out the chicken shed. <bookmark mark='d'/> "
            "The talking hemisphere watched an action it didn't choose, and made up a reason, and believed "
            "it. Gazzaniga called it the interpreter. You met its work in Part 3, in people with whole "
            "brains, who confidently explained choices they'd never made. It runs all the time. A cut cable "
            "just lets us catch it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(historical_tag(archive.GAZZANIGA_1978.cite)), FadeIn(v))
            vo.wait_until("a")
            self.play(FadeIn(sees_l), FadeIn(sees_r))
            vo.wait_until("b")
            self.play(FadeIn(picks[0]))
            self.play(FadeIn(picks[1]))
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def myth(self):
        h = load("hemispheres")
        d = archive.NIELSEN_2013.data
        head = heading(r"Are you ``left-brained'' or ``right-brained''?")
        A = axes([-2.5, 2.5], [0, 1.9], x_length=6.4, y_length=3.5, xticks=[-2, -1, 0, 1, 2], yticks=[],
                 xlabel=r"a person's lean, averaged over the whole brain \ (left $\leftarrow$ \ $\rightarrow$ right)",
                 ylabel=r"how many people", center=[-3.5, -0.75, 0])
        ax = A.ax
        ht = hist(ax, h["edges"], h["index_types"], LESION, opacity=0.45)
        hl = hist(ax, h["edges"], h["index_local"], MODEL, opacity=0.6)
        lg = legend([(LESION, r"if people came in types"), (MODEL, r"if each network leans by itself")], font_size=25)
        lg.next_to(A, UP, buff=0.1).align_to(A, LEFT)
        side = VGroup(
            wrapped_label(rf"the test: \ {fmt_int(d['people'])} people, \ the connections of "
                          rf"{fmt_int(d['regions'])} regions", 5.4, 29, WHITE),
            wrapped_label(r"language networks lean left and attention networks lean right, \ in nearly "
                          r"everybody", 5.4, 29, WHITE),
            wrapped_label(r"but one network's lean says nothing about another's: \ no whole-brain type", 5.4, 29,
                          MODEL),
            wrapped_label(r"The hemispheres differ. \ People are not one or the other.", 5.4, 31, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([4.0, -0.5, 0])
        keep_in_frame(side)
        # the popular claim, as it is sold
        types = VGroup()
        for name, col, words in ((r"``left-brained''", LEFT_H, r"logical, \ verbal, \ good with numbers"),
                                 (r"``right-brained''", RIGHT_H, r"creative, \ intuitive, \ artistic")):
            box = RoundedRectangle(width=4.6, height=2.6, corner_radius=0.15, color=col, stroke_width=3,
                                   fill_color=col, fill_opacity=0.08)
            txt = VGroup(label(name, font_size=38, color=col), wrapped_label(words, 4.0, 30, WHITE)).arrange(
                DOWN, buff=0.25).move_to(box)
            types.add(VGroup(box, txt))
        types.arrange(RIGHT, buff=0.8).move_to([0, 0.1, 0])
        types_l = label(r"a magazine, 1973; \ management courses and quizzes ever since", font_size=28,
                        color=GREY_A).next_to(types, DOWN, buff=0.35)
        src = published_tag(archive.NIELSEN_2013.cite)
        tag = psyche_tag(r"simulated: what each hypothesis predicts")
        with self.voiceover(
            "Out of this real and strange finding grew one of popular psychology's most durable ideas. In "
            "1973 a magazine article announced that we are left-brained or right-brained: logical people "
            "run on the left hemisphere, creative people on the right. It's in management courses and "
            "personality quizzes to this day. <bookmark mark='a'/> It makes a prediction. If people came in "
            "types, then someone whose language network leans left more than average should have "
            "everything else leaning left too. Average a person's lean over the whole brain, and people "
            "would spread out widely, like the red histogram. If instead each network leans by itself, the "
            "leans cancel, and everyone lands near the middle, like the green one. <bookmark mark='b'/> In "
            f"2013 a group in Utah looked, in brain scans of {d['people']:,} people. Language networks lean "
            "left, and attention networks lean right, in nearly everybody. <bookmark mark='c'/> But how "
            "strongly one network leaned in a person told you nothing about any other network. The data "
            "were, in their words, not consistent with a whole-brain type. <bookmark mark='d'/> So the "
            "hemispheres do differ in what they do. That part is true, and you've just seen it. The claim "
            "that fails is that a person is one or the other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.1) for t_ in types], lag_ratio=0.6), run_time=3.0)
            self.play(FadeIn(types_l))
            vo.wait_until("a")
            self.play(FadeOut(types), FadeOut(types_l))
            self.play(FadeIn(A), FadeIn(ht, lag_ratio=0.02), FadeIn(lg[0]), run_time=2.0)
            self.play(FadeIn(hl, lag_ratio=0.02), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()
