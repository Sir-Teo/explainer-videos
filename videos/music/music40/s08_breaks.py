from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403


class Breaks(SoundScene):
    def construct(self):
        chapter(self, 7, r"The break and the sampler", r"How do you make a new beat out of an old record?")
        self.herc()
        self.hear()
        self.samplers()
        self.law()

    # ------------------------------------------------------------------
    def herc(self):
        items = [
            (r"1973, \ the Bronx: \ DJ Kool Herc plays two copies of a record and loops its drum break", WHITE),
            (r"the `break': \ the bars where the band drops out and the drums play alone", WHITE),
            (r"dancers \ (b-boys and b-girls) \ danced the breaks; \ MCs talked over them: \ hip hop", WHITE),
            (r"a turntable became an instrument: \ a beat made from a recording", TUNE),
            (r"from 1979 hip hop was recorded; \ from the mid-1980s samplers did what the turntables did", GREY_A),
        ]
        rows_scene(self, r"the break", items,
                   "Kool Herc's early Bronx parties, including the celebrated 1973 event, helped establish break-centered DJ practice; the familiar two-copy looping technique developed across early hip-hop DJing. <bookmark mark='b'/> The break is the few bars where the band drops out and the drums play alone. <bookmark mark='c'/> Dancers danced the breaks and MCs talked over them, and hip hop began. <bookmark mark='d'/> A turntable became an instrument, and a beat could be made from a recording. <bookmark mark='e'/> From 1979 hip hop was recorded, and from the mid-1980s samplers did what the turntables had done.", marks="bcde")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("breaks")
        c = clip("breaks.three")
        n = d["slices"]
        top = VGroup(*[VGroup(Rectangle(width=0.62, height=0.6, stroke_color=GREY_B, stroke_width=1.2, fill_color=VOICE_C[k % 4], fill_opacity=0.35),
                              label(str(k + 1), font_size=15, color=WHITE)) for k in range(n)]).arrange(RIGHT, buff=0.04).move_to(UP * 1.5)
        for cell in top:
            cell[1].move_to(cell[0])
        bottom = VGroup()
        for k in d["order"]:
            if k is None:
                cell = VGroup(Rectangle(width=0.62, height=0.6, stroke_color=GREY_D, stroke_width=1.2), label(r"--", font_size=15, color=GREY_A))
            else:
                cell = VGroup(Rectangle(width=0.62, height=0.6, stroke_color=GREY_B, stroke_width=1.2, fill_color=VOICE_C[k % 4], fill_opacity=0.35), label(str(k + 1), font_size=15, color=WHITE))
            cell[1].move_to(cell[0])
            bottom.add(cell)
        bottom.arrange(RIGHT, buff=0.04).move_to(DOWN * 0.6)
        lt = label(r"the break, \ cut into sixteen slices", font_size=19, color=GREY_A).next_to(top, UP, buff=0.2)
        lb = label(r"re-sequenced \ (`--' a rest), \ then played 1.2 times faster", font_size=19, color=GREY_A).next_to(bottom, UP, buff=0.2)
        stage = VGroup(*[label(t, font_size=19, color=GREY_A) for t in (r"the break", r"chopped", r"faster")]).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Here is the sampler's method, on a two-bar drum break of our own, played by the acoustic kit models. First "
            "the break as it is. Then cut into sixteen slices, one per eighth note, and played back in a new order with a "
            "rest. Then the new beat played 1.2 times faster, by reading the samples faster, so the pitch rises too, as an "
            "early sampler did."
        ):
            self.play(FadeIn(top), FadeIn(bottom), FadeIn(lt), FadeIn(lb), FadeIn(stage))
        st = d["starts"]
        bpm = d["bpm"]
        sl = 2 * 60.0 / bpm / 4
        with self.listen(c) as snd:
            window(snd, r"break, \ chopped, \ faster", detail=r"membrane and noise models, \ re-sequenced", corner=DL, tag_corner=DR)
            for k in range(n):
                pulse(snd, top[k], st["break"] + k * sl, st["break"] + (k + 1) * sl - 0.02, buff=0.02)
                pulse(snd, bottom[k], st["chopped"] + k * sl, st["chopped"] + (k + 1) * sl - 0.02, buff=0.02)
                pulse(snd, bottom[k], st["faster"] + k * sl / d["speed"], st["faster"] + (k + 1) * sl / d["speed"] - 0.02, buff=0.02)
            ks = ["break", "chopped", "faster"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, stage[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def samplers(self):
        items = [
            (r"E-mu's SP-1200 \ (1987) \ and Akai's MPC60 \ (1988): \ sampling and sequencing in one box", WHITE),
            (r"short sample times forced short loops, \ and sped-up records to fit more in", WHITE),
            (r"producers chopped, \ re-pitched and layered: \ a collage of other people's recordings", WHITE),
            (r"the most sampled breaks were funk and soul drummers' \ (chapter 4)", TUNE),
            (r"the same idea runs through every digital audio workstation \ (Part 53)", GREY_A),
        ]
        rows_scene(self, r"samplers", items,
                   "The samplers that made the sound were E-mu's SP-1200, of 1987, and Akai's MPC60, of 1988, each sampling and "
                   "sequencing in one box. <bookmark mark='b'/> Their short sample times forced short loops, and producers sped "
                   "records up to fit more in. <bookmark mark='c'/> They chopped, re-pitched and layered, a collage of other "
                   "people's recordings. <bookmark mark='d'/> The most sampled breaks were those of funk and soul drummers, from "
                   "chapter four. <bookmark mark='e'/> And the same idea runs through every digital audio workstation, Part 53's "
                   "subject.", marks="bcde")

    # ------------------------------------------------------------------
    def law(self):
        items = [
            (r"1991: \ \textit{Grand Upright Music v. Warner Bros. Records}: \ an uncleared sample infringed copyright", WHITE),
            (r"recording and composition rights are separate; \ exceptions vary", WHITE),
            (r"2005: \ \textit{Bridgeport v. Dimension Films}, \ the Sixth Circuit rejected de minimis sampling; \ other courts disagree", WHITE),
            (r"so sampling grew expensive, \ and producers turned to replaying parts, \ or to their own sounds", TUNE),
            (r"this film samples only its own Variation 7 \ (Part 60 returns to the law)", GREY_A),
        ]
        rows_scene(self, r"the law", items,
                   "Then the law arrived. <bookmark mark='b'/> In 1991, in Grand Upright Music against Warner Brothers Records, an American court held that an uncleared sample infringed copyright. <bookmark mark='c'/> Sampling can involve separate rights in the recording and composition, with exceptions and permissions depending on jurisdiction and use, <bookmark mark='d'/> and in 2005, in Bridgeport against Dimension Films, the Sixth Circuit rejected a de minimis defense for sound-recording sampling; other courts have disagreed, so this is not a universal rule for every short sample. <bookmark mark='e'/> So sampling grew expensive, and producers turned to replaying parts, or to sounds of their own. <bookmark mark='f'/> This film samples only its own Variation 7; Part 60 returns to the law.", marks="cdef")
