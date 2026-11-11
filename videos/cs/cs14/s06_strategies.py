from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono, region


class Strategies(VoiceoverScene):
    def construct(self):
        self.card()
        self.kinds()
        self.table()
        self.sharing()
        self.theorem()

    def card(self):
        card = chapter_card(5, r"Evaluation strategies", r"Which redex first?", lit=(1960,), part=PART)
        with self.voiceover("Chapter five. Evaluation strategies."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def kinds(self):
        head = label(r"Which redex should be reduced first?", font_size=34).to_edge(UP, buff=0.3)
        rows = [
            (r"normal order", r"the leftmost, outermost redex, \ even inside a $\lambda$", YES),
            (r"applicative order", r"the leftmost, innermost redex: \ arguments first", CTRL),
            (r"call-by-name", r"outermost, \ but never inside a $\lambda$ \ (ALGOL 60)", DATA),
            (r"call-by-value", r"arguments to values first, \ never inside a $\lambda$ \ (C, Java, OCaml, Python)",
             FUNC),
            (r"call-by-need", r"call-by-name, \ but each argument evaluated at most once \ (Haskell)", HEAD),
        ]
        g = VGroup()
        for name, desc, c in rows:
            r = VGroup(region(3.4, 0.6, name, c, font_size=20), label(desc, font_size=20, color=GREY_A)).arrange(
                RIGHT, buff=0.4)
            g.add(r)
        g.arrange(DOWN, buff=0.28, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            (
            "Reduction strategies choose which work to perform. <bookmark mark='a'/> Full normal order chooses "
            "the leftmost outermost redex, including redexes under lambdas. <bookmark mark='b'/> Full applicative "
            "order chooses the leftmost innermost redex, again including lambda bodies. <bookmark mark='c'/> Weak "
            "evaluation stops beneath an unapplied lambda. Call-by-name passes the argument unevaluated and can "
            "substitute or revisit it each time it is used. Our comparison uses this pure weak model. <bookmark "
            "mark='d'/> Call-by-value evaluates an argument to a value before beta application. Many languages "
            "use a form of this rule; their sequencing and effects add language-specific details. <bookmark "
            "mark='e'/> Call-by-need adds sharing: a suspended argument is evaluated when demanded and its result "
            "is reused. This is a model for lazy implementations such as Haskell, with separate costs for "
            "allocation, forcing and retaining thunks. Weak-head results and full beta normal forms are different "
            "stopping criteria."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def table(self):
        s = load("strategies")
        head = label(r"$(\lambda x\,y.\; x)\;a\;\Omega$, \ four ways", font_size=34).to_edge(UP, buff=0.3)
        rows, cols = [], []
        for r in s["table"]:
            ok = r["steps"] is not None
            rows.append([r["strategy"], f"{r['steps']} steps" if ok else "never stops", r["result"] or "---"])
            cols.append([WHITE, YES if ok else NO, YES if ok else NO])
        tab = grid_table([r"strategy", r"outcome", r"result"], rows, widths=[3.0, 2.8, 1.6], row_h=0.55,
                         font_size=24, colors=cols, mono_cols=(0, 2)).next_to(head, DOWN, buff=0.7)
        note = VGroup(
            label(r"the function ignores its second argument; \ strategies that evaluate it first \ never get "
                  r"there", font_size=22, color=GREY_A),
            label(r"strategies that wait can only do better: \ the theorem at the end of this chapter", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here is the term from chapter two: a function that returns its first argument, applied to a and to "
            "omega. <bookmark mark='a'/> Normal order and call-by-name reduce the outside first, and finish in two "
            "steps with the answer a. Applicative order and call-by-value insist on evaluating omega before the "
            "call, and never finish. <bookmark mark='b'/> The function did not even need omega. Strategies that "
            "wait never do worse at finding an answer, which the end of this chapter makes precise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(note[0]))
            vo.wait_until("b")
            self.play(FadeIn(note[1]))
        self.wait(0.3)
        self.clear_scene()

    def sharing(self):
        s = load("strategies")
        head = label(r"How often is the argument evaluated?", font_size=34).to_edge(UP, buff=0.3)
        arg = label(r"the argument: \ $\mathit{times}\;\underline{3}\;\underline{3}$, \ read back as a number",
                    font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.3)
        rows, cols = [], []
        for r in s["share"]:
            rows.append([r["label"], f"{r['name']['beta']}", f"{r['need']['beta']}", f"{r['value']['beta']}"])
            b = [r["name"]["beta"], r["need"]["beta"], r["value"]["beta"]]
            best = min(b)
            cols.append([WHITE] + [YES if v == best else NO for v in b])
        tab = grid_table([r"the function's body", r"by name", r"by need", r"by value"], rows,
                         widths=[3.4, 1.8, 1.8, 1.8], row_h=0.55, font_size=22, colors=cols, mono_cols=()).next_to(
            arg, DOWN, buff=0.5)
        cap = label(r"$\beta$-steps on an environment machine with thunks \ (our \texttt{lazy\_eval})", font_size=18,
                    color=GREY_B).next_to(tab, DOWN, buff=0.15)
        pts = VGroup(
            label(r"by name re-evaluates the argument at every use", font_size=21, color=GREY_A),
            label(r"by value evaluates it even when it is never used", font_size=21, color=GREY_A),
            label(r"by need does neither: \ at most once, \ only if needed \ (Wadsworth, \ 1971)", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.15).next_to(cap, DOWN, buff=0.4)
        with self.voiceover(
            "Strategies also differ in cost. <bookmark mark='a'/> We ran three functions on the same argument, "
            "three times three, on a machine that counts beta steps. <bookmark mark='b'/> When the body uses its "
            "parameter three times, call-by-name evaluates the argument three times over: forty-three steps "
            "against thirty-three. <bookmark mark='c'/> When the body never uses it, call-by-value evaluates it "
            "anyway, and loses. <bookmark mark='d'/> Call-by-need wins both ways: it evaluates an argument at most "
            "once, and only if it is needed. Christopher Wadsworth described this sharing in 1971, and it is how "
            "Haskell runs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(arg))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]], FadeIn(cap))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in tab.cells[1]], FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in tab.cells[2]], *[FadeIn(c) for c in tab.cells[3]], FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def theorem(self):
        head = label(r"The standardization theorem", font_size=36).to_edge(UP, buff=0.3)
        thm = label(r"if a term has a normal form, \ normal order reaches it \ (Curry and Feys, \ 1958)",
                    font_size=26, color=HEAD).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"so normal order is the safe strategy: \ it never misses an answer that exists", font_size=23,
                  color=GREY_A),
            label(r"but it may be slow, \ and real languages choose speed: \ call-by-value", font_size=23,
                  color=GREY_A),
            label(r"and whichever path finds a normal form, \ they all find the \textit{same} one: \ chapter 6",
                  font_size=23, color=YES),
        ).arrange(DOWN, buff=0.3).next_to(thm, DOWN, buff=0.6)
        with self.voiceover("One theorem settles which strategy is safest. <bookmark mark='a'/> If a term has a normal form at all, normal order will reach it. Curry and Feys proved this standardization theorem in 1958. <bookmark mark='b'/> So normal order never misses an answer that exists. It may waste work, and real languages mostly choose call-by-value for speed and predictability, accepting that some programs loop that need not. <bookmark mark='c'/> But could two strategies find different answers? That is the subject of the next chapter.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(thm), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[:2]))
            vo.wait_until('c')
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
