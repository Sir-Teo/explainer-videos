from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403

BUS = S.ACCENT


class Process(VoiceoverScene, TreeMixin):
    def construct(self):
        self.card()
        self.buses()
        self.gaps()
        self.merge_thin()
        self.paradox()
        self.tree_voiceover("Three arrows: <bookmark mark='t'/> the gaps of a Poisson process are exponential; sums "
                            "of exponential gaps are gamma; and the geometric, shrunk to infinitely many tiny trials, "
                            "becomes the exponential.", 5)

    def card(self):
        card = chapter_card(5, r"Continuous time", r"Buses at random, \ and why you always seem to wait longer",
                            lit=(1898,), part=PART)
        with self.voiceover("Chapter five. Continuous time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def buses(self):
        d = load("process")
        times = np.asarray(d["times"])
        times = times[times < 180]
        line = NumberLine(x_range=[0, 180, 30], length=12.4, include_numbers=False, color=GREY_C).move_to([0, 2.2, 0])
        ticks = VGroup(*[MathTex(f"{t}", font_size=20, color=GREY_B).next_to(line.n2p(t), DOWN, buff=0.15)
                         for t in range(0, 181, 30)])
        tl = label(r"minutes", font_size=20, color=GREY_B).next_to(line, DOWN, buff=0.5)
        marks = VGroup(*[Line(line.n2p(t) + DOWN * 0.18, line.n2p(t) + UP * 0.18, color=BUS, stroke_width=4)
                         for t in times])
        hours = VGroup(*[DashedLine(line.n2p(h) + DOWN * 0.3, line.n2p(h) + UP * 0.3, color=GREY_D, stroke_width=1.5)
                         for h in (60, 120)])
        dfn = definition_card(r"Poisson process (rate $\lambda$)", r"events at random times: \ in any interval of "
                              r"length $t$ the count is Poisson$(\lambda t)$, \ and counts in disjoint intervals are "
                              r"independent", color=DISC, width=6.4, font_size=23).move_to([-3.2, -1.0, 0])
        per = np.asarray(d["per_hour"])
        A = axes([-0.6, 16.6], [0, 0.18], x_length=5.2, y_length=2.8, xlabel=r"buses in an hour",
                 xticks=[0, 4, 8, 12, 16], center=[3.6, -1.3, 0])
        A.ax.y_axis.set_opacity(0)
        emp = np.bincount(per, minlength=17)[:17] / len(per)
        from scipy import stats as st
        bars = pmf_bars(A.ax, range(17), emp, SIM, width=0.65)
        dots = pmf_dots(A.ax, range(17), st.poisson.pmf(range(17), 6), EXACT, radius=0.05)
        mv = MathTex(rf"\text{{mean }} {d['per_hour_mean']:.2f},\ \text{{variance }} {d['per_hour_var']:.2f}",
                     font_size=24, color=SIM).next_to(A, UP, buff=0.15)
        with self.voiceover(
            "Now let rare events happen in continuous time. <bookmark mark='a'/> Buses that run without a timetable, "
            "on average one every ten minutes, arriving at random. <bookmark mark='b'/> Chop time into tiny slices; "
            "in each, a bus arrives with a tiny probability, independently. By the law of rare events, the number "
            "in any hour is Poisson, with mean six. That's the Poisson process. <bookmark mark='c'/> Two thousand "
            "simulated hours agree: mean and variance both about six, and the Poisson shape."
        ) as vo:
            self.play(Create(line), FadeIn(ticks), FadeIn(tl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(hours), FadeIn(dfn))
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(bars), FadeIn(dots), FadeIn(mv))
        self.line, self.marks, self.ticks, self.tl, self.times = line, marks, ticks, tl, times
        self.play(FadeOut(VGroup(dfn, A, bars, dots, mv, hours)))

    def gaps(self):
        d = load("process")
        rows = [
            cmath(r"P(\text{gap} > t)", r"=", r"P(\text{no bus in } (0, t])", r"=", r"e^{-\lambda t}", font_size=34),
            cmath(r"f(t)", r"=", r"\lambda e^{-\lambda t}", r",\quad", r"E(\text{gap}) = \frac1\lambda = 10", font_size=34),
        ]
        rows[1][0].set_color(CONT)
        whys = [why(r"Poisson$(\lambda t)$ at $0$"), why(r"the exponential: \ memoryless, \ like the geometric")]
        A = axes([0, 60], [0, 0.11], x_length=5.6, y_length=2.2, xlabel=r"minutes", xticks=[0, 10, 20, 30, 40, 50, 60],
                 center=[-3.4, -2.55, 0])
        A.ax.y_axis.set_opacity(0)
        xs = np.linspace(0, 60, 200)
        gaps = np.asarray(d["gaps_sample"])
        edges = np.linspace(0, 60, 31)
        h = hist_bars(A.ax, edges, np.histogram(gaps, edges)[0] / (len(gaps) * np.diff(edges)), color=SIM, opacity=0.6)
        cv = curve(A.ax, xs, np.exp(-xs / 10) / 10, EXACT, 3)
        al = label(r"gaps between buses", font_size=22, color=GREY_A).next_to(A, UP, buff=0.1)
        B = axes([0, 80], [0, 0.03], x_length=5.6, y_length=2.2, xlabel=r"minutes until the third bus",
                 xticks=[0, 20, 40, 60, 80], center=[3.4, -2.55, 0])
        B.ax.y_axis.set_opacity(0)
        third = np.asarray(d["third"])
        e2 = np.linspace(0, 80, 41)
        h2 = hist_bars(B.ax, e2, np.histogram(third, e2)[0] / (len(third) * np.diff(e2)), color=SIM, opacity=0.6)
        g = curve(B.ax, np.linspace(0, 80, 200), [t ** 2 * np.exp(-t / 10) / (2 * 10 ** 3) for t in np.linspace(0, 80, 200)],
                  EXACT, 3)
        gl = MathTex(r"\text{gamma: } \frac{\lambda^k t^{k-1} e^{-\lambda t}}{(k-1)!}", font_size=24, color=EXACT)
        gl.next_to(B, UP, buff=0.1)
        with self.voiceover(
            "What about the gaps between buses? <bookmark mark='a'/> The gap after a bus is longer than t exactly "
            "when no bus comes in the next t minutes, and the Poisson count for that interval is zero with "
            "probability e to the minus lambda t. <bookmark mark='b'/> So the gaps are exponential, with mean ten "
            "minutes. The exponential is the continuous geometric, and it's memoryless too: having waited five "
            "minutes, you can expect to wait ten more. <bookmark mark='c'/> The time until the third bus is a sum "
            "of three independent gaps, and its distribution is the gamma. Simulated gaps and waits, blue, match "
            "the formulas, gold."
        ) as vo:
            self.play(self.line.animate.shift(UP * 0.6), self.marks.animate.shift(UP * 0.6),
                      self.ticks.animate.shift(UP * 0.6), FadeOut(self.tl))
            step = ladder(self, rows, whys, keep=2, top=2.0, x=0.2, buff=0.35)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            self.play(FadeIn(A), FadeIn(h), Create(cv), FadeIn(al))
            vo.wait_until("c")
            self.play(FadeIn(B), FadeIn(h2), Create(g), FadeIn(gl))
        self.clear_scene()

    def merge_thin(self):
        d = load("process")
        a, b = np.asarray(d["a_sample"]), np.asarray(d["b_sample"])
        rowsy = [1.9, 1.0, 0.1]
        lines = VGroup(*[NumberLine(x_range=[0, 120, 20], length=9.6, include_numbers=False, color=GREY_C)
                         .move_to([1.4, y, 0]) for y in rowsy])
        names = VGroup(label(r"route A: \ every 10 min", font_size=22, color=S.EST),
                       label(r"route B: \ every 15 min", font_size=22, color=S.LIK),
                       label(r"either", font_size=22, color=S.ACCENT))
        for n_, ln in zip(names, lines):
            n_.next_to(ln, LEFT, buff=0.25)
        ma = VGroup(*[Line(lines[0].n2p(t) + DOWN * 0.15, lines[0].n2p(t) + UP * 0.15, color=S.EST, stroke_width=4) for t in a])
        mb = VGroup(*[Line(lines[1].n2p(t) + DOWN * 0.15, lines[1].n2p(t) + UP * 0.15, color=S.LIK, stroke_width=4) for t in b])
        mm = VGroup(*[Line(lines[2].n2p(t) + DOWN * 0.15, lines[2].n2p(t) + UP * 0.15,
                           color=S.EST if t in set(a) else S.LIK, stroke_width=4) for t in np.sort(np.r_[a, b])])
        rows = VGroup(
            MathTex(r"\text{superposition: }\ \lambda_A + \lambda_B = \tfrac1{10} + \tfrac1{15} = \tfrac16", r"\quad",
                    rf"\text{{simulated mean gap }} {d['merged_gap']:.2f}", font_size=28),
            MathTex(r"\text{thinning: keep each bus w.p. } 0.6\ \Rightarrow\ \text{rate } \tfrac{0.6}{10}", r"\quad",
                    rf"\text{{simulated mean gap }} {d['room_gap']:.2f}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -1.9, 0])
        for r in rows:
            r[2].set_color(SIM)
            if r.width > 13:
                r.width = 13
        why_ = label(r"both follow from the law of rare events: \ rare chances add, \ and a random subset of rare chances "
                     r"is still rare", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3)
        if why_.width > 13:
            why_.width = 13
        intro = label('Combining and thinning processes', font_size=36)
        with self.voiceover(
            "Poisson processes combine beautifully. <bookmark mark='a'/> Two independent bus routes stop at the same "
            "corner, one every ten minutes on average and one every fifteen, each a Poisson process. "
            "<bookmark mark='b'/> Watch for either bus, and the arrivals merge into one Poisson process whose rate "
            "is the sum: a tenth plus a fifteenth, one bus every six minutes. <bookmark mark='c'/> Run it the other "
            "way: if each bus has room for you with probability point six, independently, the buses with room "
            "form a Poisson process too, with the rate multiplied by point six. <bookmark mark='d'/> Superposition "
            "and thinning, and simulation confirms both: mean gaps of six minutes and sixteen and two thirds."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(names[:2]), FadeIn(ma), FadeIn(mb))
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(names[2]), TransformFromCopy(VGroup(ma, mb), mm), run_time=2.0)
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(why_))
        self.clear_scene()

    def paradox(self):
        d = load("process")
        g = np.random.Generator(np.random.PCG64(11))
        times = np.cumsum(g.exponential(10, 30))
        times = times[times < 120]
        line = NumberLine(x_range=[0, 120, 20], length=12.4, include_numbers=False, color=GREY_C).move_to([0, 1.8, 0])
        marks = VGroup(*[Line(line.n2p(t) + DOWN * 0.2, line.n2p(t) + UP * 0.2, color=BUS, stroke_width=4) for t in times])
        bounds = np.r_[0, times]
        segs = VGroup()
        for a, b in zip(bounds[:-1], bounds[1:]):
            segs.add(Line(line.n2p(a), line.n2p(b), stroke_width=10, color=interpolate_color(ManimColor("#2A3A4E"),
                                                                                             ManimColor(S.RESID),
                                                                                             min(1, (b - a) / 30))))
        pas = g.uniform(0, times[-1], 40)
        pdots = VGroup(*[Dot(line.n2p(p) + DOWN * 0.45, radius=0.05, color=WHITE) for p in pas])
        q = label(r"you arrive at a random moment. \ How long, on average, until the next bus?", font_size=28)
        q.to_edge(UP, buff=0.4)
        guess = label(r"the intuitive answer: \ half a gap, \ $5$ minutes", font_size=26, color=GREY_A).move_to([0, 0.2, 0])
        ans = VGroup(MathTex(rf"\text{{simulated wait: }} {d['wait_mean']:.2f} \text{{ minutes}}", font_size=32, color=SIM),
                     MathTex(rf"\text{{the gap you land in averages }} {d['seen_mean']:.2f}", font_size=32, color=S.RESID))
        ans.arrange(DOWN, buff=0.25).move_to([0, -1.2, 0])
        why_ = label(r"long gaps cover more time, \ so a random moment lands in them more often: \ length-biased "
                     r"sampling", font_size=24, color=S.ACCENT).to_edge(DOWN, buff=0.45)
        if why_.width > 13:
            why_.width = 13
        intro = label('Arriving at a random moment', font_size=36)
        with self.voiceover(
            "And now a paradox. <bookmark mark='a'/> You walk to the stop at a random moment. How long, on average, "
            "until the next bus? <bookmark mark='b'/> The gaps average ten minutes, so surely, landing somewhere in "
            "a gap, you wait half of one: five. <bookmark mark='c'/> Simulate it: twenty thousand passengers, "
            f"arriving at random. They wait {d['wait_mean']:.1f} minutes on average, not five. And the gap they "
            f"land in averages {d['seen_mean']:.0f} minutes, twice the average gap. <bookmark mark='d'/> Both facts "
            "have the same cause. Long gaps cover more of the clock, so a random moment is more likely to fall in a "
            "long one. And memorylessness says that from the moment you arrive, the wait is a fresh exponential, "
            "ten minutes on average. It's called the inspection paradox, and it's everywhere: the class sizes "
            "students report are bigger than the average class, and, on average, a randomly chosen person's friends have more friends than "
            "you."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(q), Create(line), FadeIn(segs), FadeIn(marks))
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in pdots], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(FadeIn(guess))
            vo.wait_until("c")
            self.play(FadeIn(ans, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(why_))
        self.clear_scene()
