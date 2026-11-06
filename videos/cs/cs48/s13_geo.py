from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.compute import load as load22
from videos.cs.cs48.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono

ALPHABET = "0123456789bcdefghjkmnpqrstuvwxyz"     # geohash's base 32 (explainer.cs.design.keys.geohash)
KM_PER_DEG = 111.2


def square_grid(n, cell, center, color=GREY_D, width=1.0):
    """An n x n grid of cells; returns (lines, pos) where pos(x, y) is the centre of cell (x, y), y upwards."""
    cx, cy = center[0], center[1]
    x0, y0 = cx - n * cell / 2, cy - n * cell / 2
    lines = VGroup()
    for i in range(n + 1):
        lines.add(Line([x0 + i * cell, y0, 0], [x0 + i * cell, y0 + n * cell, 0], color=color, stroke_width=width))
        lines.add(Line([x0, y0 + i * cell, 0], [x0 + n * cell, y0 + i * cell, 0], color=color, stroke_width=width))

    def pos(x, y):
        return np.array([x0 + (x + 0.5) * cell, y0 + (y + 0.5) * cell, 0.0])
    return lines, pos


def curve_path(order, pos, color, width=3.0):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([pos(x, y) for x, y in order])


def runs_of(order, cells):
    """The maximal runs of consecutive curve positions that cover a set of cells."""
    idx = {tuple(p): i for i, p in enumerate(order)}
    ks = sorted(idx[c] for c in cells)
    out, cur = [], [ks[0]]
    for a, b in zip(ks, ks[1:]):
        if b == a + 1:
            cur.append(b)
        else:
            out.append(cur)
            cur = [b]
    out.append(cur)
    return [[tuple(order[k]) for k in r] for r in out]


def cell_size(chars, lat):
    """Width and height (km) of a geohash cell of `chars` characters at latitude `lat`, from the definition:
    5 bits a character, longitude taking the first, third, ... bit."""
    bits = 5 * chars
    lon_bits, lat_bits = (bits + 1) // 2, bits // 2
    w = 360 / 2 ** lon_bits * KM_PER_DEG * math.cos(math.radians(lat))
    h = 180 / 2 ** lat_bits * KM_PER_DEG
    return w, h


def km(x):
    if x >= 10:
        return f"{x:,.0f} km"
    if x >= 1:
        return f"{x:.1f} km"
    return f"{1000 * x:.0f} m"


def hexagon(center, r, color, opacity):
    pts = [center + r * np.array([math.cos(math.radians(90 + 60 * k)), math.sin(math.radians(90 + 60 * k)), 0])
           for k in range(6)]
    return Polygon(*pts, stroke_color=GREY_B, stroke_width=1.2, fill_color=color, fill_opacity=opacity)


class Geo(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.interleave()
        self.geohash()
        self.hilbert()
        self.cells()
        self.nearest()

    def card(self):
        card = chapter_card(12, r"Maps as keys", r"How does an index built for a line find what is near?",
                            lit=(1891, 2018), extra=((1891, r"Hilbert's curve"), (1966, r"Morton: \ Z-order"),
                                                     (2018, r"Uber: \ H3")), part=PART)
        with self.voiceover("Chapter twelve. Maps as keys."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ two dimensions, one index
    def problem(self):
        d = load22("kd")
        P = d["P"]
        (bx0, by0), (bx1, by1) = d["box"]
        head = label(r"Two dimensions, \ one index", font_size=36).to_edge(UP, buff=0.3)
        side, c = 4.8, np.array([-3.3, -0.35, 0])
        org = c - np.array([side / 2, side / 2, 0])

        def at(x, y):
            return org + np.array([x * side, y * side, 0])
        frame = Square(side_length=side, stroke_color=GREY_C, stroke_width=1.5).move_to(c)
        dots = VGroup(*[Dot(at(x, y), radius=0.055, color=GREY_A) for x, y in P])
        xband = Rectangle(width=(bx1 - bx0) * side, height=side, stroke_width=0, fill_color=DATA,
                          fill_opacity=0.18).move_to(at((bx0 + bx1) / 2, 0.5))
        yband = Rectangle(width=side, height=(by1 - by0) * side, stroke_width=0, fill_color=LAM,
                          fill_opacity=0.18).move_to(at(0.5, (by0 + by1) / 2))
        box = Rectangle(width=(bx1 - bx0) * side, height=(by1 - by0) * side, stroke_color=YES,
                        stroke_width=3).move_to(at((bx0 + bx1) / 2, (by0 + by1) / 2))
        in_x = [i for i, (x, y) in enumerate(P) if bx0 <= x <= bx1]
        in_y = [i for i, (x, y) in enumerate(P) if by0 <= y <= by1]
        inside = [i for i in in_x if i in in_y]
        xl = label(r"longitude", font_size=17, color=GREY_A).next_to(frame, DOWN, buff=0.12)
        yl = label(r"latitude", font_size=17, color=GREY_A).rotate(PI / 2).next_to(frame, LEFT, buff=0.12)
        notes = VGroup(
            wrapped_label(r"a B-tree \ (Part 35) \ orders one number: \ ``everything in this box'' is a range in "
                          r"two", 5.6, font_size=20, color=WHITE),
            wrapped_label(rf"an index on longitude alone returns {len(in_x)} points; \ one on latitude alone, \ "
                          rf"{len(in_y)}", 5.6, font_size=20, color=DATA),
            wrapped_label(rf"the box holds {len(inside)}: \ most of the work was wasted", 5.6, font_size=20,
                          color=YES),
            wrapped_label(r"we want one key per place, \ such that places near each other get keys near each "
                          r"other", 5.6, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, -0.1, 0])
        foot = note(rf"Part 22's {len(P)} random points and query box", font_size=16).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "A map query is a box in two dimensions: every café within a kilometre. <bookmark mark='a'/> But Part "
            "35's B-tree orders a single number. <bookmark mark='b'/> Index longitude alone, and the box returns a "
            "whole strip: twenty-three of Part 22's sixty points. Latitude alone returns twenty-two. <bookmark "
            "mark='c'/> The box holds eight. <bookmark mark='d'/> We want one key for every place, so that places "
            "near each other get keys near each other. Then an ordinary index will do."
        ) as vo:
            self.play(FadeIn(head), Create(frame), FadeIn(xl), FadeIn(yl), FadeIn(dots), FadeIn(foot))
            self.play(Create(box))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(xband), *[dots[i].animate.set_color(DATA) for i in in_x], FadeIn(notes[1]))
            self.play(FadeIn(yband), *[dots[i].animate.set_color(LAM) for i in in_y if i not in inside])
            vo.wait_until("c")
            self.play(*[dots[i].animate.set_color(YES).scale(1.5) for i in inside], FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Morton: interleave the bits
    def interleave(self):
        cv = load("curves")["order3"]
        head = label(r"Interleave the bits", font_size=36).to_edge(UP, buff=0.3)
        n, cell = 8, 0.56
        lines, pos = square_grid(n, cell, [-3.6, -0.45, 0])
        path = curve_path(cv["morton"], pos, DATA, width=3)
        xt = VGroup(*[label(str(i), font_size=16, color=GREY_B).next_to(pos(i, 0), DOWN, buff=0.32) for i in range(n)])
        yt = VGroup(*[label(str(j), font_size=16, color=GREY_B).next_to(pos(0, j), LEFT, buff=0.32) for j in range(n)])
        X, Y = 5, 3
        z = cv["morton"].index([X, Y])
        target = Square(side_length=cell, stroke_width=0, fill_color=HEAD, fill_opacity=0.55).move_to(pos(X, Y))
        zl = label(rf"{z}", font_size=18, color=WHITE).move_to(pos(X, Y))
        xb, yb = format(X, "03b"), format(Y, "03b")

        def bits(s, color):
            return VGroup(*[mono(ch, size=30, color=color) for ch in s]).arrange(RIGHT, buff=0.22)
        rx = VGroup(label(rf"$x = {X}$", font_size=26, color=DATA), bits(xb, DATA)).arrange(RIGHT, buff=0.4)
        ry = VGroup(label(rf"$y = {Y}$", font_size=26, color=LAM), bits(yb, LAM)).arrange(RIGHT, buff=0.4)
        inter = VGroup(*[mono(ch, size=30, color=col) for a, b in zip(yb, xb) for ch, col in ((a, LAM), (b, DATA))])
        inter.arrange(RIGHT, buff=0.18)
        rz = VGroup(label(rf"key", font_size=26, color=HEAD), inter,
                    label(rf"$= {z}$", font_size=26, color=HEAD)).arrange(RIGHT, buff=0.35)
        block = VGroup(rx, ry, rz).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.6, 0])
        notes = VGroup(
            wrapped_label(r"take one bit of $y$, \ one of $x$, \ in turn: \ the key is the cell's place along a "
                          r"Z-shaped path \ (Morton, \ IBM, \ 1966)", 5.8, font_size=20, color=WHITE),
            wrapped_label(r"each pair of bits picks a quadrant, \ so a shared prefix means a shared square: \ the "
                          r"key's first two bits are the quarter of the map, \ the next two the quarter of that", 5.8,
                          font_size=20, color=YES),
            wrapped_label(r"but the Z jumps: \ cells side by side across a big square's edge can be far apart "
                          r"along the path", 5.8, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(block, notes).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.7, -0.35, 0])
        ja, jb = (3, 3), (3, 4)
        jump = VGroup(*[VGroup(Square(side_length=cell, stroke_color=NO, stroke_width=4).move_to(pos(*c)),
                               label(str(cv["morton"].index(list(c))), font_size=16, color=NO).move_to(pos(*c)))
                        for c in (ja, jb)])
        with self.voiceover(
            "The oldest answer interleaves the bits. <bookmark mark='a'/> Take the cell at x five, y three, write "
            "both in binary, and take one bit of y, then one of x, in turn: twenty-seven. <bookmark mark='b'/> Number"
            " every cell this way and the keys trace a Z at every scale, as Guy Morton described at IBM in 1966. "
            "<bookmark mark='c'/> Each pair of bits picks a quadrant, so a square on the map is a range of keys. "
            "<bookmark mark='d'/> The flaw is the jumps: cells fifteen and thirty-seven are side by side."
        ) as vo:
            self.play(FadeIn(head), Create(lines), FadeIn(xt), FadeIn(yt))
            vo.wait_until("a")
            self.play(FadeIn(rx), FadeIn(ry))
            self.play(LaggedStart(*[TransformFromCopy((ry[1] if k % 2 == 0 else rx[1])[k // 2], inter[k])
                                    for k in range(6)], lag_ratio=0.3), FadeIn(rz[0]), run_time=2.0)
            self.play(FadeIn(rz[2]), FadeIn(target), FadeIn(zl))
            vo.wait_until("b")
            self.play(Create(path), FadeIn(notes[0]), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]), FadeIn(jump))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ geohash
    def geohash(self):
        g = load("geohash")
        head = label(r"Geohash: \ Z-order on the globe", font_size=36).to_edge(UP, buff=0.3)
        cw = 0.8
        W, H = 8 * cw, 4 * cw
        org = np.array([-6.6, -0.75, 0])                                     # bottom-left corner of the world

        def at(lon, lat):
            return org + np.array([(lon + 180) / 360 * W, (lat + 90) / 180 * H, 0])
        world = Rectangle(width=W, height=H, stroke_color=GREY_C, stroke_width=1.5).move_to(org + [W / 2, H / 2, 0])
        lines = VGroup(*[Line(at(-180 + 45 * i, -90), at(-180 + 45 * i, 90), color=GREY_D, stroke_width=1)
                         for i in range(1, 8)],
                       *[Line(at(-180, -90 + 45 * j), at(180, -90 + 45 * j), color=GREY_D, stroke_width=1)
                         for j in range(1, 4)])
        letters, centres = VGroup(), {}
        for col in range(8):
            for row in range(4):
                idx = (col >> 2) << 4 | (row >> 1) << 3 | ((col >> 1) & 1) << 2 | (row & 1) << 1 | (col & 1)
                p = at(-180 + 45 * (col + 0.5), -90 + 45 * (row + 0.5))
                centres[idx] = p
                ch = ALPHABET[idx]
                letters.add(mono(ch, size=20, color=HEAD if ch in "gdu" else GREY_B).move_to(p + [0.2, 0.2, 0]))
        zpath = VMobject(stroke_color=GREY_C, stroke_width=1.5).set_points_as_corners(
            [centres[i] for i in range(32)])
        lon_d = Dot(at(-0.1276, 51.5072), radius=0.07, color=YES)
        nyc_d = Dot(at(-74.006, 40.7128), radius=0.07, color=DATA)
        lon_l = label(rf"London: \ \texttt{{{g['london']}}}", font_size=17, color=YES).next_to(world, UP, buff=0.12)
        lon_l.align_to(world, RIGHT)
        nyc_l = label(rf"New York: \ \texttt{{{g['new_york']}}}", font_size=17, color=DATA).next_to(
            world, UP, buff=0.12).align_to(world, LEFT)
        lon_ln = Line(lon_d.get_center(), lon_l.get_bottom() + DOWN * 0.03, color=YES, stroke_width=1.2)
        nyc_ln = Line(nyc_d.get_center(), nyc_l.get_bottom() + DOWN * 0.03, color=DATA, stroke_width=1.2)
        lat = 51.5072
        rows = []
        for p in g["london_prefixes"]:
            w, h = cell_size(len(p), lat)
            rows.append([p, rf"{km(w)} \ $\times$ \ {km(h)}"])
        tab = grid_table([r"London's prefix", r"cell, \ wide $\times$ high"], rows, widths=[2.4, 3.4], row_h=0.4,
                         font_size=19, mono_cols=(0,))
        tab.move_to([3.85, 0.95, 0])
        notes = VGroup(
            wrapped_label(r"five bits a character, \ longitude and latitude in turn: \ each character divides the "
                          r"cell into 32", 6.2, font_size=19, color=WHITE),
            wrapped_label(r"a shared prefix means a shared cell: \ London and New York share none", 5.7, font_size=19,
                          color=YES),
            wrapped_label(r"but London sits at the edge of \texttt{g}: \ a street east of the Greenwich "
                          r"meridian begins with \texttt{u}, \ so a search covers the cell and its eight neighbours",
                          5.7, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        notes[0].next_to(world, DOWN, buff=0.3).align_to(world, LEFT)
        VGroup(notes[1], notes[2]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.35)
        notes[1:].align_to(tab, LEFT)
        meridian = DashedLine(at(0, -90), at(0, 90), color=NO, stroke_width=2)
        foot = note(r"geohashes computed; \ cell sizes from the definition at London's latitude", font_size=16)
        foot.to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Geohash, published by Gustavo Niemeyer in 2008, is the Z-order on the globe. <bookmark mark='a'/> Halve "
            "longitude, then latitude, in turn, and spell every five bits as one of thirty-two characters: the first "
            "names one of these thirty-two cells. <bookmark mark='b'/> Each further character divides the cell by "
            "thirty-two: seven pin central London to about ninety-five metres by a hundred and fifty-three. <bookmark"
            " mark='c'/> New York shares no prefix with London. <bookmark mark='d'/> But London sits on the edge of "
            "cell g; east of the Greenwich meridian, addresses begin with u. So a search covers the cell and its "
            "eight neighbours."
        ) as vo:
            self.play(FadeIn(head), Create(world), Create(lines), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(letters), Create(zpath), FadeIn(notes[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(lon_d), Create(lon_ln), FadeIn(lon_l), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*r), shift=RIGHT * 0.1) for r in tab.cells[1:]], lag_ratio=0.35),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(nyc_d), Create(nyc_ln), FadeIn(nyc_l), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(Create(meridian), FadeIn(notes[2]), Indicate(lon_d, color=NO))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Hilbert against Z-order; S2
    def hilbert(self):
        cv = load("curves")
        o3, loc = cv["order3"], cv["locality"]
        Z, Hc = loc["z-order"], loc["hilbert"]
        head = label(r"Hilbert: \ a curve without jumps", font_size=36).to_edge(UP, buff=0.3)
        n, cell = 8, 0.42
        gl_z, pz = square_grid(n, cell, [-4.6, 1.05, 0])
        gl_h, ph = square_grid(n, cell, [-0.4, 1.05, 0])
        path_z = curve_path(o3["morton"], pz, DATA, width=2.5)
        path_h = curve_path(o3["hilbert"], ph, LAM, width=2.5)
        tz = label(r"Z-order", font_size=20, color=DATA).next_to(gl_z, UP, buff=0.1)
        th = label(r"Hilbert", font_size=20, color=LAM).next_to(gl_h, UP, buff=0.1)
        qx, qy, qw, qh = 1, 2, 4, 3
        cells = [(x, y) for x in range(qx, qx + qw) for y in range(qy, qy + qh)]
        shades = [HEAD, YES, KERN, NO]

        def colour_runs(order, pos):
            rs = runs_of(order, cells)
            g = VGroup()
            for k, r in enumerate(rs):
                for c in r:
                    g.add(Square(side_length=cell * 0.92, stroke_width=0, fill_color=shades[k % 4],
                                 fill_opacity=0.5).move_to(pos(*c)))
            return g, len(rs)
        fz, nz = colour_runs(o3["morton"], pz)
        fh, nh = colour_runs(o3["hilbert"], ph)
        cz = label(rf"this box: \ {nz} key ranges", font_size=19, color=DATA).next_to(gl_z, DOWN, buff=0.15)
        ch = label(rf"this box: \ {nh} key ranges", font_size=19, color=LAM).next_to(gl_h, DOWN, buff=0.15)
        tab = grid_table([r"on a $256 \times 256$ grid", r"Z-order", r"Hilbert"],
                         [[r"key ranges to cover a $16 \times 16$ box, \ mean", f"{Z['mean_ranges_16x16']:.1f}",
                           f"{Hc['mean_ranges_16x16']:.1f}"],
                          [r"\dots \ worst of 300 boxes", f"{Z['max_ranges']}", f"{Hc['max_ranges']}"],
                          [r"neighbouring cells: \ distance along the curve, \ median",
                           f"{Z['median_gap']}", f"{Hc['median_gap']}"],
                          [r"\dots \ 99th percentile", f"{Z['p99_gap']:,}", f"{Hc['p99_gap']:,}"]],
                         widths=[5.4, 1.3, 1.3], row_h=0.4, font_size=18,
                         colors=[[WHITE, NO, YES], [WHITE, NO, YES], [WHITE, GREY_A, GREY_A], [WHITE, GREY_A, GREY_A]],
                         mono_cols=())
        tab.next_to(VGroup(cz, ch), DOWN, buff=0.35).align_to(gl_z, LEFT)
        notes = VGroup(
            wrapped_label(r"each step of the Hilbert curve moves to a cell next door; \ it has the Z's quadrants, "
                          r"\ rotated so the pieces join", 4.2, font_size=19, color=WHITE),
            wrapped_label(r"every curve must break somewhere: \ the tails match; \ but a box needs about half as "
                          r"many ranges", 4.2, font_size=19, color=YES),
            wrapped_label(r"Google's \textbf{S2}: \ the sphere projected onto a cube's six faces, \ each ordered by "
                          r"a Hilbert curve; \ a cell is a 64-bit integer, \ 30 levels deep; \ a region is covered "
                          r"by a few cells of mixed sizes, \ each a range of keys", 4.2, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.55, -0.15, 0])
        box_z = Rectangle(width=qw * cell, height=qh * cell, stroke_color=WHITE, stroke_width=3).move_to(
            (pz(qx, qy) + pz(qx + qw - 1, qy + qh - 1)) / 2)
        box_h = box_z.copy().move_to((ph(qx, qy) + ph(qx + qw - 1, qy + qh - 1)) / 2)
        foot = note(r"curves and locality computed", font_size=16).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "David Hilbert's curve of 1891 removes the jumps. <bookmark mark='a'/> It visits the same quadrants, but "
            "rotates the pieces so that every step moves next door. <bookmark mark='b'/> Ask for this box of twelve "
            "cells. Along the Z it falls into seven runs of keys, seven range scans; along Hilbert, four. <bookmark "
            "mark='c'/> On a grid of two hundred and fifty-six squared, a sixteen by sixteen box needs about thirty "
            "ranges on the Z and fifteen on Hilbert. Some neighbours still land far apart on both: every curve must "
            "break somewhere. <bookmark mark='d'/> Google's S2 projects the Earth onto a cube, orders each face along"
            " a Hilbert curve, and names cells with sixty-four bit integers, thirty levels deep."
        ) as vo:
            self.play(FadeIn(head), Create(gl_z), Create(gl_h), FadeIn(tz), FadeIn(th), FadeIn(foot))
            self.play(Create(path_z), run_time=2.0, rate_func=linear)
            vo.wait_until("a")
            self.play(Create(path_h), FadeIn(notes[0]), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(box_z), Create(box_h))
            self.play(FadeIn(fz), FadeIn(cz))
            self.play(FadeIn(fh), FadeIn(ch))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.5), FadeIn(notes[1]),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ quadtrees and hexagons
    def cells(self):
        P = load22("kd")["P"]
        head = label(r"Quadtrees and hexagons", font_size=36).to_edge(UP, buff=0.3)
        side, c = 4.4, np.array([-4.2, -0.15, 0])
        org = c - np.array([side / 2, side / 2, 0])

        def at(x, y):
            return org + np.array([x * side, y * side, 0])
        frame = Square(side_length=side, stroke_color=GREY_C, stroke_width=1.5).move_to(c)
        dots = VGroup(*[Dot(at(x, y), radius=0.05, color=GREY_A) for x, y in P])
        # an adaptive quadtree, built here over Part 22's points: split any square holding more than 3
        levels = [VGroup() for _ in range(5)]

        def split(x0, y0, s, pts, depth):
            if len(pts) <= 3 or depth >= len(levels):
                return
            m = s / 2
            levels[depth].add(Line(at(x0 + m, y0), at(x0 + m, y0 + s), color=KERN, stroke_width=1.6),
                              Line(at(x0, y0 + m), at(x0 + s, y0 + m), color=KERN, stroke_width=1.6))
            for dx in (0, 1):
                for dy in (0, 1):
                    ax, ay = x0 + dx * m, y0 + dy * m
                    split(ax, ay, m, [p for p in pts if ax <= p[0] < ax + m and ay <= p[1] < ay + m], depth + 1)
        split(0.0, 0.0, 1.0, P, 0)
        ql = label(r"an adaptive quadtree: \ split any square holding more than 3", font_size=18,
                   color=KERN).next_to(frame, DOWN, buff=0.15)
        # hexagons: a cell, its ring, the next ring (axial coordinates)
        r = 0.34
        hc = np.array([1.2, 1.05, 0])

        def hpos(q, s):
            return hc + r * np.array([math.sqrt(3) * (q + s / 2), 1.5 * s, 0])
        hexes = VGroup()
        for q in range(-2, 3):
            for s in range(-2, 3):
                k = max(abs(q), abs(s), abs(-q - s))
                if k <= 2:
                    col, op = ((HEAD, 0.75), (YES, 0.45), (DATA, 0.2))[k]
                    hexes.add(hexagon(hpos(q, s), r, col, op))
        sq_c, sc = np.array([4.75, 1.05, 0]), 0.62
        squares = VGroup(*[Square(side_length=sc, stroke_color=GREY_B, stroke_width=1.2,
                                  fill_color=HEAD if (i, j) == (0, 0) else (YES if i == 0 or j == 0 else NO),
                                  fill_opacity=0.75 if (i, j) == (0, 0) else 0.4).move_to(
                                      sq_c + sc * np.array([i, j, 0]))
                           for i in (-1, 0, 1) for j in (-1, 0, 1)])
        sql = VGroup(label(r"1", font_size=17, color=YES).move_to(sq_c + [sc, 0, 0]),
                     label(rf"{math.sqrt(2):.2f}", font_size=17, color=NO).move_to(sq_c + [sc, sc, 0]))
        notes = VGroup(
            wrapped_label(r"squares: \ four neighbours across an edge, \ four across a corner, \ at 1 and "
                          rf"{math.sqrt(2):.2f} cell widths; \ hexagons: \ six, \ all at one distance", 6.0,
                          font_size=19, color=WHITE),
            wrapped_label(r"\textbf{H3} \ (Uber, \ 2018): \ hexagons on an icosahedron, \ 16 resolutions, \ each "
                          r"cell about a seventh of its parent; \ 12 pentagons at every resolution; \ children "
                          r"only roughly tile their parent", 6.0, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, -1.9, 0])
        with self.voiceover(
            "Geohash and S2 cut the map the same way everywhere. <bookmark mark='a'/> A quadtree cuts only where it "
            "must: split any square holding more than three points, and repeat, so cells are small in the city and "
            "large over the sea. <bookmark mark='b'/> Squares are awkward for movement: four neighbours share an "
            "edge, four only a corner, one point four one widths away. A hexagon's six neighbours are all equally "
            "far. <bookmark mark='c'/> Uber's H3, open-sourced in 2018, tiles the Earth with hexagons at sixteen "
            "resolutions, each cell about a seventh of its parent. The price: twelve pentagons at every resolution, "
            "and children that only roughly tile their parent."
        ) as vo:
            self.play(FadeIn(head), Create(frame), FadeIn(dots))
            vo.wait_until("a")
            for lv in levels:
                if len(lv):
                    self.play(Create(lv), run_time=0.8)
            self.play(FadeIn(ql))
            vo.wait_until("b")
            self.play(FadeIn(squares), FadeIn(sql))
            self.play(LaggedStart(*[FadeIn(h) for h in hexes], lag_ratio=0.05), FadeIn(notes[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ nearest neighbours
    def nearest(self):
        d = load22("kd")
        hd = load22("highdim")
        kd2 = next(r for r in hd["kd"] if r["d"] == 2)
        P = d["P"]
        head = label(r"Nearest neighbours", font_size=36).to_edge(UP, buff=0.3)
        n, side = 8, 4.8
        cell = side / n
        lines, pos = square_grid(n, cell, [-3.6, -0.3, 0], color=GREY_D)
        org = np.array([-3.6 - side / 2, -0.3 - side / 2, 0])

        def at(x, y):
            return org + np.array([x * side, y * side, 0])
        dots = VGroup(*[Dot(at(x, y), radius=0.055, color=GREY_A) for x, y in P])
        q = (0.42, 0.40)                                                  # an illustrative query point
        qd = Star(n=5, outer_radius=0.14, inner_radius=0.06, color=HEAD, fill_opacity=1).move_to(at(*q))
        k = 3
        qc = (int(q[0] * n), int(q[1] * n))

        def cell_of(p):
            return (min(n - 1, int(p[0] * n)), min(n - 1, int(p[1] * n)))

        def dist(p):
            return math.hypot(p[0] - q[0], p[1] - q[1])
        # rings of cells around the query's until k candidates are found
        searched, ring_groups, ring = set(), [], 0
        while True:
            new = {(x, y) for x in range(qc[0] - ring, qc[0] + ring + 1) for y in range(qc[1] - ring, qc[1] + ring + 1)
                   if 0 <= x < n and 0 <= y < n} - searched
            searched |= new
            ring_groups.append(VGroup(*[Square(side_length=cell, stroke_width=0, fill_color=DATA,
                                               fill_opacity=0.22).move_to(pos(*c)) for c in sorted(new)]))
            found = [i for i, p in enumerate(P) if cell_of(p) in searched]
            if len(found) >= k:
                break
            ring += 1
        rk = sorted(dist(P[i]) for i in found)[k - 1]
        # every cell the circle through the k-th candidate touches must be searched as well
        extra = set()
        for x in range(n):
            for y in range(n):
                nx = min(max(q[0], x / n), (x + 1) / n)
                ny = min(max(q[1], y / n), (y + 1) / n)
                if math.hypot(nx - q[0], ny - q[1]) <= rk and (x, y) not in searched:
                    extra.add((x, y))
        extra_g = VGroup(*[Square(side_length=cell, stroke_width=0, fill_color=LAM, fill_opacity=0.28).move_to(pos(*c))
                           for c in sorted(extra)])
        circle = Circle(radius=rk * side, color=HEAD, stroke_width=2.5).move_to(at(*q))
        best = sorted(range(len(P)), key=lambda i: dist(P[i]))[:k]
        cand = [i for i in found if i not in best]
        notes = VGroup(
            wrapped_label(rf"look in the query's cell, \ then rings of neighbours, \ until there are {k} candidates",
                          5.4, font_size=19, color=DATA),
            wrapped_label(rf"the {k}rd candidate's circle may reach cells not yet searched: \ search them too; \ "
                          r"the cells only filter, \ exact distances decide", 5.4, font_size=19, color=LAM),
            wrapped_label(rf"Part 22's kd-tree: \ one nearest neighbour among {hd['kd_n']:,} points, \ visiting "
                          rf"about {kd2['visited']:.0f} of its {kd2['nodes']:,} nodes", 5.4, font_size=19,
                          color=YES),
            wrapped_label(r"in practice: \ PostGIS's R-tree index answers \texttt{ORDER BY} distance "
                          r"\texttt{LIMIT k}; \ ride-hailing \ (Part 49) \ asks it of hexagons, \ for every "
                          r"ride request", 5.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.2, 0])
        foot = note(r"Part 22's points; \ the query point is illustrative", font_size=16).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "The commonest map question is: what are the nearest three? <bookmark mark='a'/> Look in the query's "
            "cell, then in rings around it, until there are three candidates. <bookmark mark='b'/> That is not yet "
            "the answer: the circle through the third reaches cells not yet searched, where a closer point could "
            "hide. Search those too, then rank by exact distance. <bookmark mark='c'/> Part 22's kd-tree found one "
            "nearest neighbour among twenty thousand points by visiting about twenty-five of its forty thousand "
            "nodes. <bookmark mark='d'/> PostGIS answers such queries from its R-tree index, and Part 49's "
            "ride-hailing dispatcher asks them of hexagons."
        ) as vo:
            self.play(FadeIn(head), Create(lines), FadeIn(dots), FadeIn(qd), FadeIn(foot))
            vo.wait_until("a")
            for rg in ring_groups:
                self.play(FadeIn(rg), run_time=0.7)
            self.play(*[dots[i].animate.set_color(DATA).scale(1.4) for i in found], FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(circle), FadeIn(extra_g), FadeIn(notes[1]))
            self.play(*[dots[i].animate.set_color(YES).scale(1.3) for i in best],
                      *[dots[i].animate.set_color(GREY_B) for i in cand])
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KM_PER_DEG)
