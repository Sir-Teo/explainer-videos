from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.body()
        self.animals()
        self.machines()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ the body, \ animals and machines", r"What is open?",
                            lit={2013: r"Seth", 2014: r"Anderson \& Adolphs", 2015: r"Gibson et al."},
                            part=PART, scale=("brain", "mind"), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: the body, animals and machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def body(self):
        head = heading(r"Emotion as inference about the body")
        rows = rows_of([
            (r"Anil Seth, \ 2013, \ and Barrett and Simmons, \ 2015: \ the brain predicts the body's signals, \ "
             r"as Part 14's vision predicts the world", BODY),
            (r"a feeling is the brain's best guess at the causes of those signals: \ James's body, \ and chapter "
             r"two's attribution, \ in one model", COG),
            (r"the measurement problem: \ count your heartbeats without touching your pulse, \ and compare with "
             r"the true count \ (Schandry, \ 1981)", WHITE),
            (r"Zamariola and colleagues, \ 2018: \ the scores track heart rate and beliefs about it, \ not only "
             r"perception; \ the debate continues", UNPL),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"Seth (2013); \ Barrett \& Simmons (2015); \ Zamariola et al.\ (2018)")
        with self.voiceover(
            "Three frontiers. The first joins this part's two halves. <bookmark mark='a'/> In 2013 Anil Seth, and in "
            "2015 Lisa Feldman Barrett and Kyle Simmons, proposed that the brain predicts the body's internal "
            "signals, the way Part 14's vision predicts the world. <bookmark mark='b'/> A feeling, on this view, is "
            "the brain's best guess at the causes of those signals: James's body and chapter two's attribution in a "
            "single model. <bookmark mark='c'/> Testing it needs a measure of how well people sense their own "
            "bodies. The standard one asks you to count your heartbeats without touching your pulse, and compares "
            "your count with the true one. <bookmark mark='d'/> In 2018 Zamariola and her colleagues "
            "showed that the scores track people's heart rate and their beliefs about it, not only "
            "perception, and the debate about the measure continues."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def animals(self):
        head = heading(r"Do animals have emotions?")
        rows = rows_of([
            (r"Jaak Panksepp: \ seven primary emotional systems, \ in circuits below the cortex shared by "
             r"mammals: \ seeking, \ rage, \ fear, \ lust, \ care, \ panic and grief, \ play", PLEAS),
            (r"Panksepp and Burgdorf, \ 2003: \ young rats chirp at about 50 kHz when tickled, \ and seek out "
             r"the tickling hand", PLEAS),
            (r"LeDoux \ (chapter eight): \ those are survival circuits; \ whether they come with feelings is a "
             r"separate question", FEAR),
            (r"Anderson and Adolphs, \ 2014: \ study the properties of an emotional state, \ such as persistence, "
             r"\ scalability, \ valence and generalization, \ in any animal", COG),
            (r"Gibson and colleagues, \ 2015: \ fruit flies under a repeated passing shadow enter a graded, \ "
             r"lasting state of defensive arousal; \ whether they feel anything, \ the authors say, \ they "
             r"cannot tell", BODY),
        ], 12.2, 24, 0.36).move_to([0, -0.2, 0])
        tag = published_tag(r"Panksepp \& Burgdorf (2003); \ Anderson \& Adolphs (2014); \ Gibson et al.\ (2015)")
        with self.voiceover(
            "The second: do animals have emotions? <bookmark mark='a'/> Jaak Panksepp argued for seven primary "
            "emotional systems, in circuits below the cortex shared by all mammals: seeking, rage, fear, lust, care, "
            "panic and grief, and play. <bookmark mark='b'/> In 2003 he and Jeffrey Burgdorf reported that young "
            "rats chirp ultrasonically, at about fifty kilohertz, when they are tickled, and seek out the "
            "tickling hand. <bookmark mark='c'/> LeDoux's reply, from chapter eight: those are survival circuits, "
            "and whether they come with feelings is a separate question. <bookmark mark='d'/> David Anderson and "
            "Ralph Adolphs proposed a way forward in 2014: study the measurable properties of an emotional state, "
            "such as persistence, scalability, valence and generalization, in any animal. "
            "<bookmark mark='e'/> In 2015 William Gibson, in Anderson's laboratory, passed a shadow repeatedly over "
            "fruit flies. They entered a graded, lasting state of defensive arousal. Whether the flies feel "
            "anything, the authors said, their experiments cannot tell."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def machines(self):
        head = heading(r"Affect in machines")
        rows = rows_of([
            (r"Rosalind Picard, \ 1997: \ \emph{Affective Computing}, \ machines that recognize, \ express and "
             r"model emotion", WHITE),
            (r"language models, \ trained on text about people, \ describe emotions fluently, \ and can apply "
             r"appraisal rules like chapter seven's", COG),
            (r"so the questions of this part return: \ an emotion word without a body, \ a label with no arousal "
             r"to explain", BODY),
            (r"whether such a system feels anything is Part 27's question, \ and its tests do not yet apply", UNPL),
            (r"what can be asked now: \ are its descriptions of feelings accurate, \ and is it used to manipulate "
             r"them? \ (Part 60)", PLEAS),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Picard (1997)")
        with self.voiceover(
            "And the third: machines. <bookmark mark='a'/> In her 1997 book, Affective Computing, Rosalind Picard set "
            "out a field: machines that recognize, express and model emotion. <bookmark mark='b'/> Today's language "
            "models, trained on text written by people, describe emotions fluently, and can apply appraisal rules like "
            "the ones in chapter seven. <bookmark mark='c'/> So the questions of this part return in a new form: an "
            "emotion word without a body, a label with no arousal to explain. <bookmark mark='d'/> Whether such a "
            "system feels anything is Part 27's question, and its tests don't yet apply. <bookmark mark='e'/> What can "
            "be asked now is whether its descriptions of feelings are accurate, and whether it is used to manipulate "
            "ours. Part 60 returns to both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_(self):
        head = heading(r"Open problems")
        rows = rows_of([
            (r"are fear, \ anger and joy natural kinds with their own circuits, \ or categories the brain "
             r"builds? \ What result would settle it?", FACE),
            (r"how good are people at sensing their own bodies, \ and how would we measure it well?", BODY),
            (r"does the appraisal come before the feeling, \ or are both built at once?", COG),
            (r"which regulation strategies help whom, \ in daily life rather than the laboratory?", PLEAS),
        ], 12.2, 27, 0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "Four open problems. <bookmark mark='a'/> Are fear, anger and joy natural kinds with their own circuits, "
            "or categories the brain builds? And what result would settle it? <bookmark mark='b'/> How good are "
            "people at sensing their own bodies, and how would we measure it well? <bookmark mark='c'/> Does the "
            "appraisal come before the feeling, or are both built at once? <bookmark mark='d'/> And which "
            "regulation strategies help which people, in daily life rather than in the laboratory?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
