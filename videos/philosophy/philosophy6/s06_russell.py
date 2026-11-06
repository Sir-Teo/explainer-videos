from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Russell(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Russell's letter", r"Does every condition define a set?", lit=(1902,), part=PART)
        with self.voiceover("Chapter five. Russell's letter."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.frege()
        self.paradox()
        self.reply()
        self.family()

    def frege(self):
        hc = history_card(1893, r"Gottlob Frege, \textit{Grundgesetze der Arithmetik} I", r"arithmetic derived from "
                          r"logic alone", width=6.8, color=HIST).to_corner(UL, buff=0.35)
        law = VGroup(label(r"Basic Law V", font_size=28, color=GOAL),
                     MathTex(r"\{x : Fx\} = \{x : Gx\} \ \iff\ \forall x\,(Fx \leftrightarrow Gx)", font_size=38),
                     label(r"two concepts have the same extension \ iff \ they apply to the same things", font_size=24,
                           color=GREY_A)).arrange(DOWN, buff=0.3).move_to([0, 0.4, 0])
        comp = VGroup(label(r"so, in effect: \ naive comprehension", font_size=26, color=BAD),
                      MathTex(r"\exists y\, \forall x\, (x \in y \leftrightarrow \varphi(x))", font_size=38, color=BAD),
                      label(r"every condition defines a set", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.25).next_to(law, DOWN, buff=0.6)
        with self.voiceover(
            "Part 3 began with Gottlob Frege's notation. Frege's goal was larger: to derive all of arithmetic from "
            "logic. <bookmark mark='a'/>The first volume of his Basic Laws of Arithmetic appeared in 1893. One of its "
            "axioms, Basic Law Five, says that two concepts have the same extension, the same set, exactly when "
            "they apply to the same things. <bookmark mark='b'/>In effect it gives every condition a set: the set "
            "of things that satisfy it. This is naive comprehension, and it seems as innocent as anything in "
            "mathematics."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(law))
            vo.wait_until("b")
            self.play(FadeIn(comp))
        self.clear_scene()

    def paradox(self):
        d = load("russell")
        hc = history_card(r"16 June 1902", r"Bertrand Russell, letter to Frege", r"`Let $w$ be the predicate: to be a "
                          r"predicate that cannot be predicated of itself...'", width=7.4, color=HIST).to_corner(UL, buff=0.3)
        steps = VGroup(
            MathTex(r"R = \{x : x \notin x\}", font_size=40, color=GOAL),
            MathTex(r"\forall x\, (x \in R \leftrightarrow x \notin x)", font_size=36),
            MathTex(r"R \in R \ \leftrightarrow\ R \notin R", font_size=40, color=BAD),
            label(r"take $x = R$: \ a sentence equivalent to its own negation", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.35).move_to([-2.6, -0.4, 0])
        nums = VGroup(*[label(rf"{i}.", font_size=24, color=GREY_B).next_to(steps[i - 1], LEFT, buff=0.4)
                        for i in (1, 2, 3)])
        chk = VGroup(label(r"the Reasoner:", font_size=26, color=P.CLAIM),
                     MathTex(r"r \leftrightarrow \lnot r", font_size=40),
                     label(r"unsatisfiable \ (Part 2's SAT solver)" if not d["russell_satisfiable"] else r"?",
                           font_size=26, color=BAD),
                     label(r"no set can be $R$, \ so naive comprehension is inconsistent", font_size=24,
                           color=GOAL)).arrange(DOWN, buff=0.3).move_to([3.6, -0.4, 0])
        with self.voiceover(
            "On the sixteenth of June 1902, Bertrand Russell wrote to Frege. <bookmark mark='a'/>Consider the set of "
            "all sets that are not members of themselves. Call it R. By naive comprehension, it exists. "
            "<bookmark mark='b'/>Something belongs to R exactly when it does not belong to itself. "
            "<bookmark mark='c'/>Now ask about R itself. R belongs to R exactly when R does not belong to R. "
            "<bookmark mark='d'/>Write 'R belongs to R' as a single atom, r. Then the line says: r if and only if "
            "not r, and the SAT solver of Part 2 confirms what is obvious: no assignment of truth values satisfies "
            "it. Naive comprehension is inconsistent, and with it Frege's system."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(nums[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(nums[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), FadeIn(nums[2]), FadeIn(steps[3]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c) for c in chk], lag_ratio=0.35))
        self.clear_scene()

    def reply(self):
        q1 = quote_card(r"Your discovery of the contradiction has surprised me beyond words and, I should almost like to "
                        r"say, left me thunderstruck, because it has rocked the ground on which I meant to build "
                        r"arithmetic.", r"Frege to Russell, 22 June 1902", r"in van Heijenoort, \textit{From Frege to "
                        r"Gödel} (1967)", width=10.6, font_size=26).move_to([0, 1.3, 0])
        q2 = quote_card(r"Hardly anything more unfortunate can befall a scientific writer than to have one of the "
                        r"foundations of his edifice shaken after the work is finished.", r"Frege, \textit{Grundgesetze} "
                        r"II, appendix (1903)", width=10.6, font_size=26, color=BAD).next_to(q1, DOWN, buff=0.6)
        with self.voiceover(
            "Frege replied within a week, and his answer is a model of intellectual honesty. <bookmark mark='a'/>The "
            "discovery, he wrote, had left him thunderstruck, because it shook the ground on which he meant to build "
            "arithmetic. <bookmark mark='b'/>The second volume of his work was already at the printer. He added an "
            "appendix that begins: hardly anything more unfortunate can befall a scientific writer than to have one "
            "of the foundations of his edifice shaken after the work is finished."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q1))
            vo.wait_until("b")
            self.play(FadeIn(q2))
        self.clear_scene()

    def family(self):
        d = load("russell")
        head = label(r"A family of paradoxes", font_size=34, color=CONN).to_edge(UP, buff=0.45)
        rows = [(r"Burali-Forti (1897)", r"the ordinals would form an ordinal larger than all of them"),
                (r"Cantor (1899)", r"the set of all sets would have a power set bigger than itself"),
                (r"Russell (1902)", r"the set of non-self-membered sets"),
                (r"Curry (1942)", r"$C = \{x : x \in x \to q\}$: \ proves any $q$ at all, \ with no negation")]
        tab = VGroup()
        for i, (a, b) in enumerate(rows):
            y = 1.6 - 0.8 * i
            l1 = label(a, font_size=26, color=GOAL)
            l2 = label(b, font_size=24)
            l1.move_to([-6.0 + l1.width / 2, y, 0])
            l2.move_to([-2.2 + l2.width / 2, y, 0])
            tab.add(VGroup(l1, l2))
        cur = label(r"with $c$ for `$C \in C$', \ the Reasoner: \ $c \leftrightarrow (c \to q) \ \models\ q$ \ $\checkmark$",
                    font_size=24, color=OK).next_to(tab, DOWN, buff=0.5)
        cur.set_x(0)
        brk = label(r"half of this part's brick in the Wall: \ not every condition defines a set", font_size=26,
                    color=P.WALL).to_edge(DOWN, buff=0.45)
        assert d["curry_entails_q"]
        with self.voiceover(
            "Russell's was not the only paradox. <bookmark mark='a'/>Cesare Burali-Forti had found that the ordinal "
            "numbers, which we meet in Chapter 9, would form an ordinal larger than all of them. Cantor himself saw "
            "that the set of all sets would have a power set larger than itself. <bookmark mark='b'/>Russell's is "
            "the simplest. <bookmark mark='c'/>And Haskell Curry found one that needs no negation at all: a set c "
            "whose members are the things x such that, if x belongs to x, then q. Classical logic then proves q, "
            "whatever q says. The Reasoner confirms the entailment. Part 5's contraction-free logics block exactly "
            "this step. <bookmark mark='d'/>Together they are half of this part's brick in the Wall: not every "
            "condition defines a set."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(cur))
            vo.wait_until("d")
            self.play(FadeIn(brk))
        self.clear_scene()
