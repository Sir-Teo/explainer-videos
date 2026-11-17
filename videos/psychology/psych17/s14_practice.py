from __future__ import annotations

from videos.psychology.psych17.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.recommenders()
        self.medication()
        self.design()

    def card(self):
        card = chapter_card(13, r"In practice: \ recommenders, \ medicine, \ habits",
                            r"Where does this mathematics run your life?",
                            lit={2010: r"Li et al.; \ Weintraub et al."}, part=PART, scale=("person", "group"),
                            marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: recommenders, medicine, habits."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def recommenders(self):
        head = heading(r"You are the bandit's arm")
        rows = rows_of([
            (r"a news page, \ a shop, \ a video feed: \ which item to show this person, \ now?", WHITE),
            (r"each click is a reward; \ each item an arm; \ explore new items, \ exploit known favourites", REWARD),
            (r"2010: \ a contextual bandit chooses Yahoo!'s front-page stories, \ and lifts clicks over plain "
             r"exploitation", DELTA),
            (r"bandit tests now replace many fixed A/B tests: \ traffic shifts to the winner while the test runs", CUE),
            (r"but a system that learns from clicks also shapes what people come to click", INHIB),
        ], 6.4, 25, 0.4).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        d = load("abtest")
        sh = d["share"]
        A = axes([0, 20], [0, 1], x_length=5.0, y_length=3.0, xticks=[0, 10, 20], yticks=[0, 0.5, 1],
                 xlabel=r"visitors, \ thousands", ylabel=r"share shown the better version", center=[3.7, 0.5, 0],
                 font_size=17)
        ax = A.ax
        even = DashedLine(ax.c2p(0, 0.5), ax.c2p(20, 0.5), color=GREY_B, stroke_width=2)
        el = label(r"a fixed A/B test: \ half and half to the end", font_size=17, color=GREY_B).next_to(
            ax.c2p(20, 0.5), DOWN, buff=0.12).align_to(ax.c2p(20, 0), RIGHT)
        bars = VGroup()
        for k, v in enumerate(sh):
            lo, hi = ax.c2p(k + 0.5, 0), ax.c2p(k + 0.5, v)
            bars.add(Rectangle(width=0.17, height=hi[1] - lo[1], stroke_width=0, fill_color=CUE, fill_opacity=0.85)
                     .move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
        res = label(rf"clicks: \ {num(round(d['clicks_thompson']))} against {num(round(d['clicks_even']))} "
                    rf"for the even split", font_size=18, color=CUE).next_to(A, DOWN, buff=0.15)
        ptag = psyche_tag(r"Psyche: \ Thompson sampling, \ versions clicked 5\% and 6\%, \ 50 runs")
        tag = published_tag(archive.LI_2010.cite)
        with self.voiceover(
            "The mathematics of this part runs much of the internet. <bookmark mark='a'/> A news site, a shop or a "
            "video feed faces a bandit problem with every visitor: which item to show this person, now. "
            "<bookmark mark='b'/> A click is a reward, each item is an arm, and the system must explore new items "
            "while exploiting known favourites. <bookmark mark='c'/> In 2010 Lihong Li and colleagues at Yahoo! "
            "showed that a contextual bandit, one that uses what it knows about the visitor, chose front-page stories "
            "that drew more clicks than a system that only exploited. <bookmark mark='d'/> Bandit tests now replace "
            "many fixed A/B tests: instead of splitting traffic evenly to the end, they shift visitors toward the "
            "better version while the test runs. On two versions clicked five and six percent of the time, a "
            "Thompson sampler sends most visitors to the better one within a few thousand, and collects about "
            "seventy more clicks in twenty thousand visits than an even split. <bookmark mark='e'/> There's a catch that psychologists should "
            "notice. A system that learns from your clicks also changes what you'll click next. The learner and the "
            "learned-about are training each other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "d":
                    self.play(Create(even), FadeIn(el), FadeIn(ptag))
                    self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=3.0)
                    self.play(FadeIn(res))
        self.clear_scene()

    def medication(self):
        p = archive.WEINTRAUB_2010.data
        head = heading(r"A side effect the theory predicts")
        rows = rows_of([
            (r"Parkinson's disease is treated by restoring dopamine: \ levodopa, \ or drugs that mimic it", WHITE),
            (r"dopamine agonists stimulate D2-type receptors continuously, \ whatever the outcome", DELTA),
            (rf"{num(p['patients'])} patients surveyed: \ {p['any']}\% had an impulse-control disorder; \ "
             rf"{p['agonist']}\% of those on agonists, \ {p['levodopa']}\% on levodopa alone", INHIB),
            (r"gambling, \ shopping, \ binge eating, \ compulsive sex: \ often new, \ often hidden from doctors",
             REWARD),
            (r"a reinforcement signal that no longer tracks outcomes; \ doctors now warn patients and families", YOU),
        ], 6.4, 25, 0.4).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        A = axes([0, 3], [0, 20], x_length=4.6, y_length=3.2, xticks=[], yticks=[0, 10, 20], yfmt=lambda v: f"{v:g}\\%",
                 ylabel=r"with an impulse-control disorder", center=[3.8, 0.55, 0], font_size=17)
        ax = A.ax
        bars, labs = VGroup(), VGroup()
        for k, (key, name, col) in enumerate([("any", r"all patients", DATA), ("agonist", r"on an agonist", INHIB),
                                              ("levodopa", r"levodopa alone", GREY_B)]):
            lo, hi = ax.c2p(k + 0.5, 0), ax.c2p(k + 0.5, p[key])
            b = Rectangle(width=0.8, height=hi[1] - lo[1], stroke_width=0, fill_color=col, fill_opacity=0.85)
            bars.add(b.move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
            labs.add(VGroup(label(rf"{p[key]}\%", font_size=19, color=col).next_to(hi, UP, buff=0.08),
                            label(name, font_size=17, color=col).next_to(lo, DOWN, buff=0.15)))
        tag = published_tag(archive.WEINTRAUB_2010.cite)
        with self.voiceover(
            "The second application is in medicine, and it's a warning. <bookmark mark='a'/> Parkinson's disease kills "
            "dopamine neurons, and it's treated by restoring dopamine: with levodopa, its precursor, or with drugs "
            "called agonists that mimic it. <bookmark mark='b'/> Agonists stimulate dopamine receptors steadily, "
            "whatever happens. <bookmark mark='c'/> In 2010 Daniel Weintraub and colleagues surveyed more than three "
            "thousand patients. About one in seven had an impulse-control disorder, and among those taking agonists, "
            "about one in six, compared with one in fifteen on levodopa alone. <bookmark mark='d'/> Pathological "
            "gambling, compulsive shopping, binge eating, compulsive sexual behaviour: often new since treatment, and "
            "often hidden from doctors. <bookmark mark='e'/> One reading is a reinforcement signal that no longer "
            "tracks outcomes, so that a loss doesn't teach as it should. Patients and families are now warned to watch "
            "for it, and the drugs adjusted when it appears."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "c":
                    self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(labs),
                              run_time=2.0)
        self.clear_scene()

    def design(self):
        head = heading(r"Habits, \ by design")
        rows = rows_of([
            (r"a habit is a cached value: \ cheap, \ fast, \ and slow to notice when the outcome changes", MF),
            (r"so breaking one rarely works by reasoning alone: \ the cached value has not heard the argument", INHIB),
            (r"what works: \ change the cues and the context, \ the triggers that call up the cached action", CUE),
            (r"and building one: \ the same cue, \ the same action, \ reliably rewarded, \ for a long time", DELTA),
            (r"apps that reward unpredictably, \ streaks and badges: \ the same tools, \ aimed the other way; \ "
             r"Part 52", GREY_A),
        ], 12.4, 28, 0.38).move_to([0, -0.1, 0])
        with self.voiceover(
            "And the theory says something about everyday habits. <bookmark mark='a'/> A habit is a cached value: "
            "cheap and fast, and slow to notice when the outcome has changed, like the overtrained rats pressing for "
            "pellets they no longer want. <bookmark mark='b'/> That's why breaking a habit rarely works by reasoning "
            "alone. The cached value hasn't heard the argument. <bookmark mark='c'/> What tends to work is changing "
            "the cues and the context that call up the action: the phone left in another room. "
            "<bookmark mark='d'/> Building a habit is the same in reverse: the same cue, the same action, reliably "
            "rewarded, for a long time. <bookmark mark='e'/> Apps that reward unpredictably, with streaks and badges, "
            "use the same tools aimed the other way. Part 52 is about designing for minds."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
