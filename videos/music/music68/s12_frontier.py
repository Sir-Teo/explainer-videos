from __future__ import annotations

from videos.music.music68.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ what is still unknown", r"Why do simple ratios sound good, and what else is open?")
        self.question()
        self.fifths()
        self.answers()
        self.open_()
        self.star()

    # ------------------------------------------------------------------
    def question(self):
        lines = VGroup(
            label(r"Part 1: \ stop a string at two thirds of its length, \ and it sounds a fifth higher", font_size=21, color=WHITE),
            label(r"an ancient experiment linking music and physical measurement is a musical one", font_size=21, color=WHITE),
            label(r"its question, \ 2{,}500 years old: \ why do simple ratios sound good?", font_size=26, color=TUNE),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.3)
        with self.voiceover(
            "The series began with a question. <bookmark mark='a'/> Stop a string at two thirds of its length and it sounds a "
            "fifth higher. That is an ancient experiment linking music and physical measurement, and it is a musical one. <bookmark mark='b'/> The "
            "question it left is two and a half thousand years old: why do simple ratios sound good? Sixty-seven parts later, "
            "how much of it is answered?"
        ) as vo:
            self.play(FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fifths(self):
        d = load("fifths")
        c = clip("unknown.fifths")
        card = listen_card(r"Part 1's string sounds a fifth with its open string twice: \ once at exactly 3:2, \ once with the bridge "
                           r"moved by one per cent. \ Which one beats?", width=9.6)
        with self.voiceover(
            "First, Part 1's string once more. It sounds a fifth with the open string twice: once at exactly three to two, and "
            "once with the bridge moved by one per cent. Which one beats?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"], width=3.0, buff=1.2).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two fifths", kind="physical model", detail=r"Part 1's string", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["pure"], st["off"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["off"], c.duration, buff=0.08)
        res = VGroup(
            label(rf"the second: \ the open string's third partial and the fifth's second, \ {say(3 * d['f0'])} Hz and "
                  rf"{2 * 1.5 * d['f0'] / 1.01:.0f} Hz, \ beat about {d['beat_hz']:.0f} times a second", font_size=19, color=TUNE),
            label(r"at 3:2 the two partials coincide, \ and those two partials do not beat against each other", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 1.5)
        with self.voiceover(
            "The second. The open string's third partial and the fifth's second partial sit "
            f"{say(round(d['beat_hz']))} hertz apart, and so beat about {say(round(d['beat_hz']))} times a second. At exactly three "
            "to two those two partials coincide, and those two partials do not beat against each other. That is Helmholtz's answer, and Part 5's."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def answers(self):
        items = [
            (r"the physics: \ at simple ratios the partials of harmonic tones coincide, \ so they do not beat or roughen \ (Helmholtz; \ Part 5)", WHITE),
            (r"the ear: \ such a chord also looks like one harmonic series, \ one source, \ to a pitch model \ (harmonicity; \ Parts 4 and 5)", WHITE),
            (r"the timbre: \ bend the partials, \ and other intervals become the smooth ones \ (Sethares; \ Variation 5)", WHITE),
            (r"the culture: \ in 2016 listeners in the Bolivian Amazon heard roughness, \ but did not prefer consonance \ (McDermott et al.; \ Part 47)", EAR),
            (r"so part of the answer is in the sound, \ part in the ear, \ and part in what a listener has learnt", TUNE),
        ]
        rows_scene(self, r"how much is answered", items,
                   "How much is answered? <bookmark mark='b'/> The physics: at simple ratios the partials of harmonic tones "
                   "coincide, so those coinciding components do not beat against one another; other partial pairs can still contribute beating or roughness. That was Helmholtz's answer, and Part 5 measured it. "
                   "<bookmark mark='c'/> The ear: such a chord also looks to a pitch model like a single harmonic series, a single "
                   "source. <bookmark mark='d'/> The timbre: bend the partials, as Variation 5 did, and other intervals become "
                   "the smooth ones, so the ratios are good only for the sounds that have harmonic partials. "
                   "<bookmark mark='e'/> And the culture: in 2016 listeners in the Bolivian Amazon, who had heard little Western "
                   "music, heard roughness as others do but did not prefer consonant chords. <bookmark mark='f'/> So part of the "
                   "answer is in the sound, part in the ear, and part in what a listener has learnt. How the parts divide is "
                   "still open.", font_size=22, marks="bcdef")

    # ------------------------------------------------------------------
    def open_(self):
        d = load("fifths")
        items = [
            (r"how much of consonance, \ of key, \ of meter is learnt, \ and how fast, \ in how many cultures", WHITE),
            (r"what in the brain computes harmonicity and expectation, \ and why music moves people at all", WHITE),
            (r"why music exists: \ the theories of its origin are many, \ the evidence thin \ (Part 47)", WHITE),
            (r"machines that judge music as listeners do, \ and that are honest about what they were trained on", WHITE),
            (rf"and the {d['open_problems']} research problems this series posed, \ one per part, \ gathered in Part 67", TUNE),
        ]
        rows_scene(self, r"what is still open", items,
                   "And what else is still open? <bookmark mark='b'/> How much of consonance, of key and of meter is learnt, how "
                   "fast, and in how many cultures. <bookmark mark='c'/> What in the brain computes harmonicity and expectation, "
                   "and why music moves people at all. <bookmark mark='d'/> Why music exists: the theories of its origin are many "
                   "and the evidence thin. <bookmark mark='e'/> Machines that judge music as listeners do, and that are honest "
                   f"about what they learnt from. <bookmark mark='f'/> And the {say(d['open_problems'])} research problems this "
                   "series posed as questions, gathered in Part 67.", marks="bcdef")

    # ------------------------------------------------------------------
    def star(self):
        items = [
            (r"$\bigstar$ \ research problem: \ separate the ear's part from the culture's", EAR),
            (r"the same chords, \ with harmonic and with stretched partials, \ for listeners of many musical cultures and none", WHITE),
            (r"measure what each hears \ (roughness, \ fusion, \ pitch) \ apart from what each prefers", WHITE),
            (r"if roughness is heard everywhere and preference varies, \ the ratio's goodness is part sound and part learning", WHITE),
            (r"the tools are in this series: \ stretched partials \ (Part 5), \ listening tests and their power \ (Part 67)", TUNE),
        ]
        rows_scene(self, r"the last research problem", items,
                   "So the last research problem goes back to the first part. <bookmark mark='b'/> Separate the ear's part from "
                   "the culture's. Play the same chords, with harmonic partials and with stretched ones, to listeners of many "
                   "musical cultures, and to some who know little music at all. <bookmark mark='c'/> Measure what each hears, "
                   "the roughness, the fusion into one sound, the pitch, apart from what each prefers. <bookmark mark='d'/> If "
                   "roughness is heard everywhere and preference varies, the goodness of the ratio is part sound and part "
                   "learning, and the experiment helps compare perceptual and cultural contributions, without uniquely decomposing their causes. <bookmark mark='e'/> Every tool it needs is in this "
                   "series: stretched partials from Part 5, and listening tests with enough power from Part 67.", marks="bcde")
