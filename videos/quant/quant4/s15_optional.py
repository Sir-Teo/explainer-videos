from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, load

SEQ = "THTHH"  # an illustrative sequence for the gamblers' queue (HH first appears at toss 5)


class Optional(VoiceoverScene):
    def construct(self):
        f = load("firstpassage")
        pt = load("patterns")
        self.card()
        self.proof()
        self.balance(f)
        self.waiting_queue()
        self.patterns(pt)

    def card(self):
        c = chapter_card(6, r"Optional stopping, proved", r"When does stopping leave a fair game fair?", part=PART)
        with self.voiceover("Chapter six. Optional stopping, proved."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def proof(self):
        th = theorem_card(r"Optional stopping",
                          r"$M$ a martingale, $\tau$ a stopping time, finite. Then $\mathbb{E}M_\tau = M_0$ if (a) "
                          r"$\tau \le N$; or (b) $|M_{\tau \wedge n}| \le K$; or (c) $\mathbb{E}\tau < \infty$ and "
                          r"$|\Delta M| \le c$. In general: if $\{M_{\tau \wedge n}\}$ is uniformly integrable.",
                          who=r"Doob", color=MART, width=11.6, font_size=23).to_edge(UP, buff=0.3)
        rows = [cmath(r"\mathbb{E}M_{\tau \wedge n}", r"=", r"M_0 \quad \text{for every } n", font_size=36,
                      colors={r"M_0 \quad \text{for every } n": MART}),
                cmath(r"M_{\tau \wedge n}", r"\to", r"M_\tau \quad \text{a.s.}", font_size=36),
                cmath(r"|M_{\tau \wedge n}|", r"\le", r"K \ \text{or}\ |M_0| + c\,\tau \in L^1", font_size=36),
                cmath(r"\mathbb{E}M_\tau", r"=", r"\lim_n \mathbb{E}M_{\tau \wedge n} = M_0", font_size=36,
                      colors={r"\lim_n \mathbb{E}M_{\tau \wedge n} = M_0": MART}),
                cmath(r"\mathbb{E}S_{\tau_1 \wedge n} = 0", r"\ne", r"\mathbb{E}S_{\tau_1} = 1", font_size=36,
                      colors={r"\mathbb{E}S_{\tau_1} = 1": LOSS})]
        whys = [why(r"the stopped martingale is a martingale (chapter 5)"),
                why(r"$\tau$ is finite, so the stopped path is eventually constant"),
                why(r"(b) bounded; (c) each step at most $c$, and there are $\tau$ of them, with $\mathbb{E}\tau < \infty$"),
                why(r"dominated convergence moves the limit inside the expectation; (a) is the case $n = N$"),
                why(r"the walk that always wins: no bound, $\mathbb{E}\tau_1 = \infty$; the mean leaks away")]
        step = ladder(self, rows, whys, keep=4, top=1.15, x=-1.6, buff=0.6, edge=6.9)
        with self.voiceover(
            "Now the theorem, with its proof. A martingale stopped at a finite stopping time keeps its starting mean "
            "if you stop by a fixed date, or the stopped process stays bounded, or the expected time is finite and "
            "each step is bounded. <bookmark mark='a'/> The proof is four lines. At every fixed n the stopped "
            "martingale has mean M zero: chapter five. <bookmark mark='b'/> As n grows, the stopped path freezes at "
            "its value at tau. <bookmark mark='c'/> Each hypothesis gives one integrable bound on the whole stopped "
            "path: a constant, or the start plus c times tau. <bookmark mark='d'/> So dominated convergence passes "
            "the limit inside the expectation. <bookmark mark='e'/> Without a bound it fails: the walk stopped at "
            "plus one has mean zero at every finite n, but at tau it is always one. Uniform integrability says no "
            "mass escapes to infinity. Here it does."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def balance(self, f):
        H = f["hists"]
        keys = ["10", "100", "1000", "10000"]
        edges = np.arange(-150.5, 2.5, 3)
        centers = (edges[:-1] + edges[1:]) / 2
        g = axes([-150, 4], [0, 1.0], x_length=10.0, y_length=3.8, xlabel=r"$S_{\tau_1 \wedge n}$: where the stopped walk "
                 r"is at step $n$", ylabel=r"share of 10{,}000 walks (square root scale)", xticks=[-150, -100, -50, 0],
                 yticks=[0, 0.5, 1.0], yfmt=lambda u: {0: "0", 0.5: "0.25", 1.0: "1"}[u], font_size=17)
        g.to_edge(UP, buff=0.8)
        ax = g.ax

        def hist(k):
            h = np.asarray(H[k]["hist"], float)
            h = h / h.sum()
            grp = VGroup()
            for c_, v in zip(centers, h):
                if v <= 0:
                    continue
                top, bot = ax.c2p(c_, np.sqrt(v)), ax.c2p(c_, 0)
                col = QC.IDEA if c_ > 0 else LOSS
                grp.add(Rectangle(width=ax.c2p(2.6, 0)[0] - ax.c2p(0, 0)[0], height=max(top[1] - bot[1], 0.01),
                                  stroke_width=0, fill_color=col, fill_opacity=0.85).move_to((top + bot) / 2))
            return grp

        def fulcrum(k):
            m = H[k]["mean"]
            tri = Triangle(color=WHITE, fill_opacity=1).scale(0.16).move_to(ax.c2p(m, 0) + DOWN * 0.22)
            return VGroup(tri, MathTex(rf"\text{{mean }} {m:+.2f}", font_size=24).next_to(tri, DOWN, buff=0.1))

        def caption(k):
            return MathTex(rf"n = {int(k):,}".replace(",", "{,}") + rf":\ {100 * H[k]['frac_hit']:.1f}\% \text{{ at }} +1, "
                           rf"\text{{ lowest }} {H[k]['min']}", font_size=30).next_to(g, DOWN, buff=0.9)

        cur, ful, cap = hist(keys[0]), fulcrum(keys[0]), caption(keys[0])
        verdict = MathTex(r"n = \infty:\ S_{\tau_1} = 1 \text{ always: the mean jumps from 0 to 1}", font_size=32,
                          color=LOSS).next_to(cap, DOWN, buff=0.3)
        with self.voiceover(
            "Watch the mass escape. These are the positions of ten thousand stopped walks at step n. Gold is the "
            "spike at plus one, the walks that have already won; red is the rest, still below zero. A fulcrum sits "
            "at the mean. <bookmark mark='a'/> As n grows, the gold spike swallows almost everything, while a thin red "
            "tail slides further and further to the left. The balance holds: the mean stays at zero, because the few "
            "walks deep in the tail weigh more and more. <bookmark mark='b'/> In the limit the tail has left the "
            "frame, every walk is at one, and the mean jumps to one. That jump is uniform integrability failing, and "
            "it is the loophole the doubling system lives in."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cur), FadeIn(ful), FadeIn(cap))
            vo.wait_until("a")
            for k in keys[1:]:
                self.play(Transform(cur, hist(k)), Transform(ful, fulcrum(k)), Transform(cap, caption(k)), run_time=2)
                self.wait(0.6)
            vo.wait_until("b")
            self.play(FadeIn(verdict), Indicate(cur, color=QC.IDEA))
        self.wait(0.4)
        self.clear_scene()

    def waiting_queue(self):
        n = len(SEQ)
        tosses = VGroup(*[VGroup(RoundedRectangle(width=0.8, height=0.8, corner_radius=0.1, stroke_color=GREY_B),
                                 MathTex(c, font_size=36, color=QC.GAIN if c == "H" else LOSS)) for c in SEQ])
        for t in tosses:
            t[1].move_to(t[0])
        tosses.arrange(RIGHT, buff=0.5).to_edge(UP, buff=1.0)
        # gambler j arrives before toss j, stakes 1 on H, and if it wins lets the 2 ride on H again
        rows = VGroup()
        payout = []
        for j in range(n):
            w = 1.0
            hist_ = []
            for k, ch in enumerate("HH"):
                if j + k >= n:
                    break
                if SEQ[j + k] == ch:
                    w *= 2
                    hist_.append(w)
                else:
                    w = 0.0
                    hist_.append(0.0)
                    break
            payout.append(w if (j + len(hist_) == n and w > 0) else 0.0)
            chip = Circle(radius=0.22, color=color_gradient([P_C, MART], n)[j], fill_opacity=0.8)
            txt = MathTex(rf"\text{{gambler {j + 1}: }}" + (r"\to ".join([r"\$1"] + [rf"\${v:g}" for v in hist_])),
                          font_size=26)
            rows.add(VGroup(chip, txt).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tosses, DOWN, buff=0.6).align_to(tosses, LEFT)
        total = sum(payout)
        res = VGroup(
            MathTex(rf"\text{{paid out when HH appears: }} {int(total)} = 4 + 2", font_size=32, color=QC.IDEA),
            MathTex(r"\text{taken in: } \$1 \text{ per toss } = \tau", font_size=32),
            MathTex(r"\text{fair casino, bounded steps, } \mathbb{E}\tau < \infty \;\Rightarrow\; \mathbb{E}\tau = 6",
                    font_size=32, color=MART),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Optional stopping also computes, by Bob Li's trick of 1980. How long until two heads in a row? Before "
            "every toss a new gambler bets a dollar on heads at fair odds, and lets winnings ride on heads again. "
            "<bookmark mark='a'/> When heads, heads appears, gambler four holds four dollars and gambler five holds "
            "two. <bookmark mark='b'/> The casino took a dollar a toss and paid six. Its net is a martingale with "
            "bounded steps, so on average it balances: six tosses."
        ) as vo:
            self.play(FadeIn(tosses[0]), FadeIn(rows[0]))
            vo.wait_until("a")
            for j in range(1, n):
                self.play(FadeIn(tosses[j]), FadeIn(rows[j]), run_time=0.7)
            self.play(Indicate(rows[3], color=QC.IDEA), Indicate(rows[4], color=QC.IDEA))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()

    def patterns(self, pt):
        W = pt["waits"]
        abra = pt["abra"] / 1e15  # thousands of trillions
        card = lab_card(r"pattern waiting times (Li 1980)", [
            "def pattern_wait(pat, m=2):",
            "    \"\"\"Expected i.i.d. draws until pat first appears.\"\"\"",
            "    return sum(m ** k for k in range(1, len(pat) + 1)",
            "               if pat[:k] == pat[-k:])",
        ], source="explainer/quant/house/martingale.py", width=6.4).to_corner(UL, buff=0.4)
        head = [label(t, font_size=21, color=GREY_B) for t in (r"pattern", r"$\sum m^k$", r"200{,}000 simulated")]
        rows = []
        for pat in ("HH", "HT", "HTH", "HHH"):
            v = W[pat]
            rows.append([MathTex(pat, font_size=28), MathTex(str(v["theory"]), font_size=28, color=MART),
                         MathTex(rf"{v['mean']:.2f} \pm {v['se']:.2f}", font_size=28)])
        grid = VGroup(*head, *[c for r in rows for c in r]).arrange_in_grid(rows=5, cols=3, buff=(0.5, 0.18))
        grid.to_corner(UR, buff=0.5)
        pen = VGroup(
            label(r"Penney's game: you pick HHT, I pick THH", font_size=22, color=GREY_A),
            MathTex(rf"P(\text{{THH first}}) = {pt['penney_exact']:.2f}\ \ (\text{{simulated }} {pt['penney_sim']:.3f})",
                    font_size=28, color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(grid, DOWN, buff=0.5).align_to(grid, LEFT)
        pred = desk_question(r"HH or HT: which takes longer to appear in fair tosses?",
                             r"HH: 6 tosses on average against 4, although each has probability $1/4$ in any two "
                             r"tosses. HH overlaps itself.", width=6.4, font_size=21).to_corner(DR, buff=0.35)
        with self.voiceover(
            "In general, the same argument gives a formula for any pattern: add up m to the k for every k where the "
            "pattern's first k letters equal its last k. <bookmark mark='a'/> Heads heads: two plus four, six. Heads "
            "tails: only the whole pattern overlaps itself, four. Heads tails heads: ten. Three heads: fourteen. Two "
            "hundred thousand simulated sequences agree, within sampling error. A monkey typing ABRACADABRA on a "
            f"twenty-six key typewriter needs about {abra:.2f} thousand trillion keystrokes, an exercise from "
            "Williams. <bookmark mark='b'/> The overlaps also decide Penney's game: if you choose heads, heads, tails "
            f"and I choose tails, heads, heads, I win {100 * pt['penney_exact']:.0f} percent of the time. "
            "<bookmark mark='c'/> So which takes longer to appear, heads heads or heads tails? Heads heads, six "
            "against four, though each has the same chance in any two tosses: heads heads overlaps itself, so its "
            "near-misses waste time."
            " The theorem needs conditions. Next: the strategy that breaks them, doubling."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            lab_run(self, card, ['pattern_wait("HH"), pattern_wait("HT")', f"({W['HH']['theory']}, {W['HT']['theory']})",
                                 'pattern_wait("ABRACADABRA", 26)', f"{pt['abra']}"])
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*head)), LaggedStart(*[FadeIn(VGroup(*r)) for r in rows], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(pen))
            vo.wait_until("c")
            self.play(FadeIn(pred, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
