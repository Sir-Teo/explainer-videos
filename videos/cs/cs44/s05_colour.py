from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, trace

NAMES = ("data", "here", "true", "false", "lambda", "kernel")


class Colour(VoiceoverScene):
    def construct(self):
        self.card()
        self.light()
        self.gamma()
        self.perceptual()
        self.deficiency()
        self.contrast()

    def card(self):
        card = chapter_card(4, r"Colour", r"How do three numbers become a colour, \ and for whom?",
                            lit=(1931, 1976, 2020), extra=((1931, r"CIE XYZ"), (1976, r"CIELAB"),
                                                           (2009, r"Machado et al.: \ simulated deficiency"),
                                                           (2020, r"Ottosson: \ OKLab")), part=PART)
        with self.voiceover("Chapter four. Colour."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def light(self):
        head = label(r"Colour is three numbers", font_size=36).to_edge(UP, buff=0.3)
        g = axes([400, 700, 100], [0, 1.1, 0.5], x_length=6.0, y_length=2.8, x_label=r"wavelength, \ nm",
                 y_label=r"cone response", xticks=range(400, 701, 100)).move_to([-3.2, 0.8, 0])
        ax = g.ax
        cones = [(445, 28, DATA, r"S"), (535, 42, YES, r"M"), (565, 46, NO, r"L")]
        curves, names = VGroup(), VGroup()
        for mu, sd, c, n in cones:
            pts = [(w, math.exp(-0.5 * ((w - mu) / sd) ** 2)) for w in range(400, 701, 4)]
            curves.add(trace(ax, pts, c, width=3))
            names.add(label(n, font_size=20, color=c).next_to(ax.c2p(mu, 1.0), UP, buff=0.08))
        spec_cols = color_gradient([PURPLE, BLUE, TEAL, GREEN, YELLOW, ORANGE, RED], 60)
        x0, x1 = ax.c2p(400, 0)[0], ax.c2p(700, 0)[0]
        strip = VGroup(*[Rectangle(width=(x1 - x0) / 60, height=0.18, stroke_width=0, fill_color=c,
                                   fill_opacity=1) for c in spec_cols]).arrange(RIGHT, buff=0)
        strip.next_to(g[1], DOWN, buff=0.1).set_x((x0 + x1) / 2)
        g[-2].next_to(strip, DOWN, buff=0.12)        # the x label below the strip
        tag = note(r"illustrative curves", font_size=16).next_to(g, UP, buff=0.35).align_to(g, RIGHT)
        probe = ValueTracker(450)
        line = always_redraw(lambda: DashedLine(ax.c2p(probe.get_value(), 0), ax.c2p(probe.get_value(), 1.1),
                                                color=WHITE, stroke_width=2))
        bars = always_redraw(lambda: VGroup(*[
            Rectangle(width=0.5, height=max(0.02, 1.35 * math.exp(-0.5 * ((probe.get_value() - mu) / sd) ** 2)),
                      stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(
                [-4.6 + 0.7 * k, -3.5, 0], aligned_edge=DOWN) for k, (mu, sd, c, _) in enumerate(cones)]))
        bl = label(r"three responses: \ S, \ M, \ L", font_size=17, color=GREY_A).move_to([-1.3, -3.2, 0])
        W = 5.4
        side = VGroup(
            wrapped_label(r"three kinds of cone, \ short, \ medium and long: \ every spectrum is reduced to three "
                          r"numbers", W, font_size=20, color=WHITE),
            wrapped_label(r"different spectra with the same three responses look identical \ (metamers): \ so three "
                          r"primaries can imitate most colours", W, font_size=20, color=YES),
            wrapped_label(r"\textbf{CIE XYZ} \ (1931): \ a standard observer from colour-matching experiments; \ "
                          r"\textbf{sRGB} \ (HP and Microsoft, \ 1996): \ three primaries and a white, \ defined "
                          r"in XYZ", W, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.75, 0.2, 0])
        with self.voiceover(
            "Light is a spectrum, energy spread across wavelengths. <bookmark mark='a'/> The eye measures it with "
            "three kinds of cone, sensitive to short, medium and long wavelengths. <bookmark mark='b'/> Whatever "
            "the spectrum, it is reduced to three responses. <bookmark mark='c'/> Two spectra with the "
            "same three responses look identical: metamers, which is why three primaries can imitate most colours "
            "we see. <bookmark mark='d'/> In 1931 the CIE fixed a "
            "standard observer from colour-matching experiments, the XYZ space. The sRGB standard, from HP and "
            "Microsoft in 1996, defines three primaries and a white in XYZ, and almost every screen and web page "
            "assumes it."
        ) as vo:
            self.play(FadeIn(head), Create(g), FadeIn(strip), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(curves), FadeIn(names), FadeIn(side[0]))
            vo.wait_until("b")
            self.add(line, bars)
            self.play(FadeIn(bl))
            self.play(probe.animate.set_value(640), run_time=3, rate_func=there_and_back_with_pause)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def gamma(self):
        gm = load("gamma")
        rows = gm["rows"]
        head = label(r"Code values are not light", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 1, 0.25], [0, 1, 0.25], x_length=4.6, y_length=3.6, x_label=r"sRGB code value \ (0 to 1)",
                 y_label=r"fraction of white", xticks=[0, 0.5, 1], yticks=[0, 0.5, 1]).move_to([-3.7, 0.35, 0])
        ax = g.ax
        light = trace(ax, [(r["code"], r["light"]) for r in rows], HEAD, width=3.5)
        perc = trace(ax, [(r["code"], r["oklab_L"]) for r in rows], LAM, width=3)
        ll = label(r"light", font_size=18, color=HEAD).next_to(ax.c2p(0.62, 0.3), RIGHT, buff=0.1)
        pl = label(r"lightness \ (OKLab $L$)", font_size=18, color=LAM).next_to(ax.c2p(0.42, 0.62), LEFT,
                                                                             buff=0.1)
        c128 = 128 / 255
        h_code = int(gm["half_light"][1:3], 16) / 255
        m1 = VGroup(DashedLine(ax.c2p(c128, 0), ax.c2p(c128, gm["code_128_light"]), color=GREY_A),
                    DashedLine(ax.c2p(0, gm["code_128_light"]), ax.c2p(c128, gm["code_128_light"]), color=GREY_A))
        m2 = VGroup(DashedLine(ax.c2p(h_code, 0), ax.c2p(h_code, 0.5), color=YES),
                    DashedLine(ax.c2p(0, 0.5), ax.c2p(h_code, 0.5), color=YES))
        sw1 = VGroup(Square(0.9, stroke_color=GREY_B, stroke_width=1, fill_color="#808080", fill_opacity=1),
                     label(rf"\#808080: \ code 128 \ is {100 * gm['code_128_light']:.1f}\% of white's light",
                           font_size=19, color=WHITE))
        sw2 = VGroup(Square(0.9, stroke_color=GREY_B, stroke_width=1, fill_color=gm["half_light"], fill_opacity=1),
                     label(rf"\#{gm['half_light'][1:]}: \ half of white's light", font_size=19, color=YES))
        for s in (sw1, sw2):
            s[1].next_to(s[0], RIGHT, buff=0.25)
        sws = VGroup(sw1, sw2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.2, 1.55, 0])
        curve = MathTex(r"\text{light} = \left(\frac{c + 0.055}{1.055}\right)^{2.4}", font_size=34, color=HEAD)
        cn = label(r"(above a short linear segment near black)", font_size=17, color=GREY_B)
        eq = VGroup(curve, cn).arrange(DOWN, buff=0.1).next_to(sws, DOWN, buff=0.35)
        why = wrapped_label(r"equal code steps are roughly equal steps of \textit{lightness}: \ Weber and Fechner "
                            r"again, \ so the 256 codes are spent where the eye can tell them apart; \ but blending, "
                            r"\ scaling and lighting must be done in linear light \ (Part 51)", 6.4, font_size=19,
                            color=WHITE).next_to(eq, DOWN, buff=0.3).set_x(3.4)
        steps = VGroup(*[Square(0.4, stroke_width=0, fill_color="#{0:02x}{0:02x}{0:02x}".format(round(k * 25.5)),
                                fill_opacity=1) for k in range(11)]).arrange(RIGHT, buff=0)
        steps.next_to(g, DOWN, buff=0.2)
        stl = note(r"eleven equal steps of code", font_size=16).next_to(steps, DOWN, buff=0.08)
        with self.voiceover(
            "An sRGB pixel stores code values from 0 to 255, and they are not amounts of light. "
            "<bookmark mark='a'/> The transfer curve, close to a power of 2.4, maps code to light. "
            f"<bookmark mark='b'/> Code 128, the middle of the range, emits only "
            f"{100 * gm['code_128_light']:.1f} percent of white's light. <bookmark mark='c'/> Half of white's light "
            "is this much paler grey, b c b c b c. <bookmark mark='d'/> The curve is there because of Weber and "
            "Fechner: equal steps of code are roughly equal steps of perceived lightness, so the codes are spent "
            "where the eye can tell them apart. The price is that mixing, scaling and lighting must convert to "
            "linear light first, a theme of Part 51."
        ) as vo:
            self.play(FadeIn(head), Create(g), FadeIn(steps), FadeIn(stl))
            vo.wait_until("a")
            self.play(Create(light), FadeIn(ll), FadeIn(eq))
            vo.wait_until("b")
            self.play(Create(m1), FadeIn(sw1))
            vo.wait_until("c")
            self.play(Create(m2), FadeIn(sw2))
            vo.wait_until("d")
            self.play(Create(perc), FadeIn(pl), FadeIn(why))
        self.wait(0.4)
        self.clear_scene()

    def perceptual(self):
        col = load("colour")
        ck = load("gamma")["checks"]
        ok, hexes = col["oklab"], col["views"]["normal"]
        head = label(r"Perceptual spaces: \ CIELAB and OKLab", font_size=36).to_edge(UP, buff=0.3)
        # the sRGB cube in code values, drawn obliquely: r to the right, g into the page, b up
        s, o = 1.75, [-6.3, -1.3, 0]

        def P(r, g_, b):
            return [o[0] + s * (r + 0.5 * g_), o[1] + s * (b + 0.42 * g_), 0]
        corners = {(r, g_, b): "#{:02x}{:02x}{:02x}".format(255 * r, 255 * g_, 255 * b)
                   for r in (0, 1) for g_ in (0, 1) for b in (0, 1)}
        edges = VGroup(*[Line(P(*u), P(*v), color=GREY_C, stroke_width=1.5) for u in corners for v in corners
                         if sum(abs(p - q) for p, q in zip(u, v)) == 1 and u < v])
        cdots = VGroup(*[Dot(P(*u), radius=0.11, color=h, stroke_color=GREY_B, stroke_width=1)
                         for u, h in corners.items()])
        cube_l = label(r"the sRGB cube \ (code values)", font_size=18, color=GREY_A).next_to(edges, DOWN, buff=0.2)
        g = axes([-0.25, 0.25, 0.1], [-0.25, 0.25, 0.1], x_length=4.5, y_length=4.5, x_label=r"$a$: \ green to red",
                 y_label=r"$b$: \ blue to yellow", xticks=[-0.2, 0, 0.2], yticks=[-0.2, 0, 0.2],
                 fx=lambda v: f"{v:.1f}", fy=lambda v: f"{v:.1f}").move_to([-0.15, -0.1, 0])
        ax = g.ax
        where = {"data": LEFT, "here": UP, "true": LEFT, "false": DOWN, "lambda": RIGHT, "kernel": DOWN}
        pts = VGroup()
        for n in NAMES:
            d = Dot(ax.c2p(ok[n][1], ok[n][2]), radius=0.1, color=hexes[n])
            pts.add(VGroup(d, label(n, font_size=16, color=hexes[n]).next_to(d, where[n], buff=0.08)))
        red = ck["red_oklab"]
        rd = Dot(ax.c2p(red[1], red[2]), radius=0.1, color="#ff0000")
        rl = label(r"sRGB red", font_size=16, color="#ff6666").next_to(rd, UR, buff=0.04)
        grey = VGroup(Dot(ax.c2p(0, 0), radius=0.07, color=WHITE), label(r"greys", font_size=16,
                                                                         color=GREY_A).next_to(ax.c2p(0, 0), DL,
                                                                                               buff=0.05))
        W = 3.6
        side = VGroup(
            wrapped_label(r"\textbf{CIELAB} \ (1976): \ lightness $L$ and two opponent axes, \ from XYZ through a "
                          r"cube root", W, font_size=18, color=WHITE),
            wrapped_label(r"\textbf{OKLab} \ (Ottosson, \ 2020): \ refitted so that equal distances look more "
                          r"equal, \ and hues hold while lightening", W, font_size=18, color=YES),
            wrapped_label(rf"checks: \ white is $L = {ck['white_lab'][0]:.1f}$ in CIELAB and "
                          rf"${ck['white_oklab'][0]:.3f}$ in OKLab; \ sRGB red is "
                          rf"$({red[0]:.3f},\ {red[1]:.3f},\ {red[2]:.3f})$, \ the published value", W,
                          font_size=18, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([5.0, 0.1, 0])
        with self.voiceover(
            "Code values say nothing about how different two colours look. "
            "<bookmark mark='a'/> Every colour a screen can show sits in this cube of red, green and blue. "
            "<bookmark mark='b'/> Perceptual spaces bend that cube so that distance means difference. CIELAB, from "
            "1976, gives lightness and two opponent axes, green to red and blue to yellow. <bookmark mark='c'/> "
            "OKLab, published by Björn Ottosson in 2020, is refitted so that equal distances look more nearly equal "
            "and hues stay put as colours lighten. Here is this series' own palette in it, and the cube's red "
            "corner. <bookmark mark='d'/> Our conversions pass the checks: white has lightness one hundred in "
            "CIELAB and one in OKLab, and sRGB red lands on the published value."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(edges), FadeIn(cdots), FadeIn(cube_l))
            vo.wait_until("b")
            self.play(Create(g), FadeIn(grey), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.2), FadeIn(side[1]))
            self.play(Flash(cdots[4], color="#ff6666"), FadeIn(rd), FadeIn(rl))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def deficiency(self):
        col = load("colour")
        views, pairs = col["views"], col["pairs"]
        head = label(r"Our palette, \ seen by other eyes", font_size=36).to_edge(UP, buff=0.3)
        order = ("normal", "protanopia", "deuteranopia", "tritanopia")
        nice = {"normal": r"typical vision", "protanopia": r"protanopia \ (no L)",
                "deuteranopia": r"deuteranopia \ (no M)", "tritanopia": r"tritanopia \ (no S)"}
        sz, gap, xs, y0, dy = 0.62, 0.14, -3.6, 1.45, 0.88
        top = VGroup(*[label(n, font_size=16, color=GREY_B).move_to([xs + k * (sz + gap), y0 + 0.55, 0])
                       for k, n in enumerate(NAMES)])
        rows, closest = VGroup(), VGroup()
        for i, v in enumerate(order):
            y = y0 - i * dy
            nm = label(nice[v], font_size=18, color=WHITE).move_to([xs - 0.6, y, 0], aligned_edge=RIGHT)
            sws = VGroup(*[Square(sz, stroke_width=0, fill_color=views[v][n], fill_opacity=1).move_to(
                [xs + k * (sz + gap), y, 0]) for k, n in enumerate(NAMES)])
            a, b, d = pairs[v]["closest"][0]
            c = NO if d < col["threshold"] else GREY_A
            cl = label(rf"\texttt{{{a}}} and \texttt{{{b}}}: \ {d:.3f}", font_size=18, color=c).move_to(
                [1.45, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(nm, sws))
            closest.add(cl)
        ch = label(r"closest pair \ (OKLab distance)", font_size=16, color=GREY_B).move_to([1.45, y0 + 0.55, 0],
                                                                                         aligned_edge=LEFT)
        di = order.index("deuteranopia")
        k1, k2 = NAMES.index("false"), NAMES.index("kernel")
        ring = SurroundingRectangle(VGroup(rows[di][1][k1], rows[di][1][k2]), color=HEAD, buff=0.07)
        notes = VGroup(
            wrapped_label(r"about 8\% of men of European ancestry and 0.5\% of women have a colour-vision deficiency, "
                          r"\ mostly red--green \ (approximate published figures); \ simulated here with the "
                          r"matrices of Machado, \ Oliveira and Fernandes \ (2009)", 12.4, font_size=19,
                          color=WHITE),
            wrapped_label(rf"under deuteranopia \texttt{{false}} red and \texttt{{kernel}} orange are "
                          rf"{pairs['deuteranopia']['closest'][0][2]:.3f} apart: \ nearly identical; \ red means "
                          rf"\textit{{wrong}} in this series, \ so it must never be the only signal \ (below "
                          rf"{col['threshold']:.2f} counts as easily confused)", 12.4, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "About eight percent of men of European ancestry, and half a percent of women, have a colour-vision "
            "deficiency, mostly red and green; those are approximate published figures. <bookmark mark='a'/> "
            "Here is this series' palette, as typical vision sees it. <bookmark mark='b'/> Below it, the same six "
            "colours simulated for the three kinds of missing cone, with the model of Machado, Oliveira and "
            "Fernandes from 2009. <bookmark mark='c'/> For each view, the closest pair in OKLab. "
            "<bookmark mark='d'/> The honest finding is about us. Under deuteranopia, the red this series uses for "
            f"false and the orange it uses for the kernel are only {pairs['deuteranopia']['closest'][0][2]:.3f} "
            "apart: nearly the same colour. Red means wrong in these videos, so red can never be the only signal."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.4), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(ch), LaggedStart(*[FadeIn(c) for c in closest], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(Create(ring), FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def contrast(self):
        col = load("colour")
        cr, normal, deut = col["contrast"], col["views"]["normal"], col["views"]["deuteranopia"]
        n7 = ["none", "one", "two", "three", "four", "five", "all six"][sum(v >= 7 for v in cr.values())]
        assert all(v >= 4.5 for v in cr.values())
        head = label(r"Contrast, \ and never colour alone", font_size=36).to_edge(UP, buff=0.3)
        g = axes([-0.5, 5.5, 1], [0, 13, 1], x_length=5.6, y_length=3.0, y_label=r"contrast on the background",
                 yticks=[0, 4.5, 7, 12], fy=lambda v: f"{v:g}").move_to([-3.3, 0.85, 0])
        ax = g.ax
        bars = VGroup()
        for k, n in enumerate(NAMES):
            b = Rectangle(width=0.62, height=ax.c2p(0, cr[n])[1] - ax.c2p(0, 0)[1], stroke_width=0,
                          fill_color=normal[n], fill_opacity=1).move_to(ax.c2p(k, 0), aligned_edge=DOWN)
            v = label(f"{cr[n]:.1f}", font_size=16, color=BLACK).move_to(b.get_top() + DOWN * 0.2)
            t = label(n, font_size=16, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
            bars.add(VGroup(b, v, t))
        aa = DashedLine(ax.c2p(-0.5, 4.5), ax.c2p(5.5, 4.5), color=GREY_A)
        aaa = DashedLine(ax.c2p(-0.5, 7), ax.c2p(5.5, 7), color=GREY_B)
        formula = MathTex(r"\text{contrast} = \frac{L_1 + 0.05}{L_2 + 0.05}", font_size=32, color=HEAD)
        fn = wrapped_label(r"$L$: \ relative luminance, \ $0.2126R + 0.7152G + 0.0722B$ in \textit{linear} light; "
                           r"\ WCAG asks 4.5 for text, \ 7 for its strictest level", 6.0, font_size=18,
                           color=GREY_A)
        VGroup(formula, fn).arrange(DOWN, buff=0.15).next_to(bars, DOWN, buff=0.35)

        def chart(cols, shapes, cx, title, tcol):
            xs = [cx - 2.2 + 0.65 * i for i in range(6)]
            ys = [[0.2, 0.5, 0.45, 0.85, 1.0, 1.25], [0.0, 0.25, 0.65, 0.55, 0.8, 0.75]]
            grp = VGroup()
            for s_, (c, ys_) in enumerate(zip(cols, ys)):
                ln = VMobject(color=c, stroke_width=3).set_points_as_corners([[x, 0.6 + y, 0] for x, y in zip(xs,
                                                                                                          ys_)])
                grp.add(ln)
                if shapes:
                    for x, y in zip(xs, ys_):
                        m = (Square(0.16, stroke_width=0, fill_color=c, fill_opacity=1) if s_ else
                             Dot(radius=0.08, color=c)).move_to([x, 0.6 + y, 0])
                        grp.add(m)
                    grp.add(label([r"errors", r"retries"][s_], font_size=16, color=c).next_to(
                        [xs[-1], 0.6 + ys_[-1], 0], RIGHT, buff=0.12))
            frame = Rectangle(width=4.9, height=2.0, stroke_color=GREY_D, stroke_width=1).move_to([cx, 1.25, 0])
            t = label(title, font_size=17, color=tcol).next_to(frame, UP, buff=0.08)
            return VGroup(frame, grp, t)
        c1 = chart([normal["false"], normal["kernel"]], False, 3.95, r"colour alone, \ typical vision", GREY_A)
        c2 = chart([deut["false"], deut["kernel"]], False, 3.95, r"colour alone, \ deuteranopia", NO)
        c3 = chart([deut["false"], deut["kernel"]], True, 3.95, r"plus shape and labels, \ deuteranopia", YES)
        for c in (c1, c2, c3):
            c.shift(UP * 0.3)
        tag = note(r"chart illustrative; \ line colours from the simulation", font_size=16).next_to(
            c1[0], DOWN, buff=0.12).align_to(c1[0], LEFT)
        lesson = wrapped_label(r"never use colour alone: \ add shape, \ position or a label, \ so the information "
                               r"survives any one channel failing", 5.6, font_size=20, color=YES).next_to(
            tag, DOWN, buff=0.4).align_to(c1[0], LEFT)
        with self.voiceover(
            "Colour also decides whether text can be read. <bookmark mark='a'/> The contrast ratio of the Web "
            "Content Accessibility Guidelines compares relative luminances, computed in linear light, each plus "
            "a small constant for glare. <bookmark mark='b'/> Every colour in our palette clears 4.5, the level "
            f"asked for ordinary text, on the dark background; {n7} of them also clear seven. <bookmark mark='c'/> "
            "Contrast is not enough, though. A chart that separates two series by red and orange alone "
            "<bookmark mark='d'/> becomes one series under deuteranopia. <bookmark mark='e'/> Give each series a "
            "shape and a direct label as well, and the chart survives. The lesson: never use colour alone; add "
            "shape, position or a label."
        ) as vo:
            self.play(FadeIn(head), Create(g))
            vo.wait_until("a")
            self.play(FadeIn(formula), FadeIn(fn))
            vo.wait_until("b")
            self.play(Create(aa), Create(aaa), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(c1), FadeIn(tag))
            vo.wait_until("d")
            self.play(ReplacementTransform(c1[1], c2[1]), FadeOut(c1[2]), FadeIn(c2[2]))
            vo.wait_until("e")
            self.play(ReplacementTransform(c2[1], c3[1]), FadeOut(c2[2]), FadeIn(c3[2]), FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM)
