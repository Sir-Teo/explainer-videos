from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403


class Multitask(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Multitasking: \ what you pay for is what you get", r"When only some of a job can be "
             r"measured, \ what happens to the rest?", "Chapter seven. Multitasking: what you pay for is what you get.",
             lit={1975: r"Kerr's folly", 1991: r"Holmström and Milgrom", 2003: r"Jacob and Levitt"},
             scale=("person", "firm"), horizon=("a year",))
        self.teacher()
        self.curves()
        self.design()
        self.called()

    def teacher(self):
        rows = VGroup(
            label(r"a teacher has two tasks", font_size=28),
            label(r"drilling for the test: \ measured, \ by the scores", font_size=25, color=SIGNAL),
            label(r"teaching what the test can't see: \ understanding, \ curiosity, \ the subject itself",
                  font_size=25, color=EFFORT),
            label(r"both come out of the same hours and the same energy", font_size=25, color=RISK),
            label(r"pay the teacher for scores: \ what happens to the second task?", font_size=27, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Holmström and Milgrom, JLEO 7 (1991)", corner=DR, font_size=13)
        with self.voiceover(
            "Most jobs are more than one task. <bookmark mark='a'/> Take a teacher, with two. "
            "<bookmark mark='b'/> One is drilling for the test, which is measured, by the scores. "
            "<bookmark mark='c'/> The other is teaching what the test can't see: understanding, curiosity, the "
            "subject itself. <bookmark mark='d'/> Both come out of the same hours and the same energy, so more of "
            "one makes the other more costly. <bookmark mark='e'/> Now pay the teacher a bonus for test scores. In "
            "1991 Bengt Holmström and Paul Milgrom worked out what happens to the second task."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def curves(self):
        m = load("multitask")
        bs, e1, e2 = np.array(m["beta"]), np.array(m["e1"]), np.array(m["e2"])
        ax = plane([0, 2], [0, 3.6], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[0, 0.5, 1, 1.5, 2], yticks=[0, 1, 2, 3], xlabel=r"bonus per point of test score",
                   ylabel=r"effort", font_size=16, xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        c1 = path(ax, bs, e1, color=SIGNAL, width=3.5, smooth=False)
        c2 = path(ax, bs, e2, color=EFFORT, width=3.5, smooth=False)
        l1 = label(r"drilling for the test", font_size=16, color=SIGNAL).next_to(a.c2p(1.2, e1[48]), UL, buff=0.1)
        l2 = label(r"teaching the rest", font_size=16, color=EFFORT).move_to(a.c2p(0.62, 0.62))
        k = int(np.argmin(np.abs(bs - m["drop_at"])))
        drop = Dot(a.c2p(bs[k], 0), radius=0.08, color=RISK)
        dl = label(r"the rest is dropped", font_size=15, color=RISK).next_to(drop, UP, buff=0.15).shift(RIGHT * 0.4)
        side = VGroup(
            label(r"no bonus: \ both tasks, \ out of a sense of the job", font_size=21),
            label(r"as the bonus grows, \ effort moves to the test", font_size=21, color=SIGNAL),
            label(r"and away from everything else", font_size=21, color=EFFORT),
            label(r"until the rest is dropped altogether", font_size=21, color=RISK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is Agora's teacher. <bookmark mark='a'/> With no bonus, the teacher does some of both, out of a "
            "sense of what the job is. <bookmark mark='b'/> As the bonus per point grows, effort moves to the test. "
            "<bookmark mark='c'/> And because both tasks draw on the same hours, it moves away from everything else. "
            "<bookmark mark='d'/> Past a point the rest is dropped altogether. The scores rise, and the measure says "
            "the teacher is doing better. What the measure can't see has gone."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]),
                      FadeIn(Dot(a.c2p(0, e1[0]), radius=0.07, color=WHITE)))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(l1), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(l2), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(drop, scale=1.5), FadeIn(dl), FadeIn(side[3]))
        self.clear_scene()

    def design(self):
        rows = VGroup(
            label(r"when the measure misses much of the job, \ weak incentives can be best: \ even none", font_size=24,
                  color=E.ACCENT),
            label(r"why teachers, \ civil servants and judges are mostly paid flat salaries", font_size=23),
            label(r"design the job: \ put the tasks that are easy to measure in one job, \ the rest in another",
                  font_size=23, color=SIGNAL),
            label(r"and owning the tools sharpens incentives too: \ the contractor who owns the van, \ the employee "
                  r"who doesn't", font_size=22, color=PAY),
            label(r"Steven Kerr, \ 1975: \ ``On the folly of rewarding A, \ while hoping for B''", font_size=23,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Holmström and Milgrom, JLEO 7 (1991); \ Kerr, Academy of Management Journal 18(4) "
                            r"(1975)", corner=DR, font_size=13)
        with self.voiceover(
            "Holmström and Milgrom drew three lessons. <bookmark mark='a'/> First, when the measure misses much of "
            "the job, weak incentives can be best, and sometimes none at all. A flat salary at least leaves the "
            "tasks in balance. <bookmark mark='b'/> It is one reason teachers, civil servants and judges are mostly "
            "paid flat salaries. <bookmark mark='c'/> Second, design the job, not just the pay: put the tasks that "
            "are easy to measure together, and give them strong incentives, and put the rest in another job. "
            "<bookmark mark='d'/> Third, owning the tools is an incentive too, for their upkeep, which is hard to "
            "measure. A contractor who owns the van and is paid by the job takes care of it; an employee driving the "
            "firm's van on a salary has less reason to, which ties back to part eight's theory of the firm. "
            "<bookmark mark='e'/> Sixteen years earlier, a management scholar, Steven Kerr, had put the problem in a "
            "title: on the folly of rewarding A, while hoping for B."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["multitask_tests"]
        jl = tables.INCENTIVE_CASES.data["jacob_levitt"]
        cc = call_card(r"Holmström and Milgrom", c.when,
                       r"strong pay for what is measured \ pulls effort away from what isn't; \ where measures are "
                       r"narrow, \ incentives should be weak",
                       rf"after Chicago tied schools' fates to test scores, \ Jacob and Levitt found serious cheating "
                       rf"by teachers or staff \ in at least {100 * jl:.0f} to 5\% of elementary classrooms a year",
                       c.verdict, width=12.4, font_size=23).move_to(UP * 0.6)
        q = label(r"the measure became the task: \ effort went into the score itself", font_size=24,
                  color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Jacob and Levitt, QJE 118(3) (2003)", corner=DR, font_size=13)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> Holmström and Milgrom said that strong pay for what is measured pulls "
            "effort away from what isn't, and that where measures are narrow, incentives should be weak. "
            "<bookmark mark='b'/> In the 1990s Chicago's schools tied a great deal to test scores. Brian Jacob and "
            "Steven Levitt went looking for answer sheets with suspicious patterns: whole runs of hard questions "
            "right, in classes that got easy ones wrong. They found serious cheating by teachers or administrators in "
            "at least four to five percent of elementary classrooms each year. <bookmark mark='c'/> Right. And the "
            "most extreme form of it: effort went into the score itself."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3), FadeIn(q))
        self.clear_scene()
