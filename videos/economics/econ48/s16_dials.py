from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ48.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ carbon, \ energy, \ warming", r"What do the numbers say?",
             "Chapter fourteen. The Dials: the social cost of carbon, the price elasticity of energy, and the effect "
             "of a warmer year.", lit={2008: r"Hughes et al.", 2012: r"Dell et al.", 2024: r"DICE-2023"},
             scale=("nation", "world"), horizon=("a year", "a century"))
        self.carbon()
        self.energy()
        self.warming()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}"):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=0.52, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-21", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip(marks, rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def carbon(self):
        S = load("scc")
        self._show(dials.DIALS["discount"], r"the social cost of carbon \ (new)", 0, 420,
                   [0, 100, 200, 300, 400], r"dollars a tonne of CO$_2$",
                   "The first dial, new to the course: the social cost of carbon, in dollars a tonne, each in its "
                   "own year's dollars. Nordhaus's DICE-2016: 31. <bookmark mark='a'/> DICE-2023: 66. <bookmark "
                   "mark='b'/> The same model at a constant two percent: 176. <bookmark mark='c'/> The Stern Review, "
                   "with near-zero time preference: over 80. <bookmark mark='d'/> Rennert and colleagues: 185, from "
                   "44 to 413. <bookmark mark='e'/> The Environmental Protection Agency: 190. <bookmark mark='f'/> "
                   f"This film's model: {S['ramsey']:.0f}, <bookmark mark='g'/> and {S['by_rate'][2]:.0f} at two "
                   "percent. <bookmark mark='z'/> The status: contested. The spread is mostly the discount rate; at "
                   "matched rates, the models agree more than their headlines do.", "abcdefg", fmt="{:.0f}")

    def energy(self):
        self._show(dials.DIALS["energy_elasticity"], r"the price elasticity of gasoline and electricity \ (new)",
                   -0.4, 0.0, [-0.4, -0.3, -0.2, -0.1, 0.0], r"percent change in quantity per percent change in price",
                   "The second: how much people cut their use of energy when it costs more. Jonathan Hughes, "
                   "Christopher Knittel and Daniel Sperling found American drivers' short-run response to petrol "
                   "prices between minus 0.03 and minus 0.08 from 2001 to 2006, <bookmark mark='a'/> against minus "
                   "0.21 to minus 0.34 in the late 1970s. <bookmark mark='b'/> In the long run, a meta-analysis puts "
                   "it near minus 0.3. <bookmark mark='c'/> For electricity, Tatyana Deryugina, Alexander MacKay and "
                   "Julian Reif found minus 0.09 in the first six months after a price change, <bookmark mark='d'/> "
                   "growing to minus 0.27 two years later. <bookmark mark='z'/> The status: depends on the setting. "
                   "A carbon price works slowly at first and more over the years, as people replace cars, furnaces "
                   "and appliances.", "abcd", fmt="{:.2f}")

    def warming(self):
        P = load("panel")
        self._show(dials.DIALS["warming_output"], r"the effect of a warmer year on growth \ (new)", -2.0, 1.0,
                   [-2, -1, 0, 1], r"percentage points of growth per \textdegree C",
                   "The third: what a year one degree warmer does to a country's growth. Dell, Jones and Olken, for "
                   "poor countries: minus 1.3 points. <bookmark mark='a'/> This film's estimate for a country "
                   f"averaging twenty-five degrees: {100 * P['marg25']:.1f}. <bookmark mark='b'/> The poorer half, "
                   f"by Dell, Jones and Olken's method: {100 * P['djo_poor']:.1f}, with a wide interval. <bookmark "
                   f"mark='c'/> And a cool country, at five degrees: {100 * P['marg5']:+.1f}. <bookmark mark='z'/> "
                   "The status: contested. Hot, poor places lose; cool ones may gain; and whether the losses add up "
                   "over decades is the open question that decides how large climate damage is.", "abc", fmt="{:.2f}")
