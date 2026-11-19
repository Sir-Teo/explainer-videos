from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403

PERS = "#C9A0FF"
UNIF = "#F2A65A"


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ prices set by machine learning", r"If a seller can predict each buyer's value, "
             r"what happens to prices, profits and buyers?", "Chapter sixteen. Frontier: prices set by machine "
             "learning.", lit={2023: r"Dub\'e and Misra"}, scale=("person", "firm", "market"))
        self.study()
        self.agora()
        self.questions()

    def study(self):
        dm = load("dial")["dube_misra"]
        hc = history_card(2023, r"Jean-Pierre Dub\'e and Sanjog Misra", r"personalized prices for a subscription "
                          r"to an online recruiting platform, \ learned from a field experiment", color=PERS,
                          width=10.4, font_size=23).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"first, \ randomize: \ new customers are shown prices drawn at random", font_size=24),
            label(r"then learn: \ a model of who buys at which price, \ from everything known about each customer",
                  font_size=24),
            label(r"then price: \ each customer gets the price the model says earns most", font_size=24),
            label(rf"profit: \ +{100 * dm['profit_vs_uniform']:.0f}\% against the best single price, \ "
                  rf"+{100 * dm['profit_vs_status_quo']:.0f}\% against the firm's old price", font_size=24,
                  color=PROFIT),
            label(rf"buyers: \ total consumer surplus falls, \ but more than {100 * dm['share_who_gain']:.0f}\% "
                  r"of customers are better off", font_size=24, color=CS),
        ).arrange(DOWN, buff=0.32).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Dub\'e and Misra, Journal of Political Economy 131(1) (2023), abstract", corner=DR,
                            font_size=14)
        with self.voiceover(
            "First-degree discrimination needs the seller to know each buyer's value. It used to be a thought "
            "experiment. In 2023 Jean-Pierre Dubé and Sanjog Misra reported what happened when "
            "an online recruiting platform, ZipRecruiter, tried to get close. <bookmark mark='b'/> First, new "
            "customers were shown prices drawn at random. <bookmark mark='c'/> Then a machine-learning model "
            "learned who buys at which price, from everything the firm knew about each customer. "
            "<bookmark mark='d'/> Then each customer was offered the price the model said would earn most. "
            "<bookmark mark='e'/> Profits rose nineteen percent compared with the best single price, and "
            "eighty-six percent compared with the price the firm had been charging. <bookmark mark='f'/> Total "
            "consumer surplus fell. But more than sixty percent of customers were better off, because the "
            "personalized price lets the seller cut prices for buyers it would otherwise have lost."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def agora(self):
        r = load("personal")
        hist, grid = np.array(r["hist"], float), np.array(r["grid"])
        share = hist / hist.sum()
        top = float(share.max()) * 1.15
        ax = plane([0, 8], [0, top], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.2, y_length=4.8,
                   xticks=[0, 2, 4, 6, 8], yticks=[0, round(top / 2, 2), round(top, 2)], xlabel=r"price offered, \ \$",
                   ylabel=r"share of buyers", font_size=16, yfmt=lambda v: f"{100 * v:.0f}\\%")
        a = ax.ax
        mids = grid
        w = 0.8 * (grid[1] - grid[0])
        bars = VGroup(*[Rectangle(width=a.c2p(w, 0)[0] - a.c2p(0, 0)[0], height=max(a.c2p(0, s)[1] - a.c2p(0, 0)[1],
                                                                                     1e-3),
                                  stroke_width=0, fill_color=PERS, fill_opacity=0.85).move_to(a.c2p(x, 0),
                                                                                            aligned_edge=DOWN)
                        for x, s in zip(mids, share) if x <= 8 and s > 0])
        pu = r["p_uniform"]
        uline = DashedLine(a.c2p(pu, 0), a.c2p(pu, top), color=UNIF, stroke_width=2.5)
        ul = label(rf"the best single price, \ \${pu:.2f}", font_size=17, color=UNIF).next_to(a.c2p(pu, top), RIGHT,
                                                                                            buff=0.1).shift(DOWN * 0.2)
        u, p, f = r["uniform"], r["personal"], r["first_degree"]
        side = VGroup(
            label(r"Agora: \ six things known about each buyer, \\ three that matter; \ 8{,}000 buyers shown random "
                  r"prices", font_size=20),
            label(r"a logit of buying on the features and the price, \\ then a price for each buyer", font_size=20,
                  color=GREY_A),
            label(rf"profit: \ +{100 * r['profit_gain']:.0f}\% \ (to \${p['profit']:.2f} a buyer from "
                  rf"\${u['profit']:.2f})", font_size=21, color=PROFIT),
            label(rf"buyers served: \ {100 * u['share_buying']:.0f}\% $\to$ {100 * p['share_buying']:.0f}\%", font_size=21,
                  color=GREY_A),
            label(rf"{100 * r['share_pay_less']:.0f}\% pay less; \ consumer surplus {100 * r['cs_change']:.0f}\%",
                  font_size=21, color=CS),
            label(rf"total surplus up: \ \${u['total']:.2f} $\to$ \${p['total']:.2f}, \\ of the \${f['total']:.2f} "
                  r"first-degree pricing would take", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Agora runs the same experiment on simulated buyers. <bookmark mark='a'/> The seller knows six things "
            "about each buyer, of which three in fact matter to what they would pay. Eight thousand buyers are "
            "shown random prices. <bookmark mark='b'/> A logit model of buying, on the features and the price, "
            "recovers the truth, and then each new buyer is offered the price the model says earns most. Here is "
            "where those prices fall, around the best single price of two dollars eighty. <bookmark mark='c'/> "
            "Profit rises by almost a quarter. <bookmark mark='d'/> Far more buyers are served: about two in three, "
            "instead of one in two. <bookmark mark='e'/> Two thirds of buyers pay less than the single price, and "
            "consumer surplus falls by six percent, because those who pay more lose more than the rest gain. "
            "<bookmark mark='f'/> Total surplus rises, but the seller takes all of the gain and some of what buyers "
            "had: personalized pricing is a step toward first degree."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03),
                      Create(uline), FadeIn(ul), run_time=2.5)
            for mk, r_ in zip("cdef", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def questions(self):
        head = label(r"open questions", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"fairness: \ is it acceptable to charge people more because of who they are?", font_size=24),
            label(r"strategy: \ buyers who know they are being read change what they reveal", font_size=24),
            label(r"collusion: \ Calvano, Calzolari, Denicol\`o and Pastorello (2020): \ learning algorithms, \\ "
                  r"in simulated markets, \ taught themselves to keep prices high and to punish price cuts",
                  font_size=23, color=HOLD),
            label(r"Assad, Clark, Ershov and Xu (2024), \ German petrol stations: \\ in local duopolies, "
                  r"margins rose only when both stations adopted pricing software", font_size=23, color=HOLD),
            label(r"the economics of prices set by machines: \ Parts 12, 44 and 60", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.55)
        tag = published_tag(r"Calvano et al., AER 110(10) (2020); Assad et al., JPE 132(3) (2024), abstracts", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Prices set by machines raise questions economics is still working on. <bookmark mark='a'/> Fairness: "
            "is it acceptable to charge people more because of who they are, or where they live? "
            "<bookmark mark='b'/> Strategy: buyers who know their behaviour sets their price will change their "
            "behaviour. <bookmark mark='c'/> And collusion. In 2020, Emilio Calvano, Giacomo Calzolari, Vincenzo "
            "Denicolò and Sergio Pastorello showed that simple learning algorithms, competing in simulated markets, "
            "taught themselves to keep prices high and to punish any rival that cut, with no instruction to "
            "collude. <bookmark mark='d'/> Stephanie Assad, Robert Clark, Daniel Ershov and Lei Xu then studied "
            "German petrol stations, and found that in local duopolies margins rose only when both stations adopted "
            "pricing software. <bookmark mark='e'/> Competition among a few sellers, human or machine, is the subject of "
            "Part twelve, and Parts forty-four and sixty return to the machines."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
