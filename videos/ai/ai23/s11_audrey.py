from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import PART, SND_C, heat, load, node_box, spectro

HIST_C = C.HUMAN


class Audrey(VoiceoverScene):
    def construct(self):
        self.card()
        self.audrey()
        self.warp()
        self.hmm()

    def card(self):
        card = chapter_card(10, r"From Audrey to hidden Markov models", r"How did machines first recognize speech?",
                            part=PART)
        with self.voiceover("Chapter ten. From Audrey to hidden Markov models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def audrey(self):
        a = load("audrey")
        hc = history_card(1952, r"K.~H.~Davis, R.~Biddulph \& S.~Balashek, \ Bell Labs",
                          r"Audrey: \ the speech split into two bands at $900$ Hz, \ each band's frequency tracked by "
                          r"counting zero crossings; \ a stored pattern for each of the ten digits, \ and the best match "
                          r"wins. \ $97$ to $99\%$ right for one speaker; \ other voices had to be adjusted for",
                          width=6.2)
        hc.to_corner(UL, buff=0.4)
        words = [str(w) for w in a["words"]]
        # Audrey's display, schematic: the low band's frequency against the high band's, a stored region per digit
        sax = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=4.2, y_length=3.2, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.4, 0.3, 0])
        jit = np.random.default_rng(52).uniform(-0.05, 0.05, (10, 2))
        gpos = np.array([[0.12 + 0.19 * (k % 5), 0.3 + 0.42 * (k // 5)] for k in range(10)]) + jit
        gpos = gpos[np.random.default_rng(7).permutation(10)]
        regions = VGroup(*[VGroup(Ellipse(width=0.62, height=0.4, color=HIST_C, stroke_width=1.5).move_to(sax.c2p(*p_)),
                                  MathTex(str(k), font_size=20, color=HIST_C).move_to(sax.c2p(*p_)))
                           for k, p_ in enumerate(gpos)])
        trail = VMobject(color=WHITE, stroke_width=3).set_points_smoothly(
            [sax.c2p(*p_) for p_ in (gpos[7] + [-0.25, -0.1], gpos[7] + [-0.1, 0.05], gpos[7], gpos[7] + [0.06, -0.04])])
        sxl = label(r"low band ($< 900$ Hz)", font_size=18, color=GREY_B).next_to(sax, DOWN, buff=0.1)
        syl = label(r"high band", font_size=18, color=GREY_B).rotate(PI / 2).next_to(sax, LEFT, buff=0.1)
        stag = note(r"schematic", font_size=18).next_to(sax, UP, buff=0.1)
        disp = VGroup(sax, regions, trail, sxl, syl, stag)
        A, B = np.asarray(a["example_b"]), np.asarray(a["example_a"])
        ta = spectro(A.T, 2.4, 1.2, lo=A.min(), hi=A.max()).move_to([3.0, 2.3, 0])
        tl = label(r"a template: \ ``seven'', \ one voice, \ one take", font_size=20, color=GREY_A).next_to(ta, UP, buff=0.08)
        res = VGroup(
            label(rf"the same voice, \ another take: \ ${100 * float(a['same_lin']):.0f}\%$ right", font_size=24, color=SND_C),
            label(rf"eleven other voices: \ ${100 * float(a['other_lin']):.0f}\%$ right", font_size=24, color=C.SURPRISE))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.0, 0.2, 0])
        how = label(r"our replica: \ $10$ templates from one Kokoro voice, \\ each word stretched to the same length, \ "
                    r"nearest template wins", font_size=20, color=GREY_A).next_to(res, DOWN, buff=0.4)
        same, other = float(a["same_lin"]), float(a["other_lin"])
        with self.voiceover(
            "Speech recognition began with digits. <bookmark mark='a'/> In 1952 three engineers at Bell Labs built "
            "Audrey. It split the sound into two frequency bands, tracked each band's frequency by counting how often "
            "the signal crossed zero, and compared the pattern with a stored one for each of the ten digits. For the "
            "speaker it was tuned to, it was right ninety-seven to ninety-nine times in a hundred; for anyone else it "
            "had to be adjusted. <bookmark mark='b'/> We built the same idea: ten templates from one Kokoro voice, one "
            "take of each digit, and each new word goes to the nearest template. <bookmark mark='c'/> The same "
            f"voice, saying the digits again a little faster: {100 * same:.0f} percent right. Eleven other voices: "
            f"{100 * other:.0f} percent. The problem of speech recognition was never the words. It was the voices."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(sax), FadeIn(sxl), FadeIn(syl), FadeIn(stag), LaggedStart(*[FadeIn(r_) for r_ in regions],
                                                                                    lag_ratio=0.1), run_time=2.0)
            self.play(Create(trail), Indicate(regions[7]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(disp))
            self.play(FadeIn(ta), FadeIn(tl), FadeIn(how))
            vo.wait_until("c")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def warp(self):
        a = load("audrey")
        D = np.asarray(a["example_cost"])
        path = np.asarray(a["example_path"])
        n, m = D.shape
        S = 4.2
        img = heat(-np.log(D + 1e-3), S * m / max(n, m), S * n / max(n, m), color=SND_C, smooth=True).move_to([-3.2, -0.3, 0])
        cw, ch = img.width / m, img.height / n
        ul = img.get_corner(UL)
        pts = [ul + np.array([cw * (j + 0.5), -ch * (i + 0.5), 0]) for i, j in path]
        pl = VMobject(color=WHITE, stroke_width=3).set_points_as_corners(pts)
        xl = label(r"the template, \ frame by frame $\to$", font_size=18, color=GREY_A).next_to(img, UP, buff=0.1)
        yl = label(r"a new take $\downarrow$", font_size=18, color=GREY_A).rotate(PI / 2).next_to(img, LEFT, buff=0.1)
        rows = [MathTex(r"D(i, j) = d(i, j) + \min\big\{D(i{-}1, j),\ D(i, j{-}1),\ D(i{-}1, j{-}1)\big\}", font_size=30)]
        whys = [why(r"the cheapest path to $(i, j)$ \\ comes from one of three neighbours", font_size=20)]
        step = ladder(self, rows, whys, keep=1, top=2.9, x=0.4, align_index=None, edge=6.9)
        res = VGroup(
            label(rf"with time warping: \ same voice ${100 * float(a['same_dtw']):.0f}\%$, \ other voices "
                  rf"${100 * float(a['other_dtw']):.0f}\%$", font_size=22, color=SND_C),
            label(rf"templates from ten voices, \ two new voices: \ ${100 * float(a['multi_dtw']):.0f}\%$", font_size=22,
                  color=C.INTERVAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.3, -0.4, 0])
        cite_ = cite(r"T.~Vintsyuk (1968); \ H.~Sakoe \& S.~Chiba (1978)", corner=DR)
        od, sd, md = float(a["other_dtw"]), float(a["same_dtw"]), float(a["multi_dtw"])
        better = "helps" if od > float(a["other_lin"]) + 0.02 else "barely helps"
        with self.voiceover(
            "People say the same word fast or slow, stretching some sounds and not others, so squeezing every word to "
            "one length is crude. <bookmark mark='a'/> In 1968 Taras Vintsyuk in Kyiv, and in 1978 Hiroaki Sakoe and "
            "Seibi Chiba at NEC, aligned the two by dynamic programming: dynamic time warping. The cheapest "
            "alignment to each pair of frames extends the cheapest alignment to one of three neighbours. "
            "<bookmark mark='b'/> Here is the path that matches a new take of seven to the template. "
            f"<bookmark mark='c'/> Warping {better}: {100 * sd:.0f} percent for the same voice, {100 * od:.0f} for the "
            f"others. And with templates from ten voices, two voices it has never heard get {100 * md:.0f} percent. "
            "More examples beat cleverer matching, a lesson the field would learn again and again."
        ) as vo:
            self.play(FadeIn(img), FadeIn(xl), FadeIn(yl), FadeIn(cite_))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            self.play(Create(pl), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hmm(self):
        # a left-to-right HMM for a word, schematic: states for its sounds, each with a mixture of Gaussians
        states = VGroup(*[Circle(radius=0.38, color=SND_C, stroke_width=2.5) for _ in range(4)]).arrange(RIGHT, buff=0.9)
        states.move_to([-2.6, 1.6, 0])
        sl = VGroup(*[label(t, font_size=20, color=WHITE).move_to(s) for t, s in zip((r"/s/", r"/e/", r"/v/", r"/n/"), states)])
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=GREY_B, stroke_width=2.5,
                             max_tip_length_to_length_ratio=0.25) for a, b in zip(states, states[1:])])
        loops = VGroup(*[CurvedArrow(s.get_top() + LEFT * 0.2, s.get_top() + RIGHT * 0.2, angle=-PI * 1.4, color=GREY_B,
                                     stroke_width=2, tip_length=0.12) for s in states])
        gm = VGroup()
        for s in states:
            xs = np.linspace(-1, 1, 40)
            y = 0.5 * np.exp(-((xs + 0.3) / 0.25) ** 2) + 0.35 * np.exp(-((xs - 0.35) / 0.3) ** 2)
            gm.add(VMobject(stroke_color=C.MODEL_Q, stroke_width=2).set_points_smoothly(
                [s.get_bottom() + np.array([0.4 * x, -0.25 - 0.6 * v, 0]) for x, v in zip(xs, y)]))
        gl = label(r"each state: \ a mixture of Gaussians over the frame's spectrum", font_size=20, color=C.MODEL_Q)
        gl.next_to(gm, DOWN, buff=0.3)
        tag = note(r"schematic: \ a left-to-right model for ``seven''", font_size=18).next_to(states, UP, buff=0.5)
        eq = cmath(r"\hat W", r"=", r"\arg\max_W", r"P(\text{sound} \mid W)", r"\, P(W)",
                   colors={r"P(\text{sound} \mid W)": SND_C, r"\, P(W)": C.TRUE_P}, font_size=36).move_to([3.4, -0.2, 0])
        eql = VGroup(label(r"acoustic model: \ the HMMs", font_size=20, color=SND_C),
                     label(r"language model: \ $n$-grams (Part 7)", font_size=20, color=C.TRUE_P)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        eql.next_to(eq, DOWN, buff=0.25)
        dnn = node_box(r"2012: \ deep networks replace the Gaussian mixtures \\ (Toronto, \ Microsoft, \ Google, \ IBM)",
                       C.NEURAL, font_size=20).move_to([0.2, -2.8, 0])
        cite_ = cite(r"J.~Baker (1975); \ F.~Jelinek (1976); \ L.~Rabiner (1989); \ G.~Hinton et al.\ (2012)", corner=UR)
        with self.voiceover(
            "From the mid-1970s, at Carnegie Mellon and at IBM, recognition became statistics. <bookmark mark='a'/> "
            "Each word is a hidden Markov model, Part 7's model: a chain of states, one for each sound, that the "
            "speech walks through, lingering or moving on. <bookmark mark='b'/> Each state scores the spectrum of a "
            "frame with a mixture of Gaussians, all of it trained by EM and decoded by Viterbi. <bookmark mark='c'/> "
            "And words are chosen by Bayes' rule: the transcript that best explains the sound, times what a language "
            "model expects. That recipe, scaled up, ran dictation and telephone systems for thirty years. "
            "<bookmark mark='d'/> In 2012 four labs reported together that deep networks beat the Gaussian mixtures "
            "as the model of sound. The next question was whether a network could learn the whole thing, without "
            "being told which frame is which sound."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(tag), LaggedStart(*[FadeIn(VGroup(s, l_)) for s, l_ in zip(states, sl)],
                                                               lag_ratio=0.2), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arr], lag_ratio=0.2), FadeIn(loops), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(gm), FadeIn(gl))
            vo.wait_until("c")
            self.play(Write(eq), FadeIn(eql))
            vo.wait_until("d")
            self.play(FadeIn(dnn))
        self.wait(0.3)
        self.clear_scene()
