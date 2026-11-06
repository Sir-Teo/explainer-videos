from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.compute import load as load31
from videos.cs.cs48.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, bar_chart, load, module_box,
                                   tag_box)


class Async(VoiceoverScene):
    def construct(self):
        self.card()
        self.absorb()
        self.explode()
        self.priorities()
        self.delayed()
        self.pools()

    def card(self):
        card = chapter_card(6, r"Queues and asynchrony", r"What does a queue buy, \ and what does it cost?",
                            lit=(1909, 1961), extra=((1909, r"Erlang: \ telephone traffic"),
                                                     (1961, r"Little's law")), part=PART)
        with self.voiceover("Chapter six. Queues and asynchrony."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

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

    def priorities(self):
        q = load31("queue")
        head = label(r"Priorities", font_size=36).to_edge(UP, buff=0.3)
        hi = VGroup(*[Square(side_length=0.36, stroke_color=HEAD, stroke_width=1.5, fill_color=HEAD,
                             fill_opacity=0.5 if k < 2 else 0) for k in range(6)]).arrange(LEFT, buff=0)
        lo = VGroup(*[Square(side_length=0.36, stroke_color=DATA, stroke_width=1.5, fill_color=DATA,
                             fill_opacity=0.5 if k < 6 else 0) for k in range(6)]).arrange(LEFT, buff=0)
        qs = VGroup(hi, lo).arrange(DOWN, buff=0.6).move_to([-3.6, 1.2, 0])
        hl = label(r"interactive", font_size=18, color=HEAD).next_to(hi, LEFT, buff=0.2)
        ll = label(r"batch", font_size=18, color=DATA).next_to(lo, LEFT, buff=0.2)
        pool = module_box(r"workers", KERN, w=1.5, h=1.4, font=18).next_to(qs, RIGHT, buff=1.0)
        ah = Arrow(hi.get_right(), pool.get_left() + UP * 0.3, buff=0.08, stroke_width=3, color=HEAD)
        al = Arrow(lo.get_right(), pool.get_left() + DOWN * 0.3, buff=0.08, stroke_width=1.5, color=DATA)
        wl = label(r"weights, \ e.g.\ 4 : 1", font_size=16, color=GREY_B).next_to(pool, DOWN, buff=0.15)
        d = next(r for r in q["disc"] if r["name"] == "heavy-tailed")
        bars = bar_chart([d["fcfs"], d["ps"], d["srpt"]], [r"FCFS", r"sharing", r"SRPT"], [NO, LAM, YES],
                         height=2.6, bar_w=0.8, gap=0.6, fmt_=lambda v: f"{v:.1f}", font_size=18)
        bars.move_to([3.9, 1.0, 0])
        bt = label(r"heavy-tailed jobs at load 0.8: \ mean time", font_size=17, color=GREY_A).next_to(bars, UP,
                                                                                                   buff=0.2)
        notes = VGroup(
            wrapped_label(r"separate queues by urgency, \ so a flood of batch work cannot delay a user who is "
                          r"waiting", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"strict priority can starve the low queue: \ serve by weights, \ or age a job's priority "
                          r"while it waits", 12.4, font_size=20, color=HEAD),
            wrapped_label(rf"order is worth as much as speed: \ shortest jobs first cut the mean from "
                          rf"{d['fcfs']:.1f} to {d['srpt']:.1f} service times \ (Part 31's simulation)", 12.4,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(bars, DOWN, buff=0.7)
        notes.to_edge(LEFT, buff=0.5)
        with self.voiceover(
            "Not all jobs are equally urgent. <bookmark mark='a'/> Keep separate queues: an interactive one, for "
            "work someone is waiting on, and a batch one, so that a flood of batch "
            "work cannot delay a waiting user. <bookmark mark='b'/> Strict priority, though, can starve the low "
            "queue for ever. So workers serve the queues by weight, four from one for each from the other, say, or "
            "a job's priority rises the longer it waits. <bookmark mark='c'/> The order matters as much as the "
            "speed. Part 31 simulated heavy-tailed jobs at eighty percent load: first come, first served took "
            "twenty-six service times on average; serving the shortest remaining job first, two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(qs), FadeIn(hl), FadeIn(ll), FadeIn(pool), GrowArrow(ah), GrowArrow(al))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(wl), FadeIn(notes[1]), Indicate(lo, color=NO))
            vo.wait_until("c")
            self.play(FadeIn(bt), FadeIn(bars), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def delayed(self):
        head = label(r"Later, \ and again", font_size=36).to_edge(UP, buff=0.3)
        x0, x1, y = -6.0, 6.0, 1.9
        line = Arrow([x0, y, 0], [x1 + 0.4, y, 0], buff=0, stroke_width=2, color=GREY_C,
                     max_tip_length_to_length_ratio=0.02)
        tl = label(r"a sorted set, \ scored by due time", font_size=17, color=GREY_B).next_to(line, UP,
                                                                                            buff=1.0).align_to(
            line, LEFT)
        due = [(-4.6, "reminder"), (-2.9, "retry 2"), (-0.8, "digest"), (1.6, "retry 3"), (4.2, "expire")]
        tags = VGroup(*[tag_box(t, color=LAM, size=16).move_to([x, y + 0.45, 0]) for x, t in due])
        ticks = VGroup(*[Line([x, y - 0.1, 0], [x, y + 0.1, 0], color=LAM, stroke_width=2) for x, _ in due])
        now = VGroup(Line([x0 + 0.2, y - 0.35, 0], [x0 + 0.2, y + 0.2, 0], color=HEAD, stroke_width=4),
                     label(r"now", font_size=17, color=HEAD).move_to([x0 + 0.2, y - 0.55, 0]))
        ready = VGroup(*[Rectangle(width=1.3, height=0.5, stroke_color=GREY_C, stroke_width=1.5)
                         for _ in range(5)]).arrange(RIGHT, buff=0).move_to([0.0, 0.25, 0])
        rl = label(r"ready queue", font_size=17, color=GREY_A).next_to(ready, LEFT, buff=0.2)
        # retries: delays doubling, with jitter, then the dead-letter queue
        base = [1, 2, 4, 8]
        jit = [0.7, 1.6, 4.5, 6.9]                         # illustrative jittered draws
        bars = VGroup()
        for k, (b, j) in enumerate(zip(base, jit)):
            full = Rectangle(width=b * 0.42, height=0.26, stroke_color=GREY_C, stroke_width=1.2)
            fill = Rectangle(width=j * 0.42, height=0.26, stroke_width=0, fill_color=KERN, fill_opacity=0.8)
            row = VGroup(label(rf"try {k + 2}", font_size=16, color=GREY_A), VGroup(full, fill))
            fill.align_to(full, LEFT)
            row.arrange(RIGHT, buff=0.2)
            bars.add(row)
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-3.9, -1.25, 0])
        for row in bars:
            row[1].align_to(bars[0][1], LEFT)
        dlq = module_box(r"dead letters", NO, w=1.9, h=0.5, font=17).next_to(bars, RIGHT, buff=0.4).align_to(
            bars, DOWN)
        lines = VGroup(
            wrapped_label(r"a delayed job is stored by its due time; \ a poller moves whatever is due onto the ready "
                          r"queue \ (Redis sorted sets; \ SQS delay; \ a timing wheel)", 5.6, font_size=19,
                          color=WHITE),
            wrapped_label(r"a failed job waits $2^k$ times a base delay, \ drawn at random below that \ "
                          r"(``full jitter''), \ so retries do not arrive together", 5.6, font_size=19, color=KERN),
            wrapped_label(r"after the last try it goes to a dead-letter queue for a person; \ and since it may run "
                          r"twice, \ the job must be idempotent \ (Part 43)", 5.6, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, -1.35, 0])
        foot = note(r"illustrative schedule and delays", font_size=16).to_edge(DOWN, buff=0.2).set_x(-3.9)
        with self.voiceover(
            "Queues also carry work for later. <bookmark mark='a'/> A delayed job, a reminder tomorrow or a digest "
            "at six, is stored by its due time, in a sorted set or a timing wheel, and a poller moves whatever has "
            "come due onto the ready queue. <bookmark mark='b'/> Retries are delayed jobs too. After each failure a "
            "job waits twice as long as before, one second, two, four, eight, and the actual delay is drawn at "
            "random below that, so that jobs which failed together do not retry together. "
            "<bookmark mark='c'/> After the last attempt, the job goes to a dead-letter queue for a person to look "
            "at. And because a job may run twice, every job must be "
            "idempotent, as Part 43 insisted."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(line), FadeIn(tl), FadeIn(ticks), FadeIn(tags), FadeIn(now),
                      FadeIn(ready), FadeIn(rl), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            slot = 0
            for (x, _), t in zip(due[:3], tags[:3]):
                self.play(now.animate.set_x(x + 0.05), run_time=0.8, rate_func=linear)
                self.play(t.animate.scale(0.9).move_to(ready[slot]), run_time=0.6)
                slot += 1
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.3), FadeIn(lines[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(dlq), FadeIn(lines[2]))
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
