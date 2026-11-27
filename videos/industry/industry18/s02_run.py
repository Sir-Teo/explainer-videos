from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403


def cell(v: float) -> str:
    return f"${v:.1f}bn"


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: a new airliner or new engines", "Your rival is deciding too. Do you build a new plane?",
             "Chapter one. Run it. You make airliners, and so does your rival. Do you build a new plane, or hang new "
             "engines on the old one?", lit=("make", "moat"))
        self.options()
        self.matrix()
        self.flip()

    def options(self):
        U = R["run"]
        o = U["options"]
        cards = VGroup()
        for i, (k, col) in enumerate((("new", AIRBUS), ("reengine", BOEING))):
            v = o[k]
            g = VGroup(draw.plane(3.8, col), tx(v["label"], 24, col, bold=True),
                       tx(f"development: ${v['dev'] / 1e9:.0f}bn", 21, WHITE),
                       tx(f"first delivery after {v['years']} years", 21, WHITE),
                       tx(f"burns {100 * v['gain']:.0f}% less fuel", 22, PRICE, bold=True)).arrange(DOWN, buff=0.2)
            cards.add(g.move_to([-3.4 + 6.8 * i, 0.5, 0]))
        mk = tx(f"the market: {U['market']:,.0f} aircraft a year for {U['horizon']} years; ${U['margin']:.0f}m margin "
                "on each", 19, GREY_A).to_edge(DOWN, buff=0.85)
        tag = estimate_tag("the Works' duel: illustrative numbers", size=13)
        beat(self,
             "You make single-aisle airliners, the hundred-and-fifty to two-hundred-seat jets that fly most of the world's "
             "flights, and so does one rival. Fuel is an airline's biggest bill it can choose to cut, and new engines are "
             "on offer. <bookmark mark='a'/> You can design a new airliner around them: in this model, twenty billion "
             "dollars, seven years to the first delivery, and twenty per cent less fuel. <bookmark mark='b'/> Or you can "
             "hang the new engines on the airliner you already build: three billion, four years, fourteen per cent. "
             "<bookmark mark='c'/> Airlines buy whichever burns less fuel, so a few per cent moves a lot of orders. And "
             "your rival faces the same choice, at the same time.",
             base=[tag], steps=[cards[0], cards[1], mk])

    def _matrix(self, T, x0=-3.0, y0=0.1):
        cw, ch = 4.0, 1.7
        cells = {}
        for i, me in enumerate(("new", "reengine")):
            for j, them in enumerate(("new", "reengine")):
                c = np.array([x0 + cw * (j + 0.5), y0 + ch * (0.5 - i), 0])
                box = Rectangle(width=cw, height=ch, stroke_color=GREY_B, stroke_width=2, fill_color="#141A24", fill_opacity=1).move_to(c)
                mine, theirs = T[f"{me}|{them}"]
                inner = VGroup(VGroup(tx("you", 15, YOU), tx(cell(mine), 26, YOU, bold=True)).arrange(DOWN, buff=0.05),
                               VGroup(tx("rival", 15, RIVAL), tx(cell(theirs), 26, RIVAL, bold=True)).arrange(DOWN, buff=0.05)).arrange(RIGHT, buff=0.5).move_to(c)
                cells[(me, them)] = VGroup(box, inner)
        rows = VGroup(tx("you: new plane", 19, YOU, bold=True).move_to([x0 - 0.2, y0 + ch / 2, 0], aligned_edge=RIGHT),
                      tx("you: new engines", 19, YOU, bold=True).move_to([x0 - 0.2, y0 - ch / 2, 0], aligned_edge=RIGHT))
        cols = VGroup(tx("rival: new plane", 19, RIVAL, bold=True).move_to([x0 + cw / 2, y0 + ch + 0.3, 0]),
                      tx("rival: new engines", 19, RIVAL, bold=True).move_to([x0 + 1.5 * cw, y0 + ch + 0.3, 0]))
        return cells, VGroup(*[c[0] for c in cells.values()], rows, cols)

    def matrix(self):
        U = R["run"]
        T = U["table"]
        cells, frame = self._matrix(T)
        verdict = tx("New engines is the better reply whatever the rival does: both re-engine.", 18, PRICE, bold=True).to_edge(DOWN, buff=0.55)
        tag = estimate_tag("the Works' duel: value today of each programme, illustrative", size=12)
        rr, nr, rn, nn = (T[k] for k in ("reengine|reengine", "new|reengine", "reengine|new", "new|new"))
        beat(self,
             "Here are the four outcomes, each programme's value today. <bookmark mark='a'/> If you both re-engine, you "
             f"split the market and each programme is worth about {rr[0]:.0f} billion dollars. <bookmark mark='b'/> If you "
             "design a new plane while the rival re-engines, the rival's re-engined jet arrives three years before yours and "
             f"takes the orders in between: your programme is worth {nr[0]:.0f} billion, the rival's {nr[1]:.0f}. "
             "<bookmark mark='c'/> The mirror image if the rival goes new. <bookmark mark='d'/> And if you both go new, you "
             f"both spend twenty billion and wait seven years, for {nn[0]:.0f} billion each. <bookmark mark='e'/> Whatever "
             "the rival does, re-engining is your better reply. In 2010 and 2011 the real duopoly made exactly this choice: "
             "Airbus put new engines on its A320 and Boeing on its 737, which became the 737 MAX.",
             base=[frame, tag], steps=[cells[("reengine", "reengine")][1], cells[("new", "reengine")][1],
                                      cells[("reengine", "new")][1], cells[("new", "new")][1], verdict])

    def flip(self):
        U = R["run"]
        A = U["alt"]
        cells, frame = self._matrix(A)
        verdict = tx("A bigger leap flips it: both build new planes, and both end worse off.", 18, BAD, bold=True).to_edge(DOWN, buff=0.55)
        ao = U["alt_options"]
        tag = estimate_tag(f"the same game with a new plane saving {100 * ao['new']['gain']:.0f}% and new engines "
                           f"{100 * ao['reengine']['gain']:.0f}%", size=12)
        nn, rr = A["new|new"], A["reengine|reengine"]
        beat(self,
             "Now change one number. <bookmark mark='a'/> Suppose the new airliner saves twenty-three per cent of fuel and "
             f"the re-engined one thirteen. <bookmark mark='b'/> Now a new plane is the better reply whatever the rival "
             f"does, so both build one, and both end with {nn[0]:.0f} billion instead of the {rr[0]:.0f} they would have had "
             "by both re-engining. <bookmark mark='c'/> Two makers watch each other, and a few points of fuel decide whether "
             "they launch twenty-billion-dollar bets. That is the shape of the whole industry, and the chapters that follow "
             "fill in the numbers.",
             base=[frame, tag], steps=[[c[1] for c in cells.values()][:2], [c[1] for c in cells.values()][2:], verdict])
