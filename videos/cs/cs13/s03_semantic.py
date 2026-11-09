from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, mono, region


class Semantic(VoiceoverScene):
    def construct(self):
        self.card()
        self.scopes()
        self.types()
        self.layout()
        self.storage()

    def card(self):
        card = chapter_card(2, r"Names, scopes and types", r"What does each name mean, and how big is each thing?",
                            lit=(1960,), part=PART)
        with self.voiceover("Chapter two. Names, scopes and types."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def scopes(self):
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

    def layout(self):
        sem = load("semantic")
        head = label(r"How big is each thing? \ Layout", font_size=36).to_edge(UP, buff=0.3)
        rules = VGroup(
            label(r"\texttt{int} \ and pointers: \ 4 bytes, \ aligned to 4", font_size=21, color=GREY_A),
            label(r"\texttt{char}: \ 1 byte", font_size=21, color=GREY_A),
            label(r"a struct: \ fields in order, \ each at the next multiple of its alignment; \ size rounded up",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(head, DOWN, buff=0.35)
        unit = 0.62
        cols = [DATA, CTRL, YES, FUNC]

        def strip(name, lay):
            g = VGroup()
            for k, (f, off, t) in enumerate(lay["fields"]):
                r = Rectangle(width=4 * unit, height=0.7, stroke_color=cols[k], fill_color=cols[k], fill_opacity=0.2,
                              stroke_width=1.6)
                r.move_to([off * unit, 0, 0], aligned_edge=LEFT)
                t1 = mono(f, 15, WHITE).move_to(r).shift(UP * 0.12)
                t2 = mono(t, 13, cols[k]).move_to(r).shift(DOWN * 0.15)
                o = mono(str(off), 13, GREY_B).next_to(r, DOWN, buff=0.08).align_to(r, LEFT)
                g.add(VGroup(r, t1, t2, o))
            end = mono(str(lay["size"]), 13, GREY_B).next_to(g[-1][0], DOWN, buff=0.08).align_to(g[-1][0], RIGHT)
            t = label(rf"\texttt{{{name}}}: \ {lay['size']} bytes", font_size=22, color=HEAD)
            t.next_to(g, LEFT, buff=0.4)
            return VGroup(t, g, end)
        node = strip("Node", sem["layouts"]["Node"])
        ent = strip("Entry", sem["layouts"]["Entry"])
        VGroup(node, ent).arrange(DOWN, buff=0.6, aligned_edge=RIGHT).next_to(rules, DOWN, buff=0.55)
        acc = VGroup(mono("p.count", 18, CODE), MathTex(r"\to", font_size=30),
                     mono("lw  t, 12(p)", 18, FUNC)).arrange(RIGHT, buff=0.3)
        acc2 = VGroup(mono("table[i].length", 18, CODE), MathTex(r"\to", font_size=30),
                      mono("lw  t, 4(table + 12*i)", 18, FUNC)).arrange(RIGHT, buff=0.3)
        accs = VGroup(acc, acc2).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN, buff=0.45)
        with self.voiceover("The checker also decides how big each thing is, and where each part of it lives. <bookmark mark='a'/> On Pebble, integers and pointers are four bytes and must sit at addresses divisible by four; a character is one byte. A struct's fields are laid out in order, each at the next multiple of its alignment, and the struct's size is rounded up so that arrays of it stay aligned. <bookmark mark='b'/> The list Job's Node is sixteen bytes: next at zero, letters at four, length at eight, count at twelve. <bookmark mark='c'/> The array Job's Entry is twelve bytes, exactly the layout Part 6 chose by hand. <bookmark mark='d'/> From now on a field is only an offset. p dot count becomes a load from twelve bytes past p, and table of i dot length a load from four bytes past the table plus twelve times i. The names are gone; the numbers remain.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.4), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(node[0]), LaggedStart(*[FadeIn(c) for c in node[1]], lag_ratio=0.3), FadeIn(node[2]), run_time=2)
            vo.wait_until('c')
            self.play(FadeIn(ent))
            vo.wait_until('d')
            self.play(FadeIn(acc))
            self.play(FadeIn(acc2))
        self.wait(0.3)
        self.clear_scene()

    def storage(self):
        head = label(r"Where each variable lives", font_size=36).to_edge(UP, buff=0.3)
        kinds = [
            (r"globals", r"\texttt{head}, \ \texttt{tail}, \ \texttt{table}, \ \texttt{pool}",
             r"a fixed address in the data section", DATA),
            (r"locals", r"\texttt{p}, \ \texttt{i}, \ \texttt{n}", r"a virtual register: \ the back end decides",
             YES),
            (r"address taken", r"\texttt{word} \ in \texttt{main}: \ \texttt{\&word[0]}",
             "addressable storage in this implementation", FUNC),
            (r"arrays and structs", r"\texttt{digits[12]}", r"in memory, \ in the stack frame", CTRL),
        ]
        rows = VGroup()
        for name, ex, where, c in kinds:
            r = VGroup(label(name, font_size=24, color=c), label(ex, font_size=20, color=GREY_A),
                       label(where, font_size=20, color=WHITE))
            r[0].move_to([-6.3, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-3.2, 0, 0], aligned_edge=LEFT)
            r[2].move_to([1.4, 0, 0], aligned_edge=LEFT)
            rows.add(r)
        rows.arrange(DOWN, buff=0.55).next_to(head, DOWN, buff=0.7)
        for r in rows:
            r[0].align_to([-6.3, 0, 0], LEFT)
            r[1].align_to([-3.2, 0, 0], LEFT)
            r[2].align_to([1.4, 0, 0], LEFT)
        foot = label("virtual values may be transformed while preserving defined behavior",
                     font_size=21, color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover("Our checker also records how locals can be represented. <bookmark mark='a'/> Globals receive storage in the data section, with addresses resolved by the compiler and linker. <bookmark mark='b'/> Ordinary scalar locals become virtual registers. Later, the back end assigns physical registers or stack slots. This is an implementation choice, not a claim that every optimization level keeps them in registers. <bookmark mark='c'/> If a local's address is passed elsewhere, its contents may be accessed through a pointer. Our compiler gives such locals memory storage; a more sophisticated compiler could promote them after proving the pointer uses harmless. <bookmark mark='d'/> Our arrays and structs also use stack storage when local. <bookmark mark='e'/> Separating scalar values from observable memory makes analysis simpler. Moving or deleting a computation still requires preserving its effects, possible traps and required result.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, r in zip('abcd', rows):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until('e')
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
