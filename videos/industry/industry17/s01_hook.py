from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403

NAMES = {"TM": "Toyota", "VW": "Volkswagen", "GM": "General Motors", "F": "Ford", "STLA": "Stellantis",
         "HMC": "Honda", "BYD": "BYD", "TSLA": "Tesla"}


class Hook(VoiceoverScene):
    def construct(self):
        self.year()
        self.line()
        self.ohno()
        self.third()
        self.title()

    def year(self):
        M = R["hook"]["margins"]
        order = ["TM", "BYD", "TSLA", "VW", "GM", "HMC", "F", "STLA"]
        pa = viz.plot_axes([-0.2, 0.11], [0, len(order)], x_length=8.8, y_length=5.0,
                           xticks=[-0.15, -0.10, -0.05, 0, 0.05, 0.10], xfmt=lambda v: f"{100 * v:.0f}%",
                           grid=False, size=14).move_to([1.2, -0.35, 0])
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(0, len(order)), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        zl = tx("break-even", 13, GREY_B).next_to(pa.ax.c2p(0, len(order)), UP, buff=0.08)
        rows, ghosts = VGroup(), VGroup()
        for i, tk in enumerate(order):
            a, b = M[tk]
            y = len(order) - 0.5 - i
            name = tx(NAMES[tk], 16, WHITE, bold=True).next_to(pa.ax.c2p(-0.2, y), LEFT, buff=0.2)
            d0 = Dot(pa.ax.c2p(a, y), radius=0.08, color=GREY_B)
            d1 = Dot(pa.ax.c2p(b, y), radius=0.1, color=GOOD if b >= 0 else BAD)
            arr = Arrow(pa.ax.c2p(a, y), pa.ax.c2p(b, y), buff=0.1, stroke_width=3, color=GOOD if b >= a else BAD,
                        max_tip_length_to_length_ratio=0.35, tip_length=0.14)
            lab = tx(f"{100 * b:+.1f}%", 14, GOOD if b >= 0 else BAD, bold=True).next_to(d1, RIGHT if b >= a else LEFT, buff=0.12)
            rows.add(VGroup(name, d0, arr, d1, lab))
            ghosts.add(name.copy(), d0.copy())
        key = VGroup(Dot(radius=0.08, color=GREY_B), tx("2024", 14, GREY_B), Dot(radius=0.1, color=WHITE),
                     tx("2025 (Toyota and Honda: year to March 2026)", 14, WHITE)).arrange(RIGHT, buff=0.12).to_edge(UP, buff=0.95)
        head = tx("Net profit per dollar of revenue, 2024 and 2025", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("Forms 10-K of GM, Ford and Tesla and 20-F of Stellantis, Toyota and Honda (SEC); Volkswagen, Annual Report "
                     "2025; BYD, 2025 annual results (HKEX)", size=12)
        with self.voiceover(
            "In 2025 the world bought about ninety-one million new vehicles. <bookmark mark='a'/> Here is what the companies "
            "that make them kept of each dollar of revenue, the year before and that year. <bookmark mark='b'/> Toyota "
            f"kept {100 * M['TM'][1]:.1f} cents, down from almost ten. Volkswagen, {100 * M['VW'][1]:.1f}. "
            f"<bookmark mark='c'/> General Motors, {100 * M['GM'][1]:.1f}. And three of the best-known names in the business "
            f"lost money: Honda, Ford, <bookmark mark='d'/> and Stellantis, the maker of Jeep, Fiat and Peugeot, which lost "
            f"{-100 * M['STLA'][1]:.1f} cents on every dollar it took in. The car is the most desired consumer product of the "
            "last hundred years. Why is it so hard to make money making it?"
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(zl), FadeIn(head), FadeIn(src), FadeIn(ghosts))
            vo.wait_until("a")
            self.play(FadeIn(key), LaggedStart(*[FadeIn(r_[1]) for r_ in rows], lag_ratio=0.08), run_time=1.5)
            vo.wait_until("b")
            for k in range(0, 4):
                self.play(FadeIn(rows[k][0]), GrowArrow(rows[k][2]), FadeIn(rows[k][3]), FadeIn(rows[k][4]), run_time=0.6)
            vo.wait_until("c")
            for k in range(4, 7):
                self.play(FadeIn(rows[k][0]), GrowArrow(rows[k][2]), FadeIn(rows[k][3]), FadeIn(rows[k][4]), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(rows[7][0]), GrowArrow(rows[7][2]), FadeIn(rows[7][3]), FadeIn(rows[7][4]), run_time=0.8)
            self.play(Indicate(rows[7][3], color=BAD, scale_factor=1.8))
        self.clear_scene()

    def line(self):
        F = R["hook"]["ford"]
        floor = Line([-6.8, -0.6, 0], [6.8, -0.6, 0], stroke_color=GREY_B, stroke_width=3)
        rope = DashedLine([-6.8, -0.35, 0], [6.8, -0.35, 0], stroke_color=PRICE, stroke_width=2, dash_length=0.12)
        chassis = VGroup(*[draw.chassis(1.7, "#9AA3B2", parts=k) for k in range(6)])
        for k, c in enumerate(chassis):
            c.move_to([-5.6 + 2.3 * k, 0, 0]).align_to(np.array([0, -0.6, 0]), DOWN)
        workers = VGroup(*[draw.person(0.62, "#C9D3E0").move_to([-4.45 + 2.3 * k, 0, 0]).align_to(np.array([0, -0.6, 0]), DOWN)
                           for k in range(5)])
        mag = VGroup(tx("the fly-wheel magneto, April 1913:", 15, GREY_A),
                     tx(f"about {F['magneto'][0]:.0f} minutes for one worker,", 15, WHITE),
                     tx(f"{F['magneto'][1]:.0f} minutes on the line", 17, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).to_corner(UL, buff=0.4).shift(DOWN * 0.55)
        head = tx("Highland Park, Michigan, 1913-1914", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        times = [("standing still, 1913", F["chassis"][0], GREY_B), ("drawn by a rope", F["chassis"][1], SUPPLIER),
                 ("the moving line, 1914", F["chassis"][2], PRICE)]
        bars = VGroup()
        for i, (name, h, col) in enumerate(times):
            y = -1.55 - 0.62 * i
            b = bar(-3.2, y, 0.62 * h, 0.4, col)
            hh, mm = int(h), round((h - int(h)) * 60)
            lab = tx(f"{hh} h {mm:02d} min", 17, col, bold=True).next_to(b, RIGHT, buff=0.15)
            nm = tx(name, 15, GREY_A).next_to([-3.3, y, 0], LEFT, buff=0.1)
            bars.add(VGroup(nm, b, lab))
        quote = VGroup(tx("'The idea came in a general way from the overhead trolley", 15, WHITE),
                       tx("that the Chicago packers use in dressing beef.'", 15, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).to_corner(UR, buff=0.4).shift(DOWN * 0.55)
        what = tx("time to assemble one chassis", 15, GREY_B).move_to([-3.1, -1.05, 0], aligned_edge=LEFT)
        src = source("Henry Ford with Samuel Crowther, My Life and Work (1922), chapter V, pp. 81-83", size=13)
        with self.voiceover(
            f"Mass production of cars began in one building. <bookmark mark='a'/> On the first of April, {F['year']:.0f}, at Ford's "
            "Highland Park plant in Michigan, a line of workers began assembling the flywheel magneto, a small part of the "
            "Model T's ignition, each one sliding along from one worker to the next. One worker had needed about twenty minutes to build "
            f"one; on the line it took {F['magneto'][1]:.0f}. Henry Ford wrote that the idea came from the overhead trolleys of "
            "the Chicago meat packers. <bookmark mark='b'/> Then the whole car. Standing still, a team needed twelve hours "
            "and twenty-eight minutes to assemble a chassis. <bookmark mark='c'/> Pulled by a rope and a windlass down a line "
            "two hundred and fifty feet long, past piles of parts, with six assemblers walking alongside: five hours and "
            "fifty minutes. <bookmark mark='d'/> On a raised moving line in 1914: one hour and thirty-three minutes. Mass "
            "production had begun."
        ) as vo:
            self.play(FadeIn(floor), FadeIn(head), FadeIn(src), FadeIn(ghost(chassis, workers, opacity=0.3)))
            vo.wait_until("a")
            self.play(FadeIn(workers), FadeIn(quote), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(m_, shift=RIGHT * 0.1) for m_ in mag], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(chassis[0]), FadeIn(what), FadeIn(bars[0]), run_time=1.0)
            vo.wait_until("c")
            self.play(Create(rope), FadeIn(bars[1]), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(c) for c in chassis[1:]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(bars[2]), chassis.animate.shift(RIGHT * 2.3), run_time=2.0, rate_func=linear)
            self.play(chassis.animate.shift(RIGHT * 2.3), run_time=2.0, rate_func=linear)
        self.clear_scene()

    def ohno(self):
        koromo = R["hook"]["koromo"]
        loom = VGroup(Rectangle(width=1.6, height=1.0, stroke_color=GREY_B, stroke_width=2, fill_opacity=0),
                      *[Line([-0.7, y, 0], [0.7, y, 0], stroke_color=SUPPLIER, stroke_width=1.5) for y in np.linspace(-0.35, 0.35, 8)],
                      Line([-0.8, -0.5, 0], [-0.8, -1.1, 0], stroke_color=GREY_B, stroke_width=3),
                      Line([0.8, -0.5, 0], [0.8, -1.1, 0], stroke_color=GREY_B, stroke_width=3)).move_to([-4.2, 0.4, 0])
        stop = VGroup(Circle(radius=0.22, stroke_width=0, fill_color=BAD, fill_opacity=1), tx("STOP", 10, WHITE, bold=True)).move_to([-3.2, 1.2, 0])
        cards = VGroup(*[draw.kanban(0.75) for _ in range(3)]).arrange(RIGHT, buff=0.15).move_to([2.6, 0.6, 0])
        l1 = VGroup(tx("Just-in-Time", 22, PRICE, bold=True),
                    tx("Kiichiro Toyoda: 'we could have a mountain of parts", 15, WHITE),
                    tx("and still not be able to build a car'", 15, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([2.6, -1.0, 0])
        l2 = VGroup(tx("Jidoka", 22, PRICE, bold=True), tx("'automation with a human touch':", 15, WHITE),
                    tx("Sakichi Toyoda's loom of 1896 stopped", 15, WHITE), tx("itself when a thread broke", 15, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([-4.0, -1.5, 0])
        head = tx("Toyota City, after the war", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source(f"Toyota Motor Corporation, 'Toyota Production System' (the Koromo Plant's flow line, {koromo:.0f})", size=13)
        with self.voiceover(
            "The second arrival came from Japan. <bookmark mark='a'/> Toyota's roots are in looms. In 1896 Sakichi Toyoda "
            "built a power loom that stopped itself when a thread broke, so that no bad cloth was made and no one had to "
            "stand watching the machine. Toyota calls the idea jidoka: automation with a human touch. <bookmark mark='b'/> "
            "His son Kiichiro, who started the car company, put the other idea this way: 'A complete car cannot be built if "
            "even one part is missing... without this control, we could have a mountain of parts and still not be able to "
            "build a car.' Make only what is needed, when it is needed: just in time. <bookmark mark='c'/> After the war "
            "Taiichi Ohno, backed by Eiji Toyoda, built the two ideas into the Toyota Production System, with its little "
            "cards, called kanban, that tell each step only what the step after it has used. Carmakers everywhere later set "
            "out to copy it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ghost(loom, cards, opacity=0.3)))
            vo.wait_until("a")
            self.play(FadeIn(loom), FadeIn(l2))
            self.play(GrowFromCenter(stop))
            vo.wait_until("b")
            self.play(FadeIn(l1, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.4) for c in cards], lag_ratio=0.3), run_time=1.5)
            self.play(cards.animate.shift(LEFT * 0.6), run_time=1.0)
        self.clear_scene()

    def third(self):
        H = R["hook"]
        evw, cx = H["ev_world"], H["china_exports"]
        left = VGroup(tx("Electric share of new cars sold worldwide", 17, WHITE, bold=True),
                      VGroup(tx(f"{evw[2015]:.1f}%", 44, GREY_B, bold=True), tx("2015", 16, GREY_B)).arrange(DOWN, buff=0.06),
                      ).arrange(DOWN, buff=0.3)
        l25 = VGroup(tx(f"{evw[2025]:.0f}%", 60, EV, bold=True), tx("2025", 16, EV)).arrange(DOWN, buff=0.06)
        right = VGroup(tx("China's exports of passenger cars", 17, WHITE, bold=True),
                       VGroup(tx(f"${cx[2015]:.0f}bn", 44, GREY_B, bold=True), tx("2015", 16, GREY_B)).arrange(DOWN, buff=0.06),
                       ).arrange(DOWN, buff=0.3)
        r25 = VGroup(tx(f"${cx[2025]:.0f}bn", 60, COUNTRY_COL["China"], bold=True), tx("2025", 16, COUNTRY_COL["China"])).arrange(DOWN, buff=0.06)
        left.move_to([-3.4, 1.0, 0])
        right.move_to([3.4, 1.0, 0])
        l25.next_to(left, DOWN, buff=0.5)
        r25.next_to(right, DOWN, buff=0.5)
        pack = draw.battery_pack(2.0).next_to(l25, DOWN, buff=0.4)
        ship_ = draw.car_carrier(2.4).next_to(r25, DOWN, buff=0.4)
        src = source("IEA, Global EV Outlook 2026 via Our World in Data (battery electric and plug-in hybrid cars); UN Comtrade, "
                     "China's exports of HS 8703 as reported by China", size=12)
        with self.voiceover(
            "And now a third arrival. <bookmark mark='a'/> In 2015, fewer than one new car in a hundred sold in the world "
            f"ran on a battery. <bookmark mark='b'/> In 2025, {evw[2025]:.0f} in a hundred did, counting plug-in hybrids. "
            f"<bookmark mark='c'/> And China, which in 2015 exported {cx[2015]:.0f} billion dollars' worth of cars, "
            f"<bookmark mark='d'/> exported {cx[2025]:.0f} billion in 2025, more by value than Japan. This film follows the "
            "money through the business, from the plant to the dealer to the loan, and asks where it goes, and why so "
            "little of it stays with the people who make the car."
        ) as vo:
            self.play(FadeIn(src), FadeIn(left[0]), FadeIn(right[0]), FadeIn(ghost(l25, r25, opacity=0.25)))
            vo.wait_until("a")
            self.play(FadeIn(left[1]))
            vo.wait_until("b")
            self.play(FadeIn(l25, shift=UP * 0.2), FadeIn(pack))
            vo.wait_until("c")
            self.play(FadeIn(right[1]))
            vo.wait_until("d")
            self.play(FadeIn(r25, shift=UP * 0.2), FadeIn(ship_))
            self.play(ship_.animate.shift(RIGHT * 1.2), run_time=2.0)
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover(
            "Industry, Built. Part seventeen: automobiles. Why is it so hard to make money making the most desired product "
            "of the century?"
        ):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
