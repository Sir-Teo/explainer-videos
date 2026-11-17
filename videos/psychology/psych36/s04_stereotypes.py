from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


class Stereotypes(VoiceoverScene):
    def construct(self):
        self.card()
        self.categories()
        self.content()
        self.illusory()

    def card(self):
        card = chapter_card(3, r"Stereotypes", r"Where do beliefs about groups come from?",
                            lit={1976: r"Hamilton \& Gifford", 2002: r"Fiske et al."}, part=PART,
                            scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter three. Stereotypes."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def categories(self):
        head = heading(r"A stereotype is a category")
        rows = rows_of([
            (r"Part 22: \ a category stores what its members tend to have, \ so a new member can be guessed from "
             r"its label", WHITE),
            (r"a stereotype is the same machinery pointed at people: \ a prior about a person from their group", CROWD),
            (r"priors are not wrong in themselves; \ they go wrong when they are inaccurate, \ or when they are "
             r"used instead of the evidence about the person in front of you", AUTH),
            (r"and unlike a category of birds, \ a stereotype has consequences for the people in it: \ who is "
             r"hired, \ stopped, \ believed", YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "Start with what a stereotype is. <bookmark mark='a'/> Part 22 showed that a category stores what its "
            "members tend to have, so a new member can be guessed from its label. <bookmark mark='b'/> A "
            "stereotype is the same machinery pointed at people: a prior about a person from their group. "
            "<bookmark mark='c'/> Priors aren't wrong in themselves. They go wrong when they're inaccurate, or "
            "when they're used instead of the evidence about the person in front of you. <bookmark mark='d'/> And "
            "unlike a category of birds, a stereotype has consequences for the people in it: who is hired, who is "
            "stopped, who is believed."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def content(self):
        head = heading(r"Warmth and competence")
        A = axes([0, 1], [0, 1], x_length=4.6, y_length=4.0, xticks=None, yticks=None, xlabel=r"warmth",
                 ylabel=r"competence", center=[-3.6, -0.3, 0], font_size=17)
        quads = VGroup(*[label(t, font_size=15, color=c).move_to(A.ax.c2p(x, y)) for t, x, y, c in (
            (r"envied", 0.25, 0.78, OUTG), (r"admired", 0.75, 0.78, GOOD), (r"scorned", 0.25, 0.22, GREY_A),
            (r"pitied", 0.75, 0.22, IN))])
        cross = VGroup(DashedLine(A.ax.c2p(0.5, 0), A.ax.c2p(0.5, 1), color=GREY_D),
                       DashedLine(A.ax.c2p(0, 0.5), A.ax.c2p(1, 0.5), color=GREY_D))
        rows = rows_of([
            (r"Fiske, \ Cuddy, \ Glick and Xu, \ 2002: \ the stereotype content model", WHITE),
            (r"groups are placed on two dimensions: \ warmth, \ are they for us or against us? \ and competence, \ "
             r"can they act on it?", CROWD),
            (r"perceived status predicts competence; \ perceived competition predicts coldness", MODEL),
            (r"many stereotypes are mixed: \ competent but cold draws envy; \ warm but incompetent draws pity", YOU),
        ], 6.0, 20, 0.36).move_to([3.3, -0.3, 0])
        tag = historical_tag(r"Fiske, \ Cuddy, \ Glick \& Xu (2002)")
        with self.voiceover(
            "What do stereotypes contain? <bookmark mark='a'/> In 2002 Susan Fiske and colleagues proposed the "
            "stereotype content model. <bookmark mark='b'/> Groups are placed on two dimensions. Warmth: are they "
            "for us or against us? And competence: can they act on it? <bookmark mark='c'/> A group's perceived "
            "status predicts how competent it seems, and perceived competition predicts how cold. "
            "<bookmark mark='d'/> So many stereotypes are mixed. Competent but cold draws envy. Warm but "
            "incompetent draws pity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(cross))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(quads), FadeIn(rows[3]))
        self.clear_scene()

    def illusory(self):
        d = load("illusory")
        head = heading(r"A correlation that is not there")
        A = axes([-0.6, 1.6], [0, 0.6], x_length=4.4, y_length=3.4, xticks=None, yticks=[0, 0.3, 0.6],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"share of acts that were undesirable",
                 center=[-3.9, -0.4, 0], font_size=15)
        actual = bars(A.ax, [-0.15, 0.85], d["actual"], [GREY_B, GREY_B], width=0.28)
        judged = bars(A.ax, [0.15, 1.15], d["b6"], [IN, OUTG], width=0.28)
        names = VGroup(label(r"group A: \ 26", font_size=15, color=IN).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       label(r"group B: \ 13", font_size=15, color=OUTG).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15))
        key = legend([(GREY_B, r"as shown"), (OUTG, r"as remembered (model)")], font_size=14).move_to(
            A.ax.c2p(0.5, 0.56))
        rows = rows_of([
            (r"Hamilton and Gifford, \ 1976: \ people read about members of two groups, \ A twice as large as B, \ "
             r"with desirable and undesirable acts in the same 9 to 4 ratio", WHITE),
            (r"they judged the smaller group worse", OUTG),
            (r"the rare group's rare acts stand out: \ if they are remembered more strongly, \ here 1.6 times, \ "
             rf"B's undesirable share is remembered as {pct(d['b6'][1])} instead of {pct(d['actual'][1])}", MODEL),
            (r"a minority can acquire a bad name with no difference in behaviour at all", YOU),
        ], 6.4, 20, 0.34).move_to([3.0, -0.3, 0])
        tag = historical_tag(r"Hamilton \& Gifford (1976)")
        with self.voiceover(
            "Stereotypes can form even without any real difference. <bookmark mark='a'/> In 1976 Hamilton and "
            "Gifford had people read about members of two groups. Group A was twice as large as group B, and both "
            "did desirable and undesirable things in the same nine to four ratio. <bookmark mark='b'/> People "
            "judged the smaller group worse. <bookmark mark='c'/> The rare group's rare acts stand out. If they're "
            "remembered more strongly, here one point six times as strongly, group B's undesirable share is "
            f"remembered as {spct(d['b6'][1])} instead of {spct(d['actual'][1])}. <bookmark mark='d'/> So a "
            "minority can acquire a bad name with no difference in behaviour at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), GrowFromEdge(actual[0], DOWN), GrowFromEdge(actual[1], DOWN))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(judged[0], DOWN), GrowFromEdge(judged[1], DOWN), FadeIn(key), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
