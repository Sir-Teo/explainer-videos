from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

MIXED = "#F2C14E"


def pair_glyph(height=0.9):
    a = islander("ana", height)
    b = islander("bo", height)
    return VGroup(a, b).arrange(RIGHT, buff=0.9)


class Hook(VoiceoverScene):
    def construct(self):
        self.rand()
        self.nash()
        self.today()
        self.question()
        self.title()
        self.objectives()

    def rand(self):
        f = tables.FLOOD_1952.data
        hc = history_card(1950, r"Merrill Flood and Melvin Dresher, \ at the RAND Corporation", r"a new game, \ played "
                          r"a hundred times in a row by two colleagues, \ Armen Alchian and John Williams", color=EQ,
                          width=11.6, font_size=24).to_edge(UP, buff=0.45)
        cc, dd = f["mutual_cooperation"], f["mutual_defection"]
        other = f["rounds"] - cc - dd
        colors = [COOP] * cc + [MIXED] * other + [DEFECT] * dd
        cells = VGroup(*[Square(side_length=0.3, stroke_width=0, fill_color=c, fill_opacity=0.9) for c in colors])
        cells.arrange_in_grid(rows=5, cols=20, buff=0.07).next_to(hc, DOWN, buff=0.55)
        key = VGroup(
            label(rf"both cooperated: \ {cc}", font_size=22, color=COOP),
            label(rf"one cooperated, \ one defected: \ {other}", font_size=22, color=MIXED),
            label(rf"both defected, \ the equilibrium: \ {dd}", font_size=22, color=DEFECT),
        ).arrange(RIGHT, buff=0.6).next_to(cells, DOWN, buff=0.35)
        note_ = label(r"counts of the hundred rounds, \ not their order", font_size=17, color=GREY_B).next_to(
            key, DOWN, buff=0.15)
        rows = VGroup(
            label(r"each round, \ each could cooperate or defect; \ defecting was better for each, \ whatever the "
                  r"other did", font_size=23),
            label(r"so the new theory said: \ defect, \ every time", font_size=24, color=DEFECT),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Flood, RAND RM-789-1 (1952), \ as reported by Poundstone (1992)", corner=DR, font_size=13)
        with self.voiceover(
            "At the start of 1950, at the RAND Corporation in Santa Monica, two mathematicians, Merrill Flood and "
            "Melvin Dresher, invented a game to test a new idea. <bookmark mark='a'/> They had two colleagues, the "
            "economist Armen Alchian and RAND's John Williams, play it a hundred times in a row. "
            "<bookmark mark='b'/> In each round each player could cooperate or defect, and whatever the other did, "
            "defecting paid more. <bookmark mark='c'/> So the new theory said: defect, every time. "
            "<bookmark mark='d'/> They didn't. In sixty of the hundred rounds, both cooperated. Only fourteen times "
            "did both defect, the outcome the theory predicted."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(key), FadeIn(note_))
        self.clear_scene()

    def nash(self):
        f = tables.FLOOD_1952.data
        hc = history_card(1950, r"John Nash, \ a Princeton graduate student", r"``Equilibrium Points in $n$-Person "
                          r"Games'': \ a choice for each player that is best, \ given everyone else's", color=EQ,
                          width=11.0, font_size=24).to_edge(UP, buff=0.5)
        q = quote_card(r"the flaw in this experiment as a test of equilibrium point theory is that the experiment "
                       r"really amounts to having the players play one large multimove game", r"John Nash, \ in a "
                       r"comment printed in Flood's report", width=11.0, font_size=25).next_to(hc, DOWN, buff=0.5)
        rows = VGroup(
            label(r"a hundred rounds are one long game, \ in which today's move can reward or punish yesterday's",
                  font_size=24, color=COOP),
            label(r"months later, \ Albert Tucker told the game as a story about two prisoners: \ the prisoner's "
                  r"dilemma", font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(q, DOWN, buff=0.45)
        tag = published_tag(r"Nash, PNAS 36(1) (1950); \ the comment via Poundstone (1992)", corner=DR, font_size=13)
        with self.voiceover(
            "The new idea was John Nash's. <bookmark mark='a'/> A Princeton graduate student, he had defined an "
            "equilibrium of a game as a choice for each player that is best for them, given what everyone else "
            "chooses. <bookmark mark='b'/> Shown the results, Nash replied that the flaw in the experiment as a test "
            "of his theory was that it really amounted to having the players play one large multimove game. "
            "<bookmark mark='c'/> A hundred rounds are not a hundred separate games: in one long game, today's move "
            "can reward or punish yesterday's. <bookmark mark='d'/> That spring Albert Tucker, Nash's thesis "
            "adviser, told the game as a story about two prisoners, and the name stuck: the prisoner's dilemma."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        del f
        self.clear_scene()

    def today(self):
        rows = point_cards([
            (r"a few firms", r"setting prices, \\ each watching the others", BO),
            (r"bidding", r"for a painting, \ a licence, \\ an advertising slot", ANA),
            (r"arms races", r"and the treaties \\ that slowed them", USSR),
            (r"standards", r"which plug, \ which side \\ of the road", COOP),
            (r"bargaining", r"over wages, \ prices, \\ a peace", LEVEL),
            (r"climate", r"every country gains \\ if the others cut", EQ),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
        head = label(r"whenever my best choice depends on yours", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Situations like this are everywhere economics looks once a market has only a few players. "
            "<bookmark mark='a'/> A handful of firms setting prices, each watching the others. Bidders for a "
            "painting, a radio licence or an advertising slot. Two powers building weapons, and the treaties that "
            "slowed them. Which plug a country uses, or which side of the road it drives on. A union and a firm "
            "bargaining over wages. And climate: every country gains if the others cut their emissions. "
            "<bookmark mark='b'/> In each, what is best for me depends on what you do, and what is best for you "
            "depends on me."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards], lag_ratio=0.5), run_time=6)
            vo.wait_until("b")
            self.play(Indicate(head, color=WHITE))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what will people do, \ when each is predicting the others?", font_size=29, color=ANA),
            label(r"when does selfishness defeat everyone, \ and when does cooperation survive?", font_size=29,
                  color=COOP),
            label(r"and how well does the theory predict real people?", font_size=29, color=LEVEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Until now, every decision in this series was made against prices or nature, never against another "
            "mind. This part asks: what happens when my best choice depends on yours, and yours on mine? "
            "<bookmark mark='a'/> What will people do, when each is predicting what the others will do? "
            "<bookmark mark='b'/> When does selfishness leave everyone worse off, and when does cooperation survive? "
            "<bookmark mark='c'/> And how well does the theory predict what real people do?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = pair_glyph(1.0)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 11 \ $\cdot$ \ Games", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part eleven: games."):
            self.play(FadeIn(logo, shift=UP * 0.2), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act III \ $\cdot$ \ Markets", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"play the guessing game; \ dominance, \ iterated elimination, \ Nash equilibrium",
            r"four games that describe social life; \ mixed strategies, \ tested on penalty kicks",
            r"games in time: \ subgame perfection, \ the centipede, \ the ultimatum game",
            r"repetition: \ the folk theorem, \ Axelrod's tournaments, \ correlated equilibrium, \ evolution",
            r"levels of thinking fitted to data, \ incomplete information, \ bargaining, \ and learning at scale",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Three, on markets, with the tool for markets of a few. "
            "<bookmark mark='a'/> You'll play a guessing game, and we'll use it to meet dominance, the iterated "
            "elimination of bad choices, and Nash equilibrium. <bookmark mark='b'/> Four simple games that describe "
            "much of social life, and mixed strategies, tested on professional footballers. "
            "<bookmark mark='c'/> Games that unfold in time: credible threats, the centipede and the ultimatum game. "
            "<bookmark mark='d'/> Repetition: the folk theorem, Axelrod's tournaments, the traffic light, and "
            "evolution. <bookmark mark='e'/> And levels of thinking fitted to data, games with private information, "
            "bargaining, and how machines now learn to play."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
