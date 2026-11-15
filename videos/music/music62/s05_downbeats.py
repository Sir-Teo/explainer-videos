from __future__ import annotations

from videos.music.music62.common import *  # noqa: F403


class Downbeats(SoundScene):
    def construct(self):
        chapter(self, 4, r"Bars and downbeats", r"Which beat is beat one?")
        self.quiz()
        self.lowband()
        self.meters()
        self.cues()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("downbeat")
        c = clip("downbeat.two")
        card = listen_card(r"The session with a click on every beat, \ and a higher click every four. \ Twice. \ In which do the "
                           r"high clicks mark the start of each bar?", width=10.0)
        with self.voiceover("Your turn. The session with a click on every beat and a higher click every four, twice. In which do the high clicks mark the start of each bar?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"where is one?", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(r"the second: \ the accent falls with the kick drum and the chord changes; \ in the first it falls on the snare", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover("The second. There the accent falls with the kick drum and the changes of chord. In the first it falls on the snare, the backbeat, and the bar feels as if it starts in the wrong place."):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lowband(self):
        d = load("downbeat")
        s = d["strength"]
        top = max(s)
        bars = VGroup()
        for k, v in enumerate(s):
            b = Rectangle(width=1.0, height=max(0.02, 3.0 * v / top), stroke_width=0, fill_color=TUNE if v > 0.8 * top else GREY_B, fill_opacity=0.85)
            bars.add(VGroup(b, label(rf"beat {k + 1}", font_size=17, color=WHITE).next_to(b, DOWN, buff=0.15)))
        bars.arrange(RIGHT, buff=0.8, aligned_edge=DOWN).move_to(DOWN * 0.3 + LEFT * 2.0)
        side = VGroup(label(r"the low band's novelty \ (below 150 Hz: \ kick and bass), \ averaged at each place in the bar", font_size=17, color=WHITE),
                      label(r"beats 1 and 3 are strong; \ 2 and 4 weak", font_size=17, color=TUNE),
                      label(r"it says the bar has two strong beats, \ not which is first: \ chord changes and phrases must decide", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 3.5 + DOWN * 0.3)
        head = label(r"a clue in the bass", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How might a machine know? <bookmark mark='a'/> One clue is low: the kick drum and the bass mark strong beats. "
            "Average the low band's novelty at each of the four places in the bar. <bookmark mark='b'/> Beats one and three are "
            "strong, two and four weak. <bookmark mark='c'/> That says the bar has two strong beats, not which one comes first; "
            "chord changes, phrase lengths and melody have to decide, and modern systems learn all of them together."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meters(self):
        items = [
            (r"duple and triple: \ a march in two, \ a waltz in three, \ strong beats spaced differently", WHITE),
            (r"compound meters: \ 6/8 groups six quick beats in two threes, \ and is easily heard as 3/4", WHITE),
            (r"swing: \ the off-beat moved late, \ about two thirds of the way through the beat, \ or less", WHITE),
            (r"additive meters: \ 7/8 as 2+2+3, \ beats of unequal length", WHITE),
            (r"a downbeat tracker must first know which of these it is hearing", TUNE),
        ]
        rows_scene(self, r"other meters", items,
                   "And bars come in more shapes than four-four. <bookmark mark='b'/> Duple and triple: a march in two, a waltz in "
                   "three, their strong beats spaced differently. <bookmark mark='c'/> Compound meters: six-eight groups six quick "
                   "beats in two threes, and is easily heard as three-four. <bookmark mark='d'/> Swing moves the off-beat late, "
                   "about two thirds of the way through the beat, or less. <bookmark mark='e'/> Additive meters, like seven-eight "
                   "as two plus two plus three, have beats of unequal length. <bookmark mark='f'/> A downbeat tracker must first "
                   "know which of these it is hearing.", marks="bcdef")

    # ------------------------------------------------------------------
    def cues(self):
        items = [
            (r"harmony changes on strong beats; \ bass notes land on beat one; \ melodies end phrases there", WHITE),
            (r"meter is a hierarchy: \ beats within bars, \ bars within phrases \ (Part 9's grid)", WHITE),
            (r"downbeat trackers combine beat tracking with these cues, \ and since the 2010s, \ networks trained on annotated songs", WHITE),
            (r"they inherit the annotations' habits: \ 4/4, \ Western popular music, \ steady tempo", TUNE),
        ]
        rows_scene(self, r"what tells us where the bar starts", items,
                   "What tells a listener where the bar starts? <bookmark mark='b'/> Harmony changes on strong beats, bass notes "
                   "land on beat one, and melodies end their phrases there. <bookmark mark='c'/> Meter is a hierarchy: beats within "
                   "bars, bars within phrases. <bookmark mark='d'/> Downbeat trackers combine beat tracking with these cues, and "
                   "since the 2010s networks trained on annotated songs do it all at once. <bookmark mark='e'/> They inherit their "
                   "annotations' habits: four-four time, Western popular music, steady tempos. Chapter 11 returns to that.",
                   marks="bcde")
