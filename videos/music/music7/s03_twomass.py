from __future__ import annotations

import numpy as np

from videos.music.music7.common import *  # noqa: F403


class TwoMass(SoundScene):
    def construct(self):
        chapter(self, 2, r"A plate, \ a hole and a box of air", r"Where do a guitar's two lowest resonances come from?", lit=(1863,),
                extra=((1980, r"the two-mass guitar"),), spoken="A plate, a hole and a box of air")
        self.model()
        self.worked()
        self.curve()

    def guitar(self):
        box = Rectangle(width=5.0, height=1.9, stroke_color=WOOD, stroke_width=4).move_to(LEFT * 3.3 + DOWN * 0.3)
        top_l = Line(box.get_corner(UL), box.get_corner(UL) + RIGHT * 2.9, color=TUNE, stroke_width=7)
        top_r = Line(box.get_corner(UR) + LEFT * 1.3, box.get_corner(UR), color=TUNE, stroke_width=7)
        hole = VGroup(*[Dot(box.get_corner(UL) + RIGHT * (3.05 + 0.14 * k) + UP * 0.0, radius=0.05, color=AIR) for k in range(5)])
        air = Rectangle(width=4.8, height=1.7, stroke_width=0, fill_color=AIR, fill_opacity=0.1).move_to(box)
        cover = Line(box.get_corner(UL), box.get_corner(UR), color="#0E1117", stroke_width=6)
        g = VGroup(box, cover, air, top_l, top_r, hole)
        g.box, g.top, g.hole, g.air = box, VGroup(top_l, top_r), hole, air
        return g

    # ------------------------------------------------------------------
    def model(self):
        d = load("twomass")
        g = self.guitar()
        names = VGroup(label(r"the top plate: \ a mass on its own spring", font_size=24, color=TUNE).next_to(g.box, UP, buff=0.3).align_to(g.box, LEFT).shift(LEFT * 1.3),
                       label(r"the air in the hole: \ a second mass", font_size=24, color=AIR).next_to(g.box.get_corner(UR), UP, buff=1.0).shift(RIGHT * 0.3),
                       label(r"the air in the box: \ the spring between them", font_size=24, color=GREY_A).next_to(g.box, DOWN, buff=0.25))
        ptr = Line(names[1].get_corner(DL) + RIGHT * 0.3, g.hole.get_top() + UP * 0.08, color=AIR, stroke_width=1.5)
        rows = VGroup(label(r"the box with rigid walls: \ Part 2's bottle", font_size=26, color=AIR), MathTex(rf"f_h = {d['helmholtz']:.0f}\ \text{{Hz}}", font_size=34, color=AIR),
                      label(r"the plate with the hole taped shut", font_size=26, color=TUNE), MathTex(rf"f_p = {d['plate']:.0f}\ \text{{Hz}}", font_size=34, color=TUNE),
                      label(r"joined by the same air, \ they push each other apart:", font_size=26, color=GREY_A),
                      MathTex(rf"{d['lower']:.0f}\ \text{{Hz}} \quad\text{{and}}\quad {d['upper']:.0f}\ \text{{Hz}}", font_size=38, color=GOOD)).arrange(DOWN, buff=0.16).move_to(RIGHT * 3.6 + DOWN * 0.1)
        with self.voiceover(
            "Look at a guitar from the side, and forget the strings. It is a box of air with a hole in it. In "
            "Part 2 we built exactly that, and called it a bottle: the air in the neck is a mass, the air in the "
            "body is a spring, and it has one note of its own. <bookmark mark='a'/> A guitar's box holds about "
            f"fourteen litres, and its soundhole is eight and a half centimetres across. If its walls were rigid, "
            f"Part 2's formula would give it a note of {say(d['helmholtz'])} hertz. <bookmark mark='b'/> But one "
            "wall is not rigid. The top is a thin plate of spruce, and it is a mass on a spring as well, with a "
            f"note of its own: with the hole taped shut, about {say(d['plate'])} hertz. <bookmark mark='c'/> "
            "And the two share the same air. When the plate moves in, it squeezes the air, and the air pushes "
            "the plug in the hole out. Two oscillators coupled by a spring do not keep their own notes. They "
            f"push each other apart: one resonance drops to {say(d['lower'])} hertz, the other rises to "
            f"{say(d['upper'])}. Those are the two peaks you heard in the knock."
        ) as vo:
            self.play(FadeIn(g.box), FadeIn(g.air), FadeIn(g[1]), FadeIn(g.top), FadeIn(g.hole))
            vo.wait_until("a")
            self.play(FadeIn(names[1]), FadeIn(ptr), FadeIn(names[2]), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(names[0]), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(g.top.animate(rate_func=there_and_back, run_time=1.2).shift(DOWN * 0.12), g.hole.animate(rate_func=there_and_back, run_time=1.2).shift(UP * 0.25))
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
            self.play(g.top.animate(rate_func=there_and_back, run_time=1.2).shift(DOWN * 0.12), g.hole.animate(rate_func=there_and_back, run_time=1.2).shift(UP * 0.25))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        d = load("twomass")
        title = label(r"A worked example: \ check a guitar with a tuner and a piece of card", font_size=34).to_edge(UP, buff=0.4)
        law = MathTex(r"f_-^{\,2} + f_+^{\,2} \;=\; f_h^{\,2} + f_p^{\,2}", font_size=44).move_to(UP * 1.9)
        src = label(r"Christensen and Vistisen (1980): \ true for any two oscillators coupled this way", font_size=22, color=GREY_B).next_to(law, DOWN, buff=0.2)
        ask = pause_card(rf"A guitar's lower resonance is {d['lower']:.0f} Hz. \ With the hole covered by a card, \ the plate rings at {d['plate']:.0f} Hz. \\ "
                         rf"The box as a bottle should give {d['helmholtz']:.0f} Hz. \ Where is the upper resonance?", width=10.4, font_size=26).move_to(DOWN * 0.7)
        work = VGroup(MathTex(rf"f_+^2 = {d['helmholtz']:.0f}^2 + {d['plate']:.0f}^2 - {d['lower']:.0f}^2 = {d['helmholtz'] ** 2 + d['plate'] ** 2 - d['lower'] ** 2:,.0f}".replace(",", "{,}"), font_size=36),
                      MathTex(rf"f_+ = {d['upper']:.0f}\ \text{{Hz}}", font_size=44, color=GOOD)).arrange(DOWN, buff=0.3).move_to(DOWN * 0.6)
        with self.voiceover(
            "The coupling obeys a rule that is simple enough to use at a workbench. <bookmark mark='a'/> The "
            "squares of the two resonances you get add up to the squares of the two you started with. So here "
            f"is a test. A guitar's lower resonance measures {say(d['lower'])} hertz. Cover the hole with a piece "
            f"of card, and the plate alone rings at {say(d['plate'])}. The box, treated as a bottle, should be at "
            f"{say(d['helmholtz'])}. Where is the upper resonance? Pause, and work it out."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(law), FadeIn(src), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"{say(d['helmholtz'])} squared plus {say(d['plate'])} squared, less {say(d['lower'])} squared, and "
            f"take the square root: {say(d['upper'])} hertz. On real guitars the rule holds to a few hertz, and "
            "makers use it to find out what a plate is doing inside an instrument they cannot open."
        ):
            self.play(FadeOut(ask), FadeIn(work))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("twomass")
        g = axes([50, 300], [-14, 32], x_length=9.6, y_length=3.6, xlabel=r"frequency (Hz)", ylabel=r"sound radiated (dB)", xticks=[50, 100, 150, 200, 250, 300], yticks=[-10, 0, 10, 20, 30], font_size=20)
        g.move_to(DOWN * 0.2 + LEFT * 0.4)
        cu = curve_from(g, d["f"], d["db"], WOOD)
        pk = VGroup(label(rf"{d['lower']:.0f} Hz: \ plate and hole \\ move oppositely", font_size=22, color=TUNE).move_to(g.ax.c2p(141, 25)),
                    label(rf"{d['upper']:.0f} Hz: \\ they move together", font_size=22, color=TUNE).move_to(g.ax.c2p(255, 24)))
        dip = VGroup(Dot(g.ax.c2p(d["dip"], float(np.interp(d["dip"], d["f"], d["db"]))), radius=0.07, color=BAD),
                     label(rf"{d['dip']:.0f} Hz: \ they cancel", font_size=22, color=BAD).move_to(g.ax.c2p(d["dip"], -4) + RIGHT * 0.2))
        low = VGroup(DashedLine(g.ax.c2p(d["low_e"], -14), g.ax.c2p(d["low_e"], 26), color=AIR, stroke_width=2), label(r"the guitar's lowest note: \ 82 Hz", font_size=22, color=AIR).move_to(g.ax.c2p(96, -11)))
        with self.voiceover(
            "Here is the sound the two of them radiate together, against frequency. <bookmark mark='a'/> Two "
            "peaks. At the lower one the plate and the air in the hole move in opposite directions: the plate "
            "goes in as the air goes out, like breathing. At the upper one they move together. "
            f"<bookmark mark='b'/> And between the two, near {say(d['dip'])} hertz, there is a hole in the "
            "response. There the hole's air moves against the plate so exactly that the two cancel: it is the "
            "bottle's own note, the one frequency at which the guitar is nearly dumb. <bookmark mark='c'/> Now "
            "look where the guitar's lowest note is: the open sixth string, eighty-two hertz. It is below the "
            "lowest peak. The body hardly answers at that frequency at all. So the fundamental of a guitar's "
            "bottom notes is weak, and what you hear as their pitch is, in good part, supplied by your ear from "
            "the partials above: the missing fundamental of Part 4. A guitar is too small for its own lowest "
            "notes, and gets away with it."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cu), run_time=2.5)
            self.play(FadeIn(pk))
            vo.wait_until("b")
            self.play(FadeIn(dip))
            vo.wait_until("c")
            self.play(Create(low[0]), FadeIn(low[1]))
        self.wait(0.3)
        self.clear_scene()
