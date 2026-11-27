from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 10, "Called it?", "What did the railway law promise, what did the driverless trucks promise, and what is next?",
             "Chapter ten. Called it? A law's purpose in 1980, a company's launch date in 2022, and our own call on the "
             "biggest railway merger in a generation.", lit=("change",))
        self.law()
        self.aurora()
        self.ours()

    def law(self):
        q = quote(["'The purpose of this Act is to provide for the restoration, maintenance, and improvement of the physical",
                   "facilities and financial stability of the rail system of the United States.'"],
                  "the Staggers Rail Act of 1980, section 3", size=18).move_to([0, 1.6, 0])
        H = R["hook"]["ors"]
        Rl = R["rail"]["real"]
        g = bullets([f"financial stability: Union Pacific's operating ratio {H['Union Pacific'][2009]:.0f}% in 2009, {H['Union Pacific'][2025]:.1f}% in 2025",
                     f"for shippers: rail prices after inflation {100 * (1 - Rl[2025]):.0f}% below 1981's in 2025, by the BLS's index",
                     "and the regulator still watches the captive shipper and every merger"], size=18).move_to([0, -0.9, 0])
        src = source("Public Law 96-448 (govinfo); Forms 10-K via SEC company facts; BLS PPI and CPI via FRED", size=12)
        beat(self,
             "First, the law. <bookmark mark='a'/> The Staggers Act's stated purpose was 'the restoration, maintenance, and "
             "improvement of the physical facilities and financial stability' of America's railways. "
             "<bookmark mark='b'/> On financial stability it succeeded beyond anything its authors described: the railways "
             "went from the lowest earnings of any mode to the highest of any business in this film. Shippers pay less after inflation than in 1981, "
             "though more than at the low of 2001.",
             base=[src], steps=[q, g])

    def aurora(self):
        C = R["called"]
        pa = viz.plot_axes([2022, 2028.5], [0, 2], x_length=9.6, y_length=2.4, xticks=[2022, 2023, 2024, 2025, 2026, 2027, 2028],
                           xfmt=lambda v: f"{int(v)}", grid=False, size=13).move_to([0.4, 0.2, 0])
        ax = pa.ax
        d1 = Dot(ax.c2p(2023.85, 1.4), radius=0.12, color=SKY)
        l1 = tx("promised: late 2023", 16, SKY, bold=True).next_to(d1, UP, buff=0.12)
        d2 = Dot(ax.c2p(2025.3, 0.6), radius=0.12, color=GOOD)
        l2 = tx("launched: April 2025", 16, GOOD, bold=True).next_to(d2, DOWN, buff=0.12)
        d3 = Dot(ax.c2p(2027.95, 1.4), radius=0.12, color=FUEL)
        l3 = tx(f"next promise: {C['target']:,.0f}+ trucks by end-2027", 16, FUEL, bold=True).next_to(d3, UP, buff=0.12).shift(LEFT * 1.0)
        lab = tx("Aurora's driverless trucks: what it said, and what happened", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Aurora Innovation, Forms 10-K for 2021 and 2025; third-quarter 2026 shareholder letter", size=12)
        beat(self,
             "Then Aurora's own forecasts. <bookmark mark='a'/> In 2022 it said driverless trucks would launch in late "
             "2023. <bookmark mark='b'/> They launched in April 2025: right about the thing, wrong about the date, as "
             "forecasts of new technology usually are. <bookmark mark='c'/> Its next promise is more than a thousand "
             "driverless trucks running by the end of 2027, from twenty or so today, with its production 'about six weeks "
             "behind' its plan in October. We will score that one in 2028.",
             base=[pa, lab, src], steps=[[d1, l1], [d2, l2], [d3, l3]])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, RAIL, bold=True),
                       tx("Union Pacific will complete its purchase of Norfolk Southern", 22, WHITE, bold=True),
                       tx("on or before 31 December 2027.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, RAIL, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets(["for: both boards and both sets of shareholders approved; the regulator accepted the revised application",
                       "for: the companies expect to complete it 'in the second half of 2027'",
                       "against: the first application was rejected as incomplete; opponents asked for dismissal",
                       "against: a review this large, with conditions to negotiate, can run past the end of 2027"],
                      size=16).move_to([0, -0.7, 0])
        rule = tx("scored on Union Pacific's announcements: true if the acquisition is completed by 31 December 2027", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             "Now ours. In July 2025 Union Pacific agreed to buy Norfolk Southern for one of its shares and "
             f"{C['price']:.2f} dollars in cash for each Norfolk Southern share, to make the first railway from coast to "
             "coast, more than fifty thousand miles of route across forty-three states. <bookmark mark='a'/> We say it will be completed by the end of 2027, and give it "
             f"{100 * C['prob']:.0f} per cent. <bookmark mark='b'/> For: the shareholders approved, the Surface "
             "Transportation Board accepted the revised application in May 2026 and set a schedule, and the companies "
             "expect to finish in the second half of 2027. Against: the board rejected the first application as "
             "incomplete, other parties have asked it to dismiss the case, and in this series' reading a review of this "
             "size, with conditions to negotiate, can easily run into 2028. <bookmark mark='c'/> Union Pacific's "
             "announcements will settle it.",
             base=[tag], steps=[claim, why, rule])
