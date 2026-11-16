from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403


class Selection(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"Choosing a treatment", r"Can data say which treatment suits which person?")
        self.pai()
        self.sample()
        self.alternatives()

    def pai(self):
        rows_section(self, r"The personalized advantage index", [
            (r"DeRubeis and colleagues, \ 2014: \ in a trial of cognitive therapy against antidepressants, \ fit a "
             r"model of each patient's outcome under each treatment", WHITE),
            (r"the index: \ predicted outcome under one minus under the other; \ a patient's predicted advantage", MODEL),
            (r"most patients had small predicted advantages; \ for a minority, \ the predicted difference was "
             r"clinically meaningful", PERSON),
            (r"the test that matters: \ randomize patients to treatment chosen by the index or as usual, \ and "
             r"compare", GOOD),
        ], "Can data say which treatment suits which person? <bookmark mark='a'/> In 2014 Robert DeRubeis and "
           "colleagues took a trial of cognitive therapy against antidepressants, and fitted a model of each "
           "patient's outcome under each treatment. <bookmark mark='b'/> The index is the predicted outcome under one "
           "treatment minus that under the other: a patient's predicted advantage. <bookmark mark='c'/> Most patients "
           "had small predicted advantages. For a minority, the predicted difference was clinically meaningful. "
           "<bookmark mark='d'/> The test that matters is to randomize patients to treatment chosen by the index, or "
           "as usual, and compare.", tag=published_tag(r"DeRubeis et al.\ (2014)"))

    def sample(self):
        d = load("pai")
        head = heading(r"What it costs to show a rule works")
        A = axes([0.12, 0.58], [0, 3300], x_length=5.6, y_length=3.2, xticks=[0.2, 0.3, 0.4, 0.5],
                 yticks=[0, 1000, 2000, 3000], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"),
                 xlabel=r"effect size", ylabel=r"patients needed", center=[-3.3, 0.2, 0], font_size=12)
        x = np.asarray(d["d"])
        bm = bars(A.ax, x - 0.022, d["main"], CROWD, width=0.04)
        bi = bars(A.ax, x + 0.022, d["inter"], AUTH, width=0.04)
        key = VGroup(label(r"a treatment works", font_size=13, color=CROWD),
                     label(r"a choice rule works", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.2)
        i3 = int(np.argmin(abs(x - 0.3)))
        rows = rows_of([
            (r"a choice rule helps only if treatments work differently for different people: \ a treatment-by-"
             r"moderator interaction", WHITE),
            (rf"to show a main effect of size 0.3: \ about {num(round(d['main'][i3], -1))} patients, \ 80\% power", CROWD),
            (rf"an interaction of the same size: \ four times as many, \ about {num(round(d['inter'][i3], -1))}; \ "
             rf"your fourth number", AUTH),
            (r"and real interactions are usually smaller than main effects: \ few trials are big enough", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{precision.pai\_sample}")
        with self.voiceover(
            "What does it cost to show that a choice rule works? <bookmark mark='a'/> A rule helps only if treatments "
            "work differently for different people. Statistically, that's an interaction between treatment and a "
            "moderator. <bookmark mark='b'/> To show a main effect of size zero point three takes about three "
            "hundred and fifty patients, at eighty percent power. <bookmark mark='c'/> An interaction of the same "
            "size takes four times as many, about fourteen hundred. That's your fourth number. <bookmark mark='d'/> "
            "And real interactions are usually smaller than main effects, so few trials are big enough."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bm], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bi], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def alternatives(self):
        chips_section(self, r"What works while we wait", [
            (r"measurement-based care", r"measure symptoms every visit and change treatment when progress stalls "
                                        r"(Part 57's feedback)", GOOD),
            (r"stepped care", r"start with the least intensive treatment that may work; \ step up the "
                              r"non-responders", CARE),
            (r"shared decisions", r"patients' preferences and side effects are information a model does not have", PERSON),
            (r"sequential trials", r"randomize again at each step (SMART designs) to learn which next step is best",
             MODEL),
        ], "What works while we wait? <bookmark mark='a'/> Measurement-based care: measure symptoms every visit, and "
           "change treatment when progress stalls. That's Part 57's feedback. <bookmark mark='b'/> Stepped care: start "
           "with the least intensive treatment that may work, and step up those who don't respond. "
           "<bookmark mark='c'/> Shared decisions: patients' preferences and side effects are information a model "
           "doesn't have. <bookmark mark='d'/> And sequential trials, which randomize again at each step, the designs "
           "called SMART, to learn which next step is best.")
