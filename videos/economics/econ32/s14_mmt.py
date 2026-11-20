from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class MMT(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Modern monetary theory", r"What does it claim, \ and where does the mainstream agree?",
             "Chapter twelve. Modern monetary theory.", lit={2020: r"Kelton; \ Mankiw"}, scale=("nation",),
             horizon=("a year", "decades"))
        self.claims()

    def claims(self):
        cols = VGroup(
            VGroup(label(r"what it claims", font_size=24, color=E.ACCENT),
                   label(r"a government that borrows in a currency \\ it issues cannot be forced to default",
                         font_size=19,
                         color=DEBT),
                   label(r"its limit is inflation, \ not the deficit", font_size=19, color=INFL),
                   label(r"taxes, \ not interest rates, \\ should be the brake on inflation", font_size=19, color=TAX),
                   label(r"a public job guarantee \\ to hold employment full", font_size=19, color=OUTPUT)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.3),
            VGroup(label(r"where the mainstream agrees", font_size=24, color=OUTPUT),
                   label(r"no forced default in your own currency \\ (Part 31: Britain against Spain)", font_size=19,
                         color=GREY_A),
                   label(r"with r below g, \ some deficits \\ need never be repaid", font_size=19, color=GREY_A),
                   label(r"at the zero bound, \\ the budget does the work", font_size=19, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.3),
            VGroup(label(r"where it does not", font_size=24, color=INFL),
                   label(r"money-financed deficits become \\ inflation when the economy is full \\ (Part 25)",
                         font_size=19, color=GREY_A),
                   label(r"taxes are a slow, \ political brake; \\ central banks exist because of that", font_size=19,
                         color=GREY_A),
                   label(r"the fiscal theory: \ if surpluses \\ never come, \ prices adjust", font_size=19,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3),
        ).arrange(RIGHT, buff=0.55, aligned_edge=UP).move_to(DOWN * 0.1)
        if cols.width > 13.4:
            cols.width = 13.4
        tag = published_tag(r"Kelton, \ \emph{The Deficit Myth} (2020); \ Mankiw, \ \emph{AEA Papers and "
                            r"Proceedings} 110 (2020)", corner=DR, font_size=12)
        with self.voiceover(
            "Modern monetary theory became famous after 2019. <bookmark mark='a'/> Its claims, in Stephanie "
            "Kelton's book The Deficit Myth: a government that borrows in a currency it issues cannot be forced to "
            "default; its real limit is inflation, not the size of the deficit; taxes, rather than interest rates, "
            "should be the brake when inflation rises; and a public job guarantee should keep employment full. "
            "<bookmark mark='b'/> Much of the first part the mainstream accepts: Part 31 showed why Britain could "
            "not be forced into default and Spain could. With r below g, some deficits need never be repaid, and at "
            "the zero bound the budget has to do the work. <bookmark mark='c'/> Where it parts company, as critics "
            "such as "
            "Gregory Mankiw have argued: deficits paid for with new money become inflation once the economy is "
            "fully employed, as Part 25 showed; raising taxes in time is slow and political, which is why "
            "countries gave the brake to independent central banks; and the fiscal theory says that if surpluses "
            "are never expected, the price level does the adjusting."
        ) as vo:
            self.play(FadeIn(cols[0][0]), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in cols[0][1:]], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(cols[1][0]), LaggedStart(*[FadeIn(r_) for r_ in cols[1][1:]], lag_ratio=0.5),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(cols[2][0]), LaggedStart(*[FadeIn(r_) for r_ in cols[2][1:]], lag_ratio=0.5),
                      run_time=3)
        self.clear_scene()
