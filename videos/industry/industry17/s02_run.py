from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403


def money_m(v: float) -> str:
    return ("-" if v < 0 else "+") + f"${abs(v):,.0f}m"


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: the showroom duel", "Orders come in below plan. Hold the price, or pay a discount?",
             "Chapter one. Run it. You make a car; the orders are coming in below plan; your rival has the same problem. "
             "Hold the price, or pay a discount?", lit=("make", "moat"))
        self.plant()
        self.news()
        self.matrix()
        self.cut()

    def plant(self):
        U = R["run"]
        fac = draw.factory(2.6).move_to([-4.4, 1.2, 0])
        crews = VGroup(*[VGroup(*[draw.person(0.32, YOU) for _ in range(5)]).arrange(RIGHT, buff=0.04) for _ in range(2)]
                       ).arrange(DOWN, buff=0.12).next_to(fac, DOWN, buff=0.3)
        crew_l = tx("two shifts", 15, YOU).next_to(crews, DOWN, buff=0.1)
        car_ = draw.suv(1.8, YOU).move_to([-0.8, 1.6, 0])
        rows = [("list price", usd(U["price"]), WHITE),
                ("parts, materials, freight, warranty", usd(U["variable"]), SUPPLIER),
                ("left over on each car", usd(U["margin"]), PRICE),
                ("each shift, paid all year", f"${U['shift_cost']:.0f}m", YOU),
                ("tooling, engineering, overhead", f"${U['fixed']:.0f}m a year", GREY_A),
                ("capacity, two shifts", f"{U['capacity']:,.0f} cars a year", YOU)]
        tab = VGroup()
        for i, (k, v, c) in enumerate(rows):
            tab.add(VGroup(tx(k, 16, GREY_A), tx(v, 18, c, bold=True)).arrange(RIGHT, buff=0.3).move_to([2.6, 1.0 - 0.5 * i, 0], aligned_edge=RIGHT))
        for r_ in tab:
            r_.align_to(np.array([5.9, 0, 0]), RIGHT)
        be = VGroup(tx(f"break-even: {U['be']:,.0f} cars a year", 20, PRICE, bold=True),
                    tx(f"{100 * U['be_share']:.0f}% of what the plant can build", 16, PRICE)).arrange(DOWN, buff=0.06).move_to([2.0, -2.4, 0])
        tag = estimate_tag("the Works' model plant: illustrative numbers", size=13)
        with self.voiceover(
            "You run a plant that builds one crossover. <bookmark mark='a'/> It sells to dealers at "
            f"{U['price']:,.0f} dollars. The parts, materials, freight and warranty on each one cost {U['variable']:,.0f}, "
            f"so each car leaves {U['margin']:,.0f} dollars to pay for everything else. <bookmark mark='b'/> Everything else "
            f"is large and does not shrink with the orders. Two shifts of workers, each costing about {U['shift_cost']:.0f} "
            "million dollars a year, paid whether the line is busy or not; the tooling, the engineering of the model and the "
            f"plant's overhead, another {U['fixed']:.0f} million. <bookmark mark='c'/> So the plant must sell "
            f"{U['be']:,.0f} cars a year, {100 * U['be_share']:.0f} per cent of what it can build, just to break even. "
            f"The plan was {U['plan']:,.0f}."
        ) as vo:
            self.play(FadeIn(fac), FadeIn(car_), FadeIn(tag), FadeIn(ghost(tab, opacity=0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tab[:3]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(crews), FadeIn(crew_l), LaggedStart(*[FadeIn(t_) for t_ in tab[3:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(be, shift=UP * 0.1))
        self.clear_scene()

    def news(self):
        U = R["run"]
        pa = viz.plot_axes([0, 260_000], [-700, 800], x_length=8.6, y_length=4.4, xticks=[0, 100_000, 200_000, 250_000],
                           yticks=[-600, -300, 0, 300, 600], xfmt=lambda v: f"{v / 1000:.0f}k",
                           yfmt=lambda v: f"${v:+.0f}m".replace("$+", "+$").replace("$-", "-$"),
                           ylabel="the plant's profit ($ million)", size=13).move_to([-0.6, -0.4, 0])
        pa.add(xlab(pa, "cars sold in the year"))
        from explainer.industry.works import auto
        p = auto.Plant()
        x_lo = (p.shift_cost * 2 + p.fixed - 650e6) / p.margin     # where the line enters the chart
        pts = [(x, p.year(x, 2)["profit"] / 1e6) for x in np.linspace(x_lo, 250_000, 26)]
        line = poly(pa, pts, YOU, 4)
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(260_000, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        d_plan = Dot(pa.ax.c2p(U["plan"], p.year(U["plan"], 2)["profit"] / 1e6), radius=0.1, color=GOOD)
        l_plan = tx(f"plan: {U['plan']:,.0f} cars, +${p.year(U['plan'], 2)['profit'] / 1e6:.0f}m", 15, GOOD, bold=True).next_to(d_plan, UL, buff=0.1)
        d_weak = Dot(pa.ax.c2p(U["weak"], p.year(U["weak"], 2)["profit"] / 1e6), radius=0.11, color=BAD)
        l_weak = tx(f"orders 30% below plan: {U['weak']:,.0f} cars, {money_m(p.year(U['weak'], 2)['profit'] / 1e6)}", 15, BAD, bold=True).next_to(d_weak, DR, buff=0.1)
        rival = VGroup(draw.suv(1.4, RIVAL), tx("your rival: the same plant, the same orders", 15, RIVAL)).arrange(DOWN, buff=0.1).to_corner(UR, buff=0.5)
        tag = estimate_tag("the Works' model plant: illustrative numbers", size=13)
        with self.voiceover(
            "This line is your plant's profit for each number of cars it sells. <bookmark mark='a'/> At the plan, "
            f"{U['plan']:,.0f} cars, it makes about {p.year(U['plan'], 2)['profit'] / 1e6:.0f} million dollars. "
            "<bookmark mark='b'/> Then the first months of orders come in, and they are thirty per cent below plan: "
            f"{U['weak']:,.0f} cars a year. At that rate the plant loses {-p.year(U['weak'], 2)['profit'] / 1e6:.0f} "
            "million. <bookmark mark='c'/> And across the aisle, in the same showrooms, your rival's model, built in a plant "
            "just like yours, is selling just as slowly. Buyers compare the two closely. A discount on yours would take "
            "buyers from the rival, and a discount on theirs would take them from you."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(tag), FadeIn(ghost(line, opacity=0.3)))
            self.play(Create(line), run_time=2.0)
            vo.wait_until("a")
            self.play(GrowFromCenter(d_plan), FadeIn(l_plan))
            vo.wait_until("b")
            self.play(GrowFromCenter(d_weak), FadeIn(l_weak))
            vo.wait_until("c")
            self.play(FadeIn(rival, shift=LEFT * 0.3))
        self.clear_scene()

    def matrix(self):
        U = R["run"]
        T_, D = U["table"], U["demand"]
        x0, y0, cw, ch = -1.2, 0.0, 4.0, 2.0
        cells = {}
        for i, me in enumerate(("hold", "discount")):
            for j, them in enumerate(("hold", "discount")):
                c = np.array([x0 + cw * (j + 0.5), y0 + ch * (0.5 - i), 0])
                box = Rectangle(width=cw, height=ch, stroke_color=GREY_B, stroke_width=2, fill_color="#141A24", fill_opacity=1).move_to(c)
                mine, theirs = T_[f"{me}|{them}"]
                you = VGroup(tx("you", 13, YOU), tx(money_m(mine), 24, YOU, bold=True)).arrange(DOWN, buff=0.04)
                riv = VGroup(tx("rival", 13, RIVAL), tx(money_m(theirs), 24, RIVAL, bold=True)).arrange(DOWN, buff=0.04)
                inner = VGroup(you, riv).arrange(RIGHT, buff=0.6).move_to(c + UP * 0.12)
                sold = tx(f"you sell {D[f'{me}|{them}']:,.0f}", 12, GREY_B).move_to(c + DOWN * 0.68)
                cells[(me, them)] = VGroup(box, inner, sold)
        rows = VGroup(tx("you hold", 18, YOU, bold=True).move_to([x0 - 1.1, y0 + ch / 2, 0]),
                      tx(f"you discount ${U['discount']:,.0f}", 18, YOU, bold=True).move_to([x0 - 1.5, y0 - ch / 2, 0]))
        cols = VGroup(tx("rival holds", 18, RIVAL, bold=True).move_to([x0 + cw / 2, y0 + ch + 0.35, 0]),
                      tx("rival discounts", 18, RIVAL, bold=True).move_to([x0 + 1.5 * cw, y0 + ch + 0.35, 0]))
        frames = VGroup(*[c[0] for c in cells.values()])
        pause = tx("Pause: which would you choose?", 20, PRICE, bold=True).to_edge(DOWN, buff=0.5)
        verdict = tx("Whatever the rival does, discounting is better for you. So both discount, and both lose more.", 17, PRICE, bold=True).to_edge(DOWN, buff=0.45)
        tag = estimate_tag(f"the Works' duel: own-price elasticity {U['own']:.0f}, cross {U['cross']:.0f}; profits for the year", size=12)
        hh, dh, hd, dd = (T_[k] for k in ("hold|hold", "discount|hold", "hold|discount", "discount|discount"))
        with self.voiceover(
            "So here is the choice, for you and for the rival, set out as a table. Your profit is in blue, the rival's in "
            "orange. "
            f"<bookmark mark='a'/> If you both hold the price, you each lose {-hh[0]:.0f} million. Pause, and choose. "
            f"<bookmark mark='b'/> Suppose you discount by {U['discount']:,.0f} dollars and the rival holds. The rival's "
            f"buyers come to you; you sell almost all the plant can build and make {dh[0]:.0f} million, while the rival "
            f"loses {-dh[1]:.0f}. <bookmark mark='c'/> Suppose the rival discounts and you hold: the mirror image, and you "
            "are the one losing "
            f"{-hd[0]:.0f} million. <bookmark mark='d'/> And if you both discount, neither takes the other's buyers, the "
            f"market grows only a little, and you each lose {-dd[0]:.0f} million. <bookmark mark='e'/> Look at your own "
            "choice column by column. If the rival holds, you do better discounting. If the rival discounts, you also do "
            "better discounting. The rival reasons the same way. Both discount, and both end up far worse off than if both "
            "had held. Economists call "
            "it the prisoner's dilemma, and the car business lives in it."
        ) as vo:
            self.play(FadeIn(frames), FadeIn(rows), FadeIn(cols), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cells[("hold", "hold")][1:]), FadeIn(pause))
            vo.wait_until("b")
            self.play(FadeIn(cells[("discount", "hold")][1:]), FadeOut(pause))
            vo.wait_until("c")
            self.play(FadeIn(cells[("hold", "discount")][1:]))
            vo.wait_until("d")
            self.play(FadeIn(cells[("discount", "discount")][1:]))
            vo.wait_until("e")
            a1 = Arrow(cells[("hold", "hold")][0].get_bottom(), cells[("discount", "hold")][0].get_top(), buff=0.05, color=YOU, stroke_width=5)
            a2 = Arrow(cells[("hold", "discount")][0].get_bottom(), cells[("discount", "discount")][0].get_top(), buff=0.05, color=YOU, stroke_width=5)
            self.play(GrowArrow(a1), GrowArrow(a2))
            self.play(cells[("discount", "discount")][0].animate.set_stroke(BAD, 6), FadeIn(verdict))
        self.clear_scene()

    def cut(self):
        U = R["run"]
        T_ = U["table"]
        items = [("both hold, idle shifts", T_["hold|hold"][0], GREY_B), ("both discount", T_["discount|discount"][0], BAD),
                 ("both cut a shift, hold the price", U["both_cut"], GOOD)]
        g = VGroup()
        for i, (name, v, c) in enumerate(items):
            y = 1.2 - 1.1 * i
            b = bar(0.0, y, v / 120, 0.55, c)
            lab = tx(money_m(v) + " each", 18, c, bold=True).next_to(b, LEFT if v < 0 else RIGHT, buff=0.15)
            nm = tx(name, 17, WHITE).move_to([0.4, y, 0], aligned_edge=LEFT)
            g.add(VGroup(b, lab, nm))
        axis = Line([0, 1.9, 0], [0, -1.6, 0], stroke_color=GREY_B, stroke_width=2)
        head = tx("The way out: fewer cars, not cheaper ones", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        note = VGroup(tx("Why it is hard:", 17, PRICE, bold=True),
                      tx("cutting a shift means lay-offs, idle suppliers, and a smaller share", 15, GREY_A),
                      tx("each maker would rather the other cut first", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([0.0, -2.6, 0])
        tag = estimate_tag("the Works' model: illustrative numbers", size=13)
        with self.voiceover(
            "There is a third move that the table left out. <bookmark mark='a'/> If both of you cut a shift and hold the "
            f"price, you each build only {U['shift_cap']:,.0f} cars a year, but you stop paying a crew to stand idle, and "
            f"each loses {-U['both_cut']:.0f} million: <bookmark mark='b'/> the least bad outcome on offer. It is sometimes called capacity discipline. <bookmark mark='c'/> It is hard to keep. Cutting a shift means lay-offs, suppliers "
            "left idle and a smaller share of the market, and each maker would rather the other one cut first. That is the "
            "first answer to this film's question: the plants cost the same whether they are full or not, so every maker "
            "is tempted to fill its own, and when they all try, prices fall for everyone. Keep that in mind; it comes back "
            "in China."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(head), FadeIn(tag), FadeIn(ghost(g, opacity=0.3)))
            vo.wait_until("a")
            self.play(FadeIn(g[0]), FadeIn(g[1]), run_time=1.2)
            vo.wait_until("b")
            self.play(GrowFromEdge(g[2][0], LEFT), FadeIn(g[2][1:]))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.clear_scene()
