from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ reserves and currencies", r"Who does this for a living?",
             "Chapter fourteen. In practice: reserves and currencies.", lit={1983: r"Meese and Rogoff"},
             scale=("market", "world"), horizon=("a day", "a year"))
        self.jobs()
        self.called()

    def jobs(self):
        rows = VGroup(
            label(r"the people who do this", font_size=27, color=E.ACCENT),
            label(r"reserve managers: \ central banks' foreign currency, \ trillions of dollars, \ safe and liquid",
                  font_size=21, color=RES),
            label(r"currency strategists: \ at banks and funds, \ forecasts that mostly know they cannot beat the "
                  r"random walk", font_size=21, color=GBP),
            label(r"corporate treasurers: \ hedging what a firm will earn and owe abroad", font_size=21, color=DEM),
            label(r"the IMF's country desks: \ balance-of-payments needs, \ reserve adequacy, \ programmes",
                  font_size=21, color=USD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"IMF, \ \emph{Guidelines for Foreign Exchange Reserve Management}", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> Central banks' reserve managers invest trillions of "
            "dollars of foreign currency, chosen to be safe and easy to sell in a crisis, the lesson of 1992 and "
            "1997. <bookmark mark='b'/> Currency strategists at banks and funds forecast exchange rates, and the "
            "honest ones know chapter five. <bookmark mark='c'/> Corporate treasurers hedge what their firms will "
            "earn and owe abroad, which needs covered parity, not forecasts. <bookmark mark='d'/> And economists on "
            "the IMF's country desks judge what reserves a country needs and design programmes when it runs out."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["meese_rogoff_1983"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=18).move_to(UP * 0.3)
        tag = published_tag(r"Meese and Rogoff, \ \emph{JIE} 14 (1983); \ Rossi, \ \emph{JEL} 51(4) (2013)", corner=DR,
                            font_size=12)
        foot = label(r"a negative result that has lasted: \ the market already prices what the models know",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1983 Richard Meese and Kenneth Rogoff said the exchange-rate models "
            "of the 1970s could not beat a random walk at horizons of one to twelve months, even when handed the "
            "true future values of their fundamentals. <bookmark mark='b'/> Forty years later, chapter five's rerun "
            "finds the same, and Barbara Rossi's survey of the literature finds that some models win at some times, "
            "but not reliably. <bookmark mark='c'/> The verdict: right. <bookmark mark='d'/> It is the rare "
            "negative result that has lasted, and it has a reason: whatever the models know about the future, "
            "the market already knows, and has already put in the price."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
