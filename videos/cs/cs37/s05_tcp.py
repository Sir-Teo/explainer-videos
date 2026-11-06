from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (ACKC, DATA, HEAD, KERN, LAM, NO, PART, SEG, WIN, YES, grid_table, load, mono,
                                   seq_diagram)


class Tcp(VoiceoverScene):
    def construct(self):
        self.card()
        self.header()
        self.handshake()
        self.cookies()
        self.teardown()
        self.flow_control()

    def card(self):
        card = chapter_card(4, r"TCP", r"What does a real reliable stream need?", lit=(1974, 1996),
                            extra=((1981, r"RFC 793"), (1992, r"window scaling"), (1996, r"Bernstein: \ SYN "
                                                                                       r"cookies")), part=PART)
        with self.voiceover("Chapter four. TCP."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def header(self):
        head = label(r"Twenty bytes of header", font_size=36).to_edge(UP, buff=0.3)
        fields = [("source port", 2, LAM), ("dest. port", 2, LAM), ("sequence number", 4, SEG),
                  ("acknowledgement number", 4, ACKC), ("len, flags", 2, KERN), ("window", 2, WIN),
                  ("checksum", 2, GREY_B), ("urgent", 2, GREY_D)]
        g = VGroup()
        for name, n, c in fields:
            r = Rectangle(width=1.15 * n, height=0.9, stroke_color=c, stroke_width=1.8, fill_color=c,
                          fill_opacity=0.18)
            t = label(name, font_size=20, color=c).move_to(r)
            if t.width > r.width - 0.1:
                t.width = r.width - 0.1
            g.add(VGroup(r, t))
        row1 = VGroup(*g[:2], g[2]).arrange(RIGHT, buff=0)
        row2 = VGroup(g[3], g[4], g[5]).arrange(RIGHT, buff=0)
        row3 = VGroup(g[6], g[7]).arrange(RIGHT, buff=0)
        rows = VGroup(row1, row2, row3).arrange(DOWN, buff=0, aligned_edge=LEFT).next_to(head, DOWN, buff=0.45)
        notes = VGroup(
            wrapped_label(r"\textbf{sequence number}: \ which byte of the stream this segment starts with \ (bytes, "
                          r"not packets)", 12.2, font_size=21, color=SEG),
            wrapped_label(r"\textbf{acknowledgement}: \ the next byte I expect \ (cumulative: \ all before it "
                          r"arrived); \ SACK options add the blocks after a gap", 12.2, font_size=21, color=ACKC),
            wrapped_label(r"\textbf{flags}: \ SYN, \ ACK, \ FIN, \ RST; \ \textbf{window}: \ how many more bytes I "
                          r"can buffer", 12.2, font_size=21, color=KERN),
            wrapped_label(r"both directions at once: \ every segment carries data one way and an ACK the other",
                          12.2, font_size=21, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(rows, DOWN, buff=0.5)
        with self.voiceover(
            "TCP is those ideas, engineered. Its header is twenty bytes. <bookmark mark='a'/> The ports, as in UDP. "
            "Then a thirty-two-bit sequence number, which counts bytes, not packets: the position in the stream of "
            "this segment's first byte. <bookmark mark='b'/> The acknowledgement number is cumulative: it names the "
            "next byte the receiver expects, which says everything before it has arrived. An option, selective "
            "acknowledgement, adds the blocks received beyond a gap, which gives the sender Selective Repeat's "
            "information. <bookmark mark='c'/> Flags open, acknowledge, close and reset connections, and the window "
            "field says how much more the receiver can buffer. <bookmark mark='d'/> A connection carries data both "
            "ways at once, so every segment can carry data in one direction and an acknowledgement for the other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def handshake(self):
        h = load("handshake")
        head = label(r"The three-way handshake", font_size=36).to_edge(UP, buff=0.3)
        ev = [(0.0, 1.0, r"SYN, \ seq = $x$", True, SEG), (1.0, 2.0, r"SYN+ACK, \ seq = $y$, \ ack = $x{+}1$",
                                                           False, ACKC),
              (2.0, 3.0, r"ACK $y{+}1$ \ + \ request", True, SEG), (3.0, 4.0, r"response", False, ACKC)]
        sd = seq_diagram(ev, t_max=4.4, height=4.8, gap=5.4, names=(r"client", r"server")).move_to([-2.5, -0.5, 0])
        side = VGroup(
            wrapped_label(r"each side picks a random \textbf{initial sequence number} and the other confirms it",
                          4.4, font_size=20, color=WHITE),
            wrapped_label(r"random, \ so a stale segment from an old connection, \ or a forger, \ is unlikely to "
                          r"land in the window", 4.4, font_size=19, color=GREY_A),
            wrapped_label(rf"the first byte of the response arrives \textbf{{2 round trips}} after the SYN: \ "
                          rf"{2 * h['rtt_ms']:.0f} ms to Frankfurt, \ before any encryption \ (Part 30)", 4.4,
                          font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, -0.4, 0])
        with self.voiceover(
            "Before any data, the two ends must agree on where each stream starts. <bookmark mark='a'/> The client "
            "sends a segment with the SYN flag and its initial sequence number, x. <bookmark mark='b'/> The server "
            "replies with its own SYN, its own number y, and an acknowledgement of x plus one. "
            "<bookmark mark='c'/> The client acknowledges y plus one, and can send its request in the same segment. "
            "<bookmark mark='d'/> Each initial number is chosen at random, so that a delayed segment from an earlier "
            "connection between the same ports, or one forged by someone who cannot see the traffic, is unlikely to "
            "fall inside the window. <bookmark mark='e'/> The cost is time. The response's first byte arrives two "
            "round trips after the SYN was sent: two hundred and sixteen milliseconds to Frankfurt, before any "
            "encryption is set up. The last chapter of this part is about removing those round trips."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd[:4]))
            for mk, a in zip("abcd", sd.arrows):
                vo.wait_until(mk)
                self.play(FadeIn(a))
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def cookies(self):
        h = load("handshake")
        c = h["cookie"]
        head = label(r"SYN floods, \ and cookies", font_size=36).to_edge(UP, buff=0.3)
        flood = VGroup(
            wrapped_label(r"1996: \ attackers send SYNs from forged addresses \ and never answer the SYN+ACK", 12.2,
                          font_size=21, color=NO),
            wrapped_label(r"each half-open connection holds a slot in a table of a few hundred: \ a few packets a "
                          r"second fill it, \ and real clients are turned away", 12.2, font_size=21, color=GREY_A),
            wrapped_label(r"Bernstein's fix: \ \textbf{keep no state} until the third packet. \ Encode it in the "
                          r"server's sequence number, \ which the client must echo back:", 12.2, font_size=21,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.4)
        bits = VGroup()
        for n, w, col, txt in ((5, 1.4, KERN, rf"time $\bmod$ 32 \\ = {c['t']}"),
                               (3, 1.0, WIN, rf"MSS \\ {c['mss']}"),
                               (24, 6.4, HEAD, rf"24 bits of a keyed hash of the \\ four addresses and ports and the "
                                               rf"time \\ = {c['hash']:,}")):
            r = Rectangle(width=w, height=1.0, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.18)
            t = label(txt, font_size=17, color=col).move_to(r)
            if t.width > w - 0.1:
                t.width = w - 0.1
            nb = label(f"{n} bits", font_size=15, color=GREY_B).next_to(r, UP, buff=0.06)
            bits.add(VGroup(r, t, nb))
        bits.arrange(RIGHT, buff=0).next_to(flood, DOWN, buff=0.5)
        isn = mono(f"server's initial sequence number = 0x{c['hex']}", 22, CODE_C).next_to(bits, DOWN, buff=0.35)
        foot = wrapped_label(r"when the ACK returns with this number $+1$, \ the server recomputes the hash: \ if it "
                             r"matches, \ the client is real and the connection is created then", 12.2, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The handshake has a weakness, exploited in 1996 against internet providers in New York. A server must "
            "remember each connection that has sent a SYN but not yet the final ACK. <bookmark mark='a'/> An "
            "attacker sends SYNs from forged addresses, which never answer. The table of half-open connections, a "
            "few hundred entries, fills in seconds, and real clients are turned away. <bookmark mark='b'/> Dan "
            "Bernstein's answer was to remember nothing. The server puts the state it needs into the one number the "
            "client must send back: its own initial sequence number. <bookmark mark='c'/> Five bits of the time, "
            "three bits for the packet size the client asked for, and twenty-four bits of a keyed hash of the "
            "addresses, the ports and the time. Here is one, built the way Linux builds it. "
            "<bookmark mark='d'/> When the final ACK comes back carrying this number plus one, the server "
            "recomputes the hash. If it matches, the client really received the SYN+ACK, and the connection is "
            "created only then. A forger who cannot see the replies cannot guess twenty-four bits."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(flood[0]), FadeIn(flood[1]))
            vo.wait_until("b")
            self.play(FadeIn(flood[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b) for b in bits], lag_ratio=0.3), FadeIn(isn))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def teardown(self):
        h = load("handshake")
        tw = h["time_wait"]
        head = label(r"Closing, \ and TIME\_WAIT", font_size=36).to_edge(UP, buff=0.3)
        ev = [(0.0, 1.0, r"FIN", True, SEG), (1.0, 2.0, r"ACK", False, ACKC), (2.4, 3.4, r"FIN", False, ACKC),
              (3.4, 4.4, r"ACK", True, SEG)]
        sd = seq_diagram(ev, t_max=6.0, height=4.6, gap=4.6, names=(r"client", r"server")).move_to([-3.0, -0.5, 0])
        wait = Line(sd.arrows[3][0].get_start(), sd.arrows[3][0].get_start() + DOWN * 1.3, color=KERN, stroke_width=6)
        wl = label(r"TIME\_WAIT: \\ $2 \times$ MSL", font_size=18, color=KERN).next_to(wait, DOWN, buff=0.1)
        side = VGroup(
            wrapped_label(r"each direction is closed separately, \ with a FIN that is itself acknowledged", 5.0,
                          font_size=20, color=WHITE),
            wrapped_label(r"the side that closes first then waits twice the maximum segment lifetime: \ in case its "
                          r"last ACK was lost, \ and so that stray segments of this connection die before the same "
                          r"four numbers are reused", 5.0, font_size=20, color=KERN),
            wrapped_label(rf"Linux: \ {tw['wait']} s. \ A client with {tw['ports']:,} ephemeral ports can open at "
                          rf"most {tw['per_second']:.0f} connections a second to one server address and port", 5.0,
                          font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.4, 0])
        with self.voiceover(
            "Closing takes four segments, because each direction closes on its own. <bookmark mark='a'/> The client "
            "sends FIN: it has no more to say. The server acknowledges, may keep sending, and eventually sends its "
            "own FIN, which the client acknowledges. <bookmark mark='b'/> Then the side that closed first does "
            "something odd: it waits. For twice the maximum segment lifetime, it keeps the connection's four numbers "
            "reserved. If its final ACK was lost, the server will resend its FIN and must get an answer; and any "
            "stray segment of this connection must die before a new connection with the same addresses and ports "
            "could mistake it for its own. That is the alternating-bit failure again, prevented by time. "
            "<bookmark mark='c'/> On Linux the wait is sixty seconds, so a client opening many short connections to "
            "one server runs out of port numbers at about five hundred and fifty a second, which is why busy "
            "services reuse connections."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd[:4]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a) for a in sd.arrows], lag_ratio=0.4), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(wait), FadeIn(wl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def flow_control(self):
        h = load("handshake")
        head = label(r"Flow control: \ don't drown the receiver", font_size=36).to_edge(UP, buff=0.3)
        buf = VGroup(*[Square(0.5, stroke_color=GREY_C, stroke_width=1.5) for _ in range(12)]).arrange(RIGHT, buff=0)
        buf.move_to([0, 1.6, 0])
        for k in range(7):
            buf[k].set_fill(SEG, 0.45)
        bl = label(r"the receiver's buffer: \ 7 segments waiting for a slow program", font_size=19,
                   color=GREY_A).next_to(buf, DOWN, buff=0.15)
        free = Brace(VGroup(*buf[7:]), UP, color=WIN)
        fl = label(r"advertised window: \ room for 5 more", font_size=19, color=WIN).next_to(free, UP, buff=0.08)
        rows = [[f"{c['window']:,} bytes", f"{c['mbps']:.1f} Mb/s"] for c in h["caps"]]
        tab = grid_table([r"window", r"most it allows, \ RTT 108 ms"], rows, widths=[3.0, 3.6], row_h=0.42,
                         font_size=20, mono_cols=())
        tab.move_to([-2.7, -1.2, 0])
        tab.cells[1][1].set_color(NO)
        tab.cells[3][1].set_color(YES)
        side = VGroup(
            wrapped_label(r"throughput $\le$ window / RTT, \ whatever the link", 5.4, font_size=21, color=WHITE),
            wrapped_label(r"the header's 16-bit window field caps it at 64 KB: \ 4.9 Mb/s to Frankfurt", 5.4,
                          font_size=20, color=NO),
            wrapped_label(r"1992: \ \textbf{window scaling} multiplies it by up to $2^{14}$; \ the buffer must "
                          r"reach the bandwidth--delay product, \ 1.35 MB at 100 Mb/s", 5.4, font_size=20,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.7, -1.3, 0])
        with self.voiceover(
            "One more thing a sender must respect: the receiver. If the program reading the data is slow, its "
            "buffer fills. <bookmark mark='a'/> So every ACK carries the window: how many more bytes the receiver "
            "has room for. The sender never has more than that in flight. This is flow control, protecting the "
            "receiver. <bookmark mark='b'/> It also caps the speed: at most one window per round trip, whatever the "
            "link. The original header gave the window sixteen bits, sixty-four kilobytes, which allows under five "
            "megabits a second to Frankfurt. <bookmark mark='c'/> In 1992 an option let both ends scale the window "
            "by up to two to the fourteen. A fast transfer across an ocean needs a buffer as large as the "
            "bandwidth-delay product: one point three five megabytes at a hundred megabits a second. Protecting the "
            "network, rather than the receiver, is the much harder problem, and it is the next three chapters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(buf), FadeIn(bl))
            vo.wait_until("a")
            self.play(GrowFromCenter(free), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()


CODE_C = DATA
_ = (HEAD, LAM, YES)
