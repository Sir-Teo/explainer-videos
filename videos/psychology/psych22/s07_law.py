from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403

PRIOR_COL = {"erlang": MODEL, "uniform": CAT_A, "exponential": CAT_B, "gaussian": PROTO}


class Law(VoiceoverScene):
    def construct(self):
        self.card()
        self.claim()
        self.measure()
        self.test()
        self.derive()

    def card(self):
        card = chapter_card(6, r"A universal law of generalization", r"Is there a law of the mind that holds for any "
                            r"mind?", lit={1957: r"Shepard", 1987: r"Shepard", 2001: r"Tenenbaum \& Griffiths"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter six. A universal law of generalization."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def claim(self):
        head = heading(r"Shepard's law, \ 1987")
        eq = MathTex(r"g(\mathbf{x}, \mathbf{y}) = e^{-k\, d(\mathbf{x}, \mathbf{y})}", font_size=52, color=MODEL)
        eq.move_to([0, 1.6, 0])
        rows = rows_of([
            (r"something with a consequence, \ a food that nourished, \ a tone followed by a shock: \ how likely is it "
             r"that something else will have it too?", WHITE),
            (r"Shepard gathered generalization data from people and pigeons, \ for colours, \ tones, \ shapes and "
             r"Morse code, \ and scaled each into a space", SPACE),
            (r"in every case generalization fell off with distance in the same way: \ exponentially, \ concave "
             r"upwards, \ not like a bell curve", MODEL),
            (r"he called it a candidate for the first general law of psychology, \ one that should hold for any "
             r"mind evolved anywhere", PROTO),
        ], 12.4, 25, 0.34).move_to([0, -1.0, 0])
        tag = historical_tag(r"Shepard (1987), \ \emph{Science}")
        with self.voiceover(
            "Psychology has few laws. In 1987 Roger Shepard proposed one, in the journal Science. "
            "<bookmark mark='a'/> The question is generalization. Something had a consequence: a food nourished, a "
            "tone came before a shock. How likely is it that something else will have the same consequence? "
            "<bookmark mark='b'/> Shepard gathered generalization data from people and from pigeons, for colours, "
            "tones, shapes and Morse code, and scaled each set of stimuli into a psychological space, as in the last "
            "chapter. <bookmark mark='c'/> In every case generalization fell off with distance in that space in the "
            "same way: exponentially, curving upwards, not like a bell curve. <bookmark mark='d'/> He argued it was a "
            "candidate for the first general law of psychology, and that it should hold for any mind that evolved "
            "anywhere. Let's test it, and then see why he thought so."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eq))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def measure(self):
        head = heading(r"Derivation: \ measuring generalization without bias")
        eqs = VGroup(
            MathTex(r"P(\text{``same''} \mid i, j) = \frac{b\, \eta_{ij}}{\dots}", font_size=36),
            MathTex(r"g_{ij} = \sqrt{\frac{P_{ij}\, P_{ji}}{P_{ii}\, P_{jj}}}", font_size=40, color=MODEL),
        ).arrange(DOWN, buff=0.45).move_to([-3.4, 0.6, 0])
        rows = rows_of([
            (r"confusion rates mix two things: \ how similar $i$ and $j$ are, \ $\eta_{ij}$, \ and how willing a "
             r"person is to say \emph{same}", WHITE),
            (r"under Luce's choice model the bias terms cancel in this ratio, \ leaving the similarity: \ "
             r"$g_{ij} = \eta_{ij}$", MODEL),
            (r"1 for a signal with itself; \ near 0 for signals never confused", GREY_A),
            (r"this is Shepard's measure from 1957, \ applied here to Rothkopf's 36 signals", SPACE),
        ], 6.0, 22, 0.3).move_to([3.5, 0.2, 0])
        tag = published_tag(r"Shepard (1957); \ Luce (1963)")
        with self.voiceover(
            "First, a clean measure of generalization. <bookmark mark='a'/> A confusion rate mixes two things: how "
            "similar two signals are, and how ready a person is to say same in the first place. "
            "<bookmark mark='b'/> Under Luce's choice model, the bias cancels from this ratio: the square root of the "
            "two cross-confusions over the two correct responses. What's left is the similarity itself. "
            "<bookmark mark='c'/> It is one for a signal with itself, and near zero for signals never confused. "
            "<bookmark mark='d'/> It's Shepard's measure from 1957, and we'll apply it to Rothkopf's signals."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def test(self):
        d = load("morse")
        head = heading(r"Tested on Rothkopf's signals")
        A = axes([0, 2.6], [0, 1.0], x_length=6.4, y_length=3.8, xticks=[0, 1, 2], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"distance in the Morse map \ (mean = 1)",
                 ylabel=r"generalization $g$", center=[-2.7, 0.0, 0], font_size=18)
        pts = scatter(A.ax, d["dist"], d["gen"], SPACE, 0.03, 0.45)
        x = np.linspace(0, 2.6, 200)
        ce = curve(A.ax, x, np.exp(-d["k"] * x), MODEL, 4)
        cg = DashedVMobject(curve(A.ax, x, np.exp(-d["k_gauss"] * x ** 2), PROTO, 3), num_dashes=40)
        key = legend([(MODEL, rf"exponential: \ $e^{{-{d['k']:.1f} d}}$"),
                      (PROTO, rf"Gaussian: \ $e^{{-{d['k_gauss']:.1f} d^2}}$")], font_size=20).move_to([-1.0, 2.0, 0])
        rows = rows_of([
            (r"every pair of the 36 signals: \ 630 points", SPACE),
            (rf"in log $g$, \ the exponential explains {100 * d['r2_exp']:.0f}\% of the variance", MODEL),
            (rf"a Gaussian explains less than nothing: \ {100 * d['r2_gauss']:.0f}\%", PROTO),
            (r"the map was made from the ranks alone, \ so the shape was free to come out any way", WHITE),
        ], 4.6, 21, 0.3).move_to([4.6, -0.2, 0])
        ptag = psyche_tag(r"\texttt{concepts.shepard\_generalization}, \ \texttt{fit\_exponential\_law}")
        with self.voiceover(
            "Here is the test. <bookmark mark='a'/> Each point is one pair of Morse signals, six hundred and thirty "
            "of them: the generalization between the two, against their distance in the map of the last chapter. "
            "<bookmark mark='b'/> The exponential law fits well: it explains "
            f"{100 * d['r2_exp']:.0f} percent of the variance in the log of generalization. "
            "<bookmark mark='c'/> A bell-shaped Gaussian, the natural alternative, does worse than a flat line. "
            "<bookmark mark='d'/> And this isn't built in. The map was made from the rank order of the "
            "dissimilarities alone, so the curve was free to come out any shape. It came out Shepard's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ce), FadeIn(key[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cg), FadeIn(key[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def derive(self):
        d = load("regions")
        head = heading(r"Derivation: \ why exponential?")
        line = NumberLine(x_range=[-4, 4, 1], length=6.4, color=GREY_C, include_numbers=False).move_to([-3.0, 2.0, 0])
        x0 = Dot(line.n2p(0), color=CAT_A, radius=0.09)
        regs = VGroup(*[Rectangle(width=line.n2p(a + s)[0] - line.n2p(a)[0], height=0.18, stroke_width=0,
                                  fill_color=MODEL, fill_opacity=0.35).move_to([(line.n2p(a)[0] + line.n2p(a + s)[0]) / 2,
                                                                                 2.0 - 0.35 * (k + 1), 0])
                        for k, (a, s) in enumerate(((-0.5, 1.2), (-2.1, 2.8), (-0.9, 3.6), (-3.0, 3.4)))])
        eq = MathTex(r"g(d) = \int_0^\infty p(s)\, \max\Big(0,\ 1 - \frac{d}{s}\Big)\, ds", font_size=34,
                     color=MODEL).move_to([-3.0, -0.6, 0])
        eq2 = MathTex(r"p(s) = s\, e^{-s} \;\Rightarrow\; g(d) = e^{-d}", font_size=34, color=PROTO).next_to(eq, DOWN,
                                                                                                         buff=0.3)
        A = axes([0, 4], [0, 1], x_length=5.2, y_length=3.2, xticks=[0, 1, 2, 3, 4], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"distance $d$", ylabel=r"generalization", center=[3.6, 0.6, 0],
                 font_size=18)
        cs = VGroup(*[curve(A.ax, d["d"], d[k], PRIOR_COL[k], 3) for k in PRIOR_COL])
        key = legend([(PRIOR_COL[k], {"erlang": r"$p(s) \propto s e^{-s}$", "uniform": r"sizes uniform up to 4",
                                      "exponential": r"$p(s) \propto e^{-s}$", "gaussian": r"sizes near 2"}[k])
                      for k in PRIOR_COL], font_size=17).move_to(A.ax.c2p(2.85, 0.72))
        rows = rows_of([
            (r"a consequence belongs to a region of the space of unknown size and place, \ containing the stimulus "
             r"that had it", WHITE),
            (r"generalization is the probability that a new stimulus falls in that region too, \ averaged over the "
             r"regions you can't rule out", MODEL),
            (r"spread-out priors on size all give a curve close to exponential; \ only a size known almost exactly "
             r"bends it into a shoulder: \ the law comes from \emph{uncertainty} about the region", PROTO),
        ], 12.4, 21, 0.22).to_edge(DOWN, buff=0.45)
        ptag = psyche_tag(r"\texttt{concepts.consequential\_region\_gradient}")
        with self.voiceover(
            "Why should any mind obey this? Shepard's answer is one of the most elegant arguments in psychology. "
            "<bookmark mark='a'/> The consequence, being nourishing, say, belongs to some region of the space, a "
            "consequential region, of unknown size and position. All you know is that it contains the one thing "
            "you tried. <bookmark mark='b'/> Generalization to a new stimulus is the probability that it falls in "
            "that region too, averaged over all the regions you can't rule out. In one dimension, a region of size s "
            "that contains the first stimulus also contains one at distance d with probability one minus d over s. "
            "<bookmark mark='c'/> Average over sizes. With this prior on size, the integral is exactly e to the "
            "minus d. <bookmark mark='d'/> Other priors that spread over many sizes give curves close to it, all "
            "curving upwards. Only if you already knew the size almost exactly, the pink curve, does it bend into a "
            "flat shoulder. So the law comes from uncertainty about the region, whatever the stimuli are, which is "
            "why Shepard thought it should be universal. Joshua Tenenbaum and Thomas Griffiths later recast it as Bayesian inference, which "
            "is chapter ten."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), Create(line), FadeIn(x0))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in regs], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(eq2), FadeIn(A), Create(cs[0]), FadeIn(key[0]))
            vo.wait_until("d")
            self.play(Create(cs[1]), Create(cs[2]), Create(cs[3]), FadeIn(key[1]), FadeIn(key[2]), FadeIn(key[3]),
                      FadeIn(rows[2]))
        self.clear_scene()
