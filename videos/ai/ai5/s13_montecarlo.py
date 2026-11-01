from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, PART, curve, load, normal_pdf
from videos.ai.ai5.plotting import clipped_curve

TAIL = C.SURPRISE


def set_dart_prefix(dots, count):
    """Show exactly the recorded prefix, including rewinds before the replay."""
    shown = min(max(int(count), 0), len(dots))
    previous = getattr(dots, "_visible_dart_count", None)
    if previous is None:
        for i, dot in enumerate(dots):
            dot.set_opacity(1 if i < shown else 0)
    elif shown != previous:
        for i in range(min(previous, shown), max(previous, shown)):
            dots[i].set_opacity(1 if i < shown else 0)
    dots._visible_dart_count = shown
    return dots


def estimate_comparison(estimate, truth):
    if not (math.isfinite(estimate) and math.isfinite(truth)) or truth <= 0 or estimate < 0:
        return "The estimate or its positive reference probability is unavailable."
    if estimate < truth:
        return f"The estimate is below the exact probability by {100 * (1 - estimate / truth):.1f} percent."
    if estimate > truth:
        return f"The estimate is above the exact probability by {100 * (estimate / truth - 1):.1f} percent."
    return "The estimate equals the exact probability."


def direct_estimate_summary(hits, n, estimate, truth):
    if hits == 0:
        return (f"No hits appeared in the {n:,} direct draws. Zero is the estimate, "
                "not a claim that the event is impossible.")
    comparison = estimate_comparison(estimate, truth)
    return f"The {n:,} direct draws contain {hits} hits. {comparison}"


def direct_rug_samples(samples, indices, n, hits):
    """Display only genuine positions, with every rare hit included exactly once."""
    z, selected = np.asarray(samples, float), np.asarray(indices, int)
    if z.ndim != 1 or len(z) != n or not np.isfinite(z).all():
        raise ValueError("direct samples do not match their declared finite cohort")
    expected = np.unique(np.r_[np.arange(min(400, n)), np.flatnonzero(z > 4)])
    if not np.array_equal(selected, expected) or int(np.count_nonzero(z > 4)) != hits:
        raise ValueError("rug indices or hit count do not match the recorded draws")
    shown = z[selected]
    return shown, np.flatnonzero(shown > 4)


class MonteCarlo(VoiceoverScene):
    def construct(self):
        self.card()
        self.origins()
        self.darts()
        self.rate()
        self.rare()
        self.ess()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"Answers from random samples", r"Can dice compute $\pi$?", part=PART)
        with self.voiceover("Chapter eleven. Monte Carlo."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def darts(self):
        d = load("montecarlo")
        pts, inside, est = np.asarray(d["pts"]), np.asarray(d["inside"], bool), np.asarray(d["est"])
        N = int(d["N"])
        c, R = np.array([-3.7, -0.3, 0]), 2.5
        sq = Square(2 * R, color=GREY_B, stroke_width=2).move_to(c)
        circ = Circle(radius=R, color=DATA, stroke_width=3).move_to(c)
        dots = VGroup(*[Dot(c + R * np.array([p[0], p[1], 0]), radius=0.03, color=DATA if i else GREY_C)
                        for p, i in zip(pts, inside)])
        ax = Axes(x_range=[0, math.log10(N), 1], y_range=[2.6, 3.7, 0.5], x_length=5.4, y_length=3.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.4, 0.0, 0])
        xl = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 2.6), DOWN, buff=0.18)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3))])
        xn = label(r"darts thrown", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.5)
        yl = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.16)
                      for v in (2.6, 3.7)])
        zoom_note = label(r"vertical zoom: $[2.6,3.7]$ \\ triangles: estimates outside this window",
                          font_size=18, color=GREY_A).next_to(ax, UP, buff=0.15)
        pi_l = DashedLine(ax.c2p(0, math.pi), ax.c2p(math.log10(N), math.pi), color=WHITE, stroke_width=2)
        pi_t = MathTex(r"\pi", font_size=34).next_to(pi_l, RIGHT, buff=0.1)
        ns = np.unique(np.round(np.logspace(0, math.log10(N), 300)).astype(int))
        band_hi = [ax.c2p(math.log10(n), min(math.pi + 1.64 / math.sqrt(n), 3.7)) for n in ns]
        band_lo = [ax.c2p(math.log10(n), max(math.pi - 1.64 / math.sqrt(n), 2.6)) for n in ns]
        band = Polygon(*band_hi, *band_lo[::-1], stroke_width=0, fill_color=DATA, fill_opacity=0.14)
        t = ValueTracker(0)
        set_dart_prefix(dots, 0)
        dots.add_updater(lambda m: set_dart_prefix(m, t.get_value()))

        def path():
            n = max(int(t.get_value()), 1)
            m = ns[ns <= n]
            return clipped_curve(ax, np.log10(m), est[m - 1], x_bounds=(0, math.log10(N)),
                                 y_bounds=(2.6, 3.7), color=C.BITS, stroke_width=3)

        def offscale():
            markers = VGroup()
            for k in ns[ns <= max(int(t.get_value()), 1)]:
                value = float(est[k - 1])
                if value < 2.6 or value > 3.7:
                    marker = Triangle(color=C.BITS, fill_opacity=1, stroke_width=0).scale(0.07)
                    if value < 2.6:
                        marker.rotate(PI)
                    marker.move_to(ax.c2p(math.log10(k), 3.7 if value > 3.7 else 2.6))
                    markers.add(marker)
            return markers

        trace = always_redraw(path)
        boundary_marks = always_redraw(offscale)
        ev = DecimalNumber(4.0, num_decimal_places=3, font_size=40, color=C.BITS)
        ev.add_updater(lambda m: m.set_value(est[max(int(t.get_value()), 1) - 1]))
        colors = {r"\pi": DATA}
        f = cmath(r"4 \times \frac{\text{inside}}{\text{all}}", r"\approx", r"\pi", colors=colors, font_size=40)
        VGroup(f, ev).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.35)
        why = label(r"the circle's share of the square: \ $\pi / 4$", font_size=26, color=GREY_A).next_to(sq, DOWN, buff=0.2)
        shown = len(dots)
        shown_tex = f"{shown:,}".replace(",", "{,}")
        cohort_note = label(rf"square: first $\min(N,{shown_tex})$ darts \\ estimate and curve: all $N$ darts",
                            font_size=18, color=GREY_A).next_to(why, DOWN, buff=0.12)
        count_value = Integer(1, font_size=24, color=C.BITS)
        count_value.add_updater(lambda m: m.set_value(max(int(t.get_value()), 1)))
        count_label = VGroup(MathTex("N=", font_size=24, color=GREY_A), count_value)
        count_label.arrange(RIGHT, buff=0.1).next_to(xn, DOWN, buff=0.12)
        with self.voiceover(
            "Here's a strange way to compute pi: throw darts at a square, completely at random. <bookmark mark='a'/> "
            "The share inside the circle is the circle's share of the area, pi over four, so four times that share "
            "estimates pi. <bookmark mark='b'/> Watch it as the darts pile up: it lurches, then homes in."
        ) as vo:
            self.play(Create(sq), Create(circ))
            self.add(dots)
            self.play(t.animate.set_value(24), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(why), Write(f))
            vo.wait_until("b")
            # Rewind the pictured cohort together with the graph's first estimate.
            t.set_value(1)
            dots.update(0)
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(zoom_note), FadeIn(xn), Create(pi_l), FadeIn(pi_t), FadeIn(ev),
                      FadeIn(cohort_note), FadeIn(count_label))
            self.add(trace, boundary_marks)
            self.play(t.animate.set_value(24), run_time=1.0, rate_func=linear)
            self.play(t.animate.set_value(N), run_time=6.0, rate_func=linear)
        with self.voiceover(
            rf"After four thousand darts: {est[-1]:.3f}. <bookmark mark='a'/> The shaded band is how far off a run "
            "like this typically is, and it narrows like one over the square root of the number of darts."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(band))
        trace.clear_updaters()
        boundary_marks.clear_updaters()
        ev.clear_updaters()
        dots.clear_updaters()
        count_value.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rate(self):
        d = load("montecarlo")
        Ns, rms, slope = np.asarray(d["Ns"], float), np.asarray(d["rms"]), float(d["slope"])
        ax = CornerAxes(x_range=[1, 5, 1], y_range=[-3, 0, 1], x_length=7.0, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.5, 0])
        xl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=24, color=GREY_B).next_to(ax.c2p(v, -3), DOWN, buff=0.12)
                      for v in range(1, 6)])
        yl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=24, color=GREY_B).next_to(ax.c2p(1, v), LEFT, buff=0.12)
                      for v in range(-3, 1)])
        xn = label(r"darts", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.55)
        x10 = VGroup(*[label(r"$\times 10$", font_size=18, color=GREY_C).move_to([ax.c2p(v + 0.5, -3)[0], xl[0].get_y(), 0])
                       for v in range(1, 5)])
        yn = label(r"typical error", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(math.log10(n), math.log10(r)), radius=0.07, color=C.BITS) for n, r in zip(Ns, rms)])
        b = np.polyfit(np.log10(Ns), np.log10(rms), 1)
        fit = Line(ax.c2p(1, b[1] + b[0]), ax.c2p(5, b[1] + 5 * b[0]), color=WHITE, stroke_width=2.5)
        sl = label(rf"slope ${slope:.2f}$", font_size=30, color=WHITE).next_to(fit.point_from_proportion(0.55), UR, buff=0.15)
        colors = {r"\sigma": MODEL, r"N": DATA}
        f = cmath(r"\text{error}", r"\approx", r"\frac{\sigma}{\sqrt{N}}", colors=colors, font_size=48).move_to([4.7, 1.6, 0])
        notes = VGroup(label(r"one more digit: \ $100\times$ the samples", font_size=28, color=C.BITS),
                       label(r"the same rate in a million dimensions", font_size=28, color=GREY_A))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(f, DOWN, buff=0.5).set_x(4.4)
        cite_ = cite(r"N.~Metropolis \& S.~Ulam, \textit{The Monte Carlo Method} (1949)", corner=DR)
        with self.voiceover(
            "Repeat the experiment many times at each size and measure the typical error. On log scales it falls on a "
            f"line of slope {slope:.2f}. <bookmark mark='a'/> The error shrinks like one over the square root of the "
            "number of samples: each extra digit costs a hundred times more. <bookmark mark='b'/> That's slow, but "
            "the rate doesn't care about dimension: it is the same in a million dimensions, where any grid would be "
            "hopeless."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(x10), FadeIn(yl), FadeIn(xn), FadeIn(yn))
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in dots], lag_ratio=0.15), run_time=1.5)
            self.play(Create(fit), FadeIn(sl))
            vo.wait_until("a")
            self.play(Write(f))
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rare(self):
        d = load("montecarlo")
        true, plain, hits, is_est = float(d["true"]), float(d["plain_est"]), int(d["plain_hits"]), float(d["is_est"])
        n = int(d["n"])
        ax = Axes(x_range=[-4, 8, 1], y_range=[0, 0.45, 0.1], x_length=11.0, y_length=2.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([0, 0, 0])
        xs = np.linspace(-4, 8, 300)
        p = curve(ax, xs, normal_pdf(xs), color=DATA, stroke_width=4)
        q = curve(ax, xs, normal_pdf(xs, 4.0), color=MODEL, stroke_width=4)
        pl = MathTex(r"p", font_size=40, color=DATA).next_to(ax.c2p(-1.2, normal_pdf(-1.2)), UL, buff=0.1)
        ql = MathTex(r"q", font_size=40, color=MODEL).next_to(ax.c2p(5.2, normal_pdf(1.2)), UR, buff=0.1)
        x4 = ax.c2p(4, 0)
        edge = DashedLine(x4, x4 + UP * 3.0, color=TAIL, stroke_width=2.5)
        tail_l = label(r"above $4$", font_size=26, color=TAIL).next_to(edge.get_end(), RIGHT, buff=0.12)
        zs, hit_positions = direct_rug_samples(d["plain_z"], d["plain_plot_indices"], n, hits)
        rug_p = VGroup(*[Line(ax.c2p(z, 0) + DOWN * 0.12, ax.c2p(z, 0) + DOWN * 0.32,
                              color=TAIL if z > 4 else DATA, stroke_width=2.5 if z > 4 else 1.2) for z in zs])
        ys = np.asarray(d["is_y"])
        rug_q = VGroup(*[Line(ax.c2p(y, 0) + DOWN * 0.42, ax.c2p(y, 0) + DOWN * 0.62,
                              color=MODEL if y > 4 else GREY_D, stroke_width=1.2) for y in ys])
        head = label(r"How often does a standard bell land above $4$?", font_size=32).to_edge(UP, buff=0.35)
        truth = label(rf"exactly: \ ${true * 1e5:.2f}$ in $100{{,}}000$", font_size=28, color=WHITE)
        truth.next_to(head, DOWN, buff=0.2)
        r1 = label(rf"draw from $p$: \ ${hits}$ of ${n:,}$ land there \ $\to$ ${plain * 1e5:.0f}$ in $100{{,}}000$"
                   .replace(",", "{,}").replace("{{,}}", "{,}"), font_size=28, color=DATA)
        r2 = label(rf"draw from $q$, \ weight by $p/q$: \ ${is_est * 1e5:.2f}$ in $100{{,}}000$", font_size=28, color=MODEL)
        VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        sample_note = label(rf"$p$ rug: first ${min(400, n)}$ draws plus all hits above $4$; \ $q$ rug: first ${len(ys)}$ draws"
                            rf" \\ both estimates use all ${n:,}$ draws each".replace(",", "{,}"),
                            font_size=18, color=GREY_A).move_to([0, -2.4, 0])
        colors = {r"p(x)": DATA, r"q(x)": MODEL, r"\mathbb{E}_p": DATA, r"\mathbb{E}_q": MODEL}
        f = cmath(r"\mathbb{E}_p", r"[f(x)]", "=", r"\mathbb{E}_q", r"\Big[f(x)\,", r"\frac{p(x)}{q(x)}", r"\Big]",
                  colors=colors, font_size=40).move_to([3.6, 2.3, 0])
        direct_verdict = direct_estimate_summary(hits, n, plain, true)
        weighted_verdict = estimate_comparison(is_est, true)
        with self.voiceover(
            "Monte Carlo has one weakness: rare events. How often does a standard bell land above four? Exactly, "
            f"about {true * 1e5:.1f} times in a hundred thousand. <bookmark mark='a'/> {direct_verdict} "
            "The rug shows the first four hundred recorded direct draws, plus every rare hit from the full run."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(p), FadeIn(pl))
            self.play(Create(edge), FadeIn(tail_l), FadeIn(truth))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rug_p], lag_ratio=0.004), run_time=1.5)
            self.play(*[Indicate(rug_p[int(i)], color=TAIL, scale_factor=1.0) for i in hit_positions],
                      FadeIn(r1), FadeIn(sample_note))
        with self.voiceover(
            "The fix is to cheat, and then correct for it. <bookmark mark='a'/> Draw from a bell that lands out there "
            "half the time. <bookmark mark='b'/> Then weight each sample by how much likelier it is under the real "
            "distribution than under the one you drew from. The proposal rug shows its first four hundred "
            f"recorded draws. <bookmark mark='c'/> Both estimates use all {n:,} draws each. For importance "
            f"sampling, {weighted_verdict} A single run is evidence, not a guarantee of improvement."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(q), FadeIn(ql), LaggedStart(*[FadeIn(r) for r in rug_q], lag_ratio=0.004), run_time=1.8)
            vo.wait_until("b")
            self.play(Write(f))
            vo.wait_until("c")
            self.play(FadeIn(r2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def origins(self):
        cards = VGroup(
            history_card(1946, r"Stanis\l aw Ulam", r"recovering from an illness, \ asks the odds of winning solitaire: \ "
                         r"easier to play a hundred games and count", width=4.3, font_size=23),
            history_card(1947, r"John von Neumann", r"proposes following random neutrons through a bomb core, \ one "
                         r"by one, \ on the new ENIAC", width=4.3, font_size=23),
            history_card(1948, r"Kl\'ara D\'an von Neumann \& Nicholas Metropolis",
                         r"run the first Monte Carlo programs on ENIAC; \ Metropolis names the method", width=4.3, font_size=23),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.2)
        head = label(r"Monte Carlo, \ Los Alamos", font_size=38).to_edge(UP, buff=0.4)
        cards.move_to(UP * 0.9)
        g_ = np.random.default_rng(1946)
        won = g_.random(100) < 0.085  # illustration: a hundred games of solitaire, a few of them won
        games = VGroup(*[RoundedRectangle(width=0.36, height=0.48, corner_radius=0.05, stroke_width=1.2,
                                          stroke_color=GREY_B, fill_color=C.INTERVAL if w else "#1A2130", fill_opacity=0.9)
                         for w in won]).arrange_in_grid(rows=4, cols=25, buff=0.08).move_to(DOWN * 2.1)
        gl = note(rf"illustration: \ play a hundred games, \ count the wins \ ({int(won.sum())} here)").next_to(games, UP, buff=0.12)
        cite_ = cite(r"N.~Metropolis, \textit{The Beginning of the Monte Carlo Method}, \ Los Alamos Science (1987)",
                     corner=DR)
        with self.voiceover(
            "The method was born at Los Alamos. <bookmark mark='a'/> In 1946 the mathematician Stanislaw Ulam, "
            "recovering from an illness, wondered how often solitaire comes out, and saw it was easier to play a "
            "hundred games and count. <bookmark mark='b'/> John von Neumann turned the idea into a way to follow "
            "neutrons through a bomb core, <bookmark mark='c'/> and in 1948 Klara von Neumann and Nicholas Metropolis "
            "ran it on ENIAC. Metropolis named it after the casino."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), LaggedStart(*[FadeIn(g) for g in games], lag_ratio=0.02), FadeIn(gl))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ess(self):
        d = load("ess")
        dims, ess, th = np.asarray(d["dims"], float), np.asarray(d["ess"]), np.asarray(d["theory"])
        n, s = int(d["n"]), float(d["s"])
        f = cmath(r"\mathrm{ESS}", "=", r"\frac{\big(\sum_i w_i\big)^2}{\sum_i w_i^2}", font_size=40,
                  colors={r"\mathrm{ESS}": C.BITS}).move_to([3.6, 2.2, 0])
        fn = label(r"weight concentration diagnostic \\ always between $1$ and $n$", font_size=22,
                   color=GREY_A).next_to(f, DOWN, buff=0.15)
        ax = CornerAxes(x_range=[0, 2.4, 1], y_range=[-3, 4, 1], x_length=6.4, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.8, -0.5, 0])
        xt = VGroup(*[MathTex(str(int(v)), font_size=20, color=GREY_B).next_to(ax.c2p(math.log10(v), -3), DOWN, buff=0.1)
                      for v in (1, 10, 100)])
        yt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for t, v in (("10^{-2}", -2), ("1", 0), ("10^{2}", 2), ("10^{4}", 4))])
        xl = label(r"dimension", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(rf"effective samples, \ of ${n:,}$".replace(",", "{,}"), font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        lx = np.log10(dims)
        dd = np.linspace(1, 250, 200)
        log_proxy = math.log10(n) - dd * math.log10(s ** 2 / math.sqrt(2 * s ** 2 - 1))
        visible = (log_proxy >= -3) & (log_proxy <= 4)
        thc = curve(ax, np.log10(dd[visible]), log_proxy[visible], color=WHITE, stroke_width=2.5)
        floor = DashedLine(ax.c2p(0, 0), ax.c2p(2.4, 0), color=GREY_C, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(a, math.log10(v)), radius=0.045, color=C.BITS, fill_opacity=0.8)
                        for row in ess for a, v in zip(lx, row)])
        leg = VGroup(label(r"measured, \ five seeds", font_size=20, color=C.BITS),
                     label(r"large-$n$ proxy: \ $n/\mathbb{E}_q[w^2]$ \\ $n\,\big(s^2/\sqrt{2s^2 - 1}\big)^{-d}$",
                           font_size=20, color=WHITE))
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax.c2p(0.05, -1.4), RIGHT, buff=0.0)
        setup = label(rf"target: \ a standard bell in $d$ dimensions; \\ proposal: \ ${s:g}\times$ wider", font_size=22,
                      color=GREY_A).next_to(fn, DOWN, buff=0.45).align_to(fn, LEFT)
        m = ess.mean(0)
        i50, i200 = list(dims).index(50), list(dims).index(200)
        proxy_note = ("It is below one, so it cannot be a finite-sample weight count." if th[i200] < 1 else
                      "It is a population-moment approximation, not an exact finite-sample count.")
        with self.voiceover(
            "Importance sampling has a weakness of its own: the weights. <bookmark mark='a'/> This weight-based "
            "effective sample size diagnoses their concentration; it always lies between one and n. "
            "<bookmark mark='b'/> Aim at a bell with a proposal "
            f"just {100 * (s - 1):.0f} percent wider. In one dimension, {m[0]:,.0f} of {n:,} samples count; in fifty, "
            f"{m[i50]:.0f}; in two hundred the diagnostic says {m[i200]:.0f}. The population-moment, large-n proxy "
            f"is {th[i200]:.3f}. {proxy_note} Rare large weights can be missing from "
            "a finite run, so the diagnostic alone does not certify accuracy. <bookmark mark='c'/> That is why "
            "reinforcement learning clips its importance ratios, in part twenty-six."
        ) as vo:
            self.play(Write(f), FadeIn(fn))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(setup))
            vo.wait_until("b")
            self.play(Create(floor), Create(thc), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.02), FadeIn(leg), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
