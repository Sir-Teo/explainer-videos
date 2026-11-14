from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403


class Machaut(SoundScene):
    def construct(self):
        chapter(self, 10, r"Machaut and the cadence", r"How did a phrase end, before tonality?", extra=((1365, r"\textit{Messe de Nostre Dame}"),))
        self.life()
        self.quiz()
        self.counted()

    # ------------------------------------------------------------------
    def life(self):
        items = [
            (r"Guillaume de Machaut, \ about 1300--1377: \ poet first, \ composer second, \ canon of Reims", WHITE),
            (r"he had his complete works copied, \ in order, \ in great books: \ an author's \textit{œuvre}", WHITE),
            (r"the \textit{Messe de Nostre Dame}: \ the oldest complete polyphonic Mass by one known composer", TUNE),
            (r"\textit{Ma fin est mon commencement}: \ one voice is another sung backwards \ (Part 20's crab)", WHITE),
            (r"songs in fixed forms: \ ballade, \ rondeau, \ virelai: \ the poem's form is the music's", GREY_A),
        ]
        rows_scene(self, r"the poet who composed", items,
                   "The greatest figure of the new art was a poet. <bookmark mark='b'/> Guillaume de Machaut, born around "
                   "1300, served the King of Bohemia as a secretary and spent his last decades as a canon of Reims "
                   "cathedral, and he did something no composer had done before: he had his complete works, poems and "
                   "music, copied in order into large, beautiful books, as an author's collected works. "
                   "<bookmark mark='c'/> Among them is the Messe de Nostre Dame, from the 1360s, the oldest complete "
                   "polyphonic setting of the Mass by a single known composer. <bookmark mark='d'/> Another is a rondeau "
                   "whose text says my end is my beginning, and means it: one voice is another sung backwards, Part 20's "
                   "crab, and a third turns round on itself halfway. <bookmark mark='e'/> Most of his music is songs in "
                   "fixed poetic forms, the ballade, the rondeau and the virelai, in which the form of the poem is the "
                   "form of the music.")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("cadence")
        c = clip("cadence.double")
        card = listen_card(r"Two cadences to D, \ three voices. \ In one, \ the upper voices step up a whole tone; \ in the other, \ "
                           r"both are raised so they step up a semitone. \ Which one pulls harder into D, \ A or B?", width=10.6)
        with self.voiceover(
            "How did a phrase end, before there were major and minor keys? Listen to two cadences to D in three voices. "
            "In one, the upper voices rise a whole tone into the final chord; in the other, both have been raised so "
            "that they rise only a semitone. Which pulls harder into D, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll(d["A"], width=3.6, height=2.6, colors=[TUNE, BLUE, GREY_A], lo=60, hi=76, bar_h=0.16).move_to(LEFT * 3.2 + DOWN * 0.2)
        gB = voices_roll(d["B"], width=3.6, height=2.6, colors=[TUNE, BLUE, GREY_A], lo=60, hi=76, bar_h=0.16).move_to(RIGHT * 3.2 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.35)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.35)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        u = d["unit"]
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"three synthetic voices", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, d["A"], d["starts"]["A"], u, colors=[TUNE, BLUE, GREY_A])
            flash_voices(snd, gB, d["B"], d["starts"]["B"], u, colors=[TUNE, BLUE, GREY_A])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"C and G: \ whole tones up", font_size=22, color=GREY_A).next_to(gA, DOWN, buff=0.35),
                     label(r"C$\sharp$ and G$\sharp$: \ two leading tones", font_size=22, color=TUNE).next_to(gB, DOWN, buff=0.35))
        cap = label(r"a major sixth opens to an octave, \ a third to a fifth: \ the double leading-tone cadence", font_size=22, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "B, for most listeners: two voices each a semitone from their goal. The outer voices move from a major sixth, "
            "E and C sharp, out to an octave on D, while the middle voice rises a semitone to the fifth. This is the "
            "double leading-tone cadence, the standard ending of fourteenth-century music. Its goal is not a chord with "
            "a third but a bare fifth and octave, and the pull comes entirely from voices moving by the smallest step."
        ):
            self.play(FadeIn(ans), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counted(self):
        d = load("census")
        cd = d["cadences"]
        bars = columns([cd["sixth_octave"], cd["leading_tone"], cd["double"]], [r"sixth to octave", r"upper voice by a semitone", r"and a second by a semitone"],
                       width=7.0, height=2.8, color=TUNE, fmt="{:.0f}", font_size=20)
        bars.move_to(LEFT * 2.4 + DOWN * 0.3)
        t = label(rf"in {d['pieces']} pieces of the fourteenth century", font_size=21, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(label(rf"{100 * cd['leading_tone'] / cd['sixth_octave']:.0f} in 100 sixth-to-octave cadences rise by a semitone", font_size=21, color=WHITE),
                      label(rf"{cd['double']}: \ the double leading tone, \ in pieces of three or more voices", font_size=21, color=TUNE),
                      label(r"many of those semitones are not in the manuscripts: \ chapter 13", font_size=21, color=EAR)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.4))
        side.move_to(RIGHT * 3.9 + DOWN * 0.2)
        with self.voiceover(
            f"How common was it? The film's corpus holds {say(d['pieces'])} pieces of fourteenth-century polyphony, "
            "transcribed in the modern edition Polyphonic Music of the Fourteenth Century: Mass movements, motets and "
            "Italian songs. A program finds every place where two voices move from a major sixth to an octave by "
            f"contrary steps. <bookmark mark='a'/> There are {say(cd['sixth_octave'])}. In {say(round(100 * cd['leading_tone'] / cd['sixth_octave']))} "
            f"in a hundred the upper voice rises by a semitone, <bookmark mark='b'/> and {say(cd['double'])} add a second "
            "voice rising a semitone to the fifth, the full double leading tone. <bookmark mark='c'/> But hold on to one "
            "fact for later: many of those semitones are sharps that the manuscripts do not write. The editors put them "
            "in, following rules the singers knew, and chapter thirteen asks how far we can trust that."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
