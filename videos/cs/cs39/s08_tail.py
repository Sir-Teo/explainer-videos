from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace)


class Tail(VoiceoverScene):
    def construct(self):
        self.card()
        self.fanout()
        self.hedging()
        self.choices()
        self.queues()
        self.chain()

    def card(self):
        card = chapter_card(7, r"The tail at scale", r"Why is a fast service slow?", lit=(2013, 2013),
                            extra=((2013, r"Dean and Barroso: \ The Tail at Scale"),), part=PART)
        with self.voiceover("Chapter seven. The tail at scale."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def fanout(self):
        t = load("tail")
        head = label(r"One slow server in a hundred", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 3, 1], [0, 1.05, 0.25], x_length=6.4, y_length=3.8, x_label=r"servers each request waits for",
                 y_label=r"requests that are slow", xticks=(0, 1, 2, 3), yticks=(0.25, 0.5, 0.75, 1.0),
                 fx=lambda v: f"{10 ** int(v):,}", fy=lambda v: f"{v * 100:.0f}\\%").move_to([-2.8, -0.4, 0])
        ax = g.ax
        f = ax.plot(lambda x: 1 - 0.99 ** (10 ** x), x_range=[0, 3], color=GREY_B, stroke_width=2)
        dots = VGroup(*[Dot(ax.c2p(math.log10(r["fanout"]), r["frac_slow"]), radius=0.07, color=NO)
                        for r in t["plain"]])
        rows = [[f"{r['fanout']:,}", f"{r['p50']:.0f} ms", f"{r['p99']:.0f} ms", f"{r['frac_slow'] * 100:.1f}\\%"]
                for r in t["plain"]]
        tab = grid_table([r"fan-out", r"median", r"99th pct", r"slow"], rows, widths=[1.5, 1.5, 1.6, 1.4],
                         row_h=0.4, font_size=18, mono_cols=())
        tab.move_to([3.7, 0.8, 0])
        notes = VGroup(
            wrapped_label(r"each server: \ 10 ms typically, \ but 1 s for 1 request in 100 \ (a garbage collection, \ "
                          r"a queue behind a big request, \ a background compaction)", 5.0, font_size=18,
                          color=GREY_A),
            MathTex(r"P(\text{slow}) = 1 - 0.99^{n}", font_size=30, color=NO),
            wrapped_label(r"at $n = 100$, \ 63\%: \ the rare case at one server is the common case for the "
                          r"service", 5.0, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.7, -1.7, 0])
        with self.voiceover(
            "Jeff Dean and Luiz Barroso's paper of 2013 starts from one observation. A web search, or a social "
            "media feed, fans out: one user request becomes requests to a hundred or a thousand servers, and the "
            "answer waits for all of them. <bookmark mark='a'/> Suppose each server answers in ten milliseconds, "
            "except one request in a hundred, which takes a full second, because of a garbage collection, or a queue "
            "behind some large request. <bookmark mark='b'/> With one server, one percent of requests are slow. "
            "Waiting for ten, nearly ten percent. Waiting for a hundred, sixty-three percent: one minus point nine "
            "nine to the hundred. Our simulation lands on the curve. <bookmark mark='c'/> The rare event at each "
            "server is the usual event for the service. Making every server's tail shorter is expensive; the "
            "trick is to tolerate it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(Create(f), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.3), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def hedging(self):
        t = load("tail")
        head = label(r"Hedged requests", font_size=36).to_edge(UP, buff=0.3)
        rows = []
        for a, b in zip(t["plain"], t["hedged"]):
            rows.append([f"{a['fanout']:,}", f"{a['p50']:.0f} ms", f"{b['p50']:.0f} ms", f"{a['p99']:.0f} ms",
                         f"{b['p99']:.0f} ms"])
        tab = grid_table([r"fan-out", r"median", r"median, \ hedged", r"99th pct", r"99th, \ hedged"], rows,
                         widths=[1.8, 1.8, 2.4, 1.8, 2.4], row_h=0.46, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        for k in range(1, len(rows) + 1):
            tab.cells[k][2].set_color(YES)
            tab.cells[k][4].set_color(YES)
        lines = VGroup(
            wrapped_label(rf"if a server has not answered after {t['hedge_ms']} ms \ (about its 95th percentile), \ "
                          r"send the same request to a second replica and take whichever answer comes first", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"costs about 5\% more requests; \ turns a 1-second tail into tens of milliseconds, \ until "
                          r"the fan-out is so large that two slow replicas in a row become likely", 12.4,
                          font_size=21, color=YES),
            wrapped_label(r"\textbf{tied requests} go further: \ send to both at once, \ and let the one that starts "
                          r"first cancel the other", 12.4, font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "The simplest remedy is to ask twice. <bookmark mark='a'/> If a server has not answered within thirty "
            "milliseconds, about its ninety-fifth percentile, send the same request to another replica and use "
            "whichever reply comes first. <bookmark mark='b'/> It costs about five percent more requests. With a "
            "fan-out of a hundred, the median falls from a full second to forty-three milliseconds. The ninety-ninth "
            "percentile improves too, until the fan-out is so large that some request meets two slow replicas in a "
            "row. <bookmark mark='c'/> Google's systems go further with tied requests: send to two servers at once, "
            "and whichever starts the work first tells the other to cancel."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, l in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def choices(self):
        t = load("tail")
        c = t["two_choices"]
        head = label(r"The power of two choices", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"random server", f"{c['1']:.1f}", r"$\approx \ln n / \ln\ln n$"],
                [r"the less loaded of 2", f"{c['2']:.1f}", r"$\approx \ln\ln n / \ln 2$"],
                [r"the least loaded of 3", f"{c['3']:.1f}", r"$\approx \ln\ln n / \ln 3$"]]
        tab = grid_table([r"each request goes to", r"busiest of 1{,}000 servers", r"theory"], rows,
                         widths=[4.4, 3.6, 3.4], row_h=0.5, font_size=22, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        for k in (2, 3):
            tab.cells[k][1].set_color(YES)
        tab.cells[1][1].set_color(NO)
        lines = VGroup(
            wrapped_label(r"1{,}000 requests on 1{,}000 servers: \ sampling two and picking the shorter queue cuts the "
                          r"worst load from 5.5 to 3 \ (Azar, Broder, Karlin and Upfal, 1994; \ Mitzenmacher; \ "
                          r"Part 20's balls in bins)", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"the jump is from one choice to two; \ more choices add little: \ load balancers "
                          r"\ (NGINX, \ Envoy) \ ship it as the default", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Tails also come from uneven load, and one of the best results in randomized algorithms fixes that. "
            "<bookmark mark='a'/> Send a thousand requests to a thousand servers at random, and the busiest server "
            "gets about five and a half of them, as Part 20's balls-in-bins analysis predicts. Instead, sample two "
            "servers and send each request to the less loaded one: the busiest gets three. Exponentially better, "
            "for one extra probe. <bookmark mark='b'/> A third choice adds little. Load balancers like NGINX and Envoy "
            "ship the power of two choices as their default."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def queues(self):
        b = load("balance")
        PC = {"random": NO, "round robin": KERN, "two choices": YES, "shortest queue": DATA}
        head = label(r"Balancing a queue, \ not a count", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0.5, 0.96, 0.1], [0, 2.05, 0.5], x_length=6.4, y_length=3.9, x_label=r"load \ (fraction of capacity)",
                 y_label=r"99th-percentile response \ (in service times)", xticks=(0.5, 0.6, 0.7, 0.8, 0.9),
                 yticks=(0, math.log10(3), 1, math.log10(30), 2),
                 fy=lambda v: f"{10 ** v:.0f}").move_to([-2.8, -0.4, 0])
        ax = g.ax
        curves = {}
        for p, c in PC.items():
            pts = [(r["load"], math.log10(r["p99"])) for r in b["rows"] if r["policy"] == p]
            curves[p] = VGroup(trace(ax, pts, c, width=3), *[Dot(ax.c2p(x, y), radius=0.05, color=c) for x, y in pts])
        at = {r["policy"]: r for r in b["rows"] if r["load"] == 0.95}
        leg = VGroup(*[label(rf"{p}: \ {at[p]['p99']:.0f}", font_size=19, color=c) for p, c in PC.items()]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.14)
        legh = label(r"99th percentile at 95\% load", font_size=18, color=GREY_A)
        VGroup(legh, leg).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.1, 1.5, 0])
        notes = VGroup(
            wrapped_label(rf"{b['servers']} servers, \ random arrivals, \ random job lengths \ (Part 31's M/M/1, \ "
                          r"times 100)", 5.0, font_size=17, color=GREY_A),
            wrapped_label(r"random routing makes each server an M/M/1 queue: \ its tail grows like $1/(1-\rho)$; \ "
                          r"round robin halves it, \ no more", 5.0, font_size=18, color=NO),
            wrapped_label(r"two choices \ (Mitzenmacher's supermarket model, \ 1996): \ queue lengths fall "
                          r"doubly exponentially, \ and the tail stays near the ideal of asking every server", 5.0,
                          font_size=18, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.1, -1.5, 0])
        with self.voiceover(
            "Requests are not balls that land and stay; they wait in queues and leave. Michael Mitzenmacher's "
            "supermarket model asks the same question for queues. <bookmark mark='a'/> A hundred servers, requests "
            "arriving at random, each taking a random time. Sent to a random server, each server becomes Part 31's "
            "single queue, and the tail explodes as load approaches capacity: at ninety-five percent load the "
            "ninety-ninth percentile is eighty-two times the service time. <bookmark mark='b'/> Round robin, which "
            "never sends two requests in a row to the same server, halves that, and no more, because job lengths "
            "still vary. <bookmark mark='c'/> Two random choices, picking the shorter of two queues, brings it to "
            "ten and a half: queue lengths now fall off doubly exponentially. <bookmark mark='d'/> Asking every "
            "server for its queue length gets five, but asking a hundred servers costs a hundred messages per "
            "request. Two choices gets most of the way for two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]), FadeIn(legh))
            vo.wait_until("a")
            self.play(Create(curves["random"]), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(curves["round robin"]), FadeIn(leg[1]), FadeIn(notes[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(curves["two choices"]), FadeIn(leg[2]), FadeIn(notes[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(curves["shortest queue"]), FadeIn(leg[3]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def chain(self):
        c = load("chain")
        head = label(r"Tails through a call graph", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{r['depth']}", f"{r['p50']:.0f} ms", f"{r['p99']:.0f} ms", f"{r['sum_of_p99']:.0f} ms"]
                for r in c["chain"]]
        t1 = grid_table([r"services in a row", r"median", r"99th pct", r"sum of their 99ths"], rows,
                        widths=[2.4, 1.4, 1.5, 2.4], row_h=0.4, font_size=18, mono_cols=())
        rr = [[f"{r['layers']}", f"{r['attempts']:,}", f"{r['budgeted']:.2f}"] for r in c["retries"]]
        t2 = grid_table([r"layers retrying", r"3 retries each", r"10\% retry budget"], rr, widths=[2.2, 2.0, 2.4],
                        row_h=0.4, font_size=18, mono_cols=())
        h1 = label(r"latency in series \ (each: median 10 ms, \ 99th 65 ms)", font_size=19, color=HEAD)
        h2 = label(r"attempts reaching a failed bottom service", font_size=19, color=NO)
        c1 = VGroup(h1, t1).arrange(DOWN, buff=0.2).move_to([-3.3, 0.7, 0])
        c2 = VGroup(h2, t2).arrange(DOWN, buff=0.2).move_to([3.5, 0.7, 0])
        for k in range(1, len(rr) + 1):
            t2.cells[k][1].set_color(NO)
            t2.cells[k][2].set_color(YES)
        lines = VGroup(
            wrapped_label(r"percentiles do not add: \ a budget that sums each service's 99th percentile "
                          r"over-provisions a chain, \ and under-provisions a fan-out", 12.4, font_size=20,
                          color=HEAD),
            wrapped_label(r"pass the remaining deadline along with each call, \ retry at one layer only, \ and cap "
                          r"retries at a fraction of requests: \ gRPC deadlines, \ Finagle's retry budgets", 12.4,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Real requests pass through chains of services, and the tail travels with them. "
            "<bookmark mark='a'/> Give each service a median of ten milliseconds and a ninety-ninth percentile of "
            "sixty-five. Through three in a row, the end-to-end ninety-ninth percentile is a hundred and twenty "
            "milliseconds, not the hundred and ninety-two you get by adding; through ten, two hundred and sixty-five, "
            "not six hundred and fifty. Percentiles do not add, which makes naive latency budgets too generous for "
            "chains and, as we saw, far too stingy for fan-outs. <bookmark mark='b'/> Retries multiply. If the "
            "bottom service is down and each of three layers retries three times, every user request becomes sixty-"
            "four attempts at the bottom, just when it can least afford them: the retry storm of the next chapter, "
            "built in. <bookmark mark='c'/> The remedies are boring and effective: send the remaining deadline "
            "with every call so that work nobody awaits is never started, retry at one layer only, and cap "
            "retries at a tenth of requests, so that even four layers add less than half again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(c2))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN, LAM, trace)
