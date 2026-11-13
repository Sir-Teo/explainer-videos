from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from explainer.music import CHAIN, DETOUR
from videos.music.music1.common import EAR, GOOD, HIST, PART, RATIO, STR, TUNE, load


class Series(SoundScene):
    def construct(self):
        self.card()
        self.question()
        self.monochord()
        self.rules()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(13, r"What we will build", r"Where does the string go from here?",
                            lit=(-530, 1863, 2016), part=PART, links=tuple(k for k, _ in CHAIN))
        with self.voiceover("Chapter thirteen. What we will build."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def question(self):
        first = VGroup(label(r"Why does a string have a pitch?", font_size=34, color=GREY_A),
                       MathTex(r"f = \frac{1}{2L}\sqrt{\frac{T}{\mu}}", font_size=34, color=GOOD),
                       label(r"answered today", font_size=28, color=GOOD)).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.35)
        q = label(r"Why do simple ratios sound good?", font_size=46, color=EAR).move_to(UP * 2.35)
        count = label(r"answered six times, \ by six sciences", font_size=30, color=GREY_B).move_to(UP * 0.9)
        answers = [(r"about 530 \textsc{bce}", r"Pythagoras", r"because the world is made of number", r"arithmetic"),
                   (r"1636", r"Mersenne, \ Galileo", r"because the vibrations keep step", r"mechanics"),
                   (r"1701 -- 1807", r"Sauveur, \ Bernoulli, \ Fourier", r"because every tone is a ladder of partials",
                    r"mathematics"),
                   (r"1863", r"Helmholtz", r"because shared partials do not beat", r"physiology"),
                   (r"1965", r"Plomp and Levelt", r"because of how the ear separates frequencies", r"psychology"),
                   (r"2016", r"McDermott and colleagues", r"partly because we learn to think so", r"anthropology")]
        rows = VGroup()
        for yr, who, what, field in answers:
            rows.add(VGroup(label(yr, font_size=26, color=HIST), label(who, font_size=26),
                            label(what, font_size=26, color=GREY_A), label(field, font_size=24, color=TUNE)))
        xs = [-6.7, -4.5, -1.0, 5.0]
        for i, r in enumerate(rows):
            for cell, x in zip(r, xs):
                cell.move_to([x, 1.45 - 0.72 * i, 0], aligned_edge=LEFT)
        with self.voiceover(
            "This part answered one question completely: why a string has a pitch. The other one, why simple "
            "ratios sound good, has been answered six times in twenty-five centuries, <bookmark mark='a'/> each "
            "time by a different science. Number. <bookmark mark='b'/> Vibration. <bookmark mark='c'/> Partials. "
            "<bookmark mark='d'/> Beats. <bookmark mark='e'/> The ear. <bookmark mark='f'/> And, in 2016, habit. "
            "To follow that question we will need all six sciences, and that is the plan of this series."
        ) as vo:
            self.play(FadeIn(first[0]), run_time=0.5)
            self.play(FadeIn(first[1], shift=LEFT * 0.2), FadeIn(first[2]), run_time=0.8)
            self.wait(1.2)
            self.play(FadeIn(q, shift=UP * 0.15))
            self.play(FadeIn(count))
            for mark, r in zip("abcdef", rows):
                vo.wait_until(mark)
                anims = [FadeIn(r, shift=RIGHT * 0.2)]
                if mark == "a":
                    anims.append(FadeOut(count))
                self.play(*anims, run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def monochord(self):
        title = VGroup(label(r"\textbf{Monochord}", font_size=44, color=STR),
                       label(r"the instrument this series builds, \ in code", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.15)
        title.to_edge(UP, buff=0.4)
        layers = [(r"the listeners", r"transcription, \ separation, \ models that compose", r"Parts 61--66"),
                  (r"the studio", r"microphones, \ rooms, \ a mixer, \ a mastering chain, \ codecs", r"Parts 54--59"),
                  (r"the electronics", r"oscillators, \ filters, \ effects, \ a sequencer", r"Parts 48--53"),
                  (r"the instruments", r"bows, \ hammers, \ reeds, \ a voice, \ drums and bells", r"Parts 7--9"),
                  (r"the theory", r"tunings, \ scales, \ chords, \ counterpoint, \ harmony", r"Parts 6--33"),
                  (r"the physics", r"\textbf{one string}", r"today")]
        stack = VGroup()
        for i, (name, what, when) in enumerate(layers):
            on = i == len(layers) - 1
            box = RoundedRectangle(width=11.6, height=0.62, corner_radius=0.1, stroke_width=1.5,
                                   stroke_color=TUNE if on else GREY_D, fill_color=TUNE if on else GREY_D,
                                   fill_opacity=0.25 if on else 0.08)
            a = label(name, font_size=26, color=TUNE if on else WHITE).move_to(box.get_left() + RIGHT * 0.3, aligned_edge=LEFT)
            b = label(what, font_size=24, color=WHITE if on else GREY_A).move_to(box.get_left() + RIGHT * 3.2, aligned_edge=LEFT)
            c = label(when, font_size=22, color=GREY_B).move_to(box.get_right() + LEFT * 0.3, aligned_edge=RIGHT)
            stack.add(VGroup(box, a, b, c))
        stack.arrange(DOWN, buff=0.1).move_to(DOWN * 0.35)
        check = label(r"every layer is checked against something that does not share its code: \ today, "
                      r"d'Alembert's formula", font_size=24, color=GOOD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Three things will hold the series together. The first is an instrument. We call it Monochord, and "
            "today it is exactly that: one simulated string. <bookmark mark='a'/> Each part adds the layer it "
            "teaches. Real instruments: bows and hammers, reeds, a voice, drums and bells. The machinery of music "
            "theory. Oscillators, filters and effects. Then a whole studio, and finally machines that listen and "
            "write. <bookmark mark='b'/> Every layer is checked against something that does not share its code, the "
            "way today's beads were checked against d'Alembert's formula."
        ) as vo:
            one = StringView(width=9.0, scale=0.55).move_to(UP * 0.7)
            xs = np.linspace(0, 1, 121)
            shape = np.minimum(xs / 0.2, (1 - xs) / 0.8)
            clock = {"t": 0.0}

            def ring(m, dt):
                clock["t"] += dt
                m.set_shape(shape * np.cos(2 * PI * 0.9 * clock["t"]) * np.exp(-0.12 * clock["t"]))

            one.add_updater(ring)
            today = label(r"today: \ one simulated string, \ slowed so that you can see it", font_size=26, color=GREY_B)
            today.next_to(one, DOWN, buff=0.75)
            self.play(FadeIn(title), FadeIn(stack[-1]), FadeIn(one), FadeIn(today))
            vo.wait_until("a")
            one.clear_updaters()
            self.play(FadeOut(one), FadeOut(today), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(s_, shift=DOWN * 0.15) for s_ in reversed(stack[:-1])], lag_ratio=0.5),
                      run_time=max(vo.until("b"), 3.0))
            self.play(FadeIn(check))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        ch = chain(lit=("instrument",), detour=True, width=13.0, font_size=22).move_to(UP * 0.2)
        cap = label(r"\textbf{the Chain}: \ the path a piece of music travels", font_size=28, color=GREY_A).next_to(ch, UP, buff=0.5)
        inner = [ch.link[k] for k, _ in CHAIN]
        outer = [ch.link[k] for k, _ in DETOUR]
        tune = VGroup(label(r"\textbf{the Tune}", font_size=32, color=TUNE),
                      label(r"one melody through all sixty-eight parts: \ each part writes a variation with what it "
                            r"has just built", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.4).move_to(UP * 0.3)
        rules = VGroup(
            label(r"Everything you hear, you see.", font_size=32, color=WHITE),
            label(r"Every sound is computed by the series' own code.", font_size=32, color=WHITE),
            label(r"Every part trains your ear as well as your pencil.", font_size=32, color=EAR),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 1.7)
        with self.voiceover(
            "The second is a map. Music travels a chain: from a mind to a score, through a player's hands and an "
            "instrument, across the air to an ear and into another mind. <bookmark mark='a'/> Today we lit one link. "
            "The detour underneath, through microphones and loudspeakers, is how most music has travelled for the "
            "last hundred years. <bookmark mark='b'/> The third is the Tune. Every part ends by writing a variation "
            "on it, using only what that part has built, and the last part performs them. <bookmark mark='c'/> And "
            "three rules. Everything you hear, you will also see. Every sound is computed by the code we write: no "
            "recordings. And every part will train your ears as well as your pencil."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(cap))
            self.wait(1.6)
            self.play(LaggedStart(*[Indicate(m, color=WHITE, scale_factor=1.25) for m in inner], lag_ratio=0.75),
                      run_time=max(vo.until("a") - 0.2, 2.0))
            vo.wait_until("a")
            self.play(Indicate(ch.link["instrument"], color=TUNE, scale_factor=1.3))
            self.play(LaggedStart(*[Indicate(m, color=WHITE, scale_factor=1.2) for m in outer], lag_ratio=0.6),
                      run_time=max(vo.until("b") - 0.8, 2.0))
            vo.wait_until("b")
            self.play(VGroup(ch, cap).animate.shift(UP * 1.75), run_time=0.7)
            self.play(FadeIn(tune))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in rules], lag_ratio=0.6), run_time=4.0)
        self.wait(0.3)
        self.clear_scene()
