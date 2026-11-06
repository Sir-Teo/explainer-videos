from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Anselm(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"That than which nothing greater can be conceived",
                            r"Can the concept of God prove that God exists?", lit=(1078, 1781), part=PART)
        with self.voiceover("Chapter one. That than which nothing greater can be conceived."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.argument()
        self.check()
        self.gaunilo()
        self.kant()

    def argument(self):
        hc = history_card(1078, r"Anselm of Canterbury", r"\textit{Proslogion}, \ chapter II", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        steps = stack([(r"1. \ God is that than which nothing greater can be conceived", DIV),
                       (r"2. \ even the fool who denies God understands this, \ so it exists in the understanding",
                        WHITE),
                       (r"3. \ to exist in reality as well is greater than to exist in the understanding alone",
                        ABS),
                       (r"4. \ suppose it existed in the understanding alone: \ then something greater could be "
                        r"conceived", BAD),
                       (r"5. \ which contradicts 1: \ so it exists in reality", OK)], font_size=22, aligned_edge=LEFT,
                      width=12.4, buff=0.32).move_to([0, -0.5, 0])
        with self.voiceover(
            "Around 1078 Anselm, then abbot of Bec, wrote a prayer that contains an argument. <bookmark mark='a'/>"
            "God is that than which nothing greater can be conceived. <bookmark mark='b'/>Even the fool of the Psalm, "
            "who says in his heart that there is no God, understands these words; so that than which nothing greater "
            "can be conceived exists at least in his understanding. <bookmark mark='c'/>But to exist in reality as "
            "well as in the understanding is greater than to exist in the understanding alone. "
            "<bookmark mark='d'/>So suppose it existed only in the understanding. Then we could conceive of something "
            "greater: the same thing, existing in reality. <bookmark mark='e'/>That contradicts the definition. So "
            "that than which nothing greater can be conceived exists, in the understanding and in reality."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def check(self):
        d = load("anselm")
        head = label(r"Valid, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"$U$", r"it exists in the understanding", WHITE),
            (r"$\lnot R \to C$", r"if it does not exist in reality, \ something greater can be conceived", ABS),
            (r"$\lnot C$", r"nothing greater can be conceived \ (the definition)", DIV),
            (r"$\therefore\ R$", r"it exists in reality", OK),
        ]
        g = rows_table(rows, top=2.0, gap=0.45, width=8.6, x_text=-3.6, label_size=26)
        verdict = label(r"valid: \ the Reasoner finds no valuation with the premises true and $R$ false \ (" +
                        f"{d['valuations']}" + r" checked)", font_size=21, color=OK).move_to([0, -0.6, 0])
        rows2 = stack([(r"so a critic must reject a premise, \ or the logic of `greater'", GOAL),
                       (r"is existence a way of being greater? \ is `exists in the understanding' even coherent?",
                        BAD)], font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Strip the argument to its skeleton. <bookmark mark='a'/>U: it exists in the understanding. If it does "
            "not exist in reality, something greater can be conceived. Nothing greater can be conceived. Therefore R: "
            "it exists in reality. <bookmark mark='b'/>The Reasoner checks every assignment of truth values: there is "
            "none on which the premises are true and the conclusion false. The form is a reductio, and it is valid. "
            "<bookmark mark='c'/>So a critic must reject a premise, or deny that the concept of greatness behaves as "
            "the argument needs. <bookmark mark='d'/>Is existing in reality a way of being greater? Does it make "
            "sense to say that a thing exists in the understanding at all? Nine centuries of criticism focus there."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.35), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(verdict))
            for mk, r in zip("cd", rows2):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def gaunilo(self):
        head = label(r"Gaunilo's island", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        isl = island([-3.6, 0.9, 0], w=4.2, h=2.2, seed=300, color=NAT, name=r"the Lost Island")
        trees = VGroup(*[VGroup(Line([x, 0.5, 0], [x, 1.2, 0], color=WARM, stroke_width=3),
                                Circle(radius=0.22, color=OK, fill_opacity=0.6).move_to([x, 1.3, 0]))
                         for x in (-4.8, -4.0, -3.2, -2.4)])
        par = stack([(r"1. \ the Lost Island is the island than which no greater island can be conceived", NAT),
                     (r"2. \ \ldots\ so it exists in reality", BAD)], font_size=20, aligned_edge=LEFT,
                    width=6.2).move_to([3.4, 1.1, 0])
        rows = stack([(r"Gaunilo of Marmoutiers: \ the same form proves too much, \ so something in it is wrong",
                       WHITE),
                      (r"Anselm's reply: \ the argument works only for the greatest conceivable \textit{being}", DIV),
                      (r"Plantinga: \ greatness for islands has no intrinsic maximum: \ one more palm tree, \ one "
                       r"more dancing girl", ABS),
                      (r"the parody test, \ again and again: \ a valid form that proves a falsehood has a false "
                       r"premise", GOAL)], font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The first reply came at once, from a monk named Gaunilo. <bookmark mark='a'/>Think of the Lost Island, "
            "the island than which no greater island can be conceived. By Anselm's reasoning it must exist, since an "
            "island that existed in reality would be greater than one that existed only in the understanding. "
            "<bookmark mark='b'/>The same form proves too much, so something in it is wrong. "
            "<bookmark mark='c'/>Anselm replied that the argument applies only to the greatest conceivable being, "
            "not to the greatest of a kind. <bookmark mark='d'/>Alvin Plantinga sharpened the reply: island "
            "greatness has no intrinsic maximum. However many palm trees the island has, one more would make it "
            "better. <bookmark mark='e'/>This is the parody test, which this part will use again and again: if an "
            "argument's form also proves something false, the form is not enough, and a premise is doing hidden work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(isl), FadeIn(trees))
            vo.wait_until("a")
            self.play(FadeIn(par))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def kant(self):
        hc = history_card(1781, r"Immanuel Kant", r"\textit{Critique of Pure Reason}, \ A598/B626", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        piles = VGroup()
        for k, (t, col) in enumerate(((r"a hundred real thalers", WARM), (r"a hundred possible thalers", ABS))):
            x = -3.4 + 6.8 * k
            coins = VGroup(*[Circle(radius=0.16, color=col, fill_opacity=0.5 if k == 0 else 0.0,
                                    stroke_width=2).move_to([x - 1.1 + 0.36 * (i % 7), 0.2 + 0.33 * (i // 7), 0])
                             for i in range(28)])
            tl = label(t, font_size=20, color=col).next_to(coins, DOWN, buff=0.2)
            piles.add(VGroup(coins, tl))
        eq = MathTex(r"=", font_size=60, color=GREY_B).move_to([0, 0.7, 0])
        el = label(r"the same concept", font_size=18, color=GREY_A).next_to(eq, DOWN, buff=0.1)
        rows = stack([(r"`Being is obviously not a real predicate': \ it adds nothing to the concept of a thing", WHITE),
                      (r"so `God exists' does not follow from what `God' means", BAD),
                      (r"Frege: \ existence is a second-level concept: \ `there are Fs' says the concept F has "
                       r"instances \ (Part 20)", ABS),
                      (r"but Descartes's and Leibniz's versions, \ and the modal one, \ try to avoid the predicate",
                       GOAL)], font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The most famous objection is Kant's. <bookmark mark='a'/>Being, he wrote, is obviously not a real "
            "predicate: it adds nothing to the concept of a thing. A hundred real thalers contain not a coin more "
            "than a hundred possible thalers. The concept is the same; what differs is whether something answers to "
            "it. <bookmark mark='b'/>So that God exists cannot follow from what the word God means. "
            "<bookmark mark='c'/>Frege made the point precise. Existence is not a property of things but of "
            "concepts: to say that there are horses is to say that the concept horse has instances, the "
            "quantifier of Part 20. <bookmark mark='d'/>Defenders have tried to avoid the predicate. Descartes "
            "argued that existence belongs to God's essence as the sum of its angles belongs to a triangle's. And "
            "the most powerful modern version replaces existence with necessity."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(piles), FadeIn(eq), FadeIn(el))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
