from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (DATA, ETH, HEAD, IPC, KERN, LAM, NO, PART, PAY, UDPC, YES, box, grid_table,
                                   header_strip, load)


class Layers(VoiceoverScene):
    def construct(self):
        self.card()
        self.stack()
        self.hourglass()
        self.end_to_end()

    def card(self):
        card = chapter_card(2, r"Layers", r"How do you build a network out of networks?", lit=(1984, 1988),
                            extra=((1984, r"Saltzer, \ Reed and Clark: \ end to end"),
                                   (1988, r"Clark: \ the design philosophy")), part=PART)
        with self.voiceover("Chapter two. Layers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def stack(self):
        head = label(r"Each layer talks to its peer, \ through the layer below", font_size=34).to_edge(UP, buff=0.3)
        names = [("application", PAY), ("transport", UDPC), ("network", IPC), ("link", ETH), ("physical", GREY_B)]

        def column(k, x):
            g = VGroup(*[box(2.1, 0.5, rf"\text{{{n}}}", c, font_size=17) for n, c in names[5 - k:]])
            g.arrange(DOWN, buff=0.08).move_to([x, 0.4, 0]).align_to([0, 1.7, 0], UP)
            g.shift(DOWN * (0.58 * (5 - k)))
            return g
        h1 = column(5, -4.6)
        rt = column(3, 0)
        h2 = column(5, 4.6)
        cap = VGroup(label(r"Pebble 1", font_size=19, color=GREY_A).next_to(h1, UP, buff=0.12),
                     label(r"a router", font_size=19, color=GREY_A).next_to(rt, UP, buff=0.12),
                     label(r"Pebble 2", font_size=19, color=GREY_A).next_to(h2, UP, buff=0.12))
        wire = VGroup(Line(h1[-1].get_right(), rt[-1].get_left(), color=GREY_B),
                      Line(rt[-1].get_right(), h2[-1].get_left(), color=GREY_B))
        steps = [header_strip([("data", 16, PAY)], unit=0.1, min_w=1.0, font=15),
                 header_strip([("UDP", 8, UDPC), ("data", 16, PAY)], unit=0.1, min_w=0.8, font=15),
                 header_strip([("IP", 20, IPC), ("UDP", 8, UDPC), ("data", 16, PAY)], unit=0.1, min_w=0.8, font=15),
                 header_strip([("Eth", 14, ETH), ("IP", 20, IPC), ("UDP", 8, UDPC), ("data", 16, PAY), ("FCS", 4, ETH)],
                              unit=0.1, min_w=0.7, font=15)]
        for s in steps:
            s.move_to([0, -2.4, 0])
        lines = VGroup(
            label(r"\textbf{encapsulation}: \ going down, \ each layer adds a header; \ going up, \ each removes "
                  r"its own", font_size=20, color=WHITE),
            label(r"a router looks only as high as IP: \ it unwraps the frame, \ chooses the next link, \ and "
                  r"wraps a new one", font_size=20, color=IPC),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Networks are built in layers, each a service for the one above. <bookmark mark='a'/> At the top, the "
            "application, here our sixteen bytes. Below it, transport, which delivers to the right program; network, "
            "which moves packets between machines anywhere; link, which moves frames across one cable; and the "
            "physical layer, which turns bits into signals. <bookmark mark='b'/> Sending, each layer wraps what it "
            "is given in its own header: data, then a UDP header, then IP, then an Ethernet frame. "
            "<bookmark mark='c'/> Each layer's header is read only by the same layer at the other end, as if the two "
            "talked directly. <bookmark mark='d'/> A router in the middle implements only the bottom three. It strips "
            "the frame, reads the IP header to choose the next link, and wraps the packet in a new frame for that "
            "link."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(h1), FadeIn(h2), FadeIn(rt), FadeIn(cap), FadeIn(wire))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            for a, b in zip(steps, steps[1:]):
                self.play(ReplacementTransform(a, b), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]), Indicate(rt, color=IPC))
        self.wait(0.3)
        self.clear_scene()

    def hourglass(self):
        la = load("layers")
        head = label(r"The hourglass", font_size=36).to_edge(UP, buff=0.3)
        tiers = [
            ([r"web", r"mail", r"video", r"DNS", r"games"], PAY, 1.8),
            ([r"TCP", r"UDP", r"QUIC"], UDPC, 0.8),
            ([r"IP"], IPC, -0.1),
            ([r"Ethernet", r"Wi-Fi", r"5G", r"fibre", r"DSL"], ETH, -1.0),
        ]
        glass = VGroup()
        for items, c, y in tiers:
            row = VGroup(*[box(max(1.0, 0.2 * len(t) + 0.6), 0.5, rf"\text{{{t}}}", c, font_size=17) for t in items])
            row.arrange(RIGHT, buff=0.15).move_to([-2.6, y, 0])
            glass.add(row)
        rows = [[str(r["payload"]), str(r["wire"]), f"{r['efficiency']:.0%}".replace("%", r"\%")] for r in la["rows"]]
        tab = grid_table([r"UDP payload, \ bytes", r"on the wire", r"efficiency"], rows, widths=[2.6, 1.8, 1.6],
                         row_h=0.38, font_size=18, mono_cols=())
        tab.move_to([3.8, 0.6, 0])
        tl = label(r"the price of the envelopes \ (with preamble and gap)", font_size=17, color=GREY_A)
        tl.next_to(tab, UP, buff=0.15)
        lines = VGroup(
            label(r"one protocol in the waist: \ anything above runs over anything below", font_size=21,
                  color=IPC),
            label(r"so new applications and new links arrive without anyone's permission; \ the waist itself "
                  r"barely changes \ (IPv6, \ specified in 1998, \ is still not universal)", font_size=19, color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Draw the protocols the Internet actually uses, layer by layer, and the picture is an hourglass. "
            "<bookmark mark='a'/> Many applications on top; a few transports; many kinds of link at the bottom. And "
            "in the middle, at the waist, exactly one protocol: IP. <bookmark mark='b'/> Because everything speaks "
            "IP, any application runs over any link. Wi-Fi and 5G arrived without changing the web, and the web "
            "arrived without changing Ethernet. The cost is that the waist itself is almost impossible to change: "
            "IPv6 was specified in 1998, and the Internet is still moving to it. <bookmark mark='c'/> And envelopes cost bytes: sixteen "
            "bytes of data take eighty-four on the wire, a fifth efficient; full-sized packets are ninety-six "
            "percent."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in glass], lag_ratio=0.3), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()

    def end_to_end(self):
        la = load("layers")
        head = label(r"The end-to-end argument", font_size=36).to_edge(UP, buff=0.3)
        quote = label(r"``The function in question can completely and correctly be implemented only with the "
                      r"knowledge and help of the application standing at the end points''", font_size=20,
                      color=GREY_A).next_to(head, DOWN, buff=0.4)
        if quote.width > 12.6:
            quote.width = 12.6
        cite = label(r"Saltzer, \ Reed and Clark, \ 1984", font_size=17, color=GREY_B).next_to(quote, DOWN, buff=0.1)
        lines = VGroup(
            label(r"copy a file across the network: \ every link checks its frames with a CRC", font_size=21,
                  color=WHITE),
            label(rf"but a router can corrupt a packet \textit{{in its own memory}}: \ say once in "
                  rf"$10^{{{int(round(-__import__('math').log10(la['p_router'])))}}}$ packets", font_size=21,
                  color=NO),
            label(rf"a gigabyte, \ {la['packets']:,} packets, \ {la['hops']} hops: \ "
                  rf"{la['file_bad']:.1%} of copies corrupted, \ every link check passed".replace("%", r"\%"),
                  font_size=21, color=NO),
            label(r"only a check by the two ends \ (a hash of the whole file) \ catches it; \ so the network stays "
                  r"simple, \ and reliability lives at the edges", font_size=21, color=YES),
            label(r"Clark \ (1988): \ the Internet's first goal was to survive failures; \ accounting and quality of "
                  r"service came last", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(cite, DOWN, buff=0.5)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Which layer should do what? In 1984 Jerome Saltzer, David Reed and David Clark gave the answer that "
            "shaped the Internet. <bookmark mark='a'/> Suppose you copy a file across the network, and every link "
            "checks every frame with a CRC. <bookmark mark='b'/> A router can still corrupt a packet while it sits "
            "in the router's own memory, where no link check can see it. Say this happens once in a billion packets. "
            "<bookmark mark='c'/> A gigabyte crosses fifteen hops in seven hundred thousand packets, and about one "
            "copy in a hundred arrives damaged, every link check having passed. <bookmark mark='d'/> Only the two "
            "ends, comparing a checksum of the whole file, can know. So the network can be simple and best-effort, "
            "and the hard guarantees live at the edges. <bookmark mark='e'/> David Clark later wrote down the "
            "priorities: the first goal was to keep working when parts of the network failed. Accounting came last."
        ) as vo:
            self.play(FadeIn(head), FadeIn(quote), FadeIn(cite))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()


_ = (DATA, KERN, LAM)
