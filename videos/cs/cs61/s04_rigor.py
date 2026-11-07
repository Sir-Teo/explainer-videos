from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say(n) -> str:
    """A whole number as a speaker says it (British: 'nine hundred and seven')."""
    n = int(round(n))
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    return say(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + say(n % 1000))


def ms(seconds: float) -> str:
    return f"{say(seconds * 1000)} milliseconds"


T = load("timing")
TIMES = np.asarray(T["times"])
N = len(TIMES)
SD = float(TIMES.std(ddof=1))
M = load("means")
NARROW = T["narrowing"]


class Rigor(VoiceoverScene):
    def construct(self):
        self.card()
        self.runs()
        self.warmup()
        self.bootstrap()
        self.narrowing()
        self.means()

    def card(self):
        card = chapter_card(3, r"Measuring rigorously", r"How many runs, \ and how sure can you be?",
                            lit=(1979, 2007), extra=((1979, r"Efron: \ the bootstrap"),
                                                     (1986, r"Fleming and Wallace: \ geometric means"),
                                                     (2007, r"Georges, \ Buytaert and Eeckhout")), part=PART)
        with self.voiceover("Chapter three. Measuring rigorously."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def runs(self):
        head = label(r"One run is an anecdote", font_size=36).to_edge(UP, buff=0.3)
        lo, hi = 0.86, 0.97
        x0, x1, y0 = -6.2, 0.6, -1.6
        xp = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)  # noqa: E731
        base = Line([x0, y0, 0], [x1, y0, 0], color=GREY_C, stroke_width=1.5)
        xt = VGroup(*[label(rf"{v:.2f}", font_size=16, color=GREY_B).move_to([xp(v), y0 - 0.3, 0])
                      for v in (0.86, 0.88, 0.90, 0.92, 0.94, 0.96)])
        xl = label(r"seconds per run of the Job, \ in Python", font_size=18, color=GREY_A).next_to(xt, DOWN,
                                                                                                   buff=0.15)
        bins = np.floor((TIMES - lo) / 0.005).astype(int)
        seen: dict[int, int] = {}
        dots = VGroup()
        for b in bins:
            k = seen.get(b, 0)
            seen[b] = k + 1
            dots.add(Dot([xp(lo + (b + 0.5) * 0.005), y0 + 0.17 + 0.3 * k, 0], radius=0.12, color=DATA))
        tops = y0 + 0.3 * max(seen.values()) + 0.4

        def mark(v, color, text):
            ln = DashedLine([xp(v), y0, 0], [xp(v), tops, 0], color=color, stroke_width=2.5)
            return VGroup(ln, label(text, font_size=17, color=color).next_to(ln, UP, buff=0.08))
        best = mark(TIMES.min(), YES, rf"best: \ {TIMES.min():.3f}")
        mean = mark(TIMES.mean(), HEAD, rf"mean: \ {TIMES.mean():.3f}")
        worst = mark(TIMES.max(), NO, rf"worst: \ {TIMES.max():.3f}")
        mean[1].shift(UP * 0.4)
        notes = VGroup(
            wrapped_label(rf"{N} runs of the same program on the same {T['bytes'] / 1e6:.0f} million characters: "
                          rf"\ the slowest is {100 * (TIMES.max() / TIMES.min() - 1):.0f}\% slower than the fastest",
                          5.6, font_size=19, color=WHITE),
            wrapped_label(r"Georges, \ Buytaert and Eeckhout \ (OOPSLA 2007) \ surveyed Java performance papers: \ "
                          r"many reported one number \ (the best run, \ or a mean) \ with no measure of its "
                          r"uncertainty", 5.6, font_size=19, color=GREY_A),
            wrapped_label(r"they showed this can mislead, \ and asked for repeated runs and confidence intervals",
                          5.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.0, 0.3, 0])
        with self.voiceover(
            f"We ran the Job in plain Python {say(N)} times on the same text, about "
            f"{say(T['bytes'] / 1e6)} million characters. <bookmark mark='a'/> Each dot is one run. Nothing "
            "changed between them, and still they spread out. <bookmark mark='b'/> Report the best run and you "
            f"claim {ms(TIMES.min())}; report the worst and you claim {ms(TIMES.max())}, "
            f"{say(100 * (TIMES.max() / TIMES.min() - 1))} percent slower; the mean is {ms(TIMES.mean())}. "
            "<bookmark mark='c'/> In 2007 Andy Georges, Dries Buytaert and Lieven Eeckhout surveyed how Java "
            "performance papers reported their timings, and found many gave a single number, the best of several "
            "runs or a mean, with no measure of how uncertain it was. <bookmark mark='d'/> They showed that such "
            "methods can mislead, even about which of two systems is faster, and argued for repeated runs and "
            "confidence intervals instead."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(xt), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in dots], lag_ratio=0.08), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(best), FadeIn(worst))
            self.play(FadeIn(mean), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def warmup(self):
        head = label(r"Warm-up, \ and the steady state", font_size=36).to_edge(UP, buff=0.3)
        # left: a just-in-time runtime warming up (illustrative)
        ax1 = Axes(x_range=[0, 20, 5], y_range=[0, 3, 1], x_length=5.4, y_length=3.2,
                   axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False,
                                "include_tip": False}).move_to([-3.6, 0.2, 0])
        rng = np.random.default_rng(5)
        warm = [1.0 + 1.7 * np.exp(-(i - 1) / 2.2) + rng.normal(0, 0.05) for i in range(1, 21)]
        wd = VGroup(*[Dot(ax1.c2p(i, v), radius=0.05, color=KERN) for i, v in enumerate(warm, 1)])
        wl = VMobject(color=KERN, stroke_width=1.6).set_points_as_corners([d.get_center() for d in wd])
        split = DashedLine(ax1.c2p(6.5, 0), ax1.c2p(6.5, 3), color=GREY_B, stroke_width=2)
        su = label(r"start-up", font_size=17, color=KERN).next_to(ax1.c2p(3.4, 3), DOWN, buff=0.3)
        ss = label(r"steady state", font_size=17, color=YES).next_to(ax1.c2p(13, 3), DOWN, buff=0.3)
        a1x = label(r"iteration, \ within one run of the runtime", font_size=17, color=GREY_A).next_to(ax1, DOWN,
                                                                                                       buff=0.15)
        a1y = label(r"time per iteration", font_size=17, color=GREY_A).next_to(ax1, UP, buff=0.12).align_to(ax1,
                                                                                                           LEFT)
        ill = note(r"illustrative: \ a JIT-compiled runtime \ (Part 15)", font_size=16).next_to(a1x, DOWN, buff=0.12)
        # right: our runs in order
        lo, hi = 0.85, 0.98
        ax2 = Axes(x_range=[0, N + 1, 5], y_range=[lo, hi, 0.05], x_length=5.4, y_length=3.2,
                   axis_config={"color": GREY_D, "include_numbers": False, "include_tip": False}).move_to([3.4, 0.2, 0])
        jd = VGroup(*[Dot(ax2.c2p(i, v), radius=0.05, color=DATA) for i, v in enumerate(TIMES, 1)])
        jl = VMobject(color=DATA, stroke_width=1.4).set_points_as_corners([d.get_center() for d in jd])
        xt2 = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax2.c2p(v, lo), DOWN, buff=0.1)
                       for v in (1, 10, 20, 30)])
        yt2 = VGroup(*[label(rf"{v:.2f}", font_size=16, color=GREY_B).next_to(ax2.c2p(0, v), LEFT, buff=0.1)
                       for v in (0.87, 0.92, 0.97)])
        a2x = label(r"run of the Job", font_size=17, color=GREY_A).next_to(xt2, DOWN, buff=0.1)
        a2y = label(r"seconds, \ measured here", font_size=17, color=GREY_A).next_to(ax2, UP, buff=0.12).align_to(
            yt2, LEFT)
        slow = int(np.argmax(TIMES)) + 1
        ring = Circle(radius=0.14, color=NO, stroke_width=2.5).move_to(jd[slow - 1])
        foot = wrapped_label(rf"no trend: \ this Python has no JIT; \ the slowest run is number {slow}", 12.4,
                             font_size=19, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Georges and his colleagues also separated two questions. <bookmark mark='a'/> A runtime with a "
            "just-in-time compiler, like Part 15's, starts slowly, interpreting, and speeds up as it compiles the "
            "hot code. Start-up performance is the time of the first iterations: to measure it, start the "
            "runtime many times and time the first iteration of each. <bookmark mark='b'/> Steady-state "
            "performance is the time after warm-up: within each run, iterate until the timings settle, average "
            "those, and still repeat across several fresh runs, because each run can compile the code a little "
            "differently. <bookmark mark='c'/> Our Job, in order. The Python we use has no just-in-time compiler, "
            f"and the times show no trend: the slowest is run number {say(slow)}. Warm-up is not the story here; "
            "the machine's own noise is."
        ) as vo:
            self.play(FadeIn(head), Create(ax1), FadeIn(a1x), FadeIn(a1y), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(wl), LaggedStart(*[FadeIn(d) for d in wd], lag_ratio=0.1), run_time=2.5)
            self.play(Create(split), FadeIn(su))
            vo.wait_until("b")
            self.play(FadeIn(ss), Indicate(VGroup(*wd[7:]), color=YES))
            vo.wait_until("c")
            self.play(Create(ax2), FadeIn(xt2), FadeIn(yt2), FadeIn(a2x), FadeIn(a2y))
            self.play(Create(jl), LaggedStart(*[FadeIn(d) for d in jd], lag_ratio=0.05), run_time=2.5)
            self.play(Create(ring), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def bootstrap(self):
        head = label(r"The bootstrap", font_size=36).to_edge(UP, buff=0.3)
        lo, hi = 0.86, 0.97
        x0, x1 = -6.3, 0.2
        xp = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)  # noqa: E731
        ys, yr = 2.1, 0.75
        line_s = Line([x0, ys, 0], [x1, ys, 0], color=GREY_C, stroke_width=1.2)
        line_r = Line([x0, yr, 0], [x1, yr, 0], color=GREY_C, stroke_width=1.2)
        ls = label(rf"our {N} runs", font_size=17, color=DATA).next_to(line_s, UP, buff=0.18).align_to(line_s, LEFT)
        lr = label(r"one resample", font_size=17, color=HEAD).next_to(line_r, DOWN, buff=0.1).align_to(line_r, LEFT)
        st = VGroup(*[label(rf"{v:.2f}", font_size=16, color=GREY_B).next_to([xp(v), ys, 0], DOWN, buff=0.08)
                      for v in (0.87, 0.92, 0.97)])
        sample = VGroup(*[Dot([xp(v), ys, 0], radius=0.06, color=DATA) for v in TIMES])
        rng = np.random.default_rng(1)

        def resample():
            idx = rng.integers(0, N, N)
            cnt: dict[int, int] = {}
            g = VGroup()
            for i in idx:
                k = cnt.get(int(i), 0)
                cnt[int(i)] = k + 1
                g.add(Dot([xp(TIMES[i]), yr + 0.13 * k, 0], radius=0.05, color=HEAD))
            return g, float(TIMES[idx].mean())
        # the histogram of resampled means, on its own (narrower) scale
        mlo, mhi = 0.885, 0.93
        hx0, hx1, hy0 = -6.3, 0.2, -2.55
        hp = lambda v: hx0 + (v - mlo) / (mhi - mlo) * (hx1 - hx0)  # noqa: E731
        boots = TIMES[rng.integers(0, N, (4000, N))].mean(axis=1)
        cnt, edges = np.histogram(boots, bins=36, range=(mlo, mhi))
        bw = (hx1 - hx0) / 36
        bars = VGroup(*[Rectangle(width=bw - 0.02, height=max(0.01, 1.9 * c / cnt.max()), stroke_width=0,
                                  fill_color=HEAD, fill_opacity=0.75).move_to([hx0 + (i + 0.5) * bw, hy0, 0],
                                                                              aligned_edge=DOWN)
                        for i, c in enumerate(cnt)])
        hbase = Line([hx0, hy0, 0], [hx1, hy0, 0], color=GREY_C, stroke_width=1.2)
        ht = VGroup(*[label(rf"{v:.2f}", font_size=16, color=GREY_B).next_to([hp(v), hy0, 0], DOWN, buff=0.08)
                      for v in (0.89, 0.90, 0.91, 0.92, 0.93)])
        hl = label(r"mean of each resample", font_size=17, color=GREY_A).next_to(ht, DOWN, buff=0.06)
        clo, chi = T["ci_mean"]
        cil = VGroup(*[DashedLine([hp(v), hy0, 0], [hp(v), hy0 + 2.1, 0], color=YES, stroke_width=2.5)
                       for v in (clo, chi)])
        cit = label(rf"95\%: \ {clo:.3f} to {chi:.3f} s", font_size=19, color=YES).next_to(cil, UP, buff=0.08)
        rows = VGroup(
            MathTex(r"\bar x = \frac{1}{n}\sum_{i=1}^{n} x_i", font_size=32),
            MathTex(r"x^*_1, \dots, x^*_n", font_size=32, color=HEAD),
            MathTex(r"\bar x^*_1,\ \bar x^*_2,\ \dots,\ \bar x^*_B", font_size=32, color=HEAD),
            MathTex(r"\big[\, q_{2.5\%},\ q_{97.5\%} \,\big]", font_size=32, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to([3.4, 0.55, 0])
        whys = VGroup(
            label(r"the mean of the sample", font_size=17, color=GREY_B),
            label(r"$n$ draws from the sample, \ with replacement", font_size=17, color=GREY_B),
            label(r"repeat $B$ times: \ one mean each", font_size=17, color=GREY_B),
            label(r"the middle 95\% of those means", font_size=17, color=GREY_B),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        src = note(r"Efron, \ 1979", font_size=17).to_corner(DR, buff=0.35)
        r1, m1 = resample()
        r2, m2 = resample()
        r3, m3 = resample()
        with self.voiceover(
            "How sure is a mean? The textbook formula assumes the times follow a bell curve. The bootstrap, "
            "Bradley Efron's idea from 1979, assumes much less. <bookmark mark='a'/> Start with our "
            f"{say(N)} runs and their mean. <bookmark mark='b'/> Now treat the sample as if it were the whole "
            f"world: draw {say(N)} runs from it at random, with replacement, so that some appear twice and some "
            "not at all, and take the mean of that resample. <bookmark mark='c'/> Do it again, and again; each "
            "resample gives a slightly different mean. <bookmark mark='d'/> After thousands of resamples the "
            "means form a distribution, and its middle ninety-five percent is a ninety-five percent confidence "
            f"interval: here from {ms(clo)} to {ms(chi)}. The same recipe works for a median, or for the ratio of "
            "two programs' times, where no textbook formula is at hand."
        ) as vo:
            self.play(FadeIn(head), Create(line_s), FadeIn(ls), FadeIn(st), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in sample], lag_ratio=0.04), Write(rows[0]),
                      FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(Create(line_r), FadeIn(lr), FadeIn(rows[1]), FadeIn(whys[1]))
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.4) for d in r1], lag_ratio=0.04), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(hbase), FadeIn(ht), FadeIn(hl), FadeIn(rows[2]), FadeIn(whys[2]))
            for rs, nxt in ((r1, r2), (r2, r3)):
                self.play(ReplacementTransform(rs, nxt), run_time=0.9)
            self.play(FadeOut(r3), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(cil), FadeIn(cit), FadeIn(rows[3]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()
        _ = (m1, m2, m3)

    def narrowing(self):
        head = label(r"More runs, \ narrower intervals", font_size=36).to_edge(UP, buff=0.3)
        lo, hi = 0.86, 0.95
        k = len(NARROW)
        ax = Axes(x_range=[0, k + 1, 1], y_range=[lo, hi, 0.01], x_length=6.0, y_length=4.4,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False,
                               "include_tip": False}).move_to([-3.3, -0.25, 0])
        yt = VGroup(*[label(rf"{v:.2f}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0.87, 0.89, 0.91, 0.93)])
        yl = label(r"seconds", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(yt, LEFT)
        xt = VGroup(*[label(rf"{w['runs']}", font_size=17, color=GREY_B).next_to(ax.c2p(i + 1, lo), DOWN, buff=0.1)
                      for i, w in enumerate(NARROW)])
        xl = label(r"runs so far", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        bars, wl = VGroup(), VGroup()
        for i, w in enumerate(NARROW):
            seg = Line(ax.c2p(i + 1, w["lo"]), ax.c2p(i + 1, w["hi"]), color=YES, stroke_width=6)
            dot = Dot(ax.c2p(i + 1, w["mean"]), radius=0.07, color=HEAD)
            bars.add(VGroup(seg, dot))
            wl.add(label(rf"{1000 * (w['hi'] - w['lo']):.0f} ms", font_size=16, color=YES).move_to(
                ax.c2p(i + 1, lo + 0.004)))
        mean_all = float(TIMES.mean())
        pred = [(i + 1, 1.96 * SD / np.sqrt(w["runs"])) for i, w in enumerate(NARROW)]
        up = DashedVMobject(VMobject(stroke_width=2, color=GREY_A).set_points_as_corners(
            [ax.c2p(x, mean_all + h) for x, h in pred]), num_dashes=30)
        dn = DashedVMobject(VMobject(stroke_width=2, color=GREY_A).set_points_as_corners(
            [ax.c2p(x, mean_all - h) for x, h in pred]), num_dashes=30)
        pl = label(r"dashed: \ $\pm 1.96\,s/\sqrt{n}$, \ from all the runs", font_size=16, color=GREY_A).next_to(
            ax, DOWN, buff=0.75).align_to(ax, LEFT)
        cols = {r"\frac{\sigma}{\sqrt{n}}": HEAD, r"\frac{\sigma^2}{n}": HEAD}
        rows = VGroup(
            cmath(r"\operatorname{Var}(\bar x)", r"=", r"\frac{\sigma^2}{n}", colors=cols, font_size=34),
            cmath(r"\operatorname{sd}(\bar x)", r"=", r"\frac{\sigma}{\sqrt{n}}", colors=cols, font_size=34),
            cmath(r"\text{width}", r"\approx", r"2 \times 1.96", r"\times", r"\frac{\sigma}{\sqrt{n}}", colors=cols,
                  font_size=34),
            cmath(r"n \to 4n", r":", r"\text{width} \to \tfrac{1}{2}\,\text{width}", colors=cols, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62).move_to([3.6, 0.55, 0])
        whys = VGroup(
            label(r"independent runs: \ variances add, \ then divide by $n^2$", font_size=17, color=GREY_B),
            label(r"take the square root", font_size=17, color=GREY_B),
            label(r"a normal approximation, \ for many runs", font_size=17, color=GREY_B),
            label(r"four times the runs, \ half the width", font_size=17, color=GREY_B),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        drift = wrapped_label(rf"the centre drifts: \ {1000 * NARROW[0]['mean']:.0f} ms after {NARROW[0]['runs']} "
                              rf"runs, \ {1000 * NARROW[-1]['mean']:.0f} ms after {NARROW[-1]['runs']}", 5.8,
                              font_size=18, color=KERN).to_edge(DOWN, buff=0.3).align_to(rows, LEFT)
        w0, w1 = NARROW[0], NARROW[-1]
        with self.voiceover(
            "How many runs are enough? <bookmark mark='a'/> Here is the bootstrap interval after "
            + ", ".join(say(w["runs"]) for w in NARROW[:-1]) + f" and {say(w1['runs'])} of our runs. It narrows: "
            f"{say(1000 * (w0['hi'] - w0['lo']))} milliseconds wide after {say(w0['runs'])} runs, "
            f"{say(1000 * (w1['hi'] - w1['lo']))} after {say(w1['runs'])}. <bookmark mark='b'/> Why that rate? "
            "Independent runs have variances that add, so the variance of a mean of n runs is the variance of one "
            "run divided by n. <bookmark mark='c'/> Take the square root: the spread of the mean falls as one over "
            "the square root of n. <bookmark mark='d'/> The interval is about four of those wide, so to halve it "
            "you need four times the runs. The dashed lines are that prediction, and our intervals follow it. "
            "<bookmark mark='e'/> Notice, too, that the centre drifts. The formula assumes the machine does not "
            "change while you measure; a shared machine does, which is why we interleave settings, and why an "
            "interval is only as honest as that assumption."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(yl), FadeIn(xt), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(b[0]), FadeIn(b[1]), FadeIn(t))
                                    for b, t in zip(bars, wl)], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            self.play(Create(up), Create(dn), FadeIn(pl))
            vo.wait_until("e")
            self.play(FadeIn(drift), Indicate(VGroup(*[b[1] for b in bars]), color=KERN))
        self.wait(0.4)
        self.clear_scene()

    def means(self):
        head = label(r"Averaging speedups", font_size=36).to_edge(UP, buff=0.3)
        a, b = M["times_a"], M["times_b"]
        rba, rab = M["ratios_b_over_a"], [x / y for x, y in zip(a, b)]
        f = lambda v: f"{v:g}"  # noqa: E731
        rows = [[r"time on A", f"{f(a[0])} s", f"{f(a[1])} s", "", ""],
                [r"time on B", f"{f(b[0])} s", f"{f(b[1])} s", "", ""],
                [r"B / A", f(rba[0]), f(rba[1]), f(M["arith_b_over_a"]), f(M["geo_b_over_a"])],
                [r"A / B", f(rab[0]), f(rab[1]), f(M["arith_a_over_b"]), f(M["geo_a_over_b"])]]
        tab = grid_table([r"", r"benchmark 1", r"benchmark 2", r"arithmetic mean", r"geometric mean"], rows,
                         widths=[2.0, 2.2, 2.2, 2.7, 2.7], row_h=0.48, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        for r in (3, 4):
            tab.cells[r][3].set_color(NO)
            tab.cells[r][4].set_color(YES)
        ill = note(r"illustrative times", font_size=16).next_to(tab, DOWN, buff=0.08).align_to(tab, RIGHT)
        body = VGroup(*[tab.cells[r][c] for r in range(5) for c in range(3)], tab.rule)
        arith = VGroup(tab.cells[0][3], tab.cells[3][3], tab.cells[4][3])
        geo = VGroup(tab.cells[0][4], tab.cells[3][4], tab.cells[4][4])
        clash = label(r"each says the other is a quarter slower", font_size=19, color=NO).next_to(
            ill, DOWN, buff=0.1).align_to(tab.cells[0][3], LEFT)
        cols = {r"G(r)": YES, r"\frac{1}{G(r)}": YES}
        r0 = cmath(r"G(r)", r"=", r"\Big(\prod_{i=1}^{n} r_i\Big)^{1/n}", colors=cols, font_size=32)
        r1 = cmath(r"G(1/r)", r"=", r"\Big(\prod_{i=1}^{n} \frac{1}{r_i}\Big)^{1/n}", r"=", r"\frac{1}{G(r)}",
                   colors=cols, font_size=32)
        r2 = cmath(r"\log G(r)", r"=", r"\frac{1}{n}\sum_{i=1}^{n} \log r_i", colors=cols, font_size=32)
        r3 = cmath(r"\sqrt{2 \times 0.5}", r"=", r"1", colors=cols, font_size=32)
        der = VGroup(r0, r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(LEFT, buff=0.6).to_edge(
            DOWN, buff=0.3)
        whys = VGroup(
            label(r"the $n$-th root of the product", font_size=17, color=GREY_B),
            label(r"flip every ratio, \ and the mean flips: \ any reference machine", font_size=17, color=GREY_B),
            label(r"an ordinary mean of logarithms: \ $\log 2 + \log \tfrac12 = 0$", font_size=17, color=GREY_B),
            label(r"a tie, \ whichever way round", font_size=17, color=GREY_B),
        )
        for w, r in zip(whys, der):
            w.next_to(r, RIGHT, buff=0.35)
        whys.align_to(VGroup(*[w for w in whys]), LEFT)
        for w in whys:
            w.set_x(w.get_width() / 2 + max(r.get_right()[0] for r in der) + 0.35)
        total = wrapped_label(rf"but run both once each: \ A takes {f(sum(a))} s, \ B takes {f(sum(b))} s; \ for a "
                              r"fixed workload, \ total time is the honest summary", 3.6, font_size=18,
                              color=KERN).to_edge(RIGHT, buff=0.35).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Last, how to average speedups. <bookmark mark='a'/> Two programs on two benchmarks: A takes one "
            "second on the first and four on the second; B takes two on each. <bookmark mark='b'/> Divide B's "
            "times by A's and average: one and a quarter, so B is a quarter slower. Divide A's by B's instead and "
            "average: also one and a quarter, so A is a quarter slower. Both cannot be true. "
            "<bookmark mark='c'/> The geometric mean is the n-th root of the product of the ratios. "
            "<bookmark mark='d'/> Flip every ratio and it flips exactly, so it gives the same verdict whichever "
            "way round you divide, and whichever machine you normalize to. <bookmark mark='e'/> In logarithms it "
            "is an ordinary mean, where twice as fast and twice as slow cancel. Here it says one: a tie. Philip "
            "Fleming and John Wallace made this argument in 1986. <bookmark mark='f'/> But see what it does not "
            "say: run both benchmarks once each, and B finishes in four seconds, A in five. For a fixed workload, "
            "total time is the honest summary."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*[tab.cells[r][c] for r in range(3) for c in range(3)])),
                      FadeIn(tab.rule), FadeIn(ill))
            vo.wait_until("a")
            self.play(Indicate(VGroup(*tab.cells[1][1:3], *tab.cells[2][1:3]), color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[3][:3])), FadeIn(tab.cells[0][3]), FadeIn(tab.cells[3][3]))
            self.play(FadeIn(VGroup(*tab.cells[4][:3])), FadeIn(tab.cells[4][3]), FadeIn(clash))
            vo.wait_until("c")
            self.play(Write(r0), FadeIn(whys[0]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(r0.copy(), r1), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(r0.copy(), r2), FadeIn(whys[2]))
            self.play(FadeIn(r3), FadeIn(whys[3]), FadeIn(geo))
            vo.wait_until("f")
            self.play(FadeIn(total))
        self.wait(0.4)
        self.clear_scene()
        _ = (body, arith)


_ = (BG, DATA, LAM)
