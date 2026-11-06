from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, curve, fit_right, grid_table, load)

ARR = [0.4, 1.1, 1.6, 3.0, 3.3, 5.0, 5.5, 6.0]
SVC = [1.0, 0.8, 0.7, 0.9, 0.6, 0.5, 1.0, 0.4]


def fcfs(arr, svc):
    out, free = [], 0.0
    for a, s in zip(arr, svc):
        free = max(a, free) + s
        out.append(free)
    return out


class Queueing(VoiceoverScene):
    def construct(self):
        self.card()
        self.little()
        self.mm1()
        self.hockey()
        self.paths()
        self.variance()
        self.srpt()

    def card(self):
        card = chapter_card(12, r"Queueing theory", r"Why is a busy server so slow?", lit=(1909, 1961, 1968),
                            extra=((1909, r"Erlang"), (1961, r"Little's law"), (1968, r"SRPT is optimal")), part=PART)
        with self.voiceover("Chapter twelve. Queueing theory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def little(self):
        q = load("queue")
        head = label(r"Little's law, \ by areas", font_size=36).to_edge(UP, buff=0.3)
        dep = fcfs(ARR, SVC)
        T = 7.6
        ax = Axes(x_range=[0, T, 1], y_range=[0, 8.5, 2], x_length=6.6, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)

        def stair(ts, color):
            pts, n = [ax.c2p(0, 0)], 0
            for t in sorted(ts):
                pts += [ax.c2p(t, n), ax.c2p(t, n + 1)]
                n += 1
            pts.append(ax.c2p(T, n))
            return VMobject(color=color, stroke_width=3).set_points_as_corners(pts)
        A = stair(ARR, DATA)
        D = stair(dep, HEAD)
        strips = VGroup()
        for i, (a, d) in enumerate(zip(ARR, dep)):
            strips.add(Polygon(ax.c2p(a, i), ax.c2p(d, i), ax.c2p(d, i + 1), ax.c2p(a, i + 1), stroke_width=0,
                               fill_color=YES, fill_opacity=0.35))
        xl = label(r"time", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.1)
        ka = label(r"arrivals so far", font_size=18, color=DATA).move_to(ax.c2p(1.6, 6.3))
        kd = label(r"departures so far", font_size=18, color=HEAD).move_to(ax.c2p(5.6, 1.4))
        m = q["mm1"][7]
        notes = VGroup(
            label(r"strip $i$: \ one customer, \ as long as it stays: \ its time in the system $W_i$", font_size=20,
                  color=YES),
            label(r"read the same area by columns: \ the height at time $t$ is $N(t)$, \ the number inside",
                  font_size=20, color=WHITE),
            MathTex(r"\sum_i W_i = \int_0^T N(t)\,dt", font_size=34, color=WHITE),
            label(r"divide by $T$: \ $L = \lambda W$, \ for \textit{any} queue that empties", font_size=20,
                  color=HEAD),
            label(rf"simulated at load 0.8: \ $L$ = {m['L']:.3f}, \ $\lambda W$ = {m['lamW']:.3f}", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Queueing theory begins with a law so general it is almost a tautology. <bookmark mark='a'/> Plot the "
            "number of customers who have arrived at a server, and below it the number who have left. <bookmark "
            "mark='b'/> Between the two curves, each horizontal strip is one customer, from arrival to departure: "
            "its width is that customer's time in the system. <bookmark mark='c'/> Now read the same area by "
            "columns: at any moment the height between the curves is the number of customers inside. <bookmark "
            "mark='d'/> So the total of everyone's time equals the integral of the number present. <bookmark "
            "mark='e'/> Divide both sides by the length of time. On the left, arrivals per unit time times the mean "
            "time each spends; on the right, the mean number inside. L equals lambda W. John Little proved it in "
            "general in 1961: it holds for any queue, any order, any distribution. <bookmark mark='f'/> In our "
            "simulation at eighty percent load, the two sides agree to three decimal places."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(A), FadeIn(ka), Create(D), FadeIn(kd), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in strips], lag_ratio=0.15), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
            vo.wait_until("f")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def mm1(self):
        head = label(r"The M/M/1 queue", font_size=36).to_edge(UP, buff=0.3)
        states = VGroup(*[VGroup(Circle(radius=0.38, stroke_color=DATA, stroke_width=2.5, fill_color=BG,
                                        fill_opacity=1), MathTex(str(k), font_size=30)) for k in range(5)])
        for s in states:
            s[1].move_to(s[0])
        states.arrange(RIGHT, buff=1.1).next_to(head, DOWN, buff=0.9)
        dots_ = MathTex(r"\cdots", font_size=36).next_to(states, RIGHT, buff=0.4)
        arcs = VGroup()
        for a, b in zip(states[:-1], states[1:]):
            arcs.add(CurvedArrow(a[0].get_top() + RIGHT * 0.1, b[0].get_top() + LEFT * 0.1, angle=-0.8, color=YES,
                                 stroke_width=2, tip_length=0.14))
            arcs.add(CurvedArrow(b[0].get_bottom() + LEFT * 0.1, a[0].get_bottom() + RIGHT * 0.1, angle=-0.8,
                                 color=NO, stroke_width=2, tip_length=0.14))
        lam = MathTex(r"\lambda", font_size=28, color=YES).next_to(arcs[0], UP, buff=0.05)
        mu = MathTex(r"\mu", font_size=28, color=NO).next_to(arcs[1], DOWN, buff=0.05)
        sl = label(r"customers in the system: \ arrivals at rate $\lambda$ \ (Poisson), \ service at rate $\mu$ "
                   r"\ (exponential)", font_size=20, color=GREY_A).next_to(states, DOWN, buff=0.75)
        eqs = VGroup(
            MathTex(r"\lambda\, p_n = \mu\, p_{n+1}", font_size=34),
            MathTex(r"p_n = (1 - \rho)\,\rho^n, \qquad \rho = \lambda / \mu", font_size=34),
            MathTex(r"L = \sum_n n\, p_n = \frac{\rho}{1 - \rho}", font_size=34),
            MathTex(r"W = \frac{L}{\lambda} = \frac{1}{\mu - \lambda}", font_size=40, color=HEAD),
        ).arrange(RIGHT, buff=0.7).next_to(sl, DOWN, buff=0.55)
        if eqs.width > 13.2:
            eqs.scale_to_fit_width(13.2)
        caps = VGroup(*[label(t, font_size=17, color=GREY_B).next_to(e, DOWN, buff=0.2) for t, e in zip(
            (r"flow across each cut balances", r"so the states fall off geometrically", r"the mean number inside",
             r"Little's law: \ the mean time inside"), eqs)])
        with self.voiceover(
            "The simplest queue with randomness in it is called M/M/1: customers arrive at random, at rate lambda; "
            "one server works on them at rate mu, each job taking a random, exponentially distributed time. "
            "<bookmark mark='a'/> Its state is just the number of customers inside. Arrivals push it up one, at rate "
            "lambda; completions pull it down one, at rate mu. <bookmark mark='b'/> In the long run, the flow across "
            "each cut between neighbouring states must balance: lambda times the probability of n equals mu times "
            "the probability of n plus one. <bookmark mark='c'/> So the probabilities fall off geometrically, by the "
            "ratio rho, lambda over mu, which is the fraction of time the server is busy. <bookmark mark='d'/> The "
            "mean number inside is rho over one minus rho. <bookmark mark='e'/> And by Little's law, the mean time "
            "inside is one over mu minus lambda."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(s) for s in states], lag_ratio=0.15), FadeIn(dots_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.1), FadeIn(lam), FadeIn(mu), FadeIn(sl),
                      run_time=2.0)
            for mk, e, c in zip("bcde", eqs, caps):
                vo.wait_until(mk)
                self.play(FadeIn(e), FadeIn(c))
        self.wait(0.3)
        self.clear_scene()

    def hockey(self):
        q = load("queue")
        head = label(r"The hockey stick", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 1.0, 0.1], y_range=[0, 22, 5], x_length=6.6, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        xt = VGroup(*[label(f"{int(x * 100)}\\%", font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (0, 0.2, 0.4, 0.6, 0.8, 1.0)])
        yt = VGroup(*[label(str(y), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0, 5, 10, 15, 20)])
        xl = label(r"load $\rho$", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"mean response, \ in service times", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        xs = np.linspace(0, 0.955, 120)
        formula = ax.plot_line_graph(xs, 1 / (1 - xs), add_vertex_dots=False, line_color=HEAD, stroke_width=3)
        sims = VGroup(*[Dot(ax.c2p(m["rho"], m["sim"]), radius=0.06, color=YES) for m in q["mm1"]
                        if m["rho"] != 0.93])
        p50 = next(m for m in q["mm1"] if m["rho"] == 0.5)
        p90 = next(m for m in q["mm1"] if m["rho"] == 0.9)
        notes = VGroup(
            label(r"$1/(1 - \rho)$, \ and the simulation \ (dots, \ a million jobs each)", font_size=20, color=WHITE),
            label(rf"50\% busy: \ {p50['sim']:.1f} service times", font_size=21, color=YES),
            label(rf"90\% busy: \ {p90['sim']:.1f}: \ five times worse", font_size=21, color=NO),
            label(rf"and the tail: \ at 90\%, \ 1 in 100 takes {math.log(100) / 0.1:.0f} service times \\ "
                  rf"(exactly $\ln 100 / (1 - \rho)$; \ simulated {p90['p99']:.0f})", font_size=21, color=NO),
            label(r"each step closer to 100\% costs more than the last: \\ capacity planners aim for 50--70\%",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Plot one over one minus rho, the mean response time in units of the service time. <bookmark mark='a'/> "
            "It is the hockey stick. The dots are our simulation, a million jobs at each load, and they sit on the "
            "formula. <bookmark mark='b'/> At fifty percent load, a request takes twice as long as on an idle "
            "machine. <bookmark mark='c'/> At ninety percent, ten times as long: five times worse than at fifty, "
            "though the server is only working eighty percent harder. <bookmark mark='d'/> The tail is worse still: "
            "at ninety percent load, one request in a hundred takes forty-six service times, because the response time "
            "of this queue is itself exponentially distributed. <bookmark mark='e'/> "
            "Near a hundred percent, every extra percent of load costs more than the one before, which is why people "
            "who plan capacity aim for fifty to seventy percent, and why a server that seemed fine yesterday can fall "
            "over today with only a little more traffic."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(formula), LaggedStart(*[FadeIn(s) for s in sims], lag_ratio=0.1), FadeIn(notes[0]),
                      run_time=2.0)
            for mk, n_ in zip("bcde", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def paths(self):
        q = load("queue")
        head = label(r"Why: \ a random walk with a floor", font_size=36).to_edge(UP, buff=0.3)
        out = VGroup()
        for k, (rho, color) in enumerate((("0.5", YES), ("0.9", NO))):
            pth = q["paths"][rho]
            ymax = 24
            ax = Axes(x_range=[0, 300, 50], y_range=[0, ymax, 8], x_length=11.4, y_length=2.1,
                      axis_config={"color": GREY_D, "include_numbers": False})
            ax.move_to([0.3, 1.25 - 2.75 * k, 0])
            pts = []
            last = 0
            for t, n in pth:
                if t > 300:
                    break
                pts += [ax.c2p(t, min(last, ymax)), ax.c2p(t, min(n, ymax))]
                last = n
            line = VMobject(color=color, stroke_width=1.8).set_points_as_corners(pts)
            lab = label(rf"load {rho}", font_size=20, color=color).next_to(ax, LEFT, buff=0.15)
            yt = VGroup(*[label(str(y), font_size=14, color=GREY_B).next_to(ax.c2p(0, y), LEFT, buff=0.05)
                          for y in (0, 8, 16, 24)])
            out.add(VGroup(ax, line, lab, yt))
        out[0][2].shift(LEFT * 0.25)
        out[1][2].shift(LEFT * 0.25)
        xl = label(r"time, \ in service times; \ the height is the number of jobs waiting or in service", font_size=18,
                   color=GREY_A).next_to(out, DOWN, buff=0.2)
        line = label(r"at 0.9 the walk drifts down only slowly; \ every burst of arrivals takes a long time to drain",
                     font_size=21, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why so steep? Watch the number of jobs in the system over time. It is a random walk: up one at each "
            "arrival, down one at each completion, and it cannot go below zero. <bookmark mark='a'/> At fifty "
            "percent load the walk is pulled firmly down, and bursts of arrivals drain away quickly. <bookmark "
            "mark='b'/> At ninety percent the pull is weak. A burst builds a queue of fifteen or twenty, and it "
            "takes a long time to drain, so most jobs arrive to find a crowd. <bookmark mark='c'/> The averages hide "
            "this: the queue is usually short or very long, and it is the long stretches that people remember."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(out[0][0]), FadeIn(out[0][2]), FadeIn(out[0][3]), Create(out[0][1]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(out[1][0]), FadeIn(out[1][2]), FadeIn(out[1][3]), Create(out[1][1]), FadeIn(xl),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(line))
        self.wait(0.3)
        self.clear_scene()

    def variance(self):
        q = load("queue")
        head = label(r"Variance matters: \ Pollaczek--Khinchine", font_size=34).to_edge(UP, buff=0.3)
        pk = MathTex(r"W = E[S]\left(1 + \frac{\rho}{1 - \rho}\cdot\frac{1 + C^2}{2}\right)", font_size=42,
                     color=HEAD).next_to(head, DOWN, buff=0.5)
        pl = label(r"any service-time distribution, \ Poisson arrivals; \ $C^2$: \ the variance over the mean squared",
                   font_size=20, color=GREY_A).next_to(pk, DOWN, buff=0.2)
        rows = [[p["name"], f"{p['scv']:.0f}", f"{p['formula']:.2f}", f"{p['sim']:.2f}"] for p in q["pk"]]
        tab = grid_table([r"service times \ (mean 1)", r"$C^2$", r"formula", r"simulated"], rows,
                         widths=[4.0, 1.4, 2.0, 2.0], row_h=0.5, font_size=21, mono_cols=())
        tab.next_to(pl, DOWN, buff=0.45)
        lines = VGroup(
            label(r"same load \ (0.8), \ same mean: \ the variable server is \textbf{nearly eight times} slower than the "
                  r"steady one", font_size=21, color=NO),
            label(r"a few huge jobs make everyone behind them wait: \ the convoy effect of chapter 7, \ in "
                  r"probability", font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Exponential service times are a convenient assumption. Felix Pollaczek and Aleksandr Khinchine found the "
            "mean response time for any distribution of service times. <bookmark mark='a'/> It depends on the "
            "variance, through the squared coefficient of variation, C squared. <bookmark mark='b'/> At eighty "
            "percent load, with mean service time one: if every job takes exactly one, the mean response is three. "
            "With exponential times, five. With a mix of many short jobs and a few long ones, twenty-three. "
            "<bookmark mark='c'/> Same load, same mean, and the variable server is nearly eight times slower than "
            "the steady one. <bookmark mark='d'/> The few long jobs block everyone behind them: the convoy effect "
            "from chapter seven, now as a formula."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pk))
            vo.wait_until("a")
            self.play(FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def srpt(self):
        q = load("queue")
        head = label(r"The order matters too", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r["name"], f"{r['fcfs']:.2f}", f"{r['ps']:.2f}", f"{r['srpt']:.2f}"] for r in q["disc"]]
        tab = grid_table([r"load 0.8, \ mean size 1", r"FCFS", r"processor sharing", r"SRPT"], rows,
                         widths=[3.8, 1.8, 3.2, 1.8], row_h=0.55, font_size=22, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6)
        for r in (1, 2):
            tab.cells[r][3].set_color(YES)
        tab.cells[2][1].set_color(NO)
        lines = VGroup(
            label(r"\textbf{processor sharing} \ (fine-grained round robin): \ $E[T] = E[S]/(1 - \rho)$, \ whatever the "
                  r"sizes", font_size=21, color=WHITE),
            label(r"\textbf{SRPT} \ (shortest remaining processing time) \ is optimal for the mean: \ Schrage, \ 1968",
                  font_size=21, color=YES),
            label(r"with heavy-tailed sizes, \ FCFS is 13 times worse than SRPT: \ the order matters as much as the "
                  r"speed", font_size=21, color=NO),
            label(r"fear of starving big jobs proved mostly unfounded: \ SRPT for web servers \ (Harchol-Balter et al., "
                  r"2003)", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "The order of service matters as much. Same load, same jobs, three disciplines. <bookmark mark='a'/> "
            "Processor sharing, round robin with a tiny quantum, has a remarkable property: its mean response time "
            "is the mean size over one minus rho, whatever the distribution of sizes. Variance does not hurt it. "
            "<bookmark mark='b'/> Shortest remaining processing time first is optimal, by chapter seven's exchange "
            "argument, as Schrage proved in 1968: two point three six against five, for exponential sizes. "
            "<bookmark mark='c'/> With heavy-tailed sizes, the kind measured for files, web pages and jobs in data "
            "centres, first come first served is thirteen times worse than SRPT. <bookmark mark='d'/> The usual worry "
            "is that big jobs starve. Mor Harchol-Balter and her colleagues showed that for web servers they "
            "barely suffer, and built a server that schedules its connections this way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.4), run_time=2.0)
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
