from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403

LETTERS = "ABCD"
CHIP = ("#F2C14E", "#7EC8F5", "#7BD88F", "#F2788F")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Play it: \ price a coconut tree", r"What would you pay for a tree that fruits only in good "
             r"years?", "Chapter five. Play it: price a coconut tree.", lit={1978: r"Lucas"}, scale=("market",),
             horizon=("a year",))
        self.guess()
        self.reveal()

    def guess(self):
        p = load("playit")
        stage = game_stage(12.6, 6.4, center=DOWN * 0.1)
        rows = VGroup(
            label(r"next year is good or bad, \ each half the time", font_size=23, color=GREY_A),
            label(rf"a safe coconut next year costs one coconut today \ (the interest rate is "
                  rf"{100 * p['rf']:.0f})", font_size=21, color=BILL),
            label(rf"the tree: \ {p['pay_good']:.0f} coconuts in a good year, \ {p['pay_bad']:.0f} in a bad one",
                  font_size=24, color=STOCK),
            label(r"how many coconuts would the Island pay for it today?", font_size=27, color=E.ACCENT),
        ).arrange(DOWN, buff=0.28).move_to(stage.box.get_top() + DOWN * 1.6)
        chips = VGroup(*[VGroup(RoundedRectangle(width=2.4, height=1.0, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(rf"{LETTERS[i]}: \ {o:g}", font_size=26, color=c))
                         for i, (c, o) in enumerate(zip(CHIP, p["options"]))]).arrange(RIGHT, buff=0.35)
        for ch in chips:
            ch[1].move_to(ch[0])
        chips.next_to(rows, DOWN, buff=0.55)
        ring = countdown().next_to(chips, DOWN, buff=0.4)
        with self.voiceover(
            "Your turn. On the Island, next year will be good or bad, with equal chances. "
            "<bookmark mark='a'/> A coconut promised for next year, whatever happens, costs exactly one coconut "
            "today: the interest rate is zero. <bookmark mark='b'/> Now a tree. It will bear "
            f"{p['pay_good']:.0f} coconuts if the year is good, and {p['pay_bad']:.0f} if it is bad. On average, "
            f"{p['expected']:.0f}. <bookmark mark='c'/> How many coconuts would the Island pay for it today? "
            "<bookmark mark='d'/> A, six; B, eight; C, ten; or D, twelve. Pause, and choose."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(rows[0]))
            for mk, r_ in zip("abc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), FadeIn(ring),
                      run_time=2.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        p = load("playit")
        table = VGroup(
            VGroup(label(r"", font_size=22), label(r"good year", font_size=22, color=CONS),
                   label(r"bad year", font_size=22, color=RISK), label(r"price today", font_size=22,
                                                                         color=E.ACCENT)),
            VGroup(label(r"value of a coconut \\ delivered then", font_size=19, color=SDF),
                   MathTex(f"{p['m_good']:g}", font_size=34, color=SDF), MathTex(f"{p['m_bad']:g}", font_size=34,
                                                                                color=SDF), label(r"", font_size=22)),
            VGroup(label(r"the safe coconut", font_size=20, color=BILL), MathTex("1", font_size=34),
                   MathTex("1", font_size=34), MathTex(r"\tfrac12(0.8) + \tfrac12(1.2) = 1", font_size=30,
                                                      color=BILL)),
            VGroup(label(r"the tree", font_size=20, color=STOCK), MathTex(f"{p['pay_good']:.0f}", font_size=34),
                   MathTex(f"{p['pay_bad']:.0f}", font_size=34),
                   MathTex(rf"\tfrac12(0.8)(20) + \tfrac12(1.2)(0) = {p['price']:.0f}", font_size=30, color=STOCK)),
            VGroup(label(r"an insurance tree", font_size=20, color=HOUSE), MathTex(f"{p['pay_bad']:.0f}", font_size=34),
                   MathTex(f"{p['pay_good']:.0f}", font_size=34),
                   MathTex(rf"\tfrac12(0.8)(0) + \tfrac12(1.2)(20) = {p['insurance']:.0f}", font_size=30,
                           color=HOUSE)),
        )
        widths = (2.6, 1.6, 1.6, 5.8)
        for r, row in enumerate(table):
            x = -6.2
            for c, cell in enumerate(row):
                cell.move_to([x + widths[c] / 2, 2.2 - 1.05 * r, 0])
                x += widths[c] + 0.15
        note_ = label(rf"the tree's expected return: \ {p['expected']:.0f} for {p['price']:.0f}, \ "
                      rf"{100 * p['return']:.0f}\% \ against the safe {100 * p['rf']:.0f}\%: \ a risk premium",
                      font_size=23, color=E.ACCENT).to_edge(DOWN, buff=0.8)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is how the Island prices it. <bookmark mark='a'/> A coconut delivered in a good year, when "
            "everyone has plenty, is worth less to people today than one delivered in a bad year, when they are "
            "hungry: 0.8 against 1.2. These two numbers are the Island's stochastic discount factor. "
            "<bookmark mark='b'/> The safe coconut pays one in both years: half of 0.8 plus half of 1.2, exactly "
            "one. <bookmark mark='c'/> The tree pays twenty only in the good year, when coconuts are worth 0.8: "
            f"half of sixteen, so {p['price']:.0f}. If you chose B, you were right. It is worth less than its "
            f"average harvest of {p['expected']:.0f}, because it pays when coconuts are least needed. "
            "<bookmark mark='d'/> A tree that paid twenty only in bad years would be worth "
            f"{p['insurance']:.0f}, more than its average: that is insurance. <bookmark mark='e'/> So the tree "
            f"returns {100 * p['return']:.0f} percent on average against the safe zero. That is a risk premium, and "
            "it comes from when the tree pays, not how much it varies."
        ) as vo:
            self.play(FadeIn(table[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(table[1]))
            vo.wait_until("b")
            self.play(FadeIn(table[2]))
            vo.wait_until("c")
            self.play(FadeIn(table[3]))
            vo.wait_until("d")
            self.play(FadeIn(table[4]))
            vo.wait_until("e")
            self.play(FadeIn(note_))
        self.clear_scene()
