from __future__ import annotations

from videos.music.music54.common import *  # noqa: F403


class Principles(SoundScene):
    def construct(self):
        chapter(self, 1, r"Transducers and their circuits", r"How does air become a voltage?")
        self.kinds()
        self.reciprocity()
        self.condenser()
        self.analogies()
        self.uses()

    # ------------------------------------------------------------------
    def kinds(self):
        cells = VGroup()
        for name, how, where, col in ((r"dynamic", r"a coil on the diaphragm moves in a magnet: \ $e = Bl\,v$", r"stage microphones, \ loudspeakers, \ headphones", TUNE),
                                      (r"condenser", r"the diaphragm is one plate of a charged capacitor: \ its voltage follows the gap", r"studio microphones \ (Wente, \ 1916)", BLUE),
                                      (r"ribbon", r"a thin metal ribbon in a magnet's gap, \ open on both sides", r"the RCA 44 \ (1930s), \ figure-8", EAR),
                                      (r"electret", r"a condenser whose charge is frozen into a plastic film", r"Sessler and West \ (1962): \ billions a year, \ in every phone", GOLD)):
            cells.add(VGroup(label(name, font_size=22, color=col), label(how, font_size=15, color=WHITE), label(where, font_size=14, color=GREY_A)).arrange(DOWN, buff=0.2))
        cells.arrange_in_grid(2, 2, buff=(0.8, 0.8)).move_to(DOWN * 0.2)
        head = label(r"four ways to turn pressure into voltage", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A microphone turns pressure into voltage, in one of a few ways. <bookmark mark='a'/> Dynamic: a coil fixed to the "
            "diaphragm moves in a magnet's field and makes a voltage B l times its velocity. <bookmark mark='b'/> Condenser: the "
            "diaphragm is one plate of a charged capacitor, and the voltage follows the gap, the design Wente built at Bell Labs "
            "in 1916. <bookmark mark='c'/> Ribbon: a thin metal ribbon in a magnet's gap, open to the air on both sides. "
            "<bookmark mark='d'/> And the electret, from Gerhard Sessler and James West in 1962: a condenser whose charge is "
            "frozen into a plastic film. Electrets became ubiquitous; many current phones instead use MEMS microphones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(cells, 0.3)))
            for mark, cc in zip("abcd", cells):
                vo.wait_until(mark)
                self.play(FadeIn(cc), run_time=0.7)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reciprocity(self):
        lines = VGroup(
            MathTex(r"\text{as a microphone:} \quad e = B l\, v", font_size=36),
            MathTex(r"\text{as a loudspeaker:} \quad F = B l\, i", font_size=36),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.8)
        notes = VGroup(label(r"$B$: \ the magnet's field; \ $l$: \ the length of wire in it; \ one number, \ $Bl$, \ couples both ways", font_size=18, color=WHITE),
                       label(r"a moving coil makes a voltage; \ a current in it makes a force", font_size=18, color=GREY_A),
                       label(r"so every dynamic transducer is both: \ the hook's headphones, \ and the loudspeaker in your laptop", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"one number, \ both directions", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The dynamic transducer works both ways. <bookmark mark='a'/> As a microphone, the coil moving at velocity v makes a "
            "voltage B l v. As a loudspeaker, a current i in the same coil makes a force B l i. <bookmark mark='b'/> B is the "
            "magnet's field and l the length of wire in it, and one number, B l, couples the electrical side to the mechanical "
            "both ways. <bookmark mark='c'/> So every dynamic transducer is both: the hook's headphones, and the loudspeaker in "
            "your laptop."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(lines))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def analogies(self):
        rows = VGroup(VGroup(label(r"electrical", font_size=19, color=GREY_A), label(r"mechanical", font_size=19, color=GREY_A), label(r"acoustical", font_size=19, color=GREY_A)))
        for e, m, a in ((r"voltage", r"force", r"pressure"), (r"current", r"velocity", r"volume velocity"), (r"inductance", r"mass", r"a slug of air in a port"),
                        (r"capacitance", r"compliance \ (a spring)", r"a volume of air in a box"), (r"resistance", r"friction", r"radiation, \ leaks")):
            rows.add(VGroup(label(e, font_size=20, color=BLUE), label(m, font_size=20, color=TUNE), label(a, font_size=20, color=EAR)))
        rows.arrange(DOWN, buff=0.3)
        for r in rows:
            for i, mm in enumerate(r):
                mm.set_x(-4.0 + 4.0 * i)
        rows.move_to(DOWN * 0.2)
        note = label(r"the same equations in three costumes: \ one circuit simulator solves them all", font_size=18, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"three kinds of circuit", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "To compute a transducer, treat everything as a circuit. <bookmark mark='a'/> Voltage, force and pressure play the "
            "same part; so do current, velocity, and the volume of air moved per second. <bookmark mark='b'/> A mass behaves "
            "like an inductance, and so does a slug of air in a port; a spring like a capacitance, and so does a box of air; "
            "friction and radiation like resistance. <bookmark mark='c'/> The same equations in three costumes: one circuit "
            "simulator solves them all, and this part's does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3:]))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"dynamic microphones are rugged and need no power: \ the stage's workhorses", WHITE),
            (r"condensers are light and fast, \ and need power \ (48 V `phantom' power down the cable): \ the studio's", WHITE),
            (r"ribbons are delicate and smooth, \ prized for brass and voices", WHITE),
            (r"each turns pressure, \ or its gradient, \ into voltage: \ that difference shapes how they hear direction", TUNE),
            (r"which is the next chapter", GREY_A),
        ]
        rows_scene(self, r"which microphone for which job", items,
                   "Each kind found its job. <bookmark mark='b'/> Dynamic microphones are rugged and need no power: the stage's workhorses. <bookmark mark='c'/> Condensers are light and fast, and need an electrical supply; forty-eight-volt phantom power is common, while other designs use batteries, plug-in power or separate supplies: the studio's choice. <bookmark mark='d'/> Ribbons are delicate and smooth, prized for brass and voices. <bookmark mark='e'/> And each responds either to pressure, or to its gradient, a difference that shapes how they hear direction, <bookmark mark='f'/> which is the next chapter.", marks="bcdef")

    # ------------------------------------------------------------------
    def condenser(self):
        lines = VGroup(
            MathTex(r"C = \frac{\varepsilon A}{d}, \qquad V = \frac{Q}{C} = \frac{Q\,d}{\varepsilon A}", font_size=38),
            MathTex(r"\Delta V = \frac{Q}{\varepsilon A}\,\Delta d", font_size=38),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.8)
        notes = VGroup(label(r"hold the charge $Q$ fixed: \ the voltage follows the gap $d$ exactly, \ an ideal constant-charge linear relation between gap and voltage; the complete microphone also has mechanical and electrical limits", font_size=18, color=WHITE),
                       label(r"the diaphragm can be a few microns of gold-coated film: \ light, \ so it follows the air to the highest frequencies", font_size=18, color=GREY_A),
                       label(r"its output impedance is enormous, \ so a transistor in the body converts it before the cable", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        head = label(r"the condenser, \ in two lines", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The condenser deserves its two lines. <bookmark mark='a'/> A capacitor's capacitance is the permittivity times "
            "the area over the gap, and its voltage is the charge over the capacitance. <bookmark mark='b'/> Hold the charge "
            "fixed, and a change in the gap makes a proportional change in voltage: an ideal constant-charge linear relation between gap and voltage; the complete microphone also has mechanical and electrical limits. <bookmark mark='c'/> "
            "The diaphragm can be a few microns of gold-coated film, light enough to follow the air to the highest "
            "frequencies; but the output impedance is enormous, so a transistor inside the body converts it before the cable."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1:]))
        self.wait(0.4)
        self.clear_scene()
