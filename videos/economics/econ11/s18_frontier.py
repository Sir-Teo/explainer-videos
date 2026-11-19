from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

RPS = ("#F2A65A", "#7BD88F", "#C9A0FF")


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ learning to play at scale", r"Can machines find equilibria of games too large for "
             r"any person to solve?", "Chapter sixteen. Frontier: learning to play at scale.",
             lit={2017: r"Libratus"}, scale=("person", "world"))
        self.regret()
        self.poker()
        self.people()

    def regret(self):
        r = load("regret")
        avg = np.array(r["rps_row"])
        steps = np.arange(1, len(avg) + 1) * (20000 // len(avg))
        ax = plane([1.5, 4.4], [0, 0.7], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[2, 3, 4], yticks=[0, 1 / 3, 0.5, 0.7], xlabel=r"rounds played",
                   ylabel=r"average strategy", font_size=16,
                   xfmt=lambda v: {2: "100", 3: "1{,}000", 4: "10{,}000"}.get(int(round(v)), ""),
                   yfmt=lambda v: {0: "0", 1 / 3: "1/3", 0.5: "1/2", 0.7: ""}.get(v, f"{v:.1f}"))
        lines = VGroup(*[path(ax, np.log10(steps), avg[:, k], color=RPS[k], width=3, smooth=False, xr=(1.5, 4.4))
                         for k in range(3)])
        third = DashedLine(ax.ax.c2p(1.5, 1 / 3), ax.ax.c2p(4.4, 1 / 3), color=GREY_B, stroke_width=1.5)
        names = VGroup(*[label(n, font_size=17, color=c) for n, c in zip((r"rock", r"paper", r"scissors"), RPS)]
                       ).arrange(RIGHT, buff=0.3).next_to(ax, UP, buff=0.1)
        side = VGroup(
            label(r"regret: \ how much better you would have done \\ by always playing one move", font_size=21),
            label(r"regret matching (Hart and Mas-Colell, 2000): \\ play each move in proportion \\ to its positive "
                  r"regret so far", font_size=21, color=EQ),
            label(rf"Agora, \ rock-paper-scissors against itself: \\ the average strategy tends to a third each; \\ "
                  rf"regret per round after 20{{,}}000 rounds: \ {r['rps_regret']:.3f}", font_size=20, color=LEVEL),
            label(r"in any game, \ average play approaches \\ the correlated equilibria; \\ in zero-sum games, \ Nash's",
                  font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The frontier of this part is computational: how to find equilibria of games far too large to solve by "
            "hand. Much of the answer is a learning rule. <bookmark mark='a'/> Your regret for a move is how much "
            "better you would have done, so far, by always playing it. <bookmark mark='b'/> In Sergiu Hart and "
            "Andreu Mas-Colell's regret matching, published in 2000, you play each move with probability "
            "proportional to its positive regret. <bookmark mark='c'/> Agora runs it on rock, paper, scissors "
            "against itself: the average strategy wanders and then settles at a third each, and after twenty "
            "thousand rounds the regret per round is under a hundredth. <bookmark mark='d'/> In any game, average "
            "play under regret matching approaches the set of correlated equilibria of chapter ten; in two-player "
            "zero-sum games, Nash equilibrium itself."
        ) as vo:
            self.play(FadeIn(ax), Create(third), FadeIn(names), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), FadeIn(side[2]), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def poker(self):
        cards = VGroup(
            history_card(2015, r"Bowling, \ Burch, \ Johanson and Tammelin", r"heads-up limit Texas hold'em, \ "
                         r"essentially solved: \ a variant of regret minimization, \ CFR+", color=EQ, width=5.8,
                         font_size=21),
            history_card(2017, r"Brown and Sandholm's Libratus", r"heads-up no-limit hold'em: \ beat four top "
                         r"professionals over 120{,}000 hands, \ in Pittsburgh in January", color=LEVEL, width=5.8,
                         font_size=21),
        ).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"poker is a game of incomplete information, \ like chapter 13: \ each player hides their cards",
                  font_size=23),
            label(r"its game tree is astronomically large; \ no one can write the equilibrium down", font_size=23,
                  color=GREY_A),
            label(r"self-play with regret minimization finds approximate equilibria \\ that bluff, \ and that can't "
                  r"be exploited much", font_size=23, color=EQ),
            label(r"in 2019 the same team's Pluribus beat professionals at six-player no-limit", font_size=23,
                  color=LEVEL),
            label(r"how the algorithms work: \ \emph{AI, Built}", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(cards, DOWN, buff=0.5)
        tag = published_tag(r"Bowling et al., Science 347 (2015); \ Brown and Sandholm, Science 359 (2018), 365 (2019)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Scaled up, regret minimization has solved games no person could. <bookmark mark='a'/> Poker is a game "
            "of incomplete information, like chapter thirteen's: each player hides their cards. "
            "<bookmark mark='b'/> Its game tree is astronomically large, so no one can write its equilibrium down. "
            "<bookmark mark='c'/> In 2015 Michael Bowling, Neil Burch, Michael Johanson and Oskari Tammelin "
            "announced that heads-up limit Texas hold'em was essentially solved, by a regret-minimization algorithm "
            "called CFR plus. In January 2017 Noam Brown and Tuomas Sandholm's program Libratus beat four top "
            "professionals at the much larger no-limit game, over a hundred and twenty thousand hands. "
            "<bookmark mark='d'/> The strategies found by self-play bluff, and can't be exploited by much, which is "
            "what an equilibrium promises. <bookmark mark='e'/> In 2019 the same team's Pluribus beat professionals "
            "at six-player poker. <bookmark mark='f'/> How these algorithms work is told in AI, Built."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]), FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=UP * 0.2), Indicate(cards[0], scale_factor=1.02))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
            vo.wait_until("f")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def people(self):
        head = label(r"open questions", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"do people learn like this? \ reinforcement (Erev and Roth, 1998) \ and experience-weighted "
                  r"attraction \\ (Camerer and Ho, 1999) \ fit laboratory play better than equilibrium does",
                  font_size=22),
            label(r"when algorithms play each other in real markets, \ which equilibrium do they find? \ (Parts 10, "
                  r"12, 44)", font_size=23, color=HOLD),
            label(r"computing equilibria is hard in general (Part 9's PPAD); \ learning finds coarser ones quickly",
                  font_size=23, color=GREY_A),
            label(r"designing games for learning players: \ markets and auctions that work \\ even when nobody "
                  r"computes an equilibrium (Parts 16 and 17)", font_size=23, color=EQ),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        tag = published_tag(r"Erev and Roth, AER 88(4) (1998); \ Camerer and Ho, Econometrica 67(4) (1999)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Open questions follow. <bookmark mark='a'/> Do people learn like this? Models of reinforcement, by Ido "
            "Erev and Alvin Roth, and Camerer and Ho's experience-weighted attraction, fit how laboratory subjects "
            "learn better than equilibrium predicts their play. <bookmark mark='b'/> When pricing algorithms play "
            "each other in real markets, which equilibrium do they find? Part ten met the worry, and Parts twelve and "
            "forty-four return to it. <bookmark mark='c'/> Computing a Nash equilibrium is hard in general, as Part "
            "nine's frontier showed, but learning finds coarser equilibria quickly. <bookmark mark='d'/> And "
            "designers can build markets and auctions that work even when nobody computes an equilibrium at all, the "
            "subject of Parts sixteen and seventeen."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
