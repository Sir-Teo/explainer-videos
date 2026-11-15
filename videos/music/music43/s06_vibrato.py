from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403


class Vibrato(SoundScene):
    def construct(self):
        chapter(self, 5, r"Vibrato and intonation", r"If the pitch keeps moving, \ which pitch do we hear?")
        self.quiz()
        self.rates()
        self.facts()
        self.intonation()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("vibrato")
        c = clip("vibrato.quiz")
        card = listen_card(r"A plain note, \ then a note with a wide vibrato. \ "
                           r"Is the second higher, \ lower, \ or the same pitch?", width=10.4)
        with self.voiceover(
            "A question for your ears. A plain note, and then a note with a wide vibrato, its pitch swinging up and down. Is "
            "the second higher than the first, lower, or the same?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        t = np.array(d["trace_t"])
        cts = np.array(d["trace_cents"])
        x0, W, y0, H = -5.0, 10.0, 0.4, 1.4
        ax = DashedLine([x0, y0, 0], [x0 + W, y0, 0], color=GREY_B)
        trace = VMobject(color=EAR, stroke_width=3).set_points_as_corners([[x0 + W * ti / t[-1], y0 + H * ci / 80, 0] for ti, ci in zip(t, cts)])
        labs = VGroup(label(r"A4, \ 440 Hz", font_size=16, color=GREY_A).next_to(ax, LEFT, buff=0.15),
                      label(r"+60 cents", font_size=14, color=GREY_A).move_to([x0 - 0.6, y0 + H * 60 / 80, 0]),
                      label(r"$-$60 cents", font_size=14, color=GREY_A).move_to([x0 - 0.6, y0 - H * 60 / 80, 0]))
        head = label(r"the second note's pitch, \ moment by moment", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        trace.set_opacity(0)
        self.play(FadeOut(card), FadeIn(head), FadeIn(ax), FadeIn(labs))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"plain, \ then vibrato", kind="synthesized", detail=r"additive, \ bowed-string spectrum", corner=DL, tag_corner=DR)
            snd.drive(trace, lambda m, now: m.set_stroke(opacity=1.0 if now >= st["vibrato"] else 0.0))
            snd.show(trace)
            plain = label(r"first: \ the plain note", font_size=20, color=EAR).next_to(head, DOWN, buff=0.3)
            snd.show(plain)
            snd.drive(plain, lambda m, now: m.set_opacity(1.0 if now < st["vibrato"] else 0.0))
            pulse(snd, plain, st["plain"], st["vibrato"] - 0.1, buff=0.08)
        trace.set_stroke(opacity=1.0)
        self.add(trace)
        ans = label(rf"the same: \ the pitch heard is the mean, \ {d['mean_hz']:.1f} Hz, \ though it is there only in passing", font_size=20, color=TUNE).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The same. The vibrato swings sixty cents either side of 440 hertz, more than half a semitone, five and a half "
            f"times a second, and its average is {say(d['mean_hz'], 1)} hertz. Listeners hear a vibrato note at about its "
            "average pitch, as Shonle and Horan found in 1980, even though the sound passes through that pitch only "
            "for an instant in each swing."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rates(self):
        d = load("rates")
        c = clip("rates.three")
        cells = VGroup()
        for r in d["rates"]:
            t = np.linspace(0, 1.0, 300)
            y = np.sin(2 * np.pi * r * t)
            w = VMobject(color=TUNE, stroke_width=3).set_points_as_corners([[3.0 * ti, 0.5 * yi, 0] for ti, yi in zip(t, y)])
            name = {3.0: r"3 Hz: \ a wobble", 6.0: r"6 Hz: \ vibrato", 10.0: r"10 Hz: \ a tremble"}[r]
            cells.add(VGroup(label(name, font_size=20, color=WHITE), w).arrange(DOWN, buff=0.3))
        cells.arrange(RIGHT, buff=0.9).move_to(UP * 0.3)
        cap = label(r"the same 40-cent swing at three rates; \ one second of each pitch track", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Rate matters as much as width. Hear the same swing of forty cents at three, six and ten times a second."
        ):
            self.play(FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three rates", kind="synthesized", detail=r"additive, \ bowed-string spectrum", corner=DL, tag_corner=DR)
            for i, k in enumerate(("3", "6", "10")):
                pulse(snd, cells[i], st[k], st[k] + 1.8, buff=0.1)
        with self.voiceover(
            "At three it sounds like a wobble in pitch; at ten, a nervous tremble; around five to seven, it fuses into one "
            "warm, living tone. That is where singers and string players put it."
        ):
            self.play(Indicate(cells[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def facts(self):
        items = [
            (r"singers' vibrato: \ about 5.5 to 7 swings a second, \ typically 0.5 to 2 semitones from top to bottom", WHITE),
            (r"Seashore's films \ (1930s) \ found it in nearly every good singer's tone", WHITE),
            (r"string players make it with the finger rocking on the string; \ wind players with breath or lip", WHITE),
            (r"it is a style as well as a sound: \ continuous vibrato in orchestras became standard only in the 20th century", TUNE),
            (r"the period-performance movement \ (Part 25) \ plays most earlier music with less", GREY_A),
        ]
        rows_scene(self, r"vibrato in practice", items,
                   "Some facts. <bookmark mark='b'/> Singers' vibrato runs at about five and a half to seven swings a second, "
                   "typically half a semitone to two semitones from top to bottom. <bookmark mark='c'/> Seashore's films of the "
                   "1930s found it in nearly every good singer's tone. <bookmark mark='d'/> String players make it by rocking a "
                   "finger on the string; wind players with the breath or the lip. <bookmark mark='e'/> It is also a style: "
                   "continuous vibrato in orchestral strings became standard only in the twentieth century, "
                   "<bookmark mark='f'/> and the period-performance movement of Part 25 plays most earlier music with less.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def intonation(self):
        items = [
            (r"players who can bend pitch do not play equal temperament \ (Part 6)", WHITE),
            (r"string players and singers raise leading tones and sharpen major thirds in melodies", WHITE),
            (r"in chords they lean towards pure intervals: \ barbershop quartets tune dominant sevenths near 7:4", WHITE),
            (r"intonation in practice is a compromise between melody's pull and harmony's purity, \ note by note", TUNE),
            (r"chapter 6: \ two players keeping time together", GREY_A),
        ]
        rows_scene(self, r"intonation in practice", items,
                   "Players who can bend pitch also choose it. <bookmark mark='b'/> They do not play equal temperament, Part 6's "
                   "compromise. <bookmark mark='c'/> String players and singers raise leading tones and sharpen major thirds in "
                   "melodies, <bookmark mark='d'/> and in sustained chords lean towards pure intervals: barbershop quartets tune "
                   "the dominant seventh near the ratio seven to four. <bookmark mark='e'/> Intonation in practice is a "
                   "compromise between melody's pull and harmony's purity, decided note by note. <bookmark mark='f'/> Chapter six "
                   "turns to two players keeping time together.", marks="bcdef")
