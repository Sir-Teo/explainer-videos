from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403


class Gamelan(SoundScene):
    def construct(self):
        chapter(self, 7, r"Slendro and pelog", r"What if every orchestra had its own tuning?")
        self.what()
        self.hear()
        self.patet()
        self.tunein()
        self.nostandard()
        self.embat()
        self.spectra()

    # ------------------------------------------------------------------
    def what(self):
        items = [
            (r"gamelan: \ ensembles of Java and Bali, \ mostly bronze metallophones and gongs, \ with drums, \ voice, \ strings", WHITE),
            (r"two tuning systems: \ \textit{slendro}, \ five near-equal steps; \ \textit{pelog}, \ seven unequal ones", WHITE),
            (r"a full Javanese gamelan has a set of instruments for each, \ side by side", WHITE),
            (r"the instruments are made and tuned together, \ and belong together", TUNE),
            (r"many gamelans have names, \ and some are treated with ceremony", GREY_A),
        ]
        rows_scene(self, r"gamelan", items,
                   "Now south-east to Java and Bali. <bookmark mark='b'/> A gamelan is an ensemble, mostly of bronze "
                   "metallophones and gongs, with drums, voices and strings. <bookmark mark='c'/> It has two tuning systems: "
                   "slendro, with five nearly equal steps to the octave, and pelog, with seven unequal ones. <bookmark mark='d'/> "
                   "A full Javanese gamelan has a set of instruments for each, side by side. <bookmark mark='e'/> The instruments "
                   "of a gamelan are made and tuned together, and belong together. <bookmark mark='f'/> Many gamelans have "
                   "names, and some are treated with ceremony.", marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("scales")
        c = clip("scales.two")
        ruler = cents_ruler([d["slendro"], d["pelog"]], width=10.0, top=1200, labels=[r"slendro", r"pelog"], colors=[TUNE, BLUE], row_gap=1.2).move_to(UP * 0.4)
        steps = VGroup(label(r"steps: \ " + r", \ ".join(str(int(s)) for s in d["slendro_steps"]), font_size=17, color=TUNE).next_to(ruler.rows[0][0], DOWN, buff=0.25),
                       label(r"steps: \ " + r", \ ".join(str(int(s)) for s in d["pelog_steps"]), font_size=17, color=BLUE).next_to(ruler.rows[1][0], DOWN, buff=0.25))
        cap = label(r"illustrative values: \ every gamelan has its own", font_size=21, color=EAR).to_edge(DOWN, buff=0.9)
        head = label(r"slendro and pelog \ (one illustrative tuning of each)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is one illustrative tuning of each, played on a model metallophone. Slendro, with five steps of about two "
            "hundred and forty cents, none of them the piano's: neither a whole tone nor a minor third. Then pelog, seven "
            "steps from about one hundred and fifteen to two hundred and seventy cents, from which a piece usually uses five. "
            "These particular numbers are ours."
        ):
            self.play(FadeIn(head), FadeIn(ruler), FadeIn(steps), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"slendro, \ then pelog", detail=r"Part 9's bar", corner=DL, tag_corner=DR)
            pulse(snd, ruler.rows[0][3], d["starts"]["slendro"], d["starts"]["pelog"] - 0.5, buff=0.06)
            pulse(snd, ruler.rows[1][3], d["starts"]["pelog"], c.duration, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nostandard(self):
        items = [
            (r"there is no standard slendro or pelog: \ each gamelan's tuning is its own", WHITE),
            (r"measured gamelans differ by tens of cents, \ step by step \ (Surjodiningrat and others, \ 1972)", WHITE),
            (r"a gamelan's tuning, \ its \textit{embat}, \ is part of its character, \ like a voice", WHITE),
            (r"octaves are often stretched or compressed slightly, \ on purpose", TUNE),
            (r"a scale defined by a family resemblance, \ not by a number", GREY_A),
        ]
        rows_scene(self, r"no standard", items,
                   "There is no standard. <bookmark mark='b'/> Each gamelan's slendro and pelog are its own, and measurements of "
                   "many gamelans, by Wasisto Surjodiningrat and colleagues in 1972 among others, found them differing by tens "
                   "of cents, step by step. <bookmark mark='c'/> A gamelan's tuning, its embat, is part of its character, like "
                   "a voice. <bookmark mark='d'/> Even the octaves are often slightly stretched or compressed, on purpose. "
                   "<bookmark mark='e'/> The scales are defined by a family resemblance, not by numbers.", marks="bcde")

    # ------------------------------------------------------------------
    def spectra(self):
        d = load("spectra")
        c = clip("spectra.two")
        cs = d["cents"]
        top = max(max(d["harmonic"]), max(d["bar"]))
        ax = Axes(x_range=[0, 1250, 200], y_range=[0, top * 1.05, top / 4], x_length=6.4, y_length=3.2, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": False}).move_to(LEFT * 2.6 + DOWN * 0.3)
        lh = VMobject(color=TUNE, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(cs, d["harmonic"])])
        lb = VMobject(color=BLUE, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(cs, d["bar"])])
        xt = VGroup(*[label(str(v), font_size=14, color=GREY_A).next_to(ax.c2p(v, 0), DOWN, buff=0.12) for v in (0, 400, 800, 1200)])
        side = VGroup(*[label(s, font_size=20, color=c_) for s, c_ in (
            (r"Part 5's model roughness\\interval on x-axis in cents", WHITE),
            (r"harmonic tone (gold):\\dips at just intervals and the octave", TUNE),
            (r"uniform free bar \ (blue): \ dips at " + r", \ ".join(f"{m:.0f}" for m in d["min_bar"]) + r" cents;\\no dip at 1200 cents", BLUE),
            (r"Sethares: some measured gamelan spectra\\have dips near slendro steps\\this ideal uniform bar does not", EAR))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.6)).move_to(RIGHT * 3.6)
        head = label(r"spectrum and scale", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Why such scales? William Sethares, extending Part 5, suggested that a scale suits the spectrum of the instruments "
            "playing it. <bookmark mark='a'/> For a tone with harmonic partials, the dissonance curve dips at the just "
            "intervals and the octave. <bookmark mark='b'/> For a uniform free bar, Part 9's partials of one, two point seven "
            "six and five point four, the dips fall in quite different places, and there is no dip at the octave at all. "
            "<bookmark mark='c'/> Sethares, using the measured spectra of real gamelan instruments, whose bars are shaped, "
            "found dips near slendro's steps; our idealized bar does not show that, which is itself worth knowing. Listen to "
            "the same slendro on both kinds of tone."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), Create(lh), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        with self.listen(c) as snd:
            window(snd, r"harmonic tone, \ then bar", detail=r"additive tone and Part 9's bar", corner=DL, tag_corner=DR)
            pulse(snd, side[1], d["starts"]["harmonic"], d["starts"]["bar"] - 0.5, buff=0.05)
            pulse(snd, side[2], d["starts"]["bar"], c.duration, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def patet(self):
        d = load("patet")
        c = clip("patet.two")
        cells = VGroup(label(r"degrees 1 2 3 5 6", font_size=24, color=TUNE), label(r"degrees 2 3 5 6 7", font_size=24, color=BLUE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"five from seven: \ two pelog subsets", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "A pelog piece usually uses five of the seven notes. Two common choices are degrees one, two, three, five and six, and degrees two, three, five, six and seven. In Javanese practice these belong to different pathet, modes associated with different times of the night and different moods, like Part 34's ragas. Hear both subsets of the same illustrative pelog."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"two subsets", detail=r"Part 9's bar", corner=DL, tag_corner=DR)
            ks = ['A', 'B']
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < len(ks) - 1 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tunein(self):
        d = load("two_scales")
        c = clip("two_scales.two")
        cells = VGroup(label(r"slendro: \ F and E on one key", font_size=24, color=TUNE), label(r"pelog", font_size=24, color=BLUE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"the Tune's first phrase in slendro and pelog", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "What happens to a familiar melody? Here is the Tune's first phrase on a metallophone, first in the illustrative slendro, where with only five notes its F and E must share one key, then in the illustrative pelog. Neither sounds like a piano's Tune: the intervals themselves are different, and so is the melody's character."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"slendro, \ then pelog", detail=r"Part 9's bar", corner=DL, tag_corner=DR)
            ks = ['slendro', 'pelog']
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < len(ks) - 1 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def embat(self):
        items = [
            (r"a smith forges and grinds each bronze key and gong", WHITE),
            (r"thinning the middle of a key lowers it; \ shortening the ends raises it \ (Part 9's bars)", WHITE),
            (r"the tuner works by ear, \ to match the gamelan's own embat, \ not a chart", WHITE),
            (r"bronze drifts slowly over the years, \ and gamelans are retuned", TUNE),
            (r"a new gamelan copying an old one's tuning is a kind of lineage", GREY_A),
        ]
        rows_scene(self, r"how a gamelan is tuned", items,
                   "How is a gamelan tuned? <bookmark mark='b'/> A smith forges each bronze key and gong, then grinds it. <bookmark mark='c'/> Thinning the middle of a key lowers its pitch; shortening its ends raises it, as Part 9's bars showed. <bookmark mark='d'/> The tuner works by ear, to match the gamelan's own embat, not a chart. <bookmark mark='e'/> Bronze drifts slowly over the years, and gamelans are retuned. <bookmark mark='f'/> A new gamelan copying an old one's tuning is a kind of lineage.", marks="cdef")
