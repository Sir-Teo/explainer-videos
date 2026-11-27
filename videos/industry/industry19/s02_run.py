from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: the tender", "Cut your price to win the fleet, or hold it?",
             "Chapter one. Run it. A customer wants a fleet of machines, and you and a rival are bidding. Do you cut your "
             "price to win, or hold it?", lit=("dollar", "moat"))
        self.setup_()
        self.matrix(R["run"]["table"], "high")
        self.matrix(R["run"]["low"], "low")
        self.floor()

    def floor(self):
        U = R["run"]
        pa = viz.plot_axes([0, 6], [0, 1.5], x_length=9.0, y_length=4.0, xticks=[0, 1, 2, 3, 4, 5, 6],
                           yticks=[0, 0.4, 0.8, 1.0, 1.2], xfmt=lambda v: f"round {int(v)}", yfmt=lambda v: f"${v:.1f}m",
                           ylabel="the winning bid per machine, as the makers undercut each other", size=13).move_to([-0.6, -0.45, 0])
        ax = pa.ax
        bids = [1.3, 1.15, 1.0, 0.85, 0.7, 0.55, U["floor"]]
        steps_ = []
        for i, b in enumerate(bids):
            col = YOU if i % 2 == 0 else RIVAL
            d = Dot(ax.c2p(i, b), radius=0.1, color=col)
            ln = Line(ax.c2p(i - 1, bids[i - 1]), ax.c2p(i, b), stroke_color=GREY_B, stroke_width=2) if i else VGroup()
            steps_.append(VGroup(ln, d))
        cost = DashedLine(ax.c2p(0, U["cost"]), ax.c2p(6, U["cost"]), stroke_color=BAD, stroke_width=1.5, dash_length=0.08)
        cl = tx(f"cost to build: ${U['cost']:.1f}m", 14, BAD, bold=True).next_to(ax.c2p(6, U["cost"]), UP, buff=0.08).shift(LEFT * 0.8)
        fl = DashedLine(ax.c2p(0, U["floor"]), ax.c2p(6, U["floor"]), stroke_color=SERVICE, stroke_width=1.5, dash_length=0.08)
        fll = tx(f"the floor: cost less servicing, ${U['floor']:.1f}m", 14, SERVICE, bold=True).next_to(ax.c2p(3, U["floor"]), DOWN, buff=0.1)
        tag = estimate_tag("the Works' tender with free bidding: each undercut wins the fleet", size=12)
        beat(self,
             "And if the makers could bid any price, not just two? <bookmark mark='a'/> You bid one point three million. "
             "<bookmark mark='b'/> Your rival undercuts you and takes the fleet. <bookmark mark='c'/> You undercut back. "
             "Each round, the lower bid wins everything, so each maker keeps cutting <bookmark mark='d'/> below the cost "
             "of building the machine, <bookmark mark='e'/> until the price reaches the cost less the value of the "
             f"servicing: {U['floor']:.1f} million dollars, where winning is worth nothing more than losing. In this "
             "model every dollar the servicing will earn is given back at the sale. Real makers stop short of that, but "
             "the pull is in that direction.",
             base=[pa, cost, cl, fl, fll, tag], steps=[steps_[0], steps_[1], steps_[2], [steps_[3], steps_[4]], [steps_[5], steps_[6]]])

    def setup_(self):
        U = R["run"]
        fleet = VGroup(*[draw.excavator(0.7, MACHINE).move_to([-6.2 + 0.78 * (i % 10), 2.1 - 0.5 * (i // 10), 0]) for i in range(20)])
        fl = tx(f"the customer's fleet: {U['fleet']} machines (each icon: five)", 17, MACHINE, bold=True).next_to(fleet, DOWN, buff=0.2).align_to(fleet, LEFT)
        facts = VGroup(tx(f"each costs you ${U['cost']:.1f}m to build", 21, WHITE),
                       tx(f"bid high: ${U['hold']:.1f}m a machine, or cut: ${U['cut']:.1f}m", 21, PRICE, bold=True),
                       tx("the lower bid wins the whole fleet; a tie splits it", 21, WHITE),
                       tx(f"then parts and service: worth ${U['service']:.1f}m a machine, today, to whoever sold it", 21, SERVICE, bold=True)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([0.0, -1.0, 0])
        tag = estimate_tag("the Works' tender: illustrative numbers", size=13)
        beat(self,
             f"A mining company wants {U['fleet']} new machines, and two makers bid. <bookmark mark='a'/> Each machine "
             f"costs you {U['cost']:.0f} million dollars to build. <bookmark mark='b'/> You can bid "
             f"{U['hold']:.1f} million a machine, or cut to {U['cut']:.1f}, below your cost. <bookmark mark='c'/> The lower "
             "bid wins the whole fleet. <bookmark mark='d'/> And here is the catch: whoever sells the machines will sell "
             f"their parts and service for the next fifteen years, worth {U['service']:.1f} million a machine in today's "
             "money. It is the engine maker's bargain from Part 18, played out at the size of a whole fleet.",
             base=[fleet, fl, tag], steps=list(facts))

    def matrix(self, T, kind):
        U = R["run"]
        x0, y0, cw, ch = -3.0, 0.3, 4.0, 1.6
        cells = {}
        for i, me in enumerate(("hold", "cut")):
            for j, them in enumerate(("hold", "cut")):
                c = np.array([x0 + cw * (j + 0.5), y0 + ch * (0.5 - i), 0])
                box = Rectangle(width=cw, height=ch, stroke_color=GREY_B, stroke_width=2, fill_color="#141A24", fill_opacity=1).move_to(c)
                mine, theirs = T[f"{me}|{them}"]
                inner = VGroup(VGroup(tx("you", 15, YOU), tx(f"${mine:.0f}m", 26, YOU, bold=True)).arrange(DOWN, buff=0.05),
                               VGroup(tx("rival", 15, RIVAL), tx(f"${theirs:.0f}m", 26, RIVAL, bold=True)).arrange(DOWN, buff=0.05)).arrange(RIGHT, buff=0.5).move_to(c)
                cells[(me, them)] = VGroup(box, inner)
        rows = VGroup(tx("you hold", 19, YOU, bold=True).move_to([x0 - 0.2, y0 + ch / 2, 0], aligned_edge=RIGHT),
                      tx("you cut", 19, YOU, bold=True).move_to([x0 - 0.2, y0 - ch / 2, 0], aligned_edge=RIGHT))
        cols = VGroup(tx("rival holds", 19, RIVAL, bold=True).move_to([x0 + cw / 2, y0 + ch + 0.3, 0]),
                      tx("rival cuts", 19, RIVAL, bold=True).move_to([x0 + 1.5 * cw, y0 + ch + 0.3, 0]))
        frame = VGroup(*[c[0] for c in cells.values()], rows, cols)
        hh, ch_, cc = T["hold|hold"], T["cut|hold"], T["cut|cut"]
        if kind == "high":
            verdict = tx("Cutting is the better reply either way: both cut, and both earn less.", 19, BAD, bold=True).to_edge(DOWN, buff=0.6)
            tag = estimate_tag("the Works' tender: value today of the machines and their servicing, $m", size=12)
            say = ("Here are the four outcomes, counting the machines and their servicing. <bookmark mark='a'/> If you both "
                   f"hold, you split the fleet and each makes {hh[0]:.0f} million. <bookmark mark='b'/> If you cut while the "
                   f"rival holds, you lose money on every machine but win all {U['fleet']} and their servicing: "
                   f"{ch_[0]:.0f} million, and the rival nothing. <bookmark mark='c'/> And if you both cut, you split it at "
                   f"the low price: {cc[0]:.0f} million each. <bookmark mark='d'/> Cutting is the better reply whatever the "
                   "rival does, so both cut, and the money the servicing will bring is handed to the customer at the sale. "
                   "When servicing is worth this much, machines are sold close to cost, or below it.")
            steps = [cells[("hold", "hold")][1], [cells[("cut", "hold")][1], cells[("hold", "cut")][1]],
                     cells[("cut", "cut")][1], verdict]
        else:
            verdict = tx("With a low attach rate, holding pays against a rival who holds.", 19, GOOD, bold=True).to_edge(DOWN, buff=0.6)
            tag = estimate_tag(f"the same tender when only {100 * U['low_attach']:.0f}% of owners buy service from the maker", size=12)
            say = ("Now change one thing. <bookmark mark='a'/> Suppose independent workshops take most of the servicing, "
                   f"and only {100 * U['low_attach']:.0f} per cent of owners buy parts and service from the maker. "
                   f"<bookmark mark='b'/> Then cutting wins the fleet but little after it: {ch_[0]:.0f} million against "
                   f"{hh[0]:.0f} if both hold. <bookmark mark='c'/> Holding the price is now the better reply to a rival "
                   "who holds. How much of the servicing a maker keeps, its attach rate, decides how hard it fights at the "
                   f"sale. In this model, above about {100 * U['threshold']:.0f} per cent, the fight is on.")
            ring = VGroup(SurroundingRectangle(cells[("cut", "hold")][0], color=PRICE, buff=0.0, stroke_width=4),
                          SurroundingRectangle(cells[("hold", "hold")][0], color=GOOD, buff=0.0, stroke_width=4))
            steps = [[c[1] for c in cells.values()], ring, verdict]
        beat(self, say, base=[frame, tag], steps=steps)
