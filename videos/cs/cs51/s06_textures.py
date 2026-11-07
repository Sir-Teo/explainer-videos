from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, image, load


def checker_levels(n: int = 128, check: int = 16, lo: float = 0.1, hi: float = 0.9) -> list[np.ndarray]:
    """The texture of the floor (an n x n checkerboard of ``check``-texel squares) and its box-filtered pyramid, as
    uint8 images for display: each level the 2 x 2 average of the one before, as in Williams (1983)."""
    i = np.arange(n) // check
    t = np.where((i[:, None] + i[None, :]) % 2 == 0, hi, lo)
    levels = [t]
    while levels[-1].shape[0] > 1:
        a = levels[-1]
        levels.append(0.25 * (a[0::2, 0::2] + a[1::2, 0::2] + a[0::2, 1::2] + a[1::2, 1::2]))
    return [(np.clip(x, 0, 1) * 255 + 0.5).astype(np.uint8) for x in levels]


def lod_colours(lod: np.ndarray, top: float) -> np.ndarray:
    """The mip level at each pixel as colour: blue (level 0) through green to yellow (the coarsest level)."""
    stops = np.array([[0.04, 0.10, 0.30], [0.35, 0.60, 0.95], [0.40, 0.80, 0.45], [0.98, 0.85, 0.30]])
    x = np.clip(lod / top, 0, 1) * (len(stops) - 1)
    k = np.minimum(x.astype(int), len(stops) - 2)
    f = (x - k)[..., None]
    rgb = (1 - f) * stops[k] + f * stops[k + 1]
    return (rgb * 255 + 0.5).astype(np.uint8)


class Textures(VoiceoverScene):
    def construct(self):
        self.card()
        self.alias()
        self.floor()
        self.pyramid()
        self.level()
        self.aniso()
        self.msaa()

    def card(self):
        card = chapter_card(5, r"Textures and sampling", r"How do you draw a pattern finer than a pixel?",
                            lit=(1974, 1983), extra=((1974, r"Catmull: \ texture mapping"),
                                                     (1983, r"Williams: \ mipmaps")), part=PART)
        with self.voiceover("Chapter five. Textures and sampling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def alias(self):
        t = load("texture")
        head = label(r"Moir\'e is aliasing", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 1, 0.1], y_range=[-1.3, 1.3, 1], x_length=6.2, y_length=2.4,
                  axis_config={"color": GREY_D, "include_ticks": False}).move_to([-3.4, 1.15, 0])
        fast = ax.plot(lambda x: math.sin(2 * PI * 9 * x), x_range=[0, 1, 0.002], color=GREY_B, stroke_width=2)
        dots = VGroup(*[Dot(ax.c2p(k / 10, math.sin(2 * PI * 9 * k / 10)), radius=0.07, color=HEAD)
                        for k in range(11)])
        slow = ax.plot(lambda x: -math.sin(2 * PI * x), x_range=[0, 1, 0.01], color=NO, stroke_width=4)
        leg = VGroup(label(r"9 cycles", font_size=19, color=GREY_B), label(r"10 samples", font_size=19, color=HEAD),
                     label(r"what the samples say: \ 1 cycle", font_size=19, color=NO)).arrange(RIGHT, buff=0.4)
        leg.next_to(ax, DOWN, buff=0.2)
        ill = note(r"illustrative", font_size=16).next_to(ax, UP, buff=0.05).align_to(ax, RIGHT)
        rows = VGroup(
            MathTex(r"f", r"\;\longrightarrow\;", r"|f - k f_s|", font_size=34),
            MathTex(r"9", r"\;\longrightarrow\;", r"|9 - 10| = 1", font_size=34),
            MathTex(r"f_s > 2 f_{\max}", font_size=34, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.35).align_to(ax, LEFT).shift(
            RIGHT * 0.4)
        whys = VGroup(note(r"shifted by any multiple of the rate", font_size=16),
                      note(r"here", font_size=16),
                      note(r"Nyquist \ (Part 36): \ more than two samples per cycle", font_size=16, color=YES))
        for r, w in zip(rows, whys):
            w.next_to(r, RIGHT, buff=0.3)
        img = image(t["point"], height=3.0).move_to([3.9, 0.9, 0])
        cap = wrapped_label(r"our rasterizer: \ a checkered floor, \ one texel looked up at each pixel centre", 4.2,
                            font_size=18, color=GREY_A).next_to(img, DOWN, buff=0.15)
        far = wrapped_label(r"near the horizon a pixel spans many squares: \ the samples fall into false curves", 4.2,
                            font_size=18, color=NO).next_to(cap, DOWN, buff=0.2)
        with self.voiceover(
            "A texture is a picture glued onto a surface, Ed Catmull's idea of 1974. Looking it up is "
            "sampling, and sampling has a trap. <bookmark mark='a'/> A wave of nine cycles, sampled ten times. "
            "<bookmark mark='b'/> Join the samples and they trace a wave of one cycle, going the wrong way: an "
            "alias. <bookmark mark='c'/> A frequency f, sampled at a rate f s, is indistinguishable from f minus any "
            "multiple of f s. <bookmark mark='d'/> To be safe, take more than two samples per cycle, Nyquist's rule "
            "from Part 36. <bookmark mark='e'/> Our rasterizer looks up one texel at each pixel's centre. Near the "
            "horizon each pixel spans many squares, far beyond the Nyquist limit, and the samples draw curves that "
            "are not there: moiré."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(fast), FadeIn(leg[0]), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.1), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(Create(slow), FadeIn(leg[2]), fast.animate.set_stroke(opacity=0.35), run_time=1.5)
            vo.wait_until("c")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(FadeIn(img), FadeIn(cap))
            self.play(FadeIn(far))
        self.wait(0.4)
        self.clear_scene()

    def floor(self):
        t = load("texture")
        e = t["rmse"]
        head = label(r"One floor, \ four samplers", font_size=36).to_edge(UP, buff=0.3)
        spec = (("point", r"point sampling", r"1 texel per pixel", NO, e["point"]),
                ("mip", r"trilinear mipmap", r"8 texels per pixel", YES, e["mip"]),
                ("ss16", r"16 samples per pixel", r"16 texels per pixel", HEAD, e["ss16"]),
                ("reference", r"reference", r"256 jittered samples", GREY_A, None))
        cols = Group()
        for k, name, cost, c, err in spec:
            im = image(t[k], height=2.25)
            a = label(name, font_size=20, color=c)
            b = label(cost, font_size=17, color=GREY_B)
            d = label(rf"error {err:.3f}" if err is not None else r"the truth, \ nearly", font_size=19, color=c)
            cols.add(Group(im, VGroup(a, b, d).arrange(DOWN, buff=0.1)).arrange(DOWN, buff=0.15))
        cols.arrange(RIGHT, buff=0.3, aligned_edge=UP).next_to(head, DOWN, buff=0.45)
        notes = VGroup(
            wrapped_label(r"error: \ root-mean-square difference from the reference, \ brightness on a scale of 0 to "
                          rf"1, \ over all {t['pixels']:,} pixels".replace(",", "{,}"), 12.4, font_size=19,
                          color=WHITE),
            wrapped_label(rf"the mipmap cuts point sampling's error by a factor of "
                          rf"{e['point'] / e['mip']:.1f} for 8 texel reads; \ brute force needs twice that many to "
                          r"do a little better, \ and still shimmers at the horizon", 12.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Two cures: filter the texture before sampling, or take more samples. Here is the floor four ways, from "
            "our renderer. <bookmark mark='a'/> Point sampling: the moiré. <bookmark mark='b'/> The reference: "
            "two hundred and fifty-six jittered samples per pixel, averaged. <bookmark mark='c'/> Against it, point "
            "sampling is off by about a fifth of full brightness. <bookmark mark='d'/> A trilinear mipmap reads eight "
            "texels per pixel and cuts that error by a factor of three. <bookmark mark='e'/> Sixteen samples per "
            "pixel do slightly better, at twice the reads, and the far rows still shimmer. The cheap winner is the "
            "prefiltered texture."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols[0][0]), FadeIn(cols[0][1][:2]))
            vo.wait_until("b")
            self.play(FadeIn(cols[3]))
            vo.wait_until("c")
            self.play(FadeIn(cols[0][1][2]), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(cols[1]))
            vo.wait_until("e")
            self.play(FadeIn(cols[2]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def pyramid(self):
        t = load("texture")
        py = t["pyramid"]
        head = label(r"Mipmaps: \ a pyramid of prefiltered textures", font_size=36).to_edge(UP, buff=0.3)
        lv = checker_levels(py["sizes"][0])
        tiles = Group()
        for k, (arr, s) in enumerate(zip(lv, py["sizes"])):
            im = image(arr, height=1.3)
            cap = label(rf"{s} $\times$ {s}", font_size=17, color=GREY_A).next_to(im, DOWN, buff=0.1)
            lk = label(rf"level {k}", font_size=17, color=HEAD).next_to(im, UP, buff=0.1)
            tiles.add(Group(lk, im, cap))
        tiles.arrange(RIGHT, buff=0.22).next_to(head, DOWN, buff=0.4)
        arrows = VGroup(*[Arrow(tiles[k][1].get_right(), tiles[k + 1][1].get_left(), buff=0.02, stroke_width=2,
                                color=GREY_B, max_tip_length_to_length_ratio=0.5) for k in range(len(tiles) - 1)])
        fil = MathTex(r"L_{k+1}[i, j] = \tfrac14\big(L_k[2i, 2j] + L_k[2i{+}1, 2j] + L_k[2i, 2j{+}1] + "
                      r"L_k[2i{+}1, 2j{+}1]\big)", font_size=30).next_to(tiles, DOWN, buff=0.45)
        rows = [MathTex(r"\text{extra memory}", r"=", r"\tfrac14 + \tfrac1{16} + \tfrac1{64} + \cdots", font_size=34),
                MathTex(r"\text{extra memory}", r"=", r"\frac{1/4}{1 - 1/4}", font_size=34),
                MathTex(r"\text{extra memory}", r"=", r"\frac{1}{3}", font_size=34)]
        for r in rows:
            r.next_to(fil, DOWN, buff=0.45).align_to(fil, LEFT).shift(RIGHT * 0.3)
        rows[2][2].set_color(YES)
        whys = [note(r"each level a quarter of the one before", font_size=17),
                note(r"a geometric series", font_size=17),
                note(r"a third more memory, \ for every level", font_size=17, color=YES)]
        for w in whys:
            w.next_to(rows[0], RIGHT, buff=0.5)
        tot = sum(py["texels"])
        ours = wrapped_label(rf"ours: \ {py['texels'][0]:,} texels at level 0, \ {tot:,} in all: \ "
                             rf"{100 * py['overhead']:.2f}\% more".replace(",", "{,}"), 12.4, font_size=19,
                             color=WHITE).to_edge(DOWN, buff=0.45)
        grey = note(r"from level 5 down, \ each texel averages a light and a dark square equally: \ grey",
                    font_size=17).next_to(ours, UP, buff=0.15)
        with self.voiceover(
            "In 1983 Lance Williams proposed filtering the texture in advance, at every scale. <bookmark mark='a'/> "
            "Level zero is the texture. Each next level averages two by two blocks of the one before: half the "
            "width, half the height. <bookmark mark='b'/> By level five each texel covers a light and a dark square "
            "equally, and the pattern has become its average grey. Williams called it a mip map, from multum in "
            "parvo, many things in a small place. <bookmark mark='c'/> The cost? Each level has a quarter of the "
            "texels of the one before. <bookmark mark='d'/> The extra memory is a geometric series, "
            "<bookmark mark='e'/> one third. <bookmark mark='f'/> Our sixteen thousand texels become twenty-two "
            "thousand."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tiles[0]))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(tl)) for a, tl in zip(arrows, tiles[1:])],
                                  lag_ratio=0.4), run_time=3)
            self.play(Write(fil))
            vo.wait_until("b")
            self.play(FadeIn(grey), Create(SurroundingRectangle(Group(*tiles[5:]), color=HEAD, buff=0.08)))
            vo.wait_until("c")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[0], rows[1]), FadeTransform(whys[0], whys[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[1], rows[2]), FadeTransform(whys[1], whys[2]))
            vo.wait_until("f")
            self.play(FadeIn(ours))
        self.wait(0.4)
        self.clear_scene()

    def level(self):
        t = load("texture")
        lo, hi = t["lod_range"]
        head = label(r"Which level? \ Measure the pixel's footprint", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"\rho", r"=", r"\max\Big(\Big\lVert \frac{\partial (u, v)}{\partial x} \Big\rVert,\ "
                    r"\Big\lVert \frac{\partial (u, v)}{\partial y} \Big\rVert\Big)", font_size=32),
            MathTex(r"\lambda", r"=", r"\log_2 \rho", font_size=32),
            MathTex(r"c", r"=", r"(1 - f)\,\mathrm{bilinear}(L_{\lfloor\lambda\rfloor}) + "
                    r"f\,\mathrm{bilinear}(L_{\lfloor\lambda\rfloor + 1})", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([-3.2, 0.6, 0])
        rows[1][2].set_color(HEAD)
        whys = VGroup(note(r"texels crossed by one step to the next pixel", font_size=17),
                      note(r"$\rho = 1$: \ level 0; \ $\rho = 4$: \ level 2", font_size=17, color=HEAD),
                      note(r"$f = \lambda - \lfloor\lambda\rfloor$: \ blend two levels, \ 4 texels from each",
                           font_size=17, color=YES))
        for r, w in zip(rows, whys):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        img = image(lod_colours(t["lod"], hi), height=3.0).move_to([3.7, 0.75, 0])
        bar_img = image(lod_colours(np.tile(np.linspace(lo, hi, 64), (4, 1)), hi), height=0.22, nearest=False)
        bar_img.stretch_to_fit_width(img.width)
        bar_img.next_to(img, DOWN, buff=0.35)
        ticks = VGroup(*[label(rf"{v:g}", font_size=16, color=GREY_A).next_to(bar_img, DOWN, buff=0.08).set_x(
            bar_img.get_left()[0] + (v - lo) / (hi - lo) * bar_img.width) for v in range(int(lo), int(hi) + 1)])
        cap = wrapped_label(rf"the level $\lambda$ our renderer used at each pixel: \ {lo:g} at the bottom of the "
                            rf"frame, \ {hi:g} \ (the 1 $\times$ 1 grey) \ at the horizon", 4.3, font_size=18,
                            color=GREY_A).next_to(ticks, DOWN, buff=0.15)
        fwd = wrapped_label(r"a GPU gets the derivatives by differencing neighbouring pixels: \ the next chapter",
                            6.0, font_size=19, color=KERN).to_edge(DOWN, buff=0.4).set_x(-3.2)
        with self.voiceover(
            "Which level should a pixel read? The one whose texels match the pixel's footprint. <bookmark mark='a'/> "
            "Step one pixel right, or one down, and measure how far the texture coordinates move, in texels; call "
            "the larger rho. <bookmark mark='b'/> If a step crosses four texels, then two levels down a texel is four "
            "times wider: the level is the logarithm, base two, of rho. <bookmark mark='c'/> Lambda is rarely whole, "
            "so trilinear filtering reads the two nearest levels, four texels each, and blends them: the eight "
            "reads. <bookmark mark='d'/> Here is the level our renderer chose at each pixel: zero near the camera, "
            "rising to seven, the single grey texel, at the horizon. <bookmark mark='e'/> On real hardware the "
            "derivatives come from neighbouring pixels, as the next chapter shows."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(img), FadeIn(bar_img), FadeIn(ticks), FadeIn(cap))
            vo.wait_until("e")
            self.play(FadeIn(fwd))
        self.wait(0.4)
        self.clear_scene()

    def aniso(self):
        t = load("texture")
        head = label(r"Grazing angles: \ anisotropic filtering", font_size=36).to_edge(UP, buff=0.3)
        C = np.array([-3.6, 0.6, 0])
        grid = VGroup(*[Square(0.4, stroke_color=GREY_D, stroke_width=0.8).move_to(C + np.array([i * 0.4, j * 0.4,
                                                                                               0]))
                        for i in range(-6, 7) for j in range(-4, 5)])
        tl = label(r"texture space, \ one pixel's footprint", font_size=18, color=GREY_A).next_to(grid, UP,
                                                                                               buff=0.1)
        ang = 0.35
        ell = Ellipse(width=3.4, height=0.48, color=WHITE, stroke_width=3, fill_color=WHITE,
                      fill_opacity=0.12).move_to(C).rotate(ang)
        iso = Circle(radius=1.7, color=NO, stroke_width=3).move_to(C)
        axis_dir = np.array([math.cos(ang), math.sin(ang), 0])
        probes = VGroup(*[Circle(radius=0.23, color=YES, stroke_width=3).move_to(C + s * axis_dir)
                          for s in (-1.2, -0.4, 0.4, 1.2)])
        ill = note(r"illustrative", font_size=16).next_to(grid, DOWN, buff=0.1).align_to(grid, RIGHT)
        leg = VGroup(label(r"trilinear: \ one circle as wide as the long axis \ (blur)", font_size=18, color=NO),
                     label(r"anisotropic: \ $N$ probes along it, \ each as wide as the short axis", font_size=18,
                           color=YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(grid, DOWN, buff=0.45)
        leg.align_to(grid, LEFT)
        rows = VGroup(MathTex(r"N = \Big\lceil \frac{\rho_{\max}}{\rho_{\min}} \Big\rceil", font_size=32),
                      MathTex(r"\lambda = \log_2 \frac{\rho_{\max}}{N}", font_size=32)).arrange(RIGHT, buff=0.6)
        rows.next_to(leg, DOWN, buff=0.3).align_to(grid, LEFT)
        H = 60
        crops = Group(image(t["mip"][:H], height=1.55), image(t["reference"][:H], height=1.55)).arrange(
            DOWN, buff=0.55).move_to([3.9, 0.55, 0])
        cl = VGroup(label(r"trilinear mipmap, \ top half of the frame", font_size=18, color=NO).next_to(
            crops[0], UP, buff=0.08),
                    label(r"reference", font_size=18, color=GREY_A).next_to(crops[1], UP, buff=0.08))
        foot = wrapped_label(r"hardware takes up to 16 probes per pixel; \ the blur is the trilinear filter's fault, "
                             r"\ not the mipmap's", 5.4, font_size=18, color=WHITE).next_to(crops, DOWN, buff=0.3)
        with self.voiceover(
            "The mipmap has one flaw, and our floor shows it. <bookmark mark='a'/> At a grazing angle a square pixel "
            "lands on the texture as a long, thin footprint. <bookmark mark='b'/> Trilinear filtering uses one "
            "number, the larger derivative, so it filters a disc as wide as the long axis. <bookmark mark='c'/> "
            "Compare the top of our trilinear image with the reference: towards the horizon the squares have "
            "blurred into grey. <bookmark mark='d'/> Anisotropic filtering takes several probes along the long axis, "
            "each sized to the short axis, and averages them. <bookmark mark='e'/> The number of probes is the ratio "
            "of the axes, capped, and each probe reads a finer level."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(tl), FadeIn(ill))
            vo.wait_until("a")
            self.play(GrowFromCenter(ell))
            vo.wait_until("b")
            self.play(Create(iso), FadeIn(leg[0]))
            vo.wait_until("c")
            self.play(FadeIn(crops), FadeIn(cl))
            vo.wait_until("d")
            self.play(iso.animate.set_stroke(opacity=0.3), LaggedStart(*[Create(p) for p in probes], lag_ratio=0.3),
                      FadeIn(leg[1]))
            vo.wait_until("e")
            self.play(Write(rows), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def msaa(self):
        t = load("texture")
        head = label(r"Edges: \ supersampling and MSAA", font_size=36).to_edge(UP, buff=0.3)
        n, cell = 4, 1.25
        o = np.array([-6.3, 2.35, 0])

        def P(x, y):
            return o + np.array([x * cell, -y * cell, 0])
        pix = VGroup(*[Square(cell, stroke_color=GREY_C, stroke_width=1.5).move_to(P(i + 0.5, j + 0.5))
                       for j in range(3) for i in range(n)])
        a, b = np.array([0.0, 3.0]), np.array([4.0, 0.4])       # the triangle's edge, in pixel units

        def inside(x, y):
            return (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0]) > 0
        tri = Polygon(P(*a), P(*b), P(4, 3), stroke_width=0, fill_color=DATA, fill_opacity=0.35)
        edge = Line(P(*a), P(*b), color=DATA, stroke_width=3)
        ss = VGroup()
        for j in range(3):
            for i in range(n):
                for p in range(4):
                    for q in range(4):
                        x, y = i + (p + 0.5) / 4, j + (q + 0.5) / 4
                        ss.add(Dot(P(x, y), radius=0.05, color=HEAD if inside(x, y) else GREY_C))
        pattern = [(-2, -6), (6, -2), (-6, 2), (2, 6)]           # a rotated grid, in sixteenths of a pixel
        ms, shade = VGroup(), VGroup()
        for j in range(3):
            for i in range(n):
                cov = 0
                for dx, dy in pattern:
                    x, y = i + 0.5 + dx / 16, j + 0.5 + dy / 16
                    cov += inside(x, y)
                    ms.add(Dot(P(x, y), radius=0.06, color=YES if inside(x, y) else GREY_D))
                if cov:
                    shade.add(Star(5, outer_radius=0.13, color=KERN, fill_opacity=1).move_to(P(i + 0.5, j + 0.5)))
        ill = note(r"illustrative", font_size=16).next_to(pix, DOWN, buff=0.1).align_to(pix, RIGHT)
        leg = VGroup(label(r"16 samples: \ each one shaded", font_size=18, color=HEAD),
                     label(r"4 samples: \ coverage and depth only", font_size=18, color=YES),
                     label(r"one shader run per pixel per triangle", font_size=18, color=KERN)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(pix, DOWN, buff=0.45).align_to(pix, LEFT)
        tab = grid_table([r"per pixel", r"samples", r"shader runs", r"smooths"],
                         [[r"16$\times$ supersampling", r"16", r"16", r"edges and textures"],
                          [r"4$\times$ MSAA", r"4", r"1", r"edges only"]],
                         widths=[2.3, 1.1, 1.4, 2.0], row_h=0.5, font_size=19, mono_cols=(),
                         colors=[[HEAD] * 4, [YES] * 4]).move_to([3.3, 1.4, 0])
        notes = VGroup(
            wrapped_label(r"MSAA resolves the pixel as the average of its samples, \ so an edge pixel half covered "
                          r"gets half the triangle's colour", 6.2, font_size=19, color=WHITE),
            wrapped_label(r"inside a triangle all 4 samples get the same colour, \ so MSAA does nothing for textures: "
                          r"\ that is the mipmap's job", 6.2, font_size=19, color=YES),
            wrapped_label(rf"on our floor, \ 16 samples per pixel reach error {t['rmse']['ss16']:.3f} at 16 times "
                          rf"the shading work; \ the mipmap reaches {t['rmse']['mip']:.3f} at one", 6.2,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Mipmaps fix the inside of a triangle, but edges alias too, into staircases. <bookmark mark='a'/> The "
            "brute-force cure is supersampling: sixteen samples per pixel, each shaded, then averaged, for sixteen "
            "times the cost. <bookmark mark='b'/> Multisample antialiasing, MSAA, sees that a staircase is a "
            "coverage problem. It tests coverage and depth at four points per pixel, <bookmark mark='c'/> but runs "
            "the shader once per pixel per triangle and copies the colour to the covered samples. "
            "<bookmark mark='d'/> Averaging the samples softens the edge. <bookmark mark='e'/> Inside a triangle all "
            "four samples agree, so textures still need mipmaps. <bookmark mark='f'/> On our floor, sixteen samples "
            "beat the mipmap only slightly, for sixteen times the work. Good sampling is cheaper than more sampling."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pix), FadeIn(tri), Create(edge), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in ss], lag_ratio=0.004), FadeIn(leg[0]), run_time=2)
            self.play(FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]),
                      FadeIn(tab.cells[0][3]), Create(tab.rule), *[FadeIn(c) for c in tab.cells[1]])
            vo.wait_until("b")
            self.play(FadeOut(ss), LaggedStart(*[FadeIn(d, scale=0.5) for d in ms], lag_ratio=0.02), FadeIn(leg[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(shade), FadeIn(leg[2]), *[FadeIn(c) for c in tab.cells[2]])
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
            vo.wait_until("f")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
