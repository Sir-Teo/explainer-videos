from __future__ import annotations

import numpy as np

from videos.music.music31.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 8, r"Frontier: \ other spaces, \ real listeners", r"Do listeners feel distance on the Tonnetz?")
        self.listeners()
        self.vl()
        self.spaces()
        self.machines()
        self.audit()
        self.problem()

    # ------------------------------------------------------------------
    def listeners(self):
        items = [
            (r"Krumhansl \ (1998): \ listeners rated how well pairs of triads fit together", WHITE),
            (r"her ratings tracked distance on the circle of keys \ ---\ and also, \ separately, \ the PLR moves", WHITE),
            (r"the two descriptions are dual mathematically, \ but they predict different things for the ear", WHITE),
            (r"trained and untrained listeners, \ film-literate or not, \ may differ", TUNE),
            (r"the evidence is a handful of experiments, \ with small samples", GREY_A),
        ]
        rows_scene(self, r"what listeners hear", items,
                   "Do listeners feel these distances? <bookmark mark='b'/> In 1998 Carol Krumhansl asked listeners to rate how "
                   "well pairs of triads fitted together. <bookmark mark='c'/> Her results followed distance on the circle of "
                   "keys, and also, separately, the PLR moves. <bookmark mark='d'/> The two descriptions are dual for the "
                   "mathematics, but they make different predictions for the ear. <bookmark mark='e'/> Listeners with different "
                   "training, or different exposure to film music, may also differ. <bookmark mark='f'/> And the evidence is still "
                   "a handful of experiments, with small samples.", marks="cdef")

    # ------------------------------------------------------------------
    def spaces(self):
        items = [
            (r"generalized Tonnetze: \ other intervals on the axes, \ other chords as triangles", WHITE),
            (r"Tymoczko's orbifolds: \ every chord of n notes a point, \ voice leadings as paths \ (Part 32)", WHITE),
            (r"the Fourier view \ (Part 29): \ triads' place in a space of spectral magnitudes", WHITE),
            (r"which space matches the ear best is an open question", TUNE),
            (r"each makes testable predictions about similarity and surprise", GREY_A),
        ]
        rows_scene(self, r"other spaces", items,
                   "Theorists have built other spaces too. <bookmark mark='b'/> Generalized Tonnetze put other intervals on the "
                   "axes and other chords in the triangles. <bookmark mark='c'/> Tymoczko's geometry makes every chord of n notes "
                   "a point and every voice leading a path, as Part 32 will show. <bookmark mark='d'/> Part 29's Fourier view "
                   "places triads in a space of spectral magnitudes. <bookmark mark='e'/> Which space best matches what the ear "
                   "does is open, <bookmark mark='f'/> and each one makes testable predictions about similarity and surprise.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"choose pairs of triads that the key circle and the Tonnetz rank differently", WHITE),
            (r"collect similarity and `fit' ratings from listeners with varied training", WHITE),
            (r"fit models from each space and compare them, \ with intervals", WHITE),
            (r"$\bigstar$ \ research problem: \ which geometry of triads matches what listeners hear?", EAR),
            (r"the answer would say whether the moves are a theory of hearing or only of writing", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Choose pairs of triads that the circle of keys and the Tonnetz rank "
            "differently. <bookmark mark='b'/> Collect ratings of similarity and fit from listeners with varied training. "
            "<bookmark mark='c'/> Fit a model from each space and compare them, with intervals. <bookmark mark='d'/> Which "
            "geometry of triads matches what listeners hear? <bookmark mark='e'/> The answer would say whether these moves "
            "are a theory of hearing, or only of writing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vl(self):
        d = load("vl")
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 7, 1], x_length=6.4, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 18}).move_to(LEFT * 2.4 + DOWN * 0.3)
        rng = np.random.default_rng(0)
        dots = VGroup(*[Dot(ax.c2p(r["plr"] + rng.uniform(-0.12, 0.12), r["vl"] + rng.uniform(-0.12, 0.12)), radius=0.07,
                            color=TUNE if not r["triad"].endswith("m") else BLUE) for r in d["rows"]])
        xl = label(r"P, \ L, \ R steps from C major", font_size=19, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = label(r"semitones of voice leading", font_size=19, color=GREY_A).next_to(ax.y_axis, UP, buff=0.15).shift(RIGHT * 1.0)
        side = VGroup(*[label(s, font_size=20, color=c_) for s, c_ in (
            (rf"correlation: \ {d['r']:.2f}", TUNE),
            (r"close in moves: \ usually close \\ in voice leading", WHITE),
            (rf"but not always: \ {d['max_vl']} semitones \\ for D, \ F$\sharp$ and B$\flat$ major", EAR),
            (r"two distances: \\ which does the ear use?", GREY_A))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.move_to(RIGHT * 4.2 + DOWN * 0.2)
        with self.voiceover(
            "The film can at least compare two measures of distance. For each of the twenty-three other triads, its distance "
            "from C major in P, L and R steps, and the fewest semitones the three voices must move to reach it. "
            f"<bookmark mark='a'/> The two agree fairly well, a correlation of {say(d['r'], 2)}. <bookmark mark='b'/> "
            "Close in moves usually means close in voice leading. <bookmark mark='c'/> But not always: the triads that need "
            "the most voice leading, six semitones, are D, F sharp and B flat major, and none of them is the farthest in "
            "moves: that is B flat minor. <bookmark mark='d'/> Which distance the ear uses is exactly the frontier's question."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(dots))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def machines(self):
        items = [
            (r"learned chord embeddings: \ train a model on many chord sequences, \ give every chord a vector", WHITE),
            (r"in several such studies chords a fifth apart, \ and relative major and minor, \ land close together", WHITE),
            (r"the model never saw a Tonnetz: \ any geometry it finds comes from usage", WHITE),
            (r"a test: \ does a learned space agree with PLR distance, \ voice leading, \ or neither?", TUNE),
            (r"Part 62 builds chord recognition; \ this part's numbers are the baseline", GREY_A),
        ]
        rows_scene(self, r"what machines learn", items,
                   "Machines offer a third witness. <bookmark mark='b'/> Train a model on many chord sequences and it gives every "
                   "chord a vector, a point in a learned space. <bookmark mark='c'/> In several such studies, chords a fifth apart, "
                   "and relative major and minor, end up near each other. <bookmark mark='d'/> The model never saw a Tonnetz, so "
                   "whatever geometry it finds comes only from how chords are used. <bookmark mark='e'/> That makes a clean test: "
                   "does the learned space agree with P L R distance, with voice leading, or with neither? <bookmark mark='f'/> "
                   "Part 62 builds chord recognition, and this part's distances are the baseline it can be compared with.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def audit(self):
        items = [
            (r"computed exactly: \ the groups, \ their orders, \ distances, \ cycles, \ the 62 tours", WHITE),
            (r"computed from our own definitions: \ voice leading as the fewest semitones, \ three voices", WHITE),
            (r"taken from the literature: \ Beethoven's chain \ (Cohn), \ film usage \ (Lehman), \ ratings \ (Krumhansl)", WHITE),
            (r"not measured here: \ how any listener hears a move", EAR),
            (r"the moves are a fact about chords; \ their effect is a question about people", GREY_A),
        ]
        rows_scene(self, r"what this part measured, and what it did not", items,
                   "Before the research problem, an audit of this part's claims. <bookmark mark='b'/> Computed exactly: the groups, their orders, the distances, the cycles and the sixty-two tours. <bookmark mark='c'/> Computed from our own definitions: voice leading as the fewest semitones three voices must move. <bookmark mark='d'/> Taken from the literature: Beethoven's chain from Cohn, film usage from Lehman, ratings from Krumhansl. <bookmark mark='e'/> Not measured here at all: how any listener hears a move. <bookmark mark='f'/> The moves are a fact about chords; their effect is a question about people.", marks="cdef")
