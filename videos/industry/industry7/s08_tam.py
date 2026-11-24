from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry7.common import *  # noqa: F403


class Tam(VoiceoverScene):
    def construct(self):
        card(self, 9, "Addressable markets", "What is a 'total addressable market' actually counting?",
             "Chapter nine. Addressable markets.", lit=("unit",))
        self.uber()
        self.rings()

    def uber(self):
        U = R["uber"]
        cars = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.06, width=0.7, height=0.22, stroke_width=0,
                                                fill_color="#7EC8F5", fill_opacity=0.9),
                               *[Circle(radius=0.06, stroke_width=0, fill_color="#20242C", fill_opacity=1).shift(
                                   DOWN * 0.12 + RIGHT * x) for x in (-0.22, 0.22)]) for _ in range(12)])
        cars.arrange_in_grid(rows=3, cols=4, buff=(0.15, 0.2)).move_to([-4.6, 1.5, 0])
        bus = VGroup(RoundedRectangle(corner_radius=0.08, width=1.6, height=0.5, stroke_width=0, fill_color=GOLD,
                                      fill_opacity=0.9),
                     *[Rectangle(width=0.18, height=0.16, stroke_width=0, fill_color="#2B3A55", fill_opacity=1).shift(
                         RIGHT * (x - 0.6) + UP * 0.06) for x in np.linspace(0, 1.2, 6)]).move_to([-4.6, -0.6, 0])
        eqs = VGroup(
            MathTex(rf"7.5\text{{ trillion car miles}} \to \${get('uber.tam.vehicle'):.1f}\text{{tn}}", font_size=32,
                    color="#7EC8F5"),
            MathTex(rf"4.4\text{{ trillion bus and train miles}} \times 23\text{{c}} \to \${get('uber.tam.public'):.1f}"
                    r"\text{tn}", font_size=32, color=GOLD),
            MathTex(rf"= \${U['mobility']:.1f}\text{{ trillion: 'getting around'}}", font_size=36)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.2, 0.6, 0])
        inc = VGroup(tx("includes every mile you drive in your own car,", 18, GREY_A),
                     tx("every bus and train ride, in 175 countries", 18, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.06).next_to(eqs, DOWN, buff=0.35)
        on = tx(f"Uber's own trips, 2018: {U['platform_miles']:.0f} billion miles", 20, WHITE, bold=True).to_edge(
            DOWN, buff=0.55)
        src = source("Uber Technologies, Form S-1, 11 April 2019", size=13)
        with self.voiceover(
            "Go back to Uber's twelve trillion dollars, and read how it was built. <bookmark mark='a'/> Start with "
            "every passenger-car mile driven in 175 countries, seven and a half trillion of them, valued at what a "
            f"mile of driving costs: {get('uber.tam.vehicle'):.1f} trillion dollars. <bookmark mark='b'/> Add every "
            "mile travelled on a bus or a train, four point four trillion of them, at about twenty-three cents a "
            f"mile: another {get('uber.tam.public'):.0f} trillion. <bookmark mark='c'/> So 'getting around' is worth "
            f"{U['mobility']:.1f} trillion. It includes every mile you drive in your own car to work, and every bus "
            "ride in a city where Uber does not operate. <bookmark mark='d'/> Uber's own trips in 2018 came to "
            f"{U['platform_miles']:.0f} billion miles. The prospectus said so itself: less than one percent."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.2) for c_ in cars], lag_ratio=0.05),
                      run_time=1.6)
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(bus, shift=RIGHT * 0.3), Write(eqs[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]), FadeIn(inc))
            vo.wait_until("d")
            self.play(FadeIn(on, shift=UP * 0.1))
        self.clear_scene()

    def rings(self):
        U = R["uber"]
        c = np.array([-3.2, -0.4, 0])
        rT = 2.6
        rS = rT * np.sqrt(U["sam"] / U["mobility"])
        rO = rT * np.sqrt(U["revenue"][2018] / 1000 / U["mobility"])
        tam = Circle(radius=rT, stroke_color=TAM, stroke_width=3, fill_color=TAM, fill_opacity=0.1).move_to(c)
        sam = Circle(radius=rS, stroke_color=GUESS, stroke_width=3, fill_color=GUESS, fill_opacity=0.15).move_to(c)
        som = Dot(c, radius=max(rO, 0.04), color=WHITE)
        labels = VGroup(
            VGroup(tx("TAM: total addressable market", 20, TAM, bold=True),
                   tx(f"everything that could be done our way: ${U['mobility']:.1f}tn", 16, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.04),
            VGroup(tx("SAM: serviceable", 20, GUESS, bold=True),
                   tx(f"where we operate, trips under 30 miles: ${U['sam']:.1f}tn", 16, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.04),
            VGroup(tx("what we actually sell", 20, WHITE, bold=True),
                   tx(f"Uber's whole revenue, 2018: ${U['revenue'][2018]:.1f}bn", 16, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.04)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.3, 0.2, 0])
        lines = VGroup(*[Line(lab.get_left() + LEFT * 0.1, tgt, stroke_color=GREY_C, stroke_width=1.5)
                         for lab, tgt in zip(labels, (tam.point_at_angle(PI / 6), sam.point_at_angle(PI / 8), c))])
        verdict = tx("A TAM answers: how big would this be if everyone did it our way?", 20, GOLD, bold=True).to_edge(
            DOWN, buff=0.5)
        src = source("Uber Technologies, Form S-1 (2019) and Form 10-K for 2018", size=13)
        with self.voiceover(
            "Prospectuses draw this as three rings. <bookmark mark='a'/> The outer one, the total addressable market: "
            "everything that could be done the company's way, if the whole world switched. <bookmark mark='b'/> "
            "Inside it, the serviceable market: the part where the company actually operates, and for the kind of "
            f"trip it serves. For Uber, {U['sam']:.1f} trillion dollars. <bookmark mark='c'/> And at the centre, too "
            "small to see at this scale, what the company actually sells. <bookmark mark='d'/> The outer ring "
            "answers a question about ambition: how big would this be if everyone did it our way? It is not a "
            "forecast, and it is not a market in the sense this series uses the word: buyers who are paying, now, "
            "for something, at a price. Read it as the company's dream, and look for the inner rings."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(DrawBorderThenFill(tam), FadeIn(labels[0]), Create(lines[0]))
            vo.wait_until("b")
            self.play(DrawBorderThenFill(sam), FadeIn(labels[1]), Create(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(som, scale=3), FadeIn(labels[2]), Create(lines[2]))
            self.play(Flash(c, color=WHITE, line_length=0.2))
            vo.wait_until("d")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()
