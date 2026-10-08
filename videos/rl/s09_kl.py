from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import (Mono, Plot, Simplex, exact_tag, label, load, mtex, note, pct_fmt, real_tag, source,
                              token_color, why)


def tilt(p, r, beta):
    w = p * np.exp((r - r.max()) / beta)
    return w / w.sum()


class KLOptimum(VoiceoverScene):
    def construct(self):
        self.t = load("tilt")
        self.s = load("simplex")
        self.k = load("kl_est")
        self.derive()
        self.bars()
        self.simplex()
        self.frontier()
        self.estimators()

    # ------------------------------------------------------------------
    def derive(self):
        K, P, R = C.KL, C.RL_POLICY, C.REWARD
        L = [
            mtex(r"\max_\pi\;", r"\mathbb{E}_{y\sim\pi}\big[r(y)\big]", r"-", r"\beta\, \mathrm{KL}\big(\pi \,\|\, \pi_{\text{ref}}\big)", font_size=42),
            mtex(r"=", r"\sum_y \pi(y)\Big[\, r(y) - \beta \log\frac{\pi(y)}{\pi_{\text{ref}}(y)} \Big]", font_size=40),
            mtex(r"=", r"-\beta \sum_y \pi(y) \log \frac{\pi(y)}{\pi_{\text{ref}}(y)\, e^{r(y)/\beta}}", font_size=40),
            mtex(r"=", r"-\beta\, \mathrm{KL}\big(\pi \,\|\, \pi^\star\big)", r"+", r"\beta \log Z", font_size=40),
        ]
        L[0][1].set_color(R)
        L[0][3].set_color(K)
        L[3][1].set_color(K)
        L[0].to_edge(UP, buff=0.45).shift(LEFT * 1.0)
        for prev, cur in zip(L, L[1:]):
            cur.next_to(prev, DOWN, buff=0.32, aligned_edge=LEFT)
            cur.shift(RIGHT * (L[0][1].get_x() - 0.6 - cur[0].get_x()))
        reasons = [why(r"write KL as a sum"), why(r"fold $r$ into the log: $r = \beta \log e^{r/\beta}$"),
                   why(r"normalize: $Z = \sum_y \pi_{\text{ref}}(y)\, e^{r(y)/\beta}$")]
        for r_, line in zip(reasons, L[1:]):
            r_.next_to(line, RIGHT, buff=0.5)
            if r_.get_right()[0] > 6.9:
                r_.shift(LEFT * (r_.get_right()[0] - 6.9))
        star = mtex(r"\pi^\star(y)", r"=", r"\frac{1}{Z}\,", r"\pi_{\text{ref}}(y)", r"\, e^{\,r(y)/\beta}", font_size=48)
        star[0].set_color(YELLOW)
        star[3].set_color(C.REFERENCE)
        star[4].set_color(R)
        box = SurroundingRectangle(star, color=YELLOW, buff=0.2, corner_radius=0.1)
        sg = VGroup(star, box).to_edge(DOWN, buff=0.45)
        gibbs = label(r"KL $\ge 0$, and $= 0$ only when $\pi = \pi^\star$", font_size=26, color=GREY_A).next_to(sg, UP, buff=0.15)
        with self.voiceover(
            "Here is the objective RLHF actually optimizes: expected reward, minus beta times the KL divergence "
            "from the reference policy. <bookmark mark='1'/> Write the KL as a sum over answers. "
            "<bookmark mark='2'/> Now fold the reward into the logarithm, as the log of e to the r over beta. "
            "<bookmark mark='3'/> Normalize that tilted distribution, with a constant Z, and the whole objective "
            "becomes minus beta times a KL divergence to a single distribution, plus a constant."
        ) as vo:
            self.play(Write(L[0]), run_time=1.6)
            for k, mark in enumerate(["1", "2", "3"]):
                vo.wait_until(mark)
                self.play(FadeIn(L[k + 1], shift=DOWN * 0.1), FadeIn(reasons[k]))
        with self.voiceover(
            "A KL divergence is never negative, and it's zero only when the two distributions match. So the best "
            "possible policy is exactly this one: <bookmark mark='s'/> the reference, reweighted by e to the reward "
            "over beta. No training needed to know the answer; training is just a way to get there."
        ) as vo:
            self.play(FadeIn(gibbs))
            vo.wait_until("s")
            self.play(Write(star), Create(box))
        self.wait(0.3)
        self.star = sg
        self.clear_scene(sg)
        self.play(sg.animate.scale(0.75).to_corner(UL, buff=0.35))

    # ------------------------------------------------------------------
    def bars(self):
        ex = self.t["example"]
        leaves = sorted(ex["leaves"], key=lambda L: -L["p"])[:7]
        p = np.array([L["p"] for L in leaves])
        rest = 1.0 - p.sum()
        p = np.append(p, max(rest, 0.0))
        r = np.array([L["r"] for L in leaves] + [0.0])
        texts = [L["text"] for L in leaves] + ["other"]
        n = len(p)
        W, H = 1.45, 4.2
        base_y = -2.0
        x0 = -(n - 1) / 2 * W + 0.9
        beta = ValueTracker(1.0)  # log10(beta)

        def draw():
            q = tilt(p, r, 10 ** beta.get_value())
            g = VGroup()
            for i, v in enumerate(q):
                col = C.REWARD if r[i] > 0 else (GREY_B if texts[i] == "other" else C.PENALTY)
                b = Rectangle(width=W * 0.62, height=max(0.01, H * v), stroke_width=0, fill_color=col, fill_opacity=0.85)
                b.move_to([x0 + i * W, base_y + H * v / 2, 0])
                g.add(b)
                g.add(MathTex(f"{v:.2f}", font_size=22, color=GREY_A).next_to(b, UP, buff=0.06))
            return g
        bars = always_redraw(draw)
        names = VGroup()
        for i, t in enumerate(texts):
            if t == "other":
                m = label(r"other", font_size=20, color=GREY_B)
            else:
                think = t.startswith(">")
                show = (t[:7] + "…") if len(t) > 8 else t
                m = Mono(show.replace(">", "→"), font_size=15, color=C.WORK_TOK if think else WHITE)
            m.move_to([x0 + i * W, base_y - 0.3, 0])
            names.add(m)
        axis = Line([x0 - W * 0.6, base_y, 0], [x0 + (n - 1) * W + W * 0.6, base_y, 0], color=GREY_C)
        bl = always_redraw(lambda: mtex(rf"\beta = {10 ** beta.get_value():.3g}", font_size=38, color=C.KL)
                           .move_to([4.6, 2.2, 0], aligned_edge=LEFT))
        pr = always_redraw(lambda: mtex(rf"P(\text{{right}}) = {tilt(p, r, 10 ** beta.get_value())[r > 0].sum():.2f}",
                                        font_size=32, color=C.REWARD).move_to([4.6, 1.55, 0], aligned_edge=LEFT))
        head = label(rf"The model's real answers to ${ex['a']} + {ex['b']}$, before any RL", font_size=28)
        head.to_edge(UP, buff=0.35).shift(RIGHT * 1.6)
        tag = real_tag(r"real probabilities, exact tilt")
        ratio = label(r"every right answer is multiplied by the same factor: their proportions never change",
                      font_size=24, color=YELLOW).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Let's apply it to a real distribution: the answers our pocket model gives to one problem, before any "
            "reinforcement learning. Green answers are right, red ones are wrong, and the long ones show their work. "
            "<bookmark mark='b'/> With a large beta, the leash is tight and nothing changes. As beta shrinks, every "
            "right answer gets multiplied by the same factor, and the wrong ones fade. <bookmark mark='z'/> At "
            "small beta, the optimal policy is essentially always right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(axis), FadeIn(names), FadeIn(bars), FadeIn(bl), FadeIn(pr))
            vo.wait_until("b")
            self.play(beta.animate.set_value(-0.6), run_time=4.0, rate_func=smooth)
            vo.wait_until("z")
            self.play(beta.animate.set_value(-2.0), run_time=2.5, rate_func=smooth)
        with self.voiceover(
            "Notice what the tilt can't do. Right answers keep the proportions the reference gave them, and an "
            "answer the reference would never write gets probability zero, whatever its reward. The optimum only "
            "reweights what the starting model could already say."
        ) as vo:
            self.play(FadeIn(ratio))
        self.wait(0.3)
        self.clear_scene(self.star)

    # ------------------------------------------------------------------
    def simplex(self):
        s = self.s
        r = np.array(s["r"], float)
        S = Simplex(side=5.6, rewards=r).move_to(RIGHT * 2.6 + DOWN * 0.4)
        tl = np.array(s["tilt"], float)
        nat = np.array(s["natural"], float)
        tcurve = S.path(tl, C.KL, stroke_width=8)
        ncurve = S.path(nat, YELLOW, stroke_width=3)
        dashed = DashedVMobject(ncurve, num_dashes=60)
        p0 = Dot(S.p2s(s["pi0"]), radius=0.08, color=C.REFERENCE)
        p0l = label(r"$\pi_{\text{ref}}$", font_size=26, color=C.REFERENCE).next_to(p0, RIGHT, buff=0.1)
        beta = ValueTracker(0)

        def mover():
            k = int(np.clip(beta.get_value(), 0, len(tl) - 1))
            return Dot(S.p2s(tl[k]), radius=0.09, color=C.KL)
        mv = always_redraw(mover)
        l1 = label(r"$\pi^\star_\beta$ as $\beta$ goes from $\infty$ to $0$", font_size=26, color=C.KL)
        l2 = label(r"the natural-gradient path from before (dashed)", font_size=26, color=YELLOW)
        eq = mtex(r"\text{natural gradient on logits: } z_t = z_0 + t\, r", r"\;\Rightarrow\;",
                  r"\pi_t \propto \pi_{\text{ref}}\, e^{t\, r}", font_size=30)
        side = VGroup(l1, l2, eq).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        with self.voiceover(
            "Back on the triangle of three-action policies, the optimal policies for every beta trace out a single "
            "curve, from the reference toward the best corner. <bookmark mark='n'/> And here's a surprise: it's "
            "exactly the path the natural gradient followed. Natural gradient ascent on the logits adds a multiple "
            "of the reward, so after time t the policy is the reference tilted by e to the t r. Training longer "
            "plays the same role as loosening the leash."
        ) as vo:
            self.play(FadeIn(S), FadeIn(p0), FadeIn(p0l), FadeIn(exact_tag()))
            self.play(FadeIn(mv), FadeIn(l1))
            self.play(beta.animate.set_value(len(tl) - 1), Create(tcurve), run_time=3.0)
            vo.wait_until("n")
            self.play(Create(dashed), FadeIn(l2), run_time=2.0)
            self.play(FadeIn(eq))
        self.wait(0.3)
        self.clear_scene(self.star)

    # ------------------------------------------------------------------
    def frontier(self):
        t = self.t
        KLb, Rb = np.array(t["KL_beta"], float), np.array(t["R_beta"], float)
        pts = t["points"]
        kmax = max(1.0, float(np.ceil(max(p["KL"] for p in pts) * 1.1 / 0.25) * 0.25))
        m = KLb <= kmax
        plot = Plot(x_range=(0, kmax), y_range=(0.5, 1.0), width=8.0, height=4.4, x_ticks=list(np.arange(0, kmax + 1e-9, 0.25)),
                    y_ticks=[0.5, 0.75, 1.0], y_fmt=pct_fmt, x_label=r"KL from the starting model (nats per answer)",
                    y_label=r"chance of being right")
        plot.move_to(DOWN * 0.4 + LEFT * 0.6)
        xs_f = np.append(KLb[m], kmax)
        ys_f = np.append(Rb[m], Rb[m][-1])
        curve = plot.line(xs_f, ys_f, color=YELLOW, stroke_width=5)
        kl_full = float(KLb[m][-1])
        last = pts[-1]
        assert last["KL"] > 1.5 * kl_full, (last, kl_full)
        cl = label(r"the best possible trade-off: $\pi^\star_\beta$ for every $\beta$", font_size=24, color=YELLOW)
        cl.move_to(plot.c2p(kmax * 0.62, 0.66))
        dots = VGroup(*[Dot(plot.c2p(p["KL"], p["R"]), radius=0.07, color=C.RL_POLICY) for p in pts])
        path = plot.line([p["KL"] for p in pts], [p["R"] for p in pts], color=C.RL_POLICY, stroke_width=2)
        dl = label(r"our RL run (GRPO, no KL penalty), at its checkpoints", font_size=24, color=C.RL_POLICY)
        dl.move_to(plot.c2p(kmax * 0.62, 0.585))
        head = label(rf"Reward vs.\ distance, averaged over {t['n_problems']} problems", font_size=30).to_edge(UP, buff=0.3).shift(RIGHT * 1.5)
        with self.voiceover(
            "Averaged over many problems, the optimal policies give a frontier: the most reward you can possibly "
            f"have at each distance from the starting model. Being right every time costs only {kl_full:.2f} nats. "
            "<bookmark mark='r'/> Our actual training run, which had no KL penalty at all, sits below the frontier, as "
            f"every policy must. It ends almost as accurate, but about {last['KL'] / kl_full:.0f} times farther from "
            "where it started than it needed to be: unlike the optimum, it also reshuffled its right answers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(real_tag(r"exact frontier; real RL checkpoints")))
            self.play(Create(curve), FadeIn(cl), run_time=2)
            vo.wait_until("r")
            self.play(Create(path), LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.15), FadeIn(dl), run_time=2)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def estimators(self):
        k = self.k
        defs = VGroup(
            mtex(r"k_1 = -\log \rho", font_size=34, color=C.PENALTY),
            mtex(r"k_2 = \tfrac12 (\log \rho)^2", font_size=34, color=C.BASELINE),
            mtex(r"k_3 = (\rho - 1) - \log \rho", font_size=34, color=C.KL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rdef = mtex(r"\rho = \frac{\pi_{\text{ref}}(y)}{\pi_\theta(y)},\quad y \sim \pi_\theta", font_size=32)
        col = VGroup(rdef, defs).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT, buff=0.6).shift(UP * 0.8)
        plot = Plot(x_range=(-2.5, 2.5), y_range=(-2.5, 3.5), width=5.4, height=3.8, x_ticks=[-2, -1, 0, 1, 2],
                    y_ticks=[-2, 0, 2], x_label=r"$\log \rho$")
        plot.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.65)
        xs = np.linspace(-2.5, 2.5, 300)
        c1 = plot.line(xs, -xs, color=C.PENALTY, stroke_width=3)
        c2 = plot.line(xs, 0.5 * xs**2, color=C.BASELINE, stroke_width=3)
        k3 = np.exp(xs) - 1 - xs
        mm = k3 < 3.5
        c3 = plot.line(xs[mm], k3[mm], color=C.KL, stroke_width=4)
        zero = plot.hline(0, color=GREY_D)
        a = k["mu0.1"]
        rows = [(r"$k_1$", a["k1"]["bias"], a["k1"]["std"], C.PENALTY), (r"$k_2$", a["k2"]["bias"], a["k2"]["std"], C.BASELINE),
                (r"$k_3$", a["k3"]["bias"], a["k3"]["std"], C.KL)]
        assert abs(a["k1"]["std"] - 20) < 0.5 and abs(a["k3"]["std"] - 1.42) < 0.02
        tab = VGroup(VGroup(label(r"", font_size=24), label(r"bias", font_size=24, color=GREY_A),
                            label(r"spread", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.7))
        for nm, bias, std, col_ in rows:
            tab.add(VGroup(label(nm, font_size=26, color=col_), label(rf"${bias:+.3f}$", font_size=26),
                           label(rf"${std:.2f}$", font_size=26)).arrange(RIGHT, buff=0.7))
        for i, row in enumerate(tab):  # a fixed grid: the header's first cell is empty, so don't align rows by their edges
            for j, cell in enumerate(row):
                cell.move_to([j * 1.6, -0.45 * i, 0], aligned_edge=LEFT)
        tcap = label(r"true KL $= 0.005$; numbers relative to it (2 million samples)", font_size=22, color=GREY_A)
        tg = VGroup(tcap, tab).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(col, DOWN, buff=0.45).align_to(col, LEFT)
        head = label(r"Estimating the KL from samples", font_size=30).to_edge(UP, buff=0.3)
        src = source(r"J.\ Schulman, \emph{Approximating KL Divergence}, 2020; reproduced here by Monte Carlo")
        with self.voiceover(
            "In practice the KL itself has to be estimated from samples, one token at a time. John Schulman's three "
            "estimators are now in nearly every RL library. <bookmark mark='1'/> The obvious one, minus the log ratio, is "
            "unbiased, but it's negative half the time and very noisy. <bookmark mark='2'/> Half the squared log "
            "ratio is always positive, but slightly biased. <bookmark mark='3'/> And k3 adds a term whose average is "
            "exactly zero, rho minus one: it stays unbiased, it's never negative, and it's far less noisy. "
            "<bookmark mark='t'/> For two close distributions, its spread is fourteen times smaller."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rdef), FadeIn(plot), Create(zero), FadeIn(src))
            for k_, mark in enumerate(["1", "2", "3"]):
                vo.wait_until(mark)
                self.play(FadeIn(defs[k_]), Create([c1, c2, c3][k_]))
            vo.wait_until("t")
            self.play(FadeIn(tg))
        warn = VGroup(
            label(r"GRPO puts $k_3$ in the loss.\ Differentiated, it pulls toward the \emph{reversed} KL,", font_size=24),
            label(r"$\mathrm{KL}(\pi_{\text{ref}} \,\|\, \pi_\theta)$; DeepSeek-V3.2 multiplies it by $\pi_\theta/\pi_{\text{old}}$ to fix that.", font_size=24),
            label(r"Many reasoning recipes simply set $\beta = 0$ (DAPO, OLMo 3; TRL's default).", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        bg = BackgroundRectangle(warn, color=BACKGROUND, fill_opacity=0.95, buff=0.2)
        wg = VGroup(bg, warn).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "One subtlety. An estimator with the right value can have the wrong gradient. GRPO puts k3 directly in "
            "its loss, and differentiating it pulls the policy toward the reversed KL, from reference to policy. "
            "DeepSeek's V3.2 corrects this by multiplying in the importance ratio. And many reasoning recipes "
            "skip the leash entirely, and set beta to zero."
        ):
            self.play(FadeOut(tg), FadeIn(wg))
        self.wait(0.4)
        self.clear_scene()
