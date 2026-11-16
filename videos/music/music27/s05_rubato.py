from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403

ORDER = ["strict", "arch", "melody"]
NAME = {"strict": r"strict", "arch": r"a phrase arch: \ both hands bend", "melody": r"stolen time: \ only the melody bends"}
COL = {"strict": GREY_A, "arch": TUNE, "melody": EAR}


class Rubato(SoundScene):
    def construct(self):
        chapter(self, 4, r"Stolen time", r"What does a pianist do with the tempo?", extra=((1777, r"Mozart's letter on rubato"),))
        self.letter()
        self.curve()
        self.three()
        self.models()

    # ------------------------------------------------------------------
    def letter(self):
        items = [
            (r"\textit{tempo rubato}: \ `stolen time', \ taken from some notes and given to others", WHITE),
            (r"Mozart, \ 1777, \ to his father: \ in an adagio the left hand keeps time \ `and knows nothing of it'", WHITE),
            (r"Chopin's pupils describe the same: \ a steady accompaniment, \ a free melody", WHITE),
            (r"later the whole texture bends together: \ slower at the ends of phrases, \ faster in the middle", TUNE),
            (r"two kinds of rubato, \ both heard below", GREY_A),
        ]
        rows_scene(self, r"tempo rubato", items,
                   "The mazurka's limp is one kind of freedom with time; the century had a name for the general idea. "
                   "<bookmark mark='b'/> Tempo rubato means stolen time: time taken from some notes and given to others. "
                   "<bookmark mark='c'/> Mozart described it in a letter to his father in 1777: in an adagio, he wrote, his "
                   "left hand kept strict time and knew nothing of what the right hand was doing. <bookmark mark='d'/> "
                   "Chopin's pupils described the same thing in his playing, a steady accompaniment under a free melody. "
                   "<bookmark mark='e'/> Another usage concerns, to the whole texture slowing and quickening together, "
                   "slower at the ends of phrases and faster in their middles. <bookmark mark='f'/> Both kinds can be "
                   "modelled, and heard.", marks="cdef")

    # ------------------------------------------------------------------
    def curve(self):
        d = load("rubato")
        grid, tempo = np.array(d["grid"]), np.array(d["tempo_arch"])
        ax = Axes(x_range=[0, 16, 2], y_range=[0.7, 1.3, 0.1], x_length=9.0, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 18}).move_to(DOWN * 0.3)
        flat = ax.plot_line_graph(grid, np.ones_like(grid), line_color=GREY_B, add_vertex_dots=False, stroke_width=3)
        arc = ax.plot_line_graph(grid, tempo, line_color=TUNE, add_vertex_dots=False, stroke_width=4)
        xl = label(r"beats: \ two phrases of eight", font_size=19, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = label(r"tempo, \ relative", font_size=19, color=GREY_A).next_to(ax, LEFT, buff=0.15).shift(UP * 1.0)
        head = label(r"a phrase arch \ (after Todd, \ 1992): \ speed up into the middle, \ slow into the end", font_size=24, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The second kind has a simple model, the phrase arch, after the psychologist Neil Todd. <bookmark mark='a'/> Strict time is a flat line. <bookmark mark='b'/> Under the arch, each phrase begins a little slow, speeds into its middle, and slows again into its end, here a tenth faster in the middle and a fifth slower at the ends; final slowing can cue closure alongside other musical features. Measurements of many pianists playing the same piece, by Bruno Repp among others, find shapes like this, with every player bending a little differently."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(flat))
            vo.wait_until("b")
            self.play(Create(arc), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three(self):
        d = load("rubato")
        c = clip("rubato.three")
        unit = d["unit"]
        rows_ = VGroup()
        for k in ORDER:
            on = d["onsets"][k]
            mel = [[p, a_, dd] for (p, _, dd), a_ in zip(d["melody"], on)]
            g = mroll(mel, width=8.0, height=0.9, lo=70, hi=84, color=COL[k], total=18.5, bar_h=0.1)
            rows_.add(VGroup(label(NAME[k], font_size=20, color=COL[k]), g).arrange(RIGHT, buff=0.45))
        rows_.arrange(DOWN, buff=0.45, aligned_edge=RIGHT).move_to(DOWN * 0.1 + RIGHT * 0.3)
        head = label(r"the Tune's first two phrases, \ three ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Three performances of the Tune's first two phrases on Part 7's piano, with its accompaniment. "
            "Strict. Then under the phrase arch, both hands bending together. Then Mozart's stolen time: the left hand "
            "strict, the melody pushing ahead early in each bar and catching up at the bar line. Watch the notes shift."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"strict, \ arch, \ stolen", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(ORDER):
                st = d["starts"][k]
                g = rows_[i][1]
                times = [st + unit * t for t in d["onsets"][k]]
                flash(snd, g.notes, times, hot=WHITE, base=COL[k])
                end = d["starts"][ORDER[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, rows_[i][0], st, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def models(self):
        items = [
            (r"performance as data: \ onset times measured from recordings, \ beat by beat", WHITE),
            (r"Repp \ (1992): \ 28 recordings of Schumann's \textit{Träumerei}: \ a shared shape, \ individual bends", WHITE),
            (r"the Mazurka Project \ (CHARM, \ 2006--2009): \ thousands of recordings of Chopin's mazurkas", WHITE),
            (r"a model is a hypothesis about a style of playing, \ tested against those numbers", TUNE),
            (r"Part 43 builds a performer: \ tempo, \ dynamics and the evidence of recordings", GREY_A),
        ]
        rows_scene(self, r"performances measured", items,
                   "Performance has become data. <bookmark mark='b'/> Researchers mark the onset of every beat in a "
                   "recording and turn a performance into a tempo curve. <bookmark mark='c'/> Bruno Repp measured twenty-eight "
                   "recordings of Schumann's Träumerei and found a shape they shared, each pianist bending it in their own way. "
                   "<bookmark mark='d'/> The Mazurka Project in London measured beat timings and loudness in thousands of "
                   "recordings of Chopin's mazurkas. <bookmark mark='e'/> A model such as the phrase arch is then a hypothesis "
                   "about a style of playing, which those numbers can test. <bookmark mark='f'/> Part 43 builds a performer "
                   "from them.", marks="cdef")
