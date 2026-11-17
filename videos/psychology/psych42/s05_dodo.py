from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Dodo(VoiceoverScene):
    def construct(self):
        self.card()
        self.verdict()
        self.rogers()
        self.alliance()
        self.specific()

    def card(self):
        card = chapter_card(4, r"The dodo bird", r"Does it matter which therapy?",
                            lit={1936: r"Rosenzweig", 1975: r"Luborsky et al.", 2018: r"Flückiger et al."}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter four. The dodo bird."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def verdict(self):
        head = heading(r"``Everybody has won''")
        rows = rows_of([
            (r"in \emph{Alice in Wonderland}, \ the dodo judges a race: \ ``everybody has won, \ and all must have "
             r"prizes''", GREY_A),
            (r"Rosenzweig, \ 1936: \ different therapies may work equally well, \ through factors they share", WHITE),
            (r"Luborsky, \ Singer and Luborsky, \ 1975: \ a review of comparisons found few differences, \ and borrowed "
             r"the dodo's verdict", PERSON),
            (r"Wampold and colleagues, \ 1997: \ direct comparisons of bona fide therapies, \ meant to help, \ "
             r"differed by about zero on average", SYMP),
            (r"the Ledger: \ contested; \ near-equivalence on average, \ with exceptions", YOU),
        ], 12.4, 23, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Luborsky, \ Singer \& Luborsky (1975); \ Wampold et al.\ (1997)")
        with self.voiceover(
            "Which therapy works best? <bookmark mark='a'/> In Alice in Wonderland, the dodo judges a race and "
            "declares that everybody has won, and all must have prizes. <bookmark mark='b'/> In 1936 Saul Rosenzweig "
            "suggested that different therapies may work equally well, through factors they share. "
            "<bookmark mark='c'/> In 1975 Lester Luborsky and colleagues reviewed the comparisons, found few "
            "differences, and borrowed the dodo's verdict. <bookmark mark='d'/> In 1997 Bruce Wampold and colleagues "
            "meta-analysed direct comparisons of bona fide therapies, ones meant to help, and found differences of "
            "about zero on average. <bookmark mark='e'/> The Ledger marks it contested: near-equivalence on average, "
            "with exceptions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def rogers(self):
        head = heading(r"Three conditions, \ 1957")
        client = little_person(1.0, color=PERSON).move_to([-3.5, 0.95, 0])
        conds = VGroup(*[word_chip(t, color=c, font_size=21, width=w) for t, c, w in (
            (r"empathy", GOOD, 2.3), (r"unconditional positive regard", CARE, 4.6), (r"congruence", SYMP, 2.6))])
        conds[0].move_to([-5.45, 2.35, 0])
        conds[1].move_to([-3.5, -0.45, 0])
        conds[2].move_to([-1.55, 2.35, 0])
        links = VGroup(*[Line(c.get_center(), client.get_center(), color=GREY_D, stroke_width=2).set_z_index(-1)
                         for c in conds])
        card_ = theory_card(r"Client-centred therapy", r"Carl Rogers, \ 1942--1957",
                            r"empathy, \ unconditional positive regard and genuineness in the therapist are necessary "
                            r"and sufficient for change", r"they matter; \ sufficient, \ no", "contested",
                            width=6.2, font_size=20, color=CARE)
        card_.move_to([3.45, 1.15, 0])
        checks = verdict_row([
            (r"empathy goes with better outcomes: \ Elliott and colleagues, \ 2018: \ $r$ about 0.28",
             "replicated"),
            (r"positive regard and genuineness: \ smaller positive correlations \ (Farber and colleagues; \ Kolden "
             r"and colleagues, \ 2018)", "replicated, smaller"),
            (r"sufficient on their own: \ for some disorders, \ specific treatments add \ (next screens)",
             "contested"),
        ], width=12.6, font_size=20)
        checks.move_to([0, -2.05, 0])
        tag = published_tag(r"Rogers (1957); \ Elliott et al.\ (2018); \ Farber et al.\ (2018); \ Kolden et al.\ "
                            r"(2018)")
        with self.voiceover(
            "The boldest answer to what therapies share came from a therapist who thought it was the whole of "
            "therapy. <bookmark mark='a'/> Carl Rogers, the humanistic psychologist of Part 1's third force, called "
            "his method client-centred: the client, not the therapist, directs the work. He was also one of the "
            "first to record therapy sessions so that they could be studied. <bookmark mark='b'/> In 1957 he named "
            "three conditions in the therapist: empathy, understanding the client's world as the client sees it; "
            "unconditional positive regard, warmth that does not depend on what the client says or does; and "
            "congruence, being genuine rather than playing a role. These, he claimed, were necessary and "
            "sufficient for change. <bookmark mark='c'/> Sixty years later, meta-analyses led by Robert Elliott "
            "found that therapist empathy correlates with outcome at about point two eight. "
            "<bookmark mark='d'/> Positive regard and genuineness show smaller, positive correlations. "
            "<bookmark mark='e'/> Sufficient is another matter: for some disorders, as the next screens show, "
            "specific treatments add to what any good relationship gives. Later researchers widened Rogers's three "
            "conditions into one idea."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(client), FadeIn(card_.box), FadeIn(card_.name), run_time=1.4)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(Create(l_), FadeIn(c_)) for l_, c_ in zip(links, conds)],
                                  lag_ratio=0.5), FadeIn(card_.claim), run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(checks.rows[0], shift=RIGHT * 0.15), Indicate(conds[0], color=GOOD))
            vo.wait_until("d")
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(checks.rows[2], shift=RIGHT * 0.15), FadeIn(card_.verdict), FadeIn(card_.status))
        self.clear_scene()

    def alliance(self):
        head = heading(r"The alliance")
        rng = np.random.default_rng(42)
        n = 120
        a = rng.normal(0, 1, n)
        o = 0.28 * a + np.sqrt(1 - 0.28 ** 2) * rng.normal(0, 1, n)
        A = axes([-3, 3], [-3, 3], x_length=4.2, y_length=4.2, xticks=None, yticks=None, xlabel=r"alliance",
                 ylabel=r"outcome", center=[-3.6, 0.2, 0], font_size=13)
        dots = scatter(A.ax, a, o, PERSON, radius=0.045)
        fit = curve(A.ax, np.array([-3, 3]), 0.28 * np.array([-3, 3]), MODEL, stroke_width=3)
        lm = label(r"schematic: \ $r = 0.28$", font_size=13, color=GREY_B).next_to(A, DOWN, buff=0.25)
        rows = rows_of([
            (r"the common factors: \ a warm, \ credible therapist, \ a shared rationale, \ hope, \ and agreement on "
             r"goals and tasks: \ the working alliance", WHITE),
            (r"Flückiger and colleagues, \ 2018: \ 295 studies; \ alliance and outcome correlate about 0.28", MODEL),
            (r"that is modest: \ it explains about 8\% of the variance in outcome", PERSON),
            (r"and the direction is argued: \ early improvement may build the alliance, \ rather than the reverse", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Flückiger et al.\ (2018)")
        with self.voiceover(
            "What could the shared factors be? <bookmark mark='a'/> A warm, credible therapist, a shared rationale for "
            "the problem, hope, and agreement on goals and tasks: together, the working alliance. "
            "<bookmark mark='b'/> In 2018 Christoph Flückiger and colleagues pooled two hundred and ninety-five "
            "studies. Alliance and outcome correlated about zero point two eight. <bookmark mark='c'/> That's "
            "modest. It explains about eight percent of the variance in outcome. <bookmark mark='d'/> And the "
            "direction is argued. Early improvement may build the alliance, rather than the reverse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lm))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(dots))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(fit))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def specific(self):
        head = heading(r"Where ingredients matter")
        rows = rows_of([
            (r"for some problems, \ the specific technique clearly matters: \ exposure for phobias, \ panic and OCD "
             r"(Part 40)", GOOD),
            (r"Tolin, \ 2010: \ cognitive behavioural therapy did a little better than other therapies for anxiety "
             r"and depression", SYMP),
            (r"the debate continues because both sides are partly right: \ common factors carry much of the effect, "
             r"\ and specific ones add to it where the mechanism is known", PERSON),
            (r"the best test is a dismantling study: \ remove one ingredient, \ and see what is lost", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = published_tag(r"Tolin (2010)")
        with self.voiceover(
            "But the dodo isn't always right. <bookmark mark='a'/> For some problems the specific technique clearly "
            "matters: exposure, for phobias, panic and obsessive-compulsive disorder, as Part 40 showed. "
            "<bookmark mark='b'/> In 2010 David Tolin found that cognitive behavioural therapy did a little better "
            "than other therapies for anxiety and depression. <bookmark mark='c'/> The debate goes on because both "
            "sides are partly right. Common factors carry much of the effect, and specific ones add to it where the "
            "mechanism is known. <bookmark mark='d'/> The best test is a dismantling study: remove one ingredient, "
            "and see what's lost."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
