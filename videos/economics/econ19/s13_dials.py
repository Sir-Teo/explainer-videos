from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ19.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The Dials: \ growth before the escape", r"How fast did living standards grow in the four "
             r"centuries before 1700?", "Chapter eleven. The Dials: growth before the escape.",
             scale=("nation",), lit={2010: r"Clark's wages", 2015: r"Broadberry et al.", 2019: r"days worked"})
        self.dial()
        self.compound()
        self.why()

    def dial(self):
        dial = dials.DIALS["preindustrial_growth"]
        dd = load("dial")
        lo, hi = 0.0, 0.25
        head = status_head(dial, r"English living standards, \ 1300--1700 \ (new)")
        frame, rows = dial_rows(dial, lo, hi, [0, 0.05, 0.10, 0.15, 0.20, 0.25], r"growth, \ \% a year",
                                top=1.9, step=0.85, fmt="{:.3f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 17, GREY_A).to_edge(DOWN, buff=0.22)
        tag = published_tag(r"Broadberry et al.\ (2015); \ Bank of England Millennium dataset v3.1", corner=UR,
                            font_size=12)
        r0, r1, r2 = dial.estimates
        dbl = dd["doubling"]
        with self.voiceover(
            "This part opens a dial: how fast did English living standards grow in the four centuries before 1700? "
            "Three reconstructions, all in the Bank of England's dataset, answer differently. <bookmark mark='a'/> "
            f"Output per head, built up from farms, workshops and services, grew by about {r0.value:.2f} percent a "
            f"year: enough to double in about {dbl['gdppc']:.0f} years. <bookmark mark='b'/> Real wages from daily "
            f"wage rates grew by about {r1.value:.2f} percent: a doubling every thousand years. "
            "<bookmark mark='c'/> Count the extra days people worked each year, as Jane Humphries and Jacob "
            f"Weisdorf did, and earnings grew by about {r2.value:.2f} percent. <bookmark mark='d'/> The status: "
            "contested. The gap is the debate over whether England was already escaping slowly, or stuck until about "
            "1800. The dial returns in part forty-six."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def compound(self):
        dial = dials.DIALS["preindustrial_growth"]
        dd = load("dial")
        ax = plane([1300, 1700], [1.0, 2.3], center=LEFT * 1.7 + DOWN * 0.4, x_length=8.6, y_length=5.0,
                   xticks=[1300, 1400, 1500, 1600, 1700], yticks=[1.0, 1.5, 2.0], xfmt=lambda v: f"{v:.0f}",
                   ylabel=r"living standards, \ 1300 $= 1$", yfmt=lambda v: f"{v:.1f}", font_size=16)
        yrs = np.arange(1300, 1701)
        colors = (GDP, WAGE, E.ACCENT)
        keys = ("gdppc", "real_wage", "earnings_days")
        lines, ends = VGroup(), VGroup()
        for e, k, c in zip(dial.estimates, keys, colors):
            g = dd["computed"][k] / 100
            v = (1 + g) ** (yrs - 1300)
            lines.add(path(ax, yrs, v, color=c, width=4))
            ends.add(label(rf"{e.value:.3f}\% a year: \ $\times${v[-1]:.2f}", font_size=19,
                           color=c).next_to(ax.ax.c2p(1700, v[-1]), RIGHT, buff=0.12))
        rule = VGroup(
            label(r"the rule of 70:", font_size=22, color=GREY_A),
            MathTex(r"t_{\times 2} \approx \frac{70}{\text{growth in \%}}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.5)
        today = label(r"since 1800: \ more than 1\% a year, \ a doubling every sixty years or so", font_size=20,
                      color=GREY_A).to_edge(DOWN, buff=0.3)
        r0, r1, r2 = dial.estimates
        with self.voiceover(
            "Numbers this small are hard to feel, so compound them. <bookmark mark='a'/> A rough rule: anything "
            "growing at g percent a year doubles in about seventy divided by g years. <bookmark mark='b'/> At "
            f"{r1.value:.2f} percent, the day wages' rate, four centuries leave living standards only "
            f"{(1 + r1.value / 100) ** 400:.2f} times as high: a third better off, in sixteen generations. "
            f"<bookmark mark='c'/> Counting the extra days worked, {(1 + r2.value / 100) ** 400:.2f} times. "
            f"<bookmark mark='d'/> Output per head, at {r0.value:.2f} percent, more than doubles. "
            "<bookmark mark='e'/> The disagreement is between a world that barely moved and one that was slowly "
            "getting richer. Either way, it is nothing like the doubling every sixty years or so that began around "
            "1800."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            for mk, i in zip("bcd", (1, 2, 0)):
                vo.wait_until(mk)
                self.play(Create(lines[i]), FadeIn(ends[i]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(today))
        self.clear_scene()

    def why(self):
        rows = VGroup(
            label(r"why the reconstructions disagree", font_size=28, color=E.ACCENT),
            label(r"a day's wage is not a year's income: \ people worked more days as time went on", font_size=22),
            label(r"output per head counts everyone, \ landlords and merchants too, \ not only labourers",
                  font_size=22, color=GDP),
            label(r"price indexes for the 1300s rest on a handful of goods", font_size=22, color=GREY_A),
            label(r"and the endpoints matter: \ 1300 was a Malthusian low, \ 1700 a high", font_size=22,
                  color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "Why such a spread? <bookmark mark='a'/> A day's wage is not a year's income: people worked more days a "
            "year as time went on, so day wages understate the gain. <bookmark mark='b'/> Output per head counts "
            "everyone, landlords and merchants as well as labourers, whose share may have fallen. "
            "<bookmark mark='c'/> The price indexes for the fourteenth century rest on a handful of goods. "
            "<bookmark mark='d'/> And the dates matter: 1300 was a crowded, poor moment, so growth measured from it "
            "looks faster."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
