from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (CCC, DATA, HEAD, KERN, LAM, NO, PART, SEG, WIN, YES, axes, load, trace)


class Collapse(VoiceoverScene):
    def construct(self):
        self.card()
        self.story()
        self.ours()
        self.jacobson()
        self.slow_start()

    def card(self):
        card = chapter_card(6, r"Congestion collapse", r"What happens when everyone sends as fast as the receiver "
                            r"allows?", lit=(1984, 1988), extra=((1984, r"Nagle: \ congestion collapse"),
                                                                 (1986, r"October: \ 32 kb/s $\to$ 40 b/s"),
                                                                 (1988, r"Jacobson: \ Congestion Avoidance \\ and "
                                                                        r"Control")), part=PART)
        with self.voiceover("Chapter six. Congestion collapse."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def story(self):
        c = load("collapse")
        h = c["history"]
        head = label(r"October 1986", font_size=36).to_edge(UP, buff=0.3)
        lbl = Dot([-4.0, 1.0, 0], radius=0.12, color=HEAD)
        ucb = Dot([4.0, 1.0, 0], radius=0.12, color=DATA)
        ll = label(r"Lawrence Berkeley Lab", font_size=20, color=HEAD).next_to(lbl, UP, buff=0.12)
        ul = label(r"UC Berkeley", font_size=20, color=DATA).next_to(ucb, UP, buff=0.12)
        link = Line(lbl.get_center(), ucb.get_center(), color=GREY_C, stroke_width=3)
        dist = label(r"400 yards, \ three hops", font_size=18, color=GREY_B).next_to(link, DOWN, buff=0.12)
        before = label(rf"normal: \ {h['before_bps'] // 1000} kb/s", font_size=28, color=YES).move_to([-2.4, -0.8, 0])
        after = label(rf"October 1986: \ {h['after_bps']} b/s", font_size=28, color=NO).move_to([2.4, -0.8, 0])
        ratio = label(r"a thousandfold drop, \ with every link busy", font_size=24, color=WHITE).move_to([0, -1.8, 0])
        why = wrapped_label(r"every TCP sent a full window as fast as the receiver allowed; \ queues overflowed; \ "
                            r"timers, \ blind to queueing, \ fired; \ the links filled with \textbf{copies} of "
                            r"packets that were not lost", 12.4, font_size=21, color=KERN).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In October 1986, the link between the Lawrence Berkeley Laboratory and the University of California "
            "at Berkeley, four hundred yards and three routers apart, normally carried thirty-two kilobits a "
            "second. <bookmark mark='a'/> Then, for days, it carried forty bits a second. A thousandfold drop, and "
            "the links were not idle: they were completely busy. <bookmark mark='b'/> Every TCP of the time sent a "
            "full window as fast as the receiver allowed, with no thought for the network in between. Queues in the "
            "routers overflowed and dropped packets. Retransmission timers, which did not account for time spent "
            "waiting in queues, fired for packets that were only delayed. And the links filled with copies of "
            "packets that had not been lost, each one making the queues longer and the next timeouts more likely. "
            "John Nagle had predicted this, and named it, two years earlier: congestion collapse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lbl), FadeIn(ucb), FadeIn(ll), FadeIn(ul), Create(link), FadeIn(dist))
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(FadeIn(after), FadeIn(ratio))
            vo.wait_until("b")
            self.play(FadeIn(why))
        self.wait(0.4)
        self.clear_scene()

    def ours(self):
        c = load("collapse")
        head = label(r"1986 in miniature", font_size=36).to_edge(UP, buff=0.3)
        rows = c["rows"]
        g = axes([2, 8, 1], [0, 2.1, 0.5], x_length=7.4, y_length=4.0, x_label=r"total window offered \ (packets, "
                 r"log scale)", y_label=r"goodput: \ new data delivered, \ Mb/s",
                 xticks=range(3, 8), yticks=(0.5, 1.0, 1.5, 2.0), fx=lambda v: f"{2 ** int(v)}",
                 fy=lambda v: f"{v:.1f}").move_to([-2.4, -0.5, 0])
        ax = g.ax
        X = [math.log2(r["offered"]) for r in rows]
        fx = VGroup(trace(ax, [(x, r["fixed"]) for x, r in zip(X, rows)], NO, width=3.2),
                    *[Dot(ax.c2p(x, r["fixed"]), radius=0.06, color=NO) for x, r in zip(X, rows)])
        rn = VGroup(trace(ax, [(x, r["reno"]) for x, r in zip(X, rows)], CCC["reno"], width=3.2),
                    *[Dot(ax.c2p(x, r["reno"]), radius=0.06, color=CCC["reno"]) for x, r in zip(X, rows)])
        limit = c["pipe"] * (1 + (c["rto"] - 0.1) / 0.1)       # queueing beyond this outlasts the timer
        pl = DashedLine(ax.c2p(math.log2(limit), 0), ax.c2p(math.log2(limit), 2.05), color=GREY_B, dash_length=0.1)
        pll = label(r"queueing delay $>$ timer $-$ RTT", font_size=16, color=GREY_B).next_to(pl, UP, buff=0.05)
        cliff = next(r for r in rows if r["fixed"] < 1.5 and r["offered"] > 24)
        side = VGroup(
            wrapped_label(r"four flows share a 2 Mb/s link: \ 100 ms round trips, \ a 30-packet queue", 5.0,
                          font_size=19, color=GREY_A),
            wrapped_label(r"\textbf{1986 TCP}: \ a fixed window, \ a fixed timer of 200 ms, \ resend everything on "
                          r"timeout", 5.0, font_size=19, color=NO),
            wrapped_label(rf"past the cliff, \ goodput falls to {cliff['fixed']:.2f} Mb/s while the link stays "
                          rf"{cliff['fixed_util'] * 100:.1f}\% busy: \ {cliff['fixed_retx']:,} retransmissions in a "
                          rf"minute", 5.0, font_size=19, color=WHITE),
            wrapped_label(rf"\textbf{{Jacobson's TCP}} \ (Reno): \ {rows[-1]['reno']:.2f} Mb/s at every load", 5.0,
                          font_size=19, color=CCC["reno"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([4.3, -0.3, 0])
        with self.voiceover(
            "We can make it happen. Four flows share a two-megabit link, with hundred-millisecond round trips and a "
            "queue of thirty packets. <bookmark mark='a'/> Each runs a TCP of 1986: a fixed window, a fixed timer "
            "of two hundred milliseconds, and on a timeout, resend everything outstanding. We raise the window and "
            "measure the goodput, the rate of new data delivered. <bookmark mark='b'/> While the total window is "
            "small, goodput rises with it. Then the windows outgrow the pipe by so much that packets wait in the "
            "queue longer than the timer allows: the timers fire, and copies of waiting packets join the queue "
            "behind them. <bookmark mark='c'/> Goodput falls off a cliff, to a little over one megabit, while the "
            "link stays almost perfectly busy, carrying eleven thousand retransmissions a minute, most of them "
            "packets that were never lost. Our collapse is fifty percent, not a thousandfold, because we have one "
            "hop, not three, and a gentler timer. <bookmark mark='d'/> Now replace each sender with Jacobson's TCP. "
            "Goodput is one point nine four megabits at every load: the link's capacity, minus headers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(pl), FadeIn(pll))
            self.play(Create(fx), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(rn), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def jacobson(self):
        head = label(r"Jacobson's principle: \ conservation of packets", font_size=34).to_edge(UP, buff=0.3)
        pipe = RoundedRectangle(width=9.0, height=1.0, corner_radius=0.5, stroke_color=GREY_C, stroke_width=2)
        pipe.move_to([0, 1.5, 0])
        pk = VGroup(*[Square(0.4, stroke_width=0, fill_color=SEG, fill_opacity=0.85) for _ in range(9)])
        for i, p in enumerate(pk):
            p.move_to(pipe.get_left() + RIGHT * (0.6 + i * 0.97))
        pl = label(r"in equilibrium: \ a new packet enters only when an old one leaves", font_size=21,
                   color=WHITE).next_to(pipe, DOWN, buff=0.2)
        rules = VGroup(
            wrapped_label(r"\textbf{ACK clocking}: \ each ACK means a packet left the network, \ so send one more: \ "
                          r"the sender's pace becomes the bottleneck's", 12.4, font_size=21, color=YES),
            wrapped_label(r"\textbf{a better timer}: \ SRTT $+ 4$ RTTVAR, \ and Karn's backoff, \ so packets are "
                          r"not resent while they are only waiting", 12.4, font_size=21, color=LAM),
            wrapped_label(r"\textbf{a congestion window} \ \texttt{cwnd}: \ in flight $\le \min(\texttt{cwnd}, "
                          r"\text{receiver's window})$; \ a loss means a queue overflowed, \ so \textbf{halve} it; "
                          r"\ otherwise add one packet per round trip", 12.4, font_size=21, color=WIN),
            wrapped_label(r"\textbf{slow start}: \ reach equilibrium quickly, \ doubling from one packet", 12.4,
                          font_size=21, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(pl, DOWN, buff=0.45)
        with self.voiceover(
            "Van Jacobson, at the Berkeley lab, and Mike Karels diagnosed the collapse and published the cure in "
            "1988. The idea is conservation. <bookmark mark='a'/> A connection in equilibrium should put a new "
            "packet into the network only when an old one leaves it. <bookmark mark='b'/> An ACK is the evidence "
            "that a packet has left, so each ACK releases one new packet. The ACKs return at the rate the "
            "bottleneck delivers, so the sender's pace automatically becomes the bottleneck's. "
            "<bookmark mark='c'/> Conservation fails if packets are resent while still in the network: hence the "
            "timer of the last chapter. <bookmark mark='d'/> And the right amount in flight must be found. A new "
            "variable, the congestion window, limits it. In a network of reliable links, a lost packet almost "
            "always means some queue overflowed, so a loss halves the window, and each round trip without loss "
            "adds one packet. <bookmark mark='e'/> Finally, slow start, to reach equilibrium in the first place."
        ) as vo:
            self.play(FadeIn(head), Create(pipe))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pk], lag_ratio=0.1), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(rules[0]))
            self.play(pk.animate.shift(RIGHT * 0.3), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(rules[1]))
            vo.wait_until("d")
            self.play(FadeIn(rules[2]))
            vo.wait_until("e")
            self.play(FadeIn(rules[3]))
        self.wait(0.4)
        self.clear_scene()

    def slow_start(self):
        s = load("sawtooth")
        head = label(r"Slow start, \ then the sawtooth", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 20, 2], [0, 340, 80], x_length=10.5, y_length=4.2, x_label=r"seconds",
                 y_label=r"congestion window \ (packets)", xticks=range(0, 21, 2), yticks=(80, 160, 240, 320)).move_to(
            DOWN * 0.4)
        ax = g.ax
        tr = trace(ax, s["trace"], CCC["reno"], width=2.8, x_max=20)
        bdp = DashedLine(ax.c2p(0, s["bdp"]), ax.c2p(20, s["bdp"]), color=GREY_B, dash_length=0.1)
        full = DashedLine(ax.c2p(0, s["bdp"] + s["buffer"]), ax.c2p(20, s["bdp"] + s["buffer"]), color=NO,
                          dash_length=0.1)
        bl = label(r"the pipe: \ 83 packets", font_size=17, color=GREY_B).next_to(ax.c2p(20, s["bdp"]), DOWN,
                                                                                buff=0.06).shift(LEFT * 1.2)
        fl = label(r"pipe + buffer: \ a packet is dropped", font_size=17, color=NO).next_to(
            ax.c2p(20, s["bdp"] + s["buffer"]), UP, buff=0.06).shift(LEFT * 1.8)
        notes = VGroup(
            label(r"slow start: \ $+1$ per ACK, \ so the window \textbf{doubles} each round trip", font_size=19,
                  color=KERN),
            label(r"congestion avoidance: \ $+1/\texttt{cwnd}$ per ACK, \ so $+1$ per round trip; \ halve on loss",
                  font_size=19, color=CCC["reno"]),
            label(r"fast retransmit: \ three later ACKs mean a loss, \ no timeout needed", font_size=19,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Here is our Reno, alone on a ten-megabit link with a hundred-millisecond round trip, and a buffer as "
            "large as the pipe. <bookmark mark='a'/> Slow start is not slow: every ACK adds one packet to the "
            "window, so the window doubles each round trip, one, two, four, eight, until a queue overflows. "
            "<bookmark mark='b'/> From then on, congestion avoidance. Each ACK adds one over the window, so the "
            "window grows by one packet per round trip, a straight line, until the buffer overflows again and the "
            "window halves. <bookmark mark='c'/> And Reno does not wait for a timer: when three later packets have "
            "been acknowledged and one has not, that one is presumed lost, and is resent at once. This is the "
            "sawtooth, the heartbeat of the Internet since 1990. With a buffer of one pipe, the halving never "
            "empties the link: utilization is ninety-nine percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(bdp), Create(full), FadeIn(bl), FadeIn(fl))
            vo.wait_until("a")
            self.play(Create(tr), run_time=6, rate_func=linear)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (HEAD, YES)
