from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Funnel(VoiceoverScene):
    def construct(self):
        self.card()
        self.funnel()
        self.egger()
        self.other()

    def card(self):
        card = chapter_card(4, r"Seeing the filter", r"What does a filtered literature look like?", lit=(), part=PART,
                            scale=("society",), marr=("what",))
        with self.voiceover("Chapter four. Seeing the filter."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _axes(self):
        return axes([-0.6, 1.4], [0, 0.42], x_length=5.4, y_length=3.6, xticks=[-0.5, 0, 0.5, 1.0],
                    yticks=[0, 0.1, 0.2, 0.3, 0.4], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                    xlabel=r"effect $d$", ylabel=r"standard error (small studies at the top)", center=[-3.3, 0.0, 0],
                    font_size=12)

    def funnel(self):
        d = load("funnel")
        head = heading(r"A funnel with a bite taken out")
        A = self._axes()
        top = 0.42

        def pt(x, s):
            return A.ax.c2p(x, top - s)

        all_d = VGroup(*[Dot(pt(x, s), radius=0.035, color=GREY_D) for x, s in zip(d["all_y"], d["all_se"])
                         if -0.6 <= x <= 1.4])
        pub = VGroup(*[Dot(pt(x, s), radius=0.045, color=SYMP) for x, s in zip(d["y"], d["se"]) if -0.6 <= x <= 1.4])
        tri = VGroup(DashedLine(pt(d["true"], 0), pt(d["true"] - 1.96 * 0.4, 0.4), color=GREY_B, stroke_width=1.5),
                     DashedLine(pt(d["true"], 0), pt(d["true"] + 1.96 * 0.4, 0.4), color=GREY_B, stroke_width=1.5))
        sig = VMobject(stroke_color=AUTH, stroke_width=2).set_points_as_corners(
            [pt(1.96 * s, s) for s in np.linspace(0.02, 0.4, 20)])
        rows = rows_of([
            (r"each dot is a study: \ its effect against its standard error; \ small studies sit high and spread wide",
             WHITE),
            (r"with no filter the cloud is a symmetric funnel around the truth (0.2); \ grey: \ every study run", GREY_B),
            (rf"blue: \ the {d['k']} published; \ the red line is where a study becomes significant, \ and the "
             rf"small studies left of it are missing", SYMP),
            (r"a funnel with a bite taken out of one side: \ the published small studies are the lucky ones", YOU),
        ], 6.4, 19, 0.36).move_to([3.3, -0.1, 0])
        tag = psyche_tag(r"\texttt{meta.literature}: \ filter and some p-hacking")
        with self.voiceover(
            "Here's what a filter looks like. <bookmark mark='a'/> Each dot is a study, placed by its effect and its "
            "standard error. Small studies sit high and spread wide. <bookmark mark='b'/> With no filter, the cloud "
            "is a symmetric funnel around the truth. The grey dots are every study that was run. "
            "<bookmark mark='c'/> The blue ones were published. The red line is where a study becomes significant, "
            "and the small studies to its left are missing. <bookmark mark='d'/> It's a funnel with a bite taken out "
            "of one side. The published small studies are the lucky ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(tri))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(all_d))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeOut(all_d), FadeIn(pub), Create(sig))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def egger(self):
        d = load("funnel")
        head = heading(r"Egger's test, \ and the effect at zero error")
        A = axes([0, 0.42], [-0.2, 1.4], x_length=5.4, y_length=3.4, xticks=[0, 0.1, 0.2, 0.3, 0.4],
                 yticks=[0, 0.5, 1.0], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"standard error",
                 ylabel=r"effect $d$", center=[-3.3, 0.2, 0], font_size=12)
        dots = scatter(A.ax, d["se"], d["y"], SYMP, radius=0.045)
        y = np.asarray(d["y"]); se = np.asarray(d["se"])
        w = 1 / se ** 2
        X = np.column_stack([np.ones_like(se), se])
        b = np.linalg.solve(X.T @ (w[:, None] * X), X.T @ (w * y))
        line = Line(A.ax.c2p(0, b[0]), A.ax.c2p(0.42, b[0] + b[1] * 0.42), color=MODEL, stroke_width=3)
        truth = DashedLine(A.ax.c2p(0, d["true"]), A.ax.c2p(0.42, d["true"]), color=GOOD, stroke_width=2)
        rows = rows_of([
            (rf"Egger, \ 1997: \ regress effect on standard error; \ a slope means small studies show bigger effects: "
             rf"\ here $p$ = {d['egger_p']:.3f}", WHITE),
            (rf"the intercept is the effect a study with no error would find: \ PET gives {d['pet']:.2f}", MODEL),
            (rf"the naive pooled estimate is {d['naive']:.2f}; \ the truth (green) is {d['true']:.1f}", AUTH),
            (rf"PEESE, \ which bends the line, \ gives {d['peese']:.2f}; \ PET-PEESE picks between them by a rule", PERSON),
        ], 6.2, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{meta.egger}, \ \texttt{pet}, \ \texttt{peese}")
        with self.voiceover(
            "Two tools read the bite. <bookmark mark='a'/> Egger's test regresses each study's effect on its standard "
            "error. A slope means small studies show bigger effects, and here it's clearly there. "
            "<bookmark mark='b'/> The intercept is the effect a study with no error at all would find. That's PET, "
            "and here it gives about zero point one three. <bookmark mark='c'/> The naive pooled estimate is about "
            "zero point four one, and the truth is zero point two. <bookmark mark='d'/> PEESE bends the line and gives "
            "about zero point three. PET-PEESE chooses between them by a rule. Neither is the truth exactly, and the "
            "next chapter asks how often any of them is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(line))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(truth))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def other(self):
        head = heading(r"Not every asymmetric funnel is bias")
        rows = rows_of([
            (r"small studies may really have bigger effects: \ more intensive treatments, \ more select samples, \ "
             r"better fidelity", WHITE),
            (r"heterogeneity that happens to line up with study size makes the same slope", MODEL),
            (r"some effect measures are linked to their own standard errors, \ which tilts the funnel by arithmetic",
             PERSON),
            (r"and with few studies, \ chance alone makes funnels lopsided", AUTH),
            (r"asymmetry is a warning about small-study effects; \ only registration shows the studies that are missing",
             YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "But not every lopsided funnel is publication bias. <bookmark mark='a'/> Small studies may really have "
            "bigger effects: more intensive treatments, more select samples, better fidelity. "
            "<bookmark mark='b'/> Heterogeneity that happens to line up with study size makes the same slope. "
            "<bookmark mark='c'/> Some effect measures are linked to their own standard errors, which tilts the "
            "funnel by arithmetic. <bookmark mark='d'/> And with few studies, chance alone makes funnels lopsided. "
            "<bookmark mark='e'/> Asymmetry is a warning about small-study effects. Only registration shows the studies "
            "that are missing."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
