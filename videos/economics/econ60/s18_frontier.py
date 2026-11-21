from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ pricing with learning", r"Can a firm learn its demand curve \ while it sets "
             r"the price?", "Chapter sixteen. Frontier: pricing with learning.",
             lit={1933: r"Thompson", 2019: r"bandit pricing"}, scale=("firm",), horizon=("a day", "a year"))
        self.bandit()
        self.open_()

    def bandit(self):
        B = load("bandit")
        t, ts, tc = np.array(B["t"], float) / 1000, np.array(B["ts"]) / 1000, np.array(B["tc"]) / 1000
        top = float(max(tc.max(), ts.max())) * 1.1
        ax = plane([0, 20], [0, top], center=LEFT * 3.1 + DOWN * 0.4, x_length=6.0, y_length=4.6,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 5, 10, 15, 20], xlabel=r"customers, \ thousands",
                   ylabel=r"revenue lost against the best price, \ \$000", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        c1 = path(ax, t, tc, COST, 3.0, smooth=False)
        c2 = path(ax, t, ts, LEIS, 3.0, smooth=False)
        tl = vline(ax, B["test"] / 1000, 0, top, GREY_B, 1.4)
        side = VGroup(
            label(rf"six prices from \${B['prices'][0]:.0f} to \${B['prices'][-1]:.0f}; \ the best is "
                  rf"\${B['best_price']:.0f}, \ but the firm does not know it", font_size=19, color=GREY_A),
            label(rf"red: \ test each price on {B['test']:,} customers, \ then commit".replace(",", "{,}"),
                  font_size=19, color=COST),
            label(r"green: \ Thompson sampling: \ keep a posterior on each price's sales, \\ draw from it, \ charge "
                  r"the price that looks best in the draw", font_size=19, color=LEIS),
            label(r"the test wastes customers on bad prices, \ then stops learning; \\ sampling shifts to good prices "
                  r"as the evidence comes in", font_size=18, color=WHITE),
            label(r"the A/B test and the price are one activity", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.1:
            side.width = 6.1
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ 40 runs of 20,000 customers; \ agora.revenue.bandit\_pricing"
                         .replace(",", "{,}"), corner=DL, font_size=12)
        with self.voiceover(
            "The frontier joins the experiment to the price. <bookmark mark='a'/> A seller can charge any of six "
            f"prices; the best, unknown to it, is {B['best_price']:.0f} dollars. <bookmark mark='b'/> The classic "
            f"approach tests every price on {B['test']:,} customers, picks the winner, and commits. Its losses pile "
            "up during the test, and after it, whenever the test picked wrong, they keep growing. <bookmark "
            "mark='c'/> Thompson sampling, an idea from 1933, keeps a probability distribution over each price's "
            "chance of a sale, draws from it, and charges whichever price looks best in the draw. Prices that might "
            "be best keep being tried; prices that are clearly worse stop. <bookmark mark='d'/> Over twenty "
            "thousand customers it loses far less, and its losses grow ever more slowly. <bookmark mark='e'/> "
            "Pricing algorithms built on such bandits are now common online; the experiment and the price have "
            "become one activity, with chapter three's interference still to worry about."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(tl), Create(c1), FadeIn(side[1]), run_time=1.8)
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(side[2]), run_time=1.8)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def open_(self):
        cards = point_cards([
            (r"pricing AI services", r"usage priced per token or request, \ subscriptions in tiers by model: \ "
             r"versions, \ bundles and two-part tariffs again", AIR),
            (r"learning with many products", r"cross-price effects: \ a discount on one item moves another's "
             r"sales, \ so items cannot be learned one at a time", LEIS),
            (r"fairness constraints", r"personalized prices with limits on how far they may differ, \ by law or "
             r"by choice", BUS),
            (r"algorithms that meet", r"learning sellers facing learning sellers: \ when does the outcome look "
             r"like collusion?", COST),
        ], width=12.6, cols=2, font_size=20).move_to(UP * 0.1)
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.45)
        hard = label(r"what remains hard: \ a demand curve that changes because you are learning it", font_size=21,
                     color=HOLD).next_to(cards, DOWN, buff=0.45)
        with self.voiceover(
            "What remains open? <bookmark mark='a'/> Pricing AI services, sold by usage, per token or per request, "
            "and by subscription tiers: the questions are this part's, versions, bundles and two-part tariffs, with "
            "costs that fall fast. <bookmark mark='b'/> Learning with many products, where a discount on one item "
            "moves another's sales, so items cannot be learned one at a time. <bookmark mark='c'/> Personalized "
            "prices with fairness constraints, limits on how far prices may differ between buyers. <bookmark "
            "mark='d'/> And learning sellers facing learning sellers, where the outcome may look like collusion "
            "with no one intending it. <bookmark mark='e'/> What remains hardest is that buyers learn too: a demand "
            "curve that a firm is busy learning can change because the firm is learning it."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(hard))
        self.clear_scene()
