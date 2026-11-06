from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.compute import load as load34
from videos.cs.cs46.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, module_box

REC = 200            # bytes per message in the Kafka paper's experiments (Kreps, Narkhede & Rao 2011)
RATE = 1e9           # the chapter's target: a gigabyte a second
PAPER = (50_000, 400_000)    # the paper's producer: messages a second with batches of 1 and of 50


def tex_time(s: float) -> str:
    if s < 1e-6:
        return rf"{s * 1e9:.0f} ns"
    if s < 1e-3:
        return rf"{s * 1e6:.0f} $\mu$s"
    return rf"{s * 1e3:.0f} ms"


class Throughput(VoiceoverScene):
    def construct(self):
        self.card()
        self.budget()
        self.sequential()
        self.batching()
        self.zerocopy()
        self.pagecache()

    def card(self):
        card = chapter_card(2, r"Moving a gigabyte a second", r"Why is a log on disk so fast?",
                            lit=(2011, 2014), extra=((2011, r"Kafka: \ batches and \texttt{sendfile}"),
                                                     (2014, r"Kreps: \ two million writes a second")), part=PART)
        with self.voiceover("Chapter two. Moving a gigabyte a second."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def budget(self):
        d = load34("disk")
        head = label(r"The budget", font_size=36).to_edge(UP, buff=0.3)
        per = REC / RATE
        sums = VGroup(
            label(r"a 10-gigabit network link carries $10/8 = 1.25$ gigabytes a second", font_size=21, color=WHITE),
            label(rf"at {REC}-byte messages, \ one gigabyte a second is {RATE / REC / 1e6:.0f} million messages: "
                  rf"\ \textbf{{{per * 1e9:.0f} ns each}}", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.4)
        x0, dec, lo = -2.6, 1.45, -7

        def X(s):
            return x0 + dec * (math.log10(s) - lo)
        axis = Line([X(1e-7), -1.15, 0], [X(1e-1), -1.15, 0], color=GREY_C, stroke_width=1.5)
        ticks = VGroup()
        for e, t in zip(range(-7, 0), (r"100 ns", r"1 $\mu$s", r"10 $\mu$s", r"100 $\mu$s", r"1 ms", r"10 ms",
                                       r"100 ms")):
            ticks.add(Line([X(10 ** e), -1.22, 0], [X(10 ** e), -1.08, 0], color=GREY_C, stroke_width=1.5))
            ticks.add(label(t, font_size=16, color=GREY_B).move_to([X(10 ** e), -1.45, 0]))
        rows = [(r"budget per message", per, YES),
                (r"random SSD read \ (Part 34's model)", d["ssd_read_us"] * 1e-6, KERN),
                (r"random disk read \ (Part 34's model)", d["random_4k_ms"] * 1e-3, NO)]
        bars = VGroup()
        for k, (nm, v, c) in enumerate(rows):
            y = 0.95 - 0.7 * k
            r = Rectangle(width=X(v) - X(1e-7), height=0.48, stroke_width=0, fill_color=c, fill_opacity=0.85)
            r.move_to([X(1e-7), y, 0], aligned_edge=LEFT)
            t = label(nm, font_size=18, color=c).next_to([X(1e-7), y, 0], LEFT, buff=0.2)
            val = label(tex_time(v) + (rf" \ $= {v / per:,.0f}\times$" if k else ""), font_size=18,
                        color=WHITE).next_to(r, RIGHT, buff=0.15)
            bars.add(VGroup(t, r, val))
        foot = wrapped_label(r"no record may wait for anything: \ not a seek, \ not a round trip, \ not a "
                             r"system call of its own", 12.4, font_size=22, color=HEAD).to_edge(DOWN, buff=0.75)
        scale = note(r"log scale", font_size=16).next_to(axis, RIGHT, buff=0.15).shift(DOWN * 0.1)
        with self.voiceover(
            "Why a gigabyte a second? <bookmark mark='a'/> It is roughly what a ten-gigabit network link carries. In "
            "the Kafka paper's experiments a message was two hundred bytes, so a gigabyte a second means five million"
            " messages, two hundred nanoseconds each. <bookmark mark='b'/> Set that budget beside Part 34's storage "
            "model: one random read from flash costs four hundred budgets, and one from a spinning disk sixty-five "
            "thousand. <bookmark mark='c'/> So no single message may wait for anything: not a seek, not a round trip,"
            " not even a system call of its own. Everything that follows pays for many messages at once."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sums[0]))
            self.play(FadeIn(sums[1]))
            vo.wait_until("b")
            self.play(Create(axis), FadeIn(ticks), FadeIn(scale), FadeIn(bars[0][0]),
                      GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            for b in bars[1:]:
                self.play(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def sequential(self):
        d = load34("disk")
        head = label(r"Only ever sequential", font_size=36).to_edge(UP, buff=0.3)
        n = 18
        cells = VGroup(*[Rectangle(width=0.55, height=0.5, stroke_color=GREY_B, stroke_width=1.2,
                                   fill_color=DATA, fill_opacity=0.5) for _ in range(n)]).arrange(RIGHT, buff=0)
        cells.next_to(head, DOWN, buff=0.75)
        wr = Arrow(cells[-1].get_top() + UP * 0.6, cells[-1].get_top(), buff=0.03, color=HEAD, stroke_width=3)
        wr_l = label(r"the producer appends", font_size=16, color=HEAD).next_to(wr, LEFT, buff=0.1).shift(UP * 0.2)

        def reader(k, c, t):
            a = Arrow(cells[k].get_bottom() + DOWN * 0.6, cells[k].get_bottom(), buff=0.03, color=c, stroke_width=3)
            return VGroup(a, label(t, font_size=16, color=c).next_to(a, DOWN, buff=0.06))
        ra, rb = reader(3, YES, r"consumer A"), reader(11, LAM, r"consumer B")
        W = 9.0
        bars = VGroup()
        for k, (t, v, c) in enumerate(((r"sequential", d["mb_s"], YES), (r"random 4 KiB", d["random_mb_s"], NO))):
            r = Rectangle(width=max(0.04, W * v / d["mb_s"]), height=0.42, stroke_width=0, fill_color=c,
                          fill_opacity=0.85)
            r.move_to([-4.3, -0.25 - 0.62 * k, 0], aligned_edge=LEFT)
            nm = label(t, font_size=18, color=c).next_to(r.get_left(), LEFT, buff=0.15)
            val = label(rf"{v:.0f} MB/s" if v >= 10 else rf"{v:.2f} MB/s", font_size=18, color=WHITE).next_to(
                r, RIGHT, buff=0.15)
            bars.add(VGroup(nm, r, val))
        cap = label(rf"Part 34's disk: \ ${d['ratio']:.0f}\times$ apart", font_size=18, color=GREY_A).next_to(
            bars, UP, buff=0.15).align_to(bars[1][1], LEFT)
        notes = VGroup(
            wrapped_label(r"writes are appends and reads are forward scans, \ so every byte moves at the "
                          r"sequential rate; \ the kernel's read-ahead fetches the next pages before they are asked "
                          r"for", 12.4, font_size=20, color=WHITE),
            wrapped_label(rf"no tree to update: \ an append costs the same with a week of data as with none; \ and "
                          rf"partitions spread over disks and brokers add up, \ since one {d['mb_s']:.0f} MB/s disk "
                          rf"is about a seventh of the target", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The first answer is Part 34's rule: write in long runs. <bookmark mark='a'/> A log does nothing else. "
            "The producer only appends, and each consumer only reads forward from its offset, so the disk sees long "
            "sequential runs, and the kernel's read-ahead fetches pages before anyone asks for them. "
            "<bookmark mark='b'/> On Part 34's model disk that is a hundred and fifty megabytes a second, against a "
            "third of one. <bookmark mark='c'/> There is no index to maintain either, so an append costs the same "
            "with a week of data as with none. And partitions on different disks and brokers add their bandwidth "
            "together: seven such disks make a gigabyte a second."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells))
            vo.wait_until("a")
            self.play(GrowArrow(wr), FadeIn(wr_l), FadeIn(ra), FadeIn(rb))
            self.play(ra.animate.shift(RIGHT * 0.55 * 5), rb.animate.shift(RIGHT * 0.55 * 4), run_time=2.5,
                      rate_func=linear)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(cap), *[FadeIn(b[0]) for b in bars], *[GrowFromEdge(b[1], LEFT) for b in bars],
                      *[FadeIn(b[2]) for b in bars])
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def batching(self):
        head = label(r"Batching", font_size=36).to_edge(UP, buff=0.3)
        prod = module_box(r"producer", DATA, w=1.9, h=0.6).move_to([-5.6, 1.6, 0])
        buf = RoundedRectangle(width=3.2, height=0.75, corner_radius=0.08, stroke_color=HEAD, stroke_width=2)
        buf.move_to([-2.4, 1.6, 0])
        buf_l = label(r"batch buffer", font_size=16, color=HEAD).next_to(buf, UP, buff=0.08)
        brok = module_box(r"broker", KERN, w=1.9, h=0.6).move_to([2.6, 1.6, 0])
        req = Arrow(buf.get_right(), brok.get_left(), buff=0.1, color=GREY_B, stroke_width=2)
        req_l = label(r"one request", font_size=16, color=GREY_B).next_to(req, UP, buff=0.06)
        msgs = [Square(0.4, stroke_width=0, fill_color=DATA, fill_opacity=0.85) for _ in range(6)]
        slots = [buf.get_left() + RIGHT * (0.32 + 0.5 * i) for i in range(6)]
        disk = label(r"written as it came, \ fetched as it was written", font_size=16, color=KERN).next_to(
            brok, DOWN, buff=0.15)
        chart = bar_chart([PAPER[0] / 1000, PAPER[1] / 1000], [r"batch of 1", r"batch of 50"], [NO, YES],
                          height=2.2, bar_w=0.9, gap=0.9, fmt_=lambda v: rf"{v:,.0f}k", font_size=18)
        chart.move_to([-3.8, -1.5, 0])
        ctitle = label(r"messages a second, \ one producer \ (Kreps, \ Narkhede and Rao 2011)", font_size=16,
                       color=GREY_A).next_to(chart, UP, buff=0.2)
        notes = VGroup(
            label(r"time per message $= \dfrac{\text{overhead per request}}{\text{batch size}} + "
                  r"\text{cost per byte} \times \text{size}$", font_size=20, color=WHITE),
            wrapped_label(r"the producer waits up to \texttt{linger.ms} or until \texttt{batch.size} bytes, \ "
                          r"trading a few milliseconds of latency for throughput", 6.0, font_size=19, color=HEAD),
            wrapped_label(r"a whole batch is compressed at once, \ and records that repeat each other's fields "
                          r"compress far better together than apart", 6.0, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.85, -1.45, 0])
        with self.voiceover(
            "The second answer: never send one message alone. <bookmark mark='a'/> The producer collects messages for"
            " a partition into a batch and sends the batch in one request. The broker appends it exactly as it "
            "arrived, and consumers fetch it the same way. <bookmark mark='b'/> Every request has a fixed overhead, "
            "and a batch divides it among all its messages. In the Kafka paper, one producer sent fifty thousand "
            "messages a second one at a time, and four hundred thousand in batches of fifty. <bookmark mark='c'/> The"
            " price is a few milliseconds of latency while a batch fills. And a batch compresses far better than "
            "single messages, because neighbouring records repeat each other's fields."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prod), Create(buf), FadeIn(buf_l), FadeIn(brok))
            vo.wait_until("a")
            for m, s in zip(msgs, slots):
                m.move_to(prod)
                self.play(m.animate.move_to(s), run_time=0.4)
            batch = VGroup(*msgs)
            self.play(GrowArrow(req), FadeIn(req_l))
            self.play(batch.animate.arrange(RIGHT, buff=0.05).scale(0.6).next_to(brok, UP, buff=0.12), run_time=1.2)
            self.play(FadeIn(disk))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), FadeIn(ctitle), FadeIn(chart))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def zerocopy(self):
        head = label(r"Zero-copy", font_size=36).to_edge(UP, buff=0.3)
        ky, uy = 0.3, 2.0
        boxes = {
            "disk": module_box(r"disk", GREY_B, w=1.6, h=0.65).move_to([-5.6, ky, 0]),
            "pc": module_box(r"page cache", KERN, w=2.0, h=0.65).move_to([-2.6, ky, 0]),
            "sock": module_box(r"socket buffer", KERN, w=2.2, h=0.65).move_to([1.4, ky, 0]),
            "nic": module_box(r"network card", GREY_B, w=2.0, h=0.65).move_to([4.9, ky, 0]),
            "app": module_box(r"broker's buffer", DATA, w=2.4, h=0.65).move_to([-0.6, uy, 0]),
        }
        sep = DashedLine([-6.8, 1.15, 0], [6.8, 1.15, 0], color=GREY_D, stroke_width=1.5)
        sides = VGroup(label(r"user space", font_size=16, color=GREY_B).move_to([-5.8, 1.42, 0]),
                       label(r"kernel", font_size=16, color=GREY_B).move_to([-5.8, 0.88, 0]))

        def arr(a, b, k, c=GREY_A, sa=RIGHT, sb=LEFT):
            ar = Arrow(boxes[a].get_edge_center(sa), boxes[b].get_edge_center(sb), buff=0.08, color=c,
                       stroke_width=2.5, max_tip_length_to_length_ratio=0.15)
            n = Circle(radius=0.16, color=c, stroke_width=1.5, fill_color=BG, fill_opacity=1).move_to(ar)
            return VGroup(ar, n, label(f"{k}", font_size=16, color=c).move_to(n))
        copies = VGroup(arr("disk", "pc", 1), arr("pc", "app", 2, sa=UP, sb=LEFT), arr("app", "sock", 3, sa=RIGHT,
                                                                                        sb=UP),
                        arr("sock", "nic", 4))
        direct = Arrow(boxes["pc"].get_right(), boxes["sock"].get_left(), buff=0.08, color=YES, stroke_width=4)
        direct_l = label(r"\texttt{sendfile}", font_size=18, color=YES).next_to(direct, DOWN, buff=0.1)
        notes = VGroup(
            wrapped_label(r"\texttt{read} then \texttt{write}: \ four copies and two system calls, \ the bytes "
                          r"crossing into the program and back out", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"\texttt{sendfile}: \ the kernel passes the file's cached pages straight to the "
                          r"socket, \ avoiding two copies and one system call \ (Kreps, \ Narkhede and Rao 2011)", 12.4,
                          font_size=20, color=YES),
            wrapped_label(r"it works because the broker never looks inside a batch: \ the bytes on disk are the "
                          r"bytes the producer sent and the bytes the consumer gets; \ encrypting in the program "
                          r"\ (TLS) \ gives it up", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The third answer is to stop touching the bytes. <bookmark mark='a'/> Served the obvious way, data is "
            "copied from disk into the kernel's page cache, then into the program's buffer, back into the kernel's "
            "socket buffer, and out to the network card: four copies and two system calls, as the Kafka paper counts "
            "them. <bookmark mark='b'/> The sendfile call asks the kernel to pass the file's pages straight to a "
            "socket, and the middle two copies, and one system call, disappear. <bookmark mark='c'/> This works only "
            "because the broker never looks inside a message: the bytes on disk are the bytes the producer sent and "
            "the consumer receives. Encrypting in the program, as TLS does, gives zero-copy up."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(b) for b in boxes.values()], Create(sep), FadeIn(sides))
            vo.wait_until("a")
            for c in copies:
                self.play(GrowArrow(c[0]), FadeIn(c[1]), FadeIn(c[2]), run_time=0.7)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(copies[1].animate.set_opacity(0.15), copies[2].animate.set_opacity(0.15),
                      boxes["app"].animate.set_opacity(0.3))
            self.play(GrowArrow(direct), FadeIn(direct_l), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def pagecache(self):
        head = label(r"The page cache is the buffer", font_size=36).to_edge(UP, buff=0.3)
        n, w = 16, 0.6
        x0 = -4.6
        disk = VGroup(*[Rectangle(width=w, height=0.5, stroke_color=GREY_C, stroke_width=1, fill_color=DATA,
                                  fill_opacity=0.35) for _ in range(n)]).arrange(RIGHT, buff=0)
        disk.move_to([x0, 0.15, 0], aligned_edge=LEFT)
        mem = VGroup(*[Rectangle(width=w, height=0.5, stroke_color=KERN, stroke_width=1.2, fill_color=KERN,
                                 fill_opacity=0.45) for _ in range(5)]).arrange(RIGHT, buff=0)
        mem.next_to(disk[-5:], UP, buff=0.75).align_to(disk[-5], LEFT)
        ldisk = label(r"segments on disk", font_size=18, color=DATA).next_to(disk, LEFT, buff=0.2)
        lmem = label(r"page cache \ (memory)", font_size=18, color=KERN).next_to(mem, LEFT, buff=0.2)
        links = VGroup(*[DashedLine(m.get_bottom(), dk.get_top(), color=KERN, stroke_width=1, dash_length=0.06)
                         for m, dk in zip(mem, disk[-5:])])
        wr = Arrow(mem[-1].get_right() + RIGHT * 0.9, mem[-1].get_right(), buff=0.05, color=HEAD, stroke_width=3)
        wr_l = label(r"producer", font_size=16, color=HEAD).next_to(wr, UP, buff=0.06)
        ra = Arrow(mem[2].get_top() + UP * 0.05, mem[2].get_top() + UP * 0.7, buff=0, color=YES, stroke_width=3)
        ra_l = label(r"consumer at the tail: \ served from memory", font_size=16, color=YES).next_to(ra, UP, buff=0.05)
        rb = Arrow(disk[3].get_bottom(), disk[3].get_bottom() + DOWN * 0.65, buff=0.03, color=LAM, stroke_width=3)
        rb_l = label(r"consumer replaying: \ a sequential read", font_size=16, color=LAM).next_to(rb, DOWN,
                                                                                                 buff=0.05)
        notes = VGroup(
            wrapped_label(r"Kafka keeps no cache of its own: \ it writes to the file system and lets the kernel's "
                          r"page cache \ (Part 34) \ hold the recent tail \ --- \ no second copy in the heap, \ no "
                          r"garbage collector, \ and a cache that survives a restart of the broker", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"durability comes from replicas \ (chapter 1), \ not from \texttt{fsync} per message: "
                          r"\ by default the broker leaves flushing to the kernel", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(disk, DOWN, buff=1.55).set_x(0)
        with self.voiceover(
            "The last answer is to let the operating system do the caching. <bookmark mark='a'/> Kafka writes every "
            "batch to the file system and keeps no cache of its own. The kernel's page cache holds the recent tail, "
            "so a consumer that keeps up reads from memory, and the disk is never asked. <bookmark mark='b'/> A "
            "consumer replaying yesterday reads from disk, but sequentially. There is no second copy in the program's"
            " heap, no garbage collector sweeping millions of messages, and the cache stays warm when the broker "
            "restarts. <bookmark mark='c'/> Durability comes from the replicas of chapter one, not from forcing each "
            "write to disk. Together, these choices let Jay Kreps report in 2014 two million writes a second on three"
            " ordinary machines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(disk), FadeIn(ldisk))
            vo.wait_until("a")
            self.play(FadeIn(mem), FadeIn(lmem), Create(links), GrowArrow(wr), FadeIn(wr_l))
            self.play(GrowArrow(ra), FadeIn(ra_l), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(rb), FadeIn(rb_l))
            self.play(rb.animate.shift(RIGHT * w * 4), rb_l.animate.shift(RIGHT * w * 4), run_time=2, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, NO)
