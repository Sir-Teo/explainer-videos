from __future__ import annotations

from videos.industry.industry1.common import *  # noqa: F403


class Guess(VoiceoverScene):
    def construct(self):
        card(self, 1, "Guess the split", "Where do you think 1,099 dollars goes?",
             "Chapter one. Guess the split.", lit=("dollar",))
        self.phone_and_piles()

    def phone_and_piles(self):
        ph = viz.phone(4.0, back=True, body=BODY_17).shift(LEFT * 4.7 + DOWN * 0.05)
        tag = price_tag(money(R["dollar17"]["price"]), 38).next_to(ph, UP, buff=0.3)
        spec = VGroup(T("iPhone 17 Pro, 256GB", 24, I.TEXT), T("US list price, September 2025", 20, I.DIM),
                      T("before sales tax", 20, I.DIM)).arrange(DOWN, buff=0.06).next_to(ph, DOWN, buff=0.22)
        piles = [("The shop or the carrier", I.CHANNEL), ("All the parts", COL["parts"]),
                 ("The factory that assembles it", I.ASSEMBLY), ("Apple: research, design, selling", I.BRAND),
                 ("Apple's profit, after tax", I.PROFIT)]
        rows = VGroup()
        for name, c in piles:
            box = RoundedRectangle(corner_radius=0.1, width=1.7, height=0.62, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.08)
            q = TB("$ ?", 26, c).move_to(box)
            rows.add(VGroup(VGroup(box, q), T(name, 26, I.TEXT)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.34).shift(RIGHT * 1.6 + UP * 0.2)
        total = VGroup(Line(LEFT * 0.9, RIGHT * 0.9, color=I.DIM), TB("= $1,099", 28, I.MONEY)).arrange(
            DOWN, buff=0.12).next_to(rows[-1][0], DOWN, buff=0.3)
        pause = T("Pause and write down five numbers", 24, I.ACCENT).next_to(total, RIGHT, buff=0.6)
        src = source("Apple list price as reported by MacRumors, 2026-09-09", corner=DR)
        with self.voiceover(
            "Here is a phone: Apple's iPhone 17 Pro, with 256 gigabytes of storage, <bookmark mark='a'/> as it went "
            "on sale in America in September 2025 for 1,099 dollars, before sales tax. Before we take it apart, make "
            "a guess. <bookmark mark='b'/> Split the 1,099 dollars into five piles. What the shop or the carrier "
            "keeps. <bookmark mark='c'/> What all the parts cost. <bookmark mark='d'/> What the factory that puts it "
            "together is paid. <bookmark mark='e'/> What Apple spends on designing and selling it. <bookmark "
            "mark='f'/> And what Apple keeps as profit, after tax. <bookmark mark='g'/> Pause the video, and write "
            "down five numbers that add up to 1,099."
        ) as vo:
            self.play(FadeIn(ph, shift=UP * 0.2), FadeIn(spec), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(tag, shift=DOWN * 0.1))
            for k, m in enumerate("bcdef"):
                vo.wait_until(m)
                coins, fly = draw.coin_flow(tag.get_right(), rows[k][0].get_center(), n=3, r=0.09, arc=-0.4,
                                            run_time=0.9)
                self.add(coins)
                self.play(fly, FadeIn(rows[k], shift=RIGHT * 0.2), run_time=0.9)
                self.remove(coins)
            vo.wait_until("g")
            self.play(FadeIn(total), FadeIn(pause))
        self.wait(3.5)
        nxt = VGroup(T("a year later its successor costs $1,199:", 22, I.MEMORY), T("chapter 12 says why", 22,
                     I.MEMORY)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(total, RIGHT, buff=0.6)
        with self.voiceover(
            "Most people guess that either the factory or Apple gets most of it. Hold on to your numbers: we will "
            "check them in chapter five. <bookmark mark='a'/> And notice the date. A year later, the same phone's "
            "successor went on sale for 1,199 dollars. Why it cost a hundred dollars more is the story of chapter "
            "twelve, and it changes who gets the money."
        ) as vo:
            self.play(*[Indicate(r[0], color=I.MONEY, scale_factor=1.05) for r in rows], run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(pause), FadeIn(nxt))
        self.clear_scene()
