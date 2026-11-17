from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Behaviour(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"Behaviour is the treatment", r"What if the medicine is what people do?",
                     scale=("person", "society"))
        self.adherence()
        self.arithmetic()
        self.models()
        self.dpp()

    def adherence(self):
        rows_section(self, r"Adherence", [
            (r"the World Health Organization's 2003 report: \ in rich countries, \ adherence to long-term therapies "
             r"averages about 50\%", WHITE),
            (r"increasing adherence may have a far greater impact on health than any improvement in specific "
             r"treatments, \ the report argued", AUTH),
            (r"the reasons are Part 26's and Part 55's: \ costs now and benefits later, \ forgetting, \ side "
             r"effects, \ and doubt", MODEL),
            (r"what helps: \ simpler regimens, \ reminders, \ packaging, \ and asking about it without blame", GOOD),
        ], "What if the medicine is what people do? <bookmark mark='a'/> The World Health Organization's 2003 report "
           "found that in rich countries, adherence to long-term therapies averages about fifty percent. "
           "<bookmark mark='b'/> Increasing adherence, it argued, might do more for health than any improvement in "
           "specific treatments. <bookmark mark='c'/> The reasons are Part 26's and Part 55's: costs now and benefits "
           "later, forgetting, side effects, and doubt. <bookmark mark='d'/> What helps is simpler regimens, "
           "reminders, packaging, and asking about it without blame.")

    def models(self):
        head = heading(r"Models of health behaviour, \ and their records")
        stages = flow_chain([(r"not thinking of it", GREY_B), (r"thinking of it", CROWD), (r"preparing", MODEL),
                             (r"acting", GOOD), (r"keeping it up", PERSON)], box_w=2.25, box_h=0.8, buff=0.42,
                            font_size=19)
        stages.move_to([0, 2.1, 0])
        st_l = label(r"stages of change: \ Prochaska and DiClemente, \ 1983", font_size=18, color=GREY_A)
        st_l.next_to(stages, DOWN, buff=0.15)
        A = axes([-0.6, 1.6], [0, 0.8], x_length=3.6, y_length=2.4, xticks=[], yticks=[0, 0.4, 0.8],
                 yfmt=lambda v: f"{v:g}", ylabel=r"effect, \ $d$", center=[-4.3, -1.35, 0], font_size=16)
        b = bars(A.ax, [0, 1], [0.66, 0.36], [MODEL, GOOD], width=0.6)
        vals = VGroup(*[label(t, font_size=18, color=c).next_to(A.ax.c2p(x, v), UP, buff=0.08)
                        for x, v, t, c in ((0, 0.66, r"0.66", MODEL), (1, 0.36, r"0.36", GOOD))])
        names = VGroup(*[label(t, font_size=16, color=c).next_to(A.ax.c2p(x, 0), DOWN, buff=0.12)
                         for x, t, c in ((0, r"intention", MODEL), (1, r"behaviour", GOOD))])
        gap_l = label(r"the intention--behaviour gap", font_size=17, color=GREY_A).next_to(A, UP, buff=0.12)
        checks = verdict_row([
            (r"health belief model \ (Rosenstock, \ 1966): \ benefits and barriers predict best, \ perceived "
             r"risk weakly", "replicated, smaller"),
            (r"stage-matched help beats unmatched help \ (Bridle and colleagues, \ 2005: \ little evidence)",
             "failed"),
            (r"changing intentions changes behaviour, \ by about half as much \ (Webb and Sheeran, \ 2006)",
             "replicated"),
            (r"COM-B \ (Michie and colleagues, \ 2011): \ capability, \ opportunity, \ motivation: \ a "
             r"framework for designing", "not directly tested"),
        ], width=8.4, font_size=18)
        checks.move_to([2.2, -1.3, 0])
        tag = published_tag(r"Rosenstock (1966); \ Prochaska \& DiClemente (1983); \ Bridle et al.\ (2005); \ "
                            r"Webb \& Sheeran (2006); \ Michie et al.\ (2011)")
        with self.voiceover(
            "Why do people do, or not do, what would keep them well? Health psychology's textbooks answer with "
            "models. <bookmark mark='a'/> The oldest, the health belief model, came from Irwin Rosenstock and "
            "colleagues at the United States Public Health Service, puzzling over why so few people came for free "
            "screening for tuberculosis. People act, it says, when they believe they are at risk, that the illness "
            "is serious, that acting helps, and that the barriers are low. Reviews find that the benefits and the "
            "barriers predict best, and perceived risk only weakly. <bookmark mark='b'/> The theory of planned "
            "behaviour, from Part 35, puts intention at the centre. And the stages of change, from James Prochaska "
            "and Carlo DiClemente in 1983, said that people move from not thinking about a change, to thinking "
            "about it, preparing, acting and keeping it up, and that help should match the stage. "
            "<bookmark mark='c'/> It became one of the most used models in health promotion. But when Jonathan "
            "Bridle and colleagues reviewed the trials in 2005, help matched to the stage did little better than "
            "help that wasn't. <bookmark mark='d'/> Intentions do matter. In 2006 Thomas Webb and Paschal Sheeran "
            "pooled experiments that changed people's intentions and then measured what they did. A medium-to-large "
            "change in intention produced a change in behaviour about half as big. <bookmark mark='e'/> So the newer "
            "frameworks, like Susan Michie's COM-B, add what intentions leave out: whether people are able to act, "
            "and whether their surroundings let them. That is Part 55's lesson about nudges, from the other side."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(checks.rows[0], shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in stages.boxes], lag_ratio=0.25),
                      LaggedStart(*[GrowArrow(a_) for a_ in stages.arrows], lag_ratio=0.25), FadeIn(st_l),
                      run_time=2.2)
            vo.wait_until("c")
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(A), FadeIn(names), FadeIn(gap_l), GrowFromEdge(b[0], DOWN), FadeIn(vals[0]))
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(vals[1]), FadeIn(checks.rows[2], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(checks.rows[3], shift=RIGHT * 0.15))
        self.clear_scene()

    def dpp(self):
        head = heading(r"Preventing diabetes")
        A = axes([0.3, 3.7], [0, 12], x_length=5.0, y_length=3.0, xticks=None, yticks=[0, 4, 8, 12],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"new cases per 100 person-years", center=[-3.5, 0.3, 0],
                 font_size=12)
        vals = [11.0, 7.8, 4.8]
        b = bars(A.ax, [1, 2, 3], vals, [GREY_B, MODEL, GOOD], width=0.6)
        names = VGroup(*[label(s, font_size=13, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, s in enumerate([r"placebo", r"metformin", r"lifestyle"])])
        rows = rows_of([
            (r"the Diabetes Prevention Program, \ 2002: \ 3,234 adults at high risk, \ randomized to placebo, \ "
             r"metformin, \ or an intensive lifestyle programme", WHITE),
            (r"lifestyle: \ a goal of 7\% weight loss and 150 minutes of activity a week, \ with a coach and 16 "
             r"lessons", MODEL),
            (r"new cases fell by 58\% with lifestyle and 31\% with metformin, \ against placebo", GOOD),
            (r"weight returned for many over the following years (Part 28's set points and habits), \ but the "
             r"reduction in incidence partly persisted", PERSON),
        ], 6.2, 19, 0.36).move_to([3.3, -0.1, 0])
        tag = published_tag(r"Diabetes Prevention Program (2002)")
        with self.voiceover(
            "The clearest example is diabetes. <bookmark mark='a'/> In 2002 the Diabetes Prevention Program reported "
            "on three thousand two hundred adults at high risk, randomized to placebo, the drug metformin, or an "
            "intensive lifestyle programme. <bookmark mark='b'/> The lifestyle programme aimed at seven percent weight "
            "loss and a hundred and fifty minutes of activity a week, with a coach and sixteen lessons. "
            "<bookmark mark='c'/> New cases fell by fifty-eight percent with lifestyle and thirty-one percent with "
            "metformin, against placebo. <bookmark mark='d'/> Weight returned for many over the following years, "
            "Part 28's set points and habits, but the reduction in new cases partly persisted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def arithmetic(self):
        rows_section(self, r"Adherence, \ as arithmetic", [
            (r"illustrative: \ a drug that cuts the risk of a heart attack by 30\% in people who take it", WHITE),
            (r"if half of those prescribed it take it as directed, \ the risk falls by about 15\% across everyone "
             r"prescribed it", AUTH),
            (r"raising adherence from 50\% to 70\% would add as much benefit as a new drug 40\% stronger", GOOD),
            (r"what helps: \ simpler regimens (one pill a day), \ reminders, \ and the habit cues of Part 52; \ what "
             r"does not: \ information alone", MODEL),
            (r"so a behavioural trial of adherence can be worth more than a pharmacological one: \ the drug already "
             r"works", YOU),
        ], "Adherence is arithmetic. <bookmark mark='a'/> Take an illustrative drug that cuts the risk of a heart "
           "attack by thirty percent in the people who take it. <bookmark mark='b'/> If half of those prescribed it "
           "take it as directed, the risk falls by only about fifteen percent across everyone prescribed it. "
           "<bookmark mark='c'/> Raising adherence from fifty to seventy percent would add as much benefit as a new "
           "drug forty percent stronger. <bookmark mark='d'/> What helps is simpler regimens, one pill a day, "
           "reminders, and the habit cues of Part 52. What doesn't is information alone. <bookmark mark='e'/> So a "
           "behavioural trial of adherence can be worth more than a pharmacological one. The drug already works.")
