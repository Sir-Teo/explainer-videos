from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Habit(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"Habit and attention by design", r"Can a product be designed to be hard to put down?",
                     scale=("person", "society"))
        self.days()
        self.schedules()
        self.dark()

    def days(self):
        d = load("habit")
        head = heading(r"How long does a habit take?")
        A = axes([0, 200], [0, 105], x_length=5.6, y_length=3.0, xticks=[21, 66, 100, 150, 200], yticks=[0, 50, 100],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"days of daily repetition",
                 ylabel=r"automaticity", center=[-3.3, 0.3, 0], font_size=12)
        c = curve(A.ax, d["days"], d["curve"], GOOD, stroke_width=4)
        v21 = DashedLine(A.ax.c2p(21, 0), A.ax.c2p(21, 100), color=AUTH)
        ticks = VGroup(*[Line(A.ax.c2p(min(p, 199), 0), A.ax.c2p(min(p, 199), 6), color=PERSON, stroke_width=2)
                         for p in d["people"]])
        rows = rows_of([
            (r"the ``21 days'' claim traces to a 1960 self-help book's remark about patients adjusting to surgery", AUTH),
            (r"Lally and colleagues, \ 2010: \ 96 people repeated a chosen daily behaviour and rated its automaticity "
             r"for twelve weeks", WHITE),
            (r"automaticity rose and levelled off, \ reaching 95\% of its plateau after a median of 66 days, \ with a "
             r"range from 18 to 254", GOOD),
            (rf"Psyche's 96 people, \ drawn around that median: \ {100 * d['share_21']:.0f}\% within 21 days; \ a "
             rf"missed day did not reset the curve", PERSON),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.habit\_curve}, \ \texttt{habit\_people}")
        tag2 = published_tag(r"Lally et al.\ (2010)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "How long does a habit take? <bookmark mark='a'/> The popular answer, twenty-one days, traces back to a "
            "self-help book of 1960 and a remark about patients adjusting after surgery. <bookmark mark='b'/> In 2010 "
            "Phillippa Lally and colleagues had ninety-six people repeat a daily behaviour of their choice and rate "
            "how automatic it felt, for twelve weeks. <bookmark mark='c'/> Automaticity rose and levelled off. It "
            "reached ninety-five percent of its plateau after a median of sixty-six days, with a range from eighteen to "
            "two hundred and fifty-four. <bookmark mark='d'/> Among ninety-six of Psyche's people drawn around that "
            "median, about one in twenty gets there within twenty-one days. And in the study, missing a day didn't "
            "reset the curve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(v21))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(c))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(ticks))
        self.clear_scene()

    def schedules(self):
        rows_section(self, r"Part 16's schedules, \ in your pocket", [
            (r"a variable-ratio schedule, \ a reward after an unpredictable number of responses, \ gives high, \ steady "
             r"responding that is slow to extinguish", WHITE),
            (r"pull to refresh, \ a feed that sometimes holds something good, \ notifications at random moments: \ "
             r"the same schedule", AUTH),
            (r"Part 17's prediction errors: \ the uncertain reward keeps the dopamine signal alive", MODEL),
            (r"whether this amounts to addiction is contested; \ that it is designed to hold attention is not", YOU),
        ], "Part 16's schedules are in your pocket. <bookmark mark='a'/> A variable-ratio schedule, a reward after an "
           "unpredictable number of responses, gives high, steady responding that is slow to extinguish. "
           "<bookmark mark='b'/> Pull to refresh, a feed that sometimes holds something good, and notifications at "
           "random moments are the same schedule. <bookmark mark='c'/> Part 17's prediction errors explain why: an "
           "uncertain reward keeps the signal alive. <bookmark mark='d'/> Whether this amounts to addiction is "
           "contested. That it's designed to hold attention is not.")

    def dark(self):
        chips_section(self, r"Dark patterns", [
            (r"the catalogue", r"Mathur and colleagues, \ 2019: \ a crawl of about 11,000 shopping sites found dark "
                               r"patterns on over a tenth of them", AUTH),
            (r"how they work", r"false urgency and scarcity, \ hidden costs, \ pre-ticked boxes, \ confirm-shaming, \ "
                               r"cancellation made hard", PERSON),
            (r"the psychology", r"Part 26's defaults and loss aversion, \ Part 34's social proof, \ turned against the "
                                r"user", MODEL),
            (r"the response", r"regulators now name several of them as unfair; \ a designer can audit their own flows "
                              r"for each", GOOD),
        ], "The darker end has a name. <bookmark mark='a'/> In 2019 Arunesh Mathur and colleagues crawled about eleven "
           "thousand shopping sites and found dark patterns on more than a tenth of them. <bookmark mark='b'/> False "
           "urgency and scarcity, hidden costs, pre-ticked boxes, confirm-shaming, and cancellation made hard. "
           "<bookmark mark='c'/> The psychology is the series' own: Part 26's defaults and loss aversion, and Part "
           "34's social proof, turned against the user. <bookmark mark='d'/> Regulators now name several of them as "
           "unfair, and a designer can audit their own flows for each one.", chip_w=3.4, text_w=8.8)
