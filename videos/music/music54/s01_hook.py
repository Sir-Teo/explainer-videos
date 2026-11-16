from __future__ import annotations

import numpy as np

from videos.music.music54.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.reveal()
        self.story()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"The Tune's first phrase, \ sung twice. \ Flat reference response, \ then a simulated dynamic headphone "
                           r"used as a microphone. \ Which was the headphone model?", width=10.0)
        with self.voiceover(
            "A question for your ears. The Tune's first phrase, sung twice. Once through a flat reference response. Once through a simulated dynamic headphone used as a microphone. Which was the headphones?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one voice, \ two pickups", kind="physical model", detail=r"Part 8's voice", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reveal(self):
        d = load("hook")
        f = np.array(d["f"])
        ax = logf_axes(width=9.0, height=3.2, flo=20, fhi=20000, ylo=-40, yhi=35, center=DOWN * 0.3)
        cv = curve(f, np.clip(d["H"], -40, 35), ax.to, color=EAR, width=3)
        flat = DashedLine(ax.to(20, 0), ax.to(20000, 0), color=TUNE, stroke_width=2)
        key = VGroup(label(r"measurement microphone: \ flat", font_size=17, color=TUNE), label(r"headphone driver, \ run backwards", font_size=17, color=EAR)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)
        yl = label(r"dB re 1 kHz", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.15)
        note = label(rf"above the driver's resonance \ ({d['hp']['fs']:.0f} Hz) \ the moving mass rules: \ 6 dB less for every octave up", font_size=18, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"the second was the headphones", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The second: dull, boomy, but unmistakably the voice. <bookmark mark='a'/> A headphone driver is a coil on a "
            "diaphragm in a magnet's field. Push the diaphragm with sound and the coil, moving through the field, makes a "
            "voltage. <bookmark mark='b'/> But above its resonance the diaphragm's mass resists being pushed, more at every "
            "octave, so the highs fall away six decibels an octave. A loudspeaker is a microphone run backwards, and this part "
            "is about both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yl), FadeIn(flat), FadeIn(key[0]), FadeIn(ghost(cv, 0.3)))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"before 1925, \ recording was acoustic: \ singers bellowed into a horn that cut a groove by sheer pressure", WHITE),
            (r"1925: \ electrical recording, \ with Bell Labs' condenser microphone \ (Wente, \ 1916) \ and an amplifier", WHITE),
            (r"the microphone heard a soft voice close to it as well as a loud one far away", WHITE),
            (r"crooners \ (Bing Crosby above all) \ sang quietly and intimately, \ to a microphone, \ for millions", TUNE),
            (r"a transducer changed what a voice could be", GREY_A),
        ]
        rows_scene(self, r"the voice the microphone made", items,
                   "The microphone changed singing. <bookmark mark='b'/> Before 1925 recording was acoustic: singers bellowed into a "
                   "horn whose diaphragm cut a groove by sheer pressure. <bookmark mark='c'/> In 1925 major record companies introduced commercial electrical recording, with "
                   "the condenser microphone Edward Wente had built at Bell Labs in 1916, and an amplifier. <bookmark mark='d'/> The "
                   "microphone heard a soft voice close to it as well as a loud one far away, <bookmark mark='e'/> and the crooners, "
                   "Bing Crosby above all, sang quietly and intimately, to a microphone, for millions. <bookmark mark='f'/> A "
                   "transducer changed what a voice could be.", marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"transducers, \ and electrical, \ mechanical and acoustical circuits",
            r"polar patterns, \ the proximity effect, \ noise and balanced lines",
            r"the loudspeaker as a filter: \ Thiele--Small parameters",
            r"sealed and vented boxes, \ checked against their closed forms",
            r"horns, \ crossovers, \ amplifiers",
            r"headphones, \ noise cancelling, \ arrays",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Transducers, and the circuits that describe them. <bookmark mark='b'/> Polar patterns, the "
            "proximity effect, noise and balanced lines. <bookmark mark='c'/> The loudspeaker as a filter, and its Thiele-Small "
            "parameters. <bookmark mark='d'/> Sealed and vented boxes, simulated and checked against their closed forms. "
            "<bookmark mark='e'/> Horns, crossovers and amplifiers. <bookmark mark='f'/> And headphones, noise cancelling and "
            "arrays."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
