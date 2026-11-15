from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Grit(VoiceoverScene):
    def construct(self):
        self.card()
        self.grit()
        self.increment()
        self.mindset()

    def card(self):
        card = chapter_card(11, r"Grit and mindset", r"Are perseverance and belief the missing ingredients?",
                            lit={2007: r"Duckworth et al.", 2017: r"Cred\'e et al.", 2018: r"Sisk et al.",
                                 2019: r"Yeager et al."},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter eleven. Grit and mindset."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def grit(self):
        a = archive.CREDE_2017.data
        people = f"{a['people']:,}"
        head = heading(r"Grit")
        rows = rows_of([
            (r"Duckworth, \ Peterson, \ Matthews and Kelly, \ 2007: \ grit, \ perseverance and passion for long-term "
             r"goals, \ measured by a short questionnaire", WHITE),
            (r"grittier cadets were likelier to finish their first summer at West Point; \ grittier children went "
             r"further in a national spelling bee", INTR),
            (r"a best-selling book, \ and grit in school curricula", EXTR),
            (rf"Cred\'e, \ Tynan and Harms, \ 2017: \ {a['samples']} samples, \ {num(a['people'])} people; \ grit "
             rf"and academic performance $\rho = {a['grit_academic_performance']['rho']:.2f}$", WANT),
            (rf"and grit against conscientiousness, \ corrected for unreliability: \ "
             rf"$\rho = {a['grit_conscientiousness']['rho']:.2f}$, \ nearly the same trait under a new name \ "
             r"(Part 3)", LOST),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Duckworth et al.\ (2007); \ Cred\'e, \ Tynan \& Harms (2017)")
        with self.voiceover(
            "If self-control isn't a fuel, perhaps it's a trait. <bookmark mark='a'/> In 2007 Angela Duckworth, "
            "Christopher Peterson, Michael Matthews and Dennis Kelly introduced grit, perseverance and passion for "
            "long-term goals, measured with a short questionnaire. <bookmark mark='b'/> Grittier cadets were "
            "likelier to get through their first summer at West Point, and grittier children went further in a "
            "national spelling bee. <bookmark mark='c'/> A best-selling book followed, and grit entered school "
            "curricula. <bookmark mark='d'/> In 2017 Marcus Credé, Michael Tynan and Peter Harms pooled "
            f"{a['samples']} samples, {people} people. Grit's correlation with academic performance was "
            f"{a['grit_academic_performance']['rho']:.2f}: real, and modest. <bookmark mark='e'/> And its "
            "correlation with conscientiousness, one of the Big Five personality traits, corrected for "
            f"unreliability, was {a['grit_conscientiousness']['rho']:.2f}. That's nearly the same trait under a "
            "new name, the jingle-jangle problem from Part 3."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def increment(self):
        d = load("grit")
        head = heading(r"Derivation: \ what grit adds")
        eqs = VGroup(
            MathTex(r"\Delta R^2 = \frac{(r_{gy} - r_{cy}\, r_{gc})^2}{1 - r_{gc}^2}", font_size=38),
            MathTex(rf"r_{{gy}} = {d['r_gy']:.2f}, \quad r_{{gc}} = {d['r_gc']:.2f}", font_size=32),
        ).arrange(DOWN, buff=0.35)
        A = axes([0, 3], [0, 4], x_length=5.0, y_length=3.6, xticks=None, yticks=[0, 1, 2, 3, 4],
                 yfmt=lambda v: f"{v:g}", ylabel=r"variance in performance explained, \ \%",
                 center=[-3.4, -0.2, 0], font_size=16)
        b1 = bars(A.ax, [0.9], [100 * d["alone"]], WANT, width=0.9)
        b2 = bars(A.ax, [2.1], [max(100 * d["at_equal"], 0.02)], LOST, width=0.9)
        l1 = wrapped_label(r"grit alone", 1.6, 17, WANT).next_to(A.ax.c2p(0.9, 0), DOWN, buff=0.15)
        l2 = wrapped_label(r"grit beyond conscientiousness", 1.8, 17, LOST).next_to(A.ax.c2p(2.1, 0), DOWN,
                                                                                    buff=0.15)
        v1 = label(pct(d["alone"], 1), font_size=18, color=WANT).next_to(b1, UP, buff=0.08)
        v2 = label(pct(d["at_equal"], 1), font_size=18, color=LOST).next_to(b2, UP, buff=0.08)
        c = VGroup(b2, l2, v2)
        alone = VGroup(b1, l1, v1)
        al = VGroup()
        mark = VGroup()
        rows = rows_of([
            (r"the variance grit explains beyond conscientiousness, \ from three correlations", WHITE),
            (rf"grit alone explains {pct(d['alone'], 1)} of performance", WANT),
            (rf"assuming conscientiousness predicts as well as grit does \ ($r_{{cy}} = {d['r_gy']:.2f}$), "
             rf"\ grit adds {pct(d['at_equal'], 1)}: \ almost nothing", LOST),
            (r"the perseverance half of the scale does better than the passion half; \ grit beyond "
             r"conscientiousness is contested", MODEL),
        ], 5.6, 21, 0.3)
        right = VGroup(eqs, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"computed from Cred\'e, \ Tynan \& Harms (2017)'s correlations")
        with self.voiceover(
            "How much does grit add? With three correlations, you can compute it. <bookmark mark='a'/> The variance "
            "in performance that grit explains beyond conscientiousness is this: grit's correlation with "
            "performance, minus the part it shares through conscientiousness, squared, over what is left of grit "
            f"once conscientiousness is removed. <bookmark mark='b'/> Alone, grit explains {100 * d['alone']:.0f} percent of "
            "performance. <bookmark mark='c'/> Suppose conscientiousness predicts performance "
            f"exactly as well as grit does. Then grit adds about {100 * d['at_equal']:.1f} percent: almost nothing. "
            "The answer depends on that assumption, and the README works through others. <bookmark mark='d'/> Credé's analysis "
            "found that the perseverance half of the scale did better than the passion half. Whether grit adds "
            "anything beyond conscientiousness is contested, and the Ledger records it that way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(eqs))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(alone), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(c), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def mindset(self):
        head = heading(r"Growth mindset")
        rows = rows_of([
            (r"Dweck: \ students who believe ability can grow \ (a growth mindset) \ respond to failure by trying "
             r"harder; \ those who believe it is fixed give up", WHITE),
            (r"Sisk and colleagues, \ 2018: \ two meta-analyses; \ mindset and achievement correlate weakly, \ about "
             r"a tenth, \ and interventions have very small average effects", LOST),
            (r"Yeager and colleagues, \ 2019: \ a short online lesson given to a national sample of US ninth "
             r"graders, \ registered in advance; \ a small rise in grades among lower-achieving students, \ little "
             r"for the rest", INTR),
            (r"the pattern of this part: \ a real effect, \ smaller than the story, \ concentrated in some people "
             r"and places \ (continued in Part 54)", MODEL),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"Dweck (2006); \ Sisk et al.\ (2018); \ Yeager et al.\ (2019)")
        with self.voiceover(
            "A related idea is about belief rather than trait. <bookmark mark='a'/> Carol Dweck proposed that "
            "students who believe ability can grow, a growth mindset, respond to failure by trying harder, while "
            "those who believe it is fixed give up. <bookmark mark='b'/> In 2018 Victoria Sisk and colleagues "
            "published two meta-analyses. Mindset and achievement were weakly correlated, around a tenth, and "
            "mindset interventions had very small average effects. <bookmark mark='c'/> In 2019 David Yeager and "
            "colleagues ran a short online lesson with a national sample of American ninth graders, registered in "
            "advance. It raised grades a little among lower-achieving students, and did little for the rest. "
            "<bookmark mark='d'/> That's the pattern of this whole part: a real effect, smaller than the story told "
            "about it, and concentrated in some people and places. Part 54 continues it, in schools."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
