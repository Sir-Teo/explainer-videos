from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant11.common import (GAMMA, OPT, PART, SPOT, THETA, VEGA, axes3d, fixed, hint3d, load, pause,
                                         real_data, surf)


class Scalp(VoiceoverScene, ThreeDScene):
    def construct(self):
        s = load("scalp")
        sh = load("scalp_shuffle")
        self.card()
        self.trades(s)
        self.landscape(s)
        self.shuffle(s, sh)
        self.derive(s)

    def card(self):
        c = chapter_card(2, r"Gamma scalping on a real path", r"How does a long straddle turn moves into money?",
                         part=PART)
        with self.voiceover("Chapter two. Gamma scalping, on a real path."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def trades(self, s):
        t, S, sh = np.asarray(s["t"]), np.asarray(s["S"]), np.asarray(s["shares"])
        g1 = axes([0, 30], [50, 110], x_length=7.4, y_length=2.6, ylabel=r"bitcoin (per 100)", xticks=[0, 10, 20, 30],
                  yticks=[60, 80, 100], font_size=16)
        g2 = axes([0, 30], [-1, 1], x_length=7.4, y_length=2.2, xlabel=r"days from 1 May 2021",
                  ylabel=r"hedge: units of bitcoin held", xticks=[0, 10, 20, 30], yticks=[-1, 0, 1], font_size=16)
        VGroup(g1, g2).arrange(DOWN, buff=0.4).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        tr = ValueTracker(0.0)
        ts, Ss, shs = t[::2], S[::2], np.clip(sh[::2], -1, 1)
        ls = tracing(g1.ax, ts, Ss, tr, SPOT, stroke_width=2.5)
        lh = tracing(g2.ax, ts, shs, tr, OPT, stroke_width=2.5)
        d = np.diff(sh)
        idx = [i for i in range(0, len(d), 3) if abs(d[i]) > 0.01]

        def dots():
            n = at_index(np.arange(len(ts)) * 2.0, tr)
            g = VGroup()
            for i in idx:
                if i + 1 <= n:
                    g.add(Dot(g1.ax.c2p(t[i + 1], S[i + 1]), radius=0.035, color=GAMMA if d[i] > 0 else THETA))
            return g
        dd = always_redraw(dots)
        leg = legend([(GAMMA, r"hedge buys"), (THETA, r"hedge sells")], font_size=18).next_to(g1, UP, buff=0.05).align_to(
            g1, RIGHT)
        side = VGroup(
            wrapped_label(r"long gamma means the hedge always trades against the move: it buys after falls and sells "
                          r"after rises, locking in a little of each swing", 4.2, 20, GREY_A),
            wrapped_label(r"the straddle's delta runs from zero toward $-1$ as bitcoin falls: by the low, the hedge "
                          r"holds almost a full unit, bought all the way down", 4.2, 20, OPT),
            wrapped_label(r"after the crash the strike is far away: the hedge barely trades, and theta keeps charging", 4.2,
                          20, THETA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Binance BTCUSDT hourly; hedge rebalanced every hour (the House's \texttt{hedge})")
        with self.voiceover(
            "Here is the scalper at work, hour by hour. Every hour the hedge resets to the straddle's delta. Because "
            "the straddle is long gamma, the hedge always trades against the market: it buys after falls, the green "
            "dots, and sells after rises, the red ones, and each round trip locks in a little of the swing. "
            "<bookmark mark='a'/> When Bitcoin slid in the middle of the month, the straddle's delta ran toward "
            "minus one, and the hedge bought all the way down, ending with almost a whole Bitcoin. "
            "<bookmark mark='b'/> After the crash, the strike was far away. The straddle had become a put deep in the "
            "money, nearly linear, with little gamma, and the hedge barely traded, while theta kept charging."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(src), FadeIn(leg), FadeIn(side[0]))
            self.add(ls, lh, dd)
            self.play(tr.animate.set_value(len(ts) * 0.62), run_time=vo.until("a"), rate_func=linear)
            self.play(FadeIn(side[1]), tr.animate.set_value(len(ts) * 0.7), run_time=vo.until("b"), rate_func=linear)
            self.play(tr.animate.set_value(len(ts) - 1), FadeIn(side[2]), run_time=max(vo.remaining(1.0) - 0.3, 1.0))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def landscape(self, s):
        sig, T = float(s["iv"]), 30.0
        ax = axes3d([50, 120, 10], [0, 30, 10], [0, 12, 4], x_length=7.6, y_length=5.4, z_length=3.2)

        def dg(x, day):
            tau = max(T - day, 0.4) / 365
            return float(min(2 * bs.greeks(x, 100.0, tau, sig)["gamma"] * x * x / 100, 12.0))
        sf = surf(ax, dg, (50, 120), (0, 29.5), [(QC.SPOT, 0.5), (GAMMA, 4), (QC.LOSS, 11)], resolution=(28, 22),
                  opacity=0.7)
        t, S = np.asarray(s["t"])[::3], np.asarray(s["S"])[::3]
        pts = [ax.c2p(x, d, dg(x, d)) + OUT * 0.05 for x, d in zip(S, t)]
        path = VMobject(stroke_color=YELLOW, stroke_width=5).set_points_as_corners(pts)
        hint = hint3d((r"bitcoin (per 100)", SPOT), (r"days from 1 May 2021", THETA),
                      (r"dollar gamma $\Gamma S^2$ of the straddle", GAMMA))
        cap = wrapped_label(r"the path climbs the ridge while bitcoin stays near the strike, then the crash of the "
                            r"19th happens on the lowland, where a squared move earns little", 5.0, 21,
                            GREY_A).to_corner(DL, buff=0.35)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-50 * DEGREES, zoom=0.9)
        fixed(self, hint, cap)
        with self.voiceover(
            "Why so little, in so violent a month? Here is where gamma lives. This landscape is the straddle's dollar "
            "gamma, gamma times S squared, over the price and the day: what each squared move is worth. It is a "
            "ridge along the strike that sharpens into a spike as expiry nears. <bookmark mark='a'/> Now lay the real "
            "path on it, in yellow. For the first fortnight Bitcoin wandered near the strike and the path climbed the "
            "ridge. <bookmark mark='b'/> Then it slid off, and the crash of the nineteenth, the biggest moves of the "
            "year, happened down on the lowland, where a squared move earns almost nothing."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), run_time=1.2)
            self.play(Create(sf), run_time=3)
            vo.wait_until("a")
            self.play(Create(path), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(cap))
            self.move_camera(theta=-20 * DEGREES, phi=70 * DEGREES, run_time=max(vo.remaining(1.0) - 0.3, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, sf, path)),
                                                                             FadeOut(hint), FadeOut(cap)], run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shuffle(self, s, sh):
        pnl = np.asarray(sh["pnl"])
        lo, hi, nb = -2.0, 20.0, 44
        g = axes([lo, hi], [0, 1], x_length=7.6, y_length=4.0, xlabel=r"hedged straddle P\&L, per 100",
                 ylabel=r"share of the 2{,}000 reorderings", xticks=[0, 5, 10, 15, 20], yticks=[], font_size=17)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        cnt = np.histogram(np.clip(pnl, lo, hi - 1e-9), bins=nb, range=(lo, hi))[0]
        top = cnt.max() * 1.1
        n = ValueTracker(1.0)
        edges = np.linspace(lo, hi, nb + 1)

        def bars():
            k = int(n.get_value())
            c = np.histogram(np.clip(pnl[:k], lo, hi - 1e-9), bins=nb, range=(lo, hi))[0] * (len(pnl) / max(k, 1))
            gr = VGroup()
            for j in range(nb):
                if c[j] <= 0:
                    continue
                a, b = ax.c2p(edges[j], 0), ax.c2p(edges[j + 1], min(c[j] / top, 1))
                gr.add(Rectangle(width=b[0] - a[0] - 0.01, height=b[1] - a[1], stroke_width=0, fill_color=GAMMA,
                                 fill_opacity=0.75).move_to((a + b) / 2))
            return gr
        hb = always_redraw(bars)
        counter = always_redraw(lambda: MathTex(rf"{int(n.get_value()):,}".replace(",", "{,}") +
                                                r"\ \text{reorderings}", font_size=26, color=GAMMA)
                                .next_to(g, UP, buff=0.1).align_to(g, RIGHT))
        real = sh["real"]
        mk = DashedLine(ax.c2p(real, 0), ax.c2p(real, 1), color=OPT, stroke_width=3)
        mkl = label(rf"the real month: {real:+.1f}", font_size=20, color=OPT).next_to(ax.c2p(real, 1), UP, buff=0.05)
        pct = 100 * sh["pct"]
        verdict = (rf"only {pct:.1f}\% of reorderings paid less" if pct < 10 else
                   rf"{pct:.0f}\% of reorderings paid less")
        side = VGroup(
            wrapped_label(r"the same 720 hourly returns, shuffled: identical realized variance, "
                          rf"{100 * sh['rv']:.0f}\%, every time", 4.4, 20, GREY_A),
            MathTex(rf"\text{{mean }} {sh['mean']:+.1f},\ \ 90\%:\ [{sh['p5']:.1f},\ {sh['p95']:.1f}]", font_size=28,
                    color=GAMMA),
            wrapped_label(verdict + r": the real order, a slow slide and then a crash far from the strike, was "
                          r"close to the worst order there is", 4.4, 20, OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        pc = pause(r"Same returns, but the crash on day 2 instead of day 19. More, or less?", width=4.4,
                   font_size=21).to_edge(RIGHT, buff=0.4).to_edge(DOWN, buff=0.4)
        early = sh["early"]
        say = (f"only {pct:.1f} percent of the reorderings paid less." if pct < 10 else
               f"{pct:.0f} percent of the reorderings paid less.")
        if early > real and early < sh["mean"]:
            then = (f"It earns more, {early:+.1f}, but far less than the average shuffle: after an early crash, "
                    "Bitcoin spends the month far from the strike.")
        elif early > real:
            then = f"It earns more, {early:+.1f}: the big moves now come while spot is near the strike."
        else:
            then = f"It earns even less, {early:+.1f}."
        with self.voiceover(
            "Here is the proof that order matters. Keep the month's seven hundred and twenty hourly returns and "
            "shuffle their order, two thousand times. Every shuffled month has exactly the same realized "
            "variance. <bookmark mark='a'/> But the hedged straddle's profit is all over the place, averaging "
            f"{sh['mean']:.1f}. <bookmark mark='b'/> And the real month? {real:+.1f}: {say} A slow slide away from "
            "the strike followed by a crash in the lowland is close to the worst order there is. "
            f"<bookmark mark='c'/> Pause and predict: move the crash to the second day. <bookmark mark='d'/> {then}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            self.add(hb, counter)
            self.play(n.animate.set_value(len(pnl)), run_time=vo.until("a"), rate_func=rush_into)
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(mk), FadeIn(mkl))
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(pc))
            vo.wait_until("d")
            ek = DashedLine(ax.c2p(early, 0), ax.c2p(early, 0.8), color=VEGA, stroke_width=3)
            ekl = label(rf"crash on day 2: {early:+.1f}", font_size=19, color=VEGA).next_to(ax.c2p(early, 0.8), UP,
                                                                                          buff=0.05)
            self.play(Create(ek), FadeIn(ekl), FadeOut(pc))
        hb.clear_updaters()
        counter.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self, s):
        rows = [
            cmath(r"P\&L", r"=", r"\sum_k \tfrac12\,\Gamma_k S_k^2\left(r_k^2 - \sigma_i^2\,\Delta t\right) + "
                  r"\varepsilon", font_size=38, colors={r"P\&L": OPT}),
            cmath(r"\mathbb{E}[P\&L \mid \text{path}]", r"\neq", r"f\Big(\sum_k r_k^2\Big)", font_size=38),
            cmath(r"\text{log contract: }\ \tfrac12\Gamma S^2", r"=", r"\tfrac{1}{\sigma^2 \tau}\cdot\tfrac{\cdot}{\cdot}"
                  r"\ \to\ \text{weight } \tfrac{1}{S^2}\cdot S^2 = 1", font_size=34),
        ]
        rows[2] = cmath(r"\text{weight}\ \Gamma S^2 \to 1", r"\iff", r"\text{hold } \tfrac{2}{K^2}\,dK \text{ of every "
                        r"option: a variance swap}", font_size=34)
        whys = [why(r"sum the day's identity of chapter 1 over the hedging steps: each squared return is weighted by "
                    r"the dollar gamma at that moment"),
                why(r"the weight depends on where spot was when it moved, so the same returns in another order pay "
                    r"differently (El Karoui, Jeanblanc and Shreve 1998)"),
                why(r"Carr and Madan (1998): a strip of options weighted $1/K^2$ has constant dollar gamma, and collects "
                    r"$\sum r_k^2$ exactly: Part 12 builds it")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.4, buff=0.9, edge=6.9)
        card = lab_card(r"the hedger's ledger, step by step", [
            "for i in range(1, n1):",
            "    gi = bs.greeks(S[:, i], K, tau[i], sig_h, r, q, cp)",
            "    dS = S[:, i] - s_prev",
            "    step = w * (gi['price'] - v_prev - delta * dS)",
            "    mtm += step",
            "    gam_acc += w * 0.5 * gam_prev * dS ** 2",
            "    the_acc += -w * 0.5 * gam_prev * s_prev**2 * sig_h**2 * dt",
        ], source="explainer/quant/house/hedge.py (delta_hedge, at r = q = 0)", width=7.0)
        with self.voiceover(
            "In symbols. Sum the day's identity over every hedging step: each squared return is weighted by the "
            "dollar gamma at that moment. <bookmark mark='a'/> So the expected profit, given the path, is not a "
            "function of the realized variance alone. Nicole El Karoui and her coauthors made this precise; the "
            "shuffle measured it. <bookmark mark='b'/> If you want to be paid the variance itself, you need a "
            "weight that does not depend on where spot is. Peter Carr and Dilip Madan showed that a strip of "
            "options, weighted one over the strike squared, has exactly that: constant dollar gamma. That is the "
            "variance swap, which Part twelve builds. <bookmark mark='c'/> And here is the House's ledger that did "
            "all this accounting: each hour, the mark-to-market of the step, the gamma term and the theta term. "
            f"Run on the May path, gamma {s['gamma'][-1]:+.1f}, theta {s['theta'][-1]:+.1f}, net {s['pnl']:+.1f}."
            " Scalping means hedging. Next: how often."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(*[FadeOut(m) for m in self.mobjects])
            card.to_edge(UP, buff=0.5)
            self.play(FadeIn(card))
            lab_run(self, card, ["delta_hedge(t, may2021, 100, T, dvol, record=[0])  # call + put",
                                 f"gamma {s['gamma'][-1]:+.1f}   theta {s['theta'][-1]:+.1f}   net {s['pnl']:+.1f}"])
        self.wait(0.4)
        self.clear_scene()
