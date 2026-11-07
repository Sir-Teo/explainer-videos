from __future__ import annotations

import numpy as np

from videos.stats.stats61.common import *  # noqa: F403


class Generative(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter nine. Generative models and transport: learning a map from noise to data.", 9,
                            r"Generative models", r"From noise to data", lit=(2017,))
        self.gans()
        self.penalty()
        self.flow_matching()
        self.pairing()
        self.samples()
        self.steps_chart()
        self.theory()

    def gans(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A generative model is a map that pushes a simple law, Gaussian noise, onto the data "
            "distribution: the transport problem, with the target known only through samples. <bookmark mark='b'/> Martin "
            "Arjovsky, Soumith Chintala and Léon Bottou's Wasserstein GAN, in 2017, trains the map to minimize W one to the "
            "data, using chapter two's Kantorovich–Rubinstein duality: a second network plays the one-Lipschitz witness. "
            "<bookmark mark='c'/> Unlike the original GAN's Jensen–Shannon divergence, W one gives useful gradients even "
            "when the model and the data do not overlap. <bookmark mark='d'/> But the critic is only roughly Lipschitz, and "
            "what is minimized is not quite W one, as Stanczuk and co-authors later argued.",
            [(r"\text{generator}", r":", r"G_\#N(0, I) \approx P_{\text{data}}", 40),
             (r"\text{WGAN}", r":", r"\min_G \max_{\mathrm{Lip}(f) \le 1} E f(X) - E f(G(Z))", 40),
             (r"\text{why}", r":", r"\text{gradients without overlap}", 40),
             (r"\text{but}", r":", r"\text{the critic is only roughly Lipschitz}", 40)],
            [r"a pushforward", r"Arjovsky, \ Chintala \& Bottou (2017)", r"unlike Jensen--Shannon", r"not quite $W_1$"],
            colors=[(1, FLOWC)])

    def flow_matching(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Modern image and audio generators use flows instead. <bookmark mark='b'/> Pair each noise "
            "point x zero with a data point x one, and join them by a straight line: x t equals one minus t times x zero plus "
            "t times x one. <bookmark mark='c'/> Along each line the velocity is x one minus x zero. Train a network v of x "
            "and t to predict it, by least squares: flow matching, from Yaron Lipman and co-authors, and rectified flow, "
            "from Xingchao Liu and co-authors, both in 2023. <bookmark mark='d'/> To sample, draw noise and integrate the "
            "learned velocity from time zero to one. The regression's answer, the conditional mean of the velocity, "
            "transports the interpolation marginals when the conditional-mean field and continuity equation have the required integrability, existence and uniqueness properties. A fitted field and finitely many Euler steps introduce further errors.",
            [(r"\text{paths}", r":", r"x_t = (1 - t)x_0 + t\,x_1", 40),
             (r"\text{loss}", r":", r"E\,\|v(x_t, t) - (x_1 - x_0)\|^2", 40),
             (r"v^*(x, t)", r"=", r"E[x_1 - x_0 \mid x_t = x]", 40),
             (r"\text{sample}", r":", r"\dot x = v(x, t), \ \ x(0) \sim N(0, I)", 40)],
            [r"interpolation", r"Lipman et al.; \ Liu et al. (2023)", r"a regression", r"an ODE"],
            colors=[(2, FLOWC)])

    def pairing(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Pairing affects the regression problem used to learn a flow. <bookmark mark='b'/> Independent endpoint pairs can yield a curved conditional-mean velocity flow, so a one-step Euler approximation can be poor. Neither curvature nor integration difficulty is universal. <bookmark mark='c'/> Minibatch transport pairing often shortens paths and reduces conflicts. Its coupling is not the population optimal map. <bookmark mark='d'/> The ideal population quadratic-optimal coupling gives straight displacement interpolation under regularity. Finite batches, kernel smoothing, network error and numerical integration need not preserve this exactly. The next picture measures one toy implementation.",
            [(r"\text{independent}", r":", r"\text{paths cross} \Rightarrow \text{curved flow}", 40),
             (r"\text{many steps}", r":", r"\text{to integrate a curved flow}", 40),
             (r"\text{OT pairing}", r":", r"\text{minibatch assignment}", 40),
             (r"\text{no crossing}", r":", r"\text{straight flow, \ few steps}", 40)],
            [r"rectified flow's motivation", r"the cost of curvature", r"Tong et al.; \ Pooladian et al.", r"Monge, \ 1781"],
            colors=[(0, NAIVEC2), (3, PLANC)])

    def samples(self):
        d = load("flow")
        Y = np.asarray(d["Y"])

        shown=np.vstack([Y,np.asarray(d["independent"]["one_step"]),np.asarray(d["ot"]["one_step"])])
        limit=float(np.ceil(np.max(np.abs(shown))*1.05))

        def panel(P, cx, title, col):
            A = axes([-limit, limit], [-limit, limit], x_length=4.4, y_length=4.4, xlabel=r"", ylabel=r"", center=[cx, 0.05, 0])
            ax = A.ax
            data = VGroup(*[Dot(ax.c2p(*y), radius=0.03, color=TGT, fill_opacity=0.45) for y in Y])
            gen = VGroup(*[Dot(ax.c2p(*p), radius=0.035, color=col, fill_opacity=0.85) for p in np.asarray(P)])
            t = label(title, font_size=24, color=col).next_to(A, UP, buff=0.2)
            return A, data, gen, t
        A1, D1, G1, T1 = panel(d["independent"]["one_step"], -3.4, r"independent pairs: \ one Euler step", NAIVEC2)
        A2, D2, G2, T2 = panel(d["ot"]["one_step"], 3.4, r"OT pairs: \ one Euler step", PLANC)
        key = side_groups([
            [(r"gold: \ Old Faithful, \ standardized; \ dots: \ 272 generated", GREY_A)],
            [(rf"$W_2$ to the data: \ independent {d['independent']['W']['1']:.2f}, \ OT {d['ot']['W']['1']:.2f}, \ noise {d['W_noise']:.2f}", WHITE)],
        ], width=9.0, pos=(-1.6, -2.95, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> A toy version, on Old Faithful, with the velocity learned by kernel regression instead of "
            f"a network. Fresh Gaussian noise, pushed by a single Euler step of each learned flow. <bookmark mark='b'/> With "
            f"independent pairs, one step sends every point toward the average of the data: the samples collapse into a "
            f"smear between the two clusters, at W two distance {say(d['independent']['W']['1'], 2)} from the data, worse than "
            f"the noise itself at {say(d['W_noise'], 2)}. <bookmark mark='c'/> With optimal-transport pairs, the same single "
            f"step lands the samples on both clusters, at distance {say(d['ot']['W']['1'], 2)}."
        ) as vo:
            self.play(FadeIn(A1), FadeIn(A2), FadeIn(D1), FadeIn(D2), FadeIn(T1), FadeIn(T2), FadeIn(key[0]),
                      FadeIn(museum_tag(r"Old Faithful; \ the flows are simulated")))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(G1, lag_ratio=0.005), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(G2, lag_ratio=0.005), FadeIn(key[1]), run_time=1.5)
        self.clear_scene()

    def steps_chart(self):
        d = load("flow")
        steps = [1, 2, 5, 20]
        xs = np.log10(steps)
        wi = [d["independent"]["W"][str(s)] for s in steps]
        wo = [d["ot"]["W"][str(s)] for s in steps]
        A = axes([-0.05, 1.35], [0.25, 1.15], x_length=7.4, y_length=4.4, xlabel=r"Euler steps (log scale)", ylabel=r"$W_2$ to the data",
                 xticks=list(xs), xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0.4, 0.6, 0.8, 1.0], center=[-2.5, 0.2, 0])
        ax = A.ax
        li = VGroup(polyline(ax, xs, wi, NAIVEC2, 3.5), *[Dot(ax.c2p(a, b), radius=0.07, color=NAIVEC2) for a, b in zip(xs, wi)])
        lo = VGroup(polyline(ax, xs, wo, PLANC, 3.5), *[Dot(ax.c2p(a, b), radius=0.07, color=PLANC) for a, b in zip(xs, wo)])
        noise = DashedLine(ax.c2p(-0.05, d["W_noise"]), ax.c2p(1.35, d["W_noise"]), color=GREY_B, stroke_width=2)
        side = side_groups([
            [(r"grey: \ the noise itself", GREY_B)],
            [(r"red: \ independent pairs", NAIVEC2), (rf"{wi[0]:.2f} $\to$ {wi[-1]:.2f} \ over 1 to 20 steps", NAIVEC2)],
            [(r"green: \ OT pairs", PLANC), (rf"{wo[0]:.2f} at one step", PLANC)],
            [(rf"straightness: \ {d['independent']['straight']:.2f} \ vs \ {d['ot']['straight']:.3f}", GREY_A), (r"(displacement / path length)", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The same comparison over the number of steps, averaged over five fresh-noise draws conditional on one fitted velocity field. The distance is to the training empirical law, not a held-out population distribution; the saved Monte Carlo errors only describe these noise draws. The grey "
            f"line is the noise. <bookmark mark='b'/> The independent flow improves from {say(wi[0], 2)} at one step to "
            f"{say(wi[-1], 2)} at twenty: it needs the steps, because it curves. <bookmark mark='c'/> The transport flow is at "
            f"{say(wo[0], 2)} from the first step and stays there. <bookmark mark='d'/> Measured directly, the ratio of each "
            f"particle's displacement to its path length is {say(d['independent']['straight'], 2)} for the independent flow and "
            f"{say(d['ot']['straight'], 3)} for the transport flow: nearly straight in this toy fitted field. This is not a population-optimal-transport theorem for arbitrary learned flows."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated, \ 5 noise draws")))
            vo.wait_until("a")
            self.play(Create(noise), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(li), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lo), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def theory(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What statistics can say about these models is just beginning. <bookmark mark='b'/> Diffusion "
            "models, a stochastic cousin of flow matching, estimate the score of the noised data; Kazusato Oko, Shunta Akiyama and Taiji Suzuki, "
            "and Sitan Chen, Sinho Chewi and co-authors, showed in 2023 that the score can be estimated at minimax rates "
            "for smooth densities, and that with a well-estimated score the samples are close to the data law. <bookmark mark='c'/> The "
            "transport view explains why straight, non-crossing paths are cheaper to integrate. <bookmark mark='d'/> The "
            "deep-learning side of this story, with the networks themselves, is *AI, Built* Part twenty-one; Part sixty-four "
            "returns to what such models mean for statistics.",
            [(r"\text{diffusion}", r":", r"\text{estimate the score } \nabla\log p_t", 40),
             (r"\text{guarantees}", r":", r"\text{good score} \Rightarrow \text{good samples}", 40),
             (r"\text{transport}", r":", r"\text{straight paths, \ cheap integration}", 40),
             (r"\text{more}", r":", r"\textit{AI, Built} \text{ Part 21; \ Part 64}", 40)],
            [r"Ho et al.; \ Song et al.", r"Oko et al.; \ Chen et al. (2023)", r"chapter 9's lesson", r"cross-references"],
            colors=[(1, PLANC)])

    def penalty(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Practical WGAN critics approximate a constrained optimization problem. <bookmark mark='b'/> Weight clipping is a crude constraint on network parameters. <bookmark mark='c'/> For a differentiable optimal one-Lipschitz critic, saturated transport segments motivate a unit-gradient condition. Penalizing gradients on random interpolations between arbitrary real and generated points is a heuristic: these are generally not optimal transport partners, and the penalty does not enforce a global Lipschitz bound. <bookmark mark='d'/> Spectral normalization controls layer operator norms; a network bound must also account for activations, architecture and numerical norm estimation.",
            [(r"\text{clipping}", r":", r"|w| \le c: \ \text{crude}", 40),
             (r"\text{the fact}", r":", r"\|\nabla f^*\| = 1 \text{ along transport lines}", 40),
             (r"\text{penalty}", r":", r"\lambda\,E\big(\|\nabla f(\hat x)\| - 1\big)^2", 40),
             (r"\text{spectral norm}", r":", r"\text{each layer 1-Lipschitz}", 40)],
            [r"Arjovsky et al.", r"from chapter 1's duality", r"Gulrajani et al. (2017)", r"Miyato et al. (2018)"],
            colors=[(2, FLOWC)])
