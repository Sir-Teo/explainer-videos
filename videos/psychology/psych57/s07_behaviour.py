from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Behaviour(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"Behaviour is the treatment", r"What if the medicine is what people do?",
                     scale=("person", "society"))
        self.adherence()
        self.arithmetic()
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
