from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, CLAIM, FAIL, GOOD, HIST, PART, REWARD, load

FRONT, OTHER, P80 = C.BITS, GREY_C, C.TRUE_P


def minutes_tex(m: float) -> str:
    if m < 1:
        return rf"{m * 60:.0f}\,\text{{s}}"
    if m < 60:
        return rf"{m:.0f}\,\text{{min}}"
    return rf"{m / 60:.1f}\,\text{{h}}"


class Doubling(VoiceoverScene):
    def construct(self):
        self.card()
        self.measure()
        self.trend()
        self.eighty()
        self.ceiling()

    def card(self):
        card = chapter_card(6, r"Horizons that double", r"How long a task can an agent finish?", lit=(2026,), part=PART)
        with self.voiceover("Chapter six. Horizons that double."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def measure(self):
        g = axes([-1, 3, 1], [0, 1, 0.5], x_length=7.0, y_length=3.8, xlabel=r"how long the task takes a skilled person "
                 r"(log scale)", ylabel=r"the agent's success rate", xticks=[-1, 0, 1, 2, 3],
                 xfmt=lambda v: {-1: r"6\,\text{s}", 0: r"1\,\text{min}", 1: r"10\,\text{min}", 2: r"1.7\,\text{h}",
                                 3: r"17\,\text{h}"}[int(v)], yticks=[0, 0.5, 1], yfmt=lambda v: f"{int(100 * v)}\\%",
                 center=[-2.0, -0.4, 0])
        ax = g.ax
        rs = np.random.default_rng(4)
        xs = rs.uniform(-1, 3, 40)
        h = 1.2
        ys = (rs.random(40) < 1 / (1 + np.exp(2.2 * (xs - h)))).astype(float)
        dots = VGroup(*[Dot(ax.c2p(x, y * 0.96 + 0.02), radius=0.05, color=AGENT).set_opacity(0.8) for x, y in zip(xs, ys)])
        xx = np.linspace(-1, 3, 80)
        fit = curve(ax, xx, 1 / (1 + np.exp(2.2 * (xx - h))), AGENT, 3.5)
        half = DashedLine(ax.c2p(-1, 0.5), ax.c2p(h, 0.5), color=GREY_B)
        vline = DashedLine(ax.c2p(h, 0), ax.c2p(h, 0.5), color=FRONT)
        hl = label(r"the $50\%$ time horizon", font_size=22, color=FRONT).next_to(ax.c2p(h, 0), DOWN, buff=0.55)
        tag = note(r"schematic: \ one model, \ made-up tasks").to_corner(DL, buff=0.3)
        hist = history_card(2025, r"METR \ (Kwa, West, Becker et al.)", r"software and research tasks from seconds to "
                            r"many hours, \ each timed by skilled people; \ for each model, \ success against the "
                            r"log of that time, \ fitted with a logistic curve", width=5.4, color=HIST,
                            font_size=19).to_corner(UR, buff=0.3)
        with self.voiceover(
            "The research group METR turned the length of a task into a measuring stick for agents. "
            "<bookmark mark='a'/> Take hundreds of software and research tasks, and time skilled people doing each "
            "one: some take seconds, some take a working day. <bookmark mark='b'/> Run an agent on all of them and "
            "plot success against the human time, on a log scale. Short tasks it mostly gets, long ones mostly not. "
            "<bookmark mark='c'/> Fit a logistic curve, and read off where it crosses one half: the task length the "
            "agent finishes half the time, its fifty-percent time horizon. Part 31 looks at how this is measured "
            "in detail; here we follow what it shows about agents."
        ) as vo:
            self.play(FadeIn(g), FadeIn(hist), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(fit), run_time=1.5)
            self.play(Create(half), Create(vline), FadeIn(hl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plot(self):
        m = load("metr")
        rows = m["rows"]
        y_lo, y_hi = -5, 11  # log2 minutes: 2 s to 34 h
        g = axes([0, 7.6, 1], [y_lo, y_hi, 1], x_length=8.6, y_length=5.0, xticks=[0, 2, 4, 6],
                 xfmt=lambda v: f"{2019 + int(v)}", yticks=[-4, 0, 4, 8], ylabel=r"$50\%$ time horizon \ (log scale)",
                 yfmt=lambda v: {-4: r"4\,\text{s}", 0: r"1\,\text{min}", 4: r"16\,\text{min}", 8: r"4.3\,\text{h}"}[int(v)],
                 center=[-1.9, -0.35, 0])
        return m, rows, g, g.ax

    def trend(self):
        m, rows, g, ax = self.plot()
        pts = VGroup()
        for r in rows:
            col = FRONT if r["sota"] else OTHER
            y = math.log2(r["p50"])
            d = Dot(ax.c2p(r["t"], y), radius=0.065 if r["sota"] else 0.05, color=col)
            err = Line(ax.c2p(r["t"], math.log2(r["lo"])), ax.c2p(r["t"], min(math.log2(r["hi"]), 11)), color=col,
                       stroke_width=1.5).set_opacity(0.5)
            pts.add(VGroup(err, d))
        c23 = m["coef_2023"]
        t0, t1 = float(m["t2023"]), 7.4
        line = DashedLine(ax.c2p(t0, c23[0] + c23[1] * t0), ax.c2p(t1, c23[0] + c23[1] * t1), color=WHITE)
        ca = m["coef_all"]
        line_all = DashedLine(ax.c2p(0, ca[0]), ax.c2p(t1, ca[0] + ca[1] * t1), color=GREY_B).set_opacity(0.6)
        d23, (lo, hi) = float(m["doubling_2023"]), m["doubling_ci"]
        mine = VGroup(label(rf"since 2023: \ doubling every ${d23:.0f}$ days", font_size=24, color=WHITE),
                      label(rf"bootstrap $95\%$: \ ${lo:.0f}$--${hi:.0f}$ days", font_size=20, color=GREY_A),
                      label(rf"since 2019: \ every ${float(m['doubling_all']):.0f}$ days", font_size=22, color=GREY_B))
        mine.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.4)
        first = max((r for r in rows if r["sota"] and r["p50"] <= m["reliable_min"]), key=lambda r: r["t"])
        names = VGroup()
        for r in rows:
            if r["name"] in ("GPT-2", "GPT-4", "o3", first["name"]):
                names.add(label(r["name"], font_size=17, color=FRONT).next_to(ax.c2p(r["t"], math.log2(r["p50"])), LEFT,
                                                                             buff=0.12))
        leg = VGroup(VGroup(Dot(color=FRONT, radius=0.06), label(r"the frontier when released", font_size=18, color=FRONT))
                     .arrange(RIGHT, buff=0.12),
                     VGroup(Dot(color=OTHER, radius=0.05), label(r"other models", font_size=18, color=OTHER))
                     .arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(mine, DOWN, buff=0.4)
        leg.align_to(mine, LEFT)
        tag = note(r"published: \ METR, Time Horizon 1.1 (metr.org); \ the fit is computed here; \ bars: METR's "
                   r"$95\%$ intervals", font_size=17).to_edge(DOWN, buff=0.12)
        metr = m["metr"]
        agree = abs(d23 - metr["from_2023"]) < 3
        said = ("which is METR's own fit." if agree else f"against METR's own {metr['from_2023']:.0f}.")
        first_h = first["p50"] / 60
        by = {r["name"]: r["p50"] for r in rows}
        with self.voiceover(
            "Here are METR's measurements: every model they tested, by release date, on a log scale of minutes. "
            f"<bookmark mark='a'/> GPT-2, in 2019, finished tasks of {60 * by['GPT-2']:.0f} seconds. GPT-4, in "
            f"2023, about {by['GPT-4']:.0f} minutes. <bookmark mark='b'/> On a log scale the frontier climbs in a straight line, and a straight "
            "line on a log scale means a fixed doubling time. <bookmark mark='c'/> Fitting the frontier models "
            f"since 2023 gives one doubling every {d23:.0f} days, {said} Over the whole span since 2019, it is "
            f"{float(m['doubling_all']):.0f} days: the pace has quickened. <bookmark mark='d'/> The last frontier model "
            f"inside METR's reliable range, {first['name']}, finishes tasks of about {first_h:.0f} hours half the "
            "time. By the reasoning of the last chapter, every doubling is a halving of the error per step."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, scale=1.3) for p_ in pts], lag_ratio=0.08), run_time=3.0)
            self.play(FadeIn(names[:2]))
            vo.wait_until("b")
            self.play(Create(line_all), run_time=1.0)
            vo.wait_until("c")
            self.play(Create(line), FadeIn(mine[:2]), run_time=1.5)
            self.play(FadeIn(mine[2]))
            vo.wait_until("d")
            self.play(FadeIn(names[2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def eighty(self):
        m, rows, g, ax = self.plot()
        p50 = VGroup(*[Dot(ax.c2p(r["t"], math.log2(r["p50"])), radius=0.055, color=FRONT if r["sota"] else OTHER)
                       for r in rows])
        p80 = VGroup(*[Dot(ax.c2p(r["t"], math.log2(r["p80"])), radius=0.055, color=P80) for r in rows])
        links = VGroup(*[Line(a_.get_center(), b_.get_center(), color=GREY_D, stroke_width=1.2) for a_, b_ in zip(p50, p80)])
        ratio, ch = float(m["ratio_median"]), float(m["ratio_hazard"])
        rows_ = [cmath(r"P(\text{done} \mid t)", r"=", r"e^{-\lambda t}", font_size=32),
                 cmath(r"\frac{t_{50}}{t_{80}}", r"=", r"\frac{\ln 2}{\ln 1.25}", r"=", rf"{ch:.1f}", font_size=32)]
        box = VGroup(label(r"if every minute of work \\ failed with the same chance $\lambda$:", font_size=20, color=GREY_A),
                     *rows_).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.35)
        meas = label(rf"measured: \ median $t_{{50}}/t_{{80}} = {ratio:.1f}$", font_size=24, color=P80)
        meas.next_to(box, DOWN, buff=0.35).align_to(box, LEFT)
        d80 = float(m["doubling_80"])
        k80 = label(rf"$80\%$ horizons: \ doubling every ${d80:.0f}$ days", font_size=22, color=P80)
        k80.next_to(meas, DOWN, buff=0.3).align_to(box, LEFT)
        if ratio > ch * 1.15:
            verdict = (f"METR's measurements give a median of {ratio:.1f}: an agent's success falls off with length more "
                       "gently than a constant risk per minute would make it. Long tasks are not simply many short "
                       "ones; some long tasks are easy, and some short ones hard.")
        elif ratio < ch / 1.15:
            verdict = (f"METR's measurements give a median of only {ratio:.1f}: success falls off with length faster "
                       "than a constant risk per minute.")
        else:
            verdict = f"METR's measurements give a median of {ratio:.1f}, close to it."
        same = abs(d80 - float(m["doubling_2023"])) < 0.25 * float(m["doubling_2023"])
        tail = ("The eighty-percent horizons are much shorter, but they double at nearly the same pace: "
                f"every {d80:.0f} days." if same else f"The eighty-percent horizons double every {d80:.0f} days.")
        with self.voiceover(
            "Half the time is a low bar for work you'd hand over. METR also reports where each model's success "
            "curve crosses eighty percent. <bookmark mark='a'/> Those horizons are far shorter. "
            "<bookmark mark='b'/> If an agent failed with the same small chance in every minute of work, the "
            "compounding of chapter five, the ratio of the two horizons would be fixed: log 2 over log one point two "
            f"five, {ch:.1f}. <bookmark mark='c'/> {verdict} <bookmark mark='d'/> {tail}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(p50))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromPoint(l_, l_.get_start()) for l_ in links], lag_ratio=0.03),
                      LaggedStart(*[FadeIn(d_) for d_ in p80], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(box[0]), Write(box[1]))
            self.play(Write(box[2]))
            vo.wait_until("c")
            self.play(FadeIn(meas))
            vo.wait_until("d")
            self.play(FadeIn(k80))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ceiling(self):
        m = load("metr")
        rows = m["rows"]
        last = max(rows, key=lambda r: r["t"])
        lim = float(m["reliable_min"])
        ruler = NumberLine(x_range=[-2, 12, 1], length=12.0, include_numbers=False, color=GREY_C).move_to([0, 0.4, 0])
        ticks = VGroup()
        for v, t_ in ((-2, r"15\,\text{s}"), (0, r"1\,\text{min}"), (4, r"16\,\text{min}"), (6, r"1\,\text{h}"),
                      (8, r"4\,\text{h}"), (10, r"17\,\text{h}"), (12, r"68\,\text{h}")):
            ticks.add(MathTex(t_, font_size=22, color=GREY_B).next_to(ruler.n2p(v), DOWN, buff=0.15))
        lim_x = math.log2(lim)
        zone = Rectangle(width=ruler.n2p(12)[0] - ruler.n2p(lim_x)[0], height=0.5, stroke_width=0, fill_color=FAIL,
                         fill_opacity=0.2).move_to((ruler.n2p(lim_x) + ruler.n2p(12)) / 2)
        zl = label(r"above $16$ h: \ METR's tasks \\ no longer measure reliably", font_size=20, color=FAIL)
        zl.next_to(zone, UP, buff=0.2)
        marks = VGroup()
        for r in rows:
            if r["sota"] and r["t"] > 6.0:
                x = ruler.n2p(math.log2(r["p50"]))
                marks.add(VGroup(Triangle(color=FRONT, fill_opacity=1).scale(0.09).rotate(PI).move_to(x + UP * 0.25),
                                 label(r["name"], font_size=16, color=FRONT)))
        place = [UP * 0.62, UP * 1.05, UP * 1.48, UP * 0.62, UP * 1.05]
        for k, mk in enumerate(marks):
            mk[1].next_to(mk[0], UP, buff=0.08).shift(place[k % len(place)] - UP * 0.62)
        cards = VGroup(
            history_card(r"Apr 2026", rf"{last['name']}", rf"$50\%$ horizon about ${last['p50'] / 60:.0f}$ hours: \ "
                         r"past what the suite can measure", width=4.2, color=FRONT, font_size=18),
            history_card(r"Sep 2026", r"METR's page", r"Time Horizon 1.1 is no longer actively updated", width=4.2,
                         color=HIST, font_size=18),
            history_card(r"2025", r"benchmarks are not jobs", r"METR's own trial: \ experienced developers were slower "
                         r"with early-2025 AI tools (Part 31)", width=4.2, color=HIST, font_size=18),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The ruler itself is running out. <bookmark mark='a'/> METR says its current tasks cannot reliably "
            "measure horizons above sixteen hours. <bookmark mark='b'/> Its "
            f"last frontier measurement, {last['name']} in April 2026, came out at about "
            f"{last['p50'] / 60:.0f} hours, already past that line, and in September 2026 the page stopped being "
            "updated. <bookmark mark='c'/> And a horizon on a benchmark is not a job: METR's own trial found "
            "experienced developers slower, not faster, with early-2025 tools. Part 31 asks how far such trends can "
            "be trusted. Next, how coding agents in particular are measured."
        ) as vo:
            self.play(Create(ruler), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(zone), FadeIn(zl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(mk, shift=DOWN * 0.1) for mk in marks], lag_ratio=0.2), FadeIn(cards[0]),
                      FadeIn(cards[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.3)
        self.clear_scene()
