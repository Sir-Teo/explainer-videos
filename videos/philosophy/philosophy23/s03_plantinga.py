from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Plantinga(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The modal ontological argument", r"If God is possible, \ must God exist?",
                            lit=(1078, 1974), part=PART)
        with self.voiceover("Chapter two. The modal ontological argument."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.greatness()
        self.proof()
        self.frames()
        self.mirror()

    def greatness(self):
        hc = history_card(1974, r"Alvin Plantinga", r"\textit{The Nature of Necessity}, \ chapter X", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"maximal excellence", r"omniscience, \ omnipotence and moral perfection, \ in a world", ARG),
            (r"maximal greatness", r"maximal excellence in \textit{every} world: \ necessary existence is built in",
             DIV),
            (r"Anselm, \ again", r"\textit{Proslogion} III: \ a being that cannot be thought not to exist is greater "
                                 r"\ (Malcolm, \ 1960; \ Hartshorne, \ 1962)", HIST),
            (r"the premise", r"possibly, \ maximal greatness is exemplified: \ $\Diamond \Box g$", ABS),
        ]
        g = rows_table(rows, top=1.2, gap=0.5, width=8.6, x_text=-2.2, label_size=22, text_size=22)
        with self.voiceover(
            "In the twentieth century the ontological argument was reborn in modal logic. <bookmark mark='a'/>Alvin "
            "Plantinga defined maximal excellence: omniscience, omnipotence and moral perfection, in a given world. "
            "<bookmark mark='b'/>And maximal greatness: maximal excellence in every possible world. Necessary "
            "existence is part of the concept. <bookmark mark='c'/>The idea is already in Anselm's third chapter: a "
            "being that cannot be thought not to exist is greater than one that can. Norman Malcolm and Charles "
            "Hartshorne had revived it. <bookmark mark='d'/>The only premise is that maximal greatness is possibly "
            "exemplified. Write g for a maximally excellent being exists; the premise is that possibly, necessarily, "
            "g."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def proof(self):
        head = label(r"Four lines in S5", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        steps = VGroup(
            MathTex(r"1.\quad \Diamond\, \Box\, g", font_size=36),
            MathTex(r"2.\quad \Diamond \Box g \to \Box g", font_size=36, color=ABS),
            MathTex(r"3.\quad \Box\, g", font_size=36),
            MathTex(r"4.\quad g", font_size=40, color=DIV)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(
            [-3.9, 0.2, 0])
        why = VGroup(*[label(t, font_size=19, color=GREY_A) for t in (
            r"the possibility premise", r"a theorem of S5", r"1, 2, modus ponens", r"3, and T: what must be, is")])
        for w_, st in zip(why, steps):
            w_.next_to(st, RIGHT, buff=0.4)
        pts = [np.array([2.2 + 1.7 * np.cos(a), 0.6 + 1.5 * np.sin(a), 0]) for a in np.linspace(0, 2 * PI, 6)[:-1]]
        nodes = VGroup(*[Circle(radius=0.32, color=ARG, fill_opacity=0.15).move_to(p) for p in pts])
        edges = VGroup(*[Line(pts[i], pts[j], color=GREY_D, stroke_width=1.5) for i in range(5)
                         for j in range(i + 1, 5)])
        edges.set_z_index(-1)
        gl = VGroup(*[MathTex(r"g", font_size=24, color=DIV).move_to(p) for p in pts])
        cap = label(r"in S5 every world sees every world: \ `necessary somewhere' means `true everywhere'",
                    font_size=20, color=ABS).to_edge(DOWN, buff=0.6).shift(RIGHT * 0.3)
        with self.voiceover(
            "The argument is four lines long. <bookmark mark='a'/>Possibly, necessarily, g: the premise. "
            "<bookmark mark='b'/>In S5, if it is possible that g is necessary, then g is necessary. "
            "<bookmark mark='c'/>So g is necessary. <bookmark mark='d'/>And what is necessary is actual: a maximally "
            "excellent being exists. <bookmark mark='e'/>Why does line two hold? In S5 every world is accessible from "
            "every other. If g is necessary at some world, it holds at every world that world sees, which is all of "
            "them; and from every world that world is visible. Necessary somewhere means true everywhere."
        ) as vo:
            self.play(FadeIn(head))
            for mk, st, w_ in zip("abcd", steps, why):
                vo.wait_until(mk)
                self.play(Write(st), FadeIn(w_))
            vo.wait_until("e")
            self.play(Create(edges), FadeIn(nodes))
            self.play(FadeIn(gl[0]))
            self.play(LaggedStart(*[FadeIn(x) for x in gl[1:]], lag_ratio=0.2), FadeIn(cap))
        self.clear_scene()

    def frames(self):
        d = load("plantinga")
        head = label(r"Checked on every frame with up to three worlds", font_size=30, color=CONN).to_edge(UP,
                                                                                                       buff=0.35)
        hd = [r"\text{frames}", r"\text{number}", r"\Diamond\Box g \to \Box g", r"\Diamond\Box g \to g"]
        rows = []
        for s, t in (("T", r"\text{reflexive (T)}"), ("B", r"\text{reflexive, symmetric (B)}"),
                     ("S4", r"\text{reflexive, transitive (S4)}"), ("S5", r"\text{equivalence (S5)}")):
            v = d[s]
            rows.append([MathTex(t, font_size=20), MathTex(str(v["argument"]["frames"]), font_size=22),
                         MathTex(rf"{v['argument']['valid_on']}", font_size=22,
                                 color=OK if v["argument"]["valid_on"] == v["argument"]["frames"] else BAD),
                         MathTex(rf"{v['conclusion']['valid_on']}", font_size=22,
                                 color=OK if v["conclusion"]["valid_on"] == v["conclusion"]["frames"] else BAD)])
        grid = ValueGrid(hd, rows, col_w=[4.8, 1.6, 2.8, 2.6], cell_h=0.55, font_size=20).move_to([0, 0.5, 0])
        note = label(r"numbers: \ frames on which the formula is valid", font_size=17, color=GREY_A).next_to(
            grid, DOWN, buff=0.15)
        rows2 = stack([(r"valid on every S5 frame; \ on most S4 frames it fails", OK),
                       (r"the conclusion $g$ needs only B: \ symmetry carries necessity back", ABS),
                       (r"so the argument's logic is the logic of metaphysical necessity, \ S5, \ which most "
                        r"accept", GOAL)], font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The Reasoner checks this, not with a proof but on models. <bookmark mark='a'/>It generates every "
            "reflexive frame with up to three worlds and tests the formula under every valuation. Line two holds on "
            "all eight S5 frames, and on only eight of the thirty-four S4 frames: without symmetry, a world can see a "
            "world where g is necessary while g fails elsewhere. <bookmark mark='b'/>The conclusion that g is actual "
            "needs only the B axiom, symmetry: it holds on every B frame. <bookmark mark='c'/>So the logic is "
            "impeccable, provided metaphysical necessity obeys S5, and most philosophers think it does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            for r in range(4):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
            self.play(FadeIn(note), FadeIn(rows2[0]))
            for mk, r in zip("bc", rows2[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def mirror(self):
        head = label(r"The mirror image", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        a = VGroup(MathTex(r"\Diamond \Box g", font_size=40, color=DIV), MathTex(r"\Downarrow", font_size=36),
                   MathTex(r"\Box g", font_size=40, color=DIV)).arrange(DOWN, buff=0.15).move_to([-3.2, 1.0, 0])
        b = VGroup(MathTex(r"\Diamond \lnot g", font_size=40, color=BAD), MathTex(r"\Downarrow", font_size=36),
                   MathTex(r"\lnot \Diamond \Box g", font_size=40, color=BAD)).arrange(DOWN, buff=0.15).move_to(
            [3.2, 1.0, 0])
        la = label(r"possibly a maximally great being exists", font_size=19, color=DIV).next_to(a, DOWN, buff=0.2)
        lb = label(r"possibly no maximally excellent being exists", font_size=19, color=BAD).next_to(b, DOWN,
                                                                                                   buff=0.2)
        d = load("plantinga")
        ok = label(r"both valid on all " + f"{d['S5']['mirror']['frames']}" + r" S5 frames", font_size=20,
                   color=OK).move_to([0, -0.9, 0])
        rows = stack([(r"each premise seems conceivable; \ in S5 they cannot both be true", WHITE),
                      (r"the argument transfers all its force to the possibility premise", GOAL),
                      (r"Plantinga: \ not a proof, \ but shows belief in God can be rational", DIV)],
                     font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "But the logic cuts both ways. <bookmark mark='a'/>Start instead from the premise that possibly no "
            "maximally excellent being exists. In S5 that entails that it is not possible that one exists "
            "necessarily, and so that maximal greatness is impossible. <bookmark mark='b'/>The Reasoner finds the "
            "mirror argument valid on every S5 frame too. <bookmark mark='c'/>Each premise seems conceivable, yet in "
            "S5 they cannot both be true: one of them is necessarily false. <bookmark mark='d'/>So the argument "
            "transfers all its force to the possibility premise, and anyone who doubts the conclusion has equal "
            "reason to doubt it. <bookmark mark='e'/>Plantinga himself did not claim a proof. He claimed that the "
            "argument shows that belief in God is rationally acceptable, for someone who finds the premise "
            "compelling."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(la))
            vo.wait_until("a")
            self.play(FadeIn(b), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeIn(ok))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
