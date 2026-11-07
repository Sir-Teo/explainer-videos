from __future__ import annotations

import numpy as np

from videos.stats.stats32.common import *  # noqa: F403


class Zoo(VoiceoverScene):
    def construct(self):
        self.card()
        self.enet()
        self.enet_paths()
        self.group()
        self.fused_def()
        self.fused_plot()
        self.adaptive()
        self.nonconvex()
        self.rules()
        self.recovery()

    def card(self):
        card = chapter_card(6, r"The penalty zoo", r"Changing the corner to fit the problem", lit=(2001, 2005), part=PART)
        with self.voiceover("Chapter six. The penalty zoo."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def enet(self):
        rows = [
            cmath(r"\text{lasso, \ correlated } x_1 \approx x_2", r":", r"\text{picks one, \ almost arbitrarily}", font_size=28),
            cmath(r"\mathrm{pen}(\beta)", r"=", r"\alpha\|\beta\|_1 + \tfrac{1 - \alpha}{2}\|\beta\|_2^2", font_size=32),
            cmath(r"x_1 = x_2", r"\Rightarrow", r"\hat\beta_1 = \hat\beta_2 \ \ (\alpha < 1)", font_size=32),
            cmath(r"p > n", r":", r"\text{can select more than } n \text{ variables}", font_size=30),
        ]
        rows[1][-1].set_color(ENET)
        whys = [why(r"unstable selection"), why(r"Zou \& Hastie (2005): \ the elastic net"),
                why(r"the grouping effect"), why(r"the lasso cannot")]
        with self.voiceover(
            "<bookmark mark='a'/> First problem: when two predictors are nearly identical, the lasso tends to pick one and "
            "drop the other, and which one it picks can flip with a small change in the data. <bookmark mark='b'/> Hui Zou "
            "and Trevor Hastie's elastic net of 2005 mixes the lasso penalty with a little ridge. <bookmark mark='c'/> The "
            "ridge part is strictly convex, so identical predictors get identical coefficients: the grouping effect. "
            "<bookmark mark='d'/> And unlike the lasso, the elastic net can select more variables than there are "
            "observations, which matters for genes that act in correlated pathways."
        ) as vo:
            intro=label('Elastic net adds a strictly convex grouping penalty',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def enet_paths(self):
        d = load("zoo")
        lams = np.asarray(d["lams"])
        L, E = np.asarray(d["lasso"]), np.asarray(d["enet"])
        x = -np.log10(lams / lams[0])
        cols = [LASSO, S.TREAT, S.KEPT, GREY_C, GREY_C, GREY_C]
        A1 = axes([0, 2.6], [-0.2, 1.1], x_length=5.4, y_length=3.8, xlabel=r"$-\log_{10}(\lambda/\lambda_{\max})$",
                  ylabel=r"lasso", xticks=[0, 1, 2], yticks=[0, 0.5, 1], center=[-3.3, 0.4, 0])
        A2 = axes([0, 2.6], [-0.2, 1.1], x_length=5.4, y_length=3.8, xlabel=r"$-\log_{10}(\lambda/\lambda_{\max})$",
                  ylabel=r"elastic net, \ $\alpha = 0.5$", xticks=[0, 1, 2], yticks=[0, 0.5, 1], center=[3.3, 0.4, 0])
        l1 = VGroup(*[polyline(A1.ax, x, L[:, j], cols[j], 3 if j < 3 else 1.5) for j in range(6)])
        l2 = VGroup(*[polyline(A2.ax, x, E[:, j], cols[j], 3 if j < 3 else 1.5) for j in range(6)])
        foot = fit_rows(VGroup(
            label(rf"three near-copies of one signal \ (correlation {d['corr']:.2f}), \ plus three noise variables", font_size=22),
            label(r"the lasso takes two of the copies in turn and leaves the third at zero for most of the path", font_size=22, color=LASSO),
            label(r"the elastic net brings all three in together and shares the effect", font_size=22, color=ENET),
        ), 12.0, 0.2, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Three near-copies of one signal, correlated point nine six, and three pure noise "
            "variables. <bookmark mark='b'/> Along the lasso path, one copy enters first and takes most of the "
            "effect, a second follows, and the third stays at zero for most of the path. <bookmark mark='c'/> Along "
            "the elastic-net path all three enter together and share the effect almost equally, a more evenly shared "
            "association. It does not identify separate causal effects of near-duplicate predictors."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A1), FadeIn(A2))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(foot[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(l2), FadeIn(foot[2]), run_time=2.5)
        self.clear_scene()

    def group(self):
        rows = [
            cmath(r"\mathrm{pen}(\beta)", r"=", r"\textstyle\sum_g \sqrt{p_g}\, \|\beta_g\|_2", font_size=32),
            cmath(r"\text{update}", r":", r"\beta_g \leftarrow (1 - \lambda\sqrt{p_g}/\|z_g\|)_+ \, z_g", font_size=30),
            cmath(r"\text{selects}", r":", r"\text{whole groups: \ a factor's dummies, \ a spline's basis}", font_size=30),
            cmath(r"\text{sparse group lasso}", r":", r"\text{groups, \ and sparsity within them}", font_size=30),
        ]
        rows[1][-1].set_color(LASSO)
        whys = [why(r"Yuan \& Lin (2006): \ the group lasso"), why(r"orthonormalized within-group coordinates"),
                why(r"all in or all out"), why(r"Simon et al. (2013)")]
        with self.voiceover(
            "<bookmark mark='a'/> Second problem: some variables only make sense together, like the dummy variables "
            "of one categorical factor or the basis functions of one spline. Ming Yuan and Yi Lin's group lasso "
            "penalizes the Euclidean length of each group's coefficient vector, without squaring it. <bookmark "
            "mark='b'/> In coordinates with each group orthonormalized, the block update is a soft threshold: shrink "
            "the whole group's vector towards zero, and set it exactly to zero if it is short enough. <bookmark "
            "mark='c'/> So whole groups enter or leave together. <bookmark mark='d'/> Add an ordinary lasso term and "
            "you also get sparsity within the selected groups."
        ) as vo:
            intro=label('Group thresholding uses orthonormalized within-group coordinates',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fused_def(self):
        rows = [
            cmath(r"\min_\theta", r"", r"\tfrac12\textstyle\sum_i (y_i - \theta_i)^2 + \lambda \sum_i |\theta_{i+1} - \theta_i|", font_size=30),
            cmath(r"\text{sparse in}", r":", r"\text{the differences: \ a piecewise-constant fit}", font_size=30),
            cmath(r"\text{in two dimensions}", r":", r"\text{total variation: \ the hook's phantom}", font_size=30),
            cmath(r"\text{computed by}", r":", r"\text{ADMM \ (Part 21), \ or exactly by dynamic programming}", font_size=28),
        ]
        rows[0][-1].set_color(ENET)
        whys = [why(r"Tibshirani et al. (2005): \ the fused lasso"), why(r"jumps are rare"),
                why(r"Rudin, \ Osher \& Fatemi (1992)"), why(r"Johnson (2013)")]
        with self.voiceover(
            "<bookmark mark='a'/> Third: sparsity need not be in the coefficients themselves. The fused lasso "
            "penalizes the absolute differences between neighbouring values. <bookmark mark='b'/> The solution is "
            "piecewise constant, with only a few jumps. <bookmark mark='c'/> Two-dimensional total variation is the "
            "analogous gradient penalty. The hook uses the isotropic sum of gradient magnitudes, rather than a "
            "separate absolute penalty for each directional difference, introduced for image denoising by Rudin, "
            "Osher and Fatemi in 1992. <bookmark mark='d'/> It is computed by Part 21's ADMM, or exactly, in one "
            "dimension, by dynamic programming."
        ) as vo:
            intro=label('Difference penalties encourage piecewise-constant fitting',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fused_plot(self):
        d = load("zoo")["fused"]
        y, tr, fit = np.asarray(d["y"]), np.asarray(d["truth"]), np.asarray(d["fit"])
        t = np.arange(len(y))
        A = axes([0, 200], [-3.6, 4.0], x_length=8.2, y_length=4.4, xlabel=r"position", ylabel=r"signal",
                 xticks=[0, 50, 100, 150, 200], yticks=[-2, 0, 2], center=[-1.6, 0.3, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.03, color=GREY_B) for a, b in zip(t, y)])
        truth = polyline(ax, t, tr, SPIKE, 3)
        fl = polyline(ax, t, fit, ENET, 3.5)
        rows = fit_rows(VGroup(
            label(r"200 noisy readings \ (SD 0.6)", font_size=22, color=GREY_B),
            label(r"gold: \ the true steps", font_size=22, color=SPIKE),
            label(r"orange: \ fused lasso, \ $\lambda = 3$", font_size=22, color=ENET),
            label(rf"RMSE {d['rmse_fit']:.2f} \ vs \ {d['rmse_raw']:.2f} raw", font_size=22, color=HIT),
        ), 3.4, 0.42, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two hundred noisy readings of a signal with three steps, like copy-number changes along a "
            "chromosome. <bookmark mark='b'/> The true steps in gold. <bookmark mark='c'/> The fused lasso finds the jumps "
            "and flattens the noise between them, <bookmark mark='d'/> cutting the error from point five five to point two "
            "three. Its plateaus are slightly shrunk towards their neighbours, the usual price of an absolute-value penalty."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(fl), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def adaptive(self):
        rows = [
            cmath(r"\mathrm{pen}(\beta)", r"=", r"\textstyle\sum_j w_j |\beta_j|, \ \ w_j = 1/|\tilde\beta_j|^\gamma", font_size=30),
            cmath(r"\text{large } \tilde\beta_j", r":", r"\text{small penalty: \ little bias}", font_size=30),
            cmath(r"\text{small } \tilde\beta_j", r":", r"\text{large penalty: \ removed}", font_size=30),
            cmath(r"\text{oracle property}", r":", r"\text{selects the true support, \ estimates as if it were known}", font_size=28),
        ]
        rows[0][-1].set_color(LASSO)
        whys = [why(r"Zou (2006): \ the adaptive lasso"), why(r"trust strong signals"), why(r"distrust weak ones"),
                why(r"asymptotically, \ under conditions")]
        with self.voiceover(
            "<bookmark mark='a'/> Fourth problem: the lasso's bias on large effects. Hui Zou's adaptive lasso weights each "
            "coefficient's penalty by the inverse of a first-stage estimate. <bookmark mark='b'/> Variables that looked "
            "strong are barely penalized, so their estimates are nearly unbiased. <bookmark mark='c'/> Variables that looked "
            "weak are penalized heavily and removed. <bookmark mark='d'/> Zou proved an oracle property: asymptotically it "
            "selects exactly the true variables and estimates them as efficiently as if the true model were known. The "
            "asymptotics hide a lot, as chapter ten will show."
        ) as vo:
            intro=label('Adaptive weights separate initial screening from later shrinkage',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def nonconvex(self):
        rows = [
            cmath(r"\text{SCAD}", r":", r"\lambda|\beta| \text{ near } 0, \ \text{a quadratic bend, \ flat beyond } a\lambda", font_size=28),
            cmath(r"\text{MCP}", r":", r"\lambda|\beta| - \beta^2/(2\gamma) \text{ up to } \gamma\lambda, \ \text{then flat}", font_size=28),
            cmath(r"\text{both}", r":", r"\text{zero large-signal penalty derivative; continuous scalar rules}", font_size=30),
            cmath(r"\text{price}", r":", r"\text{not convex: \ local minima, \ but CD works well}", font_size=30),
        ]
        rows[2][-1].set_color(NCV)
        whys = [why(r"Fan \& Li (2001)"), why(r"Zhang (2010)"), why(r"Fan and Li's three desiderata"), why(r"Breheny \& Huang (2011)")]
        with self.voiceover(
            "<bookmark mark='a'/> Or bend the penalty itself. Jianqing Fan and Runze Li's SCAD of 2001 behaves like "
            "the lasso near zero, bends quadratically, and becomes flat beyond a times lambda. <bookmark mark='b'/> "
            "Cun-Hui Zhang's minimax concave penalty, MCP, does the same more simply. <bookmark mark='c'/> Flat means"
            " zero penalty derivative beyond the threshold, reducing shrinkage of large estimates. This is not a "
            "guarantee of finite-sample unbiasedness after selection, while small ones are still set to zero, and the"
            " thresholding rule stays continuous: Fan and Li's three requirements. <bookmark mark='d'/> The price is "
            "convexity: there can be local minima. In practice coordinate descent from the lasso solution works well,"
            " as Patrick Breheny and Jian Huang showed."
        ) as vo:
            intro=label('Flat penalty derivatives can reduce large-estimate shrinkage',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rules(self):
        z = np.linspace(-6, 6, 601)
        lam = 1.0
        A = axes([-6, 6], [-6, 6], x_length=5.6, y_length=5.0, xlabel=r"least-squares estimate $z$", ylabel=r"penalized estimate",
                 xticks=[-6, -3, 0, 3, 6], yticks=[-6, -3, 0, 3, 6], center=[-2.6, 0.0, 0])
        ax = A.ax
        idl = DashedLine(ax.c2p(-6, -6), ax.c2p(6, 6), color=GREY_D, stroke_width=1.5)
        soft = curve(ax, z, np.sign(z) * np.maximum(np.abs(z) - lam, 0), LASSO, 3)
        scad = curve(ax, z, np.where(np.abs(z) <= 2 * lam, np.sign(z) * np.maximum(np.abs(z) - lam, 0),
                                     np.where(np.abs(z) <= 3.7 * lam, ((2.7) * z - np.sign(z) * 3.7 * lam) / 1.7, z)), SPIKE, 3)
        mcp = curve(ax, z, np.where(np.abs(z) <= 3 * lam, np.sign(z) * np.maximum(np.abs(z) - lam, 0) / (1 - 1 / 3), z), NCV, 3)
        rows = fit_rows(VGroup(
            label(r"thresholding rules, \ $\lambda = 1$", font_size=22),
            label(r"lasso: \ biased by $\lambda$ forever", font_size=22, color=LASSO),
            label(r"SCAD \ ($a = 3.7$): \ rejoins the identity at $3.7$", font_size=22, color=SPIKE),
            label(r"MCP \ ($\gamma = 3$): \ rejoins at $3$", font_size=22, color=NCV),
        ), 4.4, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Their thresholding rules for an orthonormal design. <bookmark mark='b'/> The lasso's soft "
            "threshold stays a distance lambda below the diagonal forever. <bookmark mark='c'/> SCAD starts as the soft "
            "threshold, then climbs back to the diagonal, which it meets at three point seven. <bookmark mark='d'/> MCP "
            "climbs more steeply and meets the diagonal at three. Large estimates are left alone."
        ) as vo:
            self.play(FadeIn(A), Create(idl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(soft), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(scad), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(mcp), FadeIn(rows[3]))
        self.clear_scene()

    def recovery(self):
        d = load("zoo")
        sp = d["support"]
        hdr = [r"\textbf{penalty}", r"\textbf{true found (of 8)}", r"\textbf{false included}", r"\textbf{exact support}", r"\textbf{$\|\hat\beta - \beta\|^2$}"]
        names = [("lasso", r"lasso", LASSO), ("adaptive", r"adaptive lasso", S.KEPT), ("scad", r"SCAD", SPIKE), ("mcp", r"MCP", NCV)]
        body = [[nm, f"{sp[k]['tp']:.2f}", f"{sp[k]['fp']:.2f}", f"{100 * sp[k]['exact']:.1f}\\%", f"{sp[k]['err']:.2f}"] for k, nm, _ in names]
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.7, row_buff=0.32, colors=[GREY_A] + [c for _, _, c in names])
        tb.move_to([0, 1.0, 0])
        foot = fit_rows(VGroup(
            label(rf"{d['reps']} data sets: \ $n = 100$, \ $p = 200$, \ 8 true effects from 0.5 to 1, \ correlated columns", font_size=22),
            label(r"MCP: \ a third of the time exactly right, \ with fewer than half a false variable on average", font_size=22, color=NCV),
            label(r"the lasso keeps nearly three false variables to protect its shrunken true ones", font_size=22, color=LASSO),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A comparison: two hundred data sets, a hundred observations, two hundred correlated"
            " predictors, eight true effects between a half and one, with a common base lambda for lasso, SCAD and "
            "MCP; the adaptive lasso uses a separately rescaled weighted penalty. This is an illustrative tuning "
            "comparison, not an optimally matched contest. <bookmark mark='b'/> All four find about seven of the "
            "eight true variables. The lasso also includes nearly three false ones, and gets the support exactly "
            "right three percent of the time. The adaptive lasso cuts the estimation error by three quarters. "
            "<bookmark mark='c'/> MCP includes fewer than half a false variable on average and is exactly right a "
            "third of the time. Bending the penalty separates selection from shrinkage."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), FadeIn(foot[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
