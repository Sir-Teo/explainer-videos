from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403


class Aid(VoiceoverScene):
    def construct(self):
        card(self, 6, "Launch aid and the longest dispute", "Who pays when a new airliner flops?",
             "Chapter six. Launch aid, and one of the longest disputes in the history of world trade. Who pays when a "
             "new airliner flops?", lit=("moat", "change"))
        self.aid()
        self.cases()
        self.peace()

    def aid(self):
        A = R["aid"]
        h, f = A["hit"], A["flop"]
        s = 0.17  # screen units per $bn

        def col(x, parts, l1, l2):
            g, y = VGroup(), 1.5
            for v, c, who in parts:
                r_ = Rectangle(width=1.7, height=v * s, stroke_width=0, fill_color=c, fill_opacity=0.9)
                r_.move_to([x, y - v * s / 2, 0])
                r_.grow = UP
                t = VGroup(tx(who, 13, "#0E1117", bold=True), tx(bn(-v), 13, "#0E1117", bold=True)).arrange(DOWN, buff=0.04).move_to(r_)
                g.add(VGroup(r_, t))
                y -= v * s
            g.add(VGroup(tx(l1, 16, WHITE, bold=True), tx(l2, 14, GREY_A)).arrange(DOWN, buff=0.05).move_to([x, 2.15, 0]))
            return g
        base_line = Line([-6.4, 1.5, 0], [6.4, 1.5, 0], stroke_color=GREY_B, stroke_width=2)
        hit_no = col(-4.8, [(-h["trough"], BOEING, "maker")], "a hit", "no aid: the deepest hole")
        hit_aid = col(-1.6, [(-h["trough_aid"], BOEING, "maker")], "a hit", "with aid")
        flop_no = col(1.6, [(-f["end"], BAD, "maker")], "a flop", "no aid: the final loss")
        flop_aid = col(4.8, [(-f["end_aid"], BAD, "maker"), (A["loan"] - f["repaid"], PRICE, "governments")],
                       "a flop", "with aid")
        note = tx(f"aid: governments lend a third of the ${R['programme']['dev']:.0f}bn development, repaid at $8m per aircraft "
                  "delivered, if any are", 15, GREY_A).to_edge(DOWN, buff=0.7)
        tag = estimate_tag(f"the Works' programme; the flop sells {f['rate']} a year for {f['years']} years", size=12)
        beat(self,
             "For decades Airbus's new models were part-financed by its home governments, France, Germany, Spain and "
             "Britain, through what is called launch aid: loans for developing a new airliner, on what a World Trade "
             "Organization panel later found were non-commercial terms. In our model the loan is repaid out "
             "of each aircraft sold. <bookmark mark='a'/> A successful programme without aid digs a "
             f"hole of {-h['trough']:.0f} billion dollars. <bookmark mark='b'/> With governments lending a third of the "
             f"development, the hole is {-h['trough_aid']:.0f} billion, and the loan is repaid in full from deliveries. "
             f"<bookmark mark='c'/> Now a flop, selling only {f['rate']} a year: without aid the maker ends "
             f"{-f['end']:.0f} billion down. <bookmark mark='d'/> With aid, it loses {-f['end_aid']:.0f} billion and the "
             f"governments lose the {A['loan'] - f['repaid']:.0f} billion that was never repaid. Launch aid does not "
             "only lend money. It moves the risk of a flop from the maker to the taxpayer.",
             base=[base_line, note, tag], steps=[hit_no, hit_aid, flop_no, flop_aid])

    def cases(self):
        A = R["aid"]
        left = VGroup(tx("DS316: the US against Airbus's subsidies", 19, BOEING, bold=True),
                      tx(f"more than {A['instances']} instances over almost forty years", 15, WHITE),
                      tx("launch aid for every model, A300 to A380", 15, WHITE),
                      tx("filed 2004", 15, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-3.4, 1.7, 0])
        right = VGroup(tx("DS353: the EU against Boeing's subsidies", 19, AIRBUS, bold=True),
                       tx(f"alleged: ${A['claim']:.1f}bn, 1989-2006, ${A['nasa']:.1f}bn of it NASA research", 15, WHITE),
                       tx(f"the panel found at least ${A['panel']:.1f}bn, with Washington State's tax breaks", 15, WHITE),
                       tx("filed 2005", 15, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.2, 1.7, 0])
        q = quote(["'Airbus would have been unable to bring to the market the LCA that it launched as and when it did",
                   "but for the specific subsidies it received'"], "WTO panel, DS316 (LCA: large civil aircraft)", size=14,
                  width=11).move_to([0, 0.0, 0])
        bars_ = vbars([("the US may tax EU goods (2019)", A["ds316"] / 1e3, BOEING, f"${A['ds316'] / 1e3:.1f}bn a year"),
                       ("the EU may tax US goods (2020)", A["ds353"] / 1e3, AIRBUS, f"${A['ds353'] / 1e3:.1f}bn a year")],
                      base_y=-2.7, height=1.6, width=1.3, gap=3.4)
        src = source("World Trade Organization, disputes DS316 and DS353: summaries and arbitrators' decisions", size=12)
        beat(self,
             "America objected. <bookmark mark='a'/> In 2004 it took the European Union to the World Trade Organization, "
             f"listing more than {A['instances']} subsidies to Airbus over almost forty years. <bookmark mark='b'/> A year "
             f"later the EU answered with its own case: {A['claim']:.0f} billion dollars of alleged help for Boeing, more "
             "than half of it from NASA research contracts, plus state tax breaks. <bookmark mark='c'/> The panel in "
             "the first case concluded that without the subsidies Airbus could not have brought its jets to market as and "
             "when it did. <bookmark mark='d'/> Each side won its case. After fifteen years of rulings and appeals, arbitrators "
             f"let America put tariffs on {A['ds316'] / 1e3:.1f} billion dollars of European goods a year, and Europe on "
             f"{A['ds353'] / 1e3:.1f} billion of American ones.",
             base=[src], steps=[left, right, q, bars_])

    def peace(self):
        A = R["aid"]
        a = draw.plane(3.0, AIRBUS).move_to([-3.4, 0.6, 0])
        b = draw.plane(3.0, BOEING).move_to([3.4, 0.6, 0]).flip(UP)
        wall = Rectangle(width=0.3, height=2.4, stroke_width=0, fill_color=BAD, fill_opacity=0.8).move_to([0, 0.6, 0])
        wl = tx("tariffs", 15, BAD, bold=True).next_to(wall, UP, buff=0.1)
        ok = tx(f"1 September {A['tariff']}: tariff-free trade in aircraft and parts restored", 18, GOOD, bold=True).move_to([0, -1.4, 0])
        cost = tx(f"Airbus's charge for the tariffs before the agreement: about EUR {A['tariff_charge']:.1f}bn", 15, GREY_A).next_to(ok, DOWN, buff=0.2)
        src = source("Airbus SE, Annual Report 2025 (the US-EU trade agreement)", size=12)

        def lift(vo):
            self.play(FadeOut(wall), FadeOut(wl), a.animate.shift(RIGHT * 1.0), b.animate.shift(LEFT * 1.0), run_time=1.2)

        beat(self,
             "The tariffs became a bargaining chip. <bookmark mark='a'/> In 2025 new American tariffs reached aircraft and "
             f"their parts for some months, and Airbus booked about {A['tariff_charge']:.1f} billion euros of charges for "
             f"them. <bookmark mark='b'/> Then, on 1 September {A['tariff']}, Airbus reports, a US-EU trade agreement "
             "restored tariff-free trade in aircraft and parts. The subsidy fight was never settled by a ruling. Each "
             "side's factories depend on parts from the other's, and both found it cheaper to stop.",
             base=[a, b, wall, wl, src], steps=[cost, ok], after=lift)
