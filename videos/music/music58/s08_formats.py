from __future__ import annotations

from videos.music.music58.common import *  # noqa: F403


class Formats(SoundScene):
    def construct(self):
        chapter(self, 7, r"MP3, \ AAC and Opus", r"What did each generation of codec add?")
        self.table()
        self.mp3()
        self.aac()
        self.opus()
        self.business()

    # ------------------------------------------------------------------
    def table(self):
        rows = VGroup(VGroup(label(r"codec", font_size=17, color=GREY_A), label(r"year", font_size=17, color=GREY_A), label(r"transform", font_size=17, color=GREY_A),
                             label(r"transparent for most music near", font_size=17, color=GREY_A)))
        data = [(r"MP3 \ (MPEG-1 Layer III)", r"1993", r"32-band filter bank, \ then an 18-point MDCT", r"about 192 kbit/s stereo", EAR),
                (r"AAC", r"1997", r"MDCT, \ 2048 and 256", r"about 128 kbit/s", BLUE),
                (r"Vorbis", r"2002", r"MDCT, \ open and royalty-free", r"about 128 to 160 kbit/s", GREY_A),
                (r"HE-AAC", r"2003", r"AAC + spectral band replication", r"good sound at 48 kbit/s", BLUE),
                (r"Opus", r"2012", r"SILK \ (speech) \ + CELT \ (MDCT)", r"about 96 to 128 kbit/s; \ delay as low as 5 ms", TUNE)]
        for a, b_, c_, e, col in data:
            rows.add(VGroup(label(a, font_size=18, color=col), label(b_, font_size=18, color=WHITE), label(c_, font_size=16, color=WHITE), label(e, font_size=16, color=WHITE)))
        rows.arrange(DOWN, buff=0.3)
        for r in rows:
            r[0].next_to([-6.4, r[0].get_y(), 0], RIGHT, buff=0)
            r[1].set_x(-2.4)
            r[2].next_to([-1.6, r[0].get_y(), 0], RIGHT, buff=0)
            r[3].next_to([2.9, r[0].get_y(), 0], RIGHT, buff=0)
        rows.move_to(DOWN * 0.1)
        note = label(r"approximate figures from published listening tests; \ they depend on the music and the encoder", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"five codecs", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Real codecs are elaborations of ours. <bookmark mark='a'/> MP3, standardized in 1993, splits the signal into "
            "thirty-two bands and then applies a short MDCT within each. AAC, from 1997, uses the MDCT alone, with long and "
            "short blocks. Vorbis, from 2002, did the same, free of patents. HE-AAC, from 2003, added spectral band "
            "replication. And Opus, from 2012, joins a speech coder to an MDCT coder with as little as five milliseconds of delay. "
            "<bookmark mark='b'/> Each generation reached transparency at a lower bit rate: roughly a hundred and ninety-two "
            "kilobits for MP3 in stereo, a hundred and twenty-eight for AAC, less again for Opus, though the figures depend on "
            "the music and on the encoder."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mp3(self):
        items = [
            (r"a polyphase filter bank of 32 bands, \ inherited from Layers I and II, \ then an MDCT in each: \ a hybrid", WHITE),
            (r"a psychoacoustic model that runs on its own FFT, \ beside the coding path", WHITE),
            (r"Huffman codes for the quantized values; \ a bit reservoir; \ joint stereo \ (mid-side and intensity)", WHITE),
            (r"its filter bank aliases between bands, \ patched by butterflies: \ the price of compatibility", WHITE),
            (r"the encoder is not standardized, \ only the decoder: \ LAME \ (from 1998) \ made MP3 far better than its first encoders", TUNE),
        ]
        rows_scene(self, r"MP3", items,
                   "MP3 shows its history. <bookmark mark='b'/> It keeps the thirty-two-band polyphase filter bank of Layers One and "
                   "Two, and adds an MDCT inside each band: a hybrid. <bookmark mark='c'/> Its psychoacoustic model runs on its own "
                   "Fourier transform, beside the coding path. <bookmark mark='d'/> It uses Huffman codes, a bit reservoir and joint "
                   "stereo. <bookmark mark='e'/> Its filter bank leaks between bands, patched by little butterflies of arithmetic: "
                   "the price of compatibility. <bookmark mark='f'/> And only the decoder is standardized, not the encoder, so MP3 "
                   "kept improving long after 1993: the open-source LAME encoder, from 1998, made it far better than its first "
                   "encoders.", marks="bcdef")

    # ------------------------------------------------------------------
    def aac(self):
        items = [
            (r"a clean MDCT, \ 1,024 coefficients, \ with window switching and two window shapes", WHITE),
            (r"temporal noise shaping for attacks; \ prediction and noise substitution in later profiles", WHITE),
            (r"spectral band replication \ (HE-AAC): \ send the lower half of the spectrum, \ and a few bits describing how to rebuild the top from it", WHITE),
            (r"the codec of iTunes \ (2003), \ YouTube, \ digital radio and most phones", TUNE),
        ]
        rows_scene(self, r"AAC", items,
                   "AAC started over. <bookmark mark='b'/> A clean MDCT of a thousand and twenty-four coefficients, with window "
                   "switching and two window shapes. <bookmark mark='c'/> Temporal noise shaping for attacks, and prediction and "
                   "noise substitution in later profiles. <bookmark mark='d'/> Spectral band replication, in HE-AAC: send only the "
                   "lower half of the spectrum, and a few bits telling the decoder how to rebuild the top half from it, which works "
                   "because high harmonics resemble low ones. <bookmark mark='e'/> AAC became the codec of the iTunes Store in 2003, "
                   "of YouTube, digital radio and most phones.", marks="bcde")

    # ------------------------------------------------------------------
    def opus(self):
        items = [
            (r"Opus \ (IETF, \ 2012): \ open, \ royalty-free, \ from 6 to 510 kbit/s", WHITE),
            (r"SILK, \ a speech coder by linear prediction \ (Skype); \ CELT, \ an MDCT coder with low delay \ (Xiph); \ either or both", WHITE),
            (r"CELT codes each band's energy explicitly, \ and the band's shape on a sphere \ (pyramid vector quantization): \ the energy is always right", WHITE),
            (r"as little as 5 ms of delay: \ musicians can play together over a network", TUNE),
        ]
        rows_scene(self, r"Opus", items,
                   "Opus came from the internet. <bookmark mark='b'/> Standardized by the IETF in 2012, open and royalty-free, from "
                   "six to five hundred and ten kilobits. <bookmark mark='c'/> It contains SILK, a speech coder by linear prediction "
                   "from Skype, and CELT, a low-delay MDCT coder from Xiph, and uses either or both. <bookmark mark='d'/> CELT codes "
                   "each band's energy explicitly and the band's shape as a point on a sphere, so even at low rates the energy in "
                   "every band is right, and the ear forgives the detail. <bookmark mark='e'/> With as little as five milliseconds of delay, "
                   "musicians can play together over a network, which Part 59 will want.", marks="bcde")

    # ------------------------------------------------------------------
    def business(self):
        items = [
            (r"1999: \ Napster: \ millions of MP3s traded free; \ the industry's revenue begins a fifteen-year fall", WHITE),
            (r"2001: \ the iPod, \ a thousand songs in a pocket; \ 2003: \ the iTunes Store, \ 99 cents a song, \ in AAC", WHITE),
            (r"2008 on: \ streaming: \ Spotify in Ogg Vorbis, \ later Opus and AAC at several rates", WHITE),
            (r"the codec decided what music cost to copy, \ and so what it cost to buy", TUNE),
        ]
        rows_scene(self, r"the file that broke a business", items,
                   "And the business. <bookmark mark='b'/> In 1999 Napster let millions of people trade MP3s for nothing, and the "
                   "record industry's revenue began a fall that lasted fifteen years. <bookmark mark='c'/> In 2001 the iPod put a "
                   "thousand songs in a pocket; in 2003 the iTunes Store sold them at ninety-nine cents each, in AAC. "
                   "<bookmark mark='d'/> From 2008, streaming, Spotify in Ogg Vorbis and later others in Opus and AAC at several "
                   "rates. <bookmark mark='e'/> A codec decided what music cost to copy, and so what it cost to buy, as Part 60 "
                   "will follow.", marks="bcde")
