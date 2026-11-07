from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, trace

STRAT = {"no backoff": (r"no backoff", NO), "exponential": (r"exponential", KERN),
         "full jitter": (r"full jitter", YES), "equal jitter": (r"equal jitter", DATA),
         "decorrelated jitter": (r"decorrelated jitter", LAM)}


def box(text, col, w=2.4, h=1.0, size=22):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=col, stroke_width=2.2, fill_color=BG,
                         fill_opacity=1)
    return VGroup(r, label(text, font_size=size, color=col).move_to(r))


class Retries(VoiceoverScene):
    def construct(self):
        self.card()
        self.timeouts()
        self.timelines()
        self.compared()
        self.budget()
        self.hedging()

    def card(self):
        card = chapter_card(4, r"Timeouts, retries, backoff and jitter", r"When should a client try again?",
                            lit=(1976, 2015), extra=((1976, r"Metcalfe and Boggs: \ Ethernet's backoff"),
                                                     (2015, r"Brooker: \ backoff and jitter")), part=PART)
        with self.voiceover("Chapter four. Timeouts, retries, backoff and jitter."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def timeouts(self):
        head = label(r"Timeouts, \ and retries that multiply", font_size=36).to_edge(UP, buff=0.3)
        names = (r"user's app", r"front end", r"service", r"database")
        cols = (DATA, GREY_A, GREY_A, NO)
        boxes = VGroup(*[box(n, c) for n, c in zip(names, cols)]).arrange(RIGHT, buff=1.1).move_to(UP * 1.1)
        arrows = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.1, color=GREY_B,
                                stroke_width=2.5) for k in range(3)])
        tries = VGroup(*[label(r"up to 4 tries", font_size=17, color=HEAD).next_to(a, UP, buff=0.1) for a in arrows])
        counts = VGroup(*[label(rf"{4 ** (k + 1)} \ attempts", font_size=22, color=NO if k == 2 else HEAD).next_to(
            boxes[k + 1], DOWN, buff=0.25) for k in range(3)])
        one = label(r"1 \ action", font_size=22, color=DATA).next_to(boxes[0], DOWN, buff=0.25)
        down = label(r"down", font_size=18, color=NO).next_to(boxes[3], UP, buff=0.12)
        ill = note(r"illustrative: \ every layer retries three times", font_size=16).next_to(counts, DOWN, buff=0.25)
        ill.align_to(boxes, RIGHT)
        rules = VGroup(
            wrapped_label(r"a \textbf{timeout} turns an endless wait into a known failure: \ set it from the "
                          r"dependency's measured latency, \ a little above its p99.9", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"pass the \textbf{deadline} downstream, \ so inner layers stop working for callers who "
                          r"have given up", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"retry at \textbf{one} layer, \ and only requests that are safe to repeat \ (idempotency "
                          r"keys, \ Part 43)", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A request that never returns is worse than one that fails. <bookmark mark='a'/> A timeout turns an "
            "endless wait into a known failure; set it from the dependency's measured latency, a little above its "
            "ninety-nine point nine percentile, and pass the deadline down, so that inner layers stop working for "
            "callers who have given up. <bookmark mark='b'/> Failures can be retried. But look what "
            "happens when every layer does it. The database is down, and each of three layers tries four times. "
            "<bookmark mark='c'/> One tap becomes sixty-four attempts on a database that is already struggling. "
            "<bookmark mark='d'/> So retry at one layer only, and only requests that are safe to repeat, with "
            "Part 43's idempotency keys."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), *[GrowArrow(a) for a in arrows])
            vo.wait_until("a")
            self.play(FadeIn(rules[0]))
            self.play(FadeIn(rules[1]))
            vo.wait_until("b")
            self.play(FadeIn(down), boxes[3][0].animate.set_stroke(NO, 3.5), FadeIn(tries), FadeIn(one))
            for c in counts:
                self.play(FadeIn(c, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("c")
            self.play(Indicate(counts[2], color=NO, scale_factor=1.3), FadeIn(ill))
            vo.wait_until("d")
            self.play(FadeIn(rules[2]))
        self.wait(0.4)
        self.clear_scene()

    def timelines(self):
        tl = load("jitter")["timelines"]
        head = label(r"Twenty clients, \ one contended resource", font_size=36).to_edge(UP, buff=0.3)
        X0, W, TMAX = -6.0, 9.8, 3000.0
        LMAX = math.log10(1 + TMAX)

        def xpos(t):
            return X0 + W * math.log10(1 + t) / LMAX
        panels = VGroup()
        results = VGroup()
        specs = (("no backoff", r"no backoff: \ retry after 1 unit", NO),
                 ("exponential", r"exponential backoff: \ wait $2^k$ units", KERN),
                 ("full jitter", r"exponential backoff with full jitter: \ wait a random time in $[0, 2^k]$", YES))
        ph, gap, top = 1.15, 0.5, 2.45
        for p, (key, title, col) in enumerate(specs):
            att = tl[key]
            y_top = top - p * (ph + gap)
            frame = Rectangle(width=W, height=ph, stroke_color=GREY_D, stroke_width=1).move_to(
                [X0 + W / 2, y_top - ph / 2, 0])
            ttl = label(title, font_size=18, color=col).next_to(frame, UP, buff=0.06).align_to(frame, LEFT)
            clients = sorted({c for _, c in att})
            rowh = (ph - 0.1) / len(clients)
            marks = VGroup()
            last = {}
            for t, c in att:
                last[c] = max(last.get(c, 0.0), t)
            cell = 0.025
            for i, c in enumerate(clients):
                y = y_top - 0.05 - rowh * (i + 0.5)
                buckets = sorted({int(xpos(t) / cell) for t, cc in att if cc == c})
                runs, start, prev = [], None, None
                for b in buckets:
                    if start is None:
                        start = prev = b
                    elif b == prev + 1:
                        prev = b
                    else:
                        runs.append((start, prev))
                        start = prev = b
                if start is not None:
                    runs.append((start, prev))
                for a, z in runs:
                    w = max(0.035, (z - a + 1) * cell)
                    marks.add(Rectangle(width=w, height=rowh * 0.7, stroke_width=0, fill_color=col,
                                        fill_opacity=0.85).move_to([a * cell + (z - a + 1) * cell / 2, y, 0]))
            wins = VGroup()
            if key == "full jitter":
                for i, c in enumerate(clients):
                    y = y_top - 0.05 - rowh * (i + 0.5)
                    wins.add(Dot([xpos(last[c]), y, 0], radius=0.045, color=WHITE))
                res = wrapped_label(rf"{len(att)} attempts; \ all {len(clients)} done by "
                                    rf"$t = {max(last.values()):.0f}$", 2.4, font_size=17, color=YES)
            else:
                cnt = f"{len(att):,}".replace(",", "{,}")
                res = wrapped_label(cnt + r" attempts by $t = 3{,}000$; \ none done", 2.4, font_size=17, color=col)
            res.next_to(frame, RIGHT, buff=0.2)
            panels.add(VGroup(frame, ttl, marks, wins))
            results.add(res)
        base_y = top - 3 * ph - 2 * gap
        ticks = VGroup(*[label(rf"{v:,}".replace(",", "{,}"), font_size=16, color=GREY_B).move_to(
            [xpos(v), base_y - 0.22, 0]) for v in (1, 10, 100, 1000)])
        xl = label(r"time, \ in units of one write \ (log scale)", font_size=17, color=GREY_A).next_to(
            ticks, DOWN, buff=0.08).set_x(X0 + W / 2)
        with self.voiceover(
            "Retry immediately, and clients that failed together fail together again. <bookmark mark='a'/> Here "
            "twenty clients each need one write to the same record; a write fails if another overlaps it. With no "
            "backoff they collide every time, for ever. "
            "<bookmark mark='b'/> Exponential backoff, waiting one, two, four, eight units, makes far fewer "
            "attempts, but the clients stay in lockstep, wait the same time, and collide again. "
            "<bookmark mark='c'/> Add jitter, a random wait between zero and the exponential bound, and the herd "
            "spreads out. The white dots are successes: all twenty finish, after a hundred and seventy-five "
            "attempts. Randomness breaks the symmetry, as it did for Ethernet in 1976."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(pn[0]) for pn in panels], FadeIn(ticks), FadeIn(xl))
            for mk, pn, res in zip("abc", panels, results):
                vo.wait_until(mk)
                self.play(FadeIn(pn[1]))
                self.play(LaggedStart(*[FadeIn(m) for m in pn[2]], lag_ratio=0.002), run_time=2.0)
                if len(pn[3]):
                    self.play(LaggedStart(*[FadeIn(d, scale=2) for d in pn[3]], lag_ratio=0.1), run_time=1.5)
                self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def compared(self):
        rows = load("jitter")["rows"]
        head = label(r"Four ways to back off", font_size=36).to_edge(UP, buff=0.3)
        by = {(r["clients"], r["strategy"]): r for r in rows}
        n = 100
        formulas = {"no backoff": r"$b$", "exponential": r"$v = \min(c,\ b\,2^k)$",
                    "full jitter": r"$\mathrm{rand}(0,\ v)$", "equal jitter": r"$v/2 + \mathrm{rand}(0,\ v/2)$",
                    "decorrelated jitter": r"$\min(c,\ \mathrm{rand}(b,\ 3\,d_{\mathrm{prev}}))$"}
        W = [2.7, 3.6, 3.8, 2.4]
        xs = [-6.3 + sum(W[:k]) + W[k] / 2 for k in range(4)]
        y0, rh = 2.25, 0.62
        hdr = VGroup(*[label(t, font_size=18, color=GREY_B).move_to([x, y0, 0]) for t, x in
                       zip((r"strategy", r"wait before retry $k$", rf"calls, \ {n} clients \ (log)",
                            r"time until all done"), xs)])
        rule = Line([-6.3, y0 - 0.3, 0], [-6.3 + sum(W), y0 - 0.3, 0], color=GREY_D, stroke_width=1.5)
        lines = VGroup()
        lo, hi = math.log10(n), math.log10(max(by[(n, s)]["calls"] for s in STRAT))
        for i, s in enumerate(STRAT):
            r = by[(n, s)]
            name, col = STRAT[s]
            y = y0 - 0.7 - i * rh
            nm = label(name, font_size=20, color=col).move_to([xs[0], y, 0]).align_to([-6.25, 0, 0], LEFT)
            f = label(formulas[s], font_size=20, color=WHITE).move_to([xs[1], y, 0])
            frac = (math.log10(r["calls"]) - lo) / (hi - lo)
            bar = Rectangle(width=max(0.05, 2.3 * frac), height=0.3, stroke_width=0, fill_color=col,
                            fill_opacity=0.85).move_to([xs[2] - W[2] / 2 + 0.1, y, 0], aligned_edge=LEFT)
            val = label(rf"{r['calls']:,.0f}".replace(",", "{,}"), font_size=18, color=col).next_to(bar, RIGHT,
                                                                                                    buff=0.1)
            tm = label(rf"{r['time']:,.0f}".replace(",", "{,}") if r["time"] else r"never", font_size=19,
                       color=col if r["time"] else NO).move_to([xs[3], y, 0])
            lines.add(VGroup(nm, f, bar, val, tm))
        fj, dj = by[(50, "full jitter")], by[(50, "decorrelated jitter")]
        notes = VGroup(
            wrapped_label(r"$b = 1$ unit, \ cap $c = 1{,}000$; \ averages of 10 runs; \ ``never'': \ not all done "
                          r"by $t = 20{,}000$", 12.4, font_size=18, color=GREY_A),
            wrapped_label(rf"among the jittered three the differences are small and depend on the load: \ with 50 "
                          rf"clients decorrelated jitter finished first \ ({dj['time']:.0f} against {fj['time']:.0f})",
                          12.4, font_size=19, color=WHITE),
            wrapped_label(r"Brooker \ (AWS, \ 2015) \ found the same: \ backoff without jitter is the mistake; \ any "
                          r"jitter is far better", 12.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Marc Brooker compared ways to back off in 2015; we repeat his experiment with a hundred "
            "clients. <bookmark mark='a'/> With no backoff, almost a million calls, and the clients never all "
            "finish. Plain exponential backoff cuts the calls to under three thousand, but still never finishes. "
            "<bookmark mark='b'/> Full jitter waits a random time up to the exponential bound. Equal jitter keeps "
            "half the bound and randomizes the rest. Decorrelated jitter grows from the previous wait instead. All "
            "three finish, with about a thousand to eighteen hundred calls. <bookmark mark='c'/> Between them the "
            "differences are small, and change with the load. The lesson is the one Brooker drew: backoff without "
            "jitter is the mistake; any jitter is far better."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), Create(rule), FadeIn(notes[0]))
            vo.wait_until("a")
            for ln in lines[:2]:
                self.play(FadeIn(ln[0]), FadeIn(ln[1]), GrowFromEdge(ln[2], LEFT), FadeIn(ln[3]), FadeIn(ln[4]))
            vo.wait_until("b")
            for ln in lines[2:]:
                self.play(FadeIn(ln[0]), FadeIn(ln[1]), GrowFromEdge(ln[2], LEFT), FadeIn(ln[3]), FadeIn(ln[4]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def budget(self):
        o = load("overload")
        bo, bu = o["backoff"], o["budget"]
        t0, t1, frac = bu["trigger"]
        cap = bu["capacity"]
        T = len(bu["offered"])
        late_bo = sum(bo["offered"][60:]) / len(bo["offered"][60:])
        late_bu = sum(bu["offered"][60:]) / len(bu["offered"][60:])
        head = label(r"Backoff spreads retries; \ a budget limits them", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, T, 20], [0, 400, 100], x_length=9.4, y_length=4.2, x_label=r"seconds",
                 xticks=range(0, T + 1, 20), yticks=(0, 100, 200, 300, 400), font=16)
        g.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        ax = g.ax
        ylab = label(r"requests a second", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        band = Rectangle(width=ax.c2p(t1, 0)[0] - ax.c2p(t0, 0)[0], height=ax.c2p(0, 400)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=NO, fill_opacity=0.12).move_to(
            (ax.c2p(t0, 0) + ax.c2p(t1, 400)) / 2)
        band_l = label(r"trigger", font_size=16, color=NO).next_to(band, UP, buff=0.05)
        cap_pts = [(0, cap), (t0, cap), (t0, cap * frac), (t1, cap * frac), (t1, cap), (T, cap)]
        cap_line = DashedVMobject(trace(ax, cap_pts, WHITE, width=2), num_dashes=60)

        def series(v):
            return [(s + 0.5, x) for s, x in enumerate(v)]
        off_bo = trace(ax, series(bo["offered"]), NO, width=2.5)
        good_bo = trace(ax, series(bo["goodput"]), KERN, width=3)
        off_bu = trace(ax, series(bu["offered"]), DATA, width=2.5)
        good_bu = trace(ax, series(bu["goodput"]), YES, width=3)
        right = ax.get_right()[0] + 0.2
        k_bo = wrapped_label(rf"backoff with full jitter: \ still about {late_bo:.0f} sent a second, \ none answered "
                             r"in time", 2.5, font_size=17, color=NO).move_to([right, ax.c2p(0, 320)[1], 0],
                                                                             aligned_edge=LEFT)
        k_bu = wrapped_label(rf"retry budget, \ 10\%: \ about {late_bu:.0f} sent; \ answered again "
                             rf"{bu['recovered_s']:.0f} s after the trigger", 2.5, font_size=17,
                             color=YES).move_to([right, ax.c2p(0, 150)[1], 0], aligned_edge=LEFT)
        foot = wrapped_label(r"a retry budget: \ each client may add retries worth at most 10\% of its first attempts "
                             r"\ (a token bucket, \ Part 48); \ the SRE book suggests the same ratio", 12.4,
                             font_size=19, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Back to chapter three's metastable server. <bookmark mark='a'/> "
            "Give them exponential backoff with full jitter. It does not help. Backoff spreads the retries out in "
            "time, but every timed-out request still makes up to four attempts, and the sent load stays near three "
            "hundred a second. The loop holds. <bookmark mark='b'/> What breaks it is limiting the number of "
            "retries. With a retry budget, each client may add retries worth at most a tenth of its first attempts, "
            "kept as a token bucket like Part 48's rate limiter. <bookmark mark='c'/> The sent load can rise only "
            "ten percent above demand, the queue drains, and the server answers again nineteen seconds after the "
            "trigger. Google's SRE book recommends the same ten percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ylab), Create(cap_line), FadeIn(band), FadeIn(band_l))
            vo.wait_until("a")
            self.play(Create(off_bo), Create(good_bo), run_time=2.5)
            self.play(FadeIn(k_bo))
            vo.wait_until("b")
            self.play(off_bo.animate.set_stroke(opacity=0.3), good_bo.animate.set_stroke(opacity=0.3),
                      k_bo.animate.set_opacity(0.45), FadeIn(foot))
            vo.wait_until("c")
            self.play(Create(off_bu), Create(good_bu), run_time=2.5)
            self.play(FadeIn(k_bu))
        self.wait(0.4)
        self.clear_scene()

    def hedging(self):
        rows = load("hedging")["rows"]
        head = label(r"Hedged requests: \ racing the tail", font_size=36).to_edge(UP, buff=0.3)
        # the idea, as two lanes of time (illustrative)
        x0, sc = -6.2, 0.022
        lane_a = label(r"server A", font_size=18, color=GREY_A).move_to([x0 + 0.55, 2.5, 0])
        lane_b = label(r"server B", font_size=18, color=GREY_A).move_to([x0 + 0.55, 1.9, 0])
        s0 = x0 + 1.3
        bar_a = Rectangle(width=200 * sc, height=0.36, stroke_width=0, fill_color=NO, fill_opacity=0.75).move_to(
            [s0 + 100 * sc, 2.5, 0])
        a_txt = label(r"a pause: \ 200 ms", font_size=16, color=WHITE).move_to(bar_a)
        hedge_t = 20
        bar_b = Rectangle(width=7 * sc, height=0.36, stroke_width=0, fill_color=YES, fill_opacity=0.9).move_to(
            [s0 + (hedge_t + 3.5) * sc, 1.9, 0])
        hl = DashedLine([s0 + hedge_t * sc, 2.8, 0], [s0 + hedge_t * sc, 1.6, 0], color=HEAD, stroke_width=2)
        hl_t = label(r"no answer by 20 ms: \ send a copy", font_size=16, color=HEAD).next_to(hl, DOWN, buff=0.08)
        hl_t.align_to(hl, LEFT)
        won = label(r"first answer wins; \ cancel the other", font_size=16, color=YES).next_to(bar_b, RIGHT, buff=0.2)
        cut = Line(bar_a.get_left() + RIGHT * (hedge_t + 7) * sc + UP * 0.25,
                   bar_a.get_left() + RIGHT * (hedge_t + 7) * sc + DOWN * 0.25, color=WHITE, stroke_width=3)
        ill = note(r"illustrative", font_size=16).next_to(bar_a, RIGHT, buff=0.2)
        idea = VGroup(lane_a, lane_b, bar_a, a_txt, ill)
        # the measured trade-off
        g = axes([0, 12, 2], [0, 250, 50], x_length=6.4, y_length=3.2, x_label=r"extra requests sent",
                 xticks=(0, 2, 4, 6, 8, 10, 12), yticks=(0, 50, 100, 150, 200), fx=lambda v: rf"{v:g}\%", font=16)
        g.move_to([-2.75, -1.75, 0])
        ax = g.ax
        ylab = label(r"p99 latency, \ ms", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        pts = [(100 * r["extra_load"], r["p99"]) for r in rows]
        curve = trace(ax, pts, HEAD, width=2.5)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.07, color=HEAD) for x, y in pts])
        tags = VGroup()
        for r, (x, y) in zip(rows, pts):
            txt = r"no hedging" if r["hedge_at_ms"] is None else rf"hedge at {r['hedge_at_ms']:.0f} ms"
            t = label(txt + rf": \ {r['p99']:.0f} ms", font_size=16, color=WHITE)
            t.next_to(ax.c2p(x, y), UR, buff=0.1)
            tags.add(t)
        tags[3].next_to(ax.c2p(*pts[3]), UP, buff=0.3).shift(LEFT * 0.5)
        tags[0].next_to(ax.c2p(*pts[0]), RIGHT, buff=0.18)
        side = VGroup(
            wrapped_label(r"simulated: \ each reply takes an exponential time, \ mean 5 ms, \ but 2\% of requests hit "
                          r"a 200 ms pause", 4.7, font_size=18, color=GREY_A),
            wrapped_label(rf"hedging at 50 ms cuts the p99 from {rows[0]['p99']:.0f} to {rows[1]['p99']:.0f} ms for "
                          rf"{100 * rows[1]['extra_load']:.0f}\% more requests", 4.7, font_size=19, color=YES),
            wrapped_label(r"Dean and Barroso, \ ``The Tail at Scale'' \ (2013); \ the tail of Part 39; \ hedge only "
                          r"requests that are safe to repeat", 4.7, font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.3, -1.3, 0])
        with self.voiceover(
            "One kind of retry makes things faster. <bookmark mark='a'/> A request goes to server A, which happens "
            "to be in a long pause. <bookmark mark='b'/> If no answer has come by a short deadline, send a copy to "
            "server B, take whichever answer comes first, and cancel the other. Jeffrey Dean and Luiz Barroso called "
            "these hedged requests, in The Tail at Scale: the tail of Part 39. <bookmark mark='c'/> In our "
            "simulation, replies are usually quick, but one request in fifty hits a two-hundred-millisecond pause. "
            "Without hedging the ninety-ninth percentile is two hundred milliseconds. <bookmark mark='d'/> Hedging at "
            "fifty milliseconds cuts it to fifty-three, for two percent more requests; at twenty, to twenty-five, "
            "for under four percent. Hedge earlier, and the extra load grows faster than the tail shrinks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lane_a), FadeIn(lane_b))
            vo.wait_until("a")
            self.play(GrowFromEdge(bar_a, LEFT), FadeIn(a_txt), FadeIn(ill), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(hl), FadeIn(hl_t))
            self.play(GrowFromEdge(bar_b, LEFT), FadeIn(won), Create(cut))
            vo.wait_until("c")
            self.play(FadeIn(g), FadeIn(ylab), FadeIn(side[0]))
            self.play(FadeIn(dots[0]), FadeIn(tags[0]))
            vo.wait_until("d")
            self.play(Create(curve), LaggedStart(*[FadeIn(d) for d in dots[1:]], lag_ratio=0.4),
                      LaggedStart(*[FadeIn(t) for t in tags[1:]], lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
        _ = idea


_ = (DATA, LAM)
