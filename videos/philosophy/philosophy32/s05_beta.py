from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Beta(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Rule beta, \ broken", r"Can a rule that looks like logic fail?", lit=(1983,),
                            part=PART)
        with self.voiceover("Chapter four. Rule beta, broken."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.semantics()
        self.coin()
        self.checked()
        self.repair()
        self.wall_brick()

    def semantics(self):
        head = label(r"A model of having a choice", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"worlds", r"the ways things might go from here", GREY_A),
                (r"actions", r"each available action is the set of worlds it might lead to", WILL),
                (r"a choice about $p$", r"some action is guaranteed to make $p$ false", FUNC),
                (r"$N p$", r"$p$ is true, \ and no action guarantees not-$p$", SELF)]
        g = rows_table(rows, top=1.4, gap=0.55)
        with self.voiceover(
            "To test the rules, the Reasoner needs a model of what it is to have a choice. "
            "<bookmark mark='a'/>Take the worlds that might come about from here. <bookmark mark='b'/>Each action "
            "available to the agent is the set of worlds it might lead to: one world, if its outcome is certain; "
            "several, if chance has a say. <bookmark mark='c'/>The agent has a choice about whether p if some "
            "available action is guaranteed to make p false. <bookmark mark='d'/>And N p holds when p is true, and "
            "no available action guarantees not p."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def coin(self):
        d = load("rules")
        head = label(r"McKay and Johnson's coin \ (1996)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["N_no_heads"] and d["N_no_tails"] and not d["N_both"]
        assert d["actions"] == {"refrain": ["not tossed"], "toss": ["heads", "tails"]}
        pos = {"not tossed": [-4.6, 0.6, 0], "heads": [-2.4, 1.4, 0], "tails": [-2.4, -0.2, 0]}
        cols = {"not tossed": WILL, "heads": CHANCE, "tails": CHANCE}
        nodes = {w: VGroup(Circle(radius=0.5, color=cols[w], fill_opacity=0.12),
                           label(w, font_size=16, color=cols[w])).move_to(p) for w, p in pos.items()}
        act = VGroup(SurroundingRectangle(nodes["not tossed"], color=WILL, buff=0.12, corner_radius=0.2),
                     SurroundingRectangle(VGroup(nodes["heads"], nodes["tails"]), color=CHANCE, buff=0.12,
                                          corner_radius=0.2))
        al = VGroup(label(r"refrain", font_size=18, color=WILL).next_to(act[0], DOWN, buff=0.12),
                    label(r"toss", font_size=18, color=CHANCE).next_to(act[1], RIGHT, buff=0.15))
        star = label(r"actual", font_size=16, color=OK).next_to(nodes["not tossed"], UP, buff=0.32)
        rows = stack([(r"$p$: \ `the coin does not land heads' \quad $N p$ \ $\checkmark$", OK),
                      (r"$q$: \ `the coin does not land tails' \quad $N q$ \ $\checkmark$", OK),
                      (r"$p \wedge q$: \ `the coin is not tossed' \quad $N(p \wedge q)$ \ $\times$", BAD),
                      (r"agglomeration fails: \ no choice about each, \ a choice about both", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=6.4, buff=0.3).move_to([3.4, 0.4, 0])
        with self.voiceover(
            "Thomas McKay and David Johnson found the countermodel in 1996. <bookmark mark='a'/>I have a coin, and I "
            "do not toss it, though I could. If I toss it, it lands heads or tails, and nothing I can do settles "
            "which. <bookmark mark='b'/>Two actions: refrain, which leads to the coin not being tossed; and toss, "
            "which leads to heads or to tails. <bookmark mark='c'/>Let p be: the coin does not land heads. It is "
            "true, and no action guarantees heads, so N p. <bookmark mark='d'/>Let q be: the coin does not land "
            "tails. By the same reasoning, N q. <bookmark mark='e'/>But p and q together say the coin is not tossed, "
            "and I do have a choice about that: I can toss it. <bookmark mark='f'/>No choice about each, a choice "
            "about both. The principle of agglomeration, from N p and N q infer N of p and q, fails."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(*[FadeIn(n) for n in nodes.values()], FadeIn(star))
            vo.wait_until("b")
            self.play(Create(act), FadeIn(al))
            for mk, r in zip("cdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def checked(self):
        d = load("rules")
        head = label(r"Every instance, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["props"], d["pairs"], d["alpha_fail"], d["beta_fail"], d["beta_box_fail"]) == (8, 64, 0, 2, 0)
        deriv = VGroup(*[MathTex(t, font_size=28, color=c) for t, c in (
            (r"N p, \;\; N q", WHITE),
            (r"N\big(p \rightarrow (q \rightarrow (p \wedge q))\big)\quad \text{rule } \alpha", SELF),
            (r"N\big(q \rightarrow (p \wedge q)\big)\quad \text{rule } \beta", SELF),
            (r"N(p \wedge q)\quad \text{rule } \beta", BAD))]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(
            [-3.2, 0.4, 0])
        dl = label(r"$\beta$ with $\alpha$ gives agglomeration", font_size=19, color=GREY_A).next_to(deriv, UP,
                                                                                                    buff=0.35)
        hd = [r"\text{rule}", r"\text{instances}", r"\text{failures}"]
        cells = [[MathTex(r"\alpha:\ \Box p \vdash N p", font_size=24, color=OK), label(str(d["props"]), font_size=20),
                  label(str(d["alpha_fail"]), font_size=20, color=OK)],
                 [MathTex(r"\beta:\ N p,\, N(p \rightarrow q) \vdash N q", font_size=24, color=BAD),
                  label(str(d["pairs"]), font_size=20), label(str(d["beta_fail"]), font_size=20, color=BAD)],
                 [MathTex(r"\beta_\Box:\ N p,\, \Box(p \rightarrow q) \vdash N q", font_size=24, color=OK),
                  label(str(d["pairs"]), font_size=20), label(str(d["beta_box_fail"]), font_size=20, color=OK)]]
        grid = ValueGrid(hd, cells, col_w=[4.4, 1.6, 1.6], cell_h=0.7, font_size=19).move_to([3.1, 0.2, 0])
        foot = label(r"the 8 propositions of the coin model, \ and all 64 pairs of them", font_size=19,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Why does that sink rule beta? <bookmark mark='a'/>Because beta, with alpha, gives agglomeration. From N "
            "p and N q: it is necessary that p implies that q implies p and q, so by alpha no one has a choice "
            "about it. By beta, N of q implies p and q. By beta again, N of p and q. <bookmark mark='b'/>The "
            "Reasoner checks every instance on the coin model: its eight propositions, and all sixty four pairs of "
            "them. Rule alpha never fails. Rule beta fails twice, at p equal to no heads or no tails, and q equal "
            "to the coin not being tossed. <bookmark mark='c'/>And a repaired rule, beta box, which needs the "
            "connection between p and q to be necessary rather than merely not up to us, never fails at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dl), LaggedStart(*[FadeIn(x) for x in deriv], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]], FadeIn(foot))
            self.play(*[FadeIn(c) for c in grid.cell[1]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[2]])
        self.clear_scene()

    def repair(self):
        head = label(r"The argument, \ repaired", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        lines = VGroup(*[MathTex(t, font_size=32, color=c) for t, c in (
            (r"1.\quad N(P_0 \wedge L)\qquad \text{the past and the laws, \ together, \ are fixed}", LAW),
            (r"2.\quad \Box\big((P_0 \wedge L) \rightarrow P\big)\qquad \text{determinism}", LAW),
            (r"3.\quad N P\qquad \text{from 1 and 2, \ rule } \beta_\Box", BAD))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.4).move_to([0, 0.6, 0])
        foot = stack([(r"Finch and Warfield \ (1998): \ only the valid rule, \ and a stronger premise", GREY_A),
                      (r"the compatibilist must now deny premise 1: \ that we have no choice about the past and laws "
                       r"together", GOAL)], font_size=20, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The argument can be repaired. <bookmark mark='a'/>Alicia Finch and Ted Warfield, in 1998, start from "
            "the premise that no one has a choice about the past and the laws taken together. "
            "<bookmark mark='b'/>Determinism says the two together necessitate P. <bookmark mark='c'/>And the "
            "valid rule, beta box, gives N P. <bookmark mark='d'/>The repaired argument uses only a rule the "
            "Reasoner has checked. The price is a stronger first premise, and that is where compatibilists now "
            "push back, as chapter six shows."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=32, current=32).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(32, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the thirty second brick in the Wall. <bookmark mark='a'/>The dream was freedom and determinism "
            "together: a world fixed by its past and laws, in which some acts are still up to us. The consequence "
            "argument, repaired, says that if determinism is true nothing is up to us; and Frankfurt's cases, next, "
            "question what freedom needs in the first place. <bookmark mark='b'/>What it forces is a choice: "
            "redefine freedom so that it does not need the past or the laws to be up to us, or deny determinism."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[32], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()
