from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Odds(VoiceoverScene):
    def construct(self):
        card(self, 3, "The odds", "Where do drugs fail, and which kinds fail most?",
             "Chapter three. The odds. Where do drugs fail, and which kinds of drugs fail most often?", lit=("make", "moat"))
        self.phases()
        self.phase2()
        self.areas()

    def phase2(self):
        O = R["odds"]
        p2 = O["p2"]
        items = [(k, v, GOOD if v > 40 else (BAD if v < 25 else PRICE), f"{v:.1f}%") for k, v in p2.items()]
        rows = hbars(items, max_value=55, x0=-0.6, top=2.0, row=0.6, length=6.0, size=16, bar_h=0.4)
        allp = DashedLine([-0.6 + 6.0 * 28.9 / 55, 2.4, 0], [-0.6 + 6.0 * 28.9 / 55, -2.0, 0], stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        al = tx("all drugs: 28.9%", 13, GREY_B).next_to(allp, UP, buff=0.05)
        src = source("BIO, Informa and QLS, Clinical Development Success Rates 2011-2020: Phase II success by disease area", size=12)
        beat(self,
             "Phase two is the great filter, and it is harder in some diseases than others. <bookmark mark='a'/> For "
             f"blood disorders nearly half of drugs pass it, {p2['hematology']:.0f} per cent, and for metabolic diseases "
             f"{p2['metabolic']:.0f}. <bookmark mark='b'/> For the brain, about a quarter; for cancer, "
             f"{p2['oncology']:.0f} per cent; for the heart and blood vessels, {p2['cardiovascular']:.0f}; for urology "
             f"only {p2['urology']:.0f}. Phase two is where a drug first has to prove that it helps patients, and in some "
             "diseases that proof is much harder to find.",
             base=[rows.axis, allp, al, head("Phase II success by disease area, 2011-2020"), src],
             steps=[VGroup(rows[0], rows[1], rows[2]), VGroup(*rows[3:])])

    def phases(self):
        O = R["odds"]
        items = [(n, 100 * q, BAD if q < 0.4 else (GOOD if q > 0.8 else PRICE), f"{100 * q:.1f}%") for n, _, q in O["phases"]]
        bars_ = vbars(items, base_y=-2.3, height=3.8, width=1.5, gap=1.0)
        note = tx("the share of drugs that pass each stage, 2011-2020", 16, GREY_A).to_edge(UP, buff=0.9)
        src = source("BIO, Informa and QLS, Clinical Development Success Rates 2011-2020 (2021)", size=12)
        beat(self,
             "Here is the share of drugs that pass each stage, from a study of thousands of development programmes "
             f"between 2011 and 2020. <bookmark mark='a'/> About {100 * O['phases'][0][2]:.0f} per cent pass Phase one: "
             "most new drugs are safe enough. <bookmark mark='b'/> Only "
             f"{100 * O['phases'][1][2]:.0f} per cent pass Phase two. This is where a drug first has to show that it "
             "works, and most do not. <bookmark mark='c'/> Of those that reach Phase three, "
             f"{100 * O['phases'][2][2]:.0f} per cent succeed. <bookmark mark='d'/> And "
             f"{100 * O['phases'][3][2]:.0f} per cent of the drugs submitted to the FDA are approved. Multiply them and "
             f"you get {O['loa']} per cent.",
             base=[note, src], steps=list(bars_))

    def areas(self):
        O = R["odds"]
        a = O["areas"]
        items = [(k, v, BAD if v < 7 else (GOOD if v > 15 else PRICE), f"{v:.1f}%") for k, v in a.items()]
        rows = hbars(items, max_value=26, x0=-0.8, top=1.6, row=0.8, length=6.0, size=17, bar_h=0.5)
        src = source("BIO, Informa and QLS, Clinical Development Success Rates 2011-2020: likelihood of approval from Phase I",
                     size=12)
        beat(self,
             "The odds differ by disease. <bookmark mark='a'/> Drugs for blood disorders were approved about "
             f"{a['hematology']:.0f} per cent of the time, and drugs for rare diseases {a['rare diseases']:.0f} per cent. "
             "<bookmark mark='b'/> Drugs for chronic, common diseases succeeded only "
             f"{a['chronic, common diseases']:.1f} per cent of the time, and cancer drugs {a['oncology']:.1f}. Cancer was "
             f"also the biggest group in the study, {O['onc_n']:,} of the drugs entering Phase one: the industry puts the "
             "most effort where the odds are among the worst.",
             base=[rows.axis, head("Likelihood of approval from Phase I, 2011-2020"), src],
             steps=[VGroup(rows[0], rows[1], rows[2]), VGroup(rows[3], rows[4])])
