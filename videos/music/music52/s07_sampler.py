from __future__ import annotations

import numpy as np

from videos.music.music52.common import *  # noqa: F403


class Sampler(SoundScene):
    def construct(self):
        chapter(self, 6, r"Samplers", r"Why not just record every note?")
        self.history()
        self.quiz()
        self.why()
        self.zones()
        self.memory()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"1963: \ the Mellotron: \ a strip of tape behind every key, \ eight seconds long", WHITE),
            (r"1979: \ the Fairlight CMI samples into memory; \ 1981: \ the E-mu Emulator; \ then Akai's samplers for hip-hop \ (Part 40)", WHITE),
            (r"one recording, \ read faster or slower, \ plays every pitch: \ resampling \ (Part 50)", WHITE),
            (r"the catch: \ faster means shorter, \ and every resonance moves with the pitch", TUNE),
            (r"a voice read faster becomes a chipmunk; \ a piano read slower becomes a different, \ bigger piano", GREY_A),
        ]
        rows_scene(self, r"recordings as instruments", items,
                   "The plainest way to make an instrument's sound is to record it. <bookmark mark='b'/> In 1963 the Mellotron put a "
                   "strip of tape behind every key, eight seconds long. <bookmark mark='c'/> In 1979 the Fairlight sampled into "
                   "memory, in 1981 the Emulator, and then came Akai's samplers, the backbone of hip-hop in Part 40. "
                   "<bookmark mark='d'/> One recording, read faster or slower, plays every pitch: resampling, from Part 50. "
                   "<bookmark mark='e'/> The catch: faster means shorter, and every resonance moves with the pitch. "
                   "<bookmark mark='f'/> A voice read faster becomes a chipmunk; a piano read slower becomes a different, bigger "
                   "piano.", marks="bcdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("sampler")
        c = clip("sampler.four")
        card = listen_card(r"Middle C on Part 7's piano, \ recorded once, \ then played two octaves down and two octaves up. \ After each, \ "
                           r"the piano computed at that note. \ Listen for what the recording gets wrong.", width=10.4)
        with self.voiceover(
            "Hear it. Middle C on Part 7's piano, recorded once, then played back two octaves down; then the piano computed at "
            "that note. Then the same recording two octaves up, and the piano computed there. Listen for what the recording "
            "gets wrong."
        ):
            self.play(FadeIn(card))
        self.wait(0.6)
        names = ["sample36", "real36", "sample84", "real84"]
        cells = choice_boxes([r"recording, \ C2", r"piano, \ C2", r"recording, \ C6", r"piano, \ C6"], width=2.7, buff=0.35, size=19,
                             colors=[EAR, TUNE, EAR, TUNE]).move_to(UP * 0.5)
        self.play(FadeOut(card), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one recording, \ four octaves", kind="physical model", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        du = d["durations"]
        res = VGroup(label(rf"read 4 times slower: \ the note lasts {du['36']:.1f} s, \ its hammer knock a dull thud", font_size=18, color=EAR),
                     label(rf"read 4 times faster: \ {du['84']:.2f} s, \ a short, \ toy-like plink", font_size=18, color=EAR)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.5)
        with self.voiceover(
            "Two octaves down, the recording is slow and dark: the hammer's knock becomes a dull thud and the decay lasts "
            f"{say(du['36'], 1)} seconds, where the low C computed directly rings with its own, brighter attack. Two octaves up it lasts "
            f"{say(du['84'], 2)} seconds, a toy plink, where the high C computed directly is short but crisp. One recording cannot be an "
            "instrument's whole range."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"reading faster scales every frequency: \ harmonics, \ but also the body's resonances and the attack's noise", WHITE),
            (r"real instruments keep their resonances fixed while the notes move: \ the source moves, \ the filter stays \ (Part 8)", WHITE),
            (r"and real decay times change with pitch in their own way, \ not in proportion", WHITE),
            (r"so within a few semitones resampling is fine; \ over octaves it is a different instrument", WHITE),
            (r"the cure is brute force: \ record more", TUNE),
        ]
        rows_scene(self, r"why one recording is not enough", items,
                   "Why does it fail? <bookmark mark='b'/> Reading faster scales every frequency: the harmonics, but also the body's resonances and the attack's noise. <bookmark mark='c'/> Many body resonances remain approximately fixed while played pitch changes; the source moves, the filter stays, as Part 8 put it. <bookmark mark='d'/> And real decay times change with pitch in their own way, not in proportion. <bookmark mark='e'/> So within a few semitones resampling is fine; over octaves it is a different instrument. <bookmark mark='f'/> The cure is brute force: record more.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def zones(self):
        keys = VGroup()
        for i in range(36):
            keys.add(Rectangle(width=0.3, height=1.2, stroke_color=GREY_D, stroke_width=1, fill_color=WHITE, fill_opacity=0.12))
        keys.arrange(RIGHT, buff=0.02).move_to(UP * 0.8)
        zones = VGroup()
        for z in range(9):
            a, b = keys[4 * z], keys[min(4 * z + 3, 35)]
            col = [TUNE, BLUE, EAR][z % 3]
            zones.add(VGroup(Rectangle(width=b.get_right()[0] - a.get_left()[0], height=0.3, stroke_width=0, fill_color=col, fill_opacity=0.7).next_to(VGroup(a, b), DOWN, buff=0.1).align_to(a, LEFT),
                             Dot(keys[4 * z + 1].get_center() + DOWN * 0.3, radius=0.06, color=col)))
        layers = VGroup(*[Rectangle(width=keys.width, height=0.22, stroke_width=0, fill_color=interpolate_color(ManimColor(BLUE), ManimColor(EAR), j / 7), fill_opacity=0.6) for j in range(8)]).arrange(DOWN, buff=0.04).next_to(zones, DOWN, buff=0.4)
        ll = label(r"velocity layers: \ the same note recorded soft to hard", font_size=16, color=GREY_A).next_to(layers, DOWN, buff=0.15)
        zl = label(r"zones: \ each recording stretched over only a few keys", font_size=16, color=GREY_A).next_to(zones, UP, buff=1.55)
        head = label(r"multisampling", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Brute force has a name: multisampling. <bookmark mark='a'/> Record a note every few semitones and stretch each "
            "over only its own small zone of keys, so no recording moves far. <bookmark mark='b'/> Then record each note at "
            "several strengths, velocity layers, because a piano struck hard is not a loud piano struck softly: it is brighter, "
            "as Part 7 measured. Add the release of each key, the pedal's resonance and the hammer's noise, all as separate "
            "recordings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(keys))
            vo.wait_until("a")
            self.play(FadeIn(zones), FadeIn(zl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in layers], lag_ratio=0.15), FadeIn(ll), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory(self):
        d = load("sampler")
        lines = VGroup(
            MathTex(r"88 \text{ keys} \times 8 \text{ layers} \times 2 \text{ channels} \times 20 \text{ s} \times 48{,}000 \times 3 \text{ bytes}", font_size=32),
            MathTex(rf"\approx {d['library_gb']:.1f} \text{{ GB}}", font_size=40),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.6)
        notes = VGroup(label(r"one recorded grand piano, \ before pedal, \ release and room recordings: \ libraries run to tens of gigabytes", font_size=18, color=WHITE),
                       label(r"a physical model of the same piano is a few kilobytes of numbers, \ and a great deal of arithmetic", font_size=18, color=TUNE),
                       label(r"samplers trade arithmetic for memory; \ physical models trade memory for arithmetic", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.7)
        head = label(r"what brute force costs", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "What does brute force cost? <bookmark mark='a'/> Eighty-eight keys, eight layers, stereo, twenty seconds each, "
            f"at forty-eight kilohertz and three bytes a sample: about {say(d['library_gb'], 1)} gigabytes, before the pedal, "
            "release and room recordings that real libraries add, which run to tens of gigabytes. <bookmark mark='b'/> A "
            "physical model of the same piano is a few kilobytes of numbers, and a great deal of arithmetic. Samplers trade "
            "arithmetic for memory; physical models trade memory for arithmetic. The rest of this part is the second trade."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(lines), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1:]))
        self.wait(0.4)
        self.clear_scene()
