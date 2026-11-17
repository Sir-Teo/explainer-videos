from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403

NAMES = {"ev": r"expected value", "eu": r"expected utility", "pt_noweight": r"value curve only",
         "cpt": r"prospect theory"}


class Thirteen(VoiceoverScene):
    def construct(self):
        self.card()
        self.dataset()
        self.models()
        self.scatter_()
        self.curves_()

    def card(self):
        card = chapter_card(5, r"Thirteen thousand gambles", r"Does the theory predict choices it has not seen?",
                            lit={2017: r"Erev et al.", 2021: r"Peterson et al."},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter five. Thirteen thousand gambles."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def dataset(self):
        d = load("c13k")
        head = heading(r"choices13k")
        box = RoundedRectangle(corner_radius=0.12, width=5.8, height=2.6, stroke_color=DATA, stroke_width=2,
                               fill_color=BLACK, fill_opacity=0.5).move_to([-3.4, 0.6, 0])
        ex = VGroup(label(r"one problem, \ as shown", font_size=21, color=GREY_A),
                    label(r"A: \ 26 at 0.95, \ $-$1 at 0.05", font_size=24, color=SURE),
                    label(r"B: \ 21 at 0.95, \ 23 at 0.05", font_size=24, color=RISKY),
                    label(r"five choices each, \ with or without feedback", font_size=19, color=GREY_B)).arrange(
            DOWN, buff=0.2).move_to(box)
        rows = rows_of([
            (rf"Peterson, \ Bourgin, \ Agrawal, \ Reichman and Griffiths, \ 2021: \ {num(d['n_unique'])} choice "
             r"problems, \ each answered by about 16 people online", WHITE),
            (r"the format of Erev and colleagues' choice prediction competitions: \ two-outcome A, \ B with a "
             r"lottery inside, \ some with probabilities hidden, \ most with feedback", GREY_A),
            (rf"here: \ the {num(d['n_problems'])} problems shown with full descriptions and no feedback, \ "
             r"the cleanest test of a theory of described risk", DATA),
            (r"the target: \ the share of people choosing B, \ problem by problem", RISKY),
        ], 6.0, 22, 0.3).move_to([3.4, 0.2, 0])
        tag = historical_tag(r"choices13k: \ Peterson et al.\ (2021), \ github.com/jcpeterson/choices13k")
        n_all, n_desc = f"{d['n_unique']:,}", f"{d['n_problems']:,}"
        with self.voiceover(
            "Kahneman and Tversky built prospect theory on a few dozen problems. Here is a test on many more. "
            "<bookmark mark='a'/> In 2021 Joshua Peterson, David Bourgin, Mayank Agrawal, Daniel Reichman and Tom "
            f"Griffiths published choices thirteen k: {n_all} choice problems, each "
            "answered by about sixteen people online. <bookmark mark='b'/> The problems follow the format of the "
            "choice prediction competitions that Ido Erev and colleagues ran: option A has two outcomes, option B a "
            "sure part and a lottery, some probabilities are hidden, and most problems were played with feedback "
            "after each choice. <bookmark mark='c'/> For a theory of described risk the cleanest test is the "
            f"{n_desc} problems shown with full descriptions and no feedback, so "
            "those are what we'll use. Here's one. <bookmark mark='d'/> What we predict is the share of people "
            "choosing B, problem by problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows[:3]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(box), FadeIn(ex))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def models(self):
        d = load("c13k")
        head = heading(r"Four models, \ tested on problems they have not seen")
        order = ["ev", "eu", "pt_noweight", "cpt"]
        cols = [NORM, NORM, MODEL, MODEL]
        A = axes([-0.5, 4.5], [0, 0.045], x_length=6.4, y_length=3.8, xticks=None, yticks=[0, 0.01, 0.02, 0.03, 0.04],
                 yfmt=lambda v: f"{v:.2f}", ylabel=r"mean squared error, \ 10-fold cross-validated",
                 center=[-3.0, -0.2, 0], font_size=16)
        vals = [d["cv"][m] for m in order] + [d["cv"]["mean"]]
        bs = VGroup(*[bars(A.ax, [k], [v], c, width=0.6) for k, (v, c) in enumerate(zip(vals, cols + [GREY_D]))])
        labs = VGroup()
        for k, (m, v) in enumerate(zip(order + ["mean"], vals)):
            txt = NAMES.get(m, r"no model: \ the average")
            labs.add(wrapped_label(txt, 1.2, 15, GREY_A).next_to(A.ax.c2p(k, 0), DOWN, buff=0.15))
            labs.add(label(f"{v:.4f}", font_size=15, color=WHITE).next_to(A.ax.c2p(k, v), UP, buff=0.08))
        p = d["params"]["cpt"]
        r2 = d["r2"]
        rows = rows_of([
            (r"each model turns values into choice shares by a logistic rule, \ fitted by least squares", GREY_A),
            (rf"expected value explains {100 * r2['ev']:.0f}\% of the variance across problems; \ a concave "
             rf"utility, \ {100 * r2['eu']:.0f}\%", NORM),
            (rf"prospect theory's weighting function is what pays: \ {100 * r2['cpt']:.0f}\%, \ and it holds up out "
             r"of sample", MODEL),
            (rf"fitted: \ $\alpha = {p['alpha']:.2f}$, \ $\lambda = {p['lam']:.2f}$, \ $\gamma = {p['gamma']:.2f}$, "
             rf"\ $\delta = {p['delta']:.2f}$", RISKY),
        ], 5.6, 22, 0.3).move_to([3.6, 0.0, 0])
        tag = psyche_tag(r"\texttt{choice.fit\_model}, \ \texttt{cv\_models}; \ open data: \ choices13k")
        assert d["cv"]["cpt"] < d["cv"]["pt_noweight"] < d["cv"]["ev"] < d["cv"]["mean"]
        with self.voiceover(
            "Four models. <bookmark mark='a'/> Each turns the values of A and B into a predicted share choosing B "
            "through a logistic rule, and each is fitted by least squares, the way the choice prediction "
            "competitions score. We score them on problems held out of the fit, ten times over, so a model can't "
            "win by memorizing. <bookmark mark='b'/> Expected value alone explains about "
            f"{100 * r2['ev']:.0f} percent of the variation between problems; a concave utility, about "
            f"{100 * r2['eu']:.0f}. A value curve with a kink at zero but no probability weighting adds almost "
            f"nothing. <bookmark mark='c'/> Add the weighting function, and it rises to {100 * r2['cpt']:.0f} "
            "percent, with the same gain out of sample. The bent probabilities are doing the work. "
            "<bookmark mark='d'/> The fitted values are close to the 1992 ones in curvature and in the weighting of "
            f"gains, but loss aversion is only {p['lam']:.2f}, barely above one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bs[4]), FadeIn(labs[8:]), FadeIn(bs[0]), FadeIn(bs[1]), FadeIn(labs[:4]),
                      FadeIn(rows[1]))
            self.play(FadeIn(bs[2]), FadeIn(labs[4:6]))
            vo.wait_until("c")
            self.play(FadeIn(bs[3]), FadeIn(labs[6:8]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def scatter_(self):
        d = load("c13k")
        head = heading(r"Predicted against observed, \ problem by problem")
        y = d["y"]
        idx = np.arange(0, len(y), 3)  # every third problem, by rule, to keep the picture readable
        def panel(pred, col, title, center):
            A = axes([0, 1], [0, 1], x_length=4.2, y_length=4.2, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                     xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"predicted share choosing B",
                     ylabel=r"observed", center=center, font_size=16)
            diag = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(1, 1), color=GREY_B, stroke_width=2)
            dots = scatter(A.ax, pred[idx], y[idx], col, 0.025, 0.7)
            t = label(title, font_size=22, color=col).next_to(A, UP, buff=0.15)
            return VGroup(A, diag, t), dots
        g1, d1 = panel(d["pred_ev"], NORM, rf"expected value: \ $R^2 = {d['r2']['ev']:.2f}$", [-3.4, -0.6, 0])
        g2, d2 = panel(d["pred_cpt"], MODEL, rf"prospect theory: \ $R^2 = {d['r2']['cpt']:.2f}$", [3.4, -0.6, 0])
        tag = psyche_tag(rf"every third of the {num(d['n_problems'])} described problems; \ open data: \ choices13k")
        with self.voiceover(
            "Here's what that difference looks like. <bookmark mark='a'/> Each dot is a problem: the share of "
            "people who chose B, against the share a model predicts. On the left, expected value. Its predictions "
            "bunch in the middle, and many problems that people decided almost unanimously look like coin flips to "
            "it. <bookmark mark='b'/> On the right, prospect theory. The cloud tightens along the diagonal. It's "
            "far from perfect, and the misses aren't random: Peterson and colleagues found that a neural network "
            "trained on these data could do better still, and then worked out what it had learned, which we'll come "
            "back to at the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(d1, lag_ratio=0.002), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(d2, lag_ratio=0.002), run_time=2)
        self.clear_scene()

    def curves_(self):
        d = load("c13k")
        head = heading(r"The curves the data chose")
        x = d["x"]
        def norm(v):
            return v / float(np.interp(100.0, x, v))
        A = axes([-100, 100], [-2.4, 1.2], x_length=5.4, y_length=3.3, xticks=[-100, 0, 100], yticks=[-2, -1, 0, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"outcome",
                 ylabel=r"value, \ scaled so $v(100) = 1$", center=[-3.4, 0.05, 0], font_size=16)
        v92 = curve(A.ax, x, norm(d["v_92"]), GREY_B, 3)
        vf = curve(A.ax, x, norm(d["v_fit"]), MODEL, 4)
        B = axes([0, 1], [0, 1], x_length=3.3, y_length=3.3, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"$p$", ylabel=r"$w(p)$, \ gains",
                 center=[3.0, 0.05, 0], font_size=16)
        dg = DashedLine(B.ax.c2p(0, 0), B.ax.c2p(1, 1), color=GREY_D, stroke_width=2)
        w92 = curve(B.ax, d["p"], d["w_92_gain"], GREY_B, 3)
        wf = curve(B.ax, d["p"], d["w_fit_gain"], MODEL, 4)
        wfb = curve(B.ax, d["p"], d["w_fb_gain"], RISKY, 3)
        key = legend([(GREY_B, r"1992 values"), (MODEL, r"fitted, \ described"),
                      (RISKY, r"fitted, \ with feedback")], font_size=16).move_to(B.ax.c2p(0.32, 0.86))
        p, pf = d["params"]["cpt"], d["fb_params"]
        foot = rows_of([
            (rf"loss aversion at these small stakes: \ $\lambda = {p['lam']:.2f}$ described, \ "
             rf"${pf['lam']:.2f}$ with feedback", LOSS),
            (rf"with feedback the weights straighten: \ $\gamma$ {p['gamma']:.2f} to {pf['gamma']:.2f}, \ "
             rf"$\delta$ {p['delta']:.2f} to {pf['delta']:.2f}", RISKY),
        ], 12.4, 22, 0.2).to_edge(DOWN, buff=0.55)
        tag = psyche_tag(r"\texttt{choice.fit\_model}; \ open data: \ choices13k")
        with self.voiceover(
            "And here are the curves the data chose. <bookmark mark='a'/> On the left the value function, scaled so "
            "that a gain of a hundred is worth one. In grey, the 1992 version; in purple, the one fitted to these "
            "choices. The curvature is similar, but the loss branch is nearly a mirror image of the gain branch. "
            f"Loss aversion here is {p['lam']:.2f}. <bookmark mark='b'/> On the right, the weighting of gains: an "
            "inverse S again, a little milder than in 1992. <bookmark mark='c'/> Fit the same model to the problems "
            "played with feedback, where people saw what each choice paid, and the weights straighten, especially "
            f"for losses, and loss aversion drops below one, to {pf['lam']:.2f}. <bookmark mark='d'/> So this is the "
            "first appearance of a theme for the rest of the part: some of prospect theory replicates at scale, the "
            "bent probabilities above all, and some depends on the stakes and on how choices are made. Here the "
            "stakes are small, and losses barely loom."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B), FadeIn(dg))
            vo.wait_until("a")
            self.play(Create(v92), Create(vf), FadeIn(key[0]), FadeIn(key[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(w92), Create(wf), run_time=2)
            vo.wait_until("c")
            self.play(Create(wfb), FadeIn(key[2]), FadeIn(foot))
            vo.wait_until("d")
            self.play(Indicate(foot[0], color=LOSS))
        self.clear_scene()
