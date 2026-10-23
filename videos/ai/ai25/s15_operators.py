from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (HIST, KIND_COLOR, KIND_NAME, PAIR_C, PART, PLAIN, PRED_C, STRUCT, SYM, TRUE_C, load,
                                   node_box, take_away)


class Operators(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.fourier()
        self.replay()
        self.resolution()

    def card(self):
        card = chapter_card(14, r"Neural operators", r"Can a network learn an equation, not a grid?", lit=(),
                            part=PART)
        with self.voiceover("Chapter fourteen. Neural operators."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def problem(self):
        fo = load("fno")
        u0 = np.asarray(fo["show_u0"])[0]
        uT = np.asarray(fo["show_uT"])[0]
        x = np.linspace(0, 1, len(u0), endpoint=False)
        lim = float(np.ceil(max(np.abs(u0).max(), np.abs(uT).max()) * 10) / 10)
        g = axes([0, 1], [-lim, lim], x_length=5.6, y_length=3.0, xlabel=r"$x$", ylabel=r"$u$",
                 xticks=[0, 1], yticks=[-lim, 0, lim], center=[-3.3, 0.2, 0])
        c0 = curve(g.ax, x, u0, GREY_B, 3)
        cT = curve(g.ax, x, uT, TRUE_C, 3.5)
        lg = legend([(GREY_B, r"$u(x, 0)$: \ the start"), (TRUE_C, r"$u(x, 1)$: \ one time unit later")], font_size=20)
        lg.next_to(g, DOWN, buff=0.25).align_to(g.ax, LEFT)
        eq = cmath(r"\partial_t u + u\, \partial_x u", r"=", r"\nu\, \partial_{xx} u", font_size=36).move_to([3.4, 2.2, 0])
        el = label(rf"Burgers' equation, \ $\nu = {fo['nu']:g}$, \ periodic", font_size=22, color=GREY_A)
        el.next_to(eq, DOWN, buff=0.15)
        pts = VGroup(
            label(r"a solver: \ thousands of small steps, \ every time", font_size=22),
            label(r"a network on $64$ numbers: \ only ever $64$ numbers", font_size=22, color=PLAIN),
            label(r"an \textit{operator}: \ a function in, \ a function out", font_size=22, color=STRUCT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 0.0, 0])
        hist = VGroup(
            label(r"Chen \& Chen (1995): \ networks can approximate operators", font_size=20, color=GREY_B),
            label(r"DeepONet (Lu et al.\ 2021); \ Fourier neural operator (Li et al.\ 2021)", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.4).align_to(pts, LEFT)
        with self.voiceover(
            "Fields evolve by equations. Here is Burgers' equation, a one-dimensional cartoon of fluid flow: a wave "
            "that steepens where it is fast and smooths out by viscosity. <bookmark mark='a'/> From this start, "
            "one time unit later, the solution looks like this. <bookmark mark='b'/> A solver gets there in "
            "thousands of small steps, every time it is asked. A network could learn the map from start to finish, "
            "but an ordinary network works on a fixed list of numbers: trained on sixty-four points, it only knows "
            "sixty-four points. <bookmark mark='c'/> What we want is to learn the operator itself, a map from "
            "functions to functions, which can be read at any resolution. <bookmark mark='d'/> Tianping and Hong "
            "Chen proved in 1995 that networks can approximate operators; DeepONet and the Fourier neural operator, "
            "both published in 2021, made it practical."
        ) as vo:
            self.play(FadeIn(g), Create(c0), FadeIn(lg[0]), Write(eq), FadeIn(el))
            vo.wait_until("a")
            self.play(Create(cT), FadeIn(lg[1]))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fourier(self):
        rows = [
            cmath(r"v'(x)", r"=", r"\sigma\Big(W v(x) + \int \kappa(x - y)\, v(y)\, dy\Big)", font_size=34),
            cmath(r"\mathcal F[\kappa * v](k)", r"=", r"\hat\kappa(k)\, \hat v(k)", font_size=34),
            cmath(r"v'", r"=", r"\sigma\Big(W v + \mathcal F^{-1}\big[R_k \cdot \hat v(k)\big]_{|k| \le k_{\max}}\Big)",
                  font_size=34),
        ]
        rows[2][2].set_color(STRUCT)
        whys = [why(r"a layer as an integral over the whole field"), why(r"the convolution theorem"),
                why(r"learn $R_k = \hat\kappa(k)$ directly, \ for the lowest $k_{\max}$ frequencies")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.55, edge=6.9)
        props = VGroup(
            label(r"the weights live on frequencies, \ not on grid points: \ any grid can use them", font_size=23,
                  color=STRUCT),
            label(r"a shift of the input shifts the output: \ equivariant, \ like a convolution", font_size=23,
                  color=SYM),
            label(r"cost $O(n \log n)$ per layer, \ by the fast Fourier transform", font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The Fourier neural operator, from Zongyi Li, Anima Anandkumar, Andrew Stuart and colleagues, starts "
            "from a layer that is an integral: each point's new value mixes the whole field, through a kernel "
            "kappa. <bookmark mark='a'/> If the kernel depends only on the offset, the integral is a convolution, "
            "and the convolution theorem turns it into a product of Fourier transforms. <bookmark mark='b'/> So "
            "learn the kernel's transform directly: a learned complex weight for each of the lowest frequencies, "
            "sixteen in our model, and drop the rest. <bookmark mark='c'/> Three things follow. The weights belong "
            "to frequencies, not grid points, so the same network can read any grid fine enough to hold those "
            "frequencies. A shift of the input shifts the output. And each layer costs little more than a fast "
            "Fourier transform."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in props], lag_ratio=0.5), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        fo = load("fno")
        rec = fo["fno_s0"]
        frames = [np.asarray(f)[0] for f in rec["frames"]]
        snaps = list(fo["snaps"])
        uT = np.asarray(fo["show_uT"])[0]
        res = int(fo["res"])
        x = np.linspace(0, 1, len(uT), endpoint=False)
        xs = np.linspace(0, 1, res, endpoint=False)
        lim = float(np.ceil(np.abs(uT).max() * 12) / 10)
        g = axes([0, 1], [-lim, lim], x_length=6.0, y_length=3.4, xlabel=r"$x$", ylabel=r"$u(x, 1)$",
                 xticks=[0, 1], yticks=[-lim, lim], center=[-2.8, 0.1, 0])
        truth = curve(g.ax, x, uT, TRUE_C, 4)
        cur = VGroup(*[Dot(g.ax.c2p(a, np.clip(b, -lim, lim)), radius=0.035, color=STRUCT) for a, b in zip(xs, frames[0])])
        cnt = label(r"step $0$", font_size=22, color=GREY_A).next_to(g, UP, buff=0.1)
        cv = np.asarray(rec["curve"])
        ax2 = axes([0, cv[-1, 0]], [0, float(np.ceil(cv[:, 1].max() * 10) / 10)], x_length=3.8, y_length=2.6,
                   xlabel=r"training step", ylabel=r"relative error", xticks=[0, cv[-1, 0]], yticks=[0],
                   xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), center=[4.3, 0.3, 0])
        dot = Dot(ax2.ax.c2p(cv[0, 0], cv[0, 1]), color=STRUCT)
        lg = legend([(TRUE_C, r"the solver"), (STRUCT, r"FNO, \ on $64$ points")], font_size=20)
        lg.next_to(g, DOWN, buff=0.25).align_to(g.ax, LEFT)
        e_fin = float(cv[-1, 1])
        tag = note(rf"computed: \ $1{{,}}000$ training pairs at ${res}$ points; \ ${rec['params']:,}$ weights"
                   .replace(",", "{,}").replace("{{,}}", "{,}"), font_size=20).to_corner(DR, buff=0.2)
        with self.voiceover(
            f"We trained one on a thousand solutions of Burgers' equation, sampled at {res} points, against a "
            "pseudo-spectral solver's answers. <bookmark mark='a'/> Here is its prediction for a start it never saw, "
            "at checkpoints through training, beside the learning curve. <bookmark mark='b'/> It ends with a "
            f"relative error of {100 * e_fin:.1f} percent on held-out starts."
        ) as vo:
            self.play(FadeIn(g), Create(truth), FadeIn(cur), FadeIn(cnt), FadeIn(ax2), FadeIn(dot), FadeIn(lg),
                      FadeIn(tag))
            vo.wait_until("a")
            per = max(0.5, vo.until("b") / max(1, len(frames) - 1))
            for k in range(1, len(frames)):
                new = VGroup(*[Dot(g.ax.c2p(a, np.clip(b, -lim, lim)), radius=0.035, color=STRUCT)
                               for a, b in zip(xs, frames[k])])
                nl = label(rf"step ${snaps[k]:,}$".replace(",", "{,}"), font_size=22, color=GREY_A).move_to(cnt)
                idx = min(int(np.searchsorted(cv[:, 0], snaps[k])), len(cv) - 1)
                self.play(ReplacementTransform(cur, new), ReplacementTransform(cnt, nl),
                          dot.animate.move_to(ax2.ax.c2p(cv[idx, 0], cv[idx, 1])), run_time=0.7 * per)
                cur, cnt = new, nl
                self.wait(0.3 * per)
            self.play(Create(curve(ax2.ax, cv[:, 0], cv[:, 1], STRUCT, 3)))
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def resolution(self):
        fo = load("fno")
        R = list(fo["test_res"])
        lx = np.log2(R)
        E = {k: np.array([[fo[f"{k}_s{s}"]["err"][str(r)] for s in (0, 1, 2)] for r in R]) for k in ("fno", "cnn")}
        top = float(np.ceil(max(E["fno"].max(), min(E["cnn"].max(), 1.0)) * 10) / 10 + 0.05)
        g = axes([lx[0], lx[-1]], [0, top], x_length=6.0, y_length=3.6, xlabel=r"points the test is sampled at",
                 ylabel=r"relative error", xticks=list(lx), yticks=[0, top], xfmt=lambda v: f"{2 ** v:.0f}",
                 yfmt=lambda v: f"{v:.2f}", center=[-2.6, -0.1, 0])
        train_x = np.log2(int(fo["res"]))
        tl = DashedLine(g.ax.c2p(train_x, 0), g.ax.c2p(train_x, top), color=GREY_C)
        tlab = label(r"trained here", font_size=18, color=GREY_C).next_to(tl, UP, buff=0.05)
        objs = {}
        for k in ("fno", "cnn"):
            m = np.minimum(E[k].mean(1), top)
            objs[k] = VGroup(band(g.ax, lx, np.minimum(E[k].min(1), top), np.minimum(E[k].max(1), top),
                                  KIND_COLOR[k], 0.22), curve(g.ax, lx, m, KIND_COLOR[k], 3.5),
                             VGroup(*[Dot(g.ax.c2p(a, b), radius=0.05, color=KIND_COLOR[k]) for a, b in zip(lx, m)]))
        lg = legend([(STRUCT, r"Fourier neural operator"), (PLAIN, r"CNN, \ dilated, \ the same layout")],
                    font_size=20)
        lg.move_to([3.9, 1.6, 0])
        pred = fo["fno_s0"]["pred"]
        uT = np.asarray(fo["show_uT"])[1]
        x = np.linspace(0, 1, len(uT), endpoint=False)
        lim = float(np.ceil(np.abs(uT).max() * 12) / 10)
        g2 = axes([0, 1], [-lim, lim], x_length=4.2, y_length=2.2, xticks=[], yticks=[], center=[3.9, -1.3, 0])
        c_t = curve(g2.ax, x, uT, TRUE_C, 3)
        p_hi = np.asarray(pred["1024"])[1]
        c_p = curve(g2.ax, np.linspace(0, 1, len(p_hi), endpoint=False), p_hi, STRUCT, 2)
        g2l = label(r"FNO read at $1{,}024$ points", font_size=18, color=STRUCT).next_to(g2, UP, buff=0.08)
        ef, ec = E["fno"].mean(1), E["cnn"].mean(1)
        i_tr = R.index(int(fo["res"]))
        f_ratio = ef[-1] / ef[i_tr]
        fine = R[-1] // int(fo["res"])
        f_txt = (f"The Fourier neural operator's error stays at {100 * ef[i_tr]:.1f} percent on its own grid and "
                 f"{100 * ef[-1]:.1f} at {R[-1]:,} points, {fine} times finer" if f_ratio < 1.5 else
                 f"The Fourier neural operator's error grows from {100 * ef[i_tr]:.1f} percent on its own grid to "
                 f"{100 * ef[-1]:.1f} at {R[-1]:,} points")
        c_txt = (f"The CNN, at {100 * ec[i_tr]:.1f} percent on its own grid, reaches {100 * ec[-1]:.0f} percent at "
                 "the finest: its kernels, even dilated, are measured in grid points, so on a finer grid they see a "
                 "narrower stretch of the line" if ec[-1] > 2 * ec[i_tr] else
                 f"The CNN also transfers: {100 * ec[i_tr]:.1f} percent on its own grid, {100 * ec[-1]:.1f} at "
                 "the finest")
        coarse = (f"Below its training resolution, at {R[0]} points, the operator's error is {100 * ef[0]:.1f} "
                  "percent: so coarse a grid blurs the steep fronts the solution makes" if ef[0] > 1.5 * ef[i_tr] else
                  f"Even below its training resolution, at {R[0]} points, the operator's error is {100 * ef[0]:.1f} "
                  "percent")
        tag = note(r"computed: \ three seeds each \ (band: \ min--max), \ trained at $64$ points only", font_size=20)
        tag.to_corner(DR, buff=0.2)
        with self.voiceover(
            "Now the test that matters. Both networks were trained only at sixty-four points. Read them at "
            f"{R[0]} up to {R[-1]:,}. <bookmark mark='a'/> {f_txt}. <bookmark mark='b'/> {c_txt}. <bookmark "
            f"mark='c'/> {coarse}. FourCastNet, one of the first learned weather models, in 2022, was built on a "
            "variant of this Fourier layer."
        ) as vo:
            self.play(FadeIn(g), Create(tl), FadeIn(tlab), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(objs["fno"]), FadeIn(lg[0]), FadeIn(g2), Create(c_t), Create(c_p), FadeIn(g2l))
            vo.wait_until("b")
            self.play(FadeIn(objs["cnn"]), FadeIn(lg[1]))
            vo.wait_until("c")
            self.play(Indicate(objs["fno"][2][0]))
        self.wait(0.6)
        tk = take_away(r"learn the operator, \ not the grid: \ weights on frequencies \ transfer across resolutions")
        with self.voiceover(
            "Learn the operator, not the grid. Weights that belong to frequencies carry over to any resolution, "
            "which is what a model of the physical world should do. From fields to crystals."
        ):
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
