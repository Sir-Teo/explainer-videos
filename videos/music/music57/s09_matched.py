from __future__ import annotations

from videos.music.music57.common import *  # noqa: F403


class Matched(SoundScene):
    def construct(self):
        chapter(self, 8, r"Comparing at equal loudness", r"Can you trust your ears when one version is louder?")
        self.quiz()
        self.bias()
        self.method()
        self.series_rule()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("matched")
        c = clip("matched.two")
        card = listen_card(r"Two masters of Part 56's mix. \ Listen to both, \ and decide which sounds better: \ fuller, \ clearer, \ more "
                           r"alive.", width=10.0)
        with self.voiceover(
            "Your turn again. Two masters of Part 56's mix. Listen to both, and decide which sounds better: fuller, clearer, "
            "more alive."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second", r"no difference"], width=2.8, buff=0.8).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two masters?", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
            pulse(snd, boxes[2], 0, c.duration, rate=5.0, color=GREY_B, buff=0.08)
        res = label(r"the same master, \ sample for sample; \ the second is 1 dB louder, \ and nothing else", font_size=20, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            "If you chose the second, you are in good company. They are the same master, sample for sample; the second is "
            "one decibel louder, and nothing else. A decibel is barely a change in loudness, and yet it reliably reads as a "
            "change in quality."
        ):
            self.play(boxes[2][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bias(self):
        items = [
            (r"louder sounds better: \ more bass and treble \ (the ear's curves flatten with level, \ Part 4), \ more detail above the room's noise", WHITE),
            (r"listening tests find that a version a fraction of a decibel louder is preferred even when listeners hear no level difference", WHITE),
            (r"so every plug-in that makes things a little louder seems to improve them; \ every comparison of masters is rigged unless matched", WHITE),
            (r"the loudness war ran on this bias, \ one decibel at a time", TUNE),
        ]
        rows_scene(self, r"the loudness bias", items,
                   "Why? <bookmark mark='b'/> Louder really does sound fuller: the ear's equal-loudness curves flatten as level "
                   "rises, as Part 4 showed, so bass and treble come up, and quiet detail rises above the room's noise. "
                   "<bookmark mark='c'/> Listening tests find that a version a fraction of a decibel louder is preferred even when "
                   "the listeners report no difference in level. <bookmark mark='d'/> So every plug-in that makes things a little "
                   "louder seems to improve them, and every comparison of masters is rigged unless the levels are matched. "
                   "<bookmark mark='e'/> The loudness war ran on this bias, one decibel at a time.", marks="bcde")

    # ------------------------------------------------------------------
    def method(self):
        items = [
            (r"match the integrated loudness, \ to a tenth of a decibel, \ before comparing anything", WHITE),
            (r"switch quickly: \ auditory memory for timbre fades within seconds", WHITE),
            (r"blind: \ the listener must not know which is which \ (ABX, \ David Clark's comparator, \ about 1980: \ is X the same as A or as B?)", WHITE),
            (r"repeat, \ and count: \ 12 right out of 16 is significant at the 5\% level \ (Part 67)", WHITE),
            (r"ITU-R BS.1116 and MUSHRA formalize this for codecs and systems \ (Part 58)", TUNE),
        ]
        rows_scene(self, r"the method", items,
                   "So comparisons have a method. <bookmark mark='b'/> Match the integrated loudness to a tenth of a decibel before "
                   "comparing anything. <bookmark mark='c'/> Switch quickly, because memory for timbre fades within seconds. "
                   "<bookmark mark='d'/> Compare blind: the ABX test, from David Clark's comparator of about 1980, asks only whether X is "
                   "A or B, and the listener must not know. <bookmark mark='e'/> Repeat, and count: twelve right out of sixteen is "
                   "significant at five per cent, as Part 67 will show. <bookmark mark='f'/> The ITU's BS.1116 and the MUSHRA "
                   "method formalize all this for testing codecs and systems, which Part 58 uses.", marks="bcdef")

    # ------------------------------------------------------------------
    def series_rule(self):
        items = [
            (r"every ear question in this series compares sounds already matched in loudness, \ unless loudness is the point", WHITE),
            (r"each clip is set by its loudest 400 ms: \ $-15$ LUFS for an example, \ $-21$ for one meant to sit back", WHITE),
            (r"so when Part 50 compared a compressed sound with the original, \ louder could not win; \ and here the gentle master did not lose by being quieter", WHITE),
            (r"equal loudness is the series' way of making an ear question a fair one", TUNE),
        ]
        rows_scene(self, r"this series' rule", items,
                   "This series has followed the rule from the start. <bookmark mark='b'/> Every ear question compares sounds "
                   "already matched in loudness, unless loudness is the point. <bookmark mark='c'/> Each clip is set by its loudest "
                   "four hundred milliseconds, to minus fifteen LUFS for an example, minus twenty-one for one meant to sit back. "
                   "<bookmark mark='d'/> So when Part 50 compared a compressed sound with the original, louder could not win, and in this "
                   "part's hook the gentle master did not lose by being quieter. <bookmark mark='e'/> Equal loudness is what makes an ear question "
                   "fair.", marks="bcde")
