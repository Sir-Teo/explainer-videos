from __future__ import annotations

from videos.industry.industry3.common import *  # noqa: F403
from videos.industry.industry3.s03_ledger import _bank

COST_OF_CAPITAL = 0.08  # illustrative: what investors could expect elsewhere at similar risk


class Roic(VoiceoverScene):
    def construct(self):
        card(self, 8, "The return on capital", "When does a profitable business destroy value?",
             "Chapter eight. The return on capital.", lit=("moat",))
        self.idea()
        self.six()

    def idea(self):
        def stack(amount, color, x, label, sub):
            n = int(round(amount / 5))
            coins = VGroup(*[viz.coin(0.16, color).move_to(np.array([x + (k % 5) * 0.36 - 0.72, -1.9 + (k // 5) * 0.36,
                                                                      0])) for k in range(n)])
            lab = VGroup(TB(label, 26, color), T(sub, 17, I.DIM)).arrange(DOWN, buff=0.06).next_to(
                np.array([x, -1.9, 0]), DOWN, buff=0.35)
            return VGroup(coins, lab)
        put = stack(100, I.TEXT, -4.6, "$100 invested", "by the owners")
        good = stack(150, I.PROFIT, 0.0, "worth $150", "earns $12 a year: 12%")
        bad = stack(75, I.COST, 4.6, "worth $75", "earns $6 a year: 6%")
        rule = T(f"Investors could earn {100 * COST_OF_CAPITAL:.0f}% elsewhere at the same risk (an assumption)", 20,
                 I.ACCENT).to_edge(UP, buff=0.4)
        f = T("value = yearly earnings ÷ the return investors require", 19, I.DIM).next_to(rule, DOWN, buff=0.2)
        # the owners' alternative: somewhere else at the same risk
        alt = VGroup(_bank().scale(2.6), draw.factory(0.9, color=I.DIM)).arrange(RIGHT, buff=0.4).move_to([2.6, 0.2, 0])
        go = CurvedArrow(np.array([-4.0, -1.0, 0]), alt.get_left() + LEFT * 0.15, angle=-0.8, color=I.DIM,
                         stroke_width=3)
        alt_q = T("somewhere else: ?", 20, I.DIM).next_to(alt, DOWN, buff=0.25)
        alt_r = T("somewhere else: 8% a year", 20, I.ACCENT).next_to(alt, DOWN, buff=0.25)
        with self.voiceover(
            "Profit is not the same as a good business, because the owners' money is not free. They could have put "
            "it somewhere else. <bookmark mark='a'/> Suppose that elsewhere, at the same risk, they could expect "
            "eight percent a year. That is the business's cost of capital. <bookmark mark='b'/> Now they put a "
            "hundred dollars into it. <bookmark mark='c'/> If it earns twelve dollars a year, a return on capital "
            "of twelve percent, investors will pay about a hundred and fifty dollars for that stream: twelve divided "
            "by eight percent. Value was created. <bookmark mark='d'/> If it earns six dollars, it is profitable, "
            "and worth only seventy-five. Every dollar put in became seventy-five cents. And a company like that "
            "destroys more value the faster it grows, because every new dollar it invests shrinks too. Growth only "
            "helps when the return on capital is above its cost."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c) for c in put[0]], lag_ratio=0.05), FadeIn(put[1]))
            self.play(FadeIn(alt, shift=LEFT * 0.2), Create(go), FadeIn(alt_q))
            vo.wait_until("a")
            self.play(FadeIn(rule), FadeIn(f), Transform(alt_q, alt_r))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(alt, go, alt_q)), Indicate(put[0], color=WHITE, scale_factor=1.05))
            vo.wait_until("c")
            biz = draw.factory(1.1, color=I.PROFIT).move_to([-2.3, 1.0, 0])
            self.play(FadeIn(biz, shift=DOWN * 0.2))
            self.play(ReplacementTransform(put[0].copy(), good[0], path_arc=-0.8), FadeIn(good[1]), run_time=1.8)
            vo.wait_until("d")
            biz2 = draw.factory(1.1, color=I.COST).move_to([2.3, 1.0, 0])
            self.play(FadeIn(biz2, shift=DOWN * 0.2))
            self.play(ReplacementTransform(put[0].copy(), bad[0], path_arc=-0.6), FadeIn(bad[1]), run_time=1.8)
        self.clear_scene()

    def six(self):
        S = R["six"]
        ks = sorted([k for k in S if S[k]["roic"] is not None], key=lambda k: -S[k]["roic"])
        items = [(name(k), S[k]["roic"], CO[k], S[k]["kind"]) for k in ks]
        items.append(("Enron, 2000", 0.07, "#8B95A7", "Fortune's estimate, March 2001"))
        rows = viz.margin_ladder(items, max_value=0.36, bar_len=6.4, row_h=0.6, size=20, name_w=2.8)
        rows.move_to(LEFT * 0.5 + DOWN * 0.3)
        track = rows[0][1]
        x8 = track.get_left()[0] + track.width * COST_OF_CAPITAL / 0.36
        line = DashedLine(np.array([x8, rows.get_top()[1] + 0.25, 0]), np.array([x8, rows.get_bottom()[1] - 0.1, 0]),
                          color=I.ACCENT, stroke_width=2)
        ll = T("8%: the assumed cost of capital", 16, I.ACCENT).next_to(line, UP, buff=0.05)
        head = T("Return on capital: after-tax operating profit per $ of owners' money and long-term debt", 20,
                 I.TEXT).to_edge(UP, buff=0.3)
        note = T("operating profit taxed at 21%; banks left out: their debt is their raw material", 15, I.DIM).to_edge(
            DOWN, buff=0.75)
        src = source("Forms 10-K (Costco, Microsoft FY2026; others 2025); Fortune, 5 March 2001", corner=DR, size=12)
        n = S["nee"]
        with self.voiceover(
            "Here is the return on capital for five of our six companies, measured one simple way: operating "
            "profit after a standard tax, divided by the owners' money plus long-term debt. <bookmark mark='a'/> "
            f"Lilly, Microsoft and Costco earn between {100 * S['cost']['roic']:.0f} and "
            f"{100 * S['lly']['roic']:.0f} percent: far above any reasonable cost of capital. Each has something "
            "competitors cannot easily copy: patents on a medicine, software everyone already uses, members who "
            "renew. <bookmark mark='b'/> Delta earned about thirteen percent in 2025; an airline's return swings "
            "with fuel and the economy, as Part six, on the cycle, will show. <bookmark mark='c'/> NextEra shows about "
            f"{100 * n['roic']:.0f} percent, and the measure is unkind to it: a regulated utility is allowed a return "
            "close to its cost of capital, and much of NextEra's profit arrives as clean-energy tax credits, which "
            "are booked as lower income tax, below the operating line this measure uses. <bookmark mark='d'/> And "
            "the last bar is Enron in 2000, by Fortune's estimate: about seven percent, the return of a Treasury "
            "bond, for a company priced as a star. That number comes back at the end of this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.2), Create(line), FadeIn(ll),
                      run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5]), Indicate(rows[5], color="#8B95A7", scale_factor=1.04))
        self.clear_scene()
