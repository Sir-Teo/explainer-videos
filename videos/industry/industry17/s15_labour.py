from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403


class Labour(VoiceoverScene):
    def construct(self):
        card(self, 13, "Labour", "What do the people on the line cost, and what does a strike cost?",
             "Chapter thirteen. Labour. What do the people on the line cost, and what does a strike cost?",
             lit=("make", "dollar"))
        self.jobs()
        self.strike()

    def jobs(self):
        L = R["labour"]
        j = {y: v for y, v in L["jobs"].items() if y <= 2025}
        pa = viz.plot_axes([1990, 2026], [0, 1500], x_length=9.6, y_length=4.4, xticks=[1990, 2000, 2010, 2020, 2025],
                           yticks=[0, 500, 1000, 1500], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v / 1000:g}m",
                           ylabel="people employed making motor vehicles and parts in the US", size=13).move_to([-0.6, -0.5, 0])
        line = poly(pa, sorted(j.items()), MAKER, 4)
        pk, lo = L["peak"], L["low"]
        dp = Dot(pa.ax.c2p(pk, j[pk]), radius=0.09, color=GOOD)
        lp = tx(f"{pk}: {j[pk] / 1e3:.2f} million", 15, GOOD, bold=True).next_to(dp, UP, buff=0.1)
        dl = Dot(pa.ax.c2p(lo, j[lo]), radius=0.09, color=BAD)
        ll = tx(f"{lo}: {j[lo]:,.0f} thousand", 15, BAD, bold=True).next_to(dl, DOWN, buff=0.1)
        d25 = Dot(pa.ax.c2p(2025, j[2025]), radius=0.09, color=PRICE)
        l25 = tx(f"2025: {j[2025]:,.0f} thousand", 15, PRICE, bold=True).next_to(d25, UP, buff=0.1).shift(LEFT * 0.4)
        a, p_, d = L["census"]
        split = VGroup(tx("in 2022 (Census):", 15, GREY_A), tx(f"assembly {a:,.0f}", 15, MAKER), tx(f"parts {p_:,.0f}", 15, SUPPLIER),
                       tx(f"new-car dealers {d:,.0f}", 15, DEALER)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).to_corner(UR, buff=0.4).shift(DOWN * 0.4)
        src = source("BLS, Current Employment Statistics, motor vehicles and parts (via FRED, CES3133600101); US Census Bureau, "
                     "2022 Economic Census", size=12)
        with self.voiceover(
            "The car has long been one of America's great employers. <bookmark mark='a'/> In "
            f"{pk} about {j[pk] / 1e3:.1f} million Americans worked making motor vehicles and their parts. "
            f"<bookmark mark='b'/> By {lo}, after the crash, {j[lo]:,.0f} thousand: half the jobs gone in under a decade. "
            f"<bookmark mark='c'/> They have come back part of the way, to about {j[2025]:,.0f} thousand in 2025. "
            "<bookmark mark='d'/> And remember where they are: most in the parts makers, and more again selling and "
            "servicing cars at the dealers."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost(line, opacity=0.3)))
            vo.wait_until("a")
            self.play(Create(line), run_time=3.0)
            self.play(GrowFromCenter(dp), FadeIn(lp))
            vo.wait_until("b")
            self.play(GrowFromCenter(dl), FadeIn(ll))
            vo.wait_until("c")
            self.play(GrowFromCenter(d25), FadeIn(l25))
            vo.wait_until("d")
            self.play(FadeIn(split))
        self.clear_scene()

    def strike(self):
        L = R["labour"]
        st = L["steps"]
        labels = ["Nov 2023", "Sep 2024", "Sep 2025", "Sep 2026", "Sep 2027"]
        level, pts = 1.0, [(0, 1.0)]
        for k, s_ in enumerate(st):
            level *= 1 + s_ / 100
            pts.append((k + 1, level))
        pa = viz.plot_axes([0, 5.4], [0.95, 1.32], x_length=6.2, y_length=3.8, xticks=[1, 2, 3, 4, 5], yticks=[1.0, 1.1, 1.2, 1.3],
                           xfmt=lambda v: labels[int(v) - 1], yfmt=lambda v: f"x{v:.1f}", ylabel="base wage, 2023 = 1", size=12).move_to([-3.2, -0.6, 0])
        steps = VMobject(stroke_color=PRICE, stroke_width=4)
        sp = []
        for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
            sp += [pa.ax.c2p(x0, y0), pa.ax.c2p(x1, y0), pa.ax.c2p(x1, y1)]
        sp.append(pa.ax.c2p(5.4, pts[-1][1]))
        steps.set_points_as_corners(sp)
        tot = tx(f"+{100 * L['wage']:.0f}% by 2027", 20, PRICE, bold=True).next_to(pa.ax.c2p(5, pts[-1][1]), UL, buff=0.1)
        st_ = VGroup(tx("The 2023 strike, as GM counted it:", 17, WHITE, bold=True),
                     tx(f"${L['strike'][0]:.1f}bn off North American EBIT", 18, BAD, bold=True),
                     tx(f"${L['strike'][1]:.1f}bn off net income", 18, BAD, bold=True),
                     tx(f"plus a ${L['bonus']:,.0f} ratification bonus a worker,", 15, GREY_A),
                     tx("a cost-of-living allowance restored,", 15, GREY_A), tx("the contract running to April 2028", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.7, 0.4, 0])
        pay = 100 * R["dollar"]["pay_share"]
        calc = VGroup(tx(f"Payroll was {pay:.1f} cents of each dollar a car plant shipped (Census, 2022);", 14, GREY_A),
                      tx(f"a {100 * L['wage']:.0f}% raise on it is about {pay * L['wage']:.1f} cents.", 14, PRICE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([3.7, -2.2, 0])
        src = source("General Motors, Form 10-K 2023 (the strike's impact and the Labor Agreement's terms); Ford, Form 10-K 2023", size=12)
        tag = estimate_tag("the compounded raise and the payroll share: this film's arithmetic", size=12)
        with self.voiceover(
            "In September 2023 the United Auto Workers union went on strike at plants of General Motors, Ford and other "
            "makers. <bookmark mark='a'/> General Motors later estimated what the weeks of lost "
            f"production cost it: about {L['strike'][0]:.1f} billion dollars of North American operating profit. "
            f"<bookmark mark='b'/> The new contract, which Ford says covers about {L['ford_uaw']:,.0f} of its American "
            f"workers, raised base wages by {st[0]:.0f} per cent at once, {st[1]:.0f} per cent in each of the next three "
            f"Septembers and {st[4]:.0f} per cent in 2027: {100 * L['wage']:.0f} per cent in all, compounded. "
            "<bookmark mark='c'/> That sounds ruinous, but remember the dollar of chapter three: the assembly plants' "
            f"payroll was under five cents of each dollar they shipped, so the raise adds about "
            f"{pay * L['wage']:.1f} cents. What made the strike expensive was not the wages. It was the idle plants, "
            "whose fixed costs ran on while nothing was built."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(tag), FadeIn(ghost(steps, st_[0], opacity=0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in st_[:3]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(steps), run_time=2.5)
            self.play(FadeIn(tot), LaggedStart(*[FadeIn(s_) for s_ in st_[3:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(calc))
        self.clear_scene()
