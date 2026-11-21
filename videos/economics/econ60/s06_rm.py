from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class RM(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Revenue management", r"How many seats should be kept back \ for buyers who have not yet "
             r"appeared?", "Chapter five. Revenue management.",
             lit={1972: r"Littlewood", 1987: r"Belobaba's EMSR"}, scale=("firm",), horizon=("a day",))
        self.littlewood()
        self.emsr()
        self.overbook()

    def littlewood(self):
        L = load("rm")["littlewood"]
        ys, sf, rev = np.array(L["ys"]), np.array(L["sf"]), np.array(L["revenue"])
        ax = plane([0, 60], [0, 1.0], center=LEFT * 3.4 + UP * 0.9, x_length=5.4, y_length=2.6,
                   xticks=[0, 10, 20, 30, 40, 50, 60], yticks=[0, 0.5, 1.0], xlabel=r"seats protected, \ $y$",
                   ylabel=r"P(high-fare demand $> y$)", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=13)
        cv = path(ax, ys[:61], sf[:61], BUS, 2.8, smooth=False)
        rl = DashedLine(ax.ax.c2p(0, L["ratio"]), ax.ax.c2p(60, L["ratio"]), color=LEIS, stroke_width=2)
        rlab = label(rf"$p_L / p_H = {L['p_lo']:.0f}/{L['p_hi']:.0f} = {L['ratio']:.3f}$", font_size=15,
                     color=LEIS).next_to(ax.ax.c2p(60, L["ratio"]), UP, buff=0.05).shift(LEFT * 1.0)
        ys_l = vline(ax, L["y_star"], 0, 1.0, E.ACCENT, 1.8)
        bx = plane([0, 100], [11000, 22500], center=LEFT * 3.4 + DOWN * 2.3, x_length=5.4, y_length=2.4,
                   xticks=[0, 20, 40, 60, 80, 100], yticks=[12000, 16000, 20000], xlabel=r"seats protected",
                   ylabel=r"expected revenue", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=13)
        rc = path(bx, ys, rev, OPT, 2.8, smooth=False)
        rd = dot(bx, L["y_star"], L["rev_star"], E.ACCENT, 0.08)
        side = VGroup(
            label(rf"{L['seats']} seats; \ leisure fare \${L['p_lo']:.0f}, \ booked first and plentiful", font_size=19,
                  color=LEIS),
            label(rf"business fare \${L['p_hi']:.0f}: \ about {L['mean_hi']:.0f} buyers, \ late, \ uncertain",
                  font_size=19, color=BUS),
            label(r"keep the $y$-th seat back if it would sell at the high fare \\ with probability above "
                  r"$p_L/p_H$:", font_size=18, color=WHITE),
            MathTex(r"p_H \, P(D_H \ge y) \;\ge\; p_L \iff P(D_H \ge y) \ge \frac{p_L}{p_H}", font_size=28,
                    color=E.ACCENT),
            label(rf"protect {L['y_star']} seats: \ \${L['rev_star']:,.0f} \ against \${L['rev_none']:,.0f} \ selling "
                  r"to whoever comes first".replace(",", "{,}"), font_size=19, color=OPT),
            label(r"Littlewood, \ British Overseas Airways, \ 1972", font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        if side.width > 6.6:
            side.width = 6.6
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ Poisson demand, \ computed exactly", corner=DL, font_size=12)
        with self.voiceover(
            "The simplest version of the airline's problem has two fares. <bookmark mark='a'/> Leisure travellers "
            f"pay {L['p_lo']:.0f} dollars, book first, and there are more than enough of them to fill the plane. "
            f"<bookmark mark='b'/> Business travellers pay {L['p_hi']:.0f}, book late, and about {L['mean_hi']:.0f} "
            "will come, though nobody knows exactly how many. How many seats should be protected from the leisure "
            "fare? <bookmark mark='c'/> Think about one seat at a time. Selling it now at the low fare earns "
            f"{L['p_lo']:.0f} for certain. Holding it back earns {L['p_hi']:.0f}, but only if enough business "
            "travellers turn up to need it. <bookmark mark='d'/> So keep the seat if the chance it sells at the "
            "high fare is above the ratio of the fares. That is Kenneth Littlewood's rule, from British Overseas "
            "Airways in 1972. <bookmark mark='e'/> Here the curve of the chance that business demand exceeds y "
            f"crosses the ratio at {L['y_star']} seats. <bookmark mark='f'/> Protecting {L['y_star']} seats earns "
            f"{L['rev_star']:,.0f} dollars on average, against {L['rev_none']:,.0f} if every seat went to whoever "
            "booked first, and the exact calculation of revenue for every protection level peaks at the same "
            "place."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Write(side[3]), FadeIn(side[5]))
            vo.wait_until("e")
            self.play(FadeIn(ax), Create(cv), Create(rl), FadeIn(rlab), run_time=1.5)
            self.play(Create(ys_l))
            vo.wait_until("f")
            self.play(FadeIn(bx), Create(rc), FadeIn(rd), FadeIn(side[4]), run_time=1.5)
        self.clear_scene()

    def emsr(self):
        E_ = load("rm")["emsr"]
        f, prot = E_["fares"], E_["protect"]
        cols = (BUS, OPT, AIR, LEIS)
        seats = VGroup()
        bounds = [0] + [round(x) for x in prot] + [100]
        for k in range(4):
            a, b = bounds[k], bounds[k + 1]
            seats.add(Rectangle(width=max(0.11 * (b - a), 0.02), height=0.9, fill_color=cols[k], fill_opacity=0.8,
                                stroke_width=0))
        seats.arrange(RIGHT, buff=0).move_to(UP * 0.6)
        labs = VGroup(*[label(rf"\${f[k]:.0f}", font_size=18, color=cols[k]).next_to(seats[k], UP, buff=0.1)
                        for k in range(4)])
        nums = VGroup(*[label(rf"{bounds[k + 1] - bounds[k]:.0f}", font_size=16, color=BLACK).move_to(seats[k])
                        for k in range(4)])
        rows = VGroup(
            label(r"four fares: \ protect for each class the seats the classes above it are likely to need",
                  font_size=20, color=WHITE),
            label(rf"protection levels, \ nested: \ {prot[0]:.0f} for the top fare, \ {prot[1]:.0f} for the top two, "
                  rf"\ {prot[2]:.0f} for the top three", font_size=20, color=OPT),
            label(r"EMSR-b \ (Belobaba): \ treat the classes above as one, \ at their average fare, \ and apply "
                  r"Littlewood", font_size=18, color=GREY_A),
            label(r"networks: \ a seat on one leg is part of many itineraries; \ a bid price per leg, \ from a "
                  r"linear programme, \ says which bookings to accept", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(seats, DOWN, buff=0.6)
        if rows.width > 13.0:
            rows.width = 13.0
        head = label(r"many fares, \ nested", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = island_tag(r"the Island: \ normal demands; \ agora.revenue.emsr\_b", corner=DL, font_size=12)
        with self.voiceover(
            "Real airlines sell many fares. <bookmark mark='a'/> The protection levels are nested: seats protected "
            f"for the top fare, about {prot[0]:.0f}; for the top two fares together, about {prot[1]:.0f}; for the top "
            f"three, about {prot[2]:.0f}. A cheaper class can only have what is left. <bookmark mark='b'/> Peter "
            "Belobaba's heuristic, EMSR-b, computes them by treating all the classes above a fare as one class at "
            "their average fare, and applying Littlewood's rule. <bookmark mark='c'/> And seats belong to networks: "
            "a seat from the Island to the mainland is also part of every connecting trip through it. Airlines "
            "attach a bid price to each leg, from a linear programme, and accept a booking only if its fare beats "
            "the sum of the bid prices of the legs it uses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(seats), FadeIn(labs), FadeIn(nums), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def overbook(self):
        O = load("rm")["overbooking"]
        bs, val = np.array(O["bs"]), np.array(O["value"])
        ax = plane([100, 120], [16500, 19600], center=LEFT * 2.7 + DOWN * 0.4, x_length=6.4, y_length=4.4,
                   xticks=[100, 105, 110, 115, 120], yticks=[17000, 18000, 19000],
                   xlabel=r"tickets sold for 100 seats", ylabel=r"expected revenue, \ \$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=14)
        cv = path(ax, bs, val, OPT, 3.0, xr=(100, 120), yr=(16500, 19600), smooth=False)
        d = dot(ax, O["best"], O["value_best"], E.ACCENT, 0.09)
        side = VGroup(
            label(r"each ticket-holder shows up with probability 0.9", font_size=20, color=GREY_A),
            label(r"a fare of \$200; \ bumping a passenger costs \$600", font_size=20, color=GREY_A),
            label(r"sell one more ticket while \\ fare $\times$ 0.9 \ $>$ \ \$600 $\times$ P(it bumps someone)",
                  font_size=20, color=WHITE),
            label(rf"best: \ {O['best']} tickets, \ \${O['value_best']:,.0f} \ against \${O['value_no']:,.0f}"
                  .replace(",", "{,}"), font_size=21, color=OPT),
            label(rf"about {O['bumped_best']:.1f} passengers bumped per flight, \ on average", font_size=19,
                  color=COST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ binomial show-ups, \ computed exactly", corner=DL, font_size=12)
        with self.voiceover(
            "One more tool: overbooking. <bookmark mark='a'/> Not everyone who books turns up; on the Island, each "
            "ticket-holder shows up with probability nine in ten. <bookmark mark='b'/> A seat sold to someone who "
            "does not show flies empty, but a passenger who shows up to a full plane must be paid to take a later "
            "flight, here six hundred dollars. <bookmark mark='c'/> Sell one more ticket while the fare it brings, "
            "times the chance its buyer shows up, beats the cost of bumping times the chance the extra passenger is "
            f"one too many. <bookmark mark='d'/> The best is {O['best']} tickets for a hundred seats, earning "
            f"{O['value_best']:,.0f} dollars against {O['value_no']:,.0f} with no overbooking, <bookmark mark='e'/> "
            f"at the cost of about {say_num(O['bumped_best'], 1)} bumped passengers per flight, on average. Each of "
            "these rules is a small optimization; together they are the software that undercut People Express."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Create(cv), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(d, scale=1.5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
