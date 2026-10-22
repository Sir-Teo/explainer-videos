from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import FAIL, FCOL, GCOST, HEUR, HIST, LEARN, MONO, PART, PATH, SYMBOL, load, node_box


class Survives(VoiceoverScene):
    def construct(self):
        self.card()
        self.search_lives()
        self.verification()
        self.multipliers()
        self.proofs()
        self.planning()
        self.neurosymbolic()

    def card(self):
        card = chapter_card(14, r"What survives", r"Where are search and logic running today?", lit=(2017, 2024),
                            part=PART)
        with self.voiceover("Chapter fourteen. What survives."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def search_lives(self):
        then = VGroup(label(r"Deep Blue, $1997$", font_size=28, color=GREY_B),
                      label(r"alpha--beta search", font_size=24, color=GCOST),
                      label(r"$+$ about $8{,}000$ hand-tuned features", font_size=24, color=HEUR),
                      label(r"$126$ million positions a second", font_size=22, color=GREY_A))
        now = VGroup(label(r"AlphaZero, $2017$", font_size=28, color=GREY_B),
                     label(r"Monte Carlo tree search", font_size=24, color=GCOST),
                     label(r"$+$ a network that learned $h$ by self-play", font_size=24, color=LEARN),
                     label(r"about a thousand times fewer positions \\ than the chess program it beat", font_size=22,
                           color=GREY_A))
        for g in (then, now):
            g.arrange(DOWN, buff=0.22)
        then.move_to([-3.4, 0.6, 0])
        now.move_to([3.4, 0.6, 0])
        arrow = Arrow(then.get_right(), now.get_left(), buff=0.4, color=GREY_B)
        same = label(r"the same skeleton: \ search, \ guided by an evaluation", font_size=26, color=FCOL)
        same.to_edge(DOWN, buff=0.9)
        p26 = note(r"Part 26 builds AlphaZero; \ Campbell, Hoane \& Hsu (2002); \ Silver et al.\ (2018)")
        p26.to_corner(DR, buff=0.2)
        head = label(r"the symbolic era ended; \ its machinery did not", font_size=34, color=GREY_A)
        head.to_edge(UP, buff=0.4)
        with self.voiceover(
            "The symbolic era ended, but its machinery did not. <bookmark mark='a'/> Deep Blue was search plus an evaluation "
            "written by people. <bookmark mark='b'/> Twenty years later AlphaZero kept the search, Monte Carlo tree search "
            "instead of alpha-beta, and learned its evaluation by playing itself, examining about a thousand times fewer "
            "positions per second than the chess engine it beat. <bookmark mark='c'/> Search guided by an evaluation is the "
            "skeleton of both. Part 26 builds one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in then], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), LaggedStart(*[FadeIn(t) for t in now], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(same), FadeIn(p26))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verification(self):
        d = load("cdcl")
        big = d["proved"]
        w = max(int(k) for k in big)
        b = big[str(w)]
        bug = d["bug"]
        fdiv = history_card(1994, r"Intel's Pentium division bug", r"a few missing entries in a lookup table; \ a "
                            r"\$475 million charge; \ formal verification becomes routine in chip design", width=6.0,
                            color=FAIL, font_size=19).move_to([-3.5, 2.0, 0])
        eq = VGroup(label(rf"our solver: \ two ${w}$-bit adders, \ ripple-carry and Kogge--Stone", font_size=22,
                          color=GREY_A),
                    label(rf"equal on all $2^{{{2 * w}}}$ inputs: \ proved with ${b['conflicts']:,}$ conflicts"
                          .replace(",", "{,}"), font_size=24, color=PATH)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        eq.move_to([-3.2, -0.3, 0])
        wb = bug["width"]
        ce = VGroup(label(rf"a slipped wire at bit ${bug['bit']}$ of a ${wb}$-bit adder: \ caught", font_size=22,
                          color=FAIL),
                    MathTex(rf"{bug['a']:,} + {bug['b']:,} = {bug['right']:,} \pmod{{2^{{{wb}}}}}".replace(",", "{,}"),
                            font_size=30, color=PATH),
                    MathTex(rf"\text{{the buggy adder says }} {bug['wrong']:,}".replace(",", "{,}"), font_size=30,
                            color=FAIL)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([-3.2, -2.3, 0])
        smt = VGroup(history_card(2008, r"de Moura \& Bj\o rner: \ Z3", r"SAT plus theories of arithmetic, arrays, "
                                  r"bit-vectors: \ SMT", width=5.6, color=HIST, font_size=19),
                     history_card(2022, r"Amazon Web Services", r"over a billion SMT queries a day, \ checking "
                                  r"access policies", width=5.6, color=HIST, font_size=19)).arrange(DOWN, buff=0.3)
        smt.move_to([3.6, 0.2, 0])
        tag = note(r"computed: \ our CDCL solver").to_corner(DR, buff=0.2)
        ins = label(r"inputs \ $a$, $b$", font_size=24, color=GREY_A).move_to([0.9, 0.6, 0])
        ad1 = node_box(r"ripple-carry adder", GCOST, font_size=22).move_to([3.3, 1.4, 0])
        ad2 = node_box(r"Kogge--Stone adder", HEUR, font_size=22).move_to([3.3, -0.2, 0])
        cmp_ = node_box(r"differ?", FAIL, font_size=24).move_to([5.9, 0.6, 0])
        miter = VGroup(ins, ad1, ad2, cmp_,
                       Arrow(ins.get_right(), ad1.get_left(), buff=0.12, color=GREY_B, stroke_width=2.5),
                       Arrow(ins.get_right(), ad2.get_left(), buff=0.12, color=GREY_B, stroke_width=2.5),
                       Arrow(ad1.get_right(), cmp_.get_left(), buff=0.12, color=GREY_B, stroke_width=2.5),
                       Arrow(ad2.get_right(), cmp_.get_left(), buff=0.12, color=GREY_B, stroke_width=2.5))
        miter.add(label(r"as clauses: \\ satisfiable $=$ a bug, \\ unsatisfiable $=$ proved equal", font_size=20,
                        color=GREY_A).next_to(VGroup(ad2, cmp_), DOWN, buff=0.35))
        with self.voiceover(
            "Logic found its biggest job in checking machines. <bookmark mark='a'/> In 1994 a flaw in the Pentium's division "
            "circuit, a few missing table entries, cost Intel a four-hundred-and-seventy-five-million-dollar charge, and chip "
            "makers turned to formal verification, with SAT solvers among its engines. <bookmark mark='b'/> Our own small "
            f"solver proves two {w}-bit adders equal on all two to the {2 * w} inputs, with {b['conflicts']:,} conflicts. "
            f"<bookmark mark='c'/> Slip one wire at bit {bug['bit']}, and it finds an input where they disagree: "
            f"{bug['a']:,} plus {bug['b']:,} should give {bug['right']:,} in {wb} bits; the faulty circuit says "
            f"{bug['wrong']:,}. <bookmark mark='d'/> Add theories of arithmetic and data structures and you get SMT solvers like "
            "Microsoft's Z3; Amazon reported in 2022 running over a billion SMT queries a day to check who can access what."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(miter))
            vo.wait_until("a")
            self.play(FadeIn(fdiv, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(eq))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in ce], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeOut(miter), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in smt], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def multipliers(self):
        d = load("cdcl")
        W = np.asarray(d["mult_widths"])
        M = np.asarray(d["mult_conflicts"], float)
        A = np.asarray(d["adder_widths"])
        Ac = np.asarray(d["adder_cdcl"], float)
        top = np.ceil(np.log10(M.max())) + 0.3
        g = axes([1.5, max(W[-1], A[-1]) + 0.5], [0, top], x_length=6.6, y_length=4.0, xlabel=r"bits",
                 ylabel=r"conflicts \ (log scale)", xticks=[2, 4, 6, 8, 10, 12], yticks=list(range(0, int(top) + 1)),
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.4, -0.4, 0])
        la = curve(g.ax, A, np.log10(Ac), PATH, 4)
        lm = curve(g.ax, W, np.log10(M), FAIL, 4)
        lg = legend([(PATH, r"adders: \ $a + b$, \ two designs"), (FAIL, r"multipliers: \ $a \times b = b \times a$?")],
                    font_size=20).move_to([4.0, 2.0, 0])
        growth = float(np.exp(np.mean(np.diff(np.log(M[2:])))))
        txt = label(rf"about $\times {growth:.0f}$ per extra bit", font_size=24, color=FAIL).move_to([4.0, 0.6, 0])
        why_ = label(r"multiplication mixes every bit with every other: \\ there is no short proof to learn",
                     font_size=20, color=GREY_A).move_to([4.0, -0.6, 0])
        tag = note(r"computed: \ our CDCL solver").to_corner(DR, buff=0.2)
        with self.voiceover(
            "There are limits. <bookmark mark='a'/> Ask the same solver whether a multiplier gives the same answer for a times "
            f"b as for b times a. <bookmark mark='b'/> The conflicts grow about {growth:.0f}-fold with every extra bit: "
            f"{M[-1]:,.0f} at {int(W[-1])} bits. Multipliers are a famous hard case; industry handles arithmetic with algebraic "
            "methods instead."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), Create(la), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(FadeIn(lg[1]))
            vo.wait_until("b")
            self.play(Create(lm), FadeIn(txt), FadeIn(why_), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proofs(self):
        lean = VGroup(Text("theorem two_eq : 1 + 1 = 2 := by", font=MONO, font_size=22, color=WHITE),
                      Text("  norm_num", font=MONO, font_size=22, color=FCOL)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        box = SurroundingRectangle(lean, color=SYMBOL, buff=0.25, corner_radius=0.1)
        lg = VGroup(box, lean).move_to([-3.4, 2.3, 0])
        if lg.get_left()[0] < -6.85:
            lg.shift(RIGHT * (-6.85 - lg.get_left()[0]))
        flow = VGroup(node_box(r"a network proposes", LEARN, font_size=22), node_box(r"Lean checks", SYMBOL,
                                                                                      font_size=22))
        flow.arrange(RIGHT, buff=0.7).move_to([-3.6, -0.3, 0])
        flow.add(Arrow(flow[0].get_right(), flow[1].get_left(), buff=0.1, color=GREY_B))
        ll = label(r"Lean: \ a proof assistant; \ every step machine-checked", font_size=20, color=SYMBOL)
        ll.next_to(lg, DOWN, buff=0.15)
        cards = VGroup(
            history_card(2024, r"AlphaGeometry \ (Trinh et al., \textit{Nature})", r"a language model suggests "
                         r"constructions, \ a symbolic engine deduces: \ olympiad geometry", width=6.2, color=LEARN,
                         font_size=19),
            history_card(2024, r"AlphaProof \ (published in \textit{Nature}, 2025)", r"AlphaZero-style search over "
                         r"Lean proofs: \ with AlphaGeometry 2, \ four of six IMO problems, \ $28$ of $42$ points, \ "
                         r"silver-medal level", width=6.2, color=LEARN, font_size=19),
            history_card(2025, r"Gemini Deep Think", r"gold-medal score at the IMO, $35$ of $42$, \ in plain language, "
                         r"graded by the IMO's coordinators", width=6.2, color=HEUR, font_size=19),
        ).arrange(DOWN, buff=0.22).move_to([3.4, -0.2, 0])
        lesson = label(r"generate with a network, \\ check with logic", font_size=30, color=FCOL).move_to([-3.6, -2.0, 0])
        with self.voiceover(
            "Logic's other modern home is mathematics. <bookmark mark='a'/> In a proof assistant like Lean, a small trusted "
            "program checks every step, so a proof that compiles is correct. <bookmark mark='b'/> DeepMind's AlphaGeometry, in "
            "2024, paired a language model that suggests constructions with a symbolic deduction engine. "
            "<bookmark mark='c'/> AlphaProof ran AlphaZero-style search over Lean proofs; with AlphaGeometry 2, it solved four "
            "of six problems at the 2024 International Mathematical Olympiad, silver-medal level. <bookmark mark='d'/> A year "
            "later a Gemini model reached a gold-medal score writing plain language, graded by the olympiad's coordinators. "
            "<bookmark mark='e'/> Either way: a network generates, and logic or a grader checks."
        ) as vo:
            self.play(FadeIn(lg), FadeIn(ll))
            vo.wait_until("a")
            self.play(Indicate(lg, color=SYMBOL, scale_factor=1.04))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15), *([FadeIn(flow)] if k == 1 else []))
            vo.wait_until("e")
            self.play(FadeIn(lesson))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def planning(self):
        bars = [(r"LLaMA 3.1 405B \\ (zero-shot)", 62.6, GREY_B), (r"o1-preview", 97.8, LEARN),
                (r"a classical planner \\ (Fast Downward)", 100.0, PATH)]
        g = axes([0, 3], [0, 100], x_length=6.0, y_length=3.6, ylabel=r"Blocksworld problems solved",
                 yticks=[0, 50, 100], yfmt=lambda v: rf"{int(v)}\%", center=[-3.0, -0.2, 0])
        rects = VGroup()
        for i, (nm, v, col) in enumerate(bars):
            h = g.ax.c2p(0, v)[1] - g.ax.c2p(0, 0)[1]
            r = Rectangle(width=0.9, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to(g.ax.c2p(i + 0.5, 0), aligned_edge=DOWN)
            rects.add(VGroup(r, MathTex(rf"{v:g}\%", font_size=24, color=col).next_to(r, UP, buff=0.08),
                             label(nm, font_size=19, color=col).next_to(g.ax.c2p(i + 0.5, 0), DOWN, buff=0.15)))
        for r in rects:
            if r[2].width > 1.9:
                r[2].width = 1.9
        myst = label(r"renamed (``Mystery Blocksworld''): \ o1-preview $52.8\%$, \ the planner still $100\%$",
                     font_size=20, color=FAIL).next_to(g, DOWN, buff=0.95)
        cite_ = note(r"Valmeekam, Stechly \& Kambhampati (2024), PlanBench").to_corner(DL, buff=0.2)
        pattern = VGroup(node_box(r"a language model", LEARN, font_size=22), node_box(r"PDDL", SYMBOL, font_size=22),
                         node_box(r"a classical planner", PATH, font_size=22),
                         node_box(r"a plan, guaranteed", FCOL, font_size=22)).arrange(DOWN, buff=0.45)
        pattern.move_to([4.2, 0.2, 0])
        arr = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.06, color=GREY_B, stroke_width=2.5)
                       for a, b in zip(pattern, pattern[1:])])
        pl = label(r"LLM+P \ (Liu et al., 2023)", font_size=20, color=GREY_A).next_to(pattern, UP, buff=0.2)
        with self.voiceover(
            "Planning is back, inside language-model agents. <bookmark mark='a'/> On PlanBench, built from the blocks world, "
            "the best ordinary language model tested in 2024 solved sixty-three percent of problems, and OpenAI's reasoning "
            "model o1-preview ninety-eight. <bookmark mark='b'/> Rename the blocks and actions to nonsense words, logic "
            "unchanged, and o1-preview fell to fifty-three percent; a classical planner solves every instance, whatever the "
            "names. <bookmark mark='c'/> One practical answer combines them: the language model writes the problem in the "
            "planning language PDDL, and a classical planner finds a plan guaranteed to work."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rects], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(myst))
            vo.wait_until("c")
            self.play(FadeIn(pl), LaggedStart(*[FadeIn(p) for p in pattern], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neurosymbolic(self):
        left = VGroup(label(r"networks", font_size=30, color=LEARN),
                      label(r"perception, \ intuition, \\ guesses from data", font_size=24, color=GREY_A))
        right = VGroup(label(r"symbols", font_size=30, color=SYMBOL),
                       label(r"search, \ logic, \\ guarantees", font_size=24, color=GREY_A))
        for g in (left, right):
            g.arrange(DOWN, buff=0.2)
        left.move_to([-3.6, 1.4, 0])
        right.move_to([3.6, 1.4, 0])
        arrows = VGroup(CurvedArrow(left.get_right() + RIGHT * 0.2, right.get_left() + LEFT * 0.2, angle=-0.5,
                                    color=FCOL),
                        CurvedArrow(right.get_left() + LEFT * 0.2 + DOWN * 0.6, left.get_right() + RIGHT * 0.2 +
                                    DOWN * 0.6, angle=-0.5, color=FCOL))
        al = VGroup(label(r"propose", font_size=22, color=FCOL).next_to(arrows[0], UP, buff=0.05),
                    label(r"check", font_size=22, color=FCOL).next_to(arrows[1], DOWN, buff=0.05))
        ex = label(r"AlphaZero \quad AlphaProof \quad AlphaGeometry \quad FunSearch \quad AlphaEvolve \quad "
                   r"agents with tools", font_size=24, color=GREY_A).move_to(DOWN * 1.4)
        if ex.width > 13.0:
            ex.width = 13.0
        p = label(r"Parts 26, 28, 29: \ search and checking, \ inside learned systems", font_size=24, color=PATH)
        p.to_edge(DOWN, buff=0.5)
        head = label(r"symbols, \ or learning?", font_size=36, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "So the old argument, symbols or learning, ended in a merger. <bookmark mark='a'/> Networks bring what the symbolic "
            "era lacked: perception, intuition, guesses from data. <bookmark mark='b'/> Symbols bring what networks cannot "
            "promise: exhaustive search, exact logic, guarantees. <bookmark mark='c'/> Today's strongest systems let a network "
            "propose and a symbolic process check: AlphaZero, AlphaProof, FunSearch and AlphaEvolve, agents that call tools. "
            "This is neurosymbolic AI, <bookmark mark='d'/> and we will meet it again in reinforcement learning, reasoning "
            "models and agents."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(Create(arrows[0]), FadeIn(al[0]), Create(arrows[1]), FadeIn(al[1]))
            self.play(FadeIn(ex))
            vo.wait_until("d")
            self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
