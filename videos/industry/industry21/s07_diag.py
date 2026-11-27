from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class Diag(VoiceoverScene):
    def construct(self):
        card(self, 6, "Diagnostics: the laboratory", "Who earns from a blood test?",
             "Chapter six. Diagnostics. A blood test passes through two businesses: the laboratory that runs it, and the "
             "company that makes the machines and chemicals it runs on.", lit=("dollar", "change"))
        self.lab()
        self.pricevol()
        self.covid()
        self.margins()

    def lab(self):
        D = R["diag"]
        tubes = draw.test_tubes(6, 1.2)
        belt = draw.conveyor(9.0, n=10, item_color=BAD, item=0.22).move_to([0, -1.4, 0])
        tubes.move_to([-4.6, 1.2, 0])
        c = stat_cards([(f"{D['reqs']:.0f} million", "requisitions, 2025", LABS),
                        (f"${D['per_req']:.0f}", "revenue per requisition", PRICE)], y=1.4, size=38, span=7.0).shift(RIGHT * 2.2)
        src = source("Quest Diagnostics Incorporated, Form 10-K 2025", size=12)

        def run(vo):
            draw.run_belt(belt, speed=0.8)
            self.wait(2.0)
            belt.items.clear_updaters()
        beat(self,
             "A laboratory is a factory for tests. <bookmark mark='a'/> Samples arrive by the million, with a form saying "
             "which tests to run and whom to bill: a requisition. <bookmark mark='b'/> Quest handled about "
             f"{D['reqs']:.0f} million of them in 2025, <bookmark mark='c'/> and earned about {D['per_req']:.0f} dollars "
             "on each. A laboratory makes money on volume: running more samples through the same machines.",
             base=[src], steps=[tubes, [belt, c[0]], c[1]], after=run)

    def pricevol(self):
        P = R["pricevol"]
        rows = [["", "revenue per requisition", "requisitions", "of which organic"]] + [
            [str(y), f"{P[y]['rpr']:+.1f}%", f"{P[y]['vol']:+.1f}%", f"{P[y]['org']:+.1f}%"] for y in (2023, 2024, 2025)]
        cols = [None] + [[WHITE, BAD if P[y]["rpr"] < 0 else GREY_A, LABS, GOOD] for y in (2023, 2024, 2025)]
        tb = table(rows, col_x=[-5.6, -3.6, 0.6, 3.6], top=1.4, row_h=0.75, size=19, colors=cols)
        note = tx(f"in 2025, laboratories Quest bought added about {R['pricevol_acq']}% to its revenue", 17, PRICE, bold=True).move_to([0, -1.9, 0])
        src = source("Quest Diagnostics Incorporated, Form 10-K 2025: revenue per requisition and volume", size=12)
        beat(self,
             "And a laboratory does not set its own price: insurers and governments do. <bookmark mark='a'/> Quest's "
             f"revenue per requisition fell {abs(P[2023]['rpr']):.1f} per cent in 2023, <bookmark mark='b'/> rose "
             f"{P[2024]['rpr']:.1f} per cent in 2024, <bookmark mark='c'/> and {P[2025]['rpr']:.1f} per cent in 2025, "
             f"while its volume grew {P[2025]['vol']:.1f} per cent. <bookmark mark='d'/> Only {P[2025]['org']:.1f} points "
             "of that growth came from its existing business; most came from laboratories it bought. When the price is "
             "fixed by the payer, a laboratory grows by getting bigger.",
             base=[tb[0], head("Quest: price against volume"), src], steps=[tb[1], tb[2], tb[3], note])

    def covid(self):
        D = R["diag"]
        cv = D["covid"]
        items = [(str(y), v, LABS if y in (2021, 2022) else GREY_B, f"${v:.1f}bn" if v >= 1 else f"${v * 1e3:.0f}m")
                 for y, v in sorted(cv.items())]
        bars_ = vbars(items, base_y=-2.3, height=3.8, width=1.0, gap=0.5, size=15)
        src = source("Abbott Laboratories, Forms 10-K 2022 and 2025: COVID-19 testing-related sales", size=12)
        beat(self,
             "Test makers ride the same waves as their tests. <bookmark mark='a'/> Abbott sold "
             f"{cv[2020]:.1f} billion dollars of COVID-19 tests in 2020, <bookmark mark='b'/> {cv[2021]:.1f} billion in "
             f"2021 and {cv[2022]:.1f} billion in 2022, <bookmark mark='c'/> then {cv[2023]:.1f} billion in 2023 and "
             f"{cv[2025] * 1e3:.0f} million in 2025. Like the vaccine in Part 20, a test that everyone needed for two years "
             "became a small business in three.",
             base=[head("Abbott's COVID-19 test sales"), src], steps=[bars_[0], VGroup(bars_[1], bars_[2]), VGroup(*bars_[3:])])

    def margins(self):
        comp = {c["name"]: c for c in R["landscape"]["companies"]}
        names = [("Quest", LABS), ("Labcorp", LABS), ("Danaher", TOOLS), ("Thermo Fisher", TOOLS), ("Agilent", TOOLS)]
        items = [(n, comp[n]["margin"], col, f"{100 * comp[n]['margin']:.0f}%") for n, col in names]
        rows = hbars(items, max_value=0.25, x0=-0.8, top=1.4, row=0.75, length=6.0, size=18, bar_h=0.42)
        k1 = tx("the laboratories", 16, LABS, bold=True).move_to([3.6, (rows[0].get_y() + rows[1].get_y()) / 2, 0], aligned_edge=LEFT)
        k2 = tx("instrument and test makers", 16, TOOLS, bold=True).move_to([3.6, rows[3].get_y(), 0], aligned_edge=LEFT)
        lab = tx("net income per dollar of revenue, median of 2021-2025", 16, GREY_A).to_edge(UP, buff=0.9)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Who keeps more? <bookmark mark='a'/> Quest and Labcorp, two large American laboratory companies, typically kept "
             f"about {100 * comp['Quest']['margin']:.0f} and {100 * comp['Labcorp']['margin']:.0f} cents of each dollar as "
             "profit. <bookmark mark='b'/> The companies that make the instruments, chemicals and kits, such as Danaher, "
             f"Thermo Fisher and Agilent, kept {100 * min(comp[n]['margin'] for n, _ in names[2:]):.0f} to "
             f"{100 * max(comp[n]['margin'] for n, _ in names[2:]):.0f}. The laboratory competes for every contract with insurers and "
             "doctors; the maker sells an instrument once and the chemicals it runs on for years.",
             base=[rows.axis, lab, src], steps=[[rows[0], rows[1], k1], [rows[2], rows[3], rows[4], k2]])
