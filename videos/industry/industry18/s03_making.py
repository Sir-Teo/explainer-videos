from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403


class Making(VoiceoverScene):
    def construct(self):
        card(self, 2, "How an airliner is made", "Who builds which piece, and how many a month?",
             "Chapter two. How an airliner is made: who builds which piece, and how many come out of the factory each "
             "month.", lit=("unit", "make"))
        self.pieces()
        self.models()
        self.rates()

    def pieces(self):
        M = R["making"]
        col = BOEING
        fwd = RoundedRectangle(corner_radius=0.25, width=2.0, height=0.62, stroke_width=0, fill_color=col, fill_opacity=0.95)
        mid = Rectangle(width=2.2, height=0.62, stroke_width=0, fill_color=col, fill_opacity=0.85)
        aft = Polygon([-1.0, 0.31, 0], [1.0, 0.31, 0], [1.0, -0.31, 0], [-1.0, -0.12, 0], stroke_width=0, fill_color=col, fill_opacity=0.95)
        fin = Polygon([-0.9, 0.31, 0], [-0.2, 0.31, 0], [-0.7, 1.15, 0], [-1.05, 1.15, 0], stroke_width=0, fill_color=col, fill_opacity=0.9)
        wing = Polygon([-0.4, 0, 0], [0.5, 0, 0], [-0.5, -0.9, 0], [-0.9, -0.9, 0], stroke_width=0, fill_color="#B9C2CF", fill_opacity=1)
        eng = draw.turbofan(1.5, ENGINE)
        # where the pieces end up (an assembled airliner, nose right)
        home = {"aft": np.array([-2.1, 0.2, 0]), "mid": np.array([0.0, 0.2, 0]), "fwd": np.array([2.05, 0.2, 0]),
                "fin": np.array([-2.55, 0.92, 0]), "wing": np.array([-0.2, -0.32, 0]), "eng": np.array([0.45, -0.55, 0])}
        start = {"aft": np.array([-4.6, 2.0, 0]), "mid": np.array([-0.3, 2.3, 0]), "fwd": np.array([4.3, 2.0, 0]),
                 "fin": np.array([-5.4, -1.4, 0]), "wing": np.array([-1.6, -2.3, 0]), "eng": np.array([4.4, -1.8, 0])}
        parts = {"aft": aft, "mid": mid, "fwd": fwd, "fin": fin, "wing": wing, "eng": eng}
        for k, m in parts.items():
            m.move_to(start[k])
        labs = {"fwd": "nose and cockpit", "mid": "fuselage barrels", "aft": "tail section", "fin": "fin and tailplane",
                "wing": "wings", "eng": "engines: GE, Safran's and Pratt & Whitney's"}
        lab = {k: tx(labs[k], 14, GREY_A).next_to(parts[k], DOWN if k in ("fwd", "mid", "aft") else UP, buff=0.12) for k in parts}
        src = source("The Boeing Company, Form 10-K 2025 (suppliers; the Spirit acquisition); Airbus SE, Annual Report 2025",
                     size=12)
        cert = tx("each part is certified with the aircraft: no quick swaps", 16, PRICE, bold=True).move_to([0, -0.2, 0])

        def fly(vo):
            vo.wait_until("c")
            self.play(*[FadeOut(lab[k]) for k in parts], FadeOut(cert), FadeOut(self.beat_ghost), run_time=0.5)
            self.play(*[parts[k].animate.move_to(home[k]) for k in ("aft", "mid", "fwd")], run_time=1.6)
            self.play(*[parts[k].animate.move_to(home[k]) for k in ("fin", "wing", "eng")], run_time=1.4)
            fal = tx("final assembly", 20, PRICE, bold=True).move_to([0, -1.5, 0])
            self.play(FadeIn(fal, shift=UP * 0.1))
            vo.wait_until("d")
            sp = tx(f"Boeing bought Spirit AeroSystems, the 737's fuselage maker, in December 2025: ${M['spirit'] / 1e3:.1f}bn",
                    16, BOEING, bold=True).to_edge(DOWN, buff=0.75)
            self.play(FadeIn(sp))

        beat(self,
             "An airliner is not made in one place. <bookmark mark='a'/> Its fuselage arrives in barrel-shaped sections, "
             "its wings and tail from other plants, its engines from one of a few engine makers, and thousands of smaller "
             "parts from suppliers around the world. Boeing's annual report says many major components are bought from a "
             "single source, and that qualifying a new source of aluminium, titanium or composites can take a year or more. "
             "<bookmark mark='b'/> Each piece is certified with the aircraft, so a supplier cannot simply be swapped. "
             "<bookmark mark='c'/> The pieces meet at a final assembly line, where they are joined, wired and tested, and "
             "the engines hung under the wings. <bookmark mark='d'/> The joins matter. The 737's fuselage came from a "
             "separate company, Spirit AeroSystems. In January 2024 a door plug blew out of a 737-9 in flight, and the FAA's "
             "investigation covered the quality control of both Boeing and Spirit. Boeing agreed to buy Spirit, to run one "
             f"production and quality system, and the deal closed in December 2025 at {M['spirit'] / 1e3:.1f} billion "
             "dollars. Airbus took over the Spirit businesses that made parts for its own jets.",
             base=[src], steps=[[parts[k] for k in parts] + [lab[k] for k in parts], cert], after=fly)

    def models(self):
        M = R["making"]
        names = {"737": ("737", BOEING), "787": ("787 Dreamliner", BOEING), "777": ("777", BOEING), "767": ("767", BOEING),
                 "a320": ("A320 family", AIRBUS), "a220": ("A220", AIRBUS), "a350": ("A350", AIRBUS), "a330": ("A330", AIRBUS)}
        items_b = [(names[m][0], v, BOEING, f"{v:,}") for m, v in M["ba"].items()]
        items_a = [(names[m][0], v, AIRBUS, f"{v:,}") for m, v in M["ab"].items()]
        top = max(v for _, v, _, _ in items_a + items_b)
        hb = hbars(items_b, max_value=top, x0=-3.6, top=1.4, row=0.62, length=2.9, size=16)
        ha = hbars(items_a, max_value=top, x0=3.0, top=1.4, row=0.62, length=2.9, size=16)
        hd = VGroup(tx("Boeing, 2025", 20, BOEING, bold=True).move_to([-2.5, 2.3, 0]),
                    tx("Airbus, 2025", 20, AIRBUS, bold=True).move_to([4.0, 2.3, 0]))
        nb = sum(M["ba"].values())
        single_b = M["ba"]["737"] / nb
        single_a = (M["ab"]["a320"] + M["ab"]["a220"]) / sum(M["ab"].values())
        kinds = VGroup(tx("single aisle: 737, A320 family, A220: short and medium flights", 15, GREY_A),
                       tx("twin aisle: 787, 777, 767, A350, A330: long flights, fewer built", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(DOWN, buff=0.75)
        src = source("The Boeing Company, Form 10-K 2025; Airbus SE, Annual Report 2025: deliveries by model", size=12)
        beat(self,
             "What comes off those lines? Here are 2025's deliveries, model by model. <bookmark mark='a'/> Boeing delivered "
             f"{M['ba']['737']} 737s, {M['ba']['787']} 787 Dreamliners, {M['ba']['777']} 777s and {M['ba']['767']} 767s, "
             "a jet whose line also builds the US Air Force's KC-46 tanker. <bookmark mark='b'/> Airbus delivered "
             f"{M['ab']['a320']} of its A320 family, {M['ab']['a220']} A220s, {M['ab']['a350']} A350s and "
             f"{M['ab']['a330']} A330s. <bookmark mark='c'/> The single-aisle jets dominate: {100 * single_b:.0f} per cent of "
             f"Boeing's deliveries and {100 * single_a:.0f} per cent of Airbus's. They fly short and medium routes; the "
             "bigger twin-aisle jets fly the long ones, cost more each, and are built in far smaller numbers.",
             base=[hd, hb.axis, ha.axis, src], steps=[hb, ha, kinds])

    def rates(self):
        M = R["making"]
        cal = VGroup()
        for i in range(M["rate737"]):
            r_, c_ = divmod(i, 7)
            cal.add(draw.plane(0.55, BOEING, windows=False).move_to([-6.0 + 0.72 * c_, 1.6 - 0.48 * r_, 0]))
        extra = VGroup()
        for i in range(M["rate737"], M["rate47"]):
            r_, c_ = divmod(i, 7)
            extra.add(draw.plane(0.55, PRICE, windows=False).move_to([-6.0 + 0.72 * c_, 1.6 - 0.48 * r_, 0]))
        lb = tx(f"737: {M['rate737']} a month at the end of 2025", 17, BOEING, bold=True).next_to(cal, UP, buff=0.2)
        lb2 = tx(f"rate {M['rate47']} began in 2026, with the FAA's agreement", 15, PRICE, bold=True).next_to(VGroup(cal, extra), DOWN, buff=0.25)
        acal = VGroup()
        for i in range(M["rate320"]):
            r_, c_ = divmod(i, 10)
            acal.add(draw.plane(0.42, AIRBUS, windows=False).move_to([1.2 + 0.52 * c_, 1.6 - 0.42 * r_, 0]))
        la = tx(f"A320 family: aiming for {M['rate320']} a month", 17, AIRBUS, bold=True).next_to(acal, UP, buff=0.2)
        q = quote(["'Due to continued tensions with one engine supplier, the Company expects to reach",
                   "a rate of between 70 and 75 aircraft a month by the end of 2027'"], "Airbus SE, Annual Report 2025",
                  size=13, width=6.2).next_to(acal, DOWN, buff=0.3)
        src = source("The Boeing Company, Form 10-K 2025 and Form 10-Q, third quarter of 2026; Airbus SE, Annual Report 2025",
                     size=12)
        beat(self,
             "The pace of the line is the industry's most watched number. <bookmark mark='a'/> At the end of 2025 Boeing "
             f"was building {M['rate737']} 737s a month, about two every working day, up from fewer than thirty-eight at the "
             "start of the year. Since the door plug, Boeing may raise the 737's rate only with the agreement of the FAA, "
             f"America's air safety regulator. <bookmark mark='b'/> In the spring of 2026 it began moving to {M['rate47']}. "
             "<bookmark mark='c'/> Airbus builds more. It aims to make seventy-five A320s a month, "
             "<bookmark mark='d'/> and says the limit is not its own factories but an engine supplier. The bottleneck in "
             "this industry is often a part that only one company can make.",
             base=[src], steps=[[cal, lb], [extra, lb2], [acal, la], q])
