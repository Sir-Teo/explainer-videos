from __future__ import annotations

from videos.music.music66.common import *  # noqa: F403


class Judging(SoundScene):
    def construct(self):
        chapter(self, 9, r"Judging generated sound", r"How close is a generated sound to the real thing?")
        self.fad()
        self.table()
        self.limits()
        self.listening()

    # ------------------------------------------------------------------
    def fad(self):
        lines = VGroup(
            label(r"embed many one-second chunks of real sound, \ and of generated sound", font_size=20, color=WHITE),
            label(r"fit a Gaussian to each cloud of embeddings, \ and measure how far apart they are:", font_size=20, color=WHITE),
            MathTex(r"d^2 = \|\mu_r - \mu_g\|^2 + \operatorname{tr}\!\big(\Sigma_r + \Sigma_g - 2(\Sigma_r\Sigma_g)^{1/2}\big)", font_size=36, color=TUNE),
            label(r"Fréchet Audio Distance \ (Kilgour et al., \ 2019): \ the embedding was a network trained on audio events", font_size=18, color=GREY_A),
            label(r"here: \ Part 63's 62-number embedding, \ reduced to its 8 main directions", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.38)
        head = label(r"Fréchet distance", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How do you score generated sound without a listener? <bookmark mark='a'/> Embed many one-second chunks of real "
            "sound and of generated sound. <bookmark mark='b'/> Fit a Gaussian to each cloud of embeddings and measure how far "
            "apart they are: <bookmark mark='c'/> the distance between their means, plus a term for how differently they "
            "spread. <bookmark mark='d'/> That is the Fréchet Audio Distance of Kevin Kilgour and colleagues, from 2019, "
            "whose embedding was a network trained to recognize sounds. <bookmark mark='e'/> Here the embedding is Part 63's, "
            "sixty-two numbers, reduced to its eight main directions."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("fad")
        dist = d["distances"]
        top = max(dist.values())
        cols = {"the training notes, replayed": GREY_A, "another bowed phrase": GOLD, "DDSP": TUNE, "mel and Griffin-Lim": BLUE, "sample by sample": EAR, "white noise": GREY_B}
        g = VGroup()
        for k in d["order"]:
            v = dist[k]
            g.add(VGroup(label(k, font_size=18, color=cols[k]), Rectangle(width=max(0.03, 5.0 * v / top), height=0.42, stroke_width=0, fill_color=cols[k], fill_opacity=0.85),
                         label(f"{v:.1f}", font_size=17, color=WHITE)))
        g.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(LEFT * 1.0 + DOWN * 0.2)
        for r in g:
            r[1].next_to(r[0], RIGHT, buff=0.3).align_to(g, LEFT).shift(RIGHT * 3.6)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        note = label(rf"distance from {d['chunks_real']} chunks of the training strings; \ smaller is closer", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"generated against real", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        ranked = sorted(d["order"], key=lambda k: dist[k])
        with self.voiceover(
            "Here are the distances from the training strings. <bookmark mark='a'/> First a cheat: the training notes "
            f"themselves, replayed, score {say(dist['the training notes, replayed'], 1)}, the best of all, as a copying "
            "generator would. Another phrase of the real string model, "
            f"the yardstick: {say(dist['another bowed phrase'], 1)}. Then the generators: DDSP "
            f"{say(dist['DDSP'], 1)}, the mel spectrogram turned back into sound {say(dist['mel and Griffin-Lim'], 1)}, the "
            f"sample-by-sample network {say(dist['sample by sample'], 1)}, and white noise {say(dist['white noise'], 1)}. "
            f"The order, closest first: {', '.join(ranked)}. It agrees with what the ear would say here; it need not always."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.3), run_time=2.0)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"the score is only as good as the embedding: \ it sees what the embedding was trained to see", WHITE),
            (r"one number for a whole set: \ it cannot say which sound failed, \ or how", WHITE),
            (r"and it rewards copying: \ a generator that replays its training set scores perfectly", WHITE),
            (r"so report it with a listening test \ (Part 58), \ a copying test \ (Part 65), \ and the prompts used", TUNE),
        ]
        rows_scene(self, r"what the distance misses", items,
                   "The distance has the faults of every single number. <bookmark mark='b'/> It is only as good as the embedding, "
                   "and sees only what the embedding was trained to see. <bookmark mark='c'/> It is one number for a whole set, so "
                   "it cannot say which sound failed, or how. <bookmark mark='d'/> And it rewards copying: a generator that replays "
                   "its training set scores perfectly. <bookmark mark='e'/> So report it with a listening test, as in Part 58, a "
                   "copying test, as in Part 65, and the prompts that were used.", marks="bcde")

    # ------------------------------------------------------------------
    def listening(self):
        items = [
            (r"MUSHRA \ (Part 58): \ hidden reference, \ hidden anchor, \ every system rated against them, \ blind", WHITE),
            (r"for generators there is no reference: \ ask instead for preference between pairs, \ or ratings of quality and of fit to the prompt", WHITE),
            (r"the prompts matter: \ report them, \ and draw them before the systems are run, \ not after", WHITE),
            (r"and say who listened: \ musicians hear artifacts that others forgive", TUNE),
        ]
        rows_scene(self, r"listening tests for generators", items,
                   "Listening tests remain the reference. <bookmark mark='b'/> Part 58's MUSHRA test hides a reference and an "
                   "anchor among the systems, and every one is rated against them, blind. <bookmark mark='c'/> A generator has no "
                   "reference, so ask instead for preferences between pairs, or ratings of quality and of how well the music fits "
                   "the prompt. <bookmark mark='d'/> The prompts matter: report them, and choose them before the systems are run, "
                   "not after. <bookmark mark='e'/> And say who listened: musicians hear artifacts that others forgive.",
                   marks="bcde")
