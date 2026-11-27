from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Day(VoiceoverScene):
    def construct(self):
        card(self, 2, "A ship's day", "What does it cost to move a ship one day, and why do ships sail slowly?",
             "Chapter two. A ship's day. A ship is a fixed cost that burns fuel, and the arithmetic of the two decides how "
             "fast the world's goods move.", lit=("make", "dollar"))
        self.cube()
        self.voyage()
        self.speed()
        self.fuel()

    def cube(self):
        pts = {v: 100 * (v / 20) ** 3 for v in range(10, 25)}
        ch = line_chart({"fuel burned a day": (pts, FUEL)}, x=(10, 24), y=(0, 180), xticks=[10, 12, 14, 16, 18, 20, 22, 24],
                        yticks=[0, 50, 100, 150], xfmt=lambda v: f"{v:.0f} kn", yfmt=lambda v: f"{v:.0f}t",
                        ylabel="the Works: tonnes of fuel a day, by speed in knots", width=8.6, height=4.2, center=(-1.4, -0.45),
                        label_end=False)
        m1 = marker(ch.ax, 20, 100, "20 knots: 100 t a day", BAD, side=LEFT)
        m2 = marker(ch.ax, 16, 100 * 0.8 ** 3, f"16 knots: {100 * 0.8 ** 3:.0f} t", GOOD, side=UP)
        eq = MathTex(r"\text{fuel a day} \propto v^{3} \quad\Rightarrow\quad \text{fuel a mile} \propto v^{2}", font_size=36).to_edge(UP, buff=0.6)
        vessel = draw.ship(2.0).move_to([5.2, -1.6, 0])
        tag = estimate_tag("the Works: a large container ship designed for 20 knots", size=12)
        beat(self,
             "A ship pushing through water needs power that rises with the cube of its speed. <bookmark mark='a'/> In the "
             "Works, a large container ship at twenty knots burns about a hundred tonnes of fuel a day. "
             f"<bookmark mark='b'/> At sixteen knots, a fifth slower, it burns about {100 * 0.8 ** 3:.0f}: half. "
             "<bookmark mark='c'/> Per mile travelled the saving is the square of the speed: slowing down by a fifth cuts "
             "the fuel for each voyage by about a third.",
             base=[ch.frame, vessel, tag], steps=[[ch.lines["fuel burned a day"], m1], m2, eq])

    def voyage(self):
        D = R["day"]
        a, b = D["v20"], D["v16"]
        items = [("fuel, at 20 knots", a["fuel_cost"] / 1e6, FUEL, f"${a['fuel_cost'] / 1e6:.2f}m"),
                 ("the ship's days, at 20 knots", a["ship_cost"] / 1e6, SHIP, f"${a['ship_cost'] / 1e6:.2f}m"),
                 ("fuel, at 16 knots", b["fuel_cost"] / 1e6, FUEL, f"${b['fuel_cost'] / 1e6:.2f}m"),
                 ("the ship's days, at 16 knots", b["ship_cost"] / 1e6, SHIP, f"${b['ship_cost'] / 1e6:.2f}m")]
        rows = hbars(items, max_value=1.6, x0=0.4, top=1.8, row=0.85, length=5.0, size=17, bar_h=0.45)
        t1 = tx(f"20 knots: {a['days']:.0f} days, ${a['total'] / 1e6:.2f}m", 19, BAD, bold=True).move_to([-3.2, -1.9, 0])
        t2 = tx(f"16 knots: {b['days']:.0f} days, ${b['total'] / 1e6:.2f}m", 19, GOOD, bold=True).move_to([3.2, -1.9, 0])
        tag = estimate_tag("the Works: 11,000 miles, fuel at $600 a tonne, the ship's other costs $40,000 a day", size=12)
        beat(self,
             "Now a voyage of eleven thousand miles, roughly Asia to northern Europe. <bookmark mark='a'/> At twenty knots "
             f"it takes {a['days']:.0f} days and burns about {a['fuel_cost'] / 1e6:.2f} million dollars of fuel, "
             "<bookmark mark='b'/> and the ship's other costs, its capital, crew, insurance and repairs, come to "
             f"{a['ship_cost'] / 1e6:.2f} million. <bookmark mark='c'/> At sixteen knots it takes {b['days']:.0f} days and "
             f"burns {b['fuel_cost'] / 1e6:.2f} million of fuel, <bookmark mark='d'/> while the extra days cost "
             f"{b['ship_cost'] / 1e6:.2f} million. In all, {b['total'] / 1e6:.2f} million against {a['total'] / 1e6:.2f}: the "
             "slower voyage is cheaper.",
             base=[rows.axis, tag], steps=[rows[0], rows[1], rows[2], [rows[3], t1, t2]])

    def speed(self):
        D = R["day"]
        ch = line_chart({"the whole voyage": (D["sweep"], ALL), "fuel": (D["fuel_sweep"], FUEL), "the ship's days": (D["ship_sweep"], SHIP)},
                        x=(12, 24), y=(0, 3.2), xticks=[12, 14, 16, 18, 20, 22, 24], yticks=[0, 1, 2, 3],
                        xfmt=lambda v: f"{v:.0f} kn", yfmt=lambda v: f"${v:.0f}m", ylabel="the Works: cost of one voyage, by speed",
                        width=8.8, height=4.2, center=(-1.2, -0.45))
        best = D["best"][600]
        m = marker(ch.ax, best, R["day"]["sweep"][round(round(best * 2) / 2, 1)], f"cheapest: {best:.1f} knots", GOOD, side=UP)
        tag = estimate_tag("the Works: fuel at $600 a tonne", size=12)
        beat(self,
             "Drawn across every speed, <bookmark mark='a'/> the fuel falls steeply as the ship slows and the cost of its "
             f"days rises gently, <bookmark mark='b'/> so the whole voyage is cheapest at about {best:.0f} knots, well below "
             "what the ship was built for. Owners call this slow steaming. It is also a way to absorb surplus ships: a "
             "slower fleet needs more ships to carry the same cargo.",
             base=[ch.frame, tag], steps=[[ch.lines[k] for k in ("fuel", "the ship's days")] + [ch.labels[k] for k in ("fuel", "the ship's days")],
                                          [ch.lines["the whole voyage"], ch.labels["the whole voyage"], m]])

    def fuel(self):
        D = R["day"]
        items = [(f"fuel at ${p}/t", v, FUEL if p >= 600 else GOOD, f"{v:.1f} kn") for p, v in D["best"].items()]
        rows = hbars(items, max_value=20, x0=0.2, top=1.8, row=0.62, length=5.2, size=17, bar_h=0.4)
        lab = tx("the Works: the cheapest speed for the voyage, by the price of fuel", 16, GREY_A).to_edge(UP, buff=0.8)
        q = tx(f"ZIM: fuel and energy were {D['bunker']:.1f}% of its operating costs in 2025", 18, RATE, bold=True).move_to([0, -1.6, 0])
        src = source("ZIM Integrated Shipping Services, Form 20-F for 2025", size=12)
        beat(self,
             "And the dearer the fuel, the slower the ships. <bookmark mark='a'/> In the Works, at three hundred dollars a "
             f"tonne the cheapest speed is about {D['best'][300]:.0f} knots; at nine hundred, about {D['best'][900]:.0f}. "
             f"<bookmark mark='b'/> For a real line it matters: ZIM's fuel and energy were {D['bunker']:.1f} per cent of its "
             "operating costs in 2025, and more than twenty-eight per cent in each of the two years before.",
             base=[lab, src], steps=[VGroup(*rows), q])
