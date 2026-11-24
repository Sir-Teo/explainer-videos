from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry8.common import *  # noqa: F403


class Opec(VoiceoverScene):
    def construct(self):
        card(self, 10, "OPEC: a cartel's arithmetic", "Can a group of producers hold the price up, and what does it cost them?",
             "Chapter ten. OPEC: a cartel's arithmetic.", lit=("moat", "change"))
        self.share()
        self.swing()
        self.later()

    def share(self):
        W = R["world"]
        ys = sorted(W["opec_share"])
        pa = viz.plot_axes([1972, 2026], [0, 70], x_length=9.0, y_length=3.8, xticks=[1975, 1985, 1995, 2005, 2015, 2025],
                           yticks=[20, 40, 60], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}%", size=14)
        pa.move_to([0.4, -0.6, 0])
        ln = VMobject(stroke_color=OPEC, stroke_width=4).set_points_as_corners(
            [pa.ax.c2p(y, 100 * W["opec_share"][y]) for y in ys])
        a = tx(f"1973: {100 * W['opec_share'][1973]:.0f}%", 18, OPEC, bold=True).next_to(pa.ax.c2p(1973, 100 * W["opec_share"][1973]), UP, buff=0.1)
        b = tx(f"1985: {100 * W['opec_share'][1985]:.0f}%", 18, OPEC, bold=True).next_to(pa.ax.c2p(1985, 100 * W["opec_share"][1985]), DOWN, buff=0.15)
        c = tx(f"2025: {100 * W['opec_share'][2025]:.0f}%", 18, OPEC, bold=True).next_to(pa.ax.c2p(2025, 100 * W["opec_share"][2025]), UP, buff=0.15)
        head = tx("OPEC's share of the world's crude oil", 20, GREY_A).next_to(pa, UP, buff=0.2).align_to(pa, LEFT)
        src = source("US Energy Information Administration, International Energy Statistics", size=13)
        with self.voiceover(
            "A market where small shortages cause huge price swings invites a cartel: if a few producers hold oil "
            "back, together, the price rises by much more than the barrels they give up. <bookmark mark='a'/> "
            f"OPEC was founded in {get('opec.founded'):.0f}. By 1973 its members produced well over half the world's crude, "
            "<bookmark mark='b'/> and that autumn its Arab members cut supply and embargoed the United States; the "
            "price of a barrel more than doubled within months. <bookmark mark='c'/> But high prices did what high "
            "prices do. Oil from the North Sea, Alaska and Mexico came on, buyers learned to use less, and by 1985 "
            "OPEC's share was down to barely more than a quarter. <bookmark mark='d'/> It has been around a third "
            "ever since."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ln), run_time=3.0)
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(Indicate(a, color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(b))
            vo.wait_until("d")
            self.play(FadeIn(c))
        self.clear_scene()

    def swing(self):
        W = R["world"]
        sw = W["swing"]
        sau = W["saudi"]
        share = W["opec_share"]
        world = dict(zip(W["years"], W["world"]))
        opec = {y: world[y] * share[y] for y in share}
        others80, others85 = opec[1980] - sau[1980], opec[1985] - sau[1985]
        non80, non85 = world[1980] - opec[1980], world[1985] - opec[1985]
        years = list(range(1978, 1991))
        pa = viz.plot_axes([1977.4, 1990.6], [0, 11], x_length=7.4, y_length=4.0, xticks=[1978, 1980, 1982, 1984, 1986, 1988, 1990],
                           yticks=[2, 4, 6, 8, 10], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}m", size=13)
        pa.move_to([-2.4, -0.6, 0])
        bars = VGroup()
        for y in years:
            p0, p1 = pa.ax.c2p(y - 0.35, 0), pa.ax.c2p(y + 0.35, sau[y] / 1000)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=GAS,
                               fill_opacity=0.9).move_to((p0 + p1) / 2))
        head = tx("Saudi Arabia's crude output, million barrels a day", 18, GAS).next_to(pa, UP, buff=0.15).align_to(pa, LEFT)
        facts = VGroup(
            tx(f"1980 to 1985: Saudi output {100 * (sau[1985] / sau[1980] - 1):.0f}%", 18, GAS, bold=True),
            tx(f"the rest of OPEC: {100 * (others85 / others80 - 1):.0f}%", 18, OPEC),
            tx(f"everyone outside OPEC: +{100 * (non85 / non80 - 1):.0f}%", 18, BRENT),
            tx(f"WTI: ${sw['p1981']:.0f} (1981), ${sw['p1985']:.0f} (1985), ${sw['p1986']:.0f} (1986)", 18, PRICE, bold=True),
            tx(f"Saudi crude at WTI's price: ${sw['rev1981']:.0f}bn a year (1981),", 16, GREY_A),
            tx(f"${sw['rev1985']:.0f}bn (1985), ${sw['rev1986']:.0f}bn (1986)", 16, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.2, -0.2, 0])
        src = source("EIA, International Energy Statistics; WTI (FRED); this film's revenue estimate (volume x WTI)",
                     size=13)
        with self.voiceover(
            "The cartel's arithmetic has a catch, and Saudi Arabia found it. <bookmark mark='a'/> To hold the price "
            "up as demand fell and new oil arrived, someone had to cut. Saudi Arabia, the largest producer, became "
            f"the swing producer. Its output fell from {sau[1980] / 1000:.1f} million barrels a day in 1980 to "
            f"{sau[1985] / 1000:.1f} million in 1985: <bookmark mark='b'/> down by two-thirds. <bookmark mark='c'/> "
            "The rest of OPEC cut far less, and producers outside OPEC grew. <bookmark mark='d'/> The price drifted "
            "down anyway, and Saudi Arabia's oil income, at those prices, fell to about a quarter. "
            "<bookmark mark='e'/> At the end of 1985 it stopped cutting and opened the taps. Within months, a barrel "
            f"fell from about {sw['nov85']:.0f} dollars to {sw['jul86']:.0f}. Holding the price up had cost Saudi "
            "Arabia its market share; letting it go cost everyone, including itself, but stopped the bleeding of share. "
            "That is the cartel's problem: each member gains by producing more while the others hold back."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[:8]], lag_ratio=0.2), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(facts[0]))
            vo.wait_until("c")
            self.play(FadeIn(facts[1]), FadeIn(facts[2]))
            vo.wait_until("d")
            self.play(FadeIn(facts[3:]))
            vo.wait_until("e")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[8:]], lag_ratio=0.2), run_time=1.8)
            self.play(Indicate(bars[8], color=WHITE))
        self.clear_scene()

    def later(self):
        W = R["world"]
        sau = W["saudi"]
        cut = get("eia.opec.cut.2020")
        events = VGroup(
            VGroup(tx("2014-2016", 22, OPEC, bold=True),
                   tx("prices halve as shale floods in;", 17, WHITE),
                   tx(f"Saudi output rises, {sau[2014] / 1000:.1f}m to {sau[2016] / 1000:.1f}m b/d", 17, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06),
            VGroup(tx("2016", 22, OPEC, bold=True), tx("OPEC and other producers, Russia the largest,", 17, WHITE),
                   tx("begin to coordinate: 'OPEC+'", 17, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06),
            VGroup(tx("April 2020", 22, OPEC, bold=True), tx(f"OPEC+ agrees to cut {cut:.1f} million barrels a day", 17, WHITE),
                   tx("from May: OPEC's output falls 6.0m b/d in a month", 17, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06),
            VGroup(tx("2026", 22, OPEC, bold=True), tx("war shuts in the Gulf's oil:", 17, WHITE),
                   tx(f"OPEC's liquids fall from {get('eia.steo.opec.2025'):.1f}m to {get('eia.steo.opec.2026'):.1f}m b/d (EIA)", 17, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06))
        events.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0.8, -0.3, 0])
        line = Line(events.get_corner(UL) + LEFT * 0.4 + UP * 0.1, events.get_corner(DL) + LEFT * 0.4, stroke_color=OPEC,
                    stroke_width=3)
        dots = VGroup(*[Dot([line.get_x(), e.get_top()[1] - 0.15, 0], radius=0.08, color=OPEC) for e in events])
        src = source("EIA, International Energy Statistics; EIA, Today in Energy (September 2020); EIA, Short-Term Energy "
                     "Outlook (November 2026)", size=13)
        with self.voiceover(
            "The same dilemma returned. <bookmark mark='a'/> When shale oil flooded the market after 2014, Saudi "
            "Arabia did not cut. It produced more, and the price halved. <bookmark mark='b'/> In 2016 OPEC began "
            "coordinating with other producers, Russia the largest, a group known as OPEC plus. "
            "<bookmark mark='c'/> In April 2020, with the world locked down, OPEC plus agreed the biggest cut in its "
            f"history, {cut:.1f} million barrels a day, and OPEC's own output fell by six million barrels a day in a "
            "single month. <bookmark mark='d'/> And in 2026 it was not a decision but a war that took OPEC's oil off "
            "the market. A cartel can choose to hold back. It cannot choose what happens to the strait."
        ) as vo:
            self.play(FadeIn(src), Create(line))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(dots[k], scale=2), FadeIn(events[k], shift=RIGHT * 0.15))
        self.clear_scene()
