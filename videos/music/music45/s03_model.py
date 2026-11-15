from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403


class Model(SoundScene):
    def construct(self):
        chapter(self, 2, r"A model of the boundary", r"Can the split be predicted?")
        self.boundaries()
        self.fission()
        self.competition()
        self.fit()
        self.neurons()
        self.limits()

    # ------------------------------------------------------------------
    def boundaries(self):
        items = [
            (r"van Noorden mapped two boundaries against tone repetition time \ (onset to onset)", WHITE),
            (r"the temporal coherence boundary: \ above it, \ two streams are always heard, \ however hard you try to hold one", WHITE),
            (r"the fission boundary: \ below it, \ one stream is always heard \ (about 1 to 2 semitones, \ nearly flat)", WHITE),
            (r"between them, \ either can be heard: \ the ambiguous region", TUNE),
            (r"the coherence boundary climbs as the tones slow down", GREY_A),
        ]
        rows_scene(self, r"two boundaries", items,
                   "Van Noorden mapped two boundaries against the tone repetition time, from one onset to the next. "
                   "<bookmark mark='b'/> Above the temporal coherence boundary two streams are always heard, however hard you "
                   "try to hold one. <bookmark mark='c'/> Below the fission boundary, about one to two semitones and nearly flat, "
                   "one stream is always heard. <bookmark mark='d'/> Between them either can be heard: the ambiguous region. "
                   "<bookmark mark='e'/> And the coherence boundary climbs as the tones slow down.", marks="bcde")

    # ------------------------------------------------------------------
    def competition(self):
        rows_ = text_rows([
            (r"a tone `captures' the next one with a strength that falls with time and with distance in pitch", WHITE),
            (r"strength \ = \ $e^{-\Delta t / \tau} \, e^{-|\Delta z| / w}$, \ with $\Delta z$ the distance on the ear's own scale \ (ERB-number, \ Part 4)", TUNE),
            (r"in ABA-, \ the next A is 2T away at the same pitch; \ B is T away at another pitch", WHITE),
            (r"two streams if A captures A more strongly than A captures B: \ $e^{-2T/\tau} > e^{-T/\tau} e^{-\Delta z / w}$", WHITE),
            (r"that is: \ $\Delta z > (w / \tau)\, T$ \ --- \ a boundary rising in a straight line with T, \ one constant to fit", EAR),
        ])
        head = label(r"a competition model", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Here is a small model of ours, built on Bregman's idea that grouping is a competition. <bookmark mark='a'/> Let "
            "each tone capture the next with a strength that falls with time and with distance in pitch. "
            "<bookmark mark='b'/> Strength is e to the minus time over tau, times e to the minus the distance over w, with "
            "distance measured on the ear's own frequency scale, the ERB-number scale of Part 4. <bookmark mark='c'/> In the "
            "triplet, the next A is two repetition times away at the same pitch; B is one away at another pitch. "
            "<bookmark mark='d'/> Two streams form when A captures the next A more strongly than it captures B. "
            "<bookmark mark='e'/> Work it through and the boundary is a straight line in the repetition time, with a single "
            "constant, w over tau, to fit."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fit(self):
        d = load("boundary")
        x0, y0, W, H = -5.4, -2.3, 7.4, 4.2
        def P_(t, s):
            return [x0 + W * (t - 0.04) / 0.13, y0 + H * s / 14.0, 0]
        ax = VGroup(Line(P_(0.04, 0), P_(0.17, 0), color=GREY_B), Line(P_(0.04, 0), P_(0.04, 14), color=GREY_B))
        ticks = VGroup(*[label(rf"{int(1000 * t)}", font_size=14, color=GREY_A).move_to([P_(t, 0)[0], y0 - 0.25, 0]) for t in (0.05, 0.08, 0.11, 0.14, 0.17)],
                       *[label(rf"{s}", font_size=14, color=GREY_A).move_to([x0 - 0.3, P_(0.04, s)[1], 0]) for s in (0, 4, 8, 12)])
        labs = VGroup(label(r"tone repetition time \ (ms)", font_size=16, color=GREY_A).move_to([x0 + W / 2, y0 - 0.6, 0]),
                      label(r"interval \ (semitones)", font_size=16, color=GREY_A).move_to([x0 + 1.1, y0 + H + 0.3, 0]))
        model = VMobject(color=TUNE, stroke_width=4).set_points_as_corners([P_(t, s) for t, s in zip(d["trt"], d["model"]) if s <= 14])
        pts = VGroup(*[Dot(P_(t, s), radius=0.09, color=EAR) for t, s in d["points"]])
        fb = DashedLine(P_(0.04, d["fission"]), P_(0.17, d["fission"]), color=BLUE)
        zones = VGroup(label(r"two streams", font_size=18, color=EAR).move_to(P_(0.07, 11.5)), label(r"one stream", font_size=18, color=BLUE).move_to(P_(0.14, 0.7)),
                       label(r"either", font_size=18, color=GREY_A).move_to(P_(0.15, 5.0)))
        side = VGroup(label(r"pink: \ van Noorden's coherence boundary, \ read from his figure \ (to about a semitone)", font_size=17, color=EAR),
                      label(r"gold: \ the model, \ one constant fitted", font_size=17, color=TUNE),
                      label(rf"w / $\tau$ = {d['k']:.1f} ERB-numbers a second; \ error {d['rms_st']:.2f} semitones \ (root mean square)", font_size=17, color=WHITE),
                      label(r"blue, \ dashed: \ the fission boundary", font_size=17, color=BLUE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 4.6 + UP * 0.3)
        side.scale_to_fit_width(min(side.width, 4.6)).move_to(RIGHT * 4.6 + UP * 0.3)
        head = label(r"the model against the data", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Fit it. <bookmark mark='a'/> In pink, points on van Noorden's coherence boundary, read from his figure as "
            "Bregman's book reproduces it, good to about a semitone. <bookmark mark='b'/> In gold, the model, with its one "
            f"constant fitted: {say(d['k'], 1)} ERB-numbers a second. It misses the points by "
            f"{say(d['rms_st'], 2)} of a semitone on average. <bookmark mark='c'/> The dashed line is the fission boundary; "
            "between the two lies the region where either organisation can be heard. A one-line model of competition between "
            "nearness in time and nearness in pitch captures the boundary's shape."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(model), FadeIn(side[1:3]))
            vo.wait_until("c")
            self.play(Create(fb), FadeIn(side[3]), FadeIn(zones))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"the model has no build-up, \ no attention and no ambiguity: \ it says one or two, \ never both", WHITE),
            (r"real models add neural adaptation, \ competition between populations, \ and noise \ (as in Rankin and colleagues, \ 2015)", WHITE),
            (r"the peripheral channelling idea: \ tones that excite different auditory filters segregate", WHITE),
            (r"temporal coherence: \ features that rise and fall together are bound into one source", TUNE),
            (r"chapter 3: \ the scene analysis inside a melody", GREY_A),
        ]
        rows_scene(self, r"what the model leaves out", items,
                   "The model is a sketch. <bookmark mark='b'/> It has no build-up, no attention and no ambiguity: it says one "
                   "stream or two, never both. <bookmark mark='c'/> Fuller models add neural adaptation, competition between "
                   "populations of neurons, and noise, which produce the flipping back and forth. <bookmark mark='d'/> One family "
                   "of explanations is peripheral channelling: tones that excite different auditory filters segregate. "
                   "<bookmark mark='e'/> Another is temporal coherence: features that rise and fall together are bound into one "
                   "source. <bookmark mark='f'/> Chapter three turns to the scene analysis inside a melody.", marks="bcdef")

    # ------------------------------------------------------------------
    def neurons(self):
        items = [
            (r"Micheyl and colleagues \ (2005) \ recorded neurons in monkeys' primary auditory cortex during ABA- sequences", WHITE),
            (r"responses to B faded over seconds when B was far from A, \ less when it was near", WHITE),
            (r"the fading predicted the time course of human reports of two streams", WHITE),
            (r"some of streaming's build-up may be neural adaptation, \ early in the cortex", TUNE),
            (r"a model with adaptation in it would build up as listeners do", GREY_A),
        ]
        rows_scene(self, r"streaming in neurons", items,
                   "Where does the build-up come from? <bookmark mark='b'/> In 2005 Christophe Micheyl and colleagues recorded "
                   "neurons in monkeys' primary auditory cortex while ABA sequences played. <bookmark mark='c'/> The responses to "
                   "B faded over seconds when B was far from A, and less when it was near, <bookmark mark='d'/> and the fading "
                   "predicted the time course of human reports of two streams. <bookmark mark='e'/> Some of streaming's build-up "
                   "may be neural adaptation, early in the cortex, <bookmark mark='f'/> and a model with adaptation in it would "
                   "build up as listeners do.", marks="bcdef")

    # ------------------------------------------------------------------
    def fission(self):
        d = load("fission")
        c = clip("fission.fast")
        head = label(r"below the fission boundary", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        box = VGroup(RoundedRectangle(width=6.0, height=1.6, corner_radius=0.2, stroke_color=GREY_B),
                     label(rf"{d['semitones']:.0f} semitone, \ {1000 * d['trt']:.0f} ms apart: \ fast, \ but close", font_size=22, color=WHITE)).arrange(ORIGIN).move_to(UP * 0.3)
        with self.voiceover("Here is the other side. The fast tempo, but B only one semitone above A. Try to hear two streams."):
            self.play(FadeIn(head), FadeIn(box))
        with self.listen(c) as snd:
            window(snd, r"one semitone, \ fast", kind="synthesized", detail=r"sine tones", corner=DL, tag_corner=DR)
            pulse(snd, box, 0.0, c.duration, buff=0.1)
        with self.voiceover(
            "You cannot. However hard you listen for the B tones alone, they stay part of a single trill-like line. That is "
            "the fission boundary: below it, attention cannot pull the sequence apart."
        ):
            self.play(Indicate(box))
        self.wait(0.3)
        self.clear_scene()
