from __future__ import annotations

import numpy as np

from videos.stats.stats32.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.mri()
        self.phantom()
        self.zero_fill()
        self.recover()
        self.why()
        self.count()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1974, 2006)).to_edge(UP, buff=0.35)
        hc = history_card(2004, r"Emmanuel Cand\`es, \ Caltech",
                          r"Reconstructing a test image from a small fraction of its Fourier coefficients, \ he found "
                          r"the error was zero: \ not small, \ zero. \ He assumed a bug. \ It was a theorem, \ proved with "
                          r"Justin Romberg and Terence Tao (2006)", color=SPIKE, width=11.0, font_size=23).move_to([0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(r"16{,}384 unknown pixels; \ about 3{,}400 measurements", font_size=24),
            label(r"few sampled Fourier coefficients: this example recovers to numerical tolerance", font_size=24, color=SPIKE),
        ), 12.0, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2004 Emmanuel Candès was experimenting with a standard test image from medical "
            "imaging. He threw away most of its Fourier coefficients and asked a computer to rebuild the image from "
            "the few that were left, with a particular convex optimization. The error came back zero: not small, "
            "zero. He assumed there was a bug. <bookmark mark='b'/> There was none. With Justin Romberg and Terence "
            "Tao he developed recovery theory under specified measurement and sparsity conditions. This deterministic"
            " radial-mask example is a numerical demonstration, not a universal corollary of a random-measurement "
            "theorem. <bookmark mark='c'/> Sixteen thousand unknowns, about three thousand four hundred equations, "
            "and an exact answer. This part explains how that is possible."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def mri(self):
        rows = fit_rows(VGroup(
            label(r"an MRI scanner does not take a photograph", font_size=26),
            label(r"it measures the image's Fourier coefficients, \ one line of `k-space' at a time", font_size=26, color=SPIKE),
            label(r"each line costs time in the scanner: \ minutes for a child holding still", font_size=26),
            label(r"so: \ how few coefficients can we get away with?", font_size=26, color=LASSO),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The setting matters. A magnetic resonance scanner does not take a photograph. "
            "<bookmark mark='b'/> It measures the Fourier coefficients of the image, the amplitudes of waves of every "
            "frequency and direction, one line of what radiologists call k-space at a time. <bookmark mark='c'/> Every "
            "line costs time, and time in a scanner is expensive, and hard for a child who must hold still. "
            "<bookmark mark='d'/> So the practical question is: how few Fourier coefficients can we measure and still get "
            "the image?"
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def phantom(self):
        d = load("phantom")
        truth, mask = np.asarray(d["truth"]), np.asarray(d["mask"])
        p1 = PhantomPanel(truth, size=3.6, caption=r"the Shepp--Logan phantom, \ $128 \times 128$", lo=0, hi=1, center=[-3.2, 0.4, 0])
        p2 = PhantomPanel(mask, size=3.6, caption=rf"k-space: \ 22 radial lines, \ {100 * d['fraction']:.0f}\% measured",
                          lo=0, hi=1, tint=SPIKE, center=[2.4, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The test image is the Shepp–Logan phantom of 1974, a cartoon of a cross-section of the "
            "head: ellipses for the skull, the brain, and a few small features. A hundred and twenty-eight pixels square. "
            "<bookmark mark='b'/> In its Fourier domain we measure only twenty-two lines through the centre, like spokes of a "
            "wheel: about a fifth of the coefficients. The other four fifths are simply unknown."
        ) as vo:
            self.add(phantom_tag())
            vo.wait_until("a")
            self.play(FadeIn(p1))
            vo.wait_until("b")
            self.play(FadeIn(p2))
        self.wait(1.0)
        self.clear_scene()

    def zero_fill(self):
        d = load("phantom")
        truth, me = np.asarray(d["truth"]), np.asarray(d["min_energy"])
        p1 = PhantomPanel(truth, size=3.4, caption=r"truth", lo=0, hi=1, center=[-3.4, 0.6, 0])
        p2 = PhantomPanel(me, size=3.4, caption=r"minimum energy: \ unknowns set to 0", lo=0, hi=1, center=[2.0, 0.6, 0])
        rows = fit_rows(VGroup(
            label(r"the obvious answer: \ the smallest image that fits the data", font_size=22),
            label(rf"relative error {100 * d['err_me']:.0f}\%: \ streaks, \ blur, \ lost detail", font_size=22, color=RES),
        ), 12.0, 0.2, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The obvious reconstruction sets every unmeasured coefficient to zero and inverts. Among all "
            "images consistent with the measurements, it is the one with the least energy, the least-squares answer of "
            "Part 12 for an underdetermined system. <bookmark mark='b'/> It is poor: streaks radiate from every edge, the "
            "small features are smeared, and the error is forty-eight percent."
        ) as vo:
            self.add(phantom_tag())
            self.play(FadeIn(p1))
            vo.wait_until("a")
            self.play(FadeIn(p2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def recover(self):
        d = load("phantom")
        truth = np.asarray(d["truth"])
        snaps = d["snaps"]
        p1 = PhantomPanel(truth, size=3.4, caption=r"truth", lo=0, hi=1, center=[-3.4, 0.6, 0])
        p2 = PhantomPanel(np.asarray(d["min_energy"]), size=3.4, caption=r"minimum total variation", lo=0, hi=1,
                          center=[2.0, 0.6, 0], caption_color=LASSO)
        it = label(r"start", font_size=24, color=GREY_A).move_to([2.0, -1.75, 0])
        er = label(rf"error {100 * d['err_me']:.0f}\%", font_size=24, color=RES).move_to([2.0, -2.3, 0])
        foot = label(r"among all images that fit the 22 lines, \ minimum sum of local gradient magnitudes; grayscale display clipped to [0,1]",
                     font_size=22, color=GREY_A).move_to([0, -3.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Candès's reconstruction asks a different question. Among all images that agree with"
            " the measured coefficients, find the one with the smallest total variation: the sum, over pixels, of the"
            " size of the jump to their neighbours. This measures contrast-weighted local jumps, not just unweighted "
            "edge length. <bookmark mark='b'/> Solving that convex problem iteratively, the streaks fade and the "
            "error falls: nineteen percent, four, two tenths of a percent, then one part in a hundred thousand, "
            "<bookmark mark='c'/> and finally about one part in ten billion in this numerical run. This is accuracy "
            "to numerical tolerance, not a proof of literal zero error."
        ) as vo:
            self.add(phantom_tag())
            self.play(FadeIn(p1), FadeIn(p2), FadeIn(it), FadeIn(er))
            vo.wait_until("a")
            self.play(FadeIn(foot))
            vo.wait_until("b")
            cur = p2.image
            for k in ("20", "100", "400", "1500", "4000"):
                new = p2.panel_for(np.asarray(snaps[k]))
                if k == "4000":
                    self.play(FadeTransform(cur, new), run_time=0.8)
                    cur = new
                    break
                self.play(FadeTransform(cur, new),
                          Transform(it, label(rf"iteration {int(k):,}", font_size=24, color=GREY_A).move_to(it)),
                          Transform(er, label(rf"error {100 * d['err_snaps'][k]:.3g}\%", font_size=24, color=RES).move_to(er)),
                          run_time=1.2)
                cur = new
            vo.wait_until("c")
            self.play(Transform(it, label(r"iteration 4,000", font_size=24, color=GREY_A).move_to(it)),
                      Transform(er, label(r"error $1.6 \times 10^{-10}$: numerical recovery", font_size=24, color=HIT).move_to(er)))
        self.clear_scene()

    def why(self):
        d = load("phantom")
        rows = [
            cmath(r"\text{pixels}", r":", r"\text{16,384 unknowns, \ many of them nonzero}", font_size=30),
            cmath(r"\text{jumps}", r":", rf"\text{{only about {100 * d['nonzero_grad']:.0f}\% of horizontal neighbours differ}}", font_size=30),
            cmath(r"\text{Fourier samples}", r":", r"\text{each one sees the whole image}", font_size=30),
            cmath(r"\text{sparse} + \text{incoherent}", r"\Rightarrow", r"\text{few measurements suffice}", font_size=30),
        ]
        rows[3][-1].set_color(SPIKE)
        whys = [why(r"far too many for 3,400 equations"), why(r"sparse in the right basis"),
                why(r"spread out: \ no measurement is wasted"), why(r"chapter nine")]
        with self.voiceover(
            "<bookmark mark='a'/> Why can it work? The image has sixteen thousand pixels, many of them nonzero: far "
            "more unknowns than equations. <bookmark mark='b'/> But the image is simple in another sense. Only about "
            "five percent of horizontal neighbours differ: it is sparse in its jumps. <bookmark mark='c'/> And each "
            "Fourier coefficient is a weighted sum over the whole image, so every measurement carries information "
            "about every jump. <bookmark mark='d'/> Sparsity in one basis, measurements spread out in another: that "
            "combination is what lets a few equations determine many unknowns. Chapter nine makes it precise."
        ) as vo:
            intro=label('Gradient sparsity can support accurate recovery from incomplete Fourier data',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def count(self):
        rows = fit_rows(VGroup(
            label(r"regression has the same problem: \ more variables than observations", font_size=26),
            label(r"gene expression: \ 20{,}000 genes, \ 100 patients", font_size=26, color=LASSO),
            label(r"least squares has infinitely many exact fits", font_size=26, color=RES),
            label(r"the bet on sparsity: \ assume few coefficients matter, \ and find them", font_size=26, color=SPIKE),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Statistics meets the same problem constantly. <bookmark mark='b'/> In a "
            "gene-expression study there may be twenty thousand genes measured on a hundred patients. <bookmark "
            "mark='c'/> A regression of an outcome on all of them has infinitely many exact fits, each meaningless. "
            "<bookmark mark='d'/> The way out is what Hastie, Tibshirani and Friedman call the bet on sparsity: "
            "assume that only a few coefficients matter, and use a method that finds them. Other structures, such as "
            "smoothness, low rank or many small effects, can support different methods; the sparse assumption must be"
            " assessed."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 32", font_size=34, color=GREY_B), label(r"Sparsity", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"ridge, \ and why it never selects; \ from $\ell_0$ to $\ell_1$",
            r"the lasso: \ KKT conditions, \ soft thresholding, \ the octahedron",
            r"computing and tuning it: \ coordinate descent, \ LARS, \ CV, \ stability",
            r"the penalty zoo; \ Bayesian sparsity and the horseshoe",
            r"compressed sensing; \ inference after selection; \ matrix completion",
        ], color=LASSO, font_size=26)
        prereq = note(r"prerequisites: \ Parts 19, \ 21 and 23").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.sparse}; \ the phantom").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-two: sparsity. <bookmark mark='b'/> We start with ridge regression and "
            "see why it does not generally select variables; move from the hopeless count of best subsets to the "
            "convex absolute-value penalty; derive the lasso's optimality conditions and its geometry; compute its "
            "whole path and choose its tuning parameter; survey its relatives and its Bayesian counterparts; prove "
            "what we can about compressed sensing; repair inference after selection; and finish with matrices that "
            "are sparse in their singular values."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
