from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403

COL = {"Toyota": MAKER, "Volkswagen": MAKER, "GM": MAKER, "Ford": MAKER, "BYD": "#E8554E", "Tesla": EV,
       "Rivian": EV, "Lucid": EV, "Ferrari": PRICE}


class Scale(VoiceoverScene):
    def construct(self):
        card(self, 4, "Scale and platforms", "Why does a carmaker need to build millions of cars?",
             "Chapter four. Scale and platforms. Why does a carmaker need to build millions of cars?", lit=("make", "moat"))
        self.rnd()
        self.profit()
        self.platform()

    def rnd(self):
        P = R["scale"]["points"]
        lx = lambda u: np.log10(u)  # noqa: E731
        pa = viz.plot_axes([4, 7.1], [2.5, 5.0], x_length=9.4, y_length=4.8, xticks=[4, 5, 6, 7], yticks=[3, 4, 5],
                           xfmt=lambda v: {4: "10,000", 5: "100,000", 6: "1 million", 7: "10 million"}[int(v)],
                           yfmt=lambda v: {3: "$1,000", 4: "$10,000", 5: "$100,000"}[int(v)],
                           xlabel="vehicles sold in the year (log scale)", ylabel="research and development per vehicle (log scale)",
                           size=13).move_to([0.2, -0.4, 0])
        iso = VGroup()
        for tot, lab in ((1e9, "$1bn a year"), (1e10, "$10bn a year")):
            pts = [(x, np.log10(tot) - x) for x in np.linspace(4, 7.1, 30) if 2.5 <= np.log10(tot) - x <= 5.0]
            ln = DashedLine(pa.ax.c2p(*pts[0]), pa.ax.c2p(*pts[-1]), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
            iso.add(VGroup(ln, tx(lab, 13, GREY_B).next_to(pa.ax.c2p(*pts[len(pts) // 2]), UR, buff=0.05)))
        dots = VGroup()
        for name, v in P.items():
            d = Dot(pa.ax.c2p(lx(v["units"]), np.log10(v["rnd_per"])), radius=0.1, color=COL[name])
            side = {"Toyota": DOWN + LEFT * 0.4, "GM": RIGHT, "BYD": DL, "Ford": UL, "Volkswagen": UP, "Tesla": UP,
                    "Rivian": UP, "Lucid": UL, "Ferrari": DR}[name]
            lab = tx(f"{name} ${v['rnd_per']:,.0f}", 14, COL[name], bold=True).next_to(d, side, buff=0.1)
            dots.add(VGroup(d, lab))
        head = tx("Engineering is paid once, and spread over every car", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K and 20-F (SEC): R&D and units; Volkswagen, Annual Report 2025 (R&D 6.7% of revenue); BYD, 2025 "
                     "results; Toyota's R&D for its year to March 2025", size=12)
        new = [k for k in ("Rivian", "Lucid")]
        F = R["profit"]["ferrari"]
        fer = round(F["rev"] * 1e9 / F["units"], -3)
        with self.voiceover(
            "A car has to be designed, tested, crash-tested and certified before the first one is sold, and the bill for "
            "that is the same whether the maker then sells ten thousand or ten million. <bookmark mark='a'/> Here is each "
            "maker's research and development spending in its latest year, divided by the vehicles it sold. The dashed lines "
            "are what one and ten billion dollars a year come to per car. <bookmark mark='b'/> Toyota spread its engineering "
            f"over more than nine million vehicles: about {P['Toyota']['rnd_per']:,.0f} dollars a car. GM, Volkswagen, BYD "
            f"and Ford, one to three thousand. Tesla, {P['Tesla']['rnd_per']:,.0f}, since its research includes its work on "
            "self-driving and robots. <bookmark mark='c'/> Then the newcomers. Rivian spent "
            f"{P['Rivian']['rnd_per']:,.0f} dollars of research for each of the {P['Rivian']['units']:,.0f} vehicles it "
            f"delivered; Lucid, {P['Lucid']['rnd_per']:,.0f} for each of {P['Lucid']['units']:,.0f}. <bookmark mark='d'/> "
            f"Only Ferrari spends like that and does well: its revenue comes to about {fer:,.0f} euros for every car it "
            "ships."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src), FadeIn(ghost(dots, opacity=0.25)))
            vo.wait_until("a")
            self.play(FadeIn(iso))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dots[i]) for i, k in enumerate(P) if k in ("Toyota", "GM", "Volkswagen", "BYD", "Ford", "Tesla")],
                                  lag_ratio=0.25), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(dots[i]) for i, k in enumerate(P) if k in new], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(dots[list(P).index("Ferrari")]))
        self.clear_scene()

    def profit(self):
        P = R["scale"]["points"]
        order = sorted(P, key=lambda k: P[k]["profit_per"])
        rows = VGroup()
        sc = 4.6 / 180_000
        for i, k in enumerate(order):
            v = P[k]["profit_per"]
            y = 2.2 - 0.52 * i
            b = bar(0.6, y, np.sign(v) * max(abs(v) * sc, 0.05), 0.36, GOOD if v > 0 else BAD)
            lab = tx(usd(v), 15, GOOD if v > 0 else BAD, bold=True).next_to(b, RIGHT if v > 0 else LEFT, buff=0.1)
            nm = tx(k, 16, COL[k], bold=True).move_to([0.6 + (-0.25 if v > 0 else 0.25), y, 0],
                                                      aligned_edge=RIGHT if v > 0 else LEFT)
            rows.add(VGroup(nm, b, lab))
        axis = Line([0.6, 2.6, 0], [0.6, -2.6, 0], stroke_color=GREY_B, stroke_width=2)
        head = tx("Net profit per vehicle sold, latest year", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K and 20-F (SEC); Volkswagen, Annual Report 2025; BYD, 2025 results; converted at the Federal "
                     "Reserve's 2025 average rates", size=12)
        big = [k for k in order if abs(P[k]["profit_per"]) > 20_000]
        with self.voiceover(
            "Now divide each company's net profit by the vehicles it sold. <bookmark mark='a'/> The volume makers earn "
            f"hundreds of dollars a car, or a few thousand: Toyota about {P['Toyota']['profit_per']:,.0f}, Tesla "
            f"{P['Tesla']['profit_per']:,.0f}, BYD and Volkswagen under a thousand, GM {P['GM']['profit_per']:,.0f}; Ford "
            f"lost {-P['Ford']['profit_per']:,.0f}. <bookmark mark='b'/> Rivian lost {-P['Rivian']['profit_per']:,.0f} "
            f"dollars on every vehicle it delivered, and Lucid {-P['Lucid']['profit_per']:,.0f}. <bookmark mark='c'/> And "
            f"Ferrari made {P['Ferrari']['profit_per']:,.0f} on each car. Two ways to live in this business: sell millions "
            "of cars at a thin margin, or a few thousand at a fat one. In between, the bill for engineering and tooling "
            "eats you."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(head), FadeIn(src), FadeIn(ghost(*[r_[0] for r_ in rows], opacity=0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for k, r_ in zip(order, rows) if k not in big], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for k, r_ in zip(order, rows) if k in big and P[k]["profit_per"] < 0], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for k, r_ in zip(order, rows) if k in big and P[k]["profit_per"] > 0], lag_ratio=0.4))
        self.clear_scene()

    def platform(self):
        S = R["scale"]
        pl = S["platform"]
        pa = viz.plot_axes([0, 2.1e6], [0, 25_000], x_length=7.4, y_length=4.2, xticks=[0, 0.5e6, 1e6, 1.5e6, 2e6],
                           yticks=[0, 5000, 10000, 15000, 20000, 25000], xfmt=lambda v: f"{v / 1e6:g}m",
                           yfmt=lambda v: f"${v / 1000:.0f}k", xlabel="cars a year built on the platform",
                           ylabel="engineering cost per car", size=13).move_to([-2.2, -0.5, 0])
        xs = np.linspace(50e3, 2.1e6, 80)
        curve = poly(pa, [(x, pl["eng"] * 1e9 / (x * pl["years"])) for x in xs if pl["eng"] * 1e9 / (x * pl["years"]) <= 25_000], PRICE, 4)
        d1 = Dot(pa.ax.c2p(200e3, pl["curve"][200e3]), radius=0.1, color=BAD)
        l1 = tx(f"one model, 200,000 a year: {usd(pl['curve'][200e3])}", 15, BAD, bold=True).next_to(d1, RIGHT, buff=0.15)
        d2 = Dot(pa.ax.c2p(1e6, pl["curve"][1e6]), radius=0.1, color=GOOD)
        l2 = tx(f"five models, 1 million a year: {usd(pl['curve'][1e6])}", 15, GOOD, bold=True).next_to(d2, UP, buff=0.2)
        cars = VGroup(draw.car(1.0, MAKER), draw.suv(1.0, GOOD), draw.pickup(1.1, BAD), draw.suv(0.9, PRICE), draw.car(0.9, EV)).arrange(RIGHT, buff=0.12)
        floor = Rectangle(width=cars.width + 0.3, height=0.12, stroke_width=0, fill_color=GREY_B, fill_opacity=0.8).next_to(cars, DOWN, buff=0.02)
        plat = VGroup(cars, floor, tx("one platform, many models", 15, GREY_A).next_to(floor, DOWN, buff=0.1)).move_to([4.2, 1.6, 0])
        merge = VGroup(tx(f"{S['merger']:.0f}: Fiat Chrysler + PSA = Stellantis", 17, MAKER, bold=True),
                       tx("Jeep, Ram, Dodge, Chrysler, Fiat, Alfa Romeo, Maserati,", 14, GREY_A),
                       tx("Peugeot, Citroen, Opel, DS, Lancia, Abarth", 14, GREY_A),
                       tx(f"{S['stla_ship']:,.0f} thousand vehicles shipped in 2025", 15, MAKER)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([4.2, -1.3, 0])
        tag = estimate_tag(f"the Works' platform: ${pl['eng']:.0f}bn of engineering over {pl['years']} years (illustrative)", size=12)
        src = source("Stellantis, Form 20-F 2025", corner=DL, size=12)
        with self.voiceover(
            "So carmakers share the engineering. <bookmark mark='a'/> A platform is the part of a car that buyers never "
            "see: the floor, the structure that protects them in a crash, the wiring, the electronics. Suppose a new one "
            f"costs {pl['eng']:.0f} billion dollars to engineer and lasts {pl['years']} years. <bookmark mark='b'/> Built "
            f"under one model selling two hundred thousand a year, it costs {pl['curve'][200e3]:,.0f} dollars a car. "
            f"<bookmark mark='c'/> Put five models on it, a million a year, and it costs {pl['curve'][1e6]:,.0f}. "
            "<bookmark mark='d'/> This is why car companies merge. In 2021 Fiat Chrysler and France's PSA became one "
            "company, Stellantis, with more than a dozen brands to spread across fewer platforms. It is also why a newcomer "
            "with one model finds the arithmetic so hard."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(tag), FadeIn(src), FadeIn(ghost(curve, plat, opacity=0.25)))
            vo.wait_until("a")
            self.play(FadeIn(plat))
            self.play(Create(curve), run_time=2.0)
            vo.wait_until("b")
            self.play(GrowFromCenter(d1), FadeIn(l1))
            vo.wait_until("c")
            self.play(GrowFromCenter(d2), FadeIn(l2))
            vo.wait_until("d")
            self.play(FadeIn(merge, shift=UP * 0.1))
        self.clear_scene()
