from __future__ import annotations

import numpy as np
from scipy import stats as st

from videos.stats.stats7.common import *  # noqa: F403

COLS = [S.EST, S.LIK, S.POST, S.PRIOR, S.ACCENT, S.ALT]


class Special(VoiceoverScene):
    def construct(self):
        self.card()
        self.box_muller()
        self.box_proof()
        self.gamma()
        self.alias()
        self.cholesky()

    def card(self):
        card = chapter_card(4, r"Special methods", r"Clever transformations, \ one distribution at a time", part=PART)
        with self.voiceover("Chapter four. Special methods."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def box_muller(self):
        d = load("special")
        u1, u2 = np.asarray(d["u1"]), np.asarray(d["u2"])
        z1, z2 = np.asarray(d["z1"])[:600], np.asarray(d["z2"])[:600]
        A = axes([0, 1], [0, 1], x_length=4.0, y_length=4.0, xlabel=r"$U_1$", ylabel=r"$U_2$", xticks=[0, 1], yticks=[0, 1],
                 center=[-4.2, -0.6, 0])
        B = axes([-3.5, 3.5], [-3.5, 3.5], x_length=4.4, y_length=4.4, xlabel=r"$Z_1$", ylabel=r"$Z_2$", xticks=[-2, 0, 2],
                 yticks=[-2, 0, 2], center=[1.0, -0.6, 0])
        dots = VGroup(*[Dot(A.ax.c2p(a, b), radius=0.025, color=GOOD, fill_opacity=0.8) for a, b in zip(u1, u2)])
        f = VGroup(MathTex(r"R = \sqrt{-2\log U_1}", font_size=28), MathTex(r"\Theta = 2\pi U_2", font_size=28),
                   MathTex(r"(Z_1, Z_2) = (R\cos\Theta,\ R\sin\Theta)", font_size=28, color=EXACT))
        f.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([5.0, 1.6, 0])
        if f.width > 3.6:
            f.width = 3.6
        arrow = Arrow([-1.9, -0.6, 0], [-1.3, -0.6, 0], buff=0, color=GREY_B)
        res = label(r"two independent standard normals \ (Box \& Muller, 1958)", font_size=22, color=GREY_A).move_to([4.8, -2.2, 0])
        if res.width > 3.8:
            res.width = 3.8
        with self.voiceover(
            "The normal has no usable inverse CDF, but it has something better: rotational symmetry. "
            "<bookmark mark='a'/> Take two independent uniforms, a point in the unit square. <bookmark mark='b'/> "
            "Turn the first into a radius, root minus two log U one, and the second into an angle, two pi U two. "
            "<bookmark mark='c'/> The point with that radius and angle has two coordinates that are independent "
            "standard normals. George Box and Mervin Muller published it in 1958. Watch the square of uniforms "
            "become the round normal cloud."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots, lag_ratio=0.002))
            vo.wait_until("a")
            self.play(Indicate(A.ax, color=GOOD))
            vo.wait_until("b")
            self.play(FadeIn(f[:2]))
            vo.wait_until("c")
            self.play(FadeIn(B), GrowArrow(arrow), FadeIn(f[2]))
            self.play(*[dt.animate.move_to(B.ax.c2p(np.clip(a, -3.5, 3.5), np.clip(b, -3.5, 3.5))) for dt, a, b in zip(dots, z1, z2)],
                      run_time=3.5)
            self.play(FadeIn(res))
        self.clear_scene()

    def box_proof(self):
        rows = [
            cmath(r"f(z_1, z_2)", r"=", r"\frac{1}{2\pi} e^{-(z_1^2 + z_2^2)/2}", r"=", r"\frac{1}{2\pi}\, \cdot\, r\,e^{-r^2/2}"
                  r"\ \frac{dr\,d\theta}{dz_1 dz_2}", font_size=30),
            cmath(r"\Theta \sim U(0, 2\pi),\quad R", r"\sim", r"\text{Rayleigh: } P(R > r) = e^{-r^2/2}", font_size=30),
            cmath(r"P\big(\sqrt{-2\log U} > r\big)", r"=", r"P(U < e^{-r^2/2})", r"=", r"e^{-r^2/2}", font_size=30),
        ]
        rows[2][4].set_color(EXACT)
        whys = [why(r"the normal pair in polar coordinates: \ Part 5's Jacobian $r$"),
                why(r"angle uniform, \ radius Rayleigh (Part 5), \ independent"), why(r"and the Rayleigh is sampled by inversion")]
        note_ = label(r"Marsaglia's polar method (1964) avoids the sine and cosine \ by rejection from the disc", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Why does it work? Part 5 did the hard part. <bookmark mark='a'/> Two independent standard normals have a "
            "joint density that depends only on the distance from the centre; in polar coordinates, with the "
            "Jacobian r, it separates. <bookmark mark='b'/> So the angle is uniform, independent of the radius, and "
            "the radius has the Rayleigh distribution, whose tail is e to the minus r squared over two. "
            "<bookmark mark='c'/> And that tail is easy to invert: root minus two log U has exactly that tail. "
            "Two inversions and a change of coordinates make two normals. A variant by Marsaglia avoids computing "
            "sines and cosines, by rejection from a disc."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.2, buff=0.95, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            self.play(FadeIn(note_))
        self.clear_scene()

    def gamma(self):
        d = load("special")
        code = code_block([
            "d = alpha - 1/3;  c = 1/sqrt(9d)",
            "repeat:",
            "    Z = normal();  U = uniform()",
            "    V = (1 + c Z)^3",
            "    if V > 0 and log U < Z^2/2 + d - d V + d log V:",
            "        return d V",
        ], font_size=20)
        code.width = min(code.width, 6.4)
        code.move_to([-3.3, 1.0, 0])
        ed = np.linspace(0, 10, 41)
        A = axes([0, 10], [0, 0.35], x_length=4.8, y_length=3.0, xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.1, 0.2, 0.3],
                 center=[3.9, 0.7, 0])
        h = hist_bars(A.ax, ed, np.asarray(d["gamma_hist"]), color=GOOD, opacity=0.75)
        xs = np.linspace(0.01, 10, 200)
        cv = curve(A.ax, xs, st.gamma.pdf(xs, 2.5), EXACT, 3)
        rows = fit_rows(VGroup(
            label(rf"$\alpha = 2.5$: \ acceptance {100 * d['gamma_rate']:.1f}\%", font_size=24, color=ACC),
            label(rf"4,000 draws, \ mean {d['gamma_mean']:.2f} \ (truth 2.5)", font_size=24),
            label(r"Marsaglia \& Tsang (2000): \ a squeezed rejection sampler, \ nearly always accepting", font_size=22,
                  color=GREY_A),
            label(r"betas from gammas: \ $G_1 / (G_1 + G_2)$ \ (Part 5's Dirichlet)", font_size=22, color=GREY_A),
        ), 12.6, 0.25, [0, -2.5, 0])
        with self.voiceover(
            "For the gamma, there's a rejection sampler so good it almost never rejects. <bookmark mark='a'/> George "
            "Marsaglia and Wai Wan Tsang published it in 2000: transform a normal draw by a cubic, then accept or "
            "reject with one logarithmic test. Six lines. <bookmark mark='b'/> With shape two and a half, it kept "
            "ninety-nine draws in a hundred, and the four thousand draws follow the gamma density. "
            "<bookmark mark='c'/> From gammas come betas, as a ratio, and Dirichlets, exactly as Part 5 showed. "
            "Most of the samplers inside NumPy and R are designs like these: one clever transformation per "
            "family."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(code, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(h), Create(cv), FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def alias(self):
        d = load("special")
        p, prob, alias = np.asarray(d["p"]), np.asarray(d["prob"]), np.asarray(d["alias"], int)
        n = len(p)
        w, H = 0.9, 3.0
        x0, y0 = -6.4, -2.4
        cols_ = VGroup()
        for i in range(n):
            x = x0 + i * (w + 0.15)
            lo = Rectangle(width=w, height=H * prob[i], stroke_width=1.5, stroke_color=BLACK, fill_color=COLS[i], fill_opacity=0.85)
            lo.move_to([x + w / 2, y0 + H * prob[i] / 2, 0])
            g = VGroup(lo, MathTex(str(i), font_size=24).next_to(lo, DOWN, buff=0.12).set_y(y0 - 0.25))
            if prob[i] < 1 - 1e-9:
                hi = Rectangle(width=w, height=H * (1 - prob[i]), stroke_width=1.5, stroke_color=BLACK, fill_color=COLS[alias[i]],
                               fill_opacity=0.85)
                hi.move_to([x + w / 2, y0 + H * prob[i] + H * (1 - prob[i]) / 2, 0])
                g.add(hi, MathTex(str(alias[i]), font_size=20).move_to(hi))
            cols_.add(g)
        top = DashedLine([x0 - 0.1, y0 + H, 0], [x0 + n * (w + 0.15), y0 + H, 0], color=GREY_C, stroke_width=1.5)
        pl = MathTex(r"p = (0.05,\ 0.30,\ 0.10,\ 0.25,\ 0.20,\ 0.10)", font_size=28).to_edge(UP, buff=0.5)
        rows = fit_rows(VGroup(
            label(r"each column holds $1/6$ of the mass, \ split between \emph{at most two} outcomes", font_size=24),
            label(r"draw: \ pick a column ($1$ uniform), \ keep it or take its alias ($1$ more)", font_size=24, color=GOOD),
            MathTex(r"\text{frequencies: }" + ",\\ ".join(f"{v:.3f}" for v in d["alias_freq"]), font_size=24, color=ACC),
            label(r"$O(1)$ per draw, \ whatever the number of outcomes: \ Walker (1974); \ Vose (1991)", font_size=22,
                  color=GREY_A),
        ), 6.0, 0.3, [3.7, 0.2, 0])
        with self.voiceover(
            "For discrete laws, inversion needs a search; the alias method needs none. <bookmark mark='a'/> Take six "
            "outcomes with these probabilities. Multiply each by six, so the average is one. "
            "<bookmark mark='b'/> Now rearrange the mass into six columns of equal height, so that each column "
            "contains at most two outcomes: its own, and one alias that tops it up. Outcome zero, which needs only "
            "a little, is filled up with mass from outcome one. <bookmark mark='c'/> To draw, pick a column "
            "uniformly, then a uniform height: below the split, take the column's own outcome; above it, the alias. "
            "Two uniforms, no search, for any number of outcomes. Alastair Walker invented it in 1974, and Michael "
            "Vose made the table-building fast in 1991. Thirty thousand draws reproduce the probabilities."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(pl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cols_], lag_ratio=0.2), Create(top), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:]))
        self.clear_scene()

    def cholesky(self):
        rows = [
            cmath(r"\mathbf X", r"=", r"\boldsymbol\mu + L\mathbf Z", r",\qquad", r"LL^\top = \Sigma", font_size=36),
            cmath(r"\mathrm{Cov}(\mathbf X)", r"=", r"L\, \mathrm{Cov}(\mathbf Z)\, L^\top", r"=", r"\Sigma", font_size=34),
        ]
        rows[0][2].set_color(GOOD)
        rows[1][4].set_color(EXACT)
        whys = [why(r"Part 4's Cholesky factor; \ $\mathbf Z$ from Box--Muller"), why(r"Part 5's affine rule")]
        recipe = fit_rows(VGroup(
            label(r"uniforms $\to$ normals $\to$ correlated normals $\to$ \ (Part 5's copulas) \ any margins", font_size=26,
                  color=S.ACCENT),
            label(r"every random variable in this series is a function of PCG's uniforms", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "And for many variables at once, Part 4 and Part 5 already did the work. <bookmark mark='a'/> Draw a "
            "vector of independent normals with Box and Muller, and multiply by the Cholesky factor of the "
            "covariance you want, then add the mean. <bookmark mark='b'/> By Part 5's affine rule its covariance is "
            "exactly Sigma. <bookmark mark='c'/> Uniforms become normals, normals become correlated normals, and "
            "Part 5's copulas turn those into any margins we like. Every random quantity in this series, every "
            "World, every simulated study, is a function of a stream of uniforms."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=1.0, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(recipe))
        self.clear_scene()
