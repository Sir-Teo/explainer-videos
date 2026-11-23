from __future__ import annotations

from explainer.industry.calls import calls
from explainer.industry.register import get
from videos.industry.industry3.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 14, "Called it?", "Could the accounts have warned you about Enron?",
             "Chapter fourteen. Called it?", lit=("change",))
        self.mclean()
        self.enron()
        self.ours()

    def mclean(self):
        q = VGroup(T("“How exactly does Enron make its money?”", 34, I.TEXT, slant="ITALIC"),
                   T("Bethany McLean, “Is Enron Overpriced?”, Fortune, 5 March 2001", 19, I.DIM)).arrange(
            DOWN, buff=0.25).move_to(UP * 1.6)
        pts = VGroup(T("priced at about 55 times its last year's earnings", 21, I.TEXT),
                     T("return on invested capital: around 7%, about what Treasuries paid", 21, I.TEXT),
                     T("cash from operations: $1.6bn (1998), $1.2bn (1999),", 21, I.TEXT),
                     T("$0.1bn in the first nine months of 2000", 21, I.TEXT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to(DOWN * 1.0)
        src = source("Fortune, 5 March 2001 (republished 2015); figures as the article gives them", size=13)
        with self.voiceover(
            "Every part ends with a forecast. This one was made by a journalist. <bookmark mark='a'/> In March "
            "2001, Enron, the Houston energy trader, was a stock-market favourite: its revenue had just more than "
            "doubled, to over a hundred billion dollars, and its shares had returned 89 percent the year before. "
            "Bethany McLean of Fortune asked a simple question: how exactly does Enron make its money? <bookmark "
            "mark='b'/> She had read the accounts. The shares were priced at about fifty-five times the last year's "
            "earnings, yet the return on the capital in the business was around seven percent, about what a "
            "Treasury bond paid. <bookmark mark='c'/> And the cash did not match the profit. Cash from operations "
            "had fallen from 1.6 billion dollars in 1998 to 1.2 billion in 1999, and to just 100 million in the "
            "first nine months of 2000, while reported earnings kept rising. Enron said she did not understand the "
            "business."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]), FadeIn(pts[3]))
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
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(rev[0]), LaggedStart(*[FadeIn(b) for b in rev[1]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(ni[0]), LaggedStart(*[FadeIn(b) for b in ni[1]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(cf[0]), LaggedStart(*[FadeIn(b) for b in cf[1]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(note), Indicate(cf[1][2], color=I.COST))
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
            vo.wait_until("a")
            self.play(FadeIn(box), FadeIn(body[:4]))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(body[4:]))
        self.clear_scene()
        assert "Microsoft" in c.claim
