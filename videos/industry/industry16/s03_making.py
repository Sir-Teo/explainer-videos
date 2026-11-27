from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403

STATIONS = ["solder paste", "pick and place", "reflow oven", "inspection", "final assembly", "test", "box"]
APPLE_PLACES = {"China mainland": (114.0, 22.6), "India": (80.2, 13.0), "Japan": (139.7, 35.7), "South Korea": (127.0, 37.5),
                "Taiwan": (121.0, 24.8), "Vietnam": (105.8, 21.0)}


class Making(VoiceoverScene):
    def construct(self):
        card(self, 2, "From design to box", "What happens between a design and a device in a box?",
             "Chapter two. From design to box.", lit=("make",))
        self.line()
        self.scale()
        self.who()

    def line(self):
        xs = np.linspace(-5.6, 5.6, len(STATIONS))
        belt = RoundedRectangle(corner_radius=0.1, width=12.6, height=0.22, stroke_color=GREY_B, stroke_width=2, fill_color="#1B2230",
                                fill_opacity=1).move_to([0, -1.25, 0])
        rollers = VGroup(*[Circle(radius=0.08, stroke_color=GREY_B, stroke_width=1.5).move_to([x, -1.25, 0]) for x in np.linspace(-6.1, 6.1, 25)])
        boxes = VGroup()
        for x, name in zip(xs, STATIONS):
            b = RoundedRectangle(corner_radius=0.08, width=1.45, height=0.9, stroke_color=GREY_B, stroke_width=2, fill_color="#151A23", fill_opacity=1).move_to([x, 0.6, 0])
            boxes.add(VGroup(b, tx(name, 13, WHITE, bold=True).move_to(b)))
        boxes[2][0].set_fill("#4A2A1A")
        board = draw.pcb(1.1, BOARD, parts=True)
        parts = board.parts
        parts.set_opacity(0)
        board.move_to([xs[0], -0.85, 0])
        phone = draw.phone(0.9, screen="#1B2230").move_to([xs[4], -0.6, 0])
        check = tx("pass", 16, GOOD, bold=True).move_to([xs[5], -0.15, 0])
        box = draw.carton(0.8).move_to([xs[6], -0.75, 0])
        head = tx("A device's last steps: a surface-mount line, then assembly and test", 20, WHITE, bold=True).to_edge(UP, buff=0.4)
        tag = estimate_tag("a schematic of the process, not a particular factory", corner=DR, size=12)
        with self.voiceover(
            "A device starts as a design, but it is built in a few hours on a line like this. <bookmark mark='a'/> A bare "
            "circuit board enters. A printer lays solder paste through a stencil onto its pads. <bookmark mark='b'/> A "
            "pick-and-place machine sets the chips and the tiny resistors and capacitors onto the paste, many thousands an "
            "hour. <bookmark mark='c'/> An oven melts the solder, and cameras check every joint. <bookmark mark='d'/> Then "
            "final assembly: the board goes into the case with the screen, the battery and the cameras, mostly by hand. "
            "<bookmark mark='e'/> Every device is tested, <bookmark mark='f'/> boxed and shipped. Almost every part on that "
            "board was made by someone else; the line's own contribution is the putting together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(belt), FadeIn(rollers), LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.08), FadeIn(board))
            vo.wait_until("a")
            self.play(board.animate.move_to([xs[0], -0.85, 0]), Indicate(boxes[0], color=PARTS, scale_factor=1.05))
            vo.wait_until("b")
            self.play(board.animate.move_to([xs[1], -0.85, 0]), run_time=1.0)
            self.play(LaggedStart(*[p_.animate.set_opacity(1) for p_ in parts], lag_ratio=0.15), Indicate(boxes[1], color=PARTS, scale_factor=1.05), run_time=1.5)
            vo.wait_until("c")
            self.play(board.animate.move_to([xs[2], -0.85, 0]), run_time=1.0)
            self.play(Flash(board, color=ASSEMBLER, line_length=0.3, num_lines=12), boxes[2][0].animate.set_fill("#A0522D"))
            self.play(board.animate.move_to([xs[3], -0.85, 0]), boxes[2][0].animate.set_fill("#4A2A1A"), Indicate(boxes[3], color=GOOD, scale_factor=1.05))
            vo.wait_until("d")
            self.play(board.animate.move_to([xs[4], -0.85, 0]).scale(0.5), run_time=1.0)
            self.play(FadeIn(phone, scale=0.8), FadeOut(board))
            vo.wait_until("e")
            self.play(phone.animate.move_to([xs[5], -0.6, 0]))
            self.play(FadeIn(check, shift=UP * 0.1))
            vo.wait_until("f")
            self.play(phone.animate.move_to([xs[6], -0.6, 0]).scale(0.6), FadeOut(check))
            self.play(FadeIn(box, scale=0.8), FadeOut(phone))
        self.clear_scene()

    def who(self):
        wm = draw.world_map(8.2, lon=(60, 150), lat=(0, 50)).move_to([-2.6, 0.2, 0])
        dots = VGroup(*[Dot(wm.p(*ll), radius=0.12, color=ASSEMBLER).set_z_index(3) for ll in APPLE_PLACES.values()])
        names = VGroup(*[tx(n, 13, WHITE, bold=True).next_to(d, RIGHT if n not in ("India",) else LEFT, buff=0.08).set_z_index(3)
                         for n, d in zip(APPLE_PLACES, dots)])
        names[0].shift(DOWN * 0.15)
        quote = VGroup(tx("'Substantially all of the Company's hardware", 14, WHITE), tx("products are manufactured by outsourcing", 14, WHITE),
                       tx("partners that are located primarily in China", 14, WHITE), tx("mainland, India, Japan, South Korea,", 14, WHITE),
                       tx("Taiwan and Vietnam.'  Apple, 10-K, 2026", 14, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.03).move_to([4.2, 2.2, 0])
        C = R["contract"]
        flex = VGroup(tx("Flex, one of the contract manufacturers:", 15, GREY_A),
                      tx(f"{C['flex_staff']:,.0f} people", 22, ASSEMBLER, bold=True),
                      tx("in more than 100 facilities in about 30 countries", 14, GREY_A),
                      tx(f"{C['flex_china']:.0f}% of its sales made in China", 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.2, -0.9, 0])
        src = source("Apple, Form 10-K FY2026; Flex, Form 10-K FY2026 (to 31 March 2026)", size=13)
        with self.voiceover(
            "Who does that work? Very often not the company whose name is on the box. <bookmark mark='a'/> Apple's annual "
            "report says that substantially all of its hardware is made by outsourcing partners, primarily in China, India, "
            "Japan, South Korea, Taiwan and Vietnam. <bookmark mark='b'/> The partners are companies most people have never "
            f"heard of. Flex, one of the big contract manufacturers, employed about {C['flex_staff']:,.0f} people in more "
            "than a hundred facilities across some thirty countries, building for other companies' brands."
        ) as vo:
            self.play(FadeIn(wm), FadeIn(src), FadeIn(ghost(quote, flex, opacity=0.2)))
            vo.wait_until("a")
            self.play(FadeIn(quote, shift=LEFT * 0.1), LaggedStart(*[AnimationGroup(GrowFromCenter(d), FadeIn(n)) for d, n in zip(dots, names)], lag_ratio=0.2),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(flex, shift=UP * 0.1))
        self.clear_scene()

    def scale(self):
        T = R["tariffs"]
        U, V = T["units"], T["unit_value"]
        ph, lp = U["phones"]["World"][2025], U["laptops"]["World"][2025]
        per = 5
        def grid(n, icon, x):
            g = VGroup(*[icon() for _ in range(n)]).arrange_in_grid(cols=7, buff=(0.14, 0.12))
            return g.move_to([x, -0.4, 0])
        gp = grid(int(round(ph / per)), lambda: draw.phone(0.34, screen=BRAND), -3.4)
        gl = grid(int(round(lp / per)), lambda: draw.laptop(0.42, screen=PARTS), 3.0)
        lp_ = VGroup(tx(f"{ph:.0f} million smartphones", 20, BRAND, bold=True),
                     tx(f"average value at the border: ${V['phones'][2025]:.0f}", 15, GREY_A)).arrange(DOWN, buff=0.05).next_to(gp, UP, buff=0.25)
        ll = VGroup(tx(f"{lp:.0f} million laptops", 20, PARTS, bold=True),
                    tx(f"average value at the border: ${V['laptops'][2025]:.0f}", 15, GREY_A)).arrange(DOWN, buff=0.05).next_to(gl, UP, buff=0.25)
        key = tx(f"each icon: {per} million, imported into the United States in 2025", 13, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("UN Comtrade: US imports of smartphones (HS 851713) and laptops (847130), units and value, 2025", size=13)
        with self.voiceover(
            "How many come off lines like that? Take one country's purchases. <bookmark mark='a'/> In 2025 the United "
            f"States imported about {ph:.0f} million smartphones, declared at the border at about "
            f"${V['phones'][2025]:.0f} each on average. <bookmark mark='b'/> And about {lp:.0f} million laptops, at about "
            f"${V['laptops'][2025]:.0f}. That is the value declared at customs, as the devices arrive; the price in the shop "
            "is higher."
        ) as vo:
            self.play(FadeIn(src), FadeIn(key), FadeIn(lp_[0]), FadeIn(ll[0]), FadeIn(ghost(gp, gl, opacity=0.4)))
            vo.wait_until("a")
            self.play(FadeIn(lp_[1]), LaggedStart(*[FadeIn(i, scale=0.5) for i in gp], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ll[1]), LaggedStart(*[FadeIn(i, scale=0.5) for i in gl], lag_ratio=0.03), run_time=2.0)
        self.clear_scene()
