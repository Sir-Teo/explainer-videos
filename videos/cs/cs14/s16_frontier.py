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
        head = label(r"Exponential in theory, \ linear in practice", font_size=34).to_edge(UP, buff=0.3)
        sc = f["scale"]
        ax = Axes(x_range=[0, 360, 60], y_range=[0, 20, 5], x_length=4.6, y_length=3.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to(LEFT * 4.1 + DOWN * 0.3)
        pts = [ax.c2p(r["defs"], 1000 * r["seconds"]) for r in sc]
        line = VMobject(color=YES, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=YES) for p in pts])
        xl = label(r"definitions in the program", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=0.3)
        yl = label(r"inference time, \ ms", font_size=17, color=GREY_B).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        ticks = VGroup(*[label(str(v), font_size=14, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                         for v in (0, 120, 240, 360)],
                       *[label(str(v), font_size=14, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                         for v in (0, 10, 20)])
        def two(a, b, color):
            return VGroup(label(a, font_size=22, color=color), label(b, font_size=22, color=color)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1)

        side = VGroup(
            two(rf"the Job's definitions, \ copied up to {sc[-1]['defs']} times:", r"time grows in a straight line",
                YES),
            two(r"the nested-let worst case: \ $2^{2^n}$ leaves,", r"yet cheap when types are shared", GREY_A),
            two(r"DEXPTIME-complete needs deeply nested \texttt{let}s;",
                r"real programs keep nesting shallow \ (McAllester, \ 2003)", GREY_A),
            two(r"open: \ a precise account", r"of when inference is fast", HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        if side.width > 6.4:
            side.scale_to_fit_width(6.4)
        side.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        with self.voiceover(
            "Start with a puzzle from chapter ten. ML type inference is complete for exponential time, yet compilers "
            "run it on millions of lines without trouble. <bookmark mark='a'/> We timed our engine on the Job's "
            "definitions, copied over and over, up to three hundred and fifty-two definitions: the time grows in a "
            "straight line. <bookmark mark='b'/> The exponential examples need lets nested inside lets, each "
            "duplicating the last, and real programs do not look like that. David McAllester showed in 2003 that "
            "with nesting depth bounded, inference is nearly linear. <bookmark mark='c'/> A full account of which "
            "programs are hard, and why practice is so kind, is still open."
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
            label(r"each call generates a verification condition; \ an SMT solver discharges it \ (Part 13's z3)",
                  font_size=22, color=GREY_A),
            label(r"LiquidHaskell, \ F*, \ Dafny: \ array bounds, \ protocol invariants, \ cryptography proved",
                  font_size=22, color=GREY_A),
            label(r"where dependent types meet automation: \ how much can a solver decide for us?", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.25).next_to(t, DOWN, buff=0.6)
        with self.voiceover(
            "Dependent types are powerful but demand proofs. Refinement types try to have the power without the "
            "proofs. <bookmark mark='a'/> A refinement type is a base type plus a predicate: get takes an array and "
            "an integer that is at least zero and less than the array's length. <bookmark mark='b'/> Each call "
            "produces a logical condition, which an SMT solver like Part 13's z3 proves or refutes. <bookmark "
            "mark='c'/> LiquidHaskell, F star and Dafny work this way, and have been used to prove array accesses "
            "safe, protocol invariants and cryptographic code correct. <bookmark mark='d'/> The open question is "
            "how far automation can go before a human must write the proof."
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
            label(r"but an axiom does not compute: \ a program using it can get stuck", font_size=22, color=NO),
            label(r"cubical type theory \ (Cohen, Coquand, Huber, M\"ortberg, \ 2015): \ univalence as a theorem, \ "
                  r"and it runs", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "At the deep end, type theory is being used to rethink the foundations of mathematics. <bookmark "
            "mark='a'/> In dependent type theory, a equals b is itself a type, whose values are proofs that a and b "
            "are equal. <bookmark mark='b'/> Vladimir Voevodsky, a Fields medallist, proposed reading those proofs "
            "as paths in a space, and homotopy type theory was the result. <bookmark mark='c'/> Its central "
            "principle, univalence, says that equivalent types are equal, which is how mathematicians actually "
            "reason. <bookmark mark='d'/> Added as an axiom, though, it breaks chapter eight's promise: a program "
            "that uses an axiom can get stuck. <bookmark mark='e'/> Cubical type theory, from 2015, makes "
            "univalence a theorem with computational content, so programs using it still run. Implementations, "
            "such as Cubical Agda, exist; making them fast and convenient is current work."
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
            "Another frontier is typing what programs do, not only what they return. <bookmark mark='a'/> The type "
            "int to int says nothing about whether a function reads a file, throws an exception, or runs forever. "
            "<bookmark mark='b'/> Plotkin and Pretnar's effect handlers, from 2009, give one mechanism for "
            "exceptions, generators, asynchronous code and more: an effect is a request, and a handler, which is a "
            "delimited continuation, answers it. <bookmark mark='c'/> OCaml 5 shipped them in 2022, and languages "
            "like Koka track effects in types. <bookmark mark='d'/> Effect types that working programmers will "
            "accept, and that compile to fast code, are still being worked out."
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
            label(r"which inference problems stay decidable: \ rank-2 polymorphism yes, \ rank 3 and above no \ "
                  r"(Kfoury and Wells)", font_size=22, color=GREY_A),
            label(r"dependent types in a mainstream language, \ without a proof for every line", font_size=22,
                  color=GREY_A),
            label(r"univalence, \ fast: \ cubical type theory as a practical proof assistant", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first one", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here is where the field stands. <bookmark mark='a'/> Can sound gradual typing be made cheap, with a "
            "proven bound on its run-time cost? <bookmark mark='b'/> Which richer type systems keep inference "
            "decidable? Rank-two polymorphism does, and rank three and above do not, as Kfoury and Wells showed; "
            "the territory between is still being mapped. <bookmark mark='c'/> Can dependent types reach a "
            "mainstream language without demanding a proof for every line? <bookmark mark='d'/> And can "
            "univalence be made fast enough for everyday mathematics? <bookmark mark='e'/> This part's research "
            "problem takes up the first."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
