from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403

CHIP = ("#7FD1B9", "#F2C14E", "#F25F5C")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ how long does a price last?", r"Pick a typical American consumer price. \ How "
             r"long until it changes?", "Chapter one. Play it: how long does a price last?",
             lit={2004: r"Bils and Klenow", 2008: r"Nakamura and Steinsson"}, scale=("firm",),
             horizon=("a month", "a year"))
        self.choose()
        self.reveal()

    def _chips(self):
        chips = VGroup(*[VGroup(RoundedRectangle(width=3.4, height=0.95, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(t, font_size=26, color=c))
                         for c, t in zip(CHIP, (r"A: \ about a month", r"B: \ about four months",
                                                r"C: \ about a year"))]).arrange(RIGHT, buff=0.5)
        for ch in chips:
            ch[1].move_to(ch[0])
        return chips

    def choose(self):
        rows = VGroup(
            label(r"the median price in America's consumer price index:", font_size=26, color=E.ACCENT),
            label(r"how many months, \ on average, \ before it changes?", font_size=26, color=PRICE),
            label(r"(petrol changes almost weekly; \ a doctor's fee perhaps once a year; \ the median is somewhere "
                  r"in between)", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.4).move_to(UP * 1.5)
        chips = self._chips().move_to(DOWN * 1.2)
        ring = countdown().scale(0.7).next_to(chips, DOWN, buff=0.4)
        with self.voiceover(
            "Your turn. Take the prices that go into America's consumer price index, from petrol to haircuts to "
            "rent, and line them up by how often they change. <bookmark mark='a'/> Petrol changes almost every "
            "week; some fees barely once a year. What about the price in the middle? <bookmark mark='b'/> About a "
            "month; about four months; or about a year? Pause, and choose."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        chips = self._chips().move_to(UP * 2.2)
        rows = VGroup(
            label(r"Bils and Klenow, \ 2004: \ 350 categories, \ 1995--97: \ the median lasts 4.3 months", font_size=23,
                  color=CHIP[1]),
            label(r"goods 3.2 months, \ services 7.8", font_size=21, color=GREY_A),
            label(r"Nakamura and Steinsson, \ 2008: \ but many of those changes are temporary sales", font_size=23,
                  color=CHIP[2]),
            label(r"leave sales out: \ 9--12\% of regular prices change each month, \ a median of 8--11 months",
                  font_size=22, color=CHIP[2]),
            label(r"B and C are both right: \ it depends on whether a sale counts as a change", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).next_to(chips, DOWN, buff=0.6)
        tag = published_tag(r"Bils and Klenow, \ \emph{JPE} 112(5) (2004); \ Nakamura and Steinsson, \ \emph{QJE} "
                            r"123(4) (2008)", corner=DR, font_size=12)
        with self.voiceover(
            "<bookmark mark='a'/> Bils and Klenow's answer, across three hundred and fifty categories of goods and "
            "services in 1995 to 1997: the median price lasted four point three months. If you chose B, you agree "
            "with them. <bookmark mark='b'/> Goods changed faster, about every three months; services slower, "
            "about every eight. <bookmark mark='c'/> But Emi Nakamura and Jón Steinsson noticed that many of those "
            "changes are temporary sales, after which the price goes back to where it was. "
            "<bookmark mark='d'/> Leave sales out, and only nine to twelve percent of regular prices change in a "
            "month: a median of eight to eleven months. <bookmark mark='e'/> So B and C are both right, depending "
            "on whether a sale counts. For money and the cycle the answer matters, and economists still argue "
            "about which number belongs in a model."
        ) as vo:
            self.play(FadeIn(chips), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(chips[1], color=WHITE))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                if mk == "d":
                    self.play(FadeIn(r_), Indicate(chips[2], color=WHITE))
                else:
                    self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
