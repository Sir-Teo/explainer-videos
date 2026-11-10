from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table, load, mono


class Dependent(VoiceoverScene):
    def construct(self):
        self.card()
        self.vectors()
        self.pisigma()
        self.linear()
        self.rust()

    def card(self):
        card = chapter_card(13, r"Dependent and linear types", r"Can a type say more?", lit=(1984,),
                            extra=((1984, r"Trusting Trust; \ Martin-L\"of's type theory"),), part=PART)
        with self.voiceover("Chapter thirteen. Dependent and linear types."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def vectors(self):
        head = label(r"Types that mention values", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"\mathsf{Vec}\;A\;n", font_size=40, color=YES),
            MathTex(r"\mathit{append} : \mathsf{Vec}\;A\;m \to \mathsf{Vec}\;A\;n \to \mathsf{Vec}\;A\;(m + n)",
                    font_size=34),
            MathTex(r"\mathit{head} : \mathsf{Vec}\;A\;(n + 1) \to A", font_size=34),
            MathTex(r"\mathit{zip} : \mathsf{Vec}\;A\;n \to \mathsf{Vec}\;B\;n \to \mathsf{Vec}\;(A \times B)\;n",
                    font_size=34),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.5)
        notes = VGroup(
            label(r"lists of $A$s of length exactly $n$: \ the length is part of the type", font_size=21,
                  color=GREY_A),
            label(r"\textit{head} of an empty list is not a crash: \ it is a type error", font_size=21, color=YES),
            label(r"\textit{zip} cannot be called on lists of different lengths", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.45)
        with self.voiceover("So far, types and values have lived apart. Dependent types let a type mention a value. <bookmark mark='a'/> Vec A n is the type of lists of A of length exactly n: the length is part of the type. <bookmark mark='b'/> Appending a vector of length m to one of length n gives length m plus n, and the type checker verifies the arithmetic. <bookmark mark='c'/> Head accepts only vectors of length n plus one. Taking the head of an empty list is no longer a crash at run time; it is a type error. <bookmark mark='d'/> And zip demands two vectors of the same length.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Write(rows[0]), FadeIn(notes[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Write(rows[1]))
            vo.wait_until('c')
            self.play(Write(rows[2]), FadeIn(notes[1]))
            vo.wait_until('d')
            self.play(Write(rows[3]), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def pisigma(self):
        head = label(r"$\Pi$ and $\Sigma$: \ for all, \ and there exists", font_size=34).to_edge(UP, buff=0.3)
        pi = VGroup(MathTex(r"\Pi_{n : \mathsf{Nat}}\; \mathsf{Vec}\;A\;n", font_size=40, color=YES),
                    label(r"a function whose \textit{result type} depends on its argument: \ $\forall n$", font_size=21,
                          color=GREY_A)).arrange(DOWN, buff=0.15)
        sg = VGroup(MathTex(r"\Sigma_{n : \mathsf{Nat}}\; \mathsf{Vec}\;A\;n", font_size=40, color=DATA),
                    label(r"a pair whose \textit{second type} depends on its first: \ $\exists n$", font_size=21,
                          color=GREY_A)).arrange(DOWN, buff=0.15)
        VGroup(pi, sg).arrange(RIGHT, buff=1.2).next_to(head, DOWN, buff=0.6)
        hist = VGroup(
            label(r"Martin-L\"of's intuitionistic type theory \ (1972--1984): \ mathematics as programs", font_size=22,
                  color=GREY_A),
            label(r"the Calculus of Constructions \ (Coquand and Huet, \ 1988) \ $\to$ \ Coq, \ now Rocq", font_size=22,
                  color=GREY_A),
            label(r"Agda; \ Lean \ (2013), \ in which mathematicians formalize research proofs", font_size=22,
                  color=GREY_A),
            label(r"types contain programs, \ so checking a type may run one: \ that is why they must terminate",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(VGroup(pi, sg), DOWN, buff=0.6)
        with self.voiceover("Dependent function and pair types express two forms of evidence. <bookmark mark='a'/> Pi is a function type whose result can depend on its argument, such as a function taking n and returning a vector of length n. It corresponds to universal quantification under the propositions-as-types interpretation. <bookmark mark='b'/> Sigma pairs a witness with evidence depending on that witness: a length together with a vector of that length. It corresponds to an existential statement with explicit data. <bookmark mark='c'/> Martin-Lof's type theories and the calculus of constructions helped build constructive foundations and proof assistants. Rocq, Agda and Lean provide different systems; their kernels and computational features should not be identified with one tiny calculus. <bookmark mark='d'/> When types contain programs, definitional equality may require computation. The trusted logical core needs controlled reduction and recursion to preserve its metatheory. Executable partial or unsafe facilities can exist outside that core, with explicit restrictions on their use in proofs.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(pi), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(sg))
            vo.wait_until('c')
            self.play(LaggedStart(*[FadeIn(h) for h in hist[:3]], lag_ratio=0.5), run_time=3)
            vo.wait_until('d')
            self.play(FadeIn(hist[3]))
        self.wait(0.3)
        self.clear_scene()

    def linear(self):
        L = load("linear")
        head = label(r"Linear types: \ use it exactly once", font_size=34).to_edge(UP, buff=0.3)
        rows, cols = [], []
        kc = {"linear": YES, "affine": DATA, "relevant": CTRL, "unrestricted": NO}
        for r in L["rows"]:
            rows.append([r["name"], r["term"].replace("\\", "λ"), ", ".join(map(str, r["uses"])), r["kind"]])
            cols.append([WHITE, WHITE, WHITE, kc[r["kind"]]])
        tab = grid_table([r"combinator", r"term", r"uses of each parameter", r"kind"], rows,
                         widths=[2.6, 3.4, 3.2, 2.2], row_h=0.5, font_size=20, colors=cols, mono_cols=(1, 2)).next_to(
            head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"\textbf{linear}: \ exactly once; \ \textbf{affine}: \ at most once; \ \textbf{relevant}: \ at "
                  r"least once", font_size=21, color=GREY_A),
            label(r"Girard's linear logic \ (1987): \ assumptions as resources, \ consumed when used", font_size=21,
                  color=GREY_A),
            label(r"a file handle, \ a lock, \ a block of memory: \ things that must not be copied or forgotten",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "A different refinement counts uses. <bookmark mark='a'/> Our checker counts how many times each "
            "classic combinator uses each parameter. The identity, composition and flip use every argument exactly "
            "once: they are linear. The constant function throws its second argument away: affine, at most once. "
            "W and S duplicate one: relevant, at least once. <bookmark mark='b'/> Jean-Yves Girard's linear logic, "
            "from 1987, treats assumptions as resources that are consumed when used. <bookmark mark='c'/> In "
            "programming the resources are real: a file handle that must be closed exactly once, a lock, a block "
            "of memory that must be freed once and never used afterwards."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def rust(self):
        r = load("rust")
        head = label(r"Rust: \ ownership is an affine type", font_size=34).to_edge(UP, buff=0.3)
        mv = code(r["move"]["source"], size=14, color=CODE)
        bw = code(r["borrow"]["source"], size=14, color=CODE)
        pair = VGroup(mv, bw).arrange(RIGHT, buff=0.6, aligned_edge=UP)
        if pair.width > 13.2:
            pair.scale_to_fit_width(13.2)
        pair.next_to(head, DOWN, buff=0.5)
        e1 = mono(r["move"]["error"], 14, NO).next_to(mv, DOWN, buff=0.25).align_to(mv, LEFT)
        e2 = mono(r["borrow"]["error"].replace("because it is also", "because\nit is also"), 14, NO).next_to(
            bw, DOWN, buff=0.25).align_to(bw, LEFT)
        for e, c in ((e1, mv), (e2, bw)):
            if e.width > c.width + 1.0:
                e.scale_to_fit_width(c.width + 1.0)
        pts = VGroup(
            label(r"a \texttt{String} may be \textit{moved} once: \ using it afterwards is a type error", font_size=21,
                  color=GREY_A),
            label(r"borrows: \ many readers \textit{or} one writer, \ never both at once", font_size=21,
                  color=GREY_A),
            label("safe interfaces require valid unsafe implementations and runtime assumptions",
                  font_size=22, color=YES),
            mono(r.get("version", "").split(" (")[0], 14, GREY_B),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover("Rust makes ownership and borrowing concrete. <bookmark mark='a'/> The displayed String is not a Copy value. Assigning it to kept transfers ownership, so using the moved word is rejected with E zero three eight two. This is an affine discipline: a resource can be dropped as well as consumed once. Copy types follow different rules. <bookmark mark='b'/> The second example keeps a shared reference into a vector live while requesting a mutation that could reallocate its storage. The borrow checker rejects the conflict. Shared and exclusive access rules, lifetimes and library contracts work together; the slogan many readers or one writer is an introduction, not the entire aliasing model. <bookmark mark='c'/> These mechanisms support memory and data-race safety for safe code when unsafe dependencies uphold their obligations. They do not exclude memory leaks, deadlocks, logic errors or all thread races. The recorded compiler messages demonstrate these two examples on this Rust version.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(mv), run_time=0.6)
            vo.wait_until('a')
            self.play(FadeIn(e1), FadeIn(pts[0]))
            vo.wait_until('b')
            self.play(FadeIn(bw))
            self.play(FadeIn(e2), FadeIn(pts[1]))
            vo.wait_until('c')
            self.play(FadeIn(pts[2:]))
        self.wait(0.3)
        self.clear_scene()
