from __future__ import annotations

import numpy as np

from videos.stats.stats13.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.broadbalk()
        self.muck_heap()
        self.uniformity()
        self.questionnaire()
        self.objectives()

    def broadbalk(self):
        tl = timeline(lit=(1919,)).to_edge(UP, buff=0.35)
        hc = history_card(1843, r"John Bennet Lawes \ and \ Joseph Henry Gilbert, \ Rothamsted, \ Hertfordshire",
                          r"winter wheat sown on the Broadbalk field, \ in strips given different manures, \ and harvested "
                          r"and weighed every year since", color=DATA, width=9.6, font_size=24).move_to([0, 1.0, 0])
        # Broadbalk as strips: each strip one manure, painted by a made-up yield that drifts year to year
        g = np.random.Generator(np.random.PCG64(1843))
        strips = VGroup()
        base = np.array([18, 30, 34, 26, 38, 22, 35, 31, 15, 33])
        for k, b in enumerate(base):
            r = Rectangle(width=0.9, height=1.5, stroke_width=1, stroke_color=GREY_D,
                          fill_color=FieldPlot.colour(b + g.normal(0, 2), 12, 40), fill_opacity=0.95)
            strips.add(r)
        strips.arrange(RIGHT, buff=0.06).move_to([0, -1.6, 0])
        names = label(r"schematic strips and colours: \ no manure, \ farmyard manure, \ N, \ P, \ K, \ combinations", font_size=22,
                      color=GREY_A).next_to(strips, DOWN, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> In 1843 John Bennet Lawes, who had made a fortune from artificial fertilizer, and the "
            "chemist Joseph Henry Gilbert began an experiment on a field called Broadbalk, at Rothamsted, north of London. "
            "They sowed winter wheat, divided the field into long strips, and gave each strip a different manure: none at "
            "all, farmyard manure, nitrogen, phosphate, potash, and their combinations. <bookmark mark='b'/> Every year they "
            "harvested each strip and weighed the grain. The experiment is still running today, one of the oldest continuous "
            "field experiments in the world. By 1919 there were seventy-six years of carefully kept numbers."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(s_, DOWN) for s_ in strips], lag_ratio=0.12), FadeIn(names), run_time=2.5)
            for _ in range(3):
                self.play(*[s_.animate.set_fill(FieldPlot.colour(b + g.normal(0, 5), 12, 40)) for s_, b in zip(strips, base)],
                          run_time=0.8)
        self.clear_scene()

    def muck_heap(self):
        hc = history_card(1919, r"Ronald Aylmer Fisher, \ aged 29", r"hired by the station's director, \ John Russell, \ to see "
                          r"what statistics could extract from the records", color=OBS, width=9.6, font_size=24).move_to([0, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"\emph{Studies in Crop Variation I} \ (1921): \ the Broadbalk yields, \ 1852--1918", font_size=24),
            label(r"the weather, \ the weeds, \ the drift of the soil, \ a change of variety: \ all tangled with the manures", font_size=24,
                  color=RES),
            label(r"the records needed assumptions to identify manure effects", font_size=26, color=OBS),
            label(r"a job he is said to have called \ ``raking over the muck heap''", font_size=22, color=GREY_A),
        ), 12.4, 0.32, [0, -1.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1919 the director, John Russell, hired a twenty-nine-year-old mathematician, Ronald "
            "Fisher, to see what statistics could make of the records. <bookmark mark='b'/> Fisher's first papers, Studies in "
            "Crop Variation, analysed the Broadbalk yields from 1852 onward. He found slow trends, cycles and the effects of "
            "rainfall. <bookmark mark='c'/> But every comparison was tangled: a strip that did well might have had the better "
            "soil, the drier corner, fewer weeds, or a later variety of wheat. <bookmark mark='d'/> Seventy years of "
            "observations could describe what had happened. They could not isolate what a manure does without additional assumptions about soil, weather and the changing practices. <bookmark mark='e'/> "
            "Fisher is said to have described the job as raking over the muck heap."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def uniformity(self):
        d = load("field")
        u = np.asarray(d["uniform"])
        fp = field_from(u, cell=0.4, center=[-3.0, 0.1, 0], lo=40, hi=60)
        key = soil_key(40, 60, [3.6, -2.9, 0], text=r"yield of one plot, \ bushels per acre")
        rows = fit_rows(VGroup(
            label(r"a uniformity trial: \ 144 plots, \ every one treated alike", font_size=24),
            label(rf"yet the yields range from {u.min():.0f} to {u.max():.0f}, \ in patches and a drift", font_size=24, color=S.LIK),
            label(rf"plot-to-plot variation: \ {100 * d['uniform_cv']:.0f}\% of the mean", font_size=24),
            label(r"a manure worth 4\% would hide inside the soil's own noise", font_size=24, color=RES),
            label(r"Mercer \& Hall (1911) \ harvested 500 such plots of wheat at Rothamsted", font_size=22, color=GREY_A),
        ), 5.4, 0.36, [3.6, 0.0, 0])
        tag = simulated_tag(r"the field-trial simulator", corner=DR)
        with self.voiceover(
            "Here's the difficulty Fisher faced, on our own simulated field. <bookmark mark='a'/> This is a uniformity trial: a "
            "field cut into a hundred and forty-four plots, every one sown, manured and harvested in exactly the same way. "
            "<bookmark mark='b'/> Yet the yields range from about forty-one to about sixty bushels per acre, in patches, with a "
            "drift from west to east. <bookmark mark='c'/> The soil's own variation, from one plot to the next, is about eight "
            "percent of the average. <bookmark mark='d'/> A new manure that adds four percent would be invisible in a single "
            "comparison, and a manure that happened to land on the better side of the field would look like a miracle. "
            "<bookmark mark='e'/> Real uniformity trials like this one were harvested at Rothamsted: Mercer and Hall cut five "
            "hundred plots of wheat in 1910 and published them in 1911. That's what any experiment on land is up against."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fp, lag_ratio=0.01), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(key), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2], shift=RIGHT * 0.2))
        self.clear_scene()

    def questionnaire(self):
        q1 = VGroup(
            label(r"``No aphorism is more frequently repeated in connection with field trials, \ than that we must ask Nature",
                  font_size=26),
            label(r"few questions, \ or, \ ideally, \ one question, \ at a time. \ The writer is convinced that this view is",
                  font_size=26),
            label(r"wholly mistaken. \ Nature, \ he suggests, \ will best respond to a logical and carefully thought out",
                  font_size=26),
            label(r"questionnaire.''", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if q1.width > 12.6:
            q1.width = 12.6
        q1.move_to([0, 1.6, 0])
        s1 = label(r"R. A. Fisher, \ ``The arrangement of field experiments'' \ (1926)", font_size=22, color=GREY_B).next_to(q1, DOWN, buff=0.25)
        q2 = VGroup(label(r"``To consult the statistician after an experiment is finished is often merely to ask him", font_size=26, color=OBS),
                    label(r"to conduct a post mortem examination. \ He can perhaps say what the experiment died of.''", font_size=26,
                          color=OBS)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if q2.width > 12.6:
            q2.width = 12.6
        q2.move_to([0, -1.4, 0])
        s2 = label(r"R. A. Fisher, \ address to the Indian Statistical Congress \ (1938)", font_size=22, color=GREY_B).next_to(q2, DOWN, buff=0.25)
        with self.voiceover(
            "Fisher's answer was not a cleverer analysis of the old records. It was to design the data. <bookmark mark='a'/> "
            "In 1926 he wrote: No aphorism is more frequently repeated in connection with field trials, than that we must ask "
            "Nature few questions, or, ideally, one question, at a time. The writer is convinced that this view is wholly "
            "mistaken. Nature, he suggests, will best respond to a logical and carefully thought out questionnaire. "
            "<bookmark mark='b'/> And, twelve years later, more bluntly: to consult the statistician after an experiment is "
            "finished is often merely to ask him to conduct a post mortem examination. He can perhaps say what the experiment "
            "died of. This part is about the questionnaire: how to design an experiment so that its answer is unambiguous."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q1, lag_ratio=0.1), FadeIn(s1), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(q2), FadeIn(s2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 13", font_size=34, color=GREY_B), label(r"Experiments by Design", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"replication, \ randomization, \ local control; \ randomization as the basis of inference",
            r"the analysis of variance as Pythagoras; \ contrasts and many comparisons",
            r"blocks, \ Latin squares, \ crossovers; \ factorials, \ fractions, \ response surfaces",
            r"split plots and their two errors; \ optimal design; \ power",
            r"today's experiments: \ A/B tests, \ CUPED, \ sample-ratio mismatch",
        ], color=OBS, font_size=26)
        prereq = note(r"prerequisites: \ Parts 10 and 12").to_corner(DL, buff=0.3)
        built = note(r"built: \ the field-trial simulator; \ \texttt{statkit.design}").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part thirteen: experiments by design. <bookmark mark='b'/> We'll meet Fisher's three "
            "principles, and see randomization become the basis of inference itself; build the analysis of variance as "
            "Pythagoras, and handle many comparisons honestly; control the field with blocks and Latin squares; ask many "
            "questions at once with factorials, their fractions and response surfaces; meet the split plot, with its two "
            "kinds of error; choose design points optimally and plan for power; and end with the experiments that run on "
            "websites today, millions of times a year."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
