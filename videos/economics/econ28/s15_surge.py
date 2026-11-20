from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Surge(VoiceoverScene):
    def construct(self):
        card(self, 13, r"2021--23: \ the surge", r"Supply, \ demand, \ or a curve that bends?", "Chapter thirteen. "
             "2021 to 2023: the surge.", lit={2023: r"Bernanke and Blanchard; \ Benigno and Eggertsson"},
             scale=("nation",), horizon=("a year",))
        self.inflation()
        self.bend()
        self.accounts()
        self.called()

    def inflation(self):
        S = load("surge")
        ax = plane([2019, 2026.9], [-1, 10], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[2019, 2021, 2023, 2025], yticks=[0, 2, 4, 6, 8, 10], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        two = seg(ax, 2019, 2, 2026.9, 2, color=GREY_D, width=2, dashed=True)
        hd = path(ax, S["t"], S["headline"], color=INFL, width=3, smooth=False)
        co = path(ax, S["t"], S["core"], color=WAGE, width=3, smooth=False)
        be = path(ax, S["be_t"], S["be"], color=EXPECT, width=3, smooth=False)
        side = VGroup(
            label(rf"headline CPI: \ {S['peak_head']:.1f}\% \\ in mid-{S['peak_head_date'][:4]}", font_size=20,
                  color=INFL),
            label(rf"core: \ {S['peak_core']:.1f}\% at its peak", font_size=20, color=WAGE),
            label(rf"markets' 5-year expectation: \\ never above {S['be_max']:.1f}\%", font_size=20, color=EXPECT),
            label(r"the anchor held", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BLS: \ CPI and core CPI, \ 12 months; \ the 5-year breakeven rate; \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Then, in 2021, the curve woke up. <bookmark mark='a'/> American consumer prices rose "
            f"{S['peak_head']:.0f} percent in the year to June 2022, the fastest in forty years. "
            f"<bookmark mark='b'/> Core inflation, without food and energy, peaked at {S['peak_core']:.1f}. "
            "<bookmark mark='c'/> But the inflation expected over five years, read from the bond market, never went "
            f"above {S['be_max']:.1f} percent. <bookmark mark='d'/> The anchor held, and inflation came down without "
            "a recession."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(two), Create(hd), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(co), FadeIn(side[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(be), FadeIn(side[2]), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def bend(self):
        S = load("surge")
        vu, core, t = np.array(S["vu"]), np.array(S["vu_core"]), np.array(S["vu_t"])
        ax = plane([0, 2.2], [0, 7], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.4, y_length=4.8,
                   xticks=[0, 0.5, 1, 1.5, 2], yticks=[0, 2, 4, 6], xlabel=r"job openings per unemployed person",
                   ylabel=r"core inflation, \ 12 months, \ \%", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0f}",
                   font_size=15)
        before = VGroup(*[dot(ax, x, y, color=CB, r=0.04) for x, y, tt in zip(vu, core, t) if tt < 2021])
        after = VGroup(*[dot(ax, x, y, color=INFL, r=0.05) for x, y, tt in zip(vu, core, t) if tt >= 2021])
        one = seg(ax, 1, 0, 1, 7, color=GREY_B, width=2, dashed=True)
        side = VGroup(
            label(r"2001--2020: \ flat", font_size=21, color=CB),
            label(rf"2021--: \ openings per unemployed \\ up to {S['vu_peak']:.1f} in {S['vu_peak_date'][:4]}, "
                  r"\\ and inflation with them", font_size=20, color=INFL),
            label(r"Benigno and Eggertsson, \ 2023: \\ the curve bends \\ once openings exceed the unemployed",
                  font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BLS: \ JOLTS openings, \ unemployment, \ core CPI; \ monthly, \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Was the flat curve wrong after all? Measure slack differently: job openings for every unemployed "
            "person. <bookmark mark='a'/> From 2001 to 2020, in blue, core inflation sat near two percent whatever "
            "the ratio. <bookmark mark='b'/> In 2021 and 2022, in red, openings rose to about "
            f"{S['vu_peak']:.0f} for every unemployed person, and inflation rose with them. "
            "<bookmark mark='c'/> Pierpaolo Benigno and Gauti Eggertsson argued in 2023 that the curve is not a line "
            "but a hockey stick: flat while there are more unemployed than openings, steep once openings outnumber "
            "the unemployed and employers compete for workers."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(one), run_time=0.8)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in before], lag_ratio=0.005), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in after], lag_ratio=0.02), FadeIn(side[1]),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def accounts(self):
        cards = point_cards([
            (r"supply", r"Bernanke and Blanchard (2023): \\ energy, \ food and shortages \\ did most of it at first",
             WAGE),
            (r"demand", r"stimulus and savings \\ met an economy \\ that could not keep up", INFL),
            (r"a bent curve", r"Benigno and Eggertsson: \\ tight labour markets \\ make the curve steep", EXPECT),
            (r"what they agree on", r"the anchor held; \\ the labour market's effect \\ came later and lasted",
             OUTPUT),
        ], width=12.6, cols=2, font_size=22).move_to(DOWN * 0.1)
        head = label(r"three accounts, \ each at its best", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Bernanke and Blanchard, \ NBER WP 31417 (2023); \ Benigno and Eggertsson, \ NBER WP "
                            r"31197 (2023)", corner=DR, font_size=12)
        with self.voiceover(
            "Three accounts, each in its strongest form. <bookmark mark='a'/> Supply: Ben Bernanke and Olivier "
            "Blanchard decomposed the surge and found that at first most of it came from jumps in energy and food "
            "prices and from shortages in particular sectors. <bookmark mark='b'/> Demand: stimulus and savings "
            "built up in the pandemic met an economy that could not produce enough to keep up. "
            "<bookmark mark='c'/> A bent curve: the labour market was so tight that the Phillips curve became steep. "
            "<bookmark mark='d'/> They agree on more than they differ. Long-run expectations held. And the "
            "labour market's contribution, small at first, came later and lasted longer than the shocks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["team_transitory"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=19).move_to(UP * 0.1)
        tag = published_tag(r"Federal Reserve, \ press conference, \ 16 June 2021; \ BEA: \ PCE prices, \ via FRED",
                            corner=DR, font_size=12)
        T = load("transitory")
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In June 2021, the Federal Reserve's median projection had inflation, "
            f"by its preferred measure, at {T['projected_2021']} percent that year, falling to "
            f"{T['projected_2022']} percent in 2022, as the bottlenecks of the reopening cleared. Many forecasters "
            "agreed; the view was nicknamed team transitory. <bookmark mark='b'/> The measure rose "
            f"{T['actual_2021']:.1f} percent over 2021 and {T['actual_2022']:.1f} percent over 2022. The Fed began "
            f"raising rates in March 2022, and inflation fell to about {T['actual_2023']:.0f} percent over 2023, "
            "without a recession. <bookmark mark='c'/> Wrong, as a forecast. The longer argument, about whether the "
            "anchor would hold, went the transitory side's way."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
