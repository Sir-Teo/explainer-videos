from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (ACKC, CCC, CCN, DATA, HEAD, LOSS, NO, PART, SEG, YES, load, window_axes)


def hbars(rows, width=7.0, h=0.5, gap=0.32, vmax=None, font=20, unit=" s"):
    """Horizontal bars: rows of (name, value, colour); value labels to the right."""
    vmax = vmax or max(v for _, v, _ in rows)
    g = VGroup()
    g.bars, g.vals, g.names = VGroup(), VGroup(), VGroup()
    for k, (nm, v, c) in enumerate(rows):
        y = -k * (h + gap)
        w = max(0.03, width * v / vmax)
        b = Rectangle(width=w, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85)
        b.move_to([w / 2, y, 0])
        n = label(nm, font_size=font, color=c).next_to([0, y, 0], LEFT, buff=0.2)
        t = label(f"{v:.1f}{unit}", font_size=font, color=c).next_to(b, RIGHT, buff=0.15)
        g.bars.add(b)
        g.names.add(n)
        g.vals.add(t)
    g.add(g.names, g.bars, g.vals)
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.fetch()
        self.windows()
        self.plan()

    def fetch(self):
        j = load("job")
        head = label(r"Thirty novels from Frankfurt", font_size=36).to_edge(UP, buff=0.3)
        fra = Dot([4.6, 1.2, 0], radius=0.12, color=HEAD)
        sfo = Dot([-4.6, 1.2, 0], radius=0.12, color=DATA)
        fl = label(r"Frankfurt", font_size=20, color=HEAD).next_to(fra, UP, buff=0.12)
        sl = label(r"San Francisco", font_size=20, color=DATA).next_to(sfo, UP, buff=0.12)
        path = DashedLine(fra.get_center(), sfo.get_center(), color=GREY_C, dash_length=0.12)
        facts = label(rf"{j['bytes'] / 1e6:.1f} MB \ = \ {j['packets']:,} packets; \ round trip {j['rtt'] * 1000:.0f} "
                      rf"ms; \ {j['mbps']:.0f} Mb/s; \ 1 packet in 1{{,}}000 lost", font_size=21,
                      color=GREY_A).next_to(path, DOWN, buff=0.35)
        pk = VGroup(*[Square(0.16, stroke_width=0, fill_color=SEG, fill_opacity=0.9) for _ in range(9)])
        for i, p in enumerate(pk):
            p.move_to(fra.get_center() + LEFT * (0.5 + i * 0.95))
        lost = pk[4]
        rows = [(CCN[c], j[c]["seconds"], CCC[c]) for c in ("reno", "cubic", "bbr")]
        rows.append((r"the physics", j["floor"], GREY_B))
        bars = hbars(rows, width=6.5, vmax=36).move_to([0.9, -1.75, 0])
        q = label(r"the same bytes, \ the same link: \ why eleven times slower?", font_size=24,
                  color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The thirty novels we have been counting all series live, this time, on a server in Frankfurt. Pebble 1, "
            "in San Francisco, fetches them: twenty-five megabytes, seventeen thousand packets, across a path with a "
            "round trip of a hundred and eight milliseconds and a hundred megabits a second to spare. "
            "<bookmark mark='a'/> The path is not perfect. One packet in a thousand is lost on the way, and IP, as we "
            "saw last time, does nothing about it. <bookmark mark='b'/> Our TCP fetches them three times, with three "
            "different rules for how fast to send. Reno, the rule of 1990, takes thirty-five seconds. CUBIC, the "
            "default on Linux, twenty-four. BBR, Google's rule of 2016, three. <bookmark mark='c'/> The physics "
            "allows two point two: the bytes at a hundred megabits a second, plus the round trips to ask. "
            "<bookmark mark='d'/> Same bytes, same link, same losses. Why is one rule eleven times slower than "
            "another? And how does anything arrive complete and in order at all, over a network that loses, reorders "
            "and duplicates packets?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(fra), FadeIn(sfo), FadeIn(fl), FadeIn(sl), Create(path))
            self.play(FadeIn(facts))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pk], lag_ratio=0.1))
            self.play(lost.animate.set_fill(NO).scale(1.4), run_time=0.6)
            self.play(FadeOut(lost, scale=0.2))
            vo.wait_until("b")
            self.play(FadeOut(pk), FadeIn(bars.names[:3]))
            for k in range(3):
                self.play(GrowFromEdge(bars.bars[k], LEFT), FadeIn(bars.vals[k]), run_time=0.9)
            vo.wait_until("c")
            self.play(FadeIn(bars.names[3]), GrowFromEdge(bars.bars[3], LEFT), FadeIn(bars.vals[3]))
            vo.wait_until("d")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def windows(self):
        j = load("job")
        head = label(r"How fast to send: \ the window, \ over time", font_size=34).to_edge(UP, buff=0.3)
        g = window_axes(36, x_length=10.5, y_length=4.4).move_to(DOWN * 0.3)
        tr = {c: g.line(j[c]["trace"], CCC[c]) for c in ("reno", "cubic", "bbr")}
        pipe = g.hline(900, GREY_B, r"the pipe: \ 900 packets")
        bdp, bl = pipe[0], pipe[1]
        leg = VGroup(*[label(CCN[c], font_size=20, color=CCC[c]) for c in ("reno", "cubic", "bbr")]).arrange(
            RIGHT, buff=0.6).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "Here is what each did. The height is each sender's window, the most packets it allows in flight, sent "
            "but not yet acknowledged, on a logarithmic scale. "
            "To keep a hundred megabits a second busy across a hundred and eight milliseconds, about nine hundred "
            "packets must be in flight at once: the pipe. <bookmark mark='a'/> Reno climbs toward it, one packet per "
            "round trip, and halves its window at every loss. With one loss in a thousand packets it never gets "
            "close. <bookmark mark='b'/> CUBIC climbs faster, along a cubic curve. <bookmark mark='c'/> BBR ignores "
            "the losses altogether. It measures the pipe, fills it, and stays there. Each of these is a theory of "
            "what a lost packet means, and this part builds all of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(bdp), FadeIn(bl), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(tr["reno"]), run_time=3)
            vo.wait_until("b")
            self.play(Create(tr["cubic"]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(tr["bbr"]), run_time=1.5)
        self.wait(0.5)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Networks II: \ Reliable Conversation", font_size=38).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"reliability from scratch: \ stop-and-wait, \ sliding windows, \ and the sequence space they need",
            r"TCP: \ the handshake, \ cumulative ACKs, \ timers that learn the round trip",
            r"October 1986: \ the Internet's congestion collapse, \ and Jacobson's cure",
            r"AIMD, \ proved fair; \ the Mathis formula; \ queues, \ bufferbloat, \ CoDel",
            r"CUBIC, \ BBR, \ and TCP as an optimization algorithm",
            r"above TCP: \ DNS, \ HTTP/2 and QUIC, \ caches and Zipf's law",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 37 of Computer Science, Built: Networks, reliable conversation. <bookmark mark='a'/> We "
            "build reliable delivery from nothing, prove how many sequence numbers it needs, and then build TCP: its "
            "handshake, its acknowledgements, and timers that learn the round trip. We reproduce the collapse of "
            "October 1986, when the Internet's throughput fell a thousandfold, and the cure, additive increase and "
            "multiplicative decrease, which we prove fair. We derive the throughput of a TCP flow from its loss rate, "
            "watch queues swell, and meet CUBIC and BBR, and the theorem that TCP is quietly solving an optimization "
            "problem. Then we climb: names, the web, and caches."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (ACKC, LOSS, YES)
