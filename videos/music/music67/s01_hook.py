from __future__ import annotations

from videos.music.music67.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.story()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.three")
        card = listen_card(r"A test of the kind researchers use. \ You hear A, \ then B, \ then X, \ which is one of them. \ "
                           r"Is X the same as A, \ or as B?", width=9.6)
        with self.voiceover(
            "A test of the kind researchers use. You will hear A, then B, then X, which is one of the two. Is X the same as "
            "A, or as B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"A", r"B", r"X"], width=2.6, buff=0.8).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        ks = ["A", "B", "X"]
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ X", kind="physical model", detail=r"Part 38's piano; \ Part 58's coder", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        res = VGroup(label(rf"X was B: \ the phrase through Part 58's coder at {d['kbps']} kbit/s", font_size=19, color=TUNE),
                     label(r"one trial proves nothing: \ a guess is right half the time. \ How many trials would?", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.5)
        with self.voiceover(
            f"X was B, the phrase through Part 58's coder at {say(d['kbps'])} kilobits a second. Did you hear it, or guess? One "
            "trial cannot say: a guess is right half the time. How many trials would it take to know? That question, and its "
            "cousins in every corner of music research, is this part."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"1993: \ in \textit{Nature}, \ 36 students score 8 or 9 points higher on spatial tasks after ten minutes of Mozart", WHITE),
            (r"1998: \ Georgia's governor proposes a classical CD for every newborn in the state", WHITE),
            (r"1999: \ a meta-analysis finds the effect small, \ and no larger than that of anything that raises arousal or mood", WHITE),
            (r"2010: \ a larger meta-analysis: \ small, \ similar for other music, \ and largest in the original laboratory's studies", WHITE),
            (r"how did a field come to believe it, \ and how did it find out?", TUNE),
        ]
        rows_scene(self, r"ten minutes of Mozart", items,
                   "The story begins in 1993. <bookmark mark='b'/> In the journal Nature, Frances Rauscher, Gordon Shaw and Katherine "
                   "Ky reported that thirty-six students scored eight or nine points higher on spatial tasks after ten minutes of a "
                   "Mozart sonata. <bookmark mark='c'/> By 1998 the governor of Georgia had proposed a classical CD for every newborn "
                   "in the state. <bookmark mark='d'/> In 1999 Christopher Chabris's meta-analysis found the effect small, and no "
                   "larger than that of anything else that raises arousal or mood. <bookmark mark='e'/> In 2010 a larger one, from "
                   "Jakob Pietschnig and colleagues, found it small, similar for other music, and largest in the studies of the "
                   "original laboratory. <bookmark mark='f'/> How did a field come to believe it, and how did it find out?",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"kinds of knowing: \ sources, \ analysis, \ fieldwork, \ experiment, \ computation, \ practice",
            r"manuscripts copied and recovered; \ a canon against a wider corpus",
            r"experiments and the literatures they make: \ a funnel and a missing half",
            r"listening tests and how many trials they need",
            r"datasets, \ leakage, \ and the series auditing its own verdicts",
            r"standards, \ reading papers, \ and the open problems of this series",
        ], title=r"The plan", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> The kinds of knowing in music research. <bookmark mark='b'/> Manuscripts "
            "copied and recovered, and a canon set against a wider corpus. <bookmark mark='c'/> Experiments and the literatures "
            "they make. <bookmark mark='d'/> Listening tests and how many trials they need. <bookmark mark='e'/> Datasets and "
            "leakage, and this series auditing its own verdicts. And standards, reading papers, and the open problems that "
            "sixty-six parts have left."
        ) as vo:
            self.play(FadeIn(card.head))
            for mark, rr in zip("abcde", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
            self.play(FadeIn(card.rows[-1]), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
