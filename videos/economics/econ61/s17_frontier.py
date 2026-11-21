from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ markets of agents", r"What happens to a marketplace when software shops and "
             r"sells for people?", "Chapter fifteen. Frontier: markets of agents.",
             lit={2020: r"Allcott et al.; \ Calvano et al."}, scale=("person", "market"), horizon=("a decade",))
        self.search()
        self.open_questions()

    def search(self):
        ks = np.arange(1, 31)
        lo, hi = 10.0, 20.0
        paid = lo + (hi - lo) / (ks + 1)          # the expected lowest of k prices drawn from U[10, 20]
        ax = plane([1, 30], [9, 16], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.4,
                   xticks=[1, 5, 10, 20, 30], yticks=[10, 12, 14, 16], xlabel=r"sellers checked before buying",
                   ylabel=r"expected price paid, \ \$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        curve = path(ax, ks, paid, RIDER, 3.0)
        cost = seg(ax, 1, lo, 30, lo, GREY_B, 1.4, dashed=True)
        cl = label(r"the lowest price on offer", font_size=15, color=GREY_B).next_to(ax.ax.c2p(30, lo), DOWN,
                                                                                    buff=0.08).shift(LEFT * 1.0)
        p_h, p_a = dot(ax, 2, paid[1], WHITE, 0.08), dot(ax, 20, paid[19], PLAT, 0.08)
        side = VGroup(
            label(r"prices across sellers spread from \$10 to \$20", font_size=19, color=WHITE),
            label(rf"a person checks two: \ pays \${paid[1]:.2f} on average", font_size=19, color=WHITE),
            label(rf"an agent checks twenty: \ \${paid[19]:.2f}", font_size=19, color=PLAT),
            label(r"but sellers would not sit still: \ when search is free, \\ the spread of prices itself "
                  r"shrinks", font_size=18, color=GREY_A),
            label(r"and sellers' agents learn too: \ prices set by algorithms \\ that may learn not to compete "
                  r"\ (Part 60)", font_size=18, color=SURGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = agora_tag(r"computed: \ the expected lowest of $k$ prices drawn evenly from \$10 to \$20", corner=DL,
                        font_size=12)
        with self.voiceover(
            "The frontier is a marketplace where software shops and sells on people's behalf. <bookmark "
            "mark='a'/> Suppose prices for the same thing spread from ten dollars to twenty. <bookmark mark='b'/> "
            f"A person checks a couple of sellers and pays, on average, {paid[1]:.2f}. <bookmark mark='c'/> An "
            f"agent that checks twenty pays {paid[19]:.2f}. <bookmark mark='d'/> But that holds the sellers "
            "still, and they would not stay still. When searching is free, the spread of prices that made it "
            "worth searching shrinks, as the economics of search predicts; the gains go to buyers through "
            "competition, not through bargains. <bookmark mark='e'/> And the sellers will have agents too, "
            "setting prices by algorithms that, as Part sixty showed, can learn not to compete. Who wins a market "
            "of agents depends on the rules the platform writes for them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(cost), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(curve))
            vo.wait_until("b")
            self.play(FadeIn(p_h), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(p_a), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def open_questions(self):
        cards = point_cards([
            (r"recommendation and welfare", r"a feed tuned for engagement is not a feed tuned for well-being: \ "
             r"Allcott, \ Braghieri, \ Eichmeyer and Gentzkow paid users to leave Facebook for four weeks, \ and "
             r"measured what changed", RIDER),
            (r"platforms for agents", r"who pays the commission, \ and what a ranking means, \ when the buyer is a "
             r"program?", PLAT),
            (r"experiments among agents", r"when every user's agent reacts to every test, \ chapter nine's "
             r"interference is everywhere", TEST),
            (r"what remains hard", r"welfare: \ platforms measure what users do, \ not whether they are better "
             r"off", SURGE),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Allcott, \ Braghieri, \ Eichmeyer and Gentzkow, \ American Economic Review 110(3) "
                            r"(2020)", corner=DL, font_size=12)
        with self.voiceover(
            "What remains open? <bookmark mark='a'/> Recommendation and welfare. A feed tuned for engagement is "
            "not a feed tuned for well-being. Hunt Allcott, Luca Braghieri, Sarah Eichmeyer and Matthew Gentzkow "
            "paid people to deactivate Facebook for four weeks before the 2018 American elections: they spent the "
            "time offline and with friends, reported somewhat higher well-being, and followed the news less. "
            "<bookmark mark='b'/> Platforms for agents: who pays the commission, and what does a ranking mean, "
            "when the buyer is a program? <bookmark mark='c'/> Experiments among agents: when every user's agent "
            "reacts to every test, chapter nine's interference is everywhere. <bookmark mark='d'/> And the hardest "
            "of all, which runs through the whole part: platforms measure what users do, and the economist's "
            "question is whether they are better off."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
