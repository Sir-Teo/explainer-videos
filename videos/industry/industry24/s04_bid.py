from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403


class Bid(VoiceoverScene):
    def construct(self):
        card(self, 3, "The bid and the contract", "Who carries the risk that the estimate is wrong?",
             "Chapter three. The bid and the contract. Run it assumed a fixed price. The most important decision a "
             "contractor makes may be which kind of contract it signs at all.", lit=("dollar", "change"))
        self.forms()
        self.lump()
        self.fluor()
        self.charges()
        self.tutor()

    def forms(self):
        fixed = VGroup(draw.blueprint(1.4), tx("Fixed price (lump sum)", 20, BAD, bold=True),
                       tx("the contractor names a price;", 16, WHITE), tx("if it costs more, the contractor pays", 16, WHITE)
                       ).arrange(DOWN, buff=0.15).move_to([-3.4, 0.4, 0])
        cost = VGroup(draw.hardhat(1.2), tx("Cost plus a fee (reimbursable)", 20, GOOD, bold=True),
                      tx("the owner pays what it costs,", 16, WHITE), tx("plus an agreed fee or markup", 16, WHITE)
                      ).arrange(DOWN, buff=0.15).move_to([3.4, 0.4, 0])
        line = DashedLine([0, 2.4, 0], [0, -1.8, 0], stroke_color=GREY_B, stroke_width=2)
        note = tx("and in between: a guaranteed maximum price", 17, PRICE).move_to([0, -2.4, 0])
        beat(self,
             "There are two basic ways to pay for a building. <bookmark mark='a'/> A fixed price, or lump sum: the "
             "contractor names a price, and if the job costs more, the contractor pays the difference. That is the "
             "contract Run it was about, and it is where the winner's curse bites. <bookmark mark='b'/> Or cost plus a "
             "fee: the owner pays whatever the work costs, plus an agreed fee. Now the owner carries the risk, and the "
             "contractor earns less but cannot lose much. <bookmark mark='c'/> In between sits the guaranteed maximum "
             "price: cost plus a fee, up to a ceiling the contractor must absorb above.",
             base=[line], steps=[fixed, cost, note])

    def lump(self):
        q = quote(["'Under lump-sum contracts, we may bid based upon preliminary engineering drawings and specifications",
                   "provided by the client. This type of contracting presents risk because, among other things, it",
                   "requires us to predetermine the work to be performed, the project execution schedule and all costs",
                   "associated with the work based on incomplete information'"], "Fluor Corporation, Form 10-K for 2025",
                  size=17).move_to([0, 0.8, 0])
        bp = draw.blueprint(1.6).move_to([0, -1.9, 0])
        src = source("Fluor Corporation, Form 10-K for 2025", size=12)
        beat(self,
             "Fluor, an American engineering and construction firm with fifteen billion dollars of revenue, describes the "
             "problem in its own "
             "annual report. <bookmark mark='a'/> On a lump-sum contract it may bid on preliminary drawings, and must "
             "fix the work, the schedule and every cost 'based on incomplete information'. <bookmark mark='b'/> A price "
             "for a thing not yet fully designed: that is the sealed bid of chapter one, on a project worth billions.",
             base=[src], steps=[q, bp])

    def fluor(self):
        C = R["contracts"]
        bar24 = viz.bar_split([("reimbursable", get("flr.reimb.2024"), GOOD), ("lump sum", get("flr.lump.2024"), BAD)],
                              get("flr.reimb.2024") + get("flr.lump.2024"), width=10.0, height=0.7).move_to([0.6, 1.0, 0])
        bar25 = viz.bar_split([("reimbursable", C["reimb"], GOOD), ("lump sum", C["lump"], BAD)], C["reimb"] + C["lump"],
                              width=10.0 * (C["reimb"] + C["lump"]) / (get("flr.reimb.2024") + get("flr.lump.2024")),
                              height=0.7).move_to([0.6, -0.6, 0], aligned_edge=LEFT).align_to(bar24, LEFT)
        l24 = tx("end of 2024", 16, GREY_A).next_to(bar24, LEFT, buff=0.2)
        l25 = tx("end of 2025", 16, GREY_A).next_to(bar25, LEFT, buff=0.2)
        t24 = tx(f"{100 * C['share24']:.0f}% cost-reimbursable", 15, GOOD, bold=True).next_to(bar24, UP, buff=0.12)
        t25 = tx(f"{100 * C['share']:.0f}% cost-reimbursable, ${(C['reimb'] + C['lump']) / 1e3:.1f}bn in all", 15, GOOD, bold=True).next_to(bar25, DOWN, buff=0.12)
        lk = tx("red: lump sum or guaranteed maximum", 14, BAD, bold=True).next_to(bar24, UP, buff=0.12).align_to(bar24, RIGHT)
        q = tx("'focusing on reimbursable terms'", 19, PRICE, bold=True).move_to([0, -2.4, 0])
        src = source("Fluor Corporation, Form 10-K for 2025: backlog by contract type", size=12)
        beat(self,
             "So Fluor has been changing what it signs. <bookmark mark='a'/> At the end of 2024, "
             f"{100 * C['share24']:.0f} per cent of the work it had won and not yet done was on reimbursable terms. "
             f"<bookmark mark='b'/> At the end of 2025, {100 * C['share']:.0f} per cent, out of "
             f"{(C['reimb'] + C['lump']) / 1e3:.1f} billion dollars. <bookmark mark='c'/> Its strategy, in its own words, "
             "is 'focusing on reimbursable terms and only considering fixed-price contracts' where it has a strong "
             "position. A contractor that has been burned by fixed prices stops offering them.",
             base=[src], steps=[[bar24, l24, t24, lk], [bar25, l25, t25], q])

    def charges(self):
        C = R["contracts"]
        c = stat_cards([(f"${C['adj']:.0f}m", "cost growth on three infrastructure projects: design errors, prices, delays", BAD),
                        (f"${C['santos']:.0f}m", "revenue reversed in 2025 for a court judgment on a project finished in 2015", BAD),
                        (f"${C['lossbook']:.0f}m", "of work still to do on old projects already in a loss", PRICE)],
                       y=0.6, size=38, span=12.4)
        src = source("Fluor Corporation, Form 10-K for 2025", size=12)
        beat(self,
             "What does a wrong estimate look like in the accounts? <bookmark mark='a'/> In 2025 Fluor booked "
             f"{C['adj']:.0f} million dollars of cost growth on three infrastructure projects, from design errors by "
             "subcontractors, rising prices and delays. <bookmark mark='b'/> It reversed "
             f"{C['santos']:.0f} million dollars of revenue after a court ruled against it over a project in Australia it "
             "had finished ten years earlier. <bookmark mark='c'/> And it still had "
             f"{C['lossbook']:.0f} million dollars of work to do on old projects it already knew would lose money. A "
             "building contract can stay open long after the building does.",
             base=[src], steps=[c[0], c[1], c[2]])

    def tutor(self):
        T = R["contracts"]["tpc"]
        items = [(str(y), 100 * v, GOOD if v > 0 else BAD, f"{100 * v:+.1f}%") for y, v in T.items()]
        n = len(items)
        bars_ = VGroup()
        ax0 = -2.6 + 0.0
        for i, (lab, v, col, t) in enumerate(items):
            h = abs(v) * 0.3
            x = -4.2 + i * 1.4
            rect = Rectangle(width=0.9, height=max(h, 0.03), stroke_width=0, fill_color=col, fill_opacity=0.9)
            rect.move_to([x, -0.2 + (h / 2 if v > 0 else -h / 2), 0])
            vt = tx(t, 15, col, bold=True).next_to(rect, UP if v > 0 else DOWN, buff=0.08)
            yl = tx(lab, 14, GREY_A).move_to([x, 1.2 if v < 0 else -0.65, 0])
            bars_.add(VGroup(rect, vt, yl))
        axis = Line([-5.0, -0.2, 0], [-4.2 + (n - 1) * 1.4 + 0.8, -0.2, 0], stroke_color=GREY_B, stroke_width=2)
        lab = tx("Tutor Perini, a civil and building contractor: net income per dollar of revenue", 16, GREY_A).to_edge(UP, buff=0.7)
        src = source("Tutor Perini Corporation, Forms 10-K via SEC company facts", size=12)
        beat(self,
             "And some years it is the whole company. <bookmark mark='a'/> Tutor Perini, a contractor for large civil and "
             f"building projects, lost {abs(100 * T[2019]):.1f} cents on each dollar of revenue in 2019, "
             f"<bookmark mark='b'/> made a little in 2020 and 2021, <bookmark mark='c'/> and lost money again in 2022, "
             f"2023 and 2024, before a profit of {100 * T[2025]:.1f} cents in 2025. On fixed-price work, one bad "
             "estimate on one large job can wipe out years of thin profits on all the others.",
             base=[axis, lab, src], steps=[bars_[0], bars_[1:3], bars_[3:]])
