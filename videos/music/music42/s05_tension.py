from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403


class Tension(SoundScene):
    def construct(self):
        chapter(self, 4, r"Planning tension", r"Where should a phrase reach its peak?")
        self.factors()
        self.curves()
        self.hear()
        self.climax()

    # ------------------------------------------------------------------
    def factors(self):
        items = [
            (r"listeners can trace tension moment by moment, \ and largely agree \ (Krumhansl, \ 1996; \ Farbood, \ 2012)", WHITE),
            (r"it rises with pitch height, \ dissonance, \ distance from the home chord, \ and density of notes", WHITE),
            (r"Lerdahl and Krumhansl \ (2007) \ predict it from harmony; \ Farbood's model adds melody, \ loudness and tempo", WHITE),
            (r"our crude version, \ bar by bar: \ height above C4 in octaves \ + \ share of non-chord tones \ + \ the chord's distance \ + \ notes per beat over two", TUNE),
            (r"a composer plans the curve: \ where it rises, \ where it peaks, \ where it lets go", GREY_A),
        ]
        rows_scene(self, r"what makes tension", items,
                   "A phrase is also a shape in time: it tightens and relaxes. <bookmark mark='b'/> Listeners can trace that tension moment by moment, with agreement depending on the excerpts, task and listeners, as studies by Carol Krumhansl and later Morwaread Farbood illustrate. <bookmark mark='c'/> Pitch height, dissonance, tonal distance and note density can contribute, with effects that depend on context and listener expectations. <bookmark mark='d'/> Fred Lerdahl and Krumhansl predicted it from harmony in 2007; Farbood's model adds melody, loudness and tempo. <bookmark mark='e'/> Ours is crude, bar by bar: the height above middle C in octaves, plus the share of non-chord tones, plus the chord's distance from the tonic, plus notes per beat over two. <bookmark mark='f'/> A composer plans that curve: where it rises, where it peaks, and where it lets go.", marks="cdef")

    # ------------------------------------------------------------------
    def plot(self, plan, curve, col, title, x0, w=5.2, h=2.2):
        ax = VGroup(Line([x0, -1.6, 0], [x0 + w, -1.6, 0], color=GREY_D), Line([x0, -1.6, 0], [x0, -1.6 + h, 0], color=GREY_D))
        mx = 4.0
        def pts(v):
            return [[x0 + w * (k + 0.5) / len(v), -1.6 + h * y / mx, 0] for k, y in enumerate(v)]
        pl = DashedVMobject(VMobject(color=GREY_A, stroke_width=3).set_points_as_corners(pts(plan)), num_dashes=24)
        cu = VMobject(color=col, stroke_width=4).set_points_as_corners(pts(curve))
        dots = VGroup(*[Dot(p, radius=0.06, color=col) for p in pts(curve)])
        nums = VGroup(*[label(rf"{k + 1}", font_size=14, color=GREY_A).move_to([x0 + w * (k + 0.5) / len(plan), -1.85, 0]) for k in range(len(plan))])
        t = label(title, font_size=19, color=col).move_to([x0 + w / 2, 0.95, 0])
        return VGroup(ax, pl, cu, dots, nums, t)

    def curves(self):
        d = load("tension")
        L, E = d["late"], d["early"]
        a = self.plot(L["plan"], L["curve"], TUNE, rf"late climax: \ fit {L['fit']:.2f}", -6.0)
        b = self.plot(E["plan"], E["curve"], BLUE, rf"early climax: \ fit {E['fit']:.2f}", 0.8)
        key = label(r"dashed: \ the plan; \ solid: \ the tension of the melody the searcher kept \ (bars 1 to 8)", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.6)
        head = label(r"one motive, \ two plans", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        sep = r" \ "
        chords = VGroup(label(r"chords: \ " + sep.join(roman_tex(x) for x in L["chords"]), font_size=16, color=GREY_A).next_to(a, UP, buff=0.25),
                        label(r"chords: \ " + sep.join(roman_tex(x) for x in E["chords"]), font_size=16, color=GREY_A).next_to(b, UP, buff=0.25))
        with self.voiceover(
            "Give chapter nine's searcher, which we will build, two plans for the same motive. <bookmark mark='a'/> One rises "
            "to a climax in bar six and falls to the cadence. <bookmark mark='b'/> The other is tense at once and relaxes "
            "from the middle on, with its strongest harmony, a dominant seventh, in bar two. The searcher scores each draft "
            f"by how well its tension curve follows the plan: the correlation is {say(L['fit'], 2)} for the first and "
            f"{say(E['fit'], 2)} for the second. The early plan is harder, because the motive must be stated plainly "
            "in bar one, where tension starts low."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(chords[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(chords[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("tension")
        c = clip("tension.two")
        L, E = d["late"], d["early"]
        a = scored(L["melody"], L["chords"], width=5.6, height=1.7, lo=57, hi=81, size=13)
        b = scored(E["melody"], E["chords"], width=5.6, height=1.7, lo=57, hi=81, size=13)
        pair = VGroup(VGroup(a, label(rf"peak in bar {L['peak_bar']}", font_size=19, color=TUNE)).arrange(DOWN, buff=0.3),
                      VGroup(b, label(rf"peak in bar {E['peak_bar']}", font_size=19, color=BLUE)).arrange(DOWN, buff=0.3)).arrange(RIGHT, buff=0.8).move_to(UP * 0.3)
        boxes = VGroup(bar_box(a, L["peak_bar"] - 1, TUNE), bar_box(b, E["peak_bar"] - 1, BLUE))
        with self.voiceover(
            "Hear the two melodies the searcher kept, the late climax first. Listen for where each one feels most strained."
        ):
            self.play(FadeIn(pair))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"late climax, \ then early", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            cursor(snd, a, st["late"], 0.42)
            cursor(snd, b, st["early"], 0.42)
        with self.voiceover(
            f"By our measure the first peaks in bar {say(L['peak_bar'])}, high, over the supertonic chord before the "
            f"final dominant; the second peaks in bar {say(E['peak_bar'])} and then sinks for four bars. Whether your ear "
            "agreed is exactly the test a tension model has to pass."
        ):
            self.play(FadeIn(boxes))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def climax(self):
        items = [
            (r"composition treatises put a phrase's high point late: \ about two-thirds of the way or after", WHITE),
            (r"Part 21 tested the `golden section' claims for whole movements: \ weak evidence once chance is allowed for", WHITE),
            (r"late peaks leave time to fall back to the cadence; \ early peaks need something to sustain the rest", WHITE),
            (r"planning tension is planning expectation: \ Part 46 measures it in listeners", TUNE),
            (r"chapter 5: \ constraints, \ counted", GREY_A),
        ]
        rows_scene(self, r"where the peak goes", items,
                   "Where should the peak go? <bookmark mark='b'/> Composition treatises put a phrase's high point late, about "
                   "two-thirds of the way through or after. <bookmark mark='c'/> Part 21 tested the golden-section claims for "
                   "whole movements, and found weak evidence once chance was allowed for. <bookmark mark='d'/> A late peak "
                   "leaves time to fall back to the cadence; an early one needs something to sustain the rest. "
                   "<bookmark mark='e'/> Planning tension is really planning expectation, which Part 46 measures in listeners. "
                   "<bookmark mark='f'/> Chapter five counts what constraints do.", marks="cdef")
