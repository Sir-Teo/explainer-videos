from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import DATA, MONO, WALK, load

ALPHA27 = " abcdefghijklmnopqrstuvwxyz"
STATE_COLORS = [GREY_B, C.BITS, DATA]  # space, vowel, consonant
CAP = 0.36  # the letter bars are cut off at 36%


class Markov(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.matrix()
        self.letters()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Chains with short memories", r"What if the next step depends on this one?", part=4)
        with self.voiceover("Chapter five. Markov chains."):
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
        fixn = label(r"an eigenvector of $P$, \ eigenvalue $1$ \ (Part 2)", font_size=28, color=C.BITS)
        fixn.next_to(fix, DOWN, buff=0.3)
        val = MathTex(r"\pi = (" + ", ".join(f"{x:.2f}" for x in pi3) + ")", font_size=36, color=C.BITS)
        val.next_to(fixn, DOWN, buff=0.35)
        note_ = label(r"rows: \ the chances of what comes next; \\ each row adds up to $1$", font_size=24, color=GREY_A)
        note_.next_to(Pm, DOWN, buff=0.45)
        with self.voiceover(
            "Follow the whole distribution instead of a single walker, and each step is a multiplication by the table "
            "of chances, the transition matrix. <bookmark mark='a'/> The distribution that a step leaves unchanged is "
            "the chain's stationary distribution. It's an eigenvector of the matrix, with eigenvalue one, straight "
            "out of part two."
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
