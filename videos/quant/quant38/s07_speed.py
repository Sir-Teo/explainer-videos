from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BUY_C, SELL_C, BAD, FAST_C, HURDLE, MAKER_C, PART, SNIPE_C, fit_right, load)


class Speed(VoiceoverScene):
    def construct(self):
        b = load("bcs")
        self.card()
        self.race()
        self.model()
        self.sim(b)
        self.n_table(b)
        self.btc_prize(load("maker"))
        self.arms()
        self.measured()
        self.physics()
        self.remedies()
        self.auction_example()
        self.adoption()
        self.question()

    def card(self):
        c = chapter_card(6, r"The speed race", r"Why do market makers spend fortunes on microseconds?", part=PART)
        with self.voiceover("Chapter six, and the answer to the pause: four times in five. When news is public, the maker "
                            "who quoted is one runner against many, and wins the race to cancel only as often as anyone "
                            "else wins the race to trade. Eric Budish, Peter Cramton and John Shim turned that into an "
                            "equilibrium."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def race(self):
        cards = VGroup(
            desk_question(r"the news", r"a futures price moves, a correlated stock ticks, an index level updates: "
                          r"public information, seen by every fast firm within microseconds", width=12.4, font_size=19),
            desk_question(r"the race", r"the maker sends a cancel; its rivals send orders to hit the stale quote; the "
                          r"exchange processes messages one at a time, in the order they arrive", width=12.4, font_size=19),
            desk_question(r"the outcome", r"with N equally fast firms, the maker's cancel arrives first one time in N; "
                          r"otherwise its quote is sniped", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "The race. <bookmark mark='a'/> News arrives: a futures price moves, or a correlated asset ticks, public "
            "information that every fast firm sees within microseconds. <bookmark mark='b'/> The maker sends a cancel; "
            "its rivals send orders to hit the stale quote; the exchange processes messages one at a time, in the order "
            "they arrive. <bookmark mark='c'/> With N equally fast firms, the maker's cancel arrives first one time in N."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def model(self):
        rows = [cmath(r"\pi_{\text{maker}}", r"=", r"\lambda_I \tfrac{s}{2} - \lambda_J \tfrac{N-1}{N}(J - \tfrac s2)",
                      font_size=36, colors={r"\pi_{\text{maker}}": MAKER_C}),
                cmath(r"\pi_{\text{sniper}}", r"=", r"\lambda_J \tfrac1N (J - \tfrac s2)", font_size=36,
                      colors={r"\pi_{\text{sniper}}": SNIPE_C}),
                cmath(r"\pi_{\text{maker}} = \pi_{\text{sniper}}", r"\Rightarrow", r"\tfrac{s^*}{2} = \frac{\lambda_J J}"
                      r"{\lambda_I + \lambda_J}", font_size=34, colors={r"\tfrac{s^*}{2} = \frac{\lambda_J J}{\lambda_I + \lambda_J}": HURDLE})]
        whys = [why(r"the maker earns half the spread from investors arriving at rate $\lambda_I$, and loses $J - s/2$ "
                    r"each time a jump of size $J$ (rate $\lambda_J$) catches its quote stale"),
                why(r"each of the others wins a race one time in $N$"),
                why(r"in equilibrium no firm prefers the other role; the $N$ cancels: the spread is independent of "
                    r"how many firms compete")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The simplified role model. Assume at least two equally fast firms, positive investor and public-jump rates, a positive fixed jump, unit uninformed orders and frictionless price undercutting. <bookmark mark='a'/> A provider receives half-spread h from each investor and loses J minus h when a rival beats its cancel, for h below J. <bookmark mark='b'/> Each of the other firms wins with probability one over N. <bookmark mark='c'/> The role-indifference condition cancels N and gives h equal to lambda J times J divided by the sum of rates. This is conditional on the model's trading and competition assumptions."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def sim(self, b):
        sims = b["sims"]
        x = np.asarray([s["half"] for s in sims], float)
        lp = np.asarray([s["lp"] for s in sims], float)
        sn = np.asarray([s["sniper"] for s in sims], float)
        top = float(np.ceil(max(lp.max(), sn.max()) * 2) / 2)
        lo = float(np.floor(min(lp.min(), 0) * 2) / 2)
        g = axes([0, float(x.max())], [lo, top], x_length=6.4, y_length=4.4, xlabel=r"half-spread $s/2$",
                 ylabel=r"profit per unit time", xticks=[0, 1, 2, 3, 4], yticks=[lo, 0, top], yfmt=lambda v: f"{v:.1f}",
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        cl = curve(ax, x, lp, MAKER_C, stroke_width=3)
        cs = curve(ax, x, sn, SNIPE_C, stroke_width=3)
        star = DashedLine(ax.c2p(b["s_star"], lo), ax.c2p(b["s_star"], top), color=HURDLE, stroke_width=1.8)
        leg = legend([(MAKER_C, r"the maker"), (SNIPE_C, r"each sniper"), (HURDLE, r"$s^*/2$, the formula")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            "Simulate it: investors at rate one, jumps of four at rate a tenth, five firms, a long run. "
            "<bookmark mark='a'/> As the half-spread widens, the maker's profit rises and each sniper's falls. "
            f"<bookmark mark='b'/> They cross where the formula says, at {b['s_star']:.2f}. A narrower spread would make "
            "makers become snipers; a wider one would draw snipers into making."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(cl), Create(cs))
            vo.wait_until("b")
            self.play(Create(star))
        self.wait(0.4)
        self.clear_scene()

    def n_table(self, b):
        hx = [-3.4, 0.0, 3.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"firms $N$", r"maker's profit", r"each sniper's")])
        tab = VGroup(head)
        for r in b["byN"]:
            tab.add(VGroup(MathTex(str(r["N"]), font_size=26), MathTex(f"{r['lp']:.3f}", font_size=26, color=MAKER_C),
                           MathTex(f"{r['sniper']:.3f}", font_size=26, color=SNIPE_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.75 * j, 0])
        foot = wrapped_label(rf"all at the same spread, $s^*/2 = {b['s_star']:.2f}$: theoretical expected role profits are equal for each "
                             r"number of firms; finite simulated means vary around their expectations", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A consistency check within that model. <bookmark mark='a'/> At the formula's spread, expected provider profit and each sniper's profit are equal for every chosen N. The finite Monte Carlo estimates differ slightly. Each role receives investor payments divided by N; their sum is industry profit. The spread's independence from N holds with the other assumptions fixed and does not describe arbitrary entry or speed investment."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def btc_prize(self, mk):
        d = mk["days"]["2023-05-17"]
        rows = [cmath(r"\text{slow}", r":", rf"{d['slow']['n']:,}\ \text{{fills}} \times {d['slow']['pnl_per_fill']:.1f}".replace(",", "{,}"),
                      font_size=34, colors={r"\text{slow}": SNIPE_C}),
                cmath(r"\text{fast}", r":", rf"{d['fast']['n']:,}\ \text{{fills}} \times {d['fast']['pnl_per_fill']:.1f}".replace(",", "{,}"),
                      font_size=34, colors={r"\text{fast}": FAST_C}),
                cmath(r"\text{per unit quoted, a day}", r":", rf"\${0.1 * abs(d['slow']['n'] * d['slow']['pnl_per_fill']) / 1000:.0f}"
                      rf"\text{{k}} \to \${0.1 * abs(d['fast']['n'] * d['fast']['pnl_per_fill']) / 1000:.0f}\text{{k lost}}",
                      font_size=32, colors={r"\text{per unit quoted, a day}": HURDLE})]
        whys = [why(r"17 May, the slow maker of Chapter 2"),
                why(r"the idealised fast maker on the same day"),
                why(r"for one-bitcoin units, this compares selected final-mid replay losses with different fill counts and inventory paths, "
                    r"not a causal speed effect, sniping-rent estimate or executable net-profit forecast")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        slow_k = 0.1 * abs(d["slow"]["n"] * d["slow"]["pnl_per_fill"]) / 1000
        fast_k = 0.1 * abs(d["fast"]["n"] * d["fast"]["pnl_per_fill"]) / 1000
        with self.voiceover(
            f"Replay losses in dollar units. <bookmark mark='a'/> With a one-bitcoin unit and ten-cent tick, the slow rule's final-mid loss is about {slow_k:.0f} thousand dollars on May seventeenth. <bookmark mark='b'/> The within-step hindsight variant loses about {fast_k:.0f} thousand. <bookmark mark='c'/> The numerical gap combines altered fills and inventory paths. It is neither a measured sniping rent nor a causal dollar value of real latency. The replay omits funding, fees, hedging and executable liquidation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def arms(self):
        rows = [cmath(r"R", r":", r"\text{fixed race prize; equal speeds split }R/N", font_size=33),
                cmath(r"m\ge1\ \text{fast rivals}", r":", r"\text{joining them earns }R/(m+1)-c", font_size=33),
                cmath(r"0<c<R/N", r"\Rightarrow", r"\text{investing is dominant in this toy game}", font_size=32, colors={r"0<c<R/N": HURDLE})]
        whys = [why(r"a separate binary investment game: fast firms share a fixed $R$; slow firms receive zero when any fast firm exists"),
                why(r"with no fast rival, investing gains $R-R/N-c$; with $m$ fast rivals, the gain is $R/(m+1)-c$"),
                why(r"the smallest gross gain is $R/N$; all invest and each pays $c$. This is not a theorem about endogenous speed choices in every continuous market")]
        step=ladder(self,rows,whys,keep=3,top=2.6,x=-0.3,buff=0.55,edge=6.9)
        with self.voiceover("Separate the speed-investment game. <bookmark mark='a'/> Suppose a fixed prize R is split equally among fast firms, with slow firms getting nothing whenever a fast firm exists. If none invests, all share R over N. <bookmark mark='b'/> Investment costs c. With m fast rivals, joining them earns R over m plus one, less c; remaining slow earns zero. <bookmark mark='c'/> For positive c below R over N, investment is strictly dominant. Everyone invests and loses c relative to the all-slow outcome. These explicit assumptions establish a prisoner's dilemma; being faster alone does not prove it.") as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def measured(self):
        cards = VGroup(
            desk_question(r"London, measured", r"Aquilina, Budish and O'Neill (2022): races last microseconds, involve a "
                          r"handful of firms, cover about a fifth of volume, and tax all trading about half a basis point "
                          r"(Part 35)",
                          width=12.4, font_size=19),
            desk_question(r"Bitcoin, in our replay", r"the gap between the slow and the idealised fast maker of Chapter 2, "
                          r"is a selected gross-performance comparison, not an identified sniping prize", width=12.4, font_size=19),
            desk_question(r"the economics of speed", r"Baron, Brogaard, Hagströmer and Kirilenko (2019): among "
                          r"high-frequency firms, the fastest earn the most, and profits are concentrated in a few",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "External evidence and our proxy have different meanings. <bookmark mark='a'/> Aquilina, Budish and O'Neill used exchange message data to study London latency races and estimate their trading cost. <bookmark mark='b'/> Our hundred-millisecond Bitcoin replay cannot identify such races or convert its selected performance gap into the same structural quantity. <bookmark mark='c'/> Baron and colleagues document concentrated profits and associations with relative speed among observed high-frequency firms. Neither result identifies every benefit or cost of faster markets."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def physics(self):
        km = 1150.0
        c = 299792.458
        t_air = 1000 * km / c
        t_fibre = t_air * 1.47
        rows = [cmath(r"\text{Chicago--New York}", r"\approx", rf"{km:,.0f}\ \text{{km}}".replace(",", "{,}"), font_size=36),
                cmath(r"\text{light in air}", r":", rf"{t_air:.1f}\ \text{{ms one way}}", font_size=38, colors={r"\text{light in air}": FAST_C}),
                cmath(r"\text{light in fibre}", r":", rf"{t_fibre:.1f}\ \text{{ms}}\ (n \approx 1.47)", font_size=36),
                cmath(r"\text{the prize}", r":", rf"{t_fibre - t_air:.1f}\ \text{{ms}}", font_size=40, colors={r"\text{the prize}": HURDLE})]
        whys = [why(r"roughly the great-circle distance between the futures exchanges near Chicago and the stock exchanges "
                    r"near New York"),
                why(r"the physical limit: microwave and laser links come close to it"),
                why(r"glass slows light by its refractive index, and fibre routes are longer than the straight line"),
                why(r"a few milliseconds, the edge that paid for towers between the two cities; a calculation, not a "
                    r"measured route")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The physics of the race. <bookmark mark='a'/> The futures exchanges near Chicago and the stock exchanges "
            "near New York are about eleven hundred and fifty kilometres apart. <bookmark mark='b'/> Light in air "
            f"covers that in about {t_air:.1f} milliseconds. <bookmark mark='c'/> In glass fibre, slowed by its "
            f"refractive index, about {t_fibre:.1f}. <bookmark mark='d'/> The difference, under two milliseconds, is "
            "what paid for chains of microwave towers between the two cities: a calculation from physics, not any "
            "firm's measured route."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def remedies(self):
        cards = VGroup(
            desk_question(r"frequent batch auctions", r"collect orders for, say, a tenth of a second, then clear them at "
                          r"one price: a tiny speed edge no longer wins, and firms compete on price (the research chapter)",
                          width=12.4, font_size=19),
            desk_question(r"speed bumps", r"IEX introduced a 350-microsecond access delay and mechanisms for selected "
                          r"pegged orders; treatment depends on the order type and rule version", width=12.4,
                          font_size=19),
            desk_question(r"asymmetric delays and fees", r"some venues delay only takers, or price cancels and order-to-"
                          r"trade ratios; each moves rents between makers and snipers", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Design proposals. <bookmark mark='a'/> Uniform-price batches can permit quote updates and price competition within an interval; stale execution can remain near its boundary or with asymmetric information. <bookmark mark='b'/> IEX introduced a three-hundred-and-fifty-microsecond access delay and mechanisms to protect certain pegged orders. Details depend on the order type and rule version. <bookmark mark='c'/> Asymmetric delays and messaging fees change incentives too. Their welfare requires modeling information, participation and routing, rather than assuming every speed expense is waste."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def auction_example(self):
        rows = [cmath(r"\text{bids}", r":", r"100.02 \times 3,\ 100.01 \times 5,\ 100.00 \times 4", font_size=32, colors={r"\text{bids}": BUY_C}),
                cmath(r"\text{offers}", r":", r"100.00 \times 2,\ 100.01 \times 4,\ 100.03 \times 6", font_size=32,
                      colors={r"\text{offers}": SELL_C}),
                cmath(r"p^*", r"=", r"100.01:\ \text{demand } 8,\ \text{supply } 6 \Rightarrow 6\ \text{trade}", font_size=32,
                      colors={r"p^*": HURDLE})]
        whys = [why(r"all orders that arrived during the batch, sorted by price; time within the batch does not matter"),
                why(r"the same for offers"),
                why(r"a volume-maximizing uniform price; better bids fill first, then 3 of 5 marginal bid units at that "
                    r"price fill pro rata under the chosen allocation rule")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "An illustrative uniform-price auction. <bookmark mark='a'/> Aggregate bids by limit price. <bookmark mark='b'/> Aggregate offers in the same way. <bookmark mark='c'/> At a hundred dollars and one cent, demand is eight and supply six, so six units trade; nearby candidate prices trade fewer units. Better-priced bids receive priority: all three units at a hundred and two cents, then three of the five marginal bid units, rationed pro rata under our chosen rule. This allocation rule is an assumption, not universal across auctions."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def adoption(self):
        cards = VGroup(
            desk_question(r"why exchanges keep continuous trading", r"Budish, Lee and Shim (2024) argue exchanges earn "
                          r"from selling speed (colocation, data) and have little private incentive to switch", width=12.4,
                          font_size=19),
            desk_question(r"costs of batching", r"fragmented liquidity if only one venue batches, the choice of interval, "
                          r"and new games at the batch boundary", width=12.4, font_size=19),
            desk_question(r"where batching already exists", r"opening and closing auctions, and some venues' periodic "
                          r"auctions: the idea is old; doing it every tenth of a second is the novelty", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Why it has not happened. <bookmark mark='a'/> Budish, Robin Lee and Shim argue that exchanges earn from "
            "selling speed, colocation and data, and have little private reason to switch. <bookmark mark='b'/> Batching "
            "has costs too: liquidity fragments if one venue batches alone, the interval must be chosen, and new games "
            "appear at the batch boundary. <bookmark mark='c'/> And batching already exists, in opening and closing "
            "auctions: doing it ten times a second is the novelty."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = VGroup(label(r"Pause and predict", font_size=32, color=QC.IDEA),
                   wrapped_label('if a market switched to batch auctions every 100 ms, what would happen to the sniping prize, to the spread, and to the value of being a microsecond faster?', 11.8, 30)).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        with self.voiceover(
            "Pause and predict. If a market switched to batch auctions every tenth of a second, what would happen to the "
            "sniping prize, to the spread, and to the value of being a microsecond faster?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
