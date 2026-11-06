from __future__ import annotations

from videos.stats.stats27.common import *  # noqa: F403

CODE = r"""from explainer.stats.kit import ppl as P

def eight_schools(p):
    theta = p["mu"] + p["tau"] * p["z"]
    return (P.normal_lpdf(p["mu"], 0, 5)
            + P.halfcauchy_lpdf(p["tau"], 5)
            + P.normal_lpdf(p["z"], 0, 1)
            + P.normal_lpdf(y, theta, sigma))

m = P.Model({"mu": (1, "real"), "tau": (1, "positive"),
             "z": (8, "real")}, eight_schools)
fit = P.sample(m, chains=4, iters=1000, warmup=1000)"""


class PPL(VoiceoverScene):
    def construct(self):
        self.card()
        self.parts()
        self.code()
        self.transforms()
        self.autodiff()
        self.checks()
        self.debugging()
        self.real()

    def card(self):
        card = chapter_card(8, r"Built: \ a probabilistic programming language", r"Write the model; \ get the posterior", lit=(2017,), part=PART)
        with self.voiceover("Chapter eight. Built: a probabilistic programming language."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def parts(self):
        rows = fit_rows(VGroup(
            label(r"1. \ a model is a log density, \ written in ordinary code", font_size=26),
            label(r"2. \ automatic differentiation gives its gradient: \ \emph{AI, Built}'s reverse mode", font_size=26, color=SAMPLER),
            label(r"3. \ constrained parameters are mapped to $\mathbb R$, \ with their Jacobians", font_size=26, color=PRIOR),
            label(r"4. \ NUTS with adaptation, \ several chains", font_size=26, color=HIT),
            label(r"5. \ diagnostics on everything: \ $\hat R$, \ ESS, \ divergences", font_size=26, color=PATH),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Everything so far assembles into a probabilistic programming language, the design of Stan "
            "and PyMC, and statkit now has a small one. A model is just a function returning the log density. "
            "<bookmark mark='b'/> Its gradient comes from the reverse-mode automatic differentiation that AI, Built's fourth "
            "part wrote: no derivative is ever worked out by hand. <bookmark mark='c'/> Parameters with constraints, like a "
            "positive standard deviation, are transformed to the whole real line, and the transform's Jacobian is added to "
            "the log density. <bookmark mark='d'/> NUTS with Stan's warmup runs on the transformed space, several chains at "
            "once, <bookmark mark='e'/> and every result comes with R-hat, effective sample sizes and divergence counts."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def code(self):
        code = Code(code_string=CODE, language="python", background="rectangle", formatter_style="monokai",
                    add_line_numbers=False, paragraph_config={"font_size": 22})
        code.scale_to_fit_width(min(code.width, 10.5)).move_to([0, 0.3, 0])
        foot = label(r"the eight schools, \ non-centred, \ in twelve lines", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> This is the whole of chapter seven's non-centred eight schools model in statkit. The "
            "function adds up the log densities of the priors and the likelihood, written exactly as the model is written on "
            "paper. <bookmark mark='b'/> The model declares each parameter's size and support: tau is positive, so the "
            "sampler works with its logarithm. <bookmark mark='c'/> One call samples four chains with adaptation."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(code, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(code, scale_factor=1.02))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(1.0)
        self.clear_scene()

    def transforms(self):
        rows = [
            cmath(r"\tau > 0", r":", r"\tau = e^u, \ \ \log|d\tau/du| = u", font_size=30),
            cmath(r"0 < p < 1", r":", r"p = \tfrac{1}{1 + e^{-u}}, \ \ \log|dp/du| = \log p + \log(1 - p)", font_size=28),
            cmath(r"\log \pi(u)", r"=", r"\log \pi(\tau(u)) + \log|d\tau/du|", font_size=30),
            cmath(r"\text{forget the Jacobian}", r":", r"\text{a different prior, \ silently}", font_size=30),
        ]
        rows[2][2].set_color(SAMPLER)
        whys = [why(r"positive"), why(r"a probability"), why(r"change of variables"), why(r"the commonest home-made bug")]
        with self.voiceover(
            "<bookmark mark='a'/> The transforms deserve a moment. A positive parameter becomes the exponential of an "
            "unconstrained u, <bookmark mark='b'/> a probability the logistic of one. <bookmark mark='c'/> The sampler works "
            "with u, so the log density must include the log of the transform's derivative, the change-of-variables rule. "
            "<bookmark mark='d'/> Forget it, and you have silently changed the prior; it is the commonest bug in home-made "
            "samplers, and chapter twelve's calibration catches it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def checks(self):
        d = load("ppl")
        hdr = [r"\textbf{quantity}", r"\textbf{exact}", r"\textbf{statkit NUTS}", r"\textbf{MC SE}"]
        body = [[r[0], f"{r[1]:.4f}", f"{r[2]:.4f}", (f"{r[3]:.4f}" if r[3] is not None else r"")] for r in d["rows"]]
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.7, row_buff=0.28, colors=[GREY_A] + [None] * 6)
        for r in tb[1:]:
            r[1].set_color(EXACTC)
            r[2].set_color(HIT)
        tb.move_to([0, 0.6, 0])
        foot = label(r"every answer within its Monte Carlo error of the exact one; \ also tested in \texttt{tests/test\_stats\_kit\_ppl.py}",
                     font_size=22, color=GREY_A).move_to([0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A sampler must be checked against answers known in closed form. A normal mean, a "
            "proportion with its logistic transform, a Poisson rate with its log transform, and the eight schools against "
            "Part 26's exact grid. <bookmark mark='b'/> Each NUTS answer is within its Monte Carlo error of the exact one, and "
            "the same checks run in the test suite every time the code changes."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(1.0)
        self.clear_scene()

    def real(self):
        rows = fit_rows(VGroup(
            label(r"Stan (2017): \ its own language, \ C++, \ NUTS; \ the standard", font_size=24, color=SAMPLER),
            label(r"PyMC, \ NumPyro, \ Turing.jl: \ the same ideas in Python and Julia", font_size=24),
            label(r"BUGS and JAGS: \ the Gibbs generation", font_size=24, color=GREY_A),
            label(r"statkit's: \ 700 lines, \ slow, \ readable: \ for understanding, \ not production", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The real systems: Stan, with its own modelling language compiled to C++, is the standard. "
            "<bookmark mark='b'/> PyMC, NumPyro and Turing bring the same ideas to Python and Julia. <bookmark mark='c'/> BUGS "
            "and JAGS were the Gibbs-sampling generation before them. <bookmark mark='d'/> Statkit's is about seven hundred lines, slow "
            "and readable: meant for understanding what the real ones do."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def debugging(self):
        rows = fit_rows(VGroup(
            label(r"1. \ simulate fake data from the model; \ fit it; \ recover the parameters?", font_size=24, color=WHITE),
            label(r"2. \ check gradients by finite differences", font_size=24, color=SAMPLER),
            label(r"3. \ compare with an exact answer on a simpler case", font_size=24, color=EXACTC),
            label(r"4. \ run SBC: \ the rank histograms must be flat", font_size=24, color=HIT),
            label(r"5. \ read every warning: \ divergences, \ $\hat R$, \ low ESS", font_size=24, color=DIV),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> When building or using such a system, a checklist. Simulate fake data from the model, fit "
            "it, and see whether the parameters come back. <bookmark mark='b'/> Check gradients against finite differences, "
            "as statkit's tests do. <bookmark mark='c'/> Compare with an exact answer on a simplified case. "
            "<bookmark mark='d'/> Run simulation-based calibration. <bookmark mark='e'/> And read every warning the sampler "
            "gives."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def autodiff(self):
        rows = [
            cmath(r"\text{forward pass}", r":", r"\text{compute } \log\pi, \ \text{recording every operation}", font_size=30),
            cmath(r"\text{backward pass}", r":", r"\bar v_i = \textstyle\sum_{j: \, i \to j} \bar v_j\, \partial v_j/\partial v_i", font_size=30),
            cmath(r"\text{cost}", r":", r"\text{a small multiple of one evaluation, \ any } d", font_size=30),
            cmath(r"\text{so}", r":", r"\text{gradients are cheap: \ HMC scales}", font_size=30),
        ]
        rows[2][-1].set_color(HIT)
        whys = [why(r"the computation graph"), why(r"the chain rule, \ run backwards"), why(r"Baur \& Strassen (1983)"),
                why(r"AI, \ Built Part 4")]
        with self.voiceover(
            "<bookmark mark='a'/> Why gradients are affordable. The forward pass computes the log density and records each "
            "operation in a graph. <bookmark mark='b'/> The backward pass runs the chain rule from the output back to every "
            "input, accumulating each parameter's derivative. <bookmark mark='c'/> Its cost is a small constant multiple of "
            "one evaluation of the density, however many parameters there are. <bookmark mark='d'/> That single fact is why "
            "gradient-based samplers scale to thousands of dimensions, and why the same machinery trains neural networks."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
