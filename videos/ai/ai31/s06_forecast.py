from __future__ import annotations

from datetime import date

import numpy as np

from explainer import lang
from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import CI, EST, FUTURE, PART, TRUTH, load, tagline

YEAR0 = 2023  # the forecast item measures time in years since 1 January 2023


def ymd(ordinal: float) -> str:
    """A month and year on screen: December 2026, or 2026年12月 in the Chinese edition."""
    d = date.fromordinal(int(ordinal))
    return f"{d.year}年{d.month}月" if lang.LANG == "zh" else d.strftime("%B %Y")


def month_year(ordinal: float) -> tuple[str, int]:
    d = date.fromordinal(int(ordinal))
    return d.strftime("%B"), d.year


class Forecast(VoiceoverScene):
    def construct(self):
        self.card()
        self.loss_law()
        self.horizon_def()
        self.trend()
        self.backtest()
        self.caveats()

    def card(self):
        card = chapter_card(5, r"Forecasting capabilities", r"Can we see what is coming?", lit=(2020, 2022, 2025),
                            part=PART)
        with self.voiceover("Chapter five. Forecasting capabilities."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def loss_law(self):
        d = load("forecast")
        C_, L_ = np.log10(np.asarray(d["chin_C"])), np.asarray(d["chin_L"])
        g = axes([18, 27], [1.6, float(np.ceil(L_.max() * 10) / 10)], x_length=6.4, y_length=3.6,
                 xlabel=r"training compute \ (FLOP)", ylabel=r"predicted loss \ (nats per token)", xticks=[18, 21, 24, 27],
                 yticks=[1.7, 2.0, 2.5], log_x=True, center=[-3.1, -0.3, 0])
        line = curve(g.ax, C_, L_, EST, 4)
        floor = DashedLine(g.ax.c2p(18, 1.69), g.ax.c2p(27, 1.69), color=GREY_B, dash_length=0.08)
        fl = label(r"$E = 1.69$: \ the text's own entropy, \ by the fit", font_size=18, color=GREY_B)
        fl.next_to(floor, UP, buff=0.06).align_to(floor, RIGHT)
        law = cmath(r"L(N, D)", r"=", r"E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}}", font_size=36)
        law.next_to(g, UP, buff=0.3)
        lnote = note(r"Hoffmann et al.\ (2022): \ $A = 406.4$, \ $B = 410.7$, \ $\alpha = 0.34$, \ $\beta = 0.28$; \ "
                     r"here with $D = 20N$", font_size=18).next_to(law, UP, buff=0.12)
        cards = VGroup(
            history_card(2026, r"Epoch AI, \ \textit{Trends in AI} (February)", r"training compute of frontier "
                         r"language models: \ about $5\times$ a year since 2020; \ cost: \ $3.5\times$ a year",
                         width=5.8, color=EST, font_size=20),
            history_card(2022, r"emergence, \ or a mirage?", r"abilities that seem to appear suddenly with scale \ "
                         r"(Wei et al.) \ often look smooth under a continuous metric \ (Schaeffer et al., 2023): "
                         r"\ Part 12", width=5.8, color=FUTURE, font_size=20),
        ).arrange(DOWN, buff=0.3).move_to([3.7, -0.2, 0])
        tag = tagline(r"published law, \ drawn here")
        with self.voiceover(
            "Measurement tells us where models are. Can it tell us where they are going? <bookmark mark='a'/> For "
            "the loss, remarkably well. As Part 12 showed, loss falls as a power law in model size and data. "
            "Hoffmann and colleagues' fitted law, drawn here at the compute-optimal split of Part 12, falls smoothly "
            "toward a floor of about 1.69 nats per token. <bookmark mark='b'/> And compute keeps growing: Epoch AI "
            "estimates that the training compute of frontier language models has grown about five-fold a year since "
            "2020. <bookmark mark='c'/> But a loss is not an ability. Some abilities seem to switch on suddenly with "
            "scale; under a smoother way of scoring, many of those jumps flatten out. To forecast what models can do, "
            "we need a measure of ability that doesn't saturate."
        ) as vo:
            self.play(FadeIn(g), Write(law), FadeIn(lnote), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(line), Create(floor), FadeIn(fl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def horizon_def(self):
        g = axes([0, 9], [0, 1], x_length=6.6, y_length=3.4, xlabel=r"time the task takes a skilled person "
                 r"\ (log scale)", ylabel=r"the model's success rate", xticks=[0, 3, 6, 9], yticks=[0, 0.5, 1],
                 xfmt=lambda v: {0: r"\text{1 s}", 3: r"\text{1 min}", 6: r"\text{1 h}", 9: r"\text{1 day}"}.get(v, ""),
                 center=[-3.1, -0.4, 0])
        x = np.linspace(0, 9, 200)
        h = 5.0
        p = 1 / (1 + np.exp(-1.4 * (h - x)))
        cv = curve(g.ax, x, p, EST, 4)
        rng_ = np.random.default_rng(2)
        tx = rng_.uniform(0.3, 8.7, 36)
        ty = (rng_.random(36) < 1 / (1 + np.exp(-1.4 * (h - tx)))).astype(float)
        dots = VGroup(*[Dot(g.ax.c2p(a, 0.03 + 0.94 * b), radius=0.05, color=TRUTH if b else C.PENALTY, fill_opacity=0.8)
                        for a, b in zip(tx, ty)])
        half = DashedLine(g.ax.c2p(0, 0.5), g.ax.c2p(h, 0.5), color=GREY_B, dash_length=0.06)
        vert = DashedLine(g.ax.c2p(h, 0), g.ax.c2p(h, 0.5), color=CI, dash_length=0.06)
        hl = label(r"the $50\%$ time horizon", font_size=22, color=CI).next_to(g.ax.c2p(h, 0), UP, buff=0.05)
        hl.shift(RIGHT * 1.4 + UP * 0.1)
        rows = [cmath(r"p(t)", r"=", r"\sigma\big(\beta\,(\log_2 h - \log_2 t)\big)", font_size=34),
                cmath(r"p(h)", r"=", r"\sigma(0) = \tfrac12", font_size=34)]
        rows[0][2].set_color(EST)
        whys = [why(r"fitted to the model's successes and failures"), why(r"so $h$ is the task length it does half the time")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=3.6, buff=0.6, edge=6.9)
        hc = history_card(2025, r"METR, \textit{Measuring AI Ability to Complete Long Tasks} \ (Kwa et al.)",
                          r"$170$ software and research tasks, \ each timed by skilled people: \ from seconds to hours",
                          width=6.0, color=CI, font_size=20).move_to([3.6, -1.9, 0])
        sch = note(r"schematic").next_to(g, DOWN, buff=0.12).align_to(g, LEFT)
        with self.voiceover(
            "In 2025 the research group METR proposed one: the length of task a model can complete, measured in "
            "human time. <bookmark mark='a'/> They timed skilled people on a set of software and research tasks, "
            "from a few seconds to many hours. <bookmark mark='b'/> A model succeeds at short tasks and fails at long "
            "ones, and its success rate against the log of the human time is fitted with a logistic curve. "
            "<bookmark mark='c'/> Where the curve crosses one half is the model's fifty-percent time horizon: the "
            "length of task it completes half the time."
        ) as vo:
            self.play(FadeIn(g), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.15), LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.03))
            vo.wait_until("b")
            step(0)
            self.play(Create(cv))
            vo.wait_until("c")
            step(1)
            self.play(Create(half), Create(vert), FadeIn(hl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chart(self, d, x1=4.0):
        """Time horizon (minutes, log scale) against release date, 2019 to 2027."""
        g = axes([-4.0, x1], [-5, 12], x_length=10.2, y_length=5.2, xlabel=r"release date",
                 ylabel=r"$50\%$ time horizon \ (log scale)", xticks=[-4, -2, 0, 2, 4][: 4 + (x1 >= 4)],
                 yticks=[-np.log2(60) + 0, 0, np.log2(60), np.log2(60 * 8), np.log2(60 * 40)],
                 xfmt=lambda v: rf"{int(v + YEAR0)}",
                 yfmt=lambda v: {round(-np.log2(60), 3): r"\text{1 s}", 0.0: r"\text{1 min}",
                                 round(np.log2(60), 3): r"\text{1 h}", round(np.log2(480), 3): r"\text{8 h}",
                                 round(np.log2(2400), 3): r"\text{40 h}"}.get(round(v, 3), ""),
                 center=[0.3, -0.35, 0])
        return g

    def points(self, g, rows, only_before=None, after=None):
        out = VGroup()
        for r in rows:
            if only_before is not None and r["t"] >= only_before:
                continue
            if after is not None and r["t"] < after:
                continue
            x, y = r["t"], np.log2(r["p50"])
            col = EST if r["sota"] else GREY_C
            reliable = r["p50"] <= 16 * 60
            dot = Dot(g.ax.c2p(x, y), radius=0.065 if r["sota"] else 0.045, color=col if reliable else C.PENALTY)
            bar = Line(g.ax.c2p(x, np.log2(r["lo"])), g.ax.c2p(x, np.log2(r["hi"])), color=col, stroke_width=1.5,
                       stroke_opacity=0.6)
            out.add(VGroup(bar, dot))
        return out

    def trend(self):
        d = load("forecast")
        rows = d["rows"]
        g = self.chart(d)
        pts = self.points(g, rows)
        c = np.asarray(d["coef_2023"])
        xs = np.linspace(0, 3.5, 50)
        fit = DashedLine(g.ax.c2p(0, c[0]), g.ax.c2p(3.5, c[0] + c[1] * 3.5), color=CI, dash_length=0.1)
        names = {r["name"]: r for r in rows}
        tags = VGroup()
        for nm, dx, dy in (("GPT-2", 0.0, 0.35), ("GPT-4", -0.1, 0.35), ("o3", -0.25, 0.35),
                           ("Claude Mythos Preview (early)", -1.2, 0.35)):
            r = names[nm]
            tags.add(label(nm.replace(" (early)", ""), font_size=18, color=GREY_A).move_to(
                g.ax.c2p(r["t"], np.log2(r["p50"])) + np.array([dx, dy, 0])))
        dt, (lo, hi), m = d["doubling_2023"], d["doubling_ci"], d["metr"]
        stat = VGroup(label(rf"doubling every ${dt:.0f}$ days \ (our refit, frontier models since 2023)", font_size=22,
                            color=CI),
                      label(rf"bootstrap over models: \ ${lo:.0f}$--${hi:.0f}$; \ METR's fit: \ ${m['from_2023']:.0f}$ "
                            rf"(${m['lo']:.0f}$--${m['hi']:.0f}$)", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.3)
        unrel = label(r"red: \ above $16$ hours, \ where METR's tasks no longer measure reliably", font_size=18,
                      color=C.PENALTY).to_corner(DR, buff=0.25)
        tag = note(r"published: \ METR, Time Horizon 1.1 \ (metr.org); \ the fit is computed here", font_size=18)
        tag.to_corner(DL, buff=0.2)
        agree = abs(dt - m["from_2023"]) < 5
        dall, mfit = d["doubling_all"], m["from_2023"]
        if agree:
            fit_said = "That reproduces METR's own fit."
        else:
            fit_said = f"METR's own fit gives {mfit:.0f} days."
        with self.voiceover(
            "Here are METR's measurements, from their current task suite: every model they tested, by release date, "
            "on a log scale of minutes, each with its uncertainty. <bookmark mark='a'/> GPT-2, in 2019: a few seconds. "
            "GPT-4, in 2023: four minutes. o3, in 2025: two hours. In April 2026 an early version of Anthropic's "
            "Claude Mythos Preview measured about seventeen hours, beyond what the tasks can reliably measure. "
            "<bookmark mark='b'/> On a log scale the frontier is close to a straight line, and a straight line on a "
            "log scale is a doubling time. Fitting the frontier models since 2023, as METR did, gives one doubling "
            f"every {dt:.0f} days, between {lo:.0f} and {hi:.0f} if we resample the models. {fit_said} "
            f"<bookmark mark='c'/> Since 2019 as a whole the doubling time is longer, about {dall:.0f} days: the "
            "trend has sped up."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(unrel))
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.06), run_time=2.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tags], lag_ratio=0.6), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(stat), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def backtest(self):
        d = load("forecast")
        rows = d["rows"]
        g = self.chart(d)
        cut = d["cut"]
        before = self.points(g, rows, only_before=cut)
        after = self.points(g, [r for r in rows if r["sota"]], after=cut)
        cb = np.asarray(d["coef_back"])
        x_end = 3.4
        line = DashedLine(g.ax.c2p(0, cb[0]), g.ax.c2p(x_end, cb[0] + cb[1] * x_end), color=FUTURE, dash_length=0.1)
        cutline = DashedLine(g.ax.c2p(cut, -5), g.ax.c2p(cut, 12), color=GREY_C, dash_length=0.06)
        cl = label(r"pretend it is 1 January 2025", font_size=22, color=GREY_A).next_to(g.ax.c2p(cut, 12), DOWN,
                                                                                       buff=0.1).shift(LEFT * 1.9)
        later = d["later"]
        misses = VGroup(*[Arrow(g.ax.c2p(r["t"], np.log2(r["pred"])), g.ax.c2p(r["t"], np.log2(r["actual"])), buff=0.05,
                                color=C.PENALTY, stroke_width=2.5, max_tip_length_to_length_ratio=0.2) for r in later])
        last = later[-1]
        o3 = next(r for r in later if r["name"] == "o3")
        ratio = last["actual"] / last["pred"]
        under = all(r["actual"] > r["pred"] for r in later)
        tag = note(r"published data; \ fit and forecast computed here", font_size=18).to_corner(DL, buff=0.2)
        o3p, o3a = o3["pred"], o3["actual"]
        lp, la = last["pred"] / 60, last["actual"] / 60
        if under:
            verdict = (f"Every one of them came in above the forecast. o3 was predicted at {o3p:.0f} minutes and "
                       f"measured {o3a:.0f}; fifteen months out, the forecast was too low by a factor of {ratio:.0f}. "
                       "The trend itself had accelerated, which no straight line through the past could know.")
        else:
            verdict = (f"The forecast was mixed: for the last of them it predicted {lp:.1f} hours against {la:.1f} "
                       "measured.")
        with self.voiceover(
            "How good is such a forecast? Test it the honest way, with a backtest. <bookmark mark='a'/> Pretend it is "
            "the first of January 2025, and fit only the frontier models released before then: "
            f"{d['n_back']} of them, doubling every {d['doubling_back']:.0f} days. <bookmark mark='b'/> Extend the "
            "line, and compare with what came next. <bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(FadeIn(g), FadeIn(before), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cutline), FadeIn(cl))
            vo.wait_until("b")
            self.play(Create(line), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in after], lag_ratio=0.2), run_time=2.0)
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in misses], lag_ratio=0.15), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def caveats(self):
        d = load("forecast")
        wk, mo = d["week_date"], d["month_date"]
        ext = VGroup(
            label(r"if the 2023 trend simply continued:", font_size=26, color=FUTURE),
            label(rf"a $40$-hour task: \ around {ymd(wk[1])} \ ($80\%$ of resamples: \ {ymd(wk[0])} to {ymd(wk[2])})",
                  font_size=22, color=GREY_A),
            label(rf"a $167$-hour month: \ around {ymd(mo[1])} \ ({ymd(mo[0])} to {ymd(mo[2])})", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=0.45)
        cards = VGroup(
            history_card(2026, r"the ruler runs out", r"METR: \ horizons above $16$ hours are unreliable with its "
                         r"current tasks", width=4.2, color=C.PENALTY, font_size=19),
            history_card(2025, r"benchmarks are not jobs", r"METR's randomized trial: \ experienced developers were "
                         r"$19\%$ slower with early-2025 AI tools, \ though they believed they were $20\%$ faster",
                         width=4.2, color=EST, font_size=19),
            history_card(2026, r"jagged abilities", r"the International AI Safety Report: \ gold-medal olympiad "
                         r"answers, \ yet failures at some simple tasks", width=4.2, color=FUTURE, font_size=19),
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.0)
        tag = note(r"extrapolation, \ computed from the refit above", font_size=18).to_corner(DL, buff=0.2)
        wm, wy = month_year(wk[1])
        mm, my = month_year(mo[1])
        with self.voiceover(
            "Extrapolate the post-2023 trend anyway, and it says: tasks of a forty-hour working week around "
            f"{wm} of {wy}, and of a month around {mm} of {my}. Read that as arithmetic, not prophecy. "
            "<bookmark mark='a'/> Three reasons for caution. The ruler is running out: above sixteen hours, METR's "
            "tasks no longer measure reliably. <bookmark mark='b'/> Benchmarks are not jobs: in a randomized trial in "
            "2025, METR found experienced open-source developers nineteen percent slower when allowed early-2025 AI "
            "tools, though they believed they had been twenty percent faster. <bookmark mark='c'/> And abilities are "
            "jagged. The 2026 International AI Safety Report notes systems that answer olympiad problems at gold-medal "
            "level and still fail at some simple tasks. Forecasts are worth making, and worth checking, as we just "
            "did."
        ) as vo:
            self.play(FadeIn(ext), FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()
