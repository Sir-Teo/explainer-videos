from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Aposteriori(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"The necessary \textit{a posteriori}", r"Can a necessary truth be discovered?",
                            lit=(1970, 1975), part=PART)
        with self.voiceover("Chapter three. The necessary a posteriori."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.venus()
        self.square()
        self.water()
        self.metre()

    def venus(self):
        head = label(r"Hesperus and Phosphorus", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sun = Dot([-2.9, -0.3, 0], radius=0.28, color=YELLOW)
        orb_v = Circle(radius=1.3, color=GREY_C, stroke_width=1.5).move_to(sun)
        orb_e = Circle(radius=2.4, color=GREY_D, stroke_width=1.5).move_to(sun)
        earth = Dot(sun.get_center() + DOWN * 2.4, radius=0.15, color=WORLD)
        el = label(r"Earth", font_size=17, color=WORLD).next_to(earth, DOWN, buff=0.1)
        ve = Dot(sun.get_center() + np.array([-1.15, -0.6, 0]), radius=0.13, color=NAME)   # east of the Sun: dusk
        vm = Dot(sun.get_center() + np.array([1.15, -0.6, 0]), radius=0.13, color=DESC)    # west of the Sun: dawn
        lh = label(r"Hesperus: \ the evening star", font_size=17, color=NAME).next_to(ve, LEFT, buff=0.15)
        lp = label(r"Phosphorus: \ the morning star", font_size=17, color=DESC).next_to(vm, RIGHT, buff=0.15)
        sight_e = DashedLine(earth.get_center(), ve.get_center(), color=NAME, stroke_width=1.5)
        sight_m = DashedLine(earth.get_center(), vm.get_center(), color=DESC, stroke_width=1.5)
        steps = VGroup(
            MathTex(r"(1)\quad \text{Hesperus} = \text{Phosphorus}", font_size=28),
            MathTex(r"(2)\quad a = b \to \Box(a = b)", font_size=28),
            MathTex(r"(3)\quad \Box(\text{Hesperus} = \text{Phosphorus})", font_size=28, color=OK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 1.2, 0])
        why = VGroup(label(r"found by observation", font_size=19, color=GREY_A),
                     label(r"Part 21: \ the necessity of identity", font_size=19, color=GREY_A),
                     label(r"necessary, \ yet known only by experience", font_size=19, color=OK))
        for w_, st in zip(why, steps):
            w_.next_to(st, DOWN, buff=0.08, aligned_edge=LEFT)
        concl = label(r"the necessary \textit{a posteriori}: \ Kant thought every necessary truth was knowable a "
                      r"priori", font_size=21, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The ancients named a bright star of the evening Hesperus, and a bright star of the morning Phosphorus. "
            "<bookmark mark='a'/>Both are Venus, seen on either side of the Sun. That was a discovery, credited in "
            "the Greek tradition to Pythagoras or Parmenides. <bookmark mark='b'/>Now run the argument. Hesperus is "
            "Phosphorus, as observation showed. <bookmark mark='c'/>If a is b, then necessarily a is b: that was the "
            "necessity of identity, proved in Part 21 from Leibniz's law. And the names are rigid, so they pick out "
            "Venus at every world. <bookmark mark='d'/>So it is necessary that Hesperus is Phosphorus. There is no "
            "possible world where Venus is two planets. Yet nobody could have known it from the armchair. "
            "<bookmark mark='e'/>A truth that is necessary and known only a posteriori. Kant had taken it for "
            "granted that whatever is necessary can be known a priori. Kripke pulled the two notions apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sun), Create(orb_v), Create(orb_e), FadeIn(earth), FadeIn(el),
                      FadeIn(ve), FadeIn(vm), Create(sight_e), Create(sight_m), FadeIn(lh), FadeIn(lp))
            vo.wait_until("a")
            self.play(Indicate(ve, scale_factor=1.6), Indicate(vm, scale_factor=1.6))
            for mk, st, w_ in zip("bcd", steps, why):
                vo.wait_until(mk)
                self.play(Write(st), FadeIn(w_))
            vo.wait_until("e")
            self.play(FadeIn(concl))
        self.clear_scene()

    def square(self):
        head = label(r"Two distinctions, \ four boxes", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cw, ch = 4.6, 1.55
        x0, y0 = -1.0, 0.9
        boxes = VGroup()
        texts = [
            (r"$2 + 2 = 4$; \ bachelors are unmarried", OK),
            (r"Hesperus = Phosphorus; \ water is H$_2$O; \ this table is not made of ice", NAME),
            (r"`stick S is one metre long', \ said when the metre is fixed by S", DESC),
            (r"Venus is visible tonight; \ Humphrey lost", GREY_A),
        ]
        for i in range(4):
            r, c = divmod(i, 2)
            b = Rectangle(width=cw, height=ch, color=GREY_C, stroke_width=2).move_to(
                [x0 + (c - 0.5) * cw, y0 - r * ch, 0])
            t = wrapped_label(texts[i][0], cw - 0.4, 19, texts[i][1]).move_to(b)
            boxes.add(VGroup(b, t))
        top = VGroup(label(r"\textit{a priori}", font_size=22, color=WORLD).next_to(boxes[0][0], UP, buff=0.12),
                     label(r"\textit{a posteriori}", font_size=22, color=WORLD).next_to(boxes[1][0], UP, buff=0.12))
        side = VGroup(label(r"necessary", font_size=22, color=ABS).next_to(boxes[0][0], LEFT, buff=0.2),
                      label(r"contingent", font_size=22, color=ABS).next_to(boxes[2][0], LEFT, buff=0.2))
        notes = stack([(r"\textit{a priori}: \ knowable without experience \ (epistemology)", WORLD),
                       (r"necessary: \ true at every possible world \ (metaphysics)", ABS),
                       (r"Kant \ (1781): \ the two coincide; \ Kripke \ (1970): \ they come apart, \ both ways",
                        GOAL)], font_size=20, aligned_edge=LEFT, width=11.6).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Two distinctions are at work. <bookmark mark='a'/>A priori and a posteriori belong to the theory of "
            "knowledge: can the truth be known without experience? <bookmark mark='b'/>Necessary and contingent "
            "belong to metaphysics: is it true at every possible world? <bookmark mark='c'/>Cross them and you get "
            "four boxes. <bookmark mark='d'/>Necessary a priori: two plus two is four. <bookmark mark='e'/>Contingent "
            "a posteriori: Venus is visible tonight; Humphrey lost. <bookmark mark='f'/>Necessary a posteriori: "
            "Hesperus is Phosphorus, water is H two O, and, Kripke argued, a given wooden table could not have been "
            "made of ice, since its origin is essential to it. <bookmark mark='g'/>And the strangest box, the "
            "contingent a priori, which we meet in a moment. <bookmark mark='h'/>Kant had held that the two "
            "distinctions coincide. Kripke argued that they come apart in both directions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(top))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), FadeIn(side))
            vo.wait_until("c")
            self.play(*[Create(b[0]) for b in boxes])
            for mk, i in zip("defg", (0, 3, 1, 2)):
                vo.wait_until(mk)
                self.play(FadeIn(boxes[i][1]))
            vo.wait_until("h")
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    def water(self):
        hc = history_card(1975, r"Hilary Putnam", r"`The Meaning of ``Meaning''\thinspace'", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        e = island([-3.6, -0.4, 0], w=4.0, h=2.4, seed=71, color=NAME, name=r"Earth, \ 1750")
        t = island([2.0, -0.4, 0], w=4.0, h=2.4, seed=72, color=WORLD, name=r"Twin Earth, \ 1750")
        mol_e = VGroup(*[label(r"H$_2$O", font_size=19, color=NAME).move_to([-4.5 + 0.9 * (k % 3), -0.45 - 0.5 *
                                                                            (k // 3), 0]) for k in range(6)])
        mol_t = VGroup(*[label(r"XYZ", font_size=19, color=WORLD).move_to([1.1 + 0.9 * (k % 3), -0.45 - 0.5 *
                                                                          (k // 3), 0]) for k in range(6)])
        osc = VGroup(person([-3.6, 0.35, 0], color=DESC, name=r"Oscar", font_size=17),
                     person([2.0, 0.35, 0], color=DESC, name=r"Twin Oscar", font_size=17))
        rows = stack([(r"same appearance, \ taste, \ use; \ the two Oscars are in the same inner state", WHITE),
                      (r"yet `water' on Earth means H$_2$O; \ on Twin Earth, \ XYZ: \ `meanings just ain't in the "
                       r"head'", GOAL),
                      (r"`water' is rigid: \ it picks out H$_2$O at every world, \ so `water is H$_2$O' is "
                       r"necessary", NAME),
                      (r"and Twin Earth is not a world where \textit{water} is XYZ: \ it is a world without water",
                       BAD)], font_size=20, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Hilary Putnam extended the point to natural kinds. <bookmark mark='a'/>Imagine Twin Earth, exactly like "
            "Earth except that the clear liquid in its rivers and taps is not H two O but a different compound, XYZ. "
            "Go back to 1750, before chemistry could tell them apart. Oscar on Earth and Twin Oscar on Twin Earth are "
            "in the same inner state when they say water. <bookmark mark='b'/>Yet Oscar's word refers to H two O and "
            "Twin Oscar's to XYZ. Meanings, Putnam concluded, just ain't in the head. <bookmark mark='c'/>Kripke and "
            "Putnam agreed that water works like a name: it rigidly picks out the stuff that is actually here, H two "
            "O, at every world. So water is H two O is necessary, though discovered. <bookmark mark='d'/>And Twin "
            "Earth is not a world where water is XYZ. It is a world without water, where something else plays "
            "water's role."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(e), FadeIn(t))
            vo.wait_until("a")
            self.play(FadeIn(mol_e), FadeIn(mol_t), FadeIn(osc), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def metre(self):
        head = label(r"The contingent \textit{a priori}", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        bar = Rectangle(width=4.0, height=0.3, color=NAME, fill_opacity=0.6).move_to([-2.6, 2.0, 0])
        bl = label(r"stick S, \ Paris, \ time $t_0$", font_size=18, color=NAME).next_to(bar, UP, buff=0.12)
        hot = Rectangle(width=4.4, height=0.3, color=BAD, fill_opacity=0.5).move_to([-2.4, 0.85, 0])
        hl = label(r"another world: \ S was heated at $t_0$", font_size=18, color=BAD).next_to(hot, UP, buff=0.12)
        ruler = NumberLine(x_range=[0, 1.1, 0.1], length=4.4, include_numbers=False, color=GREY_B).next_to(
            hot, DOWN, buff=0.2).align_to(hot, LEFT)
        rl = label(r"one metre \ (fixed by S's actual length)", font_size=16, color=GREY_A).next_to(ruler, DOWN,
                                                                                                   buff=0.1)
        side = stack([(r"Wittgenstein: \ one can say of the standard metre neither that it is, \ nor that it is "
                       r"not, \ one metre long", GREY_A),
                      (r"Kripke: \ fix `one metre' as `the length of S at $t_0$': \ then `S is one metre long at "
                       r"$t_0$' is known \textit{a priori}", DESC),
                      (r"but it is contingent: \ S could have been longer, \ and `one metre' still names the length "
                       r"it actually has", BAD),
                      (r"Evans: \ `let Julius be whoever invented the zip': \ `Julius invented the zip' is \textit{a "
                       r"priori}, \ yet contingent", GOAL)], font_size=21, aligned_edge=LEFT, width=12.2).to_edge(
            DOWN, buff=0.45)
        with self.voiceover(
            "The fourth box. <bookmark mark='a'/>Wittgenstein remarked that there is one thing of which we can say "
            "neither that it is one metre long nor that it is not: the standard metre bar in Paris. "
            "<bookmark mark='b'/>Kripke disagreed. Suppose we fix the reference of one metre by stipulation: one "
            "metre is the length of stick S at time t nought. Then we know without measuring that S is one metre "
            "long at t nought. <bookmark mark='c'/>But it is not necessary. Had S been heated at t nought, it would "
            "have been longer than one metre, since one metre rigidly names the length S actually has. A priori, yet "
            "contingent. <bookmark mark='d'/>Gareth Evans made the same point with a stipulated name: let Julius be "
            "whoever invented the zip. Then Julius invented the zip, if anyone did, is known a priori, though "
            "Julius might have spent his life on something else. Necessity and knowability really are two "
            "different things."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(hot), FadeIn(hl), Create(ruler), FadeIn(rl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
