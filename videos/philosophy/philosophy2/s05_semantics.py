from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy2.common import *  # noqa: F403

UNIVERSE_YEARS = 1.38e10


class Semantics(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Valid by calculation", r"What does it mean for a conclusion to follow?",
                            lit=(1921,), part=PART)
        with self.voiceover("Chapter four. Valid by calculation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.definitions()
        self.peirce()
        self.forms()
        self.cost()

    def definitions(self):
        cards = VGroup(
            definition_card(r"Valuation", r"an assignment of T or F to every atom", width=5.6, font_size=24,
                            color=ATOM),
            definition_card(r"Tautology", r"true under every valuation", width=5.6, font_size=24, color=OK),
            definition_card(r"Satisfiable", r"true under at least one valuation", width=5.6, font_size=24,
                            color=P.WORLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.5)
        ent = MathTex(r"\Gamma", r"\models", r"\varphi", font_size=72).move_to([3.4, 1.4, 0])
        ent[0].set_color(ATOM)
        ent[2].set_color(GOAL)
        ent_d = wrapped_label(r"every valuation that makes all of $\Gamma$ true makes $\varphi$ true", 5.8, 28,
                              GREY_A).next_to(ent, DOWN, buff=0.35)
        val = label(r"valid argument $=$ truth preserved in every case", font_size=30, color=OK)
        val.next_to(ent_d, DOWN, buff=0.6)
        with self.voiceover(
            "Now the definitions everything else rests on. <bookmark mark='a'/>A valuation assigns true or false to "
            "every atom: one way the world might be, as far as these sentences can tell. <bookmark mark='b'/>A formula "
            "is a tautology if it comes out true under every valuation, <bookmark mark='c'/>and satisfiable if it "
            "comes out true under at least one. <bookmark mark='d'/>And a set of premises, gamma, entails a conclusion, "
            "written with this double turnstile, if every valuation that makes all the premises true also makes the "
            "conclusion true. <bookmark mark='e'/>That is what validity is: truth preserved, in every case there is."
        ) as vo:
            self.play(FadeIn(cards[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(Write(ent), FadeIn(ent_d))
            vo.wait_until("e")
            self.play(FadeIn(val, shift=UP * 0.15))
        self.clear_scene()

    def peirce(self):
        d = load("tables")
        assert d["peirce"]["tautology"]
        f = "((p -> q) -> p) -> p"
        tt = TruthTable([c for c in d["peirce"]["cols"]], names=["p", "q"], font_size=34, highlight_col=2)
        tt.scale(1.15).move_to([0, -0.4, 0])
        title = fmath(f, font_size=48, color=GOAL).to_edge(UP, buff=0.45)
        q = label(r"a tautology?", font_size=30, color=GREY_A).next_to(title, DOWN, buff=0.2)
        last = len(tt.head) - 1
        box = SurroundingRectangle(tt.column(last), buff=0.12, color=OK, stroke_width=3, corner_radius=0.08)
        with self.voiceover(
            "Is Peirce's law, if 'if p then q' implies p, then p, a tautology? Most people have no intuition about "
            "it at all. <bookmark mark='a'/>So calculate. One column for each atom, <bookmark mark='b'/>then one for "
            "each subformula, from the inside out. <bookmark mark='c'/>Every row of the last column is true. A "
            "tautology. Though, as we will see in Chapter six, a strange one: there are logicians who refuse to "
            "accept it."
        ) as vo:
            self.play(Write(title), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(tt.head[:2]), FadeIn(tt.rule), FadeIn(tt.sep), FadeIn(tt.rows_bg),
                      tt.reveal_column(0), tt.reveal_column(1))
            vo.wait_until("b")
            for c in range(2, last + 1):
                self.play(FadeIn(tt.head[c]), tt.reveal_column(c), run_time=1.1)
            vo.wait_until("c")
            self.play(Create(box))
        self.clear_scene()

    def forms(self):
        d = load("tables")["forms"]
        order = ["modus ponens", "modus tollens", "disjunctive syllogism", "hypothetical syllogism",
                 "affirming the consequent", "denying the antecedent"]
        maps = VGroup()
        for k in order:
            am = ArgumentMap(d[k]["premises"], d[k]["conclusion"], width=3.2, font_size=30)
            assert am.valid == d[k]["valid"]
            nm = label(k, font_size=22, color=GREY_A).next_to(am, UP, buff=0.2)
            g = VGroup(nm, am)
            g.am = am
            maps.add(g)
        maps.arrange_in_grid(rows=2, cols=3, buff=(0.9, 1.05)).move_to([0, 0.15, 0])
        verdicts = []
        for g in maps:
            v = g.am.verdict(font_size=22)
            v.next_to(g.am.conclusion, DOWN, buff=0.25).align_to(g.am, LEFT)
            verdicts.append(v)
        ac = d["affirming the consequent"]["countermodel"]
        story = label(r"if it rained, the streets are wet; \ the streets are wet; \ so it rained?", font_size=26,
                      color=GREY_A).to_edge(DOWN, buff=0.35)
        assert ac == {"p": False, "q": True}
        with self.voiceover(
            "Arguments are checked the same way. <bookmark mark='a'/>Modus ponens: in every row where both premises "
            "are true, so is the conclusion. Valid. <bookmark mark='b'/>Modus tollens, the disjunctive syllogism, the "
            "chain of two conditionals: valid, valid, valid."
        ) as vo:
            self.play(FadeIn(maps[0]))
            vo.wait_until("a")
            self.play(FadeIn(verdicts[0], scale=1.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(maps[i]) for i in (1, 2, 3)], lag_ratio=0.3))
            self.play(LaggedStart(*[FadeIn(verdicts[i], scale=1.2) for i in (1, 2, 3)], lag_ratio=0.3))
        with self.voiceover(
            "Now a famous mistake, affirming the consequent. <bookmark mark='a'/>If it rained, the streets are wet; "
            "the streets are wet; so it rained. <bookmark mark='b'/>The table finds the row that refutes it: p false "
            "and q true. No rain, wet streets: somebody ran a sprinkler. That row is a countermodel, and one "
            "countermodel is all it takes. <bookmark mark='c'/>Denying the antecedent fails in the same row."
        ) as vo:
            self.play(FadeIn(maps[4]))
            vo.wait_until("a")
            self.play(FadeIn(story))
            vo.wait_until("b")
            self.play(FadeIn(verdicts[4], scale=1.2))
            vo.wait_until("c")
            self.play(FadeIn(maps[5]), FadeIn(verdicts[5], scale=1.2))
        self.clear_scene()

    def cost(self):
        d = load("tables")
        hcs = VGroup(history_card(1921, r"Emil Post", r"truth tables decide every question of propositional "
                                  r"validity; the calculus is complete", width=5.2, color=HIST),
                     history_card(1921, r"Ludwig Wittgenstein", r"\textit{Tractatus}: truth tables, and "
                                  r"tautologies that `say nothing'", width=5.2, color=HIST))
        hcs.arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        dp = label(r"a decision procedure: \ always halts, always right", font_size=30, color=OK)
        dp.move_to([0, -0.6, 0])
        cost = [c for c in d["cost"] if c["n"] in (20, 30, 40, 60, 80, 100)]
        logy = [np.log10(max(c["seconds"], 1e-3)) for c in cost]
        G = axes([0, len(cost)], [-3, 22], x_length=6.0, y_length=4.4, yticks=[0, 6, 12, 18],
                 yfmt=lambda v: f"10^{{{int(v)}}}", ylabel=r"seconds, at a billion rows a second",
                 center=[-2.9, -0.9, 0])
        ax = G.ax
        bars = VGroup()
        for i, (c, ly) in enumerate(zip(cost, logy)):
            h = ax.c2p(i + 0.5, ly)[1] - ax.c2p(i + 0.5, -3)[1]
            b = Rectangle(width=0.7, height=max(h, 0.02), stroke_width=0, fill_color=BAD if c["years"] > 1 else OK,
                          fill_opacity=0.8).move_to(ax.c2p(i + 0.5, -3), aligned_edge=DOWN)
            bars.add(b)
            G.add(MathTex(rf"{c['n']}", font_size=24, color=GREY_B).next_to(ax.c2p(i + 0.5, -3), DOWN, buff=0.12))
        xl = label(r"atoms", font_size=22, color=GREY_A).next_to(G, DOWN, buff=0.1)
        univ = np.log10(UNIVERSE_YEARS * 3.15576e7)
        uline = DashedLine(ax.c2p(0, univ), ax.c2p(len(cost), univ), color=P.CONCL, stroke_width=2)
        ul = label(r"age of the universe", font_size=22, color=P.CONCL).next_to(uline, UP, buff=0.08).align_to(
            uline, LEFT)
        n60 = next(c for c in d["cost"] if c["n"] == 60)
        n100 = next(c for c in d["cost"] if c["n"] == 100)
        ratio = n100["years"] / UNIVERSE_YEARS
        rate = d["python_rows_per_second"]
        notes = VGroup(MathTex(rf"30:\ \ 1\text{{ s}}", font_size=30),
                       MathTex(rf"60:\ \ {n60['years']:.0f}\text{{ years}}", font_size=30),
                       MathTex(rf"100:\ \ {ratio:,.0f}\times\text{{ the age of the universe}}".replace(",", "{,}"),
                               font_size=30, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        notes.to_edge(RIGHT, buff=0.4).set_y(0.4)
        meas = label(rf"our table-filler (Python): {rate:,.0f} rows a second", font_size=22, color=GREY_A)
        meas.to_corner(DR, buff=0.3)
        with self.voiceover(
            "So propositional logic is decidable. There is a mechanical procedure that answers every question of "
            "validity, yes or no, and always halts. <bookmark mark='a'/>Emil Post used truth tables this way in his "
            "thesis of 1921, and Wittgenstein's Tractatus used them the same year. <bookmark mark='b'/>For this part "
            "of reasoning, Leibniz's dream is literally true: anyone can calculate, and everyone gets the same answer."
        ) as vo:
            self.play(FadeIn(dp))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in hcs], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Indicate(dp, color=OK))
        self.play(FadeOut(hcs), FadeOut(dp))
        with self.voiceover(
            "Literally true, and ruinously expensive. A table needs one row for every valuation: two to the n rows "
            "for n atoms. <bookmark mark='a'/>Thirty atoms, about a billion rows: one second, for a machine checking a "
            f"billion rows a second. <bookmark mark='b'/>Sixty atoms: {n60['years']:.0f} years. <bookmark mark='c'/>A "
            f"hundred atoms: {ratio:,.0f} times the age of the universe. <bookmark mark='d'/>Our own table-filler, in "
            f"plain Python, manages about {rate:,.0f} rows a second. Real problems have millions of atoms. Brute force "
            "will not do, and the rest of this part is about doing better."
        ) as vo:
            self.play(FadeIn(G), FadeIn(xl))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], DOWN), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2], DOWN), GrowFromEdge(bars[3], DOWN), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(uline), FadeIn(ul), GrowFromEdge(bars[4], DOWN), GrowFromEdge(bars[5], DOWN),
                      FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(meas))
        self.clear_scene()
