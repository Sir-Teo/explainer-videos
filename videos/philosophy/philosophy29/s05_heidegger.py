from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403

CHAIN = [("hammer", [-5.2, 0.6]), ("nails", [-3.0, 0.6]), ("board", [-0.8, 0.6]), ("roof", [1.4, 0.6]),
         ("shelter", [3.6, 0.6]), ("a way of living", [5.6, -0.6])]


class Heidegger(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Being-in-the-world", r"Is the world a collection of objects?", lit=(1927,), part=PART)
        with self.voiceover("Chapter four. Being-in-the-world."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.question()
        self.pictures()
        self.hammer()
        self.care()
        self.shadow()

    def question(self):
        hc = history_card(1927, r"Martin Heidegger", r"\textit{Being and Time}", width=4.8, color=HIST).to_corner(
            UL, buff=0.3)
        rows = [
            (r"the question", r"what does it mean \textit{to be}? \ not which things exist, \ but what their being "
                              r"consists in", SIGN),
            (r"Dasein", r"`being-there': \ the entity for which its own being is an issue: \ us", BODY),
            (r"the method", r"begin with how Dasein ordinarily exists, \ before any theory: \ everyday "
                            r"being-in-the-world", WORLD),
        ]
        g = rows_table(rows, top=1.2, gap=0.55)
        with self.voiceover(
            "Husserl's assistant, Martin Heidegger, turned phenomenology in a new direction. In 1927 he published "
            "Being and Time. <bookmark mark='a'/>Its question is the oldest in philosophy: what does it mean to be? "
            "Not which things exist, the question of Part 20, but what the being of anything consists in. "
            "<bookmark mark='b'/>He approaches it through the one entity that asks it: Dasein, being-there, his word "
            "for the kind of being we are, the entity for which its own being is an issue. "
            "<bookmark mark='c'/>And he begins not with perception or knowledge, as Husserl did, but with how we "
            "ordinarily exist, before any theory: everyday being-in-the-world."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def pictures(self):
        head = label(r"Two pictures of a mind and its world", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        mind = Circle(radius=0.7, color=ACT, fill_opacity=0.2).move_to([-4.6, 0.4, 0])
        ml = label(r"a mind", font_size=19, color=ACT).move_to(mind)
        objs = VGroup(*[Square(side_length=0.45, color=OBJ, fill_opacity=0.3).move_to([x, y, 0]) for x, y in
                        [(-2.4, 1.4), (-1.6, 0.2), (-2.6, -0.8), (-1.2, -1.4)]])
        rays = VGroup(*[DashedLine(mind.get_right(), o.get_left(), color=GREY_B, stroke_width=2) for o in objs])
        lt = label(r"Descartes: \ a subject representing objects", font_size=19, color=GREY_A).move_to([-3.2, -2.3, 0])
        web = VGroup()
        cen = np.array([3.4, 0.2, 0])
        nodes = [cen + 1.5 * np.array([math.cos(t), math.sin(t), 0]) for t in np.linspace(0, 2 * math.pi, 7)[:-1]]
        for p in nodes:
            web.add(Line(cen, p, color=WORLD, stroke_width=2))
        for a, b in zip(nodes, nodes[1:] + nodes[:1]):
            web.add(Line(a, b, color=WORLD, stroke_width=1.5))
        dots = VGroup(*[Dot(p, radius=0.08, color=WORLD) for p in nodes])
        me = Dot(cen, radius=0.14, color=BODY)
        rt = label(r"Heidegger: \ always already in a world of involvements", font_size=19, color=GREY_A).move_to(
            [3.4, -2.3, 0])
        foot = label(r"being-in-the-world: \ one phenomenon, \ hyphenated, \ not a mind plus a world", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Compare two pictures. <bookmark mark='a'/>In the picture that runs from Descartes to much of cognitive "
            "science, a mind sits on one side, objects on the other, and the mind relates to the world by "
            "representing it, by having inner pictures of outer things. <bookmark mark='b'/>Heidegger rejects the "
            "starting point. We are not first minds who then reach out to a world. We are always already in a world: "
            "a web of involvements, things to use, tasks under way, other people. <bookmark mark='c'/>Hence the "
            "hyphens. Being-in-the-world is a single phenomenon, not a mind plus a world plus a relation between them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(mind), FadeIn(ml), FadeIn(objs), LaggedStart(*[Create(r) for r in rays], lag_ratio=0.2),
                      FadeIn(lt))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in web], lag_ratio=0.05), FadeIn(dots), FadeIn(me), FadeIn(rt),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def hammer(self):
        head = label(r"The hammer", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        nodes, edges = VGroup(), VGroup()
        for i, (t, (x, y)) in enumerate(CHAIN):
            lab = label(t, font_size=19, color=OBJ)
            bx = RoundedRectangle(width=lab.width + 0.4, height=lab.height + 0.3, corner_radius=0.12, color=OBJ,
                                  stroke_width=2)
            nodes.add(VGroup(bx, lab).move_to([x, y, 0]))
        for a, b in zip(nodes, nodes[1:]):
            edges.add(Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2,
                            max_tip_length_to_length_ratio=0.15))
        inorder = label(r"in order to", font_size=16, color=GREY_A).next_to(edges[0], UP, buff=0.05)
        crack = VGroup(Line([-5.5, 1.0, 0], [-5.1, 0.3, 0], color=BAD, stroke_width=5),
                       Line([-5.1, 0.3, 0], [-4.9, 0.9, 0], color=BAD, stroke_width=5))
        rows = [
            (r"ready-to-hand", r"\textit{zuhanden}: \ in use the hammer withdraws; \ we attend to the nail, \ the roof, "
                               r"\ the storm coming", WORLD),
            (r"present-at-hand", r"\textit{vorhanden}: \ an object with properties \ (weight, \ shape), \ for staring "
                                 r"at \ or for science", OBJ),
            (r"breakdown", r"the hammer breaks, \ is missing, \ or is in the way: \ it becomes conspicuous, \ and the "
                           r"whole web shows itself", BAD),
        ]
        g = rows_table(rows, top=-1.0, gap=0.4)
        with self.voiceover(
            "The famous example is a hammer. <bookmark mark='a'/>Hammering, I do not perceive the hammer as an "
            "object with a weight and a shape. It withdraws. My attention is on the nail, and through the nail on "
            "the board, the roof, the shelter it gives, and what it is all for. Heidegger calls this being "
            "ready-to-hand. <bookmark mark='b'/>Each piece of equipment refers to others: the hammer is in order to "
            "drive nails, the nails in order to hold boards, the boards in order to make a roof, and the chain ends "
            "in a way of living that it is all for the sake of. <bookmark mark='c'/>To look at the hammer as an "
            "object with properties, a weight of four hundred grams, a steel head, is to treat it as present-at-hand. "
            "For Heidegger this is a derived and special attitude, the attitude of theory. "
            "<bookmark mark='d'/>We are thrown into it when equipment breaks down. The head flies off, and the hammer "
            "suddenly becomes conspicuous; if it is missing, or in the way, the same. And in the breakdown, the "
            "whole web of references that was there all along lights up."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(nodes[0]), FadeIn(g[0]), nodes[0].animate.set_opacity(0.35))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(e), FadeIn(n)) for e, n in zip(edges, nodes[1:])],
                                  lag_ratio=0.4), FadeIn(inorder), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(g[1]))
            vo.wait_until("d")
            self.play(nodes[0].animate.set_opacity(1), Create(crack), FadeIn(g[2]))
            self.play(LaggedStart(*[Indicate(n, color=SIGN, scale_factor=1.08) for n in nodes], lag_ratio=0.2))
        self.clear_scene()

    def care(self):
        head = label(r"Care, \ and time", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"thrown", r"we find ourselves already in a situation we did not choose: \ facticity", OBJ),
            (r"projecting", r"we understand ourselves by our possibilities: \ what we can be", ACT),
            (r"falling", r"absorbed in `the they', \ \textit{das Man}: \ one does what one does", GREY_A),
            (r"care", r"the unity of all three: \ Dasein's being is care, \ \textit{Sorge}", BODY),
            (r"being-towards-death", r"facing our own end individualizes us: \ authenticity is owning our "
                                     r"possibilities", BAD),
            (r"time", r"care is temporal: \ having-been, \ being-ahead, \ being-alongside: \ chapter 3, \ "
                      r"radicalized", TIME),
        ]
        g = rows_table(rows, top=1.7, gap=0.36)
        with self.voiceover(
            "What is the being of Dasein? <bookmark mark='a'/>We are thrown: we find ourselves already in a "
            "situation we did not choose, with a body, a language, a history. <bookmark mark='b'/>We are projecting: "
            "we understand ourselves by our possibilities, by what we can be. <bookmark mark='c'/>And we are falling: "
            "absorbed in what Heidegger calls the they, das Man, where one does what one does and thinks what one "
            "thinks. <bookmark mark='d'/>The unity of these is care. <bookmark mark='e'/>Facing our own death, which "
            "no one can die for us, pulls us out of the they; authenticity is owning our possibilities as ours. "
            "<bookmark mark='f'/>And care is temporal through and through: having-been, being-ahead-of-itself, "
            "being alongside things. Husserl's retention and protention, from chapter three, become the structure of "
            "existence itself."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def shadow(self):
        head = label(r"The shadow", font_size=30, color=BAD).to_edge(UP, buff=0.35)
        rows = [
            (r"1933", r"joins the Nazi party; \ rector of Freiburg, \ resigns in 1934; \ a member until 1945", BAD),
            (r"the \textit{Black Notebooks}", r"private notebooks published from 2014, \ with antisemitic passages", BAD),
            (r"the debate", r"is the politics separable from the philosophy? \ answers range from yes to not at all", HIST),
            (r"the influence", r"Sartre, \ Arendt, \ Gadamer, \ Levinas, \ Derrida, \ Dreyfus: \ much of what follows", GOAL),
        ]
        g = rows_table(rows, top=1.4, gap=0.55)
        with self.voiceover(
            "This chapter cannot end without the shadow over it. <bookmark mark='a'/>In 1933 Heidegger joined the "
            "Nazi party and became rector of the University of Freiburg. He resigned the rectorship in 1934, but "
            "remained a party member until 1945. <bookmark mark='b'/>His private notebooks, published from 2014, "
            "contain antisemitic passages. <bookmark mark='c'/>Whether, and how far, the politics infects the "
            "philosophy is still argued, with answers from not at all to through and through. "
            "<bookmark mark='d'/>What is not in doubt is the influence: Sartre, Hannah Arendt, Gadamer, Emmanuel "
            "Levinas, Derrida and Hubert Dreyfus all start from him, and so does much of the rest of this part."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
