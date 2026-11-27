from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: pay for Phase III?", "Your drug worked in Phase II. Do you spend $250 million to prove it?",
             "Chapter one. Run it. Your drug has just passed its Phase II trial. The next trial, Phase III, will cost a "
             "quarter of a billion dollars. Do you pay?", lit=("make", "dollar"))
        self.tree()
        self.answer()
        self.pipeline()

    def pipeline(self):
        Pp = R["pipeline"]
        items = [(k, v, LAB if k == "approved" else BRAND, f"{v:.1f}") for k, v in Pp.items()]
        bars_ = vbars(items, base_y=-2.3, height=3.8, width=1.3, gap=0.8)
        hd = tx("candidates that must enter each stage, on average, for one approved drug", 16, GREY_A).to_edge(UP, buff=0.9)
        tag = estimate_tag("BIO's phase success rates, 2011-2020", size=12)
        beat(self,
             "Now scale it up to a whole company. <bookmark mark='a'/> With the industry's odds, to get one drug "
             f"approved a company needs about {Pp['Phase I']:.0f} candidates entering Phase one, "
             f"<bookmark mark='b'/> about {Pp['Phase II']:.0f} entering Phase two, <bookmark mark='c'/> about "
             f"{Pp['Phase III']:.0f} entering Phase three, <bookmark mark='d'/> and one submission. "
             "<bookmark mark='e'/> A company that wants two new drugs a year must keep twenty-five new candidates "
             "entering the clinic every year, and must decide, at every stage, which ones to stop.",
             base=[hd, tag], steps=list(bars_))

    def tree(self):
        U = R["run"]
        root = VGroup(draw.flask(1.0, LAB), tx("Phase II passed", 16, LAB, bold=True)).arrange(DOWN, buff=0.1).move_to([-5.4, 0.2, 0])
        big = VGroup(tx(f"a big market ({100 * U['p_big']:.0f}% chance)", 17, GOOD, bold=True),
                     tx(f"peak sales ${U['peak_big'] / 1e3:.0f}bn a year", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-1.2, 1.7, 0])
        small = VGroup(tx(f"a small market ({100 * (1 - U['p_big']):.0f}% chance)", 17, BAD, bold=True),
                       tx(f"peak sales ${U['peak_small'] / 1e3:.2f}bn a year", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-1.2, -1.5, 0])
        a1 = Arrow(root.get_right(), big.get_left(), buff=0.15, stroke_width=3, color=GOOD)
        a2 = Arrow(root.get_right(), small.get_left(), buff=0.15, stroke_width=3, color=BAD)
        p3 = VGroup(tx(f"then Phase III: ${U['p3']:.0f}m,", 16, WHITE), tx(f"{100 * U['q3']:.0f}% pass, then the FDA {100 * U['q4']:.0f}%", 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([3.6, 0.1, 0])
        vb = tx(f"worth going on: +${U['big']:,.0f}m", 18, GOOD, bold=True).next_to(big, RIGHT, buff=0.5)
        vs = tx(f"worth going on: -${-U['small']:,.0f}m", 18, BAD, bold=True).next_to(small, RIGHT, buff=0.5)
        tag = estimate_tag("the Works: BIO's success rates, illustrative costs and markets, 10.5% cost of capital", size=12)
        beat(self,
             "Your candidate drug has passed Phase II: it seems to work in a few hundred patients. The trial also told "
             "you something about the market. <bookmark mark='a'/> There is a thirty per cent chance it is a big one, "
             "three billion dollars of sales a year at its peak, <bookmark mark='b'/> and a seventy per cent chance it is a "
             "small one, a hundred and fifty million. <bookmark mark='c'/> Phase III, the large trial that proves the drug "
             f"to the regulator, costs {U['p3']:.0f} million dollars and succeeds about {100 * U['q3']:.0f} per cent of "
             "the time. <bookmark mark='d'/> If the market is big, going on is worth about "
             f"{U['big'] / 1e3:.1f} billion dollars today. <bookmark mark='e'/> If it is small, going on loses "
             f"{-U['small']:.0f} million.",
             base=[root, tag], steps=[[a1, big], [a2, small], p3, vb, vs])

    def answer(self):
        U = R["run"]
        c = stat_cards([(f"${U['commit'] / 1e3:.2f}bn", "go on with every drug that passes Phase II", GREY_A),
                        (f"${U['flexible'] / 1e3:.2f}bn", "go on only where the market is big", GOOD),
                        (f"${U['option']:.0f}m", "the value of being free to stop", PRICE)], y=0.6, size=40, span=12)
        note = tx("Each stage of a drug's development buys information, and the right to stop.", 19, WHITE, bold=True).move_to([0, -1.6, 0])
        tag = estimate_tag("the Works' Phase III decision", size=12)
        beat(self,
             "So what is the candidate worth before you know? <bookmark mark='a'/> If you promise to run Phase III "
             f"whatever the market, about {U['commit'] / 1e3:.2f} billion dollars. <bookmark mark='b'/> If you keep the "
             f"right to stop when the market turns out small, {U['flexible'] / 1e3:.2f} billion. <bookmark mark='c'/> The "
             f"difference, {U['option']:.0f} million dollars, is the value of the option to stop. <bookmark mark='d'/> "
             "That is how drug companies think about their pipelines: every stage is a payment for information, and the "
             "best decision a company makes is often to kill a drug early, before the expensive trial.",
             base=[tag], steps=[c[0], c[1], c[2], note])
