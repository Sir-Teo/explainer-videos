from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.cold_open()
        self.kemp()
        self.gold()
        self.plan()

    # ------------------------------------------------------------------
    def cold_open(self):
        d = load("two")
        c = clip("two.tones")
        scope = Scope(width=6.0, height=2.6, color=TUNE).move_to(LEFT * 3.4 + UP * 0.5)
        scap = label(r"the wave, \ slowed down", font_size=22, color=GREY_B).next_to(scope, DOWN, buff=0.15)
        g = axes([0, 2000], [0, 1.15], x_length=5.2, y_length=2.6, xlabel=r"frequency (Hz)", ylabel=r"what is in the sound",
                 xticks=[0, 800, 1000, 1200, 2000], yticks=[], font_size=20)
        g.move_to(RIGHT * 3.6 + UP * 0.45)
        bars = VGroup(*[Line(g.ax.c2p(f, 0), g.ax.c2p(f, 1.0), color=TUNE, stroke_width=9) for f in (d["f1"], d["f2"])])
        ghost = DashedLine(g.ax.c2p(d["third"], 0), g.ax.c2p(d["third"], 0.35), color=EAR, stroke_width=4, dash_length=0.08)
        q = label(r"?", font_size=44, color=EAR).next_to(ghost, UP, buff=0.1)
        self.play(FadeIn(scope), FadeIn(scap), FadeIn(g), FadeIn(bars), run_time=0.6)
        with self.listen(c) as snd:
            window(snd, r"two pure tones: \ 1000 Hz and 1200 Hz", kind="synthesized", detail=r"two sines, \ and nothing else")
            snd.drive(scope, scope.follow(c, window=0.016))
            for k, b in enumerate(bars):
                snd.drive(b, lambda m, t, k=k: m.set_stroke(opacity=0.75 + 0.25 * np.sin(14 * t + 2.0 * k)))
        scope.set_wave(c.mono[4800:4800 + 768].astype(float), 0.95 / float(np.abs(c.mono).max()))
        with self.voiceover(
            "Two pure tones, a thousand hertz and twelve hundred, and nothing else. The spectrum of what left your "
            "loudspeaker has exactly two lines. <bookmark mark='a'/> And yet many listeners hear a third tone "
            "underneath the two: lower, and faint, at eight hundred hertz. If you did not hear it, do not worry. "
            "Before this part is over we will help you find it. <bookmark mark='b'/> If you did hear it: it was "
            "not in the air. Your ear made it."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ghost), FadeIn(q))
            vo.wait_until("b")
            note = label(rf"in the recording, \ at 800 Hz: \ {abs(d['in_the_clip_db']):.0f} dB below the two tones", font_size=26, color=EAR)
            note.to_edge(DOWN, buff=0.7)
            self.play(FadeIn(note), Indicate(q, color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kemp(self):
        card = history_card(1978, r"David Kemp, \ London",
                            r"seals a miniature loudspeaker and a microphone into a volunteer's ear canal, plays a "
                            r"click, and records what comes back", width=5.6).to_corner(UL, buff=0.45)
        g = axes([0, 20], [-1.2, 1.2], x_length=6.6, y_length=3.0, xlabel=r"milliseconds after the click", ylabel=r"sound pressure in the ear canal",
                 xticks=[0, 5, 10, 15, 20], yticks=[], font_size=20)
        g.move_to(RIGHT * 3.0 + DOWN * 0.1)
        t = np.linspace(0, 20, 1600)
        click = np.exp(-t / 0.5) * np.sin(2 * np.pi * 2.2 * t)
        chirp_f = 3.0 - 0.14 * (t - 6)
        echo = 0.16 * np.exp(-0.5 * ((t - 10.5) / 2.6) ** 2) * np.sin(2 * np.pi * np.cumsum(chirp_f) * (t[1] - t[0]))
        c1 = curve(g.ax, t[t < 4], click[t < 4], GREY_A, stroke_width=3)
        c2 = curve(g.ax, t[t >= 4], echo[t >= 4], EAR, stroke_width=3)
        l1 = label(r"the click", font_size=22, color=GREY_A).move_to(g.ax.c2p(3.0, 0.95))
        l2 = label(r"an answer, \ from the ear", font_size=24, color=EAR).move_to(g.ax.c2p(11.5, 0.62))
        tag = label(r"schematic, \ after Kemp (1978)", font_size=18, color=GREY_C).next_to(g, DOWN, buff=0.75).align_to(g, RIGHT)
        facts = VGroup(label(r"too late to be a reflection:", font_size=24, color=GREY_A),
                       label(r"sound crosses the whole ear in \ 0.1 ms", font_size=24, color=GREY_A),
                       label(r"and absent in ears that cannot hear", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        facts.next_to(card, DOWN, buff=0.4).align_to(card, LEFT)
        with self.voiceover(
            "In 1978, in London, David Kemp sealed a miniature loudspeaker and a microphone into a volunteer's ear "
            "canal, played a click, and recorded what came back. <bookmark mark='a'/> First the click itself, "
            "ringing for a millisecond or two. Then, five to fifteen milliseconds later, <bookmark mark='b'/> a "
            "faint answer. It comes far too late to be a reflection: sound crosses the whole ear in a tenth of a "
            "millisecond. <bookmark mark='c'/> And it is missing in ears that cannot hear. The ear was not only "
            "receiving sound. It was sending some back."
        ) as vo:
            self.play(FadeIn(card), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(l1), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(l2), FadeIn(tag), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(facts))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gold(self):
        c1 = history_card(1948, r"Thomas Gold, \ Cambridge",
                          r"aged 28: the inner ear is full of fluid, and fluid friction would smother any resonance. "
                          r"The ear must contain an amplifier. If it does, it may sometimes whistle.", width=4.2)
        c2 = history_card(1961, r"Georg von B\'ek\'esy",
                          r"Nobel Prize for watching waves travel in the inner ear: broad, sluggish, passive. "
                          r"His ears came from cadavers.", width=4.2)
        c3 = history_card(1978, r"David Kemp",
                          r"living ears send sound back out. Some whistle all by themselves.", width=4.2)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.7)
        line = label(r"a dead ear is passive. \quad A living ear is not.", font_size=38, color=EAR).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "One man had predicted it thirty years before. In 1948 Thomas Gold, twenty-eight years old and later a "
            "famous astrophysicist, argued that the inner ear cannot be a passive instrument. It is full of fluid, "
            "and friction in a fluid would smother any resonance in it. The ear, he said, must contain an "
            "amplifier that puts energy back in, and an amplifier like that might sometimes whistle by itself. "
            "<bookmark mark='a'/> Nobody believed him, for a good reason. Georg von Békésy had spent twenty years "
            "watching waves move inside real inner ears, and what he saw was broad, sluggish and passive. In 1961 "
            "it won him the Nobel Prize. But the ears on Békésy's bench came from cadavers. <bookmark mark='b'/> "
            "Kemp's microphone settled it. <bookmark mark='c'/> A dead ear is passive. A living ear is not."
        ) as vo:
            self.play(FadeIn(c1))
            vo.wait_until("a")
            self.play(FadeIn(c2))
            vo.wait_until("b")
            self.play(FadeIn(c3))
            vo.wait_until("c")
            self.play(FadeIn(line, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        trail = VGroup(label(r"Part 1: \ a string", font_size=26, color=STR), label(r"Part 2: \ the air", font_size=26, color=AIR),
                       label(r"Part 3: \ the spectrum", font_size=26, color=TUNE), label(r"Part 4: \ the listener", font_size=30, color=EAR)
                       ).arrange(RIGHT, buff=0.7).to_edge(UP, buff=0.5)
        card = objectives_card([
            r"how sound gets from air into the fluid of the inner ear",
            r"how a wave in that fluid sorts frequencies by place, \ and how finely",
            r"why loudness is not pressure, \ and what a loud sound hides",
            r"the two ways the ear measures pitch: \ where, \ and when",
            r"why a note keeps its pitch when its fundamental is removed, \ and where pitch stops",
            r"the frontier: \ the amplifier inside the ear",
        ], title=r"Part 4: \ The Ear", font_size=26).move_to(DOWN * 0.45)
        with self.voiceover(
            "So far this series has built a string, the air that carries its sound, and the spectrum that takes the "
            "sound apart. Part 3 ended with a puzzle: a tone with no energy at its fundamental that keeps its pitch "
            "anyway. A spectrum cannot explain that, because a spectrum describes the air. <bookmark mark='a'/> "
            "This part opens the instrument that does the listening. <bookmark mark='b'/> How sound gets from air "
            "into the fluid of the inner ear. <bookmark mark='c'/> How a wave in that fluid sorts frequencies by "
            "place, and how finely. <bookmark mark='d'/> Why loudness is not pressure, and what a loud sound hides. "
            "<bookmark mark='e'/> The two ways the ear measures pitch: where, and when. <bookmark mark='f'/> Why a "
            "note survives the loss of its fundamental, and where pitch stops altogether. <bookmark mark='g'/> And "
            "at the frontier, Gold's amplifier. Every model you will see is Monochord's own, a few hundred lines "
            "of code, checked against measurements of real ears."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(t) for t in trail[:3]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(trail[3]), FadeIn(card.head))
            for mark, r in zip("bcdefg", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
