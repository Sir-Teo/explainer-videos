from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403

FACE_COL = {"+x": OBJ, "-x": OBJ, "+y": WORLD, "-y": WORLD, "+z": ACT, "-z": ACT}


def cube(az, el, centre, scale=2.4):
    g = VGroup()
    for f, poly, shade in H.cube_profile(az, el, scale=scale):
        pts = [np.array([x, y, 0]) + np.array(centre) for x, y in poly]
        g.add(Polygon(*pts, color=WHITE, stroke_width=2, fill_color=FACE_COL[f], fill_opacity=0.25 + 0.6 * shade))
    return g


class Husserl(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"To the things themselves", r"How does a thing show itself?", lit=(1900, 1913),
                            part=PART)
        with self.voiceover("Chapter two. To the things themselves."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.reduction()
        self.noema()
        self.profiles()
        self.variation()

    def reduction(self):
        hc = history_card(1913, r"Edmund Husserl", r"\textit{Ideas I}", width=4.6, color=HIST).to_corner(UL, buff=0.3)
        beliefs = [r"the tree exists", r"it was planted years ago", r"it is made of cells", r"others see it too"]
        bl = VGroup(*[label(b, font_size=22, color=WORLD) for b in beliefs]).arrange(DOWN, buff=0.3,
                                                                                    aligned_edge=LEFT).move_to(
            [-3.2, -0.3, 0])
        brackets = VGroup(*[VGroup(MathTex(r"\big[", font_size=40, color=SIGN).next_to(b, LEFT, buff=0.08),
                                   MathTex(r"\big]", font_size=40, color=SIGN).next_to(b, RIGHT, buff=0.08))
                            for b in bl])
        left = label(r"the natural attitude: \ the world is simply there", font_size=21, color=WORLD).next_to(
            bl, UP, buff=0.4).align_to(bl, LEFT)
        appear = VGroup(*[label(x, font_size=22, color=ACT) for x in
                          [r"green, \ in blossom", r"seen from this side", r"its back side expected", r"as lovely"]]
                        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.4, -0.3, 0])
        right = label(r"what remains: \ the tree as it appears", font_size=21, color=ACT).next_to(appear, UP,
                                                                                               buff=0.4).align_to(
            appear, LEFT)
        foot = label(r"the epoch\'e: \ not doubting the world, \ but suspending the question of its existence",
                     font_size=21, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Husserl's method begins with a change of attitude. <bookmark mark='a'/>In ordinary life we are in what "
            "he called the natural attitude: the world is simply there, and we take for granted that the tree "
            "exists, that it was planted years ago, that it is made of cells, that others see it too. "
            "<bookmark mark='b'/>The phenomenologist puts all of this in brackets. Husserl called it the epoché, "
            "Greek for holding back. It is not doubt, as with Descartes: the world is not denied, only the question "
            "of its existence is set aside. <bookmark mark='c'/>What remains is the tree exactly as it appears: "
            "green and in blossom, seen from this side, with its back side expected, as lovely. The description of "
            "this, and of the acts in which it appears, is phenomenology. <bookmark mark='d'/>The reduction is not "
            "a loss of the world. It is a way of seeing, for the first time, how the world is given."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(left), LaggedStart(*[FadeIn(b) for b in bl], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in brackets], lag_ratio=0.2), bl.animate.set_opacity(0.45))
            vo.wait_until("c")
            self.play(FadeIn(right), LaggedStart(*[FadeIn(x) for x in appear], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def noema(self):
        head = label(r"Noesis and noema", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        a = VGroup(RoundedRectangle(width=3.2, height=1.0, corner_radius=0.15, color=ACT),
                   label(r"noesis: \ the act", font_size=22, color=ACT)).move_to([-4.0, 1.3, 0])
        n = VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.15, color=SIGN),
                   label(r"noema: \ the tree as perceived", font_size=22, color=SIGN)).move_to([0, 1.3, 0])
        o = VGroup(RoundedRectangle(width=3.0, height=1.0, corner_radius=0.15, color=OBJ),
                   label(r"the tree", font_size=22, color=OBJ)).move_to([4.2, 1.3, 0])
        ar = VGroup(Arrow(a.get_right(), n.get_left(), buff=0.1, color=GREY_B),
                    Arrow(n.get_right(), o.get_left(), buff=0.1, color=GREY_B))
        q = quote_card(r"The tree simpliciter can burn up, \ be resolved into its chemical elements, \ etc. \ But the "
                       r"sense \dots\ of this perception \dots\ cannot burn up.", r"Husserl", r"\textit{Ideas I}, \ "
                       r"\S 89", width=9.6, font_size=23).move_to([0, -0.6, 0])
        rows = stack([(r"Gurwitsch: \ the noema is the object itself, \ as it is perceived", OBJ),
                      (r"F{\o}llesdal \ (1969): \ the noema is a sense, \ Frege's \textit{Sinn} generalized to every "
                       r"act \ (Part 27)", SIGN)], font_size=20, aligned_edge=LEFT, width=12.0, buff=0.22).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Within experience, Husserl distinguishes two sides. <bookmark mark='a'/>The noesis is the act: this "
            "perceiving, this remembering, this imagining. <bookmark mark='b'/>The noema is what is meant, exactly "
            "as it is meant: the tree as perceived, from this side, in this light. <bookmark mark='c'/>Through the "
            "noema the act reaches the tree itself. <bookmark mark='d'/>Husserl drew the line sharply. The tree "
            "simpliciter can burn up, be resolved into its chemical elements, and so on. But the sense of this "
            "perception cannot burn up. <bookmark mark='e'/>What is a noema? Aron Gurwitsch read it as the object "
            "itself, just as it is perceived. <bookmark mark='f'/>Dagfinn Føllesdal argued in 1969 that it is a "
            "sense, Frege's notion from Part 27 generalized from words to every act of consciousness: a mode of "
            "presentation through which an act is directed at its object, if there is one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(GrowArrow(ar[0]), FadeIn(n))
            vo.wait_until("c")
            self.play(GrowArrow(ar[1]), FadeIn(o))
            vo.wait_until("d")
            self.play(FadeIn(q))
            vo.wait_until("e")
            self.play(FadeIn(rows[0]))
            vo.wait_until("f")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def profiles(self):
        d = load("adumbrations")
        head = label(r"A cube, \ never seen whole", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        c = d["counts"]
        assert d["n"] == 4000 and c == {"1": 1193, "2": 2232, "3": 575} and d["max_at_once"] == 3 and d["all_six"]
        views = [(0, 0), (45, 0), (35, 26)]
        cubes = VGroup(*[cube(az, el, [x, 1.45, 0]) for (az, el), x in zip(views, (-4.2, 0, 4.2))])
        caps = VGroup(*[label(t, font_size=19, color=GREY_A).move_to([cb.get_x(), -0.05, 0])
                        for t, cb in zip([r"one face", r"two faces", r"three faces"], cubes)])
        hd = [r"\text{faces seen at once}", r"1", r"2", r"3", r"\geq 4"]
        cells = [[label(r"of 4000 viewpoints", font_size=19, color=WHITE), MathTex(str(c["1"]), font_size=22,
                                                                                    color=OBJ),
                  MathTex(str(c["2"]), font_size=22, color=WORLD), MathTex(str(c["3"]), font_size=22, color=ACT),
                  MathTex("0", font_size=22, color=BAD)]]
        grid = ValueGrid(hd, cells, col_w=[3.4, 1.3, 1.3, 1.3, 1.3], cell_h=0.5, font_size=20).move_to([0, -1.45, 0])
        foot = stack([(r"every one of the six faces is seen from some viewpoint; \ never more than three at once", GOAL),
                      (r"the thing is given as a rule for profiles: \ the unseen sides are co-meant, \ a horizon", SIGN)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Husserl's favourite example is a perceived thing, and how it is given. <bookmark mark='a'/>A cube can be "
            "seen from straight on, showing one face; from an edge, showing two; or from a corner, showing three. "
            "<bookmark mark='b'/>The Reasoner looks at a cube from four thousand random viewpoints close around it. "
            "One face is seen from eleven hundred and ninety-three of them, two faces from two thousand two hundred "
            "and thirty-two, three from five hundred and seventy-five. Not one shows four. "
            "<bookmark mark='c'/>Yet every one of the six faces is seen from somewhere. The cube is never given "
            "all at once. Husserl's word was Abschattungen, adumbrations: a thing is given only in profiles. "
            "<bookmark mark='d'/>And still we see a cube, not a few squares. The hidden sides are meant along with "
            "the visible ones, as a horizon of what further looking would show. The thing is given as a rule for "
            "its profiles, confirmed or surprised as we move around it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in cubes], lag_ratio=0.4), FadeIn(caps))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(x) for x in grid.cell[0]])
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def variation(self):
        d = load("eidetic")
        head = label(r"Eidetic variation \ (an analogy)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = {r["property"]: r for r in d["rows"]}
        assert d["n"] == 5000
        inv = ["three sides", "angles sum to 180", "longest side faces the largest angle", "at least two acute angles",
               "each side shorter than the other two together"]
        acc = ["obtuse", "acute", "isosceles", "right-angled"]
        assert all(rows[k]["invariant"] for k in inv) and not any(rows[k]["invariant"] for k in acc)
        assert rows["obtuse"]["share"] == 0.734 and rows["acute"]["share"] == 0.266
        tri_pts = [[(-5.9, -1.6), (-3.6, -1.9), (-4.3, 0.9)], [(-6.2, -2.0), (-3.2, -1.3), (-5.6, -0.4)],
                   [(-5.4, -2.1), (-4.6, -1.8), (-3.4, 0.6)], [(-6.1, -1.0), (-3.5, -2.2), (-4.9, 0.4)]]
        tris = [Polygon(*[np.array([x, y, 0]) for x, y in t], color=SIGN, stroke_width=3, fill_opacity=0.15,
                        fill_color=SIGN) for t in tri_pts]
        hd = [r"\text{property}", r"\text{share of 5000}"]
        cells = []
        for k in inv + acc:
            r = rows[k]
            col = OK if r["invariant"] else GREY_A
            cells.append([label(k.replace("180", r"180$^\circ$"), font_size=17, color=col),
                          MathTex(rf"{100 * r['share']:.1f}\%", font_size=20, color=col)])
        grid = ValueGrid(hd, cells, col_w=[5.2, 1.8], cell_h=0.4, font_size=18).move_to([2.6, 0.3, 0])
        foot = stack([(r"invariant under every variation: \ candidates for the essence; \ the rest are accidents", OK),
                      (r"Husserl varies in imagination and claims to see necessity; \ sampling only finds "
                       r"candidates, \ each needing a proof", BAD)], font_size=19, aligned_edge=LEFT, width=12.0,
                     buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Husserl also wanted the essences of things: what makes a triangle a triangle, or a perception a "
            "perception. His method was free variation. <bookmark mark='a'/>Imagine a triangle, and vary it freely: "
            "stretch it, flatten it, tilt it. <bookmark mark='b'/>Some features survive every variation. In five "
            "thousand random triangles the Reasoner finds five that hold in every one: three sides, angles summing "
            "to a hundred and eighty degrees, the longest side facing the largest angle, at least two acute angles, "
            "and each side shorter than the other two together. <bookmark mark='c'/>Others come and go. Seventy-three "
            "percent are obtuse and twenty-seven acute; isosceles and right-angled triangles are rare accidents. "
            "What survives every variation is a candidate for the essence, the eidos. <bookmark mark='d'/>This is "
            "only an analogy. Husserl's variation runs in imagination, and he claimed it lets us see necessity "
            "directly. Sampling can only find candidates. Each needs a proof: for instance, two angles of ninety "
            "degrees or more would already add up to a hundred and eighty, so at least two angles must be acute."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(tris[0]))
            for t in tris[1:]:
                self.play(Transform(tris[0], t), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(inv)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            vo.wait_until("c")
            for r in range(len(inv), len(cells)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
