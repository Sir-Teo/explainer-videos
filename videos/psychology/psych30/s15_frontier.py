from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.scale()
        self.headcams()
        self.machines()
        self.open_()

    def card(self):
        card = chapter_card(14, r"Frontier: \ many babies, \ head cameras and machines", r"What is open?",
                            lit={2020: r"ManyBabies 1", 2022: r"Piloto et al.", 2024: r"Vong et al."},
                            part=PART, scale=("person", "group"), marr=("what", "how"))
        with self.voiceover("Chapter fourteen. Frontier: many babies, head cameras and machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def scale(self):
        head = heading(r"Infancy research at scale")
        rows = rows_of([
            (r"ManyBabies has gone on to test other classic findings across many laboratories, \ including "
             r"infants' understanding of false belief", NUM),
            (r"the same design questions as Part 43's capstone: \ a preregistered protocol, \ every laboratory's "
             r"data shared, \ moderators planned in advance", LOOK),
            (r"online testing at home, \ with webcam eye tracking, \ widens samples beyond families who can visit "
             r"a university", MIND),
            (r"the open question: \ which of the field's famous effects survive at scale, \ and what a typical "
             r"infant effect size really is", GREY_A),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"ManyBabies Consortium (2020)")
        with self.voiceover(
            "Three frontiers. The first is scale. <bookmark mark='a'/> ManyBabies has gone on to test other classic "
            "findings across many laboratories, including infants' understanding of false belief. "
            "<bookmark mark='b'/> These are the design questions of Part 43's capstone: a preregistered protocol, "
            "every laboratory's data shared, moderators planned in advance. <bookmark mark='c'/> Online testing at "
            "home, with webcam eye tracking, widens samples beyond the families who can visit a university. "
            "<bookmark mark='d'/> The open question is which of the field's famous effects survive at scale, and "
            "what a typical infant effect size really is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def headcams(self):
        head = heading(r"Through the eyes of one child")
        cam = VGroup(baby(0.6), RoundedRectangle(corner_radius=0.05, width=0.5, height=0.3, color=WHITE,
                                                  fill_opacity=0.8).shift(UP * 0.7 + RIGHT * 0.2)).move_to([-4.2, 0.5, 0])
        rows = rows_of([
            (r"head-mounted cameras record what infants actually see and hear, \ for months: \ faces close up, \ "
             r"hands, \ a few objects again and again", WHITE),
            (r"Wai Keen Vong, \ Wentao Wang, \ Emin Orhan and Brenden Lake, \ 2024: \ a network trained on 61 hours "
             r"of one child's head-camera video, \ from 6 to 25 months, \ learned many word-to-object mappings", MODEL),
            (r"a few percent of one child's waking hours, \ and no built-in knowledge of objects or words beyond a "
             r"general learner", LOOK),
            (r"it does not show that children learn this way; \ it shows how much is learnable from the input a "
             r"child really gets \ (Part 14's frontier, \ continued)", GREY_A),
        ], 7.2, 21, 0.34).move_to([2.6, -0.1, 0])
        tag = published_tag(r"Vong et al.\ (2024)")
        with self.voiceover(
            "The second frontier is the infant's own view. <bookmark mark='a'/> Head-mounted cameras record what "
            "infants actually see and hear, for months: faces close up, hands, and a few objects again and again. "
            "<bookmark mark='b'/> In 2024 Wai Keen Vong, Wentao Wang, Emin Orhan and Brenden Lake trained a network "
            "on sixty-one hours of one child's head-camera video, from six to twenty-five months, and it learned "
            "many word-to-object mappings. <bookmark mark='c'/> That's a small fraction of one child's waking "
            "hours, with no built-in knowledge of objects or words beyond a general learner. "
            "<bookmark mark='d'/> It doesn't show that children learn this way. It shows how much is learnable from "
            "the input a child really gets, which is where Part 14's frontier left off."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cam))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def machines(self):
        head = heading(r"Infants as a benchmark for machines")
        rows = rows_of([
            (r"Luis Piloto, \ Ari Weinstein, \ Peter Battaglia and Matthew Botvinick, \ 2022: \ a model shown "
             r"synthetic videos, \ then tested with violation-of-expectation probes adapted from infant studies", WHITE),
            (r"five concepts: \ solidity, \ object persistence, \ continuity, \ unchangeableness, \ directional "
             r"inertia", OBJ),
            (r"the model that represented the scene as objects showed surprise at the impossible events, \ after "
             r"as little as 28 hours of video; \ models without objects did not pass all the tests", MODEL),
            (r"the infant's looking paradigm has become a test for machine common sense, \ with the same question "
             r"attached: \ what does a surprise signal show? \ (Part 60)", GREY_A),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Piloto et al.\ (2022)")
        with self.voiceover(
            "The third frontier turns the method around. <bookmark mark='a'/> In 2022 Luis Piloto, Ari Weinstein, "
            "Peter Battaglia and Matthew Botvinick trained a model on synthetic videos and tested it with "
            "violation-of-expectation probes adapted from infant studies. <bookmark mark='b'/> There were five "
            "concepts: solidity, object persistence, continuity, unchangeableness and directional inertia. "
            "<bookmark mark='c'/> The model that represented scenes as objects showed surprise at the impossible "
            "events, after as little as twenty-eight hours of video. Models without objects did not pass all the "
            "tests. <bookmark mark='d'/> So the infant's looking paradigm has become a test for machine common sense, "
            "with the same question attached: what does a surprise signal show? Part 60 returns to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_(self):
        head = heading(r"Open problems")
        rows = rows_of([
            (r"what does a longer look measure: \ surprise, \ novelty, \ familiarity, \ or interest? \ can models "
             r"of looking decide?", LOOK),
            (r"which infant findings survive preregistered, \ multi-laboratory tests?", NUM),
            (r"how much knowledge is in the starting state, \ and how much in a few months of very structured "
             r"input?", OBJ),
            (r"which early experiences matter for later life, \ and through what?", CARE),
        ], 12.2, 27, 0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "Four open problems. <bookmark mark='a'/> What does a longer look measure: surprise, novelty, "
            "familiarity, or interest? Can models of looking decide? <bookmark mark='b'/> Which infant findings "
            "survive preregistered, multi-laboratory tests? <bookmark mark='c'/> How much knowledge is in the "
            "starting state, and how much comes from a few months of very structured input? "
            "<bookmark mark='d'/> And which early experiences matter for later life, and through what?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
