from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.anaesthesia()
        self.diagnosis()
        self.machines()

    def card(self):
        card = chapter_card(14, r"In practice: \ anaesthesia, \ injury and machines", r"Where does a theory of "
                            r"consciousness change what people do?",
                            lit={2004: r"Myles et al.", 2009: r"Schnakers et al.", 2023: r"Butlin et al."},
                            part=PART, scale=("brain", "society"), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: anaesthesia, injury and machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def anaesthesia(self):
        head = heading(r"Awareness under anaesthesia")
        rows = rows_of([
            (r"general anaesthesia is the one setting where consciousness is switched off on purpose, \ millions "
             r"of times a day", WHITE),
            (r"accidental awareness: \ rare, \ but sometimes paralysed and in pain; \ reports in a large UK audit "
             r"came to about one in twenty thousand anaesthetics", LOST),
            (r"processed-EEG monitors turn brain rhythms into a number; \ in one large trial they reduced awareness "
             r"in high-risk patients, \ in another they did no better than monitoring the anaesthetic gas", GNW),
            (r"the isolated forearm: \ a cuff keeps one arm unparalysed, \ and some patients squeeze a hand on "
             r"request when they seemed to be unconscious", SEEN),
        ], 12.0, 24, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Myles et al.\ (2004); \ Avidan et al.\ (2008); \ Pandit et al.\ (2014)")
        with self.voiceover(
            "General anaesthesia is the one setting where consciousness is switched off on purpose, millions of "
            "times a day. <bookmark mark='a'/> Occasionally it isn't fully off. <bookmark mark='b'/> Accidental "
            "awareness is rare, but a patient may be paralysed by the muscle relaxant and in pain, unable to signal. "
            "A large UK audit in 2014, counting what patients reported, found about one case in twenty thousand "
            "anaesthetics, and prospective interviews find more. <bookmark mark='c'/> Monitors that turn the EEG "
            "into a single number were meant to prevent it. In one large trial in 2004 they reduced awareness in "
            "high-risk patients; in another in 2008 they did no better than simply monitoring the anaesthetic gas. "
            "<bookmark mark='d'/> And with the isolated forearm technique, a cuff keeps one arm free of the muscle "
            "relaxant, and some patients who seemed unconscious will squeeze a hand when asked, the operating "
            "theatre's own version of covert awareness."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def diagnosis(self):
        head = heading(r"Diagnosis after brain injury")
        rows = rows_of([
            (r"a misdiagnosis is common: \ in one careful study about four in ten patients called vegetative were "
             r"minimally conscious on a standardized scale", LOST),
            (r"the Coma Recovery Scale--Revised, \ repeated, \ is the bedside standard", WHITE),
            (r"guidelines in the United States \ (2018) \ and Europe \ (2020) \ now recommend brain-based tests, \ "
             r"fMRI or EEG, \ for patients who cannot follow commands", GNW),
            (r"the stakes: \ pain relief, \ rehabilitation, \ prognosis, \ and decisions about life support", SEEN),
        ], 12.0, 24, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Schnakers et al.\ (2009); \ Giacino et al.\ (2018); \ Kondziella et al.\ (2020)")
        with self.voiceover(
            "After brain injury, the questions of this part decide treatment. <bookmark mark='a'/> In 2009 Caroline "
            "Schnakers and colleagues found that about four in ten patients diagnosed as vegetative were in fact "
            "minimally conscious when examined with a standardized scale. <bookmark mark='b'/> That scale, the Coma "
            "Recovery Scale, repeated over days, is the bedside standard. <bookmark mark='c'/> American guidelines in "
            "2018 and European guidelines in 2020 now recommend brain-based tests like those of chapter eleven for "
            "patients who can't follow commands. <bookmark mark='d'/> The stakes are pain relief, rehabilitation, "
            "prognosis, and decisions about life support."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def machines(self):
        head = heading(r"Could a machine be conscious?")
        rows = rows_of([
            (r"Butlin, \ Long and colleagues, \ 2023: \ derive indicator properties from the theories \ "
             r"(a workspace, \ recurrence, \ metacognition, \ agency) \ and check a system for them", WHITE),
            (r"by the workspace and higher-order theories, \ the right architecture would be enough", GNW),
            (r"by integrated information, \ no conventional computer is conscious, \ whatever it computes", IIT),
            (r"so the answer depends on which theory is right, \ which is why chapter nine matters; \ Part 60 "
             r"returns to it", MODEL),
        ], 12.0, 24, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Butlin, \ Long et al.\ (2023)")
        with self.voiceover(
            "The newest practical question is about machines. <bookmark mark='a'/> In 2023 Patrick Butlin, Robert "
            "Long and colleagues proposed deriving indicator properties from the scientific theories, such as a "
            "global workspace, recurrent processing, metacognition and agency, and checking artificial systems for "
            "them. <bookmark mark='b'/> On the workspace and higher-order theories, the right architecture would be "
            "enough. <bookmark mark='c'/> On integrated information, no conventional computer is conscious, whatever "
            "it computes. <bookmark mark='d'/> So the answer depends on which theory is right, which is why the "
            "adversarial tests matter outside the laboratory. Part 60 returns to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
