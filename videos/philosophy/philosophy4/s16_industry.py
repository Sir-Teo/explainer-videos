from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


class Industry(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Model checking at work", r"Where does this logic run every day?", lit=(1994,),
                            part=PART)
        with self.voiceover("Chapter fifteen. Model checking at work."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.hardware()
        self.bdd()
        self.software()
        self.limits()

    def hardware(self):
        hcs = VGroup(history_card(1994, r"the Pentium FDIV bug", r"a division error in a lookup table; \ Intel took "
                                  r"a \$475 million charge", width=6.0, color=BAD),
                     history_card(r"1990s--", r"formal verification of chips", r"model checking and theorem proving "
                                  r"become part of processor design", width=6.0, color=HIST)).arrange(
            RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        rows = VGroup(label(r"SMV (McMillan 1992): \ binary decision diagrams, \ $10^{20}$ states and more", font_size=24),
                      label(r"bounded model checking (Biere et al.\ 1999): \ temporal logic $\to$ SAT \ (Part 2)",
                            font_size=24),
                      label(r"Intel, AMD, Arm, Nvidia: \ floating-point units and cache protocols verified before "
                            r"silicon", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.9, 0])
        with self.voiceover(
            "The first big customer was hardware. <bookmark mark='a'/>In 1994 a missing entry in a lookup table made "
            "Intel's Pentium divide wrongly, in rare cases, and the recall cost Intel four hundred and seventy-five "
            "million dollars. <bookmark mark='b'/>The industry turned to formal verification. <bookmark mark='c'/>"
            "Kenneth McMillan's symbolic model checker represented sets of states as binary decision diagrams, "
            "checking systems with more states than there are grains of sand. Bounded model checking, from Part 2, "
            "translates temporal formulas into SAT. Today processors, their floating-point units and their cache "
            "protocols are checked against temporal specifications before they are made."
        ) as vo:
            self.play(FadeIn(hcs[0], shift=DOWN * 0.2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(hcs[1], shift=DOWN * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.4), run_time=3)
        self.clear_scene()

    def software(self):
        head = label(r"Software and systems", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"SPIN \ (Holzmann)", font_size=26, color=GOAL),
                   label(r"LTL model checking of protocols; \ flight software at NASA", font_size=22, color=GREY_A)),
            VGroup(label(r"SLAM and Static Driver Verifier \ (Microsoft, 2000s)", font_size=26, color=GOAL),
                   label(r"checks Windows device drivers against temporal rules for the kernel API", font_size=22,
                         color=GREY_A)),
            VGroup(label(r"TLA$^+$ at Amazon \ (Newcombe et al.\ 2015)", font_size=26, color=GOAL),
                   label(r"designs of DynamoDB and S3 specified and checked; \ a bug that needed a 35-step trace",
                         font_size=22, color=GREY_A)),
            VGroup(label(r"seL4 (2009) \ and CompCert", font_size=26, color=GOAL),
                   label(r"an operating-system kernel and a C compiler, \ proved correct in proof assistants",
                         font_size=22, color=GREY_A)))
        for r in rows:
            r.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Software followed. <bookmark mark='a'/>Gerard Holzmann's SPIN checks protocols against LTL "
            "specifications, and has been used on flight software at NASA. <bookmark mark='b'/>Microsoft's Static "
            "Driver Verifier checks Windows device drivers against temporal rules for the kernel's interface. "
            "<bookmark mark='c'/>At Amazon, engineers specified the designs of DynamoDB and S3 in Leslie Lamport's "
            "temporal logic TLA plus, and the model checker found subtle bugs, one of them needing a thirty-five-step "
            "trace to show. <bookmark mark='d'/>And whole systems have been proved correct: the seL4 operating-system "
            "kernel, and the CompCert C compiler."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def limits(self):
        rows = VGroup(
            label(r"state explosion: \ $n$ processes, $k$ states each: \ $k^n$ states", font_size=28, color=BAD),
            label(r"answers: \ symbolic sets, \ partial-order reduction, \ abstraction, \ bisimulation (Chapter 7)",
                  font_size=24, color=GREY_A),
            label(r"a check is only as good as its specification: \ who checks the formula?", font_size=28,
                  color=GOAL),
            label(r"Part 42: \ specifying what we want from machines that reason", font_size=24,
                  color=GREY_A)).arrange(DOWN, buff=0.4).move_to([0, 0.2, 0])
        with self.voiceover(
            "Two limits remain. <bookmark mark='a'/>The first is state explosion: n processes with k states each "
            "make k to the n global states. <bookmark mark='b'/>The field's answers are symbolic representations, "
            "reductions that skip equivalent interleavings, abstraction, and the bisimulation minimization of Chapter "
            "seven. <bookmark mark='c'/>The second limit is philosophical. A model checker proves that a system "
            "satisfies a formula; it cannot tell you whether the formula says what you meant. <bookmark mark='d'/>"
            "That problem, saying exactly what we want, returns at the very end of this series, in Part 42."
        ) as vo:
            for mk, r in zip("abcd", rows):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.15))
        self.clear_scene()

    def bdd(self):
        d = load("bdd")
        rows = d["rows"]
        hc = history_card(1986, r"Randal Bryant", r"reduced ordered binary decision diagrams", width=5.8,
                          color=HIST).to_corner(UL, buff=0.35)
        f = MathTex(r"(x_1 \land y_1) \lor (x_2 \land y_2) \lor \cdots \lor (x_n \land y_n)", font_size=36,
                    color=GOAL).next_to(hc, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        what = label(r"a BDD: \ a decision tree with every repeated subtree shared, \ under a fixed order of variables",
                     font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.2).align_to(f, LEFT)
        n = [r["n"] for r in rows]
        good = bar_row([r["good"] for r in rows], [rf"$n = {k}$: \ $x_1 y_1 x_2 y_2 \dots$" for k in n],
                       [OK] * len(rows), width=2.6, height=0.26, font_size=20, vmax=max(r["bad"] for r in rows))
        bad = bar_row([r["bad"] for r in rows], [rf"$n = {k}$: \ $x_1 x_2 \dots y_1 y_2 \dots$" for k in n],
                      [BAD] * len(rows), width=2.6, height=0.26, font_size=20, vmax=max(r["bad"] for r in rows))
        both = VGroup(good, bad).arrange(RIGHT, buff=0.8).move_to([0.6, -1.6, 0])
        if both.width > 13.2:
            both.width = 13.2
        lab = VGroup(label(r"nodes, \ interleaved order: \ $2n + 2$", font_size=22, color=OK).next_to(good, UP,
                                                                                                    buff=0.2),
                     label(r"nodes, \ separated order: \ $2^{n+1}$", font_size=22, color=BAD).next_to(bad, UP,
                                                                                                  buff=0.2))
        with self.voiceover(
            "The idea that made hardware verification practical is a data structure. <bookmark mark='a'/>In 1986 "
            "Randal Bryant introduced reduced ordered binary decision diagrams: a decision tree for a Boolean "
            "function, with the variables tested in a fixed order and every repeated piece shared. Sets of states "
            "become such diagrams, and the fixed points of model checking become operations on them. "
            "<bookmark mark='b'/>Their size depends dramatically on the order. Take this function, built from n "
            "pairs. The Reasoner built its diagram both ways. <bookmark mark='c'/>Testing each x right before its "
            "partner y, the diagram grows by two nodes per pair. Testing all the x's first, it doubles with every "
            "pair, because the diagram must remember every x before it sees any y. <bookmark mark='d'/>Finding a "
            "good order is itself hard, and much of the engineering of model checkers lies there."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(what))
            vo.wait_until("b")
            self.play(FadeIn(lab))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r.name), GrowFromEdge(r.bar, LEFT), FadeIn(r.value))
                                    for r in good], lag_ratio=0.15),
                      LaggedStart(*[AnimationGroup(FadeIn(r.name), GrowFromEdge(r.bar, LEFT), FadeIn(r.value))
                                    for r in bad], lag_ratio=0.15), run_time=3)
            vo.wait_until("d")
            self.play(*[Indicate(r.value, color=BAD) for r in bad[-2:]])
        self.clear_scene()
