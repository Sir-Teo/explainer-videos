from __future__ import annotations

import numpy as np

from videos.music.music53.common import *  # noqa: F403


class Callback(SoundScene):
    def construct(self):
        chapter(self, 8, r"The audio callback", r"What does real time actually demand?")
        self.deadline()
        self.identical()
        self.costs()
        self.dropouts()
        self.rules()
        self.ring()

    # ------------------------------------------------------------------
    def deadline(self):
        blocks = VGroup(*[Rectangle(width=1.4, height=0.6, stroke_color=GREY_B, stroke_width=1.5, fill_color=TUNE, fill_opacity=0.2) for _ in range(7)]).arrange(RIGHT, buff=0.0).move_to(UP * 1.2)
        tl = label(r"the sound card's buffer: \ one block plays while the next is computed", font_size=17, color=GREY_A).next_to(blocks, UP, buff=0.25)
        work = VGroup(*[Rectangle(width=1.4 * f, height=0.4, stroke_width=0, fill_color=EAR, fill_opacity=0.7) for f in (0.3, 0.35, 0.28, 0.4, 0.33, 0.3, 0.32)])
        for w, b in zip(work, blocks):
            w.next_to(b, DOWN, buff=0.3).align_to(b, LEFT)
        wl = label(r"the computer's work on each block: \ it must finish before its block is due", font_size=17, color=EAR).next_to(work, DOWN, buff=0.3)
        eq = MathTex(r"\text{deadline} = \frac{\text{block size}}{\text{sample rate}} \qquad \frac{128}{48\,000} = 2.67\ \text{ms}", font_size=32).to_edge(DOWN, buff=0.9)
        head = label(r"a block at a time, \ against a clock", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Real time means a deadline. <bookmark mark='a'/> The sound card plays from a buffer, a block of samples at a time, "
            "and while one block plays, the computer must compute the next. Every few milliseconds the operating system calls "
            "the engine, the audio callback, and asks for exactly one block. <bookmark mark='b'/> The engine has until that "
            "block is due: the block size over the sample rate. <bookmark mark='c'/> A hundred and twenty-eight samples at "
            "forty-eight kilohertz gives two point six seven milliseconds, every time, forever."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(blocks, work), 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(blocks), FadeIn(tl))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(w, LEFT) for w in work], lag_ratio=0.15), FadeIn(wl), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(eq))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def identical(self):
        d = load("callback")
        rows = VGroup(*[VGroup(label(f"{B}", font_size=20, color=WHITE), label(r"identical" if ok else r"different", font_size=20, color=TUNE if ok else EAR))
                        for B, ok in zip(d["blocks"], d["identical"])]).arrange(DOWN, buff=0.22)
        for r in rows:
            r[0].set_x(-1.6)
            r[1].set_x(1.0)
        hdr = VGroup(label(r"block size", font_size=17, color=GREY_A).move_to([-1.6, 0, 0]), label(r"against one block of four seconds", font_size=17, color=GREY_A).move_to([1.0, 0, 0]))
        tbl = VGroup(hdr, rows).arrange(DOWN, buff=0.35).move_to(LEFT * 3.4 + DOWN * 0.2)
        side = VGroup(label(rf"{d['voices']} notes on three tracks, \ one through a look-ahead limiter", font_size=17, color=WHITE),
                      label(r"compared sample by sample: \ equal to the last bit", font_size=17, color=TUNE),
                      label(r"because every voice, \ filter and delay keeps its state between blocks, \ and every note starts on its own sample", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        side.set_width(min(side.width, 5.0)).to_edge(RIGHT, buff=0.4)
        head = label(r"blocks must not change the music", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The first rule of an engine: the block size must not change the music. <bookmark mark='a'/> Our engine plays "
            f"{say(d['voices'])} notes on three tracks, one through a look-ahead limiter, in blocks from thirty-two samples to two "
            "thousand and forty-eight, and compares each result with the whole four seconds computed in one go. "
            "<bookmark mark='b'/> Every one is identical, to the last bit, because every voice, filter and delay carries its "
            "state from block to block, and every note starts on its own sample, wherever the block boundaries fall."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(side[0]), FadeIn(ghost(rows, 0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.1), run_time=1.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[1]) for r in rows], lag_ratio=0.1), FadeIn(side[1:]), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def costs(self):
        d = load("callback")
        rows = VGroup(VGroup(label(r"block", font_size=17, color=GREY_A), label(r"deadline", font_size=17, color=GREY_A), label(r"work, \ measured", font_size=17, color=GREY_A),
                             label(r"load", font_size=17, color=GREY_A)))
        for B, lat, cst, ld in zip(d["blocks"], d["latency_ms"], d["cost_ms"], d["load"]):
            rows.add(VGroup(label(f"{B}", font_size=19, color=WHITE), label(f"{lat:.2f} ms", font_size=19, color=WHITE), label(f"{cst:.3f} ms", font_size=19, color=TUNE),
                            label(f"{100 * ld:.0f}\\%", font_size=19, color=EAR if ld > 0.08 else WHITE)))
        rows.arrange(DOWN, buff=0.18)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.0 + 2.6 * i)
        rows.move_to(DOWN * 0.3)
        note = label(r"measured on this computer, \ in this part's code; \ the median block", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.3)
        head = label(r"what a block costs", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        L = d["load"]
        with self.voiceover(
            "How hard is the deadline? <bookmark mark='a'/> Here is the median work per block, measured in this implementation on this computer. With "
            f"blocks of two thousand and forty-eight samples the engine uses {say(100 * L[-1])} per cent of the time it has. "
            f"<bookmark mark='b'/> With thirty-two it uses {say(100 * L[0])} per cent: small blocks cost more than their share, "
            "because each block carries a fixed overhead, the call, the bookkeeping, the start of every loop. Small blocks mean "
            "low latency and a heavier load; large blocks the reverse. Every studio chooses its block size between the two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(note), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:][::-1]], lag_ratio=0.12), run_time=1.5)
            vo.wait_until("b")
            self.play(Indicate(rows[1], color=EAR, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dropouts(self):
        d = load("callback")
        c = clip("callback.two")
        cells = choice_boxes([r"every deadline met", rf"{d['missed']} of {d['blocks_total']} blocks late"], width=4.2, buff=1.0, colors=[TUNE, EAR]).move_to(UP * 0.4)
        cap = label(r"the late blocks are played as silence; \ the lateness is simulated \ (60\% load, \ rare stalls)", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"a missed deadline, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "What happens when a block is late? The sound card cannot wait: it plays whatever is in the buffer, silence, repeated samples or another fallback depending on the driver; this example inserts silence. "
            f"Here is the same passage clean, then with {say(d['missed'])} of its {say(d['blocks_total'])} blocks late, each a gap "
            "of under three milliseconds."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"clean, \ then dropouts", kind="synthesized", detail=r"the engine's voices", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["clean"], st["dropouts"] - 0.3, buff=0.08)
            pulse(snd, cells[1], st["dropouts"], c.duration, buff=0.08)
        with self.voiceover(
            "Each gap is a click: a few milliseconds of silence cut into a waveform. One every second is enough to ruin a "
            "recording, which is why audio engineers count these, xruns, and why an engine is written to be predictable before "
            "it is written to be fast."
        ):
            self.play(Indicate(cells[1], color=EAR, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        items = [
            (r"in the audio callback: \ no waiting on locks, \ no memory allocation, \ no files, \ no network", WHITE),
            (r"any of these can take an unknown time; \ the deadline cannot", WHITE),
            (r"so messages cross from the interface to the engine through lock-free queues", WHITE),
            (r"Ross Bencina's rule of thumb: \ `time waits for nothing'", WHITE),
            (r"and timing must be exact inside the block too", TUNE),
        ]
        rows_scene(self, r"the rules of the audio thread", items,
                   "So the audio thread has rules. <bookmark mark='b'/> In the callback: no waiting on locks, no memory allocation, no "
                   "files, no network, <bookmark mark='c'/> because any of these can take an unknown time and the deadline cannot. "
                   "<bookmark mark='d'/> Messages cross from the interface to the engine through lock-free queues. "
                   "<bookmark mark='e'/> Ross Bencina's well-known essay on the subject is called, simply, Time waits for nothing. "
                   "<bookmark mark='f'/> And timing must be exact inside the block too.", marks="bcdef")

    # ------------------------------------------------------------------
    def ring(self):
        n = 12
        circ = VGroup()
        for i in range(n):
            ang = PI / 2 - 2 * PI * i / n
            pos = 1.8 * np.array([np.cos(ang), np.sin(ang), 0])
            full = i in (3, 4, 5, 6)
            circ.add(VGroup(Square(side_length=0.55, stroke_color=GREY_B, stroke_width=1.5, fill_color=TUNE, fill_opacity=0.6 if full else 0.0).move_to(pos)))
        circ.move_to(LEFT * 2.6 + DOWN * 0.3)
        c0 = circ.get_center()
        w = Arrow(c0, circ[7].get_center(), buff=0.35, color=EAR, stroke_width=3)
        r = Arrow(c0, circ[3].get_center(), buff=0.35, color=BLUE, stroke_width=3)
        side = VGroup(label(r"a ring of slots shared by two threads", font_size=18, color=WHITE),
                      label(r"the interface writes messages at the write index \ (pink) \ and advances it", font_size=16, color=EAR),
                      label(r"the audio thread reads at the read index \ (blue) \ and advances it", font_size=16, color=BLUE),
                      label(r"one producer, \ one consumer: \\ atomic publication, \ correct memory ordering, \ full/empty handling", font_size=16, color=TUNE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5)
        head = label(r"a lock-free queue", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How does a message reach the audio thread without a lock? <bookmark mark='a'/> Through a ring of slots shared by two threads. <bookmark mark='b'/> The interface writes each message at the write index and then advances it; <bookmark mark='c'/> the audio thread reads at the read index and advances that. <bookmark mark='d'/> With a suitable single-producer, single-consumer design, atomic publication, correct memory ordering, preallocated storage and explicit full/empty handling, each operation can have bounded cost: a design goal that this diagram illustrates rather than a production queue implemented here."
        ) as vo:
            self.play(FadeIn(head), FadeIn(circ))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowArrow(w), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowArrow(r), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
