from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, MONO, PART, WALK, curve, load

ALPHA27 = " abcdefghijklmnopqrstuvwxyz"
STATE_COLORS = [GREY_B, C.BITS, DATA]  # space, vowel, consonant
CAP = 0.36  # the letter bars are cut off at 36%


class Markov(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.matrix()
        self.letters()
        self.balance()
        self.gap()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"Chains with short memories", r"What if the next step depends on this one?", part=PART)
        with self.voiceover("Chapter ten. Markov chains."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def three(self):
        d = load("markov")
        P3, pi3, walk = np.asarray(d["P3"]), np.asarray(d["pi3"]), [int(w) for w in d["walk3"]]
        assert abs(pi3 @ P3 - pi3).max() < 1e-12
        pos = [np.array([-3.4, 2.0, 0]), np.array([-5.4, -1.3, 0]), np.array([-1.4, -1.3, 0])]
        names = [r"space", r"vowel", r"consonant"]
        R = 0.62
        nodes = VGroup(*[VGroup(Circle(radius=R, color=STATE_COLORS[i], stroke_width=4, fill_color=BACKGROUND,
                                       fill_opacity=1).move_to(pos[i]),
                                label(names[i], font_size=26, color=STATE_COLORS[i]).move_to(pos[i]))
                         for i in range(3)])
        arrows, plabs = VGroup(), VGroup()
        for a in range(3):
            for b in range(3):
                p = P3[a, b]
                if p < 0.01:
                    continue
                w = 1.5 + 6 * p
                if a == b:
                    out = (pos[a] - np.array([-3.4, 0.0, 0]))
                    out = out / np.linalg.norm(out)
                    start = pos[a] + R * rotate_vector(out, 0.5)
                    end = pos[a] + R * rotate_vector(out, -0.5)
                    arr = CurvedArrow(start, end, angle=-4.2, color=GREY_B, stroke_width=w, tip_length=0.16)
                    lab_pos = pos[a] + out * (R + 0.75)
                else:
                    dvec = (pos[b] - pos[a]) / np.linalg.norm(pos[b] - pos[a])
                    nrm = rotate_vector(dvec, PI / 2)
                    s_, e_ = pos[a] + dvec * R + nrm * 0.18, pos[b] - dvec * R + nrm * 0.18
                    arr = Arrow(s_, e_, buff=0.05, color=GREY_B, stroke_width=w, max_tip_length_to_length_ratio=0.08)
                    lab_pos = (s_ + e_) / 2 + nrm * 0.32
                arrows.add(arr)
                plabs.add(MathTex(f"{p:.2f}", font_size=26, color=GREY_A).move_to(lab_pos))
        head = label(r"Three states, from Part 1's letters", font_size=32).to_corner(UL, buff=0.4)
        # the walker, and its time in each state
        walker = glow_dot(pos[walk[0]] + UP * 0.0, color=WALK, radius=0.12)
        counts = np.zeros(3)
        bars = LiveBars([0, 0, 0], max_value=0.6, height=3.0, bar_width=0.8, gap=0.45, colors=STATE_COLORS,
                        labels=names, label_font=24)
        bars.place(-1.8, x=4.0)
        ghost = VGroup(*[DashedLine([bars._cx(i) - 0.5 + 4.0 - 0.0, -1.8 + 3.0 * pi3[i] / 0.6, 0],
                                    [bars._cx(i) + 0.5 + 4.0, -1.8 + 3.0 * pi3[i] / 0.6, 0], color=WHITE,
                                    stroke_width=2) for i in range(3)])
        bl = label(r"share of time spent", font_size=26, color=GREY_A).move_to([4.0, 1.9, 0])
        nv = Integer(0, font_size=30)
        nl = VGroup(label(r"steps:", font_size=26, color=GREY_A), nv).arrange(RIGHT, buff=0.15).next_to(bl, DOWN, buff=0.15)
        pct = VGroup(*[MathTex(rf"{100 * pi3[i]:.0f}\%", font_size=26, color=WHITE)
                       .next_to(ghost[i], UP, buff=0.08) for i in range(3)])
        cite_ = cite(r"A.~A.~Markov (1906; \ vowels and consonants in \textit{Eugene Onegin}, 1913)", corner=DR)
        with self.voiceover(
            "A Markov chain is randomness with a short memory: what comes next depends only on where you are now. "
            "<bookmark mark='a'/> Here's one built from part one's letters, with just three states: a space, a "
            "vowel, or a consonant. The arrows carry the chances of what comes next. After a vowel, a consonant, "
            "seven times in ten. <bookmark mark='b'/> Follow one walker as it hops, and count the time it spends in "
            "each state."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.2),
                      LaggedStart(*[GrowArrow(a) if isinstance(a, Arrow) else Create(a) for a in arrows], lag_ratio=0.1),
                      FadeIn(plabs), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(walker), FadeIn(bars), FadeIn(bl), FadeIn(nl))
            here = walk[0]
            for j, w in enumerate(walk[1:13], start=1):
                counts[w] += 1
                anim = [Indicate(walker, color=WALK, scale_factor=1.6)] if w == here else [walker.animate.move_to(pos[w])]
                self.play(*anim, *bars.to(counts / j), ChangeDecimalToValue(nv, j), run_time=0.45)
                here = w
        with self.voiceover(
            "Keep going, and the shares settle: about nineteen percent spaces, thirty-one percent vowels, and fifty "
            "percent consonants, the same shares as in the books. <bookmark mark='a'/> Markov did exactly this by "
            "hand in 1913, with the vowels and consonants of twenty thousand letters of Pushkin."
        ) as vo:
            for j in range(13, len(walk), 8):
                for w in walk[j:j + 8]:
                    counts[w] += 1
                self.play(walker.animate.move_to(pos[walk[min(j + 7, len(walk) - 1)]]),
                          *bars.to(counts / counts.sum()), ChangeDecimalToValue(nv, int(counts.sum())), run_time=0.22)
            self.play(Create(ghost), FadeIn(pct))
            vo.wait_until("a")
            self.play(FadeIn(cite_))
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def matrix(self):
        d = load("markov")
        P3, pi3 = np.asarray(d["P3"]), np.asarray(d["pi3"])
        rows = [" & ".join(f"{P3[a, b]:.2f}" for b in range(3)) for a in range(3)]
        Pm = MathTex(r"P = \begin{bmatrix}" + r" \\ ".join(rows) + r"\end{bmatrix}", font_size=40).move_to([-2.0, 1.1, 0])
        rl = VGroup(*[label(n, font_size=22, color=STATE_COLORS[i]) for i, n in enumerate(("from space", "from vowel",
                                                                                             "from consonant"))])
        for i, r in enumerate(rl):
            r.next_to(Pm, LEFT, buff=0.2).set_y(Pm.get_center()[1] + (1 - i) * 0.52)
        colors = {r"\pi": C.BITS}
        step = cmath(r"\pi_{t+1}", "=", r"\pi_t", r"\,P", font_size=46).move_to([3.0, 1.6, 0])
        fix = cmath(r"\pi", r"\,P", "=", r"\pi", colors=colors, font_size=52).move_to([3.0, 0.2, 0])
        fixn = label(r"an eigenvector of $P$, \ eigenvalue $1$ \ (Part 3)", font_size=28, color=C.BITS)
        fixn.next_to(fix, DOWN, buff=0.3)
        val = MathTex(r"\pi = (" + ", ".join(f"{x:.2f}" for x in pi3) + ")", font_size=36, color=C.BITS)
        val.next_to(fixn, DOWN, buff=0.35)
        note_ = label(r"rows: \ the chances of what comes next; \\ each row adds up to $1$", font_size=24, color=GREY_A)
        note_.next_to(Pm, DOWN, buff=0.45)
        with self.voiceover(
            "Follow the whole distribution instead of a single walker, and each step is a multiplication by the table "
            "of chances, the transition matrix. <bookmark mark='a'/> The distribution that a step leaves unchanged is "
            "the chain's stationary distribution. It's an eigenvector of the matrix, with eigenvalue one, straight "
            "out of part three."
        ) as vo:
            self.play(FadeIn(Pm), FadeIn(rl), FadeIn(note_))
            self.play(Write(step))
            vo.wait_until("a")
            self.play(Write(fix), FadeIn(fixn))
            self.play(FadeIn(val))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def letters(self):
        d = load("markov")
        D, tv, freq = np.asarray(d["dists"]), np.asarray(d["tv"]), np.asarray(d["freq"])
        lam2 = float(d["lam2"])
        assert tv[5] < 0.01 and 0.25 < lam2 < 0.35
        labs = [Text("␣" if c == " " else c, font=MONO, font_size=18, color=GREY_A) for c in ALPHA27]
        bars = LiveBars(np.minimum(D[0], CAP), max_value=CAP, height=3.2, bar_width=0.3, gap=0.08, colors=DATA,
                        label_mobs=labs)
        bars.place(-2.6, x=-1.2)
        ghost = VGroup(*[Rectangle(width=0.3, height=max(3.2 * f / CAP, 0.002), stroke_color=WHITE, stroke_width=1.2,
                                   fill_opacity=0).move_to([bars._cx(i) - 1.2, -2.6 + 1.6 * f / CAP, 0])
                         for i, f in enumerate(freq)])
        gl = label(r"outlines: \ the letter frequencies", font_size=24, color=GREY_A).to_corner(DR, buff=0.35)
        sv = Integer(0, font_size=36, color=C.BITS)
        sl = VGroup(label(r"step", font_size=30), sv).arrange(RIGHT, buff=0.15).to_corner(UL, buff=0.45)
        head = label(r"All $27$ letters, \ starting from certainty: \ q", font_size=30).next_to(sl, RIGHT, buff=0.6)

        def over(k):
            """For a bar taller than the cut-off: its true height, written above it."""
            g = VGroup()
            for i in np.nonzero(D[k] > CAP)[0]:
                g.add(MathTex(rf"{100 * D[k][i]:.0f}\%", font_size=24, color=C.BITS)
                      .move_to([bars._cx(i) - 1.2, -2.6 + 3.2 + 0.25, 0]))
            return g

        tags = [over(k) for k in range(len(D))]
        # how far from the letter frequencies, on a log scale
        ax = Axes(x_range=[0, 8, 1], y_range=[0, 4, 1], x_length=3.4, y_length=2.2, tips=False,  # height: 4 + log10
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([4.6, 2.0, 0])
        yl = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                      for t, v in ((r"1", 4), (r"10^{-2}", 2), (r"10^{-4}", 0))])
        al = label(r"distance from the frequencies", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.1)
        pts = [ax.c2p(k, 4 + math.log10(max(tv[k], 1e-4))) for k in range(9)]
        dots = VGroup(*[Dot(p, radius=0.045, color=C.SURPRISE) for p in pts])
        lam_l = label(rf"each step: \ $\times\,{lam2:.2f}$ or so \ (the second eigenvalue)", font_size=22,
                      color=C.SURPRISE).next_to(ax, DOWN, buff=0.25)
        with self.voiceover(
            "Now all twenty-seven letters, with part one's full table. Start from certainty: the letter q. "
            "<bookmark mark='a'/> One step later, it's almost surely a u. <bookmark mark='b'/> Then the "
            "possibilities spread out, <bookmark mark='c'/> and within about five steps the chain has forgotten "
            "where it started: what's left is just the letter frequencies. <bookmark mark='d'/> How fast it forgets "
            "is set by the matrix's second-largest eigenvalue, about 0.3 here: each step shrinks the distance that's "
            "left by roughly that factor."
        ) as vo:
            self.play(FadeIn(sl), FadeIn(head), FadeIn(bars), FadeIn(tags[0]), Create(ghost), FadeIn(gl))
            self.play(Create(ax), FadeIn(yl), FadeIn(al), FadeIn(dots[0]))
            vo.wait_until("a")
            for k in range(1, 9):
                if k == 2:
                    vo.wait_until("b")
                if k == 4:
                    vo.wait_until("c")
                self.play(*bars.to(np.minimum(D[k], CAP)), FadeOut(tags[k - 1]), FadeIn(tags[k]),
                          ChangeDecimalToValue(sv, k), FadeIn(dots[k]), run_time=0.9)
            vo.wait_until("d")
            self.play(Create(VMobject(color=C.SURPRISE, stroke_width=2).set_points_as_corners(pts)), FadeIn(lam_l))
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def balance(self):
        d = load("mixing")
        colors = {r"\pi_i P_{ij}": DATA, r"\pi_j P_{ji}": C.BITS}
        rows = [
            cmath(r"\pi_i P_{ij}", "=", r"\pi_j P_{ji}", colors=colors, font_size=40),
            cmath(r"\textstyle\sum_i \pi_i P_{ij}", "=", r"\pi_j \textstyle\sum_i P_{ji} = \pi_j", font_size=40),
            cmath(r"\pi P", "=", r"\pi", font_size=40),
        ]
        whys = [why(r"detailed balance: \ as much flows $i \to j$ as $j \to i$"),
                why(r"sum over $i$; \ a row of $P$ adds to $1$"),
                why(r"so $\pi$ is stationary")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-2.4, buff=0.55, edge=6.8)
        pair = str(d["asym_pair"])
        a, b = pair[0], pair[1]
        fij, fji = float(d["flow_ij"]), float(d["flow_ji"])
        nm = {" ": r"space"}

        def nmf(c):
            return nm.get(c, rf"``{c}''")

        bars = VGroup(
            VGroup(label(rf"{nmf(a)} then {nmf(b)}", font_size=26, color=DATA),
                   Rectangle(width=max(60 * fij, 0.05), height=0.4, stroke_width=0, fill_color=DATA, fill_opacity=0.85),
                   MathTex(f"{100 * fij:.2f}\\%", font_size=28, color=DATA)).arrange(RIGHT, buff=0.25),
            VGroup(label(rf"{nmf(b)} then {nmf(a)}", font_size=26, color=C.BITS),
                   Rectangle(width=max(60 * fji, 0.05), height=0.4, stroke_width=0, fill_color=C.BITS, fill_opacity=0.85),
                   MathTex(f"{100 * fji:.2f}\\%", font_size=28, color=C.BITS)).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-1.0, -2.2, 0])
        bt = label(r"English is not reversible: \ of all letter pairs in Part 1's books", font_size=24, color=GREY_A)
        bt.next_to(bars, UP, buff=0.25).align_to(bars, LEFT)
        big = max(fij, fji) / min(fij, fji)
        with self.voiceover(
            "There is an easy way to know a distribution is stationary without solving for an eigenvector. "
            "<bookmark mark='a'/> Suppose that, in it, as much probability flows from i to j in one step as from j "
            "to i. That's called detailed balance. <bookmark mark='b'/> Sum over i, <bookmark mark='c'/> and pi "
            "times P is pi: balanced flows mean nothing changes. <bookmark mark='d'/> It's enough, not necessary. "
            f"English isn't balanced: the pair e then space is {big:.0f} times as common as space then e, because "
            "words end in e far more often than they start with it. But when we build chains to sample from a "
            "distribution, in chapter thirteen, detailed balance is how we make sure they land on it."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(bt), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in bars], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gap(self):
        d = load("mixing")
        xs, U, pi = np.asarray(d["xs"]), np.asarray(d["U"]), np.asarray(d["pi"])
        snaps, ts = np.asarray(d["snaps"]), [int(t) for t in d["ts"]]
        betas, gap, tmix, lo, hi = (np.asarray(d[k], float) for k in ("betas", "gap", "tmix", "lower", "upper"))
        # the chain: a walk on 41 sites in a double well, its distribution from the left end
        bars = LiveBars(np.minimum(snaps[0], 0.2), max_value=0.2, height=2.6, bar_width=0.11,
                        gap=0.03, colors=WALK)
        bars.place(-0.6, x=-3.4)
        ghost = VGroup(*[Rectangle(width=0.11, height=max(2.6 * min(v, 0.2) / 0.2, 0.002), stroke_color=WHITE,
                                   stroke_width=1, fill_opacity=0).move_to([bars._cx(i) - 3.4, -0.6 + 1.3 * min(v, 0.2) / 0.2, 0])
                         for i, v in enumerate(pi)])
        Uc = VMobject(color=MODEL, stroke_width=3).set_points_smoothly(
            [np.array([bars._cx(i) - 3.4, -1.5 - 0.35 * u, 0]) for i, u in enumerate(U)])
        Ul = label(r"the energy $U$: \ two wells", font_size=20, color=MODEL).next_to(Uc, DOWN, buff=0.1)
        tv = Integer(0, font_size=30, color=C.BITS)
        tl = VGroup(label(r"step", font_size=26), tv).arrange(RIGHT, buff=0.15).move_to([-3.4, 3.0, 0])
        head = label(r"$41$ sites, \ $\pi \propto e^{-\beta U}$, \ from the left end", font_size=26).next_to(tl, DOWN, buff=0.2)
        gl = label(r"outlines: \ the stationary distribution", font_size=20, color=GREY_A).next_to(ghost, UP, buff=0.15).shift(DOWN * 0.1 + RIGHT * 1.0)
        # mixing time against relaxation time
        ax = Axes(x_range=[2, 8, 1], y_range=[2, 10, 2], x_length=5.6, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.4, -0.2, 0])
        xt = VGroup(*[MathTex(f"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, 2), DOWN, buff=0.1) for v in (2, 4, 6, 8)])
        yt = VGroup(*[MathTex(f"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(2, v), LEFT, buff=0.1) for v in (2, 6, 10)])
        xl = label(r"$1/\text{gap}$: \ the relaxation time", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"steps to mix \ (within $\tfrac14$)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        lt = np.log10(1 / gap)
        dots = VGroup(*[Dot(ax.c2p(a, math.log10(b)), radius=0.06, color=C.BITS) for a, b in zip(lt, tmix)])
        lo_c = curve(ax, lt, np.log10(np.maximum(lo, 1)), color=GREY_B, stroke_width=2)
        hi_c = curve(ax, lt, np.minimum(np.log10(hi), 10), color=GREY_B, stroke_width=2)
        bl = label(r"bounds: \ $(t_{\mathrm{rel}} - 1)\ln 2 \;\le\; t_{\mathrm{mix}} \;\le\; t_{\mathrm{rel}}\ln\frac{4}{\pi_{\min}}$",
                   font_size=20, color=GREY_B).next_to(ax, DOWN, buff=0.65)
        k = list(betas).index(2.0)
        with self.voiceover(
            "How fast a chain forgets is set by its second eigenvalue; one minus it is the spectral gap. A chain "
            "with a bottleneck has a tiny gap. <bookmark mark='a'/> Here is a walk on forty-one sites, aiming at a "
            "distribution with two wells and a barrier between them. Start at the left end. <bookmark mark='b'/> "
            "The left well fills within a few hundred steps, <bookmark mark='c'/> but crossing the barrier takes "
            f"hundreds of thousands: after {ts[-1]:,} steps the right well is still filling. <bookmark mark='d'/> "
            "Raise the barrier and the gap shrinks. Plotted against one over the gap, the steps it takes to mix "
            f"rise along a line of slope {float(d['slope']):.2f}, from {int(tmix[0]):,} to {int(tmix[-1]):,}, between "
            "the two bounds the theory gives. That is why samplers stuck between the modes of a distribution are "
            "the central difficulty of chapter thirteen."
        ) as vo:
            self.play(FadeIn(tl), FadeIn(head), FadeIn(bars), Create(ghost), FadeIn(gl), Create(Uc), FadeIn(Ul))
            vo.wait_until("a")
            vo.wait_until("b")
            for j in (1, 2, 3):
                self.play(*bars.to(np.minimum(snaps[j], 0.2)), ChangeDecimalToValue(tv, ts[j]), run_time=1.0)
            vo.wait_until("c")
            for j in (4, 5, 6):
                self.play(*bars.to(np.minimum(snaps[j], 0.2)), ChangeDecimalToValue(tv, ts[j]), run_time=1.0)
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            self.play(Create(lo_c), Create(hi_c), FadeIn(bl), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.15))
            self.play(Indicate(dots[k], color=WHITE))
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()
