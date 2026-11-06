from __future__ import annotations

import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, grid_table, load)


class Packets(VoiceoverScene):
    def construct(self):
        self.card()
        self.circuits()
        self.multiplex()
        self.history()

    def card(self):
        card = chapter_card(1, r"Circuits and packets", r"Why cut a message into pieces?", lit=(1964, 1969, 1974),
                            extra=((1964, r"Baran: \ distributed networks"), (1969, r"ARPANET: \ ``LO''"),
                                   (1974, r"Cerf and Kahn: \ TCP/IP")), part=PART)
        with self.voiceover("Chapter one. Circuits and packets."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def circuits(self):
        head = label(r"A wire for every call, \ or a share of every wire", font_size=34).to_edge(UP, buff=0.3)
        rng = random.Random(3)
        users = 6
        T = 40
        bursts = [[rng.random() < 0.18 for _ in range(T)] for _ in range(users)]
        W, H = 0.13, 0.28

        def lane(row, y, color, shift):
            g = VGroup()
            for t, on in enumerate(row):
                r = Rectangle(width=W, height=H, stroke_width=0, fill_color=color if on else GREY_E,
                              fill_opacity=0.9 if on else 0.35)
                r.move_to([shift + t * W, y, 0])
                g.add(r)
            return g
        circ = VGroup(*[lane(b, 1.5 - k * 0.38, DATA, -6.2) for k, b in enumerate(bursts)])
        cl = label(r"\textbf{circuits}: \ six reserved lines, \ mostly idle", font_size=20, color=NO)
        cl.next_to(circ, UP, buff=0.15).align_to(circ, LEFT)
        merged = []
        queue = 0
        for t in range(T):
            queue += sum(b[t] for b in bursts)
            sent = min(queue, 2)
            merged.append(sent)
            queue -= sent
        pk = VGroup()
        for t, s in enumerate(merged):
            for j in range(2):
                r = Rectangle(width=W, height=H, stroke_width=0, fill_color=YES if j < s else GREY_E,
                              fill_opacity=0.9 if j < s else 0.35)
                r.move_to([0.6 + t * W, 1.5 - j * 0.38, 0])
                pk.add(r)
        pl = label(r"\textbf{packets}: \ the same traffic on two shared lines", font_size=20, color=YES)
        pl.next_to(pk, UP, buff=0.15).align_to(pk, LEFT)
        lines = VGroup(
            label(r"the telephone network \textbf{reserved} a path for each call: \ guaranteed, \ and wasted when "
                  r"silent", font_size=20, color=WHITE),
            label(r"computers talk in bursts: \ a reserved line sits idle most of the time", font_size=20,
                  color=NO),
            label(r"\textbf{packet switching}: \ cut data into packets, \ each carrying its address; \ links are "
                  r"shared, \ and a burst waits in a queue", font_size=20, color=YES),
            label(r"the price: \ no guarantee; \ packets can be delayed, \ reordered or dropped", font_size=20,
                  color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "The telephone network was built on circuits. <bookmark mark='a'/> A call reserved a path of wires and "
            "switches from end to end for as long as it lasted, which guaranteed it a fixed share of every link, "
            "whether anyone spoke or not. <bookmark mark='b'/> Computers do not talk like people. They are silent, "
            "then send a burst, then are silent again, and a reserved line sits idle most of the time. "
            "<bookmark mark='c'/> The alternative is to cut data into packets, each carrying its destination, and let "
            "every packet share every link. The six bursty users here fit on two shared lines, with a short queue "
            "when bursts coincide. <bookmark mark='d'/> The price is that nothing is guaranteed: packets can wait, "
            "arrive out of order, or be dropped when a queue overflows."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(circ), FadeIn(cl), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(pk), FadeIn(pl), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def multiplex(self):
        m = load("multiplex")
        head = label(r"Statistical multiplexing, \ computed", font_size=36).to_edge(UP, buff=0.3)
        n, p = m["users"], m["p"]
        probs = [math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(16)]
        ch = bar_chart(probs, [str(k) for k in range(16)], [YES if k <= m["cap"] else NO for k in range(16)],
                       height=2.6, bar_w=0.32, gap=0.12, fmt_=lambda v: r"\,", font_size=14)
        ch.move_to([-3.0, 0.5, 0])
        cl = label(rf"users active at once, \ of {n}, \ each active {p:.0%} of the time".replace("%", r"\%"),
                   font_size=18, color=GREY_A).next_to(ch, DOWN, buff=0.35)
        rows = [[str(r["users"]), str(r["circuit"]), str(r["packet"])] for r in m["rows"]]
        tab = grid_table([r"users", r"circuits needed", r"packet capacity \ ($P < 10^{-4}$)"], rows,
                         widths=[1.5, 2.4, 3.4], row_h=0.4, font_size=19, mono_cols=())
        tab.move_to([3.6, 0.6, 0])
        for r in range(1, len(rows) + 1):
            tab.cells[r][2].set_color(YES)
            tab.cells[r][1].set_color(NO)
        lines = VGroup(
            label(rf"a link for ten users serves {n}: \ more than ten are active with probability "
                  rf"{m['overflow']:.4f}", font_size=21, color=HEAD),
            label(r"the more users share, \ the smaller the fraction of capacity needed: \ the law of large numbers "
                  r"\ (Part 20)", font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How much does sharing save? Suppose each user is active a tenth of the time, independently, and a link "
            "can carry ten active users at once. <bookmark mark='a'/> With circuits, it serves ten users. With "
            "packets, thirty-five users can share it: the number active at once follows a binomial distribution, and "
            "more than ten are active only four times in ten thousand. <bookmark mark='b'/> The saving grows with "
            "scale. A thousand users need a thousand circuits, but a packet link sized for a hundred and thirty-seven "
            "of them overflows less than once in ten thousand. <bookmark mark='c'/> This is the law of large "
            "numbers from Part 20, and it is the economic reason the Internet is built from packets."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(cl), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def history(self):
        head = label(r"From ARPANET to the Internet", font_size=36).to_edge(UP, buff=0.3)
        events = [
            ("1964", r"Paul Baran, \ RAND: \ a mesh of message blocks that survives losing most of its nodes", DATA),
            ("1965", r"Donald Davies, \ NPL: \ names them \textit{packets}", DATA),
            ("1969", r"ARPANET's first message, \ UCLA to SRI: \ ``LO'' \ (the system crashed at the G of LOGIN)", HEAD),
            ("1974", r"Cerf and Kahn: \ a protocol to join \textit{different} networks: \ an inter-net", YES),
            ("1983", r"1 January, \ the flag day: \ ARPANET switches to TCP/IP", YES),
            ("1990s", r"the Web; \ commercial networks join; \ today some 75{,}000 networks, \ one Internet", LAM),
        ]
        rows = VGroup()
        for yr, txt, c in events:
            rows.add(VGroup(label(yr, font_size=24, color=c), label(txt, font_size=20, color=WHITE)).arrange(
                RIGHT, buff=0.4, aligned_edge=DOWN))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        for r in rows:
            r[1].shift(RIGHT * (1.3 - r[0].width))
        with self.voiceover(
            "The idea had two inventors. <bookmark mark='a'/> Paul Baran at RAND, in 1964, designed a network for "
            "the Cold War, a mesh of small message blocks that would keep working after losing most of its nodes. "
            "<bookmark mark='b'/> Donald Davies in Britain, independently, called them packets. "
            "<bookmark mark='c'/> In 1969 the ARPANET sent its first message, from UCLA to the Stanford Research "
            "Institute. It was meant to be LOGIN; the system crashed after two letters. <bookmark mark='d'/> In 1974 "
            "Vint Cerf and Bob Kahn designed a protocol to connect different networks into one, an inter-network. "
            "<bookmark mark='e'/> On the first of January 1983, ARPANET switched to it, TCP and IP. "
            "<bookmark mark='f'/> Today some seventy-five thousand independent networks run it as one Internet."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()


_ = (KERN,)
