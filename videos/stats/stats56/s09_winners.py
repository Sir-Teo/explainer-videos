from __future__ import annotations

import numpy as np

from videos.stats.stats56.common import *  # noqa: F403


class Winners(VoiceoverScene):
    def construct(self):
        self.card()
        self.conditional()
        self.window()
        self.hybrid()
        self.chart()
        self.microarray()
        self.practice()
        self.board()

    def card(self):
        card = chapter_card(8, r"Inference on winners", r"The best-looking option, \ honestly", lit=(2024,), part=PART)
        with self.voiceover("Chapter eight. Inference on winners: the best-looking option, honestly."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def conditional(self):
        rows = [
            cmath(r"Y_k \overset{\rm ind}{\sim} N(\mu_k, \sigma^2),\ \sigma\text{ known}", r",", r"\hat\jmath = \arg\max_k Y_k: \ \text{the winner}", font_size=36),
            cmath(r"\{\hat\jmath = j\}", r"=", r"\{Y_j \ge \max_{k \ne j} Y_k\}: \ \text{given the losers, \ a half-line}", font_size=34),
            cmath(r"Y_j \mid \hat\jmath = j, \ Y_{-j}", r"\sim", r"N(\mu_j, \sigma^2) \text{ truncated to } [Y_{(2)}, \infty)", font_size=34),
            cmath(r"\text{median-unbiased}", r":", r"\hat\mu_j: \ P_{\hat\mu_j}(Y > y_j \mid \cdot) = \tfrac12", font_size=34),
        ]
        rows[2][-1].set_color(CONDC)
        whys = [why(r"programs, \ neighbourhoods, \ treatments"), why(r"the polyhedral lemma, \ once more"), why(r"$Y_{(2)}$: \ the runner-up"), why(r"Andrews, \ Kitagawa \& McCloskey (2024)")]
        head = label('Conditional', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Isaiah Andrews, Toru Kitagawa and Adam McCloskey studied the case that opened this part: K independent Gaussian estimates with a common known variance, one per option, and we pick the largest. This is our simple specialization of their more general result. <bookmark mark='b'/> The event that option j wins is the event that its estimate beats every other; given the losers, that is a half-line. <bookmark mark='c'/> So the winner's estimate, given that it won, is a normal truncated below at the runner-up: the polyhedral lemma once more. <bookmark mark='d'/> Inverting it gives conditional intervals, and the value of mu at which the pivot is one half is a median-unbiased estimate, which corrects the winner's curse."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def window(self):
        e = load("winners")["example"]
        y = np.asarray(e["y"])
        A = axes([-3, 5], [0, 3.0], x_length=7.4, y_length=4.0, xlabel=r"the winner's estimate", ylabel=r"density",
                 xticks=[-2, 0, 2, 4], yticks=[0, 1, 2, 3], center=[-2.5, 0.0, 0])
        ax = A.ax
        sw = SelectionWindow(ax, a=e["second"], b=np.inf, y=float(y[e["j"]]), x_range=(-3, 5), trunc_color=CONDC, obs_color=SELC, region_color=SELC)
        pic = sw.at(e["median_unbiased"])
        dots = VGroup(*[Dot(ax.c2p(v, 0.09), radius=0.07, color=SELC if k == e["j"] else GREY_B) for k, v in enumerate(y)])
        side = fit_rows(VGroup(
            label(r"ten options; \ the first has $\mu = 1$, \ the rest 0", font_size=22),
            label(rf"winner: \ option {e['j'] + 1}, \ $y = {y[e['j']]:.2f}$; \ runner-up {e['second']:.2f}", font_size=22, color=SELC),
            label(rf"naive: \ $({e['naive'][0]:.2f}, {e['naive'][1]:.2f})$", font_size=22, color=NAIVEC),
            label(rf"conditional: \ $({e['lo']:.2f}, {e['hi']:.2f})$; \ median-unbiased {e['median_unbiased']:.2f}", font_size=22, color=CONDC),
            label(rf"hybrid: \ $({e['hybrid'][0]:.2f}, {e['hybrid'][1]:.2f})$", font_size=22, color=HYBC),
        ), 4.6, 0.38, [4.45, 0.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> One draw: ten options, the first with a true mean of one and the rest zero. <bookmark "
            f"mark='b'/> The winner is option {e['j'] + 1}, at {say(y[e['j']], 2)}, {'the truly best one' if e['j'] == 0 else 'whose true mean is zero'}, "
            f"and the runner-up is at {say(e['second'], 2)}. <bookmark mark='c'/> The naive interval is the winner plus or minus one point nine six. "
            f"<bookmark mark='d'/> The conditional law is cut at the runner-up, and the conditional interval runs from "
            f"{say(e['lo'], 2)} to {say(e['hi'], 2)}, with a median-unbiased estimate of {say(e['median_unbiased'], 2)}: the "
            f"narrow win makes it long. <bookmark mark='e'/> The hybrid interval, coming next, is {say(e['hybrid'][0], 2)} to "
            f"{say(e['hybrid'][1], 2)}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"one simulated draw")))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(sw.region), FadeIn(sw.obs), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(pic[0]), Create(pic[1]), FadeIn(pic[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def hybrid(self):
        rows = [
            cmath(r"\text{projection}", r":", r"Y_j \pm c_\beta\sigma, \ \ c_\beta \text{ simultaneous over all } K: \ \text{never long, \ often wide}", font_size=30),
            cmath(r"\text{conditional}", r":", r"\text{short when the win is clear, \ very long when it is narrow}", font_size=32),
            cmath(r"\text{hybrid}", r":", r"\text{condition also on } |Y_j - \mu_j| \le c_\beta\sigma, \ \text{miscoverage } \frac{\alpha - \beta}{1 - \beta}", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\text{valid on average; \ never longer than projection}", font_size=30),
        ]
        rows[2][-1].set_color(HYBC)
        whys = [why(r"Bonferroni-like, \ $\beta$ small"), why(r"Kivaranovic--Leeb again"), why(r"the best of both"), why(r"unconditional validity")]
        head = label('Hybrid', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Two alternatives frame the solution. The projection interval uses a simultaneous constant over all K options: never very long, but always wide. <bookmark mark='b'/> The conditional interval is short when the win is clear and very long when it is narrow. <bookmark mark='c'/> Andrews, Kitagawa and McCloskey's hybrid conditions also on the winner lying within the simultaneous band, using miscoverage alpha minus beta over one minus beta. Here beta is point zero zero five. Conditional coverage on the band and the winning event is one minus alpha over one minus beta; allocating the band-failure budget gives unconditional coverage at least one minus alpha. <bookmark mark='d'/> It keeps coverage on average over the possible winners, and it is never longer than the projection interval."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("winners")["by_gap"]
        g = [r["gap"] for r in d]
        A = axes([-0.2, 4.2], [0, 11], x_length=7.4, y_length=4.4, xlabel=r"the best option's lead $\mu_1 - 0$, \ $K = 10$", ylabel=r"median interval length",
                 xticks=[0, 1, 2, 3, 4], yticks=[0, 4, 8], center=[-2.5, 0.2, 0])
        ax = A.ax

        def ln(key, col):
            return VGroup(polyline(ax, g, [r[key] for r in d], col, 4), *[Dot(ax.c2p(a, r[key]), radius=0.06, color=col) for a, r in zip(g, d)])

        cc, ch, cp = ln("len_cond", CONDC), ln("len_hybrid", HYBC), ln("len_proj", SIMC)
        nv = DashedLine(ax.c2p(-0.2, 3.92), ax.c2p(4.2, 3.92), color=NAIVEC, stroke_width=2)
        r0, r4 = d[0], d[-1]
        side = fit_rows(VGroup(
            label(rf"red dashed: \ naive, \ 3.92; \ coverage {100 * r0['naive']:.0f}\% $\to$ {100 * r4['naive']:.0f}\%", font_size=22, color=NAIVEC),
            label(rf"blue: \ conditional: \ {r0['len_cond']:.1f} $\to$ {r4['len_cond']:.1f}; \ coverage $\approx 95\%$", font_size=22, color=CONDC),
            label(rf"purple: \ projection: \ {r0['len_proj']:.2f}; \ coverage $\approx 100\%$", font_size=22, color=SIMC),
            label(rf"green: \ hybrid: \ {r0['len_hybrid']:.1f} $\to$ {r4['len_hybrid']:.1f}; \ coverage $\approx 95\%$", font_size=22, color=HYBC),
            label(r"1,500 runs per point", font_size=22, color=GREY_A),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The four intervals as the best option's lead grows. The naive interval has fixed length, and covers only {100 * r0['naive']:.0f} percent when nothing stands out, rising to {100 * r4['naive']:.0f} when the best leads by four. <bookmark mark='b'/> The conditional interval covers ninety-five percent, but its median length is {say(r0['len_cond'], 1)} when there is no clear winner. <bookmark mark='c'/> The projection interval is always {say(r0['len_proj'], 2)} long and almost always covers. <bookmark mark='d'/> The hybrid covers ninety-five percent with a median length of {say(r0['len_hybrid'], 1)} without a clear winner and {say(r4['len_hybrid'], 1)} with one. In these simulated settings it often improves the trade-off; only the bound by projection length is uniform."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(Create(nv), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ch), FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def microarray(self):
        d = load("microarray")
        rows = fit_rows(VGroup(
            label(rf"Singh's prostate microarray: \ {d['m']:,} genes, \ $z$-values; \ the top two: \ {d['top'][0]:.2f}, \ {d['top'][1]:.2f}", font_size=26, color=GREY_A),
            label(rf"naive 95\% for the top gene's mean: \ $({d['naive'][0]:.2f}, {d['naive'][1]:.2f})$", font_size=26, color=NAIVEC),
            label(rf"conditional: \ $({d['cond'][0]:.2f}, {d['cond'][1]:.2f})$; \ median-unbiased {d['median_unbiased']:.2f}", font_size=26, color=CONDC),
            label(rf"hybrid: \ $({d['hybrid'][0]:.2f}, {d['hybrid'][1]:.2f})$; \ projection $({d['proj'][0]:.2f}, {d['proj'][1]:.2f})$", font_size=26, color=HYBC),
            label(r"independent-Gaussian working illustration: \ no certified gene discovery", font_size=26, color=SELC),
            label(r"(correlated approximate $z$-statistics; \ the displayed coverage is not established)", font_size=22, color=GREY_B),
        ), 12.4, 0.45, [0, 0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> On real data: Singh's prostate cancer microarray, Efron's example, with six thousand and thirty-three genes. The top gene's z-value is {say(d['top'][0], 2)}, and the runner-up's {say(d['top'][1], 2)}. <bookmark mark='b'/> The naive interval for the top gene's mean runs from {say(d['naive'][0], 2)} to {say(d['naive'][1], 2)}. <bookmark mark='c'/> Conditional on its winning so narrowly, the interval runs from {say(d['cond'][0], 2)} to {say(d['cond'][1], 2)}, and the median-unbiased estimate is {say(d['median_unbiased'], 2)}. <bookmark mark='d'/> The hybrid interval, {say(d['hybrid'][0], 2)} to {say(d['hybrid'][1], 2)}, excludes zero. <bookmark mark='e'/> That exclusion is a working-model calculation, not evidence with a certified ninety-five percent guarantee that the selected gene has a nonzero effect. <bookmark mark='f'/> These transformed gene test statistics are correlated and only approximately Gaussian. Known Gaussian covariance can already be handled by the polyhedral lemma; learning covariance and calibrating this high dimensional approximation are the challenges."
        ) as vo:
            self.play(FadeIn(museum_tag(r"Singh et al. (2002); \ Efron (2010)")))
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def practice(self):
        rows = [
            cmath(r"\text{correlated estimates}", r":", r"\text{still an interval along } \eta", font_size=30),
            cmath(r"\text{many winners}", r":", r"\text{inference on the top } k, \ \text{or on all above a threshold}", font_size=32),
            cmath(r"\text{applications}", r":", r"\text{job training; \ neighbourhoods}", font_size=32),
            cmath(r"\text{the lesson}", r":", r"\text{report a median-unbiased estimate and a hybrid}", font_size=32),
        ]
        rows[3][-1].set_color(HYBC)
        whys = [why(r"chapter 3's lemma"), why(r"their extensions"), why(r"the paper's two examples"), why(r"a reporting standard")]
        head = label('Practice', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> In practice the estimates are correlated, and then the event that j wins is a "
            "polyhedron in K dimensions; along the direction of the winner's estimate it is still an interval, so "
            "chapter three's lemma applies. <bookmark mark='b'/> The same ideas give inference on the top k options, "
            "or on every option above a threshold. <bookmark mark='c'/> Andrews, Kitagawa and McCloskey applied them "
            "to choosing job-training programmes by their estimated earnings effects, and to choosing neighbourhoods "
            "by estimated economic opportunity. <bookmark mark='d'/> Their recommendation is a reporting standard: "
            "whenever you report the best of several options, report a median-unbiased estimate and a hybrid interval "
            "too."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("winner", "conditional interval", "hybrid"),
                   f"<bookmark mark='a'/> The Board, with four thousand draws of ten options, one of them better by one. The "
                   f"naive interval: {100 * br[0]['achieved']:.1f} percent, broken. <bookmark mark='b'/> The conditional "
                   f"interval, {100 * br[1]['achieved']:.1f} percent, and the hybrid, {100 * br[2]['achieved']:.1f} percent: "
                   f"both kept.", [("a", [0]), ("b", [1, 2])])
