from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class MM(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Modigliani and Miller: \ the pie and its slices", r"Does it matter how a firm is financed?",
             "Chapter four. Modigliani and Miller: the pie and its slices.",
             lit={1958: r"Modigliani and Miller", 1984: r"Myers and Majluf"}, scale=("firm",), horizon=("years",))
        self.pie()
        self.leverage()
        self.breaks()

    def pie(self):
        def pie(debt_share, center):
            g = VGroup(Circle(radius=1.3, color=GREY_B, stroke_width=2).move_to(center))
            if debt_share > 0:
                g.add(Sector(radius=1.3, angle=TAU * debt_share, start_angle=PI / 2, arc_center=center,
                             color=BILL, fill_opacity=0.75, stroke_width=0))
            g.add(Sector(radius=1.3, angle=TAU * (1 - debt_share), start_angle=PI / 2 + TAU * debt_share,
                         arc_center=center, color=STOCK, fill_opacity=0.75, stroke_width=0))
            return g
        p1 = pie(0.0, LEFT * 3.5 + UP * 0.3)
        p2 = pie(0.5, RIGHT * 3.5 + UP * 0.3)
        l1 = label(r"all equity", font_size=22, color=STOCK).next_to(p1, DOWN, buff=0.3)
        l2 = label(r"half debt, \ half equity", font_size=22, color=GREY_A).next_to(p2, DOWN, buff=0.3)
        same = label(r"the same factories, \ the same cash flows: \ the same pie", font_size=25,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        rule = label(r"in a perfect market, \ the firm's value does not depend on how it is sliced", font_size=24,
                     color=WHITE).to_edge(DOWN, buff=1.0)
        tag = published_tag(r"Modigliani and Miller, AER 48(3) (1958): \ 261--297", corner=DR, font_size=12)
        with self.voiceover(
            "In 1958 Franco Modigliani and Merton Miller asked whether it matters how a firm pays for its capital. "
            "<bookmark mark='a'/> A firm is its factories and the cash they produce: a pie. Financing decides only "
            "how the pie is sliced between lenders and shareholders. <bookmark mark='b'/> All equity, or half debt "
            "and half equity: the same factories, the same cash. <bookmark mark='c'/> In a perfect market, with no "
            "taxes, no costs of bankruptcy and everyone equally informed, the value of the firm cannot depend on the "
            "slicing. If it did, an investor could buy the cheaper firm, borrow or lend on the side to copy the "
            "other's slicing, and pocket the difference."
        ) as vo:
            self.play(FadeIn(p1), FadeIn(l1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(same))
            vo.wait_until("b")
            self.play(FadeIn(p2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.clear_scene()

    def leverage(self):
        rows = VGroup(
            MathTex(r"r_E \;=\; r_A + \frac{D}{E}\,\big(r_A - r_D\big)", font_size=48, color=STOCK),
            label(r"borrowing makes the remaining equity riskier, \ so shareholders demand more", font_size=24,
                  color=GREY_A),
            label(r"the average cost of capital stays at $r_A$: \ cheap debt is not a free lunch", font_size=24,
                  color=WHITE),
            label(r"example: \ $r_A = 8\%$, \ $r_D = 4\%$; \ half debt: \ $r_E = 12\%$; \ average still $8\%$",
                  font_size=23, color=BILL),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.1)
        with self.voiceover(
            "The theorem has a second half that every finance student learns. <bookmark mark='a'/> The return "
            "shareholders require rises with leverage: the return on the firm's assets, plus the debt-to-equity "
            "ratio times the gap between that and the rate on debt. <bookmark mark='b'/> Borrowing makes the "
            "remaining equity riskier, so shareholders demand more. <bookmark mark='c'/> The weighted average cost "
            "of capital does not change: debt that looks cheap only makes equity dearer. <bookmark mark='d'/> If "
            "the assets earn eight percent and debt costs four, a firm financed half by debt has equity that must "
            "earn twelve; the average is still eight."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def breaks(self):
        rows = VGroup(
            label(r"what breaks it, \ and so what finance is about", font_size=28, color=E.ACCENT),
            label(r"taxes: \ interest is deductible, \ dividends are not: \ debt saves tax", font_size=23, color=BILL),
            label(r"bankruptcy: \ too much debt brings costly distress", font_size=23, color=RISK),
            label(r"information: \ managers know more; \ issuing shares signals bad news \ (Myers and Majluf, \ 1984)",
                  font_size=23, color=SDF),
            label(r"agency: \ debt disciplines managers, \ and tempts shareholders to gamble \ (Part 14)", font_size=23,
                  color=FIRM),
            label(r"the theorem's value is the list: \ each failure is a reason financing matters", font_size=23,
                  color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Myers and Majluf, JFE 13(2) (1984)", corner=DR, font_size=12)
        with self.voiceover(
            "The theorem is false in practice, and that is its use. <bookmark mark='a'/> It tells you exactly what "
            "must be true for financing to matter. <bookmark mark='b'/> Taxes: interest is deductible and dividends "
            "are not, so debt saves tax. <bookmark mark='c'/> Bankruptcy: too much debt brings costly distress. "
            "<bookmark mark='d'/> Information: managers know more than investors, so a share issue signals that the "
            "shares are dear, as Stewart Myers and Nicholas Majluf argued. <bookmark mark='e'/> Agency: debt "
            "disciplines managers, and tempts shareholders to gamble with lenders' money, as in Part fourteen. "
            "Each failure is a reason financing matters, and Parts twenty-six and thirty-three build on them."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:5]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
            self.play(FadeIn(rows[5]))
        self.clear_scene()
