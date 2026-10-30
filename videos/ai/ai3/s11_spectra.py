from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, MPC, RANDOM, TRAINED, chapter, dots_on, hist_bars, load

KC = {"attn": C.QUERY, "attn_out": C.VALUE, "mlp_in": C.MLP, "mlp_out": C.TRUE_P}
KN = {"attn": r"attention in", "attn_out": r"attention out", "mlp_in": r"MLP in", "mlp_out": r"MLP out"}


def mp_density(x, q):
    lo, hi = (1 - math.sqrt(q)) ** 2, (1 + math.sqrt(q)) ** 2
    x = np.asarray(x, float)
    d = np.zeros_like(x)
    m = (x > lo) & (x < hi)
    d[m] = np.sqrt((hi - x[m]) * (x[m] - lo)) / (2 * math.pi * q * x[m])
    return d


class Spectra(VoiceoverScene):
    def construct(self):
        chapter(self, 10, r"Random matrices and trained weights", r"What does training write into a matrix?",
                "Chapter ten. Random matrices, and what training writes into a network's weights.")
        self.law()
        self.trained()
        self.tails()
        self.novels()

    # ------------------------------------------------------------------
    def law(self):
        d = load("mp")["random"]
        ev, q, lo, hi = np.asarray(d["ev"]), float(d["q"]), float(d["lo"]), float(d["hi"])
        thm = theorem_card(r"the Marchenko--Pastur law",
                           r"$W$ is $N \times M$ with independent entries of mean $0$ and variance $1$. \ As "
                           r"$N, M \to \infty$ with $N/M \to q$, \ the eigenvalues of $WW^{\top}/M$ fill "
                           r"$\big[(1-\sqrt q)^2,\ (1+\sqrt q)^2\big]$ \ with density \ "
                           r"$\dfrac{\sqrt{(\lambda_+ - \lambda)(\lambda - \lambda_-)}}{2\pi q \lambda}$.",
                           who=r"V.~Marchenko \& L.~Pastur (1967)", width=6.4).to_corner(UL, buff=0.25)
        g = axes([0, 2.6, 0.5], [0, 1.1, 0.5], x_length=5.6, y_length=3.4, xticks=[0, 0.5, 1, 1.5, 2, 2.5],
                 yticks=[0, 0.5, 1.0], xlabel=r"eigenvalue of $WW^{\top}/M$", ylabel=r"density",
                 center=[3.4, -0.9, 0])
        ax = g.ax
        edges = np.linspace(0, 2.6, 53)
        cnt, _ = np.histogram(ev, bins=edges)
        dens = cnt / (len(ev) * (edges[1] - edges[0]))
        bars = hist_bars(ax, edges, dens, RANDOM, 0.7)
        xs = np.linspace(lo + 1e-4, hi - 1e-4, 200)
        mp = curve(ax, xs, mp_density(xs, q), MPC, 4)
        edge_l = VGroup(DashedLine(ax.c2p(hi, 0), ax.c2p(hi, 1.0), color=MPC, stroke_width=2),
                        MathTex(rf"\lambda_+ = {hi:.2f}", font_size=24, color=MPC).next_to(ax.c2p(hi, 1.0), UP, buff=0.05))
        cap = note(rf"computed: \ one random $768 \times 3072$ matrix, \ $q = {q:g}$").next_to(g, DOWN, buff=0.1)
        wig = history_card(1955, r"E.~Wigner",
                           r"modelled the energy levels of heavy nuclei by a random matrix's eigenvalues: \ "
                           r"the semicircle law", color=HIST, width=6.4).to_corner(DL, buff=0.25)
        above = int(d["above"])
        esc = "Not one eigenvalue escapes it." if above == 0 else f"Only {above} lie beyond it."
        with self.voiceover(
            "What does pure noise look like, through its eigenvalues? <bookmark mark='a'/> In 1955 Eugene Wigner "
            "modelled heavy nuclei's energy levels with a random matrix's eigenvalues, and found a law. "
            "<bookmark mark='b'/> In 1967 Marchenko and Pastur found it for rectangular matrices: the eigenvalues of W W "
            "transpose over M fill a fixed interval, in a fixed shape, set by the aspect ratio alone. We'll check it "
            "rather than prove it. <bookmark mark='c'/> A random 768 by 3,072 matrix, GPT-2's MLP shape: "
            f"{len(ev)} eigenvalues, <bookmark mark='d'/> and the law on top. {esc}"
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(wig, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(cap), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(mp), Create(edge_l), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trained(self):
        m = load("mp")
        s, sh = m["show"], m["shuffled"]
        ev, es = np.asarray(s["ev"]), np.asarray(sh["ev"])
        q, lo, hi = float(s["q"]), float(s["lo"]), float(s["hi"])
        L0, L1 = -2.6, 1.5
        g = axes([L0, L1, 0.5], [0, 2.4, 1], x_length=9.0, y_length=4.0, xticks=[-2, -1, 0, 1],
                 xfmt=lambda v: f"10^{{{int(v)}}}" if v not in (0, 1) else ("1" if v == 0 else "10"), yticks=[0, 1, 2],
                 xlabel=r"eigenvalue of $WW^{\top}/M$ \ (log scale)", ylabel=r"density, per unit of $\log_{10}\lambda$",
                 center=[-0.3, -0.6, 0])
        ax = g.ax
        edges = np.linspace(L0, L1, 72)
        w = edges[1] - edges[0]

        def bars(e, col, op):
            c, _ = np.histogram(np.log10(np.maximum(e, 10 ** L0)), bins=edges)
            return hist_bars(ax, edges, c / (len(e) * w), col, op)

        btr, bsh = bars(ev, TRAINED, 0.75), bars(es, RANDOM, 0.6)
        xs = np.linspace(math.log10(lo) + 1e-3, math.log10(hi) - 1e-3, 200)
        mp = curve(ax, xs, mp_density(10 ** xs, q) * 10 ** xs * math.log(10), MPC, 4)
        edge = DashedLine(ax.c2p(math.log10(hi), 0), ax.c2p(math.log10(hi), 2.2), color=MPC, stroke_width=2)
        el = MathTex(r"\lambda_+", font_size=26, color=MPC).next_to(ax.c2p(math.log10(hi), 2.2), UP, buff=0.05)
        above = int(sum(e > hi * 1.02 for e in ev))
        top = float(ev.max() / hi)
        brace = BraceBetweenPoints(ax.c2p(math.log10(hi), 0.35), ax.c2p(math.log10(ev.max()), 0.35), UP, color=TRAINED)
        bl = label(rf"${above}$ eigenvalues beyond the edge; \\ the largest ${top:.1f}\times$ it", font_size=24,
                   color=TRAINED).move_to(ax.c2p(math.log10(hi) + 1.05, 1.55))
        bl.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.05)
        head = label(rf"GPT-2, \ layer ${int(s['layer'])}$, \ the MLP's first matrix ($768 \times 3072$)", font_size=32)
        head.to_edge(UP, buff=0.3)
        leg = legend([(TRAINED, r"trained"), (RANDOM, r"the same numbers, shuffled"), (MPC, r"Marchenko--Pastur")],
                     font_size=22).move_to([4.9, 2.0, 0])
        sh_above = int(sh["above"])
        shuf = ("The escapees vanish: the spectrum falls back onto the law." if sh_above == 0 else
                f"Only {sh_above} remain beyond the edge.")
        with self.voiceover(
            f"Now a trained matrix: GPT-2's layer {int(s['layer'])}, the first matrix of its MLP, scaled the same way. "
            "<bookmark mark='a'/> Most eigenvalues sit in a bulk much like the law. <bookmark mark='b'/> But "
            f"{above} have escaped beyond the edge, the largest {top:.1f} times past it. <bookmark mark='c'/> Just "
            f"unusual values? Shuffle the same numbers into random places. {shuf} The information is in the "
            "arrangement: a few strong directions, learned."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in btr], lag_ratio=0.01), Create(mp), run_time=2.0)
            self.play(Create(edge), FadeIn(el))
            vo.wait_until("b")
            self.play(GrowFromCenter(brace), FadeIn(bl))
            vo.wait_until("c")
            self.play(btr.animate.set_opacity(0.18), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bsh], lag_ratio=0.01),
                      run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tails(self):
        m = load("mp")
        rows = m["gpt2"]
        s = m["show"]
        g = axes([-0.5, 11.5, 1], [0, 8, 2], x_length=7.6, y_length=4.0, xticks=list(range(12)), yticks=[0, 2, 4, 6, 8],
                 xlabel=r"layer", ylabel=r"fitted tail exponent $\alpha$ \ ($\rho(\lambda) \propto \lambda^{-\alpha}$)",
                 center=[-2.0, -0.6, 0])
        ax = g.ax
        band = Polygon(ax.c2p(-0.5, 1.5), ax.c2p(11.5, 1.5), ax.c2p(11.5, 5), ax.c2p(-0.5, 5), stroke_width=0,
                       fill_color=MPC, fill_opacity=0.12)
        bl = label(r"Martin \& Mahoney's range for \\ well-trained layers: \ $1.5$ to $5$", font_size=20, color=MPC)
        bl.next_to(ax.c2p(11.5, 5), UR, buff=0.1).shift(LEFT * 0.2)
        dots = VGroup()
        off = {"attn": -0.24, "attn_out": -0.08, "mlp_in": 0.08, "mlp_out": 0.24}
        for r in rows:
            dots.add(Dot(ax.c2p(r["layer"] + off[r["kind"]], min(r["alpha"], 7.9)), radius=0.06, color=KC[r["kind"]]))
        leg = legend([(KC[k], KN[k]) for k in KC], font_size=20).move_to([4.8, -1.2, 0])
        n_in = sum(1.5 <= r["alpha"] <= 5 for r in rows)
        rule = MathTex(r"\rho(\lambda) \propto \lambda^{-\alpha}, \quad \lambda > \lambda_{\min}", font_size=30)
        rule.to_edge(UP, buff=0.35)
        fit = label(r"fitted by maximum likelihood; \ $\lambda_{\min}$ chosen by the best Kolmogorov--Smirnov "
                    r"distance", font_size=20, color=GREY_A).next_to(rule, DOWN, buff=0.12)
        with self.voiceover(
            "The escapees thin out slowly, like a power law: density falling as lambda to the minus alpha. "
            "<bookmark mark='a'/> In 2019 Charles Martin and Michael Mahoney fitted such tails across hundreds of "
            "trained networks: exponents nearly always between 1.5 and 5, and within a family, heavier tails went with "
            f"better test accuracy. <bookmark mark='b'/> Fitted to all 48 of GPT-2's matrices: {n_in} fall in that "
            f"range; our layer has alpha {s['alpha']:.2f}. Random matrices have no tail at all."
        ) as vo:
            self.play(FadeIn(g), FadeIn(rule), FadeIn(fit))
            vo.wait_until("a")
            self.play(FadeIn(band), FadeIn(bl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.03), FadeIn(leg), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def novels(self):
        m = load("mp")
        rows = m["novels"]
        n = len(rows)
        g = axes([-0.5, n - 0.5, 5], [-0.1, 1.1, 0.5], x_length=8.6, y_length=3.8, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: {0: "1", 0.5: r"3.2", 1.0: "10"}[v],
                 xlabel=rf"the ${n}$ weight matrices of our novels model, \ in order", ylabel=r"largest eigenvalue "
                 r"$/\ \lambda_+$ \ (log scale)", center=[-1.0, -0.5, 0])
        ax = g.ax
        one = DashedLine(ax.c2p(-0.5, 0), ax.c2p(n - 0.5, 0), color=MPC, stroke_width=2)
        init = dots_on(ax, range(n), [math.log10(max(r["init_max_over_edge"], 0.8)) for r in rows], RANDOM, 0.07)
        tr = dots_on(ax, range(n), [math.log10(r["max_over_edge"]) for r in rows], TRAINED, 0.07)
        leg = legend([(RANDOM, r"at initialization"), (TRAINED, r"after training")], font_size=22).move_to([5.0, 1.5, 0])
        a_tr = [r["above"] for r in rows]
        a_in = [r["init_above"] for r in rows]
        cap = note(r"computed: \ every matrix in the blocks, \ scaled to variance one").to_corner(DR, buff=0.25)
        every = "every matrix has" if min(a_tr) > 0 else "the matrices have"
        with self.voiceover(
            "The same in this series' small novels model. <bookmark mark='a'/> At initialization its "
            f"{n} matrices are random: {sum(a_in)} escapees in all. <bookmark mark='b'/> After training, {every} "
            f"between {min(a_tr)} and {max(a_tr)} beyond the edge. Training writes a little structure into a sea of "
            "noise."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in init], lag_ratio=0.03), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in tr], lag_ratio=0.03), FadeIn(leg[1]))
        self.wait(0.3)
        self.clear_scene()
