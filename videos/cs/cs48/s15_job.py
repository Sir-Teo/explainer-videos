from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs48.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def box(name, color, w=2.3, h=0.75, size=19):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2, fill_color=BG,
                         fill_opacity=1)
    return VGroup(r, label(name, font_size=size, color=color).move_to(r))


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.design()
        self.load_test()
        self.cache()

    def card(self):
        card = chapter_card(14, r"The Job as a service", r"Does the design survive its load?",
                            lit=(1961, 2007), extra=((1961, r"Kleinrock: \ queueing networks"),
                                                     (2007, r"Dynamo's 99.9th percentile SLAs")), part=PART)
        with self.voiceover("Chapter fourteen. The Job as a service."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def design(self):
        p = load("jobsvc")["plain"]
        head = label(r"Upload a book, \ get its top words", font_size=36).to_edge(UP, buff=0.3)
        client = box(r"client", WHITE, w=1.6).move_to([-5.8, 0.8, 0])
        lb = box(r"load balancer", HEAD, w=2.2).move_to([-3.4, 0.8, 0])
        api = box(r"API servers", DATA, w=2.0).move_to([-0.9, 0.8, 0])
        cache = box(r"result cache", YES, w=2.1).move_to([-0.9, -0.8, 0])
        q = box(r"work queue", LAM, w=1.9).move_to([1.6, 0.8, 0])
        workers = box(rf"{p['servers']} workers", KERN, w=1.9).move_to([4.0, 0.8, 0])
        blob = box(r"blob store", GREY_A, w=1.9).move_to([4.0, -0.8, 0])
        parts = VGroup(client, lb, api, cache, q, workers, blob)
        arrows = VGroup(Arrow(client.get_right(), lb.get_left(), buff=0.05, color=GREY_B, stroke_width=2),
                        Arrow(lb.get_right(), api.get_left(), buff=0.05, color=GREY_B, stroke_width=2),
                        DoubleArrow(api.get_bottom(), cache.get_top(), buff=0.05, color=YES, stroke_width=2),
                        Arrow(api.get_right(), q.get_left(), buff=0.05, color=GREY_B, stroke_width=2),
                        Arrow(q.get_right(), workers.get_left(), buff=0.05, color=GREY_B, stroke_width=2),
                        DoubleArrow(workers.get_bottom(), blob.get_top(), buff=0.05, color=GREY_B, stroke_width=2))
        notes = VGroup(
            wrapped_label(rf"{p['books']:,} books, \ requested with Zipf popularity; \ counting one takes "
                          rf"{p['work_ms']:.0f} ms of a worker on average \ (a model)", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"capacity: \ " + rf"{p['servers']} workers $\times$ 1000 / {p['work_ms']:.0f} ms $=$ "
                          rf"{p['servers'] * 1000 / p['work_ms']:.0f} requests a second at 100\% busy", 12.4,
                          font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The Job, one more time, now as a service: upload a book, or name one, and get its twenty most common "
            "words. <bookmark mark='a'/> Requests arrive at a load balancer, which spreads them over stateless API "
            "servers. An API server first asks a result cache; on a miss, it puts the work on a queue, and one of "
            f"{p['servers']} workers fetches the book from a blob store and counts it. <bookmark mark='b'/> Our model "
            f"has {p['books']:,} books, some far more popular than others, and a count takes "
            f"{p['work_ms']:.0f} milliseconds on average. <bookmark mark='c'/> The napkin says the workers can handle "
            f"{p['servers'] * 1000 / p['work_ms']:.0f} requests a second if they are never idle. Never idle is the "
            "problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in parts], lag_ratio=0.2), Create(arrows), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def load_test(self):
        j = load("jobsvc")
        p, c = j["plain"]["rows"], j["cached"]["rows"]
        head = label(r"The load test", font_size=36).to_edge(UP, buff=0.3)
        x0, y0, xw, yh = -6.0, -2.3, 7.4, 4.3
        xmax = 260
        lmin, lmax = 0.0, math.log10(1000)

        def pt(q, ms):
            return [x0 + q / xmax * xw, y0 + (math.log10(max(ms, 1)) - lmin) / (lmax - lmin) * yh, 0]
        ax = VGroup(Line([x0, y0, 0], [x0 + xw, y0, 0], color=GREY_C), Line([x0, y0, 0], [x0, y0 + yh, 0],
                                                                              color=GREY_C))
        ticks = VGroup(*[label(f"{q}", font_size=15, color=GREY_B).move_to([pt(q, 1)[0], y0 - 0.25, 0])
                         for q in (0, 50, 100, 150, 200, 250)],
                       *[label(f"{v} ms", font_size=15, color=GREY_B).move_to([x0 - 0.5, pt(0, v)[1], 0])
                         for v in (1, 10, 100, 1000)])
        xl = label(r"requests per second", font_size=17, color=GREY_B).next_to(ax[0], DOWN, buff=0.45)

        def line(rows, key, col, dash=False):
            pts = [pt(r["qps"], min(r[key], 999)) for r in rows]
            m = VMobject(color=col, stroke_width=3).set_points_as_corners(pts)
            return DashedVMobject(m, num_dashes=30) if dash else m
        lp50, lp99 = line(p, "p50_ms", DATA), line(p, "p99_ms", NO)
        cp50, cp99 = line(c, "p50_ms", DATA, True), line(c, "p99_ms", NO, True)
        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.5, color=cl, stroke_width=3), label(t, font_size=16, color=cl))
                          .arrange(RIGHT, buff=0.12) for t, cl in ((r"p50, \ no cache", DATA), (r"p99, \ no cache", NO),
                                                                   (r"dashed: \ with a cache", GREY_A))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to([x0 + 1.5, y0 + yh - 0.4, 0])
        last = p[-1]
        side = VGroup(
            wrapped_label(rf"no cache: \ at {p[0]['qps']} requests a second, \ p99 {p[0]['p99_ms']:.0f} ms; \ at "
                          rf"{last['qps']} \ ({100 * last['utilization']:.0f}\% busy), \ {last['p99_ms']:.0f} ms", 4.6,
                          font_size=19, color=NO),
            wrapped_label(rf"with a {j['cached']['cache_size']}-entry cache: \ {100 * c[0]['hit_rate']:.0f}\% of "
                          rf"requests hit, \ and the same p99 holds to about {c[-2]['qps']} a second", 4.6,
                          font_size=19, color=YES),
            wrapped_label(r"the median barely moves until the knee; \ the tail tells you where the knee is", 4.6,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "So we load-tested the design in simulation, raising the rate of requests and measuring the median and "
            "the ninety-ninth percentile response time. <bookmark mark='a'/> Without a cache, the median sits near "
            f"{p[0]['p50_ms']:.0f} milliseconds and the tail near {p[0]['p99_ms']:.0f}, until the workers get busy. "
            f"At {last['qps']} requests a second they are {100 * last['utilization']:.0f} percent busy, and the tail "
            f"has grown to {last['p99_ms']:.0f} milliseconds: Part 31's queueing curve again. "
            "<bookmark mark='b'/> Add a result cache of three hundred entries. Because popularity is so skewed, "
            f"{100 * c[0]['hit_rate']:.0f} percent of requests hit it and return in a millisecond, so the median "
            f"collapses, and the workers see only the misses: the same tail now holds to about {c[-2]['qps']} "
            "requests a second, more than double. <bookmark mark='c'/> Notice that the median says little; the "
            "tail tells you where the knee is."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(legend))
            vo.wait_until("a")
            self.play(Create(lp50), Create(lp99), run_time=2)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cp50), Create(cp99), run_time=2)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def cache(self):
        c = load("caches")
        head = label(r"What the cache bought, \ and why", font_size=36).to_edge(UP, buff=0.3)
        r = next(x for x in c["rows"] if x["size"] == 300)
        bars = VGroup()
        for k, (name, key, col) in enumerate(((r"LRU", "lru", DATA), (r"Che's formula", "che", GREY_A),
                                              (r"W-TinyLFU", "tinylfu", YES),
                                              (r"best possible static set", "optimal_static", HEAD))):
            v = r[key]
            w = v * 12
            b = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-5.2 + w / 2, 1.4 - 0.75 * k, 0])
            bars.add(VGroup(b, label(rf"{name}: \ {100 * v:.1f}\%", font_size=18, color=col).next_to(b, RIGHT,
                                                                                                buff=0.15)))
        cap = label(rf"hit rates, \ 300 of {c['items']:,} items, \ Zipf traffic \ (chapter 3)", font_size=18,
                    color=GREY_B).next_to(bars, UP, buff=0.3).align_to(bars, LEFT)
        lines = VGroup(
            wrapped_label(r"capacity grows by $1/(1-h)$ for hit rate $h$, \ if the cache itself is cheap: \ the "
                          r"cheapest work is the work not done", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"the price: \ staleness when a book changes, \ and a stampede when a popular entry expires "
                          r"\ (chapter 4)", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Why did three hundred entries do so much? <bookmark mark='a'/> Chapter three's numbers answer it. On "
            f"skewed traffic, three hundred entries of LRU catch {100 * r['lru']:.0f} percent of requests in a "
            "catalogue of a hundred thousand, exactly as Che's formula predicts; an admission filter like TinyLFU "
            f"catches {100 * r['tinylfu']:.0f}, close to the best possible fixed set. <bookmark mark='b'/> A hit "
            "rate h multiplies capacity by one over one minus h, as long as the cache is cheap to ask, which is why "
            "caches appear in every design. <bookmark mark='c'/> The price is that answers can be stale when a book "
            "changes, and that a popular entry expiring can set off a stampede, the problems of chapter four."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b[0], LEFT) for b in bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(b[1]) for b in bars], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM)
