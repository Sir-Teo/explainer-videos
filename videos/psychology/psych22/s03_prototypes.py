from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403


def dots(points, center, scale: float = 0.22, color=CAT_A, radius: float = 0.06) -> VGroup:
    return VGroup(*[Dot([center[0] + scale * x, center[1] + scale * y, 0], radius=radius, color=color)
                    for x, y in points])


class Prototypes(VoiceoverScene):
    def construct(self):
        self.card()
        self.patterns()
        self.homa()
        self.model()

    def card(self):
        card = chapter_card(2, r"The average member", r"Is a concept stored as its central tendency?",
                            lit={1968: r"Posner \& Keele", 1975: r"Rosch", 1976: r"Homa \& Vosburgh"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter two. The average member."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def patterns(self):
        rng = np.random.default_rng(1968)
        proto = rng.uniform(-3, 3, (9, 2))
        dist = [proto + rng.normal(0, 0.55, (9, 2)) for _ in range(4)]
        head = heading(r"Dot patterns and a prototype nobody saw")
        boxes = VGroup()
        for k, pts in enumerate(dist):
            c = np.array([-5.0 + 2.25 * k, 1.3])
            boxes.add(VGroup(Square(1.8, color=GREY_D, stroke_width=1.5).move_to([c[0], c[1], 0]),
                             dots(pts, c, color=CAT_A)))
        pc = np.array([4.4, 1.3])
        pbox = VGroup(Square(1.8, color=PROTO, stroke_width=2.5).move_to([pc[0], pc[1], 0]), dots(proto, pc, color=PROTO))
        tl = label(r"trained: \ distortions", font_size=22, color=CAT_A).next_to(boxes, UP, buff=0.15)
        pl = label(r"never shown: \ the prototype", font_size=22, color=PROTO).next_to(pbox, UP, buff=0.15)
        rows = rows_of([
            (r"Posner and Keele, \ 1968: \ each category is a random pattern of nine dots; \ people learn only "
             r"jittered distortions of it", WHITE),
            (r"at test, \ the prototype itself, \ never seen, \ is classified as well as the patterns they trained on, "
             r"\ and better than new distortions", PROTO),
            (r"after a week, \ memory for the trained patterns has faded more than for the prototype", CAT_A),
            (r"the mind seems to have extracted the central tendency", MODEL),
        ], 12.4, 24, 0.3).to_edge(DOWN, buff=0.65)
        tag = historical_tag(r"Posner \& Keele (1968, \ 1970)")
        with self.voiceover(
            "If membership is similarity, the simplest answer to similarity to what is: to the average member, the "
            "prototype. <bookmark mark='a'/> In 1968 Michael Posner and Steven Keele made categories you could not "
            "have met before. Each category began as a random pattern of nine dots, and people learnt to classify "
            "only jittered distortions of it. They never saw the original. <bookmark mark='b'/> At test the original "
            "pattern, the prototype, was classified as well as the patterns they had trained on, and better than "
            "new distortions. <bookmark mark='c'/> In a follow-up, after a week the trained patterns had faded more "
            "than the prototype had. <bookmark mark='d'/> The mind, it seemed, had extracted the central tendency of "
            "what it saw, and stored that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(pbox), FadeIn(pl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def homa(self):
        d = load("homa")
        head = heading(r"Homa and Vosburgh, \ 1976: \ the test, \ from the open data")
        kinds = ("proto", "low", "med", "high")
        xs = np.arange(4)
        A = axes([-0.5, 4.5], [0, 1], x_length=6.6, y_length=3.6, xticks=[], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"classified correctly", center=[-2.6, 0.2, 0],
                 font_size=18)
        size_col = (CAT_B, EXEMPLAR, PROTO)
        g = VGroup()
        for k, n in enumerate(d["sizes"]):
            y = [d[f"mixed_{s}"][k] for s in kinds]
            g.add(VGroup(curve(A.ax, xs, y, size_col[k], 3), scatter(A.ax, xs, y, size_col[k], 0.07, 1.0)))
        old = scatter(A.ax, [4, 4, 4], d["old_mixed"], CAT_A, 0.08, 1.0)
        names = VGroup(*[label(t, font_size=19, color=GREY_A).next_to(A.ax.c2p(i, 0), DOWN, buff=0.12) for i, t in
                         enumerate((r"prototype", r"low", r"medium", r"high distortion", r"old items"))])
        key = legend([(size_col[k], rf"{int(n)} members per category") for k, n in enumerate(d["sizes"])],
                     font_size=19).move_to([4.4, 1.5, 0])
        rows = rows_of([
            (r"the prototype, \ never seen, \ is classified best", PROTO),
            (r"new patterns fall off with their distance from it", CAT_B),
            (r"and the larger the category, \ the better the generalization", EXEMPLAR),
            (r"random patterns from unrelated prototypes: \ put in a category 24 to 38\% of the time", GREY_A),
        ], 4.4, 20, 0.3).move_to([4.5, -1.1, 0])
        ptag = psyche_tag(r"open data: \ catlearn's \texttt{homa76} \ (Wills et al.)")
        with self.voiceover(
            "Here are the numbers from a careful version by Donald Homa and Robert Vosburgh in 1976, from the open "
            "data packaged with the catlearn library. <bookmark mark='a'/> The never-seen prototype is classified "
            "best of all. <bookmark mark='b'/> New patterns fall off with their distortion, their distance from the "
            "prototype. <bookmark mark='c'/> And the more members a category had, the better new patterns were "
            "classified. <bookmark mark='d'/> A prototype theory can explain that: the average of nine noisy patterns "
            "is a better estimate of the original than the average of three. But a rival theory explains it too, "
            "differently: every example you remember is one more thing a new pattern can resemble. Telling the two "
            "apart takes categories built for the purpose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(names), FadeIn(ptag), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in g], lag_ratio=0.3), FadeIn(old), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(Indicate(key, color=EXEMPLAR))
        self.clear_scene()

    def model(self):
        head = heading(r"Derivation: \ the prototype model")
        eqs = VGroup(
            MathTex(r"\mathbf{p}_J = \frac{1}{|J|} \sum_{\mathbf{y} \in J} \mathbf{y}", font_size=38, color=PROTO),
            MathTex(r"d(\mathbf{x}, \mathbf{p}_J) = \sum_k w_k\, |x_k - p_{Jk}|", font_size=38),
            MathTex(r"\eta(\mathbf{x}, \mathbf{p}_J) = e^{-c\, d(\mathbf{x}, \mathbf{p}_J)}", font_size=38, color=SPACE),
            MathTex(r"P(J \mid \mathbf{x}) = \frac{\eta(\mathbf{x}, \mathbf{p}_J)}{\sum_K \eta(\mathbf{x}, \mathbf{p}_K)}",
                    font_size=38, color=MODEL),
        ).arrange(DOWN, buff=0.35).move_to([-3.2, 0.1, 0])
        rows = rows_of([
            (r"store one summary per category: \ the mean of its members", PROTO),
            (r"distance weighted by attention $w_k$ to each dimension", WHITE),
            (r"similarity decays with distance, \ at a rate $c$", SPACE),
            (r"choose in proportion to similarity: \ Luce's rule, \ from Part 11", MODEL),
            (r"a strong prediction: \ only categories that a straight boundary can separate should be easy", LOST),
        ], 6.0, 22, 0.32).move_to([3.6, 0.0, 0])
        with self.voiceover(
            "As an equation, the prototype model has four lines. <bookmark mark='a'/> Each category is stored as one "
            "summary, the mean of its members. <bookmark mark='b'/> The distance from a new item to each prototype is "
            "summed over dimensions, each weighted by how much attention it gets. <bookmark mark='c'/> Similarity "
            "decays with distance at a rate c. <bookmark mark='d'/> And the choice follows Luce's rule from Part "
            "eleven: pick each category in proportion to its similarity. <bookmark mark='e'/> The model makes a "
            "strong prediction. Since everything is measured from two points, a category is easy only if a straight "
            "boundary can separate it from its rival. Keep that in mind."
        ) as vo:
            self.play(FadeIn(head))
            for m, e, r in zip("abcd", eqs, rows):
                vo.wait_until(m)
                self.play(Write(e), FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
