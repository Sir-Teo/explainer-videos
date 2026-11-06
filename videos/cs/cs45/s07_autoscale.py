from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, module_box,
                                   trace)


def k_max(d: int) -> float:
    """Largest gain for which e[t+1] = e[t] - K e[t-d] is stable: the roots of z^(d+1) - z^d + K stay inside the
    unit circle while K < 2 cos(d pi / (2d + 1))."""
    return 2 * math.cos(d * math.pi / (2 * d + 1))


def setup(a):
    """The experiment's settings, read back from a run: the step of the jump, the loads before and after, a
    server's capacity and the utilization target."""
    s = a["0.2-3"]["series"]
    spike = next(r["t"] for r in s if r["load"] > 1.5 * s[0]["load"])
    base = round(sum(r["load"] for r in s[:spike]) / spike, -1)
    high = round(sum(r["load"] for r in s[spike:]) / (len(s) - spike), -1)
    cap = round(s[1]["load"] / (s[1]["util"] * s[0]["servers"]), 1)
    target = round(high / (cap * a["0.2-3"]["ideal"]), 2)
    return spike, base, high, cap, target


class Autoscale(VoiceoverScene):
    def construct(self):
        self.card()
        self.loop()
        self.runs()
        self.stability()
        self.erlang()
        self.economy()
        self.predictive()

    def card(self):
        card = chapter_card(6, r"Autoscaling as control", r"How many servers does the load need, and how fast?",
                            lit=(1868, 1917), extra=((1868, r"Maxwell: \ On Governors"),
                                                     (1917, r"Erlang: \ waiting at telephone exchanges")), part=PART)
        with self.voiceover("Chapter six. Autoscaling as control."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def loop(self):
        head = label(r"An autoscaler is a feedback loop", font_size=36).to_edge(UP, buff=0.3)
        ctl = module_box(r"controller", KERN, w=2.4, h=0.65, font=20).move_to([-3.6, 2.0, 0])
        srv = module_box(r"servers $n$", YES, w=2.4, h=0.65, font=20).move_to([1.2, 2.0, 0])
        utl = module_box(r"utilization $u$", HEAD, w=2.4, h=0.65, font=20).move_to([1.2, 0.5, 0])
        mes = module_box(r"measurement", NO, w=2.4, h=0.65, font=20).move_to([-3.6, 0.5, 0])
        lod = module_box(r"load $\lambda$", DATA, w=2.0, h=0.65, font=20).move_to([5.0, 0.5, 0])
        arrows = VGroup(*[Arrow(a, b, buff=0.08, stroke_width=2.2, color=GREY_B) for a, b in (
            (ctl.get_right(), srv.get_left()), (srv.get_bottom(), utl.get_top()), (utl.get_left(), mes.get_right()),
            (mes.get_top(), ctl.get_bottom()), (lod.get_left(), utl.get_right()))])
        tags = VGroup(
            label(r"start or stop", font_size=16, color=GREY_A).next_to(arrows[0], UP, buff=0.06),
            label(r"$d$ steps late", font_size=16, color=NO).next_to(arrows[2], DOWN, buff=0.06),
            label(r"new servers take time to boot", font_size=16, color=GREY_A).next_to(arrows[1], RIGHT, buff=0.1))
        eqs = VGroup(
            VGroup(label(r"Kubernetes' Horizontal Pod Autoscaler:", font_size=19, color=GREY_A),
                   MathTex(r"n \leftarrow \left\lceil n \cdot \frac{u}{u^{*}} \right\rceil", font_size=32,
                           color=WHITE)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"our controller, \ gain $K$:", font_size=19, color=GREY_A),
                   MathTex(r"n_{t+1} = n_t + K \left( \frac{u_{t-d}}{u^{*}} - 1 \right) n_t", font_size=32,
                           color=YES)).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(VGroup(mes, utl), DOWN, buff=0.6).set_x(0)
        line = wrapped_label(r"$u^{*}$ is the target utilization; \ with $K = 1$ ours is Kubernetes' rule, \ which "
                             r"adds a tolerance band and slows scaling down", 12.4, font_size=19,
                             color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "An autoscaler watches how busy the servers are, and adds or removes some: a feedback loop. "
            "<bookmark mark='a'/> Load arrives; the servers share it, which sets their utilization; the "
            "controller measures that, and starts or stops servers. But the measurement is late, and a new "
            "server takes time to boot, so the controller acts on the past. <bookmark mark='b'/> Kubernetes' "
            "horizontal pod autoscaler multiplies the replicas by measured over target utilization, rounded up."
            " <bookmark mark='c'/> Ours moves a fraction K of the way, from a measurement d steps old. K equal "
            "to one is Kubernetes' rule."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lod), FadeIn(utl), GrowArrow(arrows[4]))
            self.play(FadeIn(srv), GrowArrow(arrows[1]), FadeIn(tags[2]))
            self.play(GrowArrow(arrows[2]), FadeIn(mes), FadeIn(tags[1]))
            self.play(GrowArrow(arrows[3]), FadeIn(ctl), GrowArrow(arrows[0]), FadeIn(tags[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[1]), FadeIn(line))
        self.wait(0.4)
        self.clear_scene()

    def runs(self):
        a = load("autoscale")
        spike, base, high, cap, target = setup(a)
        head = label(r"Settle, \ ring, \ or slam", font_size=36).to_edge(UP, buff=0.3)
        specs = [("0.3-1", YES, 30, 10), ("0.2-3", HEAD, 30, 10), ("0.5-3", NO, 120, 50), ("1.0-3", NO, 220, 100)]
        centres = [(-3.35, 1.25), (3.25, 1.25), (-3.35, -1.65), (3.25, -1.65)]
        panels = []
        for (key, col, ymax, ystep), (cx, cy) in zip(specs, centres):
            r = a[key]
            s = r["series"]
            n = len(s)
            after = [x["servers"] for x in s[spike + 5:]]
            if r["settled"]:
                verdict = rf"settles at {r['final_servers']:.1f}; \ peak {r['peak_servers']:.1f}"
            elif r["peak_servers"] >= 199:
                verdict = rf"between {min(after):.0f} and the quota of {r['peak_servers']:.0f}"
            else:
                verdict = rf"oscillates between {min(after):.0f} and {max(after):.0f}"
            title = rf"$K = {r['gain']:g}$, \ delay {r['delay']}: \ {verdict}"
            g = axes([0, n, 20], [0, ymax, ystep], x_length=5.6, y_length=1.65, y_label=title,
                     xticks=range(0, n + 1, 20), yticks=range(0, ymax + 1, ystep * (2 if ymax > 100 else 1)))
            g.move_to([cx, cy, 0])
            g[-1].set_color(col)
            ax = g.ax
            ideal = DashedLine(ax.c2p(0, r["ideal"]), ax.c2p(n, r["ideal"]), color=GREY_B, stroke_width=1.5)
            jump = DashedLine(ax.c2p(spike, 0), ax.c2p(spike, ymax), color=DATA, stroke_width=1.2)
            line = trace(ax, [(x["t"], x["servers"]) for x in s], col, width=3)
            panels.append((g, VGroup(ideal, jump), line))
        cap_l = wrapped_label(rf"load jumps from {base:.0f} to {high:.0f} requests a second at step {spike} \ "
                              r"(blue); \ a server handles " + f"{cap:g}" + r" at full use; \ target "
                              rf"{100 * target:.0f}\% utilization, \ so the right size is "
                              rf"{a['0.2-3']['ideal']:.1f} servers \ (grey)", 12.6, font_size=18,
                              color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "We gave it a load that jumps from forty to a hundred requests a second. At sixty percent "
            "utilization, the right size is about seventeen servers. <bookmark mark='a'/> With a delay of one "
            "step and a gain of three tenths, it overshoots to eighteen, and settles. <bookmark mark='b'/> With"
            " a three-step delay, a gain of two tenths still settles, after overshooting to twenty-five. "
            "<bookmark mark='c'/> At one half, it never settles, swinging between about five servers and a "
            "hundred. <bookmark mark='d'/> At a gain of one, Kubernetes' rule, it slams between one server and "
            "the quota of two hundred. Only the gain changed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap_l), *[FadeIn(p[0]) for p in panels], *[Create(p[1]) for p in panels])
            for mk, p in zip("abcd", panels):
                vo.wait_until(mk)
                self.play(Create(p[2]), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def stability(self):
        a = load("autoscale")
        head = label(r"Why delay makes it ring", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 6.3, 1], [0, 2.4, 0.5], x_length=5.6, y_length=4.0, x_label=r"delay $d$ \ (steps)",
                 y_label=r"gain $K$", xticks=range(0, 7), yticks=(0.5, 1.0, 1.5, 2.0)).move_to([-3.35, -0.35, 0])
        ax = g.ax
        ds = range(0, 7)
        curve = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(d, k_max(d)) for d in ds])
        dots = VGroup(*[Dot(ax.c2p(d, k_max(d)), radius=0.05, color=YES) for d in ds])
        region = Polygon(*[ax.c2p(d, k_max(d)) for d in ds], ax.c2p(6, 0), ax.c2p(0, 0), stroke_width=0,
                         fill_color=YES, fill_opacity=0.15)
        rl = label(r"settles", font_size=18, color=YES).move_to(ax.c2p(5.0, 0.1))
        ul = label(r"rings or slams", font_size=18, color=NO).move_to(ax.c2p(3.8, 1.5))
        runs = VGroup()
        for r in a.values():
            p = ax.c2p(r["delay"], r["gain"])
            runs.add(VGroup(Dot(p, radius=0.09, color=YES if r["settled"] else NO),
                            label(rf"${r['gain']:g}$", font_size=16, color=WHITE).next_to(p, RIGHT, buff=0.12)))
        steps = VGroup(
            label(r"near the right size $n^{*}$, \ with error $e_t = n_t - n^{*}$:", font_size=19, color=GREY_A),
            MathTex(r"e_{t+1} = e_t - K\, e_{t-d}", font_size=34, color=WHITE),
            wrapped_label(r"the correction is computed from an error $d$ steps old: \ it keeps adding servers after "
                          r"the fleet is already big enough, \ and overshoots", 5.4, font_size=19, color=WHITE),
            wrapped_label(r"the roots of $z^{d+1} - z^{d} + K$ stay inside the unit circle only while", 5.4,
                          font_size=19, color=GREY_A),
            MathTex(r"K < 2\cos\frac{d\pi}{2d+1}", font_size=34, color=YES),
            wrapped_label(rf"$d = 0$: \ $K < 2$; \ \ $d = 1$: \ $K < {k_max(1):.2f}$; \ \ $d = 3$: \ "
                          rf"$K < {k_max(3):.2f}$ \ --- \ every one of our four runs lands on the predicted side",
                          5.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.5, -0.2, 0])
        with self.voiceover(
            "Here is why. <bookmark mark='a'/> Near the right size, each step corrects the"
            " error by K times the error as it was d steps ago. So once the fleet is big enough, the controller"
            " keeps adding, because it acts on old measurements. <bookmark mark='b'/> The error dies away only "
            "while K stays below twice the cosine of d pi over two d plus one: below two with no delay, below "
            "one with one step, and below about forty-five hundredths with three. <bookmark mark='c'/> Our four"
            " runs land exactly where the curve predicts. As Maxwell found for steam-engine governors in 1868, "
            "the more a loop lags, the gentler it must be."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(steps[1]), FadeIn(steps[2]))
            vo.wait_until("b")
            self.play(FadeIn(steps[3]), FadeIn(steps[4]))
            self.play(FadeIn(region), Create(curve), FadeIn(dots), FadeIn(rl), FadeIn(ul), FadeIn(steps[5]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, scale=0.5) for r in runs], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def erlang(self):
        e = load("erlang")
        head = label(r"How many servers? \ Erlang C", font_size=36).to_edge(UP, buff=0.3)
        names = [r"0", r"1", r"\cdots", r"c-1", r"c", r"c+1", r"\cdots"]
        states = VGroup()
        for t in names:
            if t == r"\cdots":
                states.add(MathTex(t, font_size=30, color=GREY_B))
            else:
                c = Circle(radius=0.36, color=HEAD if t == "c" else DATA, stroke_width=2)
                states.add(VGroup(c, MathTex(t, font_size=24, color=WHITE).move_to(c)))
        states.arrange(RIGHT, buff=1.05).move_to([0, 1.85, 0])
        fwd, back = VGroup(), VGroup()
        downs = [r"\mu", r"2\mu", r"(c-1)\mu", r"c\mu", r"c\mu", r"c\mu"]
        for i in range(len(states) - 1):
            l, r = states[i], states[i + 1]
            fa = Arrow(l.get_right() + UP * 0.13, [r.get_left()[0], l.get_y() + 0.13, 0], buff=0.06, color=GREY_B,
                       stroke_width=1.8, max_tip_length_to_length_ratio=0.18)
            ba = Arrow([r.get_left()[0], l.get_y() - 0.13, 0], l.get_right() + DOWN * 0.13, buff=0.06, color=GREY_B,
                       stroke_width=1.8, max_tip_length_to_length_ratio=0.18)
            fwd.add(VGroup(fa, MathTex(r"\lambda", font_size=22, color=DATA).next_to(fa, UP, buff=0.04)))
            back.add(VGroup(ba, MathTex(downs[i], font_size=20, color=YES).next_to(ba, DOWN, buff=0.04)))
        cl = label(r"requests in the system: \ arrivals at rate $\lambda$, \ each busy server finishes at rate $\mu$",
                   font_size=18, color=GREY_A).next_to(VGroup(states, back), DOWN, buff=0.15)
        eqs = VGroup(
            MathTex(r"\pi_k = \pi_0 \frac{a^k}{k!} \ (k \le c), \qquad \pi_k = \pi_c\, \rho^{\,k-c} \ (k \ge c), "
                    r"\qquad a = \frac{\lambda}{\mu},\ \rho = \frac{a}{c}", font_size=28, color=WHITE),
            MathTex(r"C(c, a) = \Pr[\text{wait}] = \frac{a^c / \big(c!\,(1-\rho)\big)}{\sum_{k=0}^{c-1} "
                    r"a^k / k! \; + \; a^c / \big(c!\,(1-\rho)\big)}, \qquad W_q = \frac{C(c, a)}{c\mu - "
                    r"\lambda}", font_size=30, color=YES),
            wrapped_label(rf"check: \ two servers, \ one erlang of load: \ $C(2, 1) = {e['check']:.3f}$, \ a third; "
                          r"\ with one server $C = \rho$, \ Part 31's M/M/1 queue", 12.4, font_size=19, color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(cl, DOWN, buff=0.35)
        with self.voiceover(
            "Queueing theory supplies the target. <bookmark mark='a'/> Model the pool "
            "as Part 31's queue, now with c servers. Requests arrive at rate lambda; with k servers busy they "
            "finish at k times mu. <bookmark mark='b'/> Balancing the flow across each "
            "step gives a to the k over k factorial up to c, then a geometric tail with ratio rho, the load per"
            " server. <bookmark mark='c'/> Summing the tail gives Agner Erlang's formula of 1917 for the chance"
            " of waiting, and the mean wait follows. <bookmark mark='d'/> Two servers with one erlang of load: "
            "a request waits a third of the time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in states], lag_ratio=0.1), FadeIn(cl))
            self.play(LaggedStart(*[Create(f) for f in fwd], lag_ratio=0.1),
                      LaggedStart(*[Create(b) for b in back], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("d")
            self.play(FadeIn(eqs[2]))
        self.wait(0.4)
        self.clear_scene()

    def economy(self):
        rows_d = load("erlang")["rows"]
        head = label(r"Big pools run hotter", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{r['load']:,.0f}", f"{r['servers']:,}", f"{r['p_wait']:.2f}", f"{r['mean_wait']:.3f}",
                 f"{(r['servers'] - r['load']) / math.sqrt(r['load']):.2f}"] for r in rows_d]
        tab = grid_table([r"load $a$ \ (erlangs)", r"servers $c$", r"P(wait)", r"mean wait",
                          r"$(c - a)/\sqrt{a}$"], rows, widths=[2.2, 1.6, 1.4, 1.6, 1.8], row_h=0.5, font_size=19,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.85).to_edge(LEFT, buff=0.4)
        for i in range(1, len(rows) + 1):
            tab.cells[i][1].set_color(HEAD)
            tab.cells[i][4].set_color(LAM)
        bars = VGroup()
        x0 = tab.get_right()[0] + 0.5
        for i, r in enumerate(rows_d, 1):
            w = r["utilization"] * 3.0
            b = Rectangle(width=w, height=0.32, stroke_width=0, fill_color=YES, fill_opacity=0.85)
            b.move_to([x0 + w / 2, tab.cells[i][0].get_y(), 0])
            bars.add(VGroup(b, label(rf"{100 * r['utilization']:.0f}\%", font_size=18, color=YES).next_to(
                b, RIGHT, buff=0.1)))
        bt = label(r"utilization", font_size=19, color=GREY_B).move_to([x0 + 1.5, tab.cells[0][0].get_y(), 0])
        rule = label(r"fewest servers keeping the mean wait under a twentieth of a service time \ and P(wait) under "
                     r"a fifth", font_size=17, color=GREY_A).next_to(tab, UP, buff=0.2).align_to(tab, LEFT)
        lines = VGroup(
            wrapped_label(r"spare capacity grows like $\sqrt{a}$, \ not like $a$: \ $c \approx a + \beta\sqrt{a}$, "
                          r"\ square-root staffing \ (Halfin and Whitt, \ 1981)", 12.4, font_size=20, color=LAM),
            wrapped_label(r"so one big shared pool needs proportionally fewer idle servers than many small ones: \ "
                          r"the economy of scale behind the cloud itself", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now size pools of very different scales with one promise: a short mean wait, and at most one "
            "request in five waiting at all. <bookmark mark='a'/> Ten erlangs of load need fourteen servers, "
            "only seventy-one percent busy. A thousand erlangs need one thousand and thirty-four, ninety-seven "
            "percent busy. <bookmark mark='b'/> The spare capacity grows like the square root of the load: "
            "Halfin and Whitt's square-root staffing, from 1981. <bookmark mark='c'/> So one big shared pool "
            "needs far fewer idle servers, in proportion, than many small ones. That is the economy of scale "
            "behind the cloud itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rule), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(bt))
            vo.wait_until("a")
            for i in range(1, len(rows) + 1):
                self.play(FadeIn(VGroup(*tab.cells[i])), GrowFromEdge(bars[i - 1][0], LEFT),
                          FadeIn(bars[i - 1][1]), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(lines[0]), Indicate(VGroup(*[tab.cells[i][4] for i in range(1, len(rows) + 1)]),
                                                 color=LAM, scale_factor=1.05))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def predictive(self):
        head = label(r"Scaling before the load arrives", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 48, 6], [0, 100, 20], x_length=7.2, y_length=3.6, x_label=r"two days, \ hour by hour",
                 y_label=r"servers needed, \ and provided").move_to([-2.7, -0.1, 0])
        ax = g.ax

        def need(t):
            return 50 - 35 * math.cos(2 * math.pi * t / 24)
        ts = [i / 4 for i in range(0, 48 * 4 + 1)]
        lag = 2.0
        demand = trace(ax, [(t, need(t)) for t in ts], DATA, width=3)
        reactive = trace(ax, [(t, 1.05 * need(max(0, t - lag))) for t in ts], NO, width=2.5)
        predicted = DashedVMobject(trace(ax, [(t, 1.05 * need(t)) for t in ts], YES, width=2.5), num_dashes=80)
        short = VGroup()
        for t0, t1 in zip(ts[:-1], ts[1:]):
            lo0, hi0 = 1.05 * need(max(0, t0 - lag)), need(t0)
            if lo0 < hi0:
                short.add(Polygon(ax.c2p(t0, lo0), ax.c2p(t1, 1.05 * need(max(0, t1 - lag))), ax.c2p(t1, need(t1)),
                                  ax.c2p(t0, hi0), stroke_width=0, fill_color=NO, fill_opacity=0.35))
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=c, stroke_width=3), label(t, font_size=17, color=c))
                       .arrange(RIGHT, buff=0.12) for t, c in ((r"demand", DATA), (r"reactive", NO),
                                                                (r"predictive", YES))]).arrange(RIGHT, buff=0.4)
        key.next_to(g, DOWN, buff=0.15)
        ill = note(r"illustrative", font_size=16).next_to(ax, UP, buff=0.1).align_to(ax, RIGHT)
        notes = VGroup(
            wrapped_label(r"a reactive scaler is late by its measurement window plus a boot: \ every rising "
                          r"morning it is short \ (red)", 4.7, font_size=19, color=NO),
            wrapped_label(r"most load repeats by the day and the week: \ forecast the next hours from past weeks, \ "
                          r"and start machines one boot time early", 4.7, font_size=19, color=YES),
            wrapped_label(r"keep the reactive loop as a backstop for what no forecast saw; \ the serverless "
                          r"chapter takes boot time towards zero, \ and Part 50 plans capacity for the peaks", 4.7,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.45, -0.1, 0])
        with self.voiceover(
            "Even a well-tuned reactive loop is late. <bookmark mark='a'/> It sees the load after a measurement"
            " window, and its servers arrive a boot time after that, so every rising morning it runs short. "
            "<bookmark mark='b'/> But most load repeats, by the day and by the week. Predictive scaling, which "
            "the big clouds now offer, forecasts the next hours from past weeks and starts machines a boot time"
            " ahead. <bookmark mark='c'/> The reactive loop stays as a backstop for surprises. The next chapter"
            " shrinks the boot itself, and Part 50 returns to planning for the peaks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ill), Create(demand), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(Create(reactive), FadeIn(key[1]), run_time=2)
            self.play(FadeIn(short), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(predicted), FadeIn(key[2]), FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM)
