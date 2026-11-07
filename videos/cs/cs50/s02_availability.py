from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.gates import lamp, light, switch
from videos.cs.cs50.common import DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, grid_table, load

WIRE_C = GREY_B


def dur(minutes: float) -> str:
    """A downtime as a speaker would say it."""
    if minutes >= 2880:
        return rf"{minutes / 1440:.1f} days"
    if minutes >= 120:
        return rf"{minutes / 60:.1f} hours"
    if minutes >= 1:
        return rf"{minutes:.1f} min"
    return rf"{minutes * 60:.0f} s"


def pct(a: float, digits: int) -> str:
    return rf"{100 * a:.{digits}f}\%"


def nines_of(a: float) -> float:
    return -math.log10(1 - a)


def place(s, p):
    """Move a switch so that the midpoint of its two contacts is at p (its bounding box includes the raised blade)."""
    return s.shift(np.asarray(p, float) - (s.left() + s.right()) / 2)


def wire(a, b):
    return Line(a, b, color=WIRE_C, stroke_width=3)


def series_circuit(n, x0, x1, y, length=0.8):
    """A source dot, ``n`` switches one after another and a lamp, from x0 to x1 at height y."""
    src = Dot([x0, y, 0], radius=0.08, color=GREY_A)
    lp = lamp(on=True, radius=0.26).move_to([x1, y, 0])
    xs = [x0 + (x1 - x0) * (k + 1) / (n + 1) for k in range(n)]
    sws = [place(switch(closed=True, length=length), [x, y, 0]) for x in xs]
    pts = [src.get_center()] + [p for s in sws for p in (s.left(), s.right())] + [lp.get_left()]
    wires = VGroup(*[wire(pts[2 * k], pts[2 * k + 1]) for k in range(len(pts) // 2)])
    return VGroup(wires, src, *sws, lp), sws, lp


def parallel_bank(n, xl, xr, y, gap=0.8, length=0.8):
    """``n`` switches side by side between two rails at xl and xr, centred at height y."""
    ys = [y + gap * ((n - 1) / 2 - k) for k in range(n)]
    sws = [place(switch(closed=True, length=length), [(xl + xr) / 2, yy, 0]) for yy in ys]
    rails = VGroup(wire([xl, ys[0], 0], [xl, ys[-1], 0]), wire([xr, ys[0], 0], [xr, ys[-1], 0]))
    legs = VGroup(*[VGroup(wire([xl, yy, 0], s.left()), wire(s.right(), [xr, yy, 0])) for s, yy in zip(sws, ys)])
    return VGroup(rails, legs, *sws), sws


class Availability(VoiceoverScene):
    def construct(self):
        self.card()
        self.nines()
        self.laws()
        self.path()
        self.repair()
        self.common()

    def card(self):
        card = chapter_card(1, r"Availability arithmetic", r"How do the parts' nines make the whole's?",
                            lit=(1938, 1956), extra=((1938, r"Shannon: \ switching circuits"),
                                                     (1956, r"Moore and Shannon: \ reliable circuits")), part=PART)
        with self.voiceover("Chapter one. The arithmetic of availability."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def nines(self):
        rows = load("nines")["rows"]
        head = label(r"Nines are a downtime budget", font_size=36).to_edge(UP, buff=0.3)
        eq = MathTex(r"\text{nines} = -\log_{10}(1 - A)", r"\qquad \text{allowed downtime} = (1 - A)\times T",
                     font_size=34).next_to(head, DOWN, buff=0.4)
        eq[0].set_color(HEAD)
        eq[1].set_color(DATA)
        body = [[pct(r["availability"], 3 if r["availability"] > 0.9999 else (2 if r["availability"] > 0.999
                                                                                 else 1)),
                 rf"{r['nines']:.1f}", dur(r["per_year_min"]), dur(r["per_month_min"]), dur(r["per_week_min"])]
                for r in rows]
        tab = grid_table([r"availability", r"nines", r"a year", r"a 30-day month", r"a week"], body,
                         widths=[2.6, 1.5, 2.6, 2.9, 2.4], row_h=0.62, font_size=25, mono_cols=())
        tab.next_to(eq, DOWN, buff=0.45)
        hl = SurroundingRectangle(VGroup(*tab.cells[4]), color=HEAD, buff=0.08, stroke_width=2)
        foot = wrapped_label(r"a budget, \ not a promise: \ at four nines one bad deploy that takes ten minutes to "
                             r"roll back spends more than two months of it \ (illustrative)", 12.2, font_size=20,
                             color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Availability is the fraction of time a service does its job. Engineers count it in nines: "
            "<bookmark mark='a'/> the number of nines is minus the logarithm, base ten, of the unavailability, and "
            "the unavailability times a period is the downtime that period allows. <bookmark mark='b'/> Two nines "
            "allows three and a half days a year; three nines, about forty-three minutes a month; "
            "<bookmark mark='c'/> four nines, four minutes a month, or one minute a week. <bookmark mark='d'/> Think "
            "of it as a budget rather than a promise. At four nines, a bad deploy that takes ten minutes to roll back "
            "spends more than two months of it at once."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0]), tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(1, 4)], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(4, 6)], lag_ratio=0.4),
                      Create(hl))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def laws(self):
        laws = load("compose")["laws"]
        ser = {r["n"]: r for r in laws["series"]}
        par = {r["n"]: r for r in laws["parallel"]}
        head = label(r"Series and parallel, \ as Part 3's switch circuits", font_size=36).to_edge(UP, buff=0.3)
        y = 1.55
        sc, ss, slp = series_circuit(3, -6.4, -0.9, y)
        pc, ps = parallel_bank(3, 1.5, 3.9, y)
        src = Dot([0.7, y, 0], radius=0.08, color=GREY_A)
        plp = lamp(on=True, radius=0.26).move_to([5.6, y, 0])
        pw = VGroup(wire(src.get_center(), [1.5, y, 0]), wire([3.9, y, 0], plp.get_left()))
        pall = VGroup(pc, src, plp, pw)
        cap_s = label(r"up only if \textit{every} part is up", font_size=20, color=DATA).move_to(
            [sc.get_x(), -0.05, 0])
        cap_p = label(r"down only if \textit{every} part is down", font_size=20, color=YES).move_to(
            [pall.get_x(), -0.05, 0])
        eq_s = MathTex(r"A = \prod_i A_i", font_size=36, color=DATA).next_to(cap_s, DOWN, buff=0.3)
        eq_p = MathTex(r"A = 1 - \prod_i (1 - A_i)", font_size=36, color=YES).next_to(cap_p, DOWN, buff=0.3)
        ts = grid_table([r"parts at 99\%", r"in series"],
                        [[f"{n}", pct(ser[n]["up"], 1)] for n in (2, 10, 50)], widths=[2.2, 1.8], row_h=0.4,
                        font_size=19, mono_cols=())
        tp = grid_table([r"parts at 99\%", r"in parallel"],
                        [[f"{n}", pct(par[n]["up"], 2 if n == 2 else 4)] for n in (2, 3)], widths=[2.2, 1.8],
                        row_h=0.4, font_size=19, mono_cols=())
        ts.next_to(eq_s, DOWN, buff=0.3)
        tp.next_to(eq_p, DOWN, buff=0.3).align_to(ts, UP)
        foot = wrapped_label(r"for independent parts: \ in series the downtimes add, \ in parallel the nines add",
                             12.0, font_size=21, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Part 3's switch circuits show how the parts combine. Let a closed "
            "switch mean a part that is up, and a lit lamp mean the service works. <bookmark mark='a'/> In series, "
            "current needs every switch, so one part down takes the service down. If failures are independent, the "
            "probability that all are up is the product of their availabilities. Ten parts at ninety-nine percent "
            "give ninety percent; fifty give sixty. <bookmark mark='b'/> In parallel, the service is down only if "
            "every part is down, so multiply the unavailabilities instead. <bookmark mark='c'/> Two parts at "
            "ninety-nine percent give four nines; three give six. <bookmark mark='d'/> So a rule of thumb: in series "
            "the downtimes add, and in parallel the nines add."
        ) as vo:
            self.play(FadeIn(head), Create(sc[0]), FadeIn(sc[1:]), FadeIn(pall))
            vo.wait_until("a")
            self.play(ss[1].set(False), light(slp, False), FadeIn(cap_s))
            self.play(Write(eq_s), FadeIn(ts))
            self.play(ss[1].set(True), light(slp, True))
            vo.wait_until("b")
            self.play(ps[0].set(False), FadeIn(cap_p))
            self.play(ps[1].set(False))
            self.play(ps[2].set(False), light(plp, False))
            self.play(Write(eq_p))
            vo.wait_until("c")
            self.play(*[s.set(True) for s in ps], light(plp, True), FadeIn(tp))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def path(self):
        p = load("compose")["path"]
        head = label(r"A request's path is a circuit", font_size=36).to_edge(UP, buff=0.3)
        banks = (4, 2, 3, 2)
        per = (r"4 at 99.9\%", r"2 at 99.9\%", r"3 at 99\%", r"2 at 99.9\%")
        y1 = 1.55
        top = VGroup()
        lefts, rights, names = [], [], VGroup()
        for k, (n, row) in enumerate(zip(banks, p["rows"])):
            xc = -4.9 + k * 3.25
            bank, _ = parallel_bank(n, xc - 0.8, xc + 0.8, y1, gap=0.4, length=0.6)
            top.add(bank)
            lefts.append([xc - 0.8, y1, 0])
            rights.append([xc + 0.8, y1, 0])
            nm = VGroup(label(row["stage"], font_size=19, color=WHITE), label(per[k], font_size=17, color=GREY_B),
                        label(rf"{nines_of(row['up']):.0f} nines", font_size=18, color=YES)).arrange(DOWN, buff=0.08)
            nm.next_to([xc, y1 - 0.75, 0], DOWN, buff=0.0)
            names.add(nm)
        links = VGroup(*[wire(rights[k], lefts[k + 1]) for k in range(3)])
        src1 = Dot([-6.5, y1, 0], radius=0.08, color=GREY_A)
        lp1 = lamp(on=True, radius=0.24).move_to([6.45, y1, 0])
        links.add(wire(src1.get_center(), lefts[0]), wire(rights[3], lp1.get_left()))
        top.add(src1, lp1)
        tot1 = label(rf"in series: \ {pct(p['total'], 4)}, \ {p['nines']:.1f} nines, \ "
                     rf"{dur(p['downtime']['per_year_min'])} of downtime a year", font_size=21,
                     color=YES).next_to(names, DOWN, buff=0.25)
        y2 = -1.6
        sc, _, _ = series_circuit(4, -6.0, 6.0, y2, length=0.7)
        sn = VGroup()
        for k, row in enumerate(p["single"]):
            xc = -6.0 + 12.0 * (k + 1) / 5
            sn.add(VGroup(label(row["stage"], font_size=18, color=WHITE),
                          label(pct(row["up"], 1), font_size=17, color=GREY_B)).arrange(DOWN, buff=0.06).move_to(
                [xc, y2 - 0.55, 0]))
        tot2 = label(rf"one of each: \ {pct(p['single_total'], 2)}, \ {p['single_nines']:.1f} nines, \ "
                     rf"{dur(p['single_downtime']['per_year_min'])} a year", font_size=21, color=NO).next_to(
            sn, DOWN, buff=0.25)
        src = note(r"component availabilities illustrative; \ independent failures assumed", font_size=16).to_edge(
            DOWN, buff=0.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Real systems are both at once. <bookmark mark='a'/> A request passes through name servers, then a load "
            "balancer, then an application server, then the database: four stages in series. Replicate each stage, "
            "and it becomes a parallel bank worth six nines or more. <bookmark mark='b'/> Now the series "
            "law adds three parts in a million: five and a half nines, under two minutes a year. "
            "<bookmark mark='c'/> Build the same path from one of each and it reaches only "
            "ninety-eight point seven percent, almost five days a year, dominated by its weakest part, the single "
            "application server. <bookmark mark='d'/> Replication buys the nines, but every one of these figures "
            "assumes the parts fail independently."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), Create(links), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(nm[2], color=YES) for nm in names], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(tot1))
            vo.wait_until("c")
            self.play(Create(sc[0]), FadeIn(sc[1:]), FadeIn(sn))
            self.play(FadeIn(tot2), Indicate(sn[2], color=NO))
            vo.wait_until("d")
            self.play(FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def repair(self):
        r = load("renewal")
        sim, lever = r["sim"], r["lever"]
        head = label(r"Time between failures, \ time to repair", font_size=36).to_edge(UP, buff=0.3)
        year_h = 365.25 * 24
        x0, W, yb = -6.0, 12.0, 2.15
        bar = Rectangle(width=W, height=0.34, stroke_width=0, fill_color=YES, fill_opacity=0.7).move_to(
            [x0 + W / 2, yb, 0])
        fails = VGroup()
        for _, f, e in sim["first_year"]:
            if f >= year_h:
                continue
            w = max(0.06, (min(e, year_h) - f) / year_h * W)
            fails.add(Rectangle(width=w, height=0.5, stroke_width=0, fill_color=NO, fill_opacity=1).move_to(
                [x0 + (f + (min(e, year_h) - f) / 2) / year_h * W, yb, 0]))
        nfail = len(fails)
        ends = VGroup(label(r"January", font_size=16, color=GREY_B).next_to(bar, DOWN, buff=0.08).align_to(bar, LEFT),
                      label(r"December", font_size=16, color=GREY_B).next_to(bar, DOWN, buff=0.08).align_to(bar,
                                                                                                         RIGHT))
        cap = label(rf"one simulated server's year: \ {nfail} failures \ (red, \ widened to be visible)",
                    font_size=18, color=GREY_A).next_to(bar, UP, buff=0.15)
        eq = MathTex(r"A = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}}",
                     rf"= \frac{{{sim['mtbf_h']:.0f}\,\text{{h}}}}{{{sim['mtbf_h']:.0f}\,\text{{h}} + "
                     rf"{sim['mttr_h']:.0f}\,\text{{h}}}} = {100 * sim['formula']:.2f}\%", font_size=34)
        eq[0].set_color(HEAD)
        eq.next_to(bar, DOWN, buff=0.55)
        chk = label(rf"200 simulated years: \ {100 * sim['measured']:.1f}\% \ up", font_size=19,
                    color=GREY_A).next_to(eq, DOWN, buff=0.15)
        names = {"today": r"today: \ 720 h and 2 h", "fail half as often": r"fail half as often",
                 "repair twice as fast": r"repair twice as fast", "repair in 10 minutes": r"repair in 10 minutes"}
        cols = (GREY_B, DATA, YES, HEAD)
        vmax = max(x["down_min_per_year"] for x in lever)
        bars = VGroup()
        for row, col in zip(lever, cols):
            nm = label(names[row["case"]], font_size=19, color=col)
            b = Rectangle(width=max(0.05, 3.6 * row["down_min_per_year"] / vmax), height=0.32, stroke_width=0,
                          fill_color=col, fill_opacity=0.85)
            v = label(rf"{dur(row['down_min_per_year'])} down a year, \ {row['nines']:.1f} nines", font_size=18,
                      color=col)
            bars.add(VGroup(nm, b, v))
        for k, g in enumerate(bars):
            yy = -0.95 - 0.55 * k
            g[0].move_to([-3.4, yy, 0]).align_to([-6.6, 0, 0], LEFT)
            g[1].move_to([0, yy, 0]).align_to([-2.4, 0, 0], LEFT)
            g[2].next_to(g[1], RIGHT, buff=0.15)
        with self.voiceover(
            "Where does a part's availability come from? <bookmark mark='a'/> A part runs for a while, fails, is "
            "repaired, and runs again. Here is one simulated server's year: up for random stretches averaging a "
            "month, seven hundred and twenty hours, then down for repairs averaging two hours. "
            "<bookmark mark='b'/> Over a long run the fraction of time up is the mean time between failures over "
            "that plus the mean time to repair: ninety-nine point seven two percent, which two hundred simulated "
            "years confirm. <bookmark mark='c'/> The formula has two levers, and they are worth exactly the same: "
            "failing half as often and repairing twice as fast both halve the downtime. <bookmark mark='d'/> Repair "
            "is usually the cheaper one: failing over in ten minutes is worth twelve times fewer failures."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(GrowFromEdge(bar, LEFT), FadeIn(ends), FadeIn(cap), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(f, scale=1.6) for f in fails], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(eq))
            self.play(FadeIn(chk))
            vo.wait_until("c")
            for g in bars[:3]:
                self.play(FadeIn(g[0]), GrowFromEdge(g[1], LEFT), FadeIn(g[2]), run_time=0.8)
            vo.wait_until("d")
            g = bars[3]
            self.play(FadeIn(g[0]), GrowFromEdge(g[1], LEFT), FadeIn(g[2]))
        self.wait(0.4)
        self.clear_scene()

    def common(self):
        rows = load("common")["rows"]
        head = label(r"Correlated failures break the arithmetic", font_size=36).to_edge(UP, buff=0.3)
        y = 0.9
        src = Dot([-6.4, y, 0], radius=0.08, color=GREY_A)
        shared = place(switch(closed=True, length=0.8, color=NO), [-5.2, y, 0])
        sh_l = label(r"shared cause", font_size=19, color=NO).next_to(shared, DOWN, buff=0.25)
        bank, _ = parallel_bank(3, -4.0, -1.8, y)
        lp = lamp(on=True, radius=0.26).move_to([-0.7, y, 0])
        ws = VGroup(wire(src.get_center(), shared.left()), wire(shared.right(), [-4.0, y, 0]),
                    wire([-1.8, y, 0], lp.get_left()))
        rep_l = label(r"3 replicas, \ each 99.9\%", font_size=19, color=DATA).next_to(bank, DOWN, buff=0.25)
        circ = VGroup(src, shared, sh_l, bank, lp, ws, rep_l)
        eq = MathTex(r"A = (1 - cq)\,\big(1 - q'^{\,3}\big)", font_size=32, color=HEAD).next_to(
            circ, DOWN, buff=0.45).set_x(-3.5)
        eqn = wrapped_label(r"a share $c$ of each replica's downtime $q$ is common: \ a bad deploy, \ one power "
                            r"feed, \ one configuration; \ it acts as a part in \textit{series}", 5.8, font_size=19,
                            color=GREY_A).next_to(eq, DOWN, buff=0.25)
        vals = [r["nines"] for r in rows]
        chart = bar_chart(vals, [rf"{100 * r['share']:.0f}\%" for r in rows], [YES, HEAD, KERN, NO, NO],
                          height=3.4, bar_w=0.62, gap=0.42, vmax=9.5, fmt_=lambda v: f"{v:.1f}", font_size=19)
        chart.move_to([3.6, 0.0, 0])
        ctitle = label(r"nines of the three, \ by common share $c$", font_size=20, color=WHITE).next_to(
            chart, UP, buff=0.3)
        foot = wrapped_label(r"the common part caps the whole at its own availability, \ $1 - cq$: \ the Hook's three "
                             r"outages were each one change, \ everywhere at once", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Three replicas at ninety-nine point nine percent "
            "each promise nine nines, if they fail independently. <bookmark mark='b'/> But suppose a share of each "
            "replica's downtime has a common cause: a bad deploy, one power feed, one configuration file. That cause "
            "is a switch in series with the whole bank, and when it opens, every replica is down together. "
            "<bookmark mark='c'/> If just one percent of the downtime is shared, the three give five nines, not nine. "
            "At ten percent, four; at thirty percent, three and a half. <bookmark mark='d'/> The common part caps the "
            "whole at its own availability. The three post-mortems that opened this part were all of this kind: one "
            "change, applied everywhere at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(circ))
            vo.wait_until("a")
            self.play(FadeIn(ctitle), FadeIn(chart.bars[0]), FadeIn(chart.vals[0]), FadeIn(chart.names[0]),
                      FadeIn(chart[0]))
            vo.wait_until("b")
            self.play(shared.set(False), light(lp, False), Write(eq))
            self.play(FadeIn(eqn))
            self.play(shared.set(True), light(lp, True))
            vo.wait_until("c")
            for k in range(1, len(rows)):
                self.play(GrowFromEdge(chart.bars[k], DOWN), FadeIn(chart.vals[k]), FadeIn(chart.names[k]),
                          run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM)
