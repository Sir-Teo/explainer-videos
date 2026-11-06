from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403

AXIOMS = [
    (r"extensionality", r"\forall z\,(z \in x \leftrightarrow z \in y) \to x = y", r"a set is its members"),
    (r"pairing", r"\exists p\ \forall z\,(z \in p \leftrightarrow z = x \lor z = y)", r"$\{x, y\}$"),
    (r"union", r"\exists u\ \forall z\,(z \in u \leftrightarrow \exists y\,(z \in y \land y \in x))", r"$\bigcup x$"),
    (r"power set", r"\exists p\ \forall z\,(z \in p \leftrightarrow z \subseteq x)", r"$\mathcal{P}(x)$"),
    (r"separation", r"\exists s\ \forall z\,(z \in s \leftrightarrow z \in a \land \varphi(z))",
     r"subsets by a condition, \ \textit{inside} a given set"),
    (r"infinity", r"\exists I\,(\varnothing \in I \land \forall x \in I\ x \cup \{x\} \in I)", r"$\omega$"),
    (r"replacement", r"\text{the image of a set under a definable function is a set}", r"$\omega + \omega$ and beyond"),
    (r"foundation", r"\text{every nonempty set has an } \in\text{-minimal member}", r"no $x \in x$; \ the hierarchy"),
    (r"choice", r"\text{every family of nonempty sets has a choice function}", r"Chapter 13"),
]


class Axioms(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"The axioms", r"Which sets are there, if not one for every condition?",
                            lit=(1908,), part=PART)
        with self.voiceover("Chapter six. The axioms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.two_answers()
        self.separation()
        self.zfc()

    def two_answers(self):
        hcs = VGroup(history_card(1908, r"Bertrand Russell", r"`Mathematical logic as based on the theory of types'",
                                  width=6.0, color=HIST),
                     history_card(1908, r"Ernst Zermelo", r"`Investigations in the foundations of set theory I'",
                                  width=6.0, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        types = VGroup(*[Rectangle(width=4.2, height=0.5, stroke_color=SETC, stroke_width=2).move_to([-3.4, -1.9 + 0.7 * i, 0])
                         for i in range(4)])
        tl = VGroup(*[label(t, font_size=20, color=GREY_A).move_to(r) for t, r in zip(
            (r"individuals", r"sets of individuals", r"sets of sets of individuals", r"\dots"), types)])
        tcap = label(r"types: \ a set only contains things of the level below", font_size=22, color=GOAL).next_to(
            types, UP, buff=0.25)
        zcap = VGroup(label(r"axioms: \ say exactly which sets exist", font_size=24, color=GOAL),
                      label(r"and prove everything else from them", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.2).move_to([3.4, -0.6, 0])
        with self.voiceover(
            "In 1908 two answers to the paradox appeared. <bookmark mark='a'/>Russell's theory of types arranges "
            "everything in levels: individuals, sets of individuals, sets of those, and so on. A set may only "
            "contain things from the level below, so 'the set of sets that are not members of themselves' cannot "
            "even be written. This became the framework of Principia Mathematica. <bookmark mark='b'/>Ernst "
            "Zermelo took the other road: write down axioms that say exactly which sets exist, and derive the rest. "
            "His road became the foundation of modern mathematics."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hcs[0]), LaggedStart(*[Create(t) for t in types], lag_ratio=0.2), FadeIn(tl), FadeIn(tcap))
            vo.wait_until("b")
            self.play(FadeIn(hcs[1]), FadeIn(zcap))
        self.clear_scene()

    def separation(self):
        head = label(r"Separation: \ comprehension, \ but only inside a set you already have", font_size=30,
                     color=CONN).to_edge(UP, buff=0.5)
        f = MathTex(r"R_A = \{x \in A : x \notin x\}", font_size=44, color=GOAL).next_to(head, DOWN, buff=0.6)
        steps = VGroup(label(r"$R_A$ exists, \ for any set $A$", font_size=26),
                       label(r"if $R_A \in A$: \ $R_A \in R_A \iff R_A \notin R_A$, \ a contradiction", font_size=26),
                       label(r"so $R_A \notin A$", font_size=28, color=OK),
                       label(r"every set misses something: \ there is no set of all sets", font_size=28,
                             color=GOAL)).arrange(DOWN, buff=0.35).next_to(f, DOWN, buff=0.55)
        moral = label(r"the paradox becomes a theorem", font_size=28, color=OK).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Zermelo's key move is the axiom of separation. You may still collect the things that satisfy a "
            "condition, but only from inside a set you already have. <bookmark mark='a'/>So for any set A there is "
            "the set R A, of the members of A that are not members of themselves. <bookmark mark='b'/>Run Russell's "
            "argument. If R A were in A, then R A would belong to itself exactly when it does not. "
            "<bookmark mark='c'/>So R A is not in A. <bookmark mark='d'/>Every set leaves something out, and there "
            "is no set of all sets. <bookmark mark='e'/>The contradiction has become a theorem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(moral))
        self.clear_scene()

    def zfc(self):
        head = label(r"ZFC: \ Zermelo (1908), \ Fraenkel and Skolem (1922), \ von Neumann (1925)", font_size=28,
                     color=CONN).to_edge(UP, buff=0.35)
        rows = VGroup()
        for i, (n, f, what) in enumerate(AXIOMS):
            y = 2.45 - 0.62 * i
            l1 = label(n, font_size=24, color=GOAL)
            l2 = MathTex(f, font_size=24)
            l3 = label(what, font_size=20, color=GREY_A)
            l1.move_to([-6.4 + l1.width / 2, y, 0])
            l2.move_to([-4.3 + l2.width / 2, y, 0])
            l3.move_to([2.9 + l3.width / 2, y, 0])
            rows.add(VGroup(l1, l2, l3))
        foot = label(r"first-order, \ in the logic of Part 3: \ so the Löwenheim--Skolem theorem applies \ "
                     r"(Skolem's paradox, Part 3)", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here are the axioms as they settled by the 1920s, called ZFC after Zermelo, Abraham Fraenkel and "
            "choice. <bookmark mark='a'/>Extensionality: a set is nothing but its members. Pairing, union and power "
            "set build new sets from old. <bookmark mark='b'/>Separation carves out subsets by a condition, inside "
            "a given set. <bookmark mark='c'/>Infinity says there is an infinite set: the natural numbers. "
            "<bookmark mark='d'/>Replacement, added by Fraenkel and Skolem in 1922, says that the image of a set "
            "under a definable function is a set; without it, even omega plus omega cannot be built. "
            "<bookmark mark='e'/>Foundation, from von Neumann, rules out sets that contain themselves. "
            "<bookmark mark='f'/>And choice, which gets its own chapter. <bookmark mark='g'/>Notice that these are "
            "first-order axioms, in the logic of Part 3, so Skolem's paradox applies: they have countable models."
        ) as vo:
            self.play(FadeIn(head))
            for mk, idx in (("a", [0, 1, 2, 3]), ("b", [4]), ("c", [5]), ("d", [6]), ("e", [7]), ("f", [8])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(rows[i], shift=RIGHT * 0.15) for i in idx], lag_ratio=0.3))
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.clear_scene()
