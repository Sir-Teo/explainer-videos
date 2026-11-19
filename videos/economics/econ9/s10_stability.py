from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403
from videos.economics.econ9.s09_existence import Simplex


class Stability(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Does it get there? \ The auctioneer and Scarf's cycle", r"If prices move toward excess "
             r"demand, do they find the equilibrium?", "Chapter eight. Does it get there? The auctioneer, and Scarf's "
             "cycle.", lit={1960: r"Scarf's cycle"})
        self.auctioneer()
        self.scarf()
        self.lab()

    def auctioneer(self):
        d = load("dynamics")
        s = load("simplex")
        S = Simplex(5.6, center=LEFT * 2.8 + DOWN * 0.2)
        eq = Dot(S.p2p(s["exact"]), radius=0.09, color=E.ACCENT)
        cols = (ANA, BO, FRIDAY)
        paths = VGroup()
        starts = VGroup()
        for p_, c in zip(d["paths"], cols):
            pts = [S.p2p(p) for p in p_]
            paths.add(VMobject(stroke_color=c, stroke_width=3).set_points_smoothly(pts))
            starts.add(Dot(pts[0], radius=0.07, color=c))
        side = VGroup(
            label(r"Walras's auctioneer calls out prices; \\ nobody trades until every market clears", font_size=22),
            MathTex(r"\frac{dp_k}{dt} = z_k(p)", font_size=40, color=E.ACCENT),
            label(r"raise the price of whatever is in excess demand", font_size=21, color=GREY_A),
            label(r"from any start, \ the island's prices find it", font_size=22, color=CC),
            label(r"Arrow, Block and Hurwicz (1959): \\ when all goods are gross substitutes, \\ the auctioneer "
                  r"always succeeds", font_size=21, color=CC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Existence says the equilibrium is there. Does anything find it? Walras imagined an auctioneer. "
            "<bookmark mark='a'/> He calls out a price list, everyone says what they would buy and sell at it, and "
            "nobody trades until every market clears. <bookmark mark='b'/> In between, he raises the price of "
            "every good in excess demand and lowers the price of every good in excess supply, in proportion to the "
            "imbalance. <bookmark mark='c'/> On the island, start the auctioneer anywhere and the prices find the "
            "equilibrium. <bookmark mark='d'/> That isn't luck either. In 1959 Kenneth Arrow, Henry Block and "
            "Leonid Hurwicz proved that if every good is a gross substitute for every other, so that a higher "
            "price for one raises the demand for all the rest, the auctioneer always succeeds. Cobb–Douglas "
            "tastes like the islanders' have that property."
        ) as vo:
            self.play(Create(S.tri), FadeIn(S.corners), FadeIn(eq), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(starts), *[Create(p_) for p_ in paths], FadeIn(side[3]), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def scarf(self):
        d = load("dynamics")
        S = Simplex(5.6, center=LEFT * 2.8 + DOWN * 0.2)
        eq = Dot(S.p2p(d["scarf_eq"]), radius=0.09, color=E.ACCENT)
        pts = [S.p2p(p) for p in d["scarf"]]
        orbit = VMobject(stroke_color=HOLD, stroke_width=3).set_points_smoothly(pts)
        mover = Dot(pts[0], radius=0.1, color=HOLD)
        side = VGroup(
            label(r"Scarf (1960): \ three traders, \ three goods", font_size=23, color=HOLD),
            label(r"trader $i$ owns one unit of good $i$, \\ and wants goods $i$ and $i+1$ in equal amounts",
                  font_size=21),
            label(r"the only equilibrium: \ equal prices", font_size=22, color=E.ACCENT),
            label(r"the auctioneer circles it for ever", font_size=23, color=HOLD),
            label(rf"conserved: \ $\sum_k p_k^2 = {d['scarf_norm'][0]:.4f}$ \ and \ "
                  rf"$p_1 p_2 p_3 = {d['scarf_product'][0]:.4f}$", font_size=21, color=GREY_A),
            label(r"two conserved quantities: \ a closed orbit", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "But not every economy is like that. <bookmark mark='a'/> In 1960 Herbert Scarf built one with three "
            "traders and three goods. <bookmark mark='b'/> Each owns one unit of one good, and wants two goods in "
            "fixed, equal amounts: his own and the next one round. Left and right shoes, more or less. "
            "<bookmark mark='c'/> By symmetry, the only equilibrium has all three prices equal. "
            "<bookmark mark='d'/> Start the auctioneer anywhere else, and the prices go round and round it, for "
            "ever. <bookmark mark='e'/> The reason is two quantities the dynamics can't change: the sum of the "
            "squared prices, which Walras's law fixes, and their product. <bookmark mark='f'/> A path that keeps "
            "both fixed can't approach the centre; it can only circle. Every good is a complement to another, and "
            "the gross-substitutes condition fails."
        ) as vo:
            self.play(Create(S.tri), FadeIn(S.corners), FadeIn(eq), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(eq, color=E.ACCENT))
            vo.wait_until("d")
            self.play(FadeIn(mover), FadeIn(side[3]))
            self.play(MoveAlongPath(mover, orbit), Create(orbit), run_time=5, rate_func=linear)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]), MoveAlongPath(mover, orbit), run_time=3, rate_func=linear)
        self.clear_scene()

    def lab(self):
        hc = history_card(2004, r"Anderson, Plott, Shimomura and Granat", r"Scarf's economy in the laboratory, "
                          r"traded in a double auction: \ average prices each period followed the predicted cycle",
                          color=HOLD, width=11.0, font_size=24).move_to(UP * 1.7)
        rows = VGroup(
            label(r"existence: \ a theorem, \ for a wide class of economies", font_size=27, color=CC),
            label(r"stability: \ only for special classes, \ like gross substitutes", font_size=27, color=HOLD),
            label(r"a real market is not an auctioneer: \ people trade before prices settle", font_size=25,
                  color=GREY_A),
            label(r"so equilibrium is a prediction to test, \ not a promise", font_size=27, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).next_to(hc, DOWN, buff=0.55)
        tag = published_tag(r"Anderson et al., Journal of Economic Theory 115(2) (2004) 209--249", corner=DR,
                            font_size=14)
        with self.voiceover(
            "Is Scarf's cycle only a curiosity of the mathematics? <bookmark mark='a'/> In 2004 Christopher "
            "Anderson, Charles Plott, Ken-Ichi Shimomura and Sander Granat put his economy into a laboratory, with "
            "people trading in a double auction like the one in Part two. The average prices, period by period, "
            "went round in the direction the theory predicted. <bookmark mark='b'/> So here is the state of "
            "things. Existence is a theorem, for a wide class of economies. <bookmark mark='c'/> Stability holds "
            "only for special classes. <bookmark mark='d'/> And real markets have no auctioneer: people trade at "
            "prices that are still wrong. <bookmark mark='e'/> An equilibrium is a prediction to test, not a "
            "promise."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
