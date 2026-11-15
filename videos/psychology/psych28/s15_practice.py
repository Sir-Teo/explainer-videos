from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.incentives()
        self.weight()
        self.habits()

    def card(self):
        card = chapter_card(14, r"In practice: \ incentives, \ diets and habits", r"Where does the science of "
                            r"motivation change what people do?",
                            lit={2000: r"Gneezy \& Rustichini", 2010: r"Lally et al.", 2011: r"Hall et al."},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: incentives, diets and habits."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def incentives(self):
        head = heading(r"Incentives that backfire, \ and ones that work")
        rows = rows_of([
            (r"Gneezy and Rustichini, \ 2000: \ ten day-care centres in Israel; \ six introduce a small fine for "
             r"parents who arrive late", WHITE),
            (r"late arrivals rose, \ and stayed high after the fine was removed: \ a moral obligation had become a "
             r"price", LOST),
            (r"incentives that work are large enough to matter, \ immediate, \ and attached to the behaviour "
             r"itself: \ cash for verified quitting in smoking-cessation trials", INTR),
            (r"gamification: \ points and badges change what people do while they last, \ and can teach that "
             r"the activity is only worth doing for points \ (chapter five)", EXTR),
            (r"incentive design at work: \ Part 53", MODEL),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Gneezy \& Rustichini (2000)")
        with self.voiceover(
            "Motivation is applied everywhere, often by people who've never read the research. "
            "<bookmark mark='a'/> In 2000 Uri Gneezy and Aldo Rustichini studied ten day-care centres in Israel. "
            "Six introduced a small fine for parents who picked their children up late. <bookmark mark='b'/> Late "
            "arrivals went up, not down, and stayed up after the fine was removed. A moral obligation to the staff "
            "had become a price, and a cheap one. <bookmark mark='c'/> Incentives that work tend to be large enough "
            "to matter, immediate, and attached to the behaviour itself. In smoking-cessation trials, money paid "
            "for verified quitting has raised quit rates. <bookmark mark='d'/> Gamification, points and badges and "
            "streaks, changes what people do while it lasts, and can teach them, as the markers did, that the "
            "activity is only worth doing for points. <bookmark mark='e'/> Incentive design at work returns in "
            "Part 53."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def weight(self):
        d = load("weight")
        head = heading(r"Weight-loss programmes, \ read as control")
        rows = rows_of([
            (r"the static rule overpromises: \ planners now use dynamic models of the loop, \ like Hall and "
             r"colleagues' \ (chapter two)", BODY),
            (rf"in the loop, \ a lasting change of intake moves weight to a new settling point, \ with a time "
             rf"constant near a year: \ {d['settle_tau']:.0f} days in Psyche's version", WHITE),
            (r"most diets lose weight for six months and regain over the next few years; \ the defended set point "
             r"is one reason", LOST),
            (r"what lasts is what changes the loop for good: \ the food around a person, \ habits, \ and, \ for "
             r"some, \ drugs that act on the hunger signals themselves", INTR),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Hall et al.\ (2011)")
        with self.voiceover(
            "Weight-loss programmes are motivation meeting control theory. <bookmark mark='a'/> The static rule "
            "overpromises, so planners now use dynamic models of the loop, like the one Kevin Hall and his "
            "colleagues published in 2011, which chapter two's model imitates. <bookmark mark='b'/> In the loop, a "
            "lasting change of intake moves weight to a new settling point, with a time constant near a year; "
            f"{d['settle_tau']:.0f} days in Psyche's version. <bookmark mark='c'/> Most diets lose weight for about "
            "six months, and the weight returns over the next few years. The defended set point is one reason. "
            "<bookmark mark='d'/> What lasts is what changes the loop for good: the food around a person, habits, "
            "and, for some, drugs that act on the hunger signals themselves, which is the newest chapter of this "
            "story."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def habits(self):
        head = heading(r"Habits: \ motivation you no longer need")
        rows = rows_of([
            (r"Lally and colleagues, \ 2010: \ volunteers chose a new daily habit, \ such as a walk or a glass of "
             r"water, \ and rated how automatic it felt each day", WHITE),
            (r"automaticity rose and levelled off, \ on average after a couple of months, \ with enormous variation "
             r"between people and habits", INTR),
            (r"a habit is an action triggered by a cue, \ no longer by its goal: \ Part 17's model-free values, "
             r"\ and the if-then plans of chapter six", BODY),
            (r"habit apps work best when they fix the cue and the moment; \ streaks and rewards help while they "
             r"last", EXTR),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Lally, \ van Jaarsveld, \ Potts \& Wardle (2010)")
        with self.voiceover(
            "And the last application is a way to need motivation less. <bookmark mark='a'/> In 2010 Phillippa "
            "Lally and her colleagues asked volunteers to choose a new daily habit, such as a walk or a glass of "
            "water with lunch, and to rate each day how automatic it felt. <bookmark mark='b'/> Automaticity rose "
            "and levelled off, on average after a couple of months, with enormous variation between people and "
            "between habits. <bookmark mark='c'/> A habit is an action triggered by a cue rather than by its goal: "
            "Part 17's cached, model-free values, and the if-then plans of chapter six. <bookmark mark='d'/> Habit "
            "apps work best when they fix the cue and the moment. Streaks and rewards help, for as long as they last."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
