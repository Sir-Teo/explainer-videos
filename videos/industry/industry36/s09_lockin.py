from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403


class Lockin(VoiceoverScene):
    def construct(self):
        card(self, 7, "Lock-in and platforms", "Why do customers so rarely leave?",
             "Chapter seven. Lock-in and platforms. The whole business rests on customers staying. Here is why they do, and "
             "what it is worth.", lit=("moat",))
        self.web()
        self.churn()
        self.bundle()
        self.open_()

    def web(self):
        hub = VGroup(RoundedRectangle(corner_radius=0.15, width=3.0, height=1.0, stroke_width=0, fill_color=SUB, fill_opacity=1),
                     tx("the system of record", 18, "#1B2230", bold=True)).move_to([0, 0.2, 0])
        hub[1].move_to(hub[0])
        spokes = [("the company's data, years of it", -4.2, 2.0), ("integrations with other systems", 4.2, 2.0),
                  ("staff trained to use it", -4.2, -1.6), ("custom workflows and reports", 4.2, -1.6)]
        g = VGroup()
        for text, x, y in spokes:
            b = VGroup(RoundedRectangle(corner_radius=0.1, width=3.4, height=0.7, stroke_color=STOCK, stroke_width=2, fill_opacity=0),
                       tx(text, 15, STOCK))
            b[1].move_to(b[0])
            b.move_to([x, y, 0])
            g.add(VGroup(Line(hub.get_center(), b.get_center(), color=GREY_B, stroke_width=2).set_z_index(-1), b))
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Think of the software a company keeps its customers, its staff or its money in: the system of record. "
             "<bookmark mark='a'/> Leaving it means moving years of data, <bookmark mark='b'/> rebuilding every connection "
             "to the other systems that feed it, <bookmark mark='c'/> retraining every person who uses it, <bookmark mark='d'/> "
             "and recreating the workflows and reports built up around it. None of that appears on the price list, and all of "
             "it is a reason to stay.",
             base=[hub, tag], steps=list(g))

    def churn(self):
        Cs = R["run"]["churn_sens"]
        items = [(f"{100 * c:.0f}% of ARR lost a year", v / 1e6, SUB if c <= 0.08 else LOSS, mn(v)) for c, v in Cs.items()]
        rows = hbars(items, max_value=560, x0=0.4, top=1.6, row=0.9, length=5.2, size=17, bar_h=0.5)
        hd = tx("the Works' company: ARR after five years, by its churn", 21, WHITE, bold=True).to_edge(UP, buff=0.7)
        tag = estimate_tag("the Works: everything else unchanged", size=12)
        ks = list(Cs)
        beat(self,
             "What is staying worth? <bookmark mark='a'/> In the Works, if customers leave at four per cent of revenue a "
             f"year, ARR after five years is {Cs[ks[0]] / 1e6:.0f} million dollars. <bookmark mark='b'/> At eight per cent, our "
             f"company, {Cs[ks[1]] / 1e6:.0f} million. <bookmark mark='c'/> At twelve, {Cs[ks[2]] / 1e6:.0f}. "
             f"<bookmark mark='d'/> At sixteen, {Cs[ks[3]] / 1e6:.0f}. The same sales team and the same product: the "
             f"company that keeps its customers ends up {100 * (Cs[ks[0]] / Cs[ks[3]] - 1):.0f} per cent larger than the one "
             "that loses them.",
             base=[rows.axis, hd, tag], steps=list(rows))

    def bundle(self):
        Pl = R["platform"]
        c = stat_cards([(f"+{Pl['seats']}%", "Microsoft 365 Commercial seats, fiscal 2026", GA),
                        ("+17%", "Microsoft 365 Commercial cloud revenue", SUB),
                        ("Copilot, E5", "Microsoft's reasons: revenue per user", STOCK)], y=0.6, size=36, span=12)
        note = tx("'growth in revenue per user driven by Microsoft 365 Copilot and Microsoft 365 E5'", 16, GREY_B).move_to([0, -1.6, 0])
        src = source("Microsoft, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "Lock-in lets a seller sell more to the same people. <bookmark mark='a'/> Microsoft's count of paying business "
             f"users of Microsoft 365 grew {Pl['seats']} per cent in its last fiscal year. <bookmark mark='b'/> The revenue "
             "from them grew 17 per cent. <bookmark mark='c'/> The difference is more per user: Microsoft credits its AI "
             "assistant, Copilot, and E5, its most expensive bundle. In this series' reading, email, documents, video calls and "
             "security sold as one subscription make each extra piece cheap to add and each rival's single product hard to choose.",
             base=[src], steps=list(c) + [note])

    def open_(self):
        lines = [("operating systems and app stores: whoever owns the platform taxes what runs on it", STOCK),
                 ("open source: code anyone may copy, sold as a hosted service or with support", ENG),
                 ("the clouds: the hosting itself, the subject of Part 37", SUB),
                 ("vertical software: one industry's system of record, from hospitals to councils", PROFIT)]
        g = VGroup(*[tx(t, 18, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.1, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "Four more kinds of lock-in, in this series' reading. <bookmark mark='a'/> Platforms: whoever owns the operating "
             "system or the app store can charge everything that runs on it. <bookmark mark='b'/> Open source: code anyone may "
             "copy for free, which companies like MongoDB and GitLab sell as a hosted service with extras. "
             "<bookmark mark='c'/> The clouds, which host everyone else's software, and are Part 37. <bookmark mark='d'/> And "
             "vertical software, the system of record for one industry, from drug trials to town halls, where a specialist can "
             "own a whole niche.",
             base=[head("Other ways to stay")], steps=list(g))
