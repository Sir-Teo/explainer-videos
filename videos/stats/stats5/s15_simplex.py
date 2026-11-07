from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403

NAMES = {"flat": r"$\boldsymbol\alpha = (1, 1, 1)$", "centre": r"$(8, 8, 8)$", "corner": r"$(0.3, 0.3, 0.3)$", "skew": r"$(6, 2, 1)$"}


def tri_points(c, s):
    return [np.array(c) + s * np.array(v) for v in ((-1, -0.577, 0), (1, -0.577, 0), (0, 1.155, 0))]


def to_xy(p, corners):
    return p[0] * corners[0] + p[1] * corners[1] + p[2] * corners[2]


class Simplex(VoiceoverScene):
    def construct(self):
        self.card()
        self.multinomial()
        self.dirichlet()
        self.gammas()
        self.conjugate()
        self.spurious()

    def card(self):
        card = chapter_card(14, r"The simplex", r"Distributions over proportions", lit=(), part=PART)
        with self.voiceover("Chapter fourteen. The simplex."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def multinomial(self):
        rows = [
            cmath(r"P(N_1 = n_1, \dots, N_k = n_k)", r"=", r"\frac{n!}{n_1! \cdots n_k!}\, p_1^{n_1} \cdots p_k^{n_k}", font_size=34),
            cmath(r"\mathrm{Cov}(N_i, N_j)", r"=", r"-n\, p_i p_j", r"\quad (i \ne j)", font_size=34),
        ]
        rows[1][2].set_color(S.RESID)
        whys = [why(r"Part 2's multinomial coefficient: \ $n$ draws into $k$ categories"),
                why(r"the counts compete: \ they must add to $n$")]
        ex = label(r"votes for $k$ parties, \ blood types, \ the regions of a sample from the World", font_size=24, color=GREY_A)
        ex.to_edge(DOWN, buff=0.8)
        intro = label('Counts that add to a fixed total', font_size=36)
        with self.voiceover(
            "Many variables are proportions that must add up to one: the shares of a vote, the frequencies of blood "
            "groups. <bookmark mark='a'/> Counts in k categories from n independent draws follow the multinomial "
            "distribution, Part 2's multinomial coefficient times the probabilities. <bookmark mark='b'/> Its counts "
            "are negatively correlated, since they must add up to n: more of one leaves fewer for the others."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.0, x=-0.6, buff=0.8, edge=6.9)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            self.play(FadeIn(ex))
        self.clear_scene()

    def dirichlet(self):
        d = load("simplex")
        panels = VGroup()
        for k, key in enumerate(("flat", "centre", "corner", "skew")):
            c = np.array([-4.8 + 3.2 * k, -0.4, 0])
            corners = tri_points(c, 1.35)
            tri = Polygon(*corners, stroke_color=GREY_B, stroke_width=2)
            p = np.asarray(d[key]["p"])
            dots = VGroup(*[Dot(to_xy(q, corners), radius=0.014, color=S.PRIOR, fill_opacity=0.6) for q in p[:900]])
            t = label(NAMES[key], font_size=22, color=S.PRIOR).next_to(tri, DOWN, buff=0.25)
            panels.add(VGroup(tri, dots, t))
        f = MathTex(r"f(p_1, \dots, p_k)", r"\propto", r"p_1^{\alpha_1 - 1} \cdots p_k^{\alpha_k - 1}", r",\qquad \textstyle\sum p_i = 1",
                    font_size=32).to_edge(UP, buff=0.5)
        f[2].set_color(S.PRIOR)
        sub = label(r"each point: \ a vector of three proportions; \ corners: \ all in one category", font_size=22, color=GREY_B)
        sub.next_to(f, DOWN, buff=0.15)
        mean = label(r"$E\,p_i = \alpha_i / \sum_j \alpha_j$; \ fixed mean, larger $\sum\alpha$: more concentrated", font_size=24, color=GREY_A)
        mean.to_edge(DOWN, buff=0.4)
        tag = note(r"simulated: 900 of 1,500 draws shown").to_corner(UR, buff=0.25)
        with self.voiceover(
            "To model the proportions themselves as uncertain, we need a distribution on the simplex: the triangle "
            "of all vectors of proportions adding to one. <bookmark mark='a'/> The Dirichlet distribution, named "
            "for Peter Gustav Lejeune Dirichlet, has density proportional to each proportion raised to a power alpha "
            "minus one. It's the beta distribution in more dimensions. <bookmark mark='b'/> With all alphas one, it's "
            "uniform on the triangle. <bookmark mark='c'/> With large equal alphas, it concentrates in the middle. "
            "<bookmark mark='d'/> With alphas below one, it pushes mass into the corners: most draws put nearly "
            "everything in one category. <bookmark mark='e'/> And unequal alphas pull it toward one corner, with "
            "mean alpha i over the sum of the alphas."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(sub))
            for k, m in enumerate("bcde"):
                vo.wait_until(m)
                self.play(Create(panels[k][0]), FadeIn(panels[k][1], lag_ratio=0.002), FadeIn(panels[k][2]))
            self.play(FadeIn(mean))
        self.clear_scene()

    def conjugate(self):
        rows = [
            cmath(r"\mathbf p", r"\sim", r"\mathrm{Dirichlet}(\boldsymbol\alpha)", font_size=36),
            cmath(r"\mathbf N \mid \mathbf p", r"\sim", r"\mathrm{Multinomial}(n, \mathbf p)", font_size=36),
            cmath(r"\mathbf p \mid \mathbf N", r"\sim", r"\mathrm{Dirichlet}(\boldsymbol\alpha + \mathbf N)", font_size=38),
        ]
        rows[2][2].set_color(S.POST)
        whys = [why(r"a prior over proportions"), why(r"counts, given the proportions"),
                why(r"add the counts to the $\alpha$'s: \ conjugacy (Part 15)")]
        link = label(r"P\'olya's urn with $k$ colours is this update, \ one ball at a time", font_size=26, color=S.ACCENT)
        link.to_edge(DOWN, buff=0.7)
        intro = label('Updating uncertain proportions', font_size=36)
        with self.voiceover(
            "The Dirichlet and the multinomial fit together perfectly. <bookmark mark='a'/> Choose proportions from a "
            "Dirichlet. <bookmark mark='b'/> Draw counts from a multinomial with those proportions. "
            "<bookmark mark='c'/> Then, given the counts, the proportions are Dirichlet again, with the counts simply "
            "added to the alphas. That's called conjugacy, and Part 15 builds Bayesian inference on it. "
            "<bookmark mark='d'/> And it's Pólya's urn again: the urn with k colours adds one ball of the drawn colour "
            "each time, which is exactly this update, one observation at a time."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=0.65, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(link))
        self.clear_scene()

    def spurious(self):
        e = load("extras")["spurious"]
        x, y = np.asarray(e["x"]), np.asarray(e["y"])
        A = axes([0.4, 2.0], [0.4, 2.0], x_length=4.6, y_length=4.6, xlabel=r"$X/Z$", ylabel=r"$Y/Z$", xticks=[0.5, 1, 1.5],
                 yticks=[0.5, 1, 1.5], center=[-3.6, -0.4, 0])
        pts = scatter(A.ax, x, y, color=SIM, radius=0.02, opacity=0.5)
        hc = history_card(1897, r"Karl Pearson, \ ``On a form of spurious correlation''", r"which may arise when indices are "
                          r"used in the measurement of organs", color=S.MUSEUM, width=6.2, font_size=22).move_to([3.0, 2.0, 0])
        rows = VGroup(MathTex(rf"X, Y, Z \text{{ independent:}}\ \operatorname{{corr}}(X, Y) = {e['r_raw']:.3f}", font_size=28),
                      MathTex(rf"\operatorname{{corr}}(X/Z,\ Y/Z) = {e['r_ratio']:.3f}", font_size=30, color=S.RESID),
                      VGroup(label(r"shares of a whole and per-capita rates", font_size=24, color=GREY_A),
                             label(r"inherit correlation from the shared denominator", font_size=24, color=GREY_A)
                             ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                      label(r"for positive compositions: \ log-ratios (Aitchison 1982)", font_size=22, color=S.ACCENT))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.0, -0.8, 0])
        for r in rows:
            if r.width > 6.4:
                r.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.0, -0.8, 0])  # re-align after clamping
        tag = note(r"simulated: positive lognormal triples; 1,200 of 5,000 shown, off-panel points omitted").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Proportions carry a trap that Karl Pearson spotted in 1897. <bookmark mark='a'/> Take three independent positive lognormal "
            "variables, X, Y and Z. X and Y are uncorrelated. <bookmark mark='b'/> Now divide both by Z, as you do when "
            "you form shares or per-capita rates. The ratios are strongly correlated, about point five, purely "
            "because they share a denominator. <bookmark mark='c'/> Pearson called it spurious correlation, and it "
            "haunts anything measured as a share of a whole. For genuine compositions, John Aitchison's log-ratios "
            "from 1982 are a useful framework for relative information, not a universal fix."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(pts, lag_ratio=0.001), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def gammas(self):
        rows = [
            cmath(r"G_i \sim \mathrm{Gamma}(\alpha_i, 1)", r",\quad", r"\text{independent}", font_size=32),
            cmath(r"(p_1, \dots, p_k)", r"=", r"\Big(\frac{G_1}{T}, \dots, \frac{G_k}{T}\Big)", r",\quad", r"T = \textstyle\sum_i G_i",
                  font_size=32),
            cmath(r"f(\mathbf p, t)", r"=", r"\prod_i \frac{(p_i t)^{\alpha_i - 1} e^{-p_i t}}{\Gamma(\alpha_i)} \cdot t^{k - 1}",
                  font_size=32),
            cmath(r"f(\mathbf p, t)", r"=", r"\underbrace{\frac{\Gamma(\sum\alpha)}{\prod\Gamma(\alpha_i)}\prod_i p_i^{\alpha_i - 1}}"
                  r"_{\mathrm{Dirichlet}(\boldsymbol\alpha)}", r"\cdot", r"\underbrace{\frac{t^{\sum\alpha - 1} e^{-t}}{\Gamma(\sum\alpha)}}"
                  r"_{\mathrm{Gamma}(\sum\alpha)}", font_size=30),
        ]
        rows[3][2].set_color(S.PRIOR)
        rows[3][4].set_color(S.ACCENT)
        whys = [why(r"Part 3's gamma: \ waiting times"), why(r"normalize by the total"),
                why(r"change of variables: \ the Jacobian is $t^{k - 1}$"), why(r"it factors: \ the proportions are independent of the total")]
        take = label(r"how computers draw a Dirichlet; \ and the total tells you nothing about the shares (Lukacs 1955)", font_size=24,
                     color=S.ACCENT).to_edge(DOWN, buff=0.45)
        intro = label('Independent gammas, normalized', font_size=36)
        with self.voiceover(
            "Where does the Dirichlet come from? There's a construction that's also how computers draw from it. "
            "<bookmark mark='a'/> Take k independent gamma variables, with positive shape parameters alpha one through alpha k and a common scale, here one. "
            "<bookmark mark='b'/> Divide each by their total. <bookmark mark='c'/> Change variables from the k gammas "
            "to the k minus one free proportions and the total. The absolute Jacobian determinant of the inverse map, from proportions and total back to gammas, is t to the k minus one, "
            "chapter nine's machinery again. <bookmark mark='d'/> And the joint density factors: a Dirichlet in the "
            "proportions times a gamma in the total. So the proportions are exactly Dirichlet, and they're "
            "independent of the total, a fact Eugene Lukacs showed in 1955 characterizes the gamma. That independence holds for this gamma construction; it is not a universal fact about vote totals and shares. With k equal to two this is the beta, as a "
            "ratio of gammas."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.55, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            self.play(FadeIn(take))
        self.clear_scene()
