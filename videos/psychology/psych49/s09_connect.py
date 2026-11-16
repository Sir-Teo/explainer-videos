from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Connect(VoiceoverScene):
    def construct(self):
        self.card()
        self.rest()
        self.gsr()
        self.meaning()

    def card(self):
        card = chapter_card(8, r"Connectivity", r"What does it mean for two regions to be connected?", lit=(),
                            part=PART, scale=("brain",), marr=("how",))
        with self.voiceover("Chapter eight. Connectivity."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rest(self):
        head = heading(r"The brain at rest")
        rows = rows_of([
            (r"2001: \ Marcus Raichle and colleagues noticed regions whose activity fell during almost any "
             r"goal-directed task: \ medial prefrontal and posterior cingulate cortex among them", WHITE),
            (r"they called it a default mode of brain function", MODEL),
            (r"2003: \ Michael Greicius and colleagues found the same regions' slow fluctuations correlated at rest, "
             r"\ with no task at all", PERSON),
            (r"thousands of resting scans later, \ cortex divides into a handful of large networks, \ reproducibly; \ "
             r"the default network is one", GOOD),
            (r"what it does (memory, \ imagining, \ thinking about oneself and others) is still argued", YOU),
        ], 12.4, 22, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Raichle et al.\ (2001); \ Greicius et al.\ (2003)")
        with self.voiceover(
            "Some of the most reproducible findings come from people doing nothing. <bookmark mark='a'/> In 2001 "
            "Marcus Raichle and colleagues noticed regions whose activity fell during almost any goal-directed task, "
            "medial prefrontal and posterior cingulate cortex among them. <bookmark mark='b'/> They called it a "
            "default mode of brain function. <bookmark mark='c'/> In 2003 Michael Greicius and colleagues found that "
            "the same regions' slow fluctuations were correlated at rest, with no task at all. <bookmark mark='d'/> "
            "Thousands of resting scans later, cortex divides into a handful of large networks, reproducibly, and the "
            "default network is one of them. <bookmark mark='e'/> What it does, memory, imagining, or thinking about "
            "oneself and others, is still argued."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def gsr(self):
        d = load("gsr")
        head = heading(r"Anticorrelations made to order")
        R0, R1 = np.asarray(d["R_raw"]), np.asarray(d["R_gsr"])
        n = len(R0)

        def mat(R, center):
            img = np.where(R >= 0, R, 0)
            neg = np.where(R < 0, -R, 0)
            rgb = np.stack([0.06 + 0.9 * img + 0.9 * neg, 0.07 + 0.75 * img, 0.10 + 0.25 * img], -1)
            rgb = np.clip(rgb, 0, 1)
            im = ImageMobject((rgb * 255).astype(np.uint8))
            im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            im.scale_to_fit_height(3.0).move_to(center)
            return im

        m0 = mat(R0, [-4.6, 0.7, 0])
        m1 = mat(R1, [-0.9, 0.7, 0])
        caps = VGroup(label(r"raw", font_size=17, color=WHITE).next_to(m0, DOWN, buff=0.12),
                      label(r"global signal removed", font_size=17, color=AUTH).next_to(m1, DOWN, buff=0.12))
        rows = rows_of([
            (rf"two networks of {n // 2} regions, \ each with its own signal, \ plus a global signal shared by all; \ "
             r"no region is anticorrelated with any other", WHITE),
            (rf"raw: \ within networks {d['within_raw']:.2f}, \ between them {d['between_raw']:.2f} (gold: \ positive)",
             GOOD),
            (rf"regress out the brain's mean: \ between the networks {d['between_gsr']:.2f} (red: \ negative)", AUTH),
            (r"removing the mean forces correlations to average about zero, \ so some must turn negative; \ Murphy and "
             r"colleagues showed this in 2009, \ and the default network's anticorrelations became a fork", YOU),
        ], 5.4, 18, 0.32).move_to([4.0, -0.2, 0])
        tag = psyche_tag(r"\texttt{neurodata.global\_signal}")
        tag2 = published_tag(r"Murphy et al.\ (2009)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Connectivity has its own forks. <bookmark mark='a'/> Psyche makes two networks, each with its own "
            "signal, plus a global signal shared by every region. Nothing is anticorrelated with anything. "
            "<bookmark mark='b'/> Raw, regions within a network correlate about zero point four seven, and between "
            "networks about zero point one four. <bookmark mark='c'/> Now regress out the brain's mean signal, a "
            "common cleaning step. Between the networks, the correlation becomes about minus zero point two seven. "
            "<bookmark mark='d'/> Removing the mean forces the correlations to average about zero, so some must turn "
            "negative. Kevin Murphy and colleagues showed this in 2009, and whether the default network is "
            "anticorrelated with attention networks became a matter of this one choice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(m0), FadeIn(caps[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(m1), FadeIn(caps[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def meaning(self):
        head = heading(r"What a correlation between regions can mean")
        items = [
            (r"a direct anatomical connection", r"possible, \ but correlation does not require one", GOOD),
            (r"a common input", r"both regions driven by a third, \ or by the task, \ or by breathing and heartbeat",
             PERSON),
            (r"shared artefact", r"motion, \ the global signal, \ or the scanner", AUTH),
            (r"direction", r"correlation has none; \ lagged methods on slow fMRI signals are unreliable for it", MODEL),
        ]
        rows = VGroup()
        for name, what, col in items:
            rows.add(VGroup(word_chip(name, col, 21, width=4.6), wrapped_label(what, 7.4, 21, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.1, 0])
        foot = wrapped_label(r"a connectivity map is a map of shared fluctuation; \ causal claims need the "
                             r"interventions of Part 8", 12.0, 21, YOU).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "So what can a correlation between two regions mean? <bookmark mark='a'/> A direct connection: possible, "
            "but not required. <bookmark mark='b'/> A common input: both regions driven by a third, by the task, or by "
            "breathing and heartbeat. <bookmark mark='c'/> A shared artefact: motion, the global signal, or the "
            "scanner. <bookmark mark='d'/> And direction: correlation has none, and lagged methods on slow fMRI "
            "signals are unreliable for it. A connectivity map is a map of shared fluctuation. Causal claims need the "
            "interventions of Part 8."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(foot))
        self.clear_scene()
