from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Absolute(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"The absolute and its critics", r"Is the completed infinite a mathematical object?",
                            lit=(1883,), part=PART)
        with self.voiceover("Chapter four. The absolute, and its critics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.cantor()
        self.critics()
        self.wittgenstein()
        self.constructive()

    def cantor(self):
        hc = history_card(1899, r"Cantor to Dedekind", r"`consistent' and `inconsistent' multiplicities", width=6.2,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            VGroup(label(r"the transfinite", font_size=28, color=ORD),
                   label(r"$\aleph_0, \aleph_1, \dots$, \ $\omega, \omega + 1, \dots$: \ increasable, \ mathematical",
                         font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            VGroup(label(r"the absolute", font_size=28, color=CARD),
                   label(r"the totality of all of them: \ not increasable, \ not a set, \ for Cantor a sign of God",
                         font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            VGroup(label(r"inconsistent multiplicities", font_size=28, color=BAD),
                   label(r"collections that cannot be thought of as one thing \ without contradiction: \ "
                         r"the proper classes of Chapter 8", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.4, 0])
        with self.voiceover(
            "Cantor did not see his theory as mere mathematics. <bookmark mark='a'/>He distinguished the "
            "transfinite, the infinite numbers that can always be increased, from the absolute: the totality of all "
            "of them, which cannot be increased, and which he associated with God. <bookmark mark='b'/>In a letter to "
            "Dedekind in 1899, he even anticipated the paradoxes. Some multiplicities, he wrote, cannot be thought of "
            "as a single thing without contradiction, and the collection of all ordinals is one of them. "
            "<bookmark mark='c'/>These inconsistent multiplicities are what we now call proper classes."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Indicate(rows[2], color=BAD, scale_factor=1.03))
        self.clear_scene()

    def critics(self):
        head = label(r"The opposition", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        rows = [(r"Leopold Kronecker", r"`God made the integers; \ all else is the work of man' \ (attributed)",
                 r"opposed Cantor's appointments and papers"),
                (r"Henri Poincaré", r"`there is no actual infinite' \ (1906)", r"impredicative definitions are "
                                                                               r"circular"),
                (r"Hermann Weyl", r"\textit{Das Kontinuum} \ (1918)", r"rebuild analysis with predicative sets only"),
                (r"L.\ E.\ J.\ Brouwer", r"intuitionism \ (Part 5)", r"the infinite is only ever potential")]
        tab = VGroup()
        for i, (a, b, c) in enumerate(rows):
            y = 1.7 - 1.0 * i
            l1 = label(a, font_size=26, color=GOAL)
            l2 = label(b, font_size=22)
            l3 = label(c, font_size=20, color=GREY_A)
            l1.move_to([-6.2 + l1.width / 2, y + 0.18, 0])
            l2.move_to([-6.2 + l2.width / 2, y - 0.22, 0])
            l3.move_to([1.6 + l3.width / 2, y, 0])
            tab.add(VGroup(l1, l2, l3))
        with self.voiceover(
            "Not everyone was persuaded. <bookmark mark='a'/>Leopold Kronecker, in Berlin, is said to have declared "
            "that God made the integers, and all else is the work of man. He opposed Cantor's work, and Cantor "
            "believed he blocked his career. <bookmark mark='b'/>Henri Poincaré denied that there is any actual "
            "infinite, and objected to definitions that quantify over a totality including the thing defined. "
            "<bookmark mark='c'/>Hermann Weyl, in 1918, tried to rebuild analysis with only predicatively defined "
            "sets. <bookmark mark='d'/>And Brouwer, whom we met in Part 5, held that the infinite is only ever "
            "potential, as Aristotle had said."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def wittgenstein(self):
        q = quote_card(r"I would say, `I wouldn't dream of trying to drive anyone out of this paradise.' I would do "
                       r"something quite different: I would try to show you that it is not a paradise, so that you'll "
                       r"leave of your own accord.", r"Ludwig Wittgenstein", r"\textit{Lectures on the Foundations of "
                       r"Mathematics} (Cambridge, 1939)", width=11.0, font_size=26).move_to([0, 1.0, 0])
        pts = VGroup(label(r"what the diagonal proves: \ that no list is complete", font_size=26),
                     label(r"what it does not prove, \ Wittgenstein said: \ that there exists a larger totality",
                           font_size=26, color=GREY_A)).arrange(DOWN, buff=0.25).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The sharpest philosophical critic came later. <bookmark mark='a'/>In 1939, answering Hilbert directly, "
            "Ludwig Wittgenstein told his Cambridge students that he would not dream of driving anyone out of "
            "Cantor's paradise. He would try to show them it is not a paradise, so that they leave of their own "
            "accord. <bookmark mark='b'/>The diagonal, he argued, shows that no list of real numbers is complete. "
            "To read it as revealing a larger completed totality is a picture we add to the proof."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.5))
        self.clear_scene()

    def constructive(self):
        d = load("diagonal")
        head = label(r"The diagonal as an algorithm", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        box = VGroup(RoundedRectangle(width=3.2, height=1.4, corner_radius=0.15, stroke_color=SETC),
                     label(r"flip the diagonal", font_size=26, color=SETC))
        box[1].move_to(box[0])
        inp = label(r"any list of reals", font_size=24, color=GREY_A)
        out = label(r"a real not on it", font_size=24, color=GOAL)
        a1 = Arrow(LEFT, RIGHT, color=GREY_B)
        a2 = Arrow(LEFT, RIGHT, color=GREY_B)
        flow = VGroup(inp, a1, box, a2, out).arrange(RIGHT, buff=0.3).move_to([0, 0.8, 0])
        pts = VGroup(label(r"valid even for Brouwer: \ the proof is a construction", font_size=26, color=OK),
                     label(r"so the disagreement is not about the proof, \ but about what it is a proof \textit{of}",
                           font_size=26),
                     label(r"Part 9: \ what mathematics is about", font_size=22, color=GREY_B)).arrange(
            DOWN, buff=0.3).next_to(flow, DOWN, buff=0.8)
        with self.voiceover(
            "There is common ground. <bookmark mark='a'/>Read the diagonal argument as an algorithm: given any list "
            "of real numbers, it constructs a real number that is not on the list. <bookmark mark='b'/>In that form "
            "even Brouwer accepts it. So the disagreement is not about whether the proof is correct. It is about "
            "what the proof is a proof of: a fact about completed infinite totalities, or a fact about what lists "
            "can do. That question, what mathematics is about, is Part 9's."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in flow], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.5))
        self.clear_scene()
