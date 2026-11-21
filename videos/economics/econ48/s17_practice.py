from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ energy, \ carbon and regulation", r"Who uses these ideas, and how?",
             "Chapter fifteen. In practice: energy, carbon and regulation.", lit={1956: r"Hubbert"},
             scale=("firm", "nation"), horizon=("a year", "a decade"))
        self.people()
        self.called()

    def people(self):
        rows = VGroup(
            label(r"energy traders: \ power, \ gas and carbon permits, \ priced hour by hour", font_size=21,
                  color=POWER),
            label(r"regulators and market monitors: \ watching for withholding, \ setting caps and tariffs",
                  font_size=21, color=POLICY),
            label(r"agencies weighing rules: \ the social cost of carbon in every cost-benefit analysis",
                  font_size=21, color=OPT),
            label(r"banks, \ insurers and central banks: \ climate risk to assets and to loans", font_size=21,
                  color=HEAT),
            label(r"fisheries managers and resource firms: \ quotas, \ royalties, \ when to extract", font_size=21,
                  color=FISH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.2)
        head = label(r"the people who use this", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Who uses environmental and energy economics? <bookmark mark='a'/> Traders of power, gas and carbon "
            "permits, in markets that price every hour, as in chapter thirteen. <bookmark mark='b'/> Regulators and "
            "market monitors, who watch for withholding and design the caps and the tariffs. <bookmark mark='c'/> "
            "Government agencies, which put a social cost of carbon into the cost-benefit analysis of rules on "
            "cars, power plants and buildings, and whose answers turn on the discount rate. <bookmark mark='d'/> "
            "Banks, insurers and central banks, assessing how climate change and climate policy could hit the value "
            "of assets and the loans against them. <bookmark mark='e'/> And fisheries managers and resource firms, "
            "setting quotas and royalties and deciding when to extract, Hotelling's question in practice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["hubbert_1956"]
        O = load("oil")
        T = tables.HUBBERT_1956.data
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=18)
        cc.move_to(UP * 1.5)
        y, v = np.array(O["year"]), np.array(O["us"]) / 1000
        ax = plane([1900, 2026], [0, 11], center=DOWN * 2.0 + LEFT * 0.8, x_length=7.6, y_length=2.6,
                   xticks=[1900, 1925, 1950, 1975, 2000, 2025], yticks=[0, 5, 10], xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda x: f"{x:.0f}", font_size=12)
        yl = label(r"US oil output, \ thousand TWh", font_size=13, color=GREY_A).next_to(ax, UP, buff=0.05).align_to(
            ax, LEFT)
        cuts = (1956, T["peak"], T["low"], int(y[-1]))
        parts = [path(ax, y[(y >= a) & (y <= b)], v[(y >= a) & (y <= b)], OIL, 2.8, smooth=False)
                 for a, b in zip((int(y[0]),) + cuts[:-1], cuts)]
        pk = vline(ax, T["peak"], 0, 11, GREY_B)
        seen = label(r"what Hubbert \\ could see", font_size=12, color=GREY_A).next_to(
            ax.ax.c2p(1950, float(np.interp(1956, y, v))), UP, buff=0.25)
        lo = dot(ax, O["low_year"], O["low"] / 1000, OIL, 0.06)
        lo_l = label(rf"{O['low_year']}", font_size=12, color=OIL).next_to(lo, DOWN, buff=0.08)
        ps = dot(ax, O["passed"], float(np.interp(O["passed"], y, v)), WHITE, 0.06)
        ps_l = label(rf"{O['passed']}", font_size=12, color=WHITE).next_to(ps, LEFT, buff=0.08)
        window = shade(ax, [(T["most_likely"], T["upper"])], 0, 11, color=RECESS, opacity=0.7)
        cap = label(rf"grey: \ Hubbert's window, \\ {T['most_likely']}--{T['upper']}; \\ the series counts \\ natural "
                    rf"gas liquids, \\ so passes 1970 in {O['passed']}", font_size=13, color=GREY_A).next_to(
            ax, RIGHT, buff=0.35)
        tag = data_tag(r"Energy Institute, \ Statistical Review (2026), \ via Our World in Data", corner=DL,
                       font_size=11)
        with self.voiceover(
            "Called it? A forecast about a resource running out. <bookmark mark='a'/> In March 1956 the geophysicist "
            "M. King Hubbert, then at Shell, fitted a bell-shaped curve to the oil found and produced in the United "
            f"States and predicted that production would peak between {T['most_likely']}, his likeliest year, and "
            f"{T['upper']}, then decline. <bookmark mark='a2'/> The record, from the Energy Institute: <bookmark "
            f"mark='b'/> production peaked in {T['peak']} <bookmark mark='b2'/> and fell for 38 years, to its low in "
            f"{T['low']}. For half a century Hubbert looked like a prophet. <bookmark mark='b3'/> Then horizontal "
            f"drilling and fracturing opened the shale, and in {T['passed']} American crude output passed its 1970 "
            "peak; this series, which also counts natural gas liquids, passed it in "
            f"{O['passed']}. <bookmark mark='c'/> The verdict: partly right. Right about "
            "the peak and the decline of the oil that could be got with the technology of his day; wrong that it "
            "was the end, for the reason Simon gave in the hook: prices high enough call forth new technology."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(yl), run_time=1.0)
            self.play(Create(parts[0]), FadeIn(seen), run_time=2.5)
            self.play(FadeIn(window), FadeIn(cap), run_time=1.0)
            vo.wait_until("a2")
            self.play(Indicate(window, color=WHITE, scale_factor=1.0), FadeOut(seen))
            vo.wait_until("b")
            self.play(Create(parts[1]), run_time=1.2)
            self.play(Create(pk), run_time=0.6)
            vo.wait_until("b2")
            self.play(Create(parts[2]), run_time=3.0)
            self.play(FadeIn(lo), FadeIn(lo_l))
            vo.wait_until("b3")
            self.play(Create(parts[3]), run_time=2.5)
            self.play(FadeIn(ps), FadeIn(ps_l), FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
