from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class Customers(VoiceoverScene):
    def construct(self):
        card(self, 4, "The surgeon, the hospital and the payer", "How do you sell to three customers at once?",
             "Chapter four. The surgeon, the hospital and the payer. Each wants something different from the same device.",
             lit=("dollar", "moat"))
        self.surgeon()
        self.hospital()
        self.payer()
        self.deductible()

    def surgeon(self):
        sg = VGroup(draw.person(1.1, SURGEON), draw.surgical_robot(1.4)).arrange(RIGHT, buff=0.4).move_to([-4.2, 1.0, 0])
        q = quote(["'Our clinical sales team works on site at hospitals, interacting with surgeons or physicians,",
                   "operating room staff, and hospital administrators to develop and sustain successful",
                   "robotic-assisted surgery or bronchoscopy programs.'"], "Intuitive Surgical, Form 10-K 2025", size=15,
                  width=7.4).move_to([2.6, 1.2, 0])
        mk = tx("Stryker's Mako robot: more than 2 million knee and hip operations, with Stryker's implants", 16, DEVICE,
                bold=True).move_to([0, -1.6, 0])
        src = source("Intuitive Surgical, Inc. and Stryker Corporation, Forms 10-K 2025", size=12)
        beat(self,
             "The surgeon comes first. <bookmark mark='a'/> A surgeon who has learned one robot, one implant system, one "
             "set of instruments, has invested hours of skill in it, and switching means learning again. "
             "<bookmark mark='b'/> So device makers send their own people into the operating theatre. Intuitive's report "
             "says its clinical sales team works on site at hospitals, with surgeons, theatre staff and administrators. "
             "<bookmark mark='c'/> And robots tie the surgeon to the implants: Stryker's Mako robot, used with Stryker's "
             f"own knees and hips, had been used in more than {R['boom']['mako']:.0f} million operations by 2025.",
             base=[src], steps=[sg, q, mk])

    def hospital(self):
        hp = draw.hospital(2.2).move_to([-4.2, 0.6, 0])
        q1 = quote(["'placements of our da Vinci surgical systems have tended to be heavier in the fourth quarter",
                    "and lighter in the first quarter, as hospital budgets are reset.'"], "Intuitive Surgical, Form 10-K 2025",
                   size=15, width=7.6).move_to([2.4, 1.6, 0])
        q2 = quote(["'organizations continue to consolidate purchasing decisions ... resulting in pricing pressures",
                    "and decreased average selling prices.'"], "Intuitive Surgical, Form 10-K 2025", size=15,
                   width=7.6).move_to([2.4, -0.6, 0])
        src = source("Intuitive Surgical, Inc., Form 10-K 2025", size=12)
        beat(self,
             "The hospital comes second. It buys equipment out of a capital budget, once a year, <bookmark mark='a'/> and "
             "it shows: Intuitive places more robots in the last quarter of the year and fewer in the first, as hospital "
             "budgets reset. <bookmark mark='b'/> Hospitals also buy together, through larger systems and purchasing "
             "groups, and Intuitive's report says that consolidation brings pricing pressure and lower average selling "
             "prices. The surgeon asks for the best device; the hospital asks what it costs.",
             base=[hp, src], steps=[q1, q2])

    def payer(self):
        C = R["customers"]
        names = {"ins": "health insurers", "gov": "government (Medicare, Medicaid)", "client": "clients (doctors, hospitals, employers)",
                 "pat": "patients"}
        rows = [["", "share of tests", "share of revenue"]] + [[names[k], f"{v[0]}%", f"{v[1]}%"] for k, v in C["mix"].items()]
        tb = table(rows, col_x=[-5.0, 1.4, 4.2], top=1.6, row_h=0.62, size=18,
                   colors=[None] + [[c, c, c] for c in (PAYER, DEVICE, IMAGING, GOOD)])
        src = source("Quest Diagnostics Incorporated, Form 10-K 2025: requisition volume and net revenues by payer, 2025", size=12)
        beat(self,
             "The payer comes third, and in a laboratory you can see who pays for what. <bookmark mark='a'/> Of Quest's "
             f"tests in 2025, {C['mix']['ins'][0]} per cent were billed to health insurers, <bookmark mark='b'/> "
             f"{C['mix']['gov'][0]} per cent to government payers, which include America's Medicare and Medicaid, <bookmark mark='c'/> and "
             f"{C['mix']['client'][0]} per cent to doctors, hospitals and employers who order tests in bulk. "
             f"<bookmark mark='d'/> Patients paid directly for only about {C['mix']['pat'][0]} per cent of tests but "
             f"{C['mix']['pat'][1]} per cent of the revenue, mostly their share of insured bills.",
             base=[tb[0], head("Who pays a laboratory"), src], steps=list(tb[1:]))

    def deductible(self):
        q1 = VGroup(tx("January to March", 18, WHITE, bold=True), tx("deductibles reset:", 16, GREY_A),
                    tx("fewer benign operations", 16, BAD, bold=True)).arrange(DOWN, buff=0.08)
        q4 = VGroup(tx("October to December", 18, WHITE, bold=True), tx("deductibles met:", 16, GREY_A),
                    tx("more benign operations", 16, GOOD, bold=True)).arrange(DOWN, buff=0.08)
        months = VGroup(q1, q4).arrange(DOWN, buff=0.7).move_to([-3.6, -0.2, 0])
        ql = VGroup(Arrow(UP * 0.3, DOWN * 0.3, buff=0, color=BAD).next_to(q1, LEFT, buff=0.3),
                    Arrow(DOWN * 0.3, UP * 0.3, buff=0, color=GOOD).next_to(q4, LEFT, buff=0.3))
        note = VGroup()
        q = quote(["'In the U.S., volumes for procedures associated with benign conditions are typically",
                   "seasonally higher in the fourth quarter when more patients have met annual deductibles", "and lower in the first quarter when deductibles are reset.'"],
                  "Intuitive Surgical, Form 10-K 2025", size=15, width=6.6).move_to([3.4, 0.8, 0])
        src = source("Intuitive Surgical, Inc., Form 10-K 2025", size=12)
        beat(self,
             "And the patient, who pays least, still moves the numbers. <bookmark mark='a'/> More than half of da Vinci "
             "operations are for conditions that are not life-threatening, such as hernias and gallbladders. "
             "<bookmark mark='b'/> In America those operations rise in the last quarter of the year, when more patients "
             "have already paid their annual deductible, and fall in the first, when it resets. A surgeon's schedule follows "
             "the insurance calendar.",
             base=[src], steps=[[months, ql, note], q])
