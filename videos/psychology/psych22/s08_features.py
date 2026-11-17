from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403
from explainer.psychology.psyche import concepts as K


def feature_set(name: str, feats, color, center, width: float = 3.0) -> VGroup:
    """A named object as a box of its features."""
    title = label(name, font_size=24, color=color)
    items = VGroup(*[label(f, font_size=18, color=GREY_A) for f in feats]).arrange(DOWN, buff=0.12)
    box = RoundedRectangle(corner_radius=0.12, width=width, height=items.height + title.height + 0.6,
                           stroke_color=color, stroke_width=2)
    g = VGroup(box, title, items)
    box.move_to(center)
    title.next_to(box.get_top(), DOWN, buff=0.15)
    items.next_to(title, DOWN, buff=0.2)
    return g


class Features(VoiceoverScene):
    def construct(self):
        self.card()
        self.axioms()
        self.violations()
        self.contrast()
        self.morse()
        self.which()

    def card(self):
        card = chapter_card(7, r"Similarity is not distance", r"Do people judge similarity the way a ruler "
                            r"measures distance?", lit={1977: r"Tversky", 1982: r"Tversky \& Gati"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter seven. Similarity is not distance."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def axioms(self):
        head = heading(r"What a distance must obey")
        eqs = VGroup(
            MathTex(r"\text{minimality:} \quad d(a, b) \ge d(a, a) = 0", font_size=36),
            MathTex(r"\text{symmetry:} \quad d(a, b) = d(b, a)", font_size=36),
            MathTex(r"\text{triangle inequality:} \quad d(a, b) + d(b, c) \ge d(a, c)", font_size=36),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-2.4, 0.9, 0])
        rows = rows_of([
            (r"a map like Ekman's or Rothkopf's is a metric space: \ every distance in it obeys these three rules", WHITE),
            (r"if similarity is closeness in such a space, \ people's judgements must obey them too", SPACE),
            (r"Amos Tversky, \ 1977: \ they don't, \ and each failure is a clue to what similarity really is", PROTO),
        ], 12.4, 23, 0.3).to_edge(DOWN, buff=0.65)
        tag = historical_tag(r"Tversky (1977), \ \emph{Psychological Review}")
        with self.voiceover(
            "The last two chapters treated similarity as closeness in a space. That is a strong claim, because any "
            "distance obeys three rules. <bookmark mark='a'/> Minimality: nothing is closer to a thing than the "
            "thing itself, and every thing is the same distance, zero, from itself. <bookmark mark='b'/> Symmetry: "
            "a is as far from b as b is from a. <bookmark mark='c'/> And the triangle inequality: the way from a to c "
            "through b is never shorter than the direct way. <bookmark mark='d'/> If similarity is closeness in a "
            "space, people's judgements must obey all three. <bookmark mark='e'/> In 1977 Amos Tversky showed that "
            "they don't, and that each failure says something about what similarity really is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            for m, e in zip("abc", eqs):
                vo.wait_until(m)
                self.play(Write(e))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def violations(self):
        d = load("morse")
        head = heading(r"Three failures")
        sym = list(d["symbols"])
        diag = 100 * d["same_diag"]
        lo, hi = int(np.argmin(diag)), int(np.argmax(diag))
        assert sym[hi] == "E" and sym[lo] == "P", (sym[hi], sym[lo])  # named on screen and in the narration
        cols = VGroup()
        texts = [
            (r"minimality", [rf"in Rothkopf's data, \ a signal heard twice is called \emph{{same}} {diag[hi]:.0f}\% "
                             rf"of the time for {sym[hi]} \ (one dot), \ but only {diag[lo]:.0f}\% for {sym[lo]} \ "
                             r"(dot, \ dash, \ dash, \ dot)",
                             r"things are not all equally similar to themselves"]),
            (r"symmetry", [r"of 69 students choosing a phrase, \ 66 preferred \emph{North Korea is similar to Red "
                           r"China}; \ 3 the reverse",
                           r"in all 21 pairs of countries, \ most put the less prominent country first"]),
            (r"the triangle", [r"Jamaica is like Cuba \ (geography); \ Cuba was like Russia \ (politics, \ 1977); \ "
                               r"Jamaica is not like Russia",
                               r"two similarities can rest on different features, \ so they need not add up"]),
        ]
        for k, (t, lines) in enumerate(texts):
            c = VGroup(label(t, font_size=28, color=(SPACE, PROTO, CAT_A)[k]),
                       rows_of([(lines[0], WHITE), (lines[1], GREY_A)], 3.7, 20, 0.3)).arrange(DOWN, buff=0.35,
                                                                                            aligned_edge=LEFT)
            c.move_to([-4.4 + 4.4 * k, 0.1, 0])
            cols.add(c)
        tag = published_tag(r"Tversky (1977), \ pp.\ 328--329, \ 334; \ data: \ Rothkopf (1957)")
        with self.voiceover(
            "Here are the three failures. <bookmark mark='a'/> Minimality. In Rothkopf's Morse experiment, when the "
            f"same signal was played twice, people called it the same {diag[hi]:.0f} percent of the time for the "
            f"letter {sym[hi]}, a single dot, but only {diag[lo]:.0f} percent for {sym[lo]}. Things are not all "
            "equally similar to themselves. <bookmark mark='b'/> Symmetry. Tversky asked sixty-nine students which "
            "phrase they would rather use. Sixty-six chose North Korea is similar to Red China. Three chose the "
            "reverse. Across all twenty-one pairs of countries, most people put the less prominent country first "
            "and compared it to the more prominent one. Direct ratings showed the same asymmetry. "
            "<bookmark mark='c'/> The triangle. Jamaica is similar to Cuba, by geography. In 1977 Cuba was similar "
            "to Russia, by politics. But Jamaica and Russia are not similar at all. The example, which Tversky built "
            "on one of William James's, works because the two similarities rest on different features, so they don't "
            "add up the way distances must."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
        self.clear_scene()

    def contrast(self):
        head = heading(r"Derivation: \ the contrast model")
        eq = MathTex(r"S(a, b) = \theta\, f(A \cap B) \;-\; \alpha\, f(A - B) \;-\; \beta\, f(B - A)", font_size=38,
                     color=MODEL).move_to([0, 2.3, 0])
        A_feats = ("East Asian", "communist", "fought in Korea, 1950", "small")
        B_feats = ("East Asian", "communist", "fought in Korea, 1950", "huge", "ancient empire", "a billion people",
                   "Great Wall", "a UN veto")
        common = {"East Asian", "communist", "fought in Korea, 1950"}
        fa = feature_set(r"North Korea", A_feats, CAT_A, [-4.6, -0.3, 0], width=3.2)
        fb = feature_set(r"China", B_feats, CAT_B, [-1.1, -0.3, 0], width=3.2)
        for box, feats in ((fa, A_feats), (fb, B_feats)):
            for t, f in zip(box[2], feats):
                if f in common:
                    t.set_color(MODEL)
        A, B = set(A_feats), set(B_feats)
        s_ab = K.contrast_similarity(A, B, 1.0, 0.8, 0.2)
        s_ba = K.contrast_similarity(B, A, 1.0, 0.8, 0.2)
        calc = VGroup(
            MathTex(rf"S(\text{{NK}}, \text{{China}}) = 3 - 0.8 \times 1 - 0.2 \times 5 = {s_ab:.1f}", font_size=30,
                    color=CAT_A),
            MathTex(rf"S(\text{{China}}, \text{{NK}}) = 3 - 0.8 \times 5 - 0.2 \times 1 = {s_ba:.1f}", font_size=30,
                    color=CAT_B),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.7, 0.7, 0])
        rows = rows_of([
            (r"similarity grows with common features, \ and shrinks with each object's distinctive ones", WHITE),
            (r"$\alpha > \beta$: \ the subject's own features count more \ (\emph{focusing})", MODEL),
            (r"a sparse subject is more similar to a rich referent than the reverse:  \ asymmetry, \ with no "
             r"distance in sight", PROTO),
        ], 5.4, 21, 0.28).move_to([3.7, -1.6, 0])
        ptag = psyche_tag(r"\texttt{concepts.contrast\_similarity} \ (an illustrative feature list)")
        with self.voiceover(
            "Tversky's alternative drops space altogether. <bookmark mark='a'/> Each object is a set of features. "
            "Similarity grows with the features two objects share, and shrinks with the features each has that the "
            "other lacks. <bookmark mark='b'/> Here is an illustrative list for the two countries. The shared "
            "features are in green. <bookmark mark='c'/> The key is that the two kinds of distinctive feature are "
            "weighted differently. In a statement like a is similar to b, attention falls on a, the subject, so its "
            "own features count more: alpha is bigger than beta. <bookmark mark='d'/> Now compute. North Korea has "
            "one feature China lacks; China has five that North Korea lacks. Starting from North Korea, similarity "
            f"is {s_ab:.1f}. Starting from China, it is {s_ba:.1f}. <bookmark mark='e'/> The less prominent country "
            "is more similar to the more prominent one than the reverse: the asymmetry, from a model with no distance "
            "in it at all."
        ) as vo:
            self.play(FadeIn(head), Write(eq), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(fa), FadeIn(fb))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Write(calc[0]))
            self.play(Write(calc[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def morse(self):
        d = load("morse")
        n, more, fewer, ties = (int(v) for v in d["tversky"])
        head = heading(r"Tversky's test, \ rerun on Rothkopf's table")
        A = axes([0, 3], [0, 400], x_length=5.0, y_length=3.6, xticks=[], yticks=[0, 200, 400],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"pairs of unequal length", center=[-3.2, 0.1, 0], font_size=18)
        bs = VGroup(bars(A.ax, [0.6], [more], MODEL, 0.7), bars(A.ax, [1.5], [fewer], LOST, 0.7),
                    bars(A.ax, [2.4], [ties], GREY_B, 0.7))
        names = VGroup(*[label(t, font_size=17, color=c).next_to(A.ax.c2p(x, 0), DOWN, buff=0.15)
                         for t, c, x in ((r"shorter first", MODEL, 0.6), (r"longer first", LOST, 1.5),
                                         (r"no difference", GREY_B, 2.4))])
        ylab2 = label(r"which order is called \emph{same} more often", font_size=16, color=GREY_A).next_to(
            names, DOWN, buff=0.15).set_x(A.get_x())
        vals = VGroup(*[label(f"{v}", font_size=20, color=WHITE).next_to(A.ax.c2p(x, v), UP, buff=0.08)
                        for v, x in ((more, 0.6), (fewer, 1.5), (ties, 2.4))])
        rows = rows_of([
            (rf"{n} pairs of Morse signals differ in length; \ in {more} of them, \ the pair is called \emph{{same}} "
             rf"more often when the shorter signal comes first", WHITE),
            (rf"Tversky's own count in 1977: \ 336, \ 181 and 38; \ ours, \ from the open table: \ {more}, \ "
             rf"{fewer} and {ties}", MODEL),
            (rf"the average difference is {d['tversky_diff']:.1f} points; \ a sign test gives $p < 10^{{-10}}$", SPACE),
            (r"read as the contrast model: \ the first signal is the subject, \ and the longer, \ richer signal makes "
             r"the better referent", PROTO),
        ], 5.6, 21, 0.3).move_to([3.6, 0.1, 0])
        ptag = psyche_tag(r"open data: \ smacof's \texttt{morse2}; \ \texttt{concepts.prominence\_asymmetry}")
        with self.voiceover(
            "Tversky also tested the asymmetry on Rothkopf's Morse data, and we can rerun his test on the open table. "
            f"<bookmark mark='a'/> {n} pairs of signals differ in length. For each, compare the two orders. In "
            f"{more} pairs, people said same more often when the shorter signal came first. In {fewer}, the "
            f"reverse. {ties} were equal. <bookmark mark='b'/> Tversky's own count was three hundred and thirty-six, "
            "one hundred and eighty-one, and thirty-eight: a match to within one pair, a nice check that the open "
            "table is the one he used. <bookmark mark='c'/> The average difference is about three points, small "
            "but very reliable. <bookmark mark='d'/> Read through the contrast model, the first signal plays the "
            "subject and the second the referent, and a short signal is more like a long one than the reverse, "
            "just as North Korea is more like China."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ptag))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b, DOWN) for b in bs], FadeIn(names), FadeIn(ylab2), FadeIn(vals), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def which(self):
        head = heading(r"Spaces or features?")
        left = VGroup(label(r"spaces work for", font_size=28, color=SPACE),
                      rows_of([(r"stimuli that vary along a few continuous dimensions: \ colours, \ tones, \ sizes, \ "
                                r"the timing of beeps", WHITE),
                               (r"Shepard's law, \ which needs a space to state", GREY_A)], 5.4, 22, 0.3)
                      ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([-3.4, 0.8, 0])
        right = VGroup(label(r"features work for", font_size=28, color=PROTO),
                       rows_of([(r"conceptual things with many discrete properties: \ countries, \ faces described "
                                 r"in words, \ animals", WHITE),
                                (r"asymmetry, \ prominence and context, \ which a fixed distance cannot show",
                                 GREY_A)], 5.4, 22, 0.3)
                       ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.4, 0.8, 0])
        rows = rows_of([
            (r"and similarity is not one thing: \ which features count depends on the task and the comparison, \ "
             r"as the exemplar models' attention weights already suggested", MODEL),
            (r"that is a problem for any theory that builds concepts out of similarity alone: \ chapter nine", LOST),
        ], 12.4, 22, 0.3).to_edge(DOWN, buff=0.65)
        with self.voiceover(
            "So who is right, Shepard or Tversky? <bookmark mark='a'/> Both, for different kinds of thing. Spaces "
            "work for stimuli that vary along a few continuous dimensions, like colours, tones and the timing of "
            "beeps, and they are what Shepard's law needs. <bookmark mark='b'/> Features work for conceptual things "
            "with many discrete properties, like countries, and they capture asymmetry and prominence, which a fixed "
            "distance cannot. <bookmark mark='c'/> And similarity is not one fixed thing. Which features count "
            "depends on the task and on what is being compared, as the attention weights of the exemplar models "
            "already suggested. <bookmark mark='d'/> That is a problem for any theory that builds concepts out of "
            "similarity alone, and in chapter nine it becomes the central problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()
