from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403


class Pv(SoundScene):
    def construct(self):
        chapter(self, 8, r"Overlap-add and the phase vocoder", r"How do you stretch a sound without changing its pitch?")
        self.ola()
        self.pv()
        self.hear()
        self.limits()
        self.extreme()
        self.uses()

    # ------------------------------------------------------------------
    def ola(self):
        items = [
            (r"overlap-add: \ cut the sound into overlapping windows, \ and lay them down further apart to stretch it", WHITE),
            (r"each window keeps its pitch; \ the whole lasts longer", WHITE),
            (r"but the pieces of a steady tone no longer line up: \ where they overlap, \ they partly cancel", WHITE),
            (r"the result warbles, \ a regular flutter at the window rate", TUNE),
            (r"the cure is to fix each frequency's phase as the windows are laid down", GREY_A),
        ]
        rows_scene(self, r"overlap-add", items,
                   "The simplest way to stretch is overlap-add. <bookmark mark='b'/> Cut the sound into overlapping windows and lay "
                   "them down further apart. <bookmark mark='c'/> Each window keeps its pitch, and the whole lasts longer. "
                   "<bookmark mark='d'/> But the pieces of a steady tone no longer line up, and where they overlap they partly "
                   "cancel. <bookmark mark='e'/> The result warbles, with a regular flutter at the window rate. "
                   "<bookmark mark='f'/> The cure is to fix each frequency's phase as the windows are laid down.", marks="bcdef")

    # ------------------------------------------------------------------
    def pv(self):
        rows_ = text_rows([
            (r"James Flanagan and Roger Golden \ (1966): \ the phase vocoder", WHITE),
            (r"transform each window \ (Part 3's short-time Fourier transform); \ keep every bin's magnitude", WHITE),
            (r"from how far each bin's phase moved between windows, \ work out its true frequency", WHITE),
            (r"then rebuild the phase so that frequency advances smoothly across the new, \ wider spacing", TUNE),
            (r"Jean Laroche and Mark Dolson \ (1999): \ lock the bins around each peak together, \ so partials stay whole", GREY_A),
        ], font_size=23)
        head = label(r"the phase vocoder", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "That is the phase vocoder. <bookmark mark='a'/> James Flanagan and Roger Golden built it at Bell Labs in 1966. "
            "<bookmark mark='b'/> Transform each window, as Part 3's short-time Fourier transform does, and keep every bin's "
            "magnitude. <bookmark mark='c'/> From how far each bin's phase moved between windows, work out its true frequency. "
            "<bookmark mark='d'/> Then rebuild the phase so that frequency advances smoothly across the new, wider spacing. "
            "<bookmark mark='e'/> Jean Laroche and Mark Dolson improved it in 1999 by locking the bins around each spectral peak "
            "together, so that each partial stays whole."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("stretch")
        c = clip("stretch.three")
        cells = VGroup()
        for k, t, w in (("original", r"the original", 2.0), ("ola", r"twice as long: \ overlap-add", 4.0), ("pv", r"twice as long: \ phase vocoder", 4.0)):
            cells.add(VGroup(Rectangle(width=w * 1.4, height=0.8, stroke_color=GREY_B, fill_color=TUNE if k == "pv" else (EAR if k == "ola" else GREY_A), fill_opacity=0.25),
                             label(t, font_size=20, color=WHITE)).arrange(ORIGIN))
        cells.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(LEFT * 0.5)
        head = label(r"stretched, \ two ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear it: the sung phrase, then twice as long by overlap-add, then twice as long by the phase vocoder."):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        keys = ["original", "ola", "pv"]
        with self.listen(c) as snd:
            window(snd, r"stretched twice", kind="synthesized", detail=r"Part 8's voice", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        with self.voiceover(
            "Overlap-add flutters, as the out-of-step windows beat against each other. The phase vocoder is smooth, though a "
            "little reverberant: its known weakness, the smearing of attacks."
        ):
            self.play(Indicate(cells[2], color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"the phase vocoder smears transients: \ a drum hit spread over a window sounds soft and phasey", WHITE),
            (r"modern stretchers detect attacks and leave them alone, \ stretching only what lies between", WHITE),
            (r"pitch shifting by spectrum: \ stretch in time, \ then resample back to the original length", WHITE),
            (r"but that moves the formants too, \ so voices need the envelope separated and kept", TUNE),
            (r"every DAW's `warp' and every karaoke key change rests on these two ideas", GREY_A),
        ]
        rows_scene(self, r"limits and uses", items,
                   "The phase vocoder has limits. <bookmark mark='b'/> It smears transients: a drum hit spread over a window sounds "
                   "soft and phasey. <bookmark mark='c'/> Modern stretchers detect attacks and leave them alone, stretching only "
                   "what lies between. <bookmark mark='d'/> To shift pitch by spectrum, stretch in time and then resample back to "
                   "the original length; <bookmark mark='e'/> but that moves the formants too, so voices need their spectral "
                   "envelope separated and kept. <bookmark mark='f'/> Every audio workstation's warp, and every karaoke key change, "
                   "rests on these two ideas.", marks="bcdef")

    # ------------------------------------------------------------------
    def extreme(self):
        items = [
            (r"stretch far enough and a sound becomes a texture: \ eight times, \ eighty, \ eight hundred", WHITE),
            (r"Paul Nasca's Paulstretch \ (2006) \ randomises each bin's phase, \ giving up the attack for a smooth wash", WHITE),
            (r"a pop song slowed 800 per cent became an ambient piece that spread online in 2010", WHITE),
            (r"Variation 50 stretches one second of the Tune to eight", TUNE),
            (r"at that scale the phase vocoder is less an effect than a microscope", GREY_A),
        ]
        rows_scene(self, r"extreme stretching", items,
                   "Stretch far enough and a sound becomes a texture: eight times, eighty, eight hundred. <bookmark mark='b'/> Paul "
                   "Nasca's Paulstretch, from 2006, randomises each bin's phase, giving up the attack for a smooth wash. "
                   "<bookmark mark='c'/> A pop song slowed eight hundred per cent became an ambient piece that spread online in "
                   "2010. <bookmark mark='d'/> Variation 50 stretches one second of the Tune to eight. <bookmark mark='e'/> At that "
                   "scale the phase vocoder is less an effect than a microscope.", marks="bcde")

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"DJ software matches the tempo of two tracks without changing their key", WHITE),
            (r"film editors fit a cue to a cut a few per cent longer or shorter \ (Part 44's hit points)", WHITE),
            (r"language learners and transcribers slow speech and music down, \ keeping the pitch", WHITE),
            (r"producers move a sampled loop to a new tempo, \ or a new key, \ independently", TUNE),
            (r"each is a careful use of the same machinery: \ analyse, \ move, \ rebuild", GREY_A),
        ]
        rows_scene(self, r"stretching at work", items,
                   "Stretching is everywhere at work. <bookmark mark='b'/> DJ software matches the tempo of two tracks without "
                   "changing their key. <bookmark mark='c'/> Film editors fit a cue to a cut a few per cent longer or shorter, the "
                   "hit points of Part 44. <bookmark mark='d'/> Language learners and transcribers slow speech and music down, keeping "
                   "the pitch. <bookmark mark='e'/> Producers move a sampled loop to a new tempo, or a new key, independently. "
                   "<bookmark mark='f'/> Each is a careful use of the same machinery: analyse, move, rebuild.", marks="bcdef")
