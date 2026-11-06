from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Condorcet(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Condorcet's paradox", r"Can a majority be irrational when no voter is?", lit=(1785,), part=PART)
        with self.voiceover("Chapter one. Condorcet's paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.paradox()
        self.history()
        self.probability()
        self.evidence()

    def paradox(self):
        d = load("paradox")
        assert d["cycle"] == ["A", "B", "C"] and d["winner"] is None
        assert (d["pairwise"]["AB"], d["pairwise"]["BC"], d["pairwise"]["CA"]) == (2, 2, 2)
        head = label(r"Three voters, \ no majority winner \ (Condorcet, \ 1785)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        bal = VGroup(*[ballot(r, font_size=22) for _, r in d["profile"]]).arrange(RIGHT, buff=0.45)
        names = VGroup(*[label(rf"voter {i + 1}", font_size=18, color=GREY_A) for i in range(3)])
        for nm, b in zip(names, bal):
            nm.next_to(b, UP, buff=0.18)
        left = VGroup(bal, names).move_to([-4.0, 0.2, 0])
        pos = {"A": np.array([2.6, 1.6, 0]), "B": np.array([4.9, -1.7, 0]), "C": np.array([0.3, -1.7, 0])}
        nodes = {k: VGroup(Circle(radius=0.42, color=ALT[k], fill_opacity=0.2, stroke_width=3).move_to(pos[k]),
                           label(k, font_size=30).move_to(pos[k])) for k in pos}

        def arrow(a, b):
            s, e = pos[a], pos[b]
            u = (e - s) / np.linalg.norm(e - s)
            return Arrow(s + u * 0.48, e - u * 0.48, buff=0, color=CYC, stroke_width=6,
                         max_tip_length_to_length_ratio=0.1)

        arrows = [arrow("A", "B"), arrow("B", "C"), arrow("C", "A")]
        tags = []
        for (a, b), ar, side in zip((("A", "B"), ("B", "C"), ("C", "A")), arrows, (RIGHT, DOWN, LEFT)):
            t = label(rf"{a} beats {b}, \ 2 to 1", font_size=19, color=CYC)
            t.next_to(ar.get_center(), side, buff=0.35)
            tags.append(t)
        foot = stack([(r"each voter is transitive; \ the majority is not", BAD),
                      (r"the three ballots are one ranking, \ rotated", GREY_A)], font_size=22,
                     buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1785 the Marquis de Condorcet found the problem at the heart of this part. <bookmark mark='a'/>Three "
            "voters rank three candidates. The first ranks A, then B, then C; the second B, C, A; the third C, A, B. "
            "Each voter is perfectly consistent. <bookmark mark='b'/>Now take majorities, pair by pair. A beats B, "
            "two votes to one. <bookmark mark='c'/>B beats C, two to one. <bookmark mark='d'/>And C beats A, two to "
            "one. <bookmark mark='e'/>The majority prefers A to B, B to C, and C to A: a cycle. Every candidate loses "
            "to another, so there is no majority winner, and no majority ranking. The three ballots are a single "
            "ranking, rotated, and the symmetry is the problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(n, b)) for n, b in zip(names, bal)], lag_ratio=0.3))
            self.play(*[FadeIn(nodes[k]) for k in pos])
            for mk, i in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(GrowArrow(arrows[i]), FadeIn(tags[i]))
            vo.wait_until("e")
            self.play(FadeIn(foot), *[Indicate(a, color=BAD, scale_factor=1.05) for a in arrows])
        self.clear_scene()

    def probability(self):
        d = load("probs")
        assert d["limit"] == 0.08774 and d["exact"][0] == {"n": 3, "p": 0.05556}
        assert [s["m"] for s in d["simulated"]] == [3, 4, 5, 6, 7]
        head = label(r"How often is there no winner?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 32, 5], y_range=[0, 0.1, 0.02], x_length=6.0, y_length=3.6,
                  axis_config={"color": GREY_B, "include_tip": False, "font_size": 18},
                  x_axis_config={"numbers_to_include": [5, 10, 15, 20, 25, 30]},
                  y_axis_config={"numbers_to_include": [0.02, 0.04, 0.06, 0.08, 0.1],
                                 "decimal_number_config": {"num_decimal_places": 2}}).move_to([-3.3, -0.2, 0])
        xl = label(r"voters", font_size=18, color=VOTE).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"P(no Condorcet winner), \ 3 candidates", font_size=18, color=CYC).next_to(ax, UP, buff=0.1)
        yl.align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(e["n"], e["p"]), radius=0.06, color=CYC) for e in d["exact"]])
        vals = VGroup(*[label(f"{e['p'] * 100:.1f}\\%", font_size=14, color=GREY_A).next_to(dt, DOWN, buff=0.1)
                        for e, dt in zip(d["exact"], dots) if e["n"] in (3, 5, 11, 31)])
        lim = DashedLine(ax.c2p(0, d["limit"]), ax.c2p(32, d["limit"]), color=GOAL, stroke_width=2.5)
        limtx = label(r"Guilbaud \ (1952): \ $\tfrac14 - \tfrac{3}{2\pi}\arcsin\tfrac13 \approx 8.77\%$",
                      font_size=19, color=GOAL).next_to(ax, DOWN, buff=0.75).align_to(ax, LEFT)
        bars = VGroup()
        bx0, by0, bw, scale = 1.6, -2.0, 0.7, 9.0
        for i, s in enumerate(d["simulated"]):
            r = Rectangle(width=bw, height=s["p"] * scale, stroke_width=1, stroke_color=CYC, fill_color=CYC,
                          fill_opacity=0.55)
            r.move_to([bx0 + i * (bw + 0.25) + bw / 2, by0 + s["p"] * scale / 2, 0])
            bars.add(VGroup(r, label(f"{s['p'] * 100:.0f}\\%", font_size=16, color=WHITE).next_to(r, UP, buff=0.08),
                            label(str(s["m"]), font_size=18, color=GREY_A).next_to(r, DOWN, buff=0.12)))
        base = Line([bx0 - 0.1, by0, 0], [bx0 + 5 * (bw + 0.25), by0, 0], color=GREY_B, stroke_width=1.5)
        btx = label(r"candidates \ (101 voters, \ 20,000 simulated elections each)", font_size=17,
                    color=GREY_A).next_to(base, DOWN, buff=0.55)
        bhead = label(r"more candidates, \ more cycles", font_size=20, color=CYC).move_to([3.95, 2.3, 0])
        with self.voiceover(
            "Is the cycle a curiosity? Suppose every voter picks one of the six possible rankings at random, the "
            "model called impartial culture. <bookmark mark='a'/>The Reasoner adds up the exact probability, over "
            "every way the votes could fall, that there is no Condorcet winner: one in eighteen with three voters, "
            "about seven percent with five, eight and a half percent with thirty one. <bookmark mark='b'/>As the "
            "electorate grows, the probability tends to a limit that Georges-Théodule Guilbaud found in 1952: a "
            "quarter, minus three over two pi times the arcsine of a third, about eight point eight percent. "
            "<bookmark mark='c'/>With more candidates, cycles become common: simulating twenty thousand elections of "
            "a hundred and one voters, seventeen percent have no winner with four candidates, and thirty seven "
            "percent with seven. Real electorates are far less random than impartial culture, and cycles in real "
            "elections are rare; but they are always possible."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.15), FadeIn(vals))
            vo.wait_until("b")
            self.play(Create(lim), FadeIn(limtx))
            vo.wait_until("c")
            self.play(FadeIn(bhead), Create(base), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2), FadeIn(btx))
        self.clear_scene()

    def history(self):
        head = label(r"Before and after Condorcet", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Llull \ (1299)", r"\textit{De arte eleccionis}: \ elect by comparing every pair of candidates", HIST),
                (r"Cusanus \ (1433)", r"rank all candidates and add up points: \ the Borda count, \ three centuries early", SCORE),
                (r"Borda \ (1770)", r"to the Academy of Sciences: \ plurality can elect a candidate a majority ranks last", SCORE),
                (r"Condorcet \ (1785)", r"\textit{Essai}: \ elect the candidate who beats every other head to head, \ if there is one", MAJ),
                (r"Dodgson \ (1876)", r"Lewis Carroll rediscovers the cycle, \ and proposes the fewest swaps to a winner", CYC)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The question is older than Condorcet. <bookmark mark='a'/>The Catalan philosopher Ramon Llull, in 1299, "
            "proposed electing by comparing every pair of candidates, the method Condorcet would champion. <bookmark "
            "mark='b'/>Nicholas of Cusa, in 1433, proposed ranking all candidates and adding up points, the method "
            "that bears Borda's name. <bookmark mark='c'/>Jean-Charles de Borda told the French Academy of Sciences "
            "in 1770 that plurality voting can elect a candidate whom a majority ranks last. <bookmark "
            "mark='d'/>Condorcet's Essay of 1785 proposed electing the candidate who beats every other head to head, "
            "if there is one, and found that sometimes there is none. <bookmark mark='e'/>A century later the Oxford "
            "mathematician Charles Dodgson, better known as Lewis Carroll, rediscovered the cycle and proposed "
            "electing whoever needs the fewest swaps on ballots to become a Condorcet winner."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def evidence(self):
        head = label(r"Do cycles happen?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Riker \ (1982)", r"claimed cycles in history: \ the Powell amendment \ (1956), \ the Seventeenth Amendment", CYC),
                (r"G. Mackie \ (2003)", r"\textit{Democracy Defended}: \ most of Riker's cycles do not survive scrutiny", MAJ),
                (r"Regenwetter et al. \ (2006)", r"\textit{Behavioral Social Choice}: \ in survey and election data, \ majority cycles are rare", TRUTH),
                (r"why", r"real preferences are correlated, \ often along one dimension: \ far from impartial culture", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Do cycles happen in real votes? <bookmark mark='a'/>William Riker claimed several, including the defeat "
            "of a school construction bill in the United States House in 1956, after an amendment by Adam Clayton "
            "Powell. <bookmark mark='b'/>Gerry Mackie's Democracy Defended, of 2003, re-examined Riker's cases and "
            "argued that most do not survive scrutiny. <bookmark mark='c'/>Michel Regenwetter and colleagues' "
            "Behavioral Social Choice, of 2006, found majority cycles rare in survey and election data. <bookmark "
            "mark='d'/>The reason is that real preferences are correlated, often along a single dimension, which is "
            "far from impartial culture, as chapter seven explains."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
