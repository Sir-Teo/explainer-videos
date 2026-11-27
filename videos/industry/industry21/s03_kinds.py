from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class Kinds(VoiceoverScene):
    def construct(self):
        card(self, 2, "Four businesses", "What does a medical technology company actually sell?",
             "Chapter two. Four businesses. Medical technology is not one business but four, and they earn their money in "
             "different ways.", lit=("unit", "make"))
        self.implants()
        self.equipment()
        self.consumables()
        self.diagnostics()

    def implants(self):
        K = R["kinds"]
        items = [(k, v / 1e3, DEVICE if k != "Diabetes" else GREY_B, f"${v / 1e3:.1f}bn") for k, v in K["mdt"].items()]
        rows = hbars(items, max_value=15, x0=-0.6, top=1.4, row=0.85, length=6.0, size=17, bar_h=0.45)
        pm = draw.pacemaker(1.1).move_to([-5.2, 1.6, 0])
        lab = tx("1. implants and therapies", 22, DEVICE, bold=True).to_edge(UP, buff=0.9)
        src = source("Medtronic plc, Form 10-K for fiscal 2026: net sales by segment", size=12)
        beat(self,
             "The first is implants and the therapies around them: pacemakers, heart valves, spinal implants, new knees and "
             "hips. The largest maker is Medtronic, founded in 1949, whose fiscal year ended in April 2026 with sales of "
             f"{K['mdt_rev'] / 1e3:.1f} billion dollars. <bookmark mark='a'/> Its heart business sold "
             f"{K['mdt']['Cardiovascular'] / 1e3:.1f} billion, <bookmark mark='b'/> its brain and spine business "
             f"{K['mdt']['Neuroscience'] / 1e3:.1f} billion, <bookmark mark='c'/> its surgical tools "
             f"{K['mdt']['Medical Surgical'] / 1e3:.1f} billion, <bookmark mark='d'/> and its diabetes business, which it "
             f"is separating into a company of its own, {K['mdt']['Diabetes'] / 1e3:.1f} billion. An implant is chosen by "
             "a surgeon for one patient, used once, and paid for as part of the operation.",
             base=[rows.axis, pm, lab, src], steps=list(rows))

    def equipment(self):
        K = R["kinds"]
        g = K["gehc"]
        tot = g["products"] + g["services"]
        bar = viz.bar_split([("products", g["products"], IMAGING), ("services", g["services"], GOOD)], tot, width=9.0,
                            height=0.8).move_to([0.8, -0.6, 0])
        l1 = tx(f"products ${g['products'] / 1e3:.1f}bn", 17, IMAGING, bold=True).next_to(bar[0], DOWN, buff=0.2)
        l2 = tx(f"services ${g['services'] / 1e3:.1f}bn", 17, GOOD, bold=True).next_to(bar[1], DOWN, buff=0.2)
        sc = draw.scanner(2.2).move_to([-4.2, 1.6, 0])
        lab = tx("2. equipment, and its service", 22, IMAGING, bold=True).to_edge(UP, buff=0.9)
        src = source("GE HealthCare Technologies Inc., Form 10-K 2025: sales of products and of services", size=12)
        beat(self,
             "The second is capital equipment: scanners, monitors, ultrasound machines, robots. <bookmark mark='a'/> For "
             "a hospital each is a large capital purchase, planned in its budget. GE HealthCare, separated from "
             f"General Electric in 2023, sold {tot / 1e3:.1f} billion dollars in 2025. <bookmark mark='b'/> "
             f"{g['products'] / 1e3:.1f} billion was machines and their parts, <bookmark mark='c'/> and "
             f"{g['services'] / 1e3:.1f} billion, about a third, was servicing the machines already installed, year after "
             "year.",
             base=[lab, src], steps=[sc, [bar[0], l1], [bar[1], l2]])

    def consumables(self):
        K = R["kinds"]
        d = K["dexcom"]
        ch = line_chart({"Dexcom": (d, GOOD)}, x=(2012, 2025), y=(0, 5), xticks=[2012, 2015, 2018, 2021, 2025],
                        yticks=[0, 1, 2, 3, 4, 5], yfmt=lambda v: f"${v:.0f}bn", ylabel="Dexcom's revenue", width=8.0,
                        height=4.0, center=(1.0, -0.6), label_end=False)
        end = marker(ch.ax, 2025, d[2025], f"${d[2025]:.1f}bn", GOOD, side=LEFT)
        st = marker(ch.ax, 2012, d[2012], f"${d[2012] * 1e3:.0f}m", GOOD, side=UP)
        sen = VGroup(draw.glucose_sensor(0.45), draw.glucose_sensor(0.45, ring=PRICE), draw.glucose_sensor(0.45)).arrange(DOWN, buff=0.25).move_to([-5.6, 0.2, 0])
        lab = tx("3. consumables", 22, GOOD, bold=True).to_edge(UP, buff=0.9)
        src = source("Dexcom, Inc., Forms 10-K via SEC company facts: revenue", size=12)
        beat(self,
             "The third is consumables: things used up and bought again, like the robot's instruments, catheters, and "
             "the glucose sensors that people with diabetes wear on the skin and replace. <bookmark mark='a'/> Dexcom, "
             f"which makes such sensors, had {d[2012] * 1e3:.0f} million dollars of revenue in 2012. <bookmark mark='b'/> "
             f"By 2025 it had {d[2025]:.1f} billion. <bookmark mark='c'/> Every new user is a customer for years: revenue "
             "that repeats.",
             base=[ch.frame, lab, src], steps=[[sen, st], ch.lines["Dexcom"], end])

    def diagnostics(self):
        K = R["kinds"]
        Q = K["quest"]
        tubes = draw.test_tubes(6, 1.6).move_to([-3.6, 0.2, 0])
        c = stat_cards([(f"{Q['reqs']:.0f} million", "test requisitions in 2025", LABS),
                        (f"${Q['dis'] / 1e3:.1f}bn", "laboratory revenue", WHITE)], y=1.0, size=40, span=6.0)
        c.shift(RIGHT * 3.0)
        note = tx(f"about ${Q['dis'] / Q['reqs']:.0f} a requisition", 22, PRICE, bold=True).move_to([3.0, -1.2, 0])
        lab = tx("4. diagnostics", 22, LABS, bold=True).to_edge(UP, buff=0.9)
        src = source("Quest Diagnostics Incorporated, Form 10-K 2025", size=12)
        beat(self,
             "The fourth is diagnostics: the tests, and the instruments and chemicals that run them. "
             f"<bookmark mark='a'/> Quest Diagnostics, a laboratory company, processed about "
             f"{Q['reqs']:.0f} million test orders in 2025, <bookmark mark='b'/> for {Q['dis'] / 1e3:.1f} billion dollars "
             f"of revenue: <bookmark mark='c'/> about {Q['dis'] / Q['reqs']:.0f} dollars an order. Small sums, in huge "
             "numbers. Four businesses: one sold to the surgeon, one to the hospital's committee, one used up and bought "
             "again, one billed by the test.",
             base=[tubes, lab, src], steps=[c[0], c[1], note])
