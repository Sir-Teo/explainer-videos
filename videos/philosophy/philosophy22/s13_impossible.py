from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Impossible(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Impossible worlds", r"What if Hobbes had squared the circle?", lit=(1997, 2019),
                            part=PART)
        with self.voiceover("Chapter twelve. Impossible worlds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.coarse()
        self.counterpossibles()
        self.uses()

    def coarse(self):
        head = label(r"Intensions are too coarse", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        spots = [(-4.8, 0.9), (-2.4, 1.3), (0.0, 0.8), (2.4, 1.3), (4.8, 0.9)]
        isl = VGroup(*[island(p, w=2.0, h=1.1, seed=190 + i, color=WORLD) for i, p in enumerate(spots)])
        tags = VGroup(*[VGroup(MathTex(r"2 + 2 = 4", font_size=18, color=OK),
                               label(r"Fermat's last theorem", font_size=14, color=OK)).arrange(DOWN, buff=0.06).move_to(
            [p[0], p[1], 0]) for p in spots])
        rows = stack([(r"a proposition as a set of possible worlds: \ every necessary truth is the same set, \ "
                       r"\textit{all} of them", WHITE),
                      (r"so `$2 + 2 = 4$' and Fermat's last theorem express one proposition", BAD),
                      (r"but one can know the first and doubt the second: \ belief, \ proof and information are "
                       r"\textit{hyperintensional}", GOAL),
                      (r"and every counterfactual with an impossible antecedent is vacuously true", DESC)],
                     font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Possible worlds have a blind spot. <bookmark mark='a'/>If a proposition is the set of worlds where it "
            "is true, then every necessary truth is the same proposition: the set of all worlds. "
            "<bookmark mark='b'/>Two plus two is four holds at every world. So does Fermat's last theorem, now that "
            "Andrew Wiles has proved it. The two sentences express one proposition. <bookmark mark='c'/>Yet "
            "mathematicians knew the first for millennia while doubting the second. Knowledge, belief, proof and "
            "information distinguish things that are true at exactly the same worlds; they are hyperintensional. "
            "This was Pierre's lesson too. <bookmark mark='d'/>And on the standard semantics every counterfactual "
            "whose antecedent is impossible is true, vacuously: there are no worlds to check."
        ) as vo:
            self.play(FadeIn(head), FadeIn(isl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.15), FadeIn(rows[1]))
            for mk, r in zip("cd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def counterpossibles(self):
        d = load("cposs")
        head = label(r"Counterpossibles, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        cx = {"@": -5.95, "w1": -3.8, "i1": -1.45, "i2": 0.7, "i3": 2.85, "trivial": 5.0}
        names = {"@": r"actual", "w1": r"$w_1$", "i1": r"$i_1$", "i2": r"$i_2$", "i3": r"$i_3$",
                 "trivial": r"trivial"}
        line = Line([-2.62, 2.6, 0], [-2.62, -0.45, 0], color=GREY_C, stroke_width=2)
        ll = VGroup(label(r"possible", font_size=20, color=WORLD).move_to([-4.9, 2.55, 0]),
                    label(r"impossible", font_size=20, color=IMPW).move_to([1.8, 2.55, 0]))
        isl = VGroup()
        txt = {"square": r"squares", "care": r"cares", "2+2=4": r"$2 + 2 = 4$", "FLT": r"Fermat"}
        for k, w in enumerate(d["worlds"]):
            c = [cx[w["name"]], 0.85, 0]
            col = WORLD if w["possible"] else IMPW
            I = island(c, w=1.7, h=2.1, seed=200 + k, color=col,
                       name=names[w["name"]], font_size=18)
            facts = VGroup()
            for key in ("square", "care", "2+2=4", "FLT"):
                v = w["facts"][key]
                facts.add(label(txt[key], font_size=17, color=WHITE if v else GREY_D))
            facts.arrange(DOWN, buff=0.08).move_to(c)
            dl = label(r"distance " + str(w["distance"]), font_size=14, color=GREY_B).next_to(I.shape, DOWN,
                                                                                            buff=0.08)
            isl.add(VGroup(I, facts, dl))
        key = label(r"squares: \ Hobbes squares the circle; \ \ cares: \ the sick children care; \ \ Fermat: \ "
                    r"Fermat's last theorem; \ \ dimmed: \ false there", font_size=16, color=GREY_A).move_to(
            [0, -0.75, 0])
        hd = [r"\text{if Hobbes had squared the circle, \ldots}", r"\text{possible worlds only}",
              r"\text{with impossible worlds}"]
        rows = []
        for r in d["rows"]:
            rows.append([label(r["consequent"], font_size=18),
                         MathTex(r"\text{true (vacuously)}" if r["vacuous"] else (r"\text{true}" if r["standard"]
                                                                                  else r"\text{false}"),
                                 font_size=20, color=GOAL),
                         tf(r["impossible"])])
        grid = ValueGrid(hd, rows, col_w=[5.6, 3.2, 3.2], cell_h=0.5, font_size=18).move_to([0, -2.4, 0])
        with self.voiceover(
            "Daniel Nolan proposed taking impossible worlds seriously. <bookmark mark='a'/>The Reasoner draws six "
            "worlds as sets of sentences. Two are possible: in neither does Hobbes square the circle, which "
            "mathematics forbids. <bookmark mark='b'/>Then impossible worlds, which need not respect mathematics or "
            "even logic. In i one Hobbes squares the circle and nothing else is different; in i two he squares it and "
            "sick children in the mountains of South America care; in i three Fermat's theorem fails. And the "
            "trivial world, where everything is true. <bookmark mark='c'/>Distances follow Nolan's strangeness of "
            "impossibility: every possible world is closer to ours than any impossible one, and among the impossible, "
            "less change is closer. <bookmark mark='d'/>Now Nolan's example: if Hobbes had squared the circle, sick "
            "children in South America would have cared. With possible worlds only, there is no world where Hobbes "
            "squares the circle, so this is vacuously true, and so is its opposite. <bookmark mark='e'/>With "
            "impossible worlds, the closest world where he squares it is i one, where the children do not care. So "
            "the first counterpossible is false and the second true, as intuition says."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ll), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(isl[0]), FadeIn(isl[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(isl[k]) for k in range(2, 6)], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(*[Indicate(isl[k][2], color=GOAL) for k in range(6)])
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(grid.cell[r][c]) for r in range(2)
                                                               for c in (0, 1)])
            vo.wait_until("e")
            self.play(Indicate(isl[2], color=IMPW), *[FadeIn(grid.cell[r][2]) for r in range(2)])
        self.clear_scene()

    def uses(self):
        head = label(r"What impossible worlds are for", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"belief", r"an agent who believes $2 + 2 = 4$ need not believe every theorem: \ logical omniscience "
                        r"avoided \ (Hintikka; \ Part 12)", WORLD),
            (r"mathematics", r"`if there were a largest prime, \ multiplying them all and adding one would give a "
                             r"larger': \ reductio as a counterpossible", NAME),
            (r"logic", r"`if intuitionistic logic were correct, \ excluded middle would fail': \ true; \ `\ldots "
                       r"it would hold': \ false", CPT),
            (r"the vacuist", r"Williamson \ (2007): \ all counterpossibles are true; \ apparent falsity is pragmatics",
             GREY_A),
            (r"the price", r"which impossible worlds are there, \ and how near is each? \ Berto and Jago \ (2019)",
             IMPW),
        ]
        g = rows_table(rows, top=1.8, gap=0.45, width=8.8, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Impossible worlds have work to do. <bookmark mark='a'/>In epistemic logic, Part 12 met the problem of "
            "logical omniscience: on the standard semantics, anyone who knows anything knows all its consequences. "
            "Letting impossible worlds into an agent's space of possibilities removes that. "
            "<bookmark mark='b'/>Mathematicians reason through counterpossibles all the time: if there were a "
            "largest prime, multiplying all the primes and adding one would give a larger one. "
            "<bookmark mark='c'/>And so does the philosophy of logic: if intuitionistic logic were the correct logic, "
            "excluded middle would fail, which seems true; if it were correct, excluded middle would still hold, "
            "which seems false. If classical logic is in fact correct, both have impossible antecedents, yet they "
            "differ in truth. <bookmark mark='d'/>The vacuist, Timothy Williamson for one, holds that every counterpossible "
            "is true, and explains the appearance of falsity pragmatically. <bookmark mark='e'/>The price of the "
            "alternative is a theory of which impossible worlds there are, and how near each is. Francesco Berto and "
            "Mark Jago's book of 2019 is the current map."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
