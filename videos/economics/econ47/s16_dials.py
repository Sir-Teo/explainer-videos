from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ47.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ corruption, \ incumbency", r"What do the numbers say?",
             "Chapter fourteen. The Dials: the share of spending lost to corruption, and the incumbency advantage.",
             lit={2004: r"Reinikka and Svensson", 2007: r"Olken", 2008: r"Lee"}, scale=("village", "nation"),
             horizon=("a year",))
        self.corruption()
        self.incumbency()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}"):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=0.6, fmt=fmt)
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

    def corruption(self):
        self._show(dials.DIALS["corruption_share"], r"the share of spending lost to corruption \ (new)", 0, 90,
                   [0, 20, 40, 60, 80], r"percent of the money",
                   "The first dial is new: how much of a programme's money is lost, where someone has measured it "
                   "directly rather than asked about it. Olken's Indonesian roads without an audit: 27.7 percent. "
                   "<bookmark mark='a'/> With certain audits: 19.2. <bookmark mark='b'/> Indonesia's subsidized rice: "
                   "at least 18 percent never reached households. <bookmark mark='c'/> Uganda's school grants in the "
                   "mid-1990s: about four-fifths never reached the schools. <bookmark mark='d'/> And the Island's "
                   "roads, planted at 28. <bookmark mark='z'/> The status: depends on the setting. Losses run from "
                   "a fifth to most of the money, depending on the programme and on whether anyone is looking, and "
                   "audits and information cut them.", "abcd", fmt="{:.0f}")

    def incumbency(self):
        self._show(dials.DIALS["incumbency"], r"the incumbency advantage in close elections \ (new)", 0, 12,
                   [0, 3, 6, 9, 12], r"points of the vote at the next election",
                   "The second, also new: what barely winning is worth at the next election. David Lee's House "
                   "elections from 1946 to 1998: about 7.7 points. <bookmark mark='a'/> The Senate data analysed in "
                   "chapter four: 7.41, with an interval from about four and a half to ten. <bookmark mark='z'/> The "
                   "status: contested. In the House, bare winners and bare losers differ before the election, which "
                   "suggests the true advantage is smaller, and in Indian state elections the same design finds "
                   "incumbents at a disadvantage. The number belongs to a place and a time.", "a", fmt="{:.1f}")
