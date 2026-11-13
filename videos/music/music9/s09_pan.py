from __future__ import annotations

import numpy as np

from videos.music.music9.common import *  # noqa: F403


class Pan(SoundScene):
    def construct(self):
        chapter(self, 8, r"The steelpan", r"How do you make an instrument out of an oil barrel?", lit=(1945,), extra=((1946, r"the oil drum becomes a pan"),))
        self.story()
        self.tuning()

    # ------------------------------------------------------------------
    def story(self):
        rim = Circle(radius=1.9, color=STEEL, stroke_width=5).move_to(RIGHT * 3.6 + DOWN * 0.2)
        names = ["C", "G", "D", "A", "E", "B", r"F$\sharp$", r"C$\sharp$", r"A$\flat$", r"E$\flat$", r"B$\flat$", "F"]
        notes = VGroup()
        for k, n in enumerate(names):
            ang = PI / 2 - k * TAU / 12
            c = rim.get_center() + 1.35 * np.array([np.cos(ang), np.sin(ang), 0])
            notes.add(VGroup(Ellipse(width=0.62, height=0.5, color=STEEL, stroke_width=2, fill_color=STEEL, fill_opacity=0.15).rotate(ang - PI / 2).move_to(c), label(n, font_size=22, color=GREY_A).move_to(c)))
        cap = label(r"neighbours are a fifth apart", font_size=24, color=TUNE).next_to(rim, DOWN, buff=0.25)
        rows = VGroup(label(r"Trinidad, \ the 1930s: \ carnival bands beat on tins, \\ pans and the brake drums of cars", font_size=24, color=GREY_A),
                      label(r"a dent in a tin has a pitch, \\ and a deeper dent a different one", font_size=24, color=GREY_A),
                      label(r"1946: \ a whole oil drum, \ its top sunk into a bowl, \\ with a note hammered up for every pitch", font_size=24, color=STEEL),
                      label(r"each note is a small dome of steel: \\ a shell, \ not a skin", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(LEFT * 3.2 + DOWN * 0.1)
        with self.voiceover(
            "The newest instrument in this part is younger than the saxophone and was not designed by "
            "anybody. <bookmark mark='a'/> In Trinidad in the nineteen thirties, carnival bands, forbidden "
            "skin drums and then forbidden bamboo, were beating out their rhythms on biscuit tins, paint "
            "pans and the brake drums of cars. <bookmark mark='b'/> Somebody noticed that a dent in the "
            "bottom of a tin rings at a pitch, and that the pitch depends on the dent. A few dents made a "
            "few notes. <bookmark mark='c'/> By 1946 the players had moved to the oil drums left behind by "
            "the wartime naval base, with the top sunk into a smooth bowl by a sledgehammer and a note "
            "hammered back up out of the bowl for every pitch in the scale. <bookmark mark='d'/> Each note "
            "is a shallow dome of steel a few centimetres across. It is a curved shell, like a tiny bell, "
            "and on the lead pan the notes run round the rim in fifths, so that a note's neighbours are "
            "the ones that sound best with it."
        ) as vo:
            self.play(FadeIn(rim))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(notes[0]), FadeIn(notes[1]), FadeIn(notes[11]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(notes[k]) for k in range(2, 11)], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tuning(self):
        d = load("pan")
        c = clip("pan.build")
        names = [r"a raw dent", r"its note, \ tuned", r"and its octave", r"and its twelfth"]
        subs = [r"1 : 2.27 : 3.41", r"1", r"1 : 2", r"1 : 2 : 3"]
        bx = VGroup(*[VGroup(RoundedRectangle(width=2.8, height=1.2, corner_radius=0.14, stroke_color=STEEL, stroke_width=2), label(n, font_size=26, color=GREY_A)) for n in names]).arrange(RIGHT, buff=0.35).move_to(UP * 0.9)
        sb = VGroup(*[MathTex(t, font_size=30, color=TUNE if k else BAD).next_to(b, DOWN, buff=0.2) for k, (t, b) in enumerate(zip(subs, bx))])
        note = listen_note(r"One steelpan note, \ four times: \ before tuning, \ and then its partials tuned and added.", width=9.6, font_size=24).to_edge(DOWN, buff=0.6)
        head = label(r"Tuning with a hammer", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "A raw dome has overtones wherever its shape puts them, and sounds like a dustbin lid. The "
            "tuner's work is everything this part has been about, done by ear with a small hammer. "
            "<bookmark mark='a'/> First the dome's lowest mode is brought to the note. Then, by tapping the "
            "dome along its length, the next mode is moved until it is exactly an octave above. Then, by "
            "tapping across it, a third mode is brought to the twelfth, or the double octave. Three modes "
            "of one small shell, steered into a harmonic series one at a time. Listen to the note before "
            "tuning, and then as it is built."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bx[0]), FadeIn(sb[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(bx[k], sb[k])) for k in (1, 2, 3)], lag_ratio=0.6), FadeIn(note), run_time=6.0)
        with self.listen(c) as snd:
            window(snd, r"a steelpan note, \ built", kind="synthesized", detail=r"partials in a pan's proportions", corner=UL, tag_corner=UR)
            for ev, b in zip(("untuned", "one", "two", "three"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 1.6)
        with self.voiceover(
            "A clank; a dull thud; and then, with two more partials in tune, that bright, singing, "
            "slightly swelling sound. A good tuner spends days on one pan, and every hammer blow moves all "
            "the notes around it. Kettledrums were tuned by air, tablas by paste, marimbas by the knife, "
            "bells on the lathe. The steelpan was tuned by people who had none of that history, with a "
            "hammer, in about twenty years."
        ):
            self.play(FadeOut(note))
        self.wait(0.3)
        self.clear_scene()
