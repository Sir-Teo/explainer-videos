from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 12, r"In practice: what economists are paid to do", r"Where is this a job?",
             "Chapter twelve. In practice: what economists are paid to do.", scale=("firm", "nation"),
             horizon=("a year",))
        self.jobs()

    def jobs(self):
        items = [
            (r"the central bank", r"set interest rates; \ watch the banks; \ forecast inflation. \ Parts 25 to 31, 55, "
             r"57", E.BANKS),
            (r"the treasury and the budget office", r"score a tax or a benefit; \ project the debt. \ Parts 32, 41, 42, "
             r"58", E.GOVERNMENT),
            (r"the competition authority", r"decide whether a merger raises prices; \ catch cartels. \ Parts 10, 12, "
             r"43, 44, 59", E.SUPPLY),
            (r"the technology platform", r"design auctions, rankings and prices; \ run experiments. \ Parts 16, 17, "
             r"60, 61, 64", E.DEMAND),
            (r"development and evaluation", r"test what helps the poor, \ and what it costs. \ Parts 4, 46, 58",
             E.GAIN),
            (r"the firm", r"set prices; \ design pay; \ decide what to make and what to buy. \ Parts 8, 14, 60, 62",
             E.FIRMS),
        ]
        pc = point_cards(items, width=12.8, cols=3, font_size=22).move_to(DOWN * 0.35)
        head = heading(r"Where economists work")
        foot = label(r"every part ends with a chapter like this one", font_size=22, color=GREY_B).to_edge(DOWN,
                                                                                                        buff=0.35)
        with self.voiceover(
            "Economics is also a job, and every part of this series ends with a chapter about where its ideas are "
            "used. Here is the map for the whole course. <bookmark mark='a'/> At a central bank, economists set "
            "interest rates, watch over the banks, and forecast inflation. <bookmark mark='b'/> At a treasury or a "
            "budget office, they work out what a tax would raise, who would pay it, and what the debt will look "
            "like in twenty years. <bookmark mark='c'/> At a competition authority, they decide whether a merger "
            "would raise prices, and catch cartels. <bookmark mark='d'/> At a technology platform, they design "
            "auctions for advertising, the ranking of a search, the price of a ride, and they run thousands of "
            "experiments. <bookmark mark='e'/> In development, they test what actually helps the poorest people "
            "in the world, and what it costs. <bookmark mark='f'/> And inside ordinary firms, they set prices, "
            "design pay, and decide what to make and what to buy. Each of these has its own parts in the course."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c in zip("abcdef", pc.cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=UP * 0.1))
            self.play(FadeIn(foot))
        self.clear_scene()
