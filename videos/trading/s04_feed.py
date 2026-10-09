from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import (
    Mono, byte_strip, field_brace, fmt_int, stack_braces, label, load, mtex, node, note, packet, real_tag, schematic_tag, show_part,
    source, tagged,
)
from videos.trading.itch import LAYOUT, clock

FIELD_COLORS = [C.MSG, GREY_B, GREY_D, C.LATENCY, C.SIGNAL, C.BID, C.OURS, C.TRADE, C.ORDER]


class TheFeed(VoiceoverScene):
    def construct(self):
        show_part(self, 2, r"Seeing the market", r"the feed, and the order book")
        self.add_order()
        self.other_messages()
        self.packets()
        self.volume()

    # ------------------------------------------------------------------
    def add_order(self):
        p = load("messages")["picks"]["A"]
        raw = bytes.fromhex(p["hex"])
        f = p["fields"]
        assert len(raw) == 36 and f["stock"] == "NVDA" and f["side"] == "B" and f["shares"] == 100
        assert abs(f["price"] - 180.35) < 1e-9 and p["clock"] == "09:30:00.001333600"
        name, fields = LAYOUT["A"]
        colors = []
        for i, (fname, off, n, kind) in enumerate(fields):
            colors += [FIELD_COLORS[i]] * n
        strip = byte_strip(raw, colors, cell=0.33, font_size=17, gap=0.035).move_to(UP * 0.9)
        ttl = label(r"one real message from Nasdaq's feed: 36 bytes", font_size=34).to_edge(UP, buff=0.35)
        when = note(rf"sent at {p['clock']} a.m., " + r"December 10, 2025", font_size=24, color=GREY_A).next_to(ttl, DOWN, buff=0.12)
        with self.voiceover(
            "Let's look at what actually arrives from the exchange. <bookmark mark='b'/> This is one real message from "
            "Nasdaq's data feed, exactly as it went out a millisecond after the opening bell that morning: thirty-six "
            "bytes. The format is called ITCH, and Nasdaq publishes its specification."
        ) as vo:
            self.play(FadeIn(ttl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in strip], lag_ratio=0.03), FadeIn(when), run_time=2)

        # decode field by field, braces alternating below / above
        decoded = {
            "type": (r"type \texttt{A}: add order", None),
            "stock locate": (rf"stock \#{f['stock locate']}", None),
            "tracking number": (r"", None),
            "timestamp": (rf"{f['timestamp']:,} ns".replace(",", "{,}") + r"\\after midnight", None),
            "order reference": (rf"order \#{f['order reference']:,}".replace(",", "{,}"), None),
            "side": (r"\texttt{B}: buy", None),
            "shares": (r"100 shares", None),
            "stock": (r"\texttt{NVDA}", None),
            "price": (r"1{,}803{,}500\\= \$180.3500", None),
        }
        specs = []
        for i, (fname, off, n, kind) in enumerate(fields):
            txt = decoded[fname][0]
            if txt:
                specs.append((off, n, txt, FIELD_COLORS[i], UP if len(specs) % 2 else DOWN))
        braces = stack_braces(strip, specs)
        highs = [b for b, sp in zip(braces, specs) if sp[4][1] > 0]
        meaning = VGroup(
            label(r"\emph{Someone wants to buy 100 shares of Nvidia at \$180.35.}", font_size=32, color=WHITE),
            label(r"\emph{Nasdaq calls it order \#54{,}010{,}847.}", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Byte by byte: <bookmark mark='t'/> the first byte is the letter A: this is an Add Order. <bookmark "
            "mark='l'/> Two bytes give the stock's index for the day. <bookmark mark='ts'/> Six bytes are a timestamp: "
            "the number of nanoseconds since midnight, which works out to 9:30 and 1.3 milliseconds. <bookmark "
            "mark='r'/> Eight bytes are the order's reference number, <bookmark mark='s'/> one byte says buy or sell, "
            "<bookmark mark='q'/> four bytes the number of shares, <bookmark mark='n'/> eight the ticker, <bookmark "
            "mark='p'/> and four the price, in ten-thousandths of a dollar. <bookmark mark='m'/> Put together: someone "
            "wants to buy a hundred shares of Nvidia at 180 dollars and 35 cents, and from now on, that order will "
            "be known only by its number."
        ) as vo:
            for b, m in zip(braces, ["t", "l", "ts", "r", "s", "q", "n", "p"]):
                vo.wait_until(m)
                self.play(FadeIn(b, shift=(UP if b in highs else DOWN) * 0.1), run_time=0.5)
            vo.wait_until("m")
            self.play(FadeIn(meaning, shift=UP * 0.15))
        self.strip, self.braces, self.meaning, self.ttl, self.when = strip, braces, meaning, ttl, when
        self.clear_scene()

    # ------------------------------------------------------------------
    def other_messages(self):
        picks = load("messages")["picks"]
        rows = VGroup()
        for t, desc in [("D", r"\textbf{D}elete: remove order \#"), ("E", r"\textbf{E}xecuted: order \#"),
                        ("U", r"replace (\textbf{U}): order \#")]:
            p = picks[t]
            raw = bytes.fromhex(p["hex"])
            name, fields = LAYOUT[t]
            colors = []
            for i, (fname, off, n, kind) in enumerate(fields):
                colors += [[C.MSG, GREY_B, GREY_D, C.LATENCY, C.SIGNAL, C.OURS, C.TRADE, C.ORDER][min(i, 7)]] * n
            strip = byte_strip(raw, colors, cell=0.3, font_size=15, gap=0.03)
            f = p["fields"]
            if t == "D":
                txt = desc + fmt_int(f["order reference"])
            elif t == "E":
                txt = desc + fmt_int(f["order reference"]) + rf" traded {f['executed shares']} share"
            else:
                txt = desc + fmt_int(f["original reference"]) + r" $\to$ \#" + fmt_int(f["new reference"]) + \
                    rf", {f['shares']} @ \${f['price']:.2f}"
            row = VGroup(label(rf"{len(raw)} bytes", font_size=22, color=GREY_B), strip,
                         label(txt, font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(LEFT * 0.4 + DOWN * 0.1)
        missing = label(r"no price, no side, no ticker: just a reference number", font_size=28, color=C.CANCEL)
        missing.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Other messages are even shorter. <bookmark mark='d'/> A delete is nineteen bytes, and says only: remove "
            "order number such-and-such. <bookmark mark='e'/> An execution names the order that traded, and how many "
            "shares. <bookmark mark='u'/> A replace swaps an old order for a new one with a new price or size. "
            "<bookmark mark='x'/> Notice what's missing. A delete doesn't say the price, the side, or even the stock. "
            "To know what it means, you have to remember every order you have ever seen, all day. That's what the "
            "order book is for."
        ) as vo:
            for r, m in zip(rows, "deu"):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
            vo.wait_until("x")
            self.play(FadeIn(missing), Indicate(rows[0][2], color=C.CANCEL))
        self.clear_scene()

    # ------------------------------------------------------------------
    def packets(self):
        # one MoldUDP64 packet: header + length-prefixed messages
        hdr = VGroup(
            chipbox(r"session", 10, GREY_B), chipbox(r"sequence \#", 8, C.LATENCY), chipbox(r"count", 2, GREY_B),
        ).arrange(RIGHT, buff=0.05)
        msgs = VGroup(chipbox(r"len", 2, GREY_D), chipbox(r"Add (36)", 36 * 0.5, C.MSG), chipbox(r"len", 2, GREY_D),
                      chipbox(r"Delete (19)", 19 * 0.5, C.CANCEL), chipbox(r"len", 2, GREY_D),
                      chipbox(r"Exec (31)", 31 * 0.5, C.TRADE)).arrange(RIGHT, buff=0.05)
        pkt = VGroup(hdr, msgs).arrange(RIGHT, buff=0.12).to_edge(UP, buff=1.1)
        pl = label(r"one UDP packet (MoldUDP64): a numbered header, then messages", font_size=26).next_to(pkt, UP, buff=0.2)
        # two lanes A and B; lane A loses #4, lane B is late on #2
        lane_y = {"A": -0.3, "B": -1.6}
        start_x, end_x = -5.5, 1.8
        lanes = VGroup(*[Line([start_x, y, 0], [end_x, y, 0], color=GREY_D, stroke_width=2) for y in lane_y.values()])
        ll = VGroup(label(r"feed A", font_size=24, color=C.MSG).next_to(lanes[0], LEFT, buff=0.1),
                    label(r"feed B", font_size=24, color=C.MSG).next_to(lanes[1], LEFT, buff=0.1))
        arb = node(r"arbiter:\\first copy\\of each \#", color=C.LATENCY, width=2.3, height=1.5, font_size=22)
        arb.move_to([3.4, -0.95, 0])
        out = VGroup(*[packet(C.MSG, text=str(i)) for i in range(1, 7)]).arrange(RIGHT, buff=0.08).next_to(arb, DOWN, buff=0.4)
        out.shift(RIGHT * 0.3)
        out_l = label(r"in order, no gaps", font_size=22, color=GREY_A).next_to(out, DOWN, buff=0.1)
        tag = schematic_tag()
        with self.voiceover(
            "<bookmark mark='p'/> Messages travel in UDP packets, a few at a time, behind a small header whose key field "
            "is a sequence number. Multicast is unreliable: packets can be lost. <bookmark mark='l'/> So exchanges "
            "send everything twice, over two separate networks, called the A and B feeds. <bookmark mark='a'/> The "
            "feed handler's first job is arbitration: for each sequence number, take whichever copy arrives first, "
            "and drop the duplicate. <bookmark mark='g'/> If a number is missing from both, there's a gap, and the "
            "book can't be trusted until it's filled from a retransmission server."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(pl), FadeIn(pkt, shift=DOWN * 0.1), FadeIn(tag))
            vo.wait_until("l")
            self.play(Create(lanes), FadeIn(ll), FadeIn(arb))
            vo.wait_until("a")
            # packets travel; per lane a slightly different schedule
            sched = {"A": [0.0, 0.5, 1.0, None, 2.0, 2.5], "B": [0.15, 0.9, 1.1, 1.6, 2.2, 2.6]}
            dots = []
            anims = []
            for lane, times in sched.items():
                y = lane_y[lane]
                for i, t0 in enumerate(times):
                    if t0 is None:
                        continue
                    pk = packet(C.MSG, text=str(i + 1)).move_to([start_x, y, 0])
                    path = Line([start_x, y, 0], [arb.get_left()[0] - 0.3, y, 0])
                    anims.append(Succession(Wait(t0), MoveAlongPath(pk, path, run_time=1.6, rate_func=linear),
                                            FadeOut(pk, run_time=0.2)))
                    dots.append(pk)
            lost = VGroup(packet(C.PNL_DOWN, text="4"), label(r"lost", font_size=20, color=C.PNL_DOWN)).arrange(DOWN, buff=0.05)
            lost.move_to([-1.8, lane_y["A"] + 0.55, 0])
            self.play(*anims, FadeIn(lost, run_time=0.5), LaggedStart(*[FadeIn(o) for o in out], lag_ratio=0.45,
                                                                       run_time=4.0), run_time=4.4)
            self.play(FadeIn(out_l))
            vo.wait_until("g")
            gap = VGroup(packet(C.PNL_DOWN, text="?"), label(r"gap: stop, recover", font_size=22, color=C.PNL_DOWN))
            gap.arrange(RIGHT, buff=0.15).next_to(out_l, DOWN, buff=0.2)
            self.play(FadeIn(gap))
        self.clear_scene()

    # ------------------------------------------------------------------
    def volume(self):
        d = load("day")
        w = load("windows")["burst"]
        rth_mean = d["rth_s_mean"]
        bytes_ = w["same_ns"] * 33  # 31-byte executions + 2-byte length: the burst's size on the wire, roughly
        wire_us = bytes_ * 8 / 10e9 * 1e6
        assert 30_000 < rth_mean < 40_000 and 100 < wire_us < 120
        lines = VGroup(
            VGroup(label(r"average, 9:30 to 4:00", font_size=28, color=GREY_A),
                   label(rf"{fmt_int(rth_mean)} messages per second", font_size=34, color=C.MSG)),
            VGroup(label(r"busiest second (just after the close)", font_size=28, color=GREY_A),
                   label(rf"{fmt_int(d['peaks'][6]['max'])} messages", font_size=34, color=C.MSG)),
            VGroup(label(r"the Netflix burst: one event", font_size=28, color=GREY_A),
                   label(rf"{fmt_int(w['same_ns'])} messages $\approx$ {bytes_ / 1e3:.0f} kB: {wire_us:.0f} $\mu$s just to "
                         r"cross a 10 Gb/s wire", font_size=34, color=C.MSG)),
        )
        for row in lines:
            row.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.3)
        assert d["peaks"][6]["at_ns"] == 57_602_000_000_000
        punch = label(r"fall behind, and you are trading on a picture of the past", font_size=32, color=C.LATENCY)
        punch.to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "And the volume is relentless. <bookmark mark='a'/> On an ordinary stretch of that day, about 34 thousand "
            "messages a second. <bookmark mark='b'/> In the busiest second, just after the closing bell, 1.75 million. "
            "<bookmark mark='c'/> And bursts arrive all at once: that single Netflix event was about 136 kilobytes, "
            "which takes over a hundred microseconds just to cross a ten gigabit wire. <bookmark mark='p'/> A feed "
            "handler has to swallow all of it, in order, without falling behind, because the moment it falls behind, "
            "every decision it makes is based on a picture of the past."
        ) as vo:
            self.play(FadeIn(real_tag()))
            for r, m in zip(lines, "abc"):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
            vo.wait_until("p")
            self.play(FadeIn(punch))
        self.clear_scene()


def chipbox(text: str, n_bytes: float, color, unit=0.11, h=0.55) -> VGroup:
    r = Rectangle(width=max(n_bytes * unit, 0.35), height=h, stroke_color=color, stroke_width=1.5, fill_color=color,
                  fill_opacity=0.25)
    t = label(text, font_size=18)
    if t.width > r.width - 0.05:
        t.scale_to_fit_width(r.width - 0.08)
    t.move_to(r)
    return VGroup(r, t)
