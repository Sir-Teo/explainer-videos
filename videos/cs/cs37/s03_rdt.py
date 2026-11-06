from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (ACKC, DATA, HEAD, KERN, LAM, NO, PART, SEG, YES, grid_table, load, seq_diagram)


class Rdt(VoiceoverScene):
    def construct(self):
        self.card()
        self.stop_and_wait()
        self.alternating_bit()
        self.reordering()
        self.utilization()

    def card(self):
        card = chapter_card(2, r"Reliability from scratch", r"How do you make a lossy channel lose nothing?",
                            lit=(1969, 1969), extra=((1969, r"Bartlett, Scantlebury \\ and Wilkinson: \\ the "
                                                            r"alternating bit"),), part=PART)
        with self.voiceover("Chapter two. Reliability from scratch."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def stop_and_wait(self):
        head = label(r"Stop and wait", font_size=36).to_edge(UP, buff=0.3)
        ev = [(0.0, 1.0, r"packet 0", True, SEG), (1.0, 2.0, r"ACK 0", False, ACKC),
              (2.0, None, r"packet 1", True, SEG), (5.0, 6.0, r"packet 1 \ (again)", True, SEG),
              (6.0, 7.0, r"ACK 1", False, ACKC)]
        sd = seq_diagram(ev, t_max=7.6, height=5.2, gap=5.4).move_to([-2.3, -0.45, 0])
        timer = VGroup(
            Line(sd.arrows[2][0].get_start(), sd.arrows[2][0].get_start() + DOWN * (3 / 7.6 * 5.2), color=KERN,
                 stroke_width=5),
        )
        tl = label(r"timer \\ expires", font_size=17, color=KERN).next_to(timer, LEFT, buff=0.1)
        rules = VGroup(
            wrapped_label(r"send one packet; \ start a timer", 4.6, font_size=21, color=SEG),
            wrapped_label(r"the receiver acknowledges each packet it gets", 4.6, font_size=21, color=ACKC),
            wrapped_label(r"no ACK before the timer expires? \ \textbf{send it again}", 4.6, font_size=21,
                          color=KERN),
            wrapped_label(r"a checksum turns corruption into loss, \ so loss is the only failure left to handle",
                          4.6, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([4.4, -0.3, 0])
        with self.voiceover(
            "The simplest protocol that could possibly work. The sender sends one packet and starts a timer. "
            "<bookmark mark='a'/> The receiver, on getting a packet, sends back an acknowledgement, an ACK. When the "
            "ACK arrives, the sender sends the next packet. <bookmark mark='b'/> If a packet is lost, no ACK comes. "
            "<bookmark mark='c'/> The timer expires, and the sender sends the same packet again. "
            "<bookmark mark='d'/> Corruption needs no separate treatment: a checksum detects it, and a corrupted "
            "packet is thrown away, so it becomes a loss. Loss is the only failure left. Retransmission handles it, "
            "as long as the channel delivers something eventually."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd[:4]))
            self.play(FadeIn(sd.arrows[0]), FadeIn(rules[0]))
            vo.wait_until("a")
            self.play(FadeIn(sd.arrows[1]), FadeIn(rules[1]))
            vo.wait_until("b")
            self.play(FadeIn(sd.arrows[2]))
            vo.wait_until("c")
            self.play(Create(timer), FadeIn(tl), FadeIn(rules[2]))
            self.play(FadeIn(sd.arrows[3]), FadeIn(sd.arrows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rules[3]))
        self.wait(0.4)
        self.clear_scene()

    def alternating_bit(self):
        r = load("rdt")
        head = label(r"Lost ACKs, \ and the alternating bit", font_size=36).to_edge(UP, buff=0.3)
        ev = [(0.0, 1.0, r"packet A", True, SEG), (1.0, None, r"ACK", False, ACKC),
              (4.0, 5.0, r"packet A \ (again)", True, SEG), (5.0, 6.0, r"ACK", False, ACKC)]
        sd = seq_diagram(ev, t_max=6.6, height=4.6, gap=5.0).move_to([-3.3, -0.6, 0])
        dup = label(r"a new packet, \ or A again?", font_size=20, color=NO).next_to(sd.arrows[2][0].get_end(), UP,
                                                                              buff=0.35).shift(LEFT * 1.4)
        fix = VGroup(
            wrapped_label(r"the receiver cannot tell a retransmission from new data, \ so it would deliver A twice",
                          5.2, font_size=21, color=NO),
            wrapped_label(r"\textbf{number the packets}: \ but with stop-and-wait only two can be in question at "
                          r"once, \ so \textbf{one bit} is enough: \ 0, 1, 0, 1, \dots", 5.2, font_size=21,
                          color=YES),
            wrapped_label(r"the receiver ACKs the bit it got, \ and delivers a packet only if its bit is the one it "
                          r"expects", 5.2, font_size=21, color=WHITE),
            wrapped_label(rf"our test: \ {r['trials']} runs of 500 packets with 10\% loss on a FIFO channel: \ "
                          rf"{r['fifo_correct']} of {r['trials']} deliver 0 to 499, \ once each, \ in order", 5.2,
                          font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.5, 0])
        with self.voiceover(
            "ACKs can be lost too. <bookmark mark='a'/> Here the packet arrives, but its ACK does not. The sender's "
            "timer expires, and it sends the packet again. <bookmark mark='b'/> To the receiver, this looks exactly "
            "like the next packet. Without more information it delivers the same data twice. "
            "<bookmark mark='c'/> The fix is to number the packets. With stop-and-wait, the receiver is only ever "
            "unsure between the packet it just got and the next one, so a single bit is enough: packets are "
            "numbered zero, one, zero, one. This is the alternating-bit protocol, published in 1969 by Bartlett, "
            "Scantlebury and Wilkinson at Britain's National Physical Laboratory. <bookmark mark='d'/> The receiver "
            "acknowledges the bit it received, and passes a packet up only if its bit is the one expected next. "
            "<bookmark mark='e'/> We tested it: twenty runs of five hundred packets, losing one packet or ACK in "
            "ten. Every run delivered exactly zero to four hundred ninety-nine, once each, in order."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd[:4]), FadeIn(sd.arrows[0]))
            vo.wait_until("a")
            self.play(FadeIn(sd.arrows[1]))
            self.play(FadeIn(sd.arrows[2]))
            vo.wait_until("b")
            self.play(FadeIn(dup), FadeIn(fix[0]))
            vo.wait_until("c")
            self.play(FadeIn(fix[1]), FadeIn(sd.arrows[3]))
            vo.wait_until("d")
            self.play(FadeIn(fix[2]))
            vo.wait_until("e")
            self.play(FadeIn(fix[3]))
        self.wait(0.4)
        self.clear_scene()

    def reordering(self):
        r = load("rdt")
        ex = r["reorder_example"]
        head = label(r"But the Internet reorders", font_size=36).to_edge(UP, buff=0.3)
        ev = [(0.0, 3.6, r"", True, NO), (0.4, 1.4, r"bit 0", True, SEG),
              (1.4, 2.4, r"ACK 0", False, ACKC), (2.4, None, r"bit 1", True, SEG),
              (2.4, 3.4, r"", False, GREY_D)]
        sd = seq_diagram(ev[:4], t_max=4.4, height=4.6, gap=5.0).move_to([-3.3, -0.6, 0])
        old = label(r"old copy, \ bit 0, \ delayed", font_size=17, color=NO).next_to(sd.arrows[0][0].get_end(), LEFT,
                                                                                     buff=0.15)
        sd.arrows[0].add(old)
        lines = VGroup(
            wrapped_label(r"a delayed duplicate of an old packet arrives when the receiver expects that bit again, "
                          r"\ and is delivered as new data", 5.4, font_size=21, color=NO),
            wrapped_label(rf"same test, \ 20\% of packets delayed: \ {r['reorder_correct']} of {r['trials']} runs "
                          rf"correct; \ the first one went wrong at position {ex['first_error']}, \ delivering "
                          rf"packet {ex['wrong']} again", 5.4, font_size=21, color=KERN),
            wrapped_label(r"the bit only works if the channel is FIFO: \ a wire, \ not a network of queues", 5.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"cure: \ \textbf{many} sequence numbers, \ and a maximum lifetime for packets so old "
                          r"numbers can safely be reused \ (TCP: 32 bits, \ and IP's TTL)", 5.4, font_size=21,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.5, -0.5, 0])
        with self.voiceover(
            "That proof of correctness assumed something the Internet does not give: that packets arrive in the "
            "order they were sent. <bookmark mark='a'/> Suppose an old copy of a packet with bit zero is delayed in "
            "some queue. Meanwhile the conversation moves on, and the receiver comes to expect bit zero again. The "
            "old copy arrives, carries the right bit, and is delivered as new data. <bookmark mark='b'/> We repeated "
            "the test with one packet in five delayed. Not one run of twenty was correct; the first went wrong at "
            "position eight, delivering packet six a second time. <bookmark mark='c'/> One bit is enough on a wire, "
            "never on a network of queues. <bookmark mark='d'/> The cure is many sequence numbers, enough that a "
            "number is reused only after any old packet carrying it must be dead. TCP numbers bytes with thirty-two "
            "bits, and IP's time-to-live bounds how long a packet can wander."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd[:4]), FadeIn(sd.arrows[1]), FadeIn(sd.arrows[2]))
            vo.wait_until("a")
            self.play(FadeIn(sd.arrows[0]), FadeIn(sd.arrows[3]))
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.4)
        self.clear_scene()

    def utilization(self):
        r = load("rdt")
        head = label(r"The price of waiting", font_size=36).to_edge(UP, buff=0.3)
        bar = VGroup()
        L, R = 1.2, 10.8
        busy = Rectangle(width=L * 0.5, height=0.55, stroke_width=0, fill_color=SEG, fill_opacity=0.9)
        idle = Rectangle(width=R * 0.5, height=0.55, stroke_color=GREY_D, stroke_width=1.5, fill_opacity=0)
        bar.add(busy, idle.next_to(busy, RIGHT, buff=0))
        bar.move_to([0, 1.8, 0])
        bl = label(r"$L/R$: \ sending", font_size=18, color=SEG).next_to(busy, DOWN, buff=0.12)
        il = label(r"RTT: \ waiting for the ACK", font_size=18, color=GREY_B).next_to(idle, DOWN, buff=0.12)
        eq = MathTex(r"U = \frac{L/R}{\text{RTT} + L/R}", font_size=44, color=HEAD).move_to([-3.6, -0.4, 0])
        rows = [[f"{u['rate']:,} packets/s", f"{u['formula']:.4f}", f"{u['measured']:.4f}"] for u in r["util"]]
        tab = grid_table([r"link, \ RTT 100 ms", r"formula", r"measured"], rows, widths=[3.0, 1.8, 1.8], row_h=0.42,
                         font_size=19, mono_cols=())
        tab.move_to([3.2, -0.3, 0])
        for k in range(1, 4):
            tab.cells[k][2].set_color(YES)
        a = r["atlantic"]
        atl = wrapped_label(rf"San Francisco to Frankfurt at 1 Gb/s: \ a 1{{,}}500-byte packet takes 12 $\mu$s, \ "
                            rf"the round trip 108 ms: \ $U = {a['util']:.5f}$, \ \textbf{{{a['mbps']:.2f} Mb/s}} of a "
                            rf"thousand", 12.4, font_size=22, color=NO).to_edge(DOWN, buff=0.9)
        fix = label(r"the fix: \ keep many packets in flight at once", font_size=24, color=YES).to_edge(DOWN,
                                                                                                    buff=0.3)
        with self.voiceover(
            "Stop-and-wait is correct, and hopeless. <bookmark mark='a'/> Call the packet length L and the link "
            "rate R. Sending takes L over R; then the sender sits idle for a whole round trip, waiting. The fraction "
            "of time the link is busy is L over R, divided by the round trip plus L over R. <bookmark mark='b'/> Our "
            "simulator agrees with the formula to four digits, at every link speed: one tenth, one hundredth, one "
            "thousandth. The faster the link, the worse it gets. <bookmark mark='c'/> Across the Atlantic at a "
            "gigabit a second, a packet takes twelve microseconds to send and a hundred and eight milliseconds to "
            "acknowledge. Stop-and-wait uses a hundredth of a percent of the link: a tenth of a megabit, out of a "
            "thousand. <bookmark mark='d'/> The only way out is not to wait: keep many packets in flight at once."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bar), FadeIn(bl), FadeIn(il))
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(atl))
            vo.wait_until("d")
            self.play(FadeIn(fix))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, HEAD, LAM, YES)
