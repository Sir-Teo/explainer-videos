from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 9, "Called it?", "What did the deregulators promise, and what does an airline know about its own year?",
             "Chapter nine. Called it? A law's promise in 1978, an airline's forecast in 2026, and our own call.", lit=("change",))
        self.law()
        self.delta()
        self.ours()

    def law(self):
        q = quote(["'An Act ... to encourage, develop, and attain an air transportation system which relies on competitive",
                   "market forces to determine the quality, variety, and price of air services'"],
                  "Airline Deregulation Act, Public Law 95-504, 24 October 1978", size=18).move_to([0, 1.6, 0])
        H = R["hook"]
        g = bullets([f"price: after inflation, fares in 2025 were {100 * (1 - H['real'][2025]):.0f}% below 2000's, by the CPI",
                     f"variety: {R['traffic']['enplane'][2025]:.0f} million boardings a year on American airlines in 2025",
                     f"and the airlines? {100 * H['total'] / H['total_rev']:.1f} cents of profit a dollar over 2009-2025"],
                    size=18).move_to([0, -0.9, 0])
        src = source("Public Law 95-504 (govinfo); BLS CPI and BTS enplanements via FRED; Forms 10-K via SEC company facts", size=12)
        beat(self,
             "First, the law that made the modern industry. <bookmark mark='a'/> In October 1978 Congress passed the Airline "
             "Deregulation Act, aiming at a system that 'relies on competitive market forces to determine the quality, variety, "
             "and price of air services'. <bookmark mark='b'/> On price and variety it "
             "delivered: fares far below what they were, and almost a billion boardings a year. On the airlines themselves, it "
             "promised nothing, and they have kept about three cents in the dollar.",
             base=[src], steps=[q, g])

    def delta(self):
        C = R["called"]
        pa = viz.plot_axes([4.0, 8.0], [0, 2], x_length=9.6, y_length=2.4, xticks=[4, 5, 6, 7, 8], xfmt=lambda v: f"${v:.0f}",
                           grid=False, size=13).move_to([0.4, 0.2, 0])
        ax = pa.ax
        b1 = Line(ax.c2p(C["jan"][0], 1.5), ax.c2p(C["jan"][1], 1.5), stroke_color=BIZ, stroke_width=16)
        l1 = tx(f"January 2026: ${C['jan'][0]:.2f}-{C['jan'][1]:.2f} a share", 16, BIZ, bold=True).next_to(b1, UP, buff=0.12)
        b2 = Line(ax.c2p(C["oct"][0], 0.5), ax.c2p(C["oct"][1], 0.5), stroke_color=BAD, stroke_width=16)
        l2 = tx(f"October 2026: ${C['oct'][0]:.2f}-{C['oct'][1]:.2f}", 16, BAD, bold=True).next_to(b2, DOWN, buff=0.12)
        lab = tx("Delta's forecast of its 2026 earnings per share", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Delta Air Lines, results releases of 13 January and 9 October 2026 (Forms 8-K)", size=12)
        beat(self,
             "Then Delta's own forecast. <bookmark mark='a'/> In January 2026 it expected to earn "
             f"{C['jan'][0]:.2f} to {C['jan'][1]:.2f} dollars a share, twenty per cent more than in 2025, and in July it "
             f"repeated that range. <bookmark mark='b'/> In October it cut it to {C['oct'][0]:.2f} to {C['oct'][1]:.2f}, "
             f"having absorbed a {C['hit']:.0f} billion dollar rise in fuel. A well-run airline, forecasting its own year from "
             "inside it, was wrong by about a quarter, because of oil.",
             base=[pa, lab, src], steps=[[b1, l1], [b2, l2]])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, BIZ, bold=True),
                       tx(f"Jet fuel on the US Gulf Coast will average more than ${C['line']:.2f} a gallon", 22, WHITE, bold=True),
                       tx("over the whole of 2027.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, BIZ, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets([f"for: ${C['jet26']:.2f} a gallon on average in the first {C['jet26_n']} months of 2026, with Hormuz all but shut",
                       f"against: ${C['jet25']:.2f} in 2025; disruptions end, and high prices bring more supply",
                       "against: Frontline expects Middle East production to be restored"], size=18).move_to([0, -0.5, 0])
        rule = tx("scored on the EIA's monthly Gulf Coast jet fuel price (FRED: MJFUELUSGULF), averaged over 2027", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             "Now ours, on the cost airlines cannot control. <bookmark mark='a'/> We say jet fuel on the American Gulf Coast "
             f"will average more than {C['line']:.0f} dollars a gallon over 2027, and give it {100 * C['prob']:.0f} per cent: "
             f"less likely than not. <bookmark mark='b'/> For: it averaged {C['jet26']:.2f} in 2026 so far, with the Strait of "
             f"Hormuz all but shut. Against: it averaged {C['jet25']:.2f} in 2025; disruptions end, high prices bring out "
             "more oil, and the tanker owner Frontline expects the Gulf's production to be restored. <bookmark mark='c'/> The "
             "Energy Information Administration's monthly prices will settle it.",
             base=[tag], steps=[claim, why, rule])
        self.watch()

    def watch(self):
        g = VGroup(tx("What to watch, whichever way the call goes", 22, WHITE, bold=True),
                   tx("fares: whether airlines keep the 2026 increases once fuel falls", 18, SKY),
                   tx("seats: whether they cut flights to keep planes full", 18, BIZ),
                   tx("cards: whether the banks' payments keep growing in a slower economy", 18, CARD)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Whichever way it goes, three things will tell you how the airlines are doing. <bookmark mark='a'/> Fares: "
             "whether the increases of 2026 stick once fuel gets cheaper. <bookmark mark='b'/> Seats: whether the airlines "
             "cut flying to keep their planes full. <bookmark mark='c'/> And the cards: whether the banks keep paying more for "
             "miles if the economy slows. Those three numbers, more than any forecast, decide whether this industry's "
             "next decade looks like its last.",
             base=[tag], steps=[g[:2], g[2], g[3]])
