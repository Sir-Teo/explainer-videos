from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class Bandwidth(VoiceoverScene):
    def construct(self):
        self.card()
        self.reference()
        self.lscv_idea()
        self.lscv_curve()
        self.plugin()
        self.faithful_four()
        self.race()
        self.advice()

    def card(self):
        card = chapter_card(3, r"Choosing the bandwidth", r"From the data, \ without knowing $f''$", lit=(1991,), part=PART)
        with self.voiceover("Chapter three. Choosing the bandwidth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def reference(self):
        rows = [
            cmath(r"h^*", r"=", r"\bigl(R(K) / (\mu_2^2 R(f'') n)\bigr)^{1/5}", font_size=30),
            cmath(r"f = N(\mu, \sigma^2)", r":", r"R(f'') = \tfrac{3}{8\sqrt\pi \sigma^5}: \ \ h = 1.06\, \hat\sigma\, n^{-1/5}", font_size=28),
            cmath(r"\text{Silverman}", r":", r"h = 0.9 \min(\hat\sigma, \mathrm{IQR}/1.34)\, n^{-1/5}", font_size=28),
            cmath(r"\text{two humps}", r":", r"\hat\sigma \text{ is inflated by the gap: \ oversmooths}", font_size=28),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"depends on the unknown curvature"), why(r"pretend $f$ is normal"),
                why(r"Silverman (1986): \ a robust compromise"), why(r"Part 16 used this rule")]
        with self.voiceover(
            "<bookmark mark='a'/> The best bandwidth depends on the unknown curvature of f, the very thing we're estimating. "
            "<bookmark mark='b'/> The simplest escape: pretend f is normal. Then R of f double prime is known, and h is one "
            "point oh six sigma n to the minus a fifth. <bookmark mark='c'/> Silverman's rule of thumb, Part 16's choice, "
            "shrinks the constant and uses a robust spread. <bookmark mark='d'/> Both work for unimodal densities. For two "
            "humps the standard deviation is inflated by the gap between them, and both rules oversmooth."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lscv_idea(self):
        rows = [
            cmath(r"\text{ISE}(h)", r"=", r"\textstyle\int \hat f_h^2 - 2 \int \hat f_h f + \int f^2", font_size=30),
            cmath(r"\textstyle\int \hat f_h f", r"=", r"E_X \hat f_h(X) \approx \tfrac1n \textstyle\sum_i \hat f_{h,-i}(x_i)", font_size=30),
            cmath(r"\text{LSCV}(h)", r"=", r"\textstyle\int \hat f_h^2 - \tfrac2n \sum_i \hat f_{h,-i}(x_i)", font_size=30),
            cmath(r"\text{normal kernel}", r":", r"\text{both terms in closed form}", font_size=30),
        ]
        rows[2][2].set_color(KDEC)
        whys = [why(r"the last term doesn't depend on $h$"), why(r"leave $x_i$ out so it can't predict itself"),
                why(r"Rudemo (1982); \ Bowman (1984)"), why(r"sums of normal densities at the pairwise gaps")]
        with self.voiceover(
            "<bookmark mark='a'/> Cross-validation instead. Expand the integrated squared error: the last term doesn't depend "
            "on h, the first is computable, and the middle one involves the unknown f. <bookmark mark='b'/> But the middle "
            "term is an expectation over a new observation, which leave-one-out estimates. <bookmark mark='c'/> So the "
            "least-squares cross-validation criterion of Mats Rudemo and Adrian Bowman estimates ISE up to a constant. "
            "<bookmark mark='d'/> With normal kernels both terms are sums of normal densities at the pairwise gaps."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lscv_curve(self):
        d = load("faithful")
        lh = np.log10(np.asarray(d["lscv_h"]))
        lv = np.asarray(d["lscv"])
        A = axes([-1.4, 0.0], [float(lv.min()) - 0.02, float(lv.min()) + 0.25], x_length=7.4, y_length=4.4,
                 xlabel=r"bandwidth $h$ \ (log scale)", ylabel=r"LSCV$(h)$", xticks=[-1.3, -1, -0.5, 0], yticks=[],
                 xfmt=lambda v: f"{10 ** v:.2g}", center=[-2.0, 0.3, 0])
        ax = A.ax
        keep = lv < lv.min() + 0.25
        c = polyline(ax, lh[keep], lv[keep], KDEC, 3)
        hb = d["h"]["lscv"]
        dot = Dot(ax.c2p(np.log10(hb), lv.min()), radius=0.08, color=PATH)
        rows = fit_rows(VGroup(
            label(r"Old Faithful's 272 eruptions", font_size=22),
            label(rf"minimum at $h = {hb:.3f}$", font_size=22, color=PATH),
            label(rf"its estimate has {d['modes']['lscv']} modes", font_size=22, color=RES),
            label(r"a shallow, \ wiggly criterion", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On Old Faithful the criterion falls steeply from tiny bandwidths, <bookmark mark='b'/> "
            "reaches its minimum at h of point one oh, <bookmark mark='c'/> where the estimate has three modes, "
            "<bookmark mark='d'/> and rises slowly. The minimum is shallow, so small changes in the data move it a lot: "
            "cross-validation is nearly unbiased for the best bandwidth, but highly variable."
        ) as vo:
            self.add(faithful_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dot), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def plugin(self):
        rows = [
            cmath(r"R(f'')", r"=", r"\textstyle\int f^{(4)} f = \psi_4", font_size=30),
            cmath(r"\hat\psi_r(g)", r"=", r"\tfrac{1}{n^2} \textstyle\sum_{i,j} \phi_g^{(r)}(x_i - x_j)", font_size=30),
            cmath(r"\text{pilot } g", r":", r"\text{its own optimum needs } \psi_6, \ \text{then } \psi_8 \text{ (normal)}", font_size=28),
            cmath(r"h_{\mathrm{SJ}}", r"=", r"\bigl(R(K) / (\hat\psi_4 n)\bigr)^{1/5}", font_size=32),
        ]
        rows[3][2].set_color(KDEC)
        whys = [why(r"integrate by parts twice"), why(r"estimate the functional with a kernel"),
                why(r"two stages, \ then a normal reference"), why(r"Sheather \& Jones (1991)")]
        with self.voiceover(
            "<bookmark mark='a'/> The other strategy plugs in an estimate of the unknown curvature. Integrating by parts "
            "twice, R of f double prime is the integral of f's fourth derivative times f, called psi four. "
            "<bookmark mark='b'/> That can itself be estimated by a kernel sum over all pairs, with its own pilot bandwidth "
            "g. <bookmark mark='c'/> The best pilot depends on psi six, whose pilot depends on psi eight, where a normal "
            "reference finally stops the regress. <bookmark mark='d'/> Simon Sheather and Chris Jones's plug-in bandwidth "
            "puts the estimate into the formula."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def faithful_four(self):
        d = load("faithful")
        g = np.asarray(d["grid"])
        A = axes([1, 6], [0, 0.9], x_length=7.4, y_length=4.4, xlabel=r"eruption length (minutes)", ylabel=r"density",
                 xticks=[2, 3, 4, 5], yticks=[0, 0.4, 0.8], center=[-2.0, 0.3, 0])
        ax = A.ax
        spec = (("nr", r"normal reference", GREY_B), ("silverman", r"Silverman", HISTC), ("sj", r"Sheather--Jones", KDEC),
                ("lscv", r"LSCV", NWC))
        cs = {k: clip_curve(ax, g, np.asarray(d["kde"][k]), c, 3, ymin=0, ymax=0.9) for k, _, c in spec}
        rows = fit_rows(VGroup(*[label(rf"{t}: \ $h = {d['h'][k]:.3f}$, \ {d['modes'][k]} modes", font_size=22, color=c)
                                 for k, t, c in spec]), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The four choices on Old Faithful. The normal reference, h of point three nine, blurs the "
            "short eruptions into a low mound. <bookmark mark='b'/> Silverman's point three three, a little sharper. "
            "<bookmark mark='c'/> Sheather–Jones, point one seven: two crisp humps. <bookmark mark='d'/> Cross-validation, "
            "point one oh: three. Silverman's test of chapter zero sides with the plug-in."
        ) as vo:
            self.add(faithful_tag())
            self.play(FadeIn(A), FadeIn(rug(ax, d["x"])))
            for k, ((key, _, _), m_) in enumerate(zip(spec, "abcd")):
                vo.wait_until(m_)
                self.play(Create(cs[key]), FadeIn(rows[k]))
        self.clear_scene()

    def race(self):
        d = load("selectors")
        s = d["summary"]
        hdr = [r"\textbf{selector}", r"\textbf{$\hat h / h_{\mathrm{MISE}}$: \ median}", r"\textbf{10\%--90\%}", r"\textbf{mean ISE}"]
        spec = (("nr", r"normal reference"), ("silverman", r"Silverman"), ("lscv", r"LSCV"), ("sj", r"Sheather--Jones"))
        body = [[t, f"{s[k]['median']:.2f}", f"{s[k]['q10']:.2f}--{s[k]['q90']:.2f}", f"{s[k]['mean_ise']:.4f}"] for k, t in spec]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.3, colors=[GREY_A, GREY_B, HISTC, NWC, KDEC])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"{d['R']} samples of $n = {d['n']}$ from the two-humped stand-in; \ best possible MISE {d['mise_opt']:.4f}", font_size=22),
            label(r"LSCV: \ right on average, \ widely scattered; \ \ SJ: \ a little large, \ tightly", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A race: three hundred samples of two hundred from the two-humped density, each bandwidth "
            "measured against the one minimizing the true MISE. <bookmark mark='b'/> The normal reference bandwidth is "
            "almost three times too wide, Silverman's two and a third: they never see the two humps, and their errors are "
            "four and five times the best possible. <bookmark mark='c'/> Cross-validation is right on average, but its "
            "middle eighty percent runs from point seven two to one point two. <bookmark mark='d'/> Sheather–Jones is a "
            "fifth too wide, but consistently, and has the lowest average error, which is why it is many statisticians' "
            "default. Steve Marron and colleagues ran this race at scale in the 1990s, with the same verdict."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[1]), FadeIn(tb[2]))
            vo.wait_until("c")
            self.play(FadeIn(tb[3]))
            vo.wait_until("d")
            self.play(FadeIn(tb[4]), FadeIn(foot[1]))
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"look at several bandwidths: \ structure that survives is real", font_size=24),
            label(r"default: \ a plug-in (Sheather--Jones); \ check with CV", font_size=24, color=KDEC),
            label(r"rules of thumb oversmooth anything far from normal", font_size=24, color=RES),
            label(r"Chaudhuri \& Marron's SiZer: \ every bandwidth at once, \ with significance", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In practice, look at several bandwidths; structure that persists across a range is "
            "probably real. <bookmark mark='b'/> A plug-in is a good default, cross-validation a useful check. "
            "<bookmark mark='c'/> Rules of thumb oversmooth anything that isn't roughly normal. <bookmark mark='d'/> And "
            "Probal Chaudhuri and Steve Marron's SiZer map turned the advice into a method: at every bandwidth and location, "
            "is the estimated slope significantly up or down?"
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
