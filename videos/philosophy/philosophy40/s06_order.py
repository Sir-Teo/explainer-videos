from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Order(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Measuring order", r"Can a formula find beauty?", lit=(1933,), part=PART)
        with self.voiceover("Chapter five. Measuring order."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.birkhoff()
        self.images()
        self.progress()
        self.depth()
        self.information()
        self.pollock()

    def birkhoff(self):
        head = history_card(1933, r"George David Birkhoff", r"\textit{Aesthetic Measure}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the formula", r"aesthetic measure $M = O / C$: \ order divided by complexity", FORM),
                (r"order, \ for polygons", r"points for vertical symmetry, \ equilibrium, \ rotational symmetry, \ fit to a horizontal--vertical grid, \ minus faults", SYM),
                (r"complexity", r"the number of distinct straight lines containing the sides", TASTE),
                (r"the verdict", r"the square ranks first; \ Eysenck \ (1941) \ found the formula a poor predictor of people's preferences", BAD)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "In 1933 the mathematician George David Birkhoff published Aesthetic Measure, an attempt to compute "
            "beauty. <bookmark mark='a'/>His measure is order divided by complexity. <bookmark mark='b'/>For "
            "polygons, order earns points for vertical symmetry, balance, rotational symmetry and fit to a grid of "
            "horizontals and verticals, minus points for faults. <bookmark mark='c'/>Complexity counts the distinct "
            "straight lines on which the sides lie. <bookmark mark='d'/>The square comes out on top. Hans Eysenck "
            "tested the formula against people's preferences in 1941 and found it a poor predictor; he suggested that "
            "order and complexity should be multiplied, not divided. The deeper problem is that symmetry and "
            "simplicity are not all we value."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def information(self):
        head = label(r"Information aesthetics", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Bense; \ Moles", r"1950s--60s: \ measure aesthetic information with Shannon's entropy", FORM),
                (r"Berlyne \ (1971)", r"\textit{Aesthetics and Psychobiology}: \ pleasure peaks at intermediate complexity, \ an inverted U", TASTE),
                (r"the evidence", r"inverted U curves appear in some studies of music and pictures, \ but not reliably in all", BAD),
                (r"computational aesthetics", r"since 2005: \ models that predict ratings of photographs and paintings", SYM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Information theory offered new tools. <bookmark mark='a'/>In the 1950s and 1960s Max Bense and Abraham "
            "Moles tried to measure aesthetic information with Claude Shannon's entropy. <bookmark mark='b'/>The "
            "psychologist Daniel Berlyne's Aesthetics and Psychobiology, of 1971, proposed that pleasure peaks at "
            "intermediate complexity, an inverted U. <bookmark mark='c'/>Later studies found such curves in some "
            "experiments on music and pictures, but not reliably in all. <bookmark mark='d'/>Today computational "
            "aesthetics trains models to predict how people rate photographs and paintings, which predicts taste "
            "without explaining it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def images(self):
        c = {x["image"]: x["ratio"] for x in load("compress")["images"]}
        assert c == {"blank": 0.027, "stripes": 0.027, "rule 90": 0.422, "rule 30": 1.021, "noise": 1.021}
        ims = AE.images()
        head = label(r"How much can each picture be compressed?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        tiles = Group()
        for name in ["blank", "stripes", "rule 90", "rule 30", "noise"]:
            arr = (255 - ims[name] * 255).astype(np.uint8)
            rgb = np.stack([arr, arr, arr], axis=2)
            im = ImageMobject(rgb).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            im.height = 2.0
            fr = SurroundingRectangle(im, color=GREY_C, buff=0.02, stroke_width=1)
            nm = label(name, font_size=19, color=GREY_A).next_to(im, UP, buff=0.12)
            val = label(rf"{c[name] * 100:.0f}\% of raw size", font_size=18, color=SYM if c[name] < 0.5 else ART)
            val.next_to(im, DOWN, buff=0.15)
            tiles.add(Group(im, fr, nm, val))
        tiles.arrange(RIGHT, buff=0.45).move_to([0, 0.5, 0])
        foot = stack([(r"zlib finds the order in blank and striped images, \ some in rule 90, \ none in rule 30", GREY_A),
                      (r"yet rule 30 is fully determined by a rule of 8 cases: \ order depends on the observer's model",
                       GOAL)], font_size=21, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A modern way to measure order is compression: an image is orderly if a short description reproduces it. "
            "<bookmark mark='a'/>Here are five black and white pictures, sixty four cells square: a blank, stripes, "
            "two patterns grown by the cellular automata called rule 90 and rule 30 from a random first row, and pure "
            "noise. <bookmark mark='b'/>A standard compressor, zlib, shrinks the blank and the stripes to under three "
            "percent of their size, and rule 90 to forty two percent. Rule 30 and the noise do not shrink at all. "
            "<bookmark mark='c'/>Yet rule 30 is completely determined by a rule with eight cases, applied row after "
            "row. Order is not simply in the picture: it depends on what model the observer brings."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(Group(t[0], t[1], t[2])) for t in tiles], lag_ratio=0.25), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t[3]) for t in tiles], lag_ratio=0.2), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def progress(self):
        p = load("progress")
        assert p["rule 30"]["progress"] == 0.386 and p["noise"]["progress"] == 0.027
        head = label(r"Interest as compression progress \ (Schmidhuber), \ as a toy", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 12, 2], y_range=[0, 1.1, 0.25], x_length=7.0, y_length=4.0,
                  axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
                  x_axis_config={"numbers_to_include": [2, 4, 6, 8, 10, 12]},
                  y_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1.0],
                                 "decimal_number_config": {"num_decimal_places": 2}}).move_to([-2.6, -0.5, 0])
        xl = label(r"rows seen", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"bits needed per cell", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        cols = {"noise": ART, "rule 30": TASTE, "stripes": SYM, "blank": GREY_B}
        curves = VGroup()
        for name, c in cols.items():
            b = p[name]["bits_per_cell"][:12]
            curves.add(VMobject(color=c, stroke_width=3.5).set_points_as_corners(
                [ax.c2p(i + 1, v) for i, v in enumerate(b)]))
        side = stack([(r"an observer predicts each cell from the three above it, \ learning as it reads", GREY_A),
                      (rf"noise: \ about 1 bit per cell, \ for ever: \ no progress", ART),
                      (rf"blank: \ nearly free from the start: \ no progress", GREY_B),
                      (rf"rule 30: \ {p['rule 30']['first']:.2f} bits, \ then almost 0: \ the most progress", TASTE),
                      (r"interest = learnable, \ but not yet learned", GOAL)],
                     font_size=19, buff=0.26, aligned_edge=LEFT)
        for s0 in side:
            if s0.width > 5.2:
                s0.width = 5.2
        side.move_to([4.1, -0.2, 0])
        with self.voiceover(
            "Jürgen Schmidhuber proposed that what we find interesting, and beautiful, is what lets us improve our "
            "compression: the moment a pattern becomes predictable. The Reasoner builds a toy version. <bookmark "
            "mark='a'/>An observer reads each picture row by row, predicting each cell from the three cells above it "
            "and learning from every cell it sees. The curves show how many bits it needs per cell. <bookmark "
            "mark='b'/>Noise always costs about one bit per cell: nothing to learn. <bookmark mark='c'/>The blank "
            "costs almost nothing from the start: nothing left to learn. <bookmark mark='d'/>Rule 30 costs four tenths of "
            "a bit at first and then almost nothing, once the observer has found the rule: the largest progress. "
            "<bookmark mark='e'/>On this view, the interesting lies between the boring and the random: learnable, but "
            "not yet learned. It is a version of Daniel Berlyne's inverted U, in which pleasure peaks at intermediate "
            "complexity."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            for mk, i in zip("bcd", (0, 3, 1)):
                vo.wait_until(mk)
                self.play(Create(curves[i]), FadeIn(side[{0: 1, 3: 2, 1: 3}[i]]))
            self.play(Create(curves[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def pollock(self):
        head = label(r"Fractals and drips", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Taylor et al. \ (1999)", r"Pollock's drip paintings have fractal structure, \ with a dimension that rose over his career", FORM),
                (r"preference", r"people tend to prefer fractal dimensions around 1.3 to 1.5, \ as in many natural scenes", TASTE),
                (r"the critique", r"Jones-Smith and Mathur \ (2006): \ the analysis cannot reliably tell Pollocks from imitations", BAD),
                (r"the lesson", r"a statistic of a picture is not its value: \ order again needs an observer", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Fractals offered a new kind of order. <bookmark mark='a'/>Richard Taylor and colleagues reported in "
            "Nature in 1999 that Jackson Pollock's drip paintings have fractal structure, with a dimension that rose "
            "over his career. <bookmark mark='b'/>Taylor's later studies found that people tend to prefer fractal "
            "dimensions of about one point three to one point five, as in many natural scenes. <bookmark "
            "mark='c'/>But Katherine Jones-Smith and Harsh Mathur replied in 2006 that the analysis could not "
            "reliably tell Pollocks from imitations. <bookmark mark='d'/>A statistic of a picture is not its value; "
            "order, again, needs an observer."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def depth(self):
        head = label(r"Complexity, \ properly measured", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Kolmogorov \ (1965)", r"the complexity of a string is the length of its shortest program: \ uncomputable, \ as Part 7 would predict", FORM),
                (r"its flaw for beauty", r"noise has the highest complexity of all, \ and is not beautiful", BAD),
                (r"logical depth \ (Bennett, \ 1988)", r"how long the shortest program takes to run: \ shallow for noise and blanks, \ deep for organisms and artworks", SYM),
                (r"effective complexity", r"Gell-Mann and Lloyd \ (1996): \ the length of a description of the regularities alone", TASTE)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Mathematics offers better measures of complexity. <bookmark mark='a'/>Andrey Kolmogorov defined the "
            "complexity of a string, in 1965, as the length of the shortest program that prints it; by the limits of "
            "proof met in Part 7, it cannot be computed. <bookmark mark='b'/>For beauty it points the wrong way: "
            "noise is the most complex thing there is. <bookmark mark='c'/>Charles Bennett's logical depth, of 1988, "
            "measures instead how long the shortest program takes to run: shallow for noise and blanks alike, deep "
            "for things that, like organisms and artworks, could only have come from a long process. <bookmark "
            "mark='d'/>And Murray Gell-Mann and Seth Lloyd's effective complexity measures the length of a "
            "description of the regularities alone, setting the random parts aside."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
