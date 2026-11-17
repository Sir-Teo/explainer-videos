from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Bci(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.bits()
        self.limits()

    def card(self):
        card = chapter_card(11, r"Reading out", r"What can a brain-computer interface decode?", lit=(), part=PART,
                            scale=("cell", "brain"), marr=("how",))
        with self.voiceover("Chapter eleven. Reading out."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def history(self):
        head = heading(r"From a cursor to sentences")
        rows = rows_of([
            (r"a brain-computer interface is a decoder run live: \ record, \ decode, \ act, \ and let the person see "
             r"the result and adapt", WHITE),
            (r"scalp EEG: \ spellers that flash letters and detect the brain's response to the one attended; \ slow, \ "
             r"but non-invasive", SYMP),
            (r"arrays of electrodes in motor cortex: \ people with paralysis moving cursors and robotic arms by "
             r"intended movement", MODEL),
            (r"recent work decodes attempted speech from the cortex of a person who cannot speak, \ into text, \ with "
             r"a language model's help", PERSON),
            (r"each step is the population vector's idea, \ grown up: \ many noisy channels, \ one intended movement",
             GOOD),
        ], 12.4, 22, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Willett et al.\ (2023)")
        with self.voiceover(
            "Decoding becomes a device when it runs live. <bookmark mark='a'/> A brain-computer interface records, "
            "decodes and acts, and the person sees the result and adapts. <bookmark mark='b'/> With scalp EEG, "
            "spellers flash letters and detect the brain's response to the one being attended: slow, but needing no "
            "surgery. <bookmark mark='c'/> With electrode arrays in motor cortex, people with paralysis have moved "
            "cursors and robotic arms by intending to move. <bookmark mark='d'/> Recent work decodes attempted "
            "speech from the cortex of a person who can no longer speak, into text, with a language model's help. "
            "<bookmark mark='e'/> Each step is the population vector's idea, grown up: many noisy channels, one "
            "intended movement."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def bits(self):
        d = load("itr")
        head = heading(r"Bits per minute")
        eq = MathTex(r"B = \log_2 N + P\log_2 P + (1-P)\log_2\frac{1-P}{N-1}", font_size=32, color=MODEL)
        eq.move_to([0, 2.2, 0])
        A = axes([0.25, 1.0], [0, 40], x_length=5.0, y_length=2.6, xticks=[0.25, 0.5, 0.75, 1.0], yticks=[0, 20, 40],
                 xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.0f}", xlabel=r"accuracy (4 targets, 3 s each)",
                 ylabel=r"bits per minute", center=[-3.5, -0.4, 0], font_size=12)
        acc = np.asarray(d["acc"])
        c = curve(A.ax, acc, d["curve"], PERSON, stroke_width=4)
        rows = rows_of([
            (r"Wolpaw's formula: \ the information in one selection among $N$ targets, \ made correctly with "
             r"probability $P$, \ errors spread evenly", WHITE),
            (rf"{d['labels'][0].replace('%', r'\%')}: \ {d['bits_per_min'][0]:.0f} bits a minute", SYMP),
            (rf"{d['labels'][1].replace('%', r'\%')}: \ {d['bits_per_min'][1]:.0f}", MODEL),
            (rf"{d['labels'][2].replace('%', r'\%')}: \ {d['bits_per_min'][2]:.0f}; \ typing is a few hundred", PERSON),
            (r"accuracy near chance is worth almost nothing: \ the curve is steep at the top", YOU),
        ], 5.8, 18, 0.32).move_to([3.5, -0.5, 0])
        tag = psyche_tag(r"\texttt{neurodata.wolpaw\_itr}")
        with self.voiceover(
            "How good is a decoder? Engineers count bits. <bookmark mark='a'/> Jonathan Wolpaw's formula gives the "
            "information in one selection among N targets, made correctly with probability P. Divide by the time per "
            "selection. <bookmark mark='b'/> Two targets at ninety percent, four seconds each: about eight bits a "
            "minute. <bookmark mark='c'/> Four targets at eighty percent, three seconds each: about nineteen. "
            "<bookmark mark='d'/> Twenty-six letters at ninety-five percent, one and a half seconds each: about a "
            "hundred and sixty-seven. Typing is a few hundred. <bookmark mark='e'/> Accuracy near chance is worth "
            "almost nothing. The curve is steep at the top, so the last few percent matter most."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(c))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def limits(self):
        head = heading(r"What is decoded, \ and what is not")
        left = rows_of([
            (r"decoded", GOOD),
            (r"intended movements, \ including the movements of speech", WHITE),
            (r"what a person attends to, \ among options the system offers", WHITE),
            (r"coarse categories of what is seen or imagined, \ from a model trained on that person, \ with their "
             r"cooperation", WHITE),
        ], 5.8, 21, 0.32).move_to([-3.3, 0.0, 0])
        right = rows_of([
            (r"not decoded", AUTH),
            (r"thoughts at large, \ unbidden, \ from a stranger", WHITE),
            (r"anything from a model trained on someone else, \ without long calibration", WHITE),
            (r"anything a person declines to give: \ a resisting participant defeats the decoders tested so far", WHITE),
        ], 5.8, 21, 0.32).move_to([3.3, 0.0, 0])
        with self.voiceover(
            "So what can be read out? <bookmark mark='a'/> Intended movements, including the movements of speech. "
            "What a person attends to, among options the system offers. And coarse categories of what's seen or "
            "imagined, from a model trained on that person, with their cooperation. <bookmark mark='b'/> Not thoughts "
            "at large, unbidden, from a stranger. Not much from a model trained on someone else, without long "
            "calibration. And not what a person declines to give: so far, a resisting participant defeats the "
            "decoders. Claims beyond that deserve the audit of chapter fourteen."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
        self.wait(1.0)
        self.clear_scene()
