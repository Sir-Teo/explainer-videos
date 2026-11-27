from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403

NAMES = {"BWA": "BorgWarner", "APTV": "Aptiv", "LEA": "Lear", "ALV": "Autoliv", "GT": "Goodyear", "MGA": "Magna",
         "GM": "General Motors", "F": "Ford", "TM": "Toyota"}
WHAT = {"BWA": "drivetrains", "APTV": "wiring, electronics", "LEA": "seats, wiring", "ALV": "airbags, seat belts",
        "GT": "tyres", "MGA": "bodies, chassis, whole cars"}
SHORT = {"33631": "engines", "33632": "electrical, electronic", "33633": "steering, suspension", "33634": "brakes",
         "33635": "transmissions", "33636": "seats, interiors", "33637": "stampings", "33639": "other parts"}


class Suppliers(VoiceoverScene):
    def construct(self):
        card(self, 7, "The suppliers", "If the carmaker buys most of the car, do its suppliers keep the money?",
             "Chapter seven. The suppliers. If the carmaker buys most of the car, do its suppliers keep the money?",
             lit=("dollar", "moat"))
        self.tiers()
        self.branches()
        self.margins()

    def tiers(self):
        C = R["suppliers"]["census"]
        maker = VGroup(draw.factory(1.6, MAKER), tx("carmakers", 18, MAKER, bold=True)).arrange(DOWN, buff=0.1).move_to([0, 2.1, 0])
        t1 = VGroup(*[VGroup(draw.factory(0.9, SUPPLIER), tx(n, 13, SUPPLIER)).arrange(DOWN, buff=0.05)
                      for n in ("seats", "electronics", "drivetrain", "safety", "body")]).arrange(RIGHT, buff=0.55).move_to([0, 0.15, 0])
        t2 = VGroup(*[VGroup(draw.factory(0.6, "#9AA3B2"), tx(n, 11, GREY_A)).arrange(DOWN, buff=0.04)
                      for n in ("chips", "castings", "foam", "wire", "fasteners", "glass", "rubber")]).arrange(RIGHT, buff=0.42).move_to([0, -1.7, 0])
        lab = VGroup(tx("tier one", 15, SUPPLIER, bold=True).next_to(t1, LEFT, buff=0.4),
                     tx("tier two and materials", 15, GREY_A, bold=True).next_to(t2, LEFT, buff=0.3))
        lines1 = VGroup(*[Line(c.get_top(), maker.get_bottom(), stroke_color=SUPPLIER, stroke_width=1.5, stroke_opacity=0.6) for c in t1])
        lines2 = VGroup(*[Line(c.get_top(), t1[i % 5].get_bottom(), stroke_color=GREY_B, stroke_width=1.2, stroke_opacity=0.5) for i, c in enumerate(t2)])
        stats = VGroup(tx(f"assembly: {C['assembly'][0]:,.0f} companies, {C['assembly'][1]:,.0f} people", 15, MAKER),
                       tx(f"parts: {C['parts'][0]:,.0f} companies, {C['parts'][1]:,.0f} people", 15, SUPPLIER),
                       tx(f"bodies and trailers: {C['bodies'][0]:,.0f} companies, {C['bodies'][1]:,.0f} people", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).to_corner(UR, buff=0.4)
        src = source("US Census Bureau, 2022 Economic Census (NAICS 336110, 3362, 3363)", size=12)
        with self.voiceover(
            "The carmaker sits at the top of a pyramid of suppliers. <bookmark mark='a'/> Below it are the tier-one "
            "suppliers, which sell finished systems straight to the carmaker: seats, wiring and electronics, drivetrains, "
            "airbags, whole sections of body. <bookmark mark='b'/> Below them, tier two and the makers of materials: chips, "
            "castings, foam, wire, glass, rubber. <bookmark mark='c'/> In America, the census of 2022 counted "
            f"{C['assembly'][0]:,.0f} companies assembling vehicles, with {C['assembly'][1]:,.0f} employees, and "
            f"{C['parts'][0]:,.0f} companies making parts, with {C['parts'][1]:,.0f}. Most of the people who make cars do "
            "not work for carmakers."
        ) as vo:
            self.play(FadeIn(maker), FadeIn(src), FadeIn(ghost(t1, t2, opacity=0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in t1], lag_ratio=0.15), Create(lines1), FadeIn(lab[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in t2], lag_ratio=0.1), Create(lines2), FadeIn(lab[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in stats], lag_ratio=0.4))
        self.clear_scene()

    def branches(self):
        B = R["suppliers"]["census"]["branches"]
        items = [(SHORT[c], v[1], SUPPLIER if i % 2 == 0 else "#C98A4B") for i, (c, v) in enumerate(sorted(B.items(), key=lambda kv: -kv[1][1]))]
        tm = viz.treemap([(n, v, col, f"${v:.0f}bn") for n, v, col in items], width=9.6, height=4.6, size=18).move_to([-0.6, -0.4, 0])
        head = tx(f"What America's parts makers shipped in 2022: ${sum(v for _, v, _ in items):.0f}bn", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("US Census Bureau, 2022 Economic Census, motor vehicle parts manufacturing (NAICS 3363 and its branches)", size=12)
        with self.voiceover(
            "What do the parts makers make? <bookmark mark='a'/> The census splits their shipments by kind. The biggest "
            f"single branch is transmissions and the parts that carry power, about {items[0][1]:.0f} billion dollars; then "
            "metal stampings, engines, seats and interiors, electrical and electronic equipment, steering and brakes. "
            "<bookmark mark='b'/> Each box is a business of its own, with its own customers and its own squeeze; and the "
            "engines, gearboxes and exhausts among them have no place in a battery car."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ghost(tm, opacity=0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in tm], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(tm[0], color=PRICE), Indicate(tm[2], color=PRICE))
        self.clear_scene()

    def margins(self):
        S = R["suppliers"]
        sup = sorted(("BWA", "APTV", "LEA", "ALV", "GT", "MGA"), key=lambda k: -S["avg"][k])
        mk = ["TM", "GM", "F"]
        items = [(f"{NAMES[k]} ({WHAT[k]})", S["avg"][k], SUPPLIER) for k in sup] + [(NAMES[k], S["avg"][k], MAKER) for k in mk]
        rows = VGroup()
        for i, (n, v, col) in enumerate(items):
            y = 2.3 - 0.5 * i - (0.3 if i >= len(sup) else 0)
            b = bar(0.6, y, np.sign(v) * max(abs(v) * 55, 0.05), 0.34, col if v > 0 else BAD)
            rows.add(VGroup(tx(n, 15, WHITE).next_to([0.45, y, 0], LEFT, buff=0.0), b,
                            tx(f"{100 * v:.1f}%", 15, col if v > 0 else BAD, bold=True).next_to(b, RIGHT if v > 0 else LEFT, buff=0.1)))
        axis = Line([0.6, 2.6, 0], [0.6, -2.7, 0], stroke_color=GREY_B, stroke_width=2)
        head = tx("Net profit per dollar of revenue, average of 2015-2025", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("SEC company facts: Forms 10-K, 40-F (Magna) and 20-F (Toyota); Toyota's years end in March", size=12)
        a, g, t = S["avg"]["APTV"], S["avg"]["GM"], S["avg"]["TM"]
        with self.voiceover(
            "So do the suppliers keep the money the carmakers pay out? <bookmark mark='a'/> Over the eleven years to 2025, "
            f"the large listed suppliers kept, on average, anything from a loss to about {100 * a:.0f} cents of each "
            f"dollar. Aptiv, the wiring and electronics maker, kept the most; Goodyear, the tyre maker, lost money on "
            f"average. <bookmark mark='b'/> The carmakers did no better and no worse: General Motors {100 * g:.1f} cents, "
            f"Ford {100 * S['avg']['F']:.1f}, Toyota {100 * t:.1f}. <bookmark mark='c'/> Everyone in this chain is thin. "
            "A carmaker buys each part from one of several possible suppliers and can move it to another at the next "
            "model; a supplier with a part nobody else can make, like a chip, has the upper hand, until someone else learns "
            "to make it. Few in the chain own something the buyer cannot get elsewhere."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(head), FadeIn(src), FadeIn(ghost(*[r_[0] for r_ in rows], opacity=0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT if S["avg"][k] > 0 else RIGHT), FadeIn(r_[2]))
                                    for r_, k in zip(rows[:len(sup)], sup)], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows[len(sup):]],
                                  lag_ratio=0.25), run_time=2.0)
        self.clear_scene()
