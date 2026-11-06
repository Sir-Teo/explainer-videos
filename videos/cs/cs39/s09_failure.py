from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace)

MC = {"no retries": DATA, "retries": NO, "retries, backoff": KERN, "retries, drop expired": YES}


class Failure(VoiceoverScene):
    def construct(self):
        self.card()
        self.kinds()
        self.year()
        self.nines()
        self.detect()
        self.metastable()
        self.practice()

    def card(self):
        card = chapter_card(8, r"Failure at scale", r"What breaks when there are a hundred thousand machines?",
                            lit=(2011, 2022), extra=((2011, r"Netflix: \ Chaos Monkey"),
                                                     (2017, r"Huang et al.: \ gray failure"),
                                                     (2022, r"Huang et al.: \ metastable failures")), part=PART)
        with self.voiceover("Chapter eight. Failure at scale."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def kinds(self):
        head = label(r"Failures are not independent", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"with 100{,}000 disks of a 1\% annual failure rate, \ about 3 fail every day: \ failure is "
                          r"the normal state, \ and recovery must be automatic", 12.4, font_size=22, color=WHITE),
            wrapped_label(r"\textbf{correlated failures}: \ a power distribution unit, \ a top-of-rack switch, \ a "
                          r"bad configuration pushed everywhere at once, \ a leap second: \ replicas must sit in "
                          r"different failure domains, \ and changes must roll out slowly", 12.4, font_size=22,
                          color=NO),
            wrapped_label(r"\textbf{gray failure}: \ a machine that is slow, \ or fails only some requests, \ passes "
                          r"its health checks while users suffer: \ the observer and the user disagree", 12.4,
                          font_size=22, color=KERN),
            wrapped_label(r"\textbf{metastable failure}: \ a trigger passes, \ but the system stays down, \ held there "
                          r"by its own reaction to the trigger", 12.4, font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "At scale, failure stops being an event and becomes a rate. <bookmark mark='a'/> A hundred thousand "
            "disks failing at one percent a year means about three every day. Recovery has to be automatic, and so "
            "routine that nobody is paged. <bookmark mark='b'/> Worse, failures are not independent. A power unit "
            "or a top-of-rack switch takes down many machines at once; a bad configuration pushed everywhere takes "
            "down everything. So replicas go in different failure domains, and changes roll out slowly. "
            "<bookmark mark='c'/> Gray failures are machines that are slow, or fail only some requests, and still "
            "pass their health checks. <bookmark mark='d'/> And metastable failures, named in 2022, are the "
            "strangest: the trigger passes, but the system stays down, held there by its own reaction."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def metastable(self):
        m = load("meta")
        head = label(r"A retry storm", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 120, 20], [0, 120, 25], x_length=7.4, y_length=3.8, x_label=r"seconds",
                 y_label=r"useful answers per second", xticks=range(0, 121, 20), yticks=(25, 50, 75, 100)).move_to(
            [-2.4, -0.4, 0])
        ax = g.ax
        sp = m["retries"]["spike"]
        band = Rectangle(width=ax.c2p(sp[1], 0)[0] - ax.c2p(sp[0], 0)[0], height=3.8, stroke_width=0,
                         fill_color=NO, fill_opacity=0.12).move_to([(ax.c2p(sp[0], 0)[0] + ax.c2p(sp[1], 0)[0]) / 2,
                                                                     ax.c2p(0, 60)[1], 0])
        bl = label(r"load spike: \ 160/s", font_size=17, color=NO).next_to(band, RIGHT, buff=0.1).align_to(band, UP).shift(DOWN * 0.1)
        lines = {k: trace(ax, list(enumerate(v["goodput"])), MC[k], width=2.6) for k, v in m.items()}
        leg = VGroup(*[label(rf"{k}: \ after the spike {v['after']:.0f}/s", font_size=18, color=MC[k])
                       for k, v in m.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, 1.2, 0])
        notes = VGroup(
            wrapped_label(r"capacity 100/s, \ normal load 80/s; \ clients give up after 1 s \ and retry up to 3 "
                          r"times; \ the server still works on requests whose clients have left", 4.8, font_size=17,
                          color=GREY_A),
            wrapped_label(r"retries multiply the load by up to 4: \ the queue never drains, \ and every answer comes "
                          r"too late: \ zero goodput, \ for ever", 4.8, font_size=18, color=NO),
            wrapped_label(r"cures: \ drop work whose deadline has passed, \ shed load, \ retry budgets, \ circuit "
                          r"breakers; \ backoff alone is not enough here", 4.8, font_size=18, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, -1.5, 0])
        with self.voiceover(
            "Here is a metastable failure, simulated. A server can answer a hundred requests a second and normally "
            "gets eighty. Clients give up after one second and retry, up to three times. <bookmark mark='a'/> For "
            "ten seconds, load spikes to a hundred and sixty. Without retries the server falls behind, and when the "
            "spike passes it slowly drains its queue and recovers. <bookmark mark='b'/> With retries, every slow "
            "request comes back as two, three, four requests. The server is now working mostly on requests whose "
            "clients have already given up, every answer is too late, and goodput stays at zero long after the spike "
            "has gone. Random backoff does not save it. <bookmark mark='c'/> What does is refusing work that can no "
            "longer be useful: dropping requests whose deadline has passed brings the server straight back. Load "
            "shedding, retry budgets and circuit breakers are the same idea, and part 50 builds them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(band), FadeIn(bl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(lines["no retries"]), FadeIn(leg[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines["retries"]), Create(lines["retries, backoff"]), FadeIn(leg[1]), FadeIn(leg[2]),
                      FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(lines["retries, drop expired"]), FadeIn(leg[3]), FadeIn(notes[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def practice(self):
        head = label(r"Breaking things on purpose", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{chaos engineering}: \ Netflix's Chaos Monkey \ (2011) \ kills production machines "
                          r"at random during working hours, \ so recovery is exercised daily", 12.4, font_size=22,
                          color=YES),
            wrapped_label(r"\textbf{game days} and disaster-recovery tests: \ fail a whole datacenter, \ on purpose", 12.4,
                          font_size=22, color=HEAD),
            wrapped_label(r"\textbf{blameless post-mortems}: \ published accounts of real outages \ (cloud providers, \ "
                          r"2010s--2020s) \ show the same causes again and again: \ configuration changes, \ "
                          r"retries, \ expired certificates, \ dependency loops", 12.4, font_size=22, color=KERN),
            wrapped_label(r"and the lesson of Part 38: \ the code that runs only during failures is the code that "
                          r"has been tested least", 12.4, font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Because failure is constant, the large operators practise it. <bookmark mark='a'/> Netflix's Chaos "
            "Monkey, from 2011, kills machines in production, at random, during working hours, so that recovery is "
            "exercised every day instead of discovered during a crisis. <bookmark mark='b'/> Companies hold game "
            "days that fail an entire datacenter on purpose. <bookmark mark='c'/> And the industry publishes "
            "blameless post-mortems of real outages, which show the same causes over and over: a configuration "
            "change, a retry storm, an expired certificate, a dependency loop where the recovery tool depends on the "
            "thing that failed. <bookmark mark='d'/> It is the lesson of our Raft campaign at datacenter scale: the "
            "code that runs only during failures is the least tested code in the system."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def nines(self):
        a = load("nines")
        head = label(r"Counting nines", font_size=36).to_edge(UP, buff=0.3)

        def down(u):
            m = (1 - u) * 365.25 * 24 * 60
            if m >= 24 * 60:
                return f"{m / 60 / 24:.1f} days"
            if m >= 60:
                return f"{m / 60:.1f} hours"
            if m >= 1:
                return f"{m:.0f} min"
            return f"{m * 60:.2g} s"
        sr = [[f"{r['deps']}", f"{r['up'] * 100:.2f}\\%", down(r["up"])] for r in a["series"]]
        t1 = grid_table([r"needs all of", r"up", r"down per year"], sr, widths=[2.1, 1.8, 2.3], row_h=0.44,
                        font_size=20, mono_cols=())
        pr = [[f"{r['replicas']}", f"{r['up'] * 100:.7f}".rstrip("0") + r"\%", down(r["up"])] for r in a["parallel"]]
        t2 = grid_table([r"any one of", r"up", r"down per year"], pr, widths=[2.0, 2.5, 2.2], row_h=0.44, font_size=20,
                        mono_cols=())
        h1 = label(r"in series: \ each part 99.9\%", font_size=23, color=NO)
        h2 = label(r"in parallel, \ if independent", font_size=23, color=YES)
        c1 = VGroup(h1, t1).arrange(DOWN, buff=0.2).move_to([-3.4, 0.6, 0])
        c2 = VGroup(h2, t2).arrange(DOWN, buff=0.2).move_to([3.4, 1.0, 0])
        for k in range(1, len(sr) + 1):
            t1.cells[k][1].set_color(NO)
        for k in range(1, len(pr) + 1):
            t2.cells[k][1].set_color(YES)
        c = a["corr"]
        corr = VGroup(
            wrapped_label(rf"but racks fail too \ (here 0.05\% of the time): \ three replicas in one rack are up "
                          rf"{c['same_rack'] * 100:.2f}\%, \ worse than one machine; \ in three racks, \ "
                          rf"{c['three_racks'] * 100:.0f}\% in 2 million trials", 6.2, font_size=20, color=KERN),
        ).move_to([3.4, -1.6, 0])
        foot = wrapped_label(r"a service is no more available than the product of what it needs: \ promise less than "
                             r"your dependencies, \ cut the chain, \ and place replicas in separate failure domains",
                             12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Availability is measured in nines. Ninety-nine point nine percent, three nines, allows about nine hours "
            "of downtime a year. <bookmark mark='a'/> Parts in series multiply. A request that needs ten services, "
            "each at three nines, succeeds only ninety-nine percent of the time; a hundred, about ninety percent, "
            "more than a month of failure a year. That is why a page that calls many services must tolerate some of "
            "them failing. <bookmark mark='b'/> Replicas in parallel multiply the other way: if any one of three "
            "independent replicas will do, three nines become nine nines, thirty milliseconds of downtime a year. "
            "<bookmark mark='c'/> But the word independent carries the whole result. Put the three replicas in one "
            "rack whose switch fails a twentieth of a percent of the time, and they are worse than a single machine "
            "elsewhere. In three racks, two million simulated moments saw no outage at all. <bookmark mark='d'/> So "
            "never promise more than your dependencies multiply to, shorten the chain of things a request needs, "
            "and put replicas in separate failure domains: racks, power feeds, buildings, regions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(c1))
            vo.wait_until("b")
            self.play(FadeIn(c2))
            vo.wait_until("c")
            self.play(FadeIn(corr))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def detect(self):
        d = load("detect")
        head = label(r"Is it dead, \ or just slow?", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 1100, 200], [-0.5, 3.2, 1], x_length=6.6, y_length=3.8, x_label=r"ms to detect a real crash",
                 y_label=r"false alarms per hour", xticks=range(0, 1001, 200), yticks=(0, 1, 2, 3),
                 fy=lambda v: f"{10 ** v:,.0f}").move_to([-2.6, -0.4, 0])
        ax = g.ax

        def pts(rows):
            return [(r["detect_ms"], math.log10(max(r["false_per_hour"], 0.35))) for r in rows if r["detect_ms"] <= 1100]
        fx = VGroup(trace(ax, pts(d["fixed"]), NO, width=3), *[Dot(ax.c2p(x, y), radius=0.06, color=NO)
                                                               for x, y in pts(d["fixed"])])
        ph = VGroup(trace(ax, pts(d["accrual"]), YES, width=3), *[Dot(ax.c2p(x, y), radius=0.06, color=YES)
                                                                  for x, y in pts(d["accrual"])])
        f150 = next(r for r in d["fixed"] if r["timeout_ms"] == 175)
        p12 = next(r for r in d["accrual"] if r["phi"] == 12)
        notes = VGroup(
            wrapped_label(r"a heartbeat every 100 ms over a network that alternates calm and congested spells, \ "
                          r"plus rare garbage-collection pauses of up to 2.5 s; \ 10 simulated hours", 5.0,
                          font_size=17, color=GREY_A),
            wrapped_label(rf"\textbf{{fixed timeout}}: \ {f150['timeout_ms']} ms gives "
                          rf"{f150['false_per_hour']:.0f} false alarms an hour; \ the timeout must cover the worst "
                          r"spell", 5.0, font_size=18, color=NO),
            wrapped_label(rf"\textbf{{phi accrual}} \ (Hayashibara et al., 2004; \ Cassandra, \ Akka): \ suspicion "
                          rf"grows with how unlikely the silence is, \ given recent gaps: \ no hand tuning, \ but "
                          rf"the same trade-off \ ({p12['false_per_hour']:.0f} an hour at {p12['detect_ms']:.0f} ms)",
                          5.0, font_size=18,
                          color=YES),
            wrapped_label(r"no timeout separates a crash from a long pause \ (FLP, \ Part 38): \ a suspected node "
                          r"must be fenced off, \ not merely ignored", 5.0, font_size=18, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, -0.3, 0])
        with self.voiceover(
            "Every recovery we have seen starts with a decision: this machine has failed. But a machine that has "
            "crashed and one that is merely slow look the same from outside. <bookmark mark='a'/> We simulated "
            "heartbeats every hundred milliseconds across a network that alternates between calm and congested "
            "spells, with occasional garbage-collection pauses. A fixed timeout must be long enough for the worst "
            "spell: a timeout of a hundred and seventy-five milliseconds raises about a hundred false alarms an "
            "hour, and getting below a few an hour means waiting a quarter of a second or more. "
            "<bookmark mark='b'/> The phi accrual detector, used by Cassandra and Akka, instead keeps a window of "
            "recent gaps and raises its suspicion as the current silence becomes less likely. It needs no hand-tuned "
            "timeout, and it adapts when the network changes. But on our trace it lands on almost the same curve: "
            "faster detection buys false alarms, whichever detector you use. "
            "<bookmark mark='c'/> Neither can be certain, which is Part 38's lesson again. So a node that has been "
            "declared dead must be fenced off, by a new term, an epoch or a fencing token, because it may wake up "
            "and keep working."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(fx), FadeIn(notes[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(ph), FadeIn(notes[2]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def year(self):
        head = label(r"A year in the life of a cluster", font_size=36).to_edge(UP, buff=0.3)
        cited = [(r"individual machine failures", r"$\sim$1{,}000"), (r"hard-disk failures", r"thousands"),
                 (r"rack failures \ (40--80 machines vanish)", r"$\sim$20"),
                 (r"racks that go wonky \ (half their packets lost)", r"$\sim$5"),
                 (r"router failures and reloads", r"$\sim$15"), (r"a network rewiring", r"$\sim$1"),
                 (r"a power-distribution failure \ (500--1{,}000 machines, \ 6 hours)", r"$\sim$1")]
        tab = grid_table([r"in a new cluster's first year", r"how often"], [list(r) for r in cited],
                         widths=[7.2, 2.0], row_h=0.4, font_size=19, mono_cols=())
        tab.move_to([-2.0, 0.5, 0])
        src = label(r"Jeff Dean, \ LADIS keynote, \ 2009", font_size=16, color=GREY_B).next_to(tab, DOWN, buff=0.15)
        mtbf_h = 3 * 365.25 * 24

        def p_none(machines, hours):
            return math.exp(-machines * hours / mtbf_h)
        calc = VGroup(
            label(r"machines lasting 3 years on average:", font_size=19, color=GREY_A),
            label(rf"a 6-hour job on 1{{,}}000: \ {p_none(1000, 6) * 100:.0f}\% chance of no failure", font_size=19,
                  color=KERN),
            label(rf"a day on 10{{,}}000: \ {p_none(10000, 24) * 100:.2g}\%", font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 0.8, 0])
        foot = wrapped_label(r"so recovery is the normal path, \ not the exception: \ MapReduce's re-execution, \ "
                             r"Raft's elections and Dynamo's hinted handoff run every day", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 2009 Jeff Dean listed what a typical new Google cluster goes through in its first year. "
            "<bookmark mark='a'/> About a thousand individual machine failures and thousands of disk failures. "
            "Twenty racks failing, each taking forty to eighty machines with it, and five racks going wonky, "
            "losing half their packets. A dozen or so router failures and reloads, a network rewiring, and a power "
            "distribution failure that takes down five hundred to a thousand machines for six hours. "
            "<bookmark mark='b'/> Do the arithmetic for machines that last three years on average. A six-hour job on "
            "a thousand machines finishes without a single failure only four times in five. A day on ten thousand "
            "machines, essentially never. <bookmark mark='c'/> So recovery is the normal path, not the exception: "
            "MapReduce's re-execution, Raft's elections and Dynamo's hinted handoff are running somewhere every day."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(calc))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, LAM)
