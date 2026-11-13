from __future__ import annotations

import numpy as np

from videos.music.music8.common import *  # noqa: F403


class Cone(SoundScene):
    def construct(self):
        chapter(self, 4, r"Cones", r"Why does an oboe not sound like a clarinet?", lit=(1863,), extra=((1846, r"Sax patents the saxophone"),))
        self.shape()
        self.tip()
        self.quiz()

    # ------------------------------------------------------------------
    def shape(self):
        d = load("cone")
        cyl = bore_shape([0, 0.6], [0.0075, 0.0075], width=4.4, height=0.5, color=CLAR).move_to(LEFT * 4.2 + UP * 2.5)
        con = bore_shape([0, 0.6], [0.002, 0.03], width=4.4, height=1.1, color=SAX).move_to(LEFT * 4.2 + UP * 1.2)
        nm = VGroup(label(r"a cylinder: \ clarinet", font_size=24, color=CLAR).next_to(cyl, RIGHT, buff=0.3), label(r"a cone: \ oboe, \ bassoon, \ saxophone", font_size=24, color=SAX).next_to(con, RIGHT, buff=0.3))
        g = faxes(80, 2000, [-22, 36], x_length=10.4, y_length=2.9, ylabel=r"how hard the air column pushes back (dB)", yticks=[-20, 0, 20], fticks=(100, 200, 500, 1000, 2000), font_size=20)
        g.move_to(DOWN * 1.6)
        c1 = fcurve(g, d["f"], d["z_cyl_db"], CLAR, stroke_width=2.5)
        c2 = fcurve(g, d["f"], d["z_cone_db"], SAX)
        pc, ps = d["peaks_cyl"], d["peaks_cone"]
        t1 = VGroup(*[label(rf"{f:.0f}", font_size=20, color=CLAR).next_to(g.at(f, float(np.interp(f, d['f'], d['z_cyl_db']))), UP, buff=0.06) for f in pc[:3]])
        t2 = VGroup(*[label(rf"{f:.0f}", font_size=20, color=SAX).next_to(g.at(f, float(np.interp(f, d['f'], d['z_cone_db']))), UP, buff=0.06) for f in ps[:4]])
        with self.voiceover(
            "An oboe has a reed, like a clarinet, and is about as long. It sounds nothing like one, it plays "
            "most of an octave higher, and when it overblows it jumps an octave, not a twelfth. A saxophone and "
            "a bassoon are the same. What they share is the shape of the pipe. <bookmark mark='a'/> A "
            "clarinet's bore is a cylinder: the same width all the way down. These are cones: narrow at the "
            "reed, widening steadily to the bell. <bookmark mark='b'/> Here is the cylinder's response again, "
            f"sixty centimetres long, with its peaks at {say(pc[0])}, {say(pc[1])} and {say(pc[2])} hertz: "
            "one, three, five. <bookmark mark='c'/> And here is a cone of the same length. Its peaks are at "
            f"{say(ps[0])}, {say(ps[1])}, {say(ps[2])} and {say(ps[3])}: one, two, three, four. Every "
            "multiple, and starting most of an octave higher. The cone is closed at the reed, just as the "
            "cylinder is, and yet it has the notes of a pipe open at both ends. <bookmark mark='d'/> The "
            "reason is the spreading. In a cone a wave is a piece of a sphere, and as it runs towards the "
            "narrow end it is squeezed into less and less room. The arithmetic of that squeezing happens to "
            "put the pipe's notes exactly where an open pipe's would be. A cone behaves as though its point "
            "were an open end."
        ) as vo:
            fam = VGroup(*[label(t, font_size=34, color=SAX) for t in (r"oboe", r"bassoon", r"saxophone")]).arrange(RIGHT, buff=1.0).move_to(DOWN * 0.4)
            fl = label(r"reeds, \ like the clarinet; \ an octave between registers, \ like the flute", font_size=26, color=GREY_A).next_to(fam, DOWN, buff=0.4)
            self.play(FadeIn(fam), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(cyl), FadeIn(con), FadeIn(nm))
            vo.wait_until("b")
            self.play(FadeOut(fam), FadeOut(fl), run_time=0.4)
            self.play(FadeIn(g), Create(c1), FadeIn(t1), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(t2), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(con, color=WHITE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tip(self):
        d = load("cone")
        head = label(r"The missing tip", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        full = bore_shape([0, 0.12, 0.72], [0.0001, 0.005, 0.03], width=7.6, height=1.5, color=SAX).move_to(LEFT * 2.6 + UP * 1.3)
        cutline = DashedLine(UP * 0.5, DOWN * 0.5, color=GREY_B, stroke_width=2).move_to(full.get_left() + RIGHT * 7.6 * 0.12 / 0.72)
        tl = label(r"the reed has to go somewhere: \\ the tip is cut off", font_size=24, color=GREY_A).next_to(full, RIGHT, buff=0.3)
        rb, rc = d["ratios_bare"], d["ratios_cone"]
        tab = VGroup(
            VGroup(label(r"a perfect cone", font_size=26, color=GREY_A), MathTex(r"1 : 2 : 3 : 4", font_size=34)),
            VGroup(label(r"the tip cut off", font_size=26, color=BAD), MathTex(rf"1 : {rb[1]:.2f} : {rb[2]:.2f} : {rb[3]:.2f}", font_size=34, color=BAD)),
            VGroup(label(r"a mouthpiece with the tip's volume", font_size=26, color=GOOD), MathTex(rf"1 : {rc[1]:.2f} : {rc[2]:.2f} : {rc[3]:.2f}", font_size=34, color=GOOD)),
        )
        for k, r in enumerate(tab):
            r[0].move_to(LEFT * 5.6 + DOWN * (0.5 + 0.8 * k), aligned_edge=LEFT)
            r[1].move_to(RIGHT * 2.6 + DOWN * (0.5 + 0.8 * k))
        end = label(r"the resonances have to stay in step, \ or the reed has no family to lean on", font_size=26, color=TUNE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There is a catch. A cone that ran all the way to its point would leave nowhere to put a reed. So "
            "the point is cut off. <bookmark mark='a'/> And a cone without its tip no longer has its "
            "resonances in the ratios one, two, three, four. Monochord's cut-off cone has them at one, "
            f"{say(rb[1], 2)}, {say(rb[2], 2)}, {say(rb[3], 2)}: each one a little sharper than the last. "
            "That matters, because of what we saw with the register hole: a reed needs resonances that line "
            "up with the harmonics of its note. <bookmark mark='b'/> The cure is two centuries old. Replace "
            "the missing tip with a mouthpiece, a small chamber of any shape, whose volume is the same as "
            f"the volume of the cone that was cut away. The ratios come back: one, {say(rc[1], 2)}, "
            f"{say(rc[2], 2)}, {say(rc[3], 2)}. A saxophone's mouthpiece is sized by this rule, and so is "
            "the space inside an oboe's double reed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(full))
            self.play(Create(cutline), FadeIn(tl), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(end))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("cone")
        c = clip("cone.quiz")
        q = listen_card(r"The same note on two reed instruments. \ One has a cylinder for a bore, \ the other a cone. \\ Which is the cylinder?", width=9.6, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes(buff=2.6, width=3.0, height=1.3).move_to(UP * 0.3)
        with self.voiceover(
            "So what does the cone do to the sound? Here is the same note on two of Monochord's reed "
            "instruments. One has a cylinder for a bore, the other a cone. Which is the cylinder?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"one note, \ two bores", detail=r"model reed instruments", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.0)
        ha = harmonic_bars(d["quiz_db"]["A"], count=8, color=SAX, width=3.6, height=1.5, floor_db=-30).next_to(bx[0], DOWN, buff=0.45)
        hb = harmonic_bars(d["quiz_db"]["B"], count=8, color=CLAR, width=3.6, height=1.5, floor_db=-30).next_to(bx[1], DOWN, buff=0.45)
        la = label(rf"the cone, \ {100 * d['cone_length']:.0f} cm long: \ every harmonic", font_size=24, color=SAX).next_to(ha, DOWN, buff=0.2)
        lb = label(rf"the cylinder, \ {100 * d['cyl_length']:.0f} cm: \ the odd ones", font_size=24, color=CLAR).next_to(hb, DOWN, buff=0.2)
        with self.voiceover(
            "B was the cylinder: hollow, the even harmonics nearly gone. A was the cone: full and reedy, with "
            "every harmonic present, because every harmonic has a resonance of the pipe behind it. "
            f"<bookmark mark='a'/> And look at the lengths. For this one note the cylinder is "
            f"{say(100 * d['cyl_length'])} centimetres long and the cone {say(100 * d['cone_length'])}. That "
            "is the trade a maker faces. A cylinder reaches low notes with a short pipe and gives the "
            "clarinet's colour and its awkward twelfth. A cone needs most of twice the length, and gives a "
            "full spectrum and an octave. In 1846 Adolphe Sax patented a wide metal cone with a clarinet's "
            "mouthpiece on it, and got a new instrument."
        ) as vo:
            self.play(FadeOut(q), FadeIn(ha), FadeIn(hb))
            vo.wait_until("a")
            self.play(FadeIn(la), FadeIn(lb))
        self.wait(0.3)
        self.clear_scene()
