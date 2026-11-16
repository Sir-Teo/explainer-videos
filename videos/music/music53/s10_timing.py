from __future__ import annotations

import numpy as np

from videos.music.music53.common import *  # noqa: F403


class Timing(SoundScene):
    def construct(self):
        chapter(self, 9, r"Timing inside a block", r"Where in the block does a note begin?")
        self.snap()
        self.heard()
        self.budget()
        self.accurate()

    # ------------------------------------------------------------------
    def snap(self):
        d = load("timing")
        err = np.array(d["err_ms"])
        ax = frame_axes(width=10.0, height=2.8, xlo=-0.5, xhi=len(err) - 0.5, ylo=0, yhi=d["block_ms"] * 1.05, center=DOWN * 0.3)
        st = stems(np.arange(len(err)), err, ax.to, color=EAR, r=0.05)
        lim = DashedLine(ax.to(-0.5, d["block_ms"]), ax.to(len(err) - 0.5, d["block_ms"]), color=GREY_A, stroke_width=1.5)
        ll = label(rf"one block: \ {d['block_ms']:.1f} ms", font_size=15, color=GREY_A).next_to(lim, UP, buff=0.08).align_to(lim, RIGHT)
        xl = label(r"the 32 hi-hats in order", font_size=15, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"how early each is played, \ ms", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        note = label(rf"snapped to 1024-sample blocks: \ up to {d['max_ms']:.0f} ms early, \ spread {d['sd_ms']:.1f} ms", font_size=18, color=WHITE).to_edge(UP, buff=1.0)
        head = label(r"a sequencer that looks at the clock once a block", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A lazy engine starts each note at the beginning of the block it falls in. <bookmark mark='a'/> With blocks of a "
            f"thousand and twenty-four samples, {say(d['block_ms'], 1)} milliseconds, sixteenth-note hi-hats at a hundred and "
            f"twenty beats a minute land up to {say(d['max_ms'])} milliseconds early, by a different amount each time, because "
            "the beat and the blocks do not line up. Our engine instead starts every note on its own sample, inside the block."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(lim), FadeIn(ll), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(st), FadeIn(note), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("timing")
        c = clip("timing.two")
        card = listen_card(r"Sixteenth-note hi-hats over a kick, \ twice. \ Once every hit is placed to the sample; \ once every hit is moved "
                           r"to the start of its block. \ Which was moved?", width=9.8)
        with self.voiceover(
            "Your turn. Sixteenth-note hi-hats over a kick, twice. Once every hit is placed to the sample; once every hit is "
            "moved to the start of its block. Which was moved?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one groove, \ twice", kind="synthesized", detail=r"hats and kick", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["exact"], st["snapped"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["snapped"], c.duration, buff=0.08)
        with self.voiceover(
            "The second. Snapped to blocks, the hats limp: some pairs too close, some too far, a groove that stumbles. Placed to "
            "the sample they are even. Ensemble players align within a few tens of milliseconds and hear far less than that in a "
            "steady pulse; an engine has no excuse to add its own."
        ):
            self.play(boxes[1][0].animate.set_stroke(EAR, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def budget(self):
        items = [
            (r"latency adds up: \ the controller, \ the cable or USB, \ the input buffer, \ the engine's block, \ the output buffer, \ the converter", WHITE),
            (r"a player feels a delay above roughly ten milliseconds between the key and the sound", WHITE),
            (r"sound in air: \ about 3 ms a metre; \ a pianist hears the piano a few milliseconds late anyway", WHITE),
            (r"the budget is spent on the block size: \ small blocks, \ low latency, \ heavy load", WHITE),
            (r"and every plug-in that looks ahead adds its own latency", TUNE),
        ]
        rows_scene(self, r"the latency budget", items,
                   "Timing has a second side: latency. <bookmark mark='b'/> It adds up along the chain: the controller, the cable or USB, the input buffer, the engine's block, the output buffer, the converter. <bookmark mark='c'/> Latency sensitivity varies with player, instrument and task; roughly ten milliseconds is a useful design target, not a universal threshold between the key and the sound. <bookmark mark='d'/> Sound in air takes about three milliseconds a metre, so a pianist hears the piano a few milliseconds late anyway. <bookmark mark='e'/> The budget is spent mostly on the block size: small blocks, low latency, heavy load. <bookmark mark='f'/> And every plug-in that looks ahead adds its own latency.", marks="bcdef")

    # ------------------------------------------------------------------
    def accurate(self):
        blocks = VGroup(*[Rectangle(width=2.4, height=0.8, stroke_color=GREY_B, stroke_width=1.5) for _ in range(4)]).arrange(RIGHT, buff=0.0).move_to(UP * 0.6)
        bl = VGroup(*[label(rf"block {i}", font_size=14, color=GREY_A).next_to(b, UP, buff=0.1) for i, b in enumerate(blocks)])
        ev = Dot(blocks[1].get_left() + RIGHT * 1.5, radius=0.1, color=EAR)
        el = label(r"a note due at sample 1,700", font_size=15, color=EAR).next_to(ev, DOWN, buff=0.5)
        off = DoubleArrow(blocks[1].get_left() + DOWN * 0.25, blocks[1].get_left() + RIGHT * 1.5 + DOWN * 0.25, buff=0.0, color=TUNE, stroke_width=2, tip_length=0.12)
        ol = label(r"offset 676 into block 1 \ (1,700 $-$ 1,024)", font_size=14, color=TUNE).next_to(off, DOWN, buff=0.1)
        steps = VGroup(label(r"1. \ at the start of each block, \ take the events due before its end", font_size=17, color=WHITE),
                       label(r"2. \ for each, \ compute its offset inside the block", font_size=17, color=WHITE),
                       label(r"3. \ run the voice from that sample, \ not from the block's start", font_size=17, color=WHITE),
                       label(r"live events need timing information: \ host arrival times or transport-specific timestamps", font_size=17, color=TUNE)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(DOWN, buff=0.35)
        head = label(r"sample-accurate scheduling", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The cure for block timing is simple. <bookmark mark='a'/> At the start of each block, take the events due before its end. <bookmark mark='b'/> For each, compute its offset inside the block: a note due at sample seventeen hundred falls six hundred and seventy-six samples into the second block of a thousand and twenty-four. <bookmark mark='c'/> Then run that voice from that sample, not from the block's start. <bookmark mark='d'/> For notes played live, the engine needs to know when each message was sent, so incoming MIDI needs timestamps; the host can timestamp arrivals; timestamp support depends on the transport and protocol, and ordinary USB MIDI 1.0 packets do not carry a per-note timestamp."
        ) as vo:
            self.play(FadeIn(head), FadeIn(blocks), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(ev), FadeIn(el), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(GrowFromCenter(off), FadeIn(ol), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
        self.wait(0.4)
        self.clear_scene()
