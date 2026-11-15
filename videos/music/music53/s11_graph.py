from __future__ import annotations

import numpy as np

from videos.music.music53.common import *  # noqa: F403


def node(t, col, w=2.1):
    return VGroup(RoundedRectangle(width=w, height=0.7, corner_radius=0.12, stroke_color=col), label(t, font_size=17, color=col)).arrange(ORIGIN)


class Graph(SoundScene):
    def construct(self):
        chapter(self, 10, r"The graph, \ plug-ins and delay compensation", r"What happens when one path is late?")
        self.dag()
        self.plugins()
        self.parallel()
        self.heard()
        self.comb()
        self.freeze()

    # ------------------------------------------------------------------
    def dag(self):
        src = VGroup(node(r"drums", EAR), node(r"bass", BLUE), node(r"lead", TUNE)).arrange(DOWN, buff=0.5).move_to(LEFT * 4.6)
        fx = VGroup(node(r"compressor", GREY_A), node(r"filter", GREY_A), node(r"delay", GREY_A)).arrange(DOWN, buff=0.5).move_to(LEFT * 1.4)
        rev = node(r"reverb bus", GREY_A).move_to(RIGHT * 1.6 + DOWN * 1.2)
        mixn = node(r"mix", WHITE).move_to(RIGHT * 1.6 + UP * 0.6)
        out = node(r"out", WHITE, w=1.4).move_to(RIGHT * 4.4 + UP * 0.6)
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=2) for a, b in zip(src, fx)],
                     *[Arrow(f.get_right(), mixn.get_left(), buff=0.06, color=GREY_B, stroke_width=2) for f in fx],
                     Arrow(fx[2].get_right(), rev.get_left(), buff=0.06, color=GREY_B, stroke_width=2),
                     Arrow(rev.get_top(), mixn.get_bottom(), buff=0.06, color=GREY_B, stroke_width=2),
                     Arrow(mixn.get_right(), out.get_left(), buff=0.06, color=GREY_B, stroke_width=2))
        notes = VGroup(label(r"a directed graph with no cycles: \ each node runs once a block, \ after everything feeding it", font_size=18, color=WHITE),
                       label(r"the engine sorts the nodes \ (a topological order) \ and runs them in that order, \ every block", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        head = label(r"the processing graph", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Inside the engine, a session is a graph. <bookmark mark='a'/> Sources, the tracks; effects on each; buses that "
            "gather them; the mix; the output. <bookmark mark='b'/> It is a directed graph with no cycles, so every node can run "
            "once per block after everything that feeds it: the engine sorts the nodes, a topological order, and runs them in "
            "that order, every block."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(src, fx, rev, mixn, out), 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(src), FadeIn(fx), FadeIn(rev), FadeIn(mixn), FadeIn(out), LaggedStart(*[Create(a_) for a_ in arr], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plugins(self):
        items = [
            (r"a plug-in: \ a node written by someone else, \ loaded into the host's graph", WHITE),
            (r"1996: \ Steinberg's VST; \ then Apple's Audio Units, \ Avid's AAX, \ and the open CLAP \ (2022)", WHITE),
            (r"the contract: \ process this block, \ in place, \ before the deadline; \ report your latency", WHITE),
            (r"a look-ahead limiter \ (Part 50) \ must see the future: \ it delays its output by its look-ahead", TUNE),
            (r"and a delayed path in a graph of parallel paths is a problem", GREY_A),
        ]
        rows_scene(self, r"plug-ins", items,
                   "Many nodes come from elsewhere. <bookmark mark='b'/> A plug-in is a node written by someone else and loaded into "
                   "the host's graph. <bookmark mark='c'/> Steinberg's VST came in 1996, then Apple's Audio Units, Avid's AAX and, in "
                   "2022, the open CLAP. <bookmark mark='d'/> The contract is the same: process this block, in place, before the "
                   "deadline, and report your latency. <bookmark mark='e'/> A look-ahead limiter, from Part 50, must see the future, "
                   "so it delays its output by its look-ahead. <bookmark mark='f'/> And a delayed path in a graph of parallel paths "
                   "is a problem.", marks="bcdef")

    # ------------------------------------------------------------------
    def parallel(self):
        d = load("pdc")
        srcn = node(r"drums", EAR).move_to(LEFT * 4.4 + UP * 0.2)
        dry = node(r"dry", GREY_A).move_to(LEFT * 0.6 + UP * 1.2)
        lim = node(rf"limiter, \ {d['latency_ms']:.0f} ms late", TUNE, w=3.0).move_to(LEFT * 0.6 + DOWN * 0.8)
        mixn = node(r"mix", WHITE).move_to(RIGHT * 3.4 + UP * 0.2)
        arr = VGroup(Arrow(srcn.get_right(), dry.get_left(), buff=0.06, color=GREY_B), Arrow(srcn.get_right(), lim.get_left(), buff=0.06, color=GREY_B),
                     Arrow(dry.get_right(), mixn.get_left(), buff=0.06, color=GREY_B), Arrow(lim.get_right(), mixn.get_left(), buff=0.06, color=GREY_B))
        comp = node(rf"delay {d['latency_samples']} samples", BLUE, w=3.0).move_to(LEFT * 0.6 + UP * 2.4)
        notes = VGroup(label(r"parallel compression: \ the dry drums plus a squashed copy, \ for weight without losing the hits", font_size=17, color=WHITE),
                       label(r"the squashed copy arrives 5 ms late; \ the host must delay the dry path to match", font_size=17, color=EAR),
                       label(r"plug-in delay compensation: \ every path delayed to the slowest", font_size=17, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        head = label(r"two paths, \ one late", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the problem in its commonest form. <bookmark mark='a'/> Parallel compression: the dry drums plus a heavily "
            "squashed copy, for weight without losing the hits. <bookmark mark='b'/> The squashing is done by a look-ahead "
            f"limiter whose output arrives {say(d['latency_ms'])} milliseconds late. <bookmark mark='c'/> Unless the host delays "
            f"the dry path by the same {say(d['latency_samples'])} samples, the two copies meet misaligned. Hosts do this "
            "automatically, plug-in delay compensation, delaying every path to match the slowest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(srcn), FadeIn(dry), FadeIn(lim), FadeIn(mixn), FadeIn(arr))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), Indicate(lim, color=TUNE, scale_factor=1.05))
            vo.wait_until("c")
            self.play(FadeIn(comp), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("pdc")
        c = clip("pdc.two")
        cells = choice_boxes([r"dry path not delayed", r"compensated"], width=4.0, buff=1.0, colors=[EAR, TUNE]).move_to(UP * 0.4)
        cap = label(r"a drum loop from Part 51's circuits, \ plus its copy through a 5 ms look-ahead limiter", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"delay compensation, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear it: the loop with the dry path not delayed, then compensated."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"late, \ then aligned", kind="synthesized", detail=r"Part 51's drum circuits", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["late"], st["aligned"] - 0.3, buff=0.08)
            pulse(snd, cells[1], st["aligned"], c.duration, buff=0.08)
        with self.voiceover(
            "Misaligned, every hit has a flam, a doubled attack, and the sustained parts sound hollow and phasey. Aligned, the "
            "two copies fuse into one heavier drum."
        ):
            self.play(Indicate(cells[1], color=TUNE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def comb(self):
        d = load("pdc")
        f = np.array(d["f"])
        ax = logf_axes(width=9.0, height=3.0, flo=20, fhi=20000, ylo=-25, yhi=8, center=DOWN * 0.3)
        cv = curve(f, np.maximum(d["H_db"], -25), ax.to, color=EAR, width=2.5)
        notch = VGroup(*[DashedLine(ax.to(k * d["notch_hz"], -25), ax.to(k * d["notch_hz"], 8), color=GREY_D, stroke_width=1) for k in (1, 3, 5, 7, 9)])
        nl = label(rf"notches at {d['notch_hz']:.0f}, \ {3 * d['notch_hz']:.0f}, \ {5 * d['notch_hz']:.0f} Hz \ldots", font_size=16, color=GREY_A).to_edge(UP, buff=1.0)
        note = label(r"the sum of a sound and a copy 5 ms late: \ a comb filter \ (Part 49), \ a notch every 200 Hz from 100", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"why it sounded hollow", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Why hollow? <bookmark mark='a'/> A sound plus a copy five milliseconds late is Part 49's comb filter: wherever the "
            "delay is half a period the two cancel, at a hundred hertz, three hundred, five hundred, every two hundred hertz "
            "up the spectrum. <bookmark mark='b'/> Delay compensation removes the comb by removing the delay. One sample of "
            "bookkeeping in the engine is the difference between a mix and a mess."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(notch))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(nl), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def freeze(self):
        items = [
            (r"when the graph is too heavy for the deadline, \ the workstation renders a track offline, \ freezing it", WHITE),
            (r"offline there is no deadline: \ the same engine runs as fast or as slow as it needs", WHITE),
            (r"which is why offline and block renders must match exactly, \ as ours do", WHITE),
            (r"bouncing renders the whole mix to a file the same way", WHITE),
            (r"real time is a promise about when; \ offline rendering keeps the promise about what", TUNE),
        ]
        rows_scene(self, r"freezing and bouncing", items,
                   "One more trick makes heavy sessions possible. <bookmark mark='b'/> When the graph is too heavy for the deadline, "
                   "the workstation renders a track offline, freezing it into audio. <bookmark mark='c'/> Offline there is no "
                   "deadline: the same engine runs as fast or as slow as it needs. <bookmark mark='d'/> That is why offline and "
                   "block renders must match exactly, as ours do. <bookmark mark='e'/> Bouncing renders the whole mix to a file the "
                   "same way. <bookmark mark='f'/> Real time is a promise about when; offline rendering keeps the promise about "
                   "what.", marks="bcdef")
