from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403


def rk(r):
    return r" $>$ ".join(r)


class Strategic(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Strategic voting", r"If every rule can be gamed, \ who games it, \ and what follows?",
             "Chapter five. Strategic voting.",
             lit={1951: r"Duverger", 1973: r"Gibbard", 1975: r"Satterthwaite"}, scale=("person", "nation"),
             horizon=("a year",))
        self.theorem()
        self.island()
        self.called()

    def theorem(self):
        rows = VGroup(
            label(r"Allan Gibbard, \ 1973, \ and Mark Satterthwaite, \ 1975:", font_size=25),
            label(r"with three or more options, \ every rule that picks a winner \ and is not a dictatorship", font_size=24,
                  color=RULE),
            label(r"can be manipulated: \ someone, \ somewhere, \ gains by voting against their true ranking",
                  font_size=24, color=CYCLE),
            label(r"Arrow's theorem, \ seen from the voter's side", font_size=24, color=E.ACCENT),
            label(r"part seventeen's deferred acceptance escaped it only because it isn't a vote over shared outcomes",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Gibbard, Econometrica 41(4) (1973); \ Satterthwaite, JET 10(2) (1975)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Borda's honest men are rare, and a theorem says why it matters. <bookmark mark='a'/> Allan Gibbard in "
            "1973 and Mark Satterthwaite in 1975 proved independently that <bookmark mark='b'/> with three or more "
            "options, every rule that picks a winner and is not a dictatorship <bookmark mark='c'/> can be "
            "manipulated: there is always some situation in which some voter does better by voting against their "
            "true ranking. <bookmark mark='d'/> It is Arrow's theorem seen from the voter's side. "
            "<bookmark mark='e'/> Part seventeen's deferred acceptance made honesty safe for one side only because "
            "matching is not a vote over one outcome that everyone shares."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def island(self):
        st = load("strategy")
        pick = [("plurality", st["plurality"][0], r"vote for the lesser evil"),
                ("Borda", st["Borda"][0], r"bury the front-runner"),
                ("instant runoff", st["instant runoff"][0], r"compromise early")]
        head = label(r"on the island: \ a group that agrees can change the winner", font_size=27,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        rows = VGroup()
        for rule, m, name in pick:
            rows.add(VGroup(
                label(rf"{rule}: \ {name}", font_size=28, color=RULE),
                label(rf"the {m['count']} who truly rank \ {rk(m['truth'])} \ vote \ {rk(m['lie'])}", font_size=24,
                      color=GREY_A),
                label(rf"the winner moves from {m['honest_winner']} \ ({PLAN[m['honest_winner']]}) \ to "
                      rf"{m['new_winner']} \ ({PLAN[m['new_winner']]}), \ which they prefer", font_size=24,
                      color=VOTE[m["new_winner"]]),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(head, DOWN, buff=0.55)
        foot = label(r"only the market fair, \ the Condorcet winner, \ is safe: \ no group can beat it", font_size=25,
                     color=VOTE["E"]).to_edge(DOWN, buff=0.45)
        tag = agora_tag(corner=DR, font_size=15)
        p0, b0, i0 = pick[0][1], pick[1][1], pick[2][1]
        with self.voiceover(
            "Agora checked every way each group of like-minded islanders could change its ballot. "
            f"<bookmark mark='a'/> Under plurality, the {p0['count']} fruit-first islanders, seeing the fruit trail "
            "the fish, can all vote for the boat race instead, their second choice; the boat race wins, which they "
            "prefer to the fish. That is voting for the lesser evil. "
            f"<bookmark mark='b'/> Under Borda's count, the {b0['count']} fish-first islanders can push the boat race, "
            "the leader, to the bottom of their ballots; the market fair, their second choice, wins instead. That is "
            f"called burying. <bookmark mark='c'/> Under instant runoff, the same {i0['count']} can put the market fair "
            "first; it survives the early rounds and wins, which they much prefer to the dance. "
            "<bookmark mark='d'/> Only the market fair, the Condorcet winner, cannot be beaten this way: a plan that "
            "wins every head-to-head vote leaves no group a better deal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["duverger"]
        cc = call_card(r"Maurice Duverger, \ \emph{Les partis politiques}", c.when,
                       r"plurality rule in single-member districts tends to produce two-party systems: \ voters desert "
                       r"third parties that can't win",
                       r"every American president since 1853 a Democrat or a Republican; \ but Britain, \ Canada and "
                       r"India keep third and regional parties strong where their voters are concentrated",
                       c.verdict, width=12.4, font_size=23).move_to(UP * 0.5)
        q = label(r"strategic voting in action: \ a vote for a sure loser is wasted, \ so voters and politicians move",
                  font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Duverger (1951); \ Riker, APSR 76(4) (1982)", corner=DR, font_size=13)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1951 the French political scientist Maurice Duverger argued that "
            "plurality voting in single-member districts tends to produce two parties, because voters desert third "
            "parties that cannot win, and politicians stop joining them: strategic voting, on a national scale. "
            "<bookmark mark='b'/> In the United States, every president since 1853 has been a Democrat or a "
            "Republican. But Britain, Canada and India, which also elect by plurality, keep third and regional "
            "parties in parliament, strong where their voters are concentrated. <bookmark mark='c'/> Partly right: "
            "a tendency within each district, rather than a law for the nation."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3), FadeIn(q))
        self.clear_scene()
