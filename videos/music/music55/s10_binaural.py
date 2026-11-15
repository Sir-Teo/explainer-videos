from __future__ import annotations

import math

import numpy as np

from videos.music.music55.common import *  # noqa: F403
from videos.music.music55.s07_cues import head_top


def block(text, color=GREY_B, w=2.6, h=0.8, size=18):
    return VGroup(RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=2.5), label(text, font_size=size, color=color))


class Binaural(SoundScene):
    def construct(self):
        chapter(self, 9, r"Binaural rendering", r"Can two headphone channels put a sound anywhere round you?")
        self.ears()
        self.hrtf()
        self.render()
        self.circle()
        self.outside()
        self.tracking()
        self.crosstalk()

    # ------------------------------------------------------------------
    def ears(self):
        items = [
            (r"we hear space with two signals, \ one at each eardrum; \ reproduce those two, \ and you reproduce the space", WHITE),
            (r"binaural recording: \ microphones in the ears of a dummy head \ (Neumann's KU 80, \ 1973)", WHITE),
            (r"played on headphones, \ the room, \ the directions and the distances come back", WHITE),
            (r"but only for a head like the dummy's, \ and only while you keep still", TUNE),
            (r"binaural rendering does it by computation: \ any sound, \ from any direction, \ through a model of the ears", GREY_A),
        ]
        rows_scene(self, r"two signals", items,
                   "Stereo pans between loudspeakers. Headphones allow something else. <bookmark mark='b'/> We hear space with two "
                   "signals, one at each eardrum; reproduce those two exactly, and you reproduce the space. "
                   "<bookmark mark='c'/> Binaural recording puts microphones in the ears of a dummy head, like Neumann's KU 80 of "
                   "1973. <bookmark mark='d'/> Played on headphones, the room, the directions and the distances come back, often "
                   "startlingly. <bookmark mark='e'/> But only for a head like the dummy's, and only while you keep still. "
                   "<bookmark mark='f'/> Binaural rendering does the same by computation: any sound, from any direction, through a "
                   "model of the ears.", marks="bcdef")

    # ------------------------------------------------------------------
    def hrtf(self):
        items = [
            (r"the head-related transfer function: \ for every direction, \ the filter from a far source to each eardrum", WHITE),
            (r"measured with tiny microphones in the ear canals and a loudspeaker moved round a sphere, \ in an anechoic room", WHITE),
            (r"KEMAR, \ MIT's mannequin \ (Gardner and Martin, \ 1994); \ the CIPIC database of 45 people \ (2001)", WHITE),
            (r"time and level differences, \ plus the pinna's notches: \ every cue of Chapter 6, \ in one pair of filters", TUNE),
            (r"Monochord's ears: \ a sphere \ (Woodworth's delay, \ Brown and Duda's shadow), \ with no pinnae", GREY_A),
        ]
        rows_scene(self, r"the filters of a head", items,
                   "The tool is the head-related transfer function. <bookmark mark='b'/> For every direction, it is the filter from "
                   "a distant source to each eardrum. <bookmark mark='c'/> It is measured with tiny microphones in the ear canals "
                   "and a loudspeaker moved round a sphere, in an anechoic room, hundreds of directions for each person. "
                   "<bookmark mark='d'/> The classic sets are KEMAR, MIT's mannequin, measured by Bill Gardner and Keith Martin in "
                   "1994, and the CIPIC database of forty-five people, from 2001. <bookmark mark='e'/> It holds every cue of Chapter "
                   "6: the time and level differences, and the pinna's notches. <bookmark mark='f'/> Monochord's ears are simpler: "
                   "a sphere, with Woodworth's delay and Brown and Duda's shadow, and no pinnae, which is why its front and back "
                   "sound alike.", marks="bcdef")

    # ------------------------------------------------------------------
    def render(self):
        src = block(r"a dry sound $x$", TUNE, w=2.4).move_to(LEFT * 5.0)
        dirb = block(r"its direction $\theta(t)$", EAR, w=2.8).move_to(LEFT * 5.0 + DOWN * 1.6)
        hl = block(r"$h_L(\theta)$", WHITE, w=1.9).move_to(LEFT * 0.8 + UP * 1.0)
        hr = block(r"$h_R(\theta)$", WHITE, w=1.9).move_to(LEFT * 0.8 + DOWN * 1.0)
        ol = block(r"left ear", GREY_A, w=1.8).move_to(RIGHT * 3.0 + UP * 1.0)
        orr = block(r"right ear", GREY_A, w=1.8).move_to(RIGHT * 3.0 + DOWN * 1.0)
        arrows = VGroup(Arrow(src.get_right(), hl.get_left(), buff=0.1, color=GREY_B, stroke_width=3), Arrow(src.get_right(), hr.get_left(), buff=0.1, color=GREY_B, stroke_width=3),
                        Arrow(hl.get_right(), ol.get_left(), buff=0.1, color=GREY_B, stroke_width=3), Arrow(hr.get_right(), orr.get_left(), buff=0.1, color=GREY_B, stroke_width=3),
                        DashedLine(dirb.get_right(), hr.get_bottom() + DOWN * 0.05, color=EAR, stroke_width=2))
        note = label(r"a moving source: \ a new pair of filters every block of 1,024 samples, \ the blocks overlapped and added so that no join clicks", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"a binaural renderer", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A renderer is then simple to describe. <bookmark mark='a'/> Take a dry sound, and the direction it should come "
            "from. <bookmark mark='b'/> Filter it twice, by the head-related filters for that direction, one for each ear, and "
            "send the results to the two sides of the headphones. <bookmark mark='c'/> If the source moves, the filters must "
            "change as it goes: Monochord's renderer picks a new pair for every block of a thousand and twenty-four samples, "
            "and overlaps and adds the blocks so that no join clicks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(src, dirb, hl, hr, ol, orr, arrows), 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(src), FadeIn(dirb))
            vo.wait_until("b")
            self.play(FadeIn(hl), FadeIn(hr), FadeIn(ol), FadeIn(orr), Create(arrows), run_time=1.4)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def circle(self):
        d = load("circle")
        c = clip("circle.one")
        hd = head_top(0.9, DOWN * 0.2)
        cen = hd[0].get_center()
        R = 2.4
        ring = DashedVMobject(Circle(radius=R, stroke_color=GREY_D, stroke_width=1.5).move_to(cen), num_dashes=60)
        dot = Dot(cen + R * UP, radius=0.14, color=EAR)
        trail = TracedPath(dot.get_center, stroke_color=EAR, stroke_width=3, dissipating_time=0.8)
        marks = VGroup(label(r"front", font_size=15, color=GREY_A).next_to(cen + R * UP, UP, buff=0.2), label(r"right", font_size=15, color=GREY_A).next_to(cen + R * RIGHT, RIGHT, buff=0.2),
                       label(r"behind", font_size=15, color=GREY_A).next_to(cen + R * DOWN, DOWN, buff=0.2), label(r"left", font_size=15, color=GREY_A).next_to(cen + R * LEFT, LEFT, buff=0.2))
        head = label(r"round the head, \ twice", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Hear it, with headphones: a shaker circling Monochord's head {say(d['turns'])} times in {say(d['seconds'])} "
            "seconds, starting in front and moving to the right."
        ):
            self.play(FadeIn(head), FadeIn(hd), FadeIn(ring), FadeIn(marks), FadeIn(dot))
        self.add(trail)
        secs = d["seconds"]
        turns = d["turns"]
        with self.listen(c) as snd:
            window(snd, r"a shaker, \ circling", kind="physical model", detail=r"a spherical head, \ headphones", corner=DL, tag_corner=DR)
            snd.drive(dot, lambda m, t: m.move_to(cen + R * np.array([math.sin(2 * math.pi * turns * t / secs), math.cos(2 * math.pi * turns * t / secs), 0])))
        self.remove(trail)
        with self.voiceover(
            "The sound swings convincingly from side to side, passing through the right ear and the left. But many listeners "
            "hear the front and back halves of the circle alike, or hear the whole circle inside the head, close behind the "
            "eyes: a sphere has no pinnae, and the renderer does not know which way you are facing."
        ):
            self.play(Indicate(hd, color=EAR, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def outside(self):
        items = [
            (r"with someone else's ears, \ sounds in front often jump behind, \ and many sit inside the head", WHITE),
            (r"externalization comes back with a room: \ reflections from their own directions, \ as in the halls of Chapter 4", WHITE),
            (r"Begault and colleagues \ (NASA, \ 2001): \ even a little simulated reverberation moves sounds out of the head", WHITE),
            (r"and with personal HRTFs: \ front-back reversals become rarer \ (Wenzel and colleagues, \ 1993)", WHITE),
            (r"and with the third cue of all, \ movement", TUNE),
        ]
        rows_scene(self, r"inside the head", items,
                   "Binaural rendering's two failures are well known. <bookmark mark='b'/> With someone else's ears, sounds in front "
                   "often jump behind, and many sit inside the head instead of out in the world. <bookmark mark='c'/> "
                   "Externalization comes back with a room: reflections arriving from their own directions, as in the halls of "
                   "Chapter 4. <bookmark mark='d'/> Durand Begault's experiments at NASA, published in 2001, found that even a little "
                   "simulated reverberation moves sounds out of the head. <bookmark mark='e'/> Personal HRTFs help too: Elizabeth Wenzel and "
                   "her colleagues found in 1993 that strangers' ears cause many more front-back reversals than one's own. <bookmark mark='f'/> And so does the oldest cue of all, movement.", marks="bcdef")

    # ------------------------------------------------------------------
    def tracking(self):
        hd = head_top(0.8, LEFT * 3.4 + DOWN * 0.3)
        cen = hd[0].get_center()
        src = Dot(cen + 2.1 * UP, radius=0.12, color=EAR)
        sl = label(r"the source, \ fixed in the room", font_size=15, color=EAR).next_to(src, UP, buff=0.1)
        rel = DashedLine(cen, src.get_center(), color=EAR, stroke_width=2)
        eq = MathTex(r"\theta_{\text{render}}(t) = \theta_{\text{source}} - \theta_{\text{head}}(t)", font_size=32, color=TUNE).move_to(RIGHT * 2.8 + UP * 1.4)
        items = text_rows([(r"a gyroscope in the headphones reports the head's turn", WHITE),
                           (r"the renderer subtracts it, \ so the source stays put while the head moves", WHITE),
                           (r"turn towards a sound and it moves the right way: \ front and back are settled", TUNE),
                           (r"the whole loop must take under about 50 ms, \ or the world swims", GREY_A)], font_size=19, width=6.4).move_to(RIGHT * 2.8 + DOWN * 0.8)
        head = label(r"head tracking", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Head tracking supplies the movement. <bookmark mark='a'/> A gyroscope in the headphones reports how far the head "
            "has turned, <bookmark mark='b'/> and the renderer subtracts it from the source's direction, so the source stays "
            "fixed in the room while the head moves. <bookmark mark='c'/> Turn towards a sound and it moves as a real one "
            "would: front and back are settled at once, as Wallach found in 1940. <bookmark mark='d'/> The whole loop, sensor, "
            "radio and filters, must take less than about fifty milliseconds, or the world seems to swim. Since 2020 phones and "
            "earbuds do this for everyone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hd), FadeIn(src), FadeIn(sl), FadeIn(rel), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(items[0]), Rotate(hd, angle=-0.5, about_point=cen), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(items[1]), Rotate(hd, angle=0.5, about_point=cen), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(items[2]))
            vo.wait_until("d")
            self.play(FadeIn(items[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def crosstalk(self):
        eq = MathTex(r"\begin{pmatrix} e_L \\ e_R \end{pmatrix} = \begin{pmatrix} H_{LL} & H_{LR} \\ H_{RL} & H_{RR} \end{pmatrix} \begin{pmatrix} s_L \\ s_R \end{pmatrix}"
                     r"\quad\Rightarrow\quad \begin{pmatrix} s_L \\ s_R \end{pmatrix} = \mathbf{H}^{-1} \begin{pmatrix} b_L \\ b_R \end{pmatrix}", font_size=32).move_to(UP * 1.2)
        items = [
            (r"binaural sound on loudspeakers: \ each ear hears both loudspeakers", WHITE),
            (r"Bauer \ (1961), \ Atal and Schroeder \ (1962): \ invert the 2 by 2 matrix of paths, \ cancelling each loudspeaker at the far ear", WHITE),
            (r"the sweet spot shrinks to a few centimetres, \ and the inverse needs a great deal of bass", WHITE),
            (r"soundbars and laptops do it today, \ with a camera or a fixed seat", TUNE),
        ]
        rows = text_rows(items, font_size=21).move_to(DOWN * 1.3)
        head = label(r"binaural on loudspeakers", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Can binaural sound be played on loudspeakers? <bookmark mark='a'/> Not directly: each ear hears both "
            "loudspeakers. <bookmark mark='b'/> Benjamin Bauer in 1961, and Bishnu Atal and Manfred Schroeder in 1962, inverted "
            "the problem: the ear signals are a two-by-two matrix of paths times the loudspeaker signals, so play the matrix's "
            "inverse times the binaural signals, and each loudspeaker's sound cancels at the far ear. <bookmark mark='c'/> The "
            "sweet spot shrinks to a few centimetres, and the inverse needs a great deal of bass. <bookmark mark='d'/> Soundbars "
            "and laptops do it today, with a camera watching the listener, or a fixed seat."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(eq, rows), 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(eq), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()
