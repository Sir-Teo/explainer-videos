from __future__ import annotations

import numpy as np

from videos.music.music63.common import *  # noqa: F403


class Tagging(SoundScene):
    def construct(self):
        chapter(self, 5, r"Tags and embeddings", r"How does a machine describe what music sounds like?")
        self.tags()
        self.embedding()
        self.map()
        self.neighbours()
        self.gtzan()

    # ------------------------------------------------------------------
    def tags(self):
        items = [
            (r"tags: \ genre, \ mood, \ instruments, \ tempo, \ `good for running'", WHITE),
            (r"from people: \ Pandora's Music Genome Project \ (2000): \ analysts scoring each song on hundreds of attributes", WHITE),
            (r"from crowds: \ listeners' free tags, \ plentiful and noisy", WHITE),
            (r"from machines: \ a classifier trained on tagged audio predicts tags for everything else", WHITE),
            (r"tags make music searchable by description, \ and recommendable before anyone has played it", TUNE),
        ]
        rows_scene(self, r"describing music", items,
                   "To find music by what it sounds like, it must be described. <bookmark mark='b'/> With tags: genre, mood, "
                   "instruments, tempo, good for running. <bookmark mark='c'/> From people: Pandora's Music Genome Project, begun in "
                   "2000, had analysts score each song on hundreds of attributes. <bookmark mark='d'/> From crowds: listeners' free "
                   "tags, plentiful and noisy. <bookmark mark='e'/> And from machines: a classifier trained on tagged audio predicts "
                   "tags for everything else. <bookmark mark='f'/> Tags make music searchable by description, and recommendable "
                   "before anyone has played it.", marks="bcdef")

    # ------------------------------------------------------------------
    def embedding(self):
        lines = VGroup(
            label(r"an embedding: \ a short vector per recording, \ near for recordings that sound alike", font_size=21, color=WHITE),
            label(r"Monochord's: \ 24 log-band energies, \ their spread over time, \ 12 chroma bins, \ flux: \ 62 numbers", font_size=19, color=TUNE),
            label(r"learnt ones: \ a network's last layer, \ trained on millions of tracks to predict tags or co-listening", font_size=19, color=WHITE),
            label(r"nearest neighbours in the embedding: \ `more like this'", font_size=19, color=WHITE),
            label(r"the risk: \ near in the embedding may mean near in recording conditions, \ not in music \ (next chapter)", font_size=18, color=EAR),
        ).arrange(DOWN, buff=0.4)
        head = label(r"embeddings", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Tags are words; machines prefer vectors. <bookmark mark='a'/> An audio embedding is a vector representation whose distances reflect its chosen features or training objective. <bookmark mark='b'/> Monochord's is simple: the energy in twenty-four bands and how it varies, twelve chroma bins and the flux, sixty-two numbers. <bookmark mark='c'/> Learnt embeddings are often taken from an intermediate or output layer, trained on millions of tracks to predict tags or what people play together. <bookmark mark='d'/> Nearest neighbours in the embedding give more like this. <bookmark mark='e'/> The risk is that near in the embedding means near in recording conditions, not in music."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gtzan(self):
        items = [
            (r"2002: \ Tzanetakis and Cook's genre dataset: \ 1,000 thirty-second excerpts, \ ten genres", WHITE),
            (r"for a decade it was the benchmark: \ hundreds of papers reported accuracies on it", WHITE),
            (r"2013: \ Bob Sturm inspects it: \ repeated excerpts, \ mislabelled ones, \ distorted ones, \ many by the same few artists", WHITE),
            (r"with the same artist in training and testing, \ a system can learn the artist, \ or the recording, \ and look like it learnt the genre", WHITE),
            (r"benchmarks are data too: \ look at them", TUNE),
        ]
        rows_scene(self, r"the benchmark that was flawed", items,
                   "Which brings a cautionary tale. <bookmark mark='b'/> In 2002 George Tzanetakis and Perry Cook published a genre "
                   "dataset: a thousand thirty-second excerpts in ten genres. <bookmark mark='c'/> For a decade it was the field's "
                   "benchmark, with hundreds of papers reporting accuracies on it. <bookmark mark='d'/> In 2013 Bob Sturm looked "
                   "inside: repeated excerpts, mislabelled ones, distorted ones, and many from the same few artists. "
                   "<bookmark mark='e'/> With an artist in both training and test sets, a system can learn the artist, or the "
                   "recording, and seem to have learnt the genre. <bookmark mark='f'/> Benchmarks are data too: look at them.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def map(self):
        d = load("map")
        xy = np.array(d["xy"])
        part = np.array(d["part"])
        groups = ((1, 15, r"Acts I and II: \ sound and notes", TUNE), (16, 27, r"Acts III and IV: \ voices and history", BLUE),
                  (28, 40, r"Acts V and VI: \ after tonality, \ many musics", EAR), (41, 60, r"Acts VII to X: \ craft to the stage", GREY_B))
        cx, cy, sx, sy = -1.4, -0.4, 3.6, 2.6
        layers = VGroup()
        for lo, hi, _, col in groups:
            m = (part >= lo) & (part <= hi)
            layers.add(VGroup(*[Dot([cx + sx * p[0], cy + sy * p[1], 0], radius=0.03, color=col, fill_opacity=0.75) for p in xy[m]]))
        key = VGroup(*[label(t, font_size=15, color=col) for _, _, t, col in groups]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.4)
        ex = d["explained"]
        note = label(rf"the 62-number embedding of every clip, \ flattened onto its two main directions \ ({100 * (ex[0] + ex[1]):.0f}\% of its variance)", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.3)
        head = label(rf"{len(xy)} clips of this series, \ by sound alone", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            f"Here are all {say(len(xy))} sounds of this series so far, each placed by its embedding alone, flattened onto the two directions along which the embeddings vary most. <bookmark mark='a'/> Colour them by act. <bookmark mark='b'/> The acts overlap almost completely. The first two lean a little toward the top, with their pure tones and single strings, but every act has its plain tones and its full textures, and they land wherever they sound like they belong. The map knows sound, not subject: these features emphasize some similarities and miss others. A two-dimensional PCA projection also discards variation, so this picture is not a validated map of perceived similarity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note), FadeIn(VGroup(*layers).set_color(GREY_D)))
            vo.wait_until("a")
            for (lo, hi, _, col), lay, k in zip(groups, layers, key):
                self.play(lay.animate.set_color(col), FadeIn(k), run_time=0.6)
            vo.wait_until("b")
        self.wait(0.8)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neighbours(self):
        d = load("neighbours")
        c = clip("neighbours.four")
        card = listen_card(r"A Variation, \ then three other clips. \ Two are its nearest neighbours by the embedding; \ one is the farthest clip in the series. \ Which?", width=9.4)
        with self.voiceover("Your turn. A Variation, then three other clips. Two are its nearest neighbours by the embedding, from other parts; one is the farthest clip in the whole series. Which is the odd one out?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"the Variation", r"first", r"second", r"third"], width=2.6, height=0.9, buff=0.35, size=18).move_to(UP * 0.8)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        ks = ["start", "a", "b", "c"]
        with self.listen(c) as snd:
            window(snd, r"near, \ far, \ near", kind="physical model", detail=r"clips of Parts 13, \ 21, \ 22 and 48", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        dist = d["dist"]
        res = label(rf"the second: \ Part 48's test tones, \ distance {dist[2]:.0f}; \ the neighbours: \ Part 21's harmony \ ({dist[1]:.1f}) \ and Variation 13 \ ({dist[3]:.1f}); \ a typical clip: \ {d['median_dist']:.1f}",
                    font_size=17, color=TUNE).move_to(DOWN * 1.3)
        with self.voiceover(
            "The second: Part 48's test tones, the farthest clip in the series from this Variation. The neighbours were Part "
            "21's harmonized Tune and Variation 13: the same melody, similar instruments, found by sixty-two numbers that know "
            "nothing of melody. Near and far, here, agree with the ear."
        ):
            self.play(boxes[2][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()
