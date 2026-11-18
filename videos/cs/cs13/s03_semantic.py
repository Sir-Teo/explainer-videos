from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, mono, region


class Semantic(WatchScene):
    def construct(self):
        self.card()
        self.scopes()
        self.types()

    def card(self):
        self.chapter(2, r"Names, scopes and types", r"What does each name mean, and how big is each thing?", lit=(1960,), part=PART, said="Chapter two. Names, scopes and types.")

    def scopes(self):
        self.ask(r"Can a grammar check \\ that every name is declared before it's used?", [r"yes", r"no"], 1,
                 say="Can the grammar itself check that every variable was declared before it's used?",
                 reveal="No. That needs memory of everything declared so far: a symbol table.")
        sem = load("semantic")
        head = label(r"Which $p$ is this? \ The symbol table", font_size=36).to_edge(UP, buff=0.3)
        src = code(["var head: *Node = null;", " ", "fn lookup(w: *char, n: int) -> *Node {",
                    "    var p: *Node = head;", "    while p != null {",
                    "        if p.length == n && same(p.letters, w, n) {", "            return p;", "        }",
                    "        p = p.next;", "    }", "    var q: *Node = alloc(sizeof(Node));", "    ...",
                    "    var i: int = 0;", "    ...", "}"], size=15).to_edge(LEFT, buff=0.5).shift(DOWN * 0.25)
        why = label(r"``declared before use'' \ is not context-free \ (Part 12)", font_size=19,
                    color=GREY_A).next_to(head, DOWN, buff=0.2)
        # the scope stack, innermost on top
        frames = []
        for title, entries, c in (
                (r"globals", [(k, v) for k, v in sem["globals"].items()] + [("same", "fn"), ("lookup", "fn"),
                                                                             ("getc", "built-in"),
                                                                             ("alloc", "built-in")], DATA),
                (r"lookup", list(sem["lookup_symbols"].items()), YES)):
            rows = VGroup(*[VGroup(mono(k, 16, WHITE), mono(v, 16, CTRL)).arrange(RIGHT, buff=0.3) for k, v in
                            entries]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            for r in rows:
                r[1].move_to(r[0].get_left() + RIGHT * 1.3, aligned_edge=LEFT)
            box = SurroundingRectangle(rows, buff=0.18, color=c, corner_radius=0.08, stroke_width=1.5)
            t = label(title, font_size=18, color=c).next_to(box, UP, buff=0.06).align_to(box, LEFT)
            frames.append(VGroup(box, rows, t))
        stack = VGroup(frames[1], frames[0]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).to_edge(RIGHT, buff=1.0)
        stack.shift(DOWN * 0.3)
        look = Arrow(frames[1].get_left() + LEFT * 0.1, frames[0].get_left() + LEFT * 0.1, path_arc=1.5,
                     color=HEAD, stroke_width=2, buff=0.05)
        look_t = label(r"not here? \ look outward", font_size=17, color=HEAD).next_to(look, LEFT, buff=0.1)
        use = SurroundingRectangle(src[3], color=HEAD, buff=0.04)
        with self.voiceover(
            "The parser of Part 12 checks the grammar, but a grammar cannot check that every name was declared "
            "before it is used. <bookmark mark='a'/> That needs memory of everything declared so far, which is "
            "beyond a context-free language. So the compiler's next pass walks the tree with a symbol table. "
            "<bookmark mark='b'/> The outermost scope holds the globals and the functions, including the built-ins. "
            "Entering lookup pushes a new scope, with its parameters w and n, and then its locals as they are "
            "declared: p, q and i. <bookmark mark='c'/> When the body says head, the checker looks in the innermost "
            "scope first, finds nothing, and looks outward, to the global. A local of the same name would have "
            "shadowed it. This rule, static or lexical scope, arrived with ALGOL 60's nested blocks, and it means "
            "every use of a name is settled from the text alone, before the program runs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(why))
            vo.wait_until("b")
            self.play(FadeIn(frames[0]))
            self.play(FadeIn(frames[1]))
            vo.wait_until("c")
            self.play(Create(use))
            self.play(Create(look), FadeIn(look_t))
            self.play(Indicate(frames[0][1][0], color=HEAD))
        self.wait(0.3)
        self.clear_scene()

    def types(self):
        sem = load("semantic")
        head = label(r"Types, \ checked by rules", font_size=36).to_edge(UP, buff=0.3)
        rules = VGroup(
            MathTex(r"\frac{\Gamma \vdash e_1 : \texttt{int} \qquad \Gamma \vdash e_2 : \texttt{int}}"
                    r"{\Gamma \vdash e_1 + e_2 : \texttt{int}}", font_size=34),
            MathTex(r"\frac{\Gamma \vdash p : {*T} \qquad \Gamma \vdash i : \texttt{int}}"
                    r"{\Gamma \vdash p[i] : T}", font_size=34),
            MathTex(r"\frac{\Gamma \vdash e : {*S} \qquad S \text{ has field } f : T}"
                    r"{\Gamma \vdash e.f : T}", font_size=34),
        ).arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.45)
        if rules.width > 12.8:
            rules.scale_to_fit_width(12.8)
        gam = label(r"$\Gamma$: \ the symbol table; \ \ $\Gamma \vdash e : T$ \ reads \ ``in scope $\Gamma$, "
                    r"$e$ has type $T$''", font_size=20, color=GREY_A).next_to(rules, DOWN, buff=0.3)
        left_c, right_c = VGroup(), VGroup()
        for src, msg in sem["errors"].items():
            body = src.replace("fn main() -> int { ", "").replace(" }", "").replace("return 0;", "").strip()
            body = body.replace("fn f(a: int) -> int { return a;", "fn f(a: int) -> int {...}")
            left_c.add(mono(body, 15, CODE))
            right_c.add(mono(msg.replace("in main: ", ""), 15, NO))
        left_c.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        right_c.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        for l_, r_ in zip(left_c, right_c):
            r_.set_y(l_.get_y())
        right_c.next_to(left_c, RIGHT, buff=1.0)
        rows = VGroup(*[VGroup(l_, r_) for l_, r_ in zip(left_c, right_c)])
        rows.next_to(gam, DOWN, buff=0.45)
        cap = label(r"our checker's messages, \ on four broken programs", font_size=18, color=GREY_B).next_to(
            rows, UP, buff=0.12).align_to(rows, LEFT)
        nxt = label(r"what types can promise, \ and inferring them unwritten: \ Part 14", font_size=20,
                    color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover("The checker assigns types according to the language's rules. <bookmark mark='a'/> Above each line are premises; below it is the conclusion. Two integer operands produce an integer sum. Indexing a pointer to T by an integer produces an element of type T. Selecting a declared struct field uses that field's type. <bookmark mark='b'/> Gamma records the typing environment, including the current names and their types. Our checker applies these rules while traversing the syntax tree. <bookmark mark='c'/> These four rejected fragments initialize an integer with null, use an undeclared name, select a nonexistent field, or pass the wrong argument count. The messages are our checker's actual output. Without the required checks, an implementation might reject them elsewhere, crash or compute a wrong result; a runtime crash is not guaranteed. <bookmark mark='d'/> Part 14 studies the guarantees of particular type systems and how some types can be inferred.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.5), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(gam))
            vo.wait_until('c')
            self.play(FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.5), run_time=3)
            vo.wait_until('d')
            self.play(FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()


