from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403

FOLTEX = lambda s: fol.show(fol.parse(s), tex=True)  # noqa: E731


def rule_figure(tops, bottom, name, cond="", color=CONN, font_size=32):
    """An inference figure: premises above a bar, the conclusion below, the rule's name at the right."""
    top = VGroup(*[MathTex(t, font_size=font_size) for t in tops]).arrange(RIGHT, buff=0.6)
    bot = MathTex(bottom, font_size=font_size, color=GOAL)
    w = max(top.width, bot.width) + 0.3
    bar = Line(LEFT * w / 2, RIGHT * w / 2, color=GREY_B, stroke_width=2)
    fig = VGroup(top, bar, bot).arrange(DOWN, buff=0.12)
    nm = MathTex(name, font_size=font_size - 2, color=color).next_to(bar, RIGHT, buff=0.15)
    g = VGroup(fig, nm)
    if cond:
        g.add(label(cond, font_size=20, color=GREY_A).next_to(fig, DOWN, buff=0.18))
    return g


class Proof(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Proving with quantifiers", r"What are the rules for `all' and `some'?",
                            lit=(1935,), part=PART)
        with self.voiceover("Chapter five. Proving with quantifiers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rules()
        self.hasty()
        self.good_proof()
        self.bad_proof()
        self.drinker()
        self.gentzen()

    def rules(self):
        hc = history_card(1935, r"Gerhard Gentzen", r"`Investigations into logical deduction': natural deduction "
                          r"and the sequent calculus", width=6.4, color=HIST).to_corner(UL, buff=0.35)
        figs = VGroup(
            rule_figure([r"\forall x\, \varphi(x)"], r"\varphi(t)", r"\forall\mathrm{E}", r"any term $t$"),
            rule_figure([r"\varphi(t)"], r"\exists x\, \varphi(x)", r"\exists\mathrm{I}", r"any term $t$"),
            rule_figure([r"\varphi(a)"], r"\forall x\, \varphi(x)", r"\forall\mathrm{I}",
                        r"$a$ arbitrary: in no premise or open assumption"),
            rule_figure([r"\exists x\, \varphi(x)", r"\begin{matrix}[\varphi(a)] \\ \vdots \\ \psi\end{matrix}"],
                        r"\psi", r"\exists\mathrm{E}", r"$a$ new: not in $\psi$, the premises, or open assumptions"))
        figs.arrange_in_grid(rows=2, cols=2, buff=(1.2, 0.6)).move_to([0, -0.9, 0])
        easy = SurroundingRectangle(VGroup(figs[0], figs[1]), color=OK, buff=0.15, corner_radius=0.1)
        hard = SurroundingRectangle(VGroup(figs[2], figs[3]), color=GOAL, buff=0.15, corner_radius=0.1)
        with self.voiceover(
            "In 1935 Gerhard Gentzen gave the rules for proving with quantifiers that most textbooks still teach, "
            "in his system of natural deduction. As in Part 2, each symbol has a rule to bring it in and a rule to "
            "take it out. <bookmark mark='a'/>Two of them are easy. What holds of everything holds of any "
            "particular thing: from 'for all x, phi', infer phi of any term. And what holds of a particular thing "
            "holds of something: from phi of t, infer 'there exists an x such that phi'. <bookmark mark='b'/>The "
            "other two carry conditions, and the conditions are the whole point. To prove that everything is phi, "
            "prove it of an arbitrary object a, one you have assumed nothing about. <bookmark mark='c'/>And to use "
            "'something is phi', give that something a brand-new name, a, reason about it, and draw only "
            "conclusions that do not mention a."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(figs[0]), FadeIn(figs[1]), Create(easy))
            vo.wait_until("b")
            self.play(FadeIn(figs[2]), Create(hard))
            vo.wait_until("c")
            self.play(FadeIn(figs[3]))
        self.clear_scene()

    def hasty(self):
        lines = [(0, "P(a)", "premise", []), (0, "forall x P(x)", "allI", [1])]
        ok, msg = fol.check_fitch(lines)
        assert not ok and "not arbitrary" in msg
        cm = fol.countermodel([fol.parse("P(a)")], fol.parse("forall x P(x)"))
        assert cm is not None and len(cm.domain) == 2
        eng = VGroup(label(r"Socrates is a philosopher.", font_size=32),
                     label(r"So everything is a philosopher.", font_size=32, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.0, 1.8, 0])
        fv = FitchView(lines, font_size=32, tex=FOLTEX, center=[-2.6, -0.2, 0], just_x=2.4)
        cross = MathTex(r"\times", font_size=44, color=BAD).next_to(fv.line[1][2], RIGHT, buff=0.3)
        verdict = label(r"the Reasoner: \ line 2 rejected, \ $a$ occurs in a premise, \ so it is not arbitrary",
                        font_size=24, color=BAD).to_edge(DOWN, buff=1.0)
        dom = VGroup(VGroup(Dot(color=OBJ), label(r"$a$: \ $P$", font_size=24, color=OBJ)).arrange(RIGHT, buff=0.15),
                     VGroup(Dot(color=OBJ), label(r"$b$: \ not $P$", font_size=24, color=OBJ)).arrange(RIGHT,
                                                                                                  buff=0.15)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.3, 0])
        dl = label(r"a countermodel with two objects", font_size=22, color=GREY_A).next_to(dom, UP, buff=0.3)
        with self.voiceover(
            "Here is what the condition prevents. <bookmark mark='a'/>Socrates is a philosopher; so everything is a "
            "philosopher. <bookmark mark='b'/>As a proof: from P of a, generalize to 'for all x, P of x'. "
            "<bookmark mark='c'/>The Reasoner's proof checker refuses line two. The object a is not arbitrary: the "
            "premise says something about it. <bookmark mark='d'/>And the model finder shows why it must refuse: a "
            "world of two objects, a philosopher and something else."
        ) as vo:
            self.play(FadeIn(eng))
            vo.wait_until("b")
            self.play(FadeIn(fv))
            vo.wait_until("c")
            self.play(FadeIn(cross), FadeIn(verdict))
            vo.wait_until("d")
            self.play(FadeIn(dl), LaggedStart(*[FadeIn(d, shift=LEFT * 0.2) for d in dom], lag_ratio=0.3))
        self.clear_scene()

    GOOD = [(0, "exists y forall x L(x, y)", "premise", []),
            (1, "forall x L(x, b)", "assume", []),
            (1, "L(a, b)", "allE", [2]),
            (1, "exists y L(a, y)", "exI", [3]),
            (1, "forall x exists y L(x, y)", "allI", [4]),
            (0, "forall x exists y L(x, y)", "exE", [1, (2, 5)])]

    BAD_ = [(0, "forall x exists y L(x, y)", "premise", []),
            (0, "exists y L(a, y)", "allE", [1]),
            (1, "L(a, b)", "assume", []),
            (1, "forall x L(x, b)", "allI", [3])]

    def good_proof(self):
        assert fol.check_fitch(self.GOOD, goal="forall x exists y L(x, y)") == (True, "valid")
        head = label(r"Someone is loved by everyone; \ so everyone loves someone.", font_size=30).to_edge(UP,
                                                                                                         buff=0.4)
        fv = FitchView(self.GOOD, font_size=32, tex=FOLTEX, center=[-0.6, -0.2, 0], just_x=3.4)
        notes = [r"call the loved one $b$, a new name", r"so in particular $a$ loves $b$",
                 r"so $a$ loves someone", r"$a$ was arbitrary: generalize", r"$b$ does not appear: discharge"]
        tags = VGroup(*[label(t, font_size=20, color=GREY_A) for t in notes])
        for t, i in zip(tags, range(1, 6)):
            t.next_to(fv.line[i][2], RIGHT, buff=0.35)
        ok = label(r"the Reasoner: \ every line checked \ $\checkmark$", font_size=26, color=OK).to_edge(DOWN,
                                                                                                         buff=0.45)
        with self.voiceover(
            "Now a real proof, of the direction that holds. <bookmark mark='a'/>Someone is loved by everyone. "
            "<bookmark mark='b'/>Give that someone a new name, b: assume that everyone loves b. "
            "<bookmark mark='c'/>Then, in particular, a loves b, <bookmark mark='d'/>so a loves someone. "
            "<bookmark mark='e'/>We assumed nothing about a, so we may generalize: everyone loves someone. "
            "<bookmark mark='f'/>That conclusion does not mention b, so it follows from the original premise, and "
            "the subproof closes. <bookmark mark='g'/>The Reasoner checks every line, including both side "
            "conditions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(fv.bars[0]), FadeIn(VGroup(*fv.line[0])))
            vo.wait_until("b")
            self.play(FadeIn(fv.bars[1:]), FadeIn(VGroup(*fv.line[1])), FadeIn(tags[0]))
            for k, mk in zip(range(2, 6), "cdef"):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*fv.line[k])), FadeIn(tags[k - 1]))
            vo.wait_until("g")
            self.play(FadeIn(ok, shift=UP * 0.2))
        self.clear_scene()

    def bad_proof(self):
        ok, msg = fol.check_fitch(self.BAD_)
        assert not ok and msg.startswith("line 4") and "not arbitrary" in msg
        sw = load("tableaux")["swap"]
        head = label(r"Everyone loves someone; \ so someone is loved by everyone?", font_size=30).to_edge(UP,
                                                                                                          buff=0.4)
        fv = FitchView(self.BAD_, font_size=32, tex=FOLTEX, center=[-2.4, 0.4, 0], just_x=3.0)
        cross = MathTex(r"\times", font_size=44, color=BAD).next_to(fv.line[3][2], RIGHT, buff=0.3)
        why = label(r"$a$ occurs in the open assumption $\mathrm{L}(a, b)$", font_size=24, color=BAD).next_to(
            fv, DOWN, buff=0.4).align_to(fv, LEFT)
        g = relation_graph(["Ann", "Bo"], [tuple(p) for p in sw["countermodel"]], radius=1.1, center=[4.2, 0.2, 0])
        gl = label(rf"the model finder's countermodel: \ {sw['size']} people", font_size=22, color=GREY_A).next_to(
            g, DOWN, buff=0.3)
        gl2 = label(r"each loves the other; \ nobody is loved by both", font_size=22, color=GREY_A).next_to(
            gl, DOWN, buff=0.1)
        with self.voiceover(
            "Try the converse, and watch where it breaks. <bookmark mark='a'/>Everyone loves someone; so in "
            "particular a loves someone. Call that someone b. <bookmark mark='b'/>Now a loves b, and we would like to "
            "generalize over the lover. <bookmark mark='c'/>But a is not arbitrary any more: the assumption we are "
            "working under is about a. The Reasoner rejects line four. <bookmark mark='d'/>No other proof will "
            "succeed either, because the argument is invalid. Two people who love each other: everyone loves "
            "someone, but nobody is loved by everyone, since nobody loves themselves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fv.bars[0]), FadeIn(VGroup(*fv.line[0])))
            vo.wait_until("a")
            self.play(FadeIn(fv.bars[1:]), FadeIn(VGroup(*fv.line[1])), FadeIn(VGroup(*fv.line[2])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*fv.line[3])))
            vo.wait_until("c")
            self.play(FadeIn(cross), FadeIn(why), fv.line[3][1].animate.set_color(BAD))
            vo.wait_until("d")
            self.play(FadeIn(g), FadeIn(gl), FadeIn(gl2))
        self.clear_scene()

    def drinker(self):
        d = load("tableaux")["drinker"]
        s = VGroup(label(r"`There is someone in the pub such that, if they are drinking, everyone is drinking.'",
                         font_size=28),
                   fm(d["conclusion"], font_size=40, color=GOAL)).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.5)
        cases = VGroup(
            VGroup(label(r"case 1: \ everyone is drinking", font_size=26, color=P.CLAIM),
                   label(r"pick anyone: \ the `then' part is true", font_size=24, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"case 2: \ someone is not drinking", font_size=26, color=P.AGENT),
                   label(r"pick them: \ the `if' part is false", font_size=24, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1)).arrange(RIGHT, buff=1.2).move_to([0, -0.4, 0])
        tab = label(rf"the tableau of Chapter 6: \ closed in {len(d['steps'])} steps \ $\checkmark$", font_size=26,
                    color=OK).to_edge(DOWN, buff=1.0)
        caveat = label(r"valid only because domains are never empty: \ free logic disagrees (Parts 5, 20)",
                       font_size=24, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Logic students meet a famous oddity, named the drinking principle by Raymond Smullyan. "
            "<bookmark mark='a'/>There is someone in the pub such that, if they are drinking, everyone is drinking. "
            "It sounds absurd, and it is valid. <bookmark mark='b'/>Either everyone is drinking, and then anyone "
            "will do, because the 'then' part is true. Or someone is not drinking, and then pick them: the 'if' part "
            "is false, so the conditional is true. <bookmark mark='c'/>The tableau in the next chapter closes it in "
            f"{len(d['steps'])} steps. <bookmark mark='d'/>It depends on one assumption that first-order logic makes "
            "silently: the domain is never empty. In an empty pub there is no one to pick. Free logic, which allows "
            "empty domains and empty names, rejects it, and we meet it again in Parts 5 and 20."
        ) as vo:
            self.play(FadeIn(s[0]))
            vo.wait_until("a")
            self.play(Write(s[1]))
            vo.wait_until("b")
            self.play(FadeIn(cases[0], shift=UP * 0.2))
            self.play(FadeIn(cases[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(caveat))
        self.clear_scene()

    def gentzen(self):
        seq = MathTex(r"\Gamma \ \Rightarrow\ \Delta", font_size=52, color=CONN).move_to([0, 2.2, 0])
        sl = label(r"a sequent: \ if everything in $\Gamma$ is true, something in $\Delta$ is", font_size=24,
                   color=GREY_A).next_to(seq, DOWN, buff=0.2)
        cut = rule_figure([r"\Gamma \Rightarrow \Delta, A", r"A, \Gamma \Rightarrow \Delta"],
                          r"\Gamma \Rightarrow \Delta", r"\mathrm{Cut}", r"use a lemma $A$", font_size=34)
        cut.move_to([-3.2, -0.1, 0])
        haupt = theorem_card(r"Cut elimination (\textit{Hauptsatz})", r"every proof can be rebuilt without Cut: "
                             r"then every formula in it is a subformula of what it proves", who=r"Gentzen 1935",
                             width=6.4, font_size=22).move_to([3.3, -0.1, 0])
        price = label(r"the price: \ cut-free proofs can be vastly longer \ (Statman 1979, Orevkov 1979)",
                      font_size=24, color=BAD).to_edge(DOWN, buff=1.0)
        use = label(r"the payoff: \ proof search, \ because there is nothing to guess but pieces of the goal",
                    font_size=24, color=OK).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Gentzen's paper did something deeper. <bookmark mark='a'/>He also wrote proofs as trees of sequents: "
            "statements that if everything on the left is true, something on the right is. "
            "<bookmark mark='b'/>One rule, cut, lets a proof go through a lemma, a formula A that is proved and then "
            "used. <bookmark mark='c'/>Gentzen's main theorem says cut can always be eliminated: any proof can be "
            "rebuilt without lemmas, and then every formula in it is a piece of the conclusion. "
            "<bookmark mark='d'/>The price is length: without lemmas, some proofs grow beyond any tower of "
            "exponentials. <bookmark mark='e'/>The payoff is search. If a proof only ever uses pieces of what it "
            "proves, a machine can look for one by taking the goal apart. That is exactly what the next chapter's "
            "trees do."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(seq), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(cut))
            vo.wait_until("c")
            self.play(FadeIn(haupt, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(price))
            vo.wait_until("e")
            self.play(FadeIn(use))
        self.clear_scene()
