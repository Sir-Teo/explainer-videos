from __future__ import annotations

import numpy as np

from videos.stats.stats7.common import *  # noqa: F403

NAMES = [r"sunny", r"cloudy", r"rainy"]
SC = [S.ACCENT, GREY_A, S.EST]


def node_positions():
    return [np.array([-3.0, 1.0, 0]), np.array([0.0, -1.6, 0]), np.array([3.0, 1.0, 0])]


class Chains(VoiceoverScene):
    def construct(self):
        self.card()
        self.markov()
        self.onegin()
        self.graph()
        self.flow()
        self.rate()
        self.ergodic()

    def card(self):
        card = chapter_card(8, r"Markov chains", r"Randomness with a memory of one step", part=PART)
        with self.voiceover("Chapter eight. Markov chains."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def markov(self):
        hc = history_card(1913, r"Andrey Markov, \ on Pushkin's \emph{Eugene Onegin}", r"20,000 letters, \ classified as vowel or "
                          r"consonant: \ the chance of a vowel depends on the letter before. \ The first Markov chain, \ "
                          r"fitted to data", color=S.MUSEUM, width=7.6, font_size=24).move_to([0, 1.4, 0])
        dfn = definition_card(r"Markov chain", r"$P(X_{t+1} = j \mid X_t = i, X_{t-1}, \dots, X_0) = P_{ij}$: \ the future depends "
                              r"on the past only through the present", color=CHAIN, width=8.6, font_size=24).next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "Everything so far drew independent numbers. Many of the most useful random processes have memory. "
            "<bookmark mark='a'/> In 1913 Andrey Markov took the first twenty thousand letters of Pushkin's novel in "
            "verse, Eugene Onegin, and classified each as a vowel or a consonant. The chance of a vowel was not the "
            "same after a vowel as after a consonant: the letters were dependent, but in a simple way. "
            "<bookmark mark='b'/> A Markov chain is a sequence in which the next state depends on the past only "
            "through the present state: given where you are now, where you've been doesn't matter. All of its "
            "behaviour is in one table of transition probabilities."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(dfn))
        self.clear_scene()

    def graph(self):
        d = load("chain")
        P = np.asarray(d["P"])
        pos = node_positions()
        nodes = VGroup(*[VGroup(Circle(radius=0.6, color=c, stroke_width=3), label(n, font_size=24, color=c)).move_to(p)
                         for n, c, p in zip(NAMES, SC, pos)]).shift(LEFT * 2.6)
        arrows = VGroup()
        for i in range(3):
            for j in range(3):
                if i == j:
                    a = nodes[i][0].get_top()
                    loop = Arc(radius=0.35, start_angle=-0.3, angle=PI + 0.6, color=GREY_B, stroke_width=2).move_to(a + UP * 0.32)
                    t = MathTex(f"{P[i, j]:.1f}", font_size=22, color=GREY_B).next_to(loop, UP, buff=0.05)
                    arrows.add(VGroup(loop, t))
                else:
                    s_, e_ = nodes[i].get_center(), nodes[j].get_center()
                    v = (e_ - s_) / np.linalg.norm(e_ - s_)
                    nrm = np.array([-v[1], v[0], 0]) * 0.18
                    ar = Arrow(s_ + v * 0.62 + nrm, e_ - v * 0.62 + nrm, buff=0, color=GREY_B, stroke_width=2.5,
                               max_tip_length_to_length_ratio=0.08)
                    t = MathTex(f"{P[i, j]:.1f}", font_size=22, color=GREY_B).move_to(ar.get_center() + nrm * 2.2)
                    arrows.add(VGroup(ar, t))
        mat = MathTex(r"P = \begin{pmatrix} 0.7 & 0.2 & 0.1 \\ 0.3 & 0.5 & 0.2 \\ 0.2 & 0.3 & 0.5 \end{pmatrix}", font_size=34)
        mat.move_to([4.2, 0.8, 0])
        rl = label(r"row $i$: \ where tomorrow goes from state $i$; \ each row sums to 1", font_size=22, color=GREY_A)
        rl.next_to(mat, DOWN, buff=0.35)
        if rl.width > 5.0:
            rl.width = 5.0
        with self.voiceover(
            "Here's a toy chain: tomorrow's weather, given today's. <bookmark mark='a'/> Three states: sunny, cloudy, "
            "rainy. <bookmark mark='b'/> From sunny, it stays sunny with chance point seven, turns cloudy with point "
            "two, rainy with point one. Each state has its own row of probabilities. <bookmark mark='c'/> Collect "
            "them into a matrix. Row i says where tomorrow goes from state i, so each row adds up to one."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.1), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(mat), FadeIn(rl))
        self.clear_scene()

    def flow(self):
        d = load("chain")
        flows = np.asarray(d["flows"])
        st_ = np.asarray(d["stationary"])
        A = axes([-0.6, 2.6], [0, 1.05], x_length=5.6, y_length=4.2, xticks=[], yticks=[0, 0.5, 1], center=[-2.8, -0.4, 0])
        ax = A.ax
        labs = VGroup(*[label(n, font_size=24, color=c).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k, (n, c) in enumerate(zip(NAMES, SC))])

        def bars_at(t):
            return VGroup(*[bars(ax, [k], [flows[t][k]], SC[k], width=0.7) for k in range(3)])
        cur = bars_at(0)
        tl = MathTex(r"t = 0", font_size=36).move_to([2.0, 2.4, 0])
        rows = [
            cmath(r"\pi_{t+1}", r"=", r"\pi_t P", font_size=36),
            cmath(r"\pi_t", r"=", r"\pi_0 P^t", font_size=36),
            cmath(r"\pi", r"=", rf"({st_[0]:.3f},\ {st_[1]:.3f},\ {st_[2]:.3f})", font_size=32),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"total probability (Part 2), \ written as a row vector times $P$"), why(r"so $t$ steps are $P^t$"),
                why(r"where every start ends up")]
        dash = VGroup(*[DashedLine(ax.c2p(k - 0.45, st_[k]), ax.c2p(k + 0.45, st_[k]), color=EXACT, stroke_width=2) for k in range(3)])
        with self.voiceover(
            "Now think of probability as a fluid flowing between the states. <bookmark mark='a'/> Start certain that "
            "today is sunny: all the mass on one bar. <bookmark mark='b'/> Tomorrow's distribution is today's row "
            "vector times P: Part 2's law of total probability, as matrix multiplication. <bookmark mark='c'/> Step "
            "after step, the mass redistributes, <bookmark mark='d'/> and settles: after about ten days it no longer "
            "changes. Forty-six percent sunny, thirty-two cloudy, twenty-two rainy. Start from rain instead and you "
            "end up in the same place: the chain forgets where it began."
        ) as vo:
            self.play(FadeIn(A), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(cur), FadeIn(tl))
            step = ladder(self, rows, whys, keep=3, top=1.6, x=3.6, buff=1.0, edge=6.9)
            vo.wait_until("b")
            step(0, transform=False)
            vo.wait_until("c")
            for t in range(1, 6):
                self.play(Transform(cur, bars_at(t)), Transform(tl, MathTex(rf"t = {t}", font_size=36).move_to(tl)), run_time=0.8)
            step(1, transform=False)
            vo.wait_until("d")
            for t in range(6, 13):
                self.play(Transform(cur, bars_at(t)), Transform(tl, MathTex(rf"t = {t}", font_size=36).move_to(tl)), run_time=0.4)
            self.play(Create(dash))
            step(2, transform=False)
        self.clear_scene()

    def rate(self):
        d = load("chain")
        ev = np.asarray(d["eig"])
        flows = np.asarray(d["flows"])
        st_ = np.asarray(d["stationary"])
        dist = [0.5 * np.abs(f - st_).sum() for f in flows]
        A = axes([0, 12], [-4, 0], x_length=6.4, y_length=4.0, xlabel=r"day $t$", ylabel=r"distance to $\pi$ (log scale)",
                 xticks=[0, 4, 8, 12], yticks=[-4, -3, -2, -1, 0], yfmt=lambda v: f"10^{{{int(v)}}}", center=[-3.0, -0.5, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(t, np.log10(max(v, 1e-4))), radius=0.07, color=CHAIN) for t, v in enumerate(dist)])
        ln = polyline(ax, np.arange(13), np.log10(np.maximum(dist, 1e-4)), CHAIN, 2.5)
        guide = polyline(ax, np.arange(13), np.log10(dist[1]) + (np.arange(13) - 1) * np.log10(ev[1]), GREY_B, 1.5)
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{eigenvalues of }} P:\ 1,\ {ev[1]:.3f},\ {ev[2]:.3f}", font_size=28),
            label(r"the eigenvalue 1: \ the stationary law (chapter 9)", font_size=24, color=EXACT),
            MathTex(rf"\text{{the next one: }} \|\pi_t - \pi\| \approx C\, {ev[1]:.2f}^t", font_size=28, color=CHAIN),
            label(r"a straight line on a log scale: \ geometric convergence", font_size=24, color=GREY_A),
            label(r"Part 4's spectral ideas, \ for a matrix that need not be symmetric", font_size=22, color=GREY_B),
        ), 5.6, 0.3, [3.6, 0.2, 0])
        with self.voiceover(
            "How fast does it forget? <bookmark mark='a'/> Plot the distance to the settled distribution, on a log "
            "scale: a straight line, so the distance shrinks by the same factor every day. <bookmark mark='b'/> "
            "That factor is the transition matrix's second-largest eigenvalue, here point four six. The largest "
            "is always exactly one, and its eigenvector is the settled distribution itself, which is the subject of "
            "the next chapter. The closer the second eigenvalue is to one, the slower the chain forgets."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ln), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(guide), FadeIn(rows))
        self.clear_scene()

    def onegin(self):
        rows = [
            cmath(r"P", r"=", r"\begin{pmatrix} 0.128 & 0.872 \\ 0.663 & 0.337 \end{pmatrix}", r"\quad \begin{matrix} \text{after a vowel} \\ "
                  r"\text{after a consonant} \end{matrix}", font_size=30),
            cmath(r"\pi_{\text{vowel}}", r"=", r"\frac{0.663}{0.872 + 0.663}", r"=", r"0.432", font_size=32),
        ]
        rows[1][4].set_color(EXACT)
        whys = [why(r"Markov's counts of 20,000 letters: \ vowels rarely follow vowels"),
                why(r"a two-state chain's long-run share: \ $b/(a + b)$")]
        res = fit_rows(VGroup(
            label(r"Markov's direct count of vowels: \ 43.2\%", font_size=26, color=S.MUSEUM),
            label(r"the chain's stationary law reproduces it: \ the first statistical check of a Markov model", font_size=24,
                  color=GREY_A),
            label(r"his point: \ the law of large numbers does not need independence", font_size=24, color=S.ACCENT),
        ), 12.6, 0.3, [0, -1.9, 0])
        tag = historical_tag(r"Markov (1913), \ as reported by B. Hayes, \ \emph{American Scientist} (2013)", corner=DR)
        with self.voiceover(
            "Markov's own numbers make a perfect first example. <bookmark mark='a'/> After a vowel, the next letter of "
            "Onegin was a vowel only about thirteen percent of the time; after a consonant, sixty-six percent. "
            "<bookmark mark='b'/> A two-state chain spends a long-run share of its time in each state that's easy to "
            "compute: the chance of entering a state, over the total chance of switching. For vowels: about forty-three "
            "percent. <bookmark mark='c'/> Markov's direct count of vowels in the text: forty-three point two percent. "
            "His real point was philosophical: the law of large numbers, which Nekrasov had claimed required "
            "independence, holds for dependent sequences too."
        ) as vo:
            self.play(FadeIn(tag))
            step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.0, buff=1.1, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.4))
        self.clear_scene()

    def ergodic(self):
        d = load("chain")
        P = np.asarray(d["P"])
        st_ = np.asarray(d["stationary"])
        g = np.random.Generator(np.random.PCG64(1913))
        x, path = 0, []
        for _ in range(3000):
            x = int(g.choice(3, p=P[x]))
            path.append(x)
        path = np.asarray(path)
        n = np.arange(1, 3001)
        shares = [np.cumsum(path == k) / n for k in range(3)]
        A = axes([0, 3.48], [0, 1.0], x_length=7.2, y_length=4.0, xlabel=r"days simulated (log scale)", ylabel=r"share of days",
                 xticks=[0, 1, 2, 3], yticks=[0, 0.25, 0.5, 0.75, 1], xfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.0, -0.5, 0])
        ax = A.ax
        lines = VGroup(*[polyline(ax, np.log10(n), shares[k], SC[k], 2.5) for k in range(3)])
        dash = VGroup(*[DashedLine(ax.c2p(0, st_[k]), ax.c2p(3.48, st_[k]), color=SC[k], stroke_width=1.5) for k in range(3)])
        strip = VGroup(*[Square(side_length=0.16, stroke_width=0, fill_color=SC[v], fill_opacity=1).move_to([-5.4 + 0.17 * i, 3.2, 0])
                         for i, v in enumerate(path[:64])])
        rows = fit_rows(VGroup(
            label(r"one long run of the weather chain", font_size=24),
            label(r"the share of sunny, cloudy, rainy days $\to \pi$", font_size=24, color=EXACT),
            label(r"the ergodic theorem: \ a time average of one path equals the average over $\pi$", font_size=22, color=CHAIN),
            label(r"why one long MCMC run can stand in for independent draws", font_size=22, color=GREY_A),
        ), 4.8, 0.28, [4.4, -0.4, 0])
        with self.voiceover(
            "There's a second way to see the stationary law. <bookmark mark='a'/> Instead of evolving the whole "
            "distribution, simulate one long run of the chain: here are its first sixty-four days. "
            "<bookmark mark='b'/> Track the share of sunny, cloudy and rainy days so far. After a few thousand days "
            "they settle onto the stationary probabilities. <bookmark mark='c'/> That's the ergodic theorem for "
            "Markov chains: the time average along a single path equals the average under the stationary law. It's "
            "why one long run of a Markov chain, in chapter eleven, can stand in for independent draws."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in strip], lag_ratio=0.03), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(dash), Create(lines), FadeIn(rows[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()
