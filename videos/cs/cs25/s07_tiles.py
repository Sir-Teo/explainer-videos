from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (fit_right, BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, wang, wang_grid,
                                   words)


class Tiles(VoiceoverScene):
    def construct(self):
        self.card()
        self.wang_()
        self.computing()
        self.hat()

    def card(self):
        card = chapter_card(6, r"Tiling the plane", r"Can a finite set of tiles hide a computer?", lit=(1961, 2023),
                            extra=((1961, r"Wang"), (1966, r"Berger"), (2023, r"the hat")), part=PART)
        with self.voiceover("Chapter six. Tiling the plane."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def wang_(self):
        t = load("tiles")
        head = label(r"Wang tiles", font_size=34).to_edge(UP, buff=0.3)
        tiles = VGroup(*[VGroup(wang(tt, 0.55), mono(str(i), 14, GREY_B)) for i, tt in enumerate(t["tiles"])])
        for g in tiles:
            g[1].next_to(g[0], DOWN, buff=0.06)
        tiles.arrange(RIGHT, buff=0.12).next_to(head, DOWN, buff=0.35)
        g12 = next(r for r in t["rects"] if r["n"] == 12)["grid"]
        grid = wang_grid(t["tiles"], g12, s=0.26).next_to(tiles, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        rows = [[f"{r['n']} $\\times$ {r['n']}", words(r["nodes"]), f"{r['seconds']:.1f} s"] for r in t["rects"]]
        tab = grid_table([r"square", r"tiles tried", r"time"], rows, widths=[1.8, 2.2, 1.4], row_h=0.36, font_size=19,
                         mono_cols=(), colors=[[WHITE, DATA, GREY_A]] * len(rows))
        tab.next_to(grid, RIGHT, buff=0.6).align_to(grid, UP)
        notes = VGroup(
            label(r"rules: \ no rotations; \ touching edges must match in colour", font_size=20, color=WHITE),
            label(rf"periodic tilings would show up on a torus: \\ all {t['refuted']} tori up to $8 \times 8$ "
                  r"(two left open) \ refuted by exhaustive search", font_size=20, color=NO),
            label(r"Jeandel and Rao \ (2015): \ these 11 tiles tile the plane, \ but \textbf{only aperiodically}; \ "
                  r"and no smaller set does", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tab, DOWN, buff=0.35).align_to(tab, LEFT)
        fit_right(notes)
        with self.voiceover(
            "In 1961 Hao Wang asked a question about square tiles with coloured edges. <bookmark mark='a'/> You may "
            "not rotate them, and wherever two tiles touch, the edge colours must agree. Given a finite set, can "
            "copies of it cover the whole plane? <bookmark mark='b'/> For these eleven, a backtracking search finds "
            "squares easily: twelve by twelve in forty-five thousand tries, twenty by twenty in four million. "
            "<bookmark mark='c'/> Wang conjectured that any set that tiles the plane can also tile it periodically, "
            "with a pattern that repeats. A periodic tiling folds up onto a torus, so we searched every small torus. "
            "Every one we could finish was impossible. <bookmark mark='d'/> That is because these are Emmanuel "
            "Jeandel and Michael Rao's eleven tiles from 2015: they tile the plane, but never periodically, and they "
            "proved no smaller set can do that."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(x) for x in tiles], lag_ratio=0.08))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in grid], lag_ratio=0.003), FadeIn(VGroup(*tab.cells[0])),
                      FadeIn(tab.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def computing(self):
        head = label(r"Why tiling is undecidable", font_size=34).to_edge(UP, buff=0.35)
        rows_ = ["#q10#", "#1p0#", "#10a#"]
        cw = 0.55
        grid = VGroup()
        for r, s in enumerate(rows_):
            for c, ch in enumerate(s):
                sq = Square(side_length=cw, stroke_color=GREY_B, stroke_width=1.2).move_to(
                    [-5.4 + c * cw, 1.4 - r * cw, 0])
                if ch in "qpa":
                    sq.set_fill(HEAD, 0.45)
                grid.add(VGroup(sq, mono(ch, 20, WHITE).move_to(sq)))
        gl = label(r"row $t$ = the tape at time $t$", font_size=19, color=GREY_A).next_to(grid, DOWN, buff=0.15)
        lines = VGroup(
            label(r"make one tile per (symbol, state) cell of a Turing machine's tableau:", font_size=21, color=WHITE),
            label(r"the colours on each tile's top and bottom force the next row \\ to be the machine's next step",
                  font_size=21, color=DATA),
            label(r"so the tiles fill the plane $\iff$ the machine \textbf{runs forever}", font_size=21, color=NO),
            label(r"Berger \ (1966): \ tiling is undecidable; \ his proof needed an \textbf{aperiodic} set: \ 20,426 "
                  r"tiles", font_size=21, color=HEAD),
            label(r"then Robinson \ (1971), \ Penrose \ (1974, \ two shapes), \ Kari and Culik \ (13), \ "
                  r"Jeandel--Rao \ (11)", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(grid, RIGHT, buff=0.6).align_to(grid, UP)
        fit_right(lines)
        with self.voiceover(
            "Why should tiles be hard? <bookmark mark='a'/> Write a Turing machine's run as a table, one row per "
            "step, each row the tape at that moment, with the state marked on the head's cell. Make a tile for each "
            "kind of cell. <bookmark mark='b'/> Choose the edge colours so that a row of tiles can only be followed "
            "by the row that is the machine's next step. <bookmark mark='c'/> Then the tiles can fill the plane "
            "exactly when the machine runs forever, and deciding tiling would decide halting. <bookmark mark='d'/> "
            "Robert Berger proved this in 1966. The hard part was forcing the computation to happen everywhere at "
            "every scale, which needed a set that tiles only aperiodically. His had twenty thousand four hundred and "
            "twenty-six tiles. <bookmark mark='e'/> Raphael Robinson brought it to six shapes, Roger Penrose to two, "
            "Jarkko Kari and Karel Culik to thirteen Wang tiles, and Jeandel and Rao to eleven."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(gl))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def hat(self):
        h = load("hat")
        P = np.array(h["P"])
        head = label(r"2023: \ one tile, \ the hat", font_size=34).to_edge(UP, buff=0.35)
        sc = 0.62
        poly = Polygon(*[np.array([x * sc, y * sc, 0]) for x, y in P], color=HEAD, stroke_width=3).set_fill(HEAD, 0.35)
        poly.move_to(LEFT * 4.2 + DOWN * 0.2)
        lines = VGroup(
            label(r"Smith, \ Myers, \ Kaplan and Goodman-Strauss \ (2023): \\ a single shape that tiles the "
                  r"plane, \ and only aperiodically", font_size=21, color=HEAD),
            label(rf"13 vertices, \ 8 kites of the hexagonal grid: \\ area {h['area']:.3f} \ $= 8\sqrt3$",
                  font_size=21, color=WHITE),
            label(r"it needs its mirror image too; \\ the ``spectre'' \ (May 2023) \ does without", font_size=21,
                  color=LAM),
            label(r"David Smith, \ a retired print technician, \\ found it by hand, \ playing with shapes",
                  font_size=21, color=GREY_A),
            label(r"the einstein problem, \ open since Berger: \\ one stone, \ no period", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(poly, RIGHT, buff=0.8)
        fit_right(lines)
        with self.voiceover(
            "The sequence ended in 2023, with an amateur. <bookmark mark='a'/> David Smith, a retired print technician "
            "who played with shapes, found a single tile that covers the plane, but only aperiodically. With Joseph "
            "Myers, Craig Kaplan and Chaim Goodman-Strauss he proved it. <bookmark mark='b'/> It is called the hat: "
            "thirteen vertices, eight kites cut from a hexagonal grid. <bookmark mark='c'/> The hat needs reflected "
            "copies as well; two months later the same team found the spectre, which does not. <bookmark mark='d'/> "
            "It answered the einstein problem, German for one stone, which had been open since Berger's aperiodic "
            "sets. <bookmark mark='e'/> And it is still true that no algorithm can tell, for an arbitrary finite set "
            "of tiles, whether it covers the plane."
        ) as vo:
            self.play(FadeIn(head), DrawBorderThenFill(poly), run_time=2.0)
            for mk, ln in zip("abcde", [lines[0], lines[1], lines[2], lines[4], lines[3]]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
