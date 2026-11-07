from __future__ import annotations

import numpy as np

from videos.stats.stats51.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.sphere()
        self.density()
        self.table()
        self.question()
        self.upgrades()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1922,)).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"pick a point uniformly on the sphere in $\mathbb R^n$; \ look at its first coordinate", font_size=28),
            label(r"in 3 dimensions: \ anything from $-1$ to $1$, \ evenly spread", font_size=26, color=GREY_A),
            label(r"in 1,000 dimensions: \ within $\pm 0.062$ of zero with probability 95\%", font_size=26, color=SPHC),
            label(r"so almost all of the sphere lies near the equator, \ \emph{whichever} equator you pick", font_size=26, color=SPHC),
            label(r"Lévy (1922): \ the first concentration of measure", font_size=26, color=GOODC),
        ), 12.4, 0.55, [0, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Choose a point uniformly at random on the surface of a sphere and look at one of its coordinates. <bookmark mark='b'/> In three dimensions that coordinate is spread evenly between minus one and one: Archimedes knew that the sphere's area is uniform in height. <bookmark mark='c'/> In a thousand dimensions it is within about six hundredths of zero with probability ninety-five percent. <bookmark mark='d'/> So almost all of a high-dimensional sphere lies in a thin band around its equator. And since nothing distinguishes one coordinate from another, the same is true for each fixed equator. This is not a simultaneous claim: every point is the pole of some equator. <bookmark mark='e'/> Paul Lévy noticed this in his 1922 lectures. It was the first instance of what is now called concentration of measure, and it is the key to this part."        ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def sphere(self):
        d = load("hook")
        ns = d["ns"]
        cols = [GREY_B, S.ALT, GAUSSC, SPHC]
        sh = [SphereShell(center=(-5.0 + 3.3 * i, 0.3, 0), radius=1.3) for i in range(4)]
        disks = VGroup()
        for i, n in enumerate(ns[:4]):
            g = VGroup(sh[i].circle(), sh[i].band(d["half95"][i], color=cols[i], opacity=0.45),
                       label(rf"$n = {n:,}$", font_size=24).next_to(sh[i].circle(), DOWN, buff=0.3),
                       label(rf"$|x_1| \le {d['half95'][i]:.3f}$", font_size=22, color=cols[i]).next_to(sh[i].circle(), DOWN, buff=0.75))
            disks.add(g)
        foot = label(r"each shaded band holds 95\% of the sphere's area", font_size=26, color=GREY_A).move_to([0, -2.7, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Each disc stands for a sphere, and the shaded band is the region around the equator that "
            f"holds ninety-five percent of the sphere's area. <bookmark mark='b'/> In three dimensions the band is "
            f"almost the whole sphere, out to {say(d['half95'][0], 2)}. In ten dimensions, out to {say(d['half95'][1], 2)}. "
            f"<bookmark mark='c'/> In a hundred, {say(d['half95'][2], 2)}, and in a thousand, {say(d['half95'][3], 3)}: the band "
            f"narrows like one point nine six over root n. <bookmark mark='d'/> The sphere, in high dimensions, is a thin "
            f"waist of an object."
        ) as vo:
            self.play(FadeIn(exact_tag(r"exact: \ $x_1^2 \sim \mathrm{Beta}(\tfrac12, \tfrac{n-1}{2})$")))
            vo.wait_until("a")
            self.play(FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(disks[0]), FadeIn(disks[1]))
            vo.wait_until("c")
            self.play(FadeIn(disks[2]), FadeIn(disks[3]))
            vo.wait_until("d")
            self.play(Indicate(disks[3][1], color=SPHC))
        self.clear_scene()

    def density(self):
        d = load("hook")
        x = np.asarray(d["x"])
        A = axes([-1, 1], [0, 14], x_length=7.4, y_length=4.4, xlabel=r"$x_1$, \ one coordinate of a uniform point on $S^{n-1}$", ylabel=r"density",
                 xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 5, 10], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"3": GREY_B, "10": S.ALT, "100": GAUSSC, "1000": SPHC}
        cs = {k: clip_curve(ax, x, d["pdf"][k], c, 3.5, ymin=0, ymax=14) for k, c in cols.items()}
        rug = VGroup(*[Line(ax.c2p(v, 0), ax.c2p(v, 0.6), color=EXACTC, stroke_width=1.5) for v in d["sample"]])
        side = fit_rows(VGroup(
            label(r"density $\propto (1 - x^2)^{(n-3)/2}$", font_size=22),
            label(r"grey: \ $n = 3$: \ flat", font_size=22, color=GREY_B),
            label(r"teal, \ blue: \ $n = 10$, \ 100", font_size=22, color=GAUSSC),
            label(r"gold: \ $n = 1{,}000$: \ nearly $N(0, 1/n)$", font_size=22, color=SPHC),
            label(r"white ticks: \ 300 simulated points, \ $n = 1{,}000$", font_size=22, color=EXACTC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The exact law of one coordinate: its density is proportional to one minus x squared, to the "
            "power n minus three over two. <bookmark mark='b'/> In three dimensions the power is zero and the density is flat, "
            "Archimedes' theorem. <bookmark mark='c'/> In ten and a hundred dimensions it is a bump that narrows. <bookmark "
            "mark='d'/> In a thousand dimensions it is almost exactly normal with variance one over n. <bookmark mark='e'/> "
            "And three hundred points simulated on the thousand-dimensional sphere sit exactly where the formula says, in a "
            "sliver around zero."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact; \ ticks simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["3"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["10"]), Create(cs["100"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["1000"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(rug), FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("hook")
        rows = [[r"dimension $n$"] + [f"{n:,}" for n in d["ns"]],
                [r"area within $|x_1| \le 0.1$"] + [f"{100 * v:.1f}\\%" for v in d["band01"]],
                [r"band holding 95\%"] + [f"{v:.3f}" for v in d["half95"]]]
        tab = table_rows(rows, font_size=30, col_buff=0.7, row_buff=0.45, colors=[GREY_B, SPHC, GAUSSC])
        tab.move_to([0, 0.8, 0])
        foot = label(r"a band of fixed width swallows the sphere; \ the band holding a fixed share shrinks like $1/\sqrt n$", font_size=24, color=GREY_A).move_to([0, -1.2, 0])
        foot2 = label(r"95\% near each fixed equator; \ no simultaneous claim over all equators", font_size=26, color=SPHC).move_to([0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The same numbers as a table. The share of the sphere within a tenth of the equator is {100 * d['band01'][0]:.0f} percent in three dimensions, {100 * d['band01'][2]:.0f} percent in a hundred, and {100 * d['band01'][3]:.1f} percent in a thousand. <bookmark mark='b'/> A fixed band swallows the whole sphere, and the band holding a fixed share shrinks like one over root n. <bookmark mark='c'/> Most of the sphere is near any equator fixed in advance. The equator cannot be chosen after seeing the point."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(exact_tag(r"exact")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"the same phenomenon, \ everywhere:", font_size=28, color=GREY_A),
            label(r"a Gaussian vector's length is $\sqrt n \pm 0.7$: \ a thin shell", font_size=26, color=GAUSSC),
            label(r"independent random directions are nearly orthogonal", font_size=26, color=SPHC),
            label(r"Gaussian inputs, \ bounded Lipschitz constant: \ dimension-free concentration", font_size=26, color=GOODC),
            label(r"a random matrix's singular values sit at $\sqrt n \pm \sqrt p$", font_size=26, color=MATC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The sphere's equator is one face of a single phenomenon. <bookmark mark='b'/> A Gaussian vector in n dimensions has length root n, give or take about point seven, whatever n is: it lives on a thin shell. <bookmark mark='c'/> Two independent random directions are almost exactly perpendicular. <bookmark mark='d'/> A Lipschitz function of Gaussian inputs has dimension-free concentration when its Lipschitz constant stays bounded. <bookmark mark='e'/> And the singular values of a random matrix sit in a predictable window. This part makes each of these precise, non-asymptotically, with explicit constants, because Part fifty-two will need them at finite n and p."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(43, r"limit theorems: \ the LLN, \ the CLT, \ large deviations", r"$n \to \infty$ with the dimension fixed",
                         r"chapters 1--3: \ non-asymptotic tails, \ in any dimension"),
            upgrade_card(48, r"chaining and Talagrand for empirical processes", r"function classes, \ one at a time",
                         r"chapters 6--8: \ generic chaining, \ Gaussian comparison, \ widths"),
            upgrade_card(32, r"basis pursuit recovers sparse vectors, \ the Donoho--Tanner curve", r"an empirical phase transition",
                         r"chapters 8--9: \ the statistical dimension explains it"),
        ]
        for c in cards:
            c.scale(0.86)
        VGroup(*cards).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Three promises are due. Part forty-three proved limit theorems with the dimension fixed; "
            "chapters one to three give tail bounds that hold at every n, in every dimension. <bookmark mark='b'/> Part "
            "forty-eight developed chaining and Talagrand's inequality for empirical processes; chapters six to eight turn "
            "them into general tools for Gaussian processes. <bookmark mark='c'/> And Part thirty-two showed basis pursuit "
            "recovering sparse vectors along the Donoho–Tanner curve, as an experiment; chapters eight and nine explain "
            "where that curve comes from."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 51", font_size=34, color=GREY_B), label(r"High-Dimensional Probability", font_size=48)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"sub-Gaussian and sub-exponential variables; \ Hoeffding and Bernstein, \ sharp",
            r"thin shells, \ near-orthogonality, \ Johnson--Lindenstrauss; \ concentration of Lipschitz functions",
            r"random matrices, \ non-asymptotically; \ matrix Bernstein; \ a real covariance spectrum",
            r"chaining revisited; \ Slepian, \ Sudakov, \ Gordon; \ widths and the statistical dimension",
        ], color=SPHC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 43, \ 48").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.hdp}, \ the sphere-and-shell picture").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-one: high-dimensional probability. <bookmark mark='b'/> We'll define sub-Gaussian and sub-exponential variables and sharpen Hoeffding and Bernstein; meet thin shells, near-orthogonality and the Johnson–Lindenstrauss lemma; prove that Lipschitz functions of Gaussians concentrate; bound random matrices without asymptotics, and test the bounds on a real covariance matrix; revisit chaining; compare Gaussian processes with Slepian, Sudakov and Gordon; and end with Gaussian widths and the statistical dimension, which locate the sparse-recovery transition, with a finite-dimensional uncertainty window."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
