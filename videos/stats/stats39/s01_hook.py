from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.boreholes()
        self.matheron()
        self.question()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1951,)).to_edge(UP, buff=0.35)
        hc = history_card(1951, r"Danie Krige, \ \emph{A Statistical Approach to Some Basic Mine Valuation Problems on the Witwatersrand}",
                          r"A young South African mining engineer had core samples from boreholes, \ a few centimetres across, \ and "
                          r"had to value whole blocks of ore around them. \ Averaging the nearby samples overvalued rich blocks and "
                          r"undervalued poor ones; \ the samples were correlated with each other and with the block, \ and the "
                          r"right weights had to account for both",
                          color=FIELDC, width=11.2, font_size=22).move_to([0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(r"the question: \ the value of the ground where nobody drilled", font_size=24, color=TAUC),
            label(r"the answer: \ weights from how values covary with distance", font_size=24, color=FIELDC),
        ), 12.0, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1951 Danie Krige, a young mining engineer on South Africa's Witwatersrand gold "
            "fields, published a master's thesis about a very practical question. Mines drilled boreholes and assayed"
            " the cores, a few centimetres across, and then had to decide which blocks of ore, many metres across, "
            "were worth mining. Naively treating selected rich or poor samples as representative of a whole block "
            "misses regression toward the mean and differences in sampling support. <bookmark mark='b'/> The real "
            "question was the value of the ground where nobody had drilled. <bookmark mark='c'/> Krige's answer was "
            "to weight the samples using how gold grades covary with distance: with each other, and with the block."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def boreholes(self):
        d = load("world")
        px, py, truth = (np.asarray(d[k], float) for k in ("px", "py", "truth"))
        F = FieldSurface(px, py, truth, 0.2, width=8.0, center=[-1.6, 0.2, 0])
        sx, sy = np.asarray(d["sx"], float), np.asarray(d["sy"], float)
        pick = np.random.Generator(np.random.PCG64(3912)).choice(len(sx), 40, replace=False)
        st = F.dots(sx[pick], sy[pick], WHITE, 0.06)
        q = F.dots([0.5], [0.3], TAUC, 0.12)
        side = fit_rows(VGroup(
            label(r"the World's pollution field \ (hidden)", font_size=22, color=FIELDC),
            label(r"white: \ 40 measuring stations", font_size=22, color=GREY_A),
            label(r"gold: \ a place nobody measured", font_size=22, color=TAUC),
            label(r"what is the value there,", font_size=22, color=GREY_A),
            label(r"and how sure can we be?", font_size=22, color=GREY_A),
        ), 3.6, 0.42, [5.0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same problem in the World. Here is the pollution field over the island, which in "
            "real life nobody ever sees. <bookmark mark='b'/> We see it only at a scattering of measuring stations. "
            "<bookmark mark='c'/> And we want its value at a place nobody measured: a new school, a hospital, a home. "
            "<bookmark mark='d'/> What should we predict there, and how sure can we be? That is the question of this part."
        ) as vo:
            self.add(pollution_tag())
            vo.wait_until("a")
            self.play(FadeIn(F), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(st), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(q), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def matheron(self):
        rows = fit_rows(VGroup(
            label(r"Georges Matheron \ (Paris School of Mines, \ 1962--63): \ geostatistics, \ and the name ``kriging''", font_size=26, color=TAUC),
            label(r"independently: \ Lev Gandin \ (1963), \ objective analysis of weather maps", font_size=26),
            label(r"the same mathematics: \ Wiener--Kolmogorov prediction, \ and Gaussian processes in machine learning", font_size=26, color=FIELDC),
            label(r"today: \ mining, \ air pollution, \ climate, \ epidemiology, \ ecology, \ and tuning neural networks", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Georges Matheron, at the Paris School of Mines, turned Krige's idea into a theory in 1962 "
            "and 1963, called it geostatistics, and named the method kriging, after Krige. <bookmark mark='b'/> In the "
            "Soviet Union, Lev Gandin developed the same method at the same time, for weather maps. <bookmark mark='c'/> It "
            "is the same mathematics as Wiener and Kolmogorov's prediction of stationary processes, and as the Gaussian "
            "processes of modern machine learning. <bookmark mark='d'/> It is now used for mining, air pollution, climate, "
            "epidemiology and ecology, and, chapter thirteen, for tuning neural networks."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"Part 38: \ dependence in time, \ one direction, \ the past", font_size=26, color=GREY_A),
            label(r"here: \ dependence in every direction, \ and no natural order", font_size=26, color=FIELDC),
            label(r"how do values covary with distance? \ \ how should we predict? \ \ what can we learn?", font_size=26, color=TAUC),
            label(r"and: \ counts in areas, \ points in a window, \ and fields that change in time", font_size=26, color=AREAC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-eight's dependence ran in one direction, from the past. <bookmark mark='b'/> "
            "In space it runs in every direction at once, and there is no natural order to filter along. <bookmark "
            "mark='c'/> How do values covary with distance? How should we predict from them? And what can, and cannot, be "
            "learned from one realization of a field? <bookmark mark='d'/> We'll also meet counts in areas, points in a "
            "window, and fields that change in time."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 39", font_size=34, color=GREY_B), label(r"Space", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"random fields, \ Bochner, \ variograms; \ kriging as the best linear predictor",
            r"Mat\'ern smoothness, \ what cannot be learned, \ ML and REML",
            r"scaling: \ Vecchia, \ nearest-neighbour GPs, \ GMRFs and the SPDE",
            r"areal data and disease maps; \ point processes and Snow's map",
            r"spatial confounding; \ space--time; \ GPs in machine learning; \ honest prediction",
        ], color=TAUC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 25 and 29").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.spatial}; \ the field surface; \ data: \ Meuse, \ Snow's map").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-nine: space. <bookmark mark='b'/> We'll describe random fields and their "
            "variograms; derive kriging; meet the Matérn family and a parameter fixed-domain sampling cannot consistently separate from the variance; estimate by "
            "likelihood, and scale it to a hundred thousand locations; map disease rates in areas, and test point patterns, "
            "including Snow's map; see how spatial random effects can confound a regression; move to space and time; and "
            "end with Gaussian processes in machine learning, and honest prediction."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
