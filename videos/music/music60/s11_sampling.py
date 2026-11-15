from __future__ import annotations

from videos.music.music60.common import *  # noqa: F403


class Sampling(SoundScene):
    def construct(self):
        chapter(self, 10, r"Sampling and machines", r"Who owns a sound, \ and who owns what a machine learned from it?")
        self.quiz()
        self.law()
        self.ai_quiz()
        self.models()
        self.voices()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("sample")
        c = clip("sample.two")
        card = listen_card(r"A new beat, \ twice. \ Under one, \ a slice of our session's recording, \ looped. \ Under the other, \ the same "
                           r"harmony and melody re-played by other hands. \ Which is the sample?", width=10.0)
        with self.voiceover(
            "Your turn. A new beat, twice. Under one, a slice of our session's recording, looped. Under the other, the same harmony "
            "and melody re-played by other hands. Which is the sample?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a sample or a replay?", kind="physical model", detail=r"Part 56's session, \ Part 40's kit", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = VGroup(label(r"the first: \ the recording itself, \ voice and room and all: \ two licences, \ the composition's and the master's", font_size=18, color=TUNE),
                     label(r"the second, \ re-played: \ an interpolation, \ which needs only the composition's", font_size=18, color=WHITE)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.4)
        with self.voiceover(
            "The first: the recording itself, voice and room and all, which needs two licences, one for the composition and one "
            "for the master. The second re-plays the same notes; an interpolation like that needs only the composition's."
        ):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def law(self):
        items = [
            (r"the 1980s: \ hip-hop builds on samples, \ mostly uncleared", WHITE),
            (r"1991: \ Grand Upright v. Warner: \ an unlicensed sample is infringement \ (US)", WHITE),
            (r"2005: \ Bridgeport v. Dimension Films: \ `get a license or do not sample', \ however short \ (US, \ Sixth Circuit)", WHITE),
            (r"2016: \ VMG Salsoul v. Ciccone: \ a trivial sample may be allowed \ (Ninth Circuit); \ the US circuits disagree", WHITE),
            (r"2019: \ Pelham \ (EU Court of Justice): \ even two seconds needs a licence, \ unless changed beyond recognition", TUNE),
        ]
        rows_scene(self, r"sampling in court \ (dated)", items,
                   "Sampling law was made case by case. <bookmark mark='b'/> In the 1980s hip-hop was built on samples, mostly "
                   "uncleared. <bookmark mark='c'/> In 1991, in Grand Upright against Warner, an American court ruled an "
                   "unlicensed sample an infringement. <bookmark mark='d'/> In 2005 the Sixth Circuit went further: get a license or "
                   "do not sample, however short the sample. <bookmark mark='e'/> In 2016 the Ninth Circuit allowed a trivial "
                   "sample, so the American circuits now disagree. <bookmark mark='f'/> And in 2019 the European Court of Justice, "
                   "in a case over two seconds of Kraftwerk, held that even a tiny sample needs a licence, unless it is changed "
                   "beyond recognition.", marks="bcdef")

    # ------------------------------------------------------------------
    def ai_quiz(self):
        d = load("ai")
        c = clip("ai.two")
        card = listen_card(r"One of these melodies is an old Viennese folk song. \ The other was made a moment ago by Part 14's model, \ "
                           r"trained on folk tunes \ (but not that one). \ Which is the machine's?", width=10.0)
        with self.voiceover(
            "Another question. One of these two melodies is an old Viennese folk song. The other was made a moment ago by Part "
            "14's model, trained on the series' folk tunes, but not on that one. Which is the machine's?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"old or new?", kind="physical model", detail=r"Part 8's voice, \ Part 14's model", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(rf"the first: \ the model's \ ({d['surprise_new']:.1f} bits a note, \ to the model); \ the second, \ `{d['folk']}' \ ({d['surprise_old']:.1f} bits)",
                    font_size=18, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            f"The first was the machine's. By the model's own measure it is the less surprising of the two, {say(d['surprise_new'], 1)} bits "
            f"a note against {say(d['surprise_old'], 1)} for the folk song: machines trained on music drift towards the typical. "
            "Which raises the questions of the next minutes: whose music did it learn from, and who owns what it makes?"
        ):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def models(self):
        items = [
            (r"June 2024: \ the major labels sue two music-generation companies, \ Suno and Udio, \ over training on their recordings \ (US)", WHITE),
            (r"late 2025: \ settlements and licences begin: \ models trained on licensed catalogues, \ with payments to rights holders", WHITE),
            (r"November 2025: \ a German court finds that a chatbot reproducing song lyrics infringes \ (GEMA v. OpenAI; \ under appeal)", WHITE),
            (r"US: \ a work needs a human author to be protected; \ machine output alone is not \ (Copyright Office; \ Thaler, \ 2025)", WHITE),
            (r"whether training itself is fair use, \ or needs a licence, \ is still being decided, \ country by country", TUNE),
        ]
        rows_scene(self, r"models and rights \ (dated; \ verify the latest)", items,
                   "Models that make music are the latest machine to break the arrangement, and the story is moving fast, so take "
                   "these dates as a snapshot. <bookmark mark='b'/> In June 2024 the major labels sued two music-generation "
                   "companies, Suno and Udio, in American courts, over training on their recordings. <bookmark mark='c'/> From late "
                   "2025 came settlements and licences: models to be trained on licensed catalogues, with payments to the rights "
                   "holders. <bookmark mark='d'/> In November 2025 a court in Munich found that a chatbot reproducing song lyrics "
                   "infringed, a judgment under appeal. <bookmark mark='e'/> In America a work needs a human author to be "
                   "protected; a machine's output alone is not. <bookmark mark='f'/> Whether training itself is fair use, or needs a "
                   "licence, is still being decided, country by country.", marks="bcdef")

    # ------------------------------------------------------------------
    def voices(self):
        items = [
            (r"a voice is not a copyright: \ a singer's sound can be imitated, \ like a style", WHITE),
            (r"but it can be part of a person's likeness: \ Tennessee's ELVIS Act \ (2024) \ protects voices from unauthorized cloning", WHITE),
            (r"style is free: \ every composer learned from others; \ a model learns from millions", WHITE),
            (r"the open question is scale: \ when imitation is free and endless, \ what does the original earn?", TUNE),
        ]
        rows_scene(self, r"voices and styles", items,
                   "And voices. <bookmark mark='b'/> A voice is not a copyright: a singer's sound can be imitated, like a style. "
                   "<bookmark mark='c'/> But it can be part of a person's likeness, and in 2024 Tennessee's ELVIS Act protected "
                   "voices from unauthorized cloning. <bookmark mark='d'/> Style is free: every composer learned from others, and a "
                   "model learns from millions. <bookmark mark='e'/> The open question is scale: when imitation is free and endless, "
                   "what does the original earn?", marks="bcde")
