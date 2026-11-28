from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Power(VoiceoverScene):
    def construct(self):
        card(self, 6, "Between giants", "What happens to a middleman squeezed between huge sellers and huge buyers?",
             "Chapter six. Between giants. A wholesaler buys from a few great makers and sells to a few great chains. Three "
             "things follow.", lit=("dollar", "moat", "change"))
        self.passthrough()
        self.alliances()
        self.opioids()

    def passthrough(self):
        P = R["power"]
        pen = VGroup(*[draw.vial(0.45) for _ in range(6)]).arrange(RIGHT, buff=0.3).move_to([0, 1.9, 0])
        c = stat_cards([(f"+${P['glp1']:.1f}bn", "Cencora's GLP-1 sales, fiscal 2026, up 22%", DRUG)], y=0.3, size=40, span=6)
        q = quote(["'increased GLP-1 sales did not meaningfully contribute to segment profit'"],
                  "Cardinal Health, Form 10-K for fiscal 2026", size=20).move_to([0, -1.3, 0])
        src = source("Cencora and Cardinal Health, Forms 10-K for fiscal 2026", size=12)
        beat(self,
             "First, pass-through. <bookmark mark='a'/> Take the GLP-1s, medicines for diabetes and weight loss. "
             f"Cencora's sales of them rose {P['glp1']:.0f} billion dollars, or twenty-two per cent, in one "
             "year. <bookmark mark='b'/> But Cardinal Health told its investors plainly that its rising GLP-1 sales did not "
             "meaningfully add to its profit. A wholesaler is paid for handling a box, not for what is inside it; when the "
             "maker sets a high price, most of the extra money passes straight through.",
             base=[pen, src], steps=[c[0], q])

    def alliances(self):
        P = R["power"]
        rows = [["", "", ""],
                ["McKesson: its ten largest customers, including buying groups", f"{P['top10']:.0f}%", "of revenue"],
                ["Cencora: its five largest suppliers", f"{P['supp']:.0f}%", "of purchases"],
                ["Cardinal Health and CVS Health", "Red Oak Sourcing", "buys generic drugs together"]]
        cols = [None, [WHITE, DRUG, GREY_A], [WHITE, GOODS, GREY_A], [WHITE, TRADE, GREY_A]]
        t = table(rows, col_x=[-6.6, 1.8, 3.6], top=1.9, row_h=0.9, size=18, colors=cols)
        tag = estimate_tag("McKesson, Cencora and Cardinal Health, Forms 10-K for fiscal 2026", size=12)
        beat(self,
             "Second, buying power on both sides. <bookmark mark='a'/> McKesson's ten largest customers, counting the group "
             f"purchasing organizations that negotiate for thousands of hospitals and pharmacies together, bought "
             f"{P['top10']:.0f} per cent of everything it sold. <bookmark mark='b'/> Cencora's five largest suppliers sold it "
             f"{P['supp']:.0f} per cent of what it bought. <bookmark mark='c'/> And sometimes buyers join forces with a "
             "wholesaler: Cardinal Health and CVS Health buy generic medicines together through a venture called Red Oak "
             "Sourcing. In this series' reading, where the makers are many, as in generics, the middleman can bargain; where "
             "a maker owns a patent, it cannot.",
             base=[tag], steps=[t[1], t[2], t[3]])

    def opioids(self):
        P = R["power"]
        c = stat_cards([("2 April 2022", "the national opioid settlement takes effect", BAD),
                        (f"${P['nosa']:.0f}m", "Cardinal's sixth annual payment, July 2026", BAD),
                        (f"${P['opioid']:.1f}bn", "McKesson's estimated opioid liability still owed, March 2026", BAD)], y=0.5, size=34, span=12.6)
        note = tx("the claims concerned how the wholesalers monitored and reported shipments of controlled substances", 16, GREY_B).move_to([0, -1.6, 0])
        src = source("Cardinal Health and McKesson, Forms 10-K for fiscal 2026", size=12)
        beat(self,
             "Third, responsibility. A wholesaler sees every order. <bookmark mark='a'/> During America's opioid crisis, states "
             "and towns sued the three drug wholesalers, among others, over how they had monitored and reported shipments of "
             "controlled painkillers. A national settlement took effect in April 2022. <bookmark mark='b'/> Cardinal Health "
             f"made its sixth annual payment under it, {P['nosa']:.0f} million dollars, in July 2026. <bookmark mark='c'/> "
             f"McKesson still estimated {P['opioid']:.1f} billion dollars owed under its opioid settlements in March 2026. "
             "The middleman's position, seeing everything that flows, turned out to carry duties as well as profits.",
             base=[note, src], steps=[c[0], c[1], c[2]])
