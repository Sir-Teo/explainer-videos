from __future__ import annotations

import numpy as np

from videos.stats.stats44.common import *  # noqa: F403


class Mixing(VoiceoverScene):
    def construct(self):
        self.card()
        self.coupling()
        self.cycle()
        self.hypercube()
        self.shuffles()
        self.polya()

    def card(self):
        card = chapter_card(9, r"Coupling and mixing", r"How long until a chain forgets where it started?", lit=(1992,), part=PART)
        with self.voiceover("Chapter nine. Coupling and mixing: how long until a chain forgets where it started?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def coupling(self):
        rows = [
            cmath(r"d(t)", r"=", r"\max_x \|P^t(x, \cdot) - \pi\|_{TV}, \ \ t_{\text{mix}} = \min\{t : d(t) \le \tfrac14\}", font_size=32),
            cmath(r"\text{coupling}", r":", r"(X_t, Y_t), \ X_0 = x, \ Y_0 \sim \pi, \ \text{together after they meet at } \tau", font_size=30),
            cmath(r"\|P^t(x, \cdot) - \pi\|_{TV}", r"\le", r"P(X_t \ne Y_t) = P(\tau > t)", font_size=32),
            cmath(r"\text{Doeblin}", r":", r"P^m(x, \cdot) \ge \varepsilon\, \pi \ \Rightarrow \ d(t) \le (1 - \varepsilon)^{\lfloor t/m \rfloor}", font_size=32),
        ]
        rows[2][-1].set_color(MARTC)
        whys = [why(r"distance and mixing time"), why(r"two copies, \ one law each"), why(r"the coupling inequality"), why(r"Doeblin (1938)")]
        with self.voiceover(
            "<bookmark mark='a'/> For finite chains we can measure exactly how far a chain is from stationarity after t "
            "steps: the total variation distance from the worst start. The mixing time is when it first falls below a "
            "quarter. <bookmark mark='b'/> Wolfgang Doeblin's device for bounding it is coupling: run two copies, one from x "
            "and one from the stationary law, on a shared source of randomness, so that once they meet they move together. "
            "<bookmark mark='c'/> The distance at time t is at most the chance they have not yet met. <bookmark mark='d'/> "
            "And if, after m steps, every start has at least an epsilon chance of being drawn from the stationary law, the "
            "distance decays geometrically. This part's lab computes all of these exactly."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cycle(self):
        d = load("mixing")
        ts = np.asarray(d["ts"], float)
        A = axes([0, 400], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"steps $t$", ylabel=r"distance from uniform",
                 xticks=[0, 100, 200, 300, 400], yticks=[0, 0.25, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        dc = polyline(ax, ts, d["d_cycle"], CHAINC, 4)
        ct = polyline(ax, ts, d["coupling_tail"], MARTC, 3)
        q = DashedLine(ax.c2p(0, 0.25), ax.c2p(400, 0.25), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"the lazy walk on a cycle of {d['n']} sites", font_size=22),
            label(rf"blue: \ $d(t)$, \ exact; \ $t_{{\text{{mix}}}} = {d['tmix_cycle']}$", font_size=22, color=CHAINC),
            label(rf"gold: \ $P(\tau > t)$ for the classical coupling \ (mean {d['coupling_mean']:.0f} $= n^2/4$)", font_size=22, color=MARTC),
            label(rf"spectral gap {d['gap_cycle']:.4f}: \ relaxation time {d['relax_cycle']:.1f}", font_size=22, color=GREY_A),
            label(r"both scale like $n^2$: \ diffusion", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The lazy random walk on a cycle of twenty sites: at each step stay put with probability one "
            f"half, else move to a neighbour. <bookmark mark='b'/> In blue, its exact distance from the uniform law, from a "
            f"fixed start; it falls below a quarter after {d['tmix_cycle']} steps. <bookmark mark='c'/> In gold, the chance "
            f"that the classical coupling has not yet joined: two walkers, a coin deciding which one moves, so their gap does "
            f"a random walk until it closes, on average after n squared over four, a hundred steps. It bounds the distance "
            f"from above, as it must. <bookmark mark='d'/> The spectral gap, one minus the second eigenvalue, gives the "
            f"relaxation time, {say(d['relax_cycle'], 1)}. <bookmark mark='e'/> All of them grow like n squared: on a cycle, "
            f"mixing is diffusion."
        ) as vo:
            self.play(FadeIn(A), FadeIn(q), FadeIn(exact_tag(r"exact: matrix powers; \ coupling simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(dc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ct), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def hypercube(self):
        d = load("mixing")
        A = axes([0, 6], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"steps $/\, d$", ylabel=r"distance from uniform",
                 xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 0.25, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"10": CHAINC, "40": MARTC}
        lines = VGroup()
        for k, c in cols.items():
            h = d["hyper"][k]
            t = np.asarray(h["t"], float) / int(k)
            lines.add(polyline(ax, t, h["d"], c, 4))
        q = DashedLine(ax.c2p(0, 0.25), ax.c2p(6, 0.25), color=GREY_B, stroke_width=2)
        h10, h40 = d["hyper"]["10"], d["hyper"]["40"]
        side = fit_rows(VGroup(
            label(r"lazy walk on $\{0, 1\}^d$: \ re-flip a random bit", font_size=22),
            label(rf"$d = 10$: \ $t_{{\text{{mix}}}} = {h10['tmix']}$", font_size=22, color=CHAINC),
            label(rf"$d = 40$: \ $t_{{\text{{mix}}}} = {h40['tmix']}$", font_size=22, color=MARTC),
            label(r"order $d \log d$, \ and a sharp drop: \ the cutoff phenomenon", font_size=22, color=S.ACCENT),
            label(r"exact: \ lump states by their number of 1s", font_size=22, color=GREY_B),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A walk on the corners of a d-dimensional cube: at each step pick a coordinate and reset "
            f"it with a fair coin. <bookmark mark='b'/> With ten dimensions it mixes in {h10['tmix']} steps; <bookmark "
            f"mark='c'/> with forty, in {h40['tmix']}: <bookmark mark='d'/> of order d log d, not d squared, and, plotted "
            f"against steps per dimension, the drop sharpens as d grows: the distance stays near one, then falls almost at "
            f"once. Persi Diaconis named it the cutoff phenomenon. <bookmark mark='e'/> The cube has two to the forty corners, "
            f"but from the all-zeros start only the number of ones matters, so the exact computation needs forty-one states."
        ) as vo:
            self.play(FadeIn(A), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lines[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lines[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def shuffles(self):
        d = load("mixing")
        r = np.asarray(d["riffle"])
        A = axes([0.4, 10.6], [0, 1.15], x_length=7.4, y_length=4.4, xlabel=r"riffle shuffles $k$", ylabel=r"distance from a uniform deck",
                 xticks=list(range(1, 11)), yticks=[0, 0.25, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = bars_at(ax, np.arange(1, 11), r, 0.7, CHAINC, opacity=0.8, highlight=[6], hcolor=MARTC)
        vals = VGroup(*[label(f"{v:.3f}", font_size=16, color=GREY_A).next_to(bars[i], UP, buff=0.05) for i, v in enumerate(r)])
        side = fit_rows(VGroup(
            label(r"52 cards, \ Gilbert--Shannon--Reeds riffles", font_size=22),
            label(r"$r$ rising sequences: \ probability $\binom{2^k + 52 - r}{52} / 2^{52k}$", font_size=22, color=GREY_A),
            label(rf"exact, \ over all $52!$ orders: \ seven shuffles leave {r[6]:.3f}", font_size=22, color=MARTC),
            label(r"Bayer \& Diaconis (1992): \ ``seven shuffles suffice''", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The most famous mixing time is a card trick. Model a riffle shuffle as Gilbert, Shannon "
            f"and Reeds did: cut the deck binomially and drop cards from the two halves in proportion to their sizes. "
            f"<bookmark mark='b'/> Dave Bayer and Persi Diaconis found, in 1992, that after k shuffles the probability of an "
            f"order depends only on its number of rising sequences, through a single binomial coefficient. <bookmark "
            f"mark='c'/> That makes the distance from a uniform deck computable exactly over all fifty-two factorial orders. "
            f"The lab does it: the distance stays at one for four shuffles, falls to {say(r[5], 2)} at six, and "
            f"{say(r[6], 2)} at seven, the first time it is below a half. <bookmark mark='d'/> Hence the headline: seven "
            f"shuffles suffice. A casino that shuffles three times deals a deck that is still, in total variation, almost "
            f"perfectly predictable."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: Eulerian numbers, \ big integers")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars), FadeIn(vals), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def polya(self):
        d = load("polya")
        steps = np.log10(np.asarray(d["steps"], float))
        A = axes([1, 4], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"steps", ylabel=r"P(back at the origin by then)",
                 xticks=[1, 2, 3, 4], yticks=[0, 0.34, 0.5, 1], log_x=True, xfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"1": GOODC, "2": MARTC, "3": BADC}
        lines = VGroup()
        for k, c in cols.items():
            lines.add(VGroup(polyline(ax, steps, d["ret"][k], c, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=c) for a, b in zip(steps, d["ret"][k])]))
        lim = DashedLine(ax.c2p(1, d["polya3"]), ax.c2p(4, d["polya3"]), color=BADC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"one dimension: \ returns, \ surely", font_size=24, color=GOODC),
            label(r"two: \ returns too, \ but slowly ($\sim 1/\log n$ still out)", font_size=24, color=MARTC),
            label(rf"three: \ returns with probability only {d['polya3']}", font_size=24, color=BADC),
            label(r"Kakutani: \ ``a drunk man will find his way home, \ a drunk bird may be lost forever''", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Whether a chain returns at all is the question George Pólya answered in 1921, after "
            f"meeting the same couple again and again on his walks in a Zürich park. A simple random walk on the line "
            f"returns to its start with probability one. <bookmark mark='b'/> On the plane it also returns surely, but so "
            f"slowly that after ten thousand steps over a quarter of walks are still out. <bookmark mark='c'/> In three "
            f"dimensions it returns with probability only point three four: it is transient. <bookmark mark='d'/> The "
            f"saying attributed to Shizuo Kakutani puts it best: a drunk man will find his way home, but a drunk bird may "
            f"get lost forever."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 300 to 800 walks per point")))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lines[2]), Create(lim), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
