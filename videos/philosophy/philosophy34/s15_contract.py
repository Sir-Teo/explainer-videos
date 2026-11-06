from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Contract(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"The social contract", r"What can self-interest agree to?", lit=(1986,), part=PART)
        with self.voiceover("Chapter fourteen. The social contract."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.price()
        self.contractarians()
        self.ways()

    def price(self):
        d = load("tetrad")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mus"] == [["COLL", "DOM", "PARETO", "SELF"]]
        assert sorted(d["mcs"]) == [["COLL"], ["DOM"], ["PARETO"], ["SELF"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.6, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ the dilemma")
        positions = [(("SELF",), r"other-regarding", r"Sen \ (1977); \ Fehr and Schmidt \ (1999)", None, r""),
                     (("DOM",), r"cooperate rationally", r"Gauthier \ (1986); \ Hofstadter; \ FDT", None, r""),
                     (("COLL",), r"rationality can defeat itself", r"Hobbes; \ Parfit \ (1984)", None, r"")]
        with self.voiceover(
            "Four claims about the dilemma cannot all be true. <bookmark mark='a'/>Each player chooses what is best "
            "for herself. In a one-shot dilemma, defecting is best whatever the other does. Mutual cooperation is "
            "better for both than mutual defection. And if all choose rationally, they cannot all end up worse off "
            "than they could have been. <bookmark mark='b'/>The first two make both defect; the third says that "
            "leaves both worse off; the fourth says rationality cannot do that. <bookmark mark='c'/>Deny the first: "
            "people care about others and about fairness, as Amartya Sen argued against the rational fool in 1977, "
            "and as Ernst Fehr and Klaus Schmidt modelled in 1999. <bookmark mark='d'/>Deny the second: David "
            "Gauthier's constrained maximizers, Douglas Hofstadter's superrational players and functional decision "
            "theory's twins cooperate, as rationality itself. <bookmark mark='e'/>Or accept that individual "
            "rationality can be collectively self-defeating, with Hobbes, and with Derek Parfit, who made that idea "
            "central to Reasons and Persons. Then the remedy is not a better theory of choice, but a better game. "
            "Nobody denies the third."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who, share, note) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, share=share, share_note=note, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def contractarians(self):
        head = label(r"Contract theories after game theory", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Gauthier \ (1986)", r"\textit{Morals by Agreement}: \ morality is what rational bargainers would "
                                       r"agree to, \ and keep, \ by constrained maximization", ROW),
                (r"Binmore \ (1994, \ 1998)", r"\textit{Game Theory and the Social Contract}: \ a society's morality "
                                              r"selects among the equilibria of the repeated game of life", COOP),
                (r"Skyrms \ (1996, \ 2004)", r"conventions of justice evolve, \ shaped by who meets whom", INST),
                (r"Rawls \ (1971)", r"a contract chosen behind a veil of ignorance: \ not bargaining power but fairness "
                                    r"decides: \ Part 38", HIST)]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.4)
        with self.voiceover(
            "Game theory reshaped the social contract tradition. <bookmark mark='a'/>David Gauthier's Morals by "
            "Agreement, of 1986, argued that morality is what rational bargainers would agree to, and that it is "
            "rational to be the kind of person who keeps such agreements. <bookmark mark='b'/>Ken Binmore's Game "
            "Theory and the Social Contract treats a society's morality as a way of selecting among the many "
            "equilibria of the repeated game of life. <bookmark mark='c'/>Skyrms's conventions of justice evolve, "
            "shaped by who meets whom. <bookmark mark='d'/>And John Rawls, whom Part 38 builds, asked instead what "
            "contract people would choose behind a veil of ignorance, so that fairness, not bargaining power, "
            "decides."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def ways(self):
        head = label(r"Four ways out of the dilemma, \ built in this part", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.35)
        rows = [(r"change the payoffs", r"a sovereign, \ or Ostrom's monitored sanctions: \ cooperation becomes a "
                                        r"best response", INST),
                (r"repeat the game", r"with a long enough shadow of the future, \ reciprocity is an equilibrium: \ "
                                     r"generous tit for tat and win-stay lose-shift", COOP),
                (r"correlate", r"a public signal, \ a convention or a traffic light, \ reaches outcomes no Nash "
                               r"equilibrium can", ROW),
                (r"design", r"auctions and matchings in which honesty is optimal and outcomes stable", MONEY),
                (r"what remains", r"which equilibrium, \ and whose fairness: \ the questions of ethics and justice, \ "
                                  r"Parts 35 to 39", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.4)
        with self.voiceover(
            "The part has built four ways out of Hobbes's dilemma. <bookmark mark='a'/>Change the payoffs, with a "
            "sovereign or with Ostrom's sanctions imposed by the players themselves. <bookmark mark='b'/>Repeat the "
            "game, so that reciprocity becomes an equilibrium, and forgiving strategies inherit the population. "
            "<bookmark mark='c'/>Correlate, with a convention or a signal that reaches outcomes no Nash equilibrium "
            "can. <bookmark mark='d'/>And design the rules, so that honesty is optimal and outcomes stable. "
            "<bookmark mark='e'/>What game theory cannot say is which of the many equilibria a society should "
            "choose, and whose idea of fairness should decide. Those are the questions of ethics and justice, and the "
            "next five parts take them up."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
