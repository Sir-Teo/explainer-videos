from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.robot()
        self.three()
        self.title()

    def robot(self):
        H = R["hook"]
        bot = draw.surgical_robot(3.0).move_to([-3.6, 0.2, 0])
        c = VGroup(tx(f"{H['procs'] / 1e6:.2f} million operations in 2025", 24, DEVICE, bold=True),
                   tx(f"{H['base']:,} robots installed worldwide", 20, WHITE),
                   tx(f"about {H['per_system']:.0f} operations a robot a year", 18, GREY_A)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.8, 1.0, 0])
        price = tx(f"one robot: ${H['price'][0]:.1f}m to ${H['price'][1]:.1f}m", 20, PRICE, bold=True).move_to([2.8, -0.9, 0])
        inst = tx(f"each operation: ${H['ia'][0]:,} to ${H['ia'][1]:,} of instruments that wear out", 18, GOOD, bold=True).move_to([2.8, -1.7, 0])
        src = source("Intuitive Surgical, Inc., Form 10-K 2025", size=12)

        def arms(vo):
            for k in range(2):
                self.play(*[a.animate.shift(DOWN * 0.08 * (1 if (i + k) % 2 else -1)) for i, a in enumerate(bot.arms)], run_time=0.6)
        beat(self,
             "In 2025 surgeons around the world performed about three point one five million operations with a robot made "
             "by one company, Intuitive. The surgeon sits at a console and moves the robot's arms, "
             "which hold the instruments inside the patient through small cuts. <bookmark mark='a'/> There were "
             f"{H['base']:,} of these robots in hospitals, each doing about {H['per_system']:.0f} operations a year. "
             f"<bookmark mark='b'/> A robot sells for between {H['price'][0]:.1f} and {H['price'][1]:.1f} million dollars. "
             "<bookmark mark='c'/> And every operation uses instruments with limited lives, which expire or wear out, worth "
             f"between {H['ia'][0]:,} and {H['ia'][1]:,} dollars to the company each time.",
             base=[src, bot, c[0]], steps=[c[1:], price, inst], after=arms)

    def three(self):
        sg = VGroup(draw.person(0.9, SURGEON), tx("the surgeon chooses", 17, SURGEON, bold=True)).arrange(DOWN, buff=0.12)
        hp = VGroup(draw.hospital(1.4), tx("the hospital buys", 17, WHITE, bold=True)).arrange(DOWN, buff=0.12)
        py = VGroup(draw.note_bill(1.0), tx("an insurer pays", 17, PAYER, bold=True)).arrange(DOWN, buff=0.12)
        pt = VGroup(draw.person(0.9, GOOD), tx("the patient is treated", 17, GOOD, bold=True)).arrange(DOWN, buff=0.12)
        row = VGroup(sg, hp, py, pt).arrange(RIGHT, buff=1.2).move_to([0, 0.5, 0])
        note = tx("Four people, one purchase.", 22, PRICE, bold=True).move_to([0, -2.0, 0])
        beat(self,
             "Who is the customer? <bookmark mark='a'/> The surgeon chooses the robot, and the instruments, and is trained "
             "on them. <bookmark mark='b'/> The hospital buys the robot and pays for the instruments. <bookmark mark='c'/> An "
             "insurer, or a government, pays the hospital for the operation. <bookmark mark='d'/> And the patient, who "
             "benefits, rarely sees the price at all. <bookmark mark='e'/> Medical technology sells to all four at once, and "
             "much of how the industry works follows from that.",
             steps=[sg, hp, py, pt, note])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part twenty-one: medical technology. Who is the customer when the one who uses "
                            "it, the one who chooses it and the one who pays are three different people?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
