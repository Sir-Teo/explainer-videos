from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 14, r"Frontier: prices set by algorithms", r"Do the scissors still cut when the traders are "
             r"programs?", "Chapter fourteen. Frontier: prices set by algorithms.",
             lit={2020: r"algorithms that learn to collude"}, scale=("firm", "market"), horizon=("a day", "a year"))
        self.sim()
        self.field()
        self.open_()

    def sim(self):
        sc = study_card(r"Algorithms that learn to collude", r"Calvano, Calzolari, Denicol\`o and Pastorello (2020)",
                        [(r"what", r"two pricing programs that learn by trial and error (Q-learning), \ competing "
                                   r"again and again in a simulated market"),
                         (r"found", r"they learn to charge prices above the competitive level, \ without "
                                    r"communicating"),
                         (r"how", r"a price cut is met by a short punishment, \ then a gradual return to high "
                                  r"prices")],
                        design="structural", width=11.0, font_size=23).move_to(UP * 0.1)
        src = published_tag(r"\emph{American Economic Review} 110(10), 2020", corner=DR, font_size=16)
        with self.voiceover(
            "This part's learning traders were simple programs, and they found the competitive price. Real "
            "markets are now full of pricing programs far cleverer than they are. <bookmark mark='a'/> In 2020 four "
            "economists in Bologna, Emilio Calvano and his co-authors, set two learning algorithms to compete in a "
            "simulated market, over and over. <bookmark mark='b'/> The programs were never told to cooperate, and "
            "never communicated. They learned to charge prices above the competitive level anyway. "
            "<bookmark mark='c'/> And they learned how to keep them there: when one cut its price, the other "
            "punished it with a short price war, and then both drifted back up. That's how a cartel behaves, and "
            "no person had arranged it."
        ) as vo:
            self.play(FadeIn(src), FadeIn(sc.card), FadeIn(sc.head), FadeIn(sc[2]))
            vo.wait_until("a")
            self.play(FadeIn(sc.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(sc.body[1]))
            vo.wait_until("c")
            self.play(FadeIn(sc.body[2]))
        self.clear_scene()

    def field(self):
        sc = study_card(r"Algorithmic pricing at German petrol stations",
                        r"Assad, Clark, Ershov and Xu (2024)",
                        [(r"what", r"pricing software became widely available to German petrol stations in 2017"),
                         (r"found", r"margins rose, \ but only where a station had competitors"),
                         (r"and", r"in markets with two or three stations, \ only when all of them adopted it")],
                        design="DiD", width=11.0, font_size=23).move_to(UP * 0.1)
        src = published_tag(r"\emph{Journal of Political Economy} 132(3), 2024", corner=DR, font_size=16)
        with self.voiceover(
            "Is it happening outside the laboratory? <bookmark mark='a'/> When pricing software became widely "
            "available to German petrol stations in 2017, Stephanie Assad, Robert Clark, Daniel Ershov and Lei Xu "
            "followed what happened to their margins. <bookmark mark='b'/> Margins rose, but only for stations that "
            "had competitors nearby; a station with no rival gained nothing. <bookmark mark='c'/> And where two or "
            "three stations shared a market, margins rose only when all of them had adopted. That's the pattern "
            "you'd expect if the algorithms were learning to soften competition with each other."
        ) as vo:
            self.play(FadeIn(src), FadeIn(sc.card), FadeIn(sc.head), FadeIn(sc[2]))
            vo.wait_until("a")
            self.play(FadeIn(sc.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(sc.body[1]))
            vo.wait_until("c")
            self.play(FadeIn(sc.body[2]))
        self.clear_scene()

    def open_(self):
        head = heading(r"What is open")
        items = [
            (r"is it collusion?", r"programs that were never told to cooperate: \ who is responsible, \ and what "
             r"would the law forbid? (Parts 12, 59)", E.MISS),
            (r"thin markets", r"where few trades happen, \ how is a price discovered at all: \ new commodities, "
             r"carbon, \ rare assets (Parts 16, 44)", COFFEE),
            (r"speed", r"when prices change in microseconds, \ the race to be first can waste resources: \ batch "
             r"auctions as a fix (Part 23)", E.DEMAND),
        ]
        pc = point_cards(items, width=12.8, cols=3, font_size=22).move_to(UP * 0.3)
        star = label(r"$\star$ \ research problem: \ in Agora, replace the learning traders with two Q-learning "
                     r"sellers, \ and find when their price stays above the band", font_size=22,
                     color=E.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So here is what's open. <bookmark mark='a'/> If two programs learn to keep prices high without ever "
            "agreeing to, is that collusion, who is responsible, and what should the law forbid? Competition law "
            "was written for people who meet in smoke-filled rooms. <bookmark mark='b'/> Second, thin markets, "
            "where so few trades happen that it's not obvious a price is being discovered at all. "
            "<bookmark mark='c'/> And third, speed: when prices move in millionths of a second, the race to be first "
            "can waste real resources, and some economists propose holding auctions in tiny batches instead. "
            "<bookmark mark='d'/> The research problem for this part puts two learning sellers into Agora's pit, and "
            "asks when their price stays above the band."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c in zip("abc", pc.cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(star))
        self.clear_scene()
