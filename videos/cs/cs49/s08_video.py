from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, bar_chart, code_block, load,
                                   module_box)


def steps(ax, pts):
    """A staircase through (t, value) points: each value holds until the next time."""
    P = []
    for (t0, v), (t1, _) in zip(pts, pts[1:]):
        P += [ax.c2p(t0, v), ax.c2p(t1, v)]
    return VMobject().set_points_as_corners(P)


class Video(VoiceoverScene):
    def construct(self):
        self.card()
        self.ladder()
        self.design()
        self.control()
        self.results()

    def card(self):
        card = chapter_card(7, r"A video platform", r"Which quality should the player download next?",
                            lit=(2014, 2015), extra=((2014, r"Huang et al.: \ buffer-based"),
                                                     (2015, r"Yin et al.: \ MPC")), part=PART)
        with self.voiceover("Chapter seven. A video platform."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ladder(self):
        a = load("abr")
        lad = a["ladder"]
        head = label(r"A ladder of qualities, \ cut into segments", font_size=36).to_edge(UP, buff=0.3)
        ncol, cw, ch = 12, 0.5, 0.42
        grid = VGroup()
        cells = {}
        for q in range(len(lad)):
            for s in range(ncol):
                r = Rectangle(width=cw - 0.06, height=ch - 0.06, stroke_color=GREY_D, stroke_width=1,
                              fill_color=BG, fill_opacity=1).move_to([s * cw, q * ch, 0])
                grid.add(r)
                cells[q, s] = r
        grid.move_to([-2.6, 0.55, 0])
        names = VGroup(*[label(rf"{v:g} Mbit/s", font_size=16, color=GREY_A).next_to(cells[q, 0], LEFT, buff=0.15)
                         for q, v in enumerate(lad)])
        tl = label(r"2-second segments $\rightarrow$", font_size=16, color=GREY_B).next_to(grid, DOWN, buff=0.12)
        # the buffer-based player's choices from our simulation (every third segment of its session)
        choice = [lad.index(r) for _, _, r in a["timelines"]["buffer"][16:16 + ncol]]
        path = VMobject(color=YES, stroke_width=4).set_points_as_corners([cells[q, s].get_center()
                                                                          for s, q in enumerate(choice)])
        picked = [cells[q, s] for s, q in enumerate(choice)]
        pl = wrapped_label(r"the buffer-based player's choices in our simulation \ (every third segment)", 6.2,
                           font_size=17, color=YES).next_to(tl, DOWN, buff=0.15)
        man = code_block(["#EXTM3U", "#EXT-X-STREAM-INF:BANDWIDTH=4300000", "4300k/index.m3u8",
                          "#EXT-X-STREAM-INF:BANDWIDTH=300000", "300k/index.m3u8", "..."], size=13)
        man_t = label(r"an HLS master playlist \ (abridged)", font_size=17, color=DATA)
        manifest = VGroup(man_t, man).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.9, 1.35, 0])
        hour_top = lad[-1] * 3600 / 8 / 1000
        hour_all = sum(lad) * 3600 / 8 / 1000
        nap = VGroup(
            wrapped_label(rf"an hour watched at the top rung: \ {lad[-1]:g} Mbit/s $\times$ 3600 s $\div$ 8 $=$ "
                          rf"\textbf{{{hour_top:.1f} GB}} of transfer", 12.4, font_size=21, color=HEAD),
            wrapped_label(rf"an hour stored at every rung: \ {sum(lad):g} Mbit/s in all $=$ "
                          rf"\textbf{{{hour_all:.1f} GB}}", 12.4, font_size=21, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        ill = note(r"ladder typical, \ illustrative", font_size=16).next_to(names, UP, buff=0.15).align_to(names,
                                                                                                         LEFT)
        with self.voiceover(
            "A video platform must start quickly, never stall, and look as good as each viewer's connection allows. "
            "<bookmark mark='a'/> So every upload is encoded several times, into a ladder of qualities, here six "
            "from zero point three to four point three megabits a second, and each version is cut into segments two "
            "seconds long. <bookmark mark='b'/> A manifest lists them: Apple's HTTP Live Streaming, from 2009, and "
            "the MPEG-DASH standard of 2012 work this way. Every segment is an ordinary file fetched over HTTP, so "
            "the caches of Part 42 serve video as they serve anything else. <bookmark mark='c'/> The player chooses "
            "a rung for every segment; here are the choices our buffer-based player made. <bookmark mark='d'/> The "
            "napkin: an hour at the top rung is about one point nine gigabytes to send, and storing every rung "
            "costs about five gigabytes per hour of video."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(names), FadeIn(tl), FadeIn(ill))
            vo.wait_until("b")
            self.play(FadeIn(manifest))
            vo.wait_until("c")
            self.play(LaggedStart(*[c.animate.set_fill(YES, opacity=0.6) for c in picked], lag_ratio=0.15),
                      Create(path), FadeIn(pl), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(nap[0]))
            self.play(FadeIn(nap[1]))
        self.wait(0.4)
        self.clear_scene()

    def design(self):
        head = label(r"The design: \ encode once, \ serve from the edge", font_size=36).to_edge(UP, buff=0.3)
        y = 1.3
        up = module_box(r"upload", GREY_B, w=1.6, h=0.7).move_to([-5.9, y, 0])
        q = module_box(r"queue", KERN, w=1.5, h=0.7).move_to([-3.9, y, 0])
        enc = VGroup(*[module_box(r"encoder", KERN, w=1.7, h=0.5, font=16) for _ in range(3)]).arrange(
            DOWN, buff=0.12).move_to([-1.8, y, 0])
        origin = module_box(r"origin \ (blobs)", DATA, w=2.0, h=0.8).move_to([0.6, y, 0])
        edges = VGroup(*[module_box(r"CDN edge", YES, w=1.8, h=0.55, font=17) for _ in range(3)]).arrange(
            DOWN, buff=0.25).move_to([3.3, y, 0])
        players = VGroup(*[module_box(r"player", HEAD, w=1.3, h=0.5, font=16) for _ in range(3)]).arrange(
            DOWN, buff=0.3).move_to([5.75, y, 0])

        def arr(a, b):
            return Arrow(a, b, buff=0.06, color=GREY_C, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        arrows = VGroup(arr(up.get_right(), q.get_left()),
                        *[arr(q.get_right(), e.get_left()) for e in enc],
                        *[arr(e.get_right(), origin.get_left()) for e in enc],
                        *[arr(origin.get_right(), e.get_left()) for e in edges],
                        *[arr(e.get_right(), p.get_left()) for e, p in zip(edges, players)])
        # popularity: an illustrative Zipf curve, the head cached at the edge
        n = 24
        bars = VGroup(*[Rectangle(width=0.18, height=2.0 / (k + 1), stroke_width=0,
                                  fill_color=YES if k < 5 else GREY_C, fill_opacity=0.85) for k in range(n)])
        bars.arrange(RIGHT, buff=0.04, aligned_edge=DOWN).move_to([-3.6, -2.0, 0])
        bl = VGroup(label(r"titles by popularity \ (Zipf, \ illustrative)", font_size=17, color=GREY_A),
                    ).next_to(bars, DOWN, buff=0.12)
        hl = label(r"the head: \ at every edge", font_size=17, color=YES).next_to(bars[0], RIGHT, buff=0.15).shift(
            UP * 0.7)
        tail = label(r"the long tail: \ from the origin", font_size=17, color=GREY_B).next_to(bars[12], UP,
                                                                                            buff=0.35)
        notes = VGroup(
            wrapped_label(r"encoding is a batch job: \ segments are independent, \ so a title is encoded in parallel, "
                          r"\ through a queue \ (Part 48)", 5.6, font_size=19, color=KERN),
            wrapped_label(r"a few titles take most of the views \ (Part 37's Zipf): \ the edge holds those; \ "
                          r"Netflix's Open Connect puts its caches inside internet providers' networks", 5.6,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -2.0, 0])
        seg = Dot(radius=0.09, color=HEAD)
        with self.voiceover(
            "The design follows. <bookmark mark='a'/> An upload goes into a queue, and encoders work through it. "
            "Because segments are independent, one title is encoded by many machines at once, a batch job of the "
            "kind Part 45 rents by the minute. <bookmark mark='b'/> The finished segments sit in a blob store, the "
            "origin, and are served through the content delivery network of Part 42. <bookmark mark='c'/> "
            "Popularity follows a Zipf law, as Part 37 found for words: a few titles take most of the views, so the "
            "edges hold the head, and a request for something in the long tail travels back to the origin. Netflix "
            "goes further: its Open Connect caches sit inside internet providers' own networks, filled overnight "
            "with what is likely to be watched the next day."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(up), FadeIn(q), GrowArrow(arrows[0]), FadeIn(enc), *[GrowArrow(a) for a in arrows[1:4]],
                      FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(origin), *[GrowArrow(a) for a in arrows[4:7]], FadeIn(edges),
                      *[GrowArrow(a) for a in arrows[7:10]], FadeIn(players), *[GrowArrow(a) for a in arrows[10:]])
            seg.move_to(origin)
            self.play(FadeIn(seg))
            self.play(seg.animate.move_to(edges[0]), run_time=0.7)
            self.play(seg.animate.move_to(players[0]), run_time=0.7)
            self.play(FadeOut(seg))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(bl), run_time=1.5)
            self.play(FadeIn(hl), FadeIn(tail), FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def control(self):
        a = load("abr")
        tl = a["timelines"]
        head = label(r"Adaptive bitrate is a control loop", font_size=36).to_edge(UP, buff=0.3)
        T = 520
        top = axes([0, T, 100], [0, 8, 2], x_length=7.6, y_length=2.0, y_label=r"Mbit/s", yticks=[0, 4, 8],
                   font=15)
        bot = axes([0, T, 100], [0, 30, 10], x_length=7.6, y_length=1.7, x_label=r"seconds", y_label=r"buffer, s",
                   xticks=[0, 100, 200, 300, 400, 500], yticks=[0, 30], font=15)
        VGroup(top, bot).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(head, DOWN, buff=0.3).to_edge(LEFT,
                                                                                                         buff=0.6)
        bw = VMobject(color=GREY_C, stroke_width=1.5).set_points_as_corners(
            [top.ax.c2p(3 * i, min(v, 8)) for i, v in enumerate(a["trace"]) if 3 * i <= T])
        bwl = label(r"bandwidth", font_size=15, color=GREY_B).next_to(top.ax.c2p(T, 8), UP, buff=0.08).shift(
            LEFT * 0.6)

        def rate(p, col):
            pts = [(t, r) for t, _, r in tl[p] if t <= T]
            return steps(top.ax, pts).set_stroke(col, 3)

        def buf(p, col):
            return VMobject(color=col, stroke_width=3).set_points_as_corners(
                [bot.ax.c2p(t, b) for t, b, _ in tl[p] if t <= T])
        r_buf, b_buf = rate("buffer", YES), buf("buffer", YES)
        r_mpc, b_mpc = rate("mpc", LAM), buf("mpc", LAM)
        zones = VGroup(*[DashedLine(bot.ax.c2p(0, v), bot.ax.c2p(T, v), color=GREY_D, stroke_width=1.5)
                         for v in (5, 20)])
        zl = VGroup(label(r"reservoir", font_size=14, color=GREY_B).next_to(zones[0], RIGHT, buff=0.08),
                    label(r"cushion", font_size=14, color=GREY_B).next_to(zones[1], RIGHT, buff=0.08))
        notes = VGroup(
            wrapped_label(r"\textbf{rate-based}: \ the highest rung under the recent throughput \ (a harmonic mean of "
                          r"five); \ predictions are noisy", 3.3, font_size=18, color=DATA),
            wrapped_label(r"\textbf{buffer-based} \ (Huang et al. 2014): \ choose from the buffer alone, \ lowest "
                          r"below a reservoir, \ highest above a cushion", 3.3, font_size=18, color=YES),
            wrapped_label(r"\textbf{MPC} \ (Yin et al. 2015): \ plan five segments ahead, \ maximizing quality minus "
                          r"stalls and switches; \ act on the first, \ replan", 3.3, font_size=18, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.2)
        cap = note(r"one simulated session: \ every third segment shown", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Choosing the rung is a control problem, the same shape as Part 37's congestion control: act, observe, "
            "adjust. <bookmark mark='a'/> The grey line is the bandwidth of one simulated connection, wandering "
            "between good, fair and poor. The obvious controller is rate-based: estimate the throughput of recent "
            "downloads and pick the highest rung beneath it. But estimates are noisy, and a wrong guess drains the "
            "buffer. <bookmark mark='b'/> Te-Yuan Huang and colleagues at Netflix argued in 2014 for choosing from "
            "the buffer alone: the lowest rung while the buffer is below a reservoir, the highest once it passes a "
            "cushion, and a straight line between. Here is that player: its quality follows its buffer. "
            "<bookmark mark='c'/> Xiaoqi Yin and colleagues, in 2015, used model predictive control: predict the "
            "bandwidth, try each bitrate held over the next five segments, choosing the one that maximizes quality minus penalties for stalls and switches, "
            "take the first step, and plan again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(bot), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(bw), FadeIn(bwl), run_time=2)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(zones), FadeIn(zl), FadeIn(notes[1]))
            self.play(Create(r_buf), Create(b_buf), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), r_buf.animate.set_stroke(opacity=0.3), b_buf.animate.set_stroke(opacity=0.3))
            self.play(Create(r_mpc), Create(b_mpc), run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def results(self):
        p = load("abr")["policies"]
        head = label(r"Quality, \ stalls, \ switches", font_size=36).to_edge(UP, buff=0.3)
        order = [("rate", r"rate", DATA), ("buffer", r"buffer", YES), ("mpc", r"MPC", LAM)]
        charts = VGroup()
        for key, title, fmt_ in (("mean_bitrate", r"mean bitrate, \ Mbit/s", lambda v: f"{v:.2f}"),
                                 ("rebuffer_s", r"stalled, \ seconds", lambda v: f"{v:.1f}"),
                                 ("switches", r"quality switches", lambda v: f"{v:.0f}")):
            ch = bar_chart([p[k][key] for k, _, _ in order], [n for _, n, _ in order], [c for _, _, c in order],
                           height=3.0, bar_w=0.6, gap=0.35, fmt_=fmt_, font_size=18)
            t = label(title, font_size=19, color=WHITE).next_to(ch, UP, buff=0.3)
            charts.add(VGroup(t, ch))
        charts.arrange(RIGHT, buff=1.1, aligned_edge=DOWN).next_to(head, DOWN, buff=0.5)
        cap = note(r"five synthetic ten-minute bandwidth traces, \ 2-second segments, \ a 30-second buffer; \ "
                   r"averages", font_size=16).next_to(charts, DOWN, buff=0.25)
        notes = VGroup(
            wrapped_label(r"buffer-based never stalled; \ our MPC bought the best picture with five seconds of "
                          r"stalls: \ it trusts its forecast and keeps a smaller buffer \ (Yin et al., \ with a "
                          r"better predictor, \ found MPC ahead)", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"Dobrian et al. \ (2011): \ of the quality metrics they measured, \ the time spent "
                          r"rebuffering hurt viewers' engagement most: \ the objective's weights are a product "
                          r"decision", 12.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(cap, DOWN, buff=0.45)
        with self.voiceover(
            "We ran all three on five synthetic ten-minute traces. <bookmark mark='a'/> Mean quality: rate-based two "
            "point three three megabits a second, buffer-based two point six six, MPC two point seven nine. "
            "<bookmark mark='b'/> Stalls: the buffer-based player never stalled at all. The rate-based player "
            "stalled for about three seconds, and our MPC for about five: it bought the best picture by trusting its "
            "forecast and keeping less in reserve, so sudden drops caught it. Yin and colleagues, with a better "
            "predictor, found MPC ahead. <bookmark mark='c'/> All three switched quality between fifty and "
            "sixty-five times. <bookmark mark='d'/> Which matters most? Florin Dobrian and colleagues found in 2011 "
            "that, of the quality measures they studied, time spent rebuffering hurt viewers' engagement most. How "
            "to weigh picture against stalls is a product decision, written into the controller's objective."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(c[0]) for c in charts], *[FadeIn(c[1].names) for c in charts],
                      *[Create(c[1][0]) for c in charts], FadeIn(cap))
            for mk, c in zip("abc", charts):
                vo.wait_until(mk)
                self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in c[1].bars], lag_ratio=0.2),
                          FadeIn(c[1].vals), run_time=1.2)
                if mk == "b":
                    self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
