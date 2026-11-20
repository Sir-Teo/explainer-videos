from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ31.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ what policy does, \ and where neutral is", r"How big is the effect of a "
             r"tightening, \ of a bond purchase, \ and how low is the neutral rate?", "Chapter fourteen. The Dials: "
             "what policy does, and where neutral is.",
             lit={2004: r"Romer and Romer", 2011: r"Gagnon et al.", 2023: r"Holston, \ Laubach and Williams"},
             scale=("nation",), horizon=("a year", "decades"))
        self.shock()
        self.qe()
        self.neutral()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}", step=0.62):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=step, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 12.0, 16, GREY_A).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-20", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip(marks, rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def shock(self):
        dial = dials.DIALS["monetary_shock"]
        self._show(dial, r"a 100-basis-point tightening \ (new)", -5, 0, [-5, -4, -3, -2, -1, 0],
                   r"industrial production at its lowest, \ \%",
                   "The first new dial is the effect of a one-point tightening on output. <bookmark mark='a'/> A "
                   "standard recursive VAR: about minus seven tenths of a percent. <bookmark mark='b'/> The Romers' "
                   "narrative shocks: minus four point three. <bookmark mark='c'/> Coibion's reconciliation: two to "
                   "three. <bookmark mark='d'/> This film's VAR with commodity prices: about minus one and a third. "
                   "<bookmark mark='z'/> The status is contested. Everyone agrees on the sign and the delay; the size "
                   "depends on how the shock is found, and on whether the early 1980s are in the sample.",
                   "abcd", fmt="{:.1f}")

    def qe(self):
        dial = dials.DIALS["qe_yield"]
        self._show(dial, r"asset purchases and long yields \ (new)", -110, 0, [-100, -80, -60, -40, -20, 0],
                   r"basis points, \ for \$1.7 trillion of purchases",
                   "The second: what the first round of purchases did to long-term yields. <bookmark mark='a'/> "
                   "Gagnon and his coauthors: ninety-one basis points off the ten-year yield over the eight "
                   "announcements; <bookmark mark='b'/> fifty to a hundred off the term premium in their event "
                   "studies; <bookmark mark='c'/> thirty-eight to eighty-two by a time-series model of bond supply. "
                   "<bookmark mark='d'/> And this film's count on the same days: ninety-four. <bookmark mark='z'/> "
                   "Contested as well: the methods agree with one another, but the sceptics' point about the days in "
                   "between, and about later rounds having smaller effects, has not gone away.",
                   "abcd", fmt="{:.0f}")

    def neutral(self):
        dial = dials.DIALS["neutral_rate"]
        R = load("rstar")
        self._show(dial, r"the neutral real rate \ (new)", -0.5, 3, [-0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3],
                   r"percent a year, \ real", "The third: the neutral real rate. <bookmark mark='a'/> For the "
                   f"United States, Holston, Laubach and Williams's latest estimate is {R['last']['rstar_us']:.1f} "
                   f"percent; <bookmark mark='b'/> for the euro area, {R['last']['rstar_ea']:.1f}; "
                   f"<bookmark mark='c'/> for Canada, {R['last']['rstar_ca']:.1f}. <bookmark mark='d'/> The Fed's "
                   f"policymakers now put it at about {R['sep_last']:.1f}, <bookmark mark='e'/> down from "
                   f"{R['sep_first']:.1f} when they first published their projections in 2012. "
                   "<bookmark mark='z'/> Contested, and uncertain by a point or more either way, as the Island "
                   "showed: and every rule in Part 30 depends on it.", "abcde", fmt="{:.1f}", step=0.55)
