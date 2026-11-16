from __future__ import annotations

import numpy as np

from videos.music.music55.common import *  # noqa: F403

KCOL = {"axial": TUNE, "tangential": BLUE, "oblique": EAR}


class Modes(SoundScene):
    def construct(self):
        chapter(self, 2, r"Modes", r"Why does the bass boom in one corner and vanish in the middle?")
        self.box()
        self.ladder()
        self.count()
        self.schroeder()
        self.corner()
        self.fixes()

    # ------------------------------------------------------------------
    def box(self):
        eq = MathTex(r"f_{n_x n_y n_z} = \frac{c}{2}\sqrt{\Bigl(\frac{n_x}{L_x}\Bigr)^2 + \Bigl(\frac{n_y}{L_y}\Bigr)^2 + \Bigl(\frac{n_z}{L_z}\Bigr)^2}", font_size=38).to_edge(UP, buff=1.0)
        items = [
            (r"a pipe closed at both ends rings at $c/2L$ and its multiples \ (Part 2); \ a room is a pipe three ways at once", WHITE),
            (r"axial modes bounce between one pair of walls; \ tangential ones round four; \ oblique ones round all six", WHITE),
            (r"each mode has a pattern of loud places \ (antinodes) \ and silent planes \ (nodes); \ every mode is loud in every corner", WHITE),
            (r"a 5 by 4 by 2.7 metre room: \ the first mode, \ along its length, \ at $343/10 = 34.3$ Hz", TUNE),
        ]
        rows = text_rows(items, font_size=23).next_to(eq, DOWN, buff=0.55)
        head = label(r"a room is a pipe in three directions", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Below a few hundred hertz, a room is not a diffuse field at all. <bookmark mark='a'/> A pipe closed at both ends "
            "rings at c over twice its length and the multiples, as in Part 2; a rectangular room is such a pipe in three "
            "directions at once, and its resonances are given by this formula, one for every triple of whole numbers. "
            "<bookmark mark='b'/> Axial modes bounce between one pair of walls; tangential modes go round four walls; oblique "
            "modes round all six. <bookmark mark='c'/> Each mode has loud places, the antinodes, and silent planes, the nodes, "
            "and every mode is loud in every corner. <bookmark mark='d'/> A living room five metres by four by two point seven "
            "has its first mode along its length, at three hundred and forty-three over ten: thirty-four point three hertz."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ladder(self):
        d = load("modes")
        ax = frame_axes(width=11.0, height=2.6, xlo=20, xhi=120, ylo=0, yhi=1.0, center=DOWN * 0.4)
        hs = {"axial": 1.0, "tangential": 0.7, "oblique": 0.45}
        st = VGroup()
        for f, n, k in d["modes"]:
            st.add(VGroup(Line(ax.to(f, 0), ax.to(f, hs[k]), color=KCOL[k], stroke_width=3), Dot(ax.to(f, hs[k]), radius=0.06, color=KCOL[k])))
        tags = VGroup()
        for f, n, k in d["modes"][:5]:
            tags.add(label(rf"({n[0]},{n[1]},{n[2]})", font_size=13, color=KCOL[k]).next_to(ax.to(f, hs[k]), UP, buff=0.1))
        xt = VGroup(*[label(f"{v} Hz", font_size=15, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.12) for v in (20, 40, 60, 80, 100, 120)])
        key = VGroup(*[label(k, font_size=17, color=c_) for k, c_ in KCOL.items()]).arrange(RIGHT, buff=0.7).to_edge(UP, buff=1.0)
        note = label(rf"{len(d['modes'])} modes below 120 Hz, \ unevenly spaced: \ gaps of 10 Hz and more at the bottom", font_size=18, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"the modes of a living room", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Here are the room's modes up to a hundred and twenty hertz, with the axial ones tallest, as a visual convention; actual strengths depend on damping and source and receiver positions. <bookmark mark='a'/> The first few stand alone: one, nought, nought along the length at thirty-four hertz, nought, one, nought across the width at forty-three, the first tangential mode at fifty-five, the height at sixty-four. <bookmark mark='b'/> There are {say(len(d['modes']))} below a hundred and twenty hertz, crowding together as the frequency rises, but at the bottom there are gaps of ten hertz and more. Modes can create peaks and dips, depending on source and receiver positions and damping."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(key), FadeIn(ghost(st, 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in st[:4]], lag_ratio=0.3), FadeIn(tags[:4]), run_time=1.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in st[4:]], lag_ratio=0.08), FadeIn(tags[4:]), FadeIn(note), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        d = load("modes")
        fg = np.array(d["fgrid"])
        ax = frame_axes(width=8.6, height=3.2, xlo=20, xhi=120, ylo=0, yhi=22, center=DOWN * 0.3 + LEFT * 0.4)
        pts = []
        for i, (f, k) in enumerate(zip(fg, d["counts"])):
            if i:
                pts.append(ax.to(f, d["counts"][i - 1]))
            pts.append(ax.to(f, k))
        stair = VMobject(stroke_color=TUNE, stroke_width=3).set_points_as_corners(pts)
        wy = curve(fg, d["weyl"], ax.to, color=EAR, width=3)
        xt = VGroup(*[label(f"{v} Hz", font_size=15, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.12) for v in (20, 40, 60, 80, 100, 120)])
        yt = VGroup(*[label(f"{v}", font_size=15, color=GREY_A).next_to(ax.to(20, v), LEFT, buff=0.12) for v in (0, 10, 20)])
        eq = MathTex(r"N(f) \approx \frac{4\pi V}{3c^3}f^3 + \frac{\pi S}{4c^2}f^2 + \frac{L}{8c}f", font_size=32, color=EAR).to_edge(UP, buff=1.0)
        key = VGroup(label(r"modes counted", font_size=17, color=TUNE), label(r"Weyl's estimate", font_size=17, color=EAR)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        note = label(rf"at 120 Hz: \ {d['counts'][-1]} counted, \ {d['weyl'][-1]:.1f} estimated; \ the $f^3$ term wins, \ so modes crowd as the pitch rises", font_size=18, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"counting modes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How fast do they crowd? <bookmark mark='a'/> Count the modes below each frequency, and you get this staircase. "
            "<bookmark mark='b'/> Hermann Weyl showed in 1911 that, for any shape, the count grows like the volume times the "
            "frequency cubed, with corrections for the surface and the edges; for a box the formula is this. "
            f"<bookmark mark='c'/> At a hundred and twenty hertz the room has {say(d['counts'][-1])} modes, and Weyl estimates "
            f"{say(d['weyl'][-1], 1)}. The cube wins: double the frequency and there are eight times as many."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(ghost(VGroup(stair, wy), 0.25)))
            vo.wait_until("a")
            self.play(Create(stair), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(eq), Create(wy), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def schroeder(self):
        d = load("modes")
        eq = MathTex(r"f_S = 2000\,\sqrt{T_{60}/V}", font_size=40, color=TUNE).move_to(UP * 1.6)
        items = [
            (r"each mode is a resonance with a bandwidth set by the room's damping: \ about $2.2/T_{60}$ Hz", WHITE),
            (r"above the Schroeder frequency, \ three or more modes overlap in every bandwidth: \ the response becomes a random jumble, \ the same everywhere on average", WHITE),
            (rf"the living room \ ($T_{{60}} = {d['T']:.2f}$ s, \ {d['V']:.0f} m$^3$): \ {d['fs_room']:.0f} Hz: \ the whole bass is modal", TUNE),
            (rf"a concert hall \ (1.9 s, \ 18,750 m$^3$): \ {d['fs_hall']:.0f} Hz: \ statistical almost everywhere", BLUE),
        ]
        rows = text_rows(items, font_size=22).move_to(DOWN * 0.9)
        head = label(r"where modes stop mattering", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Where do modes stop mattering? <bookmark mark='a'/> Each mode is a resonance with a bandwidth set by the room's "
            "damping, about two point two over the reverberation time. <bookmark mark='b'/> Manfred Schroeder worked out in "
            "1954 that once about three modes overlap within each bandwidth, the response is a random jumble of peaks and dips, "
            "the same everywhere on average, making statistical descriptions more useful, provided their other assumptions are adequate. That happens above two thousand times the square "
            f"root of T over V. <bookmark mark='c'/> For the living room, {say(d['fs_room'])} hertz: its whole bass is a few "
            f"separate resonances. <bookmark mark='d'/> For a concert hall, {say(d['fs_hall'])} hertz: statistical almost "
            "everywhere. Small rooms generally have separated modes over more of the bass range; halls can still have low-frequency problems."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def corner(self):
        d = load("modes")
        c = clip("modes.two")
        f = np.array(d["spec"]["f"])
        ax = frame_axes(width=9.6, height=3.0, xlo=20, xhi=120, ylo=-35, yhi=0, center=DOWN * 0.2)
        cc = curve(f, np.clip(d["spec"]["corner"], -35, 0), ax.to, color=EAR, width=3)
        cm = curve(f, np.clip(d["spec"]["middle"], -35, 0), ax.to, color=BLUE, width=3)
        xt = VGroup(*[label(f"{v} Hz", font_size=15, color=GREY_A).next_to(ax.to(v, -35), DOWN, buff=0.12) for v in (20, 40, 60, 80, 100, 120)])
        yt = VGroup(*[label(f"{v} dB", font_size=15, color=GREY_A).next_to(ax.to(20, v), LEFT, buff=0.12) for v in (0, -15, -30)])
        key = VGroup(label(r"listening in a corner", font_size=17, color=EAR), label(r"listening in the middle", font_size=17, color=BLUE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)
        note = label(r"the source in the opposite corner; \ the middle of the room sits on a node of every odd mode", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"the same bass line, \ two seats", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The room's response from a bass speaker in one corner, <bookmark mark='a'/> heard in the opposite corner, where "
            "every mode is at an antinode: tall peaks, twenty decibels and more above the dips. <bookmark mark='b'/> And heard "
            "in the middle of the room, which sits on a node of every mode with an odd number along any wall: the first modes "
            "are simply missing. Hear a plucked bass line from Part 38, in the corner, then in the middle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(note), FadeIn(ghost(VGroup(cc, cm), 0.25)))
            vo.wait_until("a")
            self.play(Create(cc), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cm), FadeIn(key[1]), run_time=1.5)
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a corner, \ then the middle", kind="physical model", detail=r"Part 38's bass, \ a simulated room", corner=DL, tag_corner=DR)
            pulse(snd, VGroup(cc, key[0]), st["corner"], st["middle"] - 0.3, buff=0.06)
            pulse(snd, VGroup(cm, key[1]), st["middle"], c.duration, buff=0.06)
        with self.voiceover(
            "In the corner some notes boom and hang on; in the middle the line is thin, and its lowest notes are nearly gone. "
            "Same room, same bass, a few metres apart."
        ):
            self.play(Indicate(cc, color=EAR, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fixes(self):
        items = [
            (r"move the listener and the loudspeaker: \ away from the room's halfway and third-way planes, \ out of the corners", WHITE),
            (r"bass traps: \ thick absorbers or tuned panels in the corners, \ where ideal rigid-box pressure modes have antinodes; porous and pressure absorbers exploit different parts of the field", WHITE),
            (r"several subwoofers, \ placed so that they drive the modes against each other \ (Welti, \ 2002)", WHITE),
            (r"equalization can cut a peak, \ but cannot fill a node: \ no amount of power reaches a place where the mode is silent", TUNE),
            (r"and small rooms remain modal: \ the bass of a living room is never a hall's", GREY_A),
        ]
        rows_scene(self, r"taming the modes", items,
                   "What can be done? <bookmark mark='b'/> Move the listener and the loudspeaker, away from the planes halfway and "
                   "a third of the way across the room, and out of the corners. <bookmark mark='c'/> Put bass traps, thick absorbers "
                   "or tuned panels, in the corners, where ideal rigid-box pressure modes have antinodes; porous and pressure absorbers exploit different parts of the field. <bookmark mark='d'/> Use several subwoofers, placed "
                   "so that they drive the modes against each other, as Todd Welti showed in 2002. <bookmark mark='e'/> "
                   "Equalization can cut a peak, but it cannot fill a node: no amount of power reaches a place where a mode is "
                   "silent. <bookmark mark='f'/> And small rooms remain modal: the bass of a living room is never a hall's.", marks="bcdef")
