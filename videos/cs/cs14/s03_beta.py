from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.lam import beta, find_redex, parse
from videos.cs.cs14.common import APP, CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, lam_tree, load, mono


def marked(tex: str, font_size=30, color=HEAD):
    """A term whose redex is wrapped in {{...}}: the redex coloured."""
    if "{{" not in tex:
        return MathTex(tex, font_size=font_size)
    a, rest = tex.split("{{", 1)
    depth, i = 1, 0
    while depth:
        if rest.startswith("{{", i):
            depth += 1
            i += 2
        elif rest.startswith("}}", i):
            depth -= 1
            i += 2
        else:
            i += 1
    mid, b = rest[:i - 2], rest[i:]
    parts = [p for p in (a, mid, b) if p]
    m = MathTex(*parts, font_size=font_size)
    m[parts.index(mid)].set_color(color)
    return m


class Beta(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.trees()
        self.plus()
        self.omega()

    def card(self):
        card = chapter_card(2, r"Reduction and normal forms", r"How does a function compute?", lit=(1936,),
                            part=PART)
        with self.voiceover("Chapter two. Reduction and normal forms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rule(self):
        head = label(r"One rule: \ $\beta$-reduction", font_size=36).to_edge(UP, buff=0.3)
        r = MathTex(r"(\lambda x.\, t)\; s", r"\;\;\to_\beta\;\;", r"t[x := s]", font_size=54).next_to(head, DOWN,
                                                                                                   buff=0.6)
        r[0].set_color(HEAD)
        notes = VGroup(
            label(r"a function applied to an argument is a \textbf{redex}: \ a reducible expression", font_size=24,
                  color=GREY_A),
            label(r"replace it by the body, \ with the argument substituted for the parameter", font_size=24,
                  color=GREY_A),
            label(r"it may be anywhere inside a term, \ even under a $\lambda$", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(r, DOWN, buff=0.6)
        ex = MathTex(r"(\lambda x.\, x\;x)\;z \;\to_\beta\; z\;z", font_size=40, color=YES).next_to(notes, DOWN,
                                                                                                 buff=0.5)
        with self.voiceover(
            "The calculus computes with a single rule, called beta reduction. <bookmark mark='a'/> Wherever a "
            "lambda is applied to an argument, the pair is a redex, a reducible expression. <bookmark mark='b'/> "
            "Replace it by the function's body, with the argument substituted for the parameter. <bookmark "
            "mark='c'/> A redex can sit anywhere inside a larger term, even inside the body of another lambda, "
            "and any redex may be reduced at any time. <bookmark mark='d'/> Lambda x, x x applied to z becomes z "
            "z. That is all there is."
        ) as vo:
            self.play(FadeIn(head), Write(r))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    def trees(self):
        head = label(r"A step, \ on the tree", font_size=34).to_edge(UP, buff=0.3)
        t0 = parse(r"(\x. x x) ((\y. y) z)")
        p0 = find_redex(t0)
        t1 = beta(t0, p0)
        t2 = beta(t1, find_redex(t1))
        trees = [lam_tree(t, dx=0.7, dy=0.62, font_size=19) for t in (t0, t1, t2)]
        for k, tr in enumerate(trees):
            tr.move_to([-4.4 + 4.4 * k, -0.3, 0])
        labels = VGroup(*[mono(s, 17, CODE).next_to(trees[k], DOWN, buff=0.35) for k, s in
                          enumerate(("(λx. x x) ((λy. y) z)", "(λy. y) z ((λy. y) z)", "z ((λy. y) z)"))])
        arrows = VGroup(*[MathTex(r"\to_\beta", font_size=30, color=GREY_B).move_to([-2.2 + 4.4 * k, -0.3, 0])
                          for k in range(2)])
        root_box = SurroundingRectangle(trees[0], color=HEAD, buff=0.1)
        dup = label(r"the argument is copied: \ \textit{two} redexes now, \ one for each use of $x$", font_size=21,
                    color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover("Here is a step on the tree. <bookmark mark='a'/> The whole term is a redex: lambda x, x x, applied to an argument that is itself a redex. <bookmark mark='b'/> Reducing the outer one substitutes the argument for both occurrences of x. The argument has been copied, and its redex with it: now there are two. <bookmark mark='c'/> Reduce the first copy, and one remains. This copying is the source of most of what follows: of the cost differences between strategies, and of the reasons a compiler shares work instead of repeating it.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(trees[0]), FadeIn(labels[0]), Create(root_box), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(arrows[0]), FadeIn(trees[1]), FadeIn(labels[1]), FadeIn(dup))
            vo.wait_until('c')
            self.play(FadeIn(arrows[1]), FadeIn(trees[2]), FadeIn(labels[2]))
        self.wait(0.3)
        self.clear_scene()

    def plus(self):
        b = load("beta")
        head = label(r"$2 + 3$, \ one redex at a time", font_size=34).to_edge(UP, buff=0.3)
        defs = VGroup(
            MathTex(r"\underline{2} = \lambda f\,x.\; f\,(f\,x) \qquad \underline{3} = \lambda f\,x.\; f\,(f\,(f\,x))",
                    font_size=30),
            MathTex(r"\mathit{plus} = \lambda m\,n\,f\,x.\; m\,f\,(n\,f\,x)", font_size=30),
        ).arrange(DOWN, buff=0.15).next_to(head, DOWN, buff=0.3)
        steps = VGroup(*[marked(s["tex"], 26) for s in b["plus"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        steps.next_to(defs, DOWN, buff=0.4)
        if steps.width > 13:
            steps.scale_to_fit_width(13)
        cap = label(r"the redex reduced next, \ in yellow; \ the last term has none: \ a \textbf{normal form}",
                    font_size=20, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover("Here is two plus three again, slowly. <bookmark mark='a'/> A numeral n is the function that applies f to x n times, and plus takes m and n and applies f m times on top of n applications. <bookmark mark='b'/> Each line reduces the redex shown in yellow. First plus swallows its arguments, one at a time. Then three is applied to f and x, and expands into three applications of f, and two adds two more on the outside. <bookmark mark='c'/> The last line has no redex left. It is a normal form: the answer, five applications of f.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(defs), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            for s in steps[:-1]:
                self.play(FadeIn(s, shift=DOWN * 0.05), run_time=0.8)
            vo.wait_until('c')
            self.play(FadeIn(steps[-1]), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def omega(self):
        b = load("beta")
        head = label(r"Terms that never stop", font_size=36).to_edge(UP, buff=0.3)
        om = MathTex(r"\Omega \;=\; (\lambda x.\, x\,x)\;(\lambda x.\, x\,x)", font_size=44).next_to(head, DOWN,
                                                                                                 buff=0.5)
        loop = MathTex(r"\Omega \;\to_\beta\; \Omega \;\to_\beta\; \Omega \;\to_\beta\; \cdots", font_size=40,
                       color=NO).next_to(om, DOWN, buff=0.4)
        note = label(r"it reduces to itself: \ no normal form", font_size=22, color=NO).next_to(loop, DOWN,
                                                                                               buff=0.25)
        k = MathTex(r"(\lambda x\,y.\; y)\;\Omega\;z", font_size=40).next_to(note, DOWN, buff=0.6)
        ways = VGroup(
            label(rf"reduce the outside first: \ $z$, \ in {b['k_normal']} steps", font_size=22, color=YES),
            label(r"reduce $\Omega$ first: \ forever", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.15).next_to(k, DOWN, buff=0.3)
        q = label(r"so the order of reduction matters: \ chapter 5", font_size=22, color=HEAD).to_edge(DOWN,
                                                                                                       buff=0.45)
        with self.voiceover("Not every term has a normal form. <bookmark mark='a'/> Omega applies lambda x, x x to itself. <bookmark mark='b'/> One step of beta reduction gives back exactly the same term, and the next step the same again, forever. Omega has no normal form: it is the lambda calculus's infinite loop. <bookmark mark='c'/> Worse, some terms have a normal form along one path and loop along another. Here is a function that ignores its first argument, applied to omega and to z. <bookmark mark='d'/> Reduce the outside first and the answer is z, in two steps. Insist on reducing omega first, and you never finish. <bookmark mark='e'/> So the order of reduction matters. Chapter five studies it.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Write(om), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(loop), FadeIn(note))
            vo.wait_until('c')
            self.play(FadeIn(k))
            vo.wait_until('d')
            self.play(FadeIn(ways))
            vo.wait_until('e')
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()
