from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, DEMO_POS, DEMO_POS_SMALL, FUNC, HEAD, NO, PART, YES, cfg_view,
                                   code, load, mono)


class SSA(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.phi()
        self.placement()
        self.rename()
        self.payoff()

    def card(self):
        card = chapter_card(5, r"Static single assignment", r"What if every name were assigned exactly once?",
                            lit=(1991,), extra=((1991, r"SSA form; \ the Web; \ Linux"),), part=PART)
        with self.voiceover("Chapter five. Static single assignment."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def problem(self):
        head = label(r"Which $s$ is this?", font_size=36).to_edge(UP, buff=0.3)
        before = code(["s = 0", "s = s + 3", "t = s * 2", "s = t - 1", "u = s + t"], size=22, color=CODE)
        after = code(["s1 = 0", "s2 = s1 + 3", "t1 = s2 * 2", "s3 = t1 - 1", "u1 = s3 + t1"], size=22, color=YES)
        VGroup(before, after).arrange(RIGHT, buff=2.2).next_to(head, DOWN, buff=0.6)
        arr = Arrow(before.get_right(), after.get_left(), buff=0.3, color=GREY_B)
        q = label(r"one definition per name: \ every use points at exactly one place", font_size=24,
                  color=HEAD).next_to(VGroup(before, after), DOWN, buff=0.6)
        links = VGroup(*[CurvedArrow(after[a].get_right() + RIGHT * 0.05, after[b].get_right() + RIGHT * 0.05,
                                     angle=-1.2, color=FUNC, stroke_width=1.6, tip_length=0.12)
                         for a, b in ((2, 4), (3, 4))])
        join = label(r"but at a join, \ which definition arrives depends on the path taken", font_size=22,
                     color=NO).next_to(q, DOWN, buff=0.35)
        with self.voiceover(
            "In our IR the variable s is assigned in three places: in the entry, in then, and in else. To know "
            "anything about a use of s, the compiler must first work out which assignments could have produced its "
            "value. <bookmark mark='a'/> In straight-line code there is a simple cure. <bookmark mark='b'/> Give "
            "every assignment a fresh name, s one, s two, s three, and rewrite each use to the name that reaches "
            "it. <bookmark mark='c'/> Now every name is defined exactly once, and every use points at exactly one "
            "definition. Facts about s three are facts about one instruction, true wherever s three appears. "
            "<bookmark mark='d'/> The difficulty is where control flow joins. After an if, which name holds s? It "
            "depends on which branch ran."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(before))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(after))
            vo.wait_until("c")
            self.play(FadeIn(q), Create(links))
            vo.wait_until("d")
            self.play(FadeIn(join))
        self.wait(0.3)
        self.clear_scene()

    def phi(self):
        s = load("ssa")
        cfg = cfg_view(s["after"], DEMO_POS, size=12, at=RIGHT * 2.6 + DOWN * 0.1)
        B = cfg.blocks
        head = label(r"The $\phi$ function", font_size=32).to_corner(UL, buff=0.35)
        expl = VGroup(
            mono("%s.5 = φ(%s.4:then5, %s.3:else7)", 15, HEAD),
            label(r"``$s.4$ if we came from \texttt{then5}, \ $s.3$ if from \texttt{else7}''", font_size=19,
                  color=GREY_A),
            label(r"not a real instruction: \ a note about edges", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(head, DOWN, buff=0.45).align_to(head, LEFT)
        loopphi = VGroup(
            mono("%i.2 = φ(%i.1:entry, %i.3:endif6)", 15, HEAD),
            label(r"at the loop header: \ the first time round, \ or every later time", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(expl, DOWN, buff=0.5).align_to(head, LEFT)
        stats = label(rf"{s['stats']['phis']} $\phi$s \ for \ {s['stats']['variables']} variables", font_size=22,
                      color=YES).next_to(loopphi, DOWN, buff=0.5).align_to(head, LEFT)

        def phis(b):
            return VGroup(*[l for l, txt in zip(B[b].lines, [x for x in next(bb for bb in s["after"]["blocks"]
                                                                            if bb["label"] == b)["ins"]])
                            if "φ" in txt])
        with self.voiceover(
            "SSA's answer is a new kind of instruction, the phi function. <bookmark mark='a'/> Here is total "
            "in SSA form. At endif, s dot five is defined as phi of s dot four from then, and s dot three from "
            "else. <bookmark mark='b'/> Read it as: s dot five is s dot four if control arrived from then, and s dot "
            "three if it arrived from else. A phi is not an instruction any machine has. It is a note about "
            "edges, and before the back end runs it will become copies. <bookmark mark='c'/> The loop header "
            "needs phis too. i dot two is i dot one the first time we reach the test, coming from the entry, and "
            "i dot three every later time, coming back around from endif. The same holds for s. <bookmark "
            "mark='d'/> Three phis in all, for two variables."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cfg))
            vo.wait_until("a")
            self.play(Indicate(phis("endif6"), color=HEAD, scale_factor=1.3))
            self.play(FadeIn(expl[0]))
            vo.wait_until("b")
            self.play(FadeIn(expl[1:]))
            self.play(cfg.edges[("then5", "endif6")].animate.set_color(YES))
            self.play(cfg.edges[("else7", "endif6")].animate.set_color(FUNC))
            vo.wait_until("c")
            self.play(Indicate(phis("while1"), color=HEAD, scale_factor=1.3), FadeIn(loopphi))
            self.play(cfg.edges[("entry", "while1")].animate.set_color(YES),
                      cfg.edges[("endif6", "while1")].animate.set_color(FUNC))
            vo.wait_until("d")
            self.play(FadeIn(stats))
        self.wait(0.3)
        self.clear_scene()

    def placement(self):
        d = load("dom")
        head = label(r"Where do $\phi$s go? \ \ The iterated dominance frontier", font_size=32).to_edge(UP,
                                                                                                    buff=0.3)
        cfg = cfg_view(load("ir")["func"], DEMO_POS_SMALL, size=14, lines=False, at=LEFT * 4.2 + DOWN * 0.3)
        B = cfg.blocks
        steps = VGroup(
            label(r"$s$ is assigned in \ \texttt{entry}, \ \texttt{then5}, \ \texttt{else7}", font_size=21,
                  color=GREY_A),
            label(r"$\mathrm{DF}(\texttt{then5}) = \mathrm{DF}(\texttt{else7}) = \{\texttt{endif6}\}$: \ "
                  r"a $\phi$ for $s$ there", font_size=21, color=YES),
            label(r"that $\phi$ assigns $s$ too: \ $\mathrm{DF}(\texttt{endif6}) = \{\texttt{while1}\}$: \ "
                  r"a $\phi$ there", font_size=21, color=YES),
            label(r"$i$ is assigned in \ \texttt{entry}, \ \texttt{endif6}: \ a $\phi$ at \texttt{while1}",
                  font_size=21, color=CTRL),
            label(r"repeat until no new $\phi$: \ the \textit{iterated} frontier", font_size=21, color=HEAD),
            label(r"keep only those where the variable is still live: \ \textit{pruned} SSA", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.3, -0.2, 0])
        cite = label(r"Cytron, Ferrante, Rosen, Wegman, Zadeck \ (IBM, 1991)", font_size=18,
                     color=GREY_B).to_edge(DOWN, buff=0.3)
        tags = {}

        def tag(b, txt, c):
            t = MathTex(txt, font_size=26, color=c).next_to(B[b].box, RIGHT if b != "then5" else LEFT, buff=0.1)
            return t
        with self.voiceover(
            "Where must the phis go? Not at every join: that would be correct but wasteful. <bookmark mark='a'/> "
            "The answer uses the previous chapter. s is assigned in the entry, in then and in else. <bookmark "
            "mark='b'/> The frontier of then is endif, and so is the frontier of else. A definition from then meets "
            "a definition from elsewhere exactly there, so endif gets a phi for s. <bookmark mark='c'/> But that "
            "phi is itself a new assignment of s, so its own frontier needs one too: the loop header, while one. "
            "<bookmark mark='d'/> i is assigned in the entry and in endif, whose frontier is while one again. "
            "<bookmark mark='e'/> Repeat until no new phi appears: the iterated dominance frontier. <bookmark "
            "mark='f'/> And keep only the phis whose variable is still live there, which is called pruned SSA. "
            "This is the algorithm of Cytron, Ferrante, Rosen, Wegman and Zadeck at IBM, published in 1991, and "
            "almost every optimizing compiler since has used it or a descendant of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cfg))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), *[B[k].box.animate.set_fill(YES, 0.45) for k in ("entry", "then5", "else7")])
            vo.wait_until("b")
            t1 = tag("endif6", r"\phi_s", YES)
            self.play(FadeIn(steps[1]), FadeIn(t1), B["endif6"].box.animate.set_stroke(YES, 3.5))
            vo.wait_until("c")
            t2 = MathTex(r"\phi_s", font_size=26, color=YES).next_to(B["while1"].box, UP, buff=0.05).shift(
                RIGHT * 0.55)
            self.play(FadeIn(steps[2]), FadeIn(t2), B["while1"].box.animate.set_stroke(YES, 3.5))
            vo.wait_until("d")
            t3 = MathTex(r"\phi_i", font_size=26, color=CTRL).next_to(t2, RIGHT, buff=0.08)
            self.play(FadeIn(steps[3]), FadeIn(t3))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
            vo.wait_until("f")
            self.play(FadeIn(steps[5]), FadeIn(cite))
        self.wait(0.3)
        self.clear_scene()

    def rename(self):
        head = label(r"Renaming: \ one walk down the dominator tree", font_size=32).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"keep a stack of names for each variable", font_size=22, color=GREY_A),
            label(r"entering a block: \ each definition pushes a fresh name", font_size=22, color=GREY_A),
            label(r"each use takes the name on top of the stack", font_size=22, color=GREY_A),
            label(r"fill in the $\phi$ operands of the block's successors", font_size=22, color=GREY_A),
            label(r"visit the children in the dominator tree; \ on the way back, pop", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        stack_s = VGroup(*[VGroup(Rectangle(width=1.3, height=0.42, stroke_color=YES, fill_color=YES,
                                            fill_opacity=0.15), mono(n, 16, WHITE)) for n in
                           ("s.1", "s.2", "s.4")])
        for g in stack_s:
            g[1].move_to(g[0])
        stack_s.arrange(UP, buff=0.0).move_to([4.6, -1.0, 0])
        st_t = label(r"the stack for $s$, \ inside \texttt{then5}", font_size=18, color=YES).next_to(stack_s, DOWN,
                                                                                                  buff=0.15)
        why = label(r"a name defined in $d$ is visible exactly in the blocks $d$ dominates", font_size=22,
                    color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "With the phis placed, the names are filled in by a single walk. <bookmark mark='a'/> Keep a stack of "
            "names for each variable. Entering a block, each definition pushes a fresh name, and each use takes "
            "whatever name is on top. <bookmark mark='b'/> At the end of the block, fill in this block's operand "
            "of each phi in its successors. Then visit the block's children in the dominator tree, and pop the "
            "names on the way back out. <bookmark mark='c'/> Inside then five the stack for s holds s dot one from "
            "the entry, s dot two from the header's phi, and on top s dot four, then's own definition. <bookmark "
            "mark='d'/> Why the dominator tree? Because a definition in d is available, along every path, exactly "
            "in the blocks that d dominates. The tree is the program's scope structure, recovered from its graph."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in steps[:3]], lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in steps[3:]], lag_ratio=0.4), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(st_t))
            for g in stack_s:
                self.play(FadeIn(g, shift=DOWN * 0.2), run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    def payoff(self):
        lv = load("llvm")
        head = label(r"Why SSA pays", font_size=36).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"every use has one definition: \ the def--use graph is just pointers", font_size=22,
                  color=GREY_A),
            label(r"a fact about a name holds everywhere the name appears", font_size=22, color=GREY_A),
            label(r"so analyses run on the sparse def--use graph, \ not over every block", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        k = lv["ssa"].index("3:")
        theirs = code(lv["ssa"][k:k + 3], size=16, color=FUNC)
        k2 = lv["ssa"].index("17:")
        theirs2 = code(lv["ssa"][k2:k2 + 2], size=16, color=FUNC)
        llvm = VGroup(theirs, theirs2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lt = label(r"clang's \texttt{mem2reg} pass on the C version: \ the same three $\phi$s", font_size=20,
                   color=FUNC)
        g = VGroup(lt, llvm).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(pts, DOWN, buff=0.5).align_to(
            pts, LEFT)
        out = label(r"leaving SSA: \ each $\phi$ becomes a copy on each incoming edge", font_size=21,
                    color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Why go to this trouble? <bookmark mark='a'/> Because once every use has exactly one definition, the "
            "links from definitions to uses are just pointers, and a fact about a name, say that it is a constant, "
            "is true everywhere the name appears. The analyses of the next chapters can follow these links "
            "directly, instead of sweeping over every block again and again. <bookmark mark='b'/> Industrial "
            "compilers agree. This is LLVM's pass called mem2reg, run by clang on the same function written in C. "
            "Its phis sit in the same places: two at the loop header, for s and i, and one at the join after the "
            "if. <bookmark mark='c'/> And when optimization is done, the phis are taken out again: each becomes a "
            "copy placed on its incoming edge, which the register allocator will try to make disappear."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(g))
            vo.wait_until("c")
            self.play(FadeIn(out))
        self.wait(0.3)
        self.clear_scene()
