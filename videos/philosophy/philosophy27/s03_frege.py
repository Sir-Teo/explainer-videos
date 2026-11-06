from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


class Frege(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Sense and reference", r"How can $a = b$ be news?", lit=(1892,), part=PART)
        with self.voiceover("Chapter two. Sense and reference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.venus()
        self.medians()
        self.senses()
        self.indirect()

    def venus(self):
        head = label(r"The evening star and the morning star", font_size=30, color=CONN).to_edge(UP, buff=0.3)

        def sky(x, side, name, when):
            hor = Line([x - 2.0, 0.6, 0], [x + 2.0, 0.6, 0], color=GREY_C, stroke_width=2)
            sun = Arc(radius=0.35, start_angle=0, angle=PI, color=TRUTH, fill_opacity=0.9, stroke_width=0).move_to(
                [x - 1.2 * side, 0.6 + 0.17, 0])
            star = Star(n=5, outer_radius=0.13, color=WHITE, fill_opacity=1).move_to([x - 0.4 * side, 1.6, 0])
            nm = label(name, font_size=22, color=NAME).next_to(star, UP, buff=0.12)
            wt = label(when, font_size=17, color=GREY_A).next_to(hor, DOWN, buff=0.12)
            return VGroup(hor, sun, star, nm, wt)

        ev = sky(-3.6, -1, r"Hesperus", r"after sunset, \ in the west")
        mo = sky(3.6, 1, r"Phosphorus", r"before sunrise, \ in the east")
        c = np.array([0, -1.8, 0])
        sun = Dot(c, radius=0.14, color=TRUTH)
        vo_orbit = Circle(radius=0.75, color=GREY_B, stroke_width=1.5).move_to(c)
        earth_orbit = Circle(radius=1.35, color=GREY_D, stroke_width=1.5).move_to(c)
        earth = Dot(c + np.array([0, -1.35, 0]), radius=0.09, color=WORLD)
        ven = Dot(c + np.array([0.75, 0, 0]), radius=0.08, color=WHITE)
        vtag = label(r"Venus", font_size=18, color=REF).next_to(ven, RIGHT, buff=0.1)
        rows = stack([(r"`Hesperus = Hesperus': \ trivial, \ known a priori", GREY_A),
                      (r"`Hesperus = Phosphorus': \ a discovery of ancient astronomy", TRUTH)], font_size=21,
                     aligned_edge=LEFT, width=5.2, buff=0.25).move_to([4.2, -2.0, 0])
        with self.voiceover(
            "Frege's example came from the sky. <bookmark mark='a'/>After sunset, a bright star appears in the west: "
            "the Greeks called it Hesperus, the evening star. <bookmark mark='b'/>Before sunrise, a bright star "
            "appears in the east: Phosphorus, the morning star. <bookmark mark='c'/>They are one object, the planet "
            "Venus, seen on either side of the Sun. <bookmark mark='d'/>Hesperus is Hesperus tells you nothing. "
            "Hesperus is Phosphorus was a discovery of ancient astronomy. If a name contributed only its bearer, as "
            "Mill held, the two sentences would say the same thing, and they plainly do not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ev))
            vo.wait_until("b")
            self.play(FadeIn(mo))
            vo.wait_until("c")
            self.play(FadeIn(sun), Create(vo_orbit), Create(earth_orbit), FadeIn(earth), FadeIn(ven), FadeIn(vtag))
            self.play(Rotate(ven, angle=-PI, about_point=c), FadeOut(vtag), run_time=2)
            self.play(FadeIn(vtag.next_to(ven, LEFT, buff=0.1)))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def medians(self):
        d = load("medians")
        head = label(r"Frege's own example: \ three descriptions, \ one point", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        off = np.array([-2.6, -0.4, 0])
        A, B, C = (np.array([x, y, 0]) + off for x, y in d["triangle"])
        tri = Polygon(A, B, C, color=GREY_B, stroke_width=3)
        mids = d["midpoints"]
        cols = {"a": NAME, "b": REF, "c": SENSE}
        lines = {k: Line(v, np.array([*mids[k], 0]) + off, color=cols[k], stroke_width=3)
                 for k, v in (("a", A), ("b", B), ("c", C))}
        ltags = VGroup(*[label(f"${k}$", font_size=22, color=cols[k]).next_to(lines[k].get_start(), DOWN if k != "c"
                                                                              else UP, buff=0.12)
                         for k in ("a", "b", "c")])
        P = {k: np.array([*v, 0]) + off for k, v in d["points"].items()}
        cen = np.array([*d["centroid"], 0]) + off
        dot = Dot(cen, radius=0.09, color=TRUTH)
        assert d["spread"] < 1e-12
        descs = stack([(r"`the point where $a$ meets $b$'", NAME),
                       (r"`the point where $b$ meets $c$'", REF),
                       (r"`the point where $c$ meets $a$'", SENSE)], font_size=22, aligned_edge=LEFT, buff=0.25
                      ).move_to([3.6, 1.0, 0])
        px, py = d["points"]["ab"]
        assert all(abs(d["points"][k][0] - px) < 1e-6 and abs(d["points"][k][1] - py) < 1e-6 for k in ("bc", "ca"))
        vals = stack([(rf"computed: \ all three are $({px:.3f},\ {py:.3f})$", OK),
                      (r"three senses, \ one reference", TRUTH),
                      (r"`the point where $a$ meets $b$ = the point where $b$ meets $c$' \ is a theorem, \ not a "
                       r"triviality", GOAL)], font_size=20, aligned_edge=LEFT, width=5.6, buff=0.25).move_to([3.6, -1.4, 0])
        with self.voiceover(
            "Frege gave his own example from geometry. <bookmark mark='a'/>Take a triangle, and draw the lines a, b "
            "and c from each corner to the midpoint of the opposite side. <bookmark mark='b'/>Now consider three "
            "descriptions: the point where a meets b, the point where b meets c, and the point where c meets a. "
            "<bookmark mark='c'/>The Reasoner computes all three intersections. They are the same point, to the "
            "last digit of the arithmetic. <bookmark mark='d'/>The three descriptions present that point in "
            "different ways. Frege called the way of presentation the sense of an expression, and the thing "
            "presented its reference. That the first point is the second is a theorem of geometry, not a "
            "triviality, because the senses differ though the reference is the same."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(tri))
            self.play(*[Create(l) for l in lines.values()], FadeIn(ltags))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in descs], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(dot, scale=2), FadeIn(vals[0]))
            self.play(Indicate(dot, color=TRUTH, scale_factor=2))
            vo.wait_until("d")
            self.play(FadeIn(vals[1]))
            self.play(FadeIn(vals[2]))
        self.clear_scene()

    def senses(self):
        head = label(r"Sense and reference, \ for every expression", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{expression}", r"\text{sense}", r"\text{reference}"]
        rows = [[label(r"a name: \ `Hesperus'", font_size=21, color=NAME),
                 label(r"a mode of presentation", font_size=21, color=SENSE),
                 label(r"Venus", font_size=21, color=REF)],
                [label(r"a predicate: \ `is a planet'", font_size=21, color=NAME),
                 label(r"a way of grasping a concept", font_size=21, color=SENSE),
                 label(r"a concept: \ a function to truth values", font_size=21, color=REF)],
                [label(r"a sentence: \ `Hesperus is a planet'", font_size=21, color=NAME),
                 label(r"a thought", font_size=21, color=SENSE),
                 label(r"a truth value: \ the True", font_size=21, color=REF)]]
        grid = ValueGrid(hd, rows, col_w=[4.4, 4.0, 4.4], cell_h=0.6, font_size=22).move_to([0, 0.8, 0])
        comp = stack([(r"swap `Hesperus' for `Phosphorus': \ the reference of the whole, \ the True, \ is unchanged",
                       REF),
                      (r"but the thought changes: \ one can believe the first and doubt the second", SENSE),
                      (r"compositionality: \ the sense \ (and the reference) \ of a whole is fixed by those of its "
                       r"parts", GOAL)], font_size=21, aligned_edge=LEFT, width=12.0, buff=0.25).move_to([0, -2.1, 0])
        with self.voiceover(
            "Frege applied the distinction to every kind of expression. <bookmark mark='a'/>A name has a sense, a "
            "mode of presentation, and a reference, its bearer. <bookmark mark='b'/>A predicate refers to a concept, "
            "which Frege took to be a function from objects to truth values. <bookmark mark='c'/>And a whole "
            "sentence has a thought as its sense, and a truth value as its reference: the True or the False. "
            "<bookmark mark='d'/>Swap Hesperus for Phosphorus in Hesperus is a planet, and the reference of the "
            "whole is unchanged: still the True. <bookmark mark='e'/>But the thought changes, since someone could "
            "believe the first and doubt the second. <bookmark mark='f'/>Both levels obey one principle, "
            "compositionality: the sense and the reference of a whole are fixed by those of its parts. Every formal "
            "semantics in this part builds on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]])
            for mk, r in zip("def", comp):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def indirect(self):
        head = label(r"Where substitution fails", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        s1 = label(r"the ancients believed that \ \underline{Hesperus} \ is seen in the evening", font_size=26,
                   color=TRUTH)
        s2 = label(r"the ancients believed that \ \underline{Phosphorus} \ is seen in the evening", font_size=26,
                   color=TRUTH)
        pair = VGroup(VGroup(s1, tv(True, 28)).arrange(RIGHT, buff=0.4),
                      VGroup(s2, tv(False, 28)).arrange(RIGHT, buff=0.4)).arrange(DOWN, buff=0.4,
                                                                                    aligned_edge=RIGHT).move_to(
            [0, 1.2, 0])
        rows = stack([(r"inside `believes that', \ swapping co-referring names can change the truth value", BAD),
                      (r"Frege: \ in such indirect contexts, \ words refer to their \textit{customary senses}", SENSE),
                      (r"`Hesperus' and `Phosphorus' have different senses, \ so here they do not co-refer", OK),
                      (r"compositionality survives; \ the price is a reference that shifts with context", GOAL),
                      (r"chapter 13 returns to belief reports, \ and to the rivals of this answer", HIST)],
                     font_size=21, aligned_edge=LEFT, width=12.0, buff=0.26).move_to([0, -1.4, 0])
        with self.voiceover(
            "The theory meets its hardest case in reports of belief. <bookmark mark='a'/>The ancients believed that "
            "Hesperus is seen in the evening: true. Swap in the co-referring name: the ancients believed that "
            "Phosphorus is seen in the evening. That is false; they believed it was seen in the morning. "
            "<bookmark mark='b'/>So inside believes that, substitution of co-referring names can change the truth "
            "value, and compositionality of reference seems to fail. <bookmark mark='c'/>Frege's answer: in such "
            "indirect contexts, words refer not to their usual referents but to their customary senses. "
            "<bookmark mark='d'/>Hesperus and Phosphorus have different senses, so in a belief report they do not "
            "co-refer, and nothing has been substituted for its equal. <bookmark mark='e'/>Compositionality "
            "survives; the price is a reference that shifts with linguistic context. <bookmark mark='f'/>Chapter "
            "thirteen comes back to belief reports and to the rivals of this answer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pair[0]))
            self.play(FadeIn(pair[1]))
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
