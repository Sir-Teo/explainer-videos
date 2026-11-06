from __future__ import annotations

import inspect

from explainer.cs import *  # noqa: F403
from explainer.cs.design import blocks as B
from videos.cs.cs48.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, code_block, load, module_box)

# the limiter experiment's parameters (blocks.limiter_experiment's defaults; its bucket holds 20 tokens)
LP = {k: v.default for k, v in inspect.signature(B.limiter_experiment).parameters.items()}
BURST = 20
RATE = LP["limit"] / LP["window"]          # tokens a second


class Limits(VoiceoverScene):
    def construct(self):
        self.card()
        self.bucket()
        self.envelope()
        self.gcra()
        self.windows()
        self.distributed()

    def card(self):
        card = chapter_card(5, r"Rate limiting", r"How does a service say no, \ fairly and cheaply?",
                            lit=(1991, 2017), extra=((1991, r"Cruz: \ $(\sigma, \rho)$ envelopes"),
                                                     (2017, r"Cloudflare's sliding windows")), part=PART)
        with self.voiceover("Chapter five. Rate limiting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def bucket(self):
        lim = load("limiter")
        head = label(r"A bucket of tokens", font_size=36).to_edge(UP, buff=0.3)
        W, H = 1.5, 2.8
        cx, by = -3.3, -1.6                      # the bucket's centre x and its floor
        walls = VMobject(color=GREY_A, stroke_width=3).set_points_as_corners(
            [[cx - W / 2, by + H, 0], [cx - W / 2, by, 0], [cx + W / 2, by, 0], [cx + W / 2, by + H, 0]])
        level = ValueTracker(BURST)
        fill = always_redraw(lambda: Rectangle(
            width=W - 0.08, height=max(0.001, (H - 0.1) * level.get_value() / BURST), stroke_width=0,
            fill_color=YES, fill_opacity=0.55).align_to([cx, by + 0.04, 0], DOWN).set_x(cx))
        count = always_redraw(lambda: label(rf"{level.get_value():.0f} tokens", font_size=19, color=YES).next_to(
            walls, DOWN, buff=0.15))
        tap = VGroup(Arrow([cx, by + H + 0.9, 0], [cx, by + H + 0.1, 0], buff=0, color=YES, stroke_width=3),
                     label(rf"$\rho$: \ {LP['limit']} a minute", font_size=18, color=YES))
        tap[1].next_to(tap[0], RIGHT, buff=0.15)
        cap = label(rf"$\sigma = {BURST}$", font_size=19, color=HEAD).next_to(walls, LEFT, buff=0.15).align_to(
            walls, UP)
        server = module_box(r"service", KERN, w=1.5, h=0.6, font=18).move_to([-0.6, by + 0.6, 0])
        srcs = [-6.3, by + 0.6, 0]
        src = label(r"requests", font_size=18, color=DATA).move_to([-6.1, by + 1.15, 0])
        ok = [Dot(srcs, radius=0.07, color=DATA) for _ in range(BURST)]
        bad = [Dot(srcs, radius=0.07, color=DATA) for _ in range(5)]
        code = code_block([
            "tokens = min(burst, tokens + (t - last) * rate)",
            "last = t",
            "if tokens >= 1:",
            "    tokens -= 1        # allow",
            "else:",
            "    refuse             # 429",
        ], size=15).move_to([3.7, 1.3, 0])
        notes = VGroup(
            wrapped_label(r"tokens drip in at rate $\rho$ up to a depth $\sigma$; \ a request spends one, \ or is "
                          r"refused", 5.6, font_size=19, color=WHITE),
            wrapped_label(r"a burst of up to $\sigma$ passes at once; \ after that, \ only the rate", 5.6,
                          font_size=19, color=HEAD),
            wrapped_label(rf"our bursty trace: \ {lim['requests']:,} requests in {LP['horizon']:.0f} s; \ "
                          rf"{lim['bucket_allowed']} admitted", 5.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(code, DOWN, buff=0.45).align_to(code, LEFT)
        with self.voiceover(
            "A rate limiter protects a service from callers who send too much. "
            "<bookmark mark='a'/> The commonest is the token bucket. Tokens drip into a bucket at a steady rate, "
            "rho, up to a depth, sigma. Each request takes a token, or, if the bucket is empty, is refused, with "
            "Part 43's status code four hundred and twenty-nine. <bookmark mark='b'/> A burst passes at once, up to "
            "sigma requests, here twenty. <bookmark mark='c'/> Then the bucket is dry, and only the rate gets "
            "through, a hundred a minute. <bookmark mark='d'/> On our bursty test traffic, one thousand and "
            "eighty-eight requests in ten minutes, it admitted seven hundred and sixty-six."
        ) as vo:
            self.play(FadeIn(head), Create(walls), FadeIn(fill), FadeIn(count), FadeIn(cap), FadeIn(server),
                      FadeIn(src), FadeIn(code))
            vo.wait_until("a")
            self.play(GrowArrow(tap[0]), FadeIn(tap[1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.add(*ok)
            self.play(LaggedStart(*[Succession(d.animate(run_time=0.5).move_to([cx, by + 0.6, 0]),
                                               d.animate(run_time=0.5).set_color(YES).move_to(server))
                                    for d in ok], lag_ratio=0.12),
                      level.animate(rate_func=linear).set_value(0), FadeIn(notes[1]), run_time=3.5)
            self.remove(*ok)
            vo.wait_until("c")
            self.add(*bad)
            self.play(LaggedStart(*[Succession(d.animate(run_time=0.5).move_to([cx - W / 2 - 0.25, by + 0.6, 0]),
                                               d.animate(run_time=0.5).set_color(NO).shift(DOWN * 0.9))
                                    for d in bad], lag_ratio=0.25), run_time=2.5)
            self.play(*[FadeOut(d) for d in bad], level.animate(rate_func=linear).set_value(4), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def envelope(self):
        lim = load("limiter")
        head = label(r"A token bucket is an envelope", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"over any interval of length $s$:", font_size=22, color=WHITE),
            MathTex(r"\text{tokens at the start} \le \sigma", font_size=30, color=DATA),
            MathTex(r"\text{tokens added} \le \rho\, s", font_size=30, color=DATA),
            MathTex(r"\text{each admission spends one}", font_size=30, color=DATA),
            MathTex(r"A(t, t + s) \;\le\; \sigma + \rho\, s", font_size=36, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.55).shift(UP * 0.6)
        g = axes([0, 30, 10], [0, 80, 20], x_length=5.4, y_length=3.3, x_label=r"interval length $s$, \ seconds",
                 y_label=r"requests admitted", xticks=[0, 10, 20, 30], yticks=[0, 20, 40, 60, 80], font=16)
        g.to_edge(RIGHT, buff=0.5).shift(UP * 0.55)
        ax = g.ax
        env = Line(ax.c2p(0, BURST), ax.c2p(30, BURST + RATE * 30), color=HEAD, stroke_width=3)
        env_l = label(r"$\sigma + \rho s$", font_size=20, color=HEAD).next_to(env.get_end(), UP, buff=0.1).shift(
            LEFT * 0.4)
        # the greediest admitted sender: sigma at once, then one each 1/rho (the envelope's own staircase)
        pts, n, t = [ax.c2p(0, 0), ax.c2p(0, BURST)], BURST, 0.0
        while t + 1 / RATE <= 30:
            t += 1 / RATE
            pts += [ax.c2p(t, n), ax.c2p(t, n + 1)]
            n += 1
        pts.append(ax.c2p(30, n))
        stair = VMobject(color=YES, stroke_width=2.5).set_points_as_corners(pts)
        stair_l = label(r"the greediest sender allowed", font_size=17, color=YES).next_to(ax.c2p(15, 25), DOWN,
                                                                                         buff=0.1)
        lines = VGroup(
            wrapped_label(rf"checked on every interval up to 10 s of our {lim['bucket_allowed']} admitted requests: "
                          rf"\ {'none above the line' if lim['bucket_envelope_ok'] else 'violations found'}", 12.4,
                          font_size=20, color=YES),
            wrapped_label(r"Rene Cruz \ (1991): \ envelopes add, \ so a service fed by limited clients has a "
                          r"worst-case load it can be sized for; \ a \textbf{leaky bucket} instead queues the excess "
                          r"and drains it at $\rho$: \ it shapes, \ where the token bucket polices", 12.4,
                          font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The token bucket is also a guarantee. <bookmark mark='a'/> Take any interval "
            "of length s. At its start the bucket holds at most sigma tokens; during it, at most rho times s more "
            "arrive; and every admitted request spends one. <bookmark mark='b'/> So the number admitted in any "
            "interval is at most sigma plus rho s, a straight line, which the greediest allowed sender follows. "
            " <bookmark mark='c'/> We checked every interval of up to "
            "ten seconds in our trace: none crosses the line. <bookmark mark='d'/> Rene Cruz built network "
            "calculus on such envelopes in 1991. Envelopes add, so a service fed by limited clients has a worst "
            "case it can be sized for. A leaky bucket instead queues the excess and drains it steadily: it smooths, "
            "where the token bucket refuses."
        ) as vo:
            self.play(FadeIn(head), Create(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps[:4]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(steps[4]), Create(env), FadeIn(env_l))
            self.play(Create(stair), FadeIn(stair_l), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def gcra(self):
        head = label(r"The same bucket in one number", font_size=36).to_edge(UP, buff=0.3)
        code = code_block([
            "T   = 1 / rate               # spacing",
            "tau = (burst - 1) * T        # tolerance",
            "",
            "def allow(now):",
            "    if now < tat - tau:",
            "        return False         # too early",
            "    tat = max(tat, now) + T",
            "    return True",
        ], size=17).to_edge(LEFT, buff=0.6).shift(UP * 0.7)
        # a timeline: the theoretical arrival time running ahead of the clock during a burst
        x0, x1, y = 0.6, 6.4, 1.2
        line = Line([x0, y, 0], [x1, y, 0], color=GREY_C, stroke_width=2)
        now = VGroup(Line([x0 + 1.0, y - 0.25, 0], [x0 + 1.0, y + 0.25, 0], color=DATA, stroke_width=3),
                     label(r"now", font_size=17, color=DATA).move_to([x0 + 1.0, y - 0.5, 0]))
        tat = Triangle(color=HEAD, fill_opacity=1).scale(0.1).rotate(PI).move_to([x0 + 1.0, y + 0.4, 0])
        tat_l = label(r"TAT", font_size=17, color=HEAD).next_to(tat, UP, buff=0.08)
        tol = Rectangle(width=3.2, height=0.18, stroke_width=0, fill_color=YES, fill_opacity=0.35).move_to(
            [x0 + 1.0 + 1.6, y, 0])
        tol_l = label(r"tolerance $\tau$", font_size=17, color=YES).next_to(tol, DOWN, buff=0.12).shift(RIGHT * 0.6)
        notes = VGroup(
            wrapped_label(r"the \textbf{generic cell rate algorithm}, \ from ATM networks: \ keep only the "
                          r"\textit{theoretical arrival time} of the next request", 5.6, font_size=19, color=WHITE),
            wrapped_label(r"each admission pushes it $T$ ahead; \ refuse once it runs more than $\tau$ ahead of "
                          r"the clock", 5.6, font_size=19, color=HEAD),
            wrapped_label(r"with $\tau = (\sigma - 1)T$ it admits exactly what the token bucket admits: \ one "
                          r"timestamp per key, \ no refill to compute", 5.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.5, -1.3, 0])
        with self.voiceover(
            "A token bucket stores two numbers per caller. "
            "<bookmark mark='a'/> The generic cell rate algorithm, from ATM networks, stores one: the theoretical "
            "arrival time of the next request. <bookmark mark='b'/> Each admitted request "
            "pushes it one spacing, T, further ahead. Once it runs more than a tolerance tau ahead of the clock, "
            "requests are refused until the clock catches up. <bookmark mark='c'/> With tau "
            "equal to sigma minus one spacings, it admits exactly what the token bucket admits, with a single "
            "timestamp per key in a shared store."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), Create(line), FadeIn(now))
            vo.wait_until("a")
            self.play(FadeIn(tat), FadeIn(tat_l), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(tol), FadeIn(tol_l), FadeIn(notes[1]))
            for _ in range(5):
                self.play(VGroup(tat, tat_l).animate.shift(RIGHT * 0.75), run_time=0.45)
            self.play(Indicate(tat, color=NO), VGroup(tat, tat_l).animate.set_color(NO))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def windows(self):
        lim = load("limiter")
        head = label(r"Counting in windows", font_size=36).to_edge(UP, buff=0.3)
        L = lim["limit"]
        base = -0.2

        def tl(xa, xb):
            k = (xb - xa) / 120.0
            return (lambda t: xa + t * k), k
        # fixed windows: a burst either side of the boundary
        fx, fk = tl(-6.5, -0.6)
        f_axis = Line([fx(0), base, 0], [fx(120), base, 0], color=GREY_C, stroke_width=2)
        f_ticks = VGroup(*[Line([fx(t), base - 0.12, 0], [fx(t), base + 2.0, 0], color=GREY_D, stroke_width=1.5)
                           for t in (0, 60, 120)])
        f_names = VGroup(label(r"window 1", font_size=16, color=GREY_B).move_to([fx(30), base - 0.3, 0]),
                         label(r"window 2", font_size=16, color=GREY_B).move_to([fx(90), base - 0.3, 0]))
        bursts = VGroup()
        for a in (50, 60):
            r = Rectangle(width=10 * fk, height=1.2, stroke_width=0, fill_color=NO, fill_opacity=0.8)
            r.move_to([fx(a + 5), base + 0.6, 0])
            bursts.add(r)
        bursts.add(label(rf"{L} + {L}", font_size=16, color=NO).next_to(bursts, UP, buff=0.06))
        span = BraceBetweenPoints([fx(30), base + 2.1, 0], [fx(90), base + 2.1, 0], direction=UP, color=HEAD)
        span_l = label(rf"one minute, \ {2 * L} admitted", font_size=17, color=HEAD).next_to(span, UP, buff=0.06)
        f_title = label(r"fixed windows", font_size=21, color=NO).move_to([fx(60), base + 3.1, 0])
        f_notes = VGroup(
            wrapped_label(rf"a counter per window; \ a limit of {L} lets up to {2 * L} through across a boundary",
                          5.8, font_size=19, color=WHITE),
            wrapped_label(rf"our trace: \ the worst minute admitted {lim['fixed_worst_window']}", 5.8, font_size=19,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(f_names, DOWN, buff=0.35).align_to(f_axis, LEFT)
        # the sliding-window counter: weight the previous window by its overlap
        sx, sk = tl(0.6, 6.5)
        s_axis = Line([sx(0), base, 0], [sx(120), base, 0], color=GREY_C, stroke_width=2)
        s_ticks = VGroup(*[Line([sx(t), base - 0.12, 0], [sx(t), base + 2.0, 0], color=GREY_D, stroke_width=1.5)
                           for t in (0, 60, 120)])
        prev = Rectangle(width=60 * sk, height=1.2, stroke_width=0, fill_color=LAM, fill_opacity=0.45).move_to(
            [sx(30), base + 0.6, 0])
        cur = Rectangle(width=24 * sk, height=0.75, stroke_width=0, fill_color=DATA, fill_opacity=0.6).move_to(
            [sx(72), base + 0.375, 0])
        prev_l = label(r"previous: \ 80", font_size=16, color=LAM).move_to([sx(30), base - 0.3, 0])
        cur_l = label(r"current: \ 30", font_size=16, color=DATA).move_to([sx(78), base - 0.3, 0])
        win = Rectangle(width=60 * sk, height=1.7, stroke_color=HEAD, stroke_width=2.5, fill_opacity=0).move_to(
            [sx(54), base + 0.85, 0])
        win_l = label(r"the last minute", font_size=16, color=HEAD).next_to(win, UP, buff=0.06)
        s_title = label(r"sliding-window counter", font_size=21, color=YES).move_to([sx(60), base + 3.1, 0])
        formula = MathTex(r"\hat n = \text{prev}\,(1 - f) + \text{cur} = 80 \times 0.6 + 30 = 78", font_size=26,
                          color=HEAD)
        s_notes = VGroup(
            formula,
            wrapped_label(r"$f$: \ the fraction of the current window elapsed; \ two counters per key, \ assuming "
                          r"the previous window's requests were spread evenly", 5.8, font_size=19, color=WHITE),
            wrapped_label(rf"against an exact sliding log, \ on our bursty trace: \ mean error "
                          rf"{100 * lim['sliding_mean_rel_error']:.0f}\%, \ "
                          rf"worst {100 * lim['sliding_max_rel_error']:.0f}\%", 5.8, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(prev_l, DOWN, buff=0.35).align_to(s_axis, LEFT)
        foot = note(r"bursts and counts in the diagrams illustrative; \ errors and the worst minute computed",
                    font_size=16).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Many limiters count instead. <bookmark mark='a'/> The simplest keeps one counter per minute and "
            "refuses requests once it reaches the limit. But a burst at the end of one "
            "window and another at the start of the next both pass: twice the limit in a single minute. "
            "<bookmark mark='b'/> On our trace, with a limit of one hundred, the worst minute admitted one hundred "
            "and thirty-eight. <bookmark mark='c'/> A sliding log, keeping every timestamp, is exact but costly. The "
            "sliding-window counter keeps two numbers: it weights the previous window's count by how much of it the "
            "last minute still covers. <bookmark mark='d'/> That assumes the previous window was evenly spread, and "
            "bursts are not: against the exact count, our trace's mean error is fifteen percent, and the worst above "
            "a hundred percent. On real traffic it does far better: in 2017 Cloudflare reported only three "
            "wrong decisions in a hundred thousand requests."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(f_title), Create(f_axis), FadeIn(f_ticks), FadeIn(f_names), FadeIn(f_notes[0]))
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bursts], lag_ratio=0.4))
            self.play(GrowFromCenter(span), FadeIn(span_l))
            vo.wait_until("b")
            self.play(FadeIn(f_notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(s_title), Create(s_axis), FadeIn(s_ticks), FadeIn(prev), FadeIn(cur), FadeIn(prev_l),
                      FadeIn(cur_l))
            self.play(Create(win), FadeIn(win_l), FadeIn(s_notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(s_notes[1]), FadeIn(s_notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def distributed(self):
        head = label(r"One limit, \ many servers", font_size=36).to_edge(UP, buff=0.3)
        lb = module_box(r"load balancer", HEAD, w=2.6, h=0.55, font=18).move_to([-2.6, 2.3, 0])
        servers = VGroup(*[module_box(rf"server {i + 1}", KERN, w=1.5, h=0.55, font=17) for i in range(4)]).arrange(
            RIGHT, buff=0.35).move_to([-2.6, 0.9, 0])
        buckets = VGroup(*[VGroup(Rectangle(width=0.5, height=0.5, stroke_color=YES, stroke_width=2),
                                  Rectangle(width=0.44, height=0.25, stroke_width=0, fill_color=YES,
                                            fill_opacity=0.5)).next_to(s, DOWN, buff=0.15) for s in servers])
        for b in buckets:
            b[1].align_to(b[0], DOWN).shift(UP * 0.03)
        store = module_box(r"shared counters", LAM, w=3.0, h=0.6, font=18).move_to([-2.6, -1.4, 0])
        down = VGroup(*[Arrow(lb.get_bottom(), s.get_top(), buff=0.08, stroke_width=1.8, color=GREY_B,
                              max_tip_length_to_length_ratio=0.15) for s in servers])
        sync = VGroup(*[DashedLine(b.get_bottom(), store.get_top(), color=LAM, stroke_width=1.6) for b in buckets])
        opts = VGroup(
            wrapped_label(r"\textbf{central}: \ an atomic increment in a shared store per request; \ exact, \ but a "
                          r"round trip each time, \ and the store must stay up", 5.4, font_size=19, color=LAM),
            wrapped_label(r"\textbf{local}: \ each of $N$ servers enforces $\rho/N$; \ free, \ but unfair when the "
                          r"balancer spreads one caller unevenly", 5.4, font_size=19, color=YES),
            wrapped_label(r"\textbf{approximate}: \ count locally, \ share every so often; \ the overshoot grows with "
                          r"the interval; \ for millions of keys, \ a Count-Min sketch \ (Part 20) \ errs only "
                          r"towards refusing", 5.4, font_size=19, color=HEAD),
            wrapped_label(r"either way, \ answer 429 with a \texttt{Retry-After} \ (Part 43), \ and clients back off",
                          5.4, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.9, 0.15, 0])
        foot = note(r"schematic", font_size=16).to_edge(DOWN, buff=0.3).set_x(-2.6)
        with self.voiceover(
            "A fleet needs one limit per caller across all its servers. <bookmark mark='a'/> The exact answer is a "
            "shared counter, an atomic increment in a store such as "
            "Redis on every request. It costs a round trip each time. "
            "<bookmark mark='b'/> The cheapest splits the limit: each of N servers enforces its share, with no "
            "coordination, but unfairly when one caller's traffic is spread unevenly. "
            "<bookmark mark='c'/> Between them, count locally and share the counts every so often, accepting an "
            "overshoot that grows with the interval. For millions of keys, Part 20's Count-Min sketch only "
            "overestimates, so it errs towards refusing. <bookmark mark='d'/> Whichever you choose, "
            "refuse politely, with a four twenty-nine and a hint of when to retry."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lb), FadeIn(servers), Create(down), FadeIn(buckets), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(store), Create(sync), FadeIn(opts[0]))
            for mk, o in zip("bcd", opts[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(o))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, axes)
