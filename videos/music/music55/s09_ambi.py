from __future__ import annotations

import math

import numpy as np

from videos.music.music55.common import *  # noqa: F403


class Ambi(SoundScene):
    def construct(self):
        chapter(self, 8, r"Ambisonics and wave-field synthesis", r"Can we record the sound at a point, \ and rebuild it in a room?")
        self.quad()
        self.encode()
        self.decode()
        self.vectors()
        self.orders()
        self.wfs()

    # ------------------------------------------------------------------
    def quad(self):
        items = [
            (r"the 1970s: \ quadraphonic records, \ four loudspeakers, \ three incompatible formats, \ and a commercial failure", WHITE),
            (r"Michael Gerzon and Peter Fellgett, \ at Oxford: \ forget the loudspeakers; \ record the sound field at a point", WHITE),
            (r"to first order, \ a field at a point is four numbers: \ its pressure $W$ and its gradient $X$, \ $Y$, \ $Z$", WHITE),
            (r"the Soundfield microphone \ (Gerzon and Craven, \ 1975): \ four capsules on a tetrahedron, \ summed into $W$, \ $X$, \ $Y$, \ $Z$", WHITE),
            (r"Ambisonics: \ the recording knows nothing of the loudspeakers; \ a decoder is designed for each layout", TUNE),
        ]
        rows_scene(self, r"after quadraphony", items,
                   "In the 1970s the record industry tried four loudspeakers. <bookmark mark='b'/> Quadraphonic records came in "
                   "three incompatible formats, and failed. <bookmark mark='c'/> Michael Gerzon and Peter Fellgett, at Oxford, "
                   "proposed something better: forget the loudspeakers, and record the sound field at a point. "
                   "<bookmark mark='d'/> To first order, the field at a point is four numbers: its pressure, W, and its gradient in "
                   "three directions, X, Y and Z, which are an omni and three figure-8 microphones. <bookmark mark='e'/> Gerzon and "
                   "Peter Craven's Soundfield microphone of 1975 has four capsules on a tetrahedron, whose outputs sum into W, X, Y "
                   "and Z. <bookmark mark='f'/> That is Ambisonics: the recording knows nothing about the loudspeakers, and a "
                   "decoder is designed for whatever layout there is.", marks="bcdef")

    # ------------------------------------------------------------------
    def encode(self):
        eqs = VGroup(MathTex(r"W = s", font_size=36), MathTex(r"X = s\cos\theta", font_size=36), MathTex(r"Y = s\sin\theta", font_size=36)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(LEFT * 4.0 + DOWN * 0.2)
        R = 1.25
        cen = RIGHT * 2.2 + DOWN * 0.2
        th = np.linspace(0, 2 * np.pi, 121)
        omni = Circle(radius=R * 0.5, stroke_color=GREY_A, stroke_width=3).move_to(cen)

        def lobe(fn, col):
            pts = [cen + R * abs(fn(t)) * np.array([math.sin(t), math.cos(t), 0]) for t in th]
            return VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts)

        X = lobe(math.cos, TUNE)
        Y = lobe(math.sin, BLUE)
        key = VGroup(label(r"$W$: \ an omni", font_size=17, color=GREY_A), label(r"$X$: \ a figure-8 facing front", font_size=17, color=TUNE),
                     label(r"$Y$: \ a figure-8 facing left", font_size=17, color=BLUE)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(cen, RIGHT, buff=1.6)
        note = label(r"a source $s$ at angle $\theta$, \ horizontally: \ three channels, \ B-format", font_size=18, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"encoding a direction", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Encoding is three lines, if we keep to the horizontal. <bookmark mark='a'/> A sound s arriving from angle theta "
            "puts s in W, the omni. <bookmark mark='b'/> It puts s cosine theta into X, a figure-8 facing the front, "
            "<bookmark mark='c'/> and s sine theta into Y, a figure-8 facing the left. These three channels are B-format. A "
            "microphone makes them from a real field; a mixer makes them by formula, to place a sound anywhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note), FadeIn(ghost(VGroup(omni, X, Y), 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]), Create(omni), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), Create(X), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]), Create(Y), FadeIn(key[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decode(self):
        d = load("ambi")
        cen = DOWN * 0.3 + LEFT * 2.4
        R = 2.0
        sp = VGroup()
        bars = VGroup()
        for ang, g in zip(d["speakers_deg"], d["gains20"]):
            a = math.radians(ang)
            u = np.array([-math.sin(a), math.cos(a), 0])
            sp.add(Square(side_length=0.3, stroke_color=GREY_B, stroke_width=2.5).move_to(cen + R * u))
            L = 2.4 * abs(g)
            col = TUNE if g >= 0 else BLUE
            bars.add(Line(cen + (R + 0.25) * u, cen + (R + 0.25 + max(L, 0.02)) * u, color=col, stroke_width=8))
        a20 = math.radians(20)
        src = Dot(cen + 1.1 * np.array([-math.sin(a20), math.cos(a20), 0]), radius=0.11, color=EAR)
        sl = label(r"source at 20$^\circ$", font_size=15, color=EAR).next_to(src, UP, buff=0.08)
        lis = Dot(cen, radius=0.08, color=WHITE)
        eq = MathTex(r"g_i = \frac{1}{N}\bigl(W + 2X\cos\phi_i + 2Y\sin\phi_i\bigr)", font_size=32, color=TUNE).move_to(RIGHT * 3.6 + UP * 1.2)
        items = text_rows([(r"eight loudspeakers in a ring", WHITE), (r"the nearest play loudest", WHITE),
                           (r"the far side plays inverted \ (blue): \ its job is to cancel", BLUE), (r"the field at the centre is exactly the source's", TUNE)], font_size=19, width=5.0).move_to(RIGHT * 3.6 + DOWN * 0.9)
        head = label(r"decoding to a ring", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Decoding asks: what should each loudspeaker play, so that the field at the centre has the right W, X and Y? "
            "<bookmark mark='a'/> For a ring of N, the answer is this: each loudspeaker plays W plus twice the gradient "
            "pointing its way, over N. <bookmark mark='b'/> For a source at twenty degrees, the nearest loudspeakers play "
            "loudest, the side ones less, <bookmark mark='c'/> and the far side plays a little, inverted, shown in blue: its job "
            "is to cancel the near side's sound where it should not be. <bookmark mark='d'/> At the very centre the pressure "
            "and its gradient are exactly the source's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sp), FadeIn(lis), FadeIn(src), FadeIn(sl), FadeIn(ghost(bars, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(items[0]))
            vo.wait_until("b")
            self.play(*[Create(bars[i]) for i in (0, 1, 7, 2, 6)], FadeIn(items[1]))
            vo.wait_until("c")
            self.play(*[Create(bars[i]) for i in (3, 4, 5)], FadeIn(items[2]))
            vo.wait_until("d")
            self.play(FadeIn(items[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vectors(self):
        d = load("ambi")
        th = np.array(d["theta"])
        ax = frame_axes(width=8.4, height=2.8, xlo=0, xhi=360, ylo=0, yhi=1.1, center=DOWN * 0.4 + LEFT * 0.6)
        cs = VGroup(curve(th, d["res"]["basic"]["rV"], ax.to, color=GREY_A, width=3), curve(th, d["res"]["basic"]["rE"], ax.to, color=TUNE, width=3),
                    curve(th, d["res"]["maxre"]["rE"], ax.to, color=EAR, width=3))
        one = DashedLine(ax.to(0, 1.0), ax.to(360, 1.0), color=GREY_D, stroke_width=1.5)
        xt = VGroup(*[label(f"{v}$^\\circ$", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (0, 90, 180, 270, 360)])
        yt = VGroup(*[label(f"{v:g}", font_size=14, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        key = VGroup(label(r"$|r_V|$, \ basic decoder", font_size=16, color=GREY_A), label(r"$|r_E|$, \ basic decoder", font_size=16, color=TUNE),
                     label(r"$|r_E|$, \ max-$r_E$ decoder", font_size=16, color=EAR)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        eq = MathTex(r"\mathbf{r}_V = \frac{\sum g_i \mathbf{u}_i}{\sum g_i}, \qquad \mathbf{r}_E = \frac{\sum g_i^2 \mathbf{u}_i}{\sum g_i^2}", font_size=32).to_edge(UP, buff=1.0)
        b = d["res"]["basic"]["rE"][0]
        m = d["res"]["maxre"]["rE"][0]
        note = label(rf"a real source has length 1; \ the basic decoder's energy vector {b:.3f}, \ max-$r_E$'s {m:.3f}: \ the same in every direction", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"Gerzon's vectors", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How good is the illusion? Gerzon gave two measures. <bookmark mark='a'/> The velocity vector, the gains times the "
            "loudspeakers' directions, over the gains: it predicts the direction heard at low frequencies, where the ears read "
            "time. The energy vector does the same with squared gains, for high frequencies, where they read level. A single "
            "real source has both of length one. <bookmark mark='b'/> The basic decoder gets the velocity vector perfect, "
            f"length one in every direction, but its energy vector is only {say(b, 2)} long: the treble sounds blurred, "
            "spread over the ring. <bookmark mark='c'/> A max-r E decoder trades one for the other, raising the energy vector "
            f"to {say(m, 2)}. Better decoders use one design for the bass and another for the treble."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(one), FadeIn(xt), FadeIn(yt), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(Create(cs[0]), Create(cs[1]), FadeIn(key[0]), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(cs[2]), FadeIn(key[2]), FadeIn(note), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def orders(self):
        d = load("ambi")
        rows = VGroup(VGroup(label(r"order $N$", font_size=17, color=GREY_A), label(r"channels, \ ring", font_size=17, color=GREY_A), label(r"channels, \ sphere", font_size=17, color=GREY_A),
                             label(r"$|r_E|$", font_size=17, color=GREY_A), label(r"spread", font_size=17, color=GREY_A)))
        for k in ("1", "2", "3", "5", "7"):
            N = int(k)
            rows.add(VGroup(label(k, font_size=19, color=WHITE), label(f"{2 * N + 1}", font_size=19, color=WHITE), label(f"{(N + 1) ** 2}", font_size=19, color=WHITE),
                            label(f"{d['orders_rE'][k]:.3f}", font_size=19, color=TUNE), label(rf"{d['spread_deg'][k]:.1f}$^\circ$", font_size=19, color=TUNE)))
        rows.arrange(DOWN, buff=0.24)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.8 + 2.4 * i)
        rows.move_to(DOWN * 0.1)
        eq = MathTex(r"|r_E| = \cos\frac{\pi}{2N + 2} \quad (\text{max-}r_E\text{, a ring})", font_size=30, color=TUNE).to_edge(UP, buff=1.0)
        note = label(r"higher orders: \ more spherical harmonics, \ a sharper image, \ a wider sweet spot; \ third order is common in virtual reality", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"higher orders", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "First order is blurry because four channels can only hold a blurry picture. <bookmark mark='a'/> Higher-order "
            "Ambisonics adds more terms of the field's expansion in circular or spherical harmonics: two N plus one channels for "
            "a ring, N plus one squared for a sphere. <bookmark mark='b'/> With the max-r E decoder the energy vector grows as "
            "cosine of pi over two N plus two, and the image's spread, its arc cosine, shrinks: forty-five degrees at first "
            "order, twenty-two and a half at third, eleven at seventh. The sweet spot widens too. Third order, sixteen channels, "
            "is the common choice for virtual reality."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(eq), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wfs(self):
        n = 17
        xs = np.linspace(-4.0, 4.0, n)
        y0 = -0.9
        vs = np.array([0.0, -2.9])
        R0 = 4.9
        sp = VGroup(*[Square(side_length=0.22, stroke_color=GREY_B, stroke_width=2).move_to([x, y0, 0]) for x in xs])
        circles = VGroup()
        for x in xs:
            dist = math.hypot(x - vs[0], y0 - vs[1])
            r = R0 - dist
            if r > 0.05:
                circles.add(Arc(radius=r, start_angle=math.radians(5), angle=math.radians(170), arc_center=[x, y0, 0], stroke_color=BLUE, stroke_width=1.5, stroke_opacity=0.7))
        target = Arc(radius=R0, start_angle=math.radians(52), angle=math.radians(76), arc_center=[vs[0], vs[1], 0], stroke_color=TUNE, stroke_width=4)
        vdot = Dot([vs[0], vs[1], 0], radius=0.1, color=EAR)
        vl = label(r"virtual source, \ behind the loudspeakers", font_size=15, color=EAR).next_to(vdot, RIGHT, buff=0.15)
        note = label(r"Berkhout \ (Delft, \ 1988): \ each loudspeaker plays the wave as it would arrive there; \ their wavelets add up to the source's wavefront \ (Huygens)",
                     font_size=17, color=WHITE).to_edge(DOWN, buff=0.25)
        alias = label(r"above $c/2\Delta x$ the wavefront breaks up: \ 17 cm spacing, \ 1 kHz", font_size=17, color=GREY_A).to_edge(UP, buff=1.0)
        head = label(r"wave-field synthesis", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "There is another way to rebuild a field, without a sweet spot at all. <bookmark mark='a'/> Christiaan Huygens said "
            "that every point on a wavefront acts as a new source of wavelets. Guus Berkhout, at Delft in 1988, turned it "
            "round: put a line of loudspeakers where the wave would pass, and have each play the wave as it would arrive there, "
            "delayed and weighted. <bookmark mark='b'/> Their wavelets add up to the wavefront of a virtual source behind the "
            "line, and everyone in front hears it in the same place. <bookmark mark='c'/> The price is loudspeakers: above c "
            "over twice their spacing the wavefront breaks up, so seventeen-centimetre spacing works up to one kilohertz, and "
            "an installation needs hundreds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sp), FadeIn(vdot), FadeIn(vl), FadeIn(ghost(VGroup(circles, target), 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in circles], lag_ratio=0.05), FadeIn(note), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(target), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(alias))
        self.wait(0.4)
        self.clear_scene()
