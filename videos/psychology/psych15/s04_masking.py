from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


class Masking(VoiceoverScene):
    def construct(self):
        self.card()
        self.fletcher()
        self.spread()

    def card(self):
        card = chapter_card(3, r"Filters and masking", r"When does one sound hide another?",
                            lit={1940: r"Fletcher"}, part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter three. Filters and masking."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def fletcher(self):
        d = load("masking")
        head = heading(r"Fletcher's band-widening experiment, \ 1940")
        lb = np.log10(d["bw"])
        A = axes([1, np.log10(2000)], [20, 45], x_length=7.0, y_length=4.2, xticks=[1, 2, 3],
                 xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yticks=[20, 25, 30, 35, 40, 45],
                 xlabel=r"width of the noise band (Hz)", ylabel=r"threshold of the tone (dB)", center=[-2.5, -0.3, 0])
        ax = A.ax
        c = curve(ax, lb, d["thr"], SOUND, stroke_width=4)
        knee = DashedLine(ax.c2p(np.log10(d["erb"]), 20), ax.c2p(np.log10(d["erb"]), 45), color=PLACE, stroke_width=2)
        kl = label(rf"one filter: \ {d['erb']:.0f} Hz", font_size=22, color=PLACE).next_to(knee, UP, buff=0.08)
        rows = rows_of([
            (r"a 2 kHz tone in a band of noise centred on it; \ widen the band, \ keep its density fixed", WHITE),
            (r"at first the tone gets harder to hear: \ more noise, \ higher threshold", SOUND),
            (r"then the threshold stops rising: \ noise outside the tone's filter does not mask it", PLACE),
            (r"the knee measures the filter's width: \ the critical band", TIMING),
        ], 4.8, 26, 0.32).move_to([4.4, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the power-spectrum model, \ one ERB-wide filter")
        with self.voiceover(
            "How wide are the ear's filters? Harvey Fletcher, at Bell Labs, found out in 1940 with masking. "
            "<bookmark mark='a'/> Play a two-thousand-hertz tone inside a band of noise centred on it, and widen the "
            "band while keeping the noise equally dense. <bookmark mark='b'/> At first the tone gets harder to hear: "
            "more noise, higher threshold. <bookmark mark='c'/> Then, past a certain width, the threshold stops rising, "
            "however much wider the noise gets. The extra noise falls outside the filter that's listening for the "
            "tone, and the ear ignores it. <bookmark mark='d'/> Where the curve bends measures the width of that "
            "filter. Fletcher called it the critical band. Psyche's version uses the modern estimate, about two "
            "hundred and forty hertz at two thousand hertz, and the data look like this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(knee), FadeIn(kl), FadeIn(rows[3]))
        self.clear_scene()

    def spread(self):
        head = heading(r"What masking is for")
        rows = rows_of([
            (r"masking spreads upward: \ a loud low sound hides quiet high ones more than the reverse", SOUND),
            (r"the filters are lopsided: \ each one's low-frequency side is shallow", PLACE),
            (r"a sound well below threshold, \ or hidden by a louder neighbour, \ need not be sent at all", TIMING),
            (r"that is how an MP3 throws away most of the data: \ chapter fourteen", GREY_A),
        ], 12.6, 29, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "Masking isn't symmetrical. <bookmark mark='a'/> A loud low sound hides quieter high sounds far more than a "
            "loud high sound hides low ones, which is why a bass-heavy band can drown a singer. "
            "<bookmark mark='b'/> The reason is in the filters: each is lopsided, with a shallow skirt on its "
            "low-frequency side, so a low sound spills into the filters above it. <bookmark mark='c'/> Engineers turned "
            "this into money. A sound below the threshold of hearing, or hidden under a louder neighbour, needn't be "
            "stored or sent at all. <bookmark mark='d'/> That's the principle of the MP3 and every codec since, and "
            "it's in chapter fourteen."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
