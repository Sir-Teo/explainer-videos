from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.collectors()
        self.two()
        self.question()
        self.title()
        self.objectives()

    def collectors(self):
        rows = VGroup(
            label(r"every month, \ the Bureau of Labor Statistics", font_size=30, color=E.ACCENT),
            label(r"about 100{,}000 prices, \ from about 23{,}000 shops and service businesses", font_size=24,
                  color=GREY_A),
            label(r"2004: \ Mark Bils and Peter Klenow open the records behind the consumer price index", font_size=23,
                  color=PRICE),
            label(r"and count how often each price changes", font_size=24, color=PRICE),
            label(r"the median price lasts about four months: \ far less than economists had assumed", font_size=23,
                  color=FLEX),
            label(r"and yet long enough for money to move the real economy", font_size=24, color=STICKY),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"BLS, \ \emph{Handbook of Methods}: \ the CPI; \ Bils and Klenow, \ \emph{JPE} 112(5) "
                            r"(2004)", corner=DR, font_size=12)
        with self.voiceover(
            "Every month, the Bureau of Labor Statistics records about a hundred thousand prices, from about "
            "twenty-three thousand shops and service businesses across America, to build the consumer price index. "
            "<bookmark mark='a'/> In 2004, Mark Bils and Peter Klenow opened those records <bookmark mark='b'/> and "
            "did something simple: they counted how often each price changes. <bookmark mark='c'/> The median "
            "price lasted about four months, far less time than economists had been assuming. "
            "<bookmark mark='d'/> And yet, as this part will show, long enough for money to move the real economy."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def two(self):
        S = load("sticky")
        t = np.array(S["t"])
        ax = plane([1968, 2027], [-4, 20], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 5, 10, 15, 20],
                   ylabel=r"inflation over 12 months, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=15)
        zero = seg(ax, 1968, 0, 2027, 0, GREY_D, 1.5)
        flex = path(ax, t, np.clip(S["flex"], -4, 20), FLEX, 2.2, smooth=False)
        stk = path(ax, t, np.clip(S["sticky"], -4, 20), STICKY, 3, smooth=False)
        side = VGroup(
            label(r"orange: \ prices that change often \\ (petrol excluded: \ clothes, \\ cars, \ hotel rooms...)",
                  font_size=18, color=FLEX),
            label(r"blue: \ prices that change rarely \\ (rents, \ haircuts, \\ insurance, \ fees...)", font_size=18,
                  color=STICKY),
            label(rf"2022: \ the flexible ones rose {S['peak_flex_2022']:.0f}\%; \\ the sticky ones "
                  rf"{S['peak_sticky_2022']:.1f}\%", font_size=18, color=E.ACCENT),
            label(r"two kinds of price, \\ two kinds of inflation", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Federal Reserve Bank of Atlanta: \ sticky- and flexible-price CPIs less food and energy, \ "
                       r"via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Here is what that difference does. The Federal Reserve Bank of Atlanta splits the consumer price "
            "index, food and energy aside, into two groups by how often each item's price changes. "
            "<bookmark mark='a'/> In orange, the prices that change often: clothing, cars, hotel rooms. "
            "<bookmark mark='b'/> In blue, the prices that change rarely: rents, haircuts, insurance and fees. "
            f"<bookmark mark='c'/> In 2022 the flexible prices rose {S['peak_flex_2022']:.0f} percent in a year, the "
            f"sticky ones {S['peak_sticky_2022']:.1f}. <bookmark mark='d'/> The flexible line jumps with every shock; "
            "the sticky one moves slowly and carries the trend. If all prices behaved like the orange line, money "
            "would barely matter for output. Because so many behave like the blue one, it does."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(flex), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(stk), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how sticky are prices, \ and why?", font_size=26, color=PRICE),
            label(r"what do sticky prices do to the economy, \ in three equations?", font_size=26, color=INFL),
            label(r"what should a central bank do, \ and what happens when rates hit zero?", font_size=26,
                  color=CB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: why does money move the real economy, and what is the best a central bank can "
            "do? <bookmark mark='a'/> How sticky are prices, and why? <bookmark mark='b'/> What do sticky prices do "
            "to the whole economy? The answer fits in three equations, which now sit inside every central bank. "
            "<bookmark mark='c'/> And what should a central bank do with them, including when interest rates "
            "cannot fall any further?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        S = load("sticky")
        t = np.array(S["t"])
        mini = plane([1968, 2027], [-4, 20], x_length=4.2, y_length=1.4)
        logo = VGroup(path(mini, t, np.clip(S["flex"], -4, 20), FLEX, 2, smooth=False),
                      path(mini, t, np.clip(S["sticky"], -4, 20), STICKY, 3, smooth=False))
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 30 \ $\cdot$ \ Sticky Prices", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part thirty: sticky prices."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VI \ $\cdot$ \ Money and the Cycle", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"how long prices last: \ a guess, \ then the evidence; \ why prices stick",
            r"Calvo's pricing and the New Keynesian Phillips curve, \ derived",
            r"a dynamic IS curve, \ the Taylor rule, \ and the three equations solved",
            r"the divine coincidence; \ optimal policy; \ menu costs and the selection effect",
            r"the zero lower bound and forward guidance; \ medium-scale models; \ a dial",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> A guess about how long prices last, then the evidence, and why "
            "prices stick at all. <bookmark mark='b'/> Calvo's model of price setting, and the Phillips curve it "
            "implies, derived. <bookmark mark='c'/> The household's side as a dynamic IS curve, the central bank as "
            "a Taylor rule, and the three equations solved together. <bookmark mark='d'/> When stabilizing "
            "inflation also stabilizes output, what the best policy looks like, and why menu costs can make money "
            "matter less than Calvo says. <bookmark mark='e'/> And the zero lower bound, the puzzle of forward "
            "guidance, the bigger models central banks actually use, and a dial."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
