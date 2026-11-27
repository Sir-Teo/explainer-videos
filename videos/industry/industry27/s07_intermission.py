from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.freight()
        self.oil()
        self.imports()
        self.growth()

    def freight(self):
        E = R["extra"]
        ch = line_chart({"deep-sea freight prices": (E["ppi_long"], RATE)}, x=(1989, 2025), y=(0.5, 4.5),
                        xticks=[1989, 1995, 2000, 2005, 2010, 2015, 2020, 2025], yticks=[1, 2, 3, 4], yfmt=lambda v: f"x{v:.0f}",
                        ylabel="producer prices for deep-sea freight transportation, 1989 = 1", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        k = max(E["ppi_long"], key=E["ppi_long"].get)
        m1 = marker(ch.ax, 2025, E["ppi_long"][2025], f"2025: x{E['ppi_long'][2025]:.1f}", RATE, side=LEFT)
        hd = tx("Intermission: freight, oil and imports", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("BLS, producer price index for deep sea freight transportation (annual averages), via FRED", size=12)
        beat(self,
             "An intermission, and three long views. <bookmark mark='a'/> First, what American shippers pay for deep-sea "
             f"freight, as the Bureau of Labor Statistics measures it: by 2025, {E['ppi_long'][2025]:.1f} times its 1989 level, "
             f"with its highest year in {k}. <bookmark mark='b'/> Cheap is not the same as stable.",
             base=[hd, ch.frame, src], steps=[ch.lines["deep-sea freight prices"], m1])

    def oil(self):
        E = R["extra"]
        b = E["brent"]
        ch = line_chart({"Brent crude": (b, FUEL)}, x=(2005, 2026), y=(0, 140), xticks=[2005, 2010, 2015, 2020, 2026],
                        yticks=[0, 40, 80, 120], yfmt=lambda v: f"${v:.0f}", ylabel="Brent crude oil, dollars a barrel (annual average)",
                        width=9.4, height=4.4, center=(-0.6, -0.45), label_end=False)
        m1 = marker(ch.ax, 2026, b[2026], f"2026 so far: ${b[2026]:.0f}", BAD, side=LEFT)
        src = source("EIA, Brent crude oil price (monthly), via FRED; ZIM, Form 20-F for 2025", size=12)
        beat(self,
             "Second, the fuel. In ZIM's words, the price of ships' fuel 'moves in close interdependence with crude oil "
             "prices'. "
             f"<bookmark mark='a'/> Brent averaged about {b[2025]:.0f} dollars a barrel in 2025. <bookmark mark='b'/> In 2026, with "
             f"the Strait of Hormuz all but closed, it averaged {b[2026]:.0f} so far, and {E['brent_now']:.0f} in October.",
             base=[ch.frame, src], steps=[ch.lines["Brent crude"], m1])

    def imports(self):
        E = R["extra"]
        imp = E["imports"]
        ch = line_chart({"goods America imports": (imp, BOX)}, x=(2005, 2026), y=(0, 5), xticks=[2005, 2010, 2015, 2020, 2026],
                        yticks=[0, 1, 2, 3, 4, 5], yfmt=lambda v: f"${v:.0f}tn", ylabel="American imports of goods a year (annual rate)",
                        width=9.4, height=4.4, center=(-0.6, -0.45), label_end=False)
        m1 = marker(ch.ax, 2005, imp[2005], f"2005: ${imp[2005]:.1f}tn", ALL, side=UP)
        m2 = marker(ch.ax, 2026, imp[2026], f"2026: ${imp[2026]:.1f}tn", BOX, side=LEFT)
        src = source("Census Bureau and BEA, imports of goods (balance of payments basis), via FRED", size=12)
        beat(self,
             "And third, what fills the ships into America. <bookmark mark='a'/> In 2005 the country imported "
             f"{imp[2005]:.1f} trillion dollars of goods. <bookmark mark='b'/> In 2026, at the rate so far, "
             f"{imp[2026]:.1f} trillion, {imp[2026] / imp[2005]:.1f} times as much in dollars of each year.",
             base=[ch.frame, src], steps=[[ch.lines["goods America imports"], m1], m2])

    def growth(self):
        P = R["box"]["ports"]
        names = {"Korea, Rep.": "South Korea", "Viet Nam": "Vietnam", "United Arab Emirates": "UAE"}
        keys = ["China", "United States", "Singapore", "Korea, Rep.", "Malaysia", "Viet Nam", "India", "Netherlands"]
        items = [(names.get(k, k), P[k][2010], P[k][2024]) for k in keys if 2010 in P[k] and 2024 in P[k]]
        db = dumbbell(items, x=(0, 320), center=(1.0, -0.4), width=8.6, height=4.6, xticks=[0, 100, 200, 300],
                      xfmt=lambda v: f"{v:.0f}m", size=15)
        lab = tx("container port traffic, million TEU: 2010 (grey) and 2024", 17, GREY_A).to_edge(UP, buff=0.6)
        src = source("World Bank, World Development Indicators: container port traffic", size=12)
        c = {k: (P[k][2010], P[k][2024]) for k in keys}
        beat(self,
             "And where the growth went. <bookmark mark='a'/> China's ports handled "
             f"{c['China'][0]:.0f} million TEU in 2010 and {c['China'][1]:.0f} million in 2024: it added more than twice "
             f"America's entire traffic. <bookmark mark='b'/> Vietnam's grew from {c['Viet Nam'][0]:.0f} to {c['Viet Nam'][1]:.0f} "
             f"million and India's from {c['India'][0]:.0f} to {c['India'][1]:.0f}, as factories spread across Asia, while "
             f"Rotterdam's country, the Netherlands, went from {c['Netherlands'][0]:.0f} to {c['Netherlands'][1]:.0f}.",
             base=[lab, src, db.frame], steps=[VGroup(*db.rows[:1]), VGroup(*db.rows[1:])])
