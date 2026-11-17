from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


def stems(ax, harmonics, f0=200, color=SOUND, height=1.0):
    g = VGroup()
    for h in harmonics:
        g.add(Line(ax.c2p(h * f0, 0), ax.c2p(h * f0, height), color=color, stroke_width=6))
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.listen()
        self.missing()
        self.question()
        self.objectives()

    def panels(self, d, key, harmonics, color):
        W = axes([0, 15], [-1, 1], x_length=5.6, y_length=2.4, xticks=[0, 5, 10, 15], yticks=[-1, 0, 1],
                 xlabel=r"time (ms)", ylabel=r"pressure", center=[-3.4, 1.1, 0])
        wave = curve(W.ax, d["w_t"], d[key] / np.abs(d[key]).max(), color, stroke_width=3)
        F = axes([0, 1600], [0, 1.2], x_length=5.6, y_length=2.4, xticks=[0, 400, 800, 1200, 1600], yticks=[0, 1],
                 xlabel=r"frequency (Hz)", ylabel=r"amplitude", center=[3.4, 1.1, 0])
        st = stems(F.ax, harmonics, color=color)
        return W, wave, F, st

    def listen(self):
        d = load("pitch")
        head = heading(r"On you: \ listen")
        W, wave, F, st = self.panels(d, "w_full", range(1, 7), SOUND)
        rows = rows_of([
            (r"six harmonics: \ 200, \ 400, \ 600, \ 800, \ 1000 and 1200 Hz", SOUND),
            (r"you hear one note, \ with the pitch of the lowest: \ 200 Hz", YOU),
        ], 12.4, 28, 0.3).to_edge(DOWN, buff=0.8)
        tag = psyche_tag(r"computed: \ a harmonic complex, \ played as it is drawn")
        with self.voiceover(
            "Turn your sound on for this. <bookmark mark='a'/> Here's a sound made of six pure tones, at two hundred, "
            "four hundred, six hundred hertz and so on: the first six harmonics of two hundred. On the left, the "
            "pressure wave; on the right, its spectrum, one line for each tone. Listen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(W), Create(wave), FadeIn(F), LaggedStart(*[GrowFromEdge(s, DOWN) for s in st], lag_ratio=0.2),
                      FadeIn(rows[0]), run_time=2.5)
        play(self, "full")
        with self.voiceover(
            "You don't hear six tones. You hear one note, with a pitch at two hundred hertz, the lowest of them, the "
            "fundamental. That much seems obvious."
        ):
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def missing(self):
        d = load("pitch")
        head = heading(r"Now take the fundamental away")
        W, wave, F, st = self.panels(d, "w_missing", range(3, 7), PLACE)
        gone = VGroup(*[DashedLine(F.ax.c2p(f, 0), F.ax.c2p(f, 1.0), color=GREY_C, stroke_width=2) for f in (200, 400)])
        rows = rows_of([
            (r"only 600, \ 800, \ 1000 and 1200 Hz: \ nothing at 200", PLACE),
            (r"most people hear the same pitch: \ 200 Hz, \ the missing fundamental", YOU),
            (r"and here is a pure 200 Hz tone, \ for comparison", SOUND),
            (r"the pitch is not in the sound: \ the auditory system computes it", TIMING),
        ], 12.4, 27, 0.26).to_edge(DOWN, buff=0.8)
        tag = psyche_tag(r"computed: \ harmonics 3 to 6 of 200 Hz")
        with self.voiceover(
            "Now remove the first two harmonics, the two hundred and the four hundred. <bookmark mark='a'/> What's left "
            "is six hundred, eight hundred, a thousand and twelve hundred hertz. There is no energy at all at two "
            "hundred. Listen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(W), Create(wave), FadeIn(F), FadeIn(st), Create(gone), FadeIn(rows[0]), run_time=2.0)
        play(self, "missing")
        with self.voiceover(
            "The timbre is thinner. But for most people the pitch hasn't moved: it's still two hundred hertz, a note "
            "that isn't in the sound. Here's a pure two-hundred-hertz tone, to compare."
        ):
            self.play(FadeIn(rows[1]))
        self.play(FadeIn(rows[2]))
        play(self, "pure200")
        with self.voiceover(
            "This is called the missing fundamental, and the telephone has always depended on it. A classic phone line "
            "passes nothing below about three hundred hertz, and a phone's tiny speaker can barely move the air at a "
            "hundred, yet a man's voice, with its fundamental near a hundred hertz, doesn't sound like a child's. The pitch you "
            "hear isn't a property of the sound. The auditory system computes it, and chapter four shows how."
        ):
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ the other senses")
        rows = rows_of([
            (r"how does a pressure wave become a voice, \ a melody, \ a place in space?", SOUND),
            (r"how do touch, \ the body's position, \ smell, \ taste and balance code the world?", TOUCH),
            (r"why does pain not simply follow the injury?", PAIN),
            (r"and when the senses disagree, \ who wins? \ Part 14's rule, \ again", PRIOR),
        ], 11.8, 32, 0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "Part 13 followed light into the eye. Today, everything else. <bookmark mark='a'/> How does a pressure "
            "wave, a few millionths of an atmosphere, become a voice, a melody, a place in space? "
            "<bookmark mark='b'/> How do touch, the sense of the body's own position, smell, taste and balance code the "
            "world? <bookmark mark='c'/> Why does pain not simply follow the injury, so that a soldier can fail to "
            "notice a wound and an amputee can feel a hand that isn't there? <bookmark mark='d'/> And when the senses "
            "disagree, which wins? The answer, once again, is the rule of Part 14."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 15", font_size=34, color=GREY_B), label(r"The Other Senses", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"sound in physics' units, \ and the decibel as Fechner's law in engineering",
            r"the cochlea as a bank of filters, \ masking, \ and pitch computed by autocorrelation",
            r"where a sound is: \ time differences between the ears, \ and a circuit that reads them",
            r"scenes, \ speech and music: \ grouping, \ categories, \ the McGurk effect, \ consonance",
            r"touch, \ the body's position, \ pain and its gate, \ smell, \ taste and balance",
            r"hearing aids, \ codecs, \ haptics, \ and hidden losses at the frontier",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 15 of Psychology, Built: the other senses. <bookmark mark='a'/> We'll put sound in the units "
            "of physics, and meet the decibel, which is Fechner's law put to work by engineers. Then the cochlea, a "
            "bank of filters, masking, and the computation that finds a missing fundamental. Then where a sound is, "
            "from tiny time differences between the ears, and a circuit that reads them. Then scenes, speech and "
            "music: how sounds are grouped, why speech sounds fall into categories, a voice changed by a face, and why "
            "some chords sound rough. Then the body: touch, the sense of position, pain and its gate, smell, taste and "
            "balance. And at the end, hearing aids and implants, the codecs that compress your music, haptics, and "
            "hearing losses that a standard test can't see."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=26.0)
        self.clear_scene()
