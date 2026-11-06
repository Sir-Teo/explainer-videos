from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Predict(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Predicting yourself", r"Could a complete science of you tell you what you will do?",
                            lit=(1960,), part=PART)
        with self.voiceover("Chapter eleven. Predicting yourself."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.evitable()
        self.contrarian()
        self.diagonal()
        self.newcomb()

    def evitable(self):
        d = load("avoider")
        head = label(r"Determined, \ yet avoidable \ (Dennett, \ 1984; \ 2003)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        assert (d["width"], d["height"], d["steps"]) == (9, 5, 400)
        assert (d["blind_hits"], d["sighted_hits"], d["dodges"], d["deterministic"]) == (34, 0, 32, True)
        W, H, sz = d["width"], d["height"], 0.55
        o = np.array([-6.0, 1.6, 0])

        def cell(r, c):
            return o + np.array([c * sz, -r * sz, 0])
        grid = VGroup(*[Square(sz, stroke_color=GREY_D, stroke_width=1).move_to(cell(r, c)) for r in range(H)
                        for c in range(W)])
        frames = d["frames"]

        def draw(f):
            rocks = VGroup(*[Dot(cell(r, c), radius=0.16, color=LAW) for r, c in f["rocks"]])
            agent = Square(sz * 0.7, color=WILL, fill_opacity=0.9, stroke_width=0).move_to(cell(H - 1, f["pos"]))
            return VGroup(rocks, agent)
        cur = draw(frames[0])
        gl = label(r"rocks fall one row a step; \ the agent looks one row up", font_size=16, color=GREY_A).next_to(
            grid, DOWN, buff=0.25)
        hd = [r"", r"\text{blind: stays}", r"\text{sighted: steps aside}"]
        cells = [[label(r"hits in 400 steps", font_size=18), label(str(d["blind_hits"]), font_size=20, color=BAD),
                  label(str(d["sighted_hits"]), font_size=20, color=OK)],
                 [label(r"dodges", font_size=18), label(r"0", font_size=20), label(str(d["dodges"]), font_size=20,
                                                                                 color=OK)]]
        tab = ValueGrid(hd, cells, col_w=[2.6, 2.0, 2.6], cell_h=0.55, font_size=17).move_to([3.4, 1.0, 0])
        side = stack([(r"rerun: \ the identical history, \ step for step", LAW),
                      (r"each dodge: \ had it stayed, \ it would have been hit", WILL),
                      (r"determinism is not inevitability: \ what is avoided was avoidable", GOAL)], font_size=18,
                     aligned_edge=LEFT, width=6.0, buff=0.22).move_to([3.4, -1.4, 0])
        with self.voiceover(
            "Before prediction from outside, a point of Daniel Dennett's about what determinism does not mean. "
            "<bookmark mark='a'/>The Reasoner builds a deterministic world: rocks fall down a strip, one row a step, "
            "at columns fixed in advance, and an agent stands on the bottom row. <bookmark mark='b'/>One agent is "
            "blind and stays put. In four hundred steps it is hit thirty four times. The other looks one row up, and "
            "steps aside when a rock is about to land on it. It is hit no times, and dodges thirty two. "
            "<bookmark mark='c'/>Run the world again and every step repeats exactly: nothing here is undetermined. "
            "<bookmark mark='d'/>Yet each dodge supports a counterfactual: had the agent stayed, it would have been "
            "hit. <bookmark mark='e'/>Dennett's lesson is that determinism is not inevitability. In a determined "
            "world some things are avoided, by systems built to avoid them, and the capacity to avoid is what "
            "freedom, in the sense worth wanting, is made of. Incompatibilists reply that what is avoided was still "
            "fixed before the agent existed."
        ) as vo:
            self.play(FadeIn(head), Create(grid), FadeIn(cur), FadeIn(gl))
            vo.wait_until("a")
            for f in frames[1:12]:
                self.remove(cur)
                cur = draw(f)
                self.add(cur)
                self.wait(0.35)
            vo.wait_until("b")
            self.play(FadeIn(tab.head), Create(tab.rule), *[FadeIn(c) for row in tab.cell for c in row])
            for f in frames[12:24]:
                self.remove(cur)
                cur = draw(f)
                self.add(cur)
                self.wait(0.3)
            for mk, r in zip("cde", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def contrarian(self):
        d = load("prediction")
        head = label(r"A prediction the agent can read", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["public_right"] == 0 and [r["act"] for r in d["public"]] == ["right", "left"]
        hd = [r"\text{the prediction says}", r"\text{the agent reads it, \ and does}", r"\text{prediction}"]
        cells = [[label(r["prediction"], font_size=21, color=FUNC), label(r["act"], font_size=21, color=WILL),
                  label(r"wrong", font_size=21, color=BAD)] for r in d["public"]]
        grid = ValueGrid(hd, cells, col_w=[3.8, 4.6, 2.4], cell_h=0.7, font_size=20).move_to([0, 0.4, 0])
        rows = stack([(r"MacKay \ (1960): \ no prediction of your choice is one you would be right to believe, \ "
                       r"since believing it would change it", GREY_A),
                      (r"not a gap in determinism: \ a fact about predictions that become causes", GOAL)],
                     font_size=20, buff=0.22).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Suppose determinism is true, and a perfect predictor exists. Could it tell you what you will do? "
            "<bookmark mark='a'/>Imagine an agent who, before choosing left or right, reads the prediction of its "
            "choice, and does the opposite. <bookmark mark='b'/>If the prediction says left, it goes right. If it "
            "says right, it goes left. Both possible predictions are wrong. <bookmark mark='c'/>Donald MacKay argued "
            "in 1960 that there is no prediction of your choice that you would be correct to believe, since your "
            "believing it is among the causes of what you do. <bookmark mark='d'/>That is not a gap in determinism. "
            "A predictor that kept its prediction to itself could be right. It is a fact about predictions that "
            "become causes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in grid.cell[0][:1]])
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[0][1:]])
            self.play(*[FadeIn(c) for c in grid.cell[1]])
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def diagonal(self):
        d = load("prediction")
        head = label(r"The diagonal \ (Part 7)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        T = d["table"]
        n = len(T)
        assert n == 6 and all(d["differs"])
        size = 0.62
        x0, y0 = -4.6, 1.6
        cells, diag = VGroup(), VGroup()
        for i in range(n):
            for j in range(n):
                sq = Square(side_length=size, stroke_width=1, color=GREY_C).move_to([x0 + j * size, y0 - i * size, 0])
                t = label(r"L" if T[i][j] == 0 else r"R", font_size=18, color=FUNC if i != j else CHANCE).move_to(sq)
                cells.add(VGroup(sq, t))
                if i == j:
                    diag.add(SurroundingRectangle(sq, color=CHANCE, buff=0.0))
        rl = VGroup(*[label(f"predictor {i + 1}", font_size=15, color=GREY_A).next_to(
            [x0 - size / 2, y0 - i * size, 0], LEFT, buff=0.15) for i in range(n)])
        cl = VGroup(*[label(f"{j + 1}", font_size=15, color=GREY_A).move_to([x0 + j * size, y0 + 0.5, 0])
                      for j in range(n)])
        ctop = label(r"situation", font_size=16, color=GREY_A).next_to(cl, UP, buff=0.1)
        agent = VGroup(*[label(r"L" if v == 0 else r"R", font_size=18, color=WILL).move_to(
            [x0 + j * size, y0 - n * size - 0.15, 0]) for j, v in enumerate(d["diagonal"])])
        al = label(r"the diagonal agent", font_size=15, color=WILL).next_to(agent, LEFT, buff=0.3)
        side = stack([(r"in situation $k$, \ do the opposite of what predictor $k$ says there", WILL),
                      (r"so it differs from every predictor somewhere", GOAL),
                      (r"for any list of predictors whose outputs the agent can consult", GREY_A),
                      (r"Cantor's diagonal, \ and Turing's: \ no list contains it", SELF)], font_size=19,
                     aligned_edge=LEFT, width=5.2, buff=0.3).move_to([3.6, 0.4, 0])
        with self.voiceover(
            "The contrarian generalizes, by the diagonal argument of Part 7. <bookmark mark='a'/>List any "
            "predictors you like, six here, each a function from situations to predicted acts: left or right. "
            "<bookmark mark='b'/>Now build an agent that, in situation k, consults predictor k and does the "
            "opposite of what it says there. <bookmark mark='c'/>The agent differs from predictor one in situation "
            "one, from predictor two in situation two, and so on down the diagonal: it differs from every predictor "
            "on the list. <bookmark mark='d'/>The same holds for any list, however long, as long as the agent can "
            "consult the predictions. It is Cantor's diagonal, and Turing's: an agent that can read its predictions "
            "is not on any list of predictions it can read."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(rl), FadeIn(cl), FadeIn(ctop))
            vo.wait_until("b")
            self.play(Create(diag), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(a) for a in agent], lag_ratio=0.2), FadeIn(al), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def newcomb(self):
        head = label(r"A predictor you cannot defy", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        b1 = VGroup(Square(side_length=1.4, color=GREY_B, fill_opacity=0.08), label(r"\$1\,000", font_size=20,
                                                                                    color=OK)).move_to([-3.0, 0.4, 0])
        b2 = VGroup(Square(side_length=1.4, color=CHANCE, fill_opacity=0.08),
                    label(r"\$1\,000\,000 \ or nothing", font_size=16, color=CHANCE)).move_to([-0.6, 0.4, 0])
        rows = stack([(r"Newcomb's problem \ (Nozick, \ 1969)", HIST),
                      (r"a reliable predictor filled the opaque box only if it predicted you would take it alone", GREY_A),
                      (r"take one box, \ or both?", WILL),
                      (r"here the prediction is hidden: \ the agent cannot defy it, \ only respond to it: \ Part 33",
                       GOAL)], font_size=19, aligned_edge=LEFT, width=5.6, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Hide the prediction, and a different puzzle appears. <bookmark mark='a'/>Robert Nozick published it in "
            "1969 as Newcomb's problem. <bookmark mark='b'/>Two boxes: a clear one with a thousand dollars, and an "
            "opaque one, which a very reliable predictor filled with a million dollars only if it predicted you "
            "would take the opaque box alone. <bookmark mark='c'/>Do you take one box, or both? "
            "<bookmark mark='d'/>Here the agent cannot defy the prediction, because it cannot see it; it can only "
            "decide how to respond to the fact that it was made. Which answer is rational divides decision "
            "theorists to this day, and is where Part 33 begins."
        ) as vo:
            self.play(FadeIn(head), FadeIn(b1), FadeIn(b2))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
