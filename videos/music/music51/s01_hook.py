from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.reveal()
        self.tons()
        self.module()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"The Tune's first phrase, \ twice. \ One tone was built by hand from forty sine waves. \ The other is a "
                           r"two-oscillator synthesizer patch that a computer search set to imitate it. \ Which is the original?", width=10.4)
        with self.voiceover(
            "A question for your ears. The Tune's first phrase, twice. One tone was built by hand from forty sine waves, each "
            "set to its own level. The other is a two-oscillator synthesizer patch that a computer search set to imitate it. "
            "Which is the original?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one phrase, \ twice", kind="synthesized", detail=r"sines, \ and a patch", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reveal(self):
        d = load("fit")
        f = d["f"]
        tg = np.array(d["spec"]["target"])[1::2]
        ft = np.array(d["spec"]["fit"])[1::2]
        k = np.arange(1, len(tg) + 1)
        ax = frame_axes(width=11.0, height=3.4, xlo=0, xhi=len(k) + 1, ylo=-60, yhi=0, center=DOWN * 0.4)
        a = stems(k - 0.15, tg, ax.to, color=EAR, r=0.05, base_y=-60)
        b = stems(k + 0.15, ft, ax.to, color=TUNE, r=0.05, base_y=-60)
        ticks = VGroup(*[label(str(j), font_size=14, color=GREY_A).next_to(ax.to(j, -60), DOWN, buff=0.1) for j in (1, 5, 10, 15, 20, 25, 30, 35, 40, 45) if j <= len(k)])
        yl = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (0, -20, -40, -60)])
        xl = label(r"harmonic of middle C", font_size=16, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        key = VGroup(label(r"the original: \ forty sines", font_size=18, color=EAR),
                     label(rf"the patch: \ {d['fit']['distance_db']:.1f} dB from it on average", font_size=18, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.1)
        head = label(r"the second was the original", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        bump = SurroundingRectangle(VGroup(a[2], a[4], b[2], b[4]), color=GREY_A, buff=0.12, corner_radius=0.1)
        bl = label(r"the bump the patch could not make", font_size=16, color=GREY_A).next_to(bump, UP, buff=0.1)
        with self.voiceover(
            "The second was the original. Here are the two, harmonic by harmonic, in decibels below the loudest. "
            "<bookmark mark='a'/> The original's forty sines, set by hand: falling as one over the harmonic number, with a broad "
            f"bump near eleven hundred hertz. <bookmark mark='b'/> The patch: one sawtooth through a filter with cutoff near "
            f"{say(round(d['fit']['cutoff'], -2))} hertz and a little resonance, found by trying {say(d['fit']['tried'])} settings. It "
            f"lands within {say(d['fit']['distance_db'], 1)} decibels on average. <bookmark mark='c'/> Where it misses is the bump: "
            "a low-pass filter cannot lift the third, fourth and fifth harmonics without lifting what lies below them too. Two "
            "knobs and a waveform came within a few decibels of forty hand-set sines. That economy is the idea of this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(yl), FadeIn(xl), FadeIn(ghost(a, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(Create(bump), FadeIn(bl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tons(self):
        items = [
            (r"1897: \ Thaddeus Cahill patents a way to make music from electricity and send it down wires", WHITE),
            (r"1906: \ his Telharmonium plays in New York: \ dynamos, \ one for each pitch, \ nearly 200 tons of them", WHITE),
            (r"each dynamo made a near-sine; \ a note's colour was a sum of them: \ additive synthesis", WHITE),
            (r"subscribers heard it through the telephone, \ and it bled into other people's calls", WHITE),
            (r"by 1914 the company had failed; \ no recording of it survives", GREY_A),
        ]
        rows_scene(self, r"an early electrical instrument at industrial scale", items,
                   "One early large-scale electrical instrument weighed nearly two hundred tons; it was not the first device to generate tones electrically. <bookmark mark='b'/> In 1897 Thaddeus Cahill patented a way to "
                   "make music from electricity and send it down wires. <bookmark mark='c'/> In 1906 his Telharmonium began to play "
                   "in New York: dynamos, one for each pitch, nearly two hundred tons of them, filling a floor. "
                   "<bookmark mark='d'/> Each dynamo made something close to a sine wave, and a note's colour was a sum of them: "
                   "additive synthesis, at industrial scale. <bookmark mark='e'/> Subscribers heard it through the telephone, and it "
                   "bled into other people's calls. <bookmark mark='f'/> By 1914 the company had failed, and no recording of it "
                   "survives.", marks="bcdef")

    # ------------------------------------------------------------------
    def module(self):
        items = [
            (r"1964: \ Robert Moog shows voltage-controlled modules: \ an oscillator, \ a filter, \ an amplifier, \ cords between them", WHITE),
            (r"the trick was subtraction: \ start from a wave full of harmonics and filter most of them away", WHITE),
            (r"1968: \ Wendy Carlos's \textit{Switched-On Bach}, \ every line played separately on a monophonic Moog and layered on tape", WHITE),
            (r"it became one of the best-selling classical records ever made, \ with over a million copies", TUNE),
            (r"what the Telharmonium did with tons, \ a filter did with a handful of transistors", GREY_A),
        ]
        rows_scene(self, r"sixty years later", items,
                   "Sixty years later a module did the job. <bookmark mark='b'/> In 1964 Robert Moog showed voltage-controlled "
                   "modules: an oscillator, a filter and an amplifier, with patch cords between them. <bookmark mark='c'/> The trick "
                   "was subtraction: start from a wave full of harmonics, and filter most of them away. <bookmark mark='d'/> In "
                   "1968 Wendy Carlos released Switched-On Bach, every line of Bach played separately on a monophonic Moog and "
                   "layered on tape. <bookmark mark='e'/> It became one of the best-selling classical records ever made, with over a "
                   "million copies. <bookmark mark='f'/> What the Telharmonium did with tons, a filter did with a handful of "
                   "transistors.", marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"additive synthesis, \ from dynamos to the Hammond's drawbars",
            r"subtractive synthesis, \ and why digital sawtooths alias",
            r"the ladder filter, \ and running its circuit on a computer",
            r"envelopes, \ modulation, \ pulse width, \ sync and unison",
            r"wavetables and drum circuits",
            r"fitting a patch to a sound, \ and learning to do it",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Additive synthesis, from dynamos to the Hammond organ's drawbars. <bookmark mark='b'/> "
            "Subtractive synthesis, and why a digital sawtooth aliases. <bookmark mark='c'/> The ladder filter, and how to run "
            "its circuit on a computer. <bookmark mark='d'/> Envelopes, modulation, pulse width, sync and unison. "
            "<bookmark mark='e'/> Wavetables and drum circuits. <bookmark mark='f'/> And fitting a patch to a sound, by search "
            "and by learning."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
