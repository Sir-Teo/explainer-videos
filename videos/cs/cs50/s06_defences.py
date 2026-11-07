from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, bar_chart, load, mono, trace


def node(text, col, w=2.3, h=0.85, size=21):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=col, stroke_width=2.4, fill_color=BG,
                         fill_opacity=1)
    return VGroup(r, label(text, font_size=size, color=col).move_to(r))


def series(v):
    return [(s + 0.5, x) for s, x in enumerate(v)]


def shade(ax, t0, t1, y1, col, op=0.12):
    a, b = ax.c2p(t0, 0), ax.c2p(t1, y1)
    return Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0, fill_color=col,
                     fill_opacity=op).move_to((a + b) / 2)


def fmt(v: float) -> str:
    return f"{v:,.0f}"


class Defences(VoiceoverScene):
    def construct(self):
        self.card()
        self.states()
        self.breaker()
        self.shedding()
        self.summary()
        self.bulkheads()
        self.degrade()

    def card(self):
        card = chapter_card(5, r"Breakers, bulkheads and load shedding", r"How should a service say no?",
                            lit=(2007, 2015), extra=((2007, r"Nygard: \ \textit{Release It!}"),
                                                     (2015, r"Maurer: \ Fail at Scale")), part=PART)
        with self.voiceover("Chapter five. Breakers, bulkheads, and the art of refusing work."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def states(self):
        head = label(r"A circuit breaker", font_size=36).to_edge(UP, buff=0.3)
        cl = node(r"closed", YES).move_to([-4.6, 1.0, 0])
        op = node(r"open", NO).move_to([-0.7, 1.0, 0])
        ho = node(r"half-open", HEAD).move_to([-2.65, -1.9, 0])
        a1 = Arrow(cl.get_right(), op.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5)
        a2 = Arrow(op.get_bottom() + LEFT * 0.55, ho.get_top() + RIGHT * 0.35, buff=0.08, color=GREY_B,
                   stroke_width=2.5)
        a3 = Arrow(ho.get_right() + UP * 0.05, op.get_bottom() + RIGHT * 0.45, buff=0.08, color=GREY_B,
                   stroke_width=2.5)
        a4 = Arrow(ho.get_left() + UP * 0.05, cl.get_bottom() + LEFT * 0.2, buff=0.08, color=GREY_B,
                   stroke_width=2.5)
        l1 = label(r"most calls failing", font_size=18, color=NO).next_to(a1, UP, buff=0.1)
        l2 = label(r"after a cool-down", font_size=17, color=GREY_A).next_to(a2.get_center(), LEFT, buff=0.15)
        l3 = label(r"a probe fails", font_size=17, color=NO).next_to(a3.get_center(), RIGHT, buff=0.15)
        l4 = label(r"probes succeed", font_size=17, color=YES).next_to(a4.get_center(), LEFT, buff=0.15)
        fsm = VGroup(cl, op, ho)
        arrows = VGroup(a1, a2, a3, a4)
        alabels = VGroup(l1, l2, l3, l4)
        notes = VGroup(
            wrapped_label(r"\textbf{closed}: \ calls pass; \ the breaker counts recent failures", 5.0,
                          font_size=19, color=YES),
            wrapped_label(r"\textbf{open}: \ calls fail at once, \ with no timeout to wait for and no load on the "
                          r"struggling dependency", 5.0, font_size=19, color=NO),
            wrapped_label(r"\textbf{half-open}: \ a few probe calls go through to test the water", 5.0,
                          font_size=19, color=HEAD),
            wrapped_label(r"ours, \ in simulation: \ opens for 5 s when over half of the last second's calls "
                          r"failed; \ while open, \ 5\% of calls still pass as probes", 5.0, font_size=18,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.15, -0.2, 0])
        token = Dot(cl.get_center() + LEFT * 0.88, radius=0.09, color=WHITE).set_z_index(3)
        with self.voiceover(
            "Michael Nygard's book Release It!, in 2007, borrowed a device from electricians. <bookmark "
            "mark='a'/> A circuit breaker sits in the client, in front of a dependency. Closed, it lets calls "
            "through and counts the failures. <bookmark mark='b'/> When most recent calls fail, it trips open: "
            "every call fails at once, with no timeout to wait for and no load added to a struggling dependency. "
            "<bookmark mark='c'/> After a cool-down it goes half-open and lets a few probe calls through. "
            "<bookmark mark='d'/> If they succeed, it closes again; if they fail, it opens again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fsm), *[GrowArrow(a) for a in arrows], FadeIn(alabels))
            vo.wait_until("a")
            self.play(cl[0].animate.set_fill(YES, 0.25), FadeIn(token), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(cl[0].animate.set_fill(BG, 1), op[0].animate.set_fill(NO, 0.25),
                      token.animate.move_to(op.get_center() + LEFT * 0.88), Indicate(l1, color=NO), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(op[0].animate.set_fill(BG, 1), ho[0].animate.set_fill(HEAD, 0.25),
                      token.animate.move_to(ho.get_center() + LEFT * 0.88), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(ho[0].animate.set_fill(BG, 1), cl[0].animate.set_fill(YES, 0.25),
                      token.animate.move_to(cl.get_center() + LEFT * 0.88), Indicate(l4, color=YES))
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def _chart(self, head):
        g = axes([0, 120, 20], [0, 400, 100], x_length=9.4, y_length=4.1, x_label=r"seconds",
                 xticks=range(0, 121, 20), yticks=(0, 100, 200, 300, 400), font=16)
        g.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.9)
        ax = g.ax
        ylab = label(r"requests a second", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        return g, ax, ylab

    def breaker(self):
        o = load("overload")
        rt, br = o["retries"], o["breaker"]
        t0, t1, frac = br["trigger"]
        cap = br["capacity"]
        late = sum(rt["offered"][60:]) / len(rt["offered"][60:])
        opened = [s for s, v in enumerate(br["breaker_open"]) if v]
        o0, o1 = opened[0], opened[-1] + 1
        head = label(r"A breaker against chapter three's trigger", font_size=36).to_edge(UP, buff=0.3)
        g, ax, ylab = self._chart(head)
        band = shade(ax, t0, t1, 400, NO)
        band_l = label(r"trigger", font_size=16, color=NO).next_to(band, UP, buff=0.05)
        oband = shade(ax, o0, o1, 400, KERN, op=0.22)
        oband_l = label(r"breakers open", font_size=16, color=KERN).move_to(ax.c2p(t1 + 1, 200), aligned_edge=LEFT)
        cap_pts = [(0, cap), (t0, cap), (t0, cap * frac), (t1, cap * frac), (t1, cap), (120, cap)]
        cap_line = DashedVMobject(trace(ax, cap_pts, WHITE, width=2), num_dashes=60)
        off_rt = trace(ax, series(rt["offered"]), NO, width=2.5)
        good_rt = trace(ax, series(rt["goodput"]), KERN, width=3)
        off_br = trace(ax, series(br["offered"]), DATA, width=2.5)
        good_br = trace(ax, series(br["goodput"]), YES, width=3)
        right = ax.get_right()[0] + 0.2
        k_rt = wrapped_label(rf"three immediate retries: \ about {late:.0f} sent a second, \ none answered in time",
                             2.5, font_size=17, color=NO).move_to([right, ax.c2p(0, 320)[1], 0], aligned_edge=LEFT)
        k_br = wrapped_label(rf"with a breaker in every client: \ open from {o0} s to {o1} s; \ answering at full "
                             r"rate as the trigger ends", 2.5, font_size=17, color=YES).move_to(
            [right, ax.c2p(0, 150)[1], 0], aligned_edge=LEFT)
        foot = label(rf"answered in time over the two minutes: \ {fmt(sum(br['goodput']))} with breakers, \ "
                     rf"{fmt(sum(rt['goodput']))} without", font_size=21, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is chapter three's server again, its clients retrying three times. <bookmark mark='a'/> Without "
            "a breaker, the retries hold it in the bad state for good. <bookmark mark='b'/> Now give every client "
            "a breaker. Two seconds into the trigger most calls are failing, the breakers open, and the load sent "
            "falls almost to nothing. <bookmark mark='c'/> The server drains its queue, the probes succeed, the "
            "breakers close, and the server is answering at full rate as the trigger ends. <bookmark mark='d'/> "
            "In all, nine thousand one hundred and ten answers in time, against two thousand five hundred and "
            "sixty-seven."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ylab), Create(cap_line), FadeIn(band), FadeIn(band_l))
            vo.wait_until("a")
            self.play(Create(off_rt), Create(good_rt), run_time=2.0)
            self.play(FadeIn(k_rt))
            vo.wait_until("b")
            self.play(off_rt.animate.set_stroke(opacity=0.3), good_rt.animate.set_stroke(opacity=0.3),
                      k_rt.animate.set_opacity(0.45), FadeIn(oband), FadeIn(oband_l))
            self.play(Create(off_br), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(good_br), run_time=2.0)
            self.play(FadeIn(k_br))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def shedding(self):
        sh = load("overload")["shed"]
        t0, t1, frac = sh["trigger"]
        cap = sh["capacity"]
        peak = max(sh["offered"])
        trig = sh["goodput"][int(t0) + 1:int(t1)]
        head = label(r"Load shedding: \ refuse early, \ not late", font_size=36).to_edge(UP, buff=0.3)
        g, ax, ylab = self._chart(head)
        band = shade(ax, t0, t1, 400, NO)
        band_l = label(r"trigger", font_size=16, color=NO).next_to(band, UP, buff=0.05)
        cap_pts = [(0, cap), (t0, cap), (t0, cap * frac), (t1, cap * frac), (t1, cap), (120, cap)]
        cap_line = DashedVMobject(trace(ax, cap_pts, WHITE, width=2), num_dashes=60)
        off = trace(ax, series(sh["offered"]), DATA, width=2.5)
        good = trace(ax, series(sh["goodput"]), YES, width=3)
        shed = trace(ax, series(sh["shed"]), NO, width=2.5)
        right = ax.get_right()[0] + 0.2
        k_off = wrapped_label(rf"sent, \ retries included: \ at most {peak:.0f} a second", 2.5, font_size=17,
                              color=DATA).move_to([right, ax.c2p(0, 300)[1], 0], aligned_edge=LEFT)
        k_shed = wrapped_label(r"dropped: \ waited over 0.5 s, \ so its client is about to give up", 2.5,
                               font_size=17, color=NO).move_to([right, ax.c2p(0, 185)[1], 0], aligned_edge=LEFT)
        k_good = wrapped_label(rf"answered in time: \ {min(trig):.0f} to {max(trig):.0f} a second through the "
                               r"trigger, \ then at once back to normal", 2.5, font_size=17, color=YES).move_to(
            [right, ax.c2p(0, 60)[1], 0], aligned_edge=LEFT)
        foot = wrapped_label(r"CoDel's idea \ (Part 37) \ moved to services: \ judge a queue by how long its "
                             r"requests have waited, \ not by its length; \ Maurer \ (2015) \ describes Facebook's "
                             r"servers doing this, \ and serving newest first when the queue is long", 12.4,
                             font_size=19, color=WHITE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The server can defend itself too. <bookmark mark='a'/> Before serving a request, it checks how long "
            "the request has waited, and drops it if that is over half a second, since its client is about to "
            "give up. A rejection costs a fiftieth of an answer. <bookmark mark='b'/> Through the trigger it "
            "sheds what it cannot serve in time, answers the rest at its reduced capacity, and afterwards "
            "recovers at once. <bookmark mark='c'/> This is CoDel's idea from Part 37, moved from routers to "
            "services: judge a queue by how long its requests have waited, not by its length. Ben Maurer "
            "described Facebook's servers doing this in 2015, switching to last in, first out when the queue is "
            "long, so that the newest requests are served first."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ylab), Create(cap_line), FadeIn(band), FadeIn(band_l))
            vo.wait_until("a")
            self.play(Create(off), run_time=2.0)
            self.play(FadeIn(k_off))
            vo.wait_until("b")
            self.play(Create(shed), Create(good), run_time=2.5)
            self.play(FadeIn(k_shed), FadeIn(k_good))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def summary(self):
        o = load("overload")
        pols = (("none", r"no retries", GREY_A), ("retries", r"three retries", NO), ("backoff", r"with backoff", KERN),
                ("budget", r"retry budget", HEAD), ("shed", r"shedding", YES), ("breaker", r"breakers", DATA))
        vals = [sum(o[p]["goodput"]) for p, _, _ in pols]
        head = label(r"Six policies, \ one trigger", font_size=36).to_edge(UP, buff=0.3)
        ch = bar_chart(vals, [n for _, n, _ in pols], [c for _, _, c in pols], height=3.0, bar_w=1.0, gap=0.85,
                       vmax=10000, fmt_=fmt, font_size=20)
        ch.next_to(head, DOWN, buff=0.75)
        rec = VGroup()
        for k, (p, _, c) in enumerate(pols):
            r = o[p]["recovered_s"]
            txt = r"never recovers" if r is None else (r"never stuck" if r == 0 else rf"recovers after {r:.0f} s")
            rec.add(label(txt, font_size=17, color=NO if r is None else (YES if r == 0 else GREY_A)).next_to(
                ch.names[k], DOWN, buff=0.15))
        base = o["none"]["base"]
        ycap = label(rf"answered in time in 120 s \ (users send {base:.0f} a second, \ about "
                     rf"{fmt(base * 120)} in all)", font_size=19, color=GREY_A).next_to(ch, UP, buff=0.2)
        foot = wrapped_label(r"what works reduces the load, \ at the server or at the client; \ in practice budgets, "
                             r"breakers and shedding are used together", 12.4, font_size=20, color=WHITE).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Put the six side by side. <bookmark mark='a'/> Users sent eighty requests a second for two minutes. "
            "Immediate retries, with or without backoff, answered just over a quarter of them; the retry budget "
            "recovered after nineteen seconds, and no retries at all after eleven. <bookmark mark='b'/> Shedding "
            "and the breakers never got stuck. <bookmark mark='c'/> What works is reducing the load, at the "
            "server or at the client, and real systems combine all three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ycap), FadeIn(ch[0]), FadeIn(ch.names))
            vo.wait_until("a")
            for k in range(4):
                self.play(GrowFromEdge(ch.bars[k], DOWN), FadeIn(ch.vals[k]), FadeIn(rec[k]), run_time=0.7)
            vo.wait_until("b")
            for k in range(4, 6):
                self.play(GrowFromEdge(ch.bars[k], DOWN), FadeIn(ch.vals[k]), FadeIn(rec[k]), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def bulkheads(self):
        b = load("bulkhead")
        sh, bk = b["shared"], b["bulkheads"]
        s0, s1 = sh["slow"]
        n = sh["threads"]
        T = len(sh["share"]["A"])
        worst_a = min(sh["share"]["A"][int(s0):int(s1)])
        mean_bb = sum(bk["share"]["B"][int(s0):int(s1)]) / (s1 - s0)
        head = label(r"Bulkheads: \ one slow dependency", font_size=36).to_edge(UP, buff=0.3)
        sq = 0.22

        def cells(k, col):
            return VGroup(*[Square(sq, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.0)
                            for _ in range(k)])

        pool = cells(n, GREY_B).arrange_in_grid(rows=3, cols=10, buff=0.06)
        pa, pb = cells(n // 2, DATA), cells(n - n // 2, LAM)
        pa.arrange_in_grid(rows=3, cols=5, buff=0.06)
        pb.arrange_in_grid(rows=3, cols=5, buff=0.06)
        wall = Line(UP * 0.5, DOWN * 0.5, color=WHITE, stroke_width=4)
        split = VGroup(pa, wall, pb).arrange(RIGHT, buff=0.15)
        cx = (-3.45, 3.45)
        t_sh = label(rf"one pool of {n} threads", font_size=21, color=GREY_A)
        t_bk = label(rf"two bulkheads of {n // 2}", font_size=21, color=GREY_A)
        VGroup(t_sh, pool).arrange(DOWN, buff=0.15).move_to([cx[0], 2.05, 0])
        VGroup(t_bk, split).arrange(DOWN, buff=0.15).move_to([cx[1], 2.05, 0])
        charts = VGroup()
        lines = []
        for k, run in enumerate((sh, bk)):
            g = axes([0, T, 10], [0, 1, 0.5], x_length=5.2, y_length=2.1, x_label=r"seconds",
                     xticks=range(0, T + 1, 10), yticks=(0, 0.5, 1), fy=lambda v: rf"{100 * v:.0f}\%", font=15)
            g.move_to([cx[k] + 0.1, -0.55, 0])
            ax = g.ax
            bd = shade(ax, s0, s1, 1.0, KERN, op=0.18)
            la = trace(ax, series(run["share"]["A"]), DATA, width=2.8)
            lb = trace(ax, series(run["share"]["B"]), LAM, width=2.8)
            charts.add(VGroup(g, bd))
            lines.append((la, lb))
        ylab = label(r"share of calls that succeed", font_size=16, color=GREY_A).next_to(charts[0][0].ax, UP,
                                                                                         buff=0.22)
        ylab.align_to(charts[0][0].ax, LEFT).shift(UP * 0.02)
        slow_l = label(r"B slow", font_size=15, color=KERN).move_to(charts[1][1]).align_to(charts[1][1], DOWN)
        slow_l.shift(UP * 0.1)
        key = VGroup(label(r"calls to A, \ 40 a second", font_size=17, color=DATA),
                     label(r"calls to B, \ 20 a second", font_size=17, color=LAM)).arrange(RIGHT, buff=0.6)
        key.next_to(charts, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(rf"B's slow calls fill the pool: \ healthy A fails too, \ down to {100 * worst_a:.0f}\% in "
                          r"its worst second", 5.8, font_size=19, color=NO).move_to([cx[0], -3.3, 0]),
            wrapped_label(rf"A is untouched; \ B, \ with half the threads, \ averages {100 * mean_bb:.0f}\% while slow",
                          5.8, font_size=19, color=YES).move_to([cx[1], -3.3, 0]),
        )
        with self.voiceover(
            "A ship's hull is divided by bulkheads, so that one leak floods one compartment, not the ship. "
            "<bookmark mark='a'/> A service calls A forty times a second and B twenty, from one pool of thirty "
            "threads; a call that finds no free thread is rejected. <bookmark mark='b'/> At twenty seconds B "
            "turns slow, two seconds a call instead of fifty milliseconds, and its calls fill the pool. <bookmark "
            "mark='c'/> So calls to the healthy A fail too: in the worst second, only twenty-eight percent "
            "succeed. <bookmark mark='d'/> Split the pool into two bulkheads of fifteen, and A does not notice. "
            "B, with half the threads, does worse. The damage stays where it started."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t_sh), FadeIn(pool), FadeIn(charts[0][0]), FadeIn(ylab), FadeIn(key))
            vo.wait_until("b")
            self.play(LaggedStart(*[c.animate.set_fill(LAM, 0.85).set_stroke(LAM) for c in pool], lag_ratio=0.04),
                      FadeIn(charts[0][1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lines[0][0]), Create(lines[0][1]), run_time=2.0)
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(t_bk), FadeIn(split), FadeIn(charts[1]), FadeIn(slow_l))
            self.play(LaggedStart(*[c.animate.set_fill(LAM, 0.85) for c in pb], lag_ratio=0.06), run_time=1.2)
            self.play(Create(lines[1][0]), Create(lines[1][1]), run_time=2.0)
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def degrade(self):
        head = label(r"Degrade, \ don't fail", font_size=36).to_edge(UP, buff=0.3)
        # a page made of parts that matter unequally (illustrative)
        page = RoundedRectangle(width=5.0, height=4.6, corner_radius=0.15, stroke_color=GREY_C, stroke_width=2)
        page.move_to([-4.0, -0.35, 0])
        ptitle = label(r"a product page", font_size=19, color=GREY_A).next_to(page, UP, buff=0.1)

        def part(text, col, w=4.4, h=0.75):
            r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=col, stroke_width=2,
                                 fill_color=col, fill_opacity=0.12)
            return VGroup(r, label(text, font_size=18, color=WHITE).move_to(r))
        parts = VGroup(part(r"price, \ stock, \ buy button", YES), part(r"reviews", DATA),
                       part(r"recommended for you", LAM), part(r"recently viewed", DATA)).arrange(DOWN, buff=0.25)
        parts.move_to(page)
        fallback = part(r"popular items \ (cached)", HEAD).move_to(parts[2])
        slow = label(r"recommender slow", font_size=17, color=NO).next_to(page, RIGHT, buff=0.15).set_y(
            parts[2].get_y())
        ill = note(r"illustrative", font_size=16).next_to(page, DOWN, buff=0.12).align_to(page, LEFT)
        # backpressure (Part 43)
        prod = node(r"producer", DATA, w=1.9, h=0.75, size=18)
        cons = node(r"consumer", KERN, w=1.9, h=0.75, size=18)
        slots = VGroup(*[Square(0.34, stroke_color=GREY_B, stroke_width=1.5) for _ in range(6)]).arrange(RIGHT,
                                                                                                         buff=0.05)
        pipe = VGroup(prod, slots, cons).arrange(RIGHT, buff=0.35).move_to([2.95, 1.95, 0])
        f1 = Arrow(prod.get_right(), slots.get_left(), buff=0.05, color=GREY_B, stroke_width=2)
        f2 = Arrow(slots.get_right(), cons.get_left(), buff=0.05, color=GREY_B, stroke_width=2)
        back = CurvedArrow(slots.get_top() + UP * 0.08 + LEFT * 0.2, prod.get_top() + UP * 0.08, angle=PI / 3,
                           color=NO, stroke_width=2.5)
        back_l = label(r"full: \ slow down", font_size=17, color=NO).next_to(back, UP, buff=0.05)
        bp_l = label(r"backpressure \ (Part 43): \ a bounded queue", font_size=18, color=GREY_A).next_to(
            pipe, DOWN, buff=0.2)
        # criticality
        tiers = VGroup(*[VGroup(mono(t, size=17, color=c), label(d, font_size=17, color=GREY_A))
                         for t, d, c in (("CRITICAL_PLUS", r"checkout", YES), ("CRITICAL", r"page views", YES),
                                         ("SHEDDABLE_PLUS", r"prefetching", HEAD),
                                         ("SHEDDABLE", r"batch reports", NO))])
        for t in tiers:
            t[1].next_to(t[0], RIGHT, buff=0.3)
        tiers.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.4, -1.5, 0])
        xd = max(t[0].get_right()[0] for t in tiers) + 0.35
        for t in tiers:
            t[1].set_y(t[0].get_y()).align_to([xd, 0, 0], LEFT)
        order = Arrow(tiers.get_corner(UR) + RIGHT * 0.35, tiers.get_corner(DR) + RIGHT * 0.35, buff=0, color=NO,
                      stroke_width=2.5)
        tiers_t = label(r"criticality, \ as in Google's SRE book: \ shed from the bottom", font_size=18,
                        color=GREY_A).next_to(tiers, UP, buff=0.2).align_to(tiers, LEFT)
        with self.voiceover(
            "Serving something less is better than refusing. <bookmark mark='a'/> A product page has parts that "
            "matter unequally. When the recommender is slow, the page neither waits nor fails: it shows a cached "
            "list of popular items, and the price and the buy button still work. <bookmark mark='b'/> Overload "
            "can also be pushed back to its source: Part 43's backpressure bounds every queue, so a full queue "
            "slows the producer instead of growing. <bookmark mark='c'/> And when something must be refused, "
            "refuse the least important first. Google's SRE book describes tagging each request with a "
            "criticality, from critical plus down to sheddable, and shedding from the bottom."
        ) as vo:
            self.play(FadeIn(head), Create(page), FadeIn(ptitle), FadeIn(parts), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(slow), parts[2][0].animate.set_stroke(NO, 3))
            self.play(FadeOut(parts[2]), FadeIn(fallback))
            vo.wait_until("b")
            self.play(FadeIn(pipe), GrowArrow(f1), GrowArrow(f2), FadeIn(bp_l))
            self.play(LaggedStart(*[s.animate.set_fill(DATA, 0.7) for s in slots], lag_ratio=0.2), run_time=1.5)
            self.play(Create(back), FadeIn(back_l))
            vo.wait_until("c")
            self.play(FadeIn(tiers_t), LaggedStart(*[FadeIn(t) for t in tiers], lag_ratio=0.25), run_time=1.5)
            self.play(GrowArrow(order))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM,)
