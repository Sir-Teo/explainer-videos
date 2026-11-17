from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Context(VoiceoverScene):
    def construct(self):
        self.card()
        self.drift()
        self.similarity()
        self.recency()
        self.contiguity()

    def card(self):
        card = chapter_card(7, r"A context that drifts", r"Can one slowly changing state explain recency and "
                            r"contiguity?", lit={1999: r"Howard \& Kahana", 2002: r"TCM", 2009: r"CMR"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter seven. A context that drifts."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def drift(self):
        head = heading(r"Derived: \ the drift of context")
        eq = MathTex(r"\mathbf{c}_i", r"=", r"\rho_i\, \mathbf{c}_{i-1}", r"+", r"\beta\, \mathbf{c}^{\text{IN}}_i",
                     font_size=48).move_to([0, 2.2, 0])
        eq[0].set_color(CTX)
        eq[4].set_color(WORD)
        norm = MathTex(r"\|\mathbf{c}_i\| = 1", r"\ \Rightarrow\ ", r"\rho_i = \sqrt{1 + \beta^2\left[(\mathbf{c}_{i-1}"
                       r"\cdot \mathbf{c}^{\text{IN}}_i)^2 - 1\right]} - \beta\, (\mathbf{c}_{i-1} \cdot "
                       r"\mathbf{c}^{\text{IN}}_i)", font_size=32).next_to(eq, DOWN, buff=0.4)
        orth = MathTex(r"\mathbf{c}_{i-1} \perp \mathbf{c}^{\text{IN}}_i", r"\ \Rightarrow\ ",
                       r"\rho = \sqrt{1 - \beta^2}", font_size=36, color=MODEL).next_to(norm, DOWN, buff=0.35)
        # a 2-D picture of one step: the old context, the new input, the new context on the unit circle
        o = np.array([-4.2, -2.0, 0])
        r = 1.25
        b = 0.55
        ang_old = np.deg2rad(70)
        c_old = np.array([np.cos(ang_old), np.sin(ang_old), 0])
        c_in = np.array([np.cos(ang_old - PI / 2), np.sin(ang_old - PI / 2), 0])
        c_new = np.sqrt(1 - b ** 2) * c_old + b * c_in
        circ = Arc(radius=r, start_angle=-PI / 6, angle=PI * 0.9, color=GREY_C, stroke_width=2).move_arc_center_to(o)
        va = Arrow(o, o + r * c_old, buff=0, color=CTX, stroke_width=4)
        vi = Arrow(o, o + r * c_in, buff=0, color=WORD, stroke_width=4)
        vn = Arrow(o, o + r * c_new, buff=0, color=MODEL, stroke_width=5)
        la = MathTex(r"\mathbf{c}_{i-1}", font_size=26, color=CTX).next_to(va.get_end(), UP, buff=0.08)
        li = MathTex(r"\mathbf{c}^{\text{IN}}_i", font_size=26, color=WORD).next_to(vi.get_end(), RIGHT, buff=0.08)
        ln = MathTex(r"\mathbf{c}_i", font_size=26, color=MODEL).next_to(vn.get_end(), RIGHT, buff=0.08)
        rows = rows_of([
            (r"context: \ a unit vector, \ the slowly changing state of mind", CTX),
            (r"each word brings its own input $\mathbf{c}^{\text{IN}}_i$, \ and context moves a step $\beta$ toward "
             r"it", WORD),
            (r"$\rho$ is whatever keeps the length one: \ the old context shrinks as the new part grows", MODEL),
            (r"Howard and Kahana's temporal context model, \ 2002; \ CMR adds learning and a stopping rule, \ 2009",
             GREY_A),
        ], 6.8, 22, 0.28).move_to([2.9, -2.0, 0])
        tag = historical_tag(r"Howard \& Kahana (2002); \ Polyn, \ Norman \& Kahana (2009)")
        with self.voiceover(
            "Here is the idea that replaced the buffer. Suppose that at every moment there is a state of mind, a "
            "context, which changes slowly. Represent it as a vector of unit length. <bookmark mark='a'/> When a word "
            "arrives, it brings an input of its own, and the context takes a step of size beta toward that input. "
            "<bookmark mark='b'/> To keep the vector at length one, the old context has to shrink by a factor rho, "
            "and requiring the length to be one gives rho exactly. <bookmark mark='c'/> For unrelated words, each "
            "input is orthogonal to the context before it, and rho is simply the square root of one minus beta "
            "squared. Each step, a fixed share of the old context fades, and the newest word's contribution is "
            "added. <bookmark mark='d'/> Marc Howard and Michael Kahana called this the temporal context model in "
            "2002. Sean Polyn, Kenneth Norman and Kahana extended it, in 2009, into the context maintenance and "
            "retrieval model, CMR, which is the version Psyche runs."
        ) as vo:
            self.play(FadeIn(head), Write(eq), FadeIn(tag))
            self.play(Create(circ), GrowArrow(va), FadeIn(la), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(GrowArrow(vi), FadeIn(li), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(GrowArrow(vn), FadeIn(ln), Write(norm), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Write(orth))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def similarity(self):
        dr = load("drift")
        head = heading(r"Unrolled: \ nearby moments have similar contexts")
        eq = MathTex(r"\mathbf{c}_i = \beta \sum_{k \le i} \rho^{\,i-k}\, \mathbf{c}^{\text{IN}}_k", r"\qquad",
                     r"\mathbf{c}_i \cdot \mathbf{c}_j \approx \rho^{\,|i-j|}", font_size=40).move_to([0, 2.2, 0])
        eq[2].set_color(MODEL)
        S = dr["sim"]
        n = S.shape[0]
        size = 0.24
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                v = float(np.clip(S[i, j], 0, 1))
                grid.add(Square(side_length=size, stroke_width=0, fill_color=interpolate_color(
                    ManimColor("#14202c"), ManimColor(CTX), v), fill_opacity=1).move_to([j * size, -i * size, 0]))
        grid.center().move_to([-3.6, -0.75, 0])
        gl = label(r"context at study of word $i$ \ $\cdot$ \ of word $j$", font_size=19, color=GREY_A)
        gl.next_to(grid, DOWN, buff=0.2)
        A = axes([-6, 6], [0, 1], x_length=5.4, y_length=2.8, xticks=[-6, -3, 0, 3, 6], yticks=[0, 0.5, 1],
                 xlabel=r"lag $j - i$", ylabel=r"context similarity", center=[3.3, -0.55, 0], font_size=18,
                 xfmt=lambda v: f"{v:+.0f}" if v else "0", yfmt=lambda v: f"{v:.1f}")
        ax = A.ax
        cv = curve_in(ax, dr["lags"], dr["mean"], MODEL, 4)
        pts = scatter(ax, dr["lags"], dr["mean"], MODEL, radius=0.06, opacity=1.0)
        ptag = psyche_tag(r"\texttt{memory.cmr}: \ the fitted model's contexts, \ a 16-word list")
        with self.voiceover(
            "Unroll the recursion. <bookmark mark='a'/> The context at word i is a weighted sum of every input so "
            "far, each one shrunk by a factor rho for every step since it arrived. <bookmark mark='b'/> So the "
            "contexts of two words are similar in proportion to rho raised to the number of steps between them. "
            "<bookmark mark='c'/> Here is that similarity for every pair of words in a sixteen-word list, in the "
            "model fitted in the next chapter. Words near each other in time have similar contexts; words far "
            "apart, different ones. <bookmark mark='d'/> Averaged by lag, the similarity falls off on both sides, "
            "geometrically. Nothing about the words themselves is shared. Neighbours are similar only because they "
            "were experienced in nearly the same state of mind."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq[0]))
            vo.wait_until("b")
            self.play(Write(eq[2]))
            vo.wait_until("c")
            self.play(FadeIn(grid), FadeIn(gl), FadeIn(ptag), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(A), Create(cv), FadeIn(pts))
        self.clear_scene()

    def recency(self):
        head = heading(r"Recency, \ without a buffer")
        eq1 = MathTex(r"M^{CF} \mathrel{+}= \mathbf{f}_i\, \mathbf{c}_i^{\top}", font_size=40, color=WORD)
        eq2 = MathTex(r"a_i = \mathbf{c}_{\text{test}} \cdot \mathbf{c}_i \approx \rho^{\,n-i}", font_size=40,
                      color=MODEL)
        eq3 = MathTex(r"P(\text{recall } i) = \frac{a_i^{1/\tau}}{\sum_k a_k^{1/\tau}}", font_size=40, color=CUE)
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.35).move_to([-3.4, 0.4, 0])
        rows = rows_of([
            (r"at study, \ each word is bound to the context it was studied in", WORD),
            (r"at test, \ the current context is the cue: \ it is most like the last words' contexts", MODEL),
            (r"the words compete by a choice rule: \ the last word wins most often, \ and recall starts there", CUE),
            (r"a delay before recall moves the context away from \emph{all} the words, \ and recency fades", LOST),
            (r"distraction after every word spreads them all out by the same factor: \ for a choice rule only ratios "
             r"count, \ so the last word can stand out again", CTX),
            (r"the argument for the ratio rule; \ whether a fitted model obeys it is the next chapter's test", MODEL),
        ], 6.6, 22, 0.28).move_to([3.3, -0.3, 0])
        with self.voiceover(
            "Now bind each word to its context. <bookmark mark='a'/> At study, an association matrix from context to "
            "words learns the outer product of the word and the context it was studied in. "
            "<bookmark mark='b'/> At test, the context at that moment is the cue. Its match to word i is the "
            "similarity of the two contexts, which falls as rho to the power of the steps since word i. "
            "<bookmark mark='c'/> The words compete through a choice rule, as in Part 19's SIMPLE model, and the last "
            "word, whose context is closest to now, wins most often. Recency, and the tendency to start at the end, "
            "with no short-term store at all. <bookmark mark='d'/> Add thirty seconds of counting before recall, and "
            "the context drifts away from all of the words, so the last one loses its special advantage over the "
            "others and over the other cues. Recency fades, as Glanzer and Cunitz found. <bookmark mark='e'/> But "
            "fill the gaps after every word with arithmetic, and the words are spread apart by the same kind of "
            "drift that pushes the last one back. The choice rule only cares about ratios, so the last word can "
            "stand out from its neighbours again, as Bjork and Whitten found. <bookmark mark='f'/> That's the "
            "argument for the ratio rule, on any time scale. An argument isn't yet a model, though: in the next "
            "chapter we fit one, and test it on exactly these two experiments."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eq2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(eq3), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def contiguity(self):
        r = load("reinstate")
        head = heading(r"Contiguity, \ and why it leans forward")
        eq = MathTex(r"\mathbf{c}^{\text{IN}} = M^{FC}\mathbf{f}_j", r"=", r"(1 - \gamma)\,\mathbf{c}^{\text{pre}}_j",
                     r"+", r"\gamma\, \mathbf{c}_{j-1}", font_size=40).move_to([0, 2.25, 0])
        eq[2].set_color(WORD)
        eq[4].set_color(CTX)
        A = axes([-7, 7], [0, 1.05], x_length=6.6, y_length=3.3, xticks=[-6, -4, -2, 0, 2, 4, 6],
                 yticks=[0, 0.5, 1], xlabel=r"lag from the word just recalled", ylabel=r"support from the "
                 r"retrieved context", center=[-2.7, -0.75, 0], font_size=18,
                 xfmt=lambda v: f"{v:+.0f}" if v else "0", yfmt=lambda v: f"{v:.1f}")
        ax = A.ax
        lags = r["lags"]
        pre = crp_curves(ax, lags, r["pre"], WORD, dots=False)
        epi = crp_curves(ax, lags, r["episodic"], CTX, dots=False)
        fit = crp_curves(ax, lags, r["fitted"], MODEL, dots=True)
        key = legend([(WORD, r"the word's own features only"), (CTX, r"its study context only"),
                      (MODEL, r"the fitted mixture")], font_size=18).move_to([4.2, 0.85, 0])
        rows = rows_of([
            (r"recalling a word brings back context: \ its own features, \ and the context it was studied in", WHITE),
            (r"its features entered the context \emph{after} it, \ and lingered: \ they match the words that "
             r"followed", WORD),
            (r"its study context is the moment just before it: \ it matches both sides, \ leaning back", CTX),
            (r"together: \ contiguity that leans forward, \ as in every person's data", MODEL),
        ], 5.4, 21, 0.28).move_to([4.2, -1.5, 0])
        with self.voiceover(
            "And now the order of recall. <bookmark mark='a'/> When a word is recalled, the model retrieves context "
            "with it, through a second set of associations, from words to context. What comes back is a mixture: a "
            "share of the word's own features, and a share gamma of the context the word was studied in. "
            "<bookmark mark='b'/> The word's features entered the context just after the word was studied, and "
            "lingered, shrinking by rho each step. So they match the words that followed it, and not the words "
            "before. On their own they make the next recall jump forward. <bookmark mark='c'/> The retrieved study "
            "context is the state of mind just before the word arrived. It matches the words on both sides, and if "
            "anything leans backward, toward the word before. "
            "<bookmark mark='d'/> The mixture gives contiguity that leans forward, which is what the data show. "
            "Recency, the start at the end, contiguity and its asymmetry: all from one slowly drifting state of "
            "mind. Whether it also survives distraction is the next chapter's test."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(Create(pre), FadeIn(key[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(epi), FadeIn(key[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(fit), FadeIn(key[2]), FadeIn(rows[3]))
        self.clear_scene()
