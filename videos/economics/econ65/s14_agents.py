from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403


class Agents(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Agents that transact", r"What happens to markets when both buyers and sellers are "
             r"software?", "Chapter twelve. Agents that transact.", lit={1980: "Varian"}, scale=("market",),
             horizon=("a day",))
        self.shoppers()
        self.sellers()
        self.design()

    def shoppers(self):
        S = load("shoppers")
        R = S["rows"]
        mu = np.array([r["mu"] for r in R])
        ax = plane([0, 1], [0.35, 1.02], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0.4, 0.6, 0.8, 1.0],
                   xlabel=r"share of buyers whose agent compares every price",
                   ylabel=r"price \ (full price 1, \ cost 0.4)", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        cost = seg(ax, 0, S["c"], 1, S["c"], GREY_C, 2.0, dashed=True)
        clab = label(r"cost", font_size=14, color=GREY_B).next_to(ax.ax.c2p(1, S["c"]), UP, buff=0.06).shift(
            LEFT * 0.3)
        lp = path(ax, mu, [r["mean_price"] for r in R], WORK, 3.0)
        ls = path(ax, mu, [r["shoppers_pay"] for r in R], MACH, 3.0)
        la = path(ax, mu, [r["average_paid"] for r in R], GDP, 3.4)
        key = legend_rows([(WORK, "the price a buyer without an agent pays"),
                           (MACH, "the lowest price, which agents find"),
                           (GDP, "the average price paid")], font_size=15).next_to(ax.ax, RIGHT, buff=0.3).shift(
            UP * 1.2)
        Fp = MathTex(r"F(p) = 1 - \Big[\frac{1-\mu}{n\mu}\,\frac{v-p}{p-c}\Big]^{\frac{1}{n-1}}", font_size=30,
                     color=GREY_A).next_to(ax.ax, RIGHT, buff=0.3).shift(DOWN * 0.6)
        eq = MathTex(r"\bar p = c + (1-\mu)(v-c)", font_size=34, color=GDP).next_to(Fp, DOWN, buff=0.4)
        tag = published_tag(rf"Varian, \ AER 70(4) (1980); \ {S['n']} sellers; \ agora.automation.shoppers",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Now let the software trade. Start with buyers. Hal Varian's model of sales, from 1980, has two kinds "
            "of buyer: shoppers, who compare every price, and the rest, who buy from the first shop they meet. "
            f"<bookmark mark='a'/> Here, {S['n']} sellers, a full price of one and a cost of 0.4. Sellers cannot "
            "settle on one price: they mix, running random sales to catch the shoppers while charging the others "
            "a lot. <bookmark mark='b'/> Now give a growing share of buyers an agent that checks every price. "
            "<bookmark mark='c'/> The prices sellers charge fall, the agents find the lowest, <bookmark mark='d'/> "
            "and the average price paid falls in a straight line, from the full price towards cost. The formula "
            "is exact: sellers earn just what they would by selling only to the buyers without agents, at the "
            "full price. A world in which every buyer has an agent is close to perfect competition."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(cost), FadeIn(clab), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(Fp))
            vo.wait_until("b")
            self.play(Create(lp), FadeIn(key[0]), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(ls), FadeIn(key[1]), run_time=1.6)
            vo.wait_until("d")
            self.play(Create(la), FadeIn(key[2]), Write(eq), run_time=1.8)
        self.clear_scene()

    def sellers(self):
        cards = point_cards([
            (r"learning price setters", r"Part 44's Q-learners, \ playing each other, \ settle well above the "
             r"competitive price, \ with no agreement to break \ (Calvano et al., \ 2020)", NAIVE),
            (r"language-model price setters", r"pricing agents built on language models reach prices above "
             r"competition quickly, \ and harmless-seeming changes to their instructions move how far \ (Fish, \ "
             r"Gonczarowski and Shorrer, \ 2024)", IDEA),
            (r"the law", r"cartel law punishes agreement; \ software that learns to avoid price wars agrees on "
             r"nothing \ (Part 44)", GDP),
        ], width=12.6, cols=1, font_size=19).move_to(DOWN * 0.1)
        head = label(r"and when the sellers are software", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Calvano, \ Calzolari, \ Denicol\`o and Pastorello, \ AER 110(10) (2020); \ Fish, \ "
                            r"Gonczarowski and Shorrer, \ arXiv 2404.00806 (2024)", corner=DL, font_size=12)
        with self.voiceover(
            "Sellers can have agents too. <bookmark mark='a'/> In Part forty-four, simple learning algorithms set "
            "prices against each other and, with no instruction to collude and no messages, settled well above "
            "the competitive price, punishing undercutting with price wars. <bookmark mark='b'/> Sara Fish, Yannai "
            "Gonczarowski and Ran Shorrer gave the same job to agents built on language models. They reached "
            "prices above competition quickly, and seemingly harmless changes to the wording of their "
            "instructions changed how far. <bookmark mark='c'/> Cartel law punishes agreements. Software that "
            "learns to avoid price wars agrees on nothing. A market where both sides are software could be more "
            "competitive than any before, or less, depending on whose agents are smarter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def design(self):
        cards = point_cards([
            (r"signals lose their cost", r"when a polished application costs nothing, \ it stops showing "
             r"effort: \ Part 13's signals need new costs", WORK),
            (r"congestion", r"agents can apply, \ bid and message at no cost: \ Part 17's markets need "
             r"limits on how many", MACH),
            (r"identity and liability", r"who is bound by a contract an agent signs, \ and who pays when it "
             r"errs?", GDP),
            (r"speed", r"markets that clear in milliseconds, \ as in finance: \ an arms race of speed, \ "
             r"everywhere", NAIVE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"new questions for market design", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "This brings back the questions of market design. <bookmark mark='a'/> When a polished cover letter "
            "costs nothing to write, it stops signalling effort or interest: the signals of Part thirteen work "
            "only while they are costly. <bookmark mark='b'/> When agents can apply, bid and message at no cost, "
            "the markets of Part seventeen will need limits on how many, like the caps on applications in "
            "school choice. <bookmark mark='c'/> Who is bound by a contract an agent signs, and who pays when it "
            "makes a mistake? <bookmark mark='d'/> And markets everywhere may come to clear at machine speed, "
            "with the arms race that high-frequency trading brought to finance."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
