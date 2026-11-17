from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.spent()
        self.machines()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ what is spent, \ and machines that want", r"What is open?",
                            lit={2013: r"Kurzban et al.", 2022: r"Agrawal et al."},
                            part=PART, scale=("mind", "brain"), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: what is spent, and machines that want."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def spent(self):
        head = heading(r"If not a resource, \ what?")
        rows = rows_of([
            (r"opportunity cost: \ effort and boredom as the brain's estimate of the value of doing something "
             r"else", WANT),
            (r"Agrawal, \ Mattar, \ Cohen and Daw, \ 2022: \ a model in which fatigue and boredom both follow from "
             r"tracking that value over time", INTR),
            (r"learning what is worth trying: \ people adjust effort to what effort has paid in the past, \ and "
             r"may learn to find it rewarding", BODY),
            (r"what nobody can yet do: \ measure the cost of effort in the brain, \ in units a model can use, \ "
             r"and predict who will persist", LOST),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Kurzban et al.\ (2013); \ Agrawal et al.\ (2022)")
        with self.voiceover(
            "If self-control isn't a resource, what is spent? <bookmark mark='a'/> The leading answer is "
            "opportunity cost: the feeling of effort, and of boredom, as the brain's estimate of the value of doing "
            "something else. <bookmark mark='b'/> In 2022 Mayank Agrawal, Marcelo Mattar, Jonathan Cohen and "
            "Nathaniel Daw built a model in which both fatigue and boredom follow from tracking that value as time "
            "passes. <bookmark mark='c'/> A related idea is that effort's price is learned. People adjust how hard "
            "they try to what trying has paid before, and may even come to find effort rewarding. "
            "<bookmark mark='d'/> What nobody can yet do is measure the cost of effort in the brain, in units a "
            "model can use, and from it predict who will persist."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def machines(self):
        head = heading(r"Motivation in artificial agents")
        rows = rows_of([
            (r"a reinforcement learner wants exactly its reward: \ Olds and Milner's rat is the oldest picture of "
             r"what goes wrong when the reward signal can be reached directly", LOST),
            (r"reward hacking: \ agents that find a way to score without doing the task", EXTR),
            (r"curiosity for machines: \ rewards for prediction error or learning progress \ (Schmidhuber, \ "
             r"1991; \ Pathak et al., \ 2017) \ make agents explore", INTR),
            (r"homeostatic agents: \ rewards for keeping internal variables in range, \ a body for the learner",
             BODY),
            (r"the open question is shared: \ what should a system want, \ and how do you stop it wanting the "
             r"measure instead \ (Part 60)", WHITE),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Schmidhuber (1991); \ Pathak et al.\ (2017)")
        with self.voiceover(
            "Motivation is also an engineering problem now. <bookmark mark='a'/> A reinforcement learner wants "
            "exactly its reward, and Olds and Milner's rat is the oldest picture of what goes wrong when the reward "
            "signal can be reached directly. <bookmark mark='b'/> In artificial agents it's called reward hacking: "
            "finding a way to score without doing the task. <bookmark mark='c'/> Curiosity has been built into "
            "machines, as rewards for prediction error or for learning progress, from Jürgen Schmidhuber's work in "
            "1991 to Deepak Pathak and colleagues' in 2017, and it makes agents explore. <bookmark mark='d'/> And "
            "some researchers give agents homeostatic rewards, for keeping internal variables in range: a body for "
            "the learner. <bookmark mark='e'/> The open question is shared by psychology and engineering: what "
            "should a system want, and how do you stop it wanting the measure instead? Part 60 returns to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_(self):
        head = heading(r"Open problems")
        rows = rows_of([
            (r"is wanting one system or many: \ does dopamine's incentive salience explain motivation for "
             r"food, \ money, \ people and ideas alike?", WANT),
            (r"what in the brain sets the defended weight, \ and why does it defend loss more than gain?", BODY),
            (r"can self-control be measured reliably in one person at all \ (the reliability paradox, \ Part 59)?",
             CTRL),
            (r"which motivational interventions survive registered, \ large tests, \ and for whom?", INTR),
        ], 12.2, 27, 0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "Four open problems. <bookmark mark='a'/> Is wanting one system or many? Does dopamine's incentive "
            "salience explain motivation for food, money, people and ideas alike? <bookmark mark='b'/> What in the "
            "brain sets a defended body weight, and why does it defend against loss more than gain? "
            "<bookmark mark='c'/> Can self-control be measured reliably in one person at all? The tasks that show "
            "strong effects across people are often poor at ranking individuals, the reliability paradox of Part "
            "59. <bookmark mark='d'/> And which motivational interventions survive large, registered tests, and for "
            "whom?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
