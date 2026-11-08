from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy2.common import *  # noqa: F403


class Completeness(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Completeness: every validity has a proof", r"Can the rules reach every truth of "
                            r"logic?", lit=(1921, 1929), part=PART)
        with self.voiceover("Chapter eight. Completeness: every validity has a proof."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.statement()
        self.strategy()
        self.lindenbaum()
        self.compactness()

    def statement(self):
        thm = theorem_card(r"Completeness", r"if $\Gamma \models \varphi$ then $\Gamma \vdash \varphi$: every "
                           r"valid argument has a proof, using only the rules of Chapter 6", width=8.4,
                           font_size=28).move_to([0, 1.4, 0])
        hcs = VGroup(history_card(1918, r"Paul Bernays", r"propositional logic (Habilitation; published 1926)",
                                  width=4.2, color=HIST, font_size=20),
                     history_card(1921, r"Emil Post", r"propositional logic, by truth tables", width=4.2, color=HIST,
                                  font_size=20),
                     history_card(1929, r"Kurt Gödel", r"first-order logic (Part 3)", width=4.2, color=HIST,
                                  font_size=20)).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Soundness says the rules never prove too much. Completeness says they never prove too little: if a "
            "conclusion follows from the premises in every valuation, then there is a derivation of it, using only "
            "the handful of rules from Chapter six. <bookmark mark='a'/>Paul Bernays proved it for propositional "
            "logic in 1918, Emil Post in 1921 by other means, and Kurt Gödel, in 1929, for the far richer logic of "
            "Part 3."
        ) as vo:
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.2) for h in hcs], lag_ratio=0.3))
        self.clear_scene()

    def strategy(self):
        rows = [MathTex(r"\Gamma \nvdash \varphi", font_size=46),
                MathTex(r"\Gamma \cup \{\lnot\varphi\}", r"\text{ is consistent}", font_size=46),
                MathTex(r"\Gamma \cup \{\lnot\varphi\}", r"\text{ has a model}", font_size=46),
                MathTex(r"\Gamma \nvDash \varphi", font_size=46)]
        whys = [why(r"suppose there is no proof"), why(r"else $\lnot$I and $\lnot\lnot$E would prove $\varphi$"),
                why(r"the bridge: every consistent set has a model"), why(r"a valuation with $\Gamma$ true, "
                                                                          r"$\varphi$ false")]
        step = ladder(self, rows, whys, keep=4, top=2.4, x=-2.6, align_index=None, edge=6.6)
        for r in rows:
            r.set_x(-2.6)
        box = None
        with self.voiceover(
            "The proof turns the question around. <bookmark mark='a'/>Suppose the conclusion phi cannot be proved. "
            "<bookmark mark='b'/>Then adding not phi to the premises can never lead to a contradiction: if it did, "
            "negation introduction and double-negation elimination would prove phi after all. The set is "
            "consistent. <bookmark mark='c'/>So suppose we can show that every consistent set has a model, a "
            "valuation that makes all of it true. <bookmark mark='d'/>Then some valuation makes the premises true and "
            "phi false, and the argument is not valid. That is completeness, read backwards."
        ) as vo:
            step(0)
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                if k == 0:
                    self.play(Indicate(rows[0], color=CONN))
                else:
                    step(k)
                if k == 2:
                    box = SurroundingRectangle(VGroup(rows[2], whys[2]), color=GOAL, buff=0.15, corner_radius=0.08)
                    self.play(Create(box))
        with self.voiceover(
            "Consistency is a fact about proofs: no derivation of a contradiction. Having a model is a fact about "
            "truth. The whole weight of the theorem rests on the highlighted step, which builds a bridge from the "
            "first kind of fact to the second."
        ):
            self.play(Indicate(box, color=GOAL))
        self.clear_scene()

    def lindenbaum(self):
        d = load("lindenbaum")
        hc = history_card(r"c.\ 1928", r"Adolf Lindenbaum", r"every consistent set extends to a maximal one "
                          r"(lemma reported by Tarski, 1930)", width=5.0, color=HIST).to_corner(UL, buff=0.35)
        start = VGroup(label(r"start:", font_size=26, color=GREY_A),
                       *[fmath(s, font_size=34, color=ATOM) for s in d["start"]]).arrange(RIGHT, buff=0.35)
        start.next_to(hc, DOWN, buff=0.45).align_to(hc, LEFT)
        steps = d["steps"][:14]
        col = VGroup()
        for i, st in enumerate(steps):
            it = st["chose"] == "it"
            f = fmath(st["f"], font_size=28, color=GREY_A)
            arrow = MathTex(r"\Rightarrow", font_size=26, color=GREY_C)
            add = fmath(st["added"], font_size=28, color=OK if it else BAD)
            n = MathTex(rf"\varphi_{{{i + 1}}}", font_size=24, color=GREY_B)
            col.add(VGroup(n, f, arrow, add).arrange(RIGHT, buff=0.22))
        col.arrange_in_grid(rows=7, cols=2, buff=(0.7, 0.18), cell_alignment=LEFT, flow_order="dr")
        col.move_to([2.6, -0.1, 0])
        if col.get_right()[0] > 6.9:
            col.shift(LEFT * (col.get_right()[0] - 6.9))
        legend_ = VGroup(label(r"green: \ add $\varphi$", font_size=22, color=OK),
                         label(r"red: \ $\varphi$ would be inconsistent, so add $\lnot\varphi$", font_size=22,
                               color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend_.next_to(start, DOWN, buff=0.45).align_to(start, LEFT)
        v = d["valuation"]
        val = MathTex(r",\ ".join(rf"{k} = \mathrm{{{'T' if b else 'F'}}}" for k, b in v.items()), font_size=36,
                      color=P.WORLD)
        vl = label(r"the valuation it decides:", font_size=24, color=GREY_A)
        vb = VGroup(vl, val).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.5)
        note_ = note(r"consistency checked here by our solver; in the proof, by the absence of a derivation of $\bot$",
                     font_size=18).to_edge(DOWN, buff=0.15)
        first = steps[0]
        with self.voiceover(
            "The bridge is due to Adolf Lindenbaum. <bookmark mark='a'/>List every formula there is, one after "
            "another: they can be counted, like words in a dictionary. Start with a consistent set: here, p or q, and "
            "not p. <bookmark mark='b'/>Now go down the list. For each formula, add it if the set stays consistent; "
            f"otherwise, add its negation. The first is {first['f'].replace('¬', 'not ')}: "
            f"{'consistent, so it goes in' if first['chose'] == 'it' else 'that would contradict what we have, so its negation goes in'}. "
            "<bookmark mark='c'/>And so on, forever. Here are the first fourteen steps, computed."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(start))
            vo.wait_until("b")
            self.play(FadeIn(legend_), FadeIn(col[0], shift=LEFT * 0.2), FadeIn(note_))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in col[1:]], lag_ratio=0.25), run_time=4)
        with self.voiceover(
            "In the limit, the set decides every formula: it contains each one or its negation, and it is still "
            "consistent, since any contradiction would use finitely many of its members, and every finite stage is "
            "consistent. <bookmark mark='a'/>Now read off a valuation: make an atom true exactly when the set contains "
            "it. A truth lemma, proved by induction on formulas, says this valuation makes true exactly the formulas "
            "in the set. <bookmark mark='b'/>So every consistent set has a model, and completeness is proved."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(vb, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(val, color=P.WORLD))
        self.clear_scene()

    def compactness(self):
        thm = theorem_card(r"Compactness", r"if every finite subset of a set of sentences is satisfiable, the whole "
                           r"set is, \ even when the set is infinite", kind=r"Corollary", width=6.4,
                           font_size=24).to_corner(UL, buff=0.4)
        # an endless map, four-coloured: hexagons fading toward the edges (schematic)
        cols4 = [P.CLAIM, P.AGENT, P.TRUE, P.RULE]
        R = 0.36
        cells = []
        for i in range(-9, 10):
            for j in range(-6, 7):
                x = 1.5 * R * i + 3.2
                y = np.sqrt(3) * R * (j + (0.5 if i % 2 else 0)) - 0.6
                dist = np.hypot((x - 3.2) / 3.6, (y + 0.6) / 3.0)
                if dist <= 1.15:
                    cells.append((x, y, dist))
        colour = []
        for k, (x, y, _) in enumerate(cells):  # greedy: the first colour no neighbour uses
            used = {colour[m] for m, (x2, y2, _) in enumerate(cells[:k]) if np.hypot(x - x2, y - y2) < 1.05 * np.sqrt(3) * R}
            colour.append(min(c for c in range(4) if c not in used))
        for k, (x, y, _) in enumerate(cells):
            for m, (x2, y2, _) in enumerate(cells):
                if m != k and np.hypot(x - x2, y - y2) < 1.05 * np.sqrt(3) * R:
                    assert colour[m] != colour[k]
        hexes = VGroup()
        for (x, y, dist), c in zip(cells, colour):
            h = RegularPolygon(6, radius=R * 0.97, stroke_width=1, stroke_color="#0E1117", fill_color=cols4[c],
                               fill_opacity=max(0.05, 0.85 - 0.75 * dist))
            hexes.add(h.move_to([x, y, 0]))
        sch = schematic_tag(corner=DR)
        hc = history_card(1951, r"de Bruijn \& Erdős", r"an infinite map can be coloured with $k$ colours if every "
                          r"finite part of it can", width=5.6, color=HIST).next_to(thm, DOWN, buff=0.4).align_to(
            thm, LEFT)
        fwd = label(r"Part 3: infinitely large numbers. \ Part 7: proof and truth come apart.", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The construction has a remarkable consequence, called compactness. <bookmark mark='a'/>If every finite "
            "subset of a set of sentences can be made true, so can the whole set, even when the set is infinite. "
            "<bookmark mark='b'/>For example: an infinite map can be coloured with four colours, so that neighbours "
            "differ, as long as every finite piece of it can be. Nicolaas de Bruijn and Paul Erdős proved that in "
            "1951. One sentence per country; every finite set satisfiable; so the whole map is colourable."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h) for h in hexes], lag_ratio=0.003), FadeIn(sch), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2))
        with self.voiceover(
            "In propositional logic, then, proof and truth coincide exactly: what is valid can be proved, and what can "
            "be proved is valid. Nothing true escapes the rules. <bookmark mark='a'/>Compactness returns in Part 3, "
            "where it conjures numbers larger than every natural number, and the agreement of proof and truth breaks "
            "for good in Part 7."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(fwd))
        self.clear_scene()
