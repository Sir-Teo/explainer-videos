from __future__ import annotations

from explainer.industry.calls import calls
from explainer.industry.register import get
from videos.industry.industry3.common import *  # noqa: F403
from videos.industry.industry3.s03_ledger import _bank


class Called(VoiceoverScene):
    def construct(self):
        card(self, 14, "Called it?", "Could the accounts have warned you about Enron?",
             "Chapter fourteen. Called it?", lit=("change",))
        self.mclean()
        self.enron()
        self.ours()

    def mclean(self):
        E = R["enron"]
        # a magazine page: the journalist's question
        page = VGroup(RoundedRectangle(corner_radius=0.06, width=1.9, height=2.5, stroke_width=0, fill_color="#E8E4DA",
                                       fill_opacity=1),
                      Rectangle(width=1.9, height=0.42, stroke_width=0, fill_color="#C8102E", fill_opacity=1))
        page[1].align_to(page[0], UP)
        head = T("Is Enron Overpriced?", 15, "#1B1F27", weight=BOLD).move_to(page[0]).shift(UP * 0.55)
        lines = VGroup(*[Line([-0.75, 0, 0], [0.75 if k % 3 else 0.45, 0, 0], stroke_color="#8C929B", stroke_width=2)
                         for k in range(7)]).arrange(DOWN, buff=0.13, aligned_edge=LEFT).next_to(head, DOWN, buff=0.18)
        mag = VGroup(page, head, lines).move_to([-5.2, 1.25, 0])
        when = T("Fortune, 5 March 2001", 16, I.DIM).next_to(mag, DOWN, buff=0.12)
        # the company: a lit tower, its revenue and its shares
        tower = VGroup(Rectangle(width=1.0, height=3.0, stroke_width=0, fill_color="#1E2633", fill_opacity=1))
        tower.add(*[Rectangle(width=0.1, height=0.1, stroke_width=0, fill_color=draw.LIT if (i + j) % 3 else "#2A3446",
                              fill_opacity=1).move_to([-0.3 + 0.2 * j, -1.3 + 0.24 * i, 0])
                    for i in range(11) for j in range(4)])
        tower.move_to([-1.9, 1.1, 0])
        tname = VGroup(TB("Enron", 20, I.TEXT), T("Houston: gas pipelines, energy trading", 15, I.DIM)).arrange(
            DOWN, buff=0.05).next_to(tower, DOWN, buff=0.12)
        u = 0.028
        rev = VGroup()
        for k, y in enumerate((1999, 2000)):
            b = Rectangle(width=0.7, height=E["rev"][y] * u, stroke_width=0, fill_color="#7EC8F5", fill_opacity=0.9)
            b.move_to([0.6 + 1.0 * k, -0.35, 0], aligned_edge=DOWN)
            rev.add(VGroup(b, T(f"${E['rev'][y]:.0f}bn", 16, "#7EC8F5").next_to(b, UP, buff=0.05),
                           T(str(y), 15, I.DIM).next_to(b, DOWN, buff=0.06)))
        rev_t = T("revenue", 18, "#7EC8F5").next_to(rev, UP, buff=0.45)
        st0, st1 = draw.coin_stack(10, 0.3), draw.coin_stack(19, 0.3)
        st0.move_to([3.6, -0.3, 0], aligned_edge=DOWN)
        st1.move_to([5.1, -0.3, 0], aligned_edge=DOWN)
        sh = VGroup(T("$1.00", 16, I.MONEY).next_to(st0, UP, buff=0.06), T("$1.89", 16, I.MONEY).next_to(st1, UP, buff=0.06),
                    T("Jan 2000", 15, I.DIM).next_to(st0, DOWN, buff=0.08),
                    T("Dec 2000", 15, I.DIM).next_to(st1, DOWN, buff=0.08))
        sh_t = T("a dollar of its shares", 18, I.MONEY).move_to([4.35, rev_t.get_y(), 0])
        q = VGroup(T("“How exactly does Enron make its money?”", 32, I.TEXT, slant="ITALIC"),
                   T("Bethany McLean, “Is Enron Overpriced?”, Fortune, 5 March 2001", 17, I.DIM)).arrange(
            DOWN, buff=0.2).move_to([1.4, 1.7, 0])
        # what she read: the price against the return, and profit against cash
        tag = VGroup(Polygon([-0.9, -0.38, 0], [0.6, -0.38, 0], [0.95, 0, 0], [0.6, 0.38, 0], [-0.9, 0.38, 0],
                             stroke_color=I.ACCENT, stroke_width=2, fill_color="#2A2410", fill_opacity=1),
                     Circle(radius=0.07, stroke_width=0, fill_color=I.ACCENT, fill_opacity=1).move_to([0.6, 0, 0]),
                     TB("55×", 28, I.ACCENT).move_to([-0.2, 0, 0]))
        tag.move_to([-4.9, -1.6, 0])
        tag_t = T("55 times last year's earnings", 16, I.ACCENT).next_to(tag, DOWN, buff=0.15)
        bh = 1.3
        roic = Rectangle(width=0.6, height=bh, stroke_width=0, fill_color=I.PROFIT, fill_opacity=0.9).move_to(
            [-2.7, -3.0, 0], aligned_edge=DOWN)
        tsy = Rectangle(width=0.6, height=bh * 0.95, stroke_width=0, fill_color=GREY_B, fill_opacity=0.9).move_to(
            [-1.7, -3.0, 0], aligned_edge=DOWN)
        par = DashedLine(roic.get_corner(UL) + LEFT * 0.1, tsy.get_corner(UR) + RIGHT * 0.1, stroke_color=WHITE,
                         stroke_width=1.5)
        rt = VGroup(T("return on capital ≈7%", 15, I.PROFIT).next_to(roic, UP, buff=0.08).shift(LEFT * 0.2),
                    T("Treasuries", 15, GREY_B).next_to(tsy, DOWN, buff=0.06),
                    T("Enron", 15, I.PROFIT).next_to(roic, DOWN, buff=0.06))
        cash = VGroup()
        for k, (lab, v) in enumerate((("1998", 1.6), ("1999", 1.2), ("2000, 9 months", 0.1))):
            st = draw.coin_stack(max(1, int(round(v * 9))), 0.3).move_to([1.6 + 1.6 * k, -3.0, 0], aligned_edge=DOWN)
            cash.add(VGroup(st, T(f"${v:.1f}bn", 16, I.MONEY).next_to(st, UP, buff=0.06),
                            T(lab, 14, I.DIM).next_to([1.6 + 1.6 * k, -3.0, 0], DOWN, buff=0.08)))
        cash_t = T("cash from operations", 17, I.MONEY).move_to([3.2, -0.75, 0])
        prof = Arrow([1.0, -1.45, 0], [5.6, -0.95, 0], buff=0, stroke_width=5, color=I.PROFIT,
                     max_tip_length_to_length_ratio=0.06)
        prof_t = T("reported earnings: rising", 16, I.PROFIT).next_to(prof.get_end(), DOWN, buff=0.12).shift(LEFT * 0.6)
        src = source("Fortune, 5 March 2001 (republished 2015); figures as the article gives them", size=13)
        with self.voiceover(
            "Every part ends with a forecast. This one was made by a journalist. <bookmark mark='a'/> In March "
            "2001, Enron, the Houston energy trader, was a stock-market favourite: its revenue had just more than "
            "doubled, to over a hundred billion dollars, and its shares had returned 89 percent the year before. "
            "<bookmark mark='q'/> Bethany McLean of Fortune asked a simple question: how exactly does Enron make "
            "its money? <bookmark mark='b'/> She had read the accounts. The shares were priced at about "
            "fifty-five times the last year's earnings, yet the return on the capital in the business was around "
            "seven percent, about what a Treasury bond paid. <bookmark mark='c'/> And the cash did not match the "
            "profit. Cash from operations had fallen from 1.6 billion dollars in 1998 to 1.2 billion in 1999, and "
            "to just 100 million in the first nine months of 2000, while reported earnings kept rising. Enron said "
            "she did not understand the business."
        ) as vo:
            self.play(FadeIn(src), FadeIn(mag, shift=UP * 0.2), FadeIn(when))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.15), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(tower, shift=UP * 0.2), FadeIn(tname))
            self.play(FadeIn(rev_t), GrowFromEdge(rev[0][0], DOWN), FadeIn(rev[0][1:]))
            self.play(GrowFromEdge(rev[1][0], DOWN), FadeIn(rev[1][1:]), run_time=1.2)
            self.play(FadeIn(sh_t), FadeIn(st0), FadeIn(sh[0]), FadeIn(sh[2]))
            self.play(TransformFromCopy(st0, st1), FadeIn(sh[1]), FadeIn(sh[3]), run_time=1.4)
            vo.wait_until("q")
            self.play(FadeOut(VGroup(tower, tname, rev, rev_t, st0, st1, sh, sh_t)), run_time=0.6)
            self.play(Write(q[0]), FadeIn(q[1]), Indicate(mag, color=WHITE, scale_factor=1.05), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(tag, shift=RIGHT * 0.2), FadeIn(tag_t))
            self.play(Rotate(tag, 0.12, about_point=tag[1].get_center()), run_time=0.4)
            self.play(Rotate(tag, -0.12, about_point=tag[1].get_center()), run_time=0.4)
            self.play(GrowFromEdge(roic, DOWN), GrowFromEdge(tsy, DOWN), FadeIn(rt))
            self.play(Create(par))
            vo.wait_until("c")
            self.play(FadeIn(cash_t), LaggedStart(*[FadeIn(c_[0], shift=DOWN * 0.2) for c_ in cash], lag_ratio=0.4),
                      LaggedStart(*[FadeIn(c_[1:]) for c_ in cash], lag_ratio=0.4), run_time=2.0)
            self.play(GrowArrow(prof), FadeIn(prof_t), run_time=1.4)
            self.play(Indicate(cash[2], color=I.COST, scale_factor=1.4))
        self.clear_scene()

    def enron(self):
        E = R["enron"]
        yrs = [1998, 1999, 2000]
        L = 4.2

        def bars(series, mx, color, x0, title, fmt):
            g = VGroup()
            for k, y in enumerate(yrs):
                v = series[y]
                r = Rectangle(width=0.7, height=max(L * v / mx, 0.02), fill_color=color, fill_opacity=0.9,
                              stroke_width=0).move_to(np.array([x0 + k * 0.95, -2.2 + L * v / mx / 2, 0]))
                g.add(VGroup(r, T(fmt(v), 15, color).next_to(r, UP, buff=0.05),
                             T(str(y), 14, I.DIM).next_to(np.array([x0 + k * 0.95, -2.2, 0]), DOWN, buff=0.08)))
            return VGroup(TB(title, 19, color).move_to(np.array([x0 + 0.95, 2.55, 0])), g)
        rev = bars(E["rev"], 105, "#7EC8F5", -5.6, "Revenue", lambda v: f"${v:.0f}bn")
        ni = bars(E["ni"], 8.0, I.PROFIT, -1.45, "Net income", lambda v: f"${v:.2f}bn")
        cf = bars(E["cfo"], 8.0, I.MONEY, 2.7, "Cash from operations", lambda v: f"${v:.2f}bn")
        note = VGroup(T("2000's cash: year-end 'prepays', loans booked as trading", 16, I.COST),
                      T(f"(about ${E['prepays']:.0f}bn over six years: US Senate, 2002)", 16, I.COST)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).move_to(np.array([3.4, 1.75, 0]))
        out = VGroup(T(f"8 November 2001: profits for 1997-2000 restated, ${1e3 * E['restate']:.0f} million lower", 19,
                       I.TEXT),
                     T("2 December 2001: Enron files for bankruptcy", 21, I.COST)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.3)
        src = source("Enron Form 10-K 2000 and Form 8-Ks of 8 November and 17 December 2001; Senator Levin, 23 July "
                     "2002", corner=UR, size=12)
        doc = RoundedRectangle(corner_radius=0.04, width=0.7, height=0.9, stroke_width=0, fill_color="#E8E4DA",
                               fill_opacity=1)
        filing = VGroup(doc, *[Line([-0.22, 0, 0], [0.22, 0, 0], stroke_color="#8C929B", stroke_width=2).move_to(doc).shift(
            UP * (0.25 - 0.12 * k)) for k in range(5)], T("Form 10-K, 2000", 15, I.DIM).next_to(doc, DOWN, buff=0.08))
        filing.move_to([-6.1, 2.6, 0])
        floor_ = Line([-6.0, -2.2, 0], [5.6, -2.2, 0], stroke_color=I.DIM, stroke_width=1.5).set_opacity(0)
        bank = VGroup(_bank().scale(2.2), T("the banks", 15, I.DIM)).arrange(DOWN, buff=0.08).move_to([6.2, -0.9, 0])
        with self.voiceover(
            "Here are the accounts she was reading, as Enron filed them for 2000, a few weeks after her article. "
            "<bookmark mark='a'/> Revenue more than doubled, to over a hundred billion dollars, almost all of it "
            "from its wholesale energy business. <bookmark mark='b'/> Net income crept up, to just under a "
            "billion. <bookmark mark='c'/> And cash from operations, after the weak first nine months, leapt to 4.8 "
            "billion dollars for the full year. <bookmark mark='d'/> A Senate investigation later found how: "
            "deals the banks called prepays, loans dressed up as energy trades so that borrowed money arrived as "
            "operating cash, about eight billion dollars of them over six years. <bookmark mark='e'/> In November "
            "2001 Enron restated four years of profits, cutting them by 591 million dollars, and on the second of "
            "December it filed for bankruptcy. The accounts did not tell the "
            "whole truth. But the gap between profit and cash, and a return on capital that never matched the "
            "story, were there for a careful reader."
        ) as vo:
            self.play(FadeIn(src), FadeIn(filing, shift=UP * 0.2))
            self.play(*[FadeIn(g_[0]) for g_ in (rev, ni, cf)],
                      *[FadeIn(b[2]) for g_ in (rev, ni, cf) for b in g_[1]], floor_.animate.set_opacity(1))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1])) for b in rev[1]],
                                  lag_ratio=0.4), run_time=1.8)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1])) for b in ni[1]],
                                  lag_ratio=0.4), run_time=1.8)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1])) for b in cf[1]],
                                  lag_ratio=0.4), run_time=1.8)
            vo.wait_until("d")
            self.play(FadeIn(bank, shift=LEFT * 0.2), FadeIn(note))
            coins, fly = draw.coin_flow(bank.get_left(), cf[1][2][0].get_top() + DOWN * 0.3, n=8, r=0.09, arc=0.6)
            self.add(coins)
            self.play(fly, Indicate(cf[1][2], color=I.COST))
            self.remove(coins)
            vo.wait_until("e")
            self.play(FadeIn(out[0]))
            self.play(FadeIn(out[1]))
        self.clear_scene()

    def ours(self):
        c = calls(3, ours=True)[0]
        M = R["cash"]["msft"]
        box = RoundedRectangle(corner_radius=0.15, width=12.2, height=4.6, fill_color=I.PANEL, fill_opacity=1,
                               stroke_color=I.ACCENT, stroke_width=2).move_to(DOWN * 0.2)
        body = VGroup(TB("This series' call, made 23 November 2026", 24, I.ACCENT),
                      T("In fiscal 2027 (to June 2027), Microsoft's free cash flow, its cash from operations", 21,
                        I.TEXT),
                      T(f"less its additions to property and equipment, will be below fiscal 2026's {bn(M['fcf'])},",
                        21, I.TEXT),
                      T(f"even though its operating income rises above fiscal 2026's {bn(get('msft.oi'))}.", 21,
                        I.TEXT),
                      TB("Probability: 65%", 24, I.ACCENT),
                      T("Scored on Microsoft's fiscal 2027 Form 10-K, due about August 2027", 17, I.DIM)).arrange(
            DOWN, buff=0.18).move_to(box)
        q = VGroup(T(f"First quarter of fiscal 2027: free cash {bn(M['q1']['fcf'])} (a year before "
                     f"{bn(M['q1_prev']['fcf'])}); spending on equipment {bn(M['q1']['capex'])}", 16, I.DIM),
                   T(f"guidance for the year's capital spending, including finance leases: about "
                     f"${get('msft.capex_guide.fy2027'):.0f}bn", 16, I.DIM)).arrange(DOWN, buff=0.05).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "And this series' own call, logged today. <bookmark mark='a'/> In its fiscal year to June 2027, "
            "Microsoft's free cash flow, the cash from its operations less what it spends on equipment, will be "
            f"lower than the {say_bn(M['fcf'])} of fiscal 2026, even though its operating profit will be higher. "
            "<bookmark mark='b'/> The reasoning: in the first quarter, spending on equipment doubled, and free cash "
            f"fell to {say_bn(M['q1']['fcf'])} from {say_bn(M['q1_prev']['fcf'])}; and the company has guided to "
            "spending of about 170 billion dollars in the year, including leases. <bookmark mark='c'/> What would "
            "make us wrong: a slowdown in the building, or cash from customers arriving faster than expected. We "
            "put it at sixty-five percent, and we will score it on the annual report next summer."
        ) as vo:
            self.play(FadeIn(box), FadeIn(body[0]))
            vo.wait_until("a")
            self.play(FadeIn(body[1:4]))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(body[4:]))
        self.clear_scene()
        assert "Microsoft" in c.claim
