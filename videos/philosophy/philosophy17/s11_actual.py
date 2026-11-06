from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


def tick(ok: bool) -> str:
    return r"$\checkmark$" if ok else r"$\times$"


class Actual(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Actual causation", r"Did this cause that, on this occasion?", lit=(2005, 2015),
                            part=PART)
        with self.voiceover("Chapter ten. Actual causation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.definition()
        self.cases()
        self.price()
        self.normality()

    def definition(self):
        d = {(c["case"], c["candidate"]): c for c in load("actual")["cases"]}
        hc = history_card(2005, r"Joseph Halpern and Judea Pearl", r"`Causes and Explanations'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        g = CausalGraph({"ST": [-5.6, 0.6, 0], "SH": [-3.6, 0.6, 0], "BT": [-5.6, -1.4, 0], "BH": [-3.6, -1.4, 0],
                         "BS": [-1.6, -0.4, 0]},
                        [("ST", "SH"), ("SH", "BS"), ("BT", "BH"), ("BH", "BS"), ("SH", "BH")], radius=0.42,
                        font_size=18, colors={"ST": SUZY, "SH": SUZY, "BT": BILLY, "BH": BILLY, "BS": EFFECT})
        inh = label(r"$-$", font_size=30, color=BAD).next_to(g.edge[("SH", "BH")], RIGHT, buff=0.08)
        key = label(r"throws, \ hits, \ bottle shatters; \ Suzy's hit stops Billy's", font_size=18,
                    color=GREY_A).next_to(g, DOWN, buff=0.3)
        defs = stack([(r"$X = x$ is an actual cause of $\varphi$ \ (modified, \ Halpern 2015) \ iff", WHITE),
                      (r"AC1: \ $X = x$ and $\varphi$ both actually hold", GREY_A),
                      (r"AC2: \ for some set $W$ held at its \textit{actual} values, \ and some $x'$, \ "
                       r"setting $X = x'$ makes $\varphi$ false", CAUSE),
                      (r"AC3: \ no part of $X$ already satisfies AC1 and AC2", GREY_A)], font_size=20,
                     aligned_edge=LEFT, width=7.0).move_to([3.0, 0.9, 0])
        w = d[("rock throwing", "ST")]["witness"]
        wit = stack([(r"the witness for Suzy: \ hold $W = \{" + ", ".join(w["W"]) + r"\}$ at its actual value 0; \ "
                      r"set $ST = 0$: \ the bottle survives", SUZY),
                     (r"Suzy: \ " + tick(d[("rock throwing", "ST")]["hp"]) + r" \ \ Billy: \ " +
                      tick(d[("rock throwing", "BT")]["hp"]) + r" \ \ (but-for: \ " +
                      tick(d[("rock throwing", "ST")]["but_for"]) + r", \ " +
                      tick(d[("rock throwing", "BT")]["but_for"]) + r")", OK)], font_size=20, aligned_edge=LEFT,
                    width=7.0).next_to(defs, DOWN, buff=0.45, aligned_edge=LEFT)
        with self.voiceover(
            "Joseph Halpern and Judea Pearl brought structural models to the question of actual causation: did "
            "this cause that, on this occasion? <bookmark mark='a'/>The trick is to model the case finely. Suzy "
            "and Billy throw; each rock may hit; the bottle shatters if either hits; and Suzy's hitting prevents "
            "Billy's. <bookmark mark='b'/>The definition, in Halpern's modified form of 2015, has three clauses. "
            "First, the cause and the effect both actually occur. <bookmark mark='c'/>Second, there is a "
            "contingency: hold some other variables fixed at their actual values, change the candidate cause, and "
            "the effect goes away. <bookmark mark='d'/>Third, minimality: no smaller part of the candidate already "
            "does the job. <bookmark mark='e'/>For Suzy, the witness is Billy's hit. Hold it at its actual value, "
            "which is no hit, and remove Suzy's throw: the bottle survives. For Billy, no contingency works, "
            "because Billy's rock never hit. The definition says what intuition says, though neither passes the "
            "simple but-for test."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(inh), FadeIn(key))
            for mk, r in zip("bcd", [VGroup(defs[0], defs[1]), defs[2], defs[3]]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(Indicate(g.node["BH"], color=SUZY), FadeIn(wit))
        self.clear_scene()

    def cases(self):
        d = load("actual")["cases"]
        head = label(r"The definition on the classic cases", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        intuit = {("rock throwing", "ST"): (r"yes", True), ("rock throwing", "BT"): (r"no", False),
                  ("forest fire (disjunctive)", "L"): (r"yes \ (each fire alone suffices)", True),
                  ("forest fire (conjunctive)", "L"): (r"yes", True),
                  ("double prevention", "B"): (r"divided", None), ("bogus prevention", "B"): (r"no", False)}
        names = {("rock throwing", "ST"): r"preemption: \ Suzy", ("rock throwing", "BT"): r"preemption: \ Billy",
                 ("forest fire (disjunctive)", "L"): r"overdetermination: \ lightning",
                 ("forest fire (conjunctive)", "L"): r"joint causes: \ lightning",
                 ("double prevention", "B"): r"double prevention", ("bogus prevention", "B"): r"bogus prevention"}
        hd = [r"\text{case}", r"\text{but-for}", r"\text{HP 2015}", r"\text{intuition}"]
        rows = []
        for c in d:
            k = (c["case"], c["candidate"])
            it, iv = intuit[k]
            agree = iv is None or iv == c["hp"]
            rows.append([label(names[k], font_size=20), label(tick(c["but_for"]), font_size=22,
                                                              color=OK if c["but_for"] else BAD),
                         label(tick(c["hp"]), font_size=22, color=OK if c["hp"] else BAD),
                         label(it, font_size=19, color=GREY_A if agree else BAD)])
        grid = ValueGrid(hd, rows, col_w=[4.2, 1.8, 1.8, 4.4], cell_h=0.52, font_size=20).move_to([0, 0.3, 0])
        notes = stack([(r"double prevention: \ Billy shoots down the fighter that would have downed Suzy's bomber: \ "
                        r"a cause with no connecting process \ (Hall, \ 2004)", CAUSE),
                       (r"overdetermination: \ HP 2015 calls lightning \textit{part} of a cause: \ the conjunction "
                        r"`lightning and match' is the cause", BAD)], font_size=19, aligned_edge=LEFT,
                      width=12.6).to_edge(DOWN, buff=0.35)
        fire_conj = next(c for c in d if c["case"] == "forest fire (disjunctive)")["conjunction_L_and_M"]
        assert fire_conj
        with self.voiceover(
            "The Reasoner runs the definition on six classic cases. <bookmark mark='a'/>Preemption: Suzy is a "
            "cause, and Billy is not, as intuition says. <bookmark mark='b'/>Overdetermination: lightning and a "
            "dropped match each would have started the forest fire alone. Intuition calls each a cause. The modified "
            "definition says the cause is the conjunction, lightning and match, and each is only part of it. "
            "<bookmark mark='c'/>When both are needed, lightning is a cause, by every test. "
            "<bookmark mark='d'/>Double prevention: Billy shoots down an enemy fighter that would have shot down "
            "Suzy's bomber, and Suzy destroys her target. The definition says Billy's shot is a cause. Ned Hall "
            "pointed out that no process connects them, and intuitions divide. <bookmark mark='e'/>Bogus "
            "prevention: a bodyguard puts antidote in the king's coffee, but no assassin ever poisoned it. The "
            "antidote is not a cause of survival. The original 2005 definition said it was; the 2015 version "
            "fixes this. <bookmark mark='f'/>Every proposed analysis faces such a list, and none yet agrees with "
            "intuition on every case."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, rr in zip("abcde", [[0, 1], [2], [3], [4], [5]]):
                vo.wait_until(mk)
                self.play(*[FadeIn(VGroup(*grid.cell[r])) for r in rr])
                if mk == "b":
                    self.play(FadeIn(notes[1]))
                if mk == "d":
                    self.play(FadeIn(notes[0]))
            vo.wait_until("f")
            self.play(Create(grid.row_box(2, BAD)), Create(grid.row_box(4, CAUSE)))
        self.clear_scene()

    def price(self):
        d = load("actual")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["P1"], ["P2"], ["P3"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.9, font_size=21,
                       center=[0, -0.5, 0], title=r"The Price List: \ late preemption")
        positions = [(("P3",), r"Lewis \ (1986)", r"fragility: \ Billy's rock would have caused a \textit{different} "
                                                  r"shattering, \ so the actual one does depend on Suzy"),
                     (("P1",), r"Hall \ (2004)", r"two concepts: \ \textit{production} and \textit{dependence}; \ "
                                                 r"Suzy produced the shattering"),
                     (("P1",), r"Halpern and Pearl", r"dependence under a contingency: \ hold Billy's hit at its "
                                                     r"actual value"),
                     (("P2",), r"the sceptic", r"actual causation is not a relation in nature, \ but a judgment of "
                                               r"what matters \ (Hitchcock and Knobe, \ 2009)")]
        with self.voiceover(
            "Late preemption is a Price List. <bookmark mark='a'/>Causation requires counterfactual dependence, or "
            "a chain of it. Suzy's throw caused the shattering. And no chain of dependence links her throw to the "
            "shattering, because Billy's rock would have done it. <bookmark mark='b'/>The three cannot all be "
            "true. <bookmark mark='c'/>David Lewis considered denying the third, by making events fragile: the "
            "shattering caused by Billy would have been a different event, a moment later. Critics answered that fragility "
            "makes too much a cause, since nearly everything affects exactly when things happen. "
            "<bookmark mark='d'/>Ned Hall gave up the first: there are two concepts of cause, production and "
            "dependence, and Suzy produced the shattering. <bookmark mark='e'/>Halpern and Pearl give up the first "
            "in a different way: dependence is required, but only under a contingency. "
            "<bookmark mark='f'/>And a sceptic can give up the second, in a sense: that Suzy is the cause is a "
            "judgment about which factors matter, as Christopher Hitchcock and Joshua Knobe argue, not a further "
            "fact in nature."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def normality(self):
        votes = load("actual")["votes"]
        head = label(r"Normality and responsibility", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pens = stack([(r"Knobe and Fraser \ (2008): \ the pen case", CAUSE),
                      (r"faculty may take pens; \ the assistant may not; \ both take one; \ none are left", GREY_A),
                      (r"most people say the \textit{assistant} caused the problem", WHITE),
                      (r"Halpern and Hitchcock \ (2015): \ rank witnesses by how normal they are", OK)],
                     font_size=20, aligned_edge=LEFT, width=6.2).move_to([-3.4, 1.0, 0])
        hd = [r"\text{vote}", r"k", r"\text{responsibility } 1/(k+1)"]
        rows = [[MathTex(f"{v['n_for']}\\text{{--}}{v['n_against']}", font_size=24),
                 MathTex(str(v["k"]), font_size=24, color=CAUSE),
                 MathTex(f"{v['degree']:.2f}", font_size=24, color=OK)] for v in votes]
        grid = ValueGrid(hd, rows, col_w=[1.6, 1.0, 3.4], cell_h=0.52, font_size=20).move_to([3.4, 0.6, 0])
        gl = label(r"Chockler and Halpern \ (2004): \ $k$ = votes that must change before hers is pivotal",
                   font_size=19, color=GREY_A).next_to(grid, DOWN, buff=0.3)
        foot = label(r"causation is all-or-nothing; \ responsibility and blame come in degrees", font_size=22,
                     color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Two refinements bring the theory closer to how people judge. <bookmark mark='a'/>Joshua Knobe and Ben "
            "Fraser's pen case: faculty are allowed to take pens from the office, administrative assistants are "
            "not. <bookmark mark='b'/>One morning a professor and an assistant each take a pen, and none are left "
            "for an important note. <bookmark mark='c'/>Most people say the assistant caused the problem, though "
            "the two acts are symmetric in the structure. <bookmark mark='d'/>Halpern and Christopher Hitchcock "
            "built this in, by ranking contingencies by how normal they are. <bookmark mark='e'/>And Hana Chockler "
            "and Halpern defined degrees of responsibility. In an eleven-voter election won six to five, each "
            "winning voter is pivotal: responsibility one. Won eleven to nothing, five votes must change before any "
            "one voter is pivotal: responsibility one sixth. <bookmark mark='f'/>Causation is all or nothing; "
            "responsibility, and with it blame, comes in degrees."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", pens):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*row)) for row in grid.cell],
                                                                        lag_ratio=0.3), FadeIn(gl))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
