from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403


class Exemplars(VoiceoverScene):
    def construct(self):
        self.card()
        self.context()
        self.gcm()
        self.fivefour()
        self.debate()

    def card(self):
        card = chapter_card(3, r"Every member remembered", r"Is a concept the set of examples you have met?",
                            lit={1978: r"Medin \& Schaffer", 1981: r"Medin \& Schwanenflugel", 1986: r"Nosofsky",
                                 2000: r"Smith \& Minda"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter three. Every member remembered."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def context(self):
        head = heading(r"Medin and Schaffer's context model")
        rng = np.random.default_rng(78)
        a = rng.normal([-3.0, 0.6], 0.5, (6, 2))
        b = rng.normal([-0.8, -0.6], 0.5, (6, 2))
        pa = VGroup(*[Dot([x, y, 0], radius=0.09, color=CAT_A) for x, y in a])
        pb = VGroup(*[Dot([x, y, 0], radius=0.09, color=CAT_B) for x, y in b])
        probe = Star(n=5, outer_radius=0.18, inner_radius=0.08, color=WHITE, fill_opacity=1).move_to([-2.0, 0.0, 0])
        lines = VGroup(*[DashedLine(probe.get_center(), d.get_center(), color=d.get_color(), stroke_width=1.5,
                                    stroke_opacity=0.6) for d in list(pa) + list(pb)])
        rows = rows_of([
            (r"store every example you have met, \ with its category", EXEMPLAR),
            (r"a new item is compared with all of them at once; \ each similar example votes for its category", WHITE),
            (r"similarity multiplies across dimensions: \ one big mismatch makes two things very different", SPACE),
            (r"no summary is kept: \ the category is its members", EXEMPLAR),
        ], 5.6, 22, 0.32).move_to([3.7, 0.1, 0])
        tag = published_tag(r"Medin \& Schaffer (1978)")
        with self.voiceover(
            "In 1978 Douglas Medin and Marguerite Schaffer proposed the opposite. <bookmark mark='a'/> Don't store "
            "a summary at all. Store every example you've met, labelled with its category. <bookmark mark='b'/> A "
            "new item is compared with all of them at once, and each example votes for its own category in "
            "proportion to how similar it is. <bookmark mark='c'/> In their context model similarity multiplies "
            "across dimensions, so a single large mismatch makes two things very different. "
            "<bookmark mark='d'/> No abstraction is ever stored. The category is simply its members, and typicality "
            "is how many of them an item resembles."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(pa), FadeIn(pb))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(probe), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.05), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def gcm(self):
        head = heading(r"Derivation: \ the generalized context model")
        eqs = VGroup(
            MathTex(r"d(\mathbf{x}, \mathbf{y}) = \Big(\sum_k w_k\, |x_k - y_k|^r\Big)^{1/r}", font_size=36),
            MathTex(r"\eta(\mathbf{x}, \mathbf{y}) = e^{-c\, d(\mathbf{x}, \mathbf{y})}", font_size=36, color=SPACE),
            MathTex(r"S_J(\mathbf{x}) = \sum_{\mathbf{y} \in J} \eta(\mathbf{x}, \mathbf{y})", font_size=36,
                    color=EXEMPLAR),
            MathTex(r"P(J \mid \mathbf{x}) = \frac{b_J\, S_J(\mathbf{x})^\gamma}{\sum_K b_K\, S_K(\mathbf{x})^\gamma}",
                    font_size=36, color=MODEL),
        ).arrange(DOWN, buff=0.35).move_to([-3.3, 0.1, 0])
        rows = rows_of([
            (r"Nosofsky, \ 1986: \ exemplars as points in a psychological space, \ with attention $w_k$ "
             r"stretching the dimensions that matter", WHITE),
            (r"$r = 1$ for dimensions you attend to separately, \ $r = 2$ for ones you see as a whole; \ with $r = 1$, "
             r"\ $e^{-c d}$ is the context model's product", SPACE),
            (r"sum the similarity to every member of each category", EXEMPLAR),
            (r"Luce's rule again, \ with a bias $b_J$ and a determinism $\gamma$", MODEL),
            (r"the same choice rule as the prototype model: \ the only difference is \emph{what} is compared", PROTO),
        ], 6.0, 21, 0.3).move_to([3.6, 0.0, 0])
        tag = published_tag(r"Nosofsky (1986)")
        with self.voiceover(
            "Robert Nosofsky put the context model into a space in 1986: the generalized context model. "
            "<bookmark mark='a'/> Examples are points in a psychological space, and the distance between two of them "
            "weights each dimension by attention, stretching the ones that matter and shrinking the rest. "
            "<bookmark mark='b'/> The exponent r is one for dimensions you notice separately, like size and colour, "
            "and two for ones you see as a whole. With r equal to one, the exponential of minus c times the distance "
            "is exactly Medin and Schaffer's product across dimensions. <bookmark mark='c'/> The evidence for a "
            "category is the summed similarity to every one of its members. <bookmark mark='d'/> And the choice is "
            "Luce's rule again, with a bias and a determinism. <bookmark mark='e'/> Put it next to the prototype "
            "model: the same distance, the same similarity, the same choice rule. The one difference is what the new "
            "item is compared with: one average, or every member."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, e, r in zip("abcd", eqs, rows):
                vo.wait_until(m)
                self.play(Write(e), FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def fivefour(self):
        d = load("gcm54")
        head = heading(r"A structure built to tell them apart: \ the 5-4 categories")
        names = [str(n) for n in d["names"]]
        items = d["items"]
        tab = VGroup()
        for i in range(9):
            col = CAT_A if names[i].startswith("A") else CAT_B
            tab.add(VGroup(label(names[i], font_size=22, color=col),
                           label(" ".join(str(int(v)) for v in items[i]), font_size=22, color=WHITE)).arrange(RIGHT,
                                                                                                       buff=0.3))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-5.2, -0.1, 0])
        pt = label(r"the prototype of A: \ 1 1 1 1", font_size=20, color=PROTO).next_to(tab, UP, buff=0.25)
        A = axes([0, 2], [0.5, 1.0], x_length=4.0, y_length=3.0, xticks=[], yticks=[0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"predicted P(A)", center=[0.6, 0.1, 0], font_size=18)
        g = d["gcm_c3"]
        pr = d["proto_c3"]
        bw = 0.3
        bars_ = VGroup(bars(A.ax, [0.35, 1.35], [g[0], g[1]], EXEMPLAR, width=bw),
                       bars(A.ax, [0.65, 1.65], [pr[0], pr[1]], PROTO, width=bw))
        nm = VGroup(label(r"A1 \ (1110)", font_size=20, color=CAT_A).next_to(A.ax.c2p(0.5, 0.5), DOWN, buff=0.12),
                    label(r"A2 \ (1010)", font_size=20, color=CAT_A).next_to(A.ax.c2p(1.5, 0.5), DOWN, buff=0.12))
        key = legend([(EXEMPLAR, r"context model"), (PROTO, r"prototype model")], font_size=19).next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"A1 shares three features with the prototype, \ A2 only two: \ the prototype model says A1 is easier",
             PROTO),
            (r"but A2 is one step from two other A's, \ and far from every B: \ the context model says A2 is at least "
             r"as easy", EXEMPLAR),
            (r"Medin and Schaffer's second experiment: \ more errors on A1 than on A2, \ as the context model "
             r"predicted", WHITE),
        ], 4.3, 20, 0.3).move_to([4.75, -0.2, 0])
        ptag = psyche_tag(r"\texttt{concepts.gcm\_prob}, \ \texttt{prototype\_prob}: \ $c = 3$, \ equal attention")
        with self.voiceover(
            "To tell the theories apart, Medin and Schaffer built categories on purpose. <bookmark mark='a'/> Here "
            "is their most famous design, the 5-4 structure: nine training items on four binary dimensions, five in "
            "category A and four in B. The prototype of A is all ones. <bookmark mark='b'/> Look at A1 and A2. A1 "
            "shares three features with the prototype; A2 only two. The prototype model says A1 should be easier. "
            "<bookmark mark='c'/> But A2 is just one step from two other members of A, and far from every member of "
            "B, while A1 is close to two B's. The context model, summing over members, says A2 should be at least as "
            "easy. <bookmark mark='d'/> In their second experiment people made more errors on A1 than on A2, against "
            "every model that adds up independent cues, and as the context model predicted. The 5-4 structure was "
            "used in dozens of studies after that, which is where the argument went next."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tab], lag_ratio=0.1), FadeIn(pt))
            vo.wait_until("b")
            self.play(Indicate(tab[0]), Indicate(tab[1]), FadeIn(A), FadeIn(nm), FadeIn(key),
                      GrowFromEdge(bars_[1][0], DOWN), GrowFromEdge(bars_[1][1], DOWN), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars_[0][0], DOWN), GrowFromEdge(bars_[0][1], DOWN), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def debate(self):
        head = heading(r"Prototypes or exemplars?")
        rows = rows_of([
            (r"Medin and Schwanenflugel, \ 1981: \ categories that no straight boundary separates were not harder to "
             r"learn: \ a problem for prototypes", EXEMPLAR),
            (r"Smith and Minda, \ 2000: \ thirty data sets with the 5-4 structure; \ a prototype model with a little "
             r"memory for exceptions fitted many of them as well", PROTO),
            (r"Homa's large categories and early learning look prototype-like; \ small categories learnt to "
             r"perfection look exemplar-like", WHITE),
            (r"and the models can mimic each other: \ an exemplar model with low precision acts like a prototype \ "
             r"(Part 48 on telling models apart)", LOST),
            (r"the most decisive evidence came from problems where attention itself has to be learnt", MODEL),
        ], 12.4, 25, 0.36).move_to([0, -0.2, 0])
        tag = published_tag(r"Medin \& Schwanenflugel (1981); \ Smith \& Minda (2000)")
        with self.voiceover(
            "The argument has run for forty years. <bookmark mark='a'/> In 1981 Medin and Paula Schwanenflugel showed "
            "that categories no straight boundary can separate were not harder to learn, which the prototype model "
            "says they must be. <bookmark mark='b'/> But in 2000 David Smith and John Paul Minda looked at thirty data "
            "sets with the 5-4 structure, and argued that a prototype model with a little memory for exceptions "
            "fitted many of them as well. <bookmark mark='c'/> Large categories, and the early stages of learning, "
            "look prototype-like; small categories learnt to perfection look exemplar-like. "
            "<bookmark mark='d'/> And the models can mimic each other: an exemplar model with low precision behaves "
            "much like a prototype. How to tell models apart is Part 48. <bookmark mark='e'/> The most decisive "
            "evidence came from a set of six problems, where it turned out that attention itself has to be learnt."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
