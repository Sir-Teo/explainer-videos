from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403


class Making(VoiceoverScene):
    def construct(self):
        card(self, 2, "How a chip is made", "What happens to a disc of silicon in a fab?",
             "Chapter two. How a chip is made.", lit=("unit", "make"))
        self.loop()
        self.light()
        self.dies()

    def loop(self):
        x0, w = -5.0, 6.0
        base = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=SILICON, fill_opacity=1).move_to([x0 + w / 2, -2.0, 0])
        base_l = tx("silicon wafer", 14, GREY_A).next_to(base, DOWN, buff=0.08)
        film = Rectangle(width=w, height=0.25, stroke_width=0, fill_color="#5DA9E9", fill_opacity=0.9).move_to(base.get_top(), aligned_edge=DOWN)
        resist = Rectangle(width=w, height=0.18, stroke_width=0, fill_color="#F6C453", fill_opacity=0.85).move_to(film.get_top(), aligned_edge=DOWN)
        mask = VGroup(*[Rectangle(width=0.45, height=0.12, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to(
            [x0 + 0.5 + 0.9 * k, 1.9, 0]) for k in range(7)])
        mask_l = tx("mask: the pattern", 14, GREY_A).next_to(mask, UP, buff=0.08)
        beams = VGroup(*[Rectangle(width=0.4, height=3.3, stroke_width=0, fill_color=LIGHT, fill_opacity=0.25).move_to(
            [x0 + 0.95 + 0.9 * k, 0.15, 0]) for k in range(6)])
        lens = Ellipse(width=w * 0.9, height=0.35, stroke_color=LIGHT, stroke_width=2, fill_color=LIGHT, fill_opacity=0.12).move_to([x0 + w / 2, 1.2, 0])
        exposed = VGroup(*[Rectangle(width=0.4, height=0.18, stroke_width=0, fill_color="#B58CFF", fill_opacity=1).move_to(
            [x0 + 0.95 + 0.9 * k, resist.get_center()[1], 0]) for k in range(6)])
        trenches = VGroup(*[Rectangle(width=0.4, height=0.25, stroke_width=0, fill_color="#0E1117", fill_opacity=1).move_to(
            [x0 + 0.95 + 0.9 * k, film.get_center()[1], 0]) for k in range(6)])
        steps = VGroup(*[tx(t, 17, c, bold=True) for t, c in (("1. deposit a thin film", "#5DA9E9"), ("2. coat it with resist", "#F6C453"),
                                                               ("3. shine light through a mask", LIGHT), ("4. wash off the exposed resist", "#B58CFF"),
                                                               ("5. etch the film where it is bare", BAD), ("6. strip, clean, and repeat", GOOD))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.5, 0.2, 0])
        layers = VGroup(*[Rectangle(width=w, height=0.1, stroke_width=0, fill_color=c, fill_opacity=0.8) for c in
                          ("#5DA9E9", "#C9732F", "#7BD88F", "#5DA9E9", "#B58CFF", "#C9732F", "#7BD88F", "#5DA9E9")]).arrange(UP, buff=0.02)
        src = source("ASML Holding, Form 20-F 2025 (lithography); G. E. Moore, IEDM 1975 (line widths)", size=13)
        with self.voiceover(
            "A chip is built in layers on a polished disc of silicon, a wafer, by repeating one loop over and over. "
            "<bookmark mark='a'/> Lay down a thin film of material. <bookmark mark='b'/> Coat it with a light-sensitive "
            "resist. <bookmark mark='c'/> Shine light through a mask, the pattern for that layer, focused down by a lens "
            "onto the wafer. <bookmark mark='d'/> Wash away the resist the light has touched. <bookmark mark='e'/> Etch "
            "the film wherever it is now bare. <bookmark mark='f'/> Strip off the rest of the resist, clean, and start "
            "again with the next layer: transistors at the bottom, then layer upon layer of wiring to join them."
        ) as vo:
            self.play(FadeIn(base), FadeIn(base_l), FadeIn(src), FadeIn(steps.copy().set_opacity(0.25)))
            vo.wait_until("a")
            self.play(GrowFromEdge(film, DOWN), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(resist, DOWN), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(mask), FadeIn(mask_l), FadeIn(lens), FadeIn(steps[2]))
            self.play(LaggedStart(*[FadeIn(b) for b in beams], lag_ratio=0.1), FadeIn(exposed), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeOut(beams), FadeOut(exposed), FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(trenches), FadeIn(steps[4]))
            vo.wait_until("f")
            self.play(FadeOut(resist), FadeOut(mask), FadeOut(mask_l), FadeOut(lens), FadeIn(steps[5]))
            layers.move_to(film.get_top(), aligned_edge=DOWN)
            self.play(LaggedStart(*[GrowFromEdge(l, DOWN) for l in layers], lag_ratio=0.25), run_time=2.5)
        self.clear_scene()

    def light(self):
        rows = [("i-line lamp", get("asml.nm.iline")), ("krypton fluoride laser", get("asml.nm.krf")),
                ("argon fluoride laser", get("asml.nm.arf")), ("extreme ultraviolet (EUV)", get("asml.nm.euv"))]
        sc = 9.0 / 365
        bars = VGroup()
        for i, (n, nm) in enumerate(rows):
            y = 1.6 - 0.9 * i
            b = Rectangle(width=max(nm * sc, 0.06), height=0.5, stroke_width=0, fill_color=LIGHT, fill_opacity=0.4 + 0.15 * i).move_to([-3.6, y, 0], aligned_edge=LEFT)
            bars.add(VGroup(tx(n, 16, WHITE).next_to([-3.75, y, 0], LEFT, buff=0), b, tx(f"{nm:g} nm", 17, LIGHT, bold=True).next_to(b, RIGHT, buff=0.12)))
        head = tx("The wavelength of the light that prints the pattern", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
        rule = VGroup(tx("smallest feature  =  k1  x  wavelength  /  numerical aperture", 18, PRICE, bold=True),
                      tx("the Rayleigh criterion: shorter light, wider lenses, cleverer processing", 14, GREY_A)).arrange(DOWN, buff=0.06).to_edge(DOWN, buff=0.85)
        only = tx("'ASML is currently the world's only manufacturer of EUV lithography systems.'", 15, GREY_A).next_to(bars, DOWN, buff=0.3)
        src = source("ASML Holding, Form 20-F 2025 (light sources, the Rayleigh criterion, EUV)", size=13)
        with self.voiceover(
            "The smallest thing you can print is set by the light. <bookmark mark='a'/> Smaller features need shorter "
            "wavelengths. ASML's lamps and lasers give light of 365, 248 and 193 nanometres, all still in use. "
            f"<bookmark mark='b'/> The most advanced machines now use extreme ultraviolet light, {get('asml.nm.euv'):g} "
            "nanometres. <bookmark mark='c'/> The rule the toolmakers work by: the smallest feature is a constant times "
            "the wavelength, divided by the lens's numerical aperture. Over forty years, ASML says, that has improved a "
            "hundredfold. <bookmark mark='d'/> And only one company in the world makes the machines that use extreme "
            "ultraviolet light: ASML, in the Netherlands."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(b[0]) for b in bars])
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[1], LEFT), FadeIn(b[2])) for b in bars[:3]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[3][1], LEFT), FadeIn(bars[3][2]), Indicate(bars[3][2], color=LIGHT))
            vo.wait_until("c")
            self.play(FadeIn(rule, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(only))
        self.clear_scene()

    def dies(self):
        M = R["making"]
        w = draw.wafer(1.9, die=0.2).move_to([-4.0, -0.2, 0])
        w_l = VGroup(tx("one 300 mm wafer", 17, WHITE, bold=True), tx(f"about {M['dpw100']:.0f} dies of 100 mm2 (drawing not to scale)", 14, GREY_A)).arrange(
            DOWN, buff=0.04).next_to(w, UP, buff=0.15)
        rng = np.random.default_rng(3)
        bad = [d for d in w.dies if rng.random() < 0.1]
        die = Square(0.9, stroke_width=0, fill_color=DIE, fill_opacity=0.9).move_to([0.2, -0.2, 0])
        die_l = tx("cut out: a die", 15, GREY_A).next_to(die, DOWN, buff=0.12)
        pkg = draw.chip(1.3).move_to([3.2, -0.2, 0])
        pkg_l = tx("packaged and tested: a chip", 15, GREY_A).next_to(pkg, DOWN, buff=0.12)
        arrows = VGroup(Arrow([-1.9, -0.2, 0], [-0.4, -0.2, 0], color=GREY_B, stroke_width=3, buff=0.05),
                        Arrow([0.8, -0.2, 0], [2.3, -0.2, 0], color=GREY_B, stroke_width=3, buff=0.05))
        lines = VGroup(tx(f"1961: lines about {M['line61']:.0f} micrometres wide", 16, GREY_A),
                       tx(f"1975: about {M['line75']:.0f} micrometres", 16, GREY_A),
                       tx("2026: TSMC's '2-nanometer' process in volume", 16, WHITE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).to_edge(DOWN, buff=0.8).shift(RIGHT * 2.2)
        src = source("G. E. Moore, IEDM 1975 (line widths); TSMC, Form 6-K of 15 October 2026; the Works (dies per wafer)", size=13)
        with self.voiceover(
            "After many turns of the loop, the wafer holds a grid of identical chips. <bookmark mark='a'/> A wafer 300 "
            f"millimetres across holds about {M['dpw100']:.0f} dies of a hundred square millimetres. <bookmark mark='b'/> "
            "Each is tested on the wafer, and the failures marked. <bookmark mark='c'/> The good ones are cut out, "
            "<bookmark mark='d'/> mounted in a package that connects them to the outside world, and tested again. "
            f"<bookmark mark='e'/> In 1961 the lines on a chip were about {M['line61']:.0f} micrometres wide; in 1975, about "
            f"{M['line75']:.0f}, Moore reported. In 2026 TSMC was selling chips made on a process it calls two nanometres."
        ) as vo:
            self.play(FadeIn(src), FadeIn(w), FadeIn(w_l))
            vo.wait_until("a")
            self.play(Indicate(w.dies, color=DIE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(LaggedStart(*[d.animate.set_fill(DEFECT) for d in bad], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("c")
            self.play(GrowArrow(arrows[0]), FadeIn(die), FadeIn(die_l))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[1]), FadeIn(pkg), FadeIn(pkg_l))
            vo.wait_until("e")
            self.play(FadeIn(lines, shift=UP * 0.1))
        self.clear_scene()
