from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from explainer.music.monochord import tune
from videos.music.music1.common import (BAD, EAR, GOOD, HIST, MASS, PART, RATIO, STR, TUNE, PairView, anvil_shape,
                                        clip, hammer, hung_lens, hung_string, load, ring, say, window)


class Hook(SoundScene):
    def construct(self):
        self.cold_open()
        self.legend()
        self.anvil()
        self.weights()
        self.monochord()
        self.plan()

    # ------------------------------------------------------------------
    def cold_open(self):
        c = clip("hammers.opening")
        mono = MonochordView(width=10.6).shift(UP * 1.0)
        slots = VGroup()
        for n, word in zip(c.notes, tune.WORDS):
            slots.add(VGroup(label(n["name"], font_size=44, color=GREY_C), label(word, font_size=26, color=GREY_D))
                      .arrange(DOWN, buff=0.14))
        slots.arrange(RIGHT, buff=0.62, aligned_edge=UP).next_to(mono, DOWN, buff=0.9)
        self.play(FadeIn(mono), FadeIn(slots), run_time=0.6)
        prev = None
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ on one string")
            for k, n in enumerate(c.notes):
                snd.wait_until(f"n{k}")
                if prev is not None:
                    self.remove(prev)
                mono.set_stop(n["stop"])
                prev = mono.lens(n["stop"], amp=0.2)
                self.add(prev)
                snd.drive(prev, ring(at=n["t"], rate=2.0))
                slots[k][0].set_color(TUNE)
                slots[k][1].set_color(GREY_A)
        self.remove(prev)
        fifth = VGroup(Line(slots[1][0].get_top() + UP * 0.12, slots[1][0].get_top() + UP * 0.38, color=RATIO),
                       Line(slots[1][0].get_top() + UP * 0.38, slots[2][0].get_top() + UP * 0.38, color=RATIO),
                       Line(slots[2][0].get_top() + UP * 0.38, slots[2][0].get_top() + UP * 0.12, color=RATIO))
        ftag = label(r"a fifth", font_size=30, color=RATIO).next_to(fifth, UP, buff=0.1)
        with self.voiceover(
            "You know this tune. Nearly everyone on Earth does. <bookmark mark='a'/> It starts by saying one note "
            "twice, and then it jumps. <bookmark mark='b'/> Musicians call that jump a fifth. It is the subject of "
            "the oldest experiment in science, and of a question that has been open for two and a half thousand "
            "years."
        ) as vo:
            vo.wait_until("a")
            self.play(Indicate(slots[0][0], color=TUNE), Indicate(slots[1][0], color=TUNE), run_time=1.0)
            vo.wait_until("b")
            self.play(Create(fifth), FadeIn(ftag, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def legend(self):
        d = load("hammers")
        yr = label(r"about 530 \textsc{bce}", font_size=44, color=HIST).to_corner(UL, buff=0.5)
        who = label(r"Pythagoras, \ at a blacksmith's door", font_size=30, color=GREY_A).next_to(yr, RIGHT, buff=0.4)
        anv = anvil_shape(2.4).move_to(LEFT * 4.6 + DOWN * 1.9)
        hams = VGroup(*[hammer(w) for w in d["weights"]]).arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        hams.move_to(LEFT * 4.3 + UP * 0.2)
        rows = VGroup()
        for (a, b), (p, q), name in (((12, 6), (2, 1), r"the octave"), ((12, 8), (3, 2), r"the fifth"),
                                     ((12, 9), (4, 3), r"the fourth")):
            rows.add(VGroup(MathTex(rf"{a} : {b}", font_size=44, color=MASS),
                            MathTex(r"=", font_size=44, color=GREY_B),
                            MathTex(rf"{p} : {q}", font_size=44, color=RATIO),
                            label(name, font_size=34, color=WHITE)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * 3.0 + UP * 0.3)
        with self.voiceover(
            "The story goes like this. Around 530 BC, Pythagoras walks past a blacksmith's shop and hears the hammers "
            "ringing in harmony. <bookmark mark='a'/> He goes in and weighs them: twelve, nine, eight and six. "
            "<bookmark mark='b'/> Twelve to six is two to one, and those two hammers sound an octave. "
            "<bookmark mark='c'/> Twelve to eight is three to two: the fifth. <bookmark mark='d'/> Twelve to nine is "
            "four to three: the fourth."
        ) as vo:
            for h in hams:
                h.num.set_opacity(0)
            self.play(FadeIn(yr), FadeIn(who), FadeIn(anv),
                      LaggedStart(*[FadeIn(h, shift=DOWN * 0.3) for h in hams], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[h.num.animate.set_opacity(1) for h in hams], lag_ratio=0.3), run_time=1.6)
            for mark, row, pair in zip("bcd", rows, ((0, 3), (0, 2), (0, 1))):
                vo.wait_until(mark)
                self.play(FadeIn(row, shift=LEFT * 0.2), Indicate(hams[pair[0]].head, color=TUNE),
                          Indicate(hams[pair[1]].head, color=TUNE), run_time=0.9)
        strings = VGroup(*[hung_string(w, width=2.4).scale(0.5) for w in d["weights"]])
        strings.arrange(RIGHT, buff=0.3).move_to(LEFT * 3.6 + DOWN * 1.5)
        src = history_card(r"c.\ 100 \textsc{ce}", r"Nicomachus, \ then Boethius (c.\ 510)",
                           r"the story as we have it, written six centuries after the event and copied into "
                           r"every music textbook for a thousand years", width=5.6).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Then, the story says, he went home, hung the same four weights on four strings, <bookmark mark='a'/> and "
            "heard the same harmonies again. Number rules the world. <bookmark mark='b'/> We have the story from "
            "Nicomachus, who wrote it down six hundred years later. Boethius copied it, and for a thousand years it "
            "opened every textbook on music."
        ) as vo:
            self.play(FadeOut(anv), hams.animate.scale(0.7).move_to(LEFT * 3.6 + UP * 1.7), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in strings], lag_ratio=0.2), run_time=1.4)
            vo.wait_until("b")
            self.play(rows.animate.scale(0.8).to_edge(UP, buff=1.5).shift(RIGHT * 0.2), FadeIn(src, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def anvil(self):
        d = load("hammers")
        false_ = label(r"It is false.", font_size=84, color=BAD)
        both = label(r"Both halves.", font_size=44, color=GREY_A).next_to(false_, DOWN, buff=0.4)
        with self.voiceover("It is false. <bookmark mark='a'/> Both halves of it.") as vo:
            self.play(FadeIn(false_, scale=1.3), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(both))
        self.clear_scene(run_time=0.6)
        anv = anvil_shape(3.0).move_to(DOWN * 1.7)
        hams = VGroup(*[hammer(w, 0.8) for w in d["weights"]]).arrange(RIGHT, buff=0.45, aligned_edge=DOWN)
        hams.next_to(anv, UP, buff=0.9)
        cap = label(r"the ring belongs to the anvil, \ not to the hammer", font_size=30, color=GREY_A).to_edge(UP, buff=0.7)
        with self.voiceover(
            "The hammers first. Strike one anvil with four hammers and the ring you hear belongs to the anvil. "
            "Change the hammer, and the notes do not move."
        ):
            self.play(FadeIn(anv), FadeIn(hams), FadeIn(cap))
            for k in range(4):
                home = hams[k].get_center()
                self.play(hams[k].animate.move_to(anv.get_top() + UP * 0.6 + LEFT * 0.4), run_time=0.25)
                self.play(hams[k].animate.move_to(home), run_time=0.35)
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def weights(self):
        d = load("hammers")
        oc = d["as_weights"]["octave"]
        c1, c2 = clip("hammers.weights"), clip("hammers.four")
        top = hung_string(6, width=6.4).move_to(LEFT * 2.2 + UP * 2.2)
        bot = hung_string(12, width=6.4).move_to(LEFT * 2.2 + DOWN * 0.4)
        claim = VGroup(label(r"the legend:", font_size=30, color=GREY_B),
                       MathTex(r"12 : 6 = 2 : 1", font_size=40, color=RATIO),
                       label(r"an octave", font_size=30)).arrange(DOWN, buff=0.2).move_to(RIGHT * 4.2 + UP * 1.6)
        with self.voiceover(
            "Now the strings. Hang six units of weight on one string and twelve on another just like it. "
            "<bookmark mark='a'/> The legend promises an octave. Listen."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot))
            vo.wait_until("a")
            self.play(FadeIn(claim))
        with self.listen(c1) as snd:
            window(snd, r"weight 6, \ then weight 12")
            la, lb = hung_lens(top), hung_lens(bot)
            snd.show(la, lb)
            snd.drive(la, ring(at=snd.time_of("w6"), rate=1.6, stop_at=snd.time_of("w12")))
            snd.drive(lb, ring(at=snd.time_of("w12"), rate=1.6))
        verdict = VGroup(
            label(r"measured on our string:", font_size=28, color=GREY_B),
            label(rf"{oc['measured_cents']:.0f} cents", font_size=44, color=BAD),
            label(r"half an octave", font_size=30, color=BAD),
            MathTex(r"\text{pitch} \propto \sqrt{\text{weight}}", font_size=36, color=GREY_A),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 4.2 + DOWN * 1.5)
        cross = Cross(claim, stroke_color=BAD, stroke_width=5)
        with self.voiceover(
            f"That is no octave. An octave is twelve hundred cents wide, and our string, simulated, moved "
            f"{say(oc['measured_cents'])}. <bookmark mark='a'/> Exactly half an octave, the most awkward interval "
            "there is. <bookmark mark='b'/> Doubling the weight multiplies the pitch by the square root of two."
        ) as vo:
            self.play(Create(cross), FadeIn(verdict[:2]))
            vo.wait_until("a")
            self.play(FadeIn(verdict[2]))
            vo.wait_until("b")
            self.play(FadeIn(verdict[3]))
        new = hung_string(24, width=6.4).move_to(bot)
        card = history_card(1589, r"Vincenzo Galilei", r"lutenist, and father of Galileo: he hung the weights, and "
                            r"found that an octave needs four to one, a fifth nine to four, a fourth sixteen to nine",
                            width=5.4).to_corner(DR, buff=0.35)
        with self.voiceover(
            "Someone finally hung the weights. In the fifteen-eighties a lute player called Vincenzo Galilei tried "
            "it, <bookmark mark='a'/> and found that an octave takes four times the weight, not twice. "
            "<bookmark mark='b'/> His son Galileo was in his twenties, and watching."
        ) as vo:
            self.play(FadeOut(claim), FadeOut(cross), FadeOut(verdict), FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(ReplacementTransform(bot, new))
            vo.wait_until("b")
        with self.listen(c2) as snd:
            window(snd, r"weight 6, \ then weight 24")
            la, lb = hung_lens(top), hung_lens(new)
            snd.show(la, lb)
            snd.drive(la, ring(at=snd.time_of("w6"), rate=1.6, stop_at=snd.time_of("w24")))
            snd.drive(lb, ring(at=snd.time_of("w24"), rate=1.6))
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def monochord(self):
        c = clip("ratios.octave")
        pair = PairView(0.5).shift(UP * 0.9)
        half = pair.bottom.mark(0.5, r"\tfrac{1}{2}", font_size=36)
        name = label(r"the monochord: \ one string, \ a movable bridge", font_size=32, color=STR).to_edge(UP, buff=0.4)
        with self.voiceover(
            "One part of the story is true, and it is the part with an instrument in it. This is a monochord: a "
            "single string over a box, with a bridge you can slide. <bookmark mark='a'/> Stop the string at half its "
            "length, and this happens."
        ) as vo:
            self.play(FadeIn(name), FadeIn(pair.top))
            vo.wait_until("a")
            self.play(FadeIn(pair.bottom), FadeIn(half))
        with self.listen(c) as snd:
            window(snd, r"whole string, \ half, \ both")
            pair.play(self, snd)
        q1 = label(r"Why does a string have a pitch at all?", font_size=38, color=TUNE)
        q2 = label(r"Why do $2:1$ and $3:2$ sound good together?", font_size=38, color=EAR)
        qs = VGroup(q1, q2).arrange(DOWN, buff=0.4).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "An octave: the same note, higher. So the numbers are real. It was the explanation that stood on nothing "
            "for two thousand years. <bookmark mark='a'/> Why does a string have a pitch at all? "
            "<bookmark mark='b'/> And why should two to one, or three to two, sound good together? The first "
            "question we will answer today, completely. The second got its first real answer in the nineteenth "
            "century, and people are still arguing about it. This series follows that argument."
        ) as vo:
            self.play(FadeOut(half))
            vo.wait_until("a")
            self.play(FadeIn(q1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(q2, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ One String", font_size=46).to_edge(UP, buff=0.35)
        smap = series_map(current=PART, height=6.3).next_to(title, DOWN, buff=0.3)
        obj = objectives_card([
            r"the monochord: \ four numbers, \ three intervals",
            r"what sets the pitch: \ length, \ tension and mass (Mersenne's laws), \ tested on a simulated string",
            r"the wave equation, \ derived from Newton's law on one small piece of string",
            r"two pictures of one motion: \ travelling waves (d'Alembert) and standing waves (Bernoulli)",
            r"the plucked string: \ which harmonics it has, \ and why one string is already a chord",
            r"a first answer to why the ratios sound good, \ and what real strings do that the ideal one does not",
        ], font_size=26).move_to(DOWN * 0.25)
        with self.voiceover(
            "This is Part 1 of Music, Built: sixty-eight lectures that start with one string and end with an "
            "orchestra, a recording studio, and machines that listen and compose. Everything you hear in this series "
            "is made by the code we write along the way. <bookmark mark='a'/> In this part: the monochord. What sets "
            "the pitch of a string. The wave equation, from Newton's law. Travelling waves, standing waves, and the "
            "quarrel between them. Why one string is already a chord. And a first answer to Pythagoras."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
