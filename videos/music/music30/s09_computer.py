from __future__ import annotations

import numpy as np

from videos.music.music30.common import *  # noqa: F403


class Computer(SoundScene):
    def construct(self):
        chapter(self, 8, r"The computer sings", r"When did a computer first make music?", extra=((1957, r"MUSIC at Bell Labs"),))
        self.bell()
        self.patch()
        self.daisy()
        self.fm()
        self.carlos()
        self.idea()

    # ------------------------------------------------------------------
    def bell(self):
        items = [
            (r"1951: \ CSIRAC in Sydney and the Ferranti Mark 1 in Manchester play tunes by toggling a loudspeaker", WHITE),
            (r"1957: \ Max Mathews at Bell Labs writes MUSIC, \ a program that computes every sample of a sound", WHITE),
            (r"the `unit generator': \ oscillators, \ envelopes, \ filters as building blocks in code", WHITE),
            (r"slow: \ minutes of computing for seconds of sound, \ written to tape and played back", TUNE),
            (r"the same idea as this series: \ every sound computed \ (Part 48)", GREY_A),
        ]
        rows_scene(self, r"the first computer music", items,
                   "Computers made sound almost as soon as they existed. <bookmark mark='b'/> In 1951 machines in Sydney and "
                   "Manchester played tunes by switching a loudspeaker on and off. <bookmark mark='c'/> In 1957 Max Mathews at "
                   "Bell Telephone Laboratories wrote MUSIC, a program that computes every sample of a sound, "
                   "<bookmark mark='d'/> built from what he called unit generators, oscillators, envelopes and filters as "
                   "blocks of code. <bookmark mark='e'/> It was slow: minutes of computing for seconds of sound, written to tape "
                   "and played back. <bookmark mark='f'/> It is the same idea this series runs on, every sound computed, and Part "
                   "48 starts it from the bottom.", marks="cdef")

    # ------------------------------------------------------------------
    def daisy(self):
        items = [
            (r"1961: \ a Bell Labs computer sings `Daisy Bell', \ with a computed voice", WHITE),
            (r"John Kelly and Carol Lochbaum made the voice; \ Mathews the accompaniment", WHITE),
            (r"a model of the vocal tract as a chain of tubes \ (Part 8's two-tube mouth, \ extended)", WHITE),
            (r"Arthur C. Clarke heard it, \ and Kubrick's HAL sings it as he is shut down in \textit{2001}", TUNE),
            (r"the voice this series uses is a distant descendant", GREY_A),
        ]
        rows_scene(self, r"Daisy, Daisy", items,
                   "In 1961 a computer sang. <bookmark mark='b'/> At Bell Labs a computer performed the song Daisy Bell, "
                   "<bookmark mark='c'/> its voice computed by John Kelly and Carol Lochbaum and its accompaniment by Max "
                   "Mathews, <bookmark mark='d'/> from a model of the vocal tract as a chain of tubes, Part 8's two-tube mouth "
                   "extended. <bookmark mark='e'/> The writer Arthur C. Clarke heard the demonstration, and in Stanley Kubrick's "
                   "2001 the computer HAL sings Daisy as it is shut down. <bookmark mark='f'/> The synthetic voice in this "
                   "series is a distant descendant.", marks="cdef")

    # ------------------------------------------------------------------
    def fm(self):
        items = [
            (r"John Chowning, \ Stanford, \ 1967--73: \ frequency modulation as synthesis", WHITE),
            (r"one sine wave bending another's frequency makes a whole spectrum, \ cheaply", WHITE),
            (r"licensed to Yamaha: \ the DX7 \ (1983) \ became the sound of a decade's pop music", WHITE),
            (r"Chowning's \textit{Turenas} \ (1972): \ sounds moving in space, \ by computing the Doppler shift", TUNE),
            (r"Part 52 builds FM, \ grains and physical models", GREY_A),
        ]
        rows_scene(self, r"frequency modulation", items,
                   "Then came a discovery that reached everyone. <bookmark mark='b'/> At Stanford, John Chowning found that "
                   "letting one sine wave bend another's frequency produces a whole spectrum, cheaply. <bookmark mark='c'/> "
                   "Stanford licensed it to Yamaha, and the DX7 synthesizer of 1983 became the sound of a decade's pop music. "
                   "<bookmark mark='d'/> Chowning's own Turenas, of 1972, moved sounds through space by computing the Doppler "
                   "shift of a moving source. <bookmark mark='e'/> Part 52 builds frequency modulation, grains and physical "
                   "models.", marks="bcde")

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"after 1945: \ music made of sound, \ chance, \ process and statistics, \ not only notes", WHITE),
            (r"new instruments: \ the tape machine, \ the oscillator, \ the computer", WHITE),
            (r"new listening: \ to texture, \ density, \ roughness, \ the inside of a sound", WHITE),
            (r"every one of these ideas runs through the studio music of today", TUNE),
            (r"Act VIII returns to the ear; \ Acts IX and X to electric sound and the studio", GREY_A),
        ]
        rows_scene(self, r"what changed", items,
                   "What changed after 1945? <bookmark mark='b'/> Music came to be made of sound, chance, process and statistics, "
                   "not only of notes, <bookmark mark='c'/> with new instruments, the tape machine, the oscillator, the computer, "
                   "<bookmark mark='d'/> and new kinds of listening, to texture, density, roughness and the inside of a sound. "
                   "<bookmark mark='e'/> Every one of these ideas runs through the studio music of today. <bookmark mark='f'/> "
                   "The series comes back to the ear in Act Eight, and to electric sound and the studio in Acts Nine and Ten.", marks="cdef")

    # ------------------------------------------------------------------
    def patch(self):
        d = load("unitgen")
        c = clip("unitgen.three")
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.0, corner_radius=0.15, color=col), label(t, font_size=21, color=col))
                         for t, col in ((r"oscillator: \ sawtooth", TUNE), (r"envelope", BLUE), (r"low-pass filter", EAR))]).arrange(RIGHT, buff=0.9).move_to(UP * 0.8)
        for b in boxes:
            b[1].move_to(b[0])
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.1, color=GREY_B) for i in range(2)])
        wv = d["wave"]
        pts = [np.array([-1.2 + 2.4 * i / (len(wv) - 1), 0.5 * v, 0]) for i, v in enumerate(wv)]
        wave = VMobject(stroke_color=TUNE, stroke_width=2).set_points_as_corners(pts).next_to(boxes[0], DOWN, buff=0.6)
        env = envelope_curve(d["env"], width=2.4, height=0.9, color=BLUE).next_to(boxes[1], DOWN, buff=0.5)
        head = label(r"a unit-generator patch \ (as in MUSIC and every synthesizer since)", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"heard three times: \ the oscillator; \ with the envelope; \ through the filter", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Mathews's idea is still one influential modular synthesis architecture. Connect unit generators: an oscillator making a sawtooth "
            "wave, full of harmonics; an envelope that shapes its loudness over time; a filter that removes the higher "
            "harmonics, here more and more as the note dies away. Hear the oscillator alone, then with the envelope, then "
            "through the filter: three blocks, and a raw buzz becomes something like a plucked bass."
        ):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(arrows), FadeIn(wave), FadeIn(env), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"oscillator, \ envelope, \ filter", kind="synthesized", detail=r"a unit-generator patch", corner=DL, tag_corner=DR)
            keys = ["osc", "env", "filter"]
            for i, k in enumerate(keys):
                end = d["starts"][keys[i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, boxes[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def carlos(self):
        items = [
            (r"Wendy Carlos, \ \textit{Switched-On Bach} \ (1968): \ Bach on a Moog synthesizer, \ a best-selling classical record", WHITE),
            (r"Laurie Spiegel at Bell Labs: \ \textit{The Expanding Universe} \ (1980), \ music from algorithms", WHITE),
            (r"Suzanne Ciani, \ Éliane Radigue, \ Isao Tomita: \ the synthesizer as a voice of its own", WHITE),
            (r"by the 1980s, \ the electronic studio had become a widely marketed instrument, though cost and access still varied", TUNE),
            (r"Part 51 builds the analogue synthesizer", GREY_A),
        ]
        rows_scene(self, r"synthesizers reach the public", items,
                   "Synthesizers reached a wide public quickly. <bookmark mark='b'/> Wendy Carlos's Switched-On Bach, of 1968, played Bach on a Moog synthesizer and became one of the best-selling classical records of its time. <bookmark mark='c'/> At Bell Labs, Laurie Spiegel composed with algorithms; her album The Expanding Universe appeared in 1980. <bookmark mark='d'/> Suzanne Ciani, Éliane Radigue and Isao Tomita each made the synthesizer a voice of its own. <bookmark mark='e'/> By the 1980s the electronic studio had become a widely marketed instrument, though cost and access still varied. <bookmark mark='f'/> Part 51 builds the analogue synthesizer.", marks="cdef")
