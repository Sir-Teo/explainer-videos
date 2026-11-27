from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Drug(VoiceoverScene):
    def construct(self):
        card(self, 5, "A drug's life", "How does a medicine earn back its cost, and when does it stop?",
             "Chapter five. A drug's life, from launch to the day its protection ends.", lit=("dollar", "moat"))
        self.curve()
        self.split()
        self.patent()

    def split(self):
        Dsp = R["drug_split"]
        D = R["drug"]
        a = Rectangle(width=10.0 * Dsp["before"], height=0.9, stroke_width=0, fill_color=BRAND, fill_opacity=0.9)
        b = Rectangle(width=10.0 * (1 - Dsp["before"]), height=0.9, stroke_width=0, fill_color=GENERIC, fill_opacity=0.9)
        VGroup(a, b).arrange(RIGHT, buff=0).move_to([0, 0.6, 0])
        a.grow = LEFT
        b.grow = LEFT
        la = tx(f"the protected years: {100 * Dsp['before']:.0f}%", 18, BRAND, bold=True).next_to(a, DOWN, buff=0.2)
        lb = tx(f"after: {100 * (1 - Dsp['before']):.0f}%", 16, GENERIC).next_to(b, UP, buff=0.2)
        hd = tx("where a drug's value comes from (the Works, discounted)", 18, WHITE, bold=True).to_edge(UP, buff=0.9)
        tag = estimate_tag(f"the Works' drug: {D['excl']} years of exclusivity, then the cliff", size=12)
        beat(self,
             "Split that value in two. <bookmark mark='a'/> Almost all of it, "
             f"{100 * Dsp['before']:.0f} per cent, is earned while the drug is protected. <bookmark mark='b'/> The years "
             f"after the cliff add {100 * (1 - Dsp['before']):.0f} per cent. For the company that invented it, a drug is "
             "worth what it earns before its date, and every year of protection lost to a slow trial is a year of that "
             "value gone.",
             base=[hd, tag], steps=[[a, la], [b, lb]])

    def curve(self):
        D = R["drug"]
        s = {t: v / 1e3 for t, v in enumerate(D["sales"])}
        ch = line_chart({"sales": (s, BRAND)}, x=(0, 19), y=(0, 2.4), xticks=[0, 5, 10, 12, 15, 19],
                        yticks=[0, 0.5, 1.0, 1.5, 2.0], xfmt=lambda v: f"year {int(v) + 1}", yfmt=lambda v: f"${v:.1f}bn",
                        ylabel="a drug's sales after launch (the Works)", width=9.6, height=4.3, center=(-0.6, -0.45),
                        label_end=False)
        ax = ch.ax
        ramp = poly(ax, [(t, s[t]) for t in range(0, D["ramp"])], BRAND, 4)
        plateau = poly(ax, [(t, s[t]) for t in range(D["ramp"] - 1, D["excl"])], BRAND, 4)
        drop = poly(ax, [(t, s[t]) for t in range(D["excl"] - 1, 20)], GENERIC, 4)
        loe = DashedLine(ax.c2p(D["excl"] - 0.5, 0), ax.c2p(D["excl"] - 0.5, 2.3), stroke_color=BAD, stroke_width=2, dash_length=0.08)
        ll = tx("exclusivity ends", 15, BAD, bold=True).next_to(ax.c2p(D["excl"] - 0.5, 2.3), RIGHT, buff=0.1)
        npv = tx(f"worth ${D['npv'] / 1e3:.1f}bn at launch, at a {100 * D['margin']:.0f}% margin and 10.5%", 16, PRICE, bold=True).move_to([0.6, 1.9, 0])
        tag = estimate_tag(f"the Works: ${D['peak'] / 1e3:.0f}bn peak after {D['ramp']} years, {D['excl']} years of exclusivity", size=12)
        beat(self,
             "Here is an approved drug's life in our model. <bookmark mark='a'/> Sales climb for "
             f"{D['ramp']} years as doctors learn to prescribe it, to a peak of {D['peak'] / 1e3:.0f} billion dollars a "
             "year. <bookmark mark='b'/> They stay there as long as the drug is protected. <bookmark mark='c'/> Then its "
             f"exclusivity ends, generic copies arrive, and sales fall away: to {100 * D['cliff'][0]:.0f} per cent in the "
             f"first year and {100 * D['cliff'][1]:.0f} in the second. <bookmark mark='d'/> Discounted to the day of "
             f"launch, that life is worth about {D['npv'] / 1e3:.1f} billion dollars: enough to pay for one approved "
             "drug's share of the failures, with room to spare. A blockbuster pays for the misses.",
             base=[ch.frame, tag], steps=[ramp, plateau, [loe, ll, drop], npv])

    def patent(self):
        p = VGroup(Rectangle(width=10.0, height=0.7, stroke_color=GREY_B, stroke_width=2, fill_opacity=0).move_to([0, 0.8, 0]))
        used = Rectangle(width=5.2, height=0.7, stroke_width=0, fill_color=GREY_B, fill_opacity=0.5).move_to([-2.4, 0.8, 0])
        used.grow = LEFT
        left = Rectangle(width=4.8, height=0.7, stroke_width=0, fill_color=BRAND, fill_opacity=0.9).move_to([2.6, 0.8, 0])
        left.grow = LEFT
        lu = tx("spent in the laboratory and the trials", 15, GREY_A).next_to(used, DOWN, buff=0.15)
        ll = tx("left to sell under protection", 15, BRAND, bold=True).next_to(left, DOWN, buff=0.15)
        hd = tx("a patent is filed early, and its clock runs during the trials", 18, WHITE, bold=True).next_to(p, UP, buff=0.35)
        q = quote(["'Loss of patent protection for one of the Company's products typically leads to a significant and rapid",
                   "loss of sales for that product as lower priced generic or biosimilar versions become available.'"],
                  "Merck & Co., Form 10-K 2025", size=15, width=11.5).move_to([0, -1.8, 0])
        src = source("Merck & Co., Inc., Form 10-K 2025", size=12)
        beat(self,
             "Why does protection end so soon? <bookmark mark='a'/> A company patents its molecule early, before the "
             "trials, because others are searching too. The patent's clock starts then. <bookmark mark='b'/> A decade of "
             "trials uses up much of it, <bookmark mark='c'/> and what is left is the time the drug has to earn back its "
             "cost. Patent law gives some of the lost time back, and companies hold later patents too; Merck's table "
             "shows two more Keytruda patents running a year beyond the first, which it expects rivals to challenge in "
             "court. But the end always comes. <bookmark mark='d'/> Merck's annual report says it plainly: losing "
             "a patent typically means a significant and rapid loss of sales.",
             base=[p, hd, src], steps=[used, lu, [left, ll], q])
