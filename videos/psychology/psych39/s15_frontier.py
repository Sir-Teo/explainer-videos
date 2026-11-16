from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.equivalence()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ networks, \ persons and biology", r"What would a valid "
                            r"classification look like?", lit={2016: r"Kruis \& Maris"}, part=PART,
                            scale=("brain", "person"), marr=("what", "how"))
        with self.voiceover("Chapter fourteen. Frontier: networks, persons and biology."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def equivalence(self):
        head = heading(r"Same data, \ three stories")
        boxes = VGroup(*[word_chip(t, color=c, font_size=18, width=3.4) for t, c in (
            (r"a hidden common cause", PERSON), (r"symptoms causing each other", SYMP),
            (r"a shared condition among them", MODEL))]).arrange(DOWN, buff=0.45).move_to([-3.6, 0.2, 0])
        eq = VGroup(*[label(r"$=$", font_size=30, color=GREY_A).move_to(
            (boxes[k].get_bottom() + boxes[k + 1].get_top()) / 2) for k in range(2)])
        rows = rows_of([
            (r"Kruis and Maris, \ 2016: \ the network model of chapter eight, \ a latent-variable model and a "
             r"common-cause model can give exactly the same distribution of symptoms", WHITE),
            (r"so fitting data cannot by itself decide whether a disorder is a cause or a system: \ that takes "
             r"interventions and time", SYMP),
            (r"idiographic networks: \ symptoms tracked several times a day in one person, \ to estimate that "
             r"person's network (Part 47)", MODEL),
            (r"a biological classification would need markers that replicate, \ predict course or treatment, \ and "
             r"beat the interview: \ none does yet", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Kruis \& Maris (2016)")
        with self.voiceover(
            "At the frontier, three questions. <bookmark mark='a'/> In 2016 Joost Kruis and Gunter Maris showed that "
            "the network model of chapter eight, a latent-variable model and a common-cause model can give exactly "
            "the same distribution of symptoms. <bookmark mark='b'/> So fitting data can't by itself decide whether "
            "a disorder is a cause or a system. That takes interventions, and time. <bookmark mark='c'/> Second, "
            "idiographic networks: symptoms tracked several times a day in one person, to estimate that person's own "
            "network. Part 47 takes this up. <bookmark mark='d'/> Third, a biological classification would need "
            "markers that replicate, predict course or treatment, and beat the interview. None does yet."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(boxes), FadeIn(eq))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"are any common mental disorders natural kinds, \ or all of them conventions on continua?", SYMP),
            (r"what does the p factor stand for: \ a cause, \ a severity, \ or a statistical summary?", PERSON),
            (r"can networks estimated in one person predict that person's next episode?", MODEL),
            (r"why has more treatment not lowered prevalence?", AUTH),
            (r"who should decide where the threshold for a diagnosis lies, \ and on what evidence?", YOU),
        ], 12.4, 24, 0.46).move_to([0, -0.2, 0])
        with self.voiceover(
            "So, open questions. Are any common mental disorders natural kinds, or are all of them conventions on "
            "continua? <bookmark mark='b'/> What does the p factor stand for: a cause, a severity, or a statistical "
            "summary? <bookmark mark='c'/> Can a network estimated in one person predict that person's next episode? "
            "<bookmark mark='d'/> Why hasn't more treatment lowered prevalence? <bookmark mark='e'/> And who should "
            "decide where the threshold for a diagnosis lies, and on what evidence?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.15))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
