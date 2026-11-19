from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403


class Borda(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Borda against Condorcet, \ and the agenda", r"Points or head-to-head majorities? \ And how "
             r"much power does the person who sets the order of votes hold?", "Chapter two. Borda against Condorcet, "
             "and the agenda.", lit={1770: r"Borda", 1785: r"Condorcet", 1958: r"Black's history"},
             scale=("community", "nation"), horizon=("a day",))
        self.debate()
        self.irrelevant()
        self.agenda()

    def debate(self):
        p = load("playit")
        rows = VGroup(
            label(r"Jean-Charles de Borda, \ 1770: \ score each ballot, \ 4, 3, 2, 1, 0, \ and add", font_size=24,
                  color=VOTE["D"]),
            label(r"Condorcet: \ a plan that beats every other in a straight vote should win", font_size=24,
                  color=VOTE["E"]),
            label(r"the two disagree: \ on the island, \ Borda picks the boat race; \ the market fair beats it, \ "
                  rf"{p['pairwise']['E']['D']} to {p['pairwise']['D']['E']}", font_size=23, color=CYCLE),
            label(r"and Condorcet's rule can have no winner at all: \ the circle", font_size=24, color=GREY_A),
            label(r"Borda knew his count could be gamed; \ he is said to have answered that it was meant for honest "
                  r"men", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Borda (1781); \ Condorcet (1785); \ Black, \emph{The Theory of Committees and "
                            r"Elections} (1958)", corner=DR, font_size=13)
        with self.voiceover(
            "Two members of the French Academy of Sciences argued over this in the 1770s and 1780s. "
            "<bookmark mark='a'/> Jean-Charles de Borda proposed scoring each ballot, four points for a first place "
            "down to nothing for a last, and adding. <bookmark mark='b'/> Condorcet answered that a plan which beats "
            "every other in a straight vote ought to win. <bookmark mark='c'/> They can disagree, as they do on the "
            "island: Borda picks the boat race, but the market fair beats it, twenty to eighteen. "
            "<bookmark mark='d'/> And Condorcet's own rule can find no winner at all, when the majority goes round in "
            "a circle. <bookmark mark='e'/> Borda knew that his count could be gamed; the story is that he answered "
            "that his scheme was meant only for honest men."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def irrelevant(self):
        v = load("iia")
        a, b = v["pair"]
        bef = ballot(v["before"], 12, w=1.3, font_size=24)
        aft = ballot(v["after"], 12, w=1.3, font_size=24)
        arrow = Arrow(LEFT * 0.6, RIGHT * 0.6, color=GREY_B)
        top = VGroup(bef, arrow, aft).arrange(RIGHT, buff=0.5).move_to(LEFT * 3.4 + UP * 0.5)
        note = label(r"the 12 fish-first islanders move \\ the fruit above the boat race", font_size=20,
                     color=GREY_A).next_to(top, DOWN, buff=0.35)
        def order(rank, pts):
            out = rf"{rank[0]} {pts[rank[0]]}"
            for x, y in zip(rank, rank[1:]):
                out += (r" $=$ " if pts[x] == pts[y] else r" $>$ ") + rf"{y} {pts[y]}"
            return out

        rk = VGroup(
            label(r"Borda before: \ " + order(v["ranking_before"], v["points_before"]), font_size=23),
            label(r"after: \ " + order(v["ranking_after"], v["points_after"]), font_size=23, color=CYCLE),
            label(rf"nobody changed how they rank {a} against {b}, \\ yet society's order of {a} and {b} flipped",
                  font_size=23, color=E.ACCENT),
            label(r"Borda fails independence of irrelevant alternatives", font_size=23, color=RULE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Borda's count has a stranger flaw. <bookmark mark='a'/> Suppose the twelve islanders who put the fish "
            "first move the fruit up one place, above the boat race. <bookmark mark='b'/> Before, Borda ranked the "
            "market fair above the fruit. After, the fruit is above the market fair, and on top. "
            "<bookmark mark='c'/> Yet nobody changed how they rank the fruit against the market fair: the fish "
            "voters still put the fair above the fruit. Society's verdict on two plans moved because of "
            "how people ranked a third. <bookmark mark='d'/> The "
            "condition Borda breaks is called independence of irrelevant alternatives, and it is one of Arrow's."
        ) as vo:
            self.play(FadeIn(bef), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(aft), FadeIn(note))
            vo.wait_until("b")
            self.play(FadeIn(rk[0]), FadeIn(rk[1]))
            vo.wait_until("c")
            self.play(FadeIn(rk[2]))
            vo.wait_until("d")
            self.play(FadeIn(rk[3]))
        self.clear_scene()

    def agenda(self):
        m = load("cycle")
        head = label(r"the agenda: \ two plans meet, \ the winner meets the next", font_size=27,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        orders = [("A", "B", "C"), ("B", "C", "A"), ("C", "A", "B")]
        rows = VGroup()
        for o in orders:
            first = o[0] if m["pairwise"][o[0]][o[1]] > m["pairwise"][o[1]][o[0]] else o[1]
            final = first if m["pairwise"][first][o[2]] > m["pairwise"][o[2]][first] else o[2]
            rows.add(VGroup(
                label(rf"{o[0]} against {o[1]}: \ {first} wins", font_size=24, color=VOTE[first]),
                label(rf"then {first} against {o[2]}: \ {final} wins", font_size=24, color=VOTE[final]),
            ).arrange(RIGHT, buff=0.8))
        rows.arrange(DOWN, buff=0.45).move_to(UP * 0.4)
        foot = VGroup(
            label(r"with Condorcet's three voters, \ whichever plan is voted on last wins", font_size=25, color=CYCLE),
            label(r"so whoever sets the order of votes chooses the outcome", font_size=25, color=E.ACCENT),
            label(r"in committees and legislatures, \ agenda power is real power \ (Black, \ 1958; \ McKelvey, \ "
                  r"1976)", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"McKelvey, JET 12(3) (1976)", corner=DR, font_size=13)
        with self.voiceover(
            "Committees often avoid ranking everything at once. They vote on two options, then put the winner "
            "against the next. <bookmark mark='a'/> Use Condorcet's three voters. Put A against B first: A wins, "
            "then meets C, and C wins. <bookmark mark='b'/> Start with B against C, and A wins in the end. "
            "<bookmark mark='c'/> Start with C against A, and B wins. <bookmark mark='d'/> Whichever plan is voted on "
            "last wins. <bookmark mark='e'/> So whoever sets the order of the votes chooses the outcome, and Richard "
            "McKelvey showed in 1976 that, with more issues, a skilled agenda setter can lead a majority almost "
            "anywhere. In committees and legislatures, agenda power is real power."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]))
                self.play(FadeIn(r[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]), FadeIn(foot[2]))
        self.clear_scene()
