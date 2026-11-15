from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403


def wavelength_colour(nm: float) -> str:
    """An approximate display colour for a wavelength (for labelling only)."""
    stops = [(430, (0.45, 0.25, 0.95)), (470, (0.2, 0.45, 1.0)), (495, (0.1, 0.8, 0.85)), (520, (0.2, 0.9, 0.3)),
             (560, (0.75, 0.95, 0.2)), (585, (1.0, 0.85, 0.1)), (610, (1.0, 0.55, 0.1)), (650, (1.0, 0.25, 0.2)),
             (680, (0.85, 0.15, 0.2))]
    for (a, ca), (b, cb) in zip(stops[:-1], stops[1:]):
        if nm <= b:
            t = max(0.0, min(1.0, (nm - a) / (b - a)))
            r, g, bl = [x + t * (y - x) for x, y in zip(ca, cb)]
            return rgb_to_hex((r, g, bl))
    return rgb_to_hex(stops[-1][1])


class Space(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.colours()
        self.morse()

    def card(self):
        card = chapter_card(5, r"A map of similarity", r"Can a table of similarities be turned into a space?",
                            lit={1954: r"Ekman", 1957: r"Rothkopf", 1962: r"Shepard", 1964: r"Kruskal"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter five. A map of similarity."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def derive(self):
        head = heading(r"Derivation: \ from distances to a map")
        eqs = VGroup(
            MathTex(r"d_{ij}^2 = \|\mathbf{x}_i - \mathbf{x}_j\|^2 = b_{ii} + b_{jj} - 2\, b_{ij}, \quad b_{ij} = "
                    r"\mathbf{x}_i \cdot \mathbf{x}_j", font_size=34),
            MathTex(r"B = -\tfrac{1}{2}\, J D^{(2)} J, \qquad J = I - \tfrac{1}{n}\mathbf{1}\mathbf{1}^\top", font_size=34,
                    color=SPACE),
            MathTex(r"B = V \Lambda V^\top \;\Rightarrow\; X = V_k \Lambda_k^{1/2}", font_size=34, color=MODEL),
        ).arrange(DOWN, buff=0.4).move_to([-2.6, 0.9, 0])
        rows = rows_of([
            (r"if the dissimilarities were distances between points, \ the inner products $b_{ij}$ could be recovered "
             r"from them", WHITE),
            (r"double-centring does it: \ subtract row and column means \ (Torgerson, \ 1952)", SPACE),
            (r"the top eigenvectors are the map; \ the eigenvalues say how many dimensions it needs", MODEL),
            (r"Shepard and Kruskal's \emph{non-metric} version uses only the rank order of the dissimilarities: \ "
             r"find the map whose distances are in the same order, \ with the least \emph{stress}", PROTO),
        ], 12.4, 23, 0.28).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Suppose you have a table of how dissimilar every pair of things is. Can it be turned into a map? "
            "<bookmark mark='a'/> If the dissimilarities really were distances between points, then squared distance "
            "is a sum of inner products, and the inner products could be recovered. <bookmark mark='b'/> Warren "
            "Torgerson's double-centring does it: subtract the row and column means of the squared distances, and you "
            "get the matrix of inner products, B. <bookmark mark='c'/> Its top eigenvectors, scaled by the square "
            "roots of their eigenvalues, are the map, and the eigenvalues tell you how many dimensions it needs. "
            "<bookmark mark='d'/> Psychological dissimilarities are rarely distances in that strict sense, so Roger "
            "Shepard and Joseph Kruskal made a version that uses only their rank order: find the configuration whose "
            "distances come in the same order as the dissimilarities, with the least misfit, called stress. That is "
            "non-metric multidimensional scaling."
        ) as vo:
            self.play(FadeIn(head))
            for m, e, r in zip("abc", eqs, rows):
                vo.wait_until(m)
                self.play(Write(e), FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def colours(self):
        d = load("ekman")
        head = heading(r"Ekman's colours")
        X = d["X"] * 2.4
        cx, cy = -2.8, -0.1
        pts = VGroup()
        for (x, y), nm in zip(X, d["nm"]):
            col = wavelength_colour(nm)
            pts.add(VGroup(Dot([cx + x, cy + y, 0], radius=0.16, color=col),
                           label(f"{nm:.0f}", font_size=18, color=GREY_A).move_to([cx + 1.25 * x, cy + 1.25 * y, 0])))
        order = np.argsort(d["nm"])
        path = VMobject(color=GREY_C, stroke_width=1.5).set_points_as_corners(
            [[cx + X[i, 0], cy + X[i, 1], 0] for i in order])
        rows = rows_of([
            (r"Ekman, \ 1954: \ 31 people rated the similarity of every pair of 14 colours, \ 434 to 674 nm", WHITE),
            (rf"scaled into two dimensions \ (stress {d['stress']:.3f}): \ the colours lie on a circle", SPACE),
            (r"violet and red, \ the two ends of the spectrum, \ come round to meet: \ the colour circle that "
             r"Newton drew, \ recovered from judgements alone", MODEL),
            (r"its two directions line up roughly with the opponent channels of Part 13", PROTO),
        ], 5.6, 21, 0.3).move_to([3.8, 0.0, 0])
        ptag = psyche_tag(r"open data: \ smacof's \texttt{ekman}; \ \texttt{concepts.nonmetric\_mds}")
        with self.voiceover(
            "A classic example. <bookmark mark='a'/> In 1954 Gösta Ekman had thirty-one people rate the similarity "
            "of every pair of fourteen colours, from violet at 434 nanometres to red at 674. "
            f"<bookmark mark='b'/> Scaled into two dimensions, the fit is almost perfect, stress {d['stress']:.3f}, "
            "and the colours lie on a circle. <bookmark mark='c'/> Wavelength is a straight line, but the colours "
            "bend round so that violet and red, the two ends of the spectrum, come close together: the colour circle "
            "Newton drew, recovered from nothing but people's judgements of similarity. <bookmark mark='d'/> And the "
            "two directions of the map line up roughly with the opponent channels of Part 13: the space is largely the eye's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(path), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def morse(self):
        d = load("morse")
        head = heading(r"Rothkopf's Morse code")
        X = d["X"] * 2.9
        cx, cy = -2.9, -0.3
        L = d["lengths"]
        colmap = {1: CAT_A, 2: PROTO, 3: EXEMPLAR, 4: CAT_B, 5: MODEL}
        pts = VGroup()
        for (x, y), sym, sig, n in zip(X, d["symbols"], d["signals"], L):
            pts.add(VGroup(Dot([cx + x, cy + y, 0], radius=0.07, color=colmap[int(n)]),
                           label(str(sym), font_size=21, color=colmap[int(n)]).next_to([cx + x, cy + y, 0], UR,
                                                                                       buff=0.03)))
        beeps = (r"1 beep", r"2 beeps", r"3 beeps", r"4 beeps", r"5 beeps")
        key = legend([(colmap[k], beeps[k - 1]) for k in range(1, 6)], font_size=18)
        key.move_to([0.9, 2.0, 0])
        rows = rows_of([
            (r"Rothkopf, \ 1957: \ 598 people heard pairs of the 36 Morse signals and said whether they were the "
             r"same", WHITE),
            (rf"the confusions, \ scaled into two dimensions \ (stress {d['stress']:.2f})", SPACE),
            (r"one direction is the number of beeps; \ the other, \ roughly, \ the share of them that are long", MODEL),
            (r"Shepard, \ 1963: \ people hear Morse code by its length and its rhythm, \ not by its letters", PROTO),
        ], 5.0, 21, 0.3).move_to([4.3, -0.4, 0])
        ptag = psyche_tag(r"open data: \ smacof's \texttt{morse2}; \ \texttt{concepts.nonmetric\_mds}")
        with self.voiceover(
            "A harder case. <bookmark mark='a'/> In 1957 Ernst Rothkopf played 598 people pairs of Morse code signals, "
            "all thirty-six letters and digits, and asked whether the two were the same. Mistakes reveal "
            "similarity: the more often two different signals were called the same, the more alike they sound. "
            f"<bookmark mark='b'/> Here the confusions are scaled into two dimensions, with stress {d['stress']:.2f}. "
            "<bookmark mark='c'/> One direction of the map is the number of beeps, one to five; the other is, "
            "roughly, how many of them are long dashes rather than short dots. <bookmark mark='d'/> Roger Shepard "
            "found these two dimensions in 1963. Untrained listeners hear a Morse signal by its length and its "
            "rhythm, not as a letter. A map like this is a psychological space, and in the next chapter it carries a "
            "law."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.03), FadeIn(key), FadeIn(rows[1]),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
