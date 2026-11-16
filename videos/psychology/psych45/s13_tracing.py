from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Tracing(VoiceoverScene):
    def construct(self):
        self.card()
        self.bkt()
        self.student()
        self.elo()

    def card(self):
        card = chapter_card(12, r"Tracking learning", r"What if ability changes while you measure it?",
                            lit={1995: r"Corbett \& Anderson", 2015: r"Piech et al."}, part=PART, scale=("person",),
                            marr=("how",))
        with self.voiceover("Chapter twelve. Tracking learning."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def bkt(self):
        d = load("bkt")
        head = heading(r"Bayesian knowledge tracing")
        u = word_chip(r"not yet known", color=AUTH, font_size=20, width=3.0).move_to([-4.4, 1.2, 0])
        k = word_chip(r"known", color=GOOD, font_size=20, width=3.0).move_to([-1.4, 1.2, 0])
        arr = Arrow(u.get_right(), k.get_left(), buff=0.1, color=PERSON, stroke_width=3)
        t_l = label(r"learn: \ $T$", font_size=17, color=PERSON).next_to(arr, UP, buff=0.05)
        g_l = label(r"right anyway: \ guess $G$", font_size=16, color=AUTH).next_to(u, DOWN, buff=0.25)
        s_l = label(r"wrong anyway: \ slip $S$", font_size=16, color=GOOD).next_to(k, DOWN, buff=0.25)
        f, t = d["fit"], d["truth"]
        rows = rows_of([
            (r"Corbett and Anderson, \ 1995: \ each skill is a hidden state, \ unknown or known; \ each practice may "
             r"teach it", WHITE),
            (r"answers are noisy: \ a guess when it is unknown, \ a slip when it is known; \ a hidden Markov model", MODEL),
            (rf"Psyche: \ 500 simulated students, \ 10 practices each; \ fitted $T = {f['T']:.2f}$, \ $G = {f['G']:.2f}$, "
             rf"\ $S = {f['S']:.2f}$; \ the truth: \ {t['T']}, \ {t['G']}, \ {t['S']}", GOOD),
            (r"a tutor moves a student on when the chance the skill is known passes about 0.95", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.bkt\_fit}, \ 500 simulated students")
        with self.voiceover(
            "Testing assumes ability holds still. Tutoring software assumes the opposite. <bookmark mark='a'/> In "
            "1995 Albert Corbett and John Anderson treated each skill as a hidden state, unknown or known, and each "
            "practice as a chance to learn it. <bookmark mark='b'/> Answers are noisy: a lucky guess when it's "
            "unknown, a slip when it's known. It's a hidden Markov model. <bookmark mark='c'/> Psyche simulates five "
            "hundred students, ten practices each, and the fit recovers the learning, guessing and slipping rates. "
            "<bookmark mark='d'/> A tutor moves a student on when the chance the skill is known passes about ninety-"
            "five percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(u), FadeIn(k), FadeIn(arr), FadeIn(t_l))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(g_l), FadeIn(s_l))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def student(self):
        d = load("bkt")
        head = heading(r"One student, \ answer by answer")
        n = len(d["y"])
        A = axes([0.5, n + 0.5], [0, 1], x_length=6.0, y_length=3.2, xticks=list(range(1, n + 1)), yticks=[0, 0.5, 0.95, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"practice", ylabel=r"P(known)",
                 center=[-3.0, 0.3, 0], font_size=13)
        pk = curve(A.ax, np.arange(1, n + 1), d["p_known"], MODEL, stroke_width=4)
        marks = VGroup(*[label(r"$\checkmark$" if y else r"$\times$", font_size=18, color=GOOD if y else AUTH)
                         .move_to(A.ax.c2p(t + 1, 0.06)) for t, y in enumerate(d["y"])])
        thr = DashedLine(A.ax.c2p(0.5, 0.95), A.ax.c2p(n + 0.5, 0.95), color=YOU, stroke_width=1.5)
        first = int(np.argmax(d["p_known"] >= 0.95)) + 1
        rows = rows_of([
            (r"before each answer, \ the model's chance that the skill is known", WHITE),
            (r"a wrong first answer keeps it low; \ each right answer raises it, \ quickly, \ because a guess is "
             r"unlikely twice", MODEL),
            (rf"it passes 0.95 before practice {first}: \ mastery, \ by this rule", GOOD),
            (r"the same filter runs for every skill and every student, \ in tutors used by many thousands of pupils",
             YOU),
        ], 5.0, 19, 0.38).move_to([3.8, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.bkt\_filter}")
        with self.voiceover(
            "Here is one simulated student. <bookmark mark='a'/> Before each answer, the model's chance that the skill "
            "is known. <bookmark mark='b'/> A wrong first answer keeps it low. Then each right answer raises it, "
            "quickly, because a guess is unlikely twice in a row. <bookmark mark='c'/> It passes ninety-five percent "
            "within a few practices: mastery, by this rule. <bookmark mark='d'/> The same filter runs for every skill "
            "and every student, in tutors used by many thousands of pupils."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(thr))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(marks), Create(pk), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def elo(self):
        d = load("bkt")
        head = heading(r"Elo, \ and deeper models")
        A = axes([0.5, 10.5], [-2, 1.2], x_length=5.6, y_length=2.8, xticks=list(range(1, 11)), yticks=[-2, -1, 0, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"practice step",
                 ylabel=r"Elo difficulty", center=[-3.3, 0.3, 0], font_size=13)
        b = bars(A.ax, np.arange(1, 11), d["elo_items"], [PERSON] * 10, width=0.6)
        rows = rows_of([
            (r"Elo, \ from chess: \ after each answer, \ the learner's rating moves up and the item's down by "
             r"$k(\text{right} - P)$", WHITE),
            (r"run on the same answers, \ later practice items look easier: \ but they are the same skill; \ the "
             r"learners learned", PERSON),
            (r"a model that holds ability still reads learning as easy items; \ one that tracks learning needs a "
             r"model of change", MODEL),
            (r"deep knowledge tracing used a neural network instead; \ its first large gains shrank against tuned "
             r"simple models: \ the Ledger", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.elo\_learn}, \ on the same simulated answers")
        with self.voiceover(
            "Two other ways to track. <bookmark mark='a'/> Elo's rating, from chess: after each answer, the learner's "
            "rating moves up and the item's down, by a step times the surprise. <bookmark mark='b'/> Run on the same "
            "answers, the later practice items look easier. But they're the same skill. The learners learned. "
            "<bookmark mark='c'/> A model that holds ability still reads learning as easy items. Tracking learning "
            "needs a model of change. <bookmark mark='d'/> Deep knowledge tracing used a neural network instead. Its "
            "first large gains shrank against tuned simple models. That's in the Ledger."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
