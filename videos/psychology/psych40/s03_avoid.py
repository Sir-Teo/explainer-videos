from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Avoid(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_factors()
        self.loop()

    def card(self):
        card = chapter_card(2, r"Fear that never unlearns", r"Why does avoidance keep fear alive?",
                            lit={1947: r"Mowrer"}, part=PART, scale=("circuit", "person"), marr=("how",))
        with self.voiceover("Chapter two. Fear that never unlearns."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def two_factors(self):
        head = heading(r"Two factors")
        a = word_chip(r"1. \ pairing: \ signal $\to$ shock", color=AUTH, font_size=19, width=4.6).move_to([-3.6, 1.2, 0])
        b = word_chip(r"fear of the signal", color=PERSON, font_size=19, width=4.6).move_to([-3.6, 0.0, 0])
        c = word_chip(r"2. \ escape the signal: \ relief", color=GOOD, font_size=19, width=4.6).move_to([-3.6, -1.2, 0])
        arr = VGroup(Arrow(a.get_bottom(), b.get_top(), buff=0.05, color=GREY_B),
                     Arrow(b.get_bottom(), c.get_top(), buff=0.05, color=GREY_B),
                     CurvedArrow(c.get_left() + LEFT * 0.05, b.get_left() + LEFT * 0.05, angle=-1.2, color=GREY_B))
        rows = rows_of([
            (r"Mowrer, \ 1947: \ fear is learned by Pavlovian pairing (Part 16)", AUTH),
            (r"and then avoidance is learned by reward: \ escaping the feared signal brings relief, \ which "
             r"reinforces escaping", GOOD),
            (r"the trap: \ each avoided trial is a trial in which the person never finds out that nothing bad would "
             r"have happened", PERSON),
            (r"so the fear is never tested, \ and never unlearned", YOU),
        ], 6.0, 20, 0.38).move_to([3.4, -0.2, 0])
        tag = historical_tag(r"Mowrer (1947)")
        with self.voiceover(
            "Start with anxiety, and the learning of Part 16. <bookmark mark='a'/> In 1947 O. Hobart Mowrer proposed "
            "two factors. First, fear is learned by Pavlovian pairing: a signal, then shock. <bookmark mark='b'/> "
            "Then avoidance is learned by reward. Escaping the feared signal brings relief, and relief reinforces "
            "escaping. <bookmark mark='c'/> Here's the trap. Each avoided trial is a trial in which the person never "
            "finds out that nothing bad would have happened. <bookmark mark='d'/> So the fear is never tested, and "
            "never unlearned."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(a), GrowArrow(arr[0]), FadeIn(b))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), GrowArrow(arr[1]), FadeIn(c), Create(arr[2]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def loop(self):
        d = load("avoid")
        head = heading(r"The loop, \ computed")
        n = len(d["fear"])
        A = axes([0, n], [0, 1.05], x_length=5.6, y_length=3.0, xticks=[0, 20, 40, 60, 80], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"trial", ylabel=r"fear",
                 center=[-3.2, 0.2, 0], font_size=14)
        t = np.arange(n)
        acq = Rectangle(width=abs(A.ax.c2p(20, 0)[0] - A.ax.c2p(0, 0)[0]), height=3.0, stroke_width=0,
                        fill_color=AUTH, fill_opacity=0.1).move_to([(A.ax.c2p(0, 0)[0] + A.ax.c2p(20, 0)[0]) / 2,
                                                                  A.ax.c2p(0, 0.5)[1], 0])
        la = label(r"shocks", font_size=13, color=AUTH).next_to(acq, UP, buff=0.05)
        kept = curve(A.ax, t, d["fear"], PERSON, stroke_width=4)
        gone = curve(A.ax, t, d["exposure"], GOOD, stroke_width=4)
        av = np.asarray(d["avoided"], bool)
        ticks = VGroup(*[Line(A.ax.c2p(i, -0.02), A.ax.c2p(i, 0.05), color=PERSON, stroke_width=2)
                         for i in range(n) if av[i]])
        key = legend([(PERSON, r"avoidance allowed"), (GOOD, r"exposure, \ no escape")], font_size=14).move_to(
            A.ax.c2p(62, 0.85))
        rows = rows_of([
            (r"Psyche: \ a Rescorla-Wagner learner gets 20 signal-shock pairings, \ then 60 trials with no shock", WHITE),
            (rf"allowed to avoid, \ it escapes the signal on {pct(d['share_avoided'])} of trials; \ the few full "
             rf"exposures barely dent the fear, \ which ends at {d['final']:.2f}", PERSON),
            (rf"made to stay, \ exposure with response prevention, \ it learns that no shock comes: \ fear falls to "
             rf"{d['final_exposure']:.2f}", GOOD),
            (r"this is the logic of exposure therapy: \ stay with the feared thing long enough to learn that it is "
             r"safe", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.avoidance}, \ median of 21 runs")
        with self.voiceover(
            "Here's the loop in Psyche. <bookmark mark='a'/> A Rescorla-Wagner learner gets twenty pairings of a "
            "signal with shock, then sixty trials with no shock at all. <bookmark mark='b'/> Allowed to avoid, it "
            f"escapes the signal on {spct(d['share_avoided'])} of trials. The few full exposures barely dent the "
            "fear, which ends almost where it began. <bookmark mark='c'/> Made to stay, exposure with response "
            "prevention, it learns that no shock comes, and fear falls to nearly nothing. <bookmark mark='d'/> That's "
            "the logic of exposure therapy: stay with the feared thing long enough to learn that it's safe."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(acq), FadeIn(la))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(kept), FadeIn(ticks), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(gone), FadeIn(key), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
