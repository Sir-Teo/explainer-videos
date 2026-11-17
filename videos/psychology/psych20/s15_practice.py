from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.interview()
        self.surveys()
        self.clinic()

    def card(self):
        card = chapter_card(14, r"In practice: \ interviews, \ surveys, \ the clinic",
                            r"Where does knowing how recall works change what people do?", lit=(), part=PART,
                            scale=("person", "culture"), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: interviews, surveys, the clinic."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def interview(self):
        k = archive.KOHNKEN_1999.data
        head = heading(r"The cognitive interview")
        steps = VGroup(*[word_chip(t, color=c, font_size=22) for t, c in (
            (r"reinstate the context", CTX), (r"report everything", WORD), (r"change the order", CUE),
            (r"change the perspective", MODEL))]).arrange(RIGHT, buff=0.3).move_to([0, 2.0, 0])
        rows = rows_of([
            (r"Fisher and Geiselman, \ 1985: \ an interview for witnesses built from memory research", WHITE),
            (r"reinstating context, \ chapter 5; \ many cues, \ chapter 6; \ new orders of search, \ chapter 7", CTX),
            (rf"K\"ohnken and colleagues, \ 1999: \ {k['studies']} studies, \ {k['comparisons']} comparisons, \ nearly "
             rf"{num(k['people'])} people", DATA),
            (rf"more correct details: \ $d = {k['d_correct']:.2f}$; \ a few more errors too: \ $d \approx "
             rf"{k['d_incorrect']:.2f}$", MODEL),
            (rf"so accuracy hardly changes: \ {k['accuracy_ci']}\% of details correct, \ against "
             rf"{k['accuracy_si']}\% in standard interviews", WORD),
            (r"used by police forces in Britain and elsewhere; \ the interview of Part 56", GREY_A),
        ], 12.4, 24, 0.27).move_to([0, -1.05, 0])
        tag = published_tag(archive.KOHNKEN_1999.cite)
        with self.voiceover(
            "In the 1980s Ronald Fisher and Edward Geiselman set out to build a police interview for witnesses out "
            "of what the laboratory had learned about recall. <bookmark mark='a'/> It has four main instructions. "
            "Reinstate the context: picture the place, the light, how you felt. Report everything, even what seems "
            "trivial. Go through the events in a different order. And describe them from another person's point of "
            "view. <bookmark mark='b'/> Each is a chapter of this part: context as a cue, many cues instead of one, "
            "and a search that starts from somewhere new. <bookmark mark='c'/> Günter Köhnken and his colleagues "
            f"combined {k['studies']} studies in 1999. <bookmark mark='d'/> The cognitive interview drew many more "
            f"correct details than a standard interview, an effect of {k['d_correct']:.2f} standard deviations, and "
            "a small increase in errors as well. <bookmark mark='e'/> Because both rose, accuracy hardly changed: "
            f"{k['accuracy_ci']} percent of details correct, against {k['accuracy_si']}. More is remembered, and "
            "what is remembered is no less reliable. <bookmark mark='f'/> Versions of it are used by police in "
            "Britain and elsewhere, and Part 56 takes it into the courtroom."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in steps], lag_ratio=0.3), run_time=2.0)
            for m, r in zip("bcdef", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def surveys(self):
        head = heading(r"Asking people about their past")
        q1 = label(r"``In the last six months, \ has anyone broken into your home?''", font_size=26, color=LOST)
        q2 = label(r"``Since New Year's Day, \ has anyone broken into your home?''", font_size=26, color=MODEL)
        qs = VGroup(q1, q2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 2.0, 0])
        rows = rows_of([
            (r"telescoping: \ events are remembered as more recent than they were, \ and pulled into the period "
             r"asked about", LOST),
            (r"a landmark gives the period an edge you can remember: \ fewer events are pulled in \ (Loftus and "
             r"Marburger, \ 1983)", MODEL),
            (r"dates are poor cues; \ events are good ones: \ ask about the period, \ then about what happened in it",
             CTX),
            (r"for diaries and calendars, \ the same logic: \ the cue that works is part of the episode", WORD),
        ], 12.4, 25, 0.32).move_to([0, -0.9, 0])
        tag = historical_tag(r"Loftus \& Marburger (1983)")
        with self.voiceover(
            "Surveys depend on recall all the time: how many times did you see a doctor last year, were you a "
            "victim of a crime? <bookmark mark='a'/> A well-known error is telescoping. People remember events as "
            "more recent than they were, and pull them into the period being asked about, so they report too much. "
            "<bookmark mark='b'/> Elizabeth Loftus and Wesley Marburger found that anchoring the question to a "
            "landmark, an event everyone remembers, reduces it: the period then has an edge that memory can find. "
            "<bookmark mark='c'/> The lesson from encoding specificity is direct. A date is a poor cue, because "
            "dates are rarely part of what was stored. Events are good cues. So good questionnaires first ask about "
            "the period, its landmarks and routines, and then about what happened in it. "
            "<bookmark mark='d'/> Calendars and diaries used in research work the same way: the cue that works is "
            "part of the episode."
        ) as vo:
            self.play(FadeIn(head), FadeIn(q1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(q2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def clinic(self):
        head = heading(r"Memory in the clinic")
        rows = rows_of([
            (r"word-list learning tests: \ a list of 15 words read aloud, \ recalled, \ five times; \ then a second "
             r"list; \ then a delay", WHITE),
            (r"the Rey Auditory Verbal Learning Test, \ the California Verbal Learning Test: \ standard in "
             r"neuropsychology", GREY_A),
            (r"the learning curve over trials, \ what survives the interfering list, \ what survives the delay, \ "
             r"and recognition at the end", MODEL),
            (r"recall that fails while recognition holds points to search; \ both failing points to storage", CUE),
            (r"the serial-position curve as a symptom: \ in early Alzheimer's disease the first words, \ which need "
             r"long-term storage, \ fall before the last", WORD),
            (r"chapter 2's curve, \ read for one person, \ against norms for their age", CTX),
        ], 12.4, 25, 0.33).move_to([0, -0.2, 0])
        with self.voiceover(
            "And the clinic. <bookmark mark='a'/> Almost every neuropsychological assessment includes a word-list "
            "test like the one you took today. A list of fifteen words is read aloud and recalled, five times over; "
            "then a second list is read, to interfere; then the first is recalled again, after a delay, and finally "
            "recognised. <bookmark mark='b'/> The Rey test and the California test are the best known. "
            "<bookmark mark='c'/> Each stage asks a different question: how fast does the person learn, how much is "
            "lost to interference, how much survives the delay? <bookmark mark='d'/> The pattern matters. If recall "
            "fails but recognition is fine, the trouble is in the search; if both fail, the memory was never stored. "
            "<bookmark mark='e'/> Even the serial-position curve is used. In early Alzheimer's disease, recall of "
            "the first words, which depends on long-term storage, falls before recall of the last few. "
            "<bookmark mark='f'/> It's chapter two's curve, read for one person, against norms for their age."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
