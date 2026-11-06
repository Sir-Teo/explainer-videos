from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (ACKC, DATA, HEAD, KERN, LAM, NO, PART, SEG, YES, box, grid_table, load, mono)


class Transport(VoiceoverScene):
    def construct(self):
        self.card()
        self.what_ip_does()
        self.ports()
        self.udp_tcp()

    def card(self):
        card = chapter_card(1, r"The transport problem", r"What does a program need that IP does not give?",
                            lit=(1974, 1981), extra=((1974, r"Cerf and Kahn: \ TCP"), (1980, r"Postel: \ UDP"),
                                                     (1981, r"RFC 793")), part=PART)
        with self.voiceover("Chapter one. The transport problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def what_ip_does(self):
        u = load("udp")
        head = label(r"Ten thousand datagrams, \ sent in order", font_size=36).to_edge(UP, buff=0.3)
        seq = u["first"][:20]
        cells = VGroup()
        for k, v in enumerate(seq):
            ok = v == (seq[k - 1] + 1 if k else 0)
            c = SEG if ok else NO
            sq = VGroup(Square(0.52, stroke_color=c, stroke_width=1.8, fill_color=c, fill_opacity=0.2),
                        label(str(v), font_size=18, color=c))
            cells.add(sq)
        cells.arrange(RIGHT, buff=0.06).next_to(head, DOWN, buff=0.6)
        cap = label(r"the first twenty to arrive, \ in arrival order", font_size=19, color=GREY_B).next_to(
            cells, DOWN, buff=0.15)
        rows = [[r"sent", f"{u['sent']:,}"], [r"arrived", f"{u['arrived']:,}"], [r"never arrived", f"{u['lost']}"],
                [r"arrived twice", f"{u['duplicated']}"], [r"arrived after a later one", f"{u['out_of_order']}"]]
        tab = grid_table([r"", r"datagrams"], rows, widths=[4.6, 2.2], row_h=0.42, font_size=21, mono_cols=())
        tab.next_to(cap, DOWN, buff=0.45).set_x(-2.6)
        for r, c in ((3, NO), (4, KERN), (5, LAM)):
            tab.cells[r][1].set_color(c)
        side = VGroup(
            wrapped_label(r"IP promises \textit{best effort}: \ a datagram may be lost, \ duplicated, \ delayed or "
                          r"overtaken", 5.2, font_size=21, color=WHITE),
            wrapped_label(r"queues overflow; \ links flip bits and the CRC discards the frame; \ routes change "
                          r"mid-flow; \ a sender retries on a radio", 5.2, font_size=19, color=GREY_A),
            wrapped_label(r"a program wants a \textit{stream}: \ every byte, \ once, \ in order", 5.2, font_size=21,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -1.5, 0])
        with self.voiceover(
            "Send ten thousand numbered datagrams across a channel like the Internet: one percent loss, an "
            "occasional duplicate, and a few packets held back in a queue while later ones overtake them. "
            "<bookmark mark='a'/> These are the first twenty to arrive. Twelve has been overtaken by seven others. "
            "<bookmark mark='b'/> Of ten thousand, a hundred and nine never arrive, eighteen arrive twice, and two "
            "hundred and eighty-four arrive after a packet sent later. <bookmark mark='c'/> This is all IP "
            "promises: best effort. Queues overflow and drop; a corrupted frame fails its CRC and is thrown away; "
            "routes change in the middle of a transfer; a radio resends a frame whose acknowledgement it missed. "
            "<bookmark mark='d'/> A program reading a file, or a web page, wants something else entirely: a stream "
            "of bytes, every one of them, exactly once, in order. Building that on top of this is the transport "
            "layer's job."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cells], lag_ratio=0.06), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def ports(self):
        head = label(r"Ports: \ which program?", font_size=36).to_edge(UP, buff=0.3)
        host = RoundedRectangle(width=5.6, height=4.2, corner_radius=0.2, stroke_color=GREY_C, stroke_width=1.5)
        host.move_to([3.4, -0.5, 0])
        hl = label(r"Pebble 2 \ (10.4.0.2)", font_size=20, color=GREY_A).next_to(host, UP, buff=0.1)
        progs = VGroup(box(2.2, 0.6, r"web server \ :443", DATA, font_size=18),
                       box(2.2, 0.6, r"DNS \ :53", LAM, font_size=18),
                       box(2.2, 0.6, r"ssh \ :22", KERN, font_size=18)).arrange(DOWN, buff=0.35)
        progs.move_to(host.get_center() + RIGHT * 1.2)
        nic = box(1.2, 2.6, r"IP", HEAD, font_size=20).move_to(host.get_center() + LEFT * 1.8)
        arrows = VGroup(*[Arrow(nic.get_right(), p.get_left(), buff=0.1, color=GREY_B, stroke_width=2) for p in progs])
        four = mono("(203.0.113.7, 51544, 10.4.0.2, 443)", 18, YES).move_to([-3.4, 1.2, 0])
        fl = wrapped_label(r"a connection is named by four numbers: \ source address and port, \ destination "
                           r"address and port", 5.4, font_size=20, color=WHITE).next_to(four, DOWN, buff=0.3)
        udp = VGroup(
            label(r"UDP's whole header: \ 8 bytes", font_size=22, color=LAM),
            mono("src port | dst port | length | checksum", 16, LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-3.4, -1.4, 0])
        with self.voiceover(
            "First, the simplest thing a transport adds. An IP address names a machine, but a machine runs many "
            "programs. <bookmark mark='a'/> A port number, sixteen bits, names the program: four four three for a "
            "web server, fifty-three for names, twenty-two for remote logins. The operating system reads the port "
            "and hands the data to whichever program is listening. <bookmark mark='b'/> A conversation is then "
            "named by four numbers: both addresses and both ports. Your browser picks a fresh source port for each "
            "connection, so many tabs can talk to the same server without confusion. <bookmark mark='c'/> UDP, "
            "David Reed and Jon Postel's user datagram protocol of 1980, adds exactly this and a checksum: eight "
            "bytes of header and no promises. It is what DNS, video calls and games use, and, as we will see at the "
            "end, what the newest web protocol is built on."
        ) as vo:
            self.play(FadeIn(head), Create(host), FadeIn(hl), FadeIn(nic))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(p)) for a, p in zip(arrows, progs)],
                                  lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(four), FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(udp))
        self.wait(0.4)
        self.clear_scene()

    def udp_tcp(self):
        head = label(r"Two contracts", font_size=36).to_edge(UP, buff=0.3)
        rows = [
            [r"delivery", r"maybe", r"every byte, \ or an error"],
            [r"order", r"as it arrives", r"as it was sent"],
            [r"duplicates", r"possible", r"removed"],
            [r"unit", r"a datagram", r"a byte stream"],
            [r"setup", r"none", r"a handshake: \ 1 round trip"],
            [r"rate", r"as fast as you like", r"flow and congestion control"],
            [r"header", r"8 bytes", r"20 bytes \ or more"],
        ]
        tab = grid_table([r"", r"UDP", r"TCP"], rows, widths=[2.6, 3.4, 4.6], row_h=0.5, font_size=21,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for r in range(1, len(rows) + 1):
            tab.cells[r][1].set_color(LAM)
            tab.cells[r][2].set_color(DATA)
            tab.cells[r][0].set_color(GREY_B)
        foot = wrapped_label(r"TCP's promises are made by the two \textit{ends} alone: \ the routers in between keep "
                             r"no state about the conversation \ (Part 36's end-to-end argument)", 12.0, font_size=21,
                             color=YES).next_to(tab, DOWN, buff=0.6)
        with self.voiceover(
            "TCP, the transmission control protocol, makes the other contract. Every byte arrives, or the program "
            "is told the connection failed. Bytes come out in the order they went in, each exactly once. There are "
            "no messages, only a stream. <bookmark mark='a'/> It costs a handshake before any data flows, twenty "
            "bytes of header on every packet, and a sender that sometimes waits when it could send. "
            "<bookmark mark='b'/> And notice who keeps these promises: only the two computers at the ends. The "
            "routers in between know nothing about the conversation, exactly as the end-to-end argument of the last "
            "part said they should not. Everything in the next three chapters happens inside two machines, "
            "talking through a network that will not help."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]),
                      Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(1, 5)], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(5, 8)], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (ACKC, HEAD, YES)
