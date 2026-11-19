from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403


class Lemons(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Akerlof's market", r"When many buyers bid for boats they cannot inspect, \ where does the price "
             r"settle, \ and which boats trade?", "Chapter two. Akerlof's market.", lit={1970: r"Akerlof's lemons"},
             scale=("person", "market"), horizon=("a season",))
        self.crossing()
        self.vanish()
        self.gresham()
        self.called()

    def crossing(self):
        L = load("lemons")
        ps = np.array(L["prices"])
        ax = plane([0, 100], [0, 100], center=LEFT * 3.0 + DOWN * 0.3, x_length=5.4, y_length=5.0,
                   xticks=[0, 30, 60, 100], yticks=[0, 30, 60, 80, 100], xlabel=r"the market price, \ \$",
                   ylabel=r"\$", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        diag = seg(ax, 0, 0, 100, 100, color=GREY_B, width=2.5)
        dl = label(r"the price", font_size=15, color=GREY_B).next_to(a.c2p(88, 88), RIGHT, buff=0.08)
        val = path(ax, ps, L["add_value"], color=GOOD, width=3.5, smooth=False)
        vl = label(r"what the average boat for sale \\ is worth to a buyer", font_size=15, color=GOOD).next_to(
            a.c2p(12, 40), UP, buff=0.12)
        eq = Dot(a.c2p(L["add_p"], L["add_p"]), radius=0.1, color=EQ)
        side = VGroup(
            label(r"many buyers, \ each valuing a boat \\ at its worth to Bo plus \$30", font_size=21),
            label(r"at a price of $p$, \ every boat worth less than $p$ \\ is offered: \ on average worth $p/2$ to its "
                  r"owner, \\ $p/2 + 30$ to a buyer", font_size=21, color=GOOD),
            label(r"competition among buyers bids the price \\ up to that value: \ $p = p/2 + 30$", font_size=21),
            label(rf"so \${L['add_p']:.0f}: \ only boats worth less than \${L['add_p']:.0f} \\ trade, \ "
                  rf"{100 * L['add_share']:.0f}\% of them", font_size=22, color=EQ),
            label(rf"the best {100 * (1 - L['add_share']):.0f}\% never come to market: \\ \${L['add_lost']:.0f} "
                  r"of gains lost per boat on the island", font_size=21, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Now let many buyers bid for many boats, each buyer valuing a boat at its worth to its owner plus thirty "
            "dollars. <bookmark mark='a'/> At a market price of p, every owner whose boat is worth less than p puts it "
            "up for sale. The average boat for sale is then worth p over two to its owner, and p over two plus "
            "thirty to a buyer. <bookmark mark='b'/> Buyers compete, so the price rises until it equals what the "
            "average boat on sale is worth to them: p equals p over two plus thirty. <bookmark mark='c'/> The price "
            "settles at sixty dollars. Only boats worth less than sixty are sold, sixty percent of them. "
            "<bookmark mark='d'/> The best forty percent never come to market, though every one of them is worth "
            "thirty dollars more to a buyer than to its owner: twelve dollars of gains lost for every boat on the "
            "island."
        ) as vo:
            self.play(FadeIn(ax), Create(diag), FadeIn(dl), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(val), FadeIn(vl), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(eq, scale=1.5), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def vanish(self):
        L = load("lemons")
        ps = np.array(L["prices"])
        ax = plane([0, 100], [0, 100], center=LEFT * 3.0 + DOWN * 0.3, x_length=5.4, y_length=5.0,
                   xticks=[0, 50, 100], yticks=[0, 50, 75, 100], xlabel=r"the market price, \ \$", ylabel=r"\$",
                   font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        diag = seg(ax, 0, 0, 100, 100, color=GREY_B, width=2.5)
        val = path(ax, ps, L["mult_value"], color=LEMON, width=3.5, smooth=False)
        vl = label(r"$\tfrac32 \times p/2$", font_size=20, color=LEMON).next_to(a.c2p(80, 60), DOWN, buff=0.1)
        side = VGroup(
            label(r"Akerlof's own example: \ buyers value a car \\ at one and a half times its worth to the seller",
                  font_size=21),
            label(r"the average car offered at price $p$ \\ is worth $\tfrac32 \cdot \tfrac p2 = \tfrac34 p$ to a buyer: "
                  r"\\ less than $p$, \ whatever $p$ is", font_size=21, color=LEMON),
            label(r"so no price works: \ the market vanishes, \\ though every car is worth more to a buyer", font_size=22,
                  color=LOSS),
            label(r"unravelling: \ the best leave first, \\ then the next best, \ down to nothing", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Akerlof, QJE 84(3) (1970), section II; \ the curve: \ Agora", corner=DR, font_size=13)
        with self.voiceover(
            "Akerlof's own example is starker. <bookmark mark='a'/> Suppose buyers value a car at one and a half times "
            "its worth to the seller, rather than a fixed amount more. <bookmark mark='b'/> At any price p, the cars "
            "offered are worth p over two to their owners on average, and three quarters of p to a buyer: less than "
            "the price, whatever the price is. <bookmark mark='c'/> So no price works. The market vanishes, even "
            "though every car is worth more to a buyer than to its owner. <bookmark mark='d'/> Economists call it "
            "unravelling: at any price the best cars are withdrawn first, which lowers what buyers will pay, which "
            "withdraws the next best, and so on, down to nothing."
        ) as vo:
            self.play(FadeIn(ax), Create(diag), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(val), FadeIn(vl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def gresham(self):
        rows = VGroup(
            label(r"Gresham's law: \ bad money drives out good, \ because people spend the clipped coins and keep the "
                  r"rest", font_size=23),
            label(r"Akerlof's version: \ bad cars drive out good, \ because the good ones are worth more kept", font_size=23,
                  color=LEMON),
            label(r"a new car loses value the moment it leaves the showroom: \ partly because a car offered for sale "
                  r"is suspect", font_size=23, color=GREY_A),
            label(r"his other examples: \ insurance for the over-65s, \ hiring minorities, \ credit in India's "
                  r"villages, \ dishonesty", font_size=23, color=SIGNAL),
            label(r"the market's own remedies: \ guarantees, \ brand names, \ chains, \ licences: \ chapter 3",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.34).move_to(UP * 0.1)
        tag = published_tag(r"Akerlof, QJE 84(3) (1970)", corner=DR, font_size=13)
        with self.voiceover(
            "Akerlof saw an old idea in a new form. <bookmark mark='a'/> Gresham's law says that bad money drives out "
            "good: people spend their clipped and worn coins and hoard the full-weight ones. "
            "<bookmark mark='b'/> In the used-car market, bad cars drive out good ones, because the good ones are "
            "worth more kept than sold at a price that must allow for lemons. <bookmark mark='c'/> It explains a "
            "familiar puzzle: a new car loses much of its value the moment it is driven away, partly because a nearly "
            "new car offered for sale is suspect. <bookmark mark='d'/> Akerlof applied the idea to health insurance "
            "for people over sixty-five, to employers' treatment of minorities, to credit in India's villages, and to "
            "the cost of dishonesty. <bookmark mark='e'/> And he described the market's own remedies: guarantees, "
            "brand names, chains and licences, the subject of the next chapter."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["lemons_referees"]
        cc = call_card(r"the journals that turned Akerlof down", c.when,
                       r"trivial; \ or wrong, \ since if it were right \ no goods could be traded",
                       r"published in 1970; \ one of the most cited papers in economics; \ the 2001 Nobel prize with "
                       r"Spence and Stiglitz; \ used goods trade through the guarantees, \ brands and dealers \ the "
                       r"paper itself described", c.verdict, width=12.4, font_size=23).move_to(UP * 0.6)
        q = label(r"lemons markets don't vanish: \ they grow institutions, \ and those cost money", font_size=24,
                  color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Akerlof, QJE 84(3) (1970); \ the Nobel Foundation (2001)", corner=DR, font_size=13)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> The referees said the paper was trivial, or else wrong, since if it were "
            "right no goods could be traded. <bookmark mark='b'/> It became one of the most cited papers in economics, "
            "and won a share of the Nobel prize. Used goods do trade, every day, but through exactly the institutions "
            "the paper described as growing up to counter the problem. <bookmark mark='c'/> Wrong. Lemons markets "
            "don't vanish: they grow guarantees, brands and dealers, and those cost money, which is part of the price "
            "of not knowing."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3), FadeIn(q))
        self.clear_scene()
