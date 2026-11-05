from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono


def tick(s: str) -> str:
    return s.replace("'", "'")


class Inference(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.unify()
        self.trace()
        self.letpoly()
        self.job()
        self.worst()

    def card(self):
        card = chapter_card(10, r"Hindley--Milner inference", r"Can the machine find the types itself?",
                            lit=(1978,), extra=((1978, r"Milner: \ algorithm W"),), part=PART)
        with self.voiceover("Chapter ten. Hindley Milner inference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def idea(self):
        head = label(r"Types as unknowns", font_size=36).to_edge(UP, buff=0.3)
        src = mono("fun f x -> f (f x)", 28, CODE).next_to(head, DOWN, buff=0.5)
        steps = VGroup(
            label(r"give every unknown a type variable: \ $f : \alpha$, \ $x : \beta$", font_size=24, color=GREY_A),
            label(r"each use adds an equation: \ $f\,x$ \ says \ $\alpha = \beta \to \gamma$", font_size=24,
                  color=GREY_A),
            label(r"$f\,(f\,x)$ \ says \ $\alpha = \gamma \to \delta$", font_size=24, color=GREY_A),
            label(r"solve the equations: \ \textbf{unification}", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(src, DOWN, buff=0.5)
        with self.voiceover(
            "In the hook, nobody wrote a type, yet the machine knew them all. Here is how. <bookmark mark='a'/> "
            "Take the function that applies f twice. <bookmark mark='b'/> Give each unknown a type variable: f has "
            "some type alpha, x some type beta. <bookmark mark='c'/> Every use adds an equation. f applied to x "
            "says alpha must be a function from beta to some gamma. <bookmark mark='d'/> And f applied to f of x "
            "says alpha is also a function from gamma to some delta. <bookmark mark='e'/> Inference is solving "
            "these equations between types, which is called unification."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src))
            for mk, s in zip("bcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def unify(self):
        head = label(r"Unification \ (Robinson, \ 1965)", font_size=36).to_edge(UP, buff=0.3)
        rules = VGroup(
            label(r"$\alpha = T$: \ bind $\alpha$ to $T$ everywhere \ --- \ unless $\alpha$ occurs in $T$", font_size=23,
                  color=GREY_A),
            label(r"$A \to B \;=\; C \to D$: \ \ solve $A = C$ \ and \ $B = D$", font_size=23, color=GREY_A),
            label(r"$\mathsf{int} = \mathsf{bool}$, \ or \ $A \to B = \mathsf{int}$: \ a type error", font_size=23,
                  color=NO),
            label(r"the occurs check: \ $\alpha = \alpha \to \beta$ \ has no finite solution \ ($\Omega$, \ chapter 9)",
                  font_size=23, color=NO),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=0.9)
        res = label(r"the result is the \textbf{most general} solution: \ every other solution is an instance of it",
                    font_size=23, color=HEAD).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Alan Robinson gave the algorithm in 1965, for automated theorem proving. <bookmark mark='a'/> An "
            "equation between a variable and a type binds the variable to that type, everywhere it appears. "
            "<bookmark mark='b'/> An equation between two function types splits into two equations: arguments "
            "equal, results equal. <bookmark mark='c'/> Two different type constructors, like int and bool, cannot "
            "be equal: that is a type error. <bookmark mark='d'/> And a variable cannot be bound to a type that "
            "contains it: that would be the infinite type of omega. <bookmark mark='e'/> When unification "
            "succeeds, it finds the most general solution, of which every other solution is a special case."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rules):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def trace(self):
        h = load("hm")
        head = label(r"Our engine, \ step by step", font_size=34).to_edge(UP, buff=0.3)
        src = mono("fun f x -> f (f x)", 24, CODE).next_to(head, DOWN, buff=0.35)
        words = {"assume": r"assume", "bind": r"bind", "unify": r"unify"}
        rows = VGroup()
        for st in h["twice"]["trace"]:
            kind = st[0]
            if kind == "assume":
                txt = f"{st[1]} : {st[2]}"
            elif kind == "bind":
                txt = f"{st[1]} := {st[2]}"
            else:
                txt = f"{st[1]}  =  {st[2]}"
            rows.add(VGroup(label(words[kind], font_size=20, color=HEAD), mono(txt, 22, WHITE)).arrange(RIGHT,
                                                                                                    buff=0.5))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(src, DOWN, buff=0.5)
        for r in rows:
            r[1].set_x(rows.get_left()[0] + 2.0 + r[1].width / 2)
        res = VGroup(label(r"principal type:", font_size=22, color=GREY_A),
                     mono(h["twice"]["type"], 26, YES)).arrange(RIGHT, buff=0.4).next_to(rows, DOWN, buff=0.5)
        cmp = VGroup(label(r"and composition:", font_size=20, color=GREY_A),
                     mono("fun f g x -> f (g x)  :  " + h["compose"]["type"], 20, YES)).arrange(
            RIGHT, buff=0.4).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is our engine's own trace for twice. <bookmark mark='a'/> It assumes fresh variables for f and x. "
            "From f of x it binds f's variable to a function from x's variable to a new one. From the outer "
            "application it must unify that function type with another, which splits into two bindings. <bookmark "
            "mark='b'/> What is left is the principal type: for any type tick a, a function from tick a to tick a, "
            "then a tick a, gives a tick a. <bookmark mark='c'/> Composition comes out just as neatly, with three "
            "independent type variables. This is algorithm W, from Milner's 1978 paper; Roger Hindley had found the "
            "principal types of combinatory logic in 1969."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            for r in rows:
                self.play(FadeIn(r, shift=RIGHT * 0.1), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(cmp))
        self.wait(0.3)
        self.clear_scene()

    def letpoly(self):
        h = load("hm")
        head = label(r"let-polymorphism", font_size=36).to_edge(UP, buff=0.3)
        rows, cols = [], []
        for c in h["cases"][:3]:
            rows.append([c["src"], c["type"] or c["error"]])
            cols.append([WHITE, YES if c["type"] else NO])
        tab = grid_table([r"program", r"inferred"], rows, widths=[6.6, 4.6], row_h=0.6, font_size=21, colors=cols,
                         mono_cols=(0, 1)).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"a \texttt{let}-bound name is \textbf{generalized}: \ \texttt{id} $: \forall \alpha.\; \alpha \to "
                  r"\alpha$, \ fresh at each use", font_size=22, color=YES),
            label(r"a $\lambda$-bound name is not: \ one parameter, \ one type", font_size=22, color=NO),
            label(r"the price of decidability: \ full polymorphism, \ System F, \ cannot be inferred \ (Wells, \ 1994)",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "One more ingredient makes this practical. <bookmark mark='a'/> Bind the identity function with let, "
            "and use it on a number and on a boolean: the program has type int times bool. But pass the identity "
            "in as a parameter, and use it the same two ways, and inference fails. <bookmark mark='b'/> A "
            "let-bound name is generalized: once its type is found, the free type variables become for all, and "
            "each use gets fresh copies. <bookmark mark='c'/> A lambda-bound parameter is not, because its uses "
            "must agree. <bookmark mark='d'/> This restriction is the price of decidability. Joe Wells proved in "
            "1994 that inference for full polymorphism, the next chapter's System F, is undecidable."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]])
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in tab.cells[1]])
            self.play(*[FadeIn(c) for c in tab.cells[2]])
            vo.wait_until("b")
            self.play(FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]), *[FadeIn(c) for c in tab.cells[3]])
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def job(self):
        h = load("hm")
        head = label(r"The Job's types, \ inferred", font_size=34).to_edge(UP, buff=0.3)
        rows = [[n, t] for n, t in h["job"]["types"]]
        tab = grid_table([r"definition", r"principal type"], rows, widths=[2.6, 8.0], row_h=0.4, font_size=19,
                         mono_cols=(0, 1)).next_to(head, DOWN, buff=0.4)
        cap = label(rf"{len(rows)} definitions, \ {h['job']['unify_calls']} unifications, \ no annotations; \ "
                    r"type variables mark what each function does not care about", font_size=20, color=HEAD).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Here is the whole Job, as the hook promised. <bookmark mark='a'/> Eleven definitions, a few hundred "
            "unifications, and not one annotation. Reverse works on lists of anything. Lower and is letter work on "
            "character codes. Bump and count work for any type of word that supports equality, and insert and sort "
            "for any pair whose second part is a count. <bookmark mark='b'/> The type variables are a precise "
            "statement of what each function does not care about, discovered rather than declared."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]],
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def worst(self):
        h = load("hm")
        head = label(r"The worst case: \ types that explode", font_size=34).to_edge(UP, buff=0.3)
        src = VGroup(*[mono(l, 18, CODE) for l in h["exp_source"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        src.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        t1 = VGroup(label(r"type of \texttt{f1}:", font_size=19, color=GREY_B),
                    mono(h["exp"][0]["shown"], 18, YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        t1.next_to(src, RIGHT, buff=0.8).align_to(src, UP)
        rows = [[f"f{r['n']}", f"2^{r['log2_size']}", f"{r['unify_calls']}", f"{1000 * r['seconds']:.2f} ms"]
                for r in h["exp"]]
        tab = grid_table([r"function", r"leaves of its type", r"unifications", r"time"], rows,
                         widths=[1.8, 3.0, 2.2, 1.8], row_h=0.42, font_size=20, mono_cols=(0, 1, 2, 3)).next_to(
            src, DOWN, buff=0.5).set_x(0)
        pts = VGroup(
            label(r"each line squares the type: \ $2^{2^n}$ leaves", font_size=21, color=NO),
            label(r"kept as a shared graph, \ our engine stays fast; \ printed out, \ \texttt{f5}'s type has four "
                  r"billion leaves", font_size=21, color=GREY_A),
            label(r"in general, \ typability in ML is DEXPTIME-complete \ (Mairson; \ Kfoury, Tiuryn, Urzyczyn; \ "
                  r"1990)", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Inference is fast on real programs, but it has a famous worst case. <bookmark mark='a'/> f zero pairs "
            "its argument with itself. f one applies f zero twice, so its result is a pair of pairs. <bookmark "
            "mark='b'/> Each new line applies the previous function twice, and the type squares in size: after n "
            "lines, two to the two to the n leaves. <bookmark mark='c'/> Our engine keeps types as a shared graph, "
            "so it handles even f five in under a millisecond, but written out, f five's type would have four "
            "billion leaves. <bookmark mark='d'/> Mairson, and Kfoury, Tiuryn and Urzyczyn, proved in 1990 that "
            "deciding whether an ML program is typable is complete for exponential time. Nobody writes such "
            "programs, which is why the algorithm is used everywhere anyway."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src[:2]), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(src[2:]), FadeIn(tab), FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
