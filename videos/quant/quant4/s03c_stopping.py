from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, load


class Stopping(VoiceoverScene):
    def construct(self):
        f = load("firstpassage")
        self.card()
        self.bell(f)
        self.derive()
        self.walks(f)

    def card(self):
        c = chapter_card(5, r"Stopping times, and the walk that always wins", r"When may you decide to stop?",
                         part=PART)
        with self.voiceover("Chapter five. Stopping times, and the walk that always wins."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def bell(self, f):
        path = np.concatenate([[0], np.asarray(f["short_paths"][3])[:100]])
        n = len(path) - 1
        lo, hi = int(path.min()) - 2, int(path.max()) + 3
        g = axes([0, n], [lo, hi], x_length=9.0, y_length=3.6, xlabel=r"steps of a fair walk", xticks=[0, 50, 100],
                 yticks=[lo, 0, 1, hi], font_size=18).to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.8)
        ax = g.ax
        tk = ValueTracker(0.0)
        hit = np.flatnonzero(path >= 1)
        t_hit = int(hit[0]) if len(hit) else n
        one = DashedLine(ax.c2p(0, 1), ax.c2p(n, 1), color=QC.GAIN, stroke_width=2)
        live = tracing(ax, np.arange(n + 1), path, tk, MART, stroke_width=3)
        curtain = always_redraw(lambda: Rectangle(
            width=max(ax.c2p(n, 0)[0] - ax.c2p(tk.get_value(), 0)[0], 0.01), height=ax.height + 0.2, stroke_width=0,
            fill_color=GREY_E, fill_opacity=0.92).move_to(ax.c2p(n, (lo + hi) / 2), aligned_edge=RIGHT))
        ring = VGroup(Dot(ax.c2p(t_hit, path[t_hit]), radius=0.09, color=QC.IDEA),
                      label(r"A rings: first time at $+1$", font_size=22, color=QC.IDEA).next_to(
                          ax.c2p(t_hit, path[t_hit]), UP, buff=0.25))
        imax = int(np.argmax(path))
        ghost = curve(ax, np.arange(n + 1), path, GREY_B, stroke_width=2).set_stroke(opacity=0.6)
        bmark = VGroup(Dot(ax.c2p(imax, path[imax]), radius=0.09, color=LOSS),
                       label(r"B: ``ring at the top of the 100 steps''", font_size=22, color=LOSS).next_to(
                           ax.c2p(imax, path[imax]), UP, buff=0.25))
        stamp = label(r"not a stopping time", font_size=40, color=LOSS).rotate(0.15).move_to(ax.c2p(n * 0.7, lo + 1))
        stamp_box = SurroundingRectangle(stamp, color=LOSS, buff=0.12)
        rules = VGroup(
            label(r"a stopping time $\tau$: $\{\tau \le n\} \in \mathcal{F}_n$ for every $n$", font_size=24, color=MART),
            label(r"allowed: the first time at $+1$; the first time wealth doubles; ``at step 50''", font_size=21,
                  color=GREY_A),
            label(r"forbidden: the top of the path; the last visit to 0; ``the day before a crash''", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A stopping time decides whether to stop now using only what has happened up to now. "
            "<bookmark mark='a'/> A walk runs toward a curtain hiding the future. Rule A rings the first time it "
            "reaches plus one, the moment it happens. <bookmark mark='b'/> Rule B rings at the highest point of the "
            "first hundred steps. Pull back the curtain: to know that was the top, it needed the future. "
            "<bookmark mark='c'/> Rule B is not a stopping time. Hitting times and fixed dates are allowed; the peak, "
            "or the day before a crash, are not."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(rules[0]))
            self.add(live, curtain)
            vo.wait_until("a")
            self.play(tk.animate.set_value(float(t_hit)), run_time=3, rate_func=linear)
            self.play(FadeIn(ring, scale=1.3), Flash(ring[0].get_center(), color=QC.IDEA))
            vo.wait_until("b")
            self.play(tk.animate.set_value(float(min(imax + 3, n))), run_time=2, rate_func=linear)
            live.clear_updaters()
            curtain.clear_updaters()
            self.play(FadeOut(curtain), FadeIn(ghost), FadeIn(bmark))
            vo.wait_until("c")
            self.play(FadeIn(stamp, scale=1.4), Create(stamp_box))
            self.play(FadeIn(rules[1:]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"M^\tau_n = M_{\tau \wedge n}", r"=",
                      r"M_0 + \sum_{k \le n} \mathbf{1}_{\{k \le \tau\}}\,\Delta M_k", font_size=38),
                cmath(r"\{k \le \tau\}", r"=", r"\{\tau \le k - 1\}^c \in \mathcal{F}_{k-1}", font_size=38,
                      colors={r"\{\tau \le k - 1\}^c \in \mathcal{F}_{k-1}": MART}),
                cmath(r"P(\tau_1 > n)", r"=", r"P(S_n \in \{0, 1\}) \approx \sqrt{2/(\pi n)}", font_size=38),
                cmath(r"\mathbb{E}\tau_1", r"=", r"\sum_n P(\tau_1 > n) = \infty", font_size=38,
                      colors={r"\sum_n P(\tau_1 > n) = \infty": LOSS}),
                cmath(r"\mathbb{E}S_\tau", r"=", r"\mu\,\mathbb{E}\tau \quad (\mathbb{E}\tau < \infty)\ \Rightarrow\ 1 = 0",
                      font_size=38),
                cmath(r"\mathbb{E}\big[\alpha^{\tau_1}\big]", r"=", r"\frac{1 - \sqrt{1 - \alpha^2}}{\alpha}, \quad "
                      r"\alpha = \frac{1}{\cosh\sigma}", font_size=38)]
        whys = [why(r"the stopped process is the martingale transform with stake $\mathbf{1}\{k \le \tau\}$"),
                why(r"that stake is predictable, so a stopped martingale is a martingale (chapter 4)"),
                why(r"reflection: swap every path's steps after its first visit to $+1$; then Stirling"),
                why(r"the tail falls like $n^{-1/2}$, too slowly to sum: the walk that always wins takes forever on "
                    r"average"),
                why(r"Wald's identity, by contradiction: $S_{\tau_1} = 1$ but the drift $\mu$ is 0"),
                why(r"stop the exponential martingale $e^{\sigma S_n}(\cosh\sigma)^{-n}$, bounded before $\tau_1$ "
                    r"(Shreve I, ch.\ 5); its slope at $\alpha = 1$ is infinite")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.0, buff=0.68, edge=6.9)
        with self.voiceover(
            "Two facts, with proofs. A stopped martingale is the transform with stake one until the stopping time. "
            "<bookmark mark='a'/> That stake is decided a step ahead, so the stopped process is a martingale. "
            "<bookmark mark='b'/> Now a paradox. Let tau be the first time a fair walk reaches plus one. By "
            "reflection, the chance it has not arrived after n steps is the chance the walk sits at zero or one, about "
            "root two over pi n. <bookmark mark='c'/> So it arrives with probability one, yet the expected time is "
            "infinite. <bookmark mark='d'/> Wald's identity proves it in a line: a finite expected time would make "
            "the expected position zero, but it is one. <bookmark mark='e'/> Stopping the exponential martingale "
            "gives tau's whole law."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            step(5)
        self.wait(0.4)
        self.clear_scene()

    def walks(self, f):
        P = np.asarray(f["short_paths"], float)
        T = np.asarray(f["short_tau"])
        k_show = len(P)
        n = P.shape[1]
        g = axes([0, n], [-30, 4], x_length=6.2, y_length=4.0, xlabel=r"steps", ylabel=rf"{k_show} fair walks, "
                 r"frozen at $+1$", xticks=[0, 100, 200, 300], yticks=[-30, -15, 0, 1], font_size=16)
        g.to_corner(UL, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        tk = ValueTracker(0.0)
        cols = [QC.IDEA if (T[i] > 0) else P_C for i in range(k_show)]

        def walk_mob():
            t = tk.get_value()
            grp = VGroup()
            for i in range(k_show):
                stop = T[i] if T[i] > 0 else n
                m = int(np.clip(min(t, stop), 1, n))
                pts = [ax.c2p(0, 0)] + [ax.c2p(j + 1, max(P[i, j], -30)) for j in range(m)]
                grp.add(VMobject(stroke_width=1.0, stroke_color=P_C, stroke_opacity=0.35).set_points_as_corners(pts))
                if T[i] > 0 and T[i] <= t:
                    grp.add(Dot(ax.c2p(T[i], 1), radius=0.035, color=QC.IDEA))
            return grp

        fan = always_redraw(walk_mob)
        counter = always_redraw(lambda: MathTex(
            rf"\text{{hit }} +1\text{{ by step }} {int(tk.get_value())}: "
            rf"{100 * np.mean((T > 0) & (T <= tk.get_value())):.1f}\%", font_size=28, color=QC.IDEA).next_to(
            g, DOWN, buff=0.2).align_to(g, LEFT))
        grid = np.asarray(f["grid"], float)
        surv, exact = np.asarray(f["surv"]), np.asarray(f["exact"])
        g2 = axes([0, 5], [-3, 0], x_length=4.6, y_length=2.6, xlabel=r"$n$ (log)", ylabel=r"$P(\tau_1 > n)$ (log)",
                  xticks=[0, 1, 2, 3, 4, 5], xfmt=lambda u: rf"10^{{{int(u)}}}", yticks=[-3, -2, -1, 0],
                  yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=14).to_corner(UR, buff=0.5)
        a2 = g2.ax
        m = surv > 0
        ex = curve(a2, np.log10(grid), np.log10(exact), WHITE, stroke_width=2.5)
        pts2 = VGroup(*[Dot(a2.c2p(x, y), radius=0.04, color=QC.IDEA) for x, y in zip(np.log10(grid[m]), np.log10(surv[m]))])
        slope = label(r"slope $-\tfrac12$: exact (white), 10{,}000 walks to $10^5$ steps (gold)", font_size=16,
                      color=GREY_B).next_to(g2, DOWN, buff=0.15)
        rk, rm = np.asarray(f["running_k"], float), np.asarray(f["running_mean"], float)
        g3 = axes([0, 4], [0, float(rm.max()) * 1.1], x_length=4.6, y_length=1.9, xlabel=r"walks so far (log)",
                  ylabel=r"average of $\tau_1 \wedge 10^5$", xticks=[0, 2, 4], xfmt=lambda u: rf"10^{{{int(u)}}}",
                  yticks=[0, round(float(rm.max()), -2)], yfmt=lambda u: f"{u:,.0f}".replace(",", "{,}"), font_size=14)
        g3.next_to(slope, DOWN, buff=0.35).align_to(g2, LEFT)
        run = curve(g3.ax, np.log10(rk), rm, LOSS, stroke_width=2.5)
        p100 = f["p100"]
        cap = f["capped_mean"]
        pred = desk_question(r"After 100 fair steps, what fraction of walks has not yet been up 1?",
                             rf"About {100 * f['p100_exact']:.0f}\%: $\binom{{100}}{{50}}/2^{{100}} = {f['p100_exact']:.4f}$; "
                             rf"simulated {p100:.4f}.", width=5.4, font_size=21).to_corner(UR, buff=0.4)
        with self.voiceover(
            f"Here are {k_show} walks, each frozen with a gold dot when it first reaches plus one. "
            "<bookmark mark='a'/> The counter climbs fast, then slowly: some walks wander deep below zero. "
            "<bookmark mark='b'/> On log scales the chance of still waiting falls with slope minus a half, ten thousand "
            "walks on the exact curve. <bookmark mark='c'/> And the average wait never settles: capped at a hundred "
            f"steps it is {cap['100']:.0f}, at a hundred thousand {cap['100000']:.0f}, growing like the square root of "
            "the cap. <bookmark mark='d'/> After a hundred fair steps, what fraction has not yet been up one? About "
            f"{100 * f['p100_exact']:.0f} percent."
        ) as vo:
            self.play(FadeIn(g))
            self.add(fan, counter)
            vo.wait_until("a")
            self.play(tk.animate.set_value(float(n)), run_time=8, rate_func=lambda u: u ** 1.6)
            fan.clear_updaters()
            counter.clear_updaters()
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(ex), FadeIn(slope))
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts2], lag_ratio=0.05))
            vo.wait_until("c")
            self.play(FadeIn(g3), Create(run), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeOut(VGroup(g2, ex, pts2, slope)), FadeIn(pred, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
