from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ52.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ the propensity to spend", r"Which model spends a windfall like real people?",
             "Chapter thirteen. The Dials: the propensity to spend.",
             lit={2006: r"Johnson, Parker, Souleles", 2021: r"Fagereng, Holm, Natvik"}, scale=("household",),
             horizon=("a year",))
        self.dial()
        self.models()

    def dial(self):
        d = dials.DIALS["mpc_windfall"]
        head = status_head(d, r"the propensity to spend a windfall")
        frame, rows = dial_rows(d, -2, 55, [0, 10, 20, 30, 40, 50], r"percent of a one-off payment spent soon "
                                                                   r"after it arrives", top=2.2, step=0.55,
                                fmt="{:.0f}")
        meaning = wrapped_label(tex_safe(d.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-20", corner=UR, font_size=12)
        with self.voiceover(
            "The Dial for this part is the one every model in it turns on: how much of a windfall households "
            "spend. It was set in Part twenty-two. <bookmark mark='a'/> The 2001 tax rebates, mailed in an order "
            "set by the last digits of Social Security numbers: about thirty percent spent on nondurables within "
            "the quarter. <bookmark mark='b'/> The 2008 stimulus payments, about twenty percent, and more counting "
            "cars. <bookmark mark='c'/> The 2020 payments, about ten percent, when many households already had cash. "
            "<bookmark mark='d'/> Alaska's oil dividend, about a quarter; <bookmark mark='e'/> Italian households "
            "asked directly, about half; <bookmark mark='f'/> and Part twenty-two's own households. <bookmark "
            "mark='z'/> In Norway, Andreas Fagereng, Martin Holm and Gisle Natvik found that lottery winners with "
            "little liquid wealth spent small prizes entirely within the year. The status: it depends on the "
            "setting, and most of all on liquidity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.02))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r), run_time=0.6)
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def models(self):
        D = load("dials")
        ms = D["models"]
        ax = plane([0, 55], [0, len(ms)], center=RIGHT * 1.4 + DOWN * 0.3, x_length=6.6, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40, 50], yticks=[], xlabel=r"percent of a windfall spent within the quarter",
                   xfmt=lambda v: f"{v:.0f}", font_size=14)
        band_ = Rectangle(width=ax.ax.c2p(40, 0)[0] - ax.ax.c2p(10, 0)[0], height=4.6, stroke_width=0,
                          fill_color=DATA, fill_opacity=0.13).move_to((ax.ax.c2p(10, 0) + ax.ax.c2p(40, len(ms))) / 2)
        blab = label(r"the evidence", font_size=16, color=DATA).next_to(band_, UP, buff=0.08)
        names = [r"one representative household"] + [
            rf"liquid wealth: \ {m['liquid']:g} quarter" + ("" if m["liquid"] == 1 else "s") for m in ms[1:]]
        cols = [REP, POOR, POOR, MANY, RICH, RICH]
        bars = VGroup()
        for i, (m, nm, col) in enumerate(zip(ms, names, cols)):
            y = len(ms) - 1 - i + 0.5
            p0, p1 = ax.ax.c2p(0, y - 0.3), ax.ax.c2p(m["mpc"], y + 0.3)
            b = Rectangle(width=max(p1[0] - p0[0], 0.03), height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            v = label(f"{m['mpc']:.1f}", font_size=15, color=WHITE).next_to(b, RIGHT, buff=0.08)
            n_ = label(nm, font_size=16, color=col).next_to(ax.ax.c2p(0, y), LEFT, buff=0.15)
            bars.add(VGroup(b, v, n_))
        head = label(r"each model's households, \ a windfall of 1\% of a quarter's income", font_size=21,
                     color=WHITE).to_edge(UP, buff=0.5)
        foot = label(r"the representative household misses by a factor of twenty or more; \ liquidity sets the "
                     r"answer", font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now ask each model the same question. <bookmark mark='a'/> The representative household spends the "
            f"interest on a windfall and saves the rest: {ms[0]['mpc']:.1f} percent in a quarter, far outside the "
            "evidence. <bookmark mark='b'/> The households of this part, with liquid wealth from one to sixteen "
            f"quarters of income: from {ms[1]['mpc']:.0f} percent down to {ms[-1]['mpc']:.1f}. <bookmark "
            "mark='c'/> Only the economies with little liquid wealth land in the range of the evidence. The "
            "representative household misses by a factor of twenty or more, and that is why the models of the "
            "last three chapters give different answers about monetary and fiscal policy. The amount of wealth "
            "matters less than whether it can be spent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(band_), FadeIn(blab))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
