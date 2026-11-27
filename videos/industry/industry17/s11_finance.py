from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403


class Finance(VoiceoverScene):
    def construct(self):
        card(self, 9, "A bank attached to a factory", "Why does every big carmaker own a lender?",
             "Chapter nine. A bank attached to a factory. Why does every big carmaker own a lender?", lit=("dollar", "moat"))
        self.arms()
        self.loan()
        self.lease()

    def arms(self):
        F = R["finance"]
        rows = [("General Motors", [("North America, making cars", F["gmna"] / 1e3, MAKER), ("GM Financial", F["gmf"] / 1e3, FINANCE)], "$bn, 2025"),
                ("Ford", [("Ford Blue", F["blue"] / 1e3, MAKER), ("Ford Pro", F["pro"] / 1e3, MAKER), ("Model e", F["model_e"] / 1e3, BAD),
                          ("Ford Credit", F["credit"] / 1e3, FINANCE)], "$bn, 2025"),
                ("Toyota", [("cars", F["tm"][1] / 1e3, MAKER), ("financial services", F["tm"][0] / 1e3, FINANCE)], "yen trillion, year to March 2026"),
                ("Honda", [("cars", F["hmc"][1] / 1e3, BAD), ("motorcycles", F["hmc"][2] / 1e3, PRICE), ("financial services", F["hmc"][0] / 1e3, FINANCE)],
                 "yen trillion, year to March 2026")]
        g = VGroup()
        y = 2.5
        for name, items, unit in rows:
            hdr = VGroup(tx(name, 18, WHITE, bold=True), tx(unit, 13, GREY_B)).arrange(RIGHT, buff=0.2).move_to([-6.6, y, 0], aligned_edge=LEFT)
            grp = VGroup(hdr)
            y -= 0.38
            for lab, v, col in items:
                sc = 0.55 if "yen" not in unit else 1.9
                b = bar(-0.5, y, v * sc, 0.28, col if v > 0 else BAD)
                grp.add(VGroup(tx(lab, 14, GREY_A).next_to([-3.4, y, 0], LEFT, buff=0.0), b,
                               tx(f"{v:+.2f}" if "yen" in unit else f"{v:+.1f}", 13, col if v > 0 else BAD, bold=True).next_to(b, RIGHT if v > 0 else LEFT, buff=0.08)))
                y -= 0.33
            y -= 0.12
            g.add(grp)
        axis = Line([-0.5, 2.75, 0], [-0.5, y + 0.3, 0], stroke_color=GREY_B, stroke_width=1.5)
        note = tx("operating profit (GM: EBIT-adjusted; GM Financial, Ford Credit: before tax)", 13, GREY_B).to_corner(UR, buff=0.3)
        src = source("GM and Ford, Forms 10-K 2025; Toyota and Honda, Forms 20-F for the year to March 2026", size=12)
        with self.voiceover(
            "Many buyers borrow to buy a car, and the big carmakers own lenders to finance them. "
            f"<bookmark mark='a'/> In 2025 GM Financial earned {F['gmf'] / 1e3:.1f} billion dollars before tax, against "
            f"{F['gmna'] / 1e3:.1f} billion from building and selling cars in North America. <bookmark mark='b'/> Ford "
            f"Credit earned {F['credit'] / 1e3:.1f} billion: almost as much as Ford's whole petrol car business, while its "
            "electric business lost nearly five. <bookmark mark='c'/> Toyota's lending arm made almost a quarter of its "
            "operating profit. <bookmark mark='d'/> And at Honda, in the year its car business lost one point four trillion "
            "yen, its financial services made a profit, and so, handsomely, did its motorcycles."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(note), FadeIn(src), FadeIn(ghost(*[grp[0] for grp in g], opacity=0.35)))
            for mk, grp in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(grp[0]), LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in grp[1:]],
                                                     lag_ratio=0.2), run_time=1.5)
        self.clear_scene()

    def loan(self):
        F = R["finance"]
        rate = {m: v for m, v in F["rate"].items()}
        months = sorted(rate)
        t = lambda m: int(m[:4]) + (int(m[5:7]) - 0.5) / 12  # noqa: E731
        pa = viz.plot_axes([1972, 2027], [0, 18], x_length=6.6, y_length=3.6, xticks=[1980, 2000, 2020],
                           yticks=[0, 5, 10, 15], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}%",
                           ylabel="rate on a 48-month new-car loan at a bank", size=13).move_to([-3.3, -0.6, 0])
        line = poly(pa, [(t(m), rate[m]) for m in months], FINANCE, 2.5)
        lm, lv = F["last_rate"]
        d = Dot(pa.ax.c2p(t(lm), lv), radius=0.09, color=PRICE)
        dl = tx(f"{lv:.2f}% ({lm})", 14, PRICE, bold=True).next_to(d, UP, buff=0.1)
        calc = VGroup(tx(f"a {usd(F['price'])} car, 10% down", 17, WHITE),
                      tx(f"60 months at {lv:.2f}%", 17, WHITE),
                      tx(f"{usd(F['loan'])} a month", 30, PRICE, bold=True),
                      tx(f"{usd(F['loan'] * 60 + F['price'] * 0.1)} paid in all", 16, GREY_A)).arrange(DOWN, buff=0.12).move_to([3.6, 0.3, 0])
        tag = estimate_tag("the payment: the Works' loan arithmetic", size=13)
        src = source("Federal Reserve, G.19 consumer credit: finance rate on 48-month new-car loans at commercial banks (via FRED)", size=12)
        with self.voiceover(
            "Why own a bank? Because to a buyer who borrows, the price of a car is a monthly payment. <bookmark mark='a'/> The "
            "rate on a four-year new-car loan from an American bank was above fifteen per cent in the early 1980s and "
            f"around four to five through most of the 2010s; in {lm[:4]} it was {lv:.1f}. <bookmark mark='b'/> On a {F['price']:,.0f} "
            f"dollar car with a tenth paid down, five years at that rate is about {F['loan']:,.0f} dollars a month. "
            "<bookmark mark='c'/> When a carmaker wants to move cars without cutting the price on the window, its finance "
            "arm can offer a cheaper loan instead. The lender is a sales tool, and in good years a profitable one."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(tag), FadeIn(ghost(line, calc, opacity=0.25)))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.5)
            self.play(GrowFromCenter(d), FadeIn(dl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in calc], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(calc[2], color=PRICE))
        self.clear_scene()

    def lease(self):
        F = R["finance"]
        price = F["price"]
        res = price * 0.58
        col = viz.DollarColumn([("what the car is expected to lose in 3 years: the driver pays it", price - res, FINANCE, ""),
                                ("expected value when it comes back: the lender's risk", res, "#4A3A6A", "the 'residual'")],
                               total=price, height=4.6, width=1.3, label_x=0.9, size=16, fmt=lambda v: usd(v), label_width=6.0).move_to([-2.6, -0.3, 0])
        top = col.top_label(f"a {usd(price)} car on a three-year lease", 18, PRICE)
        hit = VGroup(tx("if used prices are 10% lower", 17, WHITE), tx("when the car comes back:", 17, WHITE),
                     tx(f"{usd(-0.1 * res)} a car", 28, BAD, bold=True), tx("for the lender, not the driver", 15, GREY_A)).arrange(DOWN, buff=0.1).move_to([4.2, -0.3, 0])
        tag = estimate_tag("illustrative: a residual of 58% after 3 years", size=13)
        with self.voiceover(
            "Leasing makes the bank part of the car business in another way. <bookmark mark='a'/> On a three-year lease "
            "the driver pays roughly what the car is expected to lose in value, plus interest. <bookmark mark='b'/> The "
            "lender keeps the rest: a car it must sell second-hand when the lease ends, at whatever used cars are fetching "
            "then. <bookmark mark='c'/> If used prices are ten per cent lower than it assumed, it loses about "
            f"{0.1 * res:,.0f} dollars on every car. So the finance arm earns steadily in good times and carries the "
            "carmaker's risk again in bad ones, when car prices fall and more borrowers stop paying."
        ) as vo:
            self.play(FadeIn(top), FadeIn(tag), FadeIn(ghost(col.slices, opacity=0.3)))
            vo.wait_until("a")
            self.play(FadeIn(col.slices[0]), Create(col.leaders[0]), FadeIn(col.labels[0]))
            vo.wait_until("b")
            self.play(FadeIn(col.slices[1]), Create(col.leaders[1]), FadeIn(col.labels[1]))
            vo.wait_until("c")
            self.play(FadeIn(hit, shift=LEFT * 0.2))
        self.clear_scene()
