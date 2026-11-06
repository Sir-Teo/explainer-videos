from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Foreknow(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Foreknowledge and the open future", r"If God knows what I will do, \ am I free?",
                            lit=(524, 1967), part=PART)
        with self.voiceover("Chapter twelve. Foreknowledge and the open future."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.argument()
        self.answers()
        self.tree()
        self.verdict()

    def argument(self):
        head = label(r"The argument from foreknowledge", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        steps = stack([(r"1. \ yesterday God knew that I would mow the lawn today", DIV),
                       (r"2. \ the past is now fixed: \ nothing I can do will make God not have known it", WHITE),
                       (r"3. \ necessarily, \ if God knew it, \ it is true \ (knowledge is factive)", ABS),
                       (r"4. \ so nothing I can do will make it false that I mow the lawn", BAD),
                       (r"5. \ so I do not mow freely, \ in the sense of being able to do otherwise", BAD)],
                      font_size=22, aligned_edge=LEFT, width=12.2, buff=0.32).move_to([0, -0.2, 0])
        with self.voiceover(
            "If God knows everything, God knows the future, including what I will freely do. Does that leave me free? "
            "<bookmark mark='a'/>Yesterday God knew that I would mow the lawn today. <bookmark mark='b'/>The past is "
            "now fixed: nothing I can do will make it the case that God did not know it. <bookmark mark='c'/>And "
            "necessarily, if God knew it, it is true, since knowledge implies truth. <bookmark mark='d'/>So nothing I "
            "can do will make it false that I mow the lawn. <bookmark mark='e'/>So I do not mow freely, if freedom "
            "requires being able to do otherwise. The argument is old, and Part 32 will meet its secular twin, "
            "fatalism."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def answers(self):
        hc = history_card(524, r"Boethius", r"\textit{The Consolation of Philosophy}, \ book V", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"Boethius", r"God is outside time: \ he sees all times at once, \ as we see a man walking; \ seeing does "
                          r"not compel", DIV),
            (r"Ockham", r"God's past belief is a `soft' fact, \ partly about the future: \ not fixed like a hard fact",
             ABS),
            (r"Molina", r"middle knowledge: \ God knows what I would freely do, \ in every circumstance", HUM),
            (r"open theism", r"the future free acts are not yet there to be known: \ God knows all that can be known",
             NAT),
            (r"Aristotle", r"\textit{De Interpretatione} 9: \ a sea battle tomorrow is neither true nor false today?",
             WARM),
        ]
        g = rows_table(rows, top=1.2, gap=0.45, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "There are four classic answers. <bookmark mark='a'/>Boethius, writing in prison around 524, said that God "
            "is not in time. God sees all times at once, as we might watch a man walking, and seeing a man walk does "
            "not make him walk. <bookmark mark='b'/>William of Ockham: God's past belief is a soft fact, partly about "
            "the future, so it is not fixed in the way a hard fact about the past is. <bookmark mark='c'/>Molina's "
            "middle knowledge, from chapter nine: God knows what I would freely do in every circumstance. "
            "<bookmark mark='d'/>Open theists deny that future free actions are there to be known; God knows all "
            "that can be known, and the free future cannot. <bookmark mark='e'/>Behind all of them stands Aristotle's "
            "sea battle: is it true today that there will be a sea battle tomorrow?"
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def tree(self):
        d = load("battle")
        head = label(r"Prior's branching time, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        m0 = np.array([-5.5, -0.4, 0])
        m1 = np.array([-3.5, 1.0, 0])
        m2 = np.array([-3.5, -1.8, 0])
        b1 = Line(m0, m1, color=OK, stroke_width=5)
        b2 = Line(m0, m2, color=BAD, stroke_width=5)
        trunk = Line(m0 + LEFT * 1.2, m0, color=GREY_B, stroke_width=5)
        dots = VGroup(*[Dot(p, radius=0.11, color=WHITE) for p in (m0, m1, m2)])
        labs = VGroup(label(r"today", font_size=18).next_to(m0, DOWN, buff=0.15),
                      label(r"$h_1$: \ a sea battle", font_size=18, color=OK).next_to(m1, RIGHT, buff=0.15),
                      label(r"$h_2$: \ no battle", font_size=18, color=BAD).next_to(m2, RIGHT, buff=0.15))
        hd = [r"\text{at today}", r"\text{Peircean}", r"\text{Ockhamist } h_1", r"\text{Ockhamist } h_2"]
        P_, O = d["peircean"], d["ockhamist"]
        keys = [("F battle", r"F\,b"), ("F no battle", r"F\,\lnot b"), ("F battle or F no battle", r"F\,b \lor F\,\lnot b")]
        rows = [[MathTex(t, font_size=24), tf(P_[k]), tf(O["h1"][k]), tf(O["h2"][k])] for k, t in keys]
        rows.append([MathTex(r"F\,(b \lor \lnot b)", font_size=24), tf(P_["F (battle or no battle)"]),
                     tf(True), tf(True)])
        grid = ValueGrid(hd, rows, col_w=[2.3, 1.6, 1.9, 1.9], cell_h=0.52, font_size=19).move_to([3.1, -0.3, 0])
        rows2 = stack([(r"Peircean: \ `it will be that $p$' means on \textit{every} branch: \ both futures false, \ "
                        r"bivalence fails for them", ARG),
                       (r"Ockhamist: \ truth relative to a history: \ one of them is true, \ but neither is "
                        r"\textit{settled}", ABS)], font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN,
                                                                                                         buff=0.4)
        with self.voiceover(
            "Arthur Prior turned the sea battle into logic, and the Reasoner builds his two semantics. "
            "<bookmark mark='a'/>Time branches: from today there is a history with a sea battle tomorrow and one "
            "without. <bookmark mark='b'/>On the Peircean reading, it will be that p means that p happens on every "
            "branch. Then it will be that there is a battle is false, it will be that there is no battle is also "
            "false, and so is their disjunction; though it will be that there is a battle or no battle is true. "
            "<bookmark mark='c'/>On the Ockhamist reading, truth is relative to a history. On the first history, "
            "there will be a battle; on the second, there will not; on each, one of the two is true. But neither is "
            "settled: what is true on every history is only the disjunction. <bookmark mark='d'/>Ockhamism gives "
            "God something to foreknow, truths relative to the history that will be actual, without making them "
            "settled now."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(trunk), Create(b1), Create(b2), FadeIn(dots), FadeIn(labs))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(grid.cell[r][c]) for r in range(4) for c in (0, 1)],
                      FadeIn(rows2[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[r][c]) for r in range(4) for c in (2, 3)], FadeIn(rows2[1]))
            vo.wait_until("d")
            self.play(Indicate(b1, color=DIV), Indicate(grid.cell[2][2], color=DIV))
        self.clear_scene()

    def verdict(self):
        head = label(r"Where it leaves us", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the logic", r"choose the tense logic, \ and you choose whether future contingents have truth values",
             ABS),
            (r"the theology", r"Ockhamists and Molinists keep full foreknowledge; \ open theists keep an open future",
             DIV),
            (r"the physics", r"relativity's block universe \ (Part 25) \ may make every future fact already there",
             NAT),
            (r"the freedom", r"Frankfurt \ (1969): \ is the ability to do otherwise what freedom needs? \ (Part 32)",
             HUM),
        ]
        g = rows_table(rows, top=1.7, gap=0.55, width=8.8, x_text=-2.4, label_size=22, text_size=22)
        with self.voiceover(
            "Where does it leave us? <bookmark mark='a'/>Choose your logic of tense, and you have chosen whether "
            "statements about the free future have truth values now. <bookmark mark='b'/>Ockhamists and Molinists "
            "keep full foreknowledge; open theists keep an open future, and a God who learns. "
            "<bookmark mark='c'/>Physics may take sides: the block universe of relativity, in Part 25, makes every "
            "future event as real as every past one. <bookmark mark='d'/>And Harry Frankfurt asked whether freedom "
            "needs the ability to do otherwise at all, a question for Part 32."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
