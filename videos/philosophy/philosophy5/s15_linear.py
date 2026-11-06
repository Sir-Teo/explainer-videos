from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


RULE_TEX = {"⊗": r"$\otimes$", "⊸": r"$\multimap$", "&": r"\&", "⊕": r"$\oplus$"}


def rule_tex(r: str) -> str:
    for k, v in RULE_TEX.items():
        r = r.replace(k, v)
    return r


def proof_tree(p, font_size=26, gap=0.55, hgap=0.6) -> VGroup:
    """Draw a sequent proof tree bottom-up: conclusion at the bottom, a bar, the premises above it."""
    seq = MathTex(p["seq"], font_size=font_size)
    if not p["kids"]:
        bar = Line(LEFT, RIGHT, color=GREY_B, stroke_width=1.5).set_width(seq.width + 0.2).next_to(seq, UP, buff=0.08)
        rl = label(rule_tex(p["rule"]), font_size=font_size - 8, color=CONN).next_to(bar, RIGHT, buff=0.08)
        return VGroup(seq, bar, rl)
    kids = VGroup(*[proof_tree(k, font_size, gap, hgap) for k in p["kids"]]).arrange(RIGHT, buff=hgap,
                                                                                      aligned_edge=DOWN)
    kids.next_to(seq, UP, buff=gap)
    kids.set_x(seq.get_x())
    bar = Line(LEFT, RIGHT, color=GREY_B, stroke_width=1.5).set_width(max(seq.width, kids.width) + 0.2)
    bar.move_to([seq.get_x(), (seq.get_top()[1] + kids.get_bottom()[1]) / 2, 0])
    rl = label(rule_tex(p["rule"]), font_size=font_size - 8, color=CONN).next_to(bar, RIGHT, buff=0.08)
    return VGroup(seq, bar, rl, kids)


class Linear(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Logic as resources", r"What if a premise can be used only once?", lit=(1987,),
                            part=PART)
        with self.voiceover("Chapter fourteen. Logic as resources."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.structural()
        self.machine()
        self.proof()
        self.landscape()

    def structural(self):
        head = label(r"Gentzen's structural rules \ (Part 3): \ they mention no connective", font_size=30,
                     color=CONN).to_edge(UP, buff=0.45)
        rules = [(r"weakening", r"\frac{\Gamma \vdash C}{\Gamma, A \vdash C}", r"an unused premise may be added"),
                 (r"contraction", r"\frac{\Gamma, A, A \vdash C}{\Gamma, A \vdash C}", r"a premise may be used twice"),
                 (r"exchange", r"\frac{\Gamma, A, B \vdash C}{\Gamma, B, A \vdash C}", r"order does not matter")]
        cols = VGroup()
        for n, f, t in rules:
            cols.add(VGroup(label(n, font_size=28, color=GOAL), MathTex(f, font_size=40),
                            label(t, font_size=22, color=GREY_A)).arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.7)
        q = label(r"for truth they are harmless; \ for \textit{resources} they are false", font_size=28,
                  color=BAD).to_edge(DOWN, buff=1.0)
        ex = label(r"a dollar spent cannot be spent again; \ a premise used once is gone", font_size=24,
                   color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Recall Gentzen's sequent calculus from Part 3. Besides a rule for each connective, it has three rules "
            "that mention no connective at all. <bookmark mark='a'/>Weakening: you may add a premise you never "
            "use. Contraction: you may use a premise twice. Exchange: the order of premises does not matter. "
            "<bookmark mark='b'/>If premises are truths, these are harmless: a truth stays true however often you "
            "cite it. <bookmark mark='c'/>But if premises are resources, like money, or memory, or energy, they "
            "are false. A dollar spent cannot be spent again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cols], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.clear_scene()

    def machine(self):
        d = load("linear")
        hc = history_card(1987, r"Jean-Yves Girard", r"`Linear logic', \textit{Theoretical Computer Science}",
                          width=6.2, color=HIST).to_corner(UL, buff=0.3)
        conns = VGroup(label(r"$A \multimap B$: \ spend $A$ to get $B$", font_size=22),
                       label(r"$A \otimes B$: \ both, together", font_size=22),
                       label(r"$A \mathbin{\&} B$: \ either, \ your choice", font_size=22),
                       label(r"$A \oplus B$: \ one of them, \ not your choice", font_size=22)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.35)
        hd = [label(r"sequent", font_size=22, color=P.CLAIM), label(r"linear", font_size=22, color=P.CLAIM),
              label(r"classical", font_size=22, color=P.CLAIM)]
        rows = [[MathTex(r",\ ".join(r_["hyps"]) + r" \vdash " + r_["goal"], font_size=28), r_["provable"],
                 r_["classical"]] for r_ in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[7.4, 1.5, 1.8], cell_h=0.6, font_size=26).move_to([0, -0.9, 0])
        with self.voiceover(
            "In 1987 Jean-Yves Girard published linear logic, which drops weakening and contraction. Every premise "
            "must be used, exactly once. <bookmark mark='a'/>Its connectives split the classical ones in two. The "
            "lollipop: spend A to get B. Tensor: both, together. With: either one, your choice. Plus: one of them, "
            "but not your choice. <bookmark mark='b'/>The Reasoner's new prover runs a vending machine. A dollar, "
            "and 'a dollar buys a coffee', give a coffee. <bookmark mark='c'/>One dollar and two offers do not "
            "give a coffee and a tea, though classical logic says they do: classically, the dollar is used twice. "
            "<bookmark mark='d'/>Two dollars do. <bookmark mark='e'/>A menu, 'a dollar buys coffee with tea', lets "
            "you choose tea, but not have both. <bookmark mark='f'/>And if the machine picks for you, coffee plus "
            "tea, you cannot count on coffee."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(conns))
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            for mk, idx in (("b", [0]), ("c", [1]), ("d", [2]), ("e", [3, 4]), ("f", [5])):
                vo.wait_until(mk)
                self.play(*[FadeIn(grid.cell[r][c]) for r in idx for c in range(3)])
        self.clear_scene()

    def proof(self):
        d = load("linear")
        p = d["rows"][2]["proof"]
        tree = proof_tree(p, font_size=26).move_to([0, 0.2, 0])
        if tree.width > 13.0:
            tree.width = 13.0
        head = label(r"The Reasoner's proof: \ each dollar is spent exactly once", font_size=30, color=CONN).to_edge(
            UP, buff=0.45)
        cap = label(r"$\otimes$R splits the resources between the two drinks; \ each $\multimap$L spends one dollar",
                    font_size=24, color=GOAL).to_edge(DOWN, buff=0.5)
        st = d["structural"]
        assert not st["contraction"] and not st["weakening"] and st["exchange"]
        with self.voiceover(
            "Here is the proof the Reasoner found for two dollars. <bookmark mark='a'/>Read it from the bottom. To "
            "get a coffee and a tea, split the resources: one dollar and the coffee offer for the coffee, the other "
            "dollar and the tea offer for the tea. <bookmark mark='b'/>Each half spends its dollar, and ends in an "
            "axiom, where a single resource is exactly what is needed. Nothing is left over, and nothing is used "
            "twice. <bookmark mark='c'/>The search works because, without contraction, every rule makes the "
            "sequent smaller. For this fragment, provability is decidable."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tree[0]), Create(tree[1]), FadeIn(tree[2]))
            self.play(FadeIn(tree[3]))
            vo.wait_until("b")
            self.play(Indicate(tree[3], color=GOAL))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.clear_scene()

    def landscape(self):
        head = label(r"The substructural landscape", font_size=34, color=CONN).to_edge(UP, buff=0.45)
        rows = [(r"no weakening", r"relevance logics \ (Chapter 7)"),
                (r"no contraction", r"naive truth and naive sets without Curry's paradox \ (Grišin 1974; Zardini 2011)"),
                (r"no exchange", r"the Lambek calculus: \ grammar as logic \ (Lambek 1958)"),
                (r"no cut", r"the tolerant ST \ (Chapter 12)"),
                (r"used at most once", r"Rust's ownership; \ session types; \ quantum no-cloning")]
        tab = VGroup()
        for i, (a, b) in enumerate(rows):
            y = 1.7 - 0.85 * i
            l1 = label(a, font_size=26, color=GOAL)
            l2 = label(b, font_size=24)
            l1.move_to([-6.0 + l1.width / 2, y, 0])
            l2.move_to([-2.4 + l2.width / 2, y, 0])
            tab.add(VGroup(l1, l2))
        moral = label(r"a logic is partly a theory of what premises \textit{are}", font_size=26, color=OK).to_edge(
            DOWN, buff=0.45)
        with self.voiceover(
            "Dropping each structural rule gives a family of logics. <bookmark mark='a'/>Without weakening, the "
            "relevance logics of Chapter 7. <bookmark mark='b'/>Without contraction, a remarkable escape: naive "
            "theories of truth and of sets, which classical logic makes inconsistent, become consistent, because "
            "the paradoxes use a premise twice. <bookmark mark='c'/>Without exchange, the Lambek calculus of 1958, "
            "in which a grammatical sentence is a proof and word order matters. <bookmark mark='d'/>Without cut, "
            "the tolerant logic of Chapter 12. <bookmark mark='e'/>And in computing, values used at most once: the "
            "ownership rules of the Rust language, typed communication protocols, and the quantum fact that an "
            "unknown state cannot be copied. <bookmark mark='f'/>A logic is partly a theory of what premises are."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(moral))
        self.clear_scene()
