from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load


class Stopping(VoiceoverScene):
    def construct(self):
        s = load("snell_rw")
        self.card()
        self.derive()
        self.rope(s)
        self.lab(s)
        self.secretary(load("secretary"))

    def card(self):
        c = chapter_card(11, r"Optimal stopping: the Snell envelope", r"When should you stop and take what you have?",
                         part=PART)
        with self.voiceover("Chapter eleven. Optimal stopping, and the Snell envelope."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"U_N = g_N,\quad U_n", r"=", r"\max\big(g_n,\ \mathbb{E}[U_{n+1} \mid \mathcal{F}_n]\big)",
                      font_size=32, colors={r"U_N = g_N,\quad U_n": VALUE}),
                cmath(r"U_n \ge \mathbb{E}[U_{n+1} \mid \mathcal{F}_n]", r",\ ", r"U \ge g;\quad \tilde U \text{ the same}"
                      r"\ \Rightarrow\ \tilde U \ge U", font_size=30),
                cmath(r"\tau^* = \min\{n : U_n = g_n\}", r"\ \Rightarrow\ ", r"U_0 = \mathbb{E}\,g_{\tau^*} = "
                      r"\sup_{\tau}\mathbb{E}\,g_\tau", font_size=30, colors={r"\tau^* = \min\{n : U_n = g_n\}": KELLY}),
                cmath(r"U(x)", r"=", r"\max\big(g(x),\ \tfrac12 U(x - 1) + \tfrac12 U(x + 1)\big)", font_size=30,
                      colors={r"U(x)": VALUE})]
        whys = [why(r"backward induction: at each date, the better of stopping now and the value of waiting (Snell 1952)",
                    font_size=21),
                why(r"so $U$ is a supermartingale above $g$, and by induction from $N$ the smallest one: the Snell "
                    r"envelope", font_size=21),
                why(r"before $\tau^*$ the maximum picks the waiting term, so $U$ stopped at $\tau^*$ is a martingale: "
                    r"optional sampling gives the value", font_size=21),
                why(r"a symmetric random walk with no deadline: $U$ is the smallest function above $g$ that is at "
                    r"least the average of its neighbours: the least concave majorant (Dynkin 1963)", font_size=21)]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-0.4, buff=0.75, edge=6.9)
        with self.voiceover(
            "Some decisions are not how much, but when: exercise an option, sell a house, stop searching. Let g be "
            "what you get if you stop at time n. Laurie Snell's answer, from 1952, is backward induction again: at "
            "the deadline you must stop; before it, take the better of stopping now and the expected value of "
            "waiting. <bookmark mark='a'/> That makes U a supermartingale, it drifts down on average, lying above g, "
            "and induction from the deadline shows it is the smallest such process. <bookmark mark='b'/> Stop the "
            "first time U touches g. Until then the maximum picks the waiting term, so U stopped there is a "
            "martingale, and its value today is the expected payoff of the rule: nothing does better. "
            "<bookmark mark='c'/> Now a case you can see. A random walk that steps left or right with equal "
            "chances, with no deadline. The expected value of waiting one step is the average of the two "
            "neighbours, and the smallest function above g that is at least the average of its neighbours is the "
            "smallest concave function above g."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def rope(self, s):
        g = np.asarray(s["g"])
        H = np.asarray(s["history"])
        sw = list(s["history_sweeps"])
        N = len(g) - 1
        G = axes([0, N], [0, 10], x_length=10.0, y_length=4.6, xlabel=r"position of the walk $x$",
                 ylabel=r"payoff if you stop", xticks=[0, 5, 10, 15, 20], yticks=[0, 5, 10], font_size=17)
        G.to_edge(DOWN, buff=0.7)
        ax = G.ax
        pegs = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, v), color=GREY_B, stroke_width=6) for x, v in enumerate(g)])
        caps = VGroup(*[Dot(ax.c2p(x, v), radius=0.07, color=GREY_A) for x, v in enumerate(g)])
        k = ValueTracker(0)
        rope = always_redraw(lambda: curve(ax, np.arange(N + 1), H[int(k.get_value())], VALUE, stroke_width=4))
        cnt = Integer(0, font_size=30, color=VALUE)
        cnt.add_updater(lambda m: m.set_value(sw[int(k.get_value())]))
        cl = VGroup(label(r"sweeps of value iteration:", font_size=22, color=VALUE), cnt).arrange(RIGHT, buff=0.15)
        cl.to_corner(UR, buff=0.5)
        stop = np.asarray(s["stop"]).astype(bool)
        lights = VGroup(*[Dot(ax.c2p(x, g[x]), radius=0.12, color=KELLY) for x in range(N + 1) if stop[x]])
        st_l = label(r"stop where the rope touches a peg; wait where it hangs above", font_size=22, color=KELLY)
        st_l.to_corner(UL, buff=0.5)
        q = pause_card(r"Which pegs will the rope touch?", width=4.4, font_size=22).to_corner(UL, buff=0.4)
        with self.voiceover(
            "Here is a payoff for every position, a skyline of pegs; the ends absorb the walk. Pause and predict: "
            "which pegs will the value touch? <bookmark mark='a'/> Run value iteration. Start the value at the "
            "payoff itself, and sweep: everywhere, replace the value by the larger of the peg and the average of "
            "the two neighbours. The curve lifts out of the valleys and smooths, sweep after sweep, like a rope being "
            f"pulled taut over the tallest pegs. After {s['sweeps']} sweeps it stops moving. "
            "<bookmark mark='b'/> Where the rope rests on a peg, stopping is optimal: waiting cannot beat what you "
            "hold. Where it hangs above the pegs, wait, because a better peg is reachable often enough. Starting in "
            f"the middle, at position ten, the right to choose when to stop is worth {s['U0_mid']:.2f}, though stopping "
            f"there would pay {g[10]:.0f}."
        ) as vo:
            self.play(FadeIn(G), LaggedStart(*[Create(p_) for p_ in pegs], lag_ratio=0.05), FadeIn(caps), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeOut(q), FadeIn(cl))
            self.add(rope)
            self.play(k.animate.set_value(len(H) - 1), run_time=8, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(st_l), LaggedStart(*[GrowFromCenter(d_) for d_ in lights], lag_ratio=0.15))
        rope.clear_updaters()
        cnt.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def lab(self, s):
        card = lab_card(r"the Snell envelope, two ways", [
            "def snell_envelope(g, max_sweeps, tol):",
            "    U = g.copy()",
            "    for s in range(1, max_sweeps + 1):",
            "        new = U.copy(); new[1:-1] = maximum(g[1:-1], 0.5*(U[:-2] + U[2:]))",
            "        if max(abs(new - U)) < tol: break",
            "        U = new",
            "    return U",
            "def concave_majorant(g):     # upper hull; a, b = the last two points kept",
            "    hull = []",
            "    for i in range(len(g)):",
            "        while len(hull) >= 2 and (b-a)*(g[i]-g[a]) >= (g[b]-g[a])*(i-a): hull.pop()",
            "        hull.append(i)",
            "    return interp(arange(len(g)), hull, g[hull])",
        ], source="explainer/quant/house/control.py", width=8.2, font_size=18).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Lab three. Two completely different routines in the House. One is the value iteration you just "
            "watched: six lines of maxima and averages. The other knows nothing about random walks: it computes the "
            "upper convex hull of the pegs, the shape a rope really takes, and interpolates. <bookmark mark='a'/> "
            f"Run both. Value iteration converges in {s['sweeps']} sweeps, and the two answers agree to within ten to "
            f"the minus {-int(np.floor(np.log10(s['max_gap'])))}. Probability and geometry give the same object. The "
            "test turns green."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            out = lab_run(self, card, ["U = snell_envelope(g, 200000, 1e-14); M = concave_majorant(g)",
                                       f"sweeps: {s['sweeps']}   max |U - M| = {s['max_gap']:.1e}",
                                       "assert max(abs(U - M)) < 1e-10      # passed"])
            self.play(out[-1].animate.set_color(GOOD))
        self.wait(0.4)
        self.clear_scene()

    def secretary(self, q):
        k = np.asarray(q["k"])
        g = axes([0, 100], [0, 0.45], x_length=6.6, y_length=4.2, xlabel=r"candidates rejected before choosing",
                 ylabel=r"chance of choosing the best of 100", xticks=[0, 20, 37, 60, 80, 100],
                 yticks=[0, 0.1, 0.2, 0.3, 0.4], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        exact = curve(ax, k, np.asarray(q["exact"]), VALUE, stroke_width=4)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.045, color=WHITE) for x, y in zip(k[::2], np.asarray(q["sim"])[::2])])
        top = DashedLine(ax.c2p(q["best_k"], 0), ax.c2p(q["best_k"], q["best_p"]), color=KELLY, stroke_width=2)
        tl = MathTex(rf"k = {q['best_k']}:\ {100 * q['best_p']:.1f}\%", font_size=26, color=KELLY).next_to(
            ax.c2p(q["best_k"], q["best_p"]), UP, buff=0.1)
        side = VGroup(
            wrapped_label(r"100 candidates arrive in random order; you can rank each against those seen, must accept or "
                          r"reject on the spot, and win only with the best", 4.4, 21, GREY_A),
            wrapped_label(r"rule: reject the first $k$, then take the first who beats them all; the best $k \approx "
                          r"n/e$ wins with probability $\to 1/e \approx 37\%$, however large $n$", 4.4, 21, VALUE),
            wrapped_label(r"line: exact; dots: 20{,}000 simulated searches each (Lindley 1961; Dynkin 1963)", 4.4, 19,
                          GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "A classic with a famous answer: the secretary problem. A hundred candidates arrive in random order. "
            "You can rank each one against those already seen, but must accept or reject on the spot, and win only "
            "with the very best. <bookmark mark='a'/> The Snell envelope says: reject a fixed number, then take the "
            f"first candidate better than all of them. Reject about {q['best_k']}, a hundred over e, and you choose "
            f"the best {100 * q['best_p']:.0f} percent of the time: one over e, however many candidates there are."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(exact), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), run_time=2.5)
            self.play(Create(top), FadeIn(tl), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
