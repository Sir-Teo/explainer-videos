from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


class Mill(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Methods and conditions", r"Which factor made the difference?", lit=(1843, 1965),
                            part=PART)
        with self.voiceover("Chapter two. Methods and conditions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.methods()
        self.inus()
        self.selection()

    def methods(self):
        d = load("mill")
        hc = history_card(1843, r"John Stuart Mill", r"\textit{A System of Logic}, \ Book III", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        cols = ["spark", "oxygen", "fuel", "wet", "fire"]
        hd = [r"\text{case}"] + [rf"\text{{{c}}}" for c in cols]
        rows = []
        for i, c in enumerate(d["cases"]):
            rows.append([MathTex(str(i + 1), font_size=24)] + [bool(c[k]) for k in cols])
        grid = ValueGrid(hd, rows, col_w=[1.2, 1.4, 1.5, 1.2, 1.2, 1.2], cell_h=0.48, font_size=24).next_to(
            hc, DOWN, buff=0.3).set_x(-2.2)
        side = stack([(r"agreement: \ what all fire cases share", CAUSE),
                      (", \\ ".join(d["methods"]["agreement"]), CAUSE),
                      (r"difference: \ the one factor in which a fire case and a non-fire case differ", EFFECT),
                      (", \\ ".join(d["methods"]["difference"]), EFFECT),
                      (r"oxygen never varies: \ the methods cannot see it", BAD)], font_size=20, aligned_edge=LEFT,
                     width=5.0).move_to([4.4, -0.6, 0])
        with self.voiceover(
            "John Stuart Mill turned the search for causes into methods. <bookmark mark='a'/>Here are five cases, "
            "with the circumstances present in each, and whether there was a fire. <bookmark mark='b'/>The method of "
            "agreement: look for what all the cases with the effect have in common. Spark, oxygen and fuel. "
            "<bookmark mark='c'/>The method of difference: find two cases alike in everything but one circumstance, "
            "one with the effect and one without. The Reasoner finds three such pairs: they implicate the spark, "
            "the fuel, and wetness, whose presence prevents the fire. <bookmark mark='d'/>And notice what the methods "
            "cannot see. Oxygen never varies in these cases, so neither method can detect it, though there is no "
            "fire without it. Mill's methods find causes only against a background held fixed."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in
                                                                          range(len(rows))], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]), Indicate(VGroup(*[grid.cell[r][2] for r in range(len(rows))]), color=BAD))
        self.clear_scene()

    def inus(self):
        d = load("mill")
        hc = history_card(1965, r"J.\ L.\ Mackie", r"`Causes and Conditions'", width=5.4, color=HIST).to_corner(
            UL, buff=0.3)
        eq = MathTex(r"\text{fire} \iff (\text{short circuit} \wedge \text{flammable} \wedge \lnot\text{sprinkler}) "
                     r"\vee (\text{arson} \wedge \text{flammable})", font_size=28, color=WHITE).next_to(hc, DOWN,
                                                                                                buff=0.35).set_x(0)
        boxes = VGroup()
        for i, pi in enumerate(d["prime_implicants"]):
            lits = VGroup(*[label((r"no " if v == 0 else r"") + k, font_size=21,
                                  color=CAUSE if k == "short circuit" else WHITE) for k, v in pi.items()]).arrange(
                RIGHT, buff=0.35)
            b = SurroundingRectangle(lits, buff=0.18, color=EFFECT, corner_radius=0.1)
            boxes.add(VGroup(b, lits))
        boxes.arrange(RIGHT, buff=0.8).next_to(eq, DOWN, buff=0.45)
        bl = label(r"the minimal sufficient conditions, \ found by the Reasoner \ (prime implicants)", font_size=19,
                   color=EFFECT).next_to(boxes, DOWN, buff=0.15)
        inus = VGroup(*[label(t, font_size=22, color=c) for t, c in (
            (r"\textbf{I}nsufficient: \ a short circuit alone does not make a fire", CAUSE),
            (r"\textbf{N}on-redundant: \ drop it from its condition, \ and the rest are not enough", CAUSE),
            (r"part of an \textbf{U}nnecessary \ (arson would also do) \ but", EFFECT),
            (r"\textbf{S}ufficient condition", EFFECT))]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(
            bl, DOWN, buff=0.35)
        with self.voiceover(
            "J. L. Mackie asked what we mean when an investigator says a short circuit caused a house fire. "
            "<bookmark mark='a'/>Suppose a fire occurs exactly when there is a short circuit, flammable material and "
            "no working sprinkler, or else arson and flammable material. <bookmark mark='b'/>The Reasoner finds the "
            "minimal sufficient conditions: the two clusters. <bookmark mark='c'/>The short circuit is insufficient on "
            "its own; it is a non-redundant part of its cluster; that cluster is unnecessary, since arson would also "
            "do; but it is sufficient. An INUS condition. Most of what we call causes, Mackie argued, are INUS "
            "conditions, picked out against a background field."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.4), FadeIn(bl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in inus], lag_ratio=0.5), run_time=3)
        self.clear_scene()

    def selection(self):
        head = label(r"`The' cause", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the investigator", r"the short circuit: \ the abnormal condition", CAUSE),
            (r"the insurer", r"the missing sprinkler: \ a duty that was not done", BAD),
            (r"the chemist", r"oxygen: \ just as necessary, \ never mentioned", HIDDEN),
            (r"Hart and Honoré \ (1959)", r"selection follows norms, \ abnormality and responsibility", GOAL),
            (r"Mill", r"`the cause, \ philosophically speaking, \ is the sum total of the conditions'", GREY_A),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.4, x_text=-2.4)
        with self.voiceover(
            "Which INUS condition do we call the cause? <bookmark mark='a'/>The investigator names the short circuit, "
            "the abnormal event. <bookmark mark='b'/>The insurer names the missing sprinkler, a duty that was not done. "
            "<bookmark mark='c'/>The chemist could name oxygen, just as necessary, and never mentioned. "
            "<bookmark mark='d'/>H. L. A. Hart and Tony Honoré argued that our selection follows norms: what was "
            "abnormal, and who was responsible. <bookmark mark='e'/>Mill himself thought there was no principled "
            "choice: the cause, philosophically speaking, is the sum total of the conditions. Chapter ten returns to "
            "this, with a formal definition that has to decide."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
