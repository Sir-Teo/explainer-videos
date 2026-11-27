from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.rents()
        self.owners()
        self.vacancy()
        self.landlord()

    def rents(self):
        P, Rn = R["prices"], R["rent"]
        ch = line_chart({"house prices": (P["cs"], HOUSE), "rents": (Rn["rent"], RENT), "all consumer prices": (P["cpi"], ALL)},
                        x=(2000, 2025), y=(0.8, 3.4), xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[1.0, 1.5, 2.0, 2.5, 3.0],
                        yfmt=lambda v: f"x{v:.1f}", ylabel="2000 = 1", width=9.4, height=4.4, center=(-1.0, -0.45))
        hd = tx("Intermission: renters and owners", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Case-Shiller national index; BLS CPI-U for rent of primary residence and all items; via FRED", size=12)
        beat(self,
             "An intermission, and three pictures of who owns and who rents. <bookmark mark='a'/> First, since 2000 rents "
             f"have risen {Rn['rent'][2025]:.1f} times, faster than prices in general, {P['cpi'][2025]:.1f} times. "
             f"<bookmark mark='b'/> House prices rose {P['cs'][2025]:.1f} times. Owning has got dearer faster than renting.",
             base=[hd, ch.frame, src], steps=[[ch.lines["all consumer prices"], ch.labels["all consumer prices"], ch.lines["rents"], ch.labels["rents"]],
                                              [ch.lines["house prices"], ch.labels["house prices"]]])

    def owners(self):
        O = R["rent"]["own"]
        ch = line_chart({"homeownership": ({y: v for y, v in O.items() if y <= 2025}, HOUSE)}, x=(1965, 2025), y=(60, 72),
                        xticks=[1965, 1975, 1985, 1995, 2005, 2015, 2025], yticks=[60, 63, 66, 69, 72], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="share of American households that own their home", width=9.4, height=4.4, center=(-0.6, -0.45),
                        label_end=False)
        pk = max(O, key=O.get)
        lo = min((y for y in O if y >= 2010), key=O.get)
        m1 = marker(ch.ax, pk, O[pk], f"{pk}: {O[pk]:.1f}%", PRICE, side=UP)
        m2 = marker(ch.ax, lo, O[lo], f"{lo}: {O[lo]:.1f}%", BAD, side=DOWN)
        src = source("Census Bureau, Housing Vacancies and Homeownership survey, via FRED", size=12)
        beat(self,
             "Second, who owns. <bookmark mark='a'/> The share of American households owning their home peaked at "
             f"{O[pk]:.1f} per cent in {pk}, at the height of the easy-credit boom, <bookmark mark='b'/> fell to "
             f"{O[lo]:.1f} per cent by {lo}, and in 2025 was {O[2025]:.1f}: about where it was in the 1980s.",
             base=[ch.frame, src], steps=[[ch.lines["homeownership"], m1], m2])

    def landlord(self):
        T = R["trade"]["Invitation Homes"]
        houses = VGroup(*[draw.house(0.5, color="#C9B8F0") for _ in range(12)]).arrange_in_grid(rows=2, buff=0.18).move_to([-3.4, 0.6, 0])
        c = stat_cards([(f"{R['rent']['invh']:,.0f}", "homes Invitation Homes owns to rent, end of 2025", RENT),
                        (f"{100 * T[2025][1]:.0f}%", "of its 2025 revenue kept as net income", GOOD)], y=0.6, size=38, span=6.4)
        c.shift(RIGHT * 3.2)
        src = source("Invitation Homes Inc., Form 10-K for 2025 and SEC company facts", size=12)
        beat(self,
             "Third, a new kind of owner. <bookmark mark='a'/> Invitation Homes, one of the largest of the companies that buy "
             f"single-family houses to rent out, owned {R['rent']['invh']:,.0f} of them at the end of 2025, a little under "
             f"two thousand square feet each. <bookmark mark='b'/> It kept {100 * T[2025][1]:.0f} cents of each dollar of "
             "rent as profit, more than any homebuilder in this film: an owner's return on houses rather than a builder's "
             "margin on selling them.",
             base=[houses, src], steps=[c[0], c[1]])

    def vacancy(self):
        V = R["rent"]["vacancy"]
        ch = line_chart({"rental vacancy": ({y: v for y, v in V.items() if 1990 <= y <= 2025}, RENT)}, x=(1990, 2025), y=(4, 12),
                        xticks=[1990, 2000, 2009, 2015, 2021, 2025], yticks=[4, 6, 8, 10, 12], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="share of rental homes standing empty", width=9.4, height=4.4, center=(-0.6, -0.45), label_end=False)
        pk = max(V, key=V.get)
        lo = min((y for y in V if y >= 2015), key=V.get)
        m1 = marker(ch.ax, pk, V[pk], f"{pk}: {V[pk]:.1f}%", BAD, side=UP)
        m2 = marker(ch.ax, lo, V[lo], f"{lo}: {V[lo]:.1f}%", GOOD, side=DOWN)
        m3 = marker(ch.ax, 2025, V[2025], f"2025: {V[2025]:.1f}%", RENT, side=UP)
        src = source("Census Bureau, Housing Vacancies and Homeownership survey, via FRED", size=12)
        beat(self,
             f"And how many rentals stand empty. <bookmark mark='a'/> In {pk}, {V[pk]:.1f} per cent of America's rental "
             f"homes were vacant. <bookmark mark='b'/> By {lo}, {V[lo]:.1f} per cent, the tightest on this chart, around the "
             f"time rents rose fastest. <bookmark mark='c'/> In 2025, {V[2025]:.1f} per cent.",
             base=[ch.frame, src], steps=[[ch.lines["rental vacancy"], m1], m2, m3])
