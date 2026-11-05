from __future__ import annotations

from videos.philosophy.philosophy2.common import *  # noqa: F403

RULES = [
    (r"\land\mathrm{I}", r"\dfrac{A \qquad B}{A \land B}"),
    (r"\land\mathrm{E}", r"\dfrac{A \land B}{A}"),
    (r"\lor\mathrm{I}", r"\dfrac{A}{A \lor B}"),
    (r"\lor\mathrm{E}", r"\dfrac{A \lor B \quad [A]\cdots C \quad [B]\cdots C}{C}"),
    (r"\to\mathrm{I}", r"\dfrac{[A]\cdots B}{A \to B}"),
    (r"\to\mathrm{E}", r"\dfrac{A \to B \qquad A}{B}"),
    (r"\lnot\mathrm{I}", r"\dfrac{[A]\cdots \bot}{\lnot A}"),
    (r"\lnot\mathrm{E}", r"\dfrac{A \qquad \lnot A}{\bot}"),
    (r"\bot\mathrm{E}", r"\dfrac{\bot}{B}"),
    (r"\lnot\lnot\mathrm{E}", r"\dfrac{\lnot\lnot A}{A}"),
]


def fitch_lines(d):
    return [(a, b, c, [tuple(x) if isinstance(x, list) else x for x in refs]) for a, b, c, refs in d["lines"]]


class Deduction(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Natural deduction", r"Can we prove instead of tabulating?", lit=(1935,), part=PART)
        with self.voiceover("Chapter six. Natural deduction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rules()
        self.tollens()
        self.checker()
        self.classical()

    def rules(self):
        cards = VGroup()
        for name, frac in RULES:
            m = MathTex(frac, font_size=32)
            n = MathTex(name, font_size=26, color=CONN).next_to(m, RIGHT, buff=0.15)
            cards.add(VGroup(m, n))
        cards.arrange_in_grid(rows=2, cols=5, buff=(0.45, 0.6)).move_to([0, -1.0, 0])
        if cards.width > 13.2:
            cards.width = 13.2
        for c in cards:
            c.set_opacity(0.18)
        classical = label(r"classical only", font_size=20, color=GOAL).next_to(cards[-1], DOWN, buff=0.15)
        hcs = VGroup(history_card(1934, r"Stanisław Jaśkowski", r"", width=3.6, color=HIST, font_size=20),
                     history_card(1935, r"Gerhard Gentzen", r"\textit{Untersuchungen über das logische Schließen}",
                                  width=5.2, color=HIST, font_size=20)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Truth tables tell you whether an argument is valid. They don't tell you why, and they don't scale. "
            "Proofs do both: a chain of small steps, each licensed by a rule, from the premises to the conclusion. "
            "<bookmark mark='a'/>In 1934 and 1935, Stanisław Jaśkowski and Gerhard Gentzen independently designed a "
            "proof system meant to look like ordinary reasoning, and Gentzen called it natural deduction. "
            "<bookmark mark='b'/>Every connective gets two kinds of rule: one to introduce it, one to eliminate it."
        ) as vo:
            self.play(FadeIn(cards))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in hcs], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[c.animate.set_opacity(1.0) for c in cards[:-1]], lag_ratio=0.12), run_time=3)
            self.play(cards[-1].animate.set_opacity(0.55), FadeIn(classical))
        imp = cards[4]
        with self.voiceover(
            "Some rules simply say what the connective means. From A and from B, infer A and B; from A and B, infer "
            "A. <bookmark mark='a'/>Others use temporary assumptions. To prove 'if A then B', assume A, derive B under "
            "that assumption, then discharge it and conclude 'if A then B'. That is conditional proof. "
            "<bookmark mark='b'/>Negation works the same way: if assuming A leads to a contradiction, the false "
            "constant written as an upside-down T, conclude not A. And from a contradiction, anything follows."
        ) as vo:
            self.play(Indicate(cards[0], color=CONN), Indicate(cards[1], color=CONN))
            vo.wait_until("a")
            self.play(Indicate(imp, color=GOAL, scale_factor=1.15))
            vo.wait_until("b")
            self.play(Indicate(cards[6], color=GOAL, scale_factor=1.15), Indicate(cards[8], color=CONN))
        self.clear_scene()

    def tollens(self):
        d = load("proofs")["modus_tollens"]
        lines = fitch_lines(d)
        fv = FitchView(lines, font_size=36, line_h=0.66, indent=0.5, center=[-0.6, -0.2, 0], just_x=2.6)
        hc = history_card(1952, r"Frederic Fitch", r"boxes for temporary assumptions", width=4.2, color=HIST)
        hc.to_corner(UR, buff=0.35)
        say = [r"premise", r"premise", r"assume $p$, for now", r"$\to$E: modus ponens on lines 1 and 3",
               r"$q$ and $\lnot q$: a contradiction", r"$\lnot$I: discharge the assumption"]
        ok_ = load("proofs")["modus_tollens"]["ok"]
        verdict = label(r"checked by the Reasoner: \ valid", font_size=26, color=OK).to_corner(DR, buff=0.4)
        assert ok_
        with self.voiceover(
            "Here is modus tollens, proved rather than tabulated, in the layout Frederic Fitch introduced in 1952. "
            "<bookmark mark='a'/>The premises: if p then q; not q. <bookmark mark='b'/>Now assume p, for the sake of "
            "argument. The bar marks how long the assumption lives. <bookmark mark='c'/>From p and 'if p then q', q: "
            "that is arrow elimination. <bookmark mark='d'/>But we also have not q: a contradiction. "
            "<bookmark mark='e'/>So the assumption has to go. Close its box, and conclude not p. Six lines, each one a "
            "rule anyone can check."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(fv.bars[0]))
            vo.wait_until("a")
            self.play(*[FadeIn(m) for m in fv.line[0]], *[FadeIn(m) for m in fv.line[1]], FadeIn(fv.bars[-1]))
            vo.wait_until("b")
            self.play(*[FadeIn(m) for m in fv.line[2]], *[Create(b) for b in fv.bars[1:-1]])
            vo.wait_until("c")
            self.play(*[FadeIn(m) for m in fv.line[3]])
            vo.wait_until("d")
            self.play(*[FadeIn(m) for m in fv.line[4]])
            vo.wait_until("e")
            self.play(*[FadeIn(m) for m in fv.line[5]])
            self.play(FadeIn(verdict))
        self.clear_scene()

    def checker(self):
        P_ = load("proofs")
        good = FitchView(fitch_lines(P_["modus_tollens"]), font_size=30, line_h=0.56, center=[-3.4, 0.2, 0],
                         just_x=1.6)
        bad_lines = fitch_lines(P_["broken"])
        bad = FitchView(bad_lines, font_size=30, line_h=0.56, center=[3.4, 0.2, 0], just_x=1.6)
        bad.line[-1][1].set_color(BAD)
        gv = label(r"accepted", font_size=28, color=OK).next_to(good, DOWN, buff=0.4)
        msg = P_["broken"]["message"]
        bv = label(rf"rejected: {msg}", font_size=24, color=BAD).next_to(bad, DOWN, buff=0.4)
        if bv.width > 6.4:
            bv.width = 6.4
        arrow = Arrow(bad.line[-1][1].get_left() + LEFT * 0.1, bad.line[3][1].get_left() + LEFT * 0.1,
                      path_arc=-1.6, color=BAD, stroke_width=3, buff=0.05)
        head = label(r"the Reasoner's proof checker", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Checking a proof is mechanical, so the Reasoner does it: it looks at each line, the rule it cites and "
            "the lines that rule uses. <bookmark mark='a'/>It accepts our proof. <bookmark mark='b'/>Now change the "
            "last line: instead of discharging the assumption, reuse the q we derived inside the box. "
            f"<bookmark mark='c'/>The checker refuses: {msg}. That q only held while p was assumed. Never use what "
            "was only assumed for the sake of argument: that rule is the whole point of the boxes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(good))
            vo.wait_until("a")
            self.play(FadeIn(gv))
            vo.wait_until("b")
            self.play(FadeIn(bad))
            self.play(Create(arrow))
            vo.wait_until("c")
            self.play(FadeIn(bv))
        self.clear_scene()

    def classical(self):
        P_ = load("proofs")
        pe = P_["peirce"]
        lines = fitch_lines(pe)
        fv = FitchView(lines, font_size=30, line_h=0.5, indent=0.42, center=[-2.0, -0.3, 0], just_x=2.2)
        k = next(i for i, l in enumerate(lines) if l[2] == "dne")
        hl = SurroundingRectangle(VGroup(*fv.line[k]), buff=0.08, color=GOAL, stroke_width=2.5)
        title = fmath(pe["goal"], font_size=40, color=GOAL).to_corner(UR, buff=0.45)
        tl = label(r"Peirce's law", font_size=26, color=GREY_A).next_to(title, DOWN, buff=0.15)
        lem = fmath(P_["excluded_middle"]["goal"], font_size=40, color=GOAL).next_to(tl, DOWN, buff=0.5)
        lml = label(r"excluded middle", font_size=26, color=GREY_A).next_to(lem, DOWN, buff=0.15)
        both = VGroup(title, tl, lem, lml)
        both.set_x(4.6)
        rule = VGroup(MathTex(r"\dfrac{\lnot\lnot A}{A}", font_size=44), MathTex(r"\lnot\lnot\mathrm{E}",
                                                                               font_size=30, color=GOAL))
        rule.arrange(RIGHT, buff=0.2).next_to(lml, DOWN, buff=0.6)
        brouwer = label(r"drop it: intuitionistic logic (Brouwer; Part 9)", font_size=24, color=GREY_A)
        brouwer.next_to(rule, DOWN, buff=0.3)
        if brouwer.get_right()[0] > 6.9:
            brouwer.shift(LEFT * (brouwer.get_right()[0] - 6.9))
        assert pe["classical"] and P_["excluded_middle"]["classical"]
        with self.voiceover(
            f"Not every tautology comes so easily. Here is Peirce's law, proved in {len(lines)} lines with two nested "
            "assumptions. <bookmark mark='a'/>Look at the line that does the real work. It drops a double negation: "
            "from not not p, infer p. <bookmark mark='b'/>Excluded middle, p or not p, needs the same rule, and so does "
            "every proof of Peirce's law."
        ) as vo:
            self.play(FadeIn(fv), FadeIn(title), FadeIn(tl), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(hl))
            vo.wait_until("b")
            self.play(FadeIn(lem), FadeIn(lml))
        with self.voiceover(
            "Remove that one rule and you get intuitionistic logic, the logic of the Dutch mathematician L. E. J. "
            "Brouwer. <bookmark mark='a'/>Brouwer held that to assert 'p or not p' you must be able to say which, and "
            "that a proof of 'not not p' is not yet a proof of p. Every table in this part says that excluded middle "
            "is a tautology, so on his view the tables themselves assume too much. Part 9 builds his logic, with its "
            "own semantics. One innocent-looking rule marks one of the deepest divides in the philosophy of "
            "mathematics."
        ) as vo:
            self.play(FadeIn(rule))
            vo.wait_until("a")
            self.play(FadeIn(brouwer))
        self.clear_scene()
