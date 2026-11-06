from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (GREY_B, HEAD, LAM, NO, PART, T0C, T1C, T2C, YES, load, mono)


class Consensus(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.ladder()
        self.universal()
        self.valency()

    def card(self):
        card = chapter_card(12, r"Consensus numbers", r"Which atomic instructions are more powerful?", lit=(1991,),
                            extra=((1991, r"Herlihy: \ wait-free synchronization"),), part=PART)
        with self.voiceover("Chapter twelve. Consensus numbers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def problem(self):
        d = load("consensus")
        head = label(r"Consensus: \ agree on one of the proposals", font_size=34).to_edge(UP, buff=0.3)
        rules = VGroup(
            label(r"each of $n$ threads proposes a value, \ and decides one", font_size=22, color=WHITE),
            label(r"\textbf{agreement}: \ all decide the same; \ \textbf{validity}: \ it was someone's proposal",
                  font_size=22, color=WHITE),
            label(r"\textbf{wait-free}: \ each decides in a bounded number of its own steps, \ whatever the others do",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.4)
        tas = VGroup(mono("prop[me] = mine", 19, WHITE), mono("if (tas(&flag) == 0) decide(mine)", 19, YES),
                     mono("else decide(prop[other])", 19, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        cas = VGroup(mono("CAS(&decision, EMPTY, mine)", 19, YES), mono("decide(decision)", 19, WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08)
        tg = VGroup(label(r"with test-and-set:", font_size=20, color=LAM), tas).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.1)
        cg = VGroup(label(r"with compare-and-swap:", font_size=20, color=YES), cas).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
        VGroup(tg, cg).arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(rules, DOWN, buff=0.45)
        res = VGroup(
            label(rf"checked: \ test-and-set, \ 2 threads: \ agreement in all {d['tas2']['states']} states", font_size=20,
                  color=YES),
            label(r"3 threads: \ a loser cannot tell which of the other two won: \ broken", font_size=20, color=NO),
            label(rf"compare-and-swap, \ 3 threads: \ agreement in all {d['cas3']['states']} states \ (any $n$ works)",
                  font_size=20, color=YES),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Maurice Herlihy asked in 1991 which atomic instructions are more powerful than others, and found an "
            "exact answer through one problem: consensus. <bookmark mark='a'/> Each of n threads proposes a value and "
            "must decide one. All must decide the same value, and it must be one of the proposals. <bookmark "
            "mark='b'/> And it must be wait-free: each thread decides within a bounded number of its own steps, even "
            "if the others stop. No locks. <bookmark mark='c'/> With test-and-set, two threads can do it: write your "
            "proposal where the other can see it, then test-and-set a flag. The winner decides its own value, and the "
            "loser decides the winner's. The checker confirms agreement. <bookmark mark='d'/> But with three threads, "
            "a loser knows only that it lost, not which of the other two won, and the checker finds disagreement. "
            "<bookmark mark='e'/> Compare-and-swap does it for any number: the first to swap its value into an empty "
            "decision wins, and everyone reads the decision."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(rules[0], rules[1])))
            vo.wait_until("b")
            self.play(FadeIn(rules[2]))
            vo.wait_until("c")
            self.play(FadeIn(tg), FadeIn(res[0]))
            vo.wait_until("d")
            self.play(FadeIn(res[1]))
            vo.wait_until("e")
            self.play(FadeIn(cg), FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()

    def ladder(self):
        head = label(r"Herlihy's hierarchy", font_size=36).to_edge(UP, buff=0.3)
        rungs = [(r"1", r"atomic reads and writes", GREY_B),
                 (r"2", r"test-and-set, \ swap, \ fetch-and-add, \ queues, \ stacks", LAM),
                 (r"$2n-2$", r"$n$-register assignment", HEAD),
                 (r"$\infty$", r"compare-and-swap, \ load-linked / store-conditional", YES)]
        steps = VGroup()
        for k, (n, what, c) in enumerate(rungs):
            r = Rectangle(width=9.0, height=0.8, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.12)
            nl = MathTex(n.strip("$"), font_size=36, color=c)
            row = VGroup(r, nl.move_to(r.get_left() + RIGHT * 0.9), label(what, font_size=22, color=WHITE).move_to(
                r).shift(RIGHT * 0.7))
            row.move_to([0, -2.0 + 1.05 * k, 0])
            steps.add(row)
        cap = label(r"consensus number", font_size=18, color=GREY_A).next_to(steps[-1][1], UP, buff=0.25)
        lines = VGroup(
            label(r"an object's \textbf{consensus number}: \ the most threads for which it solves wait-free consensus",
                  font_size=21, color=WHITE),
            label(r"no object can implement one higher up, \ wait-free, \ however clever the program", font_size=21,
                  color=NO),
            label(r"\textbf{universality}: \ consensus for $n$ threads builds \textit{any} object for $n$ threads, "
                  r"\ wait-free", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.25)
        steps.shift(UP * 0.5)
        cap.next_to(steps[-1][1], UP, buff=0.15)
        with self.voiceover(
            "This gives every object a number: the most threads for which it can solve wait-free consensus. <bookmark "
            "mark='a'/> Plain reads and writes: one. They cannot even solve it for two. <bookmark mark='b'/> "
            "Test-and-set, swap, fetch-and-add, and even atomic queues and stacks: exactly two. <bookmark mark='c'/> "
            "Some exotic objects sit at numbers in between. <bookmark mark='d'/> And compare-and-swap, or the "
            "load-linked and store-conditional pair of Arm and RISC-V: infinity. <bookmark mark='e'/> The ladder is "
            "strict. No object can implement one with a higher number, wait-free, however clever the program. "
            "<bookmark mark='f'/> And at the top, Herlihy proved universality: with consensus for n threads, you can "
            "build a wait-free implementation of any object at all for n threads. That is why every modern processor "
            "provides compare-and-swap or its equivalent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=UP * 0.1))
            self.play(FadeIn(cap))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
            vo.wait_until("f")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def universal(self):
        head = label(r"Universality: \ a log of agreements", font_size=34).to_edge(UP, buff=0.3)
        cells = VGroup()
        ops = (r"enq(5)", r"deq()", r"enq(9)", r"?")
        for k, t in enumerate(ops):
            c = YES if k < 3 else GREY_B
            r = RoundedRectangle(width=1.9, height=1.1, corner_radius=0.1, stroke_color=c, stroke_width=2,
                                 fill_color=c, fill_opacity=0.12)
            g = VGroup(r, label(rf"consensus {k + 1}", font_size=16, color=GREY_A).next_to(r.get_top(), DOWN,
                                                                                        buff=0.08),
                       label(t, font_size=20, color=WHITE).move_to(r).shift(DOWN * 0.12))
            cells.add(g)
        cells.arrange(RIGHT, buff=0.5).move_to([0, 1.1, 0])
        links = VGroup(*[Arrow(cells[i].get_right(), cells[i + 1].get_left(), buff=0.05, color=GREY_B,
                               stroke_width=2) for i in range(3)])
        props = VGroup(*[label(t, font_size=17, color=c) for t, c in (
            (r"T1 proposes deq()", T0C), (r"T2 proposes enq(7)", T1C), (r"T3 proposes deq()", T2C))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(cells[3], DOWN, buff=0.3)
        lines = VGroup(
            label(r"every operation is first agreed: \ the threads run consensus on what goes in the next slot",
                  font_size=20, color=WHITE),
            label(r"each thread replays the agreed log on its own copy of a sequential queue: \ the state, \ and its "
                  r"answer", font_size=20, color=HEAD),
            label(r"wait-free by \textbf{helping}: \ winners also propose losers' operations, \ so nobody loses "
                  r"forever", font_size=20, color=YES),
            label(r"any object, \ from consensus alone; \ correct, \ but $O(n)$ work per operation: \ a proof, \ not "
                  r"a recipe", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How can consensus build any object at all? <bookmark mark='a'/> Keep a log of operations, one slot "
            "after another. To perform an operation, a thread proposes it for the next empty slot, and the threads run "
            "consensus to agree on which proposal fills that slot. <bookmark mark='b'/> Every thread can then replay "
            "the agreed log, in order, on its own private copy of an ordinary sequential object, and so knows the "
            "state and the answer to its own operation. <bookmark mark='c'/> A thread that keeps losing could starve, "
            "so winners also help: they propose operations that others announced but have not yet placed. That "
            "makes it wait-free. <bookmark mark='d'/> It works for every object, which is the point of the theorem. "
            "It is also slow, with work growing with the number of threads, so it is a proof of possibility rather "
            "than a recipe."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in cells[:3]], lag_ratio=0.3), Create(links[:2]))
            vo.wait_until("a")
            self.play(FadeIn(cells[3]), Create(links[2]), FadeIn(props), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def valency(self):
        d = load("consensus")
        head = label(r"Why registers cannot do it: \ valency", font_size=34).to_edge(UP, buff=0.3)
        root = VGroup(Circle(radius=0.4, color=HEAD, fill_color=HEAD, fill_opacity=0.25),
                      label(r"bivalent", font_size=16, color=WHITE)).move_to([0, 1.6, 0])
        a = VGroup(Circle(radius=0.4, color=T0C, fill_color=T0C, fill_opacity=0.25),
                   label(r"0-valent", font_size=16, color=WHITE)).move_to([-2.4, -0.2, 0])
        b = VGroup(Circle(radius=0.4, color=T1C, fill_color=T1C, fill_opacity=0.25),
                   label(r"1-valent", font_size=16, color=WHITE)).move_to([2.4, -0.2, 0])
        ea = Arrow(root.get_bottom(), a.get_top(), buff=0.05, color=T0C, stroke_width=2.5)
        eb = Arrow(root.get_bottom(), b.get_top(), buff=0.05, color=T1C, stroke_width=2.5)
        la = label(r"thread 0 steps", font_size=17, color=T0C).next_to(ea, LEFT, buff=0.1)
        lb = label(r"thread 1 steps", font_size=17, color=T1C).next_to(eb, RIGHT, buff=0.1)
        notes = VGroup(
            label(r"a state is \textbf{bivalent} if both decisions are still reachable; \ some start must be",
                  font_size=20, color=WHITE),
            label(r"follow bivalent states to a \textbf{critical} one: \ each thread's next step decides it",
                  font_size=20, color=HEAD),
            label(r"those two steps are reads or writes: \ either they commute, \ or one overwrites the other, \ and "
                  r"a thread running alone cannot tell which happened", font_size=20, color=NO),
            label(rf"our checker on a register protocol: \ decisions {d['reg2']['finals'][-1][0]} and {d['reg2']['finals'][-1][1]}: \ disagreement",
                  font_size=20, color=NO),
            label(r"the same argument, \ with messages and crashes, \ is Fischer, Lynch and Paterson's theorem \ "
                  r"(Part 38)", font_size=20, color=YES),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Why can't reads and writes solve consensus for two threads? The proof is a beautiful argument about "
            "valency. <bookmark mark='a'/> Call a state bivalent if both decisions are still possible from it. Some "
            "initial state must be bivalent, because which proposal wins depends on the schedule. <bookmark "
            "mark='b'/> Follow bivalent states as far as possible, and you reach a critical state, where thread zero's "
            "next step would make the decision zero, and thread one's next step would make it one. <bookmark "
            "mark='c'/> But those steps are reads or writes. Two reads, or steps on different registers, commute, so "
            "the order cannot matter. If one is a write that overwrites the other's, then a thread running on alone "
            "afterwards sees the same memory in both cases and must decide the same way. Either way, a contradiction. "
            "<bookmark mark='d'/> Our checker shows it on one natural protocol: write your proposal, read the other's, "
            "take the smaller one seen. Some schedule makes them disagree. <bookmark mark='e'/> The same argument, "
            "applied to messages and crashing computers, is the famous impossibility result of Fischer, Lynch and "
            "Paterson, which Part 38 meets."
        ) as vo:
            self.play(FadeIn(head), FadeIn(root))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(ea), GrowArrow(eb), FadeIn(a), FadeIn(b), FadeIn(la), FadeIn(lb), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()
