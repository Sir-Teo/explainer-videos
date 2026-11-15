from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403

SETS = (("a", MODEL), ("b", CAT_A), ("c", CAT_B))


class Numbers(VoiceoverScene):
    def construct(self):
        self.card()
        self.game()
        self.derive()
        self.results()
        self.coincidence()

    def card(self):
        card = chapter_card(10, r"Learning a concept from a few examples", r"How can three examples be enough?",
                            lit={1999: r"Tenenbaum", 2001: r"Tenenbaum \& Griffiths", 2007: r"Xu \& Tenenbaum"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter ten. Learning a concept from a few examples."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def game(self):
        head = heading(r"The number game")
        rule = label(r"a concept picks out some of the numbers 1 to 100", font_size=26, color=GREY_A).move_to([0, 2.3, 0])
        lines = VGroup()
        for k, (key, col) in enumerate(SETS):
            ex = {"a": "16", "b": "16, \\ 8, \\ 2, \\ 64", "c": "16, \\ 23, \\ 19, \\ 20"}[key]
            lines.add(VGroup(label(rf"these are in it: \ {ex}", font_size=30, color=col),
                             label(r"is 32? \ 17? \ 87?", font_size=26, color=GREY_B)).arrange(RIGHT, buff=0.8))
        lines.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([0, 0.3, 0])
        rows = rows_of([
            (r"one example leaves you unsure; \ four can make you nearly certain, \ and of very different things", WHITE),
            (r"prototypes and exemplars answer by similarity alone; \ here the answer is sometimes a rule, \ sometimes "
             r"a range", MODEL),
        ], 12.4, 23, 0.3).to_edge(DOWN, buff=0.65)
        with self.voiceover(
            "Play a game Joshua Tenenbaum invented. <bookmark mark='a'/> A concept picks out some of the numbers from "
            "1 to 100. I tell you sixteen is in it. Is thirty-two in it? Seventeen? Eighty-seven? You're not sure. "
            "<bookmark mark='b'/> Now I tell you sixteen, eight, two and sixty-four are in it. Thirty-two? Almost "
            "certainly. Seventeen? Almost certainly not. <bookmark mark='c'/> And if the examples are sixteen, "
            "twenty-three, nineteen and twenty? Then seventeen is very likely in, and thirty-two is probably out. "
            "<bookmark mark='d'/> One example leaves you unsure. Four can make you nearly certain, and of very "
            "different kinds of thing: a rule in one case, a range in the other. <bookmark mark='e'/> Similarity "
            "alone can't do that. Sixteen is the same distance from thirty-two in both games."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rule))
            for m, ln in zip("abc", lines):
                vo.wait_until(m)
                self.play(FadeIn(ln, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def derive(self):
        d = load("numbers")
        head = heading(r"Derivation: \ the size principle")
        eqs = VGroup(
            MathTex(r"p(h \mid X) \;\propto\; p(X \mid h)\, p(h)", font_size=40),
            MathTex(r"p(X \mid h) = \Big(\frac{1}{|h|}\Big)^{n} \ \text{ if every example is in } h, \text{ else } 0",
                    font_size=34, color=MODEL),
            MathTex(r"p(y \in C \mid X) = \sum_h p(h \mid X)\, [\, y \in h \,]", font_size=36, color=CAT_A),
        ).arrange(DOWN, buff=0.4).move_to([-3.2, 0.8, 0])
        eqs[1].scale(0.9)
        ratio = MathTex(r"\frac{p(X \mid \text{powers of 2})}{p(X \mid \text{even})} = \Big(\frac{50}{6}\Big)^4 "
                        r"\approx 4{,}800", font_size=34, color=PROTO).next_to(eqs, DOWN, buff=0.45)
        rows = rows_of([
            (rf"hypotheses: \ {d['n_math']} mathematical ones \ (even, \ squares, \ powers of 2, \ multiples of 7 \dots) "
             rf"\ and every range \emph{{a}} to \emph{{b}}", WHITE),
            (r"if the examples were drawn at random from the concept, \ a small concept makes them likelier: \ each "
             r"one has probability $1/|h|$", MODEL),
            (r"predict by averaging every hypothesis still standing, \ weighted by how believable it now is", CAT_A),
            (r"four examples that are all powers of 2 would be a wild coincidence if the concept were \emph{even}", PROTO),
        ], 4.9, 21, 0.3).move_to([4.4, 0.2, 0])
        ptag = psyche_tag(r"\texttt{concepts.number\_game\_hypotheses}, \ \texttt{number\_game}")
        with self.voiceover(
            "Tenenbaum's model is Bayesian inference, with one idea at its heart. <bookmark mark='a'/> The "
            f"hypotheses are the concepts the numbers could pick out: {d['n_math']} mathematical ones, like even, "
            "squares, powers of two and multiples of seven, and every range from a to b, with a prior that favours "
            "ranges of moderate size. <bookmark mark='b'/> Now the key step. Suppose the examples were drawn at "
            "random from the true concept. Then each one has probability one over the size of the concept. A small "
            "concept makes the same examples more likely, and with n examples, the advantage is raised to the power "
            "n. This is the size principle. <bookmark mark='c'/> To predict, average every hypothesis still "
            "standing, each weighted by how believable it now is. <bookmark mark='d'/> After sixteen, eight, two and "
            "sixty-four, powers of two has six members and even has fifty. The examples are about four thousand "
            "eight hundred times likelier under powers of two. Four powers of two would be a wild coincidence if the "
            "concept were merely even."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), Write(eqs[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Write(ratio), FadeIn(rows[3]))
        self.clear_scene()

    def results(self):
        d = load("numbers")
        head = heading(r"What the model generalizes to")
        strips = VGroup()
        for k, (key, col) in enumerate(SETS):
            A = axes([0, 101], [0, 1], x_length=10.2, y_length=1.25, xticks=[1, 16, 32, 50, 64, 100] if k == 2 else [],
                     yticks=[0, 1], yfmt=lambda v: f"{v:.0f}", center=[0.6, 1.55 - 1.85 * k, 0], font_size=15)
            g = d[key + "_gen"]
            bs = bars(A.ax, np.arange(1, 101), g, col, 0.75)
            ex = d[key + "_examples"]
            marks = VGroup(*[Triangle(color=WHITE, fill_opacity=1).scale(0.07).rotate(PI).next_to(
                A.ax.c2p(float(x), 1.0), UP, buff=0.03) for x in ex])
            top = d[key + "_top"][0]
            lab = VGroup(label(", ".join(str(int(x)) for x in ex), font_size=20, color=col),
                         label(rf"best: \ {top} \ ({100 * d[key + '_top_p'][0]:.0f}\%)", font_size=16,
                               color=GREY_A)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            lab.next_to(A, LEFT, buff=0.25)
            strips.add(VGroup(A, bs, marks, lab))
        for s in strips:
            keep_in_frame(s)
        note = label(r"bar height: \ the probability that each number is in the concept", font_size=18,
                     color=GREY_A).to_edge(DOWN, buff=0.35)
        ptag = psyche_tag(r"\texttt{concepts.number\_game}")
        # the narration names the winners; these checks keep it true to the computed posterior
        assert list(d["a_top"][:3]) == ["powers of 4", "powers of 2", "squares"] and round(100 * d["a_top_p"][0]) == 28
        assert d["b_top"][0] == "powers of 2"
        with self.voiceover(
            "Here is the model on the three games, with a bar for every number from one to a hundred. "
            "<bookmark mark='a'/> After sixteen alone, generalization is spread thin. The best single hypothesis is "
            "powers of four, with 28 percent of the belief, then powers of two and the squares, and nearby "
            "numbers get some weight from the ranges. <bookmark mark='b'/> After sixteen, eight, two and sixty-four, "
            "belief collapses onto powers of two: they light up, and almost nothing else does. "
            "<bookmark mark='c'/> After sixteen, twenty-three, nineteen and twenty, the mathematical hypotheses have "
            "nothing to offer, and the model generalizes to a range around the examples, fading at the edges, much "
            "like Shepard's gradient. <bookmark mark='d'/> Rules and similarity, two styles of thinking that "
            "psychologists had long treated as separate systems, come out of one inference. When Tenenbaum ran the "
            "game with people, their judgements showed the same pattern."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), FadeIn(note))
            for m, s in zip("abc", strips):
                vo.wait_until(m)
                self.play(FadeIn(s[0]), FadeIn(s[3]), FadeIn(s[2]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in s[1]],
                                                                               lag_ratio=0.01), run_time=2)
            vo.wait_until("d")
            self.play(Indicate(strips[1][3][0]), Indicate(strips[2][3][0]))
        self.clear_scene()

    def coincidence(self):
        head = heading(r"Suspicious coincidences")
        one = VGroup(*[word_chip(r"Dalmatian", CAT_A, 22)]).move_to([-4.6, 1.5, 0])
        three = VGroup(*[word_chip(r"Dalmatian", CAT_A, 22) for _ in range(3)]).arrange(RIGHT, buff=0.15)
        three.move_to([-3.6, -0.1, 0])
        l1 = label(r"\emph{this is a fep} \ $\Rightarrow$ \ feps are dogs", font_size=22, color=GREY_A).next_to(
            one, RIGHT, buff=0.4)
        l3 = label(r"$\Rightarrow$ \ feps are Dalmatians", font_size=22, color=GREY_A).next_to(three, DOWN, buff=0.25)
        rows = rows_of([
            (r"Xu \& Tenenbaum, \ 2007: \ shown one Dalmatian called a \emph{fep}, \ adults and preschoolers "
             r"extended the word to other dogs; \ shown three, \ mostly to Dalmatians only", WHITE),
            (r"three Dalmatians by chance would be a coincidence if \emph{fep} meant any dog: \ the size principle "
             r"again", MODEL),
            (r"Tenenbaum \& Griffiths, \ 2001: \ with ranges as hypotheses, \ the same inference gives Shepard's "
             r"exponential law", PROTO),
        ], 6.2, 21, 0.3).move_to([3.3, -0.4, 0])
        tag = published_tag(r"Xu \& Tenenbaum (2007); \ Tenenbaum \& Griffiths (2001)")
        with self.voiceover(
            "The size principle shows up in word learning. <bookmark mark='a'/> Fei Xu and Joshua Tenenbaum showed "
            "adults and preschool children a Dalmatian and called it a fep. Given one example, people extended "
            "fep to other dogs, the basic level. Given three Dalmatians, all called feps, they mostly kept the word "
            "to Dalmatians. <bookmark mark='b'/> Three Dalmatians in a row would be a suspicious coincidence if fep "
            "meant any dog. That's the size principle again, and a learner who ignored it would need many more "
            "examples. <bookmark mark='c'/> And it closes the loop with chapter six. Tenenbaum and Thomas Griffiths "
            "showed that if the hypotheses are regions of a space, the same inference gives Shepard's law of "
            "generalization. Shepard's consequential regions were Bayesian all along."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(one), FadeIn(l1), FadeIn(rows[0]))
            self.play(FadeIn(three), FadeIn(l3))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
