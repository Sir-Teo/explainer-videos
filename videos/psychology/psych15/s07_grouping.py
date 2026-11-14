from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


def blocks(freqs, color_a=SOUND, color_b=PLACE, x0=-6.0, dx=0.36, y_of=None):
    g = VGroup()
    for k, f in enumerate(freqs):
        if not f:
            continue
        col = color_a if f == 500 else color_b
        g.add(Rectangle(width=dx * 0.8, height=0.18, stroke_width=0, fill_color=col, fill_opacity=0.95)
              .move_to([x0 + k * dx, y_of(f), 0]))
    return g


class Grouping(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.streaming()
        self.cues()

    def card(self):
        card = chapter_card(6, r"Auditory scene analysis", r"How does the ear pull one voice out of a crowd?",
                            lit={1953: r"Cherry", 1990: r"Bregman"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter six. Auditory scene analysis."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def problem(self):
        head = heading(r"One wave, \ many sources")
        t = np.linspace(0, 1, 600)
        s1 = 0.5 * np.sin(2 * np.pi * 6 * t)
        s2 = 0.35 * np.sin(2 * np.pi * 17 * t + 1)
        s3 = 0.25 * np.sign(np.sin(2 * np.pi * 3 * t))
        A = axes([0, 1], [-1.2, 1.2], x_length=6.0, y_length=1.0, xticks=[], yticks=[], center=[-3.4, 1.8, 0])
        B = axes([0, 1], [-1.2, 1.2], x_length=6.0, y_length=1.0, xticks=[], yticks=[], center=[-3.4, 0.5, 0])
        C = axes([0, 1], [-1.2, 1.2], x_length=6.0, y_length=1.0, xticks=[], yticks=[], center=[-3.4, -0.8, 0])
        srcs = VGroup(curve(A.ax, t, s1, SOUND), curve(B.ax, t, s2, PLACE), curve(C.ax, t, s3, TIMING))
        M = axes([0, 1], [-1.2, 1.2], x_length=5.0, y_length=2.4, xticks=[], yticks=[], center=[3.6, 0.5, 0])
        mix = curve(M.ax, t, s1 + s2 + s3, WHITE, stroke_width=3)
        ml = label(r"what reaches each ear: \ one sum", font_size=24, color=WHITE).next_to(M, UP, buff=0.1)
        rows = rows_of([
            (r"a voice, \ music and a fan add into one pressure wave; \ the ear must take the sum apart", WHITE),
            (r"Cherry, \ 1953: \ the cocktail party problem; \ Bregman, \ 1990: \ auditory scene analysis", GREY_A),
            (r"the same job grouping does for vision \ (Part 14), \ with Gestalt rules of its own", PRIOR),
        ], 12.4, 27, 0.28).to_edge(DOWN, buff=0.75)
        tag = note(r"drawn").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Now the real difficulty. <bookmark mark='a'/> A voice, music and the hum of a fan don't reach your ear "
            "separately. They add into one wave of pressure, and the ear must take the sum apart, with no labels "
            "saying which wiggle came from where. <bookmark mark='b'/> Colin Cherry named it the cocktail party problem "
            "in 1953, and Albert Bregman's book of 1990 called the solution auditory scene analysis. "
            "<bookmark mark='c'/> It's the same job that grouping does for vision, in Part 14, and it runs on Gestalt "
            "rules of its own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(srcs))
            vo.wait_until("a")
            self.play(TransformFromCopy(srcs, mix), FadeIn(M), FadeIn(ml), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def streaming(self):
        head = heading(r"On you: \ one rhythm, \ or two streams?")
        y_close = lambda f: 0.9 if f == 500 else 1.3  # noqa: E731
        y_far = lambda f: -1.2 if f == 500 else 0.0  # noqa: E731
        seq = [500, 560, 500, 0] * 4
        seq2 = [500, 1000, 500, 0] * 4
        g1 = blocks(seq, y_of=y_close)
        g2 = blocks([f if f != 560 else 1000 for f in seq2], y_of=y_far)
        l1 = label(r"close in pitch: \ a galloping rhythm", font_size=24, color=WHITE).next_to(g1, RIGHT, buff=0.4)
        l2 = label(r"far apart: \ two separate streams", font_size=24, color=WHITE).next_to(g2, RIGHT, buff=0.4)
        rows = rows_of([
            (r"listen: \ low, \ high, \ low, \ pause, \ repeated", WHITE),
            (r"close tones group into one gallop; \ far ones split, \ and the gallop vanishes", SOUND),
            (r"and once split, \ it is hard to hear how the two streams line up in time", PLACE),
        ], 12.4, 27, 0.28).to_edge(DOWN, buff=0.75)
        tag = psyche_tag(r"computed: \ tones of 500 and 560 Hz, \ then 500 and 1000 Hz, \ after van Noorden (1975)")
        with self.voiceover(
            "Here's a demonstration you can hear. <bookmark mark='a'/> A low tone, a higher one, the low one again, "
            "then a pause, repeated. When the two tones are close in pitch, you hear a single galloping rhythm. Listen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(l1), FadeIn(rows[0]))
        play(self, "stream_close")
        with self.voiceover("Now the same rhythm, with the higher tone an octave up. Listen."):
            self.play(FadeIn(g2), FadeIn(l2))
        play(self, "stream_far")
        with self.voiceover(
            "For most people the gallop falls apart into two streams: a slow beat of low tones and a slower one of "
            "high tones. <bookmark mark='a'/> Leon van Noorden mapped the boundary in 1975: the further apart the tones "
            "and the faster the sequence, the more likely they split. <bookmark mark='b'/> And once split, it becomes "
            "hard to say whether a high tone falls exactly between two low ones. You've stopped hearing one rhythm, "
            "and started hearing two sources."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def cues(self):
        head = heading(r"Bregman's grouping cues")
        rows = rows_of([
            (r"harmonicity: \ components at multiples of one fundamental belong to one source", TIMING),
            (r"common onset: \ components that start together came from one event", SOUND),
            (r"similar pitch and timbre over time: \ the streams you just heard", PLACE),
            (r"common location: \ the two ears' cues, \ chapter five", WHITE),
            (r"each a regularity of the world, \ like the Gestalt laws: \ priors for sounds; \ attention, \ Part 18", PRIOR),
        ], 12.6, 29, 0.4).move_to([0, -0.1, 0])
        with self.voiceover(
            "What tells the brain which pieces go together? <bookmark mark='a'/> Harmonicity: components at multiples "
            "of one fundamental almost always come from one source, like the harmonics of a voice. Mistune one "
            "harmonic by a few percent and it pops out as a separate tone. <bookmark mark='b'/> Common onset: "
            "components that start together came from one event. <bookmark mark='c'/> Similarity over time, in pitch "
            "and timbre: the streams you just heard. <bookmark mark='d'/> And common location, from the two ears' cues "
            "of chapter five. <bookmark mark='e'/> Each is a regularity of the world, like the Gestalt laws of vision: "
            "they're priors about sound. Which stream you then follow is the business of attention, in Part 18."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
