from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Appraisal(VoiceoverScene):
    def construct(self):
        self.card()
        self.lazarus()
        self.model()
        self.scenarios()

    def card(self):
        card = chapter_card(7, r"Appraisal", r"Is an emotion an evaluation?",
                            lit={1966: r"Lazarus", 1985: r"Smith \& Ellsworth", 2001: r"Scherer"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter seven. Appraisal."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def lazarus(self):
        head = heading(r"Emotion follows meaning")
        rows = rows_of([
            (r"Magda Arnold and Richard Lazarus: \ an emotion follows an appraisal of what an event means for "
             r"one's goals and well-being", COG),
            (r"Lazarus's films, \ 1960s: \ the same distressing film was less upsetting when a narrator framed it "
             r"in a detached, \ intellectual way", WHITE),
            (r"Craig Smith and Phoebe Ellsworth, \ 1985: \ people recalled emotional events and rated them on "
             r"appraisal dimensions; \ a handful of dimensions separated the emotions well", FACE),
            (r"the same event, \ appraised differently, \ gives a different emotion: \ a delay is frustrating if "
             r"someone caused it, \ sad if nobody did", PLEAS),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"Lazarus (1966); \ Smith \& Ellsworth (1985)")
        with self.voiceover(
            "The third family of theories puts thought first. <bookmark mark='a'/> For Magda Arnold and Richard "
            "Lazarus, an emotion follows an appraisal: an evaluation of what an event means for one's goals and "
            "well-being. <bookmark mark='b'/> In Lazarus's laboratory in the 1960s, the same distressing film was "
            "less upsetting when a narrator framed it in a detached, intellectual way. <bookmark mark='c'/> In 1985 "
            "Craig Smith and Phoebe Ellsworth asked people to recall emotional events and rate them on dimensions "
            "such as pleasantness, certainty, who was responsible, and how much control they had. A handful of "
            "dimensions separated the emotions well. <bookmark mark='d'/> The same event, appraised differently, "
            "gives a different emotion: a delay is infuriating if someone caused it, and merely sad if nobody did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def model(self):
        d = load("appraisal")
        head = heading(r"Psyche's appraisal model")
        dims = d["dims"]
        names = list(d["prototypes"])
        P = np.array([d["prototypes"][k] for k in names], float)
        cell = 0.5
        grid = VGroup()
        for i, nm in enumerate(names):
            for j in range(len(dims)):
                v = P[i, j]
                col = PLEAS if v > 0 else UNPL
                grid.add(Square(side_length=cell * 0.92, stroke_width=0, fill_color=col,
                                fill_opacity=0.15 + 0.8 * abs(v)).move_to([j * cell, -i * cell, 0]))
        grid.move_to([-2.6, -0.4, 0])
        rl = VGroup(*[label(nm, font_size=16, color=COG).next_to(grid[i * len(dims)], LEFT, buff=0.15)
                      for i, nm in enumerate(names)])
        cl = VGroup(*[label(dm, font_size=14, color=GREY_B).rotate(PI / 4).next_to(grid[j], UP, buff=0.12)
                      .shift(RIGHT * 0.15) for j, dm in enumerate(dims)])
        eq = MathTex(r"p(e \mid x) = \frac{e^{-\beta \lVert x - \mu_e \rVert}}{\sum_{e'} e^{-\beta \lVert x - "
                     r"\mu_{e'} \rVert}}", font_size=32)
        rows = rows_of([
            (r"each emotion a prototype on six appraisal dimensions: \ green positive, \ red negative", MODEL),
            (r"directions after Smith and Ellsworth, \ and Scherer; \ the values are illustrative", GREY_B),
            (r"a scenario is coded on the same dimensions; \ the nearer a prototype, \ the likelier its label", COG),
        ], 4.6, 20, 0.3)
        right = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.2, -0.2, 0])
        tag = psyche_tag(r"\texttt{emotion.appraise}")
        with self.voiceover(
            "Psyche can make an appraisal theory compute. <bookmark mark='a'/> Each emotion is a prototype on six "
            "appraisal dimensions: how pleasant, how certain, whether I caused it, whether someone else did, how "
            "much control I have, and how sudden it was. Green is positive, red negative. <bookmark mark='b'/> The "
            "directions follow Smith and Ellsworth and Klaus Scherer; the exact values are illustrative. "
            "<bookmark mark='c'/> A scenario is coded on the same six dimensions, and the nearer it lies to a "
            "prototype, the likelier that label, by a softmax over distances."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid), FadeIn(rl), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(eq), FadeIn(rows[2]))
        self.clear_scene()

    def scenarios(self):
        d = load("appraisal")
        head = heading(r"Six situations, \ appraised")
        rows = VGroup()
        for i, sc in enumerate(d["scenario"]):
            labs = d[f"labels{i}"]
            ps = d[f"p{i}"]
            t = wrapped_label(sc, 5.6, 21, WHITE)
            out = label(rf"{labs[0]} \ {100 * ps[0]:.0f}\%", font_size=22, color=COG)
            alt = label(rf"then {labs[1]} \ {100 * ps[1]:.0f}\%", font_size=16, color=GREY_B)
            rows.add(VGroup(t, VGroup(out, alt).arrange(DOWN, aligned_edge=LEFT, buff=0.08)).arrange(
                RIGHT, buff=0.6))
        for r in rows:
            r[1].shift(RIGHT * (6.2 - r[0].width))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([-0.5, 0.35, 0])
        foot = wrapped_label(r"the model gets labels right that a list of situations would also get right; \ the "
                             r"test of appraisal theory is whether changing one appraisal \ (who caused it) \ changes "
                             r"the emotion, \ and experiments that manipulate appraisals find it does", 12.6, 21,
                             MODEL).to_edge(DOWN, buff=1.0)
        tag = psyche_tag(r"\texttt{emotion.appraise}: \ six coded scenarios")
        with self.voiceover(
            "Here are six situations, coded and appraised. <bookmark mark='a'/> A colleague takes credit for your "
            "work: unpleasant, certain, someone else's doing. Anger. A noise downstairs at three in the morning: "
            "unpleasant, uncertain, sudden, out of your control. Fear. Passing an exam you trained months for: "
            "pride. Your old dog dying: sadness. Waiting to hear about a job you want: hope. Forgetting a friend's "
            "birthday party: guilt. <bookmark mark='b'/> A model like this gets right what a list of situations "
            "would also get right. The real test of appraisal theory is whether changing one appraisal, such as who "
            "caused the event, changes the emotion, and experiments that manipulate appraisals find that it does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.6), run_time=12.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
