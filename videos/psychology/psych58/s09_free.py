from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


class Free(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"The free-energy principle", r"Can one quantity explain everything a brain does?",
                     marr=("what",))
        self.derive()
        self.plot()
        self.claims()

    def derive(self):
        head = heading(r"Variational inference, \ step by step")
        lines = VGroup(
            MathTex(r"p(z \mid x) = \frac{p(x \mid z)\,p(z)}{p(x)}", font_size=34),
            MathTex(r"F(q) = \mathbb{E}_q[\log q(z) - \log p(x, z)]", font_size=34),
            MathTex(r"F(q) = \mathrm{KL}\big(q(z)\,\|\,p(z \mid x)\big) - \log p(x)", font_size=34),
            MathTex(r"F(q) \ge -\log p(x) \quad\text{(surprise)}", font_size=34),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to([-3.2, -0.1, 0])
        notes = rows_of([
            (r"Bayes' rule: \ the posterior needs $p(x)$, \ usually impossible to compute", WHITE),
            (r"pick a simple family $q$ and define the free energy $F$", MODEL),
            (r"rearranged: \ the distance from the true posterior, \ plus surprise", PERSON),
            (r"minimizing $F$ over $q$ does inference; \ its minimum bounds surprise (\emph{AI, Built}'s "
             r"variational inference)", GOOD),
        ], 5.4, 19, 0.5).move_to([3.6, -0.1, 0])
        with self.voiceover(
            "Can one quantity explain everything a brain does? First, the mathematics, step by step. "
            "<bookmark mark='a'/> Bayes' rule gives the posterior over causes z given data x, but it needs the "
            "probability of the data, which is usually impossible to compute. <bookmark mark='b'/> So pick a simple "
            "family of distributions q, and define the free energy F: the expected log of q minus the log of the "
            "joint. <bookmark mark='c'/> Rearranged, it's the divergence between q and the true posterior, plus the "
            "surprise, minus log p of x. <bookmark mark='d'/> The divergence is never negative, so minimizing F over "
            "q does inference, and its minimum is a bound on surprise. It's the variational inference of AI, Built."
        ) as vo:
            self.play(FadeIn(head))
            for m, eq_, n_ in zip("abcd", lines, notes):
                vo.wait_until(m)
                self.play(FadeIn(eq_), FadeIn(n_, shift=RIGHT * 0.15))
        self.clear_scene()

    def plot(self):
        d = load("fe")
        head = heading(r"The free energy of a small model")
        A = axes([-1, 3], [0, 6], x_length=5.6, y_length=3.2, xticks=[-1, 0, 1, 2, 3], yticks=[0, 2, 4, 6],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"the mean of $q$",
                 ylabel=r"$F$ (nats)", center=[-3.3, 0.2, 0], font_size=12)
        c = curve(A.ax, d["mu"], np.minimum(d["F"], 6), MODEL, stroke_width=4)
        s = DashedLine(A.ax.c2p(-1, d["surprise"]), A.ax.c2p(3, d["surprise"]), color=AUTH, stroke_width=2)
        dot = Dot(A.ax.c2p(d["post_mu"], d["surprise"]), radius=0.08, color=GOOD)
        rows = rows_of([
            (r"a cause $z$ with prior N(0, 1); \ a reading $x = 2$ with noise SD 0.5", WHITE),
            (r"$F$ over the mean of $q$: \ a bowl", MODEL),
            (rf"its bottom is the exact posterior mean, \ {d['post_mu']:.1f}, \ and its height the surprise, \ "
             rf"{d['surprise']:.2f} nats", GOOD),
            (r"so far, \ a theorem: \ true of any model, \ and testable only through the model chosen", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{efficient.free\_energy\_gaussian}")
        with self.voiceover(
            "Here's the free energy of a small model. <bookmark mark='a'/> A cause z has a standard normal prior, and "
            "a reading of two arrives with noise of standard deviation zero point five. <bookmark mark='b'/> Plot F "
            "against the mean of q, and it's a bowl. <bookmark mark='c'/> Its bottom is the exact posterior mean, "
            "one point six, and its height is the surprise, about two point six nats. <bookmark mark='d'/> So far "
            "this is a theorem. It's true of any model, and it can be tested only through the model that's chosen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(s), FadeIn(dot, scale=1.5))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def claims(self):
        chips_section(self, r"What the principle claims", [
            (r"Friston, \ 2010", r"any system that persists must keep its sensory states unsurprising, \ so it "
                                 r"must minimize free energy", MODEL),
            (r"perception", r"change beliefs ($q$) to fit the input: \ predictive coding is one implementation", PERSON),
            (r"action", r"change the input to fit the beliefs: \ active inference; \ desires as predictions of "
                        r"preferred states", GOOD),
            (r"the charge", r"with free choice of model and priors, \ any behaviour can be described as minimizing "
                            r"free energy; \ a principle that cannot fail is not tested by success", AUTH),
            (r"the reply", r"the principle is a framework, \ like Hamilton's; \ the specific models built with it "
                           r"make testable predictions", YOU),
        ], "Now the principle. <bookmark mark='a'/> Karl Friston argues that any system that persists must keep its "
           "sensory states unsurprising, so it must minimize free energy. <bookmark mark='b'/> In perception, it "
           "changes its beliefs to fit the input, and predictive coding is one implementation. "
           "<bookmark mark='c'/> In action, it changes the input to fit its beliefs. That's active inference, with "
           "desires recast as predictions of preferred states. <bookmark mark='d'/> The charge: with free choice of "
           "model and priors, any behaviour can be described as minimizing free energy, and a principle that can't "
           "fail isn't tested by its successes. <bookmark mark='e'/> The reply: the principle is a framework, like "
           "Hamilton's principle in physics, and the specific models built with it do make testable predictions.",
           tag=published_tag(r"Friston (2010)"), chip_w=3.4, text_w=8.6)
