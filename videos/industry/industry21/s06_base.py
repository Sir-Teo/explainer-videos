from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403

KIND_COL = {"instruments": GOOD, "leases": PRICE, "systems": DEVICE, "service": IMAGING}
KIND_NAME = {"instruments": "instruments and accessories", "leases": "robots leased", "systems": "robots sold",
             "service": "service"}


class Base(VoiceoverScene):
    def construct(self):
        card(self, 5, "The installed base", "Why is the robot the smaller part of the business?",
             "Chapter five. The installed base. Once a machine is in the hospital, it keeps earning for its maker.",
             lit=("dollar", "moat"))
        self.stacks()
        self.service()
        self.hospital_bill()
        self.repair()

    def stacks(self):
        B = R["base"]
        isrg = B["isrg"]
        scale = 3.8 / 10500
        stacks = VGroup()
        for i, y in enumerate((2023, 2024, 2025)):
            x, yb = -3.4 + 2.3 * i, -2.3
            st = VGroup()
            for k in ("instruments", "leases", "systems", "service"):
                h = isrg[y][k] * scale
                st.add(Rectangle(width=1.3, height=h, stroke_color="#0E1117", stroke_width=1.5, fill_color=KIND_COL[k],
                                 fill_opacity=0.9).move_to([x, yb + h / 2, 0]))
                yb += h
            tot = sum(isrg[y].values())
            st.add(tx(f"${tot / 1e3:.1f}bn", 15, WHITE, bold=True).next_to(st, UP, buff=0.08),
                   tx(str(y), 15, GREY_A).move_to([x, -2.6, 0]))
            stacks.add(st)
        key = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=KIND_COL[k], fill_opacity=0.9), tx(KIND_NAME[k], 15, WHITE)
                              ).arrange(RIGHT, buff=0.12) for k in ("service", "systems", "leases", "instruments")]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.6, 0.4, 0])
        rec = tx(f"recurring: {B['recurring']}% of revenue", 20, GOOD, bold=True).move_to([4.6, -1.6, 0])
        src = source("Intuitive Surgical, Inc., Form 10-K 2025: revenue by kind; recurring revenue", size=12)
        beat(self,
             "Here is Intuitive's revenue, split by what it sold. <bookmark mark='a'/> In 2023, "
             f"{sum(isrg[2023].values()) / 1e3:.1f} billion dollars; <bookmark mark='b'/> in 2025, "
             f"{sum(isrg[2025].values()) / 1e3:.1f} billion. The green at the bottom is instruments and accessories, "
             f"{isrg[2025]['instruments'] / 1e3:.1f} billion in 2025, more than robots sold and leased together. "
             "<bookmark mark='c'/> Add the service contracts and the leases and the company calls "
             f"{B['recurring']} per cent of its revenue recurring: earned from robots already installed, operation after "
             "operation, year after year.",
             base=[key, src], steps=[stacks[0], VGroup(stacks[1], stacks[2]), rec])

    def service(self):
        B = R["base"]
        items = [("products: machines and parts", B["gehc_gm_products"], IMAGING, f"{100 * B['gehc_gm_products']:.0f}%"),
                 ("services: keeping them running", B["gehc_gm_services"], GOOD, f"{100 * B['gehc_gm_services']:.0f}%")]
        rows = hbars(items, max_value=0.6, x0=-0.6, top=0.9, row=1.1, length=6.0, size=18, bar_h=0.55)
        sc = draw.scanner(1.6).move_to([-5.0, 2.0, 0])
        lab = tx("gross margin, 2025: what is left of each dollar after the cost of what was sold", 16, GREY_A).to_edge(UP, buff=0.9)
        src = source("GE HealthCare Technologies Inc., Form 10-K 2025: sales and costs of products and of services", size=12)
        beat(self,
             f"The same holds for scanners. GE HealthCare earned {100 * B['gehc_share']:.0f} per cent of its 2025 revenue "
             "from servicing its machines. <bookmark mark='a'/> On the machines and parts it sold, it kept "
             f"{100 * B['gehc_gm_products']:.0f} cents of each dollar after their cost; <bookmark mark='b'/> on service, "
             f"{100 * B['gehc_gm_services']:.0f} cents. A scanner sold is a service contract won, for as long as the scanner "
             "runs.",
             base=[rows.axis, sc, lab, src], steps=[rows[0], rows[1]])

    def hospital_bill(self):
        B = R["base"]
        sp = B["spend"]
        parts = sp["parts"]
        cols = {"system": DEVICE, "service": IMAGING, "instruments": GOOD}
        bar = viz.bar_split([(k, v, cols[k]) for k, v in parts.items()], sp["total"], width=11.0, height=0.9).move_to([0, 0.4, 0])
        labs = VGroup()
        for i, (k, v) in enumerate(parts.items()):
            labs.add(VGroup(tx(f"${v / 1e6:.1f}m", 22, cols[k], bold=True),
                            tx({"system": "the robot", "service": "four more years of service",
                                "instruments": "instruments, 300 operations a year"}[k], 14, GREY_A)
                            ).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.25))
        tot = tx(f"${sp['total'] / 1e6:.1f}m over five years: about ${sp['per_op']:,.0f} an operation", 20, WHITE, bold=True).move_to([0, 2.0, 0])
        tag = estimate_tag("the middle of Intuitive's ranges and its average instruments revenue per operation, 2025", size=12)
        beat(self,
             "Now look at it from the hospital's side: five years with one robot, at the average three hundred operations "
             "a year. <bookmark mark='a'/> The robot, at the middle of Intuitive's price range, about "
             f"{parts['system'] / 1e6:.1f} million dollars, with its first year of service. <bookmark mark='b'/> Four more "
             f"years of service at the middle of its range: {parts['service'] / 1e6:.2f} million. <bookmark mark='c'/> And "
             f"instruments, at the {R['hook']['per_op']:,.0f} dollars Intuitive earned on average per operation in 2025: "
             f"{parts['instruments'] / 1e6:.1f} million, the largest part. <bookmark mark='d'/> About "
             f"{sp['per_op']:,.0f} dollars an operation in all, half of it for instruments that wear out and must be "
             "bought again.",
             base=[tag], steps=[[bar[0], labs[0]], [bar[1], labs[1]], [bar[2], labs[2]], tot])

    def repair(self):
        B = R["base"]
        q = quote(["'The Court also ruled that there is an antitrust aftermarket for the repair and replacement",
                   "of EndoWrist instruments, and that Intuitive holds monopoly power in that aftermarket.'"],
                  "Intuitive Surgical, Form 10-Q for the third quarter of 2026, on a 2024 ruling in the hospitals' case",
                  size=15, width=11.0).move_to([0, 1.2, 0])
        c = tx(f"third quarter of 2026: a ${B['settle']:.0f}m charge to settle the hospitals' class action", 20, BAD, bold=True).move_to([0, -0.8, 0])
        src = source("Intuitive Surgical, Inc., Form 10-Q and Form 8-K for the third quarter of 2026", size=12)
        beat(self,
             "Who may service the installed base is worth fighting over. In 2021 hospitals sued Intuitive, alleging that "
             "it broke antitrust law over the service and repair of its instruments. <bookmark mark='a'/> In 2024 "
             "the court found, among other things, a separate market for repairing the instruments, in which Intuitive "
             "held monopoly power, as Intuitive's own report records. <bookmark mark='b'/> In the third quarter of 2026 "
             f"Intuitive took a charge of {B['settle']:.0f} million dollars to settle the hospitals' class action. The "
             "money in medical technology is in what happens after the sale, and so are the disputes.",
             base=[src], steps=[q, c])
