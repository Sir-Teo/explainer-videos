from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import ACOU_C, PART, SEM_C, SND_C, TEXT_C, code_grid, load, node_box, spectro

SPEAK_C = C.MODEL_Q


class TTS(VoiceoverScene):
    def construct(self):
        self.card()
        self.early()
        self.wavenet()
        self.codecs()
        self.narrator()

    def card(self):
        card = chapter_card(13, r"Speaking", r"How did machines learn to talk?", lit=(1996,), part=PART)
        with self.voiceover("Chapter thirteen. Speaking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def early(self):
        # source and filter, schematic: a buzz of pulses through resonances (formants) makes a vowel
        ax1 = Axes(x_range=[0, 1, 1], y_range=[0, 1.1, 1], x_length=3.2, y_length=1.4, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        pulses = VGroup(*[Line(ax1.c2p(x, 0), ax1.c2p(x, 0.9), color=SPEAK_C, stroke_width=3) for x in np.linspace(0.05, 0.95, 10)])
        src = VGroup(ax1, pulses, label(r"the source: \ a buzz", font_size=20, color=SPEAK_C).next_to(ax1, DOWN, buff=0.1))
        ax2 = Axes(x_range=[0, 4000, 1000], y_range=[0, 1.1, 1], x_length=3.2, y_length=1.4, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        f = np.linspace(0, 4000, 200)
        H = sum(np.exp(-((f - fc) / 90) ** 2) * a for fc, a in ((730, 1.0), (1090, 0.7), (2440, 0.4)))
        filt = VGroup(ax2, VMobject(color=SND_C, stroke_width=3).set_points_smoothly([ax2.c2p(x, y) for x, y in zip(f, H)]),
                      label(r"the filter: \ formants of ``ah''", font_size=20, color=SND_C).next_to(ax2, DOWN, buff=0.1))
        sf = VGroup(src, MathTex(r"\to", font_size=40), filt).arrange(RIGHT, buff=0.4).move_to([-2.8, 1.6, 0])
        tag = note(r"schematic \ (formants: \ Peterson \& Barney, 1952)", font_size=18).next_to(sf, UP, buff=0.15)
        eras = VGroup(*[label(t, font_size=22, color=c_) for t, c_ in (
            (r"1939: \ the Voder, \ played on keys and a pedal", GREY_A),
            (r"1980: \ Dennis Klatt's formant synthesizer \ (the voice Stephen Hawking used grew from it)", SPEAK_C),
            (r"1996: \ unit selection: \ splice recorded pieces of one speaker \ (Hunt \& Black)", SPEAK_C),
            (r"2000s: \ statistical parametric synthesis: \ HMMs predict the spectrum", SPEAK_C))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28).scale(1.15).move_to([0, -1.5, 0])
        if eras.width > 13:
            eras.width = 13
        with self.voiceover(
            "Speaking is the inverse problem, and it is older than listening. <bookmark mark='a'/> In 1939 Bell Labs "
            "showed the Voder at the World's Fair: an operator played speech on keys and a pedal. The idea behind it "
            "is the voice as a source and a filter: the vocal folds buzz, and the throat and mouth shape the buzz "
            "with resonances, the formants. <bookmark mark='b'/> In 1980 Dennis Klatt's formant synthesizer computed "
            "those resonances from rules; the voice Stephen Hawking used grew out of his work. <bookmark mark='c'/> "
            "The robotic edge went away when synthesizers started reusing real recordings: in unit selection, a "
            "speaker reads for hours, and the system splices together the pieces that join best. "
            "<bookmark mark='d'/> In the 2000s statistical models, hidden Markov models again, predicted the spectrum "
            "instead, smooth but muffled."
        ) as vo:
            self.play(FadeIn(sf), FadeIn(tag))
            self.play(FadeIn(eras[0]))
            vo.wait_until("b")
            self.play(FadeIn(eras[1]))
            vo.wait_until("c")
            self.play(FadeIn(eras[2]))
            vo.wait_until("d")
            self.play(FadeIn(eras[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wavenet(self):
        # dilated causal convolutions, schematic: 4 layers, dilations 1, 2, 4, 8
        n = 16
        xs = np.linspace(-6.0, -0.6, n)
        layers = VGroup()
        ys = [-2.4, -1.4, -0.4, 0.6, 1.6]
        for y in ys:
            layers.add(VGroup(*[Dot([x, y, 0], radius=0.07, color=GREY_B) for x in xs]))
        edges = VGroup()
        t = n - 1
        active = {t}
        for li, dil in enumerate((8, 4, 2, 1)):
            lvl = 3 - li
            nxt = set()
            for a in active:
                for b in (a, a - dil):
                    if b >= 0:
                        edges.add(Line(layers[lvl + 1][a].get_center(), layers[lvl][b].get_center(), color=SPEAK_C,
                                       stroke_width=2))
                        nxt.add(b)
            active = nxt
        top = layers[-1][t]
        out = Dot(top.get_center(), radius=0.12, color=SPEAK_C)
        ll = VGroup(*[label(rf"dilation ${d}$", font_size=16, color=GREY_B).next_to(layers[i + 1], LEFT, buff=0.1)
                      for i, d in enumerate((1, 2, 4, 8))])
        il = label(r"past samples", font_size=18, color=GREY_B).next_to(layers[0], DOWN, buff=0.1)
        tag = note(r"schematic", font_size=18).next_to(layers, UP, buff=0.2)
        rows = [MathTex(r"p(\mathbf x) = \prod_t p(x_t \mid x_1, \dots, x_{t-1})", font_size=32),
                MathTex(r"\mu\text{-law: } \ \operatorname{sign}(x)\,\frac{\ln(1 + 255|x|)}{\ln 256} \ \to \ 256 \text{ levels}",
                        font_size=28)]
        whys = [why(r"a language model over samples, \\ $16{,}000$ a second", font_size=20),
                why(r"each sample a token: \ fine steps for quiet sounds", font_size=20)]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=3.4, align_index=None, buff=0.8, edge=6.9)
        taco = node_box(r"Tacotron 2 (2017): \ text $\to$ mel spectrogram $\to$ WaveNet; \\ listeners: \ $4.53$ "
                        r"against $4.58$ for real recordings", TEXT_C, font_size=20).move_to([3.3, -1.7, 0])
        cite_ = cite(r"A.~van den Oord et al., \textit{WaveNet} (2016); \ J.~Shen et al.\ (2017)", corner=DR)
        with self.voiceover(
            "In 2016 DeepMind's WaveNet threw out the vocoder's rules and generated the wave itself, one sample at a "
            "time. <bookmark mark='a'/> It is a language model whose tokens are samples: each predicted from all the "
            "ones before, sixteen thousand a second, <bookmark mark='b'/> each sample squashed onto 256 levels by a "
            "logarithmic mu-law curve, so the vocabulary is small. <bookmark mark='c'/> To see far enough into the "
            "past, its convolutions skip by one, two, four and eight samples, doubling the reach with each layer. "
            "Listeners preferred it to the best systems of the day, but it was very slow. <bookmark mark='d'/> Google's "
            "Tacotron 2 split the job: a sequence-to-sequence network turns text into a mel spectrogram, and WaveNet "
            "turns that into sound. Listeners scored it 4.53 out of 5; real recordings scored 4.58."
        ) as vo:
            self.play(FadeIn(layers), FadeIn(il), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(ll), LaggedStart(*[Create(e) for e in edges], lag_ratio=0.03), FadeIn(out), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(taco))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def codecs(self):
        prompt = node_box(r"$3$ seconds of a voice \\ (as codec tokens)", ACOU_C, font_size=20)
        text = node_box(r"the text \\ (phonemes)", TEXT_C, font_size=20)
        ar = node_box(r"autoregressive transformer: \\ codebook $1$, \ frame by frame", SPEAK_C, font_size=20)
        nar = node_box(r"non-autoregressive: \\ codebooks $2$ to $8$", SPEAK_C, font_size=20)
        dec = node_box(r"EnCodec's decoder", ACOU_C, font_size=20)
        for m in (prompt, text, ar, nar, dec):
            m.scale(1.25)
        ins = VGroup(text, prompt).arrange(DOWN, buff=0.5).move_to([-4.9, 0.6, 0])
        ar.move_to([-0.9, 1.5, 0])
        nar.move_to([-0.9, -0.5, 0])
        dec.move_to([3.0, 0.5, 0])
        arr = VGroup(Arrow(text.get_right(), ar.get_left(), buff=0.1, color=GREY_B),
                     Arrow(prompt.get_right(), ar.get_left(), buff=0.1, color=GREY_B),
                     Arrow(ar.get_bottom(), nar.get_top(), buff=0.1, color=GREY_B),
                     Arrow(nar.get_right(), dec.get_left(), buff=0.1, color=GREY_B))
        wave = FunctionGraph(lambda x: 0.3 * np.sin(9 * x) * np.exp(-0.3 * x * x), x_range=[-1.0, 1.0], color=SND_C)
        wave.move_to([5.7, 0.5, 0])
        tag = note(r"schematic", font_size=18).to_corner(DL, buff=0.3)
        facts = label(r"VALL-E (Microsoft, January 2023): \ $60{,}000$ hours of English; \ a new voice from a "
                      r"$3$-second prompt", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.7)
        cite_ = cite(r"C.~Wang et al., \textit{VALL-E} (2023)", corner=DR)
        with self.voiceover(
            "Then speech synthesis became language modelling, with chapter nine's codec tokens as the words. "
            "<bookmark mark='a'/> Microsoft's VALL-E, in January 2023, takes the text and three seconds of someone's "
            "voice, written as EnCodec tokens. <bookmark mark='b'/> A transformer continues the voice prompt, writing "
            "the first codebook frame by frame; <bookmark mark='c'/> a second one fills in the finer codebooks all at "
            "once, and the codec's decoder makes the wave. <bookmark mark='d'/> Trained on sixty thousand hours, it "
            "could speak in a voice it had heard for three seconds, the trick that made voice cloning cheap, and that "
            "every speech model since has had to reckon with."
        ) as vo:
            self.play(FadeIn(text), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(prompt))
            vo.wait_until("b")
            self.play(GrowArrow(arr[0]), GrowArrow(arr[1]), FadeIn(ar))
            vo.wait_until("c")
            self.play(GrowArrow(arr[2]), FadeIn(nar), GrowArrow(arr[3]), FadeIn(dec), Create(wave))
            vo.wait_until("d")
            self.play(FadeIn(facts))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def narrator(self):
        nr = load("narrator")
        avail = bool(nr["available"])
        facts = VGroup(*[label(t, font_size=21, color=c_) for t, c_ in (
            (r"Qwen3-TTS (Alibaba, January 2026): \ over $5$ million hours, \ $10$ languages", SPEAK_C),
            (r"its tokenizer: \ $12.5$ frames a second, \ $16$ codebooks of $2{,}048$; \ the first semantic, \ $15$ acoustic", SEM_C),
            (r"the transformer writes codebook $1$; \ a small module predicts the other $15$", SPEAK_C),
            (r"first sound after about $0.1$ s; \ a voice cloned from $3$ seconds", SPEAK_C))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=0.45)
        if facts.width > 13:
            facts.width = 13
        cite_ = cite(r"Qwen Team, \textit{Qwen3-TTS Technical Report} (2026)", corner=DR)
        if avail:
            codes = np.asarray(nr["ref_codes"]).T  # 16 x frames
            T = codes.shape[1]
            show = min(T, 50)
            grid = code_grid(codes[:, :show], cell=0.12, K=int(nr["K"])).move_to([-2.6, -1.6, 0])
            M = np.asarray(nr["ref_mel"])
            mel = spectro(M[:, :show * 8], grid.width, 0.9, lo=M.min(), hi=M.max()).next_to(grid, UP, buff=0.12)
            gl = label(rf"the clip it clones its English voice from: \ ${show / float(nr['hz']):.0f}$ s as "
                       rf"${int(nr['n_q'])} \times {show}$ codes", font_size=19, color=GREY_A).next_to(mel, UP, buff=0.1)
            rl = VGroup(label(r"codebook $1$: \ semantic", font_size=16, color=SEM_C).next_to(grid, RIGHT, buff=0.1).align_to(grid, UP),
                        label(r"codebooks $2$--$16$: \ acoustic", font_size=16, color=ACOU_C).next_to(grid, RIGHT, buff=0.1).align_to(grid, DOWN))
            side = VGroup(label(rf"${float(nr['bps']):,.0f}$ bits a second".replace(",", "{,}"), font_size=22, color=SEM_C),
                          label(rf"encoded and decoded again: \ log-mel distance ${float(nr['mel_dist']):.2f}$", font_size=20,
                                color=GREY_A))
            if bool(nr["generated"]):
                gc = np.asarray(nr["gen_codes"]).T
                g2 = code_grid(gc, cell=0.13, K=int(nr["K"]))
                gtxt = label(r"and the narrator saying \ ``" + str(nr["sentence"]) + r"'': \ " +
                             rf"${gc.shape[1]}$ frames", font_size=19, color=SPEAK_C)
                side.add(VGroup(gtxt, g2).arrange(DOWN, buff=0.12, aligned_edge=LEFT))
            side.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, -1.3, 0])
            if side.width > 4.8:
                side.width = 4.8
            body = Group(mel, gl, grid, rl)
        else:
            side = VGroup()
            body = label(r"(Qwen3-TTS isn't installed on the computer that built this video, \\ so its codes are not shown)",
                         font_size=22, color=GREY_B).move_to(DOWN * 1.3)
        gen = ""
        if avail and bool(nr["generated"]):
            gen = (f" And here is the narrator saying a sentence of this part: {int(np.asarray(nr['gen_codes']).shape[0])} "
                   "frames, sixteen codes each, written by its transformer before a decoder made them into sound.")
        own = (f"Here is the {float(nr.get('ref_seconds', 0)):.0f}-second clip it learned its English voice from, as the codes "
               "the narrator sees: "
               f"{int(np.asarray(nr['ref_codes']).shape[0])} frames of sixteen codes, {float(nr['bps']):,.0f} bits a "
               "second." + gen) if avail else ("Its codes can't be shown here, because Qwen3-TTS isn't installed on "
                                               "the computer that built this video.")
        with self.voiceover(
            "This series has a narrator of its own. <bookmark mark='a'/> Qwen3-TTS, from Alibaba in January 2026, was "
            "trained on over five million hours of speech in ten languages. Its tokenizer is a codec like Mimi: 12.5 "
            "frames a second, sixteen codebooks of 2,048, the first taught by a self-supervised model to carry "
            "what is said, the other fifteen how it sounds. <bookmark mark='b'/> Its transformer writes the first "
            "codebook of each frame, a small module predicts the other fifteen, and the first sound comes out after "
            "about a tenth of a second. It can clone a voice from three seconds. <bookmark mark='c'/> " + own +
            f" <bookmark mark='d'/> This copy of the video is read by {narration_credit()}. From the Voder's keys to "
            "here took eighty-seven years."
        ) as vo:
            self.play(FadeIn(facts[0]), FadeIn(cite_))
            self.play(FadeIn(facts[1]), FadeIn(body))
            vo.wait_until("b")
            self.play(FadeIn(facts[2]), FadeIn(facts[3]))
            vo.wait_until("c")
            self.play(FadeIn(side))
            vo.wait_until("d")
        self.wait(0.3)
        self.clear_scene()
