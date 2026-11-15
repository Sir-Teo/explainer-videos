from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403

TR = ("A", "C", "E", "N", "O")


class Sexes(VoiceoverScene):
    def construct(self):
        self.card()
        self.similar()
        self.sapa()
        self.many()
        self.dispute()

    def card(self):
        card = chapter_card(11, r"Women and men", r"One dimension at a time, \ or all at once?",
                            lit={2005: r"Hyde", 2008: r"Schmitt et al.", 2012: r"Del Giudice et al."}, part=PART,
                            scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter eleven. Women and men."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def similar(self):
        head = heading(r"Mostly similar")
        A = axes([0, 100], [0, 1], x_length=7.0, y_length=0.9, xticks=[0, 25, 50, 75, 100], yticks=None,
                 xfmt=lambda v: f"{v:.0f}\\%", center=[0, 1.6, 0], font_size=14)
        seg = VGroup()
        x0 = 0
        for share, c, t in ((30, GOOD, r"close to zero"), (48, A_, r"small"), (22, GREY_B, r"larger")):
            r = Rectangle(width=A.ax.c2p(x0 + share, 0)[0] - A.ax.c2p(x0, 0)[0], height=0.5, stroke_width=0,
                          fill_color=c, fill_opacity=0.8).move_to(A.ax.c2p(x0, 0.5), aligned_edge=LEFT)
            seg.add(VGroup(r, label(t, font_size=16, color=c).next_to(r, UP, buff=0.08)))
            x0 += share
        rows = rows_of([
            (r"Janet Hyde, \ 2005: \ 46 meta-analyses of psychological differences between the sexes", WHITE),
            (r"30\% of the effects were close to zero and 48\% small: \ the gender similarities hypothesis", GOOD),
            (r"the exceptions included throwing distance, \ some aspects of sexuality, \ and physical aggression", GREY_A),
            (r"Paul Costa, \ Antonio Terracciano and Robert McCrae, \ 2001: \ 26 cultures, \ 23{,}031 people: \ women "
             r"score higher on neuroticism and agreeableness, \ with differences small beside the variation within "
             r"each sex", A_),
            (r"David Schmitt and colleagues, \ 2008: \ 55 nations: \ the differences are larger in more prosperous, \ "
             r"healthier and more egalitarian nations, \ mostly because of men's scores", YOU),
        ], 12.4, 20, 0.28).move_to([0, -1.3, 0])
        tag = published_tag(r"Hyde (2005); \ Costa et al.\ (2001); \ Schmitt et al.\ (2008)")
        with self.voiceover(
            "Now a question with a long and loud history. <bookmark mark='a'/> In 2005 Janet Hyde reviewed forty-six "
            "meta-analyses of psychological differences between the sexes. <bookmark mark='b'/> Thirty percent of the "
            "effects were close to zero, and forty-eight percent small. She called it the gender similarities "
            "hypothesis. <bookmark mark='c'/> The exceptions included throwing distance, some aspects of sexuality, "
            "and physical aggression. <bookmark mark='d'/> In personality, Paul Costa, Antonio Terracciano and Robert "
            "McCrae compared twenty-six cultures and twenty-three thousand people in 2001. Women scored higher on "
            "neuroticism and agreeableness, with differences small beside the variation within each sex. "
            "<bookmark mark='e'/> And in 2008 David Schmitt and colleagues found something surprising in fifty-five "
            "nations: the differences were larger in more prosperous, healthier and more egalitarian nations, mostly "
            "because of men's scores."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.1) for s_ in seg], lag_ratio=0.3), FadeIn(rows[1]))
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def sapa(self):
        d = load("sexes")
        head = heading(r"In the SAPA sample")
        A = axes([-0.6, 4.6], [-0.3, 0.6], x_length=6.0, y_length=3.8, xticks=None, yticks=[-0.2, 0, 0.2, 0.4, 0.6],
                 yfmt=lambda v: f"{v:g}", ylabel=r"women minus men, \ $d$", center=[-2.9, -0.4, 0], font_size=15)
        b = bars(A.ax, np.arange(5), d["d5"], [TRAIT_COL[t] for t in TR], width=0.6)
        names = VGroup(*[label(t, font_size=20, color=TRAIT_COL[t]).next_to(A.ax.c2p(i, -0.3), DOWN, buff=0.15)
                         for i, t in enumerate(TR)])
        vals = VGroup(*[label(f"{v:+.2f}", font_size=15, color=TRAIT_COL[t])
                        .next_to(A.ax.c2p(i, float(v)), UP if v > 0 else DOWN, buff=0.08)
                        for i, (t, v) in enumerate(zip(TR, d["d5"]))])
        rows = rows_of([
            (rf"{num(d['n'][0])} men and {num(d['n'][1])} women in the SAPA data", WHITE),
            (rf"women score higher on agreeableness, \ {d['d5'][0]:.2f} of a standard deviation, \ and on "
             rf"neuroticism, \ {d['d5'][3]:.2f}; \ slightly lower on openness, \ as these items measure it", A_),
            (r"every one of these is in Hyde's small range, \ or below it", GOOD),
        ], 5.6, 21, 0.38).move_to([3.6, -0.3, 0])
        tag = published_tag(r"data: \ Revelle et al.\ (SAPA, \ 2010), \ recomputed")
        with self.voiceover(
            f"Here it is in the SAPA data. <bookmark mark='a'/> {d['n'][0]:,} men and {d['n'][1]:,} women. "
            "<bookmark mark='b'/> Women score higher on agreeableness, by "
            f"{d['d5'][0]:.2f} of a standard deviation, and on neuroticism, by {d['d5'][3]:.2f}, and slightly lower on "
            "openness, as these items measure it. <bookmark mark='c'/> Every one of these differences is in Hyde's "
            "small range, or below it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in b], lag_ratio=0.2), FadeIn(vals), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def many(self):
        d = load("sexes")
        head = heading(r"All the dimensions at once")
        A = axes([0, 26], [0, 1.0], x_length=6.0, y_length=3.8, xticks=[1, 5, 10, 15, 20, 25],
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"items used", ylabel=r"distance between the sexes", center=[-2.9, -0.4, 0], font_size=15)
        Dl = VGroup(curve(A.ax, d["k"], d["D_k"], LOST, stroke_width=4), scatter(A.ax, d["k"], d["D_k"], LOST,
                                                                                    radius=0.06))
        dl = curve(A.ax, d["k"], d["absd_k"], GREY_B, stroke_width=3)
        key = legend([(LOST, r"Mahalanobis $D$, \ all items at once"), (GREY_B, r"average single-item $|d|$")],
                     font_size=16).move_to(A.ax.c2p(12, 0.95))
        rows = rows_of([
            (r"Mahalanobis's $D$: \ the distance between two groups' averages in many dimensions at once, \ measured "
             r"against the spread and the correlations within groups", MODEL),
            (rf"the average item differs by only {np.mean(d['absd_k']):.2f}, \ but $D$ grows as items are added: "
             rf"\ {d['D5']:.2f} on the five scales, \ {d['D25']:.2f} on all 25 items", LOST),
            (rf"overlap of the two distributions: \ {pct(d['ovl5'])} on five scales, \ {pct(d['ovl25'])} on 25 items",
             YOU),
        ], 5.6, 21, 0.38).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{personality.mahalanobis, \ d\_by\_dimensions}")
        with self.voiceover(
            "But that's one dimension at a time. <bookmark mark='a'/> Mahalanobis's D measures the distance between "
            "two groups in many dimensions at once, against the spread and the correlations within each group. "
            "<bookmark mark='b'/> The average single item differs between the sexes by only "
            f"{np.mean(d['absd_k']):.2f} of a standard deviation. But D grows as items are added: {d['D5']:.2f} on "
            f"the five scales, and {d['D25']:.2f} on all twenty-five items. <bookmark mark='c'/> The two "
            f"distributions overlap by {spct(d['ovl5'])} on the five scales, and {spct(d['ovl25'])} on the twenty-five "
            "items. Small differences, combined in their most telling direction, add up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(dl), Create(Dl[0]), FadeIn(Dl[1]), FadeIn(key), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def dispute(self):
        d = load("sexes")
        head = heading(r"Univariate or multivariate?")
        left = VGroup(label(r"$D = 2.71$", font_size=40, color=LOST),
                      wrapped_label(r"Marco Del Giudice, \ Tom Booth and Paul Irwing, \ 2012: \ the 16PF in 10{,}261 "
                                    r"Americans, \ factors measured as latent variables: \ overlap only about 10\%", 5.4, 21,
                                    WHITE)).arrange(DOWN, buff=0.3)
        right = VGroup(label(r"uninterpretable", font_size=34, color=GOOD),
                       wrapped_label(r"Janet Hyde's reply: \ $D$ picks the single combination of traits that best "
                                     r"separates the groups, \ assumes multivariate normality, \ and grows with every "
                                     r"variable added; \ no person lives on that combination", 5.4, 21, WHITE))
        right.arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.6, 0])
        foot = wrapped_label(r"both are right about different questions: \ how different is a typical trait, \ and how "
                             r"well can a profile classify a person's sex? \ Say which question a number answers", 12.0,
                             22, YOU).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Del Giudice et al.\ (2012); \ Hyde")
        with self.voiceover(
            "That arithmetic is the centre of a dispute. <bookmark mark='a'/> In 2012 Marco Del Giudice, Tom Booth "
            "and Paul Irwing analysed the 16PF answers of ten thousand two hundred and sixty-one Americans, with the "
            "factors measured as latent variables, and found a D of 2.71: an overlap of only about ten percent. <bookmark mark='b'/> Hyde replied that the number is uninterpretable. "
            "D picks the single combination of traits that best separates the groups, assumes multivariate "
            "normality, and grows with every variable added, and no person lives on that combination. "
            "<bookmark mark='c'/> Both are right, about different questions. How different is a typical trait? And "
            "how well can a whole profile tell a person's sex? A number about group differences should say which "
            "question it answers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
