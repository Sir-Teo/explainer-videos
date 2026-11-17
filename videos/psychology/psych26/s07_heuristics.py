from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


def icon_grid(n_rows: int, n_cols: int, colors, size: float = 0.3, buff: float = 0.06) -> VGroup:
    """A grid of small rounded squares, coloured in reading order."""
    out = VGroup()
    for k, col in enumerate(colors):
        r, c = divmod(k, n_cols)
        out.add(RoundedRectangle(corner_radius=0.04, width=size, height=size, stroke_width=0, fill_color=col,
                                 fill_opacity=1).move_to([c * (size + buff), -r * (size + buff), 0]))
    return out


class Heuristics(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.anchoring()
        self.linda()
        self.cabs()

    def card(self):
        card = chapter_card(6, r"Heuristics and biases", r"How do people judge what they cannot compute?",
                            lit={1973: r"Tversky \& Kahneman", 1974: r"Tversky \& Kahneman",
                                 1983: r"Tversky \& Kahneman"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter six. Heuristics and biases."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three(self):
        head = heading(r"Three rules of thumb, \ 1974")
        boxes = VGroup()
        for name, txt, ex, col in [
            (r"availability", r"judge how common something is by how easily examples come to mind",
             r"words starting with K, \ or with K third? \ most say first; \ third is more common", HEUR),
            (r"representativeness", r"judge how likely by how much it resembles the type",
             r"a shy, \ tidy man: \ librarian or farmer? \ there are far more farmers", RISKY),
            (r"anchoring and adjustment", r"start from a number at hand and adjust, \ too little",
             r"a number from a wheel of fortune moves an estimate of a fact", SURE),
        ]:
            box = RoundedRectangle(corner_radius=0.12, width=4.1, height=3.6, stroke_color=col, stroke_width=2,
                                   fill_color=BLACK, fill_opacity=0.5)
            body = VGroup(label(name, font_size=25, color=col), wrapped_label(txt, 3.6, 21, WHITE),
                          wrapped_label(ex, 3.6, 19, GREY_A)).arrange(DOWN, buff=0.3).move_to(box)
            boxes.add(VGroup(box, body))
        boxes.arrange(RIGHT, buff=0.3).move_to([0, 0.1, 0])
        foot = wrapped_label(r"usually good, \ sometimes systematically wrong: \ the errors are the clues to the rule, "
                             r"\ as visual illusions are to vision \ (Part 14)", 12.0, 24, MODEL).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Tversky \& Kahneman (1973, \ 1974)")
        with self.voiceover(
            "Prospect theory is about choosing once the chances are known. A second programme, begun earlier, asked "
            "how people judge chances in the first place. In 1974 Tversky and Kahneman published three rules of "
            "thumb in Science. <bookmark mark='a'/> Availability: judging how common something is by how easily "
            "examples come to mind. Are there more English words that start with K, or that have K as the third "
            "letter? Most people say first, because words are easier to recall by their first letter; in fact K "
            "is more common third. <bookmark mark='b'/> Representativeness: judging how likely something is by how "
            "much it resembles a type. A shy, tidy man with a passion for detail sounds like a librarian, but there "
            "are many more farmers than librarians. <bookmark mark='c'/> And anchoring: starting from a number that "
            "happens to be at hand, and adjusting too little. <bookmark mark='d'/> Each rule usually works. Its "
            "errors are systematic, and that's what makes them useful: like the visual illusions of Part 14, they "
            "reveal the rule."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, b in zip("abc", boxes):
                vo.wait_until(m)
                self.play(FadeIn(b, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def anchoring(self):
        head = heading(r"Anchoring: \ a wheel of fortune")
        def wheel(n, col, center):
            c = Circle(radius=1.0, color=col, stroke_width=3).move_to(center)
            spokes = VGroup(*[Line(center, center + 1.0 * np.array([np.cos(a), np.sin(a), 0]), color=GREY_D,
                                   stroke_width=1.5) for a in np.linspace(0, 2 * np.pi, 13)[:-1]])
            ptr = Triangle(color=col, fill_opacity=1).scale(0.12).rotate(PI).next_to(c, UP, buff=0.02)
            t = label(rf"{n}", font_size=40, color=col).move_to(center)
            return VGroup(spokes, c, ptr, t)
        w1 = wheel(10, SURE, np.array([-4.6, 1.2, 0]))
        w2 = wheel(65, RISKY, np.array([-4.6, -1.6, 0]))
        A = axes([0, 60], [-0.5, 1.5], x_length=4.6, y_length=2.6, xticks=[0, 20, 40, 60], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"median estimate: \ \% of UN members that are African",
                 center=[-0.4, -0.2, 0], font_size=16)
        b1 = Rectangle(width=abs(A.ax.c2p(25, 0)[0] - A.ax.c2p(0, 0)[0]), height=0.55, fill_color=SURE,
                       fill_opacity=0.9, stroke_width=0)
        b1.move_to(A.ax.c2p(0, 1.0), aligned_edge=LEFT)
        b2 = Rectangle(width=abs(A.ax.c2p(45, 0)[0] - A.ax.c2p(0, 0)[0]), height=0.55, fill_color=RISKY,
                       fill_opacity=0.9, stroke_width=0)
        b2.move_to(A.ax.c2p(0, 0.0), aligned_edge=LEFT)
        l1 = label(r"25", font_size=22, color=SURE).next_to(b1, RIGHT, buff=0.1)
        l2 = label(r"45", font_size=22, color=RISKY).next_to(b2, RIGHT, buff=0.1)
        rows = rows_of([
            (r"a wheel rigged to stop at 10 or 65; \ is the percentage higher or lower? \ then: \ what is it?",
             WHITE),
            (r"a number known to be random moved the answer by 20 points", HEUR),
            (r"later: \ anchors move prices, \ damages awarded by juries, \ and experts' estimates; \ and Many Labs "
             r"found the effect again in 36 samples", MODEL),
        ], 4.4, 21, 0.3).move_to([4.3, 0.0, 0])
        tag = published_tag(r"Tversky \& Kahneman (1974); \ Klein et al.\ (2014)")
        with self.voiceover(
            "The anchoring experiment is the strangest of the three. <bookmark mark='a'/> A wheel of fortune, "
            "marked from nought to a hundred, but rigged to stop at ten or at sixty-five. After it stopped, people "
            "were asked whether the percentage of African countries in the United Nations was higher or lower than "
            "that number, and then for their estimate. <bookmark mark='b'/> Those who saw ten gave a median "
            "estimate of twenty-five percent; those who saw sixty-five, forty-five. A number everyone knew to be "
            "random moved the answer by twenty points. <bookmark mark='c'/> Anchors have since been shown to move "
            "prices, damages awarded by juries, and the estimates of experts, and the effect turned up again, large, "
            "when the Many Labs project ran anchoring problems in thirty-six samples in 2014."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(w1), FadeIn(w2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), GrowFromEdge(b1, LEFT), GrowFromEdge(b2, LEFT), FadeIn(l1), FadeIn(l2),
                      FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def linda(self):
        head = heading(r"Linda, \ and the conjunction rule")
        desc = wrapped_label(r"Linda is 31, \ single, \ outspoken and very bright. \ She majored in philosophy. \ As a "
                             r"student she was deeply concerned with discrimination and social justice, \ and took "
                             r"part in anti-nuclear demonstrations.", 6.0, 22, WHITE).move_to([-3.4, 1.4, 0])
        q = VGroup(label(r"Which is more probable?", font_size=23, color=GREY_A),
                   label(r"Linda is a bank teller.", font_size=23, color=SURE),
                   label(r"Linda is a bank teller and is active in the", font_size=23, color=RISKY),
                   label(r"feminist movement.", font_size=23, color=RISKY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.12)
        q.next_to(desc, DOWN, buff=0.4, aligned_edge=LEFT)
        big = Ellipse(width=4.2, height=2.8, color=SURE, fill_opacity=0.15).move_to([3.0, 1.0, 0])
        fem = Ellipse(width=3.2, height=2.2, color=GAIN, fill_opacity=0.12).move_to([4.6, 1.0, 0])
        lb = label(r"bank tellers", font_size=21, color=SURE).next_to(big, UP, buff=0.08).shift(LEFT * 0.6)
        lf = label(r"feminists", font_size=21, color=GAIN).next_to(fem, UP, buff=0.08).shift(RIGHT * 0.6)
        both = label(r"both", font_size=20, color=RISKY).move_to([4.1, 1.0, 0])
        rule = MathTex(r"P(A \wedge B) \le P(A)", font_size=40, color=NORM).move_to([3.6, -1.0, 0])
        rows = rows_of([
            (r"85\% of 142 students chose the conjunction", RISKY),
            (r"the description resembles a feminist, \ not a bank teller: \ representativeness", HEUR),
        ], 6.0, 22, 0.25).move_to([3.4, -2.3, 0])
        tag = published_tag(r"Tversky \& Kahneman (1983)")
        with self.voiceover(
            "Representativeness has its most famous demonstration in Linda. <bookmark mark='a'/> Linda is thirty-one, "
            "single, outspoken and very bright. She majored in philosophy, and as a student was deeply concerned "
            "with discrimination and social justice. Which is more probable: that Linda is a bank teller, or that "
            "she is a bank teller and active in the feminist movement? <bookmark mark='b'/> However well the second "
            "fits, it can't be more probable. Feminist bank tellers are a subset of bank tellers, so the chance of "
            "both is never more than the chance of one. <bookmark mark='c'/> In Tversky and Kahneman's 1983 paper, "
            "eighty-five percent of a hundred and forty-two students chose the conjunction. <bookmark mark='d'/> The "
            "description resembles a feminist much more than a bank teller, and resemblance stood in for "
            "probability."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(desc))
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(big), FadeIn(lb), FadeIn(fem), FadeIn(lf), FadeIn(both))
            self.play(Write(rule))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def cabs(self):
        d = load("bayes")
        nf = d["cab_nf"]
        head = heading(r"Base rates: \ the cab problem")
        prob = rows_of([
            (r"a cab was in a hit-and-run at night; \ 85\% of the city's cabs are Green, \ 15\% Blue", WHITE),
            (r"a witness says Blue; \ tested in the same light, \ witnesses are right 80\% of the time", WHITE),
            (r"what is the chance the cab was Blue?", RISKY),
        ], 6.2, 22, 0.25).move_to([-3.3, 1.7, 0])
        colors = []
        tp, fn = nf["true_pos"], nf["sick"] - nf["true_pos"]
        fp = nf["false_pos"]
        tn = nf["well"] - fp
        colors = [SURE] * tp + [GREY_D] * fn + [GAIN] * fp + [GREY_E] * tn
        grid = icon_grid(5, 20, colors, size=0.27, buff=0.06).move_to([3.4, 1.6, 0])
        key = VGroup(label(rf"{tp} Blue, \ called Blue", font_size=19, color=SURE),
                     label(rf"{fp} Green, \ called Blue", font_size=19, color=GAIN),
                     label(r"the rest, \ called Green", font_size=19, color=GREY_B)).arrange(RIGHT, buff=0.35)
        key.next_to(grid, DOWN, buff=0.2)
        eq = MathTex(rf"P(\text{{Blue}} \mid \text{{says Blue}}) = \frac{{{tp}}}{{{tp} + {fp}}} = {d['cab']:.2f}",
                     font_size=38, color=NORM).move_to([0, -1.0, 0])
        rows = rows_of([
            (rf"the median answer was {d['cab_median_answer']:.2f}: \ the witness's accuracy, \ with the base rate "
             r"ignored", HEUR),
            (r"tell people instead that 85\% of \emph{accidents} involve Green cabs, \ a causal base rate, \ and "
             r"they use it", MODEL),
        ], 12.0, 23, 0.25).to_edge(DOWN, buff=0.7)
        tag = psyche_tag(r"\texttt{choice.bayes}, \ \texttt{natural\_frequencies}; \ Tversky \& Kahneman (1982)")
        with self.voiceover(
            "The last bias of this chapter is the neglect of base rates. <bookmark mark='a'/> A cab was involved in "
            "a hit-and-run at night. Eighty-five percent of the city's cabs are Green and fifteen percent are Blue. "
            "A witness says the cab was Blue, and tested in the same conditions, witnesses are right eighty percent "
            "of the time. What's the chance it was Blue? <bookmark mark='b'/> Picture a hundred cabs: fifteen Blue "
            f"and eighty-five Green. The witness calls {tp} of the Blue ones Blue, and also {fp} of the Green ones. "
            f"<bookmark mark='c'/> So of the {tp + fp} cabs called Blue, only {tp} are: a chance of "
            f"{d['cab']:.2f}. <bookmark mark='d'/> The median answer Tversky and Kahneman received was "
            f"{d['cab_median_answer']:.2f}, the witness's accuracy, as if the base rate didn't exist. "
            "<bookmark mark='e'/> Rephrase it so that eighty-five percent of accidents involve Green cabs, a base "
            "rate with a causal story, and people use it far more. How the information is given turns out to "
            "matter a great deal, which is where the critics come in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(prob))
            vo.wait_until("b")
            self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(key), run_time=2)
            vo.wait_until("c")
            self.play(Write(eq))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()
