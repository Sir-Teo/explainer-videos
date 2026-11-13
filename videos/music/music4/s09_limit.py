from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403


class Limit(SoundScene):
    def construct(self):
        chapter(self, 8, r"Where pitch stops", r"Is there a highest note?", lit=(1863,), extra=((1971, r"Attneave and Olson"),))
        self.tune()
        self.curve()

    # ------------------------------------------------------------------
    def tune(self):
        d = load("limit")
        c = clip("limit.tune")
        notes = d["normal_notes"]
        q = listen_note(r"The opening of the Tune, \ in pure tones, \ twice. \\ The second time it is more than three octaves higher. \ Is it still a tune?",
                        width=10.0).to_edge(UP, buff=0.4)
        g = faxes(300, 12000, [0, 1], x_length=10.0, y_length=1.0, ylabel="", yticks=[], fticks=(500, 1000, 2000, 4000, 8000), font_size=20)
        g.move_to(DOWN * 1.0)
        ratio = d["high_hz"] / d["normal_hz"]
        low = VGroup(*[Dot(g.at(n["hz"], 0.45), radius=0.1, color=TUNE).set_opacity(0.25) for n in notes])
        high = VGroup(*[Dot(g.at(n["hz"] * ratio, 0.45), radius=0.1, color=BAD).set_opacity(0.25) for n in notes])
        names = VGroup(*[label(n["name"], font_size=36, color=GREY_D) for n in notes]).arrange(RIGHT, buff=0.6).move_to(UP * 0.75)
        with self.voiceover(
            "If pitch depends on the timing of the nerve, and the timing fails above a few thousand hertz, then "
            "something should happen to music up there. Here is the opening of the Tune in pure tones, starting "
            "an octave above middle C. Then the same phrase again, more than three octaves higher, where every "
            "note is above five thousand hertz. Is the second one still a tune?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(g), FadeIn(low), FadeIn(high), FadeIn(names))
        with self.listen(c) as snd:
            window(snd, r"the Tune's opening, \ then the same above 5000 Hz", kind="synthesized", detail=r"pure tones; \ the second is high and thin", corner=DL, tag_corner=DR)
            for tag, dots in (("normal", low), ("high", high)):
                for k, nt in enumerate(notes):
                    t0 = snd.time_of(f"{tag}.n{k}")
                    t1 = t0 + nt["dur"]
                    snd.drive(dots[k], lambda m, t, t0=t0, t1=t1: m.set_opacity(1.0 if t0 <= t < t1 else 0.25).scale_to_fit_width(0.34 if t0 <= t < t1 else 0.2))
                    snd.drive(names[k], lambda m, t, t0=t0, t1=t1, col=(TUNE if tag == "normal" else BAD), prev=names[k]: m.set_color(col) if t0 <= t < t1 else m)
        for m in list(low) + list(high):
            m.set_opacity(0.6).scale_to_fit_width(0.2)
        names.set_color(GREY_D)
        card = history_card(1971, r"Fred Attneave and Richard Olson",
                            r"ask listeners to transpose a familiar jingle. Below about 5000 Hz they do it easily. "
                            r"Above, the melody falls apart.", width=6.0).move_to(DOWN * 2.6 + LEFT * 2.9)
        ans = label(r"above 5 kHz: \ higher and lower, \\ but no intervals, \ no tune", font_size=28, color=BAD).move_to(DOWN * 2.6 + RIGHT * 3.6)
        with self.voiceover(
            "For most people it is not. You can tell that the high tones move, and roughly whether they go up "
            "or down. But the intervals are gone. It no longer sounds like notes; it sounds like the squeaks of "
            "a hinge. <bookmark mark='a'/> In 1971 Fred Attneave and Richard Olson measured this. They asked "
            "listeners to transpose a jingle they knew well. Up to about five thousand hertz, people did it "
            "easily. Above that, their answers scattered. The sense of musical pitch, the thing that makes an "
            "octave an octave, has an upper edge."
        ) as vo:
            self.play(FadeOut(q), VGroup(g, low, high, names).animate.shift(UP * 1.6))
            self.play(FadeIn(ans))
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("limit")
        rows = d["salience"]
        g = faxes(20, 20000, [0, 1.1], x_length=10.4, y_length=3.0, ylabel=r"how strongly the timing model hears a pitch in a pure tone", yticks=[0, 0.5, 1],
                  fticks=(27.5, 100, 1000, 4186, 20000), font_size=20)
        g.move_to(UP * 0.7)
        cu = fcurve(g, [r["hz"] for r in rows], [r["salience"] for r in rows], EAR)
        dots = VGroup(*[Dot(g.at(r["hz"], r["salience"]), radius=0.07, color=EAR) for r in rows])
        piano = Rectangle(width=g.at(d["piano_top_hz"], 0)[0] - g.at(27.5, 0)[0], height=0.32, stroke_width=0, fill_color=STR, fill_opacity=0.6)
        piano.move_to((g.at(27.5, 0) + g.at(d["piano_top_hz"], 0)) / 2 + DOWN * 1.15)
        pl = label(r"the piano's 88 fundamentals", font_size=22, color=STR).next_to(piano, DOWN, buff=0.12)
        hear = Rectangle(width=g.at(20000, 0)[0] - g.at(20, 0)[0], height=0.32, stroke_width=0, fill_color=AIR, fill_opacity=0.35)
        hear.move_to((g.at(20, 0) + g.at(20000, 0)) / 2 + DOWN * 2.15)
        hl = label(r"what you can hear", font_size=22, color=AIR).next_to(hear, DOWN, buff=0.12)
        top = DashedLine(g.at(d["piano_top_hz"], 1.05), g.at(d["piano_top_hz"], 0) + DOWN * 2.3, color=GREY_B, stroke_width=1.5)
        only = label(r"partials only: \\ brightness, \ not notes", font_size=22, color=GREY_A).move_to(g.at(9500, 0.62))
        r = {int(x["hz"]): x["salience"] for x in rows}
        with self.voiceover(
            "Monochord's timing model agrees. Give it pure tones and ask how strongly it hears a pitch. "
            f"<bookmark mark='a'/> At two hundred and fifty hertz, {say(r[250], 2)}. At a thousand, "
            f"{say(r[1000], 2)}. At four thousand, {say(r[4000], 2)}: almost nothing. <bookmark mark='b'/> Now "
            "lay the piano underneath. Its lowest note is twenty-seven and a half hertz. Its highest, the top C, "
            f"is {say(d['piano_top_hz'])}. <bookmark mark='c'/> Instrument makers had never heard of nerve "
            "fibres. They stopped where notes stop. The piccolo ends in the same place, and so does every other "
            "instrument that plays melodies. <bookmark mark='d'/> But hearing runs on for more than two octaves "
            "beyond that. What lives up there is not notes. It is the upper partials of notes: the brightness "
            "of a cymbal, the breath on a flute, the consonants in a voice. The place code still works there, "
            "so you can hear that the sound is high. Only the clock can tell you what note it is."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cu), FadeIn(dots), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(piano), FadeIn(pl))
            vo.wait_until("c")
            self.play(Create(top))
            vo.wait_until("d")
            self.play(FadeIn(hear), FadeIn(hl), FadeIn(only))
        self.wait(0.3)
        self.clear_scene()
