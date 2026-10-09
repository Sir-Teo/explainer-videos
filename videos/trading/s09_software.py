from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import (
    FACTS, Plot, cpu_die, fmt_int, fmt_ns, label, load, machine_tag, mtex, node, note, scatter, schematic_tag, tagged,
)


class HotPath(VoiceoverScene):
    def construct(self):
        self.bypass()
        self.cores_and_rings()
        self.false_sharing()
        self.branches()
        self.jitter()

    # ------------------------------------------------------------------
    def bypass(self):
        b = load("bench")["pingpong"]
        busy, sleep = b["udp_busy_poll"]["pct"]["50"], b["udp_blocking"]["pct"]["50"]
        stack = ["network card", "interrupt", "kernel driver", "network stack", "socket buffer", "system call",
                 "your program"]
        cols = [GREY_B, C.KERNEL, C.KERNEL, C.KERNEL, C.KERNEL, C.KERNEL, C.OURS]
        left = VGroup(*[node(t, color=c, width=3.2, height=0.52, font_size=22) for t, c in zip(stack, cols)])
        left.arrange(UP, buff=0.12).move_to(LEFT * 3.6 + DOWN * 0.4)
        right = VGroup(node("network card", GREY_B, width=3.2, height=0.52, font_size=22),
                       node(r"receive ring, in your\\program's own memory", C.MSG, width=3.2, height=0.9, font_size=22),
                       node("your program, polling", C.OURS, width=3.2, height=0.52, font_size=22))
        right.arrange(UP, buff=0.9).move_to(RIGHT * 3.6 + DOWN * 0.4)
        lt = label(r"the normal path", font_size=30, color=C.KERNEL).next_to(left, UP, buff=0.25)
        rt = label(r"kernel bypass", font_size=30, color=C.MSG).next_to(right, UP, buff=0.25).align_to(lt, UP)
        ra = VGroup(Arrow(right[0].get_top(), right[1].get_bottom(), buff=0.06, color=C.MSG, stroke_width=3),
                    Arrow(right[1].get_top(), right[2].get_bottom(), buff=0.06, color=C.MSG, stroke_width=3))
        dma = label(r"DMA", font_size=20, color=C.MSG).next_to(ra[0], RIGHT, buff=0.1)
        m1 = tagged(rf"measured here: {fmt_ns(sleep, tex=False).replace('us', r'$\mu$s')} asleep, "
                    rf"{fmt_ns(busy, tex=False).replace('us', r'$\mu$s')} spinning", font_size=22, color=C.KERNEL)
        m1.next_to(left, DOWN, buff=0.2)
        m2 = tagged(r"frame to program: under 1 $\mu$s (Nigito)", font_size=22, color=C.MSG).next_to(right, DOWN, buff=0.2)
        m2.align_to(m1, UP)
        tag = schematic_tag()
        head = label(r"the hot path in software", font_size=40).to_edge(UP, buff=0.4)
        self.play(FadeIn(head), run_time=0.6)
        with self.voiceover(
            "That bottom rung, the operating system, is the first thing a trading system gets rid of. <bookmark "
            "mark='l'/> Normally, when a packet arrives, the network card interrupts the processor, the kernel's "
            "driver and network stack process it, it waits in a socket buffer, and only when your program asks, "
            "through a system call, is it copied to you. If your program was asleep, it also has to be woken up. "
            "<bookmark mark='m'/> On this machine, that path costs about fourteen microseconds when the receiver "
            "sleeps, and three when it spins. <bookmark mark='r'/> Trading firms use network cards that write packets "
            "straight into a ring of memory inside the program, which watches that memory constantly. The kernel never "
            "touches the data. Brian Nigito puts a frame's trip from the wire into a program at under a microsecond."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("l")
            self.play(FadeOut(head), FadeIn(lt), LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in left], lag_ratio=0.12), run_time=1.5)
            d = Dot(left[0].get_center(), radius=0.1, color=C.MSG)
            path = VMobject().set_points_as_corners([n.get_center() for n in left])
            self.add(d)
            self.play(MoveAlongPath(d, path), run_time=3.0, rate_func=linear)
            self.remove(d)
            vo.wait_until("m")
            self.play(FadeIn(m1))
            vo.wait_until("r")
            self.play(FadeIn(rt), FadeIn(right), GrowArrow(ra[0]), GrowArrow(ra[1]), FadeIn(dma))
            d2 = Dot(right[0].get_center(), radius=0.1, color=C.MSG)
            self.add(d2)
            self.play(MoveAlongPath(d2, VMobject().set_points_as_corners([n.get_center() for n in right])), run_time=0.8,
                      rate_func=linear)
            self.remove(d2)
            self.play(FadeIn(m2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def cores_and_rings(self):
        sp = load("bench")["spsc"]
        rate = sp["throughput_msgs_per_s"]
        med = sp["paced_latency"]["pct"]["50"]
        assert 1e7 < rate < 3e7 and 150 < med < 500
        die = cpu_die(4, size=3.9, labels=["", "", "", ""]).move_to(LEFT * 4.2 + DOWN * 0.2)
        roles = [("operating\\\\system", C.KERNEL), ("feed\\\\handler", C.MSG), ("strategy", C.SIGNAL), ("order\\\\gateway", C.ORDER)]
        rl = VGroup(*[label(t, font_size=19, color=c).move_to(core).shift(UP * 0.18) for (t, c), core in zip(roles, die.cores)])
        spin = VGroup(*[Arc(radius=0.22, angle=1.6 * PI, color=c, stroke_width=3).move_to(core).shift(DOWN * 0.42)
                        for (_, c), core in zip(roles[1:], die.cores[1:])])
        dt = label(r"one core per job, pinned, never sleeping", font_size=24).next_to(die, UP, buff=0.3)
        # a ring buffer
        n = 16
        R = 1.55
        center = RIGHT * 2.6 + DOWN * 0.3
        slots = VGroup()
        for i in range(n):
            a = PI / 2 - i * TAU / n
            s = AnnularSector(inner_radius=R - 0.45, outer_radius=R, angle=TAU / n - 0.04, start_angle=a - TAU / n + 0.02,
                              fill_color=GREY_D, fill_opacity=0.5, stroke_width=1, stroke_color=GREY_B).shift(center)
            slots.add(s)
        rlab = label(r"a ring buffer between two cores", font_size=26).next_to(slots, UP, buff=1.05)
        head = ValueTracker(0)
        tail = ValueTracker(0)

        def marker(tracker, color, text, r_out):
            def f():
                k = tracker.get_value()
                a = PI / 2 - (k + 0.5) * TAU / n
                p = center + np.array([np.cos(a), np.sin(a), 0]) * r_out
                q = center + np.array([np.cos(a), np.sin(a), 0]) * (R + 0.05 if r_out > R else R - 0.5)
                return VGroup(Arrow(p, q, buff=0, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.35),
                              label(text, font_size=20, color=color).move_to(p + (p - center) * 0.18))
            return always_redraw(f)

        def fills():
            h, t = int(head.get_value()), int(tail.get_value())
            g = VGroup()
            for k in range(t, h):
                g.add(slots[k % n].copy().set_fill(C.MSG, 0.85))
            return g

        fl = always_redraw(fills)
        hm = marker(head, C.MSG, "write", R + 0.75)
        tm = marker(tail, C.SIGNAL, "read", R - 1.05)
        stats = VGroup(label(rf"{rate / 1e6:.1f} million messages a second", font_size=26, color=C.MSG),
                       label(rf"median hand-off: {med:.0f} ns", font_size=26, color=C.LATENCY)).arrange(DOWN, buff=0.1)
        stats.next_to(slots, DOWN, buff=0.35)
        with self.voiceover(
            "Inside the program, the same philosophy. <bookmark mark='c'/> Each job gets its own processor core: one "
            "decodes the feed, one runs the strategy, one sends orders. Each core is reserved, shielded from the "
            "operating system's other work, and never sleeps: it spins in a tight loop, checking for new work billions "
            "of times a second. <bookmark mark='r'/> The cores pass messages through ring buffers: a fixed circle of "
            "slots in shared memory. <bookmark mark='w'/> The producer writes into the next slot and advances its "
            "counter; the consumer reads behind it and advances its own. No locks, no system calls, and the memory is "
            "allocated once, at startup. <bookmark mark='s'/> Measured here: almost sixteen million messages a "
            "second, and a median hand-off of three hundred nanoseconds."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(die), FadeIn(rl), FadeIn(dt))
            self.play(*[Rotate(s, angle=-TAU, about_point=s.get_center()) for s in spin], run_time=1.2, rate_func=linear)
            vo.wait_until("r")
            self.play(FadeIn(slots), FadeIn(rlab))
            self.add(fl, hm, tm)
            vo.wait_until("w")
            self.play(head.animate.set_value(6), run_time=1.5, rate_func=linear)
            self.play(head.animate.set_value(11), tail.animate.set_value(5), run_time=1.5, rate_func=linear)
            self.play(head.animate.set_value(20), tail.animate.set_value(14), run_time=2.0, rate_func=linear)
            vo.wait_until("s")
            self.play(FadeIn(stats, shift=UP * 0.1), head.animate.set_value(26), tail.animate.set_value(24),
                      run_time=1.5, rate_func=linear)
        for m in (fl, hm, tm):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def false_sharing(self):
        fs = load("bench")["falseshare"]
        same, apart = fs["same_line_ns_per_increment"], fs["separate_lines_ns_per_increment"]
        assert same / apart > 4
        c1 = node(r"core 2", C.MSG, width=1.8, height=0.9).move_to(LEFT * 4.5 + UP * 0.6)
        c2 = node(r"core 3", C.SIGNAL, width=1.8, height=0.9).move_to(RIGHT * 4.5 + UP * 0.6)
        line = VGroup(Rectangle(width=4.0, height=0.6, stroke_color=WHITE, stroke_width=2, fill_color=GREY_D, fill_opacity=0.4))
        a = Rectangle(width=0.5, height=0.6, stroke_width=0, fill_color=C.MSG, fill_opacity=0.8).align_to(line[0], LEFT)
        bb = Rectangle(width=0.5, height=0.6, stroke_width=0, fill_color=C.SIGNAL, fill_opacity=0.8).next_to(a, RIGHT, buff=0)
        line.add(a, bb, label(r"counter A", font_size=16).move_to(a).shift(DOWN * 0.5),
                 label(r"counter B", font_size=16).move_to(bb).shift(DOWN * 0.8))
        line.move_to(UP * 0.6)
        ll = label(r"one 64-byte cache line", font_size=24, color=GREY_A).next_to(line, UP, buff=0.2)
        res = VGroup(
            label(rf"counters on the same line: {same:.0f} ns per increment", font_size=28, color=C.KERNEL),
            label(rf"on separate lines: {apart:.1f} ns", font_size=28, color=C.MSG),
            label(rf"{same / apart:.0f}$\times$ slower, and neither program shares any data", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "But sharing memory between cores has a trap. Processors move memory around in sixty-four-byte blocks "
            "called cache lines, and only one core can own a line for writing at a time. <bookmark mark='l'/> Put two "
            "counters side by side, give one to each core, and let both increment their own, millions of times. "
            "<bookmark mark='p'/> They share nothing, logically, but the line they live on bounces between the two "
            "cores on every write. <bookmark mark='r'/> On this machine, that's about forty-six nanoseconds per "
            "increment instead of six: eight times slower. It's called false sharing, and the fix is just padding: "
            "keep each core's hot data on its own line."
        ) as vo:
            self.play(FadeIn(c1), FadeIn(c2), FadeIn(machine_tag()))
            vo.wait_until("l")
            self.play(FadeIn(line), FadeIn(ll))
            vo.wait_until("p")
            for k in range(3):
                self.play(line.animate.next_to(c1, DOWN, buff=0.3), run_time=0.35)
                self.play(line.animate.next_to(c2, DOWN, buff=0.3), run_time=0.35)
            self.play(line.animate.move_to(UP * 0.6), run_time=0.35)
            vo.wait_until("r")
            self.play(FadeIn(res, shift=UP * 0.1))
        self.clear_scene()

    # ------------------------------------------------------------------
    def branches(self):
        br = load("bench")["branch"]
        sh, so = br["shuffled_ns_per_element"], br["sorted_ns_per_element"]
        assert sh / so > 4
        code = VGroup(*[Text(t, font="DejaVu Sans Mono", font_size=24, color=c) for t, c in [
            ("for x in data:", GREY_A), ("    if x >= 128:", C.SIGNAL), ("        total += x", GREY_A)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        code.to_edge(UP, buff=0.8)
        rows = VGroup(
            VGroup(label(r"data in random order", font_size=28), Rectangle(width=sh * 1.6, height=0.5, stroke_width=0,
                                                                          fill_color=C.KERNEL, fill_opacity=0.85),
                   MathTex(rf"{sh:.2f}\,\mathrm{{ns}}", font_size=30)),
            VGroup(label(r"the same data, sorted", font_size=28), Rectangle(width=so * 1.6, height=0.5, stroke_width=0,
                                                                           fill_color=C.MSG, fill_opacity=0.85),
                   MathTex(rf"{so:.2f}\,\mathrm{{ns}}", font_size=30)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.3)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.3)
        expl = label(r"the processor guesses which way the \texttt{if} will go; a wrong guess costs dozens of cycles",
                     font_size=26, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Another invisible cost: <bookmark mark='c'/> here's a loop that adds up the numbers above a threshold. "
            "<bookmark mark='r'/> On random data, it takes about three and three-quarter nanoseconds per number. "
            "<bookmark mark='s'/> On the same numbers, sorted, under half a nanosecond: eight times faster. <bookmark "
            "mark='e'/> The processor guesses which way each 'if' will go before it knows, and runs ahead. Sorted data "
            "makes the guess easy; random data makes it wrong half the time, and every wrong guess throws away work. "
            "So hot-path code is written to be predictable, and some firms even keep it warm, running fake decisions "
            "through it so the caches and predictors are ready when a real one comes."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(code), FadeIn(machine_tag()))
            vo.wait_until("r")
            self.play(FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]))
            vo.wait_until("s")
            self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]))
            vo.wait_until("e")
            self.play(FadeIn(expl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def jitter(self):
        j = load("bench")["jitter"]
        at = np.array(j["at_ns"], float) / 1e9
        gap = np.array(j["gap_ns"], float)
        sm = j["summary"]
        assert sm["max_gap_ns"] > 1e6 and 0.01 < sm["lost_fraction"] < 0.1
        ch = Plot((0, 10), (300, 1e7), width=11, height=3.6, log_y=True, x_ticks=list(range(0, 11, 2)),
                  x_fmt=lambda v: rf"{int(v)}\,\mathrm{{s}}", y_ticks=[1e3, 1e4, 1e5, 1e6, 1e7],
                  y_fmt=lambda v: fmt_ns(v)).shift(UP * 0.55)
        big = gap > 1000
        pts = np.array([ch.c2p(x, y) for x, y in zip(at[big], gap[big])])
        chunk = np.minimum((at[big] / 10 * 20).astype(int), 19)
        dots = Group(*[scatter(pts[chunk == k], C.KERNEL, size=4) for k in range(20)])
        ttl = label(r"one reserved core, spinning for ten seconds: every time it was interrupted", font_size=30)
        ttl.to_edge(UP, buff=0.25)
        yl = ch.y_title(r"length of the interruption", font_size=22)
        sp = load("bench")["spsc"]["paced_latency"]["pct"]
        stats = VGroup(
            label(rf"{fmt_int(sm['over_10us'])} interruptions longer than 10 $\mu$s; the longest, {sm['max_gap_ns'] / 1e6:.1f} ms",
                  font_size=24, color=C.KERNEL),
            label(rf"ring buffer hand-off: median {sp['50']} ns, but 99th percentile {sp['99'] / 1000:.0f} $\mu$s, "
                  rf"99.9th {sp['99.9'] / 1e6:.1f} ms", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And then there's the noise that isn't your code at all. <bookmark mark='j'/> Here a reserved core on this "
            "machine did nothing but check the clock as fast as it could for ten seconds, and recorded every gap: every "
            "moment something else took the processor away from it. <bookmark mark='d'/> Tens of thousands of "
            "interruptions, eleven thousand of them longer than ten microseconds, the longest almost seven "
            "milliseconds. <bookmark mark='t'/> Those gaps are exactly the tail we saw in the ring buffer: a median "
            "hand-off of three hundred nanoseconds, but one in a hundred over a hundred microseconds. <bookmark "
            "mark='v'/> This computer is a virtual machine sharing hardware with strangers, which makes it noisy. "
            "Production trading servers are bare metal, with interrupts steered away from the trading cores, power "
            "saving switched off, and constant monitoring for exactly these spikes, because a race is lost in the "
            "tail, not the median."
        ) as vo:
            mt = machine_tag().next_to(ch.x_labels, DOWN, buff=0.12).align_to(ch.x_axis, RIGHT)
            self.play(FadeIn(ttl), Create(ch), FadeIn(yl), FadeIn(mt))
            vo.wait_until("j")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.8), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(stats[0]))
            vo.wait_until("t")
            self.play(FadeIn(stats[1]))
        self.clear_scene()
