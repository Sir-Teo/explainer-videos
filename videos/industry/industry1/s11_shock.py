from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry1.common import *  # noqa: F403


class Shock(VoiceoverScene):
    def construct(self):
        card(self, 9, "2026: the memory shock", "What happens when one link suddenly becomes scarce?",
             "Chapter nine. Twenty twenty-six: the memory shock.", lit=("change", "moat"))
        self.why()
        self.bill()
        self.makers()
        self.samsung()
        self.market()

    def why(self):
        acc = RoundedRectangle(corner_radius=0.1, width=2.2, height=2.2, fill_color=I.CHIP, fill_opacity=0.25,
                               stroke_color=I.CHIP, stroke_width=2.5).shift(LEFT * 3.2)
        acc_l = T("AI chip", 20, I.TEXT).move_to(acc)
        hbm = VGroup()
        for dx, dy in ((-1.55, 0.6), (-1.55, -0.6), (1.55, 0.6), (1.55, -0.6)):
            st = VGroup(*[Rectangle(width=0.7, height=0.12, fill_color=I.MEMORY, fill_opacity=0.9, stroke_width=0.8,
                                    stroke_color="#0E1117").shift(UP * 0.13 * k) for k in range(5)])
            hbm.add(st.move_to(acc.get_center() + np.array([dx, dy, 0])))
        hb = T("stacks of memory beside every AI chip", 18, I.MEMORY).next_to(acc, DOWN, buff=0.55)
        phone_mem = VGroup(viz.phone(1.6, back=True, body=BODY_17),
                           Rectangle(width=0.5, height=0.14, fill_color=I.MEMORY, fill_opacity=0.9, stroke_width=0)
                           ).arrange(DOWN, buff=0.2).shift(RIGHT * 1.2)
        pm = T("the memory in a phone", 18, I.MEMORY).next_to(phone_mem, DOWN, buff=0.15)
        mult = VGroup(TB("5 to 7 times", 40, I.MEMORY), T("rise in memory prices", 22, I.TEXT),
                      T("from January 2025 to August 2026", 20, I.DIM)).arrange(DOWN, buff=0.08).move_to(RIGHT * 4.6)
        src = source("TrendForce via MacRumors, 2026-08-10; Apple Form 10-K FY2026")
        quote = VGroup(T("Apple, fiscal 2026: “The Company is experiencing supply constraints and rising costs ...", 18,
                         I.TEXT), T("for key components, including advanced semiconductors, memory and storage.”", 18,
                         I.TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "In chapter three, memory was a tenth of the bill: about 52 dollars. Then the world started building "
            "data centres for artificial intelligence. <bookmark mark='a'/> Every AI chip needs stacks of very fast "
            "memory beside it, and those stacks are made by the same three companies that make the memory in your "
            "phone: Samsung, SK hynix and Micron. <bookmark mark='b'/> They shifted production to the far more "
            "profitable AI memory, and the memory left over for phones and computers ran short. <bookmark mark='c'/> "
            "Between the start of 2025 and the summer of 2026, memory prices rose five- to sevenfold, by "
            "TrendForce's count. <bookmark mark='d'/> Apple's annual report, filed this November, says the company "
            "is experiencing supply constraints and rising costs for memory and storage, and expects the trend to "
            "intensify."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(acc), FadeIn(acc_l), LaggedStart(*[FadeIn(h, shift=DOWN * 0.1) for h in hbm],
                                                              lag_ratio=0.2), FadeIn(hb))
            vo.wait_until("b")
            self.play(FadeIn(phone_mem), FadeIn(pm))
            self.play(phone_mem[1].animate.set_opacity(0.25))
            vo.wait_until("c")
            self.play(FadeIn(mult, scale=0.9))
            vo.wait_until("d")
            self.play(FadeIn(quote, shift=UP * 0.1))
        self.clear_scene()

    def bill(self):
        D17, D18 = R["dollar17"], R["dollar18"]
        sc = 4.6 / D18["bom"]
        def col(bom, mem, x, title, price):
            other = Rectangle(width=1.6, height=sc * (bom - mem), fill_color=COL["parts"], fill_opacity=0.85,
                              stroke_width=0)
            m = Rectangle(width=1.6, height=sc * mem, fill_color=I.MEMORY, fill_opacity=0.95, stroke_width=0)
            g = VGroup(other, m).arrange(UP, buff=0).move_to(np.array([x, 0, 0]), aligned_edge=DOWN).shift(DOWN * 2.3)
            lab_m = VGroup(TB(money(mem), 26, I.MEMORY), T(f"memory: {100 * mem / bom:.0f}% of the parts", 17, I.TEXT)
                           ).arrange(DOWN, buff=0.04).next_to(m, RIGHT, buff=0.2)
            lab_t = VGroup(TB(title, 24, I.TEXT), T(f"parts {money(bom)} · price {money(price)}", 18, I.DIM)
                           ).arrange(DOWN, buff=0.06).next_to(g, UP, buff=0.2)
            return VGroup(g, lab_m, lab_t)
        a = col(D17["bom"], D17["memory"], -3.6, "iPhone 17 Pro, 2025", D17["price"])
        b = col(D18["bom"], D18["memory"], 1.4, "iPhone 18 Pro, 2026", D18["price"])
        arrow = Arrow(a[0].get_right() + RIGHT * 1.4, b[0].get_left() + LEFT * 0.1, color=I.DIM, buff=0.1)
        wsj = T(f"(the WSJ's estimate: memory {money(D18['memory_wsj'])}, parts {money(D18['bom_wsj'])})", 17,
                I.DIM).to_edge(DOWN, buff=0.85).shift(RIGHT * 2.6)
        prof = VGroup(T("Apple's profit on one phone, our model:", 20, I.TEXT),
                      TB(f"{money(D17['profit'])}  →  {money(D18['profit'])} to {money(D18['profit_wsj'])}", 24,
                         I.PROFIT)).arrange(DOWN, buff=0.06).to_corner(UL, buff=0.45)
        src = source("TrendForce (parts +38%, memory 10% → 34%) and WSJ via MacRumors, 2026; this film's model")
        with self.voiceover(
            "Here is what that did to the phone. <bookmark mark='a'/> In 2025 the memory and storage in a "
            "256-gigabyte iPhone Pro cost about 52 dollars, a tenth of its parts. <bookmark mark='b'/> For its "
            "successor, the iPhone 18 Pro, TrendForce estimates the parts cost 38 percent more, and memory is now "
            "about a third of them: roughly 240 dollars, almost five times as much. The Wall Street Journal's "
            "estimate is a little lower, about 200. <bookmark mark='c'/> Apple raised the price by 100 dollars, to "
            "1,199. On our model that does not cover the extra cost, and Apple's profit on this phone falls from "
            "about 244 dollars to somewhere between 144 and 190."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(a[2]), GrowFromEdge(a[0], DOWN), FadeIn(a[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(b[2]), GrowFromEdge(b[0], DOWN), FadeIn(b[1]), run_time=1.6)
            self.play(FadeIn(wsj))
            vo.wait_until("c")
            self.play(FadeIn(prof, shift=DOWN * 0.1))
        self.clear_scene()

    def makers(self):
        rows = [("FY2023", get("micron.gm.fy2023"), get("micron.revenue.fy2023")), ("FY2025", get("micron.gm.fy2025"), get("micron.revenue.fy2025")),
                ("FY2026", get("micron.gm.fy2026"), get("micron.revenue.fy2026"))]
        pa = viz.plot_axes((0, 3), (-0.2, 1.0), x_length=5.6, y_length=4.2, yticks=[0, 0.25, 0.5, 0.75],
                           yfmt=lambda v: f"{100 * v:.0f}%", size=16, ylabel="Micron's gross margin"
                           ).shift(LEFT * 3.4 + DOWN * 0.3)
        bars = VGroup()
        for i, (yr, gm, rev) in enumerate(rows):
            p0, p1 = pa.ax.c2p(i + 0.5, 0), pa.ax.c2p(i + 0.5, gm)
            h = p1[1] - p0[1]
            r = Rectangle(width=1.0, height=abs(h), fill_color=I.MEMORY if gm > 0 else I.COST, fill_opacity=0.9,
                          stroke_width=0).move_to(np.array([p0[0], p0[1] + h / 2, 0]))
            lab = VGroup(TB(pct(gm), 22, I.MEMORY), T(f"sales {money_short(rev)}", 15, I.DIM)).arrange(DOWN, buff=0.03)
            lab.next_to(r, UP, buff=0.1) if gm > 0 else lab.next_to(r, RIGHT, buff=0.12)
            xl = T(yr, 16, I.DIM).next_to(pa.ax.c2p(i + 0.5, -0.2), DOWN, buff=0.1)
            bars.add(VGroup(r, lab, xl))
        M = R["memory"]
        per = VGroup(T("What the memory makers keep from one iPhone Pro", 20, I.TEXT),
                     VGroup(TB(money(M["kept17"]), 40, I.MEMORY), T("2025", 18, I.DIM)).arrange(DOWN, buff=0.04),
                     VGroup(TB(money(M["kept18"]), 56, I.MEMORY), T("2026", 18, I.DIM)).arrange(DOWN, buff=0.04))
        per[1:].arrange(RIGHT, buff=0.9)
        per.arrange(DOWN, buff=0.3).move_to(RIGHT * 3.4 + UP * 0.6)
        arr = Arrow(per[1].get_right(), per[2].get_left(), color=I.MEMORY, buff=0.15)
        hy = VGroup(T("SK hynix, Q3 2026:", 20, I.DIM), TB(f"{pct(get('skhynix.opm.q3_2026'))} operating margin", 22,
                    I.MEMORY)).arrange(RIGHT, buff=0.15).next_to(per, DOWN, buff=0.5)
        how = T("memory cost per phone × the makers' gross margin (Micron's)", 15, I.DIM).next_to(hy, DOWN, buff=0.3)
        src = source("Micron Form 10-K FY2023-26; SK hynix 3Q26 results; this film's model")
        with self.voiceover(
            "Where did the money go? To the memory makers. <bookmark mark='a'/> In fiscal 2023, in a glut, Micron "
            "sold memory at a loss. In fiscal 2025 it kept 40 cents of each dollar. In the year to September 2026, "
            "its sales more than tripled, to 133 billion dollars, and it kept 81 cents of each one. <bookmark "
            "mark='b'/> SK hynix reported an operating margin of 80 percent for the third quarter of 2026. <bookmark "
            "mark='c'/> Put that together on one phone. In 2025 the memory makers kept about 21 dollars of gross "
            "profit from an iPhone Pro. In 2026, about 197: as much as Apple itself, on our model, for the "
            "cheapest Pro."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.6), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(hy))
            vo.wait_until("c")
            self.play(FadeIn(per[0]), FadeIn(per[1]))
            self.play(GrowArrow(arr), FadeIn(per[2], scale=0.8), FadeIn(how))
        self.clear_scene()

    def samsung(self):
        fx = get("fx.krw.2026")
        ds, mx, mx0 = get("samsung.ds_op.q3_2026"), get("samsung.mx_op.q3_2026"), get("samsung.mx_op.q3_2025")
        head = VGroup(TB("Samsung Electronics, third quarter of 2026", 28, I.TEXT),
                      T("operating profit, by division", 20, I.DIM)).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.35)
        base = DOWN * 1.2
        sc = 2.1 / ds
        chip = Rectangle(width=2.2, height=sc * ds, fill_color=I.MEMORY, fill_opacity=0.9, stroke_width=0)
        chip.move_to(base + LEFT * 2.6, aligned_edge=DOWN)
        ph = Rectangle(width=2.2, height=max(sc * abs(mx), 0.05), fill_color=I.COST, fill_opacity=0.95, stroke_width=0)
        ph.move_to(base + RIGHT * 2.6, aligned_edge=UP)
        axis = Line(LEFT * 5, RIGHT * 5, color=I.FAINT).move_to(base)
        lc = VGroup(TB(f"+{ds:.1f} trillion won", 28, I.MEMORY), T(f"about ${ds * 1e3 / fx:.0f} billion", 20, I.DIM),
                    T("chips, mostly memory", 20, I.TEXT)).arrange(DOWN, buff=0.05).next_to(chip, UP, buff=0.15)
        lp = VGroup(T("phones and networks", 20, I.TEXT), TB(f"{mx:.1f} trillion won: a loss", 28, I.COST),
                    T(f"a year earlier: +{mx0:.1f} trillion", 18, I.DIM)).arrange(DOWN, buff=0.05).next_to(ph, DOWN, buff=0.2)
        src = source("Samsung Electronics, Third Quarter 2026 Results, 29 October 2026; FRED won rate (2026 average)")
        with self.voiceover(
            "One company shows both sides of the shock, because it sells memory and it sells phones. <bookmark "
            "mark='a'/> In the third quarter of 2026, Samsung's chip division, mostly memory, made an operating "
            "profit of 106.5 trillion won, about 74 billion dollars, in three months. <bookmark mark='b'/> In the "
            "same quarter its phone and network division lost 0.6 trillion won. A year earlier it had made 3.6 "
            "trillion. Samsung's phones were paying the prices that Samsung's memory was charging."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axis))
            vo.wait_until("a")
            self.play(GrowFromEdge(chip, DOWN), FadeIn(lc), run_time=1.6)
            vo.wait_until("b")
            self.play(GrowFromEdge(ph, UP), FadeIn(lp))
        self.clear_scene()

    def market(self):
        low = VGroup(TB("over 65%", 40, I.MEMORY), T("memory's share of the parts", 20, I.TEXT),
                     T("of a low-end phone (IDC, Q2 2026)", 18, I.DIM)).arrange(DOWN, buff=0.06)
        fall = VGroup(TB("-20%", 40, I.COST), T("smartphones shipped, Q3 2026 on Q3 2025", 20, I.TEXT),
                      T("the weakest third quarter since 2012 (Counterpoint)", 18, I.DIM)).arrange(DOWN, buff=0.06)
        prices = VGroup(TB("+20%", 40, I.MONEY), T("retail prices of smartphones in 2026", 20, I.TEXT),
                        T("(Counterpoint)", 18, I.DIM)).arrange(DOWN, buff=0.06)
        top = VGroup(low, fall, prices).arrange(RIGHT, buff=0.7)
        top.scale_to_fit_width(min(top.width, 12.8)).move_to(UP * 1.4)
        win = VGroup(TB("Pulling away", 24, I.PROFIT), T("Samsung 23% and Apple 22% of Q3 shipments,", 19, I.TEXT),
                     T("both up: they bought memory early, sell dear phones", 19, I.TEXT)).arrange(DOWN, buff=0.06)
        lose = VGroup(TB("Squeezed", 24, I.COST), T("Xiaomi's shipments down more than 30% in Q3;", 19, I.TEXT),
                      T("Transsion's profit for 2025 down by half", 19, I.TEXT)).arrange(DOWN, buff=0.06)
        bot = VGroup(win, lose).arrange(RIGHT, buff=1.2).shift(DOWN * 1.2)
        line = T("The scarce link moved, and every phone maker beneath it paid.", 26, I.ACCENT).to_edge(DOWN, buff=0.45)
        src = source("IDC (2026-08-28); Counterpoint (2026-10-12, preliminary); Transsion 2025 annual report")
        with self.voiceover(
            "For cheap phones it was worse. <bookmark mark='a'/> In a low-end phone, IDC estimates, memory is now "
            "more than 65 percent of the cost of the parts. <bookmark mark='b'/> Phone makers raised prices, by "
            "about 20 percent on average so far this year, according to Counterpoint, and people bought fewer phones: "
            "in the third quarter of 2026, about a fifth fewer than a year before, the weakest third quarter since "
            "2012. <bookmark mark='c'/> Samsung and Apple, which had bought their memory early and sell expensive "
            "phones where memory is a smaller share of the cost, gained share. <bookmark mark='d'/> Makers of "
            "cheaper phones were squeezed: Xiaomi's shipments fell by more than 30 percent in the quarter, and "
            "Transsion's profit for 2025 had already halved. <bookmark mark='e'/> Through most of their history the "
            "memory makers sat in the middle of the margin ladder, and in bad years at the bottom. In 2026 they went "
            "to the top, and everyone beneath them paid."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(low, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(prices, shift=UP * 0.1), FadeIn(fall, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(win, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(lose, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(line))
        self.clear_scene()
