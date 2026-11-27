from __future__ import annotations

import math

from videos.industry.industry18.common import *  # noqa: F403


class Programme(VoiceoverScene):
    def construct(self):
        card(self, 3, "A programme's arithmetic", "Why does the first airliner cost four times its price?",
             "Chapter three. A programme's arithmetic. A new airliner is a bet of tens of billions of dollars, paid back "
             "over decades. Here is how the bet works.", lit=("make", "dollar"))
        self.learning()
        self.valley()
        self.slow()

    def learning(self):
        P = R["programme"]
        lg = math.log10
        pa = viz.plot_axes([0, lg(2000)], [0, 480], x_length=9.6, y_length=4.4, xticks=[0, 1, 2, 3, lg(2000)],
                           yticks=[0, 100, 200, 300, 400], xfmt=lambda v: f"{10 ** v:,.0f}", yfmt=lambda v: f"${v:.0f}m",
                           ylabel="cost to build the n-th aircraft (the Works' programme)", size=13).move_to([-0.5, -0.4, 0])
        pts = [(lg(n), P["first"] * n ** math.log2(P["learning"])) for n in np.geomspace(1, 2000, 120)]
        curve = poly(pa.ax, pts, ENGINE, 4)
        price = hline(pa.ax, P["price"], 0, lg(2000), PRICE, f"price: ${P['price']:.0f}m")
        first = marker(pa.ax, 0, P["first"], f"the first: ${P['first']:.0f}m", BAD, side=RIGHT)
        n2 = marker(pa.ax, lg(2), P["unit"][2], f"the second: ${P['unit'][2]:.0f}m", BAD, side=RIGHT)
        cross = marker(pa.ax, lg(P["cross"]), P["price"], f"from the {P['cross']:.0f}th, each costs less than its price",
                       GOOD, side=UR)
        late = marker(pa.ax, lg(1000), P["unit"][1000], f"the 1,000th: ${P['unit'][1000]:.0f}m", GOOD, side=UP)
        xl = tx("aircraft built (each step ten times more)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        tag = estimate_tag(f"the Works: each doubling of the count cuts the next one's cost to {100 * P['learning']:.0f}%",
                           size=12)
        beat(self,
             "Start with the cost of building one aircraft. <bookmark mark='a'/> The first one off a new line is "
             "astonishingly expensive: workers are learning the job, tools are being adjusted, and parts are redone. In "
             f"this film's model the first costs {P['first']:.0f} million dollars to build, against a price of "
             f"{P['price']:.0f} million. <bookmark mark='b'/> But each time the number built doubles, the next one costs "
             f"{100 * P['learning']:.0f} per cent of what it did. This is the learning curve, which an engineer at an "
             f"American aircraft maker, T. P. Wright, published in {get('wright.1936')}. The second costs {P['unit'][2]:.0f} million. "
             f"<bookmark mark='c'/> From about the {P['cross']:.0f}th aircraft on, each costs less to build than it sells "
             f"for, <bookmark mark='d'/> and the thousandth costs {P['unit'][1000]:.0f} million.",
             base=[pa, xl, tag, price], steps=[first, [curve, n2], cross, late])

    def valley(self):
        P = R["programme"]
        cum = P["cum"]
        ch = line_chart({"cash": (cum, PRICE)}, x=(0, 30), y=(-45, 110), xticks=[0, 6, 10, 15, 20, 25, 30],
                        yticks=[-25, 0, 25, 50, 75, 100], yfmt=lambda v: f"${v:.0f}bn", xfmt=lambda v: f"year {int(v)}",
                        ylabel="the programme's cumulative cash (the Works)", label_end=False, width=9.8, height=4.6,
                        center=(-0.4, -0.45))
        ax = ch.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(30, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        dev = poly(ax, [(y, cum[y]) for y in range(0, P["dev_years"] + 1)], BAD, 4)
        ramp = poly(ax, [(y, cum[y]) for y in range(P["dev_years"], P["be"]["year"] + 1)], PRICE, 4)
        rest = poly(ax, [(y, cum[y]) for y in range(P["be"]["year"], 31)], GOOD, 4)
        tr = min(cum, key=cum.get)
        m_dev = callout(ax, P["dev_years"], cum[P["dev_years"]], f"{P['dev_years']} years, ${P['dev']:.0f}bn, no deliveries",
                        BAD, at=(5, 22))
        m_tr = callout(ax, tr, cum[tr], f"the bottom: {bn(P['trough'])}", BAD, at=(14, -38))
        m_be = marker(ax, P["be"]["year"], cum[P["be"]["year"]], f"even in year {P['be']['year']}, after {P['be']['units']:,.0f} aircraft",
                      GOOD, side=RIGHT)
        npv = tx(f"worth {bn(P['npv'])} today at an 8% cost of capital", 17, GOOD, bold=True).move_to([1.6, 1.9, 0])
        tag = estimate_tag("the Works' programme: illustrative", size=12)
        beat(self,
             "Now the cash. <bookmark mark='a'/> For six years the programme only spends: design, testing, "
             f"certification, tooling, {P['dev']:.0f} billion dollars before a single aircraft is delivered. "
             "<bookmark mark='b'/> Then deliveries begin, slowly, and the early aircraft cost more to build than they sell "
             f"for, so the hole keeps deepening, to {-P['trough']:.0f} billion dollars. <bookmark mark='c'/> Only when the line is up to speed and down its learning curve does the cash "
             f"come back. The programme breaks even in year {P['be']['year']}, after {P['be']['units']:,.0f} aircraft. "
             "<bookmark mark='d'/> After that it makes money for decades. Discounted at eight per cent a year, the whole "
             f"bet is worth {P['npv']:.1f} billion dollars today: positive, but small against a hole of "
             f"{-P['trough']:.0f} billion.",
             base=[ch.frame, zero, tag], steps=[[dev, m_dev], [ramp, m_tr], [rest, m_be], npv])

    def slow(self):
        P = R["programme"]
        ch = line_chart({"learning 82%": (P["cum"], GOOD), "learning 90%": (P["cum_slow"], BAD)}, x=(0, 30), y=(-160, 110),
                        xticks=[0, 10, 20, 30], yticks=[-150, -100, -50, 0, 50, 100], yfmt=lambda v: f"${v:.0f}bn",
                        xfmt=lambda v: f"year {int(v)}", ylabel="cumulative cash (the Works)", width=9.4, height=4.6,
                        center=(-0.8, -0.45))
        zero = DashedLine(ch.ax.c2p(0, 0), ch.ax.c2p(30, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        res = VGroup(tx(f"82%: worth {bn(P['npv'])} today", 17, GOOD, bold=True),
                     tx(f"90%: worth {bn(P['slow'])} today", 17, BAD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-2.6, -2.3, 0])
        rnd = tx(f"Boeing's airliner business spent ${P['rnd'] / 1e3:.1f}bn on research and development in 2025, for every model",
                 15, BOEING, bold=True).to_edge(DOWN, buff=0.6)
        tag = estimate_tag("the Works' programme with two learning rates", size=12)
        beat(self,
             "Everything rests on that learning curve. <bookmark mark='a'/> With costs falling to eighty-two per cent "
             "at each doubling, the programme pays. <bookmark mark='b'/> Change one number: suppose each doubling cuts "
             "costs only to ninety per cent. Then the aircraft never get cheap enough, every delivery loses money, and "
             f"the programme sinks to {P['cum_slow'][30]:.0f} billion dollars after thirty years. <bookmark mark='c'/> A "
             f"difference of eight points turns a bet worth {P['npv']:.0f} billion into a loss of {-P['slow']:.0f} "
             "billion. <bookmark mark='d'/> That is why a maker would rather keep improving an old design, whose learning "
             f"is already paid for, than start again. For comparison, Boeing's whole airliner business spent "
             f"{P['rnd'] / 1e3:.1f} billion dollars on research and development in 2025.",
             base=[ch.frame, zero, tag], steps=[[ch.lines["learning 82%"], ch.labels["learning 82%"]],
                                              [ch.lines["learning 90%"], ch.labels["learning 90%"]], res, rnd])
