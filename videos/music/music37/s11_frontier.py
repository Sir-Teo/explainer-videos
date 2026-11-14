from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ timing measured", r"Is a beat always divided into equal parts?")
        self.polak()
        self.hear()
        self.cultures()
        self.problem()
        self.archives()

    # ------------------------------------------------------------------
    def polak(self):
        items = [
            (r"timelines are written on equal pulses; \ are they played that way?", WHITE),
            (r"Rainer Polak \ (2010) \ measured jembe drumming from Mali, \ stroke by stroke", WHITE),
            (r"the three parts of a beat were systematically \textit{unequal}, \ in consistent proportions", WHITE),
            (r"Polak and London \ (2014): \ an uneven grid can be a meter in its own right", TUNE),
            (r"not sloppiness, \ and not swing: \ a learned, \ shared template", GREY_A),
        ]
        rows_scene(self, r"non-isochronous subdivision", items,
                   "Every timeline in this part was written on equal pulses. Are they played that way? "
                   "<bookmark mark='b'/> In 2010 Rainer Polak published measurements of jembe drumming from Mali, stroke by "
                   "stroke. <bookmark mark='c'/> In some pieces the three parts of each beat were systematically unequal, in "
                   "proportions that were consistent within and across performances. <bookmark mark='d'/> Polak and Justin London "
                   "argued in 2014 that such an uneven grid can be a meter in its own right. <bookmark mark='e'/> It is not "
                   "sloppiness, and not swing as Part 38 will measure it, but a learned and shared template.", marks="bcde")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("uneven")
        def beat_row(props, col, name):
            g = VGroup()
            for b in range(4):
                for k, pr in enumerate(props):
                    g.add(Rectangle(width=2.2 * pr, height=0.55, stroke_color=GREY_B, stroke_width=1.2, fill_color=col, fill_opacity=0.75 if k == 0 else 0.35))
            g.arrange(RIGHT, buff=0.0)
            return VGroup(label(name, font_size=19, color=col), g).arrange(RIGHT, buff=0.35)
        card = listen_card(r"A drum divides each beat into three. \ It plays twice: \ once with three equal parts, \ "
                           r"once with three unequal ones. \ Which is unequal, \ the first or the second?", width=10.4)
        with self.voiceover(
            "A question for your ears. A drum divides each beat into three strokes, and plays twice: once with the three "
            "parts equal, once with them unequal, short, medium and long, in proportions of our own that are not a "
            "measurement of any piece. Which is the unequal one, the first or the second?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ev = beat_row(d["even"], BLUE, r"first")
        un = beat_row(d["uneven"], EAR, r"second")
        rows_ = VGroup(ev, un).arrange(DOWN, buff=0.6, aligned_edge=RIGHT).move_to(UP * 0.4)
        cover = VGroup(*[SurroundingRectangle(r[1], buff=0.05, stroke_width=0, fill_color=BLACK, fill_opacity=1.0) for r in rows_])
        props = label(r"illustrative proportions \ (ours): \ " + r" \ : \ ".join(f"{x:.2f}" for x in d["uneven"]), font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        self.play(FadeOut(card), FadeIn(rows_), FadeIn(cover))
        beat = d["beat"]
        clips_ = {"even": clip("uneven.even"), "uneven": clip("uneven.uneven")}
        for name, row, prop in (("even", ev, d["even"]), ("uneven", un, d["uneven"])):
            c = clips_[name]
            offs = np.concatenate([[0.0], np.cumsum(prop)])
            with self.listen(c) as snd:
                window(snd, {"even": r"the first", "uneven": r"the second"}[name], detail=r"membrane models", corner=DL, tag_corner=DR)
                pulse(snd, row[0], 0.0, c.duration, buff=0.1)
            self.wait(0.3)
        with self.voiceover(
            "The second is the unequal one. Here are both, drawn to scale: in the first the three parts of each beat are the "
            "same width; in the second they grow, short, medium, long."
        ):
            self.play(FadeOut(cover), FadeIn(props))
        ans = label(r"steady, \ but on a different grid", font_size=22, color=TUNE).next_to(props, UP, buff=0.4)
        with self.voiceover(
            "To most listeners raised on equal subdivisions the second sounds lopsided at first, and then steady, but on a "
            "different grid. To musicians who grew up with it, the uneven grid is simply the right one."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cultures(self):
        items = [
            (r"Hannon and Trehub \ (2005): \ six-month-olds notice changes in Balkan meters that North American adults miss", WHITE),
            (r"by twelve months, \ infants have tuned to their own culture's meters", WHITE),
            (r"Jacoby and McDermott \ (2017): \ listeners' reproductions of random rhythms are drawn to simple ratios", WHITE),
            (r"Jacoby and colleagues \ (2024), \ fifteen countries: \ simple ratios everywhere, \ but which ones depends on culture", TUNE),
            (r"Part 47 asks what is universal and what is learned", GREY_A),
        ]
        rows_scene(self, r"meter across cultures", items,
                   "How much of meter is learned? <bookmark mark='b'/> Erin Hannon and Sandra Trehub found in 2005 that "
                   "six-month-old infants notice changes to Balkan meters that North American adults miss, <bookmark mark='c'/> "
                   "and that by twelve months infants have tuned to the meters of their own culture. <bookmark mark='d'/> Nori "
                   "Jacoby and Josh McDermott showed in 2017 that when people reproduce random rhythms, over and over, their "
                   "reproductions are drawn towards simple ratios. <bookmark mark='e'/> And a study of fifteen countries led by "
                   "Jacoby in 2024 found such pulls everywhere, but towards different ratios in different cultures. "
                   "<bookmark mark='f'/> Part 47 asks what is universal in music and what is learned.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"record players and listeners from several traditions, \ with motion capture of the dance", WHITE),
            (r"measure the timing of every stroke, \ and where each body places the beat", WHITE),
            (r"run the reproduction experiment with uneven grids as starting points", WHITE),
            (r"$\bigstar$ \ research problem: \ how are rhythm categories learned, \ and how fast can they change?", EAR),
            (r"the answer would say how much of a timeline lives in the ear, \ and how much in the body", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Record players and listeners from several traditions, with motion "
            "capture of the dance. <bookmark mark='b'/> Measure the timing of every stroke, and where each body places the "
            "beat. <bookmark mark='c'/> Run the reproduction experiment starting from uneven grids, and see where people's "
            "rhythms drift. <bookmark mark='d'/> How are rhythm categories learned, and how fast can they change? "
            "<bookmark mark='e'/> The answer would say how much of a timeline lives in the ear, and how much in the body."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def archives(self):
        items = [
            (r"Hugh Tracey recorded across southern and central Africa from the 1920s; \ his archive, \ ILAM, \ is in Makhanda, \ South Africa", WHITE),
            (r"projects now return copies of such recordings to the communities they came from", WHITE),
            (r"Solomon Linda's \textit{Mbube} \ (1939) \ became a world hit; \ his family were paid only after a 2006 settlement", WHITE),
            (r"credit, \ consent and royalties are part of studying music: \ the people are not data", TUNE),
            (r"Part 67 sets out how to do research with traditions well", GREY_A),
        ]
        rows_scene(self, r"archives and ethics", items,
                   "Studying this music raises questions of ownership. <bookmark mark='b'/> Hugh Tracey recorded across southern "
                   "and central Africa from the nineteen-twenties, and his archive, the International Library of African Music, "
                   "is in Makhanda in South Africa. <bookmark mark='c'/> Projects now return copies of such recordings to the "
                   "communities they came from. <bookmark mark='d'/> Solomon Linda's Mbube, recorded in 1939, became a world hit "
                   "under other names, and his family were paid only after a settlement in 2006. <bookmark mark='e'/> Credit, "
                   "consent and royalties are part of studying music; the people are not data. <bookmark mark='f'/> Part 67 sets "
                   "out how to do research with traditions well.", marks="cdef")
