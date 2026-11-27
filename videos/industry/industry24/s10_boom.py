from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403


class Boom(VoiceoverScene):
    def construct(self):
        card(self, 8, "The new boom: power and factories", "Who is building what America is building now?",
             "Chapter eight. The new boom. The strongest construction businesses of the mid-2020s are not the ones "
             "building homes or offices. They wire things.", lit=("change",))
        self.spend()
        self.quanta()
        self.backlog()
        self.margins()

    def spend(self):
        S = R["spending"]
        items = [("factories, 2019", S["manufacturing"][2019], GREY_B, f"${S['manufacturing'][2019]:.0f}bn"),
                 ("factories, 2025", S["manufacturing"][2025], "#B58CFF", f"${S['manufacturing'][2025]:.0f}bn"),
                 ("power, 2019", S["power"][2019], GREY_B, f"${S['power'][2019]:.0f}bn"),
                 ("power, 2025", S["power"][2025], BUILD, f"${S['power'][2025]:.0f}bn")]
        rows = hbars(items, max_value=250, x0=-0.2, top=1.6, row=0.8, length=6.0, size=17, bar_h=0.45)
        lab = tx("American construction spending a year, current dollars", 16, GREY_A).to_edge(UP, buff=0.8)
        src = source("Census Bureau, value of construction put in place, via FRED", size=12)
        beat(self,
             "Start with what is being built. <bookmark mark='a'/> In 2019 America spent "
             f"{S['manufacturing'][2019]:.0f} billion dollars building factories; in 2025, {S['manufacturing'][2025]:.0f} "
             f"billion. <bookmark mark='b'/> On power plants and power lines, {S['power'][2019]:.0f} billion in 2019 and "
             f"{S['power'][2025]:.0f} billion in 2025. Much of that work is wiring, piping and heavy electrical gear: the "
             "kind of work the specialty contractors in this chapter do.",
             base=[rows.axis, lab, src], steps=[rows[:2], rows[2:]])

    def quanta(self):
        C = R["contracts"]
        a, b = C["pwr_q3"]
        items = [("third quarter of 2025", a, GREY_B, f"${a:.2f}bn"), ("third quarter of 2026", b, BUILD, f"${b:.2f}bn")]
        rows = hbars(items, max_value=13, x0=-0.2, top=1.0, row=1.1, length=6.0, size=18, bar_h=0.55)
        lab = tx("Quanta Services' revenue in a quarter", 16, GREY_A).move_to([0, 2.1, 0])
        pylon = draw.pylon(1.8) if hasattr(draw, "pylon") else Square(1)
        pylon.move_to([-5.4, -1.8, 0])
        src = source("Quanta Services, Inc., Form 8-K of 29 October 2026 (Exhibit 99.1)", size=12)
        beat(self,
             "Quanta Services builds and repairs power lines, substations and the electrical systems of large plants "
             "and data centres. <bookmark mark='a'/> In the third quarter of 2025 its revenue was "
             f"{a:.2f} billion dollars. <bookmark mark='b'/> A year later, {b:.2f} billion: up "
             f"{100 * (b / a - 1):.0f} per cent in a year, some of it from businesses it bought. Its own report credits "
             "the demand for electricity from data centres, factories and reshoring.",
             base=[lab, pylon, src], steps=[rows[0], rows[1]])

    def backlog(self):
        C = R["contracts"]
        a, b = C["pwr_backlog"]
        items = [("end of 2025", a, GREY_B, f"${a:.1f}bn"), ("30 September 2026", b, BUILD, f"${b:.1f}bn")]
        rows = hbars(items, max_value=70, x0=-0.2, top=1.0, row=1.1, length=6.0, size=18, bar_h=0.55)
        lab = tx("Quanta's backlog: work won and not yet done", 16, GREY_A).move_to([0, 2.1, 0])
        note = tx(f"about {b / 4 / C['pwr_q3'][1]:.1f} years of work at its current pace", 18, PRICE, bold=True).move_to([0, -1.6, 0])
        tag = estimate_tag("this series' arithmetic: backlog over four times the latest quarter's revenue", size=12)
        src = source("Quanta Services, Inc., Form 10-K for 2025 and Form 8-K of 29 October 2026", size=12)
        beat(self,
             "And the work it has lined up. <bookmark mark='a'/> At the end of 2025 Quanta had "
             f"{a:.1f} billion dollars of work won and not yet done. <bookmark mark='b'/> Nine months later, a record "
             f"{b:.1f} billion. <bookmark mark='c'/> At its current pace that is about {b / 4 / C['pwr_q3'][1]:.1f} "
             f"years of work, {get('pwr.msa'):.0f} per cent of it under master service agreements, standing "
             "arrangements with utilities for a stream of work, rather than one-off tenders.",
             base=[lab, tag, src], steps=[rows[0], rows[1], note])

    def margins(self):
        sec = {}
        from explainer.industry.data.fetch import read
        for r in read("sec_construction"):
            if r["ticker"] in ("FIX", "EME", "STRL") and r.get("revenue") and r.get("profit") is not None:
                sec.setdefault(r["ticker"], {})[int(str(r["year_end"])[:4])] = 100 * r["profit"] / r["revenue"]
        names = {"FIX": "Comfort Systems", "EME": "EMCOR", "STRL": "Sterling"}
        cols = {"FIX": BUILD, "EME": MAKE, "STRL": GOOD}
        series = {names[k]: ({y: v for y, v in sec[k].items() if 2019 <= y <= 2025}, cols[k]) for k in names}
        ch = line_chart(series, x=(2019, 2025), y=(0, 14), xticks=list(range(2019, 2026)), yticks=[0, 2, 4, 6, 8, 10, 12, 14],
                        yfmt=lambda v: f"{v:.0f}%", ylabel="net income per dollar of revenue", width=9.0, height=4.4,
                        center=(-0.9, -0.45), nudge={"Sterling": 0.15, "Comfort Systems": -0.1})
        src = source("Forms 10-K via SEC company facts", size=12)
        f, e, s = sec["FIX"], sec["EME"], sec["STRL"]
        beat(self,
             "And some contractors' margins have widened. <bookmark mark='a'/> Comfort Systems kept "
             f"{f[2019]:.1f} cents of each dollar in 2019 and {f[2025]:.1f} in 2025. EMCOR went from {e[2019]:.1f} to "
             f"{e[2025]:.1f}, and Sterling from {s[2019]:.1f} to {s[2025]:.1f}. In this series' reading, when demand "
             "outruns the supply of skilled crews, the firms that have the crews can charge for them: the same story as "
             "the cranes and the quarries in chapter two.",
             base=[ch.frame, src], steps=[[ch.lines[k] for k in ch.lines] + [ch.labels[k] for k in ch.labels]])
