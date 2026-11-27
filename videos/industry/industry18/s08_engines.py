from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403


class Engines(VoiceoverScene):
    def construct(self):
        card(self, 7, "Engines: sold at a loss", "Why would anyone sell an engine for less than it costs?",
             "Chapter seven. Engines. The most expensive single part of an airliner, and a business that can sell it for "
             "less than it costs to make.", lit=("unit", "dollar", "moat"))
        self.how()
        self.fleet()
        self.razor()
        self.wrong()

    def how(self):
        eng = draw.turbofan(6.4, ENGINE).move_to([0, 0.3, 0])
        lab = {
            "fan": tx("the fan", 16, ENGINE, bold=True).move_to([-2.6, 2.75, 0]),
            "core": tx("the core: compress, burn, spin the turbine", 16, "#7EC8F5", bold=True).move_to([0.6, -2.4, 0]),
            "bypass": tx("most of the air goes round the core", 16, "#7EC8F5", bold=True).move_to([0.8, 2.75, 0]),
        }
        src = source("General Electric Company (GE Aerospace), Form 10-K 2025", size=12)

        def run(vo):
            for _ in range(3):
                self.play(eng.flame.animate.scale(1.25), rate_func=there_and_back, run_time=0.8)

        beat(self,
             "First, the machine. <bookmark mark='a'/> A modern jet engine is a turbofan. At the front, a huge fan "
             "draws in air. <bookmark mark='b'/> A small part of it goes into the core, where it is squeezed by rows of "
             "compressor blades, burned with fuel, and blasted through a turbine, which turns the fan. "
             "<bookmark mark='c'/> Most of the air never enters the core: the fan pushes it straight round, and that "
             "stream gives most of the thrust. The bigger the fan compared with the core, the less fuel the engine "
             "burns, which is why each new generation of engines looks fatter. It is also why engines run hot and wear: "
             "the blades in the turbine sit in gas hotter than the metal they are made of, and must be inspected and "
             "replaced through decades of flying.",
             base=[src], steps=[[eng.fan, eng[0], eng[1], lab["fan"]], [eng.core, lab["core"]], [eng.bypass, lab["bypass"]]],
             after=run)

    def fleet(self):
        E = R["engines"]
        per = 500
        dots = VGroup()
        for i in range(int(E["base"] / per)):
            r_, c_ = divmod(i, 20)
            dots.add(Dot([-6.2 + 0.32 * c_, 2.0 - 0.32 * r_, 0], radius=0.11, color=ENGINE))
        new = VGroup(*[Dot([-6.2 + 0.32 * c_, -0.9, 0], radius=0.11, color=PRICE) for c_ in range(round(E["engines"] / per))])
        l1 = tx(f"about {E['base']:,} GE commercial engines in service", 16, ENGINE, bold=True).next_to(dots, DOWN, buff=0.2).align_to(dots, LEFT)
        l2 = tx(f"{E['engines']:,} new ones delivered in 2025", 16, PRICE, bold=True).next_to(new, RIGHT, buff=0.3)
        eq = tx(f"new engines: ${E['equipment'] / 1e3:.1f}bn of revenue", 17, GREY_A).move_to([3.7, 1.6, 0])
        sv = tx(f"spare parts and servicing: ${E['services'] / 1e3:.1f}bn", 17, ENGINE, bold=True).move_to([3.7, 1.0, 0])
        pr = tx(f"segment profit: ${E['profit'] / 1e3:.1f}bn ({100 * E['profit'] / (E['equipment'] + E['services']):.1f}%)", 17, GOOD, bold=True).move_to([3.7, 0.4, 0])
        key = tx(f"each dot: {per} engines", 14, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("General Electric Company (GE Aerospace), Form 10-K 2025: Commercial Engines & Services", size=12)
        beat(self,
             "Now the business. GE Aerospace, which sells engines for both Boeing's and Airbus's jets, builds its engine "
             "for single-aisle jets, the LEAP, with France's Safran, in a fifty-fifty company called CFM. <bookmark mark='a'/> GE counts about {E['base']:,} of its commercial "
             f"engines in service around the world. <bookmark mark='b'/> In 2025 it delivered {E['engines']:,} new ones, "
             f"{E['leap']:,} of them LEAPs. The fleet already flying is about twenty times a year's "
             f"new engines. <bookmark mark='c'/> And here is the money: {E['equipment'] / 1e3:.1f} billion dollars from "
             f"selling new engines, <bookmark mark='d'/> {E['services'] / 1e3:.1f} billion from spare parts and servicing "
             f"for the fleet, <bookmark mark='e'/> and a profit of {E['profit'] / 1e3:.1f} billion. GE says that "
             "delivering more new engines held its profit back.",
             base=[key, src], steps=[[dots, l1], [new, l2], eq, sv, pr])

    def razor(self):
        E = R["engines"]
        life = E["life"]
        cum = E["cum"]
        ch = line_chart({"engine": (cum, ENGINE)}, x=(0, 25), y=(-3.5, 1.5), xticks=[0, 5, 10, 14, 20, 25],
                        yticks=[-3, -2, -1, 0, 1], xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"${v:.0f}m",
                        ylabel="one engine's cumulative value to its maker, discounted (the Works)", label_end=False,
                        width=9.6, height=4.2, center=(-0.4, -0.5))
        ax = ch.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(25, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        sale = marker(ax, 0, cum[0], f"sold for ${E['price']:.0f}m, cost ${E['cost']:.0f}m: {cum[0]:.0f}m at once", BAD, side=RIGHT)
        pay = marker(ax, life["payback_years"], cum[life["payback_years"]], f"paid back in year {life['payback_years']}", GOOD, side=DOWN)
        end = marker(ax, 25, cum[25], f"+${cum[25]:.1f}m after {E['years']} years", GOOD, side=DOWN)
        share = VGroup(tx(f"servicing: {100 * life['service_share']:.0f}% of all the money", 16, ENGINE, bold=True),
                       tx("the engine ever brings in", 16, ENGINE, bold=True)).arrange(DOWN, buff=0.05).move_to(ch.ax.c2p(18.5, -2.0))
        tag = estimate_tag(f"the Works: {E['hours']:,.0f} flight hours a year at ${E['per_hour']:.0f} an hour, a 35% service margin, 8% discount", size=12)
        beat(self,
             "Why sell new engines so cheaply? Here is one engine in our model. <bookmark mark='a'/> It costs "
             f"{E['cost']:.0f} million dollars to build and sells for {E['price']:.0f} million, a loss of "
             f"{-cum[0]:.0f} million on the day it is delivered. <bookmark mark='b'/> Then it flies about three thousand "
             "hours a year, and every hour wears it a little. The airline pays its maker for parts and shop visits, by the "
             "hour, for decades. <bookmark mark='c'/> Even discounted at eight per cent a year, the servicing pays back the "
             f"loss in year {life['payback_years']}, <bookmark mark='d'/> and after {E['years']} years the engine is worth "
             f"{cum[25]:.1f} million to its maker. <bookmark mark='e'/> Servicing brings in "
             f"{100 * life['service_share']:.0f} per cent of all the money. Selling the engine cheaply buys twenty-five "
             "years of servicing, and every engine sold today is a customer for decades.",
             base=[ch.frame, zero, tag], steps=[sale, ch.lines["engine"], pay, end, share])

    def wrong(self):
        E = R["engines"]
        ff = draw.fan_face(1.4, ENGINE).move_to([-4.2, 0.4, 0])
        q = quote(["'a rare condition in powder metal used to manufacture certain engine parts requires",
                   "accelerated inspection of the PW1100 GTF fleet, which powers the A320neo family'"],
                  "RTX Corporation (Pratt & Whitney), Form 10-K 2025", size=14, width=7.6).move_to([2.0, 1.4, 0])
        c = stat_cards([(f"${E['gtf']:.1f}bn", "charge against Pratt & Whitney's sales, 2023", BAD),
                        (f"{E['gtf_fleet']:,}+", "aircraft powered by the GTF family", ENGINE)], y=-1.1, size=36, span=8.0)
        c.shift(RIGHT * 2.0)
        src = source("RTX Corporation, Form 10-K 2025", size=12)

        def spin_it(vo):
            draw.spin(ff, speed=2.5)
            self.wait(2.0)
            ff.rotor.clear_updaters()

        beat(self,
             "The deal cuts both ways: the maker that collects for decades also pays for decades when something goes "
             "wrong. <bookmark mark='a'/> In 2023 Pratt and Whitney, part of RTX, found a rare flaw in the powder metal "
             "used for some parts of its geared turbofan, the engine on many A320neos. <bookmark mark='b'/> Engines had "
             f"to come off wings early for inspection. RTX took a charge of {E['gtf']:.1f} billion dollars against its "
             f"sales, and it expected an elevated number of aircraft on the ground through the end of 2026: jets parked "
             "while their engines wait for inspection.",
             base=[ff, src], steps=[q, c], after=spin_it)
