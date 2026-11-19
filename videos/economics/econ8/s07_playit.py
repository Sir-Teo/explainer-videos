from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Play it: \ run the boatyard", r"How many shipwrights would you hire?", "Chapter six. Play "
             "it: run the boatyard.", scale=("firm",), horizon=("a day",))
        self.setup_yard()
        self.ask()
        self.reveal()

    def table(self):
        p = load("playit")
        mp, val = np.array(p["mp"]), np.array(p["value"])
        head = VGroup(label(r"shipwright", font_size=22, color=GREY_B), label(r"extra boats", font_size=22,
                                                                             color=GREY_B),
                      label(r"worth, at \$1{,}200", font_size=22, color=GREY_B))
        xs = [-5.4, -3.4, -1.2]
        rows = VGroup()
        for i in range(8):
            r_ = VGroup(label(rf"{i + 1}", font_size=24), label(f"{mp[i]:.2f}", font_size=24, color=LAB),
                        label(rf"\${val[i]:,.0f}".replace(",", "{,}"), font_size=24, color=OUT))
            rows.add(r_)
        for j, h in enumerate(head):
            h.move_to([xs[j], 2.9, 0])
        for i, r_ in enumerate(rows):
            for j, c in enumerate(r_):
                c.move_to([xs[j], 2.35 - 0.52 * i, 0])
        rule = Line([-6.5, 2.62, 0], [0.0, 2.62, 0], color=GREY_C, stroke_width=1.5)
        return p, head, rows, rule

    def setup_yard(self):
        p, head, rows, rule = self.table()
        side = VGroup(
            label(r"Crusoe's yard this month:", font_size=26),
            label(r"4 slipways, \ already rented \ (\$1{,}600)", font_size=24, color=CAP),
            label(r"a boat sells for \$1{,}200", font_size=24, color=OUT),
            label(r"a shipwright costs \$1{,}000 a month", font_size=24, color=LAB),
            label(r"each one hired adds fewer boats \\ than the one before", font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Your turn to run the yard. <bookmark mark='a'/> This month you have four slipways, already rented. "
            "<bookmark mark='b'/> A boat sells for twelve hundred dollars, and a shipwright costs a thousand a month. "
            "<bookmark mark='c'/> Here is what each shipwright would add. The first adds two point eight three boats, "
            "worth almost thirty-four hundred dollars; the second, one point one seven, worth fourteen hundred; the "
            "third, nought point nine; and so on down."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(head), Create(rule), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows],
                                                             lag_ratio=0.25), FadeIn(side[4]), run_time=3)
        self.side, self.head, self.rows, self.rule = side, head, rows, rule

    def ask(self):
        stage = game_stage(5.8, 4.4, center=RIGHT * 3.6 + DOWN * 0.2)
        q = VGroup(label(r"how many shipwrights \\ do you hire?", font_size=32),
                   label(r"slipways are paid for either way", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.3)
        q.move_to(stage.box.get_center() + UP * 0.5)
        ring = countdown().next_to(q, DOWN, buff=0.45)
        with self.voiceover("Pause the film and decide: how many shipwrights do you hire?") as vo:
            self.play(FadeOut(self.side), FadeIn(stage), FadeIn(q))
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=6.0, rate_func=linear)
        self.play(FadeOut(stage), FadeOut(q), FadeOut(ring))

    def reveal(self):
        p = load("playit")
        val = np.array(p["value"])
        hired = p["hired"]
        marks = VGroup()
        for i, r_ in enumerate(self.rows):
            ok = val[i] >= p["wage"]
            marks.add(label(r"hire" if ok else r"stop", font_size=22, color=PASS if ok else HOLD).next_to(
                r_, RIGHT, buff=0.45))
        line = DashedLine(self.rows[hired - 1].get_corner(DL) + DOWN * 0.13 + LEFT * 0.2,
                          self.rows[hired - 1].get_corner(DR) + DOWN * 0.13 + RIGHT * 1.6, color=E.ACCENT,
                          stroke_width=2.5)
        prof = np.array(p["profit"])
        side = VGroup(
            label(rf"hire while a shipwright's boats \\ are worth more than his wage: \ {hired}", font_size=26,
                  color=E.ACCENT),
            label(r"the third adds \$1{,}079, \ the fourth only \$909", font_size=24),
            MathTex(r"p \cdot MP_L = w", font_size=40, color=E.ACCENT),
            label(rf"profit with {hired}: \ \${prof[hired]:,.0f} a month; \\ with {hired + 1}: \ "
                  rf"\${prof[hired + 1]:,.0f}; \ with {hired - 1}: \ \${prof[hired - 1]:,.0f}".replace(",", "{,}"),
                  font_size=23),
            label(r"the slipways' \$1{,}600 changes the profit, \\ not the decision", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "The rule is to compare each shipwright's value with his wage. <bookmark mark='a'/> The first two are "
            "obvious. The third adds boats worth a thousand and seventy-nine dollars, a little more than his wage: "
            "hire him. The fourth adds only nine hundred and nine: don't. <bookmark mark='b'/> So the yard hires "
            "three, where the value of the marginal product just covers the wage: price times marginal product "
            "equals the wage. <bookmark mark='c'/> With three, the month's profit is twelve hundred and seventy-nine "
            "dollars, after the slipways; with four it would be eleven hundred and eighty-eight, with two twelve "
            "hundred. <bookmark mark='d'/> Notice that the slipways' sixteen hundred dollars changed the profit but "
            "not the decision. A cost that's already sunk shouldn't change what you do next. If you hired three, "
            "you thought like a firm."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m_, shift=LEFT * 0.1) for m_ in marks], lag_ratio=0.2), run_time=3)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()
