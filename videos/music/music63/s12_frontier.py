from __future__ import annotations

from videos.music.music63.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ foundation models and creators", r"What changes when one model listens to everything?")
        self.models()
        self.creators()
        self.evidence()
        self.problem()

    # ------------------------------------------------------------------
    def models(self):
        items = [
            (r"music foundation models: \ networks trained on huge unlabelled collections, \ then adapted to many tasks \ (verify the latest)", WHITE),
            (r"audio and text in one space: \ search by a sentence, \ `a sad waltz on an out-of-tune piano'", WHITE),
            (r"one embedding for tagging, \ similarity, \ recommendation and generation", WHITE),
            (r"what they learn from is whatever was collected: \ Chapter 6's lesson, \ at a scale nobody can inspect by hand", TUNE),
        ]
        rows_scene(self, r"foundation models", items,
                   "Two frontiers. The first is scale. <bookmark mark='b'/> Music foundation models are networks trained on huge "
                   "unlabelled collections and then adapted to many tasks; check the latest, which change every year. "
                   "<bookmark mark='c'/> Some put audio and text in one space, so music can be searched by a sentence: a sad waltz "
                   "on an out-of-tune piano. <bookmark mark='d'/> One embedding then serves tagging, similarity, recommendation and "
                   "generation. <bookmark mark='e'/> And what they learn from is whatever was collected: Chapter 6's lesson, at a "
                   "scale nobody can inspect by hand.", marks="bcde")

    # ------------------------------------------------------------------
    def creators(self):
        items = [
            (r"recommendation shapes what is made: \ musicians tune songs to the first seconds, \ to playlists, \ to short videos", WHITE),
            (r"measuring that effect needs data across years of releases and plays, \ which services rarely share", WHITE),
            (r"regulators now ask: \ the EU's Digital Services Act \ (2022) \ requires large platforms to explain their recommenders", WHITE),
            (r"the effect of a recommender is a causal question: \ what would have been made and heard without it?", TUNE),
        ]
        rows_scene(self, r"effects on creators", items,
                   "The second is the effect on the people who make the music. <bookmark mark='b'/> Recommendation shapes what is "
                   "made: musicians tune songs to the first seconds, to playlists, to short videos. <bookmark mark='c'/> Measuring "
                   "that needs data across years of releases and plays, which services rarely share. <bookmark mark='d'/> Regulators "
                   "now ask: the European Union's Digital Services Act of 2022 requires large platforms to explain their "
                   "recommenders. <bookmark mark='e'/> And the effect of a recommender is a causal question: what would have been "
                   "made, and heard, without it?", marks="bcde")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"simulate a market: \ listeners with tastes, \ artists who adapt to what is rewarded, \ a recommender in the middle", WHITE),
            (r"fit its parameters to what is observable: \ release patterns, \ song lengths, \ play concentration over time", WHITE),
            (r"compare worlds: \ popularity ranking, \ personal ranking, \ exploration, \ no recommender", WHITE),
            (r"$\bigstar$ \ research problem: \ how much of the change in music over the streaming era did recommenders cause?", EAR),
            (r"an answer would inform both platform design and the regulation now being written", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Simulate a market of listeners with tastes, artists who adapt "
            "to what is rewarded, and a recommender in the middle. <bookmark mark='b'/> Fit it to what can be observed: release "
            "patterns, song lengths, the concentration of plays over time. <bookmark mark='c'/> Then compare worlds: ranking by "
            "popularity, by personal taste, with exploration, and with no recommender at all. <bookmark mark='d'/> The question: "
            "how much of the change in music over the streaming era did recommenders cause? <bookmark mark='e'/> An answer would "
            "inform both how platforms are built and the regulation now being written."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def evidence(self):
        items = [
            (r"a stream is paid once it passes thirty seconds \ (Part 60): \ the first seconds carry the money", WHITE),
            (r"Léveillé Gauvin \ (2018): \ in US top-ten hits, \ instrumental introductions shrank from about twenty seconds in the mid-1980s to about five by the mid-2010s", WHITE),
            (r"the voice and the title arrive sooner; \ songs also grew shorter in the streaming years", WHITE),
            (r"but radio, \ video, \ changing taste and attention all overlap those years: \ a trend is not a cause", WHITE),
            (r"what a system rewards, \ people make more of: \ Chapter 9's loop, \ with musicians inside it", TUNE),
        ]
        rows_scene(self, r"the evidence so far", items,
                   "What evidence is there? <bookmark mark='b'/> Some services count eligible streams after about thirty seconds, subject to platform rules and agreements; that does not guarantee a fixed payment. <bookmark mark='c'/> Hubert Léveillé Gauvin measured the top-ten hits in the United States: their instrumental introductions shrank from about twenty seconds in the mid-1980s to about five by the mid-2010s. <bookmark mark='d'/> The voice and the title arrive sooner, and songs grew shorter in the streaming years. <bookmark mark='e'/> But radio, music video, changing taste and attention all overlap those years; a trend is not a cause. <bookmark mark='f'/> The principle is older than streaming: what a system rewards, people make more of. Chapter 9's loop, with musicians inside it.", marks="bcdef")
