from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load


def _late(p):
    """Events in arrival order, each with the watermark at its arrival and whether it arrived behind it."""
    pts = sorted(p["points"], key=lambda e: e[1])
    return [(et, at, wm, et < wm) for (et, at), (_, wm) in zip(pts, p["watermark"])]


class Dataflow(VoiceoverScene):
    def construct(self):
        self.card()
        self.clocks()
        self.windows()
        self.watermark()
        self.tradeoff()
        self.triggers()

    def card(self):
        card = chapter_card(4, r"Event time and processing time", r"When has a window seen all its events?",
                            lit=(2013, 2015), extra=((2013, r"Akidau et al.: \ MillWheel"),
                                                     (2015, r"Akidau et al.: \ the Dataflow model")), part=PART)
        with self.voiceover("Chapter four. Event time and processing time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def _plot(self):
        g = axes([0, 70, 10], [0, 70, 10], x_length=5.4, y_length=4.7,
                 x_label=r"event time: \ when it happened \ (s)", y_label=r"processing time: \ when it arrived \ (s)",
                 xticks=[0, 20, 40, 60], yticks=[0, 20, 40, 60])
        g.move_to([-3.4, -0.4, 0])
        ax = g.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(66, 66), color=GREY_B, stroke_width=1.5)
        dl = label(r"no delay", font_size=16, color=GREY_B).next_to(ax.c2p(60, 60), RIGHT, buff=0.12).shift(DOWN * 0.2)
        return g, ax, VGroup(diag, dl)

    def clocks(self):
        p = load("plot")
        ev = _late(p)
        n = len(ev)
        rate = round((n - 1) / (max(e for e, *_ in ev) - min(e for e, *_ in ev)))
        maxd = max(at - et for et, at, *_ in ev)
        head = label(r"Two clocks", font_size=36).to_edge(UP, buff=0.3)
        g, ax, diag = self._plot()
        now = ValueTracker(0.0)
        dots = VGroup()
        for et, at, *_ in ev:
            d = Dot(ax.c2p(et, at), radius=0.045, color=DATA).set_opacity(0)
            d.add_updater(lambda m, at=at: m.set_opacity(1.0 if at <= now.get_value() else 0.0))
            dots.add(d)
        sweep = always_redraw(lambda: DashedLine(ax.c2p(0, now.get_value()), ax.c2p(70, now.get_value()),
                                                 color=HEAD, stroke_width=1.5))
        notes = VGroup(
            wrapped_label(r"\textbf{event time}: \ when the event happened, \ stamped by the phone or sensor that "
                          r"saw it", 5.8, font_size=20, color=WHITE),
            wrapped_label(r"\textbf{processing time}: \ when the pipeline sees it; \ always later, \ by a network "
                          r"delay, \ a queue, \ or a phone that was offline", 5.8, font_size=20, color=DATA),
            wrapped_label(rf"{n} simulated events, \ {rate} a second; \ most arrive within a few seconds, \ the "
                          rf"slowest {maxd:.1f} s late", 5.8, font_size=20, color=HEAD),
            wrapped_label(r"a count of one minute of event time cannot learn from the clock alone whether all of "
                          r"that minute's events have arrived", 5.8, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.75, -0.2, 0])
        with self.voiceover(
            "Every event in a stream carries two times. <bookmark mark='a'/> Its event time is when it happened, "
            "stamped by the phone that recorded the click. <bookmark mark='b'/> Its processing time is when the "
            "pipeline sees it, which is always later: a network delay, a queue, or a phone in a tunnel. "
            f"<bookmark mark='c'/> Plot each event at its event time across and its arrival upwards. Here are {n} "
            f"simulated events, {rate} a second, appearing as the processing clock runs. With no delay they would "
            f"lie on the diagonal; most land a little above it, the slowest about {maxd:.0f} seconds late. "
            "<bookmark mark='d'/> So a pipeline counting one minute's clicks cannot tell from its own clock when "
            "that minute's events have all arrived."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(diag[0]), FadeIn(diag[1]))
            self.add(dots, sweep)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            self.play(now.animate.set_value(68.0), run_time=7, rate_func=linear)
            sweep.clear_updaters()
            self.play(FadeOut(sweep), run_time=0.4)
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        for d in dots:
            d.clear_updaters()
        self.clear_scene()

    def windows(self):
        w = load("windows")
        ts = w["times"]
        size = w["tumbling"][0][1] - w["tumbling"][0][0]
        step = w["sliding"][0][0][0] - w["sliding"][0][1][0]
        s0 = w["sessions"][0]
        gap = s0[1] - max(t for t in ts if s0[0] <= t < s0[1])
        head = label(r"Windows: \ where in event time", font_size=36).to_edge(UP, buff=0.3)

        def X(t):
            return -4.9 + 0.36 * t
        ya = 2.3
        axis = Arrow([X(-5), ya, 0], [X(31), ya, 0], buff=0, color=GREY_C, stroke_width=2,
                     max_tip_length_to_length_ratio=0.02)
        ticks = VGroup(*[label(f"{t}", font_size=15, color=GREY_B).move_to([X(t), ya - 0.25, 0])
                         for t in (0, 10, 20, 30)])
        al = label(r"event time \ (s)", font_size=16, color=GREY_B).next_to(axis, UP, buff=0.08).align_to(axis, RIGHT)
        evs = VGroup(*[Dot([X(t), ya, 0], radius=0.08, color=DATA) for t in ts])
        ill = note(r"eight illustrative events", font_size=16).next_to(axis, UP, buff=0.08).align_to(axis, LEFT)

        def bar(a, b, y, col):
            k = sum(1 for t in ts if a <= t < b)
            r = Rectangle(width=(b - a) * 0.36 - 0.04, height=0.32, stroke_color=col, stroke_width=1.5,
                          fill_color=col, fill_opacity=0.25).move_to([(X(a) + X(b)) / 2, y, 0])
            return VGroup(r, label(f"{k}", font_size=16, color=WHITE).move_to(r))
        slides = sorted({tuple(x) for s in w["sliding"] for x in s})
        tumb = sorted({tuple(x) for x in w["tumbling"]})
        rows = VGroup(
            VGroup(label(rf"tumbling: \ {size} s, \ never overlapping", font_size=19, color=DATA),
                   VGroup(*[bar(a, b, 0, DATA) for a, b in tumb])),
            VGroup(label(rf"sliding: \ {size} s, \ every {step} s", font_size=19, color=LAM),
                   VGroup(*[bar(a, b, 0.2 if i % 2 else -0.2, LAM) for i, (a, b) in enumerate(slides)])),
            VGroup(label(rf"sessions: \ ended by a gap of {gap:.0f} s", font_size=19, color=YES),
                   VGroup(*[bar(a, b, 0, YES) for a, b in w["sessions"]])),
        )
        ys = (1.25, -0.05, -1.35)
        for r, y in zip(rows, ys):
            r[1].shift(UP * (y - 0.45))
            r[0].move_to([X(-5), y, 0], aligned_edge=LEFT)
        rows[1][0].shift(UP * 0.05)
        foot = wrapped_label(r"the numbers are events per window; \ all three are defined in event time, \ so the "
                             r"answer depends on what happened, \ not on when the pipeline heard of it", 12.4,
                             font_size=20, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The Dataflow model of Tyler Akidau and his colleagues at Google, in 2015, first asks where in event "
            f"time a result belongs. <bookmark mark='a'/> Tumbling windows cut time into fixed pieces, here {size} "
            f"seconds, so every event falls in exactly one. <bookmark mark='b'/> Sliding windows have a size and a "
            f"step, {size} seconds every {step}, so each event belongs to two. "
            "<bookmark mark='c'/> Session windows are found in the data: one user's run of activity, ended by a gap "
            f"of {gap:.0f} seconds, so a late event can merge two sessions into one. <bookmark mark='d'/> All three "
            "are defined in event time: the answer depends on what happened, not on when the pipeline heard."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(axis), FadeIn(ticks), FadeIn(al), FadeIn(ill),
                      LaggedStart(*[FadeIn(d, scale=0.5) for d in evs], lag_ratio=0.15))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), LaggedStart(*[GrowFromEdge(b, LEFT) for b in r[1]], lag_ratio=0.25),
                          run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def watermark(self):
        p = load("plot")
        ev = _late(p)
        lag = p["lag"]
        n = len(ev)
        late = [(et, at) for et, at, _, lt in ev if lt]
        fire = next(at for _, at, wm, _ in ev if wm >= 10)
        inn = sum(1 for et, at, *_ in ev if et < 10 and at < fire)
        tot = sum(1 for et, *_ in ev if et < 10)
        miss = [(et, at) for et, at, *_ in ev if et < 10 and at >= fire]
        head = label(r"Watermarks: \ when in processing time", font_size=36).to_edge(UP, buff=0.3)
        g, ax, diag = self._plot()
        dots = VGroup(*[Dot(ax.c2p(et, at), radius=0.045, color=DATA) for et, at, *_ in ev])
        reds = [dots[i] for i, e in enumerate(ev) if e[3]]
        stair = []
        for i, (_, at, wm, _) in enumerate(ev):
            nxt = ev[i + 1][1] if i + 1 < n else 68.0
            stair += [ax.c2p(max(wm, 0), at), ax.c2p(max(wm, 0), nxt)]
        curve = VMobject(color=HEAD, stroke_width=3).set_points_as_corners(stair)
        at34, wm34 = next((at, wm) for _, at, wm, _ in ev if at >= 34)
        wl = label(r"watermark", font_size=17, color=HEAD).move_to(ax.c2p(52, 24))
        wl = VGroup(wl, Line(wl.get_top() + UP * 0.05, ax.c2p(wm34 + 0.8, at34), color=HEAD, stroke_width=1.2))
        band = Rectangle(width=ax.c2p(10, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 68)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=LAM, fill_opacity=0.15).move_to(
            (ax.c2p(0, 0) + ax.c2p(10, 68)) / 2)
        fl = Line(ax.c2p(0, fire), ax.c2p(10, fire), color=LAM, stroke_width=3)
        ring = VGroup(*[Circle(radius=0.13, color=NO, stroke_width=3).move_to(ax.c2p(et, at)) for et, at in miss])
        notes = VGroup(
            wrapped_label(r"a \textbf{watermark} $W$ is the pipeline's claim: \ no event older than $W$ is still "
                          r"coming", 5.8, font_size=20, color=WHITE),
            wrapped_label(rf"a heuristic one: \ the largest event time seen so far, \ minus {lag:.0f} s", 5.8,
                          font_size=20, color=HEAD),
            wrapped_label(rf"{len(late)} of the {n} events arrive behind it: \ they are \textbf{{late}}", 5.8,
                          font_size=20, color=NO),
            wrapped_label(rf"the window $[0, 10)$ closes when $W$ passes 10, \ at {fire:.1f} s, \ with {inn} of its "
                          rf"{tot} events; \ the last arrives at {miss[0][1]:.1f} s", 5.8, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.75, -0.2, 0])
        with self.voiceover(
            "The second question is when, in processing time, a result can be given. <bookmark mark='a'/> A "
            "watermark is the pipeline's running claim that no older event is still on its way. With complete "
            "knowledge of the sources it can be exact; usually it is a guess. <bookmark mark='b'/> Ours is the "
            f"largest event time seen so far, minus {lag:.0f} seconds, climbing as a staircase behind the events. "
            f"<bookmark mark='c'/> {len(late)} of the {n} events arrive behind it: they are late. "
            "<bookmark mark='d'/> The window of the first ten seconds closes when the watermark passes ten, at "
            f"about {fire:.0f} seconds, with {inn} of its {tot} events. The last arrives {miss[0][1] - fire:.1f} "
            "seconds later, and the answer already given is wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(diag), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(curve), FadeIn(wl), FadeIn(notes[1]), run_time=3)
            vo.wait_until("c")
            self.play(*[d.animate.set_color(NO).scale(1.5) for d in reds], FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(band), Create(fl), FadeIn(notes[3]))
            self.play(Create(ring))
        self.wait(0.4)
        self.clear_scene()

    def tradeoff(self):
        w = load("watermark")
        rows = w["rows"]
        al = w["allowed_lateness"]
        r0 = rows[0]
        total = round(r0["dropped"] / (1 - r0["complete"]))
        dmax = max(r["dropped"] for r in rows)
        lmax = max(r["mean_latency"] for r in rows)
        head = label(r"How long to wait?", font_size=36).to_edge(UP, buff=0.3)
        xl, xd, xm, xe = -5.9, -4.7, -0.3, 5.7
        hdr = VGroup(label(r"lag", font_size=18, color=GREY_B).move_to([xl, 2.4, 0]),
                     label(rf"events dropped \ (of {total:,})", font_size=18, color=NO).move_to([xd, 2.4, 0],
                                                                                             aligned_edge=LEFT),
                     label(r"mean wait for a window's answer", font_size=18, color=KERN).move_to([xm, 2.4, 0],
                                                                                                 aligned_edge=LEFT),
                     label(r"windows exact", font_size=18, color=GREY_B).move_to([xe, 2.4, 0]))
        rule = Line([-6.8, 2.12, 0], [6.8, 2.12, 0], color=GREY_D, stroke_width=1.5)

        def row(r, y, name, col=WHITE):
            d = max(0.02, r["dropped"] / dmax * 3.0)
            m = max(0.02, r["mean_latency"] / lmax * 3.4)
            bd = Rectangle(width=d, height=0.3, stroke_width=0, fill_color=NO, fill_opacity=0.85).move_to(
                [xd + d / 2, y, 0])
            bm = Rectangle(width=m, height=0.3, stroke_width=0, fill_color=KERN, fill_opacity=0.85).move_to(
                [xm + m / 2, y, 0])
            return VGroup(label(name, font_size=18, color=col).move_to([xl, y, 0]), bd,
                          label(f"{r['dropped']:,}", font_size=17, color=NO).next_to(bd, RIGHT, buff=0.1), bm,
                          label(rf"{r['mean_latency']:.1f} s", font_size=17, color=KERN).next_to(bm, RIGHT, buff=0.1),
                          label(rf"{r['exact']} / {r['windows']}", font_size=18, color=col).move_to([xe, y, 0]))
        body = VGroup(*[row(r, 1.75 - 0.5 * i, rf"{r['lag']:.0f} s") for i, r in enumerate(rows)])
        extra = row(al, 1.75 - 0.5 * len(rows) - 0.1, r"5 s $+$ 60 s", YES)
        extra[0].scale(0.9)
        foot = wrapped_label(rf"{total:,} simulated events, \ some delayed a long way, \ counted in 10 s "
                             r"tumbling windows; \ green: \ answer at the watermark, \ then correct each window for a "
                             r"further 60 s \ (\textbf{allowed lateness})", 12.4, font_size=19,
                             color=GREY_A).next_to(extra, DOWN, buff=0.6).set_x(0)
        lag5 = next(r for r in rows if r["lag"] == 5.0)
        with self.voiceover(
            f"How long should the watermark wait? We sent {total:,} simulated events "
            "through ten-second windows. <bookmark mark='a'/> With no lag, answers come "
            f"{r0['mean_latency']:.0f} seconds after a window ends, and {r0['dropped']} events are dropped as too "
            f"late. Waiting five seconds drops {lag5['dropped']}. <bookmark mark='b'/> Waiting a minute drops just "
            f"{rows[-1]['dropped']}, and {rows[-1]['exact']} of the {rows[-1]['windows']} windows are exact, but "
            "every answer is more than a minute late. <bookmark mark='c'/> The way out: answer at five seconds, "
            "keep each window's state a minute longer, and correct it whenever a late event arrives. Every window "
            "ends exact, and first answers come as quickly as before."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), Create(rule), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in body[:4]], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in body[4:]], lag_ratio=0.4), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(extra, shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def triggers(self):
        al = load("watermark")["allowed_lateness"]
        head = label(r"Triggers and accumulation", font_size=36).to_edge(UP, buff=0.3)
        x0, x1, y = -5.6, 5.6, 1.9
        axis = Arrow([x0, y, 0], [x1, y, 0], buff=0, color=GREY_C, stroke_width=2,
                     max_tip_length_to_length_ratio=0.02)
        al_t = label(r"processing time, \ for one window", font_size=16, color=GREY_B).next_to(axis, DOWN, buff=0.1)
        al_t.align_to(axis, RIGHT)
        fires = [(-3.4, r"early: \ speculative", HEAD, 5), (0.0, r"on time: \ the watermark passes", YES, 9),
                 (3.4, r"late: \ one late event", NO, 10)]
        marks = VGroup()
        for x, t, c, v in fires:
            tick = Line([x, y - 0.18, 0], [x, y + 0.18, 0], color=c, stroke_width=4)
            tl = label(t, font_size=18, color=c).next_to(tick, UP, buff=0.12)
            vl = label(rf"count so far: \ {v}", font_size=17, color=GREY_A).next_to(tick, DOWN, buff=0.45)
            marks.add(VGroup(tick, tl, vl))
        rows = [[r"discarding: \ only what is new", r"5", r"4", r"1"],
                [r"accumulating: \ the whole window", r"5", r"9", r"10"],
                [r"accumulating and retracting", r"5", r"$-5$, \ $+9$", r"$-9$, \ $+10$"]]
        tab = grid_table([r"each firing emits", r"early", r"on time", r"late"], rows, widths=[5.2, 2.2, 2.2, 2.2],
                         row_h=0.5, font_size=19, mono_cols=())
        tab.next_to(axis, DOWN, buff=1.05).set_x(0)
        ill = note(r"illustrative counts", font_size=16).next_to(tab, RIGHT, buff=0.15).align_to(tab, UP)
        if ill.get_right()[0] > 6.9:
            ill.next_to(tab, DOWN, buff=0.1).align_to(tab, RIGHT)
        lines = VGroup(
            wrapped_label(rf"our run: \ a 5 s watermark with 60 s of allowed lateness fired {al['refinements']} late "
                          rf"refinements, \ and all {al['windows']} windows ended exact", 12.4, font_size=20,
                          color=YES),
            wrapped_label(r"\textbf{what} is computed, \ \textbf{where} in event time \ (windows), \ \textbf{when} in "
                          r"processing time \ (watermarks, \ triggers), \ \textbf{how} refinements relate \ "
                          r"(accumulation)", 12.4, font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.75).set_x(0)
        with self.voiceover(
            "The last two questions are when to emit and how successive answers relate. <bookmark mark='a'/> A "
            "trigger decides when a window's result goes out: early, as a speculative answer; on time, when the "
            "watermark passes; and late, once for each late event. <bookmark mark='b'/> Accumulation decides what "
            "each firing means. Discarding mode emits only what is new. Accumulating mode emits the whole window "
            "each time: five, then nine, then ten. With retractions, each firing also withdraws the previous answer, "
            "so a consumer summing across windows counts nothing twice. <bookmark mark='c'/> Our run with a minute "
            f"of allowed lateness fired {al['refinements']} refinements. <bookmark mark='d'/> What, where, when and "
            "how: the Dataflow model asks these four questions of every pipeline."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(axis), FadeIn(al_t))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.5), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(ill))
            for k in (1, 2, 3):
                self.play(FadeIn(VGroup(*tab.cells[k])), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM)
