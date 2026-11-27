from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403

SHORT = {"United States of America": "United States", "United Kingdom": "United Kingdom", "Saudi Arabia": "Saudi Arabia"}


class Budgets(VoiceoverScene):
    def construct(self):
        card(self, 11, "The world's defence budgets", "Who spends, and how fast is it rising?",
             "Chapter eleven. The world's defence budgets: the defence industry's market, country by country.",
             lit=("unit", "change"))
        self.top()
        self.world()
        self.burden()

    def top(self):
        B = R["budgets"]
        top = B["top"]
        order = sorted(top, key=lambda c: -top[c])
        cols = {"United States of America": DEFENCE, "China": BAD, "Russia": BAD, "Ukraine": PRICE}
        items = [(SHORT.get(c, c), top[c], cols.get(c, AIRBUS), f"${top[c]:,.0f}bn") for c in order]
        rows = hbars(items, max_value=950, x0=-2.6, top=2.2, row=0.47, length=7.6, size=15, bar_h=0.32)
        world = B["world"][2025] / 1e3
        us_share = top["United States of America"] / world
        tot = tx(f"the world: ${world / 1e3:.2f} trillion; the United States {100 * us_share:.0f}% of it", 17, PRICE, bold=True).to_edge(DOWN, buff=0.7)
        src = source("SIPRI Military Expenditure Database (2026 release): constant 2024 US$", size=12)
        beat(self,
             "Defence companies sell to governments, so their market is the world's defence budgets. Here they are for "
             "2025, from the Stockholm International Peace Research Institute, in 2024 dollars. "
             f"<bookmark mark='a'/> The United States spent {top['United States of America']:,.0f} billion dollars, "
             f"<bookmark mark='b'/> China about {top['China']:,.0f} billion, Russia {top['Russia']:,.0f}, and then a "
             "cluster of countries spending about sixty to a hundred and ten billion each, Germany at the top of it. "
             f"<bookmark mark='c'/> The world spent {world / 1e3:.2f} trillion dollars, and America "
             f"{100 * us_share:.0f} per cent of it.",
             base=[rows.axis, head("Military spending in 2025, the ten largest"), src],
             steps=[rows[0], VGroup(*rows[1:]), tot])

    def world(self):
        B = R["budgets"]
        w = {y: v / 1e6 for y, v in B["world"].items()}
        ch = line_chart({"the world": (w, PRICE)}, x=(1988, 2025), y=(0, 3.0), xticks=[1990, 2000, 2010, 2020, 2025],
                        yticks=[0, 1, 2, 3], yfmt=lambda v: f"${v:.0f}tn", ylabel="world military spending, constant 2024 US$",
                        width=9.6, height=4.3, center=(-0.6, -0.4), label_end=False)
        ax = ch.ax
        lo = min((y for y in w if y < 2005), key=w.get)
        m_lo = marker(ax, lo, w[lo], f"{lo}: ${w[lo]:.2f}tn", BAD, side=DOWN)
        m_25 = marker(ax, 2025, w[2025], f"2025: ${w[2025]:.2f}tn", GOOD, side=UP)
        g = B["growth"]
        items = [("Ukraine", g["Ukraine"]), ("Russia", g["Russia"]), ("Germany", g["Germany"]), ("China", g["China"]),
                 ("United States", g["United States of America"])]
        fmt = lambda v: "flat" if abs(v) < 0.005 else f"{'+' if v > 0 else '-'}{100 * abs(v):,.0f}%"  # noqa: E731
        chips = VGroup(*[tx(f"{n}: {fmt(v)}", 16, BAD if n in ("Russia", "Ukraine") else GREY_A, bold=True)
                         for n, v in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.4, 0.9, 0])
        chips_h = tx("real growth, 2021-2025", 15, WHITE, bold=True).next_to(chips, UP, buff=0.12).align_to(chips, LEFT)
        src = source("SIPRI Military Expenditure Database: world total and countries, constant 2024 US$", size=12)
        beat(self,
             "Now the world's total since 1988. <bookmark mark='a'/> After the Cold War it fell by nearly a third, to its "
             f"low in {lo}. <bookmark mark='b'/> Then it rose for two decades, and since 2021 it has jumped: "
             f"{w[2025]:.2f} trillion dollars in 2025, the highest in this record. <bookmark mark='c'/> Between 2021 and "
             f"2025, after inflation, Russia's spending rose {100 * g['Russia']:.0f} per cent, Germany's "
             f"{100 * g['Germany']:.0f} and China's {100 * g['China']:.0f}, while America's was flat. Ukraine's rose more "
             "than elevenfold.",
             base=[ch.frame, src], steps=[[ch.lines["the world"], m_lo], m_25, [chips_h, chips]])

    def burden(self):
        B = R["budgets"]
        gd = B["gdp"]
        order = sorted((c for c in gd if gd[c] is not None), key=lambda c: -gd[c])
        items = [(SHORT.get(c, c), 100 * gd[c], BAD if gd[c] > 0.05 else AIRBUS, f"{100 * gd[c]:.1f}%") for c in order]
        rows = hbars(items, max_value=40, x0=-2.6, top=2.2, row=0.47, length=7.6, size=15, bar_h=0.32)
        src = source("SIPRI Military Expenditure Database: military expenditure as a share of GDP, 2025", size=12)
        beat(self,
             "Dollars hide the burden. Here is the same spending as a share of each economy. <bookmark mark='a'/> Ukraine "
             f"spent {100 * gd['Ukraine']:.0f} per cent of its national income on defence in 2025, a country at war. "
             f"<bookmark mark='b'/> Russia spent {100 * gd['Russia']:.1f} per cent and Saudi Arabia "
             f"{100 * gd['Saudi Arabia']:.1f}; America {100 * gd['United States of America']:.1f}; the big European "
             "economies two to two and a half. Where those last numbers go next decides much of the defence industry's next decade.",
             base=[rows.axis, head("Military spending as a share of GDP, 2025"), src],
             steps=[rows[0], VGroup(*rows[1:])])
