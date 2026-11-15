from __future__ import annotations

from videos.music.music63.common import *  # noqa: F403


class Tagging(SoundScene):
    def construct(self):
        chapter(self, 5, r"Tags and embeddings", r"How does a machine describe what music sounds like?")
        self.tags()
        self.embedding()
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
            "Tags are words; machines prefer vectors. <bookmark mark='a'/> An embedding is a short vector per recording, near "
            "for recordings that sound alike. <bookmark mark='b'/> Monochord's is simple: the energy in twenty-four bands and "
            "how it varies, twelve chroma bins and the flux, sixty-two numbers. <bookmark mark='c'/> Learnt embeddings are a "
            "network's last layer, trained on millions of tracks to predict tags or what people play together. "
            "<bookmark mark='d'/> Nearest neighbours in the embedding give more like this. <bookmark mark='e'/> The risk is that "
            "near in the embedding means near in recording conditions, not in music."
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
