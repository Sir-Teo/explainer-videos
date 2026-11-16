from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403


class Pitch(SoundScene):
    def construct(self):
        chapter(self, 8, r"Pitch and its illusions", r"Can a sound rise forever?")
        self.helix()
        self.octaves()
        self.bells()
        self.quiz()
        self.risset()
        self.paradox()

    # ------------------------------------------------------------------
    def helix(self):
        items = [
            (r"pitch is built by the brain from a spectrum \ (Part 4's missing fundamental)", WHITE),
            (r"two dimensions: \ height, \ which rises steadily, \ and chroma, \ which repeats every octave", WHITE),
            (r"Roger Shepard \ (1964, \ 1982): \ pitch as a helix, \ C above C above C", WHITE),
            (r"octave equivalence: \ notes an octave apart share a name in almost every musical culture", TUNE),
            (r"pull height and chroma apart, \ and pitch can go round in a circle", GREY_A),
        ]
        rows_scene(self, r"height and chroma", items,
                   "Pitch is built by the brain from a spectrum, as Part 4's missing fundamental showed. "
                   "<bookmark mark='b'/> It has two dimensions: height, which rises steadily, and chroma, which repeats every "
                   "octave. <bookmark mark='c'/> Roger Shepard drew it as a helix: C above C above C. <bookmark mark='d'/> "
                   "Octave equivalence, notes an octave apart sharing a name, is widespread but its strength and musical use vary across populations and tasks. "
                   "<bookmark mark='e'/> Pull height and chroma apart, and pitch can go round in a circle.", marks="bcde")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("shepard")
        c = clip("shepard.steps")
        card = listen_card(r"25 tones, \ each a semitone higher than the last: \ 24 steps up. \ "
                           r"Is the last tone two octaves above the first?", width=10.4)
        with self.voiceover(
            "A question for your ears. Twenty-five tones, each a semitone higher than the one before: twenty-four steps up. "
            "Is the last tone two octaves above the first?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        # the partials and the fixed bell
        x0, W = -5.5, 11.0
        octs = 9
        bell = VMobject(color=GREY_B, stroke_width=3).set_points_as_corners([[x0 + W * x / octs, -1.6 + 2.6 * np.exp(-((x - d["centre"]) ** 2) / (2 * d["sigma"] ** 2)), 0] for x in np.linspace(0, octs, 200)])
        base = Line([x0, -1.6, 0], [x0 + W, -1.6, 0], color=GREY_D)
        parts = VGroup(*[Line([0, -1.6, 0], [0, 0.0, 0], color=TUNE, stroke_width=4) for _ in range(octs)])
        lab = label(r"partials an octave apart \ (gold) \ under a bell that never moves \ (grey); \ log frequency across", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.9)
        step = d["tone"] + d["gap"]
        def upd(m, now):
            s = min(int(now / step), d["steps"] - 1)
            pc = (s * d["step_st"] / 12.0) % 1.0
            for o, ln in enumerate(m):
                x = o + pc
                a = np.exp(-((x - d["centre"]) ** 2) / (2 * d["sigma"] ** 2))
                xx = x0 + W * x / octs
                ln.put_start_and_end_on([xx, -1.6, 0], [xx, -1.6 + 2.6 * a + 0.01, 0])
        upd(parts, 0.0)
        counter = label(r"step 0", font_size=22, color=WHITE).to_edge(UP, buff=0.6)
        self.play(FadeOut(card), FadeIn(base), FadeIn(bell), FadeIn(parts), FadeIn(lab))
        with self.listen(c) as snd:
            window(snd, r"24 steps up", kind="synthesized", detail=r"Shepard tones", corner=DL, tag_corner=DR)
            snd.drive(parts, upd)
            steps_ = VGroup(*[label(rf"step {k}", font_size=22, color=WHITE).to_edge(UP, buff=0.6) for k in range(d["steps"])])
            for k, s_ in enumerate(steps_):
                snd.show(s_)
                snd.drive(s_, lambda m, now, k=k: m.set_opacity(1.0 if min(int(now / step), d["steps"] - 1) == k else 0.0))
        ans = label(r"no: \ the last tone is the first tone again", font_size=22, color=TUNE).to_edge(UP, buff=0.6)
        with self.voiceover(
            "No. The last tone is exactly the first. Each tone is a set of partials an octave apart, and their loudness is "
            "set by a bell-shaped curve that never moves. Each step slides every partial up a semitone: the ones climbing "
            "out of the top fade away while new ones fade in at the bottom. Chroma keeps rising; height never gets anywhere. "
            "Shepard built these tones in 1964, and Jean-Claude Risset made a continuous glide of the same kind."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paradox(self):
        items = [
            (r"Deutsch's tritone paradox \ (1986): \ two Shepard tones a tritone apart, \ with no height to tell them by", WHITE),
            (r"some listeners hear the pair rise, \ others fall, \ consistently, \ depending on the pitch class", WHITE),
            (r"the pattern varies with where people grew up and the speech they heard", WHITE),
            (r"pitch perception is partly learned, \ even for the most basic judgement: \ up or down", TUNE),
            (r"chapter 9: \ remembering pitch itself", GREY_A),
        ]
        rows_scene(self, r"the tritone paradox", items,
                   "Shepard tones also make a paradox. <bookmark mark='b'/> Play two of them a tritone apart, half an octave, "
                   "where there is no height to tell them by. Diana Deutsch found in 1986 that <bookmark mark='c'/> some "
                   "listeners hear the pair rise and others fall, consistently, depending on the pitch class, "
                   "<bookmark mark='d'/> and that the pattern varies with where people grew up and the speech they heard. "
                   "<bookmark mark='e'/> Even the most basic judgement, up or down, is partly learned. <bookmark mark='f'/> "
                   "Chapter nine turns to remembering pitch itself.", marks="bcdef")

    # ------------------------------------------------------------------
    def octaves(self):
        d = load("octaves")
        c = clip("octaves.two")
        head = label(r"chroma without height", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cells = VGroup(label(r"each note in a random octave", font_size=22, color=EAR), label(r"as written", font_size=22, color=TUNE)).arrange(RIGHT, buff=2.0).move_to(UP * 0.3)
        sh = VGroup(*[label(rf"{s // 12:+d}" if s else r"0", font_size=16, color=GREY_A) for s in d["shifts"]]).arrange(RIGHT, buff=0.25).next_to(cells, DOWN, buff=0.6)
        cap = label(r"octave shifts of the 14 notes", font_size=16, color=GREY_A).next_to(sh, DOWN, buff=0.15)
        with self.voiceover(
            "If chroma were all that mattered, a melody would survive having its notes moved by octaves. Hear a familiar tune "
            "with every note put in a random octave, and then as written."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(sh), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"scrambled, \ then plain", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["scrambled"], st["plain"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["plain"], c.duration, buff=0.1)
        with self.voiceover(
            "Scrambled, it is very hard to recognise, though every note has the right name. As written, it is our Tune. "
            "Diana Deutsch showed this in 1972 with Yankee Doodle: melody lives in height and contour, not in chroma alone."
        ):
            self.play(Indicate(cells[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def risset(self):
        d = load("risset")
        c = clip("risset.glide")
        x0, W = -5.5, 11.0
        base = Line([x0, -1.6, 0], [x0 + W, -1.6, 0], color=GREY_D)
        bell = VMobject(color=GREY_B, stroke_width=3).set_points_as_corners([[x0 + W * x / 9, -1.6 + 2.6 * np.exp(-((x - 4.5) ** 2) / (2 * 1.5 ** 2)), 0] for x in np.linspace(0, 9, 200)])
        parts = VGroup(*[Line([0, -1.6, 0], [0, 0.0, 0], color=TUNE, stroke_width=4) for _ in range(9)])
        def upd(m, now):
            for o, ln in enumerate(m):
                x = (o + now / d["octave_s"]) % 9.0
                a = np.exp(-((x - 4.5) ** 2) / (2 * 1.5 ** 2))
                xx = x0 + W * x / 9
                ln.put_start_and_end_on([xx, -1.6, 0], [xx, -1.6 + 2.6 * a + 0.01, 0])
        upd(parts, 0.0)
        head = label(r"Risset's endless glide", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover("Jean-Claude Risset made the same trick continuous: a glide that rises for ever."):
            self.play(FadeIn(head), FadeIn(base), FadeIn(bell), FadeIn(parts))
        with self.listen(c) as snd:
            window(snd, r"an endless glide", kind="synthesized", detail=r"Shepard-Risset glissando", corner=DL, tag_corner=DR)
            snd.drive(parts, upd)
        with self.voiceover("Twelve seconds of rising, two octaves' worth, and it ends where it began. Film composers use the effect to build tension that never resolves."):
            self.play(Indicate(bell))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bells(self):
        items = [
            (r"inharmonic sounds have pitches too: \ a bell's strike note is often not any of its partials \ (Part 9)", WHITE),
            (r"the brain fits a harmonic template to whatever partials it finds, \ and reports the best fit", WHITE),
            (r"for a bell the best fit can sit an octave below the loudest partial, \ or between two", WHITE),
            (r"so pitch is an inference, \ like every grouping in this part", TUNE),
            (r"and sometimes two inferences compete: \ some listeners hear a bell's pitch an octave from others", GREY_A),
        ]
        rows_scene(self, r"the pitch of a bell", items,
                   "Inharmonic sounds have pitches too. <bookmark mark='b'/> A bell's strike note, Part 9 found, is often not any "
                   "of its partials. <bookmark mark='c'/> The brain fits a harmonic template to whatever partials it finds and "
                   "reports the best fit, <bookmark mark='d'/> which for a bell can sit an octave below the loudest partial, or "
                   "between two. <bookmark mark='e'/> Pitch is an inference, like every grouping in this part, "
                   "<bookmark mark='f'/> and sometimes two inferences compete: some listeners hear a bell an octave away from "
                   "others.", marks="bcdef")
