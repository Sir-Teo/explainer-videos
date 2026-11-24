from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry8.common import *  # noqa: F403


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 15, "The landscape, November 2026", "Who is who in oil and gas, and where does the market stand?",
             "Chapter fifteen. The landscape, November 2026.", lit=("unit", "moat", "change"))
        self.map_()
        self.now()

    def map_(self):
        C = R["companies"]

        def net(t):
            v = C[t]["net"].get(2025)
            return f" ${v:.1f}bn" if v is not None else ""
        groups = [
            ("National oil companies", GAS, [f"Saudi Aramco ${get('aramco.net'):.0f}bn", "ADNOC", "Kuwait Petroleum",
                                              "NIOC (Iran)", "Rosneft", "Petrobras", "CNPC / PetroChina", "Sinopec"]),
            ("The majors", BRENT, [f"ExxonMobil{net('XOM')}", f"Chevron{net('CVX')}", "Shell", "BP", "TotalEnergies"]),
            ("Independents and shale", SHALE, [f"ConocoPhillips{net('COP')}", f"EOG Resources{net('EOG')}",
                                               f"Occidental{net('OXY')}", f"Devon{net('DVN')}", "Diamondback"]),
            ("Refiners", COST, [f"Marathon Petroleum{net('MPC')}", f"Valero{net('VLO')}", "Phillips 66", "Reliance"]),
            ("Services", PRICE, [f"SLB{net('SLB')}", f"Halliburton{net('HAL')}", "Baker Hughes"]),
            ("Gas and LNG", "#9AD0F5", [f"Cheniere{net('LNG')}", "QatarEnergy"]),
            ("Traders", GREY_B, ["Vitol", "Trafigura", "Glencore"])]
        cols = VGroup()
        for title, col, names in groups:
            head = tx(title, 19, col, bold=True)
            pills = VGroup(*[pill(n, color=WHITE, size=15, stroke=col) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            cols.add(VGroup(head, pills).arrange(DOWN, aligned_edge=LEFT, buff=0.15))
        top = VGroup(*cols[:4]).arrange(RIGHT, aligned_edge=UP, buff=0.45)
        bot = VGroup(*cols[4:]).arrange(RIGHT, aligned_edge=UP, buff=0.8)
        VGroup(top, bot).arrange(DOWN, buff=0.45).move_to([0, -0.25, 0])
        if top.width > 13.2:
            VGroup(top, bot).scale_to_fit_width(13.2)
        stamp = as_of("net income, 2025, where filed", corner=UR)
        us = [t for t in ("XOM", "CVX", "COP", "EOG", "OXY", "DVN", "MPC", "VLO", "SLB", "HAL", "LNG") if C[t]["net"].get(2025)]
        n_us = len(us)
        assert sum(C[t]["net"][2025] for t in us) < get("aramco.net")
        src = source("Forms 10-K for 2025 (SEC company facts); Saudi Aramco, Annual Report 2025; names from the companies' "
                     "own reports", size=13)
        with self.voiceover(
            "Here is the industry as of November 2026. <bookmark mark='a'/> The national oil companies, owned by "
            f"states, led by Saudi Aramco, which earned more in 2025 than the {n_us} companies on this page that file "
            "their accounts in America, put together. <bookmark mark='b'/> The majors: ExxonMobil and Chevron in America, Shell, BP and "
            "TotalEnergies in Europe, each producing, refining and selling around the world. <bookmark mark='c'/> The "
            "independents, many of them shale drillers in Texas and New Mexico. <bookmark mark='d'/> The refiners, "
            "living on the crack spread. <bookmark mark='e'/> The service companies, living on everyone else's "
            "capital spending. <bookmark mark='f'/> The liquefied gas exporters. <bookmark mark='g'/> And the traders, "
            "private companies most people have never heard of, who buy, store and ship oil and fuel between all the "
            "others."
        ) as vo:
            self.play(FadeIn(src), FadeIn(stamp))
            for k, m in enumerate("abcdefg"):
                vo.wait_until(m)
                self.play(FadeIn(cols[k][0]), LaggedStart(*[FadeIn(p_, shift=UP * 0.1) for p_ in cols[k][1]], lag_ratio=0.1),
                          run_time=1.0)
        self.clear_scene()

    def now(self):
        S = R["shock"]
        rows = [(f"Middle East oil shut in: {get('eia.steo.shutin.peak'):.1f}m b/d at the peak (May)",
                 f"{get('eia.steo.shutin.oct'):.1f}m in October", STATE),
                (f"Brent: ${S['brent_oct']:.0f} in October", "below $100 again on 4 November", PRICE),
                ("Workarounds: Saudi Arabia's pipeline to the Red Sea;", "ship-to-ship transfers off Oman", BRENT),
                (f"Demand in 2026: {S['demand']:+.1f}m b/d", "the oil not used, mostly in China and the Middle East", GAS),
                (f"EIA's forecast: Brent ${S['brent_2027']:.0f} in 2027", "if flows keep recovering", WHITE)]
        g = VGroup()
        for a, b, c in rows:
            g.add(VGroup(tx(a, 20, c, bold=True), tx(b, 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([1.2, -0.3, 0])
        ship = draw.tanker(2.2).move_to([-4.8, 0.6, 0])
        sea = Rectangle(width=3.6, height=0.4, stroke_width=0, fill_color="#123A5C", fill_opacity=1).next_to(ship, DOWN, buff=-0.05)
        stamp = as_of("EIA, 10 November 2026", corner=UR)
        src = source("US Energy Information Administration, Short-Term Energy Outlook, 10 November 2026", size=13)
        with self.voiceover(
            "And the market itself, in November 2026. <bookmark mark='a'/> At the worst of the war, in May, almost "
            "eleven million barrels a day were shut in across the Middle East; by October, two and a half. "
            "<bookmark mark='b'/> Brent averaged a hundred and twenty-four dollars in October, and fell back below a "
            "hundred in early November. <bookmark mark='c'/> Oil has found other ways out of the Gulf: across Saudi "
            "Arabia by pipeline, and from ship to ship along the coast of Oman. <bookmark mark='d'/> The world used "
            "about two million barrels a day less oil this year than last. <bookmark mark='e'/> The Energy Information "
            f"Administration expects Brent to average about {S['brent_2027']:.0f} dollars in 2027, as flows recover "
            "and stocks are rebuilt. That forecast is the one this part will make a call against."
        ) as vo:
            self.play(FadeIn(src), FadeIn(stamp), FadeIn(sea), FadeIn(ship))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(g[k], shift=RIGHT * 0.15))
        self.clear_scene()
