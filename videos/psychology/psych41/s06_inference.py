from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Inference(VoiceoverScene):
    def construct(self):
        self.card()
        self.mask_model()
        self.voices()
        self.conditioned()
        self.puzzle()

    def card(self):
        card = chapter_card(5, r"Perception and hallucination as inference", r"Can a prior be too weak, \ or too "
                            r"strong?", lit={2017: r"Powers, \ Mathys \& Corlett"}, part=PART, scale=("person",),
                            marr=("what", "how"))
        with self.voiceover("Chapter five. Perception and hallucination as inference."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def mask_model(self):
        d = load("mask")
        head = heading(r"The hollow mask, \ computed")
        A = axes([0, 14], [0, 1], x_length=5.6, y_length=3.0, xticks=[0, 4, 8, 12], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"precision of the prior that faces "
                 r"bulge", ylabel=r"P(sees a face)", center=[-3.2, 0.6, 0], font_size=13)
        c = curve(A.ax, d["pp"], d["curve"], MODEL, stroke_width=3)
        eyes = DashedLine(A.ax.c2p(4, 0), A.ax.c2p(4, 1), color=GREY_B, stroke_width=1.5)
        e_l = label(r"as precise as the eyes", font_size=12, color=GREY_B).next_to(A.ax.c2p(4, 1), UP, buff=0.08)
        g1 = VGroup(*[Dot(A.ax.c2p(min(13.9, float(p)), 0.04), radius=0.03, color=GOOD, fill_opacity=0.5)
                      for p in d["prec_typical"][:150]])
        g2 = VGroup(*[Dot(A.ax.c2p(min(13.9, float(p)), 0.10), radius=0.03, color=AUTH, fill_opacity=0.5)
                      for p in d["prec_lower"][:150]])
        eq = MathTex(r"\hat{z} = \frac{\pi_{\text{prior}}\,(+1) + \pi_{\text{eyes}}\,x}{\pi_{\text{prior}} + "
                     r"\pi_{\text{eyes}}}", font_size=30, color=MODEL).move_to([-3.2, -2.2, 0])
        rows = rows_of([
            (r"Part 14's observer: \ a prior that faces bulge ($+1$) meets a noisy stereo signal that says hollow "
             r"($-1$); \ the face is seen when the posterior is above zero", WHITE),
            (r"it needs a prior more precise than the eyes: \ the curve crosses one half where the two are equal", MODEL),
            (rf"two simulated groups of 2{{,}}000: \ with the typical spread of prior precision, \ "
             rf"{pct(d['fooled_typical'])} see a face; \ with lower precision, \ {pct(d['fooled_lower'])}", GOOD),
            (r"so weaker priors, \ or less precise ones, \ predict the patients' accuracy", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.hollow\_mask}; \ two groups of 2{,}000")
        with self.voiceover(
            "First, the mask on Psyche. <bookmark mark='a'/> It's Part 14's observer. A prior that faces bulge "
            "outward meets a noisy stereo signal that says hollow, and the face is seen when the posterior lands "
            "on the bulging side. <bookmark mark='b'/> To be fooled, the prior must be more precise than the eyes. "
            "The curve crosses one half where the two are equal. <bookmark mark='c'/> Two simulated groups of two "
            "thousand. With the typical spread of prior precision, most see a face. With lower precision, only a "
            "minority do. <bookmark mark='d'/> So weaker, or less precise, priors predict the patients' accuracy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), FadeIn(eyes), FadeIn(e_l), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(g1), FadeIn(g2))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def voices(self):
        head = heading(r"Hearing what is expected")
        rows = rows_of([
            (r"Part 14: \ perception is a prior combined with sensory evidence", MODEL),
            (r"when the evidence is weak, \ a strong enough prior can produce a percept with no input at all", AUTH),
            (r"many people who never seek care hear voices; \ hearing voices is not by itself a disorder", GOOD),
            (r"the question becomes testable: \ do voice hearers weight their expectations more?", YOU),
        ], 12.4, 24, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now hallucinations. <bookmark mark='a'/> In Part 14, perception was a prior combined with sensory "
            "evidence. <bookmark mark='b'/> When the evidence is weak, a strong enough prior can produce a percept "
            "with no input at all. <bookmark mark='c'/> And hearing voices isn't confined to illness. Many people "
            "who never seek care hear voices, and hearing voices isn't by itself a disorder. "
            "<bookmark mark='d'/> So the question becomes testable. Do voice hearers weight their expectations more "
            "heavily?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def conditioned(self):
        d = load("halluc")
        head = heading(r"Conditioned hallucinations")
        nb = len(d["blocks"])
        A = axes([0.5, nb + 0.5], [0, 0.6], x_length=5.0, y_length=2.8, xticks=list(range(1, nb + 1)),
                 yticks=[0, 0.2, 0.4, 0.6], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                 xlabel=r"block (the tone ever rarer)", ylabel=r"tone heard, \ none played", center=[-3.3, 0.6, 0],
                 font_size=13)
        x = np.arange(1, nb + 1)
        lo = VGroup(curve(A.ax, x, d["low"], GOOD, stroke_width=3), scatter(A.ax, x, d["low"], GOOD, radius=0.06))
        hi = VGroup(curve(A.ax, x, d["high"], AUTH, stroke_width=3), scatter(A.ax, x, d["high"], AUTH, radius=0.06))
        key = VGroup(label(r"prior weight 0.3", font_size=14, color=GOOD),
                     label(r"prior weight 1.5", font_size=14, color=AUTH)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        key.next_to(A, DOWN, buff=0.35)
        rows = rows_of([
            (r"Powers, \ Mathys and Corlett, \ 2017: \ a light and a faint tone together, \ again and again; \ then "
             r"the tone becomes rarer", WHITE),
            (r"everyone sometimes heard a tone that was not played; \ voice hearers, \ diagnosed or not, \ did so "
             r"more, \ and a model fitted to their reports gave their priors more weight", AUTH),
            (rf"Psyche, \ 200 learners: \ with a heavily weighted prior, \ a tone is heard on {pct(d['high_all'])} of "
             rf"silent trials; \ with a light one, \ {pct(d['low_all'])}", MODEL),
            (r"the Ledger: \ contested, \ an influential result with few independent tests", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Powers, \ Mathys \& Corlett (2017)")
        with self.voiceover(
            "In 2017 Albert Powers, Christoph Mathys and Philip Corlett tested it. <bookmark mark='a'/> People saw a "
            "light and heard a faint tone together, again and again. Then the tone became rarer. "
            "<bookmark mark='b'/> Everyone sometimes heard a tone that wasn't played. Voice hearers, with a diagnosis "
            "or without one, did so more, and a model fitted to their reports gave their priors more weight. "
            "<bookmark mark='c'/> Psyche runs the design on two hundred learners. With a heavily weighted prior, it "
            "hears a tone on many more silent trials than with a light one. <bookmark mark='d'/> The Ledger marks it "
            "contested: an influential result, with few independent tests."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(lo), Create(hi), FadeIn(key), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def puzzle(self):
        head = heading(r"Too weak, \ and too strong?")
        left = VGroup(word_chip(r"the hollow mask", color=GOOD, font_size=20, width=3.6),
                      wrapped_label(r"priors about objects weaker: \ the hollow is seen as hollow", 4.6, 19, WHITE))
        right = VGroup(word_chip(r"hallucinations", color=AUTH, font_size=20, width=3.6),
                       wrapped_label(r"priors about sensations stronger: \ a tone is heard that was not played", 4.6,
                                     19, WHITE))
        for g in (left, right):
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"Sterzer and colleagues, \ 2018: \ the predictive-coding account of psychosis must explain both", WHITE),
            (r"one answer: \ precision differs by level, \ weak at low levels and over-strong at high ones, \ or "
             r"changes over the course of an illness", MODEL),
            (r"the risk: \ a theory with a free dial at every level can fit anything; \ the frontier asks for "
             r"predictions it could fail", YOU),
        ], 12.4, 21, 0.4).move_to([0, -1.7, 0])
        tag = published_tag(r"Sterzer et al.\ (2018)")
        with self.voiceover(
            "Which leaves the puzzle from the start. <bookmark mark='a'/> The hollow mask suggests priors that are "
            "too weak. Hallucinations suggest priors that are too strong. In 2018 Philipp Sterzer and colleagues "
            "reviewed the predictive-coding account of psychosis, and it has to explain both. "
            "<bookmark mark='b'/> One answer is that precision differs by level, weak at low levels and over-strong "
            "at high ones, or changes over the course of an illness. <bookmark mark='c'/> The risk is a theory with "
            "a free dial at every level, which can fit anything. The frontier asks it for predictions it could fail."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(left), FadeIn(right))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for m, r in zip("bc", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
