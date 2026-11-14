from __future__ import annotations

from videos.psychology.psych13.common import *  # noqa: F403

PROBLEMS = [
    r"Show that $P(N \ge k)$ for $N \sim \mathrm{Poisson}(a q)$ depends on $q$ and $a$ only through $\log a + \log q$, "
    r"\ and so that the frequency-of-seeing curve's shape on a log axis gives $k$ without $a$.",
    r"Hecht's flashes delivered 54 to 148 quanta at the cornea. \ With 4\% reflected, \ half the rest absorbed in the "
    r"eye, \ and at most 20\% of what reaches the retina caught, \ how many were absorbed? \ Over 500 rods, \ what is "
    r"the chance that some rod caught two?",
    r"Foveal cones are about 0.5 minutes of arc apart. \ Find the Nyquist frequency, \ and the frequency a 90 c/deg "
    r"grating would alias to.",
    r"Derive the frequency response of a difference of Gaussians, \ and find where it peaks when the surround is "
    r"three times the centre and the two have equal area.",
    r"With the cone matrix $A$ ($3 \times N$), \ show that $P = I - A^\top (A A^\top)^{-1} A$ projects onto the null "
    r"space, \ and that adding $P\mathbf{v}$ to any spectrum makes a metamer.",
    r"With \texttt{explainer.psychology.psyche.vision}: \ compute the colour-matching functions for primaries at 630, "
    r"532 and 467 nm, \ and find the wavelengths where each is negative.",
    r"$\star$ \ Design a test that would reveal a fourth dimension of colour vision, \ and say why a match with three "
    r"primaries would not.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def recap(self):
        items = [
            (r"a dark room in 1942: \ a flash seen when five to fourteen quanta are absorbed", LIGHT),
            (r"the Poisson curve's steepness counts quanta nobody can see; \ a rod answers one", LIGHT),
            (r"optics and the mosaic: \ nothing finer than about 60 cycles per degree", WHITE),
            (r"gain control spans ten log units, \ and gives Weber's law", MODEL),
            (r"the retina sends differences: \ centre minus surround, \ a band-pass filter", CENTRE),
            (r"the cortex looks for edges: \ Gabor fields, \ simple and complex cells, \ normalization", CELL),
            (r"your CSF peaks at a few cycles per degree, \ and hides what falls outside it", YOU),
            (r"colour is three numbers: \ matching is a 3-by-3 solve, \ metamers are the null space", SCONE),
            (r"opponent channels explain hue; \ colour blindness is a lost dimension", LCONE),
            (r"constancy discounts the light, \ and the dress shows the bet", GREY_A),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 13, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part thirteen in ten lines. <bookmark mark='a'/> In a dark room in 1942, a flash was seen when five to "
            "fourteen quanta were absorbed. The steepness of a Poisson curve counted quanta nobody could see, and "
            "a single rod turned out to answer a single quantum. The optics and the cone mosaic stop detail finer "
            "than about sixty cycles per degree. Gain control spans ten log units of light, and gives Weber's law on "
            "the way. The retina sends differences, a centre minus a surround, a band-pass filter. The cortex looks "
            "for edges, with Gabor-shaped fields, simple and complex cells, and normalization. Your own contrast "
            "sensitivity peaks at a few cycles per degree, and hides what falls outside it. Colour is three numbers: "
            "matching is a three-by-three solve, and metamers are the null space. Opponent channels explain how hues "
            "look, and colour blindness is a lost dimension. And constancy discounts the light, which is the bet the "
            "dress revealed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=46.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a threshold counted in quanta; \ colour predicted by a matrix. \ Whether a sensation has a size: \ still "
             r"argued", STATUS_COLOR["replicated"]),
            (r"experiments by the dozen: \ assignment by lot, \ lesions, \ twins, \ a cave", STATUS_COLOR["replicated"]),
            (r"the report mixes seeing with saying, \ and detection theory measures the two apart",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> Today was the first objection's day again: that mathematics can't "
            "apply to the inner sense. The threshold of seeing turned out to be a number of quanta, and the matching "
            "of colours a matrix inverse that predicts what ten observers in 1955 would do. <bookmark mark='b'/> "
            "Kant's deeper worry remains. A colour match says two lights look the same; it doesn't measure how red "
            "the red looks. Whether a sensation itself has a size is still argued, and Part 27 takes it up."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[1].reply),
                      FadeIn(board.rows[2].reply))
            vo.wait_until("a")
            self.play(Indicate(board.rows[0].objection, color=KANT), FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"seeing as inference: \ the dress was a preview", [14]),
            (r"the other senses, \ each with its own code", [15]),
            (r"attention as gain and normalization", [18]),
            (r"seeing without knowing: \ D.F. and blindsight", [27]),
            (r"displays, \ warnings and colour in design", [51, 52]),
            (r"efficient coding: \ why send differences", [58]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Seeing as inference, of which the dress was a preview, is "
            "Part 14. The other senses, each with a code of its own, are Part 15. Attention, which turns out to work "
            "partly by changing gain and normalization, is Part 18. Seeing without knowing, with D.F. and "
            "blindsight, is Part 27. Displays, warnings and colour in design are Parts 51 and 52. And efficient "
            "coding, the theory of why an eye would send differences at all, is Part 58."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=13.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One proves that the "
            "curve's shape gives k. One redoes Hecht's arithmetic, and asks how often a rod would catch two. One "
            "finds the mosaic's limit and an alias. One derives the difference of Gaussians' peak. One builds "
            "metamers from a projection matrix. One uses Psyche's vision module to compute matching functions for "
            "a modern display's primaries. And the last, with the star, is the frontier's problem. Pause here if "
            "you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"B. A. Wandell, \emph{Foundations of Vision} (1995)",
             r"R. W. Rodieck, \emph{The First Steps in Seeing} (1998)",
             r"D. H. Hubel, \emph{Eye, Brain, and Vision} (1988)"],
            [r"S. Hecht, S. Shlaer \& M. H. Pirenne (1942); \ D. A. Baylor, T. D. Lamb \& K.-W. Yau (1979)",
             r"E. D. Adrian \& Y. Zotterman (1926); \ S. W. Kuffler (1953); \ R. W. Rodieck (1965)",
             r"D. H. Hubel \& T. N. Wiesel (1959, 1962); \ R. C. Reid \& J.-M. Alonso (1995)",
             r"F. W. Campbell \& J. G. Robson (1968); \ C. Blakemore \& F. W. Campbell (1969); \ D. J. Heeger (1992)",
             r"W. S. Stiles \& J. M. Burch (1955); \ A. Stockman \& L. T. Sharpe (2000)",
             r"L. M. Hurvich \& D. Jameson (1957); \ G. Jordan et al.\ (2010)",
             r"R. Lafer-Sousa, K. L. Hermann \& B. R. Conway (2015); \ P. Wallisch (2017)",
             r"A. D. Milner et al.\ (1991); \ J. N. Tinsley et al.\ (2016)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Wandell's Foundations of "
            "Vision is the place to start for the mathematics."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act III: \ the senses", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 14", font_size=32, color=GREY_B), label(r"Seeing as Inference", font_size=50),
                     wrapped_label(r"Two squares send your eye identical light, \ and look different. \ That is not a "
                                   r"failure of seeing: \ it is how seeing works.", 6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "So the eye counts quanta, and sends the brain differences, filtered and compressed. "
            "<bookmark mark='a'/> But an image on the retina is flat, and ambiguous: infinitely many worlds could "
            "have produced it. <bookmark mark='b'/> Next time, two squares that send your eye exactly the same light, "
            "and look completely different. That isn't a failure of seeing. It's how seeing works: a bet about the "
            "world, and a surprisingly good one. It's Part 14: seeing as inference."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
