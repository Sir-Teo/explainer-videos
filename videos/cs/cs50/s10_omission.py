from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, trace


def ms(v: float) -> str:
    """A latency in ms or s, as a label."""
    if v >= 1000:
        return rf"{v / 1000:.1f} s"
    if v >= 10:
        return rf"{v:.0f} ms"
    return rf"{v:.1f} ms"


def box(title, body, col, w=5.0, h=1.25):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=col, stroke_width=2.2, fill_color=BG,
                         fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = label(body, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.14).move_to(r)
    return VGroup(r, t, b)


class Omission(VoiceoverScene):
    def construct(self):
        self.card()
        self.stall()
        self.reports()
        self.ramp()
        self.openclosed()

    def card(self):
        card = chapter_card(9, r"Coordinated omission", r"Why does the load test say the tail is fine?",
                            lit=(2006,), extra=((2006, r"Schroeder, \ Wierman and Harchol-Balter: \ open versus "
                                                       r"closed"),), part=PART)
        with self.voiceover("Chapter nine. Coordinated omission: how a load test can hide the very tail it was "
                            "built to measure."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def stall(self):
        o = load("omission")
        cl, tr = o["closed loop"], o["true"]
        missing = tr["n"] - cl["n"]
        head = label(r"A load generator that waits", font_size=36).to_edge(UP, buff=0.3)
        gen = box(r"load generator", r"100 requests a second, \ one at a time", DATA)
        srv = box(r"server", rf"answers in 1 ms; \ frozen {100 * o['stalled_share']:.0f}\% of the time "
                             r"\ (4 s in 40)", KERN)
        VGroup(gen, srv).arrange(RIGHT, buff=1.6).next_to(head, DOWN, buff=0.35)
        link = Arrow(gen.get_right(), srv.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5)
        # the timeline: a schematic window around one stall
        x0, x1, n_t = -3.6, 6.5, 40
        dx = (x1 - x0) / n_t
        s_a, s_b = 12, 28                      # the stall, in tick units

        def X(k):
            return x0 + dx * (k + 0.5)
        ys = {"srv": 0.55, "int": -0.35, "cl": -1.25}
        names = VGroup(
            label(r"server", font_size=19, color=KERN).move_to([-6.6, ys["srv"], 0], aligned_edge=LEFT),
            label(r"intended sends", font_size=19, color=GREY_A).move_to([-6.6, ys["int"], 0], aligned_edge=LEFT),
            label(r"closed loop sends", font_size=19, color=DATA).move_to([-6.6, ys["cl"], 0], aligned_edge=LEFT),
        )
        srv_ok = VGroup(Line([x0, ys["srv"], 0], [X(s_a) - dx / 2, ys["srv"], 0], color=YES, stroke_width=5),
                        Line([X(s_b) - dx / 2, ys["srv"], 0], [x1, ys["srv"], 0], color=YES, stroke_width=5))
        frozen = Rectangle(width=(s_b - s_a) * dx, height=0.34, stroke_width=0, fill_color=NO, fill_opacity=0.8)
        frozen.move_to([(X(s_a) + X(s_b)) / 2 - dx / 2, ys["srv"], 0])
        frozen_l = label(r"frozen", font_size=17, color=BLACK).move_to(frozen)
        band = Rectangle(width=(s_b - s_a) * dx, height=ys["srv"] - ys["cl"] + 0.6, stroke_width=0, fill_color=NO,
                         fill_opacity=0.08).move_to([frozen.get_x(), (ys["srv"] + ys["cl"]) / 2, 0])

        def tick(k, y, col):
            return Line([X(k), y - 0.17, 0], [X(k), y + 0.17, 0], color=col, stroke_width=3)
        intended = VGroup(*[tick(k, ys["int"], GREY_A) for k in range(n_t)])
        lost = VGroup(*[intended[k] for k in range(s_a + 1, s_b)])
        before = VGroup(*[tick(k, ys["cl"], DATA) for k in range(s_a)])
        wait = Rectangle(width=X(s_b) - X(s_a), height=0.22, stroke_width=0, fill_color=HEAD, fill_opacity=0.9)
        wait.move_to([(X(s_a) + X(s_b)) / 2, ys["cl"], 0])
        wait_l = label(r"one request, \ one sample of 4 s", font_size=17, color=HEAD).next_to(wait, DOWN, buff=0.12)
        after = VGroup(*[tick(k, ys["cl"], DATA) for k in range(s_b, n_t)])
        lost_l = label(r"never sent, \ so never measured", font_size=17, color=NO).next_to(
            VGroup(*lost), UP, buff=0.12)
        sch = note(r"schematic: \ one tick per intended request", font_size=16).next_to(
            VGroup(*after), DOWN, buff=0.55).align_to(after, RIGHT)
        foot = wrapped_label(rf"{tr['n']:,} requests were due; \ the closed loop measured {cl['n']:,}: \ the "
                             rf"{missing:,} it skipped are exactly the ones that would have waited", 12.6,
                             font_size=20, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is a load test. <bookmark mark='a'/> A generator is meant to send a hundred requests a second to "
            "a server that answers in one millisecond, except that every forty seconds the server freezes for four, "
            "as in a long garbage-collection pause. <bookmark mark='b'/> The generator is a closed loop: it sends a "
            "request, waits for the answer, then sends the next. <bookmark mark='c'/> When the server freezes, one "
            "request waits four seconds, and that is one sample. <bookmark mark='d'/> But in those four seconds the "
            "generator should have sent four hundred requests. Waiting, it sent none of them, so none were "
            "measured. The generator has coordinated with the server, against the measurement. <bookmark mark='e'/> "
            "Over two hundred seconds, twenty thousand requests were due, and eighteen thousand and five were "
            "recorded. The nineteen hundred and ninety-five skipped are exactly the ones that would have waited."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(gen), FadeIn(srv), GrowArrow(link))
            self.play(FadeIn(names[0]), Create(srv_ok), FadeIn(frozen), FadeIn(frozen_l), FadeIn(band))
            vo.wait_until("b")
            self.play(FadeIn(names[1]), LaggedStart(*[Create(t) for t in intended], lag_ratio=0.03), run_time=1.5)
            self.play(FadeIn(names[2]), LaggedStart(*[Create(t) for t in before], lag_ratio=0.05), run_time=1.2)
            vo.wait_until("c")
            self.play(GrowFromEdge(wait, LEFT), FadeIn(wait_l), run_time=1.5)
            self.play(LaggedStart(*[Create(t) for t in after], lag_ratio=0.05), FadeIn(sch), run_time=1.2)
            vo.wait_until("d")
            self.play(*[t.animate.set_color(NO) for t in lost], FadeIn(lost_l))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def reports(self):
        o = load("omission")
        cl, tr = o["closed loop"], o["true"]
        head = label(r"What the two measurements report", font_size=36).to_edge(UP, buff=0.3)
        lo, hi = math.log10(0.3), math.log10(10_000)
        bx0, bw = -4.6, 9.0

        def xp(v):
            return bx0 + bw * (math.log10(v) - lo) / (hi - lo)
        stats = ((r"median", "p50"), (r"90th", "p90"), (r"99th", "p99"), (r"99.9th", "p999"), (r"maximum", "max"),
                 (r"mean", "mean"))
        rows = VGroup()
        top_y, rh = 2.15, 0.74
        for i, (nm, key) in enumerate(stats):
            y = top_y - i * rh
            name = label(nm, font_size=20, color=WHITE).move_to([-6.5, y, 0], aligned_edge=LEFT)
            bars = VGroup()
            for j, (d, col) in enumerate(((cl, DATA), (tr, NO))):
                yy = y + 0.14 - j * 0.28
                b = Rectangle(width=xp(d[key]) - bx0, height=0.22, stroke_width=0, fill_color=col,
                              fill_opacity=0.85).move_to([bx0, yy, 0], aligned_edge=LEFT)
                v = label(ms(d[key]), font_size=16, color=col).next_to(b, RIGHT, buff=0.1)
                bars.add(VGroup(b, v))
            rows.add(VGroup(name, bars))
        base_y = top_y - len(stats) * rh + 0.3
        axis = Line([bx0, base_y, 0], [bx0 + bw, base_y, 0], color=GREY_C, stroke_width=1.5)
        ticks = VGroup(*[VGroup(Line([xp(v), base_y, 0], [xp(v), base_y - 0.08, 0], color=GREY_C, stroke_width=1.5),
                                label(t, font_size=15, color=GREY_B).next_to([xp(v), base_y - 0.08, 0], DOWN,
                                                                             buff=0.06))
                         for v, t in ((1, r"1 ms"), (10, r"10 ms"), (100, r"100 ms"), (1000, r"1 s"),
                                      (10_000, r"10 s"))])
        grid = VGroup(*[DashedLine([xp(v), base_y, 0], [xp(v), top_y + 0.4, 0], color=GREY_D, stroke_width=0.8,
                                   dash_length=0.05) for v in (1, 10, 100, 1000, 10_000)])
        keys = VGroup(label(r"closed loop, \ as recorded", font_size=19, color=DATA),
                      label(r"true: \ from each request's intended send time", font_size=19, color=NO)).arrange(
            RIGHT, buff=0.6).next_to(head, DOWN, buff=0.12)
        foot = label(rf"the server was frozen {100 * o['stalled_share']:.0f}\% of the time, \ so about "
                     rf"{100 * o['stalled_share']:.0f}\% of the requests due should have waited", font_size=19,
                     color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Compare what the generator reported with the truth, measured from when each request should have been "
            "sent. <bookmark mark='a'/> The closed loop says the median is one millisecond, and so are the "
            "ninetieth, the ninety-ninth and even the ninety-nine point ninth percentiles. Only the maximum, four "
            "seconds, hints at trouble, and a maximum is easy to dismiss as a fluke. <bookmark mark='b'/> But the "
            "server was frozen a tenth of the time, so about a tenth of the requests due had to wait. The true "
            "ninetieth percentile is four hundred milliseconds; the ninety-ninth, three point six seconds. "
            "<bookmark mark='c'/> Even the mean is a hundred times larger: two hundred and twenty-three "
            "milliseconds, against two. A team reading the first column would ship a service whose users wait "
            "seconds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(keys), Create(axis), FadeIn(ticks), FadeIn(grid),
                      *[FadeIn(r[0]) for r in rows])
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r[1][0][0], LEFT) for r in rows], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(r[1][0][1]) for r in rows], lag_ratio=0.15), run_time=2)
            self.play(Indicate(rows[4][1][0], color=HEAD))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r[1][1][0], LEFT) for r in rows[:5]], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(r[1][1][1]) for r in rows[:5]], lag_ratio=0.2), FadeIn(foot), run_time=2.5)
            vo.wait_until("c")
            self.play(GrowFromEdge(rows[5][1][1][0], LEFT), FadeIn(rows[5][1][1][1]))
        self.wait(0.4)
        self.clear_scene()

    def ramp(self):
        tr = load("omission")["true"]
        stall = (tr["max"] - 1.0) / 1000          # the freeze, in seconds: the longest wait less one service time
        head = label(r"Measure from when it should have been sent", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 6, 1], [0, 4.5, 1], x_length=6.4, y_length=4.7, x_label=r"intended send time, \ seconds after "
                 r"the freeze began", y_label=r"latency, \ s", xticks=range(0, 7), yticks=range(0, 5))
        g.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        ax = g.ax
        # requests every 10 ms queue behind the freeze, then drain at 1 ms each: latency 4 s - 9 ms per request
        k_end = int(stall / 0.009)
        pts = [(0.0, stall), (k_end * 0.01, stall - 0.009 * k_end), (6.0, 0.001)]
        fill_pts = [ax.c2p(x, y) for x, y in pts[:2]] + [ax.c2p(k_end * 0.01, 0), ax.c2p(0, 0)]
        area = Polygon(*fill_pts, stroke_width=0, fill_color=NO, fill_opacity=0.25)
        line = trace(ax, pts, NO, width=3.5)
        frz = Rectangle(width=ax.c2p(stall, 0)[0] - ax.c2p(0, 0)[0], height=0.18, stroke_width=0, fill_color=KERN,
                        fill_opacity=0.8).move_to(ax.c2p(stall / 2, 0) + UP * 0.09)
        dot = Dot(ax.c2p(0, stall), radius=0.09, color=DATA)
        dot_l = label(r"the closed loop's one sample", font_size=17, color=DATA).next_to(dot, RIGHT, buff=0.25)
        sch = note(r"schematic", font_size=16).next_to(ax, UP, buff=0.05).align_to(ax, RIGHT)
        notes = VGroup(
            wrapped_label(r"each request due during the freeze waits for the rest of it, \ then for the queue to "
                          r"drain: \ a ramp of waits from 4 s down to 1 ms", 5.0, font_size=19, color=NO),
            wrapped_label(r"Gil Tene named this \textbf{coordinated omission}: \ the generator's pauses line up with "
                          r"the server's", 5.0, font_size=19, color=WHITE),
            wrapped_label(r"the cure: \ send at fixed times, \ whether or not the last reply came \ (an open loop, \ "
                          r"as wrk2 does); \ or charge each sample from its intended start \ (HdrHistogram's "
                          r"correction)", 5.0, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(g, RIGHT, buff=0.55).align_to(g, UP)
        with self.voiceover(
            "Look at one freeze through the requests' eyes. <bookmark mark='a'/> The closed loop has a single "
            "point: one request that waited four seconds. <bookmark mark='b'/> A request due a second into the "
            "freeze waits about three; one due near the end waits a moment, and then the backlog drains at a "
            "millisecond each. The true waits form a ramp from four seconds down to one millisecond, and the red "
            "area is what the test never saw. <bookmark mark='c'/> Gil Tene, of Azul Systems, named this "
            "coordinated omission. <bookmark mark='d'/> The cure is to send at fixed times, whether or not the last "
            "reply has arrived, an open loop, as his load generator wrk2 does; or else to charge every sample from "
            "its intended start time, a correction his HdrHistogram library can apply."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(frz), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(dot, scale=1.6), FadeIn(dot_l))
            vo.wait_until("b")
            self.play(Create(line), run_time=2)
            self.play(FadeIn(area), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def openclosed(self):
        rows = load("openclosed")["rows"]
        head = label(r"Open against closed load", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 1.0, 0.25], [1, 4, 1], x_length=7.0, y_length=4.2, x_label=r"utilisation",
                 y_label=r"mean response time", xticks=(0, 0.25, 0.5, 0.75, 1.0), yticks=(1, 2, 3, 4),
                 fx=lambda v: rf"{100 * v:.0f}\%", fy=lambda v: (r"10 ms", r"100 ms", r"1 s", r"10 s")[int(v) - 1])
        g.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        ax = g.ax

        def P(u, r_s):
            return ax.c2p(u, min(4.0, math.log10(r_s * 1000)))
        cpts = [P(r["util"], r["closed_R"]) for r in rows]
        opts = [P(r["util"], r["open_R"]) for r in rows if r["open_R"] < 10]
        cline = VMobject(color=DATA, stroke_width=3).set_points_as_corners(cpts)
        oline = VMobject(color=NO, stroke_width=3).set_points_as_corners(opts)
        cdots = VGroup(*[Dot(p, radius=0.05, color=DATA) for p in cpts])
        odots = VGroup(*[Dot(p, radius=0.05, color=NO) for p in opts])
        last = rows[-1]
        up = Arrow(opts[-1], ax.c2p(1.0, 4.0) + UP * 0.25, buff=0.05, color=NO, stroke_width=3)
        up_l = label(rf"{last['open_R']:,.0f} s", font_size=17, color=NO).next_to(up.get_end(), LEFT, buff=0.12)
        cl_l = label(rf"{1000 * last['closed_R']:.0f} ms", font_size=17, color=DATA).next_to(cpts[-1], RIGHT,
                                                                                          buff=0.12)
        r100 = next(r for r in rows if r["N"] == 100)
        notes = VGroup(
            wrapped_label(rf"\textbf{{closed}}: \ {rows[0]['N']} to {last['N']} users, \ each thinks for 1 s, \ sends "
                          r"one request of 10 ms, \ and waits for it", 4.6, font_size=19, color=DATA),
            wrapped_label(r"\textbf{open}: \ the same throughput arriving whatever happens \ (M/M/1, \ Part 31)",
                          4.6, font_size=19, color=NO),
            wrapped_label(rf"at {100 * r100['util']:.0f}\% busy: \ {1000 * r100['closed_R']:.0f} ms closed, \ "
                          rf"{1000 * r100['open_R']:.0f} ms open", 4.6, font_size=19, color=HEAD),
            wrapped_label(r"a closed load slows itself down when the server does; \ users on the web do not", 4.6,
                          font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.5).align_to(g, UP)
        with self.voiceover(
            "The deeper lesson is about the shape of the load. In 2006 Bianca Schroeder, Adam Wierman and Mor "
            "Harchol-Balter called their paper on it a cautionary tale. <bookmark mark='a'/> In a closed system, a "
            "fixed number of users each think for a second, send one request, and wait for it. Response time stays "
            "bounded, because when the server slows, the users wait instead of sending, as our generator did. "
            "<bookmark mark='b'/> In an open system, requests arrive whatever happens, and Part 31's queue gives "
            "the response time at the same throughput. <bookmark mark='c'/> At ninety-two percent busy, the closed "
            "system answers in eighty-two milliseconds and the open one in a hundred and thirty-two. At full load "
            "the closed mean is half a second, while the open queue grows without limit. <bookmark mark='d'/> A web "
            "service faces many independent users, which is close to open. Test it with a closed loop, and you "
            "measure a gentler world than the one it lives in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cline), FadeIn(cdots), FadeIn(cl_l), FadeIn(notes[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(oline), FadeIn(odots), FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            self.play(GrowArrow(up), FadeIn(up_l))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (HEAD, LAM, YES)
