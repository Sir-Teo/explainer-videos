from __future__ import annotations

from videos.music.music64.common import *  # noqa: F403


class Mixing(SoundScene):
    def construct(self):
        chapter(self, 1, r"The mixing model", r"What exactly has to be undone?")
        self.model()
        self.cases()
        self.stems()
        self.meet()

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
            (r"a network assumes what its training data showed it: \ one set of learned statistical assumptions", TUNE),
        ]
        rows_scene(self, r"why it needs assumptions", items,
                   "With one channel and two sources there are infinitely many pairs of signals that add up to the same mixture. <bookmark mark='b'/> So every method assumes something about the sources: where they are panned, that they are independent, what they sound like. <bookmark mark='c'/> Assumptions help when they match the actual sources and mixing process. <bookmark mark='d'/> A network assumes what its training data showed it, one set of learned statistical assumptions.", marks="bcd")

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
                   "The test is our own. <bookmark mark='b'/> Part 56's synthetic session, whose every track Monochord generated and mixed. "
                   "<bookmark mark='c'/> Four stems, as the field's benchmark has them: vocals, bass, drums, and everything else. "
                   "<bookmark mark='d'/> The separators learn from the session's later phrases and are tested on its first two. "
                   "<bookmark mark='e'/> The benchmark itself, MUSDB18 from 2017, has a hundred and fifty real songs with their stems. "
                   "<bookmark mark='f'/> We can compute waveform errors against known references; numerical approximations and metric limitations still apply: we own the ingredients of the cake.", marks="bcdef")

    # ------------------------------------------------------------------
    def meet(self):
        d = load("meet")
        c = clip("meet.five")
        sh = d["energy_share"]
        names = [(r"vocals", "vocals", TUNE), (r"bass", "bass", BLUE), (r"drums", "drums", EAR), (r"other: \ piano, \ guitar", "other", GREY_B), (r"the mix", "mix", WHITE)]
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.3, height=1.0, corner_radius=0.12, stroke_color=col),
                                label(t, font_size=17, color=col)).arrange(ORIGIN) for t, _, col in names]).arrange(RIGHT, buff=0.22).move_to(UP * 0.6)
        shares = VGroup(*[label(rf"{100 * sh[k]:.0f}\% of the energy", font_size=14, color=GREY_A).next_to(b, DOWN, buff=0.15) for (_, k, _), b in zip(names[:4], boxes[:4])])
        head = label(r"meet the test set", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Before separating anything, meet the four stems, each alone for four seconds, then mixed. Every separator in "
            "this part will be asked to get from the last box back to the first four."
        ):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        ks = ["vocals", "bass", "drums", "other", "mix"]
        with self.listen(c) as snd:
            window(snd, r"four stems, \ then the mix", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.25 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        with self.voiceover(
            f"The voice carries about a third of the mix's energy, {say(round(100 * sh['vocals']))} per cent; the bass, drums "
            "and the piano and guitar a fifth or a quarter each. Easy to tell apart by ear, and, as we shall see, hard by machine."
        ):
            self.play(FadeIn(shares))
        self.wait(0.4)
        self.clear_scene()
