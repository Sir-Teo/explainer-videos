from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

KICK = "#F2A65A"
KEEP = "#7EC8F5"


class Mixed(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Mixed strategies: \ the penalty kick", r"Why would a rational player choose at random?",
             "Chapter five. Mixed strategies: the penalty kick.", lit={2003: r"Palacios-Huerta's penalties"},
             scale=("person",), horizon=("a day",))
        self.idea()
        self.kick()
        self.test()

    def idea(self):
        head = label(r"a game with no equilibrium in pure strategies", font_size=32, color=E.ACCENT).to_edge(UP,
                                                                                                         buff=0.5)
        rows = VGroup(
            label(r"a penalty: \ the kicker aims left or right; \ the goalkeeper dives left or right", font_size=25),
            label(r"if the keeper always dives left, \ kick right; \ if the kicker always kicks right, \ dive right",
                  font_size=24, color=GREY_A),
            label(r"any predictable choice can be exploited", font_size=26, color=DEFECT),
            label(r"so randomize, \ in proportions that leave the other side indifferent", font_size=26, color=EQ),
            label(r"the indifference principle: \ each player's mix is chosen to make \emph{the other} indifferent",
                  font_size=24, color=LEVEL),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Some games have no equilibrium at all in which players simply choose. <bookmark mark='a'/> Take a "
            "penalty kick. The kicker aims left or right; the goalkeeper must dive before seeing the ball. "
            "<bookmark mark='b'/> If the keeper always dives left, the kicker should aim right; if the kicker always "
            "aims right, the keeper should dive right; and so round in a circle. <bookmark mark='c'/> Any "
            "predictable choice can be exploited. <bookmark mark='d'/> So each side randomizes, in proportions that "
            "leave the other side with nothing to exploit. <bookmark mark='e'/> This is the indifference principle, "
            "and its twist: each player's mixture is set to make the other player indifferent between their options, "
            "not to suit the player's own payoffs."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def kick(self):
        p = load("penalty")
        S = np.array(p["S"])
        mat = matrix(100 * S, 100 * (1 - S), [r"kick left", r"kick right"], [r"dive left", r"dive right"],
                     row_name=r"kicker", col_name=r"keeper", cell_w=2.1, cell_h=0.95, font_size=26, row_color=KICK,
                     col_color=KEEP).shift(LEFT * 3.0 + UP * 0.6)
        note_ = label(r"percent: \ the kicker scores, \ the keeper saves", font_size=18, color=GREY_B).next_to(
            mat, DOWN, buff=0.25)
        side = VGroup(
            label(r"kicking to the natural side is more accurate, \\ so a goal is likelier when the keeper "
                  r"guesses wrong there", font_size=21),
            label(rf"in equilibrium the kicker aims left {100 * p['kick_left']:.0f}\% of the time", font_size=22,
                  color=KICK),
            label(rf"and the keeper dives left {100 * p['dive_left']:.0f}\% of the time", font_size=22, color=KEEP),
            label(rf"then the kicker scores {100 * p['value']:.1f}\% whichever way the ball goes, \\ and "
                  r"whichever way the keeper dives", font_size=22, color=EQ),
            label(r"the testable prediction: \ equal success rates on both sides", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = illustrative_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is a penalty in numbers. <bookmark mark='a'/> The table gives the kicker's chance of scoring for "
            "each combination of aim and dive. Aiming to the natural side is more accurate, so a goal is likelier "
            "when the keeper goes the wrong way there. <bookmark mark='b'/> Solving the indifference conditions, the "
            "kicker aims left thirty-eight percent of the time, <bookmark mark='c'/> and the keeper dives left "
            "forty-two percent of the time. <bookmark mark='d'/> At those mixtures the kicker scores seventy-nine and "
            "a half percent whichever way the ball goes, and the keeper concedes the same whichever way the dive goes. "
            "<bookmark mark='e'/> That is the prediction that can be tested on real football: if players are "
            "mixing as the theory says, success rates should be the same on both sides."
        ) as vo:
            self.play(FadeIn(mat), FadeIn(note_), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            for mk, r in zip("bcde", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def test(self):
        cards = VGroup(
            history_card(2002, r"Chiappori, Levitt and Groseclose", r"penalty kicks in the French and Italian first "
                         r"divisions: \ the aggregate predictions hold", color=KICK, width=5.8, font_size=21),
            history_card(2003, r"Ignacio Palacios-Huerta", r"1{,}417 penalty kicks in professional football: \ "
                         r"scoring rates equal across sides, \ and choices unpredictable from one kick to the next",
                         color=KEEP, width=5.8, font_size=21),
        ).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"professional players, \ with money and careers at stake, \ mix as the theory says", font_size=24,
                  color=EQ),
            label(r"tennis serves at Wimbledon too (Walker and Wooders, 2001)", font_size=23, color=GREY_A),
            label(r"laboratory subjects usually don't: \ they alternate too much, \ and are predictable", font_size=24,
                  color=HOLD),
            label(r"mixed strategies may describe experts better than novices", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.35).next_to(cards, DOWN, buff=0.6)
        tag = published_tag(r"Chiappori, Levitt and Groseclose, AER 92(4) (2002); \ Palacios-Huerta, REStud 70(2) "
                            r"(2003); \ Walker and Wooders, AER 91(5) (2001)", corner=DR, font_size=12)
        with self.voiceover(
            "Economists have tested it. <bookmark mark='a'/> Pierre-André Chiappori, Steven Levitt and Timothy "
            "Groseclose studied penalties in the French and Italian first divisions in 2002, and found the "
            "theory's aggregate predictions held. <bookmark mark='b'/> A year later Ignacio Palacios-Huerta studied "
            "fourteen hundred and seventeen penalty kicks, and found that scoring rates were the same whichever way "
            "players went, and that a player's next choice could not be predicted from the last. "
            "<bookmark mark='c'/> Professionals, with careers at stake, mix as the theory says. "
            "<bookmark mark='d'/> So do tennis players serving at Wimbledon, Mark Walker and John Wooders found. "
            "<bookmark mark='e'/> Students in laboratories mostly don't: they switch too often, and become "
            "predictable. <bookmark mark='f'/> Mixed equilibrium may be a better description of experts than of "
            "beginners."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            for mk, r in zip("cdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
