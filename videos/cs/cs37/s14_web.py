from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (DATA, HEAD, KERN, LAM, NO, PART, SEG, YES, axes, box, grid_table, load, trace)

MC = {"http1": KERN, "http2": NO, "quic": YES}
MN = {"http1": r"HTTP/1.1, \ 6 connections", "http2": r"HTTP/2, \ one TCP connection", "quic": r"HTTP/3 over QUIC"}


class Web(VoiceoverScene):
    def construct(self):
        self.card()
        self.http()
        self.hol()
        self.measured()
        self.quic()

    def card(self):
        card = chapter_card(13, r"The web's transport", r"Why did the web move off TCP?", lit=(1991, 2022),
                            extra=((1997, r"HTTP/1.1"), (2015, r"HTTP/2"), (2017, r"Langley et al.: \ QUIC"),
                                   (2021, r"RFC 9000")), part=PART)
        with self.voiceover("Chapter thirteen. The web's transport."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def http(self):
        head = label(r"A page is many objects", font_size=36).to_edge(UP, buff=0.3)
        page = box(2.4, 0.8, r"the HTML: \ 30 packets", DATA, font_size=19).move_to([-4.6, 1.3, 0])
        objs = VGroup(*[Square(0.32, stroke_color=LAM, stroke_width=1.5, fill_color=LAM, fill_opacity=0.25)
                        for _ in range(40)]).arrange_in_grid(rows=4, cols=10, buff=0.08).move_to([1.5, 1.3, 0])
        ol = label(r"40 images, \ scripts and styles: \ 8 packets each", font_size=19, color=LAM).next_to(
            objs, DOWN, buff=0.15)
        steps = VGroup(
            wrapped_label(r"\textbf{HTTP/1.0} \ (1996): \ one TCP connection per object: \ a handshake and a slow "
                          r"start each time", 12.4, font_size=21, color=GREY_A),
            wrapped_label(r"\textbf{HTTP/1.1} \ (1997): \ keep the connection open; \ but one request at a time on "
                          r"each, \ so browsers open \textbf{six} in parallel", 12.4, font_size=21, color=KERN),
            wrapped_label(r"\textbf{HTTP/2} \ (2015): \ \textit{one} connection, \ every object a numbered "
                          r"\textbf{stream}, \ their frames interleaved; \ headers compressed", 12.4, font_size=21,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "TCP gives one ordered stream. A web page is not one thing. <bookmark mark='a'/> It is an HTML file, "
            "and then dozens of objects it refers to: images, scripts, style sheets. Ours has forty. "
            "<bookmark mark='b'/> The first web fetched each object over a new TCP connection, paying a handshake "
            "and a slow start every time. <bookmark mark='c'/> HTTP one point one kept connections open, but each "
            "could carry only one request at a time, so browsers opened six connections to each server, and six "
            "slow starts, and six congestion controllers competing with each other. <bookmark mark='d'/> HTTP/2, "
            "grown from Google's SPDY, put everything on one connection. Each object becomes a numbered stream, and "
            "the streams' frames are interleaved, so a small image need not wait behind a large one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(page), LaggedStart(*[FadeIn(o) for o in objs], lag_ratio=0.02), FadeIn(ol))
            for mk, s in zip("bcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()

    def hol(self):
        head = label(r"Head-of-line blocking, \ again", font_size=36).to_edge(UP, buff=0.3)
        cols = [DATA, LAM, KERN, YES]
        seq = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
        row = VGroup(*[Square(0.55, stroke_color=cols[s], stroke_width=1.8, fill_color=cols[s], fill_opacity=0.35)
                       for s in seq]).arrange(RIGHT, buff=0.06).move_to([0, 1.5, 0])
        lost = row[5]
        x = VGroup(Line(lost.get_corner(UL), lost.get_corner(DR), color=NO, stroke_width=5),
                   Line(lost.get_corner(UR), lost.get_corner(DL), color=NO, stroke_width=5))
        tcp = label(r"TCP: \ one byte stream; \ everything after the hole waits", font_size=21,
                    color=NO).next_to(row, DOWN, buff=0.3)
        waiting = VGroup(*[SurroundingRectangle(r, color=NO, buff=0.03, stroke_width=2) for r in row[6:]])
        lines = VGroup(
            wrapped_label(r"the four streams are independent, \ but TCP knows only bytes: \ one lost packet of "
                          r"stream 2 stalls streams 1, \ 3 and 4 until it is repaired, \ a round trip later", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"the switch's head-of-line problem of Part 36, \ inside the transport: \ multiplexing "
                          r"over one ordered channel couples everything to its slowest part", 12.4, font_size=21,
                          color=KERN),
            wrapped_label(r"six HTTP/1.1 connections have six independent orders, \ so on a lossy path one "
                          r"connection can be \textit{faster} than HTTP/2", 12.4, font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tcp, DOWN, buff=0.5)
        with self.voiceover(
            "But the streams are interleaved inside one TCP byte stream, and TCP delivers bytes in order. "
            "<bookmark mark='a'/> Lose one packet, here belonging to stream two. Everything after it in the byte "
            "stream, the packets of streams one, three and four as well, is held by the receiver until the hole is "
            "filled, a round trip later. <bookmark mark='b'/> The four objects have nothing to do with each other, "
            "but TCP does not know that. <bookmark mark='c'/> It is the head-of-line blocking of the switch in the "
            "last part, moved into the transport: multiplexing over one ordered channel ties every stream to the "
            "slowest. <bookmark mark='d'/> Six separate connections have six separate orders, so on a lossy path "
            "old HTTP one point one can beat HTTP/2."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in row], lag_ratio=0.06))
            vo.wait_until("a")
            self.play(Create(x))
            self.play(Create(waiting), FadeIn(tcp))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        w = load("web")
        head = label(r"Measured: \ the page over a lossy path", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 5, 1], [100, 360, 50], x_length=6.6, y_length=3.8, x_label=r"loss, \ \%",
                 y_label=r"mean time until an object is usable, \ ms", xticks=range(0, 6), yticks=(150, 200, 250,
                                                                                                 300, 350),
                 fx=lambda v: f"{v:g}").move_to([-3.0, -0.5, 0])
        ax = g.ax
        rows = w["rows"]
        lines = {}
        for m in ("http1", "http2", "quic"):
            lines[m] = VGroup(trace(ax, [(r["loss"] * 100, r[m]) for r in rows], MC[m], width=3),
                              *[Dot(ax.c2p(r["loss"] * 100, r[m]), radius=0.06, color=MC[m]) for r in rows])
        leg = VGroup(*[label(MN[m], font_size=19, color=MC[m]) for m in ("http1", "http2", "quic")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.7, 1.5, 0])
        last = rows[-1]
        notes = VGroup(
            wrapped_label(rf"41 objects, \ {w['packets']} packets, \ RTT {w['rtt_ms']:.0f} ms, \ 200 trials a "
                          r"point; \ handshakes and slow starts not modelled", 5.4, font_size=18, color=GREY_A),
            wrapped_label(rf"no loss: \ HTTP/2 and QUIC are identical, \ {rows[0]['quic']:.0f} ms", 5.4,
                          font_size=19, color=WHITE),
            wrapped_label(rf"5\% loss: \ HTTP/2 \ {last['http2']:.0f} ms, \ QUIC \ {last['quic']:.0f} ms: \ a loss "
                          r"delays only its own stream", 5.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.7, -1.2, 0])
        with self.voiceover(
            "We measured it: forty-one objects fetched across our hundred-and-eight-millisecond path, two hundred "
            "times at each loss rate, timing when each object becomes usable. <bookmark mark='a'/> HTTP one point "
            "one's six connections share the link six ways and send in parallel. In our model they do well, because "
            "it leaves out their six handshakes and six slow starts, which in practice cost them dearly. "
            "<bookmark mark='b'/> HTTP/2 on one "
            "connection is as good as anything when nothing is lost, but every loss stalls every stream, and its "
            "mean climbs from two hundred and nine milliseconds to three hundred and thirty-six at five percent "
            "loss. <bookmark mark='c'/> The third line keeps the streams but gives each its own order, so a loss "
            "delays only the stream it belongs to: two hundred and twenty-seven milliseconds at five percent. That "
            "is QUIC."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(lines["http1"]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(lines["http2"]), FadeIn(leg[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(lines["quic"]), FadeIn(leg[2]), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def quic(self):
        h = load("handshake")
        head = label(r"QUIC: \ a transport over UDP", font_size=36).to_edge(UP, buff=0.3)
        stack1 = VGroup(*[box(2.6, 0.55, t, c, font_size=18) for t, c in (
            (r"HTTP/2", NO), (r"TLS 1.3", KERN), (r"TCP", DATA), (r"IP", GREY_B))]).arrange(DOWN, buff=0.05)
        stack2 = VGroup(*[box(2.6, h_, t, c, font_size=18) for t, c, h_ in (
            (r"HTTP/3", YES, 0.55), (r"QUIC \ (TLS 1.3 inside)", YES, 1.15), (r"UDP", LAM, 0.55),
            (r"IP", GREY_B, 0.55))]).arrange(DOWN, buff=0.05)
        VGroup(stack1, stack2).arrange(RIGHT, buff=0.8).move_to([-3.6, 0.2, 0])
        rows = [[r["name"], f"{r['rtts']}", f"{r['first_byte_ms']:.0f} ms"] for r in h["rows"]]
        tab = grid_table([r"setup", r"round trips", r"first byte"], rows, widths=[3.4, 1.6, 1.6], row_h=0.42,
                         font_size=18, mono_cols=())
        tab.move_to([3.4, 1.5, 0])
        for k in (3, 4):
            for j in range(3):
                tab.cells[k][j].set_color(YES)
        notes = VGroup(
            wrapped_label(r"streams with independent ordering; \ loss recovery and congestion control like TCP's, \ "
                          r"with every packet numbered afresh \ (no retransmission ambiguity)", 5.8, font_size=18,
                          color=WHITE),
            wrapped_label(r"encrypted, \ even most of the header: \ middleboxes cannot ossify what they cannot read", 5.8,
                          font_size=18, color=KERN),
            wrapped_label(r"connection IDs, \ not the four numbers: \ a phone moving from Wi-Fi to 5G keeps its "
                          r"connections", 5.8, font_size=18, color=LAM),
            wrapped_label(r"in user space, \ so it can change as fast as browsers do", 5.8, font_size=18,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -1.5, 0])
        with self.voiceover(
            "Why not fix TCP? Because TCP lives in every operating system kernel, and its header is read, and "
            "rewritten, by firewalls and other boxes all over the Internet, which break anything new. TCP had "
            "ossified. So Jim Roskind and Google's team built a new transport on top of UDP, which every box "
            "passes untouched. Standardized in 2021 as QUIC, it now carries a large share of the web. "
            "<bookmark mark='a'/> It merges the transport with TLS, the encryption of Part 30. A new connection "
            "needs one round trip before the request, instead of two or three, and a client returning to a server "
            "it knows can send its request in the very first packet. <bookmark mark='b'/> Inside, it has streams "
            "with independent orders, and loss recovery and congestion control much like TCP's, but every packet, "
            "including a retransmission, gets a fresh number, so Karn's ambiguity disappears. "
            "<bookmark mark='c'/> Almost all of it is encrypted, even most of the header, so no middlebox can come "
            "to depend on it. <bookmark mark='d'/> A connection is named by an identifier, not by addresses and "
            "ports, so a phone walking out of Wi-Fi onto a cellular network keeps its connections. "
            "<bookmark mark='e'/> And it runs in ordinary programs, so it can change as fast as browsers do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(stack1), FadeIn(stack2))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            for mk, n in zip("bcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n))
        self.wait(0.4)
        self.clear_scene()


_ = (HEAD, SEG)
