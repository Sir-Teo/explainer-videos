from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403


class Brand(VoiceoverScene):
    def construct(self):
        card(self, 6, "The brand's side", "What does the brand own that the assembler does not?",
             "Chapter six. The brand's side.", lit=("moat", "dollar"))
        self.two_businesses()
        self.mix()
        self.profit()

    def two_businesses(self):
        B = R["brand"]
        prod_rev = B["rev"] - B["services"]
        sc = 9.0 / 400
        def bar(y, rev, gp, col, name, sub):
            r_ = Rectangle(width=rev * sc, height=0.8, stroke_width=0, fill_color=col, fill_opacity=0.3).move_to([-5.4, y, 0], aligned_edge=LEFT)
            g_ = Rectangle(width=gp * sc, height=0.8, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to([-5.4, y, 0], aligned_edge=LEFT)
            lab = VGroup(tx(name, 18, WHITE, bold=True), tx(sub, 13, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).next_to(r_, UP, buff=0.1).align_to(r_, LEFT)
            v = tx(f"sales ${rev:.0f}bn; gross margin ${gp:.0f}bn = {100 * gp / rev:.1f}%", 16, col, bold=True).next_to(r_, DOWN, buff=0.1).align_to(r_, LEFT)
            return VGroup(r_, g_, lab, v)
        p = bar(1.3, prod_rev, B["gp_products"], BRAND, "Apple's products", "iPhone, Mac, iPad, wearables: made by partners")
        s_ = bar(-1.7, B["services"], B["gp_services"], PRICE, "Apple's services", "the App Store, iCloud, AppleCare, payments, advertising")
        src = source("Apple, Form 10-K FY2026 (net sales by category; gross margin by products and services)", size=13)
        with self.voiceover(
            "What does the brand own? First, the design and the name. <bookmark mark='a'/> In its fiscal 2026 Apple sold "
            f"about ${prod_rev:.0f} billion of devices, and kept {B['gm_products']:.1f} per cent of that as gross margin "
            "after paying for the parts and the assembly. <bookmark mark='b'/> Second, the devices already in people's "
            f"pockets. Selling services to their owners brought in ${B['services']:.0f} billion, at a gross margin of "
            f"{B['gm_services']:.1f} per cent. The phone is sold once; the services are sold every month to everyone who "
            "bought one."
        ) as vo:
            self.play(FadeIn(src), FadeIn(p[2]), FadeIn(s_[2]), FadeIn(ghost(p[0], s_[0], opacity=0.25)))
            vo.wait_until("a")
            self.play(GrowFromEdge(p[0], LEFT), run_time=1.2)
            self.play(GrowFromEdge(p[1], LEFT), FadeIn(p[3]))
            vo.wait_until("b")
            self.play(GrowFromEdge(s_[0], LEFT), run_time=1.0)
            self.play(GrowFromEdge(s_[1], LEFT), FadeIn(s_[3]))
        self.clear_scene()

    def profit(self):
        B = R["brand"]
        C = R["contract"]
        unit = 2.0   # $bn of profit per coin
        n_ap = int(round(B["ni"] / unit))
        n_hh = max(1, int(round(B["hh_ni_usd"] / unit)))
        def stack(n, col, x):
            g = VGroup()
            for k in range(n):
                c = draw.coin(0.16, col)
                r_, c_ = divmod(k, 11)
                c.move_to([x + c_ * 0.37, -2.2 + r_ * 0.37, 0])
                g.add(c)
            return g
        ap = stack(n_ap, BRAND, -6.0)
        hh = stack(n_hh, ASSEMBLER, 2.0)
        la = VGroup(tx("Apple, fiscal 2026", 18, BRAND, bold=True), tx(f"net income ${B['ni']:.0f}bn on ${B['rev']:.0f}bn of sales", 14, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).next_to(ap, UP, buff=0.2).align_to(ap, LEFT)
        lh = VGroup(tx("Hon Hai, 2025", 18, ASSEMBLER, bold=True), tx(f"profit to owners about ${B['hh_ni_usd']:.0f}bn on ${B['hh_rev_usd']:.0f}bn", 14, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).next_to(hh, UP, buff=0.2).align_to(hh, LEFT)
        key = tx(f"each coin: ${unit:.0f} billion of profit", 13, GREY_B).to_edge(DOWN, buff=0.45)
        dep = VGroup(tx("and the assemblers depend on the brands:", 15, GREY_A),
                     tx(f"Hon Hai's largest customer: {100 * R['honhai']['client_e'][1]:.0f}% of revenue", 15, WHITE),
                     tx(f"Jabil's largest customer: {C['jbl_a']:.0f}%", 15, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.9, 2.4, 0])
        src = source("Apple, Form 10-K FY2026; Hon Hai, audited statements 2025, at NT$31.17 to the dollar; Jabil, Form 10-K FY2026", size=13)
        with self.voiceover(
            "Put the two side by side. <bookmark mark='a'/> Apple's profit in its latest year: about "
            f"${B['ni']:.0f} billion. <bookmark mark='b'/> Hon Hai's, the largest of its assemblers: about "
            f"${B['hh_ni_usd']:.0f} billion, on about half Apple's sales. <bookmark mark='c'/> And the dependence runs one "
            f"way. Hon Hai's largest customer brought it {100 * R['honhai']['client_e'][1]:.0f} per cent of its revenue; "
            f"Jabil's, {C['jbl_a']:.0f} per cent. A brand can split its orders between assemblers; an assembler cannot "
            "easily replace a customer that size. That is what Shih's smile measures: not who works hardest, but who can "
            "be replaced."
        ) as vo:
            self.play(FadeIn(src), FadeIn(key), FadeIn(la), FadeIn(lh))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in ap], lag_ratio=0.02), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in hh], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(dep, shift=LEFT * 0.1))
        self.clear_scene()

    def mix(self):
        B = R["brand"]
        G = B["gm_hist"]
        ys = (2024, 2025, 2026)
        pa = viz.plot_axes([2023.6, 2026.4], [30, 80], x_length=5.2, y_length=3.8, xticks=list(ys), yticks=[30, 40, 50, 60, 70, 80],
                           xfmt=lambda v: f"FY{int(v)}", yfmt=lambda v: f"{v:.0f}%", ylabel="Apple's gross margin", size=12).move_to([-3.4, -0.4, 0])
        lp = poly(pa, [(y, G["products"][y]) for y in ys], BRAND, 4)
        ls = poly(pa, [(y, G["services"][y]) for y in ys], PRICE, 4)
        lpl = tx("products", 14, BRAND, bold=True).next_to(pa.ax.c2p(2026, G["products"][2026]), RIGHT, buff=0.1)
        lsl = tx("services", 14, PRICE, bold=True).next_to(pa.ax.c2p(2026, G["services"][2026]), RIGHT, buff=0.1)
        gp, gs = B["gp_products"], B["gp_services"]
        share_rev = B["services"] / B["rev"]
        share_gp = gs / (gp + gs)
        bars = VGroup()
        for i, (name, v, col) in enumerate((("share of sales", share_rev, PRICE), ("share of gross margin", share_gp, PRICE))):
            y = 0.8 - 1.6 * i
            frame = Rectangle(width=4.6, height=0.55, stroke_color=GREY_B, stroke_width=1.5).move_to([3.6, y, 0])
            fill = Rectangle(width=4.6 * v, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(frame).align_to(frame, LEFT)
            lab = tx(f"services: {100 * v:.0f}% of Apple's {name}", 15, WHITE, bold=True).next_to(frame, UP, buff=0.1).align_to(frame, LEFT)
            bars.add(VGroup(frame, fill, lab))
        src = source("Apple, Form 10-K FY2026 (gross margin and gross margin percentage, products and services, FY2024-FY2026)", size=13)
        with self.voiceover(
            "And the second business keeps growing in weight. <bookmark mark='a'/> Apple's products earned a gross margin "
            f"of {G['products'][2024]:.1f} per cent in fiscal 2024 and {G['products'][2026]:.1f} in 2026; its services, "
            f"{G['services'][2024]:.1f}, then {G['services'][2026]:.1f}. <bookmark mark='b'/> Services were "
            f"{100 * share_rev:.0f} per cent of its sales in fiscal 2026, <bookmark mark='c'/> but "
            f"{100 * share_gp:.0f} per cent of its gross margin. The device opens the account; the account keeps paying."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), *[FadeIn(b_[0]) for b_ in bars], *[FadeIn(b_[2]) for b_ in bars])
            vo.wait_until("a")
            self.play(Create(lp), FadeIn(lpl), run_time=1.2)
            self.play(Create(ls), FadeIn(lsl), run_time=1.2)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0][1], LEFT))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[1][1], LEFT))
        self.clear_scene()
