from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403


class Biotypes(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"Biotypes", r"Are there kinds of depression in the brain?", scale=("brain",))
        self.drysdale()
        self.pipeline()
        self.stability()

    def drysdale(self):
        rows_section(self, r"Four biotypes", [
            (r"Drysdale and colleagues, \ 2017: \ resting-state scans of about 1,200 people", WHITE),
            (r"they chose the connectivity features most correlated with symptoms, \ then clustered patients on them",
             MODEL),
            (r"four clusters, \ with different symptom profiles, \ and different responses to TMS in a subset", GOOD),
            (r"a promise: \ a scan that tells you which kind of depression, \ and which treatment", PERSON),
        ], "Are there kinds of depression in the brain? <bookmark mark='a'/> In 2017 Andrew Drysdale and colleagues "
           "analysed resting-state scans from about twelve hundred people. <bookmark mark='b'/> They chose the "
           "connectivity features most correlated with symptoms, then clustered patients on them. "
           "<bookmark mark='c'/> They found four clusters, with different symptom profiles, and different responses "
           "to magnetic stimulation in a subset. <bookmark mark='d'/> It was a promise: a scan that tells you which "
           "kind of depression a person has, and which treatment to give.",
           tag=published_tag(r"Drysdale et al.\ (2017)"))

    def pipeline(self):
        d = load("biotypes")
        head = heading(r"The same pipeline on data with no types")
        A = axes([0.3, 10.7], [0, 0.2], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.05, 0.1, 0.2],
                 yfmt=lambda v: f"{v:g}", ylabel=r"symptom difference, \ $p$", center=[-3.3, 0.3, 0], font_size=12)
        p = np.minimum(np.asarray(d["none_p"]), 0.199)
        bs = VGroup(*[bars(A.ax, [i + 1], [max(v, 0.004)], GOOD if v < 0.05 else AUTH, width=0.6) for i, v in
                      enumerate(p)])
        cut = DashedLine(A.ax.c2p(0.3, 0.05), A.ax.c2p(10.7, 0.05), color=GREY_B, stroke_width=2)
        cl = label(r"0.05", font_size=13, color=GREY_B).next_to(cut, RIGHT, buff=0.08)
        xl = label(r"ten simulated studies of 220 patients", font_size=13, color=GREY_A).next_to(A, DOWN, buff=0.1)
        ns = int(np.sum(d["none_p"] < 0.05))
        rows = rows_of([
            (r"Psyche's 220 patients: \ 20 connectivity features, \ no subgroups at all; \ symptoms depend weakly on "
             r"three features", WHITE),
            (r"the pipeline: \ keep the six features most correlated with symptoms, \ cluster into four, \ test "
             r"whether the clusters differ in symptoms", MODEL),
            (rf"in {ns} of 10 studies they do, \ at $p$ < 0.05: \ your second number", AUTH),
            (r"the features were chosen for their link to symptoms; \ any way of cutting them gives groups that "
             r"differ: \ circular analysis, \ Part 8's double dipping", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{precision.biotypes}, \ no structure")
        with self.voiceover(
            "Now run the same pipeline on data with no types. <bookmark mark='a'/> Psyche's two hundred and twenty "
            "patients have twenty connectivity features and no subgroups at all. Symptoms depend weakly on three "
            "features. <bookmark mark='b'/> The pipeline keeps the six features most correlated with symptoms, "
            "clusters patients into four, and tests whether the clusters differ in symptoms. <bookmark mark='c'/> In "
            "nine of ten simulated studies, they do, at p below zero point zero five. That's your second number. "
            "<bookmark mark='d'/> The features were chosen for their link to symptoms, so any way of cutting them "
            "gives groups that differ. It's circular analysis: Part 8's double dipping."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(xl), Create(cut), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bs], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def stability(self):
        d = load("biotypes")
        head = heading(r"Split the sample: \ do the clusters come back?")
        A = axes([0, 1.0], [0.4, 2.6], x_length=5.6, y_length=2.8, xticks=[0, 0.5, 1.0], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"agreement between halves (adjusted Rand index)",
                 center=[-3.3, 0.4, 0], font_size=12)
        none = scatter(A.ax, d["none_ari"], np.full(10, 2.0), AUTH, radius=0.08)
        real = scatter(A.ax, d["real_ari"], np.full(10, 1.0), GOOD, radius=0.08)
        ln = label(r"no types", font_size=14, color=AUTH).next_to(A.ax.c2p(0, 2.0), LEFT, buff=0.15)
        lr = label(r"real types", font_size=14, color=GOOD).next_to(A.ax.c2p(0, 1.0), LEFT, buff=0.15)
        rows = rows_of([
            (r"cluster two random halves separately, \ assign everyone by each half's centres, \ compare the labels",
             WHITE),
            (rf"no types: \ agreement about {np.mean(d['none_ari']):.2f}; \ the clusters are different every time",
             AUTH),
            (rf"real types (planted in Psyche): \ about {np.mean(d['real_ari']):.2f}; \ the clusters come back",
             GOOD),
            (r"Dinga and colleagues, \ 2019, \ re-ran the biotype analysis on 187 people: \ the clusters were not "
             r"stable, \ and data without clusters gave similar results", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{precision.biotypes}, \ split halves")
        tag2 = published_tag(r"Dinga et al.\ (2019)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "How do you tell real types from fake ones? Split the sample and see if the clusters come back. "
            "<bookmark mark='a'/> Cluster two random halves separately, assign everyone by each half's centres, and "
            "compare the labels. <bookmark mark='b'/> With no types, the agreement is about zero point one six. The "
            "clusters are different every time. <bookmark mark='c'/> With real types planted in Psyche, it's about "
            "zero point seven four. The clusters come back. <bookmark mark='d'/> In 2019 Richard Dinga and colleagues "
            "re-ran the biotype analysis on a hundred and eighty-seven people. The clusters weren't stable, and data "
            "without clusters gave similar results."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(ln), FadeIn(lr))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(none))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(real))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
