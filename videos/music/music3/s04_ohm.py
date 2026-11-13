from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class Ohm(SoundScene):
    def construct(self):
        chapter(self, 3, r"What the ear does with it", r"Does the ear take sounds apart too?", lit=(1863,),
                extra=((1843, r"Ohm's law of hearing"),))
        self.law()
        self.bank()
        self.globe()
        self.worked()
        self.seebeck()

    # ------------------------------------------------------------------
    def law(self):
        card = history_card(1843, r"Georg Ohm",
                            r"(of the electrical law) proposes that the ear hears a tone of a given pitch only when the "
                            r"sound contains the pure tone of that frequency: the ear performs Fourier's analysis.", width=5.8)
        card.to_corner(UL, buff=0.4)
        hc = history_card(1863, r"Hermann von Helmholtz",
                          r"tests it with resonators: hollow glass globes, each tuned to one frequency, with a small "
                          r"opening to press into the ear", width=5.8).next_to(card, DOWN, buff=0.3)
        globes = VGroup()
        for i, r in enumerate((0.75, 0.55, 0.42, 0.33)):
            body = Circle(radius=r, stroke_color="#9FB8AD", stroke_width=3, fill_color="#9FB8AD", fill_opacity=0.06)
            neck = Rectangle(width=0.22, height=0.2, stroke_color="#9FB8AD", stroke_width=3).next_to(body, UP, buff=-0.02)
            ear = Polygon([-0.07, 0, 0], [0.07, 0, 0], [0.03, -0.2, 0], [-0.03, -0.2, 0], stroke_color="#9FB8AD", stroke_width=2).next_to(body, DOWN, buff=-0.02)
            globes.add(VGroup(body, neck, ear))
        globes.arrange(RIGHT, buff=0.5, aligned_edge=DOWN).move_to(RIGHT * 3.5 + UP * 0.6)
        gcap = VGroup(label(r"each one is the bottle of Part 2:", font_size=24, color=GREY_A),
                      label(r"a mass of air on a spring of air, \ with one note of its own", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.08).next_to(globes, DOWN, buff=0.35)
        with self.voiceover(
            "So a sound can be taken apart into pure tones on paper, and in a computer. Does the ear do the same? "
            "<bookmark mark='a'/> In 1843 Georg Ohm, the Ohm of the electrical law, proposed that it does: you hear "
            "a tone of a given pitch exactly when the sound contains the pure tone of that frequency. "
            "<bookmark mark='b'/> Twenty years later Hermann von Helmholtz found a way to test it. He had glass "
            "globes blown, each with a wide mouth and a narrow nipple to fit in the ear. <bookmark mark='c'/> Each "
            "globe is the bottle of Part 2: a mass of air on a spring of air, with one note of its own. Hold one to "
            "your ear while a note sounds. If the note contains the globe's frequency, the globe sings. If not, it "
            "stays silent."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
            vo.wait_until("b")
            self.play(FadeIn(hc), LaggedStart(*[FadeIn(g) for g in globes], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(gcap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bank(self):
        d = load("ohm")
        n = np.arange(1, 11)
        gb = axes([0.3, 10.7], [0, 1.12], x_length=8.6, y_length=3.4, xlabel=r"resonator tuned to partial", ylabel=r"how strongly it rings",
                  xticks=list(range(1, 11)), yticks=[0, 0.5, 1], font_size=20)
        gb.move_to(LEFT * 1.6 + DOWN * 0.4)
        bars = VGroup(*[Rectangle(width=0.5, height=max(gb.ax.c2p(0, v)[1] - gb.ax.c2p(0, 0)[1], 0.02), stroke_width=0, fill_color=harmonic_color(k),
                                  fill_opacity=0.9).move_to(gb.ax.c2p(k, v / 2)) for k, v in zip(n, d["bank"])])
        dots = VGroup(*[Dot(gb.ax.c2p(k, v), radius=0.08, color=WHITE) for k, v in zip(n, d["fft"])])
        notes = VGroup(*[label(flat_name(t), font_size=20, color=GREY_B).move_to(gb.ax.c2p(k, 1.07)) for k, t in zip(n, d["notes"])])
        head = label(r"ten resonators, \ one plucked string", font_size=32, color=GREY_A).to_edge(UP, buff=0.5)
        leg = VGroup(label(r"bars: \ the resonators", font_size=24, color=TUNE), label(r"dots: \ the transform", font_size=24, color=WHITE),
                     label(rf"they agree within {d['worst_db']:.1f} dB \\ on the {d['strong']} strong partials", font_size=24, color=GOOD)
                     ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 4.9 + UP * 0.2)
        with self.voiceover(
            "We can run Helmholtz's experiment on our own string. Ten resonators, tuned to one, two, three, up to "
            "ten times the string's frequency. Pluck the string and measure how strongly each one rings. "
            "<bookmark mark='a'/> They all ring, the low ones most. Those are the string's partials, found without "
            "any mathematics at all: only by resonance. <bookmark mark='b'/> The white dots are the same partials "
            f"from the transform of the last chapter. On the strong partials the two agree within "
            f"{say(d['worst_db'], 1)} decibels. A row of resonators is a Fourier analyser."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gb), FadeIn(notes))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.12), FadeIn(leg[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in dots], lag_ratio=0.1), FadeIn(leg[1]), FadeIn(leg[2]))
        self.bars, self.gb = bars, gb
        self.wait(0.3)

    # ------------------------------------------------------------------
    def globe(self):
        c = clip("ohm.globe")
        with self.voiceover(
            "And you can hear what Helmholtz heard. First the string. Then the same pluck through the resonator "
            "tuned to its third partial. Then through the fifth."
        ):
            pass
        with self.listen(c) as snd:
            window(snd, r"the string, \ then through one resonator at a time", detail=r"the third partial, \ then the fifth", corner=DL, tag_corner=UR)
            for ev, pick in (("all", range(10)), ("p3", [2]), ("p5", [4])):
                t0 = snd.time_of(ev)
                snd.wait_until(t0)
                for j, b in enumerate(self.bars):
                    on = j in pick
                    snd.drive(b, lambda m, t, on=on, t0=t0, j=j: m.set_fill(opacity=(0.25 + 0.7 * float(np.exp(-(0.6 + 0.12 * j) * (t - t0)))) if on else 0.1))
                snd.wait_until(t0 + 1.95)
        for b in self.bars:
            b.set_fill(opacity=0.9)
        with self.voiceover(
            "A G, and an E, inside a C. With these globes Helmholtz catalogued the partials of voices, violins, "
            "pipes and pianos, and concluded that Ohm was right: the ear is a row of resonators, and the quality of "
            "a sound, what tells a flute from a violin, is its recipe of partials."
        ):
            self.play(Indicate(self.bars[2], color=WHITE, scale_factor=1.1), Indicate(self.bars[4], color=WHITE, scale_factor=1.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        w = load("ohm")["worked"]
        title = label(r"A worked example: \ a clarinet and six globes", font_size=36).to_edge(UP, buff=0.45)
        given = label(rf"a clarinet plays its lowest note, \ {w['f0']:.0f} Hz; \ six globes are tuned to", font_size=28, color=GREY_A).move_to(UP * 2.0)
        globes = VGroup()
        for k, f in enumerate(w["globes"], 1):
            body = Circle(radius=0.62 - 0.07 * k, stroke_color="#9FB8AD", stroke_width=3, fill_color=TUNE, fill_opacity=0.0)
            globes.add(VGroup(body, label(rf"{f:.0f}", font_size=26, color=FREQ).next_to(body, DOWN, buff=0.15)))
        globes.arrange(RIGHT, buff=0.55, aligned_edge=DOWN).move_to(UP * 0.5)
        ask = pause_card(r"Which of the globes sing? \\ (Remember what kind of pipe a clarinet is.)", width=8.0).move_to(DOWN * 1.9)
        ans = label(r"a stopped pipe has only its odd partials: \ the first, \ third and fifth globes sing", font_size=28, color=GOOD).move_to(DOWN * 1.9)
        with self.voiceover(
            "A worked example, to connect this with Part 2. A clarinet plays its lowest note, a hundred and "
            "forty-seven hertz. <bookmark mark='a'/> Six of Helmholtz's globes stand ready, tuned to one, two, three, "
            "four, five and six times that. Which of them sing? Pause, and remember what kind of pipe a clarinet is."
        ) as vo:
            self.play(FadeIn(title), FadeIn(given))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in globes], lag_ratio=0.15), FadeIn(ask, shift=UP * 0.2), run_time=1.5)
        self.wait(1.5)
        with self.voiceover(
            "A clarinet behaves as a pipe stopped at one end, and a stopped pipe has only its odd partials. So the "
            "first, third and fifth globes sing, and the second, fourth and sixth stay nearly silent. That silence "
            "is what makes a clarinet's low notes sound hollow, and Helmholtz found it with exactly this apparatus."
        ):
            self.play(FadeOut(ask), FadeIn(ans), *[globes[k - 1][0].animate.set_fill(opacity=0.6) for k in w["sing"]])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def seebeck(self):
        card = history_card(1841, r"August Seebeck",
                            r"a siren whose holes are spaced to weaken the fundamental still sounds the same pitch. "
                            r"Ohm calls it an illusion.", width=5.6).to_corner(UL, buff=0.45)
        claims = VGroup(label(r"Helmholtz's two claims", font_size=30, color=GREY_B),
                        label(r"1. \ the ear separates a sound into pure tones", font_size=30),
                        label(r"2. \ the recipe of pure tones \emph{is} the sound's quality", font_size=30)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 2.6 + UP * 1.0)
        doubts = VGroup(label(r"a pitch can be heard at a frequency that is absent \quad $\rightarrow$ Part 4", font_size=26, color=BAD),
                        label(r"the same recipe can be two different sounds \quad $\rightarrow$ chapter 10", font_size=26, color=BAD)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(DOWN * 1.9)
        with self.voiceover(
            "It is a beautiful theory, and both halves of it are too simple. <bookmark mark='a'/> Even before "
            "Helmholtz, August Seebeck had built a siren that produced a tone with almost none of its lowest "
            "partial, and people heard the low pitch anyway. Ohm called that an illusion, and the argument ran for "
            "a century. We will settle it in Part 4. <bookmark mark='b'/> The second half, that the recipe is the "
            "whole of a sound's quality, we can test ourselves, before this part is over. First, though, there is "
            "something the recipe has been leaving out all along."
        ) as vo:
            self.play(FadeIn(claims))
            vo.wait_until("a")
            self.play(FadeIn(card), FadeIn(doubts[0]))
            vo.wait_until("b")
            self.play(FadeIn(doubts[1]))
        self.wait(0.3)
        self.clear_scene()
