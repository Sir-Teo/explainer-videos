from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (BG, DATA, ETH, HEAD, IPC, KERN, LAM, NO, PART, YES)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ Networks I", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"B\log_2(1 + S/N)", font_size=50, color=HEAD), r"Shannon's capacity", HEAD),
            tile(MathTex(r"\frac{1}{2e}", font_size=60, color=NO), r"ALOHA's ceiling", NO),
            tile(MathTex(r"x^{32} + \dots + 1", font_size=48, color=ETH), r"frames and CRCs", ETH),
            tile(MathTex(r"\texttt{/24}", font_size=56, color=IPC), r"prefixes and tries", IPC),
            tile(MathTex(r"1, 2, 3, \dots, 16", font_size=48, color=KERN), r"counting to infinity", KERN),
            tile(MathTex(r"\text{customer} > \text{peer}", font_size=42, color=YES), r"BGP's policies", YES),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Packets instead of circuits, and the layers that wrap them. Shannon's limit "
            "and QAM measured against it. Bit stuffing and CRCs; ALOHA, Ethernet's backoff and Wi-Fi's hidden "
            "terminals; switches that learn and a spanning tree that tames loops. Addresses, prefixes and tries for "
            "forwarding in nanoseconds. Distance vector and its count to infinity, link state and its microloops, "
            "BGP's policies and its hijacks. Our own internet, wireless channels, and networks you can program and "
            "verify."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"TCP: \ a reliable stream over lossy packets, \ and congestion control", [37]),
            (r"agreement among machines that cannot trust the network", [38]),
            (r"replication, \ quorums and CAP over real latencies", [39]),
            (r"HTTP, \ TLS and the browser on top of all this", [42]),
            (r"cloud networks: \ virtual private clouds, \ load balancers, \ CDNs", [45]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 37 builds TCP, a reliable stream on top of packets that can be lost, and the "
            "congestion control that keeps the Internet from collapsing as ALOHA does. Part 38 makes machines agree "
            "over a network that delays and drops messages. Part 39 replicates data across these latencies. Part 42 "
            "puts HTTP and the browser on top. And Part 45 rents networks by the hour, in the cloud."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"addresses", r"plan subnets with CIDR; \ keep private ranges private; \ dual-stack IPv6"),
            (r"diagnosis", r"\texttt{ping}, \ \texttt{traceroute} or \texttt{mtr} for paths; \ \texttt{tcpdump} and "
                           r"Wireshark for packets"),
            (r"MTU", r"when large transfers hang and small ones work, \ suspect a path MTU black hole"),
            (r"Wi-Fi", r"pick uncrowded channels; \ more access points at lower power beat one loud one"),
            (r"BGP", r"filter what customers may announce; \ sign ROAs; \ drop RPKI-invalid routes"),
        ])
        with self.voiceover(
            "In practice. Plan addresses with CIDR, and run IPv6 alongside IPv4. Diagnose with ping and traceroute, "
            "or mtr, which combines them, and look at the packets themselves with tcpdump or Wireshark. When small "
            "transfers work and large ones hang, suspect a link with a smaller MTU whose error messages are being "
            "filtered. For Wi-Fi, choose uncrowded channels, and use several quiet access points rather than one "
            "loud one. And if you run BGP, filter what your customers may announce, sign your routes, and drop "
            "invalid ones."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Derive pure ALOHA's throughput $S = Ge^{-2G}$ and slotted ALOHA's $Ge^{-G}$, \ and their maxima.",
            r"Show that CRC-32 detects every burst of 32 or fewer bits, \ and every odd number of bit errors.",
            r"Prove that synchronous distance vector converges to the shortest distances in at most $n - 1$ rounds "
            r"when costs are positive and nothing changes.",
            r"Show that split horizon prevents every two-node loop but not a three-node one, \ with a counting "
            r"example.",
            r"\textit{Build.} \ Add RIP to our internet: \ periodic distance vectors as real packets; \ cut a link "
            r"and watch packets loop while it counts.",
            r"$\bigstar$ \textit{Research.} \ After a single link failure, \ find an order of router updates under "
            r"which no packet ever loops, \ and the fewest rounds such a schedule needs.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: add the RIP protocol to our internet as real packets, and watch the count to infinity happen "
            "to traffic. The last, marked with a star, is a research problem: after a link fails, in what order "
            "should routers install their new tables so that nothing ever loops, and how fast can that be done?"
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 37, \ Networks II: \ Reliable Conversation", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"a reliable byte stream from unreliable packets", HEAD),
            (r"October 1986: \ the Internet's congestion collapse", NO),
            (r"Jacobson's fix, \ AIMD, \ and why it is fair", YES),
            (r"CUBIC, \ BBR, \ QUIC", LAM))]).arrange(DOWN, buff=0.35)
        q = label(r"the novels, \ fetched over our TCP on a lossy link", font_size=26, color=GREY_A).to_edge(DOWN,
                                                                                                            buff=0.8)
        with self.voiceover(
            "Next time, Part 37: Networks, reliable conversation. IP loses, reorders and duplicates packets, and TCP "
            "turns that into a reliable stream. In October 1986 the Internet collapsed under its own traffic, and Van "
            "Jacobson's fix, additive increase and multiplicative decrease, is why it still works. We fetch the "
            "novels over our own TCP on a lossy link. Part 37, Networks."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kurose and Ross, \textit{Computer Networking: A Top-Down Approach}; \ Peterson and Davie, "
             r"\textit{Computer Networks}",
             r"Tanenbaum and Wetherall, \textit{Computer Networks}; \ Stevens, \textit{TCP/IP Illustrated}, \ vol. 1",
             r"Bertsekas and Gallager, \textit{Data Networks}; \ Varghese, \textit{Network Algorithmics}; \ Tse and "
             r"Viswanath"],
            [r"Baran \ (1964); \ Cerf and Kahn \ (1974); \ Saltzer, Reed and Clark \ (1984); \ Clark \ (1988)",
             r"Shannon \ (1948); \ Abramson \ (1970); \ Metcalfe and Boggs \ (1976); \ Perlman \ (1985)",
             r"McQuillan et al. \ (1980); \ Gao and Rexford \ (2001); \ Griffin, Shepherd and Wilfong \ (2002)",
             r"McKeown et al., \ OpenFlow \ (2008); \ Bosshart et al., \ P4 \ (2014); \ Kazemian et al. \ (2012); \ "
             r"Fogel et al., \ Batfish \ (2015)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()


_ = (DATA, LAM, NO)
