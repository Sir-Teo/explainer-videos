from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


def mod_tex(s: str) -> str:
    """'<>[]~' -> \\Diamond\\Box\\lnot p (a modality applied to p)."""
    out = s.replace("<>", r"\Diamond ").replace("[]", r"\Box ").replace("~", r"\lnot ")
    return (out + "p") if out else "p"


class Lewis(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Strict implication and the systems S1--S5", r"What does `if' mean, if not Philo's?",
                            lit=(1912,), part=PART)
        with self.voiceover("Chapter two. Strict implication, and the systems S1 to S5."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.paradoxes()
        self.strict()
        self.axioms()
        self.fourteen()
        self.topology()

    def paradoxes(self):
        head = label(r"Philo's conditional (Part 2) proves these:", font_size=30, color=CONN).to_edge(UP, buff=0.5)
        ps = VGroup(VGroup(MathTex(r"q \to (p \to q)", font_size=40),
                           label(r"`if the moon is cheese, then $2 + 2 = 4$'", font_size=24, color=GREY_A)),
                    VGroup(MathTex(r"\lnot p \to (p \to q)", font_size=40),
                           label(r"`if $2 + 2 = 5$, then I am the Pope'", font_size=24, color=GREY_A)))
        for r in ps:
            r.arrange(RIGHT, buff=0.6)
        ps.arrange(DOWN, buff=0.5).move_to([0, 0.3, 0])
        hc = history_card(1912, r"C.\ I.\ Lewis", r"`Implication and the algebra of logic': \ these are not what "
                          r"`implies' means", width=7.0, color=HIST).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In Part 2 we chose Philo's conditional: 'if p then q' is false only when p is true and q false. "
            "<bookmark mark='a'/>It makes these tautologies. A true conclusion is implied by anything: if the moon "
            "is made of cheese, then two plus two is four. <bookmark mark='b'/>And a false premise implies anything: "
            "if two plus two is five, then I am the Pope. <bookmark mark='c'/>In 1912 the American logician C. I. "
            "Lewis protested that this is not what 'implies' means. For p to imply q, it must be impossible for p to "
            "be true and q false. Not false as it happens: impossible."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ps[0]))
            vo.wait_until("b")
            self.play(FadeIn(ps[1]))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.clear_scene()

    def strict(self):
        defn = MathTex(r"p \text{ strictly implies } q", r"\;:=\;", r"\Box(p \to q)", font_size=48).move_to([0, 1.6, 0])
        defn[0].set_color(GOAL)
        dl = label(r"strict implication: \ necessarily, not $p$ without $q$", font_size=26, color=GREY_A).next_to(
            defn, DOWN, buff=0.3)
        hc = history_card(1932, r"Lewis \& Langford, \textit{Symbolic Logic}", r"five systems, S1 to S5: \ which "
                          r"laws does `necessarily' obey?", width=7.2, color=HIST).move_to([0, -0.6, 0])
        still = VGroup(MathTex(r"\Box \lnot p \to \Box(p \to q)", font_size=36, color=BAD),
                       label(r"the impossible still strictly implies everything: \ relevance logic, Part 5",
                             font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Lewis defined a new connective. <bookmark mark='a'/>p strictly implies q when, necessarily, if p then q. "
            "<bookmark mark='b'/>With his student Cooper Langford he published five axiom systems in 1932, S1 to S5, "
            "each a different answer to the question: which laws does 'necessarily' obey? Is what is necessary "
            "necessarily necessary? Is what is possible necessarily possible? <bookmark mark='c'/>Strict implication "
            "has paradoxes of its own: an impossible proposition strictly implies everything. Logics that refuse even "
            "this are relevance logics, in Part 5."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(defn), FadeIn(dl))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(still))
        self.clear_scene()

    def axioms(self):
        head = label(r"The modern systems: \ K plus axioms", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = [(r"K", r"\Box(p \to q) \to (\Box p \to \Box q)", r"necessity distributes over `if'"),
                (r"N", r"\text{if } \vdash \varphi \text{ then } \vdash \Box\varphi", r"theorems are necessary"),
                (r"T", r"\Box p \to p", r"what is necessary is true"),
                (r"4", r"\Box p \to \Box\Box p", r"necessary truths are necessarily necessary"),
                (r"B", r"p \to \Box\Diamond p", r"what is true is necessarily possible"),
                (r"5", r"\Diamond p \to \Box\Diamond p", r"what is possible is necessarily possible")]
        tab = VGroup()
        for nm, f, rd in rows:
            tab.add(VGroup(MathTex(nm, font_size=32, color=GOAL), MathTex(f, font_size=34),
                           label(rd, font_size=22, color=GREY_A)))
        for i, r in enumerate(tab):
            y = 2.2 - 0.62 * i
            r[0].move_to([-5.8, y, 0])
            r[1].move_to([-5.2 + r[1].width / 2, y, 0])
            r[2].move_to([1.6 + r[2].width / 2, y, 0])
        sys_ = VGroup(MathTex(r"\mathsf{T} = \mathsf{K} + T", font_size=32),
                      MathTex(r"\mathsf{S4} = \mathsf{K} + T + 4", font_size=32),
                      MathTex(r"\mathsf{S5} = \mathsf{K} + T + 5", font_size=32)).arrange(RIGHT, buff=0.8).to_edge(
            DOWN, buff=0.6)
        with self.voiceover(
            "Today the systems are built from a base called K, after Kripke. <bookmark mark='a'/>K has one axiom: "
            "if necessarily p implies q, and necessarily p, then necessarily q. <bookmark mark='b'/>And one rule: "
            "whatever is a theorem is necessary. <bookmark mark='c'/>On top go the optional axioms. T: what is "
            "necessary is true. Four: what is necessary is necessarily necessary. B: what is true is necessarily "
            "possible. Five: what is possible is necessarily possible. <bookmark mark='d'/>Lewis's S4 is K with T "
            "and four; S5 is K with T and five. Why these axioms and not others, and what do they mean? Chapter four "
            "has an exact answer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[2:]], lag_ratio=0.4), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(sys_))
        self.clear_scene()

    def fourteen(self):
        d = load("modalities")
        s4, s5 = d["S4"], d["S5"]
        head = label(rf"Stack $\Box$, $\Diamond$ and $\lnot$ on $p$: \ {d['tried']} strings of up to five symbols",
                     font_size=28, color=CONN).to_edge(UP, buff=0.4)
        pos = [m for m in s4 if not m.startswith("~") and not m.endswith("~")]
        neg = [m for m in s4 if m not in pos]
        colA = VGroup(*[MathTex(mod_tex(m), font_size=32, color=OK) for m in pos]).arrange(DOWN, buff=0.18)
        colB = VGroup(*[MathTex(mod_tex(m), font_size=32, color=P.AGENT) for m in neg]).arrange(DOWN, buff=0.18)
        cols = VGroup(colA, colB).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([-3.2, -0.6, 0])
        l4 = label(rf"S4: \ {len(s4)} distinct modalities", font_size=28, color=GOAL).next_to(cols, UP, buff=0.3)
        c5 = VGroup(*[MathTex(mod_tex(m), font_size=32, color=OK) for m in s5]).arrange(DOWN, buff=0.18).move_to(
            [3.6, -0.6, 0])
        l5 = label(rf"S5: \ only {len(s5)}", font_size=28, color=GOAL).next_to(c5, UP, buff=0.3)
        how = label(rf"checked on all {d['frames_S4']} S4 frames and {d['frames_S5']} S5 frames of up to 4 worlds",
                    font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is one way to see how much the axioms matter. <bookmark mark='a'/>Take p, and stack boxes, "
            "diamonds and negations in front of it, every string of up to five symbols. How many of them say "
            "different things? <bookmark mark='b'/>In S4, the Reasoner found exactly fourteen: p, necessarily p, "
            "possibly necessarily p, necessarily possibly necessarily p, and so on, and their negations. Every "
            "longer string collapses onto one of these. <bookmark mark='c'/>In S5, the collapse is total: only six "
            "survive, because in S5 only the last operator in a string matters. <bookmark mark='d'/>Each answer was "
            "found by checking every string on every frame of up to four worlds that obeys the axioms."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(l4), LaggedStart(*[FadeIn(x) for x in colA], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(x) for x in colB], lag_ratio=0.1), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(l5), LaggedStart(*[FadeIn(x) for x in c5], lag_ratio=0.15))
            vo.wait_until("d")
            self.play(FadeIn(how))
        self.clear_scene()

    def topology(self):
        hcs = VGroup(history_card(1922, r"Kazimierz Kuratowski", r"closure and complement give at most 14 sets",
                                  width=5.6, color=HIST),
                     history_card(1944, r"McKinsey \& Tarski", r"S4 is the logic of topology", width=5.6,
                                  color=HIST)).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.5)
        rd = VGroup(VGroup(MathTex(r"\Box", font_size=48, color=GOAL), label(r"interior", font_size=28)),
                    VGroup(MathTex(r"\Diamond", font_size=48, color=GOAL), label(r"closure", font_size=28)),
                    VGroup(MathTex(r"\lnot", font_size=48, color=GOAL), label(r"complement", font_size=28)))
        for r in rd:
            r.arrange(DOWN, buff=0.2)
        rd.arrange(RIGHT, buff=1.4).move_to([0, -0.5, 0])
        same = label(r"the same 14: \ Kuratowski's closure-complement sets are S4's modalities", font_size=26,
                     color=OK).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The number fourteen had appeared before, in topology. <bookmark mark='a'/>In 1922 Kazimierz Kuratowski "
            "proved that starting from one set of points and applying closure and complement, you can get at most "
            "fourteen different sets. <bookmark mark='b'/>In 1944 J. C. C. McKinsey and Alfred Tarski explained "
            "why: read the box as interior, the diamond as closure, and negation as complement, and S4 is exactly "
            "the logic of topology. <bookmark mark='c'/>Kuratowski's fourteen sets are S4's fourteen modalities. "
            "The box was not only about metaphysics; it had a geometry."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hcs[0], shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(hcs[1], shift=DOWN * 0.2), LaggedStart(*[FadeIn(r) for r in rd], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(same))
        self.clear_scene()
