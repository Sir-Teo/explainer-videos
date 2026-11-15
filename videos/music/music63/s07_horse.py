from __future__ import annotations

from videos.music.music63.common import *  # noqa: F403


class Horse(SoundScene):
    def construct(self):
        chapter(self, 6, r"Right for the wrong reasons", r"How do you know what a classifier really learnt?")
        self.hans()
        self.quiz()
        self.result()
        self.tests()

    # ------------------------------------------------------------------
    def hans(self):
        items = [
            (r"Berlin, \ 1904: \ a horse, \ Clever Hans, \ appears to do arithmetic, \ tapping out answers", WHITE),
            (r"Oskar Pfungst finds the truth: \ the horse reads tiny cues in the questioner's posture, \ and stops when they relax", WHITE),
            (r"Sturm \ (2014): \ a music classifier is a `horse' if it gets right answers from cues unrelated to the music", WHITE),
            (r"the test: \ change what should not matter, \ and see if the answers change", TUNE),
        ]
        rows_scene(self, r"Clever Hans", items,
                   "A horse explains the danger. <bookmark mark='b'/> In Berlin in 1904 a horse called Clever Hans appeared to do "
                   "arithmetic, tapping out the answers with a hoof. <bookmark mark='c'/> The psychologist Oskar Pfungst found the "
                   "truth: the horse read tiny changes in the questioner's posture, and stopped tapping when they relaxed. "
                   "<bookmark mark='d'/> In 2014 Bob Sturm proposed calling a music classifier a horse if it gets right answers from "
                   "cues that have nothing to do with the music. <bookmark mark='e'/> And the test: change what should not matter, "
                   "and see whether the answers change.", marks="bcde")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("horse")
        c = clip("horse.two")
        card = listen_card(r"Five seconds of a Variation, \ twice. \ Is there any difference? \ If so, \ in which?", width=9.0)
        with self.voiceover("Your turn, and you will need headphones or loudspeakers with real bass. Five seconds of a Variation, twice. Is there any difference, and if so, in which?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"any difference?", kind="physical model", detail=r"a Variation, \ a mains hum", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(r"the second: \ a faint mains hum at 50, \ 100 and 150 Hz, \ 24 dB down, \ as if recorded in another studio", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover("The second carries a faint mains hum, at fifty hertz and its harmonics, twenty-four decibels down, as if recorded in another studio. Easy to miss. A classifier did not miss it."):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        d = load("horse")
        rows_ = VGroup()
        for name, v, col in ((r"trained and tested with the hum", d["acc_hum"], EAR), (r"the same classifier, \ hum removed", d["acc_clean"], WHITE),
                             (r"trained and tested without any hum", d["acc_fair"], TUNE)):
            bar = Rectangle(width=6.0 * v, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.8)
            rows_.add(VGroup(label(name, font_size=18, color=col), bar, label(f"{100 * v:.0f}\\%", font_size=18, color=WHITE)))
        rows_.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.2 + LEFT * 0.5)
        for r in rows_:
            r[1].next_to(r[0], RIGHT, buff=0.3).align_to(rows_, LEFT).shift(RIGHT * 4.6)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        task = label(r"the task: \ was this Variation made in Parts 1 to 30, \ or 31 to 60? \ \ (chance: \ 50\%)", font_size=18, color=GREY_A).to_edge(UP, buff=1.0)
        note = label(rf"its strongest features: \ {', '.join(d['top_features'])} \ (the lowest bands hold the hum)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"a horse", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The task: from five seconds, did this Variation come from the first thirty parts or the last thirty? Every "
            "recording from the later parts carries that faint hum. <bookmark mark='a'/> A classifier on Monochord's embedding "
            f"scores {say(100 * d['acc_hum'])} percent. Impressive. <bookmark mark='b'/> Remove the hum, change nothing about the "
            f"music, and the same classifier falls to {say(100 * d['acc_clean'])} percent. It had learnt the hum. "
            f"<bookmark mark='c'/> Trained honestly, without any hum, it reaches {say(100 * d['acc_fair'])} percent: what the "
            "music itself tells it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(task))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tests(self):
        items = [
            (r"split by artist, \ album and studio, \ not by excerpt: \ no recording on both sides", WHITE),
            (r"intervene: \ filter, \ add noise, \ change the level, \ re-encode: \ things that should not matter", WHITE),
            (r"look at what the model uses: \ its weights, \ its saliency, \ its errors", WHITE),
            (r"test on music made elsewhere: \ another studio, \ another decade, \ another culture", WHITE),
            (r"a high score is a hypothesis about what was learnt, \ not a proof", TUNE),
        ]
        rows_scene(self, r"how to catch a horse", items,
                   "How do you catch a horse? <bookmark mark='b'/> Split the data by artist, album and studio, not by excerpt, so "
                   "that no recording sits on both sides. <bookmark mark='c'/> Intervene: filter, add noise, change the level, "
                   "re-encode, everything that should not matter. <bookmark mark='d'/> Look at what the model uses: its weights, "
                   "its saliency, its errors. <bookmark mark='e'/> Test on music made elsewhere: another studio, decade or culture. "
                   "<bookmark mark='f'/> A high score is a hypothesis about what was learnt, not a proof.", marks="bcdef")
