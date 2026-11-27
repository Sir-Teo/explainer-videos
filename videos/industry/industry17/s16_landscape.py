from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403

OFFSET = {"Toyota": UP, "Volkswagen": DOWN, "Stellantis": UP, "Honda": DOWN, "BYD": UP, "GM": UP, "Ford": DOWN,
          "Tesla": UP, "Rivian": RIGHT, "Lucid": RIGHT, "Ferrari": UP, "NIO": RIGHT, "Li Auto": DOWN, "XPeng": LEFT,
          "Magna": UP, "Aptiv": DOWN, "Lear": UP, "BorgWarner": LEFT, "Autoliv": UP, "Goodyear": DOWN, "AutoNation": RIGHT,
          "Lithia": UP, "Penske": UP, "CarMax": DOWN, "Carvana": UP}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 14, "The landscape, November 2026", "Who makes the world's cars, and who keeps anything?",
             "Chapter fourteen. The landscape, as of November 2026. Who makes the world's cars, and who keeps anything?",
             lit=("moat", "change"))
        self.scatter()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]
        lx = lambda v: np.log10(v)  # noqa: E731
        pa = viz.plot_axes([0, 2.7], [-0.25, 0.25], x_length=10.0, y_length=5.0, xticks=[0, 1, 2],
                           yticks=[-0.2, -0.1, 0, 0.1, 0.2], xfmt=lambda v: {0: "$1bn", 1: "$10bn", 2: "$100bn"}[int(v)],
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net profit per dollar of revenue, latest year", size=13).move_to([-0.3, -0.45, 0])
        pa.add(xlab(pa, "revenue, latest year (log scale)"))
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(2.7, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        dots = {}
        for c in C:
            m = max(min(c["margin"], 0.24), -0.24)
            col = GROUP_COL[c["group"]]
            d = Dot(pa.ax.c2p(lx(c["rev"]), m), radius=0.05 + 0.03 * np.sqrt(c["rev"] / 10), color=col, fill_opacity=0.85)
            name = c["name"] + (" (off scale)" if m != c["margin"] else "")
            lab = tx(name, 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            dots.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        key = VGroup(*[VGroup(Dot(radius=0.08, color=GROUP_COL[g]), tx(n, 13, GROUP_COL[g])).arrange(RIGHT, buff=0.08)
                       for g, n in (("volume", "volume makers"), ("premium", "luxury"), ("electric", "electric newcomers"),
                                    ("china", "Chinese makers"), ("supplier", "suppliers"), ("dealer", "dealers"))]).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.95)
        head = tx("The car business, latest year: size against what it kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("SEC filings (10-K, 20-F, 40-F); Volkswagen, Annual Report 2025; BYD, 2025 results (HKEX); converted at the "
                     "Federal Reserve's 2025 average rates", size=12)
        g = {c["name"]: c for c in C}
        with self.voiceover(
            "Here is the industry as its accounts showed it in late 2026, each company placed by its revenue and by what "
            "it kept. <bookmark mark='a'/> The volume makers are huge and thin. Volkswagen and Toyota take in more than "
            "three hundred billion dollars a year each; Toyota kept about eight cents in the dollar, Volkswagen two, and "
            "Stellantis, Ford and Honda lost money. <bookmark mark='b'/> The Chinese makers: BYD, with about "
            f"{g['BYD']['rev']:.0f} billion dollars of revenue, kept {100 * g['BYD']['margin']:.0f} cents; the smaller electric makers listed in New York lost money or "
            "broke even. <bookmark mark='c'/> The electric newcomers in America: Tesla kept four cents, while Rivian lost "
            f"{-100 * g['Rivian']['margin']:.0f} cents on every dollar and Lucid about twice its revenue, so far off this "
            "chart that they sit at its edge. <bookmark mark='d'/> The suppliers and the dealers mostly kept between one "
            "and seven cents; Goodyear lost money. <bookmark mark='e'/> And alone at the "
            f"top, Ferrari: {100 * g['Ferrari']['margin']:.0f} cents in the dollar."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(head), FadeIn(src), FadeIn(key),
                      FadeIn(ghost(*[v for v in dots.values()], opacity=0.2)))
            for mk, grp in zip("abcde", ("volume", "china", "electric", ("supplier", "dealer"), "premium")):
                vo.wait_until(mk)
                gs = grp if isinstance(grp, tuple) else (grp,)
                self.play(*[LaggedStart(*[FadeIn(x) for x in dots[k]], lag_ratio=0.15) for k in gs], run_time=1.5)
        self.clear_scene()

    def map(self):
        cols = [("Volume makers", MAKER, ["Toyota", "Volkswagen", "Hyundai-Kia", "Stellantis", "GM", "Ford", "Honda",
                                          "Renault-Nissan", "Suzuki"]),
                ("Luxury", PRICE, ["BMW", "Mercedes-Benz", "Ferrari", "Porsche"]),
                ("Electric and China", "#E8554E", ["BYD", "Tesla", "Geely", "SAIC", "Chery", "Li Auto", "NIO", "XPeng", "Rivian", "Lucid"]),
                ("India", SUPPLIER, ["Maruti Suzuki", "Tata Motors", "Mahindra"]),
                ("Suppliers", SUPPLIER, ["Bosch", "Denso", "Magna", "ZF", "Aptiv", "Lear", "CATL", "LG Energy Solution"]),
                ("Dealers and lenders", DEALER, ["AutoNation", "Lithia", "Penske", "CarMax", "Carvana", "GM Financial", "Ford Credit", "Ally"])]
        g = VGroup()
        for i, (title, col, names) in enumerate(cols):
            x = -5.6 + 2.25 * i
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 14, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            box.move_to([x, 0.6, 0], aligned_edge=UP).shift(UP * 1.6)
            g.add(box)
        note = tx("Names only where this film has not measured them: Hyundai, BMW, Mercedes, Renault, Nissan, Bosch, Denso, ZF and "
                  "CATL report outside the SEC, and are left for later parts", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        head = tx("The map of the business", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        with self.voiceover(
            "And the map of the business, by role. <bookmark mark='a'/> The volume makers, Japanese, German, Korean, "
            "American and French, each selling millions of cars a year. <bookmark mark='b'/> The luxury makers. "
            "<bookmark mark='c'/> The electric makers, most of them Chinese, with Tesla. <bookmark mark='d'/> India's own "
            "makers. <bookmark mark='e'/> The suppliers, including the battery makers, CATL and LG Energy Solution, which "
            "make the costliest part of an electric car. <bookmark mark='f'/> And the dealers and the lenders. Who keeps "
            "what has been the subject of the whole film."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note), FadeIn(ghost(*[b[0] for b in g], opacity=0.35)))
            for mk, box in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in box], lag_ratio=0.08), run_time=1.2)
        self.clear_scene()
