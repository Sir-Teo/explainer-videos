from __future__ import annotations

import numpy as np

from videos.stats.stats22.common import *  # noqa: F403


class Consistency(VoiceoverScene):
    def construct(self):
        self.card()
        self.kl()
        self.curves()
        self.wald()
        self.limits()

    def card(self):
        card = chapter_card(2, r"Consistency", r"The argmax of a random curve", lit=(1949,), part=PART)
        with self.voiceover("Chapter two. Consistency."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def kl(self):
        rows = [
            cmath(r"\tfrac1n \ell_n(\theta)", r"=", r"\tfrac1n \textstyle\sum_i \log f(X_i;\theta)", font_size=30),
            cmath(r"\tfrac1n \ell_n(\theta)", r"\to", r"M(\theta) = E_{\theta_0} \log f(X;\theta)", font_size=30),
            cmath(r"M(\theta_0) - M(\theta)", r"=", r"\mathrm{KL}(f_{\theta_0} \,\|\, f_\theta) \ge 0", font_size=30),
            cmath(r"\text{identifiable}", r"\Rightarrow", r"\theta_0 \text{ is the unique maximum of } M", font_size=30),
        ]
        rows[2][2].set_color(LIK)
        whys = [why(r"the average log likelihood: \ a random curve"), why(r"the law of large numbers, \ at each $\theta$"),
                why(r"Jensen (Part 21): \ Kullback--Leibler"), why(r"equality only if $f_\theta = f_{\theta_0}$")]
        intro = label('Expected log likelihood is maximized at an identifiable truth', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Why should maximum likelihood find the truth? <bookmark mark='a'/> Divide the log likelihood by n: it's "
            "an average of independent terms, a random curve over theta. <bookmark mark='b'/> By the law of large "
            "numbers, at each theta under suitable integrability it converges to a fixed curve M of theta, the "
            "expected log likelihood under the true distribution. <bookmark mark='c'/> And by Jensen's inequality "
            "from Part 21, M at the truth minus M anywhere else is a Kullback–Leibler divergence, which is never "
            "negative. <bookmark mark='d'/> If the model is identifiable, the divergence is zero only at the truth, "
            "so the limiting curve has its unique peak exactly at theta zero."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        d = load("consistency")
        th = np.asarray(d["theta"])
        A = axes([0.05, 2.0], [-1.6, -0.8], x_length=8.2, y_length=4.4, xlabel=r"Poisson rate $\theta$",
                 ylabel=r"average log likelihood (up to a constant)", xticks=[0.25, 0.61, 1.0, 1.5, 2.0], yticks=[-1.5, -1.25, -1],
                 center=[-1.5, 0.3, 0])
        ax = A.ax
        exp_c = curve(ax, th, d["expected"], TRUE, 4)
        cols = {"10": GREY_C, "100": TEAL, "1000": BLUE, "10000": PATH}
        cs = VGroup()
        for k, c in cols.items():
            y = np.asarray(d["curves"][k]["ll"])
            cs.add(VGroup(curve(ax, th, y, c, 2.5), Dot(ax.c2p(d["curves"][k]["argmax"], float(np.interp(d["curves"][k]["argmax"], th, y))), radius=0.06, color=c)))
        truth = DashedLine(ax.c2p(d["lam0"], -1.6), ax.c2p(d["lam0"], -0.8), color=TRUE, stroke_width=2)
        rows = fit_rows(VGroup(
            label(rf"Poisson, \ rate {d['lam0']:.2f}: \ the horse kicks", font_size=22),
            label(r"gold: \ $M(\theta)$, \ the limit", font_size=22, color=TRUE),
            VGroup(label(r"$n = 10$: \ grey; \ $100$: \ teal;", font_size=22),
                   label(r"$1{,}000$: \ blue; \ $10{,}000$: \ amber", font_size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            label(rf"their peaks: \ {d['curves']['10']['argmax']:.2f}, \ {d['curves']['100']['argmax']:.2f}, \ {d['curves']['1000']['argmax']:.3f}, \ {d['curves']['10000']['argmax']:.4f}", font_size=22, color=PATH),
            label(r"the curves converge, \ so their peaks do", font_size=22, color=HIT),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the picture, for a Poisson rate, using Bortkiewicz's horse kicks from Part 3: their "
            "rate, point six one, plays the truth. <bookmark mark='b'/> In gold, the limiting curve M of theta, peaked at point "
            "six one. <bookmark mark='c'/> Then the average log likelihood of samples of ten, a hundred, a thousand and ten "
            "thousand draws from one growing sample. Each is a random curve. <bookmark mark='d'/> Their peaks, the maximum "
            "likelihood estimates, sit at one point one, point six eight, point six three eight and point six one oh. "
            "<bookmark mark='e'/> As the curves settle onto "
            "the gold one, their peaks settle onto its peak. That's the whole idea of consistency."
        ) as vo:
            self.play(FadeIn(A), Create(truth))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(exp_c), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.5), FadeIn(rows[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def wald(self):
        rows = [
            cmath(r"\sup_\theta \big|\tfrac1n\ell_n(\theta) - M(\theta)\big|", r"\to", r"0", font_size=30),
            cmath(r"\sup_{|\theta - \theta_0| \ge \varepsilon} M(\theta)", r"<", r"M(\theta_0)", font_size=30),
            cmath(r"\Rightarrow", r"", r"P\big(|\hat\theta_n - \theta_0| \ge \varepsilon\big) \to 0", font_size=30),
            cmath(r"\text{Wald (1949)}", r":", r"\text{compactness, \ continuity, \ a dominating function}", font_size=28),
        ]
        rows[2][-1].set_color(HIT)
        whys = [why(r"uniform, \ not just pointwise, \ convergence"), why(r"a well-separated peak"),
                why(r"the MLE is consistent"), why(r"conditions that make the uniform step work")]
        intro = label('Uniform convergence and a separated maximum give consistency', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Turning the picture into a proof needs two things. <bookmark mark='a'/> The random curves must converge "
            "uniformly over theta, not just at each point, so that no stray spike far away can win. <bookmark "
            "mark='b'/> And the limiting peak must be well separated: everywhere at least epsilon away, M is lower by"
            " a margin. <bookmark mark='c'/> Then the probability that the estimate lands more than epsilon from the "
            "truth goes to zero. <bookmark mark='d'/> Abraham Wald gave conditions for the uniform step in 1949, "
            "compactness, suitable continuity and integrable domination can provide a modern sufficient route. Wald's"
            " 1949 theorem is a foundational result; versions differ in their precise assumptions."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def limits(self):
        rows = fit_rows(VGroup(
            label(r"no proof used normality, \ smoothness, \ or even a derivative", font_size=24, color=LIK),
            label(r"it needs: \ identifiability, \ and a fixed parameter space as $n$ grows", font_size=24),
            label(r"with parameters that multiply with $n$: \ Neyman--Scott, \ chapter seven", font_size=24, color=RES),
            label(r"with a wrong model: \ the peak of $M$ is the closest wrong answer, \ chapter ten", font_size=24, color=OBS),
            label(r"the same argument: \ M-estimators in general, \ Part 47", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Notice what the argument didn't use: no normality, no smoothness, not even a "
            "derivative. <bookmark mark='b'/> It needs identifiability and a parameter space that stays fixed as n "
            "grows. <bookmark mark='c'/> Let the parameters multiply with the data and it can fail, as chapter seven "
            "shows. <bookmark mark='d'/> Under the same uniform-convergence and separated-maximum conditions, a "
            "misspecified estimate can still converge, but to the peak of the wrong M, the model's closest "
            "approximation to the truth, as chapter ten shows. <bookmark mark='e'/> And the same argument applies to "
            "other average-objective estimators when its conditions hold, which Part 47 exploits."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
