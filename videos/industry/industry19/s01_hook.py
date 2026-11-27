from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.otis()
        self.backlog()
        self.title()

    def otis(self):
        H = R["hook"]
        lift = draw.elevator(4.4, floors=8, color=BLUE).move_to([-4.6, -0.2, 0])
        s = 2.2 / H["sv_sales"]  # screen units per $m of sales

        def pair(x, sales, op, col, name):
            bar = Rectangle(width=1.3, height=sales * s * 1.3, stroke_width=0, fill_color=col, fill_opacity=0.35)
            bar.move_to([x, -2.2 + bar.height / 2, 0])
            bar.grow = DOWN
            pr = Rectangle(width=1.3, height=max(op * s * 1.3, 0.03), stroke_width=0, fill_color=col, fill_opacity=1)
            pr.move_to([x, -2.2 + pr.height / 2, 0])
            pr.grow = DOWN
            lab = VGroup(tx(name, 18, col, bold=True), tx(f"sales ${sales / 1e3:.1f}bn", 15, GREY_A),
                         tx(f"profit ${op / 1e3:.2f}bn ({100 * op / sales:.1f}%)", 15, col, bold=True)).arrange(DOWN, buff=0.06)
            lab.next_to(bar, UP, buff=0.15)
            return VGroup(bar, lab), pr
        ne, ne_p = pair(-0.6, H["ne_sales"], H["ne_op"], MACHINE, "new elevators")
        sv, sv_p = pair(2.6, H["sv_sales"], H["sv_op"], SERVICE, "service")
        base = Line([-1.8, -2.2, 0], [4.0, -2.2, 0], stroke_color=GREY_B, stroke_width=2)
        units = tx(f"about {H['units']:.1f} million lifts and escalators under its maintenance", 16, SERVICE, bold=True).to_edge(DOWN, buff=0.7).shift(RIGHT * 1.2)
        src = source("Otis Worldwide Corporation, Form 10-K 2025: New Equipment and Service segments", size=12)

        def ride(vo):
            car = lift.car
            for k in (5, 2, 7):
                self.play(car.animate.set_y(lift.floor_y(k)), run_time=1.0)

        beat(self,
             "Otis builds elevators, and calls itself the world's largest elevator and escalator company. "
             "<bookmark mark='a'/> In 2025 it sold "
             f"{H['ne_sales'] / 1e3:.1f} billion dollars of new elevators and escalators, and made a profit on them of "
             f"{H['ne_op'] / 1e3:.2f} billion: {100 * H['ne_op'] / H['ne_sales']:.1f} cents on the dollar. "
             "<bookmark mark='b'/> It also maintains, repairs and modernizes them. That business sold "
             f"{H['sv_sales'] / 1e3:.1f} billion dollars and made {H['sv_op'] / 1e3:.1f} billion: "
             f"{100 * H['sv_op'] / H['sv_sales']:.0f} cents on the dollar. <bookmark mark='c'/> Otis looks after about "
             f"{H['units']:.1f} million lifts and escalators, its own and other makers'. And the two lines are moving "
             f"apart: since 2023 new-equipment sales have fallen from {H['ne23'] / 1e3:.1f} billion dollars to "
             f"{H['ne_sales'] / 1e3:.1f}, while service has grown from {H['sv23'] / 1e3:.1f} billion to "
             f"{H['sv_sales'] / 1e3:.1f}. The factory is the smaller part of the money, and getting smaller.",
             base=[lift, base, src], steps=[[ne, ne_p], [sv, sv_p], units], after=ride)

    def backlog(self):
        H = R["hook"]
        b24, b25, bq = H["backlog"]
        ex = draw.excavator(3.6, MACHINE).move_to([-4.4, 0.2, 0])
        items = [("end of 2024", b24, GREY_B, f"${b24:.1f}bn"), ("end of 2025", b25, MACHINE, f"${b25:.1f}bn"),
                 ("September 2026", bq, PRICE, f"${bq:.1f}bn")]
        bars_ = vbars(items, base_y=-2.3, height=3.8, width=1.2, gap=0.9, x0=0.4)
        hd = tx("Caterpillar's order backlog", 20, WHITE, bold=True).move_to([2.3, 2.6, 0])
        rob = tx(f"and {H['robots']:.0f} million industrial robots now at work in the world's factories", 17, ROBOT, bold=True).to_edge(DOWN, buff=0.45)
        src = source("Caterpillar Inc., Form 10-K 2025 and Form 10-Q for the third quarter of 2026; International "
                     "Federation of Robotics, 24 September 2026", size=12)

        def dig(vo):
            p = ex.pivot.get_center()
            self.play(Rotate(ex.boom, 0.3, about_point=p), rate_func=there_and_back, run_time=1.6)

        beat(self,
             "The machine makers are busy. <bookmark mark='a'/> Caterpillar, which calls itself the world's leading maker "
             f"of construction and mining equipment, had {b24:.0f} billion dollars of firm orders waiting at the end of 2024, <bookmark mark='b'/> "
             f"{b25:.0f} billion a year later, <bookmark mark='c'/> and {bq:.0f} billion by September 2026, much of it "
             "engines and turbines to power data centres. <bookmark mark='d'/> And the factories that use machines are "
             f"filling with robots: {H['robots']:.0f} million of them now, more than twice as many as seven years ago.",
             base=[ex, hd, src], steps=[bars_[0], bars_[1], bars_[2], rob], after=dig)

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part nineteen: machinery. How do the companies that make the machines earn "
                            "more from them after the sale than at it?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
