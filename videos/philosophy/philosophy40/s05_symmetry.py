from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Symmetry(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Seventeen ways to tile a plane", r"How much order can a pattern have?", lit=(1891,), part=PART)
        with self.voiceover("Chapter four. Seventeen ways to tile a plane."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.gallery()
        self.classify()
        self.elements()
        self.quasi()
        self.history()
        self.broken()

    def history(self):
        head = label(r"Symmetry in art and science", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the Alhambra", r"fourteenth-century tilings in Granada; \ Grünbaum \ (2006) \ counted 13 of the 17 groups there", EAST),
                (r"Escher", r"studied the Alhambra in 1936, \ and filled the plane with birds, \ fish and lizards", ART),
                (r"Weyl \ (1952)", r"\textit{Symmetry}: \ the idea that runs from ornament to crystals to physical law", FORM),
                (r"Conway \ (2008)", r"\textit{The Symmetries of Things}: \ the orbifold notation, \ and a proof of seventeen by counting", SYM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Symmetry joins art and science. <bookmark mark='a'/>The fourteenth-century tilings of the Alhambra in "
            "Granada are often said to contain all seventeen groups; Branko Grünbaum's careful count of 2006 found "
            "thirteen. <bookmark mark='b'/>Maurits Escher studied them in 1936 and spent his life filling the plane "
            "with birds, fish and lizards. <bookmark mark='c'/>Hermann Weyl's Symmetry, of 1952, traced the idea from "
            "ornament to crystals to the laws of physics. <bookmark mark='d'/>And John Conway, Heidi Burgiel and "
            "Chaim Goodman-Strauss's The Symmetries of Things, of 2008, proved that there are seventeen by a simple "
            "count of the costs of the symbols in the orbifold notation. Symmetry is the strongest case for beauty as "
            "order; whether it is enough is the next chapter's question."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    ORDER = ["p1", "p2", "pm", "pg", "cm", "pmm", "pmg", "pgg", "cmm", "p4", "p4m", "p4g", "p3", "p3m1", "p31m", "p6",
             "p6m"]

    def thumb(self, g, size=1.3, window=(-0.2, 1.8)):
        p = load("patterns")[g]
        lo, hi = window
        sc = size / (hi - lo)
        grp = VGroup()
        for poly, fl in zip(p["polys"], p["flip"]):
            c = np.mean(poly, axis=0)
            if lo <= c[0] <= hi and lo <= c[1] <= hi:
                pts = [np.array([(x - (lo + hi) / 2) * sc, (y - (lo + hi) / 2) * sc, 0]) for x, y in poly]
                grp.add(Polygon(*pts, stroke_width=0.6, stroke_color=WHITE, fill_color=ART if fl else SYM,
                                fill_opacity=0.75))
        frame = Square(side_length=size + 0.08, stroke_color=GREY_C, stroke_width=1)
        return VGroup(frame, grp)

    def gallery(self):
        w = load("wallpaper")
        assert w["distinct"] == 17 and w["all_seventeen"]
        orb = {o["name"]: o["orbifold"].replace("\u00d7", r"$\times$") for o in w["groups"]}
        head = label(r"The seventeen wallpaper groups, \ generated", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        tiles = VGroup()
        for i, g in enumerate(self.ORDER):
            t = self.thumb(g)
            nm = label(rf"{g} \ \ {orb[g]}", font_size=16, color=GREY_A).next_to(t, DOWN, buff=0.08)
            tiles.add(VGroup(t, nm))
        rows = [tiles[0:6], tiles[6:12], tiles[12:17]]
        for k, r in enumerate(rows):
            VGroup(*r).arrange(RIGHT, buff=0.42).move_to([0, 1.55 - k * 2.05, 0])
        legend = label(r"teal: \ copies of the motif by rotation or translation; \ pink: \ by reflection or glide",
                       font_size=18, color=GREY_A).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "A wallpaper pattern repeats in two independent directions. Its symmetry group is every rigid motion of "
            "the plane that leaves the pattern unchanged. <bookmark mark='a'/>The Reasoner builds each group from its "
            "list of symmetry operations, and copies one small asymmetric motif by every one of them. In teal, the "
            "copies made by rotations and translations; in pink, the mirror images made by reflections and glides. "
            "<bookmark mark='b'/>First, the groups with no rotations, or only half turns. <bookmark mark='c'/>Then "
            "those with quarter turns, and those with thirds and sixths of a turn. <bookmark mark='d'/>There are "
            "exactly seventeen. Evgraf Fedorov proved it in 1891, and George Pólya found them again in 1924. Under "
            "each pattern are its name in the crystallographers' notation, and in the orbifold notation of John "
            "Conway, where a star marks a mirror and a cross marks a glide."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tiles[0]), FadeIn(legend))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in tiles[1:9]], lag_ratio=0.2), run_time=3)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t) for t in tiles[9:]], lag_ratio=0.2), run_time=3)
            vo.wait_until("d")
            self.play(Indicate(tiles, color=GOAL, scale_factor=1.02))
        self.clear_scene()

    def classify(self):
        w = load("wallpaper")
        by = {o["name"]: o for o in w["groups"]}
        head = label(r"Naming a pattern by its symmetries", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        steps = stack([(r"1. \ the smallest rotation: \ a half, \ third, \ quarter or sixth of a turn, \ or none", SYM),
                       (r"2. \ are there mirrors? \ in how many directions?", ART),
                       (r"3. \ are there glides on axes that are not mirrors?", TASTE),
                       (r"4. \ do the rotation centres lie on mirrors?", FORM)],
                      font_size=21, buff=0.25, aligned_edge=LEFT).move_to([-3.2, 1.4, 0])
        for s0 in steps:
            if s0.width > 6.4:
                s0.width = 6.4
        steps.move_to([-3.2, 1.4, 0])
        hd = [r"\text{built as}", r"\text{turn}", r"\text{mirror dirs}", r"\text{glide}", r"\text{named}"]
        show = ["pm", "cm", "pmg", "cmm", "p4m", "p4g", "p3m1", "p31m"]
        cells = []
        for g in show:
            o = by[g]
            cells.append([label(o["built_as"], font_size=16, color=GREY_A), label(str(o["rotation"]), font_size=17),
                          label(str(o["mirror_directions"]), font_size=17), mark(o["essential_glide"], 18),
                          label(g, font_size=18, color=GOAL)])
        grid = ValueGrid(hd, cells, col_w=[2.3, 0.9, 1.6, 1.0, 1.2], cell_h=0.38, font_size=15).move_to([3.4, 0.2, 0])
        foot = label(r"all 17 built groups receive 17 different names: \ the classifier finds every group, \ once",
                     font_size=21, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How can you tell which group a pattern has? The Reasoner uses the flowchart that crystallographers "
            "teach. <bookmark mark='a'/>First find the smallest rotation that maps the pattern to itself. <bookmark "
            "mark='b'/>Then look for mirrors, and count their directions. <bookmark mark='c'/>Then look for glide "
            "reflections whose axes are not mirrors. <bookmark mark='d'/>Then ask whether the rotation centres lie on "
            "mirrors. For each built group, the classifier works these out from the group's own operations, without "
            "being told the answer. Two groups with three-fold turns and mirrors are built the same way, and only the "
            "last question tells them apart. <bookmark mark='e'/>All seventeen receive different names: the "
            "classifier finds every group, exactly once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, i in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(steps[i], shift=RIGHT * 0.2))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in grid.cell], lag_ratio=0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def elements(self):
        e = load("elements")
        assert e["group"] == "p4m" and sum(c["order"] == 4 for c in e["centres"]) == 8
        head = label(r"The symmetries of one pattern: \ p4m \ (\textasteriskcentered 442)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        p = load("patterns")["p4m"]
        lo, hi = -0.2, 1.8
        sc = 5.6 / (hi - lo)
        off = np.array([-2.6, -0.5, 0])

        def P(x, y):
            return off + np.array([(x - (lo + hi) / 2) * sc, (y - (lo + hi) / 2) * sc, 0])

        tiles = VGroup()
        for poly, fl in zip(p["polys"], p["flip"]):
            c = np.mean(poly, axis=0)
            if lo <= c[0] <= hi and lo <= c[1] <= hi:
                tiles.add(Polygon(*[P(x, y) for x, y in poly], stroke_width=0.8, stroke_color=WHITE,
                                  fill_color=ART if fl else SYM, fill_opacity=0.6))
        frame = Square(side_length=5.7, stroke_color=GREY_C, stroke_width=1).move_to(off)
        mir = VGroup(*[Line(P(*a), P(*b), color=TASTE, stroke_width=3) for a, b in e["mirrors"]])
        gl = VGroup(*[DashedLine(P(*a), P(*b), color=FORM, stroke_width=2.5, dash_length=0.12) for a, b in e["glides"]])
        cen = VGroup()
        for c in e["centres"]:
            if c["order"] == 4:
                cen.add(Square(side_length=0.22, color=BAD, fill_opacity=1).rotate(PI / 4).move_to(P(*c["at"])))
            else:
                cen.add(Ellipse(width=0.24, height=0.14, color=GOAL, fill_opacity=1).move_to(P(*c["at"])))
        side = stack([(r"solid: \ mirror lines", TASTE), (r"dashed: \ glide axes that are not mirrors", FORM),
                      (r"diamonds: \ quarter-turn centres", BAD), (r"ovals: \ half-turn centres", GOAL),
                      (r"all found by the Reasoner from the group's operations", GREY_A)],
                     font_size=21, buff=0.3, aligned_edge=LEFT).move_to([4.0, -0.4, 0])
        with self.voiceover(
            "Here is one pattern with its symmetries drawn in, all computed from the group's operations. <bookmark "
            "mark='a'/>The pattern belongs to the group p4m, the symmetry of a square tiled floor. <bookmark "
            "mark='b'/>Its mirror lines run horizontally, vertically and diagonally. <bookmark mark='c'/>Between the "
            "diagonal mirrors run glide axes: reflect, then slide. <bookmark mark='d'/>Quarter turns about the "
            "corners and centres of the squares map it to itself, and half turns about the midpoints of the edges. "
            "Every one of these was found by the Reasoner, not drawn by hand."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tiles))
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            self.play(Create(mir), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(gl), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(cen), FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def quasi(self):
        head = label(r"Beyond periodic order", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"in three dimensions", r"230 space groups \ (Fedorov; \ Schoenflies, \ 1891): \ the symmetries of crystals", SYM),
                (r"Penrose \ (1974)", r"tiles that cover the plane with five-fold symmetry, \ but never periodically", FORM),
                (r"Shechtman \ (1982)", r"an alloy whose diffraction showed five-fold symmetry: \ quasicrystals; \ Nobel prize 2011", TASTE),
                (r"girih \ (Lu and Steinhardt, \ 2007)", r"fifteenth-century Islamic tilings that are nearly Penrose patterns", EAST)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Order need not be periodic. <bookmark mark='a'/>In three dimensions there are two hundred and thirty "
            "space groups, found by Fedorov and Arthur Schoenflies in 1891: the possible symmetries of crystals. "
            "<bookmark mark='b'/>In 1974 Roger Penrose found tiles that cover the plane with five-fold symmetry but "
            "never repeat. <bookmark mark='c'/>In 1982 Dan Shechtman found an alloy whose diffraction pattern had "
            "five-fold symmetry, which crystallography said was impossible: quasicrystals, for which he won the Nobel "
            "prize in chemistry in 2011. <bookmark mark='d'/>And Peter Lu and Paul Steinhardt showed in 2007 that "
            "fifteenth-century Islamic girih tilings, on the Darb-i Imam shrine in Isfahan, are nearly perfect "
            "quasi-periodic patterns."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def broken(self):
        head = label(r"Too much symmetry?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Gombrich \ (1979)", r"\textit{The Sense of Order}: \ we enjoy order, \ and the small breaks in it that hold attention", TASTE),
                (r"Japanese design", r"asymmetry deliberately preferred, \ as in the stones of a Zen garden", EAST),
                (r"physics", r"symmetry breaking: \ the universe's structure comes from symmetries lost", FORM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Is more symmetry always more beautiful? <bookmark mark='a'/>Ernst Gombrich's The Sense of Order, of "
            "1979, argued that we enjoy order, and the small breaks in it that hold attention; perfect repetition "
            "soon bores. <bookmark mark='b'/>Japanese design often prefers asymmetry deliberately, as in the "
            "arrangement of stones in a Zen garden. <bookmark mark='c'/>And in physics, the structure of the world, "
            "from crystals to the masses of particles, comes from symmetries that were broken. Beauty may lie between "
            "order and its breaking, as Berlyne's inverted U suggests."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
