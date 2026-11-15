from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.reveal()
        self.story()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"Two bells on the same note. \ One is Part 9's tuned bell, \ built from its eight measured partials. \ The other "
                           r"was made with just two sine oscillators. \ Which one?", width=10.0)
        with self.voiceover(
            "A question for your ears. Two bells on the same note. One is Part 9's tuned bell, built from the eight partials "
            "measured on real church bells. The other was made with just two sine oscillators. Which one?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two bells", kind="synthesized", detail=r"partials, \ and two oscillators", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reveal(self):
        d = load("hook")
        ax = frame_axes(width=11.0, height=1.6, xlo=0, xhi=3300, ylo=0, yhi=1.05, center=UP * 0.6)
        bx = frame_axes(width=11.0, height=1.6, xlo=0, xhi=3300, ylo=0, yhi=1.05, center=DOWN * 1.9)
        bl = [p for p in d["bell"] if p["hz"] < 3300]
        a = stems([p["hz"] for p in bl], [p["amp"] for p in bl], ax.to, color=BLUE, r=0.05)
        fl = [x for x in d["fm_lines"] if x[0] < 3300]
        mx = max(v for _, v in fl)
        b = stems([f for f, _ in fl], [v / mx for _, v in fl], bx.to, color=TUNE, r=0.05)
        ta = label(r"first: \ Part 9's bell, \ eight oscillators, \ one per measured partial", font_size=17, color=BLUE).next_to(ax, UP, buff=0.15)
        tb = label(r"second: \ two oscillators, \ 392 Hz and 549 Hz, \ in the ratio 1 : 1.4: \ lines at $392 \pm k \times 549$", font_size=17, color=TUNE).next_to(bx, UP, buff=0.15)
        xt = VGroup(*[label(f"{k} k", font_size=14, color=GREY_A).next_to(bx.to(k * 1000, 0), DOWN, buff=0.1) for k in (0, 1, 2, 3)])
        head = label(r"the second used two oscillators", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "The second. <bookmark mark='a'/> Part 9's bell is eight oscillators, one for each partial measured on real bells: "
            "the hum, the prime, the minor-third tierce and the rest. <bookmark mark='b'/> The second is two sines. One, the "
            "carrier, at the note; the other, the modulator, at 1.4 times it, pushing the carrier's phase back and forth. "
            "Out come lines at the carrier plus and minus every multiple of the modulator, none of them in a harmonic series: "
            "a bell, from two oscillators, and as the push dies away the lines fade from the top down, as a struck bell's do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(bx), FadeIn(xt))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(ta))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(tb))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"1967: \ John Chowning at Stanford turns a vibrato up until it is faster than the note itself, \ and hears bells", WHITE),
            (r"1973: \ his paper explains it: \ one Bessel function for every sideband", WHITE),
            (r"Stanford patents it and licenses it to Yamaha: \ one of the most lucrative patents the university ever held", WHITE),
            (r"1983: \ the DX7, \ six operators and sixteen voices, \ the sound of a decade's records", TUNE),
            (r"FM was cheap: \ a sine table and a few additions per operator, \ where analogue needed circuits", GREY_A),
        ]
        rows_scene(self, r"bells from a vibrato", items,
                   "The story begins with a mistake that was not one. <bookmark mark='b'/> In 1967 John Chowning, a composer at "
                   "Stanford, turned a vibrato up until it was faster than the note itself, and heard bells. <bookmark mark='c'/> "
                   "His 1973 paper explained it: one Bessel function for every sideband. <bookmark mark='d'/> Stanford patented it and "
                   "licensed it to Yamaha, and it became one of the most lucrative patents the university ever held. "
                   "<bookmark mark='e'/> In 1983 came the DX7, six operators and sixteen voices, the sound of a decade's records. "
                   "<bookmark mark='f'/> FM was cheap: a sine table and a few additions per operator, where analogue needed "
                   "circuits.", marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"frequency modulation: \ sidebands and Bessel functions",
            r"ratios, \ indices, \ operators and algorithms",
            r"granular synthesis, \ from Gabor's quanta to clouds",
            r"spectral models and samplers",
            r"physical models: \ Karplus--Strong, \ waveguides, \ modes",
            r"what each method costs, \ and what it lets a player control",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Frequency modulation: sidebands and Bessel functions. <bookmark mark='b'/> Ratios, indices, "
            "operators and algorithms. <bookmark mark='c'/> Granular synthesis, from Gabor's quanta to clouds. "
            "<bookmark mark='d'/> Spectral models and samplers. <bookmark mark='e'/> Physical models: Karplus-Strong, "
            "waveguides and modes. <bookmark mark='f'/> And what each method costs, and what it lets a player control."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
