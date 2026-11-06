from __future__ import annotations

import numpy as np

from videos.stats.stats51.common import *  # noqa: F403


class Geometry(VoiceoverScene):
    def construct(self):
        self.card()
        self.shell()
        self.table()
        self.angles()
        self.jl()
        self.chart()

    def card(self):
        card = chapter_card(2, r"High-dimensional geometry", r"Thin shells, \ right angles, \ and random projections", lit=(1984,), part=PART)
        with self.voiceover("Chapter two. High-dimensional geometry: thin shells, right angles, and random projections."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def shell(self):
        rows = [
            cmath(r"g \sim N(0, I_n)", r":", r"\|g\|^2 = \textstyle\sum g_i^2, \ \ E\|g\|^2 = n, \ \ \mathrm{SD}(\|g\|^2) = \sqrt{2n}", font_size=32),
            cmath(r"\|g\| - \sqrt n", r"\approx", r"\frac{\|g\|^2 - n}{2\sqrt n} \ \Rightarrow \ \mathrm{SD}(\|g\|) \to \tfrac{1}{\sqrt 2} \approx 0.71", font_size=32),
            cmath(r"P\big(|\|g\| - \sqrt n| \ge t\big)", r"\le", r"2 e^{-c t^2}: \ \text{a shell of width } O(1), \ \text{at every } n", font_size=32),
            cmath(r"\text{so}", r":", r"\text{the Gaussian in } \mathbb R^{1000} \text{ is a soap bubble, \ not a ball}", font_size=34),
        ]
        rows[2][-1].set_color(GAUSSC)
        rows[3][-1].set_color(SPHC)
        whys = [why(r"a $\chi^2_n$"), why(r"the delta method"), why(r"concentration of the norm"), why(r"almost no mass near the centre")]
        with self.voiceover(
            "<bookmark mark='a'/> Take a standard Gaussian vector in n dimensions. Its squared length is a chi-square with n "
            "degrees of freedom: mean n, standard deviation root two n. <bookmark mark='b'/> Taking the square root, the "
            "length is root n plus a fluctuation whose standard deviation tends to one over root two, about point seven one, "
            "whatever n is. <bookmark mark='c'/> And the tails are Gaussian: the length is within t of root n except with "
            "probability e to the minus c t squared. <bookmark mark='d'/> So a Gaussian in a thousand dimensions does not "
            "fill a ball. Its mass sits on a thin spherical shell of radius about thirty-two, like a soap bubble, with almost "
            "nothing near the centre, even though the density is largest there."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("shells")
        rows = [[r"$n$", r"$E\|g\|$", r"simulated", r"$\mathrm{SD}\|g\|$", r"simulated", r"SD of $\langle u, v\rangle$", r"SD of the angle"]]
        for r in d["rows"]:
            rows.append([f"{r['n']:,}", f"{r['chi_mean']:.2f}", f"{r['mean']:.2f}", f"{r['chi_sd']:.3f}", f"{r['sd']:.3f}", f"{r['ip_sd']:.3f}",
                         f"{r['angle_sd_deg']:.1f}$^\\circ$"])
        tab = table_rows(rows, font_size=28, col_buff=0.6, row_buff=0.36, colors=[GREY_B] + [None] * 5)
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.8, 0])
        for i in range(1, 6):
            tab[i][3].set_color(GAUSSC)
            tab[i][5].set_color(SPHC)
        foot = label(r"3,000 draws per row; \ exact $\chi_n$ moments; \ $u, v$ independent uniform directions", font_size=24, color=GREY_A).move_to([0, -1.6, 0])
        foot2 = label(r"the shell's width stays $\approx 0.71$; \ inner products shrink like $1/\sqrt n$; \ angles crowd at $90^\circ$", font_size=24, color=SPHC).move_to([0, -2.4, 0])
        r = d["rows"]
        with self.voiceover(
            f"<bookmark mark='a'/> The numbers. The expected length grows like root n, from {say(r[0]['chi_mean'], 2)} in two "
            f"dimensions to about a hundred in ten thousand, while its standard deviation stays near point seven one: "
            f"{say(r[1]['chi_sd'], 2)} at ten, {say(r[-1]['chi_sd'], 2)} at ten thousand, with simulation agreeing. <bookmark "
            f"mark='b'/> Meanwhile the inner product of two independent random directions has standard deviation one over "
            f"root n, and the angle between them crowds around ninety degrees, with a spread of {r[-2]['angle_sd_deg']:.1f} "
            f"degrees in a thousand dimensions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated; \ exact moments")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def angles(self):
        d = load("shells")
        th = np.degrees(np.asarray(d["theta"]))
        A = axes([0, 180], [0, 0.6], x_length=7.4, y_length=4.4, xlabel=r"angle between two random directions (degrees)", ylabel=r"density per degree",
                 xticks=[0, 45, 90, 135, 180], yticks=[0, 0.2, 0.4], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"3": GREY_B, "10": S.ALT, "100": GAUSSC, "1000": SPHC}
        cs = {k: clip_curve(ax, th, np.asarray(d["angle_pdf"][k]) * np.pi / 180, c, 3.5, ymin=0, ymax=0.6) for k, c in cols.items()}
        side = fit_rows(VGroup(
            label(r"density $\propto \sin^{n-2}\theta$", font_size=22),
            label(r"grey: \ $n = 3$: \ any angle", font_size=22, color=GREY_B),
            label(r"teal, \ blue: \ $n = 10$, \ 100", font_size=22, color=GAUSSC),
            label(r"gold: \ $n = 1{,}000$: \ $90^\circ \pm 2^\circ$", font_size=22, color=SPHC),
            label(r"$e^{c\varepsilon^2 n}$ directions can be nearly orthogonal", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The law of the angle between two random directions has density proportional to the sine of "
            "the angle to the power n minus two. <bookmark mark='b'/> In three dimensions any angle is possible. <bookmark "
            "mark='c'/> As the dimension grows the density squeezes towards ninety degrees, <bookmark mark='d'/> and in a "
            "thousand dimensions two random directions are perpendicular to within a couple of degrees. <bookmark "
            "mark='e'/> A union bound then gives exponentially many directions, e to the c epsilon squared n of them, all "
            "pairwise within epsilon of orthogonal. High-dimensional space has room for far more nearly perpendicular "
            "directions than it has dimensions, which is what makes random features and embeddings work."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["3"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["10"]), Create(cs["100"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["1000"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def jl(self):
        d = load("jl")
        rows = [
            cmath(r"x_1, \dots, x_N \in \mathbb R^d", r",", r"G: k \times d \text{ Gaussian}, \ \ f(x) = Gx/\sqrt k", font_size=34),
            cmath(r"\text{one pair}", r":", r"\|f(x) - f(y)\|^2 / \|x - y\|^2 \sim \chi^2_k / k: \ \text{within } 1 \pm \varepsilon \text{ w.p. } 1 - 2e^{-c\varepsilon^2 k}", font_size=28),
            cmath(r"\text{all } \binom N2 \text{ pairs}", r":", rf"k \ge \frac{{4 \log N}}{{\varepsilon^2/2 - \varepsilon^3/3}}: \ k = {d['k_needed_30']} \text{{ for }} N = {d['N']}, \ \varepsilon = 0.3", font_size=30),
            cmath(r"\text{Johnson \& Lindenstrauss (1984)}", r":", r"\text{the dimension needed does not depend on } d", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(SPHC)
        whys = [why(r"a random projection"), why(r"chapter 1's $\chi^2$ tail"), why(r"a union bound; \ Dasgupta \& Gupta"), why(r"AI, Built, \ Part 3")]
        with self.voiceover(
            f"<bookmark mark='a'/> These facts give the Johnson–Lindenstrauss lemma. Take N points in a huge dimension d, and "
            f"map them by a random Gaussian matrix with k rows, scaled by one over root k. <bookmark mark='b'/> For a single "
            f"pair, the squared distance after projection, relative to before, is a chi-square with k degrees of freedom over "
            f"k, which is within one plus or minus epsilon except with probability e to the minus c epsilon squared k. "
            f"<bookmark mark='c'/> A union bound over all pairs needs only k of order log N over epsilon squared: for two "
            f"hundred points and thirty percent distortion, {d['k_needed_30']} dimensions. <bookmark mark='d'/> William Johnson "
            f"and Joram Lindenstrauss proved this in 1984. The striking part is what is absent: the original dimension d does "
            f"not appear at all."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("jl")
        lk = np.log10([r["k"] for r in d["rows"]])
        A = axes([0.9, 3.4], [-1.0, 0.5], x_length=7.4, y_length=4.4, xlabel=r"projection dimension $k$ \ (log scale)", ylabel=r"$\log_{10}$ worst distortion",
                 xticks=[1, 2, 3], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[-1, -0.5, 0, 0.5], center=[-2.5, 0.2, 0])
        ax = A.ax
        dev = np.log10([r["max_dev"] for r in d["rows"]])
        th = np.log10([r["theory"] for r in d["rows"]])
        cd = VGroup(polyline(ax, lk, dev, SPHC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=SPHC) for a, b in zip(lk, dev)])
        ct = DashedVMobject(polyline(ax, lk, th, BNDC, 3), num_dashes=30)
        w = {r["k"]: r for r in d["rows"]}
        side = fit_rows(VGroup(
            label(rf"{d['N']} points in $\mathbb R^{{{d['d']:,}}}$, \ two loose clusters", font_size=22),
            label(r"gold: \ the worst pair's distortion, \ $\max |\text{ratio} - 1|$", font_size=22, color=SPHC),
            label(r"purple: \ $\sqrt{8 \log N / k}$: \ the slope $-1/2$", font_size=22, color=BNDC),
            label(rf"$k = 500$: \ worst {w[500]['max_dev']:.2f}; \ {100 * w[500]['within10']:.0f}\% of pairs within 10\%", font_size=22, color=GOODC),
            label(r"from 5,000 coordinates to 500, \ geometry kept", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Two hundred points in five thousand dimensions, arranged in two loose clusters, projected "
            f"to k dimensions. <bookmark mark='b'/> In gold, the worst distortion over all nineteen thousand nine hundred pairs. "
            f"<bookmark mark='c'/> It falls like one over root k, as the purple line from the theory predicts. <bookmark "
            f"mark='d'/> At five hundred dimensions the worst pair is distorted by {100 * w[500]['max_dev']:.0f} percent and "
            f"{100 * w[500]['within10']:.0f} percent of pairs are within ten. <bookmark mark='e'/> A tenfold reduction in "
            f"dimension, with the geometry intact, and by a matrix that never looked at the data."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ct), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
