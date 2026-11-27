from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 13, "Called it?", "When Boeing names a date for a new airliner, how often is it right?",
             "Chapter thirteen. Called it? When Boeing names a date for a new airliner's first delivery, what happens?",
             lit=("change",))
        self.slips()
        self.ours()

    def _line(self, y, target, actual, label, now=False):
        pa = viz.plot_axes([2003, 2029], [0, 1], x_length=11.0, y_length=0.6, xticks=[2005, 2010, 2015, 2020, 2025],
                           xfmt=lambda v: f"{int(v)}", grid=False, size=13).move_to([0.2, y, 0])
        ax = pa.ax
        nm = tx(label, 20, BOEING, bold=True).next_to(pa, UP, buff=0.12).align_to(pa, LEFT)
        t = marker(ax, target, 0.5, f"promised: {target}", PRICE, side=UP)
        a = marker(ax, actual, 0.5, (f"now expected: {actual}" if now else f"delivered: {actual}"), BAD, side=UP)
        arr = Arrow(ax.c2p(target, 0.3), ax.c2p(actual, 0.3), buff=0.08, stroke_width=4, color=BAD)
        slip = tx(f"+{actual - target} years", 18, BAD, bold=True).next_to(arr, UP, buff=0.5)
        return VGroup(pa, nm), t, VGroup(a, arr, slip)

    def slips(self):
        C = R["called"]
        b787, t787, s787 = self._line(1.3, *C["t787"], "the 787 Dreamliner")
        b777, t777, s777 = self._line(-1.4, *C["t777x"], "the 777X", now=True)
        src = source("The Boeing Company, Forms 10-K 2005, 2011 and 2013; Form 10-Q for the third quarter of 2026", size=12)
        beat(self,
             "Here are Boeing's own forecasts, from its annual reports. <bookmark mark='a'/> In its report for 2005, "
             f"Boeing said the 787's entry into service was targeted for {C['t787'][0]}. <bookmark mark='b'/> The first "
             f"787 was delivered in September {C['t787'][1]}: three years late. <bookmark mark='c'/> In its report for "
             f"2013, Boeing said the first 777X was expected in {C['t777x'][0]}. <bookmark mark='d'/> Its latest report "
             f"expects the first one in {C['t777x'][1]}: seven years late, if it holds. New airliners are late as a rule, "
             "because certification finds problems that only flight testing can find, and every one must be fixed "
             "before the first delivery.",
             base=[b787, b777, src], steps=[t787, s787, t777, s777])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, PRICE, bold=True),
                       tx("Boeing delivers its first 777-9 to a customer by 31 December 2027.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, 1.7, 0])
        why = bullets([f"against: the last two new models slipped {C['slips'][0]} and {C['slips'][1]} years",
                       "against: an engine durability fix still has to be certified",
                       "for: the date is a year away, and Boeing expects the last phases of flight testing approved by "
                       "the end of 2026"], size=19).move_to([0, -0.4, 0])
        rule = tx("scored on Boeing's 10-K for 2027, due February 2028", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             "Now ours. <bookmark mark='a'/> We say Boeing will deliver its first 777-9 to a customer by the end of 2027, "
             f"as it expects, and we give it {100 * C['prob']:.0f} per cent. <bookmark mark='b'/> Against it: Boeing's last "
             "two new models slipped by three and seven years, and the engine fix still needs certifying. For it: the "
             "date is only a year away, and Boeing expects approval of the final flight-test phases by the end of 2026. "
             "Slightly better than a coin toss. <bookmark mark='c'/> Boeing's annual report for 2027 will settle it.",
             base=[tag], steps=[claim, why, rule])
