from __future__ import annotations

import dataclasses

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ46.common import *  # noqa: F403

SCHOOL_ROWS = ("Angrist and Krueger", "Card", "Duflo", "Duflo (published)",
               "this film (the Island's school-building programme)")


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ capital, \ cash, \ schooling", r"What do the numbers say?",
             "Chapter fourteen. The Dials: the return to capital in small firms, the consumption effect of cash, and "
             "the return to schooling.", lit={2008: r"de Mel, McKenzie and Woodruff", 2016: r"Haushofer and Shapiro"},
             scale=("firm", "household"), horizon=("a year",))
        self.capital()
        self.cash()
        self.schooling()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}"):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=0.6, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-20", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip(marks, rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def capital(self):
        self._show(dials.DIALS["return_capital_poor"], r"the return to capital in small firms \ (new)", -2, 35,
                   [0, 10, 20, 30], r"percent a month",
                   "The first dial is new: what a small firm in a poor country earns on one more dollar of capital, "
                   "in percent a month. Suresh de Mel, David McKenzie and Christopher Woodruff gave random grants of "
                   "one or two hundred dollars to Sri Lankan microenterprises, and found real returns of about five "
                   "percent a month, sixty percent a year. <bookmark mark='a'/> In Mexico, McKenzie and Woodruff "
                   "found at least twenty to thirty-three percent a month. <bookmark mark='b'/> But for the Sri Lankan "
                   "firms owned by women, the return was zero on average. <bookmark mark='c'/> The Island's best "
                   "businesses are planted at sixty percent a year, about five percent a month, <bookmark "
                   "mark='d'/> and the rest at well under one. <bookmark mark='z'/> The status: depends on the "
                   "setting. Some small firms earn far more than any lender charges, which is why credit should "
                   "help; the typical borrower's firm does not, which is why microcredit's average effect is small.",
                   "abcd", fmt="{:.1f}")

    def cash(self):
        self._show(dials.DIALS["cash_consumption"], r"the consumption effect of a cash transfer \ (new)", 0, 30,
                   [0, 10, 20, 30], r"percent rise in household consumption",
                   "The second, also new: how much a large cash transfer raises a household's consumption. In "
                   "Haushofer and Shapiro's Kenyan trial, about nine months on, by twenty-two percent. <bookmark "
                   "mark='a'/> In Egger and his coauthors' study, the neighbours who received nothing, but lived "
                   "where many others did, had consumption thirteen percent higher eighteen months on, roughly as "
                   "much as the recipients themselves. <bookmark mark='z'/> The status: depends on the setting, and "
                   "on the horizon. Gains in Haushofer and Shapiro's study had faded three years later, while the "
                   "graduation programme's were still there a year after it ended. A big push into a livelihood "
                   "behaves differently from a transfer that is spent.", "a", fmt="{:.0f}")

    def schooling(self):
        d = dials.DIALS["return_schooling"]
        keep = []
        for e in d.estimates:
            if e.who in SCHOOL_ROWS and e.design == "IV":
                if e.who == "Angrist and Krueger" and "1930-39" not in e.sample:
                    continue
                keep.append(e)
        sub = dataclasses.replace(d, estimates=tuple(keep))
        self._show(sub, r"the return to a year of school \ (rows added)", 0, 0.26, [0, 0.05, 0.1, 0.15, 0.2, 0.25],
                   r"proportional rise in earnings per year of school",
                   "The return to schooling, a dial since Part four, shown by its instrumental estimates. Angrist "
                   "and Krueger's quarter of birth in the United States, <bookmark mark='a'/> Card's college "
                   "distance, <bookmark mark='b'/> and Duflo's Indonesian schools in the version Card compiled. "
                   "<bookmark mark='c'/> This part adds the range from Duflo's published paper, six point eight to "
                   "ten point six percent, <bookmark mark='d'/> and the Island's school-building programme, "
                   "recovering its planted eight percent with some noise. <bookmark mark='z'/> The status: settled "
                   "within a range. In poor countries as in rich ones, a year of school raises earnings by roughly "
                   "six to fifteen percent, though learning, not attendance, is what it pays for.", "abcd",
                   fmt="{:.3f}")
