from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Encoding(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.ceiling()
        self.maps()

    def card(self):
        card = chapter_card(7, r"Encoding models", r"Can a model predict a voxel it has never seen respond?", lit=(),
                            part=PART, scale=("brain",), marr=("what",))
        with self.voiceover("Chapter seven. Encoding models."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def idea(self):
        head = heading(r"Predict the brain from the stimulus")
        eq = MathTex(r"y_v(\text{stimulus}) = \sum_k w_{vk}\, f_k(\text{stimulus}) + \varepsilon_v", font_size=38,
                     color=MODEL).move_to([0, 1.6, 0])
        rows = rows_of([
            (r"decoding goes from brain to label; \ encoding goes the other way, \ from features of the stimulus to "
             r"each voxel", WHITE),
            (r"the features are a theory: \ edges and orientations, \ word meanings, \ a network's layer", MODEL),
            (r"fit the weights with a penalty (ridge regression) on some stimuli; \ judge the model only on stimuli "
             r"it has never seen", PERSON),
            (r"Naselaris and colleagues set out the framework in 2011: \ a model earns its keep by prediction", GOOD),
        ], 12.4, 21, 0.38).move_to([0, -1.0, 0])
        tag = published_tag(r"Naselaris et al.\ (2011)")
        with self.voiceover(
            "Encoding models turn the arrow around. <bookmark mark='a'/> Decoding goes from the brain to a label. "
            "Encoding goes from features of the stimulus to each voxel. <bookmark mark='b'/> The features are a "
            "theory: edges and orientations, the meanings of words, or a layer of a neural network. "
            "<bookmark mark='c'/> The weights are fitted with a penalty, ridge regression, on some stimuli, and the "
            "model is judged only on stimuli it has never seen. <bookmark mark='d'/> Thomas Naselaris and colleagues "
            "set out the framework in 2011. A model earns its keep by prediction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def ceiling(self):
        d = load("encoding")
        head = heading(r"Prediction against the noise ceiling")
        r = np.asarray(d["r"])
        c = np.asarray(d["ceiling"])
        resp = np.asarray(d["responsive"], bool)
        A = axes([0, 1], [-0.2, 1], x_length=4.4, y_length=3.4, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"noise ceiling (repeat reliability)",
                 ylabel=r"prediction $r$ on new stimuli", center=[-3.7, 0.2, 0], font_size=12)
        diag = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(1, 1), color=GREY_B, stroke_width=1.5)
        dots = VGroup(scatter(A.ax, c[resp], r[resp], MODEL, radius=0.035),
                      scatter(A.ax, c[~resp], r[~resp], GREY_B, radius=0.035))
        rows = rows_of([
            (r"300 voxels, \ 40 stimulus features; \ trained on 300 stimuli, \ tested on 60 new ones, \ each shown twice",
             WHITE),
            (r"each voxel's ceiling: \ how well one showing of the test stimuli predicts the other; \ no model can do "
             r"better than the data agree with themselves", GREY_B),
            (rf"for responsive voxels the model reaches a median $r$ of {d['median_r']:.2f}, \ "
             rf"{100 * d['median_fraction']:.0f}\% of their ceiling", MODEL),
            (r"the grey voxels respond to none of the features: \ low ceilings, \ and nothing to predict", YOU),
        ], 6.4, 19, 0.38).move_to([3.2, -0.1, 0])
        tag = psyche_tag(r"\texttt{neurodata.encoding}, \ ridge")
        with self.voiceover(
            "Psyche builds a case where the true features are known. <bookmark mark='a'/> Three hundred voxels, forty "
            "stimulus features, trained on three hundred stimuli and tested on sixty new ones, each shown twice. "
            "<bookmark mark='b'/> Each voxel's noise ceiling is how well one showing of the test stimuli predicts the "
            "other. No model can do better than the data agree with themselves. <bookmark mark='c'/> For responsive "
            "voxels, the model reaches a median correlation of about zero point seven eight, near their ceiling. "
            "<bookmark mark='d'/> The grey voxels respond to none of the features: low ceilings, and nothing to "
            "predict. Real models fall well below their ceilings, and the gap is what the theory is missing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(dots[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(dots[1]))
        self.clear_scene()

    def maps(self):
        head = heading(r"Maps of meaning")
        rows = rows_of([
            (r"2016: \ Alexander Huth and colleagues played hours of stories to a handful of people in the scanner", WHITE),
            (r"each word was described by its meaning, \ as a list of numbers; \ each voxel got its own weights", MODEL),
            (r"the fitted weights tiled much of cortex with patches tuned to meanings: \ people, \ places, \ numbers, "
             r"\ and more, \ in both hemispheres", PERSON),
            (r"maps from few people, \ each scanned for hours: \ precise for them, \ and a question for everyone else",
             AUTH),
            (r"the same method maps Part 23's language network, \ and is how today's language models are compared with "
             r"brains", YOU),
        ], 12.4, 22, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Huth et al.\ (2016)")
        with self.voiceover(
            "Encoding models made a striking map. <bookmark mark='a'/> In 2016 Alexander Huth and colleagues played "
            "hours of stories to a handful of people in the scanner. <bookmark mark='b'/> Each word was described by "
            "its meaning, as a list of numbers, and each voxel got its own weights. <bookmark mark='c'/> The weights "
            "tiled much of cortex with patches tuned to kinds of meaning: people, places, numbers and more, in both "
            "hemispheres. <bookmark mark='d'/> These are maps from a few people, each scanned for hours: precise for "
            "them, and an open question for everyone else. <bookmark mark='e'/> The same method maps Part 23's "
            "language network, and it's how today's language models are compared with brains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
