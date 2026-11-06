from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


class Bill(VoiceoverScene):
    def construct(self):
        self.card()
        self.breakeven()
        self.spot()
        self.ledger()
        self.carbon()

    def card(self):
        card = chapter_card(12, r"Cost, \ carbon, \ and the Job's bill", r"What does a design cost to run?",
                            lit=(2009, 2014), extra=((2009, r"EC2 spot instances"),
                                                     (2014, r"AWS Lambda announced")), part=PART)
        with self.voiceover("Chapter twelve. Cost, carbon, and the Job's bill."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def breakeven(self):
        s = load("serverless")
        rows = s["rows"]
        head = label(r"Functions or servers?", font_size=36).to_edge(UP, buff=0.3)
        x0, y0, xw, yh = -6.0, -2.3, 7.4, 4.3
        lx = [math.log10(r["rps"]) for r in rows]
        ly_max = math.log10(max(r["lambda"] for r in rows))
        ly_min = math.log10(min(r["lambda"] for r in rows))

        def pt(x, y):
            return [x0 + (math.log10(x) - lx[0]) / (lx[-1] - lx[0]) * xw,
                    y0 + (math.log10(y) - ly_min) / (ly_max - ly_min) * yh, 0]
        ax = VGroup(Line([x0, y0, 0], [x0 + xw, y0, 0], color=GREY_C), Line([x0, y0, 0], [x0, y0 + yh, 0],
                                                                              color=GREY_C))
        ticks = VGroup()
        for r in rows:
            if r["rps"] in (0.1, 1, 10, 100, 1000):
                ticks.add(label(f"{r['rps']:g}", font_size=16, color=GREY_B).move_to([pt(r["rps"], 1)[0], y0 - 0.25,
                                                                                    0]))
        for v in (1, 10, 100, 1000):
            if ly_min <= math.log10(v) <= ly_max:
                ticks.add(label(rf"\${v:,}", font_size=16, color=GREY_B).move_to([x0 - 0.45, pt(1, v)[1], 0]))
        lam = VMobject(color=HEAD, stroke_width=3).set_points_as_corners([pt(r["rps"], r["lambda"]) for r in rows])
        srv = VMobject(color=DATA, stroke_width=3).set_points_as_corners([pt(r["rps"], r["servers"]) for r in rows])
        be = s["breakeven_rps"]
        bx = pt(be, 1)[0]
        bline = DashedLine([bx, y0, 0], [bx, y0 + yh, 0], color=YES)
        xl = label(r"requests per second, \ steady, \ all month", font_size=17, color=GREY_B).next_to(ax[0], DOWN,
                                                                                               buff=0.5)
        yl = label(r"dollars per month", font_size=17, color=GREY_B).next_to(ax[1], UP, buff=0.1)
        side = VGroup(
            wrapped_label(rf"a function: \ {s['ms']} ms at {s['mb']} MB, \ \${1e6 * s['per_request']:.2f} per "
                          r"million requests", 4.6, font_size=19, color=HEAD),
            wrapped_label(r"a server: \ one m5.large all month, \ handling up to 200 requests a second", 4.6,
                          font_size=19, color=DATA),
            wrapped_label(rf"break-even near {be:.0f} requests a second: \ below it, \ pay per request; \ above it, "
                          r"\ rent the machine", 4.6, font_size=19, color=YES),
            wrapped_label(rf"{s['prices']['date']}", 4.6, font_size=16, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "When is paying per request cheaper than renting a machine? <bookmark mark='a'/> Take a function that "
            f"runs for {s['ms']} milliseconds with half a gigabyte of memory. At Amazon's list prices, a million "
            f"calls cost about {1e6 * s['per_request']:.2f} dollars, so its monthly bill grows in proportion to the "
            "traffic. <bookmark mark='b'/> A server costs the same every month whether it is busy or idle, here one "
            "small instance able to handle two hundred requests a second. <bookmark mark='c'/> The lines cross near "
            f"{be:.0f} requests a second of steady traffic. Below that, and for anything bursty or rare, functions "
            "win; above it, a machine kept busy is cheaper, often by a wide margin. The answer depends on "
            "utilization, which is chapter five's bin packing again."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(lam), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(srv), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(bline), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def spot(self):
        sp = load("spot")
        head = label(r"Cheap machines that can be taken away", font_size=36).to_edge(UP, buff=0.3)
        rows = []
        for r in sp["rows"]:
            c = r["checkpoint_every"]
            rows.append([r"none" if c is None else rf"every {60 * c:.0f} min", f"{r['hours']:.1f}",
                         rf"\${r['cost']:.2f}"])
        rows.append([r"on demand, \ no interruptions", f"{sp['job_hours']:.1f}", rf"\${sp['on_demand_cost']:.2f}"])
        tab = grid_table([r"checkpoints", r"hours to finish", r"cost"], rows, widths=[3.4, 2.4, 1.8], row_h=0.45,
                         font_size=19, mono_cols=())
        tab.to_edge(LEFT, buff=0.7).shift(UP * 0.6)
        best = min(range(len(sp["rows"])), key=lambda i: sp["rows"][i]["cost"])
        for c in tab.cells[best + 1]:
            c.set_color(YES)
        for c in tab.cells[1]:
            c.set_color(NO)
        # a timeline of interruptions losing work since the last checkpoint
        tl = VGroup()
        x0, y = 1.6, 1.3
        tl.add(Line([x0, y, 0], [x0 + 5.0, y, 0], color=GREY_C))
        for k in range(1, 6):
            tl.add(Line([x0 + k * 0.9, y - 0.12, 0], [x0 + k * 0.9, y + 0.12, 0], color=YES, stroke_width=3))
        boom = Cross(scale_factor=0.13, stroke_color=NO).move_to([x0 + 3.3, y, 0])
        lost = Rectangle(width=0.6, height=0.2, stroke_width=0, fill_color=NO, fill_opacity=0.5).move_to(
            [x0 + 3.0, y + 0.3, 0])
        tl_l = VGroup(label(r"checkpoints", font_size=16, color=YES).next_to(tl, UP, buff=0.45),
                      label(r"interrupted: \ redo since the last one", font_size=16, color=NO).next_to(tl, DOWN,
                                                                                                   buff=0.3))
        lines = VGroup(
            wrapped_label(rf"a {sp['job_hours']:.0f}-hour job, \ an interruption every {1 / sp['interrupt_per_hour']:.0f} "
                          r"hours on average, \ checkpoints costing 1.2 minutes each \ (a model)", 5.6, font_size=19,
                          color=WHITE),
            wrapped_label(rf"Young's rule \ (1974): \ checkpoint every $\sqrt{{2C/\lambda}}$ $\approx$ "
                          rf"{60 * sp['young_interval']:.0f} minutes", 5.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tl_l, DOWN, buff=0.4).align_to(tl, LEFT)
        with self.voiceover(
            "Providers sell their spare capacity cheaply, as spot instances, on the condition that they can take "
            "it back at short notice. <bookmark mark='a'/> We modelled a ten-hour batch job on spot machines "
            "priced at a typical discount, interrupted on average once every ten hours. <bookmark mark='b'/> Without "
            f"checkpoints, every interruption sends the job back to the start: it takes {sp['rows'][0]['hours']:.0f} "
            "hours on average, and costs more than half of the on-demand price anyway. <bookmark mark='c'/> With a "
            "checkpoint every half hour or so, it finishes in under eleven hours for just over a third of the on-demand "
            "cost. <bookmark mark='d'/> The best interval balances the cost of checkpointing against the work lost "
            "on interruption; John Young's rule of 1974, the square root of twice the checkpoint cost over the "
            f"failure rate, gives {60 * sp['young_interval']:.0f} minutes, close to what the simulation finds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(Create(tl), FadeIn(tl_l[0]))
            self.play(FadeIn(boom), FadeIn(lost), FadeIn(tl_l[1]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[1])), FadeIn(VGroup(*tab.cells[-1])))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[2:-1]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def ledger(self):
        j = load("job")
        led = j["ledger"]
        row = led[-1]
        b = j["bill"]
        head = label(r"Ledger row 16", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.28,
                           label_width=4.8).scale(0.84).move_to(UP * 0.75)
        notes = VGroup(
            label(rf"the Job on sixteen functions: \ about {row['seconds']:.2f} s of wall-clock time, \ about "
                  rf"\${b['lambda']:.5f}", font_size=19, color=HEAD),
            label(r"for the first time the ledger has a second column: \ dollars, \ as well as seconds", font_size=19,
                  color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        for n in notes:
            if n.width > 12.8:
                n.width = 12.8
        with self.voiceover(
            "The ledger gets row sixteen. <bookmark mark='a'/> The Job split across sixteen functions in the cloud: "
            "less than a tenth of a second of wall-clock time, if the text is already waiting in storage and the "
            "functions are warm, and a bill of about three thousandths of a cent. <bookmark mark='b'/> For the first "
            "time the ledger needs a second column. A design is now judged by what it costs to run, as well as how "
            "fast it runs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(tab.rows[-1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def carbon(self):
        head = label(r"Energy and carbon", font_size=36).to_edge(UP, buff=0.3)
        # an illustrative day of grid carbon intensity, with a flexible job moved to the cleanest hours
        x0, y0, w, h = -6.0, -0.9, 7.2, 2.8
        hours = list(range(25))
        inten = [420 - 160 * math.exp(-((t - 13) / 3.2) ** 2) + 30 * math.cos(t / 24 * 2 * math.pi) for t in hours]
        mx = max(inten)
        pts = [[x0 + t / 24 * w, y0 + v / mx * h, 0] for t, v in zip(hours, inten)]
        curve = VMobject(color=GREY_A, stroke_width=3).set_points_as_corners(pts)
        ax = Line([x0, y0, 0], [x0 + w, y0, 0], color=GREY_C)
        tl = VGroup(*[label(f"{t:02d}:00", font_size=15, color=GREY_B).move_to([x0 + t / 24 * w, y0 - 0.25, 0])
                      for t in (0, 6, 12, 18, 24)])
        job_a = Rectangle(width=4 / 24 * w, height=0.35, stroke_width=0, fill_color=NO, fill_opacity=0.6).move_to(
            [x0 + 20 / 24 * w, y0 + 0.25, 0])
        job_b = job_a.copy().set_fill(YES, 0.6).move_to([x0 + 13 / 24 * w, y0 + 0.25, 0])
        il = label(r"grid carbon intensity over a day \ (illustrative)", font_size=17, color=GREY_B).next_to(
            curve, UP, buff=0.15)
        side = VGroup(
            wrapped_label(r"datacentres used roughly 1--1.5\% of the world's electricity in 2022 \ (International "
                          r"Energy Agency), \ and AI is raising it", 4.8, font_size=19, color=WHITE),
            wrapped_label(r"PUE, \ total power over computing power: \ the best fleets report about 1.1", 4.8,
                          font_size=19, color=DATA),
            wrapped_label(r"carbon-aware scheduling moves flexible work to the hours and regions where the grid is "
                          r"cleanest", 4.8, font_size=19, color=YES),
            wrapped_label(r"the cheapest energy is the computation not done: \ every faster row of the ledger is "
                          r"also a smaller footprint", 4.8, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Behind every bill is energy. <bookmark mark='a'/> The International Energy Agency estimated that "
            "datacentres used roughly one to one and a half percent of the world's electricity in 2022, and the "
            "growth of AI is pushing that up. <bookmark mark='b'/> Efficiency starts with the building: power usage "
            "effectiveness is total power divided by the power that reaches the computers, and the best fleets "
            "report about one point one. <bookmark mark='c'/> The grid's carbon intensity changes through the day, "
            "so flexible work, a nightly batch job, can be moved to the hours or the regions where the grid is "
            "cleanest. <bookmark mark='d'/> And the cheapest energy is the computation you never run: every row of "
            "the ledger that made the Job faster also made it smaller."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(tl), Create(curve), FadeIn(il))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(job_a), FadeIn(side[2]))
            self.play(Transform(job_a, job_b))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM)
