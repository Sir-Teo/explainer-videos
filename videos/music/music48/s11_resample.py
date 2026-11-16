from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403


class Resample(SoundScene):
    def construct(self):
        chapter(self, 10, r"Resampling and the high-resolution debate", r"How many samples a second does music need?")
        self.convert()
        self.quiz()
        self.debate()
        self.testing()
        self.verdict()

    # ------------------------------------------------------------------
    def convert(self):
        d = load("rate")
        a, b = d["ratio_441"]
        items = [
            (rf"48,000 to 44,100 is the ratio {a} to {b}: \ every {b} input samples become {a} output samples", WHITE),
            (r"each new sample is read off the band-limited curve of chapter 2, \ at its own instant", WHITE),
            (r"going down, \ the curve must first lose everything above the new Nyquist frequency, \ or it will fold", WHITE),
            (r"dropping samples without that filter is the aliasing of chapter 3, \ done in software", TUNE),
            (r"a good resampler is an exact interpolation filter: \ many taps, \ and a steep, \ clean cutoff", GREY_A),
        ]
        rows_scene(self, r"changing the rate", items,
                   "Music recorded at one rate often has to be delivered at another. <bookmark mark='b'/> Forty-eight thousand to "
                   f"forty-four thousand one hundred is the ratio {a} to {b}: every {b} input samples become {a}. "
                   "<bookmark mark='c'/> Each new sample is read off the band-limited curve of chapter two, at its own instant. "
                   "<bookmark mark='d'/> Going down, the curve must first lose everything above the new Nyquist frequency, or it "
                   "will fold. <bookmark mark='e'/> Dropping samples without that filter is chapter three's aliasing, done in "
                   "software. <bookmark mark='f'/> A good resampler is an accurate interpolation filter: many taps, and a steep, "
                   "clean cutoff.", marks="bcdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("rate")
        c = clip("rate.two")
        card = listen_card(r"A groove, \ twice. \ Once sampled at 16,000 a second, \ once at 48,000. \ Which was 16,000?", width=9.6)
        with self.voiceover("A question. A groove, twice. Once sampled at sixteen thousand a second, once at forty-eight thousand. Which was sixteen thousand?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        f = np.array(d["f"])
        ax = frame_axes(width=9.0, height=2.6, xlo=0, xhi=24000, ylo=-140, yhi=-20, center=DOWN * 0.8)
        lo = curve(f, np.clip(d["low"], -140, -20), ax.to, color=EAR, width=2.5)
        hi = curve(f, np.clip(d["full"], -140, -20), ax.to, color=TUNE, width=2.5)
        ticks = VGroup(*[label(f"{v // 1000} k", font_size=15, color=GREY_A).next_to(ax.to(v, -140), DOWN, buff=0.12) for v in (0, 8000, 16000, 24000)])
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.0, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(ORIGIN)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.6).move_to(UP * 1.5)
        self.play(FadeOut(card), FadeIn(boxes), FadeIn(ax), FadeIn(ticks))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a groove, \ twice", detail=r"Part 40's drums, \ Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        with self.voiceover(
            "The first. At sixteen thousand a second nothing above eight kilohertz survives: the cymbals lose their sizzle and "
            "the piano its edge. <bookmark mark='a'/> The spectra show it: the first stops dead at eight kilohertz; the second "
            "carries on to the top. Sixteen kilohertz supports wideband speech; traditional narrowband telephony commonly uses eight kilohertz sampling. The real question is whether anything is "
            "lost between forty-four thousand one hundred and more."
        ) as vo:
            self.play(Create(lo))
            vo.wait_until("a")
            self.play(Create(hi))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def debate(self):
        items = [
            (r"high-resolution formats: \ 96 or 192 kHz, \ 24 bits: \ is anything audible gained over 44.1 and 16?", WHITE),
            (r"E. Brad Meyer and David Moran \ (2007): \ a 16-bit, \ 44.1 kHz loop inserted into high-resolution playback", WHITE),
            (r"in hundreds of double-blind trials, \ aggregate performance did not reliably exceed chance under those study conditions", WHITE),
            (r"Joshua Reiss \ (2016): \ 18 studies, \ over 12,500 trials: \ a small but significant ability to tell, \ larger with training", TUNE),
            (r"trained listeners were right about 60 per cent of the time, \ where guessing gives 50", GREY_A),
        ]
        rows_scene(self, r"the high-resolution debate", items,
                   "That is the high-resolution debate. <bookmark mark='b'/> Formats at ninety-six or a hundred and ninety-two kilohertz and twenty-four bits are sold as better than forty-four point one and sixteen. Is anything audible gained? <bookmark mark='c'/> In 2007 E. Brad Meyer and David Moran inserted a sixteen-bit, forty-four point one kilohertz loop into high-resolution playback, <bookmark mark='d'/> and in hundreds of double-blind trials aggregate performance did not reliably exceed chance under those study conditions. <bookmark mark='e'/> In 2016 Joshua Reiss pooled eighteen studies and over twelve thousand five hundred trials, and found a small but significant ability to tell, larger with training: <bookmark mark='f'/> trained listeners were right about sixty per cent of the time, where guessing gives fifty.", marks="bcdef")

    # ------------------------------------------------------------------
    def testing(self):
        items = [
            (r"blind: \ the listener must not know which is which; \ the ABX test asks whether X is A or B", WHITE),
            (r"level-matched: \ a difference of a fraction of a decibel is heard as `better', \ not `louder'", WHITE),
            (r"enough trials: \ 12 right out of 16 happens by guessing only 3.8 per cent of the time", WHITE),
            (r"and the same music, \ from the same master, \ through the same chain apart from the one change", TUNE),
            (r"most informal comparisons fail all four", GREY_A),
        ]
        rows_scene(self, r"testing it properly", items,
                   "How should such a claim be tested? <bookmark mark='b'/> Blind: the listener must not know which is which; the "
                   "ABX test plays A, B and an unknown X, and asks whether X is A or B. <bookmark mark='c'/> Level-matched: a "
                   "difference of a fraction of a decibel is heard as better, not as louder. <bookmark mark='d'/> With enough "
                   "trials: twelve right out of sixteen happens by guessing only 3.8 per cent of the time. "
                   "<bookmark mark='e'/> And with the same music, from the same master, through the same chain apart from the one "
                   "change. <bookmark mark='f'/> Most informal comparisons fail all four.", marks="bcdef")

    # ------------------------------------------------------------------
    def verdict(self):
        items = [
            (r"for delivery, \ 44.1 or 48 kHz at 16 bits, \ properly dithered, \ is at or near the limit of what people hear", WHITE),
            (r"where differences are found, \ filters and playback chains, \ not missing samples, \ may be the cause", WHITE),
            (r"for production, \ 24 bits give headroom and 96 kHz gives room for processing that makes high frequencies", WHITE),
            (r"the arguments are about margins, \ not about stair-steps", TUNE),
            (r"how such claims should be tested comes back in Part 67", GREY_A),
        ]
        rows_scene(self, r"what to conclude", items,
                   "What should we conclude? <bookmark mark='b'/> For delivery, forty-four point one or forty-eight kilohertz at "
                   "sixteen bits, properly dithered, is at or near the limit of what people hear. <bookmark mark='c'/> Where "
                   "differences are found, filters and playback chains, rather than missing samples, may be the cause. "
                   "<bookmark mark='d'/> For production, twenty-four bits give headroom, and higher rates give room for processing "
                   "that creates high frequencies. <bookmark mark='e'/> The arguments are about margins, not about stair-steps. "
                   "<bookmark mark='f'/> How such claims should be tested comes back in Part 67.", marks="bcdef")
