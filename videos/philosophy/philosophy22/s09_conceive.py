from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Conceive(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Conceivability and possibility", r"Is what we can imagine possible?",
                            lit=(1641, 2002), part=PART)
        with self.voiceover("Chapter eight. Conceivability and possibility."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.descartes()
        self.venn()
        self.kinds()
        self.kripke()

    def descartes(self):
        hc = history_card(1641, r"René Descartes", r"\textit{Meditations}, \ Sixth Meditation", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        steps = stack([(r"1. \ I can clearly and distinctly conceive my mind existing without my body", WHITE),
                       (r"2. \ whatever I clearly and distinctly conceive is possible \ (God could make it so)", GOAL),
                       (r"3. \ so my mind could exist without my body", WHITE),
                       (r"4. \ so my mind is not identical to my body \ (identity is necessary: \ Part 21)", OK)],
                      font_size=22, aligned_edge=LEFT, width=12.0, buff=0.3).move_to([0, 0.2, 0])
        rows = stack([(r"Hume: \ `whatever the mind clearly conceives includes the idea of possible existence'",
                       NAME),
                      (r"the same shape: \ Kripke on pain \ (1970), \ Chalmers's zombies \ (1996; \ Part 31)", DESC)],
                     font_size=20, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Philosophers have long reasoned from what can be conceived to what can be. <bookmark mark='a'/>Descartes, "
            "in the Sixth Meditation: I can clearly and distinctly conceive of my mind existing without my body. "
            "<bookmark mark='b'/>Whatever I clearly and distinctly conceive is possible; God, at least, could make "
            "it so. <bookmark mark='c'/>So my mind could exist without my body. <bookmark mark='d'/>And so my mind "
            "is not my body. Notice that the last step needs the necessity of identity from Part 21: if mind and body "
            "were one thing, they could not come apart. <bookmark mark='e'/>Hume stated the bridge principle "
            "plainly: whatever the mind clearly conceives includes the idea of possible existence. "
            "<bookmark mark='f'/>The same shape of argument returns in Kripke's case against identifying pain with a "
            "brain state, and in David Chalmers's zombies, in Part 31. Everything depends on the bridge."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            for mk, r in zip("ef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def venn(self):
        head = label(r"Where the bridge seems to fail", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cc = Ellipse(width=6.4, height=4.0, color=DESC, fill_opacity=0.08).move_to([-1.7, -0.3, 0])
        pp = Ellipse(width=6.4, height=4.0, color=WORLD, fill_opacity=0.08).move_to([1.7, -0.3, 0])
        lc = label(r"seems conceivable", font_size=22, color=DESC).next_to(cc, UP, buff=0.08).shift(LEFT * 1.2)
        lp = label(r"possible", font_size=22, color=WORLD).next_to(pp, UP, buff=0.08).shift(RIGHT * 1.2)
        items = [
            (r"water is not H$_2$O", [-3.3, 0.5, 0], DESC),
            (r"Goldbach's conjecture is false \ (if it is true)", [-3.3, -0.3, 0], DESC),
            (r"Hesperus is not Phosphorus", [-3.3, -1.1, 0], DESC),
            (r"a talking donkey", [0.0, 0.3, 0], GOAL),
            (r"you were born a day later", [0.0, -0.6, 0], GOAL),
            (r"a proof too long \ for any mind to follow", [3.3, 0.0, 0], WORLD),
            (r"colours no creature has seen", [3.3, -0.9, 0], WORLD),
        ]
        labs = VGroup()
        for t, p, c in items:
            m = label(t, font_size=17, color=c)
            if m.width > 2.6:
                m = wrapped_label(t, 2.6, 17, c)
            labs.add(m.move_to(p))
        note = label(r"the left crescent: \ a posteriori necessities, \ and mathematics we have not settled",
                     font_size=20, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "But the bridge has cracks. <bookmark mark='a'/>Draw what seems conceivable beside what is possible. "
            "<bookmark mark='b'/>Much is in both: a talking donkey; your being born a day later. "
            "<bookmark mark='c'/>Some possibilities may outrun what we can conceive: a proof too long for any mind to "
            "follow, colours no creature has ever seen. <bookmark mark='d'/>The trouble is the other crescent. It "
            "seems conceivable that water is not H two O, and that Hesperus is not Phosphorus; Kripke says both are "
            "impossible. And Goldbach's conjecture and its negation both seem conceivable, though one of them is "
            "a necessary falsehood. <bookmark mark='e'/>In the left crescent sit a posteriori necessities, and "
            "mathematics we have not settled. If such cases exist, conceiving is not always a guide."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(DrawBorderThenFill(cc), DrawBorderThenFill(pp), FadeIn(lc), FadeIn(lp))
            vo.wait_until("b")
            self.play(FadeIn(labs[3]), FadeIn(labs[4]))
            vo.wait_until("c")
            self.play(FadeIn(labs[5]), FadeIn(labs[6]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(labs[i]) for i in range(3)], lag_ratio=0.4))
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.clear_scene()

    def kinds(self):
        head = label(r"Which conceivability?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Yablo \ (1993)", r"$p$ is conceivable if you can imagine a situation that you take to verify $p$",
             NAME),
            (r"prima facie, \ ideal", r"on first reflection, \ or after ideal rational reflection: \ Goldbach's "
                                      r"negation is only prima facie conceivable", WORLD),
            (r"positive, \ negative", r"you can imagine a situation where $p$, \ or you merely cannot rule $p$ out a "
                                      r"priori", CPT),
            (r"primary, \ secondary", r"conceived as a hypothesis about the actual world, \ or as a counterfactual "
                                      r"given how the actual world is", DESC),
            (r"Chalmers \ (2002)", r"the defensible bridge: \ ideal, \ primary conceivability entails primary "
                                   r"possibility", OK),
        ]
        g = rows_table(rows, top=1.9, gap=0.45, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "The modern answer is to distinguish kinds of conceivability. <bookmark mark='a'/>Stephen Yablo: p is "
            "conceivable for you if you can imagine a situation that you take to verify p. "
            "<bookmark mark='b'/>Prima facie versus ideal: conceivable on first reflection, or still conceivable after "
            "ideal reflection. The negation of a true arithmetical conjecture is conceivable only in the first sense. "
            "<bookmark mark='c'/>Positive versus negative: imagining a situation, as opposed to merely being unable to "
            "rule p out. <bookmark mark='d'/>And the key distinction: conceiving of p as a hypothesis about how our "
            "own world might turn out to be, or as a counterfactual, given how our world actually is. "
            "<bookmark mark='e'/>David Chalmers argued that a bridge survives: ideal conceivability in the first, "
            "hypothetical sense entails possibility of the corresponding kind. To make that precise, he needed two "
            "dimensions."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def kripke(self):
        head = label(r"Kripke's diagnosis", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        e = island([-3.6, 1.3, 0], w=4.0, h=2.0, seed=160, color=NAME, name=r"what we imagine")
        tw = island([2.6, 1.3, 0], w=4.0, h=2.0, seed=161, color=WORLD, name=r"what is possible")
        te = wrapped_label(r"the clear, drinkable stuff in the rivers is not H$_2$O", 2.8, 19, NAME).move_to(e.shape)
        tt = wrapped_label(r"Twin Earth: \ watery XYZ, \ and no water at all", 2.8, 19, WORLD).move_to(tw.shape)
        arr = Arrow(e.shape.get_right(), tw.shape.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        al = label(r"is really", font_size=17, color=GREY_A).next_to(arr, UP, buff=0.06)
        rows = stack([(r"we do not conceive that \textit{water} is not H$_2$O: \ we conceive an epistemic "
                       r"counterpart of our situation", WHITE),
                      (r"that situation is possible: \ the illusion of contingency is explained", OK),
                      (r"pain: \ its reference is fixed by how it feels, \ so a situation that feels like pain "
                       r"\textit{is} pain", DESC),
                      (r"so pain without C-fibres firing is not explained away: \ Kripke's case against the identity "
                       r"theory", BAD)], font_size=21, aligned_edge=LEFT, width=12.2, buff=0.28).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Kripke himself explained away the cracks, case by case. <bookmark mark='a'/>When we seem to imagine that "
            "water is not H two O, what we actually imagine is a situation where the clear, drinkable stuff in the "
            "rivers is not H two O. <bookmark mark='b'/>And that situation is perfectly possible: it is Twin Earth, "
            "a world with no water in it. We conceive an epistemic counterpart of our own situation, and mistake "
            "it for a world where water itself is something else. <bookmark mark='c'/>So the illusion that it is "
            "contingent is explained. <bookmark mark='d'/>But try the same move with pain. The reference of pain is "
            "fixed by how it feels, so a situation that feels exactly like pain is a situation with pain. "
            "<bookmark mark='e'/>There is no counterpart to fall back on. If we can conceive pain without C-fibres "
            "firing, that is a real possibility, and pain is not C-fibre firing. That is Kripke's argument against "
            "the identity theory of mind."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(e), FadeIn(te), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(al), FadeIn(tw), FadeIn(tt))
            for mk, r in zip("cde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
