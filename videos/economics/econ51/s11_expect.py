from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403

TAU = "#F2A65A"
ROUW = "#7FD1B9"


def heat(P, col, size=0.62):
    P = np.asarray(P)
    n = len(P)
    g = VGroup()
    for i in range(n):
        for j in range(n):
            v = float(P[i, j])
            sq = Square(side_length=size, stroke_width=0.8, stroke_color=GREY_D, fill_color=col,
                        fill_opacity=min(1.0, v ** 0.5) * 0.95)
            sq.move_to([j * size, -i * size, 0])
            txt = label(f"{v:.2f}" if v >= 0.005 else r"0", font_size=12,
                        color=BLACK if v > 0.5 else GREY_A).move_to(sq)
            g.add(VGroup(sq, txt))
    return g


class Expectations(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Expectations: \ chains and quadrature", r"How should a computer take an average over the "
                                                               r"future?",
             "Chapter nine. Expectations: chains and quadrature.",
             lit={1986: r"Tauchen", 1995: r"Rouwenhorst", 2010: r"Kopecky and Suen"}, scale=("household",),
             horizon=("a lifetime",))
        self.chains()
        self.numbers()
        self.quadrature()

    def chains(self):
        E_ = load("expect")["0.99"]
        h1 = heat(E_["tauchen"]["P"], TAU)
        h2 = heat(E_["rouwenhorst"]["P"], ROUW)
        VGroup(h1, h2).arrange(RIGHT, buff=1.6).move_to(DOWN * 0.3)
        t1 = label(r"Tauchen (1986)", font_size=24, color=TAU).next_to(h1, UP, buff=0.3)
        t2 = label(r"Rouwenhorst (1995)", font_size=24, color=ROUW).next_to(h2, UP, buff=0.3)
        head = label(r"five income states \ $\cdot$ \ persistence 0.99: \ the chance of moving from row to column",
                     font_size=22, color=WHITE).to_edge(UP, buff=0.5)
        n1 = label(r"the chain never moves", font_size=19, color=TAU).next_to(h1, DOWN, buff=0.3)
        n2 = label(r"a small step, \ now and then", font_size=19, color=ROUW).next_to(h2, DOWN, buff=0.3)
        with self.voiceover(
            "Most economic models need an average over the future, and the future is usually a continuous random "
            "process, such as income following an autoregression. A computer must replace it with something "
            "finite. <bookmark mark='a'/> The common way is a Markov chain on a few states. George Tauchen's method "
            "of 1986 places the states evenly and assigns the transition probabilities from the normal "
            "distribution. <bookmark mark='b'/> With five states and persistence of 0.99, typical of yearly "
            "income, its chain never moves: the chance of staying put rounds to one, because the states are too far "
            "apart for a small shock to cross. <bookmark mark='c'/> K. Geert Rouwenhorst's construction of 1995 "
            "builds the chain differently, so that it moves by a small step now and then. <bookmark mark='d'/> "
            "Karen Kopecky and Richard Suen showed in 2010 that for persistent processes it is the one to use."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(h1))
            vo.wait_until("b")
            self.play(FadeIn(n1), Indicate(h1, color=WHITE, scale_factor=1.02))
            vo.wait_until("c")
            self.play(FadeIn(t2), FadeIn(h2), FadeIn(n2))
            vo.wait_until("d")
            self.play(Indicate(h2, color=WHITE, scale_factor=1.02))
        self.clear_scene()

    def numbers(self):
        E_ = load("expect")
        rows = VGroup()
        hdr = VGroup(*[label(t, font_size=19, color=GREY_A) for t in (r"persistence", r"", r"implied persistence",
                                                                       r"implied spread", r"true spread")])
        xs = [-4.8, -2.6, -0.2, 2.4, 4.8]
        for m_, x in zip(hdr, xs):
            m_.move_to([x, 2.0, 0])
        y = 1.1
        for key in ("0.9", "0.99"):
            e = E_[key]
            for name, col in (("tauchen", TAU), ("rouwenhorst", ROUW)):
                r = e[name]
                rho_s = "1.0000" if r["rho"] > 0.99995 else f"{r['rho']:.4f}"
                g = VGroup(label(key, font_size=21, color=WHITE), label(name.capitalize(), font_size=21, color=col),
                           label(rho_s, font_size=21, color=col),
                           label(f"{r['sd']:.4f}", font_size=21, color=col),
                           label(f"{e['true_sd']:.4f}", font_size=21, color=WHITE))
                for m_, x in zip(g, xs):
                    m_.move_to([x, y, 0])
                rows.add(g)
                y -= 0.6
            y -= 0.3
        foot = label(r"Rouwenhorst's chain matches the persistence and the spread exactly, \ at any persistence",
                     font_size=21, color=ROUW).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The numbers. <bookmark mark='a'/> With persistence 0.9, Tauchen's five-state chain is a little too "
            "persistent, and its spread is about a quarter too large. <bookmark mark='b'/> Rouwenhorst's matches "
            "both exactly. <bookmark mark='c'/> With persistence 0.99, Tauchen's chain is a random walk that never "
            "steps, and its spread is a third too large; <bookmark mark='d'/> Rouwenhorst's is still exact. A "
            "model fed the wrong chain gets the wrong amount of risk, and chapter seven showed how much behaviour "
            "depends on risk."
        ) as vo:
            self.play(FadeIn(hdr))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            self.play(FadeIn(foot))
        self.clear_scene()

    def quadrature(self):
        Q = load("expect")["quadrature"]
        ax = plane([0, 5.2], [-16, 0], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.8, y_length=4.6,
                   xticks=[0, 1, 2, 3, 4, 5], yticks=[-16, -12, -8, -4, 0],
                   xlabel=r"points or draws, \ $\log_{10}$", ylabel=r"error, \ $\log_{10}$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        gx = np.log10(Q["nodes"])
        gy = np.log10(np.maximum(Q["gh"], 1e-16))
        mx = np.log10(Q["draws"])
        my = np.log10(Q["mc"])
        gh = path(ax, gx, gy, PROJ, 2.8, smooth=False)
        mc = path(ax, mx, my, VFI, 2.8, smooth=False)
        gd = VGroup(*[dot(ax, x, y_, PROJ, 0.07) for x, y_ in zip(gx, gy)])
        md = VGroup(*[dot(ax, x, y_, VFI, 0.07) for x, y_ in zip(mx, my)])
        side = VGroup(
            label(r"the average of $e^{\varepsilon/2}$, \\ $\varepsilon$ standard normal", font_size=18, color=WHITE),
            label(r"blue: \ Monte Carlo, \\ error falls like $1/\sqrt{n}$", font_size=18, color=VFI),
            label(r"pink: \ Gauss--Hermite \\ quadrature", font_size=18, color=PROJ),
            label(rf"7 nodes: \ error $10^{{{np.log10(Q['gh'][4]):.0f}}}$; \\ 100,000 draws: \ "
                  rf"$10^{{{np.log10(Q['mc'][-1]):.1f}}}$".replace("100,000", "100{,}000"), font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = label(r"computed", font_size=12, color=GREY_B).to_corner(DL, buff=0.3)
        with self.voiceover(
            "Inside each round, the average itself must be computed. Take the average of e to the half of a "
            "standard normal shock, whose true value is known. <bookmark mark='a'/> Simulate it with random draws, "
            "and the error falls like one over the square root of the number of draws: a hundred times the draws "
            "for ten times the accuracy. <bookmark mark='b'/> Gauss-Hermite quadrature instead places a few points "
            "and weights exactly where a normal distribution needs them. <bookmark mark='c'/> Seven of them beat a "
            "hundred thousand random draws by a factor of hundreds of millions; with ten, the error is at the limit of "
            "the "
            "machine. For smooth functions of normal shocks, quadrature is almost free accuracy; simulation earns "
            "its place when the shocks are many or strange."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(mc), FadeIn(md), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(gh), FadeIn(gd), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
