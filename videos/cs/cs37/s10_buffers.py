from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (CCC, DATA, HEAD, KERN, LAM, NO, PART, SEG, WIN, YES, axes, grid_table, load,
                                   trace)

QC = {"droptail": NO, "red": KERN, "codel": YES}
QN = {"droptail": r"drop-tail", "red": r"RED", "codel": r"CoDel"}


class Buffers(VoiceoverScene):
    def construct(self):
        self.card()
        self.sizes()
        self.bloat()
        self.aqm()
        self.appenzeller()

    def card(self):
        card = chapter_card(9, r"Queues", r"How big should a router's buffer be?", lit=(1993, 2012),
                            extra=((1993, r"Floyd and Jacobson: \ RED"), (2004, r"Appenzeller et al.: \ "
                                                                                r"$\text{BDP}/\sqrt{n}$"),
                                   (2010, r"Gettys: \ bufferbloat"), (2012, r"Nichols and Jacobson: \ CoDel")),
                            part=PART)
        with self.voiceover("Chapter nine. Queues."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sizes(self):
        b = load("buffers")
        head = label(r"Buffer size: \ throughput against delay", font_size=36).to_edge(UP, buff=0.3)
        rows = [[rf"{r['mult']:g} $\times$ BDP", f"{r['util'] * 100:.1f}\\%", f"{r['queue_ms']:.0f} ms",
                 f"{r['rtt_ms']:.0f} ms"] for r in b["rows"]]
        tab = grid_table([r"buffer", r"link busy", r"mean queueing delay", r"round trip"], rows,
                         widths=[2.6, 2.0, 3.2, 2.2], row_h=0.42, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        for k, r in enumerate(b["rows"], start=1):
            tab.cells[k][1].set_color(YES if r["util"] > 0.98 else KERN)
            tab.cells[k][2].set_color(NO if r["queue_ms"] > 100 else WHITE)
        lines = VGroup(
            wrapped_label(r"one Reno flow, \ 10 Mb/s, \ RTT 100 ms: \ BDP = 83 packets", 12.4, font_size=20,
                          color=GREY_A),
            wrapped_label(r"too small: \ the halved window drains the queue, \ and the link idles; \ one BDP keeps "
                          r"it busy through every halving \ (the rule of thumb of Villamizar and Song, 1994)", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"bigger than that buys \textbf{nothing} but delay: \ loss-based TCP fills whatever buffer "
                          r"it is given", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "A router needs a queue, to absorb bursts. How long should it be? We gave one Reno flow, on a "
            "ten-megabit link with a hundred-millisecond round trip, buffers from a tenth of the bandwidth-delay "
            "product to eight times it. <bookmark mark='a'/> Too small, and every halving of the window drains the "
            "queue and leaves the link idle for a while: with a tenth of the product, the link is busy only "
            "seventy-eight percent of the time. With one full product, the queue never quite empties, and the link "
            "is ninety-nine percent busy. That was the rule of thumb from 1994. <bookmark mark='b'/> Beyond that, a "
            "bigger buffer buys no throughput at all. It buys delay. A loss-based TCP keeps growing its window until "
            "something is dropped, so it fills whatever buffer it is given. With eight times the product, every "
            "packet waits four hundred milliseconds in the queue, and the round trip is over half a second."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in range(1, 5)], lag_ratio=0.25))
            vo.wait_until("a")
            self.play(FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in range(5, len(rows) + 1)],
                                  lag_ratio=0.3), FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def bloat(self):
        head = label(r"Bufferbloat", font_size=36).to_edge(UP, buff=0.3)
        house = RoundedRectangle(width=3.0, height=1.6, corner_radius=0.15, stroke_color=DATA, stroke_width=2)
        house.move_to([-4.6, 0.8, 0])
        hl = label(r"a home \\ upload: \ 1 Mb/s", font_size=19, color=DATA).move_to(house)
        modem = RoundedRectangle(width=2.6, height=1.6, corner_radius=0.15, stroke_color=NO, stroke_width=2)
        modem.move_to([0, 0.8, 0])
        q = VGroup(*[Rectangle(width=0.14, height=0.8, stroke_width=0, fill_color=NO, fill_opacity=0.8)
                     for _ in range(14)]).arrange(RIGHT, buff=0.02).move_to(modem)
        ml = label(r"the modem's buffer: \ 256 packets", font_size=18, color=NO).next_to(modem, DOWN, buff=0.12)
        net = RoundedRectangle(width=2.6, height=1.6, corner_radius=0.15, stroke_color=GREY_C, stroke_width=2)
        net.move_to([4.6, 0.8, 0])
        nl = label(r"the Internet", font_size=20, color=GREY_B).move_to(net)
        a1 = Arrow(house.get_right(), modem.get_left(), buff=0.1, color=GREY_B)
        a2 = Arrow(modem.get_right(), net.get_left(), buff=0.1, color=GREY_B)
        lines = VGroup(
            wrapped_label(r"256 packets of 1{,}500 bytes at 1 Mb/s: \ \textbf{3 seconds} of queue, \ in front of "
                          r"every packet once an upload is running", 12.4, font_size=21, color=NO),
            wrapped_label(r"a video call, \ a game, \ a DNS lookup: \ all wait behind the upload; \ Jim Gettys found "
                          r"seconds of delay in home routers, \ modems, \ Wi-Fi and phones \ (2010)", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"memory became cheap, \ so buffers grew; \ but a buffer sized for the fastest link "
                          r"is seconds long on a slow one", 12.4, font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 2010 Jim Gettys, at Bell Labs, noticed that his home network became unusable whenever he uploaded "
            "a file. <bookmark mark='a'/> His cable modem had a buffer of a few hundred packets, and an upload link "
            "of about a megabit a second. Two hundred and fifty-six packets of fifteen hundred bytes, at a megabit a "
            "second, is three seconds. Once an upload filled that queue, every packet from the house, a video "
            "call, a keystroke, a DNS lookup, waited three seconds behind it. <bookmark mark='b'/> He found the same "
            "everywhere: in home routers, modems, Wi-Fi drivers and phones. He called it bufferbloat. "
            "<bookmark mark='c'/> Memory had become cheap, so buffers grew, and nobody had noticed that a buffer "
            "sized for the fastest link a device might see was seconds long on the link it actually had."
        ) as vo:
            self.play(FadeIn(head), Create(house), FadeIn(hl), Create(modem), FadeIn(ml), Create(net), FadeIn(nl),
                      GrowArrow(a1), GrowArrow(a2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in q], lag_ratio=0.1))
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def aqm(self):
        b = load("buffers")
        head = label(r"Drop early, \ drop on delay", font_size=36).to_edge(UP, buff=0.3)
        g = axes([10, 60, 10], [0, 1300, 400], x_length=6.6, y_length=3.4, x_label=r"seconds",
                 y_label=r"queueing delay", xticks=range(10, 61, 10), yticks=(400, 800, 1200),
                 fy=lambda v: f"{v:.0f} ms").move_to([-3.0, -0.2, 0])
        ax = g.ax
        rate = 10e6 / 12000
        traces = {q: trace(ax, [(t, n / rate * 1000) for t, n in b["deep"][q]["queue"] if t >= 10], QC[q],
                           width=2.2) for q in ("droptail", "red", "codel")}
        rows = [[QN[q], f"{d['util'] * 100:.1f}\\%", f"{d['queue_ms']:.0f} ms", f"{d['p99_ms']:.0f} ms"]
                for q, d in b["deep"].items()]
        tab = grid_table([r"queue", r"busy", r"mean delay", r"99th pct"], rows, widths=[1.6, 1.2, 1.7, 1.5],
                         row_h=0.42, font_size=18, mono_cols=())
        tab.move_to([3.7, 1.4, 0])
        for k, q in enumerate(b["deep"], start=1):
            for j in range(4):
                tab.cells[k][j].set_color(QC[q])
        notes = VGroup(
            wrapped_label(r"\textbf{RED} \ (1993): \ drop with a probability that rises with the \textit{average} "
                          r"queue length, \ before it is full", 5.6, font_size=18, color=KERN),
            wrapped_label(r"\textbf{CoDel} \ (2012): \ watch how long each packet \textit{waited}; \ if the minimum "
                          r"stays above 5 ms for 100 ms, \ drop, \ faster and faster, \ until it falls", 5.6,
                          font_size=18, color=YES),
            wrapped_label(r"a buffer of 1{,}000 packets, \ Reno and CUBIC sharing 10 Mb/s", 5.6, font_size=17,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.7, -1.5, 0])
        with self.voiceover(
            "The cure is to manage the queue, not just size it. Here a buffer of a thousand packets is shared by a "
            "Reno flow and a CUBIC flow on a ten-megabit link. <bookmark mark='a'/> With plain drop-tail, the "
            "flows fill it: more than a second of delay, all the time. <bookmark mark='b'/> Random early detection, "
            "by Sally Floyd and Van Jacobson in 1993, drops packets at random before the queue is full, with a "
            "probability that rises with the average length, so flows back off early. Delay falls to a quarter of "
            "a second. But RED has knobs that depend on the link, and in practice it was rarely switched on. "
            "<bookmark mark='c'/> CoDel, by Kathleen Nichols and Van Jacobson in 2012, has none. It measures how "
            "long each packet waited, and if even the shortest wait stays above five milliseconds for a hundred "
            "milliseconds, it starts dropping, faster and faster, until the queue drains. The mean delay is three "
            "milliseconds instead of a thousand. It gives up some throughput here, eighty-eight percent busy, "
            "because two flows with long round trips refill slowly; with more flows the loss disappears. CoDel and "
            "its descendant, fq_codel, now run in Linux and in many home routers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[2]), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            vo.wait_until("a")
            self.play(Create(traces["droptail"]), FadeIn(VGroup(*tab.cells[1])), run_time=2)
            vo.wait_until("b")
            self.play(Create(traces["red"]), FadeIn(VGroup(*tab.cells[2])), FadeIn(notes[0]), run_time=2)
            vo.wait_until("c")
            self.play(Create(traces["codel"]), FadeIn(VGroup(*tab.cells[3])), FadeIn(notes[1]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def appenzeller(self):
        b = load("buffers")
        head = label(r"Many flows need less buffer", font_size=36).to_edge(UP, buff=0.3)
        app = b["appenzeller"]
        rows = []
        for n in (1, 4, 16, 64):
            a = next(x for x in app if x["n"] == n and x["rule"] == "BDP")
            s = next(x for x in app if x["n"] == n and x["rule"] != "BDP")
            rows.append([f"{n}", f"{a['buffer']}", f"{a['util'] * 100:.1f}\\%", f"{s['buffer']}",
                         f"{s['util'] * 100:.1f}\\%"])
        tab = grid_table([r"flows $n$", r"BDP", r"busy", r"$\text{BDP}/\sqrt{n}$", r"busy"], rows,
                         widths=[1.6, 1.4, 1.5, 2.2, 1.5], row_h=0.44, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for k in range(1, 5):
            tab.cells[k][3].set_color(YES)
            tab.cells[k][4].set_color(YES)
        lines = VGroup(
            wrapped_label(r"100 Mb/s, \ round trips of 80 to 120 ms: \ BDP = 833 packets", 12.4, font_size=20,
                          color=GREY_A),
            wrapped_label(r"one flow's window swings by half; \ $n$ unsynchronized flows' windows swing "
                          r"independently, \ and their \textit{sum} varies only by about $1/\sqrt{n}$ of it \ "
                          r"(the central limit theorem, \ Part 27)", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"Appenzeller, Keslassy and McKeown \ (2004): \ a backbone link carrying 10{,}000 flows "
                          r"needs a hundredth of the classic buffer", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "At the other end of the Internet, the backbone, the rule of one bandwidth-delay product had become "
            "expensive: at a hundred gigabits a second, a quarter-second of buffer is three gigabytes of very fast "
            "memory per port. <bookmark mark='a'/> In 2004 Guido Appenzeller, Isaac Keslassy and Nick McKeown "
            "pointed out that the rule was derived for one flow. One flow's window swings by half. But many flows, "
            "out of step with each other, swing independently, and their total varies only by about one over the "
            "square root of n as much: the central limit theorem. So the buffer can shrink by the square root of "
            "n. <bookmark mark='b'/> We checked. With one flow, both rules are the same. With sixty-four flows, a "
            "buffer an eighth the size keeps the link ninety-seven and a half percent busy, against ninety-eight "
            "and a half with the full one. <bookmark mark='c'/> A backbone link carrying ten thousand flows needs a "
            "hundredth of the old buffer, and router designers took notice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (CCC, HEAD, LAM, SEG, WIN)
