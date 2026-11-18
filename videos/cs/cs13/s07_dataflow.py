from __future__ import annotations

import itertools

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, DEMO_POS_SMALL, FUNC, HEAD, NO, PART, YES, cfg_view, grid_table,
                                   load, mono)


def setstr(xs):
    return "{" + ", ".join(x.replace("%", "") for x in xs) + "}"


class Dataflow(WatchScene):
    def construct(self):
        self.card()
        self.liveness()
        self.iterate()
        self.lattice()

    def card(self):
        self.chapter(6, r"Dataflow analysis and fixed points", r"What is true at each point, on every path?", lit=(1973,), extra=((1973, r"Kildall: \ dataflow on lattices"),), part=PART, said="Chapter six. Dataflow analysis and fixed points.")

    def liveness(self):
        self.ask(r"Liveness: is this value used later? \\ Which way does the information flow?", [r"forward",
                 r"backward"], 1,
                 say="Liveness asks whether a value will be used later. Does that information flow forward through the program, "
                     "or backward?",
                 reveal="Backward, from each use towards the definitions.")
        head = label(r"Liveness: \ will this value be needed?", font_size=34).to_edge(UP, buff=0.3)
        defn = label(r"$x$ is \textbf{live} at a point if some path from there uses $x$ before assigning it",
                     font_size=23, color=GREY_A).next_to(head, DOWN, buff=0.35)
        eqs = VGroup(
            MathTex(r"\mathrm{OUT}(b) = \bigcup_{s \,\in\, \mathrm{succ}(b)} \mathrm{IN}(s)", font_size=36),
            MathTex(r"\mathrm{IN}(b) = \mathrm{use}(b) \;\cup\; \big(\mathrm{OUT}(b) - \mathrm{def}(b)\big)",
                    font_size=36),
        ).arrange(DOWN, buff=0.35).next_to(defn, DOWN, buff=0.5)
        notes = VGroup(
            label(r"$\mathrm{use}(b)$: \ read in $b$ before any assignment in $b$; \ \ $\mathrm{def}(b)$: \ "
                  r"assigned in $b$", font_size=20, color=GREY_A),
            label(r"information flows \textbf{backward}: \ from uses to the definitions before them", font_size=21,
                  color=CTRL),
            label(r"why: \ a register holding a dead value is free for something else \ (chapter 11)",
                  font_size=21, color=FUNC),
        ).arrange(DOWN, buff=0.2).next_to(eqs, DOWN, buff=0.5)
        with self.voiceover("The compiler's main tool for reasoning about a whole function is dataflow analysis. The first example is liveness. <bookmark mark='a'/> A variable is live at a point if some path from that point uses it before assigning it again. Its current value might still be needed. <bookmark mark='b'/> Two equations say this for every block. A variable is live at the end of b if it is live at the start of some successor. <bookmark mark='c'/> And it is live at the start of b if b uses it before assigning it, or it is live at the end and b does not assign it. <bookmark mark='d'/> Information flows backward here, from each use to the definitions before it. <bookmark mark='e'/> The answer matters for register allocation: a register holding a value that is no longer live is free for something else.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(defn), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Write(eqs[0]))
            vo.wait_until('c')
            self.play(Write(eqs[1]), FadeIn(notes[0]))
            vo.wait_until('d')
            self.play(FadeIn(notes[1]))
            vo.wait_until('e')
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def iterate(self):
        df = load("dataflow")
        L = df["liveness"]
        head = label(r"Solving them: \ iterate until nothing changes", font_size=32).to_edge(UP, buff=0.3)
        cfg = cfg_view(load("ir")["func"], DEMO_POS_SMALL, size=14, lines=False, at=LEFT * 2.0 + DOWN * 0.35,
                       back_pad=2.0)
        B = cfg.blocks
        side = {"then5": LEFT, "entry": RIGHT, "body2": RIGHT, "else7": RIGHT, "endif6": RIGHT, "endwhile3": UP}

        def tag(b, xs, c):
            t = mono("IN " + setstr(xs), 14, c)
            box = B[b].box
            if b == "while1":      # below and to the right: clear of the back edge and of the edge to endwhile3
                return t.next_to(box, DOWN, buff=0.06).align_to(box, LEFT).shift(RIGHT * (box.width + 0.15))
            return t.next_to(box, side[b], buff=0.15)
        tags = {b: tag(b, [], CTRL) for b in B}
        cnt = label(r"updates: \ 0", font_size=22, color=GREY_A).to_corner(UR, buff=0.5).shift(DOWN * 0.6)
        start = label(r"start: \ every set empty", font_size=20, color=GREY_A).next_to(cnt, DOWN, buff=0.2)
        start.align_to(cnt, RIGHT)
        changes = len(L["trace"])
        done = VGroup(
            label(rf"{L['visits']} block visits, \ {changes} of them changed something", font_size=20, color=YES),
            label(r"a final sweep with no change: \ a fixed point", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(DOWN * 2.2)
        with self.voiceover(
            "The equations refer to each other around the loop, so we solve them the way we found dominators. "
            "<bookmark mark='a'/> Start with every set empty. Visit the blocks, backward, and apply the equations; "
            "whenever a block's set grows, its predecessors must be visited again. <bookmark mark='b'/> The exit "
            "block uses s. Endif uses i. Else uses s and i. Then uses a, s and i. The body adds nothing new to "
            "that, and the loop test adds n. The entry assigns s and i, so only a and n are live on entry: they "
            "are the parameters. <bookmark mark='c'/> But the sets just grown at the loop test flow back round the "
            "loop, to endif, then and else, which all grow again. One more sweep changes nothing. <bookmark "
            "mark='d'/> Fourteen visits, twelve of which changed something, and the answer is a fixed point of the "
            "equations: apply them once more and every set stays the same."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cfg))
            vo.wait_until("a")
            self.play(*[FadeIn(t) for t in tags.values()], FadeIn(cnt), FadeIn(start))
            vo.wait_until("b")
            for k, (b, IN, OUT) in enumerate(L["trace"]):
                if k == 7:
                    vo.wait_until("c")
                new = tag(b, IN, YES)
                nc = label(rf"updates: \ {k + 1}", font_size=22, color=GREY_A).move_to(cnt, aligned_edge=RIGHT)
                self.play(B[b].box.animate.set_fill(HEAD, 0.5), Transform(tags[b], new), Transform(cnt, nc),
                          run_time=0.6)
                self.play(B[b].box.animate.set_fill(DATA, 0.15), tags[b].animate.set_color(CTRL), run_time=0.25)
            vo.wait_until("d")
            self.play(FadeIn(done))
        self.wait(0.4)
        self.clear_scene()


    def lattice(self):
        df = load("dataflow")
        head = label(r"Why it stops: \ the facts form a lattice", font_size=34).to_edge(UP, buff=0.3)
        vars_ = ["a", "i", "n", "s"]
        subsets = [frozenset(c) for k in range(5) for c in itertools.combinations(vars_, k)]
        pos = {}
        for k in range(5):
            level = [s for s in subsets if len(s) == k]
            for j, s in enumerate(level):
                pos[s] = np.array([(j - (len(level) - 1) / 2) * 1.45 - 2.7, -2.7 + 1.25 * k, 0])
        nodes = {s: mono(setstr(sorted(s)), 14, GREY_B).move_to(pos[s]) for s in subsets}
        edges = VGroup(*[Line(nodes[a].get_top(), nodes[b].get_bottom(), color=GREY_D, stroke_width=1.2, buff=0.05)
                         for a in subsets for b in subsets if len(b) == len(a) + 1 and a < b])
        # IN(endif6) over the iteration: {} -> {i} -> {a, i, n, s}
        chain = [frozenset(), frozenset({"i"}), frozenset(vars_)]
        hops = VGroup(*[Arrow(nodes[a].get_center(), nodes[b].get_center(), buff=0.25, color=YES, stroke_width=4)
                        for a, b in zip(chain, chain[1:])])
        side = VGroup(
            label(r"sets of variables, \ ordered by $\subseteq$", font_size=21, color=GREY_A),
            label("bottom initialization + monotone updates: sets only grow", font_size=21, color=GREY_A),
            label(r"\texttt{IN(endif6)}: \ $\{\} \to \{i\} \to \{a, i, n, s\}$", font_size=21, color=YES),
            label("at most four strict additions to a variable set", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.3)
        with self.voiceover("Why does this liveness iteration stop? Kildall's framework makes the reason precise. <bookmark mark='a'/> The possible sets of four live variables form a lattice with sixteen elements, ordered by inclusion. Empty is bottom; all four variables are top. <bookmark mark='b'/> Each transfer function is monotone: enlarging the incoming facts cannot shrink its result. Because we start at bottom and revisit affected equations, induction shows that our successive facts only grow. Monotone does not mean an arbitrary starting value must grow. <bookmark mark='c'/> Endif's set grows from empty, to i alone, to all four variables. <bookmark mark='d'/> There can be at most four strict additions to any set. A fair worklist therefore terminates on this finite-height lattice, and an empty worklist means every equation is satisfied.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Create(edges), *[FadeIn(n) for n in nodes.values()], FadeIn(side[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(side[1]))
            vo.wait_until('c')
            self.play(FadeIn(side[2]), nodes[chain[0]].animate.set_color(YES))
            for h, s in zip(hops, chain[1:]):
                self.play(GrowArrow(h), nodes[s].animate.set_color(YES))
            vo.wait_until('d')
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()
        self.checkpoint(
            [(r"What does SSA give the optimizer?", r"One definition per name: def-use links are pointers"),
             (r"Why does a dataflow iteration terminate?", r"Monotone updates on a lattice of finite height")],
            narration="Checkpoint. What does SSA give the optimizer? And why does a dataflow iteration always stop?",
            answers_narration="One definition per name, so following a value is following a pointer. And each update only "
                              "moves up a lattice of finite height.")

