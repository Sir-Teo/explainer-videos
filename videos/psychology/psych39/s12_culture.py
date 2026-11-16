from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Culture(VoiceoverScene):
    def construct(self):
        self.card()
        self.idioms()
        self.frame()

    def card(self):
        card = chapter_card(11, r"Culture, \ stigma and idioms of distress", r"Does suffering speak one language?",
                            lit={1981: r"Nichter", 2015: r"Kaiser et al."}, part=PART, scale=("person", "culture"),
                            marr=("what",))
        with self.voiceover("Chapter eleven. Culture, stigma and idioms of distress."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def idioms(self):
        head = heading(r"Idioms of distress")
        rows = rows_of([
            (r"Nichter, \ 1981: \ working with Havik Brahmin women in South India, \ he called the culturally "
             r"shaped ways of expressing suffering ``idioms of distress''", WHITE),
            (r"Kaiser and colleagues, \ 2015: \ a systematic review of ``thinking too much'', \ an idiom described "
             r"in many countries", SYMP),
            (r"it overlaps with depression and anxiety, \ but is neither a translation of them nor a single "
             r"syndrome", PERSON),
            (r"DSM-5 now lists cultural concepts of distress, \ and a cultural formulation interview; \ Part 38's "
             r"lesson about measures applies to diagnoses too", MODEL),
            (r"stigma: \ the label itself can harm, \ through shame, \ lost work and avoided care; \ the language of "
             r"this series is people-first for that reason", YOU),
        ], 12.4, 21, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Nichter (1981); \ Kaiser et al.\ (2015)")
        with self.voiceover(
            "Suffering doesn't speak one language. <bookmark mark='a'/> In 1981 the anthropologist Mark Nichter, "
            "working with Havik Brahmin women in South India, called the culturally shaped ways of expressing "
            "suffering idioms of distress. <bookmark mark='b'/> In 2015 Bonnie Kaiser and colleagues reviewed one of "
            "them, thinking too much, described in many countries. <bookmark mark='c'/> It overlaps with depression "
            "and anxiety, but it's neither a translation of them nor a single syndrome. <bookmark mark='d'/> The "
            "fifth edition of the manual now lists cultural concepts of distress, and a cultural formulation "
            "interview. Part 38's lesson about measures applies to diagnoses too. <bookmark mark='e'/> And stigma: "
            "the label itself can harm, through shame, lost work, and care that's avoided. That's why this series "
            "speaks of people with a disorder, not of the disorder as the person."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def frame(self):
        head = heading(r"Diathesis and stress")
        A = axes([0, 10], [0, 10], x_length=4.4, y_length=3.2, xticks=None, yticks=None,
                 xlabel=r"stress", ylabel=r"vulnerability", center=[-3.6, -0.2, 0], font_size=14)
        xs = np.linspace(0.6, 10, 100)
        thr = curve(A.ax, xs, np.clip(12 / xs, 0, 10), AUTH, stroke_width=4)
        lt = label(r"disorder above the line", font_size=14, color=AUTH).move_to(A.ax.c2p(7, 8))
        p1 = Dot(A.ax.c2p(7, 0.6), radius=0.1, color=GOOD)
        p2 = Dot(A.ax.c2p(7, 4.5), radius=0.1, color=PERSON)
        rows = rows_of([
            (r"the frame for the next three parts: \ a disorder arises when a vulnerability, \ the diathesis, \ "
             r"meets enough stress", WHITE),
            (r"the same event can leave one person well and another ill: \ chapter eight's networks are one "
             r"mechanism", PERSON),
            (r"vulnerability comes from genes (Part 9), \ development (Parts 30 and 31) and learning (Part 16)", SYMP),
            (r"Part 40: \ fear and sadness; \ Part 41: \ psychosis, \ addiction and development; \ Part 42: \ does "
             r"therapy work?", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "One frame holds the next three parts together. <bookmark mark='a'/> A disorder arises when a "
            "vulnerability, the diathesis, meets enough stress. <bookmark mark='b'/> The same event can leave one "
            "person well and another ill, and chapter eight's networks are one mechanism for that. "
            "<bookmark mark='c'/> Vulnerability comes from genes, from development and from learning, all met "
            "earlier in the series. <bookmark mark='d'/> Next come fear and sadness, then psychosis, addiction and "
            "development, and then the question of whether therapy works."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(thr), FadeIn(lt))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(p1), FadeIn(p2))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
