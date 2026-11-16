from __future__ import annotations

from videos.music.music66.common import *  # noqa: F403


class Codecs(SoundScene):
    def construct(self):
        chapter(self, 4, r"Tokens from a codec", r"Can sound be turned into words?")
        self.idea()
        self.rvq()
        self.quiz()
        self.table()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"a language model needs a vocabulary: \ a small set of symbols, \ a few per moment", WHITE),
            (r"vector quantization: \ learn a codebook of typical frames; \ each frame becomes the number of its nearest entry", WHITE),
            (r"SoundStream \ (Zeghidour et al., \ 2021) \ and EnCodec \ (Défossez et al., \ 2022): \ an encoder, \ a quantizer, \ a decoder, \ trained together", WHITE),
            (r"their tokens are a few kilobits a second: \ an MP3's job, \ done by a network, \ with symbols at the end", TUNE),
        ]
        rows_scene(self, r"a codec's tokens", items,
                   "The second split turns sound into words. <bookmark mark='b'/> A language model needs a vocabulary: a small set "
                   "of symbols, a few for each moment. <bookmark mark='c'/> Vector quantization gives one: learn a codebook of "
                   "typical frames, and replace each frame of sound by the number of its nearest entry. <bookmark mark='d'/> "
                   "SoundStream, from Neil Zeghidour and colleagues in 2021, and EnCodec, from Alexandre Défossez and colleagues "
                   "in 2022, train an encoder, a quantizer and a decoder together. <bookmark mark='e'/> Their tokens cost a few "
                   "kilobits a second: an MP3's job, done by a network, with symbols at the end.", marks="bcde")

    # ------------------------------------------------------------------
    def rvq(self):
        lines = VGroup(
            label(r"Monochord's codec: \ each 16 ms frame's log spectrum, \ 257 numbers", font_size=20, color=WHITE),
            MathTex(r"x \approx c^{(1)}_{k_1} + c^{(2)}_{k_2} + c^{(3)}_{k_3} + c^{(4)}_{k_4}", font_size=40, color=TUNE),
            label(r"the first codebook takes the frame, \ the second what the first missed, \ and so on: \ residual vector quantization", font_size=19, color=WHITE),
            label(r"256 entries a codebook, \ so 8 bits a stage; \ 62.5 frames a second; \ codebooks learnt by k-means on the piano chorales", font_size=18, color=GREY_A),
            label(r"no learnt encoder or decoder: \ the spectrum goes in, \ Griffin-Lim's phase comes out", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.38)
        head = label(r"residual vector quantization", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Monochord's codec is the quantizer without the networks. <bookmark mark='a'/> Each sixteen-millisecond hop supplies a frame of 257 numbers, its log spectrum. <bookmark mark='b'/> The first codebook approximates the frame; the second, what the first missed; and so on: residual vector quantization, the scheme SoundStream uses. <bookmark mark='c'/> Each codebook has 256 entries, so a stage costs eight bits a frame, at sixty-two and a half frames a second, learnt by k-means on the piano chorales. <bookmark mark='d'/> There is no learnt encoder or decoder: the spectrum goes in, and Griffin-Lim's phase comes out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mark, ln in zip("abcd", lines[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("codec")
        c = clip("codec.four")
        card = listen_card(r"A piano chorale tune, \ then the same through the codec three times: \ one, \ two and four tokens a frame, \ in some order. \ Which used four?", width=10.0)
        with self.voiceover("Your turn. A piano chorale tune, then the same eight seconds through the codec three times, with one, two and four tokens a frame, in some order. Which used four?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"original", r"first", r"second", r"third"], width=2.6, buff=0.4, size=18).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        ks = ["original", "s1", "s2", "s4"]
        with self.listen(c) as snd:
            window(snd, r"a codec, \ three ways", kind="synthesized", detail=r"Part 38's piano; \ Monochord's codec", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        res = label(r"in order: \ one, \ two, \ four tokens a frame", font_size=20, color=TUNE).move_to(DOWN * 1.4)
        r = d["rows"]
        with self.voiceover(
            f"They were in order: one, two and four. If you could not tell, you were right not to: by spectrum they differ by "
            f"only {say(r['1']['dist'] - r['4']['dist'], 1)} of a decibel. For one instrument playing one kind of music, a "
            "single codebook of 256 frames already holds most of what there is; real codecs need their stages for the "
            "variety of real music."
        ):
            self.play(boxes[3][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("codec")
        rows = d["rows"]
        g = VGroup()
        for k, name in (("1", r"one token a frame"), ("2", r"two"), ("4", r"four"), ("phase only", r"unquantized spectrum: \ Griffin-Lim's phase")):
            r = rows[k]
            g.add(VGroup(label(name, font_size=19, color=WHITE), label(f"{r['tokens_per_second']:.1f}" if r["tokens_per_second"] else r"--", font_size=19, color=TUNE),
                         label(f"{r['kbps']:.1f}" if r["kbps"] else r"--", font_size=19, color=BLUE), label(f"{r['dist']:.1f} dB", font_size=19, color=EAR)))
        g.arrange(DOWN, buff=0.35)
        for r in g:
            for i, x in enumerate((-3.6, 0.4, 2.6, 4.9)):
                r[i].set_x(x)
        g.move_to(DOWN * 0.3)
        top = VGroup(*[label(t, font_size=15, color=GREY_A).move_to([x, g.get_top()[1] + 0.5, 0]) for t, x in
                       ((r"tokens a second", 0.4), (r"index kbit/s", 2.6), (r"spectral distance", 4.9))])
        head = label(r"bits against fidelity", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        note = label(r"index payload only; \ codebooks and metadata excluded", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        a, b = rows["1"], rows["4"]
        with self.voiceover(
            f"Here is the trade. One token a frame is {say(a['tokens_per_second'], 1)} tokens a second, half a kilobit for indices alone, excluding codebooks and metadata. It is "
            f"{say(a['dist'], 1)} decibels from the original by spectrum. Four tokens a frame cost four times as much and come "
            f"to {say(b['dist'], 1)}. As an unquantized reference, the true spectrum with an invented phase is "
            f"{say(rows['phase only']['dist'], 1)} away: a learned decoder can improve perceptual reconstruction; this phase-only reference is not a universal error floor. "
            "A language model over these tokens writes about sixty-two and a half symbols a second for one stream, not sixteen thousand."
        ):
            self.play(FadeIn(head), FadeIn(top), FadeIn(note), LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.25), run_time=2.0)
        self.wait(0.6)
        self.clear_scene()
