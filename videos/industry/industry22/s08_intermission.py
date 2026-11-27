from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.relative()
        self.adshare()
        self.tobacco()

    def relative(self):
        Hs = R["history"]
        rel = Hs["rel"]
        ch = line_chart({"personal care": ({y: v for y, v in rel["personal care"].items() if y <= 2025}, BRAND),
                         "food at home": ({y: v for y, v in rel["food at home"].items() if y <= 2025}, FOOD)},
                        x=(1990, 2025), y=(0.7, 1.2), xticks=[1990, 2000, 2010, 2020, 2025], yticks=[0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
                        yfmt=lambda v: f"x{v:.1f}", ylabel="consumer prices against all consumer prices, 1990 = 1",
                        width=9.6, height=4.4, center=(-0.8, -0.45))
        one = DashedLine(ch.ax.c2p(1990, 1), ch.ax.c2p(2025, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        hd = tx("Intermission: prices on the shelf", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("BLS, CPI-U: personal care, food at home and all items (NSA), annual averages, via FRED", size=12)
        beat(self,
             f"An intermission, and three pictures. First, the shelf against everything else. <bookmark mark='a'/> Since "
             f"{Hs['base']} the prices of personal care products in America have risen {Hs['x']['personal care']:.1f} times, "
             f"a little less than prices in general, {Hs['cpi_x']:.1f} times. <bookmark mark='b'/> Food bought in shops "
             f"rose {Hs['x']['food at home']:.1f} times, close to the average. The brands' premium over their costs has not "
             "come from prices racing ahead of everyone else's: it is a gap that has held, year after year.",
             base=[hd, ch.frame, one, src], steps=[[ch.lines["personal care"], ch.labels["personal care"]],
                                                   [ch.lines["food at home"], ch.labels["food at home"]]])

    def adshare(self):
        A = R["ads"]
        sh = {y: 100 * v for y, v in A["pg_share"].items()}
        ch = line_chart({"advertising": (sh, ADS)}, x=(2020, 2026), y=(8, 13), xticks=list(range(2020, 2027)),
                        yticks=[8, 9, 10, 11, 12, 13], xfmt=lambda v: f"FY{int(v) % 100:02d}", yfmt=lambda v: f"{v:.0f}%",
                        ylabel="P&G's advertising as a share of its sales", width=9.6, height=4.4, center=(-0.6, -0.45),
                        label_end=False)
        lo = min(sh, key=sh.get)
        m1 = marker(ch.ax, lo, sh[lo], f"FY{lo % 100:02d}: {sh[lo]:.1f}%", GREY_A, side=DOWN)
        m2 = marker(ch.ax, 2026, sh[2026], f"FY26: {sh[2026]:.1f}%", ADS, side=UP)
        src = source("The Procter & Gamble Company, Forms 10-K for fiscal 2020 to 2026: advertising costs and net sales", size=12)
        beat(self,
             "Second, the advertising. <bookmark mark='a'/> P&G's advertising fell to "
             f"{sh[lo]:.1f} per cent of its sales in fiscal {lo}, the year it raised prices most, <bookmark mark='b'/> and "
             f"rose to {sh[2026]:.1f} per cent by fiscal 2026. Once prices stopped rising, the spending on being remembered "
             "went back up.",
             base=[ch.frame, src], steps=[[ch.lines["advertising"], m1], m2])

    def tobacco(self):
        Hs = R["history"]
        rel = Hs["rel"]["tobacco"]
        ch = line_chart({"tobacco": ({y: v for y, v in rel.items() if y <= 2025}, SMOKE)}, x=(1990, 2025), y=(0, 4.5),
                        xticks=[1990, 2000, 2010, 2020, 2025], yticks=[0, 1, 2, 3, 4], yfmt=lambda v: f"x{v:.0f}",
                        ylabel="tobacco prices against all consumer prices, 1990 = 1", width=9.6, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        end = marker(ch.ax, 2025, rel[2025], f"2025: x{rel[2025]:.1f}", SMOKE, side=LEFT)
        src = source("BLS, CPI-U: tobacco and smoking products and all items (NSA), annual averages, via FRED", size=12)
        beat(self,
             "Third, the exception. <bookmark mark='a'/> Tobacco prices in America have risen "
             f"{Hs['x']['tobacco']:.0f} times since {Hs['base']}, against {Hs['cpi_x']:.1f} for everything; "
             f"<bookmark mark='b'/> against all prices, cigarettes cost {rel[2025]:.1f} times what they did. Taxes are "
             "part of that, since the index counts the price the smoker pays. The rest is the makers' own pricing, and the "
             "next chapter shows how they get away with it.",
             base=[ch.frame, src], steps=[ch.lines["tobacco"], end])
