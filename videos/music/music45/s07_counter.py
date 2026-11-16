from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403


class Counter(SoundScene):
    def construct(self):
        chapter(self, 6, r"Counterpoint as scene analysis", r"Why are parallel fifths forbidden?")
        self.huron()
        self.hear()
        self.bounce()
        self.rules()
        self.onsets()
        self.other()

    # ------------------------------------------------------------------
    def huron(self):
        items = [
            (r"David Huron, \ `Tone and Voice' \ (2001): \ derive the rules of voice leading from how hearing groups sound", WHITE),
            (r"the goal assumed: \ several lines, \ each heard as a line, \ none lost and none merged", WHITE),
            (r"then each classical rule turns out to protect one of the grouping principles", WHITE),
            (r"and his corpus counts showed composers obeying them more when the goal mattered more", TUNE),
            (r"Part 16's rules, \ seen from the listener's side", GREY_A),
        ]
        rows_scene(self, r"rules from perception", items,
                   "Now the payoff. <bookmark mark='b'/> In 2001 David Huron published a long paper, Tone and Voice, that derives the rules of voice leading from how hearing groups sound. <bookmark mark='c'/> Assume one goal: several lines, each heard as a line, none lost and none merged with another. <bookmark mark='d'/> Several voice-leading conventions can then be interpreted as promoting perceptual independence, alongside historical and stylistic explanations, <bookmark mark='e'/> and his counts in the repertoire showed composers obeying the rules more strictly where that goal mattered more. <bookmark mark='f'/> These are Part 16's rules, seen from the listener's side.", marks="bcdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("fuse")
        c = clip("fuse.two")
        beat = d["beat"]
        def two(a, b, col):
            notes = [[m, i, 0.9] for i, m in enumerate(a)] + [[m, i, 0.9] for i, m in enumerate(b)]
            return mroll(notes, width=4.6, height=1.8, lo=56, hi=82, color=col, total=len(a), bar_h=0.13)
        A = two(d["top"], d["parallel"], TUNE)
        B = two(d["top"], d["contrary"], BLUE)
        cells = VGroup(VGroup(label(r"parallel fifths", font_size=20, color=TUNE), A).arrange(DOWN, buff=0.25),
                       VGroup(label(r"contrary motion", font_size=20, color=BLUE), B).arrange(DOWN, buff=0.25)).arrange(RIGHT, buff=1.4).move_to(UP * 0.3)
        head = label(r"how many voices?", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear two violin duets with the same upper line. In the first, the lower part follows a fifth below in parallel. "
            "In the second, it moves the other way. Ask yourself how many voices you hear in each."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two duets", kind="synthesized", detail=r"additive, \ bowed-string spectrum", corner=DL, tag_corner=DR)
            n = len(d["top"])
            flash(snd, A.notes, [st["parallel"] + (i % n) * beat for i in range(2 * n)], hot=WHITE, base=TUNE)
            flash(snd, B.notes, [st["contrary"] + (i % n) * beat for i in range(2 * n)], hot=WHITE, base=BLUE)
        with self.voiceover(
            "In parallel fifths the two lines lock together into something like one richer line: every lower note puts its "
            "harmonics under the upper note's, and both move at the same moments in the same direction, harmonicity and "
            "common fate at once. In contrary motion the two lines stay two. That is the perceptual reason behind the oldest "
            "rule in counterpoint."
        ):
            self.play(Indicate(cells[0][0]), Indicate(cells[1][0]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        rows_ = VGroup()
        table = [(r"avoid parallel fifths and octaves", r"tonal fusion and common fate would merge the voices"),
                 (r"move by step; \ recover from leaps", r"pitch proximity keeps each line one stream"),
                 (r"avoid crossing voices", r"crossed lines regroup by pitch, \ as in the scale illusion"),
                 (r"keep voices apart, \ but not too far", r"too close they fuse; \ too far apart they stop being one texture"),
                 (r"stagger entries \ (imitation)", r"a new voice entering alone is heard as new: \ onset grouping")]
        for rule, why in table:
            rows_.add(VGroup(label(rule, font_size=19, color=TUNE), label(why, font_size=18, color=WHITE)).arrange(RIGHT, buff=0.6))
        for r in rows_:
            r[0].move_to([-3.4, 0, 0])
            r[1].next_to(r[0], RIGHT, buff=0.5)
        rows_.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(DOWN * 0.1)
        rows_.scale_to_fit_width(min(rows_.width, 12.8))
        head = label(r"the rules and the principles behind them", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is the mapping. <bookmark mark='a'/> Avoid parallel fifths and octaves, because fusion and common fate "
            "would merge the voices. <bookmark mark='b'/> Move by step and recover from leaps, because pitch proximity keeps "
            "each line one stream. <bookmark mark='c'/> Avoid crossing voices, because crossed lines regroup by pitch, as in "
            "the scale illusion. <bookmark mark='d'/> Keep voices apart, but not too far: too close they fuse, too far they "
            "stop being one texture. <bookmark mark='e'/> And stagger entries, because a voice entering alone is heard as "
            "new."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def other(self):
        items = [
            (r"the derivation predicts that the rules relax where independence is not wanted", WHITE),
            (r"Part 41's Bol\'ero mixtures and organ stops use parallel motion on purpose: \ to fuse", WHITE),
            (r"rock power chords \ (Part 40) \ are parallel fifths: \ one thick voice, \ not two", WHITE),
            (r"a style's rules encode its goal; \ change the goal and the rules change", TUNE),
            (r"chapter 7: \ the dimension of sound the rules never mention, \ timbre", GREY_A),
        ]
        rows_scene(self, r"when the rules relax", items,
                   "The derivation also predicts when the rules relax. <bookmark mark='b'/> Where independence is not wanted, "
                   "composers break them on purpose. <bookmark mark='c'/> Part 41's Boléro mixtures and the organ's stops move "
                   "in parallel to fuse, <bookmark mark='d'/> and rock power chords, from Part 40, are parallel fifths, one thick "
                   "voice rather than two. <bookmark mark='e'/> A style's rules encode its goal; change the goal and the rules "
                   "change. <bookmark mark='f'/> Chapter seven turns to the dimension the old rules never mention: timbre.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def bounce(self):
        d = load("bounce")
        c = clip("bounce.cross")
        n = len(d["up"])
        notes = [[m, i, 0.9] for i, m in enumerate(d["up"])] + [[m, i, 0.9] for i, m in enumerate(d["down"])]
        r = mroll(notes, width=8.0, height=2.4, lo=58, hi=74, color=GREY_B, total=n, bar_h=0.15).move_to(UP * 0.4)
        a = VMobject(color=TUNE, stroke_width=3).set_points_as_corners([r.notes[i].get_center() for i in range(n)])
        b = VMobject(color=BLUE, stroke_width=3).set_points_as_corners([r.notes[n + i].get_center() for i in range(n)])
        bh = VMobject(color=EAR, stroke_width=3).set_points_as_corners([r.notes[i if i < n // 2 else n + i].get_center() for i in range(n)])
        bl = VMobject(color=EAR, stroke_width=3).set_points_as_corners([r.notes[n + i if i < n // 2 else i].get_center() for i in range(n)])
        cap = label(r"played: \ a scale up \ (gold) \ and a scale down \ (blue) \ that cross", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"crossing, \ or bouncing?", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Why do voices avoid crossing? Hear a rising scale and a falling scale played together on the same kind of tone, "
            "crossing in the middle."
        ):
            self.play(FadeIn(head), FadeIn(r), Create(a), Create(b), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"two scales", kind="synthesized", detail=r"sine tones", corner=DL, tag_corner=DR)
            flash(snd, r.notes, [(i % n) * d["ioi"] for i in range(2 * n)], hot=WHITE, base=GREY_B)
            cursor(snd, r, 0.0, d["ioi"], color=WHITE)
        cap2 = label(r"heard: \ a high line that comes down and goes back up, \ a low line that goes up and comes back down", font_size=19, color=EAR).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            'Most people do not hear the scales cross. They hear a high line that comes down and bounces back up, and a low line that rises and falls back, each staying in its own range: the scale illusion again, without the ears. Tougas and Bregman studied this in 1985. Contrasting timbres can help preserve crossing-line identity, alongside rhythm, articulation and prior context.'
        ):
            self.play(FadeOut(a), FadeOut(b), FadeOut(cap), Create(bh), Create(bl), FadeIn(cap2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def onsets(self):
        items = [
            (r"onsets bind: \ voices that always move together in rhythm start to sound like one", WHITE),
            (r"Huron's counts: \ in Bach's polyphony, \ voices begin notes together less often than chance would give", WHITE),
            (r"rhythmic independence is the time-domain twin of contrary motion", WHITE),
            (r"chorales \ (Part 17) \ move together on purpose: \ one sound of four voices, \ a homophonic texture", TUNE),
            (r"the texture a composer wants decides which rules apply", GREY_A),
        ]
        rows_scene(self, r"onsets and independence", items,
                   "Rhythm matters as well. <bookmark mark='b'/> Voices that always start their notes together begin to sound "
                   "like one. <bookmark mark='c'/> Huron's counts showed that in Bach's polyphony, voices begin notes together "
                   "less often than chance would give: <bookmark mark='d'/> rhythmic independence is the twin, in time, of "
                   "contrary motion. <bookmark mark='e'/> Chorales, from Part 17, move together on purpose, one sound of four "
                   "voices. <bookmark mark='f'/> The texture a composer wants decides which rules apply.", marks="bcdef")
