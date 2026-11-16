from __future__ import annotations

from videos.music.music66.common import *  # noqa: F403
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.ledger()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune66")
        c = clip("tune.variation66")
        st = d["starts"]
        keys = d["names"]
        names = {"sung": r"sung \ (Part 8's alto)", "string": r"re-rendered: \ DDSP string", "continued": r"piano, \ then the token model"}
        head = VGroup(label(r"Variation 66", font_size=48, color=TUNE), label(r"generated", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(RoundedRectangle(width=3.6, height=1.2, corner_radius=0.12, stroke_color=TUNE),
                                label(names[k], font_size=17, color=TUNE)).arrange(ORIGIN) for k in keys]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)
        note = label(r"the Tune sung; \ the same pitch and loudness driving the DDSP string; \ the Tune's first phrase on the piano, \ continued by the token model", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here the Tune is sung, then "
            "the singer's pitch and loudness drive the DDSP string, an octave up, and last the Tune's first phrase on the piano "
            "is continued by the token model, uncurated."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"Variation 66", kind="synthesized", detail=r"Part 8's voice; \ DDSP; \ the token model", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        d = load("ddsp")
        with self.voiceover(
            f"Row sixty-six of the ledger: the DDSP string {say(d['dist'], 1)} decibels by spectrum from the string it learnt, "
            "and a few seconds of piano continued by a model trained on the synthetic piano corpus described earlier."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"raw audio is long: \ sixteen thousand decisions a second; \ mu-law makes each one a choice of 256",
            r"sample-by-sample networks capture detail, \ not structure",
            r"spectrograms and vocoders; \ codec tokens, \ stage on stage",
            r"a language model over tokens learns texture before structure",
            r"diffusion draws by removing noise; \ DDSP learns a synthesizer's controls",
            r"judge with distances, \ listeners and copying; \ marks label, \ but only what their makers mark",
        ], title=r"What we found", font_size=19).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Raw audio is long: sixteen thousand decisions a second, each, with mu-law, a choice among two hundred and fifty-six. <bookmark mark='a'/> A network that writes sample by sample can capture local detail while struggling with long-range structure in this small experiment. <bookmark mark='b'/> Spectrograms with vocoders, and codec tokens stage on stage, give compact representations. <bookmark mark='c'/> A language model over tokens learns texture before structure. <bookmark mark='d'/> Diffusion draws by removing noise, and DDSP learns the controls of a synthesizer. <bookmark mark='e'/> And generated sound is judged by distances, listeners and copying together, and marks label only what their makers chose to mark."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A codec has 8 codebooks of 1,024 entries at 75 frames a second. \ What is its bit rate, \ and how many tokens is a three-minute song?",
            r"Show that if $x_t = \sqrt{\bar\alpha_t}x_0 + \sqrt{1 - \bar\alpha_t}\varepsilon$, \ predicting $\varepsilon$ and predicting $x_0$ are equivalent.",
            r"\textbf{Ear.} \ The lab plays a codec at 1 to 4 stages and marked and unmarked phrases; \ order and spot them, \ then check.",
            r"\textbf{Build.} \ Give the DDSP synthesizer a learnt reverb \ (Part 49) \ and train it on the string in a room.",
            r"$\bigstar$ \ Can training-data attribution for generated audio be made accurate enough to pay on?",
        ], font_size=21)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, marked "
            "with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"research: \ evaluation, \ listening tests and data, \ examined", [67]),
            (r"the concert: \ the Variations, \ the generated ones labelled", [68]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In research, where evaluation, listening tests and data are examined in turn, and in "
            "the concert at the end, where the generated Variations are labelled as such."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"know the data", r"whose music trained it, \ licensed or not"),
            (r"consent for voices", r"no one's voice without them"),
            (r"label the output", r"mark it, \ and say so"),
            (r"judge three ways", r"distance, \ listeners, \ copying"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Know the data a generator learnt from, and whether it was licensed. No one's voice without their "
            "consent. Label the output: mark it, and say so. And judge it three ways: by distance, by listeners, and by how "
            "much it copies."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"A. van den Oord et al., \ `WaveNet: \ a generative model for raw audio' \ (2016)",
             r"J. Engel et al., \ `DDSP: \ differentiable digital signal processing' \ (ICLR, \ 2020)",
             r"N. Zeghidour et al., \ `SoundStream' \ (2021); \ A. Défossez et al., \ `EnCodec' \ (2022)",
             r"Z. Borsos et al., \ `AudioLM' \ (2022)"],
            [r"A. Agostinelli et al., \ `MusicLM' \ (2023); \ J. Copet et al., \ `MusicGen' \ (2023)",
             r"J. Ho, \ A. Jain and P. Abbeel, \ `Denoising diffusion probabilistic models' \ (2020)",
             r"K. Kilgour et al., \ `Fréchet Audio Distance' \ (Interspeech, \ 2019)",
             r"R. San Roman et al., \ `Proactive detection of voice cloning with localized watermarking' \ (2024)"],
            font_size=18)
        with self.voiceover("The papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        top = label(r"Act XII: \ coda", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"1993: \ thirty-six students, \ ten minutes of Mozart, \ a higher spatial score; \ soon, \ CDs for every newborn in a state.", font_size=21, color=WHITE).move_to(UP * 1.7)
        q = label(r"the effect did not replicate. \ \ How does a field know what it knows?", font_size=27, color=EAR).move_to(UP * 0.4)
        nxt = VGroup(label(r"Part 67", font_size=32, color=GREY_B), label(r"Doing Research in Music", font_size=46, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "1993: a study of thirty-six students reports that ten minutes of Mozart raised a spatial score, and within a few years a governor is sending classical CDs to every newborn in his state. <bookmark mark='a'/> Later research did not support a general intelligence benefit, and found that arousal and mood can explain short-lived task effects. How does a field know what it knows? <bookmark mark='b'/> Next time, the first part of the coda. Part 67: Doing Research in Music."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
