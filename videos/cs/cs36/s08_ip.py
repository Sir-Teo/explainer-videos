from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (CODE, DATA, HEAD, IPC, KERN, LAM, NO, PART, YES, grid_table, header_strip, load,
                                   mono, num)


class Ip(VoiceoverScene):
    def construct(self):
        self.card()
        self.addresses()
        self.header()
        self.arp()
        self.traceroute()

    def card(self):
        card = chapter_card(7, r"IP", r"How do you name every machine on Earth?", lit=(1981, 1993, 1998),
                            extra=((1981, r"RFC 791: \ IPv4"), (1993, r"CIDR"), (1998, r"IPv6")), part=PART)
        with self.voiceover("Chapter seven. IP."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def addresses(self):
        a = load("ipaddr")
        head = label(r"Addresses and prefixes", font_size=36).to_edge(UP, buff=0.3)
        addr = VGroup(mono("10.4.0.2", 30, IPC),
                      mono("00001010 00000100 00000000 00000010", 20, CODE)).arrange(DOWN, buff=0.15)
        addr.next_to(head, DOWN, buff=0.4)
        bl = label(r"prefix \texttt{10.4.0.0/24}: \ the first 24 bits name the network; \ the rest, \ the host",
                   font_size=19, color=HEAD).next_to(addr, DOWN, buff=0.35)
        agg = VGroup(*[mono(p, 18, DATA) for p in a["aggregate_in"][:4]]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        arrow = Arrow(LEFT, RIGHT, color=GREY_B).scale(0.6)
        out = mono(a["aggregate_out"][0], 20, YES)
        ag = VGroup(agg, arrow, out).arrange(RIGHT, buff=0.4).next_to(bl, DOWN, buff=0.4)
        lines = VGroup(
            label(r"\textbf{CIDR} \ (1993): \ prefixes of any length; \ four neighbouring /24s with one route become "
                  r"one /22", font_size=20, color=YES),
            label(r"\textbf{NAT}: \ a home's machines share one public address; \ the router rewrites ports \ "
                  r"(\texttt{192.168.1.10:51000} $\rightarrow$ \texttt{203.0.113.7:40000})", font_size=20, color=KERN),
            label(rf"IPv4 has $2^{{32}}$, \ about 4.3 billion addresses, \ all allocated; \ IPv6 has $2^{{128}}$: \ "
                  rf"${a['v6_per_m2'] / 10 ** 23:.1f} \times 10^{{23}}$ for every square metre of the Earth",
                  font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "IP names every interface with a thirty-two-bit address, written as four numbers. <bookmark mark='a'/> "
            "The address is read as a prefix and a rest: here the first twenty-four bits name a network, ten dot "
            "four dot zero, and the last eight a machine on it. Routers forward on prefixes, not on single addresses. "
            "<bookmark mark='b'/> Since 1993 prefixes can have any length, and neighbouring prefixes that go the "
            "same way can be merged into one shorter prefix, which keeps routing tables small. "
            "<bookmark mark='c'/> Four billion addresses turned out not to be enough. Most homes now share a single "
            "public address through network address translation, the router rewriting ports on the way out and "
            "back. <bookmark mark='d'/> IPv6 has a hundred and twenty-eight bits: enough for about seven times ten "
            "to the twenty-three addresses for every square metre of the planet."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(addr), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(ag), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def header(self):
        a = load("ipaddr")
        head = label(r"The IPv4 header", font_size=36).to_edge(UP, buff=0.3)
        strip = header_strip([("ver, len", 1, IPC), ("TOS", 1, IPC), ("length", 2, IPC), ("ID", 2, KERN),
                              ("flags, offset", 2, KERN), ("TTL", 1, NO), ("proto", 1, IPC), ("checksum", 2, IPC),
                              ("source", 4, DATA), ("destination", 4, DATA)], unit=0.55, min_w=0.9, font=16)
        strip.next_to(head, DOWN, buff=0.5)
        if strip.width > 13:
            strip.width = 13
        fr = a["fragments"]
        rows = [[str(i + 1), str(o), f"{o * 8}", str(n), "yes" if m else "no"] for i, (o, n, m) in enumerate(fr)]
        tab = grid_table([r"fragment", r"offset \ (8-byte units)", r"bytes from", r"length", r"more?"], rows,
                         widths=[1.6, 2.8, 1.8, 1.4, 1.2], row_h=0.4, font_size=18, mono_cols=())
        tab.next_to(strip, DOWN, buff=0.5).set_x(0)
        tl = label(r"4{,}000 bytes through a 1{,}500-byte MTU", font_size=18, color=KERN).next_to(tab, UP, buff=0.1)
        lines = VGroup(
            label(r"\textbf{TTL}: \ each router subtracts one, \ and drops the packet at zero: \ a loop cannot "
                  r"circulate for ever", font_size=20, color=NO),
            label(r"\textbf{fragmentation}: \ a router may split a packet that is too big for the next link; \ only "
                  r"the destination reassembles", font_size=20, color=KERN),
            label(r"today hosts discover the path's MTU and avoid fragments; \ IPv6 routers never fragment",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Every IP packet starts with twenty bytes. <bookmark mark='a'/> A version, a length, an identifier, the "
            "protocol inside, a checksum of the header, and the two addresses. <bookmark mark='b'/> And a time to "
            "live: every router subtracts one, and a router that brings it to zero drops the packet. That is what "
            "keeps a routing loop from circulating a packet for ever, the safeguard Ethernet frames lack. "
            "<bookmark mark='c'/> A packet too big for the next link can be cut into fragments, each with its own "
            "header, its offset in units of eight bytes, and a flag saying more follow; only the destination puts "
            "them back together. <bookmark mark='d'/> Fragments cause trouble, a lost one ruins the whole packet, so "
            "modern hosts discover the smallest link size on the path instead."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in strip], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Indicate(strip[5], color=NO), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(tl), FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def arp(self):
        head = label(r"Two kinds of address, \ hop by hop", font_size=36).to_edge(UP, buff=0.3)
        rows = [["Pebble 1 $\\rightarrow$ San Francisco", "02:00:..:01:01", "router sfo, \\ port 1", "10.1.0.2", "10.4.0.2", "64"],
                ["San Francisco $\\rightarrow$ New York", "sfo, port 2", "nyc, port 1", "10.1.0.2", "10.4.0.2", "63"],
                ["New York $\\rightarrow$ Paris", "nyc, port 3", "par, port 1", "10.1.0.2", "10.4.0.2", "62"],
                ["Paris $\\rightarrow$ Frankfurt", "par, port 2", "fra, port 1", "10.1.0.2", "10.4.0.2", "61"]]
        tab = grid_table([r"hop", r"MAC source", r"MAC destination", r"IP source", r"IP destination", r"TTL"], rows,
                         widths=[3.8, 2.0, 2.0, 1.6, 1.8, 0.8], row_h=0.44, font_size=17, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        for r in range(1, 5):
            for c in (1, 2):
                tab.cells[r][c].set_color(KERN)
            for c in (3, 4):
                tab.cells[r][c].set_color(IPC)
        lines = VGroup(
            label(r"the IP addresses name the two ends, \ and do not change; \ the MAC addresses name this cable's two "
                  r"ends, \ and change at every hop", font_size=20, color=WHITE),
            label(r"\textbf{ARP}: \ to send to the gateway \texttt{10.1.0.1}, \ broadcast ``who has 10.1.0.1?''; \ "
                  r"its owner replies with its MAC, \ and the answer is cached", font_size=20, color=KERN),
            label(r"nothing authenticates the reply: \ \textit{ARP spoofing} lets a neighbour impersonate the gateway "
                  r"on the local network", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "A packet carries two pairs of addresses, and they do different jobs. <bookmark mark='a'/> Follow our "
            "datagram hop by hop. The IP addresses, Pebble 1 to Pebble 2, never change; only the time to live "
            "counts down. But the Ethernet addresses change at every hop: each frame is addressed from this cable's "
            "sender to this cable's receiver, the next router. <bookmark mark='b'/> How does Pebble 1 learn its "
            "router's hardware address? It broadcasts a question on its local network: who has ten dot one dot zero "
            "dot one? The router answers with its MAC address, and Pebble 1 remembers it. That is ARP, the address "
            "resolution protocol. <bookmark mark='c'/> Nothing checks the answer, so on a local network anyone can "
            "claim to be the gateway, which is why switches in offices now watch for false replies."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def traceroute(self):
        h = load("hook")
        head = label(r"Traceroute: \ the TTL trick", font_size=36).to_edge(UP, buff=0.3)
        rows = [[str(t["ttl"]), t["by"], f"{t['ms']:.2f} ms",
                 "time exceeded" if t["by"] != "pebble2" else "echo reply"] for t in h["trace"]]
        tab = grid_table([r"send with TTL", r"reply from", r"after", r"kind"], rows, widths=[2.2, 2.2, 2.2, 3.0],
                         row_h=0.44, font_size=20, mono_cols=(1,))
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        lines = VGroup(
            label(r"send a probe with TTL 1: \ the first router drops it, \ and sends back an ICMP \textit{time "
                  r"exceeded}, \ revealing itself", font_size=20, color=WHITE),
            label(r"TTL 2 reaches the second router; \ and so on, \ until the destination answers", font_size=20,
                  color=HEAD),
            label(r"Van Jacobson, \ 1987: \ a diagnostic built from an error message", font_size=20, color=GREY_A),
            label(r"on the real Internet, \ each line is three probes, \ and some routers stay silent: \ \texttt{* * *}",
                  font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The time to live also gives us traceroute, the tool behind the opening's list of routers. "
            "<bookmark mark='a'/> Send a packet with a time to live of one. The first router decrements it to zero, "
            "drops it, and, as the rules require, sends back an error message, time exceeded, from its own address. "
            "<bookmark mark='b'/> Send another with two, and the second router answers; and so on, until the "
            "destination itself replies. In our simulation: San Francisco, New York, Paris, Frankfurt, and Pebble 2. "
            "<bookmark mark='c'/> Van Jacobson wrote it in 1987, a diagnostic built entirely out of an error "
            "message. <bookmark mark='d'/> On the real Internet some routers decline to answer, and traceroute prints "
            "stars."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]), FadeIn(tab.cells[0][3]),
                      FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[1]], FadeIn(lines[0]))
            vo.wait_until("b")
            for r in tab.cells[2:]:
                self.play(*[FadeIn(c) for c in r], run_time=0.4)
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()


_ = (LAM, num, YES)
