from __future__ import annotations

import numpy as np

from videos.music.music34.common import *  # noqa: F403


class Drone(SoundScene):
    def construct(self):
        chapter(self, 1, r"The drone", r"Why does a tanpura buzz?")
        self.role()
        self.bridge()
        self.hear()
        self.retune()
        self.physics()

    # ------------------------------------------------------------------
    def role(self):
        items = [
            (r"every note of a raga is heard against Sa, \ the tonic, \ sounding all the time", WHITE),
            (r"the tanpura: \ a long-necked lute with four strings and no frets, \ plucked in a slow cycle", WHITE),
            (r"usually Pa, \ Sa, \ Sa, \ and Sa an octave below \ (Ma or Ni for some ragas)", WHITE),
            (r"the drone fixes the reference against which intonation is judged", TUNE),
            (r"Part 5's consonance, \ heard continuously", GREY_A),
        ]
        rows_scene(self, r"the drone", items,
                   "Indian classical music is heard against a drone. <bookmark mark='b'/> Every note of a raga is measured "
                   "against Sa, the tonic, which sounds all the time. <bookmark mark='c'/> The tanpura is a long-necked lute "
                   "with four strings and no frets, plucked slowly in a cycle, <bookmark mark='d'/> usually tuned Pa, Sa, Sa, "
                   "and Sa an octave below, with Ma or Ni instead of Pa for some ragas. <bookmark mark='e'/> The drone fixes the "
                   "reference against which every note's tuning is judged: <bookmark mark='f'/> Part 5's consonance, heard "
                   "continuously.", marks="cdef")

    # ------------------------------------------------------------------
    def bridge(self):
        # a schematic: a string resting on a gently curved bridge, a thread under it
        brg = Arc(radius=6.0, start_angle=PI / 2 + 0.12, angle=-0.24, color=GREY_B, stroke_width=6).move_to(LEFT * 1.0 + DOWN * 0.6)
        string = Line(LEFT * 5.5 + DOWN * 0.3, RIGHT * 5.5 + DOWN * 0.3, color=TUNE, stroke_width=3)
        thread = Dot(LEFT * 0.4 + DOWN * 0.34, radius=0.06, color=EAR)
        labs = VGroup(label(r"string", font_size=20, color=TUNE).next_to(string, UP, buff=0.15).shift(RIGHT * 3.5),
                      label(r"curved bone bridge", font_size=20, color=GREY_B).next_to(brg, DOWN, buff=0.25),
                      label(r"the thread \ (\textit{jiv\=ari})", font_size=20, color=EAR).next_to(thread, DOWN, buff=0.6))
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"the string does not leave the bridge at a sharp edge: \ it grazes a curved surface", WHITE),
            (r"as it swings, \ the point where it leaves the bridge moves back and forth", WHITE),
            (r"that shakes energy up into high partials: \ the buzz, \ \textit{jaw\=ari}", TUNE))]).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.4)
        head = label(r"the jawari bridge", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The tanpura's sound comes from its bridge. <bookmark mark='a'/> The string does not leave the bridge at a sharp "
            "edge, as on a guitar. It lies across a wide, very gently curved surface of bone, adjusted with a cotton thread. "
            "<bookmark mark='b'/> As the string swings, the point where it lifts off the bridge moves back and forth. "
            "<bookmark mark='c'/> That moving contact shakes energy up into high partials, and the tone buzzes and shimmers. "
            "The effect, and the art of shaping the bridge, are both called jawari."
        ) as vo:
            self.play(FadeIn(head), Create(brg), Create(string), FadeIn(labs[:2]))
            vo.wait_until("a")
            self.play(FadeIn(thread), FadeIn(labs[2]), FadeIn(rows_[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("tanpura")
        c = clip("tanpura.three")
        ax = Axes(x_range=[0, 3, 0.5], y_range=[0, 1400, 200], x_length=6.4, y_length=3.4, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 15}).move_to(LEFT * 2.6 + DOWN * 0.3)
        lp = VMobject(color=BLUE, stroke_width=3).set_points_as_corners([ax.c2p(t, c_) for t, c_ in zip(d["plain"]["t"], d["plain"]["centroid"]) if t <= 3])
        lj = VMobject(color=TUNE, stroke_width=3).set_points_as_corners([ax.c2p(t, c_) for t, c_ in zip(d["jawari"]["t"], d["jawari"]["centroid"]) if t <= 3])
        xl = label(r"seconds after the pluck", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.3)
        yl = label(r"brightness: \ spectral centroid, \ Hz", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.15)
        at = d["at"]
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (rf"sharp bridge: \ {at['plain']['0.1']:.0f} Hz at 0.1 s, \ {at['plain']['0.3']:.0f} at 0.3 s", BLUE),
            (rf"curved bridge: \ {at['jawari']['0.1']:.0f} Hz, \ then {at['jawari']['0.3']:.0f}", TUNE),
            (r"then the four strings in their cycle", WHITE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.4)).move_to(RIGHT * 3.7)
        head = label(r"one string, \ two bridges: \ a finite-difference model", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Monochord models it. A string, split into eighty pieces, obeys the wave equation step by step; the curved "
            "bridge is a surface the string may touch but never pass through. Pluck it with a sharp bridge, then with the "
            f"curved one. A tenth of a second after the pluck, the plain string's brightness is {say(round(at['plain']['0.1']))} "
            f"hertz; with the curved bridge it is {say(round(at['jawari']['0.1']))}, and it stays bright for the first third "
            "of a second. Listen to both, and then to the four strings in their cycle."
        ):
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), Create(lp), Create(lj), FadeIn(side))
        with self.listen(c) as snd:
            window(snd, r"sharp bridge, \ curved bridge, \ the cycle", detail=r"a string over a curved bridge", corner=DL, tag_corner=DR)
            pulse(snd, side[0], d["starts"]["plain"], d["starts"]["jawari"] - 0.4, buff=0.06)
            pulse(snd, side[1], d["starts"]["jawari"], d["starts"]["cycle"] - 0.4, buff=0.06)
            pulse(snd, side[2], d["starts"]["cycle"], c.duration, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def physics(self):
        items = [
            (r"C. V. Raman \ (1920s): \ the sitar's and tanpura's curved bridges, \ the first physics of jawari", WHITE),
            (r"the string's contact with the bridge is nonlinear: \ amplitude changes the tone", WHITE),
            (r"modern simulations \ (Vyasarayani and others, \ Bilbao and others) \ model the contact as here", WHITE),
            (r"our model is crude: \ a rigid bridge, \ no thread, \ one plane of motion", TUNE),
            (r"it shows the main effect: \ energy pushed up into high partials", GREY_A),
        ]
        rows_scene(self, r"the physics of jawari", items,
                   "The physics has a history. <bookmark mark='b'/> C. V. Raman, who later won a Nobel prize for light, studied "
                   "the curved bridges of the sitar and tanpura in the 1920s. <bookmark mark='c'/> The contact between string and "
                   "bridge is nonlinear: how loudly the string is plucked changes its tone. <bookmark mark='d'/> Modern "
                   "simulations, by Vyasarayani and colleagues and by Stefan Bilbao's group, model the contact much as this one "
                   "does. <bookmark mark='e'/> Ours is crude: a rigid bridge, no thread, motion in one plane only. "
                   "<bookmark mark='f'/> But it shows the main effect: energy pushed up into high partials.", marks="cdef")

    # ------------------------------------------------------------------
    def retune(self):
        d = load("dronema")
        c = clip("dronema.two")
        cells = VGroup(VGroup(label(r"Pa, \ Sa, \ Sa, \ low Sa", font_size=26, color=TUNE), label(r"the usual tuning", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2),
                       VGroup(label(r"Ma, \ Sa, \ Sa, \ low Sa", font_size=26, color=BLUE), label(r"for ragas that omit Pa, \ such as Malkauns", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=2.4).move_to(UP * 0.3)
        head = label(r"the drone is tuned to the raga", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The drone is tuned to the raga. Usually the first string is Pa, the fifth. But some ragas leave Pa out "
            "altogether, Malkauns for one, and a Pa in the drone would fight them. Then the first string is tuned to Ma, the "
            "fourth, or sometimes to Ni. Listen to the usual tuning, then the tuning with Ma."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"with Pa, \ then with Ma", detail=r"a string over a curved bridge", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], d["starts"]["pa"], d["starts"]["ma"] - 0.5, buff=0.1)
            pulse(snd, cells[1], d["starts"]["ma"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()
