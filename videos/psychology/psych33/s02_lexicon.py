from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403

POLES = [("E", r"extraversion", r"talkative, \ bold, \ energetic", r"quiet, \ reserved"),
         ("A", r"agreeableness", r"warm, \ trusting, \ kind", r"cold, \ critical"),
         ("C", r"conscientiousness", r"organized, \ thorough, \ reliable", r"careless, \ disorderly"),
         ("N", r"neuroticism", r"anxious, \ moody, \ tense", r"calm, \ stable"),
         ("O", r"openness", r"curious, \ imaginative, \ artistic", r"conventional, \ narrow")]


class Lexicon(VoiceoverScene):
    def construct(self):
        self.card()
        self.funnel()
        self.five()
        self.six()

    def card(self):
        card = chapter_card(1, r"From words to five", r"How did 17{,}953 words become five dimensions?",
                            lit={1936: r"Allport \& Odbert", 1961: r"Tupes \& Christal", 1985: r"Costa \& McCrae"},
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. From words to five."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def funnel(self):
        head = heading(r"Fifty years of reduction")
        steps = [(r"17{,}953", r"Allport and Odbert's trait words, \ 1936", GREY_A),
                 (r"171", r"Raymond Cattell's clusters of near-synonyms", C_),
                 (r"16", r"Cattell's factors: \ the 16PF questionnaire, \ 1949", C_),
                 (r"5", r"five recurring factors: \ Tupes and Christal, \ 1961", YOU)]
        widths = [8.0, 5.4, 3.4, 1.8]
        bars_ = VGroup()
        for i, ((n, t, c), w) in enumerate(zip(steps, widths)):
            y = 2.0 - 1.05 * i
            r = Rectangle(width=w, height=0.62, stroke_width=0, fill_color=c, fill_opacity=0.35).move_to([-1.2, y, 0])
            bars_.add(VGroup(r, label(n, font_size=30, color=c).move_to(r),
                             wrapped_label(t, 3.6, 18, c).next_to(r, RIGHT, buff=0.3)))
        rows = rows_of([
            (r"Ernest Tupes and Raymond Christal, \ US Air Force psychologists, \ found the same five factors in trait "
             r"ratings from eight samples; \ their report was little read for twenty years", YOU),
            (r"Warren Norman found them again in 1963; \ Lewis Goldberg named them the ``Big Five'' in 1981", GOOD),
        ], 12.4, 21, 0.3).move_to([0, -2.6, 0])
        tag = historical_tag(r"Allport \& Odbert (1936); \ Tupes \& Christal (1961)")
        with self.voiceover(
            "The reduction took fifty years. <bookmark mark='a'/> It began with Allport and Odbert's seventeen "
            "thousand nine hundred and fifty-three words. <bookmark mark='b'/> In the 1940s Raymond Cattell merged "
            "near-synonyms into a hundred and seventy-one clusters, <bookmark mark='c'/> and factor analysis of "
            "ratings on them gave him sixteen factors, the basis of his 16PF questionnaire, published in 1949. "
            "<bookmark mark='d'/> Then two psychologists working for the United States Air Force, Ernest Tupes and "
            "Raymond Christal, reanalysed trait ratings from eight samples and found the same five factors each "
            "time. Their 1961 report was a technical document, and hardly anyone read it for twenty years. "
            "<bookmark mark='e'/> Warren Norman found the five again in 1963, and in 1981 Lewis Goldberg named them "
            "the Big Five."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, b in zip("abcd", bars_):
                vo.wait_until(m)
                self.play(FadeIn(b, shift=DOWN * 0.1))
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def five(self):
        head = heading(r"The five")
        rows = VGroup()
        for t, name, hi, lo in POLES:
            c = TRAIT_COL[t]
            rows.add(VGroup(word_chip(name, color=c, font_size=24, width=3.4),
                            label(lo, font_size=20, color=GREY_B), Line(LEFT * 1.6, RIGHT * 1.6, color=c,
                                                                        stroke_width=4),
                            label(hi, font_size=20, color=c)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.6, 0])
        foot = rows_of([
            (r"Paul Costa and Robert McCrae built a questionnaire for them: \ the NEO, \ with three factors at first, "
             r"\ all five by 1985, \ and 240 items and thirty facets in the 1992 revision", WHITE),
            (r"each is a continuum: \ most people are near the middle of every one", YOU),
        ], 12.4, 21, 0.28).move_to([0, -2.6, 0])
        tag = historical_tag(r"Goldberg (1981); \ Costa \& McCrae (1985, \ 1992)")
        with self.voiceover(
            "Here they are. <bookmark mark='a'/> Extraversion: talkative and bold, against quiet and reserved. "
            "Agreeableness: warm and trusting, against cold and critical. Conscientiousness: organized and "
            "reliable, against careless. Neuroticism: anxious and moody, against calm and stable. And openness: "
            "curious and imaginative, against conventional. <bookmark mark='b'/> Paul Costa and Robert McCrae built a "
            "questionnaire for them, the NEO. It measured three factors at first, all five by 1985, and in its 1992 "
            "revision it had two hundred and forty items and thirty facets. <bookmark mark='c'/> And each factor is "
            "a continuum. Most people sit near the middle of every one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=10.0)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def six(self):
        head = heading(r"Or six?")
        chips = VGroup(*[word_chip(n, color=c, font_size=22, width=2.2) for n, c in (
            (r"honesty-humility", GOOD), (r"emotionality", N_), (r"extraversion", E_), (r"agreeableness", A_),
            (r"conscientiousness", C_), (r"openness", O_))]).arrange(RIGHT, buff=0.12).move_to([0, 1.7, 0])
        chips[0].set_stroke(width=4)
        rows = rows_of([
            (r"Michael Ashton, \ Kibeom Lee and colleagues, \ 2004: \ trait adjectives in seven languages, \ Dutch, "
             r"\ French, \ German, \ Hungarian, \ Italian, \ Korean and Polish", WHITE),
            (r"a sixth factor appeared in each: \ honesty-humility, \ sincere and fair against greedy and boastful", GOOD),
            (r"the HEXACO model: \ the five, \ rearranged, \ plus honesty-humility", MODEL),
            (r"how many factors there are depends on the words a language has, \ and on how many you choose to keep: "
             r"\ chapter two shows the choosing", YOU),
        ], 12.4, 22, 0.36).move_to([0, -1.0, 0])
        tag = published_tag(r"Ashton et al.\ (2004)")
        with self.voiceover(
            "Five isn't the only answer. <bookmark mark='a'/> In 2004 Michael Ashton, Kibeom Lee and colleagues "
            "brought together lexical studies in seven languages: Dutch, French, German, Hungarian, Italian, Korean "
            "and Polish. <bookmark mark='b'/> A sixth factor appeared in each: honesty-humility, sincere and fair "
            "against greedy and boastful. <bookmark mark='c'/> Their HEXACO model keeps the five, slightly "
            "rearranged, and adds it. <bookmark mark='d'/> How many factors there are depends on the words a "
            "language has, and on how many you choose to keep. Chapter two shows the choosing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in chips], lag_ratio=0.15), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
