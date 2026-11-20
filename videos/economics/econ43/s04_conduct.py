from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class Conduct(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Conduct as a parameter", r"Can prices and quantities alone reveal market power?",
             "Chapter three. Conduct as a parameter.", lit={1982: r"Bresnahan; \ Lau"},
             scale=("industry",), horizon=("a decade",))
        self.shifts()
        self.rotation()
        self.lesson()

    def axes_(self):
        return plane([0, 9], [0, 14], center=LEFT * 1.9 + DOWN * 0.35, x_length=7.6, y_length=5.0,
                     xticks=[0, 2, 4, 6, 8], yticks=[0, 2, 4, 6, 8, 10, 12, 14], xlabel=r"quantity",
                     ylabel=r"price", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)

    def shifts(self):
        C = load("conduct")
        ax = self.axes_()
        A = [e for e in C["A"] if e["z"] == 0.0]
        dem = VGroup(*[seg(ax, 0, (10 + e["y"]) / 1.0, min(10 + e["y"], 9), (10 + e["y"] - min(10 + e["y"], 9)),
                           DEMAND, 2.6) for e in A])
        sup = seg(ax, 0, 2, 9, 11, SUPPLY, 3.0)
        mc = seg(ax, 0, 2, 9, 2, COST, 2.4, dashed=True)
        mrs = VGroup(*[seg(ax, 0, 10 + e["y"], (10 + e["y"]) / 2, 0, COST, 1.4, dashed=True) for e in A])
        dots = VGroup(*[dot(ax, e["Q"], e["P"], WHITE, 0.1) for e in A])
        side = VGroup(
            label(r"blue: \ demand, \\ shifting out", font_size=18, color=DEMAND),
            label(r"story A: \ competitive firms; \\ marginal cost rises \\ with output \ (gold)", font_size=18,
                  color=SUPPLY),
            label(r"story B: \ a monopolist; \\ flat marginal cost; \\ it sets marginal revenue \\ equal to it "
                  r"(red)", font_size=18, color=COST),
            label(r"the same prices and \\ quantities, \ every time", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.BRESNAHAN_1982.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "If concentration does not reveal conduct, can prices and quantities? Suppose you watch an industry "
            "over many years. <bookmark mark='a'/> Demand shifts out, as incomes grow, and you record the price "
            "and quantity each year. <bookmark mark='b'/> Story A: the industry is competitive, and price equals "
            "marginal cost, which rises with output. <bookmark mark='c'/> Story B: it is a monopoly with flat "
            "marginal cost, which sets output where marginal revenue equals that cost. <bookmark mark='d'/> With the "
            "numbers chosen here, both stories give exactly the same price and quantity every year. A rising supply "
            "curve under competition and a markup under monopoly can look identical. The data cannot tell them "
            "apart."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(dem[0]), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(dem[1]), Create(dem[2]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(sup), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(mc), Create(mrs), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots], lag_ratio=0.3), FadeIn(side[3]))
        self.clear_scene()

    def rotation(self):
        C = load("conduct")
        ax = self.axes_()
        a = [e for e in C["A"] if e["z"] == 0.5 and e["y"] == 3.0][0]
        b = [e for e in C["B"] if e["z"] == 0.5 and e["y"] == 3.0][0]
        a0 = [e for e in C["A"] if e["z"] == 0.0 and e["y"] == 3.0][0]
        d0 = seg(ax, 0, 13, 9, 4, DEMAND, 2.0)
        d0.set_stroke(opacity=0.4)
        d1 = seg(ax, 0, 13 / 1.5, 9, (13 - 9) / 1.5, DEMAND, 3.0)
        sup = seg(ax, 0, 2, 9, 11, SUPPLY, 3.0)
        mc = seg(ax, 0, 2, 9, 2, COST, 2.4, dashed=True)
        mr = seg(ax, 0, 13 / 1.5, 6.5, 0, COST, 1.6, dashed=True)
        old = dot(ax, a0["Q"], a0["P"], GREY_B, 0.09)
        pa = dot(ax, a["Q"], a["P"], SUPPLY, 0.11)
        pb = dot(ax, b["Q"], b["P"], COST, 0.11)
        side = VGroup(
            label(r"now demand rotates: \\ buyers become more \\ sensitive to price", font_size=18, color=DEMAND),
            label(rf"A: \ price {a['P']:.2f}, \\ quantity {a['Q']:.2f}", font_size=19, color=SUPPLY),
            label(rf"B: \ price {b['P']:.2f}, \\ quantity {b['Q']:.2f}", font_size=19, color=COST),
            label(r"a monopolist answers \\ the slope of demand; \\ a price-taker does not", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.BRESNAHAN_1982.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "In 1982 Timothy Bresnahan and Lawrence Lau showed what breaks the tie. <bookmark mark='a'/> Suppose "
            "something rotates demand, making buyers more sensitive to price, as a cheaper substitute appearing "
            "would. <bookmark mark='b'/> A competitive industry does not care about the slope of demand: it "
            "produces where demand meets its supply curve. <bookmark mark='c'/> A monopolist cares a great deal: "
            "more sensitive buyers mean a smaller markup. So the two stories now predict different prices and "
            f"quantities: {a['P']:.2f} against {b['P']:.2f}. <bookmark mark='d'/> Market power becomes a "
            "parameter that can be estimated, provided the data contain something that rotates demand and not just "
            "something that shifts it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(d0), Create(sup), Create(mc), FadeIn(old), run_time=1.5)
            vo.wait_until("a")
            self.play(ReplacementTransform(d0.copy(), d1), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(pa, scale=1.6), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(mr), FadeIn(pb, scale=1.6), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def lesson(self):
        lines = VGroup(
            MathTex(r"p \;=\; c(q) \;-\; \theta\, q\, \frac{\partial p}{\partial q}", font_size=46),
            MathTex(r"\theta = 0:\ \text{competition} \qquad \theta = 1:\ \text{monopoly or cartel}", font_size=34,
                    color=E.ACCENT),
        ).arrange(DOWN, buff=0.5).move_to(UP * 1.3)
        cards = point_cards([
            (r"the idea", r"conduct as one \\ number, \ estimated \\ like any other", THEORY),
            (r"what it needs", r"a demand rotator \\ and a model of \\ marginal cost", DEMAND),
            (r"the trouble", r"one industry, \ one \\ product, \ and much \\ resting on \\ functional form", HOLD),
        ], width=11.4, cols=3, font_size=19).move_to(DOWN * 1.5)
        tag = published_tag(tables.BRESNAHAN_1982.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The idea became a method. <bookmark mark='a'/> Write the industry's pricing rule as price equals "
            "marginal cost plus a markup scaled by a conduct parameter, theta. <bookmark mark='b'/> Theta of zero is "
            "competition; theta of one is monopoly, or a cartel acting like one. <bookmark mark='c'/> Estimate "
            "theta like any other parameter. <bookmark mark='d'/> It needs a variable that rotates demand, and a "
            "model of marginal cost. <bookmark mark='e'/> Its trouble is that real industries sell many different "
            "products, and much rests on the shape assumed for demand. Measuring market power in the cereal aisle "
            "needed demand for many products at once."
        ) as vo:
            self.play(Write(lines[0]), FadeIn(tag), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            for mk, c in zip("cde", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
