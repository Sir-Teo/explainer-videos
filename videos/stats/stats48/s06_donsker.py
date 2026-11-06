from __future__ import annotations

import numpy as np

from videos.stats.stats48.common import *  # noqa: F403


class Donsker(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.conditions()
        self.table()
        self.faithful()
        self.failures()

    def card(self):
        card = chapter_card(5, r"Donsker classes", r"A central limit theorem, uniformly over a class", lit=(1952,), part=PART)
        with self.voiceover("Chapter five. Donsker classes: a central limit theorem, uniformly over a class."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\mathbb G_n f", r"=", r"\sqrt n\,(P_n f - P f), \quad f \in \mathcal F", font_size=36),
            cmath(r"\text{finite-dimensional}", r":", r"(\mathbb G_n f_1, \dots, \mathbb G_n f_k) \Rightarrow N(0, \Sigma), \ \Sigma_{ij} = \mathrm{Cov}(f_i, f_j)", font_size=30),
            cmath(r"\mathcal F \text{ is Donsker}", r":", r"\mathbb G_n \Rightarrow \mathbb G \ \text{ in } \ell^\infty(\mathcal F), \ \text{a tight Gaussian process}", font_size=30),
            cmath(r"\text{then}", r":", r"\sup_{\mathcal F} |\mathbb G_n f| \Rightarrow \sup_{\mathcal F} |\mathbb G f| \ \text{and every continuous functional}", font_size=30),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(CLASSC)
        whys = [why(r"the empirical process"), why(r"the ordinary multivariate CLT"), why(r"tightness: \ the extra condition"), why(r"the continuous mapping theorem")]
        with self.voiceover(
            "<bookmark mark='a'/> The empirical process is a random function on the class. <bookmark mark='b'/> At finitely "
            "many functions it is asymptotically normal by the ordinary multivariate central limit theorem, with the "
            "covariances of the functions as its covariance. That part is free. <bookmark mark='c'/> A class is Donsker "
            "if the whole process converges, as a random element of the space of bounded functions on the class, to a "
            "tight Gaussian process called the P Brownian bridge. The extra ingredient is tightness: the process must not "
            "oscillate wildly between nearby functions. <bookmark mark='d'/> Then, by the continuous mapping theorem, its "
            "supremum converges to the Gaussian supremum, and so does every other continuous functional of it: Doob's "
            "heuristic made into a theorem."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def conditions(self):
        rows = [
            cmath(r"\text{tightness}", r"\Leftarrow", r"\lim_{\delta \to 0} \limsup_n E \sup_{\rho(f, g) < \delta} |\mathbb G_n f - \mathbb G_n g| = 0", font_size=30),
            cmath(r"\int_0^1 \sqrt{\log N_{[\,]}(\varepsilon, \mathcal F, L_2(P))}\, d\varepsilon < \infty", r"\Rightarrow", r"\text{Donsker}", font_size=30),
            cmath(r"\int_0^1 \sup_Q \sqrt{\log N(\varepsilon \|F\|_{Q,2}, \mathcal F, L_2(Q))}\, d\varepsilon < \infty", r"\Rightarrow", r"\text{Donsker}", font_size=28),
            cmath(r"\text{VC classes}", r":", r"\text{uniform entropy } \asymp V\log(1/\varepsilon): \ \text{Donsker for every } P", font_size=30),
        ]
        rows[1][-1].set_color(GOODC)
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(CLASSC)
        whys = [why(r"asymptotic equicontinuity"), why(r"Ossiander (1987)"), why(r"Pollard (1982); \ Dudley; \ $F$ an envelope"), why(r"Dudley (1978)")]
        with self.voiceover(
            "<bookmark mark='a'/> Tightness comes down to asymptotic equicontinuity: the process's largest increment between "
            "functions closer than delta must vanish as delta shrinks. And that is exactly what chaining controls. "
            "<bookmark mark='b'/> With brackets: if the bracketing entropy integral is finite, the class is Donsker, a "
            "theorem of Mina Ossiander's. <bookmark mark='c'/> Without brackets: if the uniform entropy integral is finite, "
            "the class is Donsker, with the entropy measured in the worst probability measure, relative to an envelope F. "
            "That is due to David Pollard, building on Dudley. <bookmark mark='d'/> VC classes have uniform entropy V log "
            "one over epsilon, whose root is integrable, so every VC class is Donsker for every distribution. The half-lines "
            "are one, and the Kolmogorov–Smirnov limit follows."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("donsker")
        rows = [[r"$n$", r"exact 95\% point of $\sqrt n D_n$", r"Kolmogorov's limit", r"size of the limit's test"]]
        for r in d["rows"]:
            rows.append([f"{r['n']:,}", f"{r['exact']:.4f}", f"{r['kolm']:.4f}", f"{100 * r['size_kolm']:.2f}\\%"])
        tab = table_rows(rows, font_size=28, col_buff=0.8, row_buff=0.33, colors=[GREY_B] + [None] * 6)
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.7, 0])
        foot = label(r"exact: \ the finite-$n$ law of $D_n$ \ (Marsaglia, \ Tsang \& Wang 2003); \ the limit is conservative, \ and close by $n = 50$", font_size=22, color=GREY_A).move_to([0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> How good is the limit? The exact finite-sample law of the Kolmogorov statistic is known, "
            f"and computable to full precision by an algorithm of Marsaglia, Tsang and Wang. Its ninety-five percent point, "
            f"times root n, is {say(d['rows'][0]['exact'], 3)} at five observations and {say(d['rows'][4]['exact'], 3)} at a hundred, "
            f"rising toward Kolmogorov's {say(d['k95'], 3)}. <bookmark mark='b'/> So the limit's critical value is a little "
            f"too big, and a test using it has true size {100 * d['rows'][0]['size_kolm']:.1f} percent at five observations "
            f"and {100 * d['rows'][3]['size_kolm']:.1f} at fifty: conservative, but close."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(exact_tag(r"exact")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def faithful(self):
        d = load("donsker")
        g = np.asarray(d["grid"])
        A = axes([40, 100], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"waiting time (minutes)", ylabel=r"$F(x)$",
                 xticks=[40, 50, 60, 70, 80, 90, 100], yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        band = VMobject(fill_color=EMPC, fill_opacity=0.22, stroke_width=0)
        band.set_points_as_corners([ax.c2p(a, b) for a, b in zip(g, d["hi"])] + [ax.c2p(a, b) for a, b in zip(g[::-1], np.asarray(d["lo"])[::-1])])
        fn = polyline(ax, g, d["fn"], EMPC, 3.5)
        fit = polyline(ax, g, d["fit"], BADC, 3.5)
        side = fit_rows(VGroup(
            label(rf"Old Faithful: \ {d['n']} waiting times", font_size=22),
            label(r"blue: \ $F_n$, \ the empirical CDF", font_size=22, color=EMPC),
            label(rf"band: \ $F_n \pm {d['half']:.3f}$, \ i.e.\ $\pm 1.358/\sqrt n$", font_size=22, color=EMPC),
            label(rf"red: \ the fitted normal, \ $N({d['mean']:.1f}, {d['sd']:.1f}^2)$", font_size=22, color=BADC),
            label(rf"it leaves the band: \ $D$ = {d['d_norm']:.3f} \ (but see chapter 12)", font_size=22, color=CLASSC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A real example. The waiting times between {d['n']} eruptions of Old Faithful, in Yellowstone, "
            f"from the Museum. <bookmark mark='b'/> Their empirical distribution function, <bookmark mark='c'/> and around it a "
            f"ninety-five percent confidence band for the true distribution function: plus or minus Kolmogorov's quantile "
            f"over root n, {say(d['half'], 3)}. Every continuous distribution function that stays inside the band is "
            f"consistent with the data. <bookmark mark='d'/> The normal distribution with the sample's mean and standard "
            f"deviation does not stay inside: <bookmark mark='e'/> its largest distance from the data is {say(d['d_norm'], 3)}, "
            f"nearly twice the band's half-width, because the waits are bimodal. Strictly, testing a fitted normal needs the "
            f"correction of chapter twelve, but this one fails by a wide margin."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Old Faithful (Azzalini \& Bowman 1990)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(fn), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(band), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(fit), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def failures(self):
        rows = fit_rows(VGroup(
            label(r"Donsker is stronger than Glivenko--Cantelli: \ it fixes the rate, \ $1/\sqrt n$, \ and the limit", font_size=26),
            label(r"too rich to be Donsker: \ smooth functions with $\alpha \le d/2$; \ convex sets in $\mathbb R^d$, \ $d \ge 4$", font_size=26, color=BADC),
            label(r"there the sup still goes to 0, \ but more slowly than $1/\sqrt n$: \ chapter 9's rates", font_size=26, color=CLASSC),
            label(r"Donsker classes are what make $\sqrt n$-asymptotics of M-estimators, \ bootstraps and bands work", font_size=26, color=GOODC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Being Donsker is a stronger property than being Glivenko–Cantelli: it fixes the rate, "
            "one over root n, and the limiting law. <bookmark mark='b'/> Some classes are Glivenko–Cantelli without being "
            "Donsker: smoothness classes whose smoothness is no more than half the dimension, or the convex sets in four or "
            "more dimensions. <bookmark mark='c'/> For those, the uniform law of large numbers still holds, but the "
            "supremum shrinks more slowly than root n, which is where chapter nine's rates come from. <bookmark mark='d'/> "
            "Donsker classes are what make the root n theory of M-estimators, the bootstrap and confidence bands work, and "
            "the next chapters use them for all three."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
