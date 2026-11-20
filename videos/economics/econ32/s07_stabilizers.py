from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class Stabilizers(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Automatic stabilizers", r"What does the budget do in a recession without anyone deciding "
             r"anything?", "Chapter six. Automatic stabilizers.", lit={2008: r"the rebates", 2020: r"the cheques"},
             scale=("household", "nation"), horizon=("a quarter", "a year"))
        self.series()
        self.cheques()

    def series(self):
        S = load("stabilizers")
        yrs = np.array(S["years"])
        ax = plane([1948, 2026], [-16, 10], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[1950, 1970, 1990, 2010], yticks=[-15, -10, -5, 0, 5, 10], ylabel=r"percent",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        zero = seg(ax, 1948, 0, 2026, 0, GREY_C, 1.5)
        dline = path(ax, yrs, S["deficit"], DEBT, 3.2, smooth=False)
        uline = path(ax, yrs, S["unemp"], INFL, 3.2, smooth=False)
        side = VGroup(
            label(r"purple: \ the federal surplus, \\ \% of GDP \ (below zero: \ deficit)", font_size=18,
                  color=DEBT),
            label(r"red: \ unemployment, \ \%", font_size=18, color=INFL),
            label(rf"each point of unemployment: \\ the balance worsens about {abs(S['slope']):.1f} points",
                  font_size=18, color=E.ACCENT),
            label(rf"2009: \ {S['d2009']:.1f}\%; \ 2020: \ {S['d2020']:.1f}\%", font_size=18, color=DEBT),
            label(r"taxes fall and benefits rise \\ on their own: \ the stabilizers", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"OMB and BLS, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Much of fiscal policy needs no decision at all. <bookmark mark='a'/> Here is the federal budget "
            "balance since 1948, as a share of GDP, <bookmark mark='b'/> and unemployment. They are close to mirror "
            "images. <bookmark mark='c'/> On average, each point of extra unemployment has come with a budget "
            f"balance about {abs(S['slope']):.1f} points worse in the same year. <bookmark mark='d'/> In 2009 the "
            f"deficit reached {abs(S['d2009']):.1f} percent of GDP, in 2020 {abs(S['d2020']):.1f}. Part of each was "
            "decided: stimulus laws. <bookmark mark='e'/> Part happened automatically: income and profit taxes "
            "fall when incomes fall, and unemployment benefits rise. Those automatic stabilizers cushion spending "
            "without waiting for Congress."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(dline), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(uline), FadeIn(side[1]), run_time=2)
            for mk, s_ in zip("cde", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
        self.clear_scene()

    def cheques(self):
        rows = VGroup(
            label(r"and the cheques \ (Part 22)", font_size=27, color=E.ACCENT),
            label(r"2001 and 2008: \ households spent a sizeable share of their rebates within months", font_size=22,
                  color=SPEND),
            label(r"the timing of the payments was random, \ so the comparison is clean", font_size=22,
                  color=GREY_A),
            label(r"so a cheque in a slump stimulates, \ even though people know it will be taxed back", font_size=22,
                  color=OUTPUT),
            label(r"which is evidence against full Ricardian equivalence", font_size=22, color=TAX),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Johnson, \ Parker and Souleles, \ \emph{AER} 96(5) (2006); \ Parker, \ Souleles, \ "
                            r"Johnson and McClelland, \ \emph{AER} 103(6) (2013); \ Part 22", corner=DR, font_size=12)
        with self.voiceover(
            "And then there are the cheques, from Part 22. <bookmark mark='a'/> In 2001 and in 2008, households "
            "spent a sizeable share of their rebates within months of receiving them. <bookmark mark='b'/> The "
            "dates of the payments were set by the last digits of social security numbers, effectively at random, "
            "so households who were paid early can be compared with those paid later. <bookmark mark='c'/> A "
            "cheque in a slump stimulates spending, <bookmark mark='d'/> which is evidence against the full "
            "Ricardian equivalence the next chapters examine."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
