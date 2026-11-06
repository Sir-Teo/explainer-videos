from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (CODE, ETH, HEAD, IPC, NO, PART, PAY, UDPC, YES, grid_table, header_strip, load,
                                   mono, world)


class Hook(VoiceoverScene):
    def construct(self):
        self.datagram()
        self.journey()
        self.plan()

    def datagram(self):
        h = load("hook")
        head = label(r"Sixteen bytes to Frankfurt", font_size=36).to_edge(UP, buff=0.3)
        msg = mono(f'"{h["payload"]}"', 26, PAY).next_to(head, DOWN, buff=0.5)
        strip = header_strip([("Ethernet", 14, ETH), ("IP", 20, IPC), ("UDP", 8, UDPC), ("data", 16, PAY),
                              ("pad", 2, GREY_B), ("FCS", 4, ETH)], unit=0.17, min_w=0.75, font=18)
        strip.next_to(msg, DOWN, buff=0.6)
        hexs = h["frame"]
        rows = [" ".join(hexs[i:i + 2] for i in range(j, min(j + 32, len(hexs)), 2)) for j in range(0, len(hexs), 32)]
        dump = VGroup(*[mono(r, 17, CODE) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        dump.next_to(strip, DOWN, buff=0.5)
        lines = VGroup(
            label(r"64 bytes on the wire for 16 of message: \ each layer wraps the one inside it", font_size=21,
                  color=WHITE),
            label(rf"the IP header's checksum \ \texttt{{{h['ip_checksum']}}}; \ the frame's CRC-32 \ "
                  rf"\texttt{{{h['fcs']}}}", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Pebble 1, a computer in San Francisco, sends sixteen bytes to Pebble 2 in Frankfurt: call me Ishmael. "
            "<bookmark mark='a'/> By the time they leave the machine they are sixty-four bytes. The message is "
            "wrapped in a UDP header, which names the program it is for; that in an IP header, which names the "
            "machine; that in an Ethernet frame, which names the next box on the cable, and ends with a checksum. "
            "<bookmark mark='b'/> Here are the actual bytes, as our network builds them. <bookmark mark='c'/> Every "
            "layer adds its own envelope, and every one of them is there for a reason this part will find."
        ) as vo:
            self.play(FadeIn(head), FadeIn(msg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in strip], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(dump))
            vo.wait_until("c")
            self.play(FadeIn(lines))
        self.wait(0.3)
        self.clear_scene()

    def journey(self):
        h = load("hook")
        it = load("internet")
        head = label(r"Across a simulated internet", font_size=36).to_edge(UP, buff=0.3)
        w = world(it["cities"], it["links"], scale=1.0, shift=UP * 0.6)
        path = [x for x in h["path"] if x in it["cities"]][::-1]
        hops = VGroup(*[Line(w.pos[a], w.pos[b], color=YES, stroke_width=5) for a, b in zip(path, path[1:])])
        rows = [[str(t["ttl"]), t["by"], f"{t['ms']:.1f} ms"] for t in h["trace"]]
        tab = grid_table([r"TTL", r"answered by", r"round trip"], rows, widths=[1.1, 2.2, 2.0], row_h=0.36,
                         font_size=18, mono_cols=(1,))
        tab.to_corner(DL, buff=0.5)
        lines = VGroup(
            label(rf"ping: \ {h['ping_ms']:.2f} ms \ round trip", font_size=22, color=YES),
            label(rf"{h['route_km']:,.0f} km of fibre each way: \ light in glass needs {h['light_ms']:.2f} ms",
                  font_size=20, color=HEAD),
            label(r"the network adds almost nothing; \ the speed of light is the bill", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(tab, RIGHT, buff=0.7).align_to(tab, DOWN)
        with self.voiceover(
            "The bytes cross an internet that we simulate in this part: eight cities, ten cables, routers that "
            "forward by the rules real routers use. <bookmark mark='a'/> The route: San Francisco to New York, "
            "across the Atlantic to Paris, on to Frankfurt. <bookmark mark='b'/> Traceroute reveals it, by a trick "
            "we will meet in chapter seven, router by router: forty-six milliseconds to New York and back, a hundred "
            "and three to Paris, a hundred and eight to Frankfurt. <bookmark mark='c'/> And here is the surprise. "
            "Eleven thousand kilometres of glass, there and back, at two thirds of the speed of light, take a hundred "
            "and eight milliseconds. The routers and queues add almost nothing. The network is as fast as physics "
            "allows; what is hard is everything else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in hops], lag_ratio=0.6), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(lines))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Networks I: \ Moving Bits", font_size=44).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"packets instead of circuits, \ and the layers that carry them",
            r"Shannon's limit, \ and how close real signals get",
            r"framing, \ checksums, \ and sharing one channel: \ ALOHA to Ethernet",
            r"switches, \ IP addresses, \ and forwarding at line rate",
            r"routing: \ distance vector, \ link state, \ and BGP's policies",
            r"our own internet, \ wireless, \ and programmable networks",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 36 of Computer Science, Built: Networks, moving bits, the first part of the act about many "
            "machines. <bookmark mark='a'/> We start with the idea of the packet, and the layers that carry it. We "
            "derive what limits each layer: Shannon's capacity for a wire, a checksum's power, the throughput of a "
            "shared channel. We build switches, addresses and a forwarding table, then the three ways the Internet "
            "routes: distance vector, link state, and BGP, the protocol that holds the Internet's networks together "
            "and that can be hijacked. And we finish with our own internet, wireless, and networks you can program."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (NO,)
