from __future__ import annotations

import textwrap
from pathlib import Path

import numpy as np

from manim import Text as Glyphs

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

ROOT = Path(__file__).resolve().parents[3]


def _inside(points: np.ndarray, x: float, y: float) -> bool:
    """Even-odd test of (x, y) against a glyph's cubic outline, flattened to short edges."""
    t = np.linspace(0, 1, 9)
    crossings = 0
    for k in range(0, len(points) - 3, 4):
        p0, p1, p2, p3 = points[k:k + 4, :2]
        c = ((1 - t) ** 3)[:, None] * p0 + (3 * (1 - t) ** 2 * t)[:, None] * p1 + \
            (3 * (1 - t) * t ** 2)[:, None] * p2 + (t ** 3)[:, None] * p3
        for (xa, ya), (xb, yb) in zip(c[:-1], c[1:]):
            if (ya > y) != (yb > y) and x < xa + (y - ya) * (xb - xa) / (yb - ya):
                crossings += 1
    return crossings % 2 == 1


def _pixel_row(cover, x0, y, cell=0.42, color=WHITE, rows=3):
    """A strip of pixels (``rows`` tall) whose columns glow with the given coverage, 0 to 1."""
    g = VGroup()
    for r in range(rows):
        for i, c in enumerate(cover):
            g.add(Square(cell, stroke_color=GREY_D, stroke_width=1, fill_color=color, fill_opacity=0.92 * c)
                  .move_to([x0 + (i + 0.5) * cell, y - r * cell, 0]))
    return g


class Text(VoiceoverScene):
    def construct(self):
        self.card()
        self.outlines()
        self.raster()
        self.hinting()
        self.subpixel()
        self.readability()

    def card(self):
        card = chapter_card(5, r"Text on screens", r"How does a curve become letters people can read?",
                            lit=(1991, 2001), extra=((1991, r"TrueType"), (2001, r"ClearType in Windows XP")),
                            part=PART)
        with self.voiceover("Chapter five. Text on screens."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def outlines(self):
        head = label(r"A letter is a curve", font_size=36).to_edge(UP, buff=0.3)
        word = Glyphs("Job", font="DejaVu Serif", font_size=200).move_to([-3.4, 0.1, 0])
        word.set_fill(opacity=0).set_stroke(WHITE, 2.5)
        anchors, handles = VGroup(), VGroup()
        for g in word:
            P = g.points
            for k in range(0, len(P) - 3, 4):
                p0, p1, p2, p3 = P[k:k + 4]
                anchors.add(Dot(p0, radius=0.04, color=DATA))
                chord = p3 - p0
                n = np.linalg.norm(chord)
                off = [abs(chord[0] * (q - p0)[1] - chord[1] * (q - p0)[0]) for q in (p1, p2)]
                bent = n > 1e-6 and max(off) / n > 0.02
                if bent:      # straight pieces have their handles on the line: show only the curved ones
                    handles.add(Line(p0, p1, color=HEAD, stroke_width=1), Line(p3, p2, color=HEAD, stroke_width=1),
                                Dot(p1, radius=0.03, color=HEAD), Dot(p2, radius=0.03, color=HEAD))
        # a coarse pixel grid over the word; a pixel is on when its centre lies inside the outline
        cell = 0.24
        x0, x1 = word.get_left()[0] - 0.1, word.get_right()[0] + 0.1
        y0, y1 = word.get_bottom()[1] - 0.1, word.get_top()[1] + 0.1
        nx, ny = int((x1 - x0) / cell) + 1, int((y1 - y0) / cell) + 1
        grid, lit = VGroup(), VGroup()
        for i in range(nx):
            for j in range(ny):
                cx, cy = x0 + (i + 0.5) * cell, y0 + (j + 0.5) * cell
                sq = Square(cell, stroke_color=GREY_D, stroke_width=0.8).move_to([cx, cy, 0])
                grid.add(sq)
                if any(_inside(g.points, cx, cy) for g in word):
                    lit.add(Square(cell, stroke_width=0, fill_color=YES, fill_opacity=0.55).move_to([cx, cy, 0]))
        notes = VGroup(
            wrapped_label(r"a font stores each letter as an \textbf{outline}: \ closed paths of B\'ezier curves, \ "
                          r"pinned by anchor points \ (blue) \ on the curve and pulled by control points \ "
                          r"(yellow) \ off it", 5.6, font_size=20, color=WHITE),
            wrapped_label(r"TrueType \ (Apple, \ 1991) \ uses quadratic curves, \ PostScript and OpenType CFF "
                          r"cubic ones; \ either scales to any size", 5.6, font_size=20, color=GREY_A),
            wrapped_label(r"to draw it, \ ask of each pixel: \ is its centre inside? \ \ Count the outline's "
                          r"crossings of a ray from the centre, \ each decided by Part 22's orientation test; \ "
                          r"Part 51 rasterizes triangles the same way", 5.6, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.1, 0])
        cap = label(r"DejaVu Serif, \ as Manim stores it: \ cubic curves", font_size=17, color=GREY_B).next_to(
            word, DOWN, buff=0.45)
        with self.voiceover(
            "A letter on a screen begins as a shape, not as pixels. <bookmark mark='a'/> A font stores each glyph as "
            "an outline: closed paths of Bézier curves, pinned by anchor points on the curve and pulled towards "
            "control points off it. <bookmark mark='b'/> TrueType, released by Apple in 1991, uses quadratic curves; "
            "PostScript fonts use cubic ones. Either way, one outline serves every size. <bookmark mark='c'/> To draw "
            "it, lay the pixel grid over the outline and ask whether each pixel's centre is inside: count how often a "
            "ray from the centre crosses the outline, using Part 22's orientation test. An odd count means inside. "
            "Part 51 will rasterize triangles the same way."
        ) as vo:
            self.play(FadeIn(head), Create(word), FadeIn(cap), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(anchors), FadeIn(handles), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeOut(handles), FadeOut(anchors), FadeIn(grid), FadeIn(notes[2]))
            self.play(LaggedStart(*[FadeIn(s) for s in lit], lag_ratio=0.01), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def raster(self):
        g = load("glyph")
        rows = {(r["px"], r["mode"]): r for r in g["rows"]}
        sizes = sorted({r["px"] for r in g["rows"]})
        head = label(r"\texttt{Job}, \ rasterized by FreeType", font_size=36).to_edge(UP, buff=0.3)
        h = 1.3
        cols = []
        for px in sizes:
            cells = Group(label(rf"{px} px", font_size=21, color=HEAD))
            for mode, color in (("mono", NO), ("antialiased", YES)):
                r = rows[(px, mode)]
                img = ImageMobject(str(ROOT / r["png"]))
                img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
                img.stretch_to_fit_height(h)
                img.stretch_to_fit_width(h * r["w"] / r["h"])
                frame = SurroundingRectangle(img, buff=0.0, color=GREY_D, stroke_width=1.2)
                lv = label(rf"{r['w']} $\times$ {r['h']} pixels, \ {r['grey_levels']} levels", font_size=17,
                           color=color)
                cells.add(Group(img, frame, lv.next_to(img, DOWN, buff=0.1)))
            cells.arrange(DOWN, buff=0.22)
            cols.append(cells)
        cols = Group(*cols).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).next_to(head, DOWN, buff=0.35).shift(
            RIGHT * 0.6)
        names = VGroup(label(r"one bit \\ per pixel", font_size=19, color=NO),
                       label(r"grey \\ levels", font_size=19, color=YES))
        names[0].next_to(cols[0][1][0], LEFT, buff=0.3)
        names[1].next_to(cols[0][2][0], LEFT, buff=0.3)
        lines = VGroup(
            wrapped_label(r"each picture enlarged so its pixels show; \ DejaVu Serif, \ drawn by FreeType through "
                          r"Python's imaging library", 12.4, font_size=19, color=GREY_A),
            wrapped_label(r"\textbf{antialiasing}: \ a pixel's grey is the share of it the outline covers, \ so an "
                          r"edge that falls a third of the way across a pixel still shows where it is", 12.4,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        lo, hi = rows[(sizes[0], "antialiased")], rows[(sizes[-1], "antialiased")]
        with self.voiceover(
            "Here is the word Job, drawn by FreeType, the open-source rasterizer, at four sizes. "
            f"<bookmark mark='a'/> With one bit per pixel, each pixel is on or off. At {sizes[0]} pixels the whole "
            f"word gets {lo['w']} by {lo['h']} of them, and the curves turn into staircases. <bookmark mark='b'/> "
            "Antialiasing lets a pixel be partly on: its grey is the share of it the outline covers, so an edge a "
            "third of the way across a pixel still shows where it is. <bookmark mark='c'/> The small word uses "
            f"{lo['grey_levels']} levels of grey, the large one {hi['grey_levels']}. At eight pixels a stroke is "
            "about one pixel wide, and where it lands matters."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(c[0]) for c in cols], FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(*[FadeIn(c[1]) for c in cols], FadeIn(names[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(c[2][:2]) for c in cols], FadeIn(names[1]), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(c[2][2]) for c in cols])
        self.wait(0.4)
        self.clear_scene()

    def hinting(self):
        head = label(r"Hinting: \ fitting outlines to the grid", font_size=36).to_edge(UP, buff=0.3)
        width, starts, n = 1.4, (1.3, 4.0, 6.7), 10          # three equal stems, an illustrative 10-pixel row
        cell = 0.5

        def coverage(stems):
            return [sum(max(0.0, min(i + 1, s + w) - max(i, s)) for s, w in stems) for i in range(n)]
        raw = [(s, width) for s in starts]
        snapped = [(float(round(s)), float(round(width))) for s in starts]

        def panel(stems, title, color, y):
            strip = _pixel_row(coverage(stems), -5.9, y, cell=cell)
            outl = VGroup(*[Rectangle(width=w * cell, height=3 * cell, stroke_color=color, stroke_width=2.5)
                            .move_to([-5.9 + (s + w / 2) * cell, y - cell, 0]) for s, w in stems])
            t = label(title, font_size=20, color=color).next_to(strip, UP, buff=0.12).align_to(strip, LEFT)
            vals = VGroup(*[label(f"{c:.1f}", font_size=16, color=GREY_B).move_to(
                [-5.9 + (i + 0.5) * cell, y - 2.75 * cell, 0]) for i, c in enumerate(coverage(stems))])
            return VGroup(strip, outl, t, vals)
        top = panel(raw, r"as drawn: \ three stems 1.4 pixels wide", NO, 1.85)
        bot = panel(snapped, r"hinted: \ each snapped to whole pixels", YES, -0.75)
        ill = note(r"illustrative \ (coverage shown under each pixel)", font_size=16).next_to(bot, DOWN, buff=0.15
                                                                                          ).align_to(bot, LEFT)
        notes = VGroup(
            wrapped_label(r"the same stem looks sharp, \ smeared or lopsided depending on where it falls", 5.6,
                          font_size=20, color=NO),
            wrapped_label(r"TrueType fonts carry \textbf{hinting} programs, \ bytecode for a small stack machine "
                          r"in the rasterizer, \ that move outline points onto pixel boundaries at each size; \ "
                          r"FreeType can also hint automatically", 5.6, font_size=20, color=WHITE),
            wrapped_label(r"it matters most where it is hardest: \ at 8 to 12 pixels a stem is one pixel, \ and a "
                          r"tenth of a pixel moves it; \ on dense screens it matters less", 5.6, font_size=20,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.7, 0.2, 0])
        with self.voiceover(
            "Coverage alone does not make small text sharp. <bookmark mark='a'/> Here are three identical stems, "
            "like the legs of an m, each one and four tenths of a pixel wide. One becomes a grey smear across two "
            "pixels, one is solid on one side, one spreads over three. Equal strokes look unequal. "
            "<bookmark mark='b'/> Hinting fixes this. A TrueType font carries small programs, bytecode for a stack "
            "machine inside the rasterizer, that move the outline's points onto pixel boundaries at each size, so "
            "every stem comes out one crisp pixel wide. <bookmark mark='c'/> It matters most at eight to twelve "
            "pixels, where a stroke is a single pixel, and much less on dense screens."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top[0]), Create(top[1]), FadeIn(top[2]), FadeIn(top[3]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(TransformFromCopy(top[1], bot[1]), FadeIn(bot[0]), FadeIn(bot[2]), FadeIn(bot[3]),
                      FadeIn(ill), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def subpixel(self):
        head = label(r"Subpixel rendering", font_size=36).to_edge(UP, buff=0.3)
        cell, n, x0 = 0.9, 5, -6.0
        stem = (1 + 1 / 3, 1.0)                        # a one-pixel stem starting a third of the way into pixel 1
        rgb = ("#FF3B30", "#34C759", "#2F7BFF")

        def lcd(y, sub):
            g = VGroup()
            for i in range(n):
                for k in range(3):
                    a, b = i + k / 3, i + (k + 1) / 3
                    cov = max(0.0, min(b, stem[0] + stem[1]) - max(a, stem[0])) * 3
                    if not sub:      # whole-pixel antialiasing: all three stripes share the pixel's coverage
                        cov = max(0.0, min(i + 1, stem[0] + stem[1]) - max(i, stem[0]))
                    g.add(Rectangle(width=cell / 3, height=cell * 1.6, stroke_width=0, fill_color=rgb[k],
                                    fill_opacity=0.12 + 0.85 * cov).move_to([x0 + (i + (k + 0.5) / 3) * cell, y, 0]))
                g.add(Rectangle(width=cell, height=cell * 1.6, stroke_color=GREY_C, stroke_width=1.5).move_to(
                    [x0 + (i + 0.5) * cell, y, 0]))
            return g
        whole = lcd(1.3, False)
        sub = lcd(-1.1, True)
        outl = VGroup(*[Rectangle(width=stem[1] * cell, height=cell * 1.8, stroke_color=WHITE, stroke_width=2.5)
                        .move_to([x0 + (stem[0] + stem[1] / 2) * cell, y, 0]) for y in (1.3, -1.1)])
        t1 = label(r"whole pixels: \ two dim greys \ (equal stripes)", font_size=20, color=NO).next_to(
            whole, UP, buff=0.15).align_to(whole, LEFT)
        t2 = label(r"stripes: \ the edge placed to a third of a pixel", font_size=20, color=YES).next_to(
            sub, UP, buff=0.15).align_to(sub, LEFT)
        ill = note(r"illustrative \ (one LCD row, \ red, \ green, \ blue stripes)", font_size=16).next_to(
            sub, DOWN, buff=0.2).align_to(sub, LEFT)
        notes = VGroup(
            wrapped_label(r"each LCD pixel is three stripes; \ light them separately and the horizontal resolution "
                          r"triples", 5.4, font_size=20, color=WHITE),
            wrapped_label(r"Microsoft's \textbf{ClearType}, \ shipped in Windows XP \ (2001); \ a filter spreads "
                          r"each edge over neighbouring stripes to tame the colour fringes", 5.4, font_size=20,
                          color=YES),
            wrapped_label(r"it must know the stripe order: \ rotate a tablet, \ or change the screen, \ and it is "
                          r"wrong; \ Apple turned it off in macOS in 2018, \ when dense screens made it unnecessary",
                          5.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.8, 0.1, 0])
        with self.voiceover(
            "A liquid-crystal pixel is really three stripes: red, green and blue. <bookmark mark='a'/> Treat the "
            "pixel as a unit, and a stem starting a third of the way in becomes two dim greys. <bookmark mark='b'/> "
            "Light the stripes one by one, and the edge can be placed to a third of a pixel: the horizontal "
            "resolution triples. <bookmark mark='c'/> "
            "Microsoft shipped this as ClearType in Windows XP, with a filter that spreads each edge across "
            "neighbouring stripes to hide the colour fringes. <bookmark mark='d'/> It needs to know the stripe order, "
            "so rotating a tablet breaks it; once screens were dense enough, Apple turned it off in macOS, in 2018."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(whole), Create(outl[0]), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(sub), Create(outl[1]), FadeIn(t2), FadeIn(ill), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def readability(self):
        head = label(r"Readable text", font_size=36).to_edge(UP, buff=0.3)
        prose = ("A line that is too long sends the eye a long way back to the start of the next one, and it is "
                 "easy to land on the wrong line. A line that is too short breaks the sentence into pieces and "
                 "makes the eye jump too often. Somewhere in between, reading feels effortless.")
        wide, narrow = textwrap.wrap(prose, 96), textwrap.wrap(prose, 60)
        long_block = Glyphs("\n".join(wide), font="DejaVu Serif", font_size=17, line_spacing=0.6, color=GREY_A)
        long_block.next_to(head, DOWN, buff=0.75)
        tl = label(rf"{max(len(s) for s in wide)} characters a line, \ tight spacing", font_size=18,
                   color=NO).next_to(long_block, UP, buff=0.1).align_to(long_block, LEFT)
        sweep = CurvedArrow(long_block.get_corner(DR) + DOWN * 0.1, long_block.get_corner(DL) + DOWN * 0.1,
                            angle=-0.12, color=NO, stroke_width=2, tip_length=0.15)
        short_block = Glyphs("\n".join(narrow), font="DejaVu Serif", font_size=17, line_spacing=1.5, color=WHITE)
        short_block.move_to([-3.0, -0.35, 0])
        ts = label(rf"{max(len(s) for s in narrow)} characters, \ line spacing 1.5", font_size=18,
                   color=YES).next_to(short_block, UP, buff=0.12).align_to(short_block, LEFT)
        samp = VGroup()
        for f in ("FreeSerif", "DejaVu Sans"):
            w = Glyphs("Hamburgefonstiv", font=f, font_size=40, color=WHITE)
            x = Glyphs("x", font=f, font_size=40)
            samp.add(VGroup(w, label(f, font_size=16, color=GREY_B)).arrange(DOWN, buff=0.12, aligned_edge=LEFT))
            samp[-1].xh = x.height
        samp.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.7, -0.35, 0])
        guides = VGroup()
        for s in samp:
            w = s[0]
            base = w[0].get_bottom()[1]          # the H sits on the baseline
            for yy, c in ((base, GREY_C), (base + s.xh, HEAD)):
                guides.add(DashedLine([w.get_left()[0] - 0.1, yy, 0], [w.get_right()[0] + 0.1, yy, 0], color=c,
                                      stroke_width=1.5, dash_length=0.06))
        tx = label(r"same size, \ different \textbf{x-height}", font_size=18, color=HEAD).next_to(samp, UP,
                                                                                               buff=0.15)
        notes = VGroup(
            wrapped_label(r"Bringhurst, \ \textit{The Elements of Typographic Style}: \ 45 to 75 characters a line, \ "
                          r"66 ideal; \ WCAG's 1.4.8 \ (AAA): \ at most 80, \ line spacing at least 1.5", 12.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"a large x-height reads bigger at the same size \ (Verdana and Georgia were drawn for "
                          r"screens that way); \ and contrast: \ at least 4.5 to 1 for body text \ (Part 42)", 12.4,
                          font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A very long line sends the eye a long way "
            "back to the start of the next, and it is easy to land on the wrong one. <bookmark mark='b'/> Robert "
            "Bringhurst's Elements of Typographic Style puts a comfortable line at forty-five to seventy-five "
            "characters; the Web Content Accessibility Guidelines, at their strictest level, ask for at most eighty, "
            "with line spacing of at least one and a half. <bookmark mark='c'/> Fonts of the same size can look "
            "very different, because the x-height, the height of the small letters, varies; Verdana and "
            "Georgia, made for screens, have large ones. <bookmark mark='d'/> And text needs contrast: Part 42 "
            "derived the ratio, and body text needs four and a half to one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(long_block), FadeIn(tl))
            self.play(Create(sweep))
            vo.wait_until("b")
            self.play(FadeIn(short_block), FadeIn(ts), FadeIn(notes[0]), long_block.animate.set_opacity(0.45))
            vo.wait_until("c")
            self.play(FadeIn(samp), FadeIn(tx))
            self.play(Create(guides))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM)
