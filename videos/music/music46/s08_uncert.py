from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403


class Uncert(SoundScene):
    def construct(self):
        chapter(self, 7, r"Surprise and uncertainty together", r"When is a surprise a pleasure?")
        self.cheung()
        self.saddle()
        self.corners()
        self.tension()
        self.film()

    # ------------------------------------------------------------------
    def cheung(self):
        items = [
            (r"Vincent Cheung and colleagues \ (2019): \ modeled a pop-song corpus; \\ tested selected chord sequences without melody or lyrics", WHITE),
            (r"a model gave each chord a surprise and an uncertainty; \ behavioral and neuroimaging cohorts rated pleasure", WHITE),
            (r"pleasure was high for surprising chords after certain contexts, \ and for unsurprising chords after uncertain ones", WHITE),
            (r"neither number alone predicted pleasure; \ their interaction did, \ and with it amygdala and hippocampus activity", TUNE),
            (r"the published finding, \ quoted; \ its chords are under copyright and not played here", GREY_A),
        ]
        rows_scene(self, r"an interaction", items,
                   "The most direct test came in 2019. <bookmark mark='b'/> Vincent Cheung and colleagues modeled harmonic expectations using a large corpus of US popular songs and tested selected chord sequences without melody or lyrics. <bookmark mark='c'/> A model gave each chord a surprise and an uncertainty, and listeners rated pleasure in behavioral and neuroimaging experiments. <bookmark mark='d'/> Pleasure was high for surprising chords after certain contexts, and for unsurprising chords after uncertain ones. <bookmark mark='e'/> Neither number alone predicted pleasure; their interaction did, and so did activity in the amygdala and hippocampus. <bookmark mark='f'/> The finding is quoted here; the songs are under copyright and are not played.", marks="bcdef")

    # ------------------------------------------------------------------
    def saddle(self):
        d = load("corpus")
        e, s = np.array(d["entropy"]), np.array(d["ic"])
        x0, y0, W, H = -5.6, -2.5, 7.0, 4.4
        def P_(a, b):
            return [x0 + W * a / 5.0, y0 + H * min(b, 10) / 10.0, 0]
        ax = VGroup(Line(P_(0, 0), P_(5, 0), color=GREY_B), Line(P_(0, 0), P_(0, 10), color=GREY_B))
        for value in range(6):
            q = P_(value, 0)
            ax.add(label(str(value), font_size=12, color=GREY_A).move_to([q[0], q[1] - 0.16, 0]))
        for value in (0, 2, 4, 6, 8, 10):
            q = P_(0, value)
            ax.add(label(str(value) + ("+" if value == 10 else ""), font_size=12, color=GREY_A).move_to([q[0] - 0.2, q[1], 0]))
        ee, ss = np.median(e), np.median(s)
        good1 = Rectangle(width=W * ee / 5, height=H * (10 - ss) / 10, stroke_width=0, fill_color=TUNE, fill_opacity=0.15).move_to([(P_(0, 0)[0] + P_(ee, 0)[0]) / 2, (P_(0, ss)[1] + P_(0, 10)[1]) / 2, 0])
        good2 = Rectangle(width=W * (5 - ee) / 5, height=H * ss / 10, stroke_width=0, fill_color=TUNE, fill_opacity=0.15).move_to([(P_(ee, 0)[0] + P_(5, 0)[0]) / 2, (P_(0, 0)[1] + P_(0, ss)[1]) / 2, 0])
        dots = VGroup(*[Dot(P_(a, b), radius=0.025, color=BLUE, fill_opacity=0.5) for a, b in zip(e[::2], s[::2])])
        labs = VGroup(label(r"uncertainty \ (bits)", font_size=15, color=GREY_A).move_to([x0 + W / 2, y0 - 0.4, 0]), label(r"surprise \ (bits)", font_size=15, color=GREY_A).move_to([x0 + 0.5, y0 + H + 0.25, 0]))
        side = VGroup(label(r"gold regions: \ where Cheung's listeners liked chords most", font_size=17, color=TUNE),
                      label(r"low uncertainty, \ high surprise: \ the well-prepared surprise", font_size=16, color=WHITE),
                      label(r"high uncertainty, \ low surprise: \ the reassuring resolution", font_size=16, color=WHITE),
                      label(r"our corpus's notes, \ split at their medians; \ the regions are a sketch of the published pattern, \ not their data", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 4.2)
        side.scale_to_fit_width(min(side.width, 4.8)).move_to(RIGHT * 4.2)
        head = label(r"where pleasure lies", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Map it onto our listener's plane. <bookmark mark='a'/> Each dot is a note from our corpus, placed by "
            "uncertainty and surprise. <bookmark mark='b'/> Cheung's listeners liked best two opposite corners: a surprise "
            "when everything had seemed certain, the well-prepared twist; and a predictable arrival when things had been "
            "uncertain, the reassuring resolution. The gold regions sketch that pattern on our notes; they are not "
            "Cheung's data, which came from chords. A good surprise needs a firm expectation to break."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(dots), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(good1), FadeIn(good2), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tension(self):
        items = [
            (r"Part 42 uses a chosen tension proxy, \ not this entropy measure", WHITE),
            (r"Lerdahl and Krumhansl's tension model and listeners' continuous ratings agree in broad shape", WHITE),
            (r"a phrase that builds uncertainty and then resolves predictably is the reassuring corner, \ stretched out in time", WHITE),
            (r"a phrase that sets up certainty and then twists is the other corner", TUNE),
            (r"composers engineer both", GREY_A),
        ]
        rows_scene(self, r"tension as uncertainty", items,
                   "This links to tension. <bookmark mark='b'/> Part 42's chosen tension proxy uses pitch height, non-chord tones, chord labels and density; it does not directly compute this listener's entropy, <bookmark mark='c'/> and Lerdahl and Krumhansl's model and listeners' continuous ratings agree in broad shape. <bookmark mark='d'/> A phrase that builds uncertainty and then resolves predictably is the reassuring corner, stretched out in time; <bookmark mark='e'/> a phrase that sets up certainty and then twists is the other. <bookmark mark='f'/> Composers engineer both.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def corners(self):
        d = load("corners")
        c = clip("corners.two")
        cells = VGroup(VGroup(label(r"certain, \ then a surprise", font_size=22, color=TUNE), label(r"a firm dominant that turns to A$\flat$ major", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.2),
                       VGroup(label(r"uncertain, \ then the expected", font_size=22, color=TUNE), label(r"wandering chords that find their way home", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=1.2).move_to(UP * 0.3)
        head = label(r"the two corners, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear the two corners. A firm approach to the dominant, held, that turns to A flat major instead of home; then "
            "chromatic chords that wander, unsure where they are going, and find their way home to C."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two corners", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["certain"], st["uncertain"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["uncertain"], c.duration, buff=0.1)
        with self.voiceover("Different pleasures: the twist you did not see coming, and the relief of a home you were not sure you would reach."):
            self.play(Indicate(cells[0]), Indicate(cells[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def film(self):
        items = [
            (r"film scores manage uncertainty on purpose \ (Part 44): \ drones and ostinatos with no cadence in sight", WHITE),
            (r"Risset's endless glide \ (Part 45): \ uncertainty that never resolves", WHITE),
            (r"the build and drop \ (Part 40): \ uncertainty raised for many bars, \ then one very likely event, \ exactly on time", WHITE),
            (r"each is a route to one of Cheung's two corners", TUNE),
            (r"chapter 8: \ expectation in the body: \ groove", GREY_A),
        ]
        rows_scene(self, r"uncertainty, \ engineered", items,
                   "Composers engineer uncertainty on purpose. <bookmark mark='b'/> Film scores, Part 44's subject, use drones and "
                   "ostinatos with no cadence in sight. <bookmark mark='c'/> Risset's endless glide, from Part 45, is uncertainty "
                   "that never resolves. <bookmark mark='d'/> And the build and drop of Part 40 raises uncertainty for many bars, "
                   "then delivers one very likely event exactly on time. <bookmark mark='e'/> Each is a route to one of Cheung's "
                   "two corners. <bookmark mark='f'/> Chapter eight turns to expectation in the body: groove.", marks="bcdef")
