from __future__ import annotations

import numpy as np

from videos.music.music54.common import *  # noqa: F403

RC = {"1.0": GREY_A, "0.15": TUNE, "0.05": EAR}


class Proximity(SoundScene):
    def construct(self):
        chapter(self, 3, r"The proximity effect", r"Why does a voice grow bass as it nears the microphone?")
        self.derive()
        self.curves()
        self.tricks()
        self.heard()
        self.crooner()

    # ------------------------------------------------------------------
    def derive(self):
        lines = VGroup(
            MathTex(r"p(r) = \frac{P}{r}\,e^{-jkr}", font_size=36),
            MathTex(r"\frac{\partial p}{\partial r} = -\Big(jk + \frac{1}{r}\Big)\frac{P}{r}\,e^{-jkr}", font_size=36),
            MathTex(r"\frac{\text{near}}{\text{far}} = 1 + \frac{1}{jkr}, \qquad \Big|\cdot\Big| = \sqrt{1 + \frac{1}{(kr)^2}}", font_size=36),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        notes = VGroup(label(r"a small source sends out a spherical wave; \ a gradient microphone measures its slope", font_size=17, color=WHITE),
                       label(r"far away only the $jk$ term matters; \ close up, \ $1/r$ adds, \ and it is largest when $kr$ is small: \ low notes, \ short distances", font_size=17, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        head = label(r"the gradient of a spherical wave", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A gradient microphone has a quirk. <bookmark mark='a'/> A small source, a mouth, sends out a spherical wave: "
            "pressure P over r, with the phase turning as k r. <bookmark mark='b'/> The microphone measures its slope, and the "
            "slope has two parts: j k, which is all there is far away, and one over r. <bookmark mark='c'/> So close up the "
            "response is one plus one over j k r times the far-away response, and the extra part is largest when k r is small: "
            "low notes, at short distances."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            for mark, ln in zip("abc", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln), run_time=0.8)
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("proximity")
        f = np.array(d["f"])
        ax = logf_axes(width=8.0, height=3.4, flo=20, fhi=20000, ylo=-2, yhi=32, center=LEFT * 0.8 + DOWN * 0.2)
        cs = VGroup(*[curve(f, d["curves"][r]["fig8"], ax.to, color=RC[r], width=3) for r in ("1.0", "0.15", "0.05")])
        cc = VGroup(*[DashedVMobject(curve(f, d["curves"][r]["card"], ax.to, color=RC[r], width=2), num_dashes=40) for r in ("0.15", "0.05")])
        key = VGroup(label(r"1 m", font_size=17, color=RC["1.0"]), label(r"15 cm", font_size=17, color=RC["0.15"]), label(r"5 cm", font_size=17, color=RC["0.05"]),
                     label(r"solid: \ figure-8; \ dashed: \ cardioid", font_size=15, color=GREY_A)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.4)
        yl = label(r"dB re far away", font_size=15, color=GREY_A).next_to(ax, LEFT, buff=0.15)
        at = d["at100"]
        note = label(rf"at 100 Hz: \ +{at['1.0']:.1f} dB at 1 m, \ +{at['0.15']:.1f} at 15 cm, \ +{at['0.05']:.1f} at 5 cm", font_size=18, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"the bass rise, \ by distance", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here it is for a figure-8. <bookmark mark='a'/> At a metre the rise is small, about a decibel at a hundred hertz. "
            f"<bookmark mark='b'/> At fifteen centimetres, {say(at['0.15'], 1)} decibels; at five, {say(at['0.05'], 1)}: the "
            "bass of a voice multiplied tenfold. <bookmark mark='c'/> A cardioid is half gradient, so its rise is gentler, but "
            "it is still there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yl), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(Create(cs[0]), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(Create(cs[1]), Create(cs[2]), FadeIn(key[1:3]), FadeIn(note))
            vo.wait_until("c")
            self.play(Create(cc[0]), Create(cc[1]), FadeIn(key[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("proximity")
        c = clip("proximity.three")
        cells = choice_boxes([r"1 m", r"15 cm", r"5 cm"], width=2.8, buff=0.8, colors=[GREY_A, TUNE, EAR]).move_to(UP * 0.4)
        cap = label(r"Part 8's tenor through a figure-8, \ matched in loudness", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"closer and closer, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear it: the tenor at a metre, at fifteen centimetres, and at five."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        names = ["far", "near", "close"]
        with self.listen(c) as snd:
            window(snd, r"three distances", kind="physical model", detail=r"Part 8's voice", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            "From a metre the voice is plain; at fifteen centimetres it is warmer; at five it is thick and chesty, the sound "
            "of a radio announcer leaning into the microphone. Matched in loudness, the change you hear is the balance of bass "
            "against everything else."
        ):
            self.play(Indicate(cells[2], color=EAR, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def crooner(self):
        items = [
            (r"singers learned to play the effect: \ closer for intimacy, \ further back for the loud notes", WHITE),
            (r"broadcasters lean in for authority; \ podcasters too", WHITE),
            (r"many microphones have a bass-cut switch to undo it", WHITE),
            (r"an omni has no proximity effect: \ pressure has no gradient term", WHITE),
            (r"the effect is pure geometry: \ a spherical wave's slope", TUNE),
        ]
        rows_scene(self, r"playing the effect", items,
                   "Performers learned to play it. <bookmark mark='b'/> Singers move closer for intimacy and further back for the "
                   "loud notes; <bookmark mark='c'/> broadcasters lean in for authority, and podcasters too. <bookmark mark='d'/> "
                   "Many microphones have a bass-cut switch to undo it. <bookmark mark='e'/> An omni has no proximity effect at all, "
                   "because pressure has no gradient term. <bookmark mark='f'/> The effect is pure geometry: a spherical wave's "
                   "slope.", marks="bcdef")

    # ------------------------------------------------------------------
    def tricks(self):
        items = [
            (r"a bass-cut filter on the microphone or the desk undoes the rise at one distance only", WHITE),
            (r"some microphones open several ports at different distances behind the diaphragm, \ so the rise is spread and smaller", WHITE),
            (r"an omni has none, \ so it can be used close without boom, \ at the cost of hearing the room", WHITE),
            (r"two diaphragms back to back let a microphone switch patterns: \ the gradient part adds the rise", WHITE),
            (r"choosing a microphone is often choosing a proximity effect", TUNE),
        ]
        rows_scene(self, r"taming the effect", items,
                   "There are ways to tame it. <bookmark mark='b'/> A bass-cut filter on the microphone or the desk undoes the rise, but only at one distance. <bookmark mark='c'/> Some microphones open several ports at different distances behind the diaphragm, so the rise is spread out and smaller. <bookmark mark='d'/> An omni has none, so it can be used close without boom, at the cost of hearing more of the room. <bookmark mark='e'/> Two diaphragms back to back let a microphone switch patterns, and the gradient part brings the rise with it. <bookmark mark='f'/> Choosing a microphone is often choosing a proximity effect.", marks="bcdef")
