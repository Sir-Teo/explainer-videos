from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, illustration, load


class Stopping(VoiceoverScene):
    def construct(self):
        s = load("stopping")
        self.card()
        self.method()
        self.region(s)
        self.table(s)

    def card(self):
        c = chapter_card(6, r"Deep optimal stopping", r"Can a network learn when to exercise?", part=PART)
        with self.voiceover("Chapter six. Deep optimal stopping."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def method(self):
        rows = [cmath(r"f_n(x)", r"\in", r"\{0, 1\}:\ \text{stop at date } n\text{, or wait}", font_size=38,
                      colors={r"f_n(x)": NET}),
                cmath(r"\max_{\theta_n}", r"\ ", r"\mathbb{E}\big[\,g_n\, F_{\theta_n}(X_n) + G_{n+1}\,(1 - F_{\theta_n}(X_n))\,"
                      r"\big]", font_size=36, colors={r"\max_{\theta_n}": GOOD})]
        whys = [why(r"Becker, Cheridito and Jentzen (2019): Part 16's Longstaff--Schwartz regressed the value of waiting; "
                    r"here a network learns the stopping decision itself, one network per exercise date"),
                why(r"train backwards from expiry: $G_{n+1}$ is what the later, already-trained rules collect on each path; "
                    r"during training the decision is softened to a probability $F$, then made hard. Any rule is a real "
                    r"strategy, so its payoff on fresh paths is a lower bound")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.4, buff=1.0, edge=6.9)
        with self.voiceover(
            "Part sixteen priced an American option by regressing the value of waiting. Sebastian Becker, Patrick "
            "Cheridito and Arnulf Jentzen asked the network to learn the decision itself. At each exercise date, a network "
            "looks at the state and says stop or wait. <bookmark mark='a'/> Training runs backwards from expiry. "
            "At each date, the network is rewarded with the payoff if it stops, or with whatever the later rules "
            "collect if it waits. Because any rule is a real strategy, its average payoff on fresh paths is a lower "
            "bound on the price."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def region(self, s):
        r = s["region"]
        gr = np.asarray(r["grid"])
        st = np.asarray(r["stop"])
        g = axes([gr[0], gr[-1]], [gr[0], gr[-1]], x_length=5.0, y_length=5.0, xlabel=r"asset 1", ylabel=r"asset 2",
                 xticks=[80, 120, 160], yticks=[80, 120, 160], font_size=15).to_edge(LEFT, buff=1.0).shift(DOWN * 0.2)
        ax = g.ax
        step_ = gr[1] - gr[0]
        cells = VGroup()
        for i in range(len(gr)):
            for j in range(len(gr)):
                if st[i, j]:
                    p0 = ax.c2p(gr[j] - step_ / 2, gr[i] - step_ / 2)
                    p1 = ax.c2p(gr[j] + step_ / 2, gr[i] + step_ / 2)
                    cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=GOOD,
                                        fill_opacity=0.55).move_to((p0 + p1) / 2))
        diag = DashedLine(ax.c2p(gr[0], gr[0]), ax.c2p(gr[-1], gr[-1]), stroke_color=GREY_B, stroke_width=1.5)
        kline = VGroup(DashedLine(ax.c2p(100, gr[0]), ax.c2p(100, 100), stroke_color=GREY_C, stroke_width=1),
                       DashedLine(ax.c2p(gr[0], 100), ax.c2p(100, 100), stroke_color=GREY_C, stroke_width=1))
        leg = legend([(GOOD, r"the network says: exercise now"), (GREY_B, r"the two assets equal")], font_size=17)
        leg.next_to(g, RIGHT, buff=0.6).align_to(g, UP)
        side = wrapped_label(r"a max-call on two assets, a year and a third in: exercise when one asset is far above the "
                             r"strike and well ahead of the other. Near the diagonal, either could still win, and the option "
                             r"to wait for the better one is worth more than the dividends lost. The two lobes are the "
                             r"textbook shape (Broadie and Detemple 1997), found without being told", 5.2, 20,
                             GREY_A).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        src = illustration(r"Bermudan max-call: $K = 100$, $r = 5\%$, dividends 10\%, $\sigma = 20\%$, 3 years, 9 dates")
        with self.voiceover(
            "What does the network learn? Here is its decision at the fourth exercise date, for a call on the better of "
            "two assets, over every pair of prices. <bookmark mark='a'/> It exercises when one asset is far above the "
            "strike and well ahead of the other. Along the diagonal, where either asset could still end up the winner, "
            "it waits: the chance to pick the better one later is worth more than the dividends given up. Two lobes, "
            "split by the diagonal: the shape known from the theory, found without being told."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(diag), FadeIn(kline), FadeIn(leg[1]))
            vo.wait_until("a")
            self.play(FadeIn(cells, lag_ratio=0.002), FadeIn(leg[0]), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def table(self, s):
        d2, d5 = s["2"], s["5"]
        gap = 100 * (d5["reference"]["lower"] - d5["lower"]) / d5["reference"]["lower"]
        head = VGroup(label(r"assets", font_size=22, color=GREY_A), label(r"our lower bound", font_size=22, color=GREY_A),
                      label(r"published", font_size=22, color=GREY_A), label(r"time", font_size=22, color=GREY_A))
        rows = VGroup(head)
        for d, r, ref in ((2, d2, rf"{d2['reference']['binomial']:.3f}\ \text{{(binomial tree)}}"),
                          (5, d5, rf"[{d5['reference']['ci'][0]:.3f},\ {d5['reference']['ci'][1]:.3f}]\ \text{{(95\% CI)}}")):
            rows.add(VGroup(MathTex(str(d), font_size=32), MathTex(rf"{r['lower']:.3f} \pm {2 * r['se']:.3f}", font_size=32,
                                                                   color=NET),
                            MathTex(ref, font_size=28, color=REF), MathTex(rf"{r['seconds'] / 60:.0f}\ \text{{min}}", font_size=28)))
        xs = [-5.0, -2.0, 1.9, 5.3]
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 1.4 - 0.9 * i, 0])
        title = label(r"Bermudan max-call, at the money", font_size=30).to_edge(UP, buff=0.7)
        foot = wrapped_label(r"our bounds are $\pm 2$ standard errors on a million fresh paths, after 500 training steps per "
                             r"date on a CPU; the published values are Becker, Cheridito and Jentzen's (2019) interval (their "
                             r"lower bound alone: 26.156) and a binomial lattice. The method scales: "
                             r"they report 500 assets, where no tree and no regression basis can follow", 11.6, 20,
                             GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            f"And the prices. With two assets, the network's rule earns {d2['lower']:.2f}, against {d2['reference']['binomial']:.2f} "
            f"from a binomial tree. <bookmark mark='a'/> With five, {d5['lower']:.2f}, {gap:.1f} percent below the "
            f"published lower bound of {d5['reference']['lower']:.2f}: a lower bound from a much smaller training budget "
            "sits a little lower, as it should. The method's real point is scale: the paper prices the same option on five hundred "
            "assets, where no tree and no regression basis can follow."
        ) as vo:
            self.play(FadeIn(title), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]), FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()
