from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Meds(VoiceoverScene):
    def construct(self):
        self.card()
        self.compare()
        self.relapse()

    def card(self):
        card = chapter_card(6, r"Pills, \ talk, \ or both", r"What happens when treatment stops?",
                            lit={2005: r"Hollon et al."}, part=PART, scale=("molecule", "person"), marr=("what",))
        with self.voiceover("Chapter six. Pills, talk, or both."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def compare(self):
        head = heading(r"Head to head")
        rows = rows_of([
            (r"for depression, \ in trials that compare them directly, \ cognitive therapy and antidepressants do "
             r"about equally well in the short term", WHITE),
            (r"combining them does somewhat better than either alone", GOOD),
            (r"people differ: \ some prefer one, \ some respond to one and not the other, \ and preference itself "
             r"affects who stays in treatment", PERSON),
            (r"which to choose is a shared decision, \ not a contest (Part 40's chapter on the drugs)", YOU),
        ], 12.4, 24, 0.48).move_to([0, -0.3, 0])
        with self.voiceover(
            "How does therapy compare with medication? <bookmark mark='a'/> For depression, in trials that compare "
            "them directly, cognitive therapy and antidepressants do about equally well in the short term. "
            "<bookmark mark='b'/> Combining them does somewhat better than either alone. <bookmark mark='c'/> People "
            "differ. Some prefer one; some respond to one and not the other; and preference itself affects who stays "
            "in treatment. <bookmark mark='d'/> Which to choose is a shared decision, not a contest."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def relapse(self):
        head = heading(r"After treatment stops")
        A = axes([0.3, 3.7], [0, 90], x_length=5.2, y_length=3.0, xticks=None, yticks=[0, 25, 50, 75],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"relapsed within a year", center=[-3.4, 0.5, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3], [31, 76, 47], [GOOD, AUTH, SYMP], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.6, 13, c).next_to(A.ax.c2p(x, 0), DOWN, buff=0.15) for x, t, c in
                         ((1, r"cognitive therapy, \ then stopped", GOOD), (2, r"drug, \ then switched to placebo", AUTH),
                          (3, r"drug continued", SYMP))])
        rows = rows_of([
            (r"Hollon and colleagues, \ 2005: \ people who had responded to cognitive therapy or to an antidepressant "
             r"were followed for a year", WHITE),
            (r"after therapy ended, \ 31\% relapsed; \ after the drug was replaced by placebo, \ 76\%; \ on the drug "
             r"continued, \ 47\%", PERSON),
            (r"therapy's effect seemed to outlast it, \ as if a skill had been learned; \ the drug's lasted while "
             r"it was taken", GOOD),
            (r"one trial, \ with modest numbers; \ later studies broadly agree that therapy lowers relapse", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Hollon et al.\ (2005)")
        with self.voiceover(
            "The difference shows when treatment stops. <bookmark mark='a'/> In 2005 Steven Hollon and colleagues "
            "followed, for a year, people who had responded to cognitive therapy or to an antidepressant. "
            "<bookmark mark='b'/> After therapy ended, about thirty percent relapsed. After the drug was replaced by a "
            "placebo, about three quarters did. With the drug continued, under half. <bookmark mark='c'/> Therapy's "
            "effect seemed to outlast it, as if a skill had been learned. The drug's effect lasted while it was "
            "taken. <bookmark mark='d'/> It's one trial, with modest numbers, and later studies broadly agree that "
            "therapy lowers relapse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in b], lag_ratio=0.4))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
