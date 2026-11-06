from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403

POS = {0: (-2.4, 0.0, 0), 1: (0.0, 1.5, 0), 2: (0.0, -1.5, 0), 3: (2.4, -1.5, 0)}


class Kripke(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Possible worlds, made precise", r"What makes `necessarily' true?", lit=(1959,),
                            part=PART)
        with self.voiceover("Chapter three. Possible worlds, made precise."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.history()
        self.definition()
        self.evaluate()
        self.deadend()
        self.readings()

    def history(self):
        hcs = VGroup(history_card(1959, r"Saul Kripke, aged 18", r"`A completeness theorem in modal logic', "
                                  r"\textit{J.\ Symbolic Logic}", width=5.8, color=HIST),
                     history_card(r"1957--63", r"Kanger, \ Hintikka, \ Montague, \ Prior", r"relational semantics, "
                                  r"found several times over", width=5.8, color=HIST)).arrange(RIGHT, buff=0.4)
        hcs.to_edge(UP, buff=0.5)
        idea = VGroup(label(r"Leibniz: \ necessary = true in \textit{all} worlds", font_size=28, color=GREY_A),
                      label(r"Kripke: \ necessary = true in all worlds \textit{accessible} from here", font_size=30,
                            color=GOAL)).arrange(DOWN, buff=0.35).move_to([0, -0.8, 0])
        with self.voiceover(
            "In 1959 Saul Kripke, then eighteen, published a paper in the Journal of Symbolic Logic that gave "
            "modal logic its semantics. <bookmark mark='a'/>Stig Kanger, Jaakko Hintikka, Richard Montague and Arthur "
            "Prior had similar ideas in the same years; Kripke's version became the standard. "
            "<bookmark mark='b'/>The idea adds one thing to Leibniz. Necessary does not mean true in all worlds, "
            "<bookmark mark='c'/>but true in all worlds accessible from this one. Change which worlds are "
            "accessible, and you change the logic."
        ) as vo:
            self.play(FadeIn(hcs[0], shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(hcs[1], shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(idea[0]))
            vo.wait_until("c")
            self.play(FadeIn(idea[1]))
        self.clear_scene()

    def definition(self):
        d = load("kripke")
        g = WorldGraph(d["worlds"], d["R"], {"p": set(d["p"])}, pos=POS, center=[-3.0, -0.4, 0], scale_pos=0.9)
        defs = VGroup(
            label(r"a \textit{frame}: \ worlds $W$, \ an accessibility relation $R$", font_size=24),
            label(r"a \textit{model}: \ a frame, \ and where each atom is true", font_size=24),
            MathTex(r"w \models \Box\varphi \iff \text{for all } v \text{ with } wRv:\ v \models \varphi",
                    font_size=32, color=GOAL),
            MathTex(r"w \models \Diamond\varphi \iff \text{for some } v \text{ with } wRv:\ v \models \varphi",
                    font_size=32, color=GOAL),
            label(r"the connectives: \ exactly as in Part 2, world by world", font_size=24, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.0, 0.2, 0])
        if defs.width > 7.2:
            defs.width = 7.2
            defs.move_to([3.1, 0.2, 0])
        with self.voiceover(
            "Here are the definitions. <bookmark mark='a'/>A frame is a set of worlds and a relation between them, "
            "accessibility, drawn as arrows. <bookmark mark='b'/>A model adds, for each atomic sentence, the worlds "
            "where it is true. Here p is true at worlds one and three. <bookmark mark='c'/>Necessarily phi is true "
            "at a world when phi is true at every world it can see. <bookmark mark='d'/>Possibly phi is true when "
            "phi is true at some world it can see. <bookmark mark='e'/>Everything else works exactly as in Part 2, "
            "one world at a time. It is Tarski's definition again, with worlds in place of objects."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(defs[0]), FadeIn(VGroup(*[g.world[w][0] for w in g.world], *[g.name[w] for w in g.name])),
                      LaggedStart(*[Create(a) for a in g.arrows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(defs[1]), FadeIn(VGroup(*g.inside.values())))
            vo.wait_until("c")
            self.play(FadeIn(defs[2]))
            vo.wait_until("d")
            self.play(FadeIn(defs[3]))
            vo.wait_until("e")
            self.play(FadeIn(defs[4]))
        self.clear_scene()

    def evaluate(self):
        d = load("kripke")
        g = WorldGraph(d["worlds"], d["R"], {"p": set(d["p"])}, pos=POS, center=[-3.0, -0.4, 0], scale_pos=0.9)
        forms = ["<>p", "[]p", "[]<>p", "[]p -> p"]
        hd = [label(r"formula", font_size=22, color=P.CLAIM)] + [MathTex(rf"w_{w}", font_size=26, color=WORLD)
                                                                 for w in d["worlds"]]
        rows = [[mf(f, font_size=28)] + d["table"][f] for f in forms]
        grid = ValueGrid(hd, rows, col_w=[2.6, 0.8, 0.8, 0.8, 0.8], font_size=24).move_to([3.4, 0.6, 0])
        note_ = label(r"$\Box p \to p$ fails at $w_2$: \ $w_2$ cannot see itself", font_size=24, color=BAD).next_to(
            grid, DOWN, buff=0.4)
        self.add(g)
        with self.voiceover(
            "Now compute. <bookmark mark='a'/>Possibly p: every world here can see some p-world. World zero sees "
            "world one, world two sees world three, and worlds one and three see themselves. True everywhere. "
            "<bookmark mark='b'/>Necessarily p is false at world zero, which can see world two, where p fails. It "
            "is true at the other three. <bookmark mark='c'/>Necessarily possibly p: at every visible world, p is "
            "possible. True everywhere, since possibly p was. <bookmark mark='d'/>And 'if necessarily p, then p' "
            "fails at world two: everything world two can see has p, but world two itself does not, because it "
            "cannot see itself. That failure is the clue to the next chapter."
        ) as vo:
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][0]) for r in range(len(rows))])
            for mk, r in zip("abcd", range(len(rows))):
                vo.wait_until(mk)
                anims = [FadeIn(grid.cell[r][c + 1], scale=0.6) for c in range(4)]
                tags = [g.tag(w, v) for w, v in zip(d["worlds"], d["table"][forms[r]])]
                self.play(*anims, *[FadeIn(t) for t in tags])
                if mk != "d":
                    self.play(*[FadeOut(t) for t in tags], run_time=0.4)
            self.play(FadeIn(note_), Indicate(g.world[2][0], color=BAD))
        self.clear_scene()

    def deadend(self):
        g = WorldGraph([0, 1], {(0, 1)}, {"p": {0}}, pos={0: (0, 0, 0), 1: (2.2, 0, 0)}, center=[-5.6, 0.4, 0])
        rows = VGroup(MathTex(r"w_1 \models \Box \varphi \ \text{ for every } \varphi", font_size=36, color=GOAL),
                      label(r"$w_1$ sees nothing, \ so `true at every visible world' holds vacuously", font_size=24,
                            color=GREY_A),
                      MathTex(r"w_1 \models \Box \bot", font_size=40, color=BAD),
                      label(r"even a contradiction is `necessary' at a dead end", font_size=24, color=BAD),
                      MathTex(r"\Box p \to \Diamond p \ \text{ fails at } w_1", font_size=34),
                      label(r"axiom D rules out dead ends: \ in deontic logic, an ideal world always exists",
                            font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.2, -0.3, 0])
        with self.voiceover(
            "One special case deserves a look. <bookmark mark='a'/>A world that sees no world at all. "
            "<bookmark mark='b'/>At such a dead end, necessarily phi is true for every phi, because there is no "
            "visible world where phi could fail. <bookmark mark='c'/>Even a contradiction is necessary there, and "
            "nothing is possible. <bookmark mark='d'/>So 'necessarily p implies possibly p' fails at a dead end. That "
            "axiom, D, says exactly that every world sees some world, and Chapter ten will need it for obligation."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(g))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
        self.clear_scene()

    def readings(self):
        head = label(r"What the arrows mean", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        rows = [(r"logical possibility", r"every world sees every world"),
                (r"physical possibility", r"worlds with our laws of nature"),
                (r"knowledge", r"worlds the agent cannot rule out"),
                (r"obligation", r"worlds where every duty is done"),
                (r"time", r"later moments"),
                (r"programs", r"states the program can reach")]
        tab = VGroup()
        for a, b in rows:
            tab.add(VGroup(label(a, font_size=26, color=GOAL), label(b, font_size=24, color=GREY_A)))
        for i, r in enumerate(tab):
            y = 1.8 - 0.62 * i
            r[0].move_to([-5.6 + r[0].width / 2, y, 0])
            r[1].move_to([-0.6 + r[1].width / 2, y, 0])
        moral = label(r"each reading suggests a shape of arrows; \ each shape validates different axioms",
                      font_size=26, color=OK).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The arrows are where the readings differ. <bookmark mark='a'/>For logical possibility, every world "
            "can see every world. For physical possibility, the visible worlds are those with our laws of nature. "
            "<bookmark mark='b'/>For knowledge, a world is visible when, for all the agent knows, it might be the "
            "actual one. For obligation, the visible worlds are the ideal ones, where every duty is done. "
            "<bookmark mark='c'/>For time, the visible moments are the later ones; for programs, the reachable "
            "states. <bookmark mark='d'/>And each reading suggests a shape for the arrows, which, as we are about "
            "to see, decides exactly which axioms hold."
        ) as vo:
            self.play(FadeIn(head))
            for mk, idx in (("a", [0, 1]), ("b", [2, 3]), ("c", [4, 5])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(tab[i], shift=RIGHT * 0.2) for i in idx], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()
