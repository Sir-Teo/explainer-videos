from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403


class Correct(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Publication bias, \ corrected", r"If a literature is selected, \ can we recover what it "
             r"would have said without selection?", "Chapter five. Publication bias, corrected.",
             lit={2019: "Andrews and Kasy"}, scale=("world",), horizon=("a decade",))
        self.model()
        self.funnel()
        self.literatures()

    def model(self):
        ax = plane([-4, 4], [0, 1.15], center=LEFT * 2.2 + DOWN * 0.2, x_length=7.2, y_length=3.8,
                   xticks=[-4, -1.96, 0, 1.96, 4], yticks=[0, 0.5, 1.0],
                   xlabel=r"the study's $z$", ylabel=r"chance of publication \ (relative)",
                   xfmt=lambda v: f"{v:.2f}".replace("-", "{-}") if abs(abs(v) - 1.96) < 1e-9 else f"{v:.0f}".replace(
                       "-", "{-}"), yfmt=lambda v: f"{v:.1f}", font_size=14)
        beta = 0.3
        step = VMobject(stroke_color=PUB, stroke_width=4)
        step.set_points_as_corners([ax.ax.c2p(-4, 1), ax.ax.c2p(-1.96, 1), ax.ax.c2p(-1.96, beta),
                                    ax.ax.c2p(1.96, beta), ax.ax.c2p(1.96, 1), ax.ax.c2p(4, 1)])
        bl = label(r"$\beta$", font_size=26, color=PUB).next_to(ax.ax.c2p(0, beta), UP, buff=0.1)
        eqs = VGroup(
            MathTex(r"f_{\text{published}}(z) \;\propto\; p(z)\, f_{\text{latent}}(z)", font_size=34),
            MathTex(r"p(z) = \begin{cases} 1 & |z| \ge 1.96 \\ \beta & |z| < 1.96 \end{cases}", font_size=32,
                    color=PUB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        rows = VGroup(
            label(r"identified from replications: \\ the originals against their repeats", font_size=18,
                  color=TRUE),
            label(r"or from a meta-study: \\ precise studies against imprecise ones", font_size=18, color=FIRST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(eqs, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(ax.ax, RIGHT, buff=0.6)
        if rows.get_right()[0] > 6.9 or eqs.get_right()[0] > 6.9:
            VGroup(eqs, rows).scale_to_fit_width(6.9 - eqs.get_left()[0])
        tag = published_tag(r"Andrews and Kasy, \ \emph{AER} 109(8) (2019)", corner=DL, font_size=12)
        with self.voiceover(
            "If selection bends a literature, model the selection. That is the idea of Isaiah Andrews and "
            "Maximilian Kasy. <bookmark mark='a'/> What gets published is what researchers found, the latent "
            "distribution, times the chance that each result is published. <bookmark mark='b'/> In the simplest "
            "version, a significant result is always published and an insignificant one with relative probability "
            "beta. Beta of one means no selection; beta of a tenth means insignificant results are ten times less "
            "likely to appear. <bookmark mark='c'/> The trick is identification. With systematic replications, "
            "compare the originals with their repeats, which were not selected. <bookmark mark='d'/> With a "
            "meta-study, compare precise studies with imprecise ones: without selection, the imprecise ones should "
            "scatter symmetrically around the precise ones."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(Create(step), FadeIn(bl), Write(eqs[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def funnel(self):
        M = load("meta")
        est, se = np.array(M["est"]), np.array(M["se"])
        miss = np.array(M["missing"])
        ax = plane([-0.35, 0.25], [0, 130], center=LEFT * 1.9 + DOWN * 0.3, x_length=8.0, y_length=5.0,
                   xticks=[-0.3, -0.2, -0.1, 0, 0.1, 0.2], yticks=[0, 25, 50, 75, 100, 125],
                   xlabel=r"estimated employment elasticity", ylabel=r"precision, \ $1/\text{se}$",
                   xfmt=lambda v: f"{v:.1f}".replace("-", "{-}"), yfmt=lambda v: f"{v:.0f}", font_size=14)

        def pts(xs, ss, col, r, op):
            return VGroup(*[Dot(ax.ax.c2p(x, 1 / s), radius=r, color=col, fill_opacity=op)
                            for x, s in zip(xs, ss) if -0.35 <= x <= 0.25 and 1 / s <= 130])
        pub = pts(est, se, PUB, 0.035, 0.85)
        gone = pts(miss[:, 0], miss[:, 1], GREY_B, 0.03, 0.35)
        lines = VGroup(vline(ax, M["theta"], 0, 130, TRUE, 2.6), vline(ax, M["naive"], 0, 130, FAIL, 2.6),
                       vline(ax, M["ak"]["theta"], 0, 130, FIRST, 2.6))
        key = VGroup(
            legend_rows([(PUB, "published"), (GREY_B, "never published (a sample)")], font_size=15),
            legend_rows([(TRUE, f"the truth: {M['theta']:.3f}".replace("-", "{-}")),
                         (FAIL, f"the published average: {M['naive']:.3f}".replace("-", "{-}")),
                         (FIRST, f"Andrews and Kasy: {M['ak']['theta']:.3f}".replace("-", "{-}"))], font_size=15),
            label(rf"insignificant results published \\ {100 * M['ak']['b_ns']:.0f}\% as often \ (truth "
                  rf"{100 * M['beta_ns']:.0f}\%)", font_size=15, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(ax.ax, RIGHT, buff=0.35)
        if key.get_right()[0] > 6.9:
            key.scale_to_fit_width(6.9 - key.get_left()[0])
        over = 100 * (M["naive"] / M["theta"] - 1)
        tag = island_tag(r"a simulated meta-study: \ agora.field.meta\_literature \ and ak\_meta", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Here is a meta-study built so the truth is known, shaped like the literature on the minimum wage. "
            f"<bookmark mark='a'/> {M['n']} published estimates of the elasticity of employment with respect to the "
            "minimum wage, each plotted against its precision. Precise studies sit high, imprecise ones low. Without "
            "selection this would be a symmetric funnel. <bookmark mark='b'/> It is not. Negative and significant "
            "estimates were always published; the rest only three times in ten. In grey, a sample of the studies that "
            "were run and never published: the funnel's missing side. <bookmark mark='c'/> The true average "
            f"elasticity is {say_num(M['theta'], 3)}. The published average is {say_num(M['naive'], 3)}, {over:.0f} "
            "percent more negative than the truth. <bookmark mark='d'/> Andrews and Kasy's model, fitted only to the "
            f"published points, gives {say_num(M['ak']['theta'], 3)}, and finds that insignificant results were "
            f"published {100 * M['ak']['b_ns']:.0f} percent as often as significant ones, close to the thirty percent "
            "that was built in."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pub], lag_ratio=0.003), FadeIn(key[0][0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(gone), FadeIn(key[0][1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[0]), FadeIn(key[1][0]))
            self.play(Create(lines[1]), FadeIn(key[1][1]))
            vo.wait_until("d")
            self.play(Create(lines[2]), FadeIn(key[1][2]), FadeIn(key[2]))
        self.clear_scene()

    def literatures(self):
        D = tables.SELECTION_67.data
        cards = point_cards([
            (r"laboratory experiments", rf"in Camerer and coauthors' replications, \ significant results were over "
             rf"{D['ak_lab']} times as likely to be published", PUB),
            (r"the minimum wage", rf"negative, \ significant estimates about {D['ak_minwage']} times as likely; \ "
             r"corrected, \ the average effect is about half the naive one", FAIL),
            (r"159 literatures", rf"{D['isd_estimates']:,} estimates: \ median power 18\% or less; \ nearly 80\% "
             r"of effects exaggerated, \ typically twofold", FIRST),
            (r"what corrections cannot do", r"they assume a model of selection; \ different models give different "
             r"answers; \ none restores the studies never run", STATE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"corrected literatures", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Andrews and Kasy (2019); \ Ioannidis, \ Stanley and Doucouliagos, \ \emph{EJ} "
                            r"127(605) (2017)", corner=DL, font_size=12)
        with self.voiceover(
            "And on real literatures. <bookmark mark='a'/> On the laboratory experiments of chapter two, Andrews and "
            "Kasy estimate that significant results were more than thirty times as likely to be published as "
            "insignificant ones. <bookmark mark='b'/> On a meta-study of the minimum wage's effect on employment, "
            "negative and significant estimates were about three times as likely to be published, and the "
            "corrected average effect is small, about half the naive one. Earlier, Hristos Doucouliagos and Tom "
            "Stanley had read sixty-four American studies the same way and found little evidence of any negative "
            "effect once selection was removed. <bookmark mark='c'/> John Ioannidis, Stanley and Doucouliagos "
            "surveyed a hundred and fifty-nine literatures in economics, sixty-four thousand estimates: the median "
            "study had eighteen percent power or less, and nearly four in five reported effects were exaggerated, "
            "typically by a factor of two. <bookmark mark='d'/> Corrections are models, though. They assume a form "
            "of selection, different forms give different answers, and none can restore the studies that were "
            "never run."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
