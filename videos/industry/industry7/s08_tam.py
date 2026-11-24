from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry7.common import *  # noqa: F403


class Tam(VoiceoverScene):
    def construct(self):
        card(self, 9, "Addressable markets", "What is a 'total addressable market' actually counting?",
             "Chapter nine. Addressable markets.", lit=("unit",))
        self.uber()
        self.eats()
        self.rings()
        self.funnel()

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

    def eats(self):
        """Uber Eats' $2.8 trillion: every restaurant meal on Earth, the ones eaten at the table included."""
        parts = [("eat-in", get("uber.eats.eatin"), "#4A5468"), ("takeaway", get("uber.eats.takeaway"), GUESS),
                 ("drive-through", get("uber.eats.drive"), UNITS), ("home delivery", get("uber.eats.delivery"), RETAIL)]
        tot = sum(v for _, v, _ in parts)
        L = 12.0
        segs, labs = VGroup(), VGroup()
        x = -L / 2
        for k, (name, v, col) in enumerate(parts):
            w = L * v / tot
            seg = Rectangle(width=w, height=1.1, stroke_color="#0E1117", stroke_width=2, fill_color=col,
                            fill_opacity=0.9).move_to([x + w / 2, 0.2, 0])
            lab = VGroup(tx(name, 17, col if k else GREY_A, bold=True), tx(f"${v:,.0f}bn", 16, GREY_B)).arrange(
                DOWN, buff=0.03)
            lab.next_to(seg, UP if k % 2 == 0 else DOWN, buff=0.18)
            segs.add(seg)
            labs.add(lab)
            x += w
        sam = BraceBetweenPoints(segs[1].get_corner(DL) + DOWN * 0.95, segs[3].get_corner(DR) + DOWN * 0.95, DOWN,
                                 color=GOLD)
        samt = tx(f"Uber Eats' SAM: ${get('uber.eats.sam'):.0f}bn", 19, GOLD, bold=True).next_to(sam, DOWN, buff=0.1)
        tam = BraceBetweenPoints(segs[0].get_corner(UL) + UP * 0.95, segs[3].get_corner(UR) + UP * 0.95, UP, color=TAM)
        tamt = tx(f"TAM: all of it, ${get('uber.tam.eats'):.1f}tn", 19, TAM, bold=True).next_to(tam, UP, buff=0.1)
        bk = get("uber.eats.bookings")
        zoom = VGroup(*[sg.copy() for sg in segs[1:]])
        zt = zoom.copy().stretch_to_fit_width(L).move_to([0, -2.15, 0])
        guides = VGroup(DashedLine(segs[1].get_corner(DL), zt.get_corner(UL), stroke_color=GREY_C, stroke_width=1.5),
                        DashedLine(segs[3].get_corner(DR), zt.get_corner(UR), stroke_color=GREY_C, stroke_width=1.5))
        sliver = Rectangle(width=L * bk / get("uber.eats.sam"), height=1.1, stroke_width=0, fill_color=WHITE,
                           fill_opacity=1).move_to(zt.get_right(), aligned_edge=RIGHT)
        bt = VGroup(tx(f"Uber Eats, 2018: ${bk:.1f}bn of orders", 17, WHITE, bold=True),
                    tx(f"{100 * bk / get('uber.eats.sam'):.0f}% of the SAM, {100 * bk / tot:.1f}% of the TAM", 15, GREY_B)
                    ).arrange(DOWN, buff=0.03).next_to(zt, DOWN, buff=0.15).align_to(zt, RIGHT)
        zl = tx("the SAM, stretched to full width", 15, GREY_B).next_to(zt, DOWN, buff=0.15).align_to(zt, LEFT)
        plates = VGroup(*[VGroup(Circle(radius=0.22, stroke_color=GREY_B, stroke_width=2, fill_color="#E8E4DA",
                                        fill_opacity=0.9), Circle(radius=0.12, stroke_width=0, fill_color=GUESS,
                                                                  fill_opacity=0.8)) for _ in range(6)]
                        ).arrange(RIGHT, buff=0.15).to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.6)
        src = source("Uber Technologies, Form S-1, 2019, citing Euromonitor International (Consumer Foodservice, 2019 "
                     "edition); spend in 2017, Uber Eats' gross bookings in 2018", size=13)
        with self.voiceover(
            "The restaurant part was built the same way. <bookmark mark='a'/> The prospectus took a commercial "
            "tracker's estimate of everything the world's consumers spent in restaurants, cafés and bars in 2017, "
            f"{get('uber.tam.eats'):.1f} trillion dollars, and split it by how the meal was eaten. "
            f"<bookmark mark='b'/> Home delivery: {get('uber.eats.delivery'):.0f} billion. Takeaway and drive-through: "
            f"{get('uber.eats.takeaway') + get('uber.eats.drive'):.0f} billion more. Together, the "
            f"{get('uber.eats.sam'):.0f} billion that Uber called the market it could serve. <bookmark mark='c'/> And "
            f"then the TAM: all of it, the {get('uber.eats.eatin') / 1000:.1f} trillion dollars of meals eaten at a "
            "restaurant table included, on the argument that some of those dinners might one day be delivered. "
            "<bookmark mark='d'/> Against that, Uber Eats took orders worth "
            f"{bk:.1f} billion dollars in 2018. Notice that this is what customers paid, food and all; Uber's own "
            "revenue was the cut it kept. And notice the years: a spend from 2017 set against orders from 2018. "
            "A good TAM reader checks both."
        ) as vo:
            frame = Rectangle(width=L, height=1.1, stroke_color=GREY_C, stroke_width=2, fill_opacity=0).move_to([0, 0.2, 0])
            ehead = tx("Uber Eats: what is the market for a meal?", 24, WHITE, bold=True).to_edge(UP, buff=1.1)
            self.play(FadeIn(src), Create(frame), FadeIn(ehead), LaggedStart(*[FadeIn(p_, scale=0.6) for p_ in plates],
                                                                             lag_ratio=0.1))
            vo.wait_until("a")
            self.play(GrowFromEdge(segs[0], LEFT), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(segs[k], LEFT), FadeIn(labs[k])) for k in (3, 1, 2)],
                                  lag_ratio=0.4), run_time=2.0)
            self.play(GrowFromCenter(sam), FadeIn(samt))
            vo.wait_until("c")
            self.play(GrowFromCenter(tam), FadeIn(tamt))
            vo.wait_until("d")
            self.play(FadeOut(sam), FadeOut(samt), FadeOut(labs[1]), FadeOut(labs[3]))
            self.play(Create(guides), Transform(zoom, zt), FadeIn(zl), run_time=1.6)
            self.play(GrowFromEdge(sliver, RIGHT), FadeIn(bt))
            self.play(Flash(sliver.get_center(), color=WHITE, line_length=0.25))
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
        rhead = tx("Three rings", 26, WHITE, bold=True).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Prospectuses draw this as three rings. <bookmark mark='a'/> The outer one, the total addressable market: "
            "everything that could be done the company's way, if the whole world switched. <bookmark mark='b'/> "
            "Inside it, the serviceable market: the part where the company actually operates, and for the kind of "
            f"trip it serves. For Uber, {U['sam']:.1f} trillion dollars. <bookmark mark='c'/> And at the centre, too "
            "small to see at this scale, what the company actually sells. Analysts sometimes add a third name for a ring "
            "between them, the serviceable obtainable market: the share the company could realistically win in the "
            "next few years. It is the one most worth arguing about, and the one prospectuses least often print. "
            "<bookmark mark='d'/> The outer ring "
            "answers a question about ambition: how big would this be if everyone did it our way? It is not a "
            "forecast, and it is not a market in the sense this series uses the word: buyers who are paying, now, "
            "for something, at a price. Read it as the company's dream, and look for the inner rings."
        ) as vo:
            self.play(FadeIn(src), FadeIn(rhead), Create(tam.copy().set_fill(opacity=0).set_stroke(opacity=0.35)))
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

    def funnel(self):
        """The inner ring, built bottom-up from Uber's own prospectus: people x trips x fare x take."""
        users, trips, book, net = (get(k) for k in ("uber.mapcs.2018", "uber.trips.2018", "uber.bookings.2018",
                                                    "uber.netrev.2018"))
        per_user = trips / users
        fare = book * 1000 / trips
        take = net / book
        steps = [(draw.crowd(8, h=0.32, color=STONE, cols=4), f"{users:.0f}m", "people using it each month"),
                 (VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.55, height=0.2, stroke_width=0,
                                            fill_color="#7EC8F5", fill_opacity=0.9) for _ in range(3)]).arrange(DOWN, buff=0.08),
                  f"x {per_user:.0f}", "trips each in the year"),
                 (draw.coin_stack(4, r=0.18), f"x ${fare:.2f}", "paid per trip, on average"),
                 (VGroup(draw.coin(0.2), tx("20%", 16, GOLD, bold=True)).arrange(RIGHT, buff=0.08), f"x {100 * take:.0f}%",
                  "kept by Uber")]
        cells = VGroup()
        for pic, num, lab in steps:
            pic.scale_to_fit_height(min(pic.height, 0.9))
            cells.add(VGroup(pic, tx(num, 30, WHITE, bold=True), tx(lab, 15, GREY_A)).arrange(DOWN, buff=0.15))
        cells.arrange(RIGHT, buff=0.7).move_to([0, 0.8, 0])
        res = VGroup(tx(f"= {trips / 1000:.2f}bn trips", 22, "#7EC8F5", bold=True),
                     tx(f"= ${book:.1f}bn of gross bookings", 22, WHITE, bold=True),
                     tx(f"= ${net:.1f}bn of revenue", 26, GOLD, bold=True)).arrange(DOWN, buff=0.18).move_to([0, -1.6, 0])
        cmp_ = tx(f"against a 'market' of ${R['uber']['tam']:.1f} trillion", 18, TAM).next_to(res, DOWN, buff=0.25)
        src = source("Uber Technologies, Form S-1, 2019 (2018: monthly active platform consumers, trips, gross bookings, "
                     "core platform adjusted net revenue); this film's division", size=13)
        with self.voiceover(
            "Now size the inner ring the other way, bottom-up, from the same prospectus. <bookmark mark='a'/> In late "
            f"2018 about {users:.0f} million people used Uber in a month. <bookmark mark='b'/> Over the year there were "
            f"{trips / 1000:.1f} billion trips, rides and meals together: about {per_user:.0f} for each of those "
            f"people. <bookmark mark='c'/> They paid, on average, about {fare:.2f} dollars a trip: "
            f"{book:.1f} billion dollars in all, which Uber calls gross bookings. <bookmark mark='d'/> Most of that went "
            f"to drivers and restaurants. Uber kept about a fifth: {net:.0f} billion dollars. <bookmark mark='e'/> "
            "People, times trips, times fare, times the share kept: that is a market you can check, line by line, "
            "against the company's own accounts. Twelve trillion dollars is not."
        ) as vo:
            self.play(FadeIn(src), FadeIn(cells[0][0]))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                anims = [FadeIn(cells[k][0]), FadeIn(cells[k][1:], shift=UP * 0.1)]
                if k:
                    anims.append(FadeIn(res[k - 1], shift=UP * 0.1))
                self.play(*anims, run_time=1.0)
            vo.wait_until("e")
            self.play(FadeIn(cmp_), Indicate(res[2], color=WHITE))
        self.clear_scene()
