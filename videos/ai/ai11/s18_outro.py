from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, PART, SAY, SCHED_COLORS, load
from videos.ai.ai11.s13_race import standings


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def axes(xr, yr):
            return Axes(x_range=[*xr, (xr[1] - xr[0]) / 4], y_range=[*yr, (yr[1] - yr[0]) / 4], x_length=TW,
                        y_length=TH - 0.2, tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        # 1. four walkers on Rosenbrock's valley
        r = load("race3d")
        a1 = axes((-2, 2), (-1, 3))
        g1 = VGroup(a1)
        for n in r["names"]:
            P = np.asarray(r[f"path_{n}"])
            g1.add(VMobject(color=OPT_COLORS[n], stroke_width=2).set_points_as_corners([a1.c2p(*p) for p in P]))
        out.append((g1, r"four ways down", OPT_COLORS["adam"]))
        # 2. kappa against sqrt(kappa)
        q = load("quad")
        lk = np.log10(np.asarray(q["kappas"], float))
        a2 = axes((0, 3), (0, 4))
        g2 = VGroup(a2, *[curve(a2, lk, np.log10(np.asarray(q[f"iters_{m}"], float)), OPT_COLORS[m], 2.5)
                          for m in ("gd", "hb", "nesterov")])
        out.append((g2, r"$\kappa$ \ against \ $\sqrt{\kappa}$", OPT_COLORS["hb"]))
        # 3. the temperature
        t = load("temperature")
        T = np.log10(np.array([[e / b for b in t["batches"]] for e in t["etas"]]))
        M = np.log10(np.asarray(t["measured"]).mean(2))
        a3 = axes((T.min(), T.max()), (M.min(), M.max()))
        out.append((VGroup(a3, *[Dot(a3.c2p(x, y), radius=0.035, color=C.SURPRISE) for x, y in zip(T.ravel(), M.ravel())]),
                    r"SGD's temperature \ $\eta/B$", C.SURPRISE))
        # 4. the edge of stability
        e = load("eos")
        eta0 = float(e["etas"][0])
        c = np.asarray(e[f"curve{eta0:g}"])
        a4 = axes((0, 4000), (0, 2 / eta0 * 1.2))
        out.append((VGroup(a4, curve(a4, c[:, 0], np.minimum(c[:, 2], 2 / eta0 * 1.2), C.TRUE_P, 2.5),
                           DashedLine(a4.c2p(0, 2 / eta0), a4.c2p(4000, 2 / eta0), color=C.TRUE_P, stroke_width=1.5)),
                    r"the edge of stability", C.TRUE_P))
        # 5. Newton-Schulz
        m = load("ns")
        b = np.asarray(m["sv_grad"], float)
        b = b / b.max()
        h = np.asarray(m["hist_grad_hybrid"], float)[-1]
        a5 = axes((0, len(b)), (0, 1.3))
        out.append((VGroup(a5, curve(a5, np.arange(len(b)), b, GREY_B, 2), curve(a5, np.arange(len(h)), np.minimum(h, 1.3),
                                                                               OPT_COLORS["muon"], 2.5)),
                    r"Muon: \ singular values to $1$", OPT_COLORS["muon"]))
        # 6. the fair race
        rc = load("race")
        allc = {o: np.median(np.asarray(rc[f"curves_{o}"])[:, :, 1], 0) for o in rc["opts"]}
        xs = np.asarray(rc[f"curves_{rc['opts'][0]}"])[0, :, 0]
        lo = float(min(v.min() for v in allc.values())) - 0.05
        a6 = axes((0, xs.max()), (lo, lo + 1.2))
        out.append((VGroup(a6, *[curve(a6, xs[1:], np.clip(v[1:], lo, lo + 1.2), OPT_COLORS[o], 2) for o, v in allc.items()]),
                    r"the race, \ run fairly", WHITE))
        # 7. travel, then settle
        s = load("schedule")
        sd = list(s["seeds"])[0]
        const = np.asarray(s[f"const_{sd}"])
        lo7 = float(min(s[f"wsdfinal_{S}_{sd}"] for S in s["lengths"])) - 0.05
        a7 = axes((0, max(s["lengths"])), (lo7, lo7 + 0.6))
        g7 = VGroup(a7, curve(a7, const[1:, 0], np.clip(const[1:, 1], lo7, lo7 + 0.6), SCHED_COLORS["constant"], 2))
        for S in s["lengths"]:
            bc = np.asarray(s[f"wsdcurve_{S}_{sd}"])
            k0 = int(0.8 * S)
            pts = [(k0, float(np.interp(k0, const[:, 0], const[:, 1])))] + [tuple(p) for p in bc]
            g7.add(VMobject(color=SCHED_COLORS["wsd"], stroke_width=2.5).set_points_as_corners(
                [a7.c2p(x, min(max(y, lo7), lo7 + 0.6)) for x, y in pts]))
        out.append((g7, r"travel, \ then settle", SCHED_COLORS["wsd"]))
        # 8. weight decay's equilibrium
        q8 = load("equilibrium")
        top = max(np.asarray(q8[f"track_{w}"])[:, 1].max() for w in q8["wd"]) * 1.1
        a8 = axes((0, int(q8["steps"])), (0, top))
        cols = ["#7FD3FF", C.BITS, C.SURPRISE]
        g8 = VGroup(a8, *[curve(a8, np.asarray(q8[f"track_{w}"])[:, 0], np.asarray(q8[f"track_{w}"])[:, 1], col, 2)
                          for w, col in zip(q8["wd"], cols)])
        out.append((g8, r"$\|W\| \propto \sqrt{\eta/\lambda}$", C.BITS))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, \ in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        st = standings(load("race"))
        win = SAY[st[0][0]]
        with self.voiceover(
            f"Let's take stock. Gradient descent needs steps in proportion to the condition number, and momentum "
            "needs only its square root. A random batch makes each step cheap and noisy, and the noise is a "
            "temperature, eta over B, which sets the size of the cloud training ends in. At a fixed step, training "
            "raises the curvature to the edge of stability, two over eta, and stays there. Adam rescales every weight "
            "and in its limit is sign descent; Shampoo and Muon see whole matrices, and Muon's step, the steepest under the "
            "spectral norm, sets every singular value to one with a polynomial. In a fair race on our own model, "
            f"{win} came first. A high learning rate travels down the river and a falling one settles, and weight "
            "decay quietly sets the size of every normalized matrix."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"the critical batch, \ learning rates across widths, \ WSD in scaling laws", [12]),
            (r"AdamW, \ warmup and decay in our transformers", [13, 14]),
            (r"Muon, \ QK-norm and QK-clip, \ loss spikes at scale", [18]),
            (r"optimizers in reinforcement learning and fine-tuning", [26, 27]),
        ], font_size=24)
        with self.voiceover(
            "All of this comes back. Part twelve measures the critical batch and keeps a learning rate as models "
            "grow wider and deeper. The transformers of parts thirteen and fourteen train with AdamW and a warmup. Part "
            "eighteen trains a model with the full modern recipe, Muon included, and keeps it stable at scale. And reinforcement "
            "learning and fine-tuning, in parts twenty-six and twenty-seven, run on the same optimizers."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"For an $L$-smooth $f$, show $f(x - \nabla f(x)/L) \le f(x) - \|\nabla f(x)\|^2/2L$. \ If also "
            r"$\|\nabla f\|^2 \ge 2\mu(f - f^*)$, deduce $f(x_k) - f^* \le (1 - \mu/L)^k (f(x_0) - f^*)$.",
            r"The heavy ball on $f = \tfrac{\lambda}{2}x^2$: \ show the roots of $z^2 - (1 + \beta - \eta\lambda)z + \beta$ "
            r"have modulus $\sqrt\beta$ when complex, \ and find $\eta, \beta$ that make this hold for all $\lambda \in "
            r"[\mu, L]$. \ How many steps for $\kappa = 10^4$, \ against gradient descent?",
            r"SGD on $f = \tfrac{\lambda}{2}x^2$ with gradient noise of variance $\sigma^2/B$: \ show the stationary "
            r"variance is $\dfrac{\eta\sigma^2}{B\,\lambda\,(2 - \eta\lambda)}$, \ and that it depends on $\eta$ and $B$ "
            r"only through $\eta/B$ when $\eta\lambda \ll 1$.",
            r"Show that $\min_{\|\Delta\|_\infty \le \eta} g^\top\Delta = -\eta\|g\|_1$ is attained at "
            r"$-\eta\operatorname{sign}(g)$, \ and that $\min_{\|\Delta\|_{2 \to 2} \le \eta}\langle G, \Delta\rangle = "
            r"-\eta\|G\|_*$ (the nuclear norm) is attained at $-\eta\,UV^\top$.",
            r"For $p(\sigma) = \tfrac32\sigma - \tfrac12\sigma^3$, \ show $p(1) = 1$, $p'(1) = 0$, \ and that "
            r"$e = 1 - \sigma$ obeys $e \mapsto \tfrac32 e^2 + O(e^3)$. \ For $2\sigma - \tfrac32\sigma^3 + \tfrac12\sigma^5$, "
            r"show $p'(1) = p''(1) = 0$: \ what is the order of convergence?",
            r"Decoupled decay $W_{t+1} = (1 - \eta\lambda)W_t - \eta u_t$ with $u_t \perp W_t$ and "
            r"$\langle u_t, u_{t+k}\rangle = \|u\|^2\beta^{|k|}$: \ show $\mathbb{E}\|W\|^2 \to "
            r"\dfrac{\eta\|u\|^2}{2\lambda}\dfrac{1 + \beta}{1 - \beta}$ for small $\eta\lambda$.",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems, from gradient descent's rate to weight decay's equilibrium. Pause here and work "
            "through them; full solutions are in this part's notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 12, \ The Mathematics of Scale", font_size=40).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[15, 25, 2], y_range=[1.5, 4.0, 0.5], x_length=9.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(DOWN * 0.4)
        lines = VGroup()
        for k, n in enumerate(np.linspace(16, 22, 5)):
            xs = np.linspace(15, 25, 80)
            ys = np.clip(1.7 + 0.6 * np.exp(-0.25 * (n - 16)) + 1.8 * np.exp(-0.7 * (xs - 15)) * np.exp(-0.1 * (n - 16)), 1.5, 4.0)
            lines.add(VMobject(color=interpolate_color(ManimColor(C.TRUE_P), ManimColor(C.BITS), k / 4), stroke_width=3)
                      .set_points_smoothly([ax.c2p(x, y) for x, y in zip(xs, ys)]))
        env = DashedLine(ax.c2p(15, 3.9), ax.c2p(25, 1.6), color=WHITE, stroke_width=2)
        tag = label(r"loss against compute, \ for models of growing size \ (schematic)", font_size=24, color=GREY_B)
        tag.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Next time: the mathematics of scale. Why bigger models get better so predictably, how to split a budget "
            "between parameters and data, and how to choose a learning rate once and keep it as the model grows. "
            "<bookmark mark='a'/> Straight lines on log–log plots, and what they promise."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(tag))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(env))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"J.~Nocedal \& S.~J.~Wright, \textit{Numerical Optimization}, 2nd ed.\ (2006); \ Y.~Nesterov, "
            r"\textit{Lectures on Convex Optimization} (2018)",
            r"L.~Bottou, F.~E.~Curtis \& J.~Nocedal, \textit{Optimization Methods for Large-Scale Machine Learning} (2018); "
            r"\ S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), ch.~6",
        ]
        papers = [
            r"Cauchy (1847); \ Robbins \& Monro (1951); \ Polyak (1964); \ Nesterov (1983); \ Rumelhart, Hinton \& "
            r"Williams (1986); \ Polyak \& Juditsky (1992); \ LeCun et al.\ (1998); \ Lessard, Recht \& Packard (2016)",
            r"Duchi, Hazan \& Singer (2011); \ Tieleman \& Hinton (2012); \ Kingma \& Ba (2014); \ Loshchilov \& Hutter "
            r"(2016, 2017); \ Chen et al., \textit{Lion} (2023)",
            r"Li, Tai \& E (2017); \ Mandt, Hoffman \& Blei (2017); \ Smith \& Le (2018); \ Goyal et al.\ (2017); \ Keskar "
            r"et al.\ (2017); \ Dinh et al.\ (2017); \ Malladi et al.\ (2022)",
            r"Cohen et al.\ (2021, 2022); \ Damian, Nichani \& Lee (2022); \ Amari (1998); \ Martens \& Grosse (2015); \ "
            r"Gupta, Koren \& Singer (2018); \ Vyas et al., \textit{SOAP} (2024)",
            r"Jordan et al., \textit{Muon} (2024); \ Bernstein \& Newhouse (2024); \ Liu et al.\ (2025); \ Kimi Team, "
            r"\textit{Kimi K2} (2025); \ Amsel et al.\ (2025); \ DeepSeek-AI, \textit{DeepSeek-V4} (2026)",
            r"Hu et al., \textit{MiniCPM} (2024); \ Wen et al., \textit{River Valley} (2024); \ Defazio et al.\ (2024); \ "
            r"Kasimbeg et al., \textit{AlgoPerf} (2025); \ Wen, Hall, Ma \& Liang (2025); \ Khona et al.\ (2026)",
            r"Pascanu, Mikolov \& Bengio (2013); \ van Laarhoven (2017); \ Kosson, Messmer \& Jaggi (2024)",
        ]
        card = reference_card(books, papers, font_size=19)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Every run is computed here; \ every number on screen "
                    r"is computed or cited; \ schematics are labelled.", font_size=18).to_edge(DOWN, buff=0.2)
        credit = note(narration_credit(), font_size=18).next_to(data, UP, buff=0.08)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.12:
            card.shift(UP * (credit.get_top()[1] + 0.12 - card.get_bottom()[1]))
        if card.get_top()[1] > 3.9:
            card.scale_to_fit_height(card.height - (card.get_top()[1] - 3.9)).align_to(credit, DOWN).shift(UP * (credit.height + 0.25))
        with self.voiceover(
            "Bottou, Curtis and Nocedal's survey is the best single account of stochastic optimization, and Jeremy "
            "Bernstein's essays explain Muon's geometry. Thanks for watching, and see you in part twelve."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
