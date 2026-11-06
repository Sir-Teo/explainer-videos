from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Machines(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Responsibility gaps", r"When a learning machine does harm, \ who answers for it?",
                            lit=(2004,), part=PART)
        with self.voiceover("Chapter fourteen. Responsibility gaps."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.gap()
        self.degrees()
        self.answers()

    def gap(self):
        hc = history_card(2004, r"Andreas Matthias", r"`The Responsibility Gap'", width=5.0,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [(r"the conditions", r"responsibility needs control and knowledge: \ the agent could foresee and "
                                    r"steer the outcome \ (Aristotle)", LAW),
                (r"learning machines", r"their behaviour is shaped by training no one fully specified, \ and can "
                                       r"change after deployment", FUNC),
                (r"the gap", r"the makers could not foresee it; \ the operators could not steer it; \ the machine is "
                             r"not an agent we can blame", BAD),
                (r"Sparrow \ (2007)", r"autonomous weapons: \ if no one is responsible for a killing, \ the killing "
                                      r"is wrong for that reason", BLAME)]
        g = rows_table(rows, top=1.4, gap=0.5)
        with self.voiceover(
            "The questions of this part now arise for machines. <bookmark mark='a'/>Since Aristotle, "
            "responsibility has been thought to need two things: control over what one does, and knowledge of it. "
            "<bookmark mark='b'/>A learning machine's behaviour is shaped by training that no one fully specified, "
            "and may change after it is deployed. <bookmark mark='c'/>So, Andreas Matthias argued in 2004, there "
            "can be a gap. The makers could not foresee what it would do, the operators could not steer it, and the "
            "machine itself is not the kind of thing we can blame. <bookmark mark='d'/>Robert Sparrow drew the "
            "conclusion for autonomous weapons in 2007: if no one can be held responsible for a killing, that is "
            "itself a reason the killing is wrong."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def degrees(self):
        d = load("responsibility")
        head = label(r"Degrees of responsibility \ (Chockler and Halpern, \ 2004)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        v = d["votes"]
        assert [r["vote"] for r in v] == ["6-5", "7-4", "8-3", "9-2", "10-1", "11-0"]
        assert d["hands"] == {"designer": 1.0, "deployer": 0.5, "overseer": 0.5}
        defn = MathTex(r"\mathrm{dr}(X) \;=\; \frac{1}{k + 1}", font_size=34, color=FUNC).move_to([-3.6, 2.1, 0])
        dl = label(r"$k$: \ fewest other changes that make $X$ critical", font_size=17, color=GREY_A).next_to(
            defn, DOWN, buff=0.15)
        hd = [r"\text{vote of 11}", r"k", r"\text{each majority voter}"]
        fr = {1.0: r"1", 0.5: r"1/2", 0.3333: r"1/3", 0.25: r"1/4", 0.2: r"1/5", 0.1667: r"1/6"}
        cells = [[label(r["vote"], font_size=19, color=WHITE), label(str(r["k"]), font_size=19, color=GREY_A),
                  MathTex(fr[r["degree"]], font_size=26, color=WILL)] for r in v]
        grid = ValueGrid(hd, cells, col_w=[2.2, 1.0, 3.0], cell_h=0.5, font_size=18).move_to([-3.2, -1.2, 0])
        harm = MathTex(r"\text{harm} \;=\; D \wedge (T \vee O)", font_size=30, color=BAD).move_to([3.4, 1.6, 0])
        hl = label(r"$D$: \ the designer ships a flaw; \ $T$: \ the deployer skips the test; \ $O$: \ the overseer "
                   r"is absent", font_size=16, color=GREY_A).next_to(harm, DOWN, buff=0.2)
        hands = stack([(r"all three failed", GREY_A), (r"designer: \ 1", BAD), (r"deployer: \ 1/2", WILL),
                       (r"overseer: \ 1/2", WILL),
                       (r"a measure, \ not a verdict: \ blame also weighs what each could know", GOAL)],
                      font_size=20, aligned_edge=LEFT, width=5.2, buff=0.25).move_to([3.4, -1.0, 0])
        with self.voiceover(
            "There is a precise way to spread responsibility over many hands. <bookmark mark='a'/>Hana Chockler and "
            "Joseph Halpern, in 2004, defined a degree of responsibility using the structural causal models of Part "
            "17. Your degree is one over k plus one, where k is the fewest other changes that would make your "
            "contribution critical. <bookmark mark='b'/>In an eleven-member vote won six to five, every majority "
            "voter was critical: degree one. Won seven to four, one other vote must change to make you critical: a "
            "half. Won eleven to nothing, five must change: one sixth. <bookmark mark='c'/>Now a harm with many "
            "hands. It happens if the designer ships a flaw, and either the deployer skips the test or the overseer "
            "is absent; all three failed. The designer's degree is one; the deployer's and the overseer's, a half "
            "each, since each would have been critical had the other done their job. <bookmark mark='d'/>It is a "
            "measure of causal contribution, not yet of blame, which Chockler and Halpern weigh further by what each "
            "agent could have known."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(defn), FadeIn(dl))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for k in range(6):
                self.play(*[FadeIn(c) for c in grid.cell[k]], run_time=0.4)
            vo.wait_until("c")
            self.play(Write(harm), FadeIn(hl))
            self.play(LaggedStart(*[FadeIn(r) for r in hands[:4]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(hands[4]))
        self.clear_scene()

    def answers(self):
        head = label(r"Closing the gap", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"many hands", r"spread responsibility over makers, \ deployers and overseers, \ as for institutions",
                 SELF),
                (r"strict liability", r"whoever profits from deploying the system answers for its harms, \ fault or "
                                      r"no fault", LAW),
                (r"meaningful human control", r"keep a human able to understand, \ intervene and answer: \ a design "
                                              r"requirement", OK),
                (r"the machine itself?", r"on Strawson's view, \ blame needs a participant; \ is there one? \ "
                                         r"Part 31's question again", BLAME),
                (r"ahead", r"fair machines, \ Part 41; \ aligned reasoners, \ Part 42", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.45)
        with self.voiceover(
            "There are several proposals to close the gap. <bookmark mark='a'/>Spread responsibility over the many "
            "hands that made, deployed and oversaw the system, as we do for institutions. "
            "<bookmark mark='b'/>Impose strict liability: whoever profits from deploying the system answers for its "
            "harms, whether or not they were at fault. <bookmark mark='c'/>Require meaningful human control: keep a "
            "person able to understand the system, to intervene, and to answer for it, and make that a requirement "
            "of design. <bookmark mark='d'/>Or ask whether the machine itself could ever be responsible. On "
            "Strawson's view, blame is an attitude toward a participant in our relationships, and whether a "
            "machine could be one returns us to Part 31's question about minds. <bookmark mark='e'/>Fair machines "
            "come in Part 41, and aligned reasoners in Part 42."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
