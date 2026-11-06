from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"In such condition there is no place for industry, \ because the fruit thereof is uncertain "
                       r"\dots\ and the life of man, \ solitary, \ poor, \ nasty, \ brutish, \ and short.",
                       r"Thomas Hobbes", r"\textit{Leviathan}, \ chapter 13 \ (1651)", width=9.4,
                       font_size=29).next_to(t, DOWN, buff=0.45)
        with self.voiceover(
            "Part 33 asked how one agent should choose. This part asks what happens when choices meet: when what is "
            "best for me depends on what you do. <bookmark mark='a'/>Thomas Hobbes, in 1651, described people "
            "without a government to keep them in awe: there is no place for industry, because its fruit is "
            "uncertain, and the life of man is solitary, poor, nasty, brutish, and short. <bookmark mark='b'/>His "
            "remedy was a sovereign. Three centuries later, game theory made his argument precise, and found both "
            "its force and its limits."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=INST, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Four questions about choosing together", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"equilibrium", r"what does it mean for choices to be stable together, \ and must such a point exist?",
             ROW),
            (r"dilemmas", r"why do rational people overgraze the commons and defect on each other?", DEFECT),
            (r"cooperation", r"how can repetition, \ evolution or correlation make cooperation stable?", COOP),
            (r"design", r"can rules be designed so that self-interest produces good outcomes: \ auctions, \ "
                        r"matching, \ the state?", INST),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Four questions run through it. <bookmark mark='a'/>What does it mean for several choices to be stable "
            "together, and must such a point always exist? <bookmark mark='b'/>Why do rational people overgraze a "
            "common pasture, and defect on each other when both would gain from trust? <bookmark mark='c'/>How can "
            "repetition, evolution or a shared signal make cooperation stable? <bookmark mark='d'/>And can the rules "
            "of the game be designed so that self-interest produces good outcomes: in auctions, in markets for "
            "school places and kidneys, and in the state itself? The prisoner's dilemma and the paradox of backward "
            "induction are this part's brick in the Wall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Nash equilibrium, \ found by support enumeration; \ best responses crossing",
            r"the dilemma and the commons, \ 1 to 100 herders; \ Ostrom's sanctions, \ simulated",
            r"the stag hunt; \ backward induction and the centipede \ (the Wall)",
            r"correlated equilibrium by linear programming; \ traffic lights",
            r"Axelrod's tournaments with noise; \ zero-determinant strategies, \ checked",
            r"evolution with rare mutations; \ Skyrms's fair division on the simplex",
            r"bargaining: \ Nash, \ Kalai--Smorodinsky, \ Rubinstein; \ the Shapley value and SHAP",
            r"auctions, \ sponsored search, \ deferred acceptance; \ the social contract and its Price List",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Nash equilibrium, found by a program that enumerates supports, and best "
            "responses crossing. <bookmark mark='b'/>The prisoner's dilemma and the commons, with up to a hundred "
            "herders, and Elinor Ostrom's sanctions simulated. <bookmark mark='c'/>The stag hunt, and backward "
            "induction in the centipede game, this part's brick in the Wall. <bookmark mark='d'/>Correlated "
            "equilibrium, found by linear programming. <bookmark mark='e'/>Axelrod's tournaments, rerun with "
            "noise, and the zero-determinant strategies discovered in 2012, checked against two thousand "
            "opponents. <bookmark mark='f'/>Evolution in a finite population, and Brian Skyrms's fair division on "
            "the simplex. <bookmark mark='g'/>Bargaining, and the Shapley value, with its use in explaining machine "
            "learning models. <bookmark mark='h'/>And mechanism design: auctions, sponsored search, the matching of "
            "students to schools, and the social contract, with its Price List."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
