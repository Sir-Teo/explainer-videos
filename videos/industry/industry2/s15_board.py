from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry2.common import *  # noqa: F403

ROWS = ["Revenue pool", "Value added", "Employment", "Gross margin", "Capital per $ of revenue", "Return on capital",
        "Concentration (top four)", "Cyclicality", "Growth", "Research and development"]


class Board(VoiceoverScene):
    def construct(self):
        card(self, 17, "The Board", "What ten numbers describe any industry?",
             "Chapter seventeen. The Board.", lit=("unit", "moat", "change"))
        io = R["io"]
        top4 = (get("share.apple.units.2025") + get("share.samsung.units.2025") + get("share.xiaomi.units.2025")
                + get("share.vivo.units.2025")) / get("market.units.2025")
        econ = {"Revenue pool": f"${io['output_total']:.1f}tn (2023)", "Value added": f"${R['gdp']:.1f}tn",
                "Employment": f"{R['jobs_total']:.0f}m payroll jobs",
                "Growth": f"+{100 * R['growth']['change']['Gross domestic product']:.0f}% real, 2015-25"}
        phones = {"Gross margin": "11% (Xiaomi) to 37% (Apple)", "Concentration (top four)": f"{100 * top4:.0f}% of units",
                  "Cyclicality": "-20% in Q3 2026", "Growth": "+1.9% units, 2025"}
        col_w = (3.6, 3.4, 3.4, 2.2)
        hdr = VGroup(T("", 18), TB("The whole economy", 19, I.ACCENT), TB("Smartphones (Part 1)", 19, I.ACCENT),
                     TB("Parts 8-56", 19, I.DIM))
        table = VGroup()
        for k, name in enumerate(["", *ROWS]):
            if k == 0:
                cells = hdr
            else:
                cells = VGroup(T(name, 18, I.TEXT), T(econ.get(name, "·"), 18, I.MONEY if name in econ else I.FAINT),
                               T(phones.get(name, "·"), 18, I.PROFIT if name in phones else I.FAINT),
                               T("one column each", 16, I.FAINT))
            x = -6.4
            for c, w in zip(cells, col_w):
                c.move_to(np.array([x, 2.75 - 0.5 * k, 0]), aligned_edge=LEFT)
                if c.width > w - 0.15:
                    c.scale_to_fit_width(w - 0.15)
                x += w
            table.add(cells)
        lines = VGroup(*[Line(np.array([-6.5, 2.5 - 0.5 * k, 0]), np.array([6.3, 2.5 - 0.5 * k, 0]),
                              color=I.EDGE, stroke_width=1) for k in range(len(ROWS) + 1)])
        src = source("BEA; BLS via FRED; IDC; Counterpoint; company filings (the Register, Parts 1 and 2)", size=14)
        with self.voiceover(
            "From here on, every part of this series fills in the same ten numbers for its industry, so that any "
            "two can be compared. We call it the Board. <bookmark mark='a'/> How much money flows through the "
            "industry; the value it adds; how many people it employs; the margin it keeps; how much capital it "
            "needs for each dollar of sales; the return it earns on that capital; how concentrated it is; how hard "
            "it falls in a downturn; how fast it grows; and how much it spends on research. <bookmark mark='b'/> For "
            "the whole economy we have filled four of them in this part: 48 trillion dollars of sales between all "
            "its industries, 31 trillion of value added, 158 million payroll jobs, and 27 percent growth in ten "
            "years after prices. <bookmark mark='c'/> For smartphones, Part one gave us four, and they show how a "
            "column is read. The margin is a range, because in the same industry Xiaomi keeps 11 cents of gross "
            "profit on a dollar of phones and Apple 37. The four biggest brands sell six in ten of the world's phones. "
            "And in the third quarter of 2026, when memory prices soared, shipments fell by a fifth: that is the "
            "cyclicality row, measured as it happened. <bookmark mark='d'/> Each part from eight onward adds a "
            "column, and by Part 56 the Board is a portrait of the whole economy, industry by industry, every "
            "number with its source and its date."
        ) as vo:
            self.play(FadeIn(table[0]), Create(lines), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r[0]) for r in table[1:]], lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[1]) for r in table[1:]], lag_ratio=0.08), run_time=1.4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r[2]) for r in table[1:]], lag_ratio=0.08), run_time=1.4)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r[3]) for r in table[1:]], lag_ratio=0.05), run_time=1.2)
        self.clear_scene()
