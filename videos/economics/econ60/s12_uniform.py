from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class Uniform(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Why chains charge the same price everywhere", r"If every store's buyers differ, \ why is the "
             r"price the same?", "Chapter ten. Why chains charge the same price everywhere.",
             lit={2019: r"DellaVigna and Gentzkow"}, scale=("firm", "nation"), horizon=("a year",))
        self.chain()
        self.why()

    def chain(self):
        Cc = load("chain")
        e, p = np.array(Cc["eps"]), np.array(Cc["p_store"])
        ax = plane([1.9, 3.3], [1.35, 2.15], center=LEFT * 2.7 + DOWN * 0.4, x_length=6.4, y_length=4.6,
                   xticks=[2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2], yticks=[1.4, 1.6, 1.8, 2.0],
                   xlabel=r"the store's elasticity of demand \ (magnitude)", ylabel=r"price $\div$ marginal cost",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(float(np.clip(x, 1.91, 3.29)), float(np.clip(y, 1.36, 2.14))), radius=0.04,
                           color=COST if y < Cc["uniform"] else LEIS) for x, y in zip(e, p)])
        u = DashedLine(ax.ax.c2p(1.9, Cc["uniform"]), ax.ax.c2p(3.3, Cc["uniform"]), color=WHITE, stroke_width=2.2)
        ul = label(rf"the chain's one price: \ {Cc['uniform']:.2f}", font_size=16, color=WHITE).next_to(
            ax.ax.c2p(3.3, Cc["uniform"]), UP, buff=0.06).shift(LEFT * 1.2)
        side = VGroup(
            label(r"each dot: \ one of 200 stores, \ at its own best price", font_size=19, color=GREY_A),
            label(rf"stores at the 10th and 90th percentiles of elasticity \\ ({Cc['e10']:.2f} and {Cc['e90']:.2f}): "
                  rf"best prices {100 * Cc['gap_10_90']:.0f}\% apart", font_size=19, color=WHITE),
            label(r"red: \ stores whose buyers pay more under one price", font_size=19, color=COST),
            label(rf"profit given up by one price: \ {100 * Cc['loss']:.1f}\%", font_size=20, color=OPT),
            label(r"DellaVigna and Gentzkow: \ the same 17\% gap in theory, \\ far less in practice; \ the median "
                  r"chain gives up \$16 million a year", font_size=18, color=SHOP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ a chain of 200 stores; \ agora.revenue.chain", corner=DL, font_size=12)
        with self.voiceover(
            "Stefano DellaVigna and Matthew Gentzkow studied the prices of America's grocery, drugstore and "
            "mass-merchandise chains, and found something the theory does not predict: most chains charge nearly "
            "the same price in every store, however different the stores' customers. <bookmark mark='a'/> On the "
            "Island, a chain has two hundred stores whose customers differ in how sensitive they are to price. "
            "Each dot is a store at its own best price. <bookmark mark='b'/> Stores at the tenth and ninetieth "
            "percentiles of elasticity should charge prices about seventeen percent apart, the same gap "
            "DellaVigna and Gentzkow computed for the typical chain. <bookmark mark='c'/> The chain charges one "
            f"price, {Cc['uniform']:.2f} times cost. In the red stores, whose customers are the most sensitive to "
            "price, that is above the store's own best price, so they pay more; in the green ones, less. <bookmark "
            f"mark='d'/> On the Island, one price gives up only {100 * Cc['loss']:.1f} percent of profit, because "
            "of chapter one's flat top. <bookmark mark='e'/> In the real data the gap in prices is far smaller "
            "than the theory says it should be, and the median chain gives up about sixteen million dollars of "
            "profit a year by pricing uniformly."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in pts], lag_ratio=0.01), FadeIn(side[0]), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(u), FadeIn(ul), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def why(self):
        cards = point_cards([
            (r"managing many prices costs", r"data, \ staff and errors; \ a little profit is lost per store", SHOP),
            (r"fairness and reputation", r"one price in every town is easy to defend, \ and to advertise", AIR),
            (r"who pays", r"poorer areas' shoppers are more sensitive to price; \ one price makes them pay more "
             r"than store-by-store prices would", COST),
            (r"a cushion in a crisis", r"prices that do not move with local demand \ do not rise after a local "
             r"shock either", LEIS),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"why one price, \ and who pays for it", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"DellaVigna and Gentzkow, \ Quarterly Journal of Economics 134(4) (2019)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "Why would chains leave money on the table? <bookmark mark='a'/> Managing thousands of prices store by "
            "store costs data, staff and mistakes, and the flat top means the loss per store is small. <bookmark "
            "mark='b'/> One price in every town is easy to defend and to advertise. <bookmark mark='c'/> It also "
            "decides who pays. Shoppers in poorer areas tend to be more sensitive to price, so store-by-store "
            "pricing would charge them less; DellaVigna and Gentzkow found that uniform pricing raises the prices "
            "poorer households pay relative to richer ones. <bookmark mark='d'/> And prices that ignore local "
            "demand do not jump after a local shock either. A rule of thumb again, with consequences the theory "
            "can measure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
