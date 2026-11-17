from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403


class Freud(VoiceoverScene):
    def construct(self):
        self.card()
        self.tradition()
        self.legacy()
        self.inkblots()

    def card(self):
        card = chapter_card(10, r"Freud, \ under Part 3's standards", r"What survived of psychoanalysis?",
                            lit={1900: r"Freud", 1921: r"Rorschach", 1998: r"Westen", 2000: r"Lilienfeld et al."},
                            part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter ten. Freud, under Part 3's standards."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def tradition(self):
        head = heading(r"The other theory of personality")
        rows = rows_of([
            (r"Sigmund Freud: \ personality as the outcome of conflict between wishes, \ conscience and reality, \ "
             r"much of it outside awareness, \ shaped in early childhood", WHITE),
            (r"its evidence was clinical: \ the analyst's interpretation of what patients said, \ case by case", GREY_A),
            (r"its influence on literature, \ therapy and everyday language is enormous: \ repression, \ denial, \ "
             r"the unconscious", O_),
            (r"but a theory that can explain any outcome after the fact predicts none in advance: \ Part 1's test "
             r"of a science", LOST),
        ], 12.4, 24, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "There's another theory of personality, older and far better known. <bookmark mark='a'/> For Sigmund "
            "Freud, personality was the outcome of conflict between wishes, conscience and reality, much of it "
            "outside awareness, and shaped in early childhood. <bookmark mark='b'/> Its evidence was clinical: the "
            "analyst's interpretation of what patients said, case by case. <bookmark mark='c'/> Its influence on "
            "literature, on therapy and on everyday language is enormous: repression, denial, the unconscious. "
            "<bookmark mark='d'/> But a theory that can explain any outcome after the fact predicts none in advance, "
            "and that's Part 1's test of a science."
        ) as vo:
            for m, r in zip("abcd", rows):
                if m == "a":
                    self.play(FadeIn(head))
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def legacy(self):
        head = heading(r"What survived")
        left = VGroup(label(r"supported", font_size=26, color=GOOD),
                      wrapped_label(r"much of mental life is not conscious: \ thoughts, \ feelings and motives", 5.4,
                                    21, WHITE),
                      wrapped_label(r"mental processes run in parallel and can conflict", 5.4, 21, WHITE),
                      wrapped_label(r"patterns of relating to others begin early and persist", 5.4, 21, WHITE))
        left.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        right = VGroup(label(r"disputed", font_size=26, color=LOST),
                       wrapped_label(r"that the laboratory unconscious, \ automatic habits and implicit memory \ "
                                     r"(Parts 20 and 27), \ resembles Freud's at all", 5.4, 21, WHITE),
                       wrapped_label(r"that these ideas came from Freud rather than from Helmholtz, \ Wundt and later "
                                     r"research", 5.4, 21, WHITE),
                       wrapped_label(r"that his case reports recorded what patients said rather than what his theory "
                                     r"expected", 5.4, 21, WHITE))
        right.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.0, 0])
        tag = published_tag(r"Westen (1998); \ Kihlstrom")
        with self.voiceover(
            "What survived? <bookmark mark='a'/> In 1998 Drew Westen argued that a set of broad propositions now "
            "have strong research support: much of mental life, thoughts, feelings and motives, isn't conscious; "
            "mental processes run in parallel and can conflict; and patterns of relating to others begin early and "
            "persist. <bookmark mark='b'/> John Kihlstrom replied that the unconscious found in the laboratory, the "
            "automatic habits and implicit memories of Parts 20 and 27, bears no resemblance to Freud's; that the "
            "ideas came before Freud, from Helmholtz and Wundt, or from later research; and that historians have "
            "shown Freud's case reports bent toward what his theory expected. The broad themes survive. The "
            "specific theory has little support."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in left], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in right], lag_ratio=0.5), run_time=4.0)
        self.clear_scene()

    def inkblots(self):
        head = heading(r"Inkblots, \ measured")
        rng = np.random.default_rng(1921)
        pts = rng.normal(0, 1, size=(14, 2)) * [0.6, 0.9]
        blot = VGroup()
        for x, y in pts:
            r = float(rng.uniform(0.15, 0.45))
            for s in (-1, 1):
                blot.add(Ellipse(width=2 * r * 1.3, height=2 * r, color="#2B2F36", fill_opacity=1, stroke_width=0)
                         .move_to([s * abs(x) - 4.2, y + 0.4, 0]))
        rows = rows_of([
            (r"Hermann Rorschach, \ 1921: \ ten inkblots, \ meant for diagnosing schizophrenia; \ used as a general "
             r"test of personality only after his death", WHITE),
            (r"Scott Lilienfeld, \ James Wood and Howard Garb, \ 2000: \ Part 3's standards applied to the Rorschach, \ "
             r"story-telling tests and human figure drawings", MODEL),
            (r"a few scores were supported; \ most were not; \ few added anything to simpler measures", LOST),
            (r"and the norms of the most used scoring system made ordinary adults look disturbed", N_),
            (r"they advised structured interviews and validated self-reports wherever possible", YOU),
        ], 7.2, 20, 0.32).move_to([2.6, -0.3, 0])
        tag = published_tag(r"Rorschach (1921); \ Lilienfeld, \ Wood \& Garb (2000)")
        with self.voiceover(
            "Freud's tradition also gave clinics their projective tests. <bookmark mark='a'/> In 1921 Hermann "
            "Rorschach published ten inkblots, meant for diagnosing schizophrenia. They became a general test of "
            "personality only after his death. <bookmark mark='b'/> In 2000 Scott Lilienfeld, James Wood and Howard "
            "Garb applied Part 3's standards to the Rorschach, to story-telling tests and to human figure drawings. "
            "<bookmark mark='c'/> A few scores were supported. Most were not, and few added anything to simpler "
            "measures. <bookmark mark='d'/> And the norms of the most widely used scoring system made ordinary "
            "adults look disturbed. <bookmark mark='e'/> They advised structured interviews and validated "
            "self-reports wherever possible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(blot))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
