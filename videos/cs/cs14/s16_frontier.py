from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.inference()
        self.refinement()
        self.hott()
        self.effects()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ the edges of type theory", r"What can types not yet do?", lit=(2013,),
                            extra=((2013, r"Homotopy Type Theory"),), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: the edges of type theory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def inference(self):
        f = load("frontier")
        head = label("Inference: a synthetic scaling experiment", font_size=34).to_edge(UP, buff=0.3)
        sc = f["scale"]
        import math
        ymax = max(10, 10 * math.ceil(1.15 * max(1000*r["seconds"] for r in sc) / 10))
        ystep = ymax / 4
        ax = Axes(x_range=[0, 360, 60], y_range=[0, ymax, ystep], x_length=4.6, y_length=3.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to(LEFT * 4.1 + DOWN * 0.3)
        pts = [ax.c2p(r["defs"], 1000 * r["seconds"]) for r in sc]
        line = VMobject(color=YES, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=YES) for p in pts])
        xl = label(r"definitions in the program", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=0.3)
        yl = label(r"inference time, \ ms", font_size=17, color=GREY_B).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        ticks = VGroup(*[label(str(v), font_size=14, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                         for v in (0, 120, 240, 360)],
                       *[label(f"{v:g}", font_size=14, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                         for v in (0, ymax / 2, ymax)])
        def two(a, b, color):
            return VGroup(label(a, font_size=22, color=color), label(b, font_size=22, color=color)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1)

        side = VGroup(
            two(rf"{sc[-1]['copies']} copies: \ {sc[-1]['defs']} definitions total", "single-host samples; no universal complexity conclusion",
                YES),
            two(r"the nested-let worst case: \ $2^{2^n}$ leaves,", r"yet cheap when types are shared", GREY_A),
            two("worst-case ML typability is DEXPTIME-complete",
                "fast-inference bounds also constrain type-scheme size", GREY_A),
            two(r"open: \ a precise account", r"of when inference is fast", HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        if side.width > 6.4:
            side.scale_to_fit_width(6.4)
        side.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        with self.voiceover(
            (
            "Worst-case inference complexity and a measured workload answer different questions. <bookmark "
            "mark='a'/> We repeat the Job's eleven definitions in up to thirty-two copies, giving three hundred "
            "and fifty-two definitions. The graph shows recorded host times for this synthetic family. "
            "Unification-call counts grow exactly with the copy count; elapsed times also include implementation "
            "and scheduling effects and need not form a straight line. <bookmark mark='b'/> Shared type graphs "
            "avoid expanding repeated subtypes in the nested-let example. Complexity analyses parameterize more "
            "than source size, including type-scheme size and let structure; bounded nesting alone is not a "
            "complete universal linear-time guarantee. McAllester's 2003 work is one source for that analysis. "
            "<bookmark mark='c'/> To investigate an implementation, state the family and representation, measure "
            "work as well as wall time, and vary the parameters. A small favorable graph cannot establish how "
            "every real program behaves."
        )
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def refinement(self):
        head = label(r"Types checked by a solver", font_size=34).to_edge(UP, buff=0.3)
        t = MathTex(r"\mathit{get} : (a : \mathsf{array}) \to \{\, i : \mathsf{int} \mid 0 \le i < \mathit{len}(a)\,\} "
                    r"\to \mathsf{int}", font_size=34, color=YES).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"\textbf{refinement types}: \ a base type plus a logical predicate \ (liquid types, \ 2008)",
                  font_size=22, color=GREY_A),
            label("conditions go to a solver: proved, refuted, unknown, or timed out",
                  font_size=22, color=GREY_A),
            label(r"LiquidHaskell, \ F*, \ Dafny: \ array bounds, \ protocol invariants, \ cryptography proved",
                  font_size=22, color=GREY_A),
            label(r"where dependent types meet automation: \ how much can a solver decide for us?", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.25).next_to(t, DOWN, buff=0.6)
        with self.voiceover(
            (
            "Refinement types attach logical predicates to values. <bookmark mark='a'/> In the displayed "
            "interface, get receives an array and an index satisfying zero less than or equal to i, and i less "
            "than the array length. The caller must establish that condition. <bookmark mark='b'/> Type checking "
            "generates verification conditions for a selected logic. An SMT solver may prove them, find a "
            "countermodel, or return unknown or a timeout. Solver failure to prove a condition does not by itself "
            "prove the program wrong. <bookmark mark='c'/> LiquidHaskell, F star and Dafny combine types, "
            "specifications and automated proof in different ways. Their verified properties depend on the stated "
            "specifications, supported theories and trust boundaries. <bookmark mark='d'/> The engineering "
            "challenge is to choose useful predicates and automation while keeping proof obligations "
            "understandable. Refinements can automate some proofs; they do not remove the need to define or "
            "justify the property."
        )
        ) as vo:
            self.play(FadeIn(head), Write(t))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def hott(self):
        head = label(r"Equality, \ rethought", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"in dependent type theory, \ $a = b$ is itself a type: \ its values are proofs of equality",
                  font_size=22, color=GREY_A),
            label(r"Voevodsky's insight: \ read those proofs as \textit{paths} in a space \ (homotopy type theory, \ "
                  r"2013)", font_size=22, color=GREY_A),
            label(r"the \textbf{univalence} axiom: \ equivalent types are equal", font_size=24, color=YES),
            label("opaque axioms can block reduction; the original STLC theorem keeps its assumptions", font_size=22, color=NO),
            label(r"cubical type theory \ (Cohen, Coquand, Huber, M\"ortberg, \ 2015): \ univalence as a theorem, \ "
                  r"and it runs", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            (
            "Identity types give equality mathematical structure. <bookmark mark='a'/> A proof that a equals b is "
            "itself a term of an identity type, and proofs can have further equalities between them. <bookmark "
            "mark='b'/> Homotopy type theory interprets these witnesses as paths and higher paths. Voevodsky's "
            "univalent foundations helped develop this connection. <bookmark mark='c'/> Univalence relates "
            "equality of types to equivalence of types: the canonical map from type equalities to equivalences is "
            "itself an equivalence. This makes precise a way of transporting mathematical structure across "
            "equivalences. <bookmark mark='d'/> Adding an axiom without computation rules can leave closed data "
            "expressions without a canonical numeral normal form. That is a question about computation and "
            "canonicity in the extended theory, not a counterexample to the earlier theorem about our original "
            "simply typed calculus. <bookmark mark='e'/> Cubical type theories provide computational treatments "
            "of univalence. Their exact normalization and canonicity results depend on the chosen calculus. "
            "Implementations such as Cubical Agda turn these ideas into proof-assistant tools."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def effects(self):
        head = label(r"Typing what programs \textit{do}", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"a type says what a function returns, \ not whether it reads files, \ throws, \ or loops", font_size=22,
                  color=GREY_A),
            label(r"\textbf{effect handlers} \ (Plotkin and Pretnar, \ 2009): \ exceptions, \ generators, \ async, \ "
                  r"one mechanism", font_size=22, color=GREY_A),
            label(r"shipped in OCaml 5 \ (2022); \ effect types in Koka and Eff", font_size=22, color=YES),
            label(r"open: \ effect types programmers will accept, \ and compile to fast code", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            (
            "In a language with unrestricted effects, an ordinary int-to-int type does not list every action a "
            "function may perform. <bookmark mark='a'/> It might read a file, raise an exception or diverge. An "
            "effect system adds information about such behavior; its guarantees depend on which effects it "
            "tracks. <bookmark mark='b'/> An algebraic effect operation sends a request to a handler. The handler "
            "receives the operation's data and a captured delimited continuation, which it may resume according "
            "to the language's rules. The handler is not itself just the continuation. <bookmark mark='c'/> OCaml "
            "5 introduced effect handlers in 2022, while languages such as Koka track effects in types. These "
            "systems differ in typing and continuation discipline. <bookmark mark='d'/> Usable interfaces, "
            "compositional reasoning and efficient implementations remain active design problems. Stating the "
            "operation and resumption rules lets us reason about a specific mechanism instead of treating all "
            "effects as interchangeable."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def open(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.35)
        qs = VGroup(
            label(r"sound gradual typing with a provably small run-time cost", font_size=22, color=GREY_A),
            label("inference decidability depends on rank, annotations and the exact calculus", font_size=22, color=GREY_A),
            label(r"dependent types in a mainstream language, \ without a proof for every line", font_size=22,
                  color=GREY_A),
            label(r"univalence, \ fast: \ cubical type theory as a practical proof assistant", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first one", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover("Research questions become useful when their model is explicit. <bookmark mark='a'/> For gradual typing, choose a cast semantics, a cost model and a comparison baseline before asking for an overhead bound. Space-efficient coercion composition already addresses some wrapper-chain problems. <bookmark mark='b'/> For polymorphic inference, specify the language, rank convention, available annotations and whether the task is checking, typability or principal inference. Different restricted systems have different decidability results. <bookmark mark='c'/> For dependent types, study a concrete way to reduce proof burden while preserving the intended trusted core. <bookmark mark='d'/> For cubical computation, measure a stated proof workload and identify normalization or representation costs. <bookmark mark='e'/> The starred exercise starts with a small gradual cast calculus, reproduces a known space result, then asks for a precisely scoped extension. Reviewing known work comes before claiming an open problem.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, q in zip('abcd', qs):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(q, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until('e')
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
