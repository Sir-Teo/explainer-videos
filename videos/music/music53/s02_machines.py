from __future__ import annotations

import numpy as np

from videos.music.music53.common import *  # noqa: F403


class Machines(SoundScene):
    def construct(self):
        chapter(self, 1, r"Machines that play", r"How old is the idea of music stored as instructions?")
        self.history()
        self.box()
        self.rolls()
        self.pianola()
        self.nancarrow()
        self.arithmetic()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"about 850, \ Baghdad: \ the Ban\=u M\=us\=a brothers describe a flute played by a turning cylinder of pins", WHITE),
            (r"a pin is an instruction: \ open this hole, \ now; \ the cylinder is a program", WHITE),
            (r"barrel organs, \ carillons and clocks played pinned cylinders for centuries", WHITE),
            (r"1796, \ Geneva: \ Antoine Favre's music box: \ pins pluck the teeth of a steel comb", TUNE),
            (r"swap the cylinder and the machine plays another tune: \ the music is data", GREY_A),
        ]
        rows_scene(self, r"music as instructions", items,
                   "Music stored as instructions is old. <bookmark mark='b'/> Around 850 in Baghdad the Banū Mūsā brothers described "
                   "a flute played by a turning cylinder of pins. <bookmark mark='c'/> A pin is an instruction, open this hole now, "
                   "and the cylinder is a program. <bookmark mark='d'/> Barrel organs, carillons and clocks played pinned cylinders "
                   "for centuries. <bookmark mark='e'/> In 1796 in Geneva, Antoine Favre made the music box: pins pluck the teeth of "
                   "a steel comb. <bookmark mark='f'/> Swap the cylinder and the machine plays another tune: the music is data.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def box(self):
        d = load("musicbox")
        c = clip("musicbox.one")
        notes = [(m, a, dd) for m, a, dd in d["notes"]]
        total = notes[-1][1] + notes[-1][2]
        drum = VGroup()
        W_, H_ = 10.0, 2.4
        frame = Rectangle(width=W_, height=H_, stroke_color=GREY_B, stroke_width=2).move_to(UP * 0.3)
        pins = VGroup()
        for m, a, dd in notes:
            pins.add(Dot([frame.get_left()[0] + W_ * (a + 0.1) / (total + 0.2), frame.get_bottom()[1] + H_ * (m - 82) / 14, 0], radius=0.07, color=TUNE))
        teeth = VGroup(*[Line([frame.get_left()[0] - 0.6, frame.get_bottom()[1] + H_ * (m - 82) / 14, 0], [frame.get_left()[0] - 0.1, frame.get_bottom()[1] + H_ * (m - 82) / 14, 0],
                              color=GREY_A, stroke_width=3) for m in sorted({n[0] for n in notes})])
        cap = label(r"the cylinder unrolled: \ one pin per note; \ the teeth of the comb at the left, \ one per pitch", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        tines = label(rf"a tine clamped at one end: \ overtones at {d['tine'][1]:.2f} and {d['tine'][2]:.2f} times the note, \ not harmonics", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"a music box, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is a music box, computed: the Tune's first two phrases on steel tines clamped at one end, whose overtones lie "
            "at six and seventeen and a half times the note, which is why a music box sounds glassy rather than like a piano."
        ):
            self.play(FadeIn(head), FadeIn(frame), FadeIn(pins), FadeIn(teeth), FadeIn(cap), FadeIn(tines))
        with self.listen(c) as snd:
            window(snd, r"a music box", kind="physical model", detail=r"clamped tines", corner=DL, tag_corner=DR)
            flash(snd, list(pins), [n[1] for n in notes], hot=WHITE, base=TUNE)
            ln = Line(frame.get_corner(DL), frame.get_corner(UL), color=WHITE, stroke_width=2)
            snd.show(ln)
            snd.drive(ln, lambda m, t: m.move_to([frame.get_left()[0] + W_ * min(max(t + 0.1, 0), total + 0.2) / (total + 0.2), frame.get_center()[1], 0]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rolls(self):
        items = [
            (r"about 1900: \ the player piano reads a paper roll: \ a hole is a key held down, \ air does the rest", WHITE),
            (r"1904: \ the Welte-Mignon reproducing piano records a pianist's dynamics and pedalling too", WHITE),
            (r"by the 1920s player pianos outsold ordinary ones in America; \ the radio and the gramophone ended them", WHITE),
            (r"a roll is a piano roll in the modern sense: \ time across, \ pitch up, \ holes for notes \ (Part 10)", TUNE),
            (r"and a roll can hold what no hands can play", GREY_A),
        ]
        rows_scene(self, r"paper rolls", items,
                   "The next machines read paper. <bookmark mark='b'/> Around 1900 the player piano read a roll: a hole is a key held "
                   "down, and air does the rest. <bookmark mark='c'/> In 1904 the Welte-Mignon reproducing piano recorded a "
                   "pianist's dynamics and pedalling too. <bookmark mark='d'/> By the 1920s player pianos outsold ordinary ones in "
                   "America, until the radio and the gramophone ended them. <bookmark mark='e'/> A roll is a piano roll in the modern "
                   "sense, time across and pitch up, as Part 10 drew it. <bookmark mark='f'/> And a roll can hold what no hands can "
                   "play.", marks="bcdef")

    # ------------------------------------------------------------------
    def pianola(self):
        d = load("pianola")
        c = clip("pianola.one")
        info = VGroup(label(rf"arpeggios at {d['rate']:.0f} notes a second", font_size=24, color=TUNE),
                      label(rf"then {len(d['chord'])} keys at once, \ over five octaves", font_size=24, color=EAR),
                      label(r"Part 7's computed piano, \ played by a roll", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        head = label(r"what no hands can play, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is what a roll can do: arpeggios at forty notes a second, then fifteen keys at once over five octaves."):
            self.play(FadeIn(head), FadeIn(info))
        with self.listen(c) as snd:
            window(snd, r"a roll", kind="physical model", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, info[0], 0.0, d["seconds"], buff=0.15)
            pulse(snd, info[1], d["seconds"], c.duration, buff=0.15)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nancarrow(self):
        items = [
            (r"Conlon Nancarrow, \ in Mexico City from the late 1940s, \ punched player-piano rolls by hand for fifty years", WHITE),
            (r"his Studies for Player Piano use speeds and densities no pianist could reach", WHITE),
            (r"tempo canons: \ the same line in several voices at different speeds, \ such as Study No. 36 at 17 : 18 : 19 : 20", WHITE),
            (r"the voices are started so that they meet at one moment: \ the convergence point", TUNE),
            (r"Variation 53 builds one, \ with the Tune at 3 : 4 : 5 : 6", GREY_A),
        ]
        rows_scene(self, r"Nancarrow", items,
                   "One composer took the roll seriously. <bookmark mark='b'/> Conlon Nancarrow, in Mexico City from the late 1940s, "
                   "punched player-piano rolls by hand for fifty years. <bookmark mark='c'/> His Studies for Player Piano use speeds "
                   "and densities no pianist could reach, <bookmark mark='d'/> and tempo canons: the same line in several voices at "
                   "different speeds, such as Study number 36, at seventeen to eighteen to nineteen to twenty. <bookmark mark='e'/> "
                   "The voices are started so that they meet at one moment, the convergence point. <bookmark mark='f'/> Variation 53 "
                   "builds one, with the Tune at three, four, five and six.", marks="bcdef")

    # ------------------------------------------------------------------
    def arithmetic(self):
        lines = VGroup(
            MathTex(r"\text{voice } v \text{ plays at } r_v \text{ beats a second; note } k \text{ falls on beat } b_k", font_size=32),
            MathTex(r"\text{it sounds at } \; s_v + \frac{b_k}{r_v}", font_size=34),
            MathTex(r"\text{to meet on note } K: \quad s_v = T - \frac{b_K}{r_v}, \qquad T = \max_v \frac{b_K}{r_v}", font_size=34),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.5)
        notes = VGroup(label(r"the slowest voice starts at zero; \ each faster one starts later, \ by just enough", font_size=18, color=WHITE),
                       label(r"before the meeting the voices drift apart in time, \ after it they would drift the other way", font_size=18, color=GREY_A),
                       label(r"Nancarrow worked this out by hand, \ with a ruler and a punch", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        head = label(r"the arithmetic of a tempo canon", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The arithmetic of a tempo canon is one line. <bookmark mark='a'/> Voice v plays at r v beats a second, and note k "
            "falls on beat b k, so it sounds at the voice's start plus b k over r v. <bookmark mark='b'/> To make every voice "
            "reach note K at the same moment T, start voice v at T minus b K over r v, with T set by the slowest voice, which "
            "starts at zero. <bookmark mark='c'/> Before the meeting the voices drift apart in time; after it they would drift "
            "the other way. Nancarrow worked this out by hand, with a ruler and a punch."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1:]))
        self.wait(0.4)
        self.clear_scene()
