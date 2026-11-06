from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load,
                                   module_box, mono)


class Micro(VoiceoverScene):
    def construct(self):
        self.card()
        self.split()
        self.cuts()
        self.fanout()
        self.deadline()

    def card(self):
        card = chapter_card(9, r"Monoliths and microservices", r"When is one program better as many?",
                            lit=(2003, 2014), extra=((2003, r"Evans: \ \textit{Domain-Driven Design}"),
                                                     (2014, r"Lewis and Fowler: \ ``Microservices''")), part=PART)
        with self.voiceover("Chapter nine. Monoliths and microservices."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def split(self):
        head = label(r"One program, \ or many", font_size=36).to_edge(UP, buff=0.3)
        specs = ((r"catalogue", DATA), (r"orders", HEAD), (r"payments", YES), (r"accounts", LAM))
        mods = VGroup(*[module_box(n, c, w=1.9, h=0.6, font=19) for n, c in specs])
        for m in mods:                                  # an opaque backing, so that lines pass behind the boxes
            m.add_to_back(m[0].copy().set_fill(BG, 1).set_stroke(width=0))
        mods.arrange_in_grid(2, 2, buff=(0.45, 0.6)).move_to([-3.9, 1.0, 0])
        mono_box = RoundedRectangle(width=mods.width + 0.7, height=mods.height + 0.9, corner_radius=0.15,
                                    stroke_color=GREY_B, stroke_width=2).move_to(mods).shift(DOWN * 0.15)
        ml = label(r"a monolith: \ one process, \ one database, \ one deploy", font_size=18,
                   color=GREY_A).next_to(mono_box, DOWN, buff=0.15)
        calls = VGroup(*[Line(mods[a].get_center(), mods[b].get_center(), color=GREY_C, stroke_width=1.5)
                         for a, b in ((0, 1), (1, 2), (1, 3), (2, 3))])
        for c in calls:
            c.set_z_index(-1)
        cl = label(r"a call: \ nanoseconds", font_size=16, color=GREY_B).next_to(mono_box, UP, buff=0.1)
        svc = mods.copy()
        targets = [[1.4, 2.0, 0], [5.4, 2.0, 0], [1.4, 0.0, 0], [5.4, 0.0, 0]]
        net = VGroup(*[DashedLine(targets[a], targets[b], color=GREY_B, stroke_width=1.8, dash_length=0.1)
                       for a, b in ((0, 1), (1, 2), (1, 3), (2, 3))])
        for n in net:
            n.set_z_index(-1)
        nl = label(r"a call: \ a message, \ milliseconds, \ and it can fail", font_size=16,
                   color=NO).move_to([3.4, -0.75, 0])
        gains = wrapped_label(r"\textbf{gains}: \ each team deploys and scales its own service \ (Conway's law, \ "
                              r"Part 40); \ a crash stays inside one service", 5.9, font_size=19, color=YES)
        costs = wrapped_label(r"\textbf{costs}: \ every call can fail, \ be slow or be repeated \ (chapter 1); \ "
                              r"data shared between services \ (chapter 10); \ one request, \ many logs", 5.9,
                              font_size=19, color=NO)
        VGroup(gains, costs).arrange(RIGHT, buff=0.6, aligned_edge=UP).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now the architectural question. <bookmark mark='a'/> A monolith is one program, deployed as a unit. "
            "Its modules call each other in nanoseconds, share one database, and fail together. "
            "<bookmark mark='b'/> Microservices split the "
            "modules into separate programs, each with its own data, talking over the network. "
            "<bookmark mark='c'/> The gain is mostly organisational. Each team deploys its own service when it "
            "is ready, and scales it on its own; Conway's law, from Part 40, says the system will mirror the teams "
            "anyway. <bookmark mark='d'/> What is lost is that every call can now fail, be slow, or be repeated, "
            "chapter one's lesson, and every piece of data two services share becomes a problem for chapter ten."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(mono_box), FadeIn(mods), Create(calls), FadeIn(ml), FadeIn(cl))
            vo.wait_until("b")
            self.add(svc)
            self.play(*[m.animate.move_to(t) for m, t in zip(svc, targets)], run_time=1.5)
            self.play(Create(net), FadeIn(nl))
            vo.wait_until("c")
            self.play(FadeIn(gains))
            vo.wait_until("d")
            self.play(FadeIn(costs))
        self.wait(0.4)
        self.clear_scene()

    def cuts(self):
        head = label(r"Where to cut", font_size=36).to_edge(UP, buff=0.3)
        ctx = [(r"sales", DATA, ["name", "segment", "open leads"]),
               (r"billing", YES, ["card on file", "invoices", "tax id"]),
               (r"shipping", KERN, ["address", "delivery slot"])]
        boxes = VGroup()
        for name, col, fields in ctx:
            body = VGroup(mono("Customer", size=16, color=WHITE),
                          *[mono("  " + f, size=14, color=GREY_A) for f in fields]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06)
            frame = RoundedRectangle(width=1.9, height=1.75, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                     fill_color=BG, fill_opacity=1)
            body.move_to(frame).shift(DOWN * 0.1)
            t = label(name, font_size=18, color=col).next_to(frame, UP, buff=0.08)
            boxes.add(VGroup(frame, body, t))
        boxes.arrange(RIGHT, buff=0.12).move_to([-3.75, 1.1, 0])
        ctx_note = wrapped_label(r"\textbf{bounded contexts} \ (Evans, \ 2003): \ each part of the business owns "
                                 r"its own model of a word like ``customer''; \ cut services along them", 5.9,
                                 font_size=19, color=WHITE).next_to(boxes, DOWN, buff=0.35)
        # deploy timelines: independent, then lock-step
        x0, x1 = 1.4, 6.6
        svcs = [r"orders", r"payments", r"stock"]

        def panel(title, times, y_top, color):
            g = VGroup(label(title, font_size=18, color=color).move_to([(x0 + x1) / 2, y_top, 0]))
            for i, (n, ts) in enumerate(zip(svcs, times)):
                y = y_top - 0.5 - i * 0.42
                g.add(label(n, font_size=16, color=GREY_A).move_to([x0 - 0.15, y, 0], aligned_edge=RIGHT))
                g.add(Line([x0, y, 0], [x1, y, 0], color=GREY_D, stroke_width=1.2))
                g.add(*[Line([x0 + (x1 - x0) * t, y - 0.13, 0], [x0 + (x1 - x0) * t, y + 0.13, 0], color=color,
                             stroke_width=4) for t in ts])
            return g
        indep = panel(r"independent deploys", [(0.1, 0.45, 0.8), (0.25, 0.6), (0.05, 0.35, 0.7, 0.92)], 2.4, YES)
        lock = panel(r"a distributed monolith", [(0.3, 0.75), (0.3, 0.75), (0.3, 0.75)], 0.3, NO)
        ties = VGroup(*[Line([x0 + (x1 - x0) * t, -0.07, 0], [x0 + (x1 - x0) * t, -1.17, 0], color=NO,
                             stroke_width=2) for t in (0.3, 0.75)])
        ill = label(r"illustrative", font_size=16, color=GREY_B).next_to(lock, DOWN, buff=0.15).align_to(lock, RIGHT)
        dm_note = wrapped_label(r"services that must deploy together, \ because they share a database, \ a library "
                                r"version or a chain of synchronous calls: \ the network's failures without the "
                                r"independence", 12.4, font_size=20, color=NO).move_to([0, -2.4, 0])
        with self.voiceover(
            "So where should the cuts go? <bookmark mark='a'/> Eric Evans' book Domain-Driven Design, in 2003, gave "
            "the answer most teams use: bounded contexts. A word like customer means different things to sales, to "
            "billing and to shipping, and each context should own its own model rather than share one giant one. "
            "<bookmark mark='b'/> Cut well, "
            "and each team deploys when it likes. <bookmark mark='c'/> Cut badly, and you get the worst of both: a "
            "distributed monolith, services that can only be deployed together because they share a database, or a "
            "library version, or a chain of synchronous calls. It has all the network's failures and none of the "
            "independence."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.4), FadeIn(ctx_note), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(indep))
            vo.wait_until("c")
            self.play(FadeIn(lock), FadeIn(ill))
            self.play(Create(ties), FadeIn(dm_note))
        self.wait(0.4)
        self.clear_scene()

    def fanout(self):
        f = load("fanout")
        rows = f["rows"]
        an = {r["fanout"]: r["p_any_tail"] for r in f["analytic_slow"]}
        head = label(r"Fan-out and the tail", font_size=36).to_edge(UP, buff=0.3)
        front = module_box(r"request", HEAD, w=1.5, h=0.55, font=17).move_to([-5.9, 0.7, 0])
        k = 20
        backs = VGroup(*[Dot(radius=0.06, color=DATA) for _ in range(k)]).arrange(DOWN, buff=0.06)
        backs.move_to([-3.0, 0.7, 0])
        lines = VGroup(*[Line(front.get_right(), d.get_center(), color=GREY_D, stroke_width=1) for d in backs])
        bl = label(rf"{k} back ends, \ in parallel", font_size=17, color=GREY_A).next_to(backs, DOWN, buff=0.15)
        slow = backs[13]
        sl = label(r"one slow", font_size=17, color=NO).next_to(slow, RIGHT, buff=0.15)
        wait = label(r"waits for all", font_size=17, color=GREY_A).next_to(front, DOWN, buff=0.15)
        trows = [[f"{r['fanout']}", f"{r['p50']:.0f}", f"{r['p99']:.0f}", f"{100 * r['share_slow']:.1f}\\%",
                  f"{100 * an[r['fanout']]:.1f}\\%"] for r in rows]
        tab = grid_table([r"$k$", r"median", r"99th pct", r"$>$ 100\,ms", r"$1 - 0.99^k$"], trows,
                         widths=[0.9, 1.4, 1.5, 1.6, 1.7], row_h=0.5, font_size=19, mono_cols=())
        tab.move_to([2.7, 0.9, 0])
        units = label(r"latency in ms; \ 20{,}000 simulated requests each", font_size=16,
                      color=GREY_B).next_to(tab, UP, buff=0.12)
        for i in range(1, len(rows) + 1):
            tab.cells[i][3].set_color(NO)
            tab.cells[i][4].set_color(HEAD)
        sgl = f["single"]
        note = wrapped_label(rf"one back end alone: \ median {sgl['p50']:.0f}\,ms, \ 99th percentile "
                             rf"{sgl['p99']:.0f}\,ms; \ one call in a hundred has a bad moment \ (a pause, \ a "
                             r"retransmit); \ with $k$ back ends the request waits for the slowest: \ Part 39's "
                             r"tail at scale", 12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Microservices also turn one request into many. <bookmark mark='a'/> Suppose a request fans out to k "
            "back ends in parallel and waits for all of them. Each back end is usually fast, ten milliseconds at "
            "the median, but one call in a hundred hits a bad moment, a pause or a retransmission. "
            "<bookmark mark='b'/> With one back end, under two percent of requests take more than a hundred "
            "milliseconds. With a hundred back ends, forty-six percent do, and the median itself has quadrupled. "
            "<bookmark mark='c'/> The chance that at least one of k back ends has a bad moment is one minus point "
            "nine nine to the k: sixty-three percent at a hundred. At many back ends the measured share is lower, "
            "because not every bad moment crosses a hundred milliseconds. It is Part 39's tail at "
            "scale: the slowest of many decides."
        ) as vo:
            self.play(FadeIn(head), FadeIn(front), FadeIn(wait))
            vo.wait_until("a")
            self.play(Create(lines), FadeIn(backs), FadeIn(bl), FadeIn(note), run_time=1.5)
            self.play(slow.animate.set_color(NO).scale(1.6), lines[13].animate.set_color(NO), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(units), FadeIn(VGroup(*[c for j, c in enumerate(tab.cells[0]) if j < 4])),
                      Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[i][:4])) for i in range(1, len(rows) + 1)],
                                  lag_ratio=0.4), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(tab.cells[0][4]),
                      LaggedStart(*[FadeIn(tab.cells[i][4]) for i in range(1, len(rows) + 1)], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def deadline(self):
        b = load("budget")
        rows, slo = b["rows"], b["slo"]
        head = label(r"A deadline travels with the request", font_size=36).to_edge(UP, buff=0.3)
        cols = [DATA, LAM, HEAD, KERN, YES]
        chain = VGroup(*[module_box(r["service"], c, w=1.95, h=0.55, font=18) for r, c in zip(rows, cols)])
        chain.arrange(RIGHT, buff=0.55).move_to([0, 2.35, 0])
        arrows = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.3) for i in range(len(rows) - 1)])
        x0, x1 = -4.2, 6.2

        def X(ms):
            return x0 + (x1 - x0) * ms / slo
        y0, dy = 1.25, 0.58
        names, lefts, works = VGroup(), VGroup(), VGroup()
        t = 0
        for i, (r, c) in enumerate(zip(rows, cols)):
            y = y0 - i * dy
            names.add(label(r["service"], font_size=17, color=c).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT))
            rem = Rectangle(width=X(slo) - X(t), height=0.4, stroke_color=GREY_C, stroke_width=1, fill_color=GREY_E,
                            fill_opacity=0.5).move_to([(X(t) + X(slo)) / 2, y, 0])
            rl = label(rf"{r['deadline_ms']}\,ms left", font_size=16, color=GREY_A).move_to(rem).align_to(
                rem, RIGHT).shift(LEFT * 0.12)
            lefts.add(VGroup(rem, rl))
            w = Rectangle(width=X(t + r["own_ms"]) - X(t), height=0.4, stroke_width=0, fill_color=c,
                          fill_opacity=0.85).move_to([(X(t) + X(t + r["own_ms"])) / 2, y, 0])
            wl = label(rf"{r['own_ms']}", font_size=16, color=WHITE).next_to(w, RIGHT, buff=0.06)
            if r["own_ms"] >= 20:
                wl.move_to(w).set_color(BLACK)
            works.add(VGroup(w, wl))
            t += r["own_ms"]
        ybase = y0 - len(rows) * dy - 0.45
        axis = Line([X(0), ybase, 0], [X(slo), ybase, 0], color=GREY_C, stroke_width=1.5)
        ticks = VGroup(*[VGroup(Line([X(m), ybase - 0.06, 0], [X(m), ybase + 0.06, 0], color=GREY_C),
                                label(f"{m}", font_size=16, color=GREY_B).next_to([X(m), ybase, 0], DOWN, buff=0.1))
                         for m in range(0, slo + 1, 25)])
        unit = label(r"ms", font_size=16, color=GREY_B).next_to(ticks[-1], RIGHT, buff=0.15)
        dl = DashedLine([X(slo), y0 + 0.35, 0], [X(slo), ybase, 0], color=NO, stroke_width=2, dash_length=0.08)
        slack = Rectangle(width=X(slo) - X(t), height=0.4, stroke_width=0, fill_color=YES, fill_opacity=0.35)
        slack.move_to([(X(t) + X(slo)) / 2, y0 - len(rows) * dy, 0])
        sl = label(rf"{b['slack']}\,ms slack", font_size=17, color=YES).next_to(slack, LEFT, buff=0.12)
        note = wrapped_label(rf"the absolute deadline \ ({slo}\,ms) \ is fixed; \ each hop receives what its caller "
                             r"has left; \ gRPC carries the remaining time in every call, \ and a service whose "
                             r"deadline has passed can stop at once", 12.4, font_size=19, color=WHITE).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "If a request must be answered within a deadline, the deadline should travel with it. "
            "<bookmark mark='a'/> This request has a hundred and fifty milliseconds. The gateway spends five of "
            "them and passes the rest, a hundred and forty-five, to auth, which spends eight and passes a hundred "
            "and thirty-seven to orders, and so on down the critical path. <bookmark mark='b'/> Payments receives "
            "eighty-two milliseconds, uses sixty, and twenty-two are left as slack. <bookmark mark='c'/> gRPC carries "
            "the remaining time in every call, so a service that sees its deadline has passed can stop at once, "
            "instead of doing work nobody will read. That is chapter eight's lesson, made exact."
        ) as vo:
            self.play(FadeIn(head), FadeIn(chain), *[GrowArrow(a) for a in arrows], Create(axis), FadeIn(ticks),
                      FadeIn(unit), Create(dl))
            vo.wait_until("a")
            for i in range(len(rows)):
                self.play(Indicate(chain[i], scale_factor=1.08), FadeIn(names[i]), FadeIn(lefts[i]), run_time=0.5)
                self.play(GrowFromEdge(works[i][0], LEFT), FadeIn(works[i][1]), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(slack), FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM,)
