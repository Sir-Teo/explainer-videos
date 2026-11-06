from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (HEAD, LAM, NO, PART, YES, curve, fit_right, grid_table, load, num)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.lincost()
        self.weak()
        self.waitfree()
        self.open_()

    def card(self):
        card = chapter_card(16, r"Frontier: \ checking concurrent programs", r"What is still unsolved?",
                            lit=(1997, 2010, 2011), extra=((1997, r"Gibbons and Korach"), (2010, r"Atig et al.: \ TSO"),
                                                           (2011, r"Attiya et al.: \ laws of order")), part=PART)
        with self.voiceover("Chapter sixteen. The frontier: checking concurrent programs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lincost(self):
        d = load("frontier")
        head = label(r"Checking linearizability is hard", font_size=34).to_edge(UP, buff=0.3)
        lin = d["lin"]
        ax = Axes(x_range=[0, 85, 20], y_range=[0, 6, 1], x_length=6.0, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.1).shift(DOWN * 0.3)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (20, 40, 60, 80)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.08)
                      for k in range(0, 7)])
        xl = label(r"operations in the history \ (4 threads, \ a queue)", font_size=17, color=GREY_A).next_to(
            xt, DOWN, buff=0.1)
        yl = label(r"search steps \ (log)", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        med = curve(ax, [r["ops"] for r in lin], [math.log10(max(1, r["median"])) for r in lin], YES)
        mx = curve(ax, [r["ops"] for r in lin], [math.log10(max(1, r["max"])) for r in lin], NO)
        cap = DashedLine(ax.c2p(0, math.log10(d["cap"])), ax.c2p(85, math.log10(d["cap"])), color=GREY_B,
                         stroke_width=1.5)
        k1 = label(r"median of 20", font_size=16, color=YES).next_to(ax.c2p(70, math.log10(lin[-2]["median"])),
                                                                      DOWN, buff=0.1)
        k2 = label(r"worst of 20 \ (capped)", font_size=16, color=NO).next_to(cap, UP, buff=0.05).align_to(cap, LEFT)
        k2.shift(RIGHT * 0.8)
        notes = VGroup(
            label(r"Gibbons and Korach \ (1997): \\ \textbf{NP-complete} in general", font_size=20, color=NO),
            label(r"tractable cases: \ a fixed number of \\ threads; \ queues and stacks with \\ distinct values "
                  r"\ (Bouajjani et al. 2015)", font_size=20, color=YES),
            label(r"in practice: \ Knossos, \ Porcupine \\ (Jepsen's database testers) \ split \\ histories "
                  r"by key and time", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "The first frontier is checking. <bookmark mark='a'/> Our linearizability checker's search grows quickly "
            "with the length of the history. The median stays modest, but the worst of twenty random queue histories "
            "hits our limit of three hundred thousand steps by sixty operations. <bookmark mark='b'/> This is not a "
            "weakness of our code. Gibbons and Korach proved in 1997 that deciding linearizability is NP-complete. "
            "<bookmark mark='c'/> There are tractable special cases. With a fixed number of threads it is polynomial, "
            "and for queues and stacks whose values are all distinct, Bouajjani and his colleagues showed that a few "
            "small bad patterns explain every violation. <bookmark mark='d'/> The testers used on real databases, "
            "Knossos and Porcupine, survive by splitting a history by key and by time."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(med), Create(mx), Create(cap), FadeIn(k1), FadeIn(k2), run_time=2.0)
            for mk, n_ in zip("bcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def weak(self):
        t = load("tso")
        head = label(r"Verifying programs on weak memory", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        for model in ("sc", "tso", "pso"):
            r = next(x for x in t["rows"] if x["alg"] == "Peterson" and x["model"] == model and x["fence"] == "False")
            rows.append([model.upper(), num(r["states"]), r"safe" if r["ok"] else r"broken"])
        tab = grid_table([r"model", r"states, \ Peterson, \ 2 rounds", r"result"], rows, widths=[1.8, 4.4, 2.2],
                         row_h=0.5, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45)
        for i, r in enumerate(rows):
            tab.cells[i + 1][2].set_color(YES if r[2] == "safe" else NO)
        lines = VGroup(
            label(r"store buffers multiply the states: \ 1{,}487 under SC, \ 61{,}051 under PSO", font_size=21,
                  color=WHITE),
            label(r"unbounded buffers: \ reachability under TSO is decidable but non-primitive-recursive \ (Atig et "
                  r"al. 2010); \ for Power and Arm, \ harder still", font_size=21, color=NO),
            label(r"the tools: \ stateless model checking with partial-order reduction \ (Flanagan and Godefroid "
                  r"2005), \ GenMC, \ herd7", font_size=21, color=HEAD),
            label(r"and the gap: \ checking a full kernel, \ or a lock-free library, \ on Arm's real model", font_size=21,
                  color=LAM),
        ).arrange(DOWN, buff=0.16).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "The second frontier is weak memory. <bookmark mark='a'/> Store buffers multiply the state space: two "
            "rounds of Peterson's algorithm have under fifteen hundred states under sequential consistency, and sixty-"
            "one thousand under partial store order. <bookmark mark='b'/> With buffers of unbounded size, Atig and "
            "colleagues proved in 2010 that checking reachability under total store order is decidable, but with a "
            "complexity beyond any tower of exponentials; for the Power and Arm models it is harder still. <bookmark "
            "mark='c'/> Practical tools avoid exploring equivalent orders, by stateless model checking with "
            "partial-order reduction, and the best, such as GenMC, now handle the C and C plus plus model. <bookmark "
            "mark='d'/> Checking a whole kernel or a lock-free library on Arm's real model remains out of reach."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def waitfree(self):
        head = label(r"The price of strong guarantees", font_size=34).to_edge(UP, buff=0.3)
        items = VGroup(*[VGroup(label(t, font_size=24, color=c), label(s, font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08) for t, s, c in (
            (r"laws of order \ (Attiya et al., \ 2011)",
             r"linearizable sets, \ queues, \ counters must use an expensive fence or atomic in some operation: \ "
             r"provably", HEAD),
            (r"wait-free, \ fast \ (Kogan and Petrank, \ 2011--12)",
             r"a lock-free fast path, \ and a wait-free slow path when a thread is starved", YES),
            (r"universal constructions are slow",
             r"Herlihy's universality is a proof, \ not a recipe: \ $O(n)$ work per operation", NO),
            (r"testing with probability guarantees \ (PCT, \ Burckhardt et al. 2010)",
             r"random priorities find any bug of depth $d$ with probability at least $1 / (n k^{d-1})$", LAM),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The third frontier is the price of the strongest guarantees. <bookmark mark='a'/> Attiya and colleagues "
            "proved in 2011 that linearizable sets, queues and counters cannot avoid an expensive fence or atomic "
            "instruction in some operation: the cost of chapter five is a law, not an engineering failure. <bookmark "
            "mark='b'/> Wait-free structures were long thought too slow for practice, until Kogan and Petrank paired "
            "a lock-free fast path with a wait-free slow path taken only by a starving thread. <bookmark mark='c'/> "
            "Herlihy's universal construction proves that anything can be made wait-free, but its cost grows with the "
            "number of threads. <bookmark mark='d'/> And testing can come with guarantees: the PCT scheduler of "
            "Burckhardt and colleagues assigns random priorities, and finds any bug that needs d ordering constraints "
            "with a probability that can be computed in advance."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open problems", font_size=36).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"1. \ A semantics for relaxed atomics without out-of-thin-air values, \ that keeps the "
                  r"optimisations", font_size=22, color=WHITE),
            label(r"2. \ Inserting the fewest fences that make a program correct on a weak model", font_size=22,
                  color=WHITE),
            label(r"3. \ Which objects and histories make linearizability checking polynomial?", font_size=22,
                  color=WHITE),
            label(r"4. \ Wait-free data structures as fast as the best lock-free ones", font_size=22, color=WHITE),
            label(r"5. \ Verified lock-free libraries on Arm's memory model", font_size=22, color=WHITE),
            label(r"6. \ Correctness for persistent memory: \ what survives a crash mid-operation?", font_size=22,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        fit_right(items)
        star = label(r"$\bigstar$ \ the part's research problem takes a small case of the second", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Six open problems. <bookmark mark='a'/> A definition of relaxed atomics that rules out values from thin "
            "air without forbidding the optimisations compilers rely on. <bookmark mark='b'/> Finding the fewest "
            "fences that make a program correct on a given weak model. <bookmark mark='c'/> Exactly which objects and "
            "which kinds of history make linearizability checking tractable. <bookmark mark='d'/> Wait-free data "
            "structures as fast as the best lock-free ones. <bookmark mark='e'/> Verified lock-free libraries on "
            "Arm's real memory model. <bookmark mark='f'/> And for the new persistent memories, a notion of "
            "correctness that says what must survive a crash in the middle of an operation. <bookmark mark='g'/> "
            "This part's research problem takes a small, computable case of the second."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcdef", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
