from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.systems()
        self.lives()
        self.machines()

    def card(self):
        card = chapter_card(15, r"Frontier: \ from lists to lives", r"Does the context model scale, \ and who else "
                            r"uses it?", lit={2008: r"Berry et al.", 2019: r"Uitvlugt \& Healey",
                                              2024: r"Ji-An et al."},
                            part=PART, scale=("mind", "culture"), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: from lists to lives."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def systems(self):
        head = heading(r"One system or many?")
        rows = rows_of([
            (r"the systems view: \ amnesia spares priming, \ so priming and recognition use different stores", WORD),
            (r"the single-system challenge: \ one memory strength, \ read by two tests with different noise, \ "
             r"can produce the same dissociations \ (Berry, \ Shanks and Henson, \ 2008)", CUE),
            (r"the test between them: \ fit both to the same people's priming and recognition, \ trial by trial", MODEL),
            (r"the stakes: \ whether ``memory systems'' are parts of the brain, \ or ways of testing one memory", LOST),
        ], 12.4, 26, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Berry, \ Shanks \& Henson (2008)")
        with self.voiceover(
            "Three open questions. The first is whether memory is one system or many. <bookmark mark='a'/> The "
            "systems view rests on dissociations like Graf, Squire and Mandler's: amnesia spares priming, so "
            "priming must use a different store. <bookmark mark='b'/> But Christopher Berry, David Shanks and "
            "Richard Henson showed in 2008 that a model with a single memory strength, read out by two tests that "
            "differ only in how noisy they are, reproduces those dissociations, and makes quantitative predictions "
            "that the systems view does not. <bookmark mark='c'/> The way to decide is to fit both kinds of model to "
            "the same people's priming and recognition, trial by trial, as we fitted the context model today. "
            "<bookmark mark='d'/> At stake is whether the boxes in the textbook diagram are parts of the brain, or "
            "ways of testing one memory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def lives(self):
        head = heading(r"From lists to lives")
        rows = rows_of([
            (r"the laws of this part come from lists of words, \ minutes long", WHITE),
            (r"Uitvlugt and Healey, \ 2019: \ people recalling the news of the past months show contiguity: \ "
             r"unrelated stories that broke close in time are recalled together", CTX),
            (r"contiguity seems roughly scale-free: \ from seconds to months \ (Healey, \ Long and Kahana, \ 2019)",
             MODEL),
            (r"open: \ is the context of a life the same drifting vector, \ or a hierarchy of contexts, \ for the "
             r"hour, \ the day, \ the year?", CUE),
            (r"open: \ what makes an event boundary, \ a door, \ a new task, \ a new city, \ and what it does to the "
             r"drift", LOST),
        ], 12.4, 26, 0.36).move_to([0, -0.2, 0])
        tag = published_tag(r"Uitvlugt \& Healey (2019); \ Healey, \ Long \& Kahana (2019)")
        with self.voiceover(
            "The second question is whether laws found with lists of words describe a life. <bookmark mark='a'/> "
            "Everything today came from lists studied for a minute and recalled at once. <bookmark mark='b'/> In "
            "2019 Mitchell Uitvlugt and Karl Healey asked people to recall news stories from the previous months. "
            "Stories that broke close together in time were recalled together, even when they had nothing else in "
            "common. <bookmark mark='c'/> Contiguity seems to have no preferred time scale: it appears from seconds "
            "to months. <bookmark mark='d'/> But is the context of a life a single drifting vector, or a hierarchy "
            "of them, one for this hour, one for this year? <bookmark mark='e'/> And what happens at a boundary, "
            "walking through a door, starting a new job, moving to a new city? Those are some of the most active "
            "questions in memory research."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def machines(self):
        head = heading(r"A context model inside a language model?")
        seq = VGroup(*[word_chip(w, font_size=34, width=0.9) for w in ("A", "B", "C", "D", "...", "B", "?")])
        seq.arrange(RIGHT, buff=0.3).move_to([0, 2.0, 0])
        ans = label(r"C", font_size=40, color=MODEL).next_to(seq[-1], DOWN, buff=0.3)
        link = CurvedArrow(seq[-2].get_top() + UP * 0.05, seq[1].get_top() + UP * 0.05, angle=PI / 3, color=CUE,
                           stroke_width=3)
        rows = rows_of([
            (r"an induction head: \ having seen B, \ look back for an earlier B, \ and predict what came after it", WHITE),
            (r"that is a lag-CRP: \ a strong lean to $+1$ from the matched item", WORD),
            (r"Ji-An, \ Zhou, \ Benna and Mattar, \ 2024: \ some attention heads in language models behave like CMR, "
             r"\ and can be written as it", MODEL),
            (r"and the attention update is a modern Hopfield network's: \ chapter 9", CTX),
            (r"open: \ is this convergence telling us what any good sequence memory must do?", CUE),
        ], 12.4, 25, 0.32).move_to([0, -1.1, 0])
        tag = published_tag(r"Ji-An et al.\ (2024)")
        with self.voiceover(
            "And the third question comes from an unexpected place. <bookmark mark='a'/> Large language models "
            "contain attention heads called induction heads. Having just seen a token, one looks back for an earlier "
            "occurrence of the same token, and predicts whatever came after it. <bookmark mark='b'/> Seen from "
            "memory research, that's a lag-conditional response probability: a strong lean to plus one from the "
            "matched item. <bookmark mark='c'/> In 2024 Li Ji-An, Corey Zhou, Marcus Benna and Marcelo Mattar "
            "showed that some of these heads behave like the context maintenance and retrieval model, and that "
            "the model can be rewritten as a kind of attention head. <bookmark mark='d'/> Add chapter nine, where "
            "attention turned out to be a Hopfield network's update, and the machinery of human memory search has "
            "turned up, twice, inside the machines. <bookmark mark='e'/> Is that a coincidence, or is it what any "
            "good memory for sequences has to do? Nobody knows yet."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in seq], lag_ratio=0.2), FadeIn(rows[0]), run_time=1.5)
            self.play(Create(link), run_time=0.8)
            self.play(FadeIn(ans))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
