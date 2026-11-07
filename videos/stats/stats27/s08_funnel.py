from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats27.common import *  # noqa: F403


class Funnel(VoiceoverScene):
    def construct(self):
        self.card()
        self.shape()
        self.neal()
        self.schools_centred()
        self.noncentred()
        self.table()
        self.other()
        self.lessons()

    def card(self):
        card = chapter_card(7, r"Neal's funnel", r"The eight schools' hidden geometry", lit=(2003,), part=PART)
        with self.voiceover("Chapter seven. Neal's funnel and the eight schools."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def shape(self):
        rows = [
            cmath(r"v", r"\sim", r"N(0, 3^2)", font_size=32),
            cmath(r"x_i \mid v", r"\sim", r"N(0, e^{v}), \ \ i = 1, \dots, 9", font_size=32),
            cmath(r"v \text{ small}", r":", r"x \text{ squeezed into a tiny neck}", font_size=30),
            cmath(r"\text{one step size}", r":", r"\text{too big for the neck, \ too small for the mouth}", font_size=30),
        ]
        rows[3][2].set_color(DIV)
        whys = [why(r"a log scale"), why(r"Neal (2003)"), why(r"curvature varies by orders of magnitude"),
                why(r"the sampler cannot enter the neck")]
        with self.voiceover(
            "<bookmark mark='a'/> Radford Neal's funnel is the hierarchical model's geometry, distilled. A scale parameter v "
            "is normal, <bookmark mark='b'/> and nine further parameters are normal with standard deviation e to the v over "
            "two. <bookmark mark='c'/> When v is very negative, the x's are squeezed into a tiny neck; when it is large, they "
            "spread across a wide mouth. <bookmark mark='d'/> No single step size suits both, and the curvature in the neck is "
            "so extreme that HMC's trajectories diverge before they can enter it."
        ) as vo:
            intro = label('A hierarchy can have strongly changing local curvature', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def neal(self):
        d = load("funnel")["funnel"]
        vc, xc, vn, xn = (np.asarray(d[k]) for k in ("vc", "xc", "vn", "xn"))
        g = []
        for k, (v, x, name, col) in enumerate(((vc, xc, r"centred: \ sample $(v, x)$", RES), (vn, xn, r"non-centred: \ $x = e^{v/2} z$", HIT))):
            A = axes([-20, 20], [-10, 9], x_length=4.6, y_length=4.4, xlabel=r"$x_1$", ylabel=r"$v$", xticks=[-15, 0, 15],
                     yticks=[-8, -4, 0, 4, 8], center=[-3.4 + 6.4 * k, 0.4, 0])
            vv = np.linspace(-10, 9, 200)
            edge = VGroup(curve(A.ax, 2 * np.exp(vv / 2), vv, GREY_C, 1.5),
                          curve(A.ax, -2 * np.exp(vv / 2), vv, GREY_C, 1.5))
            m = (np.abs(x) < 20) & (v > -10) & (v < 9)
            pts = scatter_pts(A.ax, x[m][::2], v[m][::2], col, 0.025, 0.6)
            nm = label(name, font_size=22, color=col).next_to(A, DOWN, buff=0.25)
            g.append((A, edge, pts, nm))
        rows = fit_rows(VGroup(
            label(rf"centred: \ 5\% point of $v$ \ {d['q05_c']:.2f}; \ truth {d['q05_true']:.2f}", font_size=22, color=RES),
            label(rf"non-centred: \ {d['q05_n']:.2f}", font_size=22, color=HIT),
        ), 12.0, 0.2, [0, -3.15, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two thousand NUTS draws of v against the first x. The grey lines mark two standard "
            "deviations of x at each height. <bookmark mark='b'/> Sampling v and x directly, the centred form, the "
            "draws stop at v of about minus two: the neck, below, is never visited. The true five percent point of v "
            "is minus four point nine; the sampler's is minus two point one, a badly biased answer with only one "
            "divergence to warn of it. <bookmark mark='c'/> Now sample v and standard normals z instead, and set x to"
            " e to the v over two times z: the non-centred form. Now the coordinates are independent normals, with "
            "v's different scale handled by adaptation, and the draws fill the whole funnel, neck included."
        ) as vo:
            self.add(seeded_tag())
            A0, e0, p0, n0 = g[0]
            A1, e1, p1, n1 = g[1]
            self.play(FadeIn(A0), FadeIn(A1), Create(e0), Create(e1))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in p0], lag_ratio=0.001), FadeIn(n0), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in p1], lag_ratio=0.001), FadeIn(n1), FadeIn(rows[1]), run_time=2.0)
        self.clear_scene()

    def schools_centred(self):
        d = load("funnel")
        sc = d["schools"]["centred"]
        lt, dens = np.asarray(d["lt"]), np.asarray(d["dens_lt"])
        edges = np.linspace(-6, 4, 51)
        h, _ = np.histogram(np.asarray(sc["logtau"]), edges)
        h=h/len(sc["logtau"])/np.diff(edges)
        ymax = float(max(h.max(), dens.max())) * 1.1
        A = axes([-6, 4], [0, ymax], x_length=7.2, y_length=4.2, xlabel=r"$\log\tau$", ylabel=r"density", xticks=[-6, -4, -2, 0, 2, 4],
                 yticks=[], center=[-2.0, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, h, color=RES, opacity=0.5)
        ex = curve(ax, lt, dens, EXACTC, 3.5)
        divs = VGroup(*[Line(ax.c2p(v, 0), ax.c2p(v, ymax * 0.06), color=DIV, stroke_width=2.5) for v in sc["div_logtau"]])
        rows = fit_rows(VGroup(
            label(r"$\theta_j \sim N(\mu, \tau^2)$, \ sampled directly: \ centred", font_size=22),
            label(r"gold: \ numerical reference; \ proper $N(0,25)$ and half-Cauchy(5) priors", font_size=22, color=EXACTC),
            label(rf"red: \ NUTS, \ 4 chains; \ {sc['divergent']} divergences", font_size=22, color=RES),
            label(r"ticks: \ where they happened: \ small $\tau$", font_size=22, color=DIV),
            label(rf"5\% point of $\tau$: \ {sc['q05']:.2f} vs exact {d['exact']['q05']:.2f}", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The eight schools are a funnel: log tau controls the width, and the eight effects "
            "play x. Sampled directly, as Part 26 wrote the model, <bookmark mark='b'/> against a numerical-grid "
            "reference, using a normal prior with SD five on mu and a half-Cauchy prior with scale five on tau. These"
            " are proper priors, different from Part 26's opening flat-prior fit, <bookmark mark='c'/> NUTS gives "
            "forty-seven divergences in four thousand iterations, <bookmark mark='d'/> all at small tau, where the "
            "neck is. <bookmark mark='e'/> The histogram misses the left tail: the five percent point of tau is point"
            " nine instead of about point two five. R-hat is one point oh five and the effective sample size sixty: "
            "the diagnostics are worried, and right to be."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ex), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(x) for x in divs], lag_ratio=0.02), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def noncentred(self):
        d = load("funnel")
        sc = d["schools"]["noncentred"]
        lt, dens = np.asarray(d["lt"]), np.asarray(d["dens_lt"])
        edges = np.linspace(-6, 4, 51)
        h, _ = np.histogram(np.asarray(sc["logtau"]), edges)
        h=h/len(sc["logtau"])/np.diff(edges)
        ymax = float(max(h.max(), dens.max())) * 1.1
        A = axes([-6, 4], [0, ymax], x_length=7.2, y_length=4.2, xlabel=r"$\log\tau$", ylabel=r"density", xticks=[-6, -4, -2, 0, 2, 4],
                 yticks=[], center=[-2.0, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, h, color=HIT, opacity=0.5)
        ex = curve(ax, lt, dens, EXACTC, 3.5)
        rows = fit_rows(VGroup(
            label(r"$\theta_j = \mu + \tau z_j$, \ $z_j \sim N(0, 1)$: \ non-centred", font_size=22),
            label(r"the same model, \ a different coordinate system", font_size=22, color=GREY_A),
            label(rf"{sc['divergent']} divergences; \ $\hat R = {sc['rhat']:.3f}$; \ ESS {sc['ess']:,.0f}", font_size=22, color=HIT),
            label(rf"5\% point {sc['q05']:.2f}, \ median {sc['median']:.2f}: \ exact {d['exact']['q05']:.2f}, \ {d['exact']['median']:.2f}", font_size=22, color=HIT),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now write each effect as mu plus tau times a standard normal z, and sample the z's."
            " <bookmark mark='b'/> It is the same model: only the coordinates the sampler moves in have changed. "
            "<bookmark mark='c'/> No divergences, R-hat of one point oh oh three, and an effective sample size of "
            "nineteen hundred. <bookmark mark='d'/> The histogram lies on the exact curve: five percent point point "
            "two five, median two point six nine, against the grid's about point two five and two point seven five."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A), Create(ex))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def table(self):
        d = load("funnel")
        s = d["schools"]
        hdr = [r"\textbf{eight schools}", r"\textbf{divergences}", r"\textbf{$\hat R$}", r"\textbf{ESS}", r"\textbf{5\% point of $\tau$}", r"\textbf{gradients}"]
        body = []
        for k, name in (("centred", r"centred, \ $\delta = 0.8$"), ("centred99", r"centred, \ $\delta = 0.99$"), ("noncentred", r"non-centred")):
            v = s[k]
            body.append([name, f"{v['divergent']}", f"{v['rhat']:.3f}", f"{v['ess']:,.0f}", f"{v['q05']:.2f}", f"{v['n_grad']:,}"])
        body.append([r"numerical grid", r"", r"", r"", f"{d['exact']['q05']:.2f}", r""])
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.55, row_buff=0.3, colors=[GREY_A, RES, PATH, HIT, EXACTC])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"$\delta=0.99$: \ fewer divergences, \ about 3.2 times the original gradients; \ tail still inaccurate", font_size=22, color=PATH),
            label(r"non-centring improves exploration in this weak-data example", font_size=22, color=HIT),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A tempting response to divergences is to force a smaller step size by raising the "
            "target acceptance rate. <bookmark mark='b'/> At point nine nine the divergences fall from forty-seven to"
            " four, the run costs about three point two times the original gradients, and the five percent point of "
            "tau is still point five five, not about point two five: the problem is hidden, not solved. <bookmark "
            "mark='c'/> The non-centred run agrees closely with the reference at about half the original gradient "
            "count. Reparametrization helps this weak-data example more than just increasing effort."
        ) as vo:
            self.add(schools_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]), FadeIn(tb[4]))
            vo.wait_until("b")
            self.play(FadeIn(tb[2]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(tb[3]), FadeIn(foot[1]))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"weak data (few groups, \ big $\sigma_j$): \ non-centre", font_size=24, color=HIT),
            label(r"strong data (big groups): \ centring is better: \ the funnel flips", font_size=24, color=PATH),
            label(r"Papaspiliopoulos, Roberts \& Sk\"old (2007): \ which to use depends on the data", font_size=24),
            label(r"divergences are information about your model's geometry", font_size=24, color=DIV),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Which form to use depends on the data. When groups carry little information, as here, "
            "non-centre. <bookmark mark='b'/> When each group has lots of data, the likelihood pins each effect down and the "
            "centred form is better; the funnel appears in the other coordinates instead. <bookmark mark='c'/> Omiros "
            "Papaspiliopoulos, Gareth Roberts and Martin Sköld worked out the theory. <bookmark mark='d'/> Either way, a "
            "divergence is information about your model's geometry, not noise to be suppressed."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def other(self):
        rows = [
            cmath(r"\text{regression}", r":", r"X = QR: \ \text{sample } \tilde\beta = R\beta", font_size=30),
            cmath(r"\text{scales}", r":", r"\text{standardize predictors; \ put priors on unit scales}", font_size=28),
            cmath(r"\text{positive}", r":", r"\text{log scale: \ already done by the transform}", font_size=30),
            cmath(r"\text{principle}", r":", r"\text{make the posterior look like } N(0, I)", font_size=30),
        ]
        rows[3][-1].set_color(HIT)
        whys = [why(r"orthogonal coordinates"), why(r"chapter six's mass matrix helps less if scales vary wildly"), why(r"chapter eight"), why(r"what every trick shares")]
        with self.voiceover(
            "<bookmark mark='a'/> Non-centring is one of a family of reparametrizations. In regression, factor the design "
            "matrix as Q times R and sample the rotated coefficients, which are nearly uncorrelated. <bookmark mark='b'/> "
            "Standardize predictors, so that parameters live on similar scales. <bookmark mark='c'/> Sample positive "
            "quantities on the log scale, which the transforms already do. <bookmark mark='d'/> The common principle is to "
            "find coordinates in which the posterior looks like a standard normal, the shape HMC handles best."
        ) as vo:
            intro = label('Coordinate changes must preserve the intended prior', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
