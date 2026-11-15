from __future__ import annotations

import numpy as np

from videos.music.music54.common import *  # noqa: F403


class Headphones(SoundScene):
    def construct(self):
        chapter(self, 10, r"Headphones and noise cancelling", r"Can sound be cancelled with more sound?")
        self.phones()
        self.idea()
        self.fxlms()
        self.bands()
        self.modes()
        self.heard()

    # ------------------------------------------------------------------
    def phones(self):
        items = [
            (r"a headphone is a tiny loudspeaker in a tiny box: \ the ear canal and the cup", WHITE),
            (r"sealed to the head, \ the cup is a pressure chamber: \ bass needs only a small motion", WHITE),
            (r"the outer ear's resonances, \ which a loudspeaker's sound meets on its way in, \ are bypassed: \ tuning curves restore them", WHITE),
            (r"no room either: \ the sound is inside the head unless it is processed \ (binaural, \ Part 55)", WHITE),
            (r"and the cup lets in the world's noise below a few hundred hertz", TUNE),
        ]
        rows_scene(self, r"a loudspeaker on the ear", items,
                   "Headphones are loudspeakers in miniature. <bookmark mark='b'/> Sealed to the head, the cup is a pressure chamber, "
                   "so bass needs only a tiny motion. <bookmark mark='c'/> The outer ear's own resonances, which a loudspeaker's sound "
                   "meets on its way in, are bypassed, and designers tune the response to restore them. <bookmark mark='d'/> There is "
                   "no room either: the sound sits inside the head unless it is processed, which is Part 55's binaural sound. "
                   "<bookmark mark='e'/> And the cup lets in the world's noise below a few hundred hertz.", marks="bcde")

    # ------------------------------------------------------------------
    def idea(self):
        ax = frame_axes(width=9.0, height=1.2, xlo=0, xhi=4 * np.pi, ylo=-1.2, yhi=1.2, center=UP * 1.4)
        bx = frame_axes(width=9.0, height=1.2, xlo=0, xhi=4 * np.pi, ylo=-1.2, yhi=1.2, center=DOWN * 0.2)
        cx = frame_axes(width=9.0, height=1.2, xlo=0, xhi=4 * np.pi, ylo=-1.2, yhi=1.2, center=DOWN * 1.8)
        t = np.linspace(0, 4 * np.pi, 200)
        n = curve(t, np.sin(t), ax.to, color=EAR, width=3)
        a = curve(t, -0.95 * np.sin(t), bx.to, color=BLUE, width=3)
        s = curve(t, 0.05 * np.sin(t), cx.to, color=TUNE, width=3)
        labs = VGroup(label(r"noise at the ear", font_size=16, color=EAR).next_to(ax, LEFT, buff=0.2), label(r"anti-noise", font_size=16, color=BLUE).next_to(bx, LEFT, buff=0.2),
                      label(r"what is left", font_size=16, color=TUNE).next_to(cx, LEFT, buff=0.2))
        note = label(r"Paul Lueg's patent \ (1936); \ aviation headsets \ (1989); \ now in every pair of earbuds", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.3)
        head = label(r"cancelling sound with sound", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "So fight noise with noise. <bookmark mark='a'/> Measure the noise, <bookmark mark='b'/> play its mirror image "
            "through the headphone, <bookmark mark='c'/> and at the ear the two cancel. Paul Lueg patented the idea in 1936; it "
            "reached aviation headsets in 1989; now it is in every pair of earbuds. The hard part is that the anti-noise must "
            "be exact at the eardrum, through a path that changes every time the headphones move."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(bx), FadeIn(cx))
            vo.wait_until("a")
            self.play(Create(n), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(Create(a), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(Create(s), FadeIn(labs[2]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fxlms(self):
        blocks = VGroup()
        for t, col, pos in ((r"outer mic", EAR, LEFT * 5.0 + UP * 0.8), (r"filter $w$", TUNE, LEFT * 1.6 + UP * 0.8), (r"speaker $\to$ ear: \ $S$", BLUE, RIGHT * 2.0 + UP * 0.8),
                            (r"ear mic: \ error $e$", WHITE, RIGHT * 5.0 + UP * 0.8), (r"model $\hat S$", GREY_A, LEFT * 1.6 + DOWN * 1.0)):
            blocks.add(VGroup(RoundedRectangle(width=2.4, height=0.8, corner_radius=0.12, stroke_color=col), label(t, font_size=16, color=col)).arrange(ORIGIN).move_to(pos))
        arr = VGroup(Arrow(blocks[0].get_right(), blocks[1].get_left(), buff=0.06, color=GREY_B), Arrow(blocks[1].get_right(), blocks[2].get_left(), buff=0.06, color=GREY_B),
                     Arrow(blocks[2].get_right(), blocks[3].get_left(), buff=0.06, color=GREY_B),
                     Arrow(blocks[0].get_bottom(), blocks[4].get_left(), buff=0.06, color=GREY_B, path_arc=0.6),
                     Arrow(blocks[4].get_right(), blocks[1].get_bottom() + RIGHT * 0.3, buff=0.06, color=GREY_B, path_arc=0.6),
                     Arrow(blocks[3].get_bottom(), blocks[1].get_bottom() + RIGHT * 0.6, buff=0.06, color=EAR, path_arc=-0.5))
        eq = MathTex(r"w \leftarrow w - \mu\, e\, (\hat S * x)", font_size=34).to_edge(DOWN, buff=1.0)
        note = label(r"filtered-x LMS: \ nudge every tap of $w$ against the error, \ using the outer signal as the speaker-to-ear path will change it", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"an adaptive canceller", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Our canceller adapts. <bookmark mark='a'/> An outer microphone hears the noise early; a filter shapes it into "
            "anti-noise; the speaker plays it; a microphone inside the cup hears what is left, the error. "
            "<bookmark mark='b'/> After every sample, each tap of the filter is nudged against the error, by an amount "
            "proportional to the outer signal passed through a model of the speaker-to-ear path. That is the filtered-x LMS "
            "algorithm, from Bernard Widrow's least-mean-squares rule of 1960, and it keeps adjusting as the headphones move."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(blocks, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(blocks), LaggedStart(*[Create(a) for a in arr], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(eq), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bands(self):
        d = load("anc")
        bars = VGroup()
        for i, b in enumerate(d["bands"]):
            h = 3.2 * (-b["atten"]) / 40
            bar = Rectangle(width=1.1, height=max(h, 0.03), stroke_width=0, fill_color=TUNE if b["atten"] < -10 else GREY_A, fill_opacity=0.85)
            bar.move_to([-4.0 + 2.0 * i, 1.3 - max(h, 0.03) / 2, 0])
            bars.add(VGroup(bar, label(rf"{b['lo']}--{b['hi']} Hz", font_size=15, color=GREY_A).next_to([-4.0 + 2.0 * i, 1.3, 0], UP, buff=0.12),
                            label(rf"{b['atten']:.0f} dB", font_size=17, color=WHITE).next_to(bar, DOWN, buff=0.1)))
        base = Line([-5.0, 1.3, 0], [5.0, 1.3, 0], color=GREY_B, stroke_width=1.5)
        note = label(r"the speaker-to-ear path cannot make highs, \ and its delay outruns them: \ active cancelling is for low frequencies; \ the cup's seal does the rest", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"how much it cancels, \ by band", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        b = d["bands"]
        with self.voiceover(
            "Simulate an aircraft cabin: a drone at ninety-two hertz and its harmonics, rumble, and a little hiss. "
            f"<bookmark mark='a'/> After the canceller adapts, the lowest band falls {say(-b[0]['atten'])} decibels, the next "
            f"{say(-b[1]['atten'])}, and up to a kilohertz {say(-b[2]['atten'])}. <bookmark mark='b'/> Above that, almost nothing: "
            "the anti-noise speaker's path cannot make high frequencies, and its delay outruns them. Active cancelling is for "
            "low frequencies; the cup's seal does the rest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(base), FadeIn(ghost(bars, 0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(bb) for bb in bars[:3]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(bars[3:]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("anc")
        c = clip("anc.two")
        cells = choice_boxes([r"canceller off", r"canceller on"], width=3.6, buff=1.0, colors=[EAR, TUNE]).move_to(UP * 0.4)
        cap = label(r"the cabin drone at the ear, \ with a voice singing over it", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"a cabin, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the cabin at the ear, with a voice singing over it: the canceller off, then on."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"off, \ then on", kind="synthesized", detail=r"a simulated canceller", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["off"], st["on"] - 0.3, buff=0.08)
            pulse(snd, cells[1], st["on"], c.duration, buff=0.08)
        with self.voiceover(
            "With the canceller on, the drone and rumble drop away and the voice stands clear, with only a thin hiss left, the "
            "part the canceller cannot reach."
        ):
            self.play(Indicate(cells[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modes(self):
        items = [
            (r"feedforward: \ the outer microphone hears the noise early, \ as in our simulation", WHITE),
            (r"feedback: \ a microphone inside the cup cancels whatever arrives, \ including what the outer one missed", WHITE),
            (r"most headphones combine both", WHITE),
            (r"transparency mode runs it backwards: \ the outer microphones are played in, \ to hear the world with the cups on", WHITE),
            (r"cancelling only subtracts sound: \ it does not protect hearing from loud music", TUNE),
        ]
        rows_scene(self, r"feedforward, \ feedback, \ transparency", items,
                   "Real headphones use more than one scheme. <bookmark mark='b'/> Feedforward: the outer microphone hears the noise early, as in our simulation. <bookmark mark='c'/> Feedback: a microphone inside the cup cancels whatever arrives, including what the outer one missed. <bookmark mark='d'/> Most headphones combine the two. <bookmark mark='e'/> Transparency mode runs the system backwards: the outer microphones are played in, so you hear the world with the cups on. <bookmark mark='f'/> And cancelling only subtracts noise; it does not protect hearing from loud music.", marks="bcdef")
