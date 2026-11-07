from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace

CFG = (("naive", r"naive: \ round robin, \ no timeouts", NO),
       ("timeouts and retry", r"150 ms timeout, \ one retry elsewhere", HEAD),
       ("retry, ejection and hedging", r"$+$ outlier ejection, \ hedge at 100 ms", YES))
FAULT_COL = {"crash": NO, "partition": LAM, "slow": KERN}


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.minutes()
        self.budget()
        self.raft()
        self.ledger()

    def card(self):
        card = chapter_card(14, r"The Job service under faults", r"What does it survive, \ and what does it cost?",
                            lit=(2011, 2016), extra=((2011, r"Chaos Monkey"), (2016, r"Basiri et al.: \ chaos "
                                                                                      r"engineering")), part=PART)
        with self.voiceover("Chapter fourteen. The Job's service, broken on purpose."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def setup_(self):
        c = load("chaos")
        head = label(r"The experiment", font_size=36).to_edge(UP, buff=0.3)
        client = RoundedRectangle(width=2.2, height=0.9, corner_radius=0.12, stroke_color=DATA, stroke_width=2,
                                  fill_color=BG, fill_opacity=1)
        client_g = VGroup(client, label(r"clients", font_size=20, color=DATA).move_to(client))
        client_g.move_to(LEFT * 5 + UP * 1.2)
        reps = VGroup()
        for i in range(3):
            r = RoundedRectangle(width=2.4, height=0.75, corner_radius=0.12, stroke_color=GREY_B, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            reps.add(VGroup(r, label(rf"counter {i + 1}", font_size=19, color=GREY_A).move_to(r)))
        reps.arrange(DOWN, buff=0.3).move_to(LEFT * 0.8 + UP * 1.2)
        arrows = VGroup(*[Arrow(client_g.get_right(), r.get_left(), buff=0.1, color=GREY_C, stroke_width=2)
                          for r in reps])
        # the fault schedule, an hour on a line
        x0, x1 = 1.8, 6.6
        tl = NumberLine(x_range=[0, 60, 10], length=x1 - x0, color=GREY_C, include_numbers=False).move_to(
            [(x0 + x1) / 2, -1.4, 0])
        ticks = VGroup(*[label(rf"{m}", font_size=15, color=GREY_B).next_to(tl.n2p(m), DOWN, buff=0.1)
                         for m in range(0, 61, 10)])
        cap = label(r"minutes", font_size=16, color=GREY_B).next_to(tl, DOWN, buff=0.45)
        bands, names = VGroup(), VGroup()
        for f in c["faults"]:
            col = FAULT_COL[f["kind"]]
            a, b = tl.n2p(f["from"]), tl.n2p(f["to"])
            bnd = Rectangle(width=b[0] - a[0], height=0.35, stroke_width=0, fill_color=col, fill_opacity=0.8)
            bnd.move_to([(a[0] + b[0]) / 2, -1.05, 0])
            bands.add(bnd)
            names.add(label(rf"counter {f['replica'] + 1} {f['kind'] if f['kind'] != 'slow' else 'slow, 10x'}",
                            font_size=15, color=col).next_to(bnd, UP, buff=0.08))
        sched = VGroup(tl, ticks, cap, bands, names)
        cfgs = VGroup(*[label(t, font_size=19, color=col) for _, t, col in CFG]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        slo = label(r"steady state: \ 99.9\% of requests answered within 300 ms", font_size=20, color=WHITE).move_to(
            RIGHT * 3.7 + UP * 1.9)
        if slo.width > 6.2:
            slo.width = 6.2
        with self.voiceover(
            "The Job's counting service runs as three replicas, and clients spread requests over them. "
            "<bookmark mark='a'/> A chaos experiment starts with a hypothesis about the steady state, stated in the "
            "terms the users care about: ninety-nine point nine percent of requests answered correctly within three "
            "hundred milliseconds. <bookmark mark='b'/> Then, during one simulated hour, we break things. At minute "
            "ten the first counter crashes, and connections to it are refused at once. At minute twenty-five the "
            "second is cut off by a partition, so requests to it simply vanish. And at minute forty the third turns "
            "ten times slower, the gray failure that health checks often miss. <bookmark mark='c'/> We run the hour "
            "three times, with three clients: a naive one; one with a timeout and a single retry on another replica; "
            "and one that also ejects a replica after five failures in a row, and hedges a slow request after a "
            "hundred milliseconds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(client_g), FadeIn(reps), *[GrowArrow(a) for a in arrows])
            vo.wait_until("a")
            self.play(FadeIn(slo))
            vo.wait_until("b")
            self.play(FadeIn(tl), FadeIn(ticks), FadeIn(cap))
            for i, (bnd, nm) in enumerate(zip(bands, names)):
                self.play(GrowFromEdge(bnd, LEFT), FadeIn(nm),
                          reps[i][0].animate.set_stroke(FAULT_COL[c["faults"][i]["kind"]]), run_time=0.8)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in cfgs], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()
        _ = sched

    def minutes(self):
        c = load("chaos")
        head = label(r"Good requests, \ minute by minute", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 60, 10], [0.6, 1.0, 0.1], x_length=10.5, y_length=4.4, x_label=r"minute",
                 xticks=range(0, 61, 10), yticks=(0.6, 0.7, 0.8, 0.9, 1.0), fy=lambda v: rf"{100 * v:.0f}\%")
        g.next_to(head, DOWN, buff=0.4).shift(LEFT * 0.6)
        ax = g[0]
        bands = VGroup()
        for f in c["faults"]:
            a, b = ax.c2p(f["from"], 0.6), ax.c2p(f["to"], 1.0)
            bands.add(Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0,
                                fill_color=FAULT_COL[f["kind"]], fill_opacity=0.15).move_to((a + b) / 2))
        slo_line = DashedLine(ax.c2p(0, 0.999), ax.c2p(60, 0.999), color=WHITE, stroke_width=1.5)
        lines, keys = VGroup(), VGroup()
        for name, txt, col in CFG:
            pm = c["runs"][name]["per_minute"]
            pts = [(m + 0.5, v) for m, v in enumerate(pm)]
            lines.add(trace(ax, pts, col, width=3))
            keys.add(label(rf"{100 * c['runs'][name]['good']:.2f}\% good", font_size=19, color=col))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(g, RIGHT, buff=0.3).shift(DOWN * 0.6)
        n = c["runs"]["naive"]["by_fault"]
        with self.voiceover(
            "Here is the share of requests that met the objective, minute by minute. <bookmark mark='a'/> The naive "
            f"client loses a third of its requests whenever a replica is crashed or cut off, since one request in "
            f"three goes to it, and about {100 * (1 - n['slow']):.0f} percent while one is slow. Over the hour it "
            f"keeps {100 * c['runs']['naive']['good']:.1f} percent. <bookmark mark='b'/> A timeout and one retry "
            f"elsewhere recover almost everything: {100 * c['runs']['timeouts and retry']['good']:.2f} percent, "
            "just above the objective. The misses are requests that wait out the timeout and then meet a slow "
            "reply. <bookmark mark='c'/> Ejection and hedging close the gap: the sick replica leaves the rotation "
            "within seconds, and the few slow replies are raced by a copy. Not one request in the hour missed. The "
            "price is in the next chart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(bands), Create(slo_line))
            for mk, ln, k in zip("abc", lines, keys):
                vo.wait_until(mk)
                self.play(Create(ln), FadeIn(k), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def budget(self):
        c = load("chaos")
        head = label(r"What the hour cost", font_size=36).to_edge(UP, buff=0.3)
        rows = []
        for name, txt, col in CFG:
            r = c["runs"][name]
            rows.append([txt, rf"{r['bad']:,}", rf"{100 * r['budget_share']:.2f}\%",
                         rf"{100 * r['extra_load']:.1f}\%"])
        tab = grid_table([r"client", r"bad requests", r"of the month's budget", r"extra requests sent"], rows,
                         widths=[4.6, 2.2, 3.2, 2.8], row_h=0.62, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6)
        for r, (_, _, col) in enumerate(CFG, start=1):
            for cell in tab.cells[r]:
                cell.set_color(col)
        foot = wrapped_label(r"the error budget makes the trade explicit: \ a few percent more traffic buys back "
                             r"a seventh of a month's allowance of failure, \ in one hour", 12.4, font_size=21, color=WHITE).to_edge(
            DOWN, buff=0.7)
        nv = c["runs"]["naive"]
        with self.voiceover(
            "Count the hour against the month's error budget, a tenth of a percent of a month of requests. "
            f"<bookmark mark='a'/> The naive client burned {100 * nv['budget_share']:.0f} percent of the whole "
            "month's budget in one hour of faults. <bookmark mark='b'/> Retrying used "
            f"{100 * c['runs']['timeouts and retry']['budget_share']:.2f} percent, at the price of {100 * c['runs']['timeouts and retry']['extra_load']:.0f} percent more "
            "requests, because every timed-out or refused request was sent twice. <bookmark mark='c'/> Ejection "
            "cut the retries, since the broken replica stopped receiving traffic, so the best client was also the "
            f"cheaper of the two: {100 * c['runs']['retry, ejection and hedging']['extra_load']:.1f} percent extra. "
            "<bookmark mark='d'/> This is what an error budget is for: it turns reliability from a feeling into a "
            "number you can spend, and lets you price each defence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            for mk, r in zip("abc", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def raft(self):
        r = load("raft")
        head = label(r"The same treatment for Part 38's Raft cluster", font_size=36).to_edge(UP, buff=0.3)
        n = len(r["per_second"])
        g = axes([0, n, 10], [0, 1.0, 0.25], x_length=11.0, y_length=3.4, x_label=r"second",
                 xticks=range(0, n + 1, 10), yticks=(0, 0.5, 1.0), fy=lambda v: rf"{100 * v:.0f}\%")
        g.next_to(head, DOWN, buff=0.9)
        ax = g[0]
        bars = VGroup()
        for s, v in enumerate(r["per_second"][:-1]):
            a, b = ax.c2p(s + 0.1, 0), ax.c2p(s + 0.9, max(v, 0.005))
            bars.add(Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0,
                               fill_color=YES if v > 0.95 else HEAD if v > 0.7 else NO, fill_opacity=0.85).move_to(
                (a + b) / 2))
        marks = VGroup()
        for i, m in enumerate(r["script"]):
            p = ax.c2p(m["t"], 1.0)
            ln = DashedLine(ax.c2p(m["t"], 0), p + UP * 0.1, color=GREY_B, stroke_width=1.2)
            t = label(m["what"], font_size=15, color=GREY_A).next_to(p, UP, buff=0.15 + 0.3 * (i % 2))
            marks.add(VGroup(ln, t))
        foot = label(rf"commands committed: \ {r['committed']:,} of {r['sent']:,}; \ safety violations: "
                     rf"{r['violations']}", font_size=20, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Chaos experiments are just as useful on consensus. <bookmark mark='a'/> Here is Part 38's five-node "
            "Raft cluster taking twenty client commands a second, and the share of each second's commands that "
            "were eventually committed. <bookmark mark='b'/> When we crash the leader, there is a dip of a fraction "
            "of a second: the election timeout, then a vote. Cutting the leader off in a minority causes another. "
            "Crashing two followers costs nothing at all, because three of five is still a majority. "
            "<bookmark mark='c'/> And through all of it the safety checker found no violation: no committed command "
            "was ever lost or reordered. The cluster traded a little availability for consistency, exactly as Part "
            "38 promised it would."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.02), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def ledger(self):
        j = load("job")
        led = j["ledger"]
        head = label(r"Ledger row 19", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.26,
                           label_width=4.8).scale(0.8).move_to(UP * 0.7)
        notes = VGroup(
            label(rf"one of 42 workers ten times slow: \ {j['unhedged_seconds']:.2f} s without hedging, \ "
                  rf"{j['seconds']:.2f} s with it \ (healthy: \ {j['healthy_seconds']:.2f} s)", font_size=19,
                  color=HEAD),
            label(rf"the hedges cost {j['extra_requests']:.1f} extra requests per run of thirty, \ and also trim the "
                  r"healthy tail", font_size=19, color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        for x in notes:
            if x.width > 12.8:
                x.width = 12.8
        with self.voiceover(
            "The ledger gets row nineteen, and for once the row is not about being faster. <bookmark mark='a'/> "
            "With one of the service's forty-two workers ten times slow, the thirty books take about "
            f"{j['unhedged_seconds']:.2f} seconds without hedging, since one of them usually lands on the slow "
            f"worker, and {j['seconds']:.2f} seconds with a hedge after two hundred and forty milliseconds. "
            "<bookmark mark='b'/> That is a shade faster than the healthy service without hedges, because a hedge "
            "also trims the ordinary tail, for about two extra requests in thirty. Reliability engineering rarely "
            "makes the good case faster. It keeps the bad case close to the good one, which is what users "
            "actually notice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(tab.rows[-1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM, DATA)
