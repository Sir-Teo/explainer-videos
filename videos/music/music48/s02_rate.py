from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403


class Rate(SoundScene):
    def construct(self):
        chapter(self, 1, r"Why 44,100?", r"Where did the CD's sample rate come from?")
        self.video()
        self.arithmetic()
        self.cd()
        self.why_that_high()

    # ------------------------------------------------------------------
    def video(self):
        items = [
            (r"in the 1970s, \ nothing cheap could store a million numbers a second, \ except a video recorder", WHITE),
            (r"a PCM adaptor turned audio samples into a black-and-white TV picture: \ white dots for ones, \ black for zeros", WHITE),
            (r"Sony's PCM-1600 \ (1978) \ recorded on U-matic video cassettes; \ CDs were mastered from such tapes for years", WHITE),
            (r"the sample rate had to fit the picture: \ a whole number of samples on each line, \ the same every field", TUNE),
            (r"so the CD's rate is an accident of television", GREY_A),
        ]
        rows_scene(self, r"audio on videotape", items,
                   "In the 1970s, nothing affordable could store a million numbers a second, except a video recorder. "
                   "<bookmark mark='b'/> A PCM adaptor turned audio samples into a black-and-white television picture: white "
                   "dots for ones, black for zeros. <bookmark mark='c'/> Sony's PCM-1600, from 1978, recorded on U-matic video "
                   "cassettes, and compact discs were mastered from such tapes for years. <bookmark mark='d'/> The sample rate "
                   "had to fit the picture: a whole number of samples on each line, the same in every field. "
                   "<bookmark mark='e'/> So the compact disc's sample rate is an accident of television.", marks="bcde")

    # ------------------------------------------------------------------
    def arithmetic(self):
        d = load("rate44")
        n, p = d["ntsc"], d["pal"]
        e1 = MathTex(r"3 \times 245 \times 60 = 44{,}100", font_size=48, color=TUNE)
        e2 = MathTex(r"3 \times 294 \times 50 = 44{,}100", font_size=48, color=BLUE)
        l1 = label(r"NTSC \ (America, \ Japan): \ 3 samples a line, \ 245 usable lines a field, \ 60 fields a second", font_size=19, color=GREY_A)
        l2 = label(r"PAL \ (Europe): \ 3 samples a line, \ 294 usable lines a field, \ 50 fields a second", font_size=19, color=GREY_A)
        g = VGroup(VGroup(e1, l1).arrange(DOWN, buff=0.2), VGroup(e2, l2).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.8).move_to(UP * 0.1)
        lines = VGroup(*[Line(LEFT * 1.2, RIGHT * 1.2, color=GREY_B, stroke_width=1).shift(DOWN * 0.08 * i) for i in range(10)])
        dots = VGroup(*[Dot(radius=0.035, color=WHITE).move_to([-0.9 + 0.9 * k, -0.08 * i, 0]) for i in range(10) for k in range(3)])
        screen = VGroup(RoundedRectangle(width=3.0, height=1.3, corner_radius=0.1, stroke_color=GREY_B), lines.move_to(ORIGIN), dots.move_to(ORIGIN)).to_corner(DR, buff=0.4)
        cap = label(r"three samples on every line", font_size=15, color=GREY_A).next_to(screen, UP, buff=0.1)
        head = label(r"the arithmetic", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the arithmetic. <bookmark mark='a'/> American and Japanese television, NTSC in black and white: sixty "
            "fields a second, two hundred and forty-five usable lines in each, three samples on every line: forty-four "
            "thousand one hundred samples a second. <bookmark mark='b'/> European television, PAL: fifty fields, two hundred and "
            "ninety-four lines, three samples: forty-four thousand one hundred again. One rate worked on both systems, and "
            "the compact disc kept it. Colour NTSC runs a thousandth slower, which is why some early recordings ran at "
            f"{say(d['ntsc_colour'])} instead."
        ) as vo:
            self.play(FadeIn(head), FadeIn(screen), FadeIn(cap), FadeIn(ghost(g, 0.15)))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cd(self):
        d = load("rate44")
        items = [
            (r"the compact disc \ (Sony and Philips, \ 1982): \ 44,100 samples a second, \ 16 bits each, \ two channels", WHITE),
            (rf"that is {d['cd_rate'] * 16 * 2:,} bits a second, \ about {d['cd_bytes_per_hour'] / 1e6:.0f} million bytes an hour", WHITE),
            (r"video and studios settled on 48,000: \ easier to relate to film and video frame rates", WHITE),
            (r"this series works at 48,000 throughout", TUNE),
            (r"but why should forty-odd thousand be enough?", GREY_A),
        ]
        rows_scene(self, r"the compact disc", items,
                   "In 1982 Sony and Philips launched the compact disc: forty-four thousand one hundred samples a second, "
                   "sixteen bits each, two channels. <bookmark mark='b'/> That is 1,411,200 bits every second, about six hundred "
                   "million bytes an hour. <bookmark mark='c'/> Video and studios settled on forty-eight thousand, which fits "
                   "film and video frame rates more easily. <bookmark mark='d'/> This series works at forty-eight thousand "
                   "throughout. <bookmark mark='e'/> But why should forty-odd thousand numbers a second be enough?", marks="bcde")

    # ------------------------------------------------------------------
    def why_that_high(self):
        items = [
            (r"young ears hear up to about 20,000 Hz \ (Part 4); \ the sampling theorem needs a rate above twice that", WHITE),
            (r"40,000 would be the bare minimum, \ with a perfect filter that cannot be built", WHITE),
            (r"the extra 4,100 leave room for a real filter to roll off between 20,000 and 22,050", WHITE),
            (r"a lower rate would have made the filter impossible; \ a higher one would not fit on the tape", TUNE),
            (r"chapter 2: \ why twice is enough", GREY_A),
        ]
        rows_scene(self, r"why that high, \ and no higher", items,
                   "Why that number, and not much less? <bookmark mark='b'/> Young ears hear up to about twenty thousand hertz, as "
                   "Part 4 showed, and the sampling theorem needs a rate above twice the highest frequency. "
                   "<bookmark mark='c'/> Forty thousand would be the bare minimum, with a perfect filter that cannot be built. "
                   "<bookmark mark='d'/> The extra four thousand one hundred leave room for a real filter to roll off between "
                   "twenty thousand and twenty-two thousand and fifty. <bookmark mark='e'/> A lower rate would have made the filter "
                   "impossible, and a higher one would not have fitted on the tape. <bookmark mark='f'/> Chapter two shows why "
                   "twice is enough.", marks="bcdef")
