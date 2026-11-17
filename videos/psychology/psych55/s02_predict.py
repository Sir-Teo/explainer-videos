from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"Retirement saving with automatic enrolment instead of opt-in: \ participation went from 37\% to?", PERSON),
    (r"2", r"A megastudy's best-looking intervention estimated at +7 points: \ what is its true effect, \ roughly?",
     MODEL),
    (r"3", r"Average published nudge: \ about 9 points. \ Average across government nudge-unit trials?", AUTH),
    (r"4", r"Contact from a campaign (canvassing, \ mail, \ ads) in a US general election: \ average persuasion "
           r"effect?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ five ways to the gym, \ and four numbers", r"Which nudge would you bet "
                     r"on?")
        self.rank()
        self.quiz()

    def rank(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        items = [r"a text reminder before each planned workout", r"bonus points for returning after a missed workout",
                 r"a message that most members go more than you", r"a pledge to go, \ signed",
                 r"a small cash reward per visit"]
        rows = VGroup(*[VGroup(label(rf"{chr(65 + i)}", font_size=26, color=PERSON),
                               wrapped_label(t, 6.4, 21, WHITE)).arrange(RIGHT, buff=0.35) for i, t in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.2, -0.2, 0])
        side = rows_of([
            (r"on the course site: \ rank five interventions from a gym megastudy, \ before seeing the results", WHITE),
            (r"then your ranking against the outcome, \ and against experts' forecasts", MODEL),
            (r"the descriptions are simplified versions of the kinds of arms tested", YOU),
        ], 4.2, 19, 0.36).move_to([4.6, -0.3, 0])
        with self.voiceover(
            "First, a bet. <bookmark mark='a'/> On the course site you'll rank five interventions to get people to the "
            "gym: a text reminder before each planned workout, bonus points for coming back after a missed one, a "
            "message that most members go more than you, a signed pledge, and a small cash reward per visit. "
            "<bookmark mark='b'/> Then you'll see your ranking against the outcome, and against experts' forecasts. "
            "<bookmark mark='c'/> The descriptions are simplified versions of the kinds of arms that were tested."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 21, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers. <bookmark mark='a'/> One: retirement saving with automatic enrolment instead of opting "
            "in. Participation went from thirty-seven percent to what? <bookmark mark='b'/> Two: a megastudy's "
            "best-looking intervention is estimated at plus seven points. What's its true effect, roughly? "
            "<bookmark mark='c'/> Three: the average published nudge moves behaviour about nine points. What's the "
            "average across government nudge-unit trials? <bookmark mark='d'/> And four: campaign contact in an "
            "American general election, by canvassing, mail or ads. What's its average persuasion effect? Pause "
            "here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
