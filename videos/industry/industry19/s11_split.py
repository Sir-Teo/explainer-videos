from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403


def node(text, col, size=17):
    t = tx(text, size, WHITE, bold=True)
    box = RoundedRectangle(corner_radius=0.12, width=t.width + 0.4, height=t.height + 0.3, stroke_color=col, stroke_width=2,
                           fill_color="#141A24", fill_opacity=1).move_to(t)
    return VGroup(box, t)


class Split(VoiceoverScene):
    def construct(self):
        card(self, 9, "The conglomerates come apart", "Why are the great industrial groups splitting up?",
             "Chapter nine. The conglomerates come apart. Some of the biggest industrial groups made a remarkable range of "
             "things under one roof. In four years three of the most famous broke themselves up.", lit=("change",))
        self.tree()
        self.why()
        self.vernova()

    def vernova(self):
        S = R["split"]
        m = {y: 100 * v for y, v in S["gev_m"].items() if y <= 2025}
        items = [(str(y), v, GOOD if v >= 0 else BAD, f"{v:.1f}%") for y, v in sorted(m.items())]
        rows = hbars(items, max_value=14, x0=-0.2, top=1.4, row=0.8, length=5.2, size=18, bar_h=0.5)
        src = source("GE Vernova, Forms 10-K via SEC company facts: net income attributable over revenue", size=12)
        beat(self,
             "And the pieces can change once they stand alone. <bookmark mark='a'/> GE Vernova lost money in 2022 and "
             f"2023, <bookmark mark='b'/> then kept {m[2024]:.1f} cents of each dollar in 2024, its first year on its own, "
             f"<bookmark mark='c'/> and {m[2025]:.1f} in 2025. Whether a separate management did that, or the market "
             "for its turbines and grid equipment did, the accounts alone cannot say.",
             base=[rows.axis, head("GE Vernova: net income as a share of revenue"), src],
             steps=[VGroup(rows[0], rows[1]), rows[2], rows[3]])

    def tree(self):
        S = R["split"]
        y = S["years"]
        cols = {"GE": BLUE, "3M": BAD, "Honeywell": PRICE}
        roots = {"GE": node("General Electric", cols["GE"], 19).move_to([-6.4, 2.2, 0], aligned_edge=LEFT),
                 "3M": node("3M", cols["3M"], 19).move_to([-1.6, 2.2, 0], aligned_edge=LEFT),
                 "Honeywell": node("Honeywell", cols["Honeywell"], 19).move_to([1.9, 2.2, 0], aligned_edge=LEFT)}
        kids = {
            "GE": [("GE HealthCare", f"January {y['ge_hc']}"), ("GE Vernova", f"April {y['ge_v']}"), ("GE Aerospace", "what remained")],
            "3M": [("Solventum", f"April {y['mmm']}"), ("3M", "what remained")],
            "Honeywell": [("Solstice", f"October {y['sol']}"), ("Honeywell Aerospace", f"June {y['hon']}"),
                          ("Honeywell Technologies", "what remained")],
        }
        steps_ = []
        for k in ("GE", "3M", "Honeywell"):
            g = VGroup()
            root = roots[k]
            sx = root.get_left()[0] + 0.3
            last_y = 0.9 - 1.1 * (len(kids[k]) - 1)
            g.add(Line([sx, root.get_bottom()[1], 0], [sx, last_y, 0], stroke_color=cols[k], stroke_width=2))
            for i, (name, when) in enumerate(kids[k]):
                ky = 0.9 - 1.1 * i
                nd = node(name, cols[k], 15)
                nd.move_to([sx + 0.4 + nd.width / 2, ky, 0])
                ln = Line([sx, ky, 0], nd.get_left(), stroke_color=cols[k], stroke_width=2)
                w = tx(when, 13, GREY_A).next_to(nd, DOWN, buff=0.05)
                g.add(VGroup(ln, nd, w))
            steps_.append(g)
        src = source("General Electric (GE Aerospace), Form 10-K 2025; 3M Company, Form 10-K 2025; Honeywell, Form 10-K 2025 "
                     "and Form 10-Q for the third quarter of 2026", size=12)
        beat(self,
             f"Three family trees. <bookmark mark='a'/> General Electric spun off its healthcare business in January {y['ge_hc']} and its power business, GE Vernova, "
             f"in April {y['ge_v']}; what remains is GE Aerospace, Part 18's engine maker. <bookmark mark='b'/> 3M spun "
             f"off its healthcare business, Solventum, in April {y['mmm']}. <bookmark mark='c'/> And Honeywell spun off "
             f"its materials business, Solstice, in October {y['sol']}, and its aerospace business in June {y['hon']}; "
             "the rest is now called Honeywell Technologies.",
             base=[*roots.values(), src], steps=steps_)

    def why(self):
        S = R["split"]
        q = quote(["'The separation of Honeywell Aerospace from Honeywell Technologies is intended, among other things,",
                   "to better position both companies to focus on and pursue opportunities for long-term growth and",
                   "profitability unique to each company's sector.'"], "Honeywell, Form 10-Q for the third quarter of 2026",
                  size=16, width=12).move_to([0, 1.4, 0])
        gev = S["gev"]
        last = max(gev)
        c = stat_cards([(f"${gev[last]:.1f}bn", f"GE Vernova's revenue, {last}, on its own", BLUE)],
                       y=-0.9, size=40, span=8)
        reasons = bullets(["each business gets its own board, its own capital and its own shareholders",
                           "investors choose what to own, instead of buying the whole group"], size=17).to_edge(DOWN, buff=0.8)
        src = source("Honeywell, Form 10-Q for the third quarter of 2026; GE Vernova, Form 10-K 2025 via SEC company facts", size=12)
        beat(self,
             "Why break up? The companies give the same answer. <bookmark mark='a'/> Honeywell said the split would let "
             "each company focus on the opportunities unique to its own sector. <bookmark mark='b'/> And the pieces are "
             f"big businesses in their own right: GE Vernova, the former energy business, had {gev[last]:.0f} billion "
             f"dollars of revenue in {last}. <bookmark mark='c'/> A separate company has its own board, its own capital "
             "and its own shareholders, who can buy the business they want without the rest. All three groups judged "
             "their businesses worth more apart than together.",
             base=[src], steps=[q, c, reasons])
