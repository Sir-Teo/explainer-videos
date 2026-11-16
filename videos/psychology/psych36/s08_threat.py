from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


class Threat(VoiceoverScene):
    def construct(self):
        self.card()
        self.original()
        self.adjusted()
        self.literature()

    def card(self):
        card = chapter_card(7, r"Stereotype threat", r"Can a stereotype lower a test score?",
                            lit={1995: r"Steele \& Aronson", 2004: r"Sackett et al.", 2018: r"Flore et al."},
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter seven. Stereotype threat."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def original(self):
        head = heading(r"A test called diagnostic")
        rows = rows_of([
            (r"Steele and Aronson, \ 1995: \ Black and white Stanford students took a hard verbal test", WHITE),
            (r"for some, \ it was described as diagnostic of intellectual ability; \ for others, \ as a laboratory "
             r"problem-solving task", CROWD),
            (r"Black students did worse when the test was called diagnostic", AUTH),
            (r"the idea: \ the fear of confirming a stereotype about your group is itself a load on performance; \ "
             r"it became one of the most cited findings in social psychology, \ and a basis for educational "
             r"interventions", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = historical_tag(r"Steele \& Aronson (1995)")
        with self.voiceover(
            "If stereotypes shape how others treat people, can they also shape how people perform? "
            "<bookmark mark='a'/> In 1995 Claude Steele and Joshua Aronson gave Black and white Stanford students a "
            "hard verbal test. <bookmark mark='b'/> For some it was described as diagnostic of intellectual ability. "
            "For others, as a laboratory problem-solving task. <bookmark mark='c'/> Black students did worse when "
            "the test was called diagnostic. <bookmark mark='d'/> The idea was that the fear of confirming a "
            "stereotype about your group is itself a load on performance. It became one of the most cited findings "
            "in social psychology, and a basis for educational interventions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def adjusted(self):
        head = heading(r"What the adjustment hid")
        A = axes([-0.6, 1.6], [0, 1.0], x_length=4.6, y_length=3.4, xticks=None, yticks=None,
                 ylabel=r"test score", center=[-3.7, -0.3, 0], font_size=15)
        raw = bars(A.ax, [-0.15, 0.85], [0.75, 0.75], [IN, IN], width=0.28)
        raw2 = bars(A.ax, [0.15, 1.15], [0.58, 0.40], [OUTG, OUTG], width=0.28)
        names = VGroup(label(r"not diagnostic", font_size=15, color=GREY_A).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       label(r"diagnostic", font_size=15, color=GREY_A).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15))
        key = legend([(IN, r"white students"), (OUTG, r"Black students")], font_size=14).move_to(A.ax.c2p(0.5, 0.95))
        note = label(r"the pattern reported, \ drawn schematically", font_size=14, color=GREY_B).next_to(A, DOWN,
                                                                                                    buff=0.45)
        rows = rows_of([
            (r"the published scores were adjusted for each student's earlier SAT score", WHITE),
            (r"Sackett, \ Hardison and Cullen, \ 2004: \ so even without the threat, \ the gap between the groups was "
             r"about what their SAT scores predicted; \ the adjustment had removed it from the picture", CROWD),
            (r"many textbooks and articles described the result as removing the threat removing the gap; \ "
             r"the study never claimed that", AUTH),
            (r"Part 3's lesson: \ an adjusted comparison answers a narrower question than it seems to", YOU),
        ], 6.2, 20, 0.36).move_to([3.2, -0.3, 0])
        tag = historical_tag(r"Sackett, \ Hardison \& Cullen (2004)")
        with self.voiceover(
            "How the result was reported matters. <bookmark mark='a'/> The published scores were adjusted for each "
            "student's earlier SAT score. <bookmark mark='b'/> In 2004 Paul Sackett and colleagues pointed out what "
            "that means. Even without the threat, the gap between the groups was about what their SAT scores "
            "predicted. The adjustment had taken it out of the picture. <bookmark mark='c'/> Many textbooks and "
            "articles described the result as removing the threat removing the gap. The study never claimed that. "
            "<bookmark mark='d'/> An adjusted comparison answers a narrower question than it seems to."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(key), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), *[GrowFromEdge(b_, DOWN) for b_ in raw])
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[GrowFromEdge(b_, DOWN) for b_ in raw2])
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def literature(self):
        d = load("threat")
        head = heading(r"Many small studies, \ one large one")
        A = axes([-0.8, 1.4], [0, 0.42], x_length=5.4, y_length=3.4, xticks=[-0.5, 0, 0.5, 1.0], yticks=[0, 0.2, 0.4],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"estimated effect, \ $d$",
                 ylabel=r"standard error", center=[-3.2, -0.3, 0], font_size=15)
        est, se, pub = np.asarray(d["est"], float), np.asarray(d["se"], float), np.asarray(d["published"], bool)
        jitter = 0.012 * np.sin(np.arange(len(se)) * 2.3)
        hidden = scatter(A.ax, est[~pub], se[~pub] + jitter[~pub], GREY_D, radius=0.05, opacity=0.6)
        shown = scatter(A.ax, est[pub], se[pub] + jitter[pub], AUTH, radius=0.06)
        big = Dot(A.ax.c2p(d["big_est"], d["big_se"]), radius=0.1, color=GOOD)
        bl = label(r"one large study", font_size=15, color=GOOD).next_to(big, RIGHT, buff=0.1)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, 0.42), color=GREY_B)
        rows = rows_of([
            (rf"Psyche: \ 60 laboratories test a true effect of zero with 25 people per group; \ the significant "
             rf"ones, \ and a few others, \ are published: \ {d['n_published']} studies", WHITE),
            (rf"pooled, \ the published studies say $d = {d['pooled']:.2f}$", AUTH),
            (r"Flore, \ Mulder and Wicherts, \ 2018: \ a registered study of 2{,}064 Dutch pupils, \ with "
             r"moderators set in advance: \ no effect of stereotype threat on girls' maths scores", GOOD),
            (r"the literature showed signs of publication bias; \ the effect may exist in some settings, \ but "
             r"registered tests have not found it", YOU),
        ], 6.0, 19, 0.34).move_to([3.4, -0.3, 0])
        tag = psyche_tag(r"simulated literature; \ Flore, \ Mulder \& Wicherts (2018)")
        with self.voiceover(
            "Then came the replications. <bookmark mark='a'/> First, what a filtered literature looks like. Psyche "
            "has sixty laboratories test an effect that is really zero, with twenty-five people per group. The "
            "significant ones, and a few others, get published. <bookmark mark='b'/> Pooled, the published studies "
            "say there's a sizeable effect. <bookmark mark='c'/> In 2018 Paulette Flore, Joris Mulder and Jelte "
            "Wicherts ran a registered study of more than two thousand Dutch pupils, with the analysis and "
            "moderators set in advance. They found no effect of stereotype threat on girls' maths scores. "
            "<bookmark mark='d'/> Meta-analyses of the literature have found signs of publication bias. The effect "
            "may exist in some settings, but registered tests have not found it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(hidden), FadeIn(shown), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeOut(hidden), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(big, scale=1.5), FadeIn(bl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
