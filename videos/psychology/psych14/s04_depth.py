from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


class Depth(VoiceoverScene):
    def construct(self):
        self.card()
        self.geometry()
        self.falloff()
        self.wheatstone()
        self.stereogram()
        self.monocular()

    def card(self):
        card = chapter_card(3, r"Depth from two eyes", r"How does a flat image give a third dimension?",
                            lit={1838: r"Wheatstone", 1960: r"Julesz"}, part=PART, scale=("mind", "circuit"),
                            marr=("what", "how"))
        with self.voiceover("Chapter three. Depth from two eyes."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def geometry(self):
        head = heading(r"Two eyes, \ two images")
        L, R = np.array([-0.7, -2.6, 0]), np.array([0.7, -2.6, 0])
        F = np.array([0.0, 2.4, 0])
        N = np.array([0.0, 0.9, 0])
        eyes = VGroup(*[Circle(radius=0.25, color=GREY_B, stroke_width=3).move_to(p) for p in (L, R)])
        lf = VGroup(Line(L, F, color=WORLD, stroke_width=2.5), Line(R, F, color=WORLD, stroke_width=2.5))
        ln = VGroup(Line(L, N, color=LIKE, stroke_width=2.5), Line(R, N, color=LIKE, stroke_width=2.5))
        dF = Dot(F, color=WORLD, radius=0.09)
        dN = Dot(N, color=LIKE, radius=0.09)
        aF = Angle(Line(F, L), Line(F, R), radius=0.6, color=WORLD)
        aN = Angle(Line(N, L), Line(N, R), radius=0.45, color=LIKE)
        geo = VGroup(eyes, lf, ln, dF, dN, aF, aN).move_to([-4.2, -0.3, 0])
        fl = label(r"fixated, \ distance $d$", font_size=22, color=WORLD).next_to(geo[3], RIGHT, buff=0.15)
        nl = label(r"nearer by $\Delta d$", font_size=22, color=LIKE).next_to(geo[4], RIGHT, buff=0.15)
        il = label(r"$I$", font_size=24, color=GREY_B).next_to(geo[0], DOWN, buff=0.12)
        eqs = VGroup(
            MathTex(r"\theta(d) = 2\arctan\frac{I}{2d} \approx \frac{I}{d}", font_size=40),
            MathTex(r"\delta = \theta(d - \Delta d) - \theta(d) \approx \frac{I\,\Delta d}{d^{2}}", font_size=40,
                    color=LIKE),
            MathTex(r"I \approx 6.3\ \text{cm}", font_size=34, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([2.7, 1.0, 0])
        rows = rows_of([
            (r"the disparity $\delta$ is the difference between the two eyes' angles", WHITE),
            (r"it falls with the square of distance: \ a stereo system is a near-field instrument", POST),
        ], 6.4, 27, 0.3).move_to([2.9, -2.0, 0])
        keep_in_frame(rows)
        tag = note(r"geometry, \ drawn to no scale").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Your two eyes are about six point three centimetres apart, so they see the world from slightly "
            "different places. <bookmark mark='a'/> Look at a point at distance d. The lines of sight from the two "
            "eyes meet there at an angle theta, which is two times the arctangent of I over two d, and for distances "
            "much larger than the gap between the eyes that's simply I over d. <bookmark mark='b'/> Now a second point, "
            "nearer by delta d. Its angle is a little larger. The difference between the two angles is the binocular "
            "disparity, and differentiating I over d gives it: I times delta d, over d squared. "
            "<bookmark mark='c'/> Disparity is the difference between where a point falls in the two eyes, relative "
            "to the point you're looking at. <bookmark mark='d'/> And it falls with the square of distance. Double "
            "the distance, and the same step in depth gives a quarter of the disparity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(geo[0]), FadeIn(il), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(geo[1]), FadeIn(geo[3]), FadeIn(geo[5]), FadeIn(fl), FadeIn(eqs[0]), FadeIn(eqs[2]))
            vo.wait_until("b")
            self.play(Create(geo[2]), FadeIn(geo[4]), FadeIn(geo[6]), FadeIn(nl), FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def falloff(self):
        d = load("depth")
        head = heading(r"One centimetre of depth, \ at different distances")
        A = axes([0, 10], [-2, 1.2], x_length=7.0, y_length=4.2, xticks=[0, 2, 4, 6, 8, 10],
                 yticks=[-2, -1, 0, 1], yfmt=lambda v: rf"10^{{{int(v)}}}", xlabel=r"distance (m)",
                 ylabel=r"disparity (arcmin)", center=[-2.6, -0.3, 0])
        ax = A.ax
        keep = d["d"] >= 0.4
        line = curve_in(ax, d["d"][keep], np.log10(d["disp"][keep]), LIKE, stroke_width=4)
        lim = DashedLine(ax.c2p(0, np.log10(10 / 60)), ax.c2p(10, np.log10(10 / 60)), color=GREY_B, stroke_width=2)
        lim_l = label(r"a good observer's threshold, \ about 10 arcsec", font_size=20, color=GREY_B)
        lim_l.next_to(lim, UP, buff=0.08).align_to(lim, RIGHT)
        pts = VGroup()
        for x, v in ((0.5, d["at_half"]), (2.0, d["at_two"]), (10.0, d["at_ten"])):
            pts.add(Dot(ax.c2p(x, np.log10(v)), color=WORLD, radius=0.07))
        rows = rows_of([
            (rf"at 0.5 m: \ {d['at_half']:.1f}$'$", WORLD),
            (rf"at 2 m: \ {d['at_two']:.2f}$'$", WORLD),
            (rf"at 10 m: \ {d['at_ten']:.3f}$'$, \ or {60 * d['at_ten']:.1f}$''$", WORLD),
            (r"the best observers see disparities of a few seconds of arc", WHITE),
            (r"beyond a few tens of metres, \ depth must come from other cues", PRIOR),
        ], 4.6, 27, 0.32).move_to([4.6, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ $\delta = I\,\Delta d / d(d + \Delta d)$, \ $I$ = 6.3 cm, \ $\Delta d$ = 1 cm")
        with self.voiceover(
            "Here's that square law for one centimetre of depth. The vertical axis is logarithmic. "
            "<bookmark mark='a'/> At half a metre, about arm's length, one centimetre of depth gives eight and a half "
            "minutes of arc of disparity. At two metres, about half a minute. At ten metres, two hundredths of a "
            "minute: just over one second of arc. <bookmark mark='b'/> The best observers can detect disparities of a "
            "few seconds of arc, finer than the spacing of the cones in the fovea, which is about half a minute. "
            "It's one of the hyperacuities: the brain compares positions across many receptors, and does better than "
            "any one of them. <bookmark mark='c'/> Even so, beyond a few tens of metres two eyes stop helping much, and "
            "depth has to come from other cues."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), Create(line))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.6), FadeIn(rows[0]), FadeIn(rows[1]),
                      FadeIn(rows[2]), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(lim), FadeIn(lim_l), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def wheatstone(self):
        head = heading(r"Wheatstone's stereoscope, \ 1838")
        mL = Line([-0.7, 0.7, 0], [0, 0, 0], color=GREY_A, stroke_width=6)
        mR = Line([0.7, 0.7, 0], [0, 0, 0], color=GREY_A, stroke_width=6)
        picL = Rectangle(width=0.12, height=1.4, fill_color=VISION, fill_opacity=1, stroke_width=0).move_to([-3.0, 0.3, 0])
        picR = picL.copy().move_to([3.0, 0.3, 0])
        eL, eR = Dot([-0.35, -2.2, 0], color=GREY_B, radius=0.12), Dot([0.35, -2.2, 0], color=GREY_B, radius=0.12)
        rayL = VGroup(Line(picL.get_center(), [-0.35, 0.35, 0], color=VISION, stroke_width=2),
                      Line([-0.35, 0.35, 0], eL.get_center(), color=VISION, stroke_width=2))
        rayR = VGroup(Line(picR.get_center(), [0.35, 0.35, 0], color=VISION, stroke_width=2),
                      Line([0.35, 0.35, 0], eR.get_center(), color=VISION, stroke_width=2))
        dev = VGroup(mL, mR, picL, picR, eL, eR, rayL, rayR).move_to([-3.0, -0.2, 0])
        ml = label(r"two mirrors", font_size=22, color=GREY_A).next_to(dev[0], UP, buff=0.5).shift(RIGHT * 0.7)
        pl = label(r"left picture", font_size=22, color=VISION).next_to(dev[2], DOWN, buff=0.15)
        pr = label(r"right picture", font_size=22, color=VISION).next_to(dev[3], DOWN, buff=0.15)
        rows = rows_of([
            (r"each eye sees its own drawing, \ made from its own viewpoint", WHITE),
            (r"the two flat drawings fuse into one solid object", POST),
            (r"so disparity alone is enough for depth: \ nothing else in the drawings is in depth", LIKE),
        ], 5.4, 27, 0.34).move_to([3.8, -0.2, 0])
        keep_in_frame(rows)
        tag = historical_tag(rf"{archive.WHEATSTONE_1838.cite}, \ redrawn", corner=DR)
        with self.voiceover(
            "That disparity alone can make depth was shown by Charles Wheatstone, a physicist, to the Royal Society in "
            "June 1838. <bookmark mark='a'/> His stereoscope used two mirrors at right angles, so that each eye saw "
            "its own drawing, each drawn from that eye's position. <bookmark mark='b'/> Two flat line drawings of a "
            "cube or a pyramid fused into one solid object, standing out in depth. <bookmark mark='c'/> Nothing else "
            "in the drawings had depth in it: no shading, no perspective that the other drawing lacked. The only "
            "difference between the pictures was the disparity. And within twenty years, stereoscopes and stereo "
            "photographs were a craze in Victorian parlours."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dev[:6]), FadeIn(ml), FadeIn(pl), FadeIn(pr), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(dev[6]), Create(dev[7]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def stereogram(self):
        d = load("depth")
        head = heading(r"On you: \ a square made only of disparity")
        left = picture(d["left"], 3.6).move_to([-2.3, 0.6, 0])
        right = picture(d["right"], 3.6).move_to([2.3, 0.6, 0])
        ll = label(r"left eye", font_size=24, color=GREY_B).next_to(left, UP, buff=0.12)
        rl = label(r"right eye", font_size=24, color=GREY_B).next_to(right, UP, buff=0.12)
        rows = rows_of([
            (r"each picture alone is random dots: \ no square in either", WHITE),
            (r"cross your eyes until the two pictures become three; \ in the middle one, \ a square floats", YOU),
            (r"Julesz, \ 1960: \ depth comes before shape, \ not after", POST),
        ], 12.4, 27, 0.28).to_edge(DOWN, buff=0.9)
        tag = VGroup(psyche_tag(r"computed: \ a random-dot stereogram, \ a square shifted 6 dots"),
                     historical_tag(archive.WHEATSTONE_1838.cite, corner=DL))
        with self.voiceover(
            "Here's a test you can take. <bookmark mark='a'/> These are two pictures of random dots. Look at either "
            "one: there's no shape in it at all. But in the right picture, a square patch of the left picture's dots "
            "has been shifted six dots sideways, and the gap filled with fresh random dots. "
            "<bookmark mark='b'/> If you can, cross your eyes slightly, so the two pictures slide over each other and "
            "become three. Hold the middle one steady, and wait. For most people with working stereo vision, after a "
            "few seconds, a square appears, floating in front of or behind the rest. If it doesn't work for you, "
            "you're not alone: several people in every hundred have little or no stereo vision. "
            "<bookmark mark='c'/> Bela Julesz, an engineer at Bell Labs, made these in 1960. They proved that the brain "
            "can find depth before it has found any shape: there's no shape to find in either eye's image. It has to "
            "match dots between the two eyes, which is a hard problem, since every dot looks like every other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(right), FadeIn(ll), FadeIn(rl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            self.wait(4.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def monocular(self):
        head = heading(r"Depth with one eye")
        # a texture gradient: rows of ellipses shrinking toward a horizon
        tex = VGroup()
        for k in range(9):
            y = -2.6 + 3.2 * (1 - 0.8 ** k)
            s = 0.8 ** k
            for i in range(-5, 6):
                tex.add(Ellipse(width=0.42 * s, height=0.16 * s, color=GREY_B, stroke_width=1.5).move_to(
                    [-3.6 + i * 0.55 * s, y, 0]))
        tex.move_to([-3.6, 0.1, 0])
        tl = label(r"a texture gradient", font_size=24, color=GREY_B).next_to(tex, DOWN, buff=0.2)
        cues = [
            (r"occlusion: \ what hides is nearer", WHITE),
            (r"size and texture gradients: \ the same things, \ smaller and denser, \ are further", WHITE),
            (r"perspective: \ parallel lines meet at the horizon", WHITE),
            (r"shading, \ and haze over distance", WHITE),
            (r"motion parallax: \ near things sweep past faster as you move", LIKE),
            (r"vergence and focus: \ how the eyes turn and focus, \ useful within a few metres", LIKE),
        ]
        rows = rows_of(cues, 6.2, 26, 0.3).move_to([3.4, 0.0, 0])
        keep_in_frame(rows)
        ask = label(r"many cues, \ none certain: \ how should they be combined?", font_size=28, color=PRIOR)
        ask = wrapped_label(r"many cues, \ none certain: \ how should they be combined?", 6.2, 28, PRIOR)
        ask.next_to(rows, DOWN, buff=0.45).align_to(rows, LEFT)
        tag = note(r"drawn").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Close one eye, and the world doesn't go flat. <bookmark mark='a'/> There are many cues to depth in a "
            "single image. What hides something is nearer than what it hides. Things of the same size look smaller "
            "and their textures denser as they get further away, like these ellipses. Parallel lines meet at the "
            "horizon. Shading gives shape, and distant things are hazier. <bookmark mark='b'/> And moving gives you "
            "more: as your head moves, near things sweep past faster than far ones. Within a few metres, how your "
            "eyes turn inward and how they focus also tell the brain how far away something is. "
            "<bookmark mark='c'/> None of these cues is certain. Each can be faked, as painters have known for five "
            "centuries. So the visual system has many uncertain cues, and a question that is mathematical: how should "
            "they be combined? We'll answer it in chapter six."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tex), FadeIn(tl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:4]], lag_ratio=0.7), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
            vo.wait_until("c")
            self.play(FadeIn(ask))
        self.clear_scene()
