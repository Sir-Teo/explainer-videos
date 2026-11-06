from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (BG, CCC, DATA, HEAD, KERN, LAM, NO, PART, WIN, YES)


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
        head = label(rf"Part {PART}: \ Networks II", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"W \le S/2", font_size=56, color=DATA), r"sequence space", DATA),
            tile(MathTex(r"\text{SRTT} + 4\,\text{RTTVAR}", font_size=40, color=LAM), r"timers that learn", LAM),
            tile(MathTex(r"x \to x + a,\ \ x \to bx", font_size=42, color=YES), r"AIMD, \ proved fair", YES),
            tile(MathTex(r"\frac{\text{MSS}}{\text{RTT}}\sqrt{\frac{3}{2p}}", font_size=46, color=CCC["reno"]),
                 r"the Mathis formula", CCC["reno"]),
            tile(MathTex(r"x_r = 1/q_r", font_size=52, color=WIN), r"prices on links", WIN),
            tile(MathTex(r"k^{-1.22}", font_size=56, color=KERN), r"Zipf, \ and caches", KERN),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Reliable delivery from nothing: stop-and-wait, the alternating bit, and "
            "windows, with the exact number of sequence numbers they need. TCP's handshake, its cookies and its "
            "timers. The collapse of 1986, reproduced, and Jacobson's cure, with Chiu and Jain's proof that it is "
            "fair. The Mathis formula, measured; queues, bufferbloat and CoDel; CUBIC and BBR; and Kelly's theorem "
            "that all of this is an optimization algorithm, with prices on links. Then names, the web over QUIC, "
            "and caches shaped by Zipf's law."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"agreeing over a network that loses and delays messages: \ Paxos and Raft", [38]),
            (r"replication and quorums across these round trips; \ MapReduce over the network", [39]),
            (r"HTTP, \ TLS and the browser on top of QUIC", [42]),
            (r"load balancers, \ CDNs and anycast in the cloud", [45]),
            (r"retries, \ timeouts, \ backoff and load shedding in services: \ CoDel again", [49, 50]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 38 asks machines to agree over a network that loses and delays messages, "
            "where a timeout can never tell a dead machine from a slow one. Part 39 replicates data across these "
            "round trips, and runs the Job on many machines. Part 42 builds the browser on top of QUIC and TLS. "
            "Part 45 rents load balancers and content networks by the hour. And Parts 49 and 50 find retries, "
            "backoff and CoDel's ideas inside every large service."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"long fat paths", r"raise socket buffers to the bandwidth--delay product; \ try BBR \ "
                                r"(\texttt{sysctl net.ipv4.tcp\_congestion\_control=bbr})"),
            (r"latency", r"enable \texttt{fq\_codel} or CAKE on home routers; \ shape just below the link rate"),
            (r"connections", r"reuse them: \ keep-alive, \ pools, \ HTTP/2 or HTTP/3; \ each new one costs round "
                             r"trips and a slow start"),
            (r"diagnosis", r"\texttt{ss -ti} shows cwnd, \ RTT and retransmits; \ Wireshark's stream graphs; \ "
                           r"\texttt{iperf3} for capacity"),
            (r"DNS", r"choose TTLs on purpose; \ validate DNSSEC; \ watch resolver hit rates"),
        ])
        with self.voiceover(
            "In practice. On long, fast paths, make sure socket buffers can hold a bandwidth-delay product, and try "
            "BBR, which on Linux is one setting. At home, turn on fq_codel or CAKE, shaping just below the link's "
            "rate, and bufferbloat disappears. Reuse connections: every new one costs round trips and a slow start. "
            "To see what TCP is doing, ss with the t and i flags shows each connection's window, round trip and "
            "retransmissions, and Wireshark draws its sequence numbers over time. And choose DNS times to live on "
            "purpose."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that Selective Repeat with sequence numbers mod $S$ is correct iff $W \le S/2$, \ and Go-Back-N iff "
            r"$W \le S - 1$, \ on a FIFO channel that may lose packets.",
            r"Derive the Mathis formula; \ then redo it when every loss is detected only by a timeout of 2 RTT.",
            r"Show that AIAD and MIMD preserve, \ respectively, \ the difference and the ratio of two users' rates; \ "
            r"prove AIMD converges for any $a > 0$, $0 < b < 1$.",
            r"Solve Kelly's problem with log utilities on three links in a row \ (a long flow and three short ones) "
            r"\ by hand, \ and check the prices.",
            r"\textit{Build.} \ Add delayed ACKs \ (one ACK per two segments) \ to our TCP: \ what happens to slow "
            r"start, \ to Mathis's constant, \ and to BBR's bandwidth estimate?",
            r"$\bigstar$ \textit{Research.} \ On our dumbbell with ACK jitter up to $D$, \ find the least mean queueing "
            r"delay any algorithm you can design needs to keep two flows' Jain index above 0.9; \ plot it against "
            r"$D$, \ and compare with the 2022 starvation bound.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: add delayed acknowledgements to our TCP, as real receivers do, and see what breaks. The last, "
            "marked with a star, is a research problem: how much queueing delay must any algorithm accept to stay "
            "fair when one flow's path is noisy? Measure the curve, and compare it with the starvation theorem."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 38, \ Distributed Systems I: \ Agreement", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"the two generals cannot agree over a lossy link", NO),
            (r"Lamport clocks, \ vector clocks, \ consistent snapshots", HEAD),
            (r"FLP: \ consensus is impossible in an asynchronous system", KERN),
            (r"Paxos and Raft, \ built and attacked", YES))]).arrange(DOWN, buff=0.35)
        q = label(r"Raft on our network, \ under partitions and crashes", font_size=26, color=GREY_A).to_edge(
            DOWN, buff=0.8)
        with self.voiceover(
            "Next time, Part 38: Distributed systems, agreement. Over the lossy network of this part, two generals "
            "can never be sure they agree, and with no clock in common, even the order of events is a matter of "
            "definition. Fischer, Lynch and Paterson proved that consensus is impossible when messages can be "
            "arbitrarily slow. Paxos and Raft reach it anyway, and we build Raft on our network and try to break "
            "it. Part 38, Agreement."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kurose and Ross, \textit{Computer Networking}, \ ch. 2--3; \ Peterson and Davie, \ ch. 5--6",
             r"Stevens, \textit{TCP/IP Illustrated}, \ vol. 1; \ Grigorik, \textit{High Performance Browser "
             r"Networking}",
             r"Srikant and Ying, \textit{Communication Networks}; \ Kelly and Yudovina, \textit{Stochastic "
             r"Networks}"],
            [r"Bartlett et al. \ (1969); \ Cerf and Kahn \ (1974); \ Karn and Partridge \ (1987); \ Jacobson \ "
             r"(1988); \ Chiu and Jain \ (1989)",
             r"Mathis et al. \ (1997); \ Kelly, Maulloo and Tan \ (1998); \ Low \ (2003); \ Appenzeller et al. \ "
             r"(2004)",
             r"Floyd and Jacobson \ (1993); \ Brakmo and Peterson \ (1994); \ Ha, Rhee and Xu \ (2008); \ Nichols "
             r"and Jacobson \ (2012)",
             r"Cardwell et al. \ (2016); \ Langley et al. \ (2017); \ Mockapetris \ (1987); \ Che et al. \ (2002); "
             r"\ Arun et al. \ (2022)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (HEAD, LAM, NO, YES)
