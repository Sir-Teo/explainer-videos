from __future__ import annotations

from videos.music.music64.common import *  # noqa: F403


class Mixing(SoundScene):
    def construct(self):
        chapter(self, 1, r"The mixing model", r"What exactly has to be undone?")
        self.model()
        self.cases()
        self.stems()

    # ------------------------------------------------------------------
    def model(self):
        lines = VGroup(
            MathTex(r"x(t) = \sum_{j} s_j(t)", font_size=40, color=TUNE),
            label(r"the simplest: \ sources added, \ one channel", font_size=19, color=GREY_A),
            MathTex(r"x_c(t) = \sum_j a_{cj}\, s_j(t)", font_size=36, color=WHITE),
            label(r"several channels, \ each source panned: \ instantaneous mixing", font_size=19, color=GREY_A),
            MathTex(r"x_c(t) = \sum_j (h_{cj} * s_j)(t)", font_size=36, color=WHITE),
            label(r"each source through a room and a microphone: \ convolutive mixing, \ the real case", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.3)
        head = label(r"three mixing models", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "What has to be undone? <bookmark mark='a'/> In the simplest model, the sources are added on one channel: one "
            "equation, several unknowns. <bookmark mark='b'/> With several channels, each source can be panned: each channel "
            "is a different weighted sum, instantaneous mixing. <bookmark mark='c'/> And in a real recording each source "
            "reaches each microphone through a room, so it arrives smeared in time: convolutive mixing. Part 56 built all three "
            "kinds of mix; now we run them backwards."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]), FadeIn(lines[3]))
            vo.wait_until("c")
            self.play(FadeIn(lines[4]), FadeIn(lines[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cases(self):
        items = [
            (r"one channel, \ two sources: \ infinitely many answers add up to the same mixture", WHITE),
            (r"so every method assumes something about the sources: \ where they are panned, \ that they are independent, \ what they sound like", WHITE),
            (r"the stronger and truer the assumption, \ the better the separation", WHITE),
            (r"a network assumes what its training data showed it: \ the most specific assumption of all", TUNE),
        ]
        rows_scene(self, r"why it needs assumptions", items,
                   "With one channel and two sources there are infinitely many pairs of signals that add up to the same mixture. "
                   "<bookmark mark='b'/> So every method assumes something about the sources: where they are panned, that they are "
                   "independent, what they sound like. <bookmark mark='c'/> The stronger and truer the assumption, the better the "
                   "separation. <bookmark mark='d'/> A network assumes what its training data showed it, the most specific "
                   "assumption of all.", marks="bcd")

    # ------------------------------------------------------------------
    def stems(self):
        items = [
            (r"the test: \ Part 56's session, \ whose every track Monochord recorded and mixed", WHITE),
            (r"four stems, \ as the field's benchmark has them: \ vocals, \ bass, \ drums, \ and everything else", WHITE),
            (r"the separators learn from the session's later phrases, \ and are tested on its first two", WHITE),
            (r"MUSDB18 \ (2017): \ 150 real songs with their stems, \ the benchmark most results are reported on", WHITE),
            (r"every number in this part is exact: \ we own the ingredients of the cake", TUNE),
        ]
        rows_scene(self, r"the test set", items,
                   "The test is our own. <bookmark mark='b'/> Part 56's session, whose every track Monochord recorded and mixed. "
                   "<bookmark mark='c'/> Four stems, as the field's benchmark has them: vocals, bass, drums, and everything else. "
                   "<bookmark mark='d'/> The separators learn from the session's later phrases and are tested on its first two. "
                   "<bookmark mark='e'/> The benchmark itself, MUSDB18 from 2017, has a hundred and fifty real songs with their stems. "
                   "<bookmark mark='f'/> Every number in this part is exact: we own the ingredients of the cake.", marks="bcdef")
