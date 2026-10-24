from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (AUG, LEAN_C, MSA_C, PAIR_C, PART, PLAIN, SEARCH_C, STRUCT, SYM, TRUE_C,
                                   years_line)


class History(VoiceoverScene):
    def construct(self):
        self.card()
        self.prelude()
        self.decade()
        self.blueprint()

    def card(self):
        card = chapter_card(1, r"How we got here", r"Where did symmetry meet science?", lit=(1975, 1998, 2011),
                            part=PART)
        with self.voiceover("Chapter one. How we got here."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def prelude(self):
        events = [
            (1950, r"the first computer \\ weather forecast", TRUE_C),
            (1958, r"the first protein \\ structure: myoglobin", PAIR_C),
            (1961, r"Anfinsen: the sequence \\ decides the fold", PAIR_C),
            (1968, r"Weisfeiler and Leman: \\ colour refinement", STRUCT),
            (1971, r"the Protein \\ Data Bank", PAIR_C),
            (1979, r"ECMWF's first \\ medium-range forecast", TRUE_C),
            (1989, r"convolutions: \\ shift symmetry built in", STRUCT),
            (1994, r"CASP: blind tests \\ of folding", PAIR_C),
            (2005, r"the graph \\ neural network", STRUCT),
        ]
        base, items = years_line(events, T0=1945, T1=2012, ticks=(1950, 1970, 1990, 2010), font_size=20)
        head = label(r"How we got here: \ the long prelude", font_size=36).to_edge(UP, buff=0.4)
        groups = [[0], [1, 2], [3], [4], [5], [6], [7], [8]]
        with self.voiceover(
            "This part's story has three threads, and they started far apart. <bookmark mark='m0'/> The first "
            "computer weather forecast, in 1950. <bookmark mark='m1'/> The first protein seen in three dimensions, "
            "in 1958, and in 1961 Christian Anfinsen's discovery that the sequence decides the shape. <bookmark "
            "mark='m2'/> In 1968, a test of whether two graphs are the same, which turns out to measure what graph "
            "networks can see. <bookmark mark='m3'/> The Protein Data Bank, 1971; <bookmark mark='m4'/> the first "
            "forecast of Europe's weather centre, 1979; <bookmark mark='m5'/> convolutions, with the symmetry of "
            "images built in, 1989; <bookmark mark='m6'/> CASP's blind contests in protein structure, 1994; "
            "<bookmark mark='m7'/> and the first neural networks on graphs, 2005."
        ) as vo:
            self.play(FadeIn(head), Create(base[0]), FadeIn(base[1]))
            for k, mk in enumerate(["m0", "m1", "m2", "m3", "m4", "m5", "m6", "m7"]):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(items[i], shift=UP * 0.1) for i in groups[k]], lag_ratio=0.4),
                          run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decade(self):
        events = [
            (2017, r"message passing; \\ Deep Sets; SchNet", STRUCT),
            (2018, r"AlphaFold \\ tops CASP13", PAIR_C),
            (2020, r"AlphaFold 2 \\ at CASP14", PAIR_C),
            (2021, r"EGNN; neural \\ operators", STRUCT),
            (2022, r"$200$ million \\ predicted structures", PAIR_C),
            (2023, r"GraphCast; GNoME; \\ RFdiffusion; FunSearch", TRUE_C),
            (2024, r"the Nobel; AlphaFold 3; \\ AlphaGeometry; AlphaProof", PAIR_C),
            (2025, r"AI forecasts go operational; \\ AlphaEvolve; olympiad gold", SEARCH_C),
            (2026, r"Erd\H{o}s problems \\ resolved by AI", LEAN_C),
        ]
        base, items = years_line(events, x0=-6.2, x1=6.0, T0=2016, T1=2027, ticks=(2016, 2020, 2024),
                                 font_size=19)
        head = label(r"How we got here: \ the decade", font_size=36).to_edge(UP, buff=0.4)
        groups = [[0], [1, 2], [3], [4], [5], [6], [7], [8]]
        with self.voiceover(
            "Then, within a decade, the threads met. <bookmark mark='d0'/> 2017: message passing, and networks for "
            "sets and molecules. <bookmark mark='d1'/> 2018: DeepMind's first AlphaFold wins CASP; in 2020 AlphaFold 2 "
            "comes close to experiment. <bookmark mark='d2'/> 2021: networks that turn with a molecule, and networks "
            "that learn whole solutions of equations. <bookmark mark='d3'/> 2022: predicted structures for over two "
            "hundred million proteins, free to download. <bookmark mark='d4'/> 2023: a graph network out-forecasts "
            "the best weather model in the world on most measures, and another proposes millions of new crystals. <bookmark "
            "mark='d5'/> 2024: the Nobel Prize, AlphaFold 3, machines solving olympiad problems; <bookmark "
            "mark='d6'/> 2025: AI forecasts in daily operation, new mathematics from evolutionary search; <bookmark "
            "mark='d7'/> 2026: open problems of Paul Erdős resolved by AI."
        ) as vo:
            self.play(FadeIn(head), Create(base[0]), FadeIn(base[1]))
            for k, mk in enumerate(["d0", "d1", "d2", "d3", "d4", "d5", "d6", "d7"]):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(items[i], shift=UP * 0.1) for i in groups[k]], lag_ratio=0.4),
                          run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blueprint(self):
        head = label(r"The recipe: \ find the symmetry, \ build it in", font_size=36).to_edge(UP, buff=0.35)
        cols = [r"data", r"what doesn't matter", r"the network", r"where"]
        rows = [
            (r"images", r"shifts", r"convolutions", r"Part 10"),
            (r"sets of points", r"the order", r"Deep Sets", r"chapter 3"),
            (r"graphs", r"the numbering of nodes", r"message passing", r"chapters 4--6"),
            (r"molecules", r"turns, shifts, reflections", r"equivariant networks", r"chapter 7"),
            (r"proteins", r"all of the above", r"AlphaFold", r"chapters 8--12"),
            (r"fields on a sphere", r"the grid", r"mesh networks, \ operators", r"chapters 13--14"),
            (r"sequences of words", r"(little)", r"transformers", r"Parts 13--19"),
        ]
        xs = [-5.0, -1.6, 2.0, 5.4]
        y0 = 1.95
        hrow = VGroup(*[label(c, font_size=24, color=GREY_A).move_to([x, y0, 0]) for c, x in zip(cols, xs)])
        rule = Line([-6.6, y0 - 0.32, 0], [6.6, y0 - 0.32, 0], color=GREY_D, stroke_width=1.2)
        table = VGroup()
        colors = [WHITE, SYM, STRUCT, GREY_B]
        for k, r in enumerate(rows):
            y = y0 - 0.72 - 0.56 * k
            table.add(VGroup(*[label(t, font_size=23, color=c).move_to([x, y, 0]) for t, c, x in zip(r, colors, xs)]))
        gdl = label(r"Bronstein, Bruna, Cohen \& Veli\v{c}kovi\'c (2021): \ grids, groups, graphs, geodesics, gauges",
                    font_size=22, color=GREY_B).to_edge(DOWN, buff=0.45)
        three = label(r"three ways to get a symmetry: \ show transformed copies, \ put inputs in a standard pose, \ "
                      r"or build it into the layers", font_size=22, color=AUG).next_to(gdl, UP, buff=0.25)
        with self.voiceover(
            "What ties these together is one recipe. <bookmark mark='a'/> Ask what about your data doesn't matter. "
            "For an image, where the object sits: so convolutions. <bookmark mark='b'/> For a set of points, their "
            "order. <bookmark mark='c'/> For a graph, how its nodes happen to be numbered. <bookmark mark='d'/> For "
            "a molecule, how it is turned or moved in space. <bookmark mark='e'/> A protein has all of these at once. "
            "<bookmark mark='f'/> A weather field lives on a sphere, and shouldn't depend on the grid it was stored "
            "on. <bookmark mark='g'/> Language, by contrast, has little symmetry to exploit, which is one reason the "
            "transformer learns its structure from data instead. <bookmark mark='h'/> Michael Bronstein, Joan Bruna, "
            "Taco Cohen and Petar Veličković called this programme geometric deep learning. And there are three "
            "ways to get a symmetry into a model: show it transformed copies of the data, put every input into a "
            "standard pose first, or build the symmetry into the layers. This part is mostly about the third."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hrow), Create(rule))
            for k, mk in enumerate("abcdefg"):
                vo.wait_until(mk)
                self.play(FadeIn(table[k], shift=UP * 0.1), run_time=0.8)
            vo.wait_until("h")
            self.play(FadeIn(gdl))
            self.play(FadeIn(three))
        self.wait(0.3)
        self.clear_scene()
