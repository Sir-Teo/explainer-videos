from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, module_box, trace


class Warehouse(VoiceoverScene):
    def construct(self):
        self.card()
        self.building()
        self.power()
        self.proportional()
        self.pue()
        self.failure()

    def card(self):
        card = chapter_card(1, r"The warehouse-scale computer", r"What is a computer, when the computer is a building?",
                            lit=(2007, 2009), extra=((2007, r"The Green Grid: \ PUE"),
                                                     (2009, r"Barroso and H\"olzle")), part=PART)
        with self.voiceover("Chapter one. The warehouse-scale computer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def building(self):
        head = label(r"The building is the computer", font_size=36).to_edge(UP, buff=0.3)
        rw, rh, gap, n = 0.55, 0.38, 0.06, 8
        rows_y = [1.7, 0.7, -0.5, -1.5]
        x0 = -6.1
        racks = VGroup()
        for y in rows_y:
            for i in range(n):
                racks.add(Rectangle(width=rw, height=rh, stroke_color=GREY_B, stroke_width=1.5, fill_color=GREY_E,
                                    fill_opacity=0.6).move_to([x0 + rw / 2 + i * (rw + gap), y, 0]))
        xs = [x0 + rw / 2 + i * (rw + gap) for i in range(0, n, 2)]

        def arrows(pairs, col):
            return VGroup(*[Arrow([x, a, 0], [x, b, 0], buff=0, stroke_width=2.5, color=col,
                                  max_tip_length_to_length_ratio=0.4) for x in xs for a, b in pairs])
        cold = arrows([(1.2, 1.48), (1.2, 0.92), (-1.0, -0.72), (-1.0, -1.28)], DATA)
        hot = arrows([(0.49, 0.2), (-0.29, 0.0), (1.91, 2.2), (-1.71, -2.0)], NO)
        legend = VGroup(
            VGroup(Arrow(LEFT * 0.2, RIGHT * 0.2, buff=0, color=DATA, stroke_width=2.5),
                   label(r"cold aisle: \ air in at the fronts", font_size=17, color=DATA)).arrange(RIGHT, buff=0.12),
            VGroup(Arrow(LEFT * 0.2, RIGHT * 0.2, buff=0, color=NO, stroke_width=2.5),
                   label(r"hot aisle: \ out at the backs", font_size=17, color=NO)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.4).next_to(racks, DOWN, buff=0.5)
        pick = racks[n + 7]
        rack = Rectangle(width=1.2, height=4.3, stroke_color=HEAD, stroke_width=2).move_to([0.0, 0.0, 0])
        tor = Rectangle(width=1.0, height=0.32, stroke_color=KERN, fill_color=KERN, fill_opacity=0.25,
                        stroke_width=1.5)
        tor_l = label(r"switch", font_size=16, color=WHITE).move_to(tor)
        servers = VGroup(*[Rectangle(width=0.82, height=0.15, stroke_color=DATA, stroke_width=1.2, fill_color=DATA,
                                     fill_opacity=0.2) for _ in range(18)]).arrange(DOWN, buff=0.045)
        inner = VGroup(VGroup(tor, tor_l), servers).arrange(DOWN, buff=0.1).move_to(rack).shift(LEFT * 0.06)
        strip = Rectangle(width=0.07, height=servers.height, stroke_width=0, fill_color=HEAD,
                          fill_opacity=0.8).next_to(servers, RIGHT, buff=0.04)
        rack_g = VGroup(rack, inner, strip)
        cap = label(r"one rack", font_size=18, color=HEAD).next_to(rack, DOWN, buff=0.12)
        link = DashedLine(pick.get_right(), rack.get_left() + UP * 0.6, color=HEAD, stroke_width=1.5)
        notes = VGroup(
            wrapped_label(r"Barroso and H\"olzle \ (2009): \ tens of thousands of servers, \ one owner, \ a few huge "
                          r"services, \ programmed as \textbf{one} machine", 5.2, font_size=20, color=WHITE),
            wrapped_label(r"the unit is the \textbf{rack}: \ a few dozen servers, \ a switch at the top, \ a shared "
                          r"power feed \ (the yellow strip)", 5.2, font_size=20, color=DATA),
            wrapped_label(r"rows face each other in pairs: \ cold air in at the fronts, \ hot air out at the backs "
                          r"into a contained aisle, \ back to the cooling units; \ the two streams must not mix",
                          5.2, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.15, 0.0, 0])
        with self.voiceover(
            "In 2009 Luiz Barroso and Urs Hölzle gave the modern datacentre its name: a warehouse-scale computer. "
            "<bookmark mark='a'/> The building is one computer: tens of thousands of servers, one owner, a few very "
            "large services programmed as a whole. <bookmark mark='b'/> Its unit is the rack, a few dozen servers "
            "under a switch, sharing a power feed, and racks stand in long rows. <bookmark mark='c'/> The rows face "
            "each other in pairs. Cold air is delivered between their fronts; the servers' fans pull it through, "
            "and hot air leaves from the backs into a separate, contained aisle that returns it to the cooling "
            "units."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in racks], lag_ratio=0.03, run_time=2))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(pick.animate.set_stroke(HEAD, width=3), Create(link))
            self.play(FadeIn(rack_g), FadeIn(cap), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(a) for a in cold], lag_ratio=0.05), run_time=1.5)
            self.play(LaggedStart(*[GrowArrow(a) for a in hot], lag_ratio=0.05), FadeIn(legend), FadeIn(notes[2]),
                      run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def power(self):
        head = label(r"Power is the budget", font_size=36).to_edge(UP, buff=0.3)
        names = [(r"grid", GREY_A), (r"transformers", GREY_A), (r"UPS \ (batteries)", HEAD), (r"PDU", KERN),
                 (r"rack", DATA), (r"server supply", DATA)]
        chain = VGroup(*[module_box(t, c, w=1.75, h=0.62, font=18) for t, c in names]).arrange(RIGHT, buff=0.42)
        chain.move_to([0, 1.7, 0])
        links = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.04, stroke_width=2.5,
                               color=GREY_B, max_tip_length_to_length_ratio=0.3) for i in range(len(chain) - 1)])
        heat = VGroup()
        for a in links[1:]:
            w = VMobject(color=NO, stroke_width=2).set_points_smoothly(
                [a.get_center() + UP * 0.25 + RIGHT * 0.06 * (k % 2 * 2 - 1) + UP * 0.12 * k for k in range(4)])
            heat.add(w)
        heat_l = label(r"each conversion loses a little as heat", font_size=17, color=NO).next_to(chain, UP,
                                                                                                  buff=0.42)
        gen = module_box(r"diesel generators", GREY_B, w=2.6, h=0.6, font=18).next_to(chain[2], DOWN, buff=0.75)
        gen_a = DashedLine(gen.get_top(), chain[2].get_bottom(), color=GREY_B, stroke_width=2)
        gen_l = wrapped_label(r"if the grid fails, \ the batteries carry the load for the seconds until the "
                              r"generators start", 4.2, font_size=18, color=GREY_A).next_to(gen, RIGHT, buff=0.3)
        path = Line(chain[0].get_center(), chain[-1].get_center())
        flow = VGroup(*[Dot(radius=0.07, color=HEAD) for _ in range(4)])
        notes = VGroup(
            wrapped_label(r"a building is designed for a fixed power, \ and transformers, \ generators and cooling "
                          r"all scale with it: \ the scarce resource is \textbf{watts}, \ not floor space", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"thousands of servers never peak together \ (Fan, \ Weber and Barroso, \ 2007): \ so "
                          r"operators install more than the peak ratings allow, \ and \textbf{cap} power in the rare "
                          r"moments the total comes too close", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(gen, DOWN, buff=0.7).set_x(0)
        with self.voiceover(
            "Under the floor plan is a power plan. <bookmark mark='a'/> Electricity from the grid is stepped down "
            "by transformers, then passes through an uninterruptible power supply, power distribution units, the "
            "rack, and each server's own supply. Every conversion loses a little as heat. <bookmark mark='b'/> If "
            "the grid fails, batteries carry the load for the seconds until diesel generators start. "
            "<bookmark mark='c'/> A building is designed for a fixed power, and its transformers, generators and "
            "cooling all scale with it, so the scarce resource is watts, not floor space. <bookmark mark='d'/> And "
            "because thousands of servers almost never peak at once, as Xiaobo Fan, Wolf-Dietrich Weber and Luiz "
            "Barroso measured in 2007, operators install more servers than the ratings allow, and cap power when "
            "the total comes too close."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in chain], lag_ratio=0.25), Create(links), run_time=2)
            for d in flow:
                d.move_to(path.get_start())
            self.play(LaggedStart(*[MoveAlongPath(d, path) for d in flow], lag_ratio=0.25, run_time=2.5),
                      Create(heat), FadeIn(heat_l))
            self.remove(*flow)
            vo.wait_until("b")
            self.play(FadeIn(gen), Create(gen_a), FadeIn(gen_l))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def proportional(self):
        head = label(r"Idle is expensive", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 100, 10], [0, 100, 10], x_length=6.0, y_length=4.0, x_label=r"utilization \ (\%)",
                 y_label=r"power \ (\% of peak)", xticks=[0, 25, 50, 75, 100], yticks=[0, 50, 100])
        g.move_to([-3.1, -0.35, 0])
        ax = g.ax
        band = Rectangle(width=ax.c2p(50, 0)[0] - ax.c2p(10, 0)[0], height=ax.c2p(0, 100)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=GREY_B, fill_opacity=0.15)
        band.move_to([(ax.c2p(10, 0)[0] + ax.c2p(50, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, 100)[1]) / 2, 0])
        band_l = wrapped_label(r"where servers spend most of their time", 2.2, font_size=16, color=GREY_A)
        band_l.move_to(band.get_top() + DOWN * (band_l.height / 2 + 0.12))
        idle, u = 0.5, 30
        real = trace(ax, [(0, 100 * idle), (100, 100)], NO, width=3.5)
        ideal = DashedVMobject(trace(ax, [(0, 0), (100, 100)], YES, width=3), num_dashes=30)
        p = 100 * (idle + (1 - idle) * u / 100)
        eff = (u / 100) / (p / 100)
        dot = Dot(ax.c2p(u, p), radius=0.08, color=HEAD)
        guide = DashedLine(ax.c2p(u, 0), ax.c2p(u, p), color=HEAD, stroke_width=1.5)
        dot_l = label(rf"{u}\% busy, \ {p:.0f}\% power", font_size=17, color=HEAD).move_to(ax.c2p(78, 36))
        notes = VGroup(
            wrapped_label(r"Barroso and H\"olzle \ (2007): \ servers spend most of their time 10--50\% busy, \ yet "
                          r"an idle server drew about \textbf{half} its peak power", 5.0, font_size=20, color=WHITE),
            wrapped_label(rf"model: \ a straight line from half power at idle; \ at {u}\% busy the server does "
                          rf"{eff * 100:.0f}\% of the work per watt it manages flat out", 5.0, font_size=20,
                          color=NO),
            wrapped_label(r"their remedy, \ \textbf{energy proportionality}: \ power that falls with load, \ like the "
                          r"dashed line; \ servers have improved since, \ but idle is still far from free", 5.0,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.9, -0.2, 0])
        with self.voiceover(
            "Power also explains a quieter waste. <bookmark mark='a'/> In 2007 Barroso and Hölzle observed that "
            "servers spend most of their time between ten and fifty percent busy, yet an idle server drew about "
            "half its peak power. <bookmark mark='b'/> Draw it as a straight line, from half power idle to full "
            f"power flat out. At thirty percent busy the server draws {p:.0f} percent of its peak, and does less "
            "than half the work per watt it manages flat out. <bookmark mark='c'/> Their remedy was energy "
            "proportionality, power that falls with load, like the dashed line. Servers have improved, but idle is "
            "still far from free."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(band), FadeIn(band_l), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(real))
            self.play(Create(guide), FadeIn(dot), FadeIn(dot_l), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(ideal), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def pue(self):
        head = label(r"Power usage effectiveness", font_size=36).to_edge(UP, buff=0.3)
        formula = label(r"PUE $=\dfrac{\text{power entering the building}}{\text{power reaching the computers}}$",
                        font_size=30).next_to(head, DOWN, buff=0.4)
        cited = [(r"industry average, \ 2007", r"Uptime Institute survey", 2.5),
                 (r"industry average, \ 2023", r"Uptime Institute survey", 1.58),
                 (r"Google's fleet, \ 2023", r"Google environmental report", 1.10)]
        s = 2.4
        rows = VGroup()
        for t, src, v in cited:
            it = Rectangle(width=s, height=0.5, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
            ov = Rectangle(width=(v - 1) * s, height=0.5, stroke_width=0, fill_color=KERN, fill_opacity=0.85)
            ov.next_to(it, RIGHT, buff=0)
            bar = VGroup(it, ov)
            name = VGroup(label(t, font_size=19, color=WHITE), label(src, font_size=16, color=GREY_B)).arrange(
                DOWN, aligned_edge=RIGHT, buff=0.06)
            val = label(rf"{v:.2f}: \ {100 * (1 - 1 / v):.0f}\% never reaches a computer", font_size=18,
                        color=KERN)
            rows.add(VGroup(name, bar, val))
        for k, r in enumerate(rows):
            r[1].move_to([-3.2 + r[1].width / 2, 0.45 - 0.95 * k, 0])
            r[0].next_to(r[1][0], LEFT, buff=0.25)
            r[2].next_to(r[1], RIGHT, buff=0.18)
        legend = VGroup(
            VGroup(Square(0.22, stroke_width=0, fill_color=DATA, fill_opacity=0.85),
                   label(r"reaches the computers", font_size=17, color=DATA)).arrange(RIGHT, buff=0.12),
            VGroup(Square(0.22, stroke_width=0, fill_color=KERN, fill_opacity=0.85),
                   label(r"cooling, \ conversion losses, \ lighting", font_size=17, color=KERN)).arrange(RIGHT,
                                                                                                    buff=0.12),
        ).arrange(RIGHT, buff=0.6).next_to(formula, DOWN, buff=0.35)
        foot = wrapped_label(r"defined by The Green Grid \ (2007); \ 1 would be perfect; \ PUE measures the building, "
                             r"\ not the work: \ an idle server at PUE 1.1 is still idle", 12.4, font_size=20,
                             color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The building has an overhead too. <bookmark mark='a'/> Power usage effectiveness, defined by The "
            "Green Grid in 2007, is the power entering the building divided by the power reaching the computing "
            "equipment; one would be perfect. <bookmark mark='b'/> The Uptime Institute's surveys put the industry "
            "average at about two and a half in 2007, and about one point six in 2023. <bookmark mark='c'/> Google "
            "reported one point one for its fleet in 2023. <bookmark mark='d'/> At two and a half, sixty percent of "
            "the electricity never reached a computer; at one point one, nine percent. But the ratio measures the "
            "building, not the work: an idle server in an efficient building is still idle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(formula), FadeIn(legend))
            vo.wait_until("b")
            for r in rows[:2]:
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2][0]), GrowFromEdge(rows[2][1], LEFT), FadeIn(rows[2][2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def failure(self):
        head = label(r"Failure is a rate", font_size=36).to_edge(UP, buff=0.3)
        n_racks, per, mtbf_years, repair_days, days = 50, 40, 3, 3, 30
        sq, px, py = 0.075, 0.104, 0.092
        grid = VGroup()
        for r in range(n_racks):
            for s_ in range(per):
                grid.add(Square(sq, stroke_width=0, fill_color=DATA, fill_opacity=0.55).move_to(
                    [r * px + (r // 10) * 0.06, -s_ * py, 0]))
        grid.move_to([-3.75, -0.55, 0])
        machines = n_racks * per
        rate = machines / (mtbf_years * 365.25)
        rng = random.Random(45)
        events = []                       # per day: (failed indices, repaired indices)
        down = {}
        total = 0
        for d in range(1, days + 1):
            back = [i for i, t in down.items() if d - t >= repair_days]
            for i in back:
                del down[i]
            t, k = rng.expovariate(rate), 0
            while t < 1.0:
                k += 1
                t += rng.expovariate(rate)
            new = rng.sample([i for i in range(machines) if i not in down], k)
            for i in new:
                down[i] = d
            total += k
            events.append((new, back))
        cap = label(rf"{machines:,} servers in {n_racks} racks \ (illustrative)".replace(",", "{,}"), font_size=18,
                    color=GREY_A).next_to(grid, UP, buff=0.2).align_to(grid, LEFT)
        day = label(r"day 0", font_size=20, color=HEAD).next_to(grid, UP, buff=0.2).align_to(grid, RIGHT)
        rack_k = 17
        rack_sq = VGroup(*grid[rack_k * per:(rack_k + 1) * per])
        ring = SurroundingRectangle(rack_sq, color=NO, buff=0.05, stroke_width=2.5)
        notes = VGroup(
            wrapped_label(rf"each fails once in {mtbf_years} years on average \ (an assumption): \ "
                          rf"$2000 / {mtbf_years * 365.25:.0f}$ days $\approx$ {rate:.1f} failures a day; \ here "
                          rf"{total} in a month, \ each down {repair_days} days", 5.6, font_size=19, color=WHITE),
            wrapped_label(r"failures come in groups: \ a rack's switch or power feed takes all forty at once; \ so "
                          r"does a power unit for a row, \ a cooling zone, \ a building", 5.6, font_size=19,
                          color=NO),
            wrapped_label(r"\textbf{failure domains} nest: \ server, \ rack, \ power domain, \ building, \ zone, \ "
                          r"region; \ copies must sit in different ones", 5.6, font_size=19, color=KERN),
            wrapped_label(r"Part 34: \ disks replaced at 2--4\% a year; \ Part 39: \ a cluster's year \ (Dean, \ "
                          r"2009); \ so recovery is designed in \ (chapters 8 and 11, \ Part 50)", 5.6, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.75, -0.25, 0])
        with self.voiceover(
            "At this scale, failure stops being an event and becomes a rate. <bookmark mark='a'/> Here are two "
            "thousand servers in fifty racks, each failing on average once in three years, an assumption for the "
            "picture: nearly two failures a day. Watch a month go by; the software around each red server has "
            "already moved on. <bookmark mark='b'/> Failures also come in groups. When a rack's switch or power "
            "feed fails, all forty servers vanish at once, and likewise for a power unit, a cooling zone, a "
            "building. <bookmark mark='c'/> These nested failure domains decide where copies may live. "
            "<bookmark mark='d'/> Part 34 met disks replaced at two to four percent a year, and Part 39 a "
            "cluster's first year. So recovery is designed in: chapter eight spreads storage across failure "
            "domains, and chapter eleven spreads services across zones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(cap), FadeIn(day))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for d, (new, back) in enumerate(events, 1):
                anims = [grid[i].animate.set_fill(NO, opacity=1.0) for i in new]
                anims += [grid[i].animate.set_fill(DATA, opacity=0.55) for i in back]
                anims.append(Transform(day, label(rf"day {d}", font_size=20, color=HEAD).move_to(day, RIGHT)))
                self.play(*anims, run_time=0.22)
            vo.wait_until("b")
            self.play(rack_sq.animate.set_fill(NO, opacity=1.0), Create(ring), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, YES)
