from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Mary(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Mary's room", r"Does knowing every physical fact tell you what red is like?",
                            lit=(1982,), part=PART)
        with self.voiceover("Chapter three. Mary's room."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.room()
        self.argument()
        self.model()
        self.replies()

    def room(self):
        hc = history_card(1982, r"Frank Jackson", r"`Epiphenomenal Qualia', \ \textit{Philosophical Quarterly}",
                          width=6.2, color=HIST).to_corner(UL, buff=0.3)
        room = Square(side_length=3.2, color=GREY_B).move_to([-3.2, -0.6, 0])
        mary = VGroup(Circle(radius=0.22, color=WHITE), Line([0, -0.22, 0], [0, -0.9, 0], color=WHITE)).move_to(
            [-3.6, -0.6, 0])
        screen = Rectangle(width=1.0, height=0.7, color=GREY_A, fill_color=GREY_D, fill_opacity=0.6).move_to(
            [-2.4, -0.2, 0])
        tomato = Circle(radius=0.35, color="#E0302A", fill_opacity=1).move_to([1.4, -0.6, 0])
        door = Line(room.get_corner(UR) + DOWN * 0.8, room.get_corner(DR) + UP * 0.8, color=BLACK, stroke_width=8)
        rows = stack([(r"a brilliant scientist, \ raised in a black-and-white room", GREY_A),
                      (r"she learns every physical fact about colour vision", PHYS),
                      (r"then she walks out, \ and sees a ripe tomato", FEEL),
                      (r"does she learn something new?", GOAL)], font_size=21, aligned_edge=LEFT,
                     buff=0.3).move_to([3.6, 0.6, 0])
        with self.voiceover(
            "Frank Jackson's argument of 1982 is a story. <bookmark mark='a'/>Mary is a brilliant scientist who has "
            "lived all her life in a black-and-white room, learning about the world through a black-and-white "
            "monitor. <bookmark mark='b'/>She becomes the world's expert on colour vision. She knows every physical "
            "fact there is to know about what happens when we see a ripe tomato: the wavelengths, the cones, the "
            "neural pathways, the words we say. <bookmark mark='c'/>Then one day she walks out, and sees a ripe "
            "tomato. <bookmark mark='d'/>Does she learn something new? It seems obvious that she does: she learns "
            "what it is like to see red."
        ) as vo:
            self.play(FadeIn(hc), Create(room), FadeIn(mary), FadeIn(screen))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(screen, color=PHYS))
            vo.wait_until("c")
            self.play(Create(door), mary.animate.move_to([0.4, -0.6, 0]), FadeIn(tomato), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Indicate(tomato, color=FEEL, scale_factor=1.2))
        self.clear_scene()

    def argument(self):
        head = label(r"The knowledge argument", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"1.", r"before her release, \ Mary knows every physical truth about colour vision", PHYS),
                (r"2.", r"on her release, \ she learns a truth about colour vision", FEEL),
                (r"so", r"not every truth is a physical truth: \ physicalism is false", BAD),
                (r"the joint", r"premise 2 needs `learns a truth'; \ the replies all press there", GOAL)]
        g = rows_table(rows, x_label=-6.0, x_text=-4.6, top=1.6, gap=0.5, width=10.6)
        with self.voiceover(
            "Laid out, the knowledge argument is short. <bookmark mark='a'/>One: before her release, Mary knows "
            "every physical truth about colour vision. <bookmark mark='b'/>Two: on her release she learns a truth "
            "about colour vision, what it is like to see red. <bookmark mark='c'/>So not every truth is a physical "
            "truth, and physicalism is false. <bookmark mark='d'/>The argument is valid. Every reply presses on the "
            "second premise, on what exactly she learns, and the Reasoner can make that precise."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def model(self):
        d = load("mary")
        head = label(r"What Mary can rule out", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert len(d["before"]) == 3 and len(d["after"]) == 1 and d["physical_agree"] == 1
        cols = [FEEL, SELF, GREY_B]
        boxes = VGroup()
        for k, (w, c) in enumerate(zip(d["worlds"], cols)):
            b = RoundedRectangle(width=3.6, height=2.0, corner_radius=0.2, color=c, fill_opacity=0.06)
            t = VGroup(wrapped_label(w["name"], 3.2, 20, c), label(r"physics: \ all as in the textbooks",
                                                                   font_size=16, color=PHYS)).arrange(DOWN, buff=0.3)
            boxes.add(VGroup(b, t.move_to(b)).move_to([-4.2 + 4.2 * k, 0.6, 0]))
        lb = label(r"before: \ 3 possibilities agree on every physical truth", font_size=20, color=PHYS).move_to(
            [0, -0.9, 0])
        cross = VGroup(*[Cross(boxes[k], stroke_color=BAD, stroke_width=4) for k in (1, 2)])
        la = label(r"after the tomato: \ 1 remains", font_size=20, color=FEEL).move_to([0, -1.5, 0])
        rows = stack([(r"dualist: \ she has ruled out real possibilities, \ so learnt a new fact", FEEL),
                      (r"ability hypothesis: \ she rules out nothing, \ and gains abilities", FUNC),
                      (r"phenomenal concept: \ three ways of presenting one fact, \ not three worlds", PHYS)],
                     font_size=19, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Model what Mary knows as the set of possibilities she cannot rule out. <bookmark mark='a'/>Before her "
            "release she knows every physical truth, so every possibility she leaves open agrees on all of them. "
            "What she cannot tell from her books is what seeing red is like. Perhaps it is like this. Perhaps it is "
            "the way green looks to the rest of us. Perhaps it is like nothing at all. "
            "<bookmark mark='b'/>Three possibilities, all physically the same. <bookmark mark='c'/>She sees the "
            "tomato, and two of them are gone. <bookmark mark='d'/>Now the readings divide. For the dualist, the "
            "three were real possibilities, so in ruling two out she learnt a fact that the physical truths left "
            "open. <bookmark mark='e'/>The physicalist has two ways to deny it: that she ruled anything out, or that "
            "what she ruled out were ever worlds. The next section takes them in turn."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(lb))
            vo.wait_until("c")
            self.play(Create(cross), boxes[0][0].animate.set_stroke(width=6), FadeIn(la))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
        self.clear_scene()

    def replies(self):
        d = load("mary")
        head = label(r"What Mary learns", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        assert len(d["abilities"]) == 3
        rows = [(r"abilities", r"Lewis \ (1988), \ Nemirow \ (1990): \ know-how, \ not know-that: \ to imagine, "
                               r"\ recognize and remember red", FUNC),
                (r"acquaintance", r"Conee \ (1994): \ she meets a property she already knew about", SIG),
                (r"a new concept", r"Loar \ (1990): \ an old fact, \ newly grasped under a phenomenal concept", PHYS),
                (r"the inventor", r"Jackson himself turned physicalist \ (1998, \ 2003): \ the intuition is an "
                                  r"illusion of introspection", SELF)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "Four replies. <bookmark mark='a'/>David Lewis and Laurence Nemirow: what Mary gains is know-how, not "
            "know-that. She becomes able to imagine red, to recognize it, and to remember it. She rules out "
            "nothing; she acquires abilities. <bookmark mark='b'/>Earl Conee: she becomes acquainted with a "
            "property she already knew all about, as you might meet someone you have read about. "
            "<bookmark mark='c'/>Brian Loar: she learns an old fact in a new way, under a phenomenal concept that "
            "picks out the same physical state her textbook concepts did. On this view the three possibilities "
            "were never three worlds, only three ways the one fact might have been presented to her. "
            "<bookmark mark='d'/>And Jackson himself changed sides around 1998. He came to think that the sense "
            "that Mary learns a new fact is an illusion produced by introspection, an idea chapter six develops."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
