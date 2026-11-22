from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.compute import load as load31
from videos.cs.cs48.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, bar_chart, load, module_box,
                                   tag_box)


class Async(WatchScene):
    def construct(self):
        self.card()
        self.absorb()
        self.explode()
        self.pools()

    def card(self):
        self.chapter(6, r"Queues and asynchrony", r"What does a queue buy, \ and what does it cost?", lit=(1909, 1961), extra=((1909, r"Erlang: \ telephone traffic"),
                                                     (1961, r"Little's law")), part=PART, said="Chapter six. Queues and asynchrony.")

    def absorb(self):
        head = label(r"A queue absorbs a burst", font_size=36).to_edge(UP, buff=0.3)
        y = 1.0
        client = module_box(r"client", DATA, w=1.3, h=0.6, font=18).move_to([-6.0, y, 0])
        web = module_box(r"web tier", HEAD, w=1.5, h=0.6, font=18).move_to([-4.1, y, 0])
        n_slots, sw = 10, 0.38
        slots = VGroup(*[Square(side_length=sw, stroke_color=GREY_C, stroke_width=1.5) for _ in range(n_slots)])
        slots.arrange(LEFT, buff=0.0).move_to([-0.7, y, 0])      # slot 0 is the head, on the right
        q_l = label(r"queue", font_size=18, color=LAM).next_to(slots, UP, buff=0.15)
        workers = VGroup(*[module_box(rf"worker {i + 1}", KERN, w=1.5, h=0.5, font=17) for i in range(3)]).arrange(
            DOWN, buff=0.25).move_to([2.6, y, 0])
        a1 = Arrow(client.get_right(), web.get_left(), buff=0.08, stroke_width=2, color=GREY_B)
        a2 = Arrow(web.get_right(), slots.get_left(), buff=0.08, stroke_width=2, color=GREY_B)
        a3 = Arrow(slots.get_right(), workers.get_left(), buff=0.08, stroke_width=2, color=GREY_B)
        ack = VGroup(CurvedArrow(web.get_top() + LEFT * 0.3, client.get_top() + RIGHT * 0.2, angle=0.9,
                                 color=YES, stroke_width=2))
        ack.add(label(r"202 Accepted", font_size=16, color=YES).next_to(ack[0], UP, buff=0.05))
        jobs = [Dot(web.get_center(), radius=0.1, color=LAM) for _ in range(8)]
        notes = VGroup(
            wrapped_label(r"the web tier records the work and answers at once \ (Part 43's \texttt{202} and its "
                          r"outbox); \ workers do it at their own pace", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"a burst becomes a queue that drains: \ a rate problem turned into a delay problem", 12.4,
                          font_size=20, color=LAM),
            wrapped_label(r"it works only if, \ on average, \ the workers keep up: \ a queue absorbs bursts, \ not a "
                          r"shortfall in capacity", 12.4, font_size=20, color=NO),
            wrapped_label(r"in return: \ the caller never waits for slow work, \ failures are retried from the "
                          r"queue, \ and producers and consumers scale apart \ (Kafka, \ SQS, \ RabbitMQ)", 12.4,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Some work need not happen while the caller waits: resizing an image, or sending an "
            "email. <bookmark mark='a'/> The web tier records the request, puts a job on a "
            "queue, and answers at once with Part 43's two hundred and two, accepted. Workers take jobs at their "
            "own pace. <bookmark mark='b'/> A burst now fills the queue, which drains. The "
            "queue has turned a problem of rate into a problem of delay. <bookmark mark='c'/> But only if, on "
            "average, the workers keep up: a queue absorbs bursts, never a shortfall. <bookmark mark='d'/> In "
            "return, the caller never waits for slow work, a failed job can be retried from the queue, and the "
            "producers and consumers can be scaled separately."
        ) as vo:
            self.play(FadeIn(head), FadeIn(client), FadeIn(web), FadeIn(slots), FadeIn(q_l), FadeIn(workers),
                      GrowArrow(a1), GrowArrow(a2), GrowArrow(a3))
            vo.wait_until("a")
            self.play(Create(ack[0]), FadeIn(ack[1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.add(*jobs)
            self.play(LaggedStart(*[j.animate.move_to(slots[k]) for k, j in enumerate(jobs)], lag_ratio=0.15),
                      FadeIn(notes[1]), run_time=2)
            queue = list(jobs)
            while queue:                                   # three workers take the three jobs at the head
                take, queue = queue[:3], queue[3:]
                self.play(*[j.animate.move_to(workers[i]).set_opacity(0) for i, j in enumerate(take)],
                          *[j.animate.move_to(slots[k]) for k, j in enumerate(queue)], run_time=0.9)
                self.remove(*take)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def explode(self):
        self.ask(r"A queue's load rises from $80\%$ to $95\%$. \\ The delay...", [r"rises a little",
                 r"roughly quadruples"], 1,
                 say="A worker queue runs at eighty percent load, then ninety-five. What happens to the delay?",
                 reveal="It roughly quadruples: one over one minus rho.")
        q = load31("queue")
        head = label(r"Why latency explodes near full load", font_size=36).to_edge(UP, buff=0.3)
        ymax = 50
        g = axes([0, 1, 0.25], [0, ymax, 10], x_length=6.2, y_length=4.2, x_label=r"utilization $\rho$",
                 y_label=r"time in system, \ in service times", xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[0, 10, 20, 30, 40, 50], font=16)
        g.to_edge(LEFT, buff=0.75).shift(DOWN * 0.25)
        ax = g.ax
        rows = q["mm1"]
        curve = VMobject(color=HEAD, stroke_width=3).set_points_as_corners(
            [ax.c2p(r, 1 / (1 - r)) for r in [i / 200 for i in range(0, 200)] if 1 / (1 - r) <= ymax])
        sims = VGroup(*[Dot(ax.c2p(r["rho"], r["sim"]), radius=0.06, color=DATA) for r in rows])
        tails = VGroup(*[Dot(ax.c2p(r["rho"], r["p99"]), radius=0.06, color=NO) for r in rows if r["p99"] <= ymax])
        key = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=HEAD, stroke_width=3),
                            label(r"$1/(1-\rho)$", font_size=17, color=HEAD)).arrange(RIGHT, buff=0.1),
                     VGroup(Dot(radius=0.06, color=DATA), label(r"simulated mean", font_size=17,
                                                                color=DATA)).arrange(RIGHT, buff=0.1),
                     VGroup(Dot(radius=0.06, color=NO), label(r"simulated p99", font_size=17,
                                                              color=NO)).arrange(RIGHT, buff=0.1)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.c2p(0.3, 38))
        by = {f"{r['rho']:.2f}": r for r in rows}
        pk = {p["name"]: p for p in q["pk"]}
        notes = VGroup(
            wrapped_label(rf"M/M/1 \ (Part 31): \ mean {by['0.50']['sim']:.0f} service times at half load, \ "
                          rf"{by['0.90']['sim']:.0f} at 0.9, \ {by['0.95']['sim']:.0f} at 0.95", 5.0, font_size=19,
                          color=WHITE),
            wrapped_label(rf"the tail is worse: \ p99 is {by['0.90']['p99']:.0f} service times at 0.9", 5.0,
                          font_size=19, color=NO),
            wrapped_label(rf"variability costs as much: \ at 0.8, \ {pk['deterministic']['sim']:.0f}, \ "
                          rf"{pk['exponential']['sim']:.0f} or {pk['hyperexponential']['sim']:.0f} service times as "
                          r"job sizes vary more \ (Pollaczek--Khinchine)", 5.0, font_size=19, color=LAM),
            wrapped_label(r"so a design leaves headroom, \ and measures how long jobs wait, \ not just how busy the "
                          r"workers are", 5.0, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.5).shift(UP * 0.2)
        foot = note(r"simulated in Part 31: \ a million jobs at each load", font_size=16).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "How long is the delay? Part 31 answered that. <bookmark mark='a'/> With random arrivals and random job "
            "sizes, the mean time in the system is one over one minus the utilization, in "
            "units of the service time: two at half load, ten at ninety percent, about twenty-one at ninety-five. "
            "<bookmark mark='b'/> The slowest one percent are worse: forty-eight service times at ninety percent. "
            "<bookmark mark='c'/> And variability costs as much as load. At eighty percent, jobs of identical size "
            "wait three service times on average; exponential sizes, five; and sizes that vary ten times as much, "
            "twenty-two. <bookmark mark='d'/> So a design leaves headroom, and watches how long jobs wait in the "
            "queue, not merely how busy the workers are."
        ) as vo:
            self.play(FadeIn(head), Create(g), FadeIn(foot))
            vo.wait_until("a")
            self.play(Create(curve), LaggedStart(*[FadeIn(s) for s in sims], lag_ratio=0.1), FadeIn(key[:2]),
                      FadeIn(notes[0]), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in tails], lag_ratio=0.1), FadeIn(key[2]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()



    def pools(self):
        n = load("napkin")
        head = label(r"Sizing a worker pool", font_size=36).to_edge(UP, buff=0.3)
        lam, S, target = n["write_qps"], 0.5, 0.7          # S and the target are illustrative
        busy = lam * S
        size = busy / target
        nb, ns = round(busy), round(size)
        cols = 15
        cells = VGroup(*[Square(side_length=0.26, stroke_width=1, stroke_color=GREY_D,
                                fill_color=KERN if i < nb else BG, fill_opacity=0.85 if i < nb else 1)
                         for i in range(ns)]).arrange_in_grid(cols=cols, buff=0.06)
        cells.move_to([-3.4, -0.5, 0])
        eqs = VGroup(
            MathTex(r"L = \lambda S", font_size=34, color=WHITE),
            MathTex(rf"{lam:.0f}\ \text{{jobs/s}} \times {S:g}\ \text{{s}} \approx {nb}\ \text{{busy}}", font_size=28,
                    color=KERN),
            MathTex(rf"{nb} / {target:g} \approx {ns}\ \text{{workers}}", font_size=28, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(cells, UP, buff=0.35)
        lines = VGroup(
            wrapped_label(r"Little's law \ (Part 31): \ the jobs in service equal the arrival rate times the time "
                          r"each takes; \ the napkin's writes, \ each starting a half-second job", 5.6, font_size=19,
                          color=WHITE),
            wrapped_label(r"then headroom: \ one shared queue in front of many workers can run hotter than many "
                          r"small ones \ (Erlang's pooling)", 5.6, font_size=19, color=YES),
            wrapped_label(r"scale on the age of the oldest job, \ not on processor load; \ and bound the queue, \ "
                          r"refusing work early \ (Part 43's backpressure)", 5.6, font_size=19, color=HEAD),
            wrapped_label(r"Part 49 sizes whole systems this way; \ Part 50 sets the waits they promise", 5.6,
                          font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.0, 0])
        foot = note(r"half-second jobs and the 70\% target illustrative; \ the write rate from the napkin",
                    font_size=16).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "How many workers? Little's law says the number of jobs in service is the arrival rate "
            "times the time each one takes. <bookmark mark='a'/> Take the napkin's two hundred and ten writes a "
            "second, and suppose each starts a job of half a second. On average, a hundred and five workers are "
            "busy. <bookmark mark='b'/> Add headroom, running at seventy percent: a pool of a hundred and fifty. "
            "One shared queue feeding many workers can run hotter than many small queues: Erlang's pooling. <bookmark "
            "mark='c'/> Scale the pool on the age of the oldest waiting job, not "
            "on processor load, and bound the queue so that overload is refused early. <bookmark mark='d'/> Part 49 "
            "will size whole systems this way, and Part 50 will decide what waits they may promise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eqs[0]), FadeIn(lines[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(eqs[1]), LaggedStart(*[FadeIn(c) for c in cells[:nb]], lag_ratio=0.01), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(eqs[2]), LaggedStart(*[FadeIn(c) for c in cells[nb:]], lag_ratio=0.02),
                      FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (YES, axes)
