from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Ratings(VoiceoverScene):
    def construct(self):
        self.card()
        self.graded()
        self.science()

    def card(self):
        card = chapter_card(8, r"Rating scales", r"What if the answer is not right or wrong?",
                            lit={1969: r"Samejima", 1982: r"Masters"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter eight. Rating scales."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def graded(self):
        d = load("grm")
        head = heading(r"Samejima's graded responses")
        eq = MathTex(r"P(X \ge k \mid \theta) = \frac{1}{1 + e^{-a(\theta - b_k)}}, \quad "
                     r"P(X = k) = P(X \ge k) - P(X \ge k + 1)", font_size=32, color=MODEL).move_to([0, 2.2, 0])
        j = 2
        A = axes([-4, 4], [0, 1], x_length=5.6, y_length=3.0, xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"attitude $\theta$",
                 ylabel=r"P(category)", center=[-3.4, -0.6, 0], font_size=13)
        cols = (AUTH, PERSON, SYMP, GOOD)
        cs = VGroup(*[curve(A.ax, d["th"], d["curves"][j][:, m], c) for m, c in enumerate(cols)])
        key = VGroup(*[label(t, font_size=13, color=c) for t, c in zip(d["levels"], cols)]).arrange(RIGHT, buff=0.3)
        key.next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"each threshold $b_k$ is where a person becomes likelier than not to answer at least category $k$", WHITE),
            (rf"the item ``{d['names'][j]}'' (``thanks to science and technology, \ there will be more opportunities for the future generations''): \ "
             rf"thresholds {d['B'][j][0]:.1f}, \ {d['B'][j][1]:.1f} and {d['B'][j][2]:.1f}", MODEL),
            (r"each category has its own curve, \ and its own stretch of the attitude axis", PERSON),
            (r"Masters's partial credit model is the Rasch version, \ with adjacent categories", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.5, 0])
        tag = psyche_tag(r"\texttt{irt.fit\_grm}; \ Eurobarometer 1992, \ British sample (ltm)")
        with self.voiceover(
            "Questionnaires rarely have right answers. They have categories, from strongly disagree to strongly "
            "agree. <bookmark mark='a'/> Fumiko Samejima's graded response model gives each step a threshold: the "
            "attitude at which a person becomes likelier than not to answer at least that category. "
            "<bookmark mark='b'/> Here's an item from a European survey of 1992: thanks to science and technology, "
            "there will be more opportunities for the future generations. <bookmark mark='c'/> Each category has its own curve, and its own stretch of "
            "the attitude axis. <bookmark mark='d'/> Geoff Masters's partial credit model is the Rasch version."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[Create(c) for c in cs], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def science(self):
        d = load("grm")
        head = heading(r"Four items, \ four discriminations")
        A = axes([0.3, 4.7], [0, 2.6], x_length=5.0, y_length=3.0, xticks=None, yticks=[0, 1, 2],
                 yfmt=lambda v: f"{v:g}", ylabel=r"discrimination $a$", center=[-3.4, 0.3, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3, 4], d["a"], [SYMP, PERSON, GOOD, MODEL], width=0.6)
        names = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, t in enumerate(d["names"])])
        k = int(np.argmax(d["a"]))
        rows = rows_of([
            (rf"{num(d['n'])} people, \ four positively worded items, \ four categories each", WHITE),
            (rf"``{d['names'][k]}'' discriminates most (a = {d['a'][k]:.1f}): \ it sorts people by their attitude "
             rf"most sharply", GOOD),
            (r"the other items' first thresholds are far below the people: \ almost no one strongly disagrees, \ so "
             r"those categories carry little information", PERSON),
            (r"Part 46 asks what happens between the question and the answer, \ and whether the categories are used "
             r"the same way by everyone", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.fit\_grm}; \ matches ltm's fit")
        with self.voiceover(
            "Fit all four positively worded items. <bookmark mark='a'/> Three hundred and ninety-two people, four "
            "categories each. <bookmark mark='b'/> The item about the future discriminates most: it sorts people by "
            "their attitude most sharply. <bookmark mark='c'/> And the first thresholds sit far below the people. "
            "Almost no one strongly disagrees, so those categories carry little information. <bookmark mark='d'/> "
            "Part 46 asks what happens between the question and the answer, and whether everyone uses the categories "
            "the same way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
