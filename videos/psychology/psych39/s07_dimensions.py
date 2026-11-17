from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Dimensions(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_worlds()
        self.taxometrics()

    def card(self):
        card = chapter_card(6, r"Categories or dimensions?", r"Is a disorder a kind, \ or a degree?",
                            lit={2012: r"Haslam et al.", 2020: r"Haslam et al."}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter six. Categories or dimensions?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def two_worlds(self):
        head = heading(r"A kind, \ or a degree?")
        A = axes([-4, 6], [0, 0.45], x_length=5.0, y_length=2.0, xticks=None, yticks=None,
                 xlabel=r"symptom score", center=[-3.4, 1.0, 0], font_size=13)
        xs = np.linspace(-4, 6, 300)
        mix = 0.88 * np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi) + 0.12 * np.exp(-(xs - 3.6) ** 2 / 2) / np.sqrt(2 * np.pi)
        taxon = curve(A.ax, xs, mix, PERSON, stroke_width=4)
        lt = label(r"a taxon: \ two groups", font_size=15, color=PERSON).next_to(A, UP, buff=0.1)
        B = axes([-4, 6], [0, 0.45], x_length=5.0, y_length=2.0, xticks=None, yticks=None,
                 xlabel=r"symptom score", center=[-3.4, -2.0, 0], font_size=13)
        cont = curve(B.ax, xs, np.exp(-(xs - 0.4) ** 2 / 3.2) / np.sqrt(3.2 * np.pi), SYMP, stroke_width=4)
        cut = DashedLine(B.ax.c2p(2.6, 0), B.ax.c2p(2.6, 0.32), color=AUTH)
        lc = label(r"a dimension, \ with a cut-off", font_size=15, color=SYMP).next_to(B, UP, buff=0.1)
        rows = rows_of([
            (r"a category claims a kind of person: \ two groups, \ with a gap or a second hump between them", PERSON),
            (r"a dimension claims a degree: \ one continuum, \ and the diagnosis is a line drawn across it", SYMP),
            (r"blood pressure is a dimension with a clinical cut-off; \ having a chromosome trisomy is a kind", WHITE),
            (r"the question is empirical: \ taxometric methods ask whether the data look like a mixture or a "
             r"continuum", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "Is a disorder a kind of person, or a degree? <bookmark mark='a'/> A category claims a kind: two "
            "groups, with a gap or a second hump between them. <bookmark mark='b'/> A dimension claims a degree: one "
            "continuum, with the diagnosis a line drawn across it. <bookmark mark='c'/> High blood pressure is a "
            "dimension with a clinical cut-off. Having an extra copy of a chromosome is a kind. "
            "<bookmark mark='d'/> Which one a disorder is, is an empirical question. Taxometric methods ask whether "
            "the data look like a mixture of two groups, or one continuum."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(A), Create(taxon), FadeIn(lt))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(B), Create(cont), Create(cut), FadeIn(lc))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def taxometrics(self):
        head = heading(r"Mostly degrees")
        A = axes([-0.6, 2.6], [0, 60], x_length=4.6, y_length=3.2, xticks=None, yticks=[0, 20, 40, 60],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"findings called taxonic", center=[-3.6, -0.2, 0],
                 font_size=14)
        vals = [38.9, 16.2, 14.0]
        cols = [GREY_A, SYMP, GOOD]
        b = bars(A.ax, [0, 1, 2], vals, cols, width=0.6)
        names = VGroup(*[wrapped_label(t, 1.5, 13, c).next_to(A.ax.c2p(k, 0), DOWN, buff=0.15) for k, (t, c) in
                         enumerate(((r"as reported", GREY_A), (r"with the stricter method", SYMP),
                                    (r"the reviewers' estimate", GOOD)))])
        tops = VGroup(*[label(f"{v:.1f}\\%" if v % 1 else f"{v:.0f}\\%", font_size=15, color=c).next_to(
            A.ax.c2p(k, v), UP, buff=0.08) for k, (v, c) in enumerate(zip(vals, cols))])
        rows = rows_of([
            (r"Haslam, \ Holland and Kuppens, \ 2012: \ 177 articles, \ 311 taxometric findings, \ over half a "
             r"million people", WHITE),
            (r"39\% were reported as taxonic, \ but only 16\% of those using the stricter, \ simulation-based "
             r"method; \ the reviewers estimated the true rate near 14\%", SYMP),
            (r"their 2020 update: \ the great majority of differences between people are continuous, \ and "
             r"psychopathology is no exception", GOOD),
            (r"so most diagnoses are lines drawn by convention across a continuum, \ and where to draw them is a "
             r"decision about costs, \ not a discovery", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Haslam, \ Holland \& Kuppens (2012); \ Haslam et al.\ (2020)")
        with self.voiceover(
            "What do the data say? <bookmark mark='a'/> In 2012 Nick Haslam and colleagues reviewed a hundred and "
            "seventy-seven articles: three hundred and eleven taxometric findings, over half a million people. "
            "<bookmark mark='b'/> Thirty-nine percent had been reported as taxonic. But among studies using the "
            "stricter, simulation-based method, only sixteen percent were. The reviewers estimated the true rate "
            "near fourteen percent. <bookmark mark='c'/> Their 2020 update concluded that the great majority of "
            "differences between people are continuous, and psychopathology is no exception. "
            "<bookmark mark='d'/> So most diagnoses are lines drawn by convention across a continuum. Where to draw "
            "them is a decision about costs, not a discovery."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[GrowFromEdge(x, DOWN) for x in b], FadeIn(tops))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
