from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403

Z = "#C9A0FF"


class AnythingGoes(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Anything goes: \ Sonnenschein, Mantel and Debreu", r"What does the theory say about an "
             r"economy's demand as a whole?", "Chapter eleven. Anything goes: Sonnenschein, Mantel and Debreu.",
             lit={1973: r"Sonnenschein; \ Mantel; \ Debreu"})
        self.three()
        self.theorem()
        self.cost()

    def three(self):
        s = load("smd")
        qs = np.array(s["qs"])
        z1 = np.array(s["z1"])
        ax = plane([np.log2(0.25), np.log2(4)], [-4, 5], center=LEFT * 2.7 + DOWN * 0.3, x_length=6.8,
                   y_length=5.0, xticks=[-2, -1, 0, 1, 2], yticks=[0], xlabel=r"price of good 1, \ in "
                   r"units of good 2 \ (log scale)", ylabel=r"excess demand for good 1 \ (stretched near zero)",
                   font_size=17,
                   xfmt=lambda v: {-2: "0.25", -1: "0.5", 0: "1", 1: "2", 2: "4"}[int(round(v))])
        a = ax.ax
        zero = DashedLine(a.c2p(-2, 0), a.c2p(2, 0), color=GREY_C, stroke_width=1.5)
        curve = path(ax, np.log2(qs), np.arcsinh(z1 / 1e-3), color=Z, width=4, yr=(-4, 5))
        dots, arrows = VGroup(), VGroup()
        for r, st in zip(s["roots"], s["stable"]):
            x = np.log2(r)
            dots.add(Dot(a.c2p(x, 0), radius=0.1, color=E.TRUTH if st else HOLD))
            for side_ in (-1, 1):
                start = a.c2p(x + side_ * (0.55 if st else 0.12), 0.0)
                end = a.c2p(x + side_ * (0.15 if st else 0.45), 0.0)
                arrows.add(Arrow(start, end, buff=0, stroke_width=3, color=E.TRUTH if st else HOLD,
                                 max_tip_length_to_length_ratio=0.35).shift(DOWN * 0.25))
        side = VGroup(
            label(r"two traders, \ two goods: \ each needs a little \\ of the other's good badly, \ and cares little "
                  r"beyond", font_size=21),
            label(r"convex, \ more is better: \ nothing unusual", font_size=21, color=GREY_A),
            label(r"three equilibria: \ prices $\tfrac12$, \ 1 \ and \ 2", font_size=24, color=Z),
            label(r"the auctioneer finds the outer two \\ and runs away from the middle one", font_size=21),
            label(r"which one? \ the theory can't say", font_size=23, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Scarf's economy cycled. Here's another way an economy can surprise. <bookmark mark='a'/> Two traders "
            "and two goods. Each owns mostly one good, needs at least a little of the other's badly, and beyond that "
            "doesn't care much for it. <bookmark mark='b'/> Their preferences are perfectly respectable: more is "
            "better, and the indifference curves bow the right way. <bookmark mark='c'/> But the excess demand for "
            "good one crosses zero three times. There are three equilibria, at relative prices of a half, one and "
            "two. <bookmark mark='d'/> The auctioneer would find the outer two: above them excess demand is "
            "negative, so the price falls back; below them it's positive, so it rises. The middle one is the "
            "reverse, and he runs away from it. <bookmark mark='e'/> Which equilibrium the economy ends up in, and "
            "so who is rich, the theory can't say."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(curve), FadeIn(dots), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.15), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def theorem(self):
        cards = VGroup(
            history_card(1973, r"Hugo Sonnenschein", r"which functions can be an economy's excess demand?", color=Z,
                         width=4.0, font_size=21),
            history_card(1974, r"Rolf Mantel", r"any of them, \ with enough traders", color=Z, width=4.0,
                         font_size=21),
            history_card(1974, r"G\'erard Debreu", r"as many traders as goods suffice", color=Z, width=4.0,
                         font_size=21),
        ).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"what adding up rational traders guarantees:", font_size=27),
            label(r"continuity, \ Walras's law, \ only relative prices matter \ (and wild demand when a price "
                  r"nears zero)", font_size=24, color=CC),
            label(r"and nothing else:", font_size=27),
            label(r"any function with those properties is the excess demand of some economy \\ of ordinary, "
                  r"rational traders", font_size=24, color=HOLD),
        ).arrange(DOWN, buff=0.32).next_to(cards, DOWN, buff=0.6)
        tag = published_tag(r"Sonnenschein, JET 6(4) (1973); Mantel, JET 7(3) (1974); Debreu, J.\ Math.\ Econ.\ 1(1) "
                            r"(1974)", corner=DR, font_size=13)
        with self.voiceover(
            "Is that example special? In the early nineteen seventies three economists showed that it is not. "
            "<bookmark mark='a'/> Hugo Sonnenschein asked which functions could be the excess demand of a whole "
            "economy. <bookmark mark='b'/> Rolf Mantel and Gerard Debreu completed the answer: any of them, given "
            "enough traders, and as many traders as goods is enough. <bookmark mark='c'/> Adding up rational "
            "traders guarantees only that excess demand is continuous, obeys Walras's law, depends only on "
            "relative prices, and behaves wildly as a price approaches zero. <bookmark mark='d'/> Beyond that, "
            "anything goes. Any function with those properties is the excess demand of some economy of perfectly "
            "ordinary traders."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2), FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.clear_scene()

    def cost(self):
        head = label(r"what it cost the programme", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"no general theorem of uniqueness: \ several equilibria are possible", font_size=25),
            label(r"no general theorem of stability: \ the auctioneer may never arrive", font_size=25),
            label(r"no general comparative statics: \ a shock's effect can go either way", font_size=25),
            label(r"so a model of one ``representative'' household is an assumption, \\ not a summary of many "
                  r"(Kirman, 1992)", font_size=23, color=HOLD),
            label(r"the way back: \ special structure (gross substitutes), \ or data: \\ economies observed at many "
                  r"endowments do have testable restrictions (Brown and Matzkin, 1996)", font_size=22,
                  color=CC),
        ).arrange(DOWN, buff=0.36).next_to(head, DOWN, buff=0.55)
        tag = published_tag(r"Kirman, J.\ Econ.\ Perspectives 6(2) (1992); Brown and Matzkin, Econometrica 64(6) "
                            r"(1996)", corner=DR, font_size=13)
        with self.voiceover(
            "That result cost general equilibrium theory a great deal. <bookmark mark='a'/> There is no general "
            "theorem that the equilibrium is unique. <bookmark mark='b'/> No general theorem that the auctioneer "
            "finds it. <bookmark mark='c'/> And no general rule for which way a shock moves prices. "
            "<bookmark mark='d'/> It also means that treating a whole economy as one representative household, as "
            "much of macroeconomics does, is an assumption, not a summary of many households; Alan Kirman made "
            "that case in 1992. <bookmark mark='e'/> There are two ways back. One is to assume more structure, "
            "like gross substitutes. The other is data: Donald Brown and Rosa Matzkin showed in 1996 that if we "
            "observe an economy at several different endowments, the theory does rule things out, and can be "
            "tested."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
