from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ12.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ how much do cartels overcharge?", r"Across the cartels that have been caught, "
             r"how far above the competitive price did they push prices?", "Chapter fourteen. The Dials: how much do "
             "cartels overcharge?", scale=("firm", "market", "nation"), lit={1987: r"the sentencing guidelines"})
        self.guideline()
        self.dial()

    def guideline(self):
        q = quote_card(r"It is estimated that the average gain from price-fixing is 10 percent of the selling price.",
                       r"U.S. Sentencing Guidelines, \ \S 2R1.1, \ commentary", width=11.4, font_size=28
                       ).to_edge(UP, buff=0.55)
        rows = VGroup(
            label(r"so an American cartel's base fine is set from 20\% of the commerce it affected: \\ buyers who "
                  r"stopped buying are hurt too", font_size=23),
            label(r"a fine deters only if it exceeds the gain, \ times the chance of being caught", font_size=23,
                  color=LEADER),
            label(r"so the size of the typical overcharge is a policy number: \ is 10\% right?", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.35).next_to(q, DOWN, buff=0.55)
        tag = published_tag(r"U.S. Sentencing Commission, Guidelines Manual, \S 2R1.1, application note", corner=DR,
                            font_size=13)
        with self.voiceover(
            "How large are overcharges in general? It matters, because the law builds a number into its penalties. "
            "The American sentencing guidelines say: it is estimated that the average gain from price-fixing is "
            "ten percent of the selling price. <bookmark mark='a'/> So a cartel's base fine is set from twenty "
            "percent of the commerce it affected, because the harm also falls on buyers who stopped buying. "
            "<bookmark mark='b'/> And a fine deters only if it exceeds the gain from the cartel, multiplied by the "
            "chance of being caught, which is why the leniency programme's prisoner's dilemma matters. "
            "<bookmark mark='c'/> So the typical overcharge is a policy number. Is ten percent right?"
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.1), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def dial(self):
        dial = dials.DIALS["cartel_overcharge"]
        head = status_head(dial, r"cartel overcharges \ (new)")
        frame, rows = dial_rows(dial, 0.0, 40.0, [0, 10, 20, 30, 40], r"overcharge, \ percent of the competitive "
                                r"price", top=1.9, step=0.8, fmt="{:.0f}")
        ten = DashedLine([-0.2 + 6.5 * 10 / 40, 2.35, 0], [-0.2 + 6.5 * 10 / 40, 1.9 - 0.8 * 2 - 0.45, 0],
                         color=E.MISS, stroke_width=2)
        tl = label(r"the guideline's 10\%", font_size=16, color=E.MISS).next_to(ten, UP, buff=0.05)
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 18, GREY_A).to_edge(DOWN, buff=0.2)
        extra = label(r"every estimate sits above the guideline's 10\%; \ how far above is the dispute", font_size=22,
                      color=E.ACCENT).next_to(meaning, UP, buff=0.25)
        tag = published_tag(r"Connor (1998, 2014); \ Boyer and Kotchoni, RIO 47(2) (2015)", corner=UR, font_size=12)
        with self.voiceover(
            "This part opens a dial for cartel overcharges. <bookmark mark='a'/> John Connor has collected the "
            "published estimates for hundreds of cartels; in his 2014 survey the median long-run overcharge is "
            "twenty-three percent, and the mean at least forty-nine. Marcel Boyer and Rachidi Kotchoni re-estimated "
            "the same database in 2015, correcting for how the estimates were made and which got published, and "
            "found a median of about sixteen percent. The lysine cartel's twelve to twenty-eight percent sits "
            "among them. <bookmark mark='b'/> Every estimate is above the guideline's ten percent; how far above "
            "is the dispute. <bookmark mark='c'/> So the dial is contested. At the low end, fines of a few times "
            "the overcharge deter; at the high end, they must be larger. And the cartels on the dial are the ones "
            "that were caught, which may not be typical of the ones that were not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), Create(ten), FadeIn(tl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.6), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(extra))
            vo.wait_until("c")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
