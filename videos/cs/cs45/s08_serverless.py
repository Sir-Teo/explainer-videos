from __future__ import annotations

import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load,
                                   module_box, tag_box)

PER_SERVER_RPS = 200    # the model's assumption in explainer/cs/cloud/cost.serverless_vs_server (one m5.large)


class Serverless(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.bill()
        self.cold()
        self.concurrency()

    def card(self):
        card = chapter_card(7, r"Serverless", r"What if you rented only the milliseconds?",
                            lit=(2014, 2020), extra=((2014, r"AWS Lambda"),
                                                     (2019, r"Jonas et al.: \ the Berkeley view"),
                                                     (2020, r"Shahrad et al.: \ serverless in the wild")), part=PART)
        with self.voiceover("Chapter seven. Serverless."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def model(self):
        head = label(r"A function, \ not a server", font_size=36).to_edge(UP, buff=0.3)
        srcs = VGroup(*[tag_box(t, color=DATA, size=19, w=2.7, h=0.56) for t in
                        ("HTTP request", "file uploaded", "queue message", "timer")]).arrange(DOWN, buff=0.32)
        srcs.move_to([-5.45, 0.45, 0])
        code = code_block(["def handler(event, context):", "    words = count(event['text'])",
                           "    put('top20', words[:20])", "    return 'done'"], size=18)
        frame = SurroundingRectangle(code, buff=0.25, corner_radius=0.1, color=HEAD, stroke_width=2)
        fn = VGroup(frame, code).next_to(srcs, RIGHT, buff=0.75)
        fl = label(r"your function", font_size=20, color=HEAD).next_to(frame, UP, buff=0.15)
        arrows = VGroup(*[Arrow(s.get_right(), frame.get_left(), buff=0.1, stroke_width=2, color=GREY_B,
                                max_tip_length_to_length_ratio=0.1) for s in srcs])
        inst = VGroup(*[module_box(r"instance", KERN, w=2.0, h=0.56, font=19) for _ in range(3)]).arrange(
            DOWN, buff=0.28).next_to(frame, RIGHT, buff=0.9)
        to_inst = Arrow(frame.get_right(), inst.get_left(), buff=0.1, stroke_width=2, color=GREY_B,
                        max_tip_length_to_length_ratio=0.15)
        counts = [label(rf"instances: \ {k}", font_size=20, color=KERN).next_to(inst, UP, buff=0.2)
                  for k in range(4)]
        zero = label(r"no events: \ no instances, \ no bill", font_size=19, color=YES).next_to(inst, UP, buff=0.2)
        store = module_box(r"storage, \ database", LAM, w=2.6, h=0.6, font=19).next_to(inst, DOWN, buff=0.7)
        to_store = Arrow(inst.get_bottom(), store.get_top(), buff=0.08, stroke_width=2, color=LAM,
                         max_tip_length_to_length_ratio=0.2)
        diag = VGroup(srcs, fn, fl, arrows, inst, to_inst, *counts, zero, store, to_store)
        diag.shift(LEFT * (VGroup(srcs, inst).get_center()[0]))
        lines = VGroup(
            wrapped_label(r"the platform starts an instance per concurrent event, \ runs the function, \ and bills "
                          r"the milliseconds it ran", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"instances may vanish at any moment: \ state lives outside them, \ and functions "
                          r"talk through storage \ (Jonas et al., \ Berkeley, \ 2019)", 12.4, font_size=19,
                          color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 2014 Amazon launched Lambda, and with it a new contract. <bookmark mark='a'/> You do not rent a "
            "machine at all. You upload a function and name the events that should run it: a web request, a file "
            "arriving in storage, a message on a queue, a timer. <bookmark mark='b'/> For each event the platform "
            "finds or starts an instance, runs the function, and bills the milliseconds it ran. "
            "<bookmark mark='c'/> With no events there are no instances and no bill: it scales to zero. "
            "<bookmark mark='d'/> The price of that freedom is statelessness. An instance may vanish at any "
            "moment, so anything that must last goes to storage or a database, and functions talk to each other "
            "through them. Jonas and colleagues at Berkeley, in 2019, predicted that this style would come to "
            "dominate cloud computing, and catalogued these limits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fn), FadeIn(fl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in srcs], lag_ratio=0.25), Create(arrows))
            vo.wait_until("b")
            self.play(Create(to_inst), FadeIn(counts[0]), FadeIn(lines[0]))
            for k in range(3):
                self.play(FadeIn(inst[k], shift=LEFT * 0.2), Transform(counts[0], counts[k + 1]), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeOut(inst, shift=RIGHT * 0.2), Transform(counts[0], zero))
            vo.wait_until("d")
            self.play(FadeIn(inst), FadeIn(store), Create(to_store), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def bill(self):
        s = load("serverless")
        pr = s["prices"]
        compute = s["ms"] / 1000 * s["mb"] / 1024 * pr["lambda per GB-second"] * 1e6     # $ per million
        fee = pr["lambda per million requests"]
        per_m = s["per_request"] * 1e6
        assert abs(compute + fee - per_m) < 1e-6
        busy = pr["m5.large per hour"] / (PER_SERVER_RPS * 3600) * 1e6                   # $ per million, full
        ratio = per_m / busy
        util = s["breakeven_rps"] / PER_SERVER_RPS
        assert abs(util - 1 / ratio) < 1e-9
        head = label(r"Paying by the millisecond", font_size=36).to_edge(UP, buff=0.3)
        x0, w = -4.2, 10.6
        y_srv, y_fn = 2.2, 1.45
        names = VGroup(label(r"a server", font_size=19, color=DATA).move_to([-5.5, y_srv, 0]),
                       label(r"a function", font_size=19, color=HEAD).move_to([-5.5, y_fn, 0]))
        srv = Rectangle(width=w, height=0.38, stroke_width=0, fill_color=DATA, fill_opacity=0.55).move_to(
            [x0 + w / 2, y_srv, 0])
        rng = random.Random(3)
        ts = sorted(rng.uniform(0, 1) for _ in range(40))
        slivers = VGroup(*[Rectangle(width=0.05, height=0.38, stroke_width=0, fill_color=HEAD, fill_opacity=0.95)
                           .move_to([x0 + t * w, y_fn, 0]) for t in ts])
        base = Line([x0, y_fn - 0.25, 0], [x0 + w, y_fn - 0.25, 0], color=GREY_D, stroke_width=1)
        tcap = label(r"one hour of sparse traffic \ (illustrative): \ billed always, \ against billed only while "
                     r"running", font_size=16, color=GREY_B).next_to(base, DOWN, buff=0.12)
        scale = 6.4 / per_m
        bx = -2.6
        y1, y2 = -0.3, -1.5
        b_comp = Rectangle(width=compute * scale, height=0.6, stroke_width=0, fill_color=HEAD, fill_opacity=0.85)
        b_comp.move_to([bx + compute * scale / 2, y1, 0])
        b_fee = Rectangle(width=fee * scale, height=0.6, stroke_width=0, fill_color=LAM, fill_opacity=0.85)
        b_fee.next_to(b_comp, RIGHT, buff=0)
        b_busy = Rectangle(width=busy * scale, height=0.6, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
        b_busy.move_to([bx + busy * scale / 2, y2, 0])
        n1 = label(r"a function", font_size=19, color=HEAD).next_to([bx, y1, 0], LEFT, buff=0.2)
        n2 = label(r"a busy server", font_size=19, color=DATA).next_to([bx, y2, 0], LEFT, buff=0.2)
        v1 = label(rf"\${per_m:.2f}", font_size=20, color=HEAD).next_to(b_fee, RIGHT, buff=0.15)
        v2 = label(rf"\${busy:.2f}", font_size=20, color=DATA).next_to(b_busy, RIGHT, buff=0.15)
        parts = VGroup(label(rf"compute \ \${compute:.2f}", font_size=16, color=HEAD),
                       label(rf"requests \ \${fee:.2f}", font_size=16, color=LAM))
        parts[0].next_to(b_comp, DOWN, buff=0.08)
        parts[1].next_to(b_fee, DOWN, buff=0.08).align_to(b_fee, LEFT)
        ucap = label(rf"dollars per million requests: \ {s['ms']} ms at {s['mb']} MB, \ against one m5.large "
                     rf"serving {PER_SERVER_RPS} requests every second", font_size=17, color=GREY_B).next_to(
            VGroup(n1, b_fee), UP, buff=0.25).set_x(0)
        lines = VGroup(
            wrapped_label(rf"a function costs {ratio:.1f} times as much per request as a fully busy server, \ so it "
                          rf"wins while the server would be busy less than {100 * util:.0f}\% of the time: \ below "
                          rf"{s['breakeven_rps']:.1f} of its {PER_SERVER_RPS} requests a second \ (chapter 12 plots "
                          r"it)", 12.4, font_size=19, color=YES),
            label(rf"{pr['date']}", font_size=16, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "What does the per-millisecond bill buy? <bookmark mark='a'/> A server is billed for every "
            "second it exists, busy or idle. A function is billed only while it runs. <bookmark mark='b'/> At "
            "Amazon's 2024 list prices, a hundred milliseconds at half a gigabyte costs eighty-three cents per "
            "million calls in compute, plus twenty cents per million in request fees. <bookmark mark='c'/> Now keep "
            "a small server completely busy, two hundred requests every second. Its hourly price is spread over "
            "seven hundred and twenty thousand requests: about thirteen cents per million. "
            "<bookmark mark='d'/> So a function costs nearly eight times as much per request as a busy server. It "
            "wins whenever the server would be idle more than about eighty-seven percent of the time, below about twenty-six "
            "requests a second, the break-even chapter twelve plots. Serverless is a bet on low "
            "utilization."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names), Create(base))
            vo.wait_until("a")
            self.play(GrowFromEdge(srv, LEFT), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(sl) for sl in slivers], lag_ratio=0.05), FadeIn(tcap), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(ucap), FadeIn(n1), GrowFromEdge(b_comp, LEFT), FadeIn(parts[0]))
            self.play(GrowFromEdge(b_fee, LEFT), FadeIn(parts[1]), FadeIn(v1))
            vo.wait_until("c")
            self.play(FadeIn(n2), GrowFromEdge(b_busy, LEFT), FadeIn(v2))
            vo.wait_until("d")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def cold(self):
        head = label(r"Cold starts", font_size=36).to_edge(UP, buff=0.3)
        arrivals = [2, 4, 6, 13, 15, 24, 26, 28, 39, 47, 49, 58]      # minutes into an hour (illustrative)
        x0, w = -3.6, 10.0

        def px(t):
            return x0 + t / 60 * w

        def row(keep, y, title):
            g = VGroup()
            g.add(Line([px(0), y, 0], [px(60), y, 0], color=GREY_C, stroke_width=1.5))
            colds, warm_min = 0, 0.0
            for i, t in enumerate(arrivals):
                cold = i == 0 or t - arrivals[i - 1] > keep
                colds += cold
                end = min(t + keep, arrivals[i + 1] if i + 1 < len(arrivals) else 60, 60)
                warm_min += end - t
                g.add(Rectangle(width=px(end) - px(t), height=0.3, stroke_width=0, fill_color=KERN,
                                fill_opacity=0.3).move_to([(px(t) + px(end)) / 2, y, 0]))
                g.add(Dot([px(t), y, 0], radius=0.075, color=NO if cold else YES))
            name = label(title, font_size=19, color=WHITE).next_to([px(0), y, 0], LEFT, buff=0.3)
            stat = label(rf"cold starts: \ {colds} of {len(arrivals)}; \ kept warm \ {warm_min:.0f} of 60 "
                         r"minutes", font_size=17, color=GREY_A).next_to([px(30), y, 0], DOWN, buff=0.28)
            return VGroup(name, g, stat), colds
        r1, c1 = row(3, 2.1, r"keep alive 3 min")
        r2, c2 = row(10, 0.85, r"keep alive 10 min")
        assert (c1, c2) == (6, 2)
        legend = VGroup(*[VGroup(Dot(radius=0.08, color=c), label(t, font_size=16, color=c)).arrange(RIGHT, buff=0.1)
                          for t, c in ((r"warm", YES), (r"cold", NO), (r"instance idle, \ memory held", KERN))])
        legend.arrange(RIGHT, buff=0.4).next_to(r2, DOWN, buff=0.25)
        ill = label(r"(illustrative)", font_size=16, color=GREY_B).next_to(legend, RIGHT, buff=0.4)

        def seg(t, wd, col):
            r = Rectangle(width=wd, height=0.34, stroke_width=0, fill_color=col, fill_opacity=0.85)
            tt = label(t, font_size=16, color=BLACK)
            if tt.width > wd - 0.08:
                tt.width = wd - 0.08
            return VGroup(r, tt.move_to(r))
        warm_bar = VGroup(seg(r"run", 1.2, YES))
        cold_bar = VGroup(seg(r"boot microVM", 2.2, NO), seg(r"start runtime", 2.2, KERN),
                          seg(r"init: \ load libraries", 2.8, LAM), seg(r"run", 1.2, YES)).arrange(RIGHT, buff=0)
        y_w, y_c = -0.95, -1.5
        cold_bar.move_to([0, y_c, 0]).align_to([-3.0, 0, 0], LEFT)
        warm_bar.move_to([0, y_w, 0]).align_to(cold_bar, LEFT)
        an = VGroup(label(r"a warm request", font_size=18, color=YES).next_to(warm_bar, LEFT, buff=0.25)
                    .align_to([-3.25, 0, 0], RIGHT),
                    label(r"a cold one", font_size=18, color=NO).next_to(cold_bar, LEFT, buff=0.25)
                    .align_to([-3.25, 0, 0], RIGHT))
        lines = VGroup(
            wrapped_label(r"invocation rates differ across applications by many orders of magnitude, \ so no single "
                          r"keep-alive suits all; \ Shahrad et al. \ (Azure Functions, \ 2020) \ learn each "
                          r"application's idle times", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"users fight back: \ pay to keep instances warm, \ or restore from snapshots", 12.4,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The catch is the first request. <bookmark mark='a'/> When an event arrives and no instance is warm, "
            "the platform must start one: boot a micro-VM, as in chapter two, start the language runtime, and run "
            "the function's own initialization, loading its libraries. That is a cold start, and it can take far "
            "longer than the request itself. <bookmark mark='b'/> So platforms keep an instance alive for a while "
            "after each request. With a short keep-alive, six of these twelve requests start cold. "
            "<bookmark mark='c'/> With a longer one, only two do, but memory sits reserved and idle almost all "
            "hour, and somebody pays for it. <bookmark mark='d'/> Shahrad and colleagues, studying Azure Functions "
            "in 2020, found that invocation rates differ between applications by many orders of magnitude, so no "
            "single timeout suits them all; their policy learns each application's typical idle times. Users "
            "fight back, paying to keep instances warm, or restoring them from snapshots."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(an[0]), FadeIn(warm_bar))
            self.play(FadeIn(an[1]), LaggedStart(*[FadeIn(sg, shift=RIGHT * 0.1) for sg in cold_bar],
                                                  lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(r1[0]), Create(r1[1]), FadeIn(legend), FadeIn(ill), run_time=2)
            self.play(FadeIn(r1[2]))
            vo.wait_until("c")
            self.play(FadeIn(r2[0]), Create(r2[1]), run_time=2)
            self.play(FadeIn(r2[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def concurrency(self):
        s = load("serverless")
        dur = s["ms"] / 1000
        rate = s["breakeven_rps"]
        rps = {r["rps"]: r for r in s["rows"]}
        head = label(r"Concurrency and its limits", font_size=36).to_edge(UP, buff=0.3)
        # one second of arrivals at the break-even rate (illustrative draw), each holding an instance for dur
        rng = random.Random(1)
        t, starts = 0.0, []
        while True:
            t += rng.expovariate(rate)
            if t > 1 - dur:
                break
            starts.append(t)
        lanes_free, bars = [], []
        for st in starts:
            k = next((i for i, f in enumerate(lanes_free) if f <= st), None)
            if k is None:
                lanes_free.append(0.0)
                k = len(lanes_free) - 1
            lanes_free[k] = st + dur
            bars.append((st, k))
        x0, w, y0, lh = -6.2, 6.8, -1.55, 0.4
        chart = VGroup(*[Rectangle(width=dur * w - 0.02, height=lh - 0.06, stroke_width=0, fill_color=KERN,
                                   fill_opacity=0.85).move_to([x0 + (st + dur / 2) * w, y0 + (k + 0.5) * lh, 0])
                         for st, k in bars])
        ax = VGroup(Line([x0, y0, 0], [x0 + w, y0, 0], color=GREY_C),
                    label(r"0 s", font_size=16, color=GREY_B).move_to([x0, y0 - 0.22, 0]),
                    label(r"1 s", font_size=16, color=GREY_B).move_to([x0 + w, y0 - 0.22, 0]),
                    label(rf"each bar: \ one request holding an instance for {s['ms']} ms; \ one row per instance",
                          font_size=16, color=GREY_B).move_to([x0 + w / 2, y0 - 0.55, 0]))
        cap = label(rf"one second at {rate:.1f} requests a second \ (a random draw)", font_size=17,
                    color=GREY_A).next_to([x0 + w / 2, y0 + len(lanes_free) * lh, 0], UP, buff=0.2)
        law = MathTex(r"L = \lambda W", font_size=38, color=HEAD)
        law_n = label(r"in flight $=$ arrival rate $\times$ time in the system \ (Little, \ Part 31)",
                      font_size=18, color=HEAD)
        rows = [[f"{rate:.1f}", f"{rate * dur:.1f}"],
                [f"{rps[100]['rps']:,}", f"{rps[100]['rps'] * dur:.0f}"],
                [f"{rps[1000]['rps']:,}".replace(",", "{,}"), f"{rps[1000]['rps'] * dur:.0f}"],
                [f"{1000 / dur:,.0f}".replace(",", "{,}"), r"1{,}000: \ the default cap"]]
        tab = grid_table([r"requests a second", r"instances in flight"], rows, widths=[2.6, 3.2], row_h=0.42,
                         font_size=19, mono_cols=())
        for c in tab.cells[-1]:
            c.set_color(NO)
        right = VGroup(VGroup(law, law_n).arrange(DOWN, buff=0.15), tab).arrange(DOWN, buff=0.4)
        right.move_to([3.6, 0.9, 0])
        lines = VGroup(
            wrapped_label(r"AWS's default: \ 1{,}000 concurrent executions per account in each region; \ beyond it, "
                          r"requests are throttled for the caller to retry; \ a function runs at most 15 minutes",
                          12.4, font_size=19, color=WHITE),
            wrapped_label(r"the limit that bites first is often behind the function: \ a thousand instances, \ "
                          r"each with its own connection, \ swamp a database \ (Part 43)", 12.4, font_size=19,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How many instances does a function need? <bookmark mark='a'/> Part 31's law of John Little answers: "
            "the number in flight is the arrival rate times the time each request spends. "
            "<bookmark mark='b'/> At the break-even rate of about twenty-six requests a second, each lasting a "
            "tenth of a second, that is between two and three instances on average, and more in a burst. "
            "<bookmark mark='c'/> At a thousand requests a second it is a hundred. <bookmark mark='d'/> Platforms "
            "cap this. Amazon's default is a thousand concurrent executions per account in each region, so a "
            "hundred-millisecond function tops out near ten thousand requests a second, and requests beyond the cap "
            "are throttled, refused for the caller to retry. An invocation runs fifteen minutes at most. "
            "<bookmark mark='e'/> And the limit that bites first is often behind the function: a thousand "
            "instances, each with its own connection, can swamp a database that expected a few dozen."
        ) as vo:
            self.play(FadeIn(head), Create(ax[0]), FadeIn(ax[1:]))
            vo.wait_until("a")
            self.play(Write(law), FadeIn(law_n))
            vo.wait_until("b")
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in chart], lag_ratio=0.08),
                      run_time=2.5)
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[2])), FadeIn(VGroup(*tab.cells[3])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[4])), FadeIn(lines[0]))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, math)
