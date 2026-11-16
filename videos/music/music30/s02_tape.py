from __future__ import annotations

import numpy as np

from videos.music.music30.common import *  # noqa: F403

ORDER = ["cut", "reversed", "bell", "half"]
NAME = {"cut": r"attack cut off", "reversed": r"reversed", "bell": r"untouched", "half": r"half speed"}


class Tape(SoundScene):
    def construct(self):
        chapter(self, 1, r"Music from recordings", r"What is left of a bell without its strike?", extra=((1951, r"the Paris studio's tape machines"),))
        self.machine()
        self.speeds()
        self.quiz()
        self.objects()
        self.tapes()
        self.lucier()

    # ------------------------------------------------------------------
    def machine(self):
        items = [
            (r"from 1951, \ magnetic tape: \ cut with a razor blade, \ spliced, \ looped", WHITE),
            (r"speed: \ twice as fast is an octave higher and half as long \ (Part 2)", WHITE),
            (r"reversal: \ the decay comes first, \ the attack last", WHITE),
            (r"the attack cut off: \ the first fraction of a second removed", TUNE),
            (r"filtering, \ echo, \ layering: \ the studio as an instrument", GREY_A),
        ]
        rows_scene(self, r"what a tape machine does", items,
                   "Discs gave way to magnetic tape. <bookmark mark='b'/> From 1951 the Paris studio could cut tape with a "
                   "razor blade, splice it and loop it. <bookmark mark='c'/> Played twice as fast, a sound goes up an octave and "
                   "lasts half as long, as Part 2's waves predicted. <bookmark mark='d'/> Played backwards, its decay comes "
                   "first and its attack last. <bookmark mark='e'/> And its attack can simply be cut away. "
                   "<bookmark mark='f'/> With filters, echo and layering, the studio itself became an instrument.", marks="cdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("tape")
        c = clip("tape.four")
        card = listen_card(r"A bell from Part 9, \ four ways: \ untouched, \ played backwards, \ at half speed, \ and with its first quarter-second cut off, \ "
                           r"in some order. \ Which is the untouched bell: \ A, \ B, \ C or D?", width=10.6)
        with self.voiceover(
            "A question for your ears. A bell from Part 9, four ways: untouched, played backwards, at half speed, and with "
            "its first quarter of a second cut away, in some order. Which one is the bell as it was struck? Listen to how "
            "each one begins."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        cells = VGroup()
        for k, letter in zip(ORDER, "ABCD"):
            cells.add(VGroup(label(letter, font_size=34, color=GREY_A), envelope_curve(d["env"][k], width=2.6, height=1.3, color=GREY_A)).arrange(DOWN, buff=0.3))
        cells.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.1)
        self.play(FadeOut(card), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C, \ D", detail=r"Part 9's bell", corner=DL, tag_corner=DR)
            for i, k in enumerate(ORDER):
                end = d["starts"][ORDER[i + 1]] - 0.4 if i < 3 else c.duration
                pulse(snd, cells[i][0], d["starts"][k], end, buff=0.08)
        ans = VGroup(*[label(NAME[k], font_size=19, color=TUNE if k == "bell" else GREY_A).next_to(cells[i], DOWN, buff=0.3) for i, k in enumerate(ORDER)])
        with self.voiceover(
            "C is the untouched bell: a sharp strike, then a long ringing decay. B is the same sound backwards, swelling to "
            "a sudden stop. D is an octave lower and twice as long. And A, the one with its strike removed, is the "
            "surprise: without its first quarter-second the bell’s attack cue is weakened, though its remaining spectrum can still suggest a bell. Schaeffer found that "
            "the attack carries much of what tells us what made a sound."
        ):
            self.play(FadeIn(ans), cells[2][1].animate.set_color(TUNE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def objects(self):
        items = [
            (r"Schaeffer's `sound object': \ a sound heard for itself, \ apart from its cause", WHITE),
            (r"`reduced listening': \ attend to shape, \ grain, \ mass, \ not to `a door' or `a bell'", WHITE),
            (r"\textit{Treatise on Musical Objects} \ (1966): \ a taxonomy of sounds by how they behave", WHITE),
            (r"the cut attack showed it: \ identity lives in the first moments \ (Part 4's ear)", TUNE),
            (r"Pierre Henry, \ Éliane Radigue, \ the GRM: \ a tradition that continues", GREY_A),
        ]
        rows_scene(self, r"the sound object", items,
                   "From such experiments Schaeffer built a theory. <bookmark mark='b'/> A sound object is a sound heard for "
                   "itself, apart from what caused it. <bookmark mark='c'/> Reduced listening attends to its shape, grain and "
                   "mass, not to the door or the bell behind it. <bookmark mark='d'/> His Treatise on Musical Objects, of 1966, "
                   "classifies sounds by how they behave in time. <bookmark mark='e'/> The cut attack is the key experiment: "
                   "much of a sound's identity lives in its first moments, as Part 4's ear suggested. <bookmark mark='f'/> "
                   "Pierre Henry, Éliane Radigue and the Paris research group carried the tradition on.", marks="cdef")

    # ------------------------------------------------------------------
    def tapes(self):
        items = [
            (r"Daphne Oram and Delia Derbyshire: \ the BBC Radiophonic Workshop \ (from 1958)", WHITE),
            (r"Derbyshire's realization of the \textit{Doctor Who} theme \ (1963): \ every sound made and spliced by hand", WHITE),
            (r"Halim El-Dabh in Cairo \ (1944): \ an early piece of manipulated recording", WHITE),
            (r"Pauline Oliveros, \ the San Francisco Tape Music Center \ (1962)", TUNE),
            (r"tape music became the ancestor of sampling \ (Parts 52 and 53)", GREY_A),
        ]
        rows_scene(self, r"tape, \ elsewhere", items,
                   "Tape music spread. <bookmark mark='b'/> In London, Daphne Oram and Delia Derbyshire worked at the BBC "
                   "Radiophonic Workshop, founded in 1958, <bookmark mark='c'/> and Derbyshire's realization of the Doctor Who "
                   "theme, in 1963, built every sound and spliced it by hand. <bookmark mark='d'/> In Cairo, Halim El-Dabh had "
                   "made a piece from manipulated recordings as early as 1944. <bookmark mark='e'/> In California, Pauline "
                   "Oliveros helped found the San Francisco Tape Music Center in 1962. <bookmark mark='f'/> Tape music is the "
                   "ancestor of sampling, which Parts 52 and 53 build.", marks="cdef")

    # ------------------------------------------------------------------
    def speeds(self):
        d = load("speeds")
        c = clip("speeds.three")
        order = d["order"]
        names = {"normal": r"as recorded", "double": r"twice as fast: \ an octave up, \ half as long", "half": r"half speed: \ an octave down, \ twice as long"}
        rows_ = VGroup()
        for k in order:
            w = 3.0 * d["durations"][k] / d["durations"]["normal"]
            shift = {"normal": 0, "double": 12, "half": -12}[k]
            mel = [[p + shift, a * d["durations"][k] / d["durations"]["normal"], du * d["durations"][k] / d["durations"]["normal"]] for p, a, du in d["melody"]]
            g = mroll(mel, width=w, height=1.0, lo=58, hi=98, color=TUNE, total=8.0 * d["durations"][k] / d["durations"]["normal"], bar_h=0.08)
            rows_.add(VGroup(label(names[k], font_size=20, color=GREY_A), g).arrange(RIGHT, buff=0.5))
        rows_.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.2 + LEFT * 0.5)
        head = label(r"the Tune's first phrase, \ on tape, \ at three speeds", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Hear the first operation. The Tune's first phrase on Part 7's piano, recorded; then the same recording played "
            "twice as fast, an octave higher and half as long; then at half speed, an octave lower and twice as long. On "
            "tape, pitch and time cannot be changed separately: later processing methods can decouple them; digital techniques made this especially flexible, which Part 50 builds. Listen "
            "too to the piano's character changing."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"normal, \ double, \ half", detail=r"Part 7's piano, \ re-speeded", corner=DL, tag_corner=DR)
            for i, k in enumerate(order):
                end = d["starts"][order[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, rows_[i][0], d["starts"][k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lucier(self):
        items = [
            (r"Alvin Lucier, \ \textit{I am sitting in a room} \ (1969): \ a spoken paragraph, \ recorded", WHITE),
            (r"played back into the room and re-recorded, \ again and again", WHITE),
            (r"each pass strengthens the room's own resonances and weakens everything else", WHITE),
            (r"after many passes only the room's tones remain: \ the speech becomes music", TUNE),
            (r"a filter applied many times: \ Part 49's mathematics, \ heard as a process", GREY_A),
        ]
        rows_scene(self, r"the room as instrument", items,
                   "Tape could also turn a room into an instrument. <bookmark mark='b'/> In Alvin Lucier's I am sitting in a room, of 1969, a spoken paragraph is recorded, <bookmark mark='c'/> played back into the room and recorded again, over and over. <bookmark mark='d'/> Each pass strengthens the room's own resonant frequencies and weakens everything else, <bookmark mark='e'/> until only the room's tones remain, and the speech has become music. <bookmark mark='f'/> Mathematically it is one filter applied many times, which Part 49 builds.", marks="cdef")
