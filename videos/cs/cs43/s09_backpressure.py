from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, module_box,
                                   trace)


def fmt_t(x):
    return f"{x:,.0f}" if x >= 100 else f"{x:.1f}"


class Backpressure(VoiceoverScene):
    def construct(self):
        self.card()
        self.hockey()
        self.bounded()
        self.storm()
        self.throttle()
        self.defences()

    def card(self):
        card = chapter_card(8, r"Backpressure", r"What should a service do with more work than it can do?",
                            lit=(2007, 2021), extra=((2007, r"Nygard: \ the circuit breaker"),
                                                     (2021, r"Bronson et al.: \ metastable failures")), part=PART)
        with self.voiceover("Chapter eight. Backpressure."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def hockey(self):
        rows = load("queue")["unbounded"]["rows"]
        head = label(r"A queue in front of a service", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 1, 0.1], [0, 120, 20], x_length=6.0, y_length=4.4, x_label=r"load $\rho$ \ (arrivals per "
                 r"service time)", y_label=r"mean time in system \ (service times)", xticks=(0, 0.2, 0.4, 0.6, 0.8, 1),
                 yticks=(0, 20, 40, 60, 80, 100, 120))
        g.move_to([-3.1, -0.15, 0])
        ax = g.ax
        xs = [i / 1000 for i in range(0, 990, 5)] + [0.9915]
        theory = trace(ax, [(x, 1 / (1 - x)) for x in xs], GREY_B, width=2.5)
        tl = label(r"$1/(1-\rho)$", font_size=20, color=GREY_B).next_to(ax.c2p(0.95, 60), LEFT, buff=0.15)
        dots = VGroup(*[Dot(ax.c2p(r["load"], r["mean"]), radius=0.07, color=HEAD) for r in rows if r["load"] < 1])
        wall = DashedLine(ax.c2p(1, 0), ax.c2p(1, 120), color=NO, stroke_width=2, dash_length=0.08)
        tab_rows = []
        for r in rows:
            tab_rows.append([f"{r['load']:g}", fmt_t(r["mean"]),
                             f"{r['theory_mean']:.0f}" if r["theory_mean"] is not None else r"---"])
        tab = grid_table([r"load", r"simulated", r"$1/(1-\rho)$"], tab_rows, widths=[1.2, 1.8, 1.8], row_h=0.42,
                         font_size=19, mono_cols=())
        tab.move_to([3.9, 1.1, 0])
        for i in range(1, len(rows) + 1):
            tab.cells[i][1].set_color(HEAD)
        for i, r in enumerate(rows, 1):
            if r["load"] > 1:
                for c in tab.cells[i]:
                    c.set_color(NO)
        over = [r for r in rows if r["load"] > 1]
        note = wrapped_label(rf"above load 1 there is no steady state: \ the queue grows for as long as we run "
                             rf"it \ (here 50{{,}}000 arrivals), \ to {fmt_t(over[0]['mean'])} and "
                             rf"{fmt_t(over[-1]['mean'])}", 5.0, font_size=18, color=NO).next_to(tab, DOWN,
                                                                                                 buff=0.3)
        with self.voiceover(
            "Put a queue in front of a service, and Part 31's arithmetic takes over. <bookmark mark='a'/> With "
            "random arrivals and random service times, an M M 1 queue, the mean time in the system is one over one "
            "minus the load, in service times: two at half load, ten at ninety percent, a hundred at ninety-nine. "
            "<bookmark mark='b'/> Simulated: two, five point three, eleven point four, twenty-three point seven, and "
            "a hundred and seven. <bookmark mark='c'/> Above a load of one there is no steady state: after fifty "
            "thousand arrivals the mean is over a thousand service times at one point oh five, and four thousand "
            "at one point two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(theory), FadeIn(tl), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            for i, d in enumerate(dots, 1):
                self.play(FadeIn(d, scale=1.5), FadeIn(VGroup(*tab.cells[i])), run_time=0.45)
            vo.wait_until("c")
            self.play(Create(wall), FadeIn(VGroup(*tab.cells[len(dots) + 1])), FadeIn(VGroup(*tab.cells[-1])),
                      FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def bounded(self):
        q = load("queue")
        ub, bd = q["unbounded"]["rows"], q["bounded"]["rows"]
        B = q["bounded"]["bound"]
        head = label(rf"Bound the queue at {B}", font_size=36).to_edge(UP, buff=0.3)
        slots = VGroup(*[Square(side_length=0.3, stroke_color=GREY_C, stroke_width=1.2) for _ in range(B)])
        slots.arrange(LEFT, buff=0.04).move_to([0.2, 2.25, 0])
        srv = module_box(r"service", KERN, w=1.6, h=0.55, font=18).next_to(slots, RIGHT, buff=0.45)
        a_in = Arrow(slots.get_left() + LEFT * 1.6, slots.get_left(), buff=0.08, color=GREY_B, stroke_width=2)
        a_out = Arrow(slots.get_right(), srv.get_left(), buff=0.08, color=GREY_B, stroke_width=2)
        fills = VGroup(*[Square(side_length=0.24, stroke_width=0, fill_color=DATA, fill_opacity=0.8).move_to(s)
                         for s in slots])
        rej = Dot(radius=0.11, color=NO).move_to(a_in.get_start())
        rej_l = label(r"full: \ refused at once", font_size=17, color=NO).next_to(a_in, DOWN, buff=0.12)
        rows = []
        for u, b in zip(ub, bd):
            rows.append([f"{u['load']:g}", fmt_t(u["mean"]), fmt_t(b["mean"]), f"{100 * b['shed']:.1f}\\%"])
        tab = grid_table([r"load", r"unbounded: \ mean", rf"bounded at {B}: \ mean", r"shed"], rows,
                         widths=[1.4, 2.8, 3.0, 1.6], row_h=0.38, font_size=19, mono_cols=())
        tab.next_to(slots, DOWN, buff=0.55).set_x(0)
        for i in range(1, len(rows) + 1):
            tab.cells[i][1].set_color(NO if ub[i - 1]["mean"] > 20 else WHITE)
            tab.cells[i][2].set_color(YES)
            tab.cells[i][3].set_color(HEAD)
        worst = math.ceil(max(b["mean"] for b in bd))
        note = wrapped_label(rf"with the bound, \ the mean stays under {worst} service times at every load; \ "
                             r"the overload becomes refusals the sender can see and act on: \ "
                             r"\textbf{backpressure}", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.35)
        lo = next(b for b in bd if b["shed"] > 0)
        with self.voiceover(
            "An unbounded queue never refuses work. It turns overload into waiting. <bookmark mark='a'/> So bound "
            "it. With room for twenty requests, an arrival that finds the queue full is turned away at once, with "
            "an error that says, try later. <bookmark mark='b'/> Now the mean time in the system stays under "
            "sixteen service times, even at a hundred and twenty percent load. The price is explicit: three "
            "requests in a thousand shed at a load of point eight, rising to seventeen percent at one point two. "
            "<bookmark mark='c'/> That is backpressure. The queue pushes back on whoever is sending, and overload "
            "becomes visible to the party that can act on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(slots), FadeIn(srv), GrowArrow(a_in), GrowArrow(a_out))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in fills], lag_ratio=0.15), run_time=2)
            self.add(rej)
            self.play(rej.animate.move_to(a_in.get_end() + LEFT * 0.2), run_time=0.5)
            self.play(rej.animate.move_to(a_in.get_start() + UP * 0.35), FadeIn(rej_l), run_time=0.5)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*tab.cells[i])) for i in range(1, len(rows) + 1)],
                                  lag_ratio=0.3), run_time=3)
            self.play(Indicate(tab.cells[bd.index(lo) + 1][3], color=HEAD), Indicate(tab.cells[-1][3], color=HEAD))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def storm(self):
        s = load("storm")
        pol = [("immediate", r"retry every second", NO), ("backoff", r"exponential backoff, \ jitter", HEAD),
               ("budget", r"backoff + retry budget", YES)]
        head = label(r"A retry storm", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 120, 20], [0, 1000, 200], x_length=7.4, y_length=4.4, x_label=r"seconds",
                 y_label=r"requests offered per second", xticks=(0, 20, 40, 60, 80, 100, 120),
                 yticks=(0, 200, 400, 600, 800, 1000), fy=lambda v: f"{v:,.0f}")
        g.move_to([-2.75, -0.2, 0])
        ax = g.ax
        down = Rectangle(width=ax.c2p(30, 0)[0] - ax.c2p(20, 0)[0], height=ax.c2p(0, 1000)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=NO, fill_opacity=0.15)
        down.move_to([(ax.c2p(20, 0)[0] + ax.c2p(30, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, 1000)[1]) / 2, 0])
        dl = label(r"down", font_size=16, color=NO).move_to(ax.c2p(23.5, 860))
        cap = DashedLine(ax.c2p(0, 100), ax.c2p(120, 100), color=GREY_A, stroke_width=1.5, dash_length=0.08)
        capl = label(r"capacity 100/s", font_size=16, color=GREY_A).next_to(ax.c2p(120, 100), RIGHT, buff=0.12)
        curves = [trace(ax, [(r["t"], r["offered"]) for r in s[k]["series"]], c, width=3) for k, _, c in pol]
        notes = VGroup(*[wrapped_label(
            rf"\textbf{{{name}}}: \ peak {s[k]['peak_offered']}/s, \ back below capacity at {s[k]['recovered_at']}\,s"
            + (rf"; \ gave up on {s[k]['gave_up']}" if s[k]["gave_up"] else ""), 4.4, font_size=19, color=c)
            for k, name, c in pol]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        setup = wrapped_label(r"demand 90 new requests per second; \ down from 20 to 30\,s; \ a failed request "
                              r"retries", 4.4, font_size=18, color=GREY_A)
        VGroup(setup, notes).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.6, 0.1, 0])
        with self.voiceover(
            "Now add retries. A service answers a hundred requests a second, and its clients send ninety. "
            "<bookmark mark='a'/> For ten seconds it is down, and clients retry each "
            "failure a second later, on top of new work. <bookmark mark='b'/> When the service returns it is offered "
            "nine hundred and ninety requests a second. With only ten a second to spare, the "
            "backlog takes ninety seconds to drain: recovery at a hundred and nineteen seconds. Real services also "
            "slow down when overloaded, and then a storm can sustain itself, what Bronson and colleagues in 2021 "
            "called a metastable failure. <bookmark mark='c'/> Exponential backoff with jitter spreads the retries "
            "out: a peak of three hundred and eighty-one, and recovery at sixty-nine seconds. <bookmark mark='d'/> "
            "A retry budget does better still."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(cap), FadeIn(capl), FadeIn(setup))
            vo.wait_until("a")
            self.play(FadeIn(down), FadeIn(dl))
            vo.wait_until("b")
            self.play(Create(curves[0]), run_time=3, rate_func=linear)
            self.play(FadeIn(notes[0]))
            for k, mk in ((1, "c"), (2, "d")):
                vo.wait_until(mk)
                self.play(Create(curves[k]), run_time=2.5, rate_func=linear)
                self.play(FadeIn(notes[k]))
        self.wait(0.4)
        self.clear_scene()

    def throttle(self):
        s = load("storm")
        head = label(r"A retry budget", font_size=36).to_edge(UP, buff=0.3)
        H, W = 3.2, 1.4
        bucket = Rectangle(width=W, height=H, stroke_color=GREY_B, stroke_width=2).move_to([-5.1, 0.4, 0])
        level = Rectangle(width=W - 0.1, height=H - 0.1, stroke_width=0, fill_color=YES, fill_opacity=0.6)
        level.move_to(bucket).align_to(bucket, DOWN).shift(UP * 0.05)
        half = DashedLine(bucket.get_left() + LEFT * 0.2, bucket.get_right() + RIGHT * 0.2, color=HEAD,
                          stroke_width=2, dash_length=0.08)
        bl = label(r"tokens", font_size=18, color=GREY_A).next_to(bucket, UP, buff=0.12)
        rules = VGroup(
            label(r"a failure costs 1 token", font_size=19, color=NO),
            label(r"a success earns 0.1", font_size=19, color=YES),
            label(r"below half: \ no retries", font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(bucket, RIGHT, buff=0.45)
        ill = label(r"the bucket: \ illustrative", font_size=16, color=GREY_B).next_to(bucket, DOWN, buff=0.15)
        pol = [("immediate", r"retry every second", NO), ("backoff", r"backoff + jitter", HEAD),
               ("budget", r"+ retry budget", YES)]
        rows = [[name, f"{s[k]['peak_offered']}", f"{s[k]['recovered_at']}", f"{s[k]['gave_up']}"]
                for k, name, _ in pol]
        tab = grid_table([r"policy", r"peak / s", r"recovered", r"gave up"], rows, widths=[3.0, 1.4, 1.6, 1.4],
                         row_h=0.5, font_size=19, mono_cols=())
        tab.move_to([3.15, 1.3, 0])
        for i, (_, _, c) in enumerate(pol, 1):
            tab.cells[i][0].set_color(c)
        b = s["budget"]
        retried = b["peak_offered"] - s["budget"]["series"][0]["offered"]
        lines = VGroup(
            wrapped_label(rf"in the first second of the outage, \ only {retried} failures are retried before the "
                          r"bucket falls below half", 6.6, font_size=19, color=WHITE),
            wrapped_label(rf"the price: \ {b['gave_up']} requests, \ all those that arrived during the outage, \ "
                          r"get an error instead of an answer", 6.6, font_size=19, color=NO),
            wrapped_label(r"gRPC's retry throttling works this way; \ the error goes back to a caller who can "
                          r"decide", 6.6, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        with self.voiceover(
            "gRPC's retry throttling gives each client a bucket of tokens. <bookmark mark='a'/> Each failure costs "
            "a token, each success earns back a tenth of one, and when the bucket is less than half full, the "
            "client stops retrying and reports the failure at once. <bookmark mark='b'/> In our outage the bucket "
            "falls below half within the first second: only forty-nine failures are retried. The peak is a hundred "
            "and thirty-nine, and the service is normal one second after it returns. "
            "<bookmark mark='c'/> The cost: nine hundred requests, every one that arrived during the "
            "outage, got an error instead of an answer. Whether that is acceptable is a product decision; the "
            "alternative was almost ninety more seconds of overload for everyone."
        ) as vo:
            self.play(FadeIn(head), Create(bucket), FadeIn(level), Create(half), FadeIn(bl), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.5), run_time=2)
            vo.wait_until("b")
            low = level.copy().stretch_to_fit_height(0.15).align_to(level, DOWN).set_fill(NO)
            self.play(Transform(level, low), Indicate(rules[0], color=NO), run_time=1.5)
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(VGroup(*tab.cells[1])),
                      FadeIn(VGroup(*tab.cells[2])))
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(lines[0]))
            vo.wait_until("c")
            full = level.copy().stretch_to_fit_height(H - 0.1).align_to(bucket, DOWN).shift(UP * 0.05).set_fill(YES)
            self.play(Transform(level, full), Indicate(rules[1], color=YES), FadeIn(lines[1]), run_time=2)
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def defences(self):
        head = label(r"Circuit breakers, \ shedding, \ deadlines", font_size=36).to_edge(UP, buff=0.3)

        def state(name, color):
            c = Circle(radius=0.62, stroke_color=color, stroke_width=2.5, fill_color=BG, fill_opacity=1)
            return VGroup(c, label(name, font_size=19, color=color).move_to(c))
        closed = state(r"closed", YES).move_to([-5.3, 1.3, 0])
        opened = state(r"open", NO).move_to([-1.3, 1.3, 0])
        halfo = state(r"half-open", HEAD).move_to([-3.3, -1.3, 0])

        def arc(a, b, text, angle, side):
            ar = CurvedArrow(a.get_center(), b.get_center(), angle=angle, color=GREY_B, stroke_width=2)
            ar.scale(0.62, about_point=ar.get_center())
            t = label(text, font_size=16, color=GREY_A).next_to(ar, side, buff=0.08)
            return VGroup(ar, t)
        e1 = arc(closed, opened, r"failures pass a threshold", -0.5, UP)
        e2 = arc(opened, halfo, r"after a cool-down", -0.6, RIGHT)
        e3 = arc(halfo, closed, r"a trial call succeeds", -0.6, LEFT)
        e4 = arc(halfo, opened, r"it fails", 0.6, LEFT)
        e4[1].shift(RIGHT * 0.1 + DOWN * 0.1)
        token = Dot(radius=0.1, color=WHITE).move_to(closed.get_top() + DOWN * 0.15)
        lines = VGroup(
            wrapped_label(r"\textbf{circuit breaker} \ (Nygard, \ \textit{Release It!}, \ 2007): \ while open, \ "
                          r"calls fail at once and the sick service gets room to recover", 5.6, font_size=19,
                          color=WHITE),
            wrapped_label(r"\textbf{load shedding}: \ refuse work at the door, \ cheapest first", 5.6,
                          font_size=19, color=YES),
            wrapped_label(r"\textbf{admission control}: \ cap the requests in flight, \ and adapt the cap as TCP "
                          r"adapts its window \ (Part 37)", 5.6, font_size=19, color=DATA),
            wrapped_label(r"\textbf{deadlines}: \ drop work whose caller has already given up \ (chapter 9)", 5.6,
                          font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.7, 0.35, 0])
        moral = wrapped_label(r"an infinite buffer turns overload into latency, \ latency into timeouts, \ and "
                              r"timeouts into retries", 12.4, font_size=22, color=HEAD).move_to([0, -2.85, 0])
        with self.voiceover(
            "These are one family of defences. <bookmark mark='a'/> A circuit "
            "breaker, described in Michael Nygard's book Release It! in 2007, watches calls to a dependency. "
            "When failures pass a threshold it opens, and calls fail at once, unsent. After a cool-down "
            "it lets a trial call through: success closes it, failure opens it again. <bookmark mark='b'/> Load "
            "shedding refuses work at the door, the cheapest first. Admission control caps the requests in "
            "flight, adapting the cap as TCP adapts its window. And deadlines, which chapter "
            "nine sends down a call chain, let a service drop work whose caller has already given up. "
            "<bookmark mark='c'/> An infinite buffer only turns overload into latency, "
            "latency into timeouts, and timeouts into retries."
        ) as vo:
            self.play(FadeIn(head), FadeIn(closed), FadeIn(opened), FadeIn(halfo), FadeIn(e1), FadeIn(e2),
                      FadeIn(e3), FadeIn(e4), FadeIn(token))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            for tgt, col in ((opened, NO), (halfo, HEAD), (opened, NO), (halfo, HEAD), (closed, YES)):
                self.play(token.animate.move_to(tgt.get_top() + DOWN * 0.15).set_color(col), Indicate(tgt[0],
                                                                                                       color=col),
                          run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            self.play(FadeIn(lines[2]))
            self.play(FadeIn(lines[3]))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, LAM)
