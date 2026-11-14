from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class Rhythm(SoundScene):
    def construct(self):
        chapter(self, 5, r"When chords change", r"Where in the bar does harmony move?")
        self.where()
        self.cadence()

    def cadence(self):
        d = load("rhythm")
        ch = columns([100 * d["elsewhere"], 100 * d["near_cadence"]], [r"elsewhere", r"the two beats \\ before a fermata"], width=4.6, height=2.6, color=WEAK, hot=(1,), hot_color=TUNE, fmt="{:.0f}", font_size=22, top=100).move_to(LEFT * 2.4 + DOWN * 0.6)
        t = label(r"a new chord on the next beat, \ in a hundred", font_size=22, color=GREY_A).next_to(ch, UP, buff=0.4)
        side = VGroup(label(r"harmony speeds up into a cadence", font_size=26, color=TUNE),
                      label(r"one chord a beat: \ ii, \ V, \ I, \ with no repeats", font_size=24, color=WHITE),
                      label(r"the ear hears the end coming", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.6 + DOWN * 0.3)
        head = label(r"harmonic rhythm at the end of a phrase", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Harmonic rhythm also changes within a phrase. <bookmark mark='a'/> Over the whole of the chorales, a beat "
            f"brings a new chord {say(round(100 * d['elsewhere']))} times in a hundred. In the two beats before a "
            f"fermata, {say(round(100 * d['near_cadence']))}. <bookmark mark='b'/> Approaching a cadence, Bach changes "
            "chord on almost every beat, two to five to one, rarely holding a chord over: the harmony speeds up into the end, "
            "and a listener can feel the close coming before it arrives, even without knowing the tune."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(t))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def where(self):
        d = load("rhythm")
        vals = [100 * x for x in d["change"]]
        ch = columns(vals, [r"beat 1", r"beat 2", r"beat 3", r"beat 4"], width=6.4, height=2.8, color=WEAK, hot=(0, 2), hot_color=TUNE, fmt="{:.0f}", font_size=24, top=100).move_to(LEFT * 2.6 + DOWN * 0.6)
        t = label(r"a new chord on the beat, \ in a hundred \ (chorales in four)", font_size=24, color=GREY_A).next_to(ch, UP, buff=0.4)
        side = VGroup(label(r"strong beats: \ new harmony", font_size=26, color=TUNE),
                      label(r"weak beats: \ more often the same chord, \ the voices moving inside it", font_size=24, color=WHITE),
                      label(r"harmonic rhythm: \ the pace of chord change, \ against the pace of the notes", font_size=24, color=GREY_A),
                      label(r"Part 11: \ the beats that are felt strongest", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.6))
        side.move_to(RIGHT * 3.8 + DOWN * 0.2)
        head = label(r"harmonic rhythm", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Chords also have a rhythm. In a chorale nearly every beat has a chord, but not always a new one. "
            "<bookmark mark='a'/> Count, for each beat of the bar, how often the chord there differs from the "
            f"one before. On the first beat, {say(round(vals[0]))} times in a hundred; on the third, "
            f"{say(round(vals[2]))}; on the weak second and fourth beats, {say(round(vals[1]))} and "
            f"{say(round(vals[3]))}. <bookmark mark='b'/> New harmony lands where Part 11 found the strongest "
            "beats, and the weak beats more often keep the chord while the voices move inside it. The pace "
            "of chord change is called harmonic rhythm, and composers set it against the rhythm of the notes: "
            "quick notes over slow harmony, as in these chorales, or the other way round."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(t))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
